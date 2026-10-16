"""Round pipe geometry for the process-pipe routes (LOD 3).

The routes stay in the model as centrelines (for the register, picking and the legend); this
pass turns every above-grade pipe route into rendered geometry:
- straight runs as cylinders, merged where several drawn circuits share one line;
- long-radius elbows (bend radius 1.5 D) at every change of direction, mitred in 4 segments;
- a drop to grade at the free ends of elevated lines (as the old box risers did);
- weld-neck flange pairs about every 40 ft and at the ends;
- insulated lines (steam, condensate, feedwater, chilled water, LNG) in an aluminium jacket with
  seam bands, and a coloured identification band every ~60 ft; bare lines in their service colour.
The parts are dressing ("d": 1) with "pipe": 1 so the viewer shows them with the base model
rather than behind the Detail toggle.
"""
import math

PIPE = {   # type: (insulated, jacket radius factor)
    "steam": (True, 1.0), "condensate": (True, 1.0), "feedwater": (True, 1.0), "ccw": (False, 1.0),
    "fuel_gas": (False, 1.0), "fuel_oil": (False, 1.0), "cw": (False, 1.0), "chw": (True, 1.0),
    "hydrogen": (False, 1.0), "lng": (True, 1.0), "water": (False, 1.0), "aux_steam": (True, 1.0),
}
JACKET = "pipe"


class Pipes:
    def __init__(self, item, items, parts, routes):
        self.items, self.parts, self.routes = items, parts, routes
        xs = [p[0] for r in routes for p in r["points"]]
        ys = [p[1] for r in routes for p in r["points"]]
        self.it = item("PROCESS_PIPING", "Pipe runs (rendered from the process routes)",
                       (min(xs), max(xs), min(ys), max(ys)), (0, 30), basis="typical", register=False,
                       sheet="typical (pipe detail)",
                       info="Round pipes, elbows, flanges and insulation jacketing generated from the route "
                            "centrelines; the centrelines carry the route data.")
        self.n0 = len(parts)

    def rod(self, a, b, r, c, layer, seg=14):
        self.parts.append(dict(kind="rod", a=[round(v, 2) for v in a], b=[round(v, 2) for v in b], r=round(r, 3),
                               r2=round(r, 3), color=c, seg=seg, item=self.it["id"], layer=layer, d=1, pipe=1))

    # ------------------------------------------------------------------ end connections
    SKIP = ("Pipe runs", "Pipe supports", "Cable trays", "People", "Vehicles", "Equipment ID", "Underground",
            "Firewater hydrants", "Small-bore piping", "Parking")
    NOT_EQUIP = {"concrete", "gravel", "gravel_yard", "ground", "road", "grating", "rail", "stair", "label", "lamp",
                 "hivis_o", "hivis", "hardhat", "workwear", "reflect", "pad", "fence", "tyre", "glass"}

    def _equipment_grid(self):
        """Solid equipment parts (not slabs, people, labels, buried works), on a 20 ft grid, for end connections."""
        names = {it["id"]: it for it in self.items}
        g = {}
        for p in self.parts:
            it = names.get(p.get("item"))
            if not it or it["layer"] == "SITE" or it["name"].startswith(self.SKIP) or p.get("color") in self.NOT_EQUIP:
                continue
            if p["kind"] == "rod":
                q = max(p["r"], p.get("r2") or 0)
                lo = [min(p["a"][i], p["b"][i]) - q for i in range(3)]
                hi = [max(p["a"][i], p["b"][i]) + q for i in range(3)]
            elif "min" in p:
                lo, hi = list(p["min"]), list(p["max"])
            else:
                continue
            if hi[2] <= .8 or (hi[0] - lo[0]) * (hi[1] - lo[1]) > 40000 or min(hi[0] - lo[0], hi[1] - lo[1]) < .3:
                continue
            for i in range(int(lo[0] // 20), int(hi[0] // 20) + 1):
                for j in range(int(lo[1] // 20), int(hi[1] // 20) + 1):
                    g.setdefault((i, j), []).append((lo, hi))
        return g

    def _target(self, p, reach, u=None):
        """Nearest equipment part to point p within reach: the point on it to connect to, or None. With u (the
        route's outward direction at this end), only parts ahead of or beside the end count, never ones back
        along the pipe itself."""
        best = None
        n = int(reach // 20) + 1
        for i in range(int(p[0] // 20) - n, int(p[0] // 20) + n + 1):
            for j in range(int(p[1] // 20) - n, int(p[1] // 20) + n + 1):
                for lo, hi in self.eq.get((i, j), ()):
                    c = [min(max(p[k], lo[k] + min(.3, (hi[k] - lo[k]) / 2)), hi[k] - min(.3, (hi[k] - lo[k]) / 2))
                         for k in range(3)]
                    d = math.sqrt(sum((p[k] - c[k]) ** 2 for k in range(3)))
                    if u is not None and (c[0] - p[0]) * u[0] + (c[1] - p[1]) * u[1] < -.5:
                        continue
                    if d <= reach and (best is None or d < best[0]):
                        best = (d, c)
        return None if best is None else best[1]

    def _on_pipe(self, r, x, y):
        """The end lies on another route of the same service (a tee or a continuation), or on a road sleeve."""
        for q in self.routes:
            if q is r or q["type"] != r["type"]:
                continue
            for a, b in zip(q["points"], q["points"][1:]):
                if min(a[0], b[0]) - 1 <= x <= max(a[0], b[0]) + 1 and min(a[1], b[1]) - 1 <= y <= max(a[1], b[1]) + 1:
                    return "sleeve" if q["z"] < 0 else "pipe"
        return None

    def _end(self, r, x, y, z, u=None):
        """How a route end finishes: (start points to prepend in route order, connector legs to draw)."""
        on = self._on_pipe(r, x, y)
        if on == "pipe":
            return [], None                                    # tee / continuation at the route's own level
        if on == "sleeve":
            return ([(x, y, .6)] if z > 6 else []), None       # into the road-crossing sleeve (drop drawn by supports)
        c = self._target((x, y, z), 8.0, u)                    # equipment beside the end at its own level
        if c is not None:
            return [], ((x, y, z), c)
        if z > 6:
            c = self._target((x, y, .6), 25.0, u)
            return [(x, y, .6)], (((x, y, .6), c) if c is not None else None)
        c = self._target((x, y, z), 25.0, u)
        if c is not None:
            return [], ((x, y, z), c)
        if x <= 8 or y <= 8 or x >= 2412 or y >= 1912:         # pipeline at the boundary: goes underground
            return [], ((x, y, z), (x, y, 0.0))
        return [], None

    def connect(self, leg, rad, color, layer, ins, rtype):
        """Square connector from a route end to its equipment: along x, along y, then vertical; flange at the nozzle."""
        (x, y, z), c = leg
        pts = [(x, y, z), (c[0], y, z), (c[0], c[1], z), (c[0], c[1], c[2])]
        pts = [p for k, p in enumerate(pts) if k == 0 or math.dist(p, pts[k - 1]) > .05]
        for k, (a, b) in enumerate(zip(pts, pts[1:])):
            ax = [j for j in range(3) if abs(a[j] - b[j]) > 1e-6][0]
            sg = 1 if b[ax] > a[ax] else -1
            a, b = list(a), list(b)
            a[ax] -= sg * rad                                  # legs overlap by a radius: closed square corners
            if k < len(pts) - 2:
                b[ax] += sg * rad
            self.pipe_run(tuple(a), tuple(b), rad, color, layer, ins, rtype)
        if len(pts) > 1:
            a, b = pts[-2], pts[-1]
            ax = [j for j in range(3) if abs(a[j] - b[j]) > 1e-6][0]
            if b[2] > .05:                                     # (a pipeline into the ground has no nozzle)
                self.flange(b, ax, rad, ins, layer)            # nozzle flange at the equipment
        return len(pts) - 1

    def run(self):
        segs, corners, ends = {}, {}, []
        self.eq = self._equipment_grid()
        self.n_conn = 0
        legs = []
        for r in self.routes:
            if r["type"] not in PIPE or r["z"] <= 0:
                continue
            ins, _ = PIPE[r["type"]]
            rad = r["w"] / 2 * (.92 if ins else .8)
            z = r["z"]
            pts = [tuple(p) for p in r["points"]]
            P3 = [(x, y, z) for x, y in pts]
            out = lambda a, b: ((a[0] - b[0]) / (math.dist(a, b) or 1), (a[1] - b[1]) / (math.dist(a, b) or 1))
            pre, l0 = self._end(r, pts[0][0], pts[0][1], z, out(pts[0], pts[1]))
            post, l1 = self._end(r, pts[-1][0], pts[-1][1], z, out(pts[-1], pts[-2]))
            P3 = pre + P3 + post
            for lg in (l0, l1):
                if lg is not None:
                    legs.append((lg, rad, r["color"], r["layer"], ins, r["type"]))
            P3 = [p for k, p in enumerate(P3) if k == 0 or p != P3[k - 1]]
            key = (r["layer"], r["type"], r["color"], round(rad, 3), ins)
            for a, b in zip(P3, P3[1:]):
                ax = [i for i in range(3) if abs(a[i] - b[i]) > 1e-6]
                if len(ax) != 1:
                    continue                                   # diagonal: not a pipe run we draw
                i = ax[0]
                line = tuple(round(a[j], 2) for j in range(3) if j != i)
                segs.setdefault(key + (i, line), []).append((min(a[i], b[i]), max(a[i], b[i])))
            for k in range(1, len(P3) - 1):
                p0, p, p1 = P3[k - 1], P3[k], P3[k + 1]
                d1 = tuple((p[j] - p0[j]) for j in range(3))
                d2 = tuple((p1[j] - p[j]) for j in range(3))
                n1, n2 = math.sqrt(sum(v * v for v in d1)), math.sqrt(sum(v * v for v in d2))
                if n1 < 1e-6 or n2 < 1e-6:
                    continue
                d1 = tuple(v / n1 for v in d1)
                d2 = tuple(v / n2 for v in d2)
                if abs(sum(a * b for a, b in zip(d1, d2))) > .01:
                    continue                                   # straight through or not square
                R = min(3 * rad, n1 / 2 - .05, n2 / 2 - .05)
                if R <= rad * .6:
                    continue
                corners[(key, tuple(round(v, 2) for v in p), d1, d2)] = R
            ends.append((key, P3[0]))
            ends.append((key, P3[-1]))
        # trims at corners so straight runs stop where the elbow starts
        trim = {}
        for (key, p, d1, d2), R in corners.items():
            trim.setdefault((key, p), []).append((tuple(-v for v in d1), R))
            trim.setdefault((key, p), []).append((d2, R))
        nflange = 0
        for skey, ivs in segs.items():
            key, i, line = skey[:5], skey[5], skey[6]
            layer, rtype, color, rad, ins = key
            ivs.sort()
            merged = [list(ivs[0])]
            for a, b in ivs[1:]:
                if a <= merged[-1][1] + 1e-6:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])

            def pt(s):
                q, li = [0, 0, 0], list(line)
                for j in range(3):
                    q[j] = s if j == i else li.pop(0)
                return tuple(q)

            for a, b in merged:
                for end, sgn in ((a, 1), (b, -1)):
                    for (dv, R) in trim.get((key, tuple(round(v, 2) for v in pt(end))), []):
                        if abs(dv[i] - sgn) < 1e-6:
                            if sgn > 0:
                                a = end + R
                            else:
                                b = end - R
                if b - a < .05:
                    continue
                self.pipe_run(pt(a), pt(b), rad, color, layer, ins, rtype)
                L = b - a
                n = int(L // 40)
                for k in range(1, n + 1):                     # flange pairs along the run
                    s = a + L * k / (n + 1)
                    self.flange(pt(s), i, rad, ins, layer)
                    nflange += 1
                # pipe markers every 60 ft (ASME A13.1 style): a white legend band with the
                # service colour on both sides; insulated lines carry them on the jacket
                s = a + 20
                while s < b - 10:
                    for (o0, o1, c) in ((-1.5, -.9, color), (-.9, .9, "label"), (.9, 1.5, color)):
                        lo, hi = list(pt(s + o0)), list(pt(s + o1))
                        self.rod(lo, hi, rad * 1.03, c, layer)
                    s += 60
        for (key, p, d1, d2), R in corners.items():
            layer, rtype, color, rad, ins = key
            self.elbow(p, d1, d2, R, rad, color if not ins else JACKET, layer)
        for key, p in ends:
            layer, rtype, color, rad, ins = key
            self.rod((p[0], p[1], p[2] - .1), (p[0], p[1], p[2] + .1), rad * 1.45, "steel", layer)
        for lg, rad, color, layer, ins, rtype in legs:
            self.n_conn += 1 if self.connect(lg, rad, color, layer, ins, rtype) else 0
        return len(self.parts) - self.n0

    def pipe_run(self, a, b, rad, color, layer, ins, rtype):
        self.rod(a, b, rad, JACKET if ins else color, layer, seg=16)
        if ins:                                                 # jacket seam bands every 12 ft
            ax = [j for j in range(3) if abs(a[j] - b[j]) > 1e-6][0]
            L = abs(b[ax] - a[ax])
            sgn = 1 if b[ax] > a[ax] else -1
            s = 6
            while s < L - 3:
                lo, hi = list(a), list(a)
                lo[ax] += sgn * (s - .08)
                hi[ax] += sgn * (s + .08)
                self.rod(lo, hi, rad * 1.012, "steel", layer, seg=16)
                s += 12

    def flange(self, p, axis, rad, ins, layer):
        r_f = rad * (1.18 if ins else 1.55)
        for off in (-.22, .08):
            lo, hi = list(p), list(p)
            lo[axis] += off
            hi[axis] += off + .14
            self.rod(lo, hi, r_f, "steel", layer, seg=16)

    def elbow(self, p, d1, d2, R, rad, color, layer):
        """Quarter bend from p - d1 R to p + d2 R, in 4 mitred segments."""
        C = tuple(p[j] - d1[j] * R + d2[j] * R for j in range(3))
        prev = None
        for k in range(5):
            t = math.pi / 2 * k / 4
            q = tuple(C[j] + R * (-d2[j] * math.cos(t) + d1[j] * math.sin(t)) for j in range(3))
            if prev is not None:
                # extend each segment slightly so the mitres close
                dv = [q[j] - prev[j] for j in range(3)]
                n = math.sqrt(sum(v * v for v in dv)) or 1
                e = rad * .2 / n
                a = [prev[j] - dv[j] * e for j in range(3)]
                b = [q[j] + dv[j] * e for j in range(3)]
                self.rod(a, b, rad, color, layer, seg=16)
            prev = q


def build(item, items, parts, routes):
    p = Pipes(item, items, parts, routes)
    n = p.run()
    print("pipe end connections", p.n_conn)
    return n
