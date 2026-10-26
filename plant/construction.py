"""Zone 07 part 3: the construction compound and its temporary power (owner, Oct 19 / Oct 26). The phase-2 work (the
reserved phase-2 pad, the BTM campus build-out) is run from a fenced contractor compound in the free south-east
corner of the site, x 2090-2385, y 30-245, gated onto the 30 ft access road (y 270-300). The 230 kV underground cable
runs under the apron at y 262 (EL -3), clear of everything here.

The cable story is temporary power, built the way a contractor's electrician builds it:
- a temporary utility service: a 45 ft wood riser pole inside the south fence (crossarm, pin insulators, fused
  cutouts, arresters, riser conduit), a buried 15 kV temporary feeder to a 750 kVA pad-mount transformer
  (13.8 kV / 480Y-277 V), a 480 V temporary service switchboard with the meter and main, and a 500 kW standby
  diesel generator on a trailer with its transfer switch;
- the 480 V distribution laid out on the ground: Type W 4/0 portable power cable from the switchboard to spider boxes
  (50 A GFCI distribution boxes) at the trailers, the fab tent, the reel yard and the light towers, SOOW cords from the
  spider boxes into each load, yellow cable-protector ramps wherever a cord crosses a drive, and temporary power
  poles (meter base, panel, GFCI receptacles) at the laydown;
- the compound itself: field-office trailers (contractor, owner's engineer, safety / first aid) on blocking with
  steps, landings and wall air conditioners; crew parking; conex tool containers; a fabrication tent with welders;
  a cable reel yard for the phase-2 feeders; a double-wall diesel tank in containment; portable toilets, hand-wash
  station and roll-off dumpsters; four light towers; temporary chain-link fence with windscreen, a swing gate and
  the site signs.
Typical, not engineered. Not part of the permanent cable schedule (register=False)."""
import math

import fuel
from fuel import box, rod, new_item, on

X0, X1, Y0, Y1 = 2090.0, 2385.0, 30.0, 245.0             # compound fence line
GX0, GX1 = 2228.0, 2256.0                                  # gate opening on the north fence
PAD = 0.25                                                 # gravel top


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a=0.0, vest="hivis"):
    import maintenance
    maintenance.person(x, y, PAD, a, vest=vest)


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def cord(pts, r=.13, c="cable"):
    """A portable cord laid on the gravel, through the given plan points (slight sag between them)."""
    P = [(x, y, PAD + r) for k, (x, y) in enumerate(pts) if k == 0 or (x, y) != tuple(pts[k - 1])]
    poly(P, r, c, seg=8)
    return 1


def ramp(x, y, along_x, n=3):
    """Yellow cable-protector ramp across a drive (n channels); along_x: the cords run along x."""
    L, W = 3.0, 1.8
    for k in range(n):
        o = (k - (n - 1) / 2) * L
        if along_x:
            box(x - W / 2, x + W / 2, y + o - L / 2, y + o + L / 2, PAD, PAD + .25, "sp_yellow")
        else:
            box(x + o - L / 2, x + o + L / 2, y - W / 2, y + W / 2, PAD, PAD + .25, "sp_yellow")
    return 1


def sign(x, y, n, lines, w=6.0, h=3.6, z=5.0, bg="#ffffff"):
    rod((x - n[1] * w * .4, y + n[0] * w * .4, 0), (x - n[1] * w * .4, y + n[0] * w * .4, z + h / 2), .1, "steel", seg=6)
    rod((x + n[1] * w * .4, y - n[0] * w * .4, 0), (x + n[1] * w * .4, y - n[0] * w * .4, z + h / 2), .1, "steel", seg=6)
    decal((x + n[0] * .12, y + n[1] * .12, z), n, w, h, lines, bg=bg)
    return 1


# ------------------------------------------------------------------------------------------ the compound
def ground_fence_gate():
    n = 0
    box(X0, X1, Y0, Y1, 0, PAD, "gravel_yard")
    box(GX0, GX1, Y1, 268.0, 0, PAD, "gravel_yard")                          # apron to the access road
    # temporary chain-link: posts on stands every 10 ft, mesh, green windscreen on the lower 6 ft
    runs = [((X0, Y0), (X1, Y0)), ((X1, Y0), (X1, Y1)), ((X0, Y0), (X0, Y1)), ((X0, Y1), (GX0, Y1)), ((GX1, Y1), (X1, Y1))]
    for (ax, ay), (bx, by) in runs:
        L = math.hypot(bx - ax, by - ay)
        k = max(1, round(L / 10))
        for i in range(k + 1):
            px, py = ax + (bx - ax) * i / k, ay + (by - ay) * i / k
            box(px - .9, px + .9, py - .35, py + .35, PAD, PAD + .25, "concrete")         # stand
            rod((px, py, PAD), (px, py, 7.0), .07, "steel", seg=6)
            n += 1
        t = .03
        if ax == bx:
            box(ax - t, ax + t, ay, by, PAD + .3, 6.8, "fence")
            box(ax - t - .02, ax + t + .02, ay, by, PAD + .3, 6.2, "ccs_green")
        else:
            box(ax, bx, ay - t, ay + t, PAD + .3, 6.8, "fence")
            box(ax, bx, ay - t - .02, ay + t + .02, PAD + .3, 6.2, "ccs_green")
        rod((ax, ay, 6.9), (bx, by, 6.9), .05, "steel", seg=6)                          # top rail
    for gx, sx in ((GX0, 1), (GX1, -1)):                                                 # double swing gate, open
        rod((gx, Y1, 0), (gx, Y1, 7.4), .12, "steel", seg=8)
        box(gx, gx + sx * .1, Y1 - 13.5, Y1, PAD + .3, 6.8, "fence")
        rod((gx, Y1 - 13.5, PAD + .3), (gx, Y1 - 13.5, 6.8), .06, "steel", seg=6)
    n += sign(GX0 - 12, Y1 + 6, (0, 1, 0), [("CONSTRUCTION ENTRANCE", .2, 1, "#111111"), ("SW-3X1 PHASE 2", .15, 1, "#b4591f"),
                                            ("ALL VISITORS REPORT TO THE FIELD OFFICE", .1, 0, None),
                                            ("HARD HAT · SAFETY GLASSES · VEST · BOOTS", .1, 1, "#c8102e")], w=9.0, h=5.0, z=5.5)
    n += sign(GX1 + 10, Y1 + 6, (0, 1, 0), [("CAUTION", .24, 1, "#111111", False, "#f2c21b"), ("TEMPORARY POWER IN USE", .16, 1, None),
                                            ("480 V CORDS ON GRADE · USE THE RAMPS", .12, 0, None)], w=7.0, h=4.0, z=5.0)
    return n


def trailer(x0, y0, L, W, name, door_side="+y"):
    """Field-office trailer along x on blocking: skirting, skin, windows, door with steps and landing, wall AC units,
    a meter base / disconnect on the end wall fed by its cord. Returns the cord entry point."""
    zb = 2.6
    for i in range(int(L // 8) + 1):                                                    # blocking piers
        for yy in (y0 + 1, y0 + W - 1):
            box(x0 + i * L / (L // 8) - .6, x0 + i * L / (L // 8) + .6, yy - .6, yy + .6, PAD, zb, "concrete")
    box(x0, x0 + L, y0, y0 + W, zb - .1, zb + .5, "steel_dark")                         # frame
    box(x0 + .1, x0 + L - .1, y0 + .1, y0 + W - .1, PAD, zb, "steel_dark")              # skirting
    box(x0, x0 + L, y0, y0 + W, zb + .5, zb + 9.0, "white_truck")
    box(x0 - .1, x0 + L + .1, y0 - .1, y0 + W + .1, zb + 9.0, zb + 9.4, "steel")         # roof edge
    fy = y0 + W if door_side == "+y" else y0
    s = 1 if door_side == "+y" else -1
    for k in range(int(L // 10)):                                                        # windows
        wx = x0 + 4 + k * 10
        box(wx, wx + 4, fy - .05, fy + .05, zb + 4.0, zb + 7.0, "glass")
        box(wx, wx + 4, y0 + W - fy + y0 - .05, y0 + W - fy + y0 + .05, zb + 4.0, zb + 7.0, "glass")
    dx = x0 + L / 2
    box(dx - 1.6, dx + 1.6, fy - .05, fy + .05, zb + .6, zb + 7.3, "door")
    box(dx - 3, dx + 3, fy, fy + s * 5, zb - .2, zb + .5, "timber")                     # landing
    for k in range(4):                                                                   # steps
        box(dx - 2, dx + 2, fy + s * (5 + k), fy + s * (6 + k), PAD, zb - .2 - k * .6, "timber")
    for hx in (dx - 3, dx + 3):
        rod((hx, fy + s * 5, zb + .5), (hx, fy + s * 5, zb + 3.5), .08, "steel", seg=6)
        rod((hx, fy + s * 5, zb + 3.5), (hx, fy + s * 9, PAD + 3.0), .07, "steel", seg=6)
    for ax in (x0 + 6, x0 + L - 8):                                                      # wall AC units
        box(ax, ax + 2.4, y0 + W - fy + y0 - s * 1.4, y0 + W - fy + y0, zb + 4.5, zb + 6.3, "equip")
    # meter base / fused disconnect on the west end wall, cord whip down to grade
    box(x0 - .6, x0, y0 + 2, y0 + 3.6, zb + 2.0, zb + 4.6, "panel")
    rod((x0 - .3, y0 + 2.8, zb + 2.0), (x0 - .3, y0 + 2.8, PAD + .2), .1, "cable", seg=8)
    decal((x0 + L / 2, fy + s * .08, zb + 8.1), (0, s, 0), 14.0, 1.1, [(name, .7, 1, "#111111")], bg="#ffffff")
    return (x0 - .3, y0 + 2.8)


def spider(x, y):
    """Spider box: 50 A 480 V-208Y/120 GFCI distribution on skids, orange."""
    box(x - 1.2, x + 1.2, y - .8, y + .8, PAD, PAD + .3, "steel")
    box(x - 1.0, x + 1.0, y - .7, y + .7, PAD + .3, PAD + 2.4, "pvc_orange")
    for k in range(3):
        rod((x - .6 + k * .6, y - .75, PAD + 1.6), (x - .6 + k * .6, y - .95, PAD + 1.6), .12, "pvc_grey", seg=6)
    return (x, y)


def temp_pole(x, y, face=(0, -1, 0)):
    """Temporary power pole: 6x6 timber post with a meter base, a small panel and GFCI receptacles."""
    box(x - .25, x + .25, y - .25, y + .25, -3, 14, "timber")
    box(x - .9 + face[0] * .3, x + .9 + face[0] * .3, y - .9 + face[1] * .3, y + .9 + face[1] * .3, 7, 9.5, "panel")
    box(x - .6 + face[0] * .3, x + .6 + face[0] * .3, y - .6 + face[1] * .3, y + .6 + face[1] * .3, 4.4, 6.2, "pvc_grey")
    decal((x + face[0] * .9, y + face[1] * .9, 10.6), face, 2.0, 1.1, [("TEMP POWER", .3, 1, "#ffffff"), ("480 V", .26, 1, "#ffffff")],
          bg="#c8102e")
    return (x, y)


def light_tower(x, y):
    """Trailer light tower: trailer box with its genset, mast to ~25 ft, four LED heads."""
    for u in (-4, 4):
        for v in (-2.4, 2.4):
            box(x + u - .2, x + u + .2, y + v - .2, y + v + .2, PAD, 1.6, "steel")
    box(x - 4.5, x + 4.5, y - 2.4, y + 2.4, 1.6, 6.0, "safety")
    rod((x, y, 6.0), (x, y, 25.0), .25, "steel", seg=8)
    box(x - 3, x + 3, y - .2, y + .2, 24.6, 25.0, "steel")
    for u in (-2.4, -.8, .8, 2.4):
        box(x + u - .6, x + u + .6, y - .5, y + .5, 25.0, 26.2, "lamp")
    return (x, y)


def conex(x0, y0, L, col):
    box(x0, x0 + L, y0, y0 + 8, PAD, PAD + 8.5, col)
    for k in range(int(L // 2)):
        box(x0 + k * 2 + .9, x0 + k * 2 + 1.1, y0 - .06, y0 + 8.06, PAD + .4, PAD + 8.1, "steel_dark")
    box(x0 + L - .05, x0 + L + .05, y0 + .3, y0 + 7.7, PAD + .3, PAD + 8.2, "steel_dark")      # doors end
    return 1


def pickup(x, y, along_x=True, col="white_truck"):
    L, W = 19.0, 6.6
    if along_x:
        box(x - L / 2, x + L / 2, y - W / 2, y + W / 2, 1.3 + PAD, 3.6 + PAD, col)
        box(x - 1.5, x + 4.5, y - W / 2 + .2, y + W / 2 - .2, 3.6 + PAD, 6.2 + PAD, col)
        box(x - 1.4, x + 4.4, y - W / 2 + .15, y + W / 2 - .15, 4.4 + PAD, 5.9 + PAD, "glass")
        for u in (-6, 6):
            for v in (-W / 2 - .2, W / 2 - .2):
                rod((x + u, y + v, 1.3 + PAD), (x + u, y + v + .4, 1.3 + PAD), 1.3, "tyre", seg=12)
    else:
        box(x - W / 2, x + W / 2, y - L / 2, y + L / 2, 1.3 + PAD, 3.6 + PAD, col)
        box(x - W / 2 + .2, x + W / 2 - .2, y - 1.5, y + 4.5, 3.6 + PAD, 6.2 + PAD, col)
        box(x - W / 2 + .15, x + W / 2 - .15, y - 1.4, y + 4.4, 4.4 + PAD, 5.9 + PAD, "glass")
        for u in (-6, 6):
            for v in (-W / 2 - .2, W / 2 - .2):
                rod((x + v, y + u, 1.3 + PAD), (x + v + .4, y + u, 1.3 + PAD), 1.3, "tyre", seg=12)
    return 1


# ------------------------------------------------------------------------------------------ temporary power
def utility_service():
    """Riser pole inside the south site fence, buried 15 kV feeder north into the compound to the pad-mount."""
    px, py = 2122.0, 14.0
    rod((px, py, -6), (px, py, 45), .55, "timber", r2=.42, seg=12)
    box(px - 5, px + 5, py - .25, py + .25, 41.5, 42.2, "timber")                         # crossarm
    for u in (-4.2, 0, 4.2):
        rod((px + u, py, 42.2), (px + u, py, 43.4), .22, "insulator", seg=10)              # pin insulators
        rod((px + u, py, 43.6), (px + u * .3, py, 38.0), .05, "conductor", seg=6)          # jumpers down to the cutouts
    box(px - 3.5, px + 3.5, py - .2, py + .2, 37.0, 37.5, "timber")                       # cutout arm
    for u in (-2.5, 0, 2.5):
        rod((px + u, py - .3, 35.6), (px + u, py - .3, 37.0), .12, "insulator", seg=8)    # fused cutouts
        rod((px + u, py - .4, 33.6), (px + u, py - .4, 35.2), .16, "insulator", seg=8)    # arresters
        rod((px + u, py - .3, 35.6), (px + u * .2, py - .7, 31.0), .05, "conductor", seg=6)
    rod((px, py - .7, 31.0), (px, py - .7, 0), .22, "pvc_grey", seg=8)                     # riser conduit + MV cable
    box(px - .5, px + .5, py - 1.4, py - .2, 30.6, 31.6, "steel")                          # pothead / terminations
    rod((px - 6, py, 44.4), (px + 30, py, 44.4), .05, "conductor", seg=6)                  # overhead tap along the fence
    decal((px, py - .6, 9.0), (0, -1, 0), 1.6, 2.4, [("TEMP", .22, 1, "#111111"), ("SVC", .22, 1, "#111111"),
                                                     ("13.8 kV", .2, 1, "#c8102e")], bg="#f2c21b")
    # buried 15 kV temporary feeder (MV-105 in PVC conduit) north under the fence to the transformer: marker posts
    for yy in (22.0, 34.0, 46.0):
        rod((px, yy, 0), (px, yy, 3.2), .1, "safety", seg=6)
    return 1


def power_centre():
    """750 kVA pad-mount, 480 V temporary service switchboard, standby generator and ATS. Returns the board's
    output point (where the Type W cords leave)."""
    tx, ty = 2116.0, 62.0
    box(tx - 5, tx + 5, ty - 4.5, ty + 4.5, 0, .7, "concrete")                             # pad
    box(tx - 3.6, tx + 3.6, ty - 3.2, ty + 3.2, .7, 6.4, "xfmr")                            # pad-mount (pad green)
    for u in (-2.6, 2.6):
        box(tx + u - .6, tx + u + .6, ty + 3.2, ty + 3.5, 1.2, 5.6, "steel_dark")          # radiator fins
    decal((tx, ty - 3.28, 4.6), (0, -1, 0), 3.4, 1.6, [("750 kVA", .26, 1, "#111111"), ("13.8 kV - 480Y/277 V", .17, 0, None),
                                                       ("TEMPORARY SERVICE", .17, 1, "#c8102e")], bg="#ffffff")
    for u in (-3.5, 3.5):                                                                   # bollards
        rod((tx + u, ty - 5.5, 0), (tx + u, ty - 5.5, 4.0), .3, "safety", seg=10)
    # 480 V temporary service switchboard (NEMA 3R, meter + main + six feeder breakers) on a skid
    sx0, sx1, sy0, sy1 = 2128.0, 2142.0, 56.0, 61.0
    box(sx0 - .5, sx1 + .5, sy0 - .5, sy1 + .5, 0, .6, "concrete")
    box(sx0, sx1, sy0, sy1, .6, 8.2, "panel")
    for k in range(3):
        box(sx0 + .2 + k * 4.6, sx0 + 4.4 + k * 4.6, sy0 - .06, sy0, 1.2, 7.6, "door")
    box(sx0 + .5, sx0 + 1.5, sy0 - .2, sy0, 5.2, 6.4, "white_truck")                       # meter
    decal(((sx0 + sx1) / 2, sy0 - .12, 8.8), (0, -1, 0), 8.0, 1.0, [("TEMP SERVICE 480 V 1200 A", .6, 1, "#ffffff")], bg="#c8102e")
    rod((tx + 3.6, ty, 2.5), (sx0, ty - 3.5, 2.5), .45, "cable", seg=10)                  # secondary in flex conduit
    # standby: 500 kW diesel generator on a trailer, transfer switch on the board's end
    gx, gy = 2112.0, 88.0
    box(gx - 15, gx + 15, gy - 4.2, gy + 4.2, 1.6, 2.2, "steel")
    for u in (-6, -3):
        for v in (-4.4, 4.0):
            rod((gx + u, gy + v, 1.4 + PAD), (gx + u, gy + v + .4, 1.4 + PAD), 1.4, "tyre", seg=12)
    rod((gx + 15, gy, 2.0), (gx + 22, gy, 2.0), .18, "steel", seg=6)                       # tongue
    box(gx + 21.5, gx + 22.3, gy - .4, gy + .4, PAD, 2.0, "steel")                          # jack stand
    box(gx - 14, gx + 14, gy - 4, gy + 4, 2.2, 10.5, "gen_paint")
    for k in range(6):
        box(gx - 12 + k * 4, gx - 10 + k * 4, gy - 4.06, gy + 4.06, 4.0, 9.0, "louvre")
    rod((gx - 9, gy, 10.5), (gx - 9, gy, 13.5), .5, "stack", seg=12)                       # exhaust
    decal((gx, gy - 4.1, 9.6), (0, -1, 0), 10.0, 1.0, [("500 kW STANDBY · 480 V", .55, 1, "#111111")], bg="#ffffff")
    box(sx1 + .1, sx1 + 3.1, sy0, sy1, .6, 7.4, "panel")                                   # ATS
    cord([(gx + 14, gy - 2), (2140.0, gy - 2), (sx1 + 1.6, sy1 + 1.0)], r=.2, c="cable_shd")  # gen output (SHD-GC)
    return ((sx0 + sx1) / 2, sy1)


def distribution(out):
    """Type W 4/0 from the board to the spider boxes and poles; SOOW from them to the loads. Returns cord count."""
    n = 0
    ox, oy = out
    spiders = {"trailers": (2165.0, 182.0), "fab": (2160.0, 130.0), "reels": (2268.0, 70.0), "conex": (2250.0, 150.0)}
    for k in spiders.values():
        spider(*k)
    # Type W 4/0 home runs along the yard edges (a cord per spider), ramps where they cross the main drive (x 2228-2256)
    n += cord([(ox - 2, oy + .5), (ox - 2, 120.0), (2160.0, 120.0), (2160.0, 129.2)], r=.22)
    n += cord([(ox - 1, oy + .5), (ox - 1, 110.0), (2150.0, 110.0), (2150.0, 182.0), (2163.8, 182.0)], r=.22)
    n += cord([(ox, oy + .5), (ox, 66.0), (2266.8, 66.0), (2266.8, 69.2)], r=.22)
    n += cord([(ox + 1, oy + .5), (ox + 1, 100.0), (2250.0, 100.0), (2250.0, 149.2)], r=.22)
    n += ramp(2242.0, 66.0, True) + ramp(2242.0, 100.0, True)
    return n


def build():
    it = new_item("SITE", "Construction compound (phase 2): trailers, laydown, reel yard and temporary power",
                  [2085, 2390, 0, 270], [-6, 46], area="F", register=False,
                  info="Contractor compound for the phase-2 work (the reserved phase-2 pad, the BTM campus build-out): "
                       "field offices, crew parking, conex tool storage, a fab tent, a cable reel yard and a fuel tank, "
                       "all on temporary power: a 13.8 kV temporary utility service on a riser pole, a 750 kVA pad-mount, "
                       "a 480 V temporary switchboard with a 500 kW standby generator, Type W cords to GFCI spider boxes "
                       "and SOOW cords to every load, ramps at every drive. Typical, not engineered.")
    it["wiring"] = ["Temporary MV service: 15 kV MV-105 1/C 1/0 Cu in PVC conduit, riser pole to the pad-mount",
                    "Pad-mount to switchboard: 480 V 4 sets 600 kcmil Cu XHHW-2 in flexible conduit",
                    "Distribution on grade: Type W 4/0 4/C portable power cable to each spider box (Southwire)",
                    "Spider boxes to loads: SOOW 10/4 and 12/3 portable cords, GFCI protected (Southwire)",
                    "Standby generator: SHD-GC portable cable to the transfer switch",
                    "Light towers: own gensets, no cords; grounding: bare Cu to rods at the service, generator and poles"]
    on(it)
    fuel.D = True
    n = ground_fence_gate()
    utility_service()
    out = power_centre()
    n += distribution(out)
    # field-office trailers, west of the gate, doors facing the yard
    ent = [trailer(2098.0, 200.0, 60.0, 24.0, "CONTRACTOR FIELD OFFICE", "-y"),
           trailer(2166.0, 212.0, 50.0, 12.0, "OWNER'S ENGINEER", "-y"),
           trailer(2166.0, 186.0, 44.0, 12.0, "SAFETY · FIRST AID", "-y")]
    for ex, ey in ent:                                                                      # SOOW from the spider box
        n += cord([(2165.0, 181.2), (2165.0 if ex > 2150 else 2120.0, 181.2 if ex > 2150 else 196.0), (ex - 1.5, ey)], r=.09)
    # crew parking east of the gate
    for k in range(6):
        n += pickup(2272.0 + k * 17.0, 228.0, along_x=False, col="white_truck" if k % 3 else "truck")
    for k in range(4):
        n += pickup(2290.0 + k * 22.0, 196.0, along_x=True, col="white_truck")
    # conex tool containers on the east fence, spider box feeding them
    for k, col in enumerate(("steel_dark", "red", "steel_dark", "flag_blue")):
        n += conex(2300.0, 120.0 + k * 11.0, 40.0, col)
        n += cord([(2250.0, 150.8), (2298.0, 150.8), (2298.0, 124.0 + k * 11.0)], r=.08)
    # fab tent with welders on the 480 V spider box
    box(2104.0, 2144.0, 118.0, 148.0, PAD, PAD + .05, "concrete")
    for x in (2104.0, 2124.0, 2144.0):
        for y in (118.0, 148.0):
            rod((x, y, PAD), (x, y, 12.0), .15, "steel", seg=6)
    box(2103.5, 2144.5, 117.5, 148.5, 12.0, 12.4, "tent")
    for k in range(3):
        wx = 2112.0 + k * 9.0
        box(wx - 1.2, wx + 1.2, 140.0, 142.4, PAD, PAD + 2.8, "machine")                   # welder
        n += cord([(2160.0, 130.8), (2150.0, 136.0), (wx + 1.2, 141.2)], r=.08)
        box(wx - 3, wx + 3, 124.0, 128.0, PAD, PAD + 3.0, "steel")                           # weld table
        person(wx, 130.5, a=math.pi / 2)
    # cable reel yard for the phase-2 feeders (Southwire livery), temp pole at its corner
    import showcase
    reels = [("cable_mv", "MV-105 35 kV"), ("cable_mv", "MV-105 15 kV"), ("cable_tc", "TC-ER 600 V"),
             ("cable_inst", "PLTC instrumentation"), ("cable_armor", "ARMOR-X MC-HL"), ("cable_shd", "SHD-GC portable")]
    for r in range(3):
        for k in range(6):
            cab, prod = reels[(k + r * 2) % len(reels)]
            showcase.reel(2290.0 + k * 14.0, 50.0 + r * 18.0, 7.0 if cab == "cable_mv" else 5.5, 4.0, "x", cab, prod, z0=PAD)
    temp_pole(2272.0, 46.0, (0, 1, 0))
    n += cord([(2268.0, 69.2), (2272.0, 47.0)], r=.08)
    person(2300.0, 80.0, a=0.0)
    person(2304.0, 82.0, a=math.pi)
    # double-wall diesel tank in containment, toilets, wash station, roll-offs
    box(2186.0, 2206.0, 40.0, 54.0, PAD, PAD + 2.0, "concrete")
    rod((2189.0, 47.0, PAD + 4.0), (2203.0, 47.0, PAD + 4.0), 3.2, "tank", seg=24)
    decal((2196.0, 43.7, PAD + 4.0), (0, -1, 0), 6.0, 1.6, [("DIESEL", .4, 1, "#c8102e"), ("NO SMOKING", .26, 1, "#111111")], bg="#ffffff")
    for k in range(4):
        box(2190.0 + k * 5.0, 2193.8 + k * 5.0, 225.0, 229.0, PAD, PAD + 7.5, "ccs_green")   # portable toilets
    box(2212.0, 2215.0, 225.0, 228.0, PAD, PAD + 4.5, "white_truck")                         # hand-wash
    for k in range(2):
        box(2335.0 + k * 26.0, 2357.0 + k * 26.0, 34.0, 42.0, PAD, PAD + 6.0, "steel_dark")  # roll-offs
    # light towers at the corners of the work areas
    for x, y in ((2178.0, 108.0), (2288.0, 112.0), (2378.0, 70.0), (2210.0, 238.0)):
        light_tower(x, y)
    # people at the offices and the gate
    person(2196.0, 194.0, a=math.pi / 2)
    person(2240.0, 236.0, a=-math.pi / 2, vest="hivis_o")
    fuel.D = False
    return n
