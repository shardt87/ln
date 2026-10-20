"""Zone 07 part 2: the main gate security checkpoint at LOD 3, detailed so every wire can be pointed out (owner,
Oct 20). The checkpoint sits on the 30 ft access road (y 270-300) at x 255-300, the gatehouse north of it:
- curbed islands at both lane edges carrying the access-control devices: card reader (existing), call-box intercom,
  licence-plate (LPR) camera pole, stop sign, a red / green signal on each barrier arm post;
- saw-cut vehicle-detector loops in each lane, an arming loop before the barrier and a closing loop past the speed
  table, their lead-in saw cuts running to the island pull box;
- the wiring shown where it can be seen: conduit stub-ups and liquidtight whips into every device, a pull box on the
  outbound island with its lid off and the cables in it (120 V power, Cat 6A + access-control composite, twisted loop
  lead-ins, single-mode fibre), a cable ID placard beside it; buried duct banks gatehouse -> islands (services.py);
- the gatehouse opened up: windows on every face (the guard sees both lanes), an exterior panelboard and AC
  disconnect with conduit to grade, lights under the canopy, a SECURITY sign on the canopy fascia, a CCTV pole;
- the sliding gate at the west fence: operator with its conduit, photo-eye safety posts across the opening.
Typical, not engineered."""
import fuel
from fuel import box, rod, new_item, on


def decal(*a, **k):
    import showcase
    showcase.decal(*a, **k)


def stub(x, y, z0, z1, r=.12, c="pvc_grey"):
    """A conduit stub-up from below grade into a device base."""
    rod((x, y, z0 - .3), (x, y, z1), r, c, seg=8)
    return 1


def whip(a, b, r=.09):
    """Liquidtight flexible whip from a stub-up into a device."""
    rod(a, b, r, "hero_rail", seg=8)
    return 1


def loop(x0, x1, y0, y1, lead):
    """Saw-cut detector loop in the pavement, with its lead-in saw cut to the island."""
    w, z0, z1 = .22, .27, .285
    for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + w), (x0, x1, y1 - w, y1), (x0, x0 + w, y0, y1), (x1 - w, x1, y0, y1)):
        box(a0, a1, b0, b1, z0, z1, "hero_rail")
    (lx, ly0, ly1) = lead
    box(lx - w / 2, lx + w / 2, min(ly0, ly1), max(ly0, ly1), z0, z1, "hero_rail")
    return 5


def island(y0, y1, inbound):
    """Curbed island at a lane edge with its devices; returns the pull-box centre."""
    n = 0
    box(257.5, 271.5, y0, y1, .27, .8, "concrete")
    nose = (257.5, 258.3)
    box(nose[0], nose[1], y0, y1, .8, .82, "amber")                                     # painted nose
    ym = (y0 + y1) / 2
    yd = y1 - 1.2 if inbound else y0 + 1.2                                             # device line, lane side
    # call-box intercom on a gooseneck pedestal beside the card reader
    rod((260.4, yd, .8), (260.4, yd, 4.2), .14, "steel", seg=8)
    box(260.0, 260.8, yd - .35, yd + .35, 4.2, 5.4, "panel")
    n += 2 + stub(260.4, yd + (.4 if inbound else -.4), .8, 1.3) + whip((260.4, yd + (.4 if inbound else -.4), 1.3),
                                                                         (260.4, yd, 1.6))
    # card reader (existing pedestal at x 262-263): its stub and whip
    n += stub(262.5, yd + (.5 if inbound else -.5), .8, 1.3) + whip((262.5, yd + (.5 if inbound else -.5), 1.3),
                                                                     (262.5, yd + (.25 if inbound else -.25), 1.8))
    # barrier operator (existing cabinet x 268-269.6): stub and whip, a red / green signal on top
    n += stub(267.6, yd + (.3 if inbound else -.3), .8, 1.4) + whip((267.6, yd + (.3 if inbound else -.3), 1.4),
                                                                     (268.0, yd, 1.9))
    box(268.3, 269.3, yd - .3, yd + .3, 3.6, 5.6, "hero_rail")
    rod((268.2, yd, 5.05), (268.1, yd, 5.05), .28, "red", seg=10)
    rod((268.2, yd, 4.2), (268.1, yd, 4.2), .28, "safety", seg=10)
    n += 3
    # LPR camera pole at the island nose, aimed at the approaching plate
    rod((258.9, ym, .8), (258.9, ym, 10.5), .2, "steel", seg=8)
    box(257.6, 258.9, ym - .3, ym + .3, 9.8, 10.5, "machine")
    n += 2 + stub(259.3, ym, .8, 1.6) + whip((259.3, ym, 1.6), (258.95, ym, 2.4))
    # stop sign facing the approach
    rod((258.2, yd, .8), (258.2, yd, 7.2), .07, "steel", seg=6)
    n += 1
    decal((258.1, yd, 6.6), (-1, 0, 0), 1.9, 1.9, [("STOP", .42, 1, "#ffffff")], bg="#b3261e")
    # island pull box between the devices
    px = 265.0
    box(px - 1.0, px + 1.0, ym - .9, ym + .9, .3, .82, "concrete")
    n += 1
    return n, (px, ym)


def open_pullbox(px, py):
    """The outbound island's pull box with its lid off: the cables in it, a cable ID placard beside it."""
    n = 0
    box(px - .8, px + .8, py - .7, py + .7, .35, .83, "hero_rail")                         # the open box (dark inside)
    box(px + 1.1, px + 2.7, py - .7, py + .7, .82, .9, "steel")                             # lid set down beside it
    cabs = (("cable_tc", "120 V"), ("cable_inst", "CAT 6A"), ("cable_mc", "LOOPS"), ("cable_fo", "FIBRE"))
    for k, (c, _) in enumerate(cabs):
        y = py - .45 + k * .3
        rod((px - .7, y, .6), (px + .7, y, .6), .08, c, seg=8)                              # cables across the box
        rod((px - .3 + k * .15, y, .62), (px - .3 + k * .15, y, .95), .09, c, seg=8)        # coiled slack loops
        n += 2
    rod((px - 1.7, py - .6, .8), (px - 1.7, py - .6, 3.8), .06, "steel", seg=6)       # placard stake, beside the box
    decal((px - 1.7, py - .67, 3.0), (0, -1, 0), 3.2, 1.7,
          [("PULL BOX PB-G2  ·  ACCESS CONTROL", .17, 1, "#111111"),
           ("POWER 120 V  ·  12 AWG THHN/THWN-2", .14, 0, "#222222"),
           ("READER / INTERCOM  ·  CAT 6A + 18/6 COMPOSITE", .14, 0, "#26467a"),
           ("LOOP LEAD-IN  ·  14 AWG TWISTED PAIR", .14, 0, "#222222"),
           ("LPR / CCTV  ·  SINGLE-MODE FIBRE", .14, 0, "#b5651d")], bg="#ffffff")
    return n + 1


def gatehouse():
    n = 0
    # windows on the west (approach), east and north faces, a band at desk height
    for (x0, x1, y0, y1) in ((276.84, 277.0, 308.0, 322.0), (300.0, 300.16, 308.0, 314.0), (280.0, 297.0, 325.0, 325.16)):
        box(x0, x1, y0, y1, 3.6, 8.0, "window")
        n += 1
    # exterior panelboard and the rooftop AC disconnect on the east wall, conduit to grade
    box(300.0, 300.5, 317.0, 319.0, 3.0, 6.2, "panel")
    box(300.0, 300.4, 320.0, 321.0, 7.5, 9.0, "panel")
    rod((300.3, 318.0, -.3), (300.3, 318.0, 3.0), .14, "pvc_grey", seg=8)
    rod((300.3, 320.5, 9.0), (300.3, 320.5, 12.0), .1, "alu", seg=8)                        # up to the roof unit
    rod((300.3, 318.6, 6.2), (300.3, 320.3, 7.5), .1, "alu", seg=8)
    n += 5
    # lights under the canopy
    for x in (283.0, 289.0, 295.0):
        box(x - .6, x + .6, 300.5, 301.5, 9.8, 10.0, "lamp")
        n += 1
    decal((288.5, 296.95, 10.4), (0, -1, 0), 15.0, .75, [("SECURITY  ·  ALL VISITORS STOP AND REPORT", .7, 1, "#ffffff")],
          bg="#1d1f21")
    # CCTV pole at the gatehouse SE corner: PTZ dome and two fixed cameras on the lanes
    cx, cy = 302.5, 302.5
    rod((cx, cy, 0), (cx, cy, 20), .25, "steel", seg=10)
    rod((cx, cy, 19.0), (cx - 1.4, cy, 19.0), .08, "steel", seg=6)
    rod((cx - 1.4, cy, 18.4), (cx - 1.4, cy, 18.9), .45, "machine", seg=12)                 # PTZ dome
    for (dx, dy) in ((-1.1, -.4), (-.9, .5)):
        box(cx + dx - .6, cx + dx, cy + dy - .15, cy + dy + .15, 17.0, 17.4, "machine")      # fixed cameras
    n += 5 + stub(cx + .4, cy, 0, 1.2) + whip((cx + .4, cy, 1.2), (cx + .2, cy, 1.8))
    return n


def sliding_gate():
    n = 0
    # operator at the gate's parked end, its conduit; photo-eye posts across the opening; warning sign
    box(1.6, 3.4, 264.5, 267.5, 0, 3.2, "panel")
    n += 1 + stub(2.5, 267.9, 0, .9) + whip((2.5, 267.9, .9), (2.5, 267.5, 1.6))
    for y in (269.0, 301.0):
        rod((3.2, y, 0), (3.2, y, 2.4), .14, "amber", seg=8)
        box(3.0, 3.4, y - .2, y + .2, 1.6, 2.1, "hero_rail")
        n += 2 + stub(3.6, y, 0, .6)
    rod((5.0, 264.0, 0), (5.0, 264.0, 6.0), .07, "steel", seg=6)
    decal((5.08, 264.0, 5.0), (1, 0, 0), 2.2, 1.4, [("AUTOMATIC GATE", .3, 1, "#111111"),
                                                   ("KEEP CLEAR", .26, 1, "#b3261e")], bg="#f2c21b")
    return n + 1


def build():
    it = new_item("SITE", "Main gate checkpoint: islands, access-control devices, CCTV and their wiring",
                  [0, 305, 262, 326], [-0.5, 21], area="F", register=False,
                  info="Security checkpoint at LOD 3 with the wiring visible: card readers, intercoms, LPR cameras, "
                       "barrier operators with signals, detector loops, CCTV, the gate operator and photo-eyes, each "
                       "fed by conduit from a pull box; one pull box open to show the cables. Typical.")
    it["wiring"] = ["Device power 120 V: 12 AWG Cu THHN/THWN-2 in PVC conduit (Southwire SIMpull)",
                    "Card readers / intercoms: Cat 6A + 18/6 shielded access-control composite to the gatehouse",
                    "Detector loops: 14 AWG XHHW loop wire in saw cuts, twisted-pair lead-in to the loop detectors",
                    "LPR and CCTV cameras: single-mode fibre to the gatehouse switch",
                    "Grounding: bare Cu to ground rods at each pole and the barrier operators"]
    on(it)
    fuel.D = True
    n = 0
    a, _ = island(296.0, 300.0, True)                                                   # inbound (north) lane
    b, pb = island(270.0, 274.0, False)                                                 # outbound (south) lane
    n += a + b
    n += loop(261.5, 267.0, 287.5, 295.5, (265.0, 295.5, 296.0))                       # inbound arming loop
    n += loop(279.5, 285.0, 287.5, 295.5, (282.0, 295.5, 300.0))                       # inbound closing loop
    n += loop(261.5, 267.0, 274.5, 282.5, (265.0, 274.0, 274.5))                       # outbound loops
    n += loop(279.5, 285.0, 274.5, 282.5, (282.0, 270.0, 274.5))
    n += open_pullbox(*pb)
    n += gatehouse()
    n += sliding_gate()
    fuel.D = False
    return n
