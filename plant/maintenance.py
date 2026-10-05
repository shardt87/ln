"""Cable-pulling maintenance scene on the modular power yard's 13.8 kV collector duct bank (y 960, x 1710-1900),
open ground south of the bank: high-voltage feeders and room for the reel trailer and puller truck (it first sat on
the R1 duct bank by the inlet-chilling plant, which was cramped and low-voltage). Coordinates below are the local
frame of the scene (see to_site).

A crew replaces a feeder in the bank, typical of an outage job:
- manhole MH-A (355, 1153): cover lifted off and laid aside, guard rail with chain and cones round the opening,
  davit tripod with man-riding winch, gas monitor and a ventilation blower with its duct down the shaft; a cable
  reel trailer behind a pickup pays out a new cable over a feeder sheave into the manhole, a worker guides it at
  the reel, one at the rim, one in the chamber at the duct mouth;
- manhole MH-B (355, 1340): the cable-puller truck with its capstan and boom over the open manhole, pulling rope
  down the shaft, two workers at the puller;
- between them (y 1236-1260): an open excavation exposing the duct bank, with a steel trench box, ladder, spoil
  pile, a mini excavator, orange barrier fence; the encasement is broken out over a short length so the conduits
  show, two workers in the trench.
The compound ground is cut at the openings so the shafts and the trench read from above. Typical, not engineered.
"""
import math

import fuel
from fuel import box, rod

X = 355.0
MH_A, MH_B = (X, 1153.0), (X, 1340.0)               # MH-B: a pulling manhole added for this job
EXC = (349.0, 361.0, 1236.0, 1260.0)                 # trench footprint
OPEN = [(X - 1.3, X + 1.3, MH_A[1] - 1.3, MH_A[1] + 1.3), (X - 1.3, X + 1.3, MH_B[1] - 1.3, MH_B[1] + 1.3), EXC]


def person(x, y, z, a=0.0, vest="hivis", hat="hardhat"):
    ca, sa = math.cos(a), math.sin(a)
    for s in (-1, 1):
        px, py = x + s * .28 * -sa, y + s * .28 * ca
        rod((px, py, z), (px, py, z + 2.8), .2, "workwear", seg=6)
    box(x - .55, x + .55, y - .55, y + .55, z + 2.8, z + 4.7, vest)
    for s in (-1, 1):
        px, py = x + s * .72 * -sa, y + s * .72 * ca
        rod((px, py, z + 4.6), (px + .35 * ca, py + .35 * sa, z + 3.1), .14, vest, seg=6)
    rod((x, y, z + 4.75), (x, y, z + 5.45), .36, "skin", seg=10)
    rod((x, y, z + 5.4), (x, y, z + 5.85), .43, hat, r2=.3, seg=10)


def bez(p0, p1, p2, n=10):
    return [tuple((1 - t) ** 2 * p0[k] + 2 * (1 - t) * t * p1[k] + t * t * p2[k] for k in range(3))
            for t in [i / n for i in range(n + 1)]]


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def cut_ground():
    """Split the compound ground tiles round the openings (manhole shafts and the trench)."""
    G = fuel.G
    cid = next(it["id"] for it in G["items"] if it["name"].startswith("Compound"))
    tiles = [p for p in G["parts"] if p["item"] == cid and p["kind"] == "box" and p["color"] == "ground"]
    cur = G["cur"]
    patch = fuel.new_item("NOMOD_GROUND", "Ground over the maintenance openings (shown without the modular yard)",
                          (0, 2420, 0, 1920), (-.5, 0), basis="typical", register=False)
    G["cur"] = cur
    ids = {id(t) for t in tiles}
    G["parts"][:] = [p for p in G["parts"] if id(p) not in ids]

    def sub(r, o):
        """Rectangle r minus rectangle o, as up to four pieces."""
        (a0, a1, b0, b1), (x0, x1, y0, y1) = r, o
        if not (a0 < x1 and a1 > x0 and b0 < y1 and b1 > y0):
            return [r]
        out = [(a0, a1, b0, y0), (a0, a1, y1, b1), (a0, x0, max(b0, y0), min(b1, y1)), (x1, a1, max(b0, y0), min(b1, y1))]
        return [q for q in out if q[1] - q[0] > .01 and q[3] - q[2] > .01]
    for t in tiles:
        (tx0, ty0, tz0), (tx1, ty1, tz1) = t["min"], t["max"]
        rects = [(tx0, tx1, ty0, ty1)]
        for o in OPEN:
            rects = [q for r in rects for q in sub(r, o)]
        for (a0, a1, b0, b1) in rects:
            G["parts"].append(dict(t, min=[a0, b0, tz0], max=[a1, b1, tz1]))
    for (x0, x1, y0, y1) in OPEN:
        if any(t["min"][0] < x1 and t["max"][0] > x0 and t["min"][1] < y1 and t["max"][1] > y0 for t in tiles):
            G["parts"].append(dict(kind="box", min=[x0, y0, -.5], max=[x1, y1, 0], color="ground",
                                   item=patch["id"], layer="NOMOD_GROUND"))
    pp = [p for p in G["parts"] if p["item"] == patch["id"]]
    if pp:
        patch["fp"] = [min(p["min"][0] for p in pp), max(p["max"][0] for p in pp),
                       min(p["min"][1] for p in pp), max(p["max"][1] for p in pp)]


def open_manhole(cx, cy):
    """Remove the cover and collar placed by station.manholes(); frame, shaft walls, ladder; guard rail and cones."""
    G = fuel.G
    mh = next(it["id"] for it in G["items"] if it["name"].startswith("Duct-bank manholes"))

    def near(p):
        lo, hi = (p["min"], p["max"]) if p["kind"] == "box" else (p["a"], p["b"])
        return abs((lo[0] + hi[0]) / 2 - cx) < 2.5 and abs((lo[1] + hi[1]) / 2 - cy) < 2.5
    G["parts"][:] = [p for p in G["parts"] if not (p["item"] == mh and near(p))]
    # cast frame round the opening, shaft walls down to the chamber roof, rungs
    for (x0, x1, y0, y1) in ((cx - 1.6, cx + 1.6, cy - 1.6, cy - 1.3), (cx - 1.6, cx + 1.6, cy + 1.3, cy + 1.6),
                             (cx - 1.6, cx - 1.3, cy - 1.3, cy + 1.3), (cx + 1.3, cx + 1.6, cy - 1.3, cy + 1.3)):
        box(x0, x1, y0, y1, -3.2, .25, "concrete")
    box(cx - 1.3, cx + 1.3, cy - 1.3, cy + 1.3, -9.2, -9.0, "concrete")                # chamber floor seen down the shaft
    for s in (-.5, .5):
        rod((cx + s, cy + 1.2, -9), (cx + s, cy + 1.2, 3.5), .06, "steel", seg=4)       # ladder rails, extended up
    for z in range(-8, 3, 1):
        rod((cx - .5, cy + 1.2, z), (cx + .5, cy + 1.2, z), .04, "steel", seg=4)
    # cover lifted off and laid on the ground beside the opening
    rod((cx + 3.6, cy - 2.6, 0), (cx + 3.6, cy - 2.6, .3), 1.4, "fanhub", seg=16)
    # guard rail with chain on four posts, cones
    for (dx, dy) in ((-4.5, -4.5), (4.5, -4.5), (4.5, 4.5), (-4.5, 4.5)):
        rod((cx + dx, cy + dy, 0), (cx + dx, cy + dy, 3.4), .1, "hivis_o", seg=6)
        box(cx + dx - .6, cx + dx + .6, cy + dy - .6, cy + dy + .6, 0, .2, "machine")
    for (a, b) in (((-4.5, -4.5), (4.5, -4.5)), ((4.5, -4.5), (4.5, 4.5)), ((-4.5, 4.5), (-4.5, -4.5))):
        poly(bez((cx + a[0], cy + a[1], 3.2), (cx + (a[0] + b[0]) / 2, cy + (a[1] + b[1]) / 2, 2.6),
                 (cx + b[0], cy + b[1], 3.2), 6), .05, "red", seg=4)
    for (dx, dy) in ((-7, -6), (-7, 6), (7, 0), (0, -7.5)):
        rod((cx + dx, cy + dy, 0), (cx + dx, cy + dy, 2.3), .55, "hivis_o", r2=.08, seg=10)
        box(cx + dx - .7, cx + dx + .7, cy + dy - .7, cy + dy + .7, 0, .1, "hivis_o")


def new_chamber(cx, cy):
    """Precast chamber for the pulling manhole MH-B (7 x 7 ft, 8 ft deep), as the plant's other manholes."""
    x0, x1, y0, y1 = cx - 3.5, cx + 3.5, cy - 3.5, cy + 3.5
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + .5), (x0, x1, y1 - .5, y1), (x0, x0 + .5, y0, y1), (x1 - .5, x1, y0, y1)):
        box(a0, a1, b0, b1, -9, -1.2, "ductcase")
    box(x0, x1, y0, y1, -9.3, -9, "concrete")
    for (a0, a1, b0, b1) in ((x0, x1, y0, cy - 1.3), (x0, x1, cy + 1.3, y1), (x0, cx - 1.3, cy - 1.3, cy + 1.3), (cx + 1.3, x1, cy - 1.3, cy + 1.3)):
        box(a0, a1, b0, b1, -1.2, -.4, "ductcase")
    box(x0 - .5, x1 + .5, y0 - .5, y1 + .5, 0, .3, "concrete")                      # collar at grade


def tripod(cx, cy):
    """Davit tripod over the opening with the man-riding winch and lifeline."""
    top = (cx, cy, 8.5)
    for a in (0, 2.1, 4.2):
        rod((cx + 3 * math.cos(a), cy + 3 * math.sin(a), 0), top, .13, "crane", seg=6)
    box(cx + .6, cx + 1.3, cy - .5, cy + .5, 4.5, 5.6, "crane")                       # winch on a leg
    rod(top, (cx, cy, -5.5), .03, "steel", seg=4)                                       # lifeline to the worker below


def blower(x, y, cx, cy):
    box(x - 1, x + 1, y - 1.4, y + 1.4, 0, 1.8, "crane")
    rod((x, y - 1.4, 1), (x, y + 1.4, 1), .9, "machine", seg=14)
    poly(bez((x, y + 1.4, 1), (cx - .8, cy - 3, 2.5), (cx - .8, cy - .8, -6), 8), .45, "amber", seg=10)


def reel_trailer(cx, cy):
    """Pickup and cable-reel trailer west of MH-A; cable over the feeder sheave into the shaft."""
    rx, ry, rz = cx - 15, cy + 6, 5.6                                                    # reel centre, axis along x
    box(rx - 3.2, rx + 3.2, ry - 4.5, ry + 4.5, 1.8, 2.4, "steel")                     # trailer frame
    for sx in (-3.4, 3.4):
        rod((rx + sx - .3, ry, 1.4), (rx + sx + .3, ry, 1.4), 1.4, "fanhub", seg=14)     # wheels
        rod((rx + sx * .9, ry, 2.4), (rx + sx * .9, ry, rz + .4), .3, "steel", seg=6)   # reel stands
    rod((rx - 3, ry, rz), (rx + 3, ry, rz), .25, "steel", seg=8)                        # spindle
    for sx in (-2.2, 2.2):
        rod((rx + sx - .2, ry, rz), (rx + sx + .2, ry, rz), 4.6, "timber", seg=28)      # flanges
    rod((rx - 2, ry, rz), (rx + 2, ry, rz), 3.6, "cable_tc", seg=28)                    # wound cable
    rod((rx - 2.6, ry + 4.5, 2.1), (rx - 2.6, ry + 9.5, 2.1), .18, "steel", seg=6)      # tongue
    fuel_pickup(rx - 2.6, ry + 20)
    # feeder sheave on a stand at the rim, cable from the reel top over it and down the shaft
    sx_, sy_ = cx - .9, cy + 1.5
    rod((sx_, sy_ + 2.5, 0), (sx_, sy_, 3.2), .12, "steel", seg=6)
    rod((sx_ - 2, sy_ + 2, 0), (sx_, sy_, 3.2), .12, "steel", seg=6)
    rod((sx_ - .25, sy_, 3.4), (sx_ + .25, sy_, 3.4), .9, "crane", seg=16)
    p_top = (rx, ry - .6, rz + 3.6)
    poly(bez(p_top, ((rx + sx_) / 2, (ry + sy_) / 2, rz + 5), (sx_, sy_ + .2, 4.3), 12), .22, "cable_tc")
    poly(bez((sx_, sy_ - .2, 4.3), (cx - .3, cy + .4, 4), (cx - .3, cy - .3, 1), 6), .22, "cable_tc")
    rod((cx - .3, cy - .3, 1), (cx - .3, cy - .3, -6.5), .22, "cable_tc", seg=8)
    # in the chamber: the cable bends into the duct mouth on the south wall (a conduit of the bank)
    poly(bez((cx - .3, cy - .3, -6.5), (cx - .3, cy + 3, -4.6), (cx - .3, cy + 6, -4.6), 6), .22, "cable_tc")
    return (rx, ry)


def fuel_pickup(x, y):
    L, W = 19, 6.6
    box(x - W / 2, x + W / 2, y - L / 2, y + L / 2, 1.3, 3.6, "truck")
    box(x - W / 2 + .2, x + W / 2 - .2, y - 1.5, y + 4.5, 3.6, 6.2, "truck")
    box(x - W / 2 + .15, x + W / 2 - .15, y - 1.4, y + 4.4, 4.4, 5.9, "glass")
    for v in (-6, 6):
        for u in (-W / 2, W / 2):
            rod((x + u, y + v, 1.3), (x + u + (.4 if u > 0 else -.4), y + v, 1.3), 1.3, "fanhub", seg=12)


def puller_truck(cx, cy):
    """Cable-puller truck north-west of MH-B: capstan winch at the rear, boom with sheave over the opening."""
    x, y0, y1 = cx - 18, cy + 6, cy + 34                                                 # truck along y, rear to the south
    box(x - 4, x + 4, y0, y1, 1.6, 3.4, "steel")                                        # chassis
    box(x - 4, x + 4, y1 - 8, y1, 3.4, 10, "truck")                                    # cab
    box(x - 3.8, x + 3.8, y1 - 7.5, y1 - 4.5, 6.5, 9.4, "glass")
    box(x - 4, x + 4, y0 + 2, y1 - 9, 3.4, 8.5, "crane")                               # puller body
    rod((x, y0 + 1, 6), (x, y0 + 1, 8.6), 1.3, "steel", seg=16)                        # capstan
    for (yy,) in ((y0 + 4,), (y0 + 11,), (y1 - 4,)):
        for s in (-4.1, 4.1):
            rod((x + s, yy, 1.6), (x + s + (.5 if s > 0 else -.5), yy, 1.6), 1.6, "fanhub", seg=14)
    # boom from the rear of the body out over the manhole, sheave at its tip, rope down the shaft
    b0, b1 = (x + 2, y0 + 1, 8.5), (cx, cy + .6, 9.5)
    rod(b0, b1, .4, "crane", seg=8)
    rod((x + 2, y0 + 3, 3.4), (x + 2, y0 + 1, 8.5), .3, "crane", seg=6)               # boom post
    rod((b1[0] - .25, b1[1], b1[2] - .6), (b1[0] + .25, b1[1], b1[2] - .6), .8, "steel", seg=16)
    rod((x, y0 + 1, 7.4), (b1[0], b1[1] - .3, b1[2] - .1), .06, "amber", seg=4)         # rope from the capstan
    rod((b1[0], b1[1], b1[2] - 1.4), (cx, cy + .6, -6.5), .06, "amber", seg=4)          # rope down the shaft
    poly(bez((cx, cy + .6, -6.5), (cx, cy - 2.5, -4.6), (cx, cy - 6, -4.6), 6), .06, "amber", seg=4)   # rope into the south duct
    box(cx + 5, cx + 7.5, cy + 5, cy + 7, 0, 3.2, "panel")                             # dynamometer / control stand
    for (dx, dy) in ((-7, 4), (7, 4), (0, -7.5), (7, -6)):
        rod((cx + dx, cy + dy, 0), (cx + dx, cy + dy, 2.3), .55, "hivis_o", r2=.08, seg=10)


def excavation():
    """Open trench over the duct bank: soil faces, trench box, broken-out encasement, ladder, spoil, excavator."""
    x0, x1, y0, y1 = EXC
    zf = -5.2
    box(x0, x1, y0, y1, zf - .3, zf, "gravel")                                         # trench floor
    for (a0, a1, b0, b1) in ((x0 - .3, x0, y0, y1), (x1, x1 + .3, y0, y1), (x0, x1, y0 - .3, y0), (x0, x1, y1, y1 + .3)):
        box(a0, a1, b0, b1, zf, 0, "soil")                                             # excavated faces
    # steel trench box: two side panels standing 1.5 ft proud of grade, spreaders across
    for xs in (x0 + .25, x1 - .55):
        box(xs, xs + .3, y0 + 1, y1 - 1, zf + .2, 1.5, "crane")
    for yy in (y0 + 3, y1 - 3):
        for zz in (-1.0, -3.6):
            rod((x0 + .55, yy, zz), (x1 - .55, yy, zz), .22, "steel", seg=8)
    # the duct bank across the trench: encasement broken out in the middle 10 ft, conduits exposed
    top, H, W = -2.5, 1.74, 2.4
    ym = (y0 + y1) / 2
    for (b0, b1) in ((y0 - .3, ym - 5), (ym + 5, y1 + .3)):
        box(X - W / 2, X + W / 2, b0, b1, top - H, top - .12, "concrete")
        box(X - W / 2, X + W / 2, b0, b1, top - .12, top, "ductcap")
    for k in range(6):
        ci, ri = k % 3, k // 3
        v = (ci - 1) * .62
        zc = top - .25 - .31 - ri * .62
        rod((X + v, y0 - .3, zc), (X + v, y1 + .3, zc), .22, "pvc_orange" if k == 5 else "pvc_grey", seg=10)
    # ladder up out of the trench, 3 ft above grade
    for s in (-.6, .6):
        rod((x0 + 1.2, y1 - 2 + s, zf), (x0 + .6, y1 - 2 + s, 3), .07, "crane", seg=4)
    for z in range(-4, 3):
        rod((x0 + 1.0, y1 - 2.6, z), (x0 + 1.0, y1 - 1.4, z), .05, "crane", seg=4)
    # spoil pile on the west side, kept 2 ft back from the edge
    fuel.G["parts"].append(dict(kind="hex", v=[[x0 - 14, y0 + 1, 0], [x0 - 2.5, y0 + 1, 0], [x0 - 2.5, y1 - 1, 0], [x0 - 14, y1 - 1, 0],
                                               [x0 - 10, y0 + 5, 4.5], [x0 - 6, y0 + 5, 4.5], [x0 - 6, y1 - 5, 4.5], [x0 - 10, y1 - 5, 4.5]],
                                color="soil", item=fuel.G["cur"]["id"], layer=fuel.G["cur"]["layer"]))
    # mini excavator north of the trench, arm over it
    ex, ey = X - 1, y1 + 9
    for s in (-3, 3):
        box(ex + s - .8, ex + s + .8, ey - 4, ey + 4, 0, 1.6, "fanhub")                 # tracks
    box(ex - 3, ex + 3, ey - 3, ey + 3, 1.6, 4.4, "crane")                              # upper structure
    box(ex - 2.6, ex - .2, ey - 2.8, ey + .2, 4.4, 8, "crane")                          # cab
    box(ex - 2.5, ex - .3, ey - 2.9, ey - 2.7, 4.8, 7.6, "glass")
    rod((ex + 1, ey - 2.5, 4), (ex + 1, ey - 8, 9), .45, "crane", seg=8)                 # boom
    rod((ex + 1, ey - 8, 9), (ex + 1, ey - 12, 1.5), .35, "crane", seg=8)                # stick
    box(ex + .2, ex + 1.8, ey - 13, ey - 11.5, .5, 2.2, "steel")                        # bucket
    # orange barrier fence round the trench and spoil
    pts = [(x0 - 16, y0 - 4), (x1 + 4, y0 - 4), (x1 + 4, y1 + 3), (x0 - 16, y1 + 3)]
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        for k in range(int(L // 6) + 1):
            t = k * 6 / L
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            rod((px, py, 0), (px, py, 4), .07, "steel", seg=4)
        lo = (min(a[0], b[0]), min(a[1], b[1]))
        hi = (max(a[0], b[0]), max(a[1], b[1]))
        box(lo[0] - .02, hi[0] + .02, lo[1] - .02, hi[1] + .02, .3, 3.8, "barrier")
    # sign
    rod((x1 + 6, y0 - 6, 0), (x1 + 6, y0 - 6, 5), .08, "steel", seg=4)
    box(x1 + 5, x1 + 7, y0 - 6.05, y0 - 5.95, 3.4, 5.2, "sign")


# The scene is drawn in a local frame (the bank along local y at local x = X, the work side at local x < X) and
# placed on the modular yard's 13.8 kV collector bank (y 960, x 1700-1935, open ground south of it): local
# (x, y) -> site (y + DX, Y0 + x - X). MH-B lands on the existing bend manhole at (1900, 960).
Y0, DX = 960.0, 560.0
LAYER = "OPT_MOD"


def to_site(x, y):
    return y + DX, Y0 + x - X


def _place(parts):
    for p in parts:
        if p["kind"] == "rod":
            for k in ("a", "b"):
                x, y = to_site(p[k][0], p[k][1])
                p[k] = [round(x, 2), round(y, 2), p[k][2]]
        elif p["kind"] in ("box", "prism"):
            x0, y0 = to_site(p["min"][0], p["min"][1])
            x1, y1 = to_site(p["max"][0], p["max"][1])
            p["min"] = [round(min(x0, x1), 2), round(min(y0, y1), 2), p["min"][2]]
            p["max"] = [round(max(x0, x1), 2), round(max(y0, y1), 2), p["max"][2]]
        else:
            v = [[*to_site(q[0], q[1]), q[2]] for q in p["v"]]
            p["v"] = [v[0], v[3], v[2], v[1], v[4], v[7], v[6], v[5]]          # the mirror flips the winding


def site_rect(r):
    x0, y0 = to_site(r[0], r[2])
    x1, y1 = to_site(r[1], r[3])
    return (min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1))


def build():
    global OPEN
    (sx0, sx1, sy0, sy1) = site_rect((310, 372, 1135, 1380))
    it = fuel.new_item(LAYER, "Underground: cable-pull maintenance on the modular-yard 13.8 kV collector (open manholes, reel, puller, trench)",
                       (sx0, sx1, sy0, sy1), (-9.3, 12), area="I", basis="typical", register=False,
                       sheet="typical (underground maintenance scene)",
                       info="Outage job in the modular power yard: a 13.8 kV collector feeder is replaced in the duct bank "
                            "from the RICE / SC units to MOD-EH. MH-A: cover off, guard rail, davit tripod, gas monitor and "
                            "ventilation, reel trailer paying out over a feeder sheave. MH-B: cable-puller truck with capstan "
                            "and boom. Between them an open trench with a trench box exposes the bank. Confined-space entry "
                            "with attendant (typical).")
    n0 = len(fuel.G["parts"])
    tripod(*MH_A)
    blower(MH_A[0] + 6, MH_A[1] + 3, *MH_A)
    box(MH_A[0] + 2.2, MH_A[0] + 2.8, MH_A[1] + 2.2, MH_A[1] + 2.8, 0, 1.2, "crane")   # gas monitor
    rx, ry = reel_trailer(*MH_A)
    puller_truck(*MH_B)
    excavation()
    person(rx + 4, ry - 1.5, 0, 0)                                                      # reel tender
    person(MH_A[0] - 3, MH_A[1] + 3.2, 0, -.8)                                           # guides the cable at the rim
    person(MH_A[0] + 3, MH_A[1] - 1, 0, 3.1, vest="hivis_o")                            # attendant at the tripod
    person(MH_A[0] + .3, MH_A[1] + .2, -9, 4.7)                                        # in the chamber at the duct
    person(MH_A[0] - 9, MH_A[1] - 7, 0, .6, vest="hivis_o", hat="sign")               # supervisor
    person(MH_B[0] - 12, MH_B[1] + 4, 0, 0)                                             # puller operator
    person(MH_B[0] + 4, MH_B[1] + 8, 0, 3.6, vest="hivis_o")                           # watches the dynamometer
    person(X - 2.5, EXC[2] + 8, -5.2, 1.6)                                              # in the trench
    person(X + 2.5, EXC[2] + 15, -5.2, 4.7)
    person(EXC[1] + 2.5, EXC[2] + 6, 0, 3.1, vest="hivis_o")                           # spotter at the edge
    _place(fuel.G["parts"][n0:])
    # openings, chambers and covers in site coordinates
    OPEN = [site_rect(r) for r in OPEN]
    cut_ground()
    a, b = to_site(*MH_A), to_site(*MH_B)
    fuel.G["cur"] = it
    mh = next(i["id"] for i in fuel.G["items"] if i["name"].startswith("Duct-bank manholes"))
    for (cx, cy) in (a, b):
        has = any(p["item"] == mh and p["kind"] == "box" and abs((p["min"][0] + p["max"][0]) / 2 - cx) < 3
                  and abs((p["min"][1] + p["max"][1]) / 2 - cy) < 3 for p in fuel.G["parts"])
        if not has:
            new_chamber(cx, cy)
        fuel.G["cur"] = it
        open_manhole(cx, cy)
    return it
