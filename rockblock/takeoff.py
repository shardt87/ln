"""ER-RB Rev 00 takeoff: per-block cable kit measured off the model, rolled up to a campus.

cut length  = (routed + risers + terminations + slack) x (1 + spare)
conductor-ft = cut x conductors/run x runs
Every row carries both bases: MEASURED (off the model's routed polyline) and ASSUMED (a stated typical length per run,
basis.ASSUMED_LEN). The basis switch picks one per layer; the roll-up reports the MEASURED and the ASSUMED rows as two
totals, never summed. Construction is family and insulation only: no stock numbers, no dollars."""
import csv
import json
import os
import sys

import basis as BS
import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASIS = {"L1": "MEASURED", "L2": "MEASURED", "L3": "MEASURED", "L4": "MEASURED", "L5": "ASSUMED",
                 "L6": "MEASURED", "L7": "MEASURED"}
LAYER = {k: (n, st) for k, n, _, st, _ in BS.LAYERS}


def row(c):
    mv = c["mv"]
    term = 2 * BS.v("term_mv" if mv else "term_lv")
    if c["layer"] == "L6":
        term = 0.0
    slack = BS.v("slack") * c["routed"]
    cut_m = (c["routed"] + c["risers"] + term + slack) * (1 + BS.v("spare"))
    a = BS.ASSUMED_LEN[c["layer"]]
    if c["kind"] == "L6t":
        a = 12.0
    elif c["kind"] == "L6l":
        a = 200.0
    elif c["kind"] == "L7f":
        a = BS.ASSUMED_LEN["L3"] * 9
    cut_a = (a + term) * (1 + BS.v("spare"))
    return dict(layer=c["layer"], tag=c["tag"], frm=c["frm"], to=c["to"], runs=c["runs"], cond=c["cond"],
                routed=c["routed"], risers=c["risers"], terminations=term, slack=round(slack, 1),
                cut_measured=round(cut_m, 1), cut_assumed=round(cut_a, 1),
                cft_measured=round(cut_m * c["cond"] * c["runs"]), cft_assumed=round(cut_a * c["cond"] * c["runs"]),
                construction=c["constr"], status=LAYER[c["layer"]][1], group=c["group"], block=c["block"], kind=c["kind"])


def takeoff(mw=250, basis=None, **kw):
    basis = dict(DEFAULT_BASIS, **(basis or {}))
    m = M.build(mw, **kw)
    rows = [row(c) for c in m["circuits"]]
    for r in rows:
        r["basis"] = basis[r["layer"]]
        r["cut"] = r["cut_measured"] if r["basis"] == "MEASURED" else r["cut_assumed"]
        r["cft"] = r["cft_measured"] if r["basis"] == "MEASURED" else r["cft_assumed"]
    p = m["layout"]["params"]
    # per-block kit: block 1 (every block is the same template; the measured kit is identical block to block)
    kit = [r for r in rows if r["block"] == 1]
    # roll-up by layer and by basis (two totals, never summed)
    roll = {}
    for r in rows:
        k = r["layer"]
        d = roll.setdefault(k, dict(layer=k, name=LAYER[k][0], status=LAYER[k][1], basis=r["basis"], circuits=0,
                                    cable_ft=0.0, conductor_ft=0))
        d["circuits"] += 1
        d["cable_ft"] += r["cut"] * r["runs"]
        d["conductor_ft"] += r["cft"]
    for d in roll.values():
        d["cable_ft"] = round(d["cable_ft"])
    tot = {b: sum(d["conductor_ft"] for d in roll.values() if d["basis"] == b) for b in ("MEASURED", "ASSUMED")}
    # 35 kV in ER scope vs with the feeders (scope owner TO VERIFY)
    mv_loop = sum(d["conductor_ft"] for k, d in roll.items() if k in ("L3", "L4"))
    mv_fdr = roll.get("L5", {}).get("conductor_ft", 0)
    loops = {}
    for r in rows:
        if r["layer"] == "L3":
            g = M_tag(m, r["group"])
            loops[g] = loops.get(g, 0) + r["cft"]
    return dict(doc=BS.DOC, params=p, basis=basis, kit_block=kit, rollup=list(roll.values()), totals=tot,
                mv35=dict(loops_and_ties_cft=mv_loop, feeders_cft=mv_fdr, feeder_basis=basis["L5"],
                          note="Feeders: scope owner TO VERIFY. Shown separately; the campus 35 kV in ER scope excludes them "
                               "until Cliff confirms."),
                loops_by_group=loops, rows=rows)


def M_tag(m, gid):
    return m["layout"]["groups"][gid]["tag"]


COLS = ["layer", "tag", "frm", "to", "runs", "cond", "routed", "risers", "terminations", "slack", "cut_measured",
        "cut_assumed", "basis", "cut", "cft", "construction", "status"]


def write(mw):
    t = takeoff(mw)
    base = os.path.join(HERE, "out", f"takeoff_{int(mw)}MW")
    with open(base + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([f"{BS.DOC} takeoff, {t['params']['mw']:g} MW campus ({t['params']['n_blocks']} blocks, "
                    f"{t['params']['n_groups']} groups, {t['params']['n_lineups']} lineups). {BS.STAMP}. {BS.CREDIT}."])
        w.writerow(["cut = (routed + risers + terminations + slack) x (1 + spare); conductor-ft = cut x conductors x runs. "
                    "MEASURED and ASSUMED totals are never summed. No stock numbers, no dollars."])
        w.writerow([])
        w.writerow(["PER-BLOCK KIT (RB-001; every block is the same)"])
        w.writerow(COLS)
        for r in t["kit_block"]:
            w.writerow([r[c] for c in COLS])
        w.writerow([])
        w.writerow(["CAMPUS ROLL-UP", "", "", "", "", "", "", "", "", "", "", "", "basis", "cable-ft (cut x runs)",
                    "conductor-ft", "", "status"])
        for d in t["rollup"]:
            w.writerow([d["layer"], d["name"], "", "", d["circuits"], "", "", "", "", "", "", "", d["basis"], d["cable_ft"],
                        d["conductor_ft"], "", d["status"]])
        w.writerow(["TOTAL MEASURED", "", "", "", "", "", "", "", "", "", "", "", "MEASURED", "", t["totals"]["MEASURED"]])
        w.writerow(["TOTAL ASSUMED", "", "", "", "", "", "", "", "", "", "", "", "ASSUMED", "", t["totals"]["ASSUMED"]])
        w.writerow([])
        w.writerow(["ALL CIRCUITS"])
        w.writerow(COLS)
        for r in t["rows"]:
            w.writerow([r[c] for c in COLS])
    out = {k: v for k, v in t.items() if k != "rows"}
    out["circuits"] = len(t["rows"])
    json.dump(out, open(base + ".json", "w"), indent=1)
    return t


def summary(t):
    p = t["params"]
    s = [f"{p['mw']:g} MW: {p['n_blocks']} blocks, {p['n_units']} units, {p['n_groups']} groups, {p['n_lineups']} lineups"]
    for d in t["rollup"]:
        s.append(f"  {d['layer']} {d['name'][:44]:44s} {d['basis']:8s} {d['circuits']:5d} circ  {d['cable_ft']:>10,} cable-ft"
                 f"  {d['conductor_ft']:>11,} cond-ft")
    s.append(f"  MEASURED total {t['totals']['MEASURED']:,} cond-ft | ASSUMED total {t['totals']['ASSUMED']:,} cond-ft (not summed)")
    return "\n".join(s)


if __name__ == "__main__":
    for mw in (250, 500, 1000):
        print(summary(write(mw)))
