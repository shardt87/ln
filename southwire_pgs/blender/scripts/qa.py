"""Automated delivery checks (run after render_views.py and pages.py).

    python3 qa.py
Checks: renders + callout anchors in frame, page text fits its boxes, no
unsupported claims in page copy, every PDF/PPTX/.blend opens, page count.
"""
import os
import re
import sys
import json
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
from content import PAGES, COMMON  # noqa: E402

BANNED = [r"\d+\s*%", r"\bpercent", r"\bcertif", r"\bUL\b", r"\bcompliant\b", r"\bsav(e|es|ing|ings)\b",
          r"\breduc", r"\bfaster\b", r"\bguarantee", r"\bpartner(ed)? with\b", r"\bagreed to\b",
          r"\bqualified\b(?! Southwire products)", r"lead[- ]time", r"\bcheaper\b", r"\bcost\b"]

problems = []
# 1 renders + callouts
for p in PAGES:
    j = os.path.join(ROOT, "renders", "clean", p["view"] + ".json")
    if not os.path.exists(j):
        problems.append(f"missing render {p['view']}")
        continue
    m = json.load(open(j))
    if len(m["callouts"]) != 3:
        problems.append(f"{p['key']}: {len(m['callouts'])} callouts")
    for c in m["callouts"]:
        if not c["in_frame"]:
            problems.append(f"{p['key']}: callout {c['n']} anchor out of frame")
    for f in (p["view"] + ".png", p["view"] + "_alpha.png"):
        if not os.path.exists(os.path.join(ROOT, "renders", "clean", f)):
            problems.append(f"missing {f}")
    if not os.path.exists(os.path.join(ROOT, "renders", "annotated", p["view"] + ".png")):
        problems.append(f"missing annotated {p['view']}")
# 2 copy checks
for p in PAGES:
    text = " ".join([p["headline"], p["support"], " ".join(p["callouts"]), " ".join(p["statements"]), p["next"]])
    for b in BANNED:
        if re.search(b, text, re.I):
            problems.append(f"{p['key']}: copy matches /{b}/")
for k in ("established", "proposed", "disclaimer"):
    for b in BANNED[:4]:
        if re.search(b, COMMON[k], re.I) and k != "disclaimer":
            problems.append(f"common {k} matches /{b}/")
# 3 files open
import pymupdf  # noqa: E402
from pptx import Presentation  # noqa: E402
pdfs = sorted(glob.glob(os.path.join(ROOT, "pages", "pdf", "*.pdf")))
for f in pdfs:
    d = pymupdf.open(f)
    exp = len(PAGES) + 1 if f.endswith("All_one_pagers.pdf") else 1
    if len(d) != exp:
        problems.append(f"{os.path.basename(f)}: {len(d)} pages (expected {exp})")
    r = d[0].rect
    if (round(r.width), round(r.height)) != (612, 792):
        problems.append(f"{os.path.basename(f)}: not US Letter")
    imgs = d[0].get_images()
    if not imgs:
        problems.append(f"{os.path.basename(f)}: no image")
pptxs = sorted(glob.glob(os.path.join(ROOT, "pages", "pptx", "*.pptx")))
for f in pptxs:
    prs = Presentation(f)
    exp = len(PAGES) + 1 if f.endswith("All_one_pagers.pptx") else 1
    if len(prs.slides) != exp:
        problems.append(f"{os.path.basename(f)}: {len(prs.slides)} slides")
print(f"PDFs: {len(pdfs)}  PPTX: {len(pptxs)}")
blend = os.path.join(ROOT, "blender", "Southwire_PGS_Master.blend")
try:
    import bpy  # noqa: E402
    bpy.ops.wm.open_mainfile(filepath=blend)
    sc = bpy.context.scene
    views = json.loads(sc["sw_views"])
    need = ["Generator", "Switchgear", "Control_Wiring", "Power_Cables", "Grounding", "Ehouse", "Cable_Tray",
            "Transformer", "Temporary_Power", "Assembly_Kit", "Annotations", "Cameras", "Lighting"]
    miss = [c for c in need if c not in bpy.data.collections]
    if miss:
        problems.append(f"blend missing collections {miss}")
    cams = [o for o in bpy.data.objects if o.type == "CAMERA"]
    print(f".blend: {len(bpy.data.objects)} objects, {len(bpy.data.collections)} collections, "
          f"{len(cams)} cameras, {len(views)} views, {len(bpy.data.materials)} materials")
    for v in views.values():
        if v["camera"] not in bpy.data.objects:
            problems.append(f"camera missing {v['camera']}")
except ImportError:
    print("bpy not available - .blend not checked")
print("PROBLEMS:" if problems else "ALL CHECKS PASSED")
for p in problems:
    print("  -", p)
