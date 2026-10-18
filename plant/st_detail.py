"""Steam turbine and its generator brought to the gas turbines' level (user review: "the steam turbine looks dull ...
audit cables just like the gas"). The audit found the ST with no cable at all, no junction boxes, no lube-oil lines and
one flat grey casing, against 72 thermocouple-cable parts, junction boxes, conduits and lube lines on each GT.
As on a real HP/IP + LP reheat unit, all typical, not engineered:
- finish: LP casing and exhaust hood painted in the unit blue (gen_paint), the HP/IP casing and the main stop /
  control valve chests under quilted insulation blankets (gt_blanket), crossover and main-steam pipes in aluminium
  lagging (alu); bearing housings stay machined steel;
- lube oil: supply (amber) and drain from the ST lube-oil skid to the three bearings, on the deck east of the casing;
- instrumentation: casing-metal thermocouples on the HP/IP barrel with type KX extension rings, exhaust-hood
  temperature elements, two proximity probes on every bearing with their extension cable (blue), all to junction
  boxes on the west side of the casing;
- electro-hydraulic control: shielded servo cable from both valve actuators to the HP/IP junction box, EHC
  hydraulic tubing from the skid;
- each junction box in rigid conduit up to the EL 42 control tray that runs along x 1017 and over the generator;
- generator (STG): RTD / vibration junction box with its conduit to the same tray, space-heater MC feed.
Everything stays inside the ST / STG envelopes or on the deck beside them, clear of the trays and pedestals.
"""
import math

import fuel
from fuel import box, rod, find, on

SX, SZ, BZ = 1050.0, 31.0, 33.0           # shaft line x / EL, LP barrel axis EL
TRAY_X, TRAY_Z = 1017.0, 41.0             # control tray along x 1017 (EL 42), conduits end just under it


def poly(pts, r, color, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, color, seg=seg)


def ring(cx, y, cz, rr, r, color, n=32):
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        rod((cx + rr * math.cos(a0), y, cz + rr * math.sin(a0)), (cx + rr * math.cos(a1), y, cz + rr * math.sin(a1)),
            r, color, seg=6)


def finish(st):
    n = 0
    for p in fuel.G["parts"]:
        if p["item"] != st["id"]:
            continue
        if p["kind"] == "rod" and p["color"] == "machine":
            r = p.get("r", 0)
            ys = (p["a"][1] + p["b"][1]) / 2
            if r >= 12:                                    # LP upper barrel and its dished ends
                p["color"] = "gen_paint"
            elif r >= 7 and ys > 528:                      # HP/IP casing
                p["color"] = "gt_blanket"
            elif abs(r - 2.5) < .01:                       # valve chests
                p["color"] = "gt_blanket"
            elif abs(r - 1.8) < .01 or abs(r - 1.2) < .01:  # crossover pipes, valve-chest leads
                p["color"] = "alu"
            else:
                continue
        elif p["kind"] == "box" and p["color"] == "machine":
            p["color"] = "gen_paint"                       # LP lower hood, side exhaust hood, hood flange
        elif p["kind"] == "rod" and p["color"] == "pipe":
            p["color"] = "alu"                             # main steam to the valve chests
        else:
            continue
        n += 1
    return n


def build():
    st = find("ST: steam turbine")
    n = finish(st)
    on(st)
    fuel.D = True
    # ---- lube oil from the ST skid (x 1082-1098, y 470-505) to the three bearings, east of the casing on the deck
    for yb in (470.5, 528.2, 549.6):
        poly([(1082, 487, 22.3), (1078, 487, 22.3), (1078, yb, 22.3), (SX + 5.4, yb, 22.3), (SX + 5.4, yb, 24.6)],
             .22, "amber")                                                       # supply, amber
        poly([(1082, 490, 21.9), (1079.2, 490, 21.9), (1079.2, yb + 1.2 if yb < 549 else yb - 1.2, 21.9),
              (SX + 5.6, yb + 1.2 if yb < 549 else yb - 1.2, 21.9)], .3, "machine")   # drain
        n += 2
    # ---- junction boxes on the west side: LP north / south, HP/IP
    jbs = [(1026.6, 490.0, 29.5), (1026.6, 510.0, 29.5), (1041.0, 540.0, 31.0)]
    for (x, y, z) in jbs:
        box(x - .6, x + .6, y - 1.2, y + 1.2, z - 1.5, z + 1.5, "panel")
        poly([(x - .6, y, z), (TRAY_X + 1.6, y, z), (TRAY_X + 1.6, y, TRAY_Z)], .1, "steel")   # conduit to the tray
        n += 2
    # ---- HP/IP casing-metal thermocouples (8 per band) with KX rings, lead to the HP/IP box
    for yt in (536.5, 543.5):
        for k in range(8):
            a = 2 * math.pi * (k + .5) / 8
            ca, sa = math.cos(a), math.sin(a)
            rod((SX + 8.0 * ca, yt, SZ + 8.0 * sa), (SX + 8.8 * ca, yt, SZ + 8.8 * sa), .12, "steel", seg=6)
            rod((SX + 8.8 * ca, yt - .25, SZ + 8.8 * sa), (SX + 8.8 * ca, yt + .25, SZ + 8.8 * sa), .22, "steel", seg=8)
        ring(SX, yt + .6, SZ, 9.0, .09, "cable_tcx")
        poly([(SX - 9.0, yt + .6, SZ), (1041.6, yt + .6, SZ), (1041.6, 540.0, 31.0)], .09, "cable_tcx")
        n += 19
    # ---- exhaust-hood temperature elements on the hood top, leads down the west face to the LP boxes
    for (y, yj) in ((490, 490.0), (510, 510.0)):
        for x in (1066, 1070):
            rod((x, y, 44.4), (x, y, 45.4), .18, "steel", seg=8)
        poly([(1066, y, 45.4), (1062, y, 45.4), (1030, y, 45.4), (1030, y, 31.0), (1027.2, yj, 31.0)], .08, "cable_tcx")
        n += 3
    # ---- proximity probes on every bearing (two at 45 deg) and their extension cable to the nearest box
    for (yb, jb) in ((470.5, jbs[0]), (528.2, jbs[1]), (552.0 - 1.6, jbs[2])):
        for s in (-1, 1):
            a = math.radians(90 + 45 * s)
            px, pz = SX + 3.4 * math.cos(a), SZ + 3.4 * math.sin(a)
            rod((px, yb, pz), (SX + 4.4 * math.cos(a), yb, SZ + 4.4 * math.sin(a)), .14, "steel", seg=8)
        poly([(SX - 3.1, yb, SZ + 3.1), (SX - 6.0, yb, SZ + 3.1), (SX - 6.0, yb, 34.0)], .07, "cable_inst")
        poly([(SX - 6.0, yb, 34.0), (1031.0, yb, 34.0), (1031.0, jb[1], 34.0), (jb[0] + .6, jb[1], jb[2] + 1.0)],
             .07, "cable_inst")
        n += 4
    # ---- EHC: servo cable from both valve actuators to the HP/IP box; hydraulic tubing from the skid
    for xv in (1029, 1071):
        poly([(xv, 545, 40.6), (xv, 541.5, 40.6), (1041.6, 541.5, 40.6), (1041.6, 541.0, 32.5)], .07, "cable_inst")
        poly([(1082, 500, 23.0), (1077.5, 500, 23.0), (1077.5, 549.0, 23.0), (xv, 549.0, 23.0), (xv, 546.4, 23.0),
              (xv, 546.4, 36.5)], .1, "amber")
        n += 2
    fuel.D = False
    # ---- generator: RTD / vibration box with conduit up to the tray over the STG (y 431, EL 42), heater MC feed
    sg = find("STG:")
    on(sg)
    fuel.D = True
    box(1038.6, 1039.8, 436.8, 439.2, 27.0, 30.0, "panel")
    poly([(1038.6, 438.0, 28.5), (1036.0, 438.0, 28.5), (1036.0, 431.0, 28.5), (1036.0, 431.0, TRAY_Z)], .1, "steel")
    poly([(1039.2, 436.8, 27.2), (1039.2, 428.0, 27.2), (1039.2, 428.0, 22.0), (1043.0, 428.0, 22.0)], .08, "cable_mc")
    for y in (415.2, 454.8):                                                      # proximity probes on both bearings
        for s in (-1, 1):
            a = math.radians(90 + 45 * s)
            rod((1050 + 3.0 * math.cos(a), y, 31 + 3.0 * math.sin(a)), (1050 + 4.0 * math.cos(a), y, 31 + 4.0 * math.sin(a)),
                .14, "steel", seg=8)
    poly([(1046.5, 454.8, 34.0), (1039.2, 454.8, 34.0), (1039.2, 439.2, 34.0), (1039.2, 439.2, 30.0)], .07, "cable_inst")
    poly([(1046.5, 415.2, 34.0), (1039.2, 415.2, 34.0), (1039.2, 436.8, 34.0), (1039.2, 436.8, 30.0)], .07, "cable_inst")
    fuel.D = False
    return n + 10
