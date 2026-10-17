"""Visual hierarchy (user review): the combined-cycle power block, the three HRSGs and their stacks, is the hero.
- the brand accent, only on the hero: a 7 ft burnished-copper band (hero_accent) below each stack's top platform and
  a thin 2 ft band a third of the way down, "HRSG 1/2/3" lettered large in copper on both casing faces; stacks,
  railings and platforms keep their original finishes (the black rails / crown and white-shell trials were reverted);
- the stack shells light matte grey (stack) so they and their copper bands read against the muted CCS; the HRSG
  casing is the darkest, richest finish in the plant (pro_look / palette), everything else a
  step lighter and more neutral, and handrails elsewhere galvanized grey instead of safety yellow.
Colour and lettering only: no drawn geometry changes."""
import fuel
from fuel import rod, on, find

COPPER = "#a65428"      # Southwire deck copper (lettering); bands burnished copper


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def build():
    n = 0
    for k in range(3):
        dx = 160 * k
        stack = find(f"HRSG {k + 1} stack")
        for p in fuel.G["parts"]:                   # stack shell in light matte grey, apart from the dark HRSG casing
            if p["item"] == stack["id"] and p["kind"] == "rod" and p["color"] == "hrsg" and p.get("r", 0) >= 10.9:
                p["color"] = "stack"
        on(stack)
        fuel.D = True
        rod((630 + dx, 790, 156), (630 + dx, 790, 163), 11.08, "hero_accent", seg=48)     # accent band (copper)
        rod((630 + dx, 790, 124), (630 + dx, 790, 126), 11.08, "hero_accent", seg=48)     # thin second band
        fuel.D = False
        on(find(f"HRSG {k + 1} + SCR"))
        fuel.D = True
        for (x, nx) in ((596.7 + dx, -1), (663.3 + dx, 1)):
            decal((x, 694, 70), (nx, 0, 0), 34, 9, [(f"HRSG {k + 1}", .9, True, COPPER)], bg=None)
        fuel.D = False
        n += 1
    return n
