"""GT1-3 and their generators: the wiring the hall pass left out (owner, Oct 21: "check if there are any wires at the
turbine hall turbines, I feel that we are missing"). The audit found, on each gas turbine, only the exhaust and
wheel-space thermocouple harness, two junction boxes with their conduit, the fuel manifold and lube lines, and on
each GT generator no cable at all, against the steam turbine's probes, servo cables, generator RTD box and heater feed
(st_detail.py). Added here, as on an H-class unit, all typical, not engineered:
- GT: two proximity probes (45 deg) on each bearing with their extension cable to the nearer junction box; servo /
  LVDT cable from both inlet-guide-vane actuators to JB-1; four UV flame detectors on the combustor top with their
  leads to JB-2; an ignition exciter on the deck with two braided igniter leads to the cans;
- GTG: stator RTD / vibration junction box on the east side with its rigid conduit along the GT's conduit run to
  the control-tray drop; two probes on each bearing with their cable; the space-heater MC feed; the DC field leads
  from the collector end down through the deck to the cable vault (static excitation in the electrical gallery).
Everything sits inside the GT / GTG envelopes or on the deck beside them, on the paths the existing conduits use."""
import math

import fuel
from fuel import box, rod, find, on


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def build():
    n = 0
    for k in range(3):
        dx = 160 * k
        cx, cz = 630 + dx, 29.0
        jb1, jb2 = (cx + 9.4, 480.0, 30.0), (cx + 9.4, 515.0, 31.0)               # hall.py junction boxes (west face)
        on(find(f"GT{k + 1}: H-class"))
        fuel.D = True
        # bearing proximity probes, two at 45 deg on top of each bearing, cable down the east side to the JBs
        for (yb, jb) in ((473.5, jb1), (531.0, jb2)):
            rb = 6.4 if yb < 500 else 8.0
            for s in (-1, 1):
                a = math.radians(90 + 45 * s)
                rod((cx + rb * math.cos(a), yb, cz + rb * math.sin(a)),
                    (cx + (rb + .9) * math.cos(a), yb, cz + (rb + .9) * math.sin(a)), .14, "steel", seg=8)
            top = cz + (rb + .9) * math.sin(math.radians(45)) + .4
            poly([(cx - (rb + .9) * .707, yb + .6, top), (cx + (rb + .9) * .707, yb + .6, top),
                  (cx + 9.0, yb + .6, top), (cx + 9.0, yb + .6, jb[2] + 1.0), (cx + 9.0, jb[1], jb[2] + 1.0)],
                 .07, "cable_inst")
            n += 3
        # IGV actuators (hall.py, 25 / 155 deg at r 7.3, y 472.5-475): servo / LVDT cable to JB-1, the west one over
        # the top of the inlet casing
        ae, aw = (cx + 7.3 * math.cos(math.radians(25)), cz + 7.3 * math.sin(math.radians(25))), \
                 (cx + 7.3 * math.cos(math.radians(155)), cz + 7.3 * math.sin(math.radians(155)))
        poly([(ae[0] + .8, 475.4, ae[1]), (cx + 9.2, 475.4, ae[1]), (cx + 9.2, 479.0, ae[1]), (cx + 9.4, 479.0, 31.2)],
             .07, "cable_inst")
        poly([(aw[0] - .8, 475.6, aw[1]), (aw[0] - .8, 475.6, cz + 8.6), (cx + 8.8, 475.6, cz + 8.6),
              (cx + 8.8, 475.6, ae[1]), (cx + 9.2, 475.6, ae[1])], .07, "cable_inst")
        n += 2
        # UV flame detectors on the combustor top (r 8.2), leads to JB-2
        for ang in (60, 80, 100, 120):
            a = math.radians(ang)
            p0 = (cx + 8.3 * math.cos(a), 502.0, cz + 8.3 * math.sin(a))
            p1 = (cx + 9.2 * math.cos(a), 502.0, cz + 9.2 * math.sin(a))
            rod(p0, p1, .2, "steel_dark", seg=8)
            poly([p1, (p1[0], 503.2, cz + 9.6), (cx + 9.8, 503.2, cz + 9.6)], .05, "cable_inst", seg=4)
        poly([(cx + 9.8, 503.2, cz + 9.6), (cx + 9.8, 503.2, 33.0), (cx + 9.8, 515.0, 33.0), (cx + 10.0, 515.0, 32.5)],
             .09, "cable_inst")
        n += 9
        # ignition exciter on the deck east of the combustor, two braided igniter leads to the cans
        box(cx + 9.2, cx + 11.0, 496.0, 498.4, 21.5, 23.6, "panel")
        for (y_, ang) in ((496.6, -15), (497.8, -40)):
            a = math.radians(ang)
            rod((cx + 9.4, y_, 23.0), (cx + 7.9 * math.cos(a), 498.6, cz + 7.9 * math.sin(a)), .09, "steel", seg=6)
        n += 3
        fuel.D = False
        # 480 V power, visible (owner, Oct 21: "is all the power cable there too"): Type MC-HL from the LV / control tray
        # drop beside the aux skid (x 675.6, y 487, EL 30.5) to the skid's two pump motors, a local disconnect at each
        on(find(f"GT{k + 1} aux:"))
        fuel.D = True
        for xm in (664.5 + dx, 671.5 + dx):
            poly([(675.6 + dx, 486.4, 31.2), (675.6 + dx, 477.6, 31.2), (xm, 477.6, 31.2), (xm, 477.6, 29.0),
                  (xm, 476.0, 29.0)], .1, "cable_mc")
            box(xm - .5, xm + .5, 477.9, 478.5, 31.6, 33.0, "panel")                     # local disconnect
        n += 4
        fuel.D = False

        # generator
        gx, gz = 630 + dx, 28.0
        on(find(f"GTG-{k + 1}:"))
        fuel.D = True
        box(gx + 7.2, gx + 8.0, 436.8, 439.2, 24.5, 27.5, "panel")                  # RTD / vibration box
        poly([(gx + 8.0, 438.0, 26.0), (cx + 12.5, 438.0, 26.0), (cx + 12.5, 438.0, 30.5), (cx + 12.5, 479.0, 30.5)],
             .1, "steel")                                                             # conduit to the GT conduit run
        for yb in (414.5, 451.5):                                                    # probes on both bearings
            for s in (-1, 1):
                rod((gx + s * 2.6, yb, 24.0), (gx + s * 2.6, yb, 25.0), .14, "steel", seg=8)
            poly([(gx - 2.6, yb + .3, 25.0), (gx + 2.6, yb + .3, 25.0), (gx + 7.6, yb + .3, 25.0),
                  (gx + 7.6, 437.0 if yb < 430 else 439.0, 25.0)], .07, "cable_inst")
            n += 3
        for yr in (425.0, 433.0, 441.0):                                              # stator RTD leads out of the frame
            poly([(gx + 6.9, yr, 26.5), (gx + 7.4, yr, 26.5), (gx + 7.4, 438.0, 26.5)], .05, "cable_inst", seg=4)
        poly([(gx + 7.6, 436.8, 24.6), (gx + 7.6, 428.0, 24.6), (gx + 7.6, 428.0, 21.6), (gx + 3.0, 428.0, 21.6)],
             .08, "cable_mc")                                                          # space-heater feed
        for (xl, zl) in ((gx - 5.6, gz + .5), (gx - 6.2, gz - .5)):  # DC field leads out of the collector housing,
            poly([(gx - 3.5, 411.8, zl), (xl, 411.8, zl), (xl, 411.8, 20.2)], .14, "cable_tc")  # west of the IPB phases
        box(gx - 6.9, gx - 4.9, 410.8, 412.8, 20.0, 20.25, "steel")                   # deck penetration plate
        n += 8
        fuel.D = False
    return n
