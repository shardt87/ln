"""Skid pre-assembly / pre-wire workstation for the modular-yard expansion, on the open strip between the cable reel
yard and the inlet chillers (moved Oct 23 from the maintenance laydown, now shared with cooling-tower cells): away from energised plant, reached
from the west spine road, beside the prefab staging bay and the reels. Finished skids go out on a lowboy to the modular yard.

On an expansion the electrical crew wires skids at waist height on a work pad before the crane sets them: junction
boxes, skid-edge tray and conduit are mounted, the skid wiring is pulled and terminated, the field tails are cut to
length, coiled and tagged, and continuity / insulation-resistance (megger) tests are recorded. Here:
- an open concrete work pad as the workstation (no shelter), with a fuel-gas
  conditioning skid and a pump skid on cribbing being pre-wired, workbenches, a wire wagon, test gear, JB and
  tray-fitting kits, temporary power and lights, and the crew;
- a ready-to-set row outside: an HRSG chemical-feed skid (phosphate / amine dosing), finished and tagged TESTED - READY
  TO SET, and a bare lube-oil
  skid getting kit 1 (the plug-in GT auxiliary harness): trunk in the tray, branches plugged into the devices;
- a PDC e-house delivered in two shipping splits on cribbing, the split faces wrapped, with pre-terminated
  interconnect cables coiled at the split ready to reconnect once set.
- three standardized pre-wired kits staged beside the skids they serve, with a board (owner, Oct 26): kit 1 GT
  auxiliary skid harness (lube oil), kit 2 pump-skid motor leads plus instrument harness, kit 3 e-house split
  interconnects.
- three more skid types east of the ready row: a power skid (transformer + LV switchboard + MCC) with its
  pre-terminated tails going on, an instrument-air skid being pre-wired, a factory-wired CEMS shelter ready to set.
Transformers and large e-houses are not pre-wired on site (set directly; factory-integrated), so they are not here.
Typical arrangement, generic labels.
"""
import math

import fuel
from fuel import box, rod


def person(x, y, z=0.0, a=0.0, vest="hivis", hat="hardhat"):
    import maintenance as mt
    mt.person(x, y, z, a, vest=vest, hat=hat)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def hexpart(v, c):
    fuel._add("hex", v=[[round(t, 3) for t in p] for p in v], color=c)


def cribbing(x0, x1, y0, y1, h=1.0):
    for (x, y) in ((x0 + 1, y0 + 1.5), (x1 - 1, y0 + 1.5), (x0 + 1, y1 - 1.5), (x1 - 1, y1 - 1.5),
                   ((x0 + x1) / 2, y0 + 1.5), ((x0 + x1) / 2, y1 - 1.5)):
        for k in range(3):
            if k % 2:
                box(x - 1.2, x + 1.2, y - .4, y - .1, k * h / 3, (k + 1) * h / 3, "timber")
                box(x - 1.2, x + 1.2, y + .1, y + .4, k * h / 3, (k + 1) * h / 3, "timber")
            else:
                box(x - .4, x - .1, y - 1.2, y + 1.2, k * h / 3, (k + 1) * h / 3, "timber")
                box(x + .1, x + .4, y - 1.2, y + 1.2, k * h / 3, (k + 1) * h / 3, "timber")


def skid_base(x0, x1, y0, y1, z):
    for xx in (x0, x1 - .7):
        box(xx, xx + .7, y0, y1, z, z + 1.1, "steel")
    for k in range(6):
        yy = y0 + k * (y1 - y0 - .5) / 5
        box(x0, x1, yy, yy + .5, z, z + 1.1, "steel")
    box(x0 + .7, x1 - .7, y0, y1, z + .9, z + 1.1, "grating")
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):                         # lifting lugs
        box(x - .2, x + .2, y - .2, y + .2, z + 1.1, z + 1.8, "sp_yellow")


def prewire(x0, x1, y0, y1, z, done=False, side=1, label="FG SKID"):
    """Electrical pre-wire on a skid: edge tray, JBs on stanchions, conduit drops, coiled tagged tails."""
    xe = x1 - .5 if side > 0 else x0 + .5
    zt = z + 4.2
    for yy in [y0 + 1 + k * 6 for k in range(int((y1 - y0 - 2) / 6) + 1)]:           # tray stanchions
        box(xe - .15, xe + .15, yy - .15, yy + .15, z + 1.1, zt, "steel")
    box(xe - .9, xe + .9, y0 + .8, y1 - .8, zt, zt + .35, "pipe")
    box(xe - .75, xe + .75, y0 + .8, y1 - .8, zt + .08, zt + .3, "cable_tc" if done else "cable_inst")
    jbs = [y0 + (y1 - y0) * f for f in (.2, .5, .8)]
    for k, yy in enumerate(jbs):
        box(xe - side * 1.6 - .5, xe - side * 1.6 + .5, yy - .9, yy + .9, z + 3.0, z + 5.0, "alu")            # JB
        box(xe - side * 1.6 - .52, xe - side * 1.6 + .52, yy - .3, yy + .3, z + 4.6, z + 4.8, "label")
        rod((xe - side * 1.6, yy, z + 3.0), (xe - side * 1.6, yy, z + 1.1), .12, "alu", seg=8)                  # stand
        for j in range(3):                                                                                     # conduit drops
            rod((xe - side * (2.4 + j * 1.6), yy + .5, z + 3.4), (xe - side * (2.4 + j * 1.6), yy + .5, z + 1.6), .07, "alu", seg=6)
            rod((xe - side * 1.6, yy + .5, z + 3.4), (xe - side * (2.4 + j * 1.6), yy + .5, z + 3.4), .07, "alu", seg=6)
    for k, yy in enumerate((y0 + 3, (y0 + y1) / 2, y1 - 3)):                                                   # coiled tails
        for j, c in enumerate(("cable_tc", "cable_inst", "cable_fo")):
            cx, cy, cz = xe + side * 1.4, yy + (j - 1) * 1.1, z + 1.6
            rod((cx - .25, cy, cz), (cx + .25, cy, cz), .5, c, seg=16)
            if done:
                rod((cx - .28, cy, cz), (cx + .28, cy, cz), .52, "tent", r2=.52, seg=16)
    tag = ([("TESTED", .26, 1, "#ffffff", 0, "#2f7a3c"), ("READY TO SET", .2, 1, "#111111"), (label, .16, 0, "#333333"),
            ("IR > 1 GΩ  ·  CONTINUITY OK", .13, 0, "#333333")] if done else
           [("PRE-WIRE", .26, 1, "#111111", 0, "#f2c200"), ("IN PROGRESS", .2, 1, "#111111"), (label, .16, 0, "#333333"),
            ("DO NOT LIFT", .14, 1, "#c41f27")])
    decal((xe + side * .95, (y0 + y1) / 2 + 3, zt - 1.2), (side, 0, 0), 2.6, 1.8, tag, bg="#ffffff")


def kit_fitup(x0, x1, y0, y1, z):
    """Kit 1 being fitted to a bare lube-oil skid: the pre-made harness trunk laid in the skid-edge tray, its branches
    plugged into the pump motors, filter DP switches and reservoir instruments with connectors (no field terminations),
    two branches still coiled on the deck; a fitter on the skid."""
    xe, zt = x1 - .5, z + 4.2
    for yy in [y0 + 1 + k * 6 for k in range(int((y1 - y0 - 2) / 6) + 1)]:
        box(xe - .15, xe + .15, yy - .15, yy + .15, z + 1.1, zt, "steel")
    box(xe - .9, xe + .9, y0 + .8, y1 - .8, zt, zt + .35, "pipe")
    rod((xe, y0 + 1.2, zt + .5), (xe, y1 - 1.2, zt + .5), .3, "cable_inst", seg=12)                # harness trunk
    zb = z + 1.1
    targets = [(x0 + 3.0, y0 + 15.0, zb + 2.0), (x0 + 3.0, y0 + 19.0, zb + 2.0),                 # pump motors
               (x0 + 5.0, y1 - 6.0, zb + 3.8), (x0 + 5.0, y1 - 3.8, zb + 3.8),                   # filter DP switches
               (x1 - 3.4, y0 + 4.0, zb + 5.2), (x1 - 3.4, y0 + 9.0, zb + 5.2)]                   # reservoir level / temp
    for k, (tx, ty, tz) in enumerate(targets):
        c = ("cable_tc", "cable_tc", "cable_inst", "cable_inst", "cable_inst", "cable_tc")[k]
        rod((xe, ty, zt + .5), (xe - .6, ty, zt + .5), .06, c, seg=6)
        rod((xe - .6, ty, zt + .5), (tx + .4, ty, tz + .3), .06, c, seg=6)
        rod((tx + .4, ty, tz + .3), (tx + .1, ty, tz + .3), .13, "sp_black", seg=10)              # connector, plugged
        box(tx + .3, tx + .5, ty - .15, ty + .15, tz + .45, tz + .7, "white_truck")              # branch tag
    for k in range(2):                                                                            # not yet plugged
        cy = y1 - 9 - k * 2.4
        rod((xe - 1.2, cy - .4, zb + .5), (xe - 1.2, cy + .4, zb + .5), .45, "cable_inst", seg=14)
        rod((xe - 1.2, cy - .55, zb + .5), (xe - 1.2, cy - .75, zb + .5), .13, "sp_black", seg=10)
    decal((xe + .95, (y0 + y1) / 2 + 3, zt - 1.2), (1, 0, 0), 2.8, 1.9,
          [("KIT 1 FIT-UP", .24, 1, "#111111", 0, "#f2c200"), ("plug-in harness · pre-tested", .16, 1, "#111111"),
           ("LUBE OIL SKID LOS-2", .15, 0, "#333333"), ("no field terminations", .14, 1, "#2f7a3c")], bg="#ffffff")
    person(x0 + 6.5, y0 + 17.0, z + 1.1, 0.0, vest="hivis_o")


def fuel_gas_skid(x0, x1, y0, y1, z):
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    cx = (x0 + x1) / 2 - 1.2
    for k, yy in enumerate((y0 + 4, y0 + 9)):                                       # filter separators
        rod((cx, yy, zb), (cx, yy, zb + 8), 1.25, "tank", seg=20)
        rod((cx, yy, zb + 8), (cx, yy, zb + 8.8), 1.25, "tank", r2=.4, seg=20)
    rod((cx, y0 + 14, zb + 2.0), (cx, y1 - 4, zb + 2.0), 1.5, "tank", seg=20)        # line heater
    rod((cx, y1 - 5, zb + 3.4), (cx, y1 - 5, zb + 9.5), .5, "steel_dark", seg=12)   # heater stack
    for xx in (cx - 1.8, cx + 1.6):
        rod((xx, y0 + 1, zb + 1.2), (xx, y1 - 1, zb + 1.2), .35, "fuelgas", seg=10)  # headers
    for k in range(3):                                                               # regulators / control valves
        yy = y0 + 16 + k * 3
        box(cx + 1.2, cx + 2.0, yy - .4, yy + .4, zb + 1.2, zb + 2.6, "fuelgas")
        rod((cx + 1.6, yy, zb + 2.6), (cx + 1.6, yy, zb + 3.4), .3, "sp_black", seg=10)
    box(x0 + .8, x0 + 2.6, y1 - 3.5, y1 - 1.2, zb, zb + 5.5, "panel")                # skid control panel


def chem_feed_skid(x0, x1, y0, y1, z):
    """HRSG chemical-feed skid (phosphate / amine): two dosing tanks with level gauges and agitator drives, four
    diaphragm metering pumps with motors on a drip tray, discharge manifold with calibration columns, local control
    panel and an eyewash station."""
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    cx = (x0 + x1) / 2 - 1.0
    for k, yy in enumerate((y0 + 4.5, y0 + 11.5)):                                   # dosing tanks
        rod((cx, yy, zb), (cx, yy, zb + 6.5), 2.4, "tank", seg=24)
        rod((cx, yy, zb + 6.5), (cx, yy, zb + 6.8), 2.4, "steel", seg=24)
        rod((cx, yy, zb + 6.8), (cx, yy, zb + 7.8), .4, "motor", seg=12)               # agitator drive
        rod((cx + 2.45, yy, zb + .5), (cx + 2.45, yy, zb + 6.0), .08, "glass", seg=6)  # level gauge
    box(cx - 2.2, cx + 1.6, y0 + 16.5, y1 - 7.0, zb, zb + .25, "steel_dark")           # drip tray
    for k in range(4):                                                               # metering pumps
        yy = y0 + 17.5 + k * 1.9
        box(cx - 1.6, cx - .2, yy - .5, yy + .5, zb + .25, zb + 1.3, "pump")
        rod((cx - .2, yy, zb + .8), (cx + 1.2, yy, zb + .8), .38, "motor", seg=12)
        rod((cx - .9, yy, zb + 1.3), (cx - .9, yy, zb + 3.2), .08, "steel", seg=6)
    rod((cx - .9, y0 + 17.5, zb + 3.2), (cx - .9, y1 - 7.5, zb + 3.2), .12, "steel", seg=8)   # discharge manifold
    for k in range(2):
        rod((cx - 2.0, y0 + 18 + k * 3, zb + .3), (cx - 2.0, y0 + 18 + k * 3, zb + 3.0), .2, "glass", seg=10)   # cal columns
    box(x0 + .8, x0 + 2.6, y1 - 4.5, y1 - 1.2, zb, zb + 5.5, "panel")                # local control panel
    box(x1 - 2.4, x1 - 1.6, y1 - 3.0, y1 - 2.2, zb, zb + 3.6, "safety")              # eyewash


def power_skid(x0, x1, y0, y1, z):
    """Power skid (modular electrical): 13.8 kV / 480 V transformer, close-coupled LV switchboard and an MCC on one
    base, MV termination box at the transformer, bus link to the switchboard; pre-terminated MV-in and 600 V
    feeder tails being landed from a kit crate at the skid edge (stage: kit going on)."""
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    box(x0 + 1.5, x1 - 1.5, y0 + 1.5, y0 + 9.5, zb, zb + 7.0, "xfmr")                 # transformer tank
    for k in range(5):
        xx = x0 + 2.2 + k * (x1 - x0 - 4.4) / 4
        box(xx - .2, xx + .2, y0 + .6, y0 + 1.5, zb + .8, zb + 6.2, "radiator")         # radiator fins
    box(x0 + 2.5, x1 - 2.5, y0 + 9.5, y0 + 11.0, zb + 3.0, zb + 6.8, "steel_dark")      # throat / bus link
    box(x1 - 4.0, x1 - 1.0, y0 + 3.0, y0 + 7.0, zb + 7.0, zb + 8.6, "steel")             # MV termination box (roof)
    box(x0 + 1.2, x1 - 1.2, y0 + 11.0, y0 + 20.0, zb, zb + 7.6, "swgr")                 # LV switchboard
    for k in range(4):
        yy = y0 + 11.3 + k * 2.2
        box(x0 + 1.15, x0 + 1.2, yy, yy + 2.0, zb + .4, zb + 7.2, "door")
    box(x0 + 1.2, x1 - 1.2, y0 + 21.0, y1 - 1.5, zb, zb + 7.6, "panel")                  # MCC
    for k in range(3):
        yy = y0 + 21.3 + k * 2.2
        box(x0 + 1.15, x0 + 1.2, yy, yy + 2.0, zb + .4, zb + 7.2, "door")
    # pre-terminated tails being landed: MV in from the crate up to the termination box, 600 V tails out of the MCC
    cx, cy = x1 + 3.2, y0 + 5.0
    box(cx - 1.6, cx + 1.6, cy - 2.2, cy + 2.2, 0, .4, "timber")
    for (a0, a1, b0, b1) in ((-1.6, 1.6, -2.2, -2.0), (-1.6, 1.6, 2.0, 2.2), (-1.6, -1.4, -2.2, 2.2), (1.4, 1.6, -2.2, 2.2)):
        box(cx + a0, cx + a1, cy + b0, cy + b1, .4, 1.8, "timber")
    for k in range(3):
        yy = cy - 1.2 + k * 1.2
        rod((cx - .5, yy, .9), (cx + .5, yy, .9), .5, "cable_mv", seg=14)
        rod((cx - .9, yy, 1.4), (x1 - 2.5, y0 + 4.2 + k * 1.2, zb + 8.0), .12, "cable_mv", seg=8)   # landed on the box
    for k in range(4):                                                                  # 600 V tails coiled, tagged
        yy = y0 + 22.0 + k * 1.6
        rod((x1 + .8, yy, zb + .9), (x1 + 1.4, yy, zb + .9), .5, "cable_tc", seg=14)
        box(x1 + 1.5, x1 + 1.7, yy - .15, yy + .15, zb + 1.3, zb + 1.7, "white_truck")
    decal((x1 + .1, (y0 + y1) / 2, zb + 6.0), (1, 0, 0), 3.0, 1.9,
          [("KIT GOING ON", .24, 1, "#111111", 0, "#f2c200"), ("POWER SKID PS-1", .17, 1, "#111111"),
           ("13.8 kV / 480 V · MCC", .14, 0, "#333333"), ("pre-terminated tails", .14, 1, "#2f7a3c")], bg="#ffffff")


def ia_skid(x0, x1, y0, y1, z):
    """Instrument-air skid: rotary-screw compressor package, twin-tower desiccant dryer, vertical receiver, filters."""
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    box(x0 + 1.2, x1 - 1.2, y0 + 1.2, y0 + 8.5, zb, zb + 6.0, "equip")                 # compressor package
    for k in range(3):
        box(x0 + 1.15, x0 + 1.2, y0 + 1.8 + k * 2.2, y0 + 3.6 + k * 2.2, zb + 3.0, zb + 5.4, "louvre")
    for k in range(2):                                                                  # desiccant towers
        rod((x0 + 3.2 + k * 2.6, y0 + 11.0, zb), (x0 + 3.2 + k * 2.6, y0 + 11.0, zb + 7.0), .8, "tank", seg=16)
    rod(((x0 + x1) / 2, y1 - 3.5, zb), ((x0 + x1) / 2, y1 - 3.5, zb + 8.0), 1.6, "tank", seg=20)   # receiver
    rod(((x0 + x1) / 2, y1 - 3.5, zb + 8.0), ((x0 + x1) / 2, y1 - 3.5, zb + 8.6), 1.6, "tank", r2=.5, seg=20)
    for k in range(2):
        rod((x1 - 2.0, y0 + 13.5 + k * 1.4, zb + 1.0), (x1 - 2.0, y0 + 13.5 + k * 1.4, zb + 3.2), .3, "fueloil", seg=10)   # filters
    rod((x0 + 2, y0 + 8.6, zb + 4.6), (x0 + 2, y1 - 3.5, zb + 4.6), .2, "steel", seg=8)   # air header


def cems_shelter(x0, x1, y0, y1, z):
    """CEMS analyzer shelter, factory-wired: insulated shell on a skid, door, HVAC unit, cal-gas cylinder rack, the
    heat-traced sample-line umbilical and the probe cable coiled on the roof for shipping, tagged tested."""
    box(x0, x1, y0, y1, z, z + .6, "steel_dark")
    box(x0 + .2, x1 - .2, y0 + .2, y1 - .2, z + .6, z + 10.0, "white_truck")
    box(x0, x1, y0, y1, z + 10.0, z + 10.4, "roof")
    box(x0 + .15, x0 + .2, (y0 + y1) / 2 - 1.5, (y0 + y1) / 2 + 1.5, z + .8, z + 7.6, "door")
    box(x1 - .2, x1 + 1.0, y0 + 2.0, y0 + 5.0, z + 5.0, z + 7.6, "equip")              # wall HVAC
    for k in range(4):                                                                # cal-gas cylinders
        rod((x0 - 1.0, y0 + 1.5 + k * 1.1, z + .6), (x0 - 1.0, y0 + 1.5 + k * 1.1, z + 5.2), .4, ("safety", "hivis", "steel", "safety")[k], seg=12)
    box(x0 - 1.6, x0 - .4, y0 + .8, y0 + 5.6, z + 3.8, z + 4.0, "steel")
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for l in range(3):                                                                # umbilical coil on the roof
        pts = [(cx + 2.4 * math.cos(2 * math.pi * i / 28), cy + 2.4 * math.sin(2 * math.pi * i / 28), z + 10.7 + l * .22) for i in range(29)]
        for a, b in zip(pts, pts[1:]):
            rod(a, b, .18, "pvc_orange" if l < 2 else "cable_inst", seg=8)
    decal((x0 + .05, cy + 3.0, z + 7.0), (-1, 0, 0), 2.8, 1.8,
          [("TESTED", .26, 1, "#ffffff", 0, "#2f7a3c"), ("READY TO SET", .2, 1, "#111111"), ("CEMS SHELTER CEMS-4", .16, 0, "#333333"),
           ("factory-wired · heat-traced umbilical", .13, 0, "#333333")], bg="#ffffff")


def pump_skid(x0, x1, y0, y1, z):
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    cx = (x0 + x1) / 2 - .8
    for k, yy in enumerate((y0 + 4, y0 + 11)):
        rod((cx, yy - 2.5, zb + 1.4), (cx, yy, zb + 1.4), .9, "motor", seg=16)       # motor
        rod((cx, yy, zb + 1.4), (cx, yy + 2.2, zb + 1.4), .75, "pump", seg=16)        # pump
        box(cx - 1.2, cx + 1.2, yy - 2.8, yy + 2.6, zb, zb + .4, "steel")            # baseplate
        rod((cx, yy + 1.2, zb + 2.0), (cx, yy + 1.2, zb + 4.2), .35, "water", seg=10)
    rod((cx, y0 + 1, zb + 4.2), (cx, y1 - 1, zb + 4.2), .5, "water", seg=12)         # discharge header
    rod((cx - 2.2, y0 + 1, zb + 1.0), (cx - 2.2, y1 - 1, zb + 1.0), .6, "water", seg=12)
    box(x0 + .8, x0 + 2.4, y1 - 3, y1 - 1, zb, zb + 4.8, "panel")


def lube_skid(x0, x1, y0, y1, z):
    skid_base(x0, x1, y0, y1, z)
    zb = z + 1.1
    box(x0 + 1.2, x1 - 3.2, y0 + 1.5, y0 + 12, zb, zb + 5.0, "tank")                 # reservoir
    rod(((x0 + x1) / 2 - 1, y0 + 6, zb + 5), ((x0 + x1) / 2 - 1, y0 + 6, zb + 6.5), .3, "steel", seg=8)
    for k in range(2):
        yy = y0 + 15 + k * 4
        rod((x0 + 3, yy - 1.5, zb + 1), (x0 + 3, yy + 1.5, zb + 1), .6, "motor", seg=14)
    for k in range(2):
        rod((x0 + 5, y1 - 6 + k * 2.2, zb), (x0 + 5, y1 - 6 + k * 2.2, zb + 3.6), .5, "fueloil", seg=12)   # filters
    box(x0 + 1, x0 + 4.5, y1 - 3, y1 - 1, zb, zb + 3.2, "radiator")                  # cooler


def pdc_split(x0, x1, y0, y1, z, face, name):
    """One shipping split of a PDC e-house on cribbing; the split face (x = face) wrapped in white sheeting."""
    cribbing(x0, x1, y0, y1, z)
    box(x0, x1, y0, y1, z, z + .6, "steel_dark")
    box(x0 + .1, x1 - .1, y0 + .1, y1 - .1, z + .6, z + 12, "ehouse")
    box(x0, x1, y0, y1, z + 12, z + 12.5, "roof")
    for k in range(1, int((x1 - x0) / 4)):
        xx = x0 + 4 * k
        for (yy, s) in ((y0, -1), (y1, 1)):
            box(xx - .08, xx + .08, yy, yy + s * .1, z + .7, z + 11.9, "roof")
    s = 1 if face > (x0 + x1) / 2 else -1
    box(face, face + s * .06, y0 + .2, y1 - .2, z + .7, z + 11.8, "tent")            # wrapped split face
    decal(((x0 + x1) / 2, y0 - .03, z + 9), (0, -1, 0), 8, 1.6,
          [(name, .36, 1, "#111111"), ("SHIPPING SPLIT  ·  DO NOT STACK", .2, 0, "#333333")], bg="#ffffff")


# ------------------------------------------------------------------------------- build
def _build():
    it = fuel.new_item("OPT_MODX", "Skid pre-assembly / pre-wire workstation (modular-yard expansion): work pad, skids "
                       "on cribbing, ready-to-set row, PDC shipping splits", (1996, 2118, 914, 1050), (0, 25), basis="typical",
                       register=False, area="I", sheet="typical (prefab cable installation)",
                       info="Skids wired at waist height on a concrete work pad before setting: JBs, skid-edge tray and conduit mounted, "
                            "skid wiring pulled and terminated, field tails cut to length, coiled and tagged, continuity and "
                            "insulation-resistance tests recorded. Fuel-gas and pump skids in progress; lube-oil skid getting kit 1 and an "
                            "HRSG chemical-feed skid tested and ready to set; a PDC e-house in two shipping splits with pre-terminated "
                            "interconnects coiled at the split. Transformers and large e-houses are set directly (factory-"
                            "integrated) and are not pre-wired on site.")
    fuel.on(it)
    fuel.D = True
    # open-air work pad (x 2000-2050, y 956-1016): no shelter, the crane sets the skids straight from here
    box(2001, 2049, 956, 1016, 0, .12, "concrete")                                  # slab
    cribbing(2004, 2016, 962, 994)
    fuel_gas_skid(2004, 2016, 962, 994, 1.0)
    prewire(2004, 2016, 962, 994, 1.0, done=False, side=1, label="FG-COND SKID FGS-3")
    cribbing(2026, 2035, 966, 990)
    pump_skid(2026, 2035, 966, 990, 1.0)
    prewire(2026, 2035, 966, 990, 1.0, done=False, side=1, label="CW PUMP SKID P-31A/B")
    for (bx, by) in ((2042, 966), (2042, 980)):                                     # workbenches
        box(bx - 2, bx + 2, by - 4, by + 4, 3.0, 3.2, "wood")
        for (sx, sy) in ((-1.8, -3.8), (1.8, -3.8), (-1.8, 3.8), (1.8, 3.8)):
            rod((bx + sx, by + sy, 0), (bx + sx, by + sy, 3.0), .08, "steel", seg=6)
        box(bx - 1.6, bx - .4, by - 3, by - 2, 3.2, 3.8, "sp_yellow")              # megger / test set
        box(bx + .2, bx + 1.6, by + 1, by + 2.4, 3.2, 3.6, "alu")                  # JB on the bench
    box(2040, 2046, 992, 998, 0, .5, "timber")                                     # JB kit pallet
    for k in range(6):
        box(2040.5 + (k % 3) * 1.8, 2041.9 + (k % 3) * 1.8, 992.6 + (k // 3) * 2.6, 994.6 + (k // 3) * 2.6, .5, 2.0, "alu")
    box(2040, 2046, 1001, 1007, 0, .5, "timber")                                   # tray fittings pallet
    for k in range(5):
        box(2040.4, 2045.6, 1001.4 + k * 1.1, 1002.2 + k * 1.1, .5, 1.6, "pipe")
    import simpull as sp
    sp.wire_wagon(2021, 1004)
    sp.spider_box(2034, 1008)
    sp.tripod_light(2021, 975, h=12)
    sp.tripod_light(2038, 1000, h=12)
    person(2017.8, 972, 1.0 + 1.1, math.pi, vest="hivis_o")                         # terminating at the JB (on the skid)
    person(2018.5, 984, 0, math.pi)                                                 # pulling skid wiring
    person(2037, 978, 0, math.pi)                                                   # at the pump skid JB
    person(2044.5, 966, 0, math.pi, vest="hivis_o")                                 # megger at the bench
    # ready-to-set row beside the pad
    cribbing(2062, 2074, 958, 986)
    lube_skid(2062, 2074, 958, 986, 1.0)
    kit_fitup(2062, 2074, 958, 986, 1.0)                                            # kit 1 going on (owner, Oct 26)
    cribbing(2084, 2096, 958, 990)
    chem_feed_skid(2084, 2096, 958, 990, 1.0)                                       # a different skid in the ready row
    prewire(2084, 2096, 958, 990, 1.0, done=True, side=1, label="HRSG CHEM FEED SKID CFS-2")
    decal((2080, 955.8, 4), (0, -1, 0), 10, 2.2, [("READY TO SET", .4, 1, "#ffffff"), ("CFS-2 TESTED  ·  LOS-2 KIT 1 FIT-UP", .2, 0, "#e6e6e6")],
          bg="#2f7a3c")
    rod((2075.5, 956, 0), (2075.5, 956, 5.2), .1, "steel", seg=6)
    rod((2084.5, 956, 0), (2084.5, 956, 5.2), .1, "steel", seg=6)
    person(2078, 970, 0, -.3)                                                       # QA walk-down
    # PDC e-house in two shipping splits (y 922-934), split faces at x 2041 / 2047
    pdc_split(2003, 2041, 922, 934, 1.0, 2041, "PDC-MX  SPLIT A")
    pdc_split(2047, 2085, 922, 934, 1.0, 2047, "PDC-MX  SPLIT B")
    for k in range(4):                                                               # interconnects coiled at the split
        y = 924 + k * 2.6
        rod((2042.5, y, 2.2), (2043.6, y, 2.2), 1.0, ("cable_mv", "cable_tc", "cable_tc", "cable_inst")[k], seg=18)
        rod((2042.4, y, 2.2), (2043.7, y, 2.2), 1.02, "tent", r2=1.02, seg=18)
        rod((2041.05, y, 6.5), (2042.4, y, 2.2), .12, ("cable_mv", "cable_tc", "cable_tc", "cable_inst")[k], seg=8)
    decal((2044, 921.4, 4.5), (0, -1, 0), 4.6, 1.4, [("INTERCONNECTS", .3, 1, "#111111"), ("PRE-TERMINATED  ·  SPLIT A → B", .2, 0, "#333333")],
          bg="#f2c200")
    person(2045, 919, 0, 1.4)
    kits()                                                                           # the three standardized kits
    # three more skid types in the open strip east of the ready row (owner, Oct 26): power skid (kit going on),
    # instrument-air skid (being pre-wired), CEMS shelter (factory-wired, ready to set)
    cribbing(2105, 2117, 954, 984)
    power_skid(2105, 2117, 954, 984, 1.0)
    cribbing(2125, 2135, 954, 974)
    ia_skid(2125, 2135, 954, 974, 1.0)
    prewire(2125, 2135, 954, 974, 1.0, done=False, side=1, label="INSTRUMENT AIR SKID IA-2")
    cems_shelter(2126, 2136, 980, 994, 0.0)
    person(2121.5, 962, 0, math.pi, vest="hivis_o")                                 # landing the MV tails
    person(2131, 970, 1.0 + 1.1, math.pi)                                           # on the IA skid
    fuel.D = False
    return 1


# ------------------------------------------------------------------------------- standardized pre-wired kits
def _kit_label(c, n, lines, w=4.2, h=1.6):
    decal(c, n, w, h, [("SOUTHWIRE", .2, 1, "#b4591f", 1)] + lines, bg="#ffffff", brand=True)
    decal(c, n, w, h, lines, bg="#ffffff", generic_only=True)


def harness_cart(x, y):
    """Kit 1, GT auxiliary skid harness (lube oil): two-tier cart of pre-made, pre-tested harness bundles, each a
    trunk with tagged branches and connectors, laid out in the order they go on the skid."""
    box(x - 3, x + 3, y - 1.5, y + 1.5, .6, .75, "steel")
    box(x - 3, x + 3, y - 1.5, y + 1.5, 2.4, 2.55, "steel")
    for (sx, sy) in ((-2.9, -1.4), (2.9, -1.4), (-2.9, 1.4), (2.9, 1.4)):
        rod((x + sx, y + sy, 0), (x + sx, y + sy, 2.55), .06, "steel", seg=6)
    cols = ("cable_inst", "cable_tc", "cable_armor", "cable_inst", "cable_tc", "cable_inst")
    for k, c in enumerate(cols):
        tz = .75 if k < 3 else 2.55
        cx = x - 2.0 + (k % 3) * 2.0
        rod((cx - .6, y, tz + .35), (cx + .6, y, tz + .35), .35, c, seg=14)                  # coiled trunk
        for j in range(3):                                                                    # branches with connectors
            bx = cx - .5 + j * .5
            rod((bx, y - .3, tz + .35), (bx, y - 1.3, tz + .1), .04, c, seg=4)
            box(bx - .07, bx + .07, y - 1.45, y - 1.25, tz + .02, tz + .18, "alu")
        box(cx + .55, cx + .75, y + .2, y + .4, tz + .5, tz + .8, "white_truck")             # test tag
    _kit_label((x, y - 1.55, 3.6), (0, -1, 0), [("KIT 1  ·  GT AUX SKID HARNESS", .2, 1, "#111111"),
                                               ("lube oil · PLTC / TC-ER / MC-HL", .14, 0, "#333333"),
                                               ("pre-made · pre-tested · tagged by skid point", .13, 0, "#2f7a3c")])
    rod((x - 2.1, y - 1.55, 0), (x - 2.1, y - 1.55, 4.4), .06, "steel", seg=6)
    rod((x + 2.1, y - 1.55, 0), (x + 2.1, y - 1.55, 4.4), .06, "steel", seg=6)


def motor_lead_crate(x, y):
    """Kit 2, pump-skid motor leads: an open crate of pre-terminated MV-105 motor leads (lugs and stress cones on,
    capped) and the instrument harness, sized for one horsepower / voltage band."""
    box(x - 2.4, x + 2.4, y - 1.8, y + 1.8, 0, .4, "timber")
    for (a0, a1, b0, b1) in ((-2.4, 2.4, -1.8, -1.6), (-2.4, 2.4, 1.6, 1.8), (-2.4, -2.2, -1.8, 1.8), (2.2, 2.4, -1.8, 1.8)):
        box(x + a0, x + a1, y + b0, y + b1, .4, 2.0, "timber")
    for k in range(3):                                                                         # three leads, A / B / C
        cx = x - 1.3 + k * 1.3
        rod((cx, y - .6, .9), (cx, y + .6, .9), .55, "cable_mv", seg=16)
        rod((cx, y + .7, 1.4), (cx, y + .7, 2.6), .12, "cable_mv", seg=8)                       # tail up
        rod((cx, y + .7, 2.6), (cx, y + .7, 3.0), .2, "tent", r2=.1, seg=10)                    # stress cone
        box(cx - .1, cx + .1, y + .62, y + .78, 3.0, 3.35, "copper")                            # lug
        box(cx - .25, cx + .25, y + .45, y + .55, 2.2, 2.5, ("red", "sp_yellow", "pvc_blue")[k])   # phase tape
    rod((x + 1.6, y - 1.0, 1.0), (x + 1.6, y + 1.0, 1.0), .35, "cable_inst", seg=12)            # instrument harness
    _kit_label((x, y - 1.85, 3.0), (0, -1, 0), [("KIT 2  ·  PUMP-SKID MOTOR LEADS", .2, 1, "#111111"),
                                               ("MV-105 terminated · instrument harness", .14, 0, "#333333"),
                                               ("one kit per hp / voltage band", .13, 0, "#2f7a3c")])
    for sx in (-2.1, 2.1):
        rod((x + sx, y - 1.85, .4), (x + sx, y - 1.85, 3.8), .06, "steel", seg=6)


def split_kit_reel(x, y):
    """Kit 3, e-house split interconnects: cut-to-length, terminated and tagged sets on a small reel stand, with the
    termination ends bagged, for one standard e-house size."""
    for s_ in (-1.4, 1.4):
        rod((x + s_, y - 1.2, 0), (x + s_, y, 3.2), .07, "steel", seg=6)
        rod((x + s_, y + 1.2, 0), (x + s_, y, 3.2), .07, "steel", seg=6)
    rod((x - 1.7, y, 3.2), (x + 1.7, y, 3.2), .08, "steel", seg=8)
    import simpull
    for sg in (-1, 1):
        simpull.logo_flange((x + sg * 1.1, y, 3.2), (sg, 0), 2.4, .15, spokes=8, gap=.1)
    for k, c in enumerate(("cable_mv", "cable_tc", "cable_tc", "cable_inst")):
        rod((x - 1.0 + k * .5, y, 3.2), (x - .55 + k * .5, y, 3.2), 1.9, c, seg=20)
    for k in range(4):                                                                         # bagged ends hanging
        ex = x - .9 + k * .6
        rod((ex, y - 1.9, 3.0), (ex, y - 2.1, 1.0), .08, ("cable_mv", "cable_tc", "cable_tc", "cable_inst")[k], seg=6)
        rod((ex, y - 2.1, 1.0), (ex, y - 2.1, .4), .2, "tent", seg=8)
    _kit_label((x, y - 2.6, 3.4), (0, -1, 0), [("KIT 3  ·  E-HOUSE SPLIT INTERCONNECTS", .2, 1, "#111111"),
                                              ("cut to length · terminated · tagged", .14, 0, "#333333"),
                                              ("one kit per standard e-house size", .13, 0, "#2f7a3c")], w=4.6)
    for sx in (-2.3, 2.3):
        rod((x + sx, y - 2.6, 0), (x + sx, y - 2.6, 4.2), .06, "steel", seg=6)


def kits():
    harness_cart(2068.0, 996.0)                     # beside the tested lube-oil skid
    motor_lead_crate(2030.5, 996.5)                 # beside the pump skid being pre-wired
    split_kit_reel(2056.0, 920.0)                   # beside the PDC shipping splits
    rows = [("STANDARDIZED PRE-WIRED KITS", .16, 1, "#ffffff"), ("1  GT auxiliary skid harness", .11, 0, "#e6e6e6"),
            ("2  pump-skid motor leads + instrument harness", .11, 0, "#e6e6e6"),
            ("3  e-house split interconnects", .11, 0, "#e6e6e6"),
            ("same kit, every unit · tested before it ships", .1, 1, "#f2c200")]
    decal((2086.0, 995.9, 4.2), (0, -1, 0), 7.0, 3.6, [("SOUTHWIRE", .12, 1, "#e6b089", 1)] + rows, bg="#22303a", brand=True)
    decal((2086.0, 995.9, 4.2), (0, -1, 0), 7.0, 3.6, rows, bg="#22303a", generic_only=True)
    for sx in (-3.2, 3.2):
        rod((2086.0 + sx, 996.0, 0), (2086.0 + sx, 996.0, 6.2), .1, "steel", seg=6)


# laid out at the modular yard first; moved (Oct 23, owner) from the maintenance laydown, where the shared cooling-tower
# cells crowded it, to the open strip between the cable reel yard and the inlet chillers (x 70-206, y 922-1026)
DX, DY = -1931.0, 8.0


def build():
    P, Dc = fuel.G["parts"], fuel.G.setdefault("decals", [])
    n, m = len(P), len(Dc)
    _build()
    it = fuel.G["cur"]
    for p in P[n:]:
        for key in ("min", "max", "a", "b"):
            if key in p:
                p[key][0] = round(p[key][0] + DX, 3)
                p[key][1] = round(p[key][1] + DY, 3)
        for v in p.get("v", ()):
            v[0] = round(v[0] + DX, 3)
            v[1] = round(v[1] + DY, 3)
    for d in Dc[m:]:
        d["c"][0] = round(d["c"][0] + DX, 3)
        d["c"][1] = round(d["c"][1] + DY, 3)
    it["fp"] = [66.0, 208.0, 918.0, 1030.0]
    it["name"] = it["name"].replace("(modular-yard expansion)", "beside the inlet chillers, next to the cable reel yard (modular-yard expansion)")
    it["info"] += (" Set up on the open strip between the cable reel yard and the inlet chillers (away from energised "
                   "plant, contractor access from the west spine road, next to the prefab staging bay and the reels); "
                   "finished skids go out on a lowboy to the modular yard.")
    # area sign at the pad entrance and a lowboy waiting for the first pick (same offsets as the move: +10, -790)
    fuel.on(it)
    fuel.D = True
    ox, oy = 10.0, -790.0
    decal((178 + ox, 1712 + oy, 4.5), (0, -1, 0), 9, 2.6, [("PREFAB / PRE-WIRE AREA", .3, 1, "#ffffff"), ("MODULAR-YARD EXPANSION", .18, 0, "#e6e6e6"),
                                                         ("HARD HAT · SAFETY GLASSES · GLOVES", .16, 1, "#f2c200")], bg="#22303a")
    for x in (173.6, 182.4):
        rod((x + ox, 1712.1 + oy, 0), (x + ox, 1712.1 + oy, 5.8), .1, "steel", seg=6)
    box(150 + ox, 196 + ox, 1806 + oy, 1816 + oy, 2.8, 3.4, "steel_dark")              # lowboy deck
    box(150 + ox, 160 + ox, 1806 + oy, 1816 + oy, 3.4, 5.2, "steel_dark")              # gooseneck
    for xx in (186, 190, 194):
        for s_ in (-1, 1):
            rod((xx + ox, 1811 + oy + s_ * 4.2, 1.6), (xx + ox, 1811 + oy + s_ * 3.0, 1.6), 1.6, "tyre", seg=14)
    for s_ in (-1, 1):
        rod((156 + ox, 1811 + oy + s_ * 3, 2.8), (156 + ox, 1811 + oy + s_ * 3, 0), .2, "steel", seg=6)
    fuel.D = False
    return 1
