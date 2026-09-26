#!/usr/bin/env python3
"""Assemble the GitHub Pages site: viewer (index), GT1 bay scene, render gallery."""
import glob
import html
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else "site"
os.makedirs(out, exist_ok=True)

# viewer: the artifact page is a body fragment; give it a full document
body = open(os.path.join(ROOT, "viewer", "index.html")).read()
open(os.path.join(out, "index.html"), "w").write(
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<style>[hidden]{display:none!important}</style>\n</head>\n<body>\n' + body + "\n</body>\n</html>\n")

for f in ("bay.html", "gt1_bay.json", "gt1_bay_scene.js"):
    shutil.copy(os.path.join(ROOT, "threejs", f), os.path.join(out, f))

# render gallery
os.makedirs(os.path.join(out, "renders"), exist_ok=True)
imgs = sorted(glob.glob(os.path.join(ROOT, "renders", "blender", "*_annotated.jpg")))
for f in imgs + glob.glob(os.path.join(ROOT, "renders", "blender", "contact_sheet_*.jpg")):
    shutil.copy(f, os.path.join(out, "renders", os.path.basename(f)))
cards = "\n".join(
    f'<figure><a href="renders/{os.path.basename(f)}"><img loading="lazy" src="renders/{os.path.basename(f)}" '
    f'alt="{html.escape(os.path.basename(f))}"></a><figcaption>{html.escape(os.path.basename(f)[:-14].replace("_", " · "))}'
    f'</figcaption></figure>' for f in imgs)
rep = json.load(open(os.path.join(ROOT, "verify_report.json")))
s = rep["summary"]
open(os.path.join(out, "renders.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SK-3X1 Renders</title>
<style>
body{{margin:0;background:#eef0ee;color:#1f2b33;font:14px/1.45 Arial,sans-serif}}
main{{max-width:1500px;margin:0 auto;padding:16px}}
h1{{font-size:24px;margin:8px 0 4px}} p{{color:#55636c;margin:0 0 14px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}}
@media (max-width:480px){{.g{{grid-template-columns:1fr}}}}
figure{{margin:0;background:#f8f9f7;border:1px solid #cfd5d4}} img{{width:100%;display:block}}
figcaption{{padding:6px 10px;font-size:12.5px;text-transform:uppercase;letter-spacing:.5px}}
a{{color:#b0662b}}
</style></head><body><main>
<h1>SK-3X1 Rev 14: Blender renders</h1>
<p>Sheet-11 views rendered with Cycles. Model: {s['items']} items, {s['parts']} parts, verified against the drawing
({'PASS' if s['ok'] else 'FAIL'}). <a href="./">3D viewer</a> · <a href="bay.html">GT1 bay close-up</a></p>
<div class="g">{cards}</div></main></body></html>""")
print(f"site assembled in {out}: viewer, bay scene, {len(imgs)} renders")
