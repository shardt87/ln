"""Modular power yard at LOD 3 (SK-3X1-07 / -08 and the OPT_MODX design change): the
smaller generating units, their switchgear and the skids around them.

Every item keeps its drawn footprint; the single boxes become typical equipment:
- containerized and enclosed gas gensets: ISO-style enclosure with corrugation ribs and corner
  castings, end doors, side intake louvres, roof radiator with two fans, roof silencer and stack;
- trailer units (MOB-1 trailer genset, load bank, TM2500-class turbines): chassis, axle sets,
  landing legs, gooseneck, stairs and walkways;
- fuel cells (Bloom ES5 class): power-module cabinets with seams, roof exhaust vents, doors;
- microturbines (Capstone C1000 class): enclosure with roof intake hoods and exhaust outlets;
- open engine skid, black-start gensets, BESS black-start alternative, SC inlet chillers,
  water-injection skid and aqueous-ammonia tank.

Uses the primitives in fuel.py; runs after modular.py.
"""
import fuel
from fuel import box, rod, pipe, find, strip, on


def dress(flag):
    fuel.D = flag


def items(prefix):
    return [it for it in fuel.G["items"] if it["name"].startswith(prefix)]


def wheels(axis_x, x, y0, y1, r=1.6):
    """One axle (dual tyres both sides) across a trailer that runs along x (axis_x) or y."""
    if axis_x:
        for y in (y0 - .2, y1 + .2):
            rod((x, y - .6, r), (x, y + .6, r), r, "fanhub", seg=14)
    else:
        for xx in (x[0] - .2, x[1] + .2):
            rod((xx - .6, y0, r), (xx + .6, y0, r), r, "fanhub", seg=14)


def ribs(x0, x1, y0, y1, z0, z1, along_x, pitch=1.2):
    """Corrugation ribs on the two long faces (dressing)."""
    if along_x:
        x = x0 + .6
        while x < x1 - .5:
            for y, s in ((y0, -1), (y1, 1)):
                box(x - .18, x + .18, y, y + s * .1, z0 + .3, z1 - .3, "steel")
            x += pitch
    else:
        y = y0 + .6
        while y < y1 - .5:
            for x, s in ((x0, -1), (x1, 1)):
                box(x, x + s * .1, y - .18, y + .18, z0 + .3, z1 - .3, "steel")
            y += pitch


def genset_enclosure(it, h, color="cabinet", stack_top=None, rib=True, fans=2):
    """Enclosure on sleepers with corner castings, end doors, intake louvres, roof radiator
    fans at one end and a roof silencer + stack at the other. Returns the new top."""
    x0, x1, y0, y1 = it["fp"]
    ax = (x1 - x0) >= (y1 - y0)
    L = (x1 - x0) if ax else (y1 - y0)
    W = (y1 - y0) if ax else (x1 - x0)
    strip(it)
    for t in (.06, .94):                                         # sleepers
        if ax:
            box(x0 + L * t - .8, x0 + L * t + .8, y0, y1, 0, .5, "concrete")
        else:
            box(x0, x1, y0 + L * t - .8, y0 + L * t + .8, 0, .5, "concrete")
    box(x0, x1, y0, y1, .5, h, color)
    top = h

    def P(u, v):                       # (along, across) -> (x, y)
        return (x0 + u, y0 + v) if ax else (x0 + v, y0 + u)

    def B2(u0, u1, v0, v1, z0, z1, c):
        (a, b), (c2, d) = P(u0, v0), P(u1, v1)
        box(a, c2, b, d, z0, z1, c)

    # roof radiator with fans over the first third, silencer and stack at the far end
    B2(1, L * .38, .4, W - .4, h, h + .9, "radiator")
    for k in range(fans):
        u = 1 + (L * .38 - 1) * (k + .5) / fans
        cx, cy = P(u, W / 2)
        rod((cx, cy, h + .9), (cx, cy, h + 1.3), min(W / 2 - .7, (L * .38 - 1) / fans / 2 - .2), "fan", seg=16)
    su0, su1 = L * .55, L * .9
    for u in (su0 + 1, su1 - 1):
        B2(u - .3, u + .3, W / 2 - 1, W / 2 + 1, h, h + .8, "steel")
    a, b = P(su0, W / 2), P(su1, W / 2)
    rod((a[0], a[1], h + 1.7), (b[0], b[1], h + 1.7), min(1.3, W / 4), "duct", seg=16)
    sx, sy = P(su1 - .8, W / 2)
    st = stack_top or (h + 4)
    rod((sx, sy, h + 1.7), (sx, sy, st), .55, "stack", seg=12)
    top = max(top, st)
    dress(True)
    for (u, v) in ((0, 0), (L, 0), (0, W), (L, W)):                  # corner castings
        cx, cy = P(min(max(u, .3), L - .3), min(max(v, .3), W - .3))
        for z in (.5, h - .6):
            box(cx - .35, cx + .35, cy - .35, cy + .35, z, z + .6, "steel")
    if rib:
        ribs(x0, x1, y0, y1, .5, h, ax)
    # end doors (far end) and intake louvres on the long faces at the radiator end
    if ax:
        box(x1, x1 + .12, y0 + .5, y0 + W / 2 - .1, 1, h - .8, "door")
        box(x1, x1 + .12, y0 + W / 2 + .1, y1 - .5, 1, h - .8, "door")
        for y, s in ((y0, -1), (y1, 1)):
            box(x0 + 2, x0 + L * .3, y + s * .1, y + s * .3, 2, h - 2, "louvre")
            box(x0 + L * .6, x0 + L * .6 + 3, y + s * .1, y + s * .25, 1, 7.5, "door")
    else:
        box(x0 + .5, x0 + W / 2 - .1, y1, y1 + .12, 1, h - .8, "door")
        box(x0 + W / 2 + .1, x1 - .5, y1, y1 + .12, 1, h - .8, "door")
        for x, s in ((x0, -1), (x1, 1)):
            box(x + s * .1, x + s * .3, y0 + 2, y0 + L * .3, 2, h - 2, "louvre")
    dress(False)
    it["z"] = [0, round(top, 2)]
    return top


def trailer(it, x0, x1, y0, y1, deck, axles_at, legs_at, color="cabinet", body=None):
    """Trailer along x: chassis at `deck`, axle sets, landing legs, body box (x0..x1)."""
    box(x0, x1, y0 + .6, y1 - .6, deck - 1, deck, "steel")
    for xa in axles_at:
        wheels(True, xa, y0 + .8, y1 - .8)
    for xl in legs_at:
        for y in (y0 + 1.2, y1 - 1.2):
            box(xl - .25, xl + .25, y - .25, y + .25, 0, deck - 1, "steel")
            box(xl - .6, xl + .6, y - .6, y + .6, 0, .25, "steel")
    if body:
        box(*body, color)


# ---------------------------------------------------------------------------------------
def containers():
    for it in items("CONT-") + items("GEN-E:"):
        if it["name"].startswith("CONT paralleling") or "e-house" in it["name"]:
            continue
        h = 9.5 if it["name"].startswith("CONT") else 11
        it["info"] = (it.get("info") or "") + " Enclosure with roof radiator, silencer and stack (typical)."
        genset_enclosure(it, h, "cabinet", stack_top=h + 6 if h > 10 else None)
    for it in items("Black-start genset"):
        genset_enclosure(it, 12, "ehouse", stack_top=16, fans=3)
    # open engine-generator skid
    it = find("GEN-O:")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .6, "concrete")
    box(x0 + .5, x1 - .5, y0 + .5, y1 - .5, .6, 1.4, "steel")
    box(x0 + 1, x0 + 5, y0 + .6, y1 - .6, 1.4, 7.8, "bundle")              # radiator
    rod((x0 + 5.3, (y0 + y1) / 2, 4.6), (x0 + 6, (y0 + y1) / 2, 4.6), 3, "fan", seg=18)
    box(x0 + 7, x0 + 16, y0 + 1.5, y1 - 1.5, 1.4, 6.5, "machine")            # engine
    box(x0 + 7.5, x0 + 15.5, y0 + 2, y1 - 2, 6.5, 7.6, "motor")              # rocker covers
    rod((x0 + 16, (y0 + y1) / 2, 4), (x0 + 23.5, (y0 + y1) / 2, 4), 2.6, "machine", seg=20)   # generator
    box(x0 + 22, x0 + 25, y0 + .6, y0 + 2.6, 1.4, 6.5, "panel")
    rod((x0 + 12, y1 - 1.5, 6), (x0 + 12, y1 - 1.5, 8), .4, "stack", seg=8)


def trailers():
    # MOB-1 trailer genset
    it = find("MOB-1:")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    trailer(it, x0, x1, y0, y1, 4, (x1 - 10, x1 - 6.5, x1 - 3), (x0 + 8,), "cabinet",
            body=(x0 + 1, x1 - .5, y0 + .3, y1 - .3, 4, 12.4))
    box(x0, x0 + 4, y0 + 2, y1 - 2, 3, 4, "steel")                          # gooseneck / kingpin plate
    box(x0 + 3, x0 + 18, y0 + .5, y1 - .5, 12.4, 13.1, "radiator")
    for xf in (x0 + 7, x0 + 14):
        rod((xf, (y0 + y1) / 2, 13.1), (xf, (y0 + y1) / 2, 13.5), 3.2, "fan", seg=16)
    rod((x1 - 6, (y0 + y1) / 2, 12.4), (x1 - 6, (y0 + y1) / 2, 13.5), .5, "stack", seg=8)
    dress(True)
    ribs(x0 + 1, x1 - .5, y0 + .3, y1 - .3, 4, 12.4, True, pitch=1.6)
    for s in range(4):                                                       # access stair
        box(x0 + 26, x0 + 29, y0 - 1.2 - s * .9 + 0, y0 - .3 - s * .9, .6 + s * .9, .8 + s * .9, "grating")
    dress(False)
    # load bank trailer
    it = find("LB:")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    trailer(it, x0, x1, y0, y1, 3.5, (x1 - 5, x1 - 2),
            (x0 + 4,), "cabinet", body=(x0 + 2, x1 - .5, y0 + .3, y1 - .3, 3.5, 10.5))
    for xf in (x0 + 7, x0 + 14, x0 + 21):
        box(xf - 3, xf + 3, y0 + 1, y1 - 1, 10.5, 11.3, "louvre")
        rod((xf, (y0 + y1) / 2, 11.3), (xf, (y0 + y1) / 2, 11.7), 2.6, "fan", seg=16)
    box(x0, x0 + 2, y0 + 2, y1 - 2, 2.6, 3.5, "steel")
    for it in items("TM-"):
        tm2500(it)


LEGEND_GEN = "15 kV  1/C 1000 KCMIL CU  MV-105  EPR 133%  1/3 CN  PVC JACKET  UL 1072  SUN RES  DIRECT BURIAL"


def axle(x, y0, y1, r=1.65):
    """One trailer axle across y0..y1: dual tyres each side, hubs, axle beam, fender."""
    for ya, s in ((y0, 1), (y1, -1)):
        for k in (0, 1):
            yt = ya + s * (.15 + k * 1.0)
            rod((x, yt, r), (x, yt + s * .85, r), r, "tyre", seg=18)              # tyre
            rod((x, yt - s * .03, r), (x, yt + s * .88, r), r * .55, "steel", seg=12)   # rim
        rod((x, ya - s * .05, r), (x, ya + s * .2, r), .5, "steel_dark", seg=10)   # hub
    rod((x, y0 + 1.8, r), (x, y1 - 1.8, r), .3, "steel_dark", seg=8)            # axle beam


def tm2500(it):
    """TM2500-class mobile aeroderivative at LOD 3 inside the drawn envelope (78 x 55 ft, 42 ft):
    - GT trailer (south-north y+31..41): ladder chassis, rear bogie of four axles and a two-axle mid bogie on crane
      mats, gooseneck on landing legs; turbine enclosure with panel seams, doors, roof ventilation fans and a
      vent silencer; generator enclosure at the gooseneck end with the terminal box on the north face;
    - combustion-air filter house above the generator end: weather hoods on both faces, plenum down to the inlet;
    - rectangular exhaust collector and raised stack with its silencer section at the rear;
    - control / auxiliary trailer to the south with HVAC units, door and stair, and the interconnect cables to the GT
      trailer under a cable protector;
    - fuel-gas / water-wash skid at the east end with a flexible gas hose to the trailer;
    - generator leads: six 15 kV MV-105 cables (two per phase) dropping out of the terminal box into a ground tray
      that runs north to the yard duct bank (printed jacket legend on the run)."""
    import cable_install
    x, y = it["fp"][0], it["fp"][2]
    strip(it)
    T0, T1 = y + 31, y + 41                      # GT trailer width
    D = 4.6                                      # deck top
    # crane mats under the bogies and landing legs
    for (xa, xb) in ((x + 3, x + 21), (x + 41, x + 51), (x + 59, x + 65)):
        for k in range(3):
            box(xa, xb, T0 - 1.5 + k * 4.3, T0 + 2.2 + k * 4.3, 0, .35, "timber")
    # ladder chassis, deck, gooseneck
    for yb in (T0 + 1.6, T1 - 2.8):
        box(x + 1, x + 63, yb, yb + 1.2, 3.1, 4.2, "steel_dark")
    for xc in range(4, 62, 6):
        box(x + xc, x + xc + .4, T0 + 1.6, T1 - 1.6, 3.3, 4.2, "steel_dark")      # cross members
    box(x, x + 62, T0, T1, 4.2, D, "steel")
    box(x + 62, x + 71, T0 + 2, T1 - 2, 5.0, 6.4, "steel")                        # gooseneck
    box(x + 59, x + 62.5, T0 + 2, T1 - 2, 4.2, 6.4, "steel")
    box(x + 68, x + 70, T0 + 3.5, T1 - 3.5, 4.4, 5.0, "steel_dark")               # kingpin plate
    for yl in (T0 + 2.6, T1 - 3.2):                                               # landing legs, sand shoes
        box(x + 61.5, x + 62.1, yl, yl + .6, .5, 5.0, "steel_dark")
        box(x + 60.8, x + 62.8, yl - .7, yl + 1.3, .35, .55, "steel")
    dress(True)
    for xa in (x + 6, x + 10, x + 14, x + 18, x + 44, x + 48):
        axle(xa, T0, T1)
    for (xa, xb) in ((x + 3.8, x + 20.2), (x + 41.8, x + 50.2)):                 # fenders
        for yf, s in ((T0, 1), (T1, -1)):
            box(xa, xb, yf, yf + s * 2.2, 3.6, 3.75, "steel")
    dress(False)
    # turbine enclosure (rear) and generator enclosure (front)
    ET, EG = (x + 1.5, x + 38), (x + 38.4, x + 58.5)
    box(ET[0], ET[1], T0 + .5, T1 - .5, D, 15.6, "machine")
    box(EG[0], EG[1], T0 + .5, T1 - .5, D, 14.6, "machine")
    box(ET[0] - .1, EG[1] + .1, T0 + .4, T1 - .4, 14.6, 14.9, "roof")
    dress(True)
    xs = ET[0] + 3.2
    while xs < EG[1] - 1:                                                         # panel seams
        if abs(xs - 38.2 - x) > 1:
            for yy, s in ((T0 + .5, -1), (T1 - .5, 1)):
                box(xs - .08, xs + .08, yy, yy + s * .08, D + .2, 14.4, "steel")
        xs += 3.2
    for xd in (x + 8, x + 22, x + 31, x + 46):                                    # doors with handles, both faces
        for yy, s in ((T0 + .5, -1), (T1 - .5, 1)):
            box(xd, xd + 3, yy, yy + s * .1, D + .5, D + 7.3, "door")
            box(xd + 2.4, xd + 2.6, yy + s * .1, yy + s * .25, D + 3.5, D + 4.2, "steel")
    for (xa, xb) in ((x + 3, x + 7), (x + 26, x + 30), (x + 52, x + 56)):         # wall intake louvres
        for yy, s in ((T0 + .5, -1), (T1 - .5, 1)):
            box(xa, xb, yy, yy + s * .15, 9, 13, "louvre")
    dress(False)
    # enclosure ventilation: silencer box with two fans on the turbine roof
    box(x + 18, x + 32, T0 + 1.5, T1 - 1.5, 15.6, 19.5, "louvre")
    for xf in (x + 21.5, x + 28.5):
        rod((xf, (T0 + T1) / 2, 19.5), (xf, (T0 + T1) / 2, 20.6), 2.6, "duct", seg=20)
        rod((xf, (T0 + T1) / 2, 20.6), (xf, (T0 + T1) / 2, 20.8), 2.4, "fan", seg=20)
    # combustion-air filter house over the generator end, on a frame, plenum down to the turbine inlet
    FX, FY = (x + 36, x + 57), (T0 - 2, T1 + 2)
    for (xc, yc) in ((FX[0] + 1, FY[0] + 2.2), (FX[1] - 1, FY[0] + 2.2), (FX[0] + 1, FY[1] - 2.2), (FX[1] - 1, FY[1] - 2.2)):
        box(xc - .3, xc + .3, yc - .3, yc + .3, 14.9, 18, "steel_dark")
    box(x + 38.5, x + 45, T0 + 2.5, T1 - 2.5, 14.9, 18, "duct")                    # plenum
    box(FX[0], FX[1], FY[0], FY[1], 18, 28.5, "filter")
    box(FX[0] - .2, FX[1] + .2, FY[0] - .2, FY[1] + .2, 28.5, 29, "roof")
    dress(True)
    for zh in (19.5, 22.5, 25.5):                                                 # weather hoods, both faces and the end
        for yy, s in ((FY[0], -1), (FY[1], 1)):
            box(FX[0] + .5, FX[1] - .5, yy, yy + s * 1.2, zh + 2.0, zh + 2.3, "steel")
            for xh in (FX[0] + .5, FX[1] - .7):
                box(xh, xh + .2, yy, yy + s * 1.2, zh, zh + 2.3, "steel")
        box(FX[1], FX[1] + 1.2, FY[0] + .5, FY[1] - .5, zh + 2.0, zh + 2.3, "steel")
    for k in range(6):                                                            # roof access ladder, handrail
        box(FX[1] + .1, FX[1] + .3, FY[0] + 1, FY[0] + 1.2, D + k * 4, D + k * 4 + .15, "rail")
    rod((FX[1] + .2, FY[0] + 1.1, D), (FX[1] + .2, FY[0] + 1.1, 32), .06, "rail", seg=4)
    rod((FX[1] + .2, FY[0] + 2.1, D), (FX[1] + .2, FY[0] + 2.1, 32), .06, "rail", seg=4)
    for xr in (FX[0] + .3, FX[1] - .3):
        rod((xr, FY[0] + .3, 29), (xr, FY[0] + .3, 32), .06, "rail", seg=4)
        rod((xr, FY[1] - .3, 29), (xr, FY[1] - .3, 32), .06, "rail", seg=4)
    for yr in (FY[0] + .3, FY[1] - .3):
        rod((FX[0] + .3, yr, 32), (FX[1] - .3, yr, 32), .06, "rail", seg=4)
    dress(False)
    # exhaust: rectangular collector and raised stack with a silencer section
    box(x + 2, x + 15, T0 + 1, T1 - 1, 15.6, 20.5, "duct")
    box(x + 4, x + 13, T0 + 1.6, T1 - 1.6, 20.5, 26, "stack")
    box(x + 3.4, x + 13.6, T0 + 1, T1 - 1, 26, 34, "stack")                        # silencer
    box(x + 4, x + 13, T0 + 1.6, T1 - 1.6, 34, 41.4, "stack")
    box(x + 3.7, x + 13.3, T0 + 1.3, T1 - 1.3, 41.4, 42, "steel_dark")              # top lip
    dress(True)
    for zb in (26, 34):                                                           # flange bands
        box(x + 3.3, x + 13.7, T0 + .9, T1 - .9, zb - .2, zb + .2, "steel_dark")
    for (xc, yc) in ((x + 3, T0 + .6), (x + 14, T0 + .6), (x + 3, T1 - .6), (x + 14, T1 - .6)):
        rod((xc, yc, 20.5), ((xc + x + 8.5) / 2, (yc + (T0 + T1) / 2) / 2, 30), .18, "steel_dark", seg=6)   # stays
    dress(False)
    # generator terminal box on the north face, leads down into a ground tray to the yard duct bank
    tb = (x + 47, x + 53)
    box(tb[0], tb[1], T1 - .5, T1 + 1.6, D + 1, D + 7.5, "cabinet")
    box(tb[0] + .4, tb[1] - .4, T1 + 1.6, T1 + 1.7, D + 1.6, D + 6.9, "cabinet")              # bolted cover
    box(tb[0] + 2, tb[1] - 2, T1 + 1.7, T1 + 1.75, D + 4.8, D + 6.2, "sign")
    xt = x + 50                                                                   # tray centre line, north to the route
    box(xt - 1.3, xt + 1.3, T1 + 1.7, y + 55, .35, .42, "steel")                   # open ground tray on sleepers
    for xr in (xt - 1.3, xt + 1.2):
        box(xr, xr + .1, T1 + 1.7, y + 55, .35, .75, "steel")
    for yy in range(int(T1 + 3), int(y + 55), 4):
        box(xt - 1.6, xt + 1.6, yy, yy + .5, 0, .35, "timber")
    zc = .55
    leads = [xt - 1.0 + k * .4 for k in range(6)]
    for k, xl in enumerate(leads):
        rod((xl, T1 + 1.0, D + 1), (xl, T1 + 1.0, zc + 1.0), .12, "cable_mv", seg=8)          # drop from the box
        rod((xl, T1 + 1.0, zc + 1.0), (xl, T1 + 2.4, zc), .12, "cable_mv", seg=8)             # bend into the tray
        rod((xl, T1 + 2.4, zc), (xl, y + 55, zc), .12, "cable_mv", seg=8)
    for xl, yl in ((leads[1], T1 + 5.5), (leads[3], T1 + 7.5), (leads[4], T1 + 4.5)):   # printed legends, staggered
        cable_install.legend((xl, yl, zc + .125), (0, 0, 1), (0, 1, 0), 6, LEGEND_GEN)
    box(tb[0] - .2, tb[1] + .2, T1 + 1.6, T1 + 1.9, D + 7.3, D + 7.6, "sign")     # caution sign over the box
    # control / auxiliary trailer
    A0, A1 = y + 8, y + 17
    for yb in (A0 + 1.2, A1 - 2.2):
        box(x + 4, x + 50, yb, yb + 1, 3.1, 4.1, "steel_dark")
    box(x + 4, x + 50, A0, A1, 4.1, 4.5, "steel")
    box(x + 5, x + 49, A0 + .3, A1 - .3, 4.5, 13, "ehouse")
    box(x + 4.8, x + 49.2, A0 + .1, A1 - .1, 13, 13.4, "roof")
    box(x + 49.5, x + 53, A0 + 2.5, A1 - 2.5, 4.6, 6.0, "steel")                   # gooseneck stub
    for yl in (A0 + 2.4, A1 - 3):
        box(x + 47, x + 47.6, yl, yl + .6, .5, 4.1, "steel_dark")
        box(x + 46.3, x + 48.3, yl - .7, yl + 1.3, .35, .55, "steel")
    for k in range(2):
        box(x + 4, x + 18, A0 - 1.5 + k * 6.5, A0 + 2.5 + k * 6.5, 0, .35, "timber")
    dress(True)
    for xa in (x + 9, x + 13):
        axle(xa, A0, A1)
    box(x + 5, x + 6.2, A0 + 1.5, A1 - 1.5, 6, 11, "cabinet")                     # HVAC units on the rear wall
    box(x + 5.6, x + 6.4, A0 + 2, A1 - 2, 6.5, 10.5, "louvre")
    for xh in (x + 20, x + 34):
        box(xh, xh + 4, A1 - .3, A1 + .9, 9, 12, "cabinet")                       # wall-hung units, north face
    box(x + 26, x + 29, A1 - .3, A1 - .2, 5, 12, "door")                           # door, landing and stair north
    box(x + 25, x + 30, A1, A1 + 3, 4.3, 4.5, "grating")
    for s in range(4):
        box(x + 25, x + 30, A1 + 3 + s * .9, A1 + 3.9 + s * .9, 3.3 - s * 1.0, 3.5 - s * 1.0, "grating")
    for xr in (x + 25, x + 30):
        rod((xr, A1 + .1, 7.5), (xr, A1 + 6.6, 4), .06, "rail", seg=4)
    dress(False)
    # interconnect cables between the trailers, under a yellow cable protector across the walkway
    for k in range(4):
        xc = x + 34.5 + k * .45
        rod((xc, A1 + .1, 5), (xc, A1 + .9, .3), .1, "cable_tc", seg=6)
        rod((xc, A1 + .9, .3), (xc, T0 - 1, .3), .1, "cable_tc", seg=6)
        rod((xc, T0 - 1, .3), (xc, T0 + .2, 3.4), .1, "cable_tc", seg=6)
    box(x + 33.6, x + 37.2, y + 22, y + 24.5, 0, .45, "amber")
    # fuel-gas / water-wash skid at the east end, flexible hose to the gooseneck end
    box(x + 72, x + 78, T0 - 1, T1 + 1, 0, .5, "concrete")
    box(x + 72.3, x + 77.7, T0 - .7, T1 + .7, .5, 8.5, "cabinet")
    dress(True)
    box(x + 72.2, x + 72.3, T0 + 1, T0 + 4, 1.5, 7, "door")
    box(x + 72.2, x + 72.3, T1 - 4, T1 - 1, 1.5, 7, "door")
    pipe([(x + 72, T0 + 6, 2.5), (x + 66, T0 + 6, 2.5), (x + 63, T0 + 6, 1.2), (x + 60, T0 + 6, 1.2),
          (x + 58.6, T0 + 6, 3.8)], 0, .3, "fuelgas", elbows=False)
    dress(False)


def fuel_cells_and_microturbines():
    for it in items("FC-"):
        if "inverter" in it["name"]:
            continue
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        box(x0, x1, y0, y1, 0, .5, "concrete")
        n = 4
        L = (y1 - y0 - .6) / n
        for k in range(n):                                                   # power-module cabinets
            ya = y0 + .3 + k * L
            box(x0 + .3, x1 - .3, ya + .06, ya + L - .06, .5, 6.4, "bess")
            box(x0 + .3, x1 - .3, ya + .06, ya + L - .06, 6.4, 6.6, "roof")
            box(x0 + 2, x1 - 2, ya + 1.2, ya + L - 1.2, 6.6, 7, "louvre")      # exhaust vent
        dress(True)
        for k in range(n):
            ya = y0 + .3 + k * L
            for x, s in ((x0 + .3, -1), (x1 - .3, 1)):
                box(x, x + s * .08, ya + .5, ya + L - .5, 1, 5.8, "door")
                box(x + s * .08, x + s * .18, ya + L - 1.2, ya + L - .9, 3, 3.6, "steel")   # handle
        dress(False)
    for it in items("MT-"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        box(x0, x1, y0, y1, 0, .5, "concrete")
        box(x0 + .2, x1 - .2, y0 + .2, y1 - .2, .5, 8, "cabinet")
        for k in range(4):                                                   # roof intake hoods
            ya = y0 + 1 + k * (y1 - y0 - 2) / 4
            box(x0 + .8, x1 - .8, ya + .4, ya + (y1 - y0 - 2) / 4 - .4, 8, 9, "louvre")
            rod(((x0 + x1) / 2, ya + (y1 - y0 - 2) / 8, 9), ((x0 + x1) / 2, ya + (y1 - y0 - 2) / 8, 9.5),
                .7, "stack", seg=10)                                          # exhaust outlet
        dress(True)
        ribs(x0 + .2, x1 - .2, y0 + .2, y1 - .2, .5, 8, False, pitch=1.4)
        dress(False)


def skids():
    # BESS black-start alternative (conditional): two battery containers with HVAC and a PCS
    it = find("CONDITIONAL: BESS black-start")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    for ya in (y0 + 3, y0 + 19):
        box(x0 + 1, x0 + 41, ya, ya + 8, 0, .5, "concrete")
        box(x0 + 1.2, x0 + 40.8, ya + .2, ya + 7.8, .5, 9.5, "conditional")
        box(x0 + 40.8, x0 + 42, ya + 1.5, ya + 6.5, 3, 7.5, "machine")
    box(x1 - 3, x1 - .5, y0 + 13, y1 - 15, 0, 7, "cabinet")                   # PCS between the rows
    # SC inlet chillers / evaporative coolers (conditional): chiller packages with roof fin-fans
    for it in items("CONDITIONAL: SC-"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        box(x0, x1, y0, y1, 0, .6, "concrete")
        for xa in (x0 + 2, x0 + 31):
            box(xa, xa + 27, y0 + 2, y1 - 2, .6, 9, "conditional")
            box(xa, xa + 27, y0 + 2, y1 - 2, 9, 12.6, "bundle")
            for k in range(3):
                for yy in (y0 + 10, y1 - 10):
                    rod((xa + 4.5 + 9 * k, yy, 12.6), (xa + 4.5 + 9 * k, yy, 13.4), 3.6, "fan", seg=16)
        dress(True)
        pipe([((x0 + x1) / 2, y1, 4), ((x0 + x1) / 2, y1 + 18, 4)], 4, .6, "chw")  # chilled water to the inlet
        dress(False)
    # water-injection skid: two pumps with motors, cartridge filter, sunshade
    it = find("Water-injection skid")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .7, "steel")
    for yp in (y0 + 3, y0 + 7):
        rod((x0 + 2, yp, 2), (x0 + 6, yp, 2), 1.2, "pump", seg=14)
        rod((x0 + 6.2, yp, 2), (x0 + 10, yp, 2), 1.1, "motor", seg=14)
    rod((x0 + 15, y0 + 5, .7), (x0 + 15, y0 + 5, 5.5), 1.2, "tank", seg=14)
    for (x, y) in ((x0 + .4, y0 + .4), (x1 - .4, y0 + .4), (x0 + .4, y1 - .4), (x1 - .4, y1 - .4)):
        box(x - .2, x + .2, y - .2, y + .2, .7, 7.5, "steel")
    box(x0, x1, y0, y1, 7.5, 8, "roof")
    # aqueous ammonia: horizontal tank on saddles in a curbed containment
    it = find("Aqueous ammonia")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .4, "concrete")
    for b in ((x0, x1, y0, y0 + .6), (x0, x1, y1 - .6, y1), (x0, x0 + .6, y0, y1), (x1 - .6, x1, y0, y1)):
        box(*b, .4, 2.2, "concrete")
    fuel.hvessel(x0 + 4, x1 - 4, (y0 + y1) / 2, 5.2, 4.2, saddles=(x0 + 9, x1 - 9), nozzles=(x0 + 15, x0 + 25),
                 psv=x0 + 20)
    box(x1 - 3.5, x1 - .8, y0 + 1, y0 + 3.5, .4, 6, "panel")                 # truck fill / scrubber panel


def small_units():
    """The last single-box units in the modular yard, at LOD 3 inside their drawn footprints."""
    # GSP-1 / -2: generator breaker / protection cabinets beside CONT-1 / -2 (cables in on the west face)
    for it in items("GSP-"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        box(x0, x1, y0, y1, 0, .5, "steel")
        box(x0 + .2, x1 - .2, y0 + .2, y1 - .2, .5, 7.4, "swgr")
        box(x0, x1, y0, y1, 7.4, 7.8, "roof")
        dress(True)
        for ya in (y0 + .8, (y0 + y1) / 2 + .2):                          # two doors, east face
            box(x1 - .2, x1 - .1, ya, ya + (y1 - y0) / 2 - 1, 1, 6.9, "door")
            box(x1 - .1, x1, ya + (y1 - y0) / 2 - 1.6, ya + (y1 - y0) / 2 - 1.4, 3.6, 4.4, "steel")
        for yy in (y0 + .2, y1 - .2):
            box(x0 + 2, x1 - 2, yy - .05, yy + .05, 5.2, 6.6, "louvre")
        box(x0 - .1, x0 + .2, (y0 + y1) / 2 - 1.2, (y0 + y1) / 2 + 1.2, 1.2, 2.4, "steel_dark")   # gland plate
        box(x1, x1 + .05, y0 + 1, y0 + 2.2, 6.2, 7, "sign")
        dress(False)
    # PIC: portable input cabinet with cam-lock receptacle panels on both faces
    it = find("PIC:")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .4, "steel")
    for xs in (x0 + .5, x1 - .9):                                         # skid runners
        box(xs, xs + .4, y0, y1, 0, .6, "steel_dark")
    box(x0 + .3, x1 - .3, y0 + .3, y1 - .3, .6, 6.5, "swgr")
    box(x0 + .1, x1 - .1, y0 + .1, y1 - .1, 6.5, 7, "roof")
    dress(True)
    cols = ("cable_mc", "camlock_r", "camlock_b", "camlock_w", "camlock_g")
    for xf, s in ((x0 + .3, -1), (x1 - .3, 1)):
        box(xf, xf + s * .05, y0 + .8, y1 - .8, 1.6, 3.6, "steel_dark")       # receptacle panel
        for k, c in enumerate(cols):
            yc = y0 + 1.3 + k * (y1 - y0 - 2.6) / 4
            rod((xf + s * .05, yc, 2.6), (xf + s * .35, yc, 2.6), .16, c, seg=10)
        box(xf, xf + s * .4, y0 + .6, y1 - .6, 3.7, 3.8, "steel")              # rain hood
        box(xf, xf + s * .05, y0 + 1.5, y1 - 1.5, 4.2, 6, "door")
    box(x1 - .3, x1 - .25, y0 + 2, y1 - 2, 6.1, 6.4, "sign")
    dress(False)
    # GEN-O: open engine-generator skid
    it = find("GEN-O:")
    x0, x1, y0, y1 = it["fp"]
    ym = (y0 + y1) / 2
    strip(it)
    for yb in (y0 + .6, y1 - 1.2):
        box(x0, x1, yb, yb + .6, 0, 1.2, "steel_dark")                        # base rails
    box(x0 + .3, x1 - .3, y0 + .6, y1 - .6, .9, 1.2, "steel")
    box(x0 + .5, x0 + 4, y0 + .5, y1 - .5, 1.2, 7.6, "radiator")              # radiator, west end
    box(x0 + 4, x0 + 4.4, y0 + 1, y1 - 1, 2, 7, "steel")                       # fan shroud
    box(x0 + 6, x0 + 15, ym - 1.6, ym + 1.6, 1.2, 4.8, "machine")             # engine block
    for s in (-1, 1):
        box(x0 + 6.3, x0 + 14.7, ym + s * 1.7 - .9, ym + s * 1.7 + .9, 4.2, 5.8, "motor")   # cylinder heads (V)
    rod((x0 + 15, ym, 3.4), (x0 + 16.4, ym, 3.4), 2.4, "steel", seg=18)      # flywheel housing
    rod((x0 + 16.4, ym, 3.4), (x0 + 23.5, ym, 3.4), 2.7, "machine", seg=20)  # generator
    box(x0 + 18, x0 + 22, y1 - 1.6, y1 - .4, 4.5, 7.2, "cabinet")              # terminal box
    dress(True)
    rod((x0 + 8, ym, 6.6), (x0 + 14, ym, 6.6), .9, "stack", seg=14)            # exhaust silencer on brackets
    rod((x0 + 14, ym, 6.6), (x0 + 14, ym, 7.9), .35, "stack", seg=10)
    for xb in (x0 + 9, x0 + 13):
        box(xb - .1, xb + .1, ym - .2, ym + .2, 5.6, 5.8, "steel")
    rod((x0 + 6.5, ym + 1.2, 3), (x0 + 6.5, ym + 1.2, 6.6), .25, "duct", seg=8)
    box(x1 - 2.2, x1 - .4, y0 + .6, y0 + 2.2, 1.2, 6, "panel")                 # control panel
    box(x0 + 5, x0 + 6, y0 + .6, y0 + 2, 1.2, 2.2, "battery")                  # start batteries
    for (xg, yg) in ((x0 + 2, y0 + .3), (x0 + 2, y1 - .3)):
        box(xg - 1.5, xg + 1.5, yg - .05, yg + .05, 1.5, 7, "louvre")          # radiator guards
    dress(False)
    # portable-pad gas-conditioning skid: filter-separators, line heater, regulator runs, panel
    it = find("Portable pad gas-conditioning skid")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .6, "steel")
    for xv in (x0 + 3, x0 + 7):                                               # vertical filter-separators
        rod((xv, y0 + 3, .6), (xv, y0 + 3, 6.8), 1.2, "fuelgas", seg=16)
        rod((xv, y0 + 3, 6.8), (xv, y0 + 3, 7.4), .9, "fuelgas", seg=16)
    fuel.hvessel(x0 + 11, x0 + 21, y0 + 5, 2.6, 1.6, c="equip", saddles=(x0 + 13, x0 + 19))   # line heater
    rod((x0 + 19.5, y0 + 5, 4.2), (x0 + 19.5, y0 + 5, 7.6), .35, "stack", seg=8)
    dress(True)
    for yr in (y0 + 2, y0 + 8):                                               # regulator runs
        pipe([(x0 + 22, yr, 2.2), (x1 - 1.5, yr, 2.2)], 2.2, .3, "fuelgas")
        for xr in (x0 + 24, x0 + 27):
            fuel.valve((xr, yr, 2.2), 0, .3, kind="ctrl")
    pipe([(x0 + 3, y0 + 3, 2), (x0 + 3, y0 + 8, 2), (x0 + 7, y0 + 8, 2)], 2, .3, "fuelgas")
    box(x1 - 1.2, x1 - .3, y0 + 4, y0 + 6.5, .6, 5.5, "panel")
    dress(False)
    # RICE CEMS shelter: insulated walk-in shelter, HVAC, heated sample line, calibration-gas cylinders
    it = find("RICE CEMS")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    box(x0, x1, y0, y1, 0, .5, "concrete")
    box(x0 + .3, x1 - .3, y0 + .3, y1 - .3, .5, 9.2, "ehouse")
    box(x0 + .1, x1 - .1, y0 + .1, y1 - .1, 9.2, 9.6, "roof")
    dress(True)
    box(x0 + 2, x0 + 5, y0 + .25, y0 + .3, .7, 7.6, "door")
    box(x1 - .3, x1 + .0, y0 + 3, y0 + 7, 3, 6.5, "machine")                  # wall HVAC (inside the footprint)
    for k in range(5):                                                         # cylinder rack, south face
        rod((x0 + 7 + k * 1.1, y0 + .1, .5), (x0 + 7 + k * 1.1, y0 + .1, 5.2), .4, "red" if k % 2 else "steel", seg=10)
    box(x0 + 6.4, x0 + 12.6, y0, y0 + .1, 3.5, 3.7, "steel")
    rod((x0 + 3, y1 - .4, 9.6), (x0 + 3, y1 - .4, 10), .3, "steel", seg=8)     # sample line entry
    dress(False)
    # SC-1 / SC-2 lube-oil fin-fan coolers: legs, coil bundle, fan plenums with guards, drive motors
    for it in items("SC-"):
        if "lube-oil" not in it["name"]:
            continue
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        for (xl, yl) in ((x0 + .5, y0 + .5), (x1 - .5, y0 + .5), (x0 + .5, y1 - .5), (x1 - .5, y1 - .5),
                         ((x0 + x1) / 2, y0 + .5), ((x0 + x1) / 2, y1 - .5)):
            box(xl - .3, xl + .3, yl - .3, yl + .3, 0, 5.8, "steel")
        box(x0, x1, y0, y1, 5.8, 7.4, "bundle")                               # finned coil bundle
        box(x0, x1, y0, y1, 7.4, 7.6, "steel")
        for xf in (x0 + 5, x1 - 5):
            rod((xf, (y0 + y1) / 2, 7.6), (xf, (y0 + y1) / 2, 9.4), 4.2, "steel", seg=24)   # fan ring
            rod((xf, (y0 + y1) / 2, 9.4), (xf, (y0 + y1) / 2, 9.6), 4.0, "fan", seg=24)
        dress(True)
        for xf in (x0 + 5, x1 - 5):
            rod((xf, (y0 + y1) / 2, 2.4), (xf, (y0 + y1) / 2, 5.6), .7, "motor", seg=12)      # drive under the coil
        for yh in (y0 + .2, y1 - .2):
            box(x0 + .3, x1 - .3, yh - .2, yh + .2, 6, 7.2, "steel")            # headers
        dress(False)


def build():
    containers()
    trailers()
    fuel_cells_and_microturbines()
    skids()
    small_units()
