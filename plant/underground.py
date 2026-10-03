"""Underground systems at LOD 3 (typical, not engineered).

Until now the buried systems were route data drawn as strips painted on grade. This builds them
below grade in real finishes, in their own layers (UNDERGROUND for the base plant,
OPT_UNDERGROUND for the design options), shown by the viewer's "U Underground" view with the
ground taken away:
- duct banks: concrete encasement (red-dyed top, the usual warning to excavators) at 2.5 ft cover
  along every buried cable route (13.8 kV / LV duct banks and the option feeders), the 230 kV cable
  banks deeper at 3.5 ft cover; precast manhole chambers under the covers at bends and every
  ~300 ft, handhole boxes at feeder ends;
- station ground grid: bare 4/0 Cu mesh at 1.5 ft depth under the power block, electrical areas
  and switchyard (40 ft mesh, 20 ft in the switchyard), driven rods at the perimeter, risers to
  the equipment;
- firewater ring main: ductile iron at 5 ft cover along the drawn ring and its branches;
- storm drainage: reinforced-concrete pipe under each road edge, catch-basin chambers with
  laterals, storm manholes at the junctions, the trunk to the pond inlet headwall;
- oily-water drains (HDPE): transformer containment sumps, turbine-hall lube-oil drains and the
  station transformers to the oil-water separator, separator to wastewater treatment;
- sanitary sewer (green PVC): buildings to a packaged lift station, force main to the site
  boundary;
- potable water (blue PVC) from the water treatment building to the buildings, service water
  to the power block.
Depths keep the systems apart: grid 1.5 ft, duct banks 2.5-4.5 ft, water 4.5 ft, firewater 5 ft,
sanitary 6 ft, oily water 6.5 ft, storm 7-8 ft.
"""
import math

import fuel
from fuel import box, rod, find

UG, UGO = "UNDERGROUND", "OPT_UNDERGROUND"
SHEET = "typical (underground)"


def _item(layer, name, info, **kw):
    return fuel.new_item(layer, name, (0, 2420, 0, 1920), (-12, .4), area=kw.pop("area", "A"), basis="typical",
                         sheet=SHEET, register=False, info=info, **kw)


def _merge(segs):
    """Collinear axis-aligned segments -> merged runs {(axis, c): [[a, b], ...]}."""
    runs = {}
    for (ax, ay), (bx, by) in segs:
        if ay == by and ax != bx:
            runs.setdefault(("x", ay), []).append((min(ax, bx), max(ax, bx)))
        elif ax == bx and ay != by:
            runs.setdefault(("y", ax), []).append((min(ay, by), max(ay, by)))
    out = {}
    for k, ivs in runs.items():
        ivs.sort()
        m = [list(ivs[0])]
        for a, b in ivs[1:]:
            if a <= m[-1][1] + 1e-6:
                m[-1][1] = max(m[-1][1], b)
            else:
                m.append([a, b])
        out[k] = m
    return out


def _pipe_run(pts, z, r, c, seg=10):
    for a, b in zip(pts, pts[1:]):
        za = a[2] if len(a) > 2 else z
        zb = b[2] if len(b) > 2 else z
        rod((a[0], a[1], za), (b[0], b[1], zb), r, c, seg=seg)


# ---------------------------------------------------------------------------------------------
def duct_banks(routes):
    """Concrete-encased duct banks along every buried cable route, red-dyed top."""
    groups = {}
    for r in routes:
        if r["type"] not in ("duct_bank", "mvlv_cable", "hv_cable") or r["z"] >= 0:
            continue
        opt = r["layer"].startswith("OPT_") or r["layer"] in ("SWYD_FUTURE", "HV_CORRIDOR")
        hv = r["type"] == "hv_cable"
        w = 3.0 if hv else (4.0 if r["type"] == "duct_bank" else 2.5)
        key = (opt, hv, w)
        groups.setdefault(key, []).extend(zip(r["points"], r["points"][1:]))
    n = 0
    for opt, hv in ((False, False), (False, True), (True, False), (True, True)):
        segs = {w: s for (o, h, w), s in groups.items() if o == opt and h == hv}
        if not segs:
            continue
        label = ("230 kV cable banks" if hv else "MV / LV duct banks") + (" (design options)" if opt else "")
        _item(UGO if opt else UG, f"Underground: {label}",
              "Concrete-encased PVC conduit banks, red-dyed top (excavation warning), "
              + ("3.5 ft cover, 230 kV XLPE cable in 8 in conduits with spare ways" if hv else
                 "2.5 ft cover, 5 in Schedule 40 PVC conduits (4 x 6 typical for the plant banks)")
              + "; warning tape 12 in above the bank.")
        top = -3.5 if hv else -2.5
        for w, s in segs.items():
            hw = w / 2
            for (axis, c), ivs in _merge(s).items():
                for a, b in ivs:
                    a0, b0 = a - hw, b + hw
                    if axis == "x":
                        box(a0, b0, c - hw, c + hw, top - 2.0, top - .12, "concrete")
                        box(a0, b0, c - hw, c + hw, top - .12, top, "ductcap")
                    else:
                        box(c - hw, c + hw, a0, b0, top - 2.0, top - .12, "concrete")
                        box(c - hw, c + hw, a0, b0, top - .12, top, "ductcap")
                    n += 1
    return n


def chambers():
    """Precast chambers under the manhole and handhole covers placed by station.manholes()."""
    mh = find("Duct-bank manholes and handholes")
    covers = [p for p in fuel.G["parts"] if p["item"] == mh["id"] and p["kind"] == "box" and p["color"] == "concrete"]
    _item(UG, "Underground: duct-bank manhole and handhole chambers",
          "Precast concrete manholes 7 x 7 ft, 8 ft deep, with the duct banks entering through the walls and "
          "cable racks inside; handholes 3 x 3 ft, 3 ft deep (typical).")
    for p in covers:
        x0, y0, _ = p["min"]
        x1, y1, _ = p["max"]
        if x1 - x0 > 5:                                                   # manhole
            box(x0, x1, y0, y1, -9, -.4, "concrete")
            box(x0 + .5, x1 - .5, y0 + .5, y1 - .5, -9.3, -9, "concrete")   # base slab
            rod(((x0 + x1) / 2, (y0 + y1) / 2, -.4), ((x0 + x1) / 2, (y0 + y1) / 2, 0), 1.3, "concrete", seg=16)  # chimney
        else:                                                             # handhole
            box(x0, x1, y0, y1, -3.2, -.05, "concrete")
    return len(covers)


def ground_grid(items):
    """Bare Cu mesh under the electrical, power-block and switchyard areas, rods and risers."""
    layers = ("BASE_ELECTRICAL", "BASE_SWITCHYARD", "BASE_POWER_BLOCK", "BASE_INLET_AIR")
    fps = [it["fp"] for it in items if it["layer"] in layers and it["z"][1] > .7
           and it["fp"][1] - it["fp"][0] < 1600 and it["fp"][3] - it["fp"][2] < 1200]
    sy = find("230 kV switchyard (gravel)")["fp"]
    _item(UG, "Underground: station ground grid (bare 4/0 Cu mesh, rods, risers)",
          "Bare 4/0 AWG copper at 18 in depth, exothermic joints; 40 ft mesh under the power block and electrical "
          "areas, 20 ft in the switchyard; 10 ft copper-clad rods at the perimeter; 4/0 risers to every "
          "transformer, e-house, structure and machine skid (typical, sized by the IEEE 80 study).",
          area="C")
    segs = set()

    def mark(x0, x1, y0, y1, s):
        for gx in range(int(math.floor(x0 / s)), int(math.ceil(x1 / s))):
            for gy in range(int(math.floor(y0 / s)), int(math.ceil(y1 / s))):
                a, b = gx * s, gy * s
                segs.update({((a, b), (a + s, b)), ((a, b + s), (a + s, b + s)), ((a, b), (a, b + s)),
                             ((a + s, b), (a + s, b + s))})
    for (x0, x1, y0, y1) in fps:
        if not (x0 >= sy[0] and x1 <= sy[1] and y0 >= sy[2] and y1 <= sy[3]):
            mark(max(x0 - 10, 2), min(x1 + 10, 2418), max(y0 - 10, 2), min(y1 + 10, 1918), 40)
    mark(sy[0], sy[1], sy[2], sy[3], 20)
    zg = -1.5
    runs = _merge(list(segs))
    for (axis, c), ivs in runs.items():
        for a, b in ivs:
            if axis == "x":
                rod((a, c, zg), (b, c, zg), .045, "copper", seg=5)
            else:
                rod((c, a, zg), (c, b, zg), .045, "copper", seg=5)
    # driven rods at the outer nodes (every other node on the outline), risers to equipment
    nodes = {}
    for (p, q) in segs:
        for v in (p, q):
            nodes[v] = nodes.get(v, 0) + 1
    outer = sorted(v for v, k in nodes.items() if k < 4)
    for i, (x, y) in enumerate(outer):
        if i % 2 == 0:
            rod((x, y, zg), (x, y, zg - 10), .05, "copper", seg=5)
    nris = 0
    for it in items:
        if it["layer"] not in ("BASE_ELECTRICAL", "BASE_SWITCHYARD") or it["z"][1] < 2 or it["z"][0] > 1:
            continue
        x0, x1, y0, y1 = it["fp"]
        if x1 - x0 > 400:
            continue
        for (x, y) in ((x0 - .4, y0 - .4), (x1 + .4, y1 + .4)):
            rod((x, y, zg), (x, y, .35), .05, "copper", seg=5)
            nris += 1
    return len(runs), nris


def firewater(routes):
    _item(UG, "Underground: firewater ring main (12 in ductile iron)",
          "Cement-lined ductile iron, 5 ft cover, sectionalised by post-indicator valves; hydrant and monitor "
          "laterals rise to the hydrants shown above grade (typical, NFPA 24).", area="E")
    n = 0
    for r in routes:
        if r["type"] != "firewater":
            continue
        _pipe_run([tuple(p) for p in r["points"]], -5.5, .55, "ductile", seg=12)
        for p in r["points"][1:-1]:
            box(p[0] - .9, p[0] + .9, p[1] - .9, p[1] + .9, -6.3, -4.7, "concrete")     # thrust block
        n += 1
    return n


def storm(items):
    """RCP storm sewer under each road edge, catch-basin chambers and laterals, trunk to the pond."""
    _item(UG, "Underground: storm drainage (reinforced-concrete pipe, catch basins, manholes)",
          "RCP 18-36 in under the road edges at about 0.5 % fall to the detention pond inlet headwall; catch basins "
          "with sumps and laterals; storm manholes at the junctions (typical).", area="F")
    roads = [it for it in items if it["layer"] == "SITE" and "road" in it["name"].lower()]
    n = 0
    for it in roads:
        x0, x1, y0, y1 = it["fp"]
        if (x1 - x0) >= (y1 - y0):
            ym = y0 + 1.5
            rod((x0, ym, -7.5), (x1, ym, -7.5), .9, "rcp", seg=12)
            for x in range(int(x0) + 60, int(x1) - 30, 150):
                for y in (y0 + 1.5, y1 - 1.5):
                    box(x - 1.8, x + 1.8, y - 1.5, y + 1.5, -6, -.05, "concrete")        # catch-basin chamber
                    if y != ym:
                        rod((x, y, -5), (x, ym, -7), .45, "rcp", seg=10)                  # lateral across the road
                    n += 1
        else:
            xm = x0 + 1.5
            rod((xm, y0, -7.5), (xm, y1, -7.5), .9, "rcp", seg=12)
            for y in range(int(y0) + 60, int(y1) - 30, 150):
                for x in (x0 + 1.5, x1 - 1.5):
                    box(x - 1.5, x + 1.5, y - 1.8, y + 1.8, -6, -.05, "concrete")
                    if x != xm:
                        rod((x, y, -5), (xm, y, -7), .45, "rcp", seg=10)
                    n += 1
    # storm manholes where the road drains meet
    for a in roads:
        for b in roads:
            if a is b:
                continue
            ax0, ax1, ay0, ay1 = a["fp"]
            bx0, bx1, by0, by1 = b["fp"]
            if (ax1 - ax0) >= (ay1 - ay0) and (bx1 - bx0) < (by1 - by0):
                x, y = bx0 + 1.5, ay0 + 1.5
                if ax0 <= x <= ax1 and by0 <= y <= by1:
                    rod((x, y, -9), (x, y, -.4), 2.5, "concrete", seg=16)
                    rod((x, y, -.4), (x, y, -.05), 1.3, "concrete", seg=16)
    # trunk from the west spine road drain to the pond inlet headwall (309, 1626-1640)
    _pipe_run([(371.5, 1660, -7.5), (309, 1660, -7.5), (309, 1641, -3)], -7.5, 1.4, "rcp", seg=14)
    rod((371.5, 1660, -9), (371.5, 1660, -.4), 2.5, "concrete", seg=16)
    return n


def oily_water():
    _item(UG, "Underground: oily-water drains (HDPE) to the oil-water separator",
          "Transformer containment sumps (GSU, UAT, station transformers) and the turbine-hall lube-oil area drains "
          "to the oil-water separator; separator effluent to the wastewater treatment (typical, SPCC).", area="E")
    zo, ro = -6.5, .35
    main = [(1456, 314), (1456, 1440), (1226, 1440), (1226, 1450)]
    _pipe_run([(600, 314)] + main, zo, .45, "hdpe")
    for cx, y in ((630, 325), (790, 325), (950, 325), (1051, 320), (667, 330), (827, 330), (987, 330)):
        _pipe_run([(cx, y + 6), (cx, 314)], zo, ro, "hdpe")                            # containment sump laterals
        box(cx - 1.5, cx + 1.5, y + 4.5, y + 7.5, -5, -.05, "concrete")                 # sump / valve pit
    _pipe_run([(596, 376), (1456, 376)], zo, ro, "hdpe")                              # hall drain header
    for k in range(3):                                                                 # lube-oil skid drains
        x = 668 + 160 * k
        _pipe_run([(x, 470), (x, 376)], zo, .25, "hdpe")
    _pipe_run([(1090, 470), (1090, 376)], zo, .25, "hdpe")                             # ST lube-oil / EHC area
    _pipe_run([(452, 805), (490, 805), (490, 892), (1456, 892)], zo, ro, "hdpe")       # station transformers
    _pipe_run([(1200, 1454), (745, 1454)], zo, ro, "hdpe")                            # OWS -> wastewater
    for p in ((1456, 314), (1456, 376), (1456, 892), (1456, 1440), (490, 892)):
        rod((p[0], p[1], -8), (p[0], p[1], -.4), 2, "concrete", seg=14)               # cleanout / inspection MH


def sanitary():
    _item(UG, "Underground: sanitary sewer (PVC SDR 35) and lift-station force main",
          "Gravity sewer from the buildings to a packaged duplex lift station, 3 in HDPE force main to the public "
          "sewer at the west boundary (typical).", area="F")
    zs = -6
    _pipe_run([(334, 318), (334, 650)], zs, .35, "pvc_green")
    for (x, y) in ((320, 370), (320, 515), (320, 620), (300, 318)):                   # building laterals
        _pipe_run([(x, y), (334, y)], zs + .5, .25, "pvc_green")
    for y in (370, 515, 620):
        rod((334, y, -7), (334, y, -.4), 2, "concrete", seg=14)                       # sewer manholes
    _pipe_run([(332, 664), (332, 668), (2, 668)], -4.5, .15, "hdpe")                 # force main
    lift = fuel.new_item("BASE_SERVICES", "LS-1: sanitary lift station (packaged duplex)", (326, 340, 652, 664), (0, 6),
                         tag="LS-1", area="F", basis="typical", sheet=SHEET,
                         info="Fibreglass wet well with two submersible grinder pumps, valve vault, control panel "
                              "with alarm beacon (typical).")
    rod((333, 658, -12), (333, 658, .5), 3.5, "concrete", seg=20)                    # wet well
    box(330.5, 335.5, 655.5, 660.5, .5, .7, "grating")
    box(326.5, 330, 660.5, 663.5, 0, 5.2, "panel")                                    # control panel
    rod((328.2, 662, 5.2), (328.2, 662, 6), .3, "red", seg=10)                        # alarm beacon
    lift["wiring"] = ["LV power 480 V: Cu XHHW-2, Type TC-ER in buried PVC conduit (pumps, panel)",
                      "Control 120 V: float switches, alarm to the DCS", "Grounding: bare Cu to the panel and wet well"]
    return lift


def water():
    _item(UG, "Underground: potable and service water mains (PVC C900)",
          "Potable water from the water treatment building to the buildings and safety showers; service water to "
          "the power block, HRSG area and hose stations (typical).", area="E")
    zw = -4.5
    _pipe_run([(440, 1490), (346, 1490), (346, 318)], zw, .3, "pvc_blue")             # potable main
    for (x, y) in ((320, 375), (320, 520), (320, 625), (300, 322)):
        _pipe_run([(x, y), (346, y)], zw, .18, "pvc_blue")
    _pipe_run([(560, 1445), (560, 942), (1100, 942)], zw, .35, "pvc_blue")           # service water main
    for x in (650, 810, 970):
        _pipe_run([(x, 942), (x, 880)], zw, .25, "pvc_blue")                          # to the HRSG areas
    for p in ((346, 1490), (560, 942), (346, 318)):
        box(p[0] - 1.2, p[0] + 1.2, p[1] - 1.2, p[1] + 1.2, -5, -.05, "concrete")     # valve boxes


def build(items, routes):
    nb = duct_banks(routes)
    nc = chambers()
    ng = ground_grid(items)
    nf = firewater(routes)
    ns = storm(items)
    oily_water()
    lift = sanitary()
    water()
    return dict(duct_bank_runs=nb, chambers=nc, grid_runs=ng[0], grid_risers=ng[1], firewater=nf, catch_basins=ns,
                lift=lift)
