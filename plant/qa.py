"""Plant-wide quality / realism sweep on sk3x1_model.json (geometry-level, complements verify / audit):
- floating parts: parts above grade that touch nothing else (lights, boxes, pipes hanging in the air);
- open pipe ends: pipe-like rods whose end meets no other part and is not at grade;
- obstructions in roads: anything at grade inside a road footprint (bar people, vehicles, road dressing);
- headroom: overhead parts over a road below 18 ft.
Prints counts per item and writes qa_report.json."""
import json, math, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
items = {it["id"]: it for it in M["items"]}
PIPE = {"pipe", "waterline", "fuelgas", "fueloil", "steam", "lngpipe", "cw", "chw", "hydrogen", "amber", "pvc_blue",
        "pvc_green", "hdpe", "ductile", "rcp"}
SKIP_ITEM = re.compile(r"^People|^Vehicles|^Compound|Perimeter fence|^Underground|^Duct-bank manholes|cable-pull")
UG = ("UNDERGROUND", "OPT_UNDERGROUND")


def pbox(p, pad=0.0):
    if p["kind"] in ("box", "prism"):
        b = p["min"] + p["max"]
    elif p["kind"] == "rod":
        a, c, r = p["a"], p["b"], max(p["r"], p["r2"])
        ax = [i for i in range(3) if a[i] != c[i]]
        pr = [0 if i in ax else r for i in range(3)] if len(ax) == 1 else [r] * 3
        b = [min(a[i], c[i]) - pr[i] for i in range(3)] + [max(a[i], c[i]) + pr[i] for i in range(3)]
    else:
        xs, ys, zs = zip(*p["v"])
        b = [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]
    return [b[0] - pad, b[1] - pad, b[2] - pad, b[3] + pad, b[4] + pad, b[5] + pad]


P = M["parts"]
B = [pbox(p) for p in P]
grid = defaultdict(list)
G = 10
for k, b in enumerate(B):
    if (b[3] - b[0] > 400 or b[4] - b[1] > 400) and b[5] <= .8:
        continue                                  # site-wide ground / slabs: handled as grade
    for gx in range(int(b[0] // G), int(b[3] // G) + 1):
        for gy in range(int(b[1] // G), int(b[4] // G) + 1):
            grid[(gx, gy)].append(k)


def touching(k, pad=.35, pt=None):
    b = pbox(P[k], pad) if pt is None else [pt[0] - pad, pt[1] - pad, pt[2] - pad, pt[0] + pad, pt[1] + pad, pt[2] + pad]
    seen = set()
    for gx in range(int(b[0] // G), int(b[3] // G) + 1):
        for gy in range(int(b[1] // G), int(b[4] // G) + 1):
            for j in grid.get((gx, gy), ()):
                if j == k or j in seen:
                    continue
                seen.add(j)
                c = B[j]
                if b[0] <= c[3] and b[3] >= c[0] and b[1] <= c[4] and b[4] >= c[1] and b[2] <= c[5] and b[5] >= c[2]:
                    return True
    return False


out = defaultdict(lambda: defaultdict(list))
for k, p in enumerate(P):
    it = items[p["item"]]
    if p["layer"] in UG or SKIP_ITEM.search(it["name"]):
        continue
    b = B[k]
    if b[2] > .6 and not touching(k):
        out["floating part"][it["name"][:60]].append([round(v, 1) for v in ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, b[2])])
    if p["kind"] == "rod" and p["color"] in PIPE and p["r"] >= .2:
        for e in (p["a"], p["b"]):
            if e[2] > .8 and not touching(k, pad=max(p["r"], .3) + .25, pt=e):
                out["open pipe end"][it["name"][:60]].append([round(v, 1) for v in e])
roads = [it for it in M["items"] if it["layer"] == "SITE" and "road" in it["name"].lower()]
rid = {it["id"] for it in roads}
for k, p in enumerate(P):
    it = items[p["item"]]
    if p["item"] in rid or p["layer"] in UG or SKIP_ITEM.search(it["name"]) or it["layer"] == "SITE":
        continue
    b = B[k]
    for r in roads:
        f = r["fp"]
        if b[0] < f[1] - .5 and b[3] > f[0] + .5 and b[1] < f[3] - .5 and b[4] > f[2] + .5:
            if b[2] < 3:
                out["at grade in a road"][it["name"][:60]].append([round((b[0] + b[3]) / 2, 1), round((b[1] + b[4]) / 2, 1)])
            elif b[2] < 18:
                out["under 18 ft over a road"][it["name"][:60]].append([round((b[0] + b[3]) / 2, 1), round((b[1] + b[4]) / 2, 1), round(b[2], 1)])
rep = {c: {n: v for n, v in d.items()} for c, d in out.items()}
json.dump(rep, open(os.path.join(HERE, "qa_report.json"), "w"), indent=1)
for c, d in rep.items():
    print(f"{c}: {sum(len(v) for v in d.values())} in {len(d)} items")
    for n, v in sorted(d.items(), key=lambda kv: -len(kv[1]))[:int(sys.argv[1]) if len(sys.argv) > 1 else 12]:
        print(f"   {len(v):4d}  {n}   e.g. {v[0]}")
