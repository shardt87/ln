"""Carbon capture audit pass (typical, not engineered).

Audit findings and what this adds:
- supply: the D5 bay carries two 230 kV circuits to the CCS, but only one cable was drawn, to T-2. The
  second circuit now runs in the same cable bank and branches to T-1. Each transformer gets a 230 kV cable
  termination structure (potheads, arresters, jumpers to the bushings). A firewall stands between the two
  transformers (10 ft apart, NFPA 850).
- distribution: the CCS loads were fed by automatic buried feeders chained from one piece of equipment to the
  next. They are now fed radially from the CCS MV / VFD building by a cable-tray system: a riser on the
  building's west wall, a tray along the CCS pipe rack (EL 30) with a drop to every train's DCC pumps,
  rich / lean skid, water-wash pumps and absorber; a second tray along y 1100 to the reboilers, strippers,
  reclaimer, storage, carbon filter and export compressor. The CO2 compressors (3 x ~19 MW) are fed at 13.8 kV
  by their own buried bank from the VFD building.
- absorbers: bed manways at every packed bed (access by the caged ladder and its rest platforms; no stair
  tower, at the user's direction, as for the filter houses), an intercooler skid with draw-off and return lines, an instrument / lighting tray riser up the
  shell with junction boxes and platform lights, a stack platform with CEMS sample ports, aviation obstruction
  lights (FAA: structures above 200 ft) and lightning protection.
- strippers: manways, overhead condenser over the reflux drum, tray riser with junction boxes, obstruction
  lights and lightning protection.
- booster fans: the ~16 MW motor's MV terminal box, cable riser and lube-oil console on the fan housing.
- buildings: MV / VFD building rooftop HVAC units, doors with landings; CO2 compression building roof
  ventilators and doors, and the dehydration skid (two molecular-sieve towers and a regeneration heater) east
  of it.
"""
import math

import fuel
from fuel import box, rod, find, on, pipe

SHEET = "typical (CCS audit)"
L = "OPT_CCS_ROUTES"


def routes(add_route):
    r = lambda t, pts, lay=L: add_route(t, pts, layer=lay, sheet=SHEET)
    # second 230 kV circuit from D5: shares the bank with the first, branches to T-1
    r("hv_cable", [(1890, 170), (1890, 262), (1520, 262), (1520, 1038), (1280, 1038), (1230, 1038), (1230, 1030)])
    # CCS cable trays from the MV / VFD building (riser on its west wall)
    # LV / control tray from the MV / VFD building riser onto the top of the CCS pipe rack (EL 27.3, above the
    # upper-tier pipes), drops off the rack to each train's loads
    r("lv_tray", [(1058, 1030), (1046, 1030), (1046, 1133), (590, 1133)])
    for dx in (0, 160, 320):
        r("lv_tray", [(590 + dx, 1133), (590 + dx, 1062)])               # DCC pumps, on to the DCC (junction box)
        r("lv_tray", [(682 + dx, 1133), (682 + dx, 1101)])               # rich / lean skid
        r("lv_tray", [(700 + dx, 1133), (700 + dx, 1220)])               # water-wash pumps, intercooler
        r("lv_tray", [(650 + dx, 1133), (650 + dx, 1188)])               # absorber: junction box, shell riser
    # regeneration area: buried duct banks with stub-ups (no tall tray posts in the process yard)
    b = lambda pts: add_route("mvlv_cable", pts, layer=L, sheet=SHEET)
    b([(1062, 1050), (1062, 1100), (1306, 1100)])
    for x in (1070, 1120, 1170):
        b([(x, 1100), (x, 1104)])                                         # reboilers
    for x in (1095, 1145):
        b([(x, 1100), (x, 1163)])                                         # strippers (between the shells)
    b([(1235, 1100), (1235, 1104)])                                       # reclaimer
    b([(1306, 1100), (1306, 1229)])                                       # storage, carbon filter, compression
    b([(1306, 1195), (1302, 1195)])                                       # storage pumps
    b([(1306, 1190), (1358, 1190)])                                       # export compressor
    b([(1306, 1229), (1446, 1229), (1446, 1238)])                         # dehydration skid
    # 13.8 kV to the CO2 compressor motors (buried bank from the VFD building)
    r("mvlv_cable", [(1200, 1046), (1307, 1046), (1307, 1240), (1310, 1240)])


def absorber(t, dx):
    gx, cy, R = 630 + dx, 1220.0, 31.0
    it = find(f"Absorber {t}")
    on(it)
    fuel.D = True
    # bed manways (one each side) at every packed bed and the wash section
    for z in (55, 100, 145, 190, 235):
        for a in (math.radians(150), math.radians(330)):
            ca, sa = math.cos(a), math.sin(a)
            rod((gx + R * ca, cy + R * sa, z), (gx + (R + 2.2) * ca, cy + (R + 2.2) * sa, z), 1.3, "ccs", seg=16)
            rod((gx + (R + 2.2) * ca, cy + (R + 2.2) * sa, z), (gx + (R + 2.5) * ca, cy + (R + 2.5) * sa, z), 1.6,
                "steel", seg=16)
    # instrument / lighting tray riser on the shell (from the junction box at the tray drop, EL 30)
    rx, ry = gx + 15.5, cy - 27.3
    box(rx - 1.2, rx + 1.2, ry - 1.6, ry - .4, 26, 32, "panel")                    # junction box at the drop
    for s in (-.8, .8):
        box(rx + s - .06, rx + s + .06, ry - .9, ry - .7, 32, 251, "pipe")
    for z in range(34, 251, 2):
        box(rx - .8, rx + .8, ry - .85, ry - .75, z - .05, z + .05, "pipe")
    for z in (60, 130, 200, 250):
        box(rx - 2.2, rx - 1.2, ry - 1.4, ry - .5, z + 1.5, z + 3.5, "panel")         # platform JB / lighting panel
        for a in range(0, 360, 60):                                                   # platform lights on posts
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            px, py = gx + 33.6 * ca, cy + 33.6 * sa
            rod((px, py, z + 1.2), (px, py, z + 5.5), .08, "steel", seg=4)
            box(px - .4, px + .4, py - .4, py + .4, z + 5.5, z + 6.1, "lamp")
    # stack platform with CEMS sample ports, aviation lights, lightning protection
    rod((gx, cy, 290), (gx, cy, 291), 13, "grating", seg=32)
    for a in range(0, 360, 30):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        rod((gx + 12.8 * ca, cy + 12.8 * sa, 291), (gx + 12.8 * ca, cy + 12.8 * sa, 294.5), .07, "rail", seg=4)
    for a in (0, 90, 180):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        rod((gx + 9 * ca, cy + 9 * sa, 293), (gx + 10.4 * ca, cy + 10.4 * sa, 293), .35, "steel", seg=10)   # ports
    box(gx + 9.5, gx + 11.5, cy - 1, cy + 1, 291, 294, "panel")                     # probe / analyser box
    for (z, rr) in ((312.5, 9.2), (156, 31.3)):                                     # obstruction lights
        for a in (0, 120, 240):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            box(gx + rr * ca - .45, gx + rr * ca + .45, cy + rr * sa - .45, cy + rr * sa + .45, z, z + .9, "red")
    for a in (45, 165, 285):                                                         # air terminals on the stack
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        rod((gx + 8.6 * ca, cy + 8.6 * sa, 313), (gx + 8.6 * ca, cy + 8.6 * sa, 317), .08, "copper", seg=4)
    a = math.radians(105)
    rod((gx + 9.1 * math.cos(a), cy + 9.1 * math.sin(a), 313), (gx + 9.1 * math.cos(a), cy + 9.1 * math.sin(a), 268),
        .07, "copper", seg=4)
    rod((gx + 31.1 * math.cos(a), cy + 31.1 * math.sin(a), 262), (gx + 31.1 * math.cos(a), cy + 31.1 * math.sin(a), 0),
        .07, "copper", seg=4)                                                         # down conductor
    fuel.D = False
    # intercooler skid: draw-off from the shell, pumps, plate exchanger, return
    ic = fuel.new_item("OPT_CCS", f"Absorber {t} intercooler (pumps + plate exchanger)", (679 + dx, 701 + dx, 1222, 1250),
                       (0, 12), area="G", basis="typical", sheet=SHEET,
                       info="Draws semi-rich amine off the middle bed, cools it against cooling water and returns it "
                            "one bed lower; raises CO2 loading and cuts solvent rate (typical for large absorbers).")
    box(679 + dx, 701 + dx, 1222, 1250, 0, .6, "concrete")
    box(682 + dx, 690 + dx, 1225, 1247, .6, 10, "bundle")                             # plate exchanger frame
    box(681.5 + dx, 690.5 + dx, 1224.5, 1225.2, .6, 11, "steel")
    box(681.5 + dx, 690.5 + dx, 1246.8, 1247.5, .6, 11, "steel")
    for y in (1229, 1241):
        rod((693 + dx, y, 2.2), (697 + dx, y, 2.2), 1.1, "pump", seg=12)
        rod((697.2 + dx, y, 2.2), (700.3 + dx, y, 2.2), 1.0, "motor", seg=12)
    pipe([(660.6 + dx, 1226, 120), (695 + dx, 1226, 120), (695 + dx, 1229, 120), (695 + dx, 1229, 3.4)], 120, .55, "pipe")
    pipe([(661 + dx, 1232, 112), (686 + dx, 1232, 112), (686 + dx, 1232, 10)], 112, .55, "pipe")
    ic["wiring"] = ["LV power 480 V: Cu XHHW-2, Type TC-ER (UL 1277) (intercooler pumps)",
                    "Control 120 V AC / 125 V DC: 14 AWG multiconductor, Type TC-ER (ICEA S-73-532)",
                    "Instrumentation 4-20 mA / HART: shielded pairs / triads, Type TC-ER / PLTC (flow, temperature)",
                    "Grounding: bare Cu 4/0 to the station grid"]


def stripper(t, cx):
    it = find(f"STR-{t}:")
    on(it)
    cy, R = 1187.5, 22.5
    fuel.D = True
    for z in (40, 90, 140, 180):
        for a in (math.radians(200), math.radians(340)):
            ca, sa = math.cos(a), math.sin(a)
            rod((cx + R * ca, cy + R * sa, z), (cx + (R + 2) * ca, cy + (R + 2) * sa, z), 1.2, "ccs", seg=14)
            rod((cx + (R + 2) * ca, cy + (R + 2) * sa, z), (cx + (R + 2.3) * ca, cy + (R + 2.3) * sa, z), 1.5, "steel", seg=14)
    # tray riser on the south face from the drop between the shells, junction boxes at the platforms
    sxr = cx + (24 if t != "C" else -24)
    rx = cx + R * math.cos(math.radians(250 if t != "C" else 290))
    ry = cy + R * math.sin(math.radians(250 if t != "C" else 290)) - .8
    for s in (-.7, .7):
        box(rx + s - .06, rx + s + .06, ry - .1, ry + .1, 30, 152, "pipe")
    for z in range(32, 152, 2):
        box(rx - .7, rx + .7, ry - .05, ry + .05, z - .05, z + .05, "pipe")
    for z in (70, 150):
        box(rx - 1, rx + 1, ry - 1, ry - .2, z + 1.5, z + 3.5, "panel")
    for a in (0, 120, 240):                                                          # obstruction lights
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        box(cx + 4.2 * ca - .4, cx + 4.2 * ca + .4, cy + 4.2 * sa - .4, cy + 4.2 * sa + .4, 207, 207.8, "red")
    rod((cx, cy, 207), (cx, cy, 211), .08, "copper", seg=4)
    a = math.radians(120)
    rod((cx + 22.6 * math.cos(a), cy + 22.6 * math.sin(a), 200), (cx + 22.6 * math.cos(a), cy + 22.6 * math.sin(a), 0),
        .07, "copper", seg=4)
    # overhead condenser over the reflux drum, on four posts
    for (x, y) in ((cx - 13, 1153.8), (cx + 3, 1153.8), (cx - 13, 1161.2), (cx + 3, 1161.2)):
        box(x - .3, x + .3, y - .3, y + .3, 0, 9.8, "steel")
    box(cx - 13.5, cx + 3.5, 1153.4, 1161.6, 9.6, 9.9, "steel")
    rod((cx - 14, 1157.5, 12), (cx + 4, 1157.5, 12), 2.1, "tank", seg=16)
    for x in (cx - 14, cx + 4):
        rod((x - .2, 1157.5, 12), (x + .2, 1157.5, 12), 2.4, "steel", seg=16)
    rod((cx + 1, 1157.5, 14.1), (cx + 1, 1157.5, 16), .6, "pipe", seg=10)
    fuel.D = False


def booster_fan(t, dx):
    on(find(f"BF-{t}:"))
    fuel.D = True
    box(655 + dx, 657.5 + dx, 1008, 1016, 8, 14, "panel")                           # MV motor terminal box
    rod((656.2 + dx, 1012, 0), (656.2 + dx, 1012, 8), .45, "steel", seg=10)          # cable riser from the bank
    box(655 + dx, 660 + dx, 1020, 1030, 0, 5, "tank")                               # lube-oil console
    box(655 + dx, 660 + dx, 1020, 1030, 5, 5.3, "steel")
    rod((657.5 + dx, 1025, 5.3), (657.5 + dx, 1025, 7.5), .25, "steel", seg=8)
    box(655 + dx, 656 + dx, 997, 1003, 10, 18, "louvre")                             # motor air cooler intake
    fuel.D = False


def mv_building():
    it = find("CCS MV switchgear building")
    on(it)
    fuel.D = True
    for x in (1080, 1120, 1160):                                                     # rooftop HVAC units
        box(x, x + 14, 1005, 1015, 24, 28.5, "machine")
        rod((x + 4, 1010, 28.5), (x + 4, 1010, 29), 2.4, "fan", seg=14)
        rod((x + 10, 1010, 28.5), (x + 10, 1010, 29), 2.4, "fan", seg=14)
    for x in (1100, 1170):                                                           # doors with landings, south face
        box(x, x + 4, 984.8, 985, 0, 8, "door")
        box(x - 1, x + 5, 980, 985, 0, .4, "concrete")
    box(1130, 1144, 1050, 1050.2, 0, 14, "rollup")                                 # equipment door, north face
    fuel.D = False


def transformers():
    fw = fuel.new_item("OPT_CCS", "CCS T-1 / T-2 firewall", (1253, 1257, 983, 1032), (0, 40), area="G", basis="typical",
                       register=False, sheet=SHEET,
                       info="Reinforced-concrete firewall between the two 230/13.8 kV transformers (10 ft apart), "
                            "extending past the tanks and conservators (NFPA 850).")
    box(1253, 1257, 983, 1032, 0, 40, "concrete")
    for x in (1230, 1280):
        it = fuel.new_item("OPT_CCS", f"CCS 230 kV cable termination structure ({'T-1' if x < 1250 else 'T-2'})",
                           (x - 4.5, x + 4.5, 1033, 1041), (0, 27), area="G", basis="typical", register=False, sheet=SHEET,
                           info="The 230 kV XLPE cable rises from the bank to outdoor sealing ends with arresters; "
                                "jumpers drop to the transformer HV bushings.")
        import cable_install

        def jumper(k, p0, x=x):
            p2 = (x, 1014.7 - 7.2 * (2 - k), 35.3)                                    # to the HV bushing tops
            pts = [tuple((1 - s) ** 2 * p0[j] + 2 * (1 - s) * s * ((p0[j] + p2[j]) / 2 - (1.5 if j == 2 else 0)) + s * s * p2[j]
                         for j in range(3)) for s in [i / 8 for i in range(9)]]
            for a_, b_ in zip(pts, pts[1:]):
                rod(a_, b_, .14, "conductor", seg=6)
        cable_install.hv_termination(x, 1037, 0, 1, top=jumper)


def compression():
    it = find("CO2 compression")
    on(it)
    fuel.D = True
    for x in range(1330, 1430, 25):                                                  # roof ventilators
        rod((x, 1287, 35), (x, 1287, 37.5), 2, "machine", seg=14)
        rod((x, 1287, 37.5), (x, 1287, 38.3), 2.6, "roof", r2=.6, seg=14)
    for x in (1335, 1385):                                                           # roll-up doors, south face
        box(x, x + 16, 1229.8, 1230, 0, 18, "rollup")
    box(1415, 1419, 1229.8, 1230, 0, 8, "door")
    fuel.D = False
    dh = fuel.new_item("OPT_CCS", "CO2 dehydration: molecular-sieve towers and regeneration heater", (1438, 1458, 1240, 1300),
                       (0, 40), area="G", basis="typical", sheet=SHEET,
                       info="Dries the compressed CO2 to pipeline specification between compression stages: two "
                            "adsorber towers (one drying, one regenerating) and an electric regeneration-gas heater.")
    box(1438, 1458, 1240, 1300, 0, .6, "concrete")
    for y in (1252, 1270):
        rod((1446, y, .6), (1446, y, 36), 4, "tank", seg=20)
        rod((1446, y, 36), (1446, y, 38.5), 4, "tank", r2=1.2, seg=20)
        for z in (12, 24):
            rod((1446, y, z - .15), (1446, y, z + .15), 4.25, "steel", seg=20)
    box(1440, 1456, 1285, 1296, .6, 9, "machine")                                   # regeneration heater
    pipe([(1446, 1256, 38), (1446, 1266, 38)], 38, .5, "pipe")
    pipe([(1442, 1252, 6), (1436, 1252, 6)], 6, .6, "pipe")
    pipe([(1442, 1270, 6), (1436, 1270, 6)], 6, .6, "pipe")
    dh["wiring"] = ["LV power 480 V: Cu XHHW-2, Type TC-ER (UL 1277) (regeneration heater, valve actuators)",
                    "Control 120 V AC / 125 V DC: 14 AWG multiconductor, Type TC-ER (switching-valve sequence)",
                    "Instrumentation 4-20 mA / HART: shielded pairs, Type PLTC (dew point, pressure, temperature)",
                    "Grounding: bare Cu 4/0 to the station grid"]


def storage():
    """Solvent (amine) and NaOH storage as built: bunded tank farm sized for the largest tank plus rain,
    cone roofs with vents, caged ladders and roof handrails, nozzles, a transfer-pump pad, truck unloading
    station and the lines to the CCS rack."""
    it = find("Solvent + NaOH storage")
    on(it)
    fuel.D = True
    # bund: 4 ft concrete wall round the slab, sump, stair over the wall
    for (a0, a1, b0, b1) in ((1210, 1300, 1165, 1166), (1210, 1300, 1224, 1225), (1210, 1211, 1165, 1225), (1299, 1300, 1165, 1225)):
        box(a0, a1, b0, b1, 3, 7, "concrete")
    box(1292, 1296, 1167, 1171, 1.5, 3, "concrete")                                   # bund sump
    box(1292.3, 1295.7, 1167.3, 1170.7, 2.9, 3.05, "grating")
    for k in range(5):                                                                 # step-over stair, west wall
        box(1205 + k, 1206 + k, 1192, 1196, k * 1.4, k * 1.4 + .3, "grating")
        box(1211 + k, 1212 + k, 1192, 1196, 7 - k * 1.4, 7.3 - k * 1.4, "grating")
    tanks = [(1228, 1185, 11, "amine"), (1270, 1185, 11, "amine"), (1228, 1210, 10, "NaOH"), (1285, 1212, 10, "NaOH")]
    for (cx, cy, r, kind) in tanks:
        rod((cx, cy, 30), (cx, cy, 32.5), r, "tank", r2=1.2, seg=28)                  # cone roof
        rod((cx, cy, 32.5), (cx, cy, 34), .6, "steel", seg=10)                         # vent
        rod((cx, cy, 34), (cx, cy, 34.4), 1.1, "steel", seg=10)
        for z in (10, 20):                                                             # shell weld seams / wind girders
            rod((cx, cy, z - .1), (cx, cy, z + .1), r + .08, "steel", seg=28)
        for k in range(12):                                                            # roof handrail (half ring)
            a0, a1 = math.pi * k / 12, math.pi * (k + 1) / 12
            rod((cx + (r - .5) * math.cos(a0), cy + (r - .5) * math.sin(a0), 33.2),
                (cx + (r - .5) * math.cos(a1), cy + (r - .5) * math.sin(a1), 33.2), .06, "rail", seg=4)
        a = math.radians(200)                                                          # caged ladder
        lx, ly = cx + (r + .9) * math.cos(a), cy + (r + .9) * math.sin(a)
        for s_ in (-.7, .7):
            rod((lx - s_ * math.sin(a), ly + s_ * math.cos(a), 3), (lx - s_ * math.sin(a), ly + s_ * math.cos(a), 33.5), .07, "rail", seg=4)
        tx, ty = -math.sin(a), math.cos(a)
        for z in range(4, 33):                                                         # rungs
            rod((lx - .7 * tx, ly - .7 * ty, z), (lx + .7 * tx, ly + .7 * ty, z), .04, "rail", seg=4)
        for z in range(10, 33, 3):                                                     # cage hoops
            hp = [(lx + 1.1 * tx * math.cos(u) + 1.1 * math.cos(a) * math.sin(u), ly + 1.1 * ty * math.cos(u)
                   + 1.1 * math.sin(a) * math.sin(u), z) for u in [math.pi * i / 6 for i in range(7)]]
            for p_, q_ in zip(hp, hp[1:]):
                rod(p_, q_, .04, "rail", seg=4)
        box(cx + r * .7 - .9, cx + r * .7 + .9, cy - r * .7 - .9, cy - r * .7 + .9, 3, 6, "steel")   # shell manway
        rod((cx, cy - r, 4), (cx, cy - r - 2, 4), .45, "pipe", seg=10)                # outlet nozzle
        box(cx - .6, cx + .6, cy - r - 2.6, cy - r - 2, 3.4, 4.6, "steel")             # tank valve
        box(cx + r - .1, cx + r + .3, cy - .5, cy + .5, 6, 26, "steel")                # level gauge board
        box(cx + r + .3, cx + r + .9, cy - .4, cy + .4, 15, 17, "panel")               # radar level transmitter box
    # transfer-pump pad inside the bund (south-east corner) and its lines
    box(1288, 1298, 1196, 1206, 3, 3.5, "concrete")
    for y in (1199, 1203):
        rod((1289.5, y, 4.8), (1293, y, 4.8), .8, "pump", seg=12)
        rod((1293.2, y, 4.8), (1296.5, y, 4.8), .75, "motor", seg=12)
    box(1296.8, 1298.6, 1197, 1205, 3.5, 8, "panel")                                   # local control station
    pipe([(1228, 1172, 4), (1228, 1170, 4), (1290, 1170, 4), (1290, 1199, 4.8)], 4, .45, "pipe")
    pipe([(1270, 1172, 4), (1270, 1170, 4)], 4, .45, "pipe")
    pipe([(1228, 1199, 4), (1240, 1199, 4), (1240, 1203, 4), (1289, 1203, 4.8)], 4, .4, "waterline")
    # truck unloading station outside the east wall: hose connections, drip tray, safety shower
    box(1301, 1309, 1180, 1192, 0, .4, "concrete")
    box(1301.5, 1303, 1182, 1190, .4, 4.5, "steel")
    for y in (1184, 1188):
        rod((1303, y, 3.5), (1305, y, 3.5), .35, "pipe", seg=8)
        box(1305, 1305.6, y - .5, y + .5, 3, 4, "red")
    pipe([(1301.5, 1186, 3.5), (1299, 1186, 3.5), (1299, 1186, 8), (1270, 1186, 8), (1270, 1196, 8)], 8, .4, "pipe")
    rod((1307.5, 1196, 0), (1307.5, 1196, 8), .15, "safety", seg=8)                   # safety shower / eyewash
    rod((1307.5, 1196, 8), (1307.5, 1197.5, 8.3), .6, "safety", r2=.9, seg=10)
    # lines from the pump discharge west to the CCS rack (on sleepers, then up)
    pipe([(1290, 1204, 6), (1290, 1160, 6), (1046, 1160, 6), (1046, 1135, 6), (1046, 1135, 18.5)], 6, .4, "pipe")
    for x in range(1060, 1290, 25):
        box(x - .4, x + .4, 1158.8, 1161.2, 0, 5.6, "steel")                           # pipe sleepers
    fuel.D = False


def flue_ducts():
    """HRSG stack breeching to the DCC: external stiffener frames every 8 ft, insulation cladding seams,
    fabric expansion joints at both ends, access doors, low-point drains, a sample / test-port platform, and
    portal support bents with bracing and sliding / guided shoes."""
    for k, t in enumerate("ABC"):
        dx = 160 * k
        it = find(f"Flue-gas duct, HRSG {k + 1} to DCC-{t}")
        on(it)
        x0, x1, z0, z1 = 621 + dx, 639 + dx, 44, 62
        fuel.D = True
        for y in range(832, 980, 8):                                                   # stiffener frames
            box(x0 - .35, x0, y - .25, y + .25, z0 - .35, z1 + .35, "steel")
            box(x1, x1 + .35, y - .25, y + .25, z0 - .35, z1 + .35, "steel")
            box(x0 - .35, x1 + .35, y - .25, y + .25, z1, z1 + .35, "steel")
            box(x0 - .35, x1 + .35, y - .25, y + .25, z0 - .35, z0, "steel")
        for y in range(836, 980, 16):                                                  # cladding seams
            box(x0 - .05, x1 + .05, y - .04, y + .04, z1 - .05, z1 + .05, "machine")
        for y in (829, 981):                                                           # fabric expansion joints
            box(x0 - .7, x1 + .7, y - 1.2, y + 1.2, z0 - .7, z1 + .7, "fan")
            box(x0 - .9, x1 + .9, y - 1.6, y - 1.2, z0 - .9, z1 + .9, "steel")
            box(x0 - .9, x1 + .9, y + 1.2, y + 1.6, z0 - .9, z1 + .9, "steel")
        for y in (872, 932):                                                           # access doors (west face)
            box(x0 - .45, x0 - .35, y - 1.5, y + 1.5, 48, 54, "door")
            for zz in (49, 53):
                box(x0 - .6, x0 - .45, y + 1.1, y + 1.4, zz, zz + .4, "steel")
        for y in (900, 960):                                                           # low-point drains
            rod((x0 + 9, y, z0), (x0 + 9, y, z0 - 3), .25, "pipe", seg=8)
            box(x0 + 8.6, x0 + 9.4, y - .4, y + .4, z0 - 3.8, z0 - 3, "steel")
        # test-port platform on the east face near the DCC end (south of the ring road, so the ladder lands on
        # clear grade beside the duct, not in the road), rail, ports and a caged ladder
        box(x1 + .4, x1 + 5, 948, 964, z0 + 3, z0 + 3.3, "grating")
        for yy in (948, 964):
            rod((x1 + .4, yy, z0 + 6.8), (x1 + 5, yy, z0 + 6.8), .07, "rail", seg=4)
        rod((x1 + 5, 948, z0 + 6.8), (x1 + 5, 964, z0 + 6.8), .07, "rail", seg=4)
        for y in (952, 956, 960):
            rod((x1, y, z0 + 8), (x1 + 1.2, y, z0 + 8), .4, "steel", seg=10)
        for s_ in (-.7, .7):
            rod((x1 + 5.6, 956 + s_, 0), (x1 + 5.6, 956 + s_, z0 + 3.3), .07, "rail", seg=4)
        for zz in range(1, int(z0 + 3)):                                               # rungs
            rod((x1 + 5.6, 955.3, zz), (x1 + 5.6, 956.7, zz), .04, "rail", seg=4)
        for zz in range(8, int(z0 + 3), 3):                                            # cage hoops
            hp = [(x1 + 5.6 + 1.1 * math.sin(u), 956 - 1.1 * math.cos(u), zz) for u in [math.pi * i / 6 for i in range(7)]]
            for p_, q_ in zip(hp, hp[1:]):
                rod(p_, q_, .04, "rail", seg=4)
        fuel.D = False
        # support bents: replace the two thin posts with braced portal frames, shoes under the duct
        fuel.G["parts"][:] = [p for p in fuel.G["parts"] if not (p["item"] == it["id"] and p["kind"] == "box" and p["color"] == "steel"
                                                                and p["min"][2] == 0)]
        for y in (870, 937):                                                          # clear of the ring road (y 900-930)
            for xc in (x0 - 2, x1 + 2):
                box(xc - .6, xc + .6, y - .6, y + .6, 0, z0 - 1.5, "steel")
                box(xc - 1.4, xc + 1.4, y - 1.4, y + 1.4, 0, .4, "concrete")                # pier cap
            box(x0 - 2.8, x1 + 2.8, y - .7, y + .7, z0 - 1.5, z0 - .3, "steel")           # cross beam
            fuel.D = True
            for (xa, xb) in ((x0 - 2, x1 + 2), (x1 + 2, x0 - 2)):
                rod((xa, y, 4), (xb, y, z0 - 2), .22, "steel", seg=6)                      # X bracing
            for xs in (x0 + 3, x1 - 3):
                box(xs - .8, xs + .8, y - .8, y + .8, z0 - .3, z0, "machine")               # sliding shoes
            fuel.D = False


def build():
    for i, dx in enumerate((0, 160, 320)):
        t = "ABC"[i]
        absorber(t, dx)
        booster_fan(t, dx)
    for t, cx in zip("ABC", (1070, 1120, 1170)):
        stripper(t, cx)
    mv_building()
    transformers()
    compression()
    storage()
    flue_ducts()
