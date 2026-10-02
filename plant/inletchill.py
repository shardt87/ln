"""GT inlet chilling at LOD 3 (detail cycle 8).

- Condenser-water loop closed: tower basin to the CW pumps, CW pumps into the chiller building,
  warm return from the chillers up into the tower (new `cw` routes, drawn as round pipe), and
  the chilled-water side from the chillers to the CHW pumps and the TES tank (`chw` routes).
- Chiller building: wall louvres, roof exhaust fans, refrigerant relief vent stacks, a roll-up
  door, and six chiller packages (evaporator / condenser shells and compressor) seen through it
  in the viewer.
- Chiller cooling tower (12 cells): fans with blades, hub, gearbox, shaft and motor; fan-deck
  handrail; access stair; intake louvres; a hot-water riser into every cell from a header.
- CW and CHW pump sets on plinths (pump, coupling guard, motor, suction / discharge spools).
- Inlet-chilling e-house: landings, stairs, HVAC, cable entries.
All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, find, on, strip

SHEET = "typical (inlet chilling detail)"


def dress(flag):
    fuel.D = flag


def routes(add_route):
    add_route("cw", [(280, 1240), (280, 1170)], layer="OPT_IC_ROUTES", sheet=SHEET)            # basin to CW pumps
    add_route("cw", [(250, 1150), (240, 1150)], layer="OPT_IC_ROUTES", sheet=SHEET)            # CW pumps to chillers
    add_route("cw", [(165, 1170), (165, 1240)], layer="OPT_IC_ROUTES", sheet=SHEET)            # warm return to tower
    add_route("chw", [(105, 1170), (105, 1190)], layer="OPT_IC_ROUTES", sheet=SHEET)           # chillers to CHW pumps
    add_route("chw", [(150, 1207), (176, 1207)], layer="OPT_IC_ROUTES", sheet=SHEET)           # CHW pumps to TES


    # fan-motor cables from the inlet-chilling e-house round to the tower's north face
    add_route("mvlv_cable", [(305, 1062), (312, 1062), (312, 1326), (60, 1326)], layer="OPT_IC_ROUTES", sheet=SHEET)


def pumpset(x, y, along="y", n=1, step=8, r=1.4):
    for k in range(n):
        px, py = (x + k * step, y) if along == "y" else (x, y + k * step)
        if along == "y":
            box(px - 2.4, px + 2.4, py - 1, py + 14, 0, 1, "concrete")
            rod((px, py, 3), (px, py + 4, 3), r * 1.3, "pump", seg=14)
            box(px - .9, px + .9, py + 4, py + 6, 2.2, 3.8, "amber")                 # coupling guard
            rod((px, py + 6, 3), (px, py + 12, 3), r, "motor", seg=14)
            rod((px, py - 1, 3), (px, py - 3, 3), .8, "pipe", seg=10)                 # suction spool
            rod((px, py + 1.5, 4.5), (px, py + 1.5, 7), .6, "pipe", seg=10)           # discharge
        else:
            box(px - 1, px + 14, py - 2.4, py + 2.4, 0, 1, "concrete")
            rod((px, py, 3), (px + 4, py, 3), r * 1.3, "pump", seg=14)
            box(px + 4, px + 6, py - .9, py + .9, 2.2, 3.8, "amber")
            rod((px + 6, py, 3), (px + 12, py, 3), r, "motor", seg=14)
            rod((px - 1, py, 3), (px - 3, py, 3), .8, "pipe", seg=10)
            rod((px + 1.5, py, 4.5), (px + 1.5, py, 7), .6, "pipe", seg=10)


def tower():
    it = find("Inlet-chilling tower")
    on(it)
    dress(True)
    for c in range(6):
        for r_ in range(2):
            cx, cy = 80 + 40 * c, 1260 + 40 * r_
            for b in range(8):
                a = 2 * math.pi * b / 8 + .4 * c + r_
                rod((cx + 1.8 * math.cos(a), cy + 1.8 * math.sin(a), 50.25),
                    (cx + 14.6 * math.cos(a), cy + 14.6 * math.sin(a), 50.35), .5, "fan", r2=.3, seg=6)
            rod((cx, cy, 50), (cx, cy, 50.03), 15.6, "fanhub", seg=28)                   # open stack (dark throat)
            rod((cx, cy, 50.03), (cx, cy, 50.6), 1.9, "fan", seg=14)                     # hub
            rod((cx, cy, 42), (cx, cy, 44.8), .4, "steel", seg=8)
            box(cx - 1.5, cx + 1.5, cy - 1.5, cy + 1.5, 42, 43.8, "machine")
            rod((cx, cy + 1.5, 43), (cx, cy + 17, 43), .3, "steel", seg=8)              # drive shaft
            rod((cx, cy + 17, 43), (cx, cy + 21, 43), 1.1, "motor", seg=12)
        x0 = 60 + 40 * c + 1.5
        for (y0, y1) in ((1239.7, 1240), (1320, 1320.3)):
            box(x0, x0 + 37, y0, y1, 4, 20, "louvre")                                  # intake louvres
        for k in range(1, 6):
            box(60 + 40 * k - .5, 60 + 40 * k + .5, 1240, 1320, 3, 42, "concrete")    # cell partition walls
    for y in (1241, 1319):
        rod((61, y, 45), (299, y, 45), .07, "rail", seg=4)
    for x in (61, 299):
        rod((x, 1241, 45), (x, 1319, 45), .07, "rail", seg=4)
    for k in range(20):                                                                # access stair, east end
        box(300.5, 304.5, 1244 + k * 1.9, 1245.2 + k * 1.9, 2 * k + 2, 2 * k + 2.3, "grating")
    box(300.5, 304.5, 1282, 1286, 41.7, 42, "grating")
    rod((165, 1236, 4), (165, 1236, 38), 1.3, "waterline", seg=12)                     # hot-water riser and header
    rod((165, 1236, 38), (165, 1241, 38), 1.3, "waterline", seg=12)
    rod((70, 1241.5, 38.5), (290, 1241.5, 38.5), 1.0, "waterline", seg=12)
    dress(False)


def chillers():
    it = find("Chillers x6")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    for k in range(6):                                                                 # chiller packages
        cx = x0 + 15 + (k % 3) * 55
        cy = y0 + 30 + (k // 3) * 60
        box(cx - 14, cx + 14, cy - 6, cy + 6, 0, 1, "concrete")
        rod((cx - 12, cy - 2.6, 4), (cx + 12, cy - 2.6, 4), 2.4, "tank", seg=16)      # evaporator
        rod((cx - 12, cy + 2.6, 4), (cx + 12, cy + 2.6, 4), 2.4, "tank", seg=16)      # condenser
        rod((cx - 6, cy, 8.5), (cx + 4, cy, 8.5), 2.2, "machine", seg=16)              # compressor
        rod((cx + 4, cy, 8.5), (cx + 9, cy, 8.5), 1.8, "motor", seg=14)
        box(cx + 10, cx + 13, cy - 5.5, cy - 2, 1, 7.5, "panel")                       # starter / VFD
        rod((cx - 6, y1 - 4, 25), (cx - 6, y1 - 4, 30), .35, "pipe", seg=8)            # relief vent stack
    for k in range(4):                                                                 # roof exhaust fans
        fx = x0 + 25 + k * 40
        box(fx - 3, fx + 3, (y0 + y1) / 2 - 3, (y0 + y1) / 2 + 3, 25, 27, "machine")
        rod((fx, (y0 + y1) / 2, 27), (fx, (y0 + y1) / 2, 27.4), 2.4, "fan", seg=14)
    for k in range(5):                                                                 # wall louvres (west)
        box(x0 - .2, x0, y0 + 10 + k * 24, y0 + 20 + k * 24, 8, 16, "louvre")
    box(x1, x1 + .2, y0 + 6, y0 + 20, 0, 14, "rollup")                                # roll-up door (east)
    dress(False)


def pumps_and_ehouse():
    it = find("CW pumps (inlet chilling)")
    strip(it)
    on(it)
    dress(True)
    pumpset(256, 1104, along="x", n=4, step=16)
    dress(False)
    it = find("CHW pumps")
    strip(it)
    on(it)
    dress(True)
    pumpset(66, 1193, along="y", n=4, step=20)
    dress(False)
    it = find("Inlet-chilling e-house")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    for ys in (y0 + 6, y1 - 12):                                                       # landings / stairs, east
        box(x1, x1 + 4, ys, ys + 4, 2.2, 2.5, "grating")
        for st in range(4):
            z = 2.2 - .5 * (st + 1)
            box(x1 + 4 + st * .9, x1 + 4.9 + st * .9, ys, ys + 4, z - .1, z, "grating")
        box(x1, x1 + .1, ys + .5, ys + 3.5, 2.5, 9.5, "door")
    box(x0 + 3, x0 + 9, y0 + 3, y0 + 8, 14, 17, "machine")
    rod((x0 + 6, y0 + 5.5, 17), (x0 + 6, y0 + 5.5, 17.3), 1.4, "fan", seg=12)
    dress(False)


def build():
    tower()
    chillers()
    pumps_and_ehouse()
