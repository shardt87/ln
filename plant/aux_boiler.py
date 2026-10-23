"""Auxiliary boiler AB-1 at LOD 3: a gas-fired package boiler (owner, Oct 22: the boiler section, "greenfield or
brownfield ... boilers that are used for gas power as well"). It stays the combined-cycle plant's auxiliary boiler
(start-up and sealing steam, HRSG / ST warm-keeping, CCS reboiler back-up) in its drawn envelope (x 935-995,
y 1450-1540, top EL 70), and shows what a package boiler of this class carries, all typical, not engineered:
- boiler: D-type water-tube package boiler (~150,000 lb/h class) on its skid, burner and windbox at the south end,
  steam-drum heads, water column and drum-level transmitters at the north end, safety valves and the main-steam stop
  valve (motor-operated) on the roof, roof platform with handrail and ladder;
- combustion air: FD fan with its motor and vertical inlet silencer beside the windbox (480 V, VFD in the e-house);
- fuel: natural-gas train on a skid at the burner front: manual isolation, two safety shut-off valves with the vent
  valve between (double block and bleed), regulator, vent line to EL 22, gas detector; Class I Div 2 around it;
- back end: economizer, breeching and a 70 ft stack with a CEMS / test-port platform and caged ladder;
- feedwater: deaerator on legs with its vent, two feedwater pumps, chemical feed, blowdown tank;
- electrical: AB-MCC e-house (480 V MCC, FD-fan VFD, BMS UPS) fed underground; a ladder tray at EL 17.5 from the
  e-house to the burner-management panel; VFD cable to the FD fan motor, flame-scanner and igniter cable from the
  burner front, ARMOR-X MC-HL exposed on strut to the gas train (hazardous location), drum-level instrument cable,
  conduit stub-ups at the pump motors; LED area lights; equipment ID signs.
Runs late (after the utilities pass); the steam line ties into the aux-steam route at (995, 1495, EL 12)."""
import math

import fuel
from fuel import box, rod, find, on


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def rail(pts, z, c="rail"):
    """Handrail (top and knee rail) with posts along an open polyline at deck level z."""
    for a, b in zip(pts, pts[1:]):
        for h in (1.75, 3.5):
            rod((a[0], a[1], z + h), (b[0], b[1], z + h), .05, c, seg=6)
        L = math.dist(a, b)
        for k in range(int(L // 5) + 1):
            t = k * 5 / max(L, .1)
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            rod((p[0], p[1], z), (p[0], p[1], z + 3.5), .05, c, seg=6)


def ladder(x, y, z0, z1, along="x", cage=False):
    d = (.75, 0) if along == "x" else (0, .75)
    for s in (-1, 1):
        rod((x + s * d[0], y + s * d[1], z0), (x + s * d[0], y + s * d[1], z1), .05, "rail", seg=6)
    z = z0 + 1
    while z < z1:
        rod((x - d[0], y - d[1], z), (x + d[0], y + d[1], z), .035, "rail", seg=4)
        z += 1
    if cage:
        z = z0 + 8
        while z < z1:
            for k in range(7):
                a = math.pi * k / 6
                rod((x + d[0] * math.cos(a) * 1.6, y + d[1] * math.cos(a) * 1.6 + (1.1 * math.sin(a) if along == "x" else 0),
                     z), (x + d[0] * math.cos(a) * 1.6, y + d[1] * math.cos(a) * 1.6 + (1.1 * math.sin(a) if along == "x" else 0),
                          z + .12), .03, "rail", seg=4)
            z += 4


def tray(pts, z, w, cables, step=2.0):
    """Ladder tray along an orthogonal polyline at EL z with its cables."""
    for a, b in zip(pts, pts[1:]):
        alongx = a[1] == b[1]
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for s in (-1, 1):
            if alongx:
                box(x0 - w / 2, x1 + w / 2, a[1] + s * w / 2 - .06, a[1] + s * w / 2 + .06, z - .3, z + .1, "pipe")
            else:
                box(a[0] + s * w / 2 - .06, a[0] + s * w / 2 + .06, y0 - w / 2, y1 + w / 2, z - .3, z + .1, "pipe")
        L = (x1 - x0) + (y1 - y0)
        for k in range(int(L / step) + 1):
            t = k * step / max(L, .1)
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if alongx:
                box(px - .05, px + .05, a[1] - w / 2, a[1] + w / 2, z - .26, z - .2, "pipe")
            else:
                box(a[0] - w / 2, a[0] + w / 2, py - .05, py + .05, z - .26, z - .2, "pipe")
        for j, (c, r) in enumerate(cables):
            off = -w / 2 + .18 + j * (w - .36) / max(1, len(cables) - 1)
            pa = (a[0], a[1] + off) if alongx else (a[0] + off, a[1])
            pb = (b[0], b[1] + off) if alongx else (b[0] + off, b[1])
            rod((pa[0], pa[1], z - .2 + r), (pb[0], pb[1], z - .2 + r), r, c, seg=6)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


# Oct 23 (owner): AB-1 moves to the west edge of the modular yard, beside the plant pipe corridor, so Boiler Row can be a
# complete utility unit. It is drawn at its old place and turned 90 deg anticlockwise into x 1534-1624, y 1300-1360
# (burner front east, steam outlet north to the aux-steam line up the corridor, gas in from the gas yard).
def _mv(x, y):
    return 3074.0 - y, x + 365.0


def _relocate(it, p0, d0):
    for p in fuel.G["parts"][p0:]:
        if "min" in p:
            (ax, ay), (bx, by) = _mv(p["min"][0], p["min"][1]), _mv(p["max"][0], p["max"][1])
            p["min"][:2] = [round(min(ax, bx), 2), round(min(ay, by), 2)]
            p["max"][:2] = [round(max(ax, bx), 2), round(max(ay, by), 2)]
        elif "a" in p:
            for k in ("a", "b"):
                p[k][:2] = [round(v, 2) for v in _mv(p[k][0], p[k][1])]
    for d in fuel.G.get("decals", [])[d0:]:
        d["c"][:2] = [round(v, 2) for v in _mv(d["c"][0], d["c"][1])]
        for k in ("n", "up"):
            if k in d:
                d[k] = [-d[k][1], d[k][0]] + list(d[k][2:])
    it["fp"] = [1534.0, 1624.0, 1300.0, 1360.0]
    it["info"] += " Moved Oct 23 to the west edge of the modular yard (shared start-up steam for the whole campus)."


def build():
    p0, d0 = len(fuel.G["parts"]), len(fuel.G.get("decals", []))
    n = _build()
    _relocate(find("Auxiliary boiler"), p0, d0)
    return n


def _build():
    it = find("Auxiliary boiler")
    on(it)
    fuel.D = True
    n = 0
    box(936, 994, 1451, 1539, 0, .6, "concrete")                                       # foundation pad

    # ---- boiler: skid, casing, windbox and burner front (south), drum heads and water column (north)
    X0, X1, Y0, Y1 = 950.0, 964.0, 1472.0, 1514.0
    XC = (X0 + X1) / 2
    box(X0 - .5, X1 + .5, Y0 - 6.5, Y1 + .5, .6, 2.0, "steel_dark")                   # skid base
    box(X0, X1, Y0, Y1, 2.0, 16.0, "hrsg_b")                                           # casing
    for y in range(int(Y0) + 4, int(Y1), 6):                                           # casing stiffeners
        for x in (X0 - .12, X1):
            box(x, x + .12, y - .15, y + .15, 2.0, 16.0, "steel")
    box(X0, X1, Y0 - 6, Y0, 2.0, 15.0, "machine")                                     # windbox
    rod((XC, Y0 - 6, 8.5), (XC, Y0 - 8, 8.5), 2.6, "machine", seg=24)                 # burner register / throat
    rod((XC, Y0 - 8, 8.5), (XC, Y0 - 9.2, 8.5), 1.1, "steel", seg=16)                 # gas gun and igniter
    rod((XC + 1.4, Y0 - 8, 10.3), (XC + 1.4, Y0 - 9.6, 10.3), .25, "steel", seg=8)    # igniter
    scanners = []
    for sx in (-1.9, 1.9):                                                             # two UV / IR flame scanners
        p0 = (XC + sx, Y0 - 8, 11.4)
        rod(p0, (XC + sx, Y0 - 9.4, 11.9), .3, "steel_dark", seg=10)
        scanners.append((XC + sx, Y0 - 9.4, 11.9))
    for y_ in (Y0 + .8, Y1 - .8):                                                      # drum heads with manways
        pass
    rod((XC, Y1, 13.0), (XC, Y1 + 1.2, 13.0), 2.4, "hrsg_b", seg=24)                   # steam drum head
    rod((XC, Y1 + 1.2, 13.0), (XC, Y1 + 1.5, 13.0), 1.0, "steel", seg=16)              # manway cover
    rod((XC, Y1, 4.5), (XC, Y1 + .9, 4.5), 1.6, "hrsg_b", seg=20)                      # mud drum head
    rod((X1 - 2.0, Y1 + .9, 10.5), (X1 - 2.0, Y1 + .9, 15.5), .45, "steel", seg=10)    # water column
    for zt in (11.3, 14.2):                                                            # drum-level transmitters
        box(X1 - 1.2, X1 - .4, Y1 + .6, Y1 + 1.4, zt - .4, zt + .4, "panel")
    box(X0 + 1, X0 + 3, Y1, Y1 + .5, 13.5, 15.5, "panel")                             # instrument JB on the back
    rod((X1 - .8, Y1 + 1.0, 14.2), (X1 - .8, Y1 + 1.0, 16.6), .06, "cable_inst", seg=4)
    rod((X1 - .8, Y1 + 1.0, 11.3), (X1 - .8, Y1 + 1.0, 14.2), .06, "cable_inst", seg=4)
    poly([(X1 - .8, Y1 + 1.0, 16.6), (X0 + 2, Y1 + 1.0, 16.6), (X0 + 2, Y1 + .4, 15.5)], .06, "cable_inst", seg=4)
    n += 30

    # ---- roof: platform with handrail, safety valves with vent stacks, main-steam stop valve (MOV), ladder
    box(X0, X1, Y0 + 2, Y1 - 2, 16.0, 16.25, "grating")
    rail([(X0, Y0 + 2), (X0, Y1 - 2), (X1, Y1 - 2)], 16.25)
    rail([(X1, Y0 + 2), (X0 + 1.6, Y0 + 2)], 16.25)                                   # leaves the ladder opening
    ladder(X1 + .9, Y0 + 3.5, .6, 19.8, along="y")
    for (x_, y_) in ((XC - 2.5, Y1 - 8), (XC + 2.5, Y1 - 8)):
        rod((x_, y_, 16.25), (x_, y_, 18.8), .55, "red", seg=10)                       # safety valve
        rod((x_, y_, 18.8), (x_, y_, 26.0), .45, "pipe", seg=10)                       # vent stack
        rod((x_, y_, 23.0), (x_, y_, 25.0), .9, "steel", seg=12)                       # vent silencer
    rod((XC, Y1 - 16, 16.25), (XC, Y1 - 16, 19.0), .75, "alu", seg=12)                 # steam outlet nozzle
    box(XC - 1.1, XC + 1.1, Y1 - 17.1, Y1 - 14.9, 19.0, 20.6, "steel")                 # stop valve body
    box(XC - .7, XC + .7, Y1 - 16.7, Y1 - 15.3, 20.6, 23.0, "motor")                  # MOV actuator
    # main steam to the aux-steam route (EL 12 at x 995, y 1495), insulated, on two posts
    ys = 1495.0
    poly([(XC, Y1 - 16, 19.8), (XC, ys, 19.8), (990.0, ys, 19.8), (990.0, ys, 12.0), (993.4, ys, 12.0)], .75, "alu",
         seg=12)
    for xp in (970.0, 982.0):
        rod((xp, ys, .6), (xp, ys, 19.0), .3, "steel", seg=8)
        box(xp - .9, xp + .9, ys - .3, ys + .3, 18.7, 19.05, "steel")
    n += 25

    # ---- combustion air: FD fan, motor, inlet silencer, discharge duct into the windbox side
    FX, FY = 943.5, 1467.0
    box(939.5, 947.5, 1458.0, 1472.5, .6, 1.4, "concrete")                             # fan plinth
    rod((FX, FY - 2.2, 5.0), (FX, FY + 2.2, 5.0), 3.6, "fan", seg=24)                  # scroll housing
    rod((FX, FY - 2.2, 5.0), (FX, FY - 3.0, 5.0), .6, "steel", seg=10)                 # shaft / coupling guard
    rod((FX, FY - 3.0, 5.0), (FX, FY - 7.4, 5.0), 1.5, "motor", seg=16)                # 200 hp motor
    box(FX - 1.2, FX + 1.2, FY - 7.4, FY - 3.0, 1.4, 3.6, "steel_dark")               # motor base
    box(FX + 1.3, FX + 2.0, FY - 6.0, FY - 4.6, 4.4, 5.6, "panel")                     # motor terminal box
    rod((FX, FY + 2.5, 8.6), (FX, FY + 2.5, 20.0), 1.9, "duct", seg=18)                # inlet silencer
    rod((FX, FY + 2.5, 20.0), (FX, FY + 2.5, 20.6), 2.3, "duct", r2=1.9, seg=18)      # rain hood
    box(FX + 2.6, X0, FY - 1.6, FY + 1.6, 6.0, 11.0, "duct")                          # discharge duct to windbox
    box(FX + 3.4, FX + 4.4, FY - 2.0, FY + 2.0, 11.0, 12.2, "motor")                  # damper actuator
    n += 12

    # ---- natural-gas train at the burner front (double block and bleed), Class I Div 2
    GY = 1461.5
    box(967.0, 990.0, GY - 3.5, GY + 3.5, .6, 1.2, "steel_dark")                      # skid
    poly([(992.0, GY, 0.0), (992.0, GY, 4.0), (968.0, GY, 4.0), (966.0, GY, 4.0), (966.0, GY, 9.0),
          (XC + 3.2, GY, 9.0), (XC + 3.2, Y0 - 9.0, 9.0), (XC + 1.0, Y0 - 9.0, 9.0)], .4, "fuelgas", seg=10)
    for xv, kind in ((986.5, "man"), (982.0, "reg"), (977.5, "ssov"), (974.0, "vent"), (970.5, "ssov"), (967.8, "man")):
        if kind == "man":
            rod((xv - .5, GY, 4.0), (xv + .5, GY, 4.0), .65, "steel", seg=10)
            rod((xv, GY, 4.6), (xv, GY, 5.6), .08, "steel", seg=6)
            rod((xv, GY - .6, 5.6), (xv, GY + .6, 5.6), .05, "red", seg=6)          # handwheel / lever
        elif kind == "reg":
            rod((xv - .8, GY, 4.0), (xv + .8, GY, 4.0), .9, "steel", seg=12)
            rod((xv, GY, 4.9), (xv, GY, 6.2), 1.0, "amber", r2=.5, seg=14)          # regulator diaphragm
        elif kind == "ssov":
            rod((xv - .6, GY, 4.0), (xv + .6, GY, 4.0), .75, "steel", seg=12)
            box(xv - .55, xv + .55, GY - .55, GY + .55, 4.8, 6.6, "red")             # safety shut-off actuator
        else:
            rod((xv, GY, 4.0), (xv, GY, 5.2), .3, "fuelgas", seg=8)
            box(xv - .4, xv + .4, GY - .4, GY + .4, 5.2, 6.4, "amber")                # vent valve
            poly([(xv, GY, 6.4), (xv, GY + 2.6, 6.4), (xv, GY + 2.6, 22.0)], .2, "fuelgas", seg=8)   # vent line up
            rod((xv, GY + 2.6, 22.0), (xv, GY + 2.6, 22.6), .35, "fuelgas", r2=.2, seg=8)
    for xp in (970.0, 980.0, 988.0):                                                   # pipe stands
        rod((xp, GY, 1.2), (xp, GY, 3.6), .15, "steel", seg=6)
    box(988.6, 990.0, GY + 2.4, GY + 3.2, 1.2, 5.2, "panel")                          # gas-train junction box
    box(966.6, 967.6, GY + 3.0, GY + 3.6, 6.5, 7.3, "amber")                          # gas detector
    n += 30

    # ---- back end: boiler outlet box, economizer, breeching, stack with platform and caged ladder
    box(X0 + 2, X1 - 2, Y1 + 1.5, Y1 + 4.0, 10.0, 16.0, "hrsg_b")                    # outlet box
    box(X0 + 1, X1 - 1, Y1 + 4.0, Y1 + 14.0, 6.0, 24.0, "hrsg_b")                    # economizer
    for zh in (7.5, 22.5):                                                             # economizer headers
        rod((X0 + .4, Y1 + 9, zh), (X1 - .4, Y1 + 9, zh), .45, "pipe", seg=8)
    box(XC - 3, XC + 3, Y1 + 9, Y1 + 16.5, 24.0, 30.0, "duct")                        # breeching to the stack
    SX, SY, SR = XC, Y1 + 19.0, 3.2
    rod((SX, SY, .6), (SX, SY, 70.0), SR, "stack", seg=28)
    rod((SX, SY, 69.4), (SX, SY, 70.0), SR + .25, "steel", seg=28)                   # top ring
    rod((SX, SY, 49.7), (SX, SY, 50.0), SR + 3.0, "grating", seg=28)                  # CEMS / test-port platform
    for k in range(10):
        a = 2 * math.pi * k / 10
        rod((SX + (SR + 2.9) * math.cos(a), SY + (SR + 2.9) * math.sin(a), 50.0),
            (SX + (SR + 2.9) * math.cos(a), SY + (SR + 2.9) * math.sin(a), 53.5), .05, "rail", seg=6)
    for h in (51.75, 53.5):
        rod((SX, SY, h), (SX, SY, h + .08), SR + 2.95, "rail", seg=28)
    for a in (0, 90):                                                                  # test ports
        rod((SX + SR * math.cos(math.radians(a)), SY + SR * math.sin(math.radians(a)), 52.0),
            (SX + (SR + .8) * math.cos(math.radians(a)), SY + (SR + .8) * math.sin(math.radians(a)), 52.0), .35, "steel")
    ladder(SX - SR - .9, SY, 30.0, 53.5, along="y", cage=True)
    box(SX - SR - 2.2, SX - SR - .3, SY - 1.2, SY + 1.2, 29.7, 30.0, "grating")       # rest landing over the breeching
    n += 30

    # ---- feedwater: deaerator on legs, two feedwater pumps, chemical feed, blowdown tank
    DY = 1525.0
    rod((972.0, DY, 14.0), (990.0, DY, 14.0), 3.4, "tank", seg=24)                    # deaerator storage
    rod((986.0, DY, 17.4), (986.0, DY, 21.5), 1.4, "tank", seg=16)                    # deaerating head
    rod((986.0, DY, 21.5), (986.0, DY, 24.0), .25, "pipe", seg=8)                     # vent
    for xl in (974.0, 988.0):
        for s in (-1.8, 1.8):
            rod((xl, DY + s, .6), (xl, DY + s, 11.2), .3, "steel", seg=6)
    box(972.0, 990.0, 1506.0, 1517.0, .6, 1.2, "concrete")                            # feedwater pump plinth
    for yp in (1509.0, 1514.0):
        rod((976.0, yp, 2.6), (980.5, yp, 2.6), 1.15, "pump", seg=14)
        rod((980.5, yp, 2.6), (985.5, yp, 2.6), 1.05, "motor", seg=14)
        box(983.0, 984.2, yp + 1.0, yp + 1.6, 3.0, 4.0, "panel")                      # motor terminal box
        rod((983.6, yp + 1.3, 0.0), (983.6, yp + 1.3, 3.0), .12, "alu", seg=8)       # conduit stub-up
        poly([(976.0, yp, 2.6), (974.0, yp, 2.6), (974.0, DY - 2.4, 2.6), (974.0, DY - 2.4, 11.5)], .3, "pipe", seg=8)
    poly([(976.0, 1511.5, 4.5), (968.0, 1511.5, 4.5), (968.0, Y1 + 9, 4.5), (X1 - 1, Y1 + 9, 7.5)], .3, "pipe", seg=8)
    box(968.0, 978.0, 1530.0, 1537.0, .6, 1.2, "concrete")                            # chemical feed skid
    for xt in (970.5, 975.5):
        rod((xt, 1533.5, 1.2), (xt, 1533.5, 6.5), 1.7, "tank", seg=14)
    box(976.5, 977.8, 1530.4, 1532.0, 1.2, 5.0, "panel")
    BX, BY = 942.0, 1524.0
    rod((BX, BY, .6), (BX, BY, 11.0), 2.6, "tank", seg=18)                            # blowdown tank
    rod((BX, BY, 11.0), (BX, BY, 16.5), .35, "pipe", seg=8)
    poly([(X0 - .5, 1510.0, 2.5), (BX, 1510.0, 2.5), (BX, BY - 2.7, 2.5)], .25, "pipe", seg=8)
    n += 30

    # ---- electrical: AB-MCC e-house, tray to the burner-management panel, burner / gas-train / fan cables
    EX0, EX1, EY0, EY1 = 936.5, 947.5, 1482.0, 1499.0
    box(EX0, EX1, EY0, EY1, .6, 12.0, "ehouse")
    box(EX0 - .3, EX1 + .3, EY0 - .3, EY1 + .3, 12.0, 12.4, "roof")
    box(EX1, EX1 + .1, EY0 + 2.0, EY0 + 5.5, .6, 8.0, "door")
    box(EX0 + 2.0, EX0 + 6.0, EY1, EY1 + 2.2, .6, 4.0, "machine")                     # HVAC unit
    for xc_ in (EX0 + 2.5, EX0 + 5.5, EX0 + 8.5):                                      # underground feeders rising in
        rod((xc_, EY0 + 8.5, 0.0), (xc_, EY0 + 8.5, .6), .25, "alu", seg=8)
    decal((EX1 + .12, EY0 + 11.0, 9.2), (1, 0, 0), 7.5, 1.6,
          [("AB-MCC  ·  480 V", .42, True, "#111111"), ("FD FAN VFD  ·  BMS UPS", .3, False, "#333333")], bg="#ffffff")
    # BMS panel (burner management / combustion control) east of the windbox, HMI to the east
    PX0, PX1, PY0, PY1 = 966.6, 969.0, 1473.0, 1478.0
    box(PX0, PX1, PY0, PY1, .6, 8.2, "cabinet")
    box(PX1, PX1 + .06, PY0 + .4, PY1 - .4, 1.2, 7.8, "door")
    box(PX1 + .03, PX1 + .1, PY0 + 1.4, PY1 - 1.4, 5.4, 6.8, "hmi")
    for j, c in enumerate(("led_g", "led_a", "led_r")):
        box(PX1 + .04, PX1 + .12, PY0 + 1.5 + j * .5, PY0 + 1.8 + j * .5, 4.8, 5.1, c)
    rod((PX1 + .05, PY1 - 1.0, 4.3), (PX1 + .3, PY1 - 1.0, 4.3), .2, "red", seg=10)  # E-stop
    decal((PX1 + .14, (PY0 + PY1) / 2, 7.55), (1, 0, 0), 3.6, .55, [("AB-1  BMS", .6, True, "#111111")], bg="#ffffff")
    # ladder tray EL 17.5: down the west side from the e-house, across over the windbox to the BMS panel
    TZ = 17.5
    tray([(946.0, 1496.0), (946.0, 1469.0), (967.8, 1469.0), (967.8, 1475.5)], TZ, 1.5,
         (("cable_mc", .12), ("cable_mc", .12), ("cable_tc", .08), ("cable_inst", .07), ("cable_inst", .07),
          ("cable_fa", .06)))
    rod((946.0, 1496.0, 12.4), (946.0, 1496.0, TZ - .3), .12, "cable_mc", seg=6)       # from the e-house roof
    rod((945.6, 1496.0, 12.4), (945.6, 1496.0, TZ - .3), .12, "cable_tc", seg=6)
    for (px, py, z0) in ((946.0, 1490.0, .6), (946.0, 1478.0, .6), (967.8, 1474.0, 8.2)):
        if z0 < 1:
            rod((px, py, z0), (px, py, TZ - .3), .14, "steel", seg=6)                  # tray posts
            box(px - .5, px + .5, py - .5, py + .5, z0, z0 + .4, "concrete")
    for xp in (953.0, 961.0):                                                          # stub posts on the windbox roof
        rod((xp, 1469.0, 15.0), (xp, 1469.0, TZ - .3), .12, "steel", seg=6)
    rod((967.8, 1475.5, TZ - .3), (967.8, 1475.5, 8.2), .2, "cable_tc", seg=6)          # tray drop into the BMS panel
    # VFD output cable down to the FD-fan motor terminal box
    poly([(946.4, 1469.0, TZ - .2), (946.4, 1469.0, 13.0), (946.4, FY - 5.3, 13.0), (FX + 2.0, FY - 5.3, 13.0),
          (FX + 2.0, FY - 5.3, 5.6)], .12, "cable_mc", seg=6)
    # flame-scanner and igniter cables up the burner front to the tray
    for (sx, sy, sz) in scanners + [(XC + 1.4, Y0 - 9.6, 10.3)]:
        poly([(sx, sy, sz), (sx, sy - .3, sz), (sx, sy - .3, 16.0), (sx, 1469.0, 16.0), (sx, 1469.0, TZ - .2)], .05,
             "cable_inst", seg=4)
    # gas train: ARMOR-X MC-HL exposed on strut from the BMS panel to the gas-train junction box (Class I Div 2)
    box(969.0, 989.2, GY + 2.6, GY + 3.0, 2.6, 2.8, "steel")                          # strut
    for xs in (972.0, 980.0, 987.0):
        rod((xs, GY + 2.8, 1.2), (xs, GY + 2.8, 2.6), .08, "steel", seg=6)
    for dz in (0, .32):
        poly([(PX1, PY0 + .6, 1.4 + dz), (PX1 + .6, PY0 + .6, 1.4 + dz), (PX1 + .6, GY + 2.8, 2.95 + dz),
              (988.6, GY + 2.8, 2.95 + dz)], .12, "cable_armor", seg=8)
    for xv in (977.5, 974.0, 970.5):                                                   # MC-HL drops to the actuators
        poly([(xv, GY + 2.8, 3.1), (xv, GY + .6, 3.1), (xv, GY + .6, 5.4)], .08, "cable_armor", seg=6)
    # drum-level instrument cable from the back JB along the casing top edge to the tray
    poly([(X0 + 2, Y1 + .2, 15.5), (X0 + .3, Y1 + .2, 16.6), (X0 + .3, 1490.0, 16.6), (946.75, 1490.0, 16.6),
          (946.75, 1490.0, TZ - .2)], .07, "cable_inst", seg=4)
    # LED area lights on two poles
    for (lx, ly) in ((938.0, 1453.0), (992.0, 1537.0)):
        rod((lx, ly, .6), (lx, ly, 28.0), .25, "steel", seg=8)
        box(lx - 1.2, lx + 1.2, ly - .6, ly + .6, 27.4, 28.0, "lamp")
    n += 60

    # ---- signs and an operator at the BMS panel
    decal((X1 + .14, Y0 + 14.0, 11.5), (1, 0, 0), 12.0, 3.0,
          [("AUXILIARY BOILER  AB-1", .4, True, "#111111"), ("NATURAL GAS  ·  150,000 LB/H  ·  600 PSIG", .26, False, "#333333")],
          bg="#ffffff")
    decal((988.0, GY - 3.55, 3.2), (0, -1, 0), 4.0, 1.0, [("DANGER  ·  NATURAL GAS", .5, True, "#ffffff")], bg="#b8322a")
    fuel.D = False
    import maintenance as mt
    mt.person(971.0, 1475.5, .6, 3.14)
    return n
