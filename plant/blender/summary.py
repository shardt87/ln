#!/usr/bin/env python3
"""Markdown summary of a render run (used for the GitHub job summary)."""
import glob
import json
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "renders"
print("## SK-3X1 Rev 14 Blender renders\n")
print("| View | Style | Ortho fit (ft) | Margins L/R, T/B | Samples | Render (s) |")
print("|---|---|---|---|---|---|")
rows = []
for f in glob.glob(os.path.join(root, "manifest_*.json")):
    rows += json.load(open(f))
order = ["A", "B", "B2", "C", "H", "O1", "O2", "O3", "O4", "O5", "ALL"]
for v in sorted(rows, key=lambda v: (v["style"], order.index(v["k"]) if v["k"] in order else 99)):
    print(f"| {v['name']} | {v['style']} | {v['ortho_ft']:,} | {v['margin_lr']}%, {v['margin_tb']}% "
          f"| {v['samples']} | {v.get('seconds', '')} |")
print("\nDownload the **sk3x1-renders** artifact for the annotated PNGs, contact sheets, "
      "`SK-3X1_Rev14.blend` and the OBJ.")
