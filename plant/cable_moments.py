"""Wire-and-cable hero moments for the growth markets: green hydrogen, LNG and the gas meter house (M&R).

Each moment stages real cable work at a real point of the model, the way the turbine-hall pull and the BESS trench
pull do, with the printed jacket legends on the installed cable:
- H2 (electrolyzer hall): a 2 kV DC 1/C 1000 kcmil conductor pulled from a reel on Maxis JAX stands, over a sheave
  into the DC ladder tray of electrolyzer 5; two electricians on a scissor lift feed and dress it; legends on all
  the DC cables in the five trays;
- LNG: a visible ladder tray LNG-T1 from the LNG e-house to the send-out pumps; a reel of ARMOR-X MC-HL on an
  RR-SW45 reel roller beside the e-house paying off over a sheave into the tray, a capstan puller with tension
  monitor at the pump end, crew, drops to the pump JB; legends on the tray cables;
- M&R (gas meter house yard): an instrument technician terminating PLTC-ER instrumentation cable in an open
  explosion-proof JB at the custody-transfer meter run, a SIMpull wire wagon feeding the pull from the tray drop;
  legends on the MR-T1 tray cables.
All typical, not engineered. Cable supplier: Southwire (as requested).
"""
import math

import fuel
from fuel import box, rod, on, find

H2_DC = "2 kV DC  1/C 1000 KCMIL CU  RHW-2 / USE-2  SUN RES  UL 44"
LEG = {
    "red": H2_DC + "  (+)", "cable_tc": None,
    "cable_mc": "ARMOR-X  MC-HL  600 V  3/C 4/0 AWG CU  XHHW-2  CCW AL ARMOR  PVC  CLASS I DIV 1 & 2  UL 2225",
    "cable_inst": "INSTRUMENTATION  PLTC-ER  16 AWG  4 TSP  300 V  ICEA S-73-532",
    "cable_fa": "FIRE ALARM  FPLR  16 AWG  2/C  SHIELDED  NEC 760",
}


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, z=0.0, a=0.0, vest="hivis", hat="hardhat"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest, hat=hat)


def legends(item_ids, texts, bbox, step=6.5, top=True):
    """Factory-printed jacket legends along the horizontal cable rods of the given items inside bbox."""
    import showcase
    x0, x1, y0, y1, z0, z1 = bbox
    n = 0
    for p in [q for q in fuel.G["parts"] if q["item"] in item_ids and q["kind"] == "rod" and q["color"] in texts]:
        a, b, r = p["a"], p["b"], p["r"]
        if abs(a[2] - b[2]) > .01 or not (z0 < a[2] < z1):
            continue
        text = texts[p["color"]]
        if not text:
            continue
        along_x = abs(a[1] - b[1]) < .01
        along_y = abs(a[0] - b[0]) < .01
        if not (along_x or along_y):
            continue
        lo, hi = sorted((a[0], b[0]) if along_x else (a[1], b[1]))
        lo, hi = max(lo, x0 if along_x else y0), min(hi, x1 if along_x else y1)
        L = min(4.4, 2.4 + r * 8)
        off = (hash((round(a[0], 1), round(a[1], 1), round(a[2], 2))) % 7) / 7 * step
        s = lo + off
        while s + L < hi:
            c = (s + L / 2, a[1], a[2] + r + .006) if along_x else (a[0], s + L / 2, a[2] + r + .006)
            up = (0, 1, 0) if along_x else (-1, 0, 0)
            for (t, br) in ((showcase.BRAND + "  " + text, 1), (text, 0)):
                decal(c, (0, 0, 1), L, r * .75, [(t, .8, 1, "#f2f2ee", br)], bg=None, up=up, generic_only=not br)
            n += 1
            s += step
    return n


def scissor_lift(x0, x1, y0, y1, zf, zp, c="crane"):
    box(x0, x1, y0, y1, zf, zf + 1.2, c)
    n = 4
    for k in range(n):
        za, zb = zf + 1.2 + k * (zp - zf - 1.2) / n, zf + 1.2 + (k + 1) * (zp - zf - 1.2) / n
        for y in (y0 + .3, y1 - .3):
            rod((x0 + .4, y, za), (x1 - .4, y, zb), .09, c, seg=6)
            rod((x1 - .4, y, za), (x0 + .4, y, zb), .09, c, seg=6)
    box(x0 - .3, x1 + .3, y0 - .2, y1 + .2, zp - .3, zp, "grating")
    for (a0, a1, b0, b1) in ((x0 - .3, x1 + .3, y0 - .2, y0 - .1), (x0 - .3, x1 + .3, y1 + .1, y1 + .2),
                             (x0 - .3, x0 - .2, y0 - .2, y1 + .2), (x1 + .2, x1 + .3, y0 - .2, y1 + .2)):
        box(a0, a1, b0, b1, zp + 3.3, zp + 3.45, c)
    for (px, py) in ((x0 - .25, y0 - .15), (x1 + .25, y0 - .15), (x0 - .25, y1 + .15), (x1 + .25, y1 + .15)):
        rod((px, py, zp), (px, py, zp + 3.45), .05, c, seg=4)


def sheave(x, y, z, axis="y", r=.9):
    d = (0, .25, 0) if axis == "y" else (.25, 0, 0)
    rod((x - d[0], y - d[1], z), (x + d[0], y + d[1], z), r, "crane", seg=18)
    rod((x, y, z + r), (x, y, z + r + 1.0), .06, "steel", seg=6)


# ---------------------------------------------------------------------------------------------------------
def hydrogen():
    from maintenance import bez, poly
    import showcase
    it = fuel.new_item("OPT_H2", "Cable pull: 2 kV DC conductors into the electrolyzer DC tray (green hydrogen)",
                       (2100, 2124, 1477.8, 1489), (0, 16), basis="typical", register=False, area="K",
                       sheet="typical (cable installation)",
                       info="2 kV DC 1/C 1000 kcmil Cu (RHW-2 / USE-2) pulled from a reel on Maxis JAX stands over a "
                            "sheave into the DC ladder tray of electrolyzer 5, eight conductors per rectifier (4+, 4-); "
                            "electricians on a scissor lift dress the tray. Cable supplier: Southwire (as requested).")
    on(it)
    xr, yr, D, W, zf = 2117.5, 1481.0, 6.0, 3.0, .55
    showcase.jack_reel(xr, yr, D, W, "cable_tc", "2 kV DC  1/C 1000 KCMIL  RHW-2", 1500, z=zf)
    top = (xr - D * .3, yr, zf + .5 + D * .85)
    sx, sy, sz = 2107.0, 1481.0, 12.8
    sheave(sx, sy, sz, axis="y", r=.7)
    poly(bez(top, ((top[0] + sx) / 2, sy, sz + 2.2), (sx + .5, sy, sz + .6), 12), .17, "cable_tc", seg=10)
    poly(bez((sx - .4, sy, sz + .65), (sx - .9, sy, sz + 1.2), (2105.6, 1481.0, 13.95), 5), .17, "cable_tc", seg=10)
    rod((2105.6, 1481.0, 13.95), (2105.6, 1469.0, 13.95), .17, "cable_tc", seg=10)        # laid in the tray
    rod((2105.6, 1469.0, 13.95), (2105.6, 1468.2, 12.0), .05, "rope", seg=6)         # pulling grip and rope
    scissor_lift(2108.4, 2112.2, 1478.4, 1481.4, zf, 9.4)
    person(2109.4, 1479.4, 9.4, 3.14, vest="hivis_o")                                   # feeding at the sheave
    person(2111.2, 1480.4, 9.4, 3.6)
    person(xr + 3.6, yr + 3.4, zf, 3.6)                                                 # reel tender
    person(2103.0, 1486.5, zf, 4.7, hat="sign")                                         # supervisor with radio
    box(2120.6, 2123.0, 1486.4, 1487.6, zf, zf + .9, "sp_yellow")                        # gang box
    # printed legends on the DC conductors in all five trays (red + / black -)
    ids = {i["id"] for i in fuel.G["items"] if i["name"].startswith("Rectifier ")}
    texts = {"cable_tc": H2_DC}
    return legends(ids, texts, (2010, 2170, 1468.5, 1493.5, 13.5, 14.2), step=5.5)


def lng(S):
    from maintenance import bez, poly
    import gas_lod3 as G3
    import simpull
    it = fuel.new_item("OPT_LNG", "LNG: cable tray LNG-T1 at the e-house, MC-HL on strut to the send-out pumps, with the ARMOR-X pull",
                       (1985, 2075, 1790, 1895), (0, 16), basis="typical", register=False, area="K",
                       sheet="typical (cable installation)",
                       info="ARMOR-X MC-HL (Class I Div 1 & 2) power, TC-ER control, PLTC-ER instrumentation and FPLR "
                            "fire-alarm cable in a short ladder tray along the LNG 17 e-house, then MC-HL exposed on "
                            "strut with the control cables in rigid conduit to the send-out pumps; a reel of "
                            "ARMOR-X MC-HL on an RR-SW45 reel roller pays off over a sheave into the tray, a capstan "
                            "puller with tension monitor at the pump end. Cable supplier: Southwire (as requested).")
    on(it)
    fuel.D = True
    z = G3.tray(S, [(1991.0, 1857.0), (2015.0, 1857.0)], 9.0, name="LNG", tag="LNG-T1", style="tray")
    if z:                                                                         # beyond the e-house: MC-HL on strut
        G3.tray(S, [(2015.0, 1857.0), (2015.0, 1801.0), (2027.0, 1801.0)], z, w=1.0, name="LNG", tag="LNG-C1",
                cables=(("cable_inst", .1), ("cable_fa", .08), ("cable_mc", .19), ("cable_mc", .19)))
    fuel.D = False
    if not z:
        return 0
    for s in (-.6, .6):                                                             # riser out of the e-house wall
        box(1994.0 + s - .06, 1994.0 + s + .06, 1857.0 - .06, 1857.0 + .06, 6.0, z, "pipe")
    G3.jb_stand(S, 2031.5, 1798.6, "JB-LNG-13")
    if G3.JBS:
        jx, jy = G3.JBS[-1]
        if G3.tray(S, [(2027.0, 1801.0), (jx, 1801.0), (jx, jy - .35)], z, w=.6,
                   cables=(("cable_mc", .14), ("cable_inst", .1)), stand=12, name="LNG spur"):
            G3.drop(S, jx, jy - .35, z, 5.6)
    # the pull: ARMOR-X MC-HL on a reel roller north of the e-house, over a sheave into the tray
    xr, yr = 2004.0, 1878.0
    if S.free(xr - 3.2, xr + 3.2, yr - 4.2, yr + 6.8, .7, 9, m=.2):
        simpull.reel_roller(xr, yr, 45, 7.0, 4.4, "cable_mc", "ARMOR-X MC-HL  600 V  3/C 4/0", steel=True)
        S.add([xr - 3.2, yr - 4.2, 0, xr + 3.2, yr + 6.8, 9])
        zc = .85 + math.sqrt((3.5 + .32) ** 2 - 1.35 ** 2)
        top = (xr, yr - 3.5 * .5, zc + 3.5 * .85)
        sx, sy, sz = 2004.0, 1858.4, z + .8
        sheave(sx, sy, sz, axis="x", r=.8)
        rod((sx, sy, sz + 1.8), (sx, 1857.0, z + .15), .05, "steel", seg=4)
        poly(bez(top, (xr, (yr + sy) / 2, sz + 3.0), (sx, sy + .7, sz + .4), 14), .19, "cable_mc", seg=10)
        poly(bez((sx, sy - .6, sz + .3), (sx, sy - 1.0, sz + .1), (sx, 1857.2, z - .02), 4), .19, "cable_mc", seg=10)
        rod((sx, 1857.2, z - .02), (2014.6, 1857.2, z - .02), .19, "cable_mc", seg=10)   # being pulled along the tray
        rod((2014.6, 1857.2, z - .02), (2014.6, 1801.6, z + .5), .05, "rope", seg=6)
        rod((2014.6, 1801.6, z + .5), (2022.0, 1801.6, z + .5), .05, "rope", seg=6)
        rod((2022.0, 1801.6, z + .5), (2022.0, 1806.0, 1.6), .05, "rope", seg=6)
        # capstan puller at the pump end
        if S.free(2019, 2026, 1805, 1811, .7, 4, m=.2):
            box(2019, 2025, 1806, 1810, 0, 1.2, "sw_red")
            rod((2022, 1806.4, 1.2), (2022, 1806.4, 2.9), .55, "steel", seg=14)
            box(2023.5, 2025, 1808, 1810, 1.2, 3.4, "sw_red")
            simpull.tension_monitor(2018.0, 1808.5, 0)
            simpull.triggers_box(2017.0, 1810.0, 0)
            person(2026.5, 1808.0, 0, 3.14, vest="hivis_o")
            S.add([2016, 1805, 0, 2027, 1811, 4])
        person(xr + 4.0, yr - 1.0, 0, 3.6)                                              # reel roller operator
        person(xr - 4.5, yr - 6.0, 0, 1.2)                                              # watching the sheave
        person(2009.0, 1852.0, 0, 0.0, hat="sign")                                      # supervisor
    texts = {k: v for k, v in LEG.items() if k in ("cable_mc", "cable_inst", "cable_fa")}
    texts["cable_tc"] = "TYPE TC-ER  600 V  12/C 14 AWG CU  XHHW-2  SUN RES  UL 1277"
    return legends({it["id"]}, texts, (1985, 2075, 1790, 1895, 8, 14))


def mr(S):
    from maintenance import bez, poly
    import simpull
    pts = [(p, p["min"]) for p in fuel.G["parts"] if p["kind"] == "box" and p["color"] == "machine" and
           1600 < p["min"][0] < 1800 and 1700 < p["min"][1] < 1900 and abs(p["min"][2] - 3.6) < .01]
    if not pts:
        return 0
    p, mn = min(pts, key=lambda t: abs(t[1][0] - 1646) + abs(t[1][1] - 1793))
    jx, jy = mn[0] + 1.0, mn[1] + .55                                                  # JB stand post line
    it = fuel.new_item("BASE_UTILITIES", "Cable termination: instrumentation cable into the meter-run JB (M&R)",
                       (jx - 8, jx + 8, jy - 9, jy + 3), (0, 8), basis="typical", register=False, area="D",
                       sheet="typical (cable installation)",
                       info="Instrument technician terminating PLTC-ER instrumentation and ARMOR-X MC-HL into an "
                            "explosion-proof JB through sealed glands at the custody-transfer meter run; SIMpull wire "
                            "wagon at the tray drop. Cable supplier: Southwire (as requested).")
    on(it)
    # open JB cover hinged down, terminal rail and the fanned conductors inside
    box(jx - 1.0, jx + 1.0, jy - .58 - .1, jy - .58, 3.0, 3.6, "machine")
    box(jx - .8, jx + .8, jy - .56, jy - .52, 4.1, 4.3, "copper")
    for k in range(8):
        c = ("red", "cable", "pvc_blue", "cable_inst", "red", "cable", "pvc_blue", "binder_w")[k]
        rod((jx - .7 + k * .2, jy - .5, 3.75), (jx - .7 + k * .2, jy - .5, 4.12), .03, c, seg=6)
    box(jx - 2.6, jx - 1.6, jy - 1.8, jy - 1.2, 0, .6, "sp_black")                     # tool bag
    person(jx + .2, jy - 1.9, 0, 1.57, vest="hivis_o")                                 # technician at the JB
    # SIMpull wire wagon with instrumentation cable, feeding up to the tray drop
    wx, wy = jx + 5.0, jy - 5.0
    if S.free(wx - 2, wx + 2, wy - 2, wy + 2, .7, 5, m=.2):
        simpull.wire_wagon(wx, wy)
        poly(bez((wx + .5, wy + .65, 3.65), (jx + 3.0, jy - 1.5, 5.5), (jx + .4, jy - .4, 6.3), 10), .1, "cable_inst", seg=8)
        person(wx + 2.2, wy - .5, 0, 3.4)
    ids = {i["id"] for i in fuel.G["items"] if i["name"].startswith("Pipeline M&R station: conduit racks")}
    texts = {k: v for k, v in LEG.items() if k in ("cable_mc", "cable_inst", "cable_fa")}
    texts["cable_tc"] = "TYPE TC-ER  600 V  12/C 14 AWG CU  XHHW-2  SUN RES  UL 1277"
    n = legends(ids, texts, (1560, 1800, 1690, 1900, 8, 14))
    ids = {i["id"] for i in fuel.G["items"] if i["name"].startswith("Gas yard: conduit racks")}
    return n + legends(ids, texts, (1560, 1940, 1430, 1640, 8, 14))


def build():
    import gas_lod3 as G3
    S = G3.Space()
    n = hydrogen()
    n += lng(S)
    n += mr(S)
    return n
