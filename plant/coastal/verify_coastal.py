#!/usr/bin/env python3
"""Checks for the coastal variant overlays (sheet SK-3X1-15).

- footprints: every numbered key item matches its sheet 15 shape within 0.6 ft
  (the FSRU group is shifted to the stated ~21,000 ft pipeline length);
- clashes: no two items overlap (axis-aligned parts; ground strips and connections allowed);
- siting: nothing new inside the plant compound except the buried pipeline right of way,
  land items on the land side of the shoreline, vessels and piles on the sea side;
- berth geometry: the carrier clears the berth and dolphins, and the STS pair has a fender gap.
The overlays are placed north of the plant (the sheet-15 layout rotated 90 deg); the sheet checks
run on the items mapped back to the sheet frame. Site checks then audit the placement against the
plant model: the terminal stays outside the compound, its links (road through the north gate,
send-out pipeline to the M&R, 230 kV cable) clear the plant equipment, the gate is open in the
fence, and the shoreline is north of everything on land.

    python3 plant/coastal/verify_coastal.py        # exits 1 on failure
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
REF = json.load(open(os.path.join(PLANT, "reference", "sk3x1_rev14_sheet15.json")))
TOL = 0.6
GROUND = ("plot", "roads", "link road", "right of way", "landfall (shore", "cable trench")
# item pairs that touch by design (a pipe entering the equipment it serves, lines to bollards)
CONNECT = [("unloading lines", "tank"), ("unloading lines", "jetty"), ("send-out pumps", "lng to the send-out"),
           ("lng to the send-out", "tank"), ("seawater supply", "vaporizers"), ("seawater supply", "intake"),
           ("send-out gas", "vaporizers"), ("send-out gas", "metering"), ("mooring lines", ""),
           ("sts fenders", ""), ("jetty trestle", "berth"), ("dolphins", "berth"), ("knock-out", "flare"),
           ("yoke", "fsru"), ("dolphins", "lng carrier"),
           ("relief header", "tank"), ("relief header", "knock-out"), ("outfall", "vaporizers")]


def bbox(p):
    if p["kind"] in ("box", "prism"):
        return p["min"], p["max"]
    if p["kind"] == "rod":
        r = max(p["r"], p["r2"])
        return ([min(a, b) - r for a, b in zip(p["a"], p["b"])], [max(a, b) + r for a, b in zip(p["a"], p["b"])])
    xs, ys, zs = zip(*p["v"])
    return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]


def axis_aligned(p):
    if p["kind"] != "rod":
        return p["kind"] in ("box", "prism")
    return sum(abs(a - b) > 1e-6 for a, b in zip(p["a"], p["b"])) <= 1


def to_sheet(ov):
    """Map the sheet-frame items (rotated onto the site) back to the sheet 15 frame; drop site links."""
    t = ov["coastal"]["transform"]
    C, D = t["c"], t["d"]
    keep = {it["id"] for it in ov["items"] if it.get("frame") != "site"}
    items = []
    for it in ov["items"]:
        if it["id"] not in keep:
            continue
        x0, x1, y0, y1 = it["fp"]
        items.append(dict(it, fp=[y0 + D, y1 + D, C - x1, C - x0]))
    parts = []
    for p in ov["parts"]:
        if p["item"] not in keep:
            continue
        q = dict(p)
        if p["kind"] in ("box", "prism"):
            (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
            q["min"], q["max"] = [y0 + D, C - x1, z0], [y1 + D, C - x0, z1]
        elif p["kind"] == "rod":
            q["a"] = [p["a"][1] + D, C - p["a"][0], p["a"][2]]
            q["b"] = [p["b"][1] + D, C - p["b"][0], p["b"][2]]
        else:
            q["v"] = [[y + D, C - x, z] for (x, y, z) in p["v"]]
        parts.append(q)
    meta = dict(ov["coastal"], shoreline_x=ov["coastal"]["shoreline_y"] + D)
    return dict(ov, items=items, parts=parts, coastal=meta)


def site_checks(ov, out):
    base = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))
    meta = ov["coastal"]
    shore = meta["shoreline_y"]
    links = [it for it in ov["items"] if it.get("frame") == "site"]
    sheet = [it for it in ov["items"] if it.get("frame") != "site"]
    inside = [it["name"] for it in sheet if it["fp"][0] < 2420 and it["fp"][1] > 0 and it["fp"][2] < 1920 and it["fp"][3] > 0]
    out(not inside, f"site: terminal / landfall placed north of the plant, nothing inside the compound {inside[:3]}")
    land = [it for it in sheet if it["layer"] not in ("MARINE", "LNG_JETTY")
            and "landfall" not in it["name"].lower() and "outfall" not in it["name"].lower()]
    north = [it["name"] for it in land if it["fp"][3] > shore + 1]
    out(not north, f"site: shoreline at y {shore:.0f}, north of every land item {north[:3]}")
    # links: only these enter the compound; at grade they must clear the plant equipment
    allowed = all(("right of way" in it["name"].lower() or "link road" in it["name"].lower()
                   or "termination structure" in it["name"].lower()) for it in links)
    out(allowed, f"site: {len(links)} links into the plant, all buried rights of way, their cable termination or the link road")
    bitems = {it["id"]: it for it in base["items"]}
    hits = set()
    for ln in links:
        if "link road" not in ln["name"].lower():
            continue
        x0, x1, y0, y1 = ln["fp"]
        for p in base["parts"]:
            it = bitems[p["item"]]
            if p["kind"] in ("box", "prism"):
                lo, hi = p["min"], p["max"]
            elif p["kind"] == "rod":
                r = max(p["r"], p["r2"])
                lo = [min(a, b) - r for a, b in zip(p["a"], p["b"])]
                hi = [max(a, b) + r for a, b in zip(p["a"], p["b"])]
            else:
                continue
            if hi[2] <= .6 or lo[2] >= 16:                      # grade features, overhead clear of a truck
                continue
            if lo[0] < x1 and hi[0] > x0 and lo[1] < y1 and hi[1] > y0:
                hits.add(it["name"][:50])
    out(not hits, f"site: link road clear of plant equipment, fence open at the north gate {sorted(hits)[:4]}")
    # buried links end at what they serve
    mr = next(it for it in base["items"] if it["name"].startswith("Pipeline M&R station"))["fp"]
    for ln in links:
        n = ln["name"].lower()
        if "pipeline to the plant m&r" in n:
            ok = ln["fp"][0] <= mr[1] and ln["fp"][1] >= mr[0] and ln["fp"][2] <= mr[3]
            out(ok, f"site: {ln['name'][:46]} reaches the M&R station")
        if "230 kv cable" in n and "right of way" in n:
            ok = ln["fp"][2] < 260 and ln["fp"][1] > 2420
            out(ok, "site: 230 kV cable leaves the switchyard and runs outside the east fence")
    # wiring: every powered keyed item carries its cable applications
    unwired = [it["name"][:40] for it in sheet if it.get("key") and it["layer"] != "MARINE" and not it.get("wiring")]
    out(not unwired, f"wiring: every keyed terminal item has cable applications {unwired[:3]}")


def check(variant):
    raw = json.load(open(os.path.join(HERE, f"sk3x1_coastal_{variant}.json")))
    fails, lines = 0, []

    def out(ok, msg):
        nonlocal fails
        fails += not ok
        lines.append(f"   {'ok  ' if ok else 'FAIL'}   {msg}")

    site_checks(raw, out)
    ov = to_sheet(raw)
    meta, items = ov["coastal"], {it["id"]: it for it in ov["items"]}
    P = REF["panels"][variant]

    # footprints
    dx = meta.get("fsru_offset_ft", 0)
    for it in ov["items"]:
        k = it.get("key")
        if not k:
            continue
        ref = list(P["keys"][k]["fp"])
        if variant == "B" and k in ("14", "15", "16"):
            ref[0] += dx
            ref[1] += dx
        got = it["fp"]
        if k == "15":                        # FSRU: bow stops short of the yoke tower
            d = max(abs(got[0] - ref[0]), abs(got[1] - ref[1]), abs(got[2] - ref[2]))
        else:
            d = max(abs(a - b) for a, b in zip(got, ref))
        out(d <= TOL, f"key {k:>2} {it['name'][:58]:<58} dev {d:5.2f} ft")

    # clashes (axis-aligned parts of different items)
    parts = [p for p in ov["parts"] if axis_aligned(p)]
    boxes = [(p["item"], *bbox(p)) for p in parts]
    ground = {i for i, it in items.items() if any(g in it["name"].lower() for g in GROUND)}
    cell, grid = 60.0, {}
    for n, (iid, lo, hi) in enumerate(boxes):
        if iid in ground:
            continue
        for gx in range(int(lo[0] // cell), int(hi[0] // cell) + 1):
            for gy in range(int(lo[1] // cell), int(hi[1] // cell) + 1):
                grid.setdefault((gx, gy), []).append(n)
    pairs, tested = set(), 0
    for ns in grid.values():
        for a, b in itertools.combinations(ns, 2):
            ia, ib = boxes[a][0], boxes[b][0]
            if ia == ib:
                continue
            tested += 1
            (la, ha), (lb, hb) = boxes[a][1:], boxes[b][1:]
            ov_ = [min(ha[i], hb[i]) - max(la[i], lb[i]) for i in range(3)]
            if min(ov_) > .05:
                na, nb = items[ia]["name"].lower(), items[ib]["name"].lower()
                if any((x in na and y in nb) or (x in nb and y in na) for x, y in CONNECT):
                    continue
                pairs.add(tuple(sorted((items[ia]["name"], items[ib]["name"]))))
    out(not pairs, f"clashes: {len(pairs)} item pairs ({tested} part pairs tested)")
    for a, b in sorted(pairs)[:12]:
        lines.append(f"            {a[:50]}  x  {b[:50]}")

    # siting
    shore = meta["shoreline_x"]
    inside = [it["name"] for it in ov["items"] if it["fp"][0] < 2420 and it["fp"][2] < 1920
              and "right of way" not in it["name"].lower()]
    out(not inside, f"nothing new inside the 2,420 x 1,920 ft compound {inside[:3]}")
    marine = {"MARINE", "LNG_JETTY"}
    wet = [it["name"] for it in ov["items"] if it["layer"] == "MARINE" and it["fp"][0] < shore]
    out(not wet, f"vessels and mooring on the sea side of the shoreline (x > {shore}) {wet[:3]}")
    dry = [it["name"] for it in ov["items"] if it["layer"] not in marine and it["fp"][1] > shore + 1
           and "landfall" not in it["name"].lower() and "outfall" not in it["name"].lower()]
    out(not dry, f"terminal / landfall items on the land side {dry[:3]}")
    piles = [p for p in ov["parts"] if p["color"] == "pile" and min(p["a"][0], p["b"][0]) < shore]
    out(not piles, f"jetty and berth piles all in the water ({len(piles)} on land)")

    # berth geometry
    if variant == "A":
        hull = next(it for it in ov["items"] if it["tag"] == "LNGC")["fp"]
        berth = next(it for it in ov["items"] if it.get("key") == "11")["fp"]
        gap = hull[0] - berth[1]
        out(gap >= 10, f"carrier side to berth face {gap:.1f} ft (fenders and arm reach, >= 10 ft)")
        length = hull[3] - hull[2]
        out(abs(length - 294 / .3048) < 5, f"carrier LOA {length:.0f} ft = {length * .3048:.0f} m (294 m on sheet 15)")
        jetty = next(it for it in ov["items"] if it.get("key") == "10")["fp"]
        out(abs((jetty[1] - jetty[0]) - 1700) < 60, f"jetty trestle {jetty[1] - jetty[0]:.0f} ft (~1,700 ft)")
    else:
        f = next(it for it in ov["items"] if it["tag"] == "FSRU")["fp"]
        c = next(it for it in ov["items"] if it["tag"] == "LNGC-STS")["fp"]
        out(40 <= c[0] - f[1] <= 70, f"STS fender gap FSRU to carrier {c[0] - f[1]:.0f} ft")
        lvs = next(it for it in ov["items"] if it.get("key") == "12")["fp"]
        yoke = next(it for it in ov["items"] if it.get("key") == "14")["fp"]
        run = (yoke[0] + yoke[1]) / 2 - lvs[1]
        out(20000 <= run <= 21400, f"landfall to yoke {run:,.0f} ft = {run * .3048 / 1000:.1f} km (6-6.5 km on sheet 15)")
    return fails, lines


def main():
    total = 0
    report = {}
    for v in ("A", "B"):
        fails, lines = check(v)
        total += fails
        report[v] = dict(fails=fails, lines=lines)
        print(f"coastal variant {v}")
        print("\n".join(lines))
    print("RESULT     :", "PASS" if total == 0 else f"FAIL ({total})")
    json.dump(report, open(os.path.join(HERE, "verify_coastal_report.json"), "w"), indent=1)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
