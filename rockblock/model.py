"""ER-RB Rev 00: generic RockBlock campus module, parametric.

Unit (500 kW) -> Block RB-nnn (5 units + GCB + step-up) -> Group GRP-nn (blocks_per_group on one 35 kV loop to one
switchgear breaker) -> Lineup SWG-x (groups_per_lineup group breakers, ~75-80 MW, ties to the neighbours, a feeder to the
data center) -> Campus (N lineups along the fence nearest the data center).

Coordinates: X east, Y north, Z up (EL), true feet (TRUE_SCALE = 1). Origin at the SW corner of the site.
Every block is the same template placed at (bx, by, s): world = (bx + x, by + s * y); s = -1 mirrors a north-row block
so its transformer / loop side faces the group road. Circuits are polylines in world feet: horizontal runs at trench
depth, vertical risers into the equipment. Nothing here is engineered."""
import math

import basis as BS

TRUE_SCALE = 1
U_PITCH = BS.v("unit_pitch")
B_PITCH = BS.v("block_pitch")
GL, GW, GH = BS.v("genset_lwh")
ROW_D = 40.0                     # block depth, road side at local y = 40
ROAD = BS.v("road_w")
GROUP_W = 4 * B_PITCH            # 320
GROUP_H = 2 * ROW_D + ROAD       # 110
GAP = BS.v("group_gap")
X0 = 420.0                       # west edge of the generation area (ops, warehouse, pond, gas west of it)
Y0 = 120.0
DL, DM = BS.v("depth_lv"), BS.v("depth_mv")


# ---------------------------------------------------------------- block template (local, S-row orientation) -------
def unit_x(k):
    return 4.0 + U_PITCH * k


UY0, UY1 = 16.0, 16.0 + GL       # unit enclosure (local y), terminal end north (road side)
GCB_BOX = (50.0, 60.0, 29.0, 33.0, .5, 7.5)
XF_BOX = (64.0, 73.0, 26.0, 35.0, .5, 7.0)
HV = (68.5, 35.0)                # transformer HV entry (bottom of the HV cabinet), loop riser
LANE_OWN, LANE_PASS = 37.6, 38.8  # loop corridor lanes (local y), own group / passing group
STACK = BS.v("stack_el")


def block_template():
    """Parts and items of one block in local coordinates. parts: (kind, colour, geom); items: dicts with role."""
    P, I = [], []

    def b(c, x0, x1, y0, y1, z0, z1):
        P.append(("b", c, (x0, x1, y0, y1, z0, z1)))

    def vc(c, x, y, r, z0, z1):
        P.append(("v", c, (x, y, r, z0, z1)))

    def hc(c, a, bb, r):
        P.append(("h", c, (a, bb, r)))

    for k in range(5):
        p0 = len(P)
        x0 = unit_x(k)
        x1 = x0 + GW
        xc = (x0 + x1) / 2
        b("steel_dark", x0 - .1, x1 + .1, UY0 - .2, UY1 + .2, 0, .6)               # base frame
        b("encl", x0, x1, UY0, UY1, .6, GH)                                      # ERT500-class enclosure
        for j in range(5):                                                       # radiator discharge grille (south)
            b("louvre", x0 + .5, x1 - .5, UY0 - .12, UY0, 1.4 + j * 1.35, 2.1 + j * 1.35)
        for j in range(4):                                                       # intake louvres (north, upper)
            b("louvre", x0 + .5, x1 - .5, UY1, UY1 + .1, 6.0 + j * .65, 6.4 + j * .65)
        b("seam", x0 + 3.98, x0 + 4.02, UY1, UY1 + .06, 1.0, 5.2)                # door split, road end
        b("panel", xc + .6, xc + 3.2, UY1, UY1 + .45, 1.6, 4.8)                  # generator terminal box (road end)
        b("steel", xc - 1.0, xc + 1.0, UY0 + 2.0, UY0 + 7.5, GH, GH + .3)        # silencer saddles
        hc("steel", (xc, UY0 + 1.8, GH + 1.2), (xc, UY0 + 7.6, GH + 1.2), .9)     # roof silencer
        vc("stack", xc, UY0 + 3.2, .42, GH + 2.0, STACK)                          # stack (EL 25)
        vc("steel", xc, UY0 + 3.2, .6, STACK, STACK + .15)                       # rain cap
        I.append(dict(role="unit", k=k + 1, fp=(x0 - .1, x1 + .1, UY0 - .2, UY1 + .45), z=(0, STACK + .15),
                      parts=(p0, len(P))))
    p0 = len(P)
    b("concrete", 49.0, 61.0, 27.0, 35.0, 0, .5)                                 # GCB pad
    b("gcb", *GCB_BOX)
    for xd in (52.5, 55.0, 57.5):
        b("seam", xd, xd + .08, 33.0, 33.06, 1.0, 7.1)
        b("steel_dark", xd - .5, xd - .3, 33.0, 33.12, 3.8, 4.4)
    b("gcb", 49.8, 60.2, 28.8, 33.2, 7.5, 7.8)                                   # rain hood
    I.append(dict(role="gcb", fp=(49.0, 61.0, 27.0, 35.0), z=(0, 7.8), parts=(p0, len(P))))
    p0 = len(P)
    b("concrete", 62.0, 75.0, 24.0, 37.0, 0, .5)                                 # transformer pad
    b("xfmr", *XF_BOX)
    b("xfmr", 65.0, 72.0, 33.0, 36.2, .5, 5.8)                                   # HV termination cabinet (loop side)
    for j in range(5):                                                           # radiators (east)
        b("radiator", 73.0, 74.4, 27.2 + j * 1.6, 27.9 + j * 1.6, 1.2, 6.2)
    for x in (66.5, 68.5, 70.5):
        vc("insul", x, 29.5, .25, 7.0, 7.9)
    I.append(dict(role="xfmr", fp=(62.0, 75.0, 24.0, 37.0), z=(0, 7.9), parts=(p0, len(P))))
    return P, I


TEMPLATE = block_template()


def place(bx, by, s):
    return lambda x, y: (bx + x, by + s * y)


# ---------------------------------------------------------------- campus layout ---------------------------------
def layout(mw=None, n_blocks=None, blocks_per_group=None, groups_per_lineup=None):
    bpg = blocks_per_group or BS.v("blocks_per_group")
    gpl = groups_per_lineup or BS.v("groups_per_lineup")
    blk_mw = BS.v("unit_kw") * BS.v("units_per_block") / 1000.0
    nb = n_blocks or int(math.ceil(mw / blk_mw))
    ng = int(math.ceil(nb / bpg))
    nl = int(math.ceil(ng / gpl))
    band_h = 2 * (GROUP_H + GAP)
    blocks, groups, lineups = [], [], []
    bi = 0
    for li in range(nl):
        band_y = Y0 + li * band_h
        L = dict(id=li, tag="SWG-" + _letters(li), band_y=band_y, groups=[])
        lineups.append(L)
        for j in range(gpl):
            gi = li * gpl + j
            if gi >= ng:
                break
            c, r = (1, 0) if j == 0 else (0, 0) if j == 1 else (1, 1) if j == 2 else (0, 1)
            gx = X0 + c * (GROUP_W + GAP)
            gy = band_y + r * (GROUP_H + GAP)
            n_here = min(bpg, nb - bi)
            G = dict(id=gi, tag=f"GRP-{gi + 1:02d}", lineup=li, j=j, c=c, r=r, gx=gx, gy=gy, blocks=[])
            groups.append(G)
            L["groups"].append(gi)
            n_s = min(4, n_here)                       # S row first, then N row (both west -> east)
            for q in range(n_here):
                row = 0 if q < n_s else 1
                i = q if row == 0 else q - n_s
                bx = gx + i * B_PITCH
                by, s = (gy, 1) if row == 0 else (gy + GROUP_H, -1)
                blocks.append(dict(id=bi, n=bi + 1, tag=f"RB-{bi + 1:03d}", group=gi, row=row, i=i, bx=bx, by=by, s=s))
                G["blocks"].append(bi)
                bi += 1
    x_gen_e = X0 + 2 * GROUP_W + GAP                       # east edge of the generation area
    site = dict(x_tr=x_gen_e + 10.0, swg_x0=x_gen_e + 62.0, fence_e=x_gen_e + 132.0, own_x=x_gen_e + 180.0,
                dc_x0=x_gen_e + 260.0, y_n=Y0 + nl * band_h + 40.0)
    for L in lineups:
        L["sy0"] = L["band_y"] + band_h / 2 - 32.0 - GAP / 2
    return dict(params=dict(mw=round(nb * blk_mw, 1), n_blocks=nb, blocks_per_group=bpg, groups_per_lineup=gpl,
                            n_groups=ng, n_lineups=nl, n_units=nb * 5),
                blocks=blocks, groups=groups, lineups=lineups, site=site)


def _letters(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


# switchgear breaker slots along the west face of the e-house, north -> south (local y from sy0, 8 ft sections)
SLOTS = ["TIE-N", "G1", "G2", "FDR", "G3", "G4", "SPARE", "TIE-S"]


def slot_y(L, name):
    return L["sy0"] + 64.0 - 4.0 - 8.0 * SLOTS.index(name)


# ---------------------------------------------------------------- circuits ---------------------------------------
def _len(pts):
    h = v_ = 0.0
    for a, b in zip(pts, pts[1:]):
        h += math.hypot(b[0] - a[0], b[1] - a[1])
        v_ += abs(b[2] - a[2])
    return h, v_


def circuits(lay):
    C = []
    site = lay["site"]

    def add(layer, tag, frm, to, pts, runs, cond, constr, basis="MEASURED", group=None, block=None, kind=None, mv=False):
        h, vv = _len(pts)
        C.append(dict(layer=layer, tag=tag, frm=frm, to=to, pts=[tuple(round(c, 2) for c in p) for p in pts],
                      routed=round(h, 1), risers=round(vv, 1), runs=runs, cond=cond, constr=constr, basis=basis,
                      group=group, block=block, kind=kind or layer, mv=mv))

    L1C = "600 V 1/C XHHW-2 / TC-ER, Cu/Al, size TV"
    L2C = "600 V 1/C XHHW-2 (or bus duct, TV)"
    MVC = "35 kV 1/C Al 750 kcmil, EPR / XLPE 133 %, concentric neutral (MV-105 family)"
    for bk in lay["blocks"]:
        T = place(bk["bx"], bk["by"], bk["s"])
        n = bk["n"]
        gcb_x = lambda k: 51.5 + 1.75 * k
        for k in range(5):
            xc = unit_x(k) + GW / 2
            ly = 27.9 + .3 * k
            xe = gcb_x(k)
            xt = xc + 1.9
            loc = [(xt, UY1 + .45, 2.0), (xt, UY1 + .45, -DL), (xt, ly, -DL), (xe, ly, -DL), (xe, 30.4, -DL), (xe, 30.4, .5)]
            pts = [(*T(x, y), z) for x, y, z in loc]
            add("L1", f"L1-{n:03d}-{k + 1}", f"G-{n:03d}-{k + 1}", f"GCB-{n:03d}", pts, BS.v("l1_runs"), 4, L1C,
                group=bk["group"], block=n)
            loc7 = [(xc - 1.2, UY1, 4.0), (xc - 1.2, UY1, -DL + .4), (xc - 1.2, ly + .15, -DL + .4), (xe + .4, ly + .15, -DL + .4),
                    (xe + .4, 30.0, -DL + .4), (xe + .4, 30.0, 1.0)]
            add("L7", f"L7-{n:03d}-{k + 1}", f"G-{n:03d}-{k + 1}", f"GCB-{n:03d}", [(*T(x, y), z) for x, y, z in loc7],
                2, 1, "12/C #14 TC-ER control + Cat6A, per unit", group=bk["group"], block=n, kind="L7u")
        loc = [(59.5, 31.0, .5), (59.5, 31.0, -DL), (64.6, 31.0, -DL), (64.6, 31.0, .5)]
        add("L2", f"L2-{n:03d}", f"GCB-{n:03d}", f"XFMR-{n:03d}", [(*T(x, y), z) for x, y, z in loc], BS.v("l2_runs"), 4,
            L2C, group=bk["group"], block=n)
        ring = [(1, 13), (76.5, 13), (76.5, 37.0), (1, 37.0), (1, 13)]
        pts = [(*T(x, y), -2.5) for x, y in ring]
        add("L6", f"L6-{n:03d}", f"RB-{n:03d} grid", "ring", pts, 1, 1, "4/0 bare Cu, ground ring", group=bk["group"],
            block=n, kind="L6r")
        taps = [(unit_x(k), UY0 - .2) for k in range(5)] + [(49.0, 27.0), (62.0, 24.0), (75.0, 37.0)]
        for q, (x, y) in enumerate(taps):
            yr = 13 if y < 25 else 37.0
            xr = x
            pts = [(*T(xr, yr), -2.5), (*T(x, y), -2.5), (*T(x, y), .6)]
            add("L6", f"L6-{n:03d}-T{q + 1}", f"RB-{n:03d} ring", ["G-1", "G-2", "G-3", "G-4", "G-5", "GCB", "XFMR",
                                                                 "XFMR"][q], pts, 1, 1, "2/0 bare Cu, tap",
                group=bk["group"], block=n, kind="L6t")
    # ---- 35 kV loops: SWG -> XFMR ... -> XFMR -> SWG, per group --------------------------------------------------
    for G in lay["groups"]:
        L = lay["lineups"][G["lineup"]]
        bl = [lay["blocks"][i] for i in G["blocks"]]
        S = [b for b in bl if b["row"] == 0]
        N = [b for b in bl if b["row"] == 1]
        order = list(reversed(S)) + N
        lane = LANE_OWN if G["c"] == 1 else LANE_PASS
        xt_out = site["x_tr"] + 1.4 * G["j"]
        xt_ret = xt_out + .7
        sw_x = site["swg_x0"]
        gs = "G%d" % (G["j"] + 1)
        sy = slot_y(L, gs)
        sy_r = sy - 1.2                                    # loop return lands in the same section
        hv = lambda b: (b["bx"] + HV[0], b["by"] + b["s"] * HV[1])
        ly = lambda b: b["by"] + b["s"] * lane

        def riser(b, z0=.5):
            x, y = hv(b)
            return [(x, y, z0), (x, y, -DM), (x, ly(b), -DM)]

        segs = []
        # SWG -> first transformer (east end of the S row; or N row if S is empty)
        f = order[0]
        pts = [(sw_x, sy, .5), (sw_x, sy, -DM), (xt_out, sy, -DM), (xt_out, ly(f), -DM), (hv(f)[0], ly(f), -DM),
               (hv(f)[0], hv(f)[1], -DM), (hv(f)[0], hv(f)[1], .5)]
        segs.append((f"{L['tag']} {gs}", f"XFMR-{f['n']:03d}", pts))
        for a, bb in zip(order, order[1:]):
            if a["row"] == bb["row"]:
                pts = riser(a) + [(hv(bb)[0], ly(bb), -DM)] + list(reversed(riser(bb)))[1:]
            else:                                          # S row west end -> N row west end, round the west road
                xw = G["gx"] - GAP / 2 + (.7 if G["c"] == 0 else 0)
                pts = riser(a) + [(xw, ly(a), -DM), (xw, ly(bb), -DM)] + list(reversed(riser(bb)))
            segs.append((f"XFMR-{a['n']:03d}", f"XFMR-{bb['n']:03d}", pts))
        last = order[-1]
        pts = riser(last) + [(xt_ret, ly(last), -DM), (xt_ret, sy_r, -DM), (sw_x, sy_r, -DM), (sw_x, sy_r, .5)]
        segs.append((f"XFMR-{last['n']:03d}", f"{L['tag']} {gs} (loop return)", pts))
        fib = []
        for q, (fr, to, pts) in enumerate(segs):
            add("L3", f"L3-{G['tag'][4:]}-{q + 1:02d}", fr, to, pts, 1, 3, MVC, group=G["id"], mv=True)
            fib += [(x, y + .5, z + .4) for x, y, z in pts]
        add("L7", f"L7-{G['tag']}-FO", f"{G['tag']} block controllers", f"{L['tag']} / SCADA", fib, 1, 1,
            "12-strand SM fibre ring, per group", group=G["id"], kind="L7f")
    # ---- lineup ties (closed ring A-B-...-A), feeders, lineup grounding ------------------------------------------
    LS = lay["lineups"]
    ex = site["swg_x0"] + 16.0
    if len(LS) > 1:
        pairs = [(LS[i], LS[i + 1]) for i in range(len(LS) - 1)]
        if len(LS) > 2:
            pairs.append((LS[-1], LS[0]))
        for q, (a, bb) in enumerate(pairs):
            ring_close = q == len(LS) - 1 and len(LS) > 2
            xl = ex + (14.0 if ring_close else 8.0)
            ya, yb = slot_y(a, "TIE-S" if not ring_close else "TIE-S"), slot_y(bb, "TIE-N")
            if ring_close:
                ya = slot_y(a, "TIE-S") - 1.2
                yb = slot_y(bb, "TIE-N") + 1.2
            pts = [(ex, ya, .5), (ex, ya, -DM), (xl, ya, -DM), (xl, yb, -DM), (ex, yb, -DM), (ex, yb, .5)]
            add("L4", f"L4-{a['tag'][4:]}{bb['tag'][4:]}", a["tag"], bb["tag"], pts, BS.v("feeder_sets"), 3, MVC, mv=True)
    for L in LS:
        y = slot_y(L, "FDR")
        pts = [(ex, y, .5), (ex, y, -DM), (site["dc_x0"], y, -DM), (site["dc_x0"], y, .5)]
        add("L5", f"L5-{L['tag'][4:]}", L["tag"], "Data center MV intake (customer)", pts, BS.v("feeder_sets"), 3, MVC,
            basis="ASSUMED", mv=True)
        x0, x1, y0, y1 = site["swg_x0"] - 4, site["swg_x0"] + 20, L["sy0"] - 4, L["sy0"] + 68
        add("L6", f"L6-{L['tag']}", f"{L['tag']} grid", "ring", [(x0, y0, -2.5), (x1, y0, -2.5), (x1, y1, -2.5),
                                                                  (x0, y1, -2.5), (x0, y0, -2.5)], 1, 1,
            "4/0 bare Cu, lineup ground ring", kind="L6l")
    return C


# ---------------------------------------------------------------- site equipment (absolute) ------------------------
def site_items(lay):
    """Lineup e-houses, data-center ghost, ownership line, fence, roads, ops, warehouse, pond, gas skid, gas lateral."""
    s = lay["site"]
    P, I = [], []

    def item(tag, name, key, st, info, src=""):
        I.append(dict(tag=tag, name=name, key=key, status=st, info=info, src=src, p0=len(P)))

    def done(fp, z):
        I[-1].update(fp=fp, z=z, p1=len(P))

    def b(c, x0, x1, y0, y1, z0, z1, layer="base"):
        P.append(("b", c, (x0, x1, y0, y1, z0, z1), layer))

    def vc(c, x, y, r, z0, z1, layer="base"):
        P.append(("v", c, (x, y, r, z0, z1), layer))

    yN = s["y_n"]
    for L in lay["lineups"]:
        x0, y0 = s["swg_x0"], L["sy0"]
        item(L["tag"], f"{L['tag']}: 35 kV switchgear lineup e-house ({len(L['groups'])} group breakers, ties, feeder)", 5,
             BS.TV, "Group breakers G1-G4 (one per 35 kV loop), tie breakers TIE-N / TIE-S to the neighbouring lineups, "
             "feeder breaker FDR toward the data center (~75 MW). E-house size is a placeholder.", "ER / switchgear data sheet")
        b("concrete", x0 - 3, x0 + 19, y0 - 3, y0 + 67, 0, .6)
        b("ehouse", x0, x0 + 16, y0, y0 + 64, .6, 14.0)
        b("roof", x0 - .4, x0 + 16.4, y0 - .4, y0 + 64.4, 14.0, 14.5)
        for q in range(4):
            b("hvac", x0 + 4, x0 + 12, y0 + 6 + q * 15, y0 + 11 + q * 15, 14.5, 17.0)
        for q, nm in enumerate(SLOTS):
            yy = slot_y(L, nm)
            b("seam", x0 - .06, x0, yy - 3.6, yy + 3.6, 1.2, 12.0)
            b("door" if nm.startswith("G") or nm == "FDR" else "seam", x0 - .1, x0, yy - 3.0, yy + 3.0, 1.4, 9.0)
        b("steel", x0 + 16, x0 + 20, y0 + 28, y0 + 36, 0, 3.6)                # stair landing
        done((x0 - 3, x0 + 20, y0 - 3, y0 + 67), (0, 17))
    y_lo, y_hi = Y0 - 60, yN
    item("DC", "Data center campus (customer), ghosted beyond the ownership line", 6, BS.K,
         "The load. Drawn as a ghost: not modelled. Receives the ~75 MW feeders, one per lineup.", "")
    b("ghost", s["dc_x0"], s["dc_x0"] + 520, y_lo + 40, y_hi - 40, 0, 48, "dc")
    done((s["dc_x0"], s["dc_x0"] + 520, y_lo + 40, y_hi - 40), (0, 48))
    item("OWN", "Ownership line: ER scope / customer scope, TO VERIFY", 7, BS.TV,
         "Where the ~75 MW feeders change hands is not known: ER cable or the customer's. Cliff can answer it in one line.",
         "Cliff Maynas")
    for y in range(int(y_lo), int(y_hi), 24):
        b("own", s["own_x"] - .3, s["own_x"] + .3, y, y + 14, 0, .25)
    for y in (y_lo, y_hi - 4):
        b("own", s["own_x"] - .4, s["own_x"] + .4, y, y + 4, 0, 6.0)
    b("ownwall", s["own_x"] - .1, s["own_x"] + .1, y_lo, y_hi, 0, 12.0)
    done((s["own_x"] - 1, s["own_x"] + 1, y_lo, y_hi), (0, 6))
    item("FENCE", "Site fence (ER site)", 14, BS.WA, "Chain-link, 7 ft.", "")
    fx0, fx1, fy0, fy1 = 20.0, s["fence_e"], Y0 - 70, yN + 10
    for (a0, a1, c0, c1) in ((fx0, fx1, fy0, fy0 + .2), (fx0, fx1, fy1 - .2, fy1), (fx0, fx0 + .2, fy0, fy1), (fx1 - .2, fx1, fy0, fy1)):
        b("fence", a0, a1, c0, c1, 0, 7.0)
    done((fx0, fx1, fy0, fy1), (0, 7))
    item("ROADS", "Access roads", 13, BS.WA, "Group roads between the two rows of each group, perimeter roads between groups.", "")
    for G in lay["groups"]:
        b("road", G["gx"] - GAP + 4, G["gx"] + GROUP_W + 4, G["gy"] + ROW_D + 2, G["gy"] + ROW_D + ROAD - 2, 0, .06)
    for L in lay["lineups"]:
        for r in range(2):
            y = L["band_y"] + r * (GROUP_H + GAP) - GAP + 4
            b("road", X0 - GAP + 4, s["fence_e"] - 8, y, y + GAP - 8, 0, .06)
    b("road", X0 - GAP + 4, X0 - 4, Y0 - 28, yN - 30, 0, .06)
    b("road", s["x_tr"] + 30, s["x_tr"] + 46, Y0 - 28, yN - 30, 0, .06)
    done((X0 - GAP, s["fence_e"], Y0 - 28, yN), (0, .06))
    ox, oy = 60.0, Y0 + 40
    item("OPS", "Operations / maintenance building", 8, BS.K, "Named on the call; size is a placeholder.", "Oct 26 call; El Paso press")
    b("building", ox, ox + 120, oy, oy + 60, 0, 22)
    b("roof", ox - .5, ox + 120.5, oy - .5, oy + 60.5, 22, 22.6)
    for q in range(5):
        b("glass", ox + 8 + q * 22, ox + 22 + q * 22, oy - .1, oy, 4, 12)
    done((ox, ox + 120, oy, oy + 60), (0, 22.6))
    wy = oy + 110
    item("WH", "Warehouse", 9, BS.K, "Named on the call; size is a placeholder.", "Oct 26 call")
    b("building", ox, ox + 160, wy, wy + 90, 0, 30)
    b("roof", ox - .5, ox + 160.5, wy - .5, wy + 90.5, 30, 30.6)
    for q in range(3):
        b("door", ox + 20 + q * 48, ox + 36 + q * 48, wy - .15, wy, 0, 16)
    done((ox, ox + 160, wy, wy + 90), (0, 30.6))
    py = wy + 150
    item("POND", "Water retention", 10, BS.K, "Named on the call; size is a placeholder.", "Oct 26 call")
    b("berm", ox - 10, ox + 230, py - 10, py + 150, 0, 2.5)
    b("water", ox, ox + 220, py, py + 140, 0, 2.55)
    done((ox - 10, ox + 230, py - 10, py + 150), (0, 2.6))
    gy = Y0 - 40
    item("GMS", "Gas metering skid at the lateral", 11, BS.WA, "Metering / regulation where the lateral enters.", "El Paso press / pipeline filing")
    b("concrete", 230, 290, gy - 6, gy + 18, 0, .5)
    for q in range(3):
        P.append(("h", "gaspipe", ((236, gy + 2 + q * 5, 3.0), (284, gy + 2 + q * 5, 3.0), .7), "base"))
        for x in (246, 260, 274):
            vc("valve", x, gy + 2 + q * 5, 1.1, 2.2, 3.8)
    b("panel", 232, 240, gy + 14, gy + 17, .5, 7.0)
    done((230, 290, gy - 6, gy + 18), (0, 7))
    item("GAS", "Gas lateral and headers (context, not a cable layer)", 12, BS.WA,
         "Lateral in from the west to the metering skid; buried headers along each group road to the blocks.", "")
    P.append(("h", "gaspipe", ((0, gy + 7, -5), (230, gy + 7, -5), .9), "gas"))
    xh = X0 - GAP / 2
    P.append(("h", "gaspipe", ((290, gy + 7, -5), (xh, gy + 7, -5), .8), "gas"))
    P.append(("h", "gaspipe", ((xh, gy + 7, -5), (xh, yN - 50, -5), .8), "gas"))
    for G in lay["groups"]:
        y = G["gy"] + ROW_D + ROAD / 2
        x1 = G["gx"] + GROUP_W - 20
        if G["c"] == 1:
            P.append(("h", "gaspipe", ((xh, y, -5), (x1, y, -5), .5), "gas"))
        for bi in G["blocks"]:
            bk = lay["blocks"][bi]
            x = bk["bx"] + 46
            P.append(("h", "gaspipe", ((x, y, -5), (x, bk["by"] + bk["s"] * 14, -5), .3), "gas"))
    done((0, xh + 2, gy, yN), (-5, -4))
    return P, I


def build(mw=250, **kw):
    lay = layout(mw=mw, **kw)
    return dict(layout=lay, circuits=circuits(lay), site=site_items(lay))


if __name__ == "__main__":
    for mw in (250, 500, 1000):
        m = build(mw)
        p = m["layout"]["params"]
        print(mw, p, len(m["circuits"]), "circuits")
