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
    r("lv_tray", [(1058, 1030), (1046, 1030), (1046, 1110), (590, 1110)])
    r("control_tray", [(1058, 1040), (1043, 1040), (1043, 1100), (1306, 1100)])
    for dx in (0, 160, 320):
        r("lv_tray", [(590 + dx, 1110), (590 + dx, 1062)])               # DCC pumps, on to the DCC (junction box)
        r("lv_tray", [(682 + dx, 1110), (682 + dx, 1101)])               # rich / lean skid
        r("lv_tray", [(700 + dx, 1110), (700 + dx, 1220)])               # water-wash pumps, intercooler (over the rack)
        r("lv_tray", [(650 + dx, 1110), (650 + dx, 1188)])               # absorber: junction box, shell riser
    for x in (1070, 1120, 1170):
        r("control_tray", [(x, 1100), (x, 1103.5)])                       # reboilers
    for x in (1095, 1145):
        r("control_tray", [(x, 1100), (x, 1161)])                         # strippers (between the shells)
    r("control_tray", [(1235, 1100), (1235, 1103.5)])                     # reclaimer
    r("control_tray", [(1306, 1100), (1306, 1250)])                       # storage, carbon filter, compression
    r("control_tray", [(1306, 1190), (1358, 1190)])                       # export compressor
    r("control_tray", [(1306, 1227.5), (1448, 1227.5), (1448, 1238)])     # dehydration skid
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
                           (x - 4, x + 4, 1033, 1041), (0, 26), area="G", basis="typical", register=False, sheet=SHEET,
                           info="The 230 kV XLPE cable rises from the bank to outdoor sealing ends with arresters; "
                                "jumpers drop to the transformer HV bushings.")
        box(x - 4, x + 4, 1033, 1041, 0, .6, "concrete")
        for (ddx, ddy) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
            rod((x + ddx, 1037 + ddy, .6), (x + ddx, 1037 + ddy, 18), .35, "steel", seg=6)
        box(x - 3.6, x + 3.6, 1033.4, 1040.6, 17.6, 18.2, "steel")
        for k, ph in enumerate((-2.4, 0, 2.4)):
            rod((x + ph, 1037, -1.5), (x + ph, 1037, 18.2), .25, "cable_tc", seg=8)
            rod((x + ph, 1037, 18.2), (x + ph, 1037, 24.5), .55, "insulator", r2=.3, seg=10)
            # jumper to the HV bushing tops (one row along y on the tank centreline, EL 35)
            p0, p2 = (x + ph, 1037, 24.6), (x, 1014.7 - 7.2 * (2 - k), 35.3)       # to the bushing tops
            pts = [tuple((1 - s) ** 2 * p0[j] + 2 * (1 - s) * s * ((p0[j] + p2[j]) / 2 - (1.5 if j == 2 else 0)) + s * s * p2[j]
                         for j in range(3)) for s in [i / 8 for i in range(9)]]
            for a_, b_ in zip(pts, pts[1:]):
                rod(a_, b_, .14, "conductor", seg=6)


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
