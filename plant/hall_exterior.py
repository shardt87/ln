"""Turbine hall exterior (user review: "the elevations look too plain", Oct 19). Brand once, design the rest:
- west gable, the face toward the laydown bay and the road: the van livery below the band (copper chevrons
  at the north end by the riser, pointing at the door, and a plain black rectangle from the riser over the door to
  the SW corner; the gallery end stays plain), and "3x1 CCGT" in large black lettering over the door, the
  copper band running unbroken below it (the full Southwire graphic was tried here and taken off, Oct 19: it did not
  sit well on the facade; the SIMpull trailer at the door carries the Southwire call-out; the graphic stays inside on
  the east end wall);
- no unit numbers (tried "GT 1-3" on the filter houses and "ST" on the wall, Oct 19: read as confusing, removed);
- the inside copper band carried outside at the same EL 64 round all four walls, black pilasters on the column lines
  (44 ft) and at the corners, a clerestory window strip under the eaves of both long walls, a black fascia round the
  gallery roof edge, a black coping round the main roof edge, intake louvres on the gallery wall at each GT bay, the ST bay's gallery door (the GT bays had theirs) and black
  door ID signs GAS TURBINE 1 / 2 / 3 and STEAM TURBINE over the four gallery doors with the units painted large
  above them (GT1 / GT2 / GT3 / ST1, sign-wide, Barlow Condensed ExtraBold), a black surround and two wall lights at the
  west equipment door;
- a Southwire SIMpull tractor-trailer where the generic flatbed stood (same size and heading, cab north): four 10.5 ft
  steel reels, black flanges each filled by the copper Southwire meatball, red skirts with the SIMpull SOLUTIONS livery, crew at the tail, two more reels staged by the door, one standing, one laid flat (user, Oct 19, "better for branding").
Every strip is cut back wherever something of another item stands within a few inches of the wall (pipes, trays,
risers, filter-house frames, inlet ducts), so nothing new touches the plant. The south pieces sit in their own
"Turbine hall south cladding ..." item and lift off with the cladding in the cutaway views."""
import math
import os

import fuel
from fuel import box, find, new_item, on

COLS = [482 + 44 * k for k in range(15)]             # hall column lines (x)
ZB = (64.0, 65.6)                                    # copper band, same EL as inside
ZW = (86.0, 93.0)                                    # clerestory strip
PAD = .4


def _bb(p):
    if p["kind"] in ("box", "prism"):
        return p["min"], p["max"]
    if p["kind"] == "rod":
        r = max(p.get("r", 0), p.get("r2", 0))
        return ([min(p["a"][i], p["b"][i]) - r for i in range(3)], [max(p["a"][i], p["b"][i]) + r for i in range(3)])
    if "v" in p:
        return [min(v[i] for v in p["v"]) for i in range(3)], [max(v[i] for v in p["v"]) for i in range(3)]
    return None


class Face:
    """An exterior wall face: ax = 0 (x = v, runs along y) or 1 (y = v, runs along x); s = outward sign."""

    def __init__(self, ax, v, s, skip, wallc=("hall", "roof", "hall_steel")):
        self.ax, self.v, self.s = ax, v, s
        lo, hi = (v, v + 1.0) if s > 0 else (v - 1.0, v)          # the slab a strip can occupy, plus margin
        self.obs = []
        for p in fuel.G["parts"]:
            if p["item"] in skip[0] or (p["item"] in skip[1] and p["color"] in wallc):
                continue
            b = _bb(p)
            if b and b[0][ax] < hi and b[1][ax] > lo:
                self.obs.append(b)

    def free(self, a0, a1, z0, z1, pad=PAD):
        """Free sub-intervals of [a0, a1] along the face for a strip spanning z0..z1."""
        o = 1 - self.ax
        cuts = sorted((b[0][o] - pad, b[1][o] + pad) for b in self.obs
                      if b[0][2] < z1 + PAD and b[1][2] > z0 - PAD and b[0][o] < a1 and b[1][o] > a0)
        out, x = [], a0
        for c0, c1 in cuts:
            if c0 > x:
                out.append((x, c0))
            x = max(x, c1)
        if x < a1:
            out.append((x, a1))
        return [(p, q) for p, q in out if q - p > 1.0]

    def zfree(self, a0, a1, z0, z1):
        """Free z sub-intervals for a vertical strip a0..a1 along the face."""
        o = 1 - self.ax
        cuts = sorted((b[0][2] - PAD, b[1][2] + PAD) for b in self.obs
                      if b[0][o] < a1 + PAD and b[1][o] > a0 - PAD and b[0][2] < z1 and b[1][2] > z0)
        out, z = [], z0
        for c0, c1 in cuts:
            if c0 > z:
                out.append((z, c0))
            z = max(z, c1)
        if z < z1:
            out.append((z, z1))
        return [(p, q) for p, q in out if q - p > 1.5]

    def put(self, a0, a1, z0, z1, depth, color):
        n0, n1 = (self.v, self.v + depth) if self.s > 0 else (self.v - depth, self.v)
        if self.ax == 0:
            box(n0, n1, a0, a1, z0, z1, color)
        else:
            box(a0, a1, n0, n1, z0, z1, color)
        return 1


def hstrip(f, a0, a1, z0, z1, depth, color, pad=.05):
    """A horizontal band, fitted tight (pad) against whatever of another item stands at the wall."""
    return sum(f.put(p, q, z0, z1, depth, color) for p, q in f.free(a0, a1, z0, z1, pad))


def pilaster(f, a, z0, z1, w=2.0):
    return sum(f.put(a - w / 2, a + w / 2, p, q, .3, "hall_steel") for p, q in f.zfree(a - w / 2, a + w / 2, z0, z1))


def windows(f, a0, a1):
    """Clerestory: glazed bays between the pilasters, a black sill and head."""
    n = 0
    edges = [a0] + [c for c in COLS if a0 < c < a1] + [a1]
    for p, q in zip(edges, edges[1:]):
        for s0, s1 in f.free(p + 2.5, q - 2.5, ZW[0] - .5, ZW[1] + .5):
            n += f.put(s0, s1, ZW[0], ZW[1], .12, "window")
            n += f.put(s0, s1, ZW[0] - .5, ZW[0], .25, "hall_steel")
            n += f.put(s0, s1, ZW[1], ZW[1] + .5, .25, "hall_steel")
    return n


def build():
    import showcase
    hall = find("Common turbine hall")
    clad = find("Turbine hall south cladding")
    lay, area = hall["layer"], hall.get("area", "A")
    a = new_item(lay, "Turbine hall exterior finish: copper band, black pilasters, clerestory, west-end lettering",
                 [478, 1102, 402, 562], [0, 99], area=area,
                 info="Southwire copper band at EL 64, black pilasters on the column lines, clerestory glazing, "
                      "3x1 CCGT lettering on the west end and door surround. Typical, not engineered.")
    b = new_item(lay, "Turbine hall south cladding exterior: band, pilasters, clerestory, louvres",
                 [478, 1102, 368, 404], [0, 99], area=area,
                 info="South-wall copper band, pilasters, clerestory, gallery fascia and intake louvres; lifts off "
                      "with the south cladding in the cutaway views. Typical, not engineered.")
    mine = {a["id"], b["id"]}
    walls = {hall["id"], clad["id"]}
    sk = (mine, walls)
    W, E = Face(0, 480.0, -1, sk), Face(0, 1100.0, 1, sk)
    N, SU, SG = Face(1, 560.0, 1, sk), Face(1, 403.0, -1, sk), Face(1, 370.0, -1, sk)
    n = 0
    on(a)
    fuel.D = True
    # copper band, proud of the pilasters so it reads continuous
    n += hstrip(N, 480, 1100, *ZB, .45, "hero_accent")
    n += hstrip(W, 369.5, 560.5, *ZB, .45, "hero_accent")                       # wraps both corners, gallery end included
    n += hstrip(E, 369.5, 560.5, *ZB, .45, "hero_accent")
    # pilasters: north wall on every column line, corners of both gables
    for x in COLS[1:-1]:
        n += pilaster(N, x, 0, 98)
    for f in (W, E):
        n += pilaster(f, 559.15, 0, 98, w=2.3) + pilaster(f, 403.85, 66.4, 98, w=2.3)            # flush with the corners
    n += pilaster(N, 481.0, 0, 98) + pilaster(N, 1099.0, 0, 98)
    n += windows(N, 482, 1098)
    # black coping round the main roof edge, all four walls (the south one is in the cladding item below)
    n += hstrip(N, 480, 1100, 96.8, 98.2, .5, "hero_rail")
    n += hstrip(W, 402.5, 560.5, 96.8, 98.2, .5, "hero_rail") + hstrip(E, 402.5, 560.5, 96.8, 98.2, .5, "hero_rail")
    # west equipment door (y 440-480, EL 0-36): black surround and two wall lights
    box(479.1, 479.5, 438.5, 440.0, 0, 37.5, "hero_rail"); box(479.1, 479.5, 480.0, 481.5, 0, 37.5, "hero_rail")
    box(479.1, 479.5, 438.5, 481.5, 36.0, 37.5, "hero_rail")
    for y in (436.0, 484.0):
        box(479.3, 480.0, y - .6, y + .6, 39.0, 40.0, "panel"); box(479.2, 479.3, y - .5, y + .5, 39.1, 39.6, "lamp")
    n += 7
    fuel.D = False
    # the field-service van livery on the west gable below the band (blender/hall_sign.py: livery_west.png): copper
    # chevrons north of the door pointing at it, a Southwire-black field with the van's notched edge over the door to
    # the SW corner (the gallery's west end stays plain cladding: the black there was tried and taken off)
    fuel.G["decals"].append(dict(c=[479.93, 480.0, 31.9], n=[-1, 0, 0], w=152.0, h=63.8, bg=None, lines=[], item=a["id"],
                                 layer=a["layer"], brand=0, img="livery_west.png", print=1))
    # the chevrons upper legs carried on at their angle above the band, on the upper gable panel (EL 65.6-96.8, y 534-556; user, Oct 20)
    fuel.G["decals"].append(dict(c=[479.93, 545.0, 81.2], n=[-1, 0, 0], w=22.0, h=31.2, bg=None, lines=[], item=a["id"],
                                 layer=a["layer"], brand=0, img="livery_west_up.png", print=1))
    # 3x1 CCGT on the west gable, above the band and over the door (y 429-521, EL 69-91), clear of the riser at y 527.5
    fuel.G["decals"].append(dict(c=[479.9, 475.0, 80.0], n=[-1, 0, 0], w=92.0, h=22.0, bg=None, lines=[], item=a["id"],
                                 layer=a["layer"], brand=0, img="hall_west_lettering.png", print=1))   # Barlow, as inside
    # south: upper wall over the gallery roof and the gallery's outer wall
    on(b)
    fuel.D = True
    # the gallery rises to EL 66.4 (owner, Oct 20): the copper band runs round its top at the hall's EL 64, a black
    # coping above it, and the upper wall starts over the gallery roof
    n += hstrip(SG, 480, 1100, *ZB, .45, "hero_accent")
    for x in COLS[1:-1]:
        n += pilaster(SU, x, 66.4, 98) + pilaster(SG, x, 0, ZB[0])
    n += pilaster(SU, 481.0, 66.4, 98) + pilaster(SU, 1099.0, 66.4, 98)
    n += pilaster(SG, 481.0, 0, ZB[0]) + pilaster(SG, 1099.0, 0, ZB[0])
    n += pilaster(W, 370.85, 0, ZB[0], w=2.3) + pilaster(E, 370.85, 0, ZB[0], w=2.3)
    n += windows(SU, 482, 1098)
    n += hstrip(SG, 480, 1100, ZB[1], 66.6, .35, "hero_rail")                   # gallery roof coping
    n += hstrip(W, 369.6, 403, ZB[1], 66.6, .35, "hero_rail") + hstrip(E, 369.6, 403, ZB[1], 66.6, .35, "hero_rail")
    n += hstrip(SU, 480, 1100, 96.8, 98.2, .5, "hero_rail")                     # main roof coping, south
    for k in range(3):                                                           # intake louvres, each GT bay
        x0 = 694 + 160 * k
        for p, q in SG.free(x0, x0 + 30, 33.0, 43.0):
            n += SG.put(p, q, 33.0, 43.0, .4, "louvre") + SG.put(p, q, 32.6, 33.0, .5, "hall_steel")
    # the steam-turbine bay's gallery door (the GT bays have theirs at x 569 / 729 / 889): 14 x 16 ft, like them,
    # east of GSU-ST and clear of the deck stair inside, with its apron and wall light
    box(1078.0, 1092.0, 369.5, 371.5, 0, 16, "door")
    box(1077.0, 1093.0, 340.0, 366.0, 0, .3, "road")
    box(1084.2, 1085.8, 369.1, 369.8, 19.0, 20.4, "lamp")
    n += 3
    fuel.D = False
    # door ID signs over the four gallery doors, above the conduit run and the wall lights (EL 20.6-23)
    import showcase
    # and above each sign the unit painted large on the cladding, the sign's width, in the WIRE & CABLE PARTNER face
    # (Barlow Condensed ExtraBold), so the entrances read from far off. GT1 sits 1.6 ft east of its door's centre,
    # clear of the black pilaster on the door's west edge.
    from PIL import Image
    for xc, t, u in ((577.6, "GAS TURBINE 1", "GT1"), (736.0, "GAS TURBINE 2", "GT2"), (896.0, "GAS TURBINE 3", "GT3"),
                     (1085.0, "STEAM TURBINE", "ST1")):
        showcase.decal((xc, 369.45, 21.8), (0, -1, 0), 13.0, 2.4, [(t, .56, True, "#ffffff")], bg="#1d1f21")
        iw, ih = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens", f"door_{u}.png")).size
        h = round(13.0 * ih / iw, 2)
        fuel.G["decals"].append(dict(c=[xc, 369.45, round(24.0 + h / 2, 2)], n=[0, -1, 0], w=13.0, h=h, bg=None, lines=[],
                                     item=b["id"], layer=b["layer"], brand=0, img=f"door_{u}.png", print=1))
    n += simpull_delivery(lay, area)
    return n


def simpull_delivery(lay, area):
    """A Southwire SIMpull tractor-trailer where the generic flatbed stood (x 436-444, y 459-522, cab to the north):
    a white tractor with a Southwire-red stripe and logos on the doors, a 52 ft flatbed with red skirts and the
    SIMpull SOLUTIONS livery, four 10.5 ft steel reels with black flanges filled by the copper Southwire meatball, chocked across the deck
    (paralleled, colour-coded conductors), a crew at the tail."""
    import showcase
    import simpull
    import maintenance as mt
    from fuel import rod
    decal = showcase.decal

    def logo(c, n, w, img, aspect=4.03):
        """The Southwire logo as a printed image decal (brand only; 4:1, the meatball 1:1)."""
        fuel.G["decals"].append(dict(c=[round(v, 2) for v in c], n=list(n), w=w, h=round(w / aspect, 2), bg=None, lines=[],
                                     item=it["id"], layer=it["layer"], brand=1, img=img, print=1))
    xc, yt0, yt1 = 440.0, 459.0, 511.0                     # trailer deck (y 459-511), tractor y 511-522
    hw, zd = 4.25, 4.4                                     # half width, deck top
    it = new_item(lay, "Cable delivery: SIMpull tractor-trailer at the turbine hall west door",
                  [434, 446, 452, 523], [0, 16], area=area, register=False, sheet="typical (cable installation)",
                  info="Southwire SIMpull tractor-trailer delivering four steel reels of paralleled feeder conductors "
                       "to the turbine hall through the west equipment door. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    # trailer: deck, red skirts, rear bumper, landing gear, wheels (tandem at the rear)
    box(xc - hw, xc + hw, yt0, yt1, zd - .9, zd, "steel_dark")
    for s in (-1, 1):
        x0 = xc + s * hw
        box(min(x0, x0 + s * .15), max(x0, x0 + s * .15), yt0, yt1, zd - 2.6, zd, "sw_red")
        box(xc + s * 3.2 - .3, xc + s * 3.2 + .3, yt1 - 12.5, yt1 - 12.0, .4, zd - .9, "steel")       # landing gear
    box(xc - hw + .4, xc + hw - .4, yt0 - .5, yt0, 1.6, 2.4, "steel")
    for yw in (yt0 + 4.5, yt0 + 9.0):
        for s in (-1, 1):
            rod((xc + s * (hw - 1.3), yw, 1.7), (xc + s * (hw + .05), yw, 1.7), 1.7, "tyre", seg=16)
    n += 9
    # tractor: chassis, sleeper cab, hood, windscreen, red stripe, fifth wheel under the trailer nose, wheels
    yc0 = yt1 - 3.0
    box(xc - 1.8, xc + 1.8, yc0, yt1 + 11.0, 1.6, 3.0, "steel_dark")
    box(xc - 4.0, xc + 4.0, yt1 + .5, yt1 + 7.5, 3.0, 12.5, "white_truck")                      # sleeper + cab
    box(xc - 3.7, xc + 3.7, yt1 + 7.5, yt1 + 11.5, 3.0, 7.6, "white_truck")                     # hood
    box(xc - 3.4, xc + 3.4, yt1 + 7.45, yt1 + 7.55, 8.0, 11.6, "glass")                         # windscreen
    for s in (-1, 1):
        box(min(xc + s * 4.0, xc + s * 4.06), max(xc + s * 4.0, xc + s * 4.06), yt1 + 4.6, yt1 + 7.2, 8.4, 11.2, "glass")
        box(min(xc + s * 4.0, xc + s * 4.08), max(xc + s * 4.0, xc + s * 4.08), yt1 + .5, yt1 + 7.5, 4.6, 5.4, "sw_red")
        rod((xc + s * 4.3, yt1 + 1.0, 3.0), (xc + s * 4.3, yt1 + 1.0, 13.8), .28, "alu", seg=10)  # exhaust stacks
    box(xc - 3.8, xc + 3.8, yt1 + 11.5, yt1 + 12.0, 2.4, 6.4, "steel")                          # grille / bumper
    for yw in (yt1 - 1.5, yt1 + 2.5, yt1 + 9.5):
        for s in (-1, 1):
            rod((xc + s * (hw - 1.2), yw, 1.7), (xc + s * (hw + .05), yw, 1.7), 1.7, "tyre", seg=16)
    n += 20
    # four 10.5 ft steel reels, flanges painted black, each filled by the copper Southwire meatball, axles across the trailer,
    # on chocks (an oversize load, as the big feeder reels are)
    D, W = 10.5, 7.0
    R = D / 2
    for k in range(4):
        y = yt0 + 6.0 + k * 12.6
        zc = zd + .3 + R
        for s in (-1, 1):
            simpull.flange_disc((xc + s * (W / 2 - .3), y, zc), (s, 0, 0), R, .3, col="sp_black", spokes=12)
            logo((xc + s * (W / 2 + .2), y, zc), (s, 0, 0), 2 * R * .97, "sw_meatball.png", 1.0)   # the meatball fills the flange
        simpull.bands(lambda o, xx=xc, yy=y, zz=zc: (xx + o, yy, zz), W, R * .82, simpull.FEEDER * 2, t=.35)
        rod((xc - W / 2 + .3, y, zc), (xc + W / 2 - .3, y, zc), R * .3, "steel", seg=20)
        for sy in (-1, 1):
            box(xc - W / 2, xc + W / 2, y + sy * R * .62 - .4, y + sy * R * .62 + .4, zd, zd + .6, "sp_yellow")
        n += 6
    fuel.D = False
    # livery: Southwire logo and SIMpull SOLUTIONS on both red skirts, the solid-colour logo on the cab doors
    for s in (-1, 1):
        logo((xc + s * (hw + .17), yt0 + 9.0, zd - 1.3), (s, 0, 0), 8.0, "sw_logo_white.png")
        decal((xc + s * (hw + .17), yt0 + 31.0, zd - 1.3), (s, 0, 0), 26, 2.0,
              [("SIMpull SOLUTIONS", .62, 1, "#ffffff", 1)], bg=None, brand=True)
        logo((xc + s * 4.1, yt1 + 3.8, 6.9), (s, 0, 0), 5.6, "sw_logo_solid.png")
    mt.person(xc - 2.5, yt0 - 3.0, 0, -1.57, vest="hivis_o")              # crew at the tail, toward the door
    mt.person(xc + 3.0, yt0 - 2.2, 0, -1.2)
    mt.person(xc + 6.5, yt1 + 4.0, 0, 0.0)                                 # driver beside the cab
    # two reels already off the trailer, staged on the apron south of the door: one standing on chocks, flange to
    # the road, one laid flat with the meatball up (user, Oct 19)
    it = new_item(lay, "Cable reels staged at the turbine hall west door", [457, 475, 408, 436], [0, 10], area=area,
                  register=False, sheet="typical (cable installation)",
                  info="Two Southwire steel reels off the SIMpull trailer: one standing on chocks, one laid flat. "
                       "Typical, not engineered.")
    on(it)
    fuel.D = True
    D, W = 9.0, 5.6                                        # the staged reels stay 9 ft
    R = D / 2
    xs, ys, zc = 465.0, 428.5, R + .3                     # standing: axle along x, on chocks on the apron
    for s in (-1, 1):
        simpull.flange_disc((xs + s * (W / 2 - .3), ys, zc), (s, 0, 0), R, .3, col="sp_black", spokes=12)
        logo((xs + s * (W / 2 + .2), ys, zc), (s, 0, 0), 2 * R * .97, "sw_meatball.png", 1.0)
    simpull.bands(lambda o: (xs + o, ys, zc), W, R * .82, simpull.FEEDER * 2, t=.35)
    rod((xs - W / 2 + .3, ys, zc), (xs + W / 2 - .3, ys, zc), R * .3, "steel", seg=20)
    for sy in (-1, 1):
        box(xs - W / 2, xs + W / 2, ys + sy * R * .62 - .4, ys + sy * R * .62 + .4, 0, .6, "sp_yellow")
    xl, yl = 465.5, 415.5                                  # laid flat: axle vertical, bottom flange on timber dunnage
    for dy in (-2.2, 2.2):
        box(xl - R * .9, xl + R * .9, yl + dy - .35, yl + dy + .35, 0, .5, "timber")
    z0 = .5
    for zb in (z0, z0 + W - .3):
        rod((xl, yl, zb), (xl, yl, zb + .3), R, "sp_black", seg=40)                             # flanges
    for k in range(12):                                                                          # top-flange ribs
        t_ = 2 * math.pi * k / 12
        rod((xl + R * .32 * math.cos(t_), yl + R * .32 * math.sin(t_), z0 + W),
            (xl + R * .93 * math.cos(t_), yl + R * .93 * math.sin(t_), z0 + W), .07, "sp_black", seg=6)
    simpull.bands(lambda o: (xl, yl, z0 + W / 2 + o), W, R * .82, simpull.FEEDER * 2, t=.35)
    fuel.G["decals"].append(dict(c=[xl, yl, round(z0 + W + .12, 2)], n=[0, 0, 1], up=[-1, 0, 0], w=2 * R * .97,
                                 h=2 * R * .97, bg=None, lines=[], item=it["id"], layer=it["layer"], brand=1,
                                 img="sw_meatball.png", print=1))
    fuel.D = False
    return n + 12
