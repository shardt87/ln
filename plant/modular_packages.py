"""Two more modular gas-turbine package types for the modular yard (owner, Oct 24: "the other gas power plants on the
modular yard ... different modular ones"), in the open block between the collector e-house and the SC units:

- AX-1, a compact modular aeroderivative installation (LM2500XPRESS class, ~35 MW; owner reference pictures Oct 27):
  factory modules standing on a raised steel base with stairs and yellow-railed walkways: the inlet filter module with
  its stacked weather hoods, the turbine module with its ventilation fans and ducts on the roof, the exhaust plenum and
  a tall banded stack, the generator module with its doors, the lube / fuel auxiliary skid and the control module;
  the module joints carry pre-terminated plug-in interconnects;
- IG-1, an industrial gas-turbine installation (SGT-800 / H-25 class, ~50 MW; owner reference pictures Oct 27): the
  turbine-generator building, the combustion-air filter house raised on a steel frame with its inclined filter faces,
  the exhaust diffuser out of the end wall into a tall stack, generator air coolers and ventilation on the roof with a
  railed roof walkway, the electrical and control module, the lube-oil cooler, the fuel-gas module.

Both: 13.8 kV generator leads in MV-105 to the unit step-up AX-GSU / IG-GSU (13.8 / 34.5 kV) and on to the park
collector SWG-PK (routes in build_model, electrical review Oct 28), ARMOR-X MC-HL
at the fuel-gas modules (Class I Div 2), TC-ER control from the control module. Layer OPT_MODX (design change beyond
Rev 14), not in the register. Typical, not engineered.
"""
import math

import fuel
from fuel import box, rod

L = "OPT_MODX"


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def louvre_box(x0, x1, y0, y1, z0, z1):
    box(x0, x1, y0, y1, z0, z1, "steel")
    for (a, b) in ((y0 - .15, y0), (y1, y1 + .15)):
        box(x0 + .8, x1 - .8, a, b, z0 + .8, z1 - .8, "louvre")
    box(x0 - .1, x0, y0 + .8, y1 - .8, z0 + .8, z1 - .8, "louvre")


def fin_fan(x0, x1, y0, y1, h=8.0):
    for (x, y) in ((x0 + .4, y0 + .4), (x1 - .4, y0 + .4), (x0 + .4, y1 - .4), (x1 - .4, y1 - .4)):
        rod((x, y, 0), (x, y, h - 1.5), .2, "steel", seg=6)
    box(x0, x1, y0, y1, h - 1.5, h, "radiator")
    for k in range(2):
        cx = x0 + (x1 - x0) * (k + .5) / 2
        rod((cx, (y0 + y1) / 2, h), (cx, (y0 + y1) / 2, h + .3), min(x1 - x0, y1 - y0) / 2 - .6, "fanhub", seg=20)


def gas_module(x0, x1, y0, y1, label):
    box(x0, x1, y0, y1, 0, .6, "steel_dark")
    poly([(x0 - 1.5, (y0 + y1) / 2, .2), (x0 - 1.5, (y0 + y1) / 2, 2.6), (x1 - .5, (y0 + y1) / 2, 2.6)], .35, "fuelgas", seg=10)
    for k, c in enumerate(("red", "steel", "red")):
        x = x0 + 2 + k * (x1 - x0 - 4) / 2
        box(x - .5, x + .5, (y0 + y1) / 2 - .5, (y0 + y1) / 2 + .5, 3.0, 4.4, c)
    box(x1 - 2, x1 - .5, y1 - 1.2, y1 - .4, .6, 4.5, "panel")                         # gas-module JB
    for k in range(3):                                                               # MC-HL on strut to the valves
        x = x0 + 2 + k * (x1 - x0 - 4) / 2
        poly([(x1 - 1.25, y1 - .8, 4.2), (x1 - 1.25, y1 - .8, 4.9), (x, y1 - .8, 4.9), (x, (y0 + y1) / 2 + .5, 4.4)], .07,
             "cable_armor", seg=6)
    decal(((x0 + x1) / 2, y1 + .02, 2.0), (0, 1, 0), x1 - x0 - 1, .8, [(label, .6, True, "#ffffff")], bg="#b8322a")


def stair(x, y, z_top, dx=0, dy=-1, w=3.0):
    """A straight stair from z_top down to grade, leaving (x, y) in direction (dx, dy), with yellow handrails."""
    n = max(2, int(z_top / .65))
    for k in range(n):
        z = z_top - (k + 1) * z_top / n
        cx, cy = x + dx * (k + .5) * .9, y + dy * (k + .5) * .9
        if dx:
            box(cx - .45, cx + .45, y - w / 2, y + w / 2, z, z + .12, "grating")
        else:
            box(x - w / 2, x + w / 2, cy - .45, cy + .45, z, z + .12, "grating")
    L_ = n * .9
    for s in (-1, 1):
        if dx:
            rod((x, y + s * w / 2, z_top + 3.2), (x + dx * L_, y + s * w / 2, 3.2), .07, "sp_yellow", seg=6)
        else:
            rod((x + s * w / 2, y, z_top + 3.2), (x + s * w / 2, y + dy * L_, 3.2), .07, "sp_yellow", seg=6)


def rail(pts, z):
    """Yellow handrail along a polyline at deck level z (top rail + mid rail + posts every ~6 ft)."""
    for a, b in zip(pts, pts[1:]):
        for h in (1.8, 3.4):
            rod((a[0], a[1], z + h), (b[0], b[1], z + h), .06, "sp_yellow", seg=6)
        L_ = math.dist(a, b)
        for k in range(int(L_ / 6) + 1):
            t = k * 6 / L_ if L_ else 0
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            rod((x, y, z), (x, y, z + 3.4), .06, "sp_yellow", seg=6)


def hoods(x0, x1, y, z0, z1, side):
    """Stacked weather hoods on a filter-module face at y (side -1 = south face, +1 = north face)."""
    z = z0 + 1.0
    while z + 2.2 < z1:
        box(x0 + .5, x1 - .5, min(y, y + side * 2.2), max(y, y + side * 2.2), z + 1.6, z + 2.0, "steel")   # hood top
        box(x0 + .5, x1 - .5, min(y, y + side * .15), max(y, y + side * .15), z, z + 1.6, "louvre")        # filter face
        z += 2.6


def ax1():
    """AX-1: compact modular aeroderivative (LM2500XPRESS class) on its raised steel base, west to east: control and
    auxiliary skids, generator module (terminal box at the west face, x 1988-1990), exhaust plenum and stack, turbine
    module with roof ventilation, inlet filter module with stacked weather hoods."""
    Y0, YC = 1008.0, 1032.0
    it = fuel.new_item(L, "AX-1: compact modular aeroderivative installation, LM2500XPRESS class (~35 MW)",
                       (1981, 2076, 1004, 1062), (0, 96), area="I", register=False, basis="typical", tag="AX-1",
                       sheet="typical (modular expansion)",
                       info="Aeroderivative gas-turbine generator delivered as factory modules on a raised steel base: inlet "
                            "filter module with stacked weather hoods, turbine module with roof ventilation, exhaust plenum and "
                            "stack, generator module, auxiliary (lube / fuel) skid and control module; module joints with "
                            "pre-terminated plug-in interconnects; 13.8 kV MV-105 to its unit step-up AX-GSU, MC-HL at the gas module, TC-ER control.")
    fuel.on(it)
    fuel.D = False
    box(1981, 2076, Y0, 1056, 0, .6, "concrete")                                        # pad
    ZB = 3.6                                                                            # raised base deck
    for x in range(1992, 2074, 8):                                                       # pedestals under the modules
        for y in (1023.5, 1040.5):
            box(x - .5, x + .5, y - .5, y + .5, .6, ZB - .4, "steel_dark")
    box(1990, 2073, 1023, 1041, ZB - .4, ZB, "steel_dark")                              # base frame
    box(1990, 2073, 1018.5, 1023, ZB - .2, ZB, "grating")                               # south walkway
    rail([(1990, 1018.5), (2073, 1018.5)], ZB)
    # generator module (west)
    box(1990, 2010, 1024, 1040, ZB, 17, "ehouse")
    box(1990, 2010, 1024, 1040, 17, 17.5, "roof")
    for x in (1993, 2001):
        box(x, x + 3.2, 1023.85, 1024, ZB + .4, ZB + 7.6, "steel_dark")                  # module doors
    box(1997, 2005, 1028, 1036, 17.5, 21, "louvre")                                     # generator air inlet hood
    box(1988, 1990, 1029, 1035, ZB + .5, ZB + 6.5, "motor")                              # generator terminal box
    for j in range(6):
        y = 1030.5 + j * .6
        poly([(1989, y, ZB + .5), (1989, y, 1.2), (1987.6, y, .2)], .2, "cable_mv", seg=8)
    # exhaust plenum and stack
    box(2010, 2019, 1025, 1039, ZB, 21, "duct")
    rod((2014.5, YC, 21), (2014.5, YC, 95), 5.0, "stack", seg=28)
    for z in (40, 60, 80):
        rod((2014.5, YC, z), (2014.5, YC, z + .6), 5.25, "steel", seg=28)                 # stack bands
    rod((2014.5, YC, 94.2), (2014.5, YC, 95.2), 5.3, "hero_accent", seg=28)
    # turbine module with roof ventilation fans and ducts
    box(2019, 2047, 1024, 1040, ZB, 19, "ehouse")
    box(2019, 2047, 1024, 1040, 19, 19.5, "roof")
    for x in (2024, 2037):
        box(x, x + 6, 1029, 1035, 19.5, 23.5, "steel")                                   # vent fan housing
        rod((x + 3, YC, 23.5), (x + 3, YC, 24.2), 2.6, "fanhub", seg=16)
        box(x + 6, x + 9, 1030, 1034, 21, 23, "duct")                                    # vent duct elbow
    box(2027, 2031, 1023.85, 1024, ZB + .4, ZB + 7.6, "steel_dark")                       # turbine module door
    # inlet filter module (east) with stacked weather hoods on both long faces and the east end
    box(2047, 2071, 1022, 1042, ZB, 27, "filter")
    box(2047, 2071, 1022, 1042, 27, 27.5, "roof")
    hoods(2048, 2070, 1022, ZB, 27, -1)
    hoods(2048, 2070, 1042, ZB, 27, 1)
    z = ZB + 1.0
    while z + 2.2 < 27:
        box(2071, 2073.2, 1023, 1041, z + 1.6, z + 2.0, "steel")
        z += 2.6
    # control module (south) and auxiliary lube / fuel skid (north), stairs to the walkway
    box(1990, 2010, Y0 + 2, Y0 + 9, .6, 10, "ehouse"); box(1990, 2010, Y0 + 2, Y0 + 9, 10, 10.5, "roof")
    decal((2000, Y0 + 1.9, 8.4), (0, -1, 0), 14, 1.1, [("AX-1  CONTROL MODULE", .6, True, "#111111")], bg="#ffffff")
    for k in range(5):
        x = 1994 + k * .5
        poly([(x, Y0 + 9, 7), (x, 1018.5, 7), (x, 1024, 7)], .1, "cable_tc", seg=6)
    box(2022, 2044, 1044, 1052, .6, 8, "machine")                                       # auxiliary (lube / fuel) skid
    fin_fan(2048, 2064, 1045, 1053)
    poly([(2033, 1044, 4), (2033, 1041, 4)], .4, "pipe", seg=10)
    gas_module(1992, 2008, 1045, 1051, "FUEL GAS  ·  CLASS I DIV 2")
    stair(2034, 1018.5, ZB, dy=-1)
    stair(2060, 1018.5, ZB, dy=-1)
    # module joints with plug-in interconnects (south face)
    for xj in (2010, 2019, 2047):
        box(xj - .15, xj + .15, 1023.7, 1040.3, ZB, 19.4, "hero_accent")
        for k in range(3):
            y = 1023.6
            rod((xj - 1.2, y, ZB + 2 + k * 1.6), (xj + 1.2, y, ZB + 2 + k * 1.6), .12, ("cable_mv", "cable_tc", "cable_inst")[k], seg=6)
            box(xj - .4, xj + .4, y - .3, y, ZB + 1.6 + k * 1.6, ZB + 2.4 + k * 1.6, "sp_yellow")
    decal((2033, 1023.8, 15.5), (0, -1, 0), 24, 2.6, [("AX-1  ·  COMPACT MODULAR AERODERIVATIVE", .46, True, "#111111"),
                                                      ("~35 MW  ·  13.8 kV  ·  factory modules", .3, False, "#333333")], bg="#ffffff")
    import maintenance as mt
    mt.person(2040, 1020.5, ZB, 1.57)
    fuel.D = False
    return it


def ig1():
    """IG-1: industrial gas-turbine installation (SGT-800 / H-25 class), west to east: stack, exhaust diffuser, the
    turbine-generator building (generator at the east end, terminal box at x 2176-2181), with the filter house raised on
    its steel frame above the compressor end; E&C module south, lube-oil cooler and fuel gas north."""
    YC = 1032.0
    it = fuel.new_item(L, "IG-1: industrial gas-turbine installation, SGT-800 / H-25 class (~50 MW)",
                       (2092, 2188, 1004, 1062), (0, 80), area="I", register=False, basis="typical", tag="IG-1",
                       sheet="typical (modular expansion)",
                       info="Industrial gas-turbine generator in its building: combustion-air filter house raised on a steel "
                            "frame with inclined filter faces, exhaust diffuser through the end wall into a tall stack, generator "
                            "air coolers and enclosure ventilation on the roof, electrical and control module, lube-oil cooler, "
                            "fuel-gas module; 13.8 kV MV-105 to its unit step-up AX-GSU, MC-HL at the gas module, TC-ER control.")
    fuel.on(it)
    fuel.D = False
    box(2092, 2188, 1006, 1058, 0, .6, "concrete")
    # turbine-generator building
    box(2120, 2172, 1018, 1046, .6, 26, "ehouse")
    box(2119.6, 2172.4, 1017.6, 1046.4, 26, 26.6, "roof")
    for x in range(2124, 2172, 6):
        box(x - .08, x + .08, 1017.8, 1018, .6, 26, "steel")                               # wall panel seams
    box(2160, 2166, 1017.6, 1018, .6, 9, "steel_dark")                                   # double door
    box(2172, 2176, 1028, 1036, 2, 10, "motor"); box(2176, 2181, 1029, 1035, 3, 9, "motor")   # generator terminal box
    for j in range(6):
        y = 1030.5 + j * .6
        poly([(2180, y, 3), (2180, y, 1.2), (2180.4, y, .2)], .2, "cable_mv", seg=8)
    # combustion-air filter house on its steel frame (over the compressor end), inlet duct down to the roof
    for x in (2126, 2150):
        for y in (1019, 1045):
            box(x - .6, x + .6, y - .6, y + .6, 26.6, 40, "steel")
    box(2125, 2151, 1018.5, 1045.5, 39.4, 40, "steel_dark")
    box(2126, 2150, 1021, 1043, 40, 56, "filter")
    box(2125.6, 2150.4, 1020.6, 1043.4, 56, 56.6, "roof")
    for k in range(4):                                                                   # inclined filter faces, both sides
        o = k * 1.2
        box(2127, 2149, 1021 - 1.2 - o, 1021 - o, 41.5 + k * 3.6, 44.5 + k * 3.6, "louvre")
        box(2127, 2149, 1043 + o, 1043 + 1.2 + o, 41.5 + k * 3.6, 44.5 + k * 3.6, "louvre")
    box(2134, 2142, 1028, 1036, 26.6, 40, "duct")                                        # inlet duct to the compressor
    rail([(2125, 1018.5), (2151, 1018.5), (2151, 1045.5), (2125, 1045.5), (2125, 1018.5)], 40)
    # exhaust: diffuser through the west wall into the stack
    rod((2120, YC, 11), (2107, YC, 11), 6.0, "duct", seg=24)
    rod((2101, YC, 0.6), (2101, YC, 78), 7.0, "stack", seg=32)
    rod((2101, YC, 52), (2101, YC, 53), 7.3, "steel", seg=32)
    rod((2101, YC, 77), (2101, YC, 78.2), 7.3, "hero_accent", seg=32)
    # roof: generator air coolers, enclosure ventilation, walkway with rails and a ladder
    box(2156, 2170, 1022, 1042, 26.6, 31, "radiator")
    for y in (1027, 1037):
        rod((2163, y, 31), (2163, y, 31.4), 3.4, "fanhub", seg=18)
    box(2122, 2130, 1036, 1044, 26.6, 30, "louvre")                                       # enclosure ventilation outlet
    box(2152, 2156, 1019, 1045, 26.5, 26.7, "grating")
    rail([(2152, 1019), (2152, 1045)], 26.6)
    for k in range(int(26 / 1.0)):
        box(2172.4, 2173.2, 1040, 1042, k * 1.0 + .6, k * 1.0 + .7, "sp_yellow")          # ladder rungs (east wall)
    rod((2172.8, 1040, .6), (2172.8, 1040, 29), .06, "sp_yellow", seg=6)
    rod((2172.8, 1042, .6), (2172.8, 1042, 29), .06, "sp_yellow", seg=6)
    # electrical & control module (south), lube-oil cooler and fuel gas (north), fire-suppression cabinet
    box(2132, 2170, 1007, 1015, .6, 11, "ehouse"); box(2132, 2170, 1007, 1015, 11, 11.5, "roof")
    decal((2151, 1006.9, 9.4), (0, -1, 0), 20, 1.1, [("IG-1  ELECTRICAL & CONTROL MODULE", .6, True, "#111111")], bg="#ffffff")
    for k in range(5):
        x = 2140 + k * .5
        poly([(x, 1015, 8), (x, 1018, 8)], .1, "cable_tc", seg=6)
    fin_fan(2150, 2170, 1048, 1056)
    poly([(2160, 1048, 4), (2160, 1046, 4)], .4, "pipe", seg=10)
    gas_module(2124, 2140, 1049, 1055, "FUEL GAS  ·  CLASS I DIV 2")
    box(2112, 2116, 1012, 1016, .6, 7, "red")                                            # fire-suppression cabinet
    decal((2146, 1017.4, 20.5), (0, -1, 0), 24, 2.6, [("IG-1  ·  INDUSTRIAL GAS TURBINE", .46, True, "#111111"),
                                                      ("~50 MW  ·  13.8 kV", .3, False, "#333333")], bg="#ffffff")
    import maintenance as mt
    mt.person(2156, 1016, .6, 1.57)
    fuel.D = False
    return it


def build():
    n0 = len(fuel.G["parts"])
    ax1()
    ig1()
    return len(fuel.G["parts"]) - n0
