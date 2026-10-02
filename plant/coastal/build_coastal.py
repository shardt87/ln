#!/usr/bin/env python3
"""Coastal variant of the SK-3X1 plant (sheet SK-3X1-15): the verified inland plant
model plus an LNG import terminal on the shore.

    A  onshore import terminal beside the plant (EcoElectrica / AES Andres class):
       160,000 m3 full-containment tank, vaporizers, send-out pumps, BOG compressors,
       terminal substation, control building, metering, seawater intake, flare,
       1,700 ft jetty trestle, berth with four unloading arms and a Moss-type carrier.
    B  FSRU moored offshore (Porto de Sergipe class): landfall valve station, buried
       and subsea pipeline, submerged soft-yoke mooring tower, FSRU and an LNG carrier
       alongside for ship-to-ship transfer.

Footprints come from plant/reference/sk3x1_rev14_sheet15.json (extract_sheet15.py).
Sheet 15 draws the FSRU closer than it is ("distance NOT to scale"); the model puts it
at the stated pipeline length, about 21,000 ft (6.4 km) from the landfall station.
Heights, pile spacing, vessel superstructure and every item marked "typical" are
assumptions. The inland plant model is not changed; the variant is written to
plant/coastal/sk3x1_coastal_A.json and sk3x1_coastal_B.json.

    python3 plant/coastal/build_coastal.py
"""
import json
import math
import os

import coastal_detail

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
REF = json.load(open(os.path.join(PLANT, "reference", "sk3x1_rev14_sheet15.json")))
BASE = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))

SEA = -8.0          # mean sea level, ft (plant grade is 0, the shore revetment drops to it)
FSRU_OFFSET = 21000 - (REF["panels"]["B"]["keys"]["14"]["fp"][0] - REF["panels"]["B"]["keys"]["12"]["fp"][1])


class Scene:
    def __init__(self, variant):
        self.variant = variant
        self.items, self.parts = [], []
        self.layers = {}

    def layer(self, key, label):
        self.layers[key] = dict(label=label, group="Coastal (sheet 15)")
        return key

    def item(self, layer, name, fp, z, tag="", key="", basis="typical", shape="rect", info=""):
        iid = f"coastal{self.variant.lower()}-{len(self.items):04d}"
        self.items.append(dict(id=iid, layer=layer, name=name, tag=tag, area="COAST", fp=[round(v, 2) for v in fp],
                               z=[round(v, 2) for v in z], shape=shape, info=info, basis=basis,
                               sheet="SK-3X1-15", register=bool(key), key=key))
        self.cur = (iid, layer)
        return iid

    def _p(self, **kw):
        iid, layer = self.cur
        kw.update(item=iid, layer=layer)
        self.parts.append(kw)

    def box(self, x0, x1, y0, y1, z0, z1, color):
        self._p(kind="box", min=[round(x0, 2), round(y0, 2), round(z0, 2)],
                max=[round(x1, 2), round(y1, 2), round(z1, 2)], color=color)

    def rod(self, a, b, r, color, r2=None, seg=None):
        p = dict(kind="rod", a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=r,
                 r2=r if r2 is None else r2, color=color)
        if seg:
            p["seg"] = seg
        self._p(**p)

    def hexa(self, verts, color):
        self._p(kind="hex", v=[[round(c, 2) for c in v] for v in verts], color=color)

    def prism(self, x0, x1, y0, y1, z0, z1, color, ridge="y"):
        self._p(kind="prism", min=[x0, y0, z0], max=[x1, y1, z1], color=color, ridge=ridge)

    # -- compound shapes ---------------------------------------------------
    def dome(self, cx, cy, z0, R, rise, color, n=9):
        """Spherical cap on a circle of radius R, stacked frustums."""
        Rs = (R * R + rise * rise) / (2 * rise)
        r_at = lambda h: math.sqrt(max(Rs * Rs - (h + Rs - rise) ** 2, 0))
        for i in range(n):
            h0, h1 = rise * i / n, rise * (i + 1) / n
            self.rod((cx, cy, z0 + h0), (cx, cy, z0 + h1), r_at(h0), color, r2=max(r_at(h1), .6), seg=48)

    def ladder_tower(self, x, y, w, z1, color="stair"):
        """Open stair tower: four corner posts, landings every 14 ft, cross bracing."""
        h = w / 2
        for dx in (-h, h):
            for dy in (-h, h):
                self.rod((x + dx, y + dy, 0), (x + dx, y + dy, z1), .5, "steel")
        z = 14.0
        while z < z1:
            self.box(x - h, x + h, y - h, y + h, z - .4, z, "grating")
            self.rod((x - h, y - h, z - 14), (x + h, y + h, z), .25, "steel")
            z += 14
        self.box(x - h - .5, x + h + .5, y - h - .5, y + h + .5, z1 - .5, z1, "grating")

    def pipe_path(self, pts, z, r, color, bents=0):
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            self.rod((ax, ay, z), (bx, by, z), r, color)
        if bents:                               # T-support every `bents` ft
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                L = math.hypot(bx - ax, by - ay)
                for k in range(1, int(L // bents) + 1):
                    t = k * bents / L
                    x, y = ax + t * (bx - ax), ay + t * (by - ay)
                    self.rod((x, y, 0), (x, y, z - r - .3), .45, "steel")

    def row_strip(self, pts, w, color="corridor", z=0.05, markers=250):
        """Buried pipeline right of way: a surface strip with marker posts."""
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            x0, x1 = sorted((ax, bx))
            y0, y1 = sorted((ay, by))
            self.box(x0 - w / 2, x1 + w / 2, y0 - w / 2, y1 + w / 2, -.2, z, color)
            L = math.hypot(bx - ax, by - ay)
            for k in range(int(L // markers) + 1):
                t = k * markers / max(L, 1)
                self.rod((ax + t * (bx - ax) + w / 2 - 1, ay + t * (by - ay) + w / 2 - 1, 0),
                         (ax + t * (bx - ax) + w / 2 - 1, ay + t * (by - ay) + w / 2 - 1, 4), .3, "amber")

    def fence(self, x0, x1, y0, y1, h=8, gap=None):
        for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
            if gap and gap[0] == (ax, ay, bx, by):
                a, b = gap[1]
                segs = [((ax, ay), (ax + (bx - ax) * a, ay + (by - ay) * a)),
                        ((ax + (bx - ax) * b, ay + (by - ay) * b), (bx, by))]
            else:
                segs = [((ax, ay), (bx, by))]
            for (px, py), (qx, qy) in segs:
                self.box(min(px, qx) - .1, max(px, qx) + .1, min(py, qy) - .1, max(py, qy) + .1, 0, h, "fence")

    def vessel(self, name, tag, fp, domes, deck=40.0, draft=38.0, regas=False, key="", bow="n"):
        """Moss-type LNG vessel: hull with raked bow and transom stern, four spherical
        cargo tanks under covers, accommodation aft, manifold midships."""
        x0, x1, y0, y1 = fp
        xc, hb = (x0 + x1) / 2, (x1 - x0) / 2
        keel = SEA - draft
        self.item(self.lay_marine, name, fp, (keel, deck + 85), tag=tag, key=key,
                  basis="illustrative (sheet 15 outline)", shape="hull")
        L = y1 - y0
        ybow = y1 - .13 * L                       # start of the bow taper
        ystern = y0 + .06 * L
        # parallel body
        self.box(x0, x1, ystern, ybow, keel, deck, "hull")
        self.box(x0 - .25, x1 + .25, ystern, ybow, SEA - 2, SEA + 5, "antifoul")      # boot topping
        self.box(x0 + 1, x1 - 1, ystern, ybow, deck, deck + .4, "deck")
        # bow: top and bottom outlines taper, the keel rakes back
        n = 6
        for i in range(n):
            f0, f1 = i / n, (i + 1) / n
            ya, yb = ybow + (y1 - ybow) * f0, ybow + (y1 - ybow) * f1
            wa, wb = hb * math.sqrt(1 - f0 ** 1.7), max(hb * math.sqrt(1 - f1 ** 1.7), 2)
            ka, kb = keel + (deck - 12 - keel) * f0 ** 2.2, keel + (deck - 12 - keel) * f1 ** 2.2
            q = lambda y, w, z: [(xc - w, y, z), (xc + w, y, z)]
            bot = q(ya, wa * .8, ka) + q(yb, wb * .8, kb)[::-1]
            top = q(ya, wa, deck + 4) + q(yb, wb, deck + 4)[::-1]
            self.hexa(bot + top, "hull")
        self.box(xc - 12, xc + 12, y1 - 60, y1 - 25, deck + 4, deck + 5, "deck")
        self.rod((xc, y1 - 40, deck + 5), (xc, y1 - 40, deck + 45), .8, "super")          # foremast
        # stern: narrower, cut-up
        wa, wb = hb * .82, hb
        bot = [(xc - wa * .7, y0, keel + 20), (xc + wa * .7, y0, keel + 20), (xc + wb, ystern, keel), (xc - wb, ystern, keel)]
        top = [(xc - wa, y0, deck), (xc + wa, y0, deck), (xc + wb, ystern, deck), (xc - wb, ystern, deck)]
        self.hexa(bot + top, "hull")
        # accommodation, bridge wings and funnel
        ya = ystern + 8
        self.box(xc - hb * .78, xc + hb * .78, ya, ya + 48, deck, deck + 62, "super")
        self.box(x0 - 4, x1 + 4, ya + 36, ya + 48, deck + 54, deck + 62, "super")
        self.box(xc - hb * .78 - .3, xc + hb * .78 + .3, ya + 47.7, ya + 48.3, deck + 50, deck + 58, "glass")
        self.box(xc - 16, xc + 16, ya - 2, ya + 16, deck + 62, deck + 88, "super")
        self.box(xc - 16.3, xc + 16.3, ya - 2.3, ya + 16.3, deck + 82, deck + 88, "hull")
        self.rod((xc, ya + 30, deck + 62), (xc, ya + 30, deck + 90), .6, "super")         # radar mast
        # cargo tanks: cylindrical skirt plus a dome cover, then the centreline walkway
        for (cx, cy, d) in domes:
            R = d / 2
            self.rod((cx, cy, deck), (cx, cy, deck + 24), R, "mosscover", seg=64)
            self.dome(cx, cy, deck + 24, R, R * .78, "mosscover")
            self.rod((cx, cy, deck + 24 + R * .78), (cx, cy, deck + 30 + R * .78), 5, "steel")   # tank dome
        ys = sorted(d[1] for d in domes)
        self.box(xc - 3, xc + 3, ys[0], ys[-1], deck + 24 + domes[0][2] / 2 * .78 - 3,
                 deck + 25 + domes[0][2] / 2 * .78 - 3, "grating")
        # deck piping along the port and starboard sides, manifold midships
        for s in (-1, 1):
            self.rod((xc + s * (hb - 8), ystern + 60, deck + 3), (xc + s * (hb - 8), ybow, deck + 3), 1.4, "lngpipe")
        ym = (ys[1] + ys[2]) / 2
        self.box(x0 + 3, x1 - 3, ym - 10, ym + 10, deck, deck + 10, "steel")
        for k in range(4):
            self.rod((x0 + 3, ym - 7.5 + 5 * k, deck + 6), (x0 - 1, ym - 7.5 + 5 * k, deck + 6), 1, "lngpipe")
            self.rod((x1 - 3, ym - 7.5 + 5 * k, deck + 6), (x1 + 1, ym - 7.5 + 5 * k, deck + 6), 1, "lngpipe")
        # lifeboat davits aft
        for s in (-1, 1):
            self.rod((xc + s * (hb * .78 + 5), ya + 18, deck + 34), (xc + s * (hb * .78 + 5), ya + 38, deck + 34), 4, "amber")
        if regas:
            # regasification module on the fore deck (FSRU), with a vent mast
            yr0 = ys[-1] + domes[-1][2] / 2 + 14
            yr1 = ybow - 6
            for i in range(3):
                xa = x0 + 12 + i * (hb * 2 - 24) / 3
                self.box(xa, xa + (hb * 2 - 24) / 3 - 4, yr0, yr1, deck, deck + 22, "equip")
                self.box(xa - .5, xa + (hb * 2 - 24) / 3 - 3.5, yr0 - .5, yr1 + .5, deck + 22, deck + 23, "grating")
            for k in range(6):
                self.rod((x0 + 10, yr0 + 6 + k * (yr1 - yr0 - 12) / 5, deck + 26),
                         (x1 - 10, yr0 + 6 + k * (yr1 - yr0 - 12) / 5, deck + 26), 1.2, "lngpipe")
            self.rod((xc, yr1 - 4, deck + 23), (xc, yr1 - 4, deck + 95), 1.6, "stack")
            # high-pressure send-out down to the turret / riser at the bow
            self.rod((xc, yr1, deck + 8), (xc, y1 - 6, deck + 8), 2, "pipe")


def build_A():
    S = Scene("A")
    P = REF["panels"]["A"]
    K = {k: v["fp"] for k, v in P["keys"].items()}
    shore = P["shoreline_x"]
    L_T = S.layer("LNG_TERMINAL", "A LNG import terminal (onshore)")
    L_J = S.layer("LNG_JETTY", "A Jetty trestle and berth")
    S.lay_marine = S.layer("MARINE", "LNG carrier and harbour craft")
    L_P = S.layer("LNG_PIPING", "A LNG and gas piping, buried send-out pipeline")

    bx0, bx1, by0, by1 = P["boundary"]
    S.item(L_T, "Terminal plot (as drawn on sheet 15)", P["boundary"], (0, .3), basis="drawing")
    S.box(bx0, bx1, by0, by1, -.3, .25, "gravel")
    S.fence(bx0, bx1, by0, by1, gap=((bx0, by1, bx0, by0), (.52, .6)))
    # internal roads and the connection to the plant's east ring road
    S.item(L_T, "Terminal roads (30 ft)", (2420, bx1, by0, by1), (0, .32))
    for (x0, x1, y0, y1) in ((2420, bx0 + 40, 560, 590), (bx0 + 10, bx0 + 40, by0 + 20, by1 - 20),
                             (bx0 + 10, 3440, 560, 590), (3400, 3430, by0 + 20, by1 - 20),
                             (bx0 + 10, 3430, 1390, 1420), (bx0 + 10, 3430, by0 + 20, by0 + 50)):
        S.box(x0, x1, y0, y1, -.1, .32, "road")

    # 1 LNG tank, 160,000 m3 full containment, ~270 ft dia x 160 ft
    fp = K["1"]
    cx, cy, R = (fp[0] + fp[1]) / 2, (fp[2] + fp[3]) / 2, (fp[1] - fp[0]) / 2
    S.item(L_T, "1 LNG tank 160,000 m3, full containment (Sabine Pass class, ~270 ft x 160 ft)", fp, (0, 160),
           tag="LNG-TK1", key="1", basis="sheet 15 / Matrix Service", shape="circle")
    S.rod((cx, cy, 0), (cx, cy, 5), R + 6, "concrete", seg=72)                  # raised pile cap
    S.rod((cx, cy, 5), (cx, cy, 136), R, "tankwall", seg=72)                    # pre-stressed concrete outer wall
    S.rod((cx, cy, 134), (cx, cy, 137), R + 1.2, "concrete", seg=72)            # ring beam
    S.dome(cx, cy, 137, R + .5, 23, "tankroof", n=10)
    # roof platform, in-tank pump columns and relief valves
    S.box(cx - 30, cx + 30, cy - 16, cy + 16, 158, 159, "grating")
    for k in range(3):
        S.rod((cx - 18 + 18 * k, cy, 159), (cx - 18 + 18 * k, cy, 172), 2.2, "pump")
    for a in range(8):
        t = a * math.pi / 4
        S.rod((cx + (R - 30) * math.cos(t), cy + (R - 30) * math.sin(t), 150),
              (cx + (R - 30) * math.cos(t), cy + (R - 30) * math.sin(t), 158), 1, "red")
    # stair tower and bridge to the roof (south-east), crane on the roof
    tx, ty = cx + (R + 22) * math.cos(-.9), cy + (R + 22) * math.sin(-.9)
    S.ladder_tower(tx, ty, 16, 150)
    S.box(tx - 3, cx + 12, ty - 2, ty + 2, 149.5, 150.5, "grating")
    S.rod((tx, ty, 150), (cx + 10, cy - 12, 158), .3, "rail")
    S.rod((cx + 22, cy + 10, 159), (cx + 22, cy + 10, 185), 1, "crane")
    S.rod((cx + 22, cy + 10, 185), (cx - 12, cy + 10, 180), .7, "crane")

    # 2 vaporizers x4 (2 duty + 2 standby), open-rack type (seawater)
    fp = K["2"]
    S.item(L_T, "2 Vaporizers x4, 2 duty + 2 standby (open rack, seawater)", fp, (0, 32), tag="VAP", key="2",
           basis="EcoElectrica (4 units)")
    w = (fp[1] - fp[0] - 30) / 4
    for i in range(4):
        x0 = fp[0] + 6 + i * (w + 6)
        S.box(x0, x0 + w, fp[2] + 12, fp[3] - 12, 0, 4, "concrete")             # seawater basin
        S.box(x0 + 4, x0 + w - 4, fp[2] + 18, fp[3] - 18, 4, 27, "radiator")      # finned panels
        S.box(x0 + 2, x0 + w - 2, fp[2] + 14, fp[3] - 14, 27, 31, "steel")       # distribution trough
        S.rod((x0 + w / 2, fp[2] + 8, 6), (x0 + w / 2, fp[3] - 8, 6), 1.6, "lngpipe")
    S.rod((fp[0] + 2, fp[2] + 5, 6), (fp[1] - 2, fp[2] + 5, 6), 2.6, "pipe")      # gas header
    S.rod((fp[0] + 2, fp[3] - 5, 3), (fp[1] - 2, fp[3] - 5, 3), 3.2, "seawater")  # seawater header

    # 3 HP send-out pumps (MV motors)
    fp = K["3"]
    S.item(L_T, "3 HP send-out pumps, MV motors", fp, (0, 36), tag="HP-P", key="3")
    S.box(fp[0] + 3, fp[1] - 3, fp[2] + 3, fp[3] - 3, 0, .8, "concrete")
    for i in range(3):
        for j in range(2):
            x, y = fp[0] + 22 + i * 32, fp[2] + 30 + j * 40
            S.rod((x, y, .8), (x, y, 20), 3, "pump")
            S.rod((x, y, 20), (x, y, 28), 3.6, "motor")
    for (x, y) in ((fp[0] + 6, fp[2] + 6), (fp[1] - 6, fp[2] + 6), (fp[0] + 6, fp[3] - 6), (fp[1] - 6, fp[3] - 6)):
        S.rod((x, y, 0), (x, y, 35), .7, "steel")
    S.box(fp[0] + 4, fp[1] - 4, fp[2] + 4, fp[3] - 4, 35, 36, "roof")

    # 4 boil-off gas compressors
    fp = K["4"]
    S.item(L_T, "4 Boil-off gas compressors", fp, (0, 44), tag="BOG", key="4")
    S.box(fp[0] + 5, fp[1] - 5, fp[2] + 5, fp[3] - 30, 0, 34, "building")
    S.prism(fp[0] + 5, fp[1] - 5, fp[2] + 5, fp[3] - 30, 34, 42, "roof", ridge="x")
    for i in range(3):
        S.rod((fp[0] + 25 + i * 40, fp[3] - 16, 0), (fp[0] + 25 + i * 40, fp[3] - 16, 26), 6, "tank")   # suction drums
    S.box(fp[0] + 10, fp[1] - 10, fp[3] - 28, fp[3] - 6, 18, 20, "grating")

    # 5 terminal substation + MCC e-house
    fp = K["5"]
    S.item(L_T, "5 Terminal substation + MCC e-house", fp, (0, 55), tag="T-SUB", key="5")
    S.box(fp[0] + 5, fp[1] - 5, fp[2] + 5, fp[3] - 5, -.2, .3, "gravel")
    S.box(fp[0] + 10, fp[0] + 120, fp[3] - 45, fp[3] - 10, 0, 4, "concrete")
    S.box(fp[0] + 10, fp[0] + 120, fp[3] - 45, fp[3] - 10, 4, 20, "ehouse")
    for i in range(2):
        x = fp[0] + 22 + i * 50
        S.box(x, x + 26, fp[2] + 12, fp[2] + 36, 0, 17, "xfmr")
        S.box(x - 5, x, fp[2] + 14, fp[2] + 34, 2, 15, "radiator")
        for k in range(3):
            S.rod((x + 5 + 8 * k, fp[2] + 24, 17), (x + 5 + 8 * k, fp[2] + 24, 25), .7, "insulator")
    S.box(fp[0] + 58, fp[0] + 62, fp[2] + 8, fp[2] + 42, 0, 22, "concrete")      # fire wall
    gx = fp[1] - 30                                                                # incoming line gantry
    for y in (fp[2] + 15, fp[3] - 15):
        S.rod((gx, y, 0), (gx, y, 48), 1, "steel")
        S.rod((gx + 20, y, 0), (gx + 20, y, 48), 1, "steel")
        S.box(gx - 1, gx + 21, y - 1, y + 1, 46, 48, "steel")

    # 6 control building + fire water
    fp = K["6"]
    S.item(L_T, "6 Control building + fire water", fp, (0, 40), tag="T-CB", key="6")
    S.box(fp[0] + 5, fp[0] + 75, fp[2] + 5, fp[3] - 30, 0, 22, "building")
    S.box(fp[0] + 5, fp[0] + 75, fp[2] + 5, fp[3] - 30, 22, 23.5, "roof")
    S.box(fp[0] + 5.2, fp[0] + 74.8, fp[2] + 4.7, fp[2] + 5, 8, 18, "glass")
    S.rod((fp[1] - 22, fp[3] - 22, 0), (fp[1] - 22, fp[3] - 22, 38), 17, "tank", seg=40)
    S.box(fp[1] - 40, fp[1] - 5, fp[2] + 5, fp[2] + 30, 0, 12, "building")

    # 7 send-out metering + ESD
    fp = K["7"]
    S.item(L_T, "7 Send-out metering + ESD", fp, (0, 16), tag="T-MET", key="7")
    S.box(fp[0] + 4, fp[1] - 4, fp[2] + 4, fp[3] - 4, 0, .5, "concrete")
    for k in range(2):
        y = fp[2] + 25 + k * 30
        S.rod((fp[0] + 8, y, 4), (fp[1] - 8, y, 4), 1.4, "pipe")
        S.box(fp[0] + 30, fp[0] + 42, y - 3, y + 3, 1, 7, "equip")
        S.box(fp[1] - 22, fp[1] - 16, y - 2, y + 2, 5, 10, "red")                   # ESD actuators
    S.box(fp[0] + 4, fp[1] - 4, fp[2] + 10, fp[3] - 10, 14, 15, "roof")
    for (x, y) in ((fp[0] + 6, fp[2] + 12), (fp[1] - 6, fp[2] + 12), (fp[0] + 6, fp[3] - 12), (fp[1] - 6, fp[3] - 12)):
        S.rod((x, y, 0), (x, y, 14), .4, "steel")

    # 8 seawater intake (open-rack vaporizers)
    fp = K["8"]
    S.item(L_T, "8 Seawater intake + pump house", fp, (-14, 26), tag="SW-IN", key="8")
    S.box(fp[0] + 5, fp[1], fp[2] + 8, fp[3] - 8, SEA - 6, 5, "concrete")
    S.box(fp[0] + 10, fp[1] - 25, fp[2] + 14, fp[3] - 14, 5, 22, "building")
    S.prism(fp[0] + 10, fp[1] - 25, fp[2] + 14, fp[3] - 14, 22, 26, "roof", ridge="y")
    for k in range(3):
        y = fp[2] + 25 + k * 25
        S.rod((fp[1] - 16, y, 5), (fp[1] - 16, y, 16), 2.2, "motor")
        S.rod((fp[1], y, SEA - 3), (shore + 170, y, SEA - 9), 2.4, "seawater")      # intake pipes into the sea
    S.item(L_P, "Seawater supply to the vaporizers", (K["2"][0], fp[0] + 10, fp[2] - 12, fp[2] - 4), (0, 6))
    S.pipe_path([(fp[0] + 10, fp[2] - 8), (K["2"][1] + 30, fp[2] - 8), (K["2"][1] + 30, K["2"][3] - 5),
                 (K["2"][1], K["2"][3] - 5)], 4, 2.6, "seawater", bents=30)

    # 9 vent / flare
    fp = K["9"]
    fx, fy = (fp[0] + fp[1]) / 2, (fp[2] + fp[3]) / 2
    S.item(L_T, "9 Vent / flare", fp, (0, 186), tag="FLARE", key="9", shape="circle")
    S.rod((fx, fy, 0), (fx, fy, 180), 2.4, "stack")
    S.rod((fx, fy, 180), (fx, fy, 188), 3.2, "red")
    for a in range(3):
        t = a * 2 * math.pi / 3
        for h0, h1 in ((0, 90), (90, 170)):
            r0, r1 = 13 - 11 * h0 / 170, 13 - 11 * h1 / 170
            S.rod((fx + r0 * math.cos(t), fy + r0 * math.sin(t), h0), (fx + r1 * math.cos(t), fy + r1 * math.sin(t), h1),
                  .6, "steel")
    S.item(L_T, "Flare knock-out drum", (fx - 45, fx - 15, fy - 6, fy + 6), (0, 16))
    S.rod((fx - 45, fy, 8), (fx - 15, fy, 8), 6, "tank")

    # piping (sheet 15 dotted blue: LNG; dashed brown: gas send-out)
    dashed = {tuple(map(tuple, d["pts"][:2])): d["pts"] for d in P["dashed"] if d["pts"]}
    jetty_lng = next(p for k, p in dashed.items() if k[0][0] > 5000)
    tank_to_pumps = next(p for k, p in dashed.items() if abs(k[0][0] - cx) < 2)
    vap_to_meter = next(p for k, p in dashed.items() if abs(k[0][1] - 449.8) < 2)
    sendout = next(p for k, p in dashed.items() if abs(k[0][0] - K["7"][0]) < 2)
    cable = next(p for k, p in dashed.items() if abs(k[0][1] - 941.9) < 2)
    # tank to the jetty root: along the drawn diagonal, on T-bents, 3 LNG + 1 vapour line
    onshore = [(jetty_lng[1][0], jetty_lng[1][1]), (jetty_lng[2][0] + 12, jetty_lng[2][1])]
    S.item(L_P, "LNG unloading lines, tank to jetty (3 LNG + 1 vapour)",
           (onshore[1][0], onshore[0][0], onshore[0][1] - 10, onshore[1][1] + 10), (0, 20))
    for k, (dy, r) in enumerate(((-6, 1.8), (-2, 1.8), (2, 1.8), (6, 1.3))):
        S.pipe_path([(x, y + dy) for (x, y) in onshore], 16, r, "lngpipe", bents=40 if k == 0 else 0)
    S.rod((onshore[1][0], onshore[1][1], 16), (onshore[1][0], onshore[1][1], 136), 1.8, "lngpipe")     # riser
    S.item(L_P, "LNG to the send-out pumps", (K["3"][0], cx + 4, K["3"][3], cy - R), (0, 18))
    S.pipe_path([(cx, cy - R - 4)] + [tuple(p) for p in tank_to_pumps[1:3]] + [(K["3"][0] + 50, K["3"][3])],
                14, 1.8, "lngpipe", bents=40)
    S.item(L_P, "Send-out gas, vaporizers to metering", (vap_to_meter[1][0] - 4, K["2"][0], K["2"][2],
                                                         vap_to_meter[2][1]), (0, 8))
    S.pipe_path([tuple(p) for p in vap_to_meter], 4, 2.6, "pipe", bents=30)
    # buried send-out pipeline to the plant's pipeline M&R (shown as its right of way)
    S.item(L_P, "Buried send-out pipeline to the plant M&R (right of way)",
           (sendout[-1][0] - 10, sendout[0][0], sendout[0][1] - 10, sendout[2][1] + 30), (-.2, 4))
    row = [tuple(p) for p in sendout]
    row = [row[0], row[1], (row[2][0], row[2][1] + 18), (row[3][0], row[3][1] + 18)]
    S.row_strip(row, 16)
    # substation cable trench to pumps, BOG and intake (orange on the sheet)
    S.item(L_P, "MV cable trench, substation to pumps, BOG and intake", (K["5"][1], K["8"][0], 600, 610), (-.2, .4))
    S.box(K["5"][1], K["4"][0], 604, 610, -.2, .4, "concrete")
    S.box(K["4"][0] - 6, K["4"][0], 610, K["4"][2], -.2, .4, "concrete")
    # branches to the HP send-out pumps and on to the seawater intake pumps
    S.box(K["3"][0] + 50, K["3"][0] + 56, K["3"][3], 604, -.2, .4, "concrete")
    S.box(K["4"][1], K["8"][0] + 40, 604, 610, -.2, .4, "concrete")
    S.box(K["8"][0] + 34, K["8"][0] + 40, K["8"][3], 604, -.2, .4, "concrete")
    # terminal power: buried cable from the plant 230 kV yard (east end) to the terminal substation
    S.item(L_P, "Terminal power supply: buried cable from the plant switchyard (right of way)",
           (1940, K["5"][0], 140, 690), (-.2, .4))
    S.row_strip([(1940, 150), (2450, 150), (2450, 680), (K["5"][0], 680)], 6, color="corridor", markers=300)
    # relief / vent header from the tank roof to the flare knock-out drum, on T-bents over the roads
    ra = math.radians(45)
    rx, ry = cx + (R + 5) * math.cos(ra), cy + (R + 5) * math.sin(ra)
    S.item(L_P, "Relief header, tank to flare knock-out drum", (rx - 2, fx - 15, ry - 2, fy + 2), (0, 150))
    S.rod((rx, ry, 150), (rx, ry, 18), 1.2, "pipe")
    S.rod((cx + (R - 8) * math.cos(ra), cy + (R - 8) * math.sin(ra), 152), (rx, ry, 150), 1.2, "pipe")
    S.pipe_path([(rx, ry), (rx, fy), (fx - 45, fy)], 18, 1.2, "pipe", bents=40)
    S.rod((fx - 45, fy, 18), (fx - 45, fy, 8), 1.2, "pipe")
    # seawater outfall: vaporizer discharge back to the sea, south of the pumps and the intake
    S.item(L_P, "Seawater outfall, vaporizers to the sea", (K["2"][1] - 25, shore + 120, 334, K["2"][2]), (SEA - 10, 6))
    S.pipe_path([(K["2"][1] - 20, K["2"][2]), (K["2"][1] - 20, 340), (shore - 5, 340)], 3, 2.6, "seawater")
    S.rod((shore - 5, 340, 3), (shore + 120, 340, SEA - 8), 2.6, "seawater")

    # 10 jetty trestle ~1,700 ft (EcoElectrica)
    fp = K["10"]
    jx0, jx1, jy0, jy1 = fp
    S.item(L_J, "10 Jetty trestle ~1,700 ft", fp, (SEA - 40, 26), tag="JETTY", key="10", basis="EcoElectrica")
    S.box(jx0 - 40, jx1, jy0, jy1, 10, 13, "concrete")
    S.box(jx0 - 40, shore + 6, jy0 - 4, jy1 + 4, -.5, 10, "concrete")                   # onshore abutment
    x = shore + 24
    while x < jx1:
        for y in (jy0 + 4, jy1 - 4):
            S.rod((x, y, SEA - 40), (x, y, 10), 1.5, "pile")
        S.box(x - 2, x + 2, jy0, jy1, 8, 10, "concrete")
        # pipe-rack bent on the north half of the deck
        S.rod((x, jy1 - 4, 13), (x, jy1 - 4, 21), .5, "steel")
        S.rod((x, jy0 + 20, 13), (x, jy0 + 20, 21), .5, "steel")
        S.box(x - .4, x + .4, jy0 + 19, jy1 - 3, 20.4, 21, "steel")
        x += 60
    for k, (y, r) in enumerate(((jy0 + 23, 1.8), (jy0 + 27, 1.8), (jy0 + 31, 1.8), (jy1 - 5, 1.3))):
        S.rod((jx0 - 30, y, 22.2), (jx1 + 60, y, 22.2), r, "lngpipe")
    # tie the onshore lines (z 16, along the diagonal) into the jetty rack (z 22)
    for dy in (-6, -2, 2, 6):
        S.rod((onshore[0][0], onshore[0][1] + dy, 16), (jx0 - 30, onshore[0][1] + dy, 22.2), 1.6, "lngpipe")
    for y in (jy0 + .3, jy1 - .3):
        S.box(jx0 - 40, jx1, y - .15, y + .15, 13, 16.5, "rail")
    x = jx0 + 60
    while x < jx1:
        S.rod((x, jy0 + 1, 13), (x, jy0 + 1, 40), .35, "steel")
        S.box(x - .8, x + .8, jy0 + 1, jy0 + 5, 39, 40, "lamp")
        x += 180
    S.box(jx0 - 40, jx1, jy0 + 2, jy0 + 5, 13, 14.2, "copper_dark")                  # cable tray (orange dashed)

    # 11 berth: 4 unloading arms, 3 LNG + 1 vapour
    fp = K["11"]
    S.item(L_J, "11 Berth platform: 4 unloading arms, 3 LNG + 1 vapour", fp, (SEA - 40, 90), tag="BERTH", key="11")
    S.box(fp[0], fp[1], fp[2], fp[3], 12, 16, "concrete")
    for x in range(int(fp[0]) + 10, int(fp[1]), 25):
        for y in range(int(fp[2]) + 10, int(fp[3]), 30):
            S.rod((x, y, SEA - 40), (x, y, 12), 1.5, "pile")
    arm_x = fp[1] - 16
    for k, y in enumerate(fp[2] + 60 + 26 * i for i in range(4)):
        col = "lngpipe" if k < 3 else "steel"
        S.rod((arm_x, y, 16), (arm_x, y, 46), 1.6, col)                                       # riser
        S.rod((arm_x, y, 46), (arm_x - 8, y, 80), 1.1, col)                                   # inboard arm
        S.rod((arm_x - 8, y, 80), (fp[1] + 12, y, 52), 1.0, col)                              # outboard arm
        S.box(arm_x - 16, arm_x - 8, y - 3, y + 3, 76, 84, "amber")                           # counterweight
        S.box(arm_x - 3, arm_x + 3, y - 3, y + 3, 16, 20, "equip")
    S.ladder_tower(fp[0] + 22, fp[3] - 20, 14, 62)                                             # gangway tower
    S.rod((fp[0] + 22, fp[3] - 20, 62), (fp[1] + 30, fp[3] - 40, 48), .6, "rail")
    for (x, y) in ((fp[0] + 18, fp[2] + 16), (fp[0] + 60, fp[3] - 14)):                         # fire monitors
        S.rod((x, y, 16), (x, y, 60), .8, "red")
        S.box(x - 3, x + 3, y - 3, y + 3, 60, 63, "red")
    S.box(fp[0] + 30, fp[0] + 60, fp[2] + 10, fp[2] + 40, 16, 28, "ehouse")                  # jetty control / ESD room

    # breasting and mooring dolphins with walkways
    hull = P["vessels"][0]
    S.item(L_J, "Breasting and mooring dolphins, walkways (typical)", (fp[0] - 60, hull[0], hull[2] - 150, hull[3] + 150),
           (SEA - 30, 24))
    for y in (hull[2] + 190, hull[3] - 190):
        S.box(fp[1] - 25, hull[0] - 5, y - 18, y + 18, SEA - 10, 18, "concrete")
        S.box(hull[0] - 5, hull[0] - 1, y - 14, y + 14, 0, 16, "fanhub")                    # fenders
        S.box(fp[1] - 8, fp[1] - 25, min(y, fp[2]) if y < fp[2] else fp[3], max(y, fp[3]) if y > fp[3] else fp[2],
              17, 18, "grating")
    for y in (hull[2] - 120, hull[3] + 120):
        S.box(fp[0] + 20, fp[0] + 50, y - 15, y + 15, SEA - 10, 16, "concrete")
        S.rod((fp[0] + 35, y, 16), (fp[0] + 35, y, 20), 2, "fanhub")                         # quick-release hook
        S.box(fp[0] + 33, fp[0] + 37, min(y, fp[2]) if y < fp[2] else fp[3], max(y, fp[3]) if y > fp[3] else fp[2],
              15, 16, "grating")

    # LNG carrier at the berth, ~294 m LOA (AES Andres berth max), bow north as drawn
    S.vessel("LNG carrier ~294 m LOA, Moss type, at the berth", "LNGC", hull, P["cargo_domes"])
    # mooring lines from the carrier to the mooring and breasting dolphins
    S.item(S.lay_marine, "Mooring lines", (fp[0], hull[1], hull[2] - 130, hull[3] + 130), (16, 44))
    for (tx, ty) in ((fp[0] + 35, hull[2] - 120), (fp[0] + 35, hull[3] + 120)):
        for dy in (-4, 4):
            S.rod((tx, ty, 18), (hull[0] + 6, (hull[2] + 40 if ty < hull[2] else hull[3] - 60) + dy, 44), .25, "rope")
    coastal_detail.detail_A(S, K)
    tug(S, hull[1] + 140, hull[2] + 160, 0)
    tug(S, hull[1] + 90, hull[3] + 60, 1)
    return S, dict(variant="A", shoreline_x=shore, sea_level=SEA, terminal=P["boundary"],
                   label="Onshore LNG import terminal beside the plant (sheet 15, panel A)")


def tug(S, x, y, k):
    S.item(S.lay_marine, f"Harbour tug {k + 1} (illustrative)", (x - 18, x + 18, y - 50, y + 50), (SEA - 14, 34))
    # hull in two sections: square-ish stern half, pointed bow half
    S.hexa([(x - 13, y - 45, SEA - 13), (x + 13, y - 45, SEA - 13), (x + 14, y + 5, SEA - 14), (x - 14, y + 5, SEA - 14),
            (x - 17, y - 50, SEA + 7), (x + 17, y - 50, SEA + 7), (x + 18, y + 5, SEA + 8), (x - 18, y + 5, SEA + 8)], "tug")
    S.hexa([(x - 14, y + 5, SEA - 14), (x + 14, y + 5, SEA - 14), (x + 1, y + 44, SEA - 6), (x - 1, y + 44, SEA - 6),
            (x - 18, y + 5, SEA + 8), (x + 18, y + 5, SEA + 8), (x + 1, y + 50, SEA + 11), (x - 1, y + 50, SEA + 11)], "tug")
    S.box(x - 10, x + 10, y - 22, y + 16, SEA + 7, SEA + 17, "super")
    S.box(x - 8, x + 8, y + 2, y + 14, SEA + 17, SEA + 26, "super")
    S.box(x - 8.2, x + 8.2, y + 13.8, y + 14.1, SEA + 19, SEA + 25, "glass")
    S.rod((x - 5, y - 8, SEA + 17), (x - 5, y - 8, SEA + 30), 1.4, "hull")
    S.rod((x + 5, y - 8, SEA + 17), (x + 5, y - 8, SEA + 30), 1.4, "hull")
    S.rod((x, y + 46, SEA + 6), (x, y + 51, SEA + 6), 3.5, "fanhub")


def build_B():
    S = Scene("B")
    P = REF["panels"]["B"]
    K = {k: v["fp"] for k, v in P["keys"].items()}
    shore = P["shoreline_x"]
    L_T = S.layer("LNG_LANDFALL", "B Landfall valve station and buried pipeline")
    S.lay_marine = S.layer("MARINE", "FSRU, LNG carrier and mooring")
    dx = FSRU_OFFSET

    # 12 landfall valve station: ESD, pig receiver, metering
    fp = K["12"]
    S.item(L_T, "12 Landfall valve station: ESD, pig receiver, metering", fp, (0, 20), tag="LVS", key="12")
    S.box(fp[0], fp[1], fp[2], fp[3], -.3, .25, "gravel")
    S.fence(fp[0], fp[1], fp[2], fp[3], gap=((fp[0], fp[3], fp[0], fp[2]), (.4, .6)))
    ym = (fp[2] + fp[3]) / 2
    S.rod((fp[1] - 10, ym, 5), (fp[0] + 60, ym, 5), 2.6, "pipe")                  # incoming subsea line
    S.rod((fp[1] - 70, ym + 20, 5), (fp[1] - 20, ym + 20, 5), 3.4, "amber")        # pig receiver barrel
    S.rod((fp[1] - 20, ym + 20, 5), (fp[1] - 12, ym, 5), 2, "pipe")
    for x in (fp[0] + 70, fp[0] + 100):
        S.box(x - 3, x + 3, ym - 3, ym + 3, 3, 12, "red")                           # ESD valves
    S.box(fp[0] + 12, fp[0] + 58, fp[2] + 10, fp[2] + 40, 0, 14, "building")        # metering shelter
    S.box(fp[0] + 12, fp[0] + 58, fp[2] + 10, fp[2] + 40, 14, 15.5, "roof")
    S.box(fp[0] + 110, fp[0] + 140, fp[3] - 30, fp[3] - 10, 0, 10, "ehouse")        # control kiosk, CP rectifier
    S.rod((fp[0] + 150, fp[3] - 20, 0), (fp[0] + 150, fp[3] - 20, 45), .5, "steel")  # SCADA mast
    # buried pipeline to the plant M&R, and the landfall to the shoreline
    land = next(d["pts"] for d in P["dashed"] if d["pts"] and d["pts"][0][0] < fp[0] + 2)
    S.item(L_T, "Buried gas pipeline to the plant M&R (right of way)", (1720, fp[0], land[0][1] - 10, 1950), (-.2, 4))
    S.row_strip([tuple(land[0]), tuple(land[1]), (land[2][0], land[2][1] + 18), (land[3][0], land[3][1] + 18)], 16)
    S.item(L_T, "Subsea pipeline landfall (shore approach, buried)", (fp[1], shore + 40, ym - 10, ym + 10), (-.2, 4))
    S.row_strip([(fp[1], ym), (shore - 8, ym)], 16)
    S.box(shore - 30, shore - 6, ym - 12, ym + 12, -.3, 2.5, "concrete")             # beach valve pit

    # 14 submerged soft yoke: mooring tower + gas riser, ~21,000 ft offshore
    fp = K["14"]
    yx, yy = (fp[0] + fp[1]) / 2 + dx, (fp[2] + fp[3]) / 2
    S.item(S.lay_marine, "14 Soft-yoke mooring tower + gas riser", (fp[0] + dx, fp[1] + dx, fp[2], fp[3]), (SEA - 60, 60),
           tag="YOKE", key="14", shape="circle")
    tyy = yy + 21.5                        # tower in the north half of the drawn circle, the yoke reaches the bow
    for sx in (-12, 12):
        for sy in (-12, 12):
            S.rod((yx + sx * 1.3, tyy + sy * 1.3, SEA - 60), (yx + sx, tyy + sy, 30), 1.4, "steel")
    for zz in (SEA - 20, 10):
        S.box(yx - 13, yx + 13, tyy - 13, tyy + 13, zz, zz + 1.5, "steel")
    S.box(yx - 14, yx + 14, tyy - 14, tyy + 14, 30, 34, "steel")
    S.rod((yx, tyy, 34), (yx, tyy, 46), 12, "amber")                                  # turntable
    S.rod((yx, tyy - 10, 40), (yx, yy - 20, 40), 2, "steel")                         # yoke arm
    S.rod((yx, tyy, 46), (yx, tyy, 60), 1, "steel")
    S.rod((yx, tyy, SEA - 60), (yx, tyy, 34), 1.8, "pipe")                           # gas riser

    # 15 FSRU 170,000 m3 with onboard regas; 16 LNG carrier alongside (ship to ship)
    domes = [d for d in P["cargo_domes"]]
    fsru = K["15"]
    fsru = [fsru[0] + dx, fsru[1] + dx, fsru[2], min(fsru[3], yy - 20)]
    S.vessel("15 FSRU 170,000 m3, regas onboard 14-21 million m3/day", "FSRU", fsru,
             [[d[0] + dx, d[1], d[2]] for d in domes if d[0] < K["15"][1]], regas=True, key="15")
    lngc = K["16"]
    lngc = [lngc[0] + dx, lngc[1] + dx, lngc[2], lngc[3]]
    S.vessel("16 LNG carrier, ship-to-ship transfer", "LNGC-STS", lngc,
             [[d[0] + dx, d[1], d[2]] for d in domes if d[0] > K["15"][1]], key="16")
    S.item(S.lay_marine, "STS fenders and transfer hoses", (fsru[1], lngc[0], lngc[2] + 100, lngc[3] - 100), (SEA - 4, 52))
    for y in range(int(lngc[2]) + 160, int(lngc[3]) - 120, 140):
        S.rod((fsru[1] + 25, y - 12, SEA + 2), (fsru[1] + 25, y + 12, SEA + 2), 11, "fanhub", seg=20)
    ym = (sorted(d[1] for d in domes if d[0] < K["15"][1])[1] + sorted(d[1] for d in domes if d[0] < K["15"][1])[2]) / 2
    for k in range(3):
        S.rod((fsru[1] + 1, ym - 6 + 6 * k, 46), (lngc[0] - 1, ym - 6 + 6 * k, 46), .9, "rope")
    coastal_detail.detail_B(S, K)
    tug(S, lngc[1] + 160, lngc[2] + 140, 0)
    return S, dict(variant="B", shoreline_x=shore, sea_level=SEA, fsru_offset_ft=round(dx), yoke=[round(yx), round(yy)],
                   label="FSRU moored offshore (sheet 15, panel B; distance to scale in the model)")


def write(S, meta):
    """An overlay on sk3x1_model.json: the Blender build merges it with --overlay."""
    m = dict(title=BASE["title"] + f" | coastal variant {S.variant} (SK-3X1-15)", base="sk3x1_model.json",
             disclaimer=BASE["disclaimer"], coastal=meta, layers=S.layers, items=S.items, parts=S.parts)
    path = os.path.join(HERE, f"sk3x1_coastal_{S.variant}.json")
    json.dump(m, open(path, "w"), indent=0)
    keyed = sum(1 for it in S.items if it["key"])
    print(f"wrote {os.path.relpath(path, PLANT)}: +{len(S.items)} items ({keyed} keyed to sheet 15), "
          f"+{len(S.parts)} parts, layers {', '.join(S.layers)}")


if __name__ == "__main__":
    for build in (build_A, build_B):
        write(*build())
