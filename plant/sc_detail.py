"""SC-1 / SC-2 simple-cycle units, second LOD 3 pass (owner, Oct 21: improve the simple-cycle model and its
details). Built in drawn coordinates right after modular.simple_cycle(); every part sits on an item named "SC-k ...",
so sc2_mirror.build() turns SC-2's set end for end with the rest of the unit. What a real LM6000-class site has and
the first pass left out:
- inlet: a tapered transition out of the filter house, a silencer duct over the generator with its stiffener bands
  and expansion joint, and the inlet plenum dropping into the turbine enclosure;
- enclosures: panel joints on the generator enclosure, ventilation louvres, a vent-exhaust silencer on the turbine
  roof, door steps, a strap for the CO2 cylinders on the wall, the generator line-side terminal box and a neutral
  grounding resistor;
- exhaust: expansion joints on the collector, two tempering-air fans (simple-cycle SCRs need the exhaust cooled to
  catalyst temperature) with inlet filters and ducts over the fuel-gas header into the collector;
- SCR: catalyst access doors; the ammonia flow-control skid with its dilution-air blower on the north (back) side,
  at the injection riser, towards the ammonia tank (owner, Oct 21: auxiliaries off the camera face);
- stack: foundation ring, breeching expansion joint, a CEMS shelter at the base with its heated sample line to the
  sampling platform;
- auxiliaries: a low fuel-gas module (filter / separator and valves) tight against the enclosure at the gas drop,
  the off-line water-wash skid on the back side;
- wiring: conduit stub-ups and liquidtight whips into every motor and skid, from the yard duct bank.
Typical, not engineered."""
import fuel
from fuel import box, rod, pipe, find, new_item, on

L = "OPT_MOD"


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def stub(x, y, top, into=None, r=.12):
    """Conduit stub-up out of the slab, with a liquidtight whip into the equipment."""
    rod((x, y, 0), (x, y, top), r, "pvc_grey", seg=8)
    if into:
        rod((x, y, top), into, r * .75, "hero_rail", seg=8)
    return 2 if into else 1


def item(k, x, what, fp, z, info):
    it = new_item(L, f"SC-{k} {what}", fp, z, area="I", register=False, info=info + " Typical, not engineered.")
    on(it)
    return it


def inlet(sc, x):
    """Transition, silencer duct and plenum from the filter house into the turbine enclosure (replaces the plain
    plenum box of the first pass)."""
    fuel.G["parts"][:] = [p for p in fuel.G["parts"] if not (p["item"] == sc["id"] and p["kind"] == "box" and
                                                              p["color"] == "duct" and p["min"][0] == x)]
    on(sc)
    fuel.G["parts"].append(dict(kind="hex", v=[[x, 1198, 11], [x, 1212, 11], [x, 1212, 25.4], [x, 1198, 25.4],
                                               [x + 5, 1200, 17.5], [x + 5, 1210, 17.5], [x + 5, 1210, 24.5],
                                               [x + 5, 1200, 24.5]], color="duct", item=sc["id"], layer=sc["layer"]))
    box(x + 5, x + 19, 1200, 1210, 17.5, 24.5, "duct")                          # silencer section
    box(x + 19, x + 28, 1199, 1211, 17.5, 27.0, "duct")                         # plenum into the enclosure
    box(x + 18.8, x + 28.2, 1198.8, 1211.2, 27.0, 27.4, "steel")
    n = 4
    fuel.D = True
    for xs in (x + 9, x + 13, x + 17):                                          # stiffener bands
        box(xs - .15, xs + .15, 1199.8, 1210.2, 17.5, 24.7, "steel")
        n += 1
    box(x + 5, x + 5.7, 1199.7, 1210.3, 17.3, 24.8, "steel_dark")               # expansion joint
    for (xa, ya) in ((x + 6, 1200), (x + 6, 1210), (x + 18, 1200), (x + 18, 1210)):
        box(xa - .2, xa + .2, ya - .2, ya + .2, 17.0, 17.5, "steel")            # duct saddles on the roof
    decal((x + 12, 1199.9, 21), (0, -1, 0), 8, 1.4, [("INLET SILENCER", .45, 1, "#111111")], bg="#ffffff")
    fuel.D = False
    return n + 6


def enclosures(sc, x):
    on(sc)
    fuel.D = True
    n = 0
    for xr in (x + 4, x + 8, x + 12, x + 16, x + 20):                          # generator enclosure panel joints
        for y, s in ((1193, -1), (1217, 1)):
            box(xr - .08, xr + .08, y, y + s * .12, 1.5, 17, "steel")
            n += 1
    for y, s in ((1193, -1), (1217, 1)):
        box(x + 4.5, x + 11.5, y, y + s * .2, 10, 14.5, "louvre")              # generator vent intake
        box(x + 60, x + 66, y, y + s * .2, 12, 16, "louvre")                   # turbine compartment intake
        n += 2
    box(x + 61, x + 68, 1197, 1203, 22.6, 30.5, "duct")                         # vent-exhaust silencer
    box(x + 60.8, x + 68.2, 1196.8, 1203.2, 30.5, 31.0, "steel")
    box(x + 61, x + 68, 1196.8, 1197, 27.5, 30.2, "louvre")
    n += 3
    for xd in (x + 30, x + 52):                                                 # steps at the enclosure doors
        for (y0, y1, u0, u1) in ((1190.6, 1192, 1191.3, 1192), (1218, 1219.4, 1218, 1218.7)):
            box(xd - .4, xd + 4.4, y0, y1, 0, .75, "grating")
            box(xd - .4, xd + 4.4, u0, u1, .75, 1.5, "grating")
            n += 2
    box(x + 5.4, x + 18.6, 1192.0, 1192.1, 5.2, 5.5, "steel")                    # strap over the CO2 cylinders
    for xb in (x + 5.4, x + 18.6):
        box(xb - .1, xb + .1, 1192.0, 1193.0, 5.2, 5.5, "steel")
    n += 3
    decal((x + 32, 1192.8, 10.6), (0, -1, 0), 4, 1.2, [("DANGER  ·  CO2 FIRE SUPPRESSION", .3, 1, "#ffffff"),
                                                       ("DO NOT ENTER WHEN DISCHARGED", .22, 0, "#ffffff")],
          bg="#b3261e")
    decal((x + 54, 1192.8, 10.6), (0, -1, 0), 4, 1.2, [("HIGH NOISE AREA", .34, 1, "#111111"),
                                                       ("HEARING PROTECTION REQUIRED", .22, 0, "#111111")],
          bg="#f2c21b")
    # generator line-side terminal box over the MV tray (modular_lod3 sc_trays, x + 12) and the NGR beside it
    box(x + 8, x + 16, 1217, 1219.4, 10.4, 16, "panel")
    for dx in (-.6, 0, .6):
        rod((x + 12 + dx, 1218.3, 9.6), (x + 12 + dx, 1218.3, 10.4), .16, "cable_mv", seg=8)
    box(x + 18, x + 23, 1219.5, 1223, 0, 7, "panel")
    box(x + 18.3, x + 22.7, 1219.8, 1222.7, 7, 7.6, "louvre")
    rod((x + 20.5, 1219.5, 5.5), (x + 20.5, 1217.2, 5.5), .2, "copper", seg=8)
    n += 6 + stub(x + 17.4, 1221, .8, (x + 18, 1221, 1.6))
    decal((x + 20.5, 1223.05, 4.5), (0, 1, 0), 4, 1.0, [("NGR  ·  NEUTRAL GROUNDING RESISTOR", .3, 1, "#111111")],
          bg="#ffffff")
    fuel.D = False
    return n


def auxiliaries(k, x):
    it = item(k, x, "auxiliary skids: fuel-gas module, water-wash skid", [x + 26, x + 47, 1186, 1233], [0, 10],
              "Fuel-gas module on the gas drop (coalescing filter / separator, flow meter, shut-off and control "
              "valves) and the off-line compressor water-wash skid (tank, pump, detergent).")
    n = 0
    box(x + 36, x + 46, 1187.6, 1191.9, 0, .4, "concrete")                      # fuel-gas module, low, at the wall
    box(x + 36.3, x + 45.7, 1187.9, 1191.6, .4, 5.8, "machine")
    box(x + 36.1, x + 45.9, 1187.7, 1191.8, 5.8, 6.1, "roof")
    rod((x + 44.8, 1189.8, 6.1), (x + 44.8, 1189.8, 9.5), .18, "fuelgas", seg=8)  # vent
    box(x + 26, x + 36, 1224, 1232, 0, .5, "concrete")                          # water-wash skid
    rod((x + 27.5, 1228, 3.5), (x + 33, 1228, 3.5), 2.6, "tank", seg=16)
    for xs in (x + 28.5, x + 32):
        box(xs - .3, xs + .3, 1226, 1230, .5, 1.6, "steel")
    rod((x + 34.2, 1226, .9), (x + 34.2, 1226, 2.6), .7, "pump", seg=12)
    n += 9
    fuel.D = True
    pipe([(x + 30, 1189.2, 2.5), (x + 36.3, 1189.2, 2.5)], 2.5, .3, "fuelgas")  # from the gas drop
    pipe([(x + 42, 1191.6, 3.6), (x + 42, 1193, 3.6)], 3.6, .26, "fuelgas")     # to the gas manifold
    pipe([(x + 34.2, 1226.7, 2.2), (x + 34.2, 1219.5, 2.2), (x + 34.2, 1217.2, 2.2)], 2.2, .15, "pipe")
    for xd in (x + 37, x + 41):
        box(xd, xd + 3.2, 1187.7, 1187.9, .7, 5.4, "door")
    decal((x + 41, 1187.65, 5.2), (0, -1, 0), 5, .55, [(f"SC-{k} FUEL GAS MODULE", .55, 1, "#111111")], bg="#ffffff")
    n += 5 + stub(x + 46.3, 1189.5, .8, (x + 45.7, 1189.5, 2.4)) + stub(x + 35.4, 1225, .8, (x + 34.6, 1225.6, 1.6))
    fuel.D = False
    return n


def tempering(k, x):
    """Two 100 % tempering-air fans south of the fuel-gas header, ducted over it into the exhaust collector."""
    item(k, x, "tempering-air fans (2 x 100 %)", [x + 70, x + 90, 1164, 1197], [0, 14],
         "Tempering-air fans: ambient air into the exhaust collector to bring the exhaust down to SCR catalyst "
         "temperature; inlet filters, dampers, ducts over the fuel-gas header.")
    n = 0
    box(x + 71, x + 89, 1164, 1180.5, 0, .6, "concrete")
    for xc in (x + 75.5, x + 84.5):
        t = (xc - x - 70) / 20                                                  # where the duct meets the collector
        ys = 1198 - 7 * t
        rod((xc - 1.3, 1172.5, 3.6), (xc + 1.3, 1172.5, 3.6), 2.9, "machine", seg=20)   # fan scroll
        rod((xc + 1.3, 1172.5, 3.6), (xc + 3.4, 1172.5, 3.6), 1.2, "motor", seg=14)
        box(xc - 1.2, xc + 3.4, 1171.5, 1173.5, .6, 2.2, "steel")
        box(xc - 1.8, xc + 1.8, 1165, 1168.8, .6, 7.5, "filter")               # inlet filter / silencer
        box(xc - 1.2, xc + 1.2, 1168.8, 1170.6, 2, 5.4, "duct")
        box(xc - 1.5, xc + 1.5, 1175, 1178, .6, 13, "duct")                    # riser
        box(xc - 1.5, xc + 1.5, 1175, ys + .6, 10, 13, "duct")                 # over the header into the collector
        n += 7
        fuel.D = True
        box(xc - 1.7, xc + 1.7, 1179.4, 1180.2, 9.8, 13.2, "steel")             # isolation damper frame
        box(xc - 1.71, xc + 1.71, 1179.75, 1179.85, 9.79, 13.21, "steel_dark")
        rod((xc + 1.7, 1179.8, 11.5), (xc + 2.6, 1179.8, 11.5), .35, "motor", seg=10)
        for ys_ in (1184, 1188):
            box(xc - .3, xc + .3, ys_ - .3, ys_ + .3, 0, 10, "steel")           # duct supports
        n += 4 + stub(xc + 3.4, 1170.6, .9, (xc + 3.2, 1171.6, 2.4))
        fuel.D = False
    decal((x + 80, 1164.0, 5.5), (0, -1, 0), 7, 1.2, [(f"SC-{k} TEMPERING AIR FANS", .4, 1, "#111111"),
                                                     ("2 x 100 %  ·  ROTATING EQUIPMENT", .26, 0, "#222222")],
          bg="#ffffff")
    return n


def scr(k, x):
    on(find(f"SC-{k} SCR / CO catalyst"))
    fuel.D = True
    n = 0
    for (x0, z0) in ((x + 104, 6), (x + 116, 6), (x + 104, 18), (x + 116, 18)):  # catalyst access doors
        box(x0, x0 + 3, 1190.8, 1191, z0, z0 + 4, "door")
        n += 1
    fuel.D = False
    item(k, x, "ammonia flow-control unit", [x + 95, x + 107, 1221.5, 1227], [0, 7],
         "Ammonia flow-control unit: aqueous ammonia metering, vaporiser and dilution-air blower to the injection "
         "grid riser.")
    box(x + 95.5, x + 106.5, 1221.9, 1226.5, 0, .4, "concrete")
    box(x + 96, x + 101.5, 1222.3, 1226.1, .4, 6, "panel")
    rod((x + 103.5, 1224.2, .4), (x + 103.5, 1224.2, 4.6), 1.5, "steel", seg=14)  # vaporiser
    rod((x + 102.2, 1225.5, 1.2), (x + 105.6, 1225.5, 1.2), .7, "motor", seg=12)   # dilution-air blower
    fuel.D = True
    pipe([(x + 103.5, 1224.2, 4.6), (x + 103.5, 1224.2, 5.5), (x + 100, 1221.1, 5.5)], 5.5, .22, "pipe")
    n += 4 + 1 + stub(x + 95.2, 1224, .8, (x + 96, 1224, 2))
    decal((x + 98.75, 1226.15, 4.6), (0, 1, 0), 4.5, 1.0, [("AMMONIA", .4, 1, "#ffffff"),
                                                            ("AQUEOUS NH3  ·  19 %", .26, 0, "#ffffff")], bg="#26467a")
    fuel.D = False
    return n


def stack(k, x):
    cx, cy = x + 142, 1204.5
    on(find(f"SC-{k} stack (80 ft)"))
    fuel.D = True
    rod((cx, cy, 0), (cx, cy, 1.2), 8.5, "concrete", seg=24)                   # foundation ring
    rod((cx, cy, 1.2), (cx, cy, 1.8), 7.0, "steel", seg=24)                    # base plate
    box(x + 133.5, x + 134.3, 1198.5, 1210.5, 10.5, 27.5, "steel_dark")         # breeching expansion joint
    fuel.D = False
    it = item(k, x, "CEMS shelter", [x + 150, x + 162, 1194, 1205], [0, 52],
              "Continuous emissions monitoring shelter: NOx / CO / O2 / NH3 slip analysers, heated sample line "
              "to the stack sampling ports.")
    box(x + 150.5, x + 161.5, 1194.5, 1204.5, 0, .5, "concrete")
    box(x + 151, x + 161, 1195, 1204, .5, 10.5, "ehouse")
    box(x + 150.8, x + 161.2, 1194.8, 1204.2, 10.5, 11, "roof")
    box(x + 158, x + 160.5, 1194.2, 1195, 3, 6.5, "machine")                    # wall AC unit
    fuel.D = True
    box(x + 152, x + 155, 1194.9, 1195, .5, 7.5, "door")
    rod((x + 151.5, 1199, 10.5), (x + 148.9, 1201.6, 13), .18, "cable_inst", seg=8)    # heated sample line
    rod((x + 148.9, 1201.6, 13), (x + 148.9, 1201.6, 52.5), .18, "cable_inst", seg=8)
    for z in range(16, 52, 6):
        box(x + 148.7, x + 149.4, 1201.2, 1202.0, z, z + .2, "steel")
    decal((x + 156, 1194.85, 9), (0, -1, 0), 7, 1.2, [(f"SC-{k} CEMS", .45, 1, "#111111"),
                                                     ("EMISSIONS MONITORING", .26, 0, "#222222")], bg="#ffffff")
    n = 10 + stub(x + 161.4, 1199, .9, (x + 161, 1199, 2.5))
    fuel.D = False
    on(it)
    return n


def build():
    n = 0
    for k, x in enumerate((1910, 2110), 1):
        sc = find(f"SC-{k}: aeroderivative")
        n += inlet(sc, x) + enclosures(sc, x) + auxiliaries(k, x) + tempering(k, x) + scr(k, x) + stack(k, x)
    return n
