"""Turbine hall interior finish (user review: the hall read as one flat light grey). As in a real H-class hall:
- the EL 20 turbine deck in a dark, low-sheen epoxy coating (deck_epoxy), so the machines stand on a dark floor;
- the four generators (GTG-1..3, STG) in a deep painted blue-grey (gen_paint), the turbine casings stay steel;
- the hall's structural steel (columns, girts, crane rails) painted mid blue-grey (hall_steel) against light cladding;
- each gas turbine read in sections, as a real H-class unit does: inlet plenum in the generator blue (gen_paint), a
  dark machined compressor casing (gt_cold), a darker combustor section (gt_comb) and the hot end, turbine casing
  and exhaust diffuser, under quilted silver insulation blankets (gt_blanket); flanges and rings stay bright steel;
- yellow walkway / keep-clear lines on the deck round each machine train (deck_line, flat on the deck surface);
- on the east end wall, the one you see down the GT row (Oct 19: on the van-livery black field, the sign in white,
  copper chevrons between it and the flag): "3x1 CCGT" in large lettering and a US flag (28 x 14.7 ft,
  13 stripes, 50 stars), both above the steam-turbine exhaust penetration.
No equipment geometry changes."""
import fuel
from fuel import find, box, on, new_item

GENERATORS = ("GTG-1: GT generator", "GTG-2: GT generator", "GTG-3: GT generator", "STG: steam-turbine generator")


def build():
    n = 0
    deck = find("Turbine deck EL 20")["id"]
    hall = find("Common turbine hall")["id"]
    gens = {find(g)["id"] for g in GENERATORS}
    for p in fuel.G["parts"]:
        if p["item"] == deck and p["color"] == "concrete":
            p["color"] = "deck_epoxy"
        elif p["item"] in gens and p["color"] == "steel":
            p["color"] = "gen_paint"
        elif p["item"] == hall and p["color"] == "steel":
            p["color"] = "hall_steel"
        else:
            continue
        n += 1
    for k in range(3):                                   # GT casing sections by position along the shaft (y)
        gt = find(f"GT{k + 1}: H-class")["id"]
        for p in fuel.G["parts"]:
            if p["item"] != gt or p["color"] != "machine":
                continue
            ys = (p["a"][1] + p["b"][1]) / 2 if p["kind"] == "rod" else (p["min"][1] + p["max"][1]) / 2
            if p["kind"] == "box" and p["max"][1] <= 467.5:
                p["color"] = "gen_paint"                 # inlet plenum
            elif p["kind"] == "rod" and 467 <= ys < 495 and p.get("r", 0) > 4:
                p["color"] = "gt_cold"                   # bellmouth and compressor casing
            elif p["kind"] == "rod" and 495 <= ys < 507 and p.get("r", 0) > 4:
                p["color"] = "gt_comb"                   # combustor section
            elif p["kind"] == "rod" and ys >= 507 and p.get("r", 0) > 4:
                p["color"] = "gt_blanket"                # turbine casing and exhaust diffuser
            else:
                continue
            n += 1
    on(find("Turbine deck EL 20"))
    fuel.D = True
    for (x0, x1, y0, y1) in ((612, 648, 407, 543), (772, 808, 407, 543), (932, 968, 407, 543), (1016, 1084, 407, 554)):
        w = .33                                                  # 4 in yellow line, 4 ft clear of the machine train
        for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + w), (x0, x1, y1 - w, y1), (x0, x0 + w, y0, y1), (x1 - w, x1, y0, y1)):
            box(a0, a1, b0, b1, 20.0, 20.02, "deck_line")
            n += 1
    fuel.D = False
    n += accents()
    n += end_wall()
    n += south_cladding()
    return n


def south_cladding():
    """Split the south cladding (upper south wall over the gallery roof, the gallery's outer wall, its doors and
    lights) and the main roof panels into their own item, so cutaway cameras can lift it off and look in at all four machine trains side by side.
    The structure (columns, girders) stays with the hall."""
    hall = find("Common turbine hall")
    it = new_item(hall["layer"], "Turbine hall south cladding and roof (lifted off in the cutaway views)", [480, 1100, 369, 560],
                  [0, 101], area=hall.get("area", "A"), info="Insulated wall panels, gallery doors and wall lights.")
    on(hall)
    n = 0
    for p in fuel.G["parts"]:
        if p["item"] != hall["id"] or p["kind"] != "box" or p["layer"] != hall["layer"]:
            continue
        lo, hi = p["min"], p["max"]
        upper = p["color"] == "hall" and lo[1] >= 402.5 and hi[1] <= 404.5 and lo[2] >= 59
        roof = p["color"] == "roof" and lo[2] >= 95                     # main roof panels
        outer = p["color"] in ("hall", "door", "lamp") and lo[1] >= 369.5 and hi[1] <= 372.5
        if upper or outer or roof:
            p["item"] = it["id"]
            n += 1
    on(it)                                              # the south wall's copper band lifts off with the cladding
    fuel.D = True
    box(481.0, 1098.8, 404.05, 404.25, 64.0, 65.6, "hero_accent")
    fuel.D = False
    return n + 1


def accents():
    """Southwire black and copper, as on the HRSGs and stacks: black stiffener rings and generator ribs, one copper
    band per machine (the GT turbine strut flange, the ST HP/IP lagging bands), and a copper band round the hall walls
    at EL 64 (the structural steel itself is hall_steel, now Southwire black). Yellow safety rails stay yellow."""
    n = 0
    gens = {find(g)["id"] for g in GENERATORS}
    gts = {find(f"GT{k + 1}: H-class")["id"] for k in range(3)}
    st = find("ST: steam turbine")["id"]
    for p in fuel.G["parts"]:
        if p["kind"] != "rod" or p["color"] != "steel":
            continue
        r, ys = p.get("r", 0), (p["a"][1] + p["b"][1]) / 2
        thin = abs(p["a"][1] - p["b"][1]) <= 1.3 and p["a"][0] == p["b"][0] and p["a"][2] == p["b"][2]
        if not thin:
            continue
        if p["item"] in gts and 472 <= ys <= 494 and r > 5:
            p["color"] = "hero_rail"                    # VGV ring and compressor stiffener rings
        elif p["item"] in gts and 524 <= ys <= 525.5 and r > 8:
            p["color"] = "hero_accent"                  # turbine strut flange: the copper band
        elif p["item"] in gens and r > 7:
            p["color"] = "hero_rail"                    # generator frame ribs
        elif p["item"] == st and r > 13:
            p["color"] = "hero_rail"                    # LP barrel stiffener rings
        elif p["item"] == st and 7.8 < r < 7.9:
            p["color"] = "hero_accent"                  # HP/IP lagging bands
        else:
            continue
        n += 1
    on(find("Common turbine hall"))
    fuel.D = True
    zb = (64.0, 65.6)                                   # copper band, above the gallery roof and below the flag
    box(481.0, 1098.8, 558.75, 558.95, *zb, "hero_accent")             # north wall
    box(480.05, 480.25, 404.3, 558.7, *zb, "hero_accent")              # west wall
    box(1098.75, 1098.95, 404.3, 558.7, *zb, "hero_accent")            # east wall, continuous under the sign and flag
    fuel.D = False
    return n + 3


def end_wall():
    """3x1 CCGT lettering and the US flag on the inside of the east end wall (inner face x 1099, facing west)."""
    import showcase
    on(find("Common turbine hall"))
    fuel.D = True
    xf = 1099.0
    # the plain lettering for the unbranded build; the branded build prints the full graphic (blender/hall_sign.py):
    # 3x1 CCGT, a copper rule, WIRE & CABLE PARTNER and the Southwire logo
    # the field-service van livery above the band (blender/hall_sign.py: livery_east_in.png): copper chevrons
    # between the flag and the sign pointing at it, the black field behind the sign to the SE corner
    fuel.G.setdefault("decals", []).append(dict(c=[xf - .05, 453.5, 81.85], n=[-1, 0, 0], w=99.0, h=32.3, bg=None,
                                                lines=[], item=fuel.G["cur"]["id"], layer=fuel.G["cur"]["layer"],
                                                brand=0, img="livery_east_in.png", print=1))
    showcase.decal((xf - .1, 446, 76), (-1, 0, 0), 58, 14, [("3x1 CCGT", .8, True, "#f2f2f0")], bg=None,
                   generic_only=True)
    it = fuel.G["cur"]
    fuel.G.setdefault("decals", []).append(dict(c=[xf - .1, 446.0, 81.5], n=[-1, 0, 0], w=60.0, h=30.0, bg=None, lines=[],
                                                item=it["id"], layer=it["layer"], brand=1, img="hall_wall_sign_dark.png",
                                                print=1))
    # flag: seen from the west, north (+y) is on the viewer's left, so the canton sits at the high-y, top corner
    w, h = 28.0, 28.0 / 1.9
    y0, y1, z0 = 503.0, 531.0, 69.0                    # above the copper band (EL 64-65.6)
    st = h / 13
    n = 0
    for i in range(13):
        za = z0 + h - (i + 1) * st
        box(xf - .15, xf - .05, y0, y1, za, za + st, "flag_red" if i % 2 == 0 else "flag_white")
        n += 1
    cw, ch = .4 * w, 7 * st
    box(xf - .2, xf - .15, y1 - cw, y1, z0 + h - ch, z0 + h, "flag_blue")
    for r in range(9):                                   # 50 stars: 9 rows alternating 6 and 5
        k = 6 if r % 2 == 0 else 5
        zs = z0 + h - ch * (r + 1) / 10
        for c in range(k):
            ys = y1 - cw * ((2 * c + 1) if k == 6 else (2 * c + 2)) / 12
            box(xf - .24, xf - .2, ys - .22, ys + .22, zs - .22, zs + .22, "flag_white")
            n += 1
    fuel.D = False
    return n + 2
