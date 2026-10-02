"""Water and BOP utilities at LOD 3 (detail cycle 4).

Routes (drawn by pipes.py, on sleepers, under roads in sleeves):
- raw and demineralised water: tank outlets to a header along y 1545 and into the water-treatment
  building; fire / service water from its tank round the tank farm to the fire pump house;
- auxiliary steam: from the auxiliary boiler east and north to the main pipe rack (insulated).
Dressing:
- fire pump house: diesel-driver exhaust stack and silencer, louvres, the test header with hose
  valves on the outside wall, a jockey-pump controller;
- ammonia storage: bund walls, truck unloading connection and hose station, vapour scrubber,
  safety shower / eyewash, wind sock;
- auxiliary boiler: burner front and windbox, FD fan with inlet silencer, economizer on the
  stack breeching, feedwater pump skid, blowdown tank;
- air compressors: air receivers and a desiccant dryer beside the building;
- oil-water separator: inlet pipe, access hatches, oil skimmer.
All typical, not engineered.
"""
import fuel
from fuel import box, rod, find, on, pipe


def dress(flag):
    fuel.D = flag


def routes(add_route):
    sheet = "typical (utilities detail)"
    add_route("water", [(465, 1570), (465, 1545), (600, 1545), (600, 1570)], sheet=sheet)   # raw + demin header
    add_route("water", [(520, 1545), (520, 1530)], sheet=sheet)                              # into water treatment
    add_route("water", [(530, 1616), (530, 1626), (720, 1626), (720, 1605)], sheet=sheet)   # fire / service water
    add_route("aux_steam", [(995, 1495), (1040, 1495), (1040, 852)], sheet=sheet)


def build():
    # fire pump house
    it = find("Fire pump house")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    rod((x1 - 5, y1 - 5, 16), (x1 - 5, y1 - 5, 26), .8, "stack", seg=12)                  # diesel exhaust stack
    rod((x1 - 5, y1 - 5, 17), (x1 - 5, y1 - 5, 21), 1.5, "steel", seg=14)                 # silencer
    for y in (y0 + 6, y0 + 14, y0 + 22):
        box(x1, x1 + .15, y - 2, y + 2, 8, 12, "louvre")
    rod((x0 - 1, y0 + 8, 4), (x0 - 1, y0 + 22, 4), .5, "red", seg=10)                      # test header
    for y in (y0 + 10, y0 + 15, y0 + 20):
        rod((x0 - 1, y, 4), (x0 - 2.4, y, 4), .25, "red", seg=8)
        rod((x0 - 2.4, y, 4), (x0 - 2.8, y, 4), .35, "amber", seg=8)                      # hose valve caps
    box(x0 + 2, x0 + 4, y0 - .4, y0, 2, 6, "panel")                                        # jockey-pump controller
    dress(False)

    # ammonia storage
    it = find("Ammonia storage")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + .8), (x0, x1, y1 - .8, y1), (x0, x0 + .8, y0, y1),
                             (x1 - .8, x1, y0, y1)):
        box(a0, a1, b0, b1, 4, 6.5, "concrete")                                             # bund walls
    box(x0 + 2, x0 + 6, y0 - .5, y0 + 1, 0, 5, "panel")                                     # unloading connection box
    rod((x0 + 4, y0 + 1, 4.5), (x0 + 4, y0 + 8, 4.5), .3, "pipe", seg=8)
    rod((x1 - 6, y0 + 4, 4), (x1 - 6, y0 + 4, 16), 1.6, "tank", seg=14)                    # vapour scrubber
    rod((x1 - 6, y0 + 4, 16), (x1 - 6, y0 + 4, 19), .3, "pipe", seg=8)
    rod((x1 + 3, y0 + 2, 0), (x1 + 3, y0 + 2, 8), .15, "hivis", seg=6)                      # safety shower
    rod((x1 + 3, y0 + 2, 8), (x1 + 3, y0 + 2, 8.4), .9, "hivis", seg=12)
    rod((x0 - 4, y1 - 2, 0), (x0 - 4, y1 - 2, 22), .12, "steel", seg=6)                      # wind sock mast
    rod((x0 - 4, y1 - 2, 21), (x0 - 1, y1 - 2, 20.6), .5, "hivis_o", r2=.2, seg=10)
    dress(False)

    # auxiliary boiler
    it = find("Auxiliary boiler")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    box(x0 - 2, x0, y0 + 30, y0 + 50, 6, 20, "machine")                                     # burner front / windbox
    rod((x0 - 4, y0 + 40, 13), (x0 - 2, y0 + 40, 13), 3.2, "machine", seg=16)             # burner
    rod((x0 - 10, y0 + 40, 6), (x0 - 4, y0 + 40, 6), 2.6, "fan", seg=16)                  # FD fan
    rod((x0 - 10, y0 + 40, 9), (x0 - 10, y0 + 40, 17), 1.8, "duct", seg=14)               # inlet silencer
    box(x1 - 14, x1 - 6, y1 - 14, y1 - 6, 30, 40, "duct")                                   # economizer on the breeching
    box(x0 + 4, x0 + 18, y0 - 8, y0 - .5, 0, .6, "concrete")                                # feedwater pump skid
    for xp in (x0 + 7, x0 + 14):
        rod((xp, y0 - 6, 2), (xp, y0 - 3, 2), 1.1, "pump", seg=12)
        rod((xp, y0 - 3, 2), (xp, y0 - 1, 2), 1, "motor", seg=12)
    dress(False)

    # air compressors: receivers and dryer north of the building
    it = find("Air compressors AC-A/B/C")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    for xr in (x0 + 15, x0 + 28):
        rod((xr, y1 + 7, 0), (xr, y1 + 7, 12), 3, "tank", seg=18)
        rod((xr, y1 + 7, 12), (xr, y1 + 7, 13.2), 3, "tank", r2=1, seg=18)
        rod((xr, y1 + 7, 13.2), (xr, y1 + 7, 14.5), .3, "red", seg=8)                     # relief valve
    box(x0 + 38, x0 + 50, y1 + 2, y1 + 12, 0, 9, "cabinet")                                 # desiccant dryer
    for xd in (x0 + 41, x0 + 47):
        rod((xd, y1 + 7, 9), (xd, y1 + 7, 11.5), 1.3, "tank", seg=12)
    pipe([(x0 + 10, y1, 6), (x0 + 10, y1 + 7, 6), (x0 + 12, y1 + 7, 6)], 6, .3, "pipe")
    dress(False)

    # oil-water separator
    it = find("Oil-water separator")
    x0, x1, y0, y1 = it["fp"]
    on(it)
    dress(True)
    for xh in (x0 + 5, x0 + 13, x0 + 21):
        box(xh - 1.2, xh + 1.2, y0 + 2.8, y0 + 5.2, 8, 8.3, "grating")                    # access hatches
    rod((x0 - 3, y0 + 4, 4), (x0, y0 + 4, 4), .5, "pipe", seg=8)                          # inlet
    box(x1 - 4, x1 - 1, y0 + 6, y0 + 8, 8, 10, "panel")                                   # oil skimmer drive
    dress(False)
