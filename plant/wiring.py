"""Wiring applications: every powered or instrumented item gets its cable applications and a
connection to the cable network.

1. Applications (item["wiring"]): from the equipment class, the cable applications it needs,
   each with its typical cable family (Southwire families named as the requested supplier;
   typical selection, not engineered):
   MV power, LV power, control, instrumentation, thermocouple extension, fire alarm, lighting /
   small power, data / fibre, grounding. Items in Class I Div 2 areas (gas yard, M&R, fuel-gas
   compressors, LNG, H2, gensets) take ARMOR-X MC-HL power and intrinsically safe
   instrumentation.
2. Feeders: an item no cable route reaches gets a buried feeder (duct bank for the base plant,
   MV / LV cable in the optional system's own route layer) from its nearest edge to the nearest
   point of the underground cable network, L-shaped. Items inside R1 are fed through the R1
   cable basement, the bridge crane from its conductor bar.
"""
import math
import re

ELEC = ("mv_tray", "lv_tray", "control_tray", "duct_bank", "mvlv_cable", "hv_cable", "hv_overhead", "ipb", "hmod",
        "cable_trench")
UNDER = ("duct_bank", "mvlv_cable")

MV = "MV power 13.8 / 4.16 kV: MV-105 EPR shielded, or ARMOR-X MC-HL MV-105 (ICEA S-93-639)"
LV = "LV power 480 V: Cu XHHW-2, Type TC-ER (UL 1277)"
LV_HAZ = "LV power 480 V, Class I Div 2: ARMOR-X MC-HL, Cu XHHW-2 with grounds (UL 2225)"
CTRL = "Control 120 V AC / 125 V DC: 14 AWG multiconductor, Type TC-ER (ICEA S-73-532)"
INST = "Instrumentation 4-20 mA / HART: shielded pairs / triads, Type TC-ER / PLTC"
INST_IS = "Instrumentation, intrinsically safe: shielded pairs, Type ITC / PLTC, blue jacket"
TCX = "Thermocouple extension, type KX (ANSI MC96.1 yellow)"
FA = "Fire alarm: FPLR shielded, red jacket (NEC 760)"
LIGHT = "Lighting, receptacles, small power: Cu THHN/THWN-2 in conduit (Southwire SIMpull; UL 83)"
DATA = "Data / DCS network: fibre optic (single-mode), orange jacket"
GND = "Grounding: bare Cu 4/0 to the station grid, green-insulated equipment grounds"
HT = "Heat tracing: self-regulating heat-trace circuits from the heat-trace panel"

HAZ = re.compile(r"gas yard|gas metering|regulation|filter-separator|performance heater|M&R|pig receiver|"
                 r"fuel-gas compressor|gas conditioning|ESD|LNG|H2 |hydrogen|genset|RICE|SC-\d|TM-\d|GEN-|"
                 r"MOB-|CONT-\d|MT-\d|ULSD|fuel|blending|condensate tank", re.I)
RULES = [   # (pattern, applications), first match wins
    (r"230 kV breaker|230 kV tie breaker|entrance: surge|CCVT", ["ctrl", "inst", "gnd"]),     # CT / VT secondaries, trip / close, alarms
    (r"transformer|step-up|GSU|UAT|CCS T-\d|T4-|LCT-|T-R\d|T-MOD|T-H2|MPT|rectifier", ["mv", "ctrl", "inst", "gnd"]),
    (r"data hall|electrical gallery|switchgear|e-house|PCM|MCC|load-centre|EMS|SCADA|cubicle|board|PDC", ["mv", "lv", "ctrl", "data", "fa", "light",
                                                                            "gnd"]),
    (r"BFP|boiler feed|CO2 compression|export compressor|circulating-water pump|fuel-gas compressors|"
     r"boil-off|CW pumps", ["mv", "ctrl", "inst", "gnd"]),
    (r"genset|diesel generator|EDG-|RICE|SC-\d|TM-\d|GEN-|MOB-|CONT-\d|MT-\d|FC-\d|fuel-cell|SOFC|BESS|black-start",
     ["mv", "lv", "ctrl", "inst", "tcx", "data", "fa", "gnd"]),
    (r"Comms tower", ["lv", "data", "light", "gnd"]),               # radio / microwave, aviation light
    (r"CEMS|analy|SWAS|metering|gas quality|EMS", ["lv", "inst", "data", "light", "gnd"]),
    (r"F&G|building|house|shelter|warehouse|workshop|gatehouse|control room|admin", ["lv", "ctrl", "light", "fa", "data",
                                                                               "gnd"]),
    (r"tank|dike|sump|separator", ["lv", "inst", "ht", "gnd"]),
    (r"instrument air|reclaimer|storage|damper|filter|pump|fan|blower|compressor|cooler|chiller|tower|heater|skid|vaporizer|crane|hoist|valve|station|filter|"
     r"electrolyzer|purification|dryer|scrubber|DCC|absorber|stripper|reboiler|exchanger",
     ["lv", "ctrl", "inst", "gnd"]),
]
TEXT = {"mv": MV, "lv": LV, "ctrl": CTRL, "inst": INST, "tcx": TCX, "fa": FA, "light": LIGHT, "data": DATA,
        "gnd": GND, "ht": HT}
SKIP = re.compile(r"pad\b|lane|road|corridor|apron|landing|laydown|floor|deck|foundation|^Common turbine hall|"
                  r"stack \(|breeching|transition duct|exhaust duct|inlet duct|dead-end|bus \d|(?<!Comms )(?<!cooling )(?<!chilling )tower \(|monopole|"
                  r"Pipe |Cable trays|fence|compound|containment dike|right of way|future|reserved", re.I)


def applications(it):
    name = it["name"]
    for pat, apps in RULES:
        if re.search(pat, name, re.I):
            out = []
            haz = bool(HAZ.search(name))
            for a in apps:
                if a == "lv" and haz:
                    out.append(LV_HAZ)
                elif a == "inst" and haz:
                    out.append(INST_IS)
                else:
                    out.append(TEXT[a])
            return out
    return None


def _near(it, p, t=15):
    f = it["fp"]
    return f[0] - t <= p[0] <= f[1] + t and f[2] - t <= p[1] <= f[3] + t


def _passes(it, segs, t=15):
    """A cable route passes within t of the item (a trench or tray running past it)."""
    f = it["fp"]
    return any(min(a[0], b[0]) - t <= f[1] and max(a[0], b[0]) + t >= f[0] and
               min(a[1], b[1]) - t <= f[3] and max(a[1], b[1]) + t >= f[2] for a, b in segs)


def _closest_on_seg(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return (ax + t * dx, ay + t * dy)


def route_layer(it, layers):
    if it["layer"].startswith("OPT_"):
        cand = it["layer"] + "_ROUTES"
        if cand in layers:
            return cand
        return "OPT_MOD_ROUTES"
    return "ROUTES_BASE"


def build(items, routes, layers, add_route):
    ends = [(p, r["type"]) for r in routes if r["type"] in ELEC for p in (r["points"][0], r["points"][-1])]
    segs = [(a, b) for r in routes if r["type"] in ELEC for a, b in zip(r["points"], r["points"][1:])]
    n_feed, n_apps = 0, 0
    for it in list(items):
        if not it.get("register") or (it["layer"] == "SITE" and not it["name"].startswith("Gatehouse")) or it["z"][1] < 1 or SKIP.search(it["name"]):
            continue
        apps = applications(it)
        if not apps:
            continue
        it["wiring"] = apps
        n_apps += 1
        if it["layer"] == "R1_INTERIOR":
            it["wiring"] = apps + ["Fed inside R1 through the cable basement"]
            continue
        if it["tag"] == "CRANE":
            it["wiring"] = apps + ["Fed from the crane conductor bar along the runway girder"]
            continue
        if any(_near(it, p) for p, t in ends) or _passes(it, segs):
            continue
        # nearest point of the underground cable network, own system first
        lay = route_layer(it, layers)
        f = it["fp"]
        cx, cy = (f[0] + f[1]) / 2, (f[2] + f[3]) / 2
        best = None
        for pref in (True, False):
            for r in routes:
                if r["type"] not in UNDER or r is None:
                    continue
                if pref and r["layer"] != lay:
                    continue
                for a, b in zip(r["points"], r["points"][1:]):
                    q = _closest_on_seg((cx, cy), a, b)
                    d = math.hypot(q[0] - cx, q[1] - cy)
                    if best is None or d < best[0]:
                        best = (d, q)
            if best and best[0] < 700:
                break
        if best is None:
            continue
        tx, ty = best[1]
        # start on the item's edge facing the target, then an L to the network
        sx = min(max(tx, f[0]), f[1])
        sy = min(max(ty, f[2]), f[3])
        if f[0] < tx < f[1]:
            sy = f[2] if ty < cy else f[3]
        elif f[2] < ty < f[3]:
            sx = f[0] if tx < cx else f[1]
        pts = [(round(sx, 1), round(sy, 1))]
        if abs(sx - tx) > .5 and abs(sy - ty) > .5:
            pts.append((round(tx, 1), round(sy, 1)))
        pts.append((round(tx, 1), round(ty, 1)))
        if len(pts) < 2 or pts[0] == pts[-1]:
            continue
        rtype = "duct_bank" if lay == "ROUTES_BASE" else "mvlv_cable"
        add_route(rtype, pts, lay, sheet="typical (wiring applications)")
        routes[-1]["cables"] = apps
        routes[-1]["label"] = ("Duct bank (underground)" if rtype == "duct_bank" else routes[-1]["label"])
        ends.append((pts[0], rtype))
        n_feed += 1
    return n_apps, n_feed


# applications for items the generic rules miss (applied last, by name)
OVERRIDES = [
    (r"^HRSG \d \+ SCR", [MV + " (BFP and recirculation motors via R2)", LV + " (MOVs, drain valves, SCR / NH3 skid, platform lighting)",
                         CTRL + " (drum-level, attemperator, blowdown, MOV control)", INST + " (drum level, pressure, flow, O2 / NOx)",
                         TCX + " (tube-metal and gas-path thermocouples)", HT + " (freeze protection)", LIGHT, GND]),
    (r"^Air-cooled condenser", [MV + " (fan VFD outputs from R4)", LV + " (gearbox oil heaters, deck lighting)",
                                CTRL + " (fan sequencing, vacuum control)", INST + " (vibration switches, condensate T, backpressure)",
                                HT + " (condensate drain and riser heat trace)", GND]),
    (r"^HTP-\d: heat-trace panel", [LV + " (panel supply)", HT + " (self-regulating heat-trace circuits)",
                                    CTRL + " (circuit monitoring, alarm to DCS)", GND]),
    (r"^Chemical feed$", [LV + " (metering pumps, mixers)", CTRL, INST + " (tank level, dosing flow)", GND]),
    (r"^Wastewater treatment$", [LV + " (mixers, clarifier drive, pumps, filter press)", CTRL, INST + " (pH, level, turbidity)",
                                 LIGHT, GND]),
    (r"^Auxiliary boiler$", [LV + " (FD fan, feedwater pumps)", CTRL + " (burner management system, flame scanners)",
                             INST + " (drum level, steam pressure)", FA + " (fuel-gas detection)", GND]),
    (r"^Gas yard local control enclosure", [LV, CTRL, INST_IS + " (field instruments in the gas yard)", DATA, GND]),
    (r"^CONDITIONAL: backup fuel oil \(ULSD\) unloading", [LV_HAZ + " (unloading and forwarding pumps)", CTRL,
                                                          INST + " (level, flow, leak detection)", GND]),
    (r"^M&R 1: pig receiver", [INST_IS + " (pig signaller, pressure)", GND]),
    (r"^M&R 5: ultrasonic meters", [INST_IS + " (meter heads, pressure, temperature)", DATA + " (flow computers)", GND]),
    (r"^230 kV switchyard \(gravel\)", ["Ground grid: bare Cu 4/0 mesh with ground rods, bonded to every structure",
                                        LIGHT + " (yard floodlighting)", GND]),
    (r"^Aqueous ammonia \(SC units\)", [LV + " (forwarding pumps)", INST + " (tank level, NH3 detection)", GND]),
    (r"^GSP-\d: generator breaker", [CTRL + " (trip / close, protection)", "CT / VT secondaries: 10 AWG, Type TC-ER", GND]),
    (r"^PIC: portable input cabinet", [LV + " (portable generator tails: Type W / SOOW single conductors)", GND]),
    (r"^LB: commissioning load bank", [LV + " (Type W / SOOW single conductors)", CTRL, GND]),
    (r"^H2 28: N2 purge supply", [INST + " (pressure, purge flow)", CTRL + " (purge valve control)", GND]),
]


def apply_overrides(items):
    n = 0
    for it in items:
        for pat, apps in OVERRIDES:
            if re.search(pat, it["name"]):
                it["wiring"] = apps
                n += 1
    return n
