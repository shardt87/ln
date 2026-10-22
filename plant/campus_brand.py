"""The turbine hall's facade language, lighter, on the other generation buildings (owner, Oct 20: the combined
cycle stays the hero; the rest should read as the same campus without competing with it). No chevrons, no large
lettering, no logos here:
- RICE engine hall: a 1 ft copper band (the hall's is 1.6 ft) at about two thirds of the wall, black coping on the
  roof edge, black corner pilasters, and a name sign over each end roll-up door; since Oct 22 the copper chevrons on
  the east end wall, beside the door (the owner's last branding step: the rest of the modular yard stays as is);
- SC-1 / SC-2: since Oct 21 the combined cycle's set (owner): the hall's 1.6 ft band, coping, corner pilasters,
  metallic copper chevrons at the exhaust end pointing at the paired stacks, and the unit painted large (SC1 / SC2);
- the modular e-houses (MOD-EH, MOD-LV, black-start switchgear) stay plain (owner, Oct 20).
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


def building(name, label, box_, zb, zc, wc, corners=True, signs=(), walls=None):
    """box_ = (x0, x1, y0, y1, ztop); zb = copper band (z0, z1); zc = coping (z0, z1) or None; walls = the item the
    wall panels are in, when not the building's own (SC packages since Oct 21)."""
    bld = find(name)
    x0, x1, y0, y1, zt = box_
    it = finish_item(bld, label, [x0 - 2, x1 + 2, y0 - 2, y1 + 2], [0, zt + 1])
    fuel.D = True
    n = 0
    F = faces(x0, x1, y0, y1, ({it["id"]}, {bld["id"]} | ({find(walls)["id"]} if walls else set())), wc)
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
    # RICE east end wall: the combined cycle's copper chevrons (metallic, as on the hall gable) north of the roll-up
    # door and pointing at it, running through the band to the eave trim; no lettering beyond the name sign (Oct 22)
    rf = find("RICE engine hall exterior finish")
    fuel.G["decals"].append(dict(c=[1810.07, 1110.0, 17.1], n=[1, 0, 0], w=14.0, h=32.6, bg=None, lines=[],
                                 item=rf["id"], layer=rf["layer"], brand=0, img="rice_chevrons.png", print=1, metal=.7))
    n += 1
    # SC-1 / SC-2: the turbine enclosure (x +25 .. +69.5 of the package, y 1193-1217, EL 1.5-22)
    for k, x in ((1, 1910), (2, 2110)):
        from sc2_mirror import mx
        e0, e1 = (x + 25, x + 69.5) if k == 1 else (mx(x + 69.5), mx(x + 25))   # SC-2 stands mirrored
        n += building(f"SC-{k}: aeroderivative simple-cycle unit", f"SC-{k} turbine enclosure",
                      (e0, e1, 1193, 1217, 22), (17.2, 18.8), (21.2, 22.0), ("machine", "roof", "ehouse", "door", "xray"),
                      walls=f"SC-{k} package enclosure")
        # the combined cycle's livery on the south face (owner, Oct 21): metallic copper chevrons at the exhaust end
        # pointing at the paired stacks, carried up through the band to the coping as on the hall gable, and the unit
        # painted large in the hall's Barlow face between the doors (the white nameplate came off)
        it = find(f"SC-{k} turbine enclosure exterior finish")
        X = (lambda v: v) if k == 1 else mx
        fuel.G["decals"].append(dict(c=[X(x + 62.5), 1192.86, 11.35], n=[0, -1, 0], w=11.0, h=19.7, bg=None,
                                     lines=[], item=it["id"], layer=it["layer"], brand=0,
                                     img="sc_chevrons_e.png" if k == 1 else "sc_chevrons_w.png", print=1, metal=.7))
        fuel.G["decals"].append(dict(c=[X(x + 43), 1192.86, 12.9], n=[0, -1, 0], w=(8.8, 10.1)[k - 1], h=5.4, bg=None, lines=[],
                                     item=it["id"], layer=it["layer"], brand=0, img=f"unit_SC{k}.png", print=1))
        n += 2
    # (the e-houses had a band and name sign here; taken off Oct 20 at the owner's request, they stay plain equipment)
    return n
