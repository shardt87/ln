"""Underground systems at LOD 3 (typical, not engineered).

Until now the buried systems were route data drawn as strips painted on grade. This builds them
below grade in real finishes, in their own layers (UNDERGROUND for the base plant,
OPT_UNDERGROUND for the design options), shown by the viewer's "U Underground" view with the
ground taken away:
- duct banks: concrete encasement (red-dyed top, the usual warning to excavators) at 2.5 ft cover
  along every buried cable route (13.8 kV / LV duct banks and the option feeders), the 230 kV cable
  banks deeper at 3.5 ft cover; precast manhole chambers under the covers at bends and every
  ~300 ft, handhole boxes at feeder ends;
- station ground grid: bare 4/0 Cu mesh at 1.5 ft depth under the power block, electrical areas
  and switchyard (40 ft mesh, 20 ft in the switchyard), driven rods at the perimeter, risers to
  the equipment;
- firewater ring main: ductile iron at 5 ft cover along the drawn ring and its branches;
- storm drainage: reinforced-concrete pipe under each road edge, catch-basin chambers with
  laterals, storm manholes at the junctions, the trunk to the pond inlet headwall;
- oily-water drains (HDPE): transformer containment sumps, turbine-hall lube-oil drains and the
  station transformers to the oil-water separator, separator to wastewater treatment;
- sanitary sewer (green PVC): buildings to a packaged lift station, force main to the site
  boundary;
- potable water (blue PVC) from the water treatment building to the buildings, service water
  to the power block.
Depths keep the systems at least 1 ft apart where they cross: grid 1.5 ft, MV / LV duct banks from 2.5 ft,
230 kV banks from 3.5 ft, water 6.8 ft, firewater 7.3 ft, sanitary 7.8 ft, oily water 8.3 ft, storm 9-10 ft.
"""
import math

import fuel
from fuel import box, rod, find

UG, UGO = "UNDERGROUND", "OPT_UNDERGROUND"
BURIED = ("duct_bank", "mvlv_cable", "hv_cable", "lv_tray", "mv_tray", "control_tray")   # buried when z < 0
SHEET = "typical (underground)"


def _item(layer, name, info, **kw):
    return fuel.new_item(layer, name, (0, 2420, 0, 1920), (-12, .4), area=kw.pop("area", "A"), basis="typical",
                         sheet=SHEET, register=False, info=info, **kw)


def _merge(segs):
    """Collinear axis-aligned segments -> merged runs {(axis, c): [[a, b], ...]}."""
    runs = {}
    for (ax, ay), (bx, by) in segs:
        if ay == by and ax != bx:
            runs.setdefault(("x", ay), []).append((min(ax, bx), max(ax, bx)))
        elif ax == bx and ay != by:
            runs.setdefault(("y", ax), []).append((min(ay, by), max(ay, by)))
    out = {}
    for k, ivs in runs.items():
        ivs.sort()
        m = [list(ivs[0])]
        for a, b in ivs[1:]:
            if a <= m[-1][1] + 1e-6:
                m[-1][1] = max(m[-1][1], b)
            else:
                m.append([a, b])
        out[k] = m
    return out


def _dips(a, b, r):
    """Where a buried pipe segment a -> b (3-D) crosses a duct bank with less than 1 ft clear, the pipe dives
    under it: returns the polyline with the dips."""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < .01:
        return [a, b]
    cross = []
    for (x0, x1, y0, y1, zb, zt) in BANKS:
        # parameter interval of the segment inside the bank footprint
        t0, t1 = 0.0, 1.0
        ok = True
        for (p, q, lo, hi) in ((a[0], b[0], x0, x1), (a[1], b[1], y0, y1)):
            if abs(q - p) < 1e-9:
                if not (lo <= p <= hi):
                    ok = False
                    break
            else:
                u0, u1 = sorted(((lo - p) / (q - p), (hi - p) / (q - p)))
                t0, t1 = max(t0, u0), min(t1, u1)
        if not ok or t1 <= t0:
            continue
        zm = a[2] + (b[2] - a[2]) * (t0 + t1) / 2
        if zm + r > zb - 1 and zm - r < zt + 1:                    # conflict: dive under
            cross.append((t0, t1, zb - 1 - r))
    if not cross:
        return [a, b]
    cross.sort()
    out = [a]
    ramp = 3.0 / L
    for (t0, t1, zn) in cross:
        for t, zz in ((t0 - ramp, None), (t0 - .5 / L, zn), (t1 + .5 / L, zn), (t1 + ramp, None)):
            t = min(max(t, 0), 1)
            zbase = a[2] + (b[2] - a[2]) * t
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, zbase if zz is None else min(zz, zbase)))
    out.append(b)
    return out


def _pipe_run(pts, z, r, c, seg=10):
    for a, b in zip(pts, pts[1:]):
        za = a[2] if len(a) > 2 else z
        zb = b[2] if len(b) > 2 else z
        q = _dips((a[0], a[1], za), (b[0], b[1], zb), r)
        for p_, q_ in zip(q, q[1:]):
            if math.dist(p_, q_) > .05:
                rod(p_, q_, r, c, seg=seg)


# ---------------------------------------------------------------------------------------------
TOP_MV, TOP_HV = -2.5, -5.25         # top of the encasement: 30 in cover (MV / LV); 230 kV 1 ft below the deepest MV bank
BANKS = []                            # encasement boxes, for the pipe crossings (pipes dive under with 1 ft clear)


def _bank_layout(n, hv):
    """Conduit layout for n circuits sharing a bank: ways (incl. spares), columns, rows, radius, pitch."""
    if hv:
        ways = min(3 * n + 1, 13)                  # one 8 in conduit per phase + a fibre / ground duct
        cols = 4 if ways > 3 else ways
        return ways, cols, -(-ways // cols), .36, .95
    ways = min(n + max(1, (n + 1) // 2), 24)       # one 5 in conduit per feeder + about 50 % spares
    ways = max(ways, 4)
    cols = 2 if ways <= 4 else -(-ways // 2)       # never more than two rows deep: wider, not deeper
    return ways, cols, -(-ways // cols), .22, .62


def _lines(segs):
    """Per line (axis, c): sub-intervals with the number of distinct routes along them."""
    lines = {}
    for rid, ((ax, ay), (bx, by)) in segs:
        if ay == by and ax != bx:
            lines.setdefault(("x", ay), []).append((min(ax, bx), max(ax, bx), rid))
        elif ax == bx and ay != by:
            lines.setdefault(("y", ax), []).append((min(ay, by), max(ay, by), rid))
    out = {}
    for k, ivs in lines.items():
        cuts = sorted({v for a, b, _ in ivs for v in (a, b)})
        subs = []
        for a, b in zip(cuts, cuts[1:]):
            ids = {rid for (p, q, rid) in ivs if p <= a + 1e-6 and q >= b - 1e-6}
            if ids:
                if subs and subs[-1][1] == a and subs[-1][2] == len(ids):
                    subs[-1][1] = b
                else:
                    subs.append([a, b, len(ids)])
        out[k] = subs
    return out


def duct_banks(routes, items):
    """Duct banks as built: PVC conduits in a concrete encasement with a red-dyed top, sized for the circuits
    that share each stretch; long-radius sweeps at the corners; warning tape 12 in above; stub-ups (90 deg
    sweeps up to grade) into the equipment at the feeder ends. The encasement is drawn as a cast section so the
    conduits read through it in the underground view."""
    groups = {}
    for rid, r in enumerate(routes):
        if r["type"] not in BURIED or r["z"] >= 0:
            continue
        opt = r["layer"].startswith("OPT_") or r["layer"] in ("SWYD_FUTURE", "HV_CORRIDOR")
        hv = r["type"] == "hv_cable"
        pts = []
        for a, b in zip(r["points"], r["points"][1:]):                       # a stray diagonal becomes an L
            pts.append((tuple(a), (b[0], a[1])) if a[0] != b[0] and a[1] != b[1] else (tuple(a), tuple(b)))
            if a[0] != b[0] and a[1] != b[1]:
                pts.append(((b[0], a[1]), tuple(b)))
        groups.setdefault((opt, hv), {"segs": [], "ends": []})
        groups[(opt, hv)]["segs"].extend((rid, s) for s in pts)
        groups[(opt, hv)]["ends"].extend([tuple(r["points"][0]), tuple(r["points"][-1])])
    stats = dict(runs=0, conduits=0, bends=0, stubups=0, ways_max=0)
    pads = [it for it in items if it["layer"] != "SITE" and (it["fp"][1] - it["fp"][0]) < 1500]
    for (opt, hv), g in groups.items():
        label = ("230 kV cable banks" if hv else "MV / LV duct banks") + (" (design options)" if opt else "")
        _item(UGO if opt else UG, f"Underground: {label}",
              "PVC conduits in a concrete encasement with a red-dyed top (excavation warning), "
              + ("42 in cover; one 8 in conduit per phase per 230 kV circuit plus a fibre / ground duct" if hv else
                 "30 in cover; 5 in Schedule 40 PVC, one conduit per feeder plus about 50 % spare ways (2 x 2 up to 6 x 4)")
              + "; 3 in concrete round the conduits; long-radius sweeps at the bends; red warning tape 12 in above; "
                "90 degree sweeps up into the equipment at the feeder ends (typical).")
        top = TOP_HV if hv else TOP_MV
        lines = _lines(g["segs"])
        sect = {}                                  # (axis, c) -> list of (a, b, ways, cols, rows, r, pitch)
        for (axis, c), subs in lines.items():
            for a, b, n in subs:
                ways, cols, rows, rc, pt = _bank_layout(n, hv)
                sect.setdefault((axis, c), []).append((a, b, ways, cols, rows, rc, pt))
                stats["ways_max"] = max(stats["ways_max"], ways)
        # corner points: two stretches end perpendicular there and nothing runs through
        ends_at = {}
        for (axis, c), lst in sect.items():
            for k, (a, b, *_r) in enumerate(lst):
                for v, sg in ((a, -1), (b, 1)):
                    P = (round(v, 2), round(c, 2)) if axis == "x" else (round(c, 2), round(v, 2))
                    ends_at.setdefault(P, []).append((axis, c, k, sg))
        corners = {}
        for P, lst in ends_at.items():
            axes = {e[0] for e in lst}
            if len(lst) == 2 and len(axes) == 2:
                corners[P] = lst
        R0 = 3.0 if not hv else 4.5
        for (axis, c), lst in sect.items():
            for k, (a, b, ways, cols, rows, rc, pt) in enumerate(lst):
                W, H = cols * pt + .5, rows * pt + .5
                hw = W / 2
                Pa = (round(a, 2), round(c, 2)) if axis == "x" else (round(c, 2), round(a, 2))
                Pb = (round(b, 2), round(c, 2)) if axis == "x" else (round(c, 2), round(b, 2))
                # encasement: fills the corner square at a bend, otherwise stops at the stretch end
                ea = a - (hw if Pa in corners or Pa in ends_at and len(ends_at[Pa]) > 1 else 0)
                eb = b + (hw if Pb in corners or Pb in ends_at and len(ends_at[Pb]) > 1 else 0)
                BANKS.append(((ea, eb, c - hw, c + hw) if axis == "x" else (c - hw, c + hw, ea, eb)) + (top - H, top))
                for (z0, z1, col) in ((top - H, top - .12, "ductcase"), (top - .12, top, "ductcap")):
                    if axis == "x":
                        box(ea, eb, c - hw, c + hw, z0, z1, col)
                    else:
                        box(c - hw, c + hw, ea, eb, z0, z1, col)
                if axis == "x":                                                       # warning tape
                    box(ea, eb, c - .15, c + .15, top + .97, top + 1.0, "ductcap")
                else:
                    box(c - .15, c + .15, ea, eb, top + .97, top + 1.0, "ductcap")
                # conduits: they stop short of a corner, where the sweep takes over
                ca = a + (R0 if Pa in corners else 0)
                cb = b - (R0 if Pb in corners else 0)
                if cb - ca < .5:
                    continue
                for w_ in range(ways):
                    col_i, row_i = w_ % cols, w_ // cols
                    v = (col_i - (cols - 1) / 2) * pt
                    zc = top - .25 - pt / 2 - row_i * pt
                    cc = "pvc_orange" if (w_ == ways - 1 and not hv) else "pvc_grey"
                    if axis == "x":
                        rod((ca, c + v, zc), (cb, c + v, zc), rc, cc, seg=8)
                    else:
                        rod((c + v, ca, zc), (c + v, cb, zc), rc, cc, seg=8)
                    stats["conduits"] += 1
                stats["runs"] += 1
        # long-radius sweeps at the corners (conduits of the smaller stretch carried round)
        for P, ((ax1, c1, k1, s1), (ax2, c2, k2, s2)) in corners.items():
            l1, l2 = sect[(ax1, c1)][k1], sect[(ax2, c2)][k2]
            ways, cols, rows, rc, pt = min((l1[2:], l2[2:]), key=lambda t: t[0])
            d1 = (s1, 0) if ax1 == "x" else (0, s1)
            d2 = (-s2, 0) if ax2 == "x" else (0, -s2)
            x, y = P
            T1 = (x - d1[0] * R0, y - d1[1] * R0)
            O = (T1[0] + d2[0] * R0, T1[1] + d2[1] * R0)
            perp1 = (0, 1) if ax1 == "x" else (1, 0)
            sgn = perp1[0] * d2[0] + perp1[1] * d2[1]
            for w_ in range(ways):
                col_i, row_i = w_ % cols, w_ // cols
                v = (col_i - (cols - 1) / 2) * pt
                zc = top - .25 - pt / 2 - row_i * pt
                rr = R0 - v * sgn
                q = [(O[0] - d2[0] * rr * math.cos(t) + d1[0] * rr * math.sin(t),
                      O[1] - d2[1] * rr * math.cos(t) + d1[1] * rr * math.sin(t), zc)
                     for t in [math.pi / 2 * n_ / 6 for n_ in range(7)]]
                cc = "pvc_orange" if (w_ == ways - 1 and not hv) else "pvc_grey"
                for p_, q_ in zip(q, q[1:]):
                    rod(p_, q_, rc, cc, seg=8)
            stats["bends"] += 1
        # stub-ups at feeder ends beside equipment: 90 deg sweeps up to grade in a tight grid
        seen = set()
        for (x, y) in g["ends"]:
            P = (round(x, 2), round(y, 2))
            if P in seen or len(ends_at.get(P, [])) != 1:
                continue
            seen.add(P)
            near = [it for it in pads if it["fp"][0] - 6 <= x <= it["fp"][1] + 6 and it["fp"][2] - 6 <= y <= it["fp"][3] + 6]
            if not near:
                continue
            axis, c, k, sg = ends_at[P][0]
            a, b, ways, cols, rows, rc, pt = sect[(axis, c)][k]
            d = (sg, 0) if axis == "x" else (0, sg)
            Rs = 1.6
            for w_ in range(ways):
                col_i, row_i = w_ % cols, w_ // cols
                v = (col_i - (cols - 1) / 2) * pt
                zc = top - .25 - pt / 2 - row_i * pt
                bx, by = (x, y + v) if axis == "x" else (x + v, y)
                # sweep: horizontal -> vertical, the rows fanned along the run so they rise side by side
                off = row_i * pt
                q = [(bx - d[0] * (Rs + off) + d[0] * Rs * math.sin(t), by - d[1] * (Rs + off) + d[1] * Rs * math.sin(t),
                      zc + Rs * (1 - math.cos(t))) for t in [math.pi / 2 * n_ / 5 for n_ in range(6)]]
                cc = "pvc_orange" if (w_ == ways - 1 and not hv) else "pvc_grey"
                for p_, q_ in zip(q, q[1:]):
                    rod(p_, q_, rc, cc, seg=8)
                ex, ey, ez = q[-1]
                rod((ex, ey, ez), (ex, ey, .35), rc, cc, seg=8)
                rod((ex, ey, .25), (ex, ey, .5), rc + .06, "steel", seg=8)              # bell end / bushing
            stats["stubups"] += 1
    return stats


def chambers():
    """Precast chambers under the manhole and handhole covers placed by station.manholes()."""
    mh = find("Duct-bank manholes and handholes")
    covers = [p for p in fuel.G["parts"] if p["item"] == mh["id"] and p["kind"] == "box" and p["color"] == "concrete"]
    _item(UG, "Underground: duct-bank manhole and handhole chambers",
          "Precast concrete manholes 7 x 7 ft, 8 ft deep, with the duct banks entering through the walls and "
          "cable racks inside; handholes 3 x 3 ft, 3 ft deep (typical).")
    for p in covers:
        x0, y0, _ = p["min"]
        x1, y1, _ = p["max"]
        if x1 - x0 > 5:                                                   # manhole: walls, floor, roof slab
            for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + .5), (x0, x1, y1 - .5, y1), (x0, x0 + .5, y0, y1), (x1 - .5, x1, y0, y1)):
                box(a0, a1, b0, b1, -9, -1.2, "ductcase")                  # walls: cast section, see-through
            box(x0, x1, y0, y1, -9.3, -9, "concrete")                     # base slab
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            for (a0, a1, b0, b1) in ((x0, x1, y0, cy - 1.3), (x0, x1, cy + 1.3, y1), (x0, cx - 1.3, cy - 1.3, cy + 1.3),
                                     (cx + 1.3, x1, cy - 1.3, cy + 1.3)):
                box(a0, a1, b0, b1, -1.2, -.4, "ductcase")                 # roof slab with the access opening
            for k in range(2):                                            # cable racks on the side walls
                box(x0 + .5, x0 + .7, y0 + 1, y1 - 1, -7 + 2 * k, -6.85 + 2 * k, "steel")
                box(x1 - .7, x1 - .5, y0 + 1, y1 - 1, -7 + 2 * k, -6.85 + 2 * k, "steel")
            pass                                                          # (the cover sits on the roof opening)
        else:                                                             # handhole
            box(x0, x1, y0, y1, -3.2, -.05, "concrete")
    return len(covers)


def ground_grid(items):
    """Bare Cu mesh under the electrical, power-block and switchyard areas, rods and risers."""
    layers = ("BASE_ELECTRICAL", "BASE_SWITCHYARD", "BASE_POWER_BLOCK", "BASE_INLET_AIR")
    fps = [it["fp"] for it in items if it["layer"] in layers and it["z"][1] > .7
           and it["fp"][1] - it["fp"][0] < 1600 and it["fp"][3] - it["fp"][2] < 1200]
    sy = find("230 kV switchyard (gravel)")["fp"]
    _item(UG, "Underground: station ground grid (bare 4/0 Cu mesh, rods, risers)",
          "Bare 4/0 AWG copper at 18 in depth, exothermic joints; 40 ft mesh under the power block and electrical "
          "areas, 20 ft in the switchyard; 10 ft copper-clad rods at the perimeter; 4/0 risers to every "
          "transformer, e-house, structure and machine skid (typical, sized by the IEEE 80 study).",
          area="C")
    segs = set()

    def mark(x0, x1, y0, y1, s):
        for gx in range(int(math.floor(x0 / s)), int(math.ceil(x1 / s))):
            for gy in range(int(math.floor(y0 / s)), int(math.ceil(y1 / s))):
                a, b = gx * s, gy * s
                segs.update({((a, b), (a + s, b)), ((a, b + s), (a + s, b + s)), ((a, b), (a, b + s)),
                             ((a + s, b), (a + s, b + s))})
    for (x0, x1, y0, y1) in fps:
        if not (x0 >= sy[0] and x1 <= sy[1] and y0 >= sy[2] and y1 <= sy[3]):
            mark(max(x0 - 10, 2), min(x1 + 10, 2418), max(y0 - 10, 2), min(y1 + 10, 1918), 40)
    mark(sy[0], sy[1], sy[2], sy[3], 20)
    zg = -1.5
    runs = _merge(list(segs))
    for (axis, c), ivs in runs.items():
        for a, b in ivs:
            if axis == "x":
                rod((a, c, zg), (b, c, zg), .045, "copper", seg=5)
            else:
                rod((c, a, zg), (c, b, zg), .045, "copper", seg=5)
    # driven rods at the outer nodes (every other node on the outline), risers to equipment
    nodes = {}
    for (p, q) in segs:
        for v in (p, q):
            nodes[v] = nodes.get(v, 0) + 1
    outer = sorted(v for v, k in nodes.items() if k < 4)
    for i, (x, y) in enumerate(outer):
        if i % 2 == 0:
            rod((x, y, zg), (x, y, zg - 10), .05, "copper", seg=5)
    nris = 0
    for it in items:
        if it["layer"] not in ("BASE_ELECTRICAL", "BASE_SWITCHYARD") or it["z"][1] < 2 or it["z"][0] > 1:
            continue
        x0, x1, y0, y1 = it["fp"]
        if x1 - x0 > 400:
            continue
        for (x, y) in ((x0 - .4, y0 - .4), (x1 + .4, y1 + .4)):
            rod((x, y, zg), (x, y, .35), .05, "copper", seg=5)
            nris += 1
    return len(runs), nris


def firewater(routes):
    _item(UG, "Underground: firewater ring main (12 in ductile iron)",
          "Cement-lined ductile iron, 5 ft cover, sectionalised by post-indicator valves; hydrant and monitor "
          "laterals rise to the hydrants shown above grade (typical, NFPA 24).", area="E")
    n = 0
    for r in routes:
        if r["type"] != "firewater":
            continue
        _pipe_run([tuple(p) for p in r["points"]], -7.3, .55, "ductile", seg=12)
        for p in r["points"][1:-1]:
            box(p[0] - .9, p[0] + .9, p[1] - .9, p[1] + .9, -8.1, -6.5, "concrete")     # thrust block
        n += 1
    return n


def storm(items):
    """RCP storm sewer under each road edge, catch-basin chambers and laterals, trunk to the pond."""
    _item(UG, "Underground: storm drainage (reinforced-concrete pipe, catch basins, manholes)",
          "RCP 18-36 in under the road edges at about 0.5 % fall to the detention pond inlet headwall; catch basins "
          "with sumps and laterals; storm manholes at the junctions (typical).", area="F")
    roads = [it for it in items if it["layer"] == "SITE" and "road" in it["name"].lower()]
    n = 0
    for it in roads:
        x0, x1, y0, y1 = it["fp"]
        if (x1 - x0) >= (y1 - y0):
            ym = y0 + 1.5
            _pipe_run([(x0, ym, -9.5), (x1, ym, -9.5)], -9.5, .9, "rcp", seg=12)
            for x in range(int(x0) + 60, int(x1) - 30, 150):
                for y in (y0 + 1.5, y1 - 1.5):
                    box(x - 1.8, x + 1.8, y - 1.5, y + 1.5, -7, -.05, "concrete")        # catch-basin chamber
                    if y != ym:
                        _pipe_run([(x, y, -6.3), (x, ym, -9.1)], -6.3, .45, "rcp")                  # lateral across the road
                    n += 1
        else:
            xm = x0 + 1.5
            _pipe_run([(xm, y0, -9.5), (xm, y1, -9.5)], -9.5, .9, "rcp", seg=12)
            for y in range(int(y0) + 60, int(y1) - 30, 150):
                for x in (x0 + 1.5, x1 - 1.5):
                    box(x - 1.5, x + 1.5, y - 1.8, y + 1.8, -7, -.05, "concrete")
                    if x != xm:
                        _pipe_run([(x, y, -6.3), (xm, y, -9.1)], -6.3, .45, "rcp")
                    n += 1
    # storm manholes where the road drains meet
    for a in roads:
        for b in roads:
            if a is b:
                continue
            ax0, ax1, ay0, ay1 = a["fp"]
            bx0, bx1, by0, by1 = b["fp"]
            if (ax1 - ax0) >= (ay1 - ay0) and (bx1 - bx0) < (by1 - by0):
                x, y = bx0 + 1.5, ay0 + 1.5
                if ax0 <= x <= ax1 and by0 <= y <= by1:
                    rod((x, y, -11), (x, y, -.4), 2.5, "concrete", seg=16)
                    rod((x, y, -.4), (x, y, -.05), 1.3, "concrete", seg=16)
    # trunk from the west spine road drain to the pond inlet headwall (309, 1626-1640)
    _pipe_run([(371.5, 1660, -9.5), (309, 1660, -9.5), (309, 1641, -3)], -9.5, 1.4, "rcp", seg=14)
    rod((371.5, 1660, -11), (371.5, 1660, -.4), 2.5, "concrete", seg=16)
    return n


def oily_water():
    _item(UG, "Underground: oily-water drains (HDPE) to the oil-water separator",
          "Transformer containment sumps (GSU, UAT, station transformers) and the turbine-hall lube-oil area drains "
          "to the oil-water separator; separator effluent to the wastewater treatment (typical, SPCC).", area="E")
    zo, ro = -8.3, .35
    main = [(1456, 314), (1456, 1440), (1226, 1440), (1226, 1450)]
    _pipe_run([(600, 314)] + main, zo, .45, "hdpe")
    for cx, y in ((630, 325), (790, 325), (950, 325), (1051, 320), (667, 330), (827, 330), (987, 330)):
        _pipe_run([(cx, y + 6), (cx, 314)], zo, ro, "hdpe")                            # containment sump laterals
        box(cx - 1.5, cx + 1.5, y + 4.5, y + 7.5, -9, -.05, "concrete")                 # sump / valve pit
    _pipe_run([(596, 376), (1456, 376)], zo, ro, "hdpe")                              # hall drain header
    for k in range(3):                                                                 # lube-oil skid drains
        x = 668 + 160 * k
        _pipe_run([(x, 470), (x, 376)], zo, .25, "hdpe")
    _pipe_run([(1090, 470), (1090, 376)], zo, .25, "hdpe")                             # ST lube-oil / EHC area
    _pipe_run([(452, 805), (490, 805), (490, 892), (1456, 892)], zo, ro, "hdpe")       # station transformers
    _pipe_run([(1200, 1454), (745, 1454)], zo, ro, "hdpe")                            # OWS -> wastewater
    for p in ((1456, 314), (1456, 376), (1456, 892), (1456, 1440), (490, 892)):
        rod((p[0], p[1], -9.5), (p[0], p[1], -.4), 2, "concrete", seg=14)               # cleanout / inspection MH


def sanitary():
    _item(UG, "Underground: sanitary sewer (PVC SDR 35) and lift-station force main",
          "Gravity sewer from the buildings to a packaged duplex lift station, 3 in HDPE force main to the public "
          "sewer at the west boundary (typical).", area="F")
    zs = -7.8
    _pipe_run([(334, 318), (334, 650)], zs, .35, "pvc_green")
    for (x, y) in ((320, 370), (320, 515), (320, 620), (300, 318)):                   # building laterals
        _pipe_run([(x, y), (334, y)], zs + .5, .25, "pvc_green")
    for y in (370, 515, 620):
        rod((334, y, -9), (334, y, -.4), 2, "concrete", seg=14)                       # sewer manholes
    _pipe_run([(332, 664), (332, 668), (2, 668)], -6.3, .15, "hdpe")                 # force main
    lift = fuel.new_item("BASE_SERVICES", "LS-1: sanitary lift station (packaged duplex)", (326, 340, 652, 664), (0, 6),
                         tag="LS-1", area="F", basis="typical", sheet=SHEET,
                         info="Fibreglass wet well with two submersible grinder pumps, valve vault, control panel "
                              "with alarm beacon (typical).")
    rod((333, 658, -12), (333, 658, .5), 3.5, "concrete", seg=20)                    # wet well
    box(330.5, 335.5, 655.5, 660.5, .5, .7, "grating")
    box(326.5, 330, 660.5, 663.5, 0, 5.2, "panel")                                    # control panel
    rod((328.2, 662, 5.2), (328.2, 662, 6), .3, "red", seg=10)                        # alarm beacon
    lift["wiring"] = ["LV power 480 V: Cu XHHW-2, Type TC-ER in buried PVC conduit (pumps, panel)",
                      "Control 120 V: float switches, alarm to the DCS", "Grounding: bare Cu to the panel and wet well"]
    return lift


def water():
    _item(UG, "Underground: potable and service water mains (PVC C900)",
          "Potable water from the water treatment building to the buildings and safety showers; service water to "
          "the power block, HRSG area and hose stations (typical).", area="E")
    zw = -6.8
    _pipe_run([(440, 1490), (346, 1490), (346, 318)], zw, .3, "pvc_blue")             # potable main
    for (x, y) in ((320, 375), (320, 520), (320, 625), (300, 322)):
        _pipe_run([(x, y), (346, y)], zw, .18, "pvc_blue")
    _pipe_run([(560, 1445), (560, 942), (1100, 942)], zw, .35, "pvc_blue")           # service water main
    for x in (650, 810, 970):
        _pipe_run([(x, 942), (x, 880)], zw, .25, "pvc_blue")                          # to the HRSG areas
    for p in ((346, 1490), (560, 942), (346, 318)):
        box(p[0] - 1.2, p[0] + 1.2, p[1] - 1.2, p[1] + 1.2, -7.5, -.05, "concrete")     # valve boxes


def terminations(routes, items):
    """Ends of buried cable routes that meet no equipment: 230 kV cable termination structures where the
    cables rise into a switchyard bay, and a service-entrance handhole with a marker post where the site
    service duct bank meets the boundary."""
    pads = [it for it in items if it["layer"] != "SITE" and (it["fp"][1] - it["fp"][0]) < 1500]
    bur = [r for r in routes if r["type"] in BURIED and r["z"] < 0]
    out = []
    for r in bur:
        for k, p in ((0, r["points"][0]), (-1, r["points"][-1])):
            x, y = p
            if any(it["fp"][0] - 6 <= x <= it["fp"][1] + 6 and it["fp"][2] - 6 <= y <= it["fp"][3] + 6 for it in pads):
                continue
            if any(q is not r and any(min(a[0], b[0]) - 1 <= x <= max(a[0], b[0]) + 1 and min(a[1], b[1]) - 1 <= y <= max(a[1], b[1]) + 1
                                      for a, b in zip(q["points"], q["points"][1:])) for q in bur):
                continue
            nb = r["points"][1] if k == 0 else r["points"][-2]
            L = math.hypot(nb[0] - x, nb[1] - y) or 1
            ux, uy = (nb[0] - x) / L, (nb[1] - y) / L
            if r["type"] == "hv_cable":
                cx, cy = x + ux * 6, y + uy * 6                                   # clear of the bay gantry posts
                it = fuel.new_item(r["layer"], "230 kV cable termination structure (outdoor potheads, arresters)",
                                   (cx - 4, cx + 4, cy - 4, cy + 4), (0, 26), basis="typical", register=False,
                                   area="C", sheet=SHEET,
                                   info="The 230 kV XLPE cables rise from the cable bank up the structure to outdoor "
                                        "sealing ends (potheads), with surge arresters, and connect to the bay above.")
                box(cx - 4, cx + 4, cy - 4, cy + 4, 0, .6, "concrete")
                for (dx, dy) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
                    rod((cx + dx, cy + dy, .6), (cx + dx, cy + dy, 18), .35, "steel", seg=6)
                box(cx - 3.6, cx + 3.6, cy - 3.6, cy + 3.6, 17.6, 18.2, "steel")              # platform
                for ph in (-2.2, 0, 2.2):
                    px, py = cx + uy * ph, cy - ux * ph
                    rod((px, py, -1.5), (px, py, 18.2), .25, "cable_tc", seg=8)              # cable riser
                    rod((px, py, 18.2), (px, py, 24.5), .55, "insulator", r2=.3, seg=10)      # pothead
                    rod((px + ux * 1.2, py + uy * 1.2, 18.2), (px + ux * 1.2, py + uy * 1.2, 23), .35, "insulator", seg=8)
                out.append(("230 kV termination", r["layer"], (round(cx), round(cy))))
            else:
                fuel.new_item(r["layer"], "Service-entrance handhole and marker post (site boundary)",
                              (x - 2, x + 2, y - 2, y + 2), (0, 4), basis="typical", register=False, area="F", sheet=SHEET,
                              info="Telecom / utility service duct bank meets the provider's duct at the boundary "
                                   "(typical).")
                box(x - 2, x + 2, y - 2, y + 2, -4, .35, "concrete")
                rod((x + 1.6, y + 1.6, 0), (x + 1.6, y + 1.6, 4), .15, "hivis_o", seg=8)
                out.append(("boundary handhole", r["layer"], (x, y)))
    return out


def audit(routes, items, stats):
    """Underground coverage audit: every buried cable route drawn, every end terminated, crossings clear."""
    bur = [r for r in routes if r["type"] in BURIED and r["z"] < 0]
    keep = [it for it in items if it["layer"] not in ("SITE", "UNDERGROUND", "OPT_UNDERGROUND")
            and (it["fp"][1] - it["fp"][0]) < 1500]
    term = [it for it in items if it["name"].startswith(("230 kV cable termination", "Service-entrance handhole"))]
    loose = []
    for r in bur:
        for p in (r["points"][0], r["points"][-1]):
            x, y = p
            ok = any(it["fp"][0] - 8 <= x <= it["fp"][1] + 8 and it["fp"][2] - 8 <= y <= it["fp"][3] + 8 for it in keep + term)
            ok = ok or any(q is not r and any(min(a[0], b[0]) - 1 <= x <= max(a[0], b[0]) + 1 and min(a[1], b[1]) - 1 <= y <= max(a[1], b[1]) + 1
                                              for a, b in zip(q["points"], q["points"][1:])) for q in bur)
            if not ok:
                loose.append(f"{r['type']} {r['layer']} end {p}")
    zones = {}
    for r in bur:
        z = zones.setdefault(r["layer"], [0, 0])
        z[0] += 1
        z[1] += round(sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(r["points"], r["points"][1:])))
    return dict(zones=zones, routes=len(bur), length_ft=round(sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for r in bur
                                                        for a, b in zip(r["points"], r["points"][1:]))),
                loose_ends=loose, **stats)


def build(items, routes):
    BANKS.clear()
    nb = duct_banks(routes, items)
    nt = terminations(routes, items)
    nc = chambers()
    ng = ground_grid(items)
    nf = firewater(routes)
    ns = storm(items)
    oily_water()
    lift = sanitary()
    water()
    return dict(audit=audit(routes, fuel.G['items'], nb), terminations=nt, duct_bank_runs=nb, chambers=nc, grid_runs=ng[0], grid_risers=ng[1], firewater=nf, catch_basins=ns,
                lift=lift)
