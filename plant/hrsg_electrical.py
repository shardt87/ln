"""HRSG electrical showcase (owner, Oct 22: the boiler section, greenfield HRSGs as Vogt Power / B&W build them). The
HRSGs already carry the drum-level transmitters, roof MOVs, AIG and dilution-air skid, the EL 42 control tray and its
riser (hrsg.py). Added on each of HRSG 1-3, all typical, not engineered:
- duct burner (supplementary firing, in the HP superheater cavity, at y 636 clear of the feedwater line entering at y 640): a vertical gas header
  up the east wall in the slot between the casing and the galleries, eight burner runners each with a flex hose, an
  igniter and a flame scanner, their cables down a small ladder to a burner junction box; a duct-burner fuel skid at
  grade north of the chemical-feed skid (manual isolation, two safety shut-off valves with the vent valve between,
  flow control valve, vent line up) and its BMS panel; ARMOR-X MC-HL exposed on strut from the panel to the skid
  (Class I Div 2) and the scanner / igniter multicable along grade to the panel;
- boiler feed pumps: the 13.8 kV cables that stopped at the drop's end glands (EL 10.3) over the pumps now land on a short ladder tray and
  into an MV terminal box on each motor (3 x 1/C each), with a ground bond.
Runs late (after the trays are rendered)."""
import fuel
from fuel import box, rod, find, on, new_item


def poly(pts, r, c, seg=8):
    for a, b in zip(pts, pts[1:]):
        rod(a, b, r, c, seg=seg)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def duct_burner(k, dx):
    it = new_item("BASE_POWER_BLOCK", f"HRSG {k + 1} duct burner: gas header, runners, fuel skid and BMS panel",
                  [663.8 + dx, 693.2 + dx, 634, 703], [0, 80], area="A", register=False, sheet="typical (HRSG detail)",
                  info="Supplementary firing in the HP superheater cavity: eight burner runners off a vertical gas header on "
                       "the east wall, each with igniter and flame scanner; duct-burner fuel skid (double block and bleed, "
                       "flow control) and BMS panel at grade; MC-HL to the skid valves (Class I Div 2), scanner / igniter "
                       "multicable to the panel. Typical, not engineered.")
    on(it)
    fuel.D = True
    HX, HY = 664.6 + dx, 636.0                                                       # header, in the casing / gallery slot
    rod((HX, HY, 5.5), (HX, HY, 78.0), .35, "fuelgas", seg=10)
    zr = [12.0 + 9.0 * j for j in range(8)]                                          # runner elevations
    for z in zr:
        rod((HX, HY, z), (663.85 + dx, HY, z), .14, "steel", seg=6)                  # flex hose to the runner
        box(663.8 + dx, 664.2 + dx, HY - .55, HY + .55, z - .55, z + .55, "steel_dark")   # runner flange
        rod((663.85 + dx, HY - 1.1, z + .5), (664.75 + dx, HY - 1.1, z + .5), .14, "steel", seg=8)   # igniter
        rod((663.85 + dx, HY - 1.1, z - .5), (664.75 + dx, HY - 1.1, z - .5), .17, "steel_dark", seg=8)  # flame scanner
        rod((664.75 + dx, HY - 1.1, z + .5), (664.85 + dx, HY - 2.2, z + .5), .04, "cable_inst", seg=4)
        rod((664.75 + dx, HY - 1.1, z - .5), (664.85 + dx, HY - 2.2, z - .5), .04, "cable_inst", seg=4)
    # small cable ladder down the wall beside the runners, to the burner junction box
    CY = HY - 2.4
    for s in (-.3, .3):
        box(664.55 + dx, 664.75 + dx, CY + s - .04, CY + s + .04, 9.5, 77.0, "pipe")
    z = 10.0
    while z < 77:
        box(664.55 + dx, 664.75 + dx, CY - .3, CY + .3, z - .04, z + .04, "pipe")
        z += 2.0
    for j in range(4):
        rod((664.65 + dx, CY - .2 + j * .13, 9.5), (664.65 + dx, CY - .2 + j * .13, 77.0), .05, "cable_inst", seg=4)
    box(663.8 + dx, 664.9 + dx, CY - 1.0, CY + 1.0, 6.0, 9.5, "panel")                 # burner junction box
    decal((664.92 + dx, CY, 8.9), (1, 0, 0), 1.8, .38, [(f"DB-{k + 1} JB", .6, True, "#111111")], bg="#ffffff")
    # fuel skid at grade north of the chemical-feed skid
    SX0, SX1, SY0, SY1 = 676.2 + dx, 690.0 + dx, 689.7, 700.9
    GY = 695.3
    box(SX0, SX1, SY0, SY1, 0, .6, "concrete")
    box(SX0 + .5, SX1 - .5, GY - 2.0, GY + 2.0, .6, 1.2, "steel_dark")
    poly([(SX1 - 1.0, GY, 0.0), (SX1 - 1.0, GY, 4.0), (SX0 + 1.0, GY, 4.0), (SX0 + 1.0, GY, 5.5), (HX, GY, 5.5),
          (HX, HY, 5.5)], .3, "fuelgas", seg=10)
    for xv, kind in ((SX1 - 3.0, "man"), (SX1 - 5.5, "ssov"), (SX1 - 7.7, "vent"), (SX1 - 9.9, "ssov"),
                     (SX1 - 12.2, "fcv")):
        if kind == "man":
            rod((xv - .4, GY, 4.0), (xv + .4, GY, 4.0), .5, "steel", seg=10)
            rod((xv, GY - .5, 5.0), (xv, GY + .5, 5.0), .05, "red", seg=6)
        elif kind == "ssov":
            rod((xv - .5, GY, 4.0), (xv + .5, GY, 4.0), .6, "steel", seg=12)
            box(xv - .45, xv + .45, GY - .45, GY + .45, 4.6, 6.1, "red")
        elif kind == "fcv":
            rod((xv - .5, GY, 4.0), (xv + .5, GY, 4.0), .6, "steel", seg=12)
            rod((xv, GY, 4.6), (xv, GY, 5.8), .75, "amber", r2=.4, seg=12)            # flow control valve actuator
        else:
            box(xv - .35, xv + .35, GY - .35, GY + .35, 4.4, 5.4, "amber")
            poly([(xv, GY, 5.4), (xv, GY + 2.5, 5.4), (xv, GY + 2.5, 30.0)], .18, "fuelgas", seg=8)   # vent line
    for xp in (SX0 + 2.0, SX1 - 2.0):
        rod((xp, GY, 1.2), (xp, GY, 3.7), .12, "steel", seg=6)
    for yy in (650.0, 665.0, 680.0):                                                 # pipe / cable stands along grade
        rod((HX + .2, yy, 1.6), (HX + .2, yy, 5.1), .1, "steel", seg=6)
        box(HX - .3, HX + .7, yy - .15, yy + .15, 5.0, 5.15, "steel")
    # BMS panel and its cables
    PX0, PX1, PY0, PY1 = SX1 + .5, SX1 + 3.0, 690.0, 695.5
    box(PX0, PX1, PY0, PY1, .6, 8.0, "cabinet")
    box(PX1, PX1 + .06, PY0 + .4, PY1 - .4, 1.2, 7.6, "door")
    box(PX1 + .03, PX1 + .1, PY0 + 1.4, PY1 - 1.4, 5.3, 6.6, "hmi")
    rod((PX1 + .05, PY1 - .9, 4.2), (PX1 + .3, PY1 - .9, 4.2), .2, "red", seg=10)
    decal((PX1 + .14, (PY0 + PY1) / 2, 7.4), (1, 0, 0), 3.4, .55, [(f"DB-{k + 1}  BMS", .6, True, "#111111")], bg="#ffffff")
    box(SX0 + 1.0, PX0, GY - 2.6, GY - 2.3, 2.4, 2.6, "steel")                     # strut along the skid
    for dz in (0, .3):
        poly([(PX0, PY0 + .8, 1.6 + dz), (PX0 - .4, PY0 + .8, 1.6 + dz), (PX0 - .4, GY - 2.45, 2.75 + dz),
              (SX0 + 3.0, GY - 2.45, 2.75 + dz)], .1, "cable_armor", seg=8)          # MC-HL to the valves
    for xv in (SX1 - 5.5, SX1 - 7.7, SX1 - 9.9, SX1 - 12.2):
        poly([(xv, GY - 2.45, 2.9), (xv, GY - .6, 2.9), (xv, GY - .6, 4.6)], .07, "cable_armor", seg=6)
    poly([(664.85 + dx, CY, 6.0), (665.15 + dx, CY, 4.6), (665.15 + dx, 692.5, 4.6), (PX0 - .3, 692.5, 4.6),
          (PX0 - .3, 692.5, 1.0)], .1, "cable_inst", seg=6)                            # scanner / igniter multicable  # scanner multicable
    decal((SX1 - 7.0, SY0 - .02, 2.2), (0, -1, 0), 4.6, .9, [(f"DUCT BURNER DB-{k + 1}  ·  NATURAL GAS", .55, True, "#ffffff")],
          bg="#b8322a")
    fuel.D = False
    return 80


def bfp_terminations(k, dx):
    on(find(f"BFP-{k + 1}A/B"))
    fuel.D = True
    # short ladder tray under the drop (x 674, y 639-641, EL 10.8) east over the two motors
    TZ = 10.0                                                                       # below the drop's end glands (EL 10.3)
    for s in (-1, 1):
        box(674.0 + dx, 686.0 + dx, 640.0 + s * 1.5 - .06, 640.0 + s * 1.5 + .06, TZ - .45, TZ - .05, "pipe")
    for x in range(674, 686, 2):
        box(x + dx - .05, x + dx + .05, 638.5, 641.5, TZ - .42, TZ - .36, "pipe")
    for xp in (676.0, 685.0):
        rod((xp + dx, 638.3, 1.0), (xp + dx, 638.3, TZ - .45), .12, "steel", seg=6)
        box(xp + dx - .15, xp + dx + .15, 638.3, 641.7, TZ - .6, TZ - .45, "steel")
    for m, (ym, yb0, yb1, ys) in enumerate(((626.0, 629.2, 631.6, 639.0), (648.0, 642.4, 644.8, 641.0))):
        box(683.0 + dx, 686.6 + dx, yb0, yb1, 4.2, 8.2, "motor")                       # MV terminal box
        box(683.3 + dx, 686.3 + dx, yb0 + .2, yb1 - .2, 8.2, 8.5, "steel")             # gland plate
        yb = (yb0 + yb1) / 2
        for j in range(3):
            yj = ys - .35 + j * .35 if m == 0 else ys - .35 + j * .35
            poly([(674.0 + dx, yj, 10.3), (674.0 + dx, yj, TZ - .3), (684.0 + dx + j * .4, yj, TZ - .3),
                  (684.0 + dx + j * .4, yb, TZ - .3), (684.0 + dx + j * .4, yb, 8.5)], .26, "cable_mv", seg=8)
        rod((686.6 + dx, yb, 4.6), (687.6 + dx, yb, 1.0), .06, "conductor", seg=4)    # ground bond
        decal((686.65 + dx, yb, 7.6), (1, 0, 0), 2.2, .45, [(f"BFP-{k + 1}{'AB'[m]}  13.8 kV", .6, True, "#111111")],
              bg="#ffd200")
    fuel.D = False
    return 30


def build():
    n = 0
    for k in range(3):
        dx = 160 * k
        n += duct_burner(k, dx)
        n += bfp_terminations(k, dx)
    return n
