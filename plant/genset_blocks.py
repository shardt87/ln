"""Detail on modular gas block GB-1 (GB-1.1..1.5, GBC-1, GBT-1), the wire scope made visible on one block; the three
other blocks stay plain (same geometry, kept light for the phone viewer). Drawn in the block's local frame from
build_model.gb_frame(1): u along the block (south -> north), v across it (0 at the group road, 22 at the back).
- the L1 lead trench opened along the road side: precast trench from the five units to the generator collector box,
  covers lifted and stacked at the south end, the 480 V lead sets (2 sets of 3 x 500 kcmil + ground per unit) in it,
  control / instrumentation on the far side, the leads rising into GBC-1;
- GB-1.1's generator terminal box open on its two lead sets;
- the block ground ring (bare copper) with a tap to each unit, the GBC and the transformer;
- a sign at the south end of the group road.
Typical, not engineered."""
import fuel
from fuel import box, rod

RX, Y0 = 2302.0, 466.0                     # build_model GB_RX, GB_Y[0]
TV0, TV1 = 6.3, 8.7                        # trench (v), under the lead route at v 7.5
TU1 = 50.0                                 # trench north end, short of GBC-1 (u 51)
TAPE = ("red", "amber", "pvc_blue")


def T(u, v):                               # GB-1: west of the road
    return RX - 13.0 - v, Y0 + u


def tbox(u0, u1, v0, v1, z0, z1, c):
    (xa, ya), (xb, yb) = T(u0, v0), T(u1, v1)
    box(min(xa, xb), max(xa, xb), min(ya, yb), max(ya, yb), z0, z1, c)


def trod(a, b, r, c, seg=6):
    rod((*T(a[0], a[1]), a[2]), (*T(b[0], b[1]), b[2]), r, c, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def uu(m):
    return 2 + 10.0 * m


def trench():
    u0 = 1.0
    tbox(u0, TU1, TV0, TV0 + .3, -.1, .35, "concrete")                                  # trench walls (precast, flush)
    tbox(u0, TU1, TV1 - .3, TV1, -.1, .35, "concrete")
    tbox(u0, TU1, TV0, TV1, -.15, -.05, "concrete")                                     # floor
    tbox(u0 - .3, u0, TV0, TV1, -.1, .35, "concrete")
    for k in range(6):                                                                  # covers lifted, stacked south
        tbox(-5.0, -2.0, TV0 - .2, TV1 + .2, k * .22, .2 + k * .22, "concrete")
    for m in range(5):                                                                  # per unit 2 sets x 4 conductors
        ut = uu(m) + 6.2
        for s in range(2):
            for c in range(4):
                o = (s * 4 + c) * .15
                v = TV0 + .45 + o * .9 + (m % 2) * .05
                col = "cable" if c < 3 else "pvc_green"
                ux = ut - .5 + o * .8
                trod((ux, 9.55, 1.8), (ux, 9.55, .15), .09, col)                        # out of the terminal box
                trod((ux, 9.55, .15), (ux, v, .05), .09, col)
                trod((ux, v, .05), (TU1 - .4, v, .05), .09, col)                        # along the trench to GBC-1
        for j, col in enumerate(("cable_tc", "cable_inst")):                            # control / instrumentation
            uc = uu(m) + 1.6 + j * .2
            trod((uc, 9.9, 1.2), (uc, TV1 - .5, .05), .06, col)
            trod((uc, TV1 - .5, .05), (TU1 - .4, TV1 - .5 - j * .1, .05), .06, col)
    for k in range(12):                                                                 # the bundle rising into GBC-1
        v = TV0 + .5 + k * .14
        trod((TU1 - .4, v, .05), (TU1 - .4, v, 2.6), .09, "cable")
        trod((TU1 - .4, v, 2.6), (TU1 + .95, v, 2.6), .09, "cable")
    return 1


def terminal_box_open():
    u0 = uu(0) + 5.0
    tbox(u0, u0 + 2.4, 9.9, 10.0, 1.6, 4.8, "panel")                                     # back of the open box
    tbox(u0 - .3, u0, 8.0, 9.9, 1.6, 4.8, "panel")                                       # door swung out
    for k in range(3):                                                                  # generator lugs
        u = u0 + .5 + k * .7
        tbox(u - .15, u + .15, 9.8, 9.9, 3.6, 4.3, "copper")
        trod((u, 9.85, 3.7), (u, 9.85, 1.8), .08, "cable")
        trod((u + .2, 9.85, 3.7), (u + .2, 9.85, 1.8), .08, "cable")
        trod((u, 9.83, 3.4), (u, 9.83, 3.25), .1, TAPE[k], seg=8)
    tbox(u0 + .3, u0 + 2.1, 9.85, 9.9, 2.3, 2.4, "copper")                               # ground bar
    return 1


def ground_ring():
    u0, u1, v0, v1 = -1.0, 73.0, -1.0, 22.0
    for a, b in (((u0, v0), (u1, v0)), ((u1, v0), (u1, v1)), ((u1, v1), (u0, v1)), ((u0, v1), (u0, v0))):
        trod((a[0], a[1], .08), (b[0], b[1], .08), .05, "copper", seg=4)
    for m in range(5):
        u = uu(m) + .5
        trod((u, v1, .08), (u, 20.3, .08), .04, "copper", seg=4)
        trod((u, 20.3, .08), (u, 20.3, .9), .04, "copper", seg=4)
    trod((54.0, v0, .08), (54.0, 3.5, .08), .04, "copper", seg=4)                       # GBC-1
    trod((69.5, v0, .08), (69.5, 1.0, .08), .04, "copper", seg=4)                       # GBT-1
    return 1


def sign():
    x, y = RX - 13.0, Y0 - 24.0                                                         # south of the park lane, facing it
    for s in (-1.6, 1.6):
        rod((x + s, y, 0), (x + s, y, 6.4), .08, "steel", seg=6)
    decal((x, y - .1, 4.6), (0, -1, 0), 4.2, 2.6, [("MODULAR GAS BLOCKS", .17, 1, "#ffffff"),
                                                   ("4 blocks x 5 units x 500 kW", .13, 0, "#e6e6e6"),
                                                   ("480 V > 34.5 kV loop > SWG-MY", .13, 0, "#e6e6e6"),
                                                   ("GB-1: lead trench open", .12, 1, "#f2c200")], bg="#22303a")
    return 1


def ownership_sign():
    """Where the SWG-MY feeder (L5) crosses the fence to the data centre: the ownership line, scope TO VERIFY."""
    it = fuel.new_item("OPT_MODX", "Ownership-line sign: SWG-MY feeder crosses the fence (ER scope / customer scope, to verify)",
                       (2406, 2414, 896, 904), (0, 7), area="I", register=False, basis="typical",
                       info="Marks where the L5 feeder from SWG-MY to the data centre's 34.5 kV switchgear crosses the fence. "
                            "Whether the feeder is the generator owner's cable or the data centre's is TO VERIFY.")
    fuel.on(it)
    fuel.D = True
    x, y = 2410.0, 900.0
    for s in (-1.8, 1.8):
        rod((x, y + s, 0), (x, y + s, 6.6), .08, "steel", seg=6)
    for nx in (1, -1):
        decal((x + .1 * nx, y, 4.8), (nx, 0, 0), 4.4, 2.6, [("OWNERSHIP LINE", .18, 1, "#ffffff"),
                                                           ("35 kV feeder SWG-MY > data centre", .12, 0, "#e6e6e6"),
                                                           ("generator scope | customer scope", .12, 0, "#e6e6e6"),
                                                           ("TO VERIFY", .14, 1, "#ef6a5a")], bg="#3a1f1c")
    fuel.D = False
    return 1


def build():
    xs = [T(u, v)[0] for u, v in ((-6, -2), (74, 23))]
    ys = [T(u, v)[1] for u, v in ((-6, -2), (74, 23))]
    it = fuel.new_item("OPT_MODX", "Genset block 1 detail: open lead trench, terminal box open, ground ring, sign",
                       (min(xs), max(xs), min(ys) - 2, max(ys)), (-.2, 7), area="I", register=False, basis="typical",
                       info="The wire scope on one block: 480 V lead sets (2 x 3 x 500 kcmil + ground per unit) in an open "
                            "precast trench to the generator collector box GBC-1, control / instrumentation beside them, "
                            "GB-1.1's terminal box open on its leads, the bare-copper ground ring with taps. Typical, not engineered.")
    fuel.on(it)
    fuel.D = True
    n = trench() + terminal_box_open() + ground_ring() + sign()
    fuel.D = False
    return n + ownership_sign()
