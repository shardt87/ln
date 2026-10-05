"""Pipe-end termination pass (quality sweep): every pipe end that would otherwise stop in mid-air gets a
realistic ending, chosen by its direction and what is around it:
- a horizontal end or a downward end with room below: a long-radius elbow and a drop to grade, where the line
  goes underground through a concrete sleeve block (the usual UG transition in a plant yard);
- an upward end (a pump discharge nozzle, a riser top): an isolation valve with a handwheel, then an elbow,
  a short run and the same drop to grade where there is room;
- anything with no clear path down (roofs, platforms, congested racks): a blind flange with its bolting ring.
Pipes run on short pipe shoes over flat roofs (data-hall headers) instead of floating above them.
Runs after all geometry; typical, not engineered."""
import math
from collections import defaultdict

PIPE = {"pipe", "waterline", "fuelgas", "fueloil", "steam", "lngpipe", "cw", "chw", "hydrogen", "pvc_blue",
        "pvc_green", "hdpe", "ductile"}
SKIP = ("People", "Vehicles", "Parking", "Compound", "Underground", "Duct-bank manholes", "Underground: cable-pull")
G = 10


def _pbox(p):
    if p["kind"] in ("box", "prism"):
        return p["min"] + p["max"]
    if p["kind"] == "rod":
        a, c, r = p["a"], p["b"], max(p["r"], p["r2"])
        ax = [i for i in range(3) if a[i] != c[i]]
        pr = [0 if i in ax else r for i in range(3)] if len(ax) == 1 else [r] * 3
        return [min(a[i], c[i]) - pr[i] for i in range(3)] + [max(a[i], c[i]) + pr[i] for i in range(3)]
    xs, ys, zs = zip(*p["v"])
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]


def build(items, parts):
    byid = {it["id"]: it for it in items}
    B = [_pbox(p) for p in parts]
    grid = defaultdict(list)
    for k, b in enumerate(B):
        if (b[3] - b[0] > 400 or b[4] - b[1] > 400) and b[5] <= .8:
            continue
        for gx in range(int(b[0] // G), int(b[3] // G) + 1):
            for gy in range(int(b[1] // G), int(b[4] // G) + 1):
                grid[(gx, gy)].append(k)

    def hits(b, skip=()):
        out = []
        for gx in range(int(b[0] // G), int(b[3] // G) + 1):
            for gy in range(int(b[1] // G), int(b[4] // G) + 1):
                for j in grid.get((gx, gy), ()):
                    if j in skip:
                        continue
                    c = B[j]
                    if b[0] <= c[3] and b[3] >= c[0] and b[1] <= c[4] and b[4] >= c[1] and b[2] <= c[5] and b[5] >= c[2]:
                        out.append(j)
        return out

    new = []

    def add(kind, item, layer, **kw):
        kw.update(item=item, layer=layer, d=1)
        new.append(dict(kind=kind, **kw))

    n_drop = n_valve = n_flange = 0
    for k, p in enumerate(list(parts)):
        if p["kind"] != "rod" or p["color"] not in PIPE or p["r"] < .2 or p["r"] > 2.5:
            continue
        it = byid[p["item"]]
        if it["name"].startswith(SKIP) or p["layer"] in ("UNDERGROUND", "OPT_UNDERGROUND"):
            continue
        r = p["r"]
        for end, other in ((p["a"], p["b"]), (p["b"], p["a"])):
            if end[2] < .9:
                continue
            q = .3 + r
            box = [end[0] - q, end[1] - q, end[2] - q, end[0] + q, end[1] + q, end[2] + q]
            if hits(box, skip={k}):
                continue                                         # meets something: connected
            L = math.dist(end, other) or 1
            d = [(end[i] - other[i]) / L for i in range(3)]       # outward direction
            item, layer, col = p["item"], p["layer"], p["color"]

            def floor_under(x, y, z0):
                """Top of the highest surface under (x, y) below z0 (grade 0, or a pad / slab / platform)."""
                b = [x - r - .1, y - r - .1, -1, x + r + .1, y + r + .1, z0 - r - .2]
                tops = [B[j][5] for j in hits(b, skip={k})]
                return max([0.0] + tops)

            def clear_drop(x, y, z0):
                f = floor_under(x, y, z0)
                return (z0 - f > 1.0) and (f < 1.6), f
            if d[2] > .7:                                         # upward end: valve, elbow, run, drop
                vz = end[2] + .4
                add("rod", item, layer, a=list(end), b=[end[0], end[1], vz + .9], r=r * 1.25, r2=r * 1.25, color="steel", seg=10)
                add("rod", item, layer, a=[end[0], end[1], vz + .9], b=[end[0], end[1], vz + 2.2], r=.08, r2=.08, color="steel", seg=4)
                add("rod", item, layer, a=[end[0] - .7, end[1], vz + 2.2], b=[end[0] + .7, end[1], vz + 2.25], r=.7, r2=.7,
                    color="red", seg=12)                          # handwheel
                n_valve += 1
                continue
            if abs(d[2]) < .3:                                    # horizontal end: elbow down, drop to grade
                ex, ey = end[0] + d[0] * (r + .4), end[1] + d[1] * (r + .4)
                ok, f = clear_drop(ex, ey, end[2])
                if ok and not hits([min(end[0], ex) - r, min(end[1], ey) - r, end[2] - r,
                                    max(end[0], ex) + r, max(end[1], ey) + r, end[2] + r], skip={k}):
                    add("rod", item, layer, a=list(end), b=[ex, ey, end[2]], r=r, r2=r, color=col, seg=10)
                    add("rod", item, layer, a=[ex, ey, end[2] + r * .2], b=[ex, ey, f + .3], r=r, r2=r, color=col, seg=10)
                    add("rod", item, layer, a=[ex, ey, end[2] - .05], b=[ex, ey, end[2] + .05], r=r * 1.12, r2=r * 1.12,
                        color="steel", seg=10)            # elbow weld band
                    add("box", item, layer, min=[ex - r - .6, ey - r - .6, f], max=[ex + r + .6, ey + r + .6, f + .45],
                        color="concrete")                 # UG transition / sleeve block (on grade or the pad)
                    n_drop += 1
                    continue
            ok, f = clear_drop(end[0], end[1], end[2] + r) if d[2] < -.7 else (False, 0)
            if ok:                                                # downward end: on to grade / the pad
                add("rod", item, layer, a=list(end), b=[end[0], end[1], f + .3], r=r, r2=r, color=col, seg=10)
                add("box", item, layer, min=[end[0] - r - .6, end[1] - r - .6, f], max=[end[0] + r + .6, end[1] + r + .6, f + .45],
                    color="concrete")
                n_drop += 1
                continue
            fa = [end[i] + d[i] * .18 for i in range(3)]          # blind flange
            add("rod", item, layer, a=list(end), b=fa, r=r * 1.55, r2=r * 1.55, color="steel", seg=14)
            n_flange += 1
    parts.extend(new)
    return dict(drops=n_drop, valves=n_valve, blind_flanges=n_flange)


def support_floating(items, parts):
    """Parts above grade that touch nothing (a conservator over its tank, a pump casing over its baseplate, a
    stair tread with no stringer, a header over a roof) get steel legs / pipe shoes down to the surface below
    them, when that surface is within 6 ft; tiny fittings and lights are left as they are."""
    byid = {it["id"]: it for it in items}
    B = [_pbox(p) for p in parts]
    grid = defaultdict(list)
    for k, b in enumerate(B):
        if (b[3] - b[0] > 400 or b[4] - b[1] > 400) and b[5] <= .8:
            continue
        for gx in range(int(b[0] // G), int(b[3] // G) + 1):
            for gy in range(int(b[1] // G), int(b[4] // G) + 1):
                grid[(gx, gy)].append(k)

    def hits(b, skip=()):
        out = []
        for gx in range(int(b[0] // G), int(b[3] // G) + 1):
            for gy in range(int(b[1] // G), int(b[4] // G) + 1):
                for j in grid.get((gx, gy), ()):
                    if j in skip:
                        continue
                    c = B[j]
                    if b[0] <= c[3] and b[3] >= c[0] and b[1] <= c[4] and b[4] >= c[1] and b[2] <= c[5] and b[5] >= c[2]:
                        out.append(j)
        return out
    new, n = [], 0
    for k, p in enumerate(parts):
        it = byid[p["item"]]
        if it["name"].startswith(SKIP) or p["layer"] in ("UNDERGROUND", "OPT_UNDERGROUND") or it["layer"] == "SITE":
            continue
        b = B[k]
        if b[2] <= .6 or p["color"] in ("red", "lamp", "copper", "rail", "sign", "label", "conductor"):
            continue
        if max(b[3] - b[0], b[4] - b[1], b[5] - b[2]) < .8:
            continue
        pad = .35
        if hits([b[0] - pad, b[1] - pad, b[2] - pad, b[3] + pad, b[4] + pad, b[5] + pad], skip={k}):
            continue
        # surface below: highest top under the part's footprint within 6 ft
        under = hits([b[0], b[1], b[2] - 6, b[3], b[4], b[2] - .01], skip={k})
        top = max([B[j][5] for j in under if B[j][5] < b[2]] + ([0.0] if b[2] < 6 else []), default=None)
        if top is None:
            continue
        w, d = b[3] - b[0], b[4] - b[1]
        along_x = w >= d
        legs = ([(b[0] + w * .2, (b[1] + b[4]) / 2), (b[3] - w * .2, (b[1] + b[4]) / 2)] if along_x else
                [((b[0] + b[3]) / 2, b[1] + d * .2), ((b[0] + b[3]) / 2, b[4] - d * .2)])
        if max(w, d) < 2.5:
            legs = [((b[0] + b[3]) / 2, (b[1] + b[4]) / 2)]
        s = min(.25, .15 + .02 * max(w, d))
        for (x, y) in legs:
            new.append(dict(kind="box", min=[round(x - s, 2), round(y - s, 2), round(top, 2)],
                            max=[round(x + s, 2), round(y + s, 2), round(b[2] + .05, 2)], color="steel",
                            item=p["item"], layer=p["layer"], d=1))
        n += 1
    parts.extend(new)
    return n
