"""Two more modular gas-turbine package types for the modular yard (owner, Oct 24: "the other gas power plants on the
modular yard ... different modular ones"), in the open block between the collector e-house and the SC units:

- AX-1, a factory-modular aeroderivative package (LM2500XPRESS class, ~35 MW): it ships as a few pre-built modules
  (turbine / generator enclosure on its base, the inlet filter house set on top, exhaust collector and stack, a control
  module, lube-oil cooler and fuel-gas module), so the interconnects between modules are plug-and-play: the module
  joints are marked and the pre-terminated interconnect cables are visible at each joint;
- IG-1, an industrial gas-turbine package (Titan 250 class, ~23 MW): a single-lift skid in its enclosure, radial
  inlet with the filter house on top, exhaust up through a stack, control module, lube-oil cooler, fuel-gas module.

Both: 13.8 kV generator leads in MV-105 down into the yard duct bank to MOD-EH (routes in build_model), ARMOR-X MC-HL
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


def package(name, tag, info, X0, Y0, cfg):
    """One GT package on its pad. cfg: enclosure length / height, inlet position and size, stack radius / height,
    modular (marked module joints and plug-in interconnects)."""
    EL, EH, IX, IW, IH, SR, SH, modular, mw, kind = (cfg[k] for k in ("EL", "EH", "IX", "IW", "IH", "SR", "SH", "modular",
                                                                     "mw", "kind"))
    W = 14.0
    YC = Y0 + 24.0
    it = fuel.new_item(L, name, (X0 - 3, X0 + EL + 46, Y0 - 4, Y0 + 54), (0, SH + 1), area="I", register=False,
                       basis="typical", sheet="typical (modular expansion)", info=info)
    fuel.on(it)
    fuel.D = False
    box(X0, X0 + EL + 42, Y0, Y0 + 46, 0, .8, "concrete")                              # pad
    box(X0 + 8, X0 + 8 + EL, YC - W / 2, YC + W / 2, .8, EH, "machine")                 # enclosure (gen west, GT east)
    fuel.D = True
    xe = X0 + 8 + EL
    for x in range(int(X0) + 12, int(xe) - 2, 6):                                    # enclosure panel seams
        box(x - .1, x + .1, YC - W / 2 - .15, YC - W / 2, .8, EH, "steel")
    box(X0 + 10, X0 + 13, YC - W / 2 - .2, YC - W / 2, .8, 7.5, "steel_dark")          # access door
    # inlet filter house on top (modular: set as its own module), duct down into the compressor
    ix0 = X0 + 8 + IX
    louvre_box(ix0, ix0 + IW, YC - IW / 2 - 3, YC + IW / 2 + 3, EH, EH + IH)
    box(ix0 + 1, ix0 + IW - 1, YC - IW / 2 - 2, YC + IW / 2 + 2, EH + IH, EH + IH + .5, "roof")
    # exhaust collector and stack at the east end
    box(xe, xe + 9, YC - 5, YC + 5, .8, EH, "duct")
    rod((xe + 14, YC, 0), (xe + 14, YC, SH), SR, "stack", seg=28)
    rod((xe + 9, YC, EH * .6), (xe + 14 - SR, YC, EH * .6), 4.0, "duct", seg=20)
    rod((xe + 14, YC, SH - 2), (xe + 14, YC, SH - 1.2), SR + .25, "hero_accent", seg=28)
    rod((xe + 14, YC, SH * .55), (xe + 14, YC, SH * .55 + 4), SR + .4, "steel", seg=28)   # silencer band
    # generator terminal box at the west end; MV-105 leads down into the duct bank stub-ups
    box(X0 + 4, X0 + 8, YC - 3, YC + 3, 3, 9, "motor")
    for j in range(6):
        y = YC - 1.5 + j * .6
        poly([(X0 + 5, y, 3), (X0 + 5, y, 1.2), (X0 + 4, y, .2)], .2, "cable_mv", seg=8)
    for j in range(3):
        rod((X0 + 3.5, YC - 1.2 + j * 1.2, -.0), (X0 + 3.5, YC - 1.2 + j * 1.2, .9), .35, "pipe", seg=8)
    # control module, lube-oil cooler, fuel-gas module
    box(X0 + 8, X0 + 26, Y0 + 3, Y0 + 11, .8, 10, "ehouse")
    box(X0 + 8, X0 + 26, Y0 + 3, Y0 + 11, 10, 10.5, "roof")
    decal((X0 + 17, Y0 + 2.9, 8.6), (0, -1, 0), 14, 1.2, [(f"{tag}  CONTROL / MCC MODULE", .6, True, "#111111")], bg="#ffffff")
    for k in range(5):                                                               # TC-ER control to the enclosure
        x = X0 + 12 + k * .5
        poly([(x, Y0 + 11, 7), (x, Y0 + 13, 7), (x, YC - W / 2, 7)], .1, "cable_tc", seg=6)
    fin_fan(X0 + 12, X0 + 30, YC + W / 2 + 4, YC + W / 2 + 12)
    poly([(X0 + 21, YC + W / 2 + 4, 4), (X0 + 21, YC + W / 2, 4)], .4, "pipe", seg=10)  # lube oil
    poly([(X0 + 29.6, YC + W / 2 + 4.2, 6.6), (X0 + 29.6, YC + W / 2 + .2, 6.6)], .08, "cable_tc", seg=6)  # fan motor feed
    gas_module(xe - 16, xe - 2, YC + W / 2 + 4, YC + W / 2 + 10, "FUEL GAS  ·  CLASS I DIV 2")
    poly([(xe - 9, YC + W / 2 + 7, 2.6), (xe - 9, YC + W / 2, 2.6)], .35, "fuelgas", seg=10)
    # modular package: marked module joints with pre-terminated interconnects plugged across them
    if modular:
        for xj in (X0 + 8 + EL * .45, ix0):
            box(xj - .15, xj + .15, YC - W / 2 - .25, YC + W / 2 + .25, .8, EH + .2, "hero_accent")
            for k in range(3):
                y = YC - W / 2 - .35
                rod((xj - 1.2, y, 4 + k * 1.6), (xj + 1.2, y, 4 + k * 1.6), .12, ("cable_mv", "cable_tc", "cable_inst")[k], seg=6)
                box(xj - .4, xj + .4, y - .3, y, 3.6 + k * 1.6, 4.4 + k * 1.6, "sp_yellow")    # plug / receptacle
        decal((X0 + 8 + EL * .45 + 6, YC - W / 2 - .3, EH - 2.2), (0, -1, 0), 14, 1.1,
              [("MODULE JOINT  ·  PLUG-IN INTERCONNECTS", .6, True, "#111111")], bg="#ffd200")
    decal((X0 + 8 + EL * .3, YC - W / 2 - .35, EH * .55), (0, -1, 0), 26, 3.2,
          [(f"{tag}  ·  {kind}", .48, True, "#111111"), (f"~{mw} MW  ·  13.8 kV", .3, False, "#333333")], bg="#ffffff")
    import maintenance as mt
    mt.person(X0 + 15, Y0 + 13, .8, 1.57)
    fuel.D = False
    return it


def mirror_x(p0, d0, m, it):
    """Mirror everything built since (p0, d0) about the plane x = m (the SC-2 way: a mirrored twin of the west unit)."""
    f = lambda x: round(2 * m - x, 3)
    for p in fuel.G["parts"][p0:]:
        if "min" in p:
            p["min"][0], p["max"][0] = f(p["max"][0]), f(p["min"][0])
        for key in ("a", "b"):
            if key in p:
                p[key][0] = f(p[key][0])
        for v in p.get("v", ()):
            v[0] = f(v[0])
    for d in fuel.G.get("decals", [])[d0:]:
        d["c"][0] = f(d["c"][0])
        for key in ("n", "up"):
            if key in d:
                d[key][0] = -d[key][0]
    it["fp"] = [f(it["fp"][1]), f(it["fp"][0]), it["fp"][2], it["fp"][3]]


# Oct 24 (owner): a mirrored pair like SC-1 / SC-2, stacks facing each other and on the SC stack lines (x 2052, 2116.5)
SX_W, SX_E = 2052.0, 2116.5


def build():
    n0 = len(fuel.G["parts"])
    package("AX-1: factory-modular aeroderivative package, LM2500XPRESS class (~35 MW)", "AX-1",
            "Aeroderivative package delivered as a few factory modules (enclosure with turbine and generator, inlet filter "
            "house on top, exhaust and stack, control module, lube-oil cooler, fuel-gas module); module joints with "
            "pre-terminated plug-in interconnects; 13.8 kV MV-105 to MOD-EH, MC-HL at the gas module, TC-ER control.",
            SX_W - 68, 1008.0, dict(EL=46, EH=15, IX=26, IW=18, IH=14, SR=4.4, SH=60, modular=True, mw=35,
                                    kind="AERODERIVATIVE  ·  FACTORY MODULES"))
    p0, d0 = len(fuel.G["parts"]), len(fuel.G.get("decals", []))
    X0 = 2152.0
    it = package("IG-1: industrial gas-turbine package, Titan 250 class (~23 MW)", "IG-1",
                 "Single-lift industrial gas-turbine generator package in its enclosure, radial inlet with the filter house on "
                 "top, exhaust stack, control module, lube-oil cooler, fuel-gas module; 13.8 kV MV-105 to MOD-EH, MC-HL at the "
                 "gas module, TC-ER control. Mirrored twin layout of AX-1 (stacks facing).",
                 X0, 1008.0, dict(EL=46, EH=13, IX=26, IW=14, IH=11, SR=3.8, SH=50, modular=False, mw=23,
                                  kind="INDUSTRIAL GAS TURBINE"))
    mirror_x(p0, d0, ((X0 + 8 + 46 + 14) + SX_E) / 2, it)                            # stack (X0 + 68) onto x = SX_E
    return len(fuel.G["parts"]) - n0
