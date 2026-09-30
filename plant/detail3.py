"""Detail pass (LOD 3): building and equipment dressing for close views.

Runs after detail.py and adds, as "d": 1 parts (typical, not from the drawing):
- buildings: window bands, a concrete base band, rooftop HVAC units with fans, downspouts;
- e-houses: wall panel seams and a roof overhang;
- tanks: spiral stair with handrail, roof handrail and vent, nozzles and a manway;
- RICE engine hall: roof ventilators, charge-air filters per engine, roll-up doors;
- simple-cycle and trailer-mounted turbines: enclosure ventilation fans, filter hoods;
- BESS containers: end-wall HVAC units and door seams;
- main stacks: aviation warning lights;
- site: lane markings on the 30 ft roads and cars in the parking lot.
verify.py treats all of it as dressing (bounds check only).
"""
import math
import random


class Detail3:
    def __init__(self, items, parts):
        self.items, self.parts = items, parts
        self.n0 = len(parts)
        self.own = {}
        for p in parts:
            if not p.get("d"):
                self.own.setdefault(p["item"], []).append(p)

    def box(self, it, x0, x1, y0, y1, z0, z1, c):
        self.parts.append(dict(kind="box", min=[round(min(x0, x1), 2), round(min(y0, y1), 2), round(z0, 2)],
                               max=[round(max(x0, x1), 2), round(max(y0, y1), 2), round(max(z1, z0 + .05), 2)],
                               color=c, item=it["id"], layer=it["layer"], d=1))

    def rod(self, it, a, b, r, c, r2=None, seg=8):
        self.parts.append(dict(kind="rod", a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=r,
                               r2=r if r2 is None else r2, color=c, seg=seg, item=it["id"], layer=it["layer"], d=1))

    def main_box(self, it, color):
        bs = [p for p in self.own.get(it["id"], []) if p["kind"] == "box" and p["color"] == color]
        return max(bs, key=lambda p: (p["max"][0] - p["min"][0]) * (p["max"][1] - p["min"][1]) * (p["max"][2] - p["min"][2]),
                   default=None)

    def run(self):
        self.buildings()
        self.ehouses()
        self.tanks()
        self.rice()
        self.turbine_packages()
        self.bess()
        self.stacks()
        self.site()
        return len(self.parts) - self.n0

    # ---------------------------------------------------------------------------------
    OFFICE = ("Gatehouse", "Control / admin building")
    ELECTRICAL = ("R1:",)
    WORKSHOP = ("Warehouse", "Maintenance building")

    def buildings(self):
        """Style each building by use: offices get window bands and an entrance canopy; the
        electrical building stays closed (louvres, doors); industrial buildings get ribbed
        metal cladding, a high translucent strip, roll-up doors, wall louvres and roof vents."""
        for it in self.items:
            if it["layer"].startswith(("R1_INTERIOR", "R4_INTERIOR")):
                continue
            b = self.main_box(it, "building")
            if b is None or b["min"][2] > .5:
                continue
            (x0, y0, _), (x1, y1, top) = b["min"], b["max"]
            W, D, h = x1 - x0, y1 - y0, top
            if W < 12 or D < 12 or h < 9:
                continue
            nm = it["name"]
            kind = ("office" if nm.startswith(self.OFFICE) else "electrical" if nm.startswith(self.ELECTRICAL)
                    else "industrial")
            e = .12
            # concrete base band (wainscot) all round
            self.box(it, x0 - e, x1 + e, y0 - e, y0, 0, 2.6, "concrete")
            self.box(it, x0 - e, x1 + e, y1, y1 + e, 0, 2.6, "concrete")
            self.box(it, x0 - e, x0, y0, y1, 0, 2.6, "concrete")
            self.box(it, x1, x1 + e, y0, y1, 0, 2.6, "concrete")
            faces = ((x0, x1, y0, "x", -1), (x0, x1, y1, "x", 1), (y0, y1, x0, "y", -1), (y0, y1, x1, "y", 1))

            def band(zb, zt, w, pitch, c, faces=faces):
                for (a0, a1, fixed, axis, sgn) in faces:
                    L = a1 - a0
                    n = int((L - 8) // pitch)
                    if n < 1:
                        continue
                    pad = (L - n * pitch + (pitch - w)) / 2
                    for k in range(n):
                        s0 = a0 + pad + pitch * k
                        if axis == "x":
                            self.box(it, s0, s0 + w, fixed, fixed + sgn * .14, zb, zt, c)
                        else:
                            self.box(it, fixed, fixed + sgn * .14, s0, s0 + w, zb, zt, c)

            if kind == "office":
                rows = [z for z in (h * .5 - 2,) if z > 4] if h < 22 else [6.5, 6.5 + 12]
                for zb in rows:
                    zt = zb + 4 if h >= 12 else zb + 3
                    if zt <= h - 1.5:
                        band(zb, zt, 6, 11, "window")
                # glazed entrance with a canopy on the south face
                xm = (x0 + x1) / 2
                self.box(it, xm - 5, xm + 5, y0 - .16, y0, 0, 9, "window")
                self.box(it, xm - 9, xm + 9, y0 - 8, y0, 10, 10.8, "roof")
                for xx in (xm - 8.3, xm + 8.3):
                    self.rod(it, (xx, y0 - 7.3, 0), (xx, y0 - 7.3, 10), .3, "steel", seg=8)
            elif kind == "electrical":
                band(h * .55, h * .55 + 3, 5, 24, "louvre")
            else:
                # industrial: ribbed metal cladding (recolour the primary walls and parapets)
                for p in self.own.get(it["id"], []):
                    if p["color"] == "building":
                        p["color"] = "rollup"
                # high translucent strip under the eaves, wall louvres at mid height
                band(h - 5.5, h - 3.2, 9, 10, "panel")
                band(h * .45, h * .45 + 3, 6, 30, "louvre", faces=faces[2:])
                # roll-up doors on the south face (more and bigger on the warehouse and workshop)
                big = nm.startswith(self.WORKSHOP)
                nd = (3 if W > 110 else 2) if big else (1 if W > 40 else 0)
                dw, dh = (16, min(18, h - 6)) if big else (12, min(12, h - 4))
                for k in range(nd):
                    xd = x0 + W * (k + 1) / (nd + 1) - dw / 2
                    self.box(it, xd, xd + dw, y0 - .2, y0, 0, dh, "rollup")
                    self.box(it, xd - .5, xd + dw + .5, y0 - .35, y0, dh, dh + 1, "steel")   # door head
                    for xx in (xd - 1.2, xd + dw + 1.2):                                     # bollards
                        self.rod(it, (xx, y0 - 2, 0), (xx, y0 - 2, 4), .35, "rail", seg=8)
                if big:
                    # skylight rows on the roof and ridge ventilators
                    for k in range(int((W - 20) // 24)):
                        xs = x0 + 14 + 24 * k
                        self.box(it, xs, xs + 8, y0 + D * .25, y1 - D * .25, top - 1.4, top - 1.0, "panel")
                    for k in range(3):
                        xv = x0 + W * (k + 1) / 4
                        self.box(it, xv - 2, xv + 2, (y0 + y1) / 2 - 2, (y0 + y1) / 2 + 2, top - 1.5, top + 2.5, "louvre")
                        self.box(it, xv - 2.6, xv + 2.6, (y0 + y1) / 2 - 2.6, (y0 + y1) / 2 + 2.6, top + 2.5, top + 3, "roof")
            # rooftop HVAC units with fan discs (offices and electrical rooms carry more)
            n = max(1, min(4, int(W * D / 3500))) if kind != "industrial" else 1
            for k in range(n):
                cx = x0 + W * (k + 1) / (n + 1)
                cy = y0 + D * .5 + (D * .2 if kind == "industrial" else 0)
                self.box(it, cx - 4, cx + 4, cy - 2.6, cy + 2.6, top, top + 3.8, "machine")
                self.rod(it, (cx - 1.8, cy, top + 3.8), (cx - 1.8, cy, top + 4.2), 1.5, "fan", seg=14)
                self.rod(it, (cx + 1.8, cy, top + 3.8), (cx + 1.8, cy, top + 4.2), 1.5, "fan", seg=14)
            # downspouts at the corners
            for (x, y) in ((x0 - .35, y0 - .35), (x1 + .35, y0 - .35), (x0 - .35, y1 + .35), (x1 + .35, y1 + .35)):
                self.rod(it, (x, y, .3), (x, y, top - .3), .22, "steel", seg=6)

    def ehouses(self):
        for it in self.items:
            b = self.main_box(it, "ehouse")
            if b is None:
                continue
            (x0, y0, z0), (x1, y1, z1) = b["min"], b["max"]
            W, D = x1 - x0, y1 - y0
            if W < 8 or D < 6:
                continue
            # vertical panel seams every 4 ft on the long faces
            if W >= D:
                for x in [x0 + 4 * k for k in range(1, int(W / 4))]:
                    for (y, s) in ((y0, -1), (y1, 1)):
                        self.box(it, x - .08, x + .08, y, y + s * .1, z0 + .2, z1 - .1, "roof")
            else:
                for y in [y0 + 4 * k for k in range(1, int(D / 4))]:
                    for (x, s) in ((x0, -1), (x1, 1)):
                        self.box(it, x, x + s * .1, y - .08, y + .08, z0 + .2, z1 - .1, "roof")
            # roof overhang / drip edge
            r = self.main_box(it, "roof")
            if r is not None:
                (rx0, ry0, rz0), (rx1, ry1, rz1) = r["min"], r["max"]
                self.box(it, rx0 - .6, rx1 + .6, ry0 - .6, ry1 + .6, rz1 - .3, rz1 + .07, "roof")   # top above the roof: no shared face

    def tanks(self):
        for it in self.items:
            if it["shape"] != "circle":
                continue
            shell = [p for p in self.own.get(it["id"], []) if p["kind"] == "rod" and p["color"] == "tank"
                     and p["a"][:2] == p["b"][:2]]
            if not shell:
                continue
            s = max(shell, key=lambda p: p["r"])
            cx, cy, r = s["a"][0], s["a"][1], s["r"]
            h = max(s["a"][2], s["b"][2])
            if r < 5 or h < 8:
                continue
            # spiral stair: outer and inner stringers, treads, handrail
            turns, a0 = min(.85, h / (2 * math.pi * r) * 2.2), math.radians(200)
            n = max(12, int(h / 1.2))
            prev = None
            for k in range(n + 1):
                t = k / n
                ang = a0 + t * turns * 2 * math.pi
                z = t * h
                ci, co = r + .4, r + 3.4
                pi = (cx + ci * math.cos(ang), cy + ci * math.sin(ang), z)
                po = (cx + co * math.cos(ang), cy + co * math.sin(ang), z)
                if k % 2 == 0 and k < n:
                    self.rod(it, pi, po, .18, "grating", seg=4)
                if prev:
                    self.rod(it, prev[0], pi, .12, "steel", seg=4)
                    self.rod(it, prev[1], po, .12, "steel", seg=4)
                    self.rod(it, (prev[1][0], prev[1][1], prev[1][2] + 3.4), (po[0], po[1], z + 3.4), .08, "rail", seg=4)
                if k % 3 == 0:
                    self.rod(it, po, (po[0], po[1], z + 3.4), .07, "rail", seg=4)
                prev = (pi, po)
            # roof handrail arc near the stair head, roof vent and a manway on the roof
            ang_top = a0 + turns * 2 * math.pi
            for k in range(8):
                u0, u1 = ang_top - .5 + k * .14, ang_top - .5 + (k + 1) * .14
                rr = r - 1.2
                self.rod(it, (cx + rr * math.cos(u0), cy + rr * math.sin(u0), h + 3.6),
                         (cx + rr * math.cos(u1), cy + rr * math.sin(u1), h + 3.6), .08, "rail", seg=4)
            self.rod(it, (cx, cy, h + r * .18 - .2), (cx, cy, h + r * .18 + 2.2), .9, "steel", seg=10)
            self.rod(it, (cx, cy, h + r * .18 + 2.2), (cx, cy, h + r * .18 + 2.8), 1.4, "steel", seg=10)
            # nozzles near the base and a shell manway
            for ang in (math.radians(20), math.radians(80)):
                a = (cx + r * math.cos(ang), cy + r * math.sin(ang), 3)
                b = (cx + (r + 2.2) * math.cos(ang), cy + (r + 2.2) * math.sin(ang), 3)
                self.rod(it, a, b, .7, "pipe", seg=10)
                self.rod(it, b, (b[0] + .01, b[1], b[2]), 1.1, "pipe", seg=10)
            ang = math.radians(310)
            self.rod(it, (cx + r * math.cos(ang), cy + r * math.sin(ang), 3.5),
                     (cx + (r + .8) * math.cos(ang), cy + (r + .8) * math.sin(ang), 3.5), 1.3, "steel", seg=14)

    def rice(self):
        for it in self.items:
            if not it["name"].startswith("RICE engine hall"):
                continue
            x0, x1, y0, y1 = it["fp"]
            hall = self.main_box(it, "hall")
            if hall is None:
                continue
            top = hall["max"][2]
            n = int(round((x1 - x0 - 16) / 28))
            ym = (y0 + y1) / 2
            for k in range(n):
                x = x0 + 11 + 28 * k + 9.5
                # roof ventilator on the ridge
                self.box(it, x - 2.5, x + 2.5, ym - 2.5, ym + 2.5, top + 5.5, top + 8.5, "louvre")
                self.box(it, x - 3.2, x + 3.2, ym - 3.2, ym + 3.2, top + 8.5, top + 9.1, "roof")
                # charge-air filter house on the north wall
                self.box(it, x - 6, x + 6, y1, y1 + 4.5, 16, 28, "filter")
                self.box(it, x - 6.3, x + 6.3, y1 + 4.5, y1 + 5, 15.5, 28.5, "louvre")
            # roll-up doors in both end walls
            for (xa, s) in ((x0, -1), (x1, 1)):
                self.box(it, xa, xa + s * .2, ym - 8, ym + 8, 0, 16, "rollup")
                self.box(it, xa, xa + s * .2, ym + 12, ym + 15.5, 0, 7.5, "door")

    def turbine_packages(self):
        for it in self.items:
            nm = it["name"]
            if not (nm.startswith(("SC-1:", "SC-2:", "SC-3:", "SC-4:")) or nm.startswith("TM-")):
                continue
            m = self.main_box(it, "machine")
            f = self.main_box(it, "filter")
            if m is not None:
                (x0, y0, _), (x1, y1, z1) = m["min"], m["max"]
                for k in range(3):
                    x = x0 + (x1 - x0) * (k + 1) / 4
                    self.rod(it, (x, (y0 + y1) / 2, z1), (x, (y0 + y1) / 2, z1 + 2.2), 1.6, "machine", seg=14)
                    self.rod(it, (x, (y0 + y1) / 2, z1 + 2.2), (x, (y0 + y1) / 2, z1 + 2.6), 1.9, "fan", seg=14)
            if f is not None:
                (x0, y0, z0), (x1, y1, z1) = f["min"], f["max"]
                # weather hoods on both long faces of the filter house
                for k in range(3):
                    z = z0 + (z1 - z0) * (k + .5) / 3
                    for (y, s) in ((y0, -1), (y1, 1)):
                        self.box(it, x0 + .4, x1 - .4, y, y + s * 1.6, z - 1.2, z + 1.8, "louvre")

    def bess(self):
        for p in list(self.parts):
            if p.get("d") or p["layer"] != "OPT_BESS" or p["color"] != "bess" or p["kind"] != "box":
                continue
            (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
            it = next(i for i in self.items if i["id"] == p["item"])
            if x1 - x0 > y1 - y0:          # container along x: HVAC on the east end, doors on the south face
                self.box(it, x1, x1 + 1.2, y0 + 1.5, y1 - 1.5, z0 + 3, z0 + 7.5, "machine")
                for k in range(1, 5):
                    x = x0 + (x1 - x0) * k / 5
                    self.box(it, x - .06, x + .06, y0 - .08, y0, z0 + .5, z1 - .6, "door")
            else:
                self.box(it, x0 + 1.5, x1 - 1.5, y1, y1 + 1.2, z0 + 3, z0 + 7.5, "machine")

    def stacks(self):
        for it in self.items:
            if it["tag"] not in ("STK-1", "STK-2", "STK-3") and not it["tag"].startswith("ABS-"):
                continue
            cx, cy = (it["fp"][0] + it["fp"][1]) / 2, (it["fp"][2] + it["fp"][3]) / 2
            r = (it["fp"][1] - it["fp"][0]) / 2
            top = it["z"][1]
            for z in (top - 3, top * .5):
                for ang in (0, 2.1, 4.2):
                    x, y = cx + (r + .5) * math.cos(ang), cy + (r + .5) * math.sin(ang)
                    self.box(it, x - .5, x + .5, y - .5, y + .5, z, z + 1, "red")

    def site(self):
        rnd = random.Random(14)
        for it in self.items:
            if it["layer"] != "SITE" or "road" not in it["name"].lower():
                continue
            x0, x1, y0, y1 = it["fp"]
            zt = it["z"][1] + .02
            if x1 - x0 > y1 - y0:
                yc = (y0 + y1) / 2
                for x in range(int(x0) + 20, int(x1) - 20, 40):
                    self.box(it, x, x + 12, yc - .25, yc + .25, zt - .05, zt, "lamp")
                for yy in (y0 + 1.2, y1 - 1.7):
                    self.box(it, x0 + 5, x1 - 5, yy, yy + .5, zt - .05, zt, "lamp")
            else:
                xc = (x0 + x1) / 2
                for y in range(int(y0) + 20, int(y1) - 20, 40):
                    self.box(it, xc - .25, xc + .25, y, y + 12, zt - .05, zt, "lamp")
                for xx in (x0 + 1.2, x1 - 1.7):
                    self.box(it, xx, xx + .5, y0 + 5, y1 - 5, zt - .05, zt, "lamp")
        park = next((i for i in self.items if i["name"] == "Parking"), None)
        if park:
            x0, x1, y0, y1 = park["fp"]
            zt = park["z"][1]
            colours = ["super", "hull", "door", "red", "equip", "machine", "super", "fanhub"]
            for row, yb in enumerate((y0 + 12, y0 + 70, y0 + 110, y0 + 168)):
                for x in range(int(x0) + 10, int(x1) - 10, 10):
                    if rnd.random() < .35:
                        continue
                    c = rnd.choice(colours)
                    self.box(park, x + 1.5, x + 7.5, yb, yb + 15, zt + .6, zt + 3.3, c)
                    self.box(park, x + 2, x + 7, yb + 4, yb + 11, zt + 3.3, zt + 5.0, "window" if c != "window" else "super")
                    for (wx, wy) in ((x + 1.6, yb + 3), (x + 7.4, yb + 3), (x + 1.6, yb + 12), (x + 7.4, yb + 12)):
                        self.rod(park, (wx - .3, wy, zt + 1.1), (wx + .3, wy, zt + 1.1), 1.05, "fanhub", seg=10)
                # painted bay lines
                for x in range(int(x0) + 10, int(x1) - 9, 10):
                    self.box(park, x - .15, x + .15, yb - 1, yb + 17, zt, zt + .03, "lamp")
            # EV charging: the two middle rows face a solar carport with a charger pedestal per bay
            ya, yb2 = y0 + 70, y0 + 110            # front edges of the two rows (cars at +0..+15)
            yc0, yc1 = ya + 17.5, yb2 - 2.5         # carport spans the aisle between them
            for x in range(int(x0) + 10, int(x1) - 9, 10):
                for (yp, s) in ((ya - .8, -1), (yb2 + 15.8, 1)):
                    # charger pedestal with a screen and a holstered cable
                    self.box(park, x + 3.9, x + 5.1, yp - .45, yp + .45, zt, zt + 5, "super")
                    self.box(park, x + 4.0, x + 5.0, yp + s * .47, yp + s * .5, zt + 3.3, zt + 4.4, "window")
                    self.box(park, x + 3.9, x + 5.1, yp - .47, yp + .47, zt + 4.6, zt + 5.0, "battery")
                    self.rod(park, (x + 5.1, yp, zt + 3.5), (x + 5.4, yp, zt + 1.2), .12, "fanhub", seg=6)
                # green EV bay marking
                for yy in (ya, yb2):
                    self.box(park, x + 1, x + 9, yy + 5, yy + 10, zt, zt + .035, "battery")
            # solar carport: columns down the aisle, tilted PV canopy over both rows of chargers
            for x in range(int(x0) + 20, int(x1) - 9, 30):
                self.rod(park, (x, (ya + yb2 + 15) / 2, zt), (x, (ya + yb2 + 15) / 2, zt + 11), .5, "steel", seg=10)
            ym = (ya + yb2 + 15) / 2
            for (y_lo, y_hi, z_lo, z_hi) in ((ya + 1, ym, zt + 10.2, zt + 11.6), (ym, yb2 + 14, zt + 11.6, zt + 10.2)):
                self.parts.append(dict(kind="hex", v=[[x0 + 10, y_lo, z_lo - .3], [x1 - 10, y_lo, z_lo - .3],
                                                      [x1 - 10, y_hi, z_hi - .3], [x0 + 10, y_hi, z_hi - .3],
                                                      [x0 + 10, y_lo, z_lo], [x1 - 10, y_lo, z_lo],
                                                      [x1 - 10, y_hi, z_hi], [x0 + 10, y_hi, z_hi]],
                                       color="window", item=park["id"], layer=park["layer"], d=1))
            self.box(park, x0 + 10, x1 - 10, ym - .4, ym + .4, zt + 10.6, zt + 11.8, "steel")
            # DC fast-charger cabinet and its transformer at the east end of the carport
            self.box(park, x1 - 8, x1 - 2, ym - 4, ym + 4, zt, zt + 7, "ehouse")
            self.box(park, x1 - 8, x1 - 2, ym + 6, ym + 12, zt, zt + 5.5, "xfmr")
