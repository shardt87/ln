"""Control / admin building fitted out inside (SW-3X1-12 footprint 51 x 237 x 20 ft, unchanged).

The solid building box becomes walls, a roof slab and a suspended ceiling (roof, ceiling and rooftop units on
layer CR_ROOF, so a cutaway can lift them) with the rooms on CR_INTERIOR:

- Main control room (east end, 43 x 49 ft): video wall of 16 cubes (8 x 2, ~70 in each) showing the plant
  overview, the 230 kV one-line and the CCTV mosaic across 2 x 2 cubes, with dispatch, trends, ACC and alarms on
  single cubes; a six-position operator console on an arc facing the wall, each position with six monitors (2 x
  3) showing SCADA / DCS graphics, keyboards, phones, operator chairs; hard-wired GT / ST trip and ESD buttons
  under guards at the two centre positions; shift-supervisor desk on a raised platform behind; halo light over
  the console, acoustic wall panels, GPS clock, fire-alarm panel, binder shelving, printer, plants; three
  operators at the console and the shift supervisor.
- Shift-supervisor office behind a glass wall; DCS engineering / server room (two rack rows, engineering
  workstations); lobby with reception desk, safety board and entrance; conference room with a wall display;
  break room; open office; north strip with lockers, restrooms, permit office, print / document room.

Typical arrangement, not engineered. Screen images come from plant/screens (make_screens.py).
"""
import math

import fuel
from fuel import box, rod, find

L_IN, L_ROOF = "CR_INTERIOR", "CR_ROOF"
X0, X1, Y0, Y1 = 83.0, 320.0, 345.0, 396.0      # drawn footprint
T = .8                                          # wall thickness
IX0, IX1, IY0, IY1 = X0 + T, X1 - T, Y0 + T, Y1 - T
CEIL = 12.5
ROOF_Z = (17.7, 18.5)
MCR_X = 276.0                                   # west wall of the main control room
COR = (378.0, 384.0)                            # corridor (y) west of the MCR


# ------------------------------------------------------------------------------- oriented primitives
def obox(cx, cy, a, f0, f1, s0, s1, z0, z1, c):
    """Box in a local frame at (cx, cy) turned a (rad): f forward, s left; as an 8-vertex hex part."""
    ca, sa = math.cos(a), math.sin(a)

    def P(f, s, z):
        return [round(cx + f * ca - s * sa, 3), round(cy + f * sa + s * ca, 3), round(z, 3)]
    v = [P(f0, s0, z0), P(f1, s0, z0), P(f1, s1, z0), P(f0, s1, z0)]
    v += [P(f0, s0, z1), P(f1, s0, z1), P(f1, s1, z1), P(f0, s1, z1)]
    fuel._add("hex", v=v, color=c)


def lp(cx, cy, a, f, s, z):
    ca, sa = math.cos(a), math.sin(a)
    return (cx + f * ca - s * sa, cy + f * sa + s * ca, z)


def screen(c, n, w, h, img, emit=1.4):
    fuel.G.setdefault("decals", []).append(dict(c=[round(v, 3) for v in c], n=[round(v, 4) for v in n], w=w, h=h,
                                                bg="#000000", lines=[], img=img, emit=emit,
                                                item=fuel.G["cur"]["id"], layer=fuel.G["cur"]["layer"], brand=0))


def sign(c, n, w, h, lines, bg="#ffffff"):
    import showcase
    showcase.decal(c, n, w, h, lines, bg=bg)


# ------------------------------------------------------------------------------- people (no hard hats indoors)
def person_seated(x, y, a, shirt="shirt", z=0.0, typing=True):
    """Operator seated on a chair at (x, y), facing a."""
    def P(f, s, h):
        return lp(x, y, a, f, s, z + h)
    for k in (-1, 1):
        sd = .3 * k
        rod(P(-.1, sd, 1.95), P(1.45, sd, 2.0), .26, "trousers", r2=.22, seg=10)      # thigh
        rod(P(1.45, sd, 2.0), P(1.55, sd, .35), .2, "trousers", r2=.16, seg=10)       # shin
        rod(P(1.45, sd, .18), P(2.0, sd, .18), .16, "boot", r2=.13, seg=8)            # shoe
    rod(P(-.15, 0, 1.9), P(-.25, 0, 3.4), .48, shirt, r2=.52, seg=14)                 # torso
    rod(P(-.25, -.62, 3.35), P(-.25, .62, 3.35), .24, shirt, seg=10)                  # shoulders
    for k in (-1, 1):
        sd = .66 * k
        el = P(.7, sd * .95, 2.6)
        hd = P(1.95, sd * .5, 2.62) if typing else P(1.2, sd * .7, 2.45)
        rod(P(-.25, sd, 3.3), el, .17, shirt, r2=.15, seg=10)
        rod(el, hd, .14, "skin", r2=.11, seg=8)
    rod(P(-.25, 0, 3.5), P(-.22, 0, 3.8), .16, "skin", seg=8)
    rod(P(-.2, 0, 3.78), P(-.16, 0, 4.15), .3, "skin", r2=.32, seg=14)
    rod(P(-.3, 0, 3.88), P(-.26, 0, 4.2), .3, "hair", r2=.27, seg=14)            # hair, short cut
    rod(P(-.26, 0, 4.2), P(-.23, 0, 4.27), .27, "hair", r2=.12, seg=14)


def person_standing(x, y, a, shirt="shirt", z=0.0):
    def P(f, s, h):
        return lp(x, y, a, f, s, z + h)
    for k in (-1, 1):
        sd = .27 * k
        rod(P(-.1, sd, .16), P(.42, sd, .16), .16, "boot", r2=.13, seg=8)
        rod(P(0, sd, .28), P(.02, sd, 1.55), .2, "trousers", r2=.23, seg=10)
        rod(P(.02, sd, 1.55), P(0, sd, 3.05), .24, "trousers", r2=.29, seg=10)
    rod(P(0, 0, 2.95), P(.02, 0, 4.55), .47, shirt, r2=.52, seg=14)
    rod(P(0, -.6, 4.52), P(0, .6, 4.52), .24, shirt, seg=10)
    for k in (-1, 1):
        sd = .66 * k
        rod(P(0, sd, 4.48), P(.12, sd * 1.02, 3.6), .16, shirt, r2=.14, seg=8)
        rod(P(.12, sd * 1.02, 3.6), P(.35, sd * .9, 2.95), .13, "skin", r2=.1, seg=8)
    rod(P(0, 0, 4.66), P(0, 0, 4.98), .16, "skin", seg=8)
    rod(P(.02, 0, 4.96), P(.03, 0, 5.32), .3, "skin", r2=.32, seg=14)
    rod(P(-.07, 0, 5.04), P(-.04, 0, 5.36), .3, "hair", r2=.27, seg=14)
    rod(P(-.04, 0, 5.36), P(-.02, 0, 5.43), .27, "hair", r2=.12, seg=14)


# ------------------------------------------------------------------------------- furniture
def chair(x, y, a, z=0.0):
    """Operator chair (24/7): five-star base, gas column, seat, high back, armrests."""
    for k in range(5):
        t = a + k * 2 * math.pi / 5
        rod((x, y, z + .3), (x + 1.05 * math.cos(t), y + 1.05 * math.sin(t), z + .22), .07, "steel_dark", seg=6)
        rod((x + 1.05 * math.cos(t), y + 1.05 * math.sin(t), z + .12), (x + 1.05 * math.cos(t), y + 1.05 * math.sin(t), z + .14),
            .12, "tyre", seg=8)
    rod((x, y, z + .3), (x, y, z + 1.55), .1, "steel", seg=8)
    obox(x, y, a, -.85, .85, -.85, .85, z + 1.55, z + 1.85, "chair")
    obox(x, y, a, -1.05, -.85, -.8, .8, z + 1.9, z + 4.3, "chair")
    for k in (-1, 1):
        obox(x, y, a, -.6, .45, k * .85 - .08, k * .85 + .08, z + 2.55, z + 2.65, "chair")
        rod(lp(x, y, a, -.1, k * .85, z + 1.85), lp(x, y, a, -.1, k * .85, z + 2.55), .05, "steel_dark", seg=6)


def office_chair(x, y, a):
    chair(x, y, a)


def plain_chair(x, y, a, c="chair"):
    obox(x, y, a, -.75, .75, -.75, .75, 1.45, 1.6, c)
    obox(x, y, a, -.85, -.72, -.7, .7, 1.6, 3.2, c)
    for (f, s) in ((-.6, -.6), (-.6, .6), (.6, -.6), (.6, .6)):
        rod(lp(x, y, a, f, s, 0), lp(x, y, a, f, s, 1.45), .05, "steel", seg=6)


def console_position(cx, cy, a, imgs, esd=False, phone=True):
    """One operator position; (cx, cy) the front edge of the worktop, a the facing direction (toward the wall)."""
    # worktop (charcoal laminate with a soft front edge), body, knee space, monitor bridge
    obox(cx, cy, a, 0, 3.1, -3.05, 3.05, 2.38, 2.5, "desk")
    rod(lp(cx, cy, a, 0, -3.05, 2.44), lp(cx, cy, a, 0, 3.05, 2.44), .07, "steel_dark", seg=8)
    obox(cx, cy, a, 1.7, 3.1, -3.0, 3.0, .05, 2.38, "console")
    obox(cx, cy, a, 1.68, 1.7, -2.6, 2.6, .5, 2.0, "louvre")                       # vent grille under the desk
    for k in (-1, 1):
        obox(cx, cy, a, .15, 1.7, k * 3.0 - .1, k * 3.0 + .1, .05, 2.38, "console")
    obox(cx, cy, a, 2.45, 3.1, -3.0, 3.0, 2.5, 2.72, "console")
    # monitors 2 x 3 (27 in), slight toe-in on the outer pair
    for r, (zb, zt) in enumerate(((2.95, 4.12), (4.22, 5.39))):
        for k, s in enumerate((-2.04, 0, 2.04)):
            ta = a + (-.14 if s > 0 else .14 if s < 0 else 0)
            mx, my, _ = lp(cx, cy, a, 2.72 - (abs(s) * .1), s, 0)
            obox(mx, my, ta, -.06, .06, -1.0, 1.0, zb - .04, zt + .04, "monitor")
            n = (-math.cos(ta), -math.sin(ta), 0)
            sx, sy, _ = lp(mx, my, ta, -.07, 0, 0)
            screen((sx, sy, (zb + zt) / 2), n, 1.92, 1.09, imgs[(r * 3 + k) % len(imgs)])
    for s in (-2.04, 0, 2.04):                                                     # VESA posts on the bridge
        rod(lp(cx, cy, a, 2.85, s, 2.72), lp(cx, cy, a, 2.85, s, 5.2), .07, "steel", seg=6)
    # keyboards, mice, phone, headset
    for s0, s1 in ((-1.7, -.25), (.25, 1.7)):
        obox(cx, cy, a, .45, .98, s0, s1, 2.5, 2.56, "monitor")
        obox(cx, cy, a, .5, .93, s0 + .05, s1 - .05, 2.56, 2.575, "keycap")
        obox(cx, cy, a, .55, .8, s1 + .15, s1 + .32, 2.5, 2.57, "monitor")
    if phone:
        obox(cx, cy, a, .45, 1.15, 2.2, 2.75, 2.5, 2.68, "monitor")
        obox(cx, cy, a, .5, .7, 2.25, 2.7, 2.68, 2.78, "monitor")
    if esd:                                                                       # hard-wired trips under guards
        obox(cx, cy, a, 1.4, 2.2, -2.9, -2.1, 2.5, 2.62, "sw_red")
        for k, s in enumerate((-2.75, -2.5, -2.25)):
            rod(lp(cx, cy, a, 1.8, s, 2.62), lp(cx, cy, a, 1.8, s, 2.7), .1, "amber", seg=10)
            rod(lp(cx, cy, a, 1.8, s, 2.7), lp(cx, cy, a, 1.8, s, 2.78), .08, "red", seg=10)


def troffer(x, y, z=CEIL):
    box(x - 1, x + 1, y - 2, y + 2, z - .06, z, "steel", layer=L_ROOF)
    box(x - .9, x + .9, y - 1.9, y + 1.9, z - .08, z - .06, "lamp_in", layer=L_ROOF)


def desk_pair(x, y, imgs, face=1):
    """Open-office desk (wood top, 2 monitors) with a chair; face +1 = user faces +y."""
    box(x - 2.6, x + 2.6, y - 1.3, y + 1.3, 2.4, 2.5, "wood")
    for k in (-1, 1):
        box(x + k * 2.5 - .08, x + k * 2.5 + .08, y - 1.2, y + 1.2, 0, 2.4, "steel")
    ym = y + face * .9
    for k, s in enumerate((-.95, .95)):
        box(x + s - .9, x + s + .9, ym - .05, ym + .05, 3.0, 4.05, "monitor")
        screen((x + s, ym - face * .07, 3.52), (0, -face, 0), 1.72, .96, imgs[k % len(imgs)], emit=1.1)
        rod((x + s, ym + face * .1, 2.5), (x + s, ym + face * .1, 3.4), .05, "steel", seg=6)
    box(x - .8, x + .8, y - face * .3 - .25, y - face * .3 + .25, 2.5, 2.55, "monitor")
    chair(x, y - face * 2.3, math.pi / 2 if face > 0 else -math.pi / 2)


def partition(x0, x1, y0, y1, z1=CEIL, c="wall_in"):
    box(x0, x1, y0, y1, 0, z1, c)


def door(x0, x1, y0, y1, h=7.2):
    box(x0, x1, y0, y1, 0, h, "door_in")


def glass_wall(x0, x1, y0, y1, z1=CEIL):
    """Glazed partition: mullions every 5 ft, head and sill rails, clear glass between."""
    along_x = (x1 - x0) > (y1 - y0)
    L = (x1 - x0) if along_x else (y1 - y0)
    n = max(1, int(L / 5))
    for k in range(n + 1):
        t = k * L / n
        if along_x:
            box(x0 + t - .08, x0 + t + .08, y0, y1, 0, z1, "steel_dark")
        else:
            box(x0, x1, y0 + t - .08, y0 + t + .08, 0, z1, "steel_dark")
    box(x0, x1, y0, y1, 0, .35, "steel_dark")
    box(x0, x1, y0, y1, 8.6, z1, "wall_in")
    if along_x:
        box(x0, x1, (y0 + y1) / 2 - .03, (y0 + y1) / 2 + .03, .35, 8.6, "glass_in")
    else:
        box((x0 + x1) / 2 - .03, (x0 + x1) / 2 + .03, y0, y1, .35, 8.6, "glass_in")


def plant_pot(x, y):
    rod((x, y, 0), (x, y, 1.6), .7, "console", r2=.8, seg=14)
    rod((x, y, 1.6), (x, y, 4.2), 1.0, "foliage", r2=.3, seg=12)
    rod((x, y, 2.4), (x, y, 3.4), 1.3, "foliage", r2=.9, seg=12)


# ------------------------------------------------------------------------------- build
def build():
    G = fuel.G
    items, parts = G["items"], G["parts"]
    cr = next(it for it in items if it["name"].startswith("Control / admin building"))
    n0 = len(parts)
    # 1. hollow the building: drop the solid box, keep parapets, windows, canopy; rooftop units to CR_ROOF
    main = max((p for p in parts if p["item"] == cr["id"] and p["kind"] == "box" and p["color"] == "building"),
               key=lambda p: (p["max"][2] - p["min"][2]) * (p["max"][0] - p["min"][0]))
    parts.remove(main)
    top = main["max"][2]
    for p in parts:
        if p["item"] == cr["id"]:
            lo = p["min"][2] if p["kind"] == "box" else min(p["a"][2], p["b"][2]) if p["kind"] == "rod" else 0
            hi_ok = p["kind"] == "box" and p["color"] == "building"
            if lo >= top - .05 and not hi_ok:
                p["layer"] = L_ROOF
    fuel.on(cr)
    fuel.D = False
    box(X0, X0 + T, Y0, Y1, 0, top, "building")
    box(X1 - T, X1, Y0, Y1, 0, top, "building")
    box(X0 + T, X1 - T, Y0, Y0 + T, 0, top, "building")
    box(X0 + T, X1 - T, Y1 - T, Y1, 0, top, "building")
    box(X0 + T, X1 - T, Y0 + T, Y1 - T, ROOF_Z[0], top, "roof", layer=L_ROOF)
    xm = (X0 + X1) / 2                                                            # entrance (detail3 glazing outside)
    fuel.D = True

    # 2. rooms
    room = fuel.new_item(L_IN, "Control / admin building interior: rooms, finishes, ceiling and lighting",
                         (IX0, IX1, IY0, IY1), (0, CEIL), area="F", sheet="SW-3X1-12", register=False,
                         info="Typical fit-out: main control room, shift-supervisor office, DCS engineering / server "
                         "room, lobby and reception, conference, break room, open office, lockers, restrooms, permit "
                         "office. Suspended ceiling at 12.5 ft.")
    fuel.on(room)
    fuel.D = True
    box(IX0, MCR_X, IY0, IY1, 0, .04, "vinyl")                                    # admin wing floor
    box(MCR_X, IX1, IY0, IY1, 0, .04, "carpet")                                   # control room carpet tiles
    box(84.6, MCR_X - .2, IY0 + .4, COR[0] - .3, .04, .05, "carpet")             # offices carpet
    box(IX0, IX1, IY0, IY1, CEIL, CEIL + .08, "ceiling", layer=L_ROOF)            # suspended ceiling
    for x in range(int(IX0) + 2, int(IX1), 2):                                     # 2 x 2 ft T-bar grid
        box(x - .03, x + .03, IY0, IY1, CEIL - .03, CEIL, "steel", layer=L_ROOF)
    for y in range(int(IY0) + 2, int(IY1), 2):
        box(IX0, IX1, y - .03, y + .03, CEIL - .03, CEIL, "steel", layer=L_ROOF)
    # walls: corridor, MCR west wall (glass by the supervisor office), room partitions, doors
    partition(IX0, MCR_X - .3, COR[0] - .3, COR[0])
    partition(IX0, MCR_X - .3, COR[1], COR[1] + .3)
    glass_wall(MCR_X - .3, MCR_X, IY0, COR[0])
    partition(MCR_X - .3, MCR_X, COR[1], IY1)
    door(MCR_X - .35, MCR_X + .05, COR[0], COR[1])                     # double door corridor -> MCR
    for xa in (258.0, 240.0, 220.0, 192.0, 166.0, 144.0):
        if True:
            partition(xa - .15, xa + .15, IY0, COR[0] - .3)
    for (xa, xb) in ((262, 265.5), (244, 247.5), (224, 227.5), (170, 176), (148, 151.5), (120, 123.5)):
        door(xa, xb, COR[0] - .35, COR[0] + .05)
    for xa in (104.0, 124.0, 144.0, 164.0, 184.0, 212.0, 232.0, 254.0):                   # north strip rooms
        partition(xa - .15, xa + .15, COR[1] + .3, IY1)
    for xa in (108, 128, 148, 168, 188, 216, 236, 258):
        door(xa, xa + 3.5, COR[1] - .05, COR[1] + .35)
    names = {(84, 104): "MEN'S LOCKERS", (104, 124): "WOMEN'S LOCKERS", (124, 144): "RESTROOMS", (144, 164): "PERMIT / WORK CONTROL",
             (164, 184): "PRINT / DOCUMENTS", (184, 212): "TRAINING", (212, 232): "TELECOM / UPS", (232, 254): "ELECTRICAL",
             (254, 275.7): "OPERATOR RELIEF ROOM"}
    for (a0, a1), nm in names.items():
        sign(((a0 + a1) / 2 + 3, COR[1] - .07, 7.9), (0, -1, 0), 3.2, .5, [(nm, .55, 1, "#ffffff")], bg="#2c3a46")
    for (a0, a1, nm) in ((258, 275.7, "SHIFT SUPERVISOR"), (240, 258, "OPERATIONS MEETING"), (220, 240, "DCS ENGINEERING"), (166, 192, "CONFERENCE"),
                         (144, 166, "BREAK ROOM"), (84, 144, "OFFICES")):
        sign(((a0 + a1) / 2, COR[0] + .07, 7.9), (0, 1, 0), 3.2, .5, [(nm, .55, 1, "#ffffff")], bg="#2c3a46")
    # interior faces of the exterior windows: glass with a sill, roller blinds half down in the MCR, at the exterior
    # windows' own height (detail3.py) so each reads as one opening, not two panes out of line
    bid = find("Control / admin building (main")["id"]
    ext = [p for p in fuel.G["parts"] if p["item"] == bid and p["kind"] == "box" and p["color"] == "window"
           and p["max"][2] - p["min"][2] < 6]
    WZ0, WZ1 = (ext[0]["min"][2], ext[0]["max"][2]) if ext else (8.0, 12.0)
    for (a0, a1, fixed, axis, sgn) in ((X0, X1, Y0, "x", -1), (X0, X1, Y1, "x", 1), (Y0, Y1, X0, "y", -1), (Y0, Y1, X1, "y", 1)):
        Lw = a1 - a0
        nw = int((Lw - 8) // 11)
        pad = (Lw - nw * 11 + 5) / 2
        for k in range(nw):
            s0 = a0 + pad + 11 * k
            inner = fixed - sgn * T
            if axis == "x":
                if abs(s0 + 3 - xm) < 9 and sgn < 0:
                    continue
                box(s0, s0 + 6, inner - sgn * .04, inner, WZ0, WZ1, "window")
                box(s0 - .2, s0 + 6.2, inner - sgn * .35, inner, WZ0 - .2, WZ0, "wall_in")
                if s0 > MCR_X:
                    box(s0, s0 + 6, inner - sgn * .1, inner - sgn * .06, WZ1 - 1.8, WZ1, "blind")
            else:
                if sgn > 0:
                    continue                                                      # east wall: video wall side
                box(inner - sgn * .04, inner, s0, s0 + 6, WZ0, WZ1, "window")
                box(inner - sgn * .35, inner, s0 - .2, s0 + 6.2, WZ0 - .2, WZ0, "wall_in")
    # ceiling lights everywhere (2 x 4 troffers), denser in the offices
    for x in range(90, int(MCR_X) - 2, 9):
        for y in (352, 362, 372, 381, 390):
            if 377 < y < 385 and x % 18:
                continue
            troffer(x + 2, y)

    # 3. main control room
    mcr = fuel.new_item(L_IN, "Main control room: video wall, operator console, supervisor desk", (MCR_X, IX1, IY0, IY1),
                        (0, CEIL), tag="MCR", area="F", sheet="SW-3X1-12", register=False,
                        info="Six-position operator console (2 x 3 monitors each) facing a 16-cube video wall; "
                        "shift-supervisor desk on a raised platform; hard-wired GT / ST trip and plant ESD under "
                        "guards. DCS / SCADA graphics, CCTV, dispatch and alarm summary on the wall.")
    fuel.on(mcr)
    fuel.D = True
    # video wall: 8 x 2 cubes on the east wall
    cw, ch = 5.33, 3.0
    yc, zb = (IY0 + IY1) / 2, 4.2
    y_left = yc + 4 * cw
    box(IX1 - .9, IX1, y_left - 8 * cw - .3, y_left + .3, 0, zb, "console")         # base cabinets
    for k in range(8):
        box(IX1 - .93, IX1 - .9, y_left - (k + 1) * cw + .2, y_left - k * cw - .2, .6, zb - .5, "louvre")
    box(IX1 - .9, IX1, y_left - 8 * cw - .3, y_left + .3, zb, zb + 2 * ch + .25, "monitor")
    box(IX1 - 1.1, IX1, y_left - 8 * cw - .6, y_left + .6, zb + 2 * ch + .25, CEIL, "acoustic")   # bulkhead
    layout = {(0, 0): "grid.png", (1, 0): "trend.png", (0, 7): "acc.png", (1, 7): "alarm.png"}
    for (nm, c0) in (("sld", 1), ("overview", 3), ("cctv", 5)):
        ext = ".jpg" if nm == "cctv" else ".png"
        for r in range(2):
            for q in range(2):
                layout[(r, c0 + q)] = f"{nm}_q{r}{q}{ext}"
    for (r, c), img in layout.items():
        yy = y_left - (c + .5) * cw
        zz = zb + ch * (1.5 - r) + .1
        screen((IX1 - .93, yy, zz), (-1, 0, 0), cw - .03, ch - .03, img, emit=1.6)
    sign((IX1 - 1.12, yc, CEIL - .45), (-1, 0, 0), 4.2, .7, [("14:32:07", .62, 1, "#ff3b2f")], bg="#111111")   # GPS clock
    sign((IX1 - 1.12, yc - 9, CEIL - .45), (-1, 0, 0), 4.6, .6, [("UTC 18:32:07   ·   60.002 Hz", .5, 1, "#3ee07a")], bg="#111111")
    sign((IX1 - 1.12, yc + 9, CEIL - .45), (-1, 0, 0), 4.6, .6, [("NET 1,668 MW   ·   AGC ON", .5, 1, "#ffb020")], bg="#111111")
    # operator console: six positions on an arc, focus at the video-wall centre
    F = (IX1 - 1.0, yc)
    R = 21.0
    sets = [["gt1.png", "overview_q00.png", "hrsg1.png", "alarm.png", "trend.png", "gt1.png"],
            ["hrsg1.png", "overview.png", "acc.png", "alarm.png", "grid.png", "trend.png"],
            ["overview.png", "sld.png", "gt1.png", "alarm.png", "trend.png", "hrsg1.png"],
            ["sld.png", "grid.png", "overview.png", "alarm.png", "trend.png", "acc.png"],
            ["acc.png", "overview.png", "trend.png", "alarm.png", "hrsg1.png", "sld.png"],
            ["cctv.jpg", "alarm.png", "overview.png", "grid.png", "trend.png", "cctv.jpg"]]
    seats = []
    for k in range(6):
        th = (k - 2.5) * .245
        cx, cy = F[0] - R * math.cos(th), F[1] + R * math.sin(th)
        a = math.atan2(F[1] - cy, F[0] - cx)
        console_position(cx, cy, a, sets[k], esd=k in (2, 3))
        sx, sy, _ = lp(cx, cy, a, -1.6, 0, 0)
        chair(sx, sy, a)
        seats.append((sx, sy, a))
    # supervisor desk on a raised platform behind the console
    px0, px1, py0, py1 = 279.5, 288.5, yc - 12, yc + 12
    box(px0, px1, py0, py1, .04, 1.0, "carpet")
    box(px0, px1, py0 - .12, py0, .04, 1.0, "steel")
    box(px0, px1, py1, py1 + .12, .04, 1.0, "steel")
    box(px1, px1 + .12, py0, py1, .04, 1.0, "steel")
    for k in range(3):                                                            # steps at the south end
        box(px0 + 2 + k * 1.1, px0 + 3.1 + k * 1.1, py0 - 2.4, py0 - .12, .04, .33 * (k + 1), "carpet")
    box(284.6, 287.8, yc - 7, yc + 7, 3.38, 3.5, "desk")
    box(286.4, 287.8, yc - 7, yc + 7, 1.0, 3.38, "console")
    for k, s in enumerate((-4.2, -2.1, 0, 2.1, 4.2)):
        box(287.3, 287.45, yc + s - 1.0, yc + s + 1.0, 3.9, 5.05, "monitor")
        screen((287.25, yc + s, 4.47), (-1, 0, 0), 1.92, 1.06, ["alarm.png", "trend.png", "overview.png", "grid.png", "sld.png"][k], emit=1.2)
    for s in (-3, 3):
        chair(283.0, yc + s, 0.0, z=1.0)
    # walls: acoustic panels, fire-alarm panel, binders, printer, meeting table, plants
    for k in range(4):
        x = 280 + k * 9.6
        box(x, x + 8, IY0 + .02, IY0 + .2, 1.2, 7.4, "acoustic")
        box(x, x + 8, IY1 - .2, IY1 - .02, 1.2, 7.4, "acoustic")
    sign((MCR_X + .1, 389, 5.6), (1, 0, 0), 2.6, 3.3, [("FIRE ALARM", .12, 1, "#ffffff", 0, "#c41f27"),
                                                      ("NORMAL", .14, 1, "#3ee07a"), ("AC POWER ON", .08, 0, "#dddddd"),
                                                      ("ZONE 1-48  OK", .08, 0, "#dddddd")], bg="#1a1d20")
    for k in range(4):                                                            # binder shelving (procedures, P&IDs)
        x = 280 + k * 4
        box(x, x + 3.6, IY1 - 1.5, IY1 - .25, 0, 7, "wood")
        for sh in range(4):
            box(x + .15, x + 3.45, IY1 - 1.4, IY1 - .3, 1 + sh * 1.6, 1.1 + sh * 1.6, "wood")
            for b in range(9):
                box(x + .2 + b * .36, x + .5 + b * .36, IY1 - 1.35, IY1 - .4, 1.1 + sh * 1.6, 2.2 + sh * 1.6,
                    ("binder_r", "binder_b", "binder_w", "binder_b", "binder_k")[(b + sh + k) % 5])
    box(297, 300, IY1 - 2.6, IY1 - .4, 0, 3.4, "panel_in")                        # printer
    box(297.3, 299.7, IY1 - 2.3, IY1 - .7, 3.4, 3.6, "monitor")
    plant_pot(MCR_X + 2, IY0 + 2.2)
    plant_pot(IX1 - 3, IY1 - 2.5)
    # halo light over the console, troffers round the edge (dimmed control-room lighting)
    hc = (F[0] - R + 2, yc)
    for k in range(28):
        t0, t1 = k * 2 * math.pi / 28, (k + 1) * 2 * math.pi / 28
        rod((hc[0] + 7 * math.cos(t0), hc[1] + 7 * math.sin(t0), 10.6), (hc[0] + 7 * math.cos(t1), hc[1] + 7 * math.sin(t1), 10.6),
            .35, "steel", seg=8)
        rod((hc[0] + 7 * math.cos(t0), hc[1] + 7 * math.sin(t0), 10.32), (hc[0] + 7 * math.cos(t1), hc[1] + 7 * math.sin(t1), 10.32),
            .12, "lamp_in", seg=6)
    for k in range(3):
        t = k * 2 * math.pi / 3
        rod((hc[0] + 7 * math.cos(t), hc[1] + 7 * math.sin(t), 10.9), (hc[0] + 7 * math.cos(t), hc[1] + 7 * math.sin(t), CEIL),
            .03, "steel", seg=6)
    for x in (282, 292, 304, 313):
        for y in (352, 364, 377, 389):
            if x < 295 and abs(y - yc) < 14:
                continue
            troffer(x, y)
    # people: three operators at the console, the shift supervisor at the platform rail
    for k in (1, 2, 4):
        sx, sy, a = seats[k]
        person_seated(sx, sy, a, shirt=("shirt", "shirt_w", "shirt")[k % 3])
    person_standing(287.4, yc + 9.6, 0.0, shirt="shirt_w", z=1.0)

    # 4. shift supervisor office (glass wall into the MCR)
    sup = fuel.new_item(L_IN, "Shift supervisor office and operations meeting room", (240.2, MCR_X - .3, IY0, COR[0] - .3),
                        (0, CEIL), area="F", sheet="SW-3X1-12", register=False)
    fuel.on(sup)
    fuel.D = True
    box(261, 271, IY0 + 3, IY0 + 6, 2.4, 2.5, "wood")
    box(261, 261.2, IY0 + 3, IY0 + 6, 0, 2.4, "steel")
    box(270.8, 271, IY0 + 3, IY0 + 6, 0, 2.4, "steel")
    for k, s in enumerate((-1, 1)):
        box(266 + s * 1.0 - .9, 266 + s * 1.0 + .9, IY0 + 3.1, IY0 + 3.2, 3.0, 4.05, "monitor")
        screen((266 + s * 1.0, IY0 + 3.27, 3.52), (0, 1, 0), 1.72, .96, ("trend.png", "alarm.png")[k], emit=1.1)
    chair(266, IY0 + 8.3, -math.pi / 2)
    box(259, 262, COR[0] - 4, COR[0] - .6, 0, 6.5, "panel_in")                  # filing cabinet / key press
    rod((249, 362, 0), (249, 362, 2.4), .25, "steel", seg=8)                     # operations meeting table
    rod((249, 362, 2.4), (249, 362, 2.5), 3.4, "wood", seg=24)
    for k in range(6):
        t = k * math.pi / 3 + .3
        plain_chair(249 + 4.4 * math.cos(t), 362 + 4.4 * math.sin(t), t + math.pi, "chair")
    box(240.15, 240.35, 358, 366, 3.2, 7.6, "monitor")
    screen((240.42, 362, 5.4), (1, 0, 0), 7.6, 4.2, "grid.png", emit=1.2)
    # 5. DCS engineering / server room
    srv = fuel.new_item(L_IN, "DCS engineering / server room: DCS servers, historian, network, engineering workstations",
                        (220.2, 239.8, IY0, COR[0] - .3), (0, CEIL), area="F", sheet="SW-3X1-12", register=False)
    fuel.on(srv)
    fuel.D = True
    for yr in (352.0, 360.0):
        for k in range(6):
            x = 222 + k * 2.1
            box(x, x + 2.0, yr, yr + 3.5, 0, 7, "rack")
            box(x + .1, x + 1.9, yr - .03, yr, .3, 6.7, "louvre")
            for j in range(10):
                box(x + .25, x + .35, yr - .05, yr - .02, 1 + j * .55, 1.08 + j * .55, ("led_g", "led_g", "led_a")[(j + k) % 3])
    box(221, 235, 371, 373.5, 2.4, 2.5, "wood")
    for k, x in enumerate((224, 228, 232)):
        box(x - .9, x + .9, 373.0, 373.1, 3.0, 4.05, "monitor")
        screen((x, 372.93, 3.52), (0, -1, 0), 1.72, .96, ("gt1.png", "sld.png", "trend.png")[k], emit=1.1)
        chair(x, 369.0, math.pi / 2)
    person_seated(228, 369.0, math.pi / 2, shirt="shirt_w")
    # 6. lobby / reception
    lob = fuel.new_item(L_IN, "Lobby and reception: reception desk, safety board, visitor seating", (192.2, 219.8, IY0, COR[0] - .3),
                        (0, CEIL), area="F", sheet="SW-3X1-12", register=False)
    fuel.on(lob)
    fuel.D = True
    box(196, 207, 362, 365, 0, 3.6, "wood")
    box(195.6, 207.4, 361.7, 365.3, 3.6, 3.75, "desk")
    box(198, 205, 365.5, 366, 0, 2.5, "wood")
    box(200.6, 202.4, 366.6, 366.7, 3.0, 4.05, "monitor")
    chair(201.5, 368.5, -math.pi / 2)
    sign((206, COR[0] - .37, 7.2), (0, -1, 0), 9.0, 2.4, [("SW-3X1  COMBINED CYCLE POWER PLANT", .17, 1, "#ffffff"),
                                                          ("3 x 1  ·  H-CLASS  ·  1,700 MW", .12, 0, "#c9d3da")], bg="#1f2a33")
    sign((193.4, COR[0] - .37, 5.2), (0, -1, 0), 4.6, 3.2, [("SAFETY FIRST", .14, 1, "#ffffff", 0, "#2f9a4a"),
                                                            ("DAYS WITHOUT A", .09, 0, "#222222"), ("LOST-TIME INJURY", .09, 0, "#222222"),
                                                            ("1,284", .28, 1, "#2f9a4a")], bg="#ffffff")
    for k in range(3):
        plain_chair(212 + k * 2.2, IY0 + 3, math.pi / 2, "fabric")
    plant_pot(194, IY0 + 2.5)
    plant_pot(218.5, IY0 + 2.5)
    # 7. conference room
    cnf = fuel.new_item(L_IN, "Conference room: table for 12, wall display", (166.2, 191.8, IY0, COR[0] - .3), (0, CEIL),
                        area="F", sheet="SW-3X1-12", register=False)
    fuel.on(cnf)
    fuel.D = True
    box(170, 188, 359, 364, 2.35, 2.5, "wood")
    for x in (172, 186):
        box(x - .5, x + .5, 360.5, 362.5, 0, 2.35, "steel_dark")
    for k in range(6):
        x = 171.5 + k * 3.0
        plain_chair(x, 357.6, math.pi / 2, "chair")
        plain_chair(x, 365.4, -math.pi / 2, "chair")
    box(166.4, 166.6, 357.5, 365.5, 3.2, 7.8, "monitor")
    screen((166.67, 361.5, 5.5), (1, 0, 0), 7.8, 4.4, "overview.png", emit=1.2)
    # 8. break room
    brk = fuel.new_item(L_IN, "Break room: kitchenette, fridge, tables", (144.2, 165.8, IY0, COR[0] - .3), (0, CEIL), area="F",
                        sheet="SW-3X1-12", register=False)
    fuel.on(brk)
    fuel.D = True
    box(146, 164, IY0 + .2, IY0 + 2.3, 0, 3.0, "wood")
    box(146, 164, IY0 + .2, IY0 + 2.5, 3.0, 3.15, "desk")
    box(146, 164, IY0 + .2, IY0 + 1.4, 4.8, 7.4, "wood")
    box(160, 163, IY0 + 2.6, IY0 + 5.4, 0, 6.2, "panel_in")                       # fridge
    for (x, y) in ((151, 366), (159, 366)):
        rod((x, y, 0), (x, y, 2.4), .2, "steel", seg=8)
        rod((x, y, 2.4), (x, y, 2.5), 2.0, "panel_in", seg=20)
        for k in range(4):
            t = k * math.pi / 2
            plain_chair(x + 2.8 * math.cos(t), y + 2.8 * math.sin(t), t + math.pi, "fabric")
    # 9. open office
    off = fuel.new_item(L_IN, "Open office: engineering, maintenance planning, chemistry, admin desks", (IX0, 143.8, IY0, COR[0] - .3),
                        (0, CEIL), area="F", sheet="SW-3X1-12", register=False)
    fuel.on(off)
    fuel.D = True
    imgs = [["trend.png", "alarm.png"], ["hrsg1.png", "trend.png"], ["sld.png", "grid.png"], ["acc.png", "gt1.png"]]
    for i, x in enumerate(range(90, 140, 7)):
        for j, (y, face) in enumerate(((353.0, 1), (362.0, -1), (369.5, 1))):
            desk_pair(x, y, imgs[(i + j) % 4], face)
        box(x - 2.8, x + 2.8, 357.4, 357.6, 0, 4.6, "fabric")                    # screen between rows
    for k, x in enumerate((97, 118, 132)):
        person_seated(x, 350.7, math.pi / 2, shirt=("shirt_w", "shirt", "shirt_w")[k], typing=True)
    # 10. lockers
    lck = fuel.new_item(L_IN, "Locker rooms and restrooms", (IX0, 143.8, COR[1] + .3, IY1), (0, CEIL), area="F",
                        sheet="SW-3X1-12", register=False)
    fuel.on(lck)
    fuel.D = True
    for x0_ in (86, 106):
        for k in range(10):
            x = x0_ + k * 1.4
            box(x, x + 1.35, IY1 - 1.6, IY1 - .2, 0, 6.5, "locker")
            box(x + .1, x + 1.25, IY1 - 1.63, IY1 - 1.6, 4.6, 5.0, "louvre")
        box(x0_ + 1, x0_ + 13, IY1 - 4.6, IY1 - 3.6, 1.4, 1.6, "wood")           # bench
    fuel.D = False
    return len(parts) - n0
