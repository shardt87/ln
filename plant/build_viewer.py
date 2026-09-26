#!/usr/bin/env python3
"""Inject the model, palette and verification report into
viewer/template.html -> viewer/index.html."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "viewer", "template.html")).read()
for key, fname in (("MODEL", "sk3x1_model.json"), ("PALETTE", "palette.json"), ("REPORT", "verify_report.json")):
    tpl = tpl.replace(f"/*{key}_JSON*/null", open(os.path.join(HERE, fname)).read())
open(os.path.join(HERE, "viewer", "index.html"), "w").write(tpl)
print("wrote viewer/index.html", len(tpl), "bytes")
