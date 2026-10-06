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



# printed jacket legends by tray cable colour: (text, ink)
LEGENDS = {
    "cable_mv": ("MV-105  15 kV  1/C 500 KCMIL CU  EPR 133%  TAPE SHIELD  PVC  UL 1072", "#e8e8e4"),
    "cable_armor": ("ARMOR-X  MC-HL  15 kV  3/C 500 KCMIL CU  EPR  CWA  PVC  UL 2225", "#f0e6d8"),
    "cable_tc": ("TYPE TC-ER  600 V  3/C 4/0 AWG CU  XHHW-2  SUN RES  UL 1277", "#e8e8e4"),
    "cable_inst": ("INSTRUMENTATION  PLTC-ER  16 AWG  4 TSP  300 V  ICEA S-73-532", "#f2f2ee"),
    "cable_tcx": ("TYPE KX  THERMOCOUPLE EXT  16 AWG  2/C  PLTC-ER", "#1d1f21"),
}


def tray_legends(x0=596.0, x1=724.0, step=6.5, y0=541.5, y1=553.5, z0=41.5, z1=50.0):
    """Print the jacket legend on the top of every tray cable in the turbine-hall tray stack between x0 and x1,
    repeated along the cable the way it is printed at the factory (staggered per cable)."""
    tr = next(i for i in fuel.G["items"] if i["name"].startswith("Cable trays and isolated-phase"))
    cur = fuel.G["cur"]
    fuel.G["cur"] = tr
    n = 0
    sa, ca = math.sin(math.radians(40)), math.cos(math.radians(40))    # print turned 40 deg toward the walkway
    for p in [q for q in fuel.G["parts"] if q["item"] == tr["id"] and q["kind"] == "rod" and q["color"] in LEGENDS]:
        a, b = p["a"], p["b"]
        if abs(a[1] - b[1]) > .01 or abs(a[2] - b[2]) > .01 or not (y0 < a[1] < y1 and z0 < a[2] < z1):
            continue
        lo, hi = sorted((a[0], b[0]))
        text, ink = LEGENDS[p["color"]]
        r = p["r"]
        L = min(4.6, 2.6 + r * 6)
        off = (hash((round(a[1], 2), round(a[2], 2))) % 7) / 7 * step
        x = max(lo, x0) + off
        while x + L < min(hi, x1):
            for (t, br) in ((BRAND + "  " + text, 1), (text, 0)):
                decal((x + L / 2, a[1] - (r + .005) * sa, a[2] + (r + .005) * ca), (0, -sa, ca), L, r * .7,
                      [(t, .8, 1, ink, br)], bg=None, up=(0, ca, sa), generic_only=not br)
            n += 1
            x += step
    fuel.G["cur"] = cur
    return n


def tray_dresser(lx0=650.0, ly0=535.0):
    """Electrician on a scissor lift beside the tray stack (deck EL 20), dressing and tying the cables in the MV tray,
    a second checking the cable tags in the LV tray; a reel of tie wraps and tags on the platform."""
    import maintenance as mt
    it = fuel.new_item("BASE_POWER_BLOCK", "Cable dressing: electricians on a lift at the turbine-hall tray stack",
                       (lx0 - .5, lx0 + 7.5, ly0 - .3, ly0 + 5.8), (20, 50), basis="typical", register=False,
                       area="B", sheet="typical (cable installation)",
                       info="Tray stack east of GT1: MV-105 and ARMOR-X in the EL 48 MV tray, Type TC-ER and MC-HL "
                            "in the EL 44 LV trays, instrumentation and thermocouple cable in the EL 42 control tray; "
                            "electricians dressing and tagging cable from a scissor lift. Cable supplier: Southwire "
                            "(as requested).")
    fuel.G["cur"] = it
    lx1, ly1, zp = lx0 + 7, ly0 + 5, 42.6
    box(lx0, lx1, ly0, ly1, 20, 21.5, "crane")
    for k in range(5):
        z0_, z1_ = 21.5 + k * (zp - 21.5) / 5, 21.5 + (k + 1) * (zp - 21.5) / 5
        for y in (ly0 + .3, ly1 - .3):
            rod((lx0 + .5, y, z0_), (lx1 - .5, y, z1_), .1, "crane", seg=6)
            rod((lx1 - .5, y, z0_), (lx0 + .5, y, z1_), .1, "crane", seg=6)
    box(lx0 - .3, lx1 + .3, ly0 - .2, ly1 + .3, zp, zp + .3, "grating")
    for (a0, a1, b0, b1) in ((lx0 - .3, lx1 + .3, ly0 - .2, ly0 - .1), (lx0 - .3, lx1 + .3, ly1 + .2, ly1 + .3),
                             (lx0 - .3, lx0 - .2, ly0 - .2, ly1 + .3), (lx1 + .2, lx1 + .3, ly0 - .2, ly1 + .3)):
        box(a0, a1, b0, b1, zp + 3.5, zp + 3.65, "crane")
    for (px, py) in ((lx0 - .25, ly0 - .15), (lx1 + .25, ly0 - .15), (lx0 - .25, ly1 + .25), (lx1 + .25, ly1 + .25)):
        rod((px, py, zp + .3), (px, py, zp + 3.5), .05, "crane", seg=4)
    mt.person(lx0 + 2.2, ly1 - .8, zp + .3, 1.57, vest="hivis_o")          # reaching into the MV tray
    mt.person(lx0 + 5.2, ly1 - 1.2, zp + .3, 1.3)                          # checking tags in the LV tray
    box(lx0 + .4, lx0 + 1.4, ly0 + .3, ly0 + 1.1, zp + .3, zp + 1.1, "sw_red")   # tool bag
    for k in range(3):                                                     # fresh black ties on the MV bundle
        x = lx0 + 1 + k * 2.2
        rod((x, 542.6, 48.0), (x, 542.6, 49.5), .03, "cable", seg=4)
        rod((x, 542.6, 49.5), (x, 545.4, 49.5), .03, "cable", seg=4)
        rod((x, 545.4, 49.5), (x, 545.4, 48.0), .03, "cable", seg=4)
    for k, x in enumerate((lx0 + 4.5, lx0 + 6.2)):                         # yellow cable tags on the LV cables
        box(x, x + .5, 543.95, 544.05, 44.2, 44.55, "crane")
    return it


def armor_ribs(x0=596.0, x1=652.0, pitch=.2):
    """ARMOR-X: the corrugated welded aluminium armor shows through the PVC jacket as ribs; drawn on the stretch of
    the MV-tray ARMOR-X circuit seen in the tray-stack shots."""
    tr = next(i for i in fuel.G["items"] if i["name"].startswith("Cable trays and isolated-phase"))
    cur = fuel.G["cur"]
    fuel.G["cur"] = tr
    n = 0
    for p in [q for q in fuel.G["parts"] if q["item"] == tr["id"] and q["kind"] == "rod" and q["color"] == "cable_armor"
              and abs(q["a"][1] - q["b"][1]) < .01 and 40 < q["a"][2] < 52]:
        lo, hi = sorted((p["a"][0], p["b"][0]))
        y, z, r = p["a"][1], p["a"][2], p["r"]
        x = max(lo, x0)
        while x < min(hi, x1):
            rod((x, y, z), (x + pitch * .45, y, z), r * 1.035, "cable_armor", seg=16)
            n += 1
            x += pitch
    fuel.G["cur"] = cur
    return n


def armor_sample(x=651.2, y=538.6, z=43.25):
    """A cut-off end of ARMOR-X lying on the lift platform beside the tool bag (the offcut from the termination):
    jacket stripped back to show the corrugated aluminium armor, then the three insulated conductors."""
    it = next(i for i in fuel.G["items"] if i["name"].startswith("Cable dressing: electricians"))
    cur = fuel.G["cur"]
    fuel.G["cur"] = it
    r = .38
    rod((x, y, z), (x + 1.6, y, z), r, "cable_armor", seg=18)                     # jacket
    xa = x + 1.6
    for k in range(9):                                                             # bare corrugated armor
        rod((xa + k * .2, y, z), (xa + k * .2 + .1, y, z), r * .98, "alu", seg=18)
        rod((xa + k * .2 + .1, y, z), (xa + k * .2 + .2, y, z), r * .9, "alu", seg=18)
    xc = xa + 1.8
    for j, c in enumerate(("cable", "red", "pvc_blue")):                           # conductors fanned out
        a = 2 * math.pi * j / 3
        oy, oz = .14 * math.cos(a), .14 * math.sin(a)
        rod((xc - .1, y + oy, z + oz), (xc + .9, y + oy * 2.2, z + oz * 1.4), .11, c, seg=12)
        rod((xc + .9, y + oy * 2.2, z + oz * 1.4), (xc + 1.25, y + oy * 2.2, z + oz * 1.4), .06, "copper", seg=8)
    fuel.G["cur"] = cur
