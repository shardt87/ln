"""The turbine hall's facade language, lighter, on the other generation buildings (owner, Oct 20: the combined
cycle stays the hero; the rest should read as the same campus without competing with it). No chevrons, no large
lettering, no logos here:
- RICE engine hall: a 1 ft copper band (the hall's is 1.6 ft) at about two thirds of the wall, black coping on the
  roof edge, black corner pilasters, and a name sign over each end roll-up door;
- SC-1 / SC-2: the same band and coping round the turbine enclosure (its own SC-n nameplate stays);
- the modular e-houses (MOD-EH, MOD-LV, black-start switchgear): a copper band just under the roof and a name sign
  beside the door.
Signs in the gallery-door style (Southwire black panel, white letters). Strips are cut round anything standing at
the walls (hall_exterior.Face). Typical, not engineered."""
import fuel
from fuel import find, new_item, on
from hall_exterior import Face, hstrip, pilaster

SIGN_BG = "#1d1f21"


def faces(x0, x1, y0, y1, sk, wc):
    """(face, a0, a1) for the four walls of a box; the end faces run .45 past the corners so bands wrap them."""
    return ((Face(1, y0, -1, sk, wc), x0, x1), (Face(1, y1, 1, sk, wc), x0, x1),
            (Face(0, x0, -1, sk, wc), y0 - .45, y1 + .45), (Face(0, x1, 1, sk, wc), y0 - .45, y1 + .45))


def sign(c, n, w, h, text):
    import showcase
    showcase.decal(c, n, w, h, [(text, .56, True, "#ffffff")], bg=SIGN_BG)


def finish_item(bld, label, fp, z):
    it = new_item(bld["layer"], f"{label} exterior finish: copper band, coping, name sign", fp, z,
                  area=bld.get("area"), register=False,
                  info="The campus facade language, lighter than on the turbine hall: copper band, black coping, "
                       "a name sign. Typical, not engineered.")
    on(it)
    return it


def building(name, label, box_, zb, zc, wc, corners=True, signs=()):
    """box_ = (x0, x1, y0, y1, ztop); zb = copper band (z0, z1); zc = coping (z0, z1) or None."""
    bld = find(name)
    x0, x1, y0, y1, zt = box_
    it = finish_item(bld, label, [x0 - 2, x1 + 2, y0 - 2, y1 + 2], [0, zt + 1])
    fuel.D = True
    n = 0
    F = faces(x0, x1, y0, y1, ({it["id"]}, {bld["id"]}), wc)
    for f, a0, a1 in F:
        n += hstrip(f, a0, a1, *zb, .25, "hero_accent")
        if zc:
            n += hstrip(f, a0, a1, *zc, .3, "hero_rail")
    if corners:
        for f, a0, a1 in F[:2]:
            n += pilaster(f, x0 + .6, 0, zb[0], w=1.2) + pilaster(f, x1 - .6, 0, zb[0], w=1.2)
    for (c, nrm, w, h, text) in signs:
        sign(c, nrm, w, h, text)
        n += 1
    fuel.D = False
    return n


def build():
    n = 0
    # RICE engine hall: walls 1570-1810 x 1040-1130, eaves EL 34; roll-up doors in both end walls (y 1077-1093, to
    # EL 16), so the signs sit over them
    n += building("RICE engine hall (8 engines)", "RICE engine hall", (1570, 1810, 1040, 1130, 34),
                  (22.5, 23.5), None, ("hall", "roof", "steel"),
                  signs=[((1569.75, 1085, 18.0), (-1, 0, 0), 16.0, 2.4, "RICE ENGINE HALL"),
                         ((1810.25, 1085, 18.0), (1, 0, 0), 16.0, 2.4, "RICE ENGINE HALL")])
    # its long walls already carry a steel eave trim (EL 33.4-34.2): painted black, it is the coping; the end walls get
    # a matching strip
    rice = find("RICE engine hall (8 engines)")
    for p in fuel.G["parts"]:
        if p["item"] == rice["id"] and p["kind"] == "box" and p["color"] == "steel" and p["min"][2] == 33.4:
            p["color"] = "hero_rail"
            n += 1
    on(find("RICE engine hall exterior finish"))
    fuel.D = True
    sk = ({fuel.G["cur"]["id"]}, {rice["id"]})
    for f in (Face(0, 1570, -1, sk, ("hall", "roof", "steel")), Face(0, 1810, 1, sk, ("hall", "roof", "steel"))):
        n += hstrip(f, 1039.1, 1130.9, 33.4, 34.2, .3, "hero_rail")
    fuel.D = False
    # SC-1 / SC-2: the turbine enclosure (x +25 .. +69.5 of the package, y 1193-1217, EL 1.5-22)
    for k, x in ((1, 1910), (2, 2110)):
        n += building(f"SC-{k}: aeroderivative simple-cycle unit", f"SC-{k} turbine enclosure",
                      (x + 25, x + 69.5, 1193, 1217, 22), (17.6, 18.6), (21.2, 22.0), ("machine", "roof"),
                      corners=False)              # the enclosure already carries its SC-n nameplate
    # e-houses: band under the roof eave, sign beside the door (south faces)
    n += building("MOD-EH: 13.8 kV modular collector e-house", "MOD-EH", (1915.3, 1994.7, 880.3, 899.7, 15.4),
                  (13.9, 14.7), None, ("ehouse", "roof"), corners=False,
                  signs=[((1944.0, 880.0, 7.0), (0, -1, 0), 12.0, 1.8, "MOD-EH  13.8 kV")])
    n += building("MOD-LV 480 V board", "MOD-LV", (2215.3, 2266.7, 970.3, 981.7, 9.4),
                  (7.9, 8.7), None, ("ehouse", "roof"), corners=False,
                  signs=[((2240.0, 970.0, 6.0), (0, -1, 0), 10.0, 1.8, "MOD-LV  480 V")])
    n += building("BS black-start switchgear", "Black-start switchgear", (1625.3, 1644.7, 875.3, 892.7, 11.4),
                  (9.9, 10.7), None, ("ehouse", "roof"), corners=False,
                  signs=[((1638.5, 875.0, 6.5), (0, -1, 0), 9.0, 1.6, "BLACK-START SWGR")])
    return n
