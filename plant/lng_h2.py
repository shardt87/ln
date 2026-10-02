"""LNG satellite and 25 MW green hydrogen at LOD 3 (detail cycle 9).

LNG:
- Eight horizontal vacuum-jacketed tanks: dished heads, a valve / instrument cabinet at the south
  end with fill and withdrawal lines, PSVs on the top, level-gauge box, tank ID plate; the liquid
  lines gather into a frost-white header inside the impoundment.
- Unloading skid: two articulated loading arms reaching over the truck bays, hose rack, ESD box.
- Ambient vaporizers: finned columns with top / bottom manifolds and a glycol trim heater.
- Send-out pumps: submerged-motor pump pots with motors and suction / discharge spools.
- Boil-off gas compressor: skid with compressor, motor and a knock-out drum.
- Impoundment: high-expansion foam generator, gas detectors, hazard signs.
Hydrogen:
- Electrolyzer building: ridge vents (hydrogen rises), wall louvres, gas detectors, an outdoor H2
  header to the dryer (new `hydrogen` routes: building to dryer, dryer to the compressors,
  compressors to the tube banks).
- H2 dryer: twin adsorber towers with a regeneration heater on a skid.
- Compressor containers: doors, vents, roof coolers.
- Tube banks: end frames and manifolds with isolation valves.
All typical, not engineered.
"""
import fuel
import wiring as W
from fuel import box, rod, find, on, strip, pipe

SHEET = "typical (LNG / H2 detail)"


def dress(flag):
    fuel.D = flag


def routes(add_route):
    add_route("hydrogen", [(2170, 1500), (2235, 1500), (2235, 1480), (2240, 1480)], layer="OPT_H2_ROUTES", sheet=SHEET)
    add_route("hydrogen", [(2280, 1480), (2285, 1480), (2285, 1504), (2290, 1504)], layer="OPT_H2_ROUTES", sheet=SHEET)
    add_route("hydrogen", [(2312, 1523), (2312, 1560)], layer="OPT_H2_ROUTES", sheet=SHEET)
    # rectifier transformer to rectifier (13.8 kV) and rectifier to stack (DC bus), in floor trenches
    for k in range(5):
        x = 2020 + 20 * k
        add_route("mvlv_cable", [(x + 2 * k + 6, 1530), (x + 2 * k + 6, 1518), (x + 4, 1518), (x + 4, 1505)],
                  layer="OPT_H2_ROUTES", sheet=SHEET)
        add_route("mvlv_cable", [(x + 4, 1490), (x + 4, 1478)], layer="OPT_H2_ROUTES", sheet=SHEET)


def lng():
    for k in range(8):
        x = 2130 + 20 * k
        cx = x + 6.25
        it = find(f"LNG 11: tank {k+1},")
        on(it)
        dress(True)
        rod((cx, 1747, 11), (cx, 1745.2, 11), 6.25, "tank", r2=3.4, seg=20)          # dished heads
        rod((cx, 1820.6, 11), (cx, 1822.4, 11), 6.25, "tank", r2=3.4, seg=20)
        box(cx - 2.5, cx + 2.5, 1741, 1744.6, .3, 7.5, "cabinet")                     # valve / instrument cabinet
        for dxl, c in ((-1.4, "lamp"), (1.4, "lamp")):                                 # fill / withdrawal (frosted)
            rod((cx + dxl, 1745.5, 6), (cx + dxl, 1745.5, 1.5), .35, c, seg=8)
            rod((cx + dxl, 1745.5, 1.5), (cx + dxl, 1739, 1.5), .35, c, seg=8)
        for yp in (1760, 1800):                                                        # PSVs on top
            rod((cx, yp, 17.2), (cx, yp, 19), .3, "steel", seg=8)
            rod((cx, yp, 19), (cx, yp, 20.3), .4, "red", seg=8)
        rod((cx - 1, 1802, 20), (cx - 1, 1802, 24), .2, "steel", seg=6)                # vent riser to header
        box(cx + 5.5, cx + 6.6, 1752, 1754, 5, 8, "panel")                             # level gauge box
        box(cx - 1.5, cx + 1.5, 1745.0, 1745.1, 9, 11, "sign")                         # tank ID plate
        dress(False)
    on(find("LNG 12: spill impoundment"))
    dress(True)
    rod((2128, 1739, 1.5), (2286, 1739, 1.5), .6, "lamp", seg=10)                       # liquid header (frosted)
    rod((2128, 1739, 1.5), (2128, 1739, 4.5), .6, "lamp", seg=10)
    rod((2128, 1802, 24), (2286, 1802, 24), .25, "steel", seg=6)                        # PSV vent header
    box(2120, 2128, 1820, 1830, .3, 7, "steel")                                         # hi-ex foam generator
    rod((2124, 1820, 4), (2124, 1814, 4), 2.2, "red", seg=14)
    for (x, y) in ((2118, 1740), (2295, 1740), (2118, 1832), (2295, 1832), (2205, 1734)):   # gas detectors
        rod((x, y, 0), (x, y, 5), .1, "steel", seg=4)
        box(x - .4, x + .4, y - .4, y + .4, 5, 5.9, "amber")
    for x in (2140, 2240):                                                              # hazard signs on the wall
        box(x, x + 4, 1731.9, 1732, 1.2, 3.6, "sign")
        box(x, x + 4, 1731.85, 1731.9, 3.0, 3.6, "red")
    dress(False)
    # unloading skid: loading arms over the bays, hose rack, ESD box
    on(find("LNG 10: unloading skid"))
    dress(True)
    for (xa, xb) in ((1895, 1880), (1915, 1960)):
        rod((xa, 1722, 8), (xa, 1722, 18), .7, "steel", seg=10)                         # riser
        rod((xa, 1722, 18), ((xa + xb) / 2, 1714, 22), .45, "lamp", seg=10)             # inner arm
        rod(((xa + xb) / 2, 1714, 22), (xb, 1706, 6), .45, "lamp", seg=10)              # outer arm
        rod((xa, 1722, 20), ((xa + xb) / 2, 1716, 26), .25, "steel", seg=6)             # counterweight link
        box(xa - 1.2, xa + 1.2, 1723.5, 1726, 12, 14.5, "machine")                      # counterweight
    box(1928, 1931, 1720, 1724, 0, 6, "steel")                                          # hose rack
    for h in range(3):
        rod((1929.5, 1720.5 + h, 5.5), (1929.5, 1720.5 + h, 1), .25, "fanhub", seg=6)
    box(1884, 1885, 1716, 1718, 3, 5.5, "red")                                          # ESD push-button
    dress(False)
    # ambient vaporizers rebuilt as finned columns (star fins, frosted), manifolds and trim heater
    it = find("LNG 14: vaporizers")
    strip(it)
    on(it)
    box(1880, 1990, 1760, 1820, 0, 1, "concrete")
    box(1886, 1984, 1798, 1816, 1, 12, "equip")                                          # glycol trim heater
    dress(True)
    for k in range(4):
        x0 = 1886 + 26 * k
        for f in range(3):
            for g in range(4):
                cx, cy = x0 + 3 + f * 6, 1767 + 3 + g * 6
                box(cx - 2.3, cx + 2.3, cy - .12, cy + .12, 1, 30, "lamp")             # fins (frost)
                box(cx - .12, cx + .12, cy - 2.3, cy + 2.3, 1, 30, "lamp")
                rod((cx, cy, 1), (cx, cy, 30.4), .3, "steel", seg=6)                     # core tube
        box(x0, x0 + 18, 1765, 1791, 29.6, 30, "steel")                                  # top frame
        rod((x0, 1764.5, 2), (x0 + 18, 1764.5, 2), .5, "lamp", seg=8)                   # inlet (LNG) manifold
        rod((x0, 1791.5, 29), (x0 + 18, 1791.5, 29), .5, "pipe", seg=8)                 # outlet (gas) manifold
    dress(False)
    for name, kind in (("LNG 13: send-out pumps", "pump"), ("LNG 15: boil-off gas compressor", "bog")):
        it = find(name)
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        dress(True)
        box(x0, x1, y0, y1, 0, 1, "concrete")
        if kind == "pump":
            for k in range(2):
                px = x0 + 10 + k * 20
                rod((px, (y0 + y1) / 2, 1), (px, (y0 + y1) / 2, 9), 2.2, "lamp", seg=16)    # pump pot (frosted)
                rod((px, (y0 + y1) / 2, 9), (px, (y0 + y1) / 2, 10), 2.6, "steel", seg=16)  # head flange
                rod((px, (y0 + y1) / 2 + 2.6, 6), (px, y1 - .5, 6), .5, "lamp", seg=8)      # suction
                rod((px, (y0 + y1) / 2 - 2.6, 8), (px, y0 + .5, 8), .45, "pipe", seg=8)     # discharge
                box(px + 3, px + 5, (y0 + y1) / 2 - 1, (y0 + y1) / 2 + 1, 1, 5, "panel")   # junction box
        else:
            box(x0 + 3, x1 - 12, y0 + 6, y1 - 6, 1, 3, "steel")
            box(x0 + 6, x0 + 18, y0 + 9, y1 - 9, 3, 10, "machine")                       # compressor
            rod((x0 + 18, (y0 + y1) / 2, 6.5), (x0 + 28, (y0 + y1) / 2, 6.5), 3, "motor", seg=16)
            rod((x1 - 6, (y0 + y1) / 2, 1), (x1 - 6, (y0 + y1) / 2, 12), 2.5, "tank", seg=14)   # knock-out drum
            rod((x1 - 6, (y0 + y1) / 2 + 2.5, 9), (x0 + 12, (y0 + y1) / 2 + 2.5, 9), .5, "pipe", seg=8)
        dress(False)


def h2():
    bld = find("H2 22: electrolyzer building")
    x0, x1, y0, y1 = bld["fp"]
    on(bld)
    dress(True)
    for k in range(8):                                                                 # ridge vents
        xv = x0 + 10 + k * 20
        box(xv - 3, xv + 3, (y0 + y1) / 2 - 1.5, (y0 + y1) / 2 + 1.5, 30, 32.5, "louvre")
        box(xv - 3.4, xv + 3.4, (y0 + y1) / 2 - 2, (y0 + y1) / 2 + 2, 32.5, 33, "roof")
    for k in range(6):                                                                 # wall louvres (north)
        box(x0 + 8 + k * 25, x0 + 16 + k * 25, y1, y1 + .2, 18, 24, "louvre")
    for k in range(4):                                                                 # gas detectors at the eaves
        box(x0 + 20 + k * 40, x0 + 21 + k * 40, y0 - .3, y0, 24, 25, "amber")
    box(x1, x1 + .2, y0 + 30, y0 + 44, 0, 16, "rollup")
    for k in range(2):                                                                 # hazard signs
        box(x0 + 4 + k * 140, x0 + 8 + k * 140, y0 - .12, y0 - .02, 6, 9, "sign")
        box(x0 + 4 + k * 140, x0 + 8 + k * 140, y0 - .14, y0 - .12, 8.3, 9, "red")
    dress(False)
    for k in range(5):
        for name in (f"PEM electrolyzer {k+1}", f"Rectifier {k+1}"):
            it = find(name)
            it["wiring"] = (["DC bus: Cu busbar / 2 kV DC single conductors from the rectifier, in trays",
                             W.CTRL, W.INST, "Gas detection and ESD: shielded instrument cable", W.GND]
                            if name.startswith("PEM") else
                            ["13.8 kV supply from the rectifier transformer: MV-105, 15 kV, buried",
                             "DC output: Cu busbar to the electrolyzer stack", W.CTRL, "Control / SCADA: fibre", W.GND])
    # dryer: twin adsorbers and a regeneration heater
    it = find("H2 25: H2 dryer / purification")
    x0, x1, y0, y1 = it["fp"]
    strip(it)
    on(it)
    dress(True)
    box(x0, x1, y0, y1, 0, 1, "concrete")
    for k in range(2):
        rod((x0 + 8 + k * 9, (y0 + y1) / 2, 1), (x0 + 8 + k * 9, (y0 + y1) / 2, 11), 2.6, "tank", seg=16)
        rod((x0 + 8 + k * 9, (y0 + y1) / 2, 11), (x0 + 8 + k * 9, (y0 + y1) / 2, 12), 2.6, "tank", r2=1, seg=16)
    box(x0 + 24, x0 + 34, y0 + 5, y1 - 5, 1, 7, "machine")                                # regeneration heater
    box(x1 - 4, x1 - 1, y0 + 2, y0 + 6, 1, 7, "panel")
    pipe([(x0 + 8, (y0 + y1) / 2, 12.5), (x0 + 17, (y0 + y1) / 2, 12.5)], 12.5, .3, "pipe")
    dress(False)
    for k in (1, 2):
        it = find(f"H2 26: H2 compressor {k}")
        x0, x1, y0, y1 = it["fp"]
        on(it)
        dress(True)
        for d in range(3):
            box(x0 + 4 + d * 12, x0 + 8 + d * 12, y0 - .08, y0, 1, 8, "door")
        box(x0 + 2, x0 + 14, y0 + 1, y1 - 1, 9.5, 11.5, "bundle")                          # roof cooler
        rod((x0 + 8, (y0 + y1) / 2, 11.5), (x0 + 8, (y0 + y1) / 2, 11.9), 2.6, "fan", seg=14)
        box(x1 - 6, x1 - 2, y0 + 2, y1 - 2, 9.5, 10.5, "louvre")
        dress(False)
    for (x, y) in [(2250, 1560), (2250, 1580), (2300, 1560), (2300, 1580)]:
        it = next(i for i in fuel.G["items"] if i["name"].startswith("H2 27: storage tube bank") and i["fp"][0] == x
                  and i["fp"][2] == y)
        on(it)
        dress(True)
        for (xe, s) in ((x + .5, -1), (x + 39.5, 1)):
            box(xe - .4, xe + .4, y + .5, y + 9.5, 0, 8, "steel")                           # end frame
        rod((x - .8, y + 1, 8.6), (x - .8, y + 9, 8.6), .3, "pipe", seg=8)                  # manifold
        for kk in range(3):
            rod((x + 1, y + 1.7 + 3.3 * kk, 6), (x - .8, y + 1.7 + 3.3 * kk, 8.6), .15, "pipe", seg=6)
            rod((x - .8, y + 1.7 + 3.3 * kk, 8.9), (x - .8, y + 1.7 + 3.3 * kk, 9.5), .25, "red", seg=6)   # valves
        dress(False)


def build():
    lng()
    h2()
