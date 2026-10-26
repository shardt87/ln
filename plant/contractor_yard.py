"""Contractor area on the reel / outage laydown pad (owner, Oct 26): the free south-east part of the pad, between the
prefab staging bay and the SIMpull staging (x 196-318, y 694-792), set up the way an electrical contractor runs a
cable job today:
- conduit material handling: two cantilever racks of 10 ft rigid (RMC) and PVC sticks, banded PVC bundles stacked on
  timber dunnage, HDPE innerduct reels, pallets of fittings, and a telehandler bringing a bundle in on its forks;
- a conduit bending and threading station on a work mat (hydraulic bender, threading machine, cut-off saw);
- cable laid out on the ground the way long pulls are prepared: MV cable in a figure-eight on a tarp (so it pays
  back out without twist), and a line of ground rollers carrying a pull from a reel roller toward the trench;
- a cut-to-length station: payoff reel, measuring counter and cutter on a long bench, cut lengths coiled on pallets
  and tagged by circuit;
- the supplier's job-site services point: a container office with the contractor solutions on its board (reels and
  cradles, pullers, cut-to-length, reel management and returns, pull planning, prefab assemblies);
- contemporary lighting: solar-hybrid LED light towers and LED balloon lights, on the area's spider box.
Typical, not engineered."""
import math

import fuel
from fuel import box, rod

BRAND = "SOUTHWIRE"


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a=0.0, vest="hivis", z=0.0):
    import maintenance
    maintenance.person(x, y, z, a, vest=vest)


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        if a != b:
            rod(a, b, r, c, seg=seg)


# ------------------------------------------------------------------------------------------ conduit handling
def cantilever_rack(x, y0, L, face=1):
    """Cantilever rack along y at x: uprights every 10 ft with four levels of arms reaching toward +x (face 1) or
    -x (face -1), loaded with 10 ft conduit sticks laid along y. Returns the parts count."""
    n = 0
    lv = (1.2, 3.2, 5.2, 7.2)
    k = int(L // 10)
    for i in range(k + 1):
        yy = y0 + i * L / k
        box(x - .3, x + .3, yy - .3, yy + .3, 0, 9.0, "safety")                       # upright
        box(x - .3 - face * 1.6, x + .3 - face * 1.6, yy - .25, yy + .25, 0, .4, "safety")   # base leg
        for z in lv:
            x1 = x + face * 3.6
            box(min(x, x1), max(x, x1), yy - .15, yy + .15, z - .3, z, "safety")       # arm
            rod((x1, yy, z), (x1, yy, z + .5), .08, "safety", seg=6)                   # arm stop
        n += 1
    stock = (("steel", .2, 11), ("pvc_grey", .24, 9), ("steel", .14, 14), ("pvc_grey", .3, 8))
    for (c, r, m), z in zip(stock, lv):
        for j in range(m):
            xx = x + face * (.5 + r + j * (2 * r + .02)) * (3.0 / max(3.0, m * (2 * r + .02)))
            for s in range(int(L // 10)):
                rod((xx, y0 + s * 10 + .1, z + r), (xx, y0 + s * 10 + 9.9, z + r), r, c, seg=8)
        n += 1
    return n


def pvc_bundles(x0, y0, nx, layers):
    """Banded 20 ft PVC bundles (along y) on timber dunnage, nx across, `layers` high."""
    z = 0.0
    for l in range(layers):
        for yy in (y0 + 2, y0 + 10, y0 + 18):
            box(x0 - .3, x0 + nx * 2.9, yy - .25, yy + .25, z, z + .35, "timber")      # dunnage
        z += .35
        for i in range(nx):
            bx = x0 + i * 2.9
            box(bx, bx + 2.6, y0, y0 + 20, z, z + 2.0, "pvc_grey")
            for yy in (y0 + 3, y0 + 10, y0 + 17):
                box(bx - .03, bx + 2.63, yy - .08, yy + .08, z - .02, z + 2.03, "steel_dark")   # bands
        z += 2.0
    return layers


def innerduct_reel(x, y):
    """HDPE innerduct reel (orange) on a reel stand, axis along x."""
    rod((x - 2.2, y, 0), (x - 2.2, y, 4.2), .15, "steel", seg=6)
    rod((x + 2.2, y, 0), (x + 2.2, y, 4.2), .15, "steel", seg=6)
    rod((x - 2.4, y, 4.0), (x + 2.4, y, 4.0), .12, "steel", seg=8)
    for s in (-1.7, 1.7):
        rod((x + s - .1, y, 4.0), (x + s + .1, y, 4.0), 3.8, "timber", seg=24)
    rod((x - 1.6, y, 4.0), (x + 1.6, y, 4.0), 3.2, "pvc_orange", seg=24)
    return 1


def fittings_pallet(x, y):
    box(x - 2, x + 2, y - 2, y + 2, 0, .5, "timber")
    box(x - 1.9, x + 1.9, y - 1.9, y + 1.9, .5, 3.6, "cab_in")
    return 1


def telehandler(x, y, a_deg=0.0):
    """Telehandler driving north (+y) with a PVC bundle on its forks; boom raised at the back of the cab."""
    box(x - 4, x + 4, y - 9, y + 9, 1.6, 4.4, "yellow")                                # chassis
    for sx in (-4.3, 3.7):
        for sy in (-6, 6):
            rod((x + sx, y + sy, 2.0), (x + sx + .6, y + sy, 2.0), 2.0, "tyre", seg=16)
    box(x - 4, x - 1, y - 2, y + 4, 4.4, 9.4, "yellow")                                # cab
    box(x - 4.05, x - .95, y - 1.8, y + 3.8, 5.6, 9.0, "glass")
    rod((x + 1.4, y - 7, 5.0), (x + 1.4, y + 13, 11.0), .9, "yellow", seg=10)          # boom
    box(x - 1.6, x + 4.4, y + 13, y + 13.6, 6.5, 12.0, "steel_dark")                   # carriage
    for s in (-.8, 3.6):
        box(x + s - .3, x + s + .3, y + 13.6, y + 19.5, 6.6, 6.9, "steel_dark")        # forks
    box(x - 1.4, x + 4.2, y + 13.8, y + 33.8, 6.9, 8.9, "pvc_grey")                    # 20 ft bundle
    for yy in (y + 17, y + 24, y + 31):
        box(x - 1.43, x + 4.23, yy - .08, yy + .08, 6.88, 8.93, "steel_dark")
    return 1


def bend_thread_station(x, y):
    """Hydraulic conduit bender and a threading machine on a rubber mat, a cut-off saw on its stand."""
    box(x - 6, x + 6, y - 4, y + 4, 0, .08, "mat")
    box(x - 5, x - 1, y - 1, y + 1, 0, 2.4, "steel_dark")                              # bender table
    rod((x - 3, y, 2.4), (x - 3, y, 3.4), 1.0, "red", seg=20)                          # bending shoe
    rod((x - 5.5, y + .6, 2.9), (x + 3.0, y + .6, 2.9), .2, "steel", seg=8)           # stick in the shoe
    box(x - 4.6, x - 3.6, y - 1.8, y - 1.0, 0, 1.6, "red")                             # pump
    box(x + 1, x + 5, y - 1, y + 1, 0, 2.6, "steel")                                   # threader stand
    box(x + 1.4, x + 3.4, y - .8, y + .8, 2.6, 4.0, "red")                             # threading machine
    rod((x + 3.4, y, 3.3), (x + 8.5, y, 3.3), .2, "steel", seg=8)
    box(x - 1, x + .8, y + 2.6, y + 3.6, 0, 2.6, "steel_dark")                         # saw stand
    rod((x - .1, y + 2.6, 3.0), (x - .1, y + 3.6, 3.0), .7, "sp_black", seg=16)
    person(x - 3.2, y - 2.6, math.pi / 2)
    person(x + 2.6, y + 2.4, -math.pi / 2, vest="hivis_o")
    return 1


# ------------------------------------------------------------------------------------------ cable on the ground
def figure_eight(cx, cy, R=9.0, turns=3, r=.32, c="cable_mv"):
    """Cable laid in a figure-eight on a tarp (the way a long pull is staged so it pays out without twist)."""
    box(cx - 2.3 * R, cx + 2.3 * R, cy - 1.25 * R, cy + 1.25 * R, 0, .04, "flag_blue")
    for t in range(turns):
        rr = R * (1 - .07 * t)
        pts = []
        for k in range(97):
            u = 2 * math.pi * k / 96
            x = cx + 2 * rr * math.sin(u)
            y = cy + rr * math.sin(2 * u)
            pts.append((x, y, .05 + r + t * 2 * r))
        poly(pts, r, c, seg=8)
    # the cable end tagged and capped, the tail leading to the pull
    rod((cx + 2 * R, cy, .05 + r), (cx + 2 * R + 6, cy + 1.5, .05 + r), r, c, seg=8)
    rod((cx + 2 * R + 6, cy + 1.5, .05 + r), (cx + 2 * R + 6.6, cy + 1.6, .05 + r), r + .06, "sp_black", seg=8)
    return 1


def roller_line(x0, x1, y, n, r=.28, c="cable_mv"):
    """Ground cable rollers along a pull line; the cable lies through them."""
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        box(x - .7, x + .7, y - 1.0, y + 1.0, 0, .25, "safety")
        for s in (-.9, .9):
            box(x - .12, x + .12, y + s - .1, y + s + .1, .25, 1.3, "safety")
        rod((x, y - .85, .95), (x, y + .85, .95), .3, "steel", seg=12)
    rod((x0, y, .95 + .3 + r), (x1, y, .95 + .3 + r), r, c, seg=8)
    return 1


def cut_to_length(x0, y):
    """Cut-to-length bench: payoff (reel roller) at the west end, measuring counter and cutter, coiled cut lengths on
    pallets with circuit tags."""
    import simpull
    simpull.reel_roller(x0 - 8, y, 30, 7.0, 4.4, "cable_tc", "TC-ER 600 V 3/C 4/0")
    box(x0, x0 + 30, y - 1.5, y + 1.5, 0, 3.0, "steel_dark")                            # bench
    box(x0 + .1, x0 + 29.9, y - 1.4, y + 1.4, 3.0, 3.2, "deck")
    rod((x0 - 8, y, 6.8), (x0 + 1, y, 3.6), .26, "cable_tc", seg=8)                    # cable onto the bench
    rod((x0 + 1, y, 3.5), (x0 + 24, y, 3.5), .26, "cable_tc", seg=8)
    box(x0 + 3, x0 + 5, y - 1.0, y + 1.0, 3.2, 5.0, "sp_yellow")                        # measuring counter
    box(x0 + 3.2, x0 + 4.8, y - 1.02, y - 1.0, 4.2, 4.8, "hmi")
    box(x0 + 22, x0 + 24, y - 1.0, y + 1.0, 3.2, 5.4, "red")                            # cutter
    decal((x0 + 15, y - 1.6, 1.8), (0, -1, 0), 12, 1.6, [("CUT-TO-LENGTH · TAGGED BY CIRCUIT", .5, 1, "#ffffff")], bg="#111111")
    for k in range(3):                                                                   # coiled cut lengths
        px, py = x0 + 6 + k * 9, y + 6
        box(px - 2.4, px + 2.4, py - 2.4, py + 2.4, 0, .5, "timber")
        for l in range(3):
            pts = [(px + 1.8 * math.cos(2 * math.pi * i / 24), py + 1.8 * math.sin(2 * math.pi * i / 24), .8 + l * .5) for i in range(25)]
            poly(pts, .25, ("cable_tc", "cable", "cable_inst")[k], seg=8)
        box(px + 1.8, px + 2.2, py - .3, py + .3, 1.4, 2.0, "white_truck")                 # circuit tag
    person(x0 + 6, y - 3, math.pi / 2)
    person(x0 + 23, y - 3, math.pi / 2, vest="hivis_o")
    return 1


# ------------------------------------------------------------------------------------------ services + lighting
def services_point(x, y):
    """Supplier job-site services office (20 ft container office, along y), with the contractor solutions board."""
    box(x - 4, x + 4, y - 10, y + 10, 0, 8.5, "white_truck")
    box(x - 4.05, x - 3.95, y - 6, y - 1, 3.4, 6.4, "glass")
    box(x - 4.05, x - 3.95, y + 1, y + 6, 3.4, 6.4, "glass")
    box(x - 4.05, x - 3.95, y + 7, y + 9.5, .3, 7.2, "door")
    box(x + 4, x + 5.2, y - 4, y - 1.6, 4.0, 6.0, "equip")                              # wall AC
    box(x - 6, x - 4, y + 6.5, y + 10.5, 0, .5, "timber")                               # step
    rows = [("CONTRACTOR SOLUTIONS ON SITE", .1, 1, "#e6b089"),
            ("SIMpull reels and cradles · paralleled, colour-coded", .062, 0, "#ffffff"),
            ("Maxis pullers, feeders and reel rollers", .062, 0, "#ffffff"),
            ("Cut-to-length, tagged by circuit", .062, 0, "#ffffff"),
            ("Reel management and reel returns", .062, 0, "#ffffff"),
            ("Pull planning: tension and sidewall pressure", .062, 0, "#ffffff"),
            ("Prefab: pre-terminated assemblies and harness kits", .062, 0, "#ffffff")]
    for sx in (-1, 1):
        rod((x - 8, y + sx * 6, 0), (x - 8, y + sx * 6, 10.5), .12, "steel", seg=6)
    decal((x - 8.1, y, 6.5), (-1, 0, 0), 12.0, 7.2, [(BRAND, .13, 1, "#e6b089", 1)] + rows, bg="#14171a", brand=True)
    decal((x - 8.1, y, 6.5), (-1, 0, 0), 12.0, 7.2, rows, bg="#14171a", generic_only=True)
    decal((x - 4.1, y - 3.5, 7.6), (-1, 0, 0), 7.0, .9, [(BRAND + " JOB-SITE SERVICES", .6, 1, "#ffffff", 1)], bg="#14171a", brand=True)
    decal((x - 4.1, y - 3.5, 7.6), (-1, 0, 0), 7.0, .9, [("JOB-SITE SERVICES", .6, 1, "#ffffff")], bg="#14171a", generic_only=True)
    box(x - 6.5, x - 5.5, y - 9.5, y - 7.5, 0, 3.2, "steel")                             # stand-up table, tablet
    box(x - 6.4, x - 5.6, y - 9.2, y - 7.8, 3.2, 3.3, "hmi")
    person(x - 7.5, y - 8.5, 0.0)
    return 1


def led_tower(x, y, face=0.0):
    """Solar-hybrid LED light tower: trailer with battery box, tilted solar array, mast with four LED panels."""
    box(x - 3, x + 3, y - 2.2, y + 2.2, 1.4, 4.2, "sp_black")
    rod((x - 1.2, y - 2.3, 1.2), (x - 1.2, y - 2.6, 1.2), 1.1, "tyre", seg=14)
    rod((x - 1.2, y + 2.3, 1.2), (x - 1.2, y + 2.6, 1.2), 1.1, "tyre", seg=14)
    rod((x + 3, y, 1.6), (x + 6, y, 1.6), .12, "steel", seg=6)                            # tongue
    box(x - 3.4, x + 1.8, y - 3.2, y + 3.2, 5.0, 5.2, "glass")                            # solar array (flat-ish)
    box(x - 3.4, x + 1.8, y - 3.2, y + 3.2, 4.9, 5.0, "steel")
    rod((x + 2.3, y, 4.2), (x + 2.3, y, 24.0), .22, "steel", seg=8)
    box(x + 2.0, x + 2.6, y - 2.6, y + 2.6, 23.6, 24.0, "steel")
    for s in (-1.9, -.65, .65, 1.9):
        box(x + 2.65, x + 2.95, y + s - .5, y + s + .5, 23.0, 24.6, "sp_black")
        box(x + 2.95, x + 3.0, y + s - .45, y + s + .45, 23.1, 24.5, "lamp")
    return 1


def balloon_light(x, y, h=11.0):
    for k in range(3):
        t = k * 2 * math.pi / 3
        rod((x + 1.5 * math.cos(t), y + 1.5 * math.sin(t), 0), (x, y, 3.0), .05, "steel", seg=6)
    rod((x, y, 3.0), (x, y, h), .07, "steel", seg=6)
    rod((x, y, h + .2), (x, y, h + 2.6), 1.3, "lamp_in", r2=1.1, seg=20)
    return 1


def build():
    import simpull
    it = fuel.new_item("BASE_SERVICES", "Contractor area: conduit handling, cable laid out, cut-to-length, job-site services, LED lighting",
                       (194, 320, 692, 796), (0, 26), basis="typical", register=False, area="F",
                       sheet="typical (cable installation)",
                       info="Electrical contractor's set-up on the laydown pad: cantilever racks of RMC and PVC conduit, banded "
                            "PVC bundles on dunnage, HDPE innerduct reels and fittings pallets with a telehandler; a bending and "
                            "threading station; MV cable laid in a figure-eight on a tarp and a pull on ground rollers; a "
                            "cut-to-length bench with tagged coils; the cable supplier's job-site services office (reels and "
                            "cradles, pullers, cut-to-length, reel management, pull planning, prefab assemblies); solar-hybrid "
                            "LED light towers and LED balloon lights on a spider box. Typical, not engineered.")
    fuel.on(it)
    fuel.D = True
    n = 0
    # conduit material handling (west part)
    n += cantilever_rack(199.0, 750.0, 40.0, face=1)
    n += cantilever_rack(217.0, 750.0, 40.0, face=-1)
    n += pvc_bundles(224.0, 700.0, 4, 3)
    for k in range(3):
        n += innerduct_reel(200.0 + k * 6.5, 704.0)
    for k in range(3):
        n += fittings_pallet(202.0 + k * 5.0, 718.0)
    n += telehandler(242.0, 726.0)
    n += bend_thread_station(232.0, 776.0)
    # cable laid out on the ground (east part)
    n += figure_eight(282.0, 712.0)
    n += roller_line(262.0, 312.0, 734.0, 9)
    simpull.reel_roller(256.0, 734.0, 45, 8.4, 5.0, "cable_mv", "MV-105 15 kV 500 KCMIL")
    person(300.0, 712.0, math.pi)
    person(306.0, 731.0, math.pi / 2, vest="hivis_o")
    # cut-to-length
    n += cut_to_length(264.0, 756.0)
    # job-site services point on the east edge
    n += services_point(312.0, 776.0)
    # lighting and its power: spider box, cords on grade, LED towers and balloon lights
    simpull.spider_box(258.0, 748.0)
    for p in ((259.0, 748.6, .9), (262.0, 750.0, .05), (262.0, 760.0, .05)), ((258.0, 747.4, .9), (258.0, 744.0, .05), (268.0, 744.0, .05)):
        poly(list(p), .08, "cable", seg=6)
    for x, y in ((196.5, 728.0), (312.0, 700.0), (250.0, 793.0)):
        n += led_tower(x, y)
    n += balloon_light(270.0, 768.0)
    n += balloon_light(268.0, 722.0)
    fuel.D = False
    return n
