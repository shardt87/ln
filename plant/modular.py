"""Modular power yard at LOD 3 (SK-3X1-07): the RICE engine hall with its 8 engine-generators,
exhaust trains and radiators, and the two aeroderivative simple-cycle units.

Drawn footprints, envelopes and sheet-13 heights are kept (RICE stacks 90 ft, aero stacks 80 ft);
the equipment inside them is typical, not engineered:
- RICE engines: V18 block on a base frame, two cylinder-head banks, charge-air manifold,
  two turbochargers at the free end, flywheel housing and generator with terminal box;
  exhaust from each turbocharger through the south wall to an SCR on a steel stand, a
  silencer and the stack (platform, ladder); radiator bays with fan shrouds and coolant headers;
  overhead crane inside the hall;
- simple-cycle units: inlet filter house on legs, generator and turbine enclosures on a skid,
  exhaust collector, SCR / CO catalyst housing with ammonia injection, access platforms and
  stair, outlet duct, stack platform and ladder; fin-fan lube-oil cooler.

Uses the primitives in fuel.py; run after fuel.build().
"""
import math

import fuel
from fuel import box, rod, pipe, find, strip, on


def dress(flag):
    fuel.D = flag


def ladder(x, y, z0, z1, along="x"):
    dx, dy = (.7, 0) if along == "x" else (0, .7)
    for s in (-1, 1):
        rod((x + s * dx, y + s * dy, z0), (x + s * dx, y + s * dy, z1), .08, "steel", seg=4)
    z = z0 + 1
    while z < z1:
        rod((x - dx, y - dy, z), (x + dx, y + dy, z), .05, "steel", seg=4)
        z += 1
    ox, oy = (0, -1.3) if along == "x" else (-1.3, 0)             # cage on the outer side
    for k in range(int((z1 - z0 - 8) // 4)):
        zc = z0 + 8 + 4 * k
        rod((x - dx + ox, y - dy + oy, zc), (x + dx + ox, y + dy + oy, zc), .05, "rail", seg=4)


def stack_dress(cx, cy, r, top, plat):
    """Platform ring with handrail at `plat`, caged ladder, cap ring."""
    rod((cx, cy, plat - .3), (cx, cy, plat), r + 3, "grating", seg=24)
    n = 16
    for k in range(n):                                         # handrail: a ring of segments, not a disc
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        rr = r + 2.9
        rod((cx + rr * math.cos(a0), cy + rr * math.sin(a0), plat + 3.45),
            (cx + rr * math.cos(a1), cy + rr * math.sin(a1), plat + 3.45), .07, "rail", seg=4)
    for k in range(8):
        a = k * math.pi / 4
        x, y = cx + (r + 2.9) * math.cos(a), cy + (r + 2.9) * math.sin(a)
        rod((x, y, plat), (x, y, plat + 3.5), .06, "rail", seg=4)
    rod((cx, cy, top - .8), (cx, cy, top), r + .35, "steel", seg=24)
    rod((cx + r + .9, cy, .5), (cx + r + .9, cy, plat), .08, "steel", seg=4)
    rod((cx + r + .9, cy + 1.4, .5), (cx + r + .9, cy + 1.4, plat), .08, "steel", seg=4)
    z = 2
    while z < plat:
        rod((cx + r + .9, cy, z), (cx + r + .9, cy + 1.4, z), .05, "steel", seg=4)
        z += 1.5
    for (zp, rr) in ((plat * .35, r + .25), (plat * .7, r + .25)):     # sampling-port / stiffener rings
        rod((cx, cy, zp), (cx, cy, zp + .4), rr, "steel", seg=24)


# ---------------------------------------------------------------------------------------
def rice():
    hall = find("RICE engine hall")
    x0h, x1h, y0h, y1h = hall["fp"]
    # overhead crane inside the hall: runway beams and one bridge
    on(hall)
    dress(True)
    for y in (y0h + 3, y1h - 3):
        box(x0h + 1, x1h - 1, y - .6, y + .6, 29, 30.2, "steel")
        for x in range(int(x0h) + 10, int(x1h), 28):
            box(x - .5, x + .5, y - .5, y + .5, 0, 29, "steel")
    box(1688, 1692, y0h + 2, y1h - 2, 30.2, 32.4, "crane")
    box(1686, 1694, 1083, 1089, 28.6, 30.2, "crane")
    # eave gutter and downpipes along both long walls
    for y in (y0h - .5, y1h + .5):
        box(x0h, x1h, y - .4, y + .4, 33.4, 34.2, "steel")
    dress(False)

    for k in range(8):
        x = 1581 + 28 * k
        xc = x + 9.5
        # ---- engine-generator (inside the hall)
        eg = find(f"RICE engine-generator {k + 1}")
        strip(eg)
        eg["info"] = ("Medium-speed V18 gas engine with generator on a common base frame: two cylinder-head "
                      "banks, charge-air manifold in the V, two turbochargers at the free end (typical).")
        box(x, x + 19, 1055, 1115, 0, 3, "concrete")
        box(x + 2, x + 17, 1058, 1112, 3, 4.5, "steel")                      # common base frame
        box(x + 4, x + 15, 1062, 1094, 4.5, 12, "machine")                    # crankcase / block
        for xb in (x + 3, x + 11):                                            # cylinder banks
            box(xb, xb + 5, 1063, 1093, 12, 14.6, "machine")
            for c in range(9):
                yc = 1063.6 + c * 3.25
                box(xb + .4, xb + 4.6, yc, yc + 2.6, 14.6, 15.8, "motor")      # head covers
        rod((xc, 1063, 14), (xc, 1093, 14), 1.2, "machine", seg=14)          # charge-air manifold
        for xt in (x + 5.5, x + 13.5):                                        # turbochargers
            rod((xt, 1057.5, 13.5), (xt, 1062, 13.5), 2.3, "steel", seg=18)
            rod((xt, 1062, 13.5), (xt, 1063, 13.5), 1.6, "machine", seg=14)
        rod((xc, 1094, 11), (xc, 1096, 11), 6.2, "steel", seg=24)            # flywheel housing
        rod((xc, 1096, 11), (xc, 1112, 11), 7, "machine", seg=24)            # generator
        rod((xc, 1111.6, 11), (xc, 1112.6, 11), 4.5, "machine", seg=20)
        box(x + 15.5, x + 18.5, 1100, 1107, 9, 15.5, "steel")                 # terminal box
        for yf in (1099, 1109):
            box(x + 4, x + 15, yf - 1, yf + 1, 3, 5, "steel")                   # generator feet

        # ---- exhaust train outside the south wall
        ex = find(f"RICE {k + 1} SCR")
        strip(ex)
        ex["info"] = ("Exhaust from the turbochargers through the south wall to an SCR + oxidation catalyst "
                      "on a steel stand, a silencer and the 90 ft stack (Weston ~65 ft; Humboldt Bay 100 ft).")
        box(x - 1, x + 21, 1000, 1030, 0, 1, "concrete")
        for xl in (x + 1.5, x + 18.5):
            for yl in (1003, 1027):
                box(xl - .4, xl + .4, yl - .4, yl + .4, 1, 12, "steel")
        box(x + 1, x + 19, 1002, 1028, 11.4, 12, "steel")
        box(x + 1.5, x + 18.5, 1002.5, 1027.5, 12, 22, "equip")               # SCR + oxidation catalyst
        box(x + 1, x + 19, 1002, 1028, 22, 22.4, "steel")
        rod((xc, 1004, 26.4), (xc, 1026, 26.4), 4.2, "equip", seg=22)        # silencer
        for ys in (1007, 1023):
            box(xc - 3, xc + 3, ys - .5, ys + .5, 22.4, 23.6, "steel")
        rod((xc, 1026, 26.4), (xc, 1034.2, 26.4), 2.2, "duct", seg=16)       # silencer -> stack
        rod((x + 3.5, 1040, 28), (x + 3.5, 1025.6, 28), 1.6, "duct", seg=14) # hall wall -> SCR
        rod((x + 3.5, 1025.6, 28), (x + 3.5, 1025.6, 22.2), 1.6, "duct", seg=14)
        rod((x + 3.5, 1036, 28), (x + 3.5, 1035, 28), 1.95, "steel", seg=14)  # expansion joint
        box(x + 7, x + 13, 1034, 1040, 0, 1.2, "concrete")                    # stack plinth
        rod((xc, 1037, 0), (xc, 1037, 90), 3, "stack", seg=16)
        box(x + 15, x + 20, 1029.6, 1032, 1, 7, "panel")                      # urea dosing cabinet
        dress(True)
        pipe([(x + 17.5, 1030.8, 4), (x + 17.5, 1030.8, 22.6), (x + 16, 1026, 22.6)], 4, .12, "pipe")
        # exhaust riser from the turbochargers inside the hall
        pipe([(x + 5.5, 1057.5, 13.5), (x + 5.5, 1054, 13.5), (x + 5.5, 1054, 28), (x + 3.5, 1054, 28),
              (x + 3.5, 1040, 28)], 28, 1.4, "duct")
        pipe([(x + 13.5, 1057.5, 13.5), (x + 13.5, 1052, 13.5), (x + 13.5, 1052, 26), (x + 5.5, 1052, 26),
              (x + 5.5, 1052, 27)], 26, 1.2, "duct")
        # SCR access: platform, rail, ladder
        box(x + 18.5, x + 21, 1003, 1027, 21.8, 22.2, "grating")
        for yy in (1003, 1015, 1027):
            rod((x + 21, yy, 22.2), (x + 21, yy, 25.6), .06, "rail", seg=4)
        rod((x + 21, 1003, 25.6), (x + 21, 1027, 25.6), .07, "rail", seg=4)
        ladder(x + 20.4, 1001, 1, 22, along="y")
        stack_dress(xc, 1037, 3, 90, 62)
        dress(False)

        # ---- radiators: shrouded fans, coolant headers from the hall
        rd = find(f"RICE {k + 1} radiators")
        dress(True)
        on(rd)
        for r_ in range(5):
            yc = 1146 + 16 * r_
            rod((x + 10, yc, 8.9), (x + 10, yc, 10.2), 5.4, "steel", seg=24)    # shroud
            rod((x + 10, yc, 10.2), (x + 10, yc, 10.5), 1.0, "motor", seg=12)
            box(x - 1, x + .4, 1140 + 16 * r_, 1152 + 16 * r_, 3.6, 7.4, "steel")  # headers
            box(x + 19.6, x + 21, 1140 + 16 * r_, 1152 + 16 * r_, 3.6, 7.4, "steel")
        for xp in (x + 4, x + 15):                                            # jacket-water supply / return
            pipe([(xp, 1130, 2.5), (xp, 1214, 2.5)], 2.5, .45, "pipe")
            for r_ in range(5):
                pipe([(xp, 1146 + 16 * r_, 2.5), (xp, 1146 + 16 * r_, 3.6)], 3, .3, "pipe", elbows=False)
        dress(False)


def simple_cycle():
    for k, x in enumerate((1910, 2110), 1):
        sc = find(f"SC-{k}: aeroderivative")
        strip(sc)
        sc["info"] = ("LM6000-class package: inlet filter house on legs at the west end, generator and turbine "
                      "enclosures on one skid, exhaust collector into the SCR and CO catalyst, 80 ft stack "
                      "(Mira Loma permit); CEMS, PCM with 15 kV GCB, lube-oil fin-fan cooler, CO2 fire suppression.")
        box(x, x + 70, 1192, 1218, 0, 1.5, "steel")                            # package skid
        box(x + .5, x + 24, 1193, 1217, 1.5, 17, "ehouse")                      # generator enclosure
        box(x + 25, x + 69.5, 1193, 1217, 1.5, 22, "machine")                  # turbine enclosure
        box(x + 24.6, x + 69.9, 1192.6, 1217.4, 22, 22.6, "roof")
        for xl in (x - 18.5, x - 1.5):                                          # filter house legs
            for yl in (1197.5, 1212.5):
                box(xl - .4, xl + .4, yl - .4, yl + .4, 0, 8, "steel")
        box(x - 20, x, 1196, 1214, 8, 26, "filter")                            # inlet filter house
        box(x - 20.4, x + .4, 1195.6, 1214.4, 26, 26.6, "roof")
        box(x, x + 12, 1199, 1211, 17, 24, "duct")                              # inlet plenum duct
        # exhaust collector: drawn 20 x 30 ft box, a loft from the enclosure to the SCR face
        box(x + 70, x + 90, 1190, 1220, 0, 1, "concrete")
        fuel.G["parts"].append(dict(kind="hex", v=[[x + 70, 1198, 6], [x + 70, 1212, 6], [x + 70, 1212, 18],
                                                   [x + 70, 1198, 18], [x + 90, 1191, 3], [x + 90, 1219, 3],
                                                   [x + 90, 1219, 32], [x + 90, 1191, 32]],
                                    color="duct", item=sc["id"], layer=sc["layer"]))
        for xs in (x + 74, x + 86):
            box(xs - .5, xs + .5, 1193, 1217, 1, 4.5, "steel")
        dress(True)
        for xd in (x + 30, x + 52):                                             # enclosure doors
            for y, s in ((1193, -1), (1217, 1)):
                box(xd, xd + 4, y, y + s * .15, 1.5, 9, "door")
        for xb in range(x + 6, x + 20, 3):                                      # CO2 cylinders
            rod((xb, 1190.2, 1.5), (xb, 1190.2, 7), .5, "red", seg=10)
        # filter-change platform on the west face, reached by a ladder
        box(x - 23, x - 20, 1198, 1212, 24.6, 25, "grating")
        rod((x - 23, 1198, 28.4), (x - 23, 1212, 28.4), .07, "rail", seg=4)
        ladder(x - 23.6, 1196.5, 1, 24.6, along="y")
        dress(False)

        # SCR / CO catalyst housing
        scr = find(f"SC-{k} SCR / CO catalyst")
        strip(scr)
        scr["info"] = "SCR and CO catalyst housing with ammonia injection grid; access platforms and stair (typical)."
        box(x + 90, x + 130, 1190, 1220, 0, 1, "concrete")
        for xl in (x + 92, x + 110, x + 128):
            for yl in (1191, 1219):
                box(xl - .5, xl + .5, yl - .5, yl + .5, 1, 3, "steel")
        box(x + 91, x + 129, 1191, 1219, 3, 33, "equip")
        box(x + 90.6, x + 129.4, 1190.6, 1219.4, 33, 35, "roof")
        box(x + 128, x + 135.3, 1199, 1210, 11, 27, "duct")                     # outlet to the stack
        dress(True)
        for xr in range(x + 94, x + 128, 5):                                    # casing stiffeners
            for y, s in ((1191, -1), (1219, 1)):
                box(xr - .25, xr + .25, y, y + s * .5, 3, 33, "steel")
        pipe([(x + 100, 1189, 2), (x + 100, 1189, 30), (x + 100, 1191, 30)], 2, .25, "pipe")   # NH3 to the AIG
        for xg in (x + 97, x + 100, x + 103):
            rod((xg, 1191, 30), (xg, 1191, 33.6), .15, "pipe", seg=6)
        for zp in (14, 27):                                                     # platforms on the south face
            box(x + 92, x + 128, 1186.6, 1191, zp - .3, zp, "grating")
            rod((x + 92, 1186.7, zp + 3.4), (x + 128, 1186.7, zp + 3.4), .07, "rail", seg=4)
            for xr in range(x + 92, x + 129, 6):
                rod((xr, 1186.7, zp), (xr, 1186.7, zp + 3.4), .06, "rail", seg=4)
            for xr in (x + 92, x + 128):
                box(xr - .3, xr + .3, 1186.6, 1187.2, 0, zp - .3, "steel")
        for s in range(9):                                                      # stair flight to EL 14
            z = 1.5 * s + 1.4
            box(x + 128.6, x + 132, 1179 + s, 1180 + s, z, z + .2, "grating")
        dress(False)

        st = find(f"SC-{k} stack (80 ft)")
        on(st)
        dress(True)
        stack_dress(x + 142, 1204.5, 6.5, 80, 52)
        dress(False)

        lo = find(f"SC-{k} lube-oil fin-fan cooler")
        strip(lo)
        for xl in (x + 51, x + 69):
            for yl in (1246, 1258):
                box(xl - .3, xl + .3, yl - .3, yl + .3, 0, 6.5, "steel")
        box(x + 50, x + 70, 1245, 1259, 6.5, 8.6, "bundle")
        for xf in (x + 55, x + 65):
            rod((xf, 1252, 8.6), (xf, 1252, 9.6), 4.4, "steel", seg=22)
            rod((xf, 1252, 9.6), (xf, 1252, 10), 1.0, "motor", seg=12)
        dress(True)
        pipe([(x + 58, 1245, 5), (x + 58, 1221, 5), (x + 58, 1218, 5)], 5, .3, "pipe")
        dress(False)


def build():
    rice()
    simple_cycle()
