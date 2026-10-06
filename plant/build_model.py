#!/usr/bin/env python3
"""Build the SK-3X1 Rev 14 3D coordinate model.

Source: "SK-3X1 Drawing Set Rev 14" (3x1 combined-cycle plant, 16 sheets).
Plan coordinates (X east, Y north, feet, origin at the SW corner of the
2,420 x 1,920 ft compound) come from the vector geometry of sheets
SK-3X1-01 (base site), -02 (optional systems) and -05 (R1 floor plan).
Elevations come from SK-3X1-09 (hall section), -12 (dimension review) and
-13 (height comparison). Anything without a published value uses a typical
value and is tagged basis="typical".

The model has two levels:
  items  - the equipment register: one entry per piece of equipment, with its
           drawn footprint (fp), envelope, tag, layer, area, basis and sheet.
  parts  - the carved geometry of each item (boxes, rods / cones, A-frame
           prisms and 8-vertex lofts), each pointing at its item.

Layers follow the Blender collections on SK-3X1-11, so the view
definitions on that sheet (e.g. view B hides R1_ROOF and R1_WALL_E) map
one-to-one.

Output: sk3x1_model.json, consumed by render.go (ln line art),
viewer/index.html (Three.js), export_obj.py and verify.py.

Conceptual illustration. Not engineered. Not for construction.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

items, parts = [], []
_cur = None


# ---------------------------------------------------------------------------
# Builder primitives
# ---------------------------------------------------------------------------
def item(layer, name, fp, z, *, tag="", area="", info="", basis="drawing",
         sheet="SK-3X1-01", shape="rect", register=True):
    """Start an equipment item. fp = (x0, x1, y0, y1) drawn footprint (for a
    circle: the bounding square), z = (z0, z1) envelope. Parts added after
    this call belong to it."""
    global _cur
    _cur = dict(id=f"{layer.lower()}-{len(items)+1:04d}", layer=layer, name=name,
                tag=tag, area=area, fp=[round(v, 2) for v in fp], z=list(z),
                shape=shape, info=info, basis=basis, sheet=sheet, register=register)
    items.append(_cur)
    return _cur


def _part(**kw):
    kw.setdefault("item", _cur["id"])
    kw.setdefault("layer", _cur["layer"])
    parts.append(kw)


def B(x0, x1, y0, y1, z0, z1, c="equip", layer=None):
    """Axis-aligned box."""
    _part(kind="box", min=[x0, y0, z0], max=[x1, y1, max(z1, z0 + 0.1)], color=c,
          **({"layer": layer} if layer else {}))


def R(a, b, r, c="equip", r2=None, seg=None, layer=None):
    """Rod / cylinder / cone frustum from point a to point b (radius r at a,
    r2 at b)."""
    kw = dict(kind="rod", a=list(a), b=list(b), r=r, r2=r if r2 is None else r2, color=c)
    if seg:
        kw["seg"] = seg
    if layer:
        kw["layer"] = layer
    _part(**kw)


def V(cx, cy, r, z0, z1, c="equip", r2=None, seg=None):
    """Vertical cylinder."""
    R((cx, cy, z0), (cx, cy, z1), r, c, r2, seg)


def P(x0, x1, y0, y1, z0, z1, c="equip", ridge="y"):
    """Gable / A-frame prism, ridge along `ridge`."""
    _part(kind="prism", min=[x0, y0, z0], max=[x1, y1, z1], ridge=ridge, color=c)


def H(v, c="equip"):
    """8-vertex loft (hexahedron): v = [near 4 (ccw), far 4 (same order)]."""
    _part(kind="hex", v=[list(p) for p in v], color=c)


def loft_y(y0, rect0, y1, rect1, c):
    """Loft between two rectangles facing north: rect = (x0, x1, z0, z1)."""
    a, b = rect0, rect1
    H([(a[0], y0, a[2]), (a[1], y0, a[2]), (a[1], y0, a[3]), (a[0], y0, a[3]),
       (b[0], y1, b[2]), (b[1], y1, b[2]), (b[1], y1, b[3]), (b[0], y1, b[3])], c)


def solid(layer, name, x0, x1, y0, y1, z0, z1, c="equip", **meta):
    item(layer, name, (x0, x1, y0, y1), (z0, z1), **meta)
    B(x0, x1, y0, y1, z0, z1, c)


def pad(layer, name, x0, x1, y0, y1, c="pad", z1=0.4, **meta):
    meta.setdefault("register", False)
    z1 += 0.008 * (len(items) % 30)      # unique heights: overlapping pads never share a face
    item(layer, name, (x0, x1, y0, y1), (0, z1), **meta)
    B(x0, x1, y0, y1, 0, z1, c)


def tank(layer, name, cx, cy, r, h, c="tank", **meta):
    """Vertical tank with a cone roof."""
    item(layer, name, (cx - r, cx + r, cy - r, cy + r), (0, h + r * 0.18), shape="circle", **meta)
    V(cx, cy, r, 0, h, c, seg=40 if r > 12 else 24)
    V(cx, cy, r, h, h + r * 0.18, c, r2=r * 0.12, seg=40 if r > 12 else 24)
    V(cx, cy, r + 0.4, 0, 0.8, "concrete")


def building(layer, name, x0, x1, y0, y1, h, c="building", parapet=True, **meta):
    item(layer, name, (x0, x1, y0, y1), (0, h), **meta)
    B(x0, x1, y0, y1, 0, h - (1.5 if parapet else 0), c)
    if parapet:
        t = 0.8
        for bx in [(x0, x1, y0, y0 + t), (x0, x1, y1 - t, y1), (x0, x0 + t, y0, y1), (x1 - t, x1, y0, y1)]:
            B(*bx, h - 1.5, h, c)


def ehouse(layer, name, x0, x1, y0, y1, h, **meta):
    """Prefabricated e-house on a raised skid with a stair and a door landing."""
    item(layer, name, (x0, x1, y0, y1), (0, h), **meta)
    B(x0, x1, y0, y1, 0, 2.5, "concrete")
    B(x0 + 0.3, x1 - 0.3, y0 + 0.3, y1 - 0.3, 2.5, h - 0.6, "ehouse")
    B(x0, x1, y0, y1, h - 0.6, h, "roof")
    # HVAC unit on one end wall
    if x1 - x0 >= y1 - y0:
        B(x1, x1 + 2.5, (y0 + y1) / 2 - 3, (y0 + y1) / 2 + 3, 4, 10, "machine")
    else:
        B((x0 + x1) / 2 - 3, (x0 + x1) / 2 + 3, y1, y1 + 2.5, 4, 10, "machine")


def xfmr(layer, name, x0, x1, y0, y1, h, *, bushing=0.0, fins="x", c="xfmr", hv=None, lv_dx=0.0, **meta):
    """Liquid-filled transformer: tank, radiator banks on two sides,
    conservator, HV bushings (height `bushing` above the tank) and LV throat.
    fins='x' puts radiators on the east and west faces. hv='s' (generator step-up units)
    turns the HV side to the south: bushings in an east-west row along the south edge,
    surge arresters and a take-off gantry facing the switchyard, conservator and the LV
    (isolated-phase bus) throat on the north side, towards the generator."""
    top = h + bushing
    item(layer, name, (x0, x1, y0, y1), (0, top), **meta)
    W, D = x1 - x0, y1 - y0
    B(x0, x1, y0, y1, 0, 0.6, "concrete")  # containment curb
    if fins == "x":
        tx0, tx1, ty0, ty1 = x0 + W * 0.2, x1 - W * 0.2, y0 + D * 0.08, y1 - D * 0.08
    else:
        tx0, tx1, ty0, ty1 = x0 + W * 0.08, x1 - W * 0.08, y0 + D * 0.2, y1 - D * 0.2
    th = h * 0.72
    B(tx0, tx1, ty0, ty1, 0.6, th, c)
    B(tx0 - 0.3, tx1 + 0.3, ty0 - 0.3, ty1 + 0.3, th, th + 0.6, c)  # tank cover
    n = 4 if min(W, D) > 20 else 3
    for k in range(n):
        if fins == "x":
            yy = ty0 + (ty1 - ty0) * (k + 0.5) / n
            for (a, b) in ((x0, tx0 - 0.6), (tx1 + 0.6, x1)):
                B(a, b, yy - 0.5, yy + 0.5, h * 0.12, h * 0.8, "radiator")
        else:
            xx = tx0 + (tx1 - tx0) * (k + 0.5) / n
            for (a, b) in ((y0, ty0 - 0.6), (ty1 + 0.6, y1)):
                B(xx - 0.5, xx + 0.5, a, b, h * 0.12, h * 0.8, "radiator")
    # conservator along the long axis of the tank
    rc = max(1.0, min(W, D) * 0.07)
    zc = th + 0.6 + rc + 1.2
    if hv == "s":
        gsu_hv_south(tx0, tx1, ty0, ty1, th, top, rc, zc, bushing, c, x0, x1, y0, lv_dx)
        return
    if fins == "x":
        R((tx1 - rc, ty0 + 1, zc), (tx1 - rc, ty1 - 1, zc), rc, c)
    else:
        R((tx0 + 1, ty1 - rc, zc), (tx1 - 1, ty1 - rc, zc), rc, c)
    # bushings: three HV on the tank centreline
    if bushing > 0:
        cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
        span = (tx1 - tx0) * 0.3 if fins == "x" else (ty1 - ty0) * 0.3
        for k in (-1, 0, 1):
            px, py = (cx, cy + k * span) if fins == "x" else (cx + k * span, cy)
            R((px, py, th + 0.6), (px, py, top), max(0.6, bushing * 0.06), "insulator", r2=0.35, seg=10)


def gsu_hv_south(tx0, tx1, ty0, ty1, th, top, rc, zc, bushing, c, x0, x1, y0, lv_dx=0.0):
    """GSU arrangement: HV faces the switchyard (south), LV faces the generator (north)."""
    _cur["z"][1] = 45
    cx = (tx0 + tx1) / 2
    B(x0 + .5, x0 + 3.5, y0 + 3, y0 + 7, 0.6, 7, "panel")                               # marshalling cabinet
    R((tx0 + 1, ty1 - rc - .5, zc), (tx1 - 1, ty1 - rc - .5, zc), rc, c)               # conservator, north
    for xs in (tx0 + 3, tx1 - 3):
        B(xs - .3, xs + .3, ty1 - rc - 1, ty1 - rc, th + .6, zc - rc + .2, "steel")
    B(cx + lv_dx - 5, cx + lv_dx + 5, ty1 - 1, ty1 + 2.2, th - 6, th + 1.5, c)         # LV throat to the IPB
    span = (tx1 - tx0) * 0.32
    yb = ty0 + 2.2
    for k in (-1, 0, 1):                                                                 # HV bushings, E-W row
        px = cx + k * span
        R((px, yb, th + 0.6), (px, yb - 1.2, top), max(0.6, bushing * 0.06), "insulator", r2=0.35, seg=10)
        R((px, yb - 1.2, top), (px, yb - 1.2, top + .8), .45, "steel", seg=8)              # terminal
        # surge arrester on a stand in front of each bushing
        ya = y0 + 1.6
        B(px - .4, px + .4, ya - .4, ya + .4, .6, 18, "steel")
        R((px, ya, 18), (px, ya, 27), .45, "insulator", seg=8)
        R((px, yb - 1.2, top + .8), (px, ya, 41.5), .14, "conductor", seg=6)            # dropper to the gantry
    # take-off gantry along the south edge: the 230 kV overhead to the diameter leaves from here
    for xs in (x0 + 1, x1 - 1):
        R((xs, y0 + 1, 0.6), (xs, y0 + 1, 45), 0.7, "steel", r2=0.5, seg=8)
    B(x0 + 0.5, x1 - 0.5, y0 + 0.4, y0 + 1.6, 43, 45, "steel")
    for k in (-1, 0, 1):
        R((cx + k * span, y0 + 1.6, 43), (cx + k * span, y0 + 1.6, 41.5), .3, "insulator", seg=6)


def column_grid(xs, ys, z1, s=1.5, c="steel"):
    for x in xs:
        for y in ys:
            B(x - s, x + s, y - s, y + s, 0, z1, c)


# ---------------------------------------------------------------------------
# SITE (SK-3X1-01)
# ---------------------------------------------------------------------------
L = "SITE"
item(L, "Compound (2,420 x 1,920 ft, 107 acres)", (0, 2420, 0, 1920), (0, 0), register=False,
     info="Compound unchanged since Rev 06; base plant about 43 acres.")
# ground slab built around the stormwater basin (no coplanar faces over the water)
for (gx0, gx1, gy0, gy1) in [(0, 2420, 0, 1430), (0, 2420, 1640, 1920), (0, 40, 1430, 1640), (320, 2420, 1430, 1640)]:
    B(gx0, gx1, gy0, gy1, -0.5, 0, "ground")
for (x0, x1, y0, y1, n) in [
        (0, 2400, 270, 300, "30 ft access road"), (370, 400, 300, 1675, "West spine road"),
        (1460, 1490, 270, 1400, "East spine road"), (370, 1490, 900, 930, "30 ft ring road"),
        (370, 2400, 1370, 1400, "30 ft utilities road"),
        (400, 1500, 1650, 1675, "30 ft road (reserved for CCS utilities)"),
        (1490, 2400, 1650, 1675, "30 ft fuel road (LNG trucks)"),
        (1950, 1975, 1400, 1650, "Fuel-yard link road"), (484, 508, 560, 830, "24 ft lane")]:
    pad(L, n, x0, x1, y0, y1, "road", z1=0.25 + 0.012 * len(items))   # staggered: no coplanar crossings
pad(L, "Removal apron", 400, 480, 410, 560, "road", z1=0.25, sheet="SK-3X1-10",
    info="GT, generator and ST leave the laydown bay through the west door onto a trailer.")
item(L, "Perimeter fence (8 ft)", (0, 2420, 0, 1920), (0, 8), basis="typical", register=False)
for (x0, x1, y0, y1) in [(0, 2420, 0, 0.5), (0, 1465, 1919.5, 1920), (1505, 2420, 1919.5, 1920), (0, 0.5, 0, 270),
                         (0, 0.5, 300, 1920), (2419.5, 2420, 0, 1920)]:
    B(x0, x1, y0, y1, 0, 8, "fence")
# north gate (x 1465-1505): link to the coastal LNG terminal (sheet 15 variant, placed north of the plant);
# gate posts, and the two swing leaves parked open against the fence inside
B(1464, 1465.5, 1918.5, 1920, 0, 10, "steel"); B(1504.5, 1506, 1918.5, 1920, 0, 10, "steel")
B(1446, 1464, 1918.6, 1919, 0, 8, "fence"); B(1506, 1524, 1918.6, 1919, 0, 8, "fence")
solid(L, "Gatehouse", 277, 300, 305, 325, 0, 12, "building", area="F", sheet="SK-3X1-12",
      info="Keadby 3 DCO: gatehouse 6 x 7 x 4 m.")
B(0, 1.5, 270, 272, 0, 10, "steel"); B(0, 1.5, 298, 300, 0, 10, "steel")

# ---------------------------------------------------------------------------
# A POWER BLOCK (SK-3X1-01, -03, -09, -10, -12, -13)
# ---------------------------------------------------------------------------
L = "BASE_POWER_BLOCK"
GX = [630, 790, 950]                    # GT centrelines

# Turbine hall shell: walls in BASE_POWER_BLOCK, roof in HALL_ROOF
item(L, "Common turbine hall", (480, 1100, 370, 560), (0, 101), tag="HALL", area="A",
     sheet="SK-3X1-09",
     info="Main bay y 404-560 with roof EL 98-101 (raised 6 ft in Rev 09 so the ST lift "
     "clears). Bridge-crane runway y 404-556, bridge travel EL 84-96, hook max EL 82. "
     "South inlet gallery y 370-404, roof EL 60, holds GCBs and IPB outside crane coverage.")
t = 1.0
B(480, 1100, 559, 560, 0, 98, "hall")            # north wall
B(1099, 1100, 404, 556, 0, 98, "hall")           # east wall main bay
B(480, 481, 404, 556, 0, 98, "hall")             # west wall main bay
B(480, 1100, 370, 371, 0, 58, "hall")            # gallery south wall
B(480, 481, 370, 404, 0, 58, "hall")             # gallery west wall
B(1099, 1100, 370, 404, 0, 58, "hall")           # gallery east wall
B(480, 1100, 403, 404, 60, 98, "hall")           # clerestory wall above gallery roof
B(479.5, 481.5, 440, 480, 0, 36, "door")         # west door (laydown bay), sheet 10
for i, gx in enumerate(GX):                      # gallery doors, one per bay (sheet 10)
    B(gx - 61, gx - 47, 369.5, 371.5, 0, 16, "door")
_part(kind="prism", min=[480, 404, 98], max=[1100, 560, 101], ridge="x", color="roof", layer="HALL_ROOF")
_part(kind="box", min=[480, 370, 58], max=[1100, 404, 60], color="roof", layer="HALL_ROOF")
# runway columns and crane rails (sheet 09/10)
for x in range(482, 1101, 44):
    for y in (404, 556):
        B(x - 1.2, x + 1.2, y - 1.2, y + 1.2, 0, 97, "steel")
for y in (404, 556):
    B(482, 1098, y - 1.5, y + 1.5, 82, 84, "steel")
item(L, "Bridge crane (parked over laydown bay)", (486, 540, 404, 556), (84, 96), tag="CRANE",
     area="A", sheet="SK-3X1-09", basis="typical",
     info="Covers all bays plus the laydown bay; hook max EL 82. Capacity is vendor data "
     "(unresolved requirement on SK-3X1-09).")
B(505, 511, 404, 556, 86, 96, "crane"); B(525, 531, 404, 556, 86, 96, "crane")
B(503, 533, 404, 410, 84, 96, "crane"); B(503, 533, 550, 556, 84, 96, "crane")
B(510, 526, 476, 486, 88, 95, "crane")  # trolley
R((518, 481, 88), (518, 481, 82.5), 0.4, "steel"); B(515, 521, 478, 484, 81, 82.5, "crane")

item(L, "Laydown bay (floor)", (480, 560, 370, 560), (0, 0.3), area="A", sheet="SK-3X1-10", register=False)
B(481, 560, 371, 559, 0, 0.3, "pad")
item(L, "Turbine deck EL 20", (560, 1100, 404, 556), (0, 20), area="A", sheet="SK-3X1-12",
     info="GTs, generators, ST and their skids sit on the EL 20 deck (Rev 10 correction).")
B(560, 1099, 404, 556, 0, 20, "concrete")

for i, gx in enumerate(GX, start=1):
    dx = gx - 630
    # --- gas turbine: plenum (south, cold end) -> compressor -> combustors -> turbine -> diffuser
    item(L, f"GT{i}: H-class gas turbine (60 Hz)", (617 + dx, 643 + dx, 455, 540), (20, 38),
         tag=f"GT{i}", area="A", basis="vendor", sheet="SK-3X1-12",
         info="Siemens SGT6-8000H class engine about 34 x 14 x 14 ft; 26 x 85 ft including the "
         "inlet plenum and exhaust diffuser. Top EL 38, lifted height 18 ft. Cold-end drive: "
         "inlet plenum and generator at the south end, exhaust north into the HRSG.")
    zc = 29
    B(617 + dx, 643 + dx, 455, 540, 20, 21.5, "steel")
    B(619 + dx, 641 + dx, 455, 468, 21.5, 38, "machine")
    R((gx, 468, zc), (gx, 494, zc), 6.2, "machine", r2=5.0, seg=28)
    R((gx, 494, zc), (gx, 506, zc), 8.5, "machine", seg=28)
    R((gx, 506, zc), (gx, 518, zc), 6.5, "machine", r2=8.0, seg=28)
    R((gx, 518, zc), (gx, 540, zc), 8.0, "machine", r2=9.0, seg=28)
    for k in range(8):                                        # can combustors
        a = 2 * math.pi * k / 8
        cxk, czk = gx + 9.2 * math.cos(a), zc + 9.2 * math.sin(a)
        if 21.5 < czk - 1.1 and czk + 1.1 <= 38:
            R((cxk, 495, czk), (cxk, 505, czk), 1.1, "steel", seg=10)
    # --- generator (south), exhaust duct through the north wall
    item(L, f"GTG-{i}: GT generator", (622 + dx, 638 + dx, 410, 455), (20, 36), tag=f"GTG-{i}",
         area="A", basis="typical", sheet="SK-3X1-04",
         info="21 kV (assumed); typical H2-cooled 350-450 MVA; 16 x 45 ft. Lifted height 16 ft.")
    B(622 + dx, 638 + dx, 410, 455, 20, 21.5, "steel")
    R((gx, 414, 28.5), (gx, 452, 28.5), 7.0, "machine", seg=28)
    R((gx, 410.5, 28.5), (gx, 414, 28.5), 3.5, "machine", seg=16)
    B(gx - 7.5, gx + 7.5, 426, 440, 21.5, 36, "machine")      # terminal / cooler housing
    item(L, f"GT{i} exhaust duct to HRSG {i}", (619 + dx, 641 + dx, 540, 560), (21, 38), area="A",
         register=False)
    B(620 + dx, 640 + dx, 540, 556, 21, 38, "duct")
    # --- GT skids on the deck
    solid(L, f"GT{i} aux: lube oil, hydraulics, enclosure fans", 661 + dx, 675 + dx, 470, 505, 20, 30,
          "equip", tag=f"GT{i} aux", area="A", sheet="SK-3X1-03",
          info=f"MCC-GT{i} in R1 (route LV-GTAUX-{i}).")
    solid(L, f"FS-GT{i}: CO2 fire-suppression skid", 662 + dx, 674 + dx, 510, 534, 20, 28, "red",
          tag=f"FS-GT{i}", area="A", sheet="SK-3X1-03",
          info="Detection, release and interlocks; 480 V + 24 V DC; hall control tray.")
    solid(L, f"WASH-GT{i}: compressor water-wash skid", 584 + dx, 596 + dx, 475, 495, 20, 27,
          "equip", tag=f"WASH-GT{i}", area="A", sheet="SK-3X1-03")
    solid(L, f"GT{i} removable plenum spool", 643 + dx, 658 + dx, 440, 466, 23, 37, "duct",
          tag=f"SPOOL-{i}", area="A", sheet="SK-3X1-10",
          info="Removed before any GT lift; touches the GT lift column by design.")

    # --- HRSG: casing, drums, stair, inlet transition, outlet breeching
    item(L, f"HRSG {i} + SCR (3P reheat, horizontal)", (595 + dx, 665 + dx, 600, 760), (0, 100),
         tag=f"HRSG-{i}", area="A", sheet="SK-3X1-13",
         info="70 x 160 ft, top EL 100 (501G HRSG ~70 ft; largest casing 85 ft). Three-pressure "
         "reheat with SCR. HP, IP and LP drums on the roof steel.")
    B(595 + dx, 665 + dx, 600, 760, 0, 1.5, "concrete")
    # casing about 78 ft tall (the sheet-13 note gives ~70 ft for a 501G HRSG, 85 ft the largest);
    # the drums stand on an open steel frame above it, so the overall top stays at EL 100
    B(597 + dx, 663 + dx, 601, 759, 1.5, 78, "hrsg")
    for yy in range(620, 760, 20):                            # casing stiffener bands
        B(596.5 + dx, 663.5 + dx, yy - 0.6, yy + 0.6, 1.5, 78, "steel")
    B(596.6 + dx, 663.4 + dx, 600.6, 759.4, 78, 79, "roof")    # casing roof (headers below)
    for fx in (600, 630, 660):                                 # open drum-support frame, EL 79-89
        for fy in (650, 670, 690, 710, 724, 740):
            B(fx + dx - .6, fx + dx + .6, fy - .6, fy + .6, 79, 88.6, "steel")
        B(fx + dx - .5, fx + dx + .5, 649, 741, 88.6, 89.2, "steel")
    for fy in (650, 670, 690, 710, 724, 740):
        B(600 + dx, 660 + dx, fy - .4, fy + .4, 88.6, 89.2, "steel")
    for (yy, rr) in ((660, 3.4), (700, 4.6), (732, 3.2)):     # IP, HP, LP drums
        R((600 + dx, yy, 89.2 + rr + 1), (660 + dx, yy, 89.2 + rr + 1), rr, "hrsg", seg=20)
        for sx in (606, 654):
            B(sx + dx - 1, sx + dx + 1, yy - 2, yy + 2, 89.2, 90.2, "steel")
        for side in (-1, 1):                                   # drum walkways
            ya = yy + side * (rr + 1.2)
            B(600 + dx, 660 + dx, min(ya, ya + side * 3), max(ya, ya + side * 3), 88.9, 89.2, "grating")
    for sx in (612, 648):                                     # safety-valve silencers
        R((sx + dx, 715, 89.2), (sx + dx, 715, 100), 1.0, "steel", seg=10)
    B(665 + dx, 673 + dx, 738, 752, 0, 92, "stair")
    item(L, f"HRSG {i} inlet transition duct", (595 + dx, 665 + dx, 560, 600), (2, 96), area="A",
         sheet="SK-3X1-01", info="Expands the GT exhaust into the HRSG face (SK-3X1-09 'exhaust transition').")
    loft_y(560, (620 + dx, 640 + dx, 21, 38), 600, (598 + dx, 662 + dx, 3, 77), "hrsg")
    item(L, f"HRSG {i} outlet breeching", (605 + dx, 655 + dx, 759, 779), (48, 78), area="A",
         register=False)
    # into the stack: the loft ends inside the shell (chord at y 786 is wider than the duct), no corners poke out
    loft_y(759, (605 + dx, 655 + dx, 48, 78), 786, (621 + dx, 639 + dx, 54, 74), "hrsg")
    # --- stack with CEMS platform
    item(L, f"HRSG {i} stack", (619 + dx, 641 + dx, 779, 801), (0, 180), tag=f"STK-{i}", area="A",
         sheet="SK-3X1-13", shape="circle",
         info="22 ft dia x 180 ft (US H-class filings: OCEC 149, Otay Mesa 160, Cosumnes 165, "
         "Smarr 180). CEMS sampling platform at about EL 100.")
    V(gx, 790, 11, 0, 178, "stack", seg=36)
    V(gx, 790, 11.6, 178, 180, "steel", seg=36)
    for zp in (100, 168):
        V(gx, 790, 14.5, zp, zp + 1.2, "grating", seg=36)
    solid(L, f"CEMS shelter, HRSG {i}", 648 + dx, 664 + dx, 806, 820, 0, 12, "ehouse", tag=f"CEMS-{i}",
          area="A", sheet="SK-3X1-03")
    # --- pumps and blowers at the HRSG
    item(L, f"BFP-{i}A/B: boiler feed pumps (13.8 kV DOL)", (675 + dx, 708 + dx, 615, 660), (0, 10),
         tag=f"BFP-{i}", area="A", sheet="SK-3X1-03",
         info=f"Two pumps, 13.8 kV, MV breaker DOL, from R1 SWGR-13.8-{i} via route MV-BFP-{i} "
         "(grade -> +36 at R1 wall, rack tier +36, drop to +10 at HRSG steel).")
    B(675 + dx, 708 + dx, 615, 660, 0, 1, "concrete")
    for yy in (626, 648):
        B(678 + dx, 704 + dx, yy - 4, yy + 4, 1, 3, "steel")
        R((680 + dx, yy, 6), (692 + dx, yy, 6), 3.2, "motor", seg=18)    # motor
        R((693 + dx, yy, 6), (703 + dx, yy, 6), 2.4, "pump", seg=16)     # barrel pump
    item(L, f"SCRB-{i}A/B: SCR dilution-air blowers", (675 + dx, 700 + dx, 705, 725), (0, 8),
         tag=f"SCRB-{i}", area="A", sheet="SK-3X1-03",
         info=f"480 V, MCC starters in R2{'ABC'[i-1]} (LV-SCR-{i}).")
    B(675 + dx, 700 + dx, 705, 725, 0, 1, "concrete")
    for yy in (710, 720):
        R((678 + dx, yy, 4), (686 + dx, yy, 4), 2.2, "motor", seg=14)
        B(687 + dx, 697 + dx, yy - 3.5, yy + 3.5, 1, 8, "equip")

# Steam turbine train
item(L, "ST: steam turbine (HP/IP + LP), ACC plant", (1020, 1080, 460, 552), (20, 46), tag="ST",
     area="A", basis="typical", sheet="SK-3X1-12",
     info="Top EL 46; lifted as casing halves / rotors (14 ft), not assembled. LP hoods govern "
     "width. Side exhaust east to the ACC through the 26 ft ST exhaust duct.")
B(1020, 1080, 460, 552, 20, 21.5, "steel")
R((1050, 552, 32), (1050, 518, 32), 7.0, "machine", r2=10.5, seg=28)
B(1024, 1076, 462, 516, 21.5, 40, "machine")
P(1024, 1076, 462, 516, 40, 46, "machine", ridge="y")
item(L, "STG: steam-turbine generator", (1041, 1059, 410, 460), (20, 38), tag="STG", area="A",
     basis="typical", sheet="SK-3X1-04", info="21 kV (assumed), 550-650 MVA typical.")
B(1041, 1059, 410, 460, 20, 21.5, "steel")
R((1050, 414, 29.5), (1050, 458, 29.5), 8.2, "machine", seg=28)
B(1042, 1058, 428, 444, 21.5, 38, "machine")
solid(L, "ST aux: lube oil, turning gear, EHC", 1082, 1098, 470, 505, 20, 30, "equip", tag="ST aux",
      area="A", sheet="SK-3X1-03", info="480 V MCC in R3 (LV-ST).")
item(L, "ST exhaust duct (26 ft)", (1080, 1130, 487, 513), (31, 57), tag="ST exhaust", area="A",
     sheet="SK-3X1-12", info="ST exhaust duct set to 26 ft diameter (Rev 10); side exhaust from the LP "
     "casing east through the hall wall, above the ST aux skid.")
B(1076, 1080, 489, 511, 31, 46, "duct")
R((1080, 500, 44), (1130, 500, 44), 13, "duct", seg=32)
item(L, "ACC main steam duct, manifold and street risers", (1130, 1450, 359, 513), (31, 125), area="B",
     sheet="SK-3X1-13", basis="typical",
     info="Main duct continues under the fan deck (clear of the 40 ft column grid), turns south to a "
     "manifold along the ACC south edge, and rises at each street end into the street header, so "
     "no duct passes through the fans. Hunterstown main duct 23 ft; arrangement typical.")
R((1130, 500, 44), (1150, 500, 44), 13, "duct", seg=32)
R((1150, 500, 44), (1150, 386, 44), 13, "duct", seg=32)
R((1150, 386, 44), (1150, 372, 44), 13, "duct", r2=6, seg=32)
for yy in (420, 460):
    B(1146, 1154, yy - 3, yy + 3, 0, 31, "steel")

# ---------------------------------------------------------------------------
# Filter houses and inlet ducts (SK-3X1-09, -10)
# ---------------------------------------------------------------------------
L = "BASE_INLET_AIR"
for i, gx in enumerate(GX, start=1):
    dx = gx - 630
    item(L, f"FH-{i}: GT inlet filter house on its own frame", (588 + dx, 672 + dx, 366, 403),
         (0, 135), tag=f"FH-{i}", area="A", sheet="SK-3X1-09",
         info="Casing EL 100-135 on six columns: three outside the gallery wall and three on the "
         "runway column line, so nothing cantilevers over the main roof. Filter elements "
         "change from the south platform at EL 108 via the stair tower; a hoist beam lowers "
         "them to a landing with truck access.")
    B(588 + dx, 672 + dx, 367, 403, 104, 135, "filter")
    B(588 + dx, 672 + dx, 367, 403, 100, 104, "steel")
    for k in range(3):                                        # weather hoods, south face
        z0 = 108 + 9 * k
        H([(589 + dx, 367, z0 + 7), (671 + dx, 367, z0 + 7), (671 + dx, 367, z0 + 8), (589 + dx, 367, z0 + 8),
           (589 + dx, 363, z0), (671 + dx, 363, z0), (671 + dx, 363, z0 + 1), (589 + dx, 363, z0 + 1)], "filter")
    for cx in (590, 630, 670):
        for cy in (367.5, 401.5):
            B(cx + dx - 1.5, cx + dx + 1.5, cy - 1.5, cy + 1.5, 0, 100, "steel")
    B(588 + dx, 672 + dx, 356, 366, 107, 108, "grating")      # platform EL 108
    B(588 + dx, 672 + dx, 356, 356.4, 108, 111.5, "steel")    # handrail
    B(600 + dx, 700 + dx, 352.5, 354, 114, 115.5, "steel")    # hoist beam (to landing, east)
    item(L, f"FH-{i} stair tower", (678 + dx, 688 + dx, 352, 368), (0, 111), area="A", sheet="SK-3X1-10",
         info="Stair to the filter platform at EL 108 (sheet 10).")
    B(678 + dx, 688 + dx, 352, 368, 0, 111, "stair")
    B(672 + dx, 678 + dx, 356, 362, 107, 108, "grating")
    item(L, f"FH-{i} hoist landing + truck access", (692 + dx, 707 + dx, 300, 366), (0, 0.5), area="A",
         sheet="SK-3X1-10", info="Filter elements lowered by the hoist beam to this landing; truck access "
         "from the access road.")
    B(692 + dx, 707 + dx, 338, 366, 0, 0.5, "amber")
    B(692 + dx, 707 + dx, 300, 338, 0, 0.3, "road")
    item(L, f"Gallery door apron, bay {i}", (568 + dx, 584 + dx, 300, 366), (0, 0.3), area="A",
         sheet="SK-3X1-10", info="Forklift / mobile-crane apron from the access road to the gallery door; "
         "GCB and IPB sections leave on the gallery monorail.")
    B(568 + dx, 584 + dx, 300, 366, 0, 0.3, "road")
    item(L, f"GT{i} inlet duct (drop + horizontal EL 23-37)", (658 + dx, 694 + dx, 372, 466), (23, 104),
         area="A", sheet="SK-3X1-09", tag=f"INL-{i}",
         info="Drop from the filter house through the gallery roof, then horizontal north at "
         "EL 23-37, 28-64 ft east of the GT centreline, into the plenum spool. It keeps 6 ft "
         "under the GT travel band and 4 ft under the generator band.")
    H([(644 + dx, 368, 104), (672 + dx, 368, 104), (672 + dx, 400, 104), (644 + dx, 400, 104),
       (660 + dx, 372, 96), (692 + dx, 372, 96), (692 + dx, 400, 96), (660 + dx, 400, 96)], "filter")
    B(660 + dx, 692 + dx, 372, 400, 37, 96, "filter")
    B(658 + dx, 694 + dx, 372, 466, 23, 37, "filter")

# ---------------------------------------------------------------------------
# B ACC: 80 cells = 8 streets x 10 cells of 40 ft (SK-3X1-01, -03, -05, -13)
# ---------------------------------------------------------------------------
L = "BASE_POWER_BLOCK"
item(L, "Air-cooled condenser, 80 cells (steam-cycle heat rejection)", (1130, 1450, 380, 780), (0, 125),
     tag="ACC", area="B", sheet="SK-3X1-13",
     info="8 streets x 10 cells of 40 ft. Fan deck EL 90, top of steel 125 ft (Hunterstown ~120; "
     "Sewaren, Bridgeport ~125). Fans ACC-F01..F80, 480 V VFDs in R4, fan-bridge tray at EL +90; "
     "VFD-ACC route ~633 ft to the farthest fan (verify drive-cable limits).")
B(1130, 1450, 380, 780, 88, 92, "acc")
for s in range(8):
    x0 = 1130 + 40 * s
    P(x0 + 2, x0 + 38, 382, 778, 92, 118.5, "bundle", ridge="y")
    R((x0 + 20, 382, 121.5), (x0 + 20, 778, 121.5), 3.5, "duct", seg=16)    # street steam header
for (x0, x1, y0, y1, zt) in [(1130, 1450, 379, 380, 117.5), (1130, 1450, 780, 781, 125),
                             (1129, 1130, 380, 780, 125), (1450, 1451, 380, 780, 125)]:
    B(x0, x1, y0, y1, 92, zt, "windwall")    # south wall stops under the street-header inlets
_mid = [it for it in items if it["name"].startswith("ACC main steam duct")][0]["id"]
_part(kind="rod", a=[1150, 372, 44], b=[1432, 372, 44], r=5, r2=5, color="duct", seg=20, item=_mid,
      layer="BASE_POWER_BLOCK")                                   # manifold along the south edge
for s_ in range(8):
    xs = 1150 + 40 * s_
    _part(kind="rod", a=[xs, 372, 44], b=[xs, 372, 121.5], r=3.5, r2=3.5, color="duct", seg=14, item=_mid,
          layer="BASE_POWER_BLOCK")                               # street riser
    _part(kind="rod", a=[xs, 372, 121.5], b=[xs, 382, 121.5], r=3.5, r2=3.5, color="duct", seg=14, item=_mid,
          layer="BASE_POWER_BLOCK")
for cx in range(1130, 1451, 40):
    for cy in range(380, 781, 40):
        if (cx, cy) != (1130, 500):          # ST exhaust duct entry: transfer girder instead
            B(cx - 2, cx + 2, cy - 2, cy + 2, 0, 88, "steel")
B(1128, 1132, 458, 542, 80, 88, "steel")     # transfer girder over the duct entry
for i in range(8):
    for j in range(10):
        cx, cy = 1150 + 40 * i, 400 + 40 * j
        V(cx, cy, 17, 92, 99, "fan", seg=24)
        V(cx, cy, 16.2, 97, 99.2, "fanhub", r2=2, seg=24)
B(1450, 1459.5, 380, 396, 0, 92, "stair"); B(1450, 1459.5, 764, 780, 0, 92, "stair")   # clear of the east spine road (x 1460)

# ---------------------------------------------------------------------------
# ELECTRICAL (SK-3X1-03, -04, -05)
# ---------------------------------------------------------------------------
L = "BASE_ELECTRICAL"
for i, gx in enumerate(GX, start=1):
    dx = gx - 630
    xfmr(L, f"GSU-{i}: 21/230 kV generator step-up transformer", 610 + dx, 650 + dx, 325, 365, 24,
         bushing=14, fins="x", hv="s", lv_dx=7, tag=f"GSU-{i}", area="A", sheet="SK-3X1-04",
         info="21/230 kV (assumed), 350-450 MVA typical; bushings add 12-15 ft. HV connects by "
         f"230 kV overhead to diameter D{i}; the unit pulls to the access road for replacement.")
    xfmr(L, f"UAT-{i}: 21/13.8 kV unit auxiliary transformer", 658 + dx, 676 + dx, 330, 352, 16,
         bushing=0, fins="x", tag=f"UAT-{i}", area="A", sheet="SK-3X1-04",
         info="Tapped between GCB and GSU (GSU side of the GCB), so the grid back-feeds 13.8 kV "
         f"bus {i} while GCB-{i} is open for LCI start-up. 40-60 MVA typical.")
    solid(L, f"GCB-{i}: generator circuit breaker", 625 + dx, 635 + dx, 378, 392, 14, 26, "xfmr",
          tag=f"GCB-{i}", area="A", sheet="SK-3X1-10",
          info="On the IPB in the south gallery, outside bridge-crane coverage; gallery monorail "
          "west to a door clear of the filter-house columns.")
    B(625 + dx, 635 + dx, 378, 392, 0, 14, "steel")
    solid(L, f"GSU-{i} firewall", 602 + dx, 604 + dx, 318, 368, 0, 30, "concrete", basis="typical",
          area="A", register=False)
    ehouse(L, f"R2{'ABC'[i-1]}: unit / HRSG electrical e-house (32 x 40 ft)", 552 + dx, 584 + dx,
           612, 652, 14, tag=f"R2{'ABC'[i-1]}", area="A", sheet="SK-3X1-03",
           info=f"Supply SWGR-13.8-{i}. 480 V switchgear, MCC and DCS remote I/O for SCR blowers, "
           "ammonia injection, HRSG valves and drains.")
    xfmr(L, f"T-R2{'ABC'[i-1]}: 13.8/0.48 kV", 555 + dx, 567 + dx, 664, 676, 10, bushing=0,
         area="A", sheet="SK-3X1-04")
xfmr(L, "GSU-ST: 21/230 kV (one ST GSU, baseline)", 1030, 1072, 320, 370, 24, bushing=14, fins="x", hv="s",
     tag="GSU-ST", area="A", sheet="SK-3X1-04",
     info="One ST GSU shown; 2 x 50% is a real option (Okeechobee). No UAT on the ST unit; ST "
     "auxiliaries are fed from the 13.8 kV buses.")
solid(L, "GSU-ST firewall", 1009, 1011, 318, 368, 0, 30, "concrete", basis="typical", area="A", register=False)
solid(L, "GCB-ST", 1046, 1056, 378, 392, 14, 26, "xfmr", tag="GCB-ST", area="A", sheet="SK-3X1-04")
B(1046, 1056, 378, 392, 0, 14, "steel")

# R1 main electrical building: shell split into sheet-11 collections
item(L, "R1: main electrical building (64 x 180 ft)", (410, 474, 600, 780), (0, 24), tag="R1", area="A",
     sheet="SK-3X1-05",
     info="Conventional building 64 x 180 ft (11,520 sq ft), 24 ft high (Wrexham 16 ft, Progress "
     "Power 37 ft). Holds SWGR-13.8-1/2/3, SWGR-4.16-A/B, LC-480-A/B, EMCC, MCC-GT1..3, "
     "MCC-C1/C2, protection & control, DCS, three LCI static starters with dry-type input "
     "transformers, DC/UPS and battery rooms, HVAC. Supply UAT-1/2/3 via DB-S; EDG-1/2 "
     "emergency. The Rev 04 box (120 x 50 ft) could not hold it.")
B(410, 474, 600, 780, 0, 0.6, "concrete")
B(410, 411, 600, 780, 0.6, 23, "building")                     # west wall
B(410, 474, 600, 601, 0.6, 23, "building")                     # south wall
B(410, 474, 779, 780, 0.6, 23, "building")                     # north wall
B(473, 474, 600, 780, 0.6, 23, "building", layer="R1_WALL_E")  # east wall
_part(kind="box", min=[410, 600, 23], max=[474, 780, 24], color="roof", layer="R1_ROOF")
for (x0, x1, y0, y1, h) in [(409.2, 410.8, 628, 632, 8), (409.2, 410.8, 748.5, 751.5, 8),
                            (409.2, 410.8, 764.5, 767.5, 8), (473.2, 474.8, 748.5, 751.5, 8),
                            (473.2, 474.8, 611.5, 614.5, 8), (473.2, 474.8, 627, 633, 10)]:
    _part(kind="box", min=[x0, y0, 0.6], max=[x1, y1, h], color="door",
          layer="R1_WALL_E" if x0 > 470 else "BASE_ELECTRICAL")
xfmr(L, "T4-A: 13.8/4.16 kV station transformer", 410, 430, 786, 802, 14, bushing=0, fins="y",
     tag="T4-A", area="A", sheet="SK-3X1-04")
xfmr(L, "T4-B: 13.8/4.16 kV station transformer", 410, 430, 808, 824, 14, bushing=0, fins="y",
     tag="T4-B", area="A", sheet="SK-3X1-04")
xfmr(L, "LCT-A: 13.8/0.48 kV load-centre transformer", 436, 448, 786, 798, 10, tag="LCT-A", area="A",
     sheet="SK-3X1-04")
xfmr(L, "LCT-B: 13.8/0.48 kV load-centre transformer", 436, 448, 808, 820, 10, tag="LCT-B", area="A",
     sheet="SK-3X1-04")

# R1 interior (SK-3X1-05), collection R1_INTERIOR
L = "R1_INTERIOR"
R1_ROOMS = [
    ("Cable entry / spreading area (DB-S, DB-W entries)", 410, 440, 600, 626),
    ("HVAC mechanical room (AHUs, pressurization)", 444, 474, 600, 626),
    ("Battery room BAT-1 / BAT-2 (vented, eyewash, spill containment)", 410, 438, 752, 780),
    ("DC / UPS room: CHG-1/2, DC-1/2, UPS-A/B, UPS panels", 442, 474, 752, 780),
]
for (n, x0, x1, y0, y1) in R1_ROOMS:
    item(L, "R1 " + n, (x0, x1, y0, y1), (0, 23), area="A", sheet="SK-3X1-05")
    # partitions on the sides that are not exterior walls (full height to the roof)
    if y0 > 600:
        B(x0, x1, y0, y0 + 0.5, 0.6, 23, "partition")
    if y1 < 780:
        B(x0, x1, y1 - 0.5, y1, 0.6, 23, "partition")
    if x0 > 410:
        B(x0, x0 + 0.5, y0, y1, 0.6, 23, "partition")
    if x1 < 474:
        B(x1 - 0.5, x1, y0, y1, 0.6, 23, "partition")
item(L, "R1 AHUs", (447, 471, 604, 622), (0.6, 10), area="A", sheet="SK-3X1-05", basis="typical")
B(447, 459, 604, 622, 0.6, 10, "machine"); B(462, 471, 604, 622, 0.6, 9, "machine")
item(L, "R1 battery racks BAT-1 / BAT-2", (413, 435, 756, 776), (0.6, 5.6), area="A", basis="typical",
     sheet="SK-3X1-05", info="Battery rack (each) 20 x 3 ft, illustrative.")
for yy in (757, 763, 769):
    B(414, 434, yy, yy + 3, 0.6, 5.6, "battery")
item(L, "R1 DC / UPS equipment", (446, 470, 756, 776), (0.6, 7.6), area="A", basis="typical", sheet="SK-3X1-05")
for yy in (757, 766):
    B(446, 470, yy, yy + 3, 0.6, 7.6, "cabinet")
B(426, 426.5, 636, 748, 0.6, 12, "partition")                   # LCI room wall (sheet 05)
CAB = [  # (name, x0, x1, y0, y1, height, colour) from sheet 05; heights typical
    ("SWGR-13.8-1 (11 x 36 in cubicles, 15 kV metal-clad)", 462, 470, 636, 669, 8.0, "swgr"),
    ("SWGR-13.8-2 (11 x 36 in cubicles, 15 kV metal-clad)", 462, 470, 673, 706, 8.0, "swgr"),
    ("SWGR-13.8-3 (11 x 36 in cubicles, 15 kV metal-clad)", 462, 470, 710, 743, 8.0, "swgr"),
    ("SWGR-4.16-A (9 x 36 in cubicles, 5 kV metal-clad)", 447, 454, 636, 663, 7.5, "swgr"),
    ("SWGR-4.16-B (5 kV metal-clad)", 447, 454, 666, 693, 7.5, "swgr"),
    ("LC-480-A (480 V switchgear)", 448, 454, 697, 713, 7.5, "cabinet"),
    ("LC-480-B (480 V switchgear)", 448, 454, 716, 732, 7.5, "cabinet"),
    ("EMCC (emergency MCC)", 452, 454, 735, 746, 7.5, "amber"),
    ("MCC-GT1", 441, 443, 636, 650, 7.5, "cabinet"), ("MCC-GT2", 441, 443, 652, 666, 7.5, "cabinet"),
    ("MCC-GT3", 441, 443, 668, 682, 7.5, "cabinet"), ("MCC-C1", 441, 443, 684, 698, 7.5, "cabinet"),
    ("MCC-C2", 441, 443, 700, 714, 7.5, "cabinet"),
    ("Protection & control panels (22 x 30 in)", 428, 431, 636, 691, 7.5, "panel"),
    ("DCS / network cabinets", 428, 431, 694, 724, 7.5, "panel"),
    ("Telecom / FO", 428, 431, 727, 737, 7.5, "panel"), ("LP / HT panels", 428, 431, 739, 746, 7.5, "amber"),
    ("LCI-1 static starter lineup", 414, 418, 636, 656, 7.5, "swgr"),
    ("TX-LCI-1 dry-type input transformer", 413, 422, 658, 668, 8.0, "xfmr"),
    ("LCI-2 static starter lineup", 414, 418, 672, 692, 7.5, "swgr"),
    ("TX-LCI-2 dry-type input transformer", 413, 422, 694, 704, 8.0, "xfmr"),
    ("LCI-3 static starter lineup", 414, 418, 708, 728, 7.5, "swgr"),
    ("TX-LCI-3 dry-type input transformer", 413, 422, 730, 740, 8.0, "xfmr"),
]
for (n, x0, x1, y0, y1, h, c) in CAB:
    tag = n.split(" ")[0] if n.split(" ")[0].isupper() or "-" in n.split(" ")[0] else ""
    item(L, "R1 " + n, (x0, x1, y0, y1), (0.6, 0.6 + h), tag=tag, area="A", sheet="SK-3X1-05",
         basis="drawing", info="Plan from SK-3X1-05; cabinet height typical.")
    B(x0, x1, y0, y1, 0.6, 0.6 + h, c)
    # section seams on long lineups
    L_len = y1 - y0
    if L_len > 12 and x1 - x0 >= 3:
        n_sec = int(L_len / 3)
        for k in range(1, n_sec):
            yy = y0 + L_len * k / n_sec
            B(x1, x1 + 0.08, yy - 0.05, yy + 0.05, 0.9, 0.6 + h - 0.4, "steel")
item(L, "R1 cable basement below MV rows (hatched on sheet 05)", (444, 471, 634, 747), (-8, 0), area="A",
     sheet="SK-3X1-05", basis="typical", info="Depth illustrative.")
B(444, 471, 634, 747, -8, 0, "basement")
item(L, "R1 overhead LV / control trays", (426, 472, 636, 747), (14, 15), area="A", sheet="SK-3X1-05")
for xx in (438, 456, 468):
    B(xx - 1, xx + 1, 636, 747, 14, 14.4, "pipe")            # galvanised ladder tray with its cables
    B(xx - .8, xx + .8, 636, 747, 14.4, 14.6, "cable_tc")
B(426, 472, 719, 721, 14.6, 15.0, "pipe")
B(426, 472, 719.2, 720.8, 15.0, 15.2, "cable_tc")
item(L, "R1 east-wall tray exits to hall (LCI, GT aux, DC) and tray riser to rack", (470, 478, 638, 748),
     (0, 36), area="A", sheet="SK-3X1-05")
for yy in (640, 650, 660):
    B(472.6, 474, yy - 1.5, yy + 1.5, 18, 20, "pipe")               # wall sleeve (galvanised)
# (the riser up the east wall to the rack trays is built by trays.py as a ladder riser with a wall entry)
B(470, 474, 744, 748, 0.6, 1.2, "concrete")

# R4 ACC VFD e-house, shell + typical interior (SK-3X1-03, -11 view B2)
L = "BASE_ELECTRICAL"
item(L, "R4: ACC electrical (VFD) e-house (60 x 120 ft)", (1135, 1255, 308, 368), (0, 16), tag="R4",
     area="B", sheet="SK-3X1-03",
     info="Supply SWGR-13.8-1/2/2/3 through four outdoor 13.8/0.48 kV transformers. 480 V "
     "switchgear, 92 VFDs (80 ACC fans, 12 aux cooler fans), MCC for the vacuum pumps. "
     "Cable exit toward the ACC column riser.")
B(1135, 1255, 308, 368, 0, 2.5, "concrete")
B(1135, 1136, 308, 368, 2.5, 15.4, "ehouse"); B(1135, 1255, 308, 309, 2.5, 15.4, "ehouse")
B(1135, 1255, 367, 368, 2.5, 15.4, "ehouse")
B(1254, 1255, 308, 368, 2.5, 15.4, "ehouse", layer="R4_WALL_E")
_part(kind="box", min=[1135, 308, 15.4], max=[1255, 368, 16], color="roof", layer="R4_ROOF")
L = "R4_INTERIOR"
for k, yy in enumerate((314, 326, 344, 356)):
    item(L, f"R4 VFD lineup {k+1} (23 drives, fed from T-R4-{k+1})", (1146, 1246, yy, yy + 3), (2.5, 10),
         tag=f"VFD-L{k+1}", area="B", basis="typical", sheet="SK-3X1-03",
         info="92 VFDs total per SK-3X1-03; lineup arrangement typical (sheet 11 view B2).")
    B(1146, 1246, yy, yy + 3, 2.5, 10, "cabinet")
    for s in range(1, 23):
        xx = 1146 + 100 * s / 23
        B(xx - 0.05, xx + 0.05, yy - 0.08, yy, 3, 9.6, "steel")
item(L, "R4 480 V switchgear + vacuum-pump MCC", (1138, 1143, 314, 360), (2.5, 10), area="B",
     basis="typical", sheet="SK-3X1-03")
B(1138, 1143, 314, 360, 2.5, 10, "swgr")
item(L, "R4 cable exit to the ACC column riser", (1250, 1254, 330, 346), (2.5, 14), area="B",
     sheet="SK-3X1-11")
B(1250, 1254, 330, 346, 12, 14, "copper")
L = "BASE_ELECTRICAL"
for k, (x0, y0) in enumerate([(1266, 310), (1292, 310), (1266, 340), (1292, 340)], 1):
    xfmr(L, f"T-R4-{k}: 13.8/0.48 kV", x0, x0 + 12, y0, y0 + 14, 10, fins="y", area="B", sheet="SK-3X1-04")
pad(L, "Spare e-house pad (reserve, as drawn)", 1320, 1445, 308, 368, "pad", z1=0.6, area="B")
ehouse(L, "R3: ST auxiliary electrical e-house (40 x 65 ft)", 1035, 1100, 572, 612, 14, tag="R3", area="A",
       sheet="SK-3X1-03",
       info="Supply SWGR-13.8-2. 480 V switchgear and MCC for ST lube oil, turning gear, EHC and "
       "air compressors.")
xfmr(L, "T-R3: 13.8/0.48 kV", 1053, 1065, 626, 638, 10, area="A", sheet="SK-3X1-04")
for k, (x0, x1) in enumerate([(412, 462), (468, 518)], 1):
    item(L, f"EDG-{k}: 3 MW emergency diesel generator (480 V)", (x0, x1, 338, 350), (0, 22),
         tag=f"EDG-{k}", area="F", basis="vendor", sheet="SK-3X1-12",
         info="Cat 3516C sound-attenuated enclosure 546 x 105 x 167-197 in. Emergency supply "
         "only; ATS / interlocked incomers to LC-480-A/B.")
    B(x0, x1, 338, 350, 0, 1.2, "concrete")
    B(x0 + 1, x1 - 1, 338.5, 349.5, 1.2, 15, "machine")
    R((x1 - 6, 344, 15), (x1 - 6, 344, 22), 0.9, "steel", seg=10)
for (tg, n, x0, x1, y0, y1, h, a) in [
        ("HTP-1", "heat-trace panel (rack)", 569, 575, 852, 855, 7, "A"),
        ("HTP-2", "heat-trace panel (NH3)", 912, 918, 1450, 1453, 7, "E"),
        ("HTP-3", "heat-trace panel (tanks)", 605, 611, 1541, 1544, 7, "E"),
        ("HTP-4", "heat-trace panel (gas)", 1600, 1606, 1444, 1447, 7, "D"),
        ("CPR-1", "cathodic-protection rectifier", 1541, 1545, 1478, 1481, 6, "D"),
        ("CPR-2", "cathodic-protection rectifier", 655, 659, 1578, 1582, 6, "E")]:
    solid(L, f"{tg}: {n}", x0, x1, y0, y1, 0, h, "panel", tag=tg, area=a, sheet="SK-3X1-03")

# ---------------------------------------------------------------------------
# BOP utilities around the hall and ACC; pipe racks
# ---------------------------------------------------------------------------
L = "BASE_UTILITIES"
building(L, "Air compressors AC-A/B/C", 1030, 1100, 700, 745, 14, tag="AC-A/B/C", area="A",
         sheet="SK-3X1-03", info="480 V MCC soft starters in R3 (LV-AIRC).")
building(L, "Chemical feed", 1030, 1100, 760, 781, 12, tag="Chem feed", area="A", sheet="SK-3X1-01")
building(L, "SWAS: steam and water analysis", 1030, 1100, 784, 805, 12, tag="SWAS", area="A", sheet="SK-3X1-01")
for (tg, n, x0, x1, y0, y1, cnt, info) in [
        ("CP-A/B/C", "condensate pumps (4.16 kV)", 1182, 1218, 809, 827, 3,
         "North of the ACC; 4.16 kV MV contactor, SWGR-4.16-A/B (MV-CP)."),
        ("VAC-A/B", "ACC air-removal vacuum pumps", 1235, 1265, 797, 817, 2, "480 V MCC starter in R4 (LV-VAC)."),
        ("CCW-A/B", "closed cooling water pumps", 1283, 1313, 807, 827, 2, "4.16 kV MV contactor (MV-CCW).")]:
    item(L, f"{tg}: {n}", (x0, x1, y0, y1), (0, 8), tag=tg, area="B", sheet="SK-3X1-03", info=info)
    B(x0, x1, y0, y1, 0, 1, "concrete")
    for k in range(cnt):
        xx = x0 + (x1 - x0) * (k + 0.5) / cnt
        R((xx, y0 + 2, 5), (xx, y0 + 8, 5), 2.2, "motor", seg=14)
        R((xx, y0 + 8.5, 5), (xx, y1 - 2, 5), 2.6, "pump", seg=14)
item(L, "Aux dry coolers AUXC-F01..12 (closed cooling water)", (1326, 1446, 792, 828), (0, 18), tag="AUXC",
     area="B", sheet="SK-3X1-03", info="12 fans with 480 V VFDs in R4; heat rejection for the closed "
     "cooling-water loop.")
column_grid((1328, 1386, 1444), (794, 826), 10, s=1)
B(1326, 1446, 792, 828, 10, 15, "bundle")
for k in range(6):
    for r_ in (0, 1):
        V(1336 + 20 * k, 801 + 18 * r_, 8, 15, 18, "fan", seg=18)
tank(L, "Condensate storage tank", 1155, 812, 14, 30, area="B")
for (x0, x1, y0, y1, n) in [(460, 1300, 826, 850, "Main E-W pipe and cable rack (24 ft)"),
                            (1108, 1128, 570, 850, "N-S pipe rack along the ACC")]:
    item(L, n, (x0, x1, y0, y1), (0, 42), area="A", sheet="SK-3X1-12",
         info="Widened from 16 to 24 ft in Rev 10. Process tiers EL 24/30, MV tray tier EL +36, "
         "control tray EL +42.")
    if x1 - x0 > y1 - y0:
        for x in range(int(x0), int(x1) + 1, 25):
            B(x - 0.8, x + 0.8, y0 + 1.5, y0 + 3.1, 0, 42, "steel"); B(x - 0.8, x + 0.8, y1 - 3.1, y1 - 1.5, 0, 42, "steel")
            for z in (24, 30, 36, 42):
                B(x - 0.6, x + 0.6, y0, y1, z - 0.8, z, "steel")
        for z in (24, 30, 36, 42):
            B(x0, x1, y0, y0 + 1, z - 0.8, z, "steel"); B(x0, x1, y1 - 1, y1, z - 0.8, z, "steel")
    else:
        for y in range(int(y0), int(y1) + 1, 25):
            B(x0 + 1.5, x0 + 3.1, y - 0.8, y + 0.8, 0, 42, "steel"); B(x1 - 3.1, x1 - 1.5, y - 0.8, y + 0.8, 0, 42, "steel")
            for z in (24, 30, 36, 42):
                B(x0, x1, y - 0.6, y + 0.6, z - 0.8, z, "steel")
        for z in (24, 30, 36, 42):
            B(x0, x0 + 1, y0, y1, z - 0.8, z, "steel"); B(x1 - 1, x1, y0, y1, z - 0.8, z, "steel")

# ---------------------------------------------------------------------------
# C GRID INTERFACE: 230 kV breaker-and-a-half (SK-3X1-01, -04, -13)
# ---------------------------------------------------------------------------
L = "BASE_SWITCHYARD"
pad(L, "230 kV switchyard (gravel)", 400, 1940, 50, 250, "gravel", z1=0.4, area="C", sheet="SK-3X1-04",
    register=True,
    info="Breaker-and-a-half: 5 diameters x 3 breakers = 15 positions, 9 installed in the base plant. D1 "
    "GTG-1 + Line 1, D2 GTG-2 + Line 2, D3 STG + GTG-3; D4 (BESS / modular) and D5 (CCS) are shown built "
    "out with the optional systems, plus D6 (green H2) on a bus extension: 18 breakers. "
    "345 or 500 kV is common at ~1.6 GW (Okeechobee and Greensville use 500 kV).")
PH = (-7, 0, 7)                        # phase spacing, ft
for yb, n in [(237, "230 kV bus 1"), (65, "230 kV bus 2")]:
    item(L, n + " (strain bus, 3 phases)", (530, 1925, yb - 8, yb + 8), (0, 47), tag=n.split()[-2] + n[-1],
         area="C", sheet="SK-3X1-04")
    for ph in PH:
        R((530, yb + ph, 40), (1925, yb + ph, 40), 0.35, "conductor", seg=6)
for x in (530, 1300, 1925):
    for yb in (62, 242):
        item(L, "230 kV dead-end structure (47 ft)", (x - 2, x + 2, yb - 12, yb + 12), (0, 47), area="C",
             sheet="SK-3X1-13", info="230 kV dead-ends 47 ft (CPUC Jefferson-Martin); 132 kV yards 33-37 ft.",
             register=False)
        for yy in (yb - 11, yb + 11):
            R((x, yy, 0), (x, yy, 47), 1.1, "steel", r2=0.7, seg=8)
        B(x - 0.8, x + 0.8, yb - 12, yb + 12, 43, 45, "steel")
        for ph in PH:
            R((x, yb + ph, 43), (x, yb + ph, 40.5), 0.3, "insulator", seg=6)


def diameter(d, x, installed=True, lines=(), buildout=None):
    """One breaker-and-a-half diameter. buildout: circuits text for the D4-D6 build-out, which
    is drawn complete on the SWYD_FUTURE layer (shown with the optional systems)."""
    L = "BASE_SWITCHYARD" if installed and not buildout else "SWYD_FUTURE"
    c = "xfmr" if installed else "future"
    for k, y in enumerate((110, 150, 190), 1):
        item(L, f"{d} 230 kV breaker {k}" + ("" if installed else " (position, not installed)")
             + (" (build-out)" if buildout else ""),
             (x - 8, x + 8, y - 8, y + 8), (0, 28 if installed else 1), tag=f"{d}-CB{k}", area="C",
             sheet="SK-3X1-04", info=("Dead-tank SF6 breaker (typical)." if installed else
             "Future position; breakers not installed.") + (f" Build-out of the future diameter: {buildout}."
                                                             if buildout else ""))
        B(x - 8, x + 8, y - 8, y + 8, 0, 1, "concrete")
        if not installed:
            continue
        B(x - 7, x + 7, y - 3, y + 3, 1, 6, "steel")
        R((x - 7, y, 8.5), (x + 7, y, 8.5), 2.6, c, seg=16)
        for ph in PH:                                                # bushings, two per phase
            for s in (-1, 1):
                R((x + ph, y + 1.2 * s, 10), (x + ph, y + 4 * s, 26), 0.55, "insulator", r2=0.35, seg=8)
    if not installed:
        return
    item(L, f"{d} disconnect switches, supports and conductors" + (" (build-out)" if buildout else ""),
         (x - 10, x + 10, 65, 237), (0, 40),
         area="C", sheet="SK-3X1-04", register=False)
    for y in (90, 130, 170, 210):                                    # switch / support stands
        B(x - 9, x + 9, y - 0.8, y + 0.8, 14, 15.5, "steel")
        for xs in (x - 9, x + 9):
            R((xs, y, 0), (xs, y, 14), 0.6, "steel", seg=6)
        for ph in PH:
            R((x + ph, y, 15.5), (x + ph, y, 24), 0.4, "insulator", seg=8)
    for ph in PH:
        R((x + ph, 65, 40), (x + ph, 65, 26), 0.25, "conductor", seg=6)
        R((x + ph, 237, 40), (x + ph, 237, 26), 0.25, "conductor", seg=6)
        R((x + ph, 65, 26), (x + ph, 237, 26), 0.3, "conductor", seg=6)
    for y in (130, 170):                                             # take-off gantries
        for xs in (x - 36, x + 36):
            R((xs, y, 0), (xs, y, 45), 1.0, "steel", r2=0.7, seg=8)
        B(x - 36, x + 36, y - 0.8, y + 0.8, 43, 45, "steel")


diameter("D1", 700); diameter("D2", 900); diameter("D3", 1100)
# complete yard: the D4 / D5 future diameters built out, and D6 (green H2 import) on a bus extension
diameter("D4", 1720, buildout="T-MOD-1/2 modular yard (lower) + BESS MPT (upper)")
diameter("D5", 1860, buildout="CCS 230 kV cable, 2 circuits")
L = "SWYD_FUTURE"
pad(L, "230 kV switchyard extension for D6 (gravel)", 1940, 2060, 50, 250, "gravel", z1=0.4, area="C",
    basis="typical", info="Bus extension and the D6 diameter for the green-hydrogen import (SK-3X1-14).")
for yb, n in [(237, "230 kV bus 1"), (65, "230 kV bus 2")]:
    item(L, n + " extension to D6 (build-out)", (1925, 2045, yb - 8, yb + 8), (0, 47), area="C",
         basis="typical", register=False)
    for ph in PH:
        R((1925, yb + ph, 40), (2045, yb + ph, 40), 0.35, "conductor", seg=6)
for yb in (62, 242):
    item(L, "230 kV dead-end structure (47 ft), D6 extension", (2043, 2047, yb - 12, yb + 12), (0, 47), area="C",
         basis="typical", register=False)
    for yy in (yb - 11, yb + 11):
        R((2045, yy, 0), (2045, yy, 47), 1.1, "steel", r2=0.7, seg=8)
    B(2044.2, 2045.8, yb - 12, yb + 12, 43, 45, "steel")
    for ph in PH:
        R((2045, yb + ph, 43), (2045, yb + ph, 40.5), 0.3, "insulator", seg=6)
diameter("D6", 2010, buildout="green-H2 import cable (T-H2) + spare")
L = "BASE_SWITCHYARD"
for x, n in [(670, "Line 1"), (870, "Line 2")]:
    item(L, f"{n} 230 kV terminal tower", (x - 8, x + 8, 10, 26), (0, 90), tag=n.replace(" ", "-"),
         area="C", basis="typical", sheet="SK-3X1-01", info="Line exits south to the grid.")
    for sx in (-6, 6):
        for sy in (-6, 6):
            R((x + sx, 18 + sy, 0), (x + sx * 0.3, 18 + sy * 0.3, 80), 0.6, "steel", seg=6)
    B(x - 14, x + 14, 17, 19, 68, 70, "steel"); B(x - 10, x + 10, 17, 19, 80, 81.5, "steel")
    R((x, 18, 81.5), (x, 18, 90), 0.4, "steel", seg=6)
ehouse(L, "RH: switchyard relay / control house (52 x 70 ft)", 420, 490, 180, 232, 14, tag="RH", area="C",
       sheet="SK-3X1-03",
       info="Protection, SCADA and communications for the 230 kV yard; 125 V DC and fibre to R1 via DB-S.")
L = "HV_CORRIDOR"
# footprints as drawn; the slabs are trimmed where the strips overlap (overlapping flat pads render black)
for (x0, x1, y0, y1), (sx0, sx1, sy0, sy1) in [
        ((1490, 1540, 237, 830), (1490, 1540, 287, 780)), ((1490, 2120, 780, 830), (1490, 2120, 780, 830)),
        ((2070, 2120, 780, 860), (2070, 2120, 830, 860)), ((1490, 1715, 237, 287), (1490, 1715, 237, 287)),
        ((1665, 1715, 225, 287), (1665, 1715, 225, 237))]:
    z1 = 0.2 + 0.008 * (len(items) % 30)
    item(L, "Reserved 230 kV corridor COR-HMOD", (x0, x1, y0, y1), (0, z1), register=False, sheet="SK-3X1-01",
         area="I")
    B(sx0, sx1, sy0, sy1, 0, z1, "corridor")

# ---------------------------------------------------------------------------
# F CONTROLS / SERVICE and E WATER / UTILITIES
# ---------------------------------------------------------------------------
L = "BASE_SERVICES"
pad(L, "Parking", 40, 320, 60, 240, "road", z1=0.2, area="F")
for k in range(7):
    B(60 + 36 * k, 61 + 36 * k, 80, 220, 0.2, 0.3, "fence")
building(L, "Control / admin building (main control room)", 83, 320, 345, 396, 20, tag="CR", area="F",
         sheet="SK-3X1-12",
         info="51 x 237 x 20 ft (Smarr EA, 7HA.03, 2025). Operator consoles only; DCS cabinets are "
         "distributed in R1, R2A-C, R3 and R4.")
building(L, "Warehouse", 133, 320, 470, 561, 35, area="F", sheet="SK-3X1-12", info="91 x 187 x 35 ft (Smarr EA).")
building(L, "Maintenance building / workshop", 198, 320, 600, 641, 20, area="F", sheet="SK-3X1-12",
         info="41 x 122 x 20 ft (Smarr EA).")
item(L, "Comms tower (lattice)", (250, 275, 445, 465), (0, 120), tag="COMMS", area="F", basis="typical")
for sx in (-5, 5):
    for sy in (-5, 5):
        R((262.5 + sx, 455 + sy, 0), (262.5 + sx * 0.2, 455 + sy * 0.2, 118), 0.4, "steel", seg=6)
R((262.5, 455, 118), (262.5, 455, 120), 0.2, "steel", seg=4)
V(262.5 + 1.5, 455, 1.2, 105, 108, "insulator")
pad(L, "Cable reel yard / outage laydown", 40, 320, 690, 900, "pad", z1=0.3, area="F")
item(L, "Stormwater basin", (40, 320, 1430, 1640), (-8, 0), area="F", info="Detention basin; depth illustrative.")
# a depression, not a slab: four sloped grass banks (rim at grade, toe at EL -8), the floor, and the permanent
# pool at EL -5 (wet detention pond)
for (o0, o1, i1, i0) in (((40, 1430), (320, 1430), (304, 1446), (56, 1446)), ((320, 1430), (320, 1640), (304, 1624), (304, 1446)),
                         ((320, 1640), (40, 1640), (56, 1624), (304, 1624)), ((40, 1640), (40, 1430), (56, 1446), (56, 1624))):
    top = [(o0[0], o0[1], 0), (o1[0], o1[1], 0), (i1[0], i1[1], -8), (i0[0], i0[1], -8)]
    H([(x, y, z - .6) for (x, y, z) in top] + top, "turf")
B(56, 304, 1446, 1624, -8.6, -8, "turf")
B(50, 310, 1440, 1630, -5.4, -5, "water")
L = "BASE_UTILITIES"
building(L, "Water treatment building (incl. R-WT electrical room)", 440, 600, 1445, 1530, 30, tag="R-WT", area="E",
         sheet="SK-3X1-12",
         info="R-WT: 480 V MCC for water treatment, wastewater and the fire-pump jockey pump; supply "
         "SWGR-13.8-2 via DB-W. Height 30 ft (Wrexham 33 ft).")
building(L, "Wastewater treatment", 620, 745, 1445, 1530, 25, area="E")
tank(L, "Raw water tank", 465, 1590, 20, 48, area="E", sheet="SK-3X1-12", info="40 dia x 48 ft class (Smarr EA).")
tank(L, "Fire / service water tank", 530, 1590, 26, 40, area="E", sheet="SK-3X1-12",
     info="52 dia x 40 ft (Smarr service water).")
tank(L, "Demineralised water tank", 600, 1590, 20, 48, area="E", sheet="SK-3X1-12", info="40 dia x 48 ft (Smarr demin).")
building(L, "Fire pump house", 700, 740, 1575, 1605, 16, area="E", basis="typical")
item(L, "Ammonia storage (aqueous, SCR reagent)", (800, 873, 1450, 1492), (0, 20), area="E", sheet="SK-3X1-12",
     info="73 x 42 ft (Smarr EA). Bunded; tank shown horizontal.")
B(800, 873, 1450, 1492, 0, 4, "concrete")
R((808, 1471, 12), (865, 1471, 12), 8, "tank", seg=24)
for xs in (818, 855):
    B(xs - 2, xs + 2, 1464, 1478, 0, 5, "concrete")
item(L, "Auxiliary boiler", (935, 995, 1450, 1540), (0, 70), area="E", basis="typical")
B(935, 995, 1450, 1540, 0, 30, "building")
V(985, 1530, 3, 30, 70, "stack")
item(L, "H2 / CO2 storage (generator gas)", (1080, 1125, 1450, 1510), (0, 10), area="E", basis="typical")
for k in range(4):
    R((1084 + 10 * k, 1453, 4), (1084 + 10 * k, 1507, 4), 3.2, "tank", seg=16)
item(L, "Oil-water separator", (1200, 1226, 1450, 1458), (0, 8), area="E", sheet="SK-3X1-12",
     info="26 x 8 ft (Smarr EA).")
R((1201, 1454, 4), (1225, 1454, 4), 4, "tank", seg=16)

# D FUEL GAS
pad(L, "Plant gas yard (pad)", 1560, 1940, 1430, 1640, "gravel", z1=0.4, area="D", sheet="SK-3X1-12",
    register=True, info="Pad with filter-separators, heater, metering and regulation skids; skids 16 ft "
    "max (Wrexham, Progress Power).")
item(L, "Gas yard filter-separators", (1640, 1680, 1470, 1490), (0, 12), area="D", sheet="SK-3X1-12")
for yy in (1475, 1485):
    R((1643, yy, 6), (1677, yy, 6), 3.5, "tank", seg=16)
item(L, "Fuel-gas performance heater", (1700, 1740, 1470, 1490), (0, 14), area="D", sheet="SK-3X1-12")
R((1703, 1480, 7), (1737, 1480, 7), 6, "tank", seg=18)
solid(L, "Gas metering skid", 1640, 1690, 1520, 1540, 0, 10, "equip", area="D", sheet="SK-3X1-12")
solid(L, "Gas pressure regulation skid", 1710, 1750, 1520, 1540, 0, 12, "equip", area="D", sheet="SK-3X1-12")
solid(L, "Gas yard local control enclosure", 1565, 1585, 1440, 1452, 0, 10, "ehouse", area="D",
      info="Local enclosure, not an e-house.")
solid(L, "CONDITIONAL: fuel-gas compressors", 1800, 1930, 1560, 1630, 0, 20, "conditional", area="D",
      basis="conditional", info="Needed only if pipeline pressure is below the GT requirement.")
pad(L, "CONDITIONAL: backup fuel oil (ULSD) unloading and forwarding area", 1330, 1490, 1430, 1640,
    "conditional", z1=0.4, area="D", basis="conditional", register=True)
tank(L, "CONDITIONAL: ULSD backup fuel-oil tank", 1410, 1580, 45, 40, "conditional", area="D",
     basis="conditional", info="Unloading, tank and forwarding pumps; design-dependent.")

# Pipeline M&R (by pipeline operator) - SK-3X1-14 key 1-9
L = "BASE_UTILITIES"
pad(L, "Pipeline M&R station (by pipeline operator)", 1560, 1800, 1690, 1900, "gravel", z1=0.4, area="K",
    sheet="SK-3X1-14", register=True,
    info="Built by the pipeline operator under a separate contract (Smarr shows it as its own "
    "gas supplier yard).")
item(L, "M&R 1: pig receiver, lateral terminus", (1600, 1612, 1850, 1895), (0, 6), area="K", sheet="SK-3X1-14")
R((1606, 1852, 3.5), (1606, 1893, 3.5), 2.2, "tank", seg=14)
solid(L, "M&R 2: insulating joint + ESD valve", 1602, 1610, 1830, 1838, 0, 5, "amber", area="K", sheet="SK-3X1-14")
item(L, "M&R 3: horizontal filter-separator", (1630, 1665, 1845, 1857), (0, 12), area="K", sheet="SK-3X1-14",
     info="Iron Bank (FERC).")
R((1632, 1851, 6), (1663, 1851, 6), 5, "tank", seg=16)
for k, y in enumerate([1820, 1838, 1856], 1):
    item(L, f"M&R 4: line heater {k} (water bath)", (1690, 1720, y, y + 10), (0, 10), area="K",
         sheet="SK-3X1-14", info="Cove Point: 3 heaters.")
    R((1691, y + 5, 5), (1719, y + 5, 5), 4.6, "tank", seg=16)
solid(L, "M&R 5: ultrasonic meters, 2 runs (custody transfer)", 1620, 1670, 1770, 1786, 0, 6, "equip",
      area="K", sheet="SK-3X1-14")
building(L, "M&R 6: regulation / flow control building", 1700, 1730, 1760, 1790, 16, area="K", sheet="SK-3X1-14",
         parapet=False, info="Cove Point: 30 x 30 ft.")
building(L, "M&R 7: gas quality + measurement building", 1620, 1636, 1730, 1738, 10, area="K",
         sheet="SK-3X1-14", parapet=False, info="Cove Point: 8 x 16 ft.")
tank(L, "M&R 8: condensate tank", 1751, 1861, 6, 10, area="K", sheet="SK-3X1-14")
solid(L, "M&R 9: service panel + UPS, SCADA RTU, CP", 1740, 1756, 1728, 1740, 0, 8, "panel", area="K",
      sheet="SK-3X1-14")
solid(L, "M&R CP test station (as drawn)", 1765, 1769, 1730, 1734, 0, 4, "panel", area="K", sheet="SK-3X1-01")
solid(L, "M&R SCADA antenna mast base (as drawn)", 1775, 1779, 1745, 1748, 0, 4, "panel", area="K",
      sheet="SK-3X1-01")

# ---------------------------------------------------------------------------
# G CARBON CAPTURE (SK-3X1-06), optional
# ---------------------------------------------------------------------------
L = "OPT_CCS"
for i, dx in enumerate([0, 160, 320]):
    t = "ABC"[i]
    gx = 630 + dx
    solid(L, f"DMP-{t}: diverter / bypass damper", 613 + dx, 643 + dx, 808, 826, 40, 62, "duct",
          tag=f"DMP-{t}", area="G", sheet="SK-3X1-06")
    item(L, f"Flue-gas duct, HRSG {i+1} to DCC-{t}", (621 + dx, 639 + dx, 826, 985), (40, 62), area="G",
         sheet="SK-3X1-02", register=False)
    B(621 + dx, 639 + dx, 826, 985, 44, 62, "duct")
    for yy in (870, 930):
        B(624 + dx, 636 + dx, yy - 1, yy + 1, 0, 44, "steel")
    item(L, f"DCC-{t}: direct-contact cooler (quench)", (568 + dx, 608 + dx, 985, 1060), (0, 90),
         tag=f"DCC-{t}", area="G", basis="typical", sheet="SK-3X1-13", info="90 ft; no public value found.")
    B(568 + dx, 608 + dx, 985, 1060, 0, 86, "ccs")
    P(568 + dx, 608 + dx, 985, 1060, 86, 90, "ccs", ridge="y")
    solid(L, f"DCC-{t} pumps + water filter", 568 + dx, 608 + dx, 1066, 1090, 0, 8, "pump", area="G",
          sheet="SK-3X1-06")
    item(L, f"BF-{t}: booster fan (~16 MW)", (615 + dx, 655 + dx, 985, 1035), (0, 30), tag=f"BF-{t}", area="G",
         sheet="SK-3X1-06", info="NZT: 16.4 MWe per H-class train; VFD from the CCS MV building.")
    B(615 + dx, 655 + dx, 985, 1035, 0, 2, "concrete")
    R((635 + dx, 990, 16), (635 + dx, 1012, 16), 13, "motor", seg=28)
    R((635 + dx, 1014, 12), (635 + dx, 1033, 12), 7, "motor", seg=20)
    solid(L, f"Rich/lean pumps, cross exchanger, lean cooler {t}", 660 + dx, 705 + dx, 1040, 1100, 0, 15,
          "equip", area="G", sheet="SK-3X1-06")
    item(L, f"Absorber {t} (62 ft dia x 262 ft, stack to 313 ft)", (599 + dx, 661 + dx, 1189, 1251), (0, 313),
         tag=f"ABS-{t}", area="G", sheet="SK-3X1-13", shape="circle",
         info="Keadby 3 DCO: twin absorbers 19.0 m dia x 80 m AGL (62 x 262 ft); stack to 95.5 m "
         "(313 ft). Water wash, wash pumps and cooler at the top section.")
    V(gx, 1220, 31, 0, 262, "ccs", seg=48)
    V(gx, 1220, 31, 262, 268, "ccs", r2=10, seg=48)
    V(gx, 1220, 9, 268, 313, "stack", seg=24)
    for zp in (60, 130, 200, 250):
        V(gx, 1220, 34, zp, zp + 1.2, "grating", seg=48)
    solid(L, f"Water-wash pumps {t}", 675 + dx, 705 + dx, 1150, 1195, 0, 8, "pump", area="G", sheet="SK-3X1-06")
for i, cx in enumerate([1070, 1120, 1170]):
    t = "ABC"[i]
    item(L, f"STR-{t}: stripper / regenerator (45 ft dia x 207 ft)", (cx - 22.5, cx + 22.5, 1165, 1210),
         (0, 207), tag=f"STR-{t}", area="G", sheet="SK-3X1-13", shape="circle",
         info="Keadby 3 DCO: CO2 stripper 15.0 m dia x 63 m AGL (49 x 207 ft). Reboiler, overhead "
         "condenser and reflux drum per train.")
    V(cx, 1187.5, 22.5, 0, 200, "ccs", seg=40)
    V(cx, 1187.5, 22.5, 200, 207, "ccs", r2=4, seg=40)
    for zp in (70, 150):
        V(cx, 1187.5, 24, zp, zp + 1, "grating", seg=40)
        if i < 2:                                                          # walkway to the next stripper
            B(cx + 22, cx + 28, 1193, 1197, zp + .7, zp + 1, "grating")
    solid(L, f"RB-{t}: reboiler (LP steam from ST extraction)", cx - 20, cx + 20, 1105, 1150, 0, 30, "equip",
          area="G", sheet="SK-3X1-06")
solid(L, "Reclaimer (thermal, intermittent)", 1210, 1260, 1105, 1150, 0, 25, "equip", area="G", sheet="SK-3X1-06")
item(L, "Solvent + NaOH storage", (1210, 1300, 1165, 1225), (0, 32), area="G", sheet="SK-3X1-06")
B(1210, 1300, 1165, 1225, 0, 3, "concrete")
for (cx, cy, r) in ((1228, 1185, 14), (1270, 1185, 14), (1228, 1210, 10), (1285, 1212, 10)):
    V(cx, cy, min(r, 11), 3, 30, "tank", seg=24)
solid(L, "Activated-carbon filter", 1210, 1300, 1235, 1265, 0, 15, "equip", area="G", sheet="SK-3X1-06")
building(L, "CO2 compression 3 x ~19 MW + dehydration", 1310, 1435, 1230, 1345, 35, area="G", sheet="SK-3X1-06",
         info="Three intercooled LP compressors; NZT 19.1 MWe per train.")
solid(L, "CONDITIONAL: HP export compressor + metering", 1360, 1435, 1160, 1220, 0, 20, "conditional",
      area="G", basis="conditional")
ehouse(L, "CCS MV switchgear building (VFDs)", 1060, 1200, 985, 1050, 24, area="G", sheet="SK-3X1-06",
       info="Three trains about 150 MWe (NZT 50.1 MWe per train).")
xfmr(L, "CCS T-1: 230/13.8 kV", 1210, 1250, 985, 1030, 22, bushing=13, fins="x", tag="CCS T-1", area="G",
     sheet="SK-3X1-06", info="Fed from the future D5 diameter by 230 kV underground cable (2 circuits).")
xfmr(L, "CCS T-2: 230/13.8 kV", 1260, 1300, 985, 1030, 22, bushing=13, fins="x", tag="CCS T-2", area="G",
     sheet="SK-3X1-06")
solid(L, "CCS instrument air", 1310, 1350, 985, 1030, 0, 12, "equip", area="G")
ehouse(L, "CCS F&G / control", 1360, 1435, 985, 1030, 16, area="G")
L = "OPT_CCSU"
item(L, "CCS cooling tower (~30 cells): CCS process cooling only", (440, 1190, 1740, 1860), (0, 50),
     tag="CCS-CT", area="G", sheet="SK-3X1-06",
     info="Not the ACC. About 30 cells (NZT 360-390 MWth per train); cell end walls up to 50 ft.")
B(440, 1190, 1740, 1860, 0, 3, "water")
B(440, 1190, 1740, 1860, 3, 40, "tower")
B(440, 1190, 1740, 1860, 40, 42, "grating")
for c in range(1, 15):
    B(440 + 50 * c - 0.5, 440 + 50 * c + 0.5, 1740, 1860, 3, 42, "concrete")
for c in range(15):
    for r_ in range(2):
        V(465 + 50 * c, 1770 + 60 * r_, 18, 42, 50, "tower", r2=19, seg=24)
solid(L, "CCS circulating-water pumps", 1200, 1280, 1760, 1820, 0, 12, "pump", area="G")
ehouse(L, "CT MCC / VFD e-house", 1200, 1290, 1830, 1885, 16, area="G")
building(L, "CCS wastewater (DCC + tower blowdown)", 1300, 1430, 1720, 1800, 25, area="G")

# ---------------------------------------------------------------------------
# H BESS (SK-3X1-07)
# ---------------------------------------------------------------------------
L = "OPT_BESS"
for y in (467, 525, 583, 641, 699):
    for x in range(1565, 1866, 60):
        item(L, "BESS container (ISO 40 ft high cube)", (x, x + 40, y, y + 8), (0, 10.5), area="H", basis="vendor",
             sheet="SK-3X1-12", info="BMS, HVAC and fire suppression. ISO 668: 40 x 8 x 9.5 ft.", register=False)
        B(x, x + 40, y, y + 8, 0, 1, "concrete"); B(x + 0.2, x + 39.8, y, y + 8, 1, 10.5, "bess")
        B(x + 39.8, x + 40.6, y + 1.5, y + 6.5, 3, 8, "machine")
    for x in (1590, 1710, 1830):
        xfmr(L, "BESS PCS / MV skid", x, x + 20, y + 19, y + 27, 9, fins="y", area="H", register=False)
item(L, "BESS blocks: 30 containers + 15 PCS / MV skids", (1565, 1905, 467, 726), (0, 10.5), tag="BESS", area="H",
     sheet="SK-3X1-07", info="Counts, sizes and ratings are assumptions (sheet 02).")
xfmr(L, "BESS main power transformer 34.5/230 kV (to D4 upper)", 1725, 1765, 352, 387, 24, bushing=13,
     tag="BESS MPT", area="H", sheet="SK-3X1-07")
ehouse(L, "34.5 kV collector e-house (arc-resistant)", 1800, 1850, 360, 376, 14, area="H", sheet="SK-3X1-07")
xfmr(L, "BESS auxiliary transformer", 1885, 1905, 360, 372, 8, area="H", sheet="SK-3X1-07")
ehouse(L, "BESS EMS / SCADA and revenue metering", 1885, 1905, 410, 422, 10, area="H", sheet="SK-3X1-07")
solid(L, "CONDITIONAL: grounding transformer", 1565, 1575, 415, 425, 0, 8, "conditional", area="H",
      basis="conditional")

# ---------------------------------------------------------------------------
# I MODULAR GENERATION + BLACK START, PORTABLE PAD (SK-3X1-07, -08)
# ---------------------------------------------------------------------------
L = "OPT_MOD"
item(L, "RICE engine hall (8 engines)", (1570, 1810, 1040, 1130), (0, 40), tag="RICE", area="I", sheet="SK-3X1-07",
     info="Hall for 8 medium-speed 18-cylinder engine-generators (18V50 class, approx.).")
B(1570, 1810, 1040, 1130, 0, 34, "hall"); P(1570, 1810, 1040, 1130, 34, 40, "roof", ridge="x")
for k in range(8):
    x = 1581 + 28 * k
    item(L, f"RICE engine-generator {k+1}", (x, x + 19, 1055, 1115), (0, 20), tag=f"RICE-{k+1}", area="I",
         basis="typical", sheet="SK-3X1-12", register=False)
    B(x, x + 19, 1055, 1115, 0, 3, "concrete"); B(x + 2, x + 17, 1060, 1095, 3, 20, "machine")
    R((x + 9.5, 1096, 11), (x + 9.5, 1112, 11), 7, "machine", seg=20)
    item(L, f"RICE {k+1} SCR + oxidation catalyst and stack", (x - 1, x + 21, 1000, 1040), (0, 90),
         area="I", sheet="SK-3X1-13", register=False, info="Stacks 90 ft (Weston ~65 ft; Humboldt Bay 100 ft).")
    B(x - 1, x + 21, 1000, 1030, 0, 25, "equip")
    V(x + 10, 1037, 3, 0, 90, "stack", seg=14)
    item(L, f"RICE {k+1} radiators (5)", (x - 1, x + 21, 1140, 1216), (0, 14), area="I", register=False)
    for r_ in range(5):
        column_grid((x, x + 20), (1141 + 16 * r_, 1151 + 16 * r_), 4, s=0.5)
        B(x - 1, x + 21, 1140 + 16 * r_, 1152 + 16 * r_, 4, 7, "bundle")
        V(x + 10, 1146 + 16 * r_, 5, 7, 9, "fan", seg=14)
building(L, "Lube oil / starting air / oily water building", 1570, 1690, 1235, 1290, 20, area="I", sheet="SK-3X1-07")
solid(L, "Gas conditioning skid", 1700, 1760, 1250, 1280, 0, 10, "equip", area="I")
tank(L, "Reagent storage", 1810, 1260, 12, 15, area="I")
ehouse(L, "PCM: power control module", 1820, 1860, 1140, 1220, 14, area="I", sheet="SK-3X1-07")
solid(L, "RICE CEMS", 1830, 1846, 1005, 1015, 0, 10, "ehouse", area="I")
for k, x in enumerate([1910, 2110], 1):
    item(L, f"SC-{k}: aeroderivative simple-cycle unit (LM6000 class)", (x, x + 90, 1190, 1220), (0, 35),
         tag=f"SC-{k}", area="I", sheet="SK-3X1-07",
         info="Package with filter house; SCR and CO catalyst with an 80 ft stack (Mira Loma permit), "
         "CEMS, PCM with 15 kV GCB, lube-oil fin-fan cooler, CO2 fire suppression.")
    B(x, x + 70, 1192, 1218, 0, 22, "machine")
    B(x + 70, x + 90, 1190, 1220, 0, 32, "filter")
    B(x - 20, x, 1196, 1214, 8, 26, "duct")
    solid(L, f"SC-{k} SCR / CO catalyst", x + 90, x + 130, 1190, 1220, 0, 35, "equip", area="I", register=False)
    item(L, f"SC-{k} stack (80 ft)", (x + 135.5, x + 148.5, 1198, 1211), (0, 80), area="I", sheet="SK-3X1-13",
         shape="circle", register=False)
    V(x + 142, 1204.5, 6.5, 0, 80, "stack", seg=20)
    ehouse(L, f"SC-{k} PCM + 15 kV GCB", x, x + 40, 1245, 1259, 12, area="I", register=False)
    solid(L, f"SC-{k} lube-oil fin-fan cooler", x + 50, x + 70, 1245, 1259, 0, 10, "bundle", area="I", register=False)
    solid(L, f"CONDITIONAL: SC-{k} inlet chiller / evaporative cooler", x, x + 60, 1135, 1170, 0, 14,
          "conditional", area="I", basis="conditional")
building(L, "Fuel-gas compressors 3 x 100% electric", 2290, 2370, 1180, 1240, 20, area="I", sheet="SK-3X1-07")
tank(L, "Demin tank + trailer pad", 2310, 1280, 20, 30, area="I")
solid(L, "Water-injection skid", 2255, 2275, 1280, 1290, 0, 8, "equip", area="I")
solid(L, "Aqueous ammonia (SC units)", 2240, 2280, 1318, 1330, 0, 10, "tank", area="I")
for yy in (870, 888):
    item(L, "Black-start genset (proposed; requires study)", (1570, 1616, yy, yy + 10), (0, 16), area="I",
         sheet="SK-3X1-07",
         info="Black start is proposed only: needs starting-load, transformer-energisation, "
         "protection and operating-sequence studies (SK-3X1-07).")
    B(1570, 1616, yy, yy + 10, 0, 13, "machine"); R((1610, yy + 5, 13), (1610, yy + 5, 16), 0.8, "steel")
ehouse(L, "BS black-start switchgear", 1625, 1645, 875, 893, 12, area="I", sheet="SK-3X1-07")
solid(L, "CONDITIONAL: BESS black-start alternative", 1655, 1700, 868, 900, 0, 9.5, "conditional", area="I",
      basis="conditional")
ehouse(L, "MOD-EH: 13.8 kV modular collector e-house", 1915, 1995, 880, 900, 16, tag="MOD-EH", area="I",
       sheet="SK-3X1-08")
xfmr(L, "T-MOD-1: 13.8/230 kV", 2045, 2085, 870, 905, 24, bushing=13, tag="T-MOD-1", area="I", sheet="SK-3X1-08")
xfmr(L, "T-MOD-2: 13.8/230 kV", 2105, 2145, 870, 905, 24, bushing=13, tag="T-MOD-2", area="I", sheet="SK-3X1-08")
for k in range(4):
    x = 1995 + 14 * k
    solid(L, f"FC-{k+1}: SOFC module (Bloom ES5 class, 200-300 kW)", x, x + 9, 1070, 1096, 0, 7, "bess",
          area="I", basis="vendor", sheet="SK-3X1-12", info="26 ft 5 in x 8 ft 7 in x 6 ft 9 in.")
solid(L, "Fuel-cell inverter / AC cabinet / desulfurizer", 2060, 2102, 1072, 1096, 0, 8, "ehouse", area="I")
for k in range(3):
    x = 2260 + 14 * k
    solid(L, f"MT-{k+1}: microturbine 1 MW (Capstone C1000 class)", x, x + 8, 1068, 1096, 0, 9.5, "machine",
          area="I", basis="vendor", sheet="SK-3X1-12", info="2438 x 8534 x 2896 mm.")
ehouse(L, "MOD-LV 480 V board + 480 V : 13.8 kV step-up", 2215, 2267, 970, 982, 10, area="I", sheet="SK-3X1-08")
L = "OPT_TMP"
pad(L, "Portable pad lane", 2130, 2370, 620, 640, "road", z1=0.3, area="I")
pad(L, "Portable pad lane", 2346, 2370, 305, 620, "road", z1=0.3, area="I")
solid(L, "Drive-over cable ramp (C-L01 crossing)", 2238, 2252, 617, 643, 0, 1, "amber", area="I", sheet="SK-3X1-08")
for k, y in ((1, 642), (2, 607)):
    solid(L, f"CONT-{k}: containerized genset 13.8 kV (40 ft)", 2000, 2040, y, y + 8, 0, 9.5, "machine",
          tag=f"CONT-{k}", area="I", sheet="SK-3X1-08")
    ehouse(L, f"GSP-{k}: generator breaker / protection", 2042, 2050, y - 2, y + 10, 8, tag=f"GSP-{k}", area="I",
           sheet="SK-3X1-08")
item(L, "MOB-1: trailer genset", (2160, 2213, 695, 704), (0, 13.5), tag="MOB-1", area="I", sheet="SK-3X1-08")
B(2160, 2213, 695, 704, 3, 13.5, "machine")
for xx in (2165, 2200, 2206):
    R((xx, 695.5, 1.8), (xx, 703.5, 1.8), 1.8, "conductor", seg=12)
ehouse(L, "PIC: portable input cabinet", 2255, 2263, 572, 578, 7, tag="PIC", area="I", sheet="SK-3X1-08")
solid(L, "LB: commissioning load bank (trailer)", 2295, 2325, 560, 568, 0, 12, "equip", tag="LB", area="I",
      sheet="SK-3X1-08")
solid(L, "GEN-E: enclosed industrial gas genset 2 MW", 2000, 2046, 460, 470, 0, 15, "machine", tag="GEN-E",
      area="I", basis="vendor", sheet="SK-3X1-08")
solid(L, "GEN-O: open engine-generator skid", 2010, 2036, 420, 428, 0, 8, "machine", tag="GEN-O", area="I",
      sheet="SK-3X1-08")
ehouse(L, "PAD-LV 480 V paralleling switchboard", 2160, 2190, 430, 440, 9, tag="PAD-LV", area="I", sheet="SK-3X1-08")
xfmr(L, "PAD-TX 480 V : 13.8 kV", 2215, 2227, 429, 441, 10, tag="PAD-TX", area="I", sheet="SK-3X1-08")
ehouse(L, "PAD-EH 13.8 kV switchgear e-house", 2160, 2200, 470, 484, 14, tag="PAD-EH", area="I", sheet="SK-3X1-08")
solid(L, "Portable pad gas-conditioning skid", 2310, 2340, 430, 440, 0, 8, "equip", area="I")

# ---------------------------------------------------------------------------
# I+ MODULAR EXPANSION: design change beyond Rev 14 (not on the drawing)
# Adds more of the smaller sheet 07/08 technologies beside the Rev 14 modular
# yard (2 simple-cycle units and 8 RICE engines stay as drawn): two
# trailer-mounted aeroderivatives, six containerized gensets, eight fuel-cell
# modules and three microturbines. Plots were chosen from an occupancy map of the
# verified model with a 10 ft clearance to every part and route; the north-west
# corner stays open as a maintenance laydown.
# ---------------------------------------------------------------------------
L = "OPT_MODX"
DC = dict(area="I", basis="design change", sheet="beyond Rev 14")
# the north-west corner stays open: maintenance laydown for engine and turbine exchanges
pad(L, "Maintenance laydown (gravel)", 45, 405, 1705, 1880, "gravel", z1=0.25, area="I", basis="design change",
    sheet="beyond Rev 14")
# two trailer-mounted aeroderivatives (TM2500 class) south of the portable pad
for k in range(2):
    x, y = 2010 + 120 * k, 335
    item(L, f"TM-{k + 1}: trailer-mounted aeroderivative GT (TM2500 class, ~35 MW)", (x, x + 78, y, y + 55),
         (0, 42), tag=f"TM-{k + 1}", info="Design change: gas turbine + generator trailer, control/aux trailer, "
         "inlet filter on the trailer, exhaust stack.", **DC)
    B(x, x + 64, y + 30, y + 42, 0, 4.5, "steel")                    # main trailer deck
    B(x + 2, x + 60, y + 31, y + 41, 4.5, 16, "machine")             # GT + generator enclosure
    B(x + 44, x + 60, y + 29, y + 43, 16, 24, "filter")              # inlet filter house
    V(x + 8, y + 36, 5, 16, 42, "stack", seg=16)                     # exhaust stack
    B(x + 4, x + 52, y + 8, y + 17, 0, 4.5, "steel")                 # aux / control trailer
    B(x + 6, x + 50, y + 9, y + 16, 4.5, 13, "ehouse")
    for (xx, yy) in ((x + 6, y + 30), (x + 20, y + 30), (x + 54, y + 30), (x + 6, y + 42), (x + 20, y + 42),
                     (x + 54, y + 42), (x + 10, y + 8), (x + 46, y + 8), (x + 10, y + 17), (x + 46, y + 17)):
        R((xx, yy, 1.8), (xx, yy + (1 if yy in (y + 30, y + 8) else -1), 1.8), 1.8, "conductor", seg=12)
    B(x + 66, x + 78, y + 30, y + 42, 0, 9, "cabinet")               # fuel-gas / water skid
# six more containerized gensets with a paralleling e-house
for k in range(6):
    row, i = divmod(k, 3)
    x, y = 1990 + 60 * i, 505 + 55 * row
    solid(L, f"CONT-{k + 3}: containerized gas genset 13.8 kV (40 ft)", x, x + 40, y, y + 8, 0, 9.5, "machine",
          tag=f"CONT-{k + 3}", **DC)
    B(x + 2, x + 38, y + 0.5, y + 7.5, 9.5, 11, "radiator")
    V(x + 12, y + 4, 2.2, 11, 12, "fan", seg=12); V(x + 28, y + 4, 2.2, 11, 12, "fan", seg=12)
    R((x + 36, y + 6, 11), (x + 36, y + 6, 18), 0.8, "stack", seg=10)
ehouse(L, "CONT paralleling switchgear e-house", 2195, 2240, 527, 545, 12, tag="CONT-EH", **DC)
# eight more fuel-cell modules and three more microturbines north of SC-1/SC-2
for k in range(8):
    x = 1900 + 14 * k
    solid(L, f"FC-{k + 5}: SOFC module (Bloom ES5 class, 200-300 kW)", x, x + 9, 1290, 1316, 0, 7, "bess",
          tag=f"FC-{k + 5}", **DC)
ehouse(L, "FC-5..12 inverter / AC cabinet / desulfurizer", 2016, 2056, 1292, 1316, 8, **DC)
for k in range(3):
    x = 2072 + 14 * k
    solid(L, f"MT-{k + 4}: microturbine 1 MW (Capstone C1000 class)", x, x + 8, 1289, 1317, 0, 9.5, "machine",
          tag=f"MT-{k + 4}", **DC)

# ---------------------------------------------------------------------------
# J GT INLET CHILLING (SK-3X1-02), optional
# ---------------------------------------------------------------------------
L = "OPT_IC"
item(L, "Inlet-chilling tower (12 cells): chiller heat rejection", (60, 300, 1240, 1320), (0, 50), area="J",
     basis="typical", sheet="SK-3X1-02")
B(60, 300, 1240, 1320, 0, 3, "water"); B(60, 300, 1240, 1320, 3, 40, "tower"); B(60, 300, 1240, 1320, 40, 42, "grating")
for c in range(6):
    for r_ in range(2):
        V(80 + 40 * c, 1260 + 40 * r_, 15, 42, 50, "tower", r2=16, seg=20)
building(L, "Chillers x6 (water-cooled)", 60, 240, 1040, 1170, 25, area="J", sheet="SK-3X1-02")
solid(L, "CW pumps (inlet chilling)", 250, 305, 1100, 1170, 0, 10, "pump", area="J")
ehouse(L, "Inlet-chilling e-house / transformer", 250, 305, 1040, 1085, 14, area="J")
solid(L, "CHW pumps", 60, 150, 1190, 1225, 0, 10, "pump", area="J")
tank(L, "CONDITIONAL: TES chilled-water tank", 200, 1205, 24, 40, "conditional", area="J", basis="conditional")

# ---------------------------------------------------------------------------
# K LNG SATELLITE and 25 MW GREEN HYDROGEN (SK-3X1-14), adjacent market
# ---------------------------------------------------------------------------
L = "OPT_LNG"
item(L, "LNG 12: spill impoundment (NFPA 59A, to verify)", (2115, 2298, 1732, 1836), (0, 4), area="K",
     sheet="SK-3X1-14")
for bx in [(2115, 2298, 1732, 1733), (2115, 2298, 1835, 1836), (2115, 2116, 1732, 1836), (2297, 2298, 1732, 1836)]:
    B(*bx, 0, 4, "concrete")
B(2116, 2297, 1733, 1835, 0, 0.3, "concrete")
for k in range(8):
    x = 2130 + 20 * k
    item(L, f"LNG 11: tank {k+1}, Chart HS 50000 (51,780 gal)", (x, x + 12.5, 1745, 1822.6), (0, 17.5),
         tag=f"LNG-T{k+1}", area="K", basis="vendor", sheet="SK-3X1-14",
         info="150 in dia x 931 in long. Eight tanks hold 414,000 gal, roughly 9 h of one GT or 3 h of the plant.")
    R((x + 6.25, 1747, 11), (x + 6.25, 1820.6, 11), 6.25, "tank", seg=20)
    for yy in (1760, 1805):
        B(x + 1, x + 11.5, yy - 1.5, yy + 1.5, 0.3, 7, "concrete")
pad(L, "LNG 10: truck unloading bay 1", 1840, 1912, 1690, 1712, "road", z1=0.3, area="K")
pad(L, "LNG 10: truck unloading bay 2", 1925, 1997, 1690, 1712, "road", z1=0.3, area="K")
solid(L, "LNG 10: unloading skid", 1885, 1925, 1716, 1728, 0, 8, "equip", area="K", sheet="SK-3X1-14")
item(L, "LNG 14: vaporizers + glycol heater", (1880, 1990, 1760, 1820), (0, 30), area="K", sheet="SK-3X1-14")
B(1880, 1990, 1760, 1820, 0, 1, "concrete")
for k in range(4):
    B(1886 + 26 * k, 1904 + 26 * k, 1766, 1790, 1, 30, "bundle")
B(1886, 1984, 1798, 1816, 1, 12, "equip")
solid(L, "LNG 13: send-out pumps 2 x 100%", 2030, 2070, 1765, 1795, 0, 8, "pump", area="K", sheet="SK-3X1-14")
solid(L, "LNG 15: boil-off gas compressor", 2030, 2075, 1815, 1845, 0, 12, "motor", area="K", sheet="SK-3X1-14")
solid(L, "LNG 16: send-out metering + pressure control", 1880, 1930, 1840, 1880, 0, 10, "equip", area="K",
      sheet="SK-3X1-14")
solid(L, "LNG impoundment sump pump", 1830, 1860, 1760, 1780, 0, 6, "pump", area="K")
ehouse(L, "LNG 17: LNG e-house (13.8 kV / 480 V)", 1950, 1990, 1850, 1864, 14, area="K", sheet="SK-3X1-14",
       info="15 kV from R1, about 2,690 ft (1,760 shared DB-N + 931 new).")
item(L, "LNG 18: vent stack", (2092, 2098, 1860, 1866), (0, 60), area="K", basis="typical", shape="circle")
V(2095, 1863, 1.5, 0, 60, "stack")
L = "OPT_H2"
item(L, "H2 22: electrolyzer building (5 x HyLYZER-1000 + 5 rectifiers)", (2010, 2170, 1440, 1520), (0, 30),
     tag="H2-EL", area="K", sheet="SK-3X1-14",
     info="25 MW PEM electrolysis, 10.8 t/day, sized like FPL Cavendish at Okeechobee. Hydrogen is "
     "GT fuel made from renewable or surplus power imported through D6, never from the plant's "
     "own output (SK-3X1-16). Group B hazardous area.")
B(2010, 2170, 1440, 1520, 0, 26, "hall"); P(2010, 2170, 1440, 1520, 26, 30, "roof", ridge="x")
for k in range(5):
    x = 2020 + 20 * k
    solid(L, f"PEM electrolyzer {k+1} (HyLYZER-1000)", x, x + 7.5, 1450, 1477.7, 0, 10, "bess", area="K",
          basis="vendor", sheet="SK-3X1-12", register=False, info="Cummins bulletin: 8.4 x 2.3 m.")
    solid(L, f"Rectifier {k+1} (7 MVA)", x, x + 8.2, 1490, 1504.8, 0, 8, "cabinet", area="K", basis="vendor",
          register=False, info="Cummins bulletin: 4.5 x 2.5 m, 7 MVA.")
    xfmr(L, f"H2 21: rectifier transformer {k+1} (7 MVA)", x + 2 * k, x + 2 * k + 12, 1530, 1542, 10, area="K",
         sheet="SK-3X1-14")
solid(L, "H2 24: water purification (RO / EDI)", 2125, 2160, 1455, 1480, 0, 12, "equip", area="K",
      info="9 L per kg H2 (Cummins).")
ehouse(L, "H2 20: 13.8 kV e-house", 2240, 2300, 1440, 1456, 14, area="K", sheet="SK-3X1-14")
xfmr(L, "H2 19: T-H2 230/13.8 kV (about 40 MVA)", 2330, 2370, 1440, 1480, 24, bushing=13, tag="T-H2", area="K",
     sheet="SK-3X1-14", info="230 kV cable from D6, 1,720 ft route along the east fence.")
item(L, "H2 23: dry coolers", (2185, 2225, 1440, 1560), (0, 16), area="K", sheet="SK-3X1-14",
     info="5 x 2,500 L/min (Cummins).")
column_grid((2186, 2224), range(1442, 1561, 39), 8, s=0.6)
B(2185, 2225, 1440, 1560, 8, 12, "bundle")
for k in range(3):
    V(2205, 1460 + 40 * k, 12, 12, 16, "fan", seg=18)
solid(L, "H2 25: H2 dryer / purification", 2240, 2280, 1470, 1490, 0, 12, "equip", area="K")
item(L, "H2 28: N2 purge supply", (2240, 2270, 1500, 1520), (0, 14), area="K")
for k in range(2):
    V(2248 + 14 * k, 1510, 5, 0, 14, "tank")
for k, y in ((1, 1500), (2, 1515)):
    solid(L, f"H2 26: H2 compressor {k} (40 ft ISO)", 2290, 2330, y, y + 8, 0, 9.5, "machine", area="K",
          sheet="SK-3X1-14")
for (x, y) in [(2250, 1560), (2250, 1580), (2300, 1560), (2300, 1580)]:
    item(L, "H2 27: storage tube bank (~40 ft tubes)", (x, x + 40, y, y + 10), (0, 10), area="K", register=False)
    for k in range(3):
        R((x + 1, y + 1.7 + 3.3 * k, 2.5), (x + 39, y + 1.7 + 3.3 * k, 2.5), 1.5, "tank", seg=12)
        R((x + 1, y + 1.7 + 3.3 * k, 6), (x + 39, y + 1.7 + 3.3 * k, 6), 1.5, "tank", seg=12)
item(L, "H2 storage tube banks x4", (2250, 2340, 1560, 1590), (0, 8), tag="H2-ST", area="K", sheet="SK-3X1-14",
     info="Buffer hours between solar production and turbine operation; seasonal storage needs "
     "geology such as salt caverns (SK-3X1-16).")
item(L, "H2 29: vent stack", (2378, 2382, 1595, 1599), (0, 40), area="K", basis="typical", shape="circle")
V(2380, 1597, 1.2, 0, 40, "stack")
solid(L, "H2 30: H2 / gas blending skid (plant gas yard)", 1800, 1840, 1470, 1500, 0, 10, "equip", area="K",
      sheet="SK-3X1-14", info="Blends into the GT-1 fuel branch (5% by volume pilot, as FPL tested one of three units).")

# ---------------------------------------------------------------------------
# L BTM DATA CENTRE (design option beyond Rev 14): ~150 MW campus outside the east fence, beside
# the modular yard, fed behind the meter. One BTM substation supports three operating modes,
# selected by breakers: (1) islanded on the modular yard + BTM BESS; (2) islanded with the
# normally-open 230 kV backup tie to the plant switchyard (D6); (3) grid-parallel, tie closed.
# ---------------------------------------------------------------------------
L = "OPT_DC"
DC = dict(area="L", basis="typical", sheet="design option (BTM data centre)")
pad(L, "BTM data-centre campus (crushed stone)", 2460, 3380, 300, 1380, "pad", z1=0.2, **DC)
for (x0, x1, y0, y1, n) in ((2480, 3360, 380, 410, "south"), (2480, 2510, 380, 1360, "west"),
                            (2730, 3360, 935, 965, "central"), (3330, 3360, 380, 1360, "east"),
                            (2480, 3360, 1330, 1360, "north"), (3000, 3030, 0, 380, "entrance")):
    pad(L, f"Campus road (30 ft), {n}", x0, x1, y0, y1, "road", z1=0.3, **DC)
item(L, "Campus security fence (8 ft) and entrance gate", (2460, 3380, 300, 1380), (0, 8), register=False, **DC)
for (x0, x1, y0, y1) in ((2460, 3000, 300, 300.5), (3030, 3380, 300, 300.5), (2460, 3380, 1379.5, 1380),
                         (2460, 2460.5, 300, 1380), (3379.5, 3380, 300, 1380)):
    B(x0, x1, y0, y1, 0, 8, "fence")
B(2998.5, 3000, 299, 302, 0, 10, "steel"); B(3030, 3031.5, 299, 302, 0, 10, "steel")
building(L, "DC admin / security / NOC building", 3060, 3180, 315, 370, 24, tag="DC-ADM", **DC)
solid(L, "DC gatehouse", 3035, 3052, 318, 338, 0, 11, "building", **DC)
# BTM substation: two 13.8/34.5 kV step-ups from the modular yard, the 230/34.5 kV tie, switchgear
xfmr(L, "BTM-T1: 13.8/34.5 kV step-up from the modular yard, to bus A (90 MVA)", 2530, 2565, 770, 810, 24, tag="BTM-T1", **DC)
xfmr(L, "BTM-T2: 13.8/34.5 kV step-up from the modular yard, to bus B (90 MVA)", 2580, 2615, 770, 810, 24, tag="BTM-T2", **DC)
xfmr(L, "BTM-T3: 13.8/34.5 kV step-up from the modular yard, on the bus-tie section (90 MVA, N+1)", 2530, 2565, 712,
     752, 24, tag="BTM-T3", **DC)
for k, gx in enumerate((2600, 2622)):
    xfmr(L, f"BTM-GT{k + 1}: 34.5 kV zigzag grounding transformer, bus {'AB'[k]}", gx, gx + 12, 906, 918, 9, fins="y",
         tag=f"BTM-GT{k + 1}", **DC)
xfmr(L, "BTM-TIE: 230/34.5 kV backup / grid-parallel tie transformer (180 MVA, carries the full campus)", 2630, 2675, 762, 815, 28, bushing=13,
     tag="BTM-TIE", **DC)
solid(L, "BTM 230 kV tie breaker (dead tank, normally open) + disconnect", 2650, 2668, 822, 845, 0, 22, "steel",
      tag="BTM-52T", **DC)
ehouse(L, "BTM 34.5 kV switchgear: double bus A / B with bus tie, 3-mode transfer scheme, sync check", 2530, 2650, 860,
       900, 18, tag="BTM-SWGR", **DC, info="Bus A: BTM-T1 and the genset GSU-1; bus B: BTM-T2 and GSU-2; BTM-T3 (N+1), the "
       "230 kV tie and the BTM BESS on the bus tie section; zigzag grounding transformers GT1 / GT2 on each bus. Each data hall takes one feeder from bus A (A side) and one from bus B "
       "(B side): 2N. Operating modes by breaker: (1) islanded: T1/T2 mains closed, tie open; (2) islanded with backup: "
       "the 230 kV tie closes on loss of the modular supply (open transition) or for maintenance; (3) grid-parallel: tie "
       "closed with sync check, modular yard and BESS firm the load. Typical, not engineered.")
# BTM BESS for load steps and ride-through (AI training loads swing tens of percent in seconds)
for r_ in range(5):
    y = 440 + 60 * r_
    for k in range(3):
        x = 2530 + 50 * k
        item(L, "BTM BESS container (ISO 40 ft)", (x, x + 40, y, y + 8), (0, 10.5), register=False, **DC)
        B(x, x + 40, y, y + 8, 0, 1, "concrete"); B(x + 0.2, x + 39.8, y, y + 8, 1, 10.5, "bess")
    xfmr(L, "BTM BESS PCS / MV skid", 2675, 2697, y + 14, y + 22, 9, fins="y", register=False, **DC)
item(L, "BTM BESS 40 MW / 80 MWh: 15 containers + 5 PCS / MV skids", (2530, 2697, 440, 698), (0, 10.5), tag="BTM-BESS",
     **DC, info="Absorbs the data-centre load steps so the engines follow slowly; ride-through on mode transfers.")
# data halls (single storey, ~60 MW IT each), fed 2N. Each long face carries one side (A north, B south):
# next to the wall a row of 24 two-tier power skids (UPS modules, Li-ion battery, LV switchboard), then a row of
# 24 x 3.5 MVA 34.5/0.48 kV pad-mount transformers (84 MVA per side: one side carries the whole hall), each
# transformer bus-ducted into its skid; the 24 transformers of a side hang on four 34.5 kV feeder loops of six
for (t, y0, y1) in (("A", 1020, 1280), ("B", 620, 880)):
    building(L, f"Data hall {t}: ~60 MW IT, liquid-cooled racks (closed loop)", 2730, 3290, y0, y1, 45, c="hall",
             tag=f"DH-{t}", **DC, info="Closed-loop liquid cooling to rooftop dry coolers; no evaporative water. "
             "Power 2N: A side from bus A, B side from bus B; each rack row takes one A and one B feed.")
    building(L, f"Data hall {t} gallery: MV / LV distribution, controls, cooling pumps (A and B sides)", 2700, 2728, y0,
             y1, 30, c="ehouse", tag=f"DH-{t}-EG", **DC)
    for side, sk, pm in (("A", (y1 + 2, y1 + 28), (y1 + 30, y1 + 39)), ("B", (y0 - 28, y0 - 2), (y0 - 39, y0 - 30))):
        for k in range(24):
            x = 2742 + 22.5 * k
            item(L, f"Data hall {t} {side}-side power skid {k + 1} (UPS, battery, LV switchboard, two-tier)",
                 (x, x + 18, sk[0], sk[1]), (0, 24), register=False, **DC)
            B(x, x + 18, sk[0], sk[1], 0, 1, "concrete")
            B(x + .3, x + 17.7, sk[0] + .3, sk[1] - .3, 1, 12, "ehouse")
            B(x + .3, x + 17.7, sk[0] + .3, sk[1] - .3, 12.3, 23.4, "ehouse")
            B(x, x + 18, sk[0], sk[1], 23.4, 24, "roof")
            B(x + 2, x + 16, sk[0] + 2, sk[1] - 2, 24, 26, "machine")                         # rooftop HVAC
            xfmr(L, f"Data hall {t} {side}-side pad-mount 34.5/0.48 kV (3.5 MVA)", x + 4.5, x + 13.5, pm[0], pm[1], 8,
                 fins="x", register=False, **DC)
            wy0, wy1 = (sk[1], pm[0]) if side == "A" else (pm[1], sk[0])                     # bus duct to the skid
            B(x + 8, x + 10, wy0, wy1, 5.5, 7, "steel")
            dy0, dy1 = (y1, sk[0]) if side == "A" else (sk[1], y0)                           # skid to the hall wall
            B(x + 8, x + 10, dy0, dy1, 9, 10.5, "steel")
        item(L, f"Data hall {t} {side}-side power skids: 24 x UPS + Li-ion battery + LV switchboard (bus {side})",
             (2742, 3277.5, sk[0], sk[1]), (0, 26), tag=f"DH-{t}-S{side}", **DC)
        item(L, f"Data hall {t} {side}-side MV/LV transformers: 24 x 3.5 MVA 34.5/0.48 kV pad-mount, 4 feeder loops "
             f"(bus {side})", (2742, 3277.5, pm[0], pm[1]), (0, 8), tag=f"DH-{t}-T{side}", **DC)
# backup generation: 36 x 3.6 MW diesel gensets (130 MW: IT load plus the critical cooling pumps, the BESS bridging
# the start), 13.8 kV,
# paralleled in their switchgear and stepped up to 34.5 kV by two GSUs onto bus A and bus B
for row, y in enumerate((440, 500, 560)):
    for k in range(12):
        x = 2780 + 46 * k
        item(L, f"DC backup genset {row * 12 + k + 1} (3.6 MW diesel, 13.8 kV, 48 h belly tank)", (x, x + 40, y, y + 12),
             (0, 14), register=False, **DC)
        B(x, x + 40, y, y + 12, 0, 1.5, "concrete"); B(x + 0.5, x + 39.5, y + .5, y + 11.5, 1.5, 13, "ehouse")
        R((x + 34, y + 6, 13), (x + 34, y + 6, 20), 0.9, "stack", seg=10)
item(L, "DC backup gensets 36 x 3.6 MW (diesel, 130 MW)", (2780, 3326, 440, 572), (0, 20), tag="DC-GEN", **DC)
ehouse(L, "DC genset paralleling switchgear (13.8 kV, two buses)", 2742, 2774, 440, 572, 14, tag="DC-PSG", **DC)
xfmr(L, "DC-GSU-1: genset 13.8/34.5 kV step-up to bus A (75 MVA)", 2702, 2736, 445, 480, 22, tag="DC-GSU-1", **DC)
xfmr(L, "DC-GSU-2: genset 13.8/34.5 kV step-up to bus B (75 MVA)", 2702, 2736, 525, 560, 22, tag="DC-GSU-2", **DC)

# Fuel systems at LOD 3 (gas yard, M&R train, GT gas fuel modules, ULSD area, modular gas skids)
import fuel as _fuel
_fuel.build(dict(item=item, items=items, parts=parts))
import modular as _modular
_modular.build()     # RICE hall and simple-cycle units at LOD 3
import yard as _yard
_yard.build()        # gensets, trailers, fuel cells, microturbines, skids in the modular yard
import hall as _hall
_hall.build()        # turbine hall: GTs, generators, ST, skids, fit-out
import hrsg as _hrsg
_hrsg.build()        # HRSG casing, SCR, drums, steam leads, blowdown
import station as _station
_station.build()     # cycle 2: transformers, e-houses, EDGs
import acc as _acc
_acc.build()         # cycle 3: ACC fans, drives, cable ladders, condensate drains, deck steel

# ---------------------------------------------------------------------------
# Routes: drawn centrelines lifted to their tiers
# ---------------------------------------------------------------------------
ROUTE_STYLE = {
    # type: (elevation ft, width ft, height ft, colour, label, default layer)
    "ipb":          (22, 4, 4, "copper_dark", "Isolated-phase bus + UAT tap (bus duct, not cable)", "ROUTES_BASE"),
    "mv_tray":      (36, 3, 0.8, "copper", "MV power tray (rack tier EL +36)", "ROUTES_BASE"),
    "lv_tray":      (30, 2, 0.6, "copper", "LV / hall power tray", "ROUTES_BASE"),
    "control_tray": (42, 1.5, 0.5, "copper", "Control / instrument tray (EL +42)", "ROUTES_BASE"),
    "duct_bank":    (-2, 4, 2, "ductbank", "Duct bank (underground)", "ROUTES_BASE"),
    "hv_overhead":  (40, 0.8, 0.8, "conductor", "230 kV overhead", "ROUTES_BASE"),
    "steam":        (27, 3, 3, "steam", "Steam", "PROCESS_PIPING"),
    "condensate":   (25, 2, 2, "condensate", "Condensate", "PROCESS_PIPING"),
    "feedwater":    (12, 2, 2, "feedwater", "Feedwater", "PROCESS_PIPING"),
    "ccw":          (24.5, 2, 2, "ccw", "Closed cooling water", "PROCESS_PIPING"),
    "fuel_gas":     (4, 1.5, 1.5, "fuelgas", "Fuel gas", "PROCESS_PIPING"),
    "hv_cable":     (-3, 2, 2, "copper_dark", "230 kV underground cable", None),
    "mvlv_cable":   (-2, 2, 1, "copper", "MV / LV cable (optional systems)", None),
    "cw":           (3, 4, 4, "cw", "Circulating / condenser water", "OPT_CCSU_ROUTES"),
    "chw":          (3, 2, 2, "chw", "Chilled water", "OPT_IC_ROUTES"),
    "hydrogen":     (4, 1, 1, "hydrogen", "Hydrogen", "OPT_H2_ROUTES"),
    "lng":          (4, 1.5, 1.5, "lng", "LNG (cryogenic)", "OPT_LNG_ROUTES"),
    "fuel_oil":     (6.5, 1, 1, "fueloil", "Backup fuel oil (ULSD), conditional", "PROCESS_PIPING"),
    "firewater":    (-4, 1.2, 1.2, "firewater", "Firewater ring main (buried)", "PROCESS_PIPING"),
    "cable_trench": (-1, 3, .6, "concrete", "Control-cable trench (precast, covered)", "ROUTES_BASE"),
    "water":        (3, 1.2, 1.2, "waterline", "Raw / demineralised / service water", "PROCESS_PIPING"),
    "aux_steam":    (12, 1.3, 1.3, "steam", "Auxiliary steam (insulated)", "PROCESS_PIPING"),
    "hmod":         (45, 0.8, 0.8, "conductor", "230 kV overhead tie H-MOD (reserved corridor)", "HV_CORRIDOR"),
}
OPT_AREAS = [  # (layer, x0, x1, y0, y1) from sheet 02
    ("OPT_H2_ROUTES", 1985, 2400, 1410, 1640), ("OPT_LNG_ROUTES", 1815, 2400, 1685, 1910),
    ("OPT_BESS_ROUTES", 1540, 1940, 330, 780), ("OPT_TMP_ROUTES", 1960, 2380, 330, 780),
    ("OPT_MOD_ROUTES", 1540, 2380, 820, 1360), ("OPT_CCS_ROUTES", 420, 1440, 960, 1360),
    ("OPT_CCSU_ROUTES", 420, 1440, 1690, 1900), ("OPT_IC_ROUTES", 40, 320, 960, 1360),
]


def opt_layer(pl, rtype):
    if rtype in ("steam", "flue_duct"):
        return "OPT_CCS_ROUTES"
    for pt in (pl[-1], pl[0]):
        for (lay, x0, x1, y0, y1) in OPT_AREAS:
            if x0 <= pt[0] <= x1 and y0 <= pt[1] <= y1:
                return lay
    return "OPT_MOD_ROUTES"


def clip_out(pl, box):
    """Split a polyline at an axis-aligned rectangle, keeping the parts outside.
    Trays leave R1 through the cable basement and rise at the east wall
    (SK-3X1-05), so their drawn centrelines inside R1 are not tray."""
    x0, x1, y0, y1 = box
    inside = lambda p: x0 < p[0] < x1 and y0 < p[1] < y1
    out, cur = [], []
    for a, b in zip(pl, pl[1:]):
        ia, ib = inside(a), inside(b)
        if ia and ib:
            continue
        if not ia and not ib:
            cur = cur or [a]
            cur.append(b)
            continue
        # one end inside: clip to the rectangle edge (segments are orthogonal)
        o, i = (a, b) if not ia else (b, a)
        if o[0] == i[0]:
            e = [o[0], y0 if o[1] < y0 else y1]
        else:
            e = [x0 if o[0] < x0 else x1, o[1]]
        if not ia:
            cur = cur or [a]
            cur.append(e)
            out.append(cur); cur = []
        else:
            cur = [e, b]
    if len(cur) > 1:
        out.append(cur)
    return out


R1_BOX = (410, 476, 600, 780)
routes = []
for fname, src, optional in [("routes_base.json", "SK-3X1-01", False), ("routes_optional.json", "SK-3X1-02", True)]:
    data = json.load(open(os.path.join(HERE, fname)))
    for rtype, polys in data.items():
        if rtype == "flue_duct":
            continue  # modelled as the firewall and flue-duct items
        z, w, h, colour, label, layer = ROUTE_STYLE[rtype]
        pieces = []
        for pl in polys:
            pieces += clip_out(pl, R1_BOX) if rtype in ("mv_tray", "lv_tray", "control_tray") else [pl]
        for pl in pieces:
            if len(pl) < 2 or sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pl, pl[1:])) < 3:
                continue
            lay = (opt_layer(pl, rtype) if optional else layer) if not layer or optional else layer
            if optional and rtype in ("cw", "chw", "hydrogen", "lng"):
                lay = layer
            routes.append(dict(type=rtype, layer=lay, label=label, z=z, w=w, h=h, color=colour,
                               points=pl, sheet=src))
# H-MOD 230 kV overhead tie in the reserved corridor COR-HMOD (SK-3X1-08)
HMOD = [[2095, 870], [2095, 805], [1515, 805], [1515, 262], [1690, 262], [1690, 237], [1720, 130]]
routes.append(dict(type="hmod", layer="HV_CORRIDOR", label=ROUTE_STYLE["hmod"][4], z=45, w=0.8, h=0.8,
                   color="conductor", points=HMOD, sheet="SK-3X1-08"))
# ---------------------------------------------------------------------------
# Connections the drawing leaves open (site audit, plant/audit.py): typical routing
# ---------------------------------------------------------------------------
def add_route(rtype, points, layer=None, sheet="typical (site audit)"):
    z, w, h, colour, label, default = ROUTE_STYLE[rtype]
    routes.append(dict(type=rtype, layer=layer or default, label=label, z=z, w=w, h=h, color=colour,
                       points=[[float(x), float(y)] for x, y in points], sheet=sheet))


# GT fuel gas: the drawn header stops over HRSG 1 (x 600); it now ends at the GT1 branch and
# each GT gets a branch between the HRSGs to its fuel / auxiliary skid (clear of the BFPs and the ST)
for r in routes:
    if r["type"] == "fuel_gas" and r["points"][-1] == [600.0, 885.0]:
        r["points"][-1] = [715.0, 885.0]
# (they rise at the hall's north wall to the GT gas fuel modules GFM-1..3 on the deck)
for k, xb in enumerate((715, 875, 1034)):
    add_route("fuel_gas", [(xb, 885), (xb, 570), (686 + 160 * k, 570), (686 + 160 * k, 559)], layer="PROCESS_PIPING")
# conditional backup fuel oil: forwarding pumps -> GT liquid-fuel modules, one tier above the gas
add_route("fuel_oil", [(1475, 1465), (1505, 1465), (1505, 889), (711, 889)], sheet="typical (fuel detail)")
for k, xb in enumerate((715, 875, 1034)):
    add_route("fuel_oil", [(xb - 4, 889), (xb - 4, 574), (682 + 160 * k, 574), (682 + 160 * k, 559)],
              sheet="typical (fuel detail)")
# IP feedwater supply / return between HRSG 3 and the fuel-gas performance heater
add_route("feedwater", [(985, 740), (1000, 740), (1000, 877), (1518, 877), (1518, 1493), (1712, 1493)],
          sheet="typical (fuel detail)")
add_route("feedwater", [(985, 748), (1004, 748), (1004, 873), (1522, 873), (1522, 1497), (1729, 1497),
                        (1729, 1493)], sheet="typical (fuel detail)")
# CCS circulating water: the drawn line stops on the utilities road; carry it to absorber B's foot
for r in routes:
    if r["type"] == "cw" and r["points"][-1] == [770.0, 1360.0]:
        r["points"].append([770.0, 1255.0])
# modular expansion (OPT_MODX): MV cables to the portable-pad and modular collectors, gas stubs
MX = "OPT_MODX_ROUTES"
for row, y in ((0, 505), (1, 560)):                       # CONT-3..8 -> CONT-EH (paralleling e-house)
    ys = y - 4 if row == 0 else y + 12
    add_route("mvlv_cable", [(2010, y), (2010, ys), (2190, ys), (2190, 536), (2195, 536)], MX)
add_route("mvlv_cable", [(2263, 575), (2290, 575), (2290, 564), (2295, 564)], "OPT_TMP_ROUTES",
          sheet="typical (portable pad)")                                                   # PIC -> load bank
add_route("mvlv_cable", [(2217, 527), (2217, 492), (2185, 492), (2185, 484)], MX)          # CONT-EH -> PAD-EH
add_route("mvlv_cable", [(2050, 390), (2050, 410), (2165, 410), (2165, 470)], MX)         # TM-1 -> PAD-EH
add_route("mvlv_cable", [(2170, 390), (2170, 403), (2205, 403), (2205, 477), (2200, 477)], MX)   # TM-2
add_route("mvlv_cable", [(1904, 1290), (1904, 1285), (2030, 1285), (2030, 1292)], MX)     # FC-5..12 -> inverter
add_route("mvlv_cable", [(2056, 1304), (2064, 1304), (2064, 1322), (2285, 1322), (2285, 1003),
                         (2250, 1003), (2250, 982)], MX)                                    # inverter -> MOD-LV
add_route("mvlv_cable", [(2114, 1303), (2124, 1303), (2124, 1322)], MX)                   # MT-4..6 join
add_route("fuel_gas", [(2340, 440), (2340, 452), (1985, 452), (1985, 536), (2130, 536)], MX)   # pad skid -> TM / CONT
for x in (2082, 2202):
    add_route("fuel_gas", [(x, 452), (x, 377)], MX)
for x in (2010, 2070, 2130):
    add_route("fuel_gas", [(x, 536), (x, 513)], MX)
    add_route("fuel_gas", [(x, 536), (x, 560)], MX)
add_route("fuel_gas", [(1955, 1350), (1955, 1316)], MX)                                    # header -> FC-5..12
for k in range(8):                                                                          # FC tails to the DC feeder
    add_route("mvlv_cable", [(1904 + 14 * k, 1290), (1904 + 14 * k, 1285)], MX)
# SC-1 / SC-2 fuel gas from the fuel-gas compressor building (not drawn on sheet 07)
add_route("fuel_gas", [(2290, 1182), (1940, 1182), (1940, 1190)], "OPT_MOD_ROUTES")
add_route("fuel_gas", [(2140, 1182), (2140, 1190)], "OPT_MOD_ROUTES")
add_route("fuel_gas", [(2093, 1350), (2093, 1317)], MX)                                    # header -> MT-4..6
# BESS main power transformer to the D4 upper position (230 kV cable to the take-off gantry)
add_route("hv_cable", [(1756, 352), (1756, 170)], "OPT_BESS_ROUTES", sheet="typical (switchyard build-out)")
# Turbine-hall cabling the drawing leaves to the vendor (typical): a control / instrument backbone
# from R1 along the hall north wall at EL +42, and per unit the control drops (turbine control
# cabinets, GT junction boxes, generator neutral cubicle, excitation and IPB cubicles in the
# gallery), the LV feeders to every motor load on the deck, the excitation transformer tap and
# the DC field cables to the generator collector end.
HC = "typical (hall cabling)"


def hall_lv(points, layer="ROUTES_BASE", sheet=HC):
    """LV branch off the hall LV run, which rides at EL +44 above the GT exhaust ducts."""
    add_route("lv_tray", points, layer, sheet=sheet)
    routes[-1]["z"] = 44


add_route("control_tray", [(474, 724), (500, 724), (500, 552), (1017, 552)], "ROUTES_BASE", sheet=HC)
for k in range(3):
    dx = 160 * k
    add_route("control_tray", [(606 + dx, 552), (606 + dx, 512)], "ROUTES_BASE", sheet=HC)       # -> TCP
    add_route("control_tray", [(645 + dx, 552), (645 + dx, 480)], "ROUTES_BASE", sheet=HC)       # -> GT junction boxes
    add_route("control_tray", [(650 + dx, 552), (650 + dx, 414)], "ROUTES_BASE", sheet=HC)       # -> NGT, GCB
    add_route("control_tray", [(655 + dx, 552), (655 + dx, 398)], "ROUTES_BASE", sheet=HC)       # -> EXC / SPC
    hall_lv([(668 + dx, 544), (668 + dx, 530)], "ROUTES_BASE", sheet=HC)            # -> CO2 skid
    hall_lv([(590 + dx, 544), (590 + dx, 493)], "ROUTES_BASE", sheet=HC)            # -> water wash
    hall_lv([(690 + dx, 544), (690 + dx, 526)], "ROUTES_BASE", sheet=HC)            # -> gas fuel module
    hall_lv([(605 + dx, 544), (605 + dx, 513)], "ROUTES_BASE", sheet=HC)            # -> TCP (UPS)
    hall_lv([(612 + dx, 544), (612 + dx, 440)], "ROUTES_BASE", sheet=HC)            # -> generator aux
    add_route("lv_tray", [(612 + dx, 397), (642 + dx, 397)], "ROUTES_BASE", sheet=HC)            # ET -> EXC
    add_route("lv_tray", [(648 + dx, 399), (648 + dx, 407), (636 + dx, 407)], "ROUTES_BASE", sheet=HC)   # DC field
    add_route("mv_tray", [(609 + dx, 396), (609 + dx, 386), (622 + dx, 386)], "ROUTES_BASE", sheet=HC)   # ET tap
# ST: down the west side of the ST (the 26 ft exhaust duct blocks the east side), then over the STG
add_route("control_tray", [(1017, 552), (1017, 431), (1082, 431)], "ROUTES_BASE", sheet=HC)      # -> TCP-ST
add_route("control_tray", [(1064, 431), (1064, 417)], "ROUTES_BASE", sheet=HC)                    # -> NGT-ST
add_route("lv_tray", [(1068, 401), (1068, 407), (1052, 407)], "ROUTES_BASE", sheet=HC)            # ST DC field
for k in range(3):                                                                         # GCB control
    add_route("control_tray", [(655 + 160 * k, 398), (655 + 160 * k, 385), (636 + 160 * k, 385)], "ROUTES_BASE",
              sheet=HC)
# HRSG instrument / control cabling: from the rack control tier (EL 42) down the east side of each
# HRSG to the riser at its south-east corner (clear of the stair towers and the rack bents)
for k, xr in enumerate((674.5, 837.0, 994.5)):
    add_route("control_tray", [(xr, 842), (xr, 605.5), (668.0 + 160 * k, 605.5)], "ROUTES_BASE",
              sheet="typical (HRSG detail)")
# GSU / UAT marshalling cabinets to the existing duct bank (protection, monitoring, cooling control)
for x in (612, 772, 932):
    add_route("duct_bank", [(x, 330), (x, 312)], "ROUTES_BASE", sheet=HC)
add_route("duct_bank", [(1034, 324), (1034, 312), (987, 312)], "ROUTES_BASE", sheet=HC)
item("HV_CORRIDOR", "H-MOD 230 kV monopoles in COR-HMOD", (1505, 2105, 255, 815), (0, 50), area="I",
     basis="typical", sheet="SK-3X1-08", info="Overhead tie from T-MOD-1/2 to the D4 lower position (future).")
for (x, y) in [(2095, 815), (1950, 805), (1800, 805), (1650, 805), (1515, 805), (1515, 650), (1515, 500),
               (1515, 350), (1515, 262), (1690, 262)]:
    R((x, y, 0), (x, y, 50), 1.2, "steel", r2=0.8, seg=10)
    B(x - 6, x + 6, y - 0.6, y + 0.6, 45, 46, "steel") if x != 1515 else B(x - 0.6, x + 0.6, y - 6, y + 6, 45, 46, "steel")

LAYERS = {
    "SITE": ("Site, roads and fence", "Base plant"),
    "BASE_POWER_BLOCK": ("A/B Power block: hall, GTs, ST, HRSGs, stacks, ACC", "Base plant"),
    "HALL_ROOF": ("Turbine hall and gallery roofs", "Base plant"),
    "BASE_INLET_AIR": ("Filter houses and inlet ducts", "Base plant"),
    "BASE_ELECTRICAL": ("Electrical: GSUs, UATs, GCBs, e-houses, EDGs", "Base plant"),
    "R1_ROOF": ("R1 roof", "Base plant"), "R1_WALL_E": ("R1 east wall", "Base plant"),
    "R1_INTERIOR": ("R1 interior (SK-3X1-05)", "Base plant"),
    "R4_ROOF": ("R4 roof", "Base plant"), "R4_WALL_E": ("R4 east wall", "Base plant"),
    "R4_INTERIOR": ("R4 VFD interior", "Base plant"),
    "BASE_SWITCHYARD": ("C Grid interface: 230 kV switchyard", "Base plant"),
    "BASE_UTILITIES": ("D/E Fuel gas, water and BOP utilities, pipe racks, M&R", "Base plant"),
    "BASE_SERVICES": ("F Controls / service", "Base plant"),
    "ROUTES_BASE": ("Cable trays, IPB, duct banks, 230 kV", "Routes"),
    "PROCESS_PIPING": ("Process piping", "Routes"),
    "UNDERGROUND": ("Underground: duct banks, ground grid, drains, water mains", "Routes"),
    "SWYD_FUTURE": ("D4 / D5 / D6 switchyard build-out", "Optional / adjacent"),
    "HV_CORRIDOR": ("Reserved 230 kV corridor + H-MOD tie", "Optional / adjacent"),
    "OPT_CCS": ("G Carbon capture, 3 trains", "Optional / adjacent"),
    "OPT_CCSU": ("G CCS utilities (cooling tower)", "Optional / adjacent"),
    "OPT_BESS": ("H BESS", "Optional / adjacent"),
    "OPT_MOD": ("I Modular generation + black start", "Optional / adjacent"),
    "OPT_TMP": ("I Portable / containerized power pad", "Optional / adjacent"),
    "OPT_MODX": ("I+ Modular expansion (design change beyond Rev 14)", "Optional / adjacent"),
    "OPT_MODX_ROUTES": ("I+ modular expansion routes", "Optional routes"),
    "OPT_IC": ("J GT inlet chilling", "Optional / adjacent"),
    "OPT_LNG": ("K LNG satellite", "Optional / adjacent"),
    "OPT_H2": ("K 25 MW green hydrogen", "Optional / adjacent"),
    "OPT_CCS_ROUTES": ("G routes", "Optional routes"), "OPT_CCSU_ROUTES": ("G utility routes", "Optional routes"),
    "OPT_BESS_ROUTES": ("H routes", "Optional routes"), "OPT_MOD_ROUTES": ("I modular routes", "Optional routes"),
    "OPT_TMP_ROUTES": ("I portable-pad routes", "Optional routes"), "OPT_IC_ROUTES": ("J routes", "Optional routes"),
    "OPT_LNG_ROUTES": ("K LNG routes", "Optional routes"), "OPT_H2_ROUTES": ("K H2 routes", "Optional routes"),
    "OPT_DC": ("L BTM data centre (~150 MW, design option)", "Optional / adjacent"),
    "OPT_DC_ROUTES": ("L BTM routes", "Optional routes"),
    "OPT_UNDERGROUND": ("Underground: option duct banks", "Optional routes"),
    "NOMOD_GROUND": ("Ground patch (views without the modular yard)", "Base plant"),
    "NOBESS_GROUND": ("Ground patch (views without the BESS)", "Base plant"),
}
AREAS = {"A": "Power block", "B": "ACC", "C": "Grid interface", "D": "Fuel gas", "E": "Water / utilities",
         "F": "Controls / service", "G": "Carbon capture", "H": "BESS", "I": "Modular / portable power",
         "J": "GT inlet chilling", "K": "Fuel supply (adjacent market)", "L": "BTM data centre (design option)"}
# Views from SK-3X1-11 (collections to show), plus two convenience views.
BASE_SHOW = ["SITE", "BASE_POWER_BLOCK", "HALL_ROOF", "BASE_INLET_AIR", "BASE_ELECTRICAL", "R1_ROOF", "R1_WALL_E",
             "R4_ROOF", "R4_WALL_E", "BASE_SWITCHYARD", "BASE_UTILITIES", "BASE_SERVICES", "ROUTES_BASE",
             "PROCESS_PIPING"]
VIEWS = [
    dict(k="A", n="A Plant overview", show=["SITE", "BASE_POWER_BLOCK", "BASE_ELECTRICAL", "BASE_INLET_AIR",
         "BASE_SWITCHYARD", "HALL_ROOF", "R1_ROOF", "R1_WALL_E", "R4_ROOF", "R4_WALL_E", "ROUTES_BASE",
         "PROCESS_PIPING"], t=[930, 560, 30], c=[-150, -560, 950]),
    dict(k="B", n="B R1 cutaway", show=["SITE", "BASE_ELECTRICAL", "R1_INTERIOR", "ROUTES_BASE"],
         t=[442, 692, 4], c=[560, 560, 120]),
    dict(k="B2", n="B2 R4 VFD room", show=["SITE", "BASE_ELECTRICAL", "R4_INTERIOR", "ROUTES_BASE", "BASE_POWER_BLOCK"],
         t=[1195, 338, 6], c=[1330, 250, 95]),
    dict(k="C", n="C Pumps / ACC routes", show=["SITE", "BASE_POWER_BLOCK", "BASE_ELECTRICAL", "BASE_UTILITIES",
         "ROUTES_BASE", "PROCESS_PIPING"], t=[1250, 800, 20], c=[1190, 1070, 190]),
    dict(k="H", n="Turbine hall (roof off)", show=["SITE", "BASE_POWER_BLOCK", "BASE_INLET_AIR", "BASE_ELECTRICAL",
         "ROUTES_BASE", "PROCESS_PIPING"], t=[790, 480, 25], c=[600, 250, 260]),
    dict(k="U", n="U Underground (ground removed)", show=["UNDERGROUND", "BASE_POWER_BLOCK", "BASE_ELECTRICAL",
         "BASE_SWITCHYARD", "BASE_UTILITIES", "BASE_SERVICES", "BASE_INLET_AIR"], t=[800, 420, -4], c=[560, 40, 330]),
    dict(k="U2", n="U2 Underground: all zones (BESS, modular, gas, CCS, H2, BTM)", show=["UNDERGROUND", "OPT_UNDERGROUND"]
         + [l for l in LAYERS if l.startswith(("BASE_", "OPT_")) and not l.endswith("_ROUTES") and l != "OPT_UNDERGROUND"],
         t=[1500, 900, -4], c=[600, -500, 1300]),
    dict(k="CY", n="Cable reel yard: reels and SIMpull Truck", show=BASE_SHOW,
         t=[150, 790, 2], c=[120, 690, 45]),
    dict(k="CHV", n="Cable installed: 230 kV termination at the BESS bay",
         show=BASE_SHOW + ["OPT_BESS", "OPT_BESS_ROUTES"], t=[1756, 177, 12], c=[1772, 202, 16]),
    dict(k="CEH", n="Cable installed: MV cable entries under MOD-EH",
         show=BASE_SHOW + ["OPT_MOD", "OPT_MOD_ROUTES"], t=[1960, 899, 1.6], c=[1953, 911, 4.5]),
    dict(k="CPM", n="Cable installed: data hall pad-mount termination cabinet",
         show=BASE_SHOW + ["OPT_DC", "OPT_DC_ROUTES"], t=[2751, 1318.5, 3], c=[2747.5, 1329, 5.6]),
    dict(k="CBE", n="Cable installed: BESS skid elbows and the open DC trench",
         show=BASE_SHOW + ["OPT_BESS", "OPT_BESS_ROUTES"], t=[1610, 490, 3.3], c=[1619, 483, 5.5]),
    dict(k="M", n="Maintenance: cable pull on the modular-yard 13.8 kV collector (manholes, reel, trench)",
         show=BASE_SHOW + ["OPT_MOD", "OPT_MOD_ROUTES"], t=[1805, 950, 0], c=[1680, 860, 80]),
    dict(k="O1", n="O1 Modular / portable", show=BASE_SHOW + ["OPT_MOD", "OPT_TMP", "OPT_MODX", "OPT_MOD_ROUTES", "OPT_TMP_ROUTES", "OPT_MODX_ROUTES",
         "HV_CORRIDOR", "SWYD_FUTURE"], t=[1960, 880, 20], c=[1520, 300, 760]),
    dict(k="O2", n="O2 BESS", show=BASE_SHOW + ["OPT_BESS", "OPT_BESS_ROUTES"], t=[1740, 560, 5], c=[1480, 200, 420]),
    dict(k="O3", n="O3 Carbon capture", show=BASE_SHOW + ["OPT_CCS", "OPT_CCSU", "OPT_CCS_ROUTES", "OPT_CCSU_ROUTES"],
         t=[900, 1300, 110], c=[150, 150, 1150]),
    dict(k="O4", n="O4 Inlet chilling", show=BASE_SHOW + ["OPT_IC", "OPT_IC_ROUTES"], t=[180, 1160, 20], c=[-150, 820, 420]),
    dict(k="O5", n="O5 Gas, LNG, H2", show=BASE_SHOW + ["OPT_LNG", "OPT_H2", "OPT_LNG_ROUTES", "OPT_H2_ROUTES",
         "SWYD_FUTURE"], t=[1980, 1650, 10], c=[1650, 1150, 700]),
    dict(k="O6", n="Add-on: plant + BTM data centre", show=[l for l in LAYERS if l not in ("R1_INTERIOR", "R4_INTERIOR", "UNDERGROUND", "OPT_UNDERGROUND")],
         t=[2200, 850, 30], c=[700, -1400, 1700]),
    dict(k="ALL", n="Complete plant", show=[l for l in LAYERS if l not in ("R1_INTERIOR", "R4_INTERIOR", "UNDERGROUND", "OPT_UNDERGROUND")
                                            and not l.startswith("OPT_DC")],
         t=[1210, 900, 40], c=[-350, -750, 1400]),
]


# Fit sets for the orthographic cameras (SK-3X1-11: "its fit set is projected
# along the view direction; ortho scale and target are solved so the fit set
# fills the frame with a 3% margin"). Either layers or a plan/elevation box.
FIT = {
    "A": dict(layers=["BASE_POWER_BLOCK", "BASE_INLET_AIR", "BASE_ELECTRICAL", "BASE_SWITCHYARD"],
              clip=[380, 1480, 0, 900]),       # core plant + D1-D3; the long buses run beyond
    "B": dict(box=[410, 480, 600, 780, 0, 24]),
    "B2": dict(box=[1135, 1310, 308, 368, 0, 16]),
    "C": dict(box=[1130, 1450, 790, 850, 0, 40]),
    "H": dict(box=[480, 1100, 370, 560, 0, 60]),
    "U": dict(box=[0, 2420, 0, 1920, -10, 20]),
    "U2": dict(box=[0, 3380, 0, 1920, -10, 20]),
    "M": dict(box=[1695, 1940, 905, 972, -9, 12]),
    "CY": dict(box=[44, 316, 700, 880, 0, 14]),
    "CHV": dict(box=[1745, 1767, 166, 188, 0, 27]),
    "CEH": dict(box=[1925, 1995, 890, 906, 0, 4]),
    "CPM": dict(box=[2744, 2758, 1308, 1322, 0, 9]),
    "CBE": dict(box=[1600, 1620, 480, 500, 0, 9]),
    "O1": dict(layers=["OPT_MOD", "OPT_TMP", "OPT_MODX"]),
    "O2": dict(layers=["OPT_BESS"]),
    "O3": dict(layers=["OPT_CCS", "OPT_CCSU"]),
    "O4": dict(layers=["OPT_IC"]),
    "O5": dict(layers=["OPT_LNG", "OPT_H2"], box=[1560, 2400, 1410, 1910, 0, 30]),
    "O6": dict(box=[0, 3380, 0, 1920, 0, 120]),
    "ALL": dict(box=[0, 2420, 0, 1920, 0, 120]),
}
for v in VIEWS:
    v["fit"] = FIT[v["k"]]


# the LV branch north off the rack to the heat-trace panel rides just above the tier-30 pipes
for r in routes:
    if r["type"] == "lv_tray" and [tuple(p) for p in r["points"]] == [(572.0, 838.0), (572.0, 852.0)]:
        r["z"] = 33.0

# IPB around the filter-house columns: the drawing puts the middle FH-n columns (x 630, y 366-369 and
# 400-403) on the GT centreline, where the IPB and the GCB also sit. Coordination fix (typical): the
# IPB jogs 7 ft east past each column line and returns to the centreline through the GCB; the UAT
# tap leaves the GSU-side leg and drops to the UAT clear of the east column (x 670).
_ipb = []
for r in routes:
    if r["type"] != "ipb":
        continue
    pts = [tuple(p) for p in r["points"]]
    for k, x in enumerate((630.0, 790.0, 950.0)):
        if pts == [(x, 410.0), (x, 365.0)]:
            r["points"] = [[x, 410.0], [x, 407.5], [x + 7, 407.5], [x + 7, 395.5], [x, 395.5], [x, 375.0],
                           [x + 7, 375.0], [x + 7, 363.0]]
        elif pts == [(x, 375.0), (x + 37, 375.0)]:
            r["points"] = [[x + 7, 366.0], [x + 34, 366.0]]
        elif pts == [(x + 37, 375.0), (x + 37, 352.0)]:
            r["points"] = [[x + 34, 366.0], [x + 34, 352.0]]
    _ipb.append(r)

# Hall cable tiers: the drawn MV and LV hall runs (from R1 along the north wall at y 544 / 548) would
# pass through the GT exhaust ducts (EL 21-38) at EL +36 / +30; inside the hall they ride above
# them, LV at EL +44 and MV at EL +48 (control stays at EL +42). The drawing splits each run into
# pieces, so the whole connected chain from R1 is raised. The LV run's tail to the ST aux skid
# drops back to EL +30 to pass under the 26 ft ST exhaust duct (bottom EL 31).
_tails = []
for r in list(routes):
    if r["type"] == "lv_tray" and [1010.0, 556.0] in r["points"] and [1010.0, 544.0] in r["points"]:
        k = r["points"].index([1010.0, 544.0])
        _tails.append(dict(r, points=r["points"][k:]))
        r["points"] = r["points"][:k + 1]
routes += _tails


def _chain(rtype, seed):
    """Routes of one type connected (by shared end points) to any route touching `seed`."""
    rs = [r for r in routes if r["type"] == rtype and r["z"] > 0 and not any(t is r for t in _tails)]
    key = lambda p: (round(p[0], 1), round(p[1], 1))
    hit = [r for r in rs if any(seed(p) for p in r["points"])]
    ends = {key(p) for r in hit for p in (r["points"][0], r["points"][-1])}
    grown = True
    while grown:
        grown = False
        for r in rs:
            if r in hit:
                continue
            if key(r["points"][0]) in ends or key(r["points"][-1]) in ends:
                hit.append(r)
                ends |= {key(r["points"][0]), key(r["points"][-1])}
                grown = True
    return hit


_in_hall = lambda p: 555 < p[0] < 1015 and 410 < p[1] < 559
for r in _chain("lv_tray", _in_hall):
    r["z"] = 44
for r in routes:                       # the tail east of x 1010 to the ST aux skid stays under the ST exhaust duct
    if r["type"] == "lv_tray" and r["z"] == 44 and all(p[0] >= 1010 and p[1] >= 505 for p in r["points"]):
        r["z"] = 30
for r in _chain("mv_tray", _in_hall):
    r["z"] = 48
# drawn tray legs that sit on column lines: the MV legs off the HRSG stair towers (x 672 / 832 / 992)
# and off the ACC column line and main-steam duct supports (x 1150 -> 1157, y 580 -> 585)
for r in routes:
    if r["type"] in ("lv_tray", "mv_tray") and r["z"] > 0:
        for p in r["points"]:
            if r["type"] == "mv_tray" and p[0] in (672.0, 832.0, 992.0) and 600 <= p[1] <= 840:
                p[0] += -4.85 if p[0] == 832.0 else 5       # clear of the rack bent at x 835 and the HRSG 2 column and stair
            elif r["type"] == "lv_tray" and p[0] in (672.0, 832.0, 992.0) and 700 <= p[1] <= 840:
                p[0] -= 0.6                                  # between the HRSG platform rail and the stair-tower posts
            if r["type"] == "mv_tray" and p[0] == 561.0 and 670 <= p[1] <= 840:
                p[0] = 565.0
            if r["type"] == "lv_tray" and p[0] == 1150.0 and 370 <= p[1] <= 585:
                p[0] = 1157.0
            if r["type"] == "lv_tray" and p[1] == 580.0 and 1149 <= p[0] <= 1441:
                p[1] = 585.0

# Utilities piping routes (cycle 4): tank farm water headers, fire water, auxiliary steam
import utilities as _util
_util.routes(add_route)

# Switchyard control-cable trenches (routes; their concrete is drawn in switchyard.py)
import switchyard as _swyd
_swyd.routes(add_route)
_swyd.build(routes)       # trenches, breaker mechanisms, disconnect blades, line entrances, masts, fence
_util.build()             # cycle 4: fire pump house, ammonia, aux boiler, air compressors, OWS
import services as _services
_services.routes(add_route)
N_DRAIN = _services.build()
import ponds as _ponds
_ponds.build()            # stormwater pond works and pump station; wastewater treatment process area
import lng_h2 as _lh
_lh.routes(add_route)
_lh.build()               # cycle 9: LNG satellite and green hydrogen
import inletchill as _ic
_ic.routes(add_route)
_ic.build()               # cycle 8: GT inlet chilling tower, chillers, pumps, CW / CHW loops
import bess as _bess
_bess.routes(add_route)
_bess.build()             # cycle 7: BESS yard, containers, PCS skids, collector, buildings
import datacenter as _dc
_dc.routes(add_route)
_dc.color_routes(routes)
_dc.build()               # BTM data centre: dressing, BESS / genset / substation detail
import ccs as _ccs
_ccs.routes(add_route)
import ccs_detail as _ccsd
_ccsd.routes(add_route)
for _r in routes:
    if _r.get('sheet') == 'typical (CCS audit)' and _r['type'] == 'lv_tray' and _r['points'][0][1] == 1133 or \
            (_r.get('sheet') == 'typical (CCS audit)' and _r['type'] == 'lv_tray' and [1046, 1133] in _r['points']):
        _r['z'] = 27.3                    # on top of the CCS pipe rack
_ccs.build(); _ccsd.build(); import zone_detail as _zd; _zd.build()              # cycle 6: carbon capture flue-gas path, amine piping and rack, regeneration, CT   # cycle 5: gate, fence wire and CCTV, drainage, lighting, admin / workshop dressing
import placeholders as _ph
_ph.build()               # single-box placeholders rebuilt as equipment (CCS, LNG, H2, BTM)
_dc.color_parts()         # BTM data centre: colour by supply path (islanded / modular yard / grid tie)

# Wiring applications: every powered / instrumented item gets its cable applications, and a buried
# feeder to the nearest underground cable network where no cable route reached it
import wiring as _wiring
import hall as _hall_w
_hall_w.inlet_routes(add_route)
_hall_w.gt_st_routes(add_route)
N_WAPPS, N_FEEDERS = _wiring.build(items, routes, LAYERS, add_route)
_hall_w.inlet_wiring()
_wiring.apply_overrides(items)
_fuel.G['routes'] = routes
_station.build_late()  # duct-bank manholes and handholes (after the feeders exist)

# Low pipe routes: road crossings go below grade in sleeves; sleepers / T-posts under the rest
# LV / instrument cables inside the gas yard and the M&R station run buried in conduit (hazardous
# area), not on 30 ft trays
for r in routes:
    if r["type"] == "lv_tray" and all(any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, x1, y0, y1) in _fuel.GAS_AREAS)
                                      for x, y in r["points"]):
        r["z"], r["h"] = -2, 0.6
        r["label"] = "LV / instrument cable, buried conduit (gas area)"
N_XING = _fuel.road_crossings(routes)
N_SUPPORTS = _fuel.supports(routes)
import pipes as _pipes
N_PIPE = _pipes.build(item, items, parts, routes)     # round pipes, elbows, flanges, jackets


# Detail pass (LOD 2): stairs, rails, ladders, sheds, lattice, rack piping, doors, poles
import detail as _detail
N_DETAIL = _detail.Detail(items, parts).run()
# LOD 3: building and equipment dressing for close views
import detail3 as _detail3
N_DETAIL += _detail3.Detail3(items, parts).run()
# Tray review (user screenshots): short tray stubs drawn between a duct-bank end and pad equipment
# rode the EL +36 rack tier, so a 10 ft connection became a 36 ft goalpost over the transformer. A
# duct bank comes up straight into the equipment: those stubs are now buried, with rigid-conduit
# stub-ups into the terminal compartment. In the south gallery the excitation-transformer feed
# runs at the IPB tap level (EL +24) and the ET -> excitation cable tray just above the cubicles.
_db_ends = {tuple(p) for r in routes if r["type"] == "duct_bank" for p in (r["points"][0], r["points"][-1])}
N_STUB = 0
for r in routes:
    P = r["points"]
    if r["type"] not in ("mv_tray", "lv_tray") or len(P) != 2:
        continue
    L = abs(P[0][0] - P[1][0]) + abs(P[0][1] - P[1][1])
    if L > 30 or not (tuple(P[0]) in _db_ends or tuple(P[1]) in _db_ends):
        continue
    end = P[1] if tuple(P[0]) in _db_ends else P[0]
    r["type"], r["z"], r["w"], r["h"], r["color"] = "duct_bank", -2, 3, 1.5, "ductbank"
    r["label"] = "Duct bank (underground), stub-up into the equipment"
    tgt = min((it for it in items if it["z"][1] < 20 and it["fp"][1] - it["fp"][0] < 200 and
               it["fp"][0] - 6 <= end[0] <= it["fp"][1] + 6 and it["fp"][2] - 6 <= end[1] <= it["fp"][3] + 6),
              key=lambda it: (it["fp"][1] - it["fp"][0]) * (it["fp"][3] - it["fp"][2]), default=None)
    if tgt is None:
        continue
    x0, x1, y0, y1 = tgt["fp"]
    ex, ey = min(max(end[0], x0), x1), min(max(end[1], y0), y1)       # where the bank meets the pad
    along_x = ey in (y0, y1)
    for k in range(4):                                                  # rigid conduit stub-ups
        o = -1.2 + .8 * k
        cx, cy = (ex + o, ey) if along_x else (ex, ey + o)
        parts.append(dict(kind="rod", a=[cx, cy, .3], b=[cx, cy, 2.4], r=.22, r2=.22, color="steel", seg=8,
                          item=tgt["id"], layer=tgt["layer"], d=1))
    parts.append(dict(kind="box", min=[ex - 2.2 if along_x else ex - 1, ey - 1 if along_x else ey - 2.2, 0],
                      max=[ex + 2.2 if along_x else ex + 1, ey + 1 if along_x else ey + 2.2, .3], color="concrete",
                      item=tgt["id"], layer=tgt["layer"], d=1))
    N_STUB += 1
for r in routes:
    if r.get("sheet") == HC and r["type"] == "mv_tray" and r["points"][0][1] < 404:
        r["z"] = 24                                                     # ET feed from the IPB tap
    if r.get("sheet") == HC and r["type"] == "lv_tray" and r["points"][0][1] < 400 and r["points"][-1][1] < 400:
        r["z"] = 10.5                                                   # ET -> excitation cubicles
# sanitary lift station feed (underground pass): LV duct bank from the maintenance building
add_route("duct_bank", [(320, 630), (332, 630), (332, 652)], "ROUTES_BASE", sheet="typical (underground)")
# (the ST-aux LV branch leaves R3 through its south face; R3's north face feeds the run to the rack)
# chain-link fences: every fence panel gets line posts every 10 ft and a top rail (the panel itself is the
# mesh, drawn see-through by the renderers), so no fence reads as a solid wall
N_POSTS = 0
for p in [q for q in parts if q["kind"] == "box" and q["color"] == "fence"]:
    (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
    if z1 - z0 < 4.5:
        continue
    along_x = (x1 - x0) >= (y1 - y0)
    L, T = (x1 - x0, y1 - y0) if along_x else (y1 - y0, x1 - x0)
    if L < 4 or T > 1.2:
        continue
    c = (y0 + y1) / 2 if along_x else (x0 + x1) / 2
    a0 = x0 if along_x else y0
    n = max(1, int(round(L / 10)))
    for k in range(n + 1):
        s0 = a0 + L * k / n
        px, py = (s0, c) if along_x else (c, s0)
        parts.append(dict(kind="rod", a=[round(px, 2), round(py, 2), z0], b=[round(px, 2), round(py, 2), z1 + .2],
                          r=.12, r2=.12, color="steel", seg=6, item=p["item"], layer=p["layer"], d=1))
        N_POSTS += 1
    a, b = ([x0, c, z1], [x1, c, z1]) if along_x else ([c, y0, z1], [c, y1, z1])
    parts.append(dict(kind="rod", a=a, b=b, r=.08, r2=.08, color="steel", seg=6, item=p["item"], layer=p["layer"], d=1))
# underground systems in real geometry (duct banks, chambers, ground grid, firewater, drains, water mains)
import underground as _ug
N_UG = _ug.build(items, routes)
# strung conductors sag between their supports (strain buses, shield wires, overhead lines, H-MOD, jumpers)
import cables as _cables
N_CAB = _cables.build(routes)
# trays last, so their supports and drops see every stair, platform and pipe already in the model
import trays as _trays
N_TRAY = _trays.build(item, items, parts, routes)     # ladder trays, cables, supports, drops, IPB
# realism pass last: firewater, small-bore piping, signage, people, vehicles, scaffolding, HRSG harps
import realism as _realism
N_REAL = _realism.build(item, items, parts, routes)
import maintenance as _maint
_maint.build()      # cable-pull scene on the modular-yard 13.8 kV collector bank
import showcase as _show
print("cable showcase", _show.build())
import cable_install as _ci
print("e-house bottom cable entries", _ci.ehouse_bottom_entry("MOD-EH"))
_pm = [i for i in items if i["name"].startswith("Data hall") and "pad-mount 34.5/0.48 kV (3.5 MVA)" in i["name"]]
for _i in _pm:
    _face = "+y" if "A-side" in _i["name"] else "-y"
    _ci.padmount_cabinet(_i, _face, open_=_i["name"].startswith("Data hall A A-side") and _i["fp"][0] < 2750)
_sk = [i for i in items if i["name"] == "BESS PCS / MV skid"]
for _i in _sk:
    _ci.padmount_cabinet(_i, "+x", open_=_i["fp"][0] == 1590 and _i["fp"][2] == 486)
_ci.bess_dc_trench(next(i for i in _sk if i["fp"][0] == 1710 and i["fp"][2] == 544), open_=True)
for _i in _sk:
    if not (_i["fp"][0] == 1710 and _i["fp"][2] == 544):
        _ci.bess_dc_trench(_i)
print("pad-mount cabinets", len(_pm) + len(_sk))
import terminate as _term
N_TERM = _term.build(items, parts)   # quality sweep: every open pipe end terminated (drop to UG, valve, blind flange)
print('pipe-end terminations', N_TERM)
print('supports added under floating parts', _term.support_floating(items, parts))


def validate():
    ids = {it["id"] for it in items}
    assert all(p["item"] in ids for p in parts)
    for p in parts:
        assert p["layer"] in LAYERS, p["layer"]
    for r in routes:
        assert r["layer"] in LAYERS, r
    for it in items:
        assert it["layer"] in LAYERS, it["layer"]


model = dict(
    title="SK-3X1 Rev 14 - 3x1 combined-cycle plant, 3D coordinate model",
    units="feet", axes="X east, Y north, Z up; origin SW corner of compound",
    compound=[2420, 1920],
    disclaimer="Conceptual illustration. Not engineered. Not for construction.",
    source="SK-3X1 Drawing Set Rev 14 (Sept 26, 2026), Stephan Hardt | Power Generation Solutions",
    layers={k: dict(label=v[0], group=v[1]) for k, v in LAYERS.items()},
    areas=AREAS, views=VIEWS, items=items, parts=parts, routes=routes, decals=_fuel.G.get("decals", []),
    underground_audit={k: v for k, v in N_UG['audit'].items()})

if __name__ == "__main__":
    validate()
    out = os.path.join(HERE, "sk3x1_model.json")
    def _r(o):  # 0.01 ft is far below any drawn tolerance; keeps the file small
        if isinstance(o, float):
            return round(o, 2)
        if isinstance(o, list):
            return [_r(v) for v in o]
        if isinstance(o, dict):
            return {k: _r(v) for k, v in o.items()}
        return o
    with open(out, "w") as f:
        json.dump(_r(model), f, separators=(",", ":"))
    reg = sum(1 for it in items if it["register"])
    print(f"wrote {out}: {len(items)} items ({reg} in the register), {len(parts)} parts "
          f"({N_DETAIL} detail), {len(routes)} route polylines; {N_XING} road crossings, {N_SUPPORTS} pipe supports, {N_PIPE} pipe parts, {N_TRAY} tray / IPB parts; wiring on {N_WAPPS} items, {N_FEEDERS} new feeders; realism {N_REAL}")
