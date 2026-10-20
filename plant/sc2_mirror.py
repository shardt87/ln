"""SC-2 turned end for end so the two simple-cycle units face each other (owner, Oct 20): before, SC-2's inlet filter
sat ~30 ft downwind of SC-1's stack and SCR (hot-exhaust re-ingestion); now the two stacks stand as a pair in the
middle and both inlets are at the outer ends.

Mirrored about the centre of SC-2's drawn plot (x 2110 inlet end .. 2258.5 stack):
- build(): right after the modular / yard passes, before wiring, routes and manholes, every part and decal of the
  SC-2 items (unit, SCR, stack, PCM, lube cooler, inlet chiller) and their footprints, so everything routed
  afterwards (feeders, duct banks, manholes, pipe runs) follows the mirrored unit;
- since() / mirror_since(): later passes that place SC-2 detail from fixed drawn coordinates (modular_lod3,
  campus_brand) mirror what they just added. Passes that work from the unit's own geometry (detail3) need nothing.
The routes laid in build_model.py for SC-2 (gas drop, PCM duct bank) are written at their mirrored positions."""
import fuel

XC = (2110.0 + 2258.5) / 2                                  # drawn plot centre, x 2110 (inlet end) .. 2258.5 (stack)
PREFIX = ("SC-2", "CONDITIONAL: SC-2")


def mx(x):
    return round(2 * XC - x, 3)


def mirror_part(p):
    if "min" in p:
        a, b = p["min"][0], p["max"][0]
        p["min"][0], p["max"][0] = mx(b), mx(a)
    if "a" in p:
        p["a"][0], p["b"][0] = mx(p["a"][0]), mx(p["b"][0])
    if "v" in p:
        for v in p["v"]:
            v[0] = mx(v[0])


def build():
    G = fuel.G
    ids = {it["id"] for it in G["items"] if it["name"].startswith(PREFIX)}
    for it in G["items"]:
        if it["id"] in ids and it.get("fp"):
            x0, x1 = it["fp"][0], it["fp"][1]
            it["fp"][0], it["fp"][1] = mx(x1), mx(x0)
    n = 0
    for p in G["parts"]:
        if p["item"] in ids:
            mirror_part(p)
            n += 1
    for d in G.get("decals", []):
        if d["item"] in ids:
            mirror_decal(d)
            n += 1
    return n


def mirror_decal(d):
    d["c"][0] = mx(d["c"][0])
    d["n"][0] = -d["n"][0]


def since():
    return len(fuel.G["parts"]), len(fuel.G.get("decals", []))


def mirror_since(mark, item=None):
    """Mirror the parts and decals added after `mark` (and the footprint of `item`, if given)."""
    np, nd = mark
    for p in fuel.G["parts"][np:]:
        mirror_part(p)
    for d in fuel.G.get("decals", [])[nd:]:
        mirror_decal(d)
    if item is not None and item.get("fp"):
        x0, x1 = item["fp"][0], item["fp"][1]
        item["fp"][0], item["fp"][1] = mx(x1), mx(x0)
