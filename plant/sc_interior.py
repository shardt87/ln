"""SC-1 / SC-2 package interiors (owner, Oct 21: "how about inside the enclosures of simple cycle?"). The generator
and turbine enclosures were solid boxes; they become hollow walls and roofs in their own item ("SC-k package
enclosure"), so a cutaway view can lift them off, with the package inside in a second item:
- generator enclosure: the two-pole generator on its base frame, exciter at the non-drive end, bearing pedestals and
  lube lines, the air-to-water cooler on top, the line-side terminal box with the 13.8 kV leads rising to the wall
  (to the external terminal box over the MV tray), the neutral cubicle, the coupling guard;
- turbine enclosure: the inlet plenum the roof duct drops into, the bellmouth, an LM6000-class engine (LP and HP
  compressor, combustor with its fuel-gas manifold and nozzles and the NOx water-injection ring, HP / LP turbine in
  insulating blankets), the exhaust diffuser into the collector, front and rear mounts on the base frame, the fuel
  line in from the fuel-gas module;
- the wiring a package carries: instrument and thermocouple harnesses along the engine to junction boxes on the
  north wall, an interior ladder tray to the wall penetration, and the enclosure systems: CO2 header and nozzles,
  gas and heat detectors, lights, walkways both sides, a maintenance monorail with its hoist.
Built in drawn coordinates before sc2_mirror.build() (every item is named "SC-k ..."). Typical, not engineered."""
import math

import fuel
from fuel import box, rod, find, new_item, on

L = "OPT_MOD"
YC, ZS = 1205.0, 9.0                                           # package centre line, shaft height


def panel(ax, v0, v1, a0, a1, z0, z1, c, hole=None):
    """A wall slab normal to x (ax 0: v = x, a = y) or y (ax 1: v = y, a = x), minus one rectangular hole
    (ha0, ha1, hz0, hz1)."""
    def B(p0, p1, q0, q1):
        if p1 - p0 < .01 or q1 - q0 < .01:
            return
        if ax == 0:
            box(v0, v1, p0, p1, q0, q1, c)
        else:
            box(p0, p1, v0, v1, q0, q1, c)
    if not hole:
        B(a0, a1, z0, z1)
        return
    ha0, ha1, hz0, hz1 = hole
    B(a0, ha0, z0, z1)
    B(ha1, a1, z0, z1)
    B(ha0, ha1, z0, hz0)
    B(ha0, ha1, hz1, z1)


def walls(k, x):
    """Hollow enclosures in their own item; the solid boxes and the doors leave the unit item."""
    sc = find(f"SC-{k}: aeroderivative")
    it = new_item(L, f"SC-{k} package enclosure (walls and roof)", [x, x + 70, 1192, 1218], [0, 32], area="I",
                  register=False, info="Acoustic enclosure panels and roofs of the generator and turbine compartments; "
                                       "lifted off in the cutaway views. Typical, not engineered.")
    keep = []
    for p in fuel.G["parts"]:
        if p["item"] == sc["id"] and p["kind"] == "box":
            mn = p["min"]
            if (p["color"] == "ehouse" and mn[:3] == [x + .5, 1193, 1.5]) or \
               (p["color"] == "machine" and mn[:3] == [x + 25, 1193, 1.5]) or \
               (p["color"] == "roof" and mn[0] == x + 24.6):
                continue
            if p["color"] == "door" and x + 25 <= mn[0] <= x + 70:
                p["item"] = it["id"]                                           # enclosure doors go with the walls
        keep.append(p)
    fuel.G["parts"][:] = keep
    on(it)
    t = .3
    # generator compartment, x + .5 .. 24, EL 1.5 .. 17
    panel(1, 1193, 1193 + t, x + .5, x + 24, 1.5, 16.7, "ehouse")
    panel(1, 1217 - t, 1217, x + .5, x + 24, 1.5, 16.7, "ehouse")
    panel(0, x + .5, x + .5 + t, 1193 + t, 1217 - t, 1.5, 16.7, "ehouse")
    panel(0, x + 24 - t, x + 24, 1193 + t, 1217 - t, 1.5, 16.7, "ehouse", (YC - 1.5, YC + 1.5, ZS - 1.5, ZS + 1.5))
    box(x + .5, x + 24, 1193, 1217, 16.7, 17.0, "ehouse")
    # turbine compartment, x + 25 .. 69.5, EL 1.5 .. 22, roof EL 22 - 22.6 with the inlet duct coming through it
    panel(1, 1193, 1193 + t, x + 25, x + 69.5, 1.5, 22, "machine")
    panel(1, 1217 - t, 1217, x + 25, x + 69.5, 1.5, 22, "machine")
    panel(0, x + 25, x + 25 + t, 1193 + t, 1217 - t, 1.5, 17.4, "machine", (YC - 1.5, YC + 1.5, ZS - 1.5, ZS + 1.5))
    panel(0, x + 25, x + 25 + t, 1193 + t, 1217 - t, 17.4, 22, "machine", (1198.9, 1211.1, 17.4, 22))
    panel(0, x + 69.5 - t, x + 69.5, 1193 + t, 1217 - t, 1.5, 22, "machine", (1200.5, 1209.5, 4.5, 13.5))
    for (a0, a1, b0, b1) in ((x + 24.6, x + 69.9, 1192.6, 1198.7), (x + 24.6, x + 69.9, 1211.3, 1217.4),
                             (x + 28.3, x + 69.9, 1198.7, 1211.3)):
        box(a0, a1, b0, b1, 22, 22.6, "roof")
    return it


def ring(cx, r, z, rr, c, n=18):
    for j in range(n):
        a0, a1 = 2 * math.pi * j / n, 2 * math.pi * (j + 1) / n
        rod((cx, YC + r * math.cos(a0), z + r * math.sin(a0)), (cx, YC + r * math.cos(a1), z + r * math.sin(a1)), rr, c,
            seg=6)


def interior(k, x):
    import showcase
    it = new_item(L, f"SC-{k} package interior: generator, LM6000-class engine, harnesses", [x + 1, x + 69, 1193.5, 1216.5],
                  [1.5, 21.9], area="I", register=False,
                  info="Inside the enclosures: generator with exciter, cooler and terminal box; the aeroderivative engine "
                       "with fuel and water-injection manifolds; instrument and thermocouple harnesses to the wall "
                       "junction boxes; CO2, gas and heat detection, lights, walkways, maintenance monorail. Typical.")
    fuel.D = True
    n = 0
    # ---------------------------------------------------------------- generator compartment
    box(x + 2, x + 21, 1199.5, 1210.5, 1.5, 2.6, "steel")                           # base frame
    box(x + 5.5, x + 16.5, 1200.6, 1209.4, 2.6, 5.5, "gen_paint")                    # stator feet
    rod((x + 5, YC, ZS), (x + 17, YC, ZS), 4.6, "gen_paint", seg=28)                  # stator frame
    for xe in (x + 4.3, x + 17):
        rod((xe, YC, ZS), (xe + .7, YC, ZS), 4.0, "gen_paint", seg=28)               # end shields
    for (xb0, xb1) in ((x + 3.0, x + 4.2), (x + 17.8, x + 19.0)):
        box(xb0, xb1, YC - 1.4, YC + 1.4, 2.6, ZS + .8, "machine")                   # bearing pedestals
    rod((x + 1.4, YC, ZS), (x + 3.0, YC, ZS), 1.8, "machine", seg=18)                 # exciter (non-drive end)
    box(x + 6, x + 16, 1201.5, 1208.5, 13.6, 15.8, "radiator")                       # air-to-water cooler
    for yp in (1202.5, 1207.5):
        rod((x + 6.5, yp, 15.0), (x + 1.4, yp, 15.0), .2, "cw", seg=8)               # cooler water to the wall
        rod((x + 1.4, yp, 15.0), (x + 1.4, yp, 2.6), .2, "cw", seg=8)
    box(x + 9, x + 15, 1209.4, 1213.0, 3.5, 9.0, "panel")                            # line-side terminal box
    for dx in (-.9, 0, .9):                                                           # 13.8 kV leads up to the wall
        rod((x + 12 + dx, 1212.0, 9.0), (x + 12 + dx, 1212.0, 12.0), .22, "cable_mv", seg=8)
        rod((x + 12 + dx, 1212.0, 12.0), (x + 12 + dx, 1216.5, 12.0), .22, "cable_mv", seg=8)
    box(x + 16.5, x + 19.5, 1210.0, 1212.5, 2.6, 7.0, "panel")                       # neutral cubicle / CTs
    rod((x + 3.6, 1207.6, 2.8), (x + 18.4, 1207.6, 2.8), .15, "pipe", seg=8)           # lube supply to the bearings
    for xb in (x + 3.6, x + 18.4):
        rod((xb, 1207.6, 2.8), (xb, YC + 1.2, ZS - .4), .12, "pipe", seg=6)
    rod((x + 19, YC, ZS), (x + 33, YC, ZS), .55, "steel", seg=14)                     # drive shaft to the engine front
    box(x + 21.4, x + 23.5, YC - 1.4, YC + 1.4, ZS - 1.4, ZS + 1.4, "amber")         # coupling guard
    box(x + 25.5, x + 26.0, YC - 1.4, YC + 1.4, ZS - 1.4, ZS + 1.4, "amber")
    for xl in (x + 6, x + 18):
        box(xl - .7, xl + .7, 1197.5, 1198.5, 16.3, 16.6, "lamp")
    n += 24
    # ---------------------------------------------------------------- turbine compartment
    box(x + 27, x + 68, 1199, 1211, 1.5, 2.0, "steel")                                # package base frame
    box(x + 26, x + 31, 1197, 1213, 2.0, 17.3, "duct")                                # inlet plenum (roof duct above)
    rod((x + 31, YC, ZS), (x + 33, YC, ZS), 3.6, "gt_cold", r2=2.7, seg=28)          # bellmouth
    stages = ((x + 33, x + 37, 2.7, 2.5, "gt_cold"),                                  # LP compressor
              (x + 37, x + 45, 2.3, 1.8, "gt_cold"),                                  # HP compressor
              (x + 45, x + 49, 2.6, 2.6, "gt_blanket"),                               # combustor (blanketed)
              (x + 49, x + 51, 2.4, 2.4, "gt_blanket"),                               # HP turbine
              (x + 51, x + 57, 2.6, 3.2, "gt_comb"),                                  # LP turbine
              (x + 57, x + 69.0, 3.3, 4.3, "duct"))                                   # exhaust diffuser
    for (a, b, r0, r1, c) in stages:
        rod((a, YC, ZS), (b, YC, ZS), r0, c, r2=r1, seg=28)
        rod((a - .12, YC, ZS), (a + .12, YC, ZS), max(r0, r1) + .25, "steel", seg=28)  # casing flange
        n += 2
    for xm in (x + 35, x + 56):                                                       # front / rear mounts
        box(xm - .6, xm + .6, YC - 2.2, YC + 2.2, 2.0, ZS - 2.4, "steel")
        rod((xm, YC - 2.2, ZS - 2.4), (xm, YC - 1.6, ZS - 1.6), .2, "steel", seg=6)
        rod((xm, YC + 2.2, ZS - 2.4), (xm, YC + 1.6, ZS - 1.6), .2, "steel", seg=6)
    ring(x + 46.2, 3.25, ZS, .2, "fuelgas")                                           # fuel-gas manifold
    for j in range(15):                                                               # fuel nozzles
        a = 2 * math.pi * j / 15
        rod((x + 46.2, YC + 3.25 * math.cos(a), ZS + 3.25 * math.sin(a)),
            (x + 46.6, YC + 2.65 * math.cos(a), ZS + 2.65 * math.sin(a)), .1, "fuelgas", seg=6)
    ring(x + 47.4, 3.55, ZS, .14, "cw")                                               # NOx water-injection ring
    for (xp, xr, yl, c, rr) in ((x + 42, x + 46.2, YC - 1.5, "fuelgas", .28), (x + 40, x + 47.4, YC - 2.3, "cw", .2)):
        rod((xp, 1193.5, 3.6), (xp, yl, 3.6), rr, c, seg=8)                         # supply lines from the south wall
        rod((xp, yl, 3.6), (xr, yl, 3.6), rr, c, seg=8)
        rod((xr, yl, 3.6), (xr, yl, ZS - 2.8), rr, c, seg=8)
    n += 40
    # harnesses: along the engine top to three junction boxes on the north wall, an interior tray to the penetration
    jbs = ((x + 35, "JB-1  COMPRESSOR"), (x + 47, "JB-2  COMBUSTOR"), (x + 56, "JB-3  TURBINE / TC"))
    for (xj, t) in jbs:
        box(xj - 1.2, xj + 1.2, 1215.9, 1216.6, 8.5, 12.0, "panel")
        showcase.decal((xj, 1215.85, 12.5), (0, -1, 0), 2.4, .5, [(t, .5, True, "#111111")], bg="#f2c21b")
    rod((x + 34, YC + .9, ZS + 2.75), (x + 56, YC + .9, ZS + 2.75), .12, "cable_inst", seg=8)   # engine harness
    rod((x + 34, YC - .9, ZS + 2.75), (x + 56, YC - .9, ZS + 2.75), .12, "cable_tcx", seg=8)
    for xc in range(int(x + 35), int(x + 57), 3):                                    # harness clips
        box(xc - .1, xc + .1, YC - 1.2, YC + 1.2, ZS + 2.55, ZS + 2.65, "steel")
    for (xj, _), c in zip(jbs, ("cable_inst", "cable_inst", "cable_tcx")):           # harness to each JB
        rod((xj, YC + .9, ZS + 2.75), (xj, 1215.8, 10.0), .14, c, seg=8)
    Y0, Y1, ZT = 1214.6, 1216.5, 15.0                                                 # interior ladder tray, north wall
    box(x + 28, x + 66, Y0, Y0 + .1, ZT - .3, ZT + .1, "pipe")
    box(x + 28, x + 66, Y1 - .1, Y1, ZT - .3, ZT + .1, "pipe")
    for xr in range(int(x + 29), int(x + 66), 2):
        box(xr - .05, xr + .05, Y0, Y1, ZT - .3, ZT - .22, "pipe")
    for j, c in enumerate(("cable_inst", "cable_tcx", "cable_tc", "cable_fo")):
        rod((x + 28, Y0 + .35 + j * .4, ZT - .1), (x + 66, Y0 + .35 + j * .4, ZT - .1), .12, c, seg=6)
    for (xj, _) in jbs:
        rod((xj, 1216.2, 12.0), (xj, 1216.2, ZT - .3), .15, "cable_inst", seg=6)     # JB home runs up to the tray
    box(x + 26.2, x + 27.6, 1215.2, 1216.6, 13.5, 16.5, "panel")                     # wall penetration / transit
    n += 30
    # enclosure systems
    rod((x + 30, 1210.5, 21.3), (x + 67, 1210.5, 21.3), .2, "red", seg=8)            # CO2 header
    for xn in (x + 34, x + 44, x + 54, x + 64):
        rod((xn, 1210.5, 21.3), (xn, 1210.5, 20.6), .08, "red", seg=6)
        rod((xn, 1210.5, 20.6), (xn, 1210.5, 20.4), .2, "steel", seg=8)              # nozzle
    for (xd, c) in ((x + 40, "amber"), (x + 52, "amber"), (x + 62, "panel"), (x + 33, "panel")):
        box(xd - .3, xd + .3, 1199.5, 1200.1, 21.2, 21.9, c)                         # gas (amber) / heat detectors
    for xl in (x + 32, x + 44, x + 56, x + 66):
        for yl in (1198.5, 1211.5):
            box(xl - .8, xl + .8, yl - .3, yl + .3, 21.6, 21.9, "lamp")
    for (y0, y1) in ((1193.5, 1197.4), (1213.0, 1214.4)):                            # walkways
        box(x + 31.5, x + 68.5, y0, y1, 1.5, 1.8, "grating")
    box(x + 30, x + 68, YC - .3, YC + .3, 20.6, 21.3, "crane")                      # maintenance monorail
    for xs in (x + 32, x + 50, x + 66):
        rod((xs, YC, 21.3), (xs, YC, 21.9), .1, "steel", seg=6)
    box(x + 49.2, x + 50.8, YC - .7, YC + .7, 19.7, 20.6, "crane")                  # trolley hoist
    rod((x + 50, YC, 19.7), (x + 50, YC, 15.5), .04, "steel", seg=4)
    box(x + 49.6, x + 50.4, YC - .3, YC + .3, 15.0, 15.5, "crane")                  # hook block
    n += 30
    fuel.D = False
    return n


def build():
    n = 0
    for k, x in enumerate((1910, 2110), 1):
        n += interior(k, x)
    return n
