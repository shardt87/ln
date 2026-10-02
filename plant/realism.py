"""Realism pass (LOD 3), run last so every check sees the finished model.

1. Firewater: buried ring main round the power block, branches to the BOP / gas / modular areas
   and a feed from the fire pump house; hydrants about every 200 ft, post-indicator valves at the
   corners, fixed monitors at each GSU and the gas yard, deluge valve stations at the GSUs.
2. Small-bore piping: instrument air, service water and nitrogen headers on the pipe racks;
   HRSG drain headers to the blowdown tanks; instrument-air drops at the HRSG and the gas yard.
3. Signage: equipment ID and hazard signs on buildings, e-houses and transformers.
4. Scale: people in hard hats and hi-vis at work positions (grade, the turbine deck, HRSG
   platforms, the CEMS platform, the gas yard), vehicles (pickups, a flatbed at the laydown
   bay, a forklift, a mobile crane), and scaffolding on HRSG 2.
5. Tube harps: HRSG 3's coil sections (superheater / reheater, evaporators, economizers, SCR
   and CO catalyst) with their upper and lower headers, for the cutaway camera.
Every placement is tested against the geometry already in the model and skipped if it would
pass through anything. All of it is typical, not engineered.
"""
import math


def _pbox(p):
    if p["kind"] in ("box", "prism"):
        return p["min"] + p["max"]
    if p["kind"] == "rod":
        a, b, r = p["a"], p["b"], max(p["r"], p["r2"])
        ax = [i for i in range(3) if a[i] != b[i]]
        pad = [0 if i in ax else r for i in range(3)] if len(ax) == 1 else [r] * 3
        return [min(a[i], b[i]) - pad[i] for i in range(3)] + [max(a[i], b[i]) + pad[i] for i in range(3)]
    xs, ys, zs = zip(*p["v"])
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]


class Realism:
    def __init__(self, item, items, parts, routes):
        self.item, self.items, self.parts, self.routes = item, items, parts, routes
        byid = {i["id"]: i for i in items}
        self.obs, self.grid = [], {}
        for p in parts:
            it = byid[p["item"]]
            if it["z"][1] < .8 and it["layer"] in ("SITE",):
                continue
            b = _pbox(p)
            if b[5] < .75:                         # pads, roads, slabs: walkable, not obstacles
                continue
            k = len(self.obs)
            self.obs.append(b)
            for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
                for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
                    self.grid.setdefault((gx, gy), []).append(k)
        self.cur = None
        self.n0 = len(parts)
        self.counts = {}

    # ---------------------------------------------------------------------------------
    def new(self, layer, name, fp, z, **meta):
        meta.setdefault("basis", "typical")
        meta.setdefault("register", False)
        meta.setdefault("sheet", "typical (realism pass)")
        self.cur = self.item(layer, name, fp, z, **meta)

    def box(self, x0, x1, y0, y1, z0, z1, c, layer=None):
        self.parts.append(dict(kind="box", min=[round(min(x0, x1), 2), round(min(y0, y1), 2), round(min(z0, z1), 2)],
                               max=[round(max(x0, x1), 2), round(max(y0, y1), 2), round(max(z0 + .05, z1), 2)],
                               color=c, item=self.cur["id"], layer=layer or self.cur["layer"], d=1))

    def rod(self, a, b, r, c, seg=10, layer=None, r2=None):
        self.parts.append(dict(kind="rod", a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=r,
                               r2=r if r2 is None else r2, color=c, seg=seg, item=self.cur["id"],
                               layer=layer or self.cur["layer"], d=1))

    def free(self, x0, x1, y0, y1, z0, z1, m=0.0):
        x0, x1, y0, y1 = min(x0, x1) - m, max(x0, x1) + m, min(y0, y1) - m, max(y0, y1) + m
        for gx in range(int(x0 // 10), int(x1 // 10) + 1):
            for gy in range(int(y0 // 10), int(y1 // 10) + 1):
                for k in self.grid.get((gx, gy), ()):
                    b = self.obs[k]
                    if b[0] < x1 and b[3] > x0 and b[1] < y1 and b[4] > y0 and b[2] < z1 and b[5] > z0:
                        return False
        return True

    def floor_at(self, x, y, z):
        """Top of the highest part under (x, y) within 1.2 ft below z (a floor to stand on), else None."""
        best = None
        for k in self.grid.get((int(x // 10), int(y // 10)), ()):
            b = self.obs[k]
            if b[0] <= x <= b[3] and b[1] <= y <= b[4] and z - 1.2 <= b[5] <= z + .3:
                best = b[5] if best is None else max(best, b[5])
        return best

    def count(self, k):
        self.counts[k] = self.counts.get(k, 0) + 1

    # ---------------------------------------------------------------------------------
    def firewater(self):
        loop = [(410, 310), (1450, 310), (1450, 890), (410, 890), (410, 310)]
        branches = [[(720, 1572), (720, 890)], [(1450, 890), (1450, 1410), (2350, 1410), (2350, 1430)],
                    [(1450, 310), (2170, 310), (2170, 330)], [(410, 890), (410, 1540), (445, 1540)]]
        lab = "Firewater ring main (buried, HDPE / ductile iron)"
        for pl in [loop] + branches:
            self.routes.append(dict(type="firewater", layer="PROCESS_PIPING", label=lab, z=-4, w=1.2, h=1.2,
                                    color="firewater", points=[[float(x), float(y)] for x, y in pl],
                                    sheet="typical (realism pass)"))
        self.new("PROCESS_PIPING", "Firewater hydrants, monitors, post-indicator valves and deluge stations",
                 (400, 2390, 300, 1700), (0, 12),
                 info="Hydrants about every 200 ft on the buried ring main; fixed monitors at the GSUs and the gas "
                      "yard; PIVs at the loop corners; deluge valve stations for the GSU water-spray systems.")
        segs = []
        for pl in [loop] + branches:
            segs += list(zip(pl, pl[1:]))
        for (a, b) in segs:
            L = abs(b[0] - a[0]) + abs(b[1] - a[1])
            n = max(1, int(L // 200))
            for m in range(n + 1):
                t = m / n if n else 0
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                for dx, dy in ((0, 0), (4, 0), (-4, 0), (0, 4), (0, -4), (8, 0), (0, 8)):
                    if self.free(x + dx - 1, x + dx + 1, y + dy - 1, y + dy + 1, 0, 4, .5):
                        self.hydrant(x + dx, y + dy)
                        break
        for (x, y) in ((410, 310), (1450, 310), (1450, 890), (410, 890)):
            if self.free(x + 3, x + 5, y + 3, y + 5, 0, 5, .3):
                self.box(x + 3.7, x + 4.3, y + 3.7, y + 4.3, 0, 3.6, "red")              # PIV post
                self.box(x + 3.4, x + 4.6, y + 3.6, y + 4.4, 3.6, 4.4, "red")
                self.count("post-indicator valves")
        for gx in (630, 790, 950, 1051):                                                  # GSU monitors + deluge
            mx, my = gx - 28, 312
            if self.free(mx - 1, mx + 1, my - 1, my + 1, 0, 8, .3):
                self.monitor(mx, my, toward=(gx, 345))
            dx_, dy_ = gx + 28, 312
            if self.free(dx_ - 2, dx_ + 2, dy_ - 2, dy_ + 2, 0, 8, .3):
                self.box(dx_ - 2, dx_ + 2, dy_ - 2, dy_ + 2, 0, .5, "concrete")
                self.box(dx_ - 1.6, dx_ + 1.6, dy_ - 1.6, dy_ + 1.6, .5, 7, "red")       # deluge valve house
                self.box(dx_ - 1.9, dx_ + 1.9, dy_ - 1.9, dy_ + 1.9, 7, 7.3, "roof")
                self.count("deluge valve stations")
        for (mx, my) in ((1600, 1520), (1790, 1600)):
            if self.free(mx - 1, mx + 1, my - 1, my + 1, 0, 8, .3):
                self.monitor(mx, my, toward=(1690, 1530))

    def hydrant(self, x, y):
        self.rod((x, y, 0), (x, y, 2.6), .38, "red", seg=12)
        self.rod((x, y, 2.6), (x, y, 3.1), .3, "red", r2=.12, seg=12)
        for (dx, dy) in ((.55, 0), (-.55, 0), (0, .55)):
            self.rod((x, y, 1.8), (x + dx, y + dy, 1.8), .14, "steel", seg=8)
        self.box(x - .7, x + .7, y - .7, y + .7, 0, .15, "concrete")
        self.count("hydrants")

    def monitor(self, x, y, toward):
        self.rod((x, y, 0), (x, y, 6.5), .3, "red", seg=10)
        a = math.atan2(toward[1] - y, toward[0] - x)
        self.rod((x, y, 6.5), (x + 2.2 * math.cos(a), y + 2.2 * math.sin(a), 7.4), .22, "red", r2=.12, seg=10)
        self.box(x - .5, x + .5, y - .5, y + .5, 2.5, 3.3, "red")
        self.box(x - .9, x + .9, y - .9, y + .9, 0, .2, "concrete")
        self.count("fire monitors")

    # ---------------------------------------------------------------------------------
    def small_bore(self):
        self.new("PROCESS_PIPING", "Small-bore piping: instrument air, service water, nitrogen, HRSG drains",
                 (460, 1300, 560, 850), (0, 32),
                 info="Instrument air (blue band), service water (green band) and nitrogen headers on the rack "
                      "tiers; HRSG casing drain headers to the blowdown tanks; instrument-air drops (typical).")
        racks = [i for i in self.items if i["name"].startswith(("Main E-W pipe and cable rack", "N-S pipe rack"))]
        for it in racks:
            x0, x1, y0, y1 = it["fp"]
            along_x = (x1 - x0) > (y1 - y0)
            for (z, d, f, c) in ((24, .5, .48, "pipe"), (24, .4, .52, "pipe"), (24, .6, .68, "pipe"),
                                 (30, .35, .30, "pipe")):
                r = d / 2
                # in 10 ft pieces, joined where free: a tray drop or support crossing the tier breaks
                # the line there (in the field it would jog round it)
                lo, hi = (x0 + 2, x1 - 2) if along_x else (y0 + 2, y1 - 2)
                c0 = y0 + (y1 - y0) * f if along_x else x0 + (x1 - x0) * f
                run = None
                u = lo
                while u < hi:
                    v = min(hi, u + 10)
                    ok = (self.free(u, v, c0 - r, c0 + r, z + .05, z + d) if along_x else
                          self.free(c0 - r, c0 + r, u, v, z + .05, z + d))
                    if ok:
                        run = [run[0], v] if run else [u, v]
                    if (not ok or v >= hi) and run:
                        a = (run[0], c0, z + r) if along_x else (c0, run[0], z + r)
                        b = (run[1], c0, z + r) if along_x else (c0, run[1], z + r)
                        self.rod(a, b, r, c, seg=8)
                        self.count("rack small-bore line runs")
                        run = None
                    u = v
        for k in range(3):                                                             # HRSG drain headers
            dx = 160 * k
            x = 597 + dx - 4.2
            ok = self.free(x - .3, x + .3, 606, 702, .5, 1.6)
            if ok:
                self.rod((x, 606, 1.1), (x, 702, 1.1), .3, "pipe", seg=8)
                for y in (622, 655, 690):
                    self.rod((597 + dx, y, 2.4), (x, y, 1.1), .14, "pipe", seg=6)
                self.count("HRSG drain headers")

    # ---------------------------------------------------------------------------------
    def signage(self):
        self.new("SITE", "Equipment ID and hazard signage", (0, 2420, 0, 1920), (0, 12))
        for it in self.items:
            nm = it["name"]
            if not it.get("register") or it["layer"] in ("R1_INTERIOR", "SITE"):
                continue
            kind = None
            if any(k in nm for k in ("transformer", "GSU", "UAT", "T-MOD", "MPT")):
                kind = "hazard"
            elif any(k in nm.lower() for k in ("e-house", "building", "house", "shelter")):
                kind = "id"
            if not kind:
                continue
            x0, x1, y0, y1 = it["fp"]
            cx = (x0 + x1) / 2
            z = min(7.5, max(4.5, it["z"][1] - 3))
            y = y0 - .12
            if not self.free(cx - 1.6, cx + 1.6, y - .3, y, z - .1, z + 1.4):
                continue
            self.box(cx - 1.5, cx + 1.5, y - .08, y, z, z + 1.2, "sign")
            self.box(cx - 1.3, cx - .6, y - .1, y - .08, z + .2, z + 1.0, "amber" if kind == "hazard" else "door")
            self.count("signs")

    # ---------------------------------------------------------------------------------
    def person(self, x, y, z, a=0.0, vest="hivis", hat="hardhat"):
        ca, sa = math.cos(a), math.sin(a)
        for s in (-1, 1):                                                              # legs
            px, py = x + s * .28 * -sa, y + s * .28 * ca
            self.rod((px, py, z), (px, py, z + 2.8), .2, "workwear", seg=6)
        self.box(x - .55, x + .55, y - .55, y + .55, z + 2.8, z + 4.7, vest)
        for s in (-1, 1):                                                              # arms
            px, py = x + s * .72 * -sa, y + s * .72 * ca
            self.rod((px, py, z + 4.6), (px + .25 * ca, py + .25 * sa, z + 2.9), .14, vest, seg=6)
        self.rod((x, y, z + 4.75), (x, y, z + 5.45), .36, "skin", seg=10)
        self.rod((x, y, z + 5.4), (x, y, z + 5.85), .43, hat, r2=.3, seg=10)
        self.count("people")

    def place_person(self, x, y, z, a=0.0, **kw):
        fz = 0.0 if z <= .5 else self.floor_at(x, y, z)
        if fz is None:
            return False
        if not self.free(x - .8, x + .8, y - .8, y + .8, fz + .1, fz + 6.0):
            return False
        self.person(x, y, fz + .02, a, **kw)
        return True

    def people(self):
        self.new("SITE", "People (scale figures in PPE)", (0, 2420, 0, 1920), (0, 110))
        spots = [  # (x, y, z, heading) - work positions
            (560, 300, 0, 0), (566, 302, 0, 3.0), (700, 300, 0, 1.6),           # access road by the gallery
            (520, 470, 0, 0), (528, 476, 0, 3.6),                                # laydown bay
            (690, 495, 20, 1.6), (850, 500, 20, 4.7), (1010, 470, 20, 1.6),     # turbine deck by the skids
            (665.5, 680, 25, 1.6), (825.5, 640, 50, 1.6), (985.5, 700, 74, 4.7),   # HRSG east platforms
            (630, 803.5, 101.4, 1.6), (618, 790, 101.4, 0),                     # CEMS platform, stack 1
            (1650, 1515, 0, 0), (1700, 1545, 0, 3.1), (1720, 1612, 0, 1.6),     # gas yard
            (1640, 1800, 0, 1.6), (1612, 1840, 0, 0),                            # M&R station
            (700, 150, 0, 1.6), (910, 128, 0, 4.7), (1110, 205, 0, 1.6),        # switchyard
            (420, 250, 0, 0), (300, 330, 0, 4.7), (250, 333, 0, 4.7),           # relay house, admin
            (180, 120, 0, 0), (230, 160, 0, 3.1), (120, 200, 0, 1.6),           # parking
            (1600, 1060, 0, 1.6), (1640, 1135, 0, 4.7), (1940, 1180, 0, 0),     # modular yard
            (2030, 498, 0, 1.6), (2070, 540, 0, 3.1),                            # portable pad
            (1470, 600, 0, 1.6), (1300, 700, 0, 3.1), (1180, 520, 0, 0),        # ACC area
            (600, 1590, 0, 0), (710, 1570, 0, 4.7),                              # tank farm, fire pumps
            (1452, 360, 0, 1.6), (1210, 330, 0, 4.7),                            # R4, ACC stair
            (288, 302, 0, 3.1), (262, 268, 0, 1.6),                              # guard at the gate, card reader
            (190, 596, 0, 4.7), (165, 628, 0, 0),                                # workshop yard
            (656, 1176, 0, 1.6), (716, 1110, 0, 3.1), (1092, 1222, 0, 4.7),     # CCS train A, rack, strippers
            (900, 1726, 0, 1.6), (1300, 1372, 0, 3.1),                           # CCS cooling tower, CO2 coolers
        ]
        for (x, y, z, a) in spots:
            for (dx, dy) in ((0, 0), (2, 0), (-2, 0), (0, 2), (0, -2), (3, 3), (-3, -3)):
                if self.place_person(x + dx, y + dy, z, a, vest="hivis" if (int(x + y) % 3) else "hivis_o"):
                    break

    # ---------------------------------------------------------------------------------
    def vehicle(self, x, y, a, kind):
        """Vehicle along heading a (radians); x, y = centre."""
        ca, sa = math.cos(a), math.sin(a)

        def P(u, v):
            return x + u * ca - v * sa, y + u * sa + v * ca

        def B(u0, u1, v0, v1, z0, z1, c):
            pts = [P(u0, v0), P(u1, v0), P(u0, v1), P(u1, v1)]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            self.box(min(xs), max(xs), min(ys), max(ys), z0, z1, c)

        def W(u, v, r):
            p = P(u, v)
            q = P(u, v + (.4 if v > 0 else -.4))
            self.rod((p[0], p[1], r), (q[0], q[1], r), r, "fanhub", seg=12)

        if kind == "pickup":
            L, Wd = 19, 6.6
            B(-L / 2, L / 2, -Wd / 2, Wd / 2, 1.3, 3.6, "truck")
            B(-1.5, 4.5, -Wd / 2 + .2, Wd / 2 - .2, 3.6, 6.2, "truck")
            B(-1.4, 4.4, -Wd / 2 + .15, Wd / 2 - .15, 4.4, 5.9, "glass")
            for u in (-6, 6):
                for v in (-Wd / 2, Wd / 2):
                    W(u, v, 1.3)
        elif kind == "flatbed":
            B(-26, 26, -4.1, 4.1, 3.2, 4.4, "steel")                       # trailer deck
            B(28, 36, -4.1, 4.1, 2, 10.5, "tug")                            # tractor cab
            B(26, 28, -3.5, 3.5, 3.2, 4.6, "steel")
            B(-18, 6, -3.6, 3.6, 4.4, 10, "machine")                        # load: a skid under tarp
            for u in (-22, -18, 30, 34):
                for v in (-4.1, 4.1):
                    W(u, v, 1.6)
        elif kind == "forklift":
            B(-3.5, 3.5, -2.3, 2.3, .8, 4.2, "crane")
            B(-3.5, -1, -2.3, 2.3, 4.2, 7.5, "steel")
            B(3.5, 4, -1.6, 1.6, .4, 9, "steel")
            B(4, 7, -1.4, -1.0, .3, .5, "steel")
            B(4, 7, 1.0, 1.4, .3, .5, "steel")
            for u in (-2.5, 2.5):
                for v in (-2.3, 2.3):
                    W(u, v, .9)
        elif kind == "crane":
            B(-24, 24, -4.6, 4.6, 2.4, 6.4, "crane")                        # carrier
            B(14, 22, -4.6, -.6, 6.4, 11.5, "crane")                        # carrier cab
            B(-10, 4, -4.4, 4.4, 6.4, 13, "crane")                          # superstructure
            for u in (-20, -6, 8, 18):
                for v in (-4.6, 4.6):
                    W(u, v, 2.0)
            for u in (-20, 20):                                               # outriggers
                for v in (-1, 1):
                    q = P(u, v * 11)
                    self.box(q[0] - 1, q[0] + 1, q[1] - 1, q[1] + 1, 0, .4, "steel")
                    p0 = P(u, v * 4.6)
                    self.rod((p0[0], p0[1], 3.2), (q[0], q[1], .5), .4, "crane", seg=6)
            b0 = P(2, 0)
            b1 = P(40, 0)
            self.rod((b0[0], b0[1], 12), (b1[0], b1[1], 95), 1.4, "crane", r2=.7, seg=10)   # boom
            self.rod((b1[0], b1[1], 95), (b1[0], b1[1], 55), .08, "steel", seg=4)           # hoist line
            self.box(b1[0] - .8, b1[0] + .8, b1[1] - .8, b1[1] + .8, 53, 55, "crane")       # hook block
        self.count(kind + "s")

    def place_vehicle(self, x, y, a, kind, r):
        if not self.free(x - r, x + r, y - r, y + r, .3, 13):
            return False
        self.vehicle(x, y, a, kind)
        return True

    def vehicles(self):
        self.new("SITE", "Vehicles: pickups, a flatbed at the laydown bay, a forklift, a mobile crane",
                 (0, 2420, 0, 1920), (0, 95))
        for (x, y, a) in ((1240, 285, 0), (1620, 290, math.pi), (1475, 1100, math.pi / 2),
                          (1700, 1662, 0), (385, 1300, -math.pi / 2), (2050, 1385, math.pi)):
            self.place_vehicle(x, y, a, "pickup", 10)
        self.place_vehicle(440, 485, math.pi / 2, "flatbed", 6)
        self.place_vehicle(248, 278, 0, "pickup", 8)                  # inbound at the barrier
        self.place_vehicle(118, 535, math.pi / 2, "flatbed", 6)       # delivery at the warehouse
        for (x, y) in ((345, 520), (350, 600)):
            if self.place_vehicle(x, y, 0, "forklift", 4.5):
                break
        # mobile crane on the access road east of the GSUs, boom raised over the road
        for x in (1150, 1300, 1380):
            if self.free(x - 26, x + 26, 274, 296, .3, 14) and self.free(x - 2, x + 42, 280, 290, 14, 96):
                self.vehicle(x, 285, 0, "crane")
                break

    def scaffold(self):
        self.new("BASE_POWER_BLOCK", "Scaffolding on HRSG 2 (maintenance access, typical)",
                 (749, 757, 738, 756), (0, 45))
        for (x0, x1, y0, y1) in ((749.5, 756.5, 738.5, 755.5), (909.5, 916, 736, 752), (909.5, 916, 612, 630),
                                 (749.5, 756, 612, 630), (664, 671, 612, 628)):
            if self.free(x0, x1, y0, y1, .1, 45):
                break
        else:
            return
        self.cur["fp"] = [x0, x1, y0, y1]
        for x in (x0, x1):
            for y in (y0, (y0 + y1) / 2, y1):
                self.rod((x, y, 0), (x, y, 44), .09, "steel", seg=6)
        for z in range(6, 45, 6):
            self.box(x0, x1, y0, y1, z - .15, z, "grating")
            for y in (y0, y1):
                self.rod((x0, y, z + 3.3), (x1, y, z + 3.3), .07, "rail", seg=4)
            self.rod((x0, y0, z - 6), (x0, y1, z), .06, "steel", seg=4)
        self.count("scaffolds")

    # ---------------------------------------------------------------------------------
    def harps(self):
        """HRSG 3 coil sections inside the casing (seen in the cutaway camera)."""
        self.new("BASE_POWER_BLOCK", "HRSG 3 tube harps and headers (cutaway view)", (917, 983, 601, 759), (2, 77),
                 info="Finned-tube harps in gas-flow order: HP superheater / reheater, HP evaporator, SCR and CO "
                      "catalyst, HP economizer / IP superheater, IP evaporator, LP evaporator / IP economizer, LP "
                      "economizer; upper and lower headers (typical).")
        x0, x1 = 918.5, 981.5
        sections = [(602, 640, 3, "bundle"), (640, 668, 4, "bundle"), (668, 688, 0, "filter"), (688, 712, 4, "bundle"),
                    (712, 725, 2, "bundle"), (725, 745, 3, "bundle"), (745, 758, 2, "bundle")]
        for (ya, yb, n, c) in sections:
            if n == 0:                                                  # SCR + CO catalyst blocks
                for z in (6, 26, 46):
                    self.box(x0, x1, ya + 3, ya + 9, z, z + 14, "filter")
                    self.box(x0, x1, ya + 12, yb - 2, z, z + 14, "filter")
                continue
            for m in range(n):
                y = ya + (yb - ya) * (m + .5) / n
                self.box(x0, x1, y - 1.1, y + 1.1, 6, 72, c)                       # finned tube harp
                self.rod((x0, y, 73.5), (x1, y, 73.5), .9, "hrsg", seg=12)         # upper header
                self.rod((x0, y, 4.5), (x1, y, 4.5), .8, "hrsg", seg=12)           # lower header
                for xx in (x0 + 8, (x0 + x1) / 2, x1 - 8):                         # hanger rods
                    self.rod((xx, y, 74.4), (xx, y, 77.5), .12, "steel", seg=4)
        self.count("harps")

    def run(self):
        self.firewater()
        self.small_bore()
        self.signage()
        self.people()
        self.vehicles()
        self.scaffold()
        self.harps()
        return self.counts


def build(item, items, parts, routes):
    return Realism(item, items, parts, routes).run()
