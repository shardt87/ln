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


def legs(x0, x1, y0, y1, zb, step=8.0):
    """A factory module standing on short legs: base frame at zb, legs every ~8 ft along both long edges."""
    box(x0, x1, y0, y1, zb - .35, zb, "steel_dark")
    n = max(1, int((x1 - x0) / step))
    for k in range(n + 1):
        x = x0 + .5 + k * (x1 - x0 - 1) / n
        for y in (y0 + .5, y1 - .5):
            box(x - .45, x + .45, y - .45, y + .45, .6, zb - .35, "steel_dark")


def ax1():
    """AX-1: compact modular aeroderivative (LM2500XPRESS class), rebuilt after the owner's package picture (Oct 28):
    separate factory modules on short legs, west to east: control platform with canopy and stair, inlet filter house
    with stacked weather hoods on its long faces, turbine module with a roof vent fan and an angled vent duct, the plain
    banded stack behind the exhaust end, the generator module with its door, stair and platform and a roof vent box with
    angled hoods, the auxiliary skids; lube cooler and fuel-gas module behind. Generator terminal box on the generator's
    south face (x 2051-2054), leads south to AX-GSU."""
    YC = 1032.0
    it = fuel.new_item(L, "AX-1: compact modular aeroderivative installation, LM2500XPRESS class (~35 MW)",
                       (1981, 2076, 1004, 1062), (0, 81), area="I", register=False, basis="typical", tag="AX-1",
                       sheet="typical (modular expansion)",
                       info="Aeroderivative gas-turbine generator delivered as factory modules on short legs: control "
                            "platform, inlet filter house with stacked weather hoods, turbine module with roof ventilation, "
                            "stack, generator module with roof vent hoods, auxiliary (lube / fuel) skids; module joints with "
                            "pre-terminated plug-in interconnects; 13.8 kV MV-105 to its unit step-up AX-GSU, MC-HL at the "
                            "gas module, TC-ER control.")
    fuel.on(it)
    fuel.D = False
    box(1981, 2076, 1008, 1056, 0, .6, "concrete")                                     # pad
    ZB = 3.6
    # control platform (west): open canopy over a grating deck, the unit control cabinet, stair to the south
    legs(1983, 1993, 1026, 1038, 5.0)
    box(1983, 1993, 1026, 1038, 4.8, 5.0, "grating")
    for (x, y) in ((1983.3, 1026.3), (1992.7, 1026.3), (1983.3, 1037.7), (1992.7, 1037.7)):
        box(x - .2, x + .2, y - .2, y + .2, 5, 13, "steel")
    box(1982.5, 1993.5, 1025.5, 1038.5, 13, 13.4, "roof")
    box(1986, 1990, 1031, 1036, 5, 11, "panel")                                        # control cabinet
    rail([(1993, 1026), (1993, 1038), (1983, 1038), (1983, 1026), (1986.5, 1026)], 5.0)
    stair(1988, 1026, 5.0, dy=-1)
    # inlet filter house: stacked weather hoods on both long faces, plain roof
    legs(1995, 2026, 1022, 1042, ZB)
    box(1995, 2026, 1022, 1042, ZB, 19, "filter")
    box(1995, 2026, 1022, 1042, 19, 19.5, "roof")
    hoods(1996, 2025, 1022, ZB, 19, -1)
    hoods(1996, 2025, 1042, ZB, 19, 1)
    box(2026, 2029, 1026, 1038, ZB, 15, "duct")                                        # inlet plenum to the turbine
    # turbine module: roof vent fan housing, angled vent duct, door with platform and stair
    legs(2029, 2048, 1024, 1040, ZB)
    box(2029, 2048, 1024, 1040, ZB, 16.5, "ehouse")
    box(2029, 2048, 1024, 1040, 16.5, 17, "roof")
    box(2031.5, 2038.5, 1028, 1036, 17, 21, "steel")                                    # vent fan housing
    rod((2035, YC, 21), (2035, YC, 23.6), 2.6, "steel", seg=16)
    rod((2035, YC, 23.6), (2035, YC, 24.1), 2.9, "fanhub", seg=16)
    box(2041, 2046, 1029, 1035, 17, 23, "duct")                                        # vent duct, angled outlet
    rod((2043.5, YC, 23), (2040.5, YC, 27.5), 2.4, "duct", seg=12)
    box(2033, 2036, 1023.85, 1024, ZB + .4, ZB + 7.6, "steel_dark")                    # turbine module door
    box(2031, 2040, 1019.5, 1024, ZB - .2, ZB, "grating")
    rail([(2031, 1024), (2031, 1019.5), (2040, 1019.5), (2040, 1024)], ZB)
    stair(2036.5, 1019.5, ZB, dy=-1)
    # exhaust collector north of the turbine's hot end, the plain banded stack behind the line
    box(2042, 2050, 1040, 1046, ZB, 15, "duct")
    box(2042.5, 2053.5, 1045, 1055, .6, 9, "steel_dark")                               # stack base / silencer box
    rod((2048, 1050, 9), (2048, 1050, 80), 4.6, "stack", seg=28)
    for z in (28, 46, 64):
        rod((2048, 1050, z), (2048, 1050, z + .5), 4.8, "steel", seg=28)                 # bands
    rod((2048, 1050, 79.4), (2048, 1050, 80.2), 4.9, "steel", seg=28)
    # generator module: door, platform and stair, roof vent box with angled hoods both sides, terminal box (south)
    legs(2050, 2068, 1024, 1040, ZB)
    box(2050, 2068, 1024, 1040, ZB, 15, "ehouse")
    box(2050, 2068, 1024, 1040, 15, 15.4, "roof")
    box(2055, 2063, 1027, 1037, 15.4, 22, "louvre")                                    # vent box
    box(2054.5, 2063.5, 1026.5, 1037.5, 22, 22.4, "roof")
    for s_ in (-1, 1):                                                                 # angled hoods both sides
        xa = 2055 if s_ < 0 else 2063
        rod((xa, YC, 20.5), (xa + s_ * 2.6, YC, 18.2), 2.3, "steel", seg=4)
    box(2057, 2060, 1023.85, 1024, ZB + .4, ZB + 7.6, "steel_dark")                    # generator module door
    box(2055.5, 2064, 1019.5, 1024, ZB - .2, ZB, "grating")
    rail([(2055.5, 1024), (2055.5, 1019.5), (2064, 1019.5), (2064, 1024)], ZB)
    stair(2061, 1019.5, ZB, dy=-1)
    box(2051, 2054, 1022.2, 1024, ZB + .5, ZB + 5.5, "motor")                          # generator terminal box
    for j in range(6):
        x = 2051.4 + j * .45
        poly([(x, 1023, ZB + .5), (x, 1023, 1.2), (x, 1021.4, .2)], .18, "cable_mv", seg=8)
    # auxiliary skids (east), lube-oil cooler and fuel-gas module behind
    legs(2069, 2075.5, 1025, 1039, 2.4)
    box(2069.3, 2075.2, 1026, 1038, 2.4, 8.5, "machine")
    box(2069.3, 2075.2, 1026, 1038, 8.5, 8.9, "roof")
    fin_fan(2027, 2040, 1045, 1053)
    gas_module(2057, 2073, 1045, 1051, "FUEL GAS  ·  CLASS I DIV 2")
    # control module (south-west, unchanged) with the control cables to the platform
    box(1990, 2010, 1010, 1017, .6, 10, "ehouse"); box(1990, 2010, 1010, 1017, 10, 10.5, "roof")
    decal((2000, 1009.9, 8.4), (0, -1, 0), 14, 1.1, [("AX-1  CONTROL MODULE", .6, True, "#111111")], bg="#ffffff")
    for k in range(5):
        x = 1996 + k * .5
        poly([(x, 1017, 7), (x, 1020, 7), (x, 1020, 5.3)], .1, "cable_tc", seg=6)
    # module joints with plug-in interconnects (south face)
    for xj in (2028.9, 2049):
        for k in range(3):
            rod((xj - 1.0, 1023.6, ZB + 2 + k * 1.6), (xj + 1.0, 1023.6, ZB + 2 + k * 1.6), .12,
                ("cable_mv", "cable_tc", "cable_inst")[k], seg=6)
            box(xj - .4, xj + .4, 1023.3, 1023.6, ZB + 1.6 + k * 1.6, ZB + 2.4 + k * 1.6, "sp_yellow")
    decal((2059, 1023.8, 12.4), (0, -1, 0), 14, 2.2, [("AX-1  ·  COMPACT MODULAR AERODERIVATIVE", .42, True, "#111111"),
                                                      ("~35 MW  ·  13.8 kV  ·  factory modules", .3, False, "#333333")], bg="#ffffff")
    import maintenance as mt
    mt.person(2059, 1021.5, ZB, 1.57)
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
