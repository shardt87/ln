"""Overlap check for detail parts (verify.py tests only the main parts): every part of the named items against every
part of other items, by bounding box with a small tolerance. Rods are tested on their swept box, so a diagonal rod
can report a near miss; the report lists each pair for a look.

    python tools/detail_clash.py "Item name prefix" [...]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = .05
IGNORE = ("Compound", "Underground", "Ground over", "Site drainage", "Pipe supports", "Duct-bank", "Site lighting: pole")


def bb(p):
    if p["kind"] in ("box", "prism"):
        return p["min"], p["max"]
    if p["kind"] == "rod":
        r = max(p.get("r", 0), p.get("r2", 0))
        return ([min(p["a"][i], p["b"][i]) - r for i in range(3)], [max(p["a"][i], p["b"][i]) + r for i in range(3)])
    if "v" in p:
        return [min(v[i] for v in p["v"]) for i in range(3)], [max(v[i] for v in p["v"]) for i in range(3)]
    return None


def main(prefixes, allow=()):
    M = json.load(open(os.path.join(ROOT, "sw3x1_model.json")))
    items = {i["id"]: i["name"] for i in M["items"]}
    mine = {i for i, n in items.items() if n.startswith(tuple(prefixes))}
    A = [(p, bb(p)) for p in M["parts"] if p["item"] in mine]
    B = [(p, bb(p)) for p in M["parts"] if p["item"] not in mine and not items[p["item"]].startswith(IGNORE)]
    B = [(p, b) for p, b in B if b]
    hits = {}
    for p, a in A:
        if not a:
            continue
        for q, b in B:
            if all(a[0][k] < b[1][k] - TOL and a[1][k] > b[0][k] + TOL for k in range(3)):
                key = (items[p["item"]][:50], items[q["item"]][:50])
                if any(s in key[1] for s in allow):
                    continue
                hits.setdefault(key, []).append((p["color"], q["color"], [round(v, 1) for v in a[0]]))
    for k, v in sorted(hits.items()):
        print(len(v), k, v[:3])
    print("pairs with overlaps:", len(hits))


if __name__ == "__main__":
    main(sys.argv[1:])
