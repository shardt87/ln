"""Turbine hall access: how people move between the units.

The machine trains (generator, GT, exhaust) fill the EL 20 operating deck from the south gallery to the HRSG
wall, and the cable trays run at EL 41-49 over them, so there is no headroom for a crossover bridge over the
machines. As in a real table-top turbine hall, people cross underneath:
- the solid EL 0-20 block becomes the structure it stands for: an operating-floor slab (EL 18.5-20) on a
  20 ft column grid with beams, each GT and the ST on its own table-top pedestal (top slab on legs), and an open
  ground floor (EL 0) below with LED fixtures under the slab;
- stairs from the ground floor up through guarded openings in the slab between GT1 / GT2 and GT2 / GT3, joining
  the two existing deck stairs (laydown bay, south gallery east end), so the route is up - across - down - across
  - up;
- crossover stiles (steps up, a short grated platform with handrails, steps down) where the north-south walk to
  each stair meets the inlet-chilling chilled-water headers at EL 3;
- operators on the ground floor, on a stile and on a stair.
The chilled-water headers that were buried in the old block now run visibly under the deck.
"""
import fuel
from fuel import box, rod

X0, X1, Y0, Y1 = 560.0, 1099.0, 404.0, 556.0
ZS = 18.5                               # underside of the operating-floor slab
OPEN = [(711.0, 719.0, 480.0, 516.0), (871.0, 879.0, 480.0, 516.0)]     # stair openings
PED = [(614.0, 646.0, 410.0, 540.0), (774.0, 806.0, 410.0, 540.0), (934.0, 966.0, 410.0, 540.0),
       (1018.0, 1082.0, 410.0, 552.0)]


def person(x, y, z=0.0, a=0.0, vest="hivis", hat="hardhat"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest, hat=hat)


def _in_ped(x, y, m=1.0):
    return any(a - m <= x <= b + m and c - m <= y <= d + m for (a, b, c, d) in PED)


def stair_y(x0, x1, y0, y1, z0, z1):
    """Straight stair rising toward +y: treads, stringers, handrails."""
    n = max(4, int((z1 - z0) / .62))
    run = y1 - y0
    for t in range(n):
        a, b = t * run / n, (t + 1) * run / n
        z = z0 + (z1 - z0) * (t + 1) / n
        box(x0 + .3, x1 - .3, y0 + a, y0 + b, z - .18, z, "grating")
    for xx in (x0 + .15, x1 - .15):
        rod((xx, y0, z0), (xx, y1, z1), .2, "stair", seg=4)
        rod((xx, y0, z0 + 3.5), (xx, y1, z1 + 3.5), .06, "rail", seg=4)
        for t in range(5):
            yp = y0 + t * run / 4
            zp = z0 + (z1 - z0) * t / 4
            rod((xx, yp, zp), (xx, yp, zp + 3.5), .06, "rail", seg=4)


def stile(x0, x1, ya, yb, h=5.5):
    """Crossover stile over low pipes: steps up (+y), a grated platform, steps down."""
    s = 4.0
    stair_y(x0, x1, ya, ya + s, 0, h)
    box(x0 + .2, x1 - .2, ya + s, yb - s, h - .2, h, "grating")
    for xx in (x0 + .15, x1 - .15):                                        # platform rails and posts
        rod((xx, ya + s, h + 3.5), (xx, yb - s, h + 3.5), .06, "rail", seg=4)
        rod((xx, ya + s, h + 1.75), (xx, yb - s, h + 1.75), .05, "rail", seg=4)
        for yy in (ya + s, (ya + yb) / 2, yb - s):
            rod((xx, yy, 0), (xx, yy, h + 3.5), .08, "stair", seg=4)
    # down-flight: mirror (falls toward +y)
    n = 9
    for t in range(n):
        a, b = t * s / n, (t + 1) * s / n
        z = h - h * (t + 1) / n
        box(x0 + .3, x1 - .3, yb - s + a, yb - s + b, max(0, z + h / n - .18), z + h / n, "grating")
    for xx in (x0 + .15, x1 - .15):
        rod((xx, yb - s, h), (xx, yb, 0), .2, "stair", seg=4)
        rod((xx, yb - s, h + 3.5), (xx, yb, 3.5), .06, "rail", seg=4)
    box(x0 - .5, x1 + .5, ya - .6, ya - .1, 0, .02, "yellow")               # floor marking at the foot
    box(x0 - .5, x1 + .5, yb + .1, yb + .6, 0, .02, "yellow")


def build():
    G = fuel.G
    items, parts = G["items"], G["parts"]
    deck = next(it for it in items if it["name"].startswith("Turbine deck EL 20"))
    parts[:] = [p for p in parts if not (p["item"] == deck["id"] and p["kind"] == "box" and p["color"] == "concrete"
                                         and p["min"][2] <= 0 and p["max"][2] >= 19.9)]
    deck["info"] = ("Operating floor EL 20: concrete slab on a 20 ft steel column grid, each GT and the ST on its own "
                    "table-top pedestal; open ground floor below (piping, walkways), stairs up through the slab between "
                    "the units (typical).")
    fuel.on(deck)
    fuel.D = False
    # operating-floor slab, cut around the stair openings
    xs = sorted({X0, X1} | {v for (a, b, _, _) in OPEN for v in (a, b)})
    for xa, xb in zip(xs, xs[1:]):
        op = next((o for o in OPEN if o[0] == xa), None)
        if op:
            box(xa, xb, Y0, op[2], ZS, 20, "concrete")
            box(xa, xb, op[3], Y1, ZS, 20, "concrete")
        else:
            box(xa, xb, Y0, Y1, ZS, 20, "concrete")
    # column grid and beams under the slab
    cols = []
    for x in range(570, 1095, 20):
        for y in (408.0, 480.0, 552.0):
            if _in_ped(x, y) or any(a - 1.5 <= x <= b + 1.5 and c - 1.5 <= y <= d + 1.5 for (a, b, c, d) in OPEN):
                continue
            box(x - 1, x + 1, y - 1, y + 1, 0, ZS, "steel")
            box(x - 1.8, x + 1.8, y - 1.8, y + 1.8, 0, .5, "concrete")            # base plate / grout pad
            cols.append((x, y))
    cs = set(cols)
    for (x, y) in cols:
        if (x + 20, y) in cs:
            box(x, x + 20, y - .6, y + .6, ZS - 1.6, ZS, "steel")
    for x in range(570, 1095, 20):
        for (ya, yb) in ((408.0, 480.0), (480.0, 552.0)):
            if (x, ya) in cs and (x, yb) in cs:
                box(x - .5, x + .5, ya, yb, ZS - 1.2, ZS, "steel")
    # table-top pedestals: top slab on legs (pipes pass between the legs)
    for (a, b, c, d) in PED:
        box(a, b, c, d, ZS - 5.0, ZS, "concrete")
        n = 3 if d - c < 135 else 4
        for k in range(n):
            y = c + 2 + k * (d - c - 4) / (n - 1)
            for x in (a + 2, b - 2):
                box(x - 2, x + 2, y - 2, y + 2, 0, ZS - 5.0, "concrete")
    fuel.D = True
    it = fuel.new_item("BASE_POWER_BLOCK", "Turbine hall access: stairs through the deck between the units, crossover "
                       "stiles over the chilled-water headers, ground-floor lighting", (560, 1099, 404, 556), (0, 24),
                       area="A", basis="typical", sheet="typical (hall access)", register=False,
                       info="People cross between units at grade under the operating floor: stairs up through guarded "
                            "slab openings between GT1 / GT2 and GT2 / GT3 (plus the laydown-bay and south-gallery "
                            "stairs), crossover stiles where the walk meets the EL 3 chilled-water headers, LED fixtures "
                            "under the slab.")
    fuel.on(it)
    fuel.D = True
    for (a, b, c, d) in OPEN:
        stair_y(a + 1, b - 1, c + 2, d - 2, 0, 20)                          # ground floor -> deck, rising north
        for (xa, xb, ya, yb) in ((a - .1, a + .1, c, d), (b - .1, b + .1, c, d), (a, b, c - .1, c + .1)):
            box(xa, xb, ya, yb, 20, 20.3, "sp_yellow")                        # toe board
            box(xa, xb, ya, yb, 23.3, 23.5, "sp_yellow")                      # top rail
            box(xa, xb, ya, yb, 21.7, 21.85, "sp_yellow")                     # mid rail
        for (px, py) in ((a, c), (b, c), (a, d), (b, d), (a, (c + d) / 2), (b, (c + d) / 2)):
            rod((px, py, 20), (px, py, 23.5), .08, "sp_yellow", seg=6)
        stile(a + 1, b - 1, 455.0, c + 1.5)                                  # over the CHW headers (y 464 / 470)
    for x in range(585, 1090, 30):                                           # LED fixtures under the slab
        for y in (440.0, 520.0):
            if _in_ped(x, y, 2):
                continue
            box(x - .5, x + .5, y - 2, y + 2, ZS - .25, ZS, "steel")
            box(x - .42, x + .42, y - 1.9, y + 1.9, ZS - .28, ZS - .25, "lamp_in")
    for x in range(590, 1090, 40):                                           # walkway markings along the ground floor
        if not _in_ped(x, 425, 1) and not _in_ped(x + 30, 425, 1):
            box(x, x + 30, 424.6, 424.8, 0, .02, "yellow")
            box(x, x + 30, 430.2, 430.4, 0, .02, "yellow")
    person(700, 427, 0, 0.0)                                                 # walking east on the ground floor
    person(864, 428, 0, 0.0, vest="hivis_o")
    person(715, 466, 5.5, 1.5708)                                            # on the stile
    person(875, 500, 12.5, 1.5708, vest="hivis_o")                           # climbing to the deck
    person(716, 520, 20, 1.5708)                                             # arriving on the deck
    fuel.D = False
    return 1
