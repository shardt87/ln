#!/usr/bin/env python3
"""Inject the model, palette and verification report into
viewer/template.html -> viewer/index.html.

The coastal variant A (sheet SK-3X1-15: onshore LNG import terminal, jetty,
berth and carrier) is merged in as its own layer group with a sea layer and a
'Coastal: LNG terminal' view; it is off in the other views."""
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "viewer", "template.html")).read()
model = json.load(open(os.path.join(HERE, "sk3x1_model.json")))
ov = json.load(open(os.path.join(HERE, "coastal", "sk3x1_coastal_A.json")))
meta = ov["coastal"]
model["layers"].update(ov["layers"])
model["layers"]["COASTAL_SEA"] = dict(label="A Sea and shoreline", group="Coastal (sheet 15)")
model["items"] += ov["items"]
model["parts"] += ov["parts"]
model["coastal"] = meta
coast = [l for l, v in model["layers"].items() if v["group"].startswith("Coastal")]
for v in model["views"]:
    v["show"] = [l for l in v["show"] if l not in coast]
full = next(v for v in model["views"] if v["k"] == "ALL")
model["views"].append(dict(k="COAST", n="Coastal: LNG terminal",
                           show=[l for l in full["show"] if not l.startswith("OPT_LNG")] + coast,
                           t=[3500, 1000, 20], c=[1300, -2900, 2900]))
for key, data in (("MODEL", json.dumps(model, separators=(",", ":"))),
                  ("PALETTE", open(os.path.join(HERE, "palette.json")).read()),
                  ("REPORT", open(os.path.join(HERE, "verify_report.json")).read())):
    tpl = tpl.replace(f"/*{key}_JSON*/null", data)
open(os.path.join(HERE, "viewer", "index.html"), "w").write(tpl)
print("wrote viewer/index.html", len(tpl), "bytes;", len(ov["items"]), "coastal items merged")
