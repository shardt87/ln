"""Plant-wide discrepancy scan (user review: things that look wrong at eye level, that verify / audit do not catch).
1. tray route ends that neither drop, enter a building / equipment face, continue on another tray, nor bend;
2. floating parts: above grade and touching nothing (with a 0.3 ft tolerance);
3. printed signs / labels hanging in the air (no part within 0.6 ft of the panel centre).
Prints counts and the worst offenders by item."""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
I = {i["id"]: i for i in G["items"]}


def bb(p):
    if p["kind"] in ("box", "prism"):
        return p["min"] + p["max"]
    if p["kind"] == "rod":
        a, b, r = p["a"], p["b"], max(p["r"], p.get("r2", p["r"]))
        return [min(a[0], b[0]) - r, min(a[1], b[1]) - r, min(a[2], b[2]) - r,
                max(a[0], b[0]) + r, max(a[1], b[1]) + r, max(a[2], b[2]) + r]
    xs, ys, zs = zip(*p["v"])
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]


P = G["parts"]
B = [bb(p) for p in P]
grid = defaultdict(list)
for k, b in enumerate(B):
    if b[3] - b[0] > 300 or b[4] - b[1] > 300:
        continue
    for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
        for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
            grid[(gx, gy)].append(k)
BIG = [k for k, b in enumerate(B) if b[3] - b[0] > 300 or b[4] - b[1] > 300]


def near(box, m, skip=None):
    out = []
    for gx in range(int((box[0] - m) // 10), int((box[3] + m) // 10) + 1):
        for gy in range(int((box[1] - m) // 10), int((box[4] + m) // 10) + 1):
            for k in grid.get((gx, gy), ()):
                if k == skip:
                    continue
                b = B[k]
                if b[0] - m <= box[3] and b[3] + m >= box[0] and b[1] - m <= box[4] and b[4] + m >= box[1] \
                        and b[2] - m <= box[5] and b[5] + m >= box[2]:
                    out.append(k)
    for k in BIG:
        b = B[k]
        if k != skip and b[0] - m <= box[3] and b[3] + m >= box[0] and b[1] - m <= box[4] and b[4] + m >= box[1] \
                and b[2] - m <= box[5] and b[5] + m >= box[2]:
            out.append(k)
    return out


# 1. floating parts
flo = defaultdict(list)
for k, (p, b) in enumerate(zip(P, B)):
    if b[2] < .6 or I[p["item"]]["layer"] in ("UNDERGROUND", "OPT_UNDERGROUND"):
        continue
    if not near(b, .3, skip=k):
        flo[I[p["item"]]["name"]].append([round(v, 1) for v in b[:3]])
# 2. hanging signs
hang = defaultdict(list)
for d in G.get("decals", []):
    c = d["c"]
    box = [c[0] - .05, c[1] - .05, c[2] - .05, c[0] + .05, c[1] + .05, c[2] + .05]
    if c[2] > .5 and abs(d["n"][2]) < .5 and not near(box, max(.6, d["w"] / 2)):
        hang[I.get(d["item"], {"name": "?"})["name"]].append([round(v, 1) for v in c])
# 3. tray ends with nothing at them
ends = defaultdict(list)
for r in G["routes"]:
    if r.get("surface") or r["z"] <= 0 or not r["type"].endswith("tray"):
        continue
    for p in (r["points"][0], r["points"][-1]):
        ends[(round(p[0], 1), round(p[1], 1), r["z"])].append(r)
tray_items = {i["id"] for i in G["items"] if i["name"].startswith("Cable trays and isolated")}
dead = []
for (x, y, z), rs in ends.items():
    box = [x - 2.5, y - 2.5, z - 30, x + 2.5, y + 2.5, z - .6]           # a drop / riser below the end
    vert = [k for k in near(box, 0) if P[k]["item"] in tray_items and B[k][5] - B[k][2] > .5]
    face = [k for k in near([x - 1.5, y - 1.5, z - 1, x + 1.5, y + 1.5, z + 1], 0) if P[k]["item"] not in tray_items]
    cont = sum(1 for (x2, y2, z2) in ends if (x2, y2) == (x, y) and z2 != z) or len(rs) > 1
    if not cont:                                                       # tee onto another tray run at this tier
        for r2 in G["routes"]:
            if r2 in rs or r2.get("surface") or abs(r2["z"] - z) > .6 or not r2["type"].endswith("tray"):
                continue
            for a_, b_ in zip(r2["points"], r2["points"][1:]):
                if min(a_[0], b_[0]) - 1 <= x <= max(a_[0], b_[0]) + 1 and min(a_[1], b_[1]) - 1 <= y <= max(a_[1], b_[1]) + 1:
                    cont = True
                    break
            if cont:
                break
    if not vert and not face and not cont:
        dead.append((x, y, z, rs[0]["label"]))
print(f"floating parts: {sum(len(v) for v in flo.values())} in {len(flo)} items")
for n, v in sorted(flo.items(), key=lambda t: -len(t[1]))[:25]:
    print("  ", len(v), n[:70], v[:2])
print(f"hanging signs: {sum(len(v) for v in hang.values())} in {len(hang)} items")
for n, v in sorted(hang.items(), key=lambda t: -len(t[1]))[:15]:
    print("  ", len(v), n[:70], v[:2])
print(f"tray ends with no drop / entry / continuation: {len(dead)}")
for d in dead[:25]:
    print("  ", d)
