"""Zone 07, infrastructure and construction: the plant's front door (user, Oct 19). Part 1, the control / admin
building, outside and on the roof. The same design family as the turbine hall, no Southwire logo here:
- facade: a copper band round all four walls above the window band, black coping on the parapet, black corner
  pilasters; at the glazed entrance a black portal (piers either side of the canopy, a lintel above it) lettered
  SK-3X1 POWER CAMPUS / CONTROL & ADMINISTRATION; a monument sign at the entrance walk and three flagpoles (the US
  flag in the middle);
- rooftop HVAC: two more packaged units (over the lobby and over the control room, the 24/7 load) beside the two the
  rooftop pass placed, and every unit wired as an electrician would: a fused disconnect on a strut stand beside the
  unit, rigid conduit up through the roof into it, a short MC whip from the disconnect into the unit's electrical
  section; roof-walkway pavers from the hatch to each unit;
- precision cooling for the DCS / server room (x 220-240): a concrete pad north of the building with four
  condensing units, their disconnects on a strut rack against the wall, conduit feeders and copper line sets into
  the building.
Typical, not engineered. Built last (after the rooftop pass and hall_exterior), so it sees everything already there.
"""
import math

import fuel
from fuel import box, rod, find, new_item, on

BX0, BX1, BY0, BY1 = 83.0, 320.0, 345.0, 396.0            # admin building outer faces
ZR, ZP = 18.5, 20.0                                          # roof deck, parapet top
XM = (BX0 + BX1) / 2                                         # entrance centre (detail3: glazed door xm +- 5)


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def facade():
    import showcase
    bld = find("Control / admin building (main")
    it = new_item(bld["layer"], "Control / admin building exterior finish: copper band, coping, entrance portal, sign",
                  [81, 322, 343, 398], [0, 20.6], area=bld.get("area"), register=False,
                  info="The turbine hall's facade language on the control / admin building: copper band, black coping "
                       "and corner pilasters, a black entrance portal with the campus name. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    # band, coping and corner pilasters as strips cut round anything standing at the walls (the hall's helper; the
    # building's own panels, roof, windows and base count as wall)
    from hall_exterior import Face, hstrip, pilaster
    sk = ({it["id"]}, {bld["id"]})
    wc = ("building", "roof", "concrete", "window")
    S, N = Face(1, BY0, -1, sk, wc), Face(1, BY1, 1, sk, wc)
    Wf, E = Face(0, BX0, -1, sk, wc), Face(0, BX1, 1, sk, wc)
    for f, a0, a1 in ((S, BX0, BX1), (N, BX0, BX1), (Wf, BY0 - .45, BY1 + .45), (E, BY0 - .45, BY1 + .45)):
        n += hstrip(f, a0, a1, 13.6, 14.4, .25, "hero_accent")                            # copper band
        n += hstrip(f, a0, a1, ZP - .5, ZP + .3, .3, "hero_rail")                          # coping
    for f, a in ((S, BX0 + 1.0), (S, BX1 - 1.0), (N, BX0 + 1.0), (N, BX1 - 1.0)):        # corner pilasters
        n += pilaster(f, a, 0, ZP - .5)
    # entrance portal: piers clear of the canopy (x 192.5-210.5) and the band windows, lintel above the canopy
    # (x 189.8-213.2: the roll-up door starts at x 213.35); in front of the concrete base band (y 344.88)
    y0, y1 = BY0 - .7, BY0 - .13
    box(XM - 11.7, XM - 9.1, y0, y1, 0, 17.4, "hero_rail")
    box(XM + 9.1, XM + 11.7, y0, y1, 0, 17.4, "hero_rail")
    box(XM - 11.7, XM + 11.7, y0, y1, 10.9, 17.4, "hero_rail")
    n += 3
    fuel.D = False
    showcase.decal((XM, y0 - .03, 14.15), (0, -1, 0), 22.0, 5.6,
                   [("SK-3X1 POWER CAMPUS", .42, 1, "#f2f2f0"), ("CONTROL & ADMINISTRATION", .2, 1, "#c4744a")], bg=None)
    # monument sign at the entrance walk (west of the walk), black with a copper cap
    mx, my = XM - 28.0, 318.0
    fuel.D = True
    box(mx - 11, mx + 11, my - 1.2, my + 1.2, 0, .6, "concrete")
    box(mx - 10, mx + 10, my - .8, my + .8, .6, 5.6, "hero_rail")
    box(mx - 10.2, mx + 10.2, my - 1.0, my + 1.0, 5.6, 6.0, "hero_accent")
    n += 3
    fuel.D = False
    showcase.decal((mx, my - .83, 3.3), (0, -1, 0), 18.5, 3.8,
                   [("SK-3X1 POWER CAMPUS", .4, 1, "#f2f2f0"), ("3x1 COMBINED CYCLE  ·  CONTROL & ADMINISTRATION", .18, 1,
                                                                 "#c4744a")], bg=None)
    # three flagpoles east of the walk, 11 ft apart so the flags fly clear of each other: the US flag on the taller
    # middle pole, the state flag (blue) to the west and a company flag (black with a copper stripe) to the east
    fuel.D = True
    for k, fx in enumerate((XM + 20.0, XM + 31.0, XM + 42.0)):
        fy = 318.0
        top = 32.0 if k == 1 else 28.0
        box(fx - 1.2, fx + 1.2, fy - 1.2, fy + 1.2, 0, .5, "concrete")
        rod((fx, fy, .5), (fx, fy, top), .22, "alu", r2=.12, seg=12)
        rod((fx, fy, top), (fx, fy, top + .5), .35, "lamp", seg=10)                         # finial
        z1 = top - .6
        if k == 1:
            w, h = 9.0, 9.0 / 1.9
            st = h / 13
            for i in range(13):
                za = z1 - (i + 1) * st
                box(fx + .25, fx + .25 + w, fy - .04, fy + .04, za, za + st, "flag_red" if i % 2 == 0 else "flag_white")
            box(fx + .25, fx + .25 + .4 * w, fy - .07, fy + .07, z1 - 7 * st, z1, "flag_blue")
            n += 14
        elif k == 0:
            box(fx + .25, fx + 6.25, fy - .04, fy + .04, z1 - 3.6, z1, "flag_blue")
            n += 1
        else:
            box(fx + .25, fx + 6.25, fy - .04, fy + .04, z1 - 3.6, z1, "hero_rail")
            box(fx + .25, fx + 6.25, fy - .07, fy + .07, z1 - 2.5, z1 - 2.0, "hero_accent")
            n += 2
        n += 3
    fuel.D = False
    return n


def disconnect(x, y, z, face):
    """Fused safety switch on a two-post strut stand; face = +-1 along y (which way the door faces)."""
    for dx in (-.55, .55):
        rod((x + dx, y, z), (x + dx, y, z + 3.4), .07, "steel", seg=4)
    box(x - .7, x + .7, y - .25, y + .25, z + 1.7, z + 3.4, "panel")
    box(x - .55, x + .55, y + face * .25, y + face * .28, z + 1.85, z + 3.25, "cabinet")      # door
    box(x - .1, x + .1, y + face * .28, y + face * .45, z + 2.9, z + 3.1, "sw_red")            # handle
    return 6


def hvac():
    roof = find("Control / admin building: rooftop HVAC")
    on(roof)
    fuel.D = True
    n = 0
    # the units the rooftop pass placed, plus two: over the lobby and over the control room
    units = [(258.35, 379.65, 9.5, 5.5), (144.65, 358.45, 9.5, 5.5)]
    for (x, y) in ((190.0, 382.0), (294.0, 381.0)):
        w, d, h = 9.5, 5.5, 4.2
        box(x - w / 2 - .4, x + w / 2 + .4, y - d / 2 - .4, y + d / 2 + .4, ZR, ZR + 1.0, "steel")
        box(x - w / 2, x + w / 2, y - d / 2, y + d / 2, ZR + 1.0, ZR + 1.0 + h, "equip")
        box(x + w / 2 - 2.2, x + w / 2 + .05, y - d / 2 + .3, y + d / 2 - .3, ZR + 1.4, ZR + .8 + h, "bundle")
        for fy in (y - 1.3, y + 1.3):
            rod((x + w / 2 - 1.6, fy, ZR + 1.0 + h), (x + w / 2 - 1.6, fy, ZR + 1.35 + h), 1.15, "fan", seg=16)
            rod((x + w / 2 - 1.6, fy, ZR + 1.35 + h), (x + w / 2 - 1.6, fy, ZR + 1.5 + h), .35, "fanhub", seg=10)
        for k in (-1, 1):
            box(x + k * w / 5 - .9, x + k * w / 5 + .9, y - d / 2 - .05, y - d / 2 + .02, ZR + 1.4, ZR + .6 + h, "cabinet")
        units.append((x, y, w, d))
        n += 10
    # each unit: disconnect south of its west end, conduit up through the roof, MC whip into the electrical section
    for (x, y, w, d) in units:
        dx, dy = x - w / 2 + 1.0, y - d / 2 - 2.6
        n += disconnect(dx, dy, ZR, 1)
        rod((dx, dy, ZR - .3), (dx, dy, ZR + 1.7), .1, "steel", seg=6)                     # conduit through the roof
        box(dx - .35, dx + .35, dy - .35, dy + .35, ZR, ZR + .25, "steel")                  # roof penetration boot
        ex = x - w / 2 + 1.0
        poly([(dx + .3, dy + .25, ZR + 1.9), (dx + .3, dy + 1.0, ZR + 1.2), (ex + .3, y - d / 2 - .4, ZR + 1.2),
              (ex + .3, y - d / 2 - .05, ZR + 2.0)], .09, "cable_mc", seg=6)                # MC whip
        n += 5
    # roof walkway pavers from the hatch (x 309-312, y 358-362) west along y 366, spurs to the disconnects
    yw = 366.0
    box(150.0, 307.5, yw - 1.25, yw + 1.25, ZR, ZR + .12, "concrete")
    n += 1
    for (x, y, w, d) in units:
        dx, dy = x - w / 2 + 1.0, y - d / 2 - 2.6
        if dy < yw:
            box(dx - 1.25, dx + 1.25, dy + .6, yw - 1.25, ZR, ZR + .12, "concrete")
        n += 1
    fuel.D = False
    return n


def condensers():
    bld = find("Control / admin building (main")
    it = new_item(bld["layer"], "Control / admin building: precision-cooling condensing units for the DCS / server room",
                  [208, 252, 396, 414], [0, 12], area=bld.get("area"), register=False,
                  info="Four condensing units on a pad north of the building serving the DCS / server room's "
                       "precision cooling (N+1), disconnects on a strut rack against the wall, conduit feeders and "
                       "refrigerant line sets. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = 0
    box(210.0, 250.0, 401.0, 413.0, 0, .5, "concrete")                                  # pad
    rack_y = BY1 + .6
    for (a, b) in ((211.5, 212.0), (248.0, 248.5)):                                      # strut rack posts
        box(a, b, rack_y - .2, rack_y + .2, 0, 6.5, "steel")
    box(211.5, 248.5, rack_y - .2, rack_y + .2, 6.3, 6.5, "steel")
    n += 3
    for k in range(4):
        x = 215.0 + 10.0 * k
        box(x - 2.6, x + 2.6, 404.0, 410.0, .5, 4.8, "equip")                             # condensing unit
        box(x - 2.4, x + 2.4, 403.95, 404.0, .9, 4.4, "bundle")                           # coil face
        rod((x, 407.0, 4.8), (x, 407.0, 5.15), 1.9, "fan", seg=18)
        rod((x, 407.0, 5.15), (x, 407.0, 5.3), .4, "fanhub", seg=10)
        # disconnect on the rack, conduit from the building wall, whip into the unit
        box(x - .7, x + .7, rack_y + .2, rack_y + .7, 3.4, 5.1, "panel")
        box(x - .55, x + .55, rack_y + .7, rack_y + .73, 3.55, 4.95, "cabinet")
        poly([(x - .3, BY1, 9.0), (x - .3, rack_y + .45, 9.0), (x - .3, rack_y + .45, 5.1)], .1, "steel", seg=6)
        poly([(x + .3, rack_y + .7, 3.6), (x + .3, 402.6, 1.2), (x + .3, 404.0, 1.6)], .09, "cable_mc", seg=6)
        # refrigerant line set: suction (insulated, black) and liquid (copper), up the wall into the building
        for (o, r, c) in ((1.2, .14, "sp_black"), (1.7, .06, "copper")):                 # in above the window band
            poly([(x + o, 404.0, 2.4), (x + o, 400.6, 2.4), (x + o, BY1 + .3, 2.4), (x + o, BY1 + .3, 12.4),
                  (x + o, BY1, 12.4)], r, c, seg=6)
        n += 11
    fuel.D = False
    return n


def build():
    return dict(facade=facade(), hvac=hvac(), condensers=condensers())
