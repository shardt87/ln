"""Cable trays and isolated-phase bus at LOD 3, generated from the route centrelines.

- Ladder trays for the MV (EL +36), LV (EL +30) and control / instrument (EL +42) tray routes:
  galvanised side rails and rungs, cables laid in the tray (MV: a few large triplexed
  circuits; LV and control: more, smaller ones), merged where several drawn circuits share a
  path. Supports about every 10 ft: carried by the pipe racks where a rack is under the tray;
  wall brackets with knee braces from the turbine-hall columns within 14 ft of a wall;
  otherwise trapeze stanchions from the floor below (the EL 20 deck inside the hall, grade
  outside). Vertical drops at the free ends of each tray run, down to the top of the
  equipment it feeds (or to the floor).
- Isolated-phase bus (generator -> GCB -> GSU, with the UAT tap): three round phase
  enclosures 3.2 ft apart with joint bands, on steel support frames.
The parts are dressing ("d": 1, "pipe": 1: always shown in the viewer); the routes keep the
data and stay pickable. Renderers draw these instead of the old route boxes.
"""
import math

TRAYS = {"mv_tray": (4, .32, "cable"), "lv_tray": (6, .22, "cable"), "control_tray": (8, .12, "cable")}
GALV = "pipe"


class Trays:
    def __init__(self, item, items, parts, routes):
        self.items, self.parts, self.routes = items, parts, routes
        self.it = item("ROUTES_BASE", "Cable trays and isolated-phase bus (rendered from the routes)",
                       (0, 2420, 0, 1920), (0, 45), basis="typical", register=False, sheet="typical (tray detail)",
                       info="Ladder trays with cables, supports and drops, and the three-phase IPB enclosures, "
                            "generated from the route centrelines.")
        self.n0 = len(parts)
        self.hall = next(i for i in items if i["name"] == "Common turbine hall")["fp"]
        self.deck = next(i for i in items if i["name"].startswith("Turbine deck EL 20"))["fp"]
        self.racks = [i["fp"] + [i["z"][1]] for i in items if "rack" in i["name"].lower() and i["z"][1] > 20]
        skip = ("Common turbine hall", "Turbine deck", "Pipe ", "Cable trays", "Laydown bay")
        self.solid = [i for i in items if i["layer"] != "SITE" and i["z"][1] > 1.5 and
                      not i["name"].startswith(skip) and "rack" not in i["name"].lower()]

    # ---------------------------------------------------------------------------------
    def add(self, kind, layer, **kw):
        kw.update(item=self.it["id"], layer=layer, d=1, pipe=1)
        self.parts.append(dict(kind=kind, **kw))

    def box(self, x0, x1, y0, y1, z0, z1, c, layer):
        self.add("box", layer, min=[round(min(x0, x1), 2), round(min(y0, y1), 2), round(min(z0, z1), 2)],
                 max=[round(max(x0, x1), 2), round(max(y0, y1), 2), round(max(z1, z0 + .05), 2)], color=c)

    def rod(self, a, b, r, c, layer, seg=8):
        self.add("rod", layer, a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=r, r2=r, color=c, seg=seg)

    def in_hall(self, x, y):
        f = self.hall
        return f[0] < x < f[1] and f[2] < y < f[3]

    def floor(self, x, y):
        f = self.deck
        return 20.0 if (f[0] <= x <= f[1] and f[2] <= y <= f[3]) else 0.0

    def blocked(self, x, y, z):
        return any(i["fp"][0] - .5 <= x <= i["fp"][1] + .5 and i["fp"][2] - .5 <= y <= i["fp"][3] + .5
                   and i["z"][0] < z + 1 for i in self.solid)

    def on_rack(self, x, y, z):
        return any(f[0] <= x <= f[1] and f[2] <= y <= f[3] and f[4] >= z - 2 for f in self.racks)

    def top_under(self, x, y, z):
        """Top of the equipment under a drop point (below the tray), else the floor."""
        tops = [i["z"][1] for i in self.solid if i["fp"][0] <= x <= i["fp"][1] and i["fp"][2] <= y <= i["fp"][3]
                and i["z"][1] < z - 1]
        return max(tops) if tops else self.floor(x, y)

    # ---------------------------------------------------------------------------------
    def run(self):
        runs, ends = {}, {}
        for r in self.routes:
            if r["type"] in TRAYS and r["z"] > 0:
                key = (r["layer"], r["type"], r["z"], r["w"], r["h"])
                for a, b in zip(r["points"], r["points"][1:]):
                    if a[0] == b[0] and a[1] != b[1]:
                        runs.setdefault(key + ("y", a[0]), []).append((min(a[1], b[1]), max(a[1], b[1])))
                    elif a[1] == b[1] and a[0] != b[0]:
                        runs.setdefault(key + ("x", a[1]), []).append((min(a[0], b[0]), max(a[0], b[0])))
                if r["z"] > 6:
                    for p in (r["points"][0], r["points"][-1]):
                        ends[(round(p[0], 1), round(p[1], 1), r["type"])] = key
        for k, ivs in runs.items():
            ivs.sort()
            merged = [list(ivs[0])]
            for a, b in ivs[1:]:
                if a <= merged[-1][1] + 1e-6:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])
            for a, b in merged:
                self.tray(k, a, b)
        for (x, y, t), key in ends.items():
            self.drop(key, x, y)
        for r in self.routes:
            if r["type"] == "ipb" and r["z"] > 0:
                self.ipb(r)
        return len(self.parts) - self.n0

    def tray(self, key, a, b):
        layer, rtype, z, w, h, axis, c = key
        n_cab, rc, ccol = TRAYS[rtype]
        hw, zb = w / 2, z - h / 2

        def B(s0, s1, v0, v1, z0, z1, col):
            if axis == "x":
                self.box(s0, s1, c + v0, c + v1, z0, z1, col, layer)
            else:
                self.box(c + v0, c + v1, s0, s1, z0, z1, col, layer)

        a0, b0 = a - hw, b + hw
        for s in (-1, 1):                                                       # side rails
            B(a0, b0, s * hw - (.12 if s > 0 else 0), s * hw + (0 if s > 0 else .12), zb, z + h / 2, GALV)
        s = a0 + 1
        while s < b0 - .5:                                                       # rungs
            B(s - .08, s + .08, -hw, hw, zb, zb + .12, GALV)
            s += 2
        for m in range(n_cab):                                                   # cables
            v = -hw + .2 + rc + (w - .4 - 2 * rc) * m / max(1, n_cab - 1)
            zc = zb + .12 + rc
            pa = (a0 + .3, c + v, zc) if axis == "x" else (c + v, a0 + .3, zc)
            pb = (b0 - .3, c + v, zc) if axis == "x" else (c + v, b0 - .3, zc)
            self.rod(pa, pb, rc, ccol, layer, seg=6)
        # supports about every 10 ft
        L = b0 - a0
        nsup = max(1, int(L // 10))
        for m in range(nsup + 1):
            s = a0 + .5 + (L - 1) * m / max(1, nsup)
            x, y = (s, c) if axis == "x" else (c, s)
            if self.on_rack(x, y, z):
                continue
            if self.in_hall(x, y):
                f = self.hall
                dw = min(abs(y - (f[2] + 34)), abs(y - (f[3] - 4))) if axis == "x" else 99
                if dw <= 14:                                                     # wall bracket from the column line
                    yw = f[3] - 4 if abs(y - (f[3] - 4)) < abs(y - (f[2] + 34)) else f[2] + 34
                    self.box(x - .2, x + .2, min(y - hw - .5, yw), max(y + hw + .5, yw), zb - .45, zb, "steel",
                             layer)
                    yk = yw + (y - yw) * .7
                    self.rod((x, yw, zb - 6), (x, yk, zb - .45), .12, "steel", layer, seg=4)
                    continue
            if self.blocked(x, y, z):
                continue
            base = self.floor(x, y)
            if z - base < 3:
                continue
            for sgn in (-1, 1):                                                  # trapeze stanchion pair
                px, py = (x, y + sgn * (hw + .4)) if axis == "x" else (x + sgn * (hw + .4), y)
                self.box(px - .22, px + .22, py - .22, py + .22, base, zb, "steel", layer)
            if axis == "x":
                self.box(x - .25, x + .25, y - hw - .6, y + hw + .6, zb - .4, zb, "steel", layer)
            else:
                self.box(x - hw - .6, x + hw + .6, y - .25, y + .25, zb - .4, zb, "steel", layer)

    def drop(self, key, x, y):
        layer, rtype, z, w, h = key
        n_cab, rc, ccol = TRAYS[rtype]
        bottom = self.top_under(x, y, z) + .5
        if z - bottom < 2:
            return
        hw = w / 2
        for s in (-1, 1):                                                       # vertical rails
            self.box(x - hw, x + hw, y + s * hw - .06, y + s * hw + .06, bottom, z, GALV, layer)
        zz = bottom + 1
        while zz < z - .5:
            self.box(x - hw, x + hw, y + hw - .1, y + hw, zz - .08, zz + .08, GALV, layer)
            zz += 2
        for m in range(min(n_cab, 4)):
            v = -hw + .25 + (w - .5) * m / max(1, min(n_cab, 4) - 1)
            self.rod((x + v, y + hw - .25 - rc, bottom), (x + v, y + hw - .25 - rc, z), rc, ccol, layer, seg=6)

    def ipb(self, r):
        z, layer = r["z"], r["layer"]
        for a, b in zip(r["points"], r["points"][1:]):
            ax = "x" if a[1] == b[1] else "y"
            if a[0] != b[0] and a[1] != b[1]:
                continue
            for off in (-3.2, 0, 3.2):
                if ax == "x":
                    pa, pb = (a[0], a[1] + off, z), (b[0], b[1] + off, z)
                else:
                    pa, pb = (a[0] + off, a[1], z), (b[0] + off, b[1], z)
                self.rod(pa, pb, 1.1, "ipb", layer, seg=16)
                L = abs(b[0] - a[0]) + abs(b[1] - a[1])
                n = int(L // 10)
                for m in range(1, n + 1):                                         # joint bands
                    t = m / (n + 1)
                    q = [pa[j] + (pb[j] - pa[j]) * t for j in range(3)]
                    d = [(pb[j] - pa[j]) / L * .2 for j in range(3)]
                    self.rod([q[j] - d[j] for j in range(3)], [q[j] + d[j] for j in range(3)], 1.25, "steel", layer,
                             seg=16)
            # support frames about every 12 ft
            L = abs(b[0] - a[0]) + abs(b[1] - a[1])
            n = max(1, int(L // 12))
            for m in range(n + 1):
                t = m / n
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                base = self.floor(x, y)
                if self.blocked(x, y, z) and not self.in_hall(x, y):
                    continue
                if ax == "x":
                    self.box(x - .3, x + .3, y - 4.8, y + 4.8, z - 1.6, z - 1.1, "steel", layer)
                    for s in (-1, 1):
                        self.box(x - .25, x + .25, y + s * 4.8 - .25, y + s * 4.8 + .25, base, z - 1.1, "steel", layer)
                else:
                    self.box(x - 4.8, x + 4.8, y - .3, y + .3, z - 1.6, z - 1.1, "steel", layer)
                    for s in (-1, 1):
                        self.box(x + s * 4.8 - .25, x + s * 4.8 + .25, y - .25, y + .25, base, z - 1.1, "steel", layer)


def build(item, items, parts, routes):
    return Trays(item, items, parts, routes).run()
