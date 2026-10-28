"""Three more looks for the modular power park (owner, Oct 27, reference pictures of modular gas plants):

- containerized gas engines, stacked (Rolls-Royce mtu / MWM style in the pictures): the four 40 ft engine containers
  stay on grade (build_model), their cooling containers with the roof radiators and the exhaust silencers stand above
  on a steel deck with grating walkways, handrails and a stair;
- gas engines with heat recovery (AB Energy style): a row of four sound-enclosed engines, each exhaust rising over to
  its own heat exchanger and stack on a pipe rack behind the row, insulated hot-water headers along the rack to the
  dump cooler at the end;
- mid-size industrial gas-turbine packages (Solar Turbines Titan 130 style, ~16 MW): per unit the skid enclosure, the
  barrel-roof self-cleaning inlet filter house raised on legs over the inlet end, the exhaust stack on its own braced
  frame, the lube-oil fin-fan cooler; the fuel-gas conditioning skid between the units.

Company names stay here and in HANDOFF; the signs carry the class only. Typical, not engineered.
"""
import fuel
from fuel import box, rod
from modular_packages import fin_fan, poly, rail, stair

L = "OPT_MODX"


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def by_tag(tag):
    return next(it for it in fuel.G["items"] if it.get("tag") == tag)


# ---------------------------------------------------------------------------------------------------------------
def cge_deck():
    """Steel deck over the four engine containers (x 1955-2017, y 470-510, top EL 9.6): columns in the gaps,
    grating at EL 10.4, a 20 ft cooling container with its radiator module over each engine, the exhaust silencer
    and stack at the north end, handrails round the edge, a stair down to the north gate side."""
    X0, X1, Y0, Y1, Z = 1950.0, 2022.0, 467.6, 512.4, 10.4
    it = fuel.new_item(L, "CGE-1..4 upper deck: stacked cooling containers, radiators, silencers, walkway and stair",
                       (X0, X1, Y0, 527), (0, 27), area="I", register=False, basis="typical", tag="CGE-DECK",
                       info="The containerized engine site stacked two high: the engine containers on grade, the cooling "
                            "containers with their roof radiators and the exhaust silencers on a steel deck above, grating "
                            "walkways with handrails and a stair. Typical, not engineered.")
    fuel.on(it)
    fuel.D = False
    for x in (X0 + .4, 1968.0, 1986.0, 2004.0, X1 - .4):                               # columns in the container gaps
        for y in ((Y0 + .4, Y1 - .4) if x in (X0 + .4, X1 - .4) else (Y0 + .4, 490.0, Y1 - .4)):
            box(x - .4, x + .4, y - .4, y + .4, 0, Z - .8, "steel_dark")
        box(x - .3, x + .3, Y0, Y1, Z - .8, Z - .2, "steel_dark")                      # cross girders
    for y in (Y0 + .4, Y1 - .4):
        box(X0, X1, y - .3, y + .3, Z - .8, Z - .2, "steel_dark")                      # edge girders
    box(X0, X1, Y0, Y1, Z - .2, Z, "grating")                                          # deck grating
    for k in range(4):
        x = 1955 + 18 * k
        box(x, x + 8, 471, 493, Z, Z + 8.6, "white_truck")                             # 20 ft cooling container
        for y in range(473, 492, 4):
            box(x - .08, x, y, y + .2, Z + .3, Z + 8.3, "steel"); box(x + 8, x + 8.08, y, y + .2, Z + .3, Z + 8.3, "steel")
        box(x - .6, x + 8.6, 470.5, 493.5, Z + 8.6, Z + 12.2, "radiator")              # roof radiator module
        for y in (474.5, 482, 489.5):
            rod((x + 4, y, Z + 12.2), (x + 4, y, Z + 12.6), 3.1, "fanhub", seg=16)
        box(x + 1, x + 7, 493, 494.5, Z + 1, Z + 7, "louvre")                          # end louvre
        rod((x + 4, 506, 9.6), (x + 4, 506, Z + 1.2), .7, "alu", seg=12)               # exhaust up through the deck
        rod((x + 4, 498, Z + 2.6), (x + 4, 509, Z + 2.6), 1.5, "alu", seg=16)          # silencer
        box(x + 2.5, x + 5.5, 500, 501, Z, Z + 1.2, "steel"); box(x + 2.5, x + 5.5, 506.5, 507.5, Z, Z + 1.2, "steel")
        rod((x + 4, 498, Z + 2.6), (x + 4, 498, 26.5), .8, "stack", seg=12)             # stack
        rod((x + 4, 498, 26.5), (x + 4, 498, 27.0), .95, "steel", seg=12)
    rail([(X0 + 3.4, Y1), (X1, Y1), (X1, Y0), (X0, Y0), (X0, Y1)], Z)
    stair(X0 + 1.7, Y1, Z, dy=1)
    decal((1986, Y0 - .02, Z + 4.2), (0, -1, 0), 22, 1.6, [("CONTAINERIZED GAS ENGINES  ·  STACKED", .5, True, "#111111"),
                                                      ("engines on grade  ·  cooling above", .32, False, "#333333")],
          bg="#ffffff")
    import maintenance as mt
    mt.person(1990, 495, Z, 1.57)
    return it


# ---------------------------------------------------------------------------------------------------------------
def chp_rack():
    """Pipe rack behind the CHP row (y 684-690, beam top EL 19.4): per unit the exhaust riser from the enclosure roof
    (x c, y 676), over to its vertical exhaust heat exchanger on the rack and the stack above; two insulated hot-water
    headers along the rack to the dump cooler at the east end."""
    C = [2106 + 19 * k for k in range(4)]
    it = fuel.new_item(L, "CHP-HR: exhaust heat-recovery rack (4 exhaust heat exchangers and stacks, hot-water headers, "
                          "dump cooler)", (2098, 2204, 652, 691.6), (0, 34.6), area="I", register=False, basis="typical", tag="CHP-HR",
                       info="The heat-recovery side of the CHP row: exhaust risers to the exhaust-gas heat exchangers and "
                            "stacks on the rack, insulated supply / return hot-water headers to the heat user (off site) and "
                            "the dump cooler for when there is no heat demand. Typical, not engineered.")
    fuel.on(it)
    fuel.D = False
    ZB = 19.4
    bents = [2099.0, 2115.5, 2134.5, 2153.5, 2172.5, 2196.0]
    for x in bents:
        for y in (684.0, 690.0):
            box(x - .4, x + .4, y - .4, y + .4, 0, ZB, "steel")
        box(x - .3, x + .3, 683.6, 690.4, ZB - .8, ZB, "steel")                        # bent beam
        box(x - .3, x + .3, 683.6, 690.4, 9.6, 10.2, "steel")                          # lower tier
        rod((x, 684, .5), (x, 690, ZB - 1), .12, "steel", seg=6)                       # brace
    for y in (684.0, 690.0):
        box(bents[0], bents[-1], y - .3, y + .3, ZB - .8, ZB, "steel")                 # longitudinal beams
    for c in C:
        box(c - 2, c + 2, 684.4, 689.6, ZB - .5, ZB, "steel_dark")                     # heat-exchanger saddle
        rod((c, 676, 12), (c, 676, 22.8), .8, "alu", seg=14)                           # exhaust riser
        rod((c, 676, 22.8), (c, 685.6, 22.8), .8, "alu", seg=14)                        # over to the exchanger
        rod((c, 687, ZB), (c, 687, 27.4), 1.6, "alu", seg=20)                          # exhaust heat exchanger
        rod((c, 687, 27.4), (c, 687, 28.2), 1.2, "alu", seg=20, r2=.8)
        rod((c, 687, 28.2), (c, 687, 34.0), .75, "stack", seg=14)                      # stack
        rod((c, 687, 34.0), (c, 687, 34.6), .9, "steel", seg=14)
        for z in (21.0, 25.6):
            rod((c, 687, z), (c, 687, z + .25), 1.75, "steel", seg=20)                  # flange bands
        poly([(c + 1.6, 687, 21.5), (c + 3.2, 687, 21.5), (c + 3.2, 685, 21.5), (c + 3.2, 685, ZB + .45)], .3, "alu", seg=10)
        poly([(c - 1.6, 687, 26.0), (c - 3.2, 687, 26.0), (c - 3.2, 689, 26.0), (c - 3.2, 689, ZB + .45)], .3, "alu", seg=10)
        rod((c - 3, 678, 8), (c - 3, 684.6, 8), .25, "alu", seg=8)                     # jacket water to the rack
        rod((c - 3, 684.6, 8), (c - 3, 684.6, 9.6), .25, "alu", seg=8)
    for y in (685.0, 689.0):                                                           # supply / return headers
        poly([(2099, y, ZB + .45), (2196, y, ZB + .45), (2196, y, 10.6)], .45, "alu", seg=12)
    poly([(2196, 685, 10.6), (2196, 671, 10.6), (2196, 671, 8.4)], .45, "alu", seg=12)   # down to the dump cooler
    poly([(2196, 689, 10.6), (2199, 689, 10.6), (2199, 671, 10.6), (2199, 671, 8.4)], .45, "alu", seg=12)
    poly([(2196, 689, ZB + .45), (2203, 689, ZB + .45), (2203, 689, 1.5)], .45, "alu", seg=12)   # to the heat user
    fin_fan(2189, 2203, 654, 670)                                                      # dump cooler
    import maintenance as mt
    mt.person(2125, 687, 0, 0.0)
    return it


def chp_labels():
    for k in range(4):
        it = by_tag(f"CHP-{k + 1}")
        fuel.on(it)
        fuel.D = True
        x = 2101 + 19 * k
        decal((x + 5, 652.98, 9.6), (0, -1, 0), 8, 1.2, [(f"CHP-{k + 1}", .6, True, "#111111")], bg="#ffffff")
        rod((x + 9, 678, 1.5), (x + 9, 680.5, 1.5), .2, "fuelgas", seg=8)              # gas train stub
        fuel.D = False


# ---------------------------------------------------------------------------------------------------------------
def mtg_unit(k, yc):
    """MTG-k: skid (x 1972-2030), turbine enclosure, generator end with its air hood and the terminal box on the east
    face; the barrel-roof filter house on four legs over the inlet end (x 1956-1974); the exhaust stack (x 1999.5-2009.5)
    on its braced frame; the lube-oil cooler beside (north of unit 1, south of unit 2)."""
    it = by_tag(f"MTG-{k}")
    fuel.on(it)
    fuel.D = False
    s = 1 if k == 1 else -1                                                            # cooler side
    box(1952, 2036, yc - 10, yc + 10, 0, .3, "concrete")
    box(1972, 2030, yc - 6.5, yc + 6.5, .3, 1.0, "steel_dark")                         # skid
    box(1972.3, 2016, yc - 6.2, yc + 6.2, 1.0, 13, "mosscover")                        # turbine enclosure
    box(1972.3, 2016, yc - 6.2, yc + 6.2, 13, 13.4, "tankroof")
    box(2016, 2029.7, yc - 6.2, yc + 6.2, 1.0, 12, "mosscover")                        # generator end
    box(2016, 2029.7, yc - 6.2, yc + 6.2, 12, 12.4, "tankroof")
    box(2019, 2027, yc - 4, yc + 4, 12.4, 15.4, "louvre")                              # generator air hood
    box(2018.6, 2027.4, yc - 4.4, yc + 4.4, 15.4, 15.8, "tankroof")
    for x in (1980, 1990, 2020):                                                       # enclosure doors both sides
        for y in (yc - 6.35, yc + 6.2):
            box(x, x + 3.2, y, y + .15, 1.4, 8.4, "steel")
    for x in (2010.5, 2013.5):
        box(x, x + 2, yc - 2, yc + 2, 13.4, 15.2, "steel")                             # enclosure vent fans
        rod((x + 1, yc, 15.2), (x + 1, yc, 15.6), .9, "fanhub", seg=12)
    box(2029.7, 2032, yc - 2, yc + 2, 2, 8, "motor")                                   # generator terminal box
    for j in range(6):
        y = yc - 1.5 + j * .6
        poly([(2031, y, 2.0), (2031, y, .6), (2032.2, y, .3)], .18, "cable_mv", seg=8)
    # inlet: duct into the enclosure roof, filter house on legs, barrel roof, filter faces
    box(1970, 1977, yc - 4, yc + 4, 13.4, 16.6, "duct")
    for x in (1956.5, 1973.5):
        for y in (yc - 8.3, yc + 8.3):
            box(x - .35, x + .35, y - .35, y + .35, .3, 16, "steel")
        rod((x, yc - 8.3, .8), (x, yc + 8.3, 15.4), .14, "steel", seg=6)              # end-frame braces
        rod((x, yc + 8.3, .8), (x, yc - 8.3, 15.4), .14, "steel", seg=6)
    for y in (yc - 8.3, yc + 8.3):
        box(1956.5, 1973.5, y - .25, y + .25, 15.4, 16, "steel")
    box(1956, 1974, yc - 9, yc + 9, 16, 26, "mosscover")
    rod((1956.15, yc, 26), (1973.85, yc, 26), 8.9, "tankroof", seg=28)                 # barrel roof (inset: no shared faces)
    for y, d in ((yc - 9, -1), (yc + 9, 1)):
        box(1957, 1973, min(y, y + d * .15), max(y, y + d * .15), 17, 25, "filter")   # filter faces
        for z in (19.6, 22.4):
            box(1957, 1973, min(y, y + d * .9), max(y, y + d * .9), z, z + .25, "steel")
    for z in range(2, 16, 1):                                                          # cage ladder on a leg
        rod((1955.6, yc - 8.0, z), (1955.6, yc - 8.6, z), .05, "sp_yellow", seg=4)
    rod((1955.6, yc - 8.0, 1), (1955.6, yc - 8.0, 17), .06, "sp_yellow", seg=4)
    rod((1955.6, yc - 8.6, 1), (1955.6, yc - 8.6, 17), .06, "sp_yellow", seg=4)
    # exhaust: transition, stack on its braced frame
    box(2000.5, 2008.5, yc - 4, yc + 4, 13.4, 18, "duct")
    box(1999.5, 2009.5, yc - 5, yc + 5, 18, 50, "mosscover")
    for z in (24, 32, 40, 48):
        box(1999.3, 2009.7, yc - 5.2, yc + 5.2, z, z + .4, "steel")                    # stiffener bands
    box(1999.3, 2009.7, yc - 5.2, yc + 5.2, 50, 50.6, "steel")
    for x in (1998.5, 2010.5):
        for y in (yc - 7.3, yc + 7.3):
            box(x - .35, x + .35, y - .35, y + .35, .3, 44, "steel")
    for z in (14.0, 26.0, 38.0, 44.0):
        for y in (yc - 7.3, yc + 7.3):
            box(1998.5, 2010.5, y - .2, y + .2, z - .4, z, "steel")
        for x in (1998.5, 2010.5):
            box(x - .2, x + .2, yc - 7.3, yc + 7.3, z - .4, z, "steel")
    for y in (yc - 7.3, yc + 7.3):
        for z0, z1 in ((14, 26), (26, 38)):
            rod((1998.5, y, z0), (2010.5, y, z1), .13, "steel", seg=6)
    box(1998.5, 2010.5, yc - 7.3, yc + 7.3, 43.6, 44, "grating")                       # top platform
    rail([(1998.5, yc - 7.3), (2010.5, yc - 7.3), (2010.5, yc + 7.3), (1998.5, yc + 7.3), (1998.5, yc - 7.3)], 44)
    # lube-oil cooler and its pipes
    y0, y1 = (yc + 11, yc + 18) if s == 1 else (yc - 18, yc - 11)
    fin_fan(2006, 2020, y0, y1)
    for x in (2010, 2016):
        poly([(x, yc + s * 6.5, 3), (x, yc + s * 9, 3), (x, yc + s * 9, 7.2), (x, (y0 + y1) / 2, 7.2)], .3, "pipe", seg=8)
    fuel.D = True
    decal((1994, yc - 6.36, 10.2), (0, -1, 0), 16, 1.4, [(f"MTG-{k}  ·  MID-SIZE GAS TURBINE", .5, True, "#111111"),
                                                        ("~16 MW  ·  13.8 kV", .32, False, "#333333")], bg="#ffffff")
    fuel.D = False
    return it


def mtg_fg():
    """MTG-FG skid (x 1948-1968, y 711-721): vertical scrubber, horizontal filter-separator, gas heater, block valves."""
    it = by_tag("MTG-FG")
    fuel.strip(it)
    fuel.D = False
    box(1948, 1968, 711, 721, 0, .6, "steel_dark")
    rod((1951.5, 716, .6), (1951.5, 716, 11), 1.6, "tank", seg=20)                     # scrubber
    rod((1951.5, 716, 11), (1951.5, 716, 12), 1.6, "tank", seg=20, r2=.6)
    rod((1955, 716, 3.2), (1962, 716, 3.2), 1.3, "tank", seg=20)                       # filter-separator
    for x in (1956.5, 1960.5):
        box(x - .3, x + .3, 715, 717, .6, 1.9, "steel")
    box(1963.5, 1967.5, 713, 719, .6, 6.5, "machine")                                  # heater
    poly([(1948, 716, 2.5), (1951.5, 716, 2.5)], .35, "fuelgas", seg=10)
    poly([(1953.1, 716, 8), (1955, 716, 8), (1955, 716, 4.5)], .35, "fuelgas", seg=10)
    poly([(1962, 716, 3.2), (1963.5, 716, 3.2)], .35, "fuelgas", seg=10)
    poly([(1967.5, 716, 2.5), (1968, 716, 2.5)], .35, "fuelgas", seg=10)
    for x, c in ((1949.4, "pvc_blue"), (1962.8, "pvc_blue"), (1967.8, "red")):
        box(x - .4, x + .4, 715.4, 716.6, 3.1, 4.3, c)                                 # valve actuators
    fuel.D = True
    decal((1958, 710.9, 1.0), (0, -1, 0), 14, .7, [("FUEL GAS  ·  CLASS I DIV 2", .45, True, "#ffffff")], bg="#b8322a")
    fuel.D = False
    return it


def tmod3_gantry():
    """The T-MOD 230 kV take-off gantry extended east over T-MOD-3: a new end column (x 2204), the beam continued from
    the old end column (x 2134), a strain point over T-MOD-3's bushings (x 2179), jumpers down to the three bushings,
    the bus back to the gantry, surge arresters on stands in front of the tank."""
    it = fuel.new_item("OPT_MOD", "T-MOD-3 230 kV gantry extension with arresters", (2135, 2206, 846, 857.5), (0, 46),
                       area="I", register=False, basis="typical",
                       info="The T-MOD 230 kV take-off gantry extended east over T-MOD-3 (electrical review, Oct 28): end "
                            "column, beam, strain strings, jumpers to the bushings, surge arresters. Typical, not engineered.")
    fuel.on(it)
    fuel.D = False
    rod((2204, 851, 0), (2204, 851, 46), .8, "steel", r2=.55, seg=8)
    box(2202.5, 2205.5, 849.5, 852.5, 0, .5, "concrete")
    box(2135, 2204, 850.2, 851.8, 43, 45, "steel")
    for k in range(3):
        x = 2170 + 9 * k
        box(x - .4, x + .4, 855.6, 856.4, 0, 18, "steel")                              # arrester stands
        rod((x, 856, 18), (x, 856, 26), .45, "insulator", seg=8)
    fuel.D = True
    rod((2179, 851, 43), (2179, 851, 40.3), .3, "insulator", seg=6)
    for yb in (866.5, 874.56, 882.6):                                                  # jumpers to the bushings, sagging
        a, b = (2179, yb, 37), (2179, 851, 40.3)
        m = (2179, (a[1] + b[1]) / 2, 37.5)
        pts = [tuple((1 - t) ** 2 * a[j] + 2 * (1 - t) * t * m[j] + t * t * b[j] for j in range(3)) for t in [i / 8 for i in range(9)]]
        for p_, q_ in zip(pts, pts[1:]):
            rod(p_, q_, .14, "conductor", seg=6)
    rod((2179, 851, 40.3), (2125, 851, 40.3), .14, "conductor", seg=6)               # bus to the existing gantry
    for k in range(3):
        x = 2170 + 9 * k
        rod((x, 856, 26), (2179, 851, 40.3), .08, "conductor", seg=6)                  # arrester leads
    fuel.D = False
    return it


def build():
    n0 = len(fuel.G["parts"])
    tmod3_gantry()
    cge_deck()
    chp_rack()
    chp_labels()
    for k, yc in ((1, 690), (2, 742)):
        mtg_unit(k, yc)
    mtg_fg()
    import maintenance as mt
    fuel.on(by_tag("MTG-1"))
    fuel.D = True
    mt.person(2042, 735, 0, 3.14)
    fuel.D = False
    return len(fuel.G["parts"]) - n0
