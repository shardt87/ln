"""HRSGs at LOD 3: three-pressure reheat, horizontal gas flow (south to north), with SCR.

The drawn envelope is kept (70 x 160 ft casing, top EL 100 on sheet 13); everything here is
dressing on the HRSG items and typical, not engineered:
- casing: external buckstays every 8 ft, wale bands, module seams at the coil-section breaks
  (HP superheater / reheater, HP evaporator, SCR + CO catalyst, HP economizer / IP superheater,
  IP evaporator, LP evaporator / IP economizer, LP economizer), access doors per section;
- SCR: catalyst-loading doors, the ammonia injection grid (AIG) header and lances on the west
  wall, an ammonia vaporization / dilution-air skid at grade, a catalyst-handling monorail on the
  roof;
- drums: dished heads and manways, rows of risers from the roof headers, downcomers at both ends
  down the west wall, two spring safety valves per drum with vent pipes and silencers, level
  gauge columns, a handrail round the roof;
- steam and water: main steam, hot reheat and LP steam leads over the roof edge and down the
  north face to the pipe rack; feedwater from the boiler feed pumps up the east face to the
  economizer;
- GT exhaust expansion joint, inlet-duct stiffeners, stack stiffener rings and CEMS ports, and a
  continuous / intermittent blowdown tank per HRSG.
"""
import math

import fuel
from fuel import box, rod, pipe, find, on


def dress(flag):
    fuel.D = flag


SECTIONS = [640, 668, 688, 712, 725, 745]          # coil-section breaks along the gas path (y)


def build():
    for k in range(3):
        dx = 160 * k
        x0, x1 = 597 + dx, 663 + dx          # casing faces
        it = find(f"HRSG {k + 1} + SCR")
        on(it)
        dress(True)
        bands = set(range(620, 760, 20))
        # buckstays (west and east walls) and wale bands
        for y in range(604, 758, 8):
            if any(abs(y - b) < 1.5 for b in bands):
                continue
            box(x0 - .8, x0, y - .35, y + .35, 1.5, 88, "steel")
            box(x1, x1 + .8, y - .35, y + .35, 1.5, 88, "steel")
        for z in (22, 47, 72):
            box(x0 - 1.0, x0 - .8, 601, 759, z - .5, z + .5, "steel")
        for y in SECTIONS:                                                      # module seams
            box(x0 - .25, x0, y - .15, y + .15, 1.5, 88, "machine")
            box(x0, x1, y - .15, y + .15, 89.2, 89.5, "machine")
        # access doors per section (west wall, at grade)
        for y in (622, 655, 700, 735, 752):
            box(x0 - .15, x0, y - 1.5, y + 1.5, 2, 6.5, "door")
        # SCR: catalyst loading doors (three levels), AIG header and lances, CO catalyst door
        for z in (18, 42, 66):
            box(x0 - .2, x0, 673, 683, z, z + 7, "door")
            box(x0 - .3, x0 - .2, 672.6, 683.4, z - .3, z + 7.3, "steel")
        rod((x0 - 2.2, 664, 6), (x0 - 2.2, 664, 84), .55, "pipe", seg=10)       # AIG riser
        for z in range(10, 84, 8):
            rod((x0 - 2.2, 664, z), (x0 + .4, 664, z), .18, "pipe", seg=6)    # lances
            rod((x0 - 1.4, 664, z - .3), (x0 - 1.4, 664, z + .3), .3, "amber", seg=8)   # balancing valves
        box(x0 - .2, x0, 644, 650, 30, 36, "door")                               # CO catalyst access
        # ammonia vaporization / dilution-air skid at grade, west of the SCR
        box(x0 - 16, x0 - 5, 659, 670, 0, .6, "concrete")
        rod((x0 - 13, 664.5, 2.5), (x0 - 7, 664.5, 2.5), 2, "tank", seg=16)
        rod((x0 - 12, 667.8, .6), (x0 - 12, 667.8, 5.5), 1.2, "fan", seg=14)  # dilution-air blower
        box(x0 - 15.5, x0 - 13.5, 660, 662, .6, 6, "panel")
        pipe([(x0 - 7, 664.5, 2.5), (x0 - 4, 664.5, 2.5), (x0 - 4, 664, 6), (x0 - 2.2, 664, 6)], 2.5, .35, "pipe")
        # catalyst-handling monorail over the SCR section, cantilevered west
        for y in (672, 684):
            box(x0 + 2, x0 + 2.6, y - .3, y + .3, 89.2, 95, "steel")
        box(x0 - 12, x1 - 4, 677.7, 678.3, 95, 96.2, "steel")
        box(x0 - 11, x0 - 9, 676.5, 679.5, 92, 95, "crane")                      # hoist trolley
        # drums: dished heads, manways, risers, downcomers, safety valves and silencers, gauges
        for (yy, rr) in ((660, 3.4), (700, 4.6), (732, 3.2)):
            zc = 89.2 + rr + 1
            for (xa, xb) in ((600 + dx, 598.6 + dx), (660 + dx, 661.4 + dx)):
                rod((xa, yy, zc), (xb, yy, zc), rr, "hrsg", r2=rr * .55, seg=20)   # dished heads
                rod((xb, yy, zc), (xb + (.3 if xb > xa else -.3), yy, zc), rr * .32, "steel", seg=14)   # manway
            for m in range(8):                                                       # risers
                x = 610 + dx + m * 5.7
                rod((x, yy - rr * .55, 89.2), (x, yy - rr * .55, zc - rr * .8), .32, "hrsg", seg=8)
                rod((x, yy + rr * .55, 89.2), (x, yy + rr * .55, zc - rr * .8), .32, "hrsg", seg=8)
            for xd in (603 + dx, 657 + dx):                                         # downcomers to the lower headers
                pipe([(xd, yy, zc - rr + .3), (xd, yy, 88.6), (x0 - 2, yy, 88.6), (x0 - 2, yy, 3)], 88.6,
                     .9 if rr > 4 else .7, "hrsg")
            for xs in (614 + dx, 646 + dx):                                         # spring safety valves
                rod((xs, yy, zc + rr), (xs, yy, zc + rr + 1.2), .5, "steel", seg=10)
                rod((xs, yy, zc + rr + 1.2), (xs, yy, zc + rr + 3.2), .45, "red", seg=10)
                pipe([(xs, yy, zc + rr + 2.2), (xs + 1.6, yy, zc + rr + 2.2), (xs + 1.6, yy, 104)], 104, .35, "pipe")
                rod((xs + 1.6, yy, 104), (xs + 1.6, yy, 109), .9, "steel", seg=12)   # vent silencer
            rod((628 + dx, yy + rr + .8, zc - 2), (628 + dx, yy + rr + .8, zc + 2), .25, "glass", seg=8)  # level gauge
        # roof handrail
        for (a, b) in (((x0, 601), (x1, 601)), ((x0, 759), (x1, 759)), ((x0, 601), (x0, 759)), ((x1, 601), (x1, 759))):
            rod((a[0], a[1], 92.6), (b[0], b[1], 92.6), .07, "rail", seg=4)
            rod((a[0], a[1], 90.9), (b[0], b[1], 90.9), .05, "rail", seg=4)
        for x in range(int(x0), int(x1) + 1, 6):
            for y in (601, 759):
                rod((x, y, 89.2), (x, y, 92.6), .05, "rail", seg=4)
        for y in range(601, 760, 6):
            for x in (x0, x1):
                rod((x, y, 89.2), (x, y, 92.6), .05, "rail", seg=4)
        # steam leads: over the east roof edge, down the north face beside the breeching, to the rack
        for (xl, zr, r, zt) in ((662.2 + dx, 91, 1.25, 27), (659.4 + dx, 92.2, 1.45, 25.5),
                                (656.8 + dx, 93.4, .8, 24)):
            pipe([(xl, 612, 89.2), (xl, 612, zr), (xl, 762, zr), (xl, 762, zt), (xl, 824, zt)], zr, r, "pipe")
        # feedwater from the boiler feed pumps up the east face to the economizer inlet
        pipe([(676 + dx, 652, 8), (664.6 + dx, 652, 8), (664.6 + dx, 652, 84), (664.6 + dx, 734, 84), (x1, 734, 84)], 84,
             .55, "pipe")
        # GT exhaust expansion joint and inlet-duct stiffener frames
        box(617.6 + dx, 642.4 + dx, 557.5, 560.5, 20.4, 38.6, "fanhub")
        on(find(f"HRSG {k + 1} inlet transition duct"))
        for (yf, x_a, x_b, z_a, z_b) in ((572, 613, 647, 14, 60), (586, 605, 655, 8, 75)):
            box(x_a + dx, x_a + dx + .6, yf - .3, yf + .3, z_a, z_b, "steel")
            box(x_b + dx - .6, x_b + dx, yf - .3, yf + .3, z_a, z_b, "steel")
            box(x_a + dx, x_b + dx, yf - .3, yf + .3, z_b, z_b + .6, "steel")
        # stack: stiffener rings, CEMS sampling ports at the platform, a ladder cage
        on(find(f"HRSG {k + 1} stack"))
        gx = 630 + dx
        for z in range(15, 175, 15):
            if abs(z - 100) < 3 or abs(z - 168) < 3:
                continue
            rod((gx, 790, z - .25), (gx, 790, z + .25), 11.25, "steel", seg=36)
        for a in (0.3, 1.9, 3.5):
            rod((gx + 11 * math.cos(a), 790 + 11 * math.sin(a), 103), (gx + 12 * math.cos(a), 790 + 12 * math.sin(a), 103),
                .3, "steel", seg=8)
        dress(False)

        # blowdown tank (continuous / intermittent), west of the LP end
        fuel.new_item("BASE_POWER_BLOCK", f"HRSG {k + 1} blowdown tank (continuous / intermittent)",
                      (576 + dx, 588 + dx, 704 + 0, 716), (0, 16), area="A", sheet="typical (HRSG detail)",
                      info="Atmospheric blowdown tank with vent; drum blowdown and casing drains (typical).")
        box(576 + dx, 588 + dx, 704, 716, 0, .6, "concrete")
        rod((582 + dx, 710, .6), (582 + dx, 710, 13), 5, "tank", seg=20)
        rod((582 + dx, 710, 13), (582 + dx, 710, 14.2), 5, "tank", r2=1.2, seg=20)
        rod((582 + dx, 710, 14.2), (582 + dx, 710, 16), .8, "pipe", seg=10)
        dress(True)
        pipe([(x0 - 2.5, 700, 2), (589 + dx, 700, 2), (589 + dx, 710, 2), (587 + dx, 710, 2)], 2, .3, "pipe")
        rod((582 + dx, 710, 16), (582 + dx, 710, 30), .8, "pipe", seg=10)                      # vent to atmosphere
        dress(False)
