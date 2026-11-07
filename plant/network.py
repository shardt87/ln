"""Cable route network shared by the model build and the cable schedule.

Graph: every electrical route (tray, duct bank, trench, buried cable) as a graph in feet; route vertices that
lie on another route's segment become tees, stacked nodes within 4 ft join as risers. Pieces that are still
separate are bridged by short "conduit links" (Graph.links); build_model.py lays those as real buried conduit
(ties()) so the schedule's network and the 3D model agree.
"""
import heapq
import math
from collections import defaultdict


def centre(it):
    f = it["fp"]
    return ((f[0] + f[1]) / 2, (f[2] + f[3]) / 2)


# ------------------------------------------------------------------------------------------------ route graph
ELEC = {"mv_tray": "Tray", "lv_tray": "Tray", "control_tray": "Tray", "duct_bank": "Duct bank",
        "mvlv_cable": "Duct bank", "hv_cable": "HV duct bank", "cable_trench": "Trench"}


class Graph:
    def __init__(self, routes):
        self.adj = defaultdict(list)
        self.kind = {}
        segs = []
        for r in routes:
            if r["type"] not in ELEC:
                continue
            z = r["z"]
            kind = "Surface" if r.get("surface") else ELEC[r["type"]]
            P = [(round(p[0], 1), round(p[1], 1), z) for p in r["points"]]
            for a, b in zip(P, P[1:]):
                segs.append((a, b, kind))
        # split each segment at every route vertex lying on it (T-junctions), then join coincident / stacked nodes
        verts = {s[0] for s in segs} | {s[1] for s in segs}
        grid = defaultdict(list)
        for v in verts:
            grid[(int(v[0] // 20), int(v[1] // 20))].append(v)

        def near(x, y, rad):
            gx, gy = int(x // 20), int(y // 20)
            for i in range(gx - 1, gx + 2):
                for j in range(gy - 1, gy + 2):
                    for v in grid[(i, j)]:
                        if abs(v[0] - x) <= rad and abs(v[1] - y) <= rad:
                            yield v
        for a, b, kind in segs:
            horiz = abs(a[1] - b[1]) < abs(a[0] - b[0])
            lo, hi = (min(a[0], b[0]), max(a[0], b[0])) if horiz else (min(a[1], b[1]), max(a[1], b[1]))
            pts = [a, b]
            n = max(1, int((hi - lo) // 20))
            for k in range(n + 1):                      # sample along the segment for vertices on it
                t = k / n
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                for v in near(x, y, 12):
                    if (lo - .5 <= (v[0] if horiz else v[1]) <= hi + .5 and
                            abs((v[1] - a[1]) if horiz else (v[0] - a[0])) <= 3):
                        q = (v[0], a[1], a[2]) if horiz else (a[0], v[1], a[2])
                        pts.append(q)
            pts = sorted(set(pts), key=lambda p: (p[0], p[1]) if horiz else (p[1], p[0]))
            for p, q in zip(pts, pts[1:]):
                d = math.dist(p[:2], q[:2])
                self.adj[p].append((q, d))
                self.adj[q].append((p, d))
                self.kind[(p, q)] = self.kind[(q, p)] = kind
        nodes = list(self.adj)
        ng = defaultdict(list)
        for v in nodes:
            ng[(int(v[0] // 6), int(v[1] // 6))].append(v)
        for v in nodes:                                  # vertical / stacked transitions (risers, tray to bank)
            gx, gy = int(v[0] // 6), int(v[1] // 6)
            for i in range(gx - 1, gx + 2):
                for j in range(gy - 1, gy + 2):
                    for w in ng[(i, j)]:
                        if w != v and math.dist(v[:2], w[:2]) <= 4:
                            d = math.dist(v[:2], w[:2]) + abs(v[2] - w[2])
                            self.adj[v].append((w, d))
                            self.kind[(v, w)] = "Riser"
        # bridge separate pieces of the network (tray ends to a nearby bank or tray) with short conduit links
        comp = {}
        for v in nodes:
            if v in comp:
                continue
            stack, comp[v] = [v], v
            while stack:
                u = stack.pop()
                for w, _ in self.adj[u]:
                    if w not in comp:
                        comp[w] = v
                        stack.append(w)
        bg = defaultdict(list)
        for v in nodes:
            bg[(int(v[0] // 110), int(v[1] // 110))].append(v)
        best = {}
        for v in nodes:
            gx, gy = int(v[0] // 110), int(v[1] // 110)
            for i in range(gx - 1, gx + 2):
                for j in range(gy - 1, gy + 2):
                    for w in bg[(i, j)]:
                        if comp[w] != comp[v]:
                            d = abs(v[0] - w[0]) + abs(v[1] - w[1])
                            key = tuple(sorted((comp[v], comp[w])))
                            if d <= 110 and (key not in best or d < best[key][0]):
                                best[key] = (d, v, w)
        for d, v, w in best.values():
            c = d * 1.2 + abs(v[2] - w[2])
            self.adj[v].append((w, c))
            self.adj[w].append((v, c))
            self.kind[(v, w)] = self.kind[(w, v)] = "Conduit link"
        self.n_links = len(best)
        self.bridges = sorted(best.values())
        self.comp = comp
        self.nodes = nodes
        ag = defaultdict(list)
        for v in nodes:
            ag[(int(v[0] // 50), int(v[1] // 50))].append(v)
        self.ag = ag

    def access(self, it, k=4):
        """The k network nodes nearest to an item's footprint, with the drop length (horizontal + vertical)."""
        f = it["fp"]
        cx, cy = centre(it)
        cand = []
        for rad in (1, 2, 4, 8, 16):
            gx, gy = int(cx // 50), int(cy // 50)
            cand = [v for i in range(gx - rad, gx + rad + 1) for j in range(gy - rad, gy + rad + 1) for v in self.ag[(i, j)]]
            if len(cand) >= k:
                break
        out = []
        for v in cand:
            dx = max(f[0] - v[0], 0, v[0] - f[1])
            dy = max(f[2] - v[1], 0, v[1] - f[3])
            out.append((dx + dy + abs(v[2] - 4) + 10, v))
        return sorted(out)[:k]

    def dijkstra(self, starts):
        dist = {}
        pq = [(d, v) for d, v in starts]
        heapq.heapify(pq)
        prev = {}
        while pq:
            d, v = heapq.heappop(pq)
            if v in dist:
                continue
            dist[v] = d
            for w, c in self.adj[v]:
                if w not in dist:
                    nd = d + c
                    heapq.heappush(pq, (nd, w))
                    prev.setdefault(w, (nd, v))
                    if nd < prev[w][0]:
                        prev[w] = (nd, v)
        return dist, prev


def ties(routes, detour=3.0, slack=100.0):
    """Short links that join the separate pieces of the network: first the fewest that connect everything
    (shortest first), then any other link whose ends are more than detour x its length + slack apart along
    the network (a real plant would lay that conduit rather than send cable the long way round).
    Returns [(node a, node b)] with nodes as (x, y, z); build_model.py lays each as buried conduit."""
    g = Graph(routes)
    adj = defaultdict(list)
    for v, lst in g.adj.items():
        for w, c in lst:
            if g.kind.get((v, w)) != "Conduit link":
                adj[v].append((w, c))
    up = {}

    def root(c):
        while up.get(c, c) != c:
            c = up[c]
        return c

    def link(v, w, d):
        out.append((v, w))
        c = d * 1.2 + abs(v[2] - w[2])
        adj[v].append((w, c))
        adj[w].append((v, c))

    def far(v, w, cut):
        dist = {v: 0.0}
        pq = [(0.0, v)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == w:
                return False
            if d > dist.get(u, 1e18) or d > cut:
                continue
            for x, c in adj[u]:
                if d + c < dist.get(x, 1e18):
                    dist[x] = d + c
                    heapq.heappush(pq, (d + c, x))
        return True
    out = []
    rest = []
    for d, v, w in g.bridges:
        a, b = root(g.comp[v]), root(g.comp[w])
        if a != b:
            up[a] = b
            link(v, w, d)
        else:
            rest.append((d, v, w))
    for d, v, w in rest:
        if far(v, w, detour * d * 1.2 + slack):
            link(v, w, d)
    return out
