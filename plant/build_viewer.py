#!/usr/bin/env python3
"""Inject sk3x1_model.json into viewer/template.html -> viewer/index.html."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "viewer", "template.html")).read()
data = open(os.path.join(HERE, "sk3x1_model.json")).read()
out = tpl.replace("/*MODEL_JSON*/null", data)
open(os.path.join(HERE, "viewer", "index.html"), "w").write(out)
print("wrote viewer/index.html", len(out), "bytes")
