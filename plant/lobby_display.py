"""Southwire product display in the control / admin building lobby (owner, Oct 26: the products shown in the
contractor area belong inside the admin building, like the supplier's trade-show install wall). A 25 ft display on
the lobby's east wall (inner face x 219.85, y 351-376.5), facing reception, under a header:
- wood-stud bay: plywood back, studs, plastic boxes wired with yellow, blue and red NM-B (SIMpull NM-B);
- metal-stud bay on block: steel studs, 4 in square boxes with mud rings, MC cable runs and a coil at the foot;
- cable sample shelves: short cut samples standing on two shelves with the copper ends up (MV-105, TC-ER, ARMOR-X
  MC-HL, PLTC, Cable-in-Conduit cut open, SIMpull THHN paralleled, Type W, SHD-GC), each with its label;
- tools bay: hand conduit benders on hooks, a circuit puller on a pedestal, a screen playing the plant model, a
  brochure rack.
Branded labels have generic twins (the generic viewer drops the brand lines). Typical, not engineered."""
import fuel
from fuel import box, rod

L_IN = "CR_INTERIOR"
WX = 219.85                       # east wall inner face of the lobby
BRAND = "SOUTHWIRE"


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def label(y, z, w, h, brand_lines, lines, bg="#14171a"):
    decal((WX - .62, y, z), (-1, 0, 0), w, h, brand_lines + lines, bg=bg, brand=True)
    decal((WX - .62, y, z), (-1, 0, 0), w, h, lines, bg=bg, generic_only=True)


def poly(pts, r, c, seg=6):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def wood_bay(y0, y1):
    box(WX - .5, WX - .35, y0, y1, 0, 9.5, "timber")                                     # plywood
    k = 0
    y = y0 + .2
    while y < y1 - .1:
        box(WX - .85, WX - .5, y, y + .15, 0, 9.5, "timber")                              # studs at 16 in
        y += 1.33
        k += 1
    box(WX - .85, WX - .5, y0, y1, 9.3, 9.5, "timber")
    box(WX - .85, WX - .5, y0, y1, 0, .2, "timber")
    for (yy, zz, c) in ((y0 + 1.0, 6.8, "sp_yellow"), (y0 + 3.4, 6.4, "pvc_blue"), (y0 + 4.4, 3.6, "red"), (y0 + 1.6, 3.0, "sp_yellow")):
        box(WX - 1.0, WX - .5, yy, yy + .45, zz, zz + .7, "pvc_grey")                      # plastic box
        poly([(WX - .8, yy + .22, zz + .7), (WX - .6, yy + .22, zz + 1.4), (WX - .6, yy + .7, 9.1)], .045, c)
    label((y0 + y1) / 2, 8.2, 3.6, 1.0, [(BRAND, .26, 1, "#e6b089", 1)], [("ROMEX SIMpull NM-B", .32, 1, "#ffffff"),
                                                                          ("easy to strip · fast installs", .2, 0, "#c9cdd0")])
    return 1


def metal_bay(y0, y1):
    box(WX - .5, WX - .3, y0, y1, 0, 9.5, "concrete")                                     # block back
    for k in range(4):
        y = y0 + .3 + k * (y1 - y0 - .6) / 3
        box(WX - .9, WX - .5, y, y + .12, 0, 9.5, "alu")                                  # steel studs
    box(WX - .9, WX - .5, y0, y1, 9.3, 9.45, "alu")
    for (yy, zz) in ((y0 + .8, 6.6), (y0 + 3.0, 5.0), (y0 + 4.6, 6.6), (y0 + 2.0, 2.8)):
        box(WX - 1.05, WX - .5, yy, yy + .55, zz, zz + .55, "steel")                      # 4 in box + ring
        box(WX - 1.08, WX - 1.05, yy + .08, yy + .47, zz + .08, zz + .47, "steel_dark")
        poly([(WX - .8, yy + .27, zz + .55), (WX - .65, yy + .7, zz + 1.4), (WX - .65, yy + 1.1, 9.1)], .055, "cable_mc")
    import math
    for k in range(3):                                                                     # MC coil at the foot
        pts = [(WX - 1.2 - k * .08, y0 + 4.2 + .8 * math.cos(2 * math.pi * i / 20), .9 + .8 * math.sin(2 * math.pi * i / 20)) for i in range(21)]
        poly(pts, .05, "cable_mc")
    label((y0 + y1) / 2, 8.2, 3.6, 1.0, [(BRAND, .26, 1, "#e6b089", 1)], [("MC CABLE · BOXES & RINGS", .3, 1, "#ffffff"),
                                                                          ("rough electrical components", .2, 0, "#c9cdd0")])
    return 1


SAMPLES = [("MV-105 15 kV", "cable_mv", .28), ("TC-ER 600 V", "cable_tc", .2), ("ARMOR-X MC-HL", "cable_armor", .26),
           ("PLTC", "cable_inst", .14), ("CABLE-IN-CONDUIT", "pvc_orange", .3), ("SIMpull THHN x4", "cable", .2),
           ("TYPE W", "cable", .24), ("SHD-GC", "cable_shd", .26)]


def sample_shelves(y0, y1):
    box(WX - .4, WX - .3, y0, y1, 0, 9.5, "sp_black")
    for z in (3.4, 6.0):
        box(WX - 1.9, WX - .4, y0 + .2, y1 - .2, z - .12, z, "deck")                      # shelf
        for s in (y0 + .3, y1 - .4):
            box(WX - 1.9, WX - .4, s, s + .1, z - .6, z - .12, "steel_dark")             # bracket
    for k, (name, col, r) in enumerate(SAMPLES):
        z0 = 3.4 if k < 4 else 6.0
        y = y0 + .8 + (k % 4) * (y1 - y0 - 1.4) / 3
        x = WX - 1.15
        rod((x, y, z0), (x, y, z0 + 1.2), r, col, seg=16)                                 # jacket
        if col == "pvc_orange":                                                          # CIC: conductors in the duct
            for j, (dx, dy, c) in enumerate(((-.09, -.06, "cable"), (.09, -.06, "red"), (0, .1, "pvc_blue"))):
                rod((x + dx, y + dy, z0 + 1.2), (x + dx, y + dy, z0 + 1.6), .07, c, seg=8)
        else:
            rod((x, y, z0 + 1.2), (x, y, z0 + 1.45), r * .55, "copper", seg=12)          # copper end
        decal((WX - 1.92, y, z0 - .3), (-1, 0, 0), 1.3, .3, [(name, .55, 1, "#111111")], bg="#ffffff")
    label((y0 + y1) / 2, 8.4, 4.4, 1.0, [(BRAND, .26, 1, "#e6b089", 1)], [("POWER GENERATION CABLE", .3, 1, "#ffffff"),
                                                                          ("grid to thermocouple", .2, 0, "#c9cdd0")])
    return 1


def tools_bay(y0, y1):
    import control_room as cr
    box(WX - .4, WX - .3, y0, y1, 0, 9.5, "sp_black")
    for k in range(3):                                                                    # hand benders on hooks
        y = y0 + .8 + k * .9
        rod((WX - .6, y, 7.6), (WX - .45, y, 7.6), .05, "steel", seg=6)
        rod((WX - .7, y, 7.5), (WX - .7, y, 3.8), .07, "steel", seg=6)
        rod((WX - .75, y - .25, 3.6), (WX - .75, y + .25, 3.6), .36, "red", seg=14)
    box(WX - 2.6, WX - 1.0, y0 + .6, y0 + 2.4, 0, 2.6, "sp_black")                        # pedestal
    box(WX - 2.4, WX - 1.2, y0 + .8, y0 + 2.2, 2.6, 3.4, "sp_yellow")                     # circuit puller body
    rod((WX - 1.8, y0 + 1.5, 3.4), (WX - 2.6, y0 + 1.5, 5.0), .08, "sp_black", seg=6)      # boom
    rod((WX - 2.6, y0 + 1.3, 5.0), (WX - 2.6, y0 + 1.7, 5.0), .25, "sp_yellow", seg=12)    # sheave
    box(WX - .5, WX - .3, y0 + 2.8, y1 - .4, 4.2, 7.0, "monitor")                         # screen with the model
    cr.screen((WX - .52, (y0 + 2.8 + y1 - .4) / 2, 5.6), (-1, 0, 0), y1 - y0 - 3.4, 2.6, "overview.png", emit=1.2)
    box(WX - 1.4, WX - .5, y1 - 1.6, y1 - .4, 0, 3.6, "steel_dark")                        # brochure rack
    for k in range(3):
        box(WX - 1.45, WX - 1.38, y1 - 1.5, y1 - .5, 1.0 + k * .9, 1.8 + k * .9, ("copper", "white_truck", "sp_black")[k])
    label((y0 + y1) / 2, 8.4, 4.4, 1.0, [(BRAND, .26, 1, "#e6b089", 1)], [("INSTALLED FASTER", .3, 1, "#ffffff"),
                                                                          ("benders · pullers · SIMpull", .2, 0, "#c9cdd0")])
    return 1


def build():
    it = fuel.new_item(L_IN, "Lobby display: cable and installation products (install wall, cable samples, tools)",
                       (215.5, 219.85, 350.5, 377.0), (0, 10.5), area="F", sheet="SW-3X1-12", register=False, basis="typical",
                       info="A trade-show style install wall on the lobby's east wall, facing reception: a wood-stud bay with "
                            "NM-B to plastic boxes, a metal-stud bay with MC cable to steel boxes, shelves of cut cable "
                            "samples (MV-105, TC-ER, ARMOR-X MC-HL, PLTC, Cable-in-Conduit, SIMpull THHN, Type W, SHD-GC), "
                            "conduit benders, a circuit puller, a screen with the plant model and a brochure rack. Typical.")
    fuel.on(it)
    fuel.D = True
    box(WX - .3, WX, 351.0, 376.5, 9.6, 10.6, "sp_black")                                  # header band
    decal((WX - .32, 363.75, 10.1), (-1, 0, 0), 25.0, .9, [(BRAND + "  ·  COMPLETE THE INSTALLATION", .62, 1, "#ffffff", 1)],
          bg="#14171a", brand=True)
    decal((WX - .32, 363.75, 10.1), (-1, 0, 0), 25.0, .9, [("CABLE AND INSTALLATION, GRID TO THERMOCOUPLE", .62, 1, "#ffffff")],
          bg="#14171a", generic_only=True)
    n = wood_bay(351.0, 357.0) + metal_bay(357.4, 363.4) + sample_shelves(363.8, 370.2) + tools_bay(370.6, 376.5)
    import control_room as cr
    cr.person_standing(214.6, 353.5, 0.3, shirt="shirt")                                    # a visitor at the wall
    fuel.D = False
    return n
