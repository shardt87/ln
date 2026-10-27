"""Modular yard technology bays (owner, Oct 27: one modular power unit per technology, each in its own bay). The
technology row (container genset, enclosed gas genset, open engine skid, fuel cell + inverter, microturbine) gets a
painted bay outline and a sign at the front of each bay naming the technology, its rating and its cable story; the
trailer genset and the trailer gas turbine get a sign each. Generic (no vendor names on the signs); the gas blocks keep
their own sign at the south end of the group road (genset_blocks.sign). Typical, not engineered."""
import fuel
from fuel import box, rod

# bay outline (x0, x1) on y 513-547, sign at the bay front (y 510.5), title, rating, cable story
ROW = [
    ((1992, 2048), "CONTAINER GAS GENSET", "~2 MW · 13.8 kV · 40 ft container", "SHD-GC leads to GSP-1 > PAD-EH"),
    ((2054, 2106), "ENCLOSED GAS GENSET", "2 MW · 480 V", "480 V leads to PAD-LV · control"),
    ((2112, 2144), "OPEN ENGINE SKID", "1 MW · 480 V", "480 V leads to PAD-LV · control"),
    ((2150, 2192), "FUEL CELL + INVERTER", "~250 kW · solid-oxide", "DC to the inverter · 480 V AC"),
    ((2196, 2214), "MICROTURBINE", "1 MW · 480 V", "480 V leads to PAD-LV"),
]
TRAILERS = [
    (2154.0, 690.0, "TRAILER GENSET", "13.8 kV · on wheels", "SHD-GC through the cable ramp"),
    (2144.0, 735.0, "TRAILER GAS TURBINE", "~35 MW · 13.8 kV", "15 kV MV-105 leads, 3 per phase"),
]
Y0, Y1 = 513.0, 547.0


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def sign(x, y, title, rating, story):
    for s in (-1.8, 1.8):
        rod((x + s, y, 0), (x + s, y, 6.4), .08, "steel", seg=6)
    decal((x, y - .12, 4.7), (0, -1, 0), 4.4, 2.4, [(title, .17, 1, "#ffffff"), (rating, .13, 0, "#e6e6e6"),
                                                   ("cable: " + story, .12, 1, "#f2c200")], bg="#22303a")


def build():
    n = 0
    for (x0, x1), title, rating, story in ROW:
        it = fuel.new_item("OPT_MODX", f"Technology bay: {title.lower()} (outline and sign)", (x0, x1, 509.6, Y1),
                           (0, 6.6), area="I", register=False, basis="typical",
                           info=f"Modular yard technology bay: {title.lower()}, {rating}; cable: {story}.")
        fuel.on(it)
        fuel.D = True
        for (a0, a1, b0, b1) in ((x0, x1, Y0, Y0 + .4), (x0, x1, Y1 - .4, Y1), (x0, x0 + .4, Y0, Y1), (x1 - .4, x1, Y0, Y1)):
            box(a0, a1, b0, b1, 0, .03, "amber")                                         # painted bay outline
        sign((x0 + x1) / 2, 510.5, title, rating, story)
        fuel.D = False
        n += 1
    for x, y, title, rating, story in TRAILERS:
        it = fuel.new_item("OPT_MODX", f"Technology bay sign: {title.lower()}", (x - 2.4, x + 2.4, y - .4, y + .4), (0, 6.6),
                           area="I", register=False, basis="typical",
                           info=f"Modular yard technology bay: {title.lower()}, {rating}; cable: {story}.")
        fuel.on(it)
        fuel.D = True
        sign(x, y, title, rating, story)
        fuel.D = False
        n += 1
    return n
