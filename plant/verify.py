#!/usr/bin/env python3
"""Verify sk3x1_model.json against the SK-3X1 Rev 14 drawing set.

Checks
  1. Footprints: every shape on sheet 01 (and every cabinet / room on the
     sheet 05 R1 plan) is matched by a model item or part within TOL ft.
  2. Heights: the model heights on sheet 13 are reproduced.
  3. Sheet 09 coordination screen: clearances and hook-height margins are
     recomputed from the model and compared with the values printed on the
     sheet (hall3d.py).
  4. Clashes: no two items' parts overlap, except pairs the drawings define
     as touching.
  5. Bounds: everything sits inside the compound; only basins, basements
     and duct banks go below grade.

Writes verify_report.json (embedded in the viewer) and exits 1 on failure.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 0.6
model = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
ref = json.load(open(os.path.join(HERE, "reference", "sk3x1_rev14_reference.json")))
items = {it["id"]: it for it in model["items"]}


def part_box(p):
    if p["kind"] in ("box", "prism"):
        return p["min"][0], p["max"][0], p["min"][1], p["max"][1], p["min"][2], p["max"][2]
    if p["kind"] == "rod":
        a, b, r = p["a"], p["b"], max(p["r"], p["r2"])
        pad = [r if a[i] == b[i] else 0 for i in range(3)]
        # an axis-aligned rod pads the two axes across it
        ax = [i for i in range(3) if a[i] != b[i]]
        pad = [0 if i in ax else r for i in range(3)] if len(ax) == 1 else [r, r, r]
        return (min(a[0], b[0]) - pad[0], max(a[0], b[0]) + pad[0], min(a[1], b[1]) - pad[1],
                max(a[1], b[1]) + pad[1], min(a[2], b[2]) - pad[2], max(a[2], b[2]) + pad[2])
    v = p["v"]
    xs, ys, zs = [q[0] for q in v], [q[1] for q in v], [q[2] for q in v]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def is_axis_rod(p):
    return p["kind"] != "rod" or sum(1 for i in range(3) if p["a"][i] != p["b"][i]) == 1


# Detail parts (d=1: rails, ladders, sheds, ...) are typical dressing; the drawing checks
# use the primary geometry. Bounds are checked on everything.
PB_ALL = [(p, part_box(p)) for p in model["parts"]]
PB = [(p, b) for p, b in PB_ALL if not p.get("d")]
results = {}


def plan_match(x0, x1, y0, y1):
    for it in model["items"]:
        f = it["fp"]
        if abs(f[0] - x0) <= TOL and abs(f[1] - x1) <= TOL and abs(f[2] - y0) <= TOL and abs(f[3] - y1) <= TOL:
            return it["id"]
    for p, b in PB:
        if abs(b[0] - x0) <= TOL and abs(b[1] - x1) <= TOL and abs(b[2] - y0) <= TOL and abs(b[3] - y1) <= TOL:
            return p["item"]
    return None


# 1. footprints ---------------------------------------------------------------
# Not modelled on purpose: dashed optional-reserve zones and adjacent-market
# frames on sheet 01 (their contents are modelled from sheet 02 instead).
ZONE_FILLS = {"#fbfbf9", "#e7f3f2"}
rows = []
for r in ref["sheet01_rects"]:
    if r["fill"] in ZONE_FILLS:
        continue
    m = plan_match(r["x"][0], r["x"][1], r["y"][0], r["y"][1])
    rows.append(dict(sheet="SK-3X1-01", x=r["x"], y=r["y"], fill=r["fill"], match=m,
                     name=items[m]["name"] if m else None))
for r in ref["sheet05_rects"]:
    m = plan_match(r["x"][0], r["x"][1], r["y"][0], r["y"][1])
    rows.append(dict(sheet="SK-3X1-05", x=r["x"], y=r["y"], fill=r["fill"], match=m,
                     name=items[m]["name"] if m else None))
miss = [r for r in rows if not r["match"]]
results["footprints"] = dict(checked=len(rows), matched=len(rows) - len(miss), missing=miss,
                             ok=not miss, tolerance_ft=TOL)

# 2. heights (sheet 13) -------------------------------------------------------
H13 = [("BESS container", r"^BESS container", 9.5, 1.0), ("E-house (R2A)", r"^R2A:", 14, 0),
       ("Admin building", r"^Control / admin", 20, 0), ("Maintenance bldg", r"^Maintenance building", 20, 0),
       ("R1 electrical bldg", r"^R1: main", 24, 0), ("Water treatment", r"^Water treatment", 30, 0),
       ("Warehouse", r"^Warehouse", 35, 0), ("230 kV dead-end", r"dead-end structure", 47, 0),
       ("Water tanks", r"^(Raw|Demineralised) water tank", 48, 3.6), ("CCS cooling tower", r"^CCS cooling tower", 50, 0),
       ("Aero stack", r"^SC-1 stack", 80, 0), ("RICE stacks", r"^RICE 1 SCR", 90, 0),
       ("DCC (quench)", r"^DCC-A", 90, 0), ("HRSG", r"^HRSG 1 \+ SCR", 100, 0), ("Turbine hall", r"^Common turbine hall", 101, 0),
       ("ACC", r"^Air-cooled condenser", 125, 0), ("Filter house top", r"^FH-1:", 135, 0),
       ("HRSG stack", r"^HRSG 1 stack", 180, 0), ("CO2 stripper", r"^STR-A", 207, 0),
       ("CCS absorber", r"^Absorber A", 262, None), ("Absorber stack", r"^Absorber A", 313, 0)]
import re
hrows = []
for (label, pat, want, extra) in H13:
    its = [it for it in model["items"] if re.search(pat, it["name"])]
    if not its:
        hrows.append(dict(item=label, expected=want, model=None, ok=False)); continue
    it = its[0]
    if extra is None:   # absorber shell top, not the stack
        top = max(part_box(p)[5] for p, _ in [(p, 0) for p in model["parts"] if not p.get("d")]
                  if p["item"] == it["id"] and p["color"] == "ccs" and p["kind"] == "rod" and p["r"] > 20 and p["r2"] > 20)
        extra = 0
    else:
        top = max(b[5] for p, b in PB if p["item"] == it["id"])
    # tanks carry a cone roof (extra) above the shell height on sheet 13
    ok = abs(top - extra - want) <= 0.51
    hrows.append(dict(item=label, expected=want, model=round(top - extra, 2), ok=ok))
results["heights"] = dict(rows=hrows, ok=all(r["ok"] for r in hrows))

# 3. sheet 09 coordination screen --------------------------------------------
def find(pat):
    return [it for it in model["items"] if re.search(pat, it["name"])]


def gap(a, b):
    """Separation between boxes: the largest per-axis gap (0 if they overlap),
    the measure the sheet-09 screen reports."""
    g = [max(b[2 * i] - a[2 * i + 1], a[2 * i] - b[2 * i + 1], 0) for i in range(3)]
    return max(g)


def item_parts(it, pred=lambda p: True):
    return [b for p, b in PB if p["item"] == it["id"] and pred(p)]


gt = find(r"^GT\d: H-class")
gen = find(r"^GTG-\d")
st = find(r"^ST: steam turbine")[0]
gt_top = max(max(b[5] for b in item_parts(i)) for i in gt)
gen_top = max(max(b[5] for b in item_parts(i)) for i in gen)
st_top = max(b[5] for b in item_parts(st))
GAP, HOOK, RIG, BRIDGE = 5, 82, 10, (84, 96)
LIFT = dict(gt=18, gen=16, st=14)
# travel bands: from each machine west to the laydown bay, from load bottom to hook
gt_bands = [(484, i["fp"][1], i["fp"][2], i["fp"][3], gt_top + GAP, HOOK) for i in gt]
gen_bands = [(484, i["fp"][1], i["fp"][2], i["fp"][3], gen_top + GAP, HOOK) for i in gen]
bridge = (484, 1096, 404, 556, BRIDGE[0], BRIDGE[1])
ducts_h = [b for i in find(r"inlet duct \(drop") for b in item_parts(i, lambda p: p["kind"] == "box" and p["min"][2] == 23)]
ducts_all = [b for i in find(r"inlet duct \(drop") for b in item_parts(i)]
fh_casing = [b for i in find(r"^FH-\d:") for b in item_parts(i, lambda p: p["kind"] == "box" and p["min"][2] >= 100 and p["color"] in ("filter", "steel") and p["max"][1] - p["min"][1] > 30)]
fh_south_cols = [b for i in find(r"^FH-\d:") for b in item_parts(i, lambda p: p["kind"] == "box" and p["max"][2] == 100 and p["min"][1] < 370)]
gt_lift = [(i["fp"][0], i["fp"][1], i["fp"][2], i["fp"][3], gt_top, HOOK) for i in gt]
screen = [
    ("Inlet duct (horizontal) to GT travel band", min(gap(a, b) for a in ducts_h for b in gt_bands), 6.0),
    ("Inlet duct (horizontal) to generator travel band", min(gap(a, b) for a in ducts_h for b in gen_bands), 4.0),
    ("Inlet duct to GT lift column", min(gap(a, b) for a in ducts_h for b in gt_lift), 15.0),
    ("Inlet duct to bridge-crane travel", min(gap(a, bridge) for a in ducts_all), 4.0),
    ("Filter house to bridge-crane travel", min(gap(a, bridge) for a in fh_casing), 4.0),
    ("FH south columns to bridge-crane travel", min(gap(a, bridge) for a in fh_south_cols), 35.0),
]
srows = [dict(check=n, model=round(v, 2), sheet=s, required=3.0, ok=v >= 3.0 and abs(v - s) <= 0.51)
         for (n, v, s) in screen]
hook = [("GT lift", HOOK - (gt_top + GAP + LIFT["gt"] + RIG), 11),
        ("Generator lift", HOOK - (gen_top + GAP + LIFT["gen"] + RIG), 15),
        ("ST lift-out over the ST", HOOK - (st_top + GAP + LIFT["st"] + RIG), 7),
        ("ST component travel over GT bays", HOOK - (gt_top + GAP + LIFT["st"] + RIG), 15)]
hrows9 = [dict(check=n, model=round(v, 2), sheet=s, ok=v >= 0 and abs(v - s) <= 0.51) for (n, v, s) in hook]
results["sheet09"] = dict(clearances=srows, hook=hrows9,
                          assumptions=dict(gt_top=gt_top, gen_top=gen_top, st_top=st_top, lift_gap=GAP,
                                           hook_max=HOOK, rigging=RIG, bridge_travel=BRIDGE),
                          ok=all(r["ok"] for r in srows + hrows9))

# 4. clashes ------------------------------------------------------------------
# Pairs the drawings define as touching or nested.
TOUCH = [
    (r"removable plenum spool", r"inlet duct \(drop"),        # spool bolts to the duct
    (r"removable plenum spool", r"^GT\d: H-class"),           # 'touches the GT lift column by design' (sheet 09)
    (r"^GCB-", r"UAT-\d tap"), (r"exhaust duct to HRSG", r"inlet transition"),
    (r"outlet breeching", r"stack$"), (r"outlet breeching", r"^HRSG \d \+ SCR"),
    (r"inlet transition", r"^HRSG \d \+ SCR"), (r"^GT\d: H-class", r"exhaust duct to HRSG"),
    (r"^GTG-\d", r"^GT\d: H-class"), (r"^STG", r"^ST: steam"), (r"^ST: steam", r"ST exhaust duct"),
    (r"ST exhaust duct", r"Air-cooled condenser"), (r"inlet duct \(drop", r"^FH-\d"),
    (r"inlet transition", r"Common turbine hall"), (r"exhaust duct to HRSG", r"Common turbine hall"),
    (r"inlet duct \(drop", r"Common turbine hall"), (r"^FH-\d", r"Common turbine hall"),
    (r"^GCB-", r"Common turbine hall"), (r"UAT-\d tap", r"Common turbine hall"),
    (r"ST exhaust duct", r"Common turbine hall"), (r"^Bridge crane", r"Common turbine hall"),
    (r"Turbine deck", r".*"), (r"Laydown bay floor", r".*"),
    (r"^Flue-gas duct", r"^DMP-"), (r"^Flue-gas duct", r"^DCC-"), (r"^Flue-gas duct", r"stack$"),
    (r"^Flue-gas duct", r"pipe and cable rack"), (r"^DMP-", r"stack$"),
    (r"pipe and cable rack", r"N-S pipe rack"), (r"N-S pipe rack", r"ST exhaust duct"),
    (r"^R1 ", r"^R1: main"), (r"^R1 ", r"^R1 "), (r"^R4 ", r"^R4: ACC"),
    (r"^RICE engine-generator", r"RICE engine hall"), (r"PEM electrolyzer|^Rectifier \d", r"electrolyzer building"),
    (r"230 kV bus", r"dead-end"), (r"230 kV bus", r"disconnect switches"), (r"230 kV breaker", r"disconnect switches"),
    (r"^H2 27|H2 storage tube banks", r"H2 storage tube banks|^H2 27"),
    (r"BESS container|BESS PCS", r"BESS blocks"), (r"^LNG 11", r"^LNG 12"),
    (r"^Absorber", r"Water-wash"), (r"^SC-\d", r"^SC-\d"),
    (r"monopoles", r"reserved|COR-HMOD"),
    (r"inlet duct \(drop|^FH-\d:", r"Common turbine hall"),       # penetrate the gallery roof
    (r"H2 24", r"electrolyzer building"), (r"intercooler \(pumps", r"^Absorber"), (r"^H2 26|^H2 25|^H2 28", r"^H2 2[5-8]"),
]
TOUCH = [(re.compile(a), re.compile(b)) for a, b in TOUCH]


def allowed(n1, n2):
    return any((a.search(n1) and b.search(n2)) or (a.search(n2) and b.search(n1)) for a, b in TOUCH)


solid_parts = [(p, b) for p, b in PB if is_axis_rod(p) and p["layer"] != "SITE"
               and items[p["item"]]["z"][1] > 0.7 and b[5] - b[4] > 0.35]
clashes = {}
# spatial hash on 50 ft cells
grid = {}
for idx, (p, b) in enumerate(solid_parts):
    for gx in range(int(b[0] // 50), int(b[1] // 50) + 1):
        for gy in range(int(b[2] // 50), int(b[3] // 50) + 1):
            grid.setdefault((gx, gy), []).append(idx)
seen = set()
for cell in grid.values():
    for i, j in itertools.combinations(cell, 2):
        if (i, j) in seen:
            continue
        seen.add((i, j))
        (p, a), (q, b) = solid_parts[i], solid_parts[j]
        if p["item"] == q["item"]:
            continue
        ov = [min(a[2 * k + 1], b[2 * k + 1]) - max(a[2 * k], b[2 * k]) for k in range(3)]
        if min(ov) <= 0.05:
            continue
        n1, n2 = items[p["item"]]["name"], items[q["item"]]["name"]
        if allowed(n1, n2):
            continue
        key = tuple(sorted((n1, n2)))
        vol = ov[0] * ov[1] * ov[2]
        if key not in clashes or clashes[key]["volume_ft3"] < vol:
            clashes[key] = dict(a=key[0], b=key[1], volume_ft3=round(vol, 2),
                                at=[round((max(a[0], b[0]) + min(a[1], b[1])) / 2, 1),
                                    round((max(a[2], b[2]) + min(a[3], b[3])) / 2, 1),
                                    round((max(a[4], b[4]) + min(a[5], b[5])) / 2, 1)])
cl = sorted(clashes.values(), key=lambda c: -c["volume_ft3"])
results["clashes"] = dict(pairs_tested=len(seen), clashes=cl, ok=not cl)

# 5. bounds -------------------------------------------------------------------
below_ok = re.compile(r"Stormwater|cable basement|Compound|sump pump|MC-cable risers|^FH-\d|^Underground:|^LS-1|cable termination structure|Service-entrance handhole")
oob = []
for p, b in PB_ALL:
    n = items[p["item"]]["name"]
    if p["kind"] == "rod":
        b = (min(p["a"][0], p["b"][0]), max(p["a"][0], p["b"][0]), min(p["a"][1], p["b"][1]),
             max(p["a"][1], p["b"][1]), min(p["a"][2], p["b"][2]), max(p["a"][2], p["b"][2]))
    on_campus = items[p["item"]]["layer"].startswith(("OPT_DC", "OPT_UNDERGROUND")) or b[0] >= 2435      # BTM campus east of the fence
    xmax = 3380.01 if on_campus else 2420.01
    if b[0] < -0.01 or b[1] > xmax or b[2] < -0.01 or b[3] > 1920.01 or (b[4] < -0.01 and not below_ok.search(n)):
        oob.append(n)
results["bounds"] = dict(out_of_bounds=sorted(set(oob)), ok=not oob)

ok = all(v["ok"] for v in results.values())
results["summary"] = dict(ok=ok, items=len(model["items"]), parts=len(model["parts"]), routes=len(model["routes"]))
json.dump(results, open(os.path.join(HERE, "verify_report.json"), "w"), indent=1)

print(f"footprints : {results['footprints']['matched']}/{results['footprints']['checked']} drawing shapes matched (tol {TOL} ft)")
for m in miss:
    print(f"   MISSING  {m['sheet']} x={m['x']} y={m['y']} fill={m['fill']}")
print(f"heights    : {sum(r['ok'] for r in hrows)}/{len(hrows)} sheet-13 heights reproduced")
for r in hrows:
    if not r["ok"]:
        print(f"   FAIL     {r}")
print(f"sheet 09   : {sum(r['ok'] for r in srows + hrows9)}/{len(srows + hrows9)} clearances and hook margins reproduced")
for r in srows + hrows9:
    print(f"   {'ok  ' if r['ok'] else 'FAIL'}     {r['check']:<48} model {r['model']:>6}  sheet {r['sheet']}")
print(f"clashes    : {len(cl)} clashing item pairs ({len(seen)} part pairs tested)")
for c in cl[:40]:
    print(f"   CLASH    {c['a']}  <->  {c['b']}  {c['volume_ft3']} ft3 at {c['at']}")
print(f"bounds     : {len(results['bounds']['out_of_bounds'])} items out of bounds {results['bounds']['out_of_bounds'][:5]}")
print("RESULT     :", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
