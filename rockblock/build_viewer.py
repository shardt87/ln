"""Inject the ER-RB model (three campus sizes), the takeoff and the basis register into viewer/template.html ->
viewer/index.html. The viewer instances the block template itself; circuits and site parts are sent absolute."""
import json
import os

import basis as BS
import model as M
import takeoff as TO

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = (250, 500, 1000)
COLORS = {
    "encl": "#c9cdcf", "steel_dark": "#2a2e33", "louvre": "#5f676d", "seam": "#3a4045", "panel": "#8d949a",
    "steel": "#9aa1a6", "stack": "#b8bec2", "concrete": "#6e706d", "gcb": "#a7afb4", "xfmr": "#76847a",
    "radiator": "#66726a", "insul": "#8a5a36", "ehouse": "#b7bcc0", "roof": "#596066", "hvac": "#8c9399",
    "door": "#474e54", "ghost": "#5a6f86", "own": "#d8402f", "fence": "#8a9096", "road": "#26292c",
    "building": "#8f969c", "glass": "#3d5468", "berm": "#4b5640", "water": "#2c5873", "gaspipe": "#7f878c",
    "valve": "#9a3a30", "ownwall": "#d8402f",
}
CI = {c: i for i, c in enumerate(COLORS)}
R = lambda v: round(v, 2)


def parts(P, with_layer=False):
    out = []
    for p in P:
        kind, c, g = p[0], p[1], p[2]
        lay = p[3] if with_layer else None
        if kind == "h":
            nums = [*g[0], *g[1], g[2]]
        else:
            nums = list(g)
        row = [kind, CI[c]] + [R(x) for x in nums]
        if with_layer:
            row.insert(2, {"base": 0, "dc": 1, "gas": 2}[lay])
        out.append(row)
    return out


def size_data(mw):
    m = M.build(mw)
    t = TO.takeoff(mw)
    lay = m["layout"]
    SP, SI = m["site"]
    constr = []

    def ci(s):
        if s not in constr:
            constr.append(s)
        return constr.index(s)

    circ = []
    for c, r in zip(m["circuits"], t["rows"]):
        circ.append([c["layer"], c["tag"], c["frm"], c["to"], c["runs"], c["cond"], [R(v) for p in c["pts"] for v in p],
                     r["routed"], r["risers"], r["terminations"], r["slack"], r["cut_measured"], r["cut_assumed"],
                     r["cft_measured"], r["cft_assumed"], ci(c["constr"]), c["kind"], c["group"] if c["group"] is not None else -1,
                     c["block"] or 0])
    per = {}
    for r in t["rows"]:
        d = per.setdefault(r["layer"], [0, 0, 0, 0.0, 0.0])
        d[0] += 1
        d[1] += r["cft_measured"]
        d[2] += r["cft_assumed"]
        d[3] += r["cut_measured"] * r["runs"]
        d[4] += r["cut_assumed"] * r["runs"]
    return dict(
        params=lay["params"],
        blocks=[[b["n"], b["bx"], b["by"], b["s"], b["group"]] for b in lay["blocks"]],
        groups=[[g["tag"], g["gx"], g["gy"], g["lineup"], len(g["blocks"])] for g in lay["groups"]],
        lineups=[[L["tag"], L["sy0"], L["band_y"], len(L["groups"])] for L in lay["lineups"]],
        site=lay["site"], siteParts=parts(SP, True),
        siteItems=[[i["tag"], i["name"], i["key"], i["status"], i["info"], i["src"], [R(v) for v in i["fp"]],
                    [R(v) for v in i["z"]], i["p0"], i["p1"]] for i in SI],
        circ=circ, constr=constr, per={k: [v[0], v[1], v[2], round(v[3]), round(v[4])] for k, v in per.items()},
    )


def main():
    P, I = M.TEMPLATE
    data = dict(
        doc=BS.DOC, credit=BS.CREDIT, stamp=BS.STAMP, colors=list(COLORS.values()), cnames=list(COLORS),
        layers=[list(x) for x in BS.LAYERS], key=BS.KEY,
        register=[[k, str(v[0]) if not isinstance(v[0], tuple) else " x ".join(f"{x:g}" for x in v[0]), v[1], v[2], v[3], v[4]]
                  for k, v in BS.B.items()],
        assumed=BS.ASSUMED_LEN, defaultBasis=TO.DEFAULT_BASIS,
        allow=dict(term_lv=BS.v("term_lv"), term_mv=BS.v("term_mv"), slack=BS.v("slack"), spare=BS.v("spare"),
                   depth_lv=BS.v("depth_lv"), depth_mv=BS.v("depth_mv")),
        tpl=dict(parts=parts(P), items=[[i["role"], i.get("k", 0), [R(v) for v in i["fp"]], [R(v) for v in i["z"]],
                                         i["parts"][0], i["parts"][1]] for i in I]),
        sizes={str(mw): size_data(mw) for mw in SIZES},
    )
    tpl = open(os.path.join(HERE, "viewer", "template.html")).read()
    js = json.dumps(data, separators=(",", ":"))
    out = tpl.replace("/*__DATA__*/null", js)
    p = os.path.join(HERE, "viewer", "index.html")
    open(p, "w").write(out)
    print("wrote", p, len(out), "bytes")


if __name__ == "__main__":
    main()
