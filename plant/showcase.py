"""Cable product showcase (Southwire, the requested cable supplier): where the cable goes in the plant, shown at
product level. Typical selection, not engineered; product families as named in the cable schedule (trays.py,
wiring.py); exact constructions and part numbers to be confirmed with the supplier.

- decals: flat printed panels (placards, reel-flange stencils, truck livery) kept in G["decals"], drawn by the
  viewer (canvas texture) and Blender (image texture). Lines flagged "brand" are dropped from the generic build
  (build_viewer.py --generic) so the plant model also exists unbranded.
- cutaway stands: a plinth with a true-size cable sample on top, each layer stepped back (conductor, insulation,
  shield, sheath / armor, jacket) and a spec placard, with a sign panel behind; one at each application point and
  a full product row in the reel yard.
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
def decal(c, n, w, h, lines, bg="#ffffff", fg=INK, brand=False, layer=None, up=None):
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
        d["up"] = list(up)
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


# ---------------------------------------------------------------------------- products
# layers from the outside in: (radius ft, colour, setback from the cut end ft); the conductor shows furthest.
# multi: inner conductors (count, radius of each, insulation colours) for multiconductor cables.
PRODUCTS = {
    "hv": dict(name="HV UNDERGROUND TRANSMISSION CABLE", rating="230 kV XLPE",
               spec=["2500 kcmil Cu segmental conductor", "XLPE insulation, triple extruded",
                     "Cu wire screen + Al laminate sheath", "HDPE jacket, graphite coated"],
               layers=[(.21, "cable", 0), (.195, "alu", .35), (.185, "copper_dark", .6), (.175, "cable", .8),
                       (.17, "xlpe", .95), (.085, "cable", 1.55), (.08, "copper", 1.75)]),
    "mv": dict(name="MV-105 SHIELDED POWER CABLE", rating="15 kV / 35 kV, 133 % EPR",
               spec=["500 kcmil Cu, compact stranded", "EPR insulation, 133 % level", "Cu tape shield",
                     "PVC jacket, red stripes", "ICEA S-93-639 / UL 1072"],
               layers=[(.09, "cable_mv", 0), (.083, "copper_dark", .3), (.08, "cable", .45), (.075, "xlpe", .55),
                       (.035, "copper", .95)]),
    "armorx": dict(name="ARMOR-X MC-HL", rating="600 V - 15 kV, hazardous locations",
                   spec=["3/C Cu XHHW-2 + grounds", "continuous corrugated welded Al armor",
                         "PVC jacket overall", "Class I Div 1 & 2, UL 2225"],
                   layers=[(.1, "cable_tc", 0), (.094, "alu", .35)],
                   multi=(3, .032, ["cable", "red", "pvc_blue"])),
    "tc": dict(name="TYPE TC-ER POWER & CONTROL", rating="600 V tray cable",
               spec=["Cu XHHW-2 / THHN conductors", "exposed run rated (TC-ER)", "PVC jacket, sunlight resistant",
                     "UL 1277, ICEA S-73-532"],
               layers=[(.075, "cable_tc", 0)], multi=(4, .024, ["cable", "red", "pvc_blue", "pvc_green"])),
    "inst": dict(name="INSTRUMENTATION CABLE", rating="300 / 600 V, PLTC / ITC",
                 spec=["16 / 18 AWG shielded pairs & triads", "Al-mylar shield, drain wire",
                       "blue jacket for IS circuits", "ICEA S-73-532"],
                 layers=[(.06, "cable_inst", 0), (.056, "alu", .2)], multi=(3, .018, ["cable", "hardhat", "red"])),
    "thhn": dict(name="SIMpull THHN / THWN-2", rating="600 V building wire",
                 spec=["Cu, SIMpull jacket - no lube needed", "paralleled & colour coded on one reel",
                       "SIMpull Reel and payoff delivery", "UL 83"],
                 layers=[], multi=(5, .03, ["cable", "red", "pvc_blue", "hardhat", "pvc_green"])),
    "oh": dict(name="OVERHEAD CONDUCTOR", rating="ACSR / ACSS / C7",
               spec=["Al 1350 strands (trapezoidal option)", "steel or C7 carbon-fibre core",
                     "high temperature, low sag (ACSS, C7)", "ASTM B232 / B856"],
               layers=[(.075, "alu", 0), (.045, "steel", .7), (.035, "cable", 1.2)]),
    "cu": dict(name="BARE COPPER GROUNDING", rating="4/0 AWG soft-drawn Cu",
               spec=["19-strand bare Cu, Class B", "station ground grid and risers",
                     "exothermic or compression joints", "ASTM B3 / B8"],
               layers=[(.04, "copper", 0)]),
    "dc": dict(name="ARMORLITE MC / MV-105 35 kV", rating="data centre distribution",
               spec=["34.5 kV MV-105 feeders to the pad-mounts", "Armorlite / MC-PCS branch circuits",
                     "LSZH and plenum options", "UL 1569 / UL 1072"],
               layers=[(.06, "alu", 0)], multi=(4, .02, ["cable", "red", "pvc_blue", "pvc_green"])),
}


SCALE = {"hv": 1.6, "oh": 2.4, "cu": 2.6}


def sample(x, y, z, t, key, L=3.8):
    """Display sample (2:1 so the layers read; 230 kV at 1.6:1) lying along tangent t, centred on (x, y), axis at
    height z; cut end at +t, each layer stepped back."""
    P = dict(PRODUCTS[key])
    k_ = SCALE.get(key, 2.2)
    backs = [b for (_, _, b) in P["layers"]][::-1]          # outermost layer stepped back furthest from the cut
    P["layers"] = [(r * k_, c, b) for (r, c, _), b in zip(P["layers"], backs)]
    if "multi" in P:
        P["multi"] = (P["multi"][0], P["multi"][1] * k_, P["multi"][2])
    u0 = -L / 2
    end = lambda s: (x + t[0] * (u0 + s), y + t[1] * (u0 + s), z)
    for (r, c, back) in P["layers"]:
        rod(end(0), end(L - back), r, c, seg=20)
    if "multi" in P:
        k, rr, cols = P["multi"]
        back = min(b for (_, _, b) in P["layers"]) if P["layers"] else 0
        jacket_end = L - back - .25
        ring = (P["layers"][-1][0] * .55) if P["layers"] else rr * 1.6
        for j in range(k):
            a = 2 * math.pi * j / k
            oz, ot = ring * math.sin(a), ring * math.cos(a)
            ex = (t[1] * ot, -t[0] * ot)          # offset across the cable, in plan
            a0 = (x + t[0] * u0 + ex[0], y + t[1] * u0 + ex[1], z + oz)
            sp = .25 + .12 * j                   # fanned out a little past the jacket
            a1 = (x + t[0] * (u0 + jacket_end + sp) + ex[0] * 1.6, y + t[1] * (u0 + jacket_end + sp) + ex[1] * 1.6,
                  z + oz * 1.6)
            rod(a0, a1, rr, cols[j % len(cols)], seg=10)
            tip = (a1[0] + t[0] * .3, a1[1] + t[1] * .3, a1[2])
            rod(a1, tip, rr * .55, "copper", seg=8)


def stand(x, y, face, key, layer=None):
    """Cutaway display stand: plinth, sample, spec placard on the front, sign panel behind."""
    n, t = _frame(x, y, face)
    P = PRODUCTS[key]
    W, Dp, H = 4.6, 1.5, 3.0
    corners = [_at(x, y, n, t, su * W / 2, sv * Dp / 2) for su in (-1, 1) for sv in (-1, 1)]
    xs, ys = [c[0] for c in corners], [c[1] for c in corners]
    box(min(xs), max(xs), min(ys), max(ys), 0, .25, "concrete")
    box(min(xs) + .1, max(xs) - .1, min(ys) + .1, max(ys) - .1, .25, H, "cabinet")
    rmax = max([l[0] for l in P["layers"]] + [.08]) * SCALE.get(key, 2.2)
    for su in (-1.4, 1.4):                                            # cradles
        cx, cy = _at(x, y, n, t, su, 0)
        box(cx - .2, cx + .2, cy - .2, cy + .2, H, H + rmax * .9, "steel")
    sample(x, y, H + rmax + .02, t, key)
    fx, fy = _at(x, y, n, t, 0, Dp / 2 - .1 + .02)
    decal((fx, fy, 1.55), n, W - .5, 2.3,
          [(BRAND, .17, 1, "#ffffff", 1, RED), (P["name"], .1, 1), (P["rating"], .085, 0, RED)] +
          [(s, .068, 0, "#3b4045") for s in P["spec"]], layer=layer)
    # sign panel behind the sample, on two posts
    bx, by = _at(x, y, n, t, 0, -Dp / 2 - .5)
    for su in (-2.1, 2.1):
        px, py = _at(bx, by, n, t, su, 0)
        rod((px, py, 0), (px, py, 7.4), .1, "steel", seg=8)
    p0 = _at(bx, by, n, t, -2.5, -.06)
    p1 = _at(bx, by, n, t, 2.5, .06)
    box(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]), 4.6, 7.6, "sign")
    sx, sy = _at(bx, by, n, t, 0, .08)
    decal((sx, sy, 6.1), n, 4.8, 2.8, [(BRAND, .26, 1, RED, 1), (P["name"], .12, 1), (P["rating"], .1, 0, "#55595e"),
                                       ("WHERE OUR CABLE GOES", .085, 0, "#8a8f94", 1)], layer=layer)


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
    for sgn, s in ((-1, y0 - .02), (1, y1 + .02)):
        decal(((x0 + x1 - 9.6) / 2, s, 3.4), (0, sgn, 0), 18, 1.5,
              [(BRAND + "  SIMpull SOLUTIONS", .55, 1, "#ffffff", 1)], bg=None, brand=True)
        decal((x1 - 7.0, s, 4.4), (0, sgn, 0), 3.6, 2.6,
              [(BRAND, .3, 1, RED, 1), ("SIMpull", .26, 1, INK, 1), ("SOLUTIONS", .16, 0, "#555a5f", 1)],
              bg=None, brand=True)


def payoff_crew(x, y):
    import maintenance as mt
    mt.person(x - 2, y + 2.6, 0, -1.57)
    mt.person(x + 2.2, y - 2.6, 0, 1.57, vest="hivis_o")


# ---------------------------------------------------------------------------- spots
def reel_yard():
    """The drawn cable reel yard / outage laydown (x 40-320, y 690-900) as a stocked, branded reel yard with
    the SIMpull Truck unloading and the full product row of cutaway stands."""
    it = fuel.new_item("BASE_SERVICES", "Cable showcase: reel yard with SIMpull Truck and product row",
                       (44, 316, 694, 896), (0, 14), basis="typical", register=False, area="F",
                       sheet="typical (cable product showcase)",
                       info="Reel yard on the drawn laydown pad: branded wooden reels of the plant cable families "
                            "in rows (230 kV XLPE, MV-105, ARMOR-X MC-HL, Type TC-ER, instrumentation), the SIMpull "
                            "Truck unloading SIMpull Reels on payoffs, and a row of cutaway product stands. "
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
    # product row: every family, facing the aisle (south)
    for k, key in enumerate(("hv", "mv", "armorx", "tc", "inst", "thhn", "oh", "cu", "dc")):
        stand(70 + k * 8.4, 778, "-y", key)
    # yard sign at the aisle entrance
    for sx in (232, 252):
        rod((sx, 712, 0), (sx, 712, 12), .25, "steel", seg=8)
    box(230, 254, 711.8, 712.2, 6.5, 12.5, "sign")
    decal((242, 711.7, 9.5), (0, -1, 0), 23, 5.8,
          [(BRAND, .3, 1, RED, 1), ("CABLE REEL YARD", .16, 1), ("HV  |  MV  |  LV  |  CONTROL  |  BUILDING WIRE", .09, 0, "#555a5f")])
    return it


def spot_stands():
    """One cutaway stand at each application point (in the layer of the area it belongs to)."""
    spots = [
        ("BASE_ELECTRICAL", "tc", 487, 700, "+x", "R1 tray riser: Type TC-ER, control and instrumentation cable"),
        ("BASE_SWITCHYARD", "oh", 500, 205, "-y", "Switchyard: overhead conductor"),
        ("BASE_SWITCHYARD", "cu", 509, 205, "-y", "Switchyard: bare copper ground grid"),
        ("BASE_UTILITIES", "armorx", 1546, 1435, "-y", "Plant gas yard (Class I Div 2): ARMOR-X MC-HL"),
        ("OPT_BESS_ROUTES", "hv", 1769, 176, "-y", "BESS 230 kV cable termination: HV XLPE transmission cable"),
        ("OPT_BESS", "mv", 1617, 505, "-y", "BESS collection: MV-105"),
        ("OPT_MOD", "mv", 1932, 909, "-y", "Modular yard 13.8 kV collector: MV-105"),
        ("OPT_DC", "dc", 2688, 1002, "-x", "Data hall A gallery: MV-105 35 kV and Armorlite MC"),
    ]
    n = 0
    for (layer, key, x, y, face, name) in spots:
        it = fuel.new_item(layer, f"Cable showcase stand - {name}", (x - 3.5, x + 3.5, y - 3.5, y + 3.5), (0, 7.6),
                           basis="typical", register=False, sheet="typical (cable product showcase)",
                           info="Cutaway sample at the point of use: " + PRODUCTS[key]["name"] + ", " +
                                PRODUCTS[key]["rating"] + ". Cable supplier: Southwire (as requested).")
        fuel.G["cur"] = it
        stand(x, y, face, key)
        n += 1
    return n


def build():
    fuel.G.setdefault("decals", [])
    reel_yard()
    return dict(stands=spot_stands(), decals=len(fuel.G["decals"]))
