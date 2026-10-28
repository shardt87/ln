"""Modular yard technology sites (owner, Oct 27: one technology per site, each a small working installation on its own
fenced gravel pad, built in build_model.tech_site): a sign at each site gate naming the technology, its rating and its
cable story; the trailer genset and the trailer gas turbine get a sign each. Generic (no vendor names on the signs); the gas blocks keep
their own sign at the south end of the group road (genset_blocks.sign). Typical, not engineered."""
import fuel
from fuel import rod

# site signs at each gate: (x, y), title, rating, cable story
SITES = [
    ((1962.0, 536.0), "TRAILER GAS-ENGINE FLEET", "6 x ~2.5 MW trailers · 13.8 kV", "SHD-GC > switchgear trailer > 35 kV step-up"),
    ((1962.0, 465.0), "CONTAINERIZED GAS ENGINES", "4 x ~4.4 MW · stacked: engines below, cooling above", "15 kV leads > switchgear > 35 kV step-up"),
    ((1962.0, 655.0), "MID-SIZE GAS TURBINES", "2 x ~16 MW packages · 13.8 kV", "15 kV leads > step-up > 35 kV collector"),
    ((2116.0, 650.5), "GAS ENGINES + HEAT RECOVERY", "4 x ~2.5 MW · exhaust heat to hot water", "15 kV leads > switchgear > PAD-EH"),
    ((2105.0, 616.0, 1), "PARALLELED GAS GENSETS", "8 x 1 MW · 480 V paralleled", "480 V leads > switchgear > 2 pad-mounts to 35 kV"),
    ((2140.0, 441.0, 1), "LINEAR GENERATORS", "4 x ~250 kW · gas, DC out", "DC to the inverter · 480 V AC"),
    ((2040.0, 338.5), "FUEL CELLS + MICROTURBINES", "4 x ~250 kW SOFC · 3 x 1 MW microturbines", "480 V > inverter / switchboard > PAD"),
]
TRAILERS = [
    (2154.0, 708.0, "TRAILER GENSET", "13.8 kV · on wheels", "SHD-GC through the cable ramp"),
    (2144.0, 735.0, "TRAILER GAS TURBINE", "~35 MW · 13.8 kV", "15 kV MV-105 leads, 3 per phase"),
]


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def sign(x, y, title, rating, story, ny=-1):
    """ny: the face direction, -1 south (default), +1 north: signs face the road the site's vehicle gate opens on."""
    for s in (-1.8, 1.8):
        rod((x + s, y, 0), (x + s, y, 6.4), .08, "steel", seg=6)
    decal((x, y + .12 * ny, 4.7), (0, ny, 0), 4.4, 2.4, [(title, .17, 1, "#ffffff"), (rating, .13, 0, "#e6e6e6"),
                                                   ("cable: " + story, .12, 1, "#f2c200")], bg="#22303a")


def build():
    n = 0
    for pos, title, rating, story in SITES:
        x, y = pos[:2]
        ny = pos[2] if len(pos) > 2 else -1
        it = fuel.new_item("OPT_MODX", f"Site sign: {title.lower()}", (x - 2.4, x + 2.4, y - .4, y + .4), (0, 6.6),
                           area="I", register=False, basis="typical",
                           info=f"Modular yard technology site: {title.lower()}, {rating}; cable: {story}.")
        fuel.on(it)
        fuel.D = True
        sign(x, y, title, rating, story, ny)
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
