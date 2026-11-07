"""RICE engine hall interior electrical at LOD 3 (owner, Oct 22: "audit the electrical equipment and wire and cable
at the RICE engine and turbine hall; model it better, it's too rough"). The audit found the hall with engines and
generators but no electrical inside: generator terminal boxes with nothing connected, the MV bridge stopping at the
east wall, no engine control, no lighting. Added, as in a medium-speed engine hall, all typical, not engineered:
- MV: each generator's leads (2 sets x 3 x 500 kcmil MV-105, ~870 A at 13.8 kV) rise from the line-side terminal box
  to a 24 in ladder tray over the generator line at EL 20, along the hall to the east end, down to EL 12 and out
  through the wall onto the existing bridge to the PCM; tray hung from the roof steel, labelled;
- control: a parallel control tray (instrument, thermocouple, control, fibre) with a conduit pair down to an engine
  control panel (UNIC-type cabinet: HMI, lamps, E-stop) beside each engine; three engine junction boxes on each
  block's east face with their harness along the base frame to the panel;
- hall services: LED high-bays in three rows on MC branch runs from a lighting panel on the north wall, 480 V
  welding receptacles on the north columns, fire-alarm horn-strobes, roof gas detectors (methane) on their loop.
Everything inside the hall envelope, clear of the engines, generators, crane and columns."""
import fuel
from fuel import box, rod, new_item, on

ENG = [1581 + 28 * k for k in range(8)]
YM, YC, ZT = 1112.0, 1116.6, 20.0               # MV tray / control tray centre lines, tray EL
CRANE_X = (1686.0, 1694.0)                      # bridge crane parked here: no hangers through it


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def ladder(x0, x1, yc, z, w, cables, step=2.0):
    """Ladder tray along x with cables laid in it."""
    n = 0
    for s in (-1, 1):
        box(x0, x1, yc + s * w / 2 - .06, yc + s * w / 2 + .06, z - .35, z + .15, "pipe")
    x = x0 + .5
    while x < x1:
        box(x - .05, x + .05, yc - w / 2, yc + w / 2, z - .3, z - .22, "pipe")
        x += step
        n += 1
    for j, (c, r) in enumerate(cables):
        off = -w / 2 + .2 + j * (w - .4) / max(1, len(cables) - 1)
        rod((x0, yc + off, z - .22 + r), (x1, yc + off, z - .22 + r), r, c, seg=6)
    return n + 2 + len(cables)


def build():
    it = new_item("OPT_MOD", "RICE engine hall interior electrical: MV and control trays, engine panels, lighting, FA",
                  [1572, 1810, 1044, 1129], [0, 34], area="I", register=False,
                  info="Generator leads from the terminal boxes to an EL 20 MV ladder tray and out to the PCM bridge; control "
                       "tray with drops to an engine control panel per engine; engine JBs and harness; LED high-bays on MC, "
                       "welding receptacles, horn-strobes, gas detectors. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    MV = tuple(("cable_mv", .1) for _ in range(8))
    CT = (("cable_inst", .07), ("cable_tcx", .07), ("cable_tc", .07), ("cable_fo", .06))
    # ---- MV tray over the generators, east-end drop to the wall at the bridge (y 1110.4-1113.6, EL 12)
    n += ladder(1584.0, 1806.0, YM, ZT, 2.0, MV)
    for s in (-1, 1):                                                               # drop: two side rails down
        box(1806.0 - .06, 1806.0 + .06, YM + s - .06, YM + s + .06, 12.2, ZT + .15, "pipe")
        box(1806.0, 1810.0, YM + s - .06, YM + s + .06, 11.85, 12.35, "pipe")       # short run to the wall
    for j in range(8):
        yy = YM - .8 + j * .23
        rod((1806.0, yy, ZT - .1), (1806.6, yy, ZT - .1), .1, "cable_mv", seg=6)
        rod((1806.6, yy, ZT - .1), (1806.6, yy, 12.1), .1, "cable_mv", seg=6)
        rod((1806.6, yy, 12.1), (1810.0, yy, 12.1), .1, "cable_mv", seg=6)
    box(1809.4, 1810.0, YM - 1.6, YM + 1.6, 11.2, 13.2, "steel")                    # wall sleeve / fire seal
    n += 30
    # ---- control tray beside it
    n += ladder(1584.0, 1806.0, YC, ZT, 1.4, CT)
    # hangers from the roof steel (EL 33.8), clear of the parked crane
    for x in range(1590, 1806, 10):
        if CRANE_X[0] - 1 < x < CRANE_X[1] + 1:
            continue
        for y in (YM - 1.3, YC + .9):
            rod((x, y, ZT + .15), (x, y, 33.8), .05, "steel", seg=4)
        box(x - .1, x + .1, YM - 1.3, YC + .9, ZT - .5, ZT - .35, "steel")          # trapeze
        n += 3
    for x in (1640.0, 1750.0):
        decal((x, YM - 1.08, ZT - .1), (0, -1, 0), 3.0, .45, [("RE-MV1  ·  13.8 kV", .65, True, None)], bg="#ffd200")
        decal((x, YC + .78, ZT - .1), (0, 1, 0), 3.0, .45, [("RE-C1  ·  CONTROL", .65, True, None)], bg="#ffd200")
    # ---- per engine
    for k, x in enumerate(ENG):
        xc = x + 9.5
        # generator leads: 6 cables out of the terminal-box top (x + 15.5 .. 18.5, y 1100-1107, EL 15.5) up to the tray
        for j in range(6):
            xx, yy = x + 16.8 + (j % 3) * .7, 1101.5 + (j // 3) * 3.0          # east of the generator body
            rod((xx, yy, 15.5), (xx, yy, 16.4), .1, "cable_mv", seg=6)
            rod((xx, yy, 16.4), (x + 16.8 + j * .25, YM - .5, ZT - .1), .1, "cable_mv", seg=6)
        box(x + 15.7, x + 18.3, 1100.3, 1106.7, 15.5, 15.75, "steel")               # gland plate on the box top
        n += 13
        # engine control panel in the gap east of the engine, north end
        px0, px1, py0, py1 = x + 20.0, x + 23.0, 1116.2, 1118.6
        box(px0, px1, py0, py1, 0, .4, "concrete")
        box(px0 + .1, px1 - .1, py0 + .1, py1 - .1, .4, 7.6, "cabinet")
        box(px0 + .3, px1 - .3, py0 + .05, py0 + .1, 1.0, 7.2, "door")              # door on the south face
        box(px0 + .9, px1 - .9, py0, py0 + .05, 5.4, 6.4, "hmi")                    # HMI
        for j, c in enumerate(("led_g", "led_a", "led_r")):
            box(px0 + .7 + j * .35, px0 + .9 + j * .35, py0 - .02, py0 + .05, 4.9, 5.1, c)
        rod((px1 - .7, py0, 4.4), (px1 - .7, py0 - .2, 4.4), .16, "red", seg=10)    # E-stop
        decal((x + 21.5, py0 - .03, 6.95), (0, -1, 0), 1.9, .38, [(f"ENGINE {k + 1}  LCP", .6, True, "#111111")],
              bg="#ffffff")
        for dx in (-.4, .4):                                                        # conduit pair up to the control tray
            rod((x + 21.5 + dx, 1117.4, 7.6), (x + 21.5 + dx, 1117.4, ZT - .35), .1, "alu", seg=8)
        n += 11
        # engine JBs on the block's east face (x + 15) and the harness along the base frame to the panel
        for yj in (1068.0, 1080.0, 1090.0):
            box(x + 15.0, x + 15.5, yj - .8, yj + .8, 7.5, 9.5, "panel")
            rod((x + 15.5, yj, 8.0), (x + 16.0, yj, 8.0), .07, "cable_inst", seg=6)
            rod((x + 16.0, yj, 8.0), (x + 16.0, yj, 4.7), .07, "cable_inst", seg=6)
            n += 3
        rod((x + 16.0, 1068.0, 4.7), (x + 16.0, 1113.5, 4.7), .1, "cable_inst", seg=6)
        rod((x + 16.0, 1113.5, 4.7), (x + 21.5, 1113.5, 4.7), .1, "cable_inst", seg=6)
        rod((x + 21.5, 1113.5, 4.7), (x + 21.5, py0, 4.7), .1, "cable_inst", seg=6)
        for yc in range(1070, 1113, 4):                                            # harness clips on the base frame
            box(x + 15.8, x + 16.2, yc - .05, yc + .05, 4.5, 4.9, "steel")
        n += 14
    # ---- lighting: three rows of LED high-bays at EL 27 (under the crane girders), MC branch runs, panel LP-RE
    import swgr_rooms
    for yr in (1062.0, 1092.0, 1121.0):
        for x in range(1594, 1806, 28):
            swgr_rooms.fixture(float(x), yr, 27.0, along="x", roof=33.8)
            n += 4
        rod((1590.0, yr + .9, 27.15), (1800.0, yr + .9, 27.15), .05, "cable_mc", seg=4)
        rod((1590.0, yr + .9, 27.15), (1590.0, yr + .9, 27.15) if yr == 1121.0 else (1590.0, 1121.9, 27.15), .05,
            "cable_mc", seg=4)
    box(1593.0, 1597.0, 1128.9, 1129.8, 5.0, 10.5, "panel")                        # lighting panel LP-RE
    rod((1595.0, 1129.3, 10.5), (1595.0, 1129.3, 27.15), .06, "cable_mc", seg=4)
    rod((1595.0, 1129.3, 27.15), (1595.0, 1121.9, 27.15), .06, "cable_mc", seg=4)
    decal((1595.0, 1128.85, 9.9), (0, -1, 0), 3.0, .5, [("LP-RE  ·  480/277 V", .6, True, "#111111")], bg="#ffffff")
    n += 5
    # ---- north columns: welding receptacles; horn-strobes on alternate columns, both walls; roof gas detectors
    for i, xcol in enumerate(range(1608, 1806, 28)):
        box(xcol - .8, xcol + .8, 1125.9, 1126.5, 4.0, 5.6, "panel")                 # 480 V welding receptacle
        rod((xcol, 1126.2, 5.6), (xcol, 1126.2, ZT - .4), .06, "cable_mc", seg=4)
        rod((xcol, 1126.2, ZT - .4), (xcol, YC + .7, ZT - .4), .06, "cable_mc", seg=4)
        if i % 2 == 0:
            for (yy, s) in ((1126.5 - .7, 1), (1043.5 + .4, -1)):
                box(xcol - .3, xcol + .3, yy - .2, yy + .2, 10.0, 10.8, "red")       # horn-strobe
                rod((xcol, yy, 10.8), (xcol, yy, 12.5), .03, "cable_fa", seg=4)
        n += 4
    for x in range(1600, 1806, 40):
        box(x - .3, x + .3, 1084.7, 1085.3, 32.4, 33.2, "amber")                   # methane detector at the ridge
        rod((x, 1085.0, 33.2), (x, 1085.0, 33.8), .03, "cable_fa", seg=4)
        n += 2
    rod((1600.0, 1085.0, 33.6), (1800.0, 1085.0, 33.6), .04, "cable_fa", seg=4)     # gas-detection loop
    fuel.D = False
    return n
