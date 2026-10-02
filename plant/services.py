"""Controls and services, site and security at LOD 3 (detail cycle 5).

- Main gate: sliding gate parked open along the fence, inbound and outbound barrier arms by the
  gatehouse, card-reader pedestals, speed table, site entrance sign.
- Perimeter fence: barbed-wire arms angled inward with three strands on every post, CCTV cameras at the
  corners, the gate and along the access road.
- Drainage: catch basins with grates along the road edges about every 150 ft, the stormwater
  basin's inlet headwall with riprap apron and its outlet control structure.
- Site lighting: a handhole at every pole base (buried lighting circuit), photocell boxes.
- Control / admin building: rooftop SCADA / radio mast with antennas, flagpoles, bike rack.
- Warehouse and workshop: a paved service yard to the west spine road, roll-up and personnel doors on
  the west faces, dumpsters, a gas-cylinder cage, pipe and steel stock racks.
- Parking: wheel stops in every bay, bollards at the building fronts.
All typical, not engineered.
"""
import fuel
import wiring as W
from fuel import box, rod, find, on


def dress(flag):
    fuel.D = flag


def _item(name, fp, z, **meta):
    meta.setdefault("register", False)
    return fuel.new_item("SITE", name, fp, z, area="F", sheet="typical (services detail)", **meta)


def routes(add_route):
    # gate operator, barrier arms, card readers and the CCTV at the gate, fed from the gatehouse
    add_route("duct_bank", [(277, 312), (4, 312)], sheet="typical (services detail)")
    # gatehouse LV supply and fibre from the control / admin building
    add_route("duct_bank", [(300, 325), (320, 325), (320, 392)], sheet="typical (services detail)")


def gate():
    it = _item("Main gate: sliding gate, barrier arms, card readers, entrance sign", (0, 60, 236, 312), (0, 12))
    it["wiring"] = ["Gate operator and barrier arms 120 V: Cu THHN/THWN-2 in buried PVC conduit from the gatehouse panel",
                    W.CTRL, "Access control: card readers and intercom on Cat 6A / fibre to the gatehouse", W.GND]
    fuel.D = True
    # sliding gate parked open along the west fence south of the opening
    box(-0 + .3, .9, 240, 270, .3, 8, "fence")
    for y in (240, 255, 270):
        box(.2, 1.0, y - .2, y + .2, 0, 8.6, "steel")
    rod((.6, 240, 8.2), (.6, 270, 8.2), .15, "steel", seg=6)
    # barrier arms (inbound / outbound) by the gatehouse, card readers
    for (y_post, sgn) in ((271.5, 1), (298.5, -1)):
        box(268, 269.6, y_post - .8, y_post + .8, 0, 3.6, "amber")
        rod((268.8, y_post, 3.3), (268.8, y_post + sgn * 13.5, 3.3), .18, "red", seg=6)
        box(262, 263, y_post + sgn * 2.2 - .4, y_post + sgn * 2.2 + .4, 0, 4.2, "panel")    # card reader
    box(272, 278, 270.5, 299.5, .3, .6, "amber")                                         # speed table
    # entrance sign
    for x in (24, 40):
        box(x - .3, x + .3, 303, 303.6, 0, 9, "steel")
    box(23, 41, 302.9, 303.7, 4.5, 9, "sign")
    box(24, 31, 302.85, 302.9, 5.5, 8, "door")
    fuel.D = False


def fence_and_cctv():
    it = _item("Perimeter fence barbed-wire arms and CCTV cameras", (0, 2420, 0, 1920), (0, 22))
    it["wiring"] = ["CCTV power 120 V: Cu THHN/THWN-2 in buried conduit from the nearest lighting panel",
                    "CCTV video: single-mode fibre (PoE media converter at each pole) back to the gatehouse / CR",
                    "Fence grounding: bare Cu tied to the station grid at every corner and gate post", W.GND]
    fuel.D = True
    posts = [(x, y, 0, -1) for x in list(range(20, 2420, 20)) for y in (0.25,)] + \
            [(x, y, 0, 1) for x in list(range(20, 2420, 20)) for y in (1919.75,) if not 1462 < x < 1508] + \
            [(x, y, -1, 0) for y in list(range(20, 1920, 20)) for x in (0.25,) if not (270 <= y <= 300)] + \
            [(x, y, 1, 0) for y in list(range(20, 1920, 20)) for x in (2419.75,)]
    for (x, y, dx, dy) in posts:
        rod((x, y, 8.4), (x - dx * 1.3, y - dy * 1.3, 9.7), .06, "steel", seg=4)            # arm (angled in)
    for (ax, ay, bx, by, dx, dy) in ((0, .25, 2420, .25, 0, -1), (0, 1919.75, 1465, 1919.75, 0, 1),
                                     (1505, 1919.75, 2420, 1919.75, 0, 1),
                                     (.25, 0, .25, 270, -1, 0), (.25, 300, .25, 1920, -1, 0),
                                     (2419.75, 0, 2419.75, 1920, 1, 0)):
        for k in (1, 2, 3):
            o = -.43 * k
            rod((ax + dx * o, ay + dy * o, 8.4 + .43 * k), (bx + dx * o, by + dy * o, 8.4 + .43 * k), .03, "steel", seg=4)
    cams = [(1.2, 1.2), (2418.8, 1.2), (1.2, 1918.8), (2418.8, 1918.8), (40, 266), (300, 266), (1490, 302),
            (1460, 1403), (2380, 1650)]
    for (x, y) in cams:
        rod((x, y, 0), (x, y, 20), .25, "steel", seg=8)
        box(x - .5, x + .5, y - .5, y + .5, 20, 21.2, "panel")
        rod((x, y, 19.4), (x + 1.2, y + 1.2, 19.4), .3, "lamp", seg=8)                     # camera head
    fuel.D = False


def drainage():
    _item("Site drainage: catch basins, Stormwater basin inlet headwall and outlet structure", (0, 2420, 0, 1920), (0, 4))
    fuel.D = True
    roads = [it for it in fuel.G["items"] if it["layer"] == "SITE" and "road" in it["name"].lower()]
    n = 0
    for it in roads:
        x0, x1, y0, y1 = it["fp"]
        zt = it["z"][1]
        if (x1 - x0) >= (y1 - y0):
            for x in range(int(x0) + 60, int(x1) - 30, 150):
                for y in (y0 + 1.5, y1 - 1.5):
                    box(x - 1.5, x + 1.5, y - 1.2, y + 1.2, zt, zt + .04, "fanhub")
                    n += 1
        else:
            for y in range(int(y0) + 60, int(y1) - 30, 150):
                for x in (x0 + 1.5, x1 - 1.5):
                    box(x - 1.2, x + 1.2, y - 1.5, y + 1.5, zt, zt + .04, "fanhub")
                    n += 1
    # stormwater basin (x 40-320, y 1430-1640): inlet headwall with riprap at the north-east corner,
    # outlet control structure at the south-west corner
    box(300, 318, 1622, 1626, -6, 1.2, "concrete")
    rod((309, 1626, -2), (309, 1640, -2), 1.6, "concrete", seg=14)                         # inlet pipe
    for k in range(18):
        box(296 + (k % 6) * 3.4, 299 + (k % 6) * 3.4, 1612 - (k // 6) * 3, 1615 - (k // 6) * 3, -7.6, -6.6 + (k % 3) * .3,
            "rock")
    box(48, 58, 1434, 1442, -8, 2.5, "concrete")                                          # outlet riser
    box(49, 57, 1435, 1441, 2.5, 2.8, "grating")
    fuel.D = False
    return n


def lighting_handholes():
    it = _item("Site lighting: pole handholes and photocells", (0, 2420, 0, 1920), (0, 41))
    it["wiring"] = [W.LIGHT, "Pole circuits 480/277 V: Cu XHHW-2 / USE-2 in buried PVC conduit, handhole at each pole",
                    "Photocell / contactor control from the lighting panels in the e-houses", W.GND]
    fuel.D = True
    poles = [(x, 267) for x in range(120, 2400, 160)] + [(x, 933) for x in range(420, 1480, 160)] + \
            [(367, y) for y in range(340, 1660, 160)] + [(1457, y) for y in range(340, 1400, 160)] + \
            [(x, 1403) for x in range(420, 2400, 160)]
    for (x, y) in poles:
        box(x - 1.6, x - .6, y - .5, y + .5, 0, .35, "concrete")                           # handhole
        box(x - .35, x + .35, y + .45, y + .7, 9, 10.2, "panel")                           # photocell / fuse box
    fuel.D = False


def buildings():
    cr = find("Control / admin building")
    x0, x1, y0, y1 = cr["fp"]
    on(cr)
    dress(True)
    mx, my = x1 - 12, y1 - 10
    rod((mx, my, 20), (mx, my, 52), .35, "steel", r2=.2, seg=8)                            # SCADA / radio mast
    for z, r in ((40, 1.3), (47, 1.0)):
        rod((mx, my, z), (mx, my, z + 6), .12, "lamp", seg=6)
        rod((mx + .8, my, z + 2), (mx + .8 + r, my, z + 2), .08, "steel", seg=4)
    rod((mx - 5, my, 21.5), (mx - 5, my, 23), 2.2, "lamp", r2=1.6, seg=16)                 # dish
    for k, fx in enumerate((x1 - 40, x1 - 34, x1 - 28)):                                  # flagpoles
        rod((fx, y0 - 14, 0), (fx, y0 - 14, 30), .18, "steel", seg=8)
        box(fx + .2, fx + 4.4, y0 - 14.05, y0 - 13.95, 25, 27.6, ("red", "sign", "door")[k])
    for b in range(5):                                                                    # bike rack
        rod((x0 + 10 + b * 2, y0 - 3, 0), (x0 + 10 + b * 2, y0 - 3, 2.5), .07, "steel", seg=4)
    dress(False)
    # paved service yard round the warehouse and workshop, out to the west spine road
    box(100, 370, 455, 655, 0, .15, "road")
    for name in ("Warehouse", "Maintenance building"):
        it = find(name)
        x0, x1, y0, y1 = it["fp"]
        on(it)
        dress(True)
        yd = y0 + (58 if name == "Warehouse" else 16)                                       # west roll-up door
        box(x0 - .25, x0, yd, yd + 14, .15, 16 if name == "Warehouse" else 14, "rollup")
        box(x0 - .6, x0, yd - .6, yd, .15, 16.6 if name == "Warehouse" else 14.6, "amber")
        box(x0 - .6, x0, yd + 14, yd + 14.6, .15, 16.6 if name == "Warehouse" else 14.6, "amber")
        box(x0 - 1.2, x0, yd - .6, yd + 14.6, 16.6 if name == "Warehouse" else 14.6, 17.2 if name == "Warehouse" else 15.2, "steel")
        box(x0 - .25, x0, yd + 16, yd + 19, .15, 7.5, "door")                              # personnel door
        box(x0 - 7, x0 - 1, y0 + 6, y0 + 12, 0, 5, "door")                                 # dumpsters
        box(x0 - 7, x0 - 1, y0 + 14, y0 + 20, 0, 5, "tug")
        if name == "Maintenance building":
            box(x0 - 9, x0 - 1, y1 - 12, y1 - 4, 0, 7, "fence")                            # gas-cylinder cage
            for k in range(6):
                rod((x0 - 7.5 + (k % 3) * 2.5, y1 - 10 + (k // 3) * 3, 0), (x0 - 7.5 + (k % 3) * 2.5, y1 - 10 + (k // 3) * 3, 4.6),
                    .4, ("amber", "door", "red")[k % 3], seg=8)
            for k in range(3):                                                             # pipe / steel stock racks
                xr = x0 - 30 + k * 6
                box(xr - .3, xr + .3, y0 + 2, y0 + 30, 0, 6, "steel")
                for z in (2, 4, 6):
                    box(xr - 2.5, xr + 2.5, y0 + 2, y0 + 2.4, z - .2, z, "steel")
                    box(xr - 2.5, xr + 2.5, y0 + 29.6, y0 + 30, z - .2, z, "steel")
                    for p in range(4):
                        rod((xr - 2 + p * 1.3, y0 + 2, z + .3), (xr - 2 + p * 1.3, y0 + 30, z + .3), .25, "pipe", seg=8)
        dress(False)


def parking():
    _item("Parking wheel stops and bollards", (40, 320, 60, 400), (0, 4))
    fuel.D = True
    for k in range(7):                                        # double rows either side of each divider
        x = 60.5 + 36 * k
        for s in (-1, 1):
            xs = x + s * 16
            if not 42 < xs < 318:
                continue
            for y in range(84, 220, 9):
                box(xs - .3, xs + .3, y + 1, y + 7, .2, .7, "concrete")
    cr = find("Control / admin building")
    x0, x1, y0, y1 = cr["fp"]
    for x in range(int(x0) + 6, int(x1) - 4, 12):
        rod((x, y0 - 4, 0), (x, y0 - 4, 3.5), .35, "amber", seg=10)
    fuel.D = False


def build():
    gate()
    fence_and_cctv()
    n = drainage()
    lighting_handholes()
    buildings()
    parking()
    return n
