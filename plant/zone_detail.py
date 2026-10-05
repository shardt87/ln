"""Detail pass on the generic option zones (typical, not engineered):
- BESS yard: crushed-rock surfacing (as BESS yards are built) instead of a plain pad, containers on two
  concrete plinth beams each, a 2 ft spill / fire break kerb between container rows;
- modular yard T-MOD-1 / T-MOD-2: the 230 kV leads now leave the HV bushings through a take-off gantry in the
  reserved corridor and continue to the first H-MOD monopole (they ended at the bushings), arresters on the
  gantry, and a firewall between the two transformers."""
import fuel
from fuel import box, rod, find, on


def bess():
    yd = find("BESS yard")
    on(yd)
    fuel.D = True
    for p in fuel.G["parts"]:
        if p["item"] == yd["id"] and p["kind"] == "box" and p["color"] == "pad" and p["max"][2] < .1:
            p["color"] = "gravel"
    fuel.D = False
    for it in fuel.G["items"]:
        if it["name"] != "BESS container (ISO 40 ft high cube)":
            continue
        x0, x1, y0, y1 = it["fp"]
        on(it)
        fuel.D = True
        for yb in (y0 + .6, y1 - 1.8):                                       # plinth beams
            box(x0 - .5, x1 + .5, yb, yb + 1.2, 0, .5, "concrete")
        fuel.D = False


def tmod():
    on(find("T-MOD-1"))
    fw = fuel.new_item("OPT_MOD", "T-MOD-1 / T-MOD-2 firewall", (2093, 2097, 866, 909), (0, 38), area="I",
                       basis="typical", register=False, sheet="typical (zone detail)",
                       info="Concrete firewall between the two 13.8/230 kV transformers (NFPA 850).")
    box(2093, 2097, 866, 909, 0, 38, "concrete")
    g = fuel.new_item("OPT_MOD", "T-MOD 230 kV take-off gantry with arresters", (2055, 2135, 846, 856), (0, 46), area="I",
                      basis="typical", register=False, sheet="typical (zone detail)",
                      info="The 230 kV leads of T-MOD-1 / -2 rise to a take-off gantry with surge arresters and leave on "
                           "the H-MOD overhead tie (reserved corridor COR-HMOD).")
    for x in (2056, 2134):
        rod((x, 851, 0), (x, 851, 46), .8, "steel", r2=.55, seg=8)
        box(x - 1.5, x + 1.5, 849.5, 852.5, 0, .5, "concrete")
    box(2055, 2135, 850.2, 851.8, 43, 45, "steel")
    for k, ph in enumerate((-7, 0, 7)):
        y_b = 880.3 + 7.2 * k
        for xb in (2065, 2125):
            rod((xb, 851, 43), (xb, 851, 40.3), .3, "insulator", seg=6)            # strain string
            # jumper from the bushing top down to the gantry string, slight sag
            a, b = (xb, y_b, 37), (xb, 851, 40.3)
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, min(a[2], b[2]) - 1.5)
            pts = [tuple((1 - t) ** 2 * a[j] + 2 * (1 - t) * t * m[j] + t * t * b[j] for j in range(3)) for t in [i / 8 for i in range(9)]]
            for p_, q_ in zip(pts, pts[1:]):
                rod(p_, q_, .14, "conductor", seg=6)
        # bundle on to the first H-MOD pole (2095, 815): from the gantry centre line
        a, b = (2095 + ph, 851, 40.3), (2095 + ph, 815, 41)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 38.5)
        pts = [tuple((1 - t) ** 2 * a[j] + 2 * (1 - t) * t * m[j] + t * t * b[j] for j in range(3)) for t in [i / 10 for i in range(11)]]
        for p_, q_ in zip(pts, pts[1:]):
            rod(p_, q_, .2, "conductor", seg=6)
        for xb in (2065, 2125):                                                    # bus between the two strings
            rod((xb, 851, 40.3), (2095 + ph, 851, 40.3), .14, "conductor", seg=6)
    for x in (2068, 2122):                                                         # surge arresters on stands
        for k in range(3):
            y = 856 + 2 * k
            box(x - .4, x + .4, y - .4, y + .4, 0, 18, "steel")
            rod((x, y, 18), (x, y, 26), .45, "insulator", seg=8)


def build():
    bess()
    tmod()
