#!/usr/bin/env python3
"""Site audit: connections and leftovers (complements verify.py).

- every route end lands on equipment (an item footprint, grown by a tolerance) or on another route;
- every generating / conversion / switching unit has at least one route end at it,
  or belongs to a group that has one (e.g. engines inside their hall);
- no item floats: its lowest primary part touches grade or a supporting item below;
- no leftovers from removed design options (SC-3/SC-4, RICE hall 2, RICE-9+);
- cable trays and the IPB do not pass through structures or equipment;
- every item with wiring applications has a cable route ending at it or passing it;
- tags are unique; every part and route layer is a declared layer.

    python3 plant/audit.py        # writes audit_report.json, exits 1 on findings
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
items = {it["id"]: it for it in M["items"]}
TOL = 15.0             # ft: a route end may stop this far short of the equipment it serves
UNIT = re.compile(r"^(GT\d|ST$|GSU|UAT|SC-\d|RICE-\d+|TM-\d|CONT-\d+|FC-\d+|MT-\d+|T-|GEN-|MOD-EH|PAD-|BESS|LCI|"
                  r"SWGR|MCC|PIC|GSP|H2-|R\d)")
REMOVED = re.compile(r"\b(SC-3|SC-4|T-SC3|T-SC4|RICE-(9|1[0-9]|2[0-9])|RICE-2H|RICE hall 2|engine hall 2)\b")


def near(it, x, y, tol=TOL):
    f = it["fp"]
    return f[0] - tol <= x <= f[1] + tol and f[2] - tol <= y <= f[3] + tol


def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return ((px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2) ** .5


def main():
    findings = defaultdict(list)
    equip = [it for it in M["items"] if it["layer"] != "SITE" and it["z"][1] > 1.5
             and not it["name"].startswith(("Pipe supports", "Pipe runs", "Cable trays", "Firewater hydrants", "Small-bore piping", "HRSG 3 tube harps", "Equipment ID", "People", "Vehicles"))]
    routes = M["routes"]
    # 1. route ends
    ends_at = defaultdict(list)
    for ri, r in enumerate(routes):
        for end in (r["points"][0], r["points"][-1]):
            hits = [it for it in equip if near(it, *end)]
            for it in hits:
                ends_at[it["id"]].append(ri)
            if hits:
                continue
            # valid ends that are flat by nature: switchyard buses and future bays, the gas yard pad,
            # and the fence line where the pipeline lateral enters
            pads = [it for it in M["items"] if it["layer"] in ("BASE_SWITCHYARD", "SWYD_FUTURE")
                    or it["name"].startswith("Plant gas yard")]
            if any(near(it, *end, tol=15) for it in pads) or end[1] >= 1915 or end[1] <= 5 or end[0] <= 5 or end[0] >= 2415:
                continue
            other = any(seg_dist(end, a, b) < 3 for rj, r2 in enumerate(routes) if rj != ri
                        for a, b in zip(r2["points"], r2["points"][1:]))
            if not other:
                findings["dangling route end"].append(f"{r['layer']} {r['type']} '{r.get('label', '')[:50]}' "
                                                      f"end at ({end[0]:.0f}, {end[1]:.0f})")
    # 2. units without a connection (a unit inside a connected envelope counts as connected)
    for it in equip:
        if not it["register"] or not UNIT.match(it["tag"] or ""):
            continue
        if ends_at.get(it["id"]):
            continue
        # a unit is also connected through its own auxiliaries (e.g. "SC-1 PCM + 15 kV GCB")
        if any(ends_at.get(o["id"]) for o in equip if o["id"] != it["id"] and o["name"].startswith(it["tag"] + " ")):
            continue
        host = [o for o in equip if o["id"] != it["id"] and ends_at.get(o["id"]) and
                o["fp"][0] <= it["fp"][0] + 1 and o["fp"][1] >= it["fp"][1] - 1 and
                o["fp"][2] <= it["fp"][2] + 1 and o["fp"][3] >= it["fp"][3] - 1]
        if not host:
            findings["unit with no route"].append(f"{it['layer']} {it['tag']}: {it['name'][:60]}")
    # 3. floating items
    lowest = defaultdict(lambda: 1e9)
    for p in M["parts"]:
        z = p["min"][2] if p["kind"] in ("box", "prism") else (min(p["a"][2], p["b"][2]) - (p["r"] if p["a"][2] == p["b"][2] else 0)
                                                               if p["kind"] == "rod" else min(v[2] for v in p["v"]))
        lowest[p["item"]] = min(lowest[p["item"]], z)
    for iid, z in lowest.items():
        it = items[iid]
        if z <= .6 or it["layer"].startswith(("R1_", "R4_", "HALL_ROOF")) or it["z"][0] > .6:
            continue
        under = [o for o in M["items"] if o["id"] != iid and o["z"][1] >= z - 1 and o["z"][0] < z and
                 o["fp"][0] < it["fp"][1] and o["fp"][1] > it["fp"][0] and o["fp"][2] < it["fp"][3] and o["fp"][3] > it["fp"][2]]
        if not under:
            findings["floating item"].append(f"{it['layer']} {it['name'][:60]} lowest part at EL {z:.1f}")
    # 4. leftovers from removed options
    for it in M["items"]:
        if REMOVED.search(it["name"]) or REMOVED.search(it.get("tag", "")) or REMOVED.search(it.get("info", "")):
            findings["leftover from a removed option"].append(f"{it['layer']} {it['name'][:70]}")
    for r in routes:
        if REMOVED.search(r.get("label", "")):
            findings["leftover from a removed option"].append(f"route {r['layer']} {r['label'][:70]}")
    # 5. cable trays and IPB must not pass through structures or equipment (generated geometry);
    #    allowed: the IPB entering its GCB and generator terminals, trays through the R1 wall sleeves
    tray = next((i["id"] for i in M["items"] if i["name"].startswith("Cable trays")), None)
    allowed = re.compile(r"^GCB-|^GTG-\d|R1 east-wall tray exits|^Common turbine hall|^Turbine deck|^Laydown|"
                         r"^230 kV switchyard|^Pipe supports")

    def pbox(p):
        if p["kind"] in ("box", "prism"):
            return p["min"] + p["max"]
        if p["kind"] == "rod":
            a, b, r = p["a"], p["b"], max(p["r"], p["r2"])
            ax = [i for i in range(3) if a[i] != b[i]]
            pad = [0 if i in ax else r for i in range(3)] if len(ax) == 1 else [r] * 3
            return [min(a[i], b[i]) - pad[i] for i in range(3)] + [max(a[i], b[i]) + pad[i] for i in range(3)]
        xs, ys, zs = zip(*p["v"])
        return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]
    if tray:
        T = [pbox(p) for p in M["parts"] if p["item"] == tray]
        O = [(p["item"], pbox(p)) for p in M["parts"] if p["item"] != tray and items[p["item"]]["layer"] != "SITE"
             and not allowed.search(items[p["item"]]["name"])]
        grid = defaultdict(list)
        for k, (_, b) in enumerate(O):
            for gx in range(int(b[0] // 20), int(b[3] // 20) + 1):
                for gy in range(int(b[1] // 20), int(b[4] // 20) + 1):
                    grid[(gx, gy)].append(k)
        clash = set()
        for b in T:
            for gx in range(int(b[0] // 20), int(b[3] // 20) + 1):
                for gy in range(int(b[1] // 20), int(b[4] // 20) + 1):
                    for k in grid.get((gx, gy), ()):
                        c = O[k][1]
                        if min(min(b[i + 3], c[i + 3]) - max(b[i], c[i]) for i in range(3)) > .1:
                            clash.add(items[O[k][0]]["name"][:60])
        for n in sorted(clash):
            findings["cable tray / IPB through equipment"].append(n)
    # 6. wiring applications: every item that needs wiring has a cable route ending at it or passing it
    elec = ("mv_tray", "lv_tray", "control_tray", "duct_bank", "mvlv_cable", "hv_cable", "hv_overhead", "ipb", "hmod",
            "cable_trench")
    segs = [(a, b) for r in routes if r["type"] in elec for a, b in zip(r["points"], r["points"][1:])]
    for it in M["items"]:
        if not it.get("wiring") or it["layer"] == "R1_INTERIOR" or it["tag"] == "CRANE":
            continue
        f = it["fp"]
        hit = any(min(a[0], b[0]) - TOL <= f[1] and max(a[0], b[0]) + TOL >= f[0] and
                  min(a[1], b[1]) - TOL <= f[3] and max(a[1], b[1]) + TOL >= f[2] for a, b in segs)
        if not hit:
            findings["item needing wiring with no cable"].append(f"{it['layer']} {it['name'][:60]}")
    # 7. tags and layers
    tags = Counter(it["tag"] for it in M["items"] if it["tag"])
    for t, n in tags.items():
        if n > 1:
            findings["duplicate tag"].append(f"{t} x{n}")
    layers = set(M["layers"])
    for p in M["parts"]:
        if p["layer"] not in layers:
            findings["undeclared layer"].append(p["layer"])
            break
    for r in routes:
        if r["layer"] not in layers:
            findings["undeclared layer"].append(r["layer"])
    report = {k: v for k, v in findings.items()}
    json.dump(dict(summary={k: len(v) for k, v in report.items()}, findings=report),
              open(os.path.join(HERE, "audit_report.json"), "w"), indent=1)
    for k, v in report.items():
        print(f"{k}: {len(v)}")
        for line in v[:60]:
            print("   ", line)
    print("RESULT:", "CLEAN" if not report else "FINDINGS")
    sys.exit(1 if report else 0)


if __name__ == "__main__":
    main()
