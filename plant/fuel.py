"""Fuel systems at LOD 3: plant gas yard, pipeline M&R train, GT gas fuel modules, the
conditional ULSD backup-fuel area and the modular-yard gas skids.

Drawn footprints and envelopes (SK-3X1-01 / -07 / -12 / -14) are kept; what goes inside
them is typical, not engineered: vessels on saddles with heads, nozzles, relief valves and
sump boots; metering and regulation runs with block, slam-shut, monitor and control valves;
interconnecting piping on concrete sleepers in process order. Piping between equipment is
dressing ("d": 1) so it never counts as a clash.

    import fuel; fuel.build(ns)      # ns: build_model's item(), items, parts, layers
"""
import math

G = {}            # build_model namespace: item, items, parts
D = False         # current parts are dressing
GAS, OIL = "fuelgas", "fueloil"


def _add(kind, **kw):
    it = G["cur"]
    kw.setdefault("item", it["id"])
    kw.setdefault("layer", it["layer"])
    if D:
        kw["d"] = 1
    G["parts"].append(dict(kind=kind, **kw))


def box(x0, x1, y0, y1, z0, z1, c, layer=None):
    _add("box", min=[round(min(x0, x1), 2), round(min(y0, y1), 2), round(z0, 2)],
         max=[round(max(x0, x1), 2), round(max(y0, y1), 2), round(max(z1, z0 + .05), 2)], color=c,
         **({"layer": layer} if layer else {}))


def rod(a, b, r, c, r2=None, seg=12, layer=None):
    _add("rod", a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=r, r2=r if r2 is None else r2,
         color=c, seg=seg, **({"layer": layer} if layer else {}))


def new_item(layer, name, fp, z, **meta):
    meta.setdefault("basis", "typical")
    G["cur"] = G["item"](layer, name, fp, z, **meta)
    return G["cur"]


def on(it):
    G["cur"] = it


def find(prefix):
    return next(it for it in G["items"] if it["name"].startswith(prefix))


def strip(it):
    """Drop an item's primary parts (it is rebuilt here inside the same envelope)."""
    G["parts"][:] = [p for p in G["parts"] if p["item"] != it["id"] or p.get("d")]
    G["cur"] = it


# ---------------------------------------------------------------------------------------
# building blocks
def pipe(pts, z, r, c=GAS, layer=None, elbows=True):
    """Polyline pipe at one elevation (or 3-D points), with flanged elbows."""
    P = [(p[0], p[1], p[2] if len(p) > 2 else z) for p in pts]
    for a, b in zip(P, P[1:]):
        rod(a, b, r, c, seg=12, layer=layer)
    if elbows:
        for p in P[1:-1]:
            rod((p[0], p[1], p[2] - r * 1.15), (p[0], p[1], p[2] + r * 1.15), r * 1.15, c, seg=12, layer=layer)


def flange(p, axis, r, c="steel", layer=None):
    d = [0, 0, 0]
    d[axis] = .12
    rod([p[i] - d[i] for i in range(3)], [p[i] + d[i] for i in range(3)], r * 1.7, c, seg=14, layer=layer)


def valve(p, axis, r, kind="hand", layer=None):
    """Gate / ball valve on a line along `axis` (0 x, 1 y, 2 z): body, flanges and an operator.
    kind: hand (handwheel), mov (motor operator), esd (red spring-return actuator),
    ctrl (amber diaphragm actuator), slam (red slam-shut head)."""
    x, y, z = p
    L = r * 2.6
    d = [0, 0, 0]
    d[axis] = L / 2
    rod((x - d[0], y - d[1], z - d[2]), (x + d[0], y + d[1], z + d[2]), r * 1.35, "steel", seg=12, layer=layer)
    for s in (-1, 1):
        flange((x + s * d[0], y + s * d[1], z + s * d[2]), axis, r, layer=layer)
    if axis == 2:            # vertical line: operator to the side
        rod((x, y, z), (x + r * 3, y, z), r * .35, "steel", seg=6, layer=layer)
        rod((x + r * 3, y, z - r * 1.2), (x + r * 3, y, z + r * 1.2), r * 1.2, "amber", seg=12, layer=layer)
        return
    top = z + r * 1.35
    if kind == "hand":
        rod((x, y, top), (x, y, top + r * 2.4), r * .25, "steel", seg=6, layer=layer)
        rod((x, y, top + r * 2.4), (x, y, top + r * 2.6), r * 1.5, "red", seg=16, layer=layer)
    elif kind == "mov":
        box(x - r * .9, x + r * .9, y - r * .9, y + r * .9, top, top + r * 2.4, "motor", layer=layer)
    elif kind == "esd":
        rod((x, y, top), (x, y, top + r * 1.2), r * .5, "steel", seg=8, layer=layer)
        ax = (1, 0) if axis == 1 else (0, 1)
        rod((x - ax[0] * r * 2, y - ax[1] * r * 2, top + r * 1.8), (x + ax[0] * r * 2, y + ax[1] * r * 2, top + r * 1.8),
            r * .95, "red", seg=14, layer=layer)
    elif kind == "ctrl":
        rod((x, y, top), (x, y, top + r * 1.6), r * .3, "steel", seg=6, layer=layer)
        rod((x, y, top + r * 1.6), (x, y, top + r * 2.4), r * 1.7, "amber", r2=r * 1.2, seg=16, layer=layer)
    elif kind == "slam":
        rod((x, y, top), (x, y, top + r * 1.4), r * .35, "steel", seg=6, layer=layer)
        rod((x, y, top + r * 1.4), (x, y, top + r * 2.2), r * 1.1, "red", seg=14, layer=layer)


def hvessel(x0, x1, y, z, r, c="tank", saddles=(), boot=None, closure=None, nozzles=(), psv=None):
    """Horizontal pressure vessel along x: 2:1 heads, concrete saddles, optional sump boot,
    quick-opening closure, top nozzles and a relief valve."""
    h = r * .45
    rod((x0 + h, y, z), (x1 - h, y, z), r, c, seg=22)
    rod((x0, y, z), (x0 + h, y, z), r * .55, c, r2=r, seg=22)
    rod((x1 - h, y, z), (x1, y, z), r, c, r2=r * .55, seg=22)
    for xs in saddles:
        box(xs - .7, xs + .7, y - r * .75, y + r * .75, 0, z - r * .55, "concrete")
        box(xs - .9, xs + .9, y - r * .8, y + r * .8, z - r * .62, z - r * .5, "steel")
    if boot is not None:
        rod((boot, y, z - r * .8), (boot, y, max(.3, z - r - 2.2)), r * .32, c, seg=14)
    if closure == "west":
        rod((x0 - .2, y, z), (x0 + .25, y, z), r * .62, "steel", seg=18)
    elif closure == "east":
        rod((x1 - .25, y, z), (x1 + .2, y, z), r * .62, "steel", seg=18)
    for xn in nozzles:
        rod((xn, y, z + r * .9), (xn, y, z + r + .9), .45, c, seg=10)
        rod((xn, y, z + r + .8), (xn, y, z + r + 1.0), .8, "steel", seg=12)
    if psv is not None:
        xn = psv
        rod((xn, y, z + r * .9), (xn, y, z + r + .8), .25, "steel", seg=8)
        rod((xn, y, z + r + .8), (xn, y, z + r + 1.9), .32, "red", seg=10)
        rod((xn, y, z + r + 1.4), (xn + 1.2, y, z + r + 1.4), .2, "steel", seg=6)


def sleepers(pts, z, r, step=14, skip=()):
    """Concrete sleepers with a steel shoe under a pipe at elevation z."""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L // step))
        for k in range(1, n + 1):
            t = k / (n + 1) if L > step else .5
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            if any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, x1, y0, y1) in skip):
                continue
            along_x = abs(bx - ax) > abs(by - ay)
            hx, hy = (.6, 1.5) if along_x else (1.5, .6)
            box(x - hx, x + hx, y - hy, y + hy, 0, z - r - .25, "concrete")
            box(x - hx * .5, x + hx * .5, y - hy * .5, y + hy * .5, z - r - .25, z - r, "steel")


def canopy(x0, x1, y0, y1, z, c="roof"):
    for (x, y) in ((x0 + .4, y0 + .4), (x1 - .4, y0 + .4), (x0 + .4, y1 - .4), (x1 - .4, y1 - .4)):
        box(x - .25, x + .25, y - .25, y + .25, 0, z, "steel")
    box(x0, x1, y0, y1, z, z + .45, c)
    box(x0 + .3, x1 - .3, y0 + .3, y1 - .3, z - .5, z, "steel")


def skid_runs(x0, x1, y0, y1, ys, z, r, trim, c=GAS, base="steel"):
    """Skid with parallel runs along x between an inlet header (x0) and an outlet header (x1).
    trim: list of (x, kind) valves / instruments on every run."""
    box(x0, x1, y0, y1, 0, .9, base)
    for x in (x0 + 2, (x0 + x1) / 2, x1 - 2):
        for y in ys:
            box(x - .5, x + .5, y - .5, y + .5, .9, z - r, "steel")
    xa, xb = x0 + 2.5, x1 - 2.5
    for y in ys:
        rod((xa, y, z), (xb, y, z), r, c, seg=12)
        for (x, kind) in trim:
            if kind == "meter":
                rod((x - 1.5, y, z), (x + 1.5, y, z), r * 1.6, "machine", seg=16)
                box(x - .5, x + .5, y - .5, y + .5, z + r * 1.6, z + r * 1.6 + 1.2, "panel")
            elif kind == "fc":       # flow conditioner flange pair
                flange((x, y, z), 0, r)
            elif kind == "filter":
                rod((x, y, z - r * 2.4), (x, y, z + r * 3.4), r * 1.9, "tank", seg=16)
                rod((x, y, z + r * 3.4), (x, y, z + r * 3.8), r * 2.1, "steel", seg=16)
            else:
                valve((x, y, z), 0, r, kind)
    for xh in (xa, xb):
        rod((xh, min(ys) - r, z), (xh, max(ys) + r, z), r * 1.15, c, seg=12)


# ---------------------------------------------------------------------------------------
def gas_yard():
    """Plant gas yard (SK-3X1-12): inlet ESD -> (conditional compressors) -> metering ->
    pressure regulation -> performance heater -> final filter-separators -> GT header."""
    global D
    L = "BASE_UTILITIES"
    # inlet ESD / block-valve station at the pad edge where the M&R line arrives
    new_item(L, "Gas yard inlet: ESD valve, block valve and insulating joint", (1708, 1722, 1617, 1639), (0, 8),
             area="D", sheet="typical (fuel detail)", info="Fail-closed ESD valve tripped by the fire and gas "
             "system; manual block valve; insulating joint between the operator's and the plant's cathodic "
             "protection.")
    box(1708, 1722, 1617, 1639, 0, .6, "concrete")
    rod((1715, 1639, 4), (1715, 1617, 4), .7, GAS)
    valve((1715, 1633, 4), 1, .7, "hand")
    valve((1715, 1625, 4), 1, .7, "esd")
    rod((1715, 1620.4, 4), (1715, 1619.6, 4), 1.0, "amber")         # insulating joint
    for y in (1636.5, 1629, 1621):
        box(1714, 1716, y - .4, y + .4, .6, 3.3, "steel")
    box(1718, 1721.5, 1630, 1632, .6, 5.5, "panel")                # solenoid / local panel

    # vent stack for maintenance blowdown
    new_item(L, "Gas yard vent stack (maintenance blowdown)", (1594, 1606, 1594, 1606), (0, 40), area="D",
             sheet="typical (fuel detail)", info="Cold vent for depressurizing the yard; vent header from "
             "the inlet station and the relief valves.")
    box(1594, 1606, 1594, 1606, 0, 1, "concrete")
    rod((1600, 1600, 1), (1600, 1600, 40), .75, "stack", seg=14)
    rod((1600, 1600, 39.3), (1600, 1600, 40.2), 1.0, "red", seg=14)
    for ang in (0, 2.09, 4.19):                                   # guy wires
        rod((1600, 1600, 30), (1600 + 5.5 * math.cos(ang), 1600 + 5.5 * math.sin(ang), 1), .06, "steel", seg=4)

    # filter-separators: two 100% horizontal vessels with sump boots, closures and relief valves
    fs = find("Gas yard filter-separators")
    strip(fs)
    fs["info"] = "Two 100% final filter-separators downstream of the heater: quick-opening closures, sump boots, relief valves."
    for y in (1475, 1485):
        hvessel(1643, 1677, y, 6, 3.5, saddles=(1649, 1671), boot=1673, closure="west", nozzles=(1655,), psv=1665)
        rod((1673, y, 1.6), (1673, y + 2.6, 1.6), .2, "pipe", seg=6)                # boot drain
    rod((1679, 1474, 6), (1679, 1486, 6), .55, GAS)                                   # inlet header
    rod((1641, 1474, 6), (1641, 1486, 6), .55, GAS)                                   # outlet header
    for y in (1475, 1485):
        rod((1677, y, 6), (1679, y, 6), .5, GAS)
        valve((1678.2, y, 6), 0, .45, "hand")
    box(1640, 1680, 1489, 1490, 0, .3, "concrete")

    # performance heater: shell-and-tube, gas in the tubes, IP feedwater on the shell side
    ph = find("Fuel-gas performance heater")
    strip(ph)
    ph["info"] = "Shell-and-tube: fuel gas heated to ~365 F by IP feedwater for GT efficiency (typical)."
    rod((1706, 1480, 7), (1735, 1480, 7), 5.6, "tank", seg=24)
    rod((1702, 1480, 7), (1706, 1480, 7), 5.2, "tank", r2=5.6, seg=24)
    rod((1735, 1480, 7), (1737.5, 1480, 7), 6.1, "steel", seg=24)                 # channel flange
    rod((1737.5, 1480, 7), (1740, 1480, 7), 5.8, "tank", r2=3.8, seg=24)          # channel head
    for xs in (1711, 1730):
        box(xs - .8, xs + .8, 1475, 1485, 0, 2.4, "concrete")
    for xn in (1712, 1729):                                                         # shell nozzles
        rod((xn, 1480, 12.3), (xn, 1480, 13.6), .6, "tank", seg=10)
        rod((xn, 1480, 13.5), (xn, 1480, 13.8), 1.0, "steel", seg=12)
    rod((1724, 1480, 12.4), (1724, 1480, 14), .22, "red", seg=8)                  # shell PSV

    # metering skid (plant check meter, 2 x 100% ultrasonic runs) under a sunshade
    me = find("Gas metering skid")
    strip(me)
    me["info"] = "Plant check metering: 2 x 100% ultrasonic runs with flow conditioners and block valves; " \
                 "flow computer and gas chromatograph cabinet."
    skid_runs(1640, 1690, 1521, 1539, (1526, 1534), 4, .55,
              [(1649, "hand"), (1657, "fc"), (1667, "meter"), (1681, "hand")])
    box(1684, 1688.5, 1537, 1539, .9, 6.5, "panel")
    canopy(1640.5, 1689.5, 1520.5, 1539.5, 9.4)

    # pressure regulation: slam-shut, monitor and active regulator per run, relief vent
    rg = find("Gas pressure regulation skid")
    strip(rg)
    rg["info"] = "2 x 100% runs: slam-shut valve, monitor and active pressure-control valves, " \
                 "outlet block valve; full-capacity relief valve to the vent header."
    skid_runs(1710, 1750, 1521, 1539, (1525, 1535), 4, .55,
              [(1717, "hand"), (1723, "slam"), (1731, "ctrl"), (1739, "ctrl"), (1745, "hand")])
    rod((1747.5, 1537, 4), (1747.5, 1537, 11.6), .25, "pipe", seg=8)
    rod((1747.5, 1537, 11.4), (1747.5, 1537, 12), .4, "red", seg=10)

    # conditional fuel-gas compressors: three packages, scrubbers, aftercooler bays
    fc = find("CONDITIONAL: fuel-gas compressors")
    strip(fc)
    box(1800, 1930, 1560, 1630, 0, .6, "concrete")
    for k in range(3):
        x0 = 1806 + 42 * k
        box(x0, x0 + 34, 1566, 1586, .6, 1.6, "steel")
        rod((x0 + 2, 1576, 5.2), (x0 + 12, 1576, 5.2), 3.4, "motor", seg=20)               # motor
        box(x0 + 12, x0 + 14, 1572, 1580, 1.6, 7.5, "steel")                                 # coupling guard
        box(x0 + 14, x0 + 30, 1569, 1583, 1.6, 9.5, "conditional")                           # compressor frame
        for xc in (x0 + 17, x0 + 22, x0 + 27):                                               # cylinders
            rod((xc, 1567, 6), (xc, 1585, 6), 1.7, "machine", seg=16)
        rod((x0 + 32, 1594, .6), (x0 + 32, 1594, 15), 2.0, "conditional", seg=18)            # suction scrubber
        rod((x0 + 32, 1594, 15), (x0 + 32, 1594, 16.2), 1.2, "conditional", r2=.4, seg=18)
        rod((x0 + 32, 1594, 16.2), (x0 + 32, 1594, 19.5), .22, "red", seg=8)                # PSV / vent
        # aftercooler: bundle on legs, two fans
        for (xl, yl) in ((x0 + 2, 1600), (x0 + 30, 1600), (x0 + 2, 1626), (x0 + 30, 1626)):
            box(xl - .3, xl + .3, yl - .3, yl + .3, .6, 11, "steel")
        box(x0 + 1, x0 + 31, 1599, 1627, 11, 13.2, "bundle")
        for xf in (x0 + 9, x0 + 23):
            rod((xf, 1613, 13.2), (xf, 1613, 13.9), 6, "fan", seg=24)
            rod((xf, 1613, 13.9), (xf, 1613, 14.4), 1.2, "fanhub", seg=12)

    # yard piping, in process order, on sleepers (dressing on the pad)
    on(find("Plant gas yard (pad)"))
    D = True
    main = [(1715, 1617), (1715, 1580), (1644, 1580), (1644, 1537)]
    pipe(main, 4, .7)
    valve((1715, 1599, 4), 1, .7, "hand")                                            # compressor bypass
    pipe([(1690, 1530), (1710, 1530)], 4, .6)                                        # meter -> regulation
    heat = [(1747.5, 1530), (1760, 1530), (1760, 1480), (1745, 1480)]
    pipe(heat, 4, .6)
    pipe([(1745, 1480, 4), (1745, 1480, 7), (1740, 1480, 7)], 4, .6)                  # into the channel head
    pipe([(1702, 1480, 7), (1695, 1480, 7), (1695, 1480, 4), (1679, 1480, 4), (1679, 1480, 6)], 4, .6)
    out = [(1641, 1480, 6), (1641, 1480, 4), (1560, 1480, 4)]
    pipe(out, 4, .7)
    valve((1625, 1480, 4), 0, .7, "mov")                                             # yard outlet MOV
    valve((1590, 1480, 4), 0, .7, "esd")                                             # GT header ESD
    # compressor suction / discharge (conditional)
    pipe([(1715, 1608), (1806, 1608), (1806, 1594), (1830, 1594)], 4, .55, "conditional")
    pipe([(1820, 1572), (1820, 1590), (1715, 1590)], 4.0, .55, "conditional")
    # vent header to the stack
    pipe([(1708, 1612), (1610, 1612), (1610, 1600), (1601, 1600)], 2.4, .3, "pipe")
    # hot IP feedwater to the performance heater (from the HRSG area, typical)
    for xn in (1712, 1729):                                                          # to the feedwater routes
        pipe([(xn, 1480, 13.8), (xn, 1480, 15.5), (xn, 1493, 15.5), (xn, 1493, 12)], 12, .45, "feedwater")
    # tie-ins for the optional systems (shown with their layers)
    pipe([(1812, 1640), (1812, 1636), (1716, 1636)], 4, .55, GAS, layer="OPT_LNG_ROUTES")
    pipe([(1800, 1488), (1761, 1488)], 4, .45, GAS, layer="OPT_H2_ROUTES")
    pipe([(1760, 1480), (1760, 1440), (1750, 1440), (1750, 1430)], 4, .55, GAS, layer="OPT_MOD_ROUTES")
    pipe([(1760, 1505), (1945, 1505), (1945, 1440)], 4, .55, GAS, layer="OPT_TMP_ROUTES")
    sleepers(main, 4, .7)
    sleepers([(1715, 1608), (1806, 1608)], 4, .55)
    sleepers([(1820, 1590), (1715, 1590)], 4, .55)
    sleepers(heat, 4, .6)
    sleepers([(1641, 1480), (1560, 1480)], 4, .7)
    D = False


def mr_station():
    """Pipeline M&R (SK-3X1-14 keys 1-9): pig receiver -> ESD -> filter-separator -> line
    heaters -> custody meters -> regulation building -> plant gas yard."""
    global D
    pr = find("M&R 1: pig receiver")
    strip(pr)
    rod((1606, 1890.5, 3.5), (1606, 1895, 3.5), .75, GAS, r2=1.2)                  # pipeline in, reducer
    rod((1606, 1856, 3.5), (1606, 1890.5, 3.5), 2.0, GAS, seg=18)                  # barrel
    rod((1606, 1853.3, 3.5), (1606, 1856, 3.5), 2.5, "steel", seg=18)              # quick-opening closure
    rod((1609.6, 1852.4, .2), (1609.6, 1852.4, 7.5), .2, "steel", seg=6)           # closure davit
    rod((1609.6, 1852.4, 7.5), (1606, 1852.4, 7.5), .2, "steel", seg=6)
    for y in (1862, 1884):
        box(1604.6, 1607.4, y - .6, y + .6, 0, 1.6, "concrete")
    pipe([(1606, 1859, 3.5), (1610.5, 1859, 3.5)], 3.5, .55, elbows=False)        # gas outlet nozzle
    rod((1606, 1872, 5.5), (1606, 1872, 6), .5, "red", seg=8)                      # pig signaller

    esd = find("M&R 2: insulating joint")
    strip(esd)
    box(1602, 1610, 1830, 1838, 0, .5, "concrete")
    rod((1606, 1838, 3.5), (1606, 1830, 3.5), .55, GAS)
    rod((1606, 1836.8, 3.5), (1606, 1836.2, 3.5), .9, "amber")
    valve((1606, 1833, 3.5), 1, .55, "esd")

    fs = find("M&R 3: horizontal filter-separator")
    strip(fs)
    hvessel(1632, 1663, 1851, 6.5, 4.5, saddles=(1638, 1657), boot=1657.5, closure="west", nozzles=(1641, 1655),
            psv=1648)

    for k, y in enumerate([1820, 1838, 1856], 1):
        lh = find(f"M&R 4: line heater {k}")
        strip(lh)
        lh["z"] = [0, 16]
        yc = y + 5
        rod((1692, yc, 5), (1714, yc, 5), 4.6, "tank", seg=20)                     # water bath
        rod((1691, yc, 5), (1692, yc, 5), 4.9, "steel", seg=20)
        box(1714, 1720, yc - 3.5, yc + 3.5, 0, 8, "machine")                       # burner / firebox end
        rod((1717, yc, 8), (1717, yc, 16), .7, "stack", seg=12)                     # exhaust stack
        rod((1717, yc, 15.6), (1717, yc, 16), .95, "steel", seg=12)
        rod((1700, yc, 9.4), (1700, yc, 10), .9, "tank", seg=12)                    # expansion tank
        for xs in (1696, 1710):
            box(xs - .7, xs + .7, yc - 3.5, yc + 3.5, 0, 1.2, "concrete")
        box(1711, 1713.5, yc + 3.6, yc + 4.4, 0, 5.5, "panel")                     # burner management panel

    me = find("M&R 5: ultrasonic meters")
    strip(me)
    skid_runs(1620, 1670, 1771, 1785, (1774, 1782), 3.5, .5,
              [(1631, "hand"), (1645, "meter"), (1655, "fc"), (1663, "hand")])
    box(1621, 1669, 1771.2, 1784.8, 5.5, 6, "roof")
    for (x, y) in ((1621.3, 1771.5), (1668.7, 1771.5), (1621.3, 1784.5), (1668.7, 1784.5)):
        box(x - .2, x + .2, y - .2, y + .2, .9, 5.5, "steel")

    # interconnecting piping (dressing on the station pad)
    on(find("Pipeline M&R station"))
    D = True
    p1 = [(1610.5, 1859), (1612, 1859), (1612, 1846), (1606, 1846), (1606, 1838)]
    pipe(p1, 3.5, .55)
    p2 = [(1606, 1830), (1606, 1822), (1625, 1822), (1625, 1851)]
    pipe(p2, 3.5, .55)
    pipe([(1625, 1851, 3.5), (1625, 1851, 6.5), (1632, 1851, 6.5)], 3.5, .55)
    pipe([(1663, 1851, 6.5), (1674, 1851, 6.5), (1674, 1851, 3.5), (1680, 1851, 3.5)], 3.5, .55)
    pipe([(1680, 1824), (1680, 1862)], 3.5, .6)                                     # heater inlet manifold
    pipe([(1727, 1824), (1727, 1862)], 3.5, .6)                                     # outlet manifold
    for yc in (1825, 1843, 1861):
        pipe([(1680, yc), (1691, yc)], 3.5, .45, elbows=False)
        pipe([(1720, yc), (1727, yc)], 3.5, .45, elbows=False)
        valve((1685, yc, 3.5), 0, .45, "hand")
    p3 = [(1727, 1824), (1727, 1800), (1667.5, 1800), (1667.5, 1784)]
    pipe(p3, 3.5, .55)
    p4 = [(1622.5, 1778), (1614, 1778), (1614, 1752), (1695, 1752), (1695, 1775), (1700, 1775)]
    pipe(p4, 3.5, .55)
    pipe([(1650, 1857.2, 1.8), (1650, 1870, 1.8), (1744, 1870, 1.8), (1744, 1861, 1.8)], 1.8, .22, "pipe")  # liquids
    pipe([(1640, 1771, 2), (1640, 1745, 2), (1628, 1745, 2), (1628, 1738, 2)], 2, .12, "pipe")  # sample line
    for pts in (p2, p3, p4, [(1680, 1824), (1680, 1862)], [(1727, 1824), (1727, 1862)]):
        sleepers(pts, 3.5, .55, step=12)
    D = False


def gt_modules():
    """GT gas fuel modules on the turbine deck, fed by the fuel-gas branches (and the
    conditional fuel-oil branches) rising at the north wall of the hall."""
    global D
    L = "BASE_POWER_BLOCK"
    for k in range(3):
        dx = 160 * k
        x0 = 678 + dx
        new_item(L, f"GFM-{k + 1}: GT{k + 1} gas fuel module (stop / control valves, final strainer)",
                 (x0, x0 + 16, 508, 559), (20, 30), tag=f"GFM-{k + 1}", area="A", sheet="typical (fuel detail)",
                 info="Enclosed valve module beside the GT: gas stop/ratio and control valves, final strainer, "
                      "vent valves; liquid-fuel module and pumps if backup ULSD is kept (typical).")
        box(x0, x0 + 16, 510, 530, 20, 27.6, "equip")
        box(x0 - .4, x0 + 16.4, 509.6, 530.4, 27.6, 28.1, "roof")
        D = True
        box(x0 + 16, x0 + 16.15, 513, 519, 20, 26.5, "door")
        box(x0 + 3, x0 + 13, 530, 531.2, 23, 26.5, "louvre")
        xg, xo = 686 + dx, 682 + dx
        pipe([(xg, 558.3, 4), (xg, 558.3, 25), (xg, 530, 25)], 25, .6)                 # gas riser
        pipe([(xo, 558.3, 6.5), (xo, 558.3, 23.5), (xo, 530, 23.5)], 23.5, .4, OIL)     # oil riser
        valve((xg, 545, 25), 1, .6, "mov")
        pipe([(x0, 514, 25), (x0 - 2, 514, 25), (x0 - 2, 514, 32), (643 + dx, 514, 32)], 32, .55)
        pipe([(x0, 525, 24), (x0 - 4, 525, 24), (x0 - 4, 525, 31), (643 + dx, 525, 31)], 31, .35, OIL)
        for y in (540, 552):                                                            # pipe support frame
            box(xo - 2, xg + 2, y - .3, y + .3, 22.6, 23.1, "steel")
            box(xo - 2, xo - 1.6, y - .3, y + .3, 20, 22.6, "steel")
            box(xg + 1.6, xg + 2, y - .3, y + .3, 20, 22.6, "steel")
        D = False


def ulsd():
    """Conditional backup fuel: truck unloading, containment dike, unloading / forwarding pumps."""
    global D
    L = "BASE_UTILITIES"
    new_item(L, "CONDITIONAL: ULSD tank containment dike", (1355, 1465, 1525, 1635), (0, 6), area="D",
             basis="conditional", info="Concrete dike wall around the backup fuel-oil tank (typical height).")
    for b in ((1355, 1465, 1525, 1526.2), (1355, 1465, 1633.8, 1635), (1355, 1356.2, 1525, 1635),
              (1463.8, 1465, 1525, 1635)):
        box(*b, 0, 6, "concrete")
    D = True
    for (x, y) in ((1410, 1525.6), (1440, 1525.6)):                                  # step-overs
        for s in (-1, 1):
            box(x - 1.5, x + 1.5, y + s * 1.2, y + s * 4.2, 0, 6.6 - 1.0 * abs(s), "grating")
        box(x - 1.5, x + 1.5, y - 1.2, y + 1.2, 6, 6.4, "grating")
    D = False

    new_item(L, "CONDITIONAL: ULSD truck unloading station (canopy, spill containment)",
             (1340, 1400, 1440, 1490), (0, 22), area="D", basis="conditional",
             info="One tanker bay under a canopy, curbed and drained to the oil-water separator; unloading arm.")
    box(1340, 1400, 1440, 1490, 0, .5, "concrete")
    for b in ((1340, 1400, 1440, 1441), (1340, 1400, 1489, 1490)):
        box(*b, .5, 1.2, "concrete")
    for x in (1343, 1397):
        for y in (1446, 1484):
            box(x - .6, x + .6, y - .6, y + .6, .5, 20, "steel")
    box(1338, 1402, 1442, 1488, 20, 21, "roof")
    box(1341, 1399, 1445, 1485, 19.3, 20, "steel")
    D = True
    # tanker truck (tractor + tank trailer) and the unloading arm
    box(1347, 1356, 1458, 1466, 1.5, 10, "red")                     # cab
    box(1347, 1356, 1458, 1466, 10, 10.6, "machine")
    box(1356, 1394, 1459, 1465, 1.5, 3.2, "steel")                  # chassis
    rod((1358, 1462, 7), (1393, 1462, 7), 3.6, "tank", seg=20)
    for x in (1351, 1361, 1384, 1389):
        for y in (1458, 1466):
            rod((x, y - .4, 1.6), (x, y + .4, 1.6), 1.6, "fanhub", seg=12)
    pipe([(1376, 1458.4, 4), (1376, 1452, 4), (1376, 1452, 9), (1376, 1446, 9), (1376, 1446, .5)], 4, .3, OIL)
    D = False

    new_item(L, "CONDITIONAL: ULSD unloading and forwarding pumps, duplex filters", (1415, 1475, 1448, 1480),
             (0, 10), area="D", basis="conditional",
             info="2 x 100% unloading pumps, 2 x 100% forwarding pumps to the GT liquid-fuel modules, duplex "
                  "strainers; skid under a sunshade.")
    box(1415, 1475, 1448, 1480, 0, .7, "concrete")
    for k, x in enumerate((1421, 1433, 1447, 1459)):
        box(x - 2.5, x + 4.5, 1455, 1461, .7, 1.4, "steel")
        rod((x - 1.5, 1458, 3), (x + 1, 1458, 3), 1.4, "pump", seg=14)
        rod((x + 1.3, 1458, 3), (x + 4.2, 1458, 3), 1.25, "motor", seg=14)
    for x in (1440, 1444):                                                                # duplex strainers
        rod((x, 1470, .7), (x, 1470, 5), 1.1, "tank", seg=14)
        rod((x, 1470, 5), (x, 1470, 5.6), 1.3, "steel", seg=14)
    canopy(1415.5, 1474.5, 1448.5, 1479.5, 9.4)
    D = True
    pipe([(1400, 1465), (1416, 1465), (1416, 1452), (1421, 1452), (1421, 1456)], 3, .35, OIL)       # arm -> pumps
    pipe([(1426, 1458, 3), (1430, 1458, 3), (1430, 1500, 3), (1430, 1500, 7.5), (1430, 1540, 7.5)], 3, .4, OIL)
    pipe([(1452, 1540, 7.5), (1452, 1500, 7.5), (1452, 1500, 3), (1452, 1466, 3), (1446, 1466, 3)], 3, .4, OIL)
    pipe([(1444, 1474, 3), (1470, 1474, 3), (1470, 1465, 3), (1475, 1465, 3), (1475, 1465, 6.5)], 3, .4, OIL)
    sleepers([(1430, 1482), (1430, 1500)], 3, .4)
    sleepers([(1452, 1482), (1452, 1500)], 3, .4)
    D = False


def modular_gas():
    """Gas conditioning skids for the simple-cycle units and the portable pad."""
    for prefix, (x0, x1, y0, y1), h in (("Gas conditioning skid", (1700, 1760, 1250, 1280), 10),
                                        ("Portable pad gas-conditioning skid", (2310, 2340, 430, 440), 8)):
        it = find(prefix)
        strip(it)
        it["info"] = (it.get("info") or "") + " Coalescing filters, heater and pressure control (typical)."
        if y1 - y0 >= 20:
            ys, r = (y0 + 7, y0 + 15, y0 + 23), .5
            skid_runs(x0, x1, y0, y1, ys, 4, r, [(x0 + 9, "filter"), (x0 + 19, "hand"), (x0 + 31, "ctrl"),
                                                   (x0 + 41, "slam"), (x0 + 51, "hand")])
            rod((x0 + 54, y1 - 3, 0), (x0 + 54, y1 - 3, h), .25, "pipe", seg=8)
        else:
            skid_runs(x0, x1, y0, y1, (y0 + 5,), 3.5, .45, [(x0 + 7, "filter"), (x0 + 15, "ctrl"),
                                                             (x0 + 23, "hand")])
            box(x1 - 4, x1 - 1, y1 - 2, y1 - .5, .9, 6.5, "panel")


def build(ns):
    G.update(ns)
    gas_yard()
    mr_station()
    gt_modules()
    ulsd()
    modular_gas()


# ---------------------------------------------------------------------------------------
LOW = ("fuel_gas", "fuel_oil", "feedwater", "cw", "chw", "hydrogen", "lng")
GAS_AREAS = ((1490, 1960, 1425, 1645), (1555, 1805, 1685, 1905))     # plant gas yard, M&R station


def _roads():
    return [it["fp"] for it in G["items"] if it["layer"] == "SITE" and "road" in it["name"].lower()]


def road_crossings(routes):
    """Low pipe routes (on sleepers or short posts) cannot cross a road at grade: split each
    one where it crosses a road and send that piece below grade in a sleeve (z < 0); the drop
    at each road edge is drawn by supports()."""
    roads, out, n = _roads(), [], 0
    for r in routes:
        if r["type"] not in LOW or not 0 < r["z"] <= 13:
            out.append(r)
            continue
        pts, cur, pieces = r["points"], [r["points"][0]], []
        for a, b in zip(pts, pts[1:]):
            ax, ay = a
            bx, by = b
            ivs = []
            if ax == bx or ay == by:
                horiz = ay == by
                for (x0, x1, y0, y1) in roads:
                    m = 3
                    if horiz and y0 - m <= ay <= y1 + m:
                        lo, hi = max(min(ax, bx), x0 - m), min(max(ax, bx), x1 + m)
                    elif not horiz and x0 - m <= ax <= x1 + m:
                        lo, hi = max(min(ay, by), y0 - m), min(max(ay, by), y1 + m)
                    else:
                        continue
                    if hi - lo > 6:
                        ivs.append((lo, hi))
            sgn = 1 if (bx - ax) + (by - ay) > 0 else -1
            ivs.sort(key=lambda iv: sgn * iv[0])
            for lo, hi in ivs:
                s0, s1 = (lo, hi) if sgn > 0 else (hi, lo)
                p0 = [s0, ay] if ay == by else [ax, s0]
                p1 = [s1, ay] if ay == by else [ax, s1]
                cur.append(p0)
                pieces.append(("up", cur))
                pieces.append(("down", [p0, p1]))
                cur = [p1]
                n += 1
            cur.append(b)
        pieces.append(("up", cur))
        for kind, pl in pieces:
            pl = [p for k, p in enumerate(pl) if k == 0 or p != pl[k - 1]]
            if len(pl) < 2:
                continue
            q = dict(r, points=[list(map(float, p)) for p in pl])
            if kind == "down":
                q["z"], q["h"] = -1.5, min(r["h"], 1.5)
                q["note"] = "road crossing, sleeved below grade"
            out.append(q)
    routes[:] = out
    return n


def supports(routes):
    """Sleepers / T-posts under low pipe routes, and the drop into each road-crossing sleeve.
    Supports stay out of buildings, equipment and roads."""
    global D
    roads = _roads()
    solid = [it["fp"] for it in G["items"] if it["layer"] != "SITE" and it["z"][1] > 1.5 and it["z"][0] < 1
             and not it["name"].startswith(("Pipe supports", "Pipe runs"))]
    xs = [p[0] for r in routes for p in r["points"]]
    ys = [p[1] for r in routes for p in r["points"]]
    new_item("PROCESS_PIPING", "Pipe supports and road-crossing sleeves (low pipe routes, typical)",
             (min(xs), max(xs), min(ys), max(ys)), (0, 13), register=False, sheet="typical (fuel detail)")
    D = True
    inside = lambda x, y, boxes, m=0: any(f[0] - m <= x <= f[1] + m and f[2] - m <= y <= f[3] + m for f in boxes)
    ends, count = set(), 0
    for r in routes:
        if r["type"] not in LOW:
            continue
        lay = r["layer"]
        if r["z"] < 0 and r.get("note", "").startswith("road crossing"):
            for (x, y) in (r["points"][0], r["points"][-1]):
                ends.add((round(x, 1), round(y, 1), lay, r["color"], r["w"], r["z"]))
            continue
        z, h, w = r["z"], r["h"], r["w"]
        bot = z - h / 2
        for (ax, ay), (bx, by) in zip(r["points"], r["points"][1:]):
            if ax != bx and ay != by:
                continue
            L = abs(bx - ax) + abs(by - ay)
            n = int(L // 20)
            for k in range(1, n + 1):
                t = k / (n + 1)
                x, y = ax + (bx - ax) * t, ay + (by - ay) * t
                if inside(x, y, solid, 1.5) or inside(x, y, roads, 2):
                    continue
                along_x = ay == by
                hx, hy = (.5, w / 2 + 1) if along_x else (w / 2 + 1, .5)
                if bot <= 5.5:
                    box(x - hx, x + hx, y - hy, y + hy, 0, bot - .2, "concrete", layer=lay)
                    box(x - hx * .6, x + hx * .6, y - hy * .8, y + hy * .8, bot - .2, bot, "steel", layer=lay)
                else:
                    box(x - .3, x + .3, y - .3, y + .3, 0, bot - .35, "steel", layer=lay)
                    box(x - hx, x + hx, y - hy, y + hy, bot - .35, bot, "steel", layer=lay)
                    box(x - .9, x + .9, y - .9, y + .9, 0, .4, "concrete", layer=lay)
                count += 1
    # sleeve ends: headwall and the pipe dropping from its route elevation into the sleeve
    up = {}
    for r in routes:
        if r["type"] in LOW and r["z"] > 0:
            for (x, y) in (r["points"][0], r["points"][-1]):
                up[(round(x, 1), round(y, 1), r["layer"])] = r
    for (x, y, lay, color, w, _) in ends:
        r = up.get((x, y, lay))
        if r is None:
            continue
        box(x - w / 2 - .8, x + w / 2 + .8, y - w / 2 - .8, y + w / 2 + .8, 0, .7, "concrete", layer=lay)
        if r["z"] <= 6:                     # the renderers already drop routes above EL 6 to grade
            rod((x, y, r["z"]), (x, y, 0), w / 2 * .9, color, seg=12, layer=lay)
    D = False
    return count
