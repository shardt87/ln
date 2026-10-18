"""Turbine hall interior electrical: the hall's own wire and cable, which the tray model does not draw (user review:
"the MC cable inside on the wall"). As in a real turbine hall, all typical, not engineered:
- lighting: a 480/277 V lighting panel LP-TH and a 45 kVA dry-type transformer on the north wall at the deck; MC
  branch runs along the roof purlins over each row of high-bay fixtures, a short MC drop to every fixture, and the
  row runs down the west-end columns to the wall run;
- wall runs: Type MC-HL (Southwire ARMOR-X) clipped along the inside of the crane-runway girders on both long walls,
  with a pull box at every column;
- at every column, MC down the column flange to the device: alternately a 480 V welding receptacle with a 120 V
  duplex, or a fire-alarm horn-strobe (red FPLR cable alongside) with a manual pull station at the stair columns;
- the bridge crane's runway conductor bar under the north girder, fed from a fused crane disconnect at the west end;
- exit / emergency lights over the deck stairs.
Every device sits on a column face, clear of the trays, ducts and machines.
"""
import fuel
from fuel import box, rod, find, new_item

COLS_X = [482 + 44 * k for k in range(15)]            # hall column lines (x), south wall y 404, north wall y 556
YS, YN = 405.6, 554.4                                 # MC / device plane, just off the column inner faces
ZG = 81.6                                             # wall run, under the crane-runway girder (EL 82-84)
STAIR_COLS = (702, 878)                               # columns beside the deck-stair openings
DUCTS = {"S": ((656, 696), (816, 856), (976, 1016)),   # GT inlet ducts through the south wall
         "N": ((617, 643), (777, 803), (937, 963))}    # GT exhaust ducts through the north wall
CRANE_X = (484, 542)                                  # bridge crane parked over the laydown bay (EL 84-96)


def deck(x):
    return 20.0 if x >= 560 else 0.0                  # laydown bay floor at EL 0 west of x 560


def _blocked(parts, x, y, z0, z1, pad=.45):
    """Is anything of the tray model within pad of a vertical drop at (x, y) between z0 and z1?"""
    for p in parts:
        lo, hi = (p["min"], p["max"]) if p["kind"] == "box" else (
            [min(p["a"][i], p["b"][i]) - p.get("r", 0) for i in range(3)],
            [max(p["a"][i], p["b"][i]) + p.get("r", 0) for i in range(3)])
        if lo[0] - pad < x < hi[0] + pad and lo[1] - pad < y < hi[1] + pad and lo[2] < z1 and hi[2] > z0:
            return True
    return False


def build():
    hall = find("Common turbine hall")
    tray = find("Cable trays and isolated")["id"]
    def yspan(p):
        return (p["min"][1], p["max"][1]) if p["kind"] == "box" else (min(p["a"][1], p["b"][1]), max(p["a"][1], p["b"][1]))
    tparts = [p for p in fuel.G["parts"] if p["item"] == tray and p["kind"] in ("box", "rod")
              and (yspan(p)[0] < 410 or yspan(p)[1] > 550)]          # the tray model along the two long walls
    lamps = [p for p in fuel.G["parts"] if p["item"] == hall["id"] and p["color"] == "lamp" and p["kind"] == "rod"]
    it = new_item(hall["layer"], "Turbine hall interior electrical: lighting, receptacles, fire alarm, crane bar",
                  [482, 1098, 405, 555], [0, 98], area=hall.get("area", "A"),
                  info="Lighting panel LP-TH and transformer, MC-HL wall and roof runs, welding and duplex receptacles, "
                       "fire-alarm horn-strobes and pull stations, crane runway conductor bar. Typical, not engineered.")
    it["wiring"] = ["LV 480 / 277 V lighting and 120 V receptacle branches: Type MC-HL (Southwire ARMOR-X), aluminium "
                    "armor, black PVC jacket, clipped to the girders, purlins and columns",
                    "480 V welding receptacles: Type MC-HL 4/C #6 AWG from LP-TH",
                    "Fire alarm: FPLR shielded, red jacket (NEC 760) to the horn-strobes and pull stations",
                    "Crane: 480 V runway conductor bar fed through a fused disconnect, Type MC-HL",
                    "Grounding: green-insulated equipment grounds in every MC cable"]
    n = 0
    # lighting panel and transformer on the north wall between the GT1 / GT2 exhaust ducts
    box(700, 705, 552.6, 554.6, 20, 27, "panel"); box(700.3, 704.7, 552.5, 552.6, 21, 26.5, "cabinet")
    box(707, 712, 551.6, 554.6, 20, 25, "xfmr")
    for x in (702.5, 709.5):
        rod((x, YN - .3, 27 if x < 706 else 25), (x, YN - .3, ZG), .09, "cable_mc", seg=6)
    n += 5
    # wall runs under both crane girders, pull box at every column
    for y in (YS, YN):
        rod((482, y, ZG), (1098, y, ZG), .09, "cable_mc", seg=6)
        rod((482, y, ZG - .35), (1098, y, ZG - .35), .07, "cable_fa", seg=6)
        for x in COLS_X:
            box(x - .6, x + .6, y - .25 if y > 500 else y - .15, y + .15 if y > 500 else y + .25, ZG - .8, ZG + .4, "panel")
            n += 1
        n += 2
    # column drops and devices, alternating receptacles and fire alarm
    for k, x in enumerate(COLS_X):
        for y, s in ((YS, 1), (YN, -1)):
            z0 = deck(x)
            for dx in ((x + 1.1, x - 1.1) if x < 1090 else (x - 1.1,)):   # beside the column flange, either side
                if not any(a <= dx <= b for a, b in DUCTS["S" if s > 0 else "N"]) and not _blocked(tparts, dx, y, z0, ZG):
                    break
            else:
                continue                                                    # a GT duct or a wall tray at this column

            if k % 2 == 0:                                                  # welding receptacle + duplex
                box(dx - .6, dx + .6, y - .2 if s < 0 else y, y + .2 if s > 0 else y, z0 + 3.2, z0 + 5.0, "panel")
                box(dx - .2, dx + .2, (y + .2 * s) - .08 if s > 0 else (y + .2 * s), (y + .2 * s) if s > 0 else (y + .2 * s) + .08,
                    z0 + 3.6, z0 + 4.4, "red")
                box(dx - .25, dx + .25, y - .12 if s < 0 else y, y + .12 if s > 0 else y, z0 + 2.2, z0 + 2.8, "panel")
                rod((dx, y, z0 + 5.0), (dx, y, ZG), .08, "cable_mc", seg=6)
                n += 4
            else:                                                           # fire alarm horn-strobe (+ pull station)
                box(dx - .3, dx + .3, y - .25 if s < 0 else y, y + .25 if s > 0 else y, z0 + 9.5, z0 + 10.3, "red")
                box(dx - .22, dx + .22, (y + .25 * s) - .02 if s > 0 else (y + .25 * s), (y + .25 * s) if s > 0 else (y + .25 * s) + .02,
                    z0 + 9.6, z0 + 9.8, "lamp")                                # strobe lens
                rod((dx, y, z0 + 10.3), (dx, y, ZG - .35), .06, "cable_fa", seg=6)
                n += 3
                if x in STAIR_COLS or x == 570:
                    box(dx - .2, dx + .2, y - .15 if s < 0 else y, y + .15 if s > 0 else y, z0 + 3.8, z0 + 4.4, "red")
                    rod((dx + .35, y, z0 + 4.4), (dx + .35, y, z0 + 9.5), .05, "cable_fa", seg=6)
                    n += 2
    # lighting: MC along the purlins over each fixture row, a drop to each fixture, rows down the west columns
    rows = {}
    for p in lamps:
        rows.setdefault(round(p["a"][1]), []).append(p["a"][0])
    zr = 97.2
    for y, xs in rows.items():
        rod((482, y, zr), (max(xs), y, zr), .08, "cable_mc", seg=6)
        for x in xs:
            if CRANE_X[0] <= x <= CRANE_X[1]:
                continue                                                    # fixture over the parked crane: fed in the run
            rod((x, y, zr), (x, y, 94.6), .06, "cable_mc", seg=6)
            n += 1
        n += 1
    ys = sorted(rows)
    if ys:
        rod((482.9, ys[0], zr), (482.9, ys[-1], zr), .08, "cable_mc", seg=6)          # west-end header
        rod((482.9, YN - .4, ZG), (482.9, YN - .4, zr), .08, "cable_mc", seg=6)        # up the NW column
        rod((482.9, ys[-1], zr), (482.9, YN - .4, zr), .08, "cable_mc", seg=6)
        n += 3
    # crane runway conductor bar under the north girder, fused disconnect at the west end
    rod((486, YN - .2, 80.4), (1096, YN - .2, 80.4), .22, "amber", seg=8)
    for x in range(490, 1096, 10):
        box(x - .1, x + .1, YN - .3, YN + .1, 80.6, 81.2, "steel")
        n += 1
    box(484.5, 487.5, YN - .9, YN, 30, 34, "panel"); box(485.6, 486.4, YN - 1.0, YN - .9, 31.5, 33, "red")
    rod((486, YN - .4, 34), (486, YN - .4, 80.4), .09, "cable_mc", seg=6)
    n += 4
    # exit / emergency lights over the deck-stair openings
    for x in (712.4, 872.4):                               # beside the stair openings, clear of the tray brackets
        box(x - 1, x + 1, YN - .3, YN, 30, 30.9, "safety")
        rod((x, YN - .15, 30.9), (x, YN - .15, ZG), .06, "cable_mc", seg=6)
        n += 2
    return n
