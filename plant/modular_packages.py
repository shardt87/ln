"""Two more modular gas-turbine package types for the modular yard (owner, Oct 24: "the other gas power plants on the
modular yard ... different modular ones"), in the open block between the collector e-house and the SC units:

- AX-1, a compact modular aeroderivative installation (~35 MW class, ~35 MW; owner reference pictures Oct 27):
  factory modules standing on a raised steel base with stairs and yellow-railed walkways: the inlet filter module with
  its stacked weather hoods, the turbine module with its ventilation fans and ducts on the roof, the exhaust plenum and
  a tall banded stack, the generator module with its doors, the lube / fuel auxiliary skid and the control module;
  the module joints carry pre-terminated plug-in interconnects;
- IG-1, an industrial gas-turbine installation (~50 MW class, ~50 MW; owner reference pictures Oct 27): the
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


def hoods(x0, x1, y, z0, z1, side, pitch=1.45):
    """Weather hoods on a filter face at y (side -1 = south face, +1 = north face): even rows of box hoods (sloped-
    looking top, front skirt, dark filter face behind), the way a filter house is clad (Oct 29: the old stacked
    blades read as shelves)."""
    _hood_rows(x0, x1, y, z0, z1, side, "y", pitch)


def hoods_x(y0, y1, x, z0, z1, side, pitch=1.45):
    """The same on a face at x (side -1 = west face, +1 = east face)."""
    _hood_rows(y0, y1, x, z0, z1, side, "x", pitch)


def _hood_rows(a0, a1, f, z0, z1, side, axis, pitch):
    def B(u0, u1, v0, v1, za, zb, c):
        if axis == "y":
            box(u0, u1, min(v0, v1), max(v0, v1), za, zb, c)
        else:
            box(min(v0, v1), max(v0, v1), u0, u1, za, zb, c)
    B(a0 + .3, a1 - .3, f, f + side * .12, z0 + .6, z1 - .4, "louvre")                 # filter face
    z = z0 + .8
    while z + pitch <= z1 - .2:
        B(a0 + .2, a1 - .2, f, f + side * .85, z + pitch - .22, z + pitch - .12, "steel")      # hood top
        B(a0 + .2, a1 - .2, f + side * .75, f + side * .85, z + pitch - .62, z + pitch - .12, "steel")   # skirt
        B(a0 + .2, a1 - .2, f + side * .12, f + side * .85, z + pitch - .12, z + pitch - .06, "filter")  # top flashing
        z += pitch
    for u in (a0 + .2, a1 - .35):                                                           # end cheeks
        B(u, u + .15, f, f + side * .85, z0 + .6, z - .1, "steel")


def fascia(x0, x1, y0, y1, z, h=.7, c="steel_dark"):
    """Light roof slab with a dark fascia band round its edge (the two-tone package look)."""
    box(x0, x1, y0, y1, z, z + .4, "roof")
    for (a, b, cc, d) in ((x0 - .1, x1 + .1, y0 - .1, y0 + .05), (x0 - .1, x1 + .1, y1 - .05, y1 + .1),
                          (x0 - .1, x0 + .05, y0, y1), (x1 - .05, x1 + .1, y0, y1)):
        box(a, b, cc, d, z + .4 - h, z + .4, c)


def legs(x0, x1, y0, y1, zb, step=8.0):
    """A factory module standing on short legs: base frame at zb, legs every ~8 ft along both long edges."""
    box(x0, x1, y0, y1, zb - .35, zb, "steel_dark")
    n = max(1, int((x1 - x0) / step))
    for k in range(n + 1):
        x = x0 + .5 + k * (x1 - x0 - 1) / n
        for y in (y0 + .5, y1 - .5):
            box(x - .45, x + .45, y - .45, y + .45, .6, zb - .35, "steel_dark")


def ax1():
    """AX-1: compact modular aeroderivative (~35 MW class), rebuilt after the owner's package picture (Oct 28):
    separate factory modules on short legs, west to east: control platform with canopy and stair, inlet filter house
    with stacked weather hoods on its long faces, turbine module with a roof vent fan and an angled vent duct, the plain
    banded stack behind the exhaust end, the generator module with its door, stair and platform and a roof vent box with
    angled hoods, the auxiliary skids; lube cooler and fuel-gas module behind. Generator terminal box on the generator's
    south face (x 2051-2054), leads south to AX-GSU."""
    YC = 1032.0
    it = fuel.new_item(L, "AX-1: compact modular aeroderivative installation, ~35 MW class (~35 MW)",
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
    # inlet filter house raised on a braced frame (the compact package's signature profile), inlet plenum dropping
    # into the turbine module (Oct 30)
    ZF = 12.0
    for x in (1995.6, 2010.5, 2025.4):
        for y in (1022.6, 1041.4):
            box(x - .45, x + .45, y - .45, y + .45, .6, ZF - .35, "steel")
            box(x - .8, x + .8, y - .8, y + .8, .6, 1.0, "steel_dark")
    for y in (1022.6, 1041.4):
        for (xa, xb) in ((1995.6, 2010.5), (2010.5, 2025.4)):
            rod((xa, y, 1.4), (xb, y, ZF - .8), .16, "steel", seg=6); rod((xb, y, 1.4), (xa, y, ZF - .8), .16, "steel", seg=6)
    box(1995, 2026, 1022, 1042, ZF - .35, ZF, "steel_dark")                            # frame deck
    box(1995, 2026, 1022, 1042, ZF, 27, "filter")
    box(1994.8, 2026.2, 1021.8, 1042.2, 27, 27.5, "roof")
    box(1995, 2026, 1021.9, 1042.1, ZF, ZF + .9, "gen_paint")                          # base skirt
    hoods(1996, 2025, 1022, ZF + .9, 27, -1)
    hoods(1996, 2025, 1042, ZF + .9, 27, 1)
    hoods_x(1023, 1041, 1995, ZF + .9, 27, -1)
    box(2026, 2029.5, 1026, 1038, 15, 25, "duct")                                      # inlet plenum
    box(2029.5, 2033, 1026, 1038, 17, 25, "duct")                                      # elbow onto the turbine roof
    for z in (15, 20, 25):
        box(2025.8, 2029.7, 1025.8, 1038.2, z - .2, z + .2, "steel")                     # flanges
    # turbine module: roof vent fan housing, angled vent duct, door with platform and stair
    legs(2029, 2048, 1024, 1040, ZB)
    box(2029, 2048, 1024, 1040, ZB, 16.5, "ehouse")
    fascia(2029, 2048, 1024, 1040, 16.5)
    box(2028.9, 2048.1, 1023.9, 1040.1, ZB, ZB + 1.6, "gen_paint")                       # base skirt
    box(2031.5, 2038.5, 1028, 1036, 17, 21, "steel")                                    # vent fan housing
    rod((2035, YC, 21), (2035, YC, 23.6), 2.6, "steel", seg=16)
    rod((2035, YC, 23.6), (2035, YC, 24.1), 2.9, "fanhub", seg=16)
    box(2041, 2046, 1029, 1035, 17, 24, "duct")                                        # vent outlet duct
    box(2040.4, 2046.6, 1028.4, 1035.6, 24, 24.4, "steel")                               # flange
    box(2040.8, 2046.2, 1028.8, 1035.2, 25.6, 26, "steel")                               # rain hood over the outlet
    for (x, y) in ((2041, 1029), (2046, 1029), (2041, 1035), (2046, 1035)):
        box(x - .1, x + .1, y - .1, y + .1, 24.4, 25.6, "steel")
    box(2033, 2036, 1023.85, 1024, ZB + .4, ZB + 7.6, "steel_dark")                    # turbine module door
    box(2031, 2040, 1019.5, 1024, ZB - .2, ZB, "grating")
    rail([(2031, 1024), (2031, 1019.5), (2040, 1019.5), (2040, 1024)], ZB)
    stair(2036.5, 1019.5, ZB, dy=-1)
    # exhaust collector north of the turbine's hot end, the plain banded stack behind the line
    box(2042, 2050, 1040, 1045, ZB, 15, "duct")                                        # exhaust collector
    box(2041.8, 2050.2, 1044.6, 1045.4, ZB - .2, 15.2, "hdpe")                          # expansion joint
    box(2042.5, 2053.5, 1045.4, 1055, .6, 16, "duct")                                  # transition / silencer box
    for z in (5, 10.5):
        box(2042.3, 2053.7, 1045.2, 1055.2, z, z + .4, "steel")                          # stiffener bands
    box(2042, 2054, 1044.9, 1055.5, .6, 1.4, "concrete")
    rod((2048, 1050, 16), (2048, 1050, 19), 5.4, "duct", r2=4.6, seg=28)                  # transition to round
    rod((2048, 1050, 19), (2048, 1050, 80), 4.6, "stack", seg=28)
    for k in range(int((54 - 2) / 1.2)):                                                    # caged ladder (north side)
        box(2046.6, 2049.4, 1054.7, 1054.9, 2 + k * 1.2, 2.1 + k * 1.2, "sp_yellow")
    for x in (2046.6, 2049.4):                                                              # ladder side rails
        rod((x, 1054.8, 2), (x, 1054.8, 55), .06, "sp_yellow", seg=4)
    for k in range(9):                                                                      # cage hoops
        z = 10 + k * 5
        poly([(2046.4, 1054.8, z), (2046.4, 1057.0, z), (2049.6, 1057.0, z), (2049.6, 1054.8, z)], .05, "sp_yellow", seg=4)
    for x in (2046.4, 2048, 2049.6):
        rod((x, 1057.0, 10), (x, 1057.0, 54), .04, "sp_yellow", seg=4)
    box(2044, 2052, 1054.6, 1057.5, 54, 54.3, "grating")                                 # sampling platform
    rail([(2044, 1054.6), (2044, 1057.5), (2052, 1057.5), (2052, 1054.6)], 54.3)
    for z in (28, 46, 64):
        rod((2048, 1050, z), (2048, 1050, z + .5), 4.8, "steel", seg=28)                 # bands
    rod((2048, 1050, 79.4), (2048, 1050, 80.2), 4.9, "steel", seg=28)
    # generator module: door, platform and stair, roof vent box with angled hoods both sides, terminal box (south)
    legs(2050, 2068, 1024, 1040, ZB)
    box(2050, 2068, 1024, 1040, ZB, 15, "ehouse")
    fascia(2050, 2068, 1024, 1040, 15)
    box(2049.9, 2068.1, 1023.9, 1040.1, ZB, ZB + 1.6, "gen_paint")                       # base skirt
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
    # fuel gas from the module, on sleepers under the exhaust collector, up into the turbine module; lube supply /
    # return from the cooler into the turbine module (Oct 30)
    poly([(2059, 1045, 1.2), (2059, 1042.5, 1.2), (2040, 1042.5, 1.2), (2040, 1039, 1.2), (2040, 1039, ZB - .4)], .3,
         "fuelgas", seg=10)
    for x in (2048, 2054):
        box(x - .3, x + .3, 1042, 1043, .6, .9, "concrete")
    for dx in (-.6, .6):
        poly([(2033.4 + dx, 1045, 3.0), (2033.4 + dx, 1041, 3.0), (2033.4 + dx, 1041, 5.0), (2033.4 + dx, 1040.05, 5.0)],
             .25, "fueloil", seg=8)
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
    """IG-1: industrial gas-turbine installation (~50 MW class), west to east: stack, exhaust diffuser, the
    turbine-generator building (generator at the east end, terminal box at x 2176-2181), with the filter house raised on
    its steel frame above the compressor end; E&C module south, lube-oil cooler and fuel gas north."""
    YC = 1032.0
    it = fuel.new_item(L, "IG-1: industrial gas-turbine installation, ~50 MW class (~50 MW)",
                       (2092, 2188, 1004, 1062), (0, 80), area="I", register=False, basis="typical", tag="IG-1",
                       sheet="typical (modular expansion)",
                       info="Industrial gas-turbine generator in its building: combustion-air filter house raised on a steel "
                            "frame with inclined filter faces, exhaust diffuser through the end wall into a tall stack, generator "
                            "air coolers and enclosure ventilation on the roof, electrical and control module, lube-oil cooler, "
                            "fuel-gas module; 13.8 kV MV-105 to its unit step-up AX-GSU, MC-HL at the gas module, TC-ER control.")
    fuel.on(it)
    fuel.D = False
    box(2092, 2188, 1006, 1058, 0, .6, "concrete")
    # turbine-generator building: clad steel, panel seams all round, intake louvres at the turbine end, personnel
    # doors, a roll-up door at the generator end (north), roof edge
    box(2120, 2172, 1018, 1046, .6, 26, "ehouse")
    fascia(2119.6, 2172.4, 1017.6, 1046.4, 26, h=1.0)
    box(2119.6, 2172.4, 1017.6, 1046.4, 26.4, 26.6, "roof")
    box(2119.8, 2172.2, 1017.8, 1046.2, .6, 3.2, "gen_paint")                             # base skirt
    for x in range(2124, 2172, 4):
        box(x - .08, x + .08, 1017.8, 1018, .6, 26, "steel")                               # south seams
        box(x - .08, x + .08, 1046, 1046.2, .6, 26, "steel")                               # north seams
    for y in range(1022, 1046, 4):
        box(2119.8, 2120, y - .08, y + .08, .6, 26, "steel")                               # west seams
    box(2120, 2172, 1017.75, 1018, 12.8, 13.1, "steel"); box(2120, 2172, 1046, 1046.25, 12.8, 13.1, "steel")
    for x0 in (2123, 2135):                                                                # enclosure air intakes
        box(x0, x0 + 9, 1017.7, 1018, 15, 22, "louvre"); box(x0, x0 + 9, 1046, 1046.3, 15, 22, "louvre")
        box(x0 - .2, x0 + 9.2, 1016.9, 1018, 22, 22.3, "steel"); box(x0 - .2, x0 + 9.2, 1046, 1047.1, 22, 22.3, "steel")
    box(2160, 2166, 1017.6, 1018, .6, 9, "steel_dark")                                   # double door (south)
    box(2159.4, 2166.6, 1016.4, 1018, 9.2, 9.5, "steel")                                 # door canopy
    box(2150, 2166, 1046, 1046.4, .6, 18, "rollup")                                      # roll-up door (north)
    for z in range(2, 18, 2):
        box(2150, 2166, 1046.4, 1046.5, z, z + .1, "steel")
    box(2149.4, 2166.6, 1046, 1046.8, 18, 19, "steel")                                   # door head box
    box(2172, 2176, 1028, 1036, 2, 10, "motor"); box(2176, 2181, 1029, 1035, 3, 9, "motor")   # generator terminal box
    box(2172.2, 2175.8, 1037.5, 1041.5, .6, 8, "panel")                                  # neutral grounding cubicle
    for j in range(6):
        y = 1030.5 + j * .6
        poly([(2180, y, 3), (2180, y, 1.2), (2180.4, y, .2)], .2, "cable_mv", seg=8)
    # combustion-air filter house on its braced frame over the compressor end: weather hoods on three faces, an
    # outlet transition and silencer below, and the flanged inlet duct down into the enclosure roof
    for x in (2126, 2150):
        for y in (1019, 1045):
            box(x - .6, x + .6, y - .6, y + .6, 26.6, 40, "steel")
            box(x - 1, x + 1, y - 1, y + 1, 26.6, 27.2, "steel_dark")                       # base plates
    for (xa, xb, y) in ((2126, 2150, 1019), (2126, 2150, 1045)):                          # X-bracing, long faces
        rod((xa, y, 27.5), (xb, y, 38.8), .22, "steel", seg=6); rod((xb, y, 27.5), (xa, y, 38.8), .22, "steel", seg=6)
    for x in (2126, 2150):                                                                 # X-bracing, short faces
        rod((x, 1019, 27.5), (x, 1045, 38.8), .22, "steel", seg=6); rod((x, 1045, 27.5), (x, 1019, 38.8), .22, "steel", seg=6)
    box(2125, 2151, 1018.5, 1045.5, 39.4, 40, "steel_dark")                              # deck frame
    box(2125, 2151, 1018.5, 1045.5, 40, 40.15, "grating")
    box(2127, 2149, 1022, 1042, 40.15, 56, "filter")                                     # filter house body
    for x in range(2129, 2149, 4):
        box(x - .06, x + .06, 1021.9, 1022, 40.2, 56, "steel"); box(x - .06, x + .06, 1042, 1042.1, 40.2, 56, "steel")
    box(2126.6, 2149.4, 1021.6, 1042.4, 56, 56.6, "roof")
    hoods(2127, 2149, 1022, 41, 55.5, -1)
    hoods(2127, 2149, 1042, 41, 55.5, 1)
    hoods_x(1023, 1041, 2127, 41, 55.5, -1)
    box(2149, 2149.15, 1030.5, 1033.5, 40.4, 47.4, "steel_dark")                         # filter-house access door (east)
    box(2148.9, 2149.25, 1030.3, 1033.7, 47.4, 47.7, "steel")
    rail([(2125, 1018.5), (2151, 1018.5), (2151, 1045.5), (2125, 1045.5), (2125, 1018.5)], 40.15)
    box(2131, 2145, 1026, 1038, 33.5, 39.4, "duct")                                     # outlet transition (hopper)
    box(2132.5, 2143.5, 1027.5, 1036.5, 26.6, 33.5, "duct")                              # inlet silencer section
    for z in (26.6, 30, 33.5):
        box(2132.2, 2143.8, 1027.2, 1036.8, z, z + .35, "steel")                         # duct flanges
    box(2131.5, 2144.5, 1026.5, 1037.5, 26.6, 27.4, "steel_dark")                        # roof curb
    # stair tower to the filter-house deck: north-west corner, beside the exhaust duct, four flights with landings,
    # and a bridge over the enclosure roof to the deck
    X0, X1, Y0 = 2111.0, 2119.0, 1041.5
    levels = (.6, 10.6, 20.6, 30.6, 40.15)
    for k in range(4):
        z0, z1 = levels[k], levels[k + 1]
        n = int((z1 - z0) / .65)
        yb = Y0 if k % 2 == 0 else Y0 + 4.4
        for j in range(n):
            zz = z0 + (j + 1) * (z1 - z0) / n
            t = (j + .5) / n
            xx = X0 + .6 + t * (X1 - X0 - 1.2) if k % 2 == 0 else X1 - .6 - t * (X1 - X0 - 1.2)
            box(xx - .35, xx + .35, yb, yb + 3.4, zz - .12, zz, "grating")
        if k < 3:
            box(X0, X1, Y0, Y0 + 7.8, z1 - .15, z1, "grating")                          # landing
    for (x, y) in ((X0, Y0), (X1, Y0), (X0, Y0 + 7.8), (X1, Y0 + 7.8)):
        box(x - .3, x + .3, y - .3, y + .3, .6, 43.5, "steel")
    for z in (10.6, 20.6, 30.6):
        rail([(X0, Y0 + 7.8), (X1, Y0 + 7.8), (X1, Y0)], z)
    box(X1, 2125, 1042, 1045, 39.9, 40.15, "grating")                                    # bridge to the deck
    rail([(X1, 1042), (2125, 1042)], 40.15); rail([(X1, 1045), (2125, 1045)], 40.15)
    # exhaust: rectangular diffuser outlet through the west wall, expansion joint, exhaust duct with stiffeners into
    # the stack breeching; stack on its pedestal with bands, a caged ladder and the emissions-test platform
    box(2112, 2120, 1024, 1040, 3, 20, "duct")                                          # exhaust duct
    box(2117.2, 2118, 1023.6, 1040.4, 2.6, 20.4, "hdpe")                                 # expansion joint
    for x in (2113.5, 2115.5):
        box(x, x + .3, 1023.8, 1040.2, 2.8, 20.2, "steel")                                # stiffeners
    box(2112.2, 2117.2, 1023.8, 1040.2, 20, 20.4, "steel")
    box(2108, 2112, 1025, 1039, 3, 19, "duct")                                          # breeching into the stack
    box(2093.5, 2108.5, 1024.5, 1039.5, .6, 2.4, "concrete")                             # stack pedestal
    rod((2101, YC, 2.4), (2101, YC, 78), 7.0, "stack", seg=32)
    for z in (22, 37, 52, 66):
        rod((2101, YC, z), (2101, YC, z + .6), 7.25, "steel", seg=32)                     # bands
    rod((2101, YC, 77), (2101, YC, 78.2), 7.3, "hero_accent", seg=32)
    for k in range(int((60 - 3) / 1.2)):                                                   # caged ladder (south side)
        box(2099.6, 2102.4, YC - 7.3, YC - 7.1, 3 + k * 1.2, 3.1 + k * 1.2, "sp_yellow")
    for k in range(10):
        z = 8 + k * 5.4
        rod((2099.4, YC - 7.2, z), (2099.4, YC - 9.4, z), .05, "sp_yellow", seg=4)
        rod((2102.6, YC - 7.2, z), (2102.6, YC - 9.4, z), .05, "sp_yellow", seg=4)
    rod((2099.4, YC - 9.4, 8), (2099.4, YC - 9.4, 60), .05, "sp_yellow", seg=4)
    rod((2102.6, YC - 9.4, 8), (2102.6, YC - 9.4, 60), .05, "sp_yellow", seg=4)
    box(2095, 2107, YC - 10.4, YC - 7.0, 60, 60.3, "grating")                            # emissions-test platform
    rail([(2095, YC - 7.2), (2095, YC - 10.4), (2107, YC - 10.4), (2107, YC - 7.2)], 60.3)
    for dx in (-3, 0, 3):
        rod((2101 + dx, YC - 6.9, 61.5), (2101 + dx, YC - 7.6, 61.5), .35, "steel", seg=8)   # sampling ports
    # roof: generator air coolers (two fans), two enclosure ventilation fans, walkway with rails and a ladder
    box(2156, 2170, 1022, 1042, 26.6, 27.4, "steel_dark")
    box(2156.4, 2169.6, 1022.4, 1041.6, 27.4, 31, "radiator")
    for y in (1027, 1037):
        rod((2163, y, 31), (2163, y, 31.8), 3.6, "steel", seg=20)
        rod((2163, y, 31.8), (2163, y, 32.0), 3.2, "fanhub", seg=20)
    for x in (2122.5, 2128.5):                                                             # enclosure vent fans
        box(x - 2.2, x + 2.2, 1037.5, 1041.9, 26.6, 28, "steel")
        rod((x, 1039.7, 28), (x, 1039.7, 31.5), 1.8, "duct", seg=16)
        rod((x, 1039.7, 31.5), (x, 1039.7, 31.9), 2.2, "steel", seg=16)
    box(2152, 2156, 1019, 1045, 26.6, 26.75, "grating")
    rail([(2152, 1019), (2152, 1045)], 26.6)
    for k in range(int(26 / 1.0)):
        box(2172.4, 2173.2, 1040, 1042, k * 1.0 + .6, k * 1.0 + .7, "sp_yellow")          # ladder rungs (east wall)
    rod((2172.8, 1040, .6), (2172.8, 1040, 29), .06, "sp_yellow", seg=6)
    rod((2172.8, 1042, .6), (2172.8, 1042, 29), .06, "sp_yellow", seg=6)
    # electrical & control module (south), lube-oil cooler and fuel gas (north), CO2 fire-suppression skid
    box(2132, 2170, 1007, 1015, .6, 11, "ehouse"); fascia(2132, 2170, 1007, 1015, 11)
    box(2131.9, 2170.1, 1006.9, 1015.1, .6, 2.2, "gen_paint")
    box(2140, 2146, 1015, 1018, 12, 12.4, "steel")                                       # cable tray to the building
    for x in (2140.3, 2145.7):
        box(x - .15, x + .15, 1014.6, 1015, 11.5, 12.4, "steel")
    for x in range(2135, 2170, 4):
        box(x - .06, x + .06, 1006.9, 1007, 1, 11, "steel")
    box(2134, 2137, 1006.85, 1007, 1.2, 8.2, "steel_dark")                               # module door
    box(2170, 2172.5, 1009, 1013, 4, 9, "machine")                                       # module HVAC
    decal((2151, 1006.9, 9.4), (0, -1, 0), 20, 1.1, [("IG-1  ELECTRICAL & CONTROL MODULE", .6, True, "#111111")], bg="#ffffff")
    for k in range(5):
        x = 2140 + k * .5
        poly([(x, 1015, 8), (x, 1018, 8)], .1, "cable_tc", seg=6)
    fin_fan(2150, 2170, 1048, 1056)
    for dx in (-.6, .6):                                                                   # lube supply / return
        poly([(2168 + dx, 1048, 3.5), (2168 + dx, 1046.2, 3.5)], .3, "fueloil", seg=10)
    gas_module(2124, 2140, 1049, 1055, "FUEL GAS  ·  CLASS I DIV 2")
    poly([(2140, 1052, 2.6), (2142.5, 1052, 2.6), (2142.5, 1052, 7), (2142.5, 1046.2, 7)], .35, "fuelgas", seg=10)
    box(2142, 2143, 1048.4, 1049.2, .6, 6.6, "steel")                                    # pipe support
    box(2109, 2117, 1009, 1015.5, .6, 1.2, "steel_dark")                                 # CO2 skid frame
    for i in range(4):
        for j in range(2):
            rod((2110.2 + i * 1.9, 1010.6 + j * 3.2, 1.2), (2110.2 + i * 1.9, 1010.6 + j * 3.2, 6.6), .7, "red", seg=14)
            rod((2110.2 + i * 1.9, 1010.6 + j * 3.2, 6.6), (2110.2 + i * 1.9, 1010.6 + j * 3.2, 7.2), .25, "steel", seg=8)
    box(2109, 2117, 1009, 1015.5, 7.6, 7.8, "steel")                                     # manifold rack
    poly([(2113, 1015.5, 7.4), (2113, 1017.2, 7.4), (2119.6, 1017.2, 7.4)], .15, "red", seg=8)   # discharge header
    decal((2113, 1008.9, 4), (0, -1, 0), 6, .9, [("CO2 FIRE SUPPRESSION", .45, True, "#ffffff")], bg="#b8322a")
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
