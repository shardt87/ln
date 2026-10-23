"""Geometry audit of Boiler Row (layer OPT_BOILERS) and the package boiler AB-1: the checks verify.py / audit.py do not
make on dressing parts.

1. dangling ends: every cable and pipe rod end touches another part (equipment, tray, wall, ground, the next segment);
2. unwired equipment: every motor, panel, transformer, e-house and fan has a cable end within reach;
3. floating parts: every group of touching parts reaches the ground (EL 0.35) somewhere;
4. pass-through: no cable or pipe runs through the solid body of a building, tank or piece of equipment.

    python3 tools/boiler_row_audit.py [--list]
"""
import json
import math
import os
import sys
from collections import defaultdict

PLANT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(PLANT, "sw3x1_model.json")))
ITEMS = {i["id"]: i for i in M["items"]}
CABLE = {"cable_mv", "cable_armor", "cable_tc", "cable_inst", "cable_tcx", "cable_mc", "cable", "copper", "conductor"}
WIRING = CABLE | {"alu", "ipb"}              # a conduit stub-up or isolated-phase bus counts as the wiring to equipment
PIPE = {"pipe", "fuelgas", "waterline", "alu", "steel_dark_pipe"}
EQUIP = {"motor", "cabinet", "xfmr", "ehouse", "panel", "lamp"}
SOLID = {"building", "ehouse", "xfmr", "tank", "hrsg_b", "machine", "tower", "cabinet", "motor"}
REGION = (190, 1350, 1440, 1880)
TOL = .35


def bbox(p):
    if "min" in p:
        return (*p["min"], *p["max"])
    r = max(p.get("r", 0), p.get("r2", 0))
    a, b = p["a"], p["b"]
    return (min(a[0], b[0]) - r, min(a[1], b[1]) - r, min(a[2], b[2]) - r,
            max(a[0], b[0]) + r, max(a[1], b[1]) + r, max(a[2], b[2]) + r)


def mine(p):
    it = ITEMS[p["item"]]
    return it["layer"] in ("OPT_BOILERS", "BOILER_ROW_ROOF") or it["name"] in ("Auxiliary boiler", "CEMS shelter, AB-1")


parts = []
for p in M["parts"]:
    if p["kind"] not in ("box", "rod") or ("min" not in p and "a" not in p):
        continue
    b = bbox(p)
    if b[3] < REGION[0] or b[0] > REGION[1] or b[4] < REGION[2] or b[1] > REGION[3]:
        continue
    if ITEMS[p["item"]]["layer"] == "SITE" and not ITEMS[p["item"]]["name"].startswith(("People", "Equipment ID")):
        continue                                                     # ground, fence, lighting, roads: ground level is z
    parts.append((p, b))
G = defaultdict(list)
for k, (p, b) in enumerate(parts):
    for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
        for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
            G[(gx, gy)].append(k)


def near(pt, tol):
    out = set()
    for k in G.get((int(pt[0] // 10), int(pt[1] // 10)), ()):
        b = parts[k][1]
        if b[0] - tol <= pt[0] <= b[3] + tol and b[1] - tol <= pt[1] <= b[4] + tol and b[2] - tol <= pt[2] <= b[5] + tol:
            out.add(k)
    return out


def inside_rod(pt, p, tol):
    a, b = p["a"], p["b"]
    d = [b[i] - a[i] for i in range(3)]
    L2 = sum(v * v for v in d) or 1e-9
    t = max(0, min(1, sum((pt[i] - a[i]) * d[i] for i in range(3)) / L2))
    c = [a[i] + d[i] * t for i in range(3)]
    return math.dist(pt, c) <= max(p.get("r", 0), p.get("r2", 0)) + tol


def touches(pt, k, tol=TOL):
    p, b = parts[k]
    if p["kind"] == "rod":
        return inside_rod(pt, p, tol)
    return True


def label(p):
    return f"{ITEMS[p['item']]['name'][:58]}  [{p['color']}]"


findings = defaultdict(list)
idx = {id(p): k for k, (p, b) in enumerate(parts)}
# 1. dangling ends
for k, (p, b) in enumerate(parts):
    if p["kind"] != "rod" or not mine(p) or p["color"] not in CABLE | PIPE:
        continue
    for end in (p["a"], p["b"]):
        if end[2] <= TOL:
            continue
        hit = [j for j in near(end, TOL + p.get("r", 0)) if j != k and touches(end, j, TOL + p.get("r", 0))]
        if not hit:
            findings["dangling end"].append(f"{label(p)} at ({end[0]:.1f}, {end[1]:.1f}, EL {end[2]:.1f})")
# 2. unwired equipment
cable_ends = [(e, k) for k, (p, b) in enumerate(parts) if p["kind"] == "rod" and p["color"] in WIRING for e in (p["a"], p["b"])]
CE = defaultdict(list)
for e, k in cable_ends:
    CE[(int(e[0] // 10), int(e[1] // 10))].append(e)
for k, (p, b) in enumerate(parts):
    if not mine(p) or p["color"] not in EQUIP or p["kind"] != "box" or ITEMS[p["item"]]["name"] == "Boiler Row sign":
        continue
    vol = (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2])
    if vol < .5:
        continue
    ok = False
    for gx in range(int((b[0] - 3) // 10), int((b[3] + 3) // 10) + 1):
        for gy in range(int((b[1] - 3) // 10), int((b[4] + 3) // 10) + 1):
            for e in CE.get((gx, gy), ()):
                if b[0] - 1.5 <= e[0] <= b[3] + 1.5 and b[1] - 1.5 <= e[1] <= b[4] + 1.5 and b[2] - 1.5 <= e[2] <= b[5] + 1.5:
                    ok = True
    if not ok:
        findings["equipment with no cable"].append(f"{label(p)} box x {b[0]:.0f}-{b[3]:.0f} y {b[1]:.0f}-{b[4]:.0f} "
                                                   f"EL {b[2]:.0f}-{b[5]:.0f}")
# 3. floating groups (touching parts that never reach the ground)
mk = [k for k, (p, b) in enumerate(parts) if mine(p)]
parent = list(range(len(parts)))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


for k, (p, b) in enumerate(parts):
    cells = {(gx, gy) for gx in range(int(b[0] // 10), int(b[3] // 10) + 1) for gy in range(int(b[1] // 10), int(b[4] // 10) + 1)}
    for c in cells:
        for j in G[c]:
            if j <= k:
                continue
            o = parts[j][1]
            if b[0] - .2 <= o[3] and o[0] - .2 <= b[3] and b[1] - .2 <= o[4] and o[1] - .2 <= b[4] and b[2] - .2 <= o[5] and o[2] - .2 <= b[5]:
                parent[find(k)] = find(j)
grounded = {find(k) for k, (p, b) in enumerate(parts) if b[2] <= TOL}
groups = defaultdict(list)
for k in mk:
    r = find(k)
    if r not in grounded:
        groups[r].append(k)
for r, ks in groups.items():
    p, b = parts[ks[0]]
    zs = min(parts[k][1][2] for k in ks)
    findings["floating group"].append(f"{len(ks)} parts, lowest EL {zs:.1f}, e.g. {label(p)} at ({b[0]:.0f}, {b[1]:.0f})")
# 4. cables / pipes through solid bodies
for k, (p, b) in enumerate(parts):
    if p["kind"] != "rod" or not mine(p) or p["color"] not in CABLE | PIPE:
        continue
    a, c = p["a"], p["b"]
    L = math.dist(a, c)
    n = max(2, int(L / 1.5))
    hits = set()
    for i in range(1, n):
        t = i / n
        pt = [a[q] + (c[q] - a[q]) * t for q in range(3)]
        for j in near(pt, 0):
            o, ob = parts[j]
            if j == k or o["kind"] != "box" or o["color"] not in SOLID or o["item"] == p["item"] and o["color"] in ("cabinet", "motor"):
                continue
            inset = .6
            if ob[0] + inset < pt[0] < ob[3] - inset and ob[1] + inset < pt[1] < ob[4] - inset and ob[2] + inset < pt[2] < ob[5] - inset:
                hits.add(j)
    for j in hits:
        findings["runs through a solid body"].append(f"{label(p)} through {label(parts[j][0])}")

# Reviewed and accepted (Oct 23): (check, regex on the finding, reason)
import re
ACCEPT = [
    ("dangling end", r"^Auxiliary boiler  \[pipe\] at \((791\.0, 1629|835\.0, 1630|942\.0, 1524|986\.0, 1525)", "open vent tops (blowdown tank, deaerator)"),
    ("dangling end", r"^Auxiliary boiler  \[pipe\] at \((799\.4, 1628|950\.4, 1523)", "economizer header ends on the casing face"),
    ("equipment with no cable", r"^Auxiliary boiler  \[lamp\]", "pole-mounted area lights, wired inside the pole"),
    ("floating group", r"^2 parts, lowest EL (38|42)\.0, e\.g\. Auxiliary boiler  \[rail\]", "stack ladder cage hoops, drawn 0.2 ft off the stiles"),
    ("runs through a solid body", r"^Auxiliary boiler  \[pipe\] through Auxiliary boiler", "pipes into the boiler's own casing"),
    ("runs through a solid body", r"cable_tc\] through UB-1 cooling tower .*\[ehouse\]", "fan cables leaving the CT MCC"),
    ("runs through a solid body", r"^UB-1 steam-turbine hall .*\[pipe\] through UB-1 heater bay", "main steam and reheat run through the heater bay"),
]
accepted = defaultdict(list)
for key in list(findings):
    keep = []
    for f in set(findings[key]):
        why = next((w for k_, rx, w in ACCEPT if k_ == key and re.search(rx, f)), None)
        (accepted[key].append((f, why)) if why else keep.append(f))
    findings[key] = keep
print(f"Boiler Row geometry audit: {len(mk)} parts checked")
for key in ("dangling end", "equipment with no cable", "floating group", "runs through a solid body"):
    v = findings.get(key, [])
    print(f"  {key:<28} {len(v)}")
    if "--list" in sys.argv:
        for s in sorted(set(v)):
            print("     ", s)
    for f, why in sorted(accepted.get(key, [])):
        print(f"      accepted: {f}  ({why})") if "--list" in sys.argv else None
open_n = sum(len(v) for v in findings.values())
print("RESULT:", "CLEAN" if not open_n else f"{open_n} OPEN", f"({sum(len(v) for v in accepted.values())} reviewed and accepted)")
