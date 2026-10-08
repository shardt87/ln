"""Cable on the surface in the portable / bridge-power part of the modular yard.

Permanent modular plant (RICE, LM6000-class units, collector e-house, step-up transformers) keeps its
13.8 kV / 480 V feeders in buried duct banks. Temporary and bridge-power units are cabled on grade, the
way rental power is installed, and connect to the permanent network at the pad switchgear:
- portable pad (OPT_TMP): flexible portable power cable laid loose on the gravel. MV feeders are
  three-conductor Type SHD-GC (yellow jacket); 480 V links are single-conductor Type W sets (black) with
  colour-coded cam-lock plugs at the equipment. Every lane crossing goes through a drive-over cable
  protector (the C-L01 ramp of sheet 08 now carries the MOB-1 feeder);
- bridge-power units (OPT_MODX: CONT-3..8, the CONT paralleling e-house, TM-1/2): the same SHD-GC
  cable in open ground trays on timber sleepers, since the units stay for months.
Routes whose every point lies inside the pad area are re-tagged `surface` (z just above grade) so the
underground pass skips them and the renderers draw these parts instead of a strip.
Printed jacket legends at a few points along the runs.
"""
import fuel
from fuel import box, rod

REGION = (1985, 2350, 375, 715)
LANES = [(2130, 2370, 620, 640)]                       # portable pad lanes (cable protectors where crossed)
RAMP = (2238, 2252, 617, 643)                          # drive-over cable ramp (C-L01), already drawn
LV_TAGS = ("GEN-E", "GEN-O", "PAD-LV")                 # 480 V equipment (Type W sets)
LEGEND_SHD = "15 kV  3/C 2 AWG CU  TYPE SHD-GC  EPR  CPE JACKET  2/C GROUND + GC  PORTABLE POWER CABLE  -40C"
LEGEND_W = "2000 V  1/C 4/0 AWG CU  TYPE W  EPR  CPE JACKET  -50C  OIL RES"
SURF = []


def _inside(p, m=0):
    x0, x1, y0, y1 = REGION
    return x0 - m <= p[0] <= x1 + m and y0 - m <= p[1] <= y1 + m


def convert(routes):
    """Re-tag the pad-area cable routes as surface cable (after wiring, before the underground pass)."""
    n = 0
    for r in routes:
        if r["type"] not in ("mvlv_cable", "hv_cable") or r["layer"] not in ("OPT_TMP_ROUTES", "OPT_MODX_ROUTES"):
            continue
        if not all(_inside(p) for p in r["points"]):
            continue
        P = r["points"]
        if P == [[2213.0, 695.0], [2263.0, 695.0], [2263.0, 575.0]]:       # MOB-1 -> PIC through the C-L01 ramp
            r["points"] = P = [[2213.0, 695.0], [2245.0, 695.0], [2245.0, 575.0], [2255.0, 575.0]]
        if P == [[2060.0, 390.0], [2060.0, 410.0], [2165.0, 410.0], [2165.0, 470.0]]:   # TM-1: around PAD-LV
            P = [[2060.0, 390.0], [2060.0, 410.0], [2155.0, 410.0], [2155.0, 455.0], [2165.0, 455.0], [2165.0, 470.0]]
        r["points"] = P = _trim(P)
        tray = r["layer"] == "OPT_MODX_ROUTES"
        r.update(type="mvlv_cable", z=.3, w=1.5, h=.3, color="cable_mv", surface=True,
                 label="Bridge-power feeders: portable power cable in ground trays" if tray else
                 "Portable power cable on grade (temporary power)")
        SURF.append(r)
        n += 1
    return n


def _solids():
    return [it["fp"] for it in fuel.G["items"] if it["layer"] not in ("SITE",) and it["z"][1] > 2 and it["z"][0] < 1
            and (it["fp"][1] - it["fp"][0]) < 120 and (it["fp"][3] - it["fp"][2]) < 120
            and not it["name"].startswith(("Pipe", "Cable", "Underground", "Surface", "People", "Vehicles", "Equipment ID"))]


def _trim(P):
    """Move each end out of the equipment footprint it starts inside (or on the edge of, heading inward), so the
    run stops at the face instead of passing under the unit."""
    P = [list(p) for p in P]
    S = _solids()
    for rev in (False, True):
        Q = P[::-1] if rev else P
        a, b = Q[0], Q[1]
        for f in S:
            inside = lambda x, y, m=0: f[0] - m <= x <= f[1] + m and f[2] - m <= y <= f[3] + m
            if not inside(a[0], a[1], .01):
                continue
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if not inside(a[0] + (b[0] - a[0]) * .01, a[1] + (b[1] - a[1]) * .01, -.001) and not inside(mx, my):
                continue                                          # on the edge, heading away: fine
            if a[1] == b[1]:
                a[0] = f[1] if b[0] > a[0] else f[0]
            else:
                a[1] = f[3] if b[1] > a[1] else f[2]
            if (a[0] - b[0]) * (Q[0][0] - b[0]) < 0 or (a[1] - b[1]) * (Q[0][1] - b[1]) < 0:
                pass
            break
        P = Q[::-1] if rev else Q
    return P


def _offset(P, d):
    """Axis-aligned polyline offset sideways by d (left of travel)."""
    out = []
    for k, p in enumerate(P):
        nx = ny = 0.0
        for a, b in ((P[k - 1], p) if k else (None, None), (p, P[k + 1]) if k + 1 < len(P) else (None, None)):
            if a is None:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = abs(dx) + abs(dy) or 1
            # left normal of an axis-aligned segment
            if dx:
                ny = (1 if dx > 0 else -1) * d
            else:
                nx = (-1 if dy > 0 else 1) * d
        out.append((p[0] + nx, p[1] + ny))
    return out


def _crosses(u0, u1, c, horiz, P, m=.9):
    """Does a sleeper spanning u0..u1 along a tray at cross-coordinate c sit on a loose cable run P?"""
    for a, b in zip(P, P[1:]):
        if horiz:          # tray along x: sleeper occupies x u0..u1, y c +- .9
            if a[0] == b[0] and u0 - m <= a[0] <= u1 + m and min(a[1], b[1]) - 1 <= c <= max(a[1], b[1]) + 1:
                return True
        else:
            if a[1] == b[1] and u0 - m <= a[1] <= u1 + m and min(a[0], b[0]) - 1 <= c <= max(a[0], b[0]) + 1:
                return True
    return False


def ramp():
    """Rebuild the C-L01 drive-over ramp as a modular cable protector: black base with sloped edges, yellow
    hinged lids in 3 ft modules over the cable channels."""
    it = fuel.find("Drive-over cable ramp")
    x0, x1, y0, y1 = it["fp"]
    fuel.strip(it)
    xm = (x0 + x1) / 2
    box(x0 + 2.6, x1 - 2.6, y0, y1, 0, .35, "hdpe")
    for s in (-1, 1):                                                       # sloped edge ramps, stepped
        xe = x0 if s < 0 else x1
        for k, (w, h) in enumerate(((2.6, .12), (1.8, .24), (1.0, .35))):
            box(xe, xe - s * w, y0, y1, 0, h, "hdpe") if s < 0 else box(xe - w, xe, y0, y1, 0, h, "hdpe")
    y = y0
    while y < y1 - .1:
        y2 = min(y + 3, y1)
        box(xm - 3.2, xm + 3.2, y + .04, y2 - .04, .35, .62, "amber")       # lid
        for xs in (xm - 1.1, xm + 1.1):
            box(xs - .05, xs + .05, y + .04, y2 - .04, .62, .64, "hdpe")     # hinge lines
        y = y2


def _in_lane(x, y):
    return any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, x1, y0, y1) in LANES)


def _lv(r, items):
    """A route is 480 V when it ends at a 480 V item."""
    for p in (r["points"][0], r["points"][-1]):
        for it in items:
            f = it["fp"]
            if it.get("tag") in LV_TAGS and f[0] - 3 <= p[0] <= f[1] + 3 and f[2] - 3 <= p[1] <= f[3] + 3:
                return True
    return False


def build():
    items = fuel.G["items"]
    ramp()
    if not SURF:
        return 0
    xs = [p[0] for r in SURF for p in r["points"]]
    ys = [p[1] for r in SURF for p in r["points"]]
    it = fuel.new_item("OPT_TMP", "Surface cables: portable power cable on grade and in ground trays",
                       (min(xs) - 2, max(xs) + 2, min(ys) - 2, max(ys) + 2), (0, 1.2), area="I", register=False,
                       basis="typical", sheet="typical (portable pad)",
                       info="Temporary and bridge power cabled on grade, as rental power is installed: 15 kV Type "
                            "SHD-GC portable power cable (yellow) for the MV feeders, 2000 V Type W single conductors "
                            "with cam-lock plugs for the 480 V links, drive-over cable protectors at the lane "
                            "crossings, open ground trays on sleepers for the bridge-power units. The permanent "
                            "modular plant keeps its buried duct banks.")
    import cable_install
    n_leg = 0
    loose = [r["points"] for r in SURF if r["layer"] != "OPT_MODX_ROUTES"]
    for ri, r in enumerate(SURF):
        tray = r["layer"] == "OPT_MODX_ROUTES"
        lay = "OPT_MODX" if tray else "OPT_TMP"
        lv = _lv(r, items)
        P = [tuple(p) for p in r["points"]]
        # cables: MV = two SHD-GC (r 0.11 ft), LV = two Type W sets of four (r 0.07 ft)
        if lv:
            offs, rc, col = [-.55 + .157 * k for k in range(8)], .07, "cable_mc"
        else:
            offs, rc, col = (-.14, .14), .11, "cable_shd"
        zg = .42 if tray else 0.0                                       # tray floor / gravel
        if tray:                                                       # open ground tray on sleepers
            T = [list(p) for p in P]
            for (i, j) in ((0, 1), (-1, -2)):                            # stop 1.2 ft short of the equipment faces
                for k in (0, 1):
                    if T[i][k] != T[j][k]:
                        T[i][k] += 1.2 * (1 if T[j][k] > T[i][k] else -1)
            for a, b in zip(T, T[1:]):
                horiz = a[1] == b[1]
                lo, hi = sorted((a[0], b[0])) if horiz else sorted((a[1], b[1]))
                c = a[1] if horiz else a[0]
                bx = lambda u0, u1, v0, v1, z0, z1, cc: box(u0, u1, v0, v1, z0, z1, cc, layer=lay) if horiz else \
                    box(v0, v1, u0, u1, z0, z1, cc, layer=lay)
                bx(lo - .6, hi + .6, c - .6, c + .6, .35, .42, "steel")
                for s in (-1, 1):
                    bx(lo - .6, hi + .6, c + s * .6 - .05, c + s * .6 + .05, .35, .72, "steel")
                u = lo + 2
                while u < hi - 1:                                        # sleepers, clear of loose cables below
                    if not any(_crosses(u, u + .5, c, horiz, q) for q in loose):
                        bx(u, u + .5, c - .9, c + .9, 0, .35, "timber")
                    u += 6
        for o in offs:
            Q = _offset(P, o)
            for (ax, ay), (bx_, by) in zip(Q, Q[1:]):
                # lift over a lane: the cable rides through a protector
                rod((ax, ay, zg + rc), (bx_, by, zg + rc), rc, col, seg=8, layer=lay)
        # cable protectors where a loose run crosses a pad lane (the C-L01 ramp already covers its crossing)
        if not tray:
            for a, b in zip(P, P[1:]):
                horiz = a[1] == b[1]
                if horiz:
                    continue
                for (x0, x1, y0, y1) in LANES:
                    if not (x0 <= a[0] <= x1) or RAMP[0] <= a[0] <= RAMP[1]:
                        continue
                    lo, hi = sorted((a[1], b[1]))
                    if hi < y0 or lo > y1:
                        continue
                    ya, yb = max(lo, y0 - 1.5), min(hi, y1 + 1.5)
                    yy = ya
                    while yy < yb - .1:                                   # 3 ft interlocking modules
                        y2 = min(yy + 3, yb)
                        box(a[0] - 1.5, a[0] + 1.5, yy + .03, y2 - .03, .45, .85, "amber", layer=lay)
                        for s in (-1, 1):                                 # sloped wings (stepped)
                            box(a[0] + s * 1.5, a[0] + s * 2.4, yy + .03, y2 - .03, .45, .62, "amber", layer=lay)
                        yy = y2
        # ends: MV cables rise into a gland plate; LV sets end in cam-lock plugs (black, red, blue, white + green)
        for p, q in ((P[0], P[1]), (P[-1], P[-2])):
            dx, dy = (p[0] - q[0], p[1] - q[1])
            L = abs(dx) + abs(dy) or 1
            ux, uy = dx / L, dy / L
            p = (p[0] - ux * 1.2, p[1] - uy * 1.2)                        # stand-off from the equipment face
            for k, o in enumerate(offs):
                ex, ey = p[0] - uy * o, p[1] + ux * o
                if lv:
                    cl = ("cable_mc", "camlock_r", "camlock_b", "camlock_w", "cable_mc", "camlock_r", "camlock_b",
                          "camlock_g")[k]
                    rod((ex, ey, zg + rc), (ex + ux * .6, ey + uy * .6, zg + rc), .1, cl, seg=8, layer=lay)
                else:
                    rod((ex, ey, zg + rc), (ex + ux * .4, ey + uy * .4, zg + 1.6), rc, col, seg=8, layer=lay)
            if not lv:
                box(p[0] + ux * .3 - .5 - abs(uy) * .3, p[0] + ux * .3 + .5 + abs(uy) * .3,
                    p[1] + uy * .3 - .5 - abs(ux) * .3, p[1] + uy * .3 + .5 + abs(ux) * .3, 1.5, 2.3, "steel_dark", layer=lay)
        # printed legend on the longest straight run of each route (top of the first cable)
        a, b = max(zip(P, P[1:]), key=lambda s: abs(s[1][0] - s[0][0]) + abs(s[1][1] - s[0][1]))
        L = abs(b[0] - a[0]) + abs(b[1] - a[1])
        if L > 14:
            Q = _offset([a, b], offs[0])
            ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            c = ((Q[0][0] + Q[1][0]) / 2, (Q[0][1] + Q[1][1]) / 2, zg + 2 * rc + .005)
            cable_install.legend(c, (0, 0, 1), (ux, uy, 0), min(9, L - 4), LEGEND_W if lv else LEGEND_SHD)
            n_leg += 1
    return len(SURF), n_leg
