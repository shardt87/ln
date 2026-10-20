"""Control / admin building wired, and the open office caught mid fit-out (owner, Oct 20: audit the wiring inside the
building; show the reels, lighting, cable management, conduit, MC cable, fire alarm and data in the offices still
being built out, and how the wire moves through the control side and the whole building).

Before this pass the building held finishes and furniture only: no electrical room, panelboards, conduit, tray, fire
alarm devices or data distribution. Now, all on CR_INTERIOR (the roof / ceiling cutaway shows the above-ceiling
work):
- ELECTRICAL ROOM (north strip x 232-254, was the shift kitchen): the 480 V service switchboard MDP fed from the
  duct bank at the north wall (x 262), a 75 kVA 480-208/120 V dry-type transformer, panelboards LP-1 (277/480 V
  lighting), RP-1 / RP-2 (120/208 V receptacles), EP-1 (UPS-backed control-room loads), EMT risers to the ceiling;
- TELECOM / UPS ROOM (x 212-232): two-post relay racks with fibre and copper patch panels under a ladder rack, the
  UPS and its battery cabinet, the telecom grounding busbar;
- CORRIDOR BACKBONE above the ceiling (y 378-384): an 18 in wire-basket tray with the Cat 6A bundle and the orange
  fibre innerduct, three EMT power runs, the red fire-alarm (FPLR) loop on J-hooks; branches into every room: MC
  cable to the light and receptacle boxes, fire-alarm drops to the smoke detectors and horn / strobes;
- CONTROL ROOM: the tray carried on over the MCR ceiling to the video wall (cables dropping behind it) and over the
  console arc; a poke-through floor box under each console position with its power whip (MC) and data / fibre;
- SERVER ROOM: ladder rack over both rack rows with the Cat 6A, a yellow fibre trough, an overhead power busway with
  plug-in tap boxes and cords down to each rack;
- OPEN OFFICE (x 84-144) mid fit-out: carpet, furniture and ceiling tiles not in yet, bare slab, open grid; the
  data bundles on J-hooks to the future desk drops (coiled tails hanging), MC home runs from RP-1 to the wall boxes,
  some troffers hung and whipped, the rest still boxed on the floor; smoke detectors in; an MC reel on a reel stand,
  a wire cart of THHN reels, a ladder and a scissor lift with an electrician pulling MC overhead, another on a ladder.
Typical, not engineered."""
import math

import fuel
from fuel import box, rod, new_item, on

L = "CR_INTERIOR"
IX0, IX1, IY0, IY1 = 83.8, 319.2, 345.8, 395.2
CEIL, DECK = 12.5, 17.7
COR = (378.0, 384.0)
OFF = (84.6, 143.8, 346.2, 377.7)                        # open office: the fit-out area


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a, shirt="hivis", z=0.0):
    import control_room as cr
    cr.person_standing(x, y, a, shirt=shirt, z=z)


def run(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)
    return len(pts) - 1


def jhooks(x0, x1, y, z, step=5.0):
    """J-hooks hung from the deck along x."""
    n, x = 0, x0
    while x <= x1:
        rod((x, y, z - .15), (x, y, DECK), .03, "steel", seg=4)
        box(x - .05, x + .05, y - .25, y + .25, z - .2, z - .15, "steel")
        x += step
        n += 2
    return n


def basket(x0, x1, y, z, w=1.5, along="x"):
    """Wire-basket tray: two side wires, cross wires, the cable bundle in it."""
    n = 0
    if along == "x":
        for s in (-w / 2, w / 2):
            rod((x0, y + s, z + .3), (x1, y + s, z + .3), .03, "steel", seg=4)
            rod((x0, y + s, z), (x1, y + s, z), .03, "steel", seg=4)
        x = x0
        while x <= x1:
            box(x - .02, x + .02, y - w / 2, y + w / 2, z - .02, z + .02, "steel")
            x += 1.0
            n += 1
        box(x0, x1, y - w / 2 + .1, y + w / 2 - .1, z + .02, z + .22, "cable_inst")
    else:
        for s in (-w / 2, w / 2):
            rod((y + s, x0, z + .3), (y + s, x1, z + .3), .03, "steel", seg=4)
            rod((y + s, x0, z), (y + s, x1, z), .03, "steel", seg=4)
        x = x0
        while x <= x1:
            box(y - w / 2, y + w / 2, x - .02, x + .02, z - .02, z + .02, "steel")
            x += 1.0
            n += 1
        box(y - w / 2 + .1, y + w / 2 - .1, x0, x1, z + .02, z + .22, "cable_inst")
    return n + 5


def smoke(x, y):
    rod((x, y, CEIL - .12), (x, y, CEIL), .32, "panel", seg=14)
    rod((x, y, CEIL - .14), (x, y, CEIL - .12), .1, "red", seg=8)                       # LED
    return 2


def wallbox(x, y, nx, ny, z0, z1, c, d=.25, w=.25):
    """A small box on a wall face at (x, y), standing out along (nx, ny)."""
    if nx:
        xa, xb = sorted((x, x + nx * d))
        box(xa, xb, y - w, y + w, z0, z1, c)
    else:
        ya, yb = sorted((y, y + ny * d))
        box(x - w, x + w, ya, yb, z0, z1, c)
    return 1


def horn_strobe(x, y, nx, ny):
    return wallbox(x, y, nx, ny, 7.6, 8.3, "sw_red")


def pull_station(x, y, nx, ny):
    return wallbox(x, y, nx, ny, 3.8, 4.4, "sw_red", d=.2, w=.22)


def tag(c, n, w, h, t1, t2=None):
    lines = [(t1, .5 if t2 else .7, 1, "#111111")] + ([(t2, .32, 0, "#333333")] if t2 else [])
    decal(c, n, w, h, lines, bg="#ffffff")


# ------------------------------------------------------------------------------- strip the open office
def clear_office():
    """Undo the finished open office: furniture and people out, carpet and ceiling tiles not yet in, its troffers
    taken down (some re-hung below, the rest boxed on the floor)."""
    G = fuel.G
    off = next((it for it in G["items"] if it["name"].startswith("Open office:")), None)
    rooms = next(it for it in G["items"] if it["name"].startswith("Control / admin building interior:"))
    x0, x1, y0, y1 = OFF
    keep, n = [], 0
    for p in G["parts"]:
        if off and p["item"] == off["id"]:
            n += 1
            continue
        if p["item"] == rooms["id"] and p["kind"] == "box":
            lo, hi = p["min"], p["max"]
            if p["color"] == "carpet" and lo[0] < x0 + 1 and hi[0] > x1:                 # offices carpet: starts at 144
                lo[0] = x1 + .4
            elif p["color"] == "ceiling" and hi[0] - lo[0] > 200:                         # the ceiling, minus the office
                G["parts"].append(dict(p, min=[x1 + .2, lo[1], lo[2]], max=list(hi)))
                p = dict(p, min=list(lo), max=[x1 + .2, hi[1], hi[2]])
                p["min"][1] = y1 + .3
            elif p["color"] in ("steel", "lamp_in") and lo[2] > CEIL - .2 and hi[2] <= CEIL + .01 and \
                    x0 <= lo[0] and hi[0] <= x1 and y0 <= lo[1] and hi[1] <= y1 and hi[0] - lo[0] < 2.2:
                n += 1                                                                    # troffer in the office
                continue
        keep.append(p)
    G["parts"][:] = keep
    if off:
        G["decals"] = [d for d in G.get("decals", []) if d["item"] != off["id"]]
    return n


# ------------------------------------------------------------------------------- rooms of the system
def electrical_room():
    n = 0
    box(236.0, 246.0, 392.8, 395.0, 0, .3, "concrete")                                   # housekeeping pad
    box(236.5, 244.0, 393.4, 395.0, .3, 7.8, "swgr")                                      # MDP 480 V switchboard
    for k in range(3):
        box(236.8 + k * 2.4, 238.9 + k * 2.4, 393.35, 393.4, 1.0, 7.2, "panel")           # sections
    box(244.6, 249.5, 391.8, 395.0, 0, .3, "concrete")
    box(245.0, 249.0, 392.2, 394.8, .3, 5.2, "xfmr")                                      # T-1 75 kVA dry type
    box(245.2, 248.8, 392.15, 392.2, 1.0, 4.4, "louvre")
    n += 7
    tag((240.2, 393.33, 6.6), (0, -1, 0), 3.0, .8, "MDP  480 V", "SERVICE SWITCHBOARD  ·  800 A")
    tag((247.0, 392.13, 4.7), (0, -1, 0), 2.6, .7, "T-1  75 kVA", "480 - 208/120 V")
    # panelboards on the east wall (x 254), EMT risers to the ceiling space
    for k, (nm, sub) in enumerate((("LP-1", "277/480 V LIGHTING"), ("RP-1", "120/208 V RECEPT"),
                                   ("RP-2", "120/208 V RECEPT"), ("EP-1", "UPS-BACKED  ·  MCR"))):
        y = 386.0 + k * 2.3
        box(253.3, 253.85, y, y + 1.7, 2.6, 7.6, "panel")
        for j in range(3):
            rod((253.55, y + .4 + j * .45, 7.6), (253.55, y + .4 + j * .45, 15.6), .08, "pipe", seg=8)
        tag((253.28, y + .85, 7.0), (-1, 0, 0), 1.6, .55, nm, sub)
        n += 4
    # service feeder: duct bank in at the north wall (x 262), up the wall, over the ceiling into the MDP
    for j in range(3):
        yy = 394.6 - j * .45
        run([(261.6, yy, 0), (261.6, yy, 16.4), (240.0, yy, 16.4), (240.0, yy, 7.8)], .17, "pvc_grey")
        n += 3
    # feeder MDP -> T-1 -> panels, overhead
    run([(242.5, 394.0, 7.8), (242.5, 394.0, 15.0), (247.0, 394.0, 15.0), (247.0, 394.0, 5.2)], .1, "pipe")
    run([(248.0, 393.5, 5.2), (248.0, 393.5, 15.4), (253.55, 393.5, 15.4)], .1, "pipe")
    return n + 4


def telecom_room():
    n = 0
    for x in (215.5, 219.5):                                                              # two-post relay racks
        for s in (-.9, .9):
            box(x + s - .1, x + s + .1, 392.6, 392.9, 0, 7.5, "rack")
        for j in range(8):
            box(x - .8, x + .8, 392.55, 392.6, 1.5 + j * .7, 2.0 + j * .7, ("cable_fo", "rack", "cable_inst")[j % 3])
        n += 10
    box(213.0, 222.0, 391.6, 393.9, 8.4, 8.55, "steel")                                    # ladder rack over the racks
    for x in range(213, 223):
        box(x, x + .08, 391.6, 393.9, 8.55, 8.65, "steel")
    box(213.0, 222.0, 392.0, 393.5, 8.65, 9.0, "cable_inst")
    run([(217.5, 392.6, 9.0), (217.5, 386.0, 13.8), (217.5, 381.0, 14.0)], .25, "cable_inst")  # up to the corridor tray
    run([(218.3, 392.6, 9.0), (218.3, 386.0, 13.6), (218.3, 381.6, 13.8)], .2, "cable_fo")
    box(225.0, 229.0, 393.2, 395.0, 0, 6.2, "panel")                                      # UPS
    box(229.3, 231.6, 393.2, 395.0, 0, 6.2, "rack")                                       # battery cabinet
    box(224.0, 225.6, 395.05, 395.15, 6.0, 6.3, "copper")                                  # TGB
    run([(224.8, 395.1, 6.0), (224.8, 395.1, .2)], .06, "safety")                          # bonding conductor (green)
    tag((227.0, 393.17, 5.6), (0, -1, 0), 2.4, .6, "UPS-1  40 kVA", "FEEDS EP-1  ·  15 MIN")
    tag((217.5, 392.5, 7.9), (0, -1, 0), 2.6, .5, "MDF  ·  FIBRE + CAT 6A")
    return n + 20


def corridor_backbone():
    n = 0
    x0, x1 = IX0 + 1.0, IX1 - 2.0
    n += basket(x0, x1, 380.6, 14.0)                                                      # data tray, whole length
    run([(212.0, 381.0, 14.3), (x1, 381.0, 14.3)], .14, "cable_fo")                        # fibre innerduct east
    for j in range(3):                                                                    # EMT power runs
        y = 382.6 + j * .35
        run([(x0, y, 15.2), (253.6, y, 15.2)], .08, "pipe")
        run([(253.6, y, 15.2), (x1, y, 15.2)], .08, "pipe")
    n += jhooks(x0, x1, 379.0, 14.6)                                                      # fire-alarm loop
    run([(x0, 379.0, 14.6), (x1, 379.0, 14.6)], .045, "cable_fa")
    # corridor smoke detectors and horn / strobes
    x = 92.0
    while x < 276:
        n += smoke(x, 381.0)
        x += 28.0
    for x in (100.0, 160.0, 220.0, 266.0):
        n += horn_strobe(x, COR[0] + .02, 0, 1)
    return n + 9


def room_branches():
    """Every finished room: MC to its boxes, fire-alarm drop to its detector, from the corridor."""
    n = 0
    south = ((144, 166), (166, 192), (192.2, 219.8), (220.2, 239.8), (240, 258), (258, 275.7))
    north = ((84, 104), (104, 124), (124, 144), (144, 164), (164, 184), (184, 212))
    for (a0, a1) in south:
        xm = (a0 + a1) / 2
        run([(xm, 382.6, 15.2), (xm, 382.6, 15.6), (xm, 362.0, 15.6), (xm, 362.0, 13.2)], .07, "alu")       # MC home run
        box(xm - .2, xm + .2, 361.8, 362.2, 12.9, 13.2, "steel")                                          # J-box
        run([(xm + 1.0, 379.0, 14.6), (xm + 1.0, 362.0, 14.6), (xm + 1.0, 362.0, CEIL)], .04, "cable_fa")
        n += 6 + smoke(xm + 1.0, 362.0)
    for (a0, a1) in north:
        xm = (a0 + a1) / 2
        run([(xm, 382.6, 15.2), (xm, 389.5, 15.6), (xm, 389.5, 13.2)], .07, "alu")
        run([(xm + 1.0, 379.0, 14.6), (xm + 1.0, 389.5, 14.6), (xm + 1.0, 389.5, CEIL)], .04, "cable_fa")
        n += 3 + smoke(xm + 1.0, 389.5)
    for (x, y, nx, ny) in ((196.0, IY0 + .3, 0, 1), (216.0, IY0 + .3, 0, 1)):            # lobby exit pull stations
        n += pull_station(x, y, nx, ny)
    return n


def control_room():
    n = 0
    # tray carried over the MCR ceiling: east along the corridor line, along the video wall, and over the console
    n += basket(276.0, 316.0, 380.6, 14.0)
    n += basket(354.0, 380.0, 316.5, 14.0, along="y")
    n += basket(360.0, 380.0, 296.0, 14.4, along="y")
    for k in range(6):                                                                    # cables dropping behind the wall
        y = 356.0 + k * 4.4
        run([(316.5, y, 14.2), (318.6, y, 14.2), (318.6, y, 10.5 + RF)], .12, ("cable_inst", "cable_fo")[k % 2])
        n += 2
    # each console position: a poke-through floor box, its power whip and data / fibre up into the console body
    F, R = (IX1 - 1.0, (IY0 + IY1) / 2), 21.0
    for k in range(6):
        th = (k - 2.5) * .245
        cx, cy = F[0] - R * math.cos(th), F[1] + R * math.sin(th)
        a = math.atan2(F[1] - cy, F[0] - cx)
        fx, fy = cx + 2.2 * math.cos(a), cy + 2.2 * math.sin(a)                             # under the console body
        box(fx - .45, fx + .45, fy - .45, fy + .45, RF - .02, RF + .02, "rack")             # floor grommet
        run([(304.0, fy, .5), (fx - .2, fy, .5), (fx - .2, fy, 1.6 + RF)], .07, "alu")     # MC power whip, under floor
        run([(304.0, fy, .4), (fx + .1, fy, .4), (fx + .1, fy, 1.6 + RF)], .08, "cable_inst")
        run([(304.0, fy, .35), (fx + .3, fy, .35), (fx + .3, fy, 1.6 + RF)], .05, "cable_fo")
        n += 7
    # the floor-box feeds from EP-1 run in the slab (shown as the conduit run to the first box, off the MCR west wall)
    x = 280.0
    while x < 318:
        n += smoke(x, 352.0) + smoke(x, 372.0) + smoke(x, 390.0)
        x += 14.0
    n += wallbox(MCR_X + .3, 360.0, 1, 0, 7.6 + RF, 8.3 + RF, "sw_red") + \
        wallbox(MCR_X + .3, 386.0, 1, 0, 3.8 + RF, 4.4 + RF, "sw_red", d=.2, w=.22)
    return n


MCR_X = 276.0


RF = 1.0                                                    # raised access floor height in the control room
HOLES = ((278.0, 280.0, 380.0, 382.0), (303.0, 305.0, 369.0, 371.0), (314.0, 316.0, 361.0, 363.0))
RAMP = (276.2, 288.2, 378.4, 383.6)                         # entry ramp inside the corridor door, 1:12


def _rect_minus(r, holes):
    """Rectangles covering r = (x0, x1, y0, y1) minus the holes."""
    x0, x1, y0, y1 = r
    xs = sorted({x0, x1} | {h[0] for h in holes if x0 < h[0] < x1} | {h[1] for h in holes if x0 < h[1] < x1})
    out = []
    for a, b in zip(xs, xs[1:]):
        cut = sorted((h[2], h[3]) for h in holes if h[0] <= a and h[1] >= b)
        y = y0
        for c0, c1 in cut:
            if c0 > y:
                out.append((a, b, y, c0))
            y = max(y, c1)
        if y < y1:
            out.append((a, b, y, y1))
    return out


def raise_mcr():
    """A 12 in raised access floor in the main control room: everything in the MCR item goes up by RF; the carpet
    becomes the floor tiles, with three tiles lifted to show the under-floor cable and an entry ramp at the door."""
    G = fuel.G
    mcr = next(it for it in G["items"] if it["name"].startswith("Main control room:"))
    rooms = next(it for it in G["items"] if it["name"].startswith("Control / admin building interior:"))
    def zr(p):
        if "min" in p:
            return p["min"][2], p["max"][2]
        if "a" in p:
            return min(p["a"][2], p["b"][2]), max(p["a"][2], p["b"][2])
        return min(v[2] for v in p["v"]), max(v[2] for v in p["v"])
    for p in G["parts"]:
        if p["item"] != mcr["id"]:
            continue
        lo, hi = zr(p)
        if hi >= CEIL - .1 or lo >= 10.5:                     # hung from the ceiling (halo, troffers, bulkhead): stays
            if p["kind"] == "box" and p["color"] == "acoustic" and lo < 11.5:
                p["min"][2] += RF                             # the bulkhead now starts above the raised video wall
            continue
        if "min" in p:
            p["min"][2] += RF
            p["max"][2] += RF
        if "a" in p:
            p["a"][2] += RF
            p["b"][2] += RF
        if "v" in p:
            for v in p["v"]:
                v[2] += RF
    for d in G.get("decals", []):
        if d["item"] == mcr["id"] and d["c"][2] < 10.5:
            d["c"][2] += RF
    floor = next(p for p in G["parts"] if p["item"] == rooms["id"] and p["kind"] == "box" and p["color"] == "carpet"
                 and abs(p["min"][0] - MCR_X) < .01)
    G["parts"].remove(floor)
    n = 0
    for (a0, a1, b0, b1) in _rect_minus((MCR_X, IX1, IY0, IY1), HOLES + (RAMP,)):
        box(a0, a1, b0, b1, RF - .08, RF, "carpet")                                       # floor tiles
        n += 1
    for (a0, a1, b0, b1) in HOLES:                                                        # open tiles: pedestals, stringers
        for (x, y) in ((a0, b0), (a1, b0), (a0, b1), (a1, b1)):
            rod((x, y, 0), (x, y, RF - .08), .05, "steel", seg=6)
            box(x - .2, x + .2, y - .2, y + .2, RF - .12, RF - .08, "steel")
        box(a1 + .3, a1 + 2.3, b0, b1, RF, RF + .08, "carpet")                             # the lifted tile, set down
        rod((a1 + 1.3, (b0 + b1) / 2, RF + .08), (a1 + 1.3, (b0 + b1) / 2, RF + .25), .25, "panel", seg=10)  # lifter
        n += 10
    x0, x1, y0, y1 = RAMP                                                                 # entry ramp
    v = [[x0, y0, 0], [x1, y0, RF - .08], [x1, y1, RF - .08], [x0, y1, 0],
         [x0, y0, .04], [x1, y0, RF], [x1, y1, RF], [x0, y1, .04]]
    fuel._add("hex", v=v, color="carpet")
    for y in (y0 + .1, y1 - .1):
        rod((x0, y, 3.0), (x1, y, 3.0 + RF), .06, "steel", seg=6)                          # handrails
    # under-floor basket tray from the west wall to the console and the video wall, passing under the open tiles
    pts = [(277.0, 381.0), (304.0, 381.0), (304.0, 362.0), (317.0, 362.0)]
    for (a, b) in zip(pts, pts[1:]):
        if a[1] == b[1]:
            n += basket(min(a[0], b[0]), max(a[0], b[0]), a[1], .25)
        else:
            n += basket(min(a[1], b[1]), max(a[1], b[1]), a[0], .25, along="y")
        rod((a[0], a[1] + .3, .5), (b[0], b[1] + .3, .5), .07, "alu", seg=8)               # MC power alongside
        rod((a[0] + .3, a[1], .55), (b[0] + .3, b[1], .55), .05, "cable_fo", seg=8)
    return n + 3


def server_room():
    n = 0
    for yr in (352.0, 360.0):
        yc = yr + 1.75
        box(221.6, 235.4, yc - .8, yc + .8, 8.2, 8.3, "steel")                              # ladder rack
        for x in range(222, 236):
            box(x, x + .08, yc - .8, yc + .8, 8.3, 8.4, "steel")
        box(221.6, 235.4, yc - .6, yc + .2, 8.4, 8.75, "cable_inst")
        box(221.6, 235.4, yc + .3, yc + .75, 8.4, 8.8, "crane")                             # fibre trough (yellow)
        box(221.6, 235.4, yr - .4, yr - .1, 9.4, 9.8, "pipe")                                # power busway
        for k in range(6):
            x = 223.0 + k * 2.1
            box(x - .25, x + .25, yr - .45, yr - .05, 8.9, 9.4, "panel")                     # tap box
            rod((x, yr - .25, 8.9), (x, yr + .3, 7.0), .06, "cable_tc", seg=6)               # cord to the rack PDU
            n += 2
        n += 15
    run([(225.0, 381.0, 14.0), (225.0, 362.0, 13.0), (225.0, 361.75, 9.0)], .2, "cable_inst")   # from the tray
    run([(226.0, 381.0, 14.2), (226.0, 362.0, 13.2), (226.0, 362.4, 9.2)], .14, "cable_fo")
    return n + 4


# ------------------------------------------------------------------------------- the fit-out in the open office
def reel_stand(x, y):
    """MC cable reel on an A-frame reel stand (spindle through the reel), the cable paying off overhead."""
    for s in (-1.8, 1.8):
        rod((x - 1.2, y + s, 0), (x, y + s, 2.6), .08, "steel", seg=6)
        rod((x + 1.2, y + s, 0), (x, y + s, 2.6), .08, "steel", seg=6)
    rod((x, y - 2.1, 2.6), (x, y + 2.1, 2.6), .07, "steel", seg=8)                        # spindle
    for s in (-1.4, 1.2):
        rod((x, y + s, 2.6), (x, y + s + .2, 2.6), 1.9, "rack", seg=24)                  # flanges
    rod((x, y - 1.2, 2.6), (x, y + 1.2, 2.6), 1.6, "alu", seg=24)                         # MC on the reel
    run([(x, y, 4.2), (x + 2.0, y, 9.0), (x + 4.0, y, 14.6)], .07, "alu")                 # paying up to the hooks
    decal((x, y - 1.43, 2.6), (0, -1, 0), 2.6, 1.0, [("SOUTHWIRE", .42, 1, "#ffffff"), ("MC  12/2  ·  250 FT", .3, 0, "#f2f2f0")],
          bg="#c41f27", brand=True)
    return 14


def wire_cart(x, y):
    """Wire cart with six small THHN reels on two axles, the conductors pulled off together."""
    box(x - 1.6, x + 1.6, y - 1.0, y + 1.0, .5, .6, "steel")
    for s in (-1.4, 1.4):
        for t in (-.8, .8):
            rod((x + s, y + t, 0), (x + s, y + t, .5), .06, "steel", seg=6)
            rod((x + s, y + t - .1, .25), (x + s, y + t + .1, .25), .25, "rack", seg=10)   # castors
    cols = ("cable_tc", "sw_red", "cable_inst", "panel", "safety", "cable_tc")
    for k, c in enumerate(cols):
        ax = x - 1.0 + (k % 3) * 1.0
        az = 1.4 if k < 3 else 2.6
        rod((ax - .35, y, az), (ax + .35, y, az), .55, "sw_red" if k == 0 else "rack", seg=14)
        rod((ax - .25, y, az), (ax + .25, y, az), .45, c, seg=14)
    for k in range(3):
        rod((x - 1.6, y, 2.0), (x - 1.6, y, 5.5), .015, ("cable_tc", "sw_red", "safety")[k], seg=4)
    decal((x, y - 1.03, 1.0), (0, -1, 0), 2.2, .5, [("SIMpull THHN  ·  WIRE CART", .55, 1, "#111111")], bg="#ffffff",
          brand=True)
    return 30


def ladder(x, y, h=8.0):
    for s in (-.7, .7):
        rod((x - .6, y + s, 0), (x, y + s, h), .06, "amber", seg=6)
        rod((x + .6, y + s, 0), (x, y + s, h), .06, "amber", seg=6)
    for k in range(1, 7):
        z = h * k / 7
        rod((x - .6 * (1 - k / 7), y - .7, z), (x - .6 * (1 - k / 7), y + .7, z), .04, "amber", seg=4)
    return 10


def scissor_lift(x, y, deck=8.0):
    box(x - 2.6, x + 2.6, y - 1.2, y + 1.2, .3, 1.4, "amber")                              # chassis
    for s in (-1.1, 1.1):
        for t in (-1, 1):
            rod((x + t * 2.0, y + s - .15, .45), (x + t * 2.0, y + s + .15, .45), .4, "rack", seg=12)
    n = 4
    for k in range(4):                                                                     # scissor arms
        z0, z1 = 1.4 + k * (deck - 1.6) / 4, 1.4 + (k + 1) * (deck - 1.6) / 4
        for s in (-1.0, 1.0):
            rod((x - 2.2, y + s, z0), (x + 2.2, y + s, z1), .07, "steel", seg=6)
            rod((x + 2.2, y + s, z0), (x - 2.2, y + s, z1), .07, "steel", seg=6)
            n += 2
    box(x - 2.8, x + 2.8, y - 1.3, y + 1.3, deck - .2, deck, "amber")                      # platform
    for (a0, a1, b0, b1) in ((-2.8, 2.8, -1.3, -1.25), (-2.8, 2.8, 1.25, 1.3), (-2.8, -2.75, -1.3, 1.3), (2.75, 2.8, -1.3, 1.3)):
        box(x + a0, x + a1, y + b0, y + b1, deck + 3.2, deck + 3.35, "amber")                 # guard rail
    for (dx, dy) in ((-2.75, -1.25), (2.75, -1.25), (-2.75, 1.25), (2.75, 1.25)):
        rod((x + dx, y + dy, deck), (x + dx, y + dy, deck + 3.3), .05, "amber", seg=4)
    return n + 10


def cable_puller(x, y, tx, ty, tz):
    """Cable puller (tugger) on its floor stand, rope from the capstan up to the sheave at the conduit end."""
    box(x - 1.6, x + 1.6, y - 1.2, y + 1.2, 0, .3, "crane")                               # base frame
    rod((x, y, .3), (x, y, 3.6), .18, "crane", seg=8)                                     # mast
    rod((x, y - .9, 2.6), (x, y + .9, 2.6), .45, "steel", seg=16)                          # capstan
    box(x - .9, x - .2, y - .7, y + .7, 2.0, 3.2, "sw_red")                                # motor / gearbox
    rod((x + .3, y, 3.4), (tx, ty, tz), .03, "panel", seg=4)                               # pulling rope
    rod((tx, ty, tz), (tx, ty, tz + .5), .25, "steel", seg=12)                             # sheave at the conduit end
    decal((x, y - 1.23, 1.0), (0, -1, 0), 2.6, .5, [("MAXIS CABLE PULLER", .55, 1, "#111111")], bg="#e0b01a", brand=True)
    return 6


def cable_barrel(x, y, c):
    """THHN in a payoff barrel: the drum, its payoff cone, the conductor up and away to the pull."""
    rod((x, y, 0), (x, y, 3.0), 1.0, "rack", seg=20)
    rod((x, y, 3.0), (x, y, 3.6), .6, "steel", r2=.15, seg=14)                             # payoff cone
    rod((x, y, 3.6), (x, y, 5.0), .05, c, seg=6)
    decal((x, y - 1.02, 1.6), (0, -1, 0), 1.6, .8, [("SIMpull", .45, 1, "#ffffff"), ("BARREL  ·  THHN", .3, 0, "#e8e8e8")],
          bg="#c41f27", brand=True)
    return 3


def string_lights(x0, x1, y, z):
    """Temporary construction lighting: an LED stringer hung from the J-hooks, a lamp every 6 ft."""
    n = 0
    rod((x0, y, z), (x1, y, z), .03, "cable_tc", seg=4)
    x = x0 + 2
    while x < x1:
        rod((x, y, z - .5), (x, y, z), .02, "cable_tc", seg=4)
        rod((x, y, z - .9), (x, y, z - .5), .22, "lamp", r2=.12, seg=10)
        x += 6.0
        n += 2
    return n + 1


def work_light(x, y):
    for a in (0, 2.1, 4.2):
        rod((x + 1.0 * math.cos(a), y + 1.0 * math.sin(a), 0), (x, y, 4.5), .04, "steel", seg=4)
    rod((x, y, 4.5), (x, y, 6.0), .05, "steel", seg=4)
    box(x - .5, x + .5, y - .15, y + .15, 6.0, 6.8, "lamp")
    return 5


def office_fitout():
    n = clear_office()
    x0, x1, y0, y1 = OFF
    # data to the future desk drops: J-hook runs off the corridor tray, coiled tails hanging at each drop
    for yy in (352.0, 360.0, 368.0):
        run([(x1, 380.6, 14.2), (x1 - 1.0, yy, 14.4)], .14, "cable_inst")
        n += jhooks(x0 + 6.0, x1 - 2.0, yy, 14.4, step=4.5)
        run([(x1 - 1.0, yy, 14.4), (x0 + 6.0, yy, 14.4)], .14, "cable_inst")
        for xd in (96.0, 112.0, 128.0):
            run([(xd, yy, 14.3), (xd, yy, 9.5)], .09, "cable_inst")                       # drop to the desk cluster
            rod((xd, yy, 9.3), (xd, yy, 9.9), .45, "cable_inst", seg=14)                   # service loop, tied up
            n += 2
    # power: MC home runs from RP-1 along the corridor, into the office, down the perimeter walls to the boxes
    for k, yy in enumerate((349.0, 357.0, 365.0, 373.0)):
        run([(x1 + .5, 383.3, 15.2), (x1 + .5, yy, 15.4), (x0 + 1.0, yy, 15.4), (x0 + .4, yy, 15.4),
             (x0 + .4, yy, 1.6)], .07, "alu")
        box(x0 + .2, x0 + .45, yy - .2, yy + .2, 1.2, 1.9, "steel")                        # receptacle box, no cover yet
        n += 5
    for xs in (96.0, 112.0, 128.0):                                                        # south wall boxes
        run([(xs, 349.0, 15.4), (xs, IY0 + .45, 15.4), (xs, IY0 + .45, 1.6)], .07, "alu")
        box(xs - .2, xs + .2, IY0 + .2, IY0 + .45, 1.2, 1.9, "steel")
        n += 3
    # lighting: troffers hung on the grid and whipped (MC fixture whips) in the east half; the rest boxed on the floor
    for x in (122.0, 131.0, 140.0):
        for y in (352.0, 362.0, 372.0):
            box(x - 1, x + 1, y - 2, y + 2, CEIL - .06, CEIL, "steel")
            box(x - .9, x + .9, y - 1.9, y + 1.9, CEIL - .08, CEIL - .06, "lamp_in")
            run([(x, y, CEIL), (x + .6, y + 1.2, 13.6), (x + .6, y + 1.2, 15.0)], .05, "alu")   # whip to the J-box
            box(x + .4, x + .8, y + 1.0, y + 1.4, 15.0, 15.4, "steel")
            n += 5
    for k in range(6):                                                                     # fixtures still boxed
        box(88.0 + (k % 3) * 2.4, 90.2 + (k % 3) * 2.4, 374.0 - (k // 3) * 4.6, 378.0 - (k // 3) * 4.6 - .4,
            0, .55 if k < 3 else 1.1, "timber")
        n += 1
    # fire alarm: detectors in, FPLR on J-hooks
    for x in (96.0, 120.0):
        for y in (352.0, 370.0):
            n += smoke(x, y)
    run([(x1, 379.0, 14.6), (x1 - 2.0, 370.0, 14.6), (96.0, 370.0, 14.6), (96.0, 352.0, 14.6), (120.0, 352.0, 14.6)],
        .045, "cable_fa")
    n += horn_strobe(x0 + .1, 362.0, 1, 0)
    # temporary construction lighting until the troffers are energised, a work light at the ladder
    for yy in (350.0, 358.0, 366.0, 374.0):
        n += string_lights(x0 + 3.0, x1 - 2.0, yy, 11.6)
    n += work_light(124.0, 361.0)
    # pulling THHN into the EMT on the east wall: cable puller, barrels feeding the conductors
    run([(118.0, IY0 + .5, 15.2), (118.0, IY0 + .5, 9.5)], .1, "pipe")                       # EMT down the south wall
    n += cable_puller(123.0, 352.0, 118.0, IY0 + .5, 9.2)
    for k, c in enumerate(("cable_tc", "sw_red", "safety")):
        n += cable_barrel(108.5 + k * 2.4, 351.0, c)
        rod((108.5 + k * 2.4, 351.0, 5.0), (118.0, IY0 + .6, 9.5), .03, c, seg=4)          # conductors to the conduit
    # materials, access and the crew
    n += reel_stand(100.0, 362.0)
    n += wire_cart(112.0, 372.0)
    n += ladder(128.0, 366.0, 9.0)
    n += scissor_lift(104.0, 357.0, 8.0)
    person(104.5, 357.0, math.pi / 2, z=8.0)
    person(128.6, 366.0, math.pi, z=3.8)
    person(113.5, 368.0, -math.pi / 2)
    rod((86.0, 371.0, 0), (86.0, 371.0, 5.6), .05, "steel", seg=6)
    decal((86.0, 371.06, 4.8), (0, 1, 0), 2.6, 1.3, [("FIT-OUT IN PROGRESS", .3, 1, "#111111"),
                                                     ("HARD HATS  ·  SAFETY GLASSES", .22, 0, "#111111")], bg="#f2c21b")
    return n + 6


def build():
    it = new_item(L, "Control / admin building wiring: power, lighting, fire alarm, data; open office mid fit-out",
                  [IX0, IX1, IY0, IY1], [0, DECK], area="F", register=False,
                  info="Building wiring end to end: 480 V service to the MDP in the electrical room, T-1 and the "
                       "panelboards, EMT and MC branch circuits to every room; MDF / UPS room with the fibre and Cat 6A "
                       "backbone on an 18 in basket tray over the corridor to the server room and the control room "
                       "(video wall, console floor boxes); FPLR fire-alarm loop to detectors, horn / strobes and pull "
                       "stations. The open office is mid fit-out with the cable exposed. Typical, not engineered.")
    it["wiring"] = ["Service 480 V: 4 x 4 in PVC from the duct bank, Cu XHHW-2 to the MDP",
                    "Branch circuits: MC cable (Southwire MC, 12/2 and 12/3 AL armour) from LP-1 / RP-1 / RP-2 / EP-1",
                    "Feeders: Cu THHN/THWN-2 in EMT (Southwire SIMpull)",
                    "Data: Cat 6A U/FTP in an 18 in wire-basket tray and on J-hooks; single-mode fibre in innerduct",
                    "Fire alarm: FPLR 18/2 shielded, red, on J-hooks (NEC 760)",
                    "Control room: poke-through floor boxes, MC power whips, Cat 6A and fibre to each console",
                    "Server room: overhead busway with plug-in tap boxes and cords; ladder rack and fibre trough",
                    "Grounding: TGB in the MDF bonded to the building steel and the service ground"]
    on(it)
    fuel.D = True
    n = office_fitout()
    on(it)
    fuel.D = True
    n += raise_mcr()
    n += electrical_room() + telecom_room() + corridor_backbone() + room_branches() + control_room() + server_room()
    fuel.D = False
    return n
