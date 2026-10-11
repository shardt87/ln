"""SIMpull / Maxis cable-installation equipment (Southwire, the requested cable supplier), from the SIMpull
Solutions brochure and the NECA 2026 booth: placed where cable work happens on an operating plant.

Equipment (sizes from the brochure; geometry typical):
- SIMpull Reel: 61 in high x 32 in wide, black spoked outer flanges turning on their own, inner reel with
  paralleled colour-coded feeders, magnetic chocks; on a SIMpull Cradle (steel base, rollers, fork pockets);
- SIMpull Flange: shaftless black flanges fitted to a wooden reel (up to 34 in / 2,000 lb), yellow chocks,
  eye bolts;
- SIMpull Stack (paralleled) reels: one wooden reel, up to five coloured conductors per pull, on Maxis JAX
  reel stands;
- 30K / 45K Reel Rollers (RR-SW30 / RR-SW45): welded low frames with two driven rollers, VFD motor box,
  pendant with variable speed, fork tubes;
- SIMpull CoilPAK payoffs on a CoilPAK cart, SIMpull BARREL cable drum on its hand truck, wire wagon with
  spools on two arbors;
- Maxis XD10 cable puller (boom on a wheeled base), Maxis Feeder, Extreme Duty tension monitor, Triggers
  wireless safety switch, SIMpull Head pulling grips on the conductor ends;
- temporary power and lighting: towable generator, cam-lock cords, 480 V 3-phase cart, power distribution
  boxes, extension cords, tripod LED work lights, area lights.

Placement: the reel yard (staging), an active feeder pull at the maintenance building facing it, the
turbine-hall outage pull (reel on a 45K Reel Roller) and the BESS trench pull (Maxis JAX stands).
"""
import math

import fuel
from fuel import box, rod

BRAND, RED, INK = "SOUTHWIRE", "#d2232a", "#1d1f21"
FEEDER = ("cable", "red", "pvc_blue", "binder_w", "pvc_green")          # black, red, blue, white, green


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, z=0.0, a=0.0, vest="hivis", hat="hardhat"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest, hat=hat)


def _ax(axis):
    return ((1, 0, 0), (0, 1, 0)) if axis == "x" else ((0, 1, 0), (1, 0, 0))


# ------------------------------------------------------------------------------- reels
def flange_disc(c, ax, R, t, col="sp_black", spokes=10):
    """Spoked plastic flange: rim, web, radial ribs and hub on the outer face (ax points outward)."""
    rod(c, (c[0] + ax[0] * t, c[1] + ax[1] * t, c[2]), R, col, seg=40)
    o = (c[0] + ax[0] * t, c[1] + ax[1] * t, c[2])
    rod(o, (o[0] + ax[0] * .06, o[1] + ax[1] * .06, o[2]), R * .3, col, seg=24)         # hub
    up = (0, 0, 1)
    side = (ax[1], -ax[0], 0)
    for k in range(spokes):
        t_ = 2 * math.pi * k / spokes
        d = (side[0] * math.cos(t_), side[1] * math.cos(t_), math.sin(t_))
        a = (o[0] + d[0] * R * .32, o[1] + d[1] * R * .32, o[2] + d[2] * R * .32)
        b = (o[0] + d[0] * R * .93, o[1] + d[1] * R * .93, o[2] + d[2] * R * .93)
        rod(a, b, .07, col, seg=6)


def bands(pt, W, r, cols, t=.18):
    n = len(cols)
    for k, c in enumerate(cols):
        s0 = -W / 2 + t + k * (W - 2 * t) / n
        rod(pt(s0), pt(s0 + (W - 2 * t) / n), r, c, seg=28)


def sp_reel(x, y, z0=0.0, axis="y", cols=FEEDER, cradle=True, label="SIMpull THHN  500 KCMIL", heads=False):
    """SIMpull Reel (61 x 32 in) on a SIMpull Cradle; axis 'x' or 'y'."""
    D, W = 5.08, 2.67
    R = D / 2
    ax, nx = _ax(axis)
    zb = z0 + (.55 if cradle else 0)
    zc = zb + R
    pt = lambda s, o=0.0, dz=0.0: (x + ax[0] * s + nx[0] * o, y + ax[1] * s + nx[1] * o, zc + dz)
    if cradle:
        a0, a1 = pt(-W / 2 - .45, -R * .8), pt(W / 2 + .45, R * .8)
        X0, X1, Y0, Y1 = min(a0[0], a1[0]), max(a0[0], a1[0]), min(a0[1], a1[1]), max(a0[1], a1[1])
        box(X0, X1, Y0, Y1, z0, z0 + .12, "steel_dark")                                   # base plate
        for o in (-R * .8, R * .8 - .3):                                                   # side rails with fork pockets
            b0, b1 = pt(-W / 2 - .45, o), pt(W / 2 + .45, o + .3)
            box(min(b0[0], b1[0]), max(b0[0], b1[0]), min(b0[1], b1[1]), max(b0[1], b1[1]), z0 + .12, z0 + .5, "steel_dark")
        for o in (-1.05, 1.05):                                                            # rollers under the flanges
            rod(pt(-W / 2 - .2, o, -zc + z0 + .38), pt(W / 2 + .2, o, -zc + z0 + .38), .18, "steel", seg=12)
    for s, sg in ((-W / 2, -1), (W / 2, 1)):
        base = pt(s - (.16 if sg > 0 else 0))
        flange_disc(base if sg > 0 else pt(s), (ax[0] * sg, ax[1] * sg), R, .16) if sg > 0 else \
            flange_disc(pt(s + .16), (-ax[0], -ax[1]), R, .16)
    bands(pt, W, R * .76, cols)
    rod(pt(-W / 2 + .16), pt(W / 2 - .16), R * .3, "sp_black", seg=20)                    # inner drum core
    for sg in (-1, 1):                                                                     # magnetic chocks
        c = pt(sg * (W / 2 - .05), R * .55, -R + .12)
        box(c[0] - .25, c[0] + .25, c[1] - .25, c[1] + .25, zb - .02, zb + .25, "sp_yellow")
        decal(pt(sg * (W / 2 + .14), 0, -R * .55), (ax[0] * sg, ax[1] * sg, 0), 1.25, .75,
              [("SIMpull REEL", .22, 1, INK), (label, .13, 0, "#333"), (BRAND, .16, 1, RED, 1)], bg="#f4f4f1")
    if heads:                                                                              # paralleled ends with SIMpull Heads
        for k, c in enumerate(cols):
            a = pt(-W / 2 + .35 + k * .45, -R * .9, R * .1)
            b = (a[0] - nx[0] * 1.2, a[1] - nx[1] * 1.2, a[2] - .6)
            rod(a, b, .09, c, seg=8)
            rod(b, (b[0] - nx[0] * .7, b[1] - nx[1] * .7, b[2] - .1), .11, "alu", r2=.07, seg=10)
    return pt


def flange_reel(x, y, axis="y", D=3.0, W=2.2, cols=("hardhat", "hivis_o", "concrete", "hardhat", "hivis_o", "concrete"), label=""):
    """Wooden reel fitted with SIMpull Flanges (shaftless, independently rotating), on yellow chocks."""
    R, RF = D / 2, D / 2 + .32
    ax, nx = _ax(axis)
    zc = RF
    pt = lambda s, o=0.0, dz=0.0: (x + ax[0] * s + nx[0] * o, y + ax[1] * s + nx[1] * o, zc + dz)
    for sg in (-1, 1):
        rod(pt(sg * W / 2 - (.2 if sg > 0 else 0)), pt(sg * W / 2 + (0 if sg > 0 else .2)), R, "timber", seg=32)    # wooden flange
        o = pt(sg * (W / 2 + .02) + (0 if sg > 0 else -.12))
        rod(o, (o[0] + ax[0] * .12, o[1] + ax[1] * .12, o[2]), RF, "sp_black", seg=40)                            # SIMpull Flange
        f = pt(sg * (W / 2 + .16))
        box(f[0] - .08 if axis == "x" else f[0] - .25, f[0] + .08 if axis == "x" else f[0] + .25,
            f[1] - .25 if axis == "x" else f[1] - .08, f[1] + .25 if axis == "x" else f[1] + .08, zc - RF * .55, zc + RF * .55, "steel")
        box(f[0] - .12 if axis == "x" else f[0] - .45, f[0] + .12 if axis == "x" else f[0] + .45,
            f[1] - .45 if axis == "x" else f[1] - .12, f[1] + .45 if axis == "x" else f[1] + .12, zc + .5, zc + .7, "steel")
        c = pt(sg * (W / 2 + .1), -RF * .6, -RF + .1)
        box(c[0] - .2, c[0] + .2, c[1] - .2, c[1] + .2, 0, .2, "sp_yellow")                                       # chock
        e = pt(sg * (W / 2 + .2), 0, -RF + .15)
        rod(e, (e[0], e[1], e[2] - .15), .08, "sw_red", seg=8)                                                        # eye bolt
        decal(pt(sg * (W / 2 + .2), 0, -RF * .5), (ax[0] * sg, ax[1] * sg, 0), 1.0, .45,
              [("SIMpull FLANGE", .34, 1, "#f2f2f2"), (BRAND, .26, 1, RED, 1)], bg=None)
    bands(pt, W, R * .82, cols, t=.2)


def stack_reel(x, y, D=6.0, W=4.0, cols=FEEDER, z=0.0, jax=True, label="SIMpull STACK  4 x 500 KCMIL"):
    """Paralleled SIMpull Stack reel (wooden) on Maxis JAX reel stands, axis along y."""
    R = D / 2
    zc = z + R + (.6 if jax else 0)
    if jax:
        for s in (-1, 1):
            yy = y + s * (W / 2 + .5)
            rod((x - 1.9, yy, z), (x, yy, zc), .14, "steel_dark", seg=6)
            rod((x + 1.9, yy, z), (x, yy, zc), .14, "steel_dark", seg=6)
            box(x - 2.1, x + 2.1, yy - .25, yy + .25, z, z + .18, "steel_dark")
            box(x - .3, x + .3, yy - .2, yy + .2, zc - 1.2, zc - .2, "sp_yellow")                                # lift jack
        rod((x, y - W / 2 - .9, zc), (x, y + W / 2 + .9, zc), .14, "steel", seg=8)
    pt = lambda s, o=0.0, dz=0.0: (x, y + s, zc + dz)
    for s in (-W / 2, W / 2 - .3):
        rod(pt(s), pt(s + .3), R, "timber", seg=36)
    bands(pt, W, R * .8, cols * 2, t=.3)
    for sg in (-1, 1):
        decal((x, y + sg * (W / 2 + .02), zc - R * .45), (0, sg, 0), 2.2, 1.0,
              [(BRAND, .22, 1, RED, 1), (label, .14, 1, INK), ("CUT TO LENGTH  ·  SIMpull HEADS", .11, 0, "#444")],
              bg="#f2efe6")


def reel_roller(x, y, cap=45, reel_D=8.0, reel_W=5.0, cable="cable_mv", label="MV-105 35 kV 750 KCMIL", steel=True):
    """RR-SW30 / RR-SW45 reel roller (reel axis along y): welded frame, two driven rollers, motor box, pendant."""
    L, Wd = reel_W + 2.6, 6.0 if cap == 45 else 5.2
    y0, y1 = y - L / 2, y + L / 2
    for xx in (x - Wd / 2, x + Wd / 2 - .5):
        box(xx, xx + .5, y0, y1, 0, .55, "steel_dark")                                                         # side beams
    for yy in (y0, y1 - .5):
        box(x - Wd / 2, x + Wd / 2, yy, yy + .5, 0, .55, "steel_dark")
    for s in (-1, 1):                                                                                          # fork tubes
        box(x + s * 1.6 - .45, x + s * 1.6 + .45, y0 - .05, y1 + .05, .1, .45, "steel_dark")
    for s in (-1.35, 1.35):                                                                                    # driven rollers
        rod((x + s, y0 + .5, .85), (x + s, y1 - .5, .85), .32, "steel_dark", seg=16)
        for yy in (y0 + .5, y1 - .9):
            box(x + s - .35, x + s + .35, yy, yy + .4, .45, 1.25, "steel_dark")
    box(x - 1.2, x + 1.2, y1, y1 + 1.4, 0, 1.6, "steel_dark")                                                  # motor / VFD box
    box(x - 1.0, x + 1.0, y1 + 1.4, y1 + 1.45, .3, 1.3, "panel_in")
    rod((x + .9, y1 + 1.45, .9), (x + 2.2, y1 + 2.6, .1), .03, "cable", seg=6)                                  # pendant cord
    box(x + 2.1, x + 2.5, y1 + 2.5, y1 + 2.75, .05, .75, "sp_yellow")
    decal((x + Wd / 2 + .02, y, .32), (1, 0, 0), L * .8, .38,
          [(f"{cap},000 lbs REEL ROLLER", .62, 1, "#f2f2f2")], bg=None)
    decal((x, y1 + 1.47, .8), (0, 1, 0), 1.8, .9, [(f"RR-SW{cap}", .3, 1, INK), (BRAND, .22, 1, RED, 1)], bg="#f2f2ee")
    R = reel_D / 2
    zc = .85 + math.sqrt(max(.1, (R + .32) ** 2 - 1.35 ** 2))
    pt = lambda s, o=0.0, dz=0.0: (x, y + s, zc + dz)
    for s in (-reel_W / 2, reel_W / 2 - .35):
        rod(pt(s), pt(s + .35), R, "steel_dark" if steel else "timber", seg=44)
        if steel:
            for k in range(16):                                                                                # pressed-steel ribs
                t = 2 * math.pi * k / 16
                sg = -1 if s < 0 else 1
                yy = y + s + (0 if s < 0 else .35) + sg * .03
                rod((x + R * .3 * math.cos(t), yy, zc + R * .3 * math.sin(t)),
                    (x + R * .95 * math.cos(t), yy, zc + R * .95 * math.sin(t)), .06, "steel_dark", seg=6)
    bands(pt, reel_W, R * .78, [cable] * 3, t=.35)
    for sg in (-1, 1):
        decal((x, y + sg * (reel_W / 2 + .06), zc - R * .4), (0, sg, 0), 2.6, 1.1,
              [(BRAND, .24, 1, RED, 1), (label, .15, 1, "#f2f2f2")], bg=None)


# ------------------------------------------------------------------------------- carts, drums, pullers
def caster(x, y, r=.35):
    rod((x - .12, y, r), (x + .12, y, r), r, "tyre", seg=12)
    rod((x, y, r), (x, y, r + .35), .06, "steel", seg=6)


def coilpak_cart(x, y):
    """CoilPAK cart: two shelves of translucent CoilPAK payoffs."""
    box(x - 1.6, x + 1.6, y - 1.0, y + 1.0, .7, .8, "steel_dark")
    box(x - 1.6, x + 1.6, y - 1.0, y + 1.0, 2.4, 2.5, "steel_dark")
    for (sx, sy) in ((-1.5, -.9), (1.5, -.9), (-1.5, .9), (1.5, .9)):
        rod((x + sx, y + sy, .7), (x + sx, y + sy, 3.6), .05, "steel_dark", seg=6)
        caster(x + sx, y + sy)
    rod((x - 1.5, y - .9, 3.6), (x - 1.5, y + .9, 3.6), .06, "steel_dark", seg=6)                              # handle
    for k, (cx, z) in enumerate(((-.8, .8), (.8, .8), (-.8, 2.5), (.8, 2.5))):
        c = ("coilpak_p", "coilpak_b", "coilpak_b", "coilpak_p")[k]
        rod((x + cx, y, z), (x + cx, y, z + .55), .72, c, seg=24)
        rod((x + cx, y, z + .55), (x + cx, y, z + .6), .3, "sp_black", seg=12)


def barrel_truck(x, y, a=0.0):
    """SIMpull BARREL cable drum on its hand truck, payoff guide over the top."""
    ca, sa = math.cos(a), math.sin(a)
    P = lambda f, s, z: (x + f * ca - s * sa, y + f * sa + s * ca, z)
    rod(P(0, 0, .25), P(0, 0, 3.4), 1.0, "barrel_w", seg=28)
    rod(P(0, 0, 3.38), P(0, 0, 3.42), .75, "timber", seg=20)                                    # cardboard core
    rod(P(0, 0, 1.6), P(0, 0, 1.75), 1.04, "steel_dark", seg=28)                                # strap
    c = P(-1.0, 0, 2.0)
    decal(c, (-ca, -sa, 0), 1.4, 1.0, [("SIMpull BARREL", .2, 1, "#ffffff"), ("SIMpull THHN", .17, 1, "#ffffff"),
                                       (BRAND, .16, 1, "#e6b089", 1)], bg="#1f3a5f")
    for s in (-.7, .7):                                                                          # hand truck frame
        rod(P(1.15, s, .3), P(1.15, s, 4.3), .07, "steel_dark", seg=6)
        rod(P(1.15, s, 4.3), P(.95, s, 4.6), .07, "steel_dark", seg=6)
        rod(P(1.5, s * 1.2, .55), P(1.5, s * 1.2 + (.25 if s > 0 else -.25), .55), .55, "tyre", seg=14)
    rod(P(.95, -.7, 4.6), P(.95, .7, 4.6), .07, "steel_dark", seg=6)
    rod(P(1.15, 0, 4.0), P(-.1, 0, 4.0), .06, "steel_dark", seg=6)                               # payoff arm
    rod(P(-.1, 0, 4.0), P(-.1, 0, 4.4), .2, "alu", seg=12)
    box(*sorted((P(-.9, -.6, 0)[0], P(1.5, .6, 0)[0])), *sorted((P(-.9, -.6, 0)[1], P(1.5, .6, 0)[1])), .0, .1, "steel_dark")


def wire_wagon(x, y):
    """Wire wagon: steel base on four casters, A-frame with two arbors of building-wire spools."""
    box(x - 2.2, x + 2.2, y - 1.6, y + 1.6, .55, .7, "steel_dark")
    for (sx, sy) in ((-2, -1.4), (2, -1.4), (-2, 1.4), (2, 1.4)):
        caster(x + sx, y + sy, .3)
    for sy in (-1.3, 1.3):
        rod((x - 1.6, y + sy, .7), (x, y + sy, 3.4), .07, "steel_dark", seg=6)
        rod((x + 1.6, y + sy, .7), (x, y + sy, 3.4), .07, "steel_dark", seg=6)
    for (zx, z, cols) in ((-0.9, 1.75, ("pvc_green", "pvc_blue")), (.5, 3.1, ("cable", "binder_w"))):
        rod((x + zx, y - 1.9, z), (x + zx, y + 1.9, z), .06, "steel", seg=6)
        for k, c in enumerate(cols):
            y0 = y - 1.1 + k * 1.3
            rod((x + zx, y0 - .05, z), (x + zx, y0, z), .75, "sp_black", seg=20)
            rod((x + zx, y0, z), (x + zx, y0 + .9, z), .62, c, seg=20)
            rod((x + zx, y0 + .9, z), (x + zx, y0 + .95, z), .75, "sp_black", seg=20)
    rod((x + 1.4, y + .3, 1.85), (x + 1.4, y - .5, 1.85), .62, "red", seg=20)
    rod((x + 2.2, y - 1.6, .7), (x + 2.2, y - 1.6, 1.8), .06, "steel_dark", seg=6)              # handle
    rod((x + 2.2, y + 1.6, .7), (x + 2.2, y + 1.6, 1.8), .06, "steel_dark", seg=6)
    rod((x + 2.2, y - 1.6, 1.8), (x + 2.2, y + 1.6, 1.8), .06, "steel_dark", seg=6)


def maxis_feeder(x, y):
    box(x - 1.3, x + 1.3, y - .9, y + .9, .9, 3.0, "sp_black")
    box(x - 1.1, x + 1.1, y - .92, y - .9, 1.3, 2.6, "louvre")
    for (sx, sy) in ((-1.1, -.8), (1.1, -.8), (-1.1, .8), (1.1, .8)):
        caster(x + sx, y + sy, .45)
    rod((x + 1.3, y, 3.0), (x + 1.3, y, 4.6), .07, "steel_dark", seg=6)
    rod((x + 1.3, y - .5, 4.6), (x + 1.3, y + .5, 4.6), .07, "steel_dark", seg=6)
    decal((x, y - .95, 2.95), (0, -1, 0), 1.6, .4, [("MAXIS FEEDER", .55, 1, "#f2c200")], bg=None)


def maxis_xd10(x, y, a=0.0, boom_deg=48):
    """Maxis XD10 puller: wheeled base, boom raised with the sheave at its head, capstan and motor."""
    ca, sa = math.cos(a), math.sin(a)
    P = lambda f, s, z: (x + f * ca - s * sa, y + f * sa + s * ca, z)
    for (f, s) in ((-1.4, -1.0), (1.4, -1.0), (-1.4, 1.0), (1.4, 1.0)):
        q = P(f, s, 0)
        rod((q[0], q[1] - .14, .38), (q[0], q[1] + .14, .38), .38, "tyre", seg=12)
        rod(P(f, s, .38), P(0, 0, .9), .09, "sp_black", seg=6)
    b0, b1 = P(-1.5, -.6, .7), P(1.5, .6, 1.0)
    box(min(b0[0], b1[0]), max(b0[0], b1[0]), min(b0[1], b1[1]), max(b0[1], b1[1]), .7, 1.0, "sp_yellow")
    rod(P(0, 0, 1.0), P(0, 0, 2.6), .22, "sp_black", seg=10)                                      # mast
    t = math.radians(boom_deg)
    head = P(4.2 * math.cos(t), 0, 2.6 + 4.2 * math.sin(t))
    rod(P(0, 0, 2.6), head, .16, "sp_black", seg=10)                                              # boom
    rod((head[0] - sa * .2, head[1] + ca * .2, head[2]), (head[0] + sa * .2, head[1] - ca * .2, head[2]), .5, "sp_yellow", seg=16)
    cap = P(-.5, 0, 2.2)
    rod((cap[0] - sa * .45, cap[1] + ca * .45, cap[2]), (cap[0] + sa * .45, cap[1] - ca * .45, cap[2]), .35, "alu", seg=14)  # capstan
    m = P(-.9, 0, 2.2)
    box(m[0] - .4, m[0] + .4, m[1] - .4, m[1] + .4, 1.8, 2.6, "sp_black")                         # motor
    return head


def triggers_box(x, y, z=0.0):
    box(x - .35, x + .35, y - .2, y + .2, z, z + .9, "sp_yellow")
    box(x - .2, x + .2, y - .22, y - .2, z + .5, z + .75, "led_g")
    rod((x + .25, y, z + .9), (x + .25, y, z + 1.4), .03, "sp_black", seg=6)


def tension_monitor(x, y, z=0.0):
    box(x - .5, x + .5, y - .25, y + .25, z, z + .7, "sp_black")
    box(x - .3, x + .3, y - .27, y - .25, z + .3, z + .6, "hmi")
    for s in (-.65, .65):
        rod((x + s, y, z + .2), (x + s, y, z + .5), .18, "alu", seg=10)


# ------------------------------------------------------------------------------- temporary power / lighting
def generator_trailer(x, y, kw=150, axis="x"):
    """Towable generator on a single-axle trailer (enclosure, fuel tank base, tongue)."""
    L, W = (12, 5.6) if kw >= 100 else (8, 4.6)
    box(x - L / 2, x + L / 2, y - W / 2, y + W / 2, 1.5, 2.3, "steel_dark")                       # base tank
    box(x - L / 2 + .2, x + L / 2 - .2, y - W / 2 + .1, y + W / 2 - .1, 2.3, 7.2, "white_truck")
    box(x + L / 2 - 2, x + L / 2 - .3, y - W / 2 + .08, y + W / 2 - .08, 3.0, 6.5, "louvre")
    rod((x - 1, y - W / 2 - .3, 1.3), (x - 1, y - W / 2 + .3, 1.3), 1.3, "tyre", seg=14)
    rod((x - 1, y + W / 2 - .3, 1.3), (x - 1, y + W / 2 + .3, 1.3), 1.3, "tyre", seg=14)
    rod((x - L / 2, y, 1.6), (x - L / 2 - 4, y, 1.4), .12, "steel_dark", seg=6)                   # tongue
    rod((x - L / 2 - 3.6, y, 0), (x - L / 2 - 3.6, y, 1.4), .08, "steel", seg=6)                  # jack
    rod((x + 2, y, 7.2), (x + 2, y, 8.2), .25, "steel", seg=10)                                     # exhaust
    box(x - 1.5, x + 1.5, y - W / 2 - .02, y - W / 2, 3.2, 5.2, "steel_dark")                       # lug panel / cam-locks
    for k, c in enumerate(("camlock_r", "camlock_b", "camlock_w", "camlock_g", "cable")):
        rod((x - 1.2 + k * .6, y - W / 2, 3.6), (x - 1.2 + k * .6, y - W / 2 - .2, 3.6), .1, c, seg=8)
    decal((x, y - W / 2 - .03, 6.0), (0, -1, 0), 4.2, .8, [(f"{kw} kW  ·  480 V  ·  TEMPORARY POWER", .5, 1, INK)], bg=None)


def cord(pts, c="cable", r=.08):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=8)


def three_phase_cart(x, y):
    box(x - 1.2, x + 1.2, y - .9, y + .9, .6, 4.2, "panel_in")
    box(x - 1.0, x + 1.0, y - .92, y - .9, 2.4, 3.8, "steel_dark")
    for (sx, sy) in ((-1, -.7), (1, -.7), (-1, .7), (1, .7)):
        caster(x + sx, y + sy, .3)
    decal((x, y - .95, 3.1), (0, -1, 0), 1.7, .8, [("480 V 3-PHASE", .3, 1, "#ffffff"), ("100-600 A", .26, 0, "#dddddd")], bg="#2a2d30")


def spider_box(x, y):
    """Power distribution box (yellow) on its frame, GFCI receptacles."""
    box(x - .9, x + .9, y - .6, y + .6, .35, 1.5, "sp_yellow")
    for (sx, sy) in ((-1, -.7), (1, -.7), (-1, .7), (1, .7)):
        rod((x + sx, y + sy, 0), (x + sx, y + sy, 1.7), .05, "sp_black", seg=6)
    rod((x - 1, y - .7, 1.7), (x + 1, y - .7, 1.7), .05, "sp_black", seg=6)
    rod((x - 1, y + .7, 1.7), (x + 1, y + .7, 1.7), .05, "sp_black", seg=6)
    for k in range(4):
        box(x - .75 + k * .4, x - .5 + k * .4, y - .62, y - .6, .9, 1.25, "sp_black")


def tripod_light(x, y, h=9.0):
    for k in range(3):
        t = k * 2 * math.pi / 3
        rod((x + 1.6 * math.cos(t), y + 1.6 * math.sin(t), 0), (x, y, 3.0), .05, "sp_yellow", seg=6)
    rod((x, y, 3.0), (x, y, h), .06, "sp_yellow", seg=6)
    rod((x - 1.3, y, h), (x + 1.3, y, h), .05, "sp_yellow", seg=6)
    for s in (-.85, .85):
        box(x + s - .45, x + s + .45, y - .15, y + .15, h - .45, h + .35, "sp_black")
        box(x + s - .4, x + s + .4, y - .17, y - .15, h - .4, h + .3, "lamp_in")


def area_light(x, y):
    rod((x, y, 0), (x, y, 1.0), .75, "sp_yellow", r2=.55, seg=18)
    rod((x, y, 1.0), (x, y, 2.6), .55, "lamp_in", r2=.45, seg=18)


def ext_cord_coil(x, y, c="sp_yellow"):
    rod((x, y, 0), (x, y, .3), .8, c, seg=18)
    rod((x, y, .3), (x, y, .32), .45, "pad", seg=12)


def tool_container(x, y):
    """20 ft tool & equipment container, doors open to the south."""
    box(x - 10, x + 10, y - 4, y + 4, 0, 8.5, "sp_black")
    for k in range(13):
        xx = x - 9 + k * 1.5
        box(xx, xx + .5, y - 4.08, y - 4, .4, 8.1, "steel_dark")
        box(xx, xx + .5, y + 4, y + 4.08, .4, 8.1, "steel_dark")
    decal((x, y + 4.1, 5.6), (0, 1, 0), 12, 2.0, [(BRAND, .42, 1, "#e6b089", 1), ("TOOLS & EQUIPMENT", .3, 1, "#ffffff")], bg=None, brand=True)
    decal((x, y + 4.1, 5.6), (0, 1, 0), 12, 2.0, [("TOOLS & EQUIPMENT", .42, 1, "#ffffff")], bg=None, generic_only=True)


def lifted(z, fn, *a, **k):
    """Build fn at grade, then lift its parts and decals by z (equipment standing on a floor or deck)."""
    P, Dc = fuel.G["parts"], fuel.G.setdefault("decals", [])
    n, m = len(P), len(Dc)
    out = fn(*a, **k)
    for p in P[n:]:
        for key in ("min", "max", "a", "b"):
            if key in p:
                p[key][2] = round(p[key][2] + z, 2)
        if "v" in p:
            for v in p["v"]:
                v[2] = round(v[2] + z, 3)
    for d in Dc[m:]:
        d["c"][2] = round(d["c"][2] + z, 3)
    return out


# ------------------------------------------------------------------------------- places
def reel_yard_staging():
    it = fuel.new_item("BASE_SERVICES", "Reel yard: SIMpull / Maxis staging (reels on cradles, reel rollers, flanges, stack reels, carts, pullers, temporary power)",
                       (204, 316, 800, 896), (0, 14), basis="typical", register=False, area="F",
                       sheet="typical (cable installation)",
                       info="Staging for outage and expansion cable work: SIMpull Reels on SIMpull Cradles (paralleled colour-coded "
                            "feeders), RR-SW45 / RR-SW30 reel rollers carrying 35 kV MV-105 steel reels, SIMpull Flanges on wooden "
                            "reels, SIMpull Stack reels on Maxis JAX stands, CoilPAK cart, wire wagon, SIMpull BARREL drums on hand "
                            "trucks, Maxis Feeder and XD10 puller, tool container; temporary power (150 kW generator, cam-lock cords, "
                            "480 V cart, distribution boxes) and LED work lights. Cable supplier: Southwire (as requested).")
    fuel.on(it)
    fuel.D = True
    for k in range(6):                                                          # SIMpull Reels on cradles
        cols = (FEEDER, ("cable", "red", "pvc_blue", "binder_w"), ("cable", "cable", "cable", "pvc_green"))[k % 3]
        sp_reel(212 + k * 8.0, 816, axis="y", cols=cols, label=("SIMpull THHN  4 x 500 KCMIL", "SIMpull THHN  3 x 350 KCMIL",
                                                               "SIMpull XHHW-2  4/0 AWG")[k % 3])
    reel_roller(276, 820, 45, 9.0, 5.4, "cable_mv", "MV-105 35 kV 750 KCMIL")
    reel_roller(298, 820, 45, 8.4, 5.0, "cable_mv", "MV-105 15 kV 500 KCMIL")
    reel_roller(298, 852, 30, 7.4, 4.6, "cable_armor", "ARMOR-X MC-HL 15 kV")
    for k in range(3):                                                          # SIMpull Flanges on wooden reels
        flange_reel(212 + k * 7.5, 846, "y")
    stack_reel(240, 848)
    stack_reel(256, 848, cols=("cable", "red", "pvc_blue", "binder_w"))
    tool_container(270, 886)
    wire_wagon(214, 866)
    coilpak_cart(222, 866)
    barrel_truck(229, 865, 0.0)
    barrel_truck(234, 865, 0.0)
    maxis_feeder(242, 866)
    maxis_xd10(252, 868, 0.0, boom_deg=30)
    # temporary power: generator -> cam-lock cords -> 480 V cart -> distribution boxes -> lights / cords
    generator_trailer(226, 886)
    three_phase_cart(242, 883)
    cord([(225.2, 883.1, 3.6), (225.2, 882.2, .1), (240.8, 882.2, .1), (241.2, 882.8, 1.0)], "cable", .1)
    spider_box(286, 838)
    spider_box(232, 832)
    cord([(242.6, 882.1, .1), (243, 838, .08), (284.8, 838, .08)], "cable", .08)
    cord([(243, 838, .08), (233, 832.6, .08)], "cable", .08)
    for (x, y) in ((206.5, 830), (266, 836), (310, 836), (306, 872)):
        tripod_light(x, y)
    cord([(286.9, 838.2, .9), (305, 836.5, .05), (310, 836, .05)], "sp_yellow", .05)
    cord([(232.9, 832, .9), (210, 830.5, .05), (206.5, 830, .05)], "sp_yellow", .05)
    area_light(248, 840)
    ext_cord_coil(236, 838)
    ext_cord_coil(237.8, 836.5, "pvc_blue")
    person(250, 822, 0, 1.6, vest="hivis_o")                                    # checking a reel tag
    person(296, 828.5, 0, 3.1)                                                  # roller pendant
    fuel.D = False


def feeder_pull_workshop():
    """Active pull at the maintenance building's north wall: a new 400 A welding-shop feeder (4 x 500 kcmil +
    ground, SIMpull THHN with SIMpull Heads) off a SIMpull Reel into the wireway and conduit riser; branch
    circuits from a SIMpull BARREL and a wire wagon into the second conduit; Triggers safety switch, tension
    monitor, temporary power and work light."""
    it = fuel.new_item("BASE_SERVICES", "Cable pull: welding-shop feeder into the maintenance-building wireway (SIMpull Reel, BARREL, wire wagon)",
                       (238, 272, 641.2, 664), (0, 16), basis="typical", register=False, area="F",
                       sheet="typical (cable installation)",
                       info="New 400 A feeder for the workshop welding panel: SIMpull THHN 4 x 500 kcmil + ground paralleled on a "
                            "SIMpull Reel with factory SIMpull Head pulling grips, fed into the wall wireway and conduit riser; the "
                            "puller is inside at the panel. Branch circuits from a SIMpull BARREL drum and a wire wagon. Triggers "
                            "wireless safety switch, tension monitor, temporary power and light. Cable supplier: Southwire.")
    fuel.on(it)
    fuel.D = True
    yw = 641.0                                                                  # north face of the workshop
    # wireway (pull box) on the wall with two conduit risers into the building at EL 13
    box(250, 252.6, yw, yw + .7, 2.2, 10.0, "steel")
    box(250.1, 252.5, yw + .7, yw + .74, 2.4, 9.8, "alu")
    for xx in (250.7, 251.9):
        rod((xx, yw + .35, 10.0), (xx, yw + .35, 13.0), .2, "alu", seg=12)
        rod((xx, yw + .35, 13.0), (xx, yw - .3, 13.0), .2, "alu", seg=12)
    decal((251.3, yw + .76, 8.8), (0, 1, 0), 1.6, .8, [("DANGER", .3, 1, "#ffffff", 0, "#c41f27"), ("480 V", .3, 1, INK)], bg="#ffffff")
    # SIMpull Reel on its cradle, paralleled conductors with SIMpull Heads run to the wireway mouth
    pt = sp_reel(258, 656, axis="x", cols=FEEDER, label="SIMpull THHN  4 x 500 + 1/0 G")
    for k, c in enumerate(FEEDER):
        a = pt(-1.0 + k * .45, -2.2, .3)
        m = (a[0] - 3, yw + 6, 3.6)
        b = (250.6 + k * .32, yw + .8, 3.0)
        rod(a, m, .09, c, seg=8)
        rod(m, b, .09, c, seg=8)
        rod(b, (b[0], yw + .5, 3.0), .11, "alu", r2=.07, seg=10)                # SIMpull Head entering
    tension_monitor(253.5, yw + 3.2)
    triggers_box(255.5, yw + 2.5)
    # branch circuits from a SIMpull BARREL and the wire wagon into a 1-1/4 in conduit
    rod((246.5, yw + .3, 1.5), (246.5, yw + .3, 13.0), .1, "alu", seg=10)
    barrel_truck(244, 648.5, math.pi / 2)
    for k, c in enumerate(("cable", "red", "pvc_blue", "binder_w", "pvc_green")):
        rod((244 + (k - 2) * .1, 648.5, 4.4), (246.5 + (k - 2) * .03, yw + .5, 1.6), .025, c, seg=6)
    wire_wagon(240, 656)
    # temporary power and light
    spider_box(265, 646)
    cord([(264.1, 646, .9), (262, 652, .05), (262, 680, .05)], "cable", .08)    # cam-lock feed back to the yard cart
    tripod_light(268, 652)
    person(250, 650, 0, -1.4, vest="hivis_o")                                  # feeding the heads into the wireway
    person(254.5, 652.5, 0, -2.0)                                              # at the reel
    person(256, yw + 3.6, 0, -1.6)                                              # tension monitor / radio
    fuel.D = False


def build():
    reel_yard_staging()
    feeder_pull_workshop()
    return 2
