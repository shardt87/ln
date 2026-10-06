"""Cable supply and installation details (Southwire, the requested cable supplier). Typical selection, not engineered; product families as named in the cable schedule (trays.py,
wiring.py); exact constructions and part numbers to be confirmed with the supplier.

- decals: flat printed panels (placards, reel-flange stencils, truck livery) kept in G["decals"], drawn by the
  viewer (canvas texture) and Blender (image texture). Lines flagged "brand" are dropped from the generic build
  (build_viewer.py --generic) so the plant model also exists unbranded.
- branded cable reels, the SIMpull truck (flatbed with SIMpull Reels on SIMpull payoffs) and a reel yard at the
  drawn "Cable reel yard / outage laydown" pad.
"""
import math

import fuel
from fuel import box, rod

BRAND = "SOUTHWIRE"
RED = "#d2232a"
INK = "#1d1f21"


# ---------------------------------------------------------------------------- decals
def decal(c, n, w, h, lines, bg="#ffffff", fg=INK, brand=False, layer=None, up=None, generic_only=False):
    """A printed panel centred at c, facing n (unit axis vector), w x h ft. lines: (text, size as a share of h,
    bold, colour or None, brand line, band colour or None)."""
    it = fuel.G["cur"]
    L = []
    for ln in lines:
        t, s, b, col, br, band = (list(ln) + [None] * 6)[:6]
        L.append(dict(t=t, s=s, b=int(bool(b)), c=col or fg, brand=int(bool(br)), band=band))
    d = dict(c=[round(v, 2) for v in c], n=list(n), w=round(w, 2), h=round(h, 2), bg=bg, lines=L, item=it["id"],
             layer=layer or it["layer"], brand=int(bool(brand)))
    if up:
        d["up"] = [round(v, 4) for v in up]
    if generic_only:
        d["nobrand"] = 1                         # the unbranded twin of a branded panel
    fuel.G.setdefault("decals", []).append(d)


FACE = {"-y": (0, -1, 0), "+y": (0, 1, 0), "-x": (-1, 0, 0), "+x": (1, 0, 0)}


def _frame(x, y, face):
    """(normal, tangent) unit vectors for a stand facing `face`."""
    n = FACE[face]
    t = (-n[1], n[0], 0)                       # tangent: normal turned 90 deg
    return n, t


def _at(x, y, n, t, u, v):
    """Point u along the tangent and v along the normal from (x, y)."""
    return x + t[0] * u + n[0] * v, y + t[1] * u + n[1] * v


# ---------------------------------------------------------------------------- reels and vehicles
def reel(x, y, D, W, axis, cable, product, flange="timber", length_ft=None, layer=None, z0=0.0):
    """Cable reel standing on its flanges; axis 'x' or 'y'. Stencilled flanges on both faces."""
    R = D / 2
    zc = z0 + R
    ax = (1, 0, 0) if axis == "x" else (0, 1, 0)
    pt = lambda s: (x + ax[0] * s, y + ax[1] * s, zc)
    for s in (-W / 2, W / 2 - .3):
        rod(pt(s), pt(s + .3), R, flange, seg=32)
    rod(pt(-W / 2 + .3), pt(W / 2 - .3), R * .78, cable, seg=28)
    rod(pt(-W / 2 - .1), pt(W / 2 + .1), R * .16, "steel", seg=12)                  # arbor hole bushing
    for sgn in (-1, 1):                                                           # chocks
        cx, cy = (x, y + sgn * (R * .75)) if axis == "x" else (x + sgn * (R * .75), y)
        if axis == "x":
            box(x - W / 2, x + W / 2, cy - .4, cy + .4, z0, z0 + .55, "timber")
        else:
            box(cx - .4, cx + .4, y - W / 2, y + W / 2, z0, z0 + .55, "timber")
    lines = [(BRAND, .24, 1, RED, 1), (product, .13, 1, "#2a2a2a")]
    if length_ft:
        lines.append((f"{length_ft:,} FT", .11, 0, "#2a2a2a"))
    for sgn in (-1, 1):
        c = pt(sgn * (W / 2 + .03))
        decal(c, (ax[0] * sgn, ax[1] * sgn, 0), D * .74, D * .4, lines, bg=None, brand=False, layer=layer)


def simpull_reel(x, y, z0, axis="x", cols=("cable", "red", "pvc_blue", "hardhat", "pvc_green")):
    """SIMpull Reel on its SIMpull payoff cart: steel reel on a wheeled frame, paralleled colour-coded THHN."""
    D, W = 4.6, 2.6
    R = D / 2
    zc = z0 + 1.1 + R
    ax = (1, 0, 0) if axis == "x" else (0, 1, 0)
    nx = (0, 1, 0) if axis == "x" else (1, 0, 0)
    pt = lambda s, o=0.0, dz=0.0: (x + ax[0] * s + nx[0] * o, y + ax[1] * s + nx[1] * o, zc + dz)
    # payoff cart: base frame, four casters, two uprights carrying the arbor
    a0, a1 = pt(-W / 2 - .5, -R), pt(W / 2 + .5, R)
    box(min(a0[0], a1[0]), max(a0[0], a1[0]), min(a0[1], a1[1]), max(a0[1], a1[1]), z0 + .55, z0 + .8, "sw_red")
    for s in (-W / 2 - .3, W / 2 + .3):
        for o in (-R + .4, R - .4):
            c = pt(s, o)
            rod((c[0], c[1], z0 + .3), (c[0], c[1], z0 + .55), .28, "fanhub", seg=10)
    for s in (-W / 2 - .35, W / 2 + .35):
        b0, b1 = pt(s, 0, -R + .3), pt(s, 0)
        rod((b0[0], b0[1], z0 + .8), b1, .14, "sw_red", seg=8)
    rod(pt(-W / 2 - .45), pt(W / 2 + .45), .12, "steel", seg=8)
    for s in (-W / 2, W / 2 - .18):
        rod(pt(s), pt(s + .18), R, "steel_dark", seg=28)
    # paralleled conductors wound side by side: colour bands across the drum
    n = len(cols)
    for k, c in enumerate(cols):
        s0 = -W / 2 + .18 + k * (W - .36) / n
        rod(pt(s0), pt(s0 + (W - .36) / n), R * .8, c, seg=24)
    for sgn in (-1, 1):
        decal(pt(sgn * (W / 2 + .02)), (ax[0] * sgn, ax[1] * sgn, 0), D * .7, D * .36,
              [(BRAND, .26, 1, RED, 1), ("SIMpull REEL", .17, 1, "#f2f2f2"), ("THHN / THWN-2", .12, 0, "#cfd3d6")],
              bg=None)


def simpull_truck(x, y):
    """SIMpull Truck: flatbed with SIMpull Reels on payoffs, cab to the east, tail lift at the rear (west)."""
    L, Wd = 34.0, 8.4
    x0, x1 = x - L / 2, x + L / 2
    y0, y1 = y - Wd / 2, y + Wd / 2
    box(x0 + 1, x1 - 1, y - 1.6, y + 1.6, 1.6, 2.6, "steel")                     # chassis rails
    # cab and hood
    box(x1 - 9, x1, y0 + .2, y1 - .2, 2.6, 6.2, "white_truck")
    box(x1 - 9, x1 - 2.6, y0 + .2, y1 - .2, 6.2, 10.2, "white_truck")
    box(x1 - 2.65, x1 - 2.55, y0 + .6, y1 - .6, 6.6, 9.6, "glass")                    # windscreen
    for s in (y0 + .15, y1 - .15):
        box(x1 - 8.4, x1 - 3.4, s - .06, s + .06, 6.7, 9.4, "glass")                  # door windows
    box(x1 - .2, x1 + .3, y0 + .8, y1 - .8, 2.8, 5.4, "steel")                    # grille / bumper
    # flatbed deck with red side skirts and a headboard
    box(x0, x1 - 9.6, y0, y1, 3.6, 4.2, "steel_dark")
    for s in (y0, y1 - .12):
        box(x0, x1 - 9.6, s, s + .12, 2.6, 4.2, "sw_red")
    box(x1 - 10.2, x1 - 9.6, y0, y1, 4.2, 10.6, "steel_dark")                     # headboard
    for ax in (x0 + 4, x0 + 8.5, x1 - 2.6):                                         # wheels (duals at the rear)
        rod((ax, y0 - .1, 1.9), (ax, y0 + 1.1, 1.9), 1.9, "fanhub", seg=16)
        rod((ax, y1 - 1.1, 1.9), (ax, y1 + .1, 1.9), 1.9, "fanhub", seg=16)
    # tail lift
    box(x0 - 3.2, x0, y0 + .4, y1 - .4, 3.55, 3.75, "steel")
    # three SIMpull Reels on payoffs, arbors across the truck
    for k in range(3):
        simpull_reel(x0 + 3.6 + k * 6.6, y, 4.2, axis="y")
    # livery: both skirts and the cab doors
    for sgn, s, sc in ((-1, y0 - .02, y0 + .18), (1, y1 + .02, y1 - .18)):
        decal(((x0 + x1 - 9.6) / 2, s, 3.4), (0, sgn, 0), 18, 1.5,
              [(BRAND + "  SIMpull SOLUTIONS", .55, 1, "#ffffff", 1)], bg=None, brand=True)
        decal((x1 - 7.0, sc, 4.4), (0, sgn, 0), 3.6, 2.6,
              [(BRAND, .3, 1, RED, 1), ("SIMpull", .26, 1, INK, 1), ("SOLUTIONS", .16, 0, "#555a5f", 1)],
              bg=None, brand=True)


def payoff_crew(x, y):
    import maintenance as mt
    mt.person(x - 2, y + 2.6, 0, -1.57)
    mt.person(x + 2.2, y - 2.6, 0, 1.57, vest="hivis_o")


# ---------------------------------------------------------------------------- spots
def reel_yard():
    """The drawn cable reel yard / outage laydown (x 40-320, y 690-900) stocked with reels, the SIMpull Truck
    unloading."""
    it = fuel.new_item("BASE_SERVICES", "Cable reel yard: stocked reels and SIMpull Truck",
                       (44, 316, 694, 896), (0, 14), basis="typical", register=False, area="F",
                       sheet="typical (cable product showcase)",
                       info="Reel yard on the drawn laydown pad: branded wooden reels of the plant cable families "
                            "in rows (230 kV XLPE, MV-105, ARMOR-X MC-HL, Type TC-ER, instrumentation), the SIMpull "
                            "Truck unloading SIMpull Reels on payoffs. "
                            "Cable supplier: Southwire (as requested); typical selection, not engineered.")
    fuel.G["cur"] = it
    # reel rows: axis along y so the stencilled flanges face the yard aisle (south) and the back (north)
    stock = [("hv", 13.0, 6.0, "steel_dark", "cable", "230 kV XLPE", 2200),
             ("mv", 8.0, 5.0, "timber", "cable_mv", "MV-105 15 kV 500 KCMIL", 3500),
             ("mv", 8.0, 5.0, "timber", "cable_mv", "MV-105 15 kV 500 KCMIL", 3500),
             ("armorx", 7.0, 4.4, "timber", "cable_armor", "ARMOR-X MC-HL 600 V", 2500),
             ("tc", 6.0, 4.0, "timber", "cable_tc", "TYPE TC-ER 600 V", 5000),
             ("inst", 5.0, 3.6, "timber", "cable_inst", "INSTRUMENTATION PLTC", 5000),
             ("tc", 6.0, 4.0, "timber", "cable_tc", "TYPE TC-ER CONTROL", 5000),
             ("mv", 8.0, 5.0, "timber", "cable_mv", "MV-105 35 kV 750 KCMIL", 3000)]
    for row, ry in enumerate((812, 836, 860)):
        x = 66
        for k in range(8):
            key, D, W, fl, cab, label, ft = stock[(k + row * 3) % len(stock)]
            if row > 0 and key == "hv":
                key, D, W, fl, cab, label, ft = stock[1]
            reel(x + D / 2, ry, D, W, "y", cab, label, flange=fl, length_ft=ft)
            x += D + 6
    # SIMpull Truck backed up to the yard aisle, tail to the west; two reels already on the ground
    simpull_truck(180, 734)
    for k, (x, y) in enumerate(((150, 748), (141, 753))):
        simpull_reel(x, y, 0, axis="x")
    payoff_crew(150, 748)
    import maintenance as mt
    mt.person(158, 728, 0, 3.14, vest="hivis_o")                     # driver at the tail lift
    return it


def build():
    fuel.G.setdefault("decals", [])
    reel_yard()
    return dict(decals=len(fuel.G["decals"]))


def stories():
    """Cable work staged where it tells the story of the plant being built and kept running:
    - modular yard: the SIMpull Truck has brought the replacement feeder reels to the 13.8 kV cable pull; two
      SIMpull Reels are already off the tail lift on payoffs, the crew walking them toward MH-A;
    - BESS: a DC cable reel on jack stands at the open precast trench, the crew pulling conductors in."""
    import maintenance as mt
    it = fuel.new_item("OPT_MOD", "Cable delivery: SIMpull Truck at the modular-yard cable pull",
                       (1738, 1782, 918, 936), (0, 12), basis="typical", register=False, area="I",
                       sheet="typical (cable installation)",
                       info="SIMpull Truck delivering paralleled, colour-coded feeder reels on SIMpull payoffs to the "
                            "13.8 kV collector cable replacement. Cable supplier: Southwire (as requested).")
    fuel.G["cur"] = it
    simpull_truck(1765, 928)
    simpull_reel(1741.5, 929, 0, axis="y")
    simpull_reel(1736, 933, 0, axis="y")
    mt.person(1739, 925.5, 0, 1.2, vest="hivis_o")               # pushing the payoff
    mt.person(1744.5, 932.5, 0, 3.4)
    mt.person(1751, 922.5, 0, 2.0)                                # driver at the tail lift controls
    it = fuel.new_item("OPT_BESS", "Cable pull: DC conductors into the BESS precast trench",
                       (1734, 1754, 535.5, 543.5), (0, 9), basis="typical", register=False, area="H",
                       sheet="typical (cable installation)",
                       info="Reel of 2 kV PV / RHW-2 DC conductor on jack stands; crew feeding it into the open precast "
                            "trench toward the inverter. Cable supplier: Southwire (as requested).")
    fuel.G["cur"] = it
    xr, yr, D, W = 1745.0, 539.5, 5.6, 3.4
    R = D / 2
    for s in (-1, 1):                                             # jack stands with the arbor shaft
        y = yr + s * (W / 2 + .5)
        rod((xr - 1.6, y, 0), (xr, y, R + .5), .12, "sw_red", seg=6)
        rod((xr + 1.6, y, 0), (xr, y, R + .5), .12, "sw_red", seg=6)
        box(xr - 1.8, xr + 1.8, y - .2, y + .2, 0, .15, "sw_red")
    rod((xr, yr - W / 2 - .7, R + .5), (xr, yr + W / 2 + .7, R + .5), .12, "steel", seg=8)
    reel(xr, yr, D, W, "y", "cable", "PV / RHW-2 2 kV 500 KCMIL", length_ft=2500, z0=.5)
    # conductor off the bottom of the reel, over a roller at the trench edge, down into the trench toward the west
    pts = [(xr - R * .6, yr, .5 + R * .5), (xr - R - .8, yr - 1.5, .9), (xr - R - 1.6, 535.6, .45), (xr - R - 2.2, 534.3, .2),
           (xr - R - 3.5, 534.3, -1.9), (1712, 534.3, -2.0)]
    for a, b in zip(pts, pts[1:]):
        rod(a, b, .075, "cable", seg=8)
    box(xr - R - 2.4, xr - R - 1.2, 535.2, 535.7, .15, .5, "crane")            # cable roller at the edge
    mt.person(xr - 5.5, 537.5, 0, 3.6)                                          # guiding the cable at the edge
    mt.person(1726, 536.4, 0, 3.1, vest="hivis_o")                              # pulling along the trench
    mt.person(1719, 536.5, 0, 3.1)
    mt.person(xr + 1.5, 542.6, 0, 4.4)                                          # reel tender


def jack_reel(xr, yr, D, W, cable, label, ft, z=0.0):
    """Wooden reel lifted on red reel jacks with an arbor shaft (axis along y)."""
    R = D / 2
    for s in (-1, 1):
        y = yr + s * (W / 2 + .5)
        rod((xr - 1.8, y, z), (xr, y, z + R + .5), .14, "sw_red", seg=6)
        rod((xr + 1.8, y, z), (xr, y, z + R + .5), .14, "sw_red", seg=6)
        box(xr - 2, xr + 2, y - .22, y + .22, z, z + .15, "sw_red")
    rod((xr, yr - W / 2 - .8, z + R + .5), (xr, yr + W / 2 + .8, z + R + .5), .14, "steel", seg=8)
    reel(xr, yr, D, W, "y", cable, label, length_ft=ft, z0=z + .5)


def turbine_hall_pull():
    """GT1 outage: a new 13.8 kV feeder to the GT1 auxiliaries is pulled from a reel on the laydown-bay floor, up
    over a sheave into the MV ladder tray at EL 48 and along it toward GT1; a lift on the turbine deck puts two
    electricians at tray level to feed and dress the cable; a capstan puller on the deck at the tray drop to GT1
    hauls the rope."""
    import maintenance as mt
    it = fuel.new_item("BASE_POWER_BLOCK", "Cable pull: GT1 13.8 kV feeder into the turbine-hall MV tray (outage)",
                       (518, 606, 436, 556), (0, 50), basis="typical", register=False, area="B",
                       sheet="typical (cable installation)",
                       info="Outage work: MV-105 feeder pulled from a reel on jacks in the laydown bay, over a sheave "
                            "into the EL 48 ladder tray and along it to the GT1 auxiliaries; deck lift with two "
                            "electricians feeding the tray; capstan puller at the tray drop. Cable supplier: Southwire "
                            "(as requested).")
    fuel.G["cur"] = it
    xr, yr, D = 532.0, 541.0, 9.0
    jack_reel(xr, yr, D, 5.0, "cable_mv", "MV-105 15 kV 500 KCMIL", 1800, z=.3)
    top = (xr + D * .4, yr, .3 + .5 + D * .9)
    # sheave hung from the tray corner support, the cable rising to it and into the tray
    sx, sy, sz = 557.2, 543.6, 46.6
    rod((sx, sy, sz + 1.1), (sx, sy, 49.4), .06, "steel", seg=6)                         # hanger
    rod((sx, sy - .25, sz), (sx, sy + .25, sz), 1.0, "crane", seg=18)                    # sheave wheel
    from maintenance import bez, poly
    poly(bez(top, ((top[0] + sx) / 2, (top[1] + sy) / 2 + .5, (top[2] + sz) / 2 + 3), (sx - .9, sy, sz + .6), 14), .1, "cable_mv", seg=10)
    poly(bez((sx + .2, sy, sz + 1.0), (sx + 1.6, sy, sz + 2.2), (561.5, 544.2, 48.55), 6), .1, "cable_mv", seg=10)
    rod((561.5, 544.2, 48.55), (598.6, 544.2, 48.55), .1, "cable_mv", seg=10)          # laid in the tray
    rod((598.6, 544.2, 48.55), (599.4, 446, 48.55), .04, "rope", seg=6)                 # pulling rope ahead
    rod((599.4, 446, 48.55), (601, 446, 22.4), .04, "rope", seg=6)
    # capstan puller on the deck at the drop
    box(599, 605, 443, 449, 20, 21.2, "sw_red")
    rod((601, 446, 21.2), (601, 446, 23), .55, "steel", seg=14)
    box(603, 605, 443.5, 445, 21.2, 23.5, "sw_red")
    mt.person(604, 451, 20, 4.7)
    # scissor lift on the deck beside the tray, platform at EL 42.6
    lx0, lx1, ly0, ly1 = 566, 574, 536, 541
    box(lx0, lx1, ly0, ly1, 20, 21.5, "crane")
    for k in range(5):                                                                   # scissor arms
        z0, z1 = 21.5 + k * 4.2, 21.5 + (k + 1) * 4.2
        for y in (ly0 + .3, ly1 - .3):
            rod((lx0 + .5, y, z0), (lx1 - .5, y, z1), .1, "crane", seg=6)
            rod((lx1 - .5, y, z0), (lx0 + .5, y, z1), .1, "crane", seg=6)
    box(lx0 - .5, lx1 + .5, ly0 - .3, ly1 + .3, 42.5, 42.8, "grating")
    for (a0, a1, b0, b1) in ((lx0 - .5, lx1 + .5, ly0 - .3, ly0 - .2), (lx0 - .5, lx1 + .5, ly1 + .2, ly1 + .3),
                             (lx0 - .5, lx0 - .4, ly0 - .3, ly1 + .3), (lx1 + .4, lx1 + .5, ly0 - .3, ly1 + .3)):
        box(a0, a1, b0, b1, 46, 46.15, "crane")
    for (px, py) in ((lx0 - .45, ly0 - .25), (lx1 + .45, ly0 - .25), (lx0 - .45, ly1 + .25), (lx1 + .45, ly1 + .25)):
        rod((px, py, 42.8), (px, py, 46), .05, "crane", seg=4)
    mt.person(568.5, 540, 42.8, 1.57, vest="hivis_o")
    mt.person(572, 539.8, 42.8, 1.2)
    # floor crew
    mt.person(xr + 6, yr - 4, .3, 2.4)                                                   # reel tender
    mt.person(xr + 10, yr + 3.5, .3, .3, vest="hivis_o")                                # watches the sheave, radio
    mt.person(xr - 7, yr - 9, .3, .9, hat="sign")                                        # supervisor


def splice_230(cy=575.0, cx=1520.0):
    """230 kV underground cable jointing on the CCS cable bank (x 1520): an open joint bay (vault) cut into the
    duct bank, the three single-core XLPE cables (Southwire 230 kV, the requested supplier) racked along the walls
    with staggered joints (two finished, the middle one in progress: XLPE pencilled back, connector crimped),
    cross-bonding link box, ladder, guard rail; a white jointing tent over it (sides rolled up), generator and air
    conditioner for a clean, dry joint; the next 230 kV reel on a lowboy; the HV test van; crew."""
    import maintenance as mt
    import cable_install as ci
    G = fuel.G
    L = "OPT_CCS"
    hx, hy = 5.0, 16.0                                              # vault outer half-sizes
    x0, x1, y0, y1 = cx - hx, cx + hx, cy - hy, cy + hy
    ZF = -9.5                                                       # vault floor top
    # cut the duct bank where the vault is
    bank = {i["id"] for i in G["items"] if i["name"].startswith("Underground: 230 kV cable banks")}
    out = []
    for p in list(G["parts"]):
        if p["item"] not in bank:
            continue
        if p["kind"] == "box" and p["min"][0] < x1 and p["max"][0] > x0 and p["min"][1] < y0 and p["max"][1] > y1:
            G["parts"].remove(p)
            out += [dict(p, max=[p["max"][0], y0, p["max"][2]]), dict(p, min=[p["min"][0], y1, p["min"][2]])]
        elif p["kind"] == "rod" and x0 < p["a"][0] < x1 and min(p["a"][1], p["b"][1]) < y0 and max(p["a"][1], p["b"][1]) > y1:
            G["parts"].remove(p)
            lo, hi = sorted((p["a"][1], p["b"][1]))
            out += [dict(p, a=[p["a"][0], lo, p["a"][2]], b=[p["a"][0], y0 + .5, p["a"][2]]),
                    dict(p, a=[p["a"][0], y1 - .5, p["a"][2]], b=[p["a"][0], hi, p["a"][2]])]
    G["parts"] += out
    ci.cut_ground([(x0 + 1, x1 - 1, y0 + 1, y1 - 1)], "NOCCS_GROUND")
    it = fuel.new_item(L, "230 kV cable splice: joint bay, jointing tent, reel on lowboy, test van (CCS cable bank)",
                       (1488, 1546, cy - 43, cy + 47), (ZF - 1, 14), basis="typical", register=False, area="G",
                       sheet="typical (cable installation)",
                       info="Jointing the 230 kV XLPE cable circuit to the CCS transformers in an open joint bay on "
                            "the cable bank: three staggered pre-moulded joints on cable racks, cross-bonding link box, "
                            "a clean jointing tent with generator and air conditioning, the next drum on a lowboy, and "
                            "the HV test van for the after-installation test. Cable supplier: Southwire (as requested).")
    G["cur"] = it
    # vault: floor, walls (opening to the bank at both ends), collar at grade
    box(x0, x1, y0, y1, ZF - 1, ZF, "concrete")
    for (a0, a1, b0, b1) in ((x0, x0 + 1, y0, y1), (x1 - 1, x1, y0, y1)):
        box(a0, a1, b0, b1, ZF, .3, "concrete")
    for (b0, b1) in ((y0, y0 + 1), (y1 - 1, y1)):
        box(x0 + 1, x1 - 1, b0, b1, ZF, -7.9, "concrete")             # end walls below and above the duct entry
        box(x0 + 1, x1 - 1, b0, b1, -5.1, .3, "concrete")
    # guard rail round the opening, gap at the ladder
    for (a, b) in (((x0 - .3, y0 - .3), (x1 + .3, y0 - .3)), ((x0 - .3, y1 + .3), (x1 + .3, y1 + .3)),
                   ((x0 - .3, y0 - .3), (x0 - .3, y1 + .3)), ((x1 + .3, y0 - .3), (x1 + .3, cy + 6))):
        for z in (2.0, 3.5):
            rod((a[0], a[1], z), (b[0], b[1], z), .06, "crane", seg=6)
    for (px, py) in ((x0 - .3, y0 - .3), (x1 + .3, y0 - .3), (x0 - .3, y1 + .3), (x1 + .3, y1 + .3), (x0 - .3, cy),
                     (x1 + .3, cy - 6), (x1 + .3, cy + 6)):
        rod((px, py, .3), (px, py, 3.6), .07, "crane", seg=6)
    for z in [ZF + .5 + k for k in range(10)]:                        # fixed ladder on the east wall
        rod((x1 - 1.05, cy + 8.6, z), (x1 - 1.05, cy + 10, z), .05, "steel", seg=4)
    for yy in (cy + 8.6, cy + 10):
        rod((x1 - 1.05, yy, ZF), (x1 - 1.05, yy, 3.5), .06, "steel", seg=6)
    # cable racks on the side walls and the three phases with staggered joints
    phases = [(x0 + 1.6, -1), (cx, 0), (x1 - 1.6, 1)]
    for (px, k) in phases:
        for yy in [y0 + 3 + j * 4 for j in range(int((y1 - y0 - 5) // 4) + 1)]:
            box(px - .5, px + .5, yy - .15, yy + .15, ZF, -7.2, "steel")      # rack stands
        zc = -6.9
        ent = (px, y0 + .5, -6.45)
        ext = (px, y1 - .5, -6.45)
        rod(ent, (px, y0 + 2.5, zc), .23, "cable", seg=14)
        rod((px, y1 - 2.5, zc), ext, .23, "cable", seg=14)
        jy = cy + k * 7                                                     # staggered joint positions
        if k != 0:                                                          # finished joints
            rod((px, y0 + 2.5, zc), (px, jy - 4, zc), .23, "cable", seg=14)
            rod((px, jy + 4, zc), (px, y1 - 2.5, zc), .23, "cable", seg=14)
            rod((px, jy - 4, zc), (px, jy - 2.6, zc), .23, "cable", r2=.62, seg=18)
            rod((px, jy - 2.6, zc), (px, jy + 2.6, zc), .62, "cable", seg=18)          # joint body (casing)
            rod((px, jy + 2.6, zc), (px, jy + 4, zc), .62, "cable", r2=.23, seg=18)
            for d in (-2.0, 0, 2.0):
                rod((px, jy + d - .06, zc), (px, jy + d + .06, zc), .64, "copper_dark", seg=18)   # earthing bands
            rod((px, jy, zc + .6), (px + (.5 if px < cx else -.5), jy, -4.8), .06, "copper", seg=6)  # bonding lead
        else:                                                               # joint in progress
            rod((px, y0 + 2.5, zc), (px, jy - 3.2, zc), .23, "cable", seg=14)
            rod((px, jy + 3.2, zc), (px, y1 - 2.5, zc), .23, "cable", seg=14)
            for s in (-1, 1):
                rod((px, jy + s * 3.2, zc), (px, jy + s * 2.1, zc), .2, "xlpe", seg=14)       # XLPE prepared
                rod((px, jy + s * 2.1, zc), (px, jy + s * 1.7, zc), .2, "xlpe", r2=.1, seg=14)  # pencilled
                rod((px, jy + s * 1.7, zc), (px, jy + s * .4, zc), .09, "copper", seg=10)      # conductor
            rod((px, jy - .6, zc), (px, jy + .6, zc), .13, "alu", seg=12)                     # connector
            rod((px, jy - 4.8, zc), (px, jy - 3.4, zc), .66, "cable", seg=18)                 # joint body parked
            box(px - 1.4, px + 1.4, jy - 1, jy + 1, ZF, -7.9, "timber")                       # work stand
        ci.legend((px + (.24 if px < x1 - 2 else -.24), y1 - 4, zc), (1 if px < x1 - 2 else -1, 0, 0), (0, 1, 0),
                  2.6, ci.LEGEND_HV, h=.1)
    box(x0 + 1, x0 + 1.5, cy - 1.2, cy + 1.2, -5.0, -3.2, "alu")              # cross-bonding link box
    rod((x0 + 1.25, cy, -5.0), (x0 + 1.25, cy, ZF), .05, "copper", seg=6)
    # jointers in the bay, supervisor and helper at the rim
    mt.person(cx + 1.3, cy - 1, ZF, 3.1)
    mt.person(cx - 1.3, cy + 1.5, ZF, 0, vest="hivis_o")
    mt.person(x1 + 2.5, cy - 4, 0, 3.14, hat="sign")
    mt.person(x0 - 2.5, cy + 9, 0, 0)
    # jointing tent (sides rolled up): frame, ridge roof, rolled sides at the eaves
    tx0, tx1, ty0, ty1, ze, zr = x0 - 2, x1 + 2, y0 - 2, y1 + 2, 9.0, 12.5
    for px in (tx0, tx1):
        for py in [ty0 + j * (ty1 - ty0) / 4 for j in range(5)]:
            rod((px, py, 0), (px, py, ze), .1, "alu", seg=6)
            box(px - .4, px + .4, py - .4, py + .4, 0, .15, "steel")
    G["parts"].append(dict(kind="prism", min=[tx0 - .3, ty0 - .3, ze], max=[tx1 + .3, ty1 + .3, zr], ridge="y",
                           color="tent", item=it["id"], layer=L))
    for px in (tx0 - .1, tx1 + .1):
        rod((px, ty0, ze - .4), (px, ty1, ze - .4), .3, "tent", seg=10)            # rolled-up side walls
    box(tx0 - .3, tx1 + .3, ty0 - .35, ty0 - .3, ze - 1.2, ze, "tent")              # valance, ends
    box(tx0 - .3, tx1 + .3, ty1 + .3, ty1 + .35, ze - 1.2, ze, "tent")
    decal((cx, ty0 - .4, ze - .6), (0, -1, 0), 9, 1.0,
          [(BRAND + "  HV CABLE JOINTING", .6, 1, RED, 1)], bg=None, brand=True)
    decal((cx, ty0 - .4, ze - .6), (0, -1, 0), 9, 1.0, [("HV CABLE JOINTING - CLEAN AREA", .55, 1, "#c03030")],
          bg=None, generic_only=True)
    # generator and air conditioner east of the tent, hoses / leads into the tent
    gx, gy = 1541.5, cy + 14
    box(gx - 2.5, gx + 2.5, gy - 5, gy + 5, 0, 1.2, "steel_dark")
    box(gx - 2.3, gx + 2.3, gy - 4.6, gy + 4.6, 1.2, 6.2, "white_truck")
    rod((gx, gy - 7.5, 1.2), (gx, gy - 5, 1.2), .12, "steel", seg=6)              # trailer tongue
    for s in (-1, 1):
        rod((gx + s * 2.6, gy, 1.2), (gx + s * 3.1, gy, 1.2), 1.1, "fanhub", seg=12)
    box(1532, 1536, cy + 4, cy + 8, 0, 4.5, "machine")                                      # spot air conditioner
    rod((1532, cy + 6, 3.5), (x1 + 2, cy + 6, 3.5), .5, "white_truck", seg=12)            # flexible duct into the tent
    rod((gx - 2.5, gy - 3, .6), (x1 + 2, cy + 9, .1), .06, "cable", seg=6)
    for yy in (cy - 10, cy, cy + 10):                                                  # work lights under the ridge
        box(cx - .8, cx + .8, yy - .4, yy + .4, 11.3, 11.6, "lamp")
        rod((cx, yy, 11.6), (cx, yy, 12.3), .03, "steel", seg=4)
    # HV test van, north-east, back doors open toward the bay
    vx, vy = 1537.0, cy + 29
    box(vx - 3.6, vx + 3.6, vy - 9, vy + 9, 1.2, 9.2, "white_truck")
    box(vx - 3.4, vx + 3.4, vy + 9, vy + 12, 1.2, 6.5, "white_truck")
    box(vx - 3.2, vx + 3.2, vy + 11.9, vy + 12.05, 4.2, 6.3, "glass")
    for s in (-1, 1):
        for yy in (vy - 6, vy + 9):
            rod((vx + s * 3.6, yy, 1.4), (vx + s * 4.1, yy, 1.4), 1.4, "fanhub", seg=12)
    box(vx - 3.6, vx - .2, vy - 9.3, vy - 9.1, 1.4, 8.6, "white_truck")              # rear doors swung open
    decal((vx - 3.65, vy, 6), (-1, 0, 0), 12, 1.6, [("HV CABLE TEST", .55, 1, "#1d1f21")], bg=None)
    rod((vx - 1, vy - 9.2, 2), (x1 + .3, cy + 12, .1), .07, "cable_fo", seg=6)       # test lead to the bay
    mt.person(vx - 4.8, vy - 12, 0, 3.6)
    # the next 230 kV drum on a lowboy west of the bay, tractor to the north
    lx, ly = 1499.0, cy - 3
    box(lx - 4.2, lx + 4.2, ly - 18, ly + 14, 2.2, 3.0, "steel_dark")                # lowboy deck
    box(lx - 4.2, lx + 4.2, ly + 14, ly + 26, 3.0, 5.0, "steel_dark")                 # gooseneck
    for yy in (ly - 15, ly - 11.5, ly - 8):
        for s in (-1, 1):
            rod((lx + s * 3.6, yy, 1.5), (lx + s * 4.3, yy, 1.5), 1.5, "fanhub", seg=12)
    box(lx - 4, lx + 4, ly + 20, ly + 40, 1.6, 4.5, "steel_dark")                     # tractor chassis
    box(lx - 4, lx + 4, ly + 30, ly + 40, 4.5, 11, "sw_red")                           # cab
    box(lx - 3.8, lx + 3.8, ly + 39.9, ly + 40.05, 7.5, 10.5, "glass")
    for yy in (ly + 24, ly + 28, ly + 37):
        for s in (-1, 1):
            rod((lx + s * 3.7, yy, 1.8), (lx + s * 4.4, yy, 1.8), 1.8, "fanhub", seg=12)
    reel(lx, ly - 2, 13.0, 7.2, "x", "cable", "230 kV XLPE 2500 KCMIL CU", flange="steel_dark", length_ft=1950, z0=3.0)
    for s in (-1, 1):                                                                 # chain binders
        rod((lx + s * 3.0, ly - 9, 3), (lx + s * 3.0, ly - 2, 9.5), .06, "steel", seg=4)
        rod((lx + s * 3.0, ly + 5, 3), (lx + s * 3.0, ly - 2, 9.5), .06, "steel", seg=4)
    mt.person(lx + 6, ly - 12, 0, 1.8, vest="hivis_o")
    # work-area barrier
    for (a, b) in (((1488, cy - 43), (1546, cy - 43)), ((1546, cy - 43), (1546, cy + 15)), ((1488, cy - 43), (1488, cy + 47))):
        n = max(2, int(math.dist(a, b) // 8))
        for j in range(n + 1):
            px, py = a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n
            rod((px, py, 0), (px, py, 3.6), .06, "steel", seg=4)
        rod((a[0], a[1], 3.3), (b[0], b[1], 3.3), .05, "barrier", seg=4)
        rod((a[0], a[1], 2.2), (b[0], b[1], 2.2), .05, "barrier", seg=4)
    return it
