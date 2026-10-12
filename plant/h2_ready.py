"""Hydrogen-ready plant (zone K): pipeline supply as the base case, on-site electrolysis as the alternative.

A hydrogen-ready H-class plant does not need to make hydrogen on site. The usual arrangement is a pipeline from a
production / storage hub (e.g. ACES Delta at Intermountain: electrolysis and salt-cavern storage), a receiving
station at the plant, and a blending skid that mixes hydrogen into the gas turbines' fuel (published H-class
blends roughly 30-50 % by volume, about 10-25 % of the fuel energy). So the zone now shows:
- a fenced hydrogen receiving station: pipeline riser with insulating joint and ESD valve, pig receiver,
  twin filter / coalescers, a two-run ultrasonic metering skid with a purity analyser shelter, two pressure-
  reduction trains (no preheater: hydrogen warms on expansion), relief to the existing vent stack, a nitrogen
  purge skid, a small e-house (480 V, UPS, fire & gas panel), gas detectors and UV / IR flame detectors
  (hydrogen flames are nearly invisible), Group B hazardous-area signs;
- a tube-trailer unloading bay (two trailers) used to commission and test the blend before the pipeline is in;
- a fenced, graded reserve pad for a later on-site electrolysis / storage phase, with the 230 kV cable from D6
  ending at a future T-H2 foundation and conduit stub-ups already in the pad.
The 25 MW electrolysis complex (sheet 14) moves to its own alternative layer, OPT_H2E, so it can still be shown
in place of the reserve. All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, pipe, valve, hvessel, skid_runs, sleepers, canopy, on

H2 = "hydrogen"
ALT = "OPT_H2E"
KEEP = ("H2 29", "H2 30")                 # vent stack and blending skid serve both arrangements


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, z=0.0, a=0.0, vest="hivis"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest)


def relayer(routes):
    """Move the electrolysis complex and its routes to the alternative layers."""
    G = fuel.G
    ids = set()
    for it in G["items"]:
        if it["layer"] == "OPT_H2" and not it["name"].startswith(KEEP):
            it["layer"] = ALT
            ids.add(it["id"])
    for p in G["parts"]:
        if p["item"] in ids and p["layer"] == "OPT_H2":
            p["layer"] = ALT
    for p in G["parts"]:                                   # dressing parts drawn on the route layer
        if p["layer"] == "OPT_H2_ROUTES" and p["item"] in ids:
            p["layer"] = ALT + "_ROUTES"
    n = 0
    for r in routes:
        if r["layer"] != "OPT_H2_ROUTES":
            continue
        P = r["points"]
        if r["type"] == "hv_cable" and P[0][1] < 400:      # 230 kV from D6: stays, ends at the future T-H2 pad
            continue
        if r["type"] == "hydrogen" and P[0] == [2250.0, 1575.0]:
            # tube banks -> blending skid becomes receiving station -> blending skid
            r["points"] = [[2268.0, 1510.0], [2203.0, 1510.0], [2203.0, 1435.0], [1980.0, 1435.0],
                           [1980.0, 1485.0], [1840.0, 1485.0]]
            continue
        if r["type"] == "hydrogen" and P[-1][0] <= 1978.0:  # road crossing and the run into the blending skid
            continue
        if r["type"] == "mvlv_cable" and P[0] == [1840.0, 1485.0]:
            # blending-skid power / control: from the station e-house instead of the electrolyzer building
            r["points"] = [[1840.0, 1487.0], [1990.0, 1487.0], [1990.0, 1438.0], [2222.0, 1438.0], [2222.0, 1530.0]]
            continue
        r["layer"] = ALT + "_ROUTES"
        n += 1
    return n


def fence(x0, x1, y0, y1, gate=None, h=7.0):
    """Chain-link fence with posts every 10 ft and a gate gap on one side: gate = (side, a, b)."""
    sides = (("s", (x0, y0), (x1, y0)), ("e", (x1, y0), (x1, y1)), ("n", (x1, y1), (x0, y1)), ("w", (x0, y1), (x0, y0)))
    for (nm, a, b) in sides:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L // 10))
        segs = [(0.0, 1.0)]
        if gate and gate[0] == nm:
            ga, gb = gate[1] / L, gate[2] / L
            segs = [(0.0, ga), (gb, 1.0)]
        for (t0, t1) in segs:
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            box(min(p0[0], p1[0]) - .03, max(p0[0], p1[0]) + .03, min(p0[1], p1[1]) - .03, max(p0[1], p1[1]) + .03,
                .2, h, "fence")
            rod((p0[0], p0[1], h), (p1[0], p1[1], h), .06, "steel", seg=4)
        for k in range(n + 1):
            t = k / n
            if gate and gate[0] == nm and gate[1] / L < t < gate[2] / L:
                continue
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            rod((x, y, 0), (x, y, h + .5), .1, "steel", seg=6)


def detector(x, y, z=6.0, kind="gas"):
    """Gas detector (yellow head) or UV / IR flame detector (grey head, angled) on a post."""
    rod((x, y, 0), (x, y, z), .08, "steel", seg=6)
    box(x - .4, x + .4, y - .4, y + .4, 0, .3, "concrete")
    if kind == "gas":
        rod((x, y, z - .9), (x, y, z - .2), .22, "sp_yellow", seg=10)
    else:
        box(x - .3, x + .3, y - .3, y + .3, z, z + .5, "panel")
        rod((x, y, z + .25), (x + .45, y, z + .05), .18, "machine", seg=10)


def trailer(x0, y, heading=1):
    """Hydrogen tube trailer (53 ft, 10 long tubes in a frame) with its valve cabinet at the rear (east)."""
    x1 = x0 + 53
    box(x0, x1, y - 4, y + 4, 3.6, 4.2, "steel")                         # chassis deck
    for (xa, xb) in ((x1 - 9, x1 - 2), ):
        for yy in (y - 3.2, y + 3.2):
            for xw in (xa + 1.5, xb - 1.5):
                rod((xw, yy - .6, 1.7), (xw, yy + .6, 1.7), 1.7, "tyre", seg=16)
    for yy in (y - 3.2, y + 3.2):                                          # landing legs
        box(x0 + 6, x0 + 6.4, yy - .2, yy + .2, 0, 3.6, "steel")
    for (dy, dz) in ((-2.2, 5.6), (0, 5.6), (2.2, 5.6), (-1.1, 7.6), (1.1, 7.6), (-2.2, 9.6), (0, 9.6), (2.2, 9.6),
                     (-1.1, 11.4), (1.1, 11.4)):
        rod((x0 + 2, y + dy, dz), (x1 - 4, y + dy, dz), .95, "tank", seg=14)
        rod((x0 + 1.4, y + dy, dz), (x0 + 2, y + dy, dz), .55, "tank", r2=.95, seg=14)
    for xf in (x0 + 1.2, x0 + 20, x0 + 36, x1 - 3.6):                        # frame bulkheads
        box(xf, xf + .5, y - 3.6, y + 3.6, 4.2, 12.8, "steel")
    box(x1 - 3.6, x1, y - 3.6, y + 3.6, 4.2, 10, "cabinet")                 # rear valve cabinet
    decal((x1 + .02, y, 8.2), (1, 0, 0), 4.5, 1.6, [("HYDROGEN", .42, True, "#ffffff"), ("UN 1049  2.1", .3, True, "#ffffff")],
          bg="#c8102e")


def build(routes):
    G = fuel.G
    n_moved = relayer(routes)
    L = "OPT_H2"
    fuel.D = False

    # ---- receiving station -------------------------------------------------------------------------------
    st = fuel.new_item(L, "H2R: hydrogen pipeline receiving station (pig receiver, filters, metering, pressure "
                       "reduction, ESD)", (2203, 2399, 1487, 1597), (-2, 25), tag="H2R", area="K",
                       sheet="typical (hydrogen-ready)",
                       info="Pipeline supply from a hydrogen hub (the usual case for a hydrogen-ready plant). Group B "
                            "(IIC) hazardous area: hazardous-location motors and fittings, sealed glands, ARMOR-X "
                            "MC-HL rated for Group B, gas and UV / IR flame detection.")
    on(st)
    box(2205, 2398, 1488, 1562, 0, .3, "gravel")
    fuel.D = True
    fence(2205, 2398, 1488, 1562, gate=("w", 20, 36))
    # pipeline entry: buried line up through an insulating joint to the ESD valve
    rod((2392, 1525, -1.5), (2392, 1525, 4), .6, H2, seg=12)
    rod((2392, 1525, 1.2), (2392, 1525, 1.8), .95, "fanhub", seg=14)                 # insulating joint
    pipe([(2392, 1525, 4), (2382, 1525, 4)], 4, .6, H2)
    valve((2386, 1525, 4), 0, .6, "esd")
    box(2389, 2391, 1529, 1531, 0, 5.5, "panel")                                     # ESD local panel
    # pig receiver (horizontal, quick-opening closure west), kicker and bypass
    hvessel(2342, 2374, 1545, 4.5, 1.6, c=H2, saddles=(2348, 2368), closure="west", psv=2370)
    pipe([(2382, 1525, 4), (2378, 1525, 4), (2378, 1545, 4.5), (2374, 1545, 4.5)], 4, .6, H2)
    pipe([(2342, 1545, 4.5), (2338, 1545, 4.5), (2338, 1525, 4), (2330, 1525, 4)], 4, .6, H2)
    box(2334, 2342, 1549, 1553, 0, .2, "concrete")                                   # pig handling tray
    # twin filter / coalescers (vertical)
    for xf in (2356, 2366):
        rod((xf, 1508, .8), (xf, 1508, 12), 2.1, H2, seg=18)
        rod((xf, 1508, 12), (xf, 1508, 12.8), 2.1, H2, r2=1.0, seg=18)
        rod((xf, 1508, 0), (xf, 1508, .8), 2.6, "concrete", seg=18)
        rod((xf, 1508, 12.8), (xf, 1508, 14.2), .3, "steel", seg=8)                  # PSV riser
        rod((xf, 1508, 14.2), (xf, 1508, 15.4), .35, "red", seg=10)
        box(xf + 2.2, xf + 3, 1507.5, 1508.5, 3, 6, "glass")                          # DP gauge / level glass
    pipe([(2378, 1525, 4), (2378, 1514, 4), (2366, 1514, 4)], 4, .55, H2)
    pipe([(2366, 1514, 4), (2356, 1514, 4)], 4, .55, H2)
    pipe([(2356, 1502, 4), (2366, 1502, 4)], 4, .55, H2)
    pipe([(2356, 1502, 4), (2338, 1502, 4), (2338, 1505, 4)], 4, .55, H2)
    # two-run ultrasonic metering skid and the purity / dew-point analyser shelter
    skid_runs(2310, 2336, 1496, 1516, (1501, 1511), 4, .5, [(2315, "hand"), (2321, "fc"), (2325, "meter"),
                                                            (2331, "hand")], c=H2)
    pipe([(2338, 1505, 4), (2338, 1511, 4), (2336, 1511, 4)], 4, .5, H2, elbows=False)
    box(2312, 2326, 1522, 1532, 0, .4, "concrete")
    box(2313, 2325, 1523, 1531, .4, 10, "ehouse")                                   # analyser shelter
    box(2312.6, 2325.4, 1522.6, 1531.4, 10, 10.4, "roof")
    box(2318, 2320, 1522.9, 1523, 1, 8, "door")
    for k in range(3):                                                              # sample-cylinder rack outside
        rod((2327 + k * .9, 1527, .4), (2327 + k * .9, 1527, 5), .35, "tank", seg=10)
    rod((2318, 1516, 4.6), (2318, 1522.6, 4.6), .1, "pipe", seg=6)                   # heated sample line
    # pressure-reduction trains: slam-shut, monitor and active regulators, then the outlet header
    skid_runs(2266, 2302, 1496, 1516, (1501, 1511), 4, .5, [(2296, "hand"), (2290, "slam"), (2283, "ctrl"),
                                                            (2276, "ctrl"), (2270, "hand")], c=H2)
    pipe([(2310, 1506, 4), (2302, 1506, 4)], 4, .55, H2, elbows=False)
    pipe([(2266, 1506, 4), (2266, 1510, 4), (2203, 1510, 4)], 4, .55, H2)
    valve((2240, 1510, 4), 0, .55, "mov")                                           # station outlet MOV
    valve((2214, 1510, 4), 0, .55, "esd")                                           # outlet ESD
    sleepers([(2262, 1510), (2205, 1510)], 4, .55)
    # relief / vent header to the existing vent stack (H2 29, 40 ft)
    pipe([(2300, 1518, 9), (2380, 1518, 9), (2380, 1559, 9)], 9, .35, "pipe")
    for x in (2310, 2340, 2370):
        box(x - .2, x + .2, 1517.8, 1518.2, 0, 8.6, "steel")
    rod((2380, 1559, 9), (2380, 1594, 9), .35, "pipe", seg=10)
    rod((2380, 1594, 9), (2380, 1595.5, 9), .45, "pipe", seg=10)
    for y in (1575, 1590):
        box(2379.8, 2380.2, y - .2, y + .2, 0, 8.6, "steel")
    # nitrogen purge skid (bottle racks + a small liquid N2 tank and vaporiser)
    box(2240, 2262, 1530, 1546, 0, .5, "concrete")
    for k in range(2):
        for j in range(6):
            rod((2242 + j * 1.1, 1532 + k * 2, .5), (2242 + j * 1.1, 1532 + k * 2, 5.5), .45, "tank", seg=10)
    box(2241.4, 2249, 1531.2, 1534.8, 5.5, 5.8, "steel")
    rod((2256, 1540, .5), (2256, 1540, 13), 2.2, "tank", seg=16)
    for k in range(4):
        rod((2251, 1544 - k * .7, .5), (2251, 1544 - k * .7, 8), .2, "steel", seg=6)
    pipe([(2256, 1537, 3), (2256, 1520, 3), (2268, 1520, 3), (2268, 1516, 3)], 3, .2, "pipe")
    # e-house: 480 V MCC, UPS, fire & gas / ESD panel (outside the hazardous zone, by the gate)
    box(2210, 2235, 1530, 1545, 0, .6, "concrete")
    box(2210.5, 2234.5, 1530.5, 1544.5, .6, 11, "ehouse")
    box(2210.2, 2234.8, 1530.2, 1544.8, 11, 11.5, "roof")
    box(2216, 2219, 1530.3, 1530.5, 1, 8, "door")
    box(2224, 2232, 1544.5, 1545.3, 8, 10, "fan")                                    # HVAC unit
    for k in range(5):                                                              # conduit stub-ups to the skids
        rod((2213 + k * 1.2, 1529.8, 0), (2213 + k * 1.2, 1529.8, 3), .12, "steel", seg=6)
    # detection, lighting, signs
    for (x, y) in ((2300, 1492), (2345, 1492), (2390, 1500), (2390, 1555), (2330, 1558), (2280, 1525), (2350, 1530)):
        detector(x, y, 6.0, "gas")
    for (x, y) in ((2262, 1492), (2394, 1492), (2394, 1559), (2290, 1559)):
        detector(x, y, 12.0, "flame")
    for (x, y) in ((2250, 1492), (2320, 1558), (2396, 1530)):
        rod((x, y, 0), (x, y, 24), .25, "steel", seg=8)
        box(x - 1.2, x + 1.2, y - .5, y + .5, 23.2, 24, "lamp")
    decal((2205 - .05, 1505, 5.5), (-1, 0, 0), 7, 3.6,
          [("DANGER", .22, True, "#ffffff", False, "#c8102e"), ("HYDROGEN", .2, True, None),
           ("CLASS I DIV 2 GROUP B", .13, True, None), ("NO IGNITION SOURCES", .13, False, None)], bg="#ffffff")
    decal((2205 - .05, 1550, 5.0), (-1, 0, 0), 6, 2.2,
          [("H2R  HYDROGEN RECEIVING", .3, True, None), ("PIPELINE SUPPLY  ·  ESD AT GATE", .2, False, None)],
          bg="#ffd200")
    person(2300, 1522, 0, 1.57)
    person(2358, 1520, 0, 3.14, vest="hivis_o")
    fuel.D = False

    # ---- tube-trailer unloading bay ------------------------------------------------------------------------
    tb = fuel.new_item(L, "H2T: tube-trailer unloading bay (2 bays, commissioning / test supply)",
                       (2210, 2372, 1570, 1632), (0, 14), tag="H2T", area="K", sheet="typical (hydrogen-ready)",
                       info="Trucked hydrogen in tube trailers to commission and test the GT blend before the "
                            "pipeline is in service; also a backup supply. Earthing / bonding point and ESD at the "
                            "unloading panel.")
    on(tb)
    box(2210, 2372, 1570, 1632, 0, .4, "concrete")
    fuel.D = True
    for y in (1586, 1616):
        trailer(2268, y)
        for yy in (y - 5.2, y + 5.2):                                               # bay markings
            box(2262, 2340, yy - .15, yy + .15, .4, .42, "yellow")
        box(2334, 2336, y - 1, y + 1, .4, 1.6, "concrete")                            # wheel stop
        # unloading post: flexible hose from the trailer cabinet to the header
        box(2345, 2349, y - 1.5, y + 1.5, .4, 6.5, "panel")
        rod((2345, y, 5), (2321, y + 1, 5.5), .2, "steel", seg=6)
        rod((2349, y, 4), (2356, y, 4), .35, H2, seg=10)
        box(2343.5, 2344, y + 1.6, y + 2.2, .4, 4, "sp_yellow")                      # earthing reel
    pipe([(2356, 1586, 4), (2356, 1616, 4)], 4, .35, H2)
    pipe([(2356, 1600, 4), (2362, 1600, 4), (2362, 1566, 4), (2362, 1562, 4)], 4, .4, H2)
    canopy(2340, 2352, 1576, 1626, 14)
    for (x, y) in ((2215, 1574), (2215, 1628), (2365, 1574)):
        detector(x, y, 6.0, "gas")
    decal((2210 - .05, 1600, 4.5), (-1, 0, 0), 6, 2.2,
          [("H2 TUBE-TRAILER BAY", .3, True, None), ("BOND TRAILER BEFORE UNLOADING", .2, False, None)],
          bg="#ffd200")
    person(2342, 1600, .4, 3.14)
    fuel.D = False

    # ---- reserve pad for the on-site production phase --------------------------------------------------------
    rp = fuel.new_item(L, "H2X: reserve pad, future on-site electrolysis / storage (Phase 2)",
                       (2009, 2196, 1439, 1631), (-1.5, 8), tag="H2X", area="K", sheet="typical (hydrogen-ready)",
                       register=False,
                       info="Graded and fenced land held for the 25 MW electrolysis option (layer OPT_H2E, sheet 14). "
                            "Conduit stub-ups and the 230 kV feed from D6 are in place.")
    on(rp)
    box(2010, 2195, 1440, 1630, 0, .25, "gravel")
    fuel.D = True
    fence(2010, 2195, 1440, 1630, gate=("s", 70, 90))
    for (x0, y0) in ((2020, 1528), (2040, 1528), (2062, 1528), (2084, 1528), (2106, 1528)):     # conduit stub-ups
        box(x0, x0 + 6, y0, y0 + 3, .25, .5, "concrete")
        for k in range(4):
            rod((x0 + 1 + k * 1.3, y0 + 1.5, -1), (x0 + 1 + k * 1.3, y0 + 1.5, 2), .22, "pvc_orange", seg=8)
            rod((x0 + 1 + k * 1.3, y0 + 1.5, 2), (x0 + 1 + k * 1.3, y0 + 1.5, 2.2), .3, "red", seg=8)
    for (x, y) in ((2010, 1440), (2195, 1440), (2010, 1630), (2195, 1630)):                  # survey markers
        rod((x, y, 0), (x, y, 3), .25, "yellow", seg=8)
    decal((2102, 1630 + .05, 5), (0, 1, 0), 10, 3.4,
          [("RESERVED", .3, True, "#ffffff", False, "#004c97"), ("FUTURE ELECTROLYSIS / H2 STORAGE", .17, True, None),
           ("PHASE 2  ·  25 MW  ·  230 kV FROM D6", .14, False, None)], bg="#ffffff")
    for x in (2096, 2108):
        rod((x, 1630.2, 0), (x, 1630.2, 6.8), .12, "steel", seg=6)
    fuel.D = False

    # future T-H2 foundation where the 230 kV cable from D6 comes up (drawn T-H2 position, sheet 14)
    ft = fuel.new_item(L, "H2F: future T-H2 foundation (230 / 13.8 kV, Phase 2) with the 230 kV cable stub-up",
                       (2327, 2373, 1437, 1483), (-2.5, 7), tag="H2F", area="K", sheet="SK-3X1-14", register=False,
                       info="Foundation, oil-containment curb and capped 230 kV cable stub-ups for the electrolysis "
                            "transformer; the cable from D6 is pulled and terminated in Phase 2.")
    on(ft)
    box(2330, 2370, 1440, 1480, 0, .6, "concrete")
    box(2330, 2370, 1440, 1441, .6, 1.6, "concrete")
    box(2330, 2370, 1479, 1480, .6, 1.6, "concrete")
    box(2330, 2331, 1441, 1479, .6, 1.6, "concrete")
    box(2369, 2370, 1441, 1479, .6, 1.6, "concrete")
    box(2338, 2362, 1450, 1470, .6, 1.4, "concrete")                                     # plinth
    fuel.D = True
    for k in range(3):
        x = 2344 + k * 6
        rod((x, 1443, -2), (x, 1443, 3), .35, "pvc_orange", seg=10)
        rod((x, 1443, 3), (x, 1443, 3.4), .5, "red", seg=10)
    fence(2328, 2372, 1438, 1482, gate=("s", 4, 16), h=6)
    fuel.D = False

    # blending skid serves all three GT fuel branches
    bl = fuel.find("H2 30: H2 / gas blending skid")
    bl["info"] = ("Blends pipeline hydrogen into the plant fuel header that feeds all three GTs, ratio-controlled "
                  "to the combustor limit (H-class: roughly 30-50 % by volume); started as a 5 % pilot on GT-1. "
                  "Group B hazardous area.")
    return n_moved
