"""R2A unit / HRSG e-house at LOD 3, inside and out (boiler slide 4, Oct 22: "show the wires inside the room, all of
them"). The e-house was a solid block; it becomes a shell (four walls, floor, roof, west and south walls on their own
layer R2A_ROOF so a cutaway can lift them) with the lineups and every cable leg of the HRSG 1 train the schedule carries:

- 13.8 kV primary: the three MV-105 cables from SWGR-13.8-1 drop off the EL 36 MV tray into the T-R2A air terminal
  chamber;
- 480 V secondary: 10 sets of 4 x 1/C 500 kcmil out of the T-R2A LV cable box, up a ladder, across to the north wall
  and over the room to the LC-R2A main breaker (A-P-0422);
- inside: LC-R2A 480 V switchgear and MCC-R2A-1 on the east wall, MCC-R2A-2 and the VFD lineup back to back with the
  DCS controller / marshalling cabinets in the middle, UPS, 125 V DC battery rack and the AC / DC / lighting panels on
  the west wall, a fire-alarm / F&G panel; ladder trays over each lineup (power, control, instrumentation) with the
  cable drops into every section;
- out to the field: the 600 V power riser up the north wall to the EL 30 LV tray, the control / instrument / fibre
  riser through the roof to the EL 42 control tray (both towards HRSG 1, the feed pumps, SCR, CEMS, chemical feed and
  the duct burner);
- building wire in conduit to the LED fixtures and receptacles, the fire-alarm loop to the ceiling detectors, ground
  bus, mats, nameplates and arc-flash labels, extinguishers, exit signs and a technician.
Typical, not engineered; the drawn footprint and the sheet-13 height (14 ft) are kept.
"""
import fuel
from fuel import box, rod
import swgr_rooms as sw

X0, X1, Y0, Y1 = 552.0, 584.0, 612.0, 652.0
IX0, IX1, IY0, IY1 = X0 + .6, X1 - .6, Y0 + .6, Y1 - .6        # inside face of the walls
Z, ZC = 2.5, 13.4                                               # floor, ceiling


def ladder(x0, x1, y0, y1, z, along, fill=(), rung=2.0, h=.4):
    """Ladder tray: side rails, rungs every `rung` ft, cables lying in it (colour, radius) spread across the width."""
    if along == "y":
        for x in (x0, x1 - .08):
            box(x, x + .08, y0, y1, z, z + h, "pipe")
        y = y0 + rung / 2
        while y < y1:
            box(x0, x1, y - .05, y + .05, z, z + .07, "pipe")
            y += rung
        for k, (c, r) in enumerate(fill):
            x = x0 + .2 + (x1 - x0 - .4) * (k + .5) / len(fill)
            rod((x, y0, z + .07 + r), (x, y1, z + .07 + r), r, c, seg=6)
    else:
        for y in (y0, y1 - .08):
            box(x0, x1, y, y + .08, z, z + h, "pipe")
        x = x0 + rung / 2
        while x < x1:
            box(x - .05, x + .05, y0, y1, z, z + .07, "pipe")
            x += rung
        for k, (c, r) in enumerate(fill):
            y = y0 + .2 + (y1 - y0 - .4) * (k + .5) / len(fill)
            rod((x0, y, z + .07 + r), (x1, y, z + .07 + r), r, c, seg=6)


def hangers(x0, x1, pts, z, along="y"):
    """Trapeze hangers: threaded rods from the ceiling and a strut under the tray."""
    for u in pts:
        if along == "y":
            box(x0 - .1, x1 + .1, u - .06, u + .06, z - .12, z, "steel")
            for x in (x0 - .05, x1 + .05):
                rod((x, u, z - .12), (x, u, ZC), .025, "steel", seg=4)
        else:
            box(u - .06, u + .06, x0 - .1, x1 + .1, z - .12, z, "steel")
            for y in (x0 - .05, x1 + .05):
                rod((u, y, z - .12), (u, y, ZC), .025, "steel", seg=4)


def drop(x, y0, y1, zt, zb, cols, r=.09, axis="y"):
    """A row of cables leaving a tray and dropping into a section top (spaced along `axis`)."""
    n = len(cols)
    for k, c in enumerate(cols):
        u = y0 + (y1 - y0) * (k + .5) / n
        a, b = ((x, u, zt), (x, u, zb)) if axis == "y" else ((u, x, zt), (u, x, zb))
        rod(a, b, r, c, seg=6)
    if axis == "y":
        box(x - .25, x + .25, y0, y1, zb, zb + .06, "steel_dark")          # gland plate on the section roof
    else:
        box(y0, y1, x - .25, x + .25, zb, zb + .06, "steel_dark")


def shell(it):
    """Replace the solid body with walls; move the roof (and what stands on it) to R2A_ROOF."""
    G = fuel.G
    G["parts"][:] = [p for p in G["parts"] if not (p["item"] == it["id"] and p["color"] == "ehouse" and not p.get("d"))]
    for p in G["parts"]:
        if p["item"] == it["id"] and p["kind"] == "box" and p["min"][2] >= ZC - .05:
            p["layer"] = "R2A_ROOF"
        elif p["item"] == it["id"] and p["kind"] == "rod" and min(p["a"][2], p["b"][2]) >= ZC - .05:
            p["layer"] = "R2A_ROOF"
    fuel.on(it)
    fuel.D = False
    zt = ZC
    box(X0 + .3, X1 - .3, Y0 + .3, IY0, Z, zt, "ehouse", layer="R2A_ROOF")   # south wall (lifts with the roof)
    box(X0 + .3, X1 - .3, IY1, Y1 - .3, Z, zt, "ehouse")                  # north wall
    box(X0 + .3, IX0, IY0, IY1, Z, zt, "ehouse", layer="R2A_ROOF")        # west wall (doors; lifts with the roof)
    box(IX1, X1 - .3, IY0, IY1, Z, zt, "ehouse")                          # east wall
    fuel.D = True


def split_plant_trays(region=(562.0, 640.0, 640.0, 760.0)):
    """Move the plant tray / riser parts around R2A into their own item ("R2A interconnection trays ...") so a cutaway can
    hide the overhead rack yet keep the trays that connect the e-house to the plant: the roof-gland riser and the EL 42
    control tray to the HRSG, the north-wall riser and the EL 30 LV tray, the EL 36 MV tray down to T-R2A. Box parts and
    axis-aligned rods that cross the region edge are cut in two at the edge."""
    import copy
    G = fuel.G
    tray = next(i for i in G["items"] if i["name"].startswith("Cable trays"))
    x0, x1, y0, y1 = region
    new = fuel.new_item("ROUTES_BASE", "R2A interconnection trays: risers and drops between the e-house and the plant trays",
                        (x0, x1, y0, y1), (0, 50), area="A", register=False,
                        info="The plant tray parts around R2A (cut from the tray system for the cutaway views).")
    keep, moved = [], 0

    def inside(lo, hi):
        return lo[0] >= x0 and hi[0] <= x1 and lo[1] >= y0 and hi[1] <= y1

    for p in G["parts"]:
        if p["item"] != tray["id"]:
            keep.append(p)
            continue
        if p["kind"] == "box":
            lo, hi = p["min"], p["max"]
        elif p["kind"] == "rod":
            lo = [min(p["a"][i], p["b"][i]) for i in range(3)]
            hi = [max(p["a"][i], p["b"][i]) for i in range(3)]
        else:
            keep.append(p)
            continue
        if hi[0] < x0 or lo[0] > x1 or hi[1] < y0 or lo[1] > y1:
            keep.append(p)
            continue
        if inside(lo, hi):
            p["item"] = new["id"]
            keep.append(p)
            moved += 1
            continue
        # crosses the edge: split along the one axis it runs on (boxes: the long axis; rods: axis-aligned only)
        if p["kind"] == "rod":
            ax = [i for i in range(3) if p["a"][i] != p["b"][i]]
            if len(ax) != 1 or ax[0] == 2:
                keep.append(p)
                continue
            ax = ax[0]
        else:
            ax = 0 if (hi[0] - lo[0]) >= (hi[1] - lo[1]) else 1
            other = 1 - ax
            if lo[other] < (x0, y0)[other] or hi[other] > (x1, y1)[other]:
                keep.append(p)
                continue
        a_lo, a_hi = (x0, x1) if ax == 0 else (y0, y1)
        cuts = sorted({lo[ax], hi[ax], *(c for c in (a_lo, a_hi) if lo[ax] < c < hi[ax])})
        for c0, c1 in zip(cuts, cuts[1:]):
            q = copy.deepcopy(p)
            if q["kind"] == "box":
                q["min"][ax], q["max"][ax] = round(c0, 2), round(c1, 2)
            else:
                s0 = q["a"][ax] <= q["b"][ax]
                q["a"][ax], q["b"][ax] = (round(c0, 2), round(c1, 2)) if s0 else (round(c1, 2), round(c0, 2))
            mid = (c0 + c1) / 2
            if a_lo <= mid <= a_hi:
                q["item"] = new["id"]
                moved += 1
            keep.append(q)
    G["parts"][:] = keep
    return moved


def build():
    G = fuel.G
    it = next(i for i in G["items"] if i["tag"] == "R2A")
    n0 = len(G["parts"])
    shell(it)
    split_plant_trays()
    room = fuel.new_item("BASE_ELECTRICAL", "R2A e-house interior: 480 V switchgear, MCCs, VFDs, DCS marshalling, UPS / DC, "
                         "trays and cable drops", (IX0, IX1, IY0, IY1), (Z, ZC), area="A", sheet="SW-3X1-03",
                         register=False,
                         info="Unit / HRSG 1 e-house fit-out, typical: LC-R2A 480 V switchgear fed from T-R2A (10 sets 4 x 1/C "
                              "500 kcmil), MCC-R2A-1 / -2 and the VFD lineup for the SCR blowers, chemical-feed and "
                              "blowdown pumps, HRSG MOVs and heaters; DCS controllers and marshalling for the HRSG, feed-"
                              "pump, CEMS and duct-burner I/O; 10 kVA UPS, 125 V DC battery and panels; ladder trays over "
                              "every lineup with the drops into each section; power riser to the EL 30 tray, control / "
                              "instrument / fibre riser to the EL 42 tray.")
    fuel.on(room)
    fuel.D = True
    box(IX0, IX1, IY0, IY1, Z, Z + .02, "epoxy")
    zt = 10.1                                                             # lineup tops

    # ---- east wall: MCC-R2A-1 (south) and LC-R2A 480 V switchgear (north, main breaker at the north end)
    fm = (581.2, 583.3, 613.4, 629.4)
    box(*fm, Z, zt, "cab_in")
    F = sw.Front(fm, "-x")
    sw.mcc(F, Z, zt, "cab_in")
    sw.nameplate(F, F.L / 2, zt - .3, "MCC-R2A-1", "480 V  ·  800 A  ·  65 kA  ·  HRSG 1 MOVs, HEATERS")
    sw.arc_label(F, 1.0, Z + 5.2, "480 V", 8.0)
    sw.mat(F, Z)
    fl = (578.4, 583.3, 630.2, 650.6)
    box(*fl, Z, zt, "swgr_in")
    F = sw.Front(fl, "-x")
    sw.lv_swgr(F, Z, zt, "swgr_in")
    sw.nameplate(F, F.L / 2, zt - .25, "LC-R2A", "480 V  ·  4000 A MAIN  ·  65 kA  ·  FED FROM T-R2A")
    sw.arc_label(F, 1.2, Z + 6.6, "480 V", 24.6)
    sw.mat(F, Z)

    # ---- island: MCC-R2A-2 + VFDs (front east) back to back with the DCS / marshalling cabinets (front west)
    fi = (568.2, 571.2, 614.4, 630.4)
    box(*fi, Z, zt, "cab_in")
    F = sw.Front(fi, "+x")
    sw.mcc(F, Z, zt, "cab_in")
    sw.nameplate(F, F.L / 2, zt - .3, "MCC-R2A-2", "480 V  ·  SCR BLOWERS, CHEM FEED, BLOWDOWN, CEMS")
    sw.mat(F, Z)
    fv = (568.2, 571.2, 631.2, 646.4)
    box(*fv, Z, zt, "cab_in")
    F = sw.Front(fv, "+x")
    sw.drive(F, Z, zt, "cab_in", w=2.5)
    sw.nameplate(F, F.L / 2, zt - .3, "VFD-R2A", "SCR DILUTION-AIR BLOWERS  ·  FEED-PUMP AUX  ·  480 V")
    sw.arc_label(F, 1.0, Z + 5.6, "480 V", 12.0)
    sw.mat(F, Z)
    fd = (565.2, 568.0, 614.4, 646.4)
    box(*fd, Z, zt - .3, "panel_in")
    F = sw.Front(fd, "-x")
    sw.dcs(F, Z, zt - .3, "panel_in")
    for u, t, s in ((4.0, "DCS-R2A CTRL", "HRSG 1 CONTROLLERS  ·  REDUNDANT"),
                    (16.0, "MARSHALLING", "HRSG · BFP · CEMS · DUCT BURNER I/O"),
                    (28.0, "NETWORK / F&G", "FIBRE PATCH  ·  F&G NODE")):
        sw.nameplate(F, u, zt - .55, t, s)
    sw.mat(F, Z)

    # ---- west wall between the doors: UPS, battery rack, AC / DC / lighting panels
    fu = (IX0, IX0 + 3.0, 621.4, 626.4)
    box(*fu, Z, Z + 7.2, "cab_in")
    F = sw.Front(fu, "+x")
    sw.drive(F, Z, Z + 7.2, "cab_in", w=2.5, fans=False)
    sw.nameplate(F, F.L / 2, Z + 6.9, "UPS-R2A", "10 kVA  ·  120 V AC  ·  DCS / F&G")
    for row in range(3):                                                  # 125 V DC battery: open two-tier rack
        zr = Z + .4 + row * 1.6
        box(IX0 + .1, IX0 + 2.5, 627.2, 633.6, zr, zr + .12, "steel")
        for k in range(10):
            y = 627.4 + k * .62
            box(IX0 + .4, IX0 + 1.7, y, y + .5, zr + .12, zr + 1.1, "steel_dark")
            box(IX0 + 1.0, IX0 + 1.1, y + .2, y + .3, zr + 1.1, zr + 1.18, "red")
    for y in (627.2, 633.5):
        box(IX0 + .1, IX0 + .25, y, y + .1, Z, Z + 5.4, "steel")
    sw.nameplate(sw.Front((IX0, IX0 + 2.5, 627.2, 633.6), "+x"), 3.2, Z + 5.9, "BATT-R2A", "125 V DC  ·  60 CELLS  ·  VRLA")
    sw.panelboard(sw.Front((IX0, IX0 + .1, 634.4, 641.4), "+x"), Z, Z + 7.6, "panel_in")
    sw.nameplate(sw.Front((IX0, IX0 + .3, 634.4, 641.4), "+x"), 3.5, Z + 7.9, "DC-R2A · UPS-DP · LP-R2A",
                 "125 V DC  ·  120 V AC UPS  ·  480 / 277 V LIGHTING")
    # fire-alarm / F&G panel on the south wall
    box(558.0, 561.0, IY0, IY0 + .5, Z + 3.5, Z + 7.5, "sw_red")
    box(558.6, 560.4, IY0 + .5, IY0 + .55, Z + 6.0, Z + 7.0, "hmi")
    sw.nameplate(sw.Front((556.0, 563.0, IY0, IY0 + .5), "+y"), 3.5, Z + 8.0, "FACP-R2A", "FIRE ALARM  ·  F&G")

    # ---- trays over the lineups (power EL 11.4, control / instrument EL 11.9, cross tray EL 12.4)
    P, C, I, FO, FA = "cable_tc", "cable_mc", "cable_inst", "cable_fo", "cable_fa"
    ladder(579.6, 582.0, 613.0, 646.6, 11.4, "y", [(P, .12)] * 5 + [(C, .08)] * 4)            # T1 east lineup
    hangers(579.6, 582.0, (616, 624, 632, 640), 11.4)
    ladder(568.9, 570.9, 614.0, 646.6, 11.4, "y", [(P, .11)] * 4 + [(C, .08)] * 3)            # T2 island power
    hangers(568.9, 570.9, (618, 628, 638), 11.4)
    ladder(565.4, 567.6, 614.0, 646.6, 11.9, "y", [(I, .06)] * 9 + [(FO, .05)])               # T3 island instrument
    hangers(565.4, 567.6, (618, 628, 638), 11.9)
    ladder(565.4, 582.0, 646.6, 648.2, 11.4, "x", [(P, .11)] * 3 + [(C, .08)] * 2)            # north cross tray
    hangers(646.6, 648.2, (568, 575, 580), 11.4, along="x")
    # drops into every section top
    for (a, b) in sw.sections(fm[3] - fm[2], 1.67):                     # MCC-1: power + control per section
        drop(582.0, fm[2] + a + .2, fm[2] + b - .2, 11.45, zt, [P, P, C], r=.08)
    for (a, b) in sw.sections(fl[3] - fl[2] - 2.6, 2.6):                 # LC feeders (main section is the north end)
        drop(580.4, fl[2] + a + .3, fl[2] + b - .3, 11.45, zt, [P, P, P], r=.12)
    for (a, b) in sw.sections(fi[3] - fi[2], 1.67):                     # MCC-2
        drop(569.9, fi[2] + a + .2, fi[2] + b - .2, 11.45, zt, [P, C], r=.08)
    for (a, b) in sw.sections(fv[3] - fv[2], 2.5):                      # VFD outputs
        drop(569.9, fv[2] + a + .4, fv[2] + b - .4, 11.45, zt, [P, P], r=.11)
    for (a, b) in sw.sections(fd[3] - fd[2], 2.0):                      # marshalling: home-run multipairs
        drop(566.5, fd[2] + a + .2, fd[2] + b - .2, 11.95, zt - .3, [I, I, I, I], r=.05)
    # UPS / DC / panel feeders in a wall tray along the west wall
    ladder(IX0 + .1, IX0 + 1.3, 621.4, 641.4, 10.6, "y", [(P, .07)] * 3 + [(C, .06)] * 2, rung=1.5)
    for y in (623.9, 637.9):
        rod((IX0 + .7, y, 10.6), (IX0 + .7, y, Z + 7.6), .07, "pipe", seg=6)
    for y in (630.0,):
        rod((IX0 + .7, y, 10.6), (IX0 + .7, y, Z + 5.2), .06, P, seg=6)
    rod((IX0 + .7, 641.4, 10.9), (IX0 + .7, 647.4, 10.9), .07, P, seg=6)                       # to the cross tray
    rod((IX0 + .7, 647.4, 10.9), (565.4, 647.4, 11.5), .07, P, seg=6)

    # ---- 480 V secondary from T-R2A: through the north wall, over the room to the LC-R2A main section
    ladder(558.5, 561.5, 648.6, 652.0, 12.4, "y", [(P, .13)] * 10)
    ladder(558.5, 583.2, 648.6, 651.1, 12.4, "x", [(P, .13)] * 10)
    hangers(648.6, 651.1, (562, 570, 578), 12.4, along="x")
    for k in range(10):                                                  # 10 sets drop into the main breaker section
        x = 581.0 + k * .2
        rod((x, 649.6, 12.45), (x, 649.6, zt), .1, P, seg=6)
    box(580.8, 583.1, 648.9, 650.3, zt, zt + .06, "steel_dark")
    box(558.3, 561.7, IY1 - .05, Y1 + .05, 12.3, 13.0, "steel")         # wall sleeve
    # outside: across to the T-R2A LV cable box (hung off the rack posts) and down its riser
    ladder(558.5, 561.5, 652.0, 663.2, 12.4, "y", [(P, .13)] * 10)
    box(558.25, 561.7, 657.9, 658.1, 12.2, 12.4, "steel")
    for s_ in (558.5, 561.42):
        box(s_, s_ + .08, 663.0, 663.4, 6.0, 12.8, "pipe")              # vertical ladder on the LV box
    for k in range(10):
        x = 558.75 + k * .28
        rod((x, 663.2, 6.0), (x, 663.2, 12.5), .12, P, seg=6)
    # 13.8 kV primary: MV-105 off the EL 36 tray into the T-R2A air terminal chamber
    for k in (-1, 0, 1):
        x = 561.0 + k * .7
        rod((x, 677.4, 36.0), (x, 677.4, 7.6), .2, "cable_mv", seg=8)
        rod((x, 677.4, 7.6), (x, 676.0, 7.6), .2, "cable_mv", seg=8)
        rod((x, 676.0, 7.6), (x, 676.0, 6.9), .2, "cable_mv", seg=8)
    for s_ in (559.6, 562.3):
        box(s_, s_ + .08, 677.8, 678.2, 7.0, 36.0, "pipe")
    z = 8.0
    while z < 36:
        box(559.6, 562.4, 677.8, 678.2, z, z + .07, "pipe")
        z += 2.0
    # the riser's top turns east into the side of the EL 36 MV tray (rails x 563.5 / 566.5): a short ladder branch,
    # the three cables carried over into the tray (owner, Oct 27: the riser stood beside the tray end, unconnected)
    for y_ in (676.6, 678.2):
        box(559.6, 563.5, y_ - .08, y_, 35.9, 36.6, "pipe")
    for x_ in (560.4, 561.6, 562.8):
        box(x_, x_ + .12, 676.6, 678.2, 35.9, 36.0, "pipe")
    for k in (-1, 0, 1):
        x = 561.0 + k * .7
        rod((x, 677.4, 36.0), (x, 677.4, 36.25), .2, "cable_mv", seg=8)
        rod((x, 677.4, 36.25), (564.6 + k * .6, 677.4, 36.25), .2, "cable_mv", seg=8)

    # ---- out to the field: the 600 V power / control cables leave through the north-wall transit frame (EL 8.9) for
    # the riser to the EL 30 LV tray; instrumentation, thermocouple extension, fire alarm and fibre go up through the
    # roof glands to the EL 42 control tray
    for k, x in enumerate((579.4, 579.7, 580.0, 580.39, 580.7)):
        c = C if k == 1 else P
        rod((x, 648.2, 11.5), (x, 651.0, 11.5), .1, c, seg=6)
        rod((x, 651.0, 11.5), (x, 651.0, 8.9), .1, c, seg=6)
        rod((x, 651.0, 8.9), (x, 651.45, 8.9), .1, c, seg=6)
    ladder(574.9, 579.6, 643.3, 644.7, 11.9, "x", [(I, .06)] * 3 + [(C, .07)] * 2 + [(FO, .05)])
    for y, c in ((643.56, I), (643.82, "cable_tcx"), (643.87, C), (644.05, "cable_tcx"), (644.16, I), (644.27, FA),
                 (644.48, FO)):
        rod((575.75, y, 12.0), (575.75, y, 14.3), .05, c, seg=6)
    box(575.2, 576.3, 643.2, 644.8, ZC - .1, ZC, "steel_dark")           # roof gland plate, inside

    # ---- building wire, lighting, fire alarm, finishes
    for x in (560.4, 574.8):
        rod((x, 614.0, 13.15), (x, 646.0, 13.15), .05, "pipe", seg=6)                          # EMT, THHN inside
        for y in (617.0, 623.0, 629.0, 635.0, 641.0):
            sw.fixture(x, y, 12.9, roof=ZC)
    rod((IX0 + .2, 638.0, Z + 7.6), (IX0 + .2, 638.0, 13.15), .05, "pipe", seg=6)
    rod((IX0 + .2, 638.0, 13.15), (560.4, 638.0, 13.15), .05, "pipe", seg=6)
    rod((560.4, 646.0, 13.15), (574.8, 646.0, 13.15), .05, "pipe", seg=6)
    for y in (618.0, 642.0):                                                                     # receptacles
        box(IX0, IX0 + .1, y - .3, y + .3, Z + 1.5, Z + 2.1, "label")
    for x in (562.0, 575.0):
        box(x - .3, x + .3, IY1 - .1, IY1, Z + 1.5, Z + 2.1, "label")
        box(x - .3, x + .3, IY0, IY0 + .1, Z + 1.5, Z + 2.1, "label")
    loop = [(559.5, IY0 + .5, Z + 7.5), (559.5, IY0 + .5, 13.25), (559.5, 646.0, 13.25), (576.0, 646.0, 13.25),
            (576.0, 615.0, 13.25), (562.0, 615.0, 13.25)]
    for a, b in zip(loop, loop[1:]):
        rod(a, b, .04, FA, seg=6)
    for (x, y) in ((559.5, 622.0), (559.5, 636.0), (576.0, 630.0), (576.0, 642.0), (567.0, 646.0)):
        rod((x, y, 13.25), (x, y, 13.1), .3, "label", seg=12)                                   # smoke detectors
    sw.ground_bus([(IX0 + .05, IY0 + .05), (IX0 + .05, IY1 - .05), (IX1 - .05, IY1 - .05), (IX1 - .05, IY0 + .05),
                   (IX0 + .05, IY0 + .05)], Z + 1.2)
    for (x, y, n) in ((IX0 + .2, 642.0, (1, 0)), (IX1 - .2, 612.9 + 18, (-1, 0)), (575.0, IY0 + .2, (0, 1))):
        sw.extinguisher(x, y, Z, n)
    for (x, y, n) in ((IX0 + .05, 618.0, (1, 0)), (IX0 + .05, 645.0, (1, 0))):
        sw.exit_sign(x, y, 9.6, n)
    for (xa, ya, yb) in ((563.6, 613.5, 647.0), (573.0, 613.5, 647.0)):
        box(xa - .12, xa + .12, ya, yb, Z + .02, Z + .03, "yellow")
    import figure
    figure.build(rod, 573.6, 638.0, Z, a=3.1416, vest="workwear", pose="work")                  # at a VFD keypad
    fuel.D = False
    return len(G["parts"]) - n0
