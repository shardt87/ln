"""Final campus items (owner, Oct 29: "what else is missing on a gas power campus?"):

- lightning shield masts over the switchyard, the T-MOD / RICE step-up yards, the BTM transformer yard and the GT
  step-ups (tapered steel poles with a spike, on a plinth);
- a meteorological mast by the admin building (wind, temperature, humidity, pressure: GT performance correction,
  ACC and emissions reporting);
- windsocks at every hazard area (ammonia, hydrogen, LNG, CCS, modular yard, data-centre yard, BESS) so people
  evacuate cross-wind;
- emergency assembly-point signs per area;
- eyewash / safety showers at the ammonia and reagent stores and the water-treatment chemicals.
Positions were picked on a 1 ft occupancy raster with a clear margin (no item, road or pad in the way)."""
import fuel
from fuel import box, rod

L = "SITE"
MASTS = [(449.5, 57.5), (699.5, 41.5), (949.5, 41.5), (1199.5, 41.5), (1449.5, 41.5), (1699.5, 41.5), (1931.5, 53.5),
         (449.5, 241.5), (711.5, 221.5), (949.5, 221.5), (1203.5, 259.5), (1453.5, 259.5), (1705.5, 221.5),
         (1931.5, 249.5),                                                                  # 230 kV switchyard
         (2039.5, 859.5), (2211.5, 859.5), (2039.5, 914.5), (2211.5, 914.5),              # T-MOD-1..3 yard
         (1871.5, 973.5), (1907.5, 1130.5),                                                 # RICE step-up strip
         (2514.5, 699.5), (2695.5, 705.5), (2514.5, 829.5), (2695.5, 829.5),              # BTM transformer yard
         (559.5, 304.5), (1031.5, 304.5), (559.5, 365.5)]                                  # GT step-ups
WINDSOCKS = [(879.5, 1469.5), (2289.5, 1323.5), (1829.5, 1259.5), (2185.5, 1429.5), (2101.5, 1717.5),
             (995.5, 1313.5), (1899.5, 1289.5), (2695.5, 839.5), (1917.5, 599.5)]
EYEWASH = [(879.5, 1499.5), (2285.5, 1333.5), (1825.5, 1277.5), (609.5, 1537.5)]
ASSEMBLY = [(349.5, 449.5), (759.5, 1639.5), (1929.5, 1303.5), (1959.5, 349.5), (1849.5, 1739.5), (559.5, 1289.5),
            (2719.5, 959.5), (379.5, 149.5)]
MET = (351.0, 419.0)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def shield_mast(x, y, h=75.0):
    box(x - 1.5, x + 1.5, y - 1.5, y + 1.5, 0, .8, "concrete")
    rod((x, y, .8), (x, y, h), .55, "steel", r2=.28, seg=10)
    rod((x, y, h), (x, y, h + 6), .1, "steel", r2=.03, seg=6)                     # air terminal
    box(x - .6, x + .6, y - .6, y + .6, 2, 2.4, "steel_dark")                      # ground clamp


def windsock(x, y):
    box(x - 1, x + 1, y - 1, y + 1, 0, .6, "concrete")
    rod((x, y, .6), (x, y, 20), .18, "steel", seg=8)
    rod((x - .9, y, 20.2), (x + .9, y, 20.2), .9, "steel", seg=12)                 # throat ring
    for k in range(5):                                                              # sock: orange / white bands
        xa, xb = x + .9 + 1.6 * k, x + .9 + 1.6 * (k + 1)
        rod((xa, y, 20.2 - .12 * k), (xb, y, 20.2 - .12 * (k + 1)), .9 - .13 * k, "hivis_o" if k % 2 == 0 else
            "white_truck", r2=.9 - .13 * (k + 1), seg=12)


def eyewash(x, y):
    box(x - 1, x + 1, y - 1, y + 1, 0, .3, "concrete")
    rod((x, y, .3), (x, y, 7.6), .14, "camlock_g", seg=8)
    rod((x + .9, y, 7.6), (x + .9, y, 7.3), .55, "camlock_g", seg=12)              # shower head
    rod((x, y, 7.6), (x + .9, y, 7.6), .07, "camlock_g", seg=6)
    rod((x + .8, y, 3.4), (x + .8, y, 3.7), .55, "yellow", seg=12)                 # eyewash bowl
    rod((x, y, 3.5), (x + .5, y, 3.5), .07, "camlock_g", seg=6)
    rod((x - .4, y, 5.2), (x - .4, y, 6.6), .05, "steel", seg=4)                   # pull rod
    decal((x, y - .2, 5.4), (0, -1, 0), 1.1, .8, [("EYEWASH", .3, 1, "#ffffff"), ("SAFETY SHOWER", .22, 0, "#ffffff")],
          bg="#1f7a3a")


def assembly_sign(x, y):
    for s in (-1.5, 1.5):
        rod((x + s, y, 0), (x + s, y, 7.2), .08, "steel", seg=6)
    decal((x, y - .12, 5.6), (0, -1, 0), 3.6, 2.6, [("EMERGENCY", .15, 1, "#ffffff"), ("ASSEMBLY", .15, 1, "#ffffff"),
                                                    ("POINT", .15, 1, "#ffffff"), ("muster here · check in with "
                                                                                 "your area warden", .08, 0, "#e6f2ea")],
          bg="#1f7a3a")


def met_mast(x, y):
    box(x - 2, x + 2, y - 2, y + 2, 0, .6, "concrete")
    for dx, dy in ((-1, -1), (1, -1), (0, 1)):                                    # three-leg lattice, tapering
        rod((x + dx, y + dy, .6), (x + dx * .3, y + dy * .3, 33), .08, "steel", seg=6)
    for z in range(4, 33, 4):
        f = 1 - (z - .6) / 32.4 * .7
        for (a, b) in (((-1, -1), (1, -1)), ((1, -1), (0, 1)), ((0, 1), (-1, -1))):
            rod((x + a[0] * f, y + a[1] * f, z), (x + b[0] * f, y + b[1] * f, z), .04, "steel", seg=4)
    rod((x - 2.5, y, 33), (x + 2.5, y, 33), .06, "steel", seg=6)                   # cross-arm
    rod((x - 2.5, y, 33), (x - 2.5, y, 34), .05, "steel", seg=4)
    for k in range(3):                                                              # cup anemometer
        rod((x - 2.5, y, 34), (x - 2.5 + .5 * (k - 1), y + .5 * ((k + 1) % 2 - .5), 34), .03, "steel", seg=4)
    rod((x + 2.5, y, 33), (x + 2.5, y, 34), .05, "steel", seg=4)
    box(x + 2.3, x + 3.4, y - .05, y + .05, 33.8, 34.4, "steel_dark")             # wind vane
    box(x - .5, x + .5, y - 1.6, y - 1.2, 8, 10, "panel")                          # T / RH / pressure, logger
    box(x - 1.2, x + 1.2, y - 2.2, y - 1.4, 12, 13.8, "glass")                     # solar panel


def build():
    it = fuel.new_item(L, "Lightning shield masts (75 ft, switchyard and outdoor HV yards)",
                       (440, 2700, 35, 1115), (0, 81), area="A", basis="typical", register=False,
                       sheet="typical (site finish)",
                       info="Shield masts over the outdoor HV equipment per IEEE 998 (rolling sphere); each grounded "
                            "to the station grid.")
    for x, y in MASTS:
        shield_mast(x, y)
    fuel.new_item(L, "Meteorological mast (wind, temperature, humidity, pressure)", (MET[0] - 3.4, MET[0] + 3.4,
                  MET[1] - 2.2, MET[1] + 2.2), (0, 34.4), area="F", basis="typical", register=False,
                  sheet="typical (site finish)",
                  info="33 ft met mast: ambient conditions for GT performance correction, ACC control and emissions "
                       "reporting, to the DCS.")
    met_mast(*MET)
    fuel.new_item(L, "Windsocks at the hazard areas (ammonia, hydrogen, LNG, CCS, modular yard, data centre, BESS)",
                  (870, 2710, 590, 1730), (0, 21.2), area="A", basis="typical", register=False,
                  sheet="typical (site finish)", info="Evacuate cross-wind and up-wind of a release.")
    for x, y in WINDSOCKS:
        windsock(x, y)
    fuel.new_item(L, "Eyewash / safety showers (ammonia, reagent, water-treatment chemicals)", (600, 2290, 1270, 1545),
                  (0, 7.6), area="A", basis="typical", register=False, sheet="typical (site finish)")
    for x, y in EYEWASH:
        eyewash(x, y)
    fuel.new_item(L, "Emergency assembly points (one per area)", (340, 2730, 140, 1750), (0, 7.2), area="A",
                  basis="typical", register=False, sheet="typical (site finish)")
    for x, y in ASSEMBLY:
        assembly_sign(x, y)
    return len(MASTS), len(WINDSOCKS), len(EYEWASH), len(ASSEMBLY)
