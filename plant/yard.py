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
    # TM2500-class trailers: gooseneck, landing legs, stair and walkway, exhaust collector
    for it in items("TM-"):
        x, y = it["fp"][0], it["fp"][2]
        on(it)
        dress(True)
        box(x + 64, x + 70, y + 32, y + 40, 3.6, 4.5, "steel")                # gooseneck to the tractor
        box(x + 52, x + 64, y + 33, y + 39, 4.5, 5.2, "steel")
        for (xl, yl) in ((x + 40, y + 31), (x + 40, y + 41), (x + 36, y + 9.5), (x + 36, y + 15.5)):
            box(xl - .3, xl + .3, yl - .3, yl + .3, 0, 4.5, "steel")
        box(x + 4, x + 14, y + 26, y + 29.6, 4.3, 4.6, "grating")             # walkway, south side
        for s in range(4):
            box(x + 15, x + 18, y + 26 - s * .9 - .9, y + 26 - s * .9, 3.5 - s * 1.0, 3.7 - s * 1.0, "grating")
        rod((x + 4, y + 26, 7.9), (x + 14, y + 26, 7.9), .06, "rail", seg=4)
        box(x + 2, x + 14, y + 31, y + 41, 16, 19, "duct")                    # exhaust collector under the stack
        for xd in (x + 22, x + 36):
            box(xd, xd + 3.5, y + 30.9, y + 31, 5, 13, "door")
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


def build():
    containers()
    trailers()
    fuel_cells_and_microturbines()
    skids()
