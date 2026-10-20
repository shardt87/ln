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
        # generator leads and control at the generator end of the foundation, towards the PCM (SC-4: the prefab
        # tray run carries them instead, demo() below)
        if name == "SC-3":
            n += stubs(xg - 4, xg + 4, FY1 - 4, FY1 - 1, .5, 4, 2)
        # handhole beside the PCM pad, on the duct-bank line (SC-4: east of its PCM pad, clear of the tray run)
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
TY = 1306.0                                                   # tray run centre line, between foundation and PCM pad
TZ = 1.6                                                      # module frame bottom, on steel pedestals


def coil(x, y, z, cab, tag=None):
    """Factory-terminated tail coiled flat at a landing point, end capped, tag on it."""
    import showcase
    for k in range(3):
        rod((x, y, z + k * .22), (x, y, z + k * .22 + .2), 1.1 - k * .12, cab, seg=18)
    rod((x + .9, y, z + .7), (x + 1.6, y, z + .7), .16, cab, seg=8)
    rod((x + 1.6, y, z + .7), (x + 2.0, y, z + .7), .2, "red", seg=8)                  # end cap
    if tag:
        showcase.decal((x, y - 1.25, z + 1.4), (0, -1, 0), 2.6, .7, [(tag, .32, True, "#111111"),
                       ("TERMINATED  ·  TESTED", .22, False, "#2f7a3c")], bg="#ffffff")
    return 6


def outline(x0, x1, y0, y1, z):
    """Painted footprint of the equipment still to come."""
    w = .3
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + w), (x0, x1, y1 - w, y1), (x0, x0 + w, y0, y1), (x1 - w, x1, y0, y1)):
        box(a0, a1, b0, b1, z, z + .02, "deck_line")
    return 4


def demo():
    """SC-4's pad as the prefab, plug-and-play showcase (owner, Oct 20): everything but the equipment. Three 40 ft
    factory cable modules (prefab.py's spine modules: power, control and fibre tiers, cable laid and tied) on steel
    pedestals between the foundation and the PCM pad; pigtails dropped and coiled at each landing point on the
    foundation, factory-terminated and tested; the equipment footprints painted on the slab; a landing frame on the
    PCM pad with the module tails dropped into it. SC-3 stays the plain reserved pad beside it."""
    import prefab
    import showcase
    it = new_item("OPT_MOD", "Reserved pad SC-4: plug-and-play prefab cable demonstration", [2084, 2234, 1268, 1328],
                  [0, 9], area="I", register=False,
                  info="The future SC-4 pad with its cable system already in: three factory-built 40 ft cable "
                       "modules (power / control / fibre tiers, cable laid and tied), pigtails coiled and tested at "
                       "each equipment landing point, a landing frame on the PCM pad. Set the equipment, connect, "
                       "energise. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    xs = (2090.0, 2130.0, 2170.0)
    for x in xs + (2210.0,):                                                            # pedestals at the splices
        for s in (-2.2, 2.2):
            box(x - .4, x + .4, TY + s - .4, TY + s + .4, .0, TZ, "steel")
            box(x - .9, x + .9, TY + s - .9, TY + s + .9, .0, .25, "concrete")
        n += 4
    for k, x in enumerate(xs):
        prefab.module(TY, x, TZ, along="x", tails=(k == 2), wrap=False,
                      tag=[(f"SC-4  M{k + 1:02d}", .26, 1, "#111111"), (f"{k + 1} OF 3  ·  PCM  →  GT / AUX", .16, 0, "#222222"),
                           ("PRE-WIRED  ·  TESTED", .14, 0, "#2f7a3c"), ("PREFAB CABLE MODULE", .14, 1, "#ffffff", 0, "#b5651d")])
        n += 1
    on(it)
    # the equipment still to come, painted on the slab (package east, SCR west, as SC-2), and the landing points
    n += outline(2125.5, 2214.5, 1270.5, 1299.5, .5)                                   # GT package
    n += outline(2085.5, 2124.5, 1270.5, 1299.5, .5)                                   # SCR / CO catalyst
    n += outline(2177.0, 2213.0, 1313.5, 1324.5, .6)                                   # PCM
    landings = ((2203.0, "GEN TB", "cable_mv"), (2160.0, "TCP", "cable_inst"), (2135.0, "AUX SKID", "cable_tc"),
                (2095.0, "SCR / CEMS", "cable_tc"))
    for (x, t, cab) in landings:
        # pigtail drops from the module's bottom tier to the foundation edge and is coiled at the landing point
        rod((x, TY - 2.0, TZ + .5), (x, TY - 3.6, TZ + .2), .18, cab, seg=8)
        rod((x, TY - 3.6, TZ + .2), (x, 1301.0, .6), .18, cab, seg=8)
        n += 2 + coil(x, 1297.0, .5, cab, t)
    # PCM landing frame: skid rails the PCM sets on, the module tails dropped into it
    for (a0, a1, b0, b1) in ((2178, 2212, 1314, 1314.6), (2178, 2212, 1323.4, 1324), (2178, 2178.6, 1314, 1324),
                             (2211.4, 2212, 1314, 1324)):
        box(a0, a1, b0, b1, .6, 1.1, "steel")
        n += 1
    for k, cab in enumerate(("cable_mv", "cable_tc", "cable_inst")):
        x = 2206.0 - k * 3
        rod((2210.6, TY + .5, TZ + .4 + k * 2.5), (x, 1312.0, 1.6), .2, cab, seg=8)
        n += 1 + coil(x, 1317.0, .6, cab, ("GEN LEADS", "CONTROL", "FIBRE")[k])
    fuel.D = False
    showcase.decal((2084.2, 1306.0, 5.2), (-1, 0, 0), 11.0, 3.0,
                   [("PLUG & PLAY", .36, True, "#ffffff"), ("PREFAB CABLE SYSTEM INSTALLED", .17, False, "#c4744a"),
                    ("SET THE EQUIPMENT  ·  CONNECT  ·  ENERGISE", .15, False, "#ffffff")], bg="#1d1f21")
    return n
