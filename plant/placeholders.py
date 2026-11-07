"""Replace the remaining single-box placeholders with equipment at LOD 3 (inside the same
footprints and below the same tops): kettle reboilers, the reclaimer, rich / lean amine skids
with plate cross exchangers and a lean cooler, wash and quench pump sets, carbon filters,
instrument air, CW pumps, the CO2 export compressor, LNG send-out metering and sump pump,
H2 water purification and blending skids, the BTM tie breaker and BESS containers.
All typical, not engineered.
"""
import fuel
from fuel import box, rod, find, on, strip, hvessel


def items(prefix):
    return [it for it in fuel.G["items"] if it["name"].startswith(prefix)]


def base(x0, x1, y0, y1, h=.8):
    box(x0, x1, y0, y1, 0, h, "concrete")


def frame(x0, x1, y0, y1, z0, z1):
    box(x0, x1, y0, y0 + .5, z0, z1, "steel")
    box(x0, x1, y1 - .5, y1, z0, z1, "steel")


def pump(x, y, along="x", r=1.4, z=2.6):
    """Horizontal end-suction pump set: baseplate, casing, coupling guard, motor, nozzles."""
    if along == "x":
        box(x - 1, x + 12, y - 2, y + 2, .8, 1.4, "steel")
        rod((x, y, z), (x + 3, y, z), r * 1.25, "pump", seg=14)
        box(x + 3, x + 5, y - .8, y + .8, z - .9, z + .9, "amber")
        rod((x + 5, y, z), (x + 11, y, z), r, "motor", seg=14)
        rod((x - 2.2, y, z), (x, y, z), r * .5, "pipe", seg=10)                     # suction
        rod((x + 1.5, y, z + r * 1.2), (x + 1.5, y, z + r * 1.2 + 2.5), r * .42, "pipe", seg=10)  # discharge
    else:
        box(x - 2, x + 2, y - 1, y + 12, .8, 1.4, "steel")
        rod((x, y, z), (x, y + 3, z), r * 1.25, "pump", seg=14)
        box(x - .8, x + .8, y + 3, y + 5, z - .9, z + .9, "amber")
        rod((x, y + 5, z), (x, y + 11, z), r, "motor", seg=14)
        rod((x, y - 2.2, z), (x, y, z), r * .5, "pipe", seg=10)
        rod((x, y + 1.5, z + r * 1.2), (x, y + 1.5, z + r * 1.2 + 2.5), r * .42, "pipe", seg=10)


def vvessel(x, y, r, z0, z1, c="tank", legs=True):
    rod((x, y, z0), (x, y, z1 - r * .4), r, c, seg=18)
    rod((x, y, z1 - r * .4), (x, y, z1), r, c, r2=r * .35, seg=18)
    if legs:
        for (dx, dy) in ((-.7, -.7), (.7, -.7), (-.7, .7), (.7, .7)):
            rod((x + dx * r, y + dy * r, .8), (x + dx * r, y + dy * r, z0 + .3), .25, "steel", seg=6)


def plate_hx(x0, x1, y0, y1, z1):
    """Gasketed plate exchanger: fixed and pressure plates, carrying bars, plate pack, nozzles."""
    box(x0, x0 + 1.2, y0, y1, .8, z1, "steel")
    box(x1 - 1.2, x1, y0, y1, .8, z1, "steel")
    box(x0, x1, (y0 + y1) / 2 - .3, (y0 + y1) / 2 + .3, z1 - .8, z1 - .2, "steel")
    box(x0 + 1.4, x1 - 3, y0 + .3, y1 - .3, 1.6, z1 - 1.2, "radiator")
    for zz in (2.6, z1 - 2.4):
        for yy in (y0 + 1, y1 - 1):
            rod((x0, yy, zz), (x0 - 1.8, yy, zz), .6, "pipe", seg=10)


def build():
    fuel.D = False
    # ---- CCS: DCC quench pumps and filters
    for it in items("DCC-") :
        if "pumps" not in it["name"]:
            continue
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(3):
            pump(x0 + 3 + k * 9, y0 + 5, "y", r=1.5)
        vvessel(x1 - 6, y1 - 6, 2.4, 1.2, 7.8)
        vvessel(x1 - 6, y0 + 6, 2.4, 1.2, 7.8)
        rod((x0 + 3, y0 + 2, 6.5), (x1 - 3, y0 + 2, 6.5), .7, "pipe", seg=10)       # discharge header
    # ---- CCS: water-wash pumps and wash-water cooler
    for it in items("Water-wash pumps"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(2):
            pump(x0 + 5 + k * 10, y0 + 4, "y", r=1.2)
        plate_hx(x0 + 6, x1 - 4, y1 - 14, y1 - 6, 7.6)
        rod((x0 + 4, y0 + 22, 6), (x1 - 3, y0 + 22, 6), .5, "waterline", seg=10)
    # ---- CCS: rich / lean pumps, plate cross exchangers, lean cooler
    for it in items("Rich/lean pumps"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(2):
            pump(x0 + 4, y0 + 5 + k * 8, "x", r=1.6)                                 # rich amine pumps
            pump(x0 + 4, y0 + 24 + k * 8, "x", r=1.5)                                # lean amine pumps
        plate_hx(x0 + 22, x1 - 4, y0 + 4, y0 + 12, 14.5)                             # cross exchangers
        plate_hx(x0 + 22, x1 - 4, y0 + 16, y0 + 24, 14.5)
        hvessel(x0 + 20, x1 - 2, y1 - 10, 6, 2.6, saddles=(x0 + 23, x1 - 6), nozzles=(x0 + 26, x1 - 9))   # lean cooler
        rod((x0 + 2, y0 + 44, 9), (x1 - 2, y0 + 44, 9), .8, "pipe", seg=10)
        rod((x0 + 2, y0 + 46, 9), (x1 - 2, y0 + 46, 9), .8, "pipe", seg=10)
    # ---- CCS: kettle reboilers on a steel table, LP steam in, condensate pot
    for it in items("RB-"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for (xc, yc) in ((x0 + 2, y0 + 2), (x1 - 2, y0 + 2), (x0 + 2, y1 - 2), (x1 - 2, y1 - 2),
                         ((x0 + x1) / 2, y0 + 2), ((x0 + x1) / 2, y1 - 2)):
            box(xc - .6, xc + .6, yc - .6, yc + .6, .8, 8, "steel")
        box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, 8, 8.8, "grating")
        for yk in (y0 + 13, y1 - 13):
            hvessel(x0 + 3, x1 - 3, yk, 15, 6, saddles=(x0 + 9, x1 - 9), nozzles=(x0 + 12, x1 - 12))   # kettle
            rod(((x0 + x1) / 2, yk, 21), ((x0 + x1) / 2, yk, 26), 1.6, "pipe", seg=12)   # vapour outlet
        rod((x0 + 2, (y0 + y1) / 2, 27.5), (x1 - 2, (y0 + y1) / 2, 27.5), 1.8, "lngpipe", seg=12)  # LP steam header
        for yk in (y0 + 13, y1 - 13):
            rod((x0 + 8, (y0 + y1) / 2, 27.5), (x0 + 8, yk, 20.5), 1.2, "lngpipe", seg=10)
        vvessel(x1 - 5, (y0 + y1) / 2, 1.6, 9, 15, legs=False)                        # condensate pot
    # ---- CCS: reclaimer
    for it in items("Reclaimer"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        hvessel(x0 + 4, x0 + 34, (y0 + y1) / 2, 9, 5.5, saddles=(x0 + 9, x0 + 29), nozzles=(x0 + 12, x0 + 26))
        vvessel(x1 - 8, y0 + 10, 3.5, 1.2, 18)                                       # sludge / waste drum
        box(x1 - 12, x1 - 3, y1 - 14, y1 - 4, .8, 9, "machine")                      # caustic / heater skid
        rod(((x0 + x1) / 2, (y0 + y1) / 2, 14.5), ((x0 + x1) / 2, (y0 + y1) / 2, 24.5), .9, "pipe", seg=10)
    # ---- CCS: activated-carbon filters
    for it in items("Activated-carbon filter"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(3):
            vvessel(x0 + 15 + k * 30, (y0 + y1) / 2, 6, 1.2, 14.5)
        rod((x0 + 8, y0 + 3, 4), (x1 - 8, y0 + 3, 4), .8, "pipe", seg=10)
        rod((x0 + 8, y1 - 3, 9), (x1 - 8, y1 - 3, 9), .8, "pipe", seg=10)
    # ---- CCS: instrument air
    for it in items("CCS instrument air"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(2):
            box(x0 + 3 + k * 12, x0 + 13 + k * 12, y0 + 3, y0 + 16, .8, 8, "cabinet")   # compressor packages
            box(x0 + 3 + k * 12, x0 + 13 + k * 12, y0 + 2.8, y0 + 3, 2, 7, "louvre")
        for k in range(2):
            vvessel(x0 + 8 + k * 12, y1 - 10, 3, 1.2, 11.5)                             # receivers
        box(x1 - 9, x1 - 3, y0 + 22, y0 + 32, .8, 9, "machine")                         # dryer
    # ---- CCS: CO2 export compressor (conditional)
    for it in items("CONDITIONAL: HP export compressor"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        box(x0 + 4, x0 + 40, y0 + 6, y0 + 22, .8, 2, "steel")
        rod((x0 + 6, y0 + 14, 6), (x0 + 22, y0 + 14, 6), 4.2, "machine", seg=18)      # compressor casing
        rod((x0 + 24, y0 + 14, 6), (x0 + 38, y0 + 14, 6), 3.6, "motor", seg=18)
        box(x0 + 22, x0 + 24, y0 + 11, y0 + 17, 3, 9, "amber")
        for k in range(3):                                                         # aftercooler bays
            xb = x0 + 6 + k * 12
            for (px, py) in ((xb, y0 + 28), (xb + 10, y0 + 28), (xb, y1 - 6), (xb + 10, y1 - 6)):
                box(px - .4, px + .4, py - .4, py + .4, .8, 15, "steel")
            box(xb, xb + 10, y0 + 28, y1 - 6, 15, 17.5, "bundle")
            rod((xb + 5, (y0 + 28 + y1 - 6) / 2, 17.5), (xb + 5, (y0 + 28 + y1 - 6) / 2, 19.8), 4.2, "fan", seg=16)
        for k in range(2):                                                         # metering runs
            rod((x1 - 30, y0 + 8 + k * 6, 4), (x1 - 4, y0 + 8 + k * 6, 4), .9, "pipe", seg=10)
            box(x1 - 20, x1 - 14, y0 + 6.5 + k * 6, y0 + 9.5 + k * 6, 2, 6.5, "panel")
        box(x1 - 10, x1 - 3, y1 - 12, y1 - 4, .8, 10, "ehouse")                        # analyser shelter
    # ---- CCS: circulating-water pumps
    for it in items("CCS circulating-water pumps"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(4):
            pump(x0 + 6 + k * 18, y0 + 10, "y", r=2.6, z=4)
        rod((x0 + 4, y0 + 6, 5), (x1 - 4, y0 + 6, 5), 2.2, "waterline", seg=14)
        rod((x0 + 4, y1 - 6, 6), (x1 - 4, y1 - 6, 6), 2.2, "waterline", seg=14)
    # ---- LNG send-out metering and pressure control
    for it in items("LNG 16: send-out metering"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(2):
            y = y0 + 12 + k * 14
            rod((x0 + 3, y, 3.5), (x1 - 3, y, 3.5), 1, "pipe", seg=12)
            box(x0 + 14, x0 + 22, y - 1.5, y + 1.5, 2, 5.5, "panel")                   # ultrasonic meter
            box(x1 - 16, x1 - 13, y - 1.2, y + 1.2, 2, 6, "red")                       # pressure control valve
        for (px, py) in ((x0 + 2, y0 + 2), (x1 - 2, y0 + 2), (x0 + 2, y1 - 2), (x1 - 2, y1 - 2)):
            box(px - .3, px + .3, py - .3, py + .3, .8, 9.4, "steel")
        box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, 9.4, 10, "roof")
    for it in items("LNG impoundment sump pump"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        box(x0 + 2, x1 - 2, y0 + 2, y1 - 2, -6, .4, "concrete")                       # sump pit
        box(x0 + 3, x1 - 3, y0 + 3, y1 - 3, .4, .6, "grating")
        rod(((x0 + x1) / 2, (y0 + y1) / 2, .6), ((x0 + x1) / 2, (y0 + y1) / 2, 4), .6, "pipe", seg=10)
        box((x0 + x1) / 2 + 3, (x0 + x1) / 2 + 5, y0 + 4, y0 + 6, .4, 5.5, "panel")
    # ---- H2: water purification and blending skid
    for it in items("H2 24: water purification"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(4):                                                         # RO membrane tubes
            rod((x0 + 3, y0 + 5 + k * 2.2, 6), (x0 + 22, y0 + 5 + k * 2.2, 6), .9, "tank", seg=12)
            rod((x0 + 3, y0 + 5 + k * 2.2, 8.4), (x0 + 22, y0 + 5 + k * 2.2, 8.4), .9, "tank", seg=12)
        frame(x0 + 2, x0 + 23, y0 + 3, y0 + 14, .8, 10)
        for k in range(2):
            vvessel(x1 - 6, y0 + 6 + k * 10, 2.5, 1.2, 11.5)                            # EDI / storage
        box(x0 + 3, x0 + 10, y1 - 8, y1 - 2, .8, 8, "cabinet")
    for it in items("H2 30: H2 / gas blending skid"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(2):
            rod((x0 + 3, y0 + 8 + k * 10, 4), (x1 - 3, y0 + 8 + k * 10, 4), 1, "pipe", seg=12)
            box((x0 + x1) / 2 - 2, (x0 + x1) / 2 + 2, y0 + 6.5 + k * 10, y0 + 9.5 + k * 10, 2, 7, "red")
        box(x1 - 9, x1 - 2, y1 - 9, y1 - 2, .8, 9.5, "ehouse")                          # analyser shelter
    # ---- BTM 230 kV tie breaker: dead-tank breaker, bushings, disconnect
    for it in items("BTM 230 kV tie breaker"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        for k in range(3):
            x = x0 + 3.5 + k * 5.5
            rod((x, y0 + 6, 4), (x, y0 + 14, 4), 1.6, "machine", seg=14)                 # tank
            for yb in (y0 + 6.5, y0 + 13.5):
                rod((x, yb, 5.5), (x, yb + (-2 if yb < y0 + 10 else 2), 21.5), .5, "insulator", seg=10)
        box(x0 + 1, x1 - 1, y0 + 15, y0 + 18, .8, 5, "cabinet")                          # operating mechanism
        for k in range(3):                                                            # disconnect on a stand
            x = x0 + 3.5 + k * 5.5
            rod((x, y1 - 3, .8), (x, y1 - 3, 14), .35, "steel", seg=8)
            rod((x, y1 - 3, 14), (x, y1 - 3, 18), .4, "insulator", seg=8)
            rod((x, y1 - 3, 18.4), (x, y1 - 1, 18.4), .15, "copper", seg=6)
    # ---- conditional items keep their tan tint (built only if a study confirms them) but get real shape
    for it in items("CONDITIONAL: grounding transformer"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1, .5)
        box(x0 + 2, x1 - 2, y0 + 2, y1 - 2, .5, 6, "conditional")                       # zigzag transformer tank
        for k in range(3):
            box(x0 + .5, x0 + 2, y0 + 2 + k * 2.4, y0 + 3 + k * 2.4, 1, 5.5, "radiator")
        rod(((x0 + x1) / 2, (y0 + y1) / 2, 6), ((x0 + x1) / 2, (y0 + y1) / 2, 8), .35, "insulator", seg=8)
        box(x1 - 2, x1 - .5, y0 + 3, y0 + 7, 1, 5, "cabinet")                            # neutral resistor box
    for it in items("CONDITIONAL: SC-"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        base(x0, x1, y0, y1)
        box(x0 + 2, x1 - 2, y0 + 4, y1 - 12, .8, 13.5, "conditional")                   # evaporative media house
        for k in range(5):
            box(x0 + 4 + k * 10.5, x0 + 12 + k * 10.5, y0 + 3.8, y0 + 4, 3, 12, "louvre")
        for k in range(2):
            pump(x0 + 6 + k * 16, y1 - 8, "x", r=1.0)                                    # recirculation pumps
        vvessel(x1 - 8, y1 - 6, 2.5, 1, 9, c="conditional")                              # water tank / chiller drum
    for it in items("CONDITIONAL: BESS black-start alternative"):
        x0, x1, y0, y1 = it["fp"]
        strip(it)
        on(it)
        for k in range(2):
            y = y0 + 3 + k * 15
            box(x0 + 2, x0 + 42, y, y + 8, 0, 1, "concrete")
            box(x0 + 2.2, x0 + 41.8, y, y + 8, 1, 9.5, "conditional")
            for d in range(6):
                box(x0 + 4 + d * 6, x0 + 9 + d * 6, y + 8, y + 8.08, 1.5, 9, "door")
    # ---- BTM BESS containers: rack doors, vents, strobe, E-stop
    for it in items("BTM BESS container"):
        x0, x1, y0, y1 = it["fp"]
        on(it)
        fuel.D = True
        for k in range(6):
            xd = x0 + 2.5 + k * 5.6
            box(xd, xd + 4.8, y1, y1 + .08, 1.4, 9.6, "door")
        for xv in (x0 + 8, x0 + 20, x0 + 32):
            box(xv - 1.5, xv + 1.5, y0 + 2.5, y0 + 5.5, 10.5, 11, "machine")
        rod((x0 + .6, y1 - .6, 10.5), (x0 + .6, y1 - .6, 11.4), .3, "red", seg=8)
        box(x0 - .1, x0, y0 + 2, y0 + 4, 4, 6.5, "red")
        box(x1, x1 + .8, y0 + 1.5, y0 + 6.5, 3, 8, "machine")                          # HVAC
        fuel.D = False
