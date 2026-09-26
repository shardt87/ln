#!/usr/bin/env python3
"""Export sk3x1_model.json to Wavefront OBJ + MTL (one group per object,
one material per colour key) for Blender, SketchUp, Rhino, etc.

OBJ axes: X east, Y up, Z south (Y-up convention); units feet.
Use --zup to keep the model's native X east, Y north, Z up.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZUP = "--zup" in sys.argv
BASE_ONLY = "--base" in sys.argv

COL = {"ground": "dfe3dc", "road": "c9ccca", "fence": "8f9aa1", "hall": "c7d3da", "pad": "d8d6cc",
       "concrete": "bfc2bc", "machine": "7d8a93", "amber": "e8c77a", "hrsg": "b9c3c9", "stack": "9aa4aa",
       "duct": "a3adb3", "filter": "a9b3b9", "steel": "6f7a82", "acc": "c5cbc8", "fan": "8e999f",
       "xfmr": "8c969c", "ehouse": "aab4ba", "building": "d4d9db", "motor": "97a2a8", "tank": "d9e2e4",
       "rack": "b07d4a", "gravel": "bfc6c9", "conductor": "3a4650", "future": "cdd6da",
       "corridor": "d5dfe8", "water": "7fa6b8", "conditional": "e0c07a", "ccs": "d7dedf",
       "tower": "b6c6cc", "bess": "a9bdc4", "equip": "b3bcc1", "copper": "b87333",
       "copper_dark": "8a4f1d", "ductbank": "c79a6a", "steam": "4f5b66", "condensate": "3d8f8f",
       "feedwater": "2f6f9f", "ccw": "7d8f4e", "fuelgas": "9c7a3c", "cw": "6b9ac4", "chw": "5d7fb5",
       "hydrogen": "2e8b6f", "lng": "4a78a8"}

model = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
verts, lines = [], []


def V(x, y, z):
    verts.append((x, y, z) if ZUP else (x, z, -y))
    return len(verts)


def face(*ids):
    lines.append("f " + " ".join(str(i) for i in ids))


def box(x0, y0, z0, x1, y1, z1):
    p = [V(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
        face(*(p[i] for i in q))


def cylinder(a, b, r, n=24):
    """Cylinder between points a and b (model coordinates)."""
    ax = [b[i] - a[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in ax))
    ax = [c / L for c in ax]
    ref = (1, 0, 0) if abs(ax[0]) < 0.9 else (0, 1, 0)
    u = [ax[1] * ref[2] - ax[2] * ref[1], ax[2] * ref[0] - ax[0] * ref[2], ax[0] * ref[1] - ax[1] * ref[0]]
    un = math.sqrt(sum(c * c for c in u)); u = [c / un for c in u]
    w = [ax[1] * u[2] - ax[2] * u[1], ax[2] * u[0] - ax[0] * u[2], ax[0] * u[1] - ax[1] * u[0]]
    ring = []
    for end in (a, b):
        ids = []
        for k in range(n):
            t = 2 * math.pi * k / n
            ids.append(V(*[end[i] + r * (math.cos(t) * u[i] + math.sin(t) * w[i]) for i in range(3)]))
        ring.append(ids)
    for k in range(n):
        face(ring[0][k], ring[0][(k + 1) % n], ring[1][(k + 1) % n], ring[1][k])
    face(*reversed(ring[0])); face(*ring[1])


def prism(x0, y0, z0, x1, y1, z1):
    xm = (x0 + x1) / 2
    a, b, c = V(x0, y0, z0), V(x1, y0, z0), V(xm, y0, z1)
    d, e, f = V(x0, y1, z0), V(x1, y1, z0), V(xm, y1, z1)
    face(a, b, c); face(d, f, e); face(a, c, f, d); face(b, e, f, c); face(a, d, e, b)


for o in model["objects"]:
    if BASE_ONLY and o["layer"].startswith("OPT_"):
        continue
    lines.append(f"g {o['id']}_{''.join(ch if ch.isalnum() else '_' for ch in o['name'])[:60]}")
    lines.append(f"usemtl {o['color']}")
    k = o["kind"]
    if k == "box":
        (x0, y0, z0), (x1, y1, z1) = o["min"], o["max"]
        box(x0, y0, z0, x1, y1, max(z1, z0 + 0.1))
    elif k == "prism":
        prism(*o["min"], *o["max"])
    elif k == "cyl":
        cx, cy = o["center"]
        cylinder((cx, cy, o["z0"]), (cx, cy, o["z1"]), o["r"], 32 if o["r"] > 10 else 16)
    elif k == "hcyl":
        (x0, y0, z0), (x1, y1, z1) = o["min"], o["max"]
        zc = (z0 + z1) / 2
        if o["axis"] == "x":
            yc = (y0 + y1) / 2; cylinder((x0, yc, zc), (x1, yc, zc), o["r"], 16)
        else:
            xc = (x0 + x1) / 2; cylinder((xc, y0, zc), (xc, y1, zc), o["r"], 16)

for n, r in enumerate(model["routes"]):
    if BASE_ONLY and r["layer"].startswith("OPT_"):
        continue
    lines.append(f"g route_{n:03d}_{r['type']}")
    lines.append(f"usemtl {r['color']}")
    z = 0.2 if r["z"] < 0 else r["z"]
    h = 0.4 if r["z"] < 0 else r["h"]
    hw = r["w"] / 2
    for (ax, ay), (bx, by) in zip(r["points"], r["points"][1:]):
        if ax != bx and ay != by:
            continue
        box(min(ax, bx) - hw, min(ay, by) - hw, z - h / 2, max(ax, bx) + hw, max(ay, by) + hw, z + h / 2)

name = "sk3x1_model" + ("_base" if BASE_ONLY else "")
with open(os.path.join(HERE, name + ".mtl"), "w") as f:
    for k, hexc in COL.items():
        r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
        f.write(f"newmtl {k}\nKd {r:.3f} {g:.3f} {b:.3f}\nKa 0 0 0\nd {'0.35' if k == 'hall' else '1'}\n\n")
with open(os.path.join(HERE, name + ".obj"), "w") as f:
    f.write(f"# {model['title']}\n# units: feet; {'Z up' if ZUP else 'Y up'}\n# {model['disclaimer']}\n")
    f.write(f"mtllib {name}.mtl\n")
    f.write("".join(f"v {x:.2f} {y:.2f} {z:.2f}\n" for x, y, z in verts))
    f.write("\n".join(lines) + "\n")
print(f"wrote {name}.obj: {len(verts)} vertices")
