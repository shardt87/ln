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
