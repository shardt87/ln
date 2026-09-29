#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sheets.py  --  compose each render into a numbered drawing sheet (Pillow), then bind the set (reportlab)

    python3 make_sheets.py --views views.json --renders out/renders --out out/sheets [--only 01,04] [--no-pdf]

Sheet template (landscape 4:3, 300 dpi, 6000 x 4500 px by default, see views.json "sheet"):
    title top-left (bold, dark grey), subtitle "Subject | what the view explains" in light grey, short copper rule,
    render below filling the width (declared crop, no stretching; credit line is already in the pixels),
    callouts: white disc, copper ring, thin leader to a small copper dot,
    legend in 3-4 columns, one-line footnote, fixed disclaimer, "NN / TOTAL" bottom-right.
Every camera view is issued twice: clean, then tagged.  The last sheet is text-only.
Callout positions come from out/renders/callouts.json written by render_views.py.
"""
import json, os, sys, math, argparse
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--views", default="views.json")
ap.add_argument("--renders", default="out/renders")
ap.add_argument("--out", default="out/sheets")
ap.add_argument("--only", default=None)
ap.add_argument("--no-pdf", action="store_true")
ap.add_argument("--placeholders", action="store_true", help="use flat placeholders where a render is missing (pipeline test)")
A = ap.parse_args()

V = json.load(open(A.views))
S = V["sheet"]
W, H = S["px"]
DPI = S["dpi"]
MARGIN = S.get("margin_px", 200)
COL = S["colors"]
os.makedirs(A.out, exist_ok=True)
CALL_PATH = os.path.join(A.renders, "callouts.json")
CALLOUTS = json.load(open(CALL_PATH)) if os.path.exists(CALL_PATH) else {"views": {}, "render_px": V["render"]["px"]}

def pt(p):
    return int(round(p / 72.0 * DPI))

# ---- fonts -----------------------------------------------------------------
def find_font(bold=False):
    cands = (["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf", "Helvetica-Bold.ttf"] if bold else
             ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf", "arial.ttf", "Helvetica.ttf"])
    dirs = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation", "/usr/share/fonts", "/Library/Fonts",
            "/System/Library/Fonts", "C:/Windows/Fonts", os.path.expanduser("~/.fonts"), os.path.expanduser("~/Library/Fonts")]
    for d in dirs:
        for c in cands:
            p = os.path.join(d, c)
            if os.path.exists(p):
                return p
        if os.path.isdir(d):
            for root, _, files in os.walk(d):
                for c in cands:
                    if c in files:
                        return os.path.join(root, c)
    return None

FONT_REG, FONT_BOLD = find_font(False), find_font(True)

def font(size_px, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    try:
        if path:
            return ImageFont.truetype(path, size_px)
        return ImageFont.load_default(size=size_px)
    except Exception:
        return ImageFont.load_default()

def text_w(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0]

def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

# ---- page skeleton -------------------------------------------------------------
def new_page():
    img = Image.new("RGB", (W, H), COL["page"])
    return img, ImageDraw.Draw(img)

def header(draw, view):
    f_t = font(pt(S["title_pt"]), bold=True)
    f_s = font(pt(S["subtitle_pt"]))
    y = MARGIN * 0.8
    draw.text((MARGIN, y), view["title"], fill=COL["title"], font=f_t)
    y += pt(S["title_pt"]) * 1.25
    draw.text((MARGIN, y), view["subtitle"], fill=COL["subtitle"], font=f_s)
    y += pt(S["subtitle_pt"]) * 1.35
    draw.rectangle([MARGIN, y, MARGIN + int(W * 0.09), y + pt(2)], fill=COL["copper"])
    return int(y + pt(2) + MARGIN * 0.3)

def footer(draw, view, page_no, total):
    f_f = font(pt(S["footnote_pt"]))
    f_p = font(pt(S["page_pt"]), bold=True)
    y = H - MARGIN * 0.75 - pt(S["footnote_pt"]) * 2.6
    draw.text((MARGIN, y), view.get("footnote", ""), fill=COL["footnote"], font=f_f)
    y += pt(S["footnote_pt"]) * 1.4
    draw.text((MARGIN, y), S["disclaimer"], fill=COL["footnote"], font=f_f)
    label = "%02d / %02d" % (page_no, total)
    draw.text((W - MARGIN - text_w(draw, label, f_p), y), label, fill=COL["title"], font=f_p)
    return int(H - MARGIN * 0.75 - pt(S["footnote_pt"]) * 2.6 - MARGIN * 0.25)

# ---- render placement --------------------------------------------------------
def load_render(view):
    path = os.path.join(A.renders, view["id"] + ".png")
    rw, rh = CALLOUTS.get("render_px", V["render"]["px"])
    if os.path.exists(path):
        im = Image.open(path).convert("RGB")
        return im, True
    if not A.placeholders:
        raise FileNotFoundError("render missing: %s (use --placeholders to test the layout)" % path)
    im = Image.new("RGB", (rw, rh), "#CFCECA")
    d = ImageDraw.Draw(im)
    f = font(int(rh * 0.03))
    d.text((rw * 0.05, rh * 0.45), "render %s missing - placeholder" % view["id"], fill="#8A8985", font=f)
    d.text((rw * 0.02, rh * 0.95), S["credit"], fill=COL["text"], font=font(int(rh * 0.011)))
    return im, False

def place_render(page, draw, view, y_top, y_bottom_limit):
    """crop the declared top band off, scale to the page width (or less if the height does not fit), paste, return transform."""
    im, real = load_render(view)
    rw, rh = im.size
    ct = float(view["camera"].get("crop_top", 0.0))
    crop_y0 = int(round(rh * ct))
    im = im.crop((0, crop_y0, rw, rh))
    cw, ch = im.size
    avail_w = W - 2 * MARGIN
    avail_h = y_bottom_limit - y_top
    scale = min(avail_w / cw, avail_h / ch)
    nw, nh = int(round(cw * scale)), int(round(ch * scale))
    x0 = (W - nw) // 2
    im = im.resize((nw, nh), Image.LANCZOS)
    page.paste(im, (x0, y_top))
    return dict(x0=x0, y0=y_top, x1=x0 + nw, y1=y_top + nh, scale=scale, crop_y0=crop_y0, rw=rw, rh=rh)

# ---- callouts ---------------------------------------------------------------
def draw_callouts(page, view, tf):
    vid = view["id"]
    proj = CALLOUTS["views"].get(vid, {}).get("anchors", {})
    r = int(W * 0.0078)                # bubble radius ~47 px on a 6000 px sheet
    ring = max(2, int(r * 0.11))
    dot = max(3, int(r * 0.2))
    lead = max(2, int(r * 0.07))
    SS = 2                             # supersampled overlay for smooth circles
    ov = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    f_b = font(int(r * 1.15), bold=True)
    placed = []
    legend = []
    for c in view.get("callouts", []):
        a = proj.get(c["anchor"])
        if a is None:
            print("  ! %s: no projection for %s (render_views.py not run for this view?)" % (vid, c["anchor"]))
            legend.append((c["tag"], c.get("label") or c["anchor"].replace("ANCHOR-", "")))
            continue
        # render pixel -> sheet pixel (accounts for the declared crop and the placement scale)
        rx = a["u"] * tf["rw"]
        ry = a["v"] * tf["rh"] - tf["crop_y0"]
        px = tf["x0"] + rx * tf["scale"]
        py = tf["y0"] + ry * tf["scale"]
        if not a["in_frame"] or ry < 0:
            print("  ! %s: callout %s (%s) is outside the cropped image" % (vid, c["tag"], c["anchor"]))
            continue
        # bubble position: explicit offset (fraction of bubble radius units) or automatic
        if "dx" in c or "dy" in c:
            bx, by = px + c.get("dx", 0) * r, py + c.get("dy", 0) * r
        else:
            bx, by = auto_offset(px, py, r, tf, placed)
        placed.append((bx, by))
        # leader: from bubble edge toward the dot
        vx, vy = px - bx, py - by
        L = math.hypot(vx, vy) or 1.0
        ex, ey = bx + vx / L * r, by + vy / L * r
        od.line([(ex * SS, ey * SS), (px * SS, py * SS)], fill=COL["copper"], width=lead * SS)
        od.ellipse([(px - dot) * SS, (py - dot) * SS, (px + dot) * SS, (py + dot) * SS], fill=COL["copper"])
        od.ellipse([(bx - r) * SS, (by - r) * SS, (bx + r) * SS, (by + r) * SS], fill=COL["bubble"], outline=COL["copper"], width=ring * SS)
        legend.append((c["tag"], c.get("label") or label_for(view, c, a)))
    ov = ov.resize((W, H), Image.LANCZOS)
    page.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(page)
    for (bx, by), c in zip(placed, [c for c in view.get("callouts", []) if proj.get(c["anchor"]) and proj[c["anchor"]]["in_frame"]]):
        tw = text_w(d, c["tag"], f_b)
        bb = d.textbbox((0, 0), c["tag"], font=f_b)
        th = bb[3] - bb[1]
        d.text((bx - tw / 2, by - th / 2 - bb[1]), c["tag"], fill=COL["title"], font=f_b)
    return legend

def label_for(view, c, a):
    if c["anchor"].startswith("ANCHOR-ZONE-"):
        return V["zones"].get(str(int(c["anchor"].split("-")[-1])), a.get("label", ""))
    return a.get("label", "")

def auto_offset(px, py, r, tf, placed):
    best, best_score = None, 1e18
    dist = r * 3.4
    for k in range(16):
        ang = math.radians(k * 22.5 + 11.25)
        bx, by = px + math.cos(ang) * dist, py - math.sin(ang) * dist
        if not (tf["x0"] + r < bx < tf["x1"] - r and tf["y0"] + r < by < tf["y1"] - r * 4):
            continue
        score = 0.0
        for (ox, oy) in placed:
            dd = math.hypot(bx - ox, by - oy)
            if dd < r * 2.4:
                score += (r * 2.4 - dd) * 10
        score += abs(math.sin(ang)) * 0.0 + k * 0.01     # prefer the first (upper-right) directions when tied
        if score < best_score:
            best, best_score = (bx, by), score
    if best is None:
        best = (px + dist, py - dist)
    return best

def draw_legend(draw, legend, y, y_max):
    f_l = font(pt(S["legend_pt"]))
    f_b = font(int(pt(S["legend_pt"]) * 0.95), bold=True)
    ncol = S.get("legend_columns", 4)
    if len(legend) <= 6:
        ncol = 3
    col_w = (W - 2 * MARGIN) / ncol
    rows = int(math.ceil(len(legend) / ncol))
    r = int(pt(S["legend_pt"]) * 0.62)
    line_h = int(pt(S["legend_pt"]) * 1.9)
    for i, (tag, label) in enumerate(legend):
        col, row = i // rows, i % rows
        x = MARGIN + col * col_w
        yy = y + row * line_h
        if yy + line_h > y_max:
            break
        draw.ellipse([x, yy, x + 2 * r, yy + 2 * r], fill=COL["bubble"], outline=COL["copper"], width=max(2, r // 7))
        tw = text_w(draw, tag, f_b)
        bb = draw.textbbox((0, 0), tag, font=f_b)
        draw.text((x + r - tw / 2, yy + r - (bb[3] - bb[1]) / 2 - bb[1]), tag, fill=COL["title"], font=f_b)
        lines = wrap(draw, label, f_l, col_w - 3 * r - 20)
        draw.text((x + 2 * r + 18, yy + r - pt(S["legend_pt"]) * 0.6), lines[0] + (" ..." if len(lines) > 1 else ""), fill=COL["text"], font=f_l)
    return y + rows * line_h

# ---- text-only sheet ---------------------------------------------------------
def text_sheet(view, page_no, total):
    page, d = new_page()
    y = header(d, view)
    y_end = footer(d, view, page_no, total)
    f_h = font(pt(20), bold=True)
    f_b = font(pt(15.5))
    f_s = font(pt(13))
    # power path row
    path = view["path"]
    n = len(path)
    gap = int(W * 0.02)
    box_w = int((W - 2 * MARGIN - gap * (n - 1)) / n)
    box_h = int(pt(20) * 2.4)
    y += MARGIN * 0.2
    for i, step in enumerate(path):
        x = MARGIN + i * (box_w + gap)
        d.rectangle([x, y, x + box_w, y + box_h], fill=COL["bubble"], outline=COL["copper"], width=pt(1.2))
        tw = text_w(d, step, f_h)
        d.text((x + (box_w - tw) / 2, y + box_h * 0.28), step, fill=COL["title"], font=f_h)
        if i < n - 1:
            d.line([x + box_w, y + box_h / 2, x + box_w + gap, y + box_h / 2], fill=COL["copper"], width=pt(1.2))
            d.polygon([(x + box_w + gap, y + box_h / 2), (x + box_w + gap - pt(4), y + box_h / 2 - pt(2.5)), (x + box_w + gap - pt(4), y + box_h / 2 + pt(2.5))], fill=COL["copper"])
        lines = wrap(d, view["path_detail"][i], f_s, box_w - pt(4))
        for j, ln in enumerate(lines[:7]):
            d.text((x + pt(2), y + box_h + pt(6) + j * pt(13) * 1.35), ln, fill=COL["text"], font=f_s)
    y += box_h + pt(6) + 7 * pt(13) * 1.35 + MARGIN * 0.35
    # three columns
    cols = view["columns"]
    col_w = int((W - 2 * MARGIN - gap * 2) / 3)
    ymax_cols = y
    for i, col in enumerate(cols):
        x = MARGIN + i * (col_w + gap)
        d.text((x, y), col["heading"], fill=COL["title"], font=f_h)
        d.rectangle([x, y + pt(20) * 1.3, x + int(col_w * 0.25), y + pt(20) * 1.3 + pt(1.5)], fill=COL["copper"])
        yy = y + pt(20) * 1.3 + pt(1.5) + pt(8)
        for item in col["items"]:
            d.ellipse([x, yy + pt(15.5) * 0.3, x + pt(5), yy + pt(15.5) * 0.3 + pt(5)], fill=COL["copper"])
            lines = wrap(d, item, f_b, col_w - pt(10))
            for ln in lines:
                d.text((x + pt(9), yy), ln, fill=COL["text"], font=f_b)
                yy += pt(15.5) * 1.45
            yy += pt(3)
        ymax_cols = max(ymax_cols, yy)
    y = ymax_cols + MARGIN * 0.3
    # abbreviations
    d.text((MARGIN, y), "Abbreviations", fill=COL["title"], font=f_h)
    y += pt(20) * 1.6
    ab = view["abbreviations"]
    ncol = 4
    rows = int(math.ceil(len(ab) / ncol))
    col_w = int((W - 2 * MARGIN) / ncol)
    for i, (k, vv) in enumerate(ab):
        c, r = i // rows, i % rows
        x = MARGIN + c * col_w
        yy = y + r * pt(13) * 1.6
        if yy > y_end - pt(13):
            break
        f_k = font(pt(13), bold=True)
        d.text((x, yy), k, fill=COL["title"], font=f_k)
        d.text((x + max(pt(52), text_w(d, k, f_k) + pt(10)), yy), vv, fill=COL["text"], font=f_s)
    return page

# ---- main ----------------------------------------------------------------------
def main():
    views = V["views"]
    cams = [v for v in views if v.get("kind", "camera") == "camera"]
    texts = [v for v in views if v.get("kind") == "text"]
    total = 2 * len(cams) + len(texts)
    only = set(A.only.split(",")) if A.only else None
    pages = []
    page_no = 0
    for v in views:
        if v.get("kind", "camera") == "text":
            page_no += 1
            if only and v["id"] not in only:
                continue
            p = text_sheet(v, page_no, total)
            fn = os.path.join(A.out, "sheet_%02d_%s_text.png" % (page_no, v["id"]))
            p.save(fn); pages.append(fn); print("wrote", fn)
            continue
        for tagged in (False, True):
            page_no += 1
            if only and v["id"] not in only:
                continue
            page, d = new_page()
            y = header(d, v)
            y_end = footer(d, v, page_no, total)
            legend_h = 0
            if tagged:
                n = len(v.get("callouts", []))
                ncol = 3 if n <= 6 else S.get("legend_columns", 4)
                legend_h = int(math.ceil(n / ncol)) * int(pt(S["legend_pt"]) * 1.9) + MARGIN * 0.3
            tf = place_render(page, d, v, y, int(y_end - legend_h))
            if tagged:
                legend = draw_callouts(page, v, tf)
                d = ImageDraw.Draw(page)
                draw_legend(d, legend, tf["y1"] + int(MARGIN * 0.3), y_end)
            fn = os.path.join(A.out, "sheet_%02d_%s_%s.png" % (page_no, v["id"], "tagged" if tagged else "clean"))
            page.save(fn); pages.append(fn); print("wrote", fn)
    if not A.no_pdf and pages:
        bind_pdf(pages, os.path.join(A.out, "drawing_set.pdf"))

def bind_pdf(pages, path):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
    except ImportError:
        print("reportlab not installed: PDF not written (pip install reportlab)")
        return
    pw, ph = W / DPI * 72.0, H / DPI * 72.0
    c = canvas.Canvas(path, pagesize=(pw, ph))
    c.setTitle(V.get("series", "Drawing set"))
    for p in pages:
        c.drawImage(ImageReader(p), 0, 0, width=pw, height=ph)
        c.showPage()
    c.save()
    print("wrote", path)

main()
