"""Standardized pre-wired kits for the two most repetitive parts of the campus (owner, Oct 26), staged where they are
used, next to the three skid kits on the pre-wire pad (skid_prewire.kits):
- KIT 4, BESS block kit, inside the BESS yard south of the first container row (x 1622-1668, y 408-452): one kit per
  block of two containers and one PCS / MV skid. It holds a two-reel stand of 2 kV DC home runs, cut and tagged + / -
  by rack string; a crate of 35 kV MV-105 collection jumpers with separable elbow connectors; a harness cart for the
  auxiliary, BMS and fire-alarm circuits; and a coil of bare copper grounding with compression lugs. The board notes
  15 identical blocks plus 5 at the BTM BESS.
- KIT 5, modular generator kit, on the reserved phase-2 pad beside the SC-3 PCM pad (x 1952-2026, y 1299-1333),
  waiting for the next unit (the modular yard is already built): one kit per engine or package. It holds a crate of 13.8 kV MV-105 generator leads with lugs; a cart of plug-in control
  and comms harnesses with multi-pin connectors; and a cam-lock set of Type W / SHD-GC for the portable and bridge-power
  units (colour-coded cam-locks).
Branded labels have generic twins. Typical, not engineered."""
import math

import fuel
from fuel import box, rod

BRAND = "SOUTHWIRE"


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def label(c, n, lines, w=4.4, h=1.7, bg="#ffffff", brand_col="#b4591f"):
    decal(c, n, w, h, [(BRAND, .19, 1, brand_col, 1)] + lines, bg=bg, brand=True)
    decal(c, n, w, h, lines, bg=bg, generic_only=True)


def sign_posts(x, y, w, h=4.4):
    for sx in (-w / 2 + .2, w / 2 - .2):
        rod((x + sx, y, 0), (x + sx, y, h), .06, "steel", seg=6)


def person(x, y, a=0.0, vest="hivis"):
    import maintenance
    maintenance.person(x, y, 0.0, a, vest=vest)


def board(x, y, lines):
    """A kit board on two posts, facing -y."""
    for sx in (-3.2, 3.2):
        rod((x + sx, y + .1, 0), (x + sx, y + .1, 6.4), .1, "steel", seg=6)
    decal((x, y, 4.4), (0, -1, 0), 7.0, 3.8, [(BRAND, .12, 1, "#e6b089", 1)] + lines, bg="#22303a", brand=True)
    decal((x, y, 4.4), (0, -1, 0), 7.0, 3.8, lines, bg="#22303a", generic_only=True)


def crate(x, y, w=4.8, d=3.6, h=2.0):
    box(x - w / 2, x + w / 2, y - d / 2, y + d / 2, 0, .4, "timber")
    for (a0, a1, b0, b1) in ((-w / 2, w / 2, -d / 2, -d / 2 + .2), (-w / 2, w / 2, d / 2 - .2, d / 2),
                             (-w / 2, -w / 2 + .2, -d / 2, d / 2), (w / 2 - .2, w / 2, -d / 2, d / 2)):
        box(x + a0, x + a1, y + b0, y + b1, .4, h, "timber")


def cart(x, y):
    box(x - 3, x + 3, y - 1.5, y + 1.5, .6, .75, "steel")
    box(x - 3, x + 3, y - 1.5, y + 1.5, 2.4, 2.55, "steel")
    for (sx, sy) in ((-2.9, -1.4), (2.9, -1.4), (-2.9, 1.4), (2.9, 1.4)):
        rod((x + sx, y + sy, 0), (x + sx, y + sy, 2.55), .06, "steel", seg=6)


# ------------------------------------------------------------------------------------------------ KIT 4: BESS block
def bess_kit():
    x0, y0 = 1622.0, 410.0
    # 2 kV DC home runs: two reels (red +, black -) on a reel stand pair, cut lengths tagged by rack string
    for k, c in enumerate(("red", "cable")):
        rx = x0 + 4 + k * 6.5
        for s_ in (-1.6, 1.6):
            rod((rx + s_, y0 + 2 - 1.3, 0), (rx + s_, y0 + 2, 3.4), .08, "steel", seg=6)
            rod((rx + s_, y0 + 2 + 1.3, 0), (rx + s_, y0 + 2, 3.4), .08, "steel", seg=6)
        rod((rx - 1.9, y0 + 2, 3.4), (rx + 1.9, y0 + 2, 3.4), .08, "steel", seg=8)
        import simpull
        for sg in (-1, 1):
            simpull.logo_flange((rx + sg * 1.25, y0 + 2, 3.4), (sg, 0), 2.6, .15, spokes=8, gap=.1)
        rod((rx - 1.1, y0 + 2, 3.4), (rx + 1.1, y0 + 2, 3.4), 2.1, c, seg=20)
        for j in range(3):                                                                    # tagged cut ends
            ex = rx - .8 + j * .8
            rod((ex, y0 + .4, 2.0), (ex, y0 - .4, .3), .07, c, seg=6)
            box(ex - .12, ex + .12, y0 - .55, y0 - .45, .3, .7, "white_truck")
    label((x0 + 7.2, y0 - 1.0, 5.6), (0, -1, 0), [("2 kV DC HOME RUNS", .2, 1, "#111111"), ("+ / - cut and tagged by rack string", .15, 0, "#333333")])
    sign_posts(x0 + 7.2, y0 - .9, 4.4, 5.6)
    # 35 kV collection jumpers with separable elbows
    cx, cy = x0 + 22.0, y0 + 2.0
    crate(cx, cy)
    for k in range(3):
        px = cx - 1.4 + k * 1.4
        rod((px, cy - .8, .9), (px, cy + .8, .9), .55, "cable_mv", seg=16)
        rod((px, cy + .9, 1.4), (px, cy + .9, 2.6), .14, "cable_mv", seg=8)
        rod((px, cy + .9, 2.6), (px, cy + .2, 3.3), .22, "sp_black", seg=10)                 # separable elbow
        rod((px, cy + .2, 3.3), (px, cy - .1, 3.3), .12, "sp_black", seg=8)
    label((cx, cy - 1.9, 3.2), (0, -1, 0), [("35 kV COLLECTION JUMPERS", .2, 1, "#111111"), ("MV-105 · separable elbows on", .15, 0, "#333333")])
    sign_posts(cx, cy - 1.85, 4.4, 4.0)
    # auxiliary / BMS / fire-alarm harness cart
    hx, hy = x0 + 34.0, y0 + 2.0
    cart(hx, hy)
    for k, c in enumerate(("cable_tc", "cable_inst", "cable_fa", "cable_tc", "cable_fo", "cable_inst")):
        tz = .75 if k < 3 else 2.55
        cx_ = hx - 2.0 + (k % 3) * 2.0
        rod((cx_ - .6, hy, tz + .35), (cx_ + .6, hy, tz + .35), .35, c, seg=14)
        box(cx_ + .55, cx_ + .75, hy + .2, hy + .4, tz + .5, tz + .8, "white_truck")
    label((hx, hy - 1.6, 3.6), (0, -1, 0), [("AUX · BMS · FIRE-ALARM HARNESS", .2, 1, "#111111"), ("per container pair, tested", .15, 0, "#333333")])
    sign_posts(hx, hy - 1.6, 4.4, 4.4)
    # grounding: bare copper coil with compression lugs
    gx, gy = x0 + 44.0, y0 + 2.0
    box(gx - 2, gx + 2, gy - 2, gy + 2, 0, .45, "timber")
    for l in range(4):
        pts = [(gx + 1.5 * math.cos(2 * math.pi * i / 24), gy + 1.5 * math.sin(2 * math.pi * i / 24), .6 + l * .12) for i in range(25)]
        for a, b in zip(pts, pts[1:]):
            rod(a, b, .06, "copper", seg=6)
    box(gx - .6, gx + .6, gy - .4, gy + .4, .45, .9, "steel_dark")                            # box of lugs
    # the board
    board(x0 + 22.0, y0 + 30.0, [("KIT 4  ·  BESS BLOCK KIT", .16, 1, "#ffffff"),
                                 ("per 2 containers + 1 PCS / MV skid", .11, 0, "#e6e6e6"),
                                 ("DC home runs · 35 kV elbow jumpers", .11, 0, "#e6e6e6"),
                                 ("aux / BMS / FA harness · grounding", .11, 0, "#e6e6e6"),
                                 ("15 identical blocks here + 5 at the BTM BESS", .1, 1, "#f2c200")])
    person(x0 + 16.0, y0 + 6.0, -math.pi / 2)
    return 1


# ------------------------------------------------------------------------------------------------ KIT 5: modular gen
def modular_kit():
    x0, y0 = 1958.0, 1305.0                                  # on the reserved phase-2 pad, beside the SC-3 PCM pad
    # 13.8 kV generator leads, terminated
    cx, cy = x0 + 3.0, y0 + 2.0
    crate(cx, cy)
    for k in range(3):
        px = cx - 1.4 + k * 1.4
        rod((px, cy - .8, .9), (px, cy + .8, .9), .6, "cable_mv", seg=16)
        rod((px, cy + .9, 1.4), (px, cy + .9, 2.8), .14, "cable_mv", seg=8)
        rod((px, cy + .9, 2.8), (px, cy + .9, 3.2), .2, "tent", r2=.1, seg=10)
        box(px - .1, px + .1, cy + .82, cy + .98, 3.2, 3.55, "copper")
    label((cx, cy - 1.9, 3.2), (0, -1, 0), [("13.8 kV GENERATOR LEADS", .2, 1, "#111111"), ("MV-105 · terminated · per engine", .15, 0, "#333333")])
    sign_posts(cx, cy - 1.85, 4.4, 4.0)
    # plug-in control and comms harnesses with multi-pin connectors
    hx, hy = x0 + 15.0, y0 + 2.0
    cart(hx, hy)
    for k, c in enumerate(("cable_tc", "cable_inst", "cable_fo", "cable_tc", "cable_inst", "cable_tc")):
        tz = .75 if k < 3 else 2.55
        cx_ = hx - 2.0 + (k % 3) * 2.0
        rod((cx_ - .6, hy, tz + .35), (cx_ + .6, hy, tz + .35), .35, c, seg=14)
        rod((cx_ + .2, hy - .3, tz + .35), (cx_ + .2, hy - 1.2, tz + .1), .05, c, seg=4)
        rod((cx_ + .2, hy - 1.2, tz + .1), (cx_ + .2, hy - 1.5, tz + .1), .16, "sp_black", seg=10)   # multi-pin plug
        rod((cx_ + .2, hy - 1.5, tz + .1), (cx_ + .2, hy - 1.58, tz + .1), .18, "alu", seg=10)
    label((hx, hy - 1.7, 3.6), (0, -1, 0), [("PLUG-IN CONTROL & COMMS", .2, 1, "#111111"), ("multi-pin connectors · per module joint", .15, 0, "#333333")])
    sign_posts(hx, hy - 1.7, 4.4, 4.4)
    # cam-lock portable power set: Type W / SHD-GC, colour-coded heads, on a cart
    kx, ky = x0 + 27.0, y0 + 2.0
    cart(kx, ky)
    for k, c in enumerate(("camlock_b", "camlock_r", "camlock_w", "camlock_g", "camlock_b")):
        cx_ = kx - 2.2 + k * 1.1
        rod((cx_, ky - .6, 1.15), (cx_, ky + .6, 1.15), .4, "cable", seg=14)                  # coiled single
        rod((cx_, ky - 1.2, 1.0), (cx_, ky - 1.5, 1.0), .16, c, seg=10)                       # cam-lock head
        rod((cx_, ky - .7, 1.0), (cx_, ky - 1.2, 1.0), .07, "cable", seg=6)
    for k in range(2):
        rod((kx - 1.6 + k * 3.2, ky - .6, 3.0), (kx - 1.6 + k * 3.2, ky + .6, 3.0), .42, "cable_shd", seg=14)   # SHD-GC
    label((kx, ky - 1.7, 3.6), (0, -1, 0), [("CAM-LOCK PORTABLE SETS", .2, 1, "#111111"), ("Type W · SHD-GC · bridge power", .15, 0, "#333333")])
    sign_posts(kx, ky - 1.7, 4.4, 4.4)
    board(x0 + 15.0, y0 + 25.5, [("KIT 5  ·  MODULAR GENERATOR KIT", .16, 1, "#ffffff"),
                                 ("per engine or package", .11, 0, "#e6e6e6"),
                                 ("13.8 kV leads terminated", .11, 0, "#e6e6e6"),
                                 ("plug-in control / comms · cam-lock sets", .11, 0, "#e6e6e6"),
                                 ("staged for the next unit on the phase-2 pad", .1, 1, "#f2c200")])
    person(x0 + 9.0, y0 + 6.0, -math.pi / 2, vest="hivis_o")
    return 1


def build():
    a = fuel.new_item("OPT_BESS", "Kit 4, BESS block kit: DC home runs, 35 kV elbow jumpers, aux / BMS / FA harness, grounding",
                      (1620, 1670, 404, 446), (0, 8), area="H", register=False, basis="typical",
                      info="Standardized pre-wired kit per BESS block (2 containers + 1 PCS / MV skid), staged in the yard: "
                           "2 kV DC home runs cut and tagged by rack string, 35 kV MV-105 collection jumpers with separable "
                           "elbows, the auxiliary / BMS / fire-alarm harness, bare-copper grounding with lugs. Typical.")
    fuel.on(a)
    fuel.D = True
    bess_kit()
    fuel.D = False
    b = fuel.new_item("OPT_MOD", "Kit 5, modular generator kit: 13.8 kV leads, plug-in control / comms harness, cam-lock sets",
                      (1952, 2026, 1299, 1333), (0, 8), area="I", register=False, basis="typical",
                      info="Standardized pre-wired kit per engine or package, staged on the reserved phase-2 pad for the next "
                           "unit: 13.8 kV "
                           "MV-105 generator leads terminated, plug-in control and comms harnesses with multi-pin connectors, "
                           "cam-lock Type W / SHD-GC sets for the portable and bridge-power units. Typical.")
    fuel.on(b)
    fuel.D = True
    modular_kit()
    fuel.D = False
    return 2
