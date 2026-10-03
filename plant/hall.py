"""Turbine hall at LOD 3: the gas turbines, generators, steam turbine and their skids.

Footprints and the envelopes that the sheet-09 crane screen measures are kept exactly
(GT top EL 38, generator top EL 36, ST top EL 46, all on the EL 20 deck); inside them the
machines are typical, not engineered:
- H-class GT (cold-end drive): baseplate, inlet plenum with the side inlet from the plenum
  spool, bellmouth, compressor casing with horizontal-joint flanges, stiffener rings and the
  variable guide-vane actuator ring, combustor section with 16 can covers on a fuel-gas
  manifold ring with pigtails, turbine casing, exhaust diffuser with strut flange, front and
  rear supports, lube-oil supply and drain to both bearings, junction boxes and conduits;
- H2-cooled generator: stator frame, end shields, hydrogen coolers on top, bearing pedestals,
  collector / exciter end, line-side terminal box under the south end feeding the IPB,
  coupling guard to the GT;
- steam turbine (HP-IP-LP-generator): LP casing with its east side-exhaust hood, combined
  HP/IP casing, crossover pipe, main stop / control valve chests fed by the main steam line,
  bearing pedestals, transition to the 26 ft exhaust duct;
- lube-oil skids (reservoir, pumps, duplex filters, coolers, mist eliminator), CO2 cylinder
  racks with their manifold, compressor water-wash skids;
- hall: crane rails on the runway girders, high-bay lights, wall girts.

Uses the primitives in fuel.py; runs after yard.py.
"""
import math

import fuel
from fuel import box, rod, pipe, find, strip, on


def dress(flag):
    fuel.D = flag


def ring(cx, y, cz, r, rr, c, n=24, layer=None):
    """Horizontal-axis ring (about y) of radius r, tube radius rr."""
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        rod((cx + r * math.cos(a0), y, cz + r * math.sin(a0)), (cx + r * math.cos(a1), y, cz + r * math.sin(a1)),
            rr, c, seg=6, layer=layer)


# ---------------------------------------------------------------------------------------
def gas_turbines():
    for k in range(3):
        dx = 160 * k
        cx, cz = 630 + dx, 29.0
        gt = find(f"GT{k + 1}: H-class")
        strip(gt)
        box(617 + dx, 643 + dx, 455, 540, 20, 21.5, "steel")                       # baseplate
        # inlet plenum (cold end), side inlet towards the plenum spool on the east
        box(619 + dx, 641 + dx, 455, 467, 21.5, 37.4, "machine")
        box(618.6 + dx, 641.4 + dx, 454.6, 467.4, 37.4, 38, "steel")
        rod((cx, 467, cz), (cx, 470, cz), 7.4, "machine", r2=6.3, seg=28)          # bellmouth
        # compressor
        rod((cx, 470, cz), (cx, 495, cz), 6.3, "machine", r2=5.1, seg=28)
        rod((cx, 473, cz), (cx, 474.2, cz), 6.9, "steel", seg=28)                   # VGV actuator ring
        # combustor section and can covers (inside the EL 38 envelope)
        rod((cx, 495, cz), (cx, 507, cz), 8.2, "machine", seg=32)
        for c in range(16):
            a = 2 * math.pi * (c + .5) / 16
            ca, sa = math.cos(a), math.sin(a)
            rod((cx + 7.4 * ca, 499, cz + 7.4 * sa), (cx + 8.05 * ca, 496.2, cz + 8.05 * sa), .85, "steel", seg=10)
        # turbine and exhaust diffuser
        rod((cx, 507, cz), (cx, 524, cz), 6.9, "machine", r2=7.8, seg=30)
        rod((cx, 524, cz), (cx, 525.2, cz), 8.4, "steel", seg=30)                   # strut flange
        rod((cx, 525.2, cz), (cx, 540, cz), 7.9, "machine", r2=8.9, seg=32)
        # supports
        for (ya, yb, w) in ((471, 476, 9), (528, 534, 12)):
            box(cx - w / 2, cx + w / 2, ya, yb, 21.5, cz - 5, "steel")
        dress(True)
        for y in range(477, 495, 4):                                                 # compressor stiffener rings
            rr = 6.3 - (6.3 - 5.1) * (y - 470) / 25
            rod((cx, y - .15, cz), (cx, y + .15, cz), rr + .22, "steel", seg=28)
        for s in (-1, 1):                                                            # horizontal-joint flanges
            for (y0, y1, r0, r1) in ((470, 495, 6.3, 5.1), (507, 524, 6.9, 7.8), (525.2, 540, 7.9, 8.9)):
                n = 5
                for m in range(n):
                    ya, yb = y0 + (y1 - y0) * m / n, y0 + (y1 - y0) * (m + 1) / n
                    ra = r0 + (r1 - r0) * (m + .5) / n
                    box(cx + s * ra - .35, cx + s * ra + .35, ya, yb, cz - .3, cz + .3, "steel")
            box(cx + s * 8.2 - .35, cx + s * 8.2 + .35, 495, 507, cz - .3, cz + .3, "steel")
        for a in (math.radians(25), math.radians(155)):                               # VGV actuators
            box(cx + 7.3 * math.cos(a) - .8, cx + 7.3 * math.cos(a) + .8, 472.5, 475,
                cz + 7.3 * math.sin(a) - .8, cz + 7.3 * math.sin(a) + .8, "amber")
        # fuel-gas manifold ring with pigtails to each can; feed from the gas fuel module
        ring(cx, 494.6, cz, 9.3, .32, "fuelgas", n=32)
        for c in range(16):
            a = 2 * math.pi * (c + .5) / 16
            ca, sa = math.cos(a), math.sin(a)
            rod((cx + 9.3 * ca, 494.6, cz + 9.3 * sa), (cx + 8.2 * ca, 496.4, cz + 8.2 * sa), .13, "fuelgas", seg=6)
        pipe([(643 + dx, 514, 32), (644.5 + dx, 514, 32), (644.5 + dx, 494.6, 32), (639 + dx, 494.6, 32)], 32, .45,
             "fuelgas")
        # lube oil supply (amber stripe) and drain from the aux skid to both bearings
        for (yb, zb) in ((473.5, 23.5), (531, 23.5)):
            pipe([(661 + dx, 486, 22.3), (646 + dx, 486, 22.3), (646 + dx, yb, 22.3), (cx + 4, yb, 22.3),
                  (cx + 4, yb, zb)], 22.3, .22, "amber")
            pipe([(661 + dx, 489, 21.9), (647.5 + dx, 489, 21.9), (647.5 + dx, yb + 1.2, 21.9), (cx + 4.5, yb + 1.2, 21.9)],
                 21.9, .3, "machine")
        # junction boxes and conduits to the LV / control tray drop beside the aux skid
        for (y, zj) in ((480, 30), (515, 31)):
            box(cx + 9.4, cx + 10.6, y - 1.2, y + 1.2, zj - 1.5, zj + 1.5, "panel")
            pipe([(cx + 10.6, y, zj), (cx + 12.5, y, zj), (cx + 12.5, y, 30.5), (cx + 12.5, 487, 30.5),
                  (678 + dx, 487, 30.5)], 30.5, .1, "steel")
        # exhaust thermocouples: 16 heads around the diffuser, wheel-space thermocouples on the
        # turbine casing, yellow type KX extension cable rings to the junction box at y 515
        for (yt, rt, n) in ((536, 8.6, 16), (516, 7.3, 8)):
            for m in range(n):
                a = 2 * math.pi * (m + .5) / n
                ca, sa = math.cos(a), math.sin(a)
                rod((cx + rt * ca, yt, cz + rt * sa), (cx + (rt + .9) * ca, yt, cz + (rt + .9) * sa), .12, "steel", seg=6)
                rod((cx + (rt + .9) * ca, yt - .25, cz + (rt + .9) * sa), (cx + (rt + .9) * ca, yt + .25, cz + (rt + .9) * sa),
                    .22, "steel", seg=8)                                          # thermocouple head
            ring(cx, yt + .6, cz, rt + 1.1, .09, "cable_tcx", n=32)
        pipe([(cx + 9.7, 536.6, cz), (cx + 10.2, 536.6, cz), (cx + 10.2, 515, cz + .5), (cx + 9.4, 515, 31)], cz, .09,
             "cable_tcx")
        pipe([(cx + 8.4, 516.6, cz), (cx + 9.4, 516.6, cz), (cx + 9.4, 515.5, 30.5)], cz, .09, "cable_tcx")
        dress(False)

        # generator
        gg = find(f"GTG-{k + 1}:")
        strip(gg)
        gx, gz = 630 + dx, 28.0
        box(622 + dx, 638 + dx, 410, 455, 20, 21.5, "steel")
        rod((gx, 416, gz), (gx, 450, gz), 7.0, "machine", seg=32)                   # stator frame
        for (ya, yb) in ((413.2, 416), (450, 452.6)):
            rod((gx, ya, gz), (gx, yb, gz), 6.3, "machine", seg=28)                 # end shields
        box(623 + dx, 637 + dx, 419, 447, 34.4, 36, "machine")                        # H2 cooler housings
        for y in (424, 433, 442):
            box(623.4 + dx, 636.6 + dx, y - 3.4, y + 3.4, 33.6, 35.9, "radiator")
        rod((gx, 410.4, gz), (gx, 413.2, gz), 3.6, "steel", seg=20)                 # collector / exciter end
        box(625 + dx, 635 + dx, 410, 417, 21.5, 24.5, "steel")                        # line-side terminal box
        for y in (414.5, 451.5):
            box(gx - 4.5, gx + 4.5, y - 1.3, y + 1.3, 21.5, gz - 4, "steel")       # bearing pedestals
        rod((gx, 452.6, gz), (gx, 455, gz), 2.4, "steel", seg=18)                   # coupling guard
        dress(True)
        for y in range(419, 450, 5):                                                 # frame ribs
            rod((gx, y - .2, gz), (gx, y + .2, gz), 7.2, "steel", seg=32)
        for s in (-1, 1):                                                            # cooler water piping
            pipe([(gx + s * 6.6, 421, 35), (gx + s * 8, 421, 35), (gx + s * 8, 421, 21.6)], 35, .2, "cw")
        rod((gx + 6.4, 430, 22), (gx + 6.4, 430, 26), .6, "red", seg=10)              # H2 / CO2 purge panel
        dress(False)


def steam_turbine():
    st = find("ST: steam turbine")
    strip(st)
    sx, sz = 1050, 31.0
    box(1020, 1080, 460, 552, 20, 21.5, "steel")
    # LP casing with the east side-exhaust hood (exhaust duct y 487-513)
    box(1026, 1074, 472, 528, 21.5, 40, "machine")
    _add_prism(1026, 1074, 472, 528, 40, 46, st)
    box(1074, 1076, 485, 515, 29, 45.5, "machine")                                 # hood flange to the duct
    # HP/IP casing at the north end
    rod((sx, 530, sz), (sx, 534, sz), 4.5, "machine", r2=6.6, seg=28)
    rod((sx, 534, sz), (sx, 548, sz), 6.6, "machine", seg=28)
    rod((sx, 548, sz), (sx, 551.5, sz), 6.6, "machine", r2=4.2, seg=28)
    # crossover HP/IP -> LP, inside the EL 46 envelope
    rod((sx, 538, sz + 6.4), (sx, 538, 43.5), 2.2, "machine", seg=16)
    rod((sx, 538, 43.5), (sx, 526, 43.5), 2.2, "machine", seg=16)
    rod((sx, 526, 43.5), (sx, 526, 41), 2.2, "machine", seg=16)
    # main stop / control valve chests beside the HP/IP casing
    for xv in (1029, 1071):
        rod((xv, 545, 21.5), (xv, 545, 36), 2.5, "machine", seg=18)
        box(xv - 1.4, xv + 1.4, 543.6, 546.4, 36, 40.5, "amber")
        rod((xv, 545, 30), (sx + (6.4 if xv > sx else -6.4), 541, sz), 1.2, "machine", seg=14)
    for y in (470, 529.5, 552):
        box(sx - 5, sx + 5, y - 1.2, min(y + 1.2, 552), 21.5, sz - 3.5, "steel")    # bearing pedestals
    dress(True)
    for s in (-1, 1):                                                              # horizontal joint
        box(sx + s * 6.6 - .35, sx + s * 6.6 + .35, 534, 548, sz - .3, sz + .3, "steel")
        box(1026 - .4 if s < 0 else 1074, 1026 if s < 0 else 1074.4, 472, 528, sz - .3, sz + .3, "steel")
    for y in range(476, 528, 6):                                                    # LP casing ribs
        box(1025.6, 1026, y - .3, y + .3, 21.5, 40, "steel")
    # main steam from the drawn route end into both valve chests
    for xv in (1029, 1071):
        pipe([(1050, 552, 27), (xv, 552, 27), (xv, 546.5, 27)], 27, 1.1, "pipe")
    box(1076, 1080, 487, 513, 31, 57, "duct")                                        # transition to the exhaust duct
    dress(False)
    sg = find("STG:")
    strip(sg)
    box(1041, 1059, 410, 460, 20, 21.5, "steel")
    rod((1050, 416, 29), (1050, 454, 29), 8.0, "machine", seg=32)
    for (ya, yb) in ((412.5, 416), (454, 457)):
        rod((1050, ya, 29), (1050, yb, 29), 7.2, "machine", seg=28)
    box(1042, 1058, 422, 448, 37, 38, "machine")
    rod((1050, 410.3, 29), (1050, 412.5, 29), 3.8, "steel", seg=20)
    box(1045, 1055, 410, 418, 21.5, 24.5, "steel")
    rod((1050, 457, 29), (1050, 460, 29), 2.6, "steel", seg=18)


def _add_prism(x0, x1, y0, y1, z0, z1, it):
    fuel.G["parts"].append(dict(kind="prism", min=[x0, y0, z0], max=[x1, y1, z1], ridge="y", color="machine",
                                item=it["id"], layer=it["layer"]))


def skids():
    for name, (x0, x1, y0, y1) in [(f"GT{k} aux", (661 + 160 * (k - 1), 675 + 160 * (k - 1), 470, 505))
                                   for k in (1, 2, 3)] + [("ST aux", (1082, 1098, 470, 505))]:
        it = find(name + ":")
        strip(it)
        xm = (x0 + x1) / 2
        box(x0, x1, y0, y1, 20, 20.8, "steel")
        box(x0 + .5, x1 - .5, y0 + 1, y0 + 18, 20.8, 26, "tank")                   # lube-oil reservoir
        for xp in (x0 + 3.5, x1 - 3.5):                                              # AC / DC pumps on the lid
            rod((xp, y0 + 5, 26), (xp, y0 + 5, 27.6), .9, "pump", seg=12)
            rod((xp, y0 + 5, 27.6), (xp, y0 + 5, 30), .8, "motor", seg=12)
        for xf in (x0 + 3, x1 - 3):                                                  # duplex filters
            rod((xf, y0 + 21, 20.8), (xf, y0 + 21, 26.5), 1.0, "tank", seg=14)
        box(x0 + .5, x1 - .5, y0 + 24, y1 - 1, 20.8, 28.5, "bundle")                 # oil coolers
        rod((xm, y0 + 14, 26), (xm, y0 + 14, 29.5), .6, "steel", seg=10)            # mist eliminator stack
        box(x0 + .5, x0 + 4, y0 + 10, y0 + 15, 26, 28, "panel")
        dress(True)
        pipe([(x0 + 3, y0 + 21, 26.5), (x0 + 3, y0 + 18.5, 26.5)], 26.5, .25, "amber")
        pipe([(x1 - 3, y0 + 21, 26.5), (x1 - 3, y0 + 24.5, 26.5)], 26.5, .25, "amber")
        dress(False)
    for k in (1, 2, 3):
        dx = 160 * (k - 1)
        it = find(f"FS-GT{k}:")
        strip(it)
        box(662 + dx, 674 + dx, 510, 534, 20, 20.6, "steel")
        for row, x in enumerate((664 + dx, 667 + dx, 670 + dx)):
            for y in range(512, 532, 2):
                rod((x, y + 1, 20.6), (x, y + 1, 25.8), .55, "red", seg=10)
        box(662.5 + dx, 673.5 + dx, 510.5, 533.5, 26.6, 27, "steel")               # cylinder rack frame
        rod((672.5 + dx, 511, 26.2), (672.5 + dx, 533, 26.2), .3, "red", seg=8)    # discharge manifold
        box(672.5 + dx, 674 + dx, 511, 515, 20.6, 28, "panel")
        it = find(f"WASH-GT{k}:")
        strip(it)
        box(584 + dx - 160 * 0, 596 + dx, 475, 495, 20, 20.6, "steel")
        rod((590 + dx, 481, 20.6), (590 + dx, 481, 26.4), 4, "tank", seg=20)
        rod((590 + dx, 481, 26.4), (590 + dx, 481, 27), 3.2, "tank", seg=20)
        for y in (488, 492):
            rod((587 + dx, y, 22.2), (590 + dx, y, 22.2), .9, "pump", seg=12)
            rod((590.2 + dx, y, 22.2), (593 + dx, y, 22.2), .8, "motor", seg=12)
        dress(True)
        pipe([(594 + dx, 490, 22.2), (606 + dx, 490, 22.2), (606 + dx, 466, 22.2), (619 + dx, 466, 30)], 22.2, .18,
             "pipe")
        dress(False)


def spools():
    """Removable plenum spools: bolted flange frames at both ends and lifting lugs."""
    for k in (1, 2, 3):
        dx = 160 * (k - 1)
        on(find(f"GT{k} removable plenum spool"))
        dress(True)
        for x in (643.15, 657.85):
            for (y0, y1, z0, z1) in ((440, 466, 23, 23.6), (440, 466, 36.4, 37), (440, 440.6, 23, 37), (465.4, 466, 23, 37)):
                box(x - .25 + dx, x + .25 + dx, y0, y1, z0, z1, "steel")
        for y in (445, 461):
            box(649.5 + dx, 651.5 + dx, y - .3, y + .3, 37, 38.2, "steel")
        dress(False)


def hall_fitout():
    hall = find("Common turbine hall")
    on(hall)
    dress(True)
    for y in (404, 556):                                                             # crane rails on the girders
        box(482, 1098, y - .25, y + .25, 84, 84.6, "steel")
    for x in range(520, 1100, 44):                                                   # high-bay lights
        for y in (430, 480, 530):
            rod((x, y, 96.5), (x, y, 94.5), .06, "steel", seg=4)
            rod((x, y, 94.5), (x, y, 93.6), 1.3, "lamp", r2=.8, seg=12)
    for z in (30, 50, 70):                                                           # wall girts (inside face)
        for y, s in ((404.6, 1), (558.4, -1)):
            box(484, 1096, y, y + s * .5, z - .4, z + .4, "steel")
    dress(False)


def cubicle(x0, x1, y0, y1, z0, z1, c="cabinet", face="y0", n=None):
    """Lineup of cubicles: plinth, body, roof, door seams and louvres on one face (dressing)."""
    box(x0, x1, y0, y1, z0, z0 + .4, "concrete")
    box(x0 + .1, x1 - .1, y0 + .1, y1 - .1, z0 + .4, z1 - .3, c)
    box(x0, x1, y0, y1, z1 - .3, z1, "roof")
    dress(True)
    along_x = face in ("y0", "y1")
    L = (x1 - x0) if along_x else (y1 - y0)
    n = n or max(1, int(L // 3))
    for m in range(n):
        a0 = (x0 if along_x else y0) + .1 + (L - .2) * m / n
        a1 = a0 + (L - .2) / n
        if face == "y0":
            box(a0 + .08, a1 - .08, y0, y0 + .1, z0 + .8, z1 - .8, "door")
            box(a0 + .5, a1 - .5, y0 - .02, y0 + .1, z1 - 2, z1 - 1.2, "louvre")
        elif face == "y1":
            box(a0 + .08, a1 - .08, y1 - .1, y1, z0 + .8, z1 - .8, "door")
            box(a0 + .5, a1 - .5, y1 - .1, y1 + .02, z1 - 2, z1 - 1.2, "louvre")
        elif face == "x0":
            box(x0, x0 + .1, a0 + .08, a1 - .08, z0 + .8, z1 - .8, "door")
        else:
            box(x1 - .1, x1, a0 + .08, a1 - .08, z0 + .8, z1 - .8, "door")
    dress(False)


def unit_electrical():
    """Per-unit electrical equipment the drawing leaves to the vendor (typical): static
    excitation cubicles and their dry-type excitation transformer, surge-protection / VT
    cubicle on the IPB and the GCB control cabinet in the south gallery; neutral grounding
    cubicle at the generator neutral and turbine control / protection cabinets on the deck."""
    L = "BASE_ELECTRICAL"
    units = [(k, 160 * (k - 1), f"GTG-{k}", f"GT{k}") for k in (1, 2, 3)]
    for k, dx, gen, gt in units:
        meta = dict(area="A", basis="typical", sheet="typical (hall cabling)")
        fuel.new_item(L, f"EXC-{k}: static excitation cubicles ({gen})", (640 + dx, 657 + dx, 393, 401), (0, 8),
                      tag=f"EXC-{k}", info="Thyristor bridges, field breaker, AVR and protection; DC field "
                      "cables to the generator collector end.", **meta)
        cubicle(640 + dx, 657 + dx, 393, 401, 0, 8, face="y0")
        fuel.new_item(L, f"ET-{k}: excitation transformer (dry type, {gen} terminals)", (604 + dx, 614 + dx, 392, 401),
                      (0, 9), tag=f"ET-{k}", info="Fed from the IPB at the generator terminals (typical).", **meta)
        cubicle(604 + dx, 614 + dx, 392, 401, 0, 9, c="xfmr", face="x0", n=2)
        fuel.new_item(L, f"SPC-{k}: surge-protection and VT cubicle on the IPB ({gen})", (616 + dx, 623 + dx, 394, 401),
                      (0, 8), tag=f"SPC-{k}", info="Surge capacitors, arresters and voltage transformers for metering, "
                      "protection and synchronising.", **meta)
        cubicle(616 + dx, 623 + dx, 394, 401, 0, 8, face="y0", n=2)
        fuel.new_item(L, f"NGT-{k}: neutral grounding cubicle ({gen})", (646 + dx, 653 + dx, 410, 417), (20, 27),
                      tag=f"NGT-{k}", info="Distribution-type grounding transformer and secondary resistor "
                      "(high-resistance grounding, typical).", **meta)
        cubicle(646 + dx, 653 + dx, 410, 417, 20, 27, face="x1", n=2)
        fuel.new_item(L, f"TCP-{k}: {gt} turbine control and protection cabinets", (598 + dx, 612 + dx, 505, 515), (20, 28),
                      tag=f"TCP-{k}", info="Turbine controller, overspeed and generator protection, fire and gas "
                      "panel; fibre to the DCS in the control room (typical).", **meta)
        cubicle(598 + dx, 612 + dx, 505, 515, 20, 28, face="y0")
    meta = dict(area="A", basis="typical", sheet="typical (hall cabling)")
    fuel.new_item(L, "EXC-ST: static excitation cubicles (STG)", (1060, 1077, 393, 401), (0, 8), tag="EXC-ST", **meta)
    cubicle(1060, 1077, 393, 401, 0, 8, face="y0")
    fuel.new_item(L, "NGT-ST: neutral grounding cubicle (STG)", (1061, 1068, 410, 417), (20, 27), tag="NGT-ST", **meta)
    cubicle(1061, 1068, 410, 417, 20, 27, face="x1", n=2)
    fuel.new_item(L, "TCP-ST: ST turbine control and protection cabinets", (1082, 1096, 426, 436), (20, 28),
                  tag="TCP-ST", **meta)
    cubicle(1082, 1096, 426, 436, 20, 28, face="y1")


def hall_services():
    """Hall services as dressing: crane conductor bar, lighting circuits, grounding risers,
    and a control-tray riser to each filter-house platform (pulse-jet and anti-icing controls)."""
    hall = find("Common turbine hall")
    on(hall)
    dress(True)
    box(482, 1098, 556.9, 557.3, 81, 81.8, "copper_dark")                          # crane conductor bar
    for x in range(500, 1100, 15):
        box(x - .1, x + .1, 556.9, 557.3, 81.8, 82, "insulator")
    for y in (430, 480, 530):                                                      # lighting circuit conduits
        rod((520, y, 96.6), (1092, y, 96.6), .08, "steel", seg=4)
    for x in range(520, 1100, 44):                                                 # grounding risers on the columns
        for y in (405.3, 554.6):
            box(x + 1.3, x + 1.5, y - .1, y + .1, 0, 6, "copper")
    dress(False)
    for k in range(3):
        dx = 160 * k
        fh = find(f"FH-{k + 1}:")
        on(fh)
        dress(True)
        x, y = 690 + dx, 361                                                       # ladder tray riser to EL 108
        for s in (-1, 1):
            box(x + s * .75 - .06, x + s * .75 + .06, y - .2, y + .2, 0, 108, "pipe")
        for z in range(1, 108, 2):
            box(x - .75, x + .75, y + .1, y + .2, z - .08, z + .08, "pipe")
        for m in range(4):
            rod((x - .5 + m * .33, y - .05, 0), (x - .5 + m * .33, y - .05, 108), .1, "cable", seg=6)
        box(x - 2, x + 2, y - 1.5, y + 1.5, 108, 112, "panel")                     # pulse-jet / anti-icing panel
        dress(False)


# cable applications for the hall's main machines and services (they had none; the turbine-hall
# trays and drops already reach each of them)
_MV = "MV 13.8 kV: Cu MV-105, 133% insulation, shielded, in ladder tray"
_LV = "LV 480 V: Cu XHHW-2, Type TC-ER (UL 1277), in ladder tray"
_MC = "LV 480 V / 120 V branch: Type MC-HL (Southwire ARMOR-X) from the tray to the device"
_CTRL = "Control 120 V AC / 125 V DC: 14 AWG multiconductor, Type TC-ER (ICEA S-73-532)"
_INST = "Instrumentation 4-20 mA / HART: shielded pairs / triads, Type TC-ER / PLTC"
_TCX = "Thermocouple extension: Type K (KX) shielded pairs, Type PLTC"
_RTD = "RTD leads: three-wire shielded, Type PLTC"
_VIB = "Vibration and keyphasor: proximity-probe extension cable and shielded triads"
_FA = "Fire and gas detection / CO2 release: FPLR shielded, red jacket (NEC 760)"
_DATA = "Data / DCS network: fibre optic (single-mode), orange jacket"
_LIGHT = "Lighting, receptacles, small power: Cu THHN/THWN-2 in conduit / MC cable"
_GND = "Grounding: bare Cu 4/0 to the station grid, green-insulated equipment grounds"
_HT = "Space heaters / heat trace: 120 / 240 V, Type MC or TC-ER"
HALL_WIRING = [
    (r"^GT\d: H-class gas turbine", [_CTRL, _INST, _TCX, _VIB, _FA, _MC + " (enclosure lights, heaters)", _GND]),
    (r"^GTG-\d: GT generator", [_RTD, _VIB, _CTRL, _HT, "Generator protection CT / VT secondaries: 10 AWG, Type TC-ER", _GND]),
    (r"^ST: steam turbine", [_CTRL, _INST, _TCX, _VIB, "Electro-hydraulic control (EHC) servo cable: shielded", _MC, _GND]),
    (r"^STG: steam-turbine generator", [_RTD, _VIB, _CTRL, _HT, "Generator protection CT / VT secondaries: 10 AWG, Type TC-ER", _GND]),
    (r"^ST aux", [_LV, _CTRL, _INST, _MC + " (turning gear, lube oil pumps)", _GND]),
    (r"^GCB-", [_CTRL + " (trip / close, interlocks)", "CT / VT secondaries: 10 AWG, Type TC-ER", _HT, _GND]),
    (r"^TCP-", [_LV + " (UPS-backed 120 V)", _CTRL, _INST, _DATA, _GND]),
    (r"^Bridge crane", ["Crane runway conductor bar 480 V fed from a fused disconnect at the north wall",
                        "Pendant / radio control: 120 V", _GND]),
    (r"^Common turbine hall", [_LIGHT + " (high-bay LED, emergency and exit lighting)", _FA + " (smoke, heat, manual stations, horns)",
                               _MC + " (roof exhausters, wall louvre actuators)", _DATA + " (CCTV, Wi-Fi)",
                               "Lightning protection: air terminals and down conductors to ground rods", _GND]),
]


def hall_electrical():
    """Turbine hall electrical, internal and external (audit pass): cable applications on every
    machine, lighting / small-power / fire-alarm panels, wall penetrations with fire stops, the
    crane feed, roof exhausters fed by exterior MC-cable risers, wall-pack lighting with conduit,
    exterior receptacles and alarm beacons, and lightning protection."""
    import re
    for it in fuel.G["items"]:
        for pat, apps in HALL_WIRING:
            if re.search(pat, it["name"]):
                it["wiring"] = apps
    hall = find("Common turbine hall")
    on(hall)
    dress(True)
    roof = lambda y: 98 + 3 * (1 - abs(y - 482) / 78)
    # ---- inside: power / lighting panels and fire-alarm devices along the north wall at deck level
    for k, x in enumerate(range(600, 1081, 160)):
        box(x, x + 6, 557.6, 558.6, 21, 28, "panel")                                     # lighting / small-power panel
        box(x + 7, x + 9, 557.9, 558.6, 23, 26, "red")                                    # fire-alarm panel / pull station
        rod((x + 3, 558.2, 28), (x + 3, 558.2, 44), .12, "steel", seg=6)                  # conduit up to the LV tray
        for xr in range(x - 60, x + 60, 30):                                              # receptacles / welding outlets
            if 562 < xr < 1096:
                box(xr, xr + 1.2, 558.1, 558.6, 22, 23.6, "amber")
    for (x, y) in ((482, 460), (1097, 460), (560, 405.5), (900, 405.5), (500, 557.5)):     # horn / strobes
        box(x - .4, x + .4, y - .4, y + .4, 14, 15.2, "red")
    for gx in (575, 735, 895, 1055):                                                       # exit signs over doors
        box(gx - 2, gx + 2, 371.2, 371.6, 17, 18.3, "lamp")
    # ---- crane feed: fused disconnect on a north-wall column, feed to the conductor bar
    box(546, 550, 557.4, 558.6, 70, 76, "cabinet")
    rod((548, 558, 76), (548, 558, 81.4), .12, "steel", seg=6)
    rod((548, 558, 70), (548, 558, 48), .12, "steel", seg=6)
    # ---- wall penetrations: fire-stopped sleeves where the trays cross the north wall
    for (x, z, w) in ((560, 48, 3.4), (560, 44, 3.4), (500, 42, 2.4)):
        box(x - w / 2 - .4, x + w / 2 + .4, 558.6, 560.6, z - .6, z + 1.6, "concrete")
    dress(False)
    # ---- outside: MC-cable risers on the east and west walls from the duct bank to the roof, a roof tray
    # along each side of the ridge to the roof exhausters
    out = fuel.new_item("BASE_POWER_BLOCK", "Turbine hall exterior electrical: MC-cable risers, roof exhausters, "
                        "wall lighting, receptacles, lightning protection", (472, 1108, 362, 568), (0, 106),
                        area="A", basis="typical", sheet="typical (turbine hall electrical)",
                        info="Roof exhausters and wall louvre actuators fed by Type MC-HL (ARMOR-X) cables on exterior "
                             "ladder risers from the duct bank; LED wall packs on conduit with pull boxes; weatherproof "
                             "receptacles and beacons at the doors; air terminals on the ridge, down conductors at the corners.")
    out["wiring"] = [_MC, _LIGHT, _FA, "Lightning protection: Cu / Al conductors, UL 96A", _GND]
    dress(True)
    for (x, s, y) in ((1100.2, 1, 430), (479.8, -1, 530)):
        xo = x + s * 1.2
        box(x + s * 2.6 - .8, x + s * 2.6 + .8, y - 2.5, y + 2.5, -3, .3, "concrete")      # duct bank riser box
        for d in (-1.1, 1.1):
            box(xo - .06, xo + .06, y + d - .06, y + d + .06, .3, roof(y) + 1, "pipe")     # ladder rails
        z = 2
        while z < roof(y):
            box(xo - .06, xo + .06, y - 1.1, y + 1.1, z - .06, z + .06, "pipe")            # rungs
            z += 2
        for c in range(5):
            rod((xo + s * .25, y - .8 + c * .4, .3), (xo + s * .25, y - .8 + c * .4, roof(y) + .6), .12,
                "cable_mc", seg=6)
        for z in range(12, int(roof(y)), 14):                                               # standoff brackets
            box(min(x, xo), max(x, xo), y - 1.4, y + 1.4, z - .2, z + .2, "steel")
    for yr in (470, 494):                                                                   # roof trays both sides of the ridge
        z = roof(yr)
        box(482, 1098, yr - .7, yr + .7, z + .4, z + .55, "pipe")
        for c in range(3):
            rod((482, yr - .4 + c * .4, z + .7), (1098, yr - .4 + c * .4, z + .7), .1, "cable_mc", seg=6)
        for x in range(500, 1098, 20):
            box(x - .3, x + .3, yr - .8, yr + .8, z, z + .45, "steel")                       # roof supports
    for x in range(520, 1090, 48):                                                          # roof exhausters
        for yr in (470, 494):
            z = roof(yr) + .2
            rod((x, yr + (6 if yr > 482 else -6), z), (x, yr + (6 if yr > 482 else -6), z + 3), 2.6, "machine", seg=16)
            rod((x, yr + (6 if yr > 482 else -6), z + 3), (x, yr + (6 if yr > 482 else -6), z + 4.4), 3.4, "roof",
                r2=.8, seg=16)
            box(x - .4, x + .4, yr + (2 if yr > 482 else -2.8), yr + (2.8 if yr > 482 else -2), z, z + 2.2, "panel")
    # wall packs with conduit and pull boxes, receptacles and beacons at the doors
    for (y, s) in ((559.9, 1), (370.1, -1)):
        yy = y + s * .3
        for x in range(500, 1090, 40):
            if y > 500 and any(a - 4 < x < b + 4 for (a, b) in ((619, 641), (779, 801), (939, 961), (1067, 1143))):
                continue
            box(x - .8, x + .8, yy, yy + s * .7, 19, 20.4, "lamp")
        if y > 500:
            continue
        rod((484, yy + s * .2, 18.4), (1096, yy + s * .2, 18.4), .1, "steel", seg=4)       # conduit along the wall
        for x in range(500, 1090, 80):
            box(x - .5, x + .5, yy, yy + s * .5, 17.8, 18.9, "panel")                        # pull boxes
    for gx in (575, 735, 895, 1055):
        box(gx - 9, gx - 8, 369.4, 370, 4, 5.2, "amber")                                    # WP receptacle
        rod((gx - 10, 369.6, 17), (gx - 10, 369.6, 17.8), .35, "red", seg=10)              # beacon / horn-strobe
    # lightning protection: air terminals on the ridge, down conductors at the corners to ground rods
    for x in range(484, 1100, 40):
        rod((x, 482, 101), (x, 482, 103.5), .06, "copper", seg=4)
    rod((484, 482, 101.2), (1096, 482, 101.2), .05, "copper", seg=4)
    for (x, y) in ((480.6, 404.6), (1099.4, 404.6), (480.6, 559.4), (1099.4, 559.4)):
        rod((x, y, 98), (x, y, 0), .06, "copper", seg=4)
        box(x - .3, x + .3, y - .3, y + .3, -.5, .2, "concrete")
    dress(False)


def build():
    gas_turbines()
    steam_turbine()
    skids()
    spools()
    hall_fitout()
    unit_electrical()
    hall_services()
    hall_electrical()
