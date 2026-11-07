"""Typical cable take-off for the two Boiler Row showcase boilers (boiler_row.py), written to brochure/boiler_numbers.json
as "ub" (UB-1 utility gas boiler, 300 MW class, boiler + its STG island) and "eb" (EB-1 30 MW electrode boiler).

They are not in the SW-3X1 cable schedule (the plant totals stay as they are). Counts are a typical device list for a
unit of that size, not an engineered schedule; lengths are measured on the model layout from each load to its source
(plant switchgear R1 for the 13.8 kV feeders, the unit e-houses for the rest). Footage uses the plant rule:
(route + 20 ft terminations) x 1.1, rounded up to 10 ft, times the number of cables.

    python3 tools/boiler_row_numbers.py
"""
import json
import math
import os

PLANT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (class, product, what, cables, route ft)
UB = [
    ("MV 15 kV", "MV-105 15 kV 1/C 500 kcmil", "FD fans A/B, 13.8 kV motors (1 set of 3 each)", 6, 380),
    ("MV 15 kV", "MV-105 15 kV 1/C 750 kcmil", "boiler feed pumps A/B, 13.8 kV (2 sets of 3 each)", 12, 420),
    ("MV 15 kV", "MV-105 15 kV 1/C 500 kcmil", "condensate pumps A/B, 4.16 kV (1 set of 3 each)", 6, 460),
    ("MV 15 kV", "MV-105 15 kV 1/C 750 kcmil", "unit station-service transformer primaries (2 sets of 3, x2)", 12, 300),
    ("LV 600 V", "Type TC-ER 600 V 3/C + G", "480 V motors, valve actuators, heaters, HVAC", 120, 380),
    ("Control", "Control cable 600 V Type TC-ER #14", "DCS control, interlocks, MCC starters", 380, 440),
    ("Control", "ARMOR-X MC-HL 600 V (Class I Div 2)", "burner management: 12 burners x scanner, igniter, valves, "
                                                        "position switches; gas-train SSOVs and vent", 92, 330),
    ("Instrumentation", "Instrumentation PLTC #18 shielded pairs", "pressure, flow, level, drum, O2, analyzers", 900, 480),
    ("Instrumentation", "Thermocouple extension, type K", "furnace, superheater, reheater, metal temperatures", 250, 480),
    ("Instrumentation", "Instrumentation PLTC #18 shielded pairs", "CEMS shelter at the stack (same as the HRSG shelter)", 31, 210),
    ("LV 600 V", "Type TC-ER 600 V 3/C + G #10", "stack aviation obstruction lights + failure alarm", 2, 520),
    ("Fibre / data", "Fibre optic, single-mode", "DCS ring, BMS, CEMS, STG controls", 12, 1400),
    ("Fire alarm", "Fire alarm FPLR 2/C #14", "boiler house, STG hall, burner front detectors", 20, 520),
]
EB = [
    ("MV 15 kV", "MV-105 15 kV 1/C 750 kcmil", "13.8 kV feeder, plant switchgear to the EB-1 e-house (3 sets of 3)", 9, 1050),
    ("MV 15 kV", "MV-105 15 kV 1/C 750 kcmil", "EB-1 breaker to the three boiler bushings (3 sets of 3)", 9, 90),
    ("LV 600 V", "Type TC-ER 600 V 3/C + G, VFD-rated", "circulation pumps, feedwater, aux transformer, HVAC, lighting", 10, 120),
    ("Control", "Control cable 600 V Type TC-ER #14", "PLC, breaker control, interlocks, electrode positioning", 24, 140),
    ("Instrumentation", "Instrumentation PLTC #18 shielded pairs", "pressure, level, conductivity, temperatures", 40, 140),
    ("Fibre / data", "Fibre optic, single-mode", "PLC to the plant DCS", 1, 1100),
    ("Ground", "Bare copper 4/0 AWG", "vessel, e-house and cable-shield grounding", 4, 220),
]


def total(rows):
    out = dict(runs=0, cables=0, ft=0, classes={}, rows=[])
    for cls, prod, what, n, l in rows:
        ft = math.ceil((l + 20) * 1.1 / 10) * 10 * n
        out["runs"] += 1
        out["cables"] += n
        out["ft"] += ft
        c = out["classes"].setdefault(cls, dict(cables=0, ft=0))
        c["cables"] += n
        c["ft"] += ft
        out["rows"].append(dict(cls=cls, product=prod, what=what, cables=n, ft=ft))
    return out


p = os.path.join(PLANT, "brochure", "boiler_numbers.json")
N = json.load(open(p))
N["ub"], N["eb"] = total(UB), total(EB)
json.dump(N, open(p, "w"), indent=1)
for k in ("aux", "ub", "eb"):
    print(k, N[k]["cables"], "cables,", N[k]["ft"], "ft;",
          {c: v["ft"] for c, v in N[k]["classes"].items()})
