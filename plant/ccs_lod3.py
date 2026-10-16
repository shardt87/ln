"""Carbon-capture area at LOD 3, the gas-yard standard, and a recognizable CCS identity on the absorbers.

- absorbers A-C: a painted green band round the shell between the EL 200 and EL 250 platforms with "CCS" lettered (muted sage band, dark grey-green letters, so the CCS stays secondary to the power block)
  on it four times round (clear of the ladder, the tray riser and the amine risers), "CARBON CAPTURE · ABSORBER x"
  under the lettering;
- surfaces: crushed stone over the CCS block (ring road to utilities road, west edge to the east spine road),
  a concrete drive north of the absorbers;
- equipment nameplates: DCC, booster fan, stripper, reboiler, CO2 compression, solvent storage;
- amine-area safety: combined safety shower / eyewash stations at each pump skid and the solvent storage
  (green, with blue light), corrosive / CO2 hazard signs, wheeled extinguishers;
- flood-light poles, operators (a sampling technician at each absorber sample panel), pickups.
Everything is placed only where clear of existing parts (gas_lod3.Space). All typical, not engineered.
"""
import math

import fuel
from fuel import box, rod, on, find

from gas_lod3 import Space, light_pole, extinguisher, pickup, person, decal

L = "OPT_CCS"
GREEN = "#5f8a6c"


def new(name, fp, z, info=""):
    it = fuel.new_item(L, name, fp, z, area="G", sheet="typical (carbon capture detail)", register=False, info=info)
    on(it)
    return it


BODY = {"tank", "duct", "rollup", "ehouse", "tower", "cabinet"}


def shells():
    """Colour identity (user review): every CCS equipment body (strippers, DCC / flue ducts, booster fans, reboilers,
    reclaimer, storage, carbon filter, compression and wastewater buildings, e-houses, dehydration, instrument air,
    cooling tower) in the absorbers' muted cladding, so the carbon capture reads as one family behind the power
    block; piping, structure, motors, pumps, exchangers and transformers keep their own finishes. The HRSG stacks take
    the HRSG casing colour so the combined-cycle block reads as one."""
    ids = {i["id"] for i in fuel.G["items"] if i["layer"] in ("OPT_CCS", "OPT_CCSU")}
    stacks = {i["id"] for i in fuel.G["items"] if i["name"] in ("HRSG 1 stack", "HRSG 2 stack", "HRSG 3 stack")}
    for p in fuel.G["parts"]:
        if p["item"] in ids and p["color"] in BODY:
            p["color"] = "ccs"
        elif p["item"] in stacks and p["color"] == "stack":
            p["color"] = "hrsg"


def absorber_identity():
    for i, dx in enumerate((0, 160, 320)):
        t = "ABC"[i]
        gx, cy, R = 630 + dx, 1220.0, 31.0
        on(find(f"Absorber {t} ("))
        fuel.D = True
        rod((gx, cy, 207), (gx, cy, 243), R + .08, "ccs_green", seg=64)              # painted band
        for zb in (207, 243):                                                        # white pinstripes
            rod((gx, cy, zb - .6), (gx, cy, zb), R + .09, "steel", seg=64)
        for a in (0, 90, 180, -90):                                                  # lettering, four faces (clear of ladder / riser)
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            Rp = R + .25
            decal((gx + Rp * ca, cy + Rp * sa, 227.5), (ca, sa, 0), 24, 20,
                  [("CCS", .85, True, "#3d5c47")], bg=None)
            decal((gx + Rp * ca, cy + Rp * sa, 212.4), (ca, sa, 0), 22, 2.8,
                  [(f"CARBON CAPTURE  ·  ABSORBER {t}", .7, True, "#3d5c47")], bg=None)
        fuel.D = False


def surfaces():
    new("CCS area: crushed-stone surface and concrete drive", (545, 1458, 932, 1368), (0, .2),
        "Crushed stone over the carbon-capture block; concrete drive north of the absorbers for maintenance access.")
    box(545, 1458, 932, 1368, 0, .08, "gravel_yard")
    box(545, 1205, 1292, 1306, .08, .16, "road")


def nameplates():
    plates = [
        ("DCC-{t}:", lambda dx: ((553.7 + dx, 1022, 60), (-1, 0, 0)), "DCC-{t}", "DIRECT-CONTACT COOLER"),
        ("BF-{t}:", lambda dx: ((630 + dx, 984.85, 36), (0, -1, 0)), "BF-{t}", "FLUE-GAS BOOSTER FAN  ·  16 MW"),
    ]
    for i, dx in enumerate((0, 160, 320)):
        t = "ABC"[i]
        for (nm, pos, title, sub) in plates:
            on(find(nm.format(t=t)))
            fuel.D = True
            c, n = pos(dx)
            decal(c, n, 9, 2.2, [(title.format(t=t), .42, True, None), (sub, .24, False, None)], bg="#ffffff")
            fuel.D = False
    # DCC insulation-cladding bands (as on the absorbers)
    for i, dx in enumerate((0, 160, 320)):
        on(find(f"DCC-{'ABC'[i]}:"))
        fuel.D = True
        for z in (14, 28, 42, 56, 70):
            rod((584 + dx, 1022, z - .25), (584 + dx, 1022, z + .25), 30.15, "steel", seg=64)
        fuel.D = False
    for (nm, c, n, w, title, sub) in (
            ("STR-A:", (1070, 1164.6, 30), (0, -1, 0), 9, "STR-A", "CO2 STRIPPER"),
            ("STR-B:", (1120, 1164.6, 30), (0, -1, 0), 9, "STR-B", "CO2 STRIPPER"),
            ("STR-C:", (1170, 1164.6, 30), (0, -1, 0), 9, "STR-C", "CO2 STRIPPER"),
            ("CO2 compression", (1372, 1229.85, 26), (0, -1, 0), 16, "CO2 COMPRESSION", "3 x 19 MW  ·  DEHYDRATION"),
            ("Solvent + NaOH storage", (1228, 1173.8, 22), (0, -1, 0), 10, "AMINE SOLVENT + NaOH",
             "CORROSIVE  ·  BUNDED")):
        on(find(nm))
        fuel.D = True
        decal(c, n, w, 2.2, [(title, .42, True, None), (sub, .24, False, None)], bg="#ffffff")
        fuel.D = False


def shower(S, x, y):
    """Combined safety shower / eyewash on its own pad: green frame, shower head, eyewash bowl, blue beacon."""
    p = S.place(x, y, 1.6, 1.6, 9)
    if not p:
        return False
    x, y = p
    box(x - 1.6, x + 1.6, y - 1.6, y + 1.6, 0, .3, "concrete")
    box(x - 1.4, x + 1.4, y - 1.4, y + 1.4, .3, .35, "grating")
    rod((x, y + 1, .35), (x, y + 1, 8.2), .14, "ccs_green", seg=8)                  # supply riser
    rod((x, y + 1, 8.2), (x, y, 8.2), .1, "ccs_green", seg=6)
    rod((x, y, 7.9), (x, y, 8.15), .55, "ccs_green", r2=.2, seg=12)                 # shower head
    rod((x, y + 1, 3.6), (x, y + .2, 3.6), .08, "ccs_green", seg=6)
    rod((x, y + .2, 3.4), (x, y + .2, 3.7), .55, "label", r2=.3, seg=12)            # eyewash bowl
    rod((x, y + 1, 8.2), (x, y + 1, 9.0), .2, "pvc_blue", seg=10)                   # beacon
    decal((x, y + 1.2, 6.3), (0, -1, 0), 1.6, 1.2, [("SAFETY", .3, True, "#ffffff"), ("SHOWER", .3, True, "#ffffff")],
          bg=GREEN)
    return True


def safety(S):
    new("CCS area: safety showers / eyewashes, hazard signs, flood lights, extinguishers (typical)",
        (545, 1458, 932, 1368), (0, 31),
        "Amine (MEA-class) solvent areas: combined safety shower / eyewash within 10 s of every pump skid and the "
        "solvent storage (ANSI Z358.1); corrosive and CO2 asphyxiation signage; explosion-proof floods.")
    fuel.D = True
    n = 0
    for dx in (0, 160, 320):
        for (x, y) in ((655 + dx, 1068), (708 + dx, 1170), (563 + dx, 1078)):
            n += shower(S, x, y)
    for (x, y) in ((1205, 1190), (1305, 1250), (1200, 1128)):
        n += shower(S, x, y)
    for (x, y) in ((560, 960), (720, 960), (880, 960), (1040, 960), (1200, 960), (1440, 1100),
                   (1440, 1300), (560, 1285), (720, 1285), (880, 1285), (1040, 1285), (1200, 1285),
                   (720, 1150), (880, 1150), (1300, 1080)):
        light_pole(S, x, y, h=30)
    for (x, y) in ((712, 1070), (872, 1070), (1032, 1070), (1205, 1210), (1440, 1240)):
        extinguisher(S, x, y)
    for dx in (0, 160, 320):                                                        # amine hazard signs at the skids
        p = S.place(682.5 + dx, 1037.5, 2.0, .3, 8)
        if not p:
            continue
        sx, sy = p
        for ox in (-1.8, 1.8):
            rod((sx + ox, sy + .1, 0), (sx + ox, sy + .1, 7.6), .07, "steel", seg=6)
        decal((sx, sy, 6), (0, -1, 0), 5, 2.8,
              [("DANGER", .22, True, "#ffffff", False, "#c8102e"), ("AMINE SOLVENT", .2, True, None),
               ("CORROSIVE  ·  WEAR FACE SHIELD", .13, True, None), ("SAFETY SHOWER NEARBY", .12, False, None)],
              bg="#ffffff")
    decal((1372, 1229.6, 8), (0, -1, 0), 6, 3,
          [("WARNING", .22, True, "#000000", False, "#ffd200"), ("CO2  ·  ASPHYXIANT", .2, True, None),
           ("PORTABLE CO2 MONITOR REQUIRED", .14, True, None)], bg="#ffffff")
    fuel.D = False
    print("ccs_lod3: safety showers", n)


def people(S):
    new("CCS area: operators and vehicles", (545, 1458, 932, 1368), (0, 8))
    for dx in (0, 160, 320):                                                        # sampling at each absorber
        p = S.place(654 + dx, 1177.5, .8, .8, 6)
        if p:
            person(p[0], p[1], .08, 1.57, vest="hivis")
    for (x, y, a, v) in ((690, 1102, 3.14, "hivis_o"), (850, 1104, 0, "hivis"), (1100, 1158, 1.57, "hivis"),
                         (1330, 1226, 3.14, "hivis_o"), (1240, 1160, 0, "hivis")):
        p = S.place(x, y, .8, .8, 6)
        if p:
            person(p[0], p[1], .08, a, vest=v)
    pickup(S, 760, 1299)
    pickup(S, 1010, 1299)
    pickup(S, 1350, 1100, along_x=False)


def build():
    shells()
    absorber_identity()
    surfaces()
    nameplates()
    S = Space()
    safety(S)
    people(S)
    return 1
