"""CEMS shelters at LOD 3 (boiler deck, Oct 23: "the CEMS shelters and the stack, showing all the wire and cable").
Each HRSG's CEMS shelter (16 x 14 ft, 12 ft) was a solid block. It becomes a walk-in analyzer shelter as the
industry builds them (photos of prefabricated CEMS shelters, owner, Oct 23): insulated panel walls on a steel skid,
roof with lifting lugs and an exhaust vent; outside, a stainless wall-mount HVAC unit, explosion-proof junction boxes
and fittings on rigid conduit, strobe and horn, a light over the door, a fire extinguisher, a calibration-gas cylinder
rack with regulators, the heated sample-line bulkhead, and the cable stub-ups from the duct bank. Inside: three
analyzer racks (NOx, CO, O2, NH3 slip), the sample-conditioning panel (chiller, pumps, filters), the data
acquisition PLC with UPS, the 480 / 208-120 V transformer and panel, the heated-line controller, the calibration-gas
manifold, an overhead ladder tray with the drops, lights and a smoke detector.
Every cable leg in the schedule lands here: 480 V power (TC-ER), control, fire alarm (FPLR), the control-room fibre,
the instrument pairs to JB-CEMS AI / DI, building wire; plus the probe signal / power on the stack tray.
The roof, east and south walls sit on layer CEMS_ROOF so a cutaway can lift them. Typical, not engineered;
footprint and height kept."""
import fuel
from fuel import box, rod
import swgr_rooms as sw

Z = .8                     # floor on the skid
ZC = 11.2                  # ceiling


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def shelter(k):
    dx = 160 * k
    it = fuel.find(f"CEMS shelter, HRSG {k + 1}")
    X0, X1, Y0, Y1 = 648 + dx, 664 + dx, 806.0, 820.0
    fuel.G["parts"][:] = [p for p in fuel.G["parts"] if not (p["item"] == it["id"] and not p.get("d"))]
    fuel.G["parts"][:] = [p for p in fuel.G["parts"] if not (p["item"] == it["id"] and p["color"] == "roof")]
    it["info"] = ("Walk-in CEMS analyzer shelter on a steel skid: NOx, CO, O2 and NH3-slip analyzers, sample conditioning, "
                  "data acquisition PLC and UPS, calibration gas, heated sample line from the stack probe; HVAC, "
                  "explosion-proof fittings, strobe / horn. Fed from R2A (480 V, control, fire alarm), fibre to the control "
                  "room, instrument pairs via JB-CEMS AI / DI. Typical.")
    fuel.on(it)
    fuel.D = False
    R = "CEMS_ROOF"
    # skid and shell (insulated panels with batten seams)
    box(X0, X1, Y0, Y1, 0, Z, "steel_dark")
    box(X0 + .2, X1 - .2, Y0 + .2, Y0 + .5, Z, ZC, "ehouse", layer=R)                # south wall (door)
    box(X0 + .2, X1 - .2, Y1 - .5, Y1 - .2, Z, ZC, "ehouse")                         # north wall
    box(X0 + .2, X0 + .5, Y0 + .5, Y1 - .5, Z, ZC, "ehouse")                         # west wall
    box(X1 - .5, X1 - .2, Y0 + .5, Y1 - .5, Z, ZC, "ehouse", layer=R)                # east wall
    box(X0, X1, Y0, Y1, ZC, ZC + .6, "roof", layer=R)
    fuel.D = True
    for x in range(int(X0) + 2, int(X1), 2):                                         # panel battens
        box(x - .04, x + .04, Y0 + .12, Y0 + .2, Z, ZC, "steel", layer=R)
        box(x - .04, x + .04, Y1 - .2, Y1 - .12, Z, ZC, "steel")
    for y in range(int(Y0) + 2, int(Y1), 2):
        box(X0 + .12, X0 + .2, y - .04, y + .04, Z, ZC, "steel")
    for (x, y) in ((X0 + .6, Y0 + .6), (X1 - .6, Y0 + .6), (X0 + .6, Y1 - .6), (X1 - .6, Y1 - .6)):
        rod((x, y, ZC + .6), (x, y, ZC + 1.2), .22, "steel", seg=8, layer=R)        # lifting lugs
    rod((X0 + 4, Y1 - 3, ZC + .6), (X0 + 4, Y1 - 3, ZC + 2.6), .55, "steel", seg=10, layer=R)   # exhaust vent
    rod((X0 + 4, Y1 - 3, ZC + 2.6), (X0 + 4, Y1 - 3, ZC + 3.2), 1.0, "steel", r2=.2, seg=10, layer=R)
    # ---- outside: south face, door and its fittings
    DX = X0 + 7.0
    box(DX, DX + 3.2, Y0 + .05, Y0 + .2, Z, Z + 7.2, "door", layer=R)
    box(DX + .7, DX + 2.5, Y0, Y0 + .05, Z + 4.0, Z + 6.2, "glass", layer=R)
    box(DX + 2.7, DX + 2.85, Y0 - .1, Y0 + .05, Z + 3.3, Z + 3.7, "steel", layer=R)
    decal((DX + 1.6, Y0 - .02, Z + 6.7), (0, -1, 0), 2.2, .45, [(f"CEMS-{k + 1}", .62, True, "#111111")], bg="#ffffff")
    rod((DX + 1.6, Y0 - .1, Z + 8.0), (DX + 1.6, Y0 - .6, Z + 8.0), .32, "steel_dark", seg=10)   # XP light over the door
    rod((DX + 1.6, Y0 - .6, Z + 7.9), (DX + 1.6, Y0 - .6, Z + 7.5), .28, "lamp", seg=10)
    rod((X1 - 1.2, Y0 - .1, ZC - .4), (X1 - 1.2, Y0 - .7, ZC - .4), .3, "red", seg=10)  # strobe
    rod((X1 - 2.4, Y0 - .1, ZC - .4), (X1 - 2.4, Y0 - .9, ZC - .4), .35, "steel_dark", r2=.12, seg=10)  # horn
    rod((DX - 1.2, Y0 - .25, Z + 1.2), (DX - 1.2, Y0 - .25, Z + 3.0), .28, "sw_red", seg=10)  # extinguisher
    # explosion-proof junction boxes and stainless boxes on rigid conduit (south and west faces)
    for (x, z, c) in ((X0 + 2.0, 6.2, "panel"), (X0 + 4.6, 4.4, "steel"), (X1 - 3.5, 7.4, "panel")):
        box(x - .7, x + .7, Y0 - .45, Y0, z - .9, z + .9, c)
        box(x - .2, x + .2, Y0 - .5, Y0 - .45, z + .2, z + .6, "red")
    rod((X0 + 2.0, Y0 - .25, 7.1), (X0 + 2.0, Y0 - .25, ZC - .3), .1, "pipe", seg=8)
    rod((X0 + 2.0, Y0 - .25, ZC - .3), (X1 - 3.5, Y0 - .25, ZC - .3), .1, "pipe", seg=8)
    rod((X1 - 3.5, Y0 - .25, ZC - .3), (X1 - 3.5, Y0 - .25, 8.3), .1, "pipe", seg=8)
    rod((X0 + 4.6, Y0 - .25, 3.5), (X0 + 4.6, Y0 - .25, .3), .1, "pipe", seg=8)
    # ---- north face: stainless wall-mount HVAC unit (the 2 x 5 kW loads in the schedule) with its disconnect
    box(X0 + 6, X0 + 10.5, Y1, Y1 + 1.6, Z + 1.0, Z + 8.0, "steel")
    box(X0 + 6.3, X0 + 10.2, Y1 + 1.6, Y1 + 1.65, Z + 1.4, Z + 4.0, "louvre")
    box(X0 + 6.3, X0 + 10.2, Y1 + 1.6, Y1 + 1.65, Z + 5.0, Z + 7.6, "louvre")
    box(X0 + 11.2, X0 + 12.4, Y1, Y1 + .5, Z + 4.0, Z + 5.6, "panel")                 # fused disconnect
    rod((X0 + 11.8, Y1 + .25, Z + 4.0), (X0 + 11.8, Y1 + .25, .3), .1, "pipe", seg=8)
    # ---- west face: heated sample-line bulkhead, calibration-gas cylinder rack with regulators
    box(X0 - .2, X0, 811.4, 812.6, 9.4, 10.6, "steel_dark")                          # bulkhead plate (line arrives at EL 10)
    for j in range(4):
        y = 814.4 + j * 1.15
        rod((X0 - .8, y, .3), (X0 - .8, y, 5.0), .38, "steel", seg=12)
        rod((X0 - .8, y, 5.0), (X0 - .8, y, 5.5), .18, ("amber", "red", "steel_dark", "amber")[j], seg=8)
        rod((X0 - .8, y, 5.5), (X0 - .2, y, 5.9), .04, "pipe", seg=4)                 # regulator pigtail
    box(X0 - 1.4, X0, 813.8, 818.8, 3.2, 3.35, "steel")                              # chain bar
    box(X0 - 1.6, X0, 813.6, 819.0, 6.3, 6.45, "steel")                              # canopy
    box(X0 - .35, X0, 814, 818.5, 5.8, 6.2, "steel")                                 # regulator manifold
    # ---- cable entry: rigid conduit stub-ups from the duct bank at the SE corner into an XP junction box
    CX = X1 - 1.4
    cols = ("cable_tc", "cable_tc", "cable_mc", "cable_inst", "cable_fa", "cable_fo")
    for j, c in enumerate(cols):
        x = CX - 2.2 + j * .42
        rod((x, Y0 - .9, 0), (x, Y0 - .9, 2.6), .12, "pipe", seg=8)                    # rigid conduit
        rod((x, Y0 - .9, 2.6), (x, Y0 - .4, 3.0), .12, "pipe", seg=8)                  # LB into the box
        rod((x, Y0 - .9, 0), (x, Y0 - .9, -.01), .1, c, seg=6)
    box(CX - 2.6, CX + .2, Y0 - .5, Y0, 2.6, 4.4, "panel")                            # entry junction box
    box(CX - 2.5, CX + .1, Y0 + .5, Y0 + .6, 3.1, 3.9, "steel_dark")                   # wall sleeve, inside
    decal((CX - 1.2, Y0 - .52, 4.1), (0, -1, 0), 2.6, .3, [("480 V · CONTROL · I/O · F&G · FIBRE", .5, True, "#111111")],
          bg="#ffd200")
    # ---- inside
    box(X0 + .5, X1 - .5, Y0 + .5, Y1 - .5, Z, Z + .02, "epoxy")
    # analyzer racks along the north wall (front facing south)
    for j, (name, sub) in enumerate((("NOx / O2", "chemiluminescence"), ("CO / CO2", "NDIR"), ("NH3 slip", "TDL"))):
        x0 = X0 + 1.2 + j * 2.4
        f = (x0, x0 + 2.1, Y1 - 3.0, Y1 - .5)
        box(*f, Z, Z + 7.4, "cab_in")
        F = sw.Front(f, "-y")
        for r in range(3):
            zr = Z + 4.0 + r * 1.0
            F.b(.15, 1.95, zr, zr + .8, 0, .06, "panel_in")
            F.b(.3, 1.0, zr + .2, zr + .6, .06, .08, "hmi")
            sw.lamps(F, 1.2, zr + .3, ("led_g", "led_g", "led_a"), sz=.09, gap=.18)
        F.b(.15, 1.95, Z + .4, Z + 3.6, 0, .05, "louvre")
        sw.nameplate(F, 1.05, Z + 7.1, name, sub)
    # data acquisition PLC + UPS on the east wall, front west
    f = (X1 - 2.6, X1 - .5, Y0 + 2.0, Y0 + 5.6)
    box(*f, Z, Z + 7.0, "panel_in")
    F = sw.Front(f, "-x")
    sw.dcs(F, Z, Z + 7.0, "panel_in")
    sw.nameplate(F, 1.8, Z + 6.6, "DAHS / PLC", "DATA ACQUISITION · UPS · FIBRE TO THE CR")
    # sample-conditioning panel on the west wall: chiller, pumps, filters, tubing
    box(X0 + .5, X0 + .7, Y0 + 2.0, Y0 + 7.4, Z + 1.0, Z + 8.0, "panel_in")
    box(X0 + .7, X0 + 1.9, Y0 + 2.4, Y0 + 3.8, Z + 1.2, Z + 3.4, "machine")          # chiller
    for j in range(2):
        rod((X0 + 1.3, Y0 + 4.6 + j * 1.2, Z + 2.0), (X0 + 1.3, Y0 + 4.6 + j * 1.2, Z + 3.0), .32, "motor", seg=10)
    for j in range(4):
        rod((X0 + .9, Y0 + 2.6 + j * 1.2, Z + 4.6), (X0 + .9, Y0 + 2.6 + j * 1.2, Z + 5.8), .14, "glass", seg=8)
    for j in range(5):
        rod((X0 + .8, Y0 + 2.2 + j * 1.1, Z + 6.6), (X0 + .8, Y1 - 3.2, Z + 6.6), .03, "pipe", seg=4)   # tubing
    rod((X0 + .3, 812.0, 10.0), (X0 + .8, 812.0, 10.0), .16, "pipe", seg=8)           # heated line through the bulkhead
    rod((X0 + .8, 812.0, 10.0), (X0 + .8, Y0 + 5.0, Z + 6.6), .16, "pipe", seg=8)
    box(X0 + .5, X0 + .9, Y0 + 7.8, Y0 + 9.2, Z + 6.0, Z + 7.6, "panel_in")            # heated-line controller
    # transformer and panelboard on the south wall, east of the door
    box(X1 - 4.4, X1 - 2.8, Y0 + .5, Y0 + 1.5, Z, Z + 2.6, "cab_in")                # 480 / 208-120 V dry type
    box(X1 - 4.4, X1 - 2.8, Y0 + .5, Y0 + .8, Z + 3.4, Z + 6.8, "panel_in")         # panelboard
    # calibration-gas manifold on the north wall, west end
    box(X0 + .6, X0 + 1.0, Y1 - 3.4, Y1 - .6, Z + 7.6, Z + 8.4, "steel")
    # overhead ladder tray: entry box (SE) -> along the south wall -> up the middle -> over the racks
    P, C, I, FA, FO = "cable_tc", "cable_mc", "cable_inst", "cable_fa", "cable_fo"
    fill = [(P, .08), (P, .08), (C, .06), (I, .05), (I, .05), (FA, .04), (FO, .04)]

    def ladder(x0, x1, y0, y1, z, along):
        if along == "x":
            for y in (y0, y1 - .06):
                box(x0, x1, y, y + .06, z, z + .3, "pipe")
            for j, (c, r) in enumerate(fill):
                y = y0 + .12 + (y1 - y0 - .24) * (j + .5) / len(fill)
                rod((x0, y, z + .06 + r), (x1, y, z + .06 + r), r, c, seg=6)
        else:
            for x in (x0, x1 - .06):
                box(x, x + .06, y0, y1, z, z + .3, "pipe")
            for j, (c, r) in enumerate(fill):
                x = x0 + .12 + (x1 - x0 - .24) * (j + .5) / len(fill)
                rod((x, y0, z + .06 + r), (x, y1, z + .06 + r), r, c, seg=6)
    TZ = 9.4
    ladder(X0 + 1.0, X1 - .6, Y0 + .8, Y0 + 2.0, TZ, "x")
    ladder(X0 + 8.0, X0 + 9.2, Y0 + 2.0, Y1 - 3.2, TZ, "y")
    ladder(X0 + 1.0, X0 + 8.4, Y1 - 4.0, Y1 - 3.2, TZ, "x")
    for j, c in enumerate(cols):                                                     # from the entry box up through the wall
        x = CX - 2.2 + j * .42
        rod((x, Y0 - .3, 3.5), (x, Y0 + .75, 3.5), .07, c, seg=6)                     # through the wall sleeve
        rod((x, Y0 + .75, 3.5), (x, Y0 + .75, TZ + .2), .07, c, seg=6)                # up the inside face
        rod((x, Y0 + .75, TZ + .2), (x, Y0 + .9, TZ + .2), .07, c, seg=6)
    for j in range(3):                                                               # drops into each analyzer rack
        xr = X0 + 2.25 + j * 2.4
        for m, c in enumerate((P, I, I)):
            rod((xr - .3 + m * .3, Y1 - 3.6, TZ), (xr - .3 + m * .3, Y1 - 3.6, Z + 7.4), .05, c, seg=6)
    for m, c in enumerate((P, I, FO, C)):                                            # drops into the DAHS / PLC
        rod((X1 - 1.6, Y0 + 2.4 + m * .3, TZ), (X1 - 1.6, Y0 + 2.4 + m * .3, Z + 7.0), .05, c, seg=6)
    for m, c in enumerate((P, P)):                                                   # transformer / panel
        rod((X1 - 3.8 + m * .4, Y0 + 1.2, TZ), (X1 - 3.8 + m * .4, Y0 + 1.2, Z + 6.8), .07, c, seg=6)
    rod((X0 + 1.4, Y0 + 1.4, TZ), (X0 + 1.4, Y0 + 1.4, Z + 8.0), .05, P, seg=6)       # to the conditioning panel
    rod((X0 + 1.4, Y0 + 1.4, Z + 8.0), (X0 + .7, Y0 + 2.4, Z + 8.0), .05, P, seg=6)
    for (x, y) in ((X0 + 4, Y0 + 4.5), (X0 + 4, Y1 - 5.5), (X1 - 4, Y1 - 5.5)):
        box(x - .3, x + .3, y - 1.8, y + 1.8, ZC - .25, ZC, "lamp_in")                 # LED fixtures
    rod((X0 + 11, Y1 - 6, ZC), (X0 + 11, Y1 - 6, ZC - .12), .3, "label", seg=12)       # smoke detector
    fuel.D = False
    return 1


def build():
    n0 = len(fuel.G["parts"])
    for k in range(3):
        shelter(k)
    return len(fuel.G["parts"]) - n0
