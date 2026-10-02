#!/usr/bin/env python3
"""Export sk3x1_model.json to Wavefront OBJ + MTL for Blender, SketchUp,
Rhino and similar tools. One OBJ group per equipment item, one material per
colour key; the layer (SK-3X1-11 collection) is kept in each group name.

    python3 plant/export_obj.py            # Y-up (Blender / glTF convention)
    python3 plant/export_obj.py --zup      # native X east, Y north, Z up
    python3 plant/export_obj.py --base     # base plant only (no OPT_* layers)

Units are feet.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZUP = "--zup" in sys.argv
BASE_ONLY = "--base" in sys.argv
PALETTE = json.load(open(os.path.join(HERE, "palette.json")))
model = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
items = {it["id"]: it for it in model["items"]}
verts, groups = [], {}


def V(p):
    x, y, z = p
    verts.append((x, y, z) if ZUP else (x, z, -y))
    return len(verts)


def box(f, lo, hi):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    p = [V((x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
        f.append([p[i] for i in q])


def rod(f, a, b, r1, r2, n):
    ax = [b[i] - a[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in ax)) or 1
    ax = [c / L for c in ax]
    ref = (1, 0, 0) if abs(ax[0]) < 0.9 else (0, 1, 0)
    u = [ax[1] * ref[2] - ax[2] * ref[1], ax[2] * ref[0] - ax[0] * ref[2], ax[0] * ref[1] - ax[1] * ref[0]]
    un = math.sqrt(sum(c * c for c in u)); u = [c / un for c in u]
    w = [ax[1] * u[2] - ax[2] * u[1], ax[2] * u[0] - ax[0] * u[2], ax[0] * u[1] - ax[1] * u[0]]
    rings = []
    for end, r in ((a, r1), (b, r2)):
        rings.append([V([end[i] + r * (math.cos(2 * math.pi * k / n) * u[i] + math.sin(2 * math.pi * k / n) * w[i])
                         for i in range(3)]) for k in range(n)])
    for k in range(n):
        f.append([rings[0][k], rings[0][(k + 1) % n], rings[1][(k + 1) % n], rings[1][k]])
    f.append(list(reversed(rings[0]))); f.append(rings[1])


def prism(f, lo, hi, ridge):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    if ridge == "x":
        ym = (y0 + y1) / 2
        a, b, c, d, e, g = [V(p) for p in ((x0, y0, z0), (x0, y1, z0), (x0, ym, z1), (x1, y0, z0), (x1, y1, z0), (x1, ym, z1))]
    else:
        xm = (x0 + x1) / 2
        a, b, c, d, e, g = [V(p) for p in ((x0, y0, z0), (x1, y0, z0), (xm, y0, z1), (x0, y1, z0), (x1, y1, z0), (xm, y1, z1))]
    f += [[a, b, c], [d, g, e], [a, c, g, d], [b, e, g, c], [a, d, e, b]]


def hexa(f, v):
    p = [V(q) for q in v]
    for q in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        f.append([p[i] for i in q])


for p in model["parts"]:
    it = items[p["item"]]
    if BASE_ONLY and p["layer"].startswith(("OPT_", "HV_CORRIDOR", "SWYD_FUTURE")):
        continue
    safe = "".join(ch if ch.isalnum() else "_" for ch in it["name"])
    key = (f"{p['layer']}__{it['id']}_{safe}", p["color"])
    f = groups.setdefault(key, [])
    k = p["kind"]
    if k == "box":
        box(f, p["min"], p["max"])
    elif k == "rod":
        rr = max(p["r"], p["r2"])
        rod(f, p["a"], p["b"], p["r"], p["r2"], p.get("seg", 32 if rr > 10 else 16))
    elif k == "prism":
        prism(f, p["min"], p["max"], p.get("ridge", "y"))
    elif k == "hex":
        hexa(f, p["v"])
for n, r in enumerate(model["routes"]):
    if BASE_ONLY and r["layer"].startswith(("OPT_", "HV_CORRIDOR")):
        continue
    if r["type"] == "cable_trench":
        continue                      # exported as parts (switchyard.py)
    if r["z"] > 0 and r["type"] in ("steam", "condensate", "feedwater", "ccw", "fuel_gas", "fuel_oil", "cw",
                                    "chw", "hydrogen", "lng", "mv_tray", "lv_tray", "control_tray", "ipb", "water",
                                    "aux_steam"):
        continue                      # exported as parts (round pipes, ladder trays, IPB)
    f = groups.setdefault((f"{r['layer']}__route_{n:03d}_{r['type']}", r["color"]), [])
    z = 0.2 if r["z"] < 0 else r["z"]
    h = 0.4 if r["z"] < 0 else r["h"]
    hw = r["w"] / 2
    for (ax, ay), (bx, by) in zip(r["points"], r["points"][1:]):
        if ax != bx and ay != by:
            continue
        box(f, (min(ax, bx) - hw, min(ay, by) - hw, z - h / 2), (max(ax, bx) + hw, max(ay, by) + hw, z + h / 2))

name = "sk3x1_model" + ("_base" if BASE_ONLY else "") + ("_zup" if ZUP else "")
used = sorted({c for (_, c) in groups})
with open(os.path.join(HERE, name + ".mtl"), "w") as fh:
    for c in used:
        hx = PALETTE[c]["hex"].lstrip("#")
        r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
        fh.write(f"newmtl {c}\nKd {r:.3f} {g:.3f} {b:.3f}\nKa 0 0 0\nd {PALETTE[c].get('opacity', 1)}\n\n")
with open(os.path.join(HERE, name + ".obj"), "w") as fh:
    fh.write(f"# {model['title']}\n# units: feet; {'Z up' if ZUP else 'Y up'}\n# {model['disclaimer']}\n")
    fh.write(f"mtllib {name}.mtl\n")
    fh.write("".join(f"v {x:.2f} {y:.2f} {z:.2f}\n" for x, y, z in verts))
    for (g, c), faces in groups.items():
        fh.write(f"g {g}\nusemtl {c}\n")
        fh.write("".join("f " + " ".join(map(str, q)) + "\n" for q in faces))
print(f"wrote {name}.obj: {len(verts)} vertices, {len(groups)} groups")
