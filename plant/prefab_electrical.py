"""Prefab electrical yard beside the pre-wire pad (owner, Oct 26): factory-built electrical equipment staged for the
modular / phase-2 work, and a panel shop, with cabinets opened so the inside can be seen. Free strip east of the
pre-wire pad, west of the spine road (x 218-358, y 928-1024):
- delivery lineup on dunnage (doors face south): a 15 kV metal-clad switchgear lineup (six sections; two doors open
  on a racked-out vacuum breaker and on the relay / LV compartment, one breaker out on its lift truck); a VFD lineup
  (five sections; doors open on the rectifier / inverter power modules with heat-sink fins, DC bus, input reactor,
  cooling fans and the control section); a UPS set (UPS module, bypass cabinet and three battery cabinets, doors open
  on the battery strings and the power modules);
- panel shop: an open-sided steel shelter with LED high-bays; benches with back-panels being built (DIN rail, wire
  duct, terminal blocks, breakers, relays, a PLC rack, wiring in progress); three enclosures standing open against the
  back wall, nearly finished; a back-panel on an easel; a wire-spool rack; a duct / DIN-rail stock rack; a test bench;
  the crew.
Typical, not engineered."""
import math

import fuel
from fuel import box, rod

TB = ("pvc_grey", "pvc_grey", "pvc_blue", "pvc_grey", "sp_yellow", "pvc_grey", "pvc_green")   # terminal-block colours
WIRE = ("cable_tc", "red", "pvc_blue", "white_truck", "cable_tc")


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, a=0.0, vest="hivis", z=0.0, hat="hardhat"):
    import maintenance
    maintenance.person(x, y, z, a, vest=vest, hat=hat)


# --------------------------------------------------------------------------------------------- cabinet building blocks
def carcass(x0, x1, y0, y1, z0, h, col, door=None, door_col=None):
    """Cabinet shell open at the front (y0 face): back, sides, top, plinth. door: None (closed front), 'open' (door
    swung ~100 deg out from the x0 hinge)."""
    box(x0, x1, y1 - .08, y1, z0, z0 + h, col)                                   # back
    for xs in (x0, x1 - .08):
        box(xs, xs + .08, y0, y1, z0, z0 + h, col)                               # sides
    box(x0, x1, y0, y1, z0 + h - .08, z0 + h, col)                               # top
    box(x0, x1, y0 + .1, y1, z0, z0 + .35, "steel_dark")                         # plinth
    if door is None:
        box(x0 + .04, x1 - .04, y0, y0 + .06, z0 + .35, z0 + h - .08, door_col or col)
        rod((x1 - .3, y0 - .05, z0 + h * .5), (x1 - .3, y0 - .05, z0 + h * .5 + .5), .04, "steel", seg=6)   # handle
    else:
        w = x1 - x0
        box(x0 - .06, x0, y0 - w + .05, y0, z0 + .4, z0 + h - .12, door_col or col)       # door swung open
        box(x0 - .1, x0 - .06, y0 - w * .7, y0 - w * .3, z0 + h * .55, z0 + h * .8, "white_truck")   # drawing pocket


def back_panel(x0, x1, yb, z0, z1, rows=4, dense=True):
    """Mounting plate facing -y at yb with the panel build on it: wire duct grid, DIN rails, terminal blocks, breakers,
    relays, wiring between them."""
    box(x0, x1, yb, yb + .05, z0, z1, "white_truck")
    for xd in (x0 + .25, x1 - .25):
        box(xd - .12, xd + .12, yb - .22, yb, z0 + .1, z1 - .1, "pvc_grey")     # vertical duct
    zs = [z0 + (z1 - z0) * (k + .5) / rows for k in range(rows)]
    for z in zs:
        box(x0 + .37, x1 - .37, yb - .22, yb, z + .45, z + .62, "pvc_grey")      # horizontal duct above each rail
        box(x0 + .4, x1 - .4, yb - .06, yb, z - .03, z + .03, "steel")          # DIN rail
        x = x0 + .45
        k = 0
        while x < x1 - .5:
            if k % 9 < 5 or not dense:
                box(x, x + .07, yb - .2, yb - .06, z - .18, z + .18, TB[k % len(TB)])   # terminal block
                x += .08
            else:
                box(x, x + .14, yb - .26, yb - .06, z - .22, z + .22, ("sp_black", "white_truck", "sp_black", "sp_yellow")[k % 4])  # breaker / relay
                x += .16
            k += 1
        for j in range(0, int((x1 - x0) / .35)):                                 # wires from the devices up into the duct
            xw = x0 + .5 + j * .35
            if xw < x1 - .5:
                rod((xw, yb - .12, z + .2), (xw, yb - .12, z + .45), .012, WIRE[j % len(WIRE)], seg=4)
    return zs


# --------------------------------------------------------------------------------------------- the delivery lineup
def dunnage(x0, x1, y0, y1):
    for x in (x0 + .5, (x0 + x1) / 2, x1 - .5):
        box(x - .3, x + .3, y0 - .3, y1 + .3, 0, .5, "timber")


def switchgear_lineup(x0, y0):
    """15 kV metal-clad switchgear, six 3.33 ft sections, 8 ft deep, 8 ft tall, doors to the south."""
    w, d, h, z = 3.33, 8.0, 8.0, .5
    dunnage(x0, x0 + 6 * w, y0, y0 + d)
    for k in range(6):
        sx0 = x0 + k * w
        if k in (2, 4):
            carcass(sx0, sx0 + w, y0, y0 + d, z, h, "swgr", door="open")
            if k == 2:                                                            # breaker compartment, breaker racked out
                box(sx0 + .1, sx0 + w - .1, y0 + .1, y0 + 3.4, z + .35, z + .45, "steel")          # rails
                box(sx0 + .5, sx0 + w - .5, y0 + 1.6, y0 + 3.6, z + .5, z + 3.6, "sp_black")       # vacuum breaker
                for j in range(3):
                    rod((sx0 + .9 + j * .75, y0 + 3.6, z + 2.6), (sx0 + .9 + j * .75, y0 + 4.6, z + 2.6), .12, "copper", seg=8)   # primary fingers
                    rod((sx0 + .9 + j * .75, y0 + 3.6, z + 1.2), (sx0 + .9 + j * .75, y0 + 4.6, z + 1.2), .12, "copper", seg=8)
                for j in range(3):                                                # stationary contacts and bushings in the back
                    rod((sx0 + .9 + j * .75, y0 + 6.0, z + 2.6), (sx0 + .9 + j * .75, y0 + 7.4, z + 2.6), .2, "insulator", seg=10)
                    rod((sx0 + .9 + j * .75, y0 + 6.0, z + 1.2), (sx0 + .9 + j * .75, y0 + 7.4, z + 1.2), .2, "insulator", seg=10)
                box(sx0 + .1, sx0 + w - .1, y0 + .1, y0 + d - .1, z + 4.6, z + 4.7, "steel")        # compartment barrier
                back_panel(sx0 + .2, sx0 + w - .2, y0 + 1.2, z + 4.9, z + h - .4, rows=2, dense=False)   # LV / relay compartment
                for j in range(2):
                    box(sx0 + .6 + j * 1.2, sx0 + 1.4 + j * 1.2, y0 + .9, y0 + 1.2, z + 6.6, z + 7.4, "hmi")   # protection relays
            else:                                                                 # cable compartment: the termination space
                for j in range(3):
                    rod((sx0 + .9 + j * .75, y0 + 5.5, z + .5), (sx0 + .9 + j * .75, y0 + 5.5, z + 4.2), .1, "copper", seg=8)  # bus risers
                    rod((sx0 + .9 + j * .75, y0 + 5.5, z + 3.0), (sx0 + .9 + j * .75, y0 + 4.6, z + 3.0), .08, "copper", seg=6)
                box(sx0 + .2, sx0 + w - .2, y0 + 7.2, y0 + 7.4, z + .4, z + .6, "copper")           # ground bus
                box(sx0 + .3, sx0 + w - .3, y0 + 1.0, y0 + 7.0, z + .35, z + .45, "steel_dark")      # gland plate (floor)
        else:
            carcass(sx0, sx0 + w, y0, y0 + d, z, h, "swgr")
            for j in range(2):                                                    # relay windows on the closed doors
                box(sx0 + .5 + j * 1.3, sx0 + 1.2 + j * 1.3, y0 - .02, y0, z + 6.4, z + 7.0, "hmi")
            box(sx0 + .6, sx0 + w - .6, y0 - .02, y0, z + 1.4, z + 2.2, "steel_dark")             # breaker viewing window
    # a second breaker out on its lift truck in front of section 3
    bx = x0 + 3 * w + w / 2
    box(bx - 1.2, bx + 1.2, y0 - 5.0, y0 - 2.6, 0, .4, "sp_yellow")
    for sx in (-1.0, 1.0):
        rod((bx + sx, y0 - 4.8, 0), (bx + sx, y0 - 4.8, 6.0), .1, "sp_yellow", seg=8)
    box(bx - .9, bx + .9, y0 - 4.6, y0 - 2.7, 1.6, 4.7, "sp_black")
    for j in range(3):
        rod((bx - .75 + j * .75, y0 - 2.7, 3.7), (bx - .75 + j * .75, y0 - 1.9, 3.7), .1, "copper", seg=8)
    decal((x0 + 3 * w, y0 - .1, z + h + .9), (0, -1, 0), 10.0, 1.2,
          [("15 kV METAL-CLAD SWITCHGEAR  ·  6 SECTIONS", .42, 1, "#111111"), ("factory-tested · shipping split 1 of 2", .3, 0, "#333333")],
          bg="#ffffff")
    for sx in (x0 + 3 * w - 4.6, x0 + 3 * w + 4.6):
        rod((sx, y0 - .1, 0), (sx, y0 - .1, z + h + 1.5), .06, "steel", seg=6)


def vfd_lineup(x0, y0):
    """Medium-size VFD lineup: five 3.6 ft sections (input / reactor, two drive, two control), 2.6 ft deep, 7.5 ft."""
    w, d, h, z = 3.6, 2.6, 7.5, .5
    dunnage(x0, x0 + 5 * w, y0, y0 + d)
    for k in range(5):
        sx0 = x0 + k * w
        if k in (1, 2, 4):
            carcass(sx0, sx0 + w, y0, y0 + d, z, h, "panel_in", door="open", door_col="swgr")
            if k in (1, 2):                                                       # power modules
                for j in range(3):
                    mz = z + 1.0 + j * 1.9
                    box(sx0 + .4, sx0 + w - .4, y0 + 1.0, y0 + 2.4, mz, mz + 1.5, "panel")          # module
                    for f in range(8):
                        fx = sx0 + .55 + f * (w - 1.1) / 7
                        box(fx - .03, fx + .03, y0 + .6, y0 + 1.0, mz + .1, mz + 1.4, "alu")       # heat-sink fins
                    box(sx0 + .5, sx0 + 1.3, y0 + .55, y0 + .6, mz + .9, mz + 1.3, "white_truck")   # module label
                for j in range(3):
                    box(sx0 + .6 + j * .9, sx0 + .75 + j * .9, y0 + .3, y0 + 2.4, z + h - .9, z + h - .7, "copper")   # DC bus
                rod((sx0 + w / 2, y0 + .3, z + h - .4), (sx0 + w / 2, y0 + .1, z + h - .4), .55, "fanhub", seg=16)   # fan
            else:                                                                 # control section
                back_panel(sx0 + .2, sx0 + w - .2, y0 + 2.4, z + .6, z + h - .4, rows=5)
                box(sx0 + .8, sx0 + 2.4, y0 + 2.1, y0 + 2.35, z + 5.4, z + 6.4, "panel")           # PLC / drive controller
                box(sx0 + 1.0, sx0 + 2.2, y0 + 2.08, y0 + 2.1, z + 5.6, z + 6.2, "hmi")
        else:
            carcass(sx0, sx0 + w, y0, y0 + d, z, h, "panel_in", door_col="swgr")
            box(sx0 + 1.2, sx0 + 2.4, y0 - .03, y0, z + 4.6, z + 5.4, "hmi")                       # keypad / display
            for j in range(4):
                box(sx0 + .5, sx0 + w - .5, y0 - .02, y0, z + h - 1.6 + j * .25, z + h - 1.5 + j * .25, "louvre")
    decal((x0 + 2.5 * w, y0 - .1, z + h + .9), (0, -1, 0), 9.0, 1.2,
          [("VFD LINEUP  ·  480 V  ·  FIVE SECTIONS", .42, 1, "#111111"), ("power modules · DC bus · control section", .3, 0, "#333333")],
          bg="#ffffff")
    for sx in (x0 + 2.5 * w - 4.1, x0 + 2.5 * w + 4.1):
        rod((sx, y0 - .1, 0), (sx, y0 - .1, z + h + 1.5), .06, "steel", seg=6)


def ups_set(x0, y0):
    """UPS module (4 ft), bypass cabinet (2.5 ft) and three battery cabinets (3 ft), 3 ft deep, 7 ft tall."""
    d, h, z = 3.0, 7.0, .5
    widths = (4.0, 2.5, 3.0, 3.0, 3.0)
    dunnage(x0, x0 + sum(widths), y0, y0 + d)
    x = x0
    for k, w in enumerate(widths):
        if k in (0, 2, 3):
            carcass(x, x + w, y0, y0 + d, z, h, "panel_in", door="open", door_col="white_truck")
            if k == 0:                                                            # rectifier / inverter power modules in a rack
                for j in range(4):
                    mz = z + .8 + j * 1.45
                    box(x + .3, x + w - .3, y0 + .5, y0 + 2.7, mz, mz + 1.2, "panel")
                    box(x + .4, x + 1.2, y0 + .45, y0 + .5, mz + .3, mz + .9, "led_g")
                    for f in range(5):
                        box(x + 1.5 + f * .45, x + 1.6 + f * .45, y0 + .45, y0 + .5, mz + .2, mz + 1.0, "fanhub")
            else:                                                                 # battery strings on shelves
                for j in range(5):
                    sz = z + .5 + j * 1.25
                    box(x + .15, x + w - .15, y0 + .3, y0 + 2.8, sz, sz + .08, "steel")              # shelf
                    for b in range(4):
                        bx = x + .25 + b * (w - .5) / 4
                        box(bx, bx + (w - .5) / 4 - .08, y0 + .5, y0 + 2.6, sz + .08, sz + .95, "battery")
                        rod((bx + .1, y0 + .45, sz + .9), (bx + (w - .5) / 4 - .18, y0 + .45, sz + .9), .03, "copper", seg=4)   # links
        else:
            carcass(x, x + w, y0, y0 + d, z, h, "panel_in", door_col="white_truck")
            box(x + .5, x + w - .5, y0 - .03, y0, z + 4.4, z + 5.4, "hmi")
        x += w
    decal((x0 + sum(widths) / 2, y0 - .1, z + h + .9), (0, -1, 0), 8.0, 1.2,
          [("UPS  ·  BYPASS  ·  3 BATTERY CABINETS", .42, 1, "#111111"), ("power modules · battery strings · DC links", .3, 0, "#333333")],
          bg="#ffffff")
    for sx in (x0 + sum(widths) / 2 - 3.6, x0 + sum(widths) / 2 + 3.6):
        rod((sx, y0 - .1, 0), (sx, y0 - .1, z + h + 1.5), .06, "steel", seg=6)


# --------------------------------------------------------------------------------------------- the panel shop
def shelter(x0, x1, y0, y1, eave=16.0):
    """Open-sided steel shelter: columns every ~14 ft on both long sides, rafters, a mono-pitch roof, a clad back wall
    (north), LED high-bays under the roof."""
    nx = int((x1 - x0) / 14)
    for i in range(nx + 1):
        x = x0 + i * (x1 - x0) / nx
        for y in (y0, y1):
            box(x - .4, x + .4, y - .4, y + .4, 0, eave + (1.0 if y == y1 else 0), "steel_dark")
        rod((x, y0, eave), (x, y1, eave + 1.0), .3, "steel_dark", seg=6)                    # rafter
    for k in range(10):                                                                      # roof sheets, sloped
        ya, yb_ = y0 - 2.0 + k * (y1 - y0 + 2.5) / 10, y0 - 2.0 + (k + 1) * (y1 - y0 + 2.5) / 10
        za = eave + .4 + (ya - y0) / (y1 - y0)
        box(x0 - 1.0, x1 + 1.0, ya, yb_ + .05, za, za + .25, "roof")
    box(x0, x1, y1 - .2, y1, 0, eave + .8, "building")                                       # back wall
    for xe in (x0, x1):
        box(xe - .1, xe + .1, y1 - 12.0, y1, 0, eave, "building")                           # short end returns
    box(x0 - .1, x1 + .1, y0 - .5, y0, eave - 1.6, eave + .2, "white_truck")                # fascia
    for i in range(nx):
        for y in (y0 + 10.0, y1 - 10.0):
            x = x0 + (i + .5) * (x1 - x0) / nx
            rod((x, y, eave - .4), (x, y, eave - 1.6), .02, "steel", seg=4)
            box(x - 1.0, x + 1.0, y - .7, y + .7, eave - 1.9, eave - 1.6, "lamp")                # LED high-bay


def bench(x, y, with_panel=True):
    box(x - 4.0, x + 4.0, y - 1.6, y + 1.6, 3.0, 3.2, "wood")
    for (sx, sy) in ((-3.8, -1.4), (3.8, -1.4), (-3.8, 1.4), (3.8, 1.4)):
        rod((x + sx, y + sy, 0), (x + sx, y + sy, 3.0), .08, "steel", seg=6)
    box(x - 3.9, x + 3.9, y - 1.5, y + 1.5, 1.0, 1.1, "steel")                               # lower shelf
    if with_panel:                                                                             # back-panel laid flat, mid-build
        box(x - 2.6, x + 2.6, y - 1.2, y + 1.2, 3.2, 3.25, "white_truck")
        for yy in (y - .8, y, y + .8):
            box(x - 2.2, x + 2.2, yy - .03, yy + .03, 3.25, 3.3, "steel")                     # DIN rails
            for k in range(14):
                xx = x - 2.1 + k * .3
                box(xx, xx + .07, yy - .18, yy + .18, 3.3, 3.45, TB[k % len(TB)])
        for xd in (x - 2.45, x + 2.45):
            box(xd - .12, xd + .12, y - 1.15, y + 1.15, 3.25, 3.47, "pvc_grey")               # wire duct
        for k in range(6):                                                                     # loose wire ends
            rod((x - 1.5 + k * .5, y + .3, 3.46), (x - 1.3 + k * .5, y + 1.4, 3.3), .015, WIRE[k % len(WIRE)], seg=4)
    box(x + 2.8, x + 3.6, y - 1.2, y - .4, 3.2, 3.5, "sp_yellow")                              # crimp / strip tool case


def standing_enclosure(x0, y1, w=3.0, d=2.0, h=7.0):
    """Floor-standing enclosure against the back wall, door open, internals nearly finished."""
    carcass(x0, x0 + w, y1 - d, y1, 0, h, "panel_in", door="open", door_col="swgr")
    back_panel(x0 + .2, x0 + w - .2, y1 - .1, .7, h - .4, rows=5)
    box(x0 + .3, x0 + w - .3, y1 - d + .1, y1 - .1, .4, .5, "steel_dark")                    # gland plate
    for j in range(5):
        rod((x0 + .6 + j * .45, y1 - 1.0, .1), (x0 + .6 + j * .45, y1 - 1.0, .5), .06, ("cable_tc", "cable_inst", "cable_tc", "cable_fo", "cable_tc")[j], seg=6)


def easel(x, y):
    for s in (-1.4, 1.4):
        rod((x + s, y + .9, 0), (x + s * .8, y, 6.2), .06, "steel", seg=6)
        rod((x + s, y - .9, 0), (x + s * .8, y, 6.2), .06, "steel", seg=6)
    zs = [1.8 + k * .9 for k in range(5)]
    box(x - 1.4, x + 1.4, y - .05, y, 1.4, 6.2, "white_truck")
    for z in zs:
        box(x - 1.2, x + 1.2, y - .08, y - .05, z - .03, z + .03, "steel")
        for k in range(14):
            box(x - 1.15 + k * .16, x - 1.08 + k * .16, y - .2, y - .08, z - .15, z + .15, TB[k % len(TB)])


def spool_rack(x, y):
    box(x - 3.0, x + 3.0, y - 1.0, y + 1.0, 0, .2, "steel")
    for s in (-2.9, 2.9):
        rod((x + s, y, 0), (x + s, y, 5.2), .08, "steel", seg=6)
    for row, z in enumerate((1.4, 3.0, 4.6)):
        rod((x - 3.0, y, z), (x + 3.0, y, z), .05, "steel", seg=6)
        for k in range(6):
            sx = x - 2.4 + k * .95
            rod((sx - .3, y, z), (sx + .3, y, z), .55, "sp_black", seg=14)
            rod((sx - .25, y, z), (sx + .25, y, z), .45, WIRE[(k + row) % len(WIRE)] if (k + row) % 3 else "pvc_green", seg=14)


def stock_rack(x, y):
    for s in (-.9, .9):
        rod((x + s, y, 0), (x + s, y, 6.0), .08, "steel", seg=6)
    for z in (1.5, 3.0, 4.5):
        rod((x - .9, y, z), (x + .9, y, z), .05, "steel", seg=6)
    for k in range(10):                                                                         # duct / DIN-rail lengths
        z = 1.6 + (k // 5) * 1.5
        box(x - .8 + (k % 5) * .32, x - .62 + (k % 5) * .32, y - 3.3, y + 3.3, z, z + .18, "pvc_grey" if k < 5 else "steel")


def test_bench(x, y):
    bench(x, y, with_panel=False)
    box(x - 2.4, x - .6, y - .6, y + .8, 3.2, 4.4, "sp_yellow")                                # IR / hipot tester
    box(x - .2, x + 1.6, y - .2, y + .6, 3.2, 4.6, "panel")                                     # laptop / monitor
    box(x - .1, x + 1.5, y - .22, y - .2, 3.5, 4.4, "hmi")
    rod((x - 1.5, y - .6, 3.6), (x - 1.0, y - 2.2, 3.2), .02, "red", seg=4)                     # test leads
    rod((x - 1.2, y - .6, 3.6), (x - .6, y - 2.2, 3.2), .02, "cable_tc", seg=4)


def panel_shop(x0, x1, y0, y1):
    box(x0 - 1.5, x1 + 1.5, y0 - 3.0, y1 + .5, 0, .15, "concrete")                             # slab
    shelter(x0, x1, y0, y1)
    for k, bx in enumerate((x0 + 8.0, x0 + 22.0, x0 + 36.0, x0 + 50.0)):
        bench(bx, y0 + 11.0)
    for k, ex in enumerate((x0 + 4.0, x0 + 16.0, x0 + 28.0)):
        standing_enclosure(ex, y1 - .3)
    easel(x0 + 44.0, y1 - 8.0)
    spool_rack(x1 - 6.0, y1 - 2.0)
    stock_rack(x0 + 40.0, y1 - 4.0)
    test_bench(x1 - 6.0, y0 + 11.0)
    for (px, py, a, v) in ((x0 + 8.0, y0 + 8.8, math.pi / 2, "hivis"), (x0 + 22.5, y0 + 8.8, math.pi / 2, "hivis_o"),
                           (x0 + 36.0, y0 + 13.4, -math.pi / 2, "hivis"), (x0 + 5.5, y1 - 4.0, math.pi / 2, "hivis_o"),
                           (x1 - 6.0, y0 + 8.8, math.pi / 2, "hivis")):
        person(px, py, a, v)
    decal(((x0 + x1) / 2, y0 - .52, 15.2), (0, -1, 0), 14.0, 1.2, [("PANEL SHOP  ·  CONTROL AND POWER PANELS", .5, 1, "#111111")],
          bg="#ffffff")


def build():
    it = fuel.new_item("OPT_MODX", "Prefab electrical yard: switchgear, VFD and UPS lineups (opened), panel shop",
                       (216, 360, 926, 1026), (0, 18), basis="typical", register=False, area="F",
                       sheet="typical (prefab electrical)",
                       info="Factory-built electrical equipment staged beside the pre-wire pad: a 15 kV metal-clad switchgear "
                            "lineup (a breaker racked out, a relay compartment and a cable compartment open, a breaker on its "
                            "lift truck), a VFD lineup (power modules with heat sinks, DC bus, fans, control section), a UPS "
                            "with bypass and battery cabinets (power modules, battery strings); and an open-sided panel shop "
                            "with benches, back-panels being built (DIN rail, wire duct, terminal blocks, breakers, relays), "
                            "enclosures standing open, an easel, wire spools, stock rack, test bench and the crew. Typical.")
    fuel.on(it)
    fuel.D = True
    box(218, 358, 928, 966, 0, .12, "concrete")                                                 # lineup slab
    switchgear_lineup(224.0, 944.0)
    vfd_lineup(254.0, 946.0)
    ups_set(282.0, 946.0)
    person(240.0, 937.0, math.pi / 2)
    person(262.0, 941.5, math.pi / 2, vest="hivis_o")
    person(286.0, 941.5, math.pi / 2)
    panel_shop(226.0, 296.0, 984.0, 1020.0)
    rows = [("PREFAB ELECTRICAL", .18, 1, "#ffffff"), ("modular switchgear · VFD · UPS · panel shop", .12, 0, "#e6e6e6"),
            ("built, tested and wired before it is set", .11, 1, "#f2c200")]
    decal((318.0, 939.9, 4.4), (0, -1, 0), 7.0, 2.8, rows, bg="#22303a")
    for sx in (314.8, 321.2):
        rod((sx, 940.0, 0), (sx, 940.0, 6.0), .1, "steel", seg=6)
    fuel.D = False
    return 1
