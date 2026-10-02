"""Carbon capture at LOD 3 (detail cycle 6).

Per train (A, B, C), as dressing inside the drawn footprints and sheet-13 heights:
- flue-gas path closed: the HRSG flue duct turns west into the direct-contact cooler (DCC); the
  cooled gas leaves the DCC low on its east face into the booster fan, and the fan discharges up
  into an overhead duct on steel bents north to the absorber inlet;
- DCC: quench-water riser from its pumps to the spray header, a platform with handrail and a
  caged ladder;
- absorber: lean-amine riser to the upper packed bed, water-wash riser, rich-amine bottoms line to
  the rich / lean pump skid, sample-panel and analyser box at grade;
- a CCS pipe rack (two tiers) along y 1115-1135 from the trains to the regenerators, carrying rich
  and lean amine, LP steam, condensate and cooling water.
Regeneration:
- stripper overhead lines down the shell to a CO2 product header that runs to the compression
  building; reboiler-to-stripper vapour return lines; a reflux drum per stripper;
- CO2 compression: intercooler / aftercooler fin-fan banks north of the building, louvres.
CCS cooling tower: fans with blades, hubs and gearboxes in every fan stack, fan-deck handrails and
access stair, intake louvres on both long faces, a hot-water header with a riser per cell from
the circulating-water pumps.
All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, find, on, pipe, hvessel


def dress(flag):
    fuel.D = flag


def routes(add_route):
    sheet = "typical (carbon capture detail)"
    # CCS T-1 / T-2 13.8 kV secondaries into the CCS MV switchgear building
    add_route("mvlv_cable", [(1210, 1008), (1200, 1008)], layer="OPT_CCS_ROUTES", sheet=sheet)
    add_route("mvlv_cable", [(1280, 1030), (1280, 1040), (1200, 1040)], layer="OPT_CCS_ROUTES", sheet=sheet)
    # 13.8 kV feeder from the CCS MV building to the cooling-tower MCC / VFD e-house
    add_route("mvlv_cable", [(1195, 1050), (1195, 1095), (1305, 1095), (1305, 1700), (1295, 1700), (1295, 1850),
                             (1290, 1850)], layer="OPT_CCSU_ROUTES", sheet=sheet)
    # fan-motor cables from the MCC along the north face of the cooling tower
    add_route("mvlv_cable", [(1200, 1866), (445, 1866)], layer="OPT_CCSU_ROUTES", sheet=sheet)


def trains():
    for i, dx in enumerate((0, 160, 320)):
        t = "ABC"[i]
        gx = 630 + dx
        # ---- flue gas: duct elbow into the DCC, DCC outlet to the booster fan, fan to the absorber
        on(find(f"DCC-{t}:"))
        dress(True)
        box(608 + dx, 639 + dx, 985, 1003, 44, 62, "duct")                     # elbow west into the DCC
        box(606 + dx, 608 + dx, 983, 1005, 42, 64, "steel")                    # flange frame
        box(608 + dx, 623 + dx, 993, 1009, 8, 24, "duct")                      # DCC outlet to the fan
        box(606 + dx, 608 + dx, 991, 1011, 6, 26, "steel")
        # quench-water riser from the DCC pumps to the spray header, platform, ladder
        rod((600 + dx, 1062, 6), (600 + dx, 1062, 80), .9, "pipe", seg=12)
        rod((600 + dx, 1062, 80), (600 + dx, 1059, 80), .9, "pipe", seg=12)
        rod((576 + dx, 1062, 6), (576 + dx, 1062, 60), .7, "pipe", seg=12)    # circulation return
        box(568 + dx, 608 + dx, 1060, 1064, 60, 60.5, "grating")
        rod((568 + dx, 1064, 63.5), (608 + dx, 1064, 63.5), .07, "rail", seg=4)
        for z in range(2, 60, 2):
            box(588 + dx, 590 + dx, 1060.3, 1060.6, z - .06, z + .06, "steel")
        for s in (588, 590):
            box(s + dx - .06, s + dx + .06, 1060.2, 1060.7, 0, 63, "steel")
        dress(False)
        on(find(f"BF-{t}:"))
        dress(True)
        box(627 + dx, 643 + dx, 998, 1010, 28, 34, "duct")                     # fan discharge up
        box(625 + dx, 645 + dx, 998, 1189, 34, 50, "duct")                     # overhead duct to the absorber
        for y in (1030, 1060, 1090, 1160):
            for x in (626 + dx, 644 + dx):
                box(x - .6, x + .6, y - .6, y + .6, 0, 34, "steel")
            box(624 + dx, 646 + dx, y - .7, y + .7, 32.6, 34, "steel")
        for y in (1040, 1100, 1150):
            box(624 + dx, 646 + dx, y - .3, y + .3, 33.8, 50.2, "steel")       # stiffener bands
        box(625 + dx, 645 + dx, 1180, 1182, 33, 51, "fan")                     # expansion joint
        dress(False)
        # ---- absorber: lean-amine and wash risers, rich bottoms, sample panel
        on(find(f"Absorber {t}"))
        dress(True)
        pipe([(668 + dx, 1100, 10), (668 + dx, 1228, 10), (663.5 + dx, 1228, 10), (663.5 + dx, 1228, 200),
              (660 + dx, 1228, 200)], 10, .7, "pipe")                           # lean amine to the upper bed
        pipe([(690 + dx, 1195, 6), (690 + dx, 1236, 6), (661.5 + dx, 1236, 6), (661.5 + dx, 1236, 246),
              (658 + dx, 1236, 246)], 6, .45, "waterline")                     # water wash
        pipe([(650 + dx, 1196, 3), (650 + dx, 1104, 3), (662 + dx, 1104, 3)], 3, .8, "pipe")   # rich amine
        box(652 + dx, 656 + dx, 1180, 1182, 0, 6, "panel")                      # sample / analyser panel
        box(651 + dx, 657 + dx, 1179, 1183, 6, 6.3, "roof")
        dress(False)
    # ---- CCS pipe rack y 1115-1135, x 560-1045
    on(find("Rich/lean pumps, cross exchanger, lean cooler A"))
    dress(True)
    cols = sorted({x for x in range(562, 1046, 24)})
    duct_x = [(625 + dx, 645 + dx) for dx in (0, 160, 320)]
    lines = [(1118, .9, "pipe"), (1121, .9, "pipe"), (1124, 1.2, "lngpipe"), (1127, .5, "waterline"),
             (1130, 1.1, "waterline"), (1133, 1.1, "waterline")]
    for x in cols:
        if any(a - 2 <= x <= b + 2 for a, b in duct_x):
            continue
        for y in (1116, 1134):
            box(x - .5, x + .5, y - .5, y + .5, 0, 26, "steel")
        for z in (18, 26):
            box(x - .55, x + .55, 1115, 1135, z - 1, z, "steel")
    box(560, 1046, 1115.3, 1115.8, 17, 18, "steel")
    box(560, 1046, 1134.2, 1134.7, 17, 18, "steel")
    for (y, r, c) in lines:
        rod((560, y, 18 + r), (1046, y, 18 + r), r, c, seg=12)
    for y in (1118, 1124, 1130):
        rod((560, y, 26.6), (1046, y, 26.6), .5, "pipe", seg=10)                # upper tier utilities
    # risers from each rich / lean skid onto the rack
    for dx in (0, 160, 320):
        for (x, y) in ((690 + dx, 1118), (696 + dx, 1121)):
            rod((x, 1100, 8), (x, y, 8), .6, "pipe", seg=10)
            rod((x, y, 8), (x, y, 18), .6, "pipe", seg=10)
    dress(False)


def regeneration():
    for i, cx in enumerate((1070, 1120, 1170)):
        t = "ABC"[i]
        on(find(f"STR-{t}:"))
        dress(True)
        ox = cx + 25.5
        pipe([(cx, 1187.5, 207), (cx, 1187.5, 210), (ox, 1187.5, 210), (ox, 1187.5, 30), (ox, 1230, 30)], 30, 1.1,
             "pipe")                                                            # overhead vapour / CO2 product
        for zc in range(40, 200, 30):
            box(ox - 1.6, cx + 22.6, 1187, 1188, zc - .3, zc + .3, "steel")      # pipe guides off the shell
        for k in (-8, 8):
            rod((cx + k, 1150, 18), (cx + k, 1165.5, 18), 1.8, "pipe", seg=14)    # reboiler vapour return
            rod((cx + k, 1150, 6), (cx + k, 1166, 6), 1.0, "pipe", seg=12)       # reboiler feed
        hvessel(cx - 14, cx + 6, 1157.5, 5, 3.2, saddles=(cx - 10, cx + 2), nozzles=(cx - 4,), psv=cx)   # reflux drum
        dress(False)
    on(find("CO2 compression"))
    dress(True)
    pipe([(1095.5, 1230, 30), (1303, 1230, 30), (1303, 1240, 30), (1310, 1240, 30)], 30, 1.4, "pipe")   # CO2 header
    for x in range(1110, 1300, 30):
        box(x - .5, x + .5, 1229.5, 1230.5, 0, 28.6, "steel")
        box(x - 1.5, x + 1.5, 1229, 1231, 28, 28.6, "steel")
    # intercooler / aftercooler fin-fan banks north of the building
    for b in range(4):
        x0 = 1316 + b * 29
        for (x, y) in ((x0, 1348), (x0 + 26, 1348), (x0, 1366), (x0 + 26, 1366)):
            box(x - .5, x + .5, y - .5, y + .5, 0, 15, "steel")
        box(x0, x0 + 26, 1348, 1366, 15, 18, "bundle")
        for f in range(2):
            rod((x0 + 6.5 + 13 * f, 1357, 18), (x0 + 6.5 + 13 * f, 1357, 21), 5.6, "fan", seg=20)
            rod((x0 + 6.5 + 13 * f, 1357, 15), (x0 + 6.5 + 13 * f, 1357, 13), .9, "motor", seg=10)
        rod((x0 + 2, 1347, 16.5), (x0 + 2, 1345, 16.5), .9, "pipe", seg=10)
        rod((x0 + 2, 1345, 16.5), (x0 + 2, 1345, 30), .9, "pipe", seg=10)
    for y in (1250, 1280, 1310):
        box(1435, 1435.2, y, y + 14, 12, 26, "louvre")
    dress(False)


def cooling_tower():
    ct = find("CCS cooling tower")
    on(ct)
    dress(True)
    for c in range(15):
        for r_ in range(2):
            cx, cy = 465 + 50 * c, 1770 + 60 * r_
            for b in range(8):
                a = 2 * math.pi * b / 8 + .3 * c
                rod((cx + 2 * math.cos(a), cy + 2 * math.sin(a), 50.25),
                    (cx + 17.5 * math.cos(a), cy + 17.5 * math.sin(a), 50.35), .55, "fan", r2=.35, seg=6)
            rod((cx, cy, 50), (cx, cy, 50.03), 18.6, "fanhub", seg=28)                   # open stack (dark throat)
            rod((cx, cy, 50.03), (cx, cy, 50.6), 2.2, "fan", seg=16)                     # hub
            rod((cx, cy, 42), (cx, cy, 44.8), .45, "steel", seg=8)
            box(cx - 1.8, cx + 1.8, cy - 1.8, cy + 1.8, 42, 44, "machine")          # gearbox
            rod((cx + 1.8, cy, 43), (cx + 20, cy, 43), .35, "steel", seg=8)         # drive shaft
            rod((cx + 20, cy, 43), (cx + 25, cy, 43), 1.3, "motor", seg=12)         # motor outside the stack
    for y in (1741, 1859):
        rod((441, y, 45), (1189, y, 45), .07, "rail", seg=4)
    for x in (441, 1189):
        rod((x, 1741, 45), (x, 1859, 45), .07, "rail", seg=4)
    # intake louvres on the long faces (between the cell walls)
    for c in range(15):
        x0 = 440 + 50 * c + 1.5
        for (y0, y1) in ((1739.7, 1740), (1860, 1860.3)):
            box(x0, x0 + 47, y0, y1, 4, 22, "louvre")
    # access stair at the east end
    for k in range(20):
        box(1190.5, 1194.5, 1745 + k * 1.9, 1746.2 + k * 1.9, 2 * k + 2, 2 * k + 2.3, "grating")
    box(1190.5, 1194.5, 1783, 1787, 41.7, 42, "grating")
    # hot-water header south of the tower and a riser into every cell
    pipe([(1222, 1760, 4), (1222, 1734, 4), (445, 1734, 4)], 4, 2.2, "waterline")
    for c in range(15):
        x = 465 + 50 * c
        rod((x, 1734, 4), (x, 1734, 38), 1.4, "waterline", seg=12)
        rod((x, 1734, 38), (x, 1740, 38), 1.4, "waterline", seg=12)
    dress(False)


def build():
    trains()
    regeneration()
    cooling_tower()
