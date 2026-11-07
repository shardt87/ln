"""Turbine-hall tray supports as built: shared tray-support frames instead of a forest of single posts.

The tray generator supports each tray on its own trapeze (two thin posts and a beam). In the hall the north-south
tray branches to each unit run side by side over the EL 20 operating floor, so the deck ended up with several
hundred thin posts, which reads wrong at eye level. Real halls carry parallel branches on shared tray-support
frames: two W8 columns per station on base plates, one cross-beam per tray level spanning the group, knee braces,
stations about every 20 ft. This pass replaces the per-tray posts and beams on the deck with those frames.
"""
import fuel
from fuel import box, rod

DECK = (560.0, 1100.0, 404.0, 540.0)          # operating floor; the north-wall trunk (y > 540) keeps its brackets


def build():
    G = fuel.G
    tr = next(i for i in G["items"] if i["name"].startswith("Cable trays and isolated"))
    P = G["parts"]
    x0, x1, y0, y1 = DECK
    posts = [p for p in P if p["item"] == tr["id"] and p["kind"] == "box" and p["color"] == "steel"
             and abs(p["min"][2] - 20) < .6 and p["max"][2] - p["min"][2] > 8
             and p["max"][0] - p["min"][0] < 1 and p["max"][1] - p["min"][1] < 1
             and x0 < p["min"][0] < x1 and y0 < p["min"][1] < y1]
    if not posts:
        return 0
    tops = {round(p["max"][2], 1) for p in posts}
    pid = {id(p) for p in posts}
    # trapeze beams sitting on those posts
    beams = [p for p in P if p["item"] == tr["id"] and p["kind"] == "box" and p["color"] == "steel"
             and round(p["min"][2], 1) in tops and p["max"][2] - p["min"][2] < .6
             and x0 - 3 < p["min"][0] < x1 and y0 - 3 < p["min"][1] < y1]
    bid = {id(p) for p in beams}

    def c(p):
        return ((p["min"][0] + p["max"][0]) / 2, (p["min"][1] + p["max"][1]) / 2)

    # group posts: N-S branches -> stations along y; cluster across x where branches run side by side
    stations = {}
    for p in posts:
        x, y = c(p)
        stations.setdefault(round(y / 3) * 3, []).append(p)
    frames = []
    for ys in sorted(stations):
        grp = sorted(stations[ys], key=lambda p: c(p)[0])
        cl = [[grp[0]]]
        for p in grp[1:]:
            if c(p)[0] - c(cl[-1][-1])[0] < 9:
                cl[-1].append(p)
            else:
                cl.append([p])
        for g in cl:
            frames.append((ys, g))
    # thin the stations: keep a frame about every 20 ft along each branch cluster (by x band)
    keep, last = [], {}
    for (ys, g) in sorted(frames, key=lambda t: (round(c(t[1][0])[0] / 10), t[0])):
        band = round(c(g[0])[0] / 10)
        if band in last and ys - last[band] < 17:
            continue
        last[band] = ys
        keep.append((ys, g))
    # a frame only where its cross-beams and columns are clear of everything but the trays; otherwise the group keeps
    # its own trapezes
    import gas_lod3
    S = gas_lod3.Space()
    trid = tr["id"]
    S2 = gas_lod3.Space.__new__(gas_lod3.Space)
    S2.b, S2.grid = [], {}
    items = {i["id"]: i for i in G["items"]}
    for p in P:
        it = items[p["item"]]
        if p["item"] == trid or it["layer"] in ("SITE", "UNDERGROUND", "OPT_UNDERGROUND") or it["z"][1] < .7 \
                or it["name"].startswith(("Turbine deck", "Common turbine hall")):
            continue
        S2.add(gas_lod3.Space.pbox(p))
    good, kept_posts = [], set()
    for (ys, g) in keep:
        xs = [c(p)[0] for p in g]
        ya = sum(c(p)[1] for p in g) / len(g)
        xa, xb = min(xs) - .1, max(xs) + .1
        levels = sorted({round(p["max"][2], 1) for p in g})
        ok = all(S2.free(xa - .4, xb + .4, ya - .25, ya + .25, zl + .02, zl + .38, m=0) for zl in levels) and \
            all(S2.free(xc - .45, xc + .45, ya - .45, ya + .45, 20.02, max(levels) + .3, m=0) for xc in (xa, xb))
        if ok:
            good.append((ys, g))
        else:
            kept_posts.update(id(p) for p in g)
    # stations that were thinned out lose their posts only if a frame in the same x band carries the span
    kept_bands = {}
    for (ys, g) in good:
        kept_bands.setdefault(round(c(g[0])[0] / 10), []).append(ys)
    for (ys, g) in frames:
        band = round(c(g[0])[0] / 10)
        if (ys, g) in good:
            continue
        near = [y for y in kept_bands.get(band, []) if abs(y - ys) <= 21]
        if not near:
            kept_posts.update(id(p) for p in g)
    keep = good
    rm_posts = pid - kept_posts
    kept_tops = {(round(c(p)[0], 1), round(c(p)[1], 1)) for p in posts if id(p) in kept_posts}

    def beam_kept(b):
        bx0, by0, bx1, by1 = b["min"][0], b["min"][1], b["max"][0], b["max"][1]
        return any(bx0 - .5 <= x <= bx1 + .5 and by0 - .5 <= y <= by1 + .5 for (x, y) in kept_tops)
    rm_beams = {id(b) for b in beams if not beam_kept(b)}
    fuel.G["parts"][:] = [p for p in P if id(p) not in rm_posts and id(p) not in rm_beams]
    fuel.on(tr)
    fuel.D = True
    n = 0
    for (ys, g) in keep:
        xs = [c(p)[0] for p in g]
        ya = sum(c(p)[1] for p in g) / len(g)
        xa, xb = min(xs) - .1, max(xs) + .1
        levels = sorted({round(p["max"][2], 1) for p in g})
        ztop = max(levels) + .4
        for xc in (xa, xb):                                                        # W8 columns on base plates
            box(xc - .33, xc + .33, ya - .17, ya + .17, 20.0, ztop, "steel")
            box(xc - .06, xc + .06, ya - .33, ya + .33, 20.0, ztop, "steel")
            box(xc - .45, xc + .45, ya - .45, ya + .45, 20.0, 20.1, "steel")
        for zl in levels:                                                          # cross-beam per tray level
            box(xa - .4, xb + .4, ya - .25, ya + .25, zl, zl + .4, "steel")
        for xc, s in ((xa, 1), (xb, -1)):                                          # knee braces under the top beam
            if xb - xa > 3:
                rod((xc, ya, ztop - 3.5), (xc + s * 2.5, ya, ztop - .45), .1, "steel", seg=6)
        n += 1
    fuel.D = False
    return n, len(rm_posts)
