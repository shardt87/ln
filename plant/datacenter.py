"""BTM data centre (design option, area L): cable routes and LOD 3 dressing.

Routes (buried, OPT_DC_ROUTES):
- modular yard MOD-EH (13.8 kV collector) to the BTM step-ups T1 and T2;
- 230 kV backup / grid-parallel tie from the D6 bay of the plant switchyard to BTM-TIE, outside the
  east fence (the 230 kV breaker at the campus end is normally open);
- step-ups and tie to the 34.5 kV switchgear; switchgear to the two data-hall electrical galleries
  (a ring through each gallery); BTM BESS and the genset step-up to the switchgear; the genset
  collectors along both genset rows.
Dressing: rooftop dry-cooler banks with fans and coolant headers on both halls, louvres, loading
docks and doors; BTM substation fence and signs; genset radiator fans; diverse fibre entries.
All typical, not engineered.
"""
import fuel
from fuel import box, rod, find, on

SHEET = "design option (BTM data centre)"
L = "OPT_DC_ROUTES"


def routes(add_route):
    r = lambda t, pts: add_route(t, pts, layer=L, sheet=SHEET)
    # supply: modular yard 13.8 kV (cable bus) to BTM-T1 / T2; 230 kV tie from D6; all onto the 34.5 kV buses
    r("mvlv_cable", [(1995, 892), (2520, 892), (2520, 790), (2530, 790)])        # MOD-EH to BTM-T1
    r("mvlv_cable", [(2520, 790), (2520, 760), (2597, 760), (2597, 770)])        # branch to BTM-T2
    r("hv_cable", [(2030, 120), (2435, 120), (2435, 790), (2630, 790)])           # 230 kV tie from D6
    for x in (2547, 2597, 2645):                                                  # step-ups / tie to switchgear
        r("mvlv_cable", [(x, 815), (x, 860)])
    r("mvlv_cable", [(2686, 698), (2686, 845), (2640, 845), (2640, 860)])        # BESS to the bus tie section
    # 2N distribution: four 34.5 kV feeder loops per hall side, six pad-mount transformers each, in one duct bank
    # per side along the transformer row
    sides = [  # (switchgear exit y, riser x, corridor y, direction of the corridor offsets)
        (896, 2676, 1323, 1), (891, 2681, 977, -1),       # hall A: A side (north), B side (south)
        (876, 2686, 923, 1), (866, 2704, 577, -1),        # hall B: A side (north), B side (south)
    ]
    for (ys, xr, yc, sgn) in sides:
        for j in range(4):
            x_end = 2742 + 22.5 * (6 * j + 5) + 9
            yy = yc + sgn * 1.2 * j
            r("mvlv_cable", [(2650, ys + j * .8), (xr + j * .9, ys + j * .8), (xr + j * .9, yy), (x_end, yy)])
    for (y0, y1) in ((1020, 1280), (620, 880)):                                  # LV: skids into the hall, gallery
        r("mvlv_cable", [(3000, y1 + 2), (3000, y1)])
        r("mvlv_cable", [(3000, y0 - 2), (3000, y0)])
        r("mvlv_cable", [(2731, (y0 + y1) / 2), (2726, (y0 + y1) / 2)])
    r("mvlv_cable", [(2565, 732), (2572, 732), (2572, 860)])                    # BTM-T3 to the bus tie section
    r("mvlv_cable", [(2520, 760), (2520, 732), (2530, 732)])                    # MOD-EH branch to BTM-T3
    for gx in (2606, 2628):                                                       # grounding transformers
        r("mvlv_cable", [(gx, 906), (gx, 900)])
    # backup: genset collectors (13.8 kV) to the paralleling switchgear, then GSU-1 / GSU-2 to the buses
    for y in (476, 536):
        r("mvlv_cable", [(2774, y), (3326, y)])
    r("mvlv_cable", [(2742, 462), (2736, 462)])                                   # paralleling gear to GSU-1
    r("mvlv_cable", [(2742, 542), (2736, 542)])                                   # paralleling gear to GSU-2
    r("mvlv_cable", [(2702, 462), (2696, 462), (2696, 600), (2699, 600), (2699, 850), (2650, 850)])   # GSU-1 to bus A
    r("mvlv_cable", [(2702, 542), (2699, 542), (2699, 600)])                      # GSU-2 joins, to bus B
    r("mvlv_cable", [(3060, 340), (2980, 340), (2980, 410), (2758, 410), (2758, 440)])   # admin / gate LV


# supply paths, colour-coded so the three operating modes read apart in the viewer and renders
# supply paths: tagged on items and routes (not painted), so the equipment keeps its real finishes;
# the viewer's "BTM power paths" toggle and the render callouts show them on demand
PATHS = {
    "btm_island": ("1  Islanded BTM power: campus gensets, BTM battery, 34.5 kV bus",
                   ("BTM BESS", "DC backup genset", "DC genset paralleling", "DC-GSU", "BTM 34.5 kV switchgear")),
    "btm_mod": ("2  Supply from the modular yard: 13.8 kV to the BTM step-ups (3 x 90 MVA, N+1)",
                ("BTM-T1:", "BTM-T2:", "BTM-T3:")),
    "btm_grid": ("3  230 kV grid tie to the plant switchyard (normally open)",
                 ("BTM-TIE:", "BTM 230 kV tie breaker")),
}


def path_of_route(r):
    pts = [tuple(p) for p in r["points"]]
    if r["type"] == "hv_cable" or pts[0] == (2645, 815):
        return "btm_grid"
    if pts[0] in ((1995, 892), (2520, 790), (2547, 815), (2597, 815), (2565, 732), (2520, 760)):
        return "btm_mod"
    return "btm_island"


def color_routes(routes):
    """Tag the campus cable routes with their supply path (route colour stays the cable colour)."""
    for r in routes:
        if r["layer"] == L:
            r["path"] = path_of_route(r)


def color_parts():
    """Tag the campus power items with their supply path; their parts keep their real colours."""
    for k, (label, prefixes) in PATHS.items():
        for it in fuel.G["items"]:
            if it["name"].startswith(prefixes):
                it["path"] = k
                it["info"] = ((it.get("info") or "") + f" Supply path: {label[3:]}.").strip()


def build():
    fuel.D = True
    for t, (y0, y1) in (("A", (1020, 1280)), ("B", (620, 880))):
        hall = find(f"Data hall {t}:")
        on(hall)
        for k in range(10):                                                      # rooftop dry-cooler banks
            x = 2750 + k * 52
            box(x, x + 40, y0 + 20, y1 - 20, 45, 46, "steel")                    # dunnage
            box(x + 1, x + 39, y0 + 22, y1 - 22, 46, 50, "bundle")
            for f in range(int((y1 - y0 - 44) // 14)):
                rod((x + 20, y0 + 30 + f * 14, 50), (x + 20, y0 + 30 + f * 14, 50.6), 5.6, "fan", seg=18)
            rod((x - 3, y0 + 22, 47), (x - 3, y1 - 22, 47), .9, "waterline", seg=10)   # supply / return headers
            rod((x + 43, y0 + 22, 47), (x + 43, y1 - 22, 47), .9, "waterline", seg=10)
        for k in range(9):                                                       # wall louvres (east face)
            box(3290, 3290.2, y0 + 15 + k * 30, y0 + 27 + k * 30, 20, 34, "louvre")
        for k in range(3):                                                       # loading docks (east)
            yd = y0 + 40 + k * 90
            box(3290, 3290.2, yd, yd + 12, 1, 15, "rollup")
            box(3290, 3296, yd - 1, yd + 13, 0, 4, "concrete")
            box(3296, 3296.6, yd + 1, yd + 11, 1, 4, "fanhub")                    # dock bumpers
        box(3290, 3290.2, y0 + 3, y0 + 7, 0, 8, "door")
        box(2730, 3290, y0 - .3, y0, 40, 44, "sign" if t == "A" else "hall")     # name band
    on(find("BTM 34.5 kV switchgear"))
    for (x0, x1, y0, y1) in ((2522, 2685, 705, 705.3), (2522, 2685, 925, 925.3), (2522, 2522.3, 705, 925),
                             (2685, 2685.3, 705, 925)):
        box(x0, x1, y0, y1, 0, 8, "fence")                                       # substation fence
    for x in (2560, 2620):
        box(x, x + 4, 704.6, 704.7, 4, 6.5, "sign")
        box(x, x + 4, 704.55, 704.6, 5.8, 6.5, "red")
    on(find("DC backup gensets"))
    for row, y in enumerate((440, 500, 560)):
        for k in range(12):
            x = 2780 + 46 * k
            for f in range(2):
                rod((x + 8 + f * 12, y + 6, 13), (x + 8 + f * 12, y + 6, 13.4), 4.2, "fan", seg=16)
    on(find("DC admin / security / NOC building"))
    for (x, y) in ((3075, 312), (3165, 312)):                                    # diverse fibre entries
        box(x - 1.5, x + 1.5, y - 1.5, y + 1.5, 0, .4, "concrete")
        rod((x, y, .4), (x, y, .5), 1.1, "fanhub", seg=12)
    rod((3170, 360, 24), (3170, 360, 40), .25, "steel", seg=6)                   # comms mast
    fuel.D = False
