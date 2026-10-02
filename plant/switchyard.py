"""Zone C, 230 kV switchyard, at LOD 3 (detail cycle 1).

- Control-cable trenches: precast concrete trench (walls and removable covers) from the relay
  house along the yard (y 124) and down every diameter beside its breakers; the breakers'
  CT / VT secondaries, trip / close and alarm circuits run in them to the relay house.
- Dead-tank breakers: spring operating-mechanism cabinet, bushing CT housings, ground leads.
- Disconnect switches: centre-break blades on the insulator stacks and a motor operator on each stand.
- Line entrances (Line 1 and Line 2): surge arresters and coupling-capacitor VTs on stands, with
  line traps on the dead-end span.
- Lighting masts round the yard, the yard fence with its gate at the relay house.
All typical, not engineered.
"""
import fuel
from fuel import box, rod, find, on

DIAMETERS = (700, 900, 1100, 1720, 1860, 2010)
TRENCH_Y = 124
PH = (-7, 0, 7)


def dress(flag):
    fuel.D = flag


def routes(add_route):
    """Cable trenches as routes (they carry the switchyard control cabling); run before wiring.py."""
    sheet = "typical (switchyard detail)"
    add_route("cable_trench", [(490, 200), (505, 200), (505, TRENCH_Y), (1300, TRENCH_Y)], "ROUTES_BASE", sheet=sheet)
    add_route("cable_trench", [(1300, TRENCH_Y), (DIAMETERS[-1] - 12.5, TRENCH_Y)], "SWYD_FUTURE", sheet=sheet)
    for x in DIAMETERS:
        lay = "ROUTES_BASE" if x < 1300 else "SWYD_FUTURE"
        add_route("cable_trench", [(x - 12.5, 72), (x - 12.5, 230)], lay, sheet=sheet)


def trench_parts(routes_):
    yard = find("230 kV switchyard (gravel)")
    on(yard)
    dress(True)
    for r in routes_:
        if r["type"] != "cable_trench":
            continue
        lay = r["layer"].replace("ROUTES_BASE", "BASE_SWITCHYARD")
        for a, b in zip(r["points"], r["points"][1:]):
            x0, x1 = sorted((a[0], b[0]))
            y0, y1 = sorted((a[1], b[1]))
            along_x = x1 - x0 > y1 - y0
            if along_x:
                box(x0 - 1.5, x1 + 1.5, y0 - 1.5, y0 + 1.5, 0, .55, "concrete", layer=lay)
                s = x0 - 1.5
                while s < x1 + 1.5:                      # precast covers with joints
                    box(s + .04, min(s + 4, x1 + 1.5) - .04, y0 - 1.35, y0 + 1.35, .55, .7, "concrete", layer=lay)
                    s += 4
            else:
                box(x0 - 1.5, x0 + 1.5, y0 - 1.5, y1 + 1.5, 0, .55, "concrete", layer=lay)
                s = y0 - 1.5
                while s < y1 + 1.5:
                    box(x0 - 1.35, x0 + 1.35, s + .04, min(s + 4, y1 + 1.5) - .04, .55, .7, "concrete", layer=lay)
                    s += 4
    dress(False)


def breakers():
    for d, x in zip(("D1", "D2", "D3", "D4", "D5", "D6"), DIAMETERS):
        for k, y in enumerate((110, 150, 190), 1):
            it = find(f"{d} 230 kV breaker {k}")
            on(it)
            dress(True)
            box(x - 10.5, x - 8.2, y - 2, y + 2, 1, 6.5, "cabinet")                # operating mechanism
            box(x - 10.7, x - 8, y - 2.2, y + 2.2, 6.5, 6.8, "roof")
            rod((x - 9.4, y, 1), (x - 12.5, y, .3), .12, "steel", seg=6)             # control conduit to the trench
            for ph in PH:                                                             # bushing CT housings
                for s in (-1, 1):
                    rod((x + ph, y + 1.5 * s, 11.2), (x + ph, y + 1.75 * s, 12.6), .95, "xfmr", seg=12)
            rod((x + 7.5, y + 3, 1), (x + 7.5, y + 3, .2), .1, "copper", seg=4)       # ground lead
            dress(False)
        sw = [i for i in fuel.G["items"] if i["name"].startswith(f"{d} disconnect switches")]
        if not sw:
            continue
        on(sw[0])
        dress(True)
        for y in (90, 130, 170, 210):
            for ph in PH:                                                             # centre-break blades
                rod((x + ph, y - 2.8, 24.3), (x + ph, y + 2.8, 24.3), .14, "conductor", seg=6)
                rod((x + ph, y, 24), (x + ph, y, 24.6), .3, "steel", seg=8)
            box(x + 9.4, x + 11, y - .8, y + .8, 4, 7, "cabinet")                    # motor operator
            rod((x + 10.2, y, 7), (x + 9.4, y, 14), .08, "steel", seg=4)               # operating rod
        dress(False)


def line_entrances():
    L = "BASE_SWITCHYARD"
    for (x, n) in ((670, "Line 1"), (870, "Line 2")):
        fuel.new_item(L, f"{n} entrance: surge arresters, CCVTs and line traps", (x - 9, x + 9, 74, 84), (0, 40),
                      area="C", sheet="typical (switchyard detail)",
                      info="Station-class surge arresters, coupling-capacitor voltage transformers for "
                           "metering / protection / PLC, and line traps on the incoming span (typical).")
        box(x - 9, x + 9, 74, 84, 0, .5, "concrete")
        for ph in PH:
            for (yy, kind) in ((76.5, "arr"), (81.5, "cvt")):
                box(x + ph - .5, x + ph + .5, yy - .5, yy + .5, .5, 12, "steel")       # stand
                if kind == "arr":
                    rod((x + ph, yy, 12), (x + ph, yy, 21), .55, "insulator", seg=10)
                    rod((x + ph, yy, 21), (x + ph, yy, 21.6), 1.0, "steel", seg=10)    # grading ring
                else:
                    rod((x + ph, yy, 12), (x + ph, yy, 14), 1.1, "xfmr", seg=12)       # CCVT base tank
                    rod((x + ph, yy, 14), (x + ph, yy, 24), .5, "insulator", seg=10)
        fuel.D = True
        for ph in (-7, 7):                                                            # line traps (two phases)
            rod((x + ph, 70, 36), (x + ph, 70, 40), 1.1, "steel", seg=14)
        fuel.D = False


def masts_and_fence():
    fuel.new_item("BASE_SWITCHYARD", "Switchyard lighting masts and fence", (398, 2062, 46, 256), (0, 62),
                  area="C", basis="typical", register=False, sheet="typical (switchyard detail)")
    for x in range(560, 2000, 360):
        for y in (48.5, 252):
            box(x - .5, x + .5, y - .5, y + .5, 0, 58, "steel")
            box(x - 2.5, x + 2.5, y - .6, y + .6, 58, 59, "steel")
            for dx in (-2, 0, 2):
                box(x + dx - .5, x + dx + .5, y - .9, y + .9, 57.2, 58, "lamp")
    fuel.D = True
    for (x0, x1, y0, y1) in ((398, 2062, 46, 46.3), (398, 2062, 255.7, 256), (398, 398.3, 46, 256),
                             (2061.7, 2062, 46, 256)):
        L_ = max(x1 - x0, y1 - y0)
        if x1 - x0 > y1 - y0:
            box(x0, x1, y0, y1, 0, 8, "fence")
            for x in range(int(x0), int(x1), 10):
                box(x, x + .3, y0 - .1, y1 + .1, 0, 8.5, "steel")
        else:
            for (ya, yb) in ((y0, 180), (232, y1)):                                  # gate opening at the relay house
                box(x0, x1, ya, yb, 0, 8, "fence")
            for y in range(int(y0), int(y1), 10):
                box(x0 - .1, x1 + .1, y, y + .3, 0, 8.5, "steel")
    fuel.D = False


def build(routes_):
    trench_parts(routes_)
    breakers()
    line_entrances()
    masts_and_fence()
