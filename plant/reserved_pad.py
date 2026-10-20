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
        # generator leads and control at the generator end of the foundation, towards the PCM
        n += stubs(xg - 4, xg + 4, FY1 - 4, FY1 - 1, .5, 4, 2)
        # handhole beside the PCM pad, on the duct-bank line
        hx = p0 + 12
        box(hx - 2, hx + 2, PY0 - 6, PY0 - 2, 0, .25, "concrete")
        box(hx - 1.6, hx + 1.6, PY0 - 5.6, PY0 - 2.4, .25, .3, "steel")
        # fuel-gas tie-in riser, capped and blinded, at the foundation's north edge
        xr = (f0 + f1) / 2
        rod((xr, FY0 - 2, 0), (xr, FY0 - 2, 2.6), .33, "fuelgas", seg=12)
        rod((xr, FY0 - 2, 2.6), (xr, FY0 - 2, 2.9), .6, "steel", seg=12)
        n += 4
    fuel.D = False
    showcase.decal((X0 - 1.2, 1299.0, 5.0), (-1, 0, 0), 15.0, 3.2,
                   [("RESERVED - SC-3 / SC-4", .4, True, "#ffffff"),
                    ("FUTURE SIMPLE-CYCLE PAIR  ·  PRE-WIRED", .2, False, "#c4744a")], bg="#1d1f21")
    return n + 1
