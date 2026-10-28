"""Modular power yard at LOD 3, the gas-yard standard: what the RICE hall and the simple-cycle units need around them
to read as a working yard rather than equipment on bare ground.

- surfaces: crushed-stone yard, concrete drives between the equipment rows, aprons at the doors;
- visible cable as installed in a yard like this:
  - the RICE exhaust-train services rack along the south wall (rigid conduit bank + exposed ARMOR-X MC on strut)
    with drops into each urea-dosing cabinet and the CEMS shelter; heated sample lines down each stack;
  - the radiator-fan feeders along the north wall, a fused disconnect per radiator bank, MC on strut up the
    radiator gaps to each fan motor;
  - the 13.8 kV generator cables from the engine hall to the PCM switchgear on a ladder-tray bridge
    (MV-105, printed legends), and a cable-dressing crew on a scissor lift under it;
  - generator-to-PCM ladder trays on both simple-cycle units;
- equipment detail: SCR housings (stiffeners, catalyst doors, nameplates), silencer bands, engine numbers on the
  hall, simple-cycle filter-house weather hoods, enclosure vent fans and nameplates, PCM signage;
- furniture: flood-light poles, extinguishers, a spares laydown (ISO containers, cable reels), people, pickups,
  a forklift.
Everything is placed only where clear of existing parts (gas_lod3.Space). All typical, not engineered.
"""
import fuel
from fuel import box, rod, on, find

import gas_lod3 as G3
from gas_lod3 import Space, tray, light_pole, extinguisher, pickup, person, decal

L = "OPT_MOD"
ENG = [1581 + 28 * k for k in range(8)]
MV_TXT = "MV-105  15 kV  1/C 500 KCMIL CU  EPR  133% INS  TAPE SHIELD  PVC  UL 1072"


def new(name, fp, z, info=""):
    it = fuel.new_item(L, name, fp, z, area="I", sheet="typical (modular detail)", register=False, info=info)
    on(it)
    return it


# ---------------------------------------------------------------------------------------------------------
def surfaces():
    new("Modular yard: crushed-stone surface, concrete drives and aprons", (1556, 2392, 860, 1336), (0, .2),
        "Compacted crushed stone over the yard; concrete drives between the equipment rows for maintenance access.")
    # crushed stone, kept off the open cable-pull manholes of the collector (1695-1940 x 910-980)
    for (x0, x1, y0, y1) in ((1556, 2392, 860, 910), (1556, 2392, 980, 1336), (1556, 1690, 910, 980),
                             (1945, 2392, 910, 980)):
        box(x0, x1, y0, y1, 0, .08, "gravel_yard")
    for (x0, x1, y0, y1) in ((1556, 1900, 981, 995),          # south drive along the exhaust trains
                             (1864, 1880, 995, 1336),         # N-S drive between the PCM and the aero units
                             (1556, 1835, 1221, 1232),        # north drive between radiators and the lube building
                             (1835, 1864, 1222.6, 1232),      # (narrowed past the PCM's end-wall HVAC unit)
                             (1880, 2392, 1104, 1124)):       # drive between the aero units and the fuel cells
        # (the drive between the SC units and their PCMs, y 1226-1240, is gone (road audit, Oct 28): generator leads and
        # lube-oil lines cross that strip; the SC units are served from the y 1104 drive, the PCMs from the reserved pad)
        box(x0, x1, y0, y1, .08, .16, "road")
    for (x0, x1, y0, y1) in ((1824, 1836, 1128, 1136), (1926, 1940, 870, 876)):
        box(x0, x1, y0, y1, .08, .2, "concrete")                # door aprons


# ---------------------------------------------------------------------------------------------------------
def bend_drop(S, x, y0, y1, z, zb, mc=True, into=None):
    """Conduit (and an MC cable beside it) leaving a rack at (x, y0, z), across to y1 and down to zb; `into`: a
    last horizontal stub at zb to a wall face at that y."""
    lo, hi = min(y0, y1), max(y0, y1)
    if not S.free(x - .45, x + .45, lo, hi, zb + .05, z - .6, m=0):
        return False
    for dx, c, r in ((-.2, "steel", .1),) + (((.2, "cable_mc", .13),) if mc else ()):
        rod((x + dx, y0, z + .1), (x + dx, y1, z + .1), r, c, seg=8)
        rod((x + dx, y1, z + .1), (x + dx, y1, zb), r, c, seg=8)
        rod((x + dx, y1, z + .1 - r * 1.2), (x + dx, y1, z + .1 + r * 1.2), r * 1.25, c, seg=8)     # elbow / LB
        if into is not None:
            rod((x + dx, y1, zb), (x + dx, into, zb), r, c, seg=8)
    S.add([x - .45, lo - .2, zb, x + .45, hi + .2, z + .3])
    return True


def services_racks(S):
    """South-wall exhaust-train services and north-wall radiator-fan feeders."""
    it = new("RICE yard: conduit racks and exposed ARMOR-X MC on strut (SCR dosing, CEMS, radiator fans)",
             (1570, 1850, 1000, 1216), (0, 42),
             "480 V power to the urea-dosing cabinets and radiator fans as ARMOR-X MC on strut beside a rigid "
             "conduit bank (control, instrument, fire alarm); fused disconnects per radiator bank; heated CEMS "
             "sample lines from each stack to the CEMS shelter.")
    fuel.D = True
    # fan disconnect stands first, so the racks' posts keep clear of them
    disc = []
    for x in ENG:
        xd, yd = x + 24, 1137.2
        if S.free(xd - 1, xd + 1, yd - .6, yd + .6, .7, 7, m=.1):
            S.add([xd - 1, yd - .6, 0, xd + 1, yd + .6, 5.6])
            box(xd - 1, xd + 1, yd - .6, yd + .6, 0, .35, "concrete")
            for dx in (-.75, .75):
                rod((xd + dx, yd + .3, .35), (xd + dx, yd + .3, 6.4), .1, "steel", seg=6)
            box(xd - .9, xd + .9, yd + .2, yd + .4, 5.9, 6.1, "steel")
            box(xd - .65, xd + .65, yd - .45, yd + .2, 3.0, 5.6, "panel")                   # fused disconnect
            box(xd + .65, xd + .8, yd - .2, yd - .05, 4.0, 4.6, "red")                       # operating handle
            disc.append((xd, yd))
    zs = tray(S, [(1579, 1033), (1814, 1033), (1814, 1066), (1810.2, 1066)], 10.0, w=1.0, name="RICE south",
              tag="MY-C1")
    zn = tray(S, [(1579, 1135), (1806, 1135), (1806, 1130.2)], 10.0, w=1.0, name="RICE north", tag="MY-C2")
    n = 0
    if zs:
        for x in ENG:                                                       # into the urea-dosing cabinet tops
            n += bend_drop(S, x + 16.2, 1033, 1031.0, zs, 7.0)
        sp = tray(S, [(1814, 1032.2), (1814, 1029), (1838, 1029), (1838, 1017.2)], zs, w=.75,
                  cables=(("cable_mc", .13), ("cable_inst", .1), ("cable_inst", .1)), name="CEMS spur")
        if sp:
            box(1813.6, 1814.4, 1032.2, 1032.5, sp - .1, sp, "steel")                       # tee off the trunk
            n += bend_drop(S, 1838, 1017.2, 1015.4, sp, 7.5, into=1014.75)
        for x in ENG:                                                       # heated sample line down each stack
            xt = x + 9.5 - 3.45
            rod((xt, 1037, 40.5), (xt, 1037, zs + .5), .12, "cable_inst", seg=8)
            rod((xt, 1037, zs + .5), (xt, 1033.4, zs + .5), .12, "cable_inst", seg=8)
            rod((xt + .35, 1037, 40.5), (xt - .1, 1037, 40.5), .12, "cable_inst", seg=8)    # probe flange
            for zb in (14, 26, 34):
                box(xt, x + 9.5 - 3.02, 1036.9, 1037.1, zb, zb + .15, "steel")
            box(xt - .35, xt + .35, 1036.6, 1037.4, 39.2, 40.2, "machine")                  # probe junction box
    if zn:
        for (xd, yd) in disc:
            if bend_drop(S, xd, 1135.5, yd + .3 - .55, zn, 5.6):
                n += 1
            # MC up the radiator gap to each fan motor
            r = tray(S, [(xd, 1139.5), (xd, 1213)], 8.4, w=.6, cables=(("cable_mc", .12), ("cable_tc", .09)),
                     name="fan feeders")
            if r:
                rod((xd + .5, yd - .1, 5.6), (xd + .5, yd - .1, r + .15), .12, "cable_mc", seg=8)
                rod((xd + .5, yd - .1, r + .15), (xd + .5, 1139.5, r + .15), .12, "cable_mc", seg=8)
                for k in range(5):
                    yc = 1146 + 16 * k
                    xr = xd - 2.65                                                            # radiator side x + 21
                    rod((xd - .2, yc, r + .15), (xr, yc, r + .15), .1, "cable_mc", seg=6)
                    rod((xr, yc, r + .15), (xr, yc, 6.6), .1, "cable_mc", seg=6)
                    box(xr - .3, xr + .3, yc - .4, yc + .4, 5.0, 6.6, "machine")             # motor JB on the frame
    fuel.D = False
    print("modular_lod3: racks", zs, zn, "drops", n)


# ---------------------------------------------------------------------------------------------------------
def mv_bridge(S):
    """13.8 kV generator cables from the engine hall to the PCM on a ladder-tray bridge, crew dressing them."""
    it = new("RICE generator cables: 13.8 kV MV-105 on the ladder-tray bridge to the PCM (cable dressing crew)",
             (1808, 1860, 1070, 1142), (0, 18),
             "Eight 13.8 kV generator circuits (1/C 500 kcmil MV-105, triplexed) leave the engine hall's east wall "
             "on a 36 in ladder tray to the PCM switchgear; two electricians on a scissor lift dress and tie the "
             "cables; spare reel on the drive. Cable supplier: Southwire (as requested).")
    fuel.D = True
    cab = tuple(("cable_mv", .21) for _ in range(9)) + (("cable_fo", .09),)
    z = tray(S, [(1810.2, 1112), (1845, 1112), (1845, 1139.9)], 12.0, w=3.0, cables=cab, name="MV bridge",
             style="tray", tag="MY-T1")
    if z:
        for (a0, a1, b0, b1) in ((1810.02, 1810.5, 1110.2, 1113.8), (1843.2, 1846.8, 1139.6, 1140.25)):
            box(a0, a1, b0, b1, z - .6, z + .9, "steel")                                        # wall sleeves
        # scissor lift under the bridge, two electricians tying the triplex
        from cable_moments import scissor_lift
        if S.free(1824, 1830, 1103.5, 1109.5, .7, z - .7, m=.2):
            scissor_lift(1824.5, 1829.5, 1104, 1109, 0, z - 4.6)
            S.add([1824, 1103.5, 0, 1830, 1109.5, z - .7])
            person(1826, 1108.2, z - 4.6, 1.57)
            person(1828.4, 1108.2, z - 4.6, 1.57, vest="hivis_o")
        import showcase
        if S.free(1834, 1844, 1078, 1092, .7, 9, m=.3):
            showcase.reel(1839, 1085, 8.0, 5.0, "x", "cable_mv", "MV-105 15 kV 1/C 500 KCMIL", length_ft=2500)
            S.add([1834, 1078, 0, 1844, 1092, 9])
            person(1837, 1091.5, 0, -1.2)
        from cable_moments import legends
        legends({it["id"]}, {"cable_mv": MV_TXT}, (1808, 1860, 1100, 1142, z - 1, z + 1))
    fuel.D = False
    return z


def sc_trays(S):
    from sc2_mirror import mx
    for k, x in enumerate((1910, 2110), 1):
        xt = x + 12 if k == 1 else mx(x + 12)              # SC-2 stands mirrored (sc2_mirror.py)
        it = new(f"SC-{k}: generator cables to the PCM (13.8 kV MV-105 on ladder tray)",
                 (xt - 3, xt + 3, 1217, 1246), (0, 14))
        fuel.D = True
        # 5 sets x 3 x 750 kcmil MV-105 for ~2,100 A, as the cable schedule sizes it (cable audit, Oct 21: the tray
        # showed 6), one layer on a 36 in ladder tray, the CT / VT control cable beside them
        z = tray(S, [(xt, 1217.6), (xt, 1244.9)], 9.0, w=3.0,
                 cables=tuple(("cable_mv", .08) for _ in range(15)) + (("cable_tc", .06),), name=f"SC-{k} gen",
                 style="tray", tag=f"SC{k}-T1")
        if z:
            from cable_moments import legends
            legends({it["id"]}, {"cable_mv": MV_TXT}, (xt - 3, xt + 3, 1217, 1246, z - 1, z + 1))
        fuel.D = False


# ---------------------------------------------------------------------------------------------------------
def equipment():
    for k, x in enumerate(ENG):
        xc = x + 9.5
        on(find(f"RICE {k + 1} SCR"))
        fuel.D = True
        for xf, s in ((x + 1.5, -1), (x + 18.5, 1)):                     # SCR housing: stiffeners, catalyst doors
            for y in range(1005, 1027, 3):
                box(xf, xf + s * .2, y - .12, y + .12, 12, 22, "steel")
            box(xf, xf + s * .2, 1002.5, 1027.5, 16.9, 17.1, "steel")
        for y0 in (1011.3, 1020.3):
            box(x + 1.25, x + 1.5, y0, y0 + 2.4, 13.2, 16.5, "door")
        decal((x + 1.2, 1015, 20.2), (-1, 0, 0), 5.5, 1.3,
              [(f"SCR-{k + 1}", .45, True, None), ("SCR + OXIDATION CATALYST", .25, False, None)], bg="#ffffff")
        for y in range(1006, 1026, 4):                                   # silencer bands
            rod((xc, y - .08, 26.4), (xc, y + .08, 26.4), 4.28, "steel", seg=24)
        fuel.D = False
        on(find("RICE engine hall"))
        fuel.D = True
        decal((xc, 1039.85, 21.5), (0, -1, 0), 5.2, 2.2,
              [(f"ENGINE {k + 1}", .42, True, None), (f"G-{k + 1}  ·  13.8 kV  ·  18 MW", .24, False, None)],
              bg="#ffffff")
        fuel.D = False
    on(find("RICE engine hall"))
    fuel.D = True
    # (a white RICE ENGINE HALL panel stood here above the band; owner, Oct 22: one name sign per end, the black one over
    # the door in campus_brand.py stays)
    fuel.D = False
    on(find("PCM: power control module"))
    fuel.D = True
    decal((1848, 1140.0, 10.5), (0, -1, 0), 14, 2.2,
          [("PCM-1", .42, True, None), ("13.8 kV GENERATOR SWITCHGEAR  ·  ARC FLASH HAZARD", .22, False, None)],
          bg="#ffffff")
    fuel.D = False

    import sc2_mirror
    for k, x in enumerate((1910, 2110), 1):
        on(find(f"SC-{k}: aeroderivative"))
        mark = sc2_mirror.since()
        fuel.D = True
        for zz in [9.0 + 1.6 * i for i in range(9)]:                     # filter-house weather hoods
            box(x - 20.9, x - 20, 1196.4, 1213.6, zz, zz + .18, "steel")
            box(x - 20.9, x - 20.7, 1196.4, 1213.6, zz - .7, zz, "steel")
        on(find(f"SC-{k} package enclosure"))             # roof fans and panel joints go with the walls (cutaways)
        for xs in (x + 30, x + 42, x + 56):                               # enclosure vent fans
            rod((xs, 1205, 22.6), (xs, 1205, 24.0), 1.5, "fan", seg=18)
            rod((xs, 1205, 24.0), (xs, 1205, 24.3), 1.7, "steel", seg=18)
        rod((x + 18, 1196, 17), (x + 18, 1196, 18.4), 1.3, "fan", seg=16)   # clear of the inlet duct
        for xr in (x + 27, x + 37, x + 42, x + 47, x + 62, x + 67):        # turbine enclosure panel joints
            for y, s in ((1193, -1), (1217, 1)):
                box(xr - .08, xr + .08, y, y + s * .12, 1.5, 22, "steel")
        # (the white SC-k nameplate stood here; the unit is lettered in campus_brand.py since Oct 21)
        fuel.D = False
        if k == 2:
            sc2_mirror.mirror_since(mark)                  # drawn coordinates -> the mirrored unit


# ---------------------------------------------------------------------------------------------------------
def forklift(S, x, y):
    p = S.place(x, y, 2.2, 4.5, 9)
    if not p:
        return
    x, y = p
    box(x - 2, x + 2, y - 3, y + 2.5, .9, 3.6, "sp_yellow")                  # body / counterweight
    box(x - 1.9, x + 1.9, y - 1.5, y + 1.6, 3.6, 7.6, "steel")               # overhead guard (posts as a frame)
    box(x - 1.7, x + 1.7, y - 1.3, y + 1.4, 3.7, 7.5, "glass")
    for xm in (x - 1.2, x + 1.2):
        box(xm - .2, xm + .2, y + 2.6, y + 2.9, .3, 8.5, "steel")             # mast
        box(xm - .15, xm + .15, y + 2.9, y + 6.4, .3, .5, "steel")            # forks
    for (u, v) in ((-2.1, -2), (1.9, -2), (-2.1, 1.6), (1.9, 1.6)):
        rod((x + u, y + v, .9), (x + u + .2, y + v, .9), .9, "tyre", seg=12)


def laydown(S):
    new("Modular yard: engine spares and cable-reel laydown (ISO containers, reels, pallets)",
        (2295, 2390, 990, 1095), (0, 10),
        "Engine-plant spares kept on site: two ISO containers (cylinder heads, turbocharger cartridges, "
        "filters), cable reels for the yard's 480 V and control circuits on timber, pallets.")
    import showcase
    for (x0, y0) in ((2305, 1010), (2305, 1022)):                            # 20 ft ISO containers
        if S.free(x0, x0 + 20, y0, y0 + 8, .7, 9, m=.3):
            box(x0, x0 + 20, y0, y0 + 8, .3, 8.8, "ehouse")
            for xr in range(int(x0) + 1, int(x0) + 20, 2):
                box(xr, xr + .15, y0 - .08, y0, .5, 8.5, "steel")
            box(x0 + 19.9, x0 + 20, y0 + .3, y0 + 7.7, .4, 8.6, "door")
            S.add([x0, y0, 0, x0 + 20, y0 + 8, 9])
    k = 0
    for (x, y, D, W, c, prod) in ((2340, 1015, 6.0, 4.0, "cable_mc", "ARMOR-X MC 600 V 3/C 4/0"),
                                  (2350, 1015, 6.0, 4.0, "cable_tc", "TYPE TC-ER 600 V 12/C 14"),
                                  (2360, 1015, 5.0, 3.5, "cable_inst", "PLTC-ER 16 AWG 4 TSP"),
                                  (2345, 1035, 7.0, 4.5, "cable_mv", "MV-105 15 kV 1/C 500")):
        if S.free(x - W / 2 - .5, x + W / 2 + .5, y - D / 2 - .5, y + D / 2 + .5, .7, D + .5, m=.2):
            showcase.reel(x, y, D, W, "x", c, prod, length_ft=2500 if D > 6 else 1000)
            S.add([x - W / 2 - .5, y - D / 2 - .5, 0, x + W / 2 + .5, y + D / 2 + .5, D + .5])
            k += 1
    for (x, y) in ((2370, 1050), (2376, 1050), (2370, 1056)):                   # pallets of crated parts
        if S.free(x - 2, x + 2, y - 2, y + 2, .7, 4, m=.2):
            box(x - 2, x + 2, y - 2, y + 2, 0, .5, "timber")
            box(x - 1.8, x + 1.8, y - 1.8, y + 1.8, .5, 3.4, "wood")
            S.add([x - 2, y - 2, 0, x + 2, y + 2, 4])
    forklift(S, 2335, 1060)
    print("modular_lod3: laydown reels", k)


def furniture(S):
    new("Modular yard: flood-light poles, extinguishers (typical)", (1556, 2392, 860, 1336), (0, 31))
    fuel.D = True
    for (x, y) in ((1605, 998), (1689, 998), (1773, 998), (1862, 1000), (1862, 1100), (1862, 1200),
                   (1640, 1218), (1740, 1218), (1885, 1243), (2000, 1243), (2100, 1243), (2200, 1243),
                   (1990, 1127), (2100, 1127), (2210, 1127), (2320, 1127), (1950, 1000), (2160, 960),
                   (2330, 940), (1600, 890)):
        light_pole(S, x, y, h=30)
    for (x, y) in ((1812, 1035), (1603, 1137), (1717, 1137), (1905, 1225), (2105, 1225), (1862, 1135),
                   (1810, 1236)):
        extinguisher(S, x, y)
    fuel.D = False
    new("Modular yard: operators and vehicles", (1556, 2392, 860, 1336), (0, 8))
    pickup(S, 1640, 988)
    pickup(S, 1760, 1230)                          # on the north drive (was parked at SC-1's air inlet)
    pickup(S, 2000, 1114)                          # on the drive south of the SC units
    for (x, y, a, v) in ((1710.5, 1027.6, 1.57, "hivis"), (1706.4, 1027.6, 1.2, "hivis_o"), (1830, 1133, 1.57, "hivis"),
                         (1960, 1226, 0, "hivis"), (1725, 1218, 3.14, "hivis_o")):
        p = S.place(x, y, .8, .8, 6)
        if p:
            person(p[0], p[1], .16, a, vest=v)


def build():
    S = Space()
    surfaces()
    equipment()
    S = Space()                                    # re-index with the dressing
    services_racks(S)
    z = mv_bridge(S)
    sc_trays(S)
    laydown(S)
    furniture(S)
    return 1 if z else 0
