"""Battery energy storage at LOD 3 (detail cycle 7).

- BESS yard: crushed-stone surface, its own 8 ft security fence with a double vehicle gate on
  the west side, hazard signage (NFPA 855) on the fence and gate, lighting poles in the aisles.
- Each container (ISO 40 ft high cube): six battery-rack doors on the north face, HVAC unit at
  the east end (drawn), roof deflagration vents and a gas-detection exhaust fan, a strobe /
  horn at the door end, fire-suppression release and E-stop panel, ground leads, and a precast
  DC cable trench to its PCS / MV skid.
- Each PCS / MV skid: inverter (PCS) cabinet with cooling grille beside the MV step-up
  transformer, LV DC combiner, ground leads.
- 34.5 kV collector circuits: three buried feeders, one per skid column, up the aisles to the
  collector e-house; the e-house to the main power transformer by 34.5 kV cable.
- Collector e-house and EMS building: stairs and landings, HVAC, cable entries.
All typical, not engineered.
"""
import fuel
import wiring as W
from fuel import box, rod, find, on


def dress(flag):
    fuel.D = flag


SHEET = "typical (BESS detail)"
COLS = (1615, 1735, 1855)          # the aisle just east of each PCS / MV skid column


def routes(add_route):
    for x in COLS:
        add_route("mvlv_cable", [(x, 722), (x, 400), (1825, 400), (1825, 376)], layer="OPT_BESS_ROUTES", sheet=SHEET)
    add_route("mvlv_cable", [(1800, 368), (1765, 368)], layer="OPT_BESS_ROUTES", sheet=SHEET)   # e-house to MPT


def yard():
    it = fuel.new_item("OPT_BESS", "BESS yard: surfacing, fence, gate, signage, lighting", (1550, 1920, 345, 740), (0, 30),
                       area="H", sheet=SHEET, register=False)
    it["wiring"] = ["Yard lighting: Cu THHN/THWN-2 in buried PVC conduit from the BESS auxiliary board",
                    "Fence grounding: bare Cu tied to the BESS ground grid at every corner and gate post"]
    fuel.D = True
    box(1552, 1918, 347, 738, 0, .08, "pad")
    for (x0, x1, y0, y1) in ((1550, 1920, 345, 345.4), (1550, 1920, 739.6, 740), (1919.6, 1920, 345, 740),
                             (1550, 1550.4, 345, 494), (1550, 1550.4, 525, 740)):
        box(x0, x1, y0, y1, 0, 8, "fence")
    for x in range(1550, 1921, 20):
        for y in (345.2, 739.8):
            box(x - .2, x + .2, y - .2, y + .2, 0, 8.5, "fence")
    for y in range(345, 741, 20):
        for x in (1550.2, 1919.8):
            if x < 1551 and 494 < y < 525:
                continue
            box(x - .2, x + .2, y - .2, y + .2, 0, 8.5, "fence")
    for y in (494, 525):                                                        # gate posts and leaves (open)
        box(1549.6, 1550.8, y - .6, y + .6, 0, 10, "steel")
    box(1535, 1535.4, 494, 509, 0, 8, "fence")
    box(1535, 1535.4, 510, 525, 0, 8, "fence")
    for (x, y) in ((1549.8, 520), (1549.8, 600), (1549.8, 700), (1700, 345.2), (1900, 739.8)):   # hazard signs
        box(x - .05 if x < 1600 else x - 1.5, x + .05 if x < 1600 else x + 1.5,
            y - 1.5 if x < 1600 else y - .05, y + 1.5 if x < 1600 else y + .05, 4.5, 6.5, "sign")
        box(x - .06 if x < 1600 else x - 1.5, x + .06 if x < 1600 else x + 1.5,
            y - 1.5 if x < 1600 else y - .06, y + 1.5 if x < 1600 else y + .06, 6.1, 6.5, "red")
    for (x, y) in ((1615, 509), (1855, 509), (1615, 625), (1855, 625), (1735, 740 - 12)):   # aisle lights
        rod((x, y, 0), (x, y, 30), .3, "steel", r2=.18, seg=8)
        box(x - .8, x + .8, y - .5, y + .5, 29.2, 30, "lamp")
    fuel.D = False


def containers():
    for it in fuel.G["items"]:
        if it["name"] != "BESS container (ISO 40 ft high cube)":
            continue
        x0, x1, y0, y1 = it["fp"]
        it["wiring"] = ["DC power 1,500 V: Cu 2 kV PV / RHW-2 single conductors in the precast trench to the PCS",
                        "Auxiliary 480 V (HVAC, lighting): Cu XHHW-2, Type TC-ER from the skid auxiliary panel",
                        "BMS / EMS data: fibre optic and Cat 6A to the EMS building",
                        W.FA + "; gas detection and suppression release", W.GND]
        on(it)
        dress(True)
        for k in range(6):                                                      # battery-rack doors (north face)
            xd = x0 + 2.5 + k * 5.6
            box(xd, xd + 4.8, y1, y1 + .08, 1.4, 9.6, "door")
            box(xd + 4.2, xd + 4.5, y1 + .08, y1 + .2, 5, 5.6, "steel")         # handle
        for xv in (x0 + 8, x0 + 20, x0 + 32):                                  # deflagration vents
            box(xv - 1.5, xv + 1.5, y0 + 2.5, y0 + 5.5, 10.5, 11, "machine")
        rod((x0 + 3, y0 + 4, 10.5), (x0 + 3, y0 + 4, 11.8), 1, "fan", seg=12)   # gas-detection exhaust fan
        rod((x0 + .6, y1 - .6, 10.5), (x0 + .6, y1 - .6, 11.4), .3, "red", seg=8)   # strobe / horn
        box(x0 - .1, x0, y0 + 2, y0 + 4, 4, 6.5, "red")                         # suppression release / E-stop
        box(x0 - .1, x0, y0 + 5, y0 + 6.5, 4.5, 6, "sign")
        for (gx, gy) in ((x0 + .5, y0 + .5), (x1 - .5, y1 - .5)):
            rod((gx, gy, 1), (gx, gy, .1), .08, "copper", seg=4)
        dress(False)


def skids():
    for it in fuel.G["items"]:
        if it["name"] != "BESS PCS / MV skid":
            continue
        x0, x1, y0, y1 = it["fp"]
        it["wiring"] = ["34.5 kV collector: Al MV-105 single conductors 35 kV, 133% insulation, buried, to the collector e-house",
                        "DC 1,500 V from two containers: Cu 2 kV PV / RHW-2 in precast trench",
                        W.CTRL, "PCS control / EMS: fibre optic", W.GND]
        on(it)
        dress(True)
        box(x0 - 9, x0 - 1, y0, y1, 0, 1, "concrete")                           # PCS pad
        box(x0 - 8.5, x0 - 1.5, y0 + .5, y1 - .5, 1, 8.5, "cabinet")            # inverter (PCS)
        box(x0 - 8.6, x0 - 1.4, y1 - .6, y1 - .4, 3, 7.5, "louvre")             # cooling grille
        box(x0 - 8.6, x0 - 1.4, y0 + .4, y0 + .6, 3, 7.5, "louvre")
        box(x0 - 8, x0 - 2, y0 + 1, y1 - 1, 8.5, 9.3, "machine")                # roof fans
        box(x0 - 1.5, x0, y0 + 2, y0 + 6, 2, 6, "steel")                         # LV bus link to the transformer
        box(x0 - 10.5, x0 - 9, y0 + 2, y0 + 5, 1, 5.5, "panel")                 # DC combiner
        for (gx, gy) in ((x0 - 8.5, y0 + .5), (x1 - .5, y1 - .5)):
            rod((gx, gy, 1), (gx, gy, .1), .08, "copper", seg=4)
        # precast DC trench from the two containers it serves (the row south of the skid)
        yc = y0 - 11                                                             # container north face
        box(x0 - 5, x0 + 45, yc + .2, yc + 2.2, 0, .3, "concrete")
        box(x0 - 6, x0 - 4, yc + 2.2, y0, 0, .3, "concrete")
        dress(False)


def buildings():
    for name in ("34.5 kV collector e-house", "BESS EMS / SCADA"):
        it = find(name)
        x0, x1, y0, y1 = it["fp"]
        on(it)
        dress(True)
        h = it["z"][1]
        for xs in (x0 + 4, x1 - 8):                                             # landings and stairs, south face
            box(xs, xs + 4, y0 - 4, y0, 2.2, 2.5, "grating")
            for st in range(4):
                z = 2.2 - .5 * (st + 1)
                box(xs, xs + 4, y0 - 4 - (st + 1) * .9, y0 - 4 - st * .9, z - .1, z, "grating")
            box(xs + .5, xs + 3.5, y0 - .1, y0, 2.5, 9.5, "door")
            box(xs + 1, xs + 3, y0 - .3, y0 - .1, 10, 10.5, "lamp")
        box(x1 - 6, x1 - 1, y1 - 4, y1 - 1, h, h + 3, "machine")                # HVAC
        rod((x1 - 3.5, y1 - 2.5, h + 3), (x1 - 3.5, y1 - 2.5, h + 3.3), 1.3, "fan", seg=12)
        for k in range(int((x1 - x0) // 12)):                                   # bottom cable entries
            xc = x0 + 6 + k * 12
            box(xc - 1.2, xc + 1.2, y1 - 1.6, y1 - .4, 0, 2.2, "steel")
            for c in range(3):
                rod((xc - .7 + c * .7, y1 - 1, 0), (xc - .7 + c * .7, y1 - 1, 2.1), .18, "cable_mv", seg=6)
        dress(False)


def build():
    yard()
    containers()
    skids()
    buildings()
