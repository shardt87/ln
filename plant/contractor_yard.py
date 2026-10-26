"""Contractor area on the reel / outage laydown pad (owner, Oct 26): the free south-east part of the pad, between the
prefab staging bay and the SIMpull staging (x 196-318, y 694-792), set up the way an electrical contractor runs a
cable job today:
- conduit material handling: two cantilever racks of 10 ft rigid (RMC) and PVC sticks, banded PVC bundles stacked on
  timber dunnage, HDPE innerduct reels, pallets of fittings;
- a conduit bending and threading station on a work mat (hydraulic bender, threading machine, cut-off saw);
- a SIMpull paralleled feeder pull: three SIMpull Reels on Cradles, twelve colour-coded conductors gathered into
  one pulling grip and swivel, the rope to a Maxis XD10 with a tension monitor; a line of ground rollers carrying an
  MV pull from a reel roller toward the trench; a reel-return station; pallets of armored MC coils;
- a cut-to-length station: payoff reel, measuring counter and cutter on a long bench, cut lengths coiled on pallets
  and tagged by circuit;
- the supplier's job-site services point: a container office with the contractor solutions on its board (reels and
  cradles, pullers, cut-to-length, reel management and returns, pull planning, prefab assemblies);
- temporary power and lighting from the supplier's own range: a 480 V Type W feed from the staging area's 480 V cart to a
  100 A power distribution box, 50 A boxes at each work area, extension-cord reels on the ground paying out to LED stand
  lights, and LED string lights on posts over the bench and the bending station.
Typical, not engineered."""
import math

import fuel

BRAND = "SOUTHWIRE"
Z = 0.3                                    # the laydown pad top: everything here stands on it


def box(x0, x1, y0, y1, z0, z1, c):
    fuel.box(x0, x1, y0, y1, z0 + Z, z1 + Z, c)


def rod(a, b, r, c, r2=None, seg=12):
    fuel.rod((a[0], a[1], a[2] + Z), (b[0], b[1], b[2] + Z), r, c, r2=r2, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a=0.0, vest="hivis", z=0.0):
    import maintenance
    maintenance.person(x, y, z + Z, a, vest=vest)


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
def paralleled_pull(y0=703.0):
    """SIMpull paralleled feeder pull: three SIMpull Reels on Cradles (four colour-coded conductors each) paying off
    side by side, the twelve conductors gathered into one pulling grip and swivel, and the rope to a Maxis XD10."""
    import simpull
    ys = [y0 + k * 7.5 for k in range(3)]
    jx, jy = 286.0, y0 + 7.5
    for y in ys:
        simpull.sp_reel(266.0, y, z0=Z, axis="y", cols=simpull.FEEDER[:4], label="SIMpull THHN  4 x 500 KCMIL")
        for k, c in enumerate(simpull.FEEDER[:4]):
            o = (k - 1.5) * .22
            a = (268.0, y + o, 3.1)
            b = (272.0, y + o, .25)
            m = (280.0, (y + jy) / 2 + o * .6, .25)
            e = (jx, jy + o * .4, .45)
            poly([a, b, m, e], .09, c, seg=6)
    rod((jx, jy, .45), (jx + 2.2, jy, .45), .42, "alu", r2=.16, seg=14)                 # pulling grip (basket)
    rod((jx + 2.2, jy, .45), (jx + 2.9, jy, .45), .14, "steel", seg=10)                 # swivel
    head = (299.2, jy, 5.7 + Z)
    fuel.rod((jx + 2.9, jy, .45 + Z), head, .06, "sp_yellow", seg=6)                     # pulling rope to the boom sheave
    fuel.rod(head, (301.5, jy, 2.5 + Z), .06, "sp_yellow", seg=6)                        # down to the capstan
    simpull.maxis_xd10(302.0, jy, math.pi, boom_deg=48)
    simpull.tension_monitor(305.0, jy + 3.0)
    rows = [("PARALLELED FEEDER PULL", .2, 1, "#111111"), ("3 SIMpull reels · 12 conductors · one pull", .14, 0, None),
            ("tension monitored", .12, 0, None)]
    sx_, sy_ = 276.0, y0 - 4.0
    rod((sx_ - 2.4, sy_, 0), (sx_ - 2.4, sy_, 5.0), .08, "steel", seg=6)
    rod((sx_ + 2.4, sy_, 0), (sx_ + 2.4, sy_, 5.0), .08, "steel", seg=6)
    decal((sx_, sy_ - .1, 4.0 + Z), (0, -1, 0), 6.0, 2.4, [(BRAND, .16, 1, "#b4591f", 1)] + rows, bg="#ffffff", brand=True)
    decal((sx_, sy_ - .1, 4.0 + Z), (0, -1, 0), 6.0, 2.4, rows, bg="#ffffff", generic_only=True)
    person(292.0, jy - 3.0, math.pi / 2)
    person(304.0, jy - 3.5, math.pi / 2, vest="hivis_o")
    return 1


def reel_return(x, y):
    """Empty reels laid flat in two stacks for the supplier's reel-return pickup, with the sign."""
    for k in range(2):
        cx = x + k * 7.0
        for l in range(3):
            z = l * 2.4
            rod((cx, y, z), (cx, y, z + .25), 2.7, "timber", seg=24)                         # bottom flange
            rod((cx, y, z + .25), (cx, y, z + 2.0), 1.1, "timber", seg=18)                   # drum
            rod((cx, y, z + 2.0), (cx, y, z + 2.25), 2.7, "timber", seg=24)                  # top flange
    rows = [("REEL RETURN", .3, 1, "#111111"), ("empty reels · scheduled pickup", .18, 0, None)]
    rod((x + 11.0, y - 1.2, 0), (x + 11.0, y - 1.2, 5.0), .08, "steel", seg=6)
    rod((x + 11.0, y + 1.2, 0), (x + 11.0, y + 1.2, 5.0), .08, "steel", seg=6)
    decal((x + 11.1, y, 4.2 + Z), (1, 0, 0), 4.0, 1.8, [(BRAND, .22, 1, "#b4591f", 1)] + rows, bg="#ffffff", brand=True)
    decal((x + 11.1, y, 4.2 + Z), (1, 0, 0), 4.0, 1.8, rows, bg="#ffffff", generic_only=True)
    return 1


def mc_pallets(x, y):
    """Two pallets of armored MC cable coils, shrink-wrapped, tagged."""
    for k in range(2):
        px = x + k * 5.0
        box(px - 2, px + 2, y - 2, y + 2, 0, .5, "timber")
        for l in range(3):
            rod((px, y, .5 + l * .7), (px, y, 1.15 + l * .7), 1.6, "cable_mc", seg=20)
            rod((px, y, 1.15 + l * .7), (px, y, 1.17 + l * .7), .7, "sp_black", seg=14)
        box(px + 1.6, px + 2.0, y - .3, y + .3, 1.2, 1.8, "white_truck")                       # tag
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


def sw_power_box(x, y, label="TEMPORARY POWER", big=False):
    """Southwire temporary power distribution box (yellow, on skids): 50 A (or 100 A) input, GFCI 120 V and 240 V
    outlets on the faces; branded label with its generic twin."""
    w, d, h = (2.6, 1.8, 2.6) if big else (1.9, 1.3, 2.0)
    for sy in (-d / 2 + .15, d / 2 - .15):
        box(x - w / 2 - .2, x + w / 2 + .2, y + sy - .12, y + sy + .12, 0, .3, "steel_dark")      # skids
    box(x - w / 2, x + w / 2, y - d / 2, y + d / 2, .3, .3 + h, "sp_yellow")
    box(x - w / 2 + .1, x + w / 2 - .1, y - d / 2 + .1, y + d / 2 - .1, .3 + h, .45 + h, "sp_yellow")
    for k in range(4 if big else 3):                                                     # outlets
        ox = x - w / 2 + .45 + k * (w - .9) / max(1, (3 if big else 2))
        box(ox - .17, ox + .17, y - d / 2 - .04, y - d / 2, .9, 1.4, "sp_black")
        box(ox - .17, ox + .17, y + d / 2, y + d / 2 + .04, .9, 1.4, "sp_black")
    rod((x - w / 2 - .3, y, .3 + h * .8), (x + w / 2 + .3, y, .3 + h * .8), .06, "sp_black", seg=6)   # lift handle
    zc = Z + .3 + h * .62
    decal((x, y - d / 2 - .06, zc), (0, -1, 0), w * .9, .7, [(BRAND, .4, 1, "#111111", 1), (label, .26, 1, "#111111")],
          bg="#f2c21b", brand=True)
    decal((x, y - d / 2 - .06, zc), (0, -1, 0), w * .9, .7, [(label, .4, 1, "#111111")], bg="#f2c21b", generic_only=True)
    return (x, y + d / 2)


def cord_reel(x, y, out_pts, col="sp_yellow", axis="x"):
    """Extension-cord reel standing on the ground (steel frame, drum with the cord wound on it), its cord paid out on
    the ground through out_pts to the load."""
    ax = (1, 0) if axis == "x" else (0, 1)
    for s_ in (-.7, .7):
        px, py = x + ax[0] * s_, y + ax[1] * s_
        rod((px - ax[1] * .9, py - ax[0] * .9, 0), (px, py, 1.9), .05, "steel_dark", seg=6)
        rod((px + ax[1] * .9, py + ax[0] * .9, 0), (px, py, 1.9), .05, "steel_dark", seg=6)
    rod((x - ax[0] * .8, y - ax[1] * .8, 1.3), (x + ax[0] * .8, y + ax[1] * .8, 1.3), .9, "sp_black", seg=18)   # flanges
    rod((x - ax[0] * .6, y - ax[1] * .6, 1.3), (x + ax[0] * .6, y + ax[1] * .6, 1.3), .78, col, seg=18)        # wound cord
    rod((x, y, 2.2), (x + ax[0] * .1, y + ax[1] * .1, 2.9), .05, "steel_dark", seg=6)                          # handle
    pts = [(x, y, 1.3 - .78)] + [(p[0], p[1], .06) for p in out_pts]
    poly([(a, b, c + 0) for a, b, c in pts], .07, col, seg=6)
    return 1


def led_stand_light(x, y, h=10.0, heads=2):
    """Southwire LED stand light: tripod, telescoping mast, one or two LED panel heads, cord down the mast."""
    for k in range(3):
        t = k * 2 * math.pi / 3 + .3
        rod((x + 1.7 * math.cos(t), y + 1.7 * math.sin(t), 0), (x, y, 2.8), .05, "sp_black", seg=6)
    rod((x, y, 2.8), (x, y, h - .4), .08, "sp_black", seg=6)
    rod((x, y, h - .4), (x, y, h), .05, "steel", seg=6)
    for k in range(heads):
        hx = x + (k - (heads - 1) / 2) * 1.4
        rod((x, y, h), (hx, y, h), .05, "sp_black", seg=6)
        box(hx - .55, hx + .55, y - .18, y + .18, h - .2, h + .75, "sp_yellow")
        box(hx - .5, hx + .5, y - .2, y - .18, h - .15, h + .7, "lamp")
    return (x, y)


def string_lights(pts, h=9.0, step=6.0):
    """Southwire LED string lights hung between posts over a work area: timber posts, the string sagging between them,
    LED bulbs every few feet in cages."""
    for (x, y) in pts:
        box(x - .2, x + .2, y - .2, y + .2, 0, h + .4, "timber")
        box(x - .7, x + .7, y - .7, y + .7, 0, .25, "concrete")                    # weighted base
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        n = max(2, int(L // step))
        prev = None
        for i in range(n + 1):
            t = i / n
            z = h - 1.2 * 4 * t * (1 - t)                                            # sag
            p = (ax + (bx - ax) * t, ay + (by - ay) * t, z)
            if prev:
                rod(prev, p, .03, "sp_black", seg=4)
            if 0 < i < n:
                rod((p[0], p[1], z - .1), (p[0], p[1], z - .55), .2, "lamp", r2=.12, seg=10)
            prev = p
    return 1


def build():
    import simpull
    it = fuel.new_item("BASE_SERVICES", "Contractor area: conduit handling, cable laid out, cut-to-length, job-site services, LED lighting",
                       (194, 320, 692, 796), (0, 26), basis="typical", register=False, area="F",
                       sheet="typical (cable installation)",
                       info="Electrical contractor's set-up on the laydown pad: cantilever racks of RMC and PVC conduit, banded "
                            "PVC bundles on dunnage, HDPE innerduct reels and fittings pallets; a bending and "
                            "threading station; a SIMpull paralleled feeder pull (three reels, one grip, Maxis XD10), an MV pull on ground rollers, reel return, MC coils; a "
                            "cut-to-length bench with tagged coils; the cable supplier's job-site services office (reels and "
                            "cradles, pullers, cut-to-length, reel management, pull planning, prefab assemblies); "
                            "temporary power: power distribution boxes, cord reels on the ground, LED stand lights and LED string lights. Typical, not engineered.")
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
    n += bend_thread_station(232.0, 776.0)
    # cable laid out on the ground (east part)
    n += paralleled_pull()
    n += reel_return(296.0, 697.5)
    n += mc_pallets(250.0, 698.0)
    n += roller_line(262.0, 312.0, 734.0, 9)
    simpull.reel_roller(256.0, 734.0, 45, 8.4, 5.0, "cable_mv", "MV-105 15 kV 500 KCMIL")
    person(306.0, 731.0, math.pi / 2, vest="hivis_o")
    # cut-to-length
    n += cut_to_length(264.0, 756.0)
    # job-site services point on the east edge
    n += services_point(312.0, 776.0)
    # temporary power and lighting, all Southwire: a 480 V feed in Type W from the staging area's 480 V cart, a 100 A
    # power distribution box, 50 A boxes at each work area, cord reels on the ground paying out to LED stand lights and
    # LED string lights
    poly([(242.0, 882.1, .1), (246.0, 878.0, .1), (246.0, 803.0, .1), (252.0, 797.0, .1), (252.0, 768.0, .1), (251.6, 767.0, .1)],
         .2, "cable_shd", seg=8)
    BX, BY = 250.5, 766.0
    sw_power_box(BX, BY, "TEMPORARY POWER 480 V / 100 A", big=True)
    boxes = {"cut": (266.0, 767.6), "rollers": (258.0, 728.0), "bend": (244.0, 768.0), "office": (300.0, 768.0)}
    for k, (bx, by) in boxes.items():
        sw_power_box(bx, by, "TEMPORARY POWER")
    # 6 AWG cords from the big box to each small box, on the ground
    for (bx, by) in boxes.values():
        poly([(BX, BY - .9, .1), (BX, (BY + by) / 2, .08), (bx, (BY + by) / 2, .08), (bx, by - .7, .1)], .1, "cable", seg=6)
    # cord reels on the ground from the boxes to the lights
    lights = [((272.0, 772.0), "cut"), ((288.0, 772.0), "cut"), ((270.0, 726.0), "rollers"), ((300.0, 740.0), "rollers"),
              ((236.0, 782.0), "bend"), ((228.0, 770.0), "bend"), ((306.0, 762.0), "office")]
    for k, ((lx, ly), src) in enumerate(lights):
        bx, by = boxes[src]
        rx, ry = bx + (lx - bx) * .35, by + (ly - by) * .35 + .9
        cord_reel(rx, ry, [(lx, ly)], col=("sp_yellow", "pvc_orange")[k % 2])
        poly([(bx, by + .7, .9), (rx, ry - .6, .1), (rx, ry, .5)], .06, "sp_yellow", seg=6)
        led_stand_light(lx, ly, heads=2 if k % 3 else 1)
    string_lights([(262.0, 752.0), (277.0, 752.0), (292.0, 752.0)])                  # over the cut-to-length bench
    string_lights([(224.0, 771.0), (232.0, 785.0), (240.0, 771.0)])                   # over the bending station
    fuel.D = False
    return n
