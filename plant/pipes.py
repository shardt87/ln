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
    "hydrogen": (False, 1.0), "lng": (True, 1.0),
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

    def run(self):
        segs, corners, ends = {}, {}, []
        for r in self.routes:
            if r["type"] not in PIPE or r["z"] <= 0:
                continue
            ins, _ = PIPE[r["type"]]
            rad = r["w"] / 2 * (.92 if ins else .8)
            z = r["z"]
            pts = [tuple(p) for p in r["points"]]
            P3 = [(x, y, z) for x, y in pts]
            if z > 6:                                         # drop to grade at both ends
                P3 = [(pts[0][0], pts[0][1], .6)] + P3 + [(pts[-1][0], pts[-1][1], .6)]
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
                if ins:                                         # coloured ID bands
                    s = a + 20
                    while s < b - 10:
                        lo, hi = list(pt(s - .9)), list(pt(s + .9))
                        self.rod(lo, hi, rad * 1.025, color, layer)
                        s += 60
        for (key, p, d1, d2), R in corners.items():
            layer, rtype, color, rad, ins = key
            self.elbow(p, d1, d2, R, rad, color if not ins else JACKET, layer)
        for key, p in ends:
            layer, rtype, color, rad, ins = key
            self.rod((p[0], p[1], p[2] - .1), (p[0], p[1], p[2] + .1), rad * 1.45, "steel", layer)
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
    return Pipes(item, items, parts, routes).run()
