#!/usr/bin/env python3
"""Tile the annotated renders into one contact sheet per style.

    python3 plant/blender/contact_sheet.py plant/renders/blender
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "renders", "blender")
ORDER = ["A", "B", "B2", "C", "H", "O1", "O2", "O3", "O4", "O5"]
for style in ("drawing", "photo"):
    files = [os.path.join(root, f"{k}_{style}_annotated.png") for k in ORDER]
    files = [f for f in files if os.path.exists(f)]
    if not files:
        continue
    thumbs = [Image.open(f).convert("RGB") for f in files]
    tw = 960
    thumbs = [t.resize((tw, int(t.height * tw / t.width)), Image.LANCZOS) for t in thumbs]
    cols = 2
    th = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    gap = 12
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * th + (rows + 1) * gap), (238, 240, 238))
    for i, t in enumerate(thumbs):
        x, y = gap + (i % cols) * (tw + gap), gap + (i // cols) * (th + gap)
        sheet.paste(t, (x, y))
        ImageDraw.Draw(sheet).rectangle((x - 1, y - 1, x + tw, y + t.height), outline=(207, 213, 212))
    out = os.path.join(root, f"contact_sheet_{style}.png")
    sheet.save(out, optimize=True)
    print("wrote", out, f"({len(thumbs)} views)")
