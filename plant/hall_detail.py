"""Turbine hall: detail on the equipment that still read as plain blocks at eye level (audit cameras A1-A4).

- lube-oil skids (GT1-3 aux, ST aux): reservoir with stiffener ribs, bolted manways and a vent on the lid, a
  level-gauge column, a lid handrail; the oil coolers as plate heat exchangers (frame, follower, plate pack, tie
  bars, nozzles) instead of a solid bundle;
- steam turbine LP casing: vertical stiffeners on all four faces, the horizontal-joint flange all round, insulation
  cladding seams, a nameplate;
- nameplates on each GT and generator.
Everything stays inside each item's footprint. All typical, not engineered.
"""
import fuel
from fuel import box, rod, find, on


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def lube_skid(name, x0, x1, y0, y1):
    it = find(name)
    on(it)
    fuel.D = True
    ra, rb = y0 + 1, y0 + 18                                                       # reservoir y span (z 20.8-26)
    for y in range(int(ra) + 2, int(rb), 3):                                       # stiffener ribs on both long sides
        for xs in (x0 + .5, x1 - .5):
            box(xs - .1, xs + .1, y - .12, y + .12, 20.8, 25.9, "steel")
    for (xm, ym) in ((x0 + 3.5, ra + 10), (x1 - 3.5, ra + 10)):                    # bolted manways on the lid
        rod((xm, ym, 26), (xm, ym, 26.25), 1.1, "steel", seg=18)
        rod((xm, ym, 26.25), (xm, ym, 26.35), .95, "machine", seg=18)
    rod(((x0 + x1) / 2 + 2, ra + 2.5, 26), ((x0 + x1) / 2 + 2, ra + 2.5, 28.4), .25, "steel", seg=8)  # vent
    rod(((x0 + x1) / 2 + 2, ra + 2.5, 28.4), ((x0 + x1) / 2 + 2, ra + 2.5, 28.9), .4, "steel", seg=10)
    box(x0 + .3, x0 + .5, ra + 6, ra + 6.4, 21.2, 25.6, "glass")                     # level gauge column
    for (a, b) in (((x0 + .6, ra + .2), (x1 - .6, ra + .2)), ((x1 - .6, ra + .2), (x1 - .6, rb - .2))):
        rod((a[0], a[1], 29.4), (b[0], b[1], 29.4), .06, "rail", seg=4)              # lid handrail
        rod((a[0], a[1], 27.7), (b[0], b[1], 27.7), .05, "rail", seg=4)
    for (px, py) in ((x0 + .6, ra + .2), (x1 - .6, ra + .2), (x1 - .6, rb - .2), (x1 - .6, (ra + rb) / 2)):
        rod((px, py, 26), (px, py, 29.4), .05, "rail", seg=4)
    decal(((x0 + x1) / 2, y0 + .9, 23.5), (0, -1, 0), 4.0, 1.2,
          [(name.split(":")[0] + " LUBE OIL", .35, True, None), ("ISO VG 32  ·  NO OPEN FLAME", .22, False, None)],
          bg="#ffffff")
    fuel.D = False
    # plate heat exchangers instead of the solid cooler bundle
    G = fuel.G
    G["parts"][:] = [p for p in G["parts"] if not (p["item"] == it["id"] and p["kind"] == "box" and p["color"] == "bundle")]
    on(it)
    fuel.D = True
    ca, cb = y0 + 24, y1 - 1
    for (xa, xb) in ((x0 + .7, (x0 + x1) / 2 - .4), ((x0 + x1) / 2 + .4, x1 - .7)):
        box(xa, xb, ca, ca + .7, 20.8, 28.3, "machine")                            # fixed frame plate
        box(xa, xb, cb - .6, cb, 20.8, 28.3, "machine")                            # follower
        box(xa + .25, xb - .25, ca + .7, cb - .6, 21.6, 27.6, "radiator")          # plate pack
        for zz in (27.9, 21.2):                                                     # carrying / guide bars
            rod(((xa + xb) / 2, ca + .3, zz), ((xa + xb) / 2, cb - .3, zz), .14, "steel", seg=8)
        for xt in (xa + .15, xb - .15):                                             # tie bars
            for zz in (21.6, 27.6):
                rod((xt, ca, zz), (xt, cb, zz), .07, "steel", seg=6)
        for zz in (22.4, 26.8):                                                     # nozzles on the fixed plate
            rod((xa + .9, ca, zz), (xa + .9, ca - .7, zz), .28, "amber" if zz < 24 else "cw", seg=10)
    fuel.D = False


def st_casing():
    it = find("ST: steam turbine")
    on(it)
    fuel.D = True
    for x in list(range(1031, 1044, 4)) + list(range(1057, 1072, 4)):                # lower-hood ribs, N / S faces
        for (ya, yb) in ((473.6, 474), (526, 526.4)):
            box(x - .3, x + .3, ya, yb, 21.5, 33, "steel")
    decal((1037.5, 473.55, 28), (0, -1, 0), 7, 1.8,
          [("STEAM TURBINE  HP-IP / LP", .34, True, None), ("ST-1  ·  3,600 RPM", .24, False, None)], bg="#e9ecef")
    fuel.D = False


def nameplates():
    for k in range(3):
        dx = 160 * k
        on(find(f"GT{k + 1}: H-class"))
        fuel.D = True
        decal((630 + dx, 454.9, 33.5), (0, -1, 0), 6, 1.6, [(f"GT-{k + 1}", .5, True, None),
              ("H-CLASS GAS TURBINE  ·  60 Hz", .24, False, None)], bg="#e9ecef")
        on(find(f"GTG-{k + 1}:"))
        decal((630 + dx + 7.05, 433, 28), (1, 0, 0), 5, 1.4, [(f"GTG-{k + 1}", .5, True, None),
              ("H2-COOLED GENERATOR", .26, False, None)], bg="#e9ecef")
        fuel.D = False


def build():
    for k in range(3):
        dx = 160 * k
        lube_skid(f"GT{k + 1} aux:", 661 + dx, 675 + dx, 470, 505)
    lube_skid("ST aux:", 1082, 1098, 470, 505)
    st_casing()
    nameplates()
    return 1
