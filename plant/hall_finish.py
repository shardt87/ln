"""Turbine hall interior finish (user review: the hall read as one flat light grey). As in a real H-class hall:
- the EL 20 turbine deck in a dark, low-sheen epoxy coating (deck_epoxy), so the machines stand on a dark floor;
- the four generators (GTG-1..3, STG) in a deep painted blue-grey (gen_paint), the turbine casings stay steel;
- the hall's structural steel (columns, girts, crane rails) painted mid blue-grey (hall_steel) against light cladding.
Colour only: no geometry changes."""
import fuel
from fuel import find

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
    return n
