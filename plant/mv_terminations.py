"""MV cable connections at the generators, shown (owner, Oct 22: "curious about how MV connects to the turbine";
both views asked for). Typical, not engineered:
- SC-1 generator line-side terminal box, opened: the cover off and laid on the slab; inside, the 13.8 kV leads come
  through three wall bushings onto copper phase bars, and the 15 MV-105 750 kcmil cables from the ladder tray below
  (5 per phase, as the cable schedule sizes them) rise through the gland plate, each with phase tape, a cold-shrink
  termination with rain sheds, a compression lug bolted to its bar and the shield drain to a ground bus;
- GT1 starting connection: the static starter's output (3 sets x 3 x 750 kcmil 5 kV, cable schedule) leaves SFC-1 on
  a ladder tray to a starting disconnect switch (SDS-1) on a steel stand beside the isolated-phase bus, south of the
  hall; the switch's cable chamber stands open on the 9 cold-shrink terminations; a tap enclosure ties the switch to
  the bus. Closed only while the LCI runs the generator as a motor to start the gas turbine.
Runs late (after the SC-1 terminal box and tray exist, and after the IPB routes are rendered)."""
import fuel
from fuel import box, rod, find, new_item, on

TAPE = ("red", "amber", "cable_inst")                         # phases A / B / C


def termination(xc, yc, z0, z1, ph, ground_y):
    """One 1/C MV cable rising from z0, phase tape, cold-shrink termination with three sheds, lug to z1, shield drain."""
    zt = z0 + .9
    rod((xc, yc, z0), (xc, yc, zt), .08, "cable_mv", seg=10)
    rod((xc, yc, zt - .35), (xc, yc, zt - .15), .09, TAPE[ph], seg=10)               # phase tape
    rod((xc, yc, zt), (xc, yc, zt + 1.3), .11, "hdpe", seg=10)                       # cold-shrink body
    for k in range(3):
        zs = zt + .45 + k * .3
        rod((xc, yc, zs), (xc, yc, zs + .05), .19, "hdpe", seg=12)                   # rain sheds
    rod((xc, yc, zt + 1.3), (xc, yc, z1), .065, "copper", seg=8)                     # compression lug barrel
    rod((xc, yc, zt - .05), (xc, ground_y, z0 + .25), .03, "copper", seg=4)          # shield drain to the ground bus
    return 8


def sc1_terminal_box():
    x = 1910.0
    sc = find("SC-1: aeroderivative")
    keep = []
    for p in fuel.G["parts"]:                                  # the closed box and its three token drops come off
        if p["item"] == sc["id"]:
            if p["kind"] == "box" and p["color"] == "panel" and p["min"][:3] == [x + 8, 1217, 10.4]:
                continue
            if p["kind"] == "rod" and p["color"] == "cable_mv" and p["a"][2] == 10.1 and p["b"][2] == 10.4:
                continue
        keep.append(p)
    fuel.G["parts"][:] = keep
    it = new_item("OPT_MOD", "SC-1 generator terminal box TB-G1 (opened): 13.8 kV cable terminations",
                  [x + 7.5, x + 16.5, 1216.9, 1224], [0, 16.2], area="I", register=False,
                  info="Line-side terminal box opened: three wall bushings onto copper phase bars; 15 x 750 kcmil MV-105 "
                       "(5 per phase) up from the ladder tray with cold-shrink terminations, compression lugs and shield "
                       "drains to the ground bus. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    # the box: back plate on the enclosure wall, sides, top, gland plate; the front cover off, on the slab
    box(x + 8, x + 16, 1217.13, 1217.25, 10.4, 16, "panel")                          # back plate, off the wall joints
    for xs in (x + 8, x + 15.85):
        box(xs, xs + .15, 1217.25, 1219.4, 10.4, 16, "panel")
    box(x + 8.15, x + 15.85, 1217.2, 1219.4, 15.85, 16, "panel")
    box(x + 8.15, x + 15.85, 1217.2, 1219.4, 10.4, 10.55, "steel")                    # gland plate
    box(x + 8.5, x + 15.5, 1224.4, 1227.2, 0, .12, "panel")                          # the cover, on the slab
    n += 6
    # bushings through the wall and the phase bars
    for ph, xp in enumerate((x + 9.6, x + 12.0, x + 14.4)):
        rod((xp, 1217.2, 15.0), (xp, 1217.8, 15.0), .24, "insulator", seg=12)
        for k in range(3):
            rod((xp, 1217.3 + k * .15, 15.0), (xp, 1217.35 + k * .15, 15.0), .34, "insulator", seg=12)
        rod((xp, 1217.75, 15.0), (xp, 1217.75, 13.7), .06, "copper", seg=6)           # strap down to the bar
        box(xp - 1.0, xp + 1.0, 1217.55, 1217.8, 13.3, 13.7, "copper")               # phase bar
        for j in range(5):                                                             # 5 cables per phase
            xc = xp + (j - 2) * .42
            n += termination(xc, 1218.35, 10.55, 13.3, ph, 1219.0)
            rod((xc, 1218.35, 13.3), (xc, 1217.8, 13.45), .05, "copper", seg=6)        # lug palm to the bar
            rod((xc, 1217.8, 13.45), (xc, 1217.5, 13.45), .04, "steel", seg=6)         # bolt
            # up from the tray (cables at x + 10.75 .. 13.25, EL ~8.9) through the gland plate
            xt = x + 10.75 + (ph * 5 + j) * 2.5 / 14
            rod((xt, 1218.35, 9.25), (xc, 1218.35, 10.55), .08, "cable_mv", seg=8)
        n += 6
    box(x + 8.4, x + 15.6, 1218.9, 1219.1, 10.6, 10.8, "copper")                     # ground bus
    rod((x + 15.6, 1219.0, 10.7), (x + 16.4, 1219.7, .3), .05, "copper", seg=6)      # bonded down to the grid
    import showcase
    showcase.decal((x + 12, 1225.8, .14), (0, 0, 1), 6.0, 1.4,
                   [("TB-G1  ·  13.8 kV  ·  GENERATOR LINE SIDE", .26, True, "#111111"),
                    ("3 x 5 x 750 kcmil MV-105  ·  COLD-SHRINK TERMINATIONS", .18, False, "#222222")], bg="#ffffff",
                   up=(0, 1, 0))
    showcase.decal((x + 16.08, 1218.3, 14.6), (1, 0, 0), 1.8, .9, [("DANGER", .4, True, "#ffffff"),
                   ("13,800 V", .32, True, "#ffffff")], bg="#b3261e")
    fuel.D = False
    return n


def gt1_starting_connection():
    it = new_item("BASE_ELECTRICAL", "SDS-1: GT1 starting disconnect at the IPB, LCI output cables and terminations",
                  [641.4, 697, 381, 393.5], [0, 26], area="A", register=False,
                  info="Starting disconnect switch beside the GT1 isolated-phase bus: the LCI (SFC-1) output, 3 sets x 3 x "
                       "750 kcmil 5 kV, on a ladder tray from the starter, terminated in the switch's cable chamber; a tap "
                       "enclosure to the bus. Closed only for the start. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    X0, X1, Y0, Y1, Z0, Z1 = 643.0, 649.0, 383.0, 389.0, 19.0, 25.5
    for (lx, ly) in ((X0 + .4, Y0 + .4), (X1 - .4, Y0 + .4), (X0 + .4, Y1 - .4), (X1 - .4, Y1 - .4)):
        box(lx - .9, lx + .9, ly - .9, ly + .9, 0, .5, "concrete")
        box(lx - .25, lx + .25, ly - .25, ly + .25, .5, Z0, "steel")                  # stand legs
    box(X0 - .3, X1 + .3, Y0 - .3, Y1 + .3, Z0 - .4, Z0, "grating")                  # platform under the switch
    # switch housing (upper, closed) and cable chamber (lower, door open toward the south)
    box(X0, X1, Y0, Y1, Z0 + 2.6, Z1, "ipb")
    box(X0, X1, Y1 - .15, Y1, Z0, Z0 + 2.6, "ipb")
    for xs in (X0, X1 - .15):
        box(xs, xs + .15, Y0, Y1, Z0, Z0 + 2.6, "ipb")
    box(X0 - 2.6, X0 - 2.45, Y0 - 2.6, Y0, Z0, Z0 + 2.4, "ipb")                       # the open door, swung west
    box(X0 + 1.2, X0 + 2.2, Y0 - .1, Y0, Z0 + 3.4, Z0 + 4.2, "glass")                 # viewing window on the blades
    rod((X1, Y0 + 1.5, Z0 + 4.8), (X1 + .9, Y0 + 1.5, Z0 + 4.8), .12, "red", seg=8)     # operating handle
    n += 14
    # tap enclosure to the bus (the C-phase line at x 640.2, EL 22)
    box(641.2, X0, 389.2, 392.6, 20.6, 23.4, "ipb")
    # inside the chamber: three phase bars, 9 terminations (3 per phase) up from the gland plate
    box(X0 + .15, X1 - .15, Y0, Y1 - .15, Z0, Z0 + .15, "steel")                      # gland plate
    for ph, xp in enumerate((X0 + 1.5, X0 + 3.0, X0 + 4.5)):
        box(xp - .45, xp + .45, Y1 - .6, Y1 - .4, Z0 + 2.0, Z0 + 2.3, "copper")
        for j in range(3):
            xc = xp + (j - 1) * .38
            n += termination(xc, Y1 - 1.2, Z0 + .15, Z0 + 2.0, ph, Y1 - 1.8)
            rod((xc, Y1 - 1.2, Z0 + 2.0), (xc, Y1 - .6, Z0 + 2.15), .045, "copper", seg=6)
    box(X0 + .3, X1 - .3, Y1 - 1.9, Y1 - 1.7, Z0 + .2, Z0 + .35, "copper")            # ground bus
    box(X0 + 1.0, X1 - 1.0, Y0 + .6, Y0 + 1.0, Z0 + 2.45, Z0 + 2.6, "lamp")           # chamber light
    # ladder tray from SFC-1 (west face x 696, EL ~8) to under the switch, then the cables rise into the chamber
    ZT, YT = 13.0, 388.0                                # north of the EL 42 tray posts at y 384-386
    for s in (-1, 1):
        box(646.0, 696.0, YT + s * 1.25 - .06, YT + s * 1.25 + .06, ZT - .35, ZT + .15, "pipe")
    for k in range(51):
        box(646.0 + k - .05, 646.0 + k + .05, YT - 1.25, YT + 1.25, ZT - .3, ZT - .22, "pipe")
    for xs in (660.0, 670.0, 680.0, 692.0):                                            # supports
        box(xs - .3, xs + .3, YT - .3, YT + .3, 0, ZT - .4, "steel")
        box(xs - .3, xs + .3, YT - 1.5, YT + 1.5, ZT - .6, ZT - .35, "steel")
        box(xs - .8, xs + .8, YT - .8, YT + .8, 0, .4, "concrete")
    cx = [X0 + 1.5 + (ph * 1.5) + (j - 1) * .38 for ph in range(3) for j in range(3)]
    for i, xc in enumerate(cx):
        yy = YT - 1.0 + i * .25
        rod((696.0, yy, ZT - .1), (647.5, yy, ZT - .1), .08, "cable_mv", seg=8)        # 9 cables along the tray
        rod((647.5, yy, ZT - .1), (xc, Y1 - 1.2, Z0 - .4), .08, "cable_mv", seg=8)     # rise to the chamber
        rod((xc, Y1 - 1.2, Z0 - .4), (xc, Y1 - 1.2, Z0 + .15), .08, "cable_mv", seg=8)
    rod((696.0, YT, ZT - .1), (697.0, YT, ZT - .1), .3, "steel", seg=8)                # gland at the LCI wall
    n += 70
    import showcase
    showcase.decal((X0 + 3.0, Y0 - .03, Z0 + 5.4), (0, -1, 0), 4.4, 1.1,
                   [("SDS-1  ·  STARTING DISCONNECT", .3, True, "#111111"),
                    ("GT1 LCI  ·  3 x 3 x 750 kcmil 5 kV", .22, False, "#222222")], bg="#ffffff")
    showcase.decal((680.0, YT - 1.3, ZT - .1), (0, -1, 0), 3.4, .45, [("LCI-1 OUTPUT  ·  SFC-1 → SDS-1", .6, True, None)],
                   bg="#ffd200")
    fuel.D = False
    return n


def moment():
    """Cable moment at SC-1 (owner, Oct 22: "make a wire cable moment"): the 13.8 kV generator leads being terminated.
    Two electricians on a scissor lift at the opened terminal box with the cold-shrink kits; the last set of
    750 kcmil MV-105 paying off a reel on an RR-SW30 reel roller, up over a sheave into the ladder tray (the tray
    cables carry their printed jacket legends, modular_lod3); a VLF test cart standing by for the withstand test;
    a sign telling the story. Typical, not engineered."""
    import cable_moments as cm
    import simpull
    import showcase
    x = 1910.0
    it = new_item("OPT_MOD", "Cable moment: SC-1 13.8 kV generator leads (terminating, the last set off the reel)",
                  [x - 3, x + 20, 1219, 1244], [0, 14], area="I", register=False,
                  info="Electricians terminating the 15 x 750 kcmil MV-105 generator leads in TB-G1 with cold-shrink kits; "
                       "the last set off a reel on an RR-SW30 reel roller over a sheave into the tray; VLF test cart "
                       "ready for the withstand test. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    cm.scissor_lift(x + 2.6, x + 9.6, 1219.9, 1223.4, 0, 8.4)                          # at the opened box
    cm.person(x + 6.4, 1220.9, 8.4, a=-1.5708)
    cm.person(x + 8.8, 1221.3, 8.4, a=-1.5708, vest="hivis_o")
    for (bx, by) in ((x + 3.0, 1222.3), (x + 4.5, 1222.3)):                          # termination kits
        box(bx, bx + 1.2, by, by + .8, 8.4, 9.1, "timber")
    rod((x + 5.9, 1222.6, 8.4), (x + 5.9, 1222.6, 9.2), .25, "sp_yellow", seg=10)      # cable-prep tool bag
    n += 6
    # the last set off the reel: RR-SW30 roller, reel of 750 kcmil MV-105, payoff over a sheave into the tray
    simpull.reel_roller(x + 2.0, 1236.5, cap=30, reel_D=6.0, reel_W=3.6, cable="cable_mv",
                        label="MV-105 15 kV 750 KCMIL CU EPR")
    cm.sheave(x + 10.2, 1236.5, 10.4, axis="x", r=.8)
    rod((x + 2.0, 1236.5, 7.0), (x + 7.0, 1236.5, 9.8), .08, "cable_mv", seg=8)
    rod((x + 7.0, 1236.5, 9.8), (x + 10.2, 1236.5, 11.2), .08, "cable_mv", seg=8)
    rod((x + 10.2, 1236.5, 11.2), (x + 11.4, 1236.5, 9.3), .08, "cable_mv", seg=8)
    cm.person(x + 5.5, 1239.0, 0, a=0.0)                                                # reel tender
    n += 6
    # VLF test cart, leads coiled on it, ready for the withstand test after termination
    tx, ty = x + 17.0, 1226.0
    for (wx, wy) in ((tx - .8, ty - .7), (tx + .8, ty - .7), (tx - .8, ty + .7), (tx + .8, ty + .7)):
        rod((wx, wy - .1, .3), (wx, wy + .1, .3), .3, "tyre", seg=10)
    box(tx - 1.1, tx + 1.1, ty - 1.0, ty + 1.0, .5, 2.8, "panel")
    box(tx - .9, tx + .3, ty - .8, ty + .8, 2.8, 3.8, "machine")
    rod((tx + .7, ty, 3.0), (tx + .7, ty, 3.4), .45, "red", seg=12)                    # test lead coil
    showcase.decal((tx - .3, ty - 1.03, 3.3), (0, -1, 0), 1.2, .55, [("VLF 0.1 Hz", .4, True, "#7CFC9A"),
                   ("READY", .3, False, "#ffffff")], bg="#16181a")
    n += 8
    showcase.decal((x - 2.4, 1230.5, 5.0), (-1, 0, 0), 6.4, 2.4,
                   [("SC-1 GENERATOR LEADS  ·  13.8 kV", .2, True, "#111111"),
                    ("15 x 750 kcmil MV-105  ·  5 PER PHASE", .15, False, "#222222"),
                    ("TERMINATE  ·  VLF TEST  ·  ENERGIZE", .15, True, "#b5651d"),
                    ("SOUTHWIRE MV-105 · SIMpull REEL", .12, False, "#444444")], bg="#ffffff")
    fuel.D = False
    return n


def build():
    return sc1_terminal_box() + gt1_starting_connection() + moment()
