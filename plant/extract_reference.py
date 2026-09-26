#!/usr/bin/env python3
"""Extract reference geometry from the SK-3X1 Rev 14 drawing PDF.

Writes reference/sk3x1_rev14_reference.json, which verify.py checks the
model against. Needs PyMuPDF (pip install pymupdf) and the drawing set:

    python3 plant/extract_reference.py path/to/SK-3X1_Drawing_Set_Rev14.pdf

The JSON is committed, so verify.py runs without the PDF.
"""
import json
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))


def col(c):
    return None if c is None else "#%02x%02x%02x" % tuple(int(255 * v) for v in c)


def sheet01(page):
    # Sheet 01 plan frame = the 2,420 x 1,920 ft compound.
    x0, y1 = 39.9305, 720.0472
    s = 2420 / (816.8695 - 39.9305)
    X = lambda v: round((v - x0) * s, 1)
    Y = lambda v: round((y1 - v) * s, 1)
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.x0 < 38 or r.x1 > 818 or r.y0 < 100 or d.get("fill") is None:
            continue
        kinds = "".join(i[0] for i in d["items"])
        if kinds not in ("re", "cccccccc"):
            continue  # riser triangles, section hatching
        stroke = col(d.get("color"))
        if stroke in ("#c0692a", "#27313a"):
            continue  # area badges and road-crossing symbols
        rects.append(dict(x=[X(r.x0), X(r.x1)], y=[Y(r.y1), Y(r.y0)],
                          shape="circle" if kinds.startswith("c") else "rect",
                          fill=col(d.get("fill"))))
    return rects


def sheet05(page):
    # R1 floor plan, rotated: plant north to the right, east wall at the top.
    k = (803.76 - 69.36) / 180
    Y = lambda px: round(600 + (px - 69.36) / k, 1)
    X = lambda py: round(474 - (py - 146.52) / k, 1)
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        if not (60 < r.x0 < 810 and 140 < r.y0 < 420) or d.get("fill") is None:
            continue
        if r.width < 3 and r.height < 3:
            continue
        rects.append(dict(x=[X(r.y1), X(r.y0)], y=[Y(r.x0), Y(r.x1)], fill=col(d.get("fill"))))
    return rects


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else "SK-3X1_Drawing_Set_Rev14.pdf"
    doc = pymupdf.open(pdf)
    ref = dict(source=os.path.basename(pdf), sheet01_rects=sheet01(doc[0]),
               sheet05_rects=sheet05(doc[4]))
    out = os.path.join(HERE, "reference", "sk3x1_rev14_reference.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(ref, open(out, "w"), indent=0)
    print(f"wrote {out}: {len(ref['sheet01_rects'])} sheet-01 shapes, "
          f"{len(ref['sheet05_rects'])} sheet-05 shapes")


if __name__ == "__main__":
    main()
