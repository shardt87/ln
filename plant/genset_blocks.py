"""Detail on modular gas block GB-1 (GB-1.1..1.5, GBC-1, GBT-1), the wire scope made visible on one block; the five other
blocks stay plain (same geometry, kept light for the phone viewer):
- the L1 lead trench opened along the south side: precast trench from the five units to the generator collector box, its
  covers lifted and stacked at the west end, the 480 V lead sets (2 sets of 3 x 500 kcmil + ground per unit) laid in it,
  the control / instrumentation cables on the far side, the leads rising into GBC-1;
- GB-1.1's generator terminal box open on its two lead sets;
- the block ground ring (bare copper) with a tap to each unit, the GBC and the transformer;
- a sign: six blocks x five 500 kW units, 480 V -> 34.5 kV loop -> SWG-MY -> data centre.
Typical, not engineered (block geometry from build_model GB_BLOCKS)."""
import fuel
from fuel import box, rod

BX, BY = 2262.0, 458.0                    # block GB-1 origin (build_model GB_BLOCKS[0])
TY0, TY1 = BY + 6.3, BY + 8.7              # trench (y), under the lead route at y BY + 7.5
TX1 = BX + 46.0                            # trench east end, short of GBC-1 (x BX + 47)
TAPE = ("red", "amber", "pvc_blue")


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def ux(m):
    return BX + 2 + 8.6 * m


def trench():
    x0 = BX + 1.0
    box(x0, TX1, TY0, TY0 + .3, -.1, .35, "concrete")                                 # trench walls (precast, flush)
    box(x0, TX1, TY1 - .3, TY1, -.1, .35, "concrete")
    box(x0, TX1, TY0, TY1, -.15, -.05, "concrete")                                     # floor
    box(x0 - .3, x0, TY0, TY1, -.1, .35, "concrete")
    for k in range(6):                                                                 # covers lifted, stacked west
        box(BX - 5.0, BX - 2.0, TY0 - .2, TY1 + .2, k * .22, .2 + k * .22, "concrete")
    for m in range(5):                                                                 # per unit 2 sets x 4 conductors
        xt = ux(m) + 6.2
        for s in range(2):
            for c in range(4):
                o = (s * 4 + c) * .15
                y = TY0 + .45 + o * .9 + (m % 2) * .05
                col = "cable" if c < 3 else "pvc_green"
                xx = xt - .5 + o * .8
                rod((xx, BY + 9.55, 1.8), (xx, BY + 9.55, .15), .09, col, seg=6)            # out of the terminal box
                rod((xx, BY + 9.55, .15), (xx, y, .05), .09, col, seg=6)
                rod((xx, y, .05), (TX1 - .4, y, .05), .09, col, seg=6)                     # along the trench to GBC-1
        for j, col in enumerate(("cable_tc", "cable_inst")):                           # control / instrumentation
            xc = ux(m) + 1.6 + j * .2
            rod((xc, BY + 9.9, 1.2), (xc, TY1 - .5, .05), .06, col, seg=6)
            rod((xc, TY1 - .5, .05), (TX1 - .4, TY1 - .5 - j * .1, .05), .06, col, seg=6)
    for k in range(12):                                                                # the bundle rising into GBC-1
        y = TY0 + .5 + k * .14
        rod((TX1 - .4, y, .05), (TX1 - .4, y, 2.6), .09, "cable", seg=6)
        rod((TX1 - .4, y, 2.6), (BX + 46.95, y, 2.6), .09, "cable", seg=6)
    return 1


def terminal_box_open():
    x0 = ux(0) + 5.0
    box(x0, x0 + 2.4, BY + 9.9, BY + 10.0, 1.6, 4.8, "panel")                          # back of the open box
    box(x0 - .3, x0, BY + 8.0, BY + 9.9, 1.6, 4.8, "panel")                            # door swung out
    for k in range(3):                                                                 # generator lugs
        x = x0 + .5 + k * .7
        box(x - .15, x + .15, BY + 9.8, BY + 9.9, 3.6, 4.3, "copper")
        rod((x, BY + 9.85, 3.7), (x, BY + 9.85, 1.8), .08, "cable", seg=6)
        rod((x + .2, BY + 9.85, 3.7), (x + .2, BY + 9.85, 1.8), .08, "cable", seg=6)
        rod((x, BY + 9.83, 3.4), (x, BY + 9.83, 3.25), .1, TAPE[k], seg=8)
    box(x0 + .3, x0 + 2.1, BY + 9.85, BY + 9.9, 2.3, 2.4, "copper")                    # ground bar
    return 1


def ground_ring():
    x0, x1, y0, y1 = BX - 1.0, BX + 73.0, BY - 1.0, BY + 22.0
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        rod((a[0], a[1], .08), (b[0], b[1], .08), .05, "copper", seg=4)
    for m in range(5):
        x = ux(m) + .5
        rod((x, y1, .08), (x, BY + 20.3, .08), .04, "copper", seg=4)
        rod((x, BY + 20.3, .08), (x, BY + 20.3, .9), .04, "copper", seg=4)
    rod((BX + 50.0, y0, .08), (BX + 50.0, BY + 5.0, .08), .04, "copper", seg=4)        # GBC-1
    rod((BX + 63.0, y0, .08), (BX + 63.0, BY + 1.0, .08), .04, "copper", seg=4)        # GBT-1
    return 1


def sign():
    x, y = BX - 4.0, BY + 15.0
    for s in (-1.6, 1.6):
        rod((x, y + s, 0), (x, y + s, 6.4), .08, "steel", seg=6)
    decal((x - .1, y, 4.6), (-1, 0, 0), 4.2, 2.6, [("MODULAR GAS BLOCKS", .17, 1, "#ffffff"),
                                                   ("6 blocks x 5 units x 500 kW", .13, 0, "#e6e6e6"),
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
    it = fuel.new_item("OPT_MODX", "Genset block 1 detail: open lead trench, terminal box open, ground ring, sign",
                       (BX - 6, BX + 74, BY - 2, BY + 23), (-.2, 7), area="I", register=False, basis="typical",
                       info="The wire scope on one block: 480 V lead sets (2 x 3 x 500 kcmil + ground per unit) in an open "
                            "precast trench to the generator collector box GBC-1, control / instrumentation beside them, "
                            "GB-1.1's terminal box open on its leads, the bare-copper ground ring with taps. Typical, not engineered.")
    fuel.on(it)
    fuel.D = True
    n = trench() + terminal_box_open() + ground_ring() + sign()
    fuel.D = False
    return n + ownership_sign()
