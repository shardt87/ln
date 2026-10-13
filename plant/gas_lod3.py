"""Plant gas yard and pipeline M&R station at LOD 3: the yard furniture that makes a gas area read as one.

Both areas are Class I Div 2 Group D (natural gas). The process equipment was already modelled; this pass adds:
- a chain-link fence round each pad, opened where pipes cross it, with a vehicle gate and hazard signs;
- explosion-proof LED flood poles, fixed gas detectors by each equipment group, wheeled dry-chemical
  extinguishers and a windsock;
- instrument junction-box stands at each equipment group: steel post, explosion-proof JB, rigid conduits rising
  from the buried duct bank with conduit seals (EYS), flexible conduit to the field instruments. Inside the
  hazardous area the power and control cable is ARMOR-X MC-HL / Type TC-ER in buried conduit, not on trays;
- dressing on the plain buildings: the gas-yard control enclosure, the M&R gas-quality building, the M&R
  service panel, the SCADA antenna mast, the CP test station;
- insulation bands and nameplates on the heaters and vessels;
- operators and a pickup in each area.
Every piece is placed only where it is clear of the existing parts. All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, on, find, pipe, valve


class Space:
    """Clearance test against every part already in the model (2-D grid on 10 ft cells)."""

    def __init__(self):
        self.b, self.grid = [], {}
        items = {i["id"]: i for i in fuel.G["items"]}
        for p in fuel.G["parts"]:
            it = items[p["item"]]
            if it["layer"] in ("SITE", "UNDERGROUND", "OPT_UNDERGROUND") or it["z"][1] < .7:
                continue
            bb = self.pbox(p)
            if bb[5] < .7:
                continue
            self.add(bb)

    @staticmethod
    def pbox(p):
        if p["kind"] in ("box", "prism"):
            return p["min"] + p["max"]
        if p["kind"] == "rod":
            a, b, r = p["a"], p["b"], max(p["r"], p["r2"])
            return [min(a[0], b[0]) - r, min(a[1], b[1]) - r, min(a[2], b[2]) - r,
                    max(a[0], b[0]) + r, max(a[1], b[1]) + r, max(a[2], b[2]) + r]
        xs, ys, zs = zip(*p["v"])
        return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]

    def add(self, bb):
        k = len(self.b)
        self.b.append(bb)
        for gx in range(int(bb[0] // 10), int(bb[3] // 10) + 1):
            for gy in range(int(bb[1] // 10), int(bb[4] // 10) + 1):
                self.grid.setdefault((gx, gy), []).append(k)

    def free(self, x0, x1, y0, y1, z0=.7, z1=30.0, m=.6):
        x0, x1, y0, y1 = x0 - m, x1 + m, y0 - m, y1 + m
        for gx in range(int(x0 // 10), int(x1 // 10) + 1):
            for gy in range(int(y0 // 10), int(y1 // 10) + 1):
                for k in self.grid.get((gx, gy), ()):
                    b = self.b[k]
                    if b[0] < x1 and b[3] > x0 and b[1] < y1 and b[4] > y0 and b[2] < z1 and b[5] > z0:
                        return False
        return True

    def place(self, x, y, hw, hd, z1, tries=((0, 0), (3, 0), (-3, 0), (0, 3), (0, -3), (6, 0), (-6, 0), (0, 6),
                                              (0, -6), (5, 5), (-5, -5), (5, -5), (-5, 5))):
        for (dx, dy) in tries:
            if self.free(x + dx - hw, x + dx + hw, y + dy - hd, y + dy + hd, .7, z1):
                self.add([x + dx - hw, y + dy - hd, 0, x + dx + hw, y + dy + hd, z1])
                return x + dx, y + dy
        return None


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, z=0.0, a=0.0, vest="hivis"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest)


# ---------------------------------------------------------------------------------------------------------
def fence(S, x0, x1, y0, y1, gate, z0=.4, h=7.0):
    """Chain-link fence along the four sides, opened (2 ft each side) wherever an existing part crosses the line
    below the top rail, and at the vehicle gate (side, a, b along the side)."""
    sides = (("s", (x0, y0), (x1, y0)), ("e", (x1, y0), (x1, y1)), ("n", (x0, y1), (x1, y1)), ("w", (x0, y0), (x0, y1)))
    for (nm, a, b) in sides:
        horiz = a[1] == b[1]
        c = a[1] if horiz else a[0]
        lo, hi = (a[0], b[0]) if horiz else (a[1], b[1])
        cuts = []
        for bb in S.b:
            if bb[2] > z0 + h or bb[5] < z0 + .3:
                continue
            if horiz and bb[1] - .3 <= c <= bb[4] + .3 and bb[3] > lo and bb[0] < hi:
                cuts.append((bb[0] - 2, bb[3] + 2))
            if not horiz and bb[0] - .3 <= c <= bb[3] + .3 and bb[4] > lo and bb[1] < hi:
                cuts.append((bb[1] - 2, bb[4] + 2))
        if gate and gate[0] == nm:
            cuts.append((lo + gate[1], lo + gate[2]))
        cuts.sort()
        segs, t = [], lo
        for (ca, cb) in cuts:
            if ca > t:
                segs.append((t, min(ca, hi)))
            t = max(t, cb)
        if t < hi:
            segs.append((t, hi))
        for (sa, sb) in segs:
            if sb - sa < 1.5:
                continue
            if horiz:
                box(sa, sb, c - .03, c + .03, z0 + .2, z0 + h, "fence")
                rod((sa, c, z0 + h), (sb, c, z0 + h), .06, "steel", seg=4)
            else:
                box(c - .03, c + .03, sa, sb, z0 + .2, z0 + h, "fence")
                rod((c, sa, z0 + h), (c, sb, z0 + h), .06, "steel", seg=4)
            n = max(1, int((sb - sa) // 10))
            for k in range(n + 1):
                v = sa + (sb - sa) * k / n
                p = (v, c) if horiz else (c, v)
                rod((p[0], p[1], 0), (p[0], p[1], z0 + h + .5), .1, "steel", seg=6)
    # gate leaves (open) and gate posts
    nm, ga, gb = gate
    (a, b) = dict((s[0], (s[1], s[2])) for s in sides)[nm]
    horiz = a[1] == b[1]
    lo = a[0] if horiz else a[1]
    for v in (lo + ga, lo + gb):
        p = (v, a[1]) if horiz else (a[0], v)
        rod((p[0], p[1], 0), (p[0], p[1], z0 + h + .8), .22, "steel", seg=8)


def light_pole(S, x, y, h=26.0):
    p = S.place(x, y, .8, .8, h + 1)
    if not p:
        return
    x, y = p
    rod((x + .4, y, .2), (x + .4, y, h - 1.6), .07, "steel", seg=6)              # lighting circuit conduit up the pole
    box(x - .8, x + .8, y - .8, y + .8, 0, 1.2, "concrete")
    rod((x, y, 1.2), (x, y, h), .28, "steel", seg=8, r2=.18)
    for s in (-1, 1):                                                         # two explosion-proof LED floods
        rod((x, y, h - .4), (x + s * 1.6, y, h - .4), .1, "steel", seg=4)
        box(x + s * 1.6 - .6, x + s * 1.6 + .6, y - .5, y + .5, h - 1.3, h - .5, "lamp")


def detector(S, x, y):
    p = S.place(x, y, .4, .4, 7)
    if not p:
        return
    x, y = p
    box(x - .4, x + .4, y - .4, y + .4, 0, .4, "concrete")
    rod((x, y, .4), (x, y, 6.2), .08, "steel", seg=6)
    rod((x, y, 5.2), (x, y, 6.0), .24, "sp_yellow", seg=10)
    box(x - .25, x + .25, y + .1, y + .45, 4.2, 4.9, "panel")                 # transmitter head


def jb_stand(S, x, y, tag=None):
    """Instrument junction-box stand: post, explosion-proof JB, rigid conduits up from the duct bank with seals."""
    p = S.place(x, y, 1.4, .8, 7)
    if not p:
        return
    x, y = p
    JBS.append((x, y))
    box(x - 1.4, x + 1.4, y - .8, y + .8, 0, .35, "concrete")
    for dx in (-1.1, 1.1):
        rod((x + dx, y, .35), (x + dx, y, 6.5), .12, "steel", seg=6)              # unistrut posts
    box(x - 1.2, x + 1.2, y - .1, y + .1, 6.3, 6.5, "steel")
    box(x - 1.0, x + 1.0, y - .55, y - .1, 3.6, 5.6, "machine")                    # explosion-proof JB (cast)
    for k in range(4):
        xc = x - .75 + k * .5
        rod((xc, y - .35, -1), (xc, y - .35, 3.6), .1, "steel", seg=6)              # rigid conduit from below grade
        rod((xc, y - .35, 1.6), (xc, y - .35, 2.1), .15, "steel", seg=8)            # conduit seal (EYS)
    rod((x + .9, y - .35, 5.6), (x + .9, y - .35, 6.2), .08, "cable_inst", seg=6)  # flex to the instruments
    if tag:
        decal((x, y - .56, 5.05), (0, -1, 0), 1.5, .5, [(tag, .6, True, None)], bg="#ffffff")


JBS = []


def extinguisher(S, x, y):
    p = S.place(x, y, .9, .9, 4)
    if not p:
        return
    x, y = p
    rod((x, y, .9), (x, y, 3.6), .6, "red", seg=12)                                 # 150 lb wheeled dry chemical
    rod((x - .6, y, .55), (x + .6, y, .55), .55, "tyre", seg=12)
    rod((x, y + .5, 3.2), (x, y + .9, 1.2), .07, "cable_tc", seg=4)                # hose


def windsock(S, x, y):
    p = S.place(x, y, .6, .6, 26)
    if not p:
        return
    x, y = p
    box(x - .6, x + .6, y - .6, y + .6, 0, .8, "concrete")
    rod((x, y, .8), (x, y, 25), .16, "steel", seg=8)
    rod((x, y, 24.5), (x + 6, y + 1, 23.6), .85, "amber", r2=.35, seg=12)


def pickup(S, x, y, along_x=True):
    L, W = 19.0, 6.6
    hw, hd = (L / 2, W / 2) if along_x else (W / 2, L / 2)
    p = S.place(x, y, hw, hd, 7)
    if not p:
        return
    x, y = p
    if along_x:
        box(x - L / 2, x + L / 2, y - W / 2, y + W / 2, 1.3, 3.6, "truck")
        box(x - 1.5, x + 4.5, y - W / 2 + .2, y + W / 2 - .2, 3.6, 6.2, "truck")
        box(x - 1.4, x + 4.4, y - W / 2 + .15, y + W / 2 - .15, 4.4, 5.9, "glass")
        for u in (-6, 6):
            for v in (-W / 2 - .2, W / 2 - .2):
                rod((x + u, y + v, 1.3), (x + u, y + v + .4, 1.3), 1.3, "fanhub", seg=12)
    else:
        box(x - W / 2, x + W / 2, y - L / 2, y + L / 2, 1.3, 3.6, "truck")
        box(x - W / 2 + .2, x + W / 2 - .2, y - 1.5, y + 4.5, 3.6, 6.2, "truck")
        box(x - W / 2 + .15, x + W / 2 - .15, y - 1.4, y + 4.4, 4.4, 5.9, "glass")
        for u in (-6, 6):
            for v in (-W / 2 - .2, W / 2 - .2):
                rod((x + v, y + u, 1.3), (x + v + .4, y + u, 1.3), 1.3, "fanhub", seg=12)


def hazard_sign(x, y, n, title="DANGER"):
    decal((x, y, 4.6), n, 5.5, 3.0,
          [(title, .22, True, "#ffffff", False, "#c8102e"), ("FLAMMABLE GAS", .2, True, None),
           ("CLASS I DIV 2 GROUP D", .13, True, None), ("NO SMOKING · NO IGNITION SOURCES", .12, False, None)],
          bg="#ffffff")


# ---------------------------------------------------------------------------------------------------------
def bands(x0, x1, y, z, r, step=4.0):
    """Insulation / cladding bands on a horizontal vessel along x."""
    x = x0 + step / 2
    while x < x1:
        rod((x - .06, y, z), (x + .06, y, z), r + .06, "steel", seg=20)
        x += step


def gas_yard(S):
    # equipment dressing first (on the equipment items)
    ph = find("Fuel-gas performance heater")
    on(ph)
    fuel.D = True
    bands(1707, 1734, 1480, 7, 5.6)
    decal((1720, 1474.35, 7), (0, -1, 0), 3, 1.2, [("E-201", .45, True, None), ("FUEL GAS HEATER", .25, False, None)],
          bg="#ffffff")
    fs = find("Gas yard filter-separators")
    on(fs)
    for y in (1475, 1485):
        bands(1647, 1673, y, 6, 3.5, 5)
        rod((1660, y - 3.5, 6), (1660, y - 4.2, 6), .25, "steel", seg=8)          # DP gauge stem
        box(1659.5, 1660.5, y - 4.6, y - 4.2, 5.6, 6.6, "panel")
    ce = find("Gas yard local control enclosure")
    on(ce)
    box(1572, 1575, 1452, 1452.2, .2, 7.6, "door")                                  # door (north)
    box(1585, 1586.2, 1444, 1449, 4, 8, "fan")                                       # wall HVAC (east)
    box(1564.8, 1585.2, 1439.8, 1452.2, 10, 10.4, "roof")                            # roof cap
    for k in range(6):                                                               # conduit bank into the wall
        rod((1567 + k * .6, 1439.7, -1), (1567 + k * .6, 1439.7, 3.2), .14, "steel", seg=6)
        rod((1567 + k * .6, 1439.7, 3.2), (1567 + k * .6, 1440, 3.2), .14, "steel", seg=6)
    box(1573.5, 1574.5, 1452, 1452.3, 8, 8.8, "lamp")
    decal((1580, 1452.25, 6.5), (0, 1, 0), 4, 1.4, [("GY-CE-1", .4, True, None), ("GAS YARD CONTROL", .28, False, None)],
          bg="#ffffff")
    fuel.D = False

    it = fuel.new_item("BASE_UTILITIES", "Gas yard: fence and gate, lighting, gas detection, instrument JB stands, "
                       "extinguishers, windsock, signs (typical)", (1560, 1940, 1430, 1640), (-1, 27), area="D",
                       sheet="typical (fuel detail)", register=False,
                       info="Class I Div 2 Group D area: explosion-proof floods, fixed gas detectors, instrument JB "
                            "stands with sealed rigid conduit from the buried duct bank (ARMOR-X MC-HL / TC-ER cable "
                            "in conduit inside the hazardous area).")
    on(it)
    fuel.D = True
    fence(S, 1561.5, 1938.5, 1431.5, 1638.5, gate=("n", 64, 84))
    for (x, y) in ((1572, 1470), (1572, 1600), (1640, 1505), (1695, 1600), (1760, 1455), (1760, 1560),
                   (1860, 1530), (1930, 1600)):
        light_pole(S, x, y)
    for (x, y) in ((1660, 1494), (1700, 1492), (1745, 1495), (1700, 1517), (1650, 1545), (1725, 1612),
                   (1612, 1592), (1840, 1556), (1890, 1556), (1770, 1520)):
        detector(S, x, y)
    for (x, y, t) in ((1690, 1494, "JB-201"), (1660, 1500, "JB-202"), (1678, 1546, "JB-203"), (1740, 1545, "JB-204"),
                      (1724, 1607, "JB-205"), (1866, 1554, "JB-206")):
        jb_stand(S, x, y, t)
    for (x, y) in ((1636, 1496), (1755, 1505), (1700, 1620), (1880, 1640 - 6)):
        extinguisher(S, x, y)
    windsock(S, 1933, 1437)
    for (x, y, n) in ((1615, 1638.6, (0, 1, 0)), (1680, 1638.6, (0, 1, 0)), (1561.4, 1520, (-1, 0, 0)),
                      (1938.6, 1520, (1, 0, 0))):
        hazard_sign(x, y, n)
    fuel.D = False
    people = fuel.new_item("BASE_UTILITIES", "Gas yard: operators and maintenance pickup", (1600, 1700, 1495, 1636),
                           (0, 7), area="D", register=False)
    on(people)
    pickup(S, 1648, 1622)
    for (x, y, a, v) in ((1688, 1497, 1.57, "hivis"), (1700, 1546, 3.14, "hivis_o"), (1662, 1505, 0, "hivis")):
        p = S.place(x, y, .8, .8, 6)
        if p:
            person(p[0], p[1], .6, a, vest=v)


def mr_station(S):
    q = find("M&R 7: gas quality + measurement building")
    on(q)
    fuel.D = True
    box(1626, 1629, 1729.8, 1730, .2, 7.4, "door")
    box(1636, 1637.2, 1732, 1736, 5, 8, "fan")
    for k in range(4):                                                               # calibration-gas cylinders
        rod((1621 + k * .9, 1729.2, 0), (1621 + k * .9, 1729.2, 5), .38, "tank", seg=10)
    box(1620.4, 1624.6, 1728.6, 1729.8, 3.6, 3.9, "steel")
    box(1627, 1628, 1729.7, 1730, 8, 8.8, "lamp")
    decal((1632, 1729.75, 6.5), (0, -1, 0), 3.4, 1.2, [("M&R-7", .4, True, None), ("GAS QUALITY", .28, False, None)],
          bg="#ffffff")
    sp = find("M&R 9: service panel")
    on(sp)
    for k in range(4):
        box(1741 + k * 3.7, 1744.3 + k * 3.7, 1727.8, 1728, 1, 7.4, "panel")
    box(1739, 1757, 1726, 1741, 8.6, 9, "roof")                                       # sunshade
    for (x, y) in ((1739.3, 1726.3), (1756.7, 1726.3), (1739.3, 1740.7), (1756.7, 1740.7)):
        box(x - .2, x + .2, y - .2, y + .2, 0, 8.6, "steel")
    am = find("M&R SCADA antenna mast")
    on(am)
    rod((1777, 1746.5, 4), (1777, 1746.5, 38), .3, "steel", seg=8, r2=.18)
    rod((1777, 1746.5, 36), (1780.5, 1746.5, 36), .06, "steel", seg=4)
    box(1780.5, 1781, 1745.8, 1747.2, 34, 38, "panel")                                # yagi / panel antenna
    rod((1777, 1746.5, 38), (1777, 1746.5, 41), .05, "steel", seg=4)                  # whip
    cp = find("M&R CP test station")
    on(cp)
    box(1766.4, 1767.6, 1731.4, 1732.6, 4, 5.2, "yellow")
    fuel.D = False

    it = fuel.new_item("BASE_UTILITIES", "Pipeline M&R station: fence and gate, lighting, gas detection, JB stands, "
                       "extinguishers, windsock, signs (typical)", (1560, 1800, 1690, 1900), (-1, 27), area="D",
                       sheet="typical (fuel detail)", register=False,
                       info="Operator's custody-transfer station, Class I Div 2 Group D: fenced separately from the "
                            "plant, explosion-proof floods, gas detection, JB stands with sealed rigid conduit.")
    on(it)
    fuel.D = True
    fence(S, 1561.5, 1798.5, 1691.5, 1898.5, gate=("s", 40, 60))
    for (x, y) in ((1575, 1720), (1575, 1840), (1660, 1810), (1740, 1810), (1785, 1880), (1785, 1720)):
        light_pole(S, x, y)
    for (x, y) in ((1620, 1840), (1648, 1862), (1705, 1812), (1705, 1874), (1645, 1765), (1715, 1755)):
        detector(S, x, y)
    for (x, y, t) in ((1618, 1863, "JB-101"), (1686, 1815, "JB-102"), (1646, 1793, "JB-103"), (1733, 1775, "JB-104")):
        jb_stand(S, x, y, t)
    for (x, y) in ((1590, 1830), (1690, 1800), (1760, 1760)):
        extinguisher(S, x, y)
    windsock(S, 1792, 1893)
    for (x, y, n) in ((1610, 1691.4, (0, -1, 0)), (1630, 1691.4, (0, -1, 0))):
        hazard_sign(x, y, n, title="DANGER")
    decal((1690, 1691.4, 4.6), (0, -1, 0), 6.5, 2.4,
          [("PIPELINE OPERATOR", .26, True, None), ("CUSTODY TRANSFER · AUTHORIZED PERSONNEL ONLY", .16, False, None)],
          bg="#ffd200")
    fuel.D = False
    people = fuel.new_item("BASE_UTILITIES", "M&R station: operator and pickup", (1600, 1780, 1700, 1800), (0, 7),
                           area="D", register=False)
    on(people)
    pickup(S, 1650, 1712)
    for (x, y, a) in ((1648, 1789, 0), (1690, 1805, 1.57)):
        p = S.place(x, y, .8, .8, 6)
        if p:
            person(p[0], p[1], .4, a, vest="hivis_o")


def yard_equipment(S):
    """Equipment a real plant gas yard has that the first model lacked: final coalescers, an electric start-up /
    dew-point heater, a gas-chromatograph shelter at the meters, a drains tank in a bund, the yard's pad-mounted
    480 V transformer and LV panel; a crushed-stone surface with a concrete drive and walkways."""
    G = fuel.G
    pad = find("Plant gas yard (pad)")
    for p in G["parts"]:
        if p["item"] == pad["id"] and p["kind"] == "box" and p["max"][0] - p["min"][0] > 300:
            p["color"] = "gravel_yard"
    mr = find("Pipeline M&R station (by")
    for p in G["parts"]:
        if p["item"] == mr["id"] and p["kind"] == "box" and p["max"][0] - p["min"][0] > 200:
            p["color"] = "gravel_yard"
    L = "BASE_UTILITIES"

    def new(name, fp, z, info):
        if not S.free(fp[0], fp[1], fp[2], fp[3], .7, z[1], m=.3):
            print("gas_lod3: no room for", name)
            return None
        S.add([fp[0], fp[2], 0, fp[1], fp[3], z[1]])
        it = fuel.new_item(L, name, fp, z, area="D", sheet="typical (fuel detail)", register=False, info=info)
        on(it)
        return it

    if new("Gas yard final coalescers (2 x 100 %)", (1598, 1628, 1500, 1522), (0, 17),
           "Vertical coalescing filters after the filter-separators: last line of defence against liquid carry-over "
           "to the DLN combustors."):
        box(1598, 1628, 1500, 1522, .59, 1.4, "steel")
        for x in (1606, 1620):
            rod((x, 1512, 1.4), (x, 1512, 14), 2.2, "tank", seg=18)
            rod((x, 1512, 14), (x, 1512, 15), 2.2, "tank", r2=.9, seg=18)
            rod((x, 1512, 15), (x, 1512, 16.6), .3, "steel", seg=8)
            rod((x, 1512, 16.6), (x, 1512, 17), .38, "red", seg=10)                    # PSV
            fuel.D = True
            for z in (4, 7, 10, 13):
                rod((x, 1512, z - .06), (x, 1512, z + .06), 2.28, "steel", seg=18)
            box(x + 2.2, x + 2.8, 1511.5, 1512.5, 3, 8, "glass")                       # level glass
            fuel.D = False
        for x in (1606, 1620):
            rod((x, 1509.8, 4), (x, 1481.3, 4), .55, "fuelgas", seg=12)
            valve((x, 1500, 4), 1, .5, "hand")
        rod((1600, 1512, 9), (1626, 1512, 9), .2, "pipe", seg=6)                        # balance line
        S.add([1603, 1481, 0, 1623, 1500, 5.5])
    if new("E-202: electric start-up / dew-point heater skid", (1758, 1792, 1516, 1546), (0, 9),
           "Electric fuel-gas heater for start-up and dew-point margin before the performance heater has steam; "
           "480 V SCR power panel, Class I Div 2 terminal box."):
        box(1758, 1792, 1516, 1546, .59, 1.3, "steel")
        rod((1763, 1531, 4.5), (1782, 1531, 4.5), 2.1, "tank", seg=18)
        rod((1782, 1531, 4.5), (1784.5, 1531, 4.5), 2.6, "machine", seg=18)             # terminal enclosure
        for x in (1766, 1779):
            box(x - .7, x + .7, 1529, 1533, 1.3, 2.6, "steel")
        box(1786, 1791, 1519, 1527, 1.3, 8.4, "cabinet")                                # SCR power panel
        box(1785.8, 1791.2, 1518.8, 1527.2, 8.4, 8.8, "roof")
        rod((1788.5, 1527, 6), (1788.5, 1531, 6), .14, "steel", seg=6)
        rod((1788.5, 1531, 6), (1784.5, 1531, 6), .14, "steel", seg=6)
        pipe([(1760, 1531, 4.5), (1760, 1540, 4.5), (1790, 1540, 4.5)], 4.5, .5, "fuelgas")
    if new("Gas chromatograph / analyser shelter (fuel quality, Wobbe)", (1693, 1705, 1546, 1557), (0, 10),
           "On-line GC and Wobbe index for GT fuel control; heated sample line from the metering skid."):
        box(1693, 1705, 1546, 1557, .59, 1, "concrete")
        box(1694, 1704, 1547, 1556, 1, 9, "ehouse")
        box(1693.6, 1704.4, 1546.6, 1556.4, 9, 9.4, "roof")
        box(1697.5, 1699.5, 1546.9, 1547, 1.2, 7.6, "door")
        for k in range(3):
            rod((1706 + k * .9, 1551, .59), (1706 + k * .9, 1551, 5), .35, "tank", seg=10)
        rod((1690, 1538, 4.5), (1690, 1551, 4.5), .1, "pipe", seg=6)
        rod((1690, 1551, 4.5), (1694, 1551, 4.5), .1, "pipe", seg=6)
    if new("Gas yard drains / condensate tank in a bund", (1570, 1596, 1538, 1564), (0, 13),
           "Collects filter-separator and coalescer drains; bunded, level-switched, emptied by vacuum truck."):
        for (a, b, c, d) in ((1570, 1596, 1538, 1539), (1570, 1596, 1563, 1564), (1570, 1571, 1538, 1564),
                             (1595, 1596, 1538, 1564)):
            box(a, b, c, d, .59, 2.6, "concrete")                                       # bund wall
        rod((1583, 1551, .59), (1583, 1551, 11), 5, "tank", seg=22)
        rod((1583, 1551, 11), (1583, 1551, 12.2), 5, "tank", r2=1.2, seg=22)
        rod((1583, 1551, 12.2), (1583, 1551, 13), .4, "steel", seg=8)
        box(1589, 1593, 1541, 1544, .59, 2.5, "pump")
    if new("Gas yard 480 V pad-mount transformer and LV panel", (1588, 1599, 1440, 1453), (0, 8),
           "13.8 kV / 480 V, feeds the heaters, heat tracing and lighting; LV panel for the yard."):
        box(1588, 1599, 1440, 1453, 0, .6, "concrete")
        box(1589, 1596, 1441, 1447, .6, 6, "xfmr")
        for k in range(5):
            box(1589.4 + k * 1.4, 1590 + k * 1.4, 1440.6, 1441, 1, 5.4, "xfmr")            # radiator fins
        box(1589, 1596, 1448.5, 1452, .6, 7.2, "cabinet")
    # crushed-stone yard: concrete drive from the north gate and walkways along the equipment rows
    it = fuel.new_item(L, "Gas yard: concrete drive and walkways", (1600, 1800, 1494, 1638), (0, .65), area="D",
                       register=False)
    on(it)
    box(1627, 1643, 1560, 1638, .59, .64, "road")
    box(1600, 1643, 1556, 1564, .59, .64, "road")                                       # turning apron
    box(1600, 1760, 1494, 1499, .59, .63, "concrete")                                   # walkway between rows
    box(1640, 1755, 1541, 1545, .59, .63, "concrete")


# ---------------------------------------------------------------------------------------------------------
# visible cable: ladder tray on T-stanchions (MC-HL / TC-ER in tray is permitted in Class I Div 2, NEC 501.10(B))
CABLES = (("cable_mc", .2), ("cable_mc", .2), ("cable_tc", .14), ("cable_inst", .11), ("cable_inst", .11),
          ("cable_fa", .09))


def _seg_box(a, b, z, w):
    x0, x1 = min(a[0], b[0]), max(a[0], b[0])
    y0, y1 = min(a[1], b[1]), max(a[1], b[1])
    if a[1] == b[1]:
        y0, y1 = y0 - w / 2, y1 + w / 2
    else:
        x0, x1 = x0 - w / 2, x1 + w / 2
    return x0, x1, y0, y1


def tray(S, pts, z, w=1.5, cables=CABLES, stand=16.0, name="", tag=None):
    """Ladder tray along an orthogonal polyline at elevation z (raised in 1.5 ft steps until clear)."""
    for zz in (z, z + 1.5, z + 3, z + 4.5):
        if all(S.free(*_seg_box(a, b, zz, w), zz - .6, zz + .9, m=.15) for a, b in zip(pts, pts[1:])):
            z = zz
            break
    else:
        print("gas_lod3: tray blocked", name, pts[0])
        return None
    for a, b in zip(pts, pts[1:]):
        x0, x1, y0, y1 = _seg_box(a, b, z, w)
        S.add([x0, y0, z - .6, x1, y1, z + .9])
        alongx = a[1] == b[1]
        for s in (-1, 1):                                                         # side rails
            if alongx:
                box(x0, x1, a[1] + s * w / 2 - .06, a[1] + s * w / 2 + .06, z - .35, z + .15, "pipe")
            else:
                box(a[0] + s * w / 2 - .06, a[0] + s * w / 2 + .06, y0, y1, z - .35, z + .15, "pipe")
        L = abs(b[0] - a[0]) + abs(b[1] - a[1])
        for k in range(int(L) + 1):                                               # rungs every foot
            t = k / max(L, 1)
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if alongx:
                box(px - .05, px + .05, py - w / 2, py + w / 2, z - .3, z - .22, "pipe")
            else:
                box(px - w / 2, px + w / 2, py - .05, py + .05, z - .3, z - .22, "pipe")
        for j, (c, r) in enumerate(cables):                                       # cables laid in the tray
            off = -w / 2 + .25 + j * (w - .5) / max(1, len(cables) - 1)
            pa = (a[0], a[1] + off) if alongx else (a[0] + off, a[1])
            pb = (b[0], b[1] + off) if alongx else (b[0] + off, b[1])
            rod((pa[0], pa[1], z - .22 + r), (pb[0], pb[1], z - .22 + r), r, c, seg=6)
        if tag:                                                                   # tray ID tags on the outer rail
            for k in range(1, int(L // 30) + 1):
                t = k * 30 / L
                px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                if alongx:
                    decal((px, py - w / 2 - .08, z - .1), (0, -1, 0), 2.4, .42, [(tag, .7, True, None)], bg="#ffd200")
                else:
                    decal((px - w / 2 - .08, py, z - .1), (-1, 0, 0), 2.4, .42, [(tag, .7, True, None)], bg="#ffd200")
        n = max(1, int(L // stand))
        for k in range(n + 1):                                                    # T-stanchions
            t = k / n
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if not S.free(px - .5, px + .5, py - .5, py + .5, .7, z - .7, m=.1):
                continue
            box(px - .3, px + .3, py - .3, py + .3, 0, z - .4, "steel")
            box(px - .6, px + .6, py - .6, py + .6, 0, .5, "concrete")
            if alongx:
                box(px - .2, px + .2, py - w / 2 - .2, py + w / 2 + .2, z - .6, z - .35, "steel")
            else:
                box(px - w / 2 - .2, px + w / 2 + .2, py - .2, py + .2, z - .6, z - .35, "steel")
    return z


def drop(S, x, y, z_top, z_bot, n=3):
    """Armored cable drop from the tray to a JB / panel: cables in a short vertical ladder."""
    if not S.free(x - .5, x + .5, y - .3, y + .3, max(z_bot + .2, 7.1), z_top - .5, m=0):
        return False
    for s in (-.4, .4):
        box(x + s - .05, x + s + .05, y - .05, y + .05, z_bot, z_top, "pipe")
    for j in range(n):
        c = "cable_mc" if j == 0 else "cable_inst"
        rod((x - .25 + j * .25, y, z_top - .2), (x - .25 + j * .25, y, z_bot + .4), .13, c, seg=6)
        rod((x - .25 + j * .25, y, z_bot + .4), (x - .25 + j * .25, y, z_bot), .2, "steel", seg=8)   # sealing gland
    for zc in range(int(z_bot) + 1, int(z_top)):
        box(x - .45, x + .45, y - .05, y + .05, zc, zc + .08, "pipe")                 # drop-ladder rungs
    S.add([x - .5, y - .3, z_bot, x + .5, y + .3, z_top])
    return True


def trunk_to(S, pts, jx, jy):
    """Nearest point on the trunk polyline to (jx, jy) along an orthogonal spur."""
    best = None
    for a, b in zip(pts, pts[1:]):
        if a[1] == b[1] and min(a[0], b[0]) <= jx <= max(a[0], b[0]):
            d = abs(jy - a[1])
            if best is None or d < best[0]:
                best = (d, (jx, a[1]))
        if a[0] == b[0] and min(a[1], b[1]) <= jy <= max(a[1], b[1]):
            d = abs(jx - a[0])
            if best is None or d < best[0]:
                best = (d, (a[0], jy))
    return best


TAGS = {"Gas yard": "GY-T", "Pipeline M&R station": "MR-T"}


def cable_runs(S, area, trunks, riser, jbs, extra=()):
    """Trunk trays from the control building riser, spurs to each JB stand with a cable drop, and extra drops."""
    it = fuel.new_item("BASE_UTILITIES", f"{area}: cable tray and drops (ARMOR-X MC-HL power, TC-ER control, "
                       "instrument and fire-alarm cable)", (1560, 1940, 1430, 1900), (0, 14), area="D",
                       sheet="typical (fuel detail)", register=False,
                       info="Class I Div 2 Group D: MC-HL and TC-ER in ladder tray on T-stanchions (NEC 501.10(B)), "
                            "drops to explosion-proof JBs through sealed fittings; heat-trace and lighting circuits.")
    on(it)
    fuel.D = True
    zt = None
    allpts = []
    for pts in trunks:
        z = tray(S, pts, 9.0, name=area, tag=TAGS.get(area, "T-1") + f"{len(allpts) + 1}")
        if z:
            zt = z if zt is None else zt
            allpts.append((pts, z))
    rx, ry, rz0 = riser
    if zt and allpts:
        z = allpts[0][1]
        for s in (-.6, .6):
            box(rx + s - .06, rx + s + .06, ry - .06, ry + .06, rz0, z, "pipe")
        for j, (c, r) in enumerate(CABLES[:4]):
            rod((rx - .4 + j * .27, ry, rz0), (rx - .4 + j * .27, ry, z - .2), r * .8, c, seg=6)
    n = 0
    for (jx, jy) in jbs:
        for (pts, z) in allpts:
            b = trunk_to(S, pts, jx, jy - .35)
            if b and b[0] < 60:
                (tx, ty) = b[1]
                sp = [(tx, ty), (jx, ty), (jx, jy - .35)] if abs(tx - jx) > .5 else [(tx, ty), (jx, jy - .35)]
                sp = [p for i, p in enumerate(sp) if i == 0 or p != sp[i - 1]]
                if len(sp) > 1 and tray(S, sp, z, w=.75, cables=(("cable_mc", .14), ("cable_inst", .1)),
                                        stand=12, name=area + " spur") and drop(S, jx, jy - .35, z, 6.5):
                    n += 1
                break
    for (x, y, zb) in extra:
        for (pts, z) in allpts:
            b = trunk_to(S, pts, x, y)
            if b and b[0] < 40:
                (tx, ty) = b[1]
                sp = [(tx, ty), (x, ty), (x, y)] if abs(tx - x) > .5 and abs(ty - y) > .5 else [(tx, ty), (x, y)]
                sp = [p for i, p in enumerate(sp) if i == 0 or p != sp[i - 1]]
                if len(sp) > 1 and tray(S, sp, z, w=.75, cables=(("cable_mc", .16), ("cable_tc", .1)),
                                        stand=12, name=area + " spur") and drop(S, x, y, z, zb):
                    n += 1
                break
    fuel.D = False
    print(f"gas_lod3: {area}: {len(allpts)} trunks, {n} drops")


def build():
    S = Space()
    yard_equipment(S)
    gas_yard(S)
    jb_yard = list(JBS)
    del JBS[:]
    mr_station(S)
    jb_mr = list(JBS)
    cable_runs(S, "Gas yard",
               [[(1580, 1455.5), (1580, 1462), (1631.5, 1462), (1631.5, 1510), (1755, 1510), (1755, 1600),
                 (1715, 1600)],
                [(1765, 1556), (1866, 1556)]],
               (1580, 1455.5, 5.5), jb_yard,
               extra=((1788.5, 1527.4, 8.8), (1699, 1557.2, 9.4), (1592.5, 1452.3, 7.2)))
    cable_runs(S, "Pipeline M&R station",
               [[(1748, 1742), (1748, 1806), (1600, 1806), (1600, 1866)],
                [(1748, 1776), (1733, 1776)]],
               (1748, 1742, 2.0), jb_mr)
    return 1
