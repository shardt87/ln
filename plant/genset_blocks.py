"""Detail on genset block 1 (GB-1.1..1.4, GBS-1, GBT-1) of the modular gas genset blocks (owner, Oct 26): the wire
scope made visible on one block, the five others left plain (same geometry, kept light for the phone viewer):
- the lead trench opened: a precast trench from the four gensets to the block switchgear with its covers lifted and
  stacked, the 480 V lead sets (2 sets of 3 x 500 kcmil + ground per genset) laid in it with phase tape at the ends,
  the control, instrumentation and aux cables on the far side of the trench;
- GB-1.1's generator terminal box open: the two lead sets landed on the generator lugs;
- the block ground ring: bare copper round the block with a tail to each genset, the switchgear and the pad-mount;
- a sign at the row: six blocks x four ~450 kW gensets, 480 V to 13.8 kV.
Typical, not engineered (block geometry from build_model GB_BLOCKS)."""
import fuel
from fuel import box, rod

BX, BY = 2254.0, 458.0                    # block 1 origin (build_model GB_BLOCKS[0])
TY0, TY1 = BY + 7.6, BY + 10.4             # trench (y), under the lead routes at y BY + 9
TAPE = ("red", "amber", "pvc_blue")


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def trench():
    x0, x1 = BX + 3.0, BX + 40.0
    box(x0, x1, TY0, TY0 + .3, -.1, .35, "concrete")                              # trench walls (precast, flush)
    box(x0, x1, TY1 - .3, TY1, -.1, .35, "concrete")
    box(x0, x1, TY0, TY1, -.15, -.05, "concrete")                                  # floor
    box(x0 - .3, x0, TY0, TY1, -.1, .35, "concrete")
    for k in range(6):                                                             # covers lifted and stacked
        box(BX + 41.0, BX + 44.0, TY0 - .2, TY1 + .2, .0 + k * .22, .2 + k * .22, "concrete")
    # lead sets: per genset 2 sets of 3 x 500 kcmil + ground, from the genset's tail down into the trench and west
    for m in range(4):
        gx = BX + 5.0 + 11.0 * m
        for s in range(2):
            for c in range(4):
                o = (s * 4 + c) * .17
                y = TY0 + .45 + (m % 2) * .1 + o * .2
                z = .05 + (m * 2 + s) * .0 + c * .0
                col = "cable" if c < 3 else "pvc_green"
                xx = gx - .6 + o
                rod((xx, BY + 11.4, 2.6), (xx, BY + 11.4, .2), .1, col, seg=6)               # out of the terminal box
                rod((xx, BY + 11.4, .2), (xx, y + .3, .05), .1, col, seg=6)
                rod((xx, y + .3, .05), (BX + 11.0 + o * .4, y + .3, .05), .1, col, seg=6)    # along the trench to GBS-1
        # control / instrumentation / aux on the north side of the trench
        for j, col in enumerate(("cable_tc", "cable_inst", "cable_tc")):
            rod((gx + .9 + j * .2, BY + 11.6, 1.2), (gx + .9 + j * .2, TY1 - .5, .05), .06, col, seg=6)
            rod((gx + .9 + j * .2, TY1 - .5, .05), (BX + 12.0, TY1 - .5 - j * .1, .05), .06, col, seg=6)
    for k in range(12):                                                            # the bundle rising into GBS-1
        rod((BX + 11.0 + k * .12, TY0 + .6, .05), (BX + 11.0 + k * .12, BY + 6.2, 2.5), .1, "cable", seg=6)
    return 1


def terminal_box_open():
    gx = BX + 1.0
    box(gx + 1.5, gx + 6.5, BY + 11.0, BY + 11.4, 2.5, 6.0, "panel")              # back of the open box
    box(gx + 1.2, gx + 1.5, BY + 9.0, BY + 11.4, 2.5, 6.0, "panel")               # door swung out
    for k in range(3):                                                             # generator lugs / bus
        x = gx + 2.4 + k * 1.3
        box(x - .25, x + .25, BY + 11.0, BY + 11.1, 4.6, 5.4, "copper")
        rod((x, BY + 11.05, 4.7), (x, BY + 11.05, 2.6), .1, "cable", seg=6)
        rod((x + .3, BY + 11.05, 4.7), (x + .3, BY + 11.05, 2.6), .1, "cable", seg=6)
        rod((x, BY + 11.03, 4.4), (x, BY + 11.03, 4.2), .12, TAPE[k], seg=8)
    box(gx + 2.0, gx + 6.0, BY + 11.05, BY + 11.15, 3.2, 3.35, "copper")          # ground bar
    return 1


def ground_ring():
    x0, x1, y0, y1 = BX - 1.0, BX + 45.0, BY - 2.0, BY + 37.0
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        rod((a[0], a[1], .08), (b[0], b[1], .08), .05, "copper", seg=4)
    for m in range(4):
        gx = BX + 1.0 + 11.0 * m
        rod((gx, y1, .08), (gx, BY + 34.0, .08), .04, "copper", seg=4)
        rod((gx, BY + 34.0, .08), (gx, BY + 34.0, 1.2), .04, "copper", seg=4)
    rod((BX + 2.0, y0, .08), (BX + 2.0, BY, .08), .04, "copper", seg=4)
    rod((BX + 36.0, y0, .08), (BX + 36.0, BY, .08), .04, "copper", seg=4)
    return 1


def sign():
    x, y = BX - 6.0, BY + 4.0
    for s in (-1.6, 1.6):
        rod((x, y + s, 0), (x, y + s, 6.4), .08, "steel", seg=6)
    decal((x + .1, y, 4.6), (1, 0, 0), 4.0, 2.6, [("MODULAR GAS GENSET BLOCKS", .17, 1, "#ffffff"),
                                                  ("6 blocks x 4 gensets x ~450 kW", .13, 0, "#e6e6e6"),
                                                  ("480 V to 13.8 kV, into PAD-EH", .13, 0, "#e6e6e6"),
                                                  ("block 1: lead trench open", .12, 1, "#f2c200")], bg="#22303a")
    return 1


def build():
    it = fuel.new_item("OPT_MODX", "Genset block 1 detail: open lead trench, terminal box open, ground ring, sign",
                       (2246, 2300, 454, 497), (-.2, 7), area="I", register=False, basis="typical",
                       info="The wire scope on one block: 480 V lead sets (2 x 3 x 500 kcmil + ground per genset) in an open "
                            "precast trench to the block switchgear, control / instrumentation / aux beside them, GB-1.1's "
                            "terminal box open on the leads, the bare-copper ground ring with tails. Typical, not engineered.")
    fuel.on(it)
    fuel.D = True
    n = trench() + terminal_box_open() + ground_ring() + sign()
    fuel.D = False
    return n
