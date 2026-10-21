"""Reserved pad for a future SC-3 / SC-4 simple-cycle pair, pre-wired (owner, Oct 20: rather than two more units
in the open strip south of SC-1 / SC-2, a phase-2 pad: the growth story without the clutter).

The strip between the SC PCM row and the yard edge (x 1886-2234, y 1264-1334), laid out as SC-1 / SC-2 are: a
mirrored pair, stacks inboard and inlets outboard, each unit's PCM pad at its generator (inlet) end:
- a low concrete curb round the reserved area, yellow bollards at its corners and a sign at the road;
- two unit foundation slabs and two stack pads, poured and left bare;
- two PCM pads, each tied by a buried duct bank into the yard MV duct bank (routes in build_model.py, so the
  network, manholes and cable schedule see them): conduit stub-ups capped at the PCM pads and at the generator
  end of each foundation, a handhole beside each PCM pad;
- a capped, blinded fuel-gas riser at each unit for the future tie-in.
Typical, not engineered."""
import fuel
from fuel import box, rod, new_item, on

X0, X1, Y0, Y1 = 1886.0, 2234.0, 1264.0, 1334.0
UNITS = (  # (name, foundation x0..x1, stack pad x0..x1, PCM pad x0..x1, generator-end x)
    ("SC-3", (1905.0, 2035.0), (2038.0, 2054.0), (1905.0, 1945.0), 1917.0),
    ("SC-4", (2085.0, 2215.0), (2066.0, 2082.0), (2175.0, 2215.0), 2203.0),
)
FY0, FY1 = 1270.0, 1300.0                                     # unit foundations (package + SCR)
PY0, PY1 = 1312.0, 1326.0                                     # PCM pads


def stubs(x0, x1, y0, y1, z, nx, ny, r=.22):
    """A bank of capped conduit stub-ups."""
    n = 0
    for i in range(nx):
        for j in range(ny):
            x = x0 + (x1 - x0) * (i + .5) / nx
            y = y0 + (y1 - y0) * (j + .5) / ny
            rod((x, y, z), (x, y, z + 1.5), r, "pvc_grey", seg=10)
            rod((x, y, z + 1.5), (x, y, z + 1.75), r + .06, "red", seg=10)
            n += 2
    return n


def build():
    import showcase
    it = new_item("OPT_MOD", "Reserved pad: SC-3 / SC-4 future simple-cycle pair (pre-wired)", [X0, X1, Y0, Y1], [0, 6],
                  area="I", register=False,
                  info="Phase-2 pad for two more LM6000-class units, laid out as SC-1 / SC-2 (stacks paired, inlets "
                       "outboard). Foundations poured; PCM pads tied into the yard MV duct bank; conduits stubbed up "
                       "and capped; fuel-gas tie-in risers capped and blinded. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    w = .8                                                     # curb round the reserved area
    for (a0, a1, b0, b1) in ((X0, X1, Y0, Y0 + w), (X0, X1, Y1 - w, Y1), (X0, X0 + w, Y0, Y1), (X1 - w, X1, Y0, Y1)):
        box(a0, a1, b0, b1, 0, .35, "concrete")
        box(a0, a1, b0, b1, .35, .37, "deck_line")                                     # yellow line: reserved
        n += 2
    for (x, y) in ((X0 + 1.5, Y0 + 1.5), (X1 - 1.5, Y0 + 1.5), (X0 + 1.5, Y1 - 1.5), (X1 - 1.5, Y1 - 1.5)):
        rod((x, y, 0), (x, y, 4), .35, "crane", seg=10)                                # bollards
        n += 1
    for name, (f0, f1), (s0, s1), (p0, p1), xg in UNITS:
        box(f0, f1, FY0, FY1, 0, .5, "concrete")                                       # unit foundation
        box(s0, s1, 1277.0, 1293.0, 0, .8, "concrete")                                 # stack pad
        for (ax, ay) in ((s0 + 2, 1279), (s1 - 2, 1279), (s0 + 2, 1291), (s1 - 2, 1291)):
            rod((ax, ay, .8), (ax, ay, 1.6), .12, "steel", seg=6)                      # anchor-bolt clusters
        box(p0, p1, PY0, PY1, 0, .6, "concrete")                                       # PCM pad
        n += 6
        # MV feeder to MOD-EH and control / aux conduits, stubbed up and capped through the PCM pad
        n += stubs(p0 + 6, p0 + 18, PY0 + 2, PY0 + 6, .6, 6, 2)
        n += stubs(p0 + 24, p0 + 32, PY0 + 2, PY0 + 4, .6, 4, 1, r=.15)
        # generator leads and control at the generator end of the foundation, towards the PCM (SC-4: the cable bus
        # and the cable trench carry them instead, demo() below)
        if name == "SC-3":
            n += stubs(xg - 4, xg + 4, FY1 - 4, FY1 - 1, .5, 4, 2)
        # handhole beside the PCM pad, on the duct-bank line (SC-4: east of its PCM pad, clear of the cable bus)
        hx, hy = (p0 + 12, PY0 - 4) if name == "SC-3" else (p1 + 9, PY0 + 4)
        box(hx - 2, hx + 2, hy - 2, hy + 2, 0, .25, "concrete")
        box(hx - 1.6, hx + 1.6, hy - 1.6, hy + 1.6, .25, .3, "steel")
        # fuel-gas tie-in riser, capped and blinded, at the foundation's north edge
        xr = (f0 + f1) / 2
        rod((xr, FY0 - 2, 0), (xr, FY0 - 2, 2.6), .33, "fuelgas", seg=12)
        rod((xr, FY0 - 2, 2.6), (xr, FY0 - 2, 2.9), .6, "steel", seg=12)
        n += 4
    fuel.D = False
    n += demo()
    on(it)
    showcase.decal((X0 - 1.2, 1299.0, 5.0), (-1, 0, 0), 15.0, 3.2,
                   [("RESERVED - SC-3 / SC-4", .4, True, "#ffffff"),
                    ("FUTURE SIMPLE-CYCLE PAIR  ·  PRE-WIRED", .2, False, "#c4744a")], bg="#1d1f21")
    return n + 1


# ------------------------------------------------------------------------------- SC-4: plug-and-play demonstration
# Remodelled Oct 21 (owner: the elevated three-tier spine modules read generic and clunky on a simple-cycle pad, and
# that is not how such a pad is wired). As an LM6000-class pad is really built: generator power in a factory cable
# bus over the short run to the PCM; control, instrument and fibre in a precast surface cable trough with lids
# from the PCM pad to each skid landing; the harnesses factory-cut, pre-terminated and tested, coiled at each landing;
# the ground-grid pigtails up at the foundation corners.
TR0, TR1 = 1303.5, 1307.0                                     # main trench (y), between the foundation and the PCM pad
TX0, TX1 = 2090.0, 2183.0                                     # x; stops short of the PCM duct-bank route at x 2187


def coil(x, y, z, cab, tag=None):
    """Factory-terminated harness coiled flat at a landing point, connector capped, tag on it."""
    import showcase
    for k in range(3):
        rod((x, y, z + k * .22), (x, y, z + k * .22 + .2), 1.1 - k * .12, cab, seg=18)
    rod((x + .9, y, z + .7), (x + 1.6, y, z + .7), .16, cab, seg=8)
    rod((x + 1.6, y, z + .7), (x + 2.1, y, z + .7), .26, "steel_dark", seg=10)        # plug connector
    rod((x + 2.1, y, z + .7), (x + 2.35, y, z + .7), .3, "red", seg=10)              # dust cap
    if tag:
        showcase.decal((x, y - 1.25, z + 1.4), (0, -1, 0), 2.6, .7, [(tag, .32, True, "#111111"),
                       ("PRE-TERMINATED  ·  TESTED", .22, False, "#2f7a3c")], bg="#ffffff")
    return 7


def outline(x0, x1, y0, y1, z):
    """Painted footprint of the equipment still to come."""
    w = .3
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + w), (x0, x1, y1 - w, y1), (x0, x0 + w, y0, y1), (x1 - w, x1, y0, y1)):
        box(a0, a1, b0, b1, z, z + .02, "deck_line")
    return 4


def trench(x0, x1, y0, y1, open_=(), along="x"):
    """Precast surface cable trough on grade (2 ft deep): walls and floor, a tray inside with control (TC-ER),
    instrument (shielded ITC) and single-mode fibre, lids on except over the open stretches."""
    n = 0
    if along == "x":
        B = lambda a0, a1, b0, b1, z0, z1, c: box(a0, a1, b0, b1, z0, z1, c)
        lo, hi, c0, c1 = x0, x1, y0, y1
    else:
        B = lambda a0, a1, b0, b1, z0, z1, c: box(b0, b1, a0, a1, z0, z1, c)
        lo, hi, c0, c1 = y0, y1, x0, x1
    B(lo, hi, c0, c0 + .4, 0, 1.95, "concrete")
    B(lo, hi, c1 - .4, c1, 0, 1.95, "concrete")
    B(lo, hi, c0 + .4, c1 - .4, 0, .3, "concrete")
    B(lo, hi, c0 + .6, c0 + .7, .7, 1.1, "pipe")                                      # tray rails
    B(lo, hi, c1 - .7, c1 - .6, .7, 1.1, "pipe")
    w = (c1 - c0 - 1.6) / 3
    for k, cab in enumerate(("cable_tc", "cable_inst", "cable_fo")):
        B(lo, hi, c0 + .8 + k * w, c0 + .8 + (k + 1) * w - .05, .75, 1.05, cab)
    n += 8
    a = lo
    while a < hi - .01:                                                               # lids, 3 ft
        b = min(hi, a + 3.0)
        if not any(o0 <= a and b <= o1 for (o0, o1) in open_):
            B(a + .03, b - .03, c0, c1, 1.95, 2.15, "concrete")
            n += 1
        a = b
    return n


def demo():
    """SC-4's pad as the plug-and-play showcase: everything but the equipment."""
    import showcase
    it = new_item("OPT_MOD", "Reserved pad SC-4: plug-and-play prefab cable demonstration", [2084, 2234, 1268, 1328],
                  [0, 12], area="I", register=False,
                  info="The future SC-4 pad with its cable system already in, as an LM6000-class pad is built: "
                       "generator power in a factory cable bus to the PCM (13.8 kV, MV-105 paralleled per phase); "
                       "control, instrument and fibre in a precast surface cable trough to each skid landing; harnesses "
                       "factory-cut, pre-terminated and tested, coiled at each landing; ground-grid pigtails up at the "
                       "foundation. Set the equipment, connect, energise. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    # the equipment still to come, painted on the slab (package east, SCR west, as SC-2), and the PCM
    n += outline(2125.5, 2214.5, 1270.5, 1299.5, .5)                                   # GT package
    n += outline(2085.5, 2124.5, 1270.5, 1299.5, .5)                                   # SCR / CO catalyst
    n += outline(2177.0, 2213.0, 1313.5, 1324.5, .6)                                   # PCM
    # main trough, two stretches with the lids off (stacked on the slab beside them) to show the cables
    opens = ((2132.0, 2141.0), (2156.0, 2165.0))
    n += trench(TX0, TX1, TR0, TR1, opens)
    for (o0, o1) in opens:
        for k in range(3):
            box(o0 + 1, o0 + 3.9, 1301.0, 1303.0, k * .2, k * .2 + .18, "concrete")
        n += 3
    # branches to the skid landings on the foundation and to the PCM pad; harnesses up out of each, coiled
    landings = ((2160.0, "TCP", "cable_inst"), (2135.0, "AUX SKID", "cable_tc"), (2095.0, "SCR / CEMS", "cable_tc"))
    for (x, t, cab) in landings:
        n += trench(x - 1.25, x + 1.25, 1300.0, TR0, along="y")
        rod((x, 1300.8, 1.0), (x, 1300.4, .6), .18, cab, seg=8)
        rod((x, 1300.4, .6), (x, 1298.2, .6), .18, cab, seg=8)
        n += 2 + coil(x, 1297.0, .5, cab, t)
    n += trench(2178.75, 2181.25, TR1, 1312.0, along="y")
    for k, (cab, t) in enumerate((("cable_tc", "CONTROL"), ("cable_fo", "FIBRE"), ("cable_tc", "AUX POWER"))):
        xc = 2185.0 + k * 5
        rod((2180.0, 1311.0, 1.0), (2180.0, 1312.5, .9), .16, cab, seg=8)
        rod((2180.0, 1312.5, .9), (2180.0, 1320.0, .9), .16, cab, seg=8)        # past the MV stub-ups
        rod((2180.0, 1320.0, .9), (xc, 1321.5, .9), .16, cab, seg=8)
        n += 3 + coil(xc, 1321.5, .6, cab, t)
    # PCM landing frame: the skid rails the PCM sets on
    for (a0, a1, b0, b1) in ((2178, 2212, 1314, 1314.6), (2178, 2212, 1323.4, 1324), (2178, 2178.6, 1314, 1324),
                             (2211.4, 2212, 1314, 1324)):
        box(a0, a1, b0, b1, .6, 1.1, "steel")
        n += 1
    # generator power: factory cable bus from the generator terminal landing to the PCM breaker, two bolted sections
    # on a pair of portal supports, both ends flanged and capped
    xb0, xb1, zb0, zb1 = 2201.8, 2204.2, 8.6, 11.0
    for yp in (1302.0, 1311.0):
        for xp in (2200.6, 2205.4):
            box(xp - .9, xp + .9, yp - .9, yp + .9, 0, .4, "concrete")
            box(xp - .2, xp + .2, yp - .2, yp + .2, .4, zb0 - .4, "steel")
        box(2200.2, 2205.8, yp - .25, yp + .25, zb0 - .4, zb0, "steel")
        n += 5
    for (y0, y1) in ((1300.8, 1307.0), (1307.0, 1313.4)):
        box(xb0, xb1, y0, y1, zb0, zb1, "alu")
        for xs in (xb0 - .05, xb1):                                                    # ventilation slots
            box(xs, xs + .05, y0 + .6, y1 - .6, zb0 + .9, zb0 + 1.5, "louvre")
        n += 3
    for yf in (1300.8, 1307.0, 1313.4):                                                 # flanges, the middle one bolted
        box(xb0 - .25, xb1 + .25, yf - .15, yf + .15, zb0 - .25, zb1 + .25, "steel")
        n += 1
    for yf, s in ((1300.8, -1), (1313.4, 1)):                                          # end caps
        box(xb0 + .2, xb1 - .2, yf + s * .15, yf + s * .4, zb0 + .2, zb1 - .2, "red")
        n += 1
    showcase.decal((2203.0, 1300.2, zb0 - 1.3), (0, -1, 0), 4.0, 1.1, [("CABLE BUS  ·  GEN → PCM", .3, True, "#111111"),
                   ("13.8 kV  ·  AWAITING GENERATOR", .22, False, "#b3261e")], bg="#ffffff")
    # ground grid: bare copper pigtails up at the foundation and PCM pad corners
    for (gx, gy) in ((2086.0, 1271.0), (2150.0, 1271.0), (2214.0, 1271.0), (2086.0, 1299.0), (2150.0, 1299.0),
                     (2214.0, 1299.0), (2176.0, 1313.0), (2214.0, 1325.0)):
        z = .6 if gy > 1310 else .5
        rod((gx, gy, z), (gx, gy, z + 1.4), .07, "copper", seg=6)
        rod((gx, gy, z + 1.4), (gx + .5, gy, z + 1.7), .07, "copper", seg=6)
        n += 2
    fuel.D = False
    showcase.decal((2084.2, 1306.0, 5.2), (-1, 0, 0), 11.0, 3.0,
                   [("PLUG & PLAY", .36, True, "#ffffff"), ("CABLE SYSTEM INSTALLED  ·  PRE-TERMINATED", .17, False, "#c4744a"),
                    ("SET THE EQUIPMENT  ·  CONNECT  ·  ENERGISE", .15, False, "#ffffff")], bg="#1d1f21")
    return n
