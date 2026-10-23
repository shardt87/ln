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
    it = fuel.new_item(L, "UB-1: utility gas-fired boiler, 300 MW class (Boiler Row, representative)", (992, 1150, 1515, 1640),
                       (0, 230), area="D", register=False, basis="typical",
                       info="Representative 300 MW-class natural-gas-fired utility boiler, as built new for AI-campus power "
                            "or converted from coal: boiler house, burner front, gas train and BMS (Class I Div 2), FD fans "
                            "on 13.8 kV motors, SCR, air heater, 230 ft stack with CEMS. Showcase, not part of SW-3X1.")
    on(it)
    fuel.D = False
    X0, X1, Y0, Y1, H = 1008.0, 1076.0, 1542.0, 1624.0, 170.0
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
    for r_ in range(3):
        for c_ in range(4):
            x = X0 + 14 + c_ * 13.3
            z = 38 + r_ * 13
            rod((x, Y0 - 7, z), (x, Y0 - 9.5, z), 2.2, "steel_dark", seg=16)
            rod((x + 1.6, Y0 - 9.5, z + 1.6), (x + 1.6, Y0 - 10.4, z + 2.0), .3, "steel", seg=8)   # flame scanner
            rod((x + 1.6, Y0 - 10.4, z + 2.0), (x + 1.6, Y0 - 11.2, z + 2.0), .06, "cable_inst", seg=4)
    for z in (36, 49, 62):                                                           # burner-front platforms
        box(X0 + 4, X1 - 4, Y0 - 16, Y0 - 7, z - .3, z, "grating")
        rail([(X0 + 4, Y0 - 16), (X1 - 4, Y0 - 16)], z)
    # stair tower at the SW corner
    box(X0 - 14, X0 - 2, Y0 - 2, Y0 + 12, 0, H + 4, "steel")
    for z in range(10, int(H), 10):
        box(X0 - 14.5, X0 - 1.5, Y0 - 2.5, Y0 + 12.5, z - .3, z, "grating")
    decal((X0 + 34, Y0 - .5, 140), (0, -1, 0), 44, 9, [("UTILITY GAS BOILER  UB-1", .42, True, "#111111"),
                                                       ("300 MW CLASS  ·  NATURAL GAS  ·  REPRESENTATIVE", .24, False, "#333333")],
          bg="#ffffff")
    # gas train + burner management at the foot of the burner front (Class I Div 2)
    GY = Y0 - 22
    box(X0 + 6, X1 - 6, GY - 3, GY + 3, 0, 1.2, "steel_dark")
    poly([(X0 - 10, GY, 0.3), (X0 - 10, GY, 4.0), (X1 - 8, GY, 4.0)], .7, "fuelgas", seg=12)   # gas header up from the buried plant line
    for xv, kind in ((X0 + 14, "ssov"), (X0 + 22, "vent"), (X0 + 30, "ssov"), (X0 + 40, "fcv")):
        rod((xv - .9, GY, 4.0), (xv + .9, GY, 4.0), 1.1, "steel", seg=12)
        if kind == "vent":
            box(xv - .6, xv + .6, GY - .6, GY + .6, 4.8, 6.4, "amber")
        else:
            box(xv - .8, xv + .8, GY - .8, GY + .8, 5.0, 7.0, "red")
    for c_ in range(4):                                                              # risers to each burner column
        x = X0 + 14 + c_ * 13.3
        poly([(x, GY, 4.0), (x, GY, 8.0), (x, Y0 - 8, 8.0), (x, Y0 - 8, 36.0)], .35, "fuelgas", seg=8)
    BX0, BX1 = X1 - 18, X1 - 10                                                      # BMS panel
    box(BX0, BX1, GY - 10, GY - 7, 0, 8, "cabinet")
    decal(((BX0 + BX1) / 2, GY - 10.05, 7.0), (0, -1, 0), 6.5, 1.0, [("UB-1  BURNER MANAGEMENT", .55, True, "#111111")], bg="#ffffff")
    box(X0 + 8, BX0, GY - 4.4, GY - 4.0, 3.0, 3.2, "steel")                         # strut
    for dz in (0, .35, .7):
        poly([(BX0, GY - 8.5, 3.2 + dz), (X0 + 8, GY - 4.2, 3.2 + dz)], .12, "cable_armor", seg=8)
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
    it = fuel.new_item(L, "UB-1 steam-turbine hall and generator step-up (Boiler Row)", (1150, 1250, 1525, 1640), (0, 75),
                       area="D", register=False, basis="typical",
                       info="Steam turbine generator for UB-1 in its hall (overhead crane), generator step-up transformer and "
                            "isolated-phase bus. Showcase.")
    on(it)
    fuel.D = False
    X0, X1, Y0, Y1 = 1160.0, 1222.0, 1530.0, 1630.0
    box(X0, X1, Y0, Y1, 0, 72, "building")
    box(X0 - .5, X1 + .5, Y0 - .5, Y1 + .5, 72, 74, "roof")
    fuel.D = True
    for y in range(int(Y0) + 6, int(Y1), 10):
        box(X0 - .3, X0, y - .2, y + .2, 0, 72, "steel")
    box(X0 - .1, X0, Y0 + 30, Y0 + 70, 40, 62, "louvre")
    decal((X0 - .2, (Y0 + Y1) / 2, 66), (-1, 0, 0), 30, 4.6, [("STEAM TURBINE GENERATOR", .55, True, "#111111")], bg="#ffffff")
    # main steam line from the boiler penthouse
    poly([(1064, 1583, 172), (1064, 1583, 176), (1150, 1583, 176), (1150, 1583, 60), (X0, 1583, 60)], 1.2, "pipe", seg=12)
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
                       (1250, 1325, 1520, 1640), (0, 48), area="D", register=False, basis="typical",
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
    poly([(VX + 4, VY, 27.5), (VX + 9, VY, 27.5), (VX + 9, VY, 22), (X1, VY, 22)], .9, "pipe", seg=12)   # steam out
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
    electric_boiler()
    sign()
    return len(fuel.G["parts"]) - n0
