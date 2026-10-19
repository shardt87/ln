"""Turbine hall exterior (user review: "the elevations look too plain", Oct 19). Brand once, design the rest:
- west gable, the face toward the laydown bay and the road: the one exterior sign, 100 x 50 ft over the door, the same printed graphic as inside
  the east end wall ("3x1 CCGT", copper rule, WIRE & CABLE PARTNER, Southwire logo); the generic build keeps plain
  "3x1 CCGT";
- no unit numbers (tried "GT 1-3" on the filter houses and "ST" on the wall, Oct 19: read as confusing, removed);
- the inside copper band carried outside at the same EL 64 round all four walls, black pilasters on the column lines
  (44 ft) and at the corners, a clerestory window strip under the eaves of both long walls, a black fascia along the
  gallery roof edge, intake louvres on the gallery wall at each GT bay, a black surround and two wall lights at the
  west equipment door;
- a Southwire SIMpull Truck backed up to the west door, tail lift toward the hall, two SIMpull Reels on board and a
  crew at the tail lift (replaces the generic flatbed there: user, Oct 19, "better for branding").
Every strip is cut back wherever something of another item stands within a few inches of the wall (pipes, trays,
risers, filter-house frames, inlet ducts), so nothing new touches the plant. The south pieces sit in their own
"Turbine hall south cladding ..." item and lift off with the cladding in the cutaway views."""
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

    def __init__(self, ax, v, s, skip):
        self.ax, self.v, self.s = ax, v, s
        lo, hi = (v, v + 1.0) if s > 0 else (v - 1.0, v)          # the slab a strip can occupy, plus margin
        self.obs = []
        for p in fuel.G["parts"]:
            if p["item"] in skip[0] or (p["item"] in skip[1] and p["color"] in ("hall", "roof")):
                continue
            b = _bb(p)
            if b and b[0][ax] < hi and b[1][ax] > lo:
                self.obs.append(b)

    def free(self, a0, a1, z0, z1):
        """Free sub-intervals of [a0, a1] along the face for a strip spanning z0..z1."""
        o = 1 - self.ax
        cuts = sorted((b[0][o] - PAD, b[1][o] + PAD) for b in self.obs
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


def hstrip(f, a0, a1, z0, z1, depth, color):
    return sum(f.put(p, q, z0, z1, depth, color) for p, q in f.free(a0, a1, z0, z1))


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
    a = new_item(lay, "Turbine hall exterior finish: copper band, black pilasters, clerestory, west-end sign",
                 [478, 1102, 402, 562], [0, 99], area=area,
                 info="Southwire copper band at EL 64, black pilasters on the column lines, clerestory glazing, "
                      "west-end sign and door surround. Typical, not engineered.")
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
    n += hstrip(W, 403, 424, *ZB, .45, "hero_accent") + hstrip(W, 526, 560, *ZB, .45, "hero_accent")   # stops at the sign
    n += hstrip(E, 403, 560, *ZB, .45, "hero_accent")
    # pilasters: north wall on every column line, corners of both gables
    for x in COLS[1:-1]:
        n += pilaster(N, x, 0, 98)
    for f in (W, E):
        n += pilaster(f, 557.0, 0, 98) + pilaster(f, 405.0, 60, 98)
    n += pilaster(N, 481.0, 0, 98) + pilaster(N, 1099.0, 0, 98)
    n += windows(N, 482, 1098)
    # west equipment door (y 440-480, EL 0-36): black surround and two wall lights
    box(479.1, 479.5, 438.5, 440.0, 0, 37.5, "hero_rail"); box(479.1, 479.5, 480.0, 481.5, 0, 37.5, "hero_rail")
    box(479.1, 479.5, 438.5, 481.5, 36.0, 37.5, "hero_rail")
    for y in (436.0, 484.0):
        box(479.3, 480.0, y - .6, y + .6, 39.0, 40.0, "panel"); box(479.2, 479.3, y - .5, y + .5, 39.1, 39.6, "lamp")
    n += 7
    fuel.D = False
    # the one exterior sign, on the west gable above the band (branded print + the plain twin for the generic build)
    # 100 x 50 ft over the door (y 425-525, EL 44-94), clear of the riser at y 527.5; the band stops at its edges
    showcase.decal((479.9, 475.0, 72.0), (-1, 0, 0), 92, 22, [("3x1 CCGT", .8, True, "#1d1f21")], bg=None,
                   generic_only=True)
    fuel.G.setdefault("decals", []).append(dict(c=[479.9, 475.0, 69.0], n=[-1, 0, 0], w=100.0, h=50.0, bg=None,
                                                lines=[], item=a["id"], layer=a["layer"], brand=1,
                                                img="hall_wall_sign.png", print=1))
    # south: upper wall over the gallery roof and the gallery's outer wall
    on(b)
    fuel.D = True
    n += hstrip(SU, 480, 1100, *ZB, .45, "hero_accent")
    for x in COLS[1:-1]:
        n += pilaster(SU, x, 60, 98) + pilaster(SG, x, 0, 56.5)
    n += pilaster(SU, 481.0, 60, 98) + pilaster(SU, 1099.0, 60, 98)
    n += pilaster(SG, 481.0, 0, 56.5) + pilaster(SG, 1099.0, 0, 56.5)
    n += pilaster(W, 371.0, 0, 56.5) + pilaster(E, 371.0, 0, 56.5)
    n += windows(SU, 482, 1098)
    n += hstrip(SG, 480, 1100, 56.5, 58.0, .35, "hero_rail")                    # gallery roof fascia
    for k in range(3):                                                           # intake louvres, each GT bay
        x0 = 694 + 160 * k
        for p, q in SG.free(x0, x0 + 30, 33.0, 43.0):
            n += SG.put(p, q, 33.0, 43.0, .4, "louvre") + SG.put(p, q, 32.6, 33.0, .5, "hall_steel")
    fuel.D = False
    n += simpull_delivery(lay, area)
    return n


def simpull_delivery(lay, area):
    """The SIMpull Truck (showcase.simpull_truck, cab east) built at the west door and mirrored in x, so its cab is
    to the west and the tail lift faces the door (y 440-480)."""
    import showcase
    import maintenance as mt
    x, y = 451.0, 460.0
    it = new_item(lay, "Cable delivery: SIMpull Truck at the turbine hall west door", [428, 472, 454, 466], [0, 12],
                  area=area, register=False, sheet="typical (cable installation)",
                  info="Southwire SIMpull Truck delivering SIMpull Reels to the turbine hall through the west "
                       "equipment door. Typical, not engineered.")
    on(it)
    P, D = fuel.G["parts"], fuel.G["decals"]
    p0, d0 = len(P), len(D)
    showcase.simpull_truck(x, y)
    for p in P[p0:]:                                       # mirror x about the truck centre
        if p["kind"] in ("box", "prism"):
            p["min"][0], p["max"][0] = 2 * x - p["max"][0], 2 * x - p["min"][0]
        if p["kind"] == "rod":
            p["a"][0], p["b"][0] = 2 * x - p["a"][0], 2 * x - p["b"][0]
        if "v" in p:
            for v in p["v"]:
                v[0] = 2 * x - v[0]
    for d in D[d0:]:
        d["c"][0] = round(2 * x - d["c"][0], 2)
        d["n"][0] = -d["n"][0]
    mt.person(x + 20.5, y - 5.2, 0, 3.14, vest="hivis_o")            # at the tail-lift controls
    mt.person(x + 22.0, y + 5.4, 0, 2.6)
    return len(P) - p0
