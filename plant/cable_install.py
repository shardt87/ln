"""Installed cable at the point of use, modelled the way it is built (typical, not engineered).

hv_termination(): a 230 kV outdoor cable termination structure. The three single-core XLPE cables (Southwire
230 kV, the requested supplier) come up out of the duct bank through steel cable guards, are cleated to support
beams every 3 ft, pass through the platform into the outdoor sealing ends (stress-cone body, shedded composite
insulator, top terminal). Surge arresters stand behind the sealing ends, jumpered to the top terminals; the
sheath-bonding leads run from the sealing-end bases to a link box on the front column, with a copper lead to the
ground grid. The cable jacket carries its printed legend.
"""
import math

import fuel
from fuel import box, rod

LEGEND_HV = "230 kV  1/C 2500 KCMIL CU  XLPE  CU WIRE SHIELD  AL LAMINATE  HDPE JACKET  ICEA S-108-720"
BRAND = "SOUTHWIRE"


def legend(c, n, along, length, text, r=.0, h=.13):
    """Printed jacket legend: a narrow strip on the cable surface, text running along the cable."""
    import showcase
    up = (n[1] * along[2] - n[2] * along[1], n[2] * along[0] - n[0] * along[2], n[0] * along[1] - n[1] * along[0])
    # text runs along `along`: decal right = up x n must equal `along`, so up = n x along
    showcase.decal(c, n, length, h, [(BRAND + "  " + text, .78, 1, "#e9e9e6", 1)], bg=None, up=up)
    showcase.decal(c, n, length, h, [(text, .78, 1, "#e9e9e6")], bg=None, up=up, generic_only=True)


def hv_termination(cx, cy, fx, fy, top=None):
    """Termination structure centred on (cx, cy); (fx, fy) points to the front, where the cables come up.
    top: optional callback(k, terminal_xyz) for the onward connection of each phase."""
    vx, vy = fy, -fx                                          # across the structure (phase spacing)
    P = lambda u, v, z: (cx + fx * u + vx * v, cy + fy * u + vy * v, z)

    def bx(u0, u1, v0, v1, z0, z1, c):
        a, b = P(u0, v0, 0), P(u1, v1, 0)
        box(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1]), z0, z1, c)

    ZP = 16.0                                                 # platform top
    bx(-4, 4, -4.4, 4.4, 0, .6, "concrete")                   # foundation
    cols = [(1.6, -3.4), (1.6, 3.4), (-3.2, -3.4), (-3.2, 3.4)]
    for (u, v) in cols:
        bx(u - .25, u + .25, v - .25, v + .25, .6, ZP - .5, "steel")              # W8 columns
        bx(u - .5, u + .5, v - .5, v + .5, .6, .75, "steel")                      # base plates
    for (ua, va), (ub, vb) in (((-3.2, -3.4), (-3.2, 3.4)), ((-3.2, -3.4), (1.6, -3.4)), ((-3.2, 3.4), (1.6, 3.4))):
        for (z0, z1) in ((1.5, 8), (8, 14.5)):                                    # X-bracing, back and sides
            rod(P(ua, va, z0), P(ub, vb, z1), .1, "steel", seg=6)
            rod(P(ua, va, z1), P(ub, vb, z0), .1, "steel", seg=6)
    bx(-3.6, 2.4, -3.8, 3.8, ZP - .5, ZP, "steel")                                # platform beams
    bx(-3.5, 2.3, -3.7, 3.7, ZP, ZP + .12, "grating")
    UC = 2.0                                                  # cable line, in front of the cleat beams
    for z in (3.5, 6.5, 9.5, 12.5):                           # cleat beams between the front columns
        bx(1.4, 1.75, -3.4, 3.4, z - .2, z + .2, "steel")
    for k, v in enumerate((-2.3, 0, 2.3)):
        # out of the duct, through the cable guard, cleated up to the platform
        rod(P(UC, v, -3.0), P(UC, v, ZP - .7), .2, "cable", seg=14)
        rod(P(UC, v, .6), P(UC, v, 8), .3, "pipe", seg=14)                         # steel cable guard
        bx(UC - .4, UC + .4, v - .4, v + .4, .6, .9, "concrete")                  # duct mouth, sealed
        for z in (3.5, 6.5, 9.5, 12.5):
            if z > 8:
                bx(UC - .28, UC + .28, v - .3, v + .3, z - .17, z + .17, "alu")    # trefoil / single cleat
            bx(1.75, UC - .2, v - .08, v + .08, z - .1, z + .1, "alu")            # cleat bolt bracket
        rod(P(UC, v, ZP - .8), P(UC, v, ZP), .3, "alu", seg=12)                   # entry gland under the platform
        # sealing end: base plate, stress-cone body, shedded insulator, top terminal
        bx(UC - .55, UC + .55, v - .55, v + .55, ZP + .12, ZP + .4, "alu")
        rod(P(UC, v, ZP + .4), P(UC, v, ZP + 1.8), .4, "alu", r2=.33, seg=16)
        rod(P(UC, v, ZP + 1.8), P(UC, v, ZP + 9.2), .26, "insulator", r2=.2, seg=12)
        for j in range(15):
            z = ZP + 2.1 + j * .48
            rod(P(UC, v, z), P(UC, v, z + .07), .62 - .012 * j, "insulator", seg=16)
        rod(P(UC, v, ZP + 9.2), P(UC, v, ZP + 9.6), .34, "alu", seg=12)
        rod(P(UC, v, ZP + 9.6), P(UC, v, ZP + 10.4), .12, "alu", seg=8)           # terminal stalk
        term = P(UC, v, ZP + 10.4)
        # surge arrester behind, on its pedestal, jumpered to the top terminal; ground lead down the back column
        UA = -1.6
        bx(UA - .45, UA + .45, v - .45, v + .45, ZP + .12, ZP + .6, "steel")
        rod(P(UA, v, ZP + .6), P(UA, v, ZP + 6.6), .24, "pvc_grey", seg=12)
        for j in range(10):
            z = ZP + .9 + j * .55
            rod(P(UA, v, z), P(UA, v, z + .06), .48, "pvc_grey", seg=14)
        rod(P(UA, v, ZP + 6.6), P(UA, v, ZP + 6.9), .3, "alu", seg=10)
        a, c = term, P(UA, v, ZP + 6.9)
        mid = tuple((a[i] + c[i]) / 2 for i in range(3))
        pts = [tuple((1 - s) ** 2 * a[i] + 2 * (1 - s) * s * (mid[i] + (1.4 if i == 2 else 0)) + s * s * c[i]
                     for i in range(3)) for s in [q / 6 for q in range(7)]]
        for p0, p1 in zip(pts, pts[1:]):
            rod(p0, p1, .07, "conductor", seg=6)
        rod(P(UA, v, ZP + .3), P(UA - .1, v, ZP - .5), .05, "copper", seg=6)
        # sheath-bonding lead: sealing-end base -> along under the platform -> down the front column to the link box
        vb = 3.78 + .14 * k
        lead = [P(UC, v, ZP + .25), P(UC + .45, v, ZP - .3), P(UC + .45, vb, ZP - .3), P(2.0, vb, ZP - .9),
                P(2.0, vb, 6.3)]
        for p0, p1 in zip(lead, lead[1:]):
            rod(p0, p1, .06, "cable", seg=6)
        if top:
            top(k, term)
        legend(P(UC + .205, v, 11.6), (fx, fy, 0), (0, 0, 1), 5.2, LEGEND_HV)
    # link box on the front column with its ground lead to the grid; arrester surge counter
    bx(1.1, 2.15, 3.65, 4.3, 4.3, 6.3, "alu")
    rod(P(1.6, 3.95, 4.3), P(1.6, 3.95, .6), .06, "copper", seg=6)
    bx(-3.2 - .55, -3.2 - .25, 2.9, 3.6, 5.5, 6.4, "cabinet")
    return P




def _bez(p0, p1, p2, n=8):
    return [tuple((1 - t) ** 2 * p0[k] + 2 * (1 - t) * t * p1[k] + t * t * p2[k] for k in range(3))
            for t in [i / n for i in range(n + 1)]]


def _poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def ehouse_bottom_entry(prefix):
    """An e-house drawn on a solid plinth becomes the usual pier-and-skid installation, and the cables come up
    out of the duct-bank stub-ups at its face, under the skid beam and into gland plates under the floor
    (bottom-entry switchgear): MV triplex from the grey conduits, fibre from the orange ones."""
    G = fuel.G
    it = next(i for i in G["items"] if i["name"].startswith(prefix))
    x0, x1, y0, y1 = it["fp"]
    plinth = [p for p in G["parts"] if p["item"] == it["id"] and p["kind"] == "box" and p["color"] == "concrete"
              and p["min"][2] <= 0 and p["max"][2] >= 2 and p["max"][0] - p["min"][0] > (x1 - x0) * .9]
    if not plinth:
        return 0
    zf = plinth[0]["max"][2]                                   # underside of the e-house floor
    for p in plinth:
        G["parts"].remove(p)
    cur = G["cur"]
    G["cur"] = it
    zb = zf - .6                                               # skid base depth
    mh = [i["id"] for i in G["items"] if i["name"].startswith(("Underground: MV / LV duct banks", "Underground: duct banks"))]
    stub_x = [p["a"][0] for p in G["parts"] if p["item"] in mh and p["kind"] == "rod" and p["color"] == "steel"
              and abs(p["a"][0] - p["b"][0]) < .01 and .3 < p["b"][2] < .7 and x0 - .5 <= p["a"][0] <= x1 + .5
              and y0 - 2 <= p["a"][1] <= y1 + 2]
    nx = max(2, round((x1 - x0) / 10))
    xs = [x0 + 1 + k * (x1 - x0 - 2) / nx for k in range(nx + 1)]
    for x in xs:                                               # piers and cross beams, clear of the cable entries
        while any(abs(x - sx) < 3 for sx in stub_x):
            x += 1.5 if x < (x0 + x1) / 2 else -1.5
        for y in (y0 + 1, (y0 + y1) / 2, y1 - 1):
            box(x - 1, x + 1, y - 1, y + 1, 0, zb, "concrete")
        box(x - .25, x + .25, y0, y1, zb, zf, "steel")
    for y in (y0, y1 - .5):                                    # perimeter skid beams (W-shape)
        box(x0, x1, y, y + .5, zb, zf, "steel")
    for x in (x0, x1 - .5):
        box(x, x + .5, y0, y1, zb, zf, "steel")
    # cables out of the stub-ups at the faces
    ends = [p for p in G["parts"] if p["item"] in mh and p["kind"] == "rod" and p["color"] == "steel"
            and abs(p["a"][0] - p["b"][0]) < .01 and abs(p["a"][1] - p["b"][1]) < .01 and .3 < p["b"][2] < .7
            and x0 - .5 <= p["a"][0] <= x1 + .5 and y0 - 2 <= p["a"][1] <= y1 + 2]
    cond = {}
    for p in G["parts"]:                                      # colour of the conduit under each coupling
        if p["item"] in mh and p["kind"] == "rod" and p["color"] in ("pvc_grey", "pvc_orange") and abs(p["b"][2] - .35) < .02:
            cond[(round(p["b"][0], 2), round(p["b"][1], 2))] = p["color"]
    plates = {}
    n = 0
    for e in ends:
        x, y = e["a"][0], e["a"][1]
        if y0 + 1 < y < y1 - 1:
            continue
        yi = y - 1.9 if y > (y0 + y1) / 2 else y + 1.9             # under the floor, inside the skid beam
        col = cond.get((round(x, 2), round(y, 2)), "pvc_grey")
        if col == "pvc_orange":
            path = _bez((x, y, .5), (x, y, zb - .35), (x, yi, zb - .35), 10) + [(x, yi, zf - .2)]
            _poly(path, .05, "cable_fo", seg=10)
        else:
            for j, (ox, oz) in enumerate(((-.07, 0), (.07, 0), (0, .12))):         # triplexed 1/C MV-105
                path = (_bez((x + ox, y, .5 + oz), (x + ox, y, zb - .4 + oz), (x + ox, yi, zb - .4 + oz), 10)
                        + [(x + ox, yi, zf - .2)])
                _poly(path, .065, "cable_mv", seg=10)
            rod((x, y, .38), (x, y, .62), .3, "pvc_grey", seg=12)                    # end bell / duct seal
        plates.setdefault((round(x), yi > (y0 + y1) / 2), []).append((x, yi))
        n += 1
    for (_, _), pts in plates.items():                        # gland plate under the switchgear section
        xs_ = [p[0] for p in pts]
        yi = pts[0][1]
        box(min(xs_) - .6, max(xs_) + .6, yi - .5, yi + .5, zf - .25, zf, "alu")
    G["cur"] = cur
    return n
