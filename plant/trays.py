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

# Cable schedule (typical selection, not engineered; Southwire families named as the requested supplier,
# part numbers to be confirmed with the supplier): per tray class, the cable types laid in the tray,
# in the order they lie across it: (description, colour key, radius ft, count).
CABLES = {
    "mv_tray": [
        ("15 kV MV-105 power, 1/C Cu, 133% EPR, copper-tape shield, PVC jacket, triplexed "
         "(Southwire MV-105 type; ICEA S-93-639 / UL 1072)", "cable_mv", .30, 3),
        ("15 kV ARMOR-X MC-HL / MV-105, 3/C Cu EPR, continuous corrugated welded armor, red PVC jacket "
         "(Southwire ARMOR-X)", "cable_mv", .38, 1),
    ],
    "lv_tray": [
        ("600 V power, Cu XHHW-2, Type TC-ER, black PVC jacket (Southwire Type TC-ER; UL 1277)", "cable_tc", .20, 3),
        ("600 V ARMOR-X MC-HL power and VFD cable, Cu XHHW-2 with grounds, continuous corrugated welded "
         "aluminium armor, black PVC jacket, for Class I Div 2 areas (Southwire ARMOR-X MC-HL; UL 2225)",
         "cable_mc", .22, 2),
        ("600 V control, 14 AWG multiconductor, Type TC-ER (Southwire control cable; ICEA S-73-532)",
         "cable_tc", .10, 2),
    ],
    "control_tray": [
        ("600 V control, 14 AWG multiconductor, Type TC-ER, black (Southwire; ICEA S-73-532)", "cable_tc", .12, 2),
        ("Instrumentation, 16/18 AWG shielded pairs and triads, Type TC-ER / PLTC, blue jacket for "
         "intrinsically safe circuits (Southwire instrumentation; ICEA S-73-532)", "cable_inst", .11, 3),
        ("Thermocouple extension, type KX (exhaust and wheel-space thermocouples), yellow jacket "
         "(ANSI MC96.1 colour code; ICEA S-73-532)", "cable_tcx", .09, 2),
        ("Fire alarm, FPLR shielded, red jacket (NEC 760)", "cable_fa", .08, 1),
        ("Fibre optic (DCS / turbine control network), orange jacket", "cable_fo", .07, 1),
    ],
}
BUILDING_WIRE = ("Lighting, receptacles and small power: Cu THHN/THWN-2 building wire in rigid / EMT conduit "
                 "(Southwire SIMpull THHN; UL 83)")
GALV = "pipe"


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


class Trays:
    def __init__(self, item, items, parts, routes):
        self.items, self.parts, self.routes = items, parts, routes
        self.it = item("ROUTES_BASE", "Cable trays and isolated-phase bus (rendered from the routes)",
                       (0, 2420, 0, 1920), (0, 45), basis="typical", register=False, sheet="typical (tray detail)",
                       info="Ladder trays with cables, supports and drops, and the three-phase IPB enclosures, "
                            "generated from the route centrelines.")
        self.n0 = len(parts)
        self.gaps, self.retry, self.held, self.posts = [], [], [], []
        self.hall = next(i for i in items if i["name"] == "Common turbine hall")["fp"]
        self.deck = next(i for i in items if i["name"].startswith("Turbine deck EL 20"))["fp"]
        is_rack = lambda i: "pipe rack" in i["name"].lower() or "pipe and cable rack" in i["name"].lower()
        self.racks = [i["fp"] + [i["z"][1]] for i in items if is_rack(i) and i["z"][1] > 20]
        skip = ("Common turbine hall", "Turbine deck", "Pipe ", "Cable trays", "Laydown bay")
        self.solid = [i for i in items if i["layer"] != "SITE" and i["z"][1] > 1.5 and
                      not i["name"].startswith(skip) and not is_rack(i)]
        # obstacle index: every part already in the model that a support, drop or frame must not pass
        # through (walls, deck, pads and the ground are what supports stand on, so they are left out)
        byid = {i["id"]: i for i in items}
        free_of = ("Common turbine hall", "Turbine deck", "Laydown", "230 kV switchyard", "Pipe supports")
        self.obs, self.grid, self.obs_ok = [], {}, []
        for p in parts:
            it = byid[p["item"]]
            if it["layer"] == "SITE" or it["z"][1] < 1 or it["name"].startswith(free_of):
                continue
            b = _pbox(p)
            k = len(self.obs)
            self.obs.append(b)
            self.obs_ok.append(p["color"] in ("steel", "stair") and not it["name"].startswith(("HRSG", "Air-cooled")))
            for gx in range(int(b[0] // 10), int(b[3] // 10) + 1):
                for gy in range(int(b[1] // 10), int(b[4] // 10) + 1):
                    self.grid.setdefault((gx, gy), []).append(k)

    def free(self, *boxes):
        for (x0, x1, y0, y1, z0, z1) in boxes:
            seen = set()
            for gx in range(int(min(x0, x1) // 10), int(max(x0, x1) // 10) + 1):
                for gy in range(int(min(y0, y1) // 10), int(max(y0, y1) // 10) + 1):
                    for k in self.grid.get((gx, gy), ()):
                        if k in seen:
                            continue
                        seen.add(k)
                        b = self.obs[k]
                        if (min(max(x0, x1), b[3]) - max(min(x0, x1), b[0]) > .05 and
                                min(max(y0, y1), b[4]) - max(min(y0, y1), b[1]) > .05 and
                                min(z1, b[5]) - max(z0, b[2]) > .05):
                            return False
        return True

    def highest_below(self, x0, x1, y0, y1, z):
        """Top of the highest part under a footprint, below z."""
        top = 0.0
        for gx in range(int(x0 // 10), int(x1 // 10) + 1):
            for gy in range(int(y0 // 10), int(y1 // 10) + 1):
                for k in self.grid.get((gx, gy), ()):
                    b = self.obs[k]
                    if b[0] < x1 and b[3] > x0 and b[1] < y1 and b[4] > y0 and b[5] < z:
                        top = max(top, b[5])
        return top

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

    def side_entry(self, x, y, z):
        """The tray ends at the face of equipment or a building it enters from the side."""
        return any(i["fp"][0] - 4 <= x <= i["fp"][1] + 4 and i["fp"][2] - 4 <= y <= i["fp"][3] + 4
                   and i["z"][0] < z < i["z"][1] - .5 and not (i["fp"][0] < x < i["fp"][1] and i["fp"][2] < y < i["fp"][3])
                   for i in self.solid)

    def top_under(self, x, y, z):
        """Top of the equipment under a drop point (below the tray), else the floor."""
        tops = [i["z"][1] for i in self.solid if i["fp"][0] <= x <= i["fp"][1] and i["fp"][2] <= y <= i["fp"][3]
                and i["z"][1] <= z + .5]
        return max(tops) if tops else self.floor(x, y)

    # ---------------------------------------------------------------------------------
    def run(self):
        for r in self.routes:                                   # the schedule rides on each tray route
            if r["type"] in CABLES:
                r["cables"] = [d for (d, _, _, _) in CABLES[r["type"]]]
        runs, ends = {}, {}
        for r in self.routes:
            if r["type"] in TRAYS and r["z"] > 0:
                key = (r["layer"], r["type"], r["z"], r["w"], r["h"])
                for a, b in zip(r["points"], r["points"][1:]):
                    if a[0] == b[0] and a[1] != b[1]:
                        runs.setdefault(key + ("y", a[0]), []).append((min(a[1], b[1]), max(a[1], b[1])))
                    elif a[1] == b[1] and a[0] != b[0]:
                        runs.setdefault(key + ("x", a[1]), []).append((min(a[0], b[0]), max(a[0], b[0])))
                if r["z"] > 6 and len(r["points"]) > 1:
                    P = r["points"]
                    for p, q in ((P[0], P[1]), (P[-1], P[-2])):           # q: the neighbour, inside the run
                        dx, dy = p[0] - q[0], p[1] - q[1]
                        L = math.hypot(dx, dy) or 1
                        ends[(round(p[0], 1), round(p[1], 1), r["type"])] = (key, (dx / L, dy / L))
        merged_runs = {}
        for k, ivs in runs.items():
            ivs.sort()
            merged = [list(ivs[0])]
            for a, b in ivs[1:]:
                if a <= merged[-1][1] + 1e-6:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])
            merged_runs[k] = merged
        # radius bends: a point where exactly two runs of one tray class end at right angles, and no run
        # passes through, gets a bend fitting; the straight runs stop at its tangent points
        at = {}
        for k, ivs in merged_runs.items():
            key, axis, c = k[:5], k[5], k[6]
            for a, b in ivs:
                for v, sgn in ((a, -1), (b, 1)):
                    pt = (round(v, 2), round(c, 2)) if axis == "x" else (round(c, 2), round(v, 2))
                    at.setdefault((key, pt), []).append((axis, c, a, b, sgn))
        self.trim, bends = {}, []
        for (key, pt), lst in at.items():
            if len(lst) != 2 or lst[0][0] == lst[1][0]:
                continue
            through = any(k[:5] == key and ((k[5] == "x" and abs(k[6] - pt[1]) < .01 and any(a + .01 < pt[0] < b - .01 for a, b in iv)) or
                          (k[5] == "y" and abs(k[6] - pt[0]) < .01 and any(a + .01 < pt[1] < b - .01 for a, b in iv)))
                          for k, iv in merged_runs.items())
            R = key[3] / 2 + 1.0
            if through or any(b - a < R + 1 for (_, _, a, b, _) in lst):
                continue
            for (axis, c, a, b, sgn) in lst:
                self.trim[(key, axis, round(c, 2), round(b if sgn > 0 else a, 2))] = R
            bends.append((key, pt, lst, R))
        # junctions: an end that lies on another tray run at the same tier continues there, no drop
        segs = [(r["z"], r["points"][k], r["points"][k + 1]) for r in self.routes if r["type"] in TRAYS and r["z"] > 0
                for k in range(len(r["points"]) - 1)]

        def on_run(x, y, z):
            n = 0
            for (zz, a, b) in segs:
                if abs(zz - z) > .1:
                    continue
                if min(a[0], b[0]) - .1 <= x <= max(a[0], b[0]) + .1 and min(a[1], b[1]) - .1 <= y <= max(a[1], b[1]) + .1:
                    n += 1
            return n > 1                     # the run it ends on, plus at least one other

        # pipe routes below a drop point (a drop never passes through a pipe; the cables continue in conduit)
        pipes = [(r["z"], r["w"], a, b) for r in self.routes if r["type"] not in TRAYS and r["type"] != "ipb"
                 and 0 < r["z"] for a, b in zip(r["points"], r["points"][1:])]

        def over_pipe(x, y, z, hw):
            return any(zz < z and min(a[0], b[0]) - w / 2 - hw <= x <= max(a[0], b[0]) + w / 2 + hw and
                       min(a[1], b[1]) - w / 2 - hw <= y <= max(a[1], b[1]) + w / 2 + hw for (zz, w, a, b) in pipes)

        drops = []
        self.waterfall = {}
        for (x, y, t), (key, d) in ends.items():
            enters = any(i["fp"][0] - .5 <= x <= i["fp"][1] + .5 and i["fp"][2] - .5 <= y <= i["fp"][3] + .5
                         and i["z"][1] < key[2] and ("e-house" in i["name"] or "building" in i["name"].lower())
                         for i in self.solid)          # the tray ends over a building it enters: drop to its roof entry
            if on_run(x, y, key[2]) or self.side_entry(x, y, key[2]) or (over_pipe(x, y, key[2], key[3] / 2) and not enters):
                continue
            drops.append((key, x, y, d))
            self.waterfall[(key, round(x, 2), round(y, 2))] = d
        for k, ivs in merged_runs.items():
            for a, b in ivs:
                self.tray(k, a, b)
        # ganged trapezes: a support spot with no room for its own posts shares the posts of a parallel tray
        # beside it (one beam carries both trays), as tray tiers do in a congested area
        for (held, s0, x, y, z, zb, hw, axis, layer) in self.retry:
            cand = []
            for (px, py, pz) in self.posts:
                if abs(pz - (zb - .4)) > .6:
                    continue
                along, perp = (abs(px - x), abs(py - y)) if axis == "x" else (abs(py - y), abs(px - x))
                if along < 6 and hw < perp < 8:
                    cand.append((along + perp, px, py))
            for _, px, py in sorted(cand):
                xx, yy = (px, y) if axis == "x" else (x, py)
                bm = ((xx - .25, xx + .25, min(py, yy - hw - .3), max(py, yy + hw + .3), zb - .4, zb) if axis == "x" else
                      (min(px, xx - hw - .3), max(px, xx + hw + .3), yy - .25, yy + .25, zb - .4, zb))
                if self.free(bm):
                    self.box(*bm, "steel", layer)
                    held.append(xx if axis == "x" else yy)
                    break
        for held, a0, b0, info in self.held:
            pts = [a0] + sorted(held) + [b0]
            gap = max(q - p for p, q in zip(pts, pts[1:]))
            if gap > 22:
                self.gaps.append((round(gap),) + info)
        for b in bends:
            self.bend(*b)
        for (key, x, y, d) in drops:
            self.drop(key, x, y, d)
        for r in self.routes:
            if r["type"] == "ipb" and r["z"] > 0:
                self.ipb(r)
        return len(self.parts) - self.n0

    def lanes(self, rtype, w, zb):
        """Cable lanes across a tray: (colour, radius, offset across the tray, centre height)."""
        hw = w / 2
        cabs = [(col, r) for (_, col, r, n) in CABLES[rtype] for _ in range(n)]
        span = w - .4
        rows, row, used = [], [], 0.0
        for (col, r) in cabs:
            if row and used + 2 * r > span:
                rows.append(row)
                row, used = [], 0.0
            row.append((col, r))
            used += 2 * r
        rows.append(row)
        out, zbase = [], zb + .12
        for row in rows:
            used = sum(2 * r for _, r in row)
            gap = max(0.0, (span - used) / max(1, len(row) - 1)) if len(row) > 1 else 0
            v = -hw + .2 + (0 if len(row) > 1 else (span - used) / 2)
            for (col, r) in row:
                out.append((col, r, v + r, zbase + r))
                v += 2 * r + gap
            zbase += 2 * max(r for _, r in row) * .85
        return out

    def tray(self, key, a, b):
        layer, rtype, z, w, h, axis, c = key
        n_cab, rc, ccol = TRAYS[rtype]
        hw, zb = w / 2, z            # the tray sits ON its tier: route z is the bottom (rack beam top)
        k5 = key[:5]

        def B(s0, s1, v0, v1, z0, z1, col):
            if axis == "x":
                self.box(s0, s1, c + v0, c + v1, z0, z1, col, layer)
            else:
                self.box(c + v0, c + v1, s0, s1, z0, z1, col, layer)

        a0, b0 = a - hw, b + hw
        ta = self.trim.get((k5, axis, round(c, 2), round(a, 2)))
        tb = self.trim.get((k5, axis, round(c, 2), round(b, 2)))
        ra0, rb0 = (a + ta if ta else a0), (b - tb if tb else b0)                 # rails stop at a bend's tangent
        for s in (-1, 1):                                                       # side rails
            B(ra0, rb0, s * hw - (.12 if s > 0 else 0), s * hw + (0 if s > 0 else .12), zb, zb + h, GALV)
        s = ra0 + 1
        while s < rb0 - .5:                                                      # rungs
            B(s - .08, s + .08, -hw, hw, zb, zb + .12, GALV)
            s += 2
        # cables in schedule order, packed across the tray width in layers (never past the side rails);
        # at a bend they stop at the tangent (the bend carries them round), at a drop they stop where the
        # waterfall starts to curve them down
        Rb = 1.2
        pa_ = (a, c) if axis == "x" else (c, a)
        pb_ = (b, c) if axis == "x" else (c, b)
        ca = a + ta if ta else (a - (hw - .5 - Rb) if (k5, round(pa_[0], 2), round(pa_[1], 2)) in self.waterfall else a0 + .3)
        cb = b - tb if tb else (b + (hw - .5 - Rb) if (k5, round(pb_[0], 2), round(pb_[1], 2)) in self.waterfall else b0 - .3)
        for (col, r, v, zc) in self.lanes(rtype, w, zb):
            pa = (ca, c + v, zc) if axis == "x" else (c + v, ca, zc)
            pb = (cb, c + v, zc) if axis == "x" else (c + v, cb, zc)
            self.rod(pa, pb, r, col, layer, seg=6)
        # supports about every 10 ft; each one checks the geometry around it and shifts up to 5 ft
        # along the run, or is left out, rather than pass through steel, pipes or equipment
        L = b0 - a0
        nsup = max(1, int(L // 12))            # 12 ft support spacing (NEMA 12 ladder tray class)
        held = []
        for m in range(nsup + 1):
            s0 = a0 + .5 + (L - 1) * m / max(1, nsup)
            for ds in (0, 2.5, -2.5, 5, -5):
                s = min(max(s0 + ds, a0 + .3), b0 - .3)
                x, y = (s, c) if axis == "x" else (c, s)
                if self.on_rack(x, y, z):
                    held.append(s)
                    break
                opts = self.support(x, y, z, zb, hw, axis)
                if opts is None:
                    held.append(s)
                    break
                done = False
                for parts in opts:
                    if self.free(*[q[:6] for q in parts]):
                        for q in parts:
                            if q[6] == "box" and q[5] - q[4] > 3 and q[1] - q[0] < .5 and q[3] - q[2] < .5:
                                self.posts.append(((q[0] + q[1]) / 2, (q[2] + q[3]) / 2, q[5]))
                            if q[6] == "rod":
                                self.rod(q[7], q[8], .06 if q[5] - q[4] > 6 and q[1] - q[0] < .2 else .12, "steel", layer, seg=4)
                            else:
                                self.box(*q[:6], "steel", layer)
                        held.append(s)
                        done = True
                        break
                if done:
                    break
            else:
                self.retry.append((held, s0, x, y, z, zb, hw, axis, layer))
        self.held.append((held, a0, b0, (layer, rtype, axis, round(c, 1), round(a, 1), round(b, 1), z)))

    def lowest_above(self, x0, x1, y0, y1, z, reach=24):
        """Bottom of the lowest part over a footprint within reach above z (structure to hang from), else None."""
        best = None
        for gx in range(int(x0 // 10), int(x1 // 10) + 1):
            for gy in range(int(y0 // 10), int(y1 // 10) + 1):
                for k in self.grid.get((gx, gy), ()):
                    b = self.obs[k]
                    if b[0] < x1 and b[3] > x0 and b[1] < y1 and b[4] > y0 and z < b[2] < z + reach:
                        best = b[2] if best is None else min(best, b[2])
        return best

    def support(self, x, y, z, zb, hw, axis):
        """Candidate supports, each a list of boxes (x0, x1, y0, y1, z0, z1, kind, ...), tried in order;
        None where none is needed (the tray sits just above the floor)."""
        if self.in_hall(x, y) and axis == "x":
            f = self.hall
            yn, ys = f[3] - 4, f[2] + 34
            if min(abs(y - yn), abs(y - ys)) <= 14:                              # wall bracket from the columns
                yw = yn if abs(y - yn) < abs(y - ys) else ys
                yk = yw + (y - yw) * .7
                arm = (x - .2, x + .2, min(y - hw - .5, yw), max(y + hw + .5, yw), zb - .45, zb, "box")
                brace = (x - .12, x + .12, min(yw, yk), max(yw, yk), zb - 5.5, zb - .45, "rod", (x, yw, zb - 5.5),
                         (x, yk, zb - .45))
                return [[arm, brace]]
        base = self.floor(x, y)
        if z - base < 3:
            return None
        beam = ((x - .25, x + .25, y - hw - .6, y + hw + .6, zb - .4, zb, "box") if axis == "x" else
                (x - hw - .6, x + hw + .6, y - .25, y + .25, zb - .4, zb, "box"))
        opts = []
        # 1. trapeze stanchion pair from the floor (grade, or the EL 20 deck in the hall); it is placed only
        #    where the actual parts leave room (the equipment envelope alone no longer rules it out)
        for off in (.4, 2.6):                     # wider portal where the tray rides over a pipe on the same line
            st = []
            for sgn in (-1, 1):
                px, py = (x, y + sgn * (hw + off)) if axis == "x" else (x + sgn * (hw + off), y)
                st.append((px - .22, px + .22, py - .22, py + .22, base, zb - .4, "box"))
            bm = ((x - .25, x + .25, y - hw - off - .2, y + hw + off + .2, zb - .4, zb, "box") if axis == "x" else
                  (x - hw - off - .2, x + hw + off + .2, y - .25, y + .25, zb - .4, zb, "box"))
            opts.append(st + [bm])
        # 1a. single-post cantilever (T-support) beside equipment that leaves no room on one side
        for off in (.4, 2.6, 4.5):
            for sgn in (-1, 1):
                px, py = (x, y + sgn * (hw + off)) if axis == "x" else (x + sgn * (hw + off), y)
                post = (px - .25, px + .25, py - .25, py + .25, base, zb - .4, "box")
                arm = ((x - .25, x + .25, min(py, y - hw - .3), max(py, y + hw + .3), zb - .4, zb, "box") if axis == "x" else
                       (min(px, x - hw - .3), max(px, x + hw + .3), y - .25, y + .25, zb - .4, zb, "box"))
                opts.append([post, arm])
        # 1b. stanchions on a flat e-house / building roof under the tray
        roof = [i["z"][1] for i in self.solid if i["fp"][0] <= x <= i["fp"][1] and i["fp"][2] <= y <= i["fp"][3]
                and i["z"][1] < zb - 3 and ("e-house" in i["name"] or "building" in i["name"].lower())]
        if roof:
            rb = max(roof) + .2                   # on the roof membrane, clear of its flashing
            st = []
            for sgn in (-1, 1):
                px, py = (x, y + sgn * (hw + .4)) if axis == "x" else (x + sgn * (hw + .4), y)
                st.append((px - .22, px + .22, py - .22, py + .22, rb, zb - .4, "box"))
            opts.append(st + [beam])
        # 2. trapeze hung on threaded rods from the steel above (ACC deck beams, platforms, rack steel);
        #    not in the turbine hall, where the crane travels under the roof
        if True:
            x0, x1 = (x - .3, x + .3) if axis == "x" else (x - hw - .5, x + hw + .5)
            y0, y1 = (y - hw - .5, y + hw + .5) if axis == "x" else (y - .3, y + .3)
            top = self.lowest_above(x0, x1, y0, y1, zb + 1.5, reach=30)
            if top is not None and (not self.in_hall(x, y) or top < 80):    # in the hall: never into the crane path
                hg = []
                for sgn in (-1, 1):
                    px, py = (x, y + sgn * (hw + .4)) if axis == "x" else (x + sgn * (hw + .4), y)
                    hg.append((px - .06, px + .06, py - .06, py + .06, zb - .4, top, "rod", (px, py, zb - .4), (px, py, top)))
                opts.append(hg + [beam])
        # 3. cantilever bracket with knee brace off a nearby column or post (ACC, rack, platform steel)
        col = self.column_near(x, y, zb, hw, axis)
        if col is not None:
            cx, cy = col
            if axis == "x":
                arm = (x - .2, x + .2, min(cy, y - hw - .5), max(cy, y + hw + .5), zb - .45, zb, "box")
                yk = cy + (y - cy) * .7
                brace = (x - .12, x + .12, min(cy, yk), max(cy, yk), zb - 5, zb - .45, "rod", (x, cy, zb - 5), (x, yk, zb - .45))
            else:
                arm = (min(cx, x - hw - .5), max(cx, x + hw + .5), y - .2, y + .2, zb - .45, zb, "box")
                xk = cx + (x - cx) * .7
                brace = (min(cx, xk), max(cx, xk), y - .12, y + .12, zb - 5, zb - .45, "rod", (cx, y, zb - 5), (xk, y, zb - .45))
            opts.append([arm, brace])
        return opts

    def column_near(self, x, y, zb, hw, axis, reach=12):
        """Face of the nearest slender vertical member beside the tray (spanning the tray height), else None."""
        best = None
        for gx in range(int((x - reach) // 10), int((x + reach) // 10) + 1):
            for gy in range(int((y - reach) // 10), int((y + reach) // 10) + 1):
                for k in self.grid.get((gx, gy), ()):
                    b = self.obs[k]
                    if not self.obs_ok[k] or not (b[2] < zb - 6 and b[5] > zb + .5 and b[3] - b[0] < 3.5 and b[4] - b[1] < 3.5):
                        continue
                    if axis == "x" and b[0] - .5 <= x <= b[3] + .5:
                        d = min(abs(b[1] - y), abs(b[4] - y))
                        if hw < d < reach and (best is None or d < best[0]):
                            best = (d, (x, b[1] - .15 if b[1] > y else b[4] + .15))
                    if axis == "y" and b[1] - .5 <= y <= b[4] + .5:
                        d = min(abs(b[0] - x), abs(b[3] - x))
                        if hw < d < reach and (best is None or d < best[0]):
                            best = (d, (b[0] - .15 if b[0] > x else b[3] + .15, y))
        return best[1] if best else None

    def bend(self, key, pt, lst, R):
        """Radius bend fitting at an L corner: curved side rails, radial rungs, cables swept round."""
        layer, rtype, z, w, h = key
        hw, zb = w / 2, z
        x, y = pt
        # unit directions: d1 along the first run towards the corner, d2 from the corner along the second
        (ax1, c1, a1, b1, s1), (ax2, c2, a2, b2, s2) = lst
        d1 = (s1, 0) if ax1 == "x" else (0, s1)
        d2 = (-s2, 0) if ax2 == "x" else (0, -s2)
        T1 = (x - d1[0] * R, y - d1[1] * R)
        O = (T1[0] + d2[0] * R, T1[1] + d2[1] * R)
        n = 8

        def P(rr, th):
            return (O[0] - d2[0] * rr * math.cos(th) + d1[0] * rr * math.sin(th),
                    O[1] - d2[1] * rr * math.cos(th) + d1[1] * rr * math.sin(th))
        for rr in (R - hw, R + hw):                                              # side rails
            for k in range(n):
                t0, t1 = math.pi / 2 * k / n, math.pi / 2 * (k + 1) / n
                pi0, pi1 = P(rr - .06, t0), P(rr - .06, t1)
                po0, po1 = P(rr + .06, t0), P(rr + .06, t1)
                v = [[*pi0, zb], [*pi1, zb], [*po1, zb], [*po0, zb], [*pi0, zb + h], [*pi1, zb + h], [*po1, zb + h], [*po0, zb + h]]
                self.add("hex", layer, v=[[round(q, 2) for q in p] for p in v], color=GALV)
        for k in range(1, 4):                                                    # rungs
            th = math.pi / 2 * k / 4
            p0, p1 = P(R - hw, th), P(R + hw, th)
            self.rod((*p0, zb + .06), (*p1, zb + .06), .07, GALV, layer, seg=4)
        # cables: the lane at offset v (across the first run, + = along +y / +x) lies at radius R - s,
        # s = its offset towards the inside of the bend
        perp1 = (0, 1) if ax1 == "x" else (1, 0)
        sgn = perp1[0] * d2[0] + perp1[1] * d2[1]
        for (col, r, v, zc) in self.lanes(rtype, w, zb):
            rr = R - v * sgn
            pts = [(*P(rr, math.pi / 2 * k / n), zc) for k in range(n + 1)]
            for p, q in zip(pts, pts[1:]):
                self.rod(p, q, r, col, layer, seg=6)

    def drop(self, key, x, y, d=(0, 1)):
        layer, rtype, z, w, h = key
        n_cab, rc, ccol = TRAYS[rtype]
        hw = w / 2
        # the drop lands on whatever is below it (equipment top, pipe, platform), never passes through
        bottom = max(self.top_under(x, y, z), self.highest_below(x - hw, x + hw, y - hw, y + hw, z)) + .3
        if z - bottom < 2 or not self.free((x - hw, x + hw, y - hw, y + hw, bottom + .05, z)):
            return
        dx, dy = (1 if abs(d[0]) > abs(d[1]) else 0) * (1 if d[0] > 0 else -1), (1 if abs(d[1]) >= abs(d[0]) else 0) * (1 if d[1] > 0 else -1)
        lat = (abs(dy), abs(dx))                                                  # across the tray
        for s in (-1, 1):                                                       # vertical side rails
            cx, cy = x + lat[0] * s * hw, y + lat[1] * s * hw
            ox, oy = x + dx * hw, y + dy * hw                                     # channel rails on the outer face
            if dx:
                self.box(min(ox, ox - dx * .4), max(ox, ox - dx * .4), cy - .06, cy + .06, bottom, z, GALV, layer)
            else:
                self.box(cx - .06, cx + .06, min(oy, oy - dy * .4), max(oy, oy - dy * .4), bottom, z, GALV, layer)
        zz = bottom + 1
        fx, fy = x + dx * hw, y + dy * hw                                         # rungs on the outer face
        while zz < z - .5:
            if dx:
                self.box(fx - .1 * dx, fx, y - hw, y + hw, zz - .08, zz + .08, GALV, layer)
            else:
                self.box(x - hw, x + hw, fy - .1 * dy, fy, zz - .08, zz + .08, GALV, layer)
            zz += 2
        # waterfall: each cable leaves the tray, curves down over a 1.2 ft radius and drops against the
        # rungs to a gland at the equipment
        Rb, e0 = 1.2, hw - .5 - 1.2
        for (col, r, v, zc) in self.lanes(rtype, w, z)[:6]:
            bx, by = x + lat[0] * v, y + lat[1] * v
            S = (bx + dx * e0, by + dy * e0)
            pts = []
            for k in range(7):
                th = math.pi / 2 * k / 6
                pts.append((S[0] + dx * Rb * math.sin(th), S[1] + dy * Rb * math.sin(th), zc - Rb * (1 - math.cos(th))))
            ex, ey = pts[-1][0], pts[-1][1]
            pts.append((ex, ey, bottom + .5))
            for p, q in zip(pts, pts[1:]):
                self.rod(p, q, r, col, layer, seg=6)
            self.rod((ex, ey, bottom), (ex, ey, bottom + .5), r + .08, "steel", layer, seg=8)   # cable gland

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
                self.rod(pa, pb, 1.0, "ipb", layer, seg=16)
                L = abs(b[0] - a[0]) + abs(b[1] - a[1])
                n = int(L // 10)
                for m in range(1, n + 1):                                         # joint bands
                    t = m / (n + 1)
                    q = [pa[j] + (pb[j] - pa[j]) * t for j in range(3)]
                    d = [(pb[j] - pa[j]) / L * .2 for j in range(3)]
                    self.rod([q[j] - d[j] for j in range(3)], [q[j] + d[j] for j in range(3)], 1.12, "steel", layer,
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
                    fr = [(x - .3, x + .3, y - 4.8, y + 4.8, z - 1.6, z - 1.1)] + \
                         [(x - .25, x + .25, y + s * 4.8 - .25, y + s * 4.8 + .25, base, z - 1.1) for s in (-1, 1)]
                else:
                    fr = [(x - 4.8, x + 4.8, y - .3, y + .3, z - 1.6, z - 1.1)] + \
                         [(x + s * 4.8 - .25, x + s * 4.8 + .25, y - .25, y + .25, base, z - 1.1) for s in (-1, 1)]
                if not self.free(*fr):
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
    t = Trays(item, items, parts, routes)
    n = t.run()
    build.gaps = t.gaps
    return n
