"""BFP-1B at LOD 3 with kit 2 being landed (owner, Oct 26): the boiler feed pump motors are the flagship for the
pump-skid motor-lead kit (six identical ~5 MW, 13.8 kV direct-on-line motors). On BFP-1B (x 680-692, y 648):
- the motor: ribbed frame, end shields, feet on the baseplate, fan cowl at the non-drive end, lifting eyes, a
  nameplate, an RTD / space-heater auxiliary box on the frame;
- the MV terminal box opened (cover off, leaning on the plinth): three motor lead studs on stand-off insulators, the
  three pre-terminated MV-105 leads of the kit dropping through the top gland plate, each with its cold-shrink
  termination, phase tape and compression lug bolted to its stud, shield drains to a ground bar;
- the kit's instrument harness plugged into the RTD box (one multi-pin connector, no terminations), the trunk up to
  the ladder tray;
- an electrician at the open box torquing the lugs, the emptied kit crate on the slab with its tag, a lock-out
  tag on the breaker-side warning plate.
Typical, not engineered. Runs after hrsg_electrical (which built the closed terminal boxes)."""
import math

import fuel
from fuel import box, rod, find, new_item, on

TAPE = ("red", "amber", "cable_inst")                       # phases A / B / C
X0, X1, YB0, YB1 = 683.0, 686.6, 642.4, 644.8               # BFP-1B terminal box (hrsg_electrical)
YM = 648.0                                                  # motor axis (y), EL 6
LEADS_X = (684.0, 684.4, 684.8)                             # the three drops (hrsg_electrical)


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def person(x, y, z, a, vest="hivis"):
    import maintenance
    maintenance.person(x, y, z, a, vest=vest)


def strip_closed_box():
    """Remove BFP-1B's closed terminal box, its gland plate and its label (rebuilt open here)."""
    it = find("BFP-1A/B")
    G = fuel.G
    G["parts"][:] = [p for p in G["parts"] if not (p["item"] == it["id"] and p["kind"] == "box" and (
        (p["color"] == "motor" and p["min"][:2] == [X0, YB0]) or (p["color"] == "steel" and p["min"][:2] == [X0 + .3, YB0 + .2])))]
    G["decals"][:] = [d for d in G.get("decals", []) if not (d["item"] == it["id"] and abs(d["c"][0] - 686.65) < .01
                                                            and abs(d["c"][1] - (YB0 + YB1) / 2) < .01)]


def motor_detail():
    for k in range(9):                                                                 # cooling ribs
        x = 680.6 + k * 1.3
        rod((x, YM, 6.0), (x + .25, YM, 6.0), 3.35, "motor", seg=24)
    for x in (680.0, 692.0):                                                           # end shields
        rod((x - .2, YM, 6.0), (x + .2, YM, 6.0), 3.0, "steel_dark", seg=24)
    rod((678.4, YM, 6.0), (680.0, YM, 6.0), 2.6, "motor", r2=2.9, seg=24)            # fan cowl (non-drive end)
    for sy in (-2.4, 2.4):                                                             # feet
        box(681.0, 691.0, YM + sy - .5, YM + sy + .5, 3.0, 3.5, "motor")
    for x in (682.0, 690.0):                                                           # lifting eyes
        rod((x, YM, 9.2), (x, YM, 9.9), .25, "steel", seg=10)
    box(688.0, 691.2, YM - 3.4, YM - 3.3, 5.0, 6.8, "steel")                          # nameplate
    decal((689.6, YM - 3.42, 5.9), (0, -1, 0), 3.0, 1.6, [("BFP-1B MOTOR", .22, 1, "#111111"), ("5,000 kW · 13,800 V", .18, 0, "#222222"),
                                                         ("3,580 rpm · DOL · 60 Hz", .16, 0, "#222222")], bg="#d9dcdf")
    box(688.6, 690.2, YM + 2.9, YM + 3.5, 6.6, 8.0, "steel")                          # RTD / heater aux box
    return 1


def open_box():
    box(X0, X1, YB1, YB1 + .12, 4.2, 8.2, "motor")                                     # back (motor side)
    for xs in (X0, X1 - .12):
        box(xs, xs + .12, YB0, YB1, 4.2, 8.2, "motor")                                 # sides
    box(X0, X1, YB0, YB1, 4.2, 4.35, "motor")                                          # bottom
    box(X0 + .3, X1 - .3, YB0 + .2, YB1 - .2, 8.2, 8.5, "steel")                      # gland plate (top, cables in)
    box(X0 + .2, X1 - .2, YB0 - 1.4, YB0 - 1.25, 1.0, 4.8, "motor")                    # the cover, leaning on the plinth
    for k, x in enumerate((683.9, 684.8, 685.7)):                                      # motor lead studs on insulators
        rod((x, YB1 - .1, 5.2), (x, YB1 - .9, 5.2), .22, "insulator", seg=12)
        rod((x, YB1 - .9, 5.2), (x, YB1 - 1.2, 5.2), .08, "copper", seg=8)
    box(X0 + .3, X1 - .3, YB0 + .2, YB0 + .35, 4.5, 4.7, "copper")                      # ground bar
    return 1


def kit_leads():
    """The pre-terminated leads: down through the gland plate, cold-shrink body, lug onto each stud."""
    for k, (xl, xs) in enumerate(zip(LEADS_X, (683.9, 684.8, 685.7))):
        yl = (YB0 + YB1) / 2
        rod((xl, yl, 8.5), (xl, yl, 7.9), .26, "cable_mv", seg=10)                      # through the gland
        rod((xl, yl, 7.9), (xs, yl, 7.4), .1, "cable_mv", seg=8)                         # cable (jacket off below)
        rod((xs, yl, 7.4), (xs, yl, 7.2), .11, TAPE[k], seg=10)                          # phase tape
        rod((xs, yl, 7.2), (xs, yl, 6.0), .12, "hdpe", seg=10)                           # cold-shrink body
        for j in range(3):
            rod((xs, yl, 6.3 + j * .28), (xs, yl, 6.35 + j * .28), .2, "hdpe", seg=12)   # sheds
        rod((xs, yl, 6.0), (xs, yl, 5.5), .07, "copper", seg=8)                          # lug barrel
        rod((xs, yl, 5.5), (xs, YB1 - 1.2, 5.2), .06, "copper", seg=6)                   # lug palm on the stud
        rod((xs, yl, 7.1), (xs + .2, YB0 + .3, 4.7), .03, "copper", seg=4)              # shield drain to the bar
        box(xs - .1, xs + .1, yl - .2, yl - .12, 7.45, 7.75, "white_truck")               # kit tag (factory)
    return 1


def harness():
    """Instrument harness: one multi-pin plug into the RTD box, the trunk up to the tray."""
    pts = [(689.4, YM + 3.5, 8.0), (689.4, YM + 3.9, 9.8), (689.4, 641.8, 9.8), (686.0, 641.8, 9.6)]
    for a, b in zip(pts, pts[1:]):
        rod(a, b, .11, "cable_inst", seg=8)
    rod((689.4, YM + 3.5, 8.0), (689.4, YM + 3.5, 8.25), .2, "sp_black", seg=10)        # connector, plugged
    return 1


def crew_and_crate():
    # the electrician on the slab at the open box, torquing the lugs
    person(684.8, 640.4, 1.0, math.pi / 2, vest="hivis_o")
    # the emptied kit crate on the slab
    cx, cy = 695.5, 657.0
    box(cx - 2.2, cx + 2.2, cy - 1.6, cy + 1.6, 1.0, 1.4, "timber")
    for (a0, a1, b0, b1) in ((-2.2, 2.2, -1.6, -1.4), (-2.2, 2.2, 1.4, 1.6), (-2.2, -2.0, -1.6, 1.6), (2.0, 2.2, -1.6, 1.6)):
        box(cx + a0, cx + a1, cy + b0, cy + b1, 1.4, 3.0, "timber")
    lines = [("KIT 2  ·  MOTOR LEADS  ·  BFP-1B", .22, 1, "#111111"), ("3 x MV-105 250 kcmil · pre-terminated", .16, 0, "#333333"),
             ("+ instrument harness · tested", .15, 1, "#2f7a3c")]
    decal((cx, cy - 1.65, 2.2), (0, -1, 0), 4.0, 1.4, [("SOUTHWIRE", .18, 1, "#b4591f", 1)] + lines, bg="#ffffff", brand=True)
    decal((cx, cy - 1.65, 2.2), (0, -1, 0), 4.0, 1.4, lines, bg="#ffffff", generic_only=True)
    # lock-out tag on the box side
    box(X1, X1 + .05, YB0 + .4, YB0 + .9, 6.6, 7.4, "red")
    decal((X1 + .06, YB0 + 1.6, 7.4), (1, 0, 0), 1.6, .8, [("LOCKED OUT", .32, 1, "#ffffff"), ("SWGR-13.8-1 BKR", .22, 0, "#ffffff")], bg="#b3261e")
    return 1


def build():
    strip_closed_box()
    it = new_item("BASE_ELECTRICAL", "BFP-1B motor at LOD 3: terminal box opened, kit 2 pre-terminated leads landed, instrument harness",
                  [677.5, 698.0, 640.5, 659.0], [1.0, 10.0], area="A", register=False,
                  info="Boiler feed pump BFP-1B (~5 MW, 13.8 kV, DOL): ribbed motor frame, fan cowl, feet, nameplate, RTD box; "
                       "the MV terminal box opened on three pre-terminated MV-105 leads from kit 2 (cold-shrink terminations, "
                       "phase tape, lugs on the motor studs, shield drains to the ground bar); the instrument harness on one "
                       "plug; an electrician torquing the lugs, the emptied kit crate, lock-out tag. Typical, not engineered.")
    on(it)
    fuel.D = True
    n = motor_detail() + open_box() + kit_leads() + harness() + crew_and_crate()
    fuel.D = False
    return n
