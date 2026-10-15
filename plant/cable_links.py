"""Cable continuity pass (user audit: "every cable connected"): ladder risers wherever two tray tiers meet at one
point without a vertical connection (a tray route ending at EL 44 over the start of an EL 30 branch, ...).
Run after the trays are rendered. The riser is a vertical ladder (two rails, rungs every foot) with the tray's
cables running down it, drawn on the tray item."""
from collections import defaultdict

import fuel
from fuel import box, rod

CAB = (("cable_tc", .16), ("cable_mc", .2), ("cable_tc", .16), ("cable_mc", .2))


def build(routes):
    tr = next(i for i in fuel.G["items"] if i["name"].startswith("Cable trays and isolated"))
    ends = defaultdict(set)
    for r in routes:
        if r.get("surface") or r["z"] <= 0 or not r["type"].endswith("tray"):
            continue
        for p in (r["points"][0], r["points"][-1]):
            ends[(round(p[0], 1), round(p[1], 1))].add(r["z"])
    # existing vertical cable already spanning the tiers?
    vert = [p for p in fuel.G["parts"] if p["kind"] == "rod" and str(p["color"]).startswith("cable")
            and abs(p["a"][0] - p["b"][0]) < .05 and abs(p["a"][1] - p["b"][1]) < .05 and abs(p["a"][2] - p["b"][2]) > 2]
    fuel.on(tr)
    fuel.D = True
    n = 0
    for (x, y), zs in ends.items():
        zs = sorted(zs)
        for z0, z1 in zip(zs, zs[1:]):
            if any(abs(v["a"][0] - x) < 2 and abs(v["a"][1] - y) < 2 and min(v["a"][2], v["b"][2]) <= z0 + 1
                   and max(v["a"][2], v["b"][2]) >= z1 - 1 for v in vert):
                continue
            for s in (-.75, .75):                                                   # rails
                rod((x + s, y, z0 - .4), (x + s, y, z1 + .1), .06, "pipe", seg=4)
            z = z0
            while z < z1:
                box(x - .75, x + .75, y - .05, y + .05, z - .04, z + .04, "pipe")      # rungs
                z += 1
            k = 0
            for dx in (-.45, 0, .45):                                               # cable bundle on the ladder
                for dy in (-.45, 0, .45):
                    c, r = CAB[k % len(CAB)]
                    rod((x + dx, y + dy, z0 - .2), (x + dx, y + dy, z1 + .3), r * .8, c, seg=6)
                    k += 1
            n += 1
    # tray ends that got no drop (e.g. a pipe below the end blocked the drop ladder) over equipment 0.5-4 ft below:
    # the cables bend down into top glands on it
    parts = fuel.G["parts"]
    items = {i["id"]: i for i in fuel.G["items"]}
    def has_drop(x, y, z):
        return any(p["kind"] == "rod" and str(p["color"]).startswith("cable") and abs(p["a"][0] - x) < 2.5
                   and abs(p["a"][1] - y) < 2.5 and abs(p["a"][0] - p["b"][0]) < .05 and abs(p["a"][1] - p["b"][1]) < .05
                   and min(p["a"][2], p["b"][2]) < z - .5 for p in parts)
    fuel.on(tr)
    fuel.D = True
    for r in routes:
        if r.get("surface") or r["z"] <= 0 or not r["type"].endswith("tray"):
            continue
        for p0, p1 in ((r["points"][0], r["points"][1] if len(r["points"]) > 1 else None),
                       (r["points"][-1], r["points"][-2] if len(r["points"]) > 1 else None)):
            if p1 is None:
                continue
            x, y, z = p0[0], p0[1], r["z"]
            if any(len(r2["points"]) > 1 and r2 is not r and r2["z"] > 0 and not r2.get("surface") and
                   any((abs(q[0] - x) < .2 and abs(q[1] - y) < .2) for q in r2["points"]) for r2 in routes):
                continue                                                   # continues on another tray / riser
            if has_drop(x, y, z):
                continue
            tops = [b["max"][2] for b in parts if b["kind"] == "box" and b["item"] != tr["id"]
                    and b["min"][0] <= x <= b["max"][0] and b["min"][1] <= y <= b["max"][1]
                    and items[b["item"]]["layer"] not in ("SITE",) and .5 <= z - b["max"][2] <= 4
                    and not any(w in items[b["item"]]["name"].lower() for w in ("building", "e-house", "hall"))]
            if not tops:
                continue
            top = max(tops)
            ux, uy = (p0[0] - p1[0]), (p0[1] - p1[1])
            L = (ux * ux + uy * uy) ** .5 or 1
            ux, uy = ux / L, uy / L
            for k, (c, rr) in enumerate(CAB):
                off = -.45 + k * .3
                sx, sy = x - ux * .6 + uy * off, y - uy * .6 - ux * off
                rod((sx, sy, z + .2), (sx + ux * .5, sy + uy * .5, z - .3), rr * .8, c, seg=6)
                rod((sx + ux * .5, sy + uy * .5, z - .3), (sx + ux * .5, sy + uy * .5, top), rr * .8, c, seg=6)
                rod((sx + ux * .5, sy + uy * .5, top), (sx + ux * .5, sy + uy * .5, top + .3), rr * .8 + .08, "steel", seg=8)
            n += 1
    fuel.D = False
    return n
