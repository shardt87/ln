"""The supplier's installation products in use in the admin building's open-office fit-out (owner, Oct 26: put the
products from the trade-show install wall into the unfinished construction zone in the office, not on a display).
Added to the fit-out that admin_wiring.py already stages (Maxis puller and feeder, SIMpull BARRELs, CoilPAK cart,
MC reel, wire wagon):
- a metal-stud partition being framed for two private offices (x 136, y 351-375): top and bottom track, studs at
  16 in, steel boxes with mud rings at receptacle and switch height, MC cable dropping from above into each box, the
  first drywall sheets on the far face;
- an EMT bending corner: a bundle of 10 ft EMT sticks on blocks, an electrician bending a stick with a hand bender,
  finished 90s and offsets stacked, a second bender leaning on the wall;
- a materials cart of rough-in components (boxes, rings, MC connectors), a parts-bin rack of fittings and supports,
  and a pallet of MC coils;
- receptacles on the new wall (three trimmed out with plates, two hanging on their pigtails, a GFCI), switches in,
  MC connectors at every box, box support brackets and cable support clips on the studs;
- junction boxes with blank covers above the ceiling where the MC home run splits to the drops, hung from the deck;
- a strut-trapeze run on threaded rod from beam clamps, carrying three EMT runs with couplings and strut straps.
NM-B is left out on purpose: it is not permitted in a noncombustible commercial building like this one, where MC
and wire in EMT are the norm. Typical, not engineered."""
import math

import fuel
from fuel import box, rod

L_IN = "CR_INTERIOR"
BRAND = "SOUTHWIRE"
PX = 136.0                         # the new partition's centre line (x)
PY0, PY1 = 351.0, 375.0
CEIL = 12.5


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a, z=0.0):
    import admin_wiring as aw
    aw.person(x, y, a, z=z)


def poly(pts, r, c, seg=6):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def partition():
    box(PX - .15, PX + .15, PY0, PY1, 0, .12, "alu")                                       # bottom track
    box(PX - .15, PX + .15, PY0, PY1, CEIL - .12, CEIL, "alu")                              # top track
    y = PY0
    while y <= PY1 + .01:
        box(PX - .15, PX + .15, y - .03, y + .03, .12, CEIL - .12, "alu")                   # studs at 16 in
        y += 1.333
    for (y0, y1, z0, z1) in ((PY0, PY0 + 4, 0, 8), (PY0 + 4, PY0 + 8, 0, 8), (PY0, PY0 + 4, 8, CEIL - .1)):
        box(PX + .15, PX + .2, y0 + .02, y1 - .02, z0 + .02, z1 - .02, "wall_in")           # first drywall sheets
    n = 0
    boxes = ((353.6, 1.5), (357.6, 4.0), (361.6, 1.5), (365.6, 1.5), (369.6, 4.0), (373.0, 1.5))
    for k, (yy, zz) in enumerate(boxes):
        box(PX - .5, PX - .15, yy - .2, yy + .2, zz - .2, zz + .2, "steel")                 # 4 in box
        box(PX - .55, PX - .5, yy - .16, yy + .16, zz - .16, zz + .16, "steel_dark")        # mud ring
        box(PX - .4, PX - .2, yy - .62, yy + .62, zz - .35, zz - .28, "steel")              # box support bracket, stud to stud
        poly([(PX - .3, yy + .1, zz + .2), (PX - .3, yy + .3, zz + 1.4), (PX - .3, yy + .3, CEIL + .3),
              (PX - .3, yy + .3, 14.6)], .055, "cable_mc")                                     # MC drop from the J-box above
        rod((PX - .3, yy + .1, zz + .2), (PX - .3, yy + .1, zz + .33), .085, "alu", seg=8)   # MC connector at the box
        for cz in (zz + 2.5, 7.5, 10.5):                                                     # support clips on the stud
            if cz > zz + 1.4:
                box(PX - .4, PX - .15, yy + .22, yy + .38, cz - .06, cz + .06, "steel_dark")
        if zz == 1.5:                                                                         # receptacles
            if k < 3:                                                                         # trimmed out: device + plate
                box(PX - .6, PX - .55, yy - .14, yy + .14, zz - .2, zz + .2, "white_truck")
                box(PX - .62, PX - .6, yy - .05, yy + .05, zz + .03, zz + .12, "sp_black")
                box(PX - .62, PX - .6, yy - .05, yy + .05, zz - .12, zz - .03, "sp_black")
            else:                                                                             # device hanging on pigtails
                poly([(PX - .55, yy - .05, zz + .1), (PX - .9, yy - .05, zz - .2), (PX - 1.0, yy - .05, zz - .6)], .015, "cable_tc", seg=4)
                poly([(PX - .55, yy + .05, zz + .1), (PX - .9, yy + .05, zz - .2), (PX - 1.0, yy + .05, zz - .6)], .015, "panel", seg=4)
                box(PX - 1.05, PX - .95, yy - .12, yy + .12, zz - 1.0, zz - .6, "white_truck" if k != 5 else "panel")   # GFCI on the last
        else:                                                                                 # switch boxes: device in, no plate yet
            box(PX - .58, PX - .55, yy - .06, yy + .06, zz - .14, zz + .14, "white_truck")
        n += 1
    # junction boxes above the ceiling where the MC home run splits to the drops, on box hangers off the deck
    for jy in (355.6, 363.6, 371.3):
        box(PX - .3, PX + .3, jy - .3, jy + .3, 14.4, 14.9, "steel")
        box(PX - .32, PX + .32, jy - .32, jy + .32, 14.35, 14.4, "steel_dark")               # blank cover (underside)
        rod((PX, jy, 14.9), (PX, jy, 17.7), .03, "steel", seg=4)                              # hanger rod to the deck
        box(PX - .12, PX + .12, jy - .12, jy + .12, 17.55, 17.7, "steel_dark")                # beam clamp
        poly([(PX, jy, 14.9), (PX + .2, jy, 15.4), (143.0, jy, 15.4), (143.4, 381.0, 15.4)], .06, "cable_mc")   # home run
    person(134.0, 366.5, 0.0)                                                                # fixing a box
    return n


def bending_corner():
    for x in (89.0, 97.0):
        box(x - .3, x + .3, 347.4, 349.4, 0, .35, "timber")                                 # blocks
    for k in range(12):
        y = 347.6 + (k % 6) * .3
        z = .45 + (k // 6) * .22
        rod((87.0, y, z), (97.0 + 1.0, y, z), .07, "steel", seg=8)                          # EMT sticks
    rod((89.0, 352.0, .12), (98.0, 352.0, .12), .07, "steel", seg=8)                        # the stick being bent
    rod((95.0, 352.0, .12), (95.0, 352.0 + 2.0, .12 + 1.6), .07, "steel", seg=8)
    rod((94.7, 352.0, .3), (95.3, 352.0, .3), .45, "red", seg=14)                           # bender shoe on the stick
    rod((95.0, 351.6, .5), (95.0, 349.6, 4.4), .07, "steel", seg=6)                         # handle
    person(95.6, 350.7, math.pi / 2)
    for k in range(3):                                                                       # finished 90s
        o = 355.0 + k * .4
        poly([(88.0, o, .1)] + [(88.0 + 1.5 * math.sin(t * math.pi / 12), o, .1 + 1.5 * (1 - math.cos(t * math.pi / 12)))
                                 for t in range(1, 7)] + [(89.5, o, 3.0)], .07, "steel", seg=8)
    for k in range(2):                                                                       # offsets
        o = 356.6 + k * .4
        poly([(86.0, o, .1), (88.5, o, .1), (89.2, o, .6), (92.0, o, .6)], .07, "steel", seg=8)
    for (ex, ey, ez) in ((89.5, 355.0, 3.0), (89.5, 355.4, 3.0), (89.5, 355.8, 3.0)):
        rod((ex, ey, ez - .1), (ex, ey, ez + .15), .11, "steel", seg=8)                     # set-screw connectors on the 90s
    rod((85.2, 358.5, .2), (85.2, 358.9, 4.2), .07, "steel", seg=6)                          # spare bender, leaning
    rod((85.2, 358.3, .3), (85.2, 358.9, .3), .4, "red", seg=14)
    decal((85.3, 358.6, 2.4), (1, 0, 0), 1.4, .45, [(BRAND, .5, 1, "#ffffff", 1)], bg="#c41f27", brand=True)
    return 1


def materials_cart(x, y):
    box(x - 2.2, x + 2.2, y - 1.2, y + 1.2, .5, .6, "steel")
    box(x - 2.2, x + 2.2, y - 1.2, y + 1.2, 2.2, 2.3, "steel")
    for (sx, sy) in ((-2.1, -1.1), (2.1, -1.1), (-2.1, 1.1), (2.1, 1.1)):
        rod((x + sx, y + sy, 0), (x + sx, y + sy, 2.3), .05, "steel", seg=6)
    for k in range(3):                                                                       # cartons
        bx = x - 1.8 + k * 1.3
        box(bx, bx + 1.1, y - .9, y + .9, .6, 1.5, "timber")
        box(bx, bx + 1.1, y - .9, y + .9, 2.3, 3.0 + (k % 2) * .4, "timber")
    rows = [("ROUGH ELECTRICAL COMPONENTS", .34, 1, "#111111"), ("boxes · rings · MC connectors", .26, 0, "#333333")]
    decal((x, y - 1.25, 1.1), (0, -1, 0), 3.8, .9, [(BRAND, .3, 1, "#b4591f", 1)] + rows, bg="#ffffff", brand=True)
    decal((x, y - 1.25, 1.1), (0, -1, 0), 3.8, .9, rows, bg="#ffffff", generic_only=True)
    return 1


def mc_pallet(x, y):
    box(x - 2, x + 2, y - 2, y + 2, 0, .45, "timber")
    for l in range(3):
        rod((x, y, .45 + l * .65), (x, y, 1.05 + l * .65), 1.6, "cable_mc", seg=20)
        rod((x, y, 1.05 + l * .65), (x, y, 1.07 + l * .65), .7, "sp_black", seg=14)
    return 1


def trapeze_run(x0, x1, ys):
    """Strut trapezes hung on threaded rod from beam clamps at the deck, carrying three EMT runs along y with set-screw
    couplings every 10 ft and strut straps at each trapeze."""
    for y in ys:
        for x in (x0, x1):
            box(x - .12, x + .12, y - .12, y + .12, 17.55, 17.7, "steel_dark")                # beam clamp
            rod((x, y, 14.2), (x, y, 17.55), .03, "steel", seg=4)                              # threaded rod
            rod((x, y, 14.15), (x, y, 14.25), .07, "steel", seg=6)                             # nut and washer
        box(x0 - .3, x1 + .3, y - .1, y + .1, 14.25, 14.45, "steel")                             # strut channel
    ems = [x0 + .5 + k * (x1 - x0 - 1.0) / 2 for k in range(3)]
    for ex in ems:
        rod((ex, ys[0] - 2.0, 14.58), (ex, ys[-1] + 2.0, 14.58), .1, "pipe", seg=10)            # EMT
        y = ys[0] - 2.0 + 10.0
        while y < ys[-1] + 2.0:
            rod((ex, y - .2, 14.58), (ex, y + .2, 14.58), .14, "steel", seg=10)                 # coupling
            y += 10.0
        for y in ys:
            box(ex - .16, ex + .16, y - .06, y + .06, 14.45, 14.74, "steel_dark")               # strut strap
    return 1


def fittings_bins(x, y):
    """Parts-bin rack on the cart's end: fittings and supports sorted for the crew."""
    box(x - 1.6, x + 1.6, y - .5, y + .5, 0, 5.2, "steel_dark")
    for r in range(4):
        for c in range(4):
            bx, bz = x - 1.4 + c * .75, .6 + r * 1.15
            box(bx, bx + .6, y - .55, y - .2, bz, bz + .45, ("sp_yellow", "pvc_blue", "red", "steel")[(r + c) % 4])
    rows = [("FITTINGS & SUPPORTS", .3, 1, "#111111"), ("MC / EMT connectors · couplings · straps · J-hooks · clamps · rod", .17, 0, "#333333")]
    decal((x, y - .58, 5.6), (0, -1, 0), 3.4, .9, [(BRAND, .26, 1, "#b4591f", 1)] + rows, bg="#ffffff", brand=True)
    decal((x, y - .58, 5.6), (0, -1, 0), 3.4, .9, rows, bg="#ffffff", generic_only=True)
    return 1


def build():
    it = fuel.new_item(L_IN, "Open-office fit-out: metal-stud partition with boxes and MC drops, EMT bending, rough-in materials",
                       (84.6, 143.8, 346.2, 377.7), (0, 15.6), area="F", sheet="SW-3X1-12", register=False, basis="typical",
                       info="Added to the open-office fit-out: a metal-stud partition being framed with steel boxes, mud rings "
                            "and MC drops; an EMT bending corner with a hand bender in use and finished bends; a cart of rough "
                            "electrical components; a pallet of MC coils. NM-B is not used: this is a noncombustible "
                            "commercial building (MC and wire in EMT). Typical, not engineered.")
    fuel.on(it)
    fuel.D = True
    n = partition() + bending_corner() + materials_cart(90.0, 363.0) + mc_pallet(140.5, 349.0)
    n += trapeze_run(141.2, 143.3, (352.0, 360.0, 368.0, 376.0)) + fittings_bins(90.0, 366.6)
    fuel.D = False
    return n
