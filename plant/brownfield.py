"""Brownfield boiler work (owner, Oct 22: "on brownfields there's a lot of replacement of these boilers ... greenfield or
brownfield"): HRSG 3 shown mid-outage, replacing an HP evaporator module, all typical, not engineered:
- the roof cut open over one 12 ft shipping module of the HP evaporator section (y 668-688; the roof and the centre
  drum-frame stringer are split in build_model.py for HRSG 3), a temporary guard rail round the opening, the
  neighbouring modules' upper headers showing in the slot;
- the old module (12 ft wide, 70 ft of finned tube, weathered) lifted clear of the roof on a spreader bar, two
  tag lines to the crew on the drum walkway;
- a crawler crane east of the HRSG on timber mats: tracks, carbody, house, counterweight, a 215 ft lattice boom with
  its mast and pendants, load lines to the hook block;
- the new module waiting on a heavy-haul lowboy on the ring road north of the unit;
- the cable work that rides the outage, by the R2C e-house: SIMpull Reels on Cradles paying new instrument / control
  cable over a sheave up to the HRSG marshalling junction box, pre-terminated harness crates with QR tags, the old cable
  cut back and coiled into a recycling bin, a cone-and-chain barricade, the outage sign, crew.
The point for the boiler OEMs: on a replacement the outage clock is the cost; SIMpull pulls and pre-terminated cable
take cable off the critical path."""
import math

import fuel
from fuel import box, rod, new_item, on


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def norm(v):
    L = math.sqrt(sum(c * c for c in v))
    return [c / L for c in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def lattice(p0, p1, hw0, hwm, hw1, c="crane", rc=.42, step=10.0):
    """Square lattice boom from p0 to p1: four chords, rings and face diagonals; half-width hw0 at the foot, hwm along
    the middle, hw1 at the head."""
    u = norm([p1[i] - p0[i] for i in range(3)])
    v = norm([-u[1], u[0], 0.0])
    w = cross(u, v)
    L = math.dist(p0, p1)
    hw = lambda t: hw0 + (hwm - hw0) * min(1, t / .15) if t < .15 else (hwm if t < .85 else hwm + (hw1 - hwm) * (t - .85) / .15)
    corner = lambda t, a, b: [p0[i] + u[i] * L * t + (v[i] * a + w[i] * b) * hw(t) for i in range(3)]
    C = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    n = max(2, int(L / step))
    ts = [k / n for k in range(n + 1)]
    for (a, b) in C:
        for t0, t1 in zip(ts, ts[1:]):
            rod(corner(t0, a, b), corner(t1, a, b), rc, c, seg=6)
    for k, t in enumerate(ts):
        for j in range(4):
            a0, b0 = C[j]
            a1, b1 = C[(j + 1) % 4]
            rod(corner(t, a0, b0), corner(t, a1, b1), rc * .45, c, seg=4)          # ring
            if k < n:
                rod(corner(t, a0, b0), corner(ts[k + 1], a1, b1), rc * .4, c, seg=4)   # lacing
    return u, v, w


def crawler_crane(cx, cy, tip):
    """Crawler crane, tracks along x, boom slewed west to the tip."""
    for ty in (cy - 18.5, cy + 11.0):                                               # timber mats and tracks
        box(cx - 22, cx + 22, ty - 1.5, ty + 8.5, 0, .5, "timber")
        box(cx - 20, cx + 20, ty, ty + 7.0, .5, 5.0, "steel_dark")
        for xi in (cx - 20, cx + 20):
            rod((xi, ty, 2.8), (xi, ty + 7.0, 2.8), 2.3, "steel_dark", seg=16)        # idler / drive tumbler
        for k in range(16):
            xs = cx - 18.5 + k * 2.5
            box(xs - .5, xs + .5, ty - .05, ty + 7.05, 4.9, 5.15, "steel")           # track shoes
    box(cx - 10, cx + 10, cy - 11.5, cy + 11.0, 2.5, 6.0, "crane")                   # carbody
    box(cx - 12, cx + 16, cy - 6.5, cy + 6.5, 6.0, 16.0, "crane")                    # house
    box(cx - 17, cx - 11, cy + 2.0, cy + 7.0, 6.0, 14.5, "crane")                     # cab
    box(cx - 17.05, cx - 16.9, cy + 2.4, cy + 6.6, 9.0, 13.8, "glass")
    box(cx - 16.6, cx - 11.4, cy + 6.95, cy + 7.05, 9.0, 13.8, "glass")
    for k in range(4):                                                                # counterweight slabs
        box(cx + 16, cx + 26, cy - 8.0, cy + 8.0, 6.0 + k * 3.0, 8.8 + k * 3.0, "steel_dark")
    decal((cx + 26.05, cy, 15.5), (1, 0, 0), 10.0, 2.0, [("600 T  CRAWLER", .55, True, "#111111")], bg="#e2b622")
    p0 = (cx - 9.0, cy, 12.0)
    lattice(p0, tip, 2.5, 3.6, 2.0)
    rod((tip[0] - 1.5, tip[1] - 2.2, tip[2]), (tip[0] - 1.5, tip[1] + 2.2, tip[2]), 1.4, "crane", seg=14)   # head sheaves
    mast = (cx + 12.0, cy, 64.0)
    for s in (-2.0, 2.0):
        rod((cx + 4.0, cy + s, 16.0), (mast[0], mast[1] + s, mast[2]), .5, "crane", seg=8)   # mast legs
        rod((mast[0], mast[1] + s, mast[2]), (tip[0] + .5, tip[1] + s * .6, tip[2] + .5), .14, "steel", seg=6)   # pendants
        rod((mast[0], mast[1] + s, mast[2]), (cx + 24.0, cy + s * 2, 18.0), .14, "steel", seg=6)              # backhitch
    return p0


def build():
    it = new_item("BASE_POWER_BLOCK", "Brownfield outage: HRSG 3 HP evaporator module replacement (crane lift, new module, "
                  "cable work)", [884, 1086, 640, 920], [0, 210], area="A", register=False,
                  sheet="typical (boiler replacement outage)",
                  info="Outage scene: one HP evaporator shipping module of HRSG 3 lifted out through the opened roof by a "
                       "crawler crane, the replacement waiting on a heavy-haul lowboy on the ring road, and the cable work done "
                       "in the same window: SIMpull Reels paying new cable to the HRSG marshalling box, pre-terminated "
                       "harnesses, old cable cut back to a recycling bin. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    # ---- roof opening over the module slot (roof and centre stringer split in build_model.py)
    OX0, OX1, OY0, OY1 = 943.0, 957.0, 674.0, 686.0
    box(OX0, OX1, OY0, OY1, 85.0, 85.03, "mat")                                     # the dark slot
    for (a0, a1, b0, b1) in ((OX0, OX1, OY0, OY0 + .3), (OX0, OX1, OY1 - .3, OY1),
                             (OX0, OX0 + .3, OY0 + .3, OY1 - .3), (OX1 - .3, OX1, OY0 + .3, OY1 - .3)):
        box(a0, a1, b0, b1, 85.03, 86.15, "steel_dark")                               # cut edge / curb
    for yh in (OY0 + 1.2, OY1 - 1.2):                                                 # neighbours' upper headers
        rod((OX0 + .5, yh, 85.6), (OX1 - .5, yh, 85.6), .5, "hrsg_b", seg=10)
    for (a, b) in (((OX0 - 2, OY0 - 2), (OX1 + 2, OY0 - 2)), ((OX1 + 2, OY0 - 2), (OX1 + 2, OY1 + 2)),
                   ((OX1 + 2, OY1 + 2), (OX0 - 2, OY1 + 2)), ((OX0 - 2, OY1 + 2), (OX0 - 2, OY0 - 2))):
        for h in (1.75, 3.5):                                                         # temporary guard rail
            rod((a[0], a[1], 86.0 + h), (b[0], b[1], 86.0 + h), .06, "amber", seg=4)
        rod((a[0], a[1], 86.4), (a[0], a[1], 89.5), .07, "amber", seg=4)
    n += 20
    # ---- the old module on the hook: 12 ft wide, 70 ft of finned tube, weathered
    MX0, MX1, MY = 944.0, 956.0, 680.0
    ZB, ZT = 104.0, 174.0
    rod((MX0, MY, ZT), (MX1, MY, ZT), .85, "steel_dark", seg=12)                     # upper header
    rod((MX0, MY, ZB), (MX1, MY, ZB), .85, "steel_dark", seg=12)                     # lower header
    for k in range(12):
        x = MX0 + .5 + k
        for dy in (-.9, .9):
            rod((x, MY + dy, ZB + .8), (x, MY + dy, ZT - .8), .2, "deck", seg=6)        # finned tubes (weathered)
    for z in (ZB + 18, ZB + 36, ZB + 54):                                             # tube-support straps
        box(MX0 - .2, MX1 + .2, MY - 1.3, MY + 1.3, z - .2, z + .2, "steel_dark")
    for x in (MX0 + 1.0, MX1 - 1.0):                                                  # lifting lugs and slings
        box(x - .2, x + .2, MY - .3, MY + .3, ZT + .85, ZT + 1.8, "steel")
        rod((x, MY, ZT + 1.8), (x, MY, 180.0), .08, "steel", seg=4)
    box(MX0, MX1, MY - .5, MY + .5, 180.0, 181.0, "sp_yellow")                        # spreader bar
    for x in (MX0 + .5, MX1 - .5):
        rod((x, MY, 181.0), (950.0, MY, 186.0), .1, "steel", seg=4)
    box(948.6, 951.4, MY - 1.2, MY + 1.2, 186.0, 190.5, "sp_yellow")                  # hook block
    for dx_ in (-.6, -.2, .2, .6):
        rod((950.0 + dx_, MY, 190.5), (950.0 + dx_, MY, 205.6), .07, "steel", seg=4)  # load lines
    for (x, xr) in ((MX0, 938.0), (MX1, 962.0)):                                      # tag lines to the drum walkway
        rod((x, MY, ZB), (xr, 692.7, 92.6), .05, "rope", seg=4)
    decal((950.0, MY - 1.15, ZB + 6.0), (0, -1, 0), 9.0, 1.4, [("OLD  HP EVAP MODULE 3", .55, True, "#ffffff")],
          bg="#3c4247")
    n += 40
    # ---- crawler crane east of the HRSG
    crawler_crane(1062.0, 659.5, (951.5, MY, 207.0))
    n += 200
    # ---- crew on the roof walkway and a rigger at the crane
    import maintenance as mt
    mt.person(938.5, 692.7, 89.2, 1.57, vest="hivis_o")
    mt.person(961.5, 692.7, 89.2, 1.57)
    mt.person(1036.5, 690.0, 0.0, 3.14, vest="hivis_o", hat="sign")                 # lift supervisor
    # ---- the new module on a heavy-haul lowboy on the ring road
    LY = 913.0
    box(950.0, 1028.0, LY - 6.0, LY + 6.0, 2.9, 4.1, "steel_dark")                    # lowboy deck
    for k in range(9):                                                                # axle lines
        x = 954.0 + k * 3.2 if k < 4 else 1004.0 + (k - 4) * 3.2
        for s in (-1, 1):
            rod((x, LY + s * 4.0, 1.75), (x, LY + s * 6.1, 1.75), 1.4, "tyre", seg=12)
    box(1028.0, 1034.0, LY - 2.0, LY + 2.0, 3.3, 5.3, "steel_dark")                   # gooseneck
    box(1032.0, 1050.0, LY - 4.2, LY + 4.2, 1.9, 4.3, "steel_dark")                   # tractor chassis
    box(1040.0, 1050.0, LY - 4.2, LY + 4.2, 4.3, 12.3, "hivis_o")                     # heavy-haul tractor cab
    box(1049.9, 1050.0, LY - 3.4, LY + 3.4, 7.5, 11.0, "glass")
    for x in (1036.0, 1040.0, 1046.5):
        for s in (-1, 1):
            rod((x, LY + s * 3.2, 2.15), (x, LY + s * 4.4, 2.15), 1.8, "tyre", seg=12)
    for x in (953.0, 989.0, 1025.0):                                                  # cribbing
        box(x - 1.5, x + 1.5, LY - 6.0, LY + 6.0, 4.1, 4.9, "timber")
    NX0, NX1 = 951.0, 1025.0                                                          # the new module lying flat
    rod((NX0, LY - 6.0, 6.9), (NX0, LY + 6.0, 6.9), .85, "steel", seg=12)
    rod((NX1, LY - 6.0, 6.9), (NX1, LY + 6.0, 6.9), .85, "steel", seg=12)
    for k in range(12):
        y = LY - 5.5 + k
        for dz in (-.9, .9):
            rod((NX0 + .8, y, 6.9 + dz), (NX1 - .8, y, 6.9 + dz), .2, "alu", seg=6)
    for x in (970.0, 989.0, 1008.0):
        box(x - .2, x + .2, LY - 6.3, LY + 6.3, 4.9, 8.9, "steel_dark")
    decal((989.0, LY - 6.45, 7.0), (0, -1, 0), 22.0, 2.2,
          [("NEW  HP EVAPORATOR MODULE  ·  HRSG 3", .55, True, "#111111")], bg="#ffffff")
    for x, y in ((947.0, LY - 8.0), (1052.0, LY + 8.0)):                             # escort cones / flags
        rod((x, y, .9), (x, y, 3.2), .55, "hivis_o", r2=.08, seg=10)
    mt.person(1053.0, LY - 6.0, 0.35, 3.14)
    n += 60
    # ---- cable work riding the outage, by the R2C e-house
    import simpull
    simpull.sp_reel(888.5, 683.0, 0, axis="y", cols=("cable_inst", "cable_inst", "cable_tc", "cable_tcx", "cable_fo"))
    simpull.sp_reel(888.5, 692.5, 0, axis="y", cols=("cable_tc", "cable_tc", "cable_inst", "cable_fa", "cable_inst"))
    SH = (896.5, 697.0, 8.5)                                                          # pulling sheave on a stand
    rod((SH[0], SH[1], 0), (SH[0], SH[1], 7.6), .18, "steel", seg=8)
    box(SH[0] - 1.2, SH[0] + 1.2, SH[1] - 1.2, SH[1] + 1.2, 0, .3, "steel_dark")
    rod((SH[0] - .4, SH[1], SH[2]), (SH[0] + .4, SH[1], SH[2]), 1.0, "crane", seg=14)
    for (ry, c) in ((683.0, "cable_inst"), (692.5, "cable_tc")):
        poly([(889.6, ry, 5.6), (893.0, (ry + SH[1]) / 2, 7.5), (SH[0], SH[1] - .6, SH[2] + .9)], .11, c, seg=6)
    poly([(SH[0], SH[1] + .6, SH[2] + .9), (SH[0], SH[1] + .6, 36.0), (913.8, SH[1] + .6, 36.0), (913.8, 691.0, 36.0),
          (913.8, 691.0, 38.0), (914.6, 691.0, 38.0)], .13, "cable_tc", seg=6)                 # up to the marshalling JB
    for k in range(2):                                                                # pre-terminated harness crates
        x0 = 893.0 + k * 0.0
        y0 = 678.5 + k * 5.0
        box(x0, x0 + 4.0, y0, y0 + 3.4, 0, 2.6, "timber")
        for j in range(3):
            rod((x0 + 2.0, y0 + 1.7, 2.6 + j * .25), (x0 + 2.0, y0 + 1.7, 2.85 + j * .25), 1.4 - j * .15,
                ("cable_inst", "cable_tc", "cable_tcx")[j], seg=18)                    # coiled harness tails
        import reserved_pad as rp
        rp.qr(x0 + 2.0, y0 - .02, 1.5, .8)
        decal((x0 + 2.0, y0 - .03, .6), (0, -1, 0), 3.4, .5, [("PRE-TERMINATED  ·  HRSG 3", .6, True, "#111111")],
              bg="#ffffff")
    BX0, BX1, BY0, BY1 = 903.5, 910.5, 679.0, 686.0                                   # recycling bin with the old cable
    box(BX0, BX1, BY0, BY1, 0, .3, "steel_dark")
    for (a0, a1, b0, b1) in ((BX0, BX1, BY0, BY0 + .2), (BX0, BX1, BY1 - .2, BY1), (BX0, BX0 + .2, BY0, BY1),
                             (BX1 - .2, BX1, BY0, BY1)):
        box(a0, a1, b0, b1, .3, 4.0, "safety")
    for j in range(4):                                                                # coils of cut-back cable
        cx_, cy_ = BX0 + 2.0 + (j % 2) * 3.0, BY0 + 2.0 + (j // 2) * 3.0
        rod((cx_, cy_, .3 + j * .5), (cx_, cy_, .7 + j * .5), 1.3, "cable", seg=16)
    decal(((BX0 + BX1) / 2, BY0 - .02, 2.6), (0, -1, 0), 6.0, 1.0,
          [("CABLE RECYCLING", .5, True, "#ffffff"), ("CUT-BACK  ·  HRSG 3", .3, False, "#ffffff")], bg=None)
    for (x, y) in ((884.5, 677.5), (911.5, 677.5), (911.5, 699.0), (884.5, 699.0)):  # cone-and-chain barricade
        rod((x, y, 0), (x, y, 2.3), .55, "hivis_o", r2=.08, seg=10)
    for (a, b) in (((884.5, 677.5), (911.5, 677.5)), ((884.5, 677.5), (884.5, 699.0)), ((884.5, 699.0), (896.0, 699.0))):
        rod((a[0], a[1], 2.0), (b[0], b[1], 2.0), .04, "barrier", seg=4)
    rod((897.0, 676.6, 0), (897.0, 676.6, 6.5), .1, "steel", seg=6)                  # outage sign
    decal((897.0, 676.45, 5.4), (0, -1, 0), 6.0, 2.0,
          [("HRSG 3  OUTAGE", .38, True, "#ffffff"), ("MODULE REPLACEMENT + CABLE", .22, True, "#ffffff"),
           ("LOCKOUT / TAGOUT IN FORCE", .2, False, "#ffffff")], bg="#b8322a")
    decal((897.0, 676.75, 5.4), (0, 1, 0), 6.0, 2.0,
          [("HRSG 3  OUTAGE", .38, True, "#ffffff"), ("MODULE REPLACEMENT + CABLE", .22, True, "#ffffff"),
           ("LOCKOUT / TAGOUT IN FORCE", .2, False, "#ffffff")], bg="#b8322a")          # both faces
    mt.person(891.5, 687.8, 0, 0.0)                                                   # reel tender
    mt.person(899.5, 692.0, 0, 1.2, vest="hivis_o")                                   # at the sheave
    mt.person(894.5, 683.2, 0, -1.57)                                                 # scanning the harness QR
    fuel.D = False
    return n + 60
