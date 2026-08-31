# make_sheets.py — compose CAD-style renders into an engineering sheet-set PDF.
#
# Wraps each render from render_cad.py in standard drafting sheet furniture:
# trimmed border with zone reference grid, title block, revision table,
# third-angle projection symbol, general notes, and a graphic scale bar.
#
# Usage:
#   python scripts/blender/make_sheets.py --images-dir out/cad --output out/sheets.pdf
#
# The sheet list at the bottom maps image basenames to sheet titles/numbers;
# adjust it (or pass --project/--drawn/--rev) for other models.

import argparse
import os

from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = 17 * inch, 11 * inch  # ANSI B landscape
MARGIN = 0.42 * inch
ZONE_COLS = 8
ZONE_ROWS = 4
INK = (0.08, 0.09, 0.11)
ACCENT = (0.84, 0.42, 0.04)


def hairline(c, w=0.6):
    c.setLineWidth(w)
    c.setStrokeColorRGB(*INK)


def draw_border(c):
    hairline(c, 1.6)
    c.rect(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN)
    tick = 0.16 * inch
    hairline(c, 0.7)
    # zone reference grid on all four edges
    for i in range(1, ZONE_COLS):
        x = MARGIN + (PAGE_W - 2 * MARGIN) * i / ZONE_COLS
        c.line(x, MARGIN, x, MARGIN - tick + 0.16 * inch)
        c.line(x, PAGE_H - MARGIN, x, PAGE_H - MARGIN + tick - 0.16 * inch)
    for j in range(1, ZONE_ROWS):
        y = MARGIN + (PAGE_H - 2 * MARGIN) * j / ZONE_ROWS
        c.line(MARGIN, y, MARGIN - tick + 0.16 * inch, y)
        c.line(PAGE_W - MARGIN, y, PAGE_W - MARGIN + tick - 0.16 * inch, y)
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(*INK)
    for i in range(ZONE_COLS):
        x = MARGIN + (PAGE_W - 2 * MARGIN) * (i + 0.5) / ZONE_COLS
        label = str(ZONE_COLS - i)  # numbered right-to-left per drafting convention
        c.drawCentredString(x, MARGIN - 0.22 * inch, label)
        c.drawCentredString(x, PAGE_H - MARGIN + 0.12 * inch, label)
    for j in range(ZONE_ROWS):
        y = MARGIN + (PAGE_H - 2 * MARGIN) * (j + 0.5) / ZONE_ROWS
        label = chr(ord("A") + j)
        c.drawCentredString(MARGIN - 0.18 * inch, y - 2.5, label)
        c.drawCentredString(PAGE_W - MARGIN + 0.18 * inch, y - 2.5, label)
    # centring marks
    hairline(c, 1.0)
    for x, y, dx, dy in [(PAGE_W / 2, MARGIN, 0, -1), (PAGE_W / 2, PAGE_H - MARGIN, 0, 1),
                         (MARGIN, PAGE_H / 2, -1, 0), (PAGE_W - MARGIN, PAGE_H / 2, 1, 0)]:
        c.line(x, y, x + dx * 0.25 * inch, y + dy * 0.25 * inch)


def draw_title_block(c, meta, sheet):
    w, h = 5.1 * inch, 1.62 * inch
    x0, y0 = PAGE_W - MARGIN - w, MARGIN
    hairline(c, 1.2)
    c.rect(x0, y0, w, h)
    r1, r2 = y0 + h - 0.42 * inch, y0 + h - 0.80 * inch
    r3 = y0 + 0.40 * inch
    hairline(c, 0.7)
    c.line(x0, r1, x0 + w, r1)
    c.line(x0, r2, x0 + w, r2)
    c.line(x0, r3, x0 + w, r3)

    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x0 + 8, r1 + 11, meta["project"])
    c.setFont("Helvetica", 6.5)
    c.drawString(x0 + 8, r1 + 3, meta["subtitle"])

    c.setFont("Helvetica", 6)
    c.drawString(x0 + 8, r2 + h * 0.132, "SHEET TITLE")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + 8, r2 + 5, sheet["title"])

    # middle band: field grid
    cols = [("SCALE", sheet.get("scale", "AS NOTED")), ("SIZE", "ANSI B"),
            ("DWG NO", sheet["number"]), ("REV", meta["rev"]), ("STATUS", meta["status"])]
    cw = w / len(cols)
    for i, (label, value) in enumerate(cols):
        cx = x0 + i * cw
        if i:
            c.line(cx, r3, cx, r2)
        c.setFont("Helvetica", 6)
        c.drawString(cx + 5, r2 - 9, label)
        c.setFont("Helvetica-Bold", 9 if len(value) < 14 else 7.5)
        color = ACCENT if label == "STATUS" else INK
        c.setFillColorRGB(*color)
        c.drawString(cx + 5, r3 + 6, value)
        c.setFillColorRGB(*INK)

    cols2 = [("DRAWN", meta["drawn"]), ("CHECKED", meta.get("checked", "—")),
             ("DATE", meta["date"]), ("MODEL BASIS", meta["basis"])]
    cw2 = w / len(cols2)
    for i, (label, value) in enumerate(cols2):
        cx = x0 + i * cw2
        if i:
            c.line(cx, y0, cx, r3)
        c.setFont("Helvetica", 6)
        c.drawString(cx + 5, r3 - 9, label)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(cx + 5, y0 + 6, value)


def draw_rev_table(c, meta):
    w, h = 3.6 * inch, 0.62 * inch
    x0, y0 = PAGE_W - MARGIN - w, PAGE_H - MARGIN - h
    hairline(c, 0.9)
    c.rect(x0, y0, w, h)
    header_y = y0 + h - 0.2 * inch
    c.line(x0, header_y, x0 + w, header_y)
    widths = [0.45, 1.95, 0.75, 0.45]
    labels = ["REV", "DESCRIPTION", "DATE", "BY"]
    cx = x0
    c.setFont("Helvetica", 6)
    for wd, label in zip(widths, labels):
        c.drawString(cx + 4, header_y + 5, label)
        cx += wd * inch
        if label != labels[-1]:
            c.line(cx, y0, cx, y0 + h)
    row = [meta["rev"], meta["rev_desc"], meta["date"], meta["initials"]]
    cx = x0
    c.setFont("Helvetica", 7)
    for wd, value in zip(widths, row):
        c.drawString(cx + 4, y0 + h - 0.34 * inch, value)
        cx += wd * inch


def draw_third_angle_symbol(c, x, y):
    # truncated-cone third-angle projection symbol
    hairline(c, 0.9)
    c.circle(x + 0.14 * inch, y, 0.065 * inch)
    c.circle(x + 0.14 * inch, y, 0.115 * inch)
    x1 = x + 0.34 * inch
    c.lines([(x1, y - 0.115 * inch, x1 + 0.3 * inch, y - 0.065 * inch),
             (x1, y + 0.115 * inch, x1 + 0.3 * inch, y + 0.065 * inch),
             (x1, y - 0.115 * inch, x1, y + 0.115 * inch),
             (x1 + 0.3 * inch, y - 0.065 * inch, x1 + 0.3 * inch, y + 0.065 * inch)])
    c.setFont("Helvetica", 6)
    c.drawString(x, y - 0.26 * inch, "THIRD ANGLE PROJECTION")


def draw_notes(c, notes):
    x0, y0 = MARGIN + 0.18 * inch, MARGIN + 0.16 * inch
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(*INK)
    c.drawString(x0, y0 + 12 * len(notes) + 14, "GENERAL NOTES")
    c.setFont("Helvetica", 6.5)
    for i, note in enumerate(notes):
        y = y0 + 12 * (len(notes) - i)
        c.drawString(x0, y, f"{i + 1}.  {note}")
    draw_third_angle_symbol(c, x0 + 0.05 * inch, y0 - 0.02 * inch + 0.12 * inch)


def draw_scale_bar(c, x, y, feet_per_inch):
    length = 2.0 * inch
    total_ft = 2 * feet_per_inch
    hairline(c, 0.8)
    c.setFont("Helvetica", 6)
    segments = 4
    for i in range(segments):
        sx = x + length * i / segments
        if i % 2 == 0:
            c.setFillColorRGB(*INK)
            c.rect(sx, y, length / segments, 4, fill=1)
        else:
            c.rect(sx, y, length / segments, 4, fill=0)
        c.setFillColorRGB(*INK)
        c.drawCentredString(sx, y - 8, str(int(total_ft * i / segments)))
    c.rect(x, y, length, 4)
    c.drawCentredString(x + length, y - 8, f"{int(total_ft)} FT")
    c.drawString(x + length + 0.12 * inch, y, f"GRAPHIC SCALE · 1 IN = {int(feet_per_inch)} FT")


def place_image(c, path, area):
    ax, ay, aw, ah = area
    img = ImageReader(path)
    iw, ih = img.getSize()
    scale = min(aw / iw, ah / ih)
    dw, dh = iw * scale, ih * scale
    x = ax + (aw - dw) / 2
    y = ay + (ah - dh) / 2
    c.drawImage(img, x, y, dw, dh, preserveAspectRatio=True, anchor="c")
    hairline(c, 0.5)
    c.rect(x, y, dw, dh)


def build(args, sheets, meta):
    c = canvas.Canvas(args.output, pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"{meta['project']} — {meta['rev']} CAD sheet set")
    for sheet in sheets:
        path = os.path.join(args.images_dir, sheet["image"])
        if not os.path.exists(path):
            print(f"skipping {sheet['number']}: missing {path}")
            continue
        draw_border(c)
        draw_title_block(c, meta, sheet)
        draw_rev_table(c, meta)
        draw_notes(c, meta["notes"] + sheet.get("notes", []))
        draw_scale_bar(c, MARGIN + 4.7 * inch, MARGIN + 0.28 * inch, sheet.get("fpi", 50))
        # drawing area above the notes / title block strip
        area = (MARGIN + 0.25 * inch, MARGIN + 1.85 * inch,
                PAGE_W - 2 * MARGIN - 0.5 * inch, PAGE_H - 2 * MARGIN - 2.75 * inch)
        place_image(c, path, area)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(*INK)
        c.drawString(MARGIN + 0.25 * inch, PAGE_H - MARGIN - 0.32 * inch, sheet["heading"])
        c.setFont("Helvetica", 7.5)
        c.drawString(MARGIN + 0.25 * inch, PAGE_H - MARGIN - 0.5 * inch, sheet["subheading"])
        c.showPage()
    c.save()
    print(f"wrote {args.output}")


def main():
    p = argparse.ArgumentParser(description="Compose CAD renders into a sheet-set PDF")
    p.add_argument("--images-dir", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--project", default="CALLER POWER GENERATION SOLUTIONS")
    p.add_argument("--drawn", default="STEPHAN HARDT")
    p.add_argument("--date", default="2026-08-31")
    p.add_argument("--rev", default="REV 89")
    args = p.parse_args()

    meta = {
        "project": args.project,
        "subtitle": "3x1 CCGT + MODULAR / BESS   ·   MODEL BASIS REV 89C   ·   SUPERSEDES SK-9",
        "drawn": args.drawn,
        "checked": "—",
        "date": args.date,
        "rev": args.rev,
        "rev_desc": "REISSUED — CAD LINEWORK SHEET SET",
        "initials": "".join(w[0] for w in args.drawn.split()[:2]),
        "status": "CONCEPT",
        "basis": "REV 89C GLB",
        "notes": [
            "ORTHOGRAPHIC PROJECTIONS EXTRACTED FROM THE REV 89C MODEL. HIDDEN LINES REMOVED.",
            "LINEWORK: SILHOUETTES, CREASES, BORDERS AND MATERIAL BOUNDARIES (FREESTYLE).",
            "RASTER SHEET — DO NOT SCALE FOR CONSTRUCTION. DIMENSIONS GOVERN FROM THE MODEL.",
        ],
    }
    sheets = [
        {"image": "hl_iso.png", "number": "SK-10 / 001",
         "title": "GENERAL ARRANGEMENT — ISOMETRIC",
         "heading": "GENERAL ARRANGEMENT · ISOMETRIC PROJECTION · HIDDEN LINE",
         "subheading": "True isometric (azimuth 45°, elevation 35.26°); full plant, turbine hall sectioned open",
         "scale": "NTS", "fpi": 50},
        {"image": "hl_plan.png", "number": "SK-10 / 002",
         "title": "GENERAL ARRANGEMENT — PLAN",
         "heading": "GENERAL ARRANGEMENT · PLAN · HIDDEN LINE",
         "subheading": "Orthographic plan projection; roofs as modelled, hall opening per Rev 89C",
         "scale": "NTS", "fpi": 50},
        {"image": "el_front.png", "number": "SK-10 / 003",
         "title": "ELEVATION — SOUTH",
         "heading": "SOUTH ELEVATION · HIDDEN LINE",
         "subheading": "Orthographic elevation looking north; grade at EL. 0'-0\"",
         "scale": "NTS", "fpi": 40},
        {"image": "el_right.png", "number": "SK-10 / 004",
         "title": "ELEVATION — EAST",
         "heading": "EAST ELEVATION · HIDDEN LINE",
         "subheading": "Orthographic elevation looking west; grade at EL. 0'-0\"",
         "scale": "NTS", "fpi": 40},
        {"image": "sh_iso.png", "number": "SK-10 / 005",
         "title": "SHADED MODEL VIEW — ISOMETRIC",
         "heading": "SHADED MODEL VIEW · ISOMETRIC · FEATURE EDGES",
         "subheading": "Materials as modelled under neutral studio light; black feature edges overlaid",
         "scale": "NTS", "fpi": 50},
        {"image": "bp_iso.png", "number": "SK-10 / 006",
         "title": "PRESENTATION — BLUEPRINT",
         "heading": "PRESENTATION SHEET · BLUEPRINT LINEWORK",
         "subheading": "White-on-blue presentation rendering of the isometric linework",
         "scale": "NTS", "fpi": 50},
    ]
    build(args, sheets, meta)


if __name__ == "__main__":
    main()
