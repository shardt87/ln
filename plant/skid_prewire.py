"""Skid pre-assembly / pre-wire workstation for the modular-yard expansion, in the drawn maintenance laydown
(north-west corner, gravel, fenced): away from energised plant, reached from the west spine road, the east half of
the laydown left clear for engine / turbine exchanges. Finished skids go out on a lowboy to the modular yard.

On an expansion the electrical crew wires skids at waist height under cover before the crane sets them: junction
boxes, skid-edge tray and conduit are mounted, the skid wiring is pulled and terminated, the field tails are cut to
length, coiled and tagged, and continuity / insulation-resistance (megger) tests are recorded. Here:
- a fabric shelter (arched frame, roll-up east side, open south end) as the workstation, with a fuel-gas
  conditioning skid and a pump skid on cribbing being pre-wired, workbenches, a wire wagon, test gear, JB and
  tray-fitting kits, temporary power and lights, and the crew;
- a ready-to-set row outside: a lube-oil skid and a second fuel-gas skid, finished and tagged TESTED - READY TO SET;
- a PDC e-house delivered in two shipping splits on cribbing, the split faces wrapped, with pre-terminated
  interconnect cables coiled at the split ready to reconnect once set.
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


# ------------------------------------------------------------------------------- shelter
def shelter(cx, y0, y1, W=50.0, H=24.0, wall=2.0, open_east=.55):
    """Arched fabric shelter along y: ribs every 10 ft, ballast blocks, fabric panels (east side rolled up)."""
    a, b = W / 2, H - wall
    n = 14
    ts = [math.pi * k / n for k in range(n + 1)]
    P = lambda t, r=0.0: (cx + (a + r) * math.cos(t), wall + (b + r) * math.sin(t))
    for k in range(n):
        t0, t1 = ts[k], ts[k + 1]
        if t1 <= open_east:
            continue
        (x0, z0), (x1, z1) = P(t0), P(t1)
        (X0, Z0), (X1, Z1) = P(t0, .12), P(t1, .12)
        hexpart([(x0, y1, z0), (x1, y1, z1), (x1, y0, z1), (x0, y0, z0),
                 (X0, y1, Z0), (X1, y1, Z1), (X1, y0, Z1), (X0, y0, Z0)], "tent")
    (xr, zr) = P(open_east)
    rod((xr, y0, zr - .3), (xr, y1, zr - .3), .5, "tent", seg=12)                      # rolled-up east curtain
    for y in [y0 + 10 * k for k in range(int((y1 - y0) / 10) + 1)]:
        for k in range(n):
            (x0, z0), (x1, z1) = P(ts[k], -.15), P(ts[k + 1], -.15)
            rod((x0, y, z0), (x1, y, z1), .18, "steel", seg=6)
        for s in (-1, 1):
            rod((cx + s * a, y, 0), (cx + s * a, y, wall), .18, "steel", seg=6)
            box(cx + s * a - 1, cx + s * a + 1, y - 1, y + 1, 0, 1.0, "concrete")   # ballast block
    for k in (3, 7, 11):                                                               # purlins
        (x0, z0) = P(ts[k], -.2)
        rod((x0, y0, z0), (x0, y1, z0), .1, "steel", seg=6)


# ------------------------------------------------------------------------------- skids
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
    it = fuel.new_item("OPT_MODX", "Skid pre-assembly / pre-wire workstation (modular-yard expansion): fabric shelter, skids "
                       "on cribbing, ready-to-set row, PDC shipping splits", (1996, 2118, 914, 1050), (0, 25), basis="typical",
                       register=False, area="I", sheet="typical (prefab cable installation)",
                       info="Skids wired at waist height under cover before setting: JBs, skid-edge tray and conduit mounted, "
                            "skid wiring pulled and terminated, field tails cut to length, coiled and tagged, continuity and "
                            "insulation-resistance tests recorded. Fuel-gas and pump skids in progress; lube-oil and a second "
                            "fuel-gas skid tested and ready to set; a PDC e-house in two shipping splits with pre-terminated "
                            "interconnects coiled at the split. Transformers and large e-houses are set directly (factory-"
                            "integrated) and are not pre-wired on site.")
    fuel.on(it)
    fuel.D = True
    # shelter (x 2000-2050, y 956-1016), open to the south, east side rolled up
    shelter(2025, 956, 1016)
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
    # ready-to-set row outside the shelter
    cribbing(2062, 2074, 958, 986)
    lube_skid(2062, 2074, 958, 986, 1.0)
    prewire(2062, 2074, 958, 986, 1.0, done=True, side=1, label="LUBE OIL SKID LOS-2")
    cribbing(2084, 2096, 958, 990)
    fuel_gas_skid(2084, 2096, 958, 990, 1.0)
    prewire(2084, 2096, 958, 990, 1.0, done=True, side=1, label="FG-COND SKID FGS-4")
    decal((2080, 955.8, 4), (0, -1, 0), 10, 2.2, [("READY TO SET", .4, 1, "#ffffff"), ("SKIDS TESTED  ·  CRANE PICK ORDER 1-2", .2, 0, "#e6e6e6")],
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
    fuel.D = False
    return 1


# laid out at the modular yard first, moved into the maintenance laydown (x 45-405, y 1705-1880), west half
DX, DY = -1941.0, 798.0


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
    it["fp"] = [it["fp"][0] + DX, it["fp"][1] + DX, it["fp"][2] + DY, it["fp"][3] + DY]
    it["name"] = it["name"].replace("(modular-yard expansion)", "in the maintenance laydown (modular-yard expansion)")
    it["info"] += (" Set up in the maintenance laydown (away from energised plant, contractor access from the west spine "
                   "road); finished skids go out on a lowboy to the modular yard. East half kept clear for engine / "
                   "turbine exchanges.")
    # area sign at the laydown entrance and a lowboy waiting for the first pick
    fuel.on(it)
    fuel.D = True
    decal((178, 1712, 4.5), (0, -1, 0), 9, 2.6, [("PREFAB / PRE-WIRE AREA", .3, 1, "#ffffff"), ("MODULAR-YARD EXPANSION", .18, 0, "#e6e6e6"),
                                                 ("HARD HAT · SAFETY GLASSES · GLOVES", .16, 1, "#f2c200")], bg="#22303a")
    for x in (173.6, 182.4):
        rod((x, 1712.1, 0), (x, 1712.1, 5.8), .1, "steel", seg=6)
    box(150, 196, 1806, 1816, 2.8, 3.4, "steel_dark")                                  # lowboy deck
    box(150, 160, 1806, 1816, 3.4, 5.2, "steel_dark")                                  # gooseneck
    for xx in (186, 190, 194):
        for s_ in (-1, 1):
            rod((xx, 1811 + s_ * 4.2, 1.6), (xx, 1811 + s_ * 3.0, 1.6), 1.6, "tyre", seg=14)
    for s_ in (-1, 1):
        rod((156, 1811 + s_ * 3, 2.8), (156, 1811 + s_ * 3, 0), .2, "steel", seg=6)
    fuel.D = False
    return 1
