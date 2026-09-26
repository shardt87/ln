#!/usr/bin/env python3
"""Build the SK-3X1 Rev 14 3D coordinate model.

Source: "SK-3X1 Drawing Set Rev 14" (3x1 combined-cycle plant, 16 sheets).
Plan coordinates (X east, Y north, feet, origin at the SW corner of the
2,420 x 1,920 ft compound) were recovered from the vector geometry of sheets
SK-3X1-01 (base site) and SK-3X1-02 (optional systems). Elevations come from
SK-3X1-09 (hall section), SK-3X1-12 (dimension review) and SK-3X1-13 (height
comparison). Items with no stated height use typical values and are tagged
basis="typical".

Output: sk3x1_model.json, consumed by render.go (ln line art), the Three.js
viewer (viewer/index.html) and export_obj.py.

Conceptual illustration. Not engineered. Not for construction.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

objects = []
counts = {}


def _id(prefix):
    counts[prefix] = counts.get(prefix, 0) + 1
    return f"{prefix}-{counts[prefix]:03d}"


def box(layer, name, x0, x1, y0, y1, z0, z1, *, tag=None, color="equip",
        info="", basis="drawing", sheet="SK-3X1-01"):
    objects.append(dict(id=_id(layer), kind="box", layer=layer, name=name,
                        tag=tag or "", min=[x0, y0, z0], max=[x1, y1, z1],
                        color=color, info=info, basis=basis, sheet=sheet))


def cyl(layer, name, cx, cy, r, z0, z1, *, tag=None, color="equip", info="",
        basis="drawing", sheet="SK-3X1-01", axis="z"):
    """Cylinder. axis='z' vertical; axis='x'/'y' horizontal, centred at z0..z1 midpoint."""
    objects.append(dict(id=_id(layer), kind="cyl", layer=layer, name=name,
                        tag=tag or "", center=[cx, cy], r=r, z0=z0, z1=z1,
                        axis=axis, color=color, info=info, basis=basis,
                        sheet=sheet))


def hcyl(layer, name, x0, x1, y0, y1, zc, r, **kw):
    """Horizontal cylinder spanning a plan rectangle along its long side."""
    along = "x" if (x1 - x0) >= (y1 - y0) else "y"
    objects.append(dict(id=_id(layer), kind="hcyl", layer=layer, name=name,
                        tag=kw.pop("tag", ""), min=[x0, y0, zc - r],
                        max=[x1, y1, zc + r], r=r, axis=along,
                        color=kw.pop("color", "equip"), info=kw.pop("info", ""),
                        basis=kw.pop("basis", "drawing"),
                        sheet=kw.pop("sheet", "SK-3X1-01")))


def prism(layer, name, x0, x1, y0, y1, z0, z1, *, ridge="y", **kw):
    """Gable / A-frame prism (ACC streets). Ridge runs along `ridge`."""
    objects.append(dict(id=_id(layer), kind="prism", layer=layer, name=name,
                        tag=kw.pop("tag", ""), min=[x0, y0, z0],
                        max=[x1, y1, z1], ridge=ridge,
                        color=kw.pop("color", "equip"), info=kw.pop("info", ""),
                        basis=kw.pop("basis", "drawing"),
                        sheet=kw.pop("sheet", "SK-3X1-01")))


def pad(layer, name, x0, x1, y0, y1, color="pad", z1=0.5, **kw):
    box(layer, name, x0, x1, y0, y1, 0, z1, color=color, **kw)


# ---------------------------------------------------------------------------
# SITE: compound, fence, roads (SK-3X1-01)
# ---------------------------------------------------------------------------
L = "SITE"
pad(L, "Compound (2,420 x 1,920 ft, 107 acres)", 0, 2420, 0, 1920, color="ground",
    z1=0.0, info="Compound unchanged since Rev 06. Base plant about 43 acres; "
    "construction laydown is on temporary land outside the fence.")
for (x0, x1, y0, y1, n) in [
    (0, 2400, 270, 300, "30 ft access road"),
    (370, 400, 300, 1675, "West spine road"),
    (1460, 1490, 270, 1400, "East spine road"),
    (370, 1490, 900, 930, "30 ft ring road"),
    (370, 2400, 1370, 1400, "30 ft utilities road"),
    (400, 1500, 1650, 1675, "30 ft road (reserved for CCS utilities)"),
    (1490, 2400, 1650, 1675, "30 ft fuel road (LNG trucks)"),
    (1950, 1975, 1400, 1650, "Fuel-yard link road"),
    (484, 508, 560, 830, "24 ft lane (turbine hall west)"),
]:
    pad(L, n, x0, x1, y0, y1, color="road", z1=0.3)
pad(L, "Removal apron (GT / generator / ST removal)", 400, 480, 410, 560,
    color="road", z1=0.3, sheet="SK-3X1-10",
    info="Opens to the ring road; equipment leaves the laydown bay through "
    "the west door onto a trailer.")
# fence (thin walls, 8 ft)
for (x0, x1, y0, y1) in [(0, 2420, 0, 1), (0, 2420, 1919, 1920), (0, 1, 0, 1920),
                         (2419, 2420, 0, 1920)]:
    box(L, "Perimeter fence (8 ft)", x0, x1, y0, y1, 0, 8, color="fence",
        basis="typical")
box(L, "Main gate", 0, 6, 272, 298, 0, 10, color="fence", basis="typical")

# ---------------------------------------------------------------------------
# BASE_POWER_BLOCK: turbine hall, GTs, ST, HRSGs, stacks (SK-3X1-01/03/09/10)
# ---------------------------------------------------------------------------
L = "BASE_POWER_BLOCK"
box(L, "Common turbine hall (main bay)", 480, 1100, 404, 560, 0, 101,
    tag="HALL", color="hall", sheet="SK-3X1-09",
    info="Covers all bays plus the laydown bay. Bridge-crane runway y 404-556, "
    "bridge travel EL 84-96, hook max EL 82, roof EL 98-101 (raised 6 ft in "
    "Rev 09 so the ST lift clears).")
box(L, "South inlet gallery (outside crane runway)", 480, 1100, 370, 404, 0, 60,
    tag="GALLERY", color="hall", sheet="SK-3X1-09",
    info="Roof EL 60. Houses GCBs and IPB; each bay has a monorail west to a "
    "door clear of the filter-house columns.")
box(L, "Laydown bay floor", 480, 560, 404, 556, 0, 1, color="pad",
    sheet="SK-3X1-10", info="GT, generator and ST components are lowered here and "
    "leave through the west door.")
box(L, "Turbine deck EL 20", 560, 1100, 404, 556, 0, 20, color="concrete",
    sheet="SK-3X1-12", info="GTs, generators, ST and skids sit on the EL 20 deck.")
for i, gx in enumerate([630, 790, 950], start=1):
    dx = gx - 630
    box(L, f"GT{i}: H-class gas turbine (60 Hz)", 617 + dx, 643 + dx, 455, 540, 20, 38,
        tag=f"GT{i}", color="machine", basis="vendor", sheet="SK-3X1-12",
        info="Siemens SGT6-8000H class engine about 34 x 14 x 14 ft; plan incl. "
        "plenum + diffuser 26 x 85 ft. GT top EL 38. Lifted height 18 ft.")
    box(L, f"GTG-{i}: GT generator", 622 + dx, 638 + dx, 410, 455, 20, 36,
        tag=f"GTG-{i}", color="machine", basis="typical", sheet="SK-3X1-04",
        info="21 kV (assumed), typical H2-cooled 350-450 MVA. 16 x 45 ft.")
    box(L, f"GT{i} lube oil / hydraulics / enclosure fans skid", 661 + dx, 675 + dx, 470, 505,
        20, 30, tag=f"GT{i} aux", sheet="SK-3X1-03",
        info="MCC-GT fed from R1 (LV-GTAUX).")
    box(L, f"FS-GT{i}: CO2 fire-suppression skid", 662 + dx, 674 + dx, 510, 534, 20, 28,
        tag=f"FS-GT{i}", sheet="SK-3X1-03",
        info="Detection, release and interlocks; 480 V + 24 V DC.")
    box(L, f"WASH-GT{i}: compressor water-wash skid", 584 + dx, 596 + dx, 475, 495, 20, 27,
        tag=f"WASH-GT{i}", sheet="SK-3X1-03")
    box(L, f"GT{i} inlet removable plenum spool", 643 + dx, 658 + dx, 440, 466, 23, 37,
        tag="spool", color="amber", sheet="SK-3X1-10",
        info="Removed before any GT lift (touches the GT lift column by design).")
    box(L, f"HRSG {i} + SCR (3P reheat, horizontal)", 595 + dx, 665 + dx, 600, 760, 0, 100,
        tag=f"HRSG-{i}", color="hrsg", sheet="SK-3X1-13",
        info="70 x 160 ft, EL 100 (501G HRSG ~70 ft; largest casing 85 ft). "
        "Boiler feed pumps and SCR blowers alongside.")
    box(L, f"HRSG {i} inlet transition duct", 605 + dx, 655 + dx, 560, 600, 12, 88,
        color="hrsg", sheet="SK-3X1-01", info="GT exhaust to HRSG.")
    cyl(L, f"HRSG {i} stack", 630 + dx, 790, 11, 0, 180, tag=f"STK-{i}",
        color="stack", sheet="SK-3X1-13",
        info="22 ft dia x 180 ft (US H-class filings: OCEC 149, Otay Mesa 160, "
        "Cosumnes 165, Smarr 180).")
    box(L, f"CEMS shelter HRSG {i}", 648 + dx, 664 + dx, 806, 820, 0, 12, tag="CEMS",
        sheet="SK-3X1-03")
    box(L, f"BFP-{i}A/B: boiler feed pumps (13.8 kV DOL)", 675 + dx, 708 + dx, 615, 660,
        0, 10, tag=f"BFP-{i}", color="motor", sheet="SK-3X1-03",
        info="2 pumps, 13.8 kV, MV breaker DOL, fed from R1 SWGR-13.8-"
        f"{i} via route MV-BFP-{i}.")
    box(L, f"SCRB-{i}A/B: SCR dilution-air blowers", 675 + dx, 700 + dx, 705, 725, 0, 8,
        tag=f"SCRB-{i}", color="motor", sheet="SK-3X1-03",
        info=f"480 V, MCC starter in R2{'ABC'[i-1]} (LV-SCR-{i}).")

box(L, "ST: steam turbine (HP/IP + LP), ACC plant", 1020, 1080, 460, 552, 20, 46,
    tag="ST", color="machine", basis="typical", sheet="SK-3X1-12",
    info="Top EL 46; lifted as casing halves / rotors (14 ft). LP hoods govern width.")
box(L, "STG: steam-turbine generator", 1041, 1059, 410, 460, 20, 38, tag="STG",
    color="machine", basis="typical", info="21 kV (assumed), 550-650 MVA typical.")
box(L, "ST aux: lube oil, turning gear, EHC", 1082, 1098, 470, 505, 20, 30,
    tag="ST aux", sheet="SK-3X1-03", info="480 V MCC in R3 (LV-ST).")
box(L, "ST exhaust duct (26 ft) to ACC", 1080, 1140, 487, 513, 22, 48,
    tag="ST exhaust", color="duct", sheet="SK-3X1-12",
    info="ST exhaust duct set to 26 ft diameter (Rev 10).")
box(L, "ACC steam riser", 1140, 1166, 487, 513, 22, 112, color="duct",
    basis="typical")
box(L, "ACC steam distribution header", 1140, 1160, 400, 760, 104, 118,
    color="duct", basis="typical", info="Hunterstown ACC duct 23 ft.")

# Filter houses on their own frames (SK-3X1-09/10)
for i, gx in enumerate([630, 790, 950], start=1):
    dx = gx - 630
    box("BASE_INLET_AIR", f"FH-{i}: GT inlet filter house (on frame)", 588 + dx, 672 + dx, 366, 403,
        100, 135, tag=f"FH-{i}", color="filter", sheet="SK-3X1-09",
        info="EL 100-135, no cantilever over the main roof. Three columns "
        "outside the gallery wall and three on the runway column line.")
    box("BASE_INLET_AIR", f"FH-{i} filter platform EL 108", 588 + dx, 672 + dx, 356, 366,
        107, 108, color="steel", sheet="SK-3X1-10",
        info="Filter elements changed from the south platform; hoist beam lowers "
        "them to a landing with truck access from the access road.")
    box("BASE_INLET_AIR", f"FH-{i} stair tower", 574 + dx, 586 + dx, 350, 366, 0, 110,
        color="steel", basis="typical", sheet="SK-3X1-10")
    box("BASE_INLET_AIR", f"GT{i} inlet duct drop", 660 + dx, 692 + dx, 372, 400, 37, 100,
        color="filter", sheet="SK-3X1-09")
    box("BASE_INLET_AIR", f"GT{i} inlet duct EL 23-37", 658 + dx, 694 + dx, 372, 466, 23, 37,
        color="filter", sheet="SK-3X1-09",
        info="Runs below the GT (EL 43-82) and generator (EL 41) travel bands "
        "with at least 4 ft clearance (hall3d.py check).")
    for cx in (590, 630, 670):
        for cy in (367.5, 401.5):
            box("BASE_INLET_AIR", f"FH-{i} frame column", cx + dx - 1.5, cx + dx + 1.5,
                cy - 1.5, cy + 1.5, 0, 100, color="steel", sheet="SK-3X1-10")

# ACC (80 cells: 8 streets x 10 cells, 40 ft) (SK-3X1-01/05/13)
L = "BASE_ACC"
box(L, "ACC fan deck EL 90 (80 cells)", 1130, 1450, 380, 780, 88, 92, tag="ACC",
    color="acc", sheet="SK-3X1-13",
    info="Air-cooled condenser, 80 cells of 40 ft (steam-cycle heat rejection). "
    "Top of steel ~120-125 ft (Hunterstown ~120; Sewaren, Bridgeport ~125). "
    "80 fan motors ACC-F01..F80, 480 V VFD from R4.")
for s in range(8):
    x0 = 1130 + 40 * s
    prism(L, f"ACC street {s+1}: A-frame tube bundles", x0 + 2, x0 + 38, 382, 778, 92, 122,
          ridge="y", color="acc", sheet="SK-3X1-13")
    hcyl(L, f"ACC street {s+1} steam header", x0 + 16.5, x0 + 23.5, 382, 778, 124.5, 3.5,
         color="duct", basis="typical")
for (x0, x1, y0, y1) in [(1130, 1450, 379, 380), (1130, 1450, 780, 781),
                         (1129, 1130, 380, 780), (1450, 1451, 380, 780)]:
    box(L, "ACC windwall", x0, x1, y0, y1, 92, 125, color="acc", sheet="SK-3X1-13")
for i in range(9):
    for j in range(11):
        cx, cy = 1130 + 40 * i, 380 + 40 * j
        box(L, "ACC support column", cx - 2, cx + 2, cy - 2, cy + 2, 0, 88, color="steel",
            basis="typical")
for i in range(8):
    for j in range(10):
        cyl(L, f"ACC-F{i*10+j+1:02d} fan", 1150 + 40 * i, 400 + 40 * j, 16, 92, 94,
            color="fan", sheet="SK-3X1-03")

# ---------------------------------------------------------------------------
# BASE_ELECTRICAL: GSUs, UATs, GCBs, R1..R4, EDGs (SK-3X1-03/04/05)
# ---------------------------------------------------------------------------
L = "BASE_ELECTRICAL"
for i, gx in enumerate([630, 790, 950], start=1):
    dx = gx - 630
    box(L, f"GSU-{i}: 21/230 kV generator step-up transformer", 610 + dx, 650 + dx, 325, 365,
        0, 24, tag=f"GSU-{i}", color="xfmr", sheet="SK-3X1-04",
        info="21/230 kV (assumed), 350-450 MVA typical; bushings add 12-15 ft. "
        f"HV connects to 230 kV breaker-and-a-half diameter D{i}.")
    box(L, f"GSU-{i} HV bushings", 620 + dx, 640 + dx, 335, 355, 24, 38, color="xfmr",
        basis="typical")
    box(L, f"UAT-{i}: 21/13.8 kV unit auxiliary transformer", 658 + dx, 676 + dx, 330, 352,
        0, 16, tag=f"UAT-{i}", color="xfmr", sheet="SK-3X1-04",
        info="Tapped between GCB and GSU (GSU side of the GCB), so the grid can "
        f"back-feed 13.8 kV bus {i} while GCB-{i} is open. 40-60 MVA typical.")
    box(L, f"GCB-{i}: generator circuit breaker", 625 + dx, 635 + dx, 378, 392, 14, 26,
        tag=f"GCB-{i}", color="xfmr", sheet="SK-3X1-10",
        info="In the south gallery on the IPB, outside bridge-crane coverage; "
        "gallery monorail to the west door.")
    box(L, f"GSU-{i} cooler bank / containment (as drawn)", 568 + dx, 584 + dx, 300, 366, 0, 12,
        color="concrete", sheet="SK-3X1-03")
    box(L, f"GSU-{i} bay equipment (as drawn)", 692 + dx, 707 + dx, 300, 366, 0, 12,
        color="concrete", sheet="SK-3X1-03")
    box(L, f"IPB tap enclosure {i}", 678 + dx, 688 + dx, 352, 368, 0, 14, color="xfmr",
        sheet="SK-3X1-01")
    box(L, f"GSU-{i} firewall", 602 + dx, 604 + dx, 318, 368, 0, 30, color="concrete",
        basis="typical")
    box(L, f"R2{'ABC'[i-1]}: unit / HRSG e-house (32 x 40 ft)", 552 + dx, 584 + dx, 612, 652,
        0, 14, tag=f"R2{'ABC'[i-1]}", color="ehouse", sheet="SK-3X1-03",
        info=f"Supply SWGR-13.8-{i}. 480 V switchgear, MCC and DCS remote I/O for "
        "SCR blowers, ammonia injection, HRSG valves and drains.")
    box(L, f"T-R2{'ABC'[i-1]}: 13.8/0.48 kV", 555 + dx, 567 + dx, 664, 676, 0, 10,
        color="xfmr", sheet="SK-3X1-04")
box(L, "GSU-ST: 21/230 kV (one ST GSU, baseline)", 1030, 1072, 320, 370, 0, 24,
    tag="GSU-ST", color="xfmr", sheet="SK-3X1-04",
    info="2 x 50% ST GSUs is a real option (Okeechobee). No UAT on the ST unit.")
box(L, "GSU-ST HV bushings", 1041, 1061, 335, 355, 24, 38, color="xfmr", basis="typical")
box(L, "GSU-ST firewall", 1009, 1011, 318, 368, 0, 30, color="concrete", basis="typical")
box(L, "GCB-ST", 1046, 1056, 378, 392, 14, 26, tag="GCB-ST", color="xfmr",
    sheet="SK-3X1-04")
box(L, "R1: main electrical building (64 x 180 ft)", 410, 474, 600, 780, 0, 24, tag="R1",
    color="building", sheet="SK-3X1-05",
    info="Holds SWGR-13.8-1/2/3 (11 cubicles each), SWGR-4.16-A/B, LC-480-A/B, "
    "EMCC, MCC-GT1..3, MCC-C1/C2, protection & control panels, DCS, three LCI "
    "static starters with dry-type input transformers, battery room (BAT-1/2), "
    "DC/UPS room, HVAC. Supply UAT-1/2/3 via DB-S; EDG-1/2 emergency. "
    "Rev 05 enlarged from 120 x 50 ft. Height 24 ft (Wrexham 16 ft; Progress "
    "Power 37 ft).")
box(L, "T4-A: 13.8/4.16 kV station transformer", 410, 430, 786, 802, 0, 14, tag="T4-A",
    color="xfmr", sheet="SK-3X1-04")
box(L, "T4-B: 13.8/4.16 kV station transformer", 410, 430, 808, 824, 0, 14, tag="T4-B",
    color="xfmr", sheet="SK-3X1-04")
box(L, "LCT-A: 13.8/0.48 kV load-centre transformer", 436, 448, 786, 798, 0, 10,
    tag="LCT-A", color="xfmr", sheet="SK-3X1-04")
box(L, "LCT-B: 13.8/0.48 kV load-centre transformer", 436, 448, 808, 820, 0, 10,
    tag="LCT-B", color="xfmr", sheet="SK-3X1-04")
box(L, "R3: ST auxiliary e-house (40 x 65 ft)", 1035, 1100, 572, 612, 0, 14, tag="R3",
    color="ehouse", sheet="SK-3X1-03",
    info="Supply SWGR-13.8-2. 480 V switchgear and MCC for ST lube oil, turning "
    "gear, EHC and air compressors.")
box(L, "T-R3: 13.8/0.48 kV", 1053, 1065, 626, 638, 0, 10, color="xfmr")
box(L, "R4: ACC VFD e-house (60 x 120 ft)", 1135, 1255, 308, 368, 0, 16, tag="R4",
    color="ehouse", sheet="SK-3X1-03",
    info="Supply SWGR-13.8-1/2/2/3 via four outdoor transformers. 480 V "
    "switchgear, 92 VFDs (80 ACC fans + 12 aux cooler fans), MCC for vacuum "
    "pumps. VFD-ACC route ~633 ft to the farthest fan (verify drive cable limits).")
for k, (x0, y0) in enumerate([(1266, 310), (1292, 310), (1266, 340), (1292, 340)], 1):
    box(L, f"T-R4-{k}: 13.8/0.48 kV", x0, x0 + 12, y0, y0 + 14, 0, 10, color="xfmr",
        sheet="SK-3X1-04")
box(L, "Spare e-house pad (reserve, as drawn)", 1320, 1445, 308, 368, 0, 0.6,
    color="pad", sheet="SK-3X1-01")
box(L, "EDG-1: 3 MW emergency diesel (480 V)", 412, 462, 338, 350, 0, 15, tag="EDG-1",
    color="machine", basis="vendor", sheet="SK-3X1-12",
    info="Cat 3516C sound-attenuated enclosure. Emergency supply only; ATS / "
    "interlocked incomers to LC-480-A/B.")
box(L, "EDG-2: 3 MW emergency diesel (480 V)", 468, 518, 338, 350, 0, 15, tag="EDG-2",
    color="machine", basis="vendor", sheet="SK-3X1-12")
box(L, "HTP-1: heat-trace panel", 569, 575, 852, 855, 0, 7, tag="HTP-1", sheet="SK-3X1-03")
box(L, "HTP-2: heat-trace panel (NH3)", 912, 918, 1450, 1453, 0, 7, tag="HTP-2")
box(L, "HTP-3: heat-trace panel (tanks)", 605, 611, 1541, 1544, 0, 7, tag="HTP-3")
box(L, "HTP-4: heat-trace panel (gas)", 1600, 1606, 1444, 1447, 0, 7, tag="HTP-4")
box(L, "CPR-1: cathodic-protection rectifier", 1541, 1545, 1478, 1481, 0, 6, tag="CPR-1")
box(L, "CPR-2: cathodic-protection rectifier", 655, 659, 1578, 1582, 0, 6, tag="CPR-2")

# ---------------------------------------------------------------------------
# BASE_UTILITIES: BOP around ACC and hall
# ---------------------------------------------------------------------------
L = "BASE_UTILITIES"
box(L, "Air compressors AC-A/B/C", 1030, 1100, 700, 745, 0, 14, tag="AC-A/B/C",
    color="building", sheet="SK-3X1-03", info="480 V MCC soft starters in R3.")
box(L, "Chemical feed", 1030, 1100, 760, 781, 0, 12, tag="Chem feed", color="building")
box(L, "SWAS: steam & water analysis", 1030, 1100, 784, 805, 0, 12, tag="SWAS",
    color="building")
box(L, "CP-A/B/C: condensate pumps (4.16 kV)", 1182, 1218, 809, 827, 0, 7, tag="CP-A/B/C",
    color="motor", sheet="SK-3X1-03", info="North of ACC; 4.16 kV MV contactor, "
    "SWGR-4.16-A/B (route MV-CP).")
box(L, "VAC-A/B: ACC air-removal vacuum pumps", 1235, 1265, 797, 817, 0, 7, tag="VAC-A/B",
    color="motor", sheet="SK-3X1-03")
box(L, "CCW-A/B: closed cooling water pumps", 1283, 1313, 807, 827, 0, 7, tag="CCW-A/B",
    color="motor", sheet="SK-3X1-03")
box(L, "Aux dry coolers AUXC-F01..12 (closed cooling water)", 1326, 1446, 792, 828, 6, 16,
    tag="AUXC", color="acc", sheet="SK-3X1-03",
    info="12 fans, 480 V VFDs in R4. Heat rejection for the closed cooling-water loop.")
cyl(L, "Condensate storage tank", 1155, 812, 14, 0, 30, color="tank")
# pipe racks (EL 24-36 tiers)
for (x0, x1, y0, y1, n) in [(460, 1300, 826, 850, "Main E-W pipe / cable rack (24 ft)"),
                            (1108, 1128, 570, 850, "N-S pipe rack along ACC")]:
    box(L, n + " - tiers EL 24/30/36", x0, x1, y0, y1, 23, 37, color="rack",
        sheet="SK-3X1-12", info="Pipe rack widened from 16 to 24 ft (Rev 10). "
        "MV tray tier EL +36, control tray EL +42.")
    step = 25
    if x1 - x0 > y1 - y0:
        xs = range(int(x0), int(x1) + 1, step)
        for x in xs:
            for y in (y0, y1 - 2):
                box(L, "rack bent", x - 1, x + 1, y, y + 2, 0, 42, color="steel",
                    basis="typical")
    else:
        for y in range(int(y0), int(y1) + 1, step):
            for x in (x0, x1 - 2):
                box(L, "rack bent", x, x + 2, y - 1, y + 1, 0, 42, color="steel",
                    basis="typical")

# ---------------------------------------------------------------------------
# BASE_SWITCHYARD: 230 kV breaker-and-a-half (SK-3X1-01/04)
# ---------------------------------------------------------------------------
L = "BASE_SWITCHYARD"
pad(L, "230 kV switchyard (gravel)", 400, 1940, 50, 250, color="gravel", z1=0.4,
    sheet="SK-3X1-04", info="Breaker-and-a-half: 5 diameters x 3 breakers = 15 "
    "breakers (9 installed). D1 GTG-1/Line 1, D2 GTG-2/Line 2, D3 STG/GTG-3; "
    "D4 (BESS / modular) and D5 (CCS) future. 345 or 500 kV is common at ~1.6 GW.")
for yb, n in [(237, "230 kV bus 1"), (65, "230 kV bus 2")]:
    box(L, n + " (strain bus)", 530, 1925, yb - 1, yb + 1, 38, 40, color="conductor",
        sheet="SK-3X1-04")
for x in (530, 1300, 1925):
    for yb in (62, 242):
        box(L, "230 kV dead-end structure (47 ft)", x - 12, x + 12, yb - 1.5, yb + 1.5, 0, 47,
            color="steel", sheet="SK-3X1-13",
            info="230 kV dead-ends 47 ft (CPUC Jefferson-Martin).")
for d, x in [("D1", 700), ("D2", 900), ("D3", 1100)]:
    for y in (110, 150, 190):
        box(L, f"{d} 230 kV breaker", x - 8, x + 8, y - 8, y + 8, 0, 12, tag=d,
            color="xfmr", sheet="SK-3X1-04")
    box(L, f"{d} diameter gantry", x - 1, x + 1, 70, 232, 0, 35, color="steel",
        basis="typical")
for d, x in [("D4 future", 1720), ("D5 future (CCS)", 1860)]:
    for y in (110, 150, 190):
        box(L, f"{d} breaker position (not installed)", x - 8, x + 8, y - 8, y + 8, 0, 1,
            color="future", sheet="SK-3X1-04")
for x, n in [(670, "Line 1"), (870, "Line 2")]:
    box(L, f"{n} 230 kV line take-off tower", x - 6, x + 6, 12, 24, 0, 90, color="steel",
        basis="typical")
box(L, "RH: switchyard relay / control house (52 x 70 ft)", 420, 490, 180, 232, 0, 14,
    tag="RH", color="ehouse", sheet="SK-3X1-03",
    info="Protection, SCADA and communications for the 230 kV yard; 125 V DC and "
    "fibre to R1 via DB-S.")
pad(L, "Reserved 230 kV corridor COR-HMOD (modular tie)", 1490, 1540, 237, 830,
    color="corridor", z1=0.2, sheet="SK-3X1-08")
pad(L, "Reserved 230 kV corridor COR-HMOD (modular tie)", 1490, 2120, 780, 830,
    color="corridor", z1=0.2, sheet="SK-3X1-08")

# ---------------------------------------------------------------------------
# BASE_SERVICES: controls / service quarter (F) and water / utilities (E)
# ---------------------------------------------------------------------------
L = "BASE_SERVICES"
pad(L, "Parking", 40, 320, 60, 240, color="road", z1=0.2)
box(L, "Gatehouse", 277, 300, 305, 325, 0, 12, color="building", sheet="SK-3X1-12")
box(L, "Control / admin building (main control room)", 83, 320, 345, 396, 0, 20, tag="CR",
    color="building", sheet="SK-3X1-12",
    info="51 x 237 x 20 ft (Smarr EA, 7HA.03, 2025). Operator consoles only; DCS "
    "cabinets are distributed in R1, R2A-C, R3 and R4.")
box(L, "Warehouse", 133, 320, 470, 561, 0, 35, color="building", sheet="SK-3X1-12",
    info="91 x 187 x 35 ft (Smarr EA).")
box(L, "Maintenance building / workshop", 198, 320, 600, 641, 0, 20, color="building",
    sheet="SK-3X1-12", info="41 x 122 x 20 ft (Smarr EA).")
box(L, "Comms tower (lattice)", 258, 267, 451, 460, 0, 120, color="steel", basis="typical")
pad(L, "Cable reel yard / outage laydown", 40, 320, 690, 900, color="pad", z1=0.3)
box(L, "Stormwater basin", 40, 320, 1430, 1640, -8, 0, color="water",
    info="Detention basin (depth illustrative).")
L = "BASE_WATER"
box(L, "Water treatment building (incl. R-WT electrical room)", 440, 600, 1445, 1530, 0, 30,
    tag="R-WT", color="building", sheet="SK-3X1-12",
    info="R-WT: 480 V MCC for water treatment, wastewater and fire-pump jockey "
    "pump; supply SWGR-13.8-2 via DB-W. Height 30 ft (Wrexham 33 ft).")
box(L, "Wastewater treatment", 620, 745, 1445, 1530, 0, 25, color="building")
cyl(L, "Raw water tank", 465, 1590, 20, 0, 48, color="tank", sheet="SK-3X1-12",
    info="40 dia x 48 ft class (Smarr EA).")
cyl(L, "Fire / service water tank", 530, 1590, 26, 0, 40, color="tank", sheet="SK-3X1-12",
    info="52 dia x 40 ft (Smarr service water).")
cyl(L, "Demineralised water tank", 600, 1590, 20, 0, 48, color="tank", sheet="SK-3X1-12",
    info="40 dia x 48 ft (Smarr demin).")
box(L, "Fire pump house", 700, 740, 1575, 1605, 0, 16, color="building", basis="typical")
box(L, "Ammonia storage (aqueous, SCR reagent)", 800, 873, 1450, 1492, 0, 4, color="concrete",
    sheet="SK-3X1-12", info="73 x 42 ft (Smarr EA). Bund shown, tank below.")
hcyl(L, "Ammonia storage tank", 806, 867, 1462, 1480, 10, 8, color="tank")
box(L, "Auxiliary boiler", 935, 995, 1450, 1540, 0, 30, color="building", basis="typical")
cyl(L, "Aux boiler stack", 985, 1530, 3, 30, 70, color="stack", basis="typical")
box(L, "H2 / CO2 storage (generator gas)", 1080, 1125, 1450, 1510, 0, 10, color="tank")
box(L, "Oil-water separator", 1200, 1226, 1450, 1458, 0, 8, color="tank", sheet="SK-3X1-12",
    info="26 x 8 ft (Smarr EA).")
L = "BASE_FUEL"
pad(L, "Plant gas yard (pad)", 1560, 1940, 1430, 1640, color="gravel", z1=0.4,
    sheet="SK-3X1-12", info="Pad with filter-separators, heater, metering and "
    "regulation skids; skids 16 ft max (Wrexham, Progress Power).")
box(L, "Gas yard filter-separators", 1640, 1680, 1470, 1490, 0, 12, color="tank")
box(L, "Fuel-gas performance heater", 1700, 1740, 1470, 1490, 0, 14, color="equip")
box(L, "Gas metering skid", 1640, 1690, 1520, 1540, 0, 10, color="equip")
box(L, "Gas pressure regulation skid", 1710, 1750, 1520, 1540, 0, 12, color="equip")
box(L, "Gas yard local control enclosure", 1565, 1585, 1440, 1452, 0, 10, color="ehouse",
    info="Local enclosure, not an e-house.")
box(L, "CONDITIONAL: fuel-gas compressors", 1800, 1930, 1560, 1630, 0, 20, color="conditional",
    sheet="SK-3X1-01", basis="conditional",
    info="Needed only if pipeline pressure is below GT requirement.")
box(L, "CONDITIONAL: backup fuel oil (ULSD) unloading / forwarding", 1330, 1490, 1430, 1640,
    0, 0.4, color="conditional", basis="conditional")
cyl(L, "CONDITIONAL: ULSD backup fuel-oil tank", 1410, 1580, 45, 0, 40, color="conditional",
    basis="conditional", info="Unloading, tank and forwarding pumps; design-dependent.")

# ---------------------------------------------------------------------------
# ADJACENT MARKET: pipeline M&R (base: always exists, by pipeline operator)
# ---------------------------------------------------------------------------
L = "ADJ_MR"
pad(L, "Pipeline M&R station (by pipeline operator)", 1560, 1800, 1690, 1900,
    color="gravel", z1=0.4, sheet="SK-3X1-14")
box(L, "1 Pig receiver, lateral terminus", 1600, 1612, 1850, 1895, 0, 6, color="tank")
box(L, "2 Insulating joint + ESD valve", 1602, 1610, 1830, 1838, 0, 5)
hcyl(L, "3 Horizontal filter-separator", 1630, 1665, 1845, 1857, 6, 6, color="tank")
for k, y in enumerate([1820, 1838, 1856]):
    hcyl(L, f"4 Line heater {k+1} (water bath)", 1690, 1720, y, y + 10, 5, 5, color="tank")
box(L, "5 Ultrasonic meters, 2 runs (custody)", 1620, 1670, 1770, 1786, 0, 6)
box(L, "6 Regulation / flow control building (30 x 30 ft)", 1700, 1730, 1760, 1790, 0, 16,
    color="building", sheet="SK-3X1-14", info="Cove Point: 30 x 30 ft.")
box(L, "7 Gas quality + measurement building (8 x 16 ft)", 1620, 1636, 1730, 1738, 0, 10,
    color="building")
cyl(L, "8 Condensate tank", 1751, 1861, 6, 0, 10, color="tank")
box(L, "9 Service panel + UPS, SCADA RTU, CP", 1740, 1756, 1728, 1740, 0, 8, color="ehouse")

# ---------------------------------------------------------------------------
# OPTIONAL: carbon capture, 3 trains (SK-3X1-06)
# ---------------------------------------------------------------------------
L = "OPT_CCS"
for i, dx in enumerate([0, 160, 320]):
    t = "ABC"[i]
    box(L, f"DMP-{t}: diverter / bypass damper", 613 + dx, 643 + dx, 808, 826, 40, 62,
        color="duct", sheet="SK-3X1-06")
    box(L, f"Flue-gas duct HRSG {i+1} to DCC-{t}", 621 + dx, 639 + dx, 826, 985, 44, 62,
        color="duct", sheet="SK-3X1-02")
    box(L, f"DCC-{t}: direct-contact cooler (quench)", 568 + dx, 608 + dx, 985, 1060, 0, 90,
        tag=f"DCC-{t}", color="ccs", sheet="SK-3X1-13", basis="typical",
        info="90 ft; no public value found.")
    box(L, f"DCC-{t} pumps + water filter", 568 + dx, 608 + dx, 1066, 1090, 0, 8, color="motor")
    box(L, f"BF-{t}: booster fan (~16 MW)", 615 + dx, 655 + dx, 985, 1035, 0, 30, tag=f"BF-{t}",
        color="motor", sheet="SK-3X1-06",
        info="NZT: 16.4 MWe per H-class train. VFD cables from CCS MV building.")
    box(L, f"Rich/lean pumps + cross exchanger + lean cooler {t}", 660 + dx, 705 + dx,
        1040, 1100, 0, 15, color="equip")
    cyl(L, f"Absorber {t} (62 ft dia x 262 ft)", 630 + dx, 1220, 31, 0, 262, tag=f"ABS-{t}",
        color="ccs", sheet="SK-3X1-13",
        info="Keadby 3 DCO: twin absorbers 19.0 m dia x 80 m AGL (62 x 262 ft).")
    cyl(L, f"Absorber {t} stack (to 313 ft)", 630 + dx, 1220, 9, 262, 313, color="stack",
        sheet="SK-3X1-13", info="Keadby 3 twin: 95.5 m (313 ft).")
    box(L, f"Water-wash pumps {t}", 675 + dx, 705 + dx, 1150, 1195, 0, 8, color="motor")
for i, cx in enumerate([1070, 1120, 1170]):
    t = "ABC"[i]
    cyl(L, f"STR-{t}: stripper / regenerator (45 ft dia x 207 ft)", cx, 1187.5, 22.5, 0, 207,
        tag=f"STR-{t}", color="ccs", sheet="SK-3X1-13",
        info="Keadby 3 DCO: CO2 stripper 15.0 m dia x 63 m AGL (49 x 207 ft). "
        "Reboiler, overhead condenser and reflux drum per train.")
    box(L, f"RB-{t}: reboiler (LP steam from ST extraction)", cx - 20, cx + 20, 1105, 1150,
        0, 30, color="equip", sheet="SK-3X1-06")
box(L, "Reclaimer (thermal, intermittent)", 1210, 1260, 1105, 1150, 0, 25, color="equip")
box(L, "Solvent + NaOH storage", 1210, 1300, 1165, 1225, 0, 30, color="tank")
box(L, "Activated-carbon filter", 1210, 1300, 1235, 1265, 0, 15, color="equip")
box(L, "CO2 compression 3 x ~19 MW + dehydration", 1310, 1435, 1230, 1345, 0, 35,
    color="building", sheet="SK-3X1-06",
    info="Three intercooled LP compressors; NZT 19.1 MWe per train.")
box(L, "CONDITIONAL: HP export compressor + metering", 1360, 1435, 1160, 1220, 0, 20,
    color="conditional", basis="conditional")
box(L, "CCS MV switchgear building (VFDs)", 1060, 1200, 985, 1050, 0, 24, color="ehouse",
    sheet="SK-3X1-06", info="Three trains ~150 MWe (NZT 50.1 MWe/train).")
box(L, "CCS T-1: 230/13.8 kV", 1210, 1250, 985, 1030, 0, 22, tag="CCS T-1", color="xfmr",
    info="Fed from future D5 diameter by 230 kV underground cable (2 circuits).")
box(L, "CCS T-2: 230/13.8 kV", 1260, 1300, 985, 1030, 0, 22, tag="CCS T-2", color="xfmr")
box(L, "CCS instrument air", 1310, 1350, 985, 1030, 0, 12, color="equip")
box(L, "CCS F&G / control", 1360, 1435, 985, 1030, 0, 16, color="ehouse")
L = "OPT_CCSU"
box(L, "CCS cooling tower (~30 cells) - CCS process cooling only", 440, 1190, 1740, 1860, 0, 42,
    color="tower", sheet="SK-3X1-06",
    info="Not the ACC. NZT gives 360-390 MWth per train. Cell end walls up to 50 ft.")
for c in range(15):
    for r in range(2):
        cyl(L, "CCS tower fan stack", 465 + 50 * c, 1770 + 60 * r, 18, 42, 50, color="tower",
            basis="typical")
box(L, "CCS circulating-water pumps", 1200, 1280, 1760, 1820, 0, 12, color="motor")
box(L, "CT MCC / VFD e-house", 1200, 1290, 1830, 1885, 0, 16, color="ehouse")
box(L, "CCS wastewater (DCC + tower blowdown)", 1300, 1430, 1720, 1800, 0, 25,
    color="building")

# ---------------------------------------------------------------------------
# OPTIONAL: BESS (SK-3X1-07)
# ---------------------------------------------------------------------------
L = "OPT_BESS"
for y in (467, 525, 583, 641, 699):
    for x in range(1565, 1866, 60):
        box(L, "BESS container (ISO 40 ft HC)", x, x + 40, y, y + 8, 0, 9.5, color="bess",
            basis="vendor", info="BMS, HVAC, fire suppression. ISO 668 40 x 8 x 9.5 ft.")
    for x in (1590, 1710, 1830):
        box(L, "BESS PCS / MV skid", x, x + 20, y + 19, y + 27, 0, 9, color="xfmr")
box(L, "BESS main power transformer 34.5/230 kV (to D4 upper)", 1725, 1765, 352, 387, 0, 24,
    color="xfmr", info="Main power transformer to D4 upper position (future).")
box(L, "34.5 kV collector e-house (arc-resistant)", 1800, 1850, 360, 376, 0, 14,
    color="ehouse")
box(L, "BESS auxiliary transformer", 1885, 1905, 360, 372, 0, 8, color="xfmr")
box(L, "BESS EMS / SCADA", 1885, 1905, 410, 422, 0, 10, color="ehouse")
box(L, "CONDITIONAL: grounding transformer", 1565, 1575, 415, 425, 0, 8, color="conditional",
    basis="conditional")

# ---------------------------------------------------------------------------
# OPTIONAL: modular generation + black start (SK-3X1-07/08)
# ---------------------------------------------------------------------------
L = "OPT_MOD"
box(L, "RICE engine hall (8 engines)", 1570, 1810, 1040, 1130, 0, 40, color="hall",
    info="Hall for 8 medium-speed 18-cyl engines (18V50 class approx.).")
for k in range(8):
    x = 1581 + 28 * k
    box(L, f"RICE engine-generator {k+1}", x, x + 19, 1055, 1115, 0, 20, color="machine")
    box(L, f"SCR + oxidation catalyst, engine {k+1}", x - 1, x + 21, 1000, 1030, 0, 25,
        color="equip")
    cyl(L, f"RICE stack {k+1}", x + 10, 1037, 3, 0, 90, color="stack", sheet="SK-3X1-13",
        info="90 ft (Weston ~65 ft; Humboldt Bay 100 ft).")
    for r in range(5):
        box(L, "RICE radiator", x - 1, x + 21, 1140 + 16 * r, 1152 + 16 * r, 4, 14,
            color="acc")
box(L, "Lube oil / starting air / oily water building", 1570, 1690, 1235, 1290, 0, 20,
    color="building")
box(L, "Gas conditioning skid", 1700, 1760, 1250, 1280, 0, 10)
box(L, "Reagent storage", 1795, 1825, 1245, 1275, 0, 15, color="tank")
box(L, "PCM: power control module", 1820, 1860, 1140, 1220, 0, 14, color="ehouse")
box(L, "RICE CEMS", 1830, 1846, 1005, 1015, 0, 10)
for k, x in enumerate([1910, 2110], 1):
    box(L, f"SC-{k}: aeroderivative package (LM6000 class)", x, x + 90, 1190, 1220, 0, 30,
        color="machine", info="Simple-cycle unit with filter house.")
    box(L, f"SC-{k} SCR / CO catalyst", x + 90, x + 130, 1190, 1220, 0, 35, color="equip")
    cyl(L, f"SC-{k} stack (80 ft)", x + 142, 1204.5, 6.5, 0, 80, color="stack",
        sheet="SK-3X1-13", info="Mira Loma permit: 80 ft.")
    box(L, f"SC-{k} PCM + 15 kV GCB", x, x + 40, 1245, 1259, 0, 12, color="ehouse")
    box(L, f"SC-{k} lube-oil fin-fan cooler", x + 50, x + 70, 1245, 1259, 0, 10, color="acc")
    box(L, f"CONDITIONAL: SC-{k} inlet chiller / evap cooler", x, x + 60, 1135, 1170, 0, 14,
        color="conditional", basis="conditional")
box(L, "Fuel-gas compressors 3 x 100% electric", 2290, 2370, 1180, 1240, 0, 20,
    color="building")
box(L, "Demin tank + trailer pad", 2290, 2330, 1260, 1300, 0, 30, color="tank")
box(L, "Water-injection skid", 2255, 2275, 1280, 1290, 0, 8)
box(L, "Aqueous ammonia (SC units)", 2240, 2280, 1318, 1330, 0, 10, color="tank")
box(L, "Black-start gensets (proposed)", 1570, 1616, 870, 880, 0, 13, color="machine")
box(L, "Black-start gensets (proposed)", 1570, 1616, 888, 898, 0, 13, color="machine")
box(L, "BS switchgear", 1625, 1645, 875, 893, 0, 12, color="ehouse")
box(L, "CONDITIONAL: BESS black-start alternative", 1655, 1700, 868, 900, 0, 9.5,
    color="conditional", basis="conditional")
box(L, "MOD-EH: 13.8 kV modular collector e-house", 1915, 1995, 880, 900, 0, 16,
    color="ehouse", sheet="SK-3X1-08")
box(L, "T-MOD-1: 13.8/230 kV", 2045, 2085, 870, 905, 0, 24, color="xfmr", sheet="SK-3X1-08")
box(L, "T-MOD-2: 13.8/230 kV", 2105, 2145, 870, 905, 0, 24, color="xfmr", sheet="SK-3X1-08")
for k in range(4):
    x = 1995 + 14 * k
    box(L, f"Fuel cell SOFC module {k+1} (Bloom ES5 class)", x, x + 9, 1070, 1096, 0, 7,
        color="bess", basis="vendor", info="26 ft 5 in x 8 ft 7 in x 6 ft 9 in.")
box(L, "Fuel-cell inverter / AC cabinet / desulfurizer", 2060, 2102, 1072, 1096, 0, 8,
    color="ehouse")
for k in range(3):
    x = 2260 + 14 * k
    box(L, f"Microturbine {k+1} (1 MW, Capstone C1000 class)", x, x + 8, 1068, 1096, 0, 9.5,
        color="machine", basis="vendor")
box(L, "MOD-LV 480 V board + step-up", 2215, 2267, 970, 982, 0, 10, color="ehouse")
L = "OPT_TMP"
pad(L, "Portable pad lane", 2130, 2370, 620, 640, color="road", z1=0.3)
pad(L, "Portable pad lane", 2346, 2370, 305, 620, color="road", z1=0.3)
box(L, "Drive-over cable ramp", 2238, 2252, 617, 643, 0, 1, color="amber")
box(L, "CONT-1: containerized genset 13.8 kV (40 ft)", 2000, 2040, 642, 650, 0, 9.5,
    color="machine", sheet="SK-3X1-08")
box(L, "CONT-2: containerized genset 13.8 kV (40 ft)", 2000, 2040, 607, 615, 0, 9.5,
    color="machine", sheet="SK-3X1-08")
box(L, "GSP-1 gen. breaker / protection", 2042, 2050, 640, 652, 0, 8, color="ehouse")
box(L, "GSP-2 gen. breaker / protection", 2042, 2050, 605, 617, 0, 8, color="ehouse")
box(L, "MOB-1: trailer genset", 2160, 2213, 695, 704, 0, 13.5, color="machine")
box(L, "PIC: portable input cabinet", 2255, 2263, 572, 578, 0, 7, color="ehouse")
box(L, "Commissioning load bank (trailer)", 2295, 2325, 560, 568, 0, 12, color="equip")
box(L, "GEN-E: enclosed industrial gas genset 2 MW", 2000, 2046, 460, 470, 0, 15,
    color="machine", basis="vendor")
box(L, "GEN-O: open engine-generator skid", 2010, 2036, 420, 428, 0, 8, color="machine")
box(L, "PAD-LV 480 V paralleling switchboard", 2160, 2190, 430, 440, 0, 9, color="ehouse")
box(L, "PAD-TX 480 V : 13.8 kV", 2215, 2227, 429, 441, 0, 10, color="xfmr")
box(L, "PAD-EH 13.8 kV switchgear e-house", 2160, 2200, 470, 484, 0, 14, color="ehouse")
box(L, "Portable pad gas-conditioning skid", 2310, 2340, 430, 440, 0, 8)

# ---------------------------------------------------------------------------
# OPTIONAL: GT inlet chilling (SK-3X1-02)
# ---------------------------------------------------------------------------
L = "OPT_IC"
box(L, "Inlet-chilling tower (12 cells) - chiller heat rejection", 60, 300, 1240, 1320, 0, 42,
    color="tower", basis="typical")
for c in range(6):
    for r in range(2):
        cyl(L, "Inlet-chilling tower fan stack", 80 + 40 * c, 1260 + 40 * r, 15, 42, 50,
            color="tower", basis="typical")
box(L, "Chillers x6 (water-cooled)", 60, 240, 1040, 1170, 0, 25, color="building")
box(L, "CHW / CW pumps", 250, 305, 1100, 1170, 0, 10, color="motor")
box(L, "Inlet-chilling e-house / transformer", 250, 305, 1040, 1085, 0, 14, color="ehouse")
box(L, "CHW pumps", 60, 150, 1190, 1225, 0, 10, color="motor")
cyl(L, "CONDITIONAL: TES chilled-water tank", 200, 1205, 24, 0, 40, color="conditional",
    basis="conditional")

# ---------------------------------------------------------------------------
# ADJACENT MARKET: LNG satellite and 25 MW green hydrogen (SK-3X1-14)
# ---------------------------------------------------------------------------
L = "OPT_LNG"
box(L, "12 Spill impoundment (NFPA 59A, to verify)", 2115, 2298, 1732, 1836, 0, 4,
    color="concrete")
for k in range(8):
    x = 2130 + 20 * k
    hcyl(L, f"11 LNG tank {k+1}: Chart HS 50000 (51,780 gal)", x, x + 12.5, 1745, 1822.6, 11,
         6.25, color="tank", basis="vendor", sheet="SK-3X1-14",
         info="150 in dia x 931 in long; 8 tanks = 414,000 gal, roughly 9 h of one GT.")
pad(L, "10 LNG truck unloading bay 1", 1840, 1912, 1690, 1712, color="road", z1=0.3)
pad(L, "10 LNG truck unloading bay 2", 1925, 1997, 1690, 1712, color="road", z1=0.3)
box(L, "10 Unloading skid", 1885, 1925, 1716, 1728, 0, 8)
box(L, "14 Vaporizers + glycol heater", 1880, 1990, 1760, 1820, 0, 18, color="equip")
box(L, "13 Send-out pumps 2 x 100%", 2030, 2070, 1765, 1795, 0, 8, color="motor")
box(L, "15 Boil-off gas compressor", 2030, 2075, 1815, 1845, 0, 12, color="motor")
box(L, "16 Send-out metering + pressure control", 1880, 1930, 1840, 1880, 0, 10)
box(L, "LNG impoundment sump pump", 1830, 1860, 1760, 1780, 0, 6)
box(L, "17 LNG e-house (13.8 kV / 480 V)", 1950, 1990, 1850, 1864, 0, 14, color="ehouse",
    info="15 kV from R1 ~2,690 ft (1,760 shared DB-N + 931 new).")
cyl(L, "18 LNG vent stack", 2095, 1863, 2, 0, 60, color="stack", basis="typical")
L = "OPT_H2"
box(L, "22 Electrolyzer building: 5 x HyLYZER-1000 + 5 rectifiers", 2010, 2170, 1440, 1520,
    0, 30, color="hall", sheet="SK-3X1-14",
    info="25 MW PEM electrolysis, 10.8 t/day, sized like FPL Cavendish at "
    "Okeechobee. H2 is turbine fuel from renewable power imported via D6.")
for k in range(5):
    x = 2020 + 20 * k
    box(L, f"PEM electrolyzer {k+1} (HyLYZER-1000)", x, x + 7.5, 1450, 1477.7, 0, 10,
        color="bess", basis="vendor")
    box(L, f"Rectifier {k+1} (7 MVA)", x, x + 8.2, 1490, 1504.8, 0, 8, color="ehouse",
        basis="vendor")
    box(L, f"21 Rectifier transformer {k+1} (7 MVA)", x + 2 * k, x + 2 * k + 12, 1530, 1542,
        0, 10, color="xfmr")
box(L, "24 Water purification (RO / EDI)", 2125, 2160, 1455, 1480, 0, 12)
box(L, "20 H2 13.8 kV e-house", 2240, 2300, 1440, 1456, 0, 14, color="ehouse")
box(L, "19 T-H2 230/13.8 kV (~40 MVA)", 2330, 2370, 1440, 1480, 0, 24, color="xfmr",
    info="230 kV cable from D6, 1,720 ft route along the east fence.")
box(L, "23 Dry coolers", 2185, 2225, 1440, 1560, 4, 14, color="acc")
box(L, "25 H2 dryer / purification", 2240, 2280, 1470, 1490, 0, 12)
box(L, "28 N2 purge supply", 2240, 2270, 1500, 1520, 0, 10, color="tank")
box(L, "26 H2 compressor 1 (40 ft ISO)", 2290, 2330, 1500, 1508, 0, 9.5, color="machine")
box(L, "26 H2 compressor 2 (40 ft ISO)", 2290, 2330, 1515, 1523, 0, 9.5, color="machine")
for (x, y) in [(2250, 1560), (2250, 1580), (2300, 1560), (2300, 1580)]:
    hcyl(L, "27 H2 storage tube bank (~40 ft tubes)", x, x + 40, y, y + 10, 5, 5, color="tank")
cyl(L, "29 H2 vent stack", 2380, 1597, 2, 0, 40, color="stack", basis="typical")
box(L, "30 H2 / gas blending skid (plant gas yard)", 1800, 1840, 1470, 1500, 0, 10,
    color="equip", info="Blends into the GT-1 fuel branch (5% vol pilot).")
L = "OPT_D6"
for y in (110, 150, 190):
    box(L, "D6 future (H2) breaker position", 2002, 2018, y - 8, y + 8, 0, 1, color="future")

# ---------------------------------------------------------------------------
# Routes (cables, trays, pipes) extracted from the drawing vectors
# ---------------------------------------------------------------------------
ROUTE_STYLE = {
    # type: (elevation ft, width ft, height ft, colour key, label, layer)
    "ipb":          (20, 4, 4, "copper_dark", "Isolated-phase bus + UAT tap (bus duct, not cable)", "ROUTES_BASE"),
    "mv_tray":      (36, 3, 1, "copper", "MV power tray (rack tier EL +36)", "ROUTES_BASE"),
    "lv_tray":      (30, 2, 0.8, "copper", "LV / hall power tray", "ROUTES_BASE"),
    "control_tray": (42, 1.5, 0.6, "copper", "Control / instrument tray (EL +42)", "ROUTES_BASE"),
    "duct_bank":    (-2, 4, 2, "ductbank", "Duct bank (underground)", "ROUTES_BASE"),
    "hv_overhead":  (40, 1, 1, "conductor", "230 kV overhead", "ROUTES_BASE"),
    "steam":        (26, 3, 3, "steam", "Steam", "PROCESS_PIPING"),
    "condensate":   (25, 2, 2, "condensate", "Condensate", "PROCESS_PIPING"),
    "feedwater":    (12, 2, 2, "feedwater", "Feedwater", "PROCESS_PIPING"),
    "ccw":          (24, 2, 2, "ccw", "Closed cooling water", "PROCESS_PIPING"),
    "fuel_gas":     (4, 1.5, 1.5, "fuelgas", "Fuel gas", "PROCESS_PIPING"),
    "flue_duct":    (0, 0, 0, "", "", ""),  # handled as firewall boxes / ducts
    "hv_cable":     (-3, 2, 2, "copper_dark", "230 kV underground cable", "OPT_ROUTES"),
    "mvlv_cable":   (-2, 2, 1, "copper", "MV / LV cable (optional systems)", "OPT_ROUTES"),
    "cw":           (3, 4, 4, "cw", "Circulating / condenser water", "OPT_ROUTES"),
    "chw":          (3, 2, 2, "chw", "Chilled water", "OPT_ROUTES"),
    "hydrogen":     (4, 1, 1, "hydrogen", "Hydrogen", "OPT_ROUTES"),
    "lng":          (4, 1.5, 1.5, "lng", "LNG (cryogenic)", "OPT_ROUTES"),
}
routes = []
for fname, src in [("routes_base.json", "SK-3X1-01"), ("routes_optional.json", "SK-3X1-02")]:
    data = json.load(open(os.path.join(HERE, fname)))
    for rtype, polys in data.items():
        z, w, h, colour, label, layer = ROUTE_STYLE[rtype]
        if not layer:
            continue
        for pl in polys:
            if len(pl) < 2:
                continue
            routes.append(dict(type=rtype, layer=layer, label=label, z=z, w=w, h=h,
                               color=colour, points=pl, sheet=src))

LAYERS = {
    "SITE": "Site, roads and fence",
    "BASE_POWER_BLOCK": "A Power block (hall, GTs, ST, HRSGs, stacks)",
    "BASE_INLET_AIR": "Filter houses and inlet ducts",
    "BASE_ACC": "B Air-cooled condenser (80 cells)",
    "BASE_ELECTRICAL": "Electrical: GSUs, UATs, GCBs, R1-R4, EDGs",
    "BASE_UTILITIES": "BOP: pumps, coolers, pipe racks",
    "BASE_SWITCHYARD": "C Grid interface: 230 kV switchyard",
    "BASE_SERVICES": "F Controls / service",
    "BASE_WATER": "E Water / utilities",
    "BASE_FUEL": "D Fuel gas yard (+ conditional items)",
    "ADJ_MR": "Pipeline M&R (by pipeline operator)",
    "ROUTES_BASE": "Cable trays, bus, duct banks, 230 kV",
    "PROCESS_PIPING": "Process piping (steam, condensate, FW, CCW, gas)",
    "OPT_CCS": "Optional G: carbon capture (3 trains)",
    "OPT_CCSU": "Optional G: CCS utilities (cooling tower)",
    "OPT_BESS": "Optional H: BESS",
    "OPT_MOD": "Optional I: modular generation + black start",
    "OPT_TMP": "Optional I: portable / containerized power pad",
    "OPT_IC": "Optional J: GT inlet chilling",
    "OPT_LNG": "Adjacent K: LNG satellite",
    "OPT_H2": "Adjacent K: 25 MW green hydrogen",
    "OPT_D6": "Adjacent K: D6 future (H2) diameter",
    "OPT_ROUTES": "Optional-system routes",
}

model = dict(
    title="SK-3X1 Rev 14 - 3x1 combined-cycle plant, 3D coordinate model",
    units="feet", axes="X east, Y north, Z up; origin SW corner of compound",
    compound=[2420, 1920],
    disclaimer="Conceptual illustration. Not engineered. Not for construction.",
    source="SK-3X1 Drawing Set Rev 14 (Sept 26, 2026), Stephan Hardt | Power Generation Solutions",
    layers=LAYERS, objects=objects, routes=routes)

if __name__ == "__main__":
    out = os.path.join(HERE, "sk3x1_model.json")
    with open(out, "w") as f:
        json.dump(model, f, separators=(",", ":"))
    by_layer = {}
    for o in objects:
        by_layer[o["layer"]] = by_layer.get(o["layer"], 0) + 1
    print(f"wrote {out}: {len(objects)} objects, {len(routes)} route polylines")
    for k, v in by_layer.items():
        print(f"  {k:18s} {v}")
