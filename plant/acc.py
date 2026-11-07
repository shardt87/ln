"""Air-cooled condenser at LOD 3 (detail cycle 3).

80 cells (8 streets x 10 cells of 40 ft), fan deck EL 88-92, top of steel EL 125 (sheet 13). The
drawn steel, bundles, wind walls and steam ducts stay; this adds, as dressing:
- each cell: inlet bell (fan ring) under the deck, a 9-blade fan with hub inside the shroud, the
  motor and right-angle gearbox on a fan bridge under the deck, a vibration switch box;
- fan-bridge cable ladders: one per street under the deck, fed from R4 (the VFDs) by a riser at
  the south end, with a drop to every motor;
- condensate drain headers along both lower edges of every street's A-frame, draining to a
  collector at the north end;
- deck structure: girders between the column heads under the deck, X-bracing in the end bays of
  the north and east faces, a perimeter handrail on the fan deck;
- the vacuum (air-removal) pumps and the auxiliary dry coolers: skids, motors, separators,
  fin-fan bundles with fans.
All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, find, on


def dress(flag):
    fuel.D = flag


def cells():
    acc = find("Air-cooled condenser")
    on(acc)
    dress(True)
    for i in range(8):
        sx = 1150 + 40 * i
        for j in range(10):
            cx, cy = sx, 400 + 40 * j
            rod((cx, cy, 84.5), (cx, cy, 88), 18.2, "fanhub", r2=17.2, seg=28)       # inlet bell under the deck
            for b in range(9):                                                       # fan blades
                a = 2 * math.pi * b / 9 + .2 * j
                rod((cx + 2.2 * math.cos(a), cy + 2.2 * math.sin(a), 95.6),
                    (cx + 15.6 * math.cos(a), cy + 15.6 * math.sin(a), 95.9), .5, "fan", r2=.35, seg=6)
            rod((cx, cy, 94.8), (cx, cy, 96.4), 2.1, "fanhub", seg=16)              # hub
            rod((cx, cy, 88), (cx, cy, 94.8), .5, "steel", seg=8)                    # drive shaft
            box(cx - 2, cx + 2, cy - 2, cy + 2, 84, 87.6, "machine")                 # right-angle gearbox
            rod((cx + 2, cy, 85.8), (cx + 8.5, cy, 85.8), 1.5, "motor", seg=14)      # motor
            box(cx - 9, cx + 9, cy - .5, cy + .5, 83.4, 84, "steel")                 # fan bridge beam
            box(cx + 2.5, cx + 3.3, cy - 2.3, cy - 1.7, 85, 86.2, "panel")           # vibration switch
            rod((cx + 6, cy, 84.3), (cx + 6, cy - 9, 84.3), .12, "cable_tc", seg=4)   # motor drop to the ladder
            rod((cx + 6, cy - 9, 84.3), (cx + 6, cy - 9, 84.9), .12, "cable_tc", seg=4)
        # fan-bridge cable ladder along the street, 9 ft south of each fan row centre line
        lx = sx + 6
        for s in (-.7, .7):
            box(lx + s - .06, lx + s + .06, 382, 778, 84.9, 85.3, "pipe")
        y = 383
        while y < 777:
            box(lx - .7, lx + .7, y - .08, y + .08, 84.9, 85.0, "pipe")
            y += 2
        for c in range(4):
            rod((lx - .45 + c * .3, 382, 85.1), (lx - .45 + c * .3, 778, 85.1), .1, "cable_tc", seg=6)
        # condensate drain headers along both lower edges of the A-frame, to a collector at the north end
        for ex in (sx - 18, sx + 18):
            rod((ex, 384, 92.8), (ex, 776, 92.4), .55, "pipe", seg=10)
        rod((sx - 18, 776.5, 92.4), (sx + 18, 776.5, 92.4), .7, "pipe", seg=10)
    # riser from R4 to the deck at the south-west corner, then a header ladder along the south edge
    rx, ry = 1136.5, 376
    for s in (-.75, .75):
        box(rx + s - .06, rx + s + .06, ry - .2, ry + .2, 16, 85.3, "pipe")
    z = 17
    while z < 85:
        box(rx - .75, rx + .75, ry + .1, ry + .2, z - .08, z + .08, "pipe")
        z += 2
    for c in range(5):
        rod((rx - .5 + c * .25, ry - .05, 16), (rx - .5 + c * .25, ry - .05, 85.2), .1, "cable_tc", seg=6)
    for s in (-.7, .7):
        box(1136, 1438, 383 + s - .06, 383 + s + .06, 84.9, 85.3, "pipe")
    # girders between column heads under the deck
    for cx in range(1130, 1451, 40):
        box(cx - .6, cx + .6, 380, 780, 86, 88, "steel")
    for cy in range(380, 781, 40):
        box(1130, 1450, cy - .6, cy + .6, 86.6, 88, "steel")
    # X-bracing in the end bays of the north and east faces
    for (x0, x1) in ((1290, 1330), (1410, 1450)):        # clear of the LV tray leaving north at x 1140
        rod((x0, 780, 2), (x1, 780, 84), .35, "steel", seg=6)
        rod((x1, 780, 2), (x0, 780, 84), .35, "steel", seg=6)
    for (y0, y1) in ((620, 660), (740, 780)):
        rod((1450, y0, 2), (1450, y1, 84), .35, "steel", seg=6)
        rod((1450, y1, 2), (1450, y0, 84), .35, "steel", seg=6)
    # fan-deck perimeter handrail (inside the wind wall)
    for (a, b) in (((1131, 381), (1449, 381)), ((1131, 779), (1449, 779)), ((1131, 381), (1131, 779)),
                   ((1449, 381), (1449, 779))):
        rod((a[0], a[1], 95.4), (b[0], b[1], 95.4), .07, "rail", seg=4)
    dress(False)


def vacuum_and_coolers():
    vac = find("VAC-A/B")
    x0, x1, y0, y1 = vac["fp"]
    on(vac)
    dress(True)
    for k, x in enumerate((x0 + 7, x0 + 21)):
        box(x - 5, x + 5, y0 + 3, y0 + 17, 0, .8, "steel")
        rod((x, y0 + 5, 3), (x, y0 + 11, 3), 2, "pump", seg=16)                   # liquid-ring pump
        rod((x, y0 + 11.3, 3), (x, y0 + 15.5, 3), 1.6, "motor", seg=14)
        rod((x + 3.4, y0 + 8, .8), (x + 3.4, y0 + 8, 7.6), 1.2, "tank", seg=14)   # separator
    dress(False)
    aux = find("Aux dry coolers")
    x0, x1, y0, y1 = aux["fp"]
    on(aux)
    dress(True)
    for k in range(12):
        x = x0 + 5 + k * 10
        rod((x, (y0 + y1) / 2, 17.4), (x, (y0 + y1) / 2, 18), 4.2, "fan", seg=20)
        rod((x, (y0 + y1) / 2, 18), (x, (y0 + y1) / 2, 18.4), .9, "fanhub", seg=10)
    rod((x0 + 1, y0 + 2, 6), (x1 - 1, y0 + 2, 6), .7, "pipe", seg=10)          # CCW supply / return headers
    rod((x0 + 1, y0 + 4, 6), (x1 - 1, y0 + 4, 6), .7, "pipe", seg=10)
    dress(False)


def build():
    cells()
    vacuum_and_coolers()
