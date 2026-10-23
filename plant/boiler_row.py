"""Boiler Row (owner, Oct 23: "boilers is a critical moment ... utility boilers, gas boilers and electric boilers").
A showcase on the open land east of the auxiliary boiler AB-1 (x 1005-1325, y 1515-1645, between the H2 / CO2 storage
and the 30 ft road), on its own layer OPT_BOILERS so the SW-3X1 plant and its cable schedule are unchanged. With AB-1
(the gas package boiler) it lines up the three boiler stories west to east:

- UB-1, a utility gas-fired boiler, 300 MW class, representative (true height, reduced footprint), as built new for
  AI campuses or converted from coal: a clad boiler house 170 ft high with buckstay bands, the burner front on the
  south face (three rows of burners, windbox), a stair tower and platforms; the natural-gas train and burner-management
  panel at its foot (Class I Div 2, ARMOR-X MC-HL on strut); two FD fans with 13.8 kV motors and their MV cable; the
  back end (economizer / SCR with ammonia injection, regenerative air heater, flue duct) and a 230 ft stack with a CEMS
  platform; the main-steam line to the steam-turbine hall with its generator step-up transformer;
- EB-1, an electric (electrode) boiler, 30 MW at 13.8 kV: a boiler house whose roof sits on layer BOILER_ROW_ROOF
  (lifted in the cutaway), the electrode vessel with three bushings, circulation pumps and the steam header inside;
  the EB-1 MV e-house (13.8 kV breaker, PLC) and the MV-105 feeder in parallel sets on a ladder tray into the
  boiler roof; ground grid connection.
Typical, not engineered; for the boiler deck and the Nov 11 tour."""
import math

import fuel
from fuel import box, rod, on

L = "OPT_BOILERS"
LR = "BOILER_ROW_ROOF"


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def rail(pts, z):
    for a, b in zip(pts, pts[1:]):
        for h in (1.75, 3.5):
            rod((a[0], a[1], z + h), (b[0], b[1], z + h), .05, "rail", seg=6)
        n = int(math.dist(a, b) // 6) + 1
        for k in range(n + 1):
            t = k / n
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            rod((p[0], p[1], z), (p[0], p[1], z + 3.5), .05, "rail", seg=6)


def ladder_tray(pts, z, w, cables, step=2.0):
    import aux_boiler
    aux_boiler.tray(pts, z, w, cables, step)


def utility_boiler():
    it = fuel.new_item(L, "UB-1: utility gas-fired boiler, 300 MW class (Boiler Row, representative)", (990, 1150, 1515, 1637),
                       (0, 230), area="D", register=False, basis="typical",
                       info="Representative 300 MW-class natural-gas-fired utility boiler, as built new for AI-campus power "
                            "or converted from coal: boiler house, burner front, gas train and BMS (Class I Div 2), FD fans "
                            "on 13.8 kV motors, SCR, air heater, 230 ft stack with CEMS. Showcase, not part of SW-3X1.")
    on(it)
    fuel.D = False
    X0, X1, Y0, Y1, H = 1008.0, 1076.0, 1550.0, 1632.0, 170.0
    box(X0 - 4, X1 + 4, Y0 - 4, Y1 + 4, 0, 1.0, "concrete")
    box(X0, X1, Y0, Y1, 1.0, H, "hrsg_b")                                            # clad boiler house
    fuel.D = True
    for z in range(20, int(H), 18):                                                  # buckstay bands
        box(X0 - .4, X1 + .4, Y0 - .4, Y1 + .4, z, z + .9, "steel")
    for x in range(int(X0) + 6, int(X1), 8):                                        # cladding ribs (south face)
        box(x - .15, x + .15, Y0 - .25, Y0, 1.0, H, "steel")
    box(X0 - 1, X1 + 1, Y0 - 1, Y1 + 1, H, H + 2, "roof")                           # roof
    box(X0 + 12, X1 - 12, Y0 + 20, Y1 - 20, H + 2, H + 14, "hrsg_b")                # drum penthouse
    # burner front: windbox and three rows of four burners on the south face
    box(X0 + 6, X1 - 6, Y0 - 7, Y0, 30, 72, "machine")
    GY = Y0 - 22
    BF = Y0 - 7                                                                       # windbox face
    for r_, lv in enumerate("ABC"):
        z = 38 + r_ * 13
        zp = z - 2                                                                    # platform level
        for c_ in range(4):
            x = X0 + 14 + c_ * 13.3
            rod((x, BF + .05, z), (x, BF - .3, z), 2.7, "steel_dark", seg=24)          # quarl / mounting flange
            rod((x, BF - .3, z), (x, BF - 2.6, z), 2.0, "steel", seg=24)              # air register housing
            rod((x, BF - 2.6, z), (x, BF - 2.9, z), 2.25, "steel_dark", seg=24)       # front plate
            rod((x, BF - 2.9, z), (x, BF - 4.6, z), .35, "steel", seg=10)             # gas gun
            poly([(x, BF - 4.6, z), (x, BF - 4.6, z + 2.9)], .22, "fuelgas", seg=8)     # gun hose up to the level header
            box(x - .45, x + .45, BF - 5.05, BF - 4.15, z + 1.5, z + 2.3, "red")         # burner gas valve
            rod((x + 1.6, BF - 2.9, z + 1.6), (x + 2.1, BF - 4.4, z + 2.2), .28, "steel", seg=10)    # flame scanner
            rod((x - 1.6, BF - 2.9, z + 1.0), (x - 1.9, BF - 4.8, z + 1.3), .16, "steel_dark", seg=8)  # igniter
            box(x - 2.6, x - 1.4, BF - 5.6, BF - 4.6, zp, zp + 1.2, "cabinet")            # igniter transformer
            box(x - .7, x + .7, BF - 2.2, BF - .8, z + 2.1, z + 3.1, "motor")             # air-register actuator
            for (a, b) in (((x + 2.1, BF - 4.4, z + 2.2), (x + 2.1, BF - 5.4, zp + .4)),   # flex conduit to the tray
                           ((x - 2.0, BF - 5.1, zp + 1.2), (x - 2.0, BF - 5.6, zp + .4)),
                           ((x + .7, BF - 1.5, z + 2.6), (x + 1.1, BF - 5.5, zp + .4)),
                           ((x, BF - 4.6, z + 1.9), (x + .4, BF - 5.5, zp + .4))):
                poly([a, (a[0], b[1], a[2]), b], .07, "cable_armor", seg=6)
        poly([(X0 + 9, BF - 4.6, z + 2.9), (X1 - 9, BF - 4.6, z + 2.9)], .45, "fuelgas", seg=10)   # level gas header
        box(X0 + 10, X1 - 8, BF - 6.1, BF - 4.9, zp + .2, zp + .45, "steel")             # level cable tray on the platform
        box(X1 - 7.5, X1 - 5, BF - 6.4, BF - 5.4, zp, zp + 2.6, "cabinet")                # level junction box
        decal((X1 - 6.25, BF - 6.45, zp + 1.9), (0, -1, 0), 2.4, .5, [(f"BURNER LEVEL {lv} JB", .7, True, "#111111")], bg="#ffd200")
        for k in range(4):
            poly([(X1 - 6.25 + (k - 1.5) * .3, BF - 5.9, zp), (X1 - 6.25 + (k - 1.5) * .3, BF - 5.9, zp - .6),
                  (X1 - 4.4, BF - 5.9, zp - .6)], .08, "cable_armor", seg=6)
    poly([(X0 + 9, GY, 4.0), (X0 + 9, GY, 6.0), (X0 + 9, BF - 4.6, 6.0), (X0 + 9, BF - 4.6, 66.9)], .55, "fuelgas", seg=10)  # main gas riser
    box(X1 - 4.6, X1 - 3.4, BF - 6.4, BF - 5.2, 3, 64, "steel")                         # BMS riser channel, levels A-C to the panel
    for k in range(6):
        rod((X1 - 4.4 + k * .16, BF - 5.0, 3.2), (X1 - 4.4 + k * .16, BF - 5.0, 62.6), .07, "cable_armor", seg=6)
    for z in (36, 49, 62):                                                           # burner-front platforms
        box(X0 + 4, X1 - 4, Y0 - 16, Y0 - 7, z - .3, z, "grating")
        rail([(X0 + 4, Y0 - 16), (X1 - 4, Y0 - 16)], z)
        rail([(X0 + 4, Y0 - 16), (X0 + 4, Y0 - 7)], z) if z != 36 else None
        rail([(X1 - 4, Y0 - 16), (X1 - 4, Y0 - 7)], z)
        for xk in range(int(X0) + 10, int(X1) - 3, 12):                               # knee braces under the platform
            rod((xk, Y0 - 15.4, z - .4), (xk, Y0 - 7.2, z - 6.5), .22, "steel", seg=6)
            box(xk - .2, xk + .2, Y0 - 15.6, Y0 - 7, z - .9, z - .3, "steel")
        for xl in (X0 + 20, X0 + 40, X1 - 12):                                       # platform lights + their circuit
            rod((xl, Y0 - 15.8, z + 3.5), (xl, Y0 - 15.8, z + 4.4), .06, "steel", seg=6)
            box(xl - .5, xl + .5, Y0 - 16.1, Y0 - 15.5, z + 4.4, z + 4.8, "lamp")
        poly([(X0 + 4.2, Y0 - 15.8, z + 3.5), (X1 - 12, Y0 - 15.8, z + 3.5)], .05, "cable_tc", seg=4)
    # windbox stiffeners between and around the burners
    for zs in (33, 46, 59, 71):
        box(X0 + 6, X1 - 6, BF - .7, BF, zs - .5, zs + .5, "steel_dark")
    for c_ in range(5):
        xs = X0 + 7.35 + c_ * 13.3
        box(xs - .4, xs + .4, BF - .7, BF, 30, 72, "steel_dark")
    # stair tower to the three burner levels (west end): columns, switchback flights, landings, rails
    SX0, SX1, SY0, SY1 = X0 - 8, X0 + 3.5, Y0 - 16, Y0 - 7
    for (cx, cy) in ((SX0, SY0), (SX1, SY0), (SX0, SY1), (SX1, SY1)):
        box(cx - .4, cx + .4, cy - .4, cy + .4, 0, 66, "steel")
    zl = 0.0
    for k in range(10):                                                              # 6.5 ft flights, alternating
        z0, z1 = k * 6.5, (k + 1) * 6.5 if k < 9 else 62
        y_ = SY0 + 2 if k % 2 == 0 else SY1 - 2
        xa, xb = (SX0 + 1, SX1 - 3) if k % 2 == 0 else (SX1 - 3, SX0 + 1)
        n = 9
        for j in range(n):
            t = j / n
            xx = xa + (xb - xa) * t
            box(min(xx, xx + (xb - xa) / n), max(xx, xx + (xb - xa) / n), y_ - 1.8, y_ + 1.8,
                z0 + (z1 - z0) * t, z0 + (z1 - z0) * t + .25, "grating")
        rod((xa, y_ - 1.9, z0 + 3.4), (xb, y_ - 1.9, z1 + 3.4), .05, "rail", seg=4)
        box(SX1 - 3, SX1, SY0 + .2, SY1 - .2, z1 - .25, z1, "grating")                 # landing
    rail([(SX0, SY0), (SX0, SY1)], 62)
    decal(((SX0 + SX1) / 2, SY0 - .45, 8), (0, -1, 0), 8, 1.2, [("BURNER LEVELS A-C", .6, True, "#111111")], bg="#ffd200")
    # flame-scanner cooling air: two blowers at grade, a riser and a header per level, a hose to every scanner
    box(X0 + 22, X0 + 34, Y0 - 15, Y0 - 11, 0, .6, "concrete")
    for k in range(2):
        bx_ = X0 + 25 + k * 6
        rod((bx_, Y0 - 13, .6), (bx_, Y0 - 13, 3.2), 1.3, "machine", seg=16)               # blower
        box(bx_ + 1.3, bx_ + 3.3, Y0 - 14, Y0 - 12, .6, 2.4, "motor")                     # motor (480 V)
        poly([(bx_ + 3.3, Y0 - 13, 1.5), (bx_ + 3.3, Y0 - 15.5, 1.5), (bx_ + 3.3, Y0 - 15.5, .1)], .1, "cable_tc", seg=6)
    poly([(X0 + 31, Y0 - 13, 3.2), (X0 + 31, Y0 - 13, 5), (X0 + 31, BF - .9, 5), (X0 + 31, BF - .9, 66)], .35, "pipe", seg=8)
    decal((X0 + 28, Y0 - 15.1, 2.6), (0, -1, 0), 6, .8, [("SCANNER COOLING AIR", .6, True, "#111111")], bg="#ffffff")
    for r_ in range(3):
        z = 38 + r_ * 13
        poly([(X0 + 10, BF - .9, z + 3.7), (X1 - 9, BF - .9, z + 3.7)], .22, "pipe", seg=8)
        for c_ in range(4):
            x = X0 + 14 + c_ * 13.3
            poly([(x + 2.1, BF - .9, z + 3.7), (x + 2.1, BF - 4.4, z + 3.7), (x + 2.1, BF - 4.4, z + 2.4)], .08, "pipe", seg=6)
    # operators on burner levels B and A, one at the BMS panel
    import maintenance as mt
    mt.person(X0 + 30, Y0 - 12, 49, 0.0)
    mt.person(X1 - 12, Y0 - 13, 36, 3.14)
    mt.person(X1 + 2, GY - 6, 0, 1.57)
    # exposed structural steel: columns outside the casing, safety-valve vents on the penthouse roof
    for x in (X0, X0 + 17, X0 + 34, X0 + 51, X1):
        for y in (Y0 - 1.6, Y1):
            box(x - .9, x + .9, y, y + 1.6, 0, H + 2, "steel_dark")
    for y in (Y0 + 20.5, Y0 + 41, Y0 + 61.5):
        box(X0 - 1.6, X0, y - .9, y + .9, 0, H + 2, "steel_dark")
    for k in range(6):
        vx = X0 + 18 + k * 6.4
        rod((vx, Y0 + 40, H + 14), (vx, Y0 + 40, H + 26), .55, "pipe", seg=10)       # safety-valve vent stacks
        rod((vx, Y0 + 40, H + 24), (vx, Y0 + 40, H + 30), 1.25, "steel", seg=14)     # silencers
    # hot-air duct: air heater outlet to the windbox
    box(X1 + 4, X1 + 13, Y0 - 6, Y0 + 44, 70, 79, "duct")
    box(X0 + 6, X1 + 13, Y0 - 7, Y0, 72, 79, "duct")
    # elevator beside the stair tower
    box(X0 - 12, X0 - 3, Y1 - 27, Y1 - 17, 0, H + 12, "building")
    # stair tower at the NW corner
    box(X0 - 14, X0 - 2, Y1 - 16, Y1, 0, H + 4, "steel")
    for z in range(10, int(H), 10):
        box(X0 - 14.5, X0 - 1.5, Y1 - 16.5, Y1 + .5, z - .3, z, "grating")
    decal((X0 + 34, Y0 - .5, 140), (0, -1, 0), 44, 9, [("UTILITY GAS BOILER  UB-1", .42, True, "#111111"),
                                                       ("300 MW CLASS  ·  NATURAL GAS  ·  REPRESENTATIVE", .24, False, "#333333")],
          bg="#ffffff")
    # gas train + burner management at the foot of the burner front (Class I Div 2)
    GY = Y0 - 22
    box(X0 + 6, X1 - 6, GY - 3, GY + 3, 0, 1.2, "steel_dark")
    poly([(926, 1584, 4.0), (X0 - 10, 1584, 4.0), (X0 - 10, GY, 4.0), (X1 - 8, GY, 4.0)], .7, "fuelgas", seg=12)   # gas header up from the buried plant line
    for xv, kind in ((X0 + 14, "ssov"), (X0 + 22, "vent"), (X0 + 30, "ssov"), (X0 + 40, "fcv")):
        rod((xv - .9, GY, 4.0), (xv + .9, GY, 4.0), 1.1, "steel", seg=12)
        if kind == "vent":
            box(xv - .6, xv + .6, GY - .6, GY + .6, 4.8, 6.4, "amber")
        else:
            box(xv - .8, xv + .8, GY - .8, GY + .8, 5.0, 7.0, "red")
    BX0, BX1 = X1 - 4, X1 + 4                                                        # BMS panel
    box(BX0, BX1, GY - 3, GY, 0, 8, "cabinet")
    decal(((BX0 + BX1) / 2, GY - 3.05, 7.0), (0, -1, 0), 6.5, 1.0, [("UB-1  BURNER MANAGEMENT", .55, True, "#111111")], bg="#ffffff")
    box(X0 + 8, BX0, GY - 4.4, GY - 4.0, 3.0, 3.2, "steel")                         # strut
    for dz in (0, .35, .7):
        poly([(BX0, GY - 1.5, 3.2 + dz), (BX0 - 2, GY - 4.2, 3.2 + dz), (X0 + 8, GY - 4.2, 3.2 + dz)], .12, "cable_armor", seg=8)
    for xv in (X0 + 14, X0 + 22, X0 + 30, X0 + 40):
        poly([(xv, GY - 4.2, 3.4), (xv, GY - 1.2, 3.4), (xv, GY - 1.2, 5.0)], .09, "cable_armor", seg=6)
    decal((X0 + 26, GY - 3.1, 1.6), (0, -1, 0), 10, 1.0, [("DANGER  ·  NATURAL GAS  ·  CLASS I DIV 2", .5, True, "#ffffff")], bg="#b8322a")
    # FD fans with 13.8 kV motors and their MV cable, SE of the boiler
    for k_, fy in enumerate((Y0 + 4, Y0 + 24)):
        fx = X1 + 6
        rod((fx, fy, 9), (fx + 10, fy, 9), 7.5, "machine", seg=24)                  # fan housing
        box(fx + 11, fx + 19, fy - 3.5, fy + 3.5, 1, 9, "motor")                    # 13.8 kV motor
        box(fx + 12, fx + 15, fy + 3.5, fy + 5.5, 4, 7, "motor")                    # MV terminal box
        rod((fx + 13.5, fy + 5.5, 4), (fx + 13.5, fy + 5.5, .2), .3, "cable_mv", seg=8)
        poly([(fx, fy, 9), (X1, fy, 9)], 3.5, "duct", seg=16)
        decal((fx + 19.05, fy, 7.5), (1, 0, 0), 4.5, .9, [(f"FD FAN {'AB'[k_]}  ·  13.8 kV", .55, True, "#111111")], bg="#ffd200")
    # back end: economizer / SCR, air heater, flue duct, stack
    box(X1, X1 + 26, Y0 + 40, Y1, 60, 150, "hrsg_b")                                 # backpass with SCR
    box(X1 + 26, X1 + 30, Y0 + 50, Y0 + 70, 100, 110, "pipe")                        # AIG header
    rod((X1 + 13, Y0 + 52, 40), (X1 + 13, Y0 + 52, 60), 9, "machine", seg=24)        # rotary air heater
    poly([(X1 + 13, Y0 + 70, 70), (X1 + 40, Y0 + 70, 70), (X1 + 52, Y0 + 70, 70)], 6.5, "duct", seg=16)
    SX, SY = X1 + 58, Y0 + 70
    rod((SX, SY, 0), (SX, SY, 230), 9.5, "stack", seg=36)
    box(SX - 13, SX + 13, SY - 13, SY + 13, 120, 120.5, "grating")                   # CEMS platform
    for (a, h) in ((0, 120), (1.6, 228)):
        pass
    for z in (60, 140, 200):
        rod((SX, SY, z), (SX, SY, z + 2), 10.2, "hero_accent", seg=36)
    rod((SX - 9.7, SY, 2), (SX - 9.7, SY, 229), .08, "steel", seg=4)                 # obstruction-light conduit
    for a in (0, 2.1, 4.2):
        box(SX + 9.8 * math.cos(a) - .5, SX + 9.8 * math.cos(a) + .5, SY + 9.8 * math.sin(a) - .5,
            SY + 9.8 * math.sin(a) + .5, 226, 227, "red")
    fuel.D = False
    return it


def steam_turbine_hall():
    it = fuel.new_item(L, "UB-1 steam-turbine hall and generator step-up (Boiler Row)", (1150, 1250, 1525, 1640), (0, 84),
                       area="D", register=False, basis="typical",
                       info="Steam turbine generator for UB-1 in its hall (overhead crane), generator step-up transformer and "
                            "isolated-phase bus. Showcase.")
    on(it)
    fuel.D = False
    X0, X1, Y0, Y1 = 1160.0, 1222.0, 1530.0, 1632.0
    box(X0, X1, Y0, Y1, 0, 80, "building")
    box(X0, X1 + .5, Y0 - .5, Y1 + .5, 80, 82, "roof")
    fuel.D = True
    box(X0 - .6, X1 + .6, Y0 - .6, Y1 + .6, 78, 80, "hero_accent")                   # copper coping, as on the heater bay
    for x in range(int(X0) + 6, int(X1), 10):
        box(x - .2, x + .2, Y0 - .3, Y0, 0, 78, "steel")                              # south-face ribs
    box(X1, X1 + .1, Y0 + 30, Y0 + 70, 40, 62, "louvre")
    decal(((X0 + X1) / 2, Y0 - .35, 70), (0, -1, 0), 50, 5.0, [("UB-1 TURBINE HALL", .55, True, "#111111")], bg="#ffffff")
    # main steam line from the boiler penthouse
    for (y, r) in ((1583, 1.3), (1588.5, 1.8), (1577.5, 1.5)):                     # main steam, hot reheat, cold reheat
        poly([(1060, y, 184), (1060, y, 188), (1150 - (y - 1583), y, 188), (1150 - (y - 1583), y, 60), (X0, y, 60)], r, "pipe", seg=14)
    # GSU transformer and IPB on the east
    box(X1 + 4, X1 + 22, Y0 + 30, Y0 + 54, 0, 1, "concrete")
    box(X1 + 7, X1 + 19, Y0 + 33, Y0 + 51, 1, 18, "xfmr")
    for k in range(3):
        rod((X1 + 10 + k * 3, Y0 + 42, 18), (X1 + 10 + k * 3, Y0 + 42, 25), .5, "insulator", seg=10)
        rod((X1, Y0 + 38 + k * 2.5, 14), (X1 + 7, Y0 + 38 + k * 2.5, 14), .9, "ipb", seg=14)
    for (fx, a) in ((X1 + 5.5, 0), (X1 + 20.5, 0)):
        for k in range(4):
            box(fx - .5, fx + .5, Y0 + 34 + k * 4.5, Y0 + 37 + k * 4.5, 3, 15, "radiator")
    fuel.D = False
    return it


def electric_boiler():
    it = fuel.new_item(L, "EB-1: electric (electrode) boiler, 30 MW at 13.8 kV, with its MV e-house (Boiler Row)",
                       (1250, 1300.5, 1520, 1640), (0, 48), area="D", register=False, basis="typical",
                       info="Electrode boiler, 30 MW, 13.8 kV, ~1,250 A: MV-105 in parallel sets from the EB-1 13.8 kV "
                            "breaker to the boiler bushings, bare-copper grounding, PLC, circulation pumps. Showcase.")
    on(it)
    fuel.D = False
    X0, X1, Y0, Y1, H = 1256.0, 1300.0, 1545.0, 1615.0, 40.0
    box(X0 - 2, X1 + 2, Y0 - 2, Y1 + 2, 0, 1.0, "concrete")
    box(X0, X1, Y0, Y0 + .6, 1, H, "building", layer=LR)                             # south wall (cutaway)
    box(X0, X1, Y1 - .6, Y1, 1, H, "building")
    box(X0, X0 + .6, Y0, Y1, 1, H, "building")
    box(X1 - .6, X1, Y0, Y1, 1, H, "building", layer=LR)                             # east wall (cutaway)
    box(X0 - .5, X1 + .5, Y0 - .5, Y1 + .5, H, H + 1.5, "roof", layer=LR)
    fuel.D = True
    box(X0 + .6, X1 - .6, Y0 + .6, Y1 - .6, 1.0, 1.05, "epoxy")
    decal((X0 - .05, (Y0 + Y1) / 2, 34), (-1, 0, 0), 30, 4.4, [("ELECTRIC BOILER  EB-1", .5, True, "#111111"),
                                                             ("30 MW  ·  13.8 kV  ·  ELECTRODE", .3, False, "#333333")],
          bg="#ffffff")
    # electrode vessel on its skirt, MV termination enclosure on top with three bushings, steam header, pumps
    VX, VY = 1278.0, 1592.0
    rod((VX, VY, 1.0), (VX, VY, 4.0), 5.0, "steel_dark", seg=36)                      # skirt
    rod((VX, VY, 4.0), (VX, VY, 26.0), 6.0, "alu", seg=36)
    rod((VX, VY, 26.0), (VX, VY, 29.0), 6.0, "alu", r2=3.5, seg=36)
    for z in (8, 16, 24):
        rod((VX, VY, z), (VX, VY, z + .5), 6.15, "steel", seg=36)                    # insulation bands
    decal((VX, VY - 6.2, 18), (0, -1, 0), 7, 2.2, [("DANGER  13.8 kV", .55, True, "#ffffff")], bg="#b8322a")
    BT = []
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        bx, by = VX + 2.2 * math.cos(a), VY + 2.2 * math.sin(a)
        rod((bx, by, 28.5), (bx, by, 32.0), .55, "insulator", seg=12)               # MV bushing
        rod((bx, by, 32.0), (bx, by, 32.6), .35, "copper", seg=8)
        BT.append((bx, by))
    poly([(VX + 4, VY, 27.5), (VX + 9, VY, 27.5), (VX + 9, VY, 22), (1328, VY, 22), (1328, VY, 14.2)], .9, "pipe", seg=12)   # steam out to storage
    for k in range(2):                                                               # circulation pumps
        px = VX - 9 + k * 6
        box(px - 2, px + 2, Y0 + 9, Y0 + 14, 1.0, 1.6, "concrete")
        rod((px, Y0 + 11.5, 1.6), (px, Y0 + 11.5, 4.6), 1.3, "motor", seg=14)
        poly([(px, Y0 + 11.5, 3.0), (px, VY - 6, 3.0)], .5, "pipe", seg=10)
    box(X0 + 1, X0 + 4, Y0 + 6, Y0 + 14, 1, 8, "cabinet")                              # PLC panel
    box(X0 + 1, X0 + 4, Y0 + 16, Y0 + 24, 1, 8, "cabinet")                             # pump starters
    decal((X0 + 4.05, Y0 + 15, 7.2), (1, 0, 0), 15, 1.0, [("EB-1 PLC  ·  PUMP MCC", .55, True, "#111111")], bg="#ffffff")
    for y in (Y0 + 10, Y0 + 20):
        poly([(X0 + 4, y, 7.5), (X0 + 6, y, 9.6), (VX - 9, Y0 + 11.5, 9.6), (VX - 9, Y0 + 11.5, 4.6)], .07, "cable_tc", seg=4)
    rod((VX + 6, VY, 2), (VX + 7.5, VY, 1.05), .1, "copper", seg=4)                   # ground bond
    # EB-1 MV e-house south of the boiler house (13.8 kV breaker + PLC), cable entry from the duct bank
    EX0, EX1, EY0, EY1 = 1262.0, 1300.0, 1522.0, 1538.0
    box(EX0, EX1, EY0, EY1, 0, 2.5, "concrete")
    box(EX0 + .3, EX1 - .3, EY0 + .3, EY1 - .3, 2.5, 13.5, "ehouse")
    box(EX0, EX1, EY0, EY1, 13.5, 14.2, "roof")
    decal((EX0 + 19, EY0 - .02, 11), (0, -1, 0), 18, 1.6, [("EB-1  13.8 kV SWITCHGEAR", .6, True, "#111111")], bg="#ffffff")
    for k in range(6):                                                               # conduit stub-ups from the duct bank
        x = EX1 - 6 + k * .7
        rod((x, EY0 - 1.2, 0), (x, EY0 - 1.2, 2.4), .22, "pipe", seg=8)
    # MV-105 feeder, 3 parallel sets of 3 x 1/C 750 kcmil: out of the e-house north wall at EL 10, a ladder tray across
    # the gap and through the boiler-house south wall, along the floor at EL 10, then up the vessel to the bushings
    TZ, TX = 10.0, VX - 8.5
    box(TX - 3, TX + 3, EY1, EY1 + .3, 8.6, 11.6, "steel")                             # e-house wall sleeve frame
    ladder_tray([(TX, EY1), (TX, VY - 1), ], TZ, 4.4, [("cable_mv", .22)] * 9)
    for (x, y) in ((TX - 2.4, EY1 + 3.5), (TX - 2.4, Y0 + 30), (TX + 2.4, Y0 + 30)):
        rod((x, y, 1.0), (x, y, TZ - .2), .18, "steel", seg=8)                       # tray supports
    box(TX - 2.6, TX + 2.6, EY1 + 3.3, EY1 + 3.7, TZ - .4, TZ - .2, "steel")
    for k in range(9):                                                                # riser up the vessel to the bushings
        j, b = k % 3, BT[k // 3]
        x = TX - 1.6 + k * .4
        poly([(x, VY - 1, TZ + .3), (x, VY - 1, TZ + .3 + .1), (VX - 6.6, VY - 1.2 + j * .45, TZ + .4),
              (VX - 6.6, VY - 1.2 + j * .45, 30.5), (b[0] + (j - 1) * .25, b[1], 33.6), (b[0] + (j - 1) * .25, b[1], 32.6)],
             .2, "cable_mv", seg=8)
    box(VX - 7.4, VX - 6.2, VY - 1.8, VY + .8, TZ, 30.5, "steel")                       # riser cleat channel
    decal((TX, Y0 + 30, TZ + 1.2), (-1, 0, 0), 9, .9, [("MV-105  ·  3 SETS  ·  13.8 kV", .55, True, "#111111")], bg="#ffd200")
    fuel.D = False
    return it


def heater_bay():
    """The bay that joins the UB-1 boiler house and the turbine hall into one power-station block (owner, Oct 23): feedwater
    heaters, the deaerator on the roof, boiler feed pumps, the unit control room and, under it, the cable spreading room
    where every circuit of the unit comes together. Same cladding and copper coping as the turbine hall."""
    it = fuel.new_item(L, "UB-1 heater bay: feedwater heaters, deaerator, unit control room, cable spreading room (Boiler Row)",
                       (1110, 1160, 1528, 1598), (0, 122), area="D", register=False, basis="typical",
                       info="Heater bay between the boiler house and the turbine hall: LP / HP feedwater heaters, deaerator and "
                            "storage tank on the roof, boiler feed pumps at grade, unit control room at EL 30 and the cable "
                            "spreading room below it, where every circuit of the unit is marshalled. Showcase.")
    on(it)
    X0, X1, Y0, Y1, H = 1110.0, 1159.9, 1530.0, 1598.0, 105.0
    fuel.D = False
    box(X0, X1, Y0, Y1, 0, H, "building")
    box(X0 - .5, X1, Y0 - .5, Y1 + .5, H, H + 2, "roof")
    fuel.D = True
    box(X0 - .6, X1, Y0 - .6, Y1 + .6, H - 2, H, "hero_accent")                       # copper coping
    for x in range(int(X0) + 5, int(X1), 10):
        box(x - .2, x + .2, Y0 - .3, Y0, 0, H - 2, "steel")                           # south-face ribs
    box(X0 + 3, X1 - 3, Y0 - .15, Y0, 30, 36, "glass")                                 # unit control room windows
    box(X0 + 3, X1 - 3, Y0 - .2, Y0, 8, 13, "louvre")                                 # cable spreading room vents
    box(X0 + 4, X0 + 10, Y0 - .3, Y0, 0, 10, "steel_dark")                            # roller door
    decal(((X0 + X1) / 2, Y0 - .35, 46), (0, -1, 0), 40, 5.0, [("UB-1 HEATER BAY", .5, True, "#111111"),
                                                               ("UNIT CONTROL ROOM  ·  FEEDWATER", .3, False, "#333333")],
          bg="#ffffff")
    decal((X0 + 30, Y0 - .35, 15.2), (0, -1, 0), 16, 1.6, [("CABLE SPREADING ROOM", .62, True, "#111111")], bg="#ffd200")
    # deaerator and storage tank on the roof
    for x in (X0 + 10, X1 - 10):
        box(x - 2, x + 2, 1560, 1570, H + 2, H + 5, "steel")                            # saddles
    rod((X0 + 6, 1565, H + 10), (X1 - 6, 1565, H + 10), 6.0, "tank", seg=28)            # storage tank
    rod((X0 + 14, 1565, H + 16), (X0 + 14, 1565, H + 26), 2.6, "tank", seg=20)         # deaerator head
    rod((X0 + 14, 1565, H + 26), (X0 + 14, 1565, H + 28), 2.6, "tank", r2=1.2, seg=20)
    rail([(X0 + 1, Y0 + 1), (X1 - 1, Y0 + 1), (X1 - 1, Y1 - 1), (X0 + 1, Y1 - 1), (X0 + 1, Y0 + 1)], H + 2)
    # cable from the spine tray into the spreading room
    for k in range(10):
        x = 1131 + k * .45
        poly([(x, 1518, 22.4), (x, 1521.5, 22.4), (x, 1521.5, 11), (x, Y0, 11)], .14, "cable_tc", seg=6)
    box(1129.5, 1136.5, Y0 - .3, Y0, 9, 13, "steel")                                  # wall sleeve frame
    fuel.D = False
    return it


def steam_storage():
    it = fuel.new_item(L, "EB-1 steam accumulator (thermal storage, Boiler Row)", (1318, 1340, 1512, 1616), (0, 32),
                       area="D", register=False, basis="typical",
                       info="Steam accumulator: EB-1 runs when power is cheap or surplus and stores the steam for later. Showcase.")
    on(it)
    fuel.D = False
    box(1319, 1338, 1570, 1614, 0, .8, "concrete")
    rod((1328, 1572, 8.5), (1328, 1612, 8.5), 5.6, "tank", seg=32)
    fuel.D = True
    for y in (1578, 1606):
        box(1324, 1332, y - 1.5, y + 1.5, .8, 5, "concrete")                        # saddles
    for y in (1572, 1612):
        rod((1328, y, 8.5), (1328, y + (-1 if y < 1600 else 1) * 1.6, 8.5), 5.6, "tank", r2=3.0, seg=32)  # heads
    rod((1328, 1592, 14.1), (1328, 1592, 14.8), .9, "steel", seg=12)
    decal((1322.3, 1592, 9), (-1, 0, 0), 22, 2.6, [("STEAM STORAGE", .62, True, "#111111")], bg="#ffffff")
    poly([(1328, 1570.4, 8.5), (1328, 1566, 8.5), (1328, 1566, 31.2), (1328, 1513.6, 31.2)], .8, "pipe", seg=12)   # to the spine
    fuel.D = False
    return it


SPY, SPX0, SPX1 = 1516.0, 999.0, 1340.0


def spine():
    it = fuel.new_item(L, "Boiler Row spine rack: steam header, gas header, condensate and cable trays", (992, 1342, 1505, 1531),
                       (0, 34), area="D", register=False, basis="typical",
                       info="One rack along the fronts of all three boilers: steam header back to the plant via the AB-1 aux-steam header, "
                            "fuel-gas header, condensate return; ladder trays below with control, instrument and MV cable. Showcase.")
    on(it)
    fuel.D = False
    bents = [(x, SPY) for x in range(int(SPX0) + 4, int(SPX1) + 1, 22) if not 1004 < x < 1032] + [(1034, SPY), (SPX1, SPY)]
    for (x, y) in bents:
        horiz = y == SPY
        for d in (-4, 4):
            px, py = (x, y + d) if horiz else (x + d, y)
            box(px - .6, px + .6, py - .6, py + .6, 0, 32, "hero_accent")
        a, b = ((x, y - 4.6), (x, y + 4.6)) if horiz else ((x - 4.6, y), (x + 4.6, y))
        for z in (22, 30):
            box(min(a[0], b[0]) - .5, max(a[0], b[0]) + .5, min(a[1], b[1]) - .5, max(a[1], b[1]) + .5, z - 1.1, z, "hero_accent")
    fuel.D = True
    # pipes on the top tier: the main run east-west, then the west leg south to AB-1's aux-steam header
    for off, r, c in ((-2.4, 1.15, "pipe"), (0, .55, "pipe"), (2.4, .65, "fuelgas")):
        end = [(998, SPY + off, 12.0), (998, 1510, 12.0)] if off < 0 else [(998 + off, SPY + off, .5)]
        poly([(SPX1, SPY + off, 31.2), (998 + max(off, 0), SPY + off, 31.2)] + end, r, c, seg=12)   # steam into the plant aux header
    decal((1240, SPY - 5.2, 26), (0, -1, 0), 34, 2.2, [("STEAM  ·  CONDENSATE  ·  FUEL GAS  ·  CABLE", .6, True, "#ffffff")], bg="#b8322a")
    # ladder trays on the lower tier: control / instrument (amber) and MV
    ladder_tray([(SPX1 - 4, SPY), (1000, SPY)], 22.2, 4.2, [("cable_tc", .14)] * 10 + [("cable_mv", .2)] * 3)
    for x, z in ((1046, 6.0), (1190, 20.0), (1282, 14.6)):                         # drops: UB-1 gas train, STG, EB-1 e-house
        for k in range(5):
            poly([(x + k * .35, SPY + 2, 22.4), (x + k * .35, SPY + 4.6, 22.4), (x + k * .35, SPY + 4.6, z)], .1,
                 "cable_tc", seg=6)
    for k in range(5):                                                              # AB-1: into its east face
        poly([(1000, SPY - 1 + k * .5, 22.4), (996.5, SPY - 1 + k * .5, 22.4), (996.5, SPY - 1 + k * .5, 10)], .1, "cable_tc", seg=6)
    poly([(1200, 1530, 30), (1200, 1513.6, 30), (1200, 1513.6, 31.2)], .7, "pipe", seg=10)   # STG extraction steam
    fuel.D = False
    return it


HUB = (1135.0, 1195.0, 1462.0, 1505.0)
TRY = 1515.0


def hub():
    it = fuel.new_item(L, "Boiler Row control room and MCC (cable hub)", (1130, 1200, 1458, 1515), (0, 21), area="D",
                       register=False, basis="typical",
                       info="Shared control room, DCS / BMS cabinets and 480 V MCC for the three boilers; amber control and "
                            "instrument cable rises from here into the spine tray to every bay. Showcase.")
    on(it)
    x0, x1, y0, y1 = HUB
    fuel.D = False
    box(x0 - 1, x1 + 1, y0 - 1, y1 + 1, 0, 1.2, "concrete")
    box(x0, x1, y0, y1, 1.2, 16, "ehouse")
    box(x0 - .4, x1 + .4, y0 - .4, y1 + .4, 16, 16.8, "roof")
    fuel.D = True
    box(x0 + 8, x0 + 16, y0 + 10, y0 + 22, 16.8, 20, "machine")                       # rooftop HVAC
    box(x1 - 14, x1 - 9, y0 - .3, y0, 1.2, 8.5, "steel_dark")                        # door
    decal(((x0 + x1) / 2, y0 - .1, 12.5), (0, -1, 0), 38, 3.4, [("BOILER ROW CONTROL  ·  MCC", .5, True, "#111111"),
                                                               ("every boiler's cable starts here", .3, False, "#555555")],
          bg="#ffffff")
    # every boiler's cable leaves here: up the north wall and into the spine tray at EL 22
    for k in range(10):
        poly([(1160 + k * .5, y1, 9), (1160 + k * .5, y1 + 1.2, 9), (1160 + k * .5, y1 + 1.2, 22.4), (1160 + k * .5, SPY - 1, 22.4)],
             .14, "cable_tc", seg=6)
    box(1158.5, 1166.5, y1, y1 + 2.4, 8, 22, "steel")                                 # riser channel
    fuel.D = False
    return it


def cooling():
    """UB-1's condenser cooling, where AB-1 stood: a three-cell mechanical-draft cooling tower with its basin, two vertical
    circulating-water pumps on 4.16 kV motors (MV-105), CW pipes going below grade to the STG condenser, and the tower MCC
    (fan motors on VFDs) fed from the plant duct bank at x 915."""
    it = fuel.new_item(L, "UB-1 cooling tower (3 cells) and circulating-water pumps (Boiler Row)", (912, 1000, 1442, 1544), (0, 52),
                       area="D", register=False, basis="typical",
                       info="Mechanical-draft cooling tower for the UB-1 condenser, 3 cells; two vertical CW pumps on 4.16 kV "
                            "motors (MV-105), CW supply and return below grade to the STG; tower MCC with fan VFDs. Showcase.")
    on(it)
    # same build as the CCS cooling tower (ccs.cooling_tower): basin, tower casing, concrete cell walls, grating fan deck,
    # flared fan stacks with blades, hub, gearbox, shaft and motor outside the stack, intake louvres, teal hot-water risers
    X0, X1, Y0, Y1 = 936.0, 984.0, 1450.0, 1540.0
    CELL = 30.0
    fuel.D = False
    box(X0, X1, Y0, Y1, 0, 3, "water")
    box(X0, X1, Y0, Y1, 3, 40, "tower")
    box(X0, X1, Y0, Y1, 40, 42, "grating")
    for c in range(1, 3):
        box(X0, X1, Y0 + CELL * c - .5, Y0 + CELL * c + .5, 3, 42, "concrete")
    fuel.D = True
    for c in range(3):
        cx, cy = (X0 + X1) / 2, Y0 + CELL * (c + .5)
        rod((cx, cy, 42), (cx, cy, 50), 12.5, "tower", r2=13.2, seg=24)                  # fan stack
        for b in range(8):
            a = 2 * math.pi * b / 8 + .3 * c
            rod((cx + 1.6 * math.cos(a), cy + 1.6 * math.sin(a), 50.25),
                (cx + 12 * math.cos(a), cy + 12 * math.sin(a), 50.35), .45, "fan", r2=.3, seg=6)
        rod((cx, cy, 50), (cx, cy, 50.03), 12.9, "fanhub", seg=28)                       # open stack (dark throat)
        rod((cx, cy, 50.03), (cx, cy, 50.6), 1.7, "fan", seg=16)                         # hub
        box(cx - 1.4, cx + 1.4, cy - 1.4, cy + 1.4, 42, 43.6, "machine")                  # gearbox
        rod((cx + 1.4, cy, 42.8), (cx + 15, cy, 42.8), .3, "steel", seg=8)                # drive shaft
        rod((cx + 15, cy, 42.8), (cx + 19, cy, 42.8), 1.1, "motor", seg=12)               # motor outside the stack
        box(X1 - 2.2, X1 - .4, cy + 3, cy + 5, 42, 44.5, "cabinet")                       # local disconnect
        poly([(X1 - 1.3, cy + 4, 44.5), (X1 - 1.3, cy + 4, 45), (cx + 17, cy + 4, 45), (cx + 17, cy + .9, 43.4)], .1,
             "cable_tc", seg=6)
        for (x0, x1) in ((X0 - .3, X0), (X1, X1 + .3)):                                   # intake louvres on the long faces
            box(x0, x1, Y0 + CELL * c + 1.5, Y0 + CELL * (c + 1) - 1.5, 4, 22, "louvre")
    for y in (Y0 + 1, Y1 - 1):
        rod((X0 + 1, y, 45), (X1 - 1, y, 45), .07, "rail", seg=4)
    for x in (X0 + 1, X1 - 1):
        rod((x, Y0 + 1, 45), (x, Y1 - 1, 45), .07, "rail", seg=4)
    # access stair at the north end, as on the CCS tower
    for k in range(20):
        box(X0 + 4 + k * 1.9, X0 + 5.2 + k * 1.9, Y1 + .5, Y1 + 4.5, 2 * k + 2, 2 * k + 2.3, "grating")
    for ys in (Y1 + .5, Y1 + 4.5):
        rod((X0 + 2.1, ys, 0), (X0 + 4 + 38.2, ys, 42), .18, "steel", seg=6)
        rod((X0 + 2.1, ys, 3.5), (X0 + 4 + 38.2, ys, 45.5), .06, "rail", seg=4)
    # hot-water return from the STG condenser: up out of the ground at the north-east corner, a header along the east face
    # and a riser into every cell
    poly([(987, 1546, 0), (987, 1546, 4), (987, Y0 + 4, 4)], 2.0, "waterline", seg=16)
    for c in range(3):
        y = Y0 + CELL * (c + .5) - 8
        rod((987, y, 4), (987, y, 38), 1.2, "waterline", seg=12)
        rod((987, y, 38), (X1, y, 38), 1.2, "waterline", seg=12)
    decal(((X0 + X1) / 2, Y0 - .35, 31), (0, -1, 0), 40, 4.0, [("UB-1 COOLING TOWER", .48, True, "#111111"),
                                                               ("3 CELLS  ·  CONDENSER COOLING", .28, False, "#333333")], bg="#ffffff")
    # fan riser: VFD-rated cable from the tower MCC up the stair to the deck
    for k in range(3):
        poly([(925, 1500 + k * .5, 11), (933, 1500 + k * .5, 11), (933, Y1 + 5.5 + k * .4, 11), (X0 + 44, Y1 + 5.5 + k * .4, 11),
              (X0 + 44, Y1 + 5.5 + k * .4, 42.6), (X0 + 44, Y1 - 1 - k * .4, 42.6)], .14, "cable_tc", seg=6)
    # CW pump pit on the east side with two vertical pumps, 4.16 kV motors, discharge pipes down to the buried CW lines
    box(X1 + 2, X1 + 14, Y0 + 10, Y0 + 40, 0, 1.2, "concrete")
    for k, py in enumerate((Y0 + 17.0, Y0 + 33.0)):
        rod((X1 + 8, py, 1.2), (X1 + 8, py, 6), 2.0, "steel", seg=20)                     # pump head
        rod((X1 + 8, py, 6), (X1 + 8, py, 12), 2.4, "motor", seg=20)                      # 4.16 kV motor
        rod((X1 + 8, py, 12), (X1 + 8, py, 12.8), 1.4, "motor", seg=16)
        box(X1 + 10.4, X1 + 12.6, py - 1.2, py + 1.2, 7, 10, "motor")                    # MV terminal box
        for j in range(3):
            rod((X1 + 11.1 + j * .35, py, 7), (X1 + 11.1 + j * .35, py, .1), .17, "cable_mv", seg=8)   # MV-105 stub-up
        poly([(X1 + 8, py, 3.5), (X1 + 8, py - 4, 3.5), (X1 + 8, py - 4, .05)], 1.6, "pipe", seg=16)   # discharge, below grade
        decal((X1 + 13.05, py, 9.2), (1, 0, 0), 4.6, .9, [(f"CWP-{'AB'[k]}  ·  4.16 kV", .6, True, "#111111")], bg="#ffd200")
    # tower MCC e-house (fans on VFDs), fed from the plant duct bank at x 915
    box(916, 932, 1488, 1512, 0, 2.5, "concrete")
    box(916.3, 931.7, 1488.3, 1511.7, 2.5, 12, "ehouse")
    box(916, 932, 1488, 1512, 12, 12.6, "roof")
    decal((931.75, 1500, 10), (1, 0, 0), 14, 1.4, [("CT MCC  ·  FAN VFDs", .62, True, "#111111")], bg="#ffffff")
    for k in range(4):
        rod((917.5 + k * .7, 1486.8, 0), (917.5 + k * .7, 1486.8, 2.4), .22, "pipe", seg=8)        # stub-ups from the duct bank
    fuel.D = False
    return it


def back_bay():
    """Behind AB-1, west of UB-1: where UB-1's MV and its gas start. Two station-service transformers and the UB-1 13.8 kV
    switchgear e-house (MV-105 out to the FD fans on a tray behind the boiler), and the gas metering and pressure-reducing
    station (Class I Div 2, ARMOR-X MC-HL on strut) feeding the UB-1 gas train."""
    it = fuel.new_item(L, "UB-1 electrical bay: station-service transformers SST-A/B and the 13.8 kV switchgear e-house (Boiler Row)",
                       (928, 1108, 1556, 1646), (0, 22), area="D", register=False, basis="typical",
                       info="Two 13.8 kV station-service transformers on an oil-containment pad with a firewall, and the UB-1 "
                            "13.8 kV switchgear: MV-105 to the FD fans and feed pumps leaves here. Showcase.")
    on(it)
    fuel.D = False
    box(934, 988, 1562, 1596, 0, .8, "concrete")                                      # containment pad
    for k, x in enumerate((938.0, 966.0)):
        box(x, x + 16, 1567, 1589, .8, 14, "xfmr")
        fuel.D = True
        for j in range(5):
            box(x - 1.2, x, 1569 + j * 4, 1571.5 + j * 4, 2, 12, "radiator")
        for j in range(3):
            rod((x + 4 + j * 4, 1578, 14), (x + 4 + j * 4, 1578, 19), .45, "insulator", seg=10)
        box(x + 4, x + 12, 1589, 1592, 4, 11, "steel")                                 # MV cable box
        decal((x + 8, 1566.9, 11), (0, -1, 0), 8, 1.4, [(f"SST-{'AB'[k]}  ·  13.8 kV", .6, True, "#111111")], bg="#ffd200")
        for j in range(6):                                                           # MV-105 to the switchgear
            poly([(x + 5.5 + j, 1592, 9), (x + 5.5 + j, 1594, 12.4), (x + 5.5 + j, 1617, 12.4), (x + 5.5 + j, 1619.6, 7)],
                 .2, "cable_mv", seg=8)
        fuel.D = False
    box(959.5, 961.5, 1563, 1595, .8, 18, "concrete")                                # firewall
    fuel.D = True
    for (x0, x1) in ((941, 954), (969, 982)):                                         # ladder trays transformers to e-house
        box(x0, x1, 1593.5, 1617.5, 12, 12.25, "steel")
    fuel.D = False
    EX0, EX1, EY0, EY1 = 930.0, 990.0, 1619.6, 1636.0
    box(EX0, EX1, EY0, EY1, 0, 2.5, "concrete")
    box(EX0 + .3, EX1 - .3, EY0 + .3, EY1 - .3, 2.5, 14.5, "ehouse")
    box(EX0, EX1, EY0, EY1, 14.5, 15.2, "roof")
    fuel.D = True
    decal((960, EY0 - .02, 12.2), (0, -1, 0), 30, 1.8, [("UB-1  13.8 kV SWITCHGEAR  ·  MV-105 STARTS HERE", .55, True, "#111111")],
          bg="#ffffff")
    for x in (944, 976):
        box(x - 1.6, x + 1.6, EY0 - 4, EY0, 2.5, 3, "grating")                          # landings
    box(EX1 - 6, EX1 - 2, EY0 + 4, EY0 + 12, 15.2, 18, "machine")                     # HVAC
    # MV-105 to the FD fans: out of the e-house roof, a ladder tray behind the boiler, then down to the fan motors
    for j in range(6):
        poly([(981 + j * .6, EY0 + 8, 15.2), (981 + j * .6, EY0 + 8, 20.5), (984, EY0 + 8 + (j - 2.5) * .5, 20.5)],
             .2, "cable_mv", seg=8)
    ladder_tray([(984, EY0 + 8), (984, 1642), (1106, 1642), (1106, 1576)], 20.4, 3.6, [("cable_mv", .2)] * 6)
    for (x, y) in ((986.4, 1640), (1030, 1644.2), (1070, 1644.2), (1108.4, 1610), (1108.4, 1585)):
        rod((x, y, 0), (x, y, 20), .25, "steel", seg=8)
    for k_, fy in enumerate((1554.0, 1574.0)):                                       # drops to the FD fan MV terminal boxes
        for j in range(3):
            poly([(1106, 1576 + j * .5, 20.6), (1106, fy + 4.5 + j * .5, 20.6), (1095.5 + j * .4, fy + 4.5, 20.6),
                  (1095.5 + j * .4, fy + 4.5, 7)], .18, "cable_mv", seg=8)
    fuel.D = False

    it2 = fuel.new_item(L, "UB-1 gas metering and pressure-reducing station (Boiler Row)", (880, 928, 1556, 1612), (0, 14), area="D",
                        register=False, basis="typical",
                        info="Fuel-gas metering, filter-separator and two pressure-reducing runs for UB-1; Class I Div 2, "
                             "instrument and power in ARMOR-X MC-HL on strut. Showcase.")
    on(it2)
    fuel.D = False
    box(882, 926, 1560, 1608, 0, .6, "gravel")
    fuel.D = True
    rod((890, 1566, 1), (890, 1566, 13), 3.0, "tank", seg=24)                         # filter-separator
    for y in (1578.0, 1590.0):                                                        # two regulator runs
        poly([(884, y, 3.2), (924, y, 3.2)], .6, "fuelgas", seg=12)
        for x, c in ((896, "red"), (904, "steel"), (912, "red"), (918, "steel")):
            box(x - .9, x + .9, y - .9, y + .9, 2.4, 5.2, c)
        for x in (888, 922):
            box(x - .6, x + .6, y - 2, y + 2, 0, 2.6, "concrete")
    poly([(884, 1566, 3.2), (884, 1590, 3.2)], .6, "fuelgas", seg=12)
    poly([(924, 1578, 3.2), (926, 1578, 3.2), (926, 1584, 3.2), (926, 1584, 4.0)], .7, "fuelgas", seg=12)
    poly([(924, 1590, 3.2), (926, 1590, 3.2), (926, 1584, 3.2)], .7, "fuelgas", seg=12)
    rod((905, 1600, .6), (905, 1600, 4.4), .3, "steel", seg=8)                         # meter run
    box(902, 908, 1598, 1602, 2.6, 5, "steel")
    box(914, 922, 1603, 1606, 0, 7, "cabinet")                                        # metering RTU / analyzer
    decal((918, 1602.95, 6.2), (0, -1, 0), 7, .9, [("GAS METERING RTU", .6, True, "#111111")], bg="#ffffff")
    box(886, 922, 1594.6, 1595, 3, 3.2, "steel")                                      # strut
    for k in range(4):
        poly([(918, 1603, 3.4 + k * .3), (918, 1595, 3.4 + k * .3), (886 + k * 9, 1595, 3.4 + k * .3),
              (886 + k * 9, 1591, 4.6)], .09, "cable_armor", seg=6)
    decal((904, 1559.5, 1.4), (0, -1, 0), 14, 1.0, [("DANGER  ·  NATURAL GAS  ·  CLASS I DIV 2", .55, True, "#ffffff")], bg="#b8322a")
    fuel.D = False


def support_yard():
    """West of the UB-1 electrical bay (x 782-878, y 1502-1645) and at the stack: what a complete unit still needs."""
    import showcase
    import maintenance as mt
    # condensate storage tank and transfer pumps
    it = fuel.new_item(L, "UB-1 condensate storage tank and transfer pumps (Boiler Row)", (790, 845, 1510, 1550), (0, 40), area="D",
                       register=False, basis="typical",
                       info="Condensate storage tank (~30 ft dia) and two transfer pumps on 480 V motors (TC-ER power). Showcase.")
    on(it)
    fuel.D = False
    rod((810, 1530, 0), (810, 1530, 1.2), 16.5, "concrete", seg=36)
    rod((810, 1530, 1.2), (810, 1530, 36), 15, "tank", seg=36)
    fuel.D = True
    rod((810, 1530, 36), (810, 1530, 38.5), 15, "tank", r2=4, seg=36)
    for z in (12, 24):
        rod((810, 1530, z), (810, 1530, z + .4), 15.15, "steel", seg=36)
    for k in range(10):                                                             # spiral-ish stair up the shell
        a = -1.2 + k * .16
        x_, y_ = 810 + 15.6 * math.cos(a), 1530 + 15.6 * math.sin(a)
        box(x_ - 1.2, x_ + 1.2, y_ - 1.2, y_ + 1.2, 1.2 + k * 3.6, 1.5 + k * 3.6, "grating")
    decal((810, 1514.85, 28), (0, -1, 0), 20, 3.0, [("UB-1 CONDENSATE STORAGE", .5, True, "#111111")], bg="#ffffff")
    for k, py in enumerate((1524.0, 1536.0)):
        box(830, 840, py - 2.5, py + 2.5, 0, .6, "concrete")
        rod((832, py, 1.8), (835, py, 1.8), 1.0, "machine", seg=14)                  # pump
        rod((835, py, 1.8), (839, py, 1.8), .9, "motor", seg=14)                     # 480 V motor
        poly([(825.6, py, 3), (832, py, 3), (832, py, 1.8)], .45, "pipe", seg=10)
        poly([(839, py + .6, 2.3), (839, py + 2.2, 2.3), (839, py + 2.2, .1)], .1, "cable_tc", seg=6)
    fuel.D = False

    # emergency diesel generator for safe shutdown, cabled into the UB-1 switchgear e-house
    it = fuel.new_item(L, "UB-1 emergency diesel generator, 480 V, ~2 MW (Boiler Row)", (843, 932, 1598, 1640), (0, 24), area="D",
                       register=False, basis="typical",
                       info="Standby generator for safe shutdown (turning gear, lube oil, DC chargers, emergency lighting): "
                            "sub-base day tank, exhaust silencer, ATS in the e-house; 1/C 500 kcmil in parallel on a ladder "
                            "tray into the switchgear. Showcase.")
    on(it)
    fuel.D = False
    box(845, 880, 1604, 1620, 0, 1.2, "concrete")
    box(846, 879, 1605, 1619, 1.2, 4, "steel_dark")                                   # sub-base day tank
    box(846.5, 878.5, 1605.5, 1618.5, 4, 14, "machine")                              # enclosure
    fuel.D = True
    box(846.4, 849, 1606, 1618, 5, 13, "louvre")                                     # radiator end
    rod((872, 1612, 14), (872, 1612, 20), .9, "stack", seg=12)                       # exhaust
    rod((872, 1612, 15), (872, 1612, 18), 1.6, "steel", seg=14)                      # silencer
    decal((862, 1605.4, 11.5), (0, -1, 0), 22, 1.8, [("UB-1 EMERGENCY DIESEL GENERATOR  ·  480 V", .58, True, "#111111")],
          bg="#ffd200")
    for (x, y) in ((884, 1612), (906, 1612), (928, 1612)):
        rod((x, y + 2.2, 0), (x, y + 2.2, 9.6), .2, "steel", seg=8)
    ladder_tray([(879, 1612), (929.5, 1612), (929.5, 1622)], 9.8, 3.0, [("cable", .28)] * 8)
    for k in range(8):
        poly([(878.5, 1610.6 + k * .4, 8), (879.5, 1610.6 + k * .4, 10)], .14, "cable", seg=6)
    fuel.D = False

    # CEMS shelter at the UB-1 stack
    it = fuel.new_item(L, "UB-1 CEMS shelter at the stack (Boiler Row)", (1104, 1126, 1598, 1616), (0, 122), area="D", register=False,
                       basis="typical",
                       info="Analyzer shelter for the UB-1 stack: NOx / CO / O2 / NH3 slip, heated sample line from the EL 120 "
                            "platform; power, instrument pairs and fibre to the DCS. Showcase.")
    on(it)
    fuel.D = False
    box(1111, 1123, 1600, 1614, 0, 1, "concrete")
    box(1111.3, 1122.7, 1600.3, 1613.7, 1, 10.5, "ehouse")
    box(1111, 1123, 1600, 1614, 10.5, 11.1, "roof")
    fuel.D = True
    decal((1111.25, 1607, 8.5), (-1, 0, 0), 10, 1.4, [("UB-1 CEMS", .62, True, "#111111")], bg="#ffffff")
    box(1115, 1118, 1603, 1607, 11.1, 13, "machine")                                  # HVAC
    poly([(1123, 1611, 8), (1124.6, 1612.6, 8), (1124.6, 1612.6, 119.6)], .35, "steel_dark", seg=8)   # heated sample line
    for k in range(3):
        poly([(1111, 1602 + k * .5, 6), (1108.6, 1602 + k * .5, 6), (1108.6, 1602 + k * .5, 20.4)], .1, "cable_tc", seg=6)
    fuel.D = False


def mv_feed():
    """The 13.8 kV feeder to EB-1 comes in buried: a marker strip with red posts from the south to the e-house stub-ups."""
    it = fuel.new_item(L, "EB-1 13.8 kV feeder duct bank (marker strip)", (1290, 1298, 1462, 1521), (0, 4), area="D",
                       register=False, basis="typical")
    on(it)
    fuel.D = True
    box(1292, 1296, 1462, 1520.5, 0, .12, "concrete")
    for y in range(1466, 1520, 12):
        rod((1297.2, y, 0), (1297.2, y, 3.2), .18, "red", seg=8)
    decal((1294, 1474, .14), (0, 0, 1), 12, 2.6, [("13.8 kV  MV-105  ·  DANGER", .55, True, "#ffffff")], bg="#b8322a",
          up=(0, 1, 0))
    fuel.D = False


def bays():
    """Three bays, each on its own pad with a bay plate painted on the ground in front."""
    it = fuel.new_item(L, "Boiler Row bays: pads and bay plates", (790, 1342, 1490, 1640), (0, .3), area="D", register=False,
                       basis="typical")
    on(it)
    fuel.D = True
    for (cx, cy, t, sub) in ((1058, 1497, "UTILITY BOILER", "gas · 300 MW class"),
                             (1250, 1497, "ELECTRIC BOILER", "13.8 kV · no flame"),
                             (814, 1551, "PACKAGE BOILER", "start-up steam")):
        decal((cx, cy, .16), (0, 0, 1), 44, 9 if cx < 900 else 11.5, [(t, .44, True, "#e39a5f"), (sub.upper(), .26, True, "#ffffff")],
              bg="#1d2125", up=(0, 1, 0))
    box(1003, 1250, 1546, 1636, 0, .14, "concrete")                                   # bay 2 pad (boiler + STG)
    box(1253, 1342, 1520, 1636, 0, .14, "concrete")                                   # bay 3 pad
    fuel.D = False


def sign():
    it = fuel.new_item(L, "Boiler Row sign", (1005, 1030, 1505, 1512), (0, 12), area="D", register=False, basis="typical")
    on(it)
    fuel.D = True
    for x in (1007.0, 1028.0):
        rod((x, 1508, 0), (x, 1508, 8), .25, "steel", seg=8)
    box(1006, 1029, 1507.8, 1508.2, 6.5, 11.5, "panel")
    decal((1017.5, 1507.75, 9.0), (0, -1, 0), 22, 4.6, [("BOILER ROW", .5, True, "#ffffff"),
                                                       ("PACKAGE  ·  UTILITY  ·  ELECTRIC", .28, False, "#e39a5f")], bg="#15181b")
    fuel.D = False


def build():
    n0 = len(fuel.G["parts"])
    utility_boiler()
    steam_turbine_hall()
    heater_bay()
    electric_boiler()
    steam_storage()
    spine()
    hub()
    cooling()
    back_bay()
    support_yard()
    mv_feed()
    bays()
    sign()
    return len(fuel.G["parts"]) - n0
