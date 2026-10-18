"""Turbine hall interior finish (user review: the hall read as one flat light grey). As in a real H-class hall:
- the EL 20 turbine deck in a dark, low-sheen epoxy coating (deck_epoxy), so the machines stand on a dark floor;
- the four generators (GTG-1..3, STG) in a deep painted blue-grey (gen_paint), the turbine casings stay steel;
- the hall's structural steel (columns, girts, crane rails) painted mid blue-grey (hall_steel) against light cladding;
- each gas turbine read in sections, as a real H-class unit does: inlet plenum in the generator blue (gen_paint), a
  dark machined compressor casing (gt_cold), a darker combustor section (gt_comb) and the hot end, turbine casing
  and exhaust diffuser, under quilted silver insulation blankets (gt_blanket); flanges and rings stay bright steel;
- yellow walkway / keep-clear lines on the deck round each machine train (deck_line, flat on the deck surface);
- on the east end wall, the one you see down the GT row: "3x1 CCGT" in large lettering and a US flag (28 x 14.7 ft,
  13 stripes, 50 stars), both above the steam-turbine exhaust penetration.
No equipment geometry changes."""
import fuel
from fuel import find, box, on

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
    n += end_wall()
    return n


def end_wall():
    """3x1 CCGT lettering and the US flag on the inside of the east end wall (inner face x 1099, facing west)."""
    import showcase
    on(find("Common turbine hall"))
    fuel.D = True
    xf = 1099.0
    showcase.decal((xf - .1, 448, 73), (-1, 0, 0), 58, 14, [("3x1 CCGT", .8, True, "#1e2833")], bg=None)
    # flag: seen from the west, north (+y) is on the viewer's left, so the canton sits at the high-y, top corner
    w, h = 28.0, 28.0 / 1.9
    y0, y1, z0 = 501.0, 529.0, 66.0
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
