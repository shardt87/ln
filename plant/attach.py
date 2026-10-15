"""Final pass (user review: "nothing floating"): every part above grade that touches nothing gets fixed.
- nearest support below it (a hoop, a rail, a cylinder, a lamp over a slab): a post down onto that support;
- nearest support beside it (a wall lamp, a beacon, a box standing off a wall): a short mounting bracket across
  the gap;
- small dressing with nothing at all within 3.5 ft (left over from an earlier layout) is removed.
Gaps under 0.3 ft are treated as contact. Runs on the final part list, before the model is written."""
from collections import defaultdict

TOL, REACH = .3, 3.5
SKIP_LAYERS = {"UNDERGROUND", "OPT_UNDERGROUND"}


def bb(p):
    if p["kind"] in ("box", "prism"):
        return list(p["min"]) + list(p["max"])
    if p["kind"] == "rod":
        a, b, r = p["a"], p["b"], max(p["r"], p.get("r2", p["r"]))
        return [min(a[0], b[0]) - r, min(a[1], b[1]) - r, min(a[2], b[2]) - r,
                max(a[0], b[0]) + r, max(a[1], b[1]) + r, max(a[2], b[2]) + r]
    xs, ys, zs = zip(*p["v"])
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]


def gap(a, b):
    d = [max(0, b[i] - a[i + 3], a[i] - b[i + 3]) for i in range(3)]
    return (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** .5, d


def run(parts, item_layer):
    B = [bb(p) for p in parts]
    grid, big = defaultdict(list), []
    for k, b in enumerate(B):
        if b[3] - b[0] > 300 or b[4] - b[1] > 300:
            big.append(k)
            continue
        for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
            for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
                grid[(gx, gy)].append(k)

    def cands(b, m):
        seen = set()
        for gx in range(int((b[0] - m) // 10), int((b[3] + m) // 10) + 1):
            for gy in range(int((b[1] - m) // 10), int((b[4] + m) // 10) + 1):
                for k in grid.get((gx, gy), ()):
                    if k not in seen:
                        seen.add(k)
                        yield k
        yield from big

    new, drop, n_post, n_br = [], set(), 0, 0
    for k, (p, b) in enumerate(zip(parts, B)):
        if b[2] < .6 or p.get("layer") in SKIP_LAYERS or item_layer.get(p["item"]) in SKIP_LAYERS:
            continue
        best = None
        for j in cands(b, REACH):
            if j == k:
                continue
            g, d = gap(b, B[j])
            if g <= TOL:
                best = None
                break
            if best is None or g < best[0]:
                best = (g, j, d)
        else:
            if best is None or best[0] > REACH:                # nothing within reach: stray dressing
                vol = (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2])
                if vol < 60:
                    drop.add(k)
                continue
            g, j, d = best
            o = B[j]
            base = dict(item=p["item"], layer=p["layer"])
            if d[2] > 0 and o[5] <= b[2] and d[0] < .5 and d[1] < .5:        # support below: posts down onto it
                long_x, long_y = b[3] - b[0] > 3, b[4] - b[1] > 3
                xs = [b[0] + .1, b[3] - .1] if long_x else [(b[0] + b[3]) / 2]
                ys = [b[1] + .1, b[4] - .1] if long_y else [(b[1] + b[4]) / 2]
                pts = [(x, (b[1] + b[4]) / 2) for x in xs] if long_x else [((b[0] + b[3]) / 2, y) for y in ys]
                for (x, y) in pts:
                    x = min(max(x, o[0] + .05), o[3] - .05)
                    y = min(max(y, o[1] + .05), o[4] - .05)
                    new.append(dict(kind="rod", a=[round(x, 2), round(y, 2), round(o[5], 2)],
                                    b=[round(x, 2), round(y, 2), round(b[2] + .05, 2)], r=.06, r2=.06, color="steel",
                                    seg=6, d=1, **base))
                    n_post += 1
            else:                                                            # beside: a bracket across the gap
                c = [(b[i] + b[i + 3]) / 2 for i in range(3)]
                lo = [min(b[i + 3], o[i + 3]) if d[i] > 0 and b[i] > o[i + 3] else (b[i + 3] if d[i] > 0 else c[i] - .08)
                      for i in range(3)]
                hi = [max(b[i], o[i]) if d[i] > 0 and b[i] > o[i + 3] else (o[i] if d[i] > 0 else c[i] + .08)
                      for i in range(3)]
                mn = [min(lo[i], hi[i]) for i in range(3)]
                mx = [max(lo[i], hi[i]) for i in range(3)]
                for i in range(3):
                    if d[i] > 0:
                        if b[i] > o[i + 3]:
                            mn[i], mx[i] = o[i + 3] - .02, b[i] + .02
                        else:
                            mn[i], mx[i] = b[i + 3] - .02, o[i] + .02
                    else:
                        mn[i], mx[i] = c[i] - .08, c[i] + .08
                new.append(dict(kind="box", min=[round(v, 2) for v in mn], max=[round(v, 2) for v in mx],
                                color="steel", d=1, **base))
                n_br += 1
    parts[:] = [p for k, p in enumerate(parts) if k not in drop] + new
    return n_post, n_br, len(drop)


def signs(parts, decals):
    """Printed panels with nothing behind or beside them get two posts to grade (a free-standing sign)."""
    B = [bb(p) for p in parts]
    grid = defaultdict(list)
    for k, b in enumerate(B):
        if b[3] - b[0] > 300 or b[4] - b[1] > 300:
            continue
        for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
            for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
                grid[(gx, gy)].append(k)
    n = 0
    for d in decals:
        c, w, h, nrm = d["c"], d["w"], d["h"], d["n"]
        if c[2] < .5 or abs(nrm[2]) > .5:
            continue
        m = max(.6, w / 2)
        hit = False
        for gx in range(int((c[0] - m) // 10), int((c[0] + m) // 10) + 1):
            for gy in range(int((c[1] - m) // 10), int((c[1] + m) // 10) + 1):
                for k in grid.get((gx, gy), ()):
                    b = B[k]
                    if b[0] - m <= c[0] <= b[3] + m and b[1] - m <= c[1] <= b[4] + m and b[2] - .6 <= c[2] <= b[5] + .6:
                        hit = True
                        break
                if hit:
                    break
            if hit:
                break
        if hit:
            continue
        tx, ty = -nrm[1], nrm[0]                                   # along the panel
        for s in (-1, 1):
            x, y = c[0] + tx * s * (w / 2 - .2) - nrm[0] * .08, c[1] + ty * s * (w / 2 - .2) - nrm[1] * .08
            parts.append(dict(kind="rod", a=[round(x, 2), round(y, 2), 0], b=[round(x, 2), round(y, 2), round(c[2] + h / 2, 2)],
                              r=.07, r2=.07, color="steel", seg=6, d=1, item=d["item"], layer=d["layer"]))
        n += 1
    return n
