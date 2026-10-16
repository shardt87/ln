"""Visual hierarchy (user review): the combined-cycle power block, the three HRSGs and their stacks, is the hero.
- the brand palette, only on the hero: stack platform and HRSG access handrails in black (hero_rail),
  a 7 ft burnished-copper band (hero_accent) and a thin 2 ft band a third of the way down below each stack's top platform, "HRSG 1/2/3" lettered large in copper on both casing faces;
- the HRSG / stack cladding is the darkest, richest finish in the plant (pro_look / palette), everything else a
  step lighter and more neutral, and handrails elsewhere galvanized grey instead of safety yellow.
Colour and lettering only: no drawn geometry changes."""
import fuel
from fuel import rod, on, find

COPPER = "#a65428"      # Southwire deck copper (lettering); bands burnished copper, railings black


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def build():
    n = 0
    for k in range(3):
        dx = 160 * k
        ids = {find(f"HRSG {k + 1} stack")["id"], find(f"HRSG {k + 1} + SCR")["id"]}
        for p in fuel.G["parts"]:
            if p["item"] in ids and p["color"] in ("rail", "sp_yellow"):
                p["color"] = "hero_rail"                                                   # black handrails
                n += 1
        on(find(f"HRSG {k + 1} stack"))
        fuel.D = True
        rod((630 + dx, 790, 156), (630 + dx, 790, 163), 11.08, "hero_accent", seg=48)     # accent band (copper)
        rod((630 + dx, 790, 124), (630 + dx, 790, 126), 11.08, "hero_accent", seg=48)     # thin second band
        fuel.D = False
        on(find(f"HRSG {k + 1} + SCR"))
        fuel.D = True
        for (x, nx) in ((596.7 + dx, -1), (663.3 + dx, 1)):
            decal((x, 694, 70), (nx, 0, 0), 34, 9, [(f"HRSG {k + 1}", .9, True, COPPER)], bg=None)
        fuel.D = False
    return n
