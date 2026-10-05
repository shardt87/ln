"""Strung conductors that hang like conductors (typical, not engineered).

Every overhead conductor was a straight rod between its end points. Strung (flexible) conductors
sag between their supports; this replaces them with catenaries:
- 230 kV strain buses: spans between the dead-end structures (x 530, 1300, 1925, 2045), about
  0.7 % sag; the bay droppers now meet the bus at its sagged height;
- overhead shield wires on the dead-end peaks, ~0.5 % sag;
- the GSU -> switchyard 230 kV overhead lines (drawn as routes) as three phase conductors with
  sag, with angle / dead-end structures where the drawn route turns;
- the H-MOD tie between its monopoles, insulator strings at each pole;
- short jumpers and droppers (bushing to gantry, arrester taps) with a slight curve.
Rigid tubular bus (the bay conductors on post insulators at EL 26) stays straight, as it is.
"""
import math

import fuel
from fuel import box, rod, find

PH = (-7, 0, 7)


def cat_pts(a, b, sag, n=16):
    """Points of a catenary-like curve (parabola, adequate for small sag / span) from a to b."""
    pts = []
    for k in range(n + 1):
        t = k / n
        p = [a[j] + (b[j] - a[j]) * t for j in range(3)]
        p[2] -= 4 * sag * t * (1 - t)
        pts.append(p)
    return pts


def strung(a, b, sag, r, c="conductor", n=16, layer=None):
    pts = cat_pts(a, b, sag, n)
    for p, q in zip(pts, pts[1:]):
        rod(p, q, r, c, seg=6, layer=layer)


def bus_z(x, spans, z0, rate):
    for (xa, xb) in spans:
        if xa - .01 <= x <= xb + .01:
            L = xb - xa
            t = (x - xa) / L
            return z0 - 4 * rate * L * t * (1 - t)
    return z0


def _take(pred):
    parts = fuel.G["parts"]
    out = [p for p in parts if pred(p)]
    keep = [p for p in parts if not pred(p)]
    parts[:] = keep
    return out


def strain_buses():
    spans = [(530, 1300), (1300, 1925), (1925, 2045)]
    rate = .007
    names = [it for it in fuel.G["items"] if it["name"].startswith("230 kV bus ")]
    ids = {it["id"]: it for it in names}
    old = _take(lambda p: p["item"] in ids and p["kind"] == "rod" and p["color"] == "conductor"
                and abs(p["a"][2] - 40) < .01 and abs(p["b"][2] - 40) < .01)
    for p in old:
        it = ids[p["item"]]
        fuel.G["cur"] = it
        y = p["a"][1]
        x0, x1 = sorted((p["a"][0], p["b"][0]))
        for (xa, xb) in spans:
            if xa >= x0 - .01 and xb <= x1 + .01:
                strung((xa, y, 40), (xb, y, 40), rate * (xb - xa), .35, layer=p.get("layer"))
    # bay droppers: from the bus (now sagged) down to the rigid bay bus
    for p in fuel.G["parts"]:
        if p["kind"] == "rod" and p["color"] == "conductor" and p["a"][1] in (65, 237) and p["b"][1] == p["a"][1] \
                and p["a"][0] == p["b"][0] and abs(p["a"][2] - 40) < .01 and abs(p["b"][2] - 26) < .01:
            p["a"][2] = round(bus_z(p["a"][0], spans, 40, rate), 2)
    return len(old)


def shield_wires():
    ids = {it["id"] for it in fuel.G["items"] if it["name"].startswith("230 kV bus ")}
    old = _take(lambda p: p["item"] in ids and p["kind"] == "rod" and p["color"] == "conductor"
                and abs(p["a"][2] - 55) < .01 and abs(p["b"][2] - 55) < .01)
    for p in old:
        fuel.G["cur"] = next(it for it in fuel.G["items"] if it["id"] == p["item"])
        y = p["a"][1]
        for (xa, xb) in ((530, 1300), (1300, 1925)):
            strung((xa, y, 55), (xb, y, 55), .005 * (xb - xa), .08, layer=p.get("layer"))
    return len(old)


def jumpers():
    """Short slanted conductor rods (droppers, jumpers) get a slight curve."""
    old = _take(lambda p: p["kind"] == "rod" and p["color"] == "conductor"
                and 2 < math.dist(p["a"], p["b"]) < 60 and abs(p["a"][2] - p["b"][2]) > .5
                and (abs(p["a"][0] - p["b"][0]) > .5 or abs(p["a"][1] - p["b"][1]) > .5))
    for p in old:
        fuel.G["cur"] = next(it for it in fuel.G["items"] if it["id"] == p["item"])
        L = math.dist(p["a"], p["b"])
        d = p.get("d")
        fuel.D = bool(d)
        strung(p["a"], p["b"], .04 * L + .2, p["r"], n=8, layer=p.get("layer"))
        fuel.D = False
    return len(old)


def _offset_poly(pts, o):
    """Polyline offset by o to the left, mitred at the corners."""
    out = []
    for k, p in enumerate(pts):
        ns, segs = [], []
        if k > 0:
            segs.append((pts[k - 1], p))
        if k < len(pts) - 1:
            segs.append((p, pts[k + 1]))
        for a, b in segs:
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            ns.append((-dy / L, dx / L))
        if len(ns) == 1:
            mx, my = ns[0][0] * o, ns[0][1] * o
        else:
            dot = ns[0][0] * ns[1][0] + ns[0][1] * ns[1][1]
            mx, my = (ns[0][0] + ns[1][0]) * o / (1 + dot), (ns[0][1] + ns[1][1]) * o / (1 + dot)
        out.append((p[0] + mx, p[1] + my))
    return out


def overhead_lines(routes):
    """GSU -> switchyard 230 kV overhead (drawn routes) as phase conductors with sag; angle structures."""
    n = 0
    for r in routes:
        if r["type"] != "hv_overhead":
            continue
        pts = [tuple(p) for p in r["points"]]
        it = fuel.new_item(r["layer"], f"230 kV overhead line conductors {pts[0][0]:.0f}-{pts[-1][0]:.0f}",
                           (min(p[0] for p in pts) - 9, max(p[0] for p in pts) + 9, min(p[1] for p in pts) - 9,
                            max(p[1] for p in pts) + 9), (30, 46), basis="typical", register=False, area="C",
                           sheet="typical (strung conductors)",
                           info="ACSR conductors, three phases 7 ft apart, sagging between the gantries and the "
                                "angle structures (typical).")
        for o in PH:
            q = _offset_poly(pts, o)
            for a, b in zip(q, q[1:]):
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                strung((a[0], a[1], 41.5), (b[0], b[1], 41.5), .03 * L + .5, .2, layer=r["layer"])
        n += 1
        # angle structures at the interior points: steel monopole, crossarm along the bisector with
        # strain insulators at the three phase positions
        qs = {o: _offset_poly(pts, o) for o in PH}
        roads = [i["fp"] for i in fuel.G["items"] if i["layer"] == "SITE" and "road" in i["name"].lower()]
        for k in range(1, len(pts) - 1):
            x, y = pts[k]
            for f in roads:                                       # the pole stands clear of any road (6 ft margin)
                if f[0] - 6 < x < f[1] + 6 and f[2] - 6 < y < f[3] + 6:
                    y = f[2] - 6 if abs(y - f[2]) < abs(y - f[3]) else f[3] + 6
            fuel.new_item(r["layer"], "230 kV angle structure (steel monopole)", (x - 12, x + 12, y - 12, y + 12),
                          (0, 48), basis="typical", register=False, area="C", sheet="typical (strung conductors)")
            box(x - 2.5, x + 2.5, y - 2.5, y + 2.5, 0, .5, "concrete")                     # drilled-pier cap
            rod((x, y, .5), (x, y, 48), 1.1, "steel", r2=.6, seg=10)
            (ax, ay), (bx, by) = qs[PH[0]][k], qs[PH[-1]][k]
            rod((ax, ay, 44.5), (bx, by, 44.5), .4, "steel", seg=6)                        # crossarm
            for o in PH:
                qx, qy = qs[o][k]
                rod((qx, qy, 44.3), (qx, qy, 41.6), .3, "insulator", seg=6)
    return n


def hmod():
    poles = [(2095, 815), (1950, 805), (1800, 805), (1650, 805), (1515, 805), (1515, 650), (1515, 500),
             (1515, 350), (1515, 262), (1690, 262)]
    it = find("H-MOD 230 kV monopoles")
    fuel.G["cur"] = it
    path = poles + [(1690, 237), (1720, 130)]
    for o in (-5, 0, 5):
        q = _offset_poly(path, o)
        for k, (a, b) in enumerate(zip(q, q[1:])):
            za = 41.0
            zb = 41.0 if k < len(q) - 2 else 41.5
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            strung((a[0], a[1], za), (b[0], b[1], zb), .025 * L + .5, .22, layer=it["layer"])
        for (x, y) in q[:len(poles)]:
            rod((x, y, 45), (x, y, 41), .25, "insulator", seg=6)                      # suspension string
    return len(poles)


def build(routes):
    return dict(strain=strain_buses(), shield=shield_wires(), jumpers=jumpers(), lines=overhead_lines(routes),
                hmod=hmod())
