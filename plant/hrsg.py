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
    casing()
    stacks()
    hrsg_cables_and_auxiliaries()


def casing():
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
            box(x0 - .8, x0, y - .35, y + .35, 1.5, 78, "steel")
            box(x1, x1 + .8, y - .35, y + .35, 1.5, 78, "steel")
        for z in (20, 40, 60):
            box(x0 - 1.0, x0 - .8, 601, 759, z - .5, z + .5, "steel")
        # insulated casing panels: thin skins between the buckstays and wale bands, two tones
        ys = [y for y in range(604, 758, 8) if not any(abs(y - b) < 1.5 for b in bands)]
        edges = sorted(set([601] + ys + [759]))
        zs = [1.5, 20, 40, 60, 78]
        for i, (ya, yb) in enumerate(zip(edges, edges[1:])):
            for j, (za, zb) in enumerate(zip(zs, zs[1:])):
                c = "hrsg" if (i + j) % 2 else "hrsg_b"
                box(x0 - .12, x0 - .05, ya + .4, yb - .4, za + .55, zb - .55, c)
                box(x1 + .05, x1 + .12, ya + .4, yb - .4, za + .55, zb - .55, c)
        for y in SECTIONS:                                                      # module seams
            box(x0 - .25, x0, y - .15, y + .15, 1.5, 78, "machine")
            box(x0, x1, y - .15, y + .15, 79, 79.3, "machine")
        # access doors per section (west wall, at grade)
        for y in (622, 655, 700, 735, 752):
            box(x0 - .15, x0, y - 1.5, y + 1.5, 2, 6.5, "door")
        # SCR: catalyst loading doors (three levels), AIG header and lances, CO catalyst door
        for z in (14, 34, 54):
            box(x0 - .2, x0, 673, 683, z, z + 7, "door")
            box(x0 - .3, x0 - .2, 672.6, 683.4, z - .3, z + 7.3, "steel")
        rod((x0 - 2.2, 664, 6), (x0 - 2.2, 664, 74), .55, "pipe", seg=10)       # AIG riser
        for z in range(10, 74, 8):
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
            box(x0 + 2, x0 + 2.6, y - .3, y + .3, 79, 95, "steel")
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
                rod((x, yy - rr * .55, 79), (x, yy - rr * .55, zc - rr * .8), .32, "hrsg", seg=8)
                rod((x, yy + rr * .55, 79), (x, yy + rr * .55, zc - rr * .8), .32, "hrsg", seg=8)
            for xd in (603 + dx, 657 + dx):                                         # downcomers to the lower headers
                pipe([(xd, yy, zc - rr + .3), (xd, yy, 84), (x0 - 2, yy, 84), (x0 - 2, yy, 3)], 84,
                     .9 if rr > 4 else .7, "hrsg")
            for xs in (614 + dx, 646 + dx):                                         # spring safety valves
                rod((xs, yy, zc + rr), (xs, yy, zc + rr + 1.2), .5, "steel", seg=10)
                rod((xs, yy, zc + rr + 1.2), (xs, yy, zc + rr + 3.2), .45, "red", seg=10)
                pipe([(xs, yy, zc + rr + 2.2), (xs + 1.6, yy, zc + rr + 2.2), (xs + 1.6, yy, 104)], 104, .35, "pipe")
                rod((xs + 1.6, yy, 104), (xs + 1.6, yy, 109), .9, "steel", seg=12)   # vent silencer
            rod((628 + dx, yy + rr + .8, zc - 2), (628 + dx, yy + rr + .8, zc + 2), .25, "glass", seg=8)  # level gauge
        # roof handrail
        for (a, b) in (((x0, 601), (x1, 601)), ((x0, 759), (x1, 759)), ((x0, 601), (x0, 759)), ((x1, 601), (x1, 759))):
            rod((a[0], a[1], 82.4), (b[0], b[1], 82.4), .07, "rail", seg=4)
            rod((a[0], a[1], 80.7), (b[0], b[1], 80.7), .05, "rail", seg=4)
        for x in range(int(x0), int(x1) + 1, 6):
            for y in (601, 759):
                rod((x, y, 79), (x, y, 82.4), .05, "rail", seg=4)
        for y in range(601, 760, 6):
            for x in (x0, x1):
                rod((x, y, 79), (x, y, 82.4), .05, "rail", seg=4)
        # steam leads: over the east roof edge, down the north face beside the breeching, to the rack
        for (xl, zr, r, zt) in ((662.2 + dx, 91, 1.25, 27), (659.4 + dx, 92.2, 1.45, 25.5),
                                (656.8 + dx, 93.4, .8, 24)):
            pipe([(xl, 612, 79), (xl, 612, zr), (xl, 762, zr), (xl, 762, zt), (xl, 824, zt)], zr, r, "pipe")
        # feedwater from the boiler feed pumps up the east face to the economizer inlet
        pipe([(676 + dx, 652, 8), (664.6 + dx, 652, 8), (664.6 + dx, 652, 70), (664.6 + dx, 734, 70), (x1, 734, 70)], 70,
             .55, "pipe")
        # GT exhaust expansion joint and inlet-duct stiffener frames
        box(617.6 + dx, 642.4 + dx, 557.5, 560.5, 20.4, 38.6, "fanhub")
        on(find(f"HRSG {k + 1} inlet transition duct"))
        for (yf, x_a, x_b, z_a, z_b) in ((572, 613, 647, 14, 52), (586, 605, 655, 8, 67)):
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


# ---------------------------------------------------------------------------------------
def stacks():
    """Stack dressing that makes the stack, its breeching joint, the CEMS and the cables read
    right: base plinth and access door, caged ladder with rest platforms to the CEMS platform
    (EL 100) and on to the top platform (EL 168), handrails, CEMS probes and a heated sample
    umbilical on a small ladder tray down the stack to the CEMS shelter, aviation-light conduit,
    lightning air terminals and down conductors, and the breeching expansion joint."""
    for k in range(3):
        dx = 160 * k
        gx, gy, r = 630 + dx, 790, 11
        st = find(f"HRSG {k + 1} stack")
        on(st)
        dress(True)
        rod((gx, gy, 0), (gx, gy, 1.5), r + 1.5, "concrete", seg=36)                 # foundation plinth
        box(gx - 2.5, gx + 2.5, gy - r - .15, gy - r + .3, 1.5, 9, "door")           # access door (south)
        # caged ladder on the east side, rest platforms every ~30 ft
        lx, ly = gx + r + 1.0, gy + 2.5
        for (z0, z1) in ((1.5, 100), (101.2, 168)):
            for s_ in (-.7, .7):
                rod((lx, ly + s_, z0), (lx, ly + s_, z1), .07, "steel", seg=4)
            z = z0 + 1
            while z < z1:
                rod((lx, ly - .7, z), (lx, ly + .7, z), .05, "steel", seg=4)
                z += 1
            z = z0 + 8
            while z < z1 - 3:                                                         # cage hoops
                rod((lx + 1.3, ly - .9, z), (lx + 1.3, ly + .9, z), .05, "rail", seg=4)
                rod((lx, ly - .9, z), (lx + 1.3, ly - .9, z), .05, "rail", seg=4)
                rod((lx, ly + .9, z), (lx + 1.3, ly + .9, z), .05, "rail", seg=4)
                z += 4
        for zp in (30, 60, 130):                                                      # rest platforms
            box(lx - .5, lx + 3, ly - 2.5, ly + 2.5, zp - .3, zp, "grating")
            rod((lx + 3, ly - 2.5, zp + 3.4), (lx + 3, ly + 2.5, zp + 3.4), .06, "rail", seg=4)
        for zp in (100, 168):                                                         # platform handrails
            n = 24
            for m in range(n):
                a0, a1 = 2 * math.pi * m / n, 2 * math.pi * (m + 1) / n
                rod((gx + 14.3 * math.cos(a0), gy + 14.3 * math.sin(a0), zp + 1.2 + 3.4),
                    (gx + 14.3 * math.cos(a1), gy + 14.3 * math.sin(a1), zp + 1.2 + 3.4), .07, "rail", seg=4)
                rod((gx + 14.3 * math.cos(a0), gy + 14.3 * math.sin(a0), zp + 1.2),
                    (gx + 14.3 * math.cos(a0), gy + 14.3 * math.sin(a0), zp + 4.6), .05, "rail", seg=4)
        # CEMS probes at EL 103 (four ports) and the probe junction box
        for a in (0.2, 1.77, 3.34, 4.91):
            ca, sa = math.cos(a), math.sin(a)
            rod((gx + r * ca, gy + r * sa, 103), (gx + (r + 1.4) * ca, gy + (r + 1.4) * sa, 103), .35, "steel", seg=8)
            box(gx + (r + 1.4) * ca - .5, gx + (r + 1.4) * ca + .5, gy + (r + 1.4) * sa - .5, gy + (r + 1.4) * sa + .5,
                102.3, 103.7, "panel")
        jx, jy = gx + r + .6, gy + 6.5
        box(jx - .6, jx + .6, jy - 1, jy + 1, 101.2, 104.5, "panel")
        # heated sample umbilical and probe power on a small ladder tray down the stack, then to the shelter
        tx, ty = gx + r + .35, gy + 6.5
        for s_ in (-.5, .5):
            box(tx - .06, tx + .06, ty + s_ - .06, ty + s_ + .06, 10, 101.2, "pipe")
        z = 11
        while z < 101:
            box(tx - .08, tx + .08, ty - .5, ty + .5, z - .05, z + .05, "pipe")
            z += 2
        rod((tx, ty - .2, 10), (tx, ty - .2, 101.2), .16, "pipe", seg=8)               # heated sample line
        rod((tx, ty + .2, 10), (tx, ty + .2, 101.2), .1, "cable_inst", seg=6)          # analyzer signal / power
        pipe([(tx, ty, 10), (648 + dx - 3, ty, 10), (648 + dx - 3, 812, 10), (648 + dx, 812, 10)], 10, .16, "pipe")
        for (y_, z_) in ((ty, 10),):
            for x_ in range(int(tx) + 4, int(648 + dx - 3), 6):                       # sample-line supports
                box(x_ - .2, x_ + .2, y_ - .2, y_ + .2, 0, z_ - .2, "steel")
        # aviation-light conduit and lightning protection
        rod((gx - r - .25, gy, 2), (gx - r - .25, gy, 178), .08, "steel", seg=4)
        for a in (math.pi * .75, math.pi * 1.25):
            rod((gx + (r + .2) * math.cos(a), gy + (r + .2) * math.sin(a), 0),
                (gx + (r + .2) * math.cos(a), gy + (r + .2) * math.sin(a), 180), .06, "copper", seg=4)
        for a in (0, math.pi / 2, math.pi, 1.5 * math.pi):
            rod((gx + 10.5 * math.cos(a), gy + 10.5 * math.sin(a), 180), (gx + 10.5 * math.cos(a),
                gy + 10.5 * math.sin(a), 184), .1, "copper", seg=4)
        # breeching expansion joint and stiffener frames
        on(find(f"HRSG {k + 1} outlet breeching"))
        box(605.5 + dx, 654.5 + dx, 762, 764, 47.5, 78.5, "fanhub")
        for (yf, xa, xb, za, zb) in ((770, 611, 649, 50, 76.5), (776, 616, 644, 52, 75.5)):
            box(xa + dx, xa + dx + .5, yf - .25, yf + .25, za, zb, "steel")
            box(xb + dx - .5, xb + dx, yf - .25, yf + .25, za, zb, "steel")
            box(xa + dx, xb + dx, yf - .25, yf + .25, zb, zb + .5, "steel")
        # CCS diverter damper (optional layer): inlet duct from the stack shell and support steel
        dm = [i for i in fuel.G["items"] if i["name"].startswith(f"DMP-{'ABC'[k]}:")]
        if dm:
            on(dm[0])
            box(621 + dx, 639 + dx, 797, 808, 44, 60, "duct")
            for (xs, ys) in ((614 + dx, 809), (642 + dx, 809), (614 + dx, 825), (642 + dx, 825)):
                box(xs - .6, xs + .6, ys - .6, ys + .6, 0, 40, "steel")
            box(613 + dx, 643 + dx, 808, 826, 39.4, 40, "steel")
            box(612 + dx, 616 + dx, 815, 819, 50, 55, "motor")                             # damper actuator
        dress(False)


def hrsg_cables_and_auxiliaries():
    """Instrument and control cabling up each HRSG, and the auxiliaries that go with it:
    a ladder-tray riser on the south-east corner from the EL 42 control tray to the roof, roof
    junction boxes, cable runs along the drum frame to drum-level transmitter bridles, motor-
    operated stop valves on the steam leads, and a chemical-feed skid (phosphate / amine) at grade."""
    for k in range(3):
        dx = 160 * k
        x1 = 663 + dx
        it = find(f"HRSG {k + 1} + SCR")
        on(it)
        dress(True)
        rx, ry = x1 + 3.2, 605.5
        for s_ in (-.75, .75):                                                        # riser EL 42 -> 79
            box(rx + s_ - .06, rx + s_ + .06, ry - .2, ry + .2, 42, 80, "pipe")
        z = 43
        while z < 80:
            box(rx - .75, rx + .75, ry + .1, ry + .2, z - .08, z + .08, "pipe")
            z += 2
        for m, col in enumerate(("cable_tc", "cable_inst", "cable_inst", "cable_tcx")):
            rod((rx - .5 + m * .33, ry - .05, 42), (rx - .5 + m * .33, ry - .05, 80), .1, col, seg=6)
        box(rx - 1.5, rx + 1.5, ry - 1, ry + 1, 80, 80.3, "grating")
        box(x1 - 6, x1 - 2, 603, 606, 79, 83, "panel")                                # roof junction box
        # cable runs along the drum-frame beam and drum-level bridles at each drum end
        rod((x1 - 3, 606, 88.9), (x1 - 3, 740, 88.9), .2, "cable_inst", seg=6)
        pipe([(x1 - 4, 604.5, 83), (x1 - 3, 604.5, 83), (x1 - 3, 604.5, 88.9), (x1 - 3, 606, 88.9)], 83, .2,
             "cable_inst")
        for (yy, rr) in ((660, 3.4), (700, 4.6), (732, 3.2)):
            zc = 89.2 + rr + 1
            bx = 662.6 + dx
            rod((bx, yy + rr * .6, zc - rr - .5), (bx, yy + rr * .6, zc + rr * .5), .3, "pipe", seg=8)  # bridle
            for zt in (zc - rr * .4, zc + rr * .1):
                box(bx - .3, bx + .3, yy + rr * .6 + .3, yy + rr * .6 + 1, zt - .4, zt + .4, "panel")   # transmitters
            rod((bx, yy + rr * .6 + 1, zc), (x1 - 3, yy + rr * .6 + 1, 88.9), .08, "cable_inst", seg=4)
        # motor-operated stop valves on the steam leads at the roof
        for xl in (662.2 + dx, 659.4 + dx, 656.8 + dx):
            box(xl - .9, xl + .9, 630 - .9, 630 + .9, 90.5 if xl > 661 else (91.7 if xl > 658 else 92.9), 93, "steel")
        for xl, zr in ((662.2 + dx, 91), (659.4 + dx, 92.2), (656.8 + dx, 93.4)):
            box(xl - .7, xl + .7, 629.3, 630.7, zr + 1.3, zr + 3.4, "motor")
        dress(False)
        # chemical-feed skid (phosphate / amine) beside the boiler feed pumps
        fuel.new_item("BASE_POWER_BLOCK", f"HRSG {k + 1} chemical feed skid (phosphate / amine)",
                      (676 + dx, 690 + dx, 668, 680), (0, 9), area="A", sheet="typical (HRSG detail)",
                      info="Dosing tanks and metering pumps for drum phosphate and feedwater amine (typical).")
        box(676 + dx, 690 + dx, 668, 680, 0, .6, "concrete")
        for (cx_, cy_) in ((679.5 + dx, 674), (686.5 + dx, 674)):
            rod((cx_, cy_, .6), (cx_, cy_, 7), 2.6, "tank", seg=16)
        box(677 + dx, 689 + dx, 668.4, 670, .6, 2.4, "pump")
        box(688 + dx, 689.8 + dx, 677, 679.8, .6, 6, "panel")
