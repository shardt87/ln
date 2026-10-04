"""Detail pass (LOD 2) for the SK-3X1 model.

Adds the fine engineering detail that makes the plant read as a plant:
open stair towers with landings and handrails, guarded platforms, caged
ladders, transformer radiator fans and bushing sheds, lattice bracing on
switchyard structures, rack piping, HRSG downcomers and side platforms,
building doors and louvres, light poles and fence posts.

Every part added here carries "d": 1. verify.py checks the primary
geometry against the drawing and treats detail parts as dressing; all of it
is typical (no drawing gives it).
"""
import math
import re

HANDRAIL_H = 3.5
POST = 0.18


class Detail:
    def __init__(self, items, parts):
        self.items, self.parts = items, parts
        self.by_id = {it["id"]: it for it in items}
        self.n0 = len(parts)

    # -- primitives ----------------------------------------------------------
    def box(self, item, layer, x0, x1, y0, y1, z0, z1, c):
        self.parts.append(dict(kind="box", min=[x0, y0, z0], max=[x1, y1, max(z1, z0 + .05)], color=c,
                               item=item, layer=layer, d=1))

    def rod(self, item, layer, a, b, r, c, r2=None, seg=8):
        self.parts.append(dict(kind="rod", a=list(a), b=list(b), r=r, r2=r if r2 is None else r2, color=c,
                               seg=seg, item=item, layer=layer, d=1))

    def hexa(self, item, layer, v, c):
        self.parts.append(dict(kind="hex", v=[list(p) for p in v], color=c, item=item, layer=layer, d=1))

    # -- building blocks -------------------------------------------------------
    def rail_line(self, it, ly, a, b, z, posts=True):
        """Guard rail along a straight edge: top rail, mid rail, posts."""
        (x0, y0), (x1, y1) = a, b
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 0.5:
            return
        for h in (HANDRAIL_H, HANDRAIL_H / 2):
            self.rod(it, ly, (x0, y0, z + h), (x1, y1, z + h), .09, "rail", seg=6)
        if posts:
            n = max(1, int(L / 6))
            for k in range(n + 1):
                t = k / n
                x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                self.box(it, ly, x - POST / 2, x + POST / 2, y - POST / 2, y + POST / 2, z, z + HANDRAIL_H, "rail")
        # toe board
        self.rod(it, ly, (x0, y0, z + .25), (x1, y1, z + .25), .12, "rail", seg=4)

    def rail_rect(self, it, ly, x0, x1, y0, y1, z, skip=()):
        edges = {"s": ((x0, y0), (x1, y0)), "e": ((x1, y0), (x1, y1)), "n": ((x1, y1), (x0, y1)), "w": ((x0, y1), (x0, y0))}
        for k, (a, b) in edges.items():
            if k not in skip:
                self.rail_line(it, ly, a, b, z)

    def rail_ring(self, it, ly, cx, cy, r, z, n=24):
        pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
        for k in range(n):
            a, b = pts[k], pts[(k + 1) % n]
            for h in (HANDRAIL_H, HANDRAIL_H / 2):
                self.rod(it, ly, (a[0], a[1], z + h), (b[0], b[1], z + h), .09, "rail", seg=4)
            if k % 2 == 0:
                self.box(it, ly, a[0] - .09, a[0] + .09, a[1] - .09, a[1] + .09, z, z + HANDRAIL_H, "rail")

    def stair_tower(self, it, ly, x0, x1, y0, y1, z1):
        """Open steel stair tower: four columns, landings every ~12 ft,
        switchback flights and guard rails."""
        for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            self.box(it, ly, x - .35, x + .35, y - .35, y + .35, 0, z1, "steel")
        W, D = x1 - x0, y1 - y0
        along_y = D >= W
        n = max(1, round(z1 / 12))
        h = z1 / n
        for k in range(1, n + 1):
            z = k * h
            # landing at alternate ends
            if along_y:
                ly0, ly1 = (y1 - 3.2, y1) if k % 2 else (y0, y0 + 3.2)
                self.box(it, ly, x0, x1, ly0, ly1, z - .3, z, "grating")
                self.rail_line(it, ly, (x0, ly0), (x0, ly1), z, posts=False)
                self.rail_line(it, ly, (x1, ly0), (x1, ly1), z, posts=False)
                # flight from the previous landing
                za = z - h
                ya, yb = (y0 + 3.2, y1 - 3.2) if k % 2 else (y1 - 3.2, y0 + 3.2)
                xm0, xm1 = (x0, x0 + W / 2 - .2) if k % 2 else (x0 + W / 2 + .2, x1)
                zb0 = max(za - .4, 0)
                self.hexa(it, ly, [(xm0, ya, zb0), (xm1, ya, zb0), (xm1, ya, za + (.4 if za == 0 else 0)), (xm0, ya, za + (.4 if za == 0 else 0)),
                                   (xm0, yb, z - .4), (xm1, yb, z - .4), (xm1, yb, z), (xm0, yb, z)], "stair")
                for xs in (xm0, xm1):
                    self.rod(it, ly, (xs, ya, za + HANDRAIL_H), (xs, yb, z + HANDRAIL_H), .09, "rail", seg=4)
            else:
                lx0, lx1 = (x1 - 3.2, x1) if k % 2 else (x0, x0 + 3.2)
                self.box(it, ly, lx0, lx1, y0, y1, z - .3, z, "grating")
                za = z - h
                xa, xb = (x0 + 3.2, x1 - 3.2) if k % 2 else (x1 - 3.2, x0 + 3.2)
                ym0, ym1 = (y0, y0 + D / 2 - .2) if k % 2 else (y0 + D / 2 + .2, y1)
                zb0 = max(za - .4, 0)
                self.hexa(it, ly, [(xa, ym0, zb0), (xa, ym1, zb0), (xa, ym1, za + (.4 if za == 0 else 0)), (xa, ym0, za + (.4 if za == 0 else 0)),
                                   (xb, ym0, z - .4), (xb, ym1, z - .4), (xb, ym1, z), (xb, ym0, z)], "stair")
                for ys in (ym0, ym1):
                    self.rod(it, ly, (xa, ys, za + HANDRAIL_H), (xb, ys, z + HANDRAIL_H), .09, "rail", seg=4)
        # bracing on the two long faces
        for k in range(n):
            za, zb = k * h, (k + 1) * h
            if along_y:
                for xx in (x0, x1):
                    self.rod(it, ly, (xx, y0, za), (xx, y1, zb), .12, "steel", seg=4)
            else:
                for yy in (y0, y1):
                    self.rod(it, ly, (x0, yy, za), (x1, yy, zb), .12, "steel", seg=4)

    def caged_ladder(self, it, ly, x, y, z0, z1, nx, ny):
        """Ladder on a vessel wall at (x, y), outward normal (nx, ny)."""
        tx, ty = -ny, nx
        for s in (-.8, .8):
            self.rod(it, ly, (x + tx * s, y + ty * s, z0), (x + tx * s, y + ty * s, z1), .1, "rail", seg=4)
        zc = z0 + 8
        while zc < z1:
            pts = [(x + tx * 1.4 * math.cos(a) + nx * (1.2 + 1.4 * math.sin(a)),
                    y + ty * 1.4 * math.cos(a) + ny * (1.2 + 1.4 * math.sin(a))) for a in
                   [math.pi * k / 6 for k in range(7)]]
            for a, b in zip(pts, pts[1:]):
                self.rod(it, ly, (a[0], a[1], zc), (b[0], b[1], zc), .07, "rail", seg=4)
            zc += 6
        for s in (-1.4, 0, 1.4):
            px, py = x + tx * s + nx * (1.2 + (1.4 if s == 0 else 0)), y + ty * s + ny * (1.2 + (1.4 if s == 0 else 0))
            self.rod(it, ly, (px, py, z0 + 8), (px, py, z1), .06, "rail", seg=4)

    # -- passes ----------------------------------------------------------------
    def run(self):
        P = self.parts
        by_item = {}
        for i, p in enumerate(P):
            by_item.setdefault(p["item"], []).append(i)
        drop = set()
        for iid, idxs in by_item.items():
            it = self.by_id[iid]
            name = it["name"]
            for i in idxs:
                p = P[i]
                c, k, ly = p["color"], p["kind"], p["layer"]
                # open stair towers replace solid blocks
                if c == "stair" and k == "box":
                    (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
                    if z1 - z0 > 20:
                        drop.add(i)
                        self.stair_tower(iid, ly, x0, x1, y0, y1, z1)
                # guard rails on rectangular gratings (platforms)
                if c == "grating" and k == "box":
                    (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
                    if z1 > 20 and (x1 - x0) > 4 and (y1 - y0) > 4:
                        self.rail_rect(iid, ly, x0, x1, y0, y1, z1)
                # guard rails on ring platforms (stacks, absorbers, strippers)
                if c == "grating" and k == "rod" and p["a"][0] == p["b"][0] and p["a"][1] == p["b"][1]:
                    self.rail_ring(iid, ly, p["a"][0], p["a"][1], p["r"] - .3, max(p["a"][2], p["b"][2]))
                # bushing and post-insulator sheds
                if c == "insulator" and k == "rod":
                    a, b = p["a"], p["b"]
                    L = math.dist(a, b)
                    n = max(3, int(L / 1.4))
                    for s in range(1, n):
                        t = s / n
                        q = [a[j] + (b[j] - a[j]) * t for j in range(3)]
                        d = [(b[j] - a[j]) / L for j in range(3)]
                        rr = (p["r"] + (p["r2"] - p["r"]) * t) * 1.9
                        self.rod(iid, ly, [q[j] - d[j] * .12 for j in range(3)], [q[j] + d[j] * .12 for j in range(3)],
                                 rr, "insulator", seg=12)
                # transformer radiators: cooling fans under each bank and header pipes
                if c == "radiator" and k == "box" and p["min"][2] >= 2.2:
                    (x0, y0, z0), (x1, y1, z1) = p["min"], p["max"]
                    if x1 - x0 > y1 - y0:          # bank sticks out along x
                        self.rod(iid, ly, ((x0 + x1) / 2, (y0 + y1) / 2, z0 - .2), ((x0 + x1) / 2, (y0 + y1) / 2, z0 - 1.4),
                                 min(1.4, (x1 - x0) / 3), "fan", seg=12)
                    else:
                        self.rod(iid, ly, ((x0 + x1) / 2, (y0 + y1) / 2, z0 - .2), ((x0 + x1) / 2, (y0 + y1) / 2, z0 - 1.4),
                                 min(1.4, (y1 - y0) / 3), "fan", seg=12)
            # vessels: caged ladders on stacks, absorbers, strippers, water tanks
            if re.search(r"stack$|^Absorber|^STR-|water tank|Condensate storage", name) and it["shape"] == "circle":
                cx, cy = (it["fp"][0] + it["fp"][1]) / 2, (it["fp"][2] + it["fp"][3]) / 2
                r = (it["fp"][1] - it["fp"][0]) / 2
                top = it["z"][1]
                shell = [P[i] for i in idxs if P[i]["kind"] == "rod" and P[i]["color"] in ("stack", "ccs", "tank")]
                if shell:
                    top = max(max(s["a"][2], s["b"][2]) for s in shell if s["r"] >= r * .7) if any(
                        s["r"] >= r * .7 for s in shell) else top
                    r = max(s["r"] for s in shell)
                    ang = math.radians(225)
                    nx, ny = math.cos(ang), math.sin(ang)
                    self.caged_ladder(iid, it["layer"], cx + nx * r, cy + ny * r, 0, top, nx, ny)
                    if "tank" in name.lower():
                        self.rail_ring(iid, it["layer"], cx, cy, r * .96, top)
        # remove replaced blocks (iterate descending so indices stay valid)
        for i in sorted(drop, reverse=True):
            del P[i]
        self.hrsg()
        self.switchyard()
        self.racks()
        self.buildings()
        self.site()
        return len(P) - self.n0 + len(drop)

    def find(self, pat):
        return [it for it in self.items if re.search(pat, it["name"])]

    def hrsg(self):
        for it in self.find(r"^HRSG \d \+ SCR"):
            x0, x1, y0, y1 = it["fp"]
            iid, ly = it["id"], it["layer"]
            # side access platforms (east face) with rails, at three levels
            for z in (25, 50, 74):
                self.box(iid, ly, x1, x1 + 5, y0 + 12, y1 - 30, z - .4, z, "grating")
                self.rail_line(iid, ly, (x1 + 5, y0 + 12), (x1 + 5, y1 - 30), z)
                for yy in range(int(y0 + 12), int(y1 - 30) + 1, 20):
                    self.rod(iid, ly, (x1, yy, z - .4), (x1 + 5, yy, z - 3.5), .15, "steel", seg=4)
            # (downcomers are drawn per drum in hrsg.py)
            # corner columns
            for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                self.box(iid, ly, x - .6, x + .6, y - .6, y + .6, 0, 79, "steel")

    def switchyard(self):
        # lattice bracing on dead-end structures (columns at yb +/- 11)
        for it in self.find(r"dead-end structure"):
            x = (it["fp"][0] + it["fp"][1]) / 2
            y0, y1 = it["fp"][2] + 1, it["fp"][3] - 1
            for (za, zb) in ((0, 14), (14, 28), (28, 43)):
                self.rod(it["id"], it["layer"], (x, y0, za), (x, y1, zb), .18, "steel", seg=4)
                self.rod(it["id"], it["layer"], (x, y1, za), (x, y0, zb), .18, "steel", seg=4)
                self.rod(it["id"], it["layer"], (x, y0, zb), (x, y1, zb), .15, "steel", seg=4)
            # shield-wire peaks
            for yy in (y0, y1):
                self.rod(it["id"], it["layer"], (x, yy, 47), (x, yy, 55), .25, "steel", r2=.12, seg=4)
        # overhead shield wires along both buses
        its = self.find(r"^230 kV bus 1") + self.find(r"^230 kV bus 2")
        for it in its:
            yb = (it["fp"][2] + it["fp"][3]) / 2
            for yy in (yb - 11, yb + 11):
                self.rod(it["id"], it["layer"], (530, yy, 55), (1925, yy, 55), .08, "conductor", seg=4)
        # (control-cable trenches: switchyard.py)

    def racks(self):
        # process pipes on the EL 24 and EL 30 tiers (the drawn routes carry the rest)
        for it in self.find(r"pipe and cable rack|N-S pipe rack"):
            x0, x1, y0, y1 = it["fp"]
            iid, ly = it["id"], it["layer"]
            along_x = (x1 - x0) > (y1 - y0)
            specs = [(24, 2.0, .20), (24, 1.2, .30), (24, 1.6, .78), (30, 1.4, .66), (30, .9, .76), (30, 2.2, .88)]
            # (tier-30 pipes on the north half: the LV tray rides tier 30 at y 838 and its legs leave south)
            # a rack that ENDS in another rack stops at that rack's edge and its lines tee into the other
            # rack's lines of the same tier; a rack crossed in its middle keeps its lines running through
            tee = None
            for o in self.find(r"pipe and cable rack|N-S pipe rack"):
                if o is it:
                    continue
                ox0, ox1, oy0, oy1 = o["fp"]
                if not (ox0 < x1 and ox1 > x0 and oy0 < y1 and oy1 > y0):
                    continue
                if along_x and (ox0 <= x0 + 1 or ox1 >= x1 - 1):
                    tee = ("x0", ox1, o) if ox0 <= x0 + 1 else ("x1", ox0, o)
                elif not along_x and (oy0 <= y0 + 1 or oy1 >= y1 - 1):
                    tee = ("y0", oy1, o) if oy0 <= y0 + 1 else ("y1", oy0, o)
            if tee:
                if tee[0] == "x0":
                    x0 = tee[1]
                elif tee[0] == "x1":
                    x1 = tee[1]
                elif tee[0] == "y0":
                    y0 = tee[1]
                else:
                    y1 = tee[1]
            for (z, dia, f) in specs:
                r = dia / 2
                if along_x:
                    y = y0 + (y1 - y0) * f
                    a, b = (x0 + 2, y, z + r), (x1 - 2, y, z + r)
                else:
                    x = x0 + (x1 - x0) * f
                    a, b = (x, y0 + 2, z + r), (x, y1 - 2, z + r)
                ends = []
                if tee:
                    # carry the line into the other rack to the first line on the same tier (a tee)
                    o = tee[2]
                    oy = [o["fp"][2] + (o["fp"][3] - o["fp"][2]) * ff for (zz, dd, ff) in specs if zz == z]
                    ox = [o["fp"][0] + (o["fp"][1] - o["fp"][0]) * ff for (zz, dd, ff) in specs if zz == z]
                    if tee[0] == "y1":
                        b = (b[0], min(oy), b[2])
                    elif tee[0] == "y0":
                        a = (a[0], max(oy), a[2])
                    elif tee[0] == "x1":
                        b = (min(ox), b[1], b[2])
                    else:
                        a = (max(ox), a[1], a[2])
                    ends = [b if tee[0] in ("y1", "x1") else a, (b[0], 834.5, z + r), (a[0], 841.5, z + r)]
                drop_at = []
                k = specs.index((z, dia, f))
                back = 2 + 12 * k                                       # each line peels off at its own bent
                if not ends or ends[0] is not a:
                    a = (a[0] + back, a[1], a[2]) if along_x else (a[0], a[1] + back, a[2])
                    drop_at.append(a)
                if not ends or ends[0] is not b:
                    b = (b[0] - back, b[1], b[2]) if along_x else (b[0], b[1] - back, b[2])
                    drop_at.append(b)
                jog = None
                if tee and tee[0] in ("y1", "y0") and z == 30:
                    # the tier-30 LV tray runs along the other rack at y 837-839: hop over it
                    yj = 834.5 if tee[0] == "y1" else 841.5
                    end = b if tee[0] == "y1" else a
                    jog = [(end[0], yj, z + r), (end[0], yj, z + r + 3.4), (end[0], end[1], z + r + 3.4), end]
                    if tee[0] == "y1":
                        b = jog[0]
                    else:
                        a = jog[0]
                self.rod(iid, ly, a, b, r, "pipe", seg=10)
                if jog:
                    for q0, q1 in zip(jog, jog[1:]):
                        self.rod(iid, ly, q0, q1, r, "pipe", seg=10)
                    for q in jog[1:3]:
                        self.rod(iid, ly, (q[0], q[1], q[2] - r * 1.1), (q[0], q[1], q[2] + r * 1.1), r * 1.12, "pipe", seg=10)
                # free ends: lines peel off one by one toward the rack end, each elbowing down at its own
                # bent and dropping to its user at grade (isolation valve, pipe support at the foot)
                for e2 in drop_at:
                    top, foot = e2[2], 1.2
                    self.rod(iid, ly, (e2[0], e2[1], top - r * 1.1), (e2[0], e2[1], top + r * 1.1), r * 1.12, "pipe", seg=10)
                    self.rod(iid, ly, (e2[0], e2[1], top), (e2[0], e2[1], foot), r, "pipe", seg=10)
                    zv = min(6.5, top - 3)                              # isolation valve with a handwheel
                    self.rod(iid, ly, (e2[0], e2[1], zv - r * .9), (e2[0], e2[1], zv + r * .9), r * 1.6, "steel", seg=10)
                    hx, hy = (0, 1.2) if along_x else (1.2, 0)
                    self.rod(iid, ly, (e2[0], e2[1], zv), (e2[0] + hx, e2[1] + hy, zv), .1, "steel", seg=4)
                    self.rod(iid, ly, (e2[0] + hx, e2[1] + hy, zv), (e2[0] + hx * 1.1, e2[1] + hy * 1.1, zv), max(r, .5),
                             "red", seg=10)
                    self.box(iid, ly, e2[0] - r - .4, e2[0] + r + .4, e2[1] - r - .4, e2[1] + r + .4, 0, foot - r * .2, "concrete")
            # longitudinal bracing in every third bay
            if along_x:
                for x in range(int(x0), int(x1) - 25, 75):
                    for yy in (y0 + 2.3, y1 - 2.3):
                        self.rod(iid, ly, (x, yy, 0), (x + 25, yy, 23), .2, "steel", seg=4)
            else:
                for y in range(int(y0), int(y1) - 25, 75):
                    for xx in (x0 + 2.3, x1 - 2.3):
                        self.rod(iid, ly, (xx, y, 0), (xx, y + 25, 23), .2, "steel", seg=4)

    def buildings(self):
        """Doors and wall louvres on buildings and e-houses (south face)."""
        for it in self.items:
            ids = [p for p in self.parts if p["item"] == it["id"] and p.get("d") != 1]
            cols = {p["color"] for p in ids}
            x0, x1, y0, y1 = it["fp"]
            if not it["register"] or it["layer"].startswith("R1_") or it["layer"].startswith("R4_"):
                continue
            if "building" in cols and (x1 - x0) > 20 and "parapet" not in it["name"]:
                w = x1 - x0
                h = it["z"][1]
                # personnel door + roll-up door + louvre band
                self.box(it["id"], it["layer"], x0 + w * .15, x0 + w * .15 + 3.5, y0 - .25, y0, 0, 7.5, "door")
                if w > 60:
                    self.box(it["id"], it["layer"], x0 + w * .55, x0 + w * .55 + 14, y0 - .25, y0, 0, 14, "rollup")
                self.box(it["id"], it["layer"], x0 + w * .3, x0 + w * .3 + 8, y0 - .2, y0, h * .55, h * .55 + 3, "louvre")
            if "ehouse" in cols and "roof" in cols and (x1 - x0) >= 20:
                # door with a small stair and landing on the south face
                w = x1 - x0
                dx = x0 + w * .2
                self.box(it["id"], it["layer"], dx, dx + 3.5, y0 - .2, y0, 2.5, 9.5, "door")
                self.box(it["id"], it["layer"], dx - 1, dx + 4.5, y0 - 4, y0, 2.2, 2.5, "grating")
                self.hexa(it["id"], it["layer"], [(dx - 1, y0 - 4, 2.5), (dx + 4.5, y0 - 4, 2.5), (dx + 4.5, y0 - 4, 2.1),
                                                   (dx - 1, y0 - 4, 2.1), (dx - 1, y0 - 8, .2), (dx + 4.5, y0 - 8, .2),
                                                   (dx + 4.5, y0 - 8, 0), (dx - 1, y0 - 8, 0)], "stair")

    def site(self):
        site = [it for it in self.items if it["layer"] == "SITE"][0]
        sid = site["id"]
        # fence posts every 20 ft
        for x in [0.3] + list(range(20, 2420, 20)) + [2419.7]:
            for y in (0.25, 1919.75):
                if y > 1 and 1462 < x < 1508:                  # north gate
                    continue
                self.box(sid, "SITE", x - .2, x + .2, y - .2, y + .2, 0, 8.5, "steel")
        for y in [0.3] + list(range(20, 1920, 20)) + [1919.7]:
            for x in (0.25, 2419.75):
                if x < 1 and 270 <= y <= 300:
                    continue
                self.box(sid, "SITE", x - .2, x + .2, y - .2, y + .2, 0, 8.5, "steel")
        # area lighting poles along the access road, ring road and spine roads
        poles = [(x, 267) for x in range(120, 2400, 160)] + [(x, 933) for x in range(420, 1480, 160)] + \
                [(367, y) for y in range(340, 1660, 160)] + [(1457, y) for y in range(340, 1400, 160)] + \
                [(x, 1403) for x in range(420, 2400, 160)]
        for (x, y) in poles:
            self.rod(sid, "SITE", (x, y, 0), (x, y, 40), .45, "steel", r2=.25, seg=8)
            self.rod(sid, "SITE", (x, y, 39), (x + 4, y, 40.5), .15, "steel", seg=4)
            self.box(sid, "SITE", x + 3.2, x + 5.4, y - .7, y + .7, 39.6, 40.4, "lamp")
