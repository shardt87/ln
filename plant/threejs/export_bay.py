#!/usr/bin/env python3
"""Export one equipment bay of the model as compact JSON for gt1_bay_scene.js.

    python3 plant/threejs/export_bay.py [x0 x1 y0 y1]   # default: GT train 1 bay

Parts: [0, box...] [1, rod...] [2, hex...] [3, prism...] with a colour index
into the palette; routes: [z, w, h, colour, points].
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(HERE, "..", "sk3x1_model.json")))
pal = json.load(open(os.path.join(HERE, "..", "palette.json")))
box = tuple(map(float, sys.argv[1:5])) if len(sys.argv) >= 5 else (548, 712, 296, 828)
cols = sorted(pal)
ci = {c: i for i, c in enumerate(cols)}
r = lambda v: round(v, 1)


def anchor(p):
    return p.get("min") or p.get("a") or p["v"][0]


enc = []
for p in m["parts"]:
    a = anchor(p)
    if not (box[0] <= a[0] <= box[1] and box[2] <= a[1] <= box[3]) or p["layer"].startswith(("OPT_", "R1_", "SITE")):
        continue
    c = ci.get(p["color"], ci["equip"])
    if p["kind"] == "box":
        enc.append([0, *map(r, p["min"]), *map(r, p["max"]), c])
    elif p["kind"] == "rod":
        enc.append([1, *map(r, p["a"]), *map(r, p["b"]), round(p["r"], 2), round(p["r2"], 2), c, p.get("seg", 16)])
    elif p["kind"] == "prism":
        enc.append([3, *map(r, p["min"]), *map(r, p["max"]), c, 1 if p.get("ridge") == "x" else 0])
    else:
        enc.append([2, *[r(v) for q in p["v"] for v in q], c])
rts = [[rt["z"], rt["w"], rt["h"], ci[rt["color"]], rt["points"]] for rt in m["routes"]
       if rt["z"] > 0 and not rt["layer"].startswith("OPT")
       and all(box[0] <= x <= box[1] and box[2] <= y <= box[3] for x, y in rt["points"])]
out = os.path.join(HERE, "gt1_bay.json")
json.dump(dict(c=[pal[k]["hex"] for k in cols], k=cols, p=enc, r=rts), open(out, "w"), separators=(",", ":"))
print(f"wrote {out}: {len(enc)} parts, {len(rts)} routes")
