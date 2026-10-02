"""Coastal variant at LOD 3 (detail cycle 10): dressing and wiring for the LNG import terminal
(panel A) and the landfall valve station (panel B). Parts are attached to the item they dress,
so the clash check sees them as part of that item. All typical, not engineered.
"""
import math

SEA = -8.0
MV = "MV 13.8 kV: Southwire MV-105 shielded, 133% insulation, in the buried trench"
LV = "LV 480 V: Cu XHHW-2, Type TC-ER (UL 1277)"
LV_HAZ = "LV 480 V, Class I Div 2: Type MC-HL (Southwire ARMOR-X) with listed glands"
CTRL = "Control 120 V AC / 125 V DC: 14 AWG multiconductor, Type TC-ER"
INST_IS = "Instrumentation (intrinsically safe): 16 AWG shielded pairs, blue jacket, Type PLTC"
INST = "Instrumentation 4-20 mA / HART: 16 AWG shielded pairs, Type PLTC / ITC"
TCX = "Thermocouple extension: Type K (KX) shielded pairs"
DATA = "Data / DCS: single-mode fibre, orange jacket"
FA = "Fire and gas: FPLR shielded, red jacket (NEC 760)"
LIGHT = "Lighting and small power: Cu THHN/THWN-2 in conduit"
GND = "Grounding: bare Cu 4/0 to the terminal grid"
HV = "230 kV: XLPE cable from the plant switchyard, buried"
WIRING = {
    "1": [MV + " (in-tank pumps via the pump columns)", INST_IS + " (level, temperature, density)", TCX + " (tank floor / wall)",
          FA, GND],
    "2": [LV_HAZ, INST_IS, CTRL, GND],
    "3": [MV + " (send-out pump motors)", CTRL, INST_IS, FA, GND],
    "4": [MV + " (compressor motors)", LV_HAZ, CTRL, INST_IS, TCX, FA, GND],
    "5": [HV, MV, LV, CTRL, DATA, FA, GND],
    "6": [LV, CTRL, LIGHT, FA, DATA, GND],
    "7": [LV_HAZ, INST_IS, DATA + " (flow computers)", GND],
    "8": [MV + " (seawater pump motors)", CTRL, INST, GND],
    "9": [LV_HAZ + " (pilot ignition)", TCX + " (pilot flame)", INST_IS, GND],
    "10": [LV_HAZ + " (jetty lighting, heat tracing)", DATA + " (ship-shore link)", FA, GND],
    "11": [LV_HAZ + " (arm hydraulics, lighting)", CTRL + " (ERS / ESD)", INST_IS, DATA + " (ship-shore link, SIGTTO)",
           FA, GND],
    "12": [LV, INST_IS, DATA + " (SCADA)", "Cathodic protection: rectifier DC cable, HMWPE", GND],
}


def on(S, key=None, name=None):
    for it in S.items:
        if (key and it["key"] == key) or (name and it["name"].startswith(name)):
            S.cur = (it["id"], it["layer"])
            return it
    raise KeyError(key or name)


def person(S, x, y, z=0.0, vest="hivis"):
    S.rod((x, y, z), (x, y, z + 2.8), .32, "workwear", seg=8)
    S.rod((x, y, z + 2.8), (x, y, z + 4.6), .42, vest, seg=8)
    S.rod((x, y, z + 4.6), (x, y, z + 5.3), .3, "skin", seg=8)
    S.rod((x, y, z + 5.3), (x, y, z + 5.7), .36, "hardhat", seg=8)


def pickup(S, x, y, along="x"):
    if along == "x":
        S.box(x - 9, x + 9, y - 3.2, y + 3.2, 1.2, 4, "truck")
        S.box(x - 3, x + 3.5, y - 3, y + 3, 4, 6.4, "truck")
        S.box(x + 3.4, x + 3.6, y - 2.6, y + 2.6, 4.4, 6.1, "glass")
        for dx in (-6, 6):
            for dy in (-3, 3):
                S.rod((x + dx, y + dy - .4 * (dy > 0), 1.2), (x + dx, y + dy + .4 * (dy < 0), 1.2), 1.2, "fanhub", seg=12)
    else:
        S.box(x - 3.2, x + 3.2, y - 9, y + 9, 1.2, 4, "truck")
        S.box(x - 3, x + 3, y - 3, y + 3.5, 4, 6.4, "truck")
        S.box(x - 2.6, x + 2.6, y + 3.4, y + 3.6, 4.4, 6.1, "glass")
        for dy in (-6, 6):
            for dx in (-3, 3):
                S.rod((x + dx - .4 * (dx > 0), y + dy, 1.2), (x + dx + .4 * (dx < 0), y + dy, 1.2), 1.2, "fanhub", seg=12)


def detail_A(S, K):
    for it in S.items:
        if it["key"] in WIRING:
            it["wiring"] = WIRING[it["key"]]
    # 1 tank: water-curtain / deluge ring, roof handrail, level gauge housings, ID band, gas detectors
    t = on(S, "1")
    fp = K["1"]
    cx, cy, R = (fp[0] + fp[1]) / 2, (fp[2] + fp[3]) / 2, (fp[1] - fp[0]) / 2
    for z in (60, 132):
        for a in range(24):
            t0, t1 = a * math.pi / 12, (a + 1) * math.pi / 12
            S.rod((cx + (R + 1.6) * math.cos(t0), cy + (R + 1.6) * math.sin(t0), z),
                  (cx + (R + 1.6) * math.cos(t1), cy + (R + 1.6) * math.sin(t1), z), .45, "firewater", seg=8)
    for a in range(8):
        t0 = a * math.pi / 4 + .2
        S.rod((cx + (R + 1.6) * math.cos(t0), cy + (R + 1.6) * math.sin(t0), 5),
              (cx + (R + 1.6) * math.cos(t0), cy + (R + 1.6) * math.sin(t0), 132), .3, "firewater", seg=8)
    for (dx, dy) in ((-30, -16), (30, -16), (30, 16), (-30, 16)):
        S.rod((cx + dx, cy + dy, 159), (cx + dx, cy + dy, 162.5), .1, "rail", seg=4)
    for (ax, ay, bx, by) in ((-30, -16, 30, -16), (30, -16, 30, 16), (30, 16, -30, 16), (-30, 16, -30, -16)):
        S.rod((cx + ax, cy + ay, 162.5), (cx + bx, cy + by, 162.5), .08, "rail", seg=4)
    for k in range(2):                                                                 # level / temperature gauges
        S.box(cx - 26 + k * 6, cx - 22 + k * 6, cy + 10, cy + 14, 159, 164, "cabinet")
    S.box(cx - 40, cx + 40, cy - R - .3, cy - R, 100, 112, "sign")                      # tank ID band
    for a in range(6):
        t0 = a * math.pi / 3
        x, y = cx + (R + 12) * math.cos(t0), cy + (R + 12) * math.sin(t0)
        S.rod((x, y, 0), (x, y, 5), .1, "steel", seg=4)
        S.box(x - .4, x + .4, y - .4, y + .4, 5, 5.9, "amber")
    # 3 HP pumps: suction header and drops, discharge header, junction boxes, gas detectors
    on(S, "3")
    fp = K["3"]
    for j in range(2):
        y = fp[2] + 30 + j * 40
        S.rod((fp[0] + 10, y + 7, 8), (fp[1] - 10, y + 7, 8), .9, "lngpipe", seg=10)       # suction
        S.rod((fp[0] + 10, y - 7, 24), (fp[1] - 10, y - 7, 24), .8, "pipe", seg=10)        # discharge
        for i in range(3):
            x = fp[0] + 22 + i * 32
            S.rod((x, y + 7, 8), (x, y + 3, 8), .6, "lngpipe", seg=8)
            S.rod((x, y - 3, 24), (x, y - 7, 24), .55, "pipe", seg=8)
            S.box(x + 4, x + 6, y - 1, y + 1, 1, 5, "panel")
    for (x, y) in ((fp[0] + 8, fp[2] + 50), (fp[1] - 8, fp[2] + 50)):
        S.box(x - .4, x + .4, y - .4, y + .4, 6, 6.9, "amber")
    # 4 BOG building: louvres, roll-up door, roof vents
    on(S, "4")
    fp = K["4"]
    for k in range(6):
        S.box(fp[0] + 12 + k * 20, fp[0] + 20 + k * 20, fp[2] + 4.8, fp[2] + 5, 18, 26, "louvre")
    S.box(fp[0] + 4.8, fp[0] + 5, fp[2] + 20, fp[2] + 36, 0, 18, "rollup")
    for k in range(4):
        S.box(fp[0] + 20 + k * 30, fp[0] + 26 + k * 30, (fp[2] + fp[3] - 25) / 2 - 2, (fp[2] + fp[3] - 25) / 2 + 2, 42, 44,
              "louvre")
    # 5 substation e-house: doors, landings, HVAC
    on(S, "5")
    fp = K["5"]
    for xd in (fp[0] + 20, fp[0] + 100):
        S.box(xd, xd + 4, fp[3] - 45.2, fp[3] - 45, 4.5, 11.5, "door")
        S.box(xd - 1, xd + 5, fp[3] - 49, fp[3] - 45, 3.7, 4, "grating")
    for k in range(3):
        S.box(fp[0] + 30 + k * 30, fp[0] + 36 + k * 30, fp[3] - 32, fp[3] - 26, 20, 23, "machine")
    # 6 control building: entrance canopy, doors, HVAC, antenna mast, parked pickups
    on(S, "6")
    fp = K["6"]
    S.box(fp[0] + 30, fp[0] + 46, fp[2] - 1, fp[2] + 5, 10, 10.6, "roof")
    S.box(fp[0] + 35, fp[0] + 41, fp[2] + 4.7, fp[2] + 4.9, 0, 8, "door")
    for k in range(3):
        S.box(fp[0] + 15 + k * 20, fp[0] + 22 + k * 20, fp[2] + 25, fp[2] + 31, 23.5, 27, "machine")
    S.rod((fp[0] + 70, fp[3] - 34, 23.5), (fp[0] + 70, fp[3] - 34, 38), .2, "steel", seg=6)
    # 8 intake: travelling screens and trash rake on the deck
    on(S, "8")
    fp = K["8"]
    for k in range(3):
        y = fp[2] + 25 + k * 25
        S.box(fp[1] - 8, fp[1] - 4, y - 5, y + 5, 5, 22, "steel")
        S.box(fp[1] - 8.2, fp[1] - 3.8, y - 5.2, y + 5.2, 20, 22, "machine")
    S.box(fp[1] - 3, fp[1] - 1, fp[2] + 15, fp[3] - 15, 5, 7, "amber")                 # rake rail
    # 10 jetty: fire-water main, life-ring stands, signs
    on(S, "10")
    fp = K["10"]
    jx0, jx1, jy0, jy1 = fp
    S.rod((jx0 - 30, jy0 + 9, 14.5), (jx1, jy0 + 9, 14.5), .9, "firewater", seg=10)
    x = jx0 + 120
    while x < jx1:
        S.rod((x, jy1 - 1.2, 13), (x, jy1 - 1.2, 17), .12, "steel", seg=4)
        S.rod((x, jy1 - 1.2, 16), (x, jy1 - 1.6, 16), 1, "hivis_o", seg=12)
        x += 300
    S.box(jx0 - 20, jx0 - 12, jy0 + .1, jy0 + .3, 15, 19, "sign")
    S.box(jx0 - 20, jx0 - 12, jy0 + .05, jy0 + .1, 18, 19, "red")
    # 11 berth: ERS couplings on the arms, ESD stations, people
    on(S, "11")
    fp = K["11"]
    for i in range(4):
        y = fp[2] + 60 + 26 * i
        S.box(fp[1] + 10, fp[1] + 14, y - 1.6, y + 1.6, 50, 54, "red")                  # emergency release coupler
    for (x, y) in ((fp[0] + 8, fp[2] + 6), (fp[1] - 8, fp[3] - 6)):
        S.box(x - .6, x + .6, y - .6, y + .6, 16, 20, "red")
    for (x, y) in ((fp[1] - 30, fp[2] + 70), (fp[1] - 34, fp[2] + 96), (fp[0] + 26, fp[2] + 50)):
        person(S, x, y, 16, vest="hivis_o")
    # terminal people and vehicles (on the roads and at the control building)
    on(S, name="Terminal roads")
    for (x, y) in ((2700, 585), (3150, 575)):
        pickup(S, x, y, "x")
    for (x, y) in ((2640, 790), (2650, 792), (2900, 600), (3420, 812)):
        person(S, x, y, .32)


def detail_B(S, K):
    for it in S.items:
        if it["key"] in WIRING:
            it["wiring"] = WIRING[it["key"]]
    on(S, "12")
    fp = K["12"]
    ym = (fp[2] + fp[3]) / 2
    for x in (fp[0] + 70, fp[0] + 100):
        S.box(x - 1.5, x + 1.5, ym - 1.5, ym + 1.5, 12, 14, "panel")                    # ESD valve actuators
    S.box(fp[0] + 141, fp[0] + 143, fp[3] - 26, fp[3] - 22, 0, 6, "cabinet")             # CP rectifier
    S.rod((fp[0] + 150, fp[3] - 20, 40), (fp[0] + 153, fp[3] - 20, 40), 1.6, "lamp", seg=12)   # SCADA dish
    pickup(S, fp[0] + 30, fp[3] - 8, "x")
    person(S, fp[0] + 64, ym + 6, 0)
