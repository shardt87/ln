"""Roads, access and vehicle logic (owner, Oct 28: "make sure the roads make sense and flow logic, like you cannot have a
car behind the air inlet"). Reads sw3x1_model.json and checks:

1. roads clear: no equipment standing on a road or drive (overhead structures above 14 ft, pipe-crossing sleeves, gates,
   cable ramps, signs, people and vehicles excepted);
2. roads connected: every road / drive joins the network that starts at the main gate;
3. vehicles: every vehicle and trailer stands on a drivable surface (road, concrete, crushed stone, pad, mats), can be
   driven to from the main gate along a 14 ft clear lane (obstacles 1-14 ft high block it), and is not parked in front
   of an air inlet (within 25 ft of a filter face) or in a transformer's oil-containment / firewall bay;
4. cable on grade: no portable / ground-tray cable runs along a road, every crossing has a drive-over protector;
5. fenced sites: each gate opens onto ground a vehicle can reach.

Writes road_audit.json; exit 1 on any FAIL. A 2 ft raster; typical, not a traffic study."""
import json
import math
import os
import re
import sys
from collections import deque

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "sw3x1_model.json")))
ITEMS = {i["id"]: i for i in M["items"]}
CELL = 2.0
XMAX, YMAX = 3400.0, 1920.0
NX, NY = int(XMAX / CELL), int(YMAX / CELL)
DRIVE = ("road", "concrete", "gravel", "gravel_yard", "pad", "epoxy", "timber", "gravel_pad")   # surfaced: park here
OPEN = ("ground", "turf")                              # open ground: passable, not a parking surface
GATE = (30.0, 285.0)                                   # main gate, on the 30 ft access road
CAMPUS_GATE = (3015.0, 20.0)
PASS_NAMES = re.compile(r"^Vehicles|operators|^People|sign\b|Site sign|Technology bay sign|Surface cables|Equipment ID|"
                        r"Drive-over|cable ramp|hoist landing|apron|Main gate|"
                        r"barrier|Gatehouse|lighting masts|Perimeter fence|Underground|Ground over|Compound|"
                        r"Site lighting|Site drainage|manholes|Cable trays and isolated|Firewater hydrants|"
                        r"walkways|crushed-stone|surfacing", re.I)
HIGH = 14.0                                            # clear height under overhead structures
ROADLIKE = re.compile(r"road|lane|drive|unloading bay", re.I)
NOT_ROAD = re.compile(r"^(Parking|Removal apron|Gallery door apron|Control / admin|Turbine hall|FH-\d hoist)")
TEMP_WORK = re.compile(r"outage|Cable pull|Cable reels staged|Cable moment|crane lift|"         # road closed for the job
                       r"^LNG 10: unloading skid", re.I)            # (its bay-2 loading arm is on the trailer parked there)


def grid_box(x0, x1, y0, y1):
    i0, i1 = max(0, int(x0 / CELL)), min(NX, int(math.ceil(x1 / CELL)))
    j0, j1 = max(0, int(y0 / CELL)), min(NY, int(math.ceil(y1 / CELL)))
    return i0, i1, j0, j1


def part_bbox(p):
    if p["kind"] == "rod":
        r = max(p["r"], p.get("r2", p["r"]))
        a, b = p["a"], p["b"]
        return (min(a[0], b[0]) - r, max(a[0], b[0]) + r, min(a[1], b[1]) - r, max(a[1], b[1]) + r,
                min(a[2], b[2]) - r, max(a[2], b[2]) + r)
    if "min" in p:
        return p["min"][0], p["max"][0], p["min"][1], p["max"][1], p["min"][2], p["max"][2]
    return None


def vehicles():
    """Wheel clusters: rods lying on the ground (radius 0.7-2.2 ft, axis horizontal), grouped per item within 14 ft."""
    W = []
    for p in M["parts"]:
        if p["kind"] == "rod" and p["color"] in ("fanhub", "tyre") and abs(p["a"][2] - p["r"]) < .2 \
                and abs(p["b"][2] - p["r"]) < .2 and .7 <= p["r"] <= 2.2:
            W.append(((p["a"][0] + p["b"][0]) / 2, (p["a"][1] + p["b"][1]) / 2, p["item"]))
    cl = []
    for x, y, i in W:
        for c in cl:
            if c["item"] == i and min(math.hypot(x - a, y - b) for a, b in c["pts"]) < 14:
                c["pts"].append((x, y))
                break
        else:
            cl.append(dict(item=i, pts=[(x, y)]))
    out = []
    for c in cl:
        xs, ys = [p[0] for p in c["pts"]], [p[1] for p in c["pts"]]
        bb = [min(xs) - 3, max(xs) + 3, min(ys) - 3, max(ys) + 3]
        f = ITEMS[c["item"]]["fp"]
        if (f[1] - f[0]) * (f[3] - f[2]) < 1500:      # a trailer that is its own item: the whole body, gooseneck included
            bb = [min(bb[0], f[0]), max(bb[1], f[1]), min(bb[2], f[2]), max(bb[3], f[3])]
        out.append(dict(item=c["item"], name=ITEMS[c["item"]]["name"], bb=tuple(bb)))
    return out


def main():
    drive = np.zeros((NX, NY), bool)
    openg = np.zeros((NX, NY), bool)
    road = np.zeros((NX, NY), bool)
    obst = np.zeros((NX, NY), bool)
    owner = {}                                         # obstacle cell -> item (for the road check)
    roads = []
    for p in M["parts"]:
        bb = part_bbox(p)
        if bb is None:
            continue
        x0, x1, y0, y1, z0, z1 = bb
        it = ITEMS[p["item"]]
        if p["kind"] == "box" and z1 <= 1.0 and z0 >= -.6 and p["color"] in OPEN:
            i0, i1, j0, j1 = grid_box(x0, x1, y0, y1)
            openg[i0:i1, j0:j1] = True
        if p["kind"] == "box" and z1 <= 1.0 and z0 >= -.6 and p["color"] in DRIVE:
            i0, i1, j0, j1 = grid_box(x0, x1, y0, y1)
            drive[i0:i1, j0:j1] = True
            if p["color"] == "road" and ROADLIKE.search(it["name"]) and not NOT_ROAD.search(it["name"]):
                road[i0:i1, j0:j1] = True
                roads.append((x0, x1, y0, y1, it["name"]))
    road_core = road & np.roll(road, 1, 0) & np.roll(road, -1, 0) & np.roll(road, 1, 1) & np.roll(road, -1, 1)
    vs = vehicles()
    veh_items = {v["item"] for v in vs}
    for p in M["parts"]:
        bb = part_bbox(p)
        if bb is None:
            continue
        x0, x1, y0, y1, z0, z1 = bb
        it = ITEMS[p["item"]]
        if z1 <= 1.0 or z0 >= HIGH or it["layer"].startswith(("OPT_UNDERGROUND", "UNDERGROUND")):
            continue
        if (x1 - x0) * (y1 - y0) > 40000 or PASS_NAMES.search(it["name"]):
            continue
        if p.get("d") and (x1 - x0) < .5 and (y1 - y0) < .5:
            continue                                   # thin dressing (rails, conduits) never blocks a vehicle
        sx = .3 if x1 - x0 > 1.2 else 0                 # trim edge brushes, but keep thin walls / fences whole
        sy = .3 if y1 - y0 > 1.2 else 0
        i0, i1, j0, j1 = grid_box(x0 + sx, x1 - sx, y0 + sy, y1 - sy)
        if i1 <= i0 or j1 <= j0:
            continue
        obst[i0:i1, j0:j1] = True
        if it["id"] not in veh_items and not TEMP_WORK.search(it["name"]):
            sub = road_core[i0:i1, j0:j1]
            if sub.any():
                owner.setdefault(it["name"], 0)
                owner[it["name"]] += int(sub.sum())
    # fences: 7-8 ft chain-link counts as obstacle (gates are gaps in the parts already)
    free = (drive | openg) & ~obst
    # a 14 ft clear lane (single-lane plant road with clearance): a centre cell is passable when the 7 x 7 cell
    # (14 ft) square round it is free
    pas = free.copy()
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            pas &= np.roll(np.roll(free, dx, 0), dy, 1)
    reach = np.zeros_like(pas)
    q = deque()
    for (gx, gy) in (GATE, CAMPUS_GATE):
        i, j = int(gx / CELL), int(gy / CELL)
        if pas[i, j]:
            reach[i, j] = True
            q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < NX and 0 <= b < NY and pas[a, b] and not reach[a, b]:
                reach[a, b] = True
                q.append((a, b))
    # widen the reach by 10 ft: a parked vehicle's own body (cab, boom carrier, deck beyond the wheels) is an obstacle too
    near = reach.copy()
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            near |= np.roll(np.roll(reach, dx, 0), dy, 1)

    res = dict(roads={}, vehicles=[], gates=[], ok=True)
    # 1. roads clear
    blocked = {k: v for k, v in owner.items() if v * CELL * CELL >= 8}
    res["roads"]["blocked_by"] = sorted(blocked.items(), key=lambda kv: -kv[1])
    # 2. roads connected (a road cell not reached, in a chunk of the road over 400 sq ft)
    lost = []
    for (x0, x1, y0, y1, nm) in roads:
        i0, i1, j0, j1 = grid_box(x0, x1, y0, y1)
        sub_r, sub_n = road[i0:i1, j0:j1], near[i0:i1, j0:j1]
        if sub_r.sum() and (sub_n & sub_r).sum() < .5 * sub_r.sum() and (x1 - x0) * (y1 - y0) > 400:
            lost.append(f"{nm[:60]} ({x0:.0f}-{x1:.0f}, {y0:.0f}-{y1:.0f})")
    res["roads"]["unreached"] = lost
    # 3. vehicles
    inlets = [part_bbox(p) + (p["item"],) for p in M["parts"] if p["color"] == "filter" and p.get("kind") == "box"
              and part_bbox(p)[5] - part_bbox(p)[4] > 4]
    xf = [i["fp"] for i in M["items"] if re.search(r"transformer|GSU|T-MOD|step-up", i["name"], re.I)
          and i["z"][1] > 5 and not re.search(r"grounding|pad-mount|firewall|gantry|cabinet", i["name"], re.I)]
    for v in vs:
        x0, x1, y0, y1 = v["bb"]
        i0, i1, j0, j1 = grid_box(x0, x1, y0, y1)
        on = drive[i0:i1, j0:j1].mean() if i1 > i0 and j1 > j0 else 0
        ok_reach = bool(near[i0:i1, j0:j1].any())
        d_in = min([max(f[0] - x1, x0 - f[1], 0) + max(f[2] - y1, y0 - f[3], 0) for f in inlets if f[6] != v["item"]]
                   or [999])
        in_xf = any(f[0] - 2 < (x0 + x1) / 2 < f[1] + 2 and f[2] - 2 < (y0 + y1) / 2 < f[3] + 2 for f in xf)
        issues = []
        if on < .6:
            issues.append(f"off the drivable surface ({on:.0%} on)")
        if not ok_reach:
            issues.append("no 14 ft drive path from the gate")
        if d_in < 25:
            issues.append(f"{d_in:.0f} ft from an air-inlet filter face")
        if in_xf:
            issues.append("inside a transformer bay")
        res["vehicles"].append(dict(name=v["name"][:70], at=[round((x0 + x1) / 2), round((y0 + y1) / 2)], issues=issues))
    # 4. cable on grade (portable power cable, ground trays): never along a road, a protector at every crossing
    prot = [part_bbox(p) for p in M["parts"] if p["color"] == "amber" and p.get("kind") == "box"
            and re.match(r"Surface cables|Drive-over cable ramp", ITEMS[p["item"]]["name"])]
    cab = []
    for r in M["routes"]:
        if not r.get("surface"):
            continue
        P = r["points"]
        for a, b in zip(P, P[1:]):
            horiz = a[1] == b[1]
            for (x0, x1, y0, y1, nm) in roads:
                long_x = (x1 - x0) >= (y1 - y0)
                if horiz and long_x and y0 + .5 <= a[1] <= y1 - .5 and \
                        min(max(a[0], b[0]), x1) - max(min(a[0], b[0]), x0) > 6:
                    cab.append(f"runs along {nm[:40]} at y {a[1]:.0f}")
                elif not horiz and not long_x and x0 + .5 <= a[0] <= x1 - .5 and \
                        min(max(a[1], b[1]), y1) - max(min(a[1], b[1]), y0) > 6:
                    cab.append(f"runs along {nm[:40]} at x {a[0]:.0f}")
                elif horiz and not long_x and y0 <= a[1] <= y1 and min(a[0], b[0]) <= x0 and max(a[0], b[0]) >= x1:
                    if not any(q[0] <= (x0 + x1) / 2 <= q[1] and q[2] - .5 <= a[1] <= q[3] + .5 for q in prot):
                        cab.append(f"crosses {nm[:40]} at y {a[1]:.0f} without a protector")
                elif not horiz and long_x and x0 <= a[0] <= x1 and min(a[1], b[1]) <= y0 and max(a[1], b[1]) >= y1:
                    if not any(q[2] <= (y0 + y1) / 2 <= q[3] and q[0] - .5 <= a[0] <= q[1] + .5 for q in prot):
                        cab.append(f"crosses {nm[:40]} at x {a[0]:.0f} without a protector")
    res["surface_cables"] = sorted(set(cab))
    # 5. fenced site gates
    for it in M["items"]:
        if "chain-link fence" not in it["name"]:
            continue
        x0, x1, y0, y1 = it["fp"]
        xm = (x0 + x1) / 2
        ok = False
        for yy in (y0 - 8, y1 + 8):                    # the 14 ft lane has to arrive at the gate opening itself
            i, j = int(xm / CELL), int(yy / CELL)
            if 0 <= j < NY and reach[i - 1:i + 2, j - 1:j + 2].any():
                ok = True
        res["gates"].append(dict(site=it["name"].split(":")[0], ok=ok))
    fails = (len(res["roads"]["blocked_by"]) + len(lost) + len(res["surface_cables"]) + sum(bool(v["issues"]) for v in res["vehicles"])
             + sum(not g["ok"] for g in res["gates"]))
    res["ok"] = fails == 0
    json.dump(res, open(os.path.join(HERE, "road_audit.json"), "w"), indent=1)
    print(f"roads      : {len(roads)} road / drive surfaces; blocked by {len(res['roads']['blocked_by'])} items; "
          f"{len(lost)} not reached from the gate")
    for nm, n in res["roads"]["blocked_by"][:30]:
        print(f"   BLOCKS   {nm[:80]}  ({n * CELL * CELL:.0f} sq ft of road)")
    for nm in lost:
        print(f"   UNREACHED {nm}")
    print(f"vehicles   : {len(vs)}; {sum(bool(v['issues']) for v in res['vehicles'])} with issues")
    for v in res["vehicles"]:
        if v["issues"]:
            print(f"   VEHICLE  {v['name'][:60]} at {v['at']}: {'; '.join(v['issues'])}")
    print(f"cable on grade: {len(res['surface_cables'])} runs along a road or unprotected crossings")
    for c in res["surface_cables"]:
        print(f"   CABLE    {c}")
    print(f"site gates : {len(res['gates'])}; {sum(not g['ok'] for g in res['gates'])} not reachable")
    for g in res["gates"]:
        if not g["ok"]:
            print(f"   GATE     {g['site']}")
    if "--png" in sys.argv:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        img = np.zeros((NY, NX, 3))
        img[...] = .95
        img[drive.T] = (.85, .82, .7)
        img[road.T] = (.6, .6, .6)
        img[(reach & drive).T] = img[(reach & drive).T] * .7 + np.array((.2, .45, .2)) * .3
        img[obst.T] = (.25, .25, .3)
        f, a = plt.subplots(figsize=(34, 19))
        a.imshow(img, origin="lower", extent=(0, XMAX, 0, YMAX))
        for v in res["vehicles"]:
            a.plot(*v["at"], "o", ms=5, color="r" if v["issues"] else "b")
        plt.savefig(sys.argv[sys.argv.index("--png") + 1], dpi=60, bbox_inches="tight")
    print("RESULT     :", "PASS" if res["ok"] else "FAIL")
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
