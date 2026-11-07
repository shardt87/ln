"""Recompute the HRSG 1 train totals in brochure/boiler_numbers.json from the Cable Schedule sheet (same train filter
as blender/deck_boilers.py: HRSG 1, its feed pumps, SCR blowers, chemical feed, blowdown, CEMS, stack, duct burner).
Run after cable_schedule.py. The auxiliary-boiler block is left as it is.

    python3 tools/boiler_numbers.py
"""
import json
import math
import os
import re

import openpyxl

PLANT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN = r"HRSG[- ]1\b|BFP-1|SCRB-1|CEMS-1|STK-1|HRSG 1 "
SKIP = r"T-R2A"                                       # the e-house supply legs are shown separately on the slides
wb = openpyxl.load_workbook(os.path.join(PLANT, "brochure", "SW-3X1_Cable_Schedule_and_BOM.xlsx"), read_only=True)
out = dict(runs=0, cables=0, ft=0, classes={}, products={})
for r in list(wb["Cable Schedule"].iter_rows(values_only=True))[1:]:
    ends = " ".join(str(r[k]) for k in (4, 5, 6, 7))
    if not re.search(TRAIN, ends) or re.search(SKIP, ends) or (r[4] == "R2A" and r[6] == "R2A"):
        continue
    n = r[13] * r[14]
    ft = math.ceil(((r[19] or 0) + (r[20] or 0) + 20) * 1.1 / 10) * 10 * n
    out["runs"] += 1
    out["cables"] += n
    out["ft"] += ft
    c = out["classes"].setdefault(r[8], dict(cables=0, ft=0))
    c["cables"] += n
    c["ft"] += ft
    out["products"][r[9]] = out["products"].get(r[9], 0) + ft
p = os.path.join(PLANT, "brochure", "boiler_numbers.json")
N = json.load(open(p))
N["hrsg"] = out
json.dump(N, open(p, "w"), indent=1)
print("HRSG train:", out["runs"], "runs,", out["cables"], "cables,", out["ft"], "ft")
