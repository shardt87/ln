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
    fuel.D = False
    return n
