"""Visual hierarchy (user review): the combined-cycle power block, the three HRSGs and their stacks, is the hero.
- the brand palette, only on the hero: stack platform and HRSG access handrails in black (hero_rail),
  a 7 ft burnished-copper band (hero_accent) and a thin 2 ft band a third of the way down below each stack's top platform, "HRSG 1/2/3" lettered large in copper on both casing faces;
- the stack shells are light gloss (hero_stack) with silver stiffener rings (hero_ring), so the copper band and the
  black crown read against them; the HRSG casing keeps the darkest, richest finish; everything else neutral, and handrails elsewhere galvanized grey instead of safety yellow.
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
        stack = find(f"HRSG {k + 1} stack")["id"]
        for p in fuel.G["parts"]:
            if p["item"] == stack and p["kind"] == "rod" and p.get("r", 0) >= 10.9:
                if p["color"] == "hrsg":
                    p["color"] = "hero_stack"           # stack shell: light gloss, the brightest thing on the skyline
                    continue
                if p["color"] == "steel":
                    p["color"] = "hero_ring"            # stiffener rings: silver, so the shell stays light
                    continue
            if p["item"] in ids and p["color"] in ("rail", "sp_yellow", "steel", "grating", "stair"):
                p["color"] = "hero_rail"            # Southwire black: handrails, platforms, stairs, ladders, brackets
                n += 1
        on(find(f"HRSG {k + 1} stack"))
        fuel.D = True
        rod((630 + dx, 790, 156), (630 + dx, 790, 163), 11.08, "hero_accent", seg=48)     # accent band (copper)
        for (z0, z1) in ((154.6, 156), (163, 164.4)):                                   # black pinstripes framing it
            rod((630 + dx, 790, z0), (630 + dx, 790, z1), 11.09, "hero_rail", seg=48)
        rod((630 + dx, 790, 124), (630 + dx, 790, 126), 11.08, "hero_accent", seg=48)     # thin second band
        rod((630 + dx, 790, 171), (630 + dx, 790, 178), 11.08, "hero_rail", seg=48)       # black crown at the stack top
        fuel.D = False
        on(find(f"HRSG {k + 1} + SCR"))
        fuel.D = True
        for (x, nx) in ((596.7 + dx, -1), (663.3 + dx, 1)):
            decal((x, 694, 70), (nx, 0, 0), 34, 9, [(f"HRSG {k + 1}", .9, True, COPPER)], bg=None)
        fuel.D = False
    return n
