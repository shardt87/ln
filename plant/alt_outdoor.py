"""Alternative turbine-island layout for comparison (viewer view "Alternative: GTs outdoors"):
the three gas turbines stand outdoors on the EL 20 deck in their own OEM-style acoustic enclosures, and only the
steam turbine-generator sits in a building with its own bridge crane.

The base model follows the drawing set (one common turbine hall over all four units). For the comparison view the
hall's walls, columns, crane and roof-mounted electrical are on HALL_SHELL (shown in every other view) and this
module's parts are on ALT_OUTDOOR / ALT_ROOF (shown only in the alternative view). Nothing else changes: same
machines, deck, trays, IPB and piping.

Typical arrangement (warm-climate US practice): each GT package has a turbine-compartment enclosure and a generator
enclosure with ventilation fans, louvred intakes, access doors and its own CO2 fire suppression (the FS skids already
in the model). The ST building is a steel frame with insulated wall panels and a bridge crane for casing and rotor
lifts. Generic, not engineered.
"""
import fuel
from fuel import box, rod

LAY, ROOF = "ALT_OUTDOOR", "ALT_ROOF"
SHELL_ITEMS = ("Common turbine hall", "Bridge crane (parked over laydown bay)", "Turbine hall exterior electrical")


def enclosure(x0, x1, y0, y1, z0, z1, doors, fans):
    """Acoustic enclosure: panel walls with vertical stiffeners, a roof, access doors, roof vent fans."""
    t = .5
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + t), (x0, x1, y1 - t, y1), (x0, x0 + t, y0, y1), (x1 - t, x1, y0, y1)):
        box(a0, a1, b0, b1, z0, z1 - .4, "building", layer=LAY)                     # solid insulated panels
    box(x0 - .2, x1 + .2, y0 - .2, y1 + .2, z1 - .4, z1, "steel", layer=LAY)          # roof
    fuel.D = True
    for x in range(int(x0) + 4, int(x1) - 1, 4):                                       # panel joints, long walls
        for y in (y0 - .08, y1 + .08 - .1):
            box(x - .08, x + .08, y, y + .1, z0, z1 - .4, "steel", layer=LAY)
    for y in range(int(y0) + 4, int(y1) - 1, 4):
        for x in (x0 - .08, x1 - .02):
            box(x, x + .1, y - .08, y + .08, z0, z1 - .4, "steel", layer=LAY)
    for (x, y, side) in doors:                                                         # personnel doors
        if side in "ns":
            yy = y0 - .12 if side == "s" else y1 + .02
            box(x - 1.6, x + 1.6, yy, yy + .1, z0, z0 + 7.2, "door", layer=LAY)
        else:
            xx = x0 - .12 if side == "w" else x1 + .02
            box(xx, xx + .1, y - 1.6, y + 1.6, z0, z0 + 7.2, "door", layer=LAY)
    for (x, y) in fans:                                                                # roof vent fans + hoods
        rod((x, y, z1), (x, y, z1 + 2.2), 2.1, "fanhub", seg=24, layer=LAY)
        rod((x, y, z1 + 2.2), (x, y, z1 + 2.6), 2.5, "steel", seg=24, layer=LAY)
    fuel.D = False


def run(items, parts):
    # 1. the common hall's shell onto its own layer (floor slab and roof stay where they are)
    ids = {it["id"] for it in items if it["name"].startswith(SHELL_ITEMS)}
    n_shell = 0
    for p in parts:
        if p.get("item") in ids and p["layer"] != "HALL_ROOF" and p.get("color") != "concrete":
            p["layer"] = "HALL_SHELL"
            n_shell += 1
    # 2. gas turbines outdoors: turbine-compartment and generator enclosures on the deck
    for k in range(3):
        dx = 160 * k
        fuel.new_item(LAY, f"ALT: GT{k + 1} acoustic enclosure (turbine compartment)", (613.6 + dx, 643.5 + dx, 467, 540),
                      (20, 48.6), register=False, area="A", sheet="typical (alternative layout)",
                      info="Outdoor GT package enclosure: insulated acoustic panels, ventilation fans, access doors; "
                           "CO2 fire suppression from the FS skid. Shown only in the alternative-layout view.")
        enclosure(613.6 + dx, 643.5 + dx, 467, 540, 20, 46, doors=[(613.6 + dx, 490, "w"), (643.5 + dx, 515, "e")],
                  fans=[(624 + dx, 500), (636 + dx, 520)])
        fuel.new_item(LAY, f"ALT: GTG-{k + 1} generator enclosure", (619 + dx, 641 + dx, 411, 455), (20, 44.6),
                      register=False, area="A", sheet="typical (alternative layout)",
                      info="Outdoor generator enclosure over the H2-cooled generator. Alternative-layout view only.")
        enclosure(619 + dx, 641 + dx, 411, 455, 20, 42, doors=[(641 + dx, 440, "e")], fans=[(630 + dx, 433)])
    # 3. the steam turbine-generator in its own building with a bridge crane
    x0, x1, y0, y1, H = 1016.0, 1104.0, 405.0, 560.0, 90.0
    fuel.new_item(LAY, "ALT: steam turbine building (ST, STG and auxiliaries, bridge crane)", (x0, x1, y0, y1), (0, H),
                  register=False, area="A", sheet="typical (alternative layout)",
                  info="With the GTs outdoors only the ST keeps a building: casing halves and rotors need a bridge crane, "
                       "and the ST valves, lube-oil and EHC systems stay out of the weather. Alternative-layout view only.")
    t = .6
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + t), (x0, x1, y1 - t, y1), (x0, x0 + t, y0, y1), (x1 - t, x1, y0, y1)):
        box(a0, a1, b0, b1, 0, H, "hall", layer=LAY)
    for x in [x0 + 22 * i for i in range(5)]:                                          # frame columns
        for y in (y0 + .6, y1 - 1.8):
            box(x - .6, x + .6, y, y + 1.2, 0, H, "steel", layer=LAY)
    for y in (y0 + 3, y1 - 3):                                                         # crane runway girders + rails
        box(x0 + .6, x1 - .6, y - .7, y + .7, 74, 76, "steel", layer=LAY)
    box(1052, 1058, y0 + 2, y1 - 2, 77, 81, "yellow", layer=LAY)                       # crane bridge
    box(1053, 1057, 470, 478, 74.5, 77, "steel", layer=LAY)                            # trolley / hook block
    fuel.D = True
    for z in (22, 44, 66):                                                             # wall girts
        for (a0, a1, b0, b1) in ((x0, x1, y0 - .2, y0), (x0, x1, y1, y1 + .2)):
            box(a0, a1, b0, b1, z - .2, z + .2, "steel", layer=LAY)
    box(1070, 1090, y0 - .15, y0 - .05, 0, 22, "door", layer=LAY)                       # roll-up door, south wall
    fuel.D = False
    box(x0 - .5, x1 + .5, y0 - .5, y1 + .5, H, H + 1.2, "roof", layer=ROOF)
    return n_shell
