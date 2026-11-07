"""Electrolyzer hall H2 22 at LOD 3 (25 MW PEM, 5 x 5 MW PEM units, sheet 14).

The building was a solid block. It is now an open hall, and its roof sits on its own layer (H2_ROOF) so cameras
and the viewer can lift it off:
- portal-frame steel (columns and roof trusses every 20 ft), insulated wall panels on a slab with an epoxy floor,
  louvres, a roll-up door, ceiling hydrogen detectors at the high points, exhaust fans and LED high-bays;
- five electrolyzer skids: frame, four PEM stack modules with end plates and tie rods, an H2 / water separator and
  an O2 / water separator, a circulation pump, process piping, a local control cabinet; H2 to an overhead header
  along the hall and out through the east wall, O2 vents up through the roof;
- five rectifiers (12-pulse thyristor, 7 MVA) with cabinet doors and roof vents;
- the DC bus: per unit a ladder tray from the rectifier top over the aisle to the stack, carrying parallel
  single-conductor DC cables (red +, black -), with drops at both ends;
- the 13.8 kV supply: the rectifier transformers north of the hall feed each rectifier through a covered floor
  trench (MV-105 in the trench, conduits up into the cabinet);
- an LV / control room (MCC, PLC / SCADA, UPS) in the north-east corner, cooling-water headers from the dry
  coolers, people at work;
- outside: a pipe track under the dry coolers to the dryer and compressors (N2, instrument air, cooling water)
  with a covered cable trench beside it.
All typical, not engineered.
"""
import fuel
from fuel import box, rod, pipe, find, on

X0, X1, Y0, Y1 = 2010.0, 2170.0, 1440.0, 1520.0
EAVE = 26.0
ROOF = "H2_ROOF"
UNITS = [2020.0 + 20 * k for k in range(5)]          # electrolyzer / rectifier x0


def person(x, y, z=0.0, a=0.0, vest="hivis"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest)


def hollow():
    G = fuel.G
    bld = find("H2 22: electrolyzer building")
    keep = []
    for p in G["parts"]:
        if p["item"] == bld["id"]:
            if p["kind"] == "box" and p["color"] == "hall":
                continue                                                   # the solid block goes
            if p["kind"] == "prism" or (p.get("min") and p["min"][2] >= 29.9):
                p["layer"] = ROOF                                          # roof and ridge vents lift off
        keep.append(p)
    G["parts"][:] = keep
    bld["info"] = (bld.get("info", "") + " Open hall: portal frame, five PEM skids, five rectifiers with DC cable "
                   "trays over the aisle, 13.8 kV in floor trenches, LV / control room.").strip()
    return bld


def shell(bld):
    on(bld)
    fuel.D = False
    box(X0, X1, Y0, Y1, 0, .5, "concrete")                                  # slab
    fuel.D = True
    box(X0 + .6, X1 - .6, Y0 + .6, Y1 - .6, .5, .55, "epoxy")
    for (a, b, c, d) in ((X0, X1, Y0, Y0 + .6), (X0, X1, Y1 - .6, Y1), (X0, X0 + .6, Y0, Y1), (X1 - .6, X1, Y0, Y1)):
        box(a, b, c, d, .5, EAVE, "hall")                                   # wall panels
    for (a, b, c, d) in ((X0 + .6, X1 - .6, Y0 + .6, Y0 + .7), (X0 + .6, X1 - .6, Y1 - .7, Y1 - .6),
                         (X0 + .6, X0 + .7, Y0 + .6, Y1 - .6), (X1 - .7, X1 - .6, Y0 + .6, Y1 - .6)):
        box(a, b, c, d, .55, EAVE - .5, "wall_in")                          # liner
    # portal frames: columns on both long walls and a truss across the span every 20 ft
    for x in [X0 + 1.2 + 20 * k for k in range(9)]:
        x = min(x, X1 - 1.2)
        for y in (Y0 + 1.2, Y1 - 1.2):
            box(x - .5, x + .5, y - .5, y + .5, .55, EAVE, "steel")
        box(x - .3, x + .3, Y0 + 1, Y1 - 1, EAVE - .6, EAVE, "steel")       # bottom chord
        rod((x, Y0 + 1, EAVE), (x, (Y0 + Y1) / 2, 29.6), .3, "steel", seg=6)   # top chords to the ridge
        rod((x, Y1 - 1, EAVE), (x, (Y0 + Y1) / 2, 29.6), .3, "steel", seg=6)
        for t in range(1, 8):                                               # web
            yy = Y0 + 1 + (Y1 - Y0 - 2) * t / 8
            zt = EAVE + (29.6 - EAVE) * (1 - abs(yy - (Y0 + Y1) / 2) / ((Y1 - Y0) / 2 - 1))
            rod((x, yy, EAVE - .3), (x, yy, zt), .12, "steel", seg=4)
    for y in (Y0 + 20, (Y0 + Y1) / 2, Y1 - 20):                             # purlins / bracing line
        box(X0 + 1, X1 - 1, y - .2, y + .2, EAVE - .4, EAVE - .1, "steel")
    # LED high-bays, hydrogen detectors at the high points, exhaust fans high on the walls
    for x in [X0 + 11 + 20 * k for k in range(8)]:
        for y in (Y0 + 18, Y1 - 18):
            box(x - 1, x + 1, y - .6, y + .6, EAVE - 1.6, EAVE - 1.3, "steel")
            box(x - .9, x + .9, y - .5, y + .5, EAVE - 1.7, EAVE - 1.6, "lamp_in")
        rod((x, (Y0 + Y1) / 2, EAVE + 2.2), (x, (Y0 + Y1) / 2, EAVE + 1.6), .25, "sp_yellow", seg=10)
    for x in (X0 + 30, X0 + 70, X0 + 110, X0 + 150):
        rod((x, Y0 + .6, 20), (x, Y0 + 1.6, 20), 1.8, "fan", seg=16)
        rod((x, Y1 - .6, 20), (x, Y1 - 1.6, 20), 1.8, "fan", seg=16)
    fuel.D = False


def unit(x0):
    """One PEM electrolyzer skid inside its 7.5 x 27.7 ft footprint (stacks south, separators north)."""
    G = fuel.G
    k = UNITS.index(x0)
    it = find(f"PEM electrolyzer {k + 1}")
    G["parts"][:] = [p for p in G["parts"] if p["item"] != it["id"]]
    on(it)
    x1, y0, y1 = x0 + 7.5, 1450.0, 1477.7
    xc = (x0 + x1) / 2
    box(x0, x1, y0, y1, .55, 1.3, "steel")                                  # skid frame
    fuel.D = True
    for s in range(4):                                                      # stack modules
        ya = y0 + 1 + s * 4.2
        box(x0 + .8, x1 - .8, ya + .4, ya + 3.6, 1.3, 6.8, "bess")
        for yy in (ya + .2, ya + 3.6):
            box(x0 + .5, x1 - .5, yy, yy + .25, 1.3, 7.3, "steel")            # end plates
        for (dx, dz) in ((.9, 1.8), (6.6, 1.8), (.9, 6.8), (6.6, 6.8)):
            rod((x0 + dx, ya + .1, dz), (x0 + dx, ya + 3.9, dz), .1, "steel", seg=6)   # tie rods
        box(x0 + 1.4, x0 + 2.4, ya + 1.2, ya + 2.8, 7.3, 8.2, "copper")      # DC terminal (+)
        box(x1 - 2.4, x1 - 1.4, ya + 1.2, ya + 2.8, 7.3, 8.2, "copper_dark")  # DC terminal (-)
    yb = y0 + 19
    for (dx, c, nm) in ((1.9, "hydrogen", "H2"), (5.6, "tank", "O2")):      # gas / water separators
        rod((x0 + dx, yb + 3, 1.3), (x0 + dx, yb + 3, 9.5), 1.4, c, seg=16)
        rod((x0 + dx, yb + 3, 9.5), (x0 + dx, yb + 3, 10.2), 1.4, c, r2=.5, seg=16)
    rod((xc, yb, 2.2), (xc, yb + 1.6, 2.2), .8, "pump", seg=12)              # circulation pump
    box(xc - .7, xc + .7, yb - 1.6, yb, 1.3, 2.9, "motor")
    box(x0 + .5, x1 - .5, y1 - 2.6, y1 - .2, 1.3, 7.5, "cab_in")              # local control cabinet
    pipe([(x0 + 1.9, yb + 3, 10.2), (x0 + 1.9, yb + 3, 12.5), (x0 + 1.9, 1485.4, 12.5)], 12.5, .25, "hydrogen")
    pipe([(x0 + 5.6, yb + 3, 10.2), (x0 + 5.6, yb + 3, 11.6), (x1 + .6, yb + 3, 11.6), (x1 + .6, yb + 3, 33.5)], 11.6,
         .3, "pipe")                                                         # O2 vent, clear of the DC tray, through the roof
    rod((x1 + .6, yb + 3, 33.5), (x1 + .6, yb + 3, 34.3), .5, "steel", seg=10)
    pipe([(x0 + 1.5, y0 + 1, 7.6), (x0 + 1.5, yb + 1.5, 7.6), (x0 + 1.9, yb + 1.5, 7.6)], 7.6, .2, "pipe")
    fuel.D = False


def rectifier_and_dc(x0):
    G = fuel.G
    k = UNITS.index(x0)
    it = find(f"Rectifier {k + 1}")
    G["parts"][:] = [p for p in G["parts"] if p["item"] != it["id"]]
    on(it)
    x1, y0, y1 = x0 + 8.2, 1490.0, 1504.8
    box(x0, x1, y0, y1, .55, .9, "steel")
    box(x0 + .1, x1 - .1, y0 + .1, y1 - .1, .9, 8, "cab_in")
    fuel.D = True
    for j in range(4):                                                      # doors on the aisle side
        ya = y0
        box(x0 + .3 + j * 1.95, x0 + 2.1 + j * 1.95, ya - .05, ya + .1, 1.2, 7.6, "panel_in")
        box(x0 + 1.8 + j * 1.95, x0 + 1.95 + j * 1.95, ya - .12, ya, 4, 5, "steel")     # handles
    for j in range(3):
        box(x0 + 1 + j * 2.4, x0 + 2.8 + j * 2.4, y0 + 3, y1 - 3, 8, 8.6, "louvre")    # roof vents
    box(x0 + .3, x1 - .3, y0 + .1, y0 + .12, 6.2, 7, "lamp_in")                  # status display strip
    # DC bus: ladder tray from the rectifier top, over the aisle at EL 14, down to the stack terminals
    xa, xb = x0 + 1.2, x0 + 6.3                                              # tray rails (width ~5 ft)
    ys, ye = y0 + 4, 1468.0                                                  # rectifier top -> past the last stack
    zt = 14.0
    for xr in (xa, xb):
        box(xr - .08, xr + .08, ys - .1, ys + .1, 8.6, zt, "pipe")             # riser rails
        box(xr - .08, xr + .08, ye, ys, zt - .4, zt, "pipe")                  # horizontal rails
        box(xr - .08, xr + .08, ye - .1, ye + .1, 8.2, zt, "pipe")            # drop rails
    y = ye + .5
    while y < ys:
        box(xa, xb, y - .08, y + .08, zt - .4, zt - .3, "pipe")               # rungs
        y += 1.0
    for zz in range(9, int(zt), 1):
        box(xa, xb, ys - .08, ys + .08, zz, zz + .1, "pipe")
        box(xa, xb, ye - .08, ye + .08, zz, zz + .1, "pipe")
    for j in range(8):                                                       # parallel 1/C DC cables
        xcab = xa + .35 + j * .6
        col = "cable_tc"                                                     # black jackets, polarity by tape
        tape = "red" if j < 4 else "sp_black"
        for (pa, pb) in (((xcab, ys, 9.0), (xcab, ys, 9.5)), ((xcab, ye, 9.0), (xcab, ye, 9.5))):
            rod(pa, pb, .19, tape, seg=8)
        rod((xcab, ys, 8.6), (xcab, ys, zt - .1), .17, col, seg=8)
        rod((xcab, ys, zt - .1), (xcab, ye, zt - .1), .17, col, seg=8)
        rod((xcab, ye, zt - .1), (xcab, ye, 8.3), .17, col, seg=8)
    for yh in (ye + 4, (ye + ys) / 2, ys - 4):                                # trapeze hangers from the truss line
        for xr in (xa - .3, xb + .3):
            rod((xr, yh, zt - .5), (xr, yh, EAVE - .6), .06, "steel", seg=4)
        box(xa - .4, xb + .4, yh - .15, yh + .15, zt - .7, zt - .4, "steel")
    box(x0 + .5, x0 + 7.7, 1467.6, 1468.6, 7.3, 8.1, "copper")                 # stack DC bus bar
    # 13.8 kV from the rectifier transformer: floor trench under a checker-plate cover, conduits into the cabinet
    xt = x0 + 4.1
    box(xt - 1.6, xt + 1.6, y1, Y1 - .6, .55, .6, "grating")
    for j in range(3):
        rod((xt - 1 + j, y1 - 1, .3), (xt - 1 + j, y1 - 1, 1.2), .2, "steel", seg=6)
    fuel.D = False


def electrical_room():
    it = fuel.new_item("OPT_H2", "H2 22 LV / control room (MCC, PLC / SCADA, UPS)", (2128, 2166, 1492, 1516), (0, 12),
                       area="K", sheet="typical (H2 hall)", register=False,
                       info="480 V MCC for the pumps, fans and HVAC; PLC / SCADA and safety PLC; UPS; fibre to the "
                            "control room.")
    on(it)
    for (a, b, c, d) in ((2128, 2166, 1492, 1492.4), (2128, 2128.4, 1492, 1516), (2165.6, 2166, 1492, 1516)):
        box(a, b, c, d, .55, 12, "wall_in")
    box(2128, 2166, 1492, 1516, 12, 12.4, "wall_in")                           # ceiling slab
    box(2140, 2143, 1491.9, 1492, .55, 7.5, "door_in")
    fuel.D = True
    for j in range(8):                                                       # MCC lineup along the north side
        box(2130 + j * 2.6, 2132.4 + j * 2.6, 1511, 1514, .55, 7.6, "cab_in")
        box(2130.2 + j * 2.6, 2132.2 + j * 2.6, 1510.9, 1511, 1.5, 7, "panel_in")
    for j in range(3):                                                       # PLC / UPS cabinets
        box(2150 + j * 3, 2152.6 + j * 3, 1496, 1499, .55, 7.6, "cab_in")
    fuel.D = False


def cooling_and_people():
    bld = find("H2 22: electrolyzer building")
    on(bld)
    fuel.D = True
    # cooling-water supply / return headers from the dry coolers, along the hall at EL 11 with drops to each skid
    for (yy, c, ty, xd) in ((1482.5, "cw", 1503.5, 2172), (1484.0, "ccw", 1505.2, 2171)):
        pipe([(X0 + 12, yy, 11), (xd, yy, 11), (xd, yy, 2.4), (xd, ty, 2.4), (2205, ty, 2.4), (2205, ty, 8)], 11,
             .4, c)                                                         # to the dry coolers along the pipe track
        for x0 in UNITS:
            rod((x0 + 3.7, yy, 11), (x0 + 3.7, yy, 3), .2, c, seg=8)
            rod((x0 + 3.7, yy, 3), (x0 + 3.7, 1477.7, 3), .2, c, seg=8)
    pipe([(X0 + 12, 1485.4, 12.5), (2174, 1485.4, 12.5), (2174, 1485.4, 4), (2174, 1498.6, 4)], 12.5, .35,
         "hydrogen")                                                        # H2 header out to the dryer line
    for x in [X0 + 11 + 20 * k for k in range(8)]:
        rod((x, 1483.2, 10.4), (x, 1483.2, EAVE - .6), .08, "steel", seg=4)                  # pipe hangers
        box(x - .3, x + .3, 1481.8, 1486.2, 10.2, 10.6, "steel")
    fuel.D = False
    people = fuel.new_item("OPT_H2", "H2 22 hall: technicians", (2030, 2110, 1478, 1490), (0, 6), area="K",
                           register=False)
    on(people)
    person(2034, 1483, .55, 3.14)
    person(2076, 1486, .55, 0)
    person(2097, 1481, .55, 1.57, vest="hivis_o")


def pipe_track():
    """Pipe track under the dry coolers to the dryer and compressors, with a covered cable trench beside it."""
    it = fuel.new_item("OPT_H2", "H2 pipe track and cable trench, hall -> dryer / compressors (N2, instrument air, "
                       "cooling water, control / fibre)", (2170, 2240, 1493, 1509), (0, 4), area="K",
                       sheet="typical (H2 hall)", register=False)
    on(it)
    fuel.D = True
    lines = ((1494.5, "pipe", .25), (1496.0, "pipe", .2))                     # N2, instrument air
    for (yy, c, r) in lines:
        rod((2170.6, yy, 2.4), (2238, yy, 2.4), r, c, seg=10)
    for x in range(2176, 2238, 12):
        box(x - .6, x + .6, 1493.8, 1497, 0, 2.15, "concrete")
        box(x - .6, x + .6, 1503, 1505.8, 0, 2.0, "concrete")                     # under the cooling-water pair
    box(2170.6, 2238, 1507, 1509, 0, .25, "grating")                                    # cable trench cover
    fuel.D = False


def build():
    bld = hollow()
    shell(bld)
    for x0 in UNITS:
        unit(x0)
        rectifier_and_dc(x0)
    electrical_room()
    cooling_and_people()
    pipe_track()
    return 1
