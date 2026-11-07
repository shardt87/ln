"""Turbine hall south electrical gallery at LOD 3 (owner, Oct 22 audit: "model it better, it's too rough"). The
gallery equipment of each generator (static exciter EXC, excitation transformer ET, surge-protection / VT cubicle SPC,
neutral grounding cubicle NGT, static starter SFC with its isolation transformer, generator breaker GCB) stood as
cabinet boxes with a few door panels, unlit, with none of the power between them drawn. Rebuilt with the
switchgear-room fronts (swgr_rooms.py), all typical, not engineered:
- EXC: louvred thyristor-bridge sections with keypads and roof fans; SPC and NGT: protection-panel fronts; ET:
  louvred dry-type transformer enclosure; SFC: drive sections on each LCI cabinet, the isolation transformer louvred;
  GCB: operating-mechanism cabinet, nameplate and the bus flanges each side;
- the cables into the cubicle tops from the existing trays: the ET secondary down from the EL 10.5 tray into the
  exciter, the DC field cables rising from the exciter to the EL 30 field tray (which gt_wiring.py now meets at the
  generator collector); the static starter's output already rises to SDS-1 (mv_terminations.py);
- the gallery lit: LED high-bays in two rows at EL 30 on hangers to the gallery roof steel, placed only where clear.
Runs late (after the IPB and trays are rendered and the SDS-1 / field-lead passes)."""
import fuel
from fuel import box, rod, find, on

import swgr_rooms as S

DX = (0, 160, 320)                               # GT1-3 offsets; the ST set sits at its own x


def strip_fronts(it):
    """Drop the old door / louvre panels of a cubicle item (the swgr fronts replace them)."""
    fuel.G["parts"][:] = [p for p in fuel.G["parts"] if not (p["item"] == it["id"] and p["color"] in ("door", "louvre"))]


def body(it, colors=("cabinet", "xfmr")):
    bs = [p for p in fuel.G["parts"] if p["item"] == it["id"] and p["kind"] == "box" and p["color"] in colors]
    return bs


def label(F, u, z, text, w=3.0):
    import showcase
    c = F.p(u, z, .12)
    showcase.decal(c, F.n(), w, .45, [(text, .6, True, "#111111")], bg="#ffffff")


def tray(pts, z, w, cables):
    """Short ladder tray along an orthogonal polyline at EL z with its cables."""
    n = 0
    for a, b in zip(pts, pts[1:]):
        alongx = a[1] == b[1]
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for s in (-1, 1):
            if alongx:
                box(x0, x1, a[1] + s * w / 2 - .06, a[1] + s * w / 2 + .06, z - .3, z + .12, "pipe")
            else:
                box(a[0] + s * w / 2 - .06, a[0] + s * w / 2 + .06, y0, y1, z - .3, z + .12, "pipe")
        L = (x1 - x0) + (y1 - y0)
        for k in range(int(L / 1.5) + 1):
            t = min(1.0, k * 1.5 / max(L, .1))
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if alongx:
                box(px - .05, px + .05, a[1] - w / 2, a[1] + w / 2, z - .28, z - .22, "pipe")
            else:
                box(a[0] - w / 2, a[0] + w / 2, py - .05, py + .05, z - .28, z - .22, "pipe")
        for j, (c, r) in enumerate(cables):
            off = -w / 2 + .18 + j * (w - .36) / max(1, len(cables) - 1)
            pa = (a[0], a[1] + off) if alongx else (a[0] + off, a[1])
            pb = (b[0], b[1] + off) if alongx else (b[0] + off, b[1])
            rod((pa[0], pa[1], z - .22 + r), (pb[0], pb[1], z - .22 + r), r, c, seg=6)
        n += 6
    return n


def unit(tag_sfx, dx, st=False):
    n = 0
    exc = find(f"EXC-{tag_sfx}:")
    strip_fronts(exc)
    cab = body(exc, ("cabinet",))[0]
    (x0, y0, z0), (x1, y1, z1) = cab["min"], cab["max"]
    on(exc)
    fuel.D = True
    F = S.Front((x0, x1, y0, y1), "-y")
    S.drive(F, z0, z1, "cab_in", w=2.4)
    label(F, F.L / 2, z1 - .25, f"EXC-{tag_sfx}  STATIC EXCITER", w=4.2)
    n += 30
    fuel.D = False
    for pre in ("SPC", "NGT"):
        try:
            it = find(f"{pre}-{tag_sfx}:")
        except StopIteration:
            continue
        strip_fronts(it)
        b = body(it, ("cabinet",))[0]
        (a0, b0, c0), (a1, b1, c1) = b["min"], b["max"]
        on(it)
        fuel.D = True
        F = S.Front((a0, a1, b0, b1), "-y" if pre == "SPC" else "+y")
        S.pc_panel(F, c0, c1, "cab_in")
        label(F, F.L / 2, c1 - .25, f"{pre}-{tag_sfx}", w=2.0)
        fuel.D = False
        n += 12
    if not st:
        et = find(f"ET-{tag_sfx}:")
        strip_fronts(et)
        b = body(et, ("xfmr",))[0]
        (a0, b0, c0), (a1, b1, c1) = b["min"], b["max"]
        on(et)
        fuel.D = True
        S.dry_xfmr((a0, a1, b0, b1), c0, c1)
        fuel.D = False
        sfc = find(f"SFC-{tag_sfx}:")
        strip_fronts(sfc)
        on(sfc)
        fuel.D = True
        for b in body(sfc, ("cabinet",)):
            (a0, b0, c0), (a1, b1, c1) = b["min"], b["max"]
            F = S.Front((a0, a1, b0, b1), "-y")
            S.drive(F, c0, c1, "cab_in", w=2.5)
            n += 10
        for b in body(sfc, ("xfmr",)):
            (a0, b0, c0), (a1, b1, c1) = b["min"], b["max"]
            S.dry_xfmr((a0, a1, b0, b1), c0, c1)
        cabs = body(sfc, ("cabinet",))
        if cabs:
            (a0, b0, c0), (a1, b1, c1) = cabs[0]["min"], cabs[0]["max"]
            label(S.Front((a0, a1, b0, b1), "-y"), 1.6, c1 - .25, f"SFC-{tag_sfx}  LCI", w=3.0)
        fuel.D = False
    # cables from the existing trays into the cubicle tops (tray model: ET -> EXC on the EL 10.5 LV tray ending at
    # x 642, y 397; the exciter's field run leaves on the EL 30 tray starting at x 648, y 399 for the GTs)
    on(exc)
    fuel.D = True
    if not st:
        # (the ET secondary already drops into the exciter top from the tray model's EL 10.5 tray at x 642)
        for (dxl, c) in ((-.45, "cable_tc"), (-.15, "cable_tc"), (.15, "red"), (.45, "red")):
            rod((x0 + 8.0 + dxl, 399.0, z1), (x0 + 8.0 + dxl, 399.0, 29.35), .1, c, seg=6)
        box(x0 + 7.2, x0 + 8.8, 398.6, 399.4, z1, z1 + .25, "steel")                     # gland plate
    fuel.D = False
    return n + 8


def gcbs():
    n = 0
    for t in ("1", "2", "3", "ST"):
        g = find(f"GCB-{t}")
        b = body(g, ("xfmr",))
        if not b:
            continue
        (x0, y0, z0), (x1, y1, z1) = b[0]["min"], b[0]["max"]
        on(g)
        fuel.D = True
        F = S.Front((x0, x1, y0, y1), "+x")
        F.b(2.0, F.L - 2.0, z0 + 1.0, z0 + 6.0, 0, 1.4, "cab_in")                  # operating-mechanism cabinet
        F.b(2.3, F.L - 2.3, z0 + 1.3, z0 + 5.7, 1.4, 1.45, "steel_dark")
        S.lamps(F, 2.6, z0 + 5.0, ("led_r", "led_g", "led_a"))
        S.handle(F, F.L - 2.6, z0 + 2.5, z0 + 3.6)
        label(F, F.L / 2, z0 + 6.5, f"GCB-{t}  GENERATOR BREAKER", w=4.0)
        for yf in (y0 + .2, y1 - .2):                                              # bus flanges each side
            box(x0 - .3, x1 + .3, yf - .15, yf + .15, z0 + 1.5, z1 - 1.5, "steel_dark")
        fuel.D = False
        n += 10
    return n


def lighting():
    """LED high-bays in two rows at EL 30, hung to EL 38 (under the EL 42 trays), only where the space is clear."""
    lo, hi = (480.0, 370.0, 26.0), (1100.0, 404.0, 39.0)
    obs = []
    for p in fuel.G["parts"]:
        if p["kind"] == "box":
            a, b = p["min"], p["max"]
        elif p["kind"] == "rod":
            r = max(p["r"], p.get("r2", p["r"]))
            a = [min(p["a"][i], p["b"][i]) - r for i in range(3)]
            b = [max(p["a"][i], p["b"][i]) + r for i in range(3)]
        else:
            continue
        if all(a[i] < hi[i] and b[i] > lo[i] for i in range(3)):
            obs.append((a, b))
    it = find("Turbine hall interior electrical")
    on(it)
    fuel.D = True
    n = 0
    for yr in (377.0, 397.0):
        x = 500.0
        while x < 1085:
            ok = not any(a[0] < x + 2.6 and b[0] > x - 2.6 and a[1] < yr + 1.2 and b[1] > yr - 1.2 and a[2] < 38.2
                         and b[2] > 29.4 for a, b in obs)
            if ok:
                S.fixture(x, yr, 30.0, along="x", roof=38.0)
                n += 4
            x += 22.0
    fuel.D = False
    return n


def build():
    n = 0
    for k, dx in enumerate(DX):
        n += unit(str(k + 1), dx)
    n += unit("ST", 0, st=True)
    n += gcbs()
    n += lighting()
    return n
