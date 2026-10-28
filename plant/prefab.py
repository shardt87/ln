"""Prefabricated cable systems: the modular-yard cable spine going in, and the prefab staging bay on the reel /
outage laydown pad.

- Cable spine (modular-yard expansion, OPT_MODX): an elevated LV power / control / fibre spine from the MOD-EH
  e-house north toward the aeroderivative units, built from 40 ft factory modules: a welded frame carrying three
  ladder-tray tiers (EL 12 power, EL 14.5 control / instrumentation, EL 17 fibre innerduct) with the cable already
  laid and tied, coiled tails at the leading end. Bents every 20 ft on pier footings. Modules 1-4 are set and
  spliced; module 5 hangs from a mobile crane on a spreader bar, two riggers on tag lines, two electricians on a
  boom lift at the splice; the bents for module 6 stand ready.
- Prefab staging bay (south strip of the reel / outage laydown pad): spine modules 6-9 on timber dunnage,
  shrink-wrapped tails, sequence tags; one arriving on a flatbed trailer; pre-terminated MV cable assemblies in
  open crates (factory terminations, capped ends); prefab multi-conduit racks; pre-wired junction-box skids.

Generic labels (prefabricated cable spine / pre-terminated assemblies); typical, not engineered.
"""
import math

import fuel
from fuel import box, rod

SX = 1976.0                       # spine centre line (x)
SY0 = 904.0                       # MOD-EH north face is y 900
MOD = 40.0
TIERS = ((12.0, "cable_tc", "POWER"), (14.5, "cable_inst", "CONTROL"), (17.0, "cable_fo", "FIBRE"))
HW = 2.5                          # half width of the module frame


def person(x, y, z=0.0, a=0.0, vest="hivis", hat="hardhat"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest, hat=hat)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


# ------------------------------------------------------------------------------- spine module (along y, or x)
def module(x, y0, z0, along="y", n=1, tails=False, wrap=False, tag=None):
    """One 40 ft spine module with its frame bottom at z0, starting at (x, y0) and running +y (or +x)."""
    def B(a0, a1, s0, s1, z_0, z_1, c):                     # a along the module, s across
        if along == "y":
            box(x + s0, x + s1, y0 + a0, y0 + a1, z_0, z_1, c)
        else:
            box(y0 + a0, y0 + a1, x + s0, x + s1, z_0, z_1, c)

    def R(a, s, z, a2, s2, z2, r, c):
        if along == "y":
            rod((x + s, y0 + a, z), (x + s2, y0 + a2, z2), r, c, seg=8)
        else:
            rod((y0 + a, x + s, z), (y0 + a2, x + s2, z2), r, c, seg=8)
    top = z0 + 6.6
    for s in (-HW, HW - .35):                                # bottom chords and top chords
        B(0, MOD, s, s + .35, z0, z0 + .45, "steel")
        B(0, MOD, s, s + .35, top - .35, top, "steel")
    for k in range(5):                                       # verticals and cross members every 10 ft
        a = min(MOD - .3, k * 10)
        for s in (-HW, HW - .3):
            B(a, a + .3, s, s + .3, z0 + .45, top - .35, "steel")
        for dz in (.0, 2.5, 5.0):
            B(a, a + .3, -HW, HW, z0 + dz, z0 + dz + .3, "steel")
        if k < 4:                                            # diagonal bracing on both sides
            for s in (-HW + .15, HW - .15):
                R(a + .3, s, z0 + .45, a + 9.7, s, top - .35, .07, "steel")
    for (zt, cab, _), dz in zip(TIERS, (.3, 2.8, 5.3)):
        zt = z0 + dz
        for s in (-1.9, 1.75):                               # ladder tray side rails
            B(0, MOD, s, s + .15, zt, zt + .5, "pipe")
        for k in range(40):                                  # rungs
            B(k + .4, k + .55, -1.9, 1.9, zt, zt + .08, "pipe")
        B(0, MOD, -1.7, 1.6, zt + .08, zt + .38, cab)          # cable laid in the tray
        if tails:                                            # coiled tails at the leading end, waiting for the next module
            for s in (-1.0, .4):
                R(MOD + .2, s, zt + .3, MOD + .2, s + .8, zt + .3, .45, cab)
                R(MOD + .1, s - .1, zt + .3, MOD + .3, s + .9, zt + .3, .5, "tent" if wrap else cab)
        if wrap:
            B(-.1, .25, -2.0, 2.0, zt - .05, zt + .6, "tent")
            B(MOD - .25, MOD + .1, -2.0, 2.0, zt - .05, zt + .6, "tent")
    if tag:
        if along == "y":
            decal((x + HW + .03, y0 + 4, z0 + 1.6), (1, 0, 0), 3.2, 1.3, tag, bg="#ffffff")
        else:
            decal((y0 + 4, x - HW - .03, z0 + 1.6), (0, -1, 0), 3.2, 1.3, tag, bg="#ffffff")


def tag_lines(n, of, route="MOD-EH  →  SC-1"):
    return [(f"SPINE  M{n:02d}", .26, 1, "#111111"), (f"{n} OF {of}  ·  {route}", .16, 0, "#222222"),
            ("TOS EL 11'-0\"  ·  MATCH MARK A/B", .13, 0, "#444444"), ("PREFAB CABLE SPINE", .14, 1, "#ffffff", 0, "#b5651d")]


def bent(y, z_top=11.0):
    """Two-post bent with a top beam on pier footings."""
    for s in (-HW - .5, HW + .5):
        box(SX + s - .6, SX + s + .6, y - .6, y + .6, 0, 1.0, "concrete")
        box(SX + s - .25, SX + s + .25, y - .25, y + .25, 1.0, z_top, "steel")
    box(SX - HW - 1.0, SX + HW + 1.0, y - .3, y + .3, z_top - .6, z_top, "steel")


def crane(cx, cy, tip):
    """Truck-mounted crane: carrier with outriggers on pads, superstructure, telescopic boom to the tip."""
    L, W = 42, 9
    box(cx - L / 2, cx + L / 2, cy - W / 2, cy + W / 2, 2.0, 4.6, "crane")                   # carrier
    for k in range(5):
        ax = cx - L / 2 + 5 + k * 7.5
        for s in (-1, 1):
            rod((ax, cy + s * (W / 2 - .4), 1.9), (ax, cy + s * (W / 2 + .3), 1.9), 1.9, "tyre", seg=14)
    box(cx + L / 2 - 8, cx + L / 2, cy - W / 2, cy - W / 2 + 4, 4.6, 9.0, "crane")              # cab
    for (ox, oy) in ((-L / 2 + 3, -1), (-L / 2 + 3, 1), (L / 2 - 4, -1), (L / 2 - 4, 1)):     # outriggers
        px, py = cx + ox, cy + oy * (W / 2 + 7)
        box(min(cx + ox - .6, px - .6), max(cx + ox + .6, px + .6), min(cy, py) if oy > 0 else py, max(cy, py) if oy < 0 else py,
            3.2, 4.2, "crane")
        rod((px, py, 4.0), (px, py, .4), .35, "steel", seg=8)
        box(px - 2, px + 2, py - 2, py + 2, 0, .4, "timber")
    box(cx - 8, cx + 6, cy - 5, cy + 5, 4.6, 10.5, "crane")                                     # superstructure
    box(cx - 12, cx - 8, cy - 4, cy + 4, 4.6, 9.5, "steel_dark")                                # counterweight
    pivot = (cx + 2, cy, 10.0)
    dx, dy, dz = tip[0] - pivot[0], tip[1] - pivot[1], tip[2] - pivot[2]
    for k, r in enumerate((1.4, 1.15, .9, .7)):                                                 # telescopic sections
        t0, t1 = k / 4, (k + 1.12) / 4
        rod((pivot[0] + dx * t0, pivot[1] + dy * t0, pivot[2] + dz * t0),
            (pivot[0] + dx * min(1, t1), pivot[1] + dy * min(1, t1), pivot[2] + dz * min(1, t1)), r, "crane", seg=10)
    rod((cx + 2, cy, 6), (pivot[0] + dx * .35, pivot[1] + dy * .35, pivot[2] + dz * .35), .5, "steel", seg=8)  # luffing ram
    rod(tip, (tip[0] + 1.2, tip[1], tip[2] + .6), .9, "crane", seg=12)                          # sheave head


def spine_install():
    it = fuel.new_item("OPT_MODX", "Prefab cable spine going in: MOD-EH north along the 34.5 kV collector lanes (modules on bents, "
                       "module 5 on the crane)", (1900, 2004, 900, 1150), (0, 70), basis="typical", register=False, area="I",
                       sheet="typical (prefab cable installation)",
                       info="Elevated LV power / control / fibre spine for the modular-yard expansion, built from 40 ft factory "
                            "modules (frame, three ladder-tray tiers, cable laid and tied, coiled tails). Bents every 20 ft. "
                            "Modules 1-4 set and spliced; module 5 hanging from a truck crane on a spreader bar with tag lines; "
                            "electricians on a boom lift at the splice; bents for module 6 standing.")
    fuel.on(it)
    fuel.D = True
    zb = 11.0
    for k in range(13):                                                                         # bents for modules 1-6
        bent(SY0 + 2 + k * 20)
    for n in range(4):
        y0 = SY0 + n * MOD
        module(SX, y0, zb, tails=(n == 3), tag=tag_lines(n + 1, 9) if n in (0, 3) else None)
        for (zt, _, _), dz in zip(TIERS, (.3, 2.8, 5.3)):                                       # splice plates at the joints
            if n:
                for s in (-1.95, 1.9):
                    box(SX + s - .05, SX + s + .2, y0 - .6, y0 + .6, zb + dz - .05, zb + dz + .55, "steel_dark")
    # drop into MOD-EH: three tier risers down the north wall to a wall entry
    for k, (zt, cab, _) in enumerate(TIERS):
        x = SX - 1.2 + k * 1.2
        box(x - .5, x + .5, 900.1, 901.0, 9.0, zb + .3 + k * 2.5, "pipe")
        box(x - .35, x + .35, 900.2, 900.8, 9.0, zb + .3 + k * 2.5, cab)
    box(SX - 2.4, SX + 2.4, 900.0, 900.4, 7.6, 9.4, "steel_dark")                               # wall entry seal frame
    for (zt, cab, _), dz in zip(TIERS, (.3, 2.8, 5.3)):                                       # stubs from the risers to module 1
        box(SX - 1.9, SX + 1.9, 901.0, SY0, zb + dz, zb + dz + .5, "pipe")
        box(SX - 1.7, SX + 1.6, 901.0, SY0, zb + dz + .08, zb + dz + .38, cab)
    # module 5 on the crane, 6 ft above its seat, square to the line
    y5 = SY0 + 4 * MOD
    zh = zb + 6.0
    module(SX, y5 + .4, zh, tag=tag_lines(5, 9))
    sp_z = zh + 6.6 + 9.0
    box(SX - .4, SX + .4, y5 + 2, y5 + MOD - 1.6, sp_z - .5, sp_z, "sp_yellow")                 # spreader bar
    hook = (SX, y5 + MOD / 2 + .2, sp_z + 9.0)
    for ya in (y5 + 2.5, y5 + MOD - 2):
        rod((SX, ya, sp_z), hook, .06, "rope", seg=6)                                             # top slings
        for s in (-HW + .2, HW - .2):
            rod((SX, ya, sp_z - .5), (SX + s, ya, zh + 6.6), .05, "rope", seg=6)                  # module slings
    box(hook[0] - .6, hook[0] + .6, hook[1] - .6, hook[1] + .6, hook[2] - .4, hook[2] + 1.6, "sp_yellow")  # hook block
    tip = (SX - 2, hook[1], hook[2] + 26)
    rod((hook[0], hook[1], hook[2] + 1.6), tip, .04, "steel", seg=4)                             # hoist line
    crane(1922, 1066, tip)
    for (ya, px, py) in ((y5 + 1, 1966, y5 - 2), (y5 + MOD - 1, 1988, y5 + MOD + 4)):            # tag lines to riggers
        rod((SX, ya, zh), (px, py, 3.6), .03, "rope", seg=4)
        person(px, py, 0, math.atan2(ya - py, SX - px), vest="hivis_o")
    # boom lift at the module 4/5 splice with two electricians
    bx, by = 1975.0, y5 - 3                                                     # clear of AX-1's pad (x 1981)
    box(bx - 3, bx + 3, by - 4, by + 4, .5, 2.6, "crane")
    for s in (-1, 1):
        rod((bx + 2.4, by + s * 3.2, 1.1), (bx + 2.6, by + s * 3.2 - .5, 1.1), 1.1, "tyre", seg=12)
        rod((bx - 2.4, by + s * 3.2, 1.1), (bx - 2.6, by + s * 3.2 - .5, 1.1), 1.1, "tyre", seg=12)
    rod((bx, by, 2.6), (SX + 3.6, by + 2.0, zb + 2.5), .45, "crane", seg=10)
    box(SX + 2.8, SX + 6.8, by + .5, by + 4.5, zb + 2.5, zb + 2.7, "grating")
    for (a0, a1, b0, b1) in ((SX + 2.8, SX + 6.8, by + .5, by + .6), (SX + 2.8, SX + 6.8, by + 4.4, by + 4.5),
                             (SX + 6.7, SX + 6.8, by + .5, by + 4.5)):
        box(a0, a1, b0, b1, zb + 6.0, zb + 6.15, "crane")
    person(SX + 4.0, by + 1.8, zb + 2.7, math.pi, vest="hivis_o")
    person(SX + 5.3, by + 3.4, zb + 2.7, 2.7)
    person(1950, 1000, 0, .4, hat="sign")                                                     # lift supervisor
    fuel.D = False


# ------------------------------------------------------------------------------- staging bay
def dunnage(x0, x1, y, w=6.0, n=4):
    for k in range(n):
        xx = x0 + 1 + k * (x1 - x0 - 2) / (n - 1)
        box(xx - .5, xx + .5, y - w / 2, y + w / 2, 0, .6, "timber")


def mv_crate(x, y):
    """Pre-terminated MV assembly: reel in an open crate, cut-to-length conductors with factory terminations."""
    box(x - 3.5, x + 3.5, y - 2.5, y + 2.5, 0, .5, "timber")
    for s in (-1, 1):
        box(x - 3.5, x + 3.5, y + s * 2.5 - .25, y + s * 2.5, .5, 3.2, "timber")
    rod((x - 2.2, y, 3.4), (x + 2.2, y, 3.4), 2.6, "timber", seg=28)
    rod((x - 1.9, y, 3.4), (x + 1.9, y, 3.4), 2.2, "cable_mv", seg=24)
    for k in range(3):                                                     # three terminated ends, capped
        a = (x + 2.5, y - .8 + k * .8, 1.0)
        rod((x + 1.6, y - .8 + k * .8, 1.6), a, .14, "cable_mv", seg=8)
        rod(a, (a[0] + 1.2, a[1], 1.0), .22, "xlpe", r2=.16, seg=10)        # stress cone / termination body
        for j in range(3):
            rod((a[0] + .3 + j * .3, a[1], 1.0), (a[0] + .4 + j * .3, a[1], 1.0), .32, "insulator", seg=10)  # sheds
        rod((a[0] + 1.2, a[1], 1.0), (a[0] + 1.6, a[1], 1.0), .12, "red", seg=8)   # end cap
    decal((x, y - 2.53, 2.2), (0, -1, 0), 4.0, 1.4, [("PRE-TERMINATED MV", .22, 1, "#111111"),
                                                     ("15 kV 1/C 500 KCMIL  ·  3 x 312 FT", .16, 0, "#222222"),
                                                     ("T-MOD-1 FDR B  ·  TESTED", .16, 0, "#2f7a3c")], bg="#ffffff")


def conduit_rack(x, y, L=20.0):
    for xx in (x + .5, x + L / 2, x + L - .5):
        box(xx - .2, xx + .2, y - 1.5, y + 1.5, .6, 3.0, "steel")
    for r in range(2):
        for k in range(4):
            rod((x, y - 1.05 + k * .7, 1.2 + r * 1.0), (x + L, y - 1.05 + k * .7, 1.2 + r * 1.0), .2,
                ("alu", "pvc_grey")[r], seg=10)
    dunnage(x, x + L, y, 3.4, 3)


def jb_skid(x, y):
    box(x - 2.5, x + 2.5, y - 2, y + 2, 0, .5, "steel")
    box(x - 1.5, x + 1.5, y - .8, y + .8, .5, 5.0, "steel")
    box(x - 1.3, x + 1.3, y - 1.2, y - .8, 2.0, 4.6, "panel")
    for k in range(4):
        rod((x - 1 + k * .65, y - .3, .5), (x - 1 + k * .65, y - .3, 2.0), .1, "alu", seg=8)
    decal((x, y - 1.23, 4.1), (0, -1, 0), 2.0, .6, [("JB-SC1-04  PRE-WIRED", .4, 1, "#111111")], bg="#ffffff")


def flatbed(x0, y, L=48):
    """Flatbed trailer (tractor detached), deck at EL 5."""
    box(x0, x0 + L, y - 4.2, y + 4.2, 4.4, 5.0, "steel_dark")
    box(x0 + 2, x0 + L - 2, y - 1.6, y + 1.6, 3.0, 4.4, "steel")
    for ax in (x0 + 4, x0 + 8.5):
        for s in (-1, 1):
            rod((ax, y + s * 3.0, 1.8), (ax, y + s * 4.2, 1.8), 1.8, "tyre", seg=14)
    for s in (-1, 1):                                                       # landing legs
        rod((x0 + L - 6, y + s * 2.5, 3.0), (x0 + L - 6, y + s * 2.5, 0), .2, "steel", seg=6)
    for k in range(5):                                                      # straps
        xx = x0 + 6 + k * 9
        for sg in (-1, 1):                                                  # ratchet straps over the load
            box(xx - .12, xx + .12, y + sg * 2.62 - .03, y + sg * 2.62 + .03, 5.0, 11.65, "sp_yellow")
        box(xx - .12, xx + .12, y - 2.62, y + 2.62, 11.6, 11.66, "sp_yellow")


def staging_bay():
    it = fuel.new_item("BASE_SERVICES", "Prefab staging bay: cable spine modules on dunnage, pre-terminated MV assemblies, "
                       "prefab conduit racks, pre-wired JB skids", (44, 200, 694, 802), (0, 13), basis="typical",
                       register=False, area="F", sheet="typical (prefab cable installation)",
                       info="Laydown for prefabricated cable systems on the reel / outage pad: spine modules 6-9 on timber "
                            "dunnage with shrink-wrapped tails and sequence tags, one arriving on a flatbed; pre-terminated MV "
                            "assemblies in open crates (factory terminations, tested, capped); prefab multi-conduit racks; "
                            "pre-wired junction-box skids. Kept apart from the reel rows; crane / truck lane along the south edge.")
    fuel.on(it)
    fuel.D = True
    for k, (x0, y) in enumerate(((52, 790), (98, 790), (52, 776))):         # modules on dunnage, along x
        dunnage(x0, x0 + 40, y, 6.0, 5)
        module(y, x0, .6, along="x", tails=True, wrap=True, tag=tag_lines(6 + k, 9))
    flatbed(96, 774, 48)                                                     # module 9 arriving
    module(774, 99, 5.0, along="x", tails=True, wrap=True, tag=tag_lines(9, 9))
    for k, x in enumerate((58, 68, 78)):
        mv_crate(x, 708)
    conduit_rack(92, 706)
    conduit_rack(92, 716)
    jb_skid(122, 705)
    jb_skid(130, 705)
    jb_skid(122, 714)
    decal((46.2, 720, 4.0), (1, 0, 0), 8, 3, [("PREFAB STAGING", .3, 1, "#ffffff"), ("SPINE MODULES  ·  PRE-TERMINATED MV", .14, 0, "#e6e6e6"),
                                             ("CRANE LANE  ·  KEEP CLEAR", .16, 1, "#f2c200")], bg="#22303a")
    for (x, y) in ((45.5, 717.5), (45.5, 722.5)):
        rod((x, y, 0), (x, y, 5.5), .12, "steel", seg=6)
    person(90, 784, 0, .2, vest="hivis_o")                                  # checking a sequence tag
    person(64, 714, 0, -1.2)                                                # QA at the MV crates
    fuel.D = False


def build():
    spine_install()
    staging_bay()
    return 2
