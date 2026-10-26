"""SK-2300 sheet set for ER-RB Rev 00: letter landscape, 300 dpi, a stated ratio scale on every sheet with a graphic bar
drawn at the same scale, numbered key bubbles against the fixed equipment key, the credit and the stamp on every sheet.

SK-2301 campus isometric                       SK-2304 35 kV loop and lineup topology
SK-2302 block plan + elevation, dimensions     SK-2305 four-view X-ray
SK-2303 one block electrical (L1 / L2)         SK-2306 per-block takeoff, campus roll-up, verification register"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon, Rectangle, FancyBboxPatch

import basis as BS
import model as M
import takeoff as TO

for f in os.listdir(os.path.join(HERE, "fonts")):
    font_manager.fontManager.addfont(os.path.join(HERE, "fonts", f))
COND, BODY, MONO = "Barlow Condensed", "Barlow", "DejaVu Sans Mono"
BG, PANEL, INK, INK2, RULE, CU, CU2 = "#0f1113", "#171a1d", "#e7e4de", "#9aa3a8", "#2c3238", "#d0743a", "#e8955c"
STC = {BS.K: INK, BS.WA: "#e3a21a", BS.TV: "#ef6a5a"}
STS = {BS.K: "K", BS.WA: "WA", BS.TV: "TV"}
LC = {k: c for k, _, c, _, _ in BS.LAYERS}
LDASH = {k: d for k, _, _, _, d in BS.LAYERS}
FILL = dict(encl="#c9cdcf", gcb="#a7afb4", xfmr="#76847a", ehouse="#b7bcc0", building="#8f969c", road="#24272a",
            water="#2c5873", berm="#3d4634", concrete="#55585a", ghost="#5a6f86", steel="#8c9399", roof="#596066",
            hvac="#8c9399", radiator="#66726a", panel="#8d949a", stack="#b8bec2")
W, H = 11.0, 8.5
DATE = "Oct 26, 2026"
OUT = os.path.join(os.path.dirname(HERE), "out")


def fig_frame(num, title, scale_txt, keys, notes=()):
    fig = plt.figure(figsize=(W, H), dpi=300)
    fig.patch.set_facecolor(BG)
    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_xlim(0, W)
    bg.set_ylim(0, H)
    bg.axis("off")
    bg.add_patch(Rectangle((.25, .25), W - .5, H - .5, fill=False, ec=RULE, lw=1.0))
    bg.add_patch(Rectangle((8.35, .25), 0, H - .5, fill=False, ec=RULE, lw=.8))
    # header strip (right column)
    bg.text(8.5, 8.0, "ER-RB  ·  ROCKBLOCK CAMPUS MODULE", color=CU2, fontsize=8.5, family=COND, weight="bold")
    bg.text(8.5, 7.7, title.upper(), color=INK, fontsize=13, family=COND, weight="bold", va="top", wrap=True)
    # key panel
    y = 6.75
    bg.text(8.5, y, "EQUIPMENT KEY", color=INK2, fontsize=7, family=COND, weight="bold")
    y -= .2
    for n, t in BS.KEY:
        if n not in keys:
            continue
        bubble(bg, 8.6, y + .03, n, r=.075, fs=5.6)
        bg.text(8.75, y, t, color=INK, fontsize=6.4, family=BODY, va="center")
        y -= .19
    if notes:
        y -= .1
        bg.text(8.5, y, "NOTES", color=INK2, fontsize=7, family=COND, weight="bold")
        y -= .18
        for t in notes:
            for line in wrap(t, 52):
                bg.text(8.5, y, line, color=INK, fontsize=6.0, family=BODY, va="top")
                y -= .14
            y -= .05
    # status legend
    yl = 2.38
    bg.text(8.5, yl, "STATUS", color=INK2, fontsize=7, family=COND, weight="bold")
    for i, (s, lab) in enumerate(((BS.K, "KNOWN"), (BS.WA, "WORKING ASSUMPTION"), (BS.TV, "TO VERIFY"))):
        xx = 8.5 + [0, .55, 1.62][i]
        bg.add_patch(FancyBboxPatch((xx, yl - .27), [.45, .98, .6][i], .16, boxstyle="square,pad=0", fill=False,
                                    ec=STC[s], lw=.8, ls=["-", "--", ":"][i]))
        bg.text(xx + [.45, .98, .6][i] / 2, yl - .19, lab, color=STC[s], fontsize=5.5, family=COND, weight="bold",
                ha="center", va="center")
    # title block
    tb = (8.35, .25, W - .25 - 8.35, 1.85)
    bg.add_patch(Rectangle(tb[:2], tb[2], tb[3], fill=True, fc=PANEL, ec=RULE, lw=.8))
    bg.text(8.5, 1.88, num, color=CU, fontsize=22, family=COND, weight="bold", va="top")
    bg.text(10.6, 1.86, BS.DOC.upper(), color=INK, fontsize=8, family=MONO, ha="right", va="top")
    bg.text(10.6, 1.68, DATE, color=INK2, fontsize=6.5, family=MONO, ha="right", va="top")
    bg.text(8.5, 1.36, "SCALE  " + scale_txt, color=INK, fontsize=7, family=MONO, va="top")
    bg.text(8.5, 1.12, BS.CREDIT, color=INK, fontsize=7.4, family=BODY, va="top")
    bg.text(8.5, .9, "Letter landscape · 300 dpi · true feet · X east, Y north, EL up", color=INK2, fontsize=5.8,
            family=BODY, va="top")
    bg.text(8.5, .72, "Sources: Oct 26, 2026 call; public record (ERock S-1/A,", color=INK2, fontsize=5.8, family=BODY, va="top")
    bg.text(8.5, .6, "10-Q Q2 2026, ERT500 release, PUCT Docket 59076). Nothing under NDA.", color=INK2, fontsize=5.8,
            family=BODY, va="top")
    bg.text(8.5, .43, BS.STAMP.upper(), color=CU2, fontsize=5.6, family=COND, weight="bold", va="top")
    # bottom-left stamp under the drawing
    bg.text(.4, .36, BS.STAMP.upper() + "   ·   " + BS.CREDIT + "   ·   " + BS.DOC + "  " + num, color=INK2,
            fontsize=5.8, family=COND)
    return fig, bg


def wrap(t, n):
    out, line = [], ""
    for w in t.split():
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def bubble(ax, x, y, n, r=.09, fs=6.5, lead=None):
    if lead:
        ax.plot([x, lead[0]], [y, lead[1]], color=CU, lw=.5, zorder=20)
        ax.add_patch(Circle(lead, r * .25, color=CU, zorder=20))
    ax.add_patch(Circle((x, y), r, fc=BG, ec=CU, lw=.8, zorder=21))
    ax.text(x, y, str(n), color=CU2, fontsize=fs, family=COND, weight="bold", ha="center", va="center", zorder=22)


def scaled_axes(fig, rect_in, N, cx, cy):
    """Axes at rect (inches) whose data units are feet at 1:N, centred on (cx, cy)."""
    x, y, w, h = rect_in
    ax = fig.add_axes([x / W, y / H, w / W, h / H])
    fw, fh = w * N / 12.0, h * N / 12.0
    ax.set_xlim(cx - fw / 2, cx + fw / 2)
    ax.set_ylim(cy - fh / 2, cy + fh / 2)
    ax.set_aspect("equal")
    ax.set_autoscale_on(False)
    ax.axis("off")
    ax.set_facecolor(BG)
    return ax


def scale_bar(bg, x, y, N, ft_ticks, label=None, angle=0.0):
    """Graphic bar at 1:N on the sheet (inches), ticks in feet. angle in degrees (iso axis)."""
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    L = ft_ticks[-1] * 12.0 / N
    for i, (a, b) in enumerate(zip(ft_ticks, ft_ticks[1:])):
        a_in, b_in = a * 12.0 / N, b * 12.0 / N
        p = [(x + a_in * c, y + a_in * s), (x + b_in * c, y + b_in * s), (x + b_in * c - .05 * s, y + b_in * s + .05 * c),
             (x + a_in * c - .05 * s, y + a_in * s + .05 * c)]
        bg.add_patch(Polygon(p, closed=True, fc=CU if i % 2 == 0 else BG, ec=CU, lw=.6))
    for t in ft_ticks:
        t_in = t * 12.0 / N
        bg.text(x + t_in * c + .07 * s, y + t_in * s - .07 * c, f"{t:g}", color=INK, fontsize=5.5, family=MONO,
                ha="center", va="top", rotation=angle)
    bg.text(x + L * c + .12 * c, y + L * s + .12 * s, "ft", color=INK, fontsize=5.5, family=MONO, va="center",
            rotation=angle)
    bg.text(x - .12 * s, y + .12 * c, label or f"1:{N:,}", color=INK2, fontsize=6, family=MONO, rotation=angle)


# ------------------------------------------------------------------------------------------------ geometry helpers
def block_boxes(bk, detail=False):
    """Simplified boxes of one block (world): units, GCB, XFMR (+ pads)."""
    P, I = M.TEMPLATE
    T = M.place(bk["bx"], bk["by"], bk["s"])
    out = []
    for kind, c, g in P:
        if kind != "b":
            continue
        if not detail and c not in ("encl", "gcb", "xfmr", "concrete"):
            continue
        (x0, y0), (x1, y1) = T(g[0], g[2]), T(g[1], g[3])
        out.append((min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), g[4], g[5], c))
    return out


def site_boxes(m, skip=("own", "fence", "seam", "door", "glass", "ownwall")):
    SP, SI = m["site"]
    return [(g[0], g[1], g[2], g[3], g[4], g[5], c) for kind, c, g, lay in SP if kind == "b" and lay != "gas" and c not in skip]


def plan_boxes(ax, boxes, lw=.2, alpha=1.0, z=1, mono=None):
    for x0, x1, y0, y1, z0, z1, c in boxes:
        fc = mono or FILL.get(c, "#7a8086")
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc if c not in ("ghost",) else "none",
                               ec="#5a6f86" if c == "ghost" else BG, lw=lw if c != "ghost" else .6,
                               ls="-" if c != "ghost" else (0, (4, 3)), alpha=alpha, zorder=z + (0 if c in ("road", "concrete", "berm") else 1)))


def plot_circuits(ax, circs, lw_scale=1.0, alpha=1.0, z=5):
    W_ = {"L1": .5, "L2": 1.0, "L3": 1.0, "L4": 1.0, "L5": 1.3, "L6": .35, "L7": .35}
    for c in circs:
        xs = [p[0] for p in c["pts"]]
        ys = [p[1] for p in c["pts"]]
        ax.plot(xs, ys, color=LC[c["layer"]], lw=W_[c["layer"]] * lw_scale, alpha=alpha, zorder=z,
                ls=(0, (4, 2)) if LDASH[c["layer"]] else "-", solid_capstyle="butt")


def own_line(ax, m, lab=True):
    s = m["layout"]["site"]
    y0, y1 = M.Y0 - 60, s["y_n"]
    ax.plot([s["own_x"]] * 2, [y0, y1], color="#d8402f", lw=.9, ls=(0, (6, 3)), zorder=8)
    if lab:
        ax.text(s["own_x"] + 8, (y0 + y1) / 2, "ER SCOPE  |  CUSTOMER SCOPE — TO VERIFY", color="#ef6a5a", fontsize=5.5,
                family=COND, weight="bold", rotation=90, va="center", zorder=9)


# ------------------------------------------------------------------------------------------------ SK-2301
def sk2301(pdf, m):
    lay = m["layout"]
    N = 4800
    fig, bg = fig_frame("SK-2301", "Campus isometric, 250 MW", "1:4,800 along the isometric axes", [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13],
                        notes=[f"{lay['params']['n_blocks']} RockBlocks, {lay['params']['n_units']} units of 500 kW, "
                               f"{lay['params']['n_groups']} groups of 8 on 35 kV loops, {lay['params']['n_lineups']} switchgear "
                               "lineups along the fence nearest the data center.",
                               "Isometric drawing: lengths along the three isometric axes are true at 1:4,800; the graphic bar "
                               "lies on the X axis. Base view: no circuits drawn (they live in the cable layers and SK-2305).",
                               "The data center is ghosted beyond the ownership line; its size is not modelled."])
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    iso = lambda x, y, z: ((x - y) * c30, (x + y) * s30 + z)
    boxes = site_boxes(m)
    for bk in lay["blocks"]:
        boxes += block_boxes(bk)
    s = lay["site"]
    cx, cy = iso(1000, 640, 0)
    ax = scaled_axes(fig, (.35, .55, 7.9, 7.65), N, cx, cy + 40)
    shade = lambda hexc, f: tuple(min(1, max(0, int(hexc[i:i + 2], 16) / 255 * f)) for i in (1, 3, 5))
    boxes.sort(key=lambda b: (-(b[0] + b[1] + b[2] + b[3]), b[4]))
    for x0, x1, y0, y1, z0, z1, c in boxes:
        col = FILL.get(c, "#7a8086")
        if c == "ghost":
            pts = [iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)]
            ax.add_patch(Polygon(pts, closed=True, fc="#5a6f86", alpha=.12, ec="#5a6f86", lw=.5, ls=(0, (4, 3))))
            for (a, b_) in ((x0, y0), (x1, y0), (x0, y1)):
                ax.plot(*zip(iso(a, b_, z0), iso(a, b_, z1)), color="#5a6f86", lw=.4, ls=(0, (4, 3)))
            continue
        top = [iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)]
        south = [iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y0, z1), iso(x0, y0, z1)]
        west = [iso(x0, y0, z0), iso(x0, y1, z0), iso(x0, y1, z1), iso(x0, y0, z1)]
        if z1 - z0 > .3:
            ax.add_patch(Polygon(west, closed=True, fc=shade(col, .55), ec="none"))
            ax.add_patch(Polygon(south, closed=True, fc=shade(col, .75), ec="none"))
        ax.add_patch(Polygon(top, closed=True, fc=shade(col, 1.0), ec=BG if z1 - z0 > .3 else "none", lw=.1))
    # ownership line
    y0, y1 = M.Y0 - 60, s["y_n"]
    ax.plot(*zip(iso(s["own_x"], y0, 0), iso(s["own_x"], y1, 0)), color="#d8402f", lw=.8, ls=(0, (6, 3)))
    # bubbles
    b1 = lay["blocks"][3]
    L0 = lay["lineups"][0]
    pts = {1: iso(b1["bx"] + 20, b1["by"] + 21, 9), 2: iso(b1["bx"] + 55, b1["by"] + 31, 7), 3: iso(b1["bx"] + 68, b1["by"] + 30, 7),
           5: iso(s["swg_x0"] + 8, L0["sy0"] + 32, 14), 6: iso(s["dc_x0"] + 260, 700, 48), 7: iso(s["own_x"], 200, 0),
           8: iso(120, M.Y0 + 70, 22), 9: iso(140, M.Y0 + 200, 30), 10: iso(170, M.Y0 + 330, 2), 11: iso(260, M.Y0 - 34, 6),
           13: iso(M.X0 + 160, M.Y0 + 63, 0)}
    off = {1: (-260, -340), 2: (-120, -420), 3: (40, -440), 5: (330, -260), 6: (300, 200), 7: (300, -300), 8: (-300, 120),
           9: (-320, 160), 10: (-300, 200), 11: (-280, -100), 13: (-300, -200)}
    for n, p in pts.items():
        bubble(ax, p[0] + off[n][0], p[1] + off[n][1], n, r=28, fs=6.5, lead=p)
    # north arrow (iso: north = +y -> screen direction (-c30, s30))
    nx, ny = .9, 7.6
    bg.annotate("", xy=(nx - .22 * c30, ny + .22 * s30), xytext=(nx, ny), arrowprops=dict(arrowstyle="-|>", color=CU, lw=1))
    bg.text(nx - .3 * c30, ny + .3 * s30, "N", color=INK, fontsize=8, family=COND, weight="bold", ha="center", va="center")
    scale_bar(bg, .55, .75, N, [0, 200, 400, 800], "1:4,800 on the X axis", angle=30)
    pdf.savefig(fig, facecolor=BG)
    return fig


# ------------------------------------------------------------------------------------------------ SK-2302
def dim(ax, a, b, off, text, st, vertical=False, fs=5.6):
    """Dimension string between a and b (plan coords), offset perpendicular."""
    col = STC[st]
    if not vertical:
        y = a[1] + off
        ax.plot([a[0], a[0]], [a[1], y + (.6 if off > 0 else -.6)], color=INK2, lw=.3)
        ax.plot([b[0], b[0]], [b[1], y + (.6 if off > 0 else -.6)], color=INK2, lw=.3)
        ax.annotate("", xy=(a[0], y), xytext=(b[0], y), arrowprops=dict(arrowstyle="<|-|>", color=col, lw=.5, mutation_scale=4))
        ax.text((a[0] + b[0]) / 2, y + (.5 if off > 0 else -.5), f"{text} {STS[st]}", color=col, fontsize=fs, family=MONO,
                ha="center", va="bottom" if off > 0 else "top")
    else:
        x = a[0] + off
        ax.plot([a[0], x + (.6 if off > 0 else -.6)], [a[1], a[1]], color=INK2, lw=.3)
        ax.plot([b[0], x + (.6 if off > 0 else -.6)], [b[1], b[1]], color=INK2, lw=.3)
        ax.annotate("", xy=(x, a[1]), xytext=(x, b[1]), arrowprops=dict(arrowstyle="<|-|>", color=col, lw=.5, mutation_scale=4))
        ax.text(x + (.5 if off > 0 else -.5), (a[1] + b[1]) / 2, f"{text} {STS[st]}", color=col, fontsize=fs, family=MONO,
                ha="left" if off > 0 else "right", va="center", rotation=90)


def sk2302(pdf, m):
    N = 180
    fig, bg = fig_frame("SK-2302", "Block plan and elevation, RB-nnn", "1:180 (plan and elevation)", [1, 2, 3, 4, 13],
                        notes=["One RockBlock in local coordinates, road side north. Dimension strings carry their status: "
                               "K known, WA working assumption, TV to verify.",
                               "Unit footprint 10 x 8 ft KNOWN (ERT500 release); 448 sq ft per 2.5 MW block KNOWN "
                               "(erock.com); unit height, GCB and transformer sizes are placeholders TO VERIFY.",
                               "Stack top EL 25: TCEQ gas-EGU standard permit minimum, working assumption."])
    bk = dict(bx=0, by=0, s=1)
    boxes = block_boxes(bk, detail=True)
    ax = scaled_axes(fig, (.35, 3.6, 7.9, 4.55), N, 38, 22)
    ax.add_patch(Rectangle((-6, M.ROW_D), 92, M.ROAD, fc=FILL["road"], ec="none", zorder=0))
    ax.text(38, M.ROW_D + 12, "GROUP ACCESS ROAD", color=INK2, fontsize=6, family=COND, ha="center")
    plan_boxes(ax, boxes, lw=.25)
    ax.plot([-6, 86], [M.LANE_OWN] * 2, color=LC["L3"], lw=.6, ls=(0, (3, 2)), zorder=6)
    ax.text(84, M.LANE_OWN + .5, "35 kV loop corridor", color=LC["L3"], fontsize=5.5, family=COND, ha="right", va="bottom", zorder=7)
    x0 = M.unit_x(0)
    dim(ax, (x0, M.UY0), (x0 + 8, M.UY0), -3.5, "8'-0\"", BS.K)
    dim(ax, (x0, M.UY0), (M.unit_x(1), M.UY0), -8, "8'-7\" pitch", BS.WA)
    dim(ax, (x0, M.UY0), (x0, M.UY1), -3.5, "10'-0\"", BS.K, vertical=True)
    dim(ax, (M.unit_x(0), M.UY0), (M.unit_x(4) + 8, M.UY0), -12.5, "42'-5\" (5 units)", BS.WA)
    dim(ax, (50, 29), (60, 29), -4.5, "10'", BS.TV)
    dim(ax, (64, 26), (73, 26), -6.5, "9'", BS.TV)
    dim(ax, (73, 26), (73, 35), 4.5, "9'", BS.TV, vertical=True)
    dim(ax, (0, 40), (80, 40), 6, "80'-0\" block pitch", BS.WA)
    dim(ax, (0, 0), (0, 40), -9, "40'-0\" block depth", BS.WA, vertical=True)
    for n, p, o in ((1, (M.unit_x(2) + 4, 21), (0, 12)), (2, (55, 31), (-6, 12)), (3, (68.5, 30), (4, 14)), (4, (30, M.LANE_OWN), (-14, 7)),
                    (13, (20, 52), (-14, 3))):
        bubble(ax, p[0] + o[0], p[1] + o[1], n, r=1.6, fs=6, lead=p)
    bg.text(.45, 8.05, "PLAN", color=INK, fontsize=9, family=COND, weight="bold")
    # elevation (looking north at the south face): x horizontal, z vertical
    ax2 = scaled_axes(fig, (.35, 1.05, 7.9, 2.3), N, 38, 11)
    ax2.plot([-6, 86], [0, 0], color=INK2, lw=.6)
    for x0_, x1_, y0, y1, z0, z1, c in sorted(boxes, key=lambda b: -b[2]):
        if c in ("louvre", "seam", "steel_dark", "concrete"):
            continue
        ax2.add_patch(Rectangle((x0_, z0), x1_ - x0_, z1 - z0, fc=FILL.get(c, "#7a8086"), ec=BG, lw=.25))
    for k in range(5):
        xc = M.unit_x(k) + 4
        ax2.add_patch(Rectangle((xc - .42, M.GH + 2), .84, M.STACK - M.GH - 2, fc=FILL["stack"], ec=BG, lw=.2))
        ax2.add_patch(Rectangle((xc - .9, M.GH + .3), 1.8, 1.8, fc=FILL["steel"], ec=BG, lw=.2))
    dim(ax2, (M.unit_x(0), 0), (M.unit_x(0), M.GH), -1.6, "9'-0\"", BS.TV, vertical=True)
    dim(ax2, (M.unit_x(0), 0), (M.unit_x(0), M.STACK), -5.5, "EL 25'-0\" stack top", BS.WA, vertical=True)
    dim(ax2, (73, 0), (73, 7.9), 5, "7'-11\"", BS.TV, vertical=True)
    bg.text(.45, 3.42, "ELEVATION, LOOKING NORTH", color=INK, fontsize=9, family=COND, weight="bold")
    scale_bar(bg, .55, .72, N, [0, 5, 10, 20, 30], "1:180  (1 in = 15 ft)")
    pdf.savefig(fig, facecolor=BG)


# ------------------------------------------------------------------------------------------------ SK-2303
def sk2303(pdf, m):
    N = 180
    fig, bg = fig_frame("SK-2303", "One block electrical: L1, L2, GCB, transformer", "1:180 (plan); one-line not to scale",
                        [1, 2, 3, 4],
                        notes=["L1 480 V generator leads, KNOWN topology: unit terminal box to its own GCB breaker; 2 parallel "
                               "sets of 4 x 1/C per unit (count and size TO VERIFY).",
                               "L2 block feed GCB to transformer LV: 8 parallel sets of 4 x 1/C or bus duct, TO VERIFY.",
                               "L6 ground ring 4/0 bare Cu with taps, L7 control + Cat6A per unit: working assumptions.",
                               "Circuits drawn at trench depth (EL -3); risers into the equipment bottoms."])
    lay = m["layout"]
    bk = lay["blocks"][0]
    circ = [c for c in m["circuits"] if c["block"] == bk["n"]]
    boxes = block_boxes(bk, detail=True)
    ax = scaled_axes(fig, (.35, 3.75, 7.9, 4.45), N, bk["bx"] + 38, bk["by"] + 24)
    plan_boxes(ax, boxes, lw=.25, alpha=.55)
    plot_circuits(ax, circ, lw_scale=1.6)
    g3 = [c for c in m["circuits"] if c["layer"] == "L3" and (c["frm"] == "XFMR-001" or c["to"] == "XFMR-001")]
    plot_circuits(ax, g3, lw_scale=1.6)
    ax.text(bk["bx"] + 59.5, bk["by"] + 29.5, "L2", color=LC["L2"], fontsize=6, family=MONO, weight="bold")
    ax.text(bk["bx"] + 2, bk["by"] + 12, "L6 ground ring", color=LC["L6"], fontsize=5.5, family=MONO, va="top")
    ax.text(bk["bx"] + 70, bk["by"] + 38.6, "L3 loop: from XFMR-002, on to XFMR-005 round the west road", color=LC["L3"], fontsize=5.5, family=MONO, va="bottom")
    for n, p, o in ((1, (bk["bx"] + M.unit_x(1) + 4, bk["by"] + 21), (-4, -13)), (2, (bk["bx"] + 55, bk["by"] + 31), (-8, -16)),
                    (3, (bk["bx"] + 68.5, bk["by"] + 30), (6, -16)), (4, (bk["bx"] + 40, bk["by"] + M.LANE_OWN), (0, 8))):
        bubble(ax, p[0] + o[0], p[1] + o[1], n, r=1.6, fs=6, lead=p)
    bg.text(.45, 8.05, "PLAN, RB-001 WITH ITS CIRCUITS", color=INK, fontsize=9, family=COND, weight="bold")
    # one-line (schematic, inches)
    ol = fig.add_axes([.35 / W, 1.0 / H, 7.9 / W, 2.55 / H])
    ol.set_xlim(0, 7.9)
    ol.set_ylim(0, 2.55)
    ol.axis("off")
    ol.text(.1, 2.42, "ONE-LINE, ONE BLOCK (NOT TO SCALE)", color=INK, fontsize=9, family=COND, weight="bold", va="top")
    for k in range(5):
        x = .55 + k * .7
        ol.add_patch(Circle((x, 1.75), .18, fill=False, ec=INK, lw=.8))
        ol.text(x, 1.75, "G", color=INK, fontsize=7, family=COND, ha="center", va="center", weight="bold")
        ol.text(x, 2.0, f"G-nnn-{k + 1}", color=INK2, fontsize=4.8, family=MONO, ha="center")
        ol.plot([x, x], [1.57, 1.2], color=LC["L1"], lw=1.4)
        ol.add_patch(Rectangle((x - .07, 1.0), .14, .14, fill=False, ec=INK, lw=.8))
        ol.plot([x, x], [1.0, .82], color=INK, lw=.8)
    ol.text(.2, 1.38, "L1  480 V", color=LC["L1"], fontsize=5.5, family=MONO, ha="left")
    ol.plot([.4, 3.5], [.82, .82], color=INK, lw=2.2)
    ol.text(3.55, .82, "GCB-nnn 480 V bus, 5 breakers (KNOWN)", color=INK, fontsize=5.5, family=MONO, va="center")
    ol.plot([2.0, 2.0], [.82, .5], color=LC["L2"], lw=2.2)
    ol.text(2.06, .62, "L2  8 sets or bus (TV)", color=LC["L2"], fontsize=5.5, family=MONO)
    for dy in (0, .22):
        ol.add_patch(Circle((2.0, .38 - dy), .12, fill=False, ec=INK, lw=.8))
    ol.text(2.2, .27, "XFMR-nnn 480 V : 34.5 kV, ~3 MVA (WA; kV TV)", color=INK, fontsize=5.5, family=MONO, va="center")
    ol.plot([2.0, 2.0], [.04, -.0], color=INK, lw=.8)
    ol.plot([1.0, 3.0], [.04, .04], color=LC["L3"], lw=2.0)
    ol.text(.98, .04, "L3 loop in ", color=LC["L3"], fontsize=5.5, family=MONO, ha="right", va="center")
    ol.text(3.02, .04, " L3 loop out", color=LC["L3"], fontsize=5.5, family=MONO, ha="left", va="center")
    scale_bar(bg, 5.4, .72, N, [0, 5, 10, 20], "1:180 plan (1 in = 15 ft)")
    pdf.savefig(fig, facecolor=BG)


# ------------------------------------------------------------------------------------------------ SK-2304
def sk2304(pdf, m):
    lay = m["layout"]
    p = lay["params"]
    nl, ng = p["n_lineups"], p["n_groups"]
    n_tie = nl if nl > 2 else (1 if nl == 2 else 0)
    fig, bg = fig_frame("SK-2304", "35 kV loop and lineup topology", "one-line NTS; key plan 1:9,600",
                        [3, 4, 5, 6, 7],
                        notes=["One loop per group: out from the group breaker, through every block transformer, home to the "
                               "same lineup (loop return position TO VERIFY: same breaker or a second one).",
                               "Lineup ties close a ring A-B-...-A (KNOWN: switchgear-to-switchgear loops for redundancy).",
                               "One ~75 MW feeder per lineup to the data center; scope owner TO VERIFY."])
    ol = fig.add_axes([.35 / W, 2.3 / H, 7.9 / W, 5.85 / H])
    ol.set_xlim(0, 7.9)
    ol.set_ylim(0, 5.85)
    ol.axis("off")
    ol.text(.1, 5.75, f"ONE-LINE, {p['mw']:g} MW CAMPUS (NOT TO SCALE)", color=INK, fontsize=9, family=COND, weight="bold", va="top")
    rowh = 5.2 / nl
    for li, L in enumerate(lay["lineups"]):
        y = 5.25 - li * rowh - rowh / 2
        ol.plot([5.6, 7.1], [y, y], color=INK, lw=2.4)
        ol.text(5.62, y + .07, L["tag"], color=CU2, fontsize=8, family=COND, weight="bold", va="bottom")
        gl = L["groups"]
        for j, gi in enumerate(gl):
            G = lay["groups"][gi]
            yy = y + (j - (len(gl) - 1) / 2) * min(.22, rowh / 5)
            ol.add_patch(Rectangle((5.6 - .14, yy - .045), .09, .09, fill=False, ec=INK, lw=.6))
            ol.plot([5.51, 5.6], [yy, yy], color=INK, lw=.6)
            nb = len(G["blocks"])
            xs = [.35 + q * (4.6 / max(nb, 1)) for q in range(nb)]
            ol.plot([xs[0], 5.46], [yy + .03, yy + .03], color=LC["L3"], lw=.7)
            ol.plot([xs[0], 5.46], [yy - .03, yy - .03], color=LC["L3"], lw=.7)
            ol.plot([xs[0], xs[0]], [yy - .03, yy + .03], color=LC["L3"], lw=.7)
            for x in xs:
                ol.add_patch(Circle((x + .1, yy), .03, fc=BG, ec=INK, lw=.4, zorder=3))
            ol.text(.3, yy, G["tag"], color=INK2, fontsize=4.6, family=MONO, ha="right", va="center")
        # feeder
        ol.add_patch(Rectangle((6.3 - .045, y - .2), .09, .09, fill=False, ec=INK, lw=.6))
        ol.plot([6.3, 6.3], [y, y - .11], color=INK, lw=.6)
        ol.plot([6.3, 6.3, 7.75], [y - .2, y - .26, y - .26], color=LC["L5"], lw=1.0)
        # ties
        if li < nl - 1:
            ol.plot([6.9, 6.9], [y, y - rowh], color=LC["L4"], lw=.9, ls=(0, (3, 2)))
            ol.add_patch(Rectangle((6.9 - .045, y - .18), .09, .09, fill=False, ec=INK, lw=.6))
    if nl > 2:
        ytop, ybot = 5.25 - rowh / 2, 5.25 - (nl - 1) * rowh - rowh / 2
        ol.plot([7.0, 7.45, 7.45, 7.0], [ybot, ybot, ytop, ytop], color=LC["L4"], lw=.9, ls=(0, (3, 2)))
        ol.text(7.5, (ytop + ybot) / 2, "L4 ring close", color=LC["L4"], fontsize=5, family=MONO, rotation=90, va="center")
    ol.text(7.75, .05, "to data center (L5, TV)", color=LC["L5"], fontsize=5, family=MONO, ha="right")
    ol.text(.35, .05, "o block transformer XFMR-nnn on the loop      [] breaker      L3 amber loop, L4 dashed ties, L5 red feeders",
            color=INK2, fontsize=5.2, family=MONO)
    # breaker reconciliation
    rec = [("Group breakers (one per loop)", ng), ("Tie breakers (2 per lineup, ring)" if nl > 2 else "Tie breakers", 2 * n_tie),
           ("Feeder breakers (one per lineup)", nl), ("Spare sections (one per lineup)", nl),
           ("Breakers + spares, total", ng + 2 * n_tie + 2 * nl), ("Loops = groups", ng), ("Transformers on loops = blocks", p["n_blocks"])]
    t = fig.add_axes([.35 / W, .55 / H, 4.4 / W, 1.6 / H])
    t.axis("off")
    t.set_xlim(0, 4.4)
    t.set_ylim(0, 1.6)
    t.text(0, 1.55, "BREAKER COUNT RECONCILED", color=INK, fontsize=8, family=COND, weight="bold", va="top")
    for i, (a, b) in enumerate(rec):
        yy = 1.3 - i * .17
        t.text(0, yy, a, color=INK, fontsize=6, family=BODY, va="center")
        t.text(3.2, yy, f"{b}", color=CU2 if i == 4 else INK, fontsize=6.5, family=MONO, ha="right", va="center")
    t.text(0, .03, f"Check: {ng} x 1 + {nl} x (2 ties + 1 feeder + 1 spare) = {ng + 2 * n_tie + 2 * nl}",
           color=INK2, fontsize=5.2, family=MONO)
    t.text(0, -.1, f"{p['n_blocks']} blocks / 8 per loop = {p['n_blocks'] / 8:g} -> {ng} loops", color=INK2, fontsize=5.2, family=MONO)
    # key plan at 1:9,600
    N = 9600
    s = lay["site"]
    kp = scaled_axes(fig, (4.9, .5, 3.35, 1.75), N, 950, 720)
    plan_boxes(kp, [b for b in site_boxes(m) if b[6] in ("ehouse", "ghost", "building", "water")], lw=.1)
    for bk in lay["blocks"]:
        kp.add_patch(Rectangle((bk["bx"], min(bk["by"], bk["by"] + bk["s"] * 40)), 76, 40, fc="#7a8086", ec="none"))
    plot_circuits(kp, [c for c in m["circuits"] if c["layer"] in ("L3", "L4", "L5")], lw_scale=.5)
    own_line(kp, m, lab=False)
    kp.text(950, 1450, "KEY PLAN", color=INK2, fontsize=6, family=COND, weight="bold", ha="center")
    scale_bar(bg, 5.0, .38, N, [0, 400, 800], "key plan 1:9,600")
    pdf.savefig(fig, facecolor=BG)


# ------------------------------------------------------------------------------------------------ SK-2305
def sk2305(pdf, m):
    lay = m["layout"]
    s = lay["site"]
    N = 2880
    fig, bg = fig_frame("SK-2305", "Four-view X-ray: context, sources, distribution, reach", "1:2,880 (all four views)",
                        [1, 3, 5, 6, 7],
                        notes=["The same two lineup bands (SWG-A and SWG-B, eight groups) four times, adding cable layers: 1 context, 2 sources "
                               "(L1 / L2 at every block), 3 internal distribution (L3 loops, L6, L7), 4 plant-wide reach "
                               "(L4 ties, L5 feeders across the ownership line).",
                               "Base views stay clean; these are the cable layers, drawn at trench depth."])
    L0 = lay["lineups"][0]
    cx, cy = 880, L0["band_y"] + 284
    panels = [("1  CONTEXT", []), ("2  SOURCES: L1, L2", ["L1", "L2"]), ("3  INTERNAL DISTRIBUTION: L3, L6, L7", ["L3", "L6", "L7"]),
              ("4  PLANT-WIDE REACH: ALL LAYERS", ["L1", "L2", "L3", "L4", "L5", "L6", "L7"])]
    base = site_boxes(m)
    blocks = []
    for bk in lay["blocks"]:
        blocks += block_boxes(bk)
    rects = [(.35, 4.5, 3.9, 3.55), (4.35, 4.5, 3.9, 3.55), (.35, .75, 3.9, 3.55), (4.35, .75, 3.9, 3.55)]
    for (t, Ls), r in zip(panels, rects):
        ax = scaled_axes(fig, r, N, cx, cy)
        dim_ = .35 if Ls else 1.0
        plan_boxes(ax, base, lw=.1, alpha=dim_)
        plan_boxes(ax, blocks, lw=.05, alpha=dim_)
        own_line(ax, m, lab=False)
        if Ls:
            plot_circuits(ax, [c for c in m["circuits"] if c["layer"] in Ls], lw_scale=.55)
        bg.text(r[0] + .08, r[1] + r[3] - .05, t, color=INK, fontsize=7.5, family=COND, weight="bold", va="top")
        bg.add_patch(Rectangle((r[0], r[1]), r[2], r[3], fill=False, ec=RULE, lw=.6))
        if not Ls:
            b4 = lay["blocks"][3]
            for n, p, o in ((1, (b4["bx"] + 20, b4["by"] + 21), (-60, -70)), (3, (b4["bx"] + 68, b4["by"] + 30), (40, -80)),
                            (5, (s["swg_x0"] + 8, L0["sy0"] + 32), (80, 60)), (6, (s["dc_x0"] + 30, L0["sy0"]), (60, -90)),
                            (7, (s["own_x"], L0["band_y"] + 20), (-40, -60))):
                bubble(ax, p[0] + o[0], p[1] + o[1], n, r=17, fs=6, lead=p)
    leg = [f"{k} {n.split(' (')[0]}" for k, n, _, _, _ in BS.LAYERS]
    bg.text(.4, .6, " · ".join(leg[:4]), color=INK2, fontsize=5, family=MONO)
    bg.text(.4, .5, " · ".join(leg[4:]), color=INK2, fontsize=5, family=MONO)
    scale_bar(bg, 5.6, .52, N, [0, 100, 200, 400], "1:2,880 (1 in = 240 ft)")
    pdf.savefig(fig, facecolor=BG)


# ------------------------------------------------------------------------------------------------ SK-2306
def sk2306(pdf, m):
    t = TO.takeoff(250)
    fig, bg = fig_frame("SK-2306", "Per-block takeoff, campus roll-up, verification register", "key plan 1:480; tables n/a",
                        [1, 2, 3],
                        notes=["cut = (routed + risers + terminations + slack) x (1 + spare); conductor-ft = cut x conductors x runs.",
                               "MEASURED off the model's routes; ASSUMED = a stated typical length per run. The two totals are never "
                               "summed. L5 feeders on the ASSUMED basis until their scope is confirmed.",
                               "No stock numbers, no dollars. CSV / JSON carry every circuit."])
    ax = fig.add_axes([.35 / W, .5 / H, 7.9 / W, 7.65 / H])
    ax.set_xlim(0, 7.9)
    ax.set_ylim(0, 7.65)
    ax.axis("off")
    y = 7.55
    ax.text(0, y, "PER-BLOCK CABLE KIT · RB-001 (EVERY BLOCK IS THE SAME)", color=INK, fontsize=8, family=COND, weight="bold", va="top")
    y -= .25
    cols = [("Layer", 0), ("Circuit", .35), ("From - to", 1.1), ("Runs", 2.75), ("Cond", 3.1), ("Len/run ft", 3.45), ("Cut ft", 4.05),
            ("Cond-ft", 4.6), ("Construction", 5.15)]
    for h, x in cols:
        ax.text(x, y, h.upper(), color=INK2, fontsize=5, family=COND, weight="bold")
    y -= .04
    ax.plot([0, 7.9], [y, y], color=CU, lw=.6)
    kit = sorted(t["kit_block"], key=lambda r: (r["layer"], r["tag"]))
    agg = []
    for r in kit:                        # fold the eight ground taps into one row
        if r["layer"] == "L6" and "-T" in r["tag"]:
            if agg and agg[-1]["tag"] == "L6-001-T1..T8":
                a = agg[-1]
                a["routed"] += r["routed"] + r["risers"]
                a["cut"] += r["cut"]
                a["cft"] += r["cft"]
                continue
            r = dict(r, tag="L6-001-T1..T8", frm="ring", to="8 taps", routed=r["routed"] + r["risers"], risers=0)
        agg.append(dict(r))
    tot = 0
    for r in agg:
        y -= .145
        vals = [r["layer"], r["tag"], f"{r['frm']} → {r['to']}"[:30], str(r["runs"]), str(r["cond"]),
                f"{r['routed'] + r['risers']:.1f}", f"{r['cut']:.1f}", f"{r['cft']:,}", r["construction"][:40]]
        for (h, x), v in zip(cols, vals):
            ax.text(x + (.3 if h in ("Runs", "Cond") else .5 if h in ("Len/run ft", "Cut ft", "Cond-ft") else 0), y, v,
                    color=LC.get(r["layer"], INK) if h == "Layer" else INK, fontsize=5.2,
                    family=MONO, ha="right" if h in ("Runs", "Cond", "Len/run ft", "Cut ft", "Cond-ft") else "left")
        tot += r["cft"]
    y -= .17
    ax.plot([0, 7.9], [y + .1, y + .1], color=CU, lw=.5)
    ax.text(0, y, "Block kit total, MEASURED", color=INK, fontsize=5.8, family=BODY, weight="bold")
    ax.text(5.1, y, f"{tot:,} conductor-ft", color=CU2, fontsize=5.8, family=MONO, ha="right")
    # roll-up across sizes
    y -= .35
    ax.text(0, y, "CAMPUS ROLL-UP · CONDUCTOR-FT BY LAYER · SAME MODEL, THREE CAMPUSES", color=INK, fontsize=8, family=COND, weight="bold", va="top")
    y -= .25
    T3 = {mw: TO.takeoff(mw) for mw in (250, 500, 1000)}
    hdr = ["Layer", "Family", "Status", "Basis", "250 MW", "500 MW", "1,000 MW"]
    xs = [0, .35, 2.6, 3.45, 4.75, 5.75, 6.85]
    for h, x in zip(hdr, xs):
        ax.text(x, y, h.upper(), color=INK2, fontsize=5, family=COND, weight="bold", ha="right" if "MW" in h else "left")
    y -= .04
    ax.plot([0, 7.9], [y, y], color=CU, lw=.6)
    for d in T3[250]["rollup"]:
        y -= .15
        k = d["layer"]
        vals = [k, d["name"][:40], STS[d["status"]], d["basis"]] + [f"{next(e for e in T3[mw]['rollup'] if e['layer'] == k)['conductor_ft']:,}"
                                                                     for mw in (250, 500, 1000)]
        for i, (v, x) in enumerate(zip(vals, xs)):
            ax.text(x, y, v, color=(LC[k] if i == 0 else STC[d["status"]] if i == 2 else INK), fontsize=5.4, family=MONO,
                    ha="right" if i >= 4 else "left")
    for b in ("MEASURED", "ASSUMED"):
        y -= .17
        ax.text(0, y, f"Total, {b} rows" + (" (never added to the measured total)" if b == "ASSUMED" else ""), color=INK,
                fontsize=5.6, family=BODY, weight="bold")
        for mw, x in zip((250, 500, 1000), xs[4:]):
            ax.text(x, y, f"{T3[mw]['totals'][b]:,}", color=CU2 if b == "MEASURED" else INK, fontsize=5.6, family=MONO, ha="right")
    y -= .15
    for mw, x in zip((250, 500, 1000), xs[4:]):
        p = T3[mw]["params"]
        ax.text(x, y, f"{p['n_blocks']} blk · {p['n_groups']} grp · {p['n_lineups']} SWG", color=INK2, fontsize=4.6, family=MONO, ha="right")
    # register (TV items)
    y -= .38
    ax.text(0, y, "VERIFICATION REGISTER · OPEN ITEMS (TO VERIFY) AND WHERE TO CHECK", color=INK, fontsize=8, family=COND, weight="bold", va="top")
    y -= .2
    for k, v in BS.B.items():
        if v[2] != BS.TV:
            continue
        y -= .14
        val = v[0] if not isinstance(v[0], tuple) else " x ".join(f"{x:g}" for x in v[0])
        ax.text(0, y, "TV", color=STC[BS.TV], fontsize=5.2, family=MONO)
        ax.text(.3, y, f"{v[3]}: {val} {v[1]}".strip()[:84], color=INK, fontsize=5.2, family=BODY)
        ax.text(7.9, y, v[4][:40], color=INK2, fontsize=5.2, family=BODY, ha="right")
    # key plan of one block at 1:480 (bottom-right of the drawing area)
    N = 480
    kp = scaled_axes(fig, (8.5, 2.95, 1.9, 1.05), N, 38, 20)
    plan_boxes(kp, block_boxes(dict(bx=0, by=0, s=1)), lw=.1)
    plot_circuits(kp, [c for c in m["circuits"] if c["block"] == 1 and c["layer"] in ("L1", "L2")], lw_scale=.4)
    for n, p in ((1, (M.unit_x(0) + 4, 21)), (2, (55, 31)), (3, (68.5, 30))):
        bubble(kp, p[0], p[1] + 12, n, r=3.2, fs=5, lead=p)
    scale_bar(bg, 8.55, 2.72, N, [0, 20, 40], "key plan 1:480")
    pdf.savefig(fig, facecolor=BG)


def main():
    m = M.build(250)
    path = os.path.join(OUT, "ER-RB_Rev00_SK-2300.pdf")
    with PdfPages(path) as pdf:
        for f in (sk2301, sk2302, sk2303, sk2304, sk2305, sk2306):
            f(pdf, m)
            plt.close("all")
    print("wrote", path)


if __name__ == "__main__":
    main()
