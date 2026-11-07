"""Stormwater pond and wastewater treatment at LOD 3.

Stormwater basin (x 40-320, y 1430-1640, drawn): the banks, floor and permanent pool are built in
build_model.py; this adds the pond's works:
- stormwater pump station on the west bank: pump house, wet well with hatches, suction from the
  outlet structure, discharge to the permitted outfall at the west fence (flap gate, sampling box);
- forebay rock berm across the inlet corner, emergency spillway (riprap) on the south bank;
- 6 ft safety fence round the rim with a maintenance gate and an access ramp down the east bank;
  life ring, depth gauge and signs.
Wastewater treatment (x 620-745, y 1445-1530, drawn as one building): rebuilt as a process area inside
the same footprint and height:
- equalization basin (open concrete, two mixers, walkway), two pH-neutralization tanks with mixers,
  a circular clarifier with its rotating bridge, centre well and effluent launder, a sludge holding tank;
- a smaller building for the filter press, chemical feed (acid / caustic / polymer) and controls;
- process piping between the units and treated effluent to the outfall line.
All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, find, on, strip, pipe


def dress(flag):
    fuel.D = flag


def stormwater():
    it = fuel.new_item("BASE_SERVICES", "Stormwater pump station (2 x 100% submersible pumps)", (6, 38, 1436, 1486), (0, 16),
                       area="F", basis="typical", sheet="typical (ponds detail)",
                       info="Lifts the detention pond to the permitted outfall at the west fence when gravity "
                            "discharge is not available; level-controlled, duty / standby.")
    # pump house
    box(10, 34, 1446, 1466, 0, 1, "concrete")
    box(10.4, 33.6, 1446.4, 1465.6, 1, 13, "building")
    box(10, 34, 1446, 1466, 13, 14, "roof")
    box(33.6, 33.8, 1452, 1460, 1, 9, "rollup")
    box(10.2, 10.4, 1462, 1465, 1, 8, "door")
    for z in (8, 11):
        box(10.2, 10.3, 1450, 1456, z, z + 1.5, "louvre")
    # wet well with hatches and the pump discharge columns
    rod((24, 1476, -14), (24, 1476, 1.2), 6.5, "concrete", seg=24)
    for dx in (-2.5, 2.5):
        box(24 + dx - 1.5, 24 + dx + 1.5, 1474, 1478, 1.2, 1.35, "grating")
        rod((24 + dx, 1476, 1.35), (24 + dx, 1476, 4.5), .55, "pipe", seg=10)
        rod((24 + dx, 1476, 4.5), (24 + dx, 1468, 4.5), .55, "pipe", seg=10)
        rod((24 + dx, 1472, 3.6), (24 + dx, 1472, 5.4), .9, "steel", seg=10)          # check valve
    box(16, 32, 1482, 1484, 0, 6, "panel")                                                # control panel / VFDs
    box(15.5, 32.5, 1481.5, 1484.5, 6, 6.4, "roof")
    # suction from the outlet structure (buried) and discharge to the outfall at the west fence
    rod((48, 1438, -6), (30, 1476, -6), .9, "pipe", seg=10)
    rod((10, 1460, 3), (2, 1460, 3), .7, "pipe", seg=10)
    rod((2, 1460, 3), (2, 1460, -2), .7, "pipe", seg=10)
    box(1.5, 5, 1468, 1472, 0, 3, "concrete")                                             # outfall sampling box
    box(1.6, 4.9, 1468.1, 1471.9, 3, 3.2, "grating")
    fuel.D = True
    it2 = fuel.new_item("BASE_SERVICES", "Stormwater pond works: fence, forebay, spillway, access ramp",
                        (36, 324, 1426, 1644), (-8, 6), area="F", basis="typical", sheet="typical (ponds detail)",
                        register=False)
    # 6 ft safety fence on the rim, maintenance gate on the east side
    for (x0, x1, y0, y1) in ((36, 324, 1426, 1426.3), (36, 324, 1643.7, 1644), (36, 36.3, 1426, 1644),
                             (323.7, 324, 1426, 1515), (323.7, 324, 1545, 1644)):
        box(x0, x1, y0, y1, 0, 6, "fence")
    for y in (1515, 1545):
        box(323.4, 324.3, y - .4, y + .4, 0, 7, "steel")
    # access ramp down the east bank (gravel)
    fuel.G["parts"].append(dict(kind="hex", v=[[304, 1518, -8.3], [320, 1518, -.3], [320, 1542, -.3], [304, 1542, -8.3],
                                               [304, 1518, -8], [320, 1518, 0], [320, 1542, 0], [304, 1542, -8]],
                                color="gravel", item=it2["id"], layer="BASE_SERVICES", d=1))
    # forebay berm of rock across the inlet corner, emergency spillway on the south bank
    for k in range(9):
        box(268 + k * 4, 272 + k * 4, 1588 - k * 3.5, 1592 - k * 3.5, -8, -4.6, "rock")
    box(150, 190, 1430, 1446, -3, -2.6, "rock")
    box(150, 190, 1426, 1430, -2.6, 0, "concrete")
    # depth gauge, life ring, signs
    rod((60, 1450, -8), (60, 1450, 1), .2, "sign", seg=6)
    for z in range(-8, 1, 2):
        box(59.7, 60.3, 1449.6, 1450.4, z - .08, z + .08, "red")
    rod((100, 1426.6, 0), (100, 1426.6, 4.5), .12, "steel", seg=4)
    rod((100, 1427.1, 3.5), (100, 1427.3, 3.5), 1, "hivis_o", seg=12)
    for x in (80, 240):
        box(x, x + 4, 1425.8, 1425.9, 3, 5.5, "sign")
        box(x, x + 4, 1425.75, 1425.8, 4.9, 5.5, "red")
    fuel.D = False
    return it


def wastewater():
    it = find("Wastewater treatment")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    on(it)
    it["info"] = ("Process wastewater (HRSG blowdown, demin regeneration, floor drains after the OWS): "
                  "equalization, pH neutralization, clarification, sludge thickening and filter press; treated "
                  "effluent to the permitted outfall or reuse as cooling-tower make-up. Typical, not engineered.")
    box(x0, x1, y0, y1, 0, .4, "concrete")                                               # process slab
    # building: filter press, chemical feed and controls (north-west part of the footprint)
    box(x0, x0 + 62, y1 - 40, y1, .4, 23.5, "building")
    box(x0, x0 + 62, y1 - 40, y1, 23.5, 25, "roof")
    box(x0 + 20, x0 + 34, y1 - 40.2, y1 - 40, .4, 14, "rollup")
    box(x0 + 40, x0 + 43.5, y1 - 40.2, y1 - 40, .4, 7.5, "door")
    for k in range(3):
        box(x0 + 4 + k * 18, x0 + 12 + k * 18, y1 - 40.2, y1 - 40, 15, 18, "louvre")
    # equalization basin: open concrete tank, two mixers, walkway
    ex0, ex1, ey0, ey1 = x0 + 4, x0 + 56, y0 + 4, y0 + 38
    for (a0, a1, b0, b1) in ((ex0, ex1, ey0, ey0 + 1), (ex0, ex1, ey1 - 1, ey1), (ex0, ex0 + 1, ey0, ey1), (ex1 - 1, ex1, ey0, ey1)):
        box(a0, a1, b0, b1, .4, 9, "concrete")
    box(ex0 + 1, ex1 - 1, ey0 + 1, ey1 - 1, .4, 6.8, "water")
    box(ex0, ex1, (ey0 + ey1) / 2 - 1.5, (ey0 + ey1) / 2 + 1.5, 9, 9.3, "grating")         # walkway
    for xm in (ex0 + 15, ex1 - 15):
        box(xm - 1.2, xm + 1.2, (ey0 + ey1) / 2 - 1.2, (ey0 + ey1) / 2 + 1.2, 9.3, 12, "motor")
        rod((xm, (ey0 + ey1) / 2, 9), (xm, (ey0 + ey1) / 2, 2), .2, "steel", seg=6)
    for yr in ((ey0 + ey1) / 2 - 1.5, (ey0 + ey1) / 2 + 1.5):
        rod((ex0, yr, 12.5), (ex1, yr, 12.5), .06, "rail", seg=4)
    # pH neutralization tanks and the sludge holding tank (south-east)
    for (cx, cy, r, c) in ((x0 + 70, y0 + 11, 5, "tank"), (x0 + 84, y0 + 11, 5, "tank"), (x1 - 9, y0 + 11, 5.5, "tank")):
        rod((cx, cy, .4), (cx, cy, 14), r, c, seg=20)
        rod((cx, cy, 14), (cx, cy, 15.2), r, c, r2=r * .3, seg=20)
        box(cx - .9, cx + .9, cy - .9, cy + .9, 15.2, 17.5, "motor")                        # mixer drive
    pipe([(x0 + 70, y0 + 16, 12), (x0 + 84, y0 + 16, 12)], 12, .35, "pipe")
    # circular clarifier: wall, rotating bridge to the centre well, effluent launder, drive
    ccx, ccy, cr = x0 + 96, y0 + 52, 23
    rod((ccx, ccy, .4), (ccx, ccy, 11), cr, "concrete", seg=40)
    rod((ccx, ccy, 11), (ccx, ccy, 11.05), cr - .8, "water", seg=40)
    rod((ccx, ccy, 10.4), (ccx, ccy, 11.2), cr - 1.2, "concrete", r2=cr - 2.2, seg=40)     # launder
    rod((ccx, ccy, 11), (ccx, ccy, 14), 2.6, "steel", seg=16)                             # centre well / drive
    box(ccx - 1.8, ccx + 1.8, ccy - 1.8, ccy + 1.8, 14, 16.5, "motor")
    box(ccx - cr, ccx, ccy - 1.6, ccy + 1.6, 12.2, 12.6, "grating")                        # bridge
    for yr in (ccy - 1.6, ccy + 1.6):
        rod((ccx - cr, yr, 16), (ccx, yr, 16), .06, "rail", seg=4)
    a = math.radians(30)
    rod((ccx + cr * math.cos(a), ccy + cr * math.sin(a), 9), (x1 + .5, ccy + cr * math.sin(a), 9), .5, "pipe", seg=8)
    # process piping: equalization -> neutralization -> clarifier -> effluent; sludge to the filter press
    pipe([(ex1, y0 + 20, 4), (x0 + 65, y0 + 20, 4), (x0 + 65, y0 + 11, 4)], 4, .45, "pipe")
    pipe([(x0 + 89, y0 + 11, 5), (x0 + 96, y0 + 11, 5), (x0 + 96, ccy - cr - .5, 5)], 5, .45, "pipe")
    pipe([(ccx - 4, ccy, 1.5), (x0 + 65, ccy, 1.5), (x0 + 62, y1 - 30, 1.5)], 1.5, .35, "pipe")
    fuel.G["cur"] = it


def build():
    stormwater()
    wastewater()
