"""Switchgear rooms at LOD 3: R1 (SK-3X1-05) and the R4 ACC VFD e-house (SK-3X1-03, -11 view B2).

The lineups keep their drawn footprints and heights; the plain cabinet boxes get the fronts a
switchgear room actually shows:
- 15 kV / 5 kV metal-clad switchgear (36 in two-high cubicles): breaker door with viewing window,
  racking port and handle, relay / instrument door with protective relay, meter, indicating lamps
  and breaker control switch, mimic bus, cubicle nameplates, base channel, arc-resistant plenum on
  the roof with its exhaust duct to the outside wall;
- 480 V switchgear: four-high draw-out breaker cells with trip units;
- MCCs (20 in sections): buckets with disconnect handles and pilot lights, vertical and top
  wireways, conduit drops from the overhead tray;
- protection & control panels: flush relays, test switches, lamps; DCS / telecom cabinets with
  perforated doors and status LEDs; panelboards;
- static starters (LCI) and VFDs: louvred doors, keypads, roof fan hoods; dry-type transformers
  in louvred enclosures;
- the room: epoxy floor, yellow aisle lines, dielectric mats in front of every lineup, LED
  fixtures, HVAC supply duct and diffusers, copper ground bus on the walls, fire extinguishers,
  exit signs, nameplates and arc-flash labels, a breaker lift truck and a technician; in R4 the
  VFD output trays over the lineups and the bus-duct entries from T-R4-1..4.

Runs after detail3 (which leaves the interiors alone). Interior-only colours (`*_in`, `led_*`,
`hmi`, `lamp_in`) stay clean in Blender (no weathering) and the LEDs / screens / fixtures glow.
"""
import fuel
from fuel import box, rod

FACES = {"+x", "-x", "+y", "-y"}


class Front:
    """Coordinates on a lineup front: u runs along the lineup, z is height, d is the distance out of
    the front face (negative = into the cabinet)."""

    def __init__(self, fp, face):
        self.x0, self.x1, self.y0, self.y1 = fp
        self.face = face
        self.L = (self.y1 - self.y0) if face[1] == "x" else (self.x1 - self.x0)
        self.D = (self.x1 - self.x0) if face[1] == "x" else (self.y1 - self.y0)
        self.s = 1 if face[0] == "+" else -1
        self.plane = {"+x": self.x1, "-x": self.x0, "+y": self.y1, "-y": self.y0}[face]

    def n(self):
        return {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0)}[self.face]

    def p(self, u, z, d):
        a = self.plane + self.s * d
        return (a, self.y0 + u, z) if self.face[1] == "x" else (self.x0 + u, a, z)

    def b(self, u0, u1, z0, z1, d0, d1, c):
        a0, a1 = self.plane + self.s * d0, self.plane + self.s * d1
        if self.face[1] == "x":
            box(a0, a1, self.y0 + u0, self.y0 + u1, z0, z1, c)
        else:
            box(self.x0 + u0, self.x0 + u1, a0, a1, z0, z1, c)


def lamps(F, u, z, cols=("led_r", "led_g", "led_a"), sz=.13, gap=.3):
    for k, c in enumerate(cols):
        F.b(u + k * gap, u + k * gap + sz, z, z + sz, .05, .1, c)


def relay(F, u, z, w=.85, h=1.15):
    """Numerical protection relay faceplate: small LCD, target LEDs, navigation and function keys."""
    F.b(u, u + w, z, z + h, .06, .13, "steel_dark")
    F.b(u + .08, u + w - .08, z + h - .32, z + h - .1, .13, .135, "hmi")          # 2-line LCD
    for k in range(8):                                                           # target LEDs
        F.b(u + .1 + k * (w - .2) / 8, u + .14 + k * (w - .2) / 8, z + h - .42, z + h - .38, .13, .14,
            "led_g" if k < 2 else "led_r" if k == 2 else "mimic")
    for r in range(2):                                                           # pushbuttons
        for k in range(4):
            F.b(u + .12 + k * (w - .24) / 4, u + .12 + (k + .6) * (w - .24) / 4, z + .15 + r * .18, z + .27 + r * .18,
                .13, .15, "label" if r else "panel_in")


def handle(F, u, z0, z1):
    F.b(u, u + .1, z0, z1, .05, .16, "steel")


def sections(L, w):
    n = max(1, round(L / w))
    return [(L * k / n, L * (k + 1) / n) for k in range(n)]


# ------------------------------------------------------------------------------- equipment fronts
def mv_swgr(F, z0, z1, body, u0=0, u1=None, vent=0.0, ff=False):
    """Metal-clad switchgear, 36 in cubicles, two-high (breaker below, relay / instrument door above)."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.15, 0, "steel_dark")                              # base channel / kick plate
    F.b(u0 + .1, u1 - .1, z0 + 4.55, z0 + 4.62, .06, .065, "mimic")             # mimic bus
    for (a, c) in sections(u1 - u0, 3.0):
        a, c = u0 + a, u0 + c
        W = c - a
        F.b(a - .025, a + .025, z0 + .3, z1, 0, .03, "steel_dark")               # cubicle seam
        F.b(a + .06, c - .06, z0 + .38, z0 + 3.9, 0, .06, body)                  # breaker door
        F.b(a + .06, c - .06, z0 + 3.98, z1 - .55, 0, .06, body)                 # relay / instrument door
        F.b(a + .06, c - .06, z1 - .48, z1 - .08, 0, .04, body)                  # top wireway cover
        F.b(a + W * .3, a + W * .7, z0 + 2.45, z0 + 3.2, .06, .08, "glass")       # breaker viewing window
        F.b(a + W * .45, a + W * .55, z0 + 1.55, z0 + 1.7, .06, .09, "steel_dark")  # racking port
        handle(F, c - .38, z0 + 1.7, z0 + 2.6)
        handle(F, c - .38, z0 + 5.0, z0 + 5.8)
        F.b(a + W * .5 - .03, a + W * .5 + .03, z0 + 3.98, z0 + 4.55, .06, .065, "mimic")  # drop to the breaker
        relay(F, a + .35, z0 + 5.5)                                              # feeder / motor protection relay
        F.b(a + 1.55, a + 2.25, z0 + 6.15, z0 + 6.75, .06, .1, "steel_dark")      # power meter
        F.b(a + 1.65, a + 2.15, z0 + 6.42, z0 + 6.62, .1, .105, "hmi")
        lamps(F, a + 1.5, z0 + 5.15)                                            # open / closed / spring charged
        F.b(a + 1.62, a + 1.84, z0 + 4.8, z0 + 5.0, .06, .2, "steel_dark")        # breaker control switch
        F.b(a + .8, a + 2.2, z1 - 1.12, z1 - .8, .06, .08, "label")              # cubicle nameplate
        F.b(a + .25, c - .25, z1, z1 + .07, -2.8, -.35, body)                    # arc-resistant relief flaps
    F.b(u0, u1, z1, z1 + 1.35, -(F.D - .3), -(F.D - 2.6), body)                  # arc plenum along the roof
    if vent:                                                                    # plenum exhaust to the wall
        r0, r1 = -(F.D - .3), -(F.D - 2.6)
        F.b(u1 - 2.3, u1 - .2, z1 + .15, z1 + 1.2, -(F.D + vent), r0, body)


def lv_swgr(F, z0, z1, body, u0=0, u1=None):
    """480 V draw-out switchgear: four breaker cells per section."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.15, 0, "steel_dark")
    for (a, c) in sections(u1 - u0, 2.6):
        a, c = u0 + a, u0 + c
        F.b(a - .025, a + .025, z0 + .3, z1, 0, .03, "steel_dark")
        h = (z1 - .5 - (z0 + .35)) / 4
        for k in range(4):
            zb = z0 + .35 + k * h
            F.b(a + .06, c - .06, zb + .04, zb + h - .04, 0, .05, body)
            if k == 0:
                continue                                                        # bottom cell: spare / cable
            F.b(a + .4, c - .4, zb + .3, zb + h - .35, .05, .1, "steel_dark")    # breaker escutcheon
            F.b(a + .7, a + 1.2, zb + h * .5, zb + h * .5 + .35, .1, .11, "hmi")  # trip unit
            lamps(F, c - .75, zb + h - .3, ("led_r", "led_g"), sz=.11, gap=.22)
        F.b(a + .06, c - .06, z1 - .46, z1 - .06, 0, .04, body)
        F.b(a + .6, c - .6, z1 - .38, z1 - .16, .04, .06, "label")


def mcc(F, z0, z1, body, u0=0, u1=None):
    """Motor control centre: 20 in sections, buckets with disconnect handles, vertical wireway."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.12, 0, "steel_dark")
    pat = [1.0, 1.0, 1.5, 1.0, 2.0, 1.0]
    for j, (a, c) in enumerate(sections(u1 - u0, 1.67)):
        a, c = u0 + a, u0 + c
        F.b(a - .02, a + .02, z0 + .3, z1, 0, .03, "steel_dark")
        F.b(c - .4, c - .05, z0 + .35, z1 - .6, 0, .05, body)                    # vertical wireway door
        F.b(a + .05, c - .05, z1 - .55, z1 - .06, 0, .05, body)                  # top horizontal wireway
        top = z1 - .6
        bot = z0 + .4
        rot = pat[j % 3:] + pat[:j % 3]
        hs = [h * (top - bot) / sum(rot) for h in rot]
        zb = bot
        for h in hs:
            F.b(a + .05, c - .45, zb + .03, zb + h - .03, 0, .05, body)          # bucket door
            F.b(a + .2, a + .42, zb + h * .5 - .2, zb + h * .5 + .2, .05, .1, "steel_dark")   # disconnect
            F.b(a + .27, a + .35, zb + h * .5 - .05, zb + h * .5 + .32, .1, .16, "red")      # handle
            F.b(a + .6, a + .9, zb + h - .3, zb + h - .14, .05, .07, "label")
            lamps(F, a + .6, zb + .18, ("led_r", "led_g"), sz=.09, gap=.18)
            zb += h


def pc_panel(F, z0, z1, body, u0=0, u1=None):
    """Protection & control panels (22 in): flush relays, test switches, lamps."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.12, 0, "steel_dark")
    for (a, c) in sections(u1 - u0, 1.83):
        a, c = u0 + a, u0 + c
        W = c - a
        F.b(a - .02, a + .02, z0 + .3, z1, 0, .03, "steel_dark")
        F.b(a + .05, c - .05, z0 + .35, z1 - .1, 0, .05, body)
        F.b(a + .2, c - .2, z1 - .55, z1 - .32, .05, .07, "label")
        for r, zr in enumerate((z0 + 5.3, z0 + 4.0, z0 + 2.7)):
            for k in range(2):
                ua = a + .15 + k * (W - .3) / 2
                ub = ua + (W - .3) / 2 - .1
                relay(F, ua, zr, w=ub - ua, h=1.05)
        for k in range(4):                                                      # test switches
            F.b(a + .2 + k * (W - .4) / 4, a + .2 + (k + .8) * (W - .4) / 4, z0 + 1.9, z0 + 2.3, .05, .12, "label")
        lamps(F, a + .25, z0 + 1.5, ("led_r", "led_g", "led_a"), sz=.1, gap=.22)
        handle(F, c - .22, z0 + 3.4, z0 + 4.2)


def dcs(F, z0, z1, body, u0=0, u1=None):
    """DCS / network / telecom cabinets: perforated doors, status LEDs."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.12, 0, "steel_dark")
    for (a, c) in sections(u1 - u0, 2.0):
        a, c = u0 + a, u0 + c
        F.b(a - .02, a + .02, z0 + .3, z1, 0, .03, "steel_dark")
        F.b(a + .05, c - .05, z0 + .35, z1 - .1, 0, .04, body)
        F.b(a + .2, c - .2, z0 + .8, z1 - .9, .04, .06, "louvre")               # perforated panel
        F.b(a + .25, c - .25, z1 - .7, z1 - .45, .04, .06, "label")
        for k in range(5):
            F.b(a + .3 + k * .25, a + .38 + k * .25, z1 - .85, z1 - .77, .06, .08, "led_g" if k != 3 else "led_a")
        handle(F, c - .2, z0 + 3.4, z0 + 4.4)


def drive(F, z0, z1, body, w=2.5, u0=0, u1=None, fans=True, top=None):
    """Static starter / VFD sections: louvred doors, keypad, roof fan hoods."""
    u1 = F.L if u1 is None else u1
    F.b(u0, u1, z0, z0 + .3, -.15, 0, "steel_dark")
    for (a, c) in sections(u1 - u0, w):
        a, c = u0 + a, u0 + c
        W = c - a
        F.b(a - .025, a + .025, z0 + .3, z1, 0, .03, "steel_dark")
        F.b(a + .06, c - .06, z0 + .38, z1 - .1, 0, .05, body)
        F.b(a + .3, c - .3, z0 + .6, z0 + 1.9, .05, .08, "louvre")              # intake grille
        F.b(a + .3, c - .3, z1 - 1.9, z1 - .8, .05, .08, "louvre")              # upper grille
        F.b(a + W * .5 - .3, a + W * .5 + .3, z0 + 4.3, z0 + 5.1, .05, .12, "steel_dark")     # keypad
        F.b(a + W * .5 - .22, a + W * .5 + .22, z0 + 4.75, z0 + 5.0, .12, .125, "hmi")
        for k in range(3):
            F.b(a + W * .5 - .2 + k * .15, a + W * .5 - .1 + k * .15, z0 + 4.4, z0 + 4.5, .12, .14, "label")
        lamps(F, a + W * .5 - .3, z0 + 3.8, ("led_g", "led_a", "led_r"), sz=.11, gap=.22)
        F.b(a + W * .5 - .5, a + W * .5 + .5, z1 - .68, z1 - .44, .05, .07, "label")
        handle(F, c - .35, z0 + 2.6, z0 + 3.6)
        if fans:
            pc = F.p(a + W * .5, z1, -F.D * .5)
            rod(pc, (pc[0], pc[1], z1 + .45), min(.65, W * .3), "fan", seg=16)
            rod((pc[0], pc[1], z1 + .45), (pc[0], pc[1], z1 + .55), min(.65, W * .3) * .8, "steel_dark", seg=16)


def dry_xfmr(fp, z0, z1):
    """Dry-type transformer enclosure: louvre bands low and high on every face, lifting lugs."""
    for face in FACES:
        F = Front(fp, face)
        F.b(.4, F.L - .4, z0 + .5, z0 + 2.2, 0, .06, "louvre")
        F.b(.4, F.L - .4, z1 - 2.0, z1 - .6, 0, .06, "louvre")
        F.b(F.L * .5 - .5, F.L * .5 + .5, z0 + 3.8, z0 + 4.4, 0, .04, "label")
    x0, x1, y0, y1 = fp
    for (x, y) in ((x0 + .6, y0 + .6), (x1 - .6, y0 + .6), (x0 + .6, y1 - .6), (x1 - .6, y1 - .6)):
        box(x - .12, x + .12, y - .12, y + .12, z1, z1 + .4, "steel")


def panelboard(F, z0, z1, body):
    for (a, c) in sections(F.L, 3.5):
        F.b(a + .2, c - .2, z0 + 2.5, z1 - .8, 0, .2, body)
        F.b(a + .5, c - .5, z1 - 1.2, z1 - .95, .2, .22, "label")
        handle(F, c - .45, z0 + 4.4, z0 + 5.0)


# ------------------------------------------------------------------------------- room furniture
def mat(F, z, depth=3.0):
    F.b(0, F.L, z, z + .04, 0, depth, "mat")


def fixture(x, y, z, along="y", roof=None):
    """LED linear high-bay, 4 ft x 1 ft, on two hangers."""
    dx, dy = (.5, 2) if along == "y" else (2, .5)
    box(x - dx, x + dx, y - dy, y + dy, z - .3, z, "steel")
    box(x - dx + .08, x + dx - .08, y - dy + .08, y + dy - .08, z - .34, z - .3, "lamp_in")
    for k in (-1, 1):
        a = (x, y + k * (dy - .4)) if along == "y" else (x + k * (dx - .4), y)
        rod((a[0], a[1], z), (a[0], a[1], roof or z + 2.0), .03, "steel", seg=6)


def extinguisher(x, y, z, n):
    rod((x, y, z + 1.2), (x, y, z + 2.9), .25, "sw_red", seg=12)
    rod((x, y, z + 2.9), (x, y, z + 3.25), .08, "steel_dark", seg=8)
    sx, sy = x - n[0] * .3, y - n[1] * .3
    box(sx - .03 if n[0] else sx - .5, sx + .03 if n[0] else sx + .5,
        sy - .5 if n[0] else sy - .03, sy + .5 if n[0] else sy + .03, z + 5.2, z + 6.2, "sw_red")


def exit_sign(x, y, z, n):
    w = (.06, .6) if n[0] else (.6, .06)
    box(x - w[0], x + w[0], y - w[1], y + w[1], z, z + .55, "label")
    box(x - w[0] - .01, x + w[0] + .01, y - w[1] * .7, y + w[1] * .7, z + .12, z + .4, "led_r")


def ground_bus(pts, z):
    for (a, b) in zip(pts, pts[1:]):
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        box(x0 - .02, x1 + .02, y0 - .02, y1 + .02, z, z + .17, "cu_bus")


def lift_truck(x, y, z, along="y"):
    """MV breaker lift truck with a spare vacuum breaker on its forks."""
    if along == "y":
        box(x - 1.3, x + 1.3, y - 1.4, y + 1.4, z + .35, z + .55, "steel_dark")
        for (wx, wy) in ((x - 1.1, y - 1.1), (x + 1.1, y - 1.1), (x - 1.1, y + 1.1), (x + 1.1, y + 1.1)):
            rod((wx - .1, wy, z + .25), (wx + .1, wy, z + .25), .25, "tyre", seg=12)
        for wx in (x - 1.1, x + 1.1):
            box(wx - .1, wx + .1, y + 1.1, y + 1.3, z + .55, z + 6.5, "amber")        # mast
        box(x - 1.2, x + 1.2, y + 1.1, y + 1.3, z + 6.3, z + 6.5, "amber")
        box(x - 1.2, x + 1.2, y - 1.3, y + 1.1, z + 2.0, z + 2.1, "steel")           # forks
        box(x - 1.0, x + 1.0, y - 1.2, y + .9, z + 2.1, z + 4.4, "steel_dark")       # breaker
        box(x - .9, x + .9, y - 1.25, y - 1.2, z + 2.4, z + 4.1, "swgr_in")           # breaker front plate
        box(x - .5, x + .5, y - 1.3, y - 1.25, z + 3.3, z + 3.8, "label")
        for k in (-1, 0, 1):
            rod((x + k * .6, y + .9, z + 3.2), (x + k * .6, y + 1.05, z + 3.2), .14, "copper_dark", seg=8)  # primary fingers
        rod((x - .8, y + 1.5, z + 3.8), (x + .8, y + 1.5, z + 3.8), .06, "steel", seg=8)                 # push bar


def hvac_duct(x0, x1, y0, y1, z0, z1, diffusers, roof=23):
    box(x0, x1, y0, y1, z0, z1, "duct")
    for y in range(int(y0) + 4, int(y1), 10):                                   # trapeze hangers to the roof steel
        rod((x0 - .15, y, z0 - .1), (x0 - .15, y, roof), .03, "steel", seg=6)
        rod((x1 + .15, y, z0 - .1), (x1 + .15, y, roof), .03, "steel", seg=6)
        box(x0 - .25, x1 + .25, y - .08, y + .08, z0 - .15, z0, "steel")
    for (x, y) in diffusers:
        box(x - .9, x + .9, y - .9, y + .9, z0 - .25, z0, "duct")
        box(x - .7, x + .7, y - .7, y + .7, z0 - .27, z0 - .25, "louvre")


def conduits(x_tray, z_tray, x_eq, z_top, ys, r=.07):
    for y in ys:
        rod((x_tray, y, z_tray - .2), (x_eq, y, z_tray - .2), r, "pipe", seg=8)
        rod((x_eq, y, z_tray - .2), (x_eq, y, z_top), r, "pipe", seg=8)


# ------------------------------------------------------------------------------- build
def _decal(c, n, w, h, lines, bg="#ffffff"):
    import showcase
    showcase.decal(c, n, w, h, lines, bg=bg)


def arc_label(F, u, z, volts, cal):
    c = F.p(u, z, .1)
    _decal(c, F.n(), .85, .62, [("WARNING", .2, 1, "#111111", 0, "#ff7a00"),
                                ("Arc Flash and Shock Hazard", .1, 1, "#111111"),
                                (f"{cal} cal/cm2 at 18 in", .1, 0, "#111111"),
                                (f"Shock hazard: {volts}", .1, 0, "#111111"),
                                ("PPE category per NFPA 70E", .09, 0, "#333333")])


def nameplate(F, u, z, text, sub):
    _decal(F.p(u, z, .12), F.n(), 3.6, .55, [(text, .48, 1, "#ffffff"), (sub, .26, 0, "#e9e9e9")], bg="#1d2b38")


def build():
    G = fuel.G
    items, parts = G["items"], G["parts"]
    fuel.D = True
    n0 = len(parts)
    by = {}
    for it in items:
        if it["layer"] in ("R1_INTERIOR", "R4_INTERIOR"):
            by[it["name"]] = it
    interior = {it["id"] for it in by.values()}
    # the plain section seams drawn on the long lineups give way to real fronts; cabinet bodies get the
    # clean interior finishes (ANSI 61 grey, no weathering)
    recol = {"swgr": "swgr_in", "cabinet": "cab_in", "panel": "panel_in"}
    keep = []
    for p in parts:
        if p.get("item") in interior and not p.get("d") and p["color"] == "steel":
            continue
        if p.get("item") in interior and p["color"] in recol:
            p["color"] = recol[p["color"]]
        keep.append(p)
    parts[:] = keep

    def it_(prefix):
        return next(v for k, v in by.items() if k.startswith(prefix))

    def foot(it):
        ps = [p for p in parts if p.get("item") == it["id"] and p["kind"] == "box" and not p.get("d")]
        b = max(ps, key=lambda p: (p["max"][0] - p["min"][0]) * (p["max"][1] - p["min"][1]))
        return (b["min"][0], b["max"][0], b["min"][1], b["max"][1]), b["min"][2], b["max"][2], b["color"]

    # ---------------- R1 main room ----------------
    Z = .6
    for k in (1, 2, 3):
        it = it_(f"R1 SWGR-13.8-{k}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "-x")
        mv_swgr(F, z0, z1, c, vent=473 - f[1])
        nameplate(F, F.L / 2, z1 - .25 + .0, f"SWGR-13.8-{k}", "13.8 kV  ·  1200 A  ·  40 kA  ·  ARC-RESISTANT TYPE 2B")
        arc_label(F, 1.5, Z + 5.0, "13,800 V", 8.4)
        mat(F, Z)
    for k, ab in enumerate("AB"):
        it = it_(f"R1 SWGR-4.16-{ab}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "+x")
        mv_swgr(F, z0, z1, c)
        nameplate(F, F.L / 2, z1 - .25, f"SWGR-4.16-{ab}", "4.16 kV  ·  2000 A  ·  40 kA  ·  METAL-CLAD")
        arc_label(F, 1.5, Z + 5.0, "4,160 V", 11.2)
        mat(F, Z)
    for ab in "AB":
        it = it_(f"R1 LC-480-{ab}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "+x")
        lv_swgr(F, z0, z1, c)
        arc_label(F, 1.3, Z + 6.6, "480 V", 24.6)
        mat(F, Z)
    it = it_("R1 EMCC")
    fuel.on(it)
    f, z0, z1, c = foot(it)
    F = Front(f, "+x")
    mcc(F, z0, z1, c)
    mat(F, Z)
    for tg in ("MCC-GT1", "MCC-GT2", "MCC-GT3", "MCC-C1", "MCC-C2"):
        it = it_(f"R1 {tg}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "-x")
        mcc(F, z0, z1, c)
        nameplate(F, F.L / 2, z1 - .3, tg, "480 V MCC  ·  800 A  ·  65 kA")
        mat(F, Z)
        conduits(438.9, 14, (f[0] + f[1]) / 2, z1, [f[2] + 1.5 + 2.2 * j for j in range(int((f[3] - f[2] - 2) / 2.2))])
    it = it_("R1 Protection & control")
    fuel.on(it)
    f, z0, z1, c = foot(it)
    F = Front(f, "+x")
    pc_panel(F, z0, z1, c)
    mat(F, Z)
    for pre in ("R1 DCS / network", "R1 Telecom / FO"):
        it = it_(pre)
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "+x")
        dcs(F, z0, z1, c)
        mat(F, Z)
    it = it_("R1 LP / HT panels")
    fuel.on(it)
    f, z0, z1, c = foot(it)
    panelboard(Front(f, "+x"), z0, z1, c)
    for k in (1, 2, 3):
        it = it_(f"R1 LCI-{k} static")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "+x")
        drive(F, z0, z1, c, w=2.5)
        nameplate(F, F.L / 2, z1 - .3, f"LCI-{k}", f"GT{k} STATIC STARTER  ·  LOAD-COMMUTATED INVERTER")
        arc_label(F, 1.2, Z + 5.6, "4,160 V", 6.2)
        mat(F, Z)
        it = it_(f"R1 TX-LCI-{k}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        dry_xfmr(f, z0, z1)

    # room dressing
    room = fuel.new_item("R1_INTERIOR", "R1 switchgear room finishes: epoxy floor, aisle lines, mats, lighting, HVAC, "
                         "ground bus, extinguishers, exit signs", (411, 473, 626, 752), (0.6, 22), area="A",
                         sheet="SK-3X1-05", basis="typical", register=False,
                         info="Interior finishes and fittings, typical for an electrical building: sealed epoxy floor, "
                         "yellow egress lines, Class 2 dielectric mats in front of every lineup, LED high-bays, ducted "
                         "HVAC (positive pressure), 1/4 x 2 in copper ground bus, extinguishers, exit signs.")
    fuel.on(room)
    box(411, 426, 626, 752, Z, Z + .02, "epoxy")
    box(426.5, 473, 626, 752, Z, Z + .02, "epoxy")
    for (xa, ya, yb) in ((432.2, 630, 748), (439.8, 630, 748), (455.3, 630, 748), (460.7, 630, 748),
                         (419.2, 630, 748), (424.8, 630, 748)):
        box(xa - .12, xa + .12, ya, yb, Z + .02, Z + .03, "yellow")
    for yy in (629.5, 749.5):
        box(426.6, 472.5, yy - .12, yy + .12, Z + .02, Z + .03, "yellow")
    for x in (422, 436, 458, 471):
        for y in range(636, 748, 12):
            fixture(x, y + 4, 20.5, roof=23)
    hvac_duct(447.5, 450.5, 628, 750, 18.4, 20.0, [(449, y) for y in range(640, 750, 20)])
    hvac_duct(433, 435, 628, 750, 18.6, 19.8, [(434, y) for y in range(645, 750, 25)])
    ground_bus([(411.1, 626.6), (411.1, 751.4), (472.9, 751.4), (472.9, 626.6), (411.1, 626.6)], 1.6)
    for (x, y, n) in ((411.3, 640, (1, 0)), (411.3, 720, (1, 0)), (472.7, 690, (-1, 0)), (426.9, 700, (1, 0)),
                      (444, 626.8, (0, 1)), (444, 751.2, (0, -1))):
        extinguisher(x, y, Z, n)
    for (x, y, n) in ((411.15, 630, (1, 0)), (472.85, 630, (-1, 0)), (472.85, 750, (-1, 0)), (411.15, 750, (1, 0))):
        exit_sign(x, y, 9.4, n)
    lift_truck(458, 632.5, Z)
    import figure
    figure.build(rod, 459.8, 690, Z, a=0.0, vest="workwear", pose="work")       # reading a relay on SWGR-13.8-2

    # ---------------- R4 VFD e-house ----------------
    Z4 = 2.5
    for k in range(4):
        it = it_(f"R4 VFD lineup {k + 1}")
        fuel.on(it)
        f, z0, z1, c = foot(it)
        F = Front(f, "+y" if k in (0, 2) else "-y")
        drive(F, z0, z1, c, w=100 / 23)
        nameplate(F, F.L / 2, z1 - .3, f"VFD-L{k + 1}", f"23 x ACC FAN DRIVES  ·  480 V  ·  FED FROM T-R4-{k + 1}")
        arc_label(F, 2.0, Z4 + 5.6, "480 V", 18.0)
        mat(F, Z4)
        yc = (f[2] + f[3]) / 2
        # VFD output cable tray over the lineup, running to the cable exit at the east wall
        box(f[0], 1250, yc - 1, yc + 1, 12.6, 12.9, "pipe")
        box(f[0], 1250, yc - .8, yc + .8, 12.9, 13.1, "cable_tc")
        for s in range(23):
            xx = f[0] + 100 * (s + .5) / 23
            rod((xx, yc, z1 + .6), (xx, yc, 12.6), .12, "pipe", seg=8)
        # bus duct from T-R4-k through the east wall into the lineup end
        box(f[1] - 1.6, 1255.6, yc - .5, yc + .5, 11.0, 11.8, "swgr_in")
        box(f[1] - 1.6, f[1] - .4, yc - .5, yc + .5, z1, 11.0, "swgr_in")
    it = it_("R4 480 V switchgear")
    fuel.on(it)
    f, z0, z1, c = foot(it)
    F = Front(f, "+x")
    lv_swgr(F, z0, z1, c, 0, 20)
    mcc(F, z0, z1, c, 20.6, F.L)
    nameplate(F, 10, z1 - .3, "R4-LC / R4-MCC", "480 V SWITCHGEAR + VACUUM-PUMP MCC")
    arc_label(F, 1.3, Z4 + 6.6, "480 V", 22.0)
    mat(F, Z4)
    room4 = fuel.new_item("R4_INTERIOR", "R4 VFD room finishes: floor, mats, lighting, HVAC, ground bus, extinguishers",
                          (1136, 1254, 309, 367), (2.5, 15.4), area="B", sheet="SK-3X1-03", basis="typical",
                          register=False, info="Typical e-house fit-out: floor coating, dielectric mats, LED fixtures, "
                          "wall-mounted HVAC (four units, N+1) with supply grilles, ground bus, extinguishers.")
    fuel.on(room4)
    box(1136, 1254, 309, 367, Z4, Z4 + .02, "epoxy")
    for y in (321.5, 351.5, 336.5):
        for x in range(1150, 1246, 12):
            fixture(x, y, 14.8, along="x", roof=15.4)
    for x in (1160, 1190, 1220, 1245):                                            # wall-mounted HVAC (north wall)
        box(x - 3, x + 3, 368, 371, 6, 13, "machine")
        box(x - 2.6, x + 2.6, 371, 371.1, 7, 9.5, "louvre")
        box(x - 2, x + 2, 366.9, 367, 11, 13, "louvre")                          # supply grille inside
    ground_bus([(1136.1, 309.6), (1136.1, 366.4), (1253.9, 366.4), (1253.9, 309.6), (1136.1, 309.6)], 3.5)
    for (x, y, n) in ((1136.3, 340, (1, 0)), (1253.7, 320, (-1, 0)), (1200, 309.3, (0, 1))):
        extinguisher(x, y, Z4, n)
    for (x, y, n) in ((1136.15, 320, (1, 0)), (1253.85, 350, (-1, 0))):
        exit_sign(x, y, 11.0, n)
    figure.build(rod, 1180, 319.8, Z4, a=-1.5708, vest="workwear", pose="work")  # at a drive keypad, lineup 1
    fuel.D = False
    return len(parts) - n0
