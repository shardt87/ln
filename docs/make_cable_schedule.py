import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment

OUT = sys.argv[1]
F = "Arial"
BLUE = Font(name=F, color="0000FF", size=9)
BLACK = Font(name=F, size=9)
GREEN = Font(name=F, color="008000", size=9)
BOLD = Font(name=F, bold=True, size=9)
HDR = Font(name=F, bold=True, color="FFFFFF", size=9)
HFILL = PatternFill("solid", fgColor="1F3864")
HELPFILL = PatternFill("solid", fgColor="595959")
YELLOW = PatternFill("solid", fgColor="FFFF00")
SECT = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

wb = Workbook()

# ---------------------------------------------------------------- Cover
cv = wb.active
cv.title = "Cover"
cover = [
    ("CABLE SCHEDULE", BOLD),
    ("Combined Cycle Power Plant with Post-Combustion CCS, Gas Metering / LNG and Modular RICE Plant", BOLD),
    ("", None),
    ("Document No.", "CCPP-E-CS-0001"),
    ("Revision", "C (Preliminary - issued for review, NOT FOR CONSTRUCTION). Rev B: converted to US NEC practice - 13.8 kV / 480 V, AWG/kcmil, Type MC-HL armored cable. Rev C: CO2 compressor VFD line/output split; ACC fan local disconnects with flexible Machine Flex type VFD final drops."),
    ("Date", "2026-10-18"),
    ("Basis of layout", "Equipment positions from the 3D line-art model examples/powerplant.go (repo shardt87/ln, branch claude/powerplant-example). Coordinates in metres, site grid: X east, Y north, Z up. Lengths reported in metres and feet."),
    ("Basis of ratings", "Representative ratings for a ~1x1 F-class CCGT (GT ~290 MVA, ST ~175 MVA), amine CCS train, 8 x 2.5 MVA containerised gas engines, 230 kV switchyard. Ratings are typical values, NOT taken from a specific project. See 'Design Basis'."),
    ("Cable construction", "Power, VFD and control: 600 V and 15 kV Type MC-HL, Cu, XHHW-2 / EPR (MV-105) insulation, continuous corrugated welded aluminum armor (CCW) with PVC jacket - e.g. Southwire Armor-X (product named as an example of the construction only). Final drops to vibrating VFD-driven motors (ACC fans): flexible shielded VFD cable Type TC-ER with 3 symmetrical grounds - e.g. Southwire Machine Flex. Instrument: armored PLTC / ITC-HL. All tray-rated (-TC/-ER), sunlight resistant, UL 1685 / IEEE 1202 FT4. MC-HL with listed fittings is suitable for Class I Div 1 & 2 areas (gas metering, LNG, BOG) per NEC 501.10."),
    ("", None),
    ("Sheets", None),
    ("Design Basis", "Global inputs: route slack, termination allowance, sag allowance, wastage, voltage drop limits, standards."),
    ("Equipment", "Equipment / termination point list with site coordinates (from the 3D model)."),
    ("Cable Types", "Cable / conductor / busduct library: OD, ampacity, mV/A/m, mass, reel length."),
    ("Raceways", "Trays, trenches, duct banks, busducts, OHL - elevation, correction factor and fill check."),
    ("Cable Schedule", "One row per circuit. Route length, total length, running and design current, loading, voltage drop and check are all formulas."),
    ("BOQ Summary", "Quantities by cable type (with wastage, reels, mass) and by system."),
    ("References", "Public documents identified as references for typical arrangements, and cable product data."),
    ("", None),
    ("Legend", None),
    ("Blue text", "Hard-coded input - edit these"),
    ("Black text", "Formula - do not overwrite"),
    ("Green text", "Lookup from another sheet"),
    ("Yellow fill", "Key assumption to be verified against vendor / project data"),
    ("", None),
    ("Route length method", "M = Manhattan route along raceway: (|dX|+|dY| + rise from each end to raceway elevation) x (1+slack) + 2 x termination allowance.  D = direct span (overhead conductors): 3D distance x (1+sag allowance).  A value in 'Length Override' replaces the calculation (used for earth grids / bonds)."),
    ("Sizing", "Design current = running current x sizing factor: 1.25 for motors (NEC 430.22) and continuous loads (NEC 210.19 / 215.2), 1.15 for generator conductors (NEC 445.13), 1.00 for transformer secondaries / busduct. Allowable ampacity = base ampacity (NEC 310.16 75 C column for 600 V; NEC 311.60 for 15 kV) x raceway correction factor. Voltage drop uses NEC Ch. 9 Table 9 effective Z at 0.85 PF (AC) or Table 8 DC resistance."),
    ("Limitations", "Preliminary sizing only. Short-circuit withstand (ICEA P-32-382), motor starting voltage dip, ground fault return path, detailed tray fill per NEC 392.22 and ampacity per NEC 392.80 / IEEE 835 (Neher-McGrath for duct banks) must be verified at detailed design. Raceway fill counts each cable on its primary raceway only."),
]
for i, (a, b) in enumerate(cover, start=1):
    c = cv.cell(row=i, column=1, value=a)
    if isinstance(b, Font):
        c.font = Font(name=F, bold=True, size=14 if i == 1 else 11)
    else:
        c.font = BOLD
        if b is not None:
            d = cv.cell(row=i, column=2, value=b)
            d.font = BLACK
            d.alignment = WRAP
cv["A21"].font = Font(name=F, bold=True, color="0000FF", size=9)
cv["A23"].font = Font(name=F, bold=True, color="008000", size=9)
cv["A24"].fill = YELLOW
cv.column_dimensions["A"].width = 22
cv.column_dimensions["B"].width = 120

# ---------------------------------------------------------------- Design Basis
db = wb.create_sheet("Design Basis")
db["A1"] = "DESIGN BASIS - GLOBAL INPUTS"
db["A1"].font = Font(name=F, bold=True, size=12)
params = [
    ("Route slack / snaking allowance", 0.10, "0%", "Typical 5-15% on tray routes for bends, drops and snaking."),
    ("Termination allowance per end (m)", 3, "0.0", "Gland / connector, tail and dressing inside panel / terminal box."),
    ("Overhead conductor sag allowance", 0.03, "0%", "Conductor length over chord for strung bus and line spans."),
    ("Procurement wastage allowance", 0.05, "0%", "Applied in BOQ only."),
    ("Ambient air design temperature (deg C)", 40, "0", "Information - included in raceway correction factors (NEC 310.15(B) 0.88 for 75 C at 40 C)."),
    ("Earth thermal resistivity (RHO)", 90, "0", "Information - included in duct bank factors (IEEE 835 / NEC 311.60, RHO 90)."),
    ("Feet per metre", 3.28084, "0.00000", "Unit conversion."),
]
db["A3"] = "Parameter"; db["B3"] = ""; db["C3"] = "Value"; db["D3"] = "Note"
for c in ("A3", "C3", "D3"):
    db[c].font = HDR; db[c].fill = HFILL
for i, (name, val, fmt, note) in enumerate(params, start=4):
    db.cell(row=i, column=1, value=name).font = BLACK
    v = db.cell(row=i, column=3, value=val)
    v.font = BLUE; v.number_format = fmt
    if i < 10:
        v.fill = YELLOW
    db.cell(row=i, column=4, value=note).font = BLACK
SLACK, TERM, SAG, WASTE, FT = "'Design Basis'!$C$4", "'Design Basis'!$C$5", "'Design Basis'!$C$6", "'Design Basis'!$C$7", "'Design Basis'!$C$10"

db["A12"] = "System"; db["B12"] = "Nominal voltage"; db["C12"] = "Max steady-state voltage drop"; db["D12"] = "Note"
for c in ("A12", "B12", "C12", "D12"):
    db[c].font = HDR; db[c].fill = HFILL
systems = [
    ("HV Overhead", "230 kV", None, "Strung bus / OHL - checked for ampacity only."),
    ("Busduct", "18 / 19 kV IPB, 480 V LV busway", None, "Checked for ampacity only."),
    ("MV Power", "13.8 kV", 0.03, "Feeder volt drop, full load running."),
    ("LV Power", "480 V, 3-ph 3-wire + ground", 0.03, "NEC 215.2 / 210.19 informational notes: 3% feeder or branch, 5% total."),
    ("DC Power", "125 V DC / 120-208 V UPS", 0.03, "Battery / UPS to load."),
    ("Control", "120 V AC / 125 V DC", None, "Size by CT burden / voltage at coil - not checked here."),
    ("Instrument", "24 V DC / 4-20 mA / TC", None, "Not checked here."),
    ("Fibre Optic", "-", None, "-"),
    ("Earthing", "-", None, "Size per IEEE 80 fault study."),
]
for i, (s, vn, lim, note) in enumerate(systems, start=13):
    db.cell(row=i, column=1, value=s).font = BLUE
    db.cell(row=i, column=2, value=vn).font = BLUE
    c = db.cell(row=i, column=3, value=lim)
    c.font = BLUE; c.number_format = "0.0%"
    if lim is not None:
        c.fill = YELLOW
    db.cell(row=i, column=4, value=note).font = BLACK
SYS_FIRST, SYS_LAST = 13, 13 + len(systems) - 1
SYS_RANGE = f"'Design Basis'!$A${SYS_FIRST}:$A${SYS_LAST}"
VDL_RANGE = f"'Design Basis'!$C${SYS_FIRST}:$C${SYS_LAST}"

db["A24"] = "Design standards (reference)"
db["A24"].font = BOLD
stds = [
    "NFPA 70 (NEC) 2023: 310.16 / 311.60 ampacity, 330 Type MC, 392 cable tray, 430.22 motors, 445.13 generators, 501.10 Class I wiring, 725 PLTC, 727 ITC",
    "NEC Chapter 9 Tables 8 and 9: conductor DC resistance and AC effective impedance (voltage drop)",
    "UL 1569 Metal-Clad Cables; UL 2225 cables and fittings for hazardous locations (MC-HL)",
    "ICEA S-95-658 (NEMA WC70) 600 V cables; ICEA S-93-639 (NEMA WC74) 5-46 kV shielded power cables; ICEA S-73-532 control & instrument",
    "IEEE 835: Power cable ampacity tables; IEEE 525: Cable design and installation in substations",
    "IEEE 1202 / UL 1685: Vertical tray flame test (FT4)",
    "IEEE 738: Bare overhead conductor ampacity; IEEE C37.23: Metal-enclosed (isolated phase) bus",
    "IEEE 80: AC substation grounding",
]
for i, s in enumerate(stds, start=25):
    db.cell(row=i, column=1, value=s).font = BLACK
db.column_dimensions["A"].width = 40
db.column_dimensions["B"].width = 30
db.column_dimensions["C"].width = 28
db.column_dimensions["D"].width = 70

# ---------------------------------------------------------------- Equipment
eq = wb.create_sheet("Equipment")
E = [
    # tag, description, area, x, y, z, model reference
    # 10 Switchyard / HV
    ("SWY-B1", "230 kV bay 1 - RICE transformer bay (gantry dead-end)", "10", 20, 137.5, 12.5, "Gantry x=20"),
    ("SWY-B2", "230 kV bay 2 - bus coupler (gantry dead-end)", "10", 40, 137.5, 12.5, "Gantry x=40"),
    ("SWY-B3", "230 kV bay 3 - GT generator bay (gantry dead-end)", "10", 60, 137.5, 12.5, "Gantry x=60"),
    ("SWY-B4", "230 kV bay 4 - ST generator bay / line exit (gantry dead-end)", "10", 80, 137.5, 12.5, "Gantry x=80"),
    ("TWR-01", "230 kV transmission tower 1 (terminal)", "10", 130, 137.5, 31.5, "Tower x=130"),
    ("TWR-02", "230 kV transmission tower 2 (suspension)", "10", 200, 152.5, 31.5, "Tower x=200"),
    ("TWR-03", "230 kV transmission tower 3 (suspension)", "10", 270, 167.5, 31.5, "Tower x=270"),
    ("SWY-RB", "Switchyard relay & control building", "10", 95, 128, 0.5, "Not drawn - assumed"),
    ("RICE-TX-HV", "RICE step-up transformer 11/230 kV 22 MVA - HV bushings", "50", 19, 107.5, 8, "Transformer at (14-20,105-110)"),
    ("RICE-TX-LV", "RICE step-up transformer 11/230 kV 22 MVA - LV cable box", "50", 14.5, 107.5, 2, "Transformer at (14-20,105-110)"),
    # 20 Power block
    ("GEN-GT", "Gas turbine generator ~290 MVA, 19 kV - line terminals", "20", 58, 18, 4, "GT generator box (52-64,10-18)"),
    ("GEN-ST", "Steam turbine generator ~175 MVA, 18 kV - line terminals", "20", 60, 46, 6, "ST hall north wall"),
    ("GSU-GT-HV", "GT step-up transformer 19/230 kV 290 MVA - HV bushings", "20", 54, 65.5, 10, "Transformer(50,60)"),
    ("GSU-GT-LV", "GT step-up transformer - LV bushings / marshalling box", "20", 54, 60, 4.5, "Transformer(50,60)"),
    ("GSU-ST-HV", "ST step-up transformer 18/230 kV 175 MVA - HV bushings", "20", 74, 65.5, 10, "Transformer(70,60)"),
    ("GSU-ST-LV", "ST step-up transformer - LV bushings / marshalling box", "20", 74, 60, 4.5, "Transformer(70,60)"),
    ("UAT-1", "Unit auxiliary transformer 1, 19/11.5 kV 45 MVA", "20", 44, 64, 3, "Not drawn - west of GSU-GT"),
    ("UAT-2", "Unit auxiliary transformer 2, 18/11.5 kV 30 MVA (feeds CCS)", "20", 86, 64, 3, "Not drawn - east of GSU-ST"),
    ("NGR-GT", "GT generator neutral grounding transformer cubicle", "20", 62, 18, 1, "Assumed"),
    ("NGR-ST", "ST generator neutral grounding transformer cubicle", "20", 64, 46, 1, "Assumed"),
    ("LCI-TX", "GT static starter (LCI) isolation transformer 8 MVA", "20", 40, -6, 0.5, "GT PEECC - assumed"),
    ("LCI-GT", "GT static starter (LCI) cubicle", "20", 44, -6, 0.5, "GT PEECC - assumed"),
    ("GTCP", "GT control panel (in PEECC)", "20", 46, -6, 0.5, "GT PEECC - assumed"),
    ("MCC-GT", "GT auxiliary MCC 400 V (in PEECC)", "20", 48, -6, 0.5, "GT PEECC - assumed"),
    ("M-GT-LOP", "GT AC lube oil pump motor 75 kW", "20", 60, -5, 0.5, "GT enclosure (42-70,-3..7)"),
    ("M-GT-ELOP", "GT DC emergency lube oil pump motor 15 kW", "20", 61, -5, 0.5, "GT enclosure"),
    ("M-GT-VNT-A", "GT enclosure ventilation fan A 45 kW", "20", 52, 6.5, 11, "Roof vent package (46-66,-2.5..6.5)"),
    ("M-GT-VNT-B", "GT enclosure ventilation fan B 45 kW", "20", 60, 6.5, 11, "Roof vent package"),
    ("JB-GT-TC", "GT exhaust thermocouple junction box", "20", 72, 2, 6, "Exhaust diffuser (70-76)"),
    ("JB-FG-GT", "F&G junction box - GT enclosure", "20", 60, -3, 1, "GT enclosure"),
    ("MCC-HRSG", "HRSG auxiliary MCC 400 V", "20", 80, -9, 0.5, "Assumed south of HRSG"),
    ("M-BFP-A", "HP/IP boiler feed pump A motor 3.2 MW, 11 kV", "20", 86, -9, 0.5, "South of HRSG"),
    ("M-BFP-B", "HP/IP boiler feed pump B motor 3.2 MW, 11 kV", "20", 90, -9, 0.5, "South of HRSG"),
    ("M-HRSG-RCP", "HRSG preheater recirculation pump motor 55 kW", "20", 100, -8, 0.5, "South of HRSG"),
    ("JB-HRSG-01", "HRSG drum platform instrument junction box", "20", 97, -6, 30, "HP drum z=30"),
    ("STK", "HRSG stack (lightning down conductor)", "20", 117, 3, 55, "Stack r=3.5, h=55"),
    ("AE-STK", "CEMS probe at stack sample port", "20", 117, -0.5, 40, "Stack"),
    ("CEMS-SH", "CEMS analyser shelter", "20", 122, -8, 0.5, "Assumed"),
    ("TCP-ST", "ST control panel", "20", 85, 40, 0.5, "ST hall (52-92,28-46)"),
    ("MCC-ST", "ST auxiliary MCC 400 V", "20", 88, 30, 0.5, "ST hall"),
    ("M-ST-TG", "ST turning gear motor 37 kW", "20", 66, 36, 6, "ST at (60-72,32-40)"),
    ("M-ST-LOP", "ST AC lube oil pump motor 55 kW", "20", 70, 30, 0.5, "ST hall"),
    ("M-ST-ELOP", "ST DC emergency lube oil pump motor 22 kW", "20", 72, 30, 0.5, "ST hall"),
    ("M-CEP-A", "Condensate extraction pump A motor 500 kW, 11 kV", "20", 88, 44, 0.5, "ST hall"),
    ("M-CEP-B", "Condensate extraction pump B motor 500 kW, 11 kV", "20", 88, 41, 0.5, "ST hall"),
    ("RIO-PB", "DCS remote I/O cabinet - power block", "20", 68, 22, 0.5, "Assumed"),
    ("EG-PB", "Power block main earth grid (nearest riser)", "20", 75, 20, -0.8, "Buried"),
    # 30 ACC
    ("LVT-ACC", "ACC fan transformer 11/0.69 kV 4 MVA", "30", 146, 40, 0.5, "East of ACC (98-142,26-60)"),
    ("MCC-ACC", "ACC fan VFD switchroom 690 V", "30", 146, 46, 0.5, "East of ACC"),
    ("JB-ACC", "ACC instrument junction box", "30", 142, 30, 0.5, "ACC"),
]
fan = 1
for x in (104, 112, 120, 128, 136):
    for y in (32, 43, 54):
        E.append((f"M-ACC-{fan:02d}", f"ACC fan motor {fan:02d}, 200 kW 690 V (VFD)", "30", x, y, 20.5, f"Fan ring ({x},{y}) on deck z=20"))
        E.append((f"DS-ACC-{fan:02d}", f"ACC fan {fan:02d} local disconnect switch (in sight of motor, NEC 430.102)", "30", x + 4, y, 20.5, f"Fan bridge beside ring ({x},{y})"))
        fan += 1
E += [
    # 40 CCS
    ("MVS-CCS", "CCS 11 kV switchboard (CCS substation)", "40", 178, 58, 0.5, "Tray TR-02 end (180,64)"),
    ("LVT-CCS", "CCS LV transformer 11/0.42 kV 2.5 MVA", "40", 182, 60, 0.5, "CCS substation"),
    ("PMCC-CCS", "CCS power / motor control centre 400 V", "40", 176, 60, 0.5, "CCS substation"),
    ("RIO-CCS", "DCS remote I/O cabinet - CCS", "40", 174, 58, 0.5, "CCS substation"),
    ("M-BF", "Flue gas booster fan motor 6.5 MW, 11 kV", "40", 150, -4, 0.5, "Booster fan (145-155,-8..0)"),
    ("M-DCC-A", "Direct contact cooler circulation pump A 400 kW, 11 kV", "40", 146, 6, 0.5, "DCC r=5 at (150,3)"),
    ("M-DCC-B", "Direct contact cooler circulation pump B 400 kW, 11 kV", "40", 146, 9, 0.5, "DCC"),
    ("M-RAP-A", "Rich amine pump A 700 kW, 11 kV", "40", 174, 16, 0.5, "Absorber r=8 at (170,6)"),
    ("M-RAP-B", "Rich amine pump B 700 kW, 11 kV", "40", 177, 16, 0.5, "Absorber"),
    ("M-LAP-A", "Lean amine pump A 800 kW, 11 kV", "40", 186, 12, 0.5, "Stripper r=4 at (190,20)"),
    ("M-LAP-B", "Lean amine pump B 800 kW, 11 kV", "40", 186, 15, 0.5, "Stripper"),
    ("M-RBC-A", "Reboiler condensate pump A 110 kW, 400 V", "40", 200, 24, 0.5, "Reboiler at (198,20)"),
    ("M-CO2C", "CO2 compressor motor 14 MW, 11 kV (VFD)", "40", 195, 39, 0.5, "Compressor bldg (180-210,32-46)"),
    ("UCP-CO2", "CO2 compressor unit control panel", "40", 192, 34, 0.5, "Compressor bldg"),
    ("VFD-CO2", "CO2 compressor MV variable frequency drive, 13.8 kV in / out", "40", 186, 40, 0.5, "Compressor bldg - assumed"),
    ("PKG-DEH", "CO2 dehydration package (TEG) 250 kVA", "40", 214, 39, 0.5, "Dehydration (210-218,34-44)"),
    ("FC-CO2", "CO2 export fiscal meter skid / flow computer", "40", 242, 39, 1, "Meter skid (240-244,37-41)"),
    ("JB-ABS-01", "Absorber instrument junction box (mid-height)", "40", 170, -2.5, 30, "Absorber"),
    ("JB-STR-01", "Stripper instrument junction box", "40", 190, 15.5, 20, "Stripper"),
    ("JB-FG-CCS", "F&G junction box - CCS area", "40", 172, -3, 1, "CCS"),
    ("C-ABS", "Absorber column shell (lightning / bonding)", "40", 170, 6, 0, "Absorber"),
    ("EG-CCS", "CCS area earth grid (nearest riser)", "40", 190, 25, -0.8, "Buried"),
    # 50 RICE
    ("MVS-RICE", "RICE 11 kV collector switchgear e-house", "50", 12, 99, 0.5, "E-house (6-18,96-102)"),
    ("LVT-RICE", "RICE auxiliary transformer 11/0.42 kV 1 MVA", "50", 10, 104, 0.5, "Assumed"),
    ("MCC-RICE", "RICE auxiliary MCC 400 V", "50", 16, 99, 0.5, "E-house"),
    ("RPC", "RICE plant controller", "50", 8, 99, 0.5, "E-house"),
    ("EG-RICE", "RICE area earth grid (nearest riser)", "50", -4, 85, -0.8, "Buried"),
]
for i in range(8):
    y = 70 + i * 4.2 + 1.45
    E.append((f"GEN-R{i+1:02d}", f"Gas engine genset {i+1} (40 ft container) 2.5 MVA, 11 kV - terminal box", "50", 2.2, round(y, 2), 1.5, f"Container y={70+i*4.2:.1f}"))
for i in range(8):
    y = 70 + i * 4.2 + 1.45
    E.append((f"AUX-R{i+1:02d}", f"Genset {i+1} auxiliary panel (radiator fans, pre-lube, jacket heater)", "50", -4, round(y, 2), 1, f"Container y={70+i*4.2:.1f}"))
E += [
    # 60 Gas / LNG
    ("TK-LNG", "LNG full-containment tank (bonding)", "60", -60, 10, 0, "Tank r=16 at (-60,10)"),
    ("M-LNG-P1", "LNG in-tank send-out pump 1, 250 kW 400 V (top penetration)", "60", -60, 10, 24, "Tank roof z=24"),
    ("M-LNG-P2", "LNG in-tank send-out pump 2, 250 kW 400 V (top penetration)", "60", -58, 12, 24, "Tank roof z=24"),
    ("LT-LNG", "LNG tank level / temperature gauging head", "60", -60, -6, 24, "Tank roof"),
    ("C-BOG", "Boil-off gas compressor motor 900 kW, 11 kV", "60", -45, 25, 0.5, "Assumed north of vaporizers"),
    ("JB-LNG", "LNG area instrument junction box", "60", -44, 8, 0.5, "Pipe to station y=10"),
    ("HTP-LNG", "Heat tracing / lighting panel - LNG area", "60", -42, 4, 0.5, "Assumed"),
    ("XV-001", "Station inlet ESD valve (electro-hydraulic actuator)", "60", -24, 10, 4, "Inlet pipe (-44..-25, y=10, z=4)"),
    ("LVT-GAS", "Gas station transformer 11/0.42 kV 1.6 MVA", "60", -12, 16, 0.5, "Assumed north of skid"),
    ("MCC-GAS", "Gas station MCC 400 V (shelter)", "60", -20, 12, 0.5, "Shelter (-25..-15,10-14)"),
    ("RIO-GAS", "DCS remote I/O cabinet - gas station (shelter)", "60", -18, 12, 0.5, "Shelter"),
    ("FC-GAS", "Fiscal gas flow computer / metering panel (shelter)", "60", -17, 12, 0.5, "Shelter"),
    ("AT-GC", "Gas chromatograph (shelter)", "60", -22, 12, 0.5, "Shelter"),
    ("FT-101A", "Ultrasonic gas meter run A", "60", -7.25, -3, 2.2, "Meter body run y=-3"),
    ("FT-101B", "Ultrasonic gas meter run B", "60", -7.25, 0, 2.2, "Meter body run y=0"),
    ("FT-101C", "Ultrasonic gas meter run C (spare / check)", "60", -7.25, 3, 2.2, "Meter body run y=3"),
    ("PCV-101", "Pressure reducing / regulating valve skid", "60", 1.5, 1.5, 2.5, "Regulator box (0-3,0-3)"),
    ("H-101", "Fuel gas electric heater 400 kW", "60", 2, 7, 1.5, "Heater (0-4, y=7)"),
    ("JB-GAS", "Gas station instrument junction box", "60", -10, 8, 0.5, "Skid"),
    ("EG-GAS", "Gas / LNG area earth grid (nearest riser)", "60", -30, 5, -0.8, "Buried"),
    # 70 Main electrical building
    ("MVS-1", "Main 11 kV switchboard (main electrical building)", "70", 36, 52, 0.5, "E-house (34-46,50-56)"),
    ("PMCC-1", "Main power / motor control centre 400 V", "70", 44, 52, 0.5, "E-house"),
    ("LVT-1", "Main LV transformer 11/0.42 kV 2.5 MVA", "70", 34, 57, 0.5, "North of e-house"),
    ("DCS-CCR", "DCS servers / central control room", "70", 40, 55, 0.5, "E-house"),
    ("GPP", "Generator & transformer protection panels", "70", 38, 55, 0.5, "E-house"),
    ("DCB-1", "125 V DC battery and chargers", "70", 42, 55, 0.5, "E-house"),
    ("UPS-1", "230 V AC UPS", "70", 43, 55, 0.5, "E-house"),
    ("FGP-1", "Fire & gas panel", "70", 39, 55.5, 0.5, "E-house"),
    ("EG-SWY", "Switchyard earth grid (nearest riser)", "10", 50, 137.5, -0.8, "Buried"),
]
US_TEXT = [
    ("19/11.5 kV", "19/13.8 kV"), ("18/11.5 kV", "18/13.8 kV"), ("11/230 kV", "13.8/230 kV"),
    ("11/0.69 kV 4 MVA", "13.8/0.48 kV 3 MVA"), ("11/0.42 kV", "13.8/0.48 kV"),
    ("200 kW 690 V", "150 kW 480 V"), ("690 V", "480 V"), ("400 V", "480 V"), ("11 kV", "13.8 kV"),
]
def us(s):
    for a, b in US_TEXT:
        s = s.replace(a, b)
    return s
E = [(t, us(d), *rest) for t, d, *rest in E]
eh = ["Tag", "Description", "Area", "X (m)", "Y (m)", "Z term. (m)", "Location in 3D model / basis"]
for j, h in enumerate(eh, start=1):
    c = eq.cell(row=1, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.alignment = CENTER; c.border = BORDER
for i, row in enumerate(E, start=2):
    for j, val in enumerate(row, start=1):
        c = eq.cell(row=i, column=j, value=val)
        c.font = BLUE if j in (1, 2, 3, 4, 5, 6) else BLACK
        c.border = BORDER
        if j in (4, 5, 6):
            c.number_format = "0.0"
    if "assumed" in row[6].lower() or "not drawn" in row[6].lower():
        eq.cell(row=i, column=7).fill = YELLOW
EQ_LAST = len(E) + 1
for col, w in zip("ABCDEFG", (13, 62, 6, 8, 8, 10, 36)):
    eq.column_dimensions[col].width = w
eq.freeze_panes = "B2"
eq.auto_filter.ref = f"A1:G{EQ_LAST}"
tags = [r[0] for r in E]
assert len(tags) == len(set(tags)), "duplicate tag"
EQ_TAG = f"Equipment!$A$2:$A${EQ_LAST}"
def EQCOL(c):
    return f"Equipment!${c}$2:${c}${EQ_LAST}"

# ---------------------------------------------------------------- Cable types
ct = wb.create_sheet("Cable Types")

# Voltage drop factors from NEC Chapter 9.
# 3-phase AC: line-to-line drop per A per m = sqrt(3) x Z(ohm/kft) / 304.8 m  ->  mV/A/m = 5.683 x Z
# DC / 1-phase: loop drop = 2 x R(ohm/kft) / 304.8 m                           ->  mV/A/m = 6.562 x R
Z085 = {"2/0": 0.10, "10": 1.1, "6": 0.45, "2": 0.19, "1/0": 0.12, "4/0": 0.069, "350": 0.048, "500": 0.039}  # Table 9, Cu, Al conduit, 0.85 PF
RDC = {"10": 1.24, "6": 0.491, "2": 0.194, "500": 0.0258}  # Table 8, Cu uncoated, 75 C
ZMV = {"2": 0.188, "1/0": 0.126, "4/0": 0.075, "500": 0.045, "750": 0.037, "1000": 0.033}  # 15 kV shielded, R cos + X sin at 0.85 PF
def mv3(z):
    return round(5.683 * z, 3)
def mvdc(r):
    return round(6.562 * r, 3)

MCHL = "Type MC-HL, CCW Al armor (Armor-X type), PVC jkt"
# code, description, category, conductors per run, OD mm, base ampacity A per run, mV/A/m, kg/m per conductor, reel m
T = [
    ("ACSR-DRAKE", "ACSR 795 kcmil 'Drake' 26/7, 1 per phase", "HV Overhead", 3, 28.1, 900, None, 1.628, 2000),
    ("ACSR-DRAKE-2B", "ACSR 795 kcmil 'Drake' 26/7, twin bundle per phase", "HV Overhead", 6, 28.1, 1800, None, 1.628, 2000),
    ("SW-7/16-EHS", "Shield wire 7/16\" EHS galvanized steel", "HV Overhead", 1, 11.1, None, None, 0.595, 3000),
    ("OPGW-24", "OPGW 24-fiber shield wire", "HV Overhead", 1, 14.0, None, None, 0.62, 4000),
    ("IPB-10K", "Isolated phase bus 24 kV, 10 kA (per phase metre)", "Busduct", 3, None, 10000, None, 160, None),
    ("IPB-7K", "Isolated phase bus 24 kV, 7 kA (per phase metre)", "Busduct", 3, None, 7000, None, 120, None),
    ("IPB-3K", "Isolated phase tap bus 24 kV, 3 kA (per phase metre)", "Busduct", 3, None, 3000, None, 70, None),
    ("LVBD-4000", "600 V busway 4000 A, Cu, 3-ph + ground, outdoor feeder", "Busduct", 1, None, 4000, None, 45, None),
    ("LVBD-2500", "600 V busway 2500 A, Cu, 3-ph + ground, outdoor feeder", "Busduct", 1, None, 2500, None, 30, None),
    ("MV-1C-2-NGR", f"15 kV MV-105 1/C #2 AWG Cu EPR 133% shielded, {MCHL}", "MV Power", 1, 33, 195, None, 1.6, 300),
    ("MV-3C-2", f"15 kV MV-105 3/C #2 AWG Cu EPR 133% shielded + GC, {MCHL}", "MV Power", 1, 61, 165, mv3(ZMV["2"]), 4.0, 300),
    ("MV-3C-1/0", f"15 kV MV-105 3/C 1/0 AWG Cu EPR 133% shielded + GC, {MCHL}", "MV Power", 1, 66, 215, mv3(ZMV["1/0"]), 5.3, 300),
    ("MV-3C-4/0", f"15 kV MV-105 3/C 4/0 AWG Cu EPR 133% shielded + GC, {MCHL}", "MV Power", 1, 76, 310, mv3(ZMV["4/0"]), 8.0, 300),
    ("MV-3C-500", f"15 kV MV-105 3/C 500 kcmil Cu EPR 133% shielded + GC, {MCHL}", "MV Power", 1, 94, 515, mv3(ZMV["500"]), 15.5, 300),
    ("MV-1C-500-TPX", f"15 kV MV-105 1/C 500 kcmil Cu EPR 133% shielded, {MCHL}, triplexed set", "MV Power", 3, 41, 585, mv3(ZMV["500"]), 4.4, 300),
    ("MV-1C-750-TPX", f"15 kV MV-105 1/C 750 kcmil Cu EPR 133% shielded, {MCHL}, triplexed set", "MV Power", 3, 46, 740, mv3(ZMV["750"]), 6.2, 300),
    ("MV-1C-1000-TPX", f"15 kV MV-105 1/C 1000 kcmil Cu EPR 133% shielded, {MCHL}, triplexed set", "MV Power", 3, 51, 860, mv3(ZMV["1000"]), 7.9, 300),
    ("LV-3C-10", f"600 V 3/C #10 AWG + G Cu XHHW-2, {MCHL}", "LV Power", 1, 20, 35, mv3(Z085["10"]), 0.6, 600),
    ("LV-3C-6", f"600 V 3/C #6 AWG + G Cu XHHW-2, {MCHL}", "LV Power", 1, 24, 65, mv3(Z085["6"]), 0.95, 600),
    ("LV-3C-2", f"600 V 3/C #2 AWG + G Cu XHHW-2, {MCHL}", "LV Power", 1, 31, 115, mv3(Z085["2"]), 1.8, 600),
    ("LV-3C-1/0", f"600 V 3/C 1/0 AWG + G Cu XHHW-2, {MCHL}", "LV Power", 1, 37, 150, mv3(Z085["1/0"]), 2.6, 300),
    ("LV-3C-4/0", f"600 V 3/C 4/0 AWG + G Cu XHHW-2, {MCHL}", "LV Power", 1, 47, 230, mv3(Z085["4/0"]), 4.6, 300),
    ("LV-3C-350", f"600 V 3/C 350 kcmil + G Cu XHHW-2, {MCHL}", "LV Power", 1, 57, 310, mv3(Z085["350"]), 7.2, 300),
    ("LV-3C-500", f"600 V 3/C 500 kcmil + G Cu XHHW-2, {MCHL}", "LV Power", 1, 66, 380, mv3(Z085["500"]), 9.8, 300),
    ("LV-VFD-500", f"600/1000 V VFD 3/C 500 kcmil + 3 symmetrical G, Cu XLPE, {MCHL}", "LV Power", 1, 70, 380, mv3(Z085["500"]), 11.0, 300),
    ("LV-MFX-2/0", "1000 V 3/C 2/0 AWG + 3 symmetrical G, flexible tinned Cu XHHW-2, foil + braid shield, TPE jkt, Type TC-ER, NFPA 79 (Machine Flex type)", "LV Power", 1, 38, 175, mv3(Z085["2/0"]), 2.6, 300),
    ("LV-2C-10", f"600 V 2/C #10 AWG + G Cu XHHW-2, {MCHL}", "DC Power", 1, 18, 35, mvdc(RDC["10"]), 0.5, 600),
    ("LV-2C-6", f"600 V 2/C #6 AWG + G Cu XHHW-2, {MCHL}", "DC Power", 1, 22, 65, mvdc(RDC["6"]), 0.8, 600),
    ("LV-2C-2", f"600 V 2/C #2 AWG + G Cu XHHW-2, {MCHL}", "DC Power", 1, 28, 115, mvdc(RDC["2"]), 1.4, 600),
    ("LV-1C-500", f"600 V 1/C 500 kcmil Cu XHHW-2, {MCHL} (+/- pair)", "DC Power", 2, 34, 465, mvdc(RDC["500"]), 3.3, 300),
    ("CTL-7C-12", f"600 V 7/C #12 AWG Cu XHHW-2 control, {MCHL}", "Control", 1, 19, None, None, 0.6, 600),
    ("CTL-12C-14", f"600 V 12/C #14 AWG Cu XHHW-2 control, {MCHL}", "Control", 1, 21, None, None, 0.7, 600),
    ("CTL-25C-14", f"600 V 25/C #14 AWG Cu XHHW-2 control, {MCHL}", "Control", 1, 27, None, None, 1.1, 600),
    ("CTL-12C-10", f"600 V 12/C #10 AWG Cu XHHW-2 control (CT circuits), {MCHL}", "Control", 1, 27, None, None, 1.2, 600),
    ("INS-1TSP-16", "300 V 1 TSP #16 AWG, PLTC/ITC-HL, CCW armor, PVC jkt (IS blue)", "Instrument", 1, 13, None, None, 0.25, 600),
    ("INS-2TSP-16", "300 V 2 TSP #16 AWG, PLTC/ITC-HL, CCW armor, PVC jkt (IS blue)", "Instrument", 1, 16, None, None, 0.35, 600),
    ("INS-12TSP-18", "300 V 12 TSP #18 AWG indiv. + overall shield, PLTC/ITC-HL, CCW armor", "Instrument", 1, 30, None, None, 0.9, 600),
    ("INS-24TSP-18", "300 V 24 TSP #18 AWG indiv. + overall shield, PLTC/ITC-HL, CCW armor", "Instrument", 1, 38, None, None, 1.4, 600),
    ("INS-TC-12P-KX", "300 V 12 pair #16 AWG type KX thermocouple extension, ITC-HL, CCW armor", "Instrument", 1, 30, None, None, 0.8, 600),
    ("INS-RS485", "300 V 1 TSP #22 AWG 120 ohm RS-485, ITC-HL, CCW armor", "Instrument", 1, 12, None, None, 0.2, 600),
    ("FO-24SM", "24-fiber single-mode OFCR, interlocked Al armor", "Fibre Optic", 1, 19, None, None, 0.30, 2000),
    ("FO-48SM", "48-fiber single-mode OFCR, interlocked Al armor", "Fibre Optic", 1, 21, None, None, 0.36, 2000),
    ("EG-CU-4/0", "Bare stranded Cu 4/0 AWG ground grid conductor (buried)", "Earthing", 1, 13.3, None, None, 0.97, 300),
    ("EB-CU-2/0", "Green insulated Cu 2/0 AWG bonding jumper", "Earthing", 1, 15, None, None, 0.62, 300),
]
th = ["Code", "Description", "Category", "Conductors / cables per run", "OD (mm)", "Base ampacity per run (A)", "mV/A/m (3-ph line, or 1-ph/DC loop)", "Mass (kg/m per conductor)", "Std reel length (m)", "Basis"]
for j, h in enumerate(th, start=1):
    c = ct.cell(row=1, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.alignment = CENTER; c.border = BORDER
basis = {
    "HV Overhead": "IEEE 738 typical (40 C ambient, 75 C conductor, 2 ft/s wind)",
    "Busduct": "Vendor nominal rating (IEEE C37.23 / UL 857)",
    "MV Power": "NEC 311.60(C) 15 kV Cu 90 C in air, 40 C ambient (approx.); VD from R cos + X sin at 0.85 PF",
    "LV Power": "NEC 310.16 Cu 75 C column (termination limit); NEC 392.80(A)(1); VD NEC Ch.9 Table 9, 0.85 PF",
    "DC Power": "NEC 310.16 75 C (1/C in tray: 392.80(A)(2), 75% of 310.17); VD NEC Ch.9 Table 8 DC loop",
    "Control": "Not current-rated here",
    "Instrument": "Not current-rated here",
    "Fibre Optic": "-",
    "Earthing": "Size per IEEE 80 fault study",
}
for i, row in enumerate(T, start=2):
    for j, val in enumerate(row, start=1):
        c = ct.cell(row=i, column=j, value=val)
        c.font = BLUE
        c.border = BORDER
    ct.cell(row=i, column=10, value=basis[row[2]]).font = BLACK
    ct.cell(row=i, column=10).border = BORDER
    ct.cell(row=i, column=6).fill = YELLOW if row[5] is not None else PatternFill()
    ct.cell(row=i, column=7).number_format = "0.000"
CT_LAST = len(T) + 1
for col, w in zip("ABCDEFGHIJ", (15, 78, 12, 12, 8, 12, 14, 12, 12, 70)):
    ct.column_dimensions[col].width = w
ct.freeze_panes = "B2"
CT_CODE = f"'Cable Types'!$A$2:$A${CT_LAST}"
def CTCOL(c):
    return f"'Cable Types'!${c}$2:${c}${CT_LAST}"

# ---------------------------------------------------------------- Raceways
rw = wb.create_sheet("Raceways")
R = [
    # id, description, type, elevation, width mm, usable depth mm, tiers, max fill, derate
    ("OHL", "Overhead strung conductors (switchyard / line)", "Overhead", None, None, None, None, None, 1.0),
    ("IPB-GT", "Isolated phase bus route GT generator -> GSU / UAT-1", "Busduct", 4, None, None, None, None, 1.0),
    ("IPB-ST", "Isolated phase bus route ST generator -> GSU / UAT-2", "Busduct", 4, None, None, None, None, 1.0),
    ("BD", "LV busduct, transformer to switchboard (local)", "Busduct", 3, None, None, None, None, 1.0),
    ("TR-01", "Ladder tray: main electrical bldg -> GT / HRSG (40,50 -> 40,20 -> 46,20)", "Tray", 5, 900, 100, 4, 0.40, 0.88),
    ("TR-02", "Ladder tray: main electrical bldg -> ACC -> CCS (46,53 -> 140,53 -> 140,64 -> 180,64 -> 180,40)", "Tray", 5, 900, 100, 4, 0.40, 0.88),
    ("TR-03", "Ladder tray: main electrical bldg -> gas station / LNG (40,50 -> -4,50 -> -4,14)", "Tray", 5, 900, 100, 3, 0.40, 0.88),
    ("TR-04", "Ladder tray: RICE gensets -> collector e-house (4,70 -> 4,104 -> 12,104)", "Tray", 3, 1000, 100, 3, 0.40, 0.88),
    ("TR-05", "Ladder tray: CCS internal (substation -> absorber / stripper / compressor)", "Tray", 6, 900, 100, 4, 0.40, 0.88),
    ("TR-06", "Ladder tray: ACC VFD room -> fan deck, 2 risers (east / west) x 600 mm, single layer for 500 kcmil (NEC 392.22)", "Tray", 20, 600, 100, 4, 0.40, 0.88),
    ("TR-07", "Ladder tray: gas station / LNG local", "Tray", 3, 600, 100, 3, 0.40, 0.88),
    ("TR-08", "Concrete cable trench: switchyard bays -> relay building", "Trench", -0.8, 1000, 600, 1, 0.40, 0.88),
    ("DB-01", "Duct bank: main electrical bldg / transformer yard -> switchyard relay bldg", "Duct bank", -1.2, 1200, 600, 1, 0.30, 0.70),
    ("DB-02", "Duct bank: RICE e-house -> main electrical bldg", "Duct bank", -1.2, 900, 600, 1, 0.30, 0.70),
    ("DB-03", "Duct bank: UAT-1 -> main 13.8 kV switchgear", "Duct bank", -1.2, 1200, 600, 1, 0.30, 0.70),
    ("LOCAL", "Local tray / conduit within a building or package", "Local", 1, None, None, None, None, 0.88),
    ("EG", "Buried earth grid / bonding", "Buried", -0.8, None, None, None, None, None),
]
rh = ["Raceway ID", "Description", "Type", "Elevation (m)", "Width (mm)", "Usable depth (mm)", "Tiers", "Max fill", "Correction factor", "Capacity (mm2)", "Cable area used (mm2)", "Fill (% of max)", "Check"]
for j, h in enumerate(rh, start=1):
    c = rw.cell(row=1, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.alignment = CENTER; c.border = BORDER
R_LAST = len(R) + 1
for i, row in enumerate(R, start=2):
    for j, val in enumerate(row, start=1):
        c = rw.cell(row=i, column=j, value=val)
        c.font = BLUE; c.border = BORDER
    rw.cell(row=i, column=8).number_format = "0%"
    rw.cell(row=i, column=9).number_format = "0.00"
    if row[8] is not None and row[2] in ("Tray", "Duct bank", "Trench", "Local"):
        rw.cell(row=i, column=9).fill = YELLOW
    rw.cell(row=i, column=10, value=f'=IF(E{i}="","",E{i}*F{i}*G{i}*H{i})')
    rw.cell(row=i, column=11, value=f"=SUMIFS('Cable Schedule'!$AF:$AF,'Cable Schedule'!$L:$L,A{i})")
    rw.cell(row=i, column=12, value=f'=IF(J{i}="","",K{i}/J{i})')
    rw.cell(row=i, column=13, value=f'=IF(J{i}="","n/a",IF(L{i}<=1,"OK","OVERFILL"))')
    for j in (10, 11, 12, 13):
        c = rw.cell(row=i, column=j); c.font = BLACK; c.border = BORDER
    rw.cell(row=i, column=10).number_format = "#,##0"
    rw.cell(row=i, column=11).number_format = "#,##0"
    rw.cell(row=i, column=12).number_format = "0%"
for col, w in zip("ABCDEFGHIJKLM", (10, 70, 10, 10, 10, 10, 7, 8, 10, 12, 14, 12, 11)):
    rw.column_dimensions[col].width = w
rw.freeze_panes = "B2"
rw.conditional_formatting.add(f"M2:M{R_LAST}", CellIsRule(operator="equal", formula=['"OVERFILL"'], fill=PatternFill("solid", fgColor="F4B084")))
RW_ID = f"Raceways!$A$2:$A${R_LAST}"
def RWCOL(c):
    return f"Raceways!${c}$2:${c}${R_LAST}"

# ---------------------------------------------------------------- Cable schedule rows
C = []  # (no, area, system, service, from, to, type, runs, raceway, method, override, V, ph, load, pf, sf, note)
def add(no, area, system, service, frm, to, typ, runs=1, rway="LOCAL", method="M", override=None, V=None, ph=None, load=None, pf=None, sf=None, note=""):
    if load is not None and sf is None:
        sf = 1.25
    C.append((no, area, system, service, frm, to, typ, runs, rway, method, override, V, ph, load, pf, sf, note))

HZ = "MC-HL with listed Class I fittings (NEC 501.10)"
# HV overhead
add("10-HV-001", "10", "HV Overhead", "GT GSU 230 kV to bay 3 (strung)", "GSU-GT-HV", "SWY-B3", "ACSR-DRAKE", 1, "OHL", "D", None, 230000, 3, 290000, 1, 1.0, "Load in kVA")
add("10-HV-002", "10", "HV Overhead", "ST GSU 230 kV to bay 4 (strung)", "GSU-ST-HV", "SWY-B4", "ACSR-DRAKE", 1, "OHL", "D", None, 230000, 3, 175000, 1, 1.0, "Load in kVA")
add("10-HV-003", "10", "HV Overhead", "RICE transformer 230 kV to bay 1 (strung)", "RICE-TX-HV", "SWY-B1", "ACSR-DRAKE", 1, "OHL", "D", None, 230000, 3, 22000, 1, 1.0, "Load in kVA")
add("10-HV-004", "10", "HV Overhead", "Strung main bus bay 1 - bay 2", "SWY-B1", "SWY-B2", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0, "Rated for total plant export")
add("10-HV-005", "10", "HV Overhead", "Strung main bus bay 2 - bay 3", "SWY-B2", "SWY-B3", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0)
add("10-HV-006", "10", "HV Overhead", "Strung main bus bay 3 - bay 4", "SWY-B3", "SWY-B4", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0)
add("10-HV-007", "10", "HV Overhead", "Outgoing 230 kV line: bay 4 to terminal tower T1", "SWY-B4", "TWR-01", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0)
add("10-HV-008", "10", "HV Overhead", "Outgoing 230 kV line span T1 - T2", "TWR-01", "TWR-02", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0)
add("10-HV-009", "10", "HV Overhead", "Outgoing 230 kV line span T2 - T3", "TWR-02", "TWR-03", "ACSR-DRAKE-2B", 1, "OHL", "D", None, 230000, 3, 487000, 1, 1.0)
add("10-HV-010", "10", "HV Overhead", "Switchyard shield wires (2 off) bay 1 - bay 4", "SWY-B1", "SWY-B4", "SW-7/16-EHS", 2, "OHL", "D", note="Lightning shielding over gantries")
add("10-HV-011", "10", "HV Overhead", "Line OPGW: bay 4 to T3 (teleprotection / SCADA)", "SWY-B4", "TWR-03", "OPGW-24", 1, "OHL", "D", note="Chord length bay 4 -> T3; refine per tower spotting")
# IPB
add("20-IPB-001", "20", "Busduct", "GT generator main IPB to GSU-GT LV", "GEN-GT", "GSU-GT-LV", "IPB-10K", 1, "IPB-GT", "M", None, 19000, 3, 290000, 1, 1.0, "Includes GCB if fitted")
add("20-IPB-002", "20", "Busduct", "GT IPB tap to UAT-1", "GEN-GT", "UAT-1", "IPB-3K", 1, "IPB-GT", "M", None, 19000, 3, 45000, 1, 1.0)
add("20-IPB-003", "20", "Busduct", "ST generator main IPB to GSU-ST LV", "GEN-ST", "GSU-ST-LV", "IPB-7K", 1, "IPB-ST", "M", None, 18000, 3, 175000, 1, 1.0)
add("20-IPB-004", "20", "Busduct", "ST IPB tap to UAT-2", "GEN-ST", "UAT-2", "IPB-3K", 1, "IPB-ST", "M", None, 18000, 3, 30000, 1, 1.0)
add("20-MV-001", "20", "MV Power", "GT generator neutral to NGR", "GEN-GT", "NGR-GT", "MV-1C-2-NGR", 1, "LOCAL", note="Neutral - fault current limited by NGR")
add("20-MV-002", "20", "MV Power", "ST generator neutral to NGR", "GEN-ST", "NGR-ST", "MV-1C-2-NGR", 1, "LOCAL", note="Neutral - fault current limited by NGR")
# MV main
add("70-MV-001", "70", "MV Power", "UAT-1 to 13.8 kV main switchgear incomer", "UAT-1", "MVS-1", "MV-1C-1000-TPX", 4, "DB-03", "M", None, 13800, 3, 45000, 1, 1.0, "Transformer secondary - 4 triplexed sets")
add("70-MV-002", "70", "MV Power", "UAT-2 to CCS 13.8 kV switchgear incomer", "UAT-2", "MVS-CCS", "MV-1C-750-TPX", 3, "TR-02", "M", None, 13800, 3, 30000, 1, 1.0, "Transformer secondary - 3 triplexed sets")
add("70-MV-003", "70", "MV Power", "MVS-1 / MVS-CCS bus tie", "MVS-1", "MVS-CCS", "MV-1C-500-TPX", 1, "TR-02", "M", None, 13800, 3, 10000, 1, 1.0)
add("70-MV-004", "70", "MV Power", "MVS-1 to GT LCI isolation transformer", "MVS-1", "LCI-TX", "MV-3C-500", 1, "TR-01", "M", None, 13800, 3, 8000, 1)
add("70-MV-005", "20", "MV Power", "LCI output to GT generator (start-up)", "LCI-GT", "GEN-GT", "MV-1C-500-TPX", 2, "TR-01", "M", None, 6000, 3, 8000, 1, 1.0, "Variable frequency; LCI max output voltage assumed 6 kV")
add("70-MV-006", "20", "MV Power", "Boiler feed pump A", "MVS-1", "M-BFP-A", "MV-3C-4/0", 1, "TR-01", "M", None, 13800, 3, 3200, 0.86, note="Motor: 125% FLC (NEC 430.22)")
add("70-MV-007", "20", "MV Power", "Boiler feed pump B", "MVS-1", "M-BFP-B", "MV-3C-4/0", 1, "TR-01", "M", None, 13800, 3, 3200, 0.86)
add("70-MV-008", "20", "MV Power", "Condensate extraction pump A", "MVS-1", "M-CEP-A", "MV-3C-2", 1, "TR-02", "M", None, 13800, 3, 500, 0.82, note="#2 AWG minimum for 15 kV / fault withstand")
add("70-MV-009", "20", "MV Power", "Condensate extraction pump B", "MVS-1", "M-CEP-B", "MV-3C-2", 1, "TR-02", "M", None, 13800, 3, 500, 0.82)
add("70-MV-010", "70", "MV Power", "Main LV transformer LVT-1", "MVS-1", "LVT-1", "MV-3C-1/0", 1, "LOCAL", "M", None, 13800, 3, 2500, 1)
add("70-MV-011", "30", "MV Power", "ACC fan transformer LVT-ACC", "MVS-1", "LVT-ACC", "MV-3C-1/0", 1, "TR-02", "M", None, 13800, 3, 3000, 1)
add("70-MV-012", "60", "MV Power", "Gas station transformer LVT-GAS", "MVS-1", "LVT-GAS", "MV-3C-2", 1, "TR-03", "M", None, 13800, 3, 1600, 1)
add("70-MV-013", "60", "MV Power", "BOG compressor motor", "MVS-1", "C-BOG", "MV-3C-2", 1, "TR-03", "M", None, 13800, 3, 900, 0.82, note="Class I Div 2 - " + HZ)
add("70-MV-014", "50", "MV Power", "RICE black-start / island tie to MVS-1", "MVS-RICE", "MVS-1", "MV-1C-500-TPX", 2, "DB-02", "M", None, 13800, 3, 10000, 1, 1.0)
# CCS MV
add("40-MV-001", "40", "MV Power", "Flue gas booster fan", "MVS-CCS", "M-BF", "MV-1C-500-TPX", 1, "TR-05", "M", None, 13800, 3, 6500, 0.86, note="Across-the-line start - check voltage dip")
add("40-MV-002", "40", "MV Power", "CO2 compressor VFD line side", "MVS-CCS", "VFD-CO2", "MV-1C-750-TPX", 2, "TR-05", "M", None, 13800, 3, 14000, 0.90, note="Input transformer integral to VFD")
add("40-MV-010", "40", "MV Power", "CO2 compressor VFD output to motor", "VFD-CO2", "M-CO2C", "MV-1C-750-TPX", 2, "LOCAL", "M", None, 13800, 3, 14000, 0.90, note="VFD output: shielded, symmetrical triplexed sets; confirm insulation for dv/dt with VFD vendor")
add("40-MV-003", "40", "MV Power", "Lean amine pump A", "MVS-CCS", "M-LAP-A", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 800, 0.84)
add("40-MV-004", "40", "MV Power", "Lean amine pump B", "MVS-CCS", "M-LAP-B", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 800, 0.84)
add("40-MV-005", "40", "MV Power", "Rich amine pump A", "MVS-CCS", "M-RAP-A", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 700, 0.84)
add("40-MV-006", "40", "MV Power", "Rich amine pump B", "MVS-CCS", "M-RAP-B", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 700, 0.84)
add("40-MV-007", "40", "MV Power", "DCC circulation pump A", "MVS-CCS", "M-DCC-A", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 400, 0.82)
add("40-MV-008", "40", "MV Power", "DCC circulation pump B", "MVS-CCS", "M-DCC-B", "MV-3C-2", 1, "TR-05", "M", None, 13800, 3, 400, 0.82)
add("40-MV-009", "40", "MV Power", "CCS LV transformer LVT-CCS", "MVS-CCS", "LVT-CCS", "MV-3C-1/0", 1, "LOCAL", "M", None, 13800, 3, 2500, 1)
# RICE MV
for i in range(8):
    add(f"50-MV-{i+1:03d}", "50", "MV Power", f"Genset {i+1} to collector switchgear", f"GEN-R{i+1:02d}", "MVS-RICE", "MV-3C-2", 1, "TR-04", "M", None, 13800, 3, 2500, 1, 1.15, "Generator: 115% (NEC 445.13); load in kVA")
add("50-MV-009", "50", "MV Power", "Collector switchgear to RICE step-up transformer LV", "MVS-RICE", "RICE-TX-LV", "MV-1C-750-TPX", 2, "LOCAL", "M", None, 13800, 3, 22000, 1, 1.0, "2 triplexed sets")
add("50-MV-010", "50", "MV Power", "RICE auxiliary transformer LVT-RICE", "MVS-RICE", "LVT-RICE", "MV-3C-2", 1, "LOCAL", "M", None, 13800, 3, 1000, 1)
# LV busway (transformer secondaries)
add("70-BD-001", "70", "Busduct", "LVT-1 to PMCC-1 main", "LVT-1", "PMCC-1", "LVBD-4000", 1, "BD", "M", None, 480, 3, 2500, 1, 1.0)
add("30-BD-001", "30", "Busduct", "LVT-ACC to ACC VFD switchboard", "LVT-ACC", "MCC-ACC", "LVBD-4000", 1, "BD", "M", None, 480, 3, 3000, 1, 1.0)
add("60-BD-001", "60", "Busduct", "LVT-GAS to gas station MCC", "LVT-GAS", "MCC-GAS", "LVBD-2500", 1, "BD", "M", None, 480, 3, 1600, 1, 1.0)
add("40-BD-001", "40", "Busduct", "LVT-CCS to PMCC-CCS", "LVT-CCS", "PMCC-CCS", "LVBD-4000", 1, "BD", "M", None, 480, 3, 2500, 1, 1.0)
add("50-BD-001", "50", "Busduct", "LVT-RICE to RICE MCC", "LVT-RICE", "MCC-RICE", "LVBD-2500", 1, "BD", "M", None, 480, 3, 1000, 1, 1.0)
# LV distribution - 480 V
add("70-LV-001", "20", "LV Power", "PMCC-1 to GT auxiliary MCC", "PMCC-1", "MCC-GT", "LV-3C-500", 2, "TR-01", "M", None, 480, 3, 350, 1, note="Load in kVA; 125% continuous (NEC 215.2)")
add("70-LV-002", "20", "LV Power", "PMCC-1 to HRSG auxiliary MCC", "PMCC-1", "MCC-HRSG", "LV-3C-350", 2, "TR-01", "M", None, 480, 3, 250, 1)
add("70-LV-003", "20", "LV Power", "PMCC-1 to ST auxiliary MCC", "PMCC-1", "MCC-ST", "LV-3C-500", 2, "TR-02", "M", None, 480, 3, 300, 1)
add("70-LV-004", "70", "LV Power", "PMCC-1 to UPS-1 rectifier", "PMCC-1", "UPS-1", "LV-3C-1/0", 1, "LOCAL", "M", None, 480, 3, 80, 1)
add("70-LV-005", "70", "LV Power", "PMCC-1 to 125 V DC chargers", "PMCC-1", "DCB-1", "LV-3C-2", 1, "LOCAL", "M", None, 480, 3, 60, 1)
add("70-LV-006", "10", "LV Power", "PMCC-1 to switchyard relay bldg panelboard", "PMCC-1", "SWY-RB", "LV-3C-4/0", 1, "DB-01", "M", None, 480, 3, 100, 1, note="Relay bldg has its own 125 V DC battery")
add("70-LV-007", "20", "LV Power", "PMCC-1 to CEMS shelter", "PMCC-1", "CEMS-SH", "LV-3C-6", 1, "TR-02", "M", None, 480, 3, 20, 1)
add("20-LV-001", "20", "LV Power", "GT AC lube oil pump", "MCC-GT", "M-GT-LOP", "LV-3C-4/0", 1, "LOCAL", "M", None, 480, 3, 75, 0.80, note="Motor: 125% FLC (NEC 430.22)")
add("20-LV-002", "20", "LV Power", "GT enclosure vent fan A", "MCC-GT", "M-GT-VNT-A", "LV-3C-2", 1, "LOCAL", "M", None, 480, 3, 45, 0.80)
add("20-LV-003", "20", "LV Power", "GT enclosure vent fan B", "MCC-GT", "M-GT-VNT-B", "LV-3C-2", 1, "LOCAL", "M", None, 480, 3, 45, 0.80)
add("20-LV-004", "20", "LV Power", "HRSG recirculation pump", "MCC-HRSG", "M-HRSG-RCP", "LV-3C-1/0", 1, "LOCAL", "M", None, 480, 3, 55, 0.80)
add("20-LV-005", "20", "LV Power", "ST turning gear", "MCC-ST", "M-ST-TG", "LV-3C-2", 1, "LOCAL", "M", None, 480, 3, 37, 0.78)
add("20-LV-006", "20", "LV Power", "ST AC lube oil pump", "MCC-ST", "M-ST-LOP", "LV-3C-1/0", 1, "LOCAL", "M", None, 480, 3, 55, 0.80)
for i in range(15):
    add(f"30-LV-{i+1:03d}", "30", "LV Power", f"ACC fan {i+1:02d} VFD output to local disconnect", "MCC-ACC", f"DS-ACC-{i+1:02d}", "LV-VFD-500", 1, "TR-06", "M", None, 480, 3, 150, 0.85, note="Armor-X type VFD cable, symmetrical grounds")
for i in range(15):
    add(f"30-LV-{i+16:03d}", "30", "LV Power", f"ACC fan {i+1:02d} disconnect to motor (flexible final drop)", f"DS-ACC-{i+1:02d}", f"M-ACC-{i+1:02d}", "LV-MFX-2/0", 2, "LOCAL", "M", 6, 480, 3, 150, 0.85, note="Machine Flex type TC-ER VFD cable for vibration; 360 deg shield termination glands")
add("40-LV-001", "40", "LV Power", "Reboiler condensate pump A", "PMCC-CCS", "M-RBC-A", "LV-3C-350", 1, "TR-05", "M", None, 480, 3, 110, 0.82)
add("40-LV-002", "40", "LV Power", "CO2 dehydration package", "PMCC-CCS", "PKG-DEH", "LV-3C-350", 2, "TR-05", "M", None, 480, 3, 250, 1, note="Load in kVA")
add("40-LV-003", "40", "LV Power", "CO2 fiscal meter skid", "PMCC-CCS", "FC-CO2", "LV-3C-10", 1, "TR-05", "M", None, 480, 3, 15, 1)
for i in range(8):
    add(f"50-LV-{i+1:03d}", "50", "LV Power", f"Genset {i+1} auxiliaries", "MCC-RICE", f"AUX-R{i+1:02d}", "LV-3C-1/0", 1, "TR-04", "M", None, 480, 3, 75, 1, note="Load in kVA")
add("60-LV-001", "60", "LV Power", "Fuel gas electric heater H-101", "MCC-GAS", "H-101", "LV-3C-500", 2, "TR-07", "M", None, 480, 3, 400, 0.98, note="Class I Div 2 - " + HZ)
add("60-LV-002", "60", "LV Power", "LNG in-tank pump 1", "MCC-GAS", "M-LNG-P1", "LV-3C-500", 2, "TR-07", "M", None, 480, 3, 250, 0.84, note="Class I Div 1 at tank roof - " + HZ)
add("60-LV-003", "60", "LV Power", "LNG in-tank pump 2", "MCC-GAS", "M-LNG-P2", "LV-3C-500", 2, "TR-07", "M", None, 480, 3, 250, 0.84, note="Class I Div 1 at tank roof - " + HZ)
add("60-LV-004", "60", "LV Power", "LNG area heat tracing / lighting panel", "MCC-GAS", "HTP-LNG", "LV-3C-2", 1, "TR-07", "M", None, 480, 3, 60, 1)
add("60-LV-005", "60", "LV Power", "Inlet ESD valve hydraulic power unit", "MCC-GAS", "XV-001", "LV-3C-10", 1, "TR-07", "M", None, 480, 3, 3, 0.80, note="Class I Div 2 - " + HZ)
add("60-LV-006", "60", "LV Power", "Gas chromatograph supply (120 V)", "MCC-GAS", "AT-GC", "LV-2C-10", 1, "LOCAL", "M", None, 120, 1, 2, 1)
# DC / UPS
add("70-DC-001", "20", "DC Power", "GT DC emergency lube oil pump", "DCB-1", "M-GT-ELOP", "LV-1C-500", 1, "TR-01", "M", None, 125, "DC", 15, 1, note="Circuit integrity (CI) cable to be considered")
add("70-DC-002", "20", "DC Power", "ST DC emergency lube oil pump", "DCB-1", "M-ST-ELOP", "LV-1C-500", 1, "TR-02", "M", None, 125, "DC", 22, 1, note="Circuit integrity (CI) cable to be considered")
add("70-DC-003", "70", "DC Power", "125 V DC trip / closing supply to MVS-1", "DCB-1", "MVS-1", "LV-2C-10", 1, "LOCAL", "M", None, 125, "DC", 2, 1)
add("70-DC-004", "20", "DC Power", "125 V DC to GT control / PEECC", "DCB-1", "GTCP", "LV-2C-2", 1, "TR-01", "M", None, 125, "DC", 3, 1)
add("70-UP-001", "70", "DC Power", "UPS to DCS servers / CCR (208 V 1-ph)", "UPS-1", "DCS-CCR", "LV-2C-2", 1, "LOCAL", "M", None, 208, 1, 10, 1)
add("70-UP-002", "20", "DC Power", "UPS to GT control panel (208 V 1-ph)", "UPS-1", "GTCP", "LV-2C-2", 1, "TR-01", "M", None, 208, 1, 5, 1)
add("70-UP-003", "20", "DC Power", "UPS to ST control panel (208 V 1-ph)", "UPS-1", "TCP-ST", "LV-2C-2", 1, "TR-02", "M", None, 208, 1, 5, 1)
add("70-UP-004", "20", "DC Power", "UPS to power block RIO (208 V 1-ph)", "UPS-1", "RIO-PB", "LV-2C-6", 1, "TR-01", "M", None, 208, 1, 3, 1)
add("70-UP-005", "40", "DC Power", "UPS to CCS RIO (208 V 1-ph)", "UPS-1", "RIO-CCS", "LV-2C-2", 1, "TR-02", "M", None, 208, 1, 5, 1)
add("70-UP-006", "60", "DC Power", "UPS to gas station RIO / flow computer (208 V 1-ph)", "UPS-1", "RIO-GAS", "LV-2C-2", 1, "TR-03", "M", None, 208, 1, 3, 1)
# Control / protection (MC-HL control cable)
for b in (1, 2, 3, 4):
    add(f"10-CT-{2*b-1:03d}", "10", "Control", f"Bay {b} breaker / disconnect switch control & status", f"SWY-B{b}", "SWY-RB", "CTL-25C-14", 2, "TR-08")
    add(f"10-CT-{2*b:03d}", "10", "Control", f"Bay {b} CT / CCVT secondaries", f"SWY-B{b}", "SWY-RB", "CTL-12C-10", 2, "TR-08", note="Check CT burden")
add("20-CT-001", "20", "Control", "GSU-GT protection: CTs, sudden pressure, WTI/OTI, LTC", "GSU-GT-LV", "GPP", "CTL-12C-10", 2, "DB-03")
add("20-CT-002", "20", "Control", "GSU-GT alarms / cooling control", "GSU-GT-LV", "GPP", "CTL-25C-14", 1, "DB-03")
add("20-CT-003", "20", "Control", "GSU-ST protection: CTs, sudden pressure, WTI/OTI, LTC", "GSU-ST-LV", "GPP", "CTL-12C-10", 2, "DB-03")
add("20-CT-004", "20", "Control", "GSU-ST alarms / cooling control", "GSU-ST-LV", "GPP", "CTL-25C-14", 1, "DB-03")
add("20-CT-005", "20", "Control", "UAT-1 protection & alarms", "UAT-1", "GPP", "CTL-12C-10", 1, "DB-03")
add("20-CT-006", "20", "Control", "UAT-2 protection & alarms", "UAT-2", "GPP", "CTL-12C-10", 1, "DB-03")
add("20-CT-007", "20", "Control", "GT generator CT / VT secondaries", "GEN-GT", "GPP", "CTL-12C-10", 2, "TR-01")
add("20-CT-008", "20", "Control", "ST generator CT / VT secondaries", "GEN-ST", "GPP", "CTL-12C-10", 2, "TR-02")
add("50-CT-001", "50", "Control", "RICE transformer protection & alarms", "RICE-TX-LV", "RPC", "CTL-12C-10", 1, "LOCAL")
add("70-CT-001", "70", "Control", "MVS-1 hardwired interface to DCS", "MVS-1", "DCS-CCR", "CTL-25C-14", 4, "LOCAL")
add("20-CT-009", "20", "Control", "GT control to GT aux MCC", "GTCP", "MCC-GT", "CTL-25C-14", 3, "LOCAL")
add("20-CT-010", "20", "Control", "GT control to LCI", "GTCP", "LCI-GT", "CTL-25C-14", 1, "LOCAL")
add("60-CT-001", "60", "Control", "Inlet ESD valve solenoids and limit switches", "XV-001", "RIO-GAS", "CTL-7C-12", 1, "TR-07", note="Class I Div 2 - " + HZ)
add("40-CT-001", "40", "Control", "CO2 compressor UCP to VFD / CCS switchgear", "UCP-CO2", "MVS-CCS", "CTL-25C-14", 2, "TR-05")
# Fibre
add("10-FO-001", "10", "Fibre Optic", "Switchyard relay bldg to DCS / SCADA", "SWY-RB", "DCS-CCR", "FO-48SM", 2, "DB-01", note="Diverse routes recommended")
add("10-FO-002", "10", "Fibre Optic", "Generator protection intertrip to switchyard", "GPP", "SWY-RB", "FO-24SM", 2, "DB-01")
add("20-FO-001", "20", "Fibre Optic", "GT control to DCS", "GTCP", "DCS-CCR", "FO-24SM", 2, "TR-01", note="Redundant pair")
add("20-FO-002", "20", "Fibre Optic", "ST control to DCS", "TCP-ST", "DCS-CCR", "FO-24SM", 2, "TR-02", note="Redundant pair")
add("20-FO-003", "20", "Fibre Optic", "Power block RIO to DCS", "RIO-PB", "DCS-CCR", "FO-24SM", 2, "TR-01", note="Redundant pair")
add("20-FO-004", "20", "Fibre Optic", "CEMS shelter to DCS", "CEMS-SH", "DCS-CCR", "FO-24SM", 1, "TR-02")
add("30-FO-001", "30", "Fibre Optic", "ACC VFD switchroom to DCS", "MCC-ACC", "DCS-CCR", "FO-24SM", 1, "TR-02")
add("40-FO-001", "40", "Fibre Optic", "CCS RIO to DCS", "RIO-CCS", "DCS-CCR", "FO-48SM", 2, "TR-02", note="Redundant pair")
add("40-FO-002", "40", "Fibre Optic", "CO2 compressor UCP to CCS RIO", "UCP-CO2", "RIO-CCS", "FO-24SM", 1, "TR-05")
add("50-FO-001", "50", "Fibre Optic", "RICE plant controller to DCS", "RPC", "DCS-CCR", "FO-24SM", 2, "DB-02", note="Redundant pair")
add("60-FO-001", "60", "Fibre Optic", "Gas station RIO to DCS", "RIO-GAS", "DCS-CCR", "FO-24SM", 2, "TR-03", note="Redundant pair")
for i in range(8):
    add(f"50-CT-{i+2:03d}", "50", "Control", f"Genset {i+1} control / sync / protection to RPC", f"GEN-R{i+1:02d}", "RPC", "CTL-25C-14", 1, "TR-04", note="Plus genset LAN on fiber by vendor")
# Instrumentation (armored PLTC / ITC-HL)
add("60-IN-001", "60", "Instrument", "Ultrasonic meter A to flow computer", "FT-101A", "FC-GAS", "INS-2TSP-16", 1, "TR-07", note="Custody transfer; intrinsically safe")
add("60-IN-002", "60", "Instrument", "Ultrasonic meter B to flow computer", "FT-101B", "FC-GAS", "INS-2TSP-16", 1, "TR-07", note="Custody transfer; intrinsically safe")
add("60-IN-003", "60", "Instrument", "Ultrasonic meter C to flow computer", "FT-101C", "FC-GAS", "INS-2TSP-16", 1, "TR-07", note="Custody transfer; intrinsically safe")
add("60-IN-004", "60", "Instrument", "Gas chromatograph to flow computer (Modbus)", "AT-GC", "FC-GAS", "INS-RS485", 1, "LOCAL")
add("60-IN-005", "60", "Instrument", "Flow computer to gas station RIO (Modbus)", "FC-GAS", "RIO-GAS", "INS-RS485", 1, "LOCAL")
add("60-IN-006", "60", "Instrument", "Gas station JB (PT/TT/DPT) to RIO", "JB-GAS", "RIO-GAS", "INS-24TSP-18", 1, "TR-07", note="Intrinsically safe")
add("60-IN-007", "60", "Instrument", "Pressure regulator position / PT to JB", "PCV-101", "JB-GAS", "INS-1TSP-16", 2, "TR-07", note="Intrinsically safe")
add("60-IN-008", "60", "Instrument", "LNG tank gauging to RIO", "LT-LNG", "RIO-GAS", "INS-12TSP-18", 1, "TR-07")
add("60-IN-009", "60", "Instrument", "LNG area JB to RIO", "JB-LNG", "RIO-GAS", "INS-24TSP-18", 1, "TR-07", note="Intrinsically safe")
add("20-IN-001", "20", "Instrument", "GT exhaust thermocouples to GT control", "JB-GT-TC", "GTCP", "INS-TC-12P-KX", 2, "TR-01")
add("20-IN-002", "20", "Instrument", "HRSG drum JB to power block RIO", "JB-HRSG-01", "RIO-PB", "INS-24TSP-18", 2, "TR-01")
add("20-IN-003", "20", "Instrument", "CEMS probe to analyser shelter", "AE-STK", "CEMS-SH", "INS-2TSP-16", 1, "LOCAL", note="Heated sample line by vendor")
add("30-IN-001", "30", "Instrument", "ACC JB to power block RIO", "JB-ACC", "RIO-PB", "INS-24TSP-18", 1, "TR-02")
add("40-IN-001", "40", "Instrument", "Absorber JB to CCS RIO", "JB-ABS-01", "RIO-CCS", "INS-24TSP-18", 2, "TR-05")
add("40-IN-002", "40", "Instrument", "Stripper JB to CCS RIO", "JB-STR-01", "RIO-CCS", "INS-24TSP-18", 1, "TR-05")
add("40-IN-003", "40", "Instrument", "CO2 fiscal meter to CCS RIO (Modbus)", "FC-CO2", "RIO-CCS", "INS-RS485", 1, "TR-05")
add("70-FG-001", "60", "Instrument", "F&G loop: gas station / LNG detectors", "FGP-1", "JB-GAS", "INS-12TSP-18", 1, "TR-03", note="Circuit integrity (CI) rated")
add("70-FG-002", "20", "Instrument", "F&G loop: GT enclosure detectors", "FGP-1", "JB-FG-GT", "INS-12TSP-18", 1, "TR-01", note="Circuit integrity (CI) rated")
add("70-FG-003", "40", "Instrument", "F&G loop: CCS area detectors", "FGP-1", "JB-FG-CCS", "INS-12TSP-18", 1, "TR-02", note="Circuit integrity (CI) rated")
# Grounding
add("20-EG-001", "20", "Earthing", "Power block main ground grid (mesh)", "EG-PB", "EG-PB", "EG-CU-4/0", 1, "EG", "M", 1800, note="Length estimate - confirm by IEEE 80 study")
add("10-EG-001", "10", "Earthing", "Switchyard ground grid (mesh)", "EG-SWY", "EG-SWY", "EG-CU-4/0", 1, "EG", "M", 2400, note="Length estimate - confirm by IEEE 80 study")
add("40-EG-001", "40", "Earthing", "CCS area ground grid (mesh)", "EG-CCS", "EG-CCS", "EG-CU-4/0", 1, "EG", "M", 1200, note="Length estimate")
add("60-EG-001", "60", "Earthing", "Gas / LNG area ground grid (mesh)", "EG-GAS", "EG-GAS", "EG-CU-4/0", 1, "EG", "M", 900, note="Length estimate")
add("50-EG-001", "50", "Earthing", "RICE area ground grid (mesh)", "EG-RICE", "EG-RICE", "EG-CU-4/0", 1, "EG", "M", 600, note="Length estimate")
add("10-EG-002", "10", "Earthing", "Interconnection power block grid - switchyard grid", "EG-PB", "EG-SWY", "EG-CU-4/0", 2, "EG", "M", note="Two diverse connections")
add("50-EG-002", "50", "Earthing", "Interconnection power block grid - RICE grid", "EG-PB", "EG-RICE", "EG-CU-4/0", 2, "EG", "M")
add("40-EG-002", "40", "Earthing", "Interconnection power block grid - CCS grid", "EG-PB", "EG-CCS", "EG-CU-4/0", 2, "EG", "M")
add("60-EG-002", "60", "Earthing", "Interconnection power block grid - gas/LNG grid", "EG-PB", "EG-GAS", "EG-CU-4/0", 2, "EG", "M", note="Insulating joints on gas pipe - check cathodic protection")
add("20-EG-002", "20", "Earthing", "GSU-GT tank and neutral bonds", "GSU-GT-LV", "EG-PB", "EB-CU-2/0", 4, "EG", "M", 15)
add("20-EG-003", "20", "Earthing", "GSU-ST tank and neutral bonds", "GSU-ST-LV", "EG-PB", "EB-CU-2/0", 4, "EG", "M", 15)
add("20-EG-004", "20", "Earthing", "Stack lightning down conductors", "STK", "EG-PB", "EG-CU-4/0", 2, "EG", "M", 70)
add("40-EG-003", "40", "Earthing", "Absorber column bonds", "C-ABS", "EG-CCS", "EB-CU-2/0", 2, "EG", "M", 10)
add("60-EG-003", "60", "Earthing", "LNG tank bonds", "TK-LNG", "EG-GAS", "EB-CU-2/0", 4, "EG", "M", 20)

nos = [r[0] for r in C]
assert len(nos) == len(set(nos)), [n for n in nos if nos.count(n) > 1]
for r in C:
    assert r[4] in tags and r[5] in tags, r
    assert r[6] in [t[0] for t in T], r
    assert r[8] in [x[0] for x in R], r

# ---------------------------------------------------------------- Cable schedule sheet
cs = wb.create_sheet("Cable Schedule", 4)
heads = [
    ("A", "Cable No.", 11), ("B", "Area", 5), ("C", "System", 11), ("D", "Service / Function", 38),
    ("E", "From Tag", 11), ("F", "From Equipment", 34), ("G", "To Tag", 11), ("H", "To Equipment", 34),
    ("I", "Cable Type", 15), ("J", "Cable Description", 44), ("K", "Parallel Runs", 7), ("L", "Raceway", 8),
    ("M", "Route Method", 7), ("N", "Length Override (m)", 9), ("O", "Route Length / Run (m)", 9),
    ("P", "Route Length / Run (ft)", 9), ("Q", "Total Conductor Length (m)", 10), ("R", "Total Conductor Length (ft)", 10),
    ("S", "System Voltage (V)", 9), ("T", "Phases", 6), ("U", "Load (kW / kVA)", 9), ("V", "PF x Eff.", 7),
    ("W", "Running Current (A)", 9), ("X", "Sizing Factor", 7), ("Y", "Design Current (A)", 9),
    ("Z", "Allowable Ampacity / Run (A)", 10), ("AA", "Total Capacity (A)", 9), ("AB", "Loading (%)", 8),
    ("AC", "Volt Drop (%)", 8), ("AD", "VD Limit (%)", 7), ("AE", "Check", 8), ("AF", "Cable Area (mm2)", 9),
    ("AG", "Notes", 44),
    ("AI", "X from", 7), ("AJ", "Y from", 7), ("AK", "Z from", 7), ("AL", "X to", 7), ("AM", "Y to", 7),
    ("AN", "Z to", 7), ("AO", "Raceway Elev.", 7), ("AP", "Correction", 7), ("AQ", "Cond. / Run", 7),
    ("AR", "OD (mm)", 7), ("AS", "Base Ampacity (A)", 8), ("AT", "mV/A/m", 7),
]
HELPERS = ("AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT")
cs["A1"] = "CABLE SCHEDULE - CCPP-E-CS-0001 Rev C (PRELIMINARY) - US NEC practice, Type MC-HL armored cable"
cs["A1"].font = Font(name=F, bold=True, size=12)
cs["AI1"] = "Calculation helpers (lookups - do not edit)"
cs["AI1"].font = BOLD
for col, h, w in heads:
    c = cs[f"{col}2"]
    c.value = h
    c.font = HDR
    c.fill = HELPFILL if col in HELPERS else HFILL
    c.alignment = CENTER
    c.border = BORDER
    cs.column_dimensions[col].width = w
cs.column_dimensions["AH"].width = 2
cs.row_dimensions[2].height = 42

def look(retcol, keycell, keyrange):
    return f"INDEX({retcol},MATCH({keycell},{keyrange},0))"

r0 = 3
for k, row in enumerate(C):
    r = r0 + k
    no, area, system, service, frm, to, typ, runs, rway, method, override, V, ph, load, pf, sf, note = row
    inputs = {"A": no, "B": area, "C": system, "D": service, "E": frm, "G": to, "I": typ, "K": runs,
              "L": rway, "M": method, "N": override, "S": V, "T": ph, "U": load, "V": pf, "X": sf, "AG": note}
    for col, val in inputs.items():
        c = cs[f"{col}{r}"]
        c.value = val
        c.font = BLUE if col != "AG" else BLACK
    f = {
        "F": f"={look(EQCOL('B'), f'E{r}', EQ_TAG)}",
        "H": f"={look(EQCOL('B'), f'G{r}', EQ_TAG)}",
        "J": f"={look(CTCOL('B'), f'I{r}', CT_CODE)}",
        "AI": f"={look(EQCOL('D'), f'E{r}', EQ_TAG)}",
        "AJ": f"={look(EQCOL('E'), f'E{r}', EQ_TAG)}",
        "AK": f"={look(EQCOL('F'), f'E{r}', EQ_TAG)}",
        "AL": f"={look(EQCOL('D'), f'G{r}', EQ_TAG)}",
        "AM": f"={look(EQCOL('E'), f'G{r}', EQ_TAG)}",
        "AN": f"={look(EQCOL('F'), f'G{r}', EQ_TAG)}",
        "AO": f'=IF({look(RWCOL("D"), f"L{r}", RW_ID)}="",0,{look(RWCOL("D"), f"L{r}", RW_ID)})',
        "AP": f'=IF({look(RWCOL("I"), f"L{r}", RW_ID)}="","",{look(RWCOL("I"), f"L{r}", RW_ID)})',
        "AQ": f"={look(CTCOL('D'), f'I{r}', CT_CODE)}",
        "AR": f'=IF({look(CTCOL("E"), f"I{r}", CT_CODE)}="","",{look(CTCOL("E"), f"I{r}", CT_CODE)})',
        "AS": f'=IF({look(CTCOL("F"), f"I{r}", CT_CODE)}="","",{look(CTCOL("F"), f"I{r}", CT_CODE)})',
        "AT": f'=IF({look(CTCOL("G"), f"I{r}", CT_CODE)}="","",{look(CTCOL("G"), f"I{r}", CT_CODE)})',
        "O": (f'=IF(N{r}<>"",N{r},IF(M{r}="D",'
              f'ROUNDUP(SQRT((AL{r}-AI{r})^2+(AM{r}-AJ{r})^2+(AN{r}-AK{r})^2)*(1+{SAG}),0),'
              f'ROUNDUP((ABS(AL{r}-AI{r})+ABS(AM{r}-AJ{r})+ABS(AO{r}-AK{r})+ABS(AO{r}-AN{r}))*(1+{SLACK})+2*{TERM},0)))'),
        "P": f"=ROUND(O{r}*{FT},0)",
        "Q": f"=O{r}*K{r}*AQ{r}",
        "R": f"=ROUND(Q{r}*{FT},0)",
        "W": f'=IF(OR(U{r}="",S{r}=""),"",IF(T{r}=3,U{r}*1000/(SQRT(3)*S{r}*V{r}),U{r}*1000/(S{r}*V{r})))',
        "Y": f'=IF(W{r}="","",W{r}*IF(X{r}="",1,X{r}))',
        "Z": f'=IF(OR(AS{r}="",AP{r}=""),"",AS{r}*AP{r})',
        "AA": f'=IF(Z{r}="","",Z{r}*K{r})',
        "AB": f'=IF(OR(Y{r}="",AA{r}=""),"",Y{r}/AA{r})',
        "AC": f'=IF(OR(W{r}="",AT{r}=""),"",AT{r}*(W{r}/K{r})*O{r}/1000/S{r})',
        "AD": f'=IF(W{r}="","",IFERROR(IF(INDEX({VDL_RANGE},MATCH(C{r},{SYS_RANGE},0))="","",INDEX({VDL_RANGE},MATCH(C{r},{SYS_RANGE},0))),""))',
        "AE": f'=IF(W{r}="","n/a",IF(AA{r}="","CHECK",IF(AND(AB{r}<=1,OR(AC{r}="",AD{r}="",AC{r}<=AD{r})),"OK","CHECK")))',
        "AF": f'=IF(AR{r}="","",K{r}*AQ{r}*PI()/4*AR{r}^2)',
    }
    for col, val in f.items():
        c = cs[f"{col}{r}"]
        c.value = val
        c.font = GREEN if col in ("F", "H", "J") or col in HELPERS else BLACK
    for col, _, _ in heads:
        cs[f"{col}{r}"].border = BORDER
        cs[f"{col}{r}"].alignment = Alignment(vertical="top")
    for col in ("O", "P", "Q", "R", "S", "U", "W", "Y", "Z", "AA", "AF"):
        cs[f"{col}{r}"].number_format = "#,##0"
    cs[f"V{r}"].number_format = "0.00"
    cs[f"X{r}"].number_format = "0.00"
    for col in ("AB", "AC", "AD"):
        cs[f"{col}{r}"].number_format = "0.0%"
    for col in ("AI", "AJ", "AK", "AL", "AM", "AN", "AO"):
        cs[f"{col}{r}"].number_format = "0.0"
    cs[f"AP{r}"].number_format = "0.00"
    cs[f"AT{r}"].number_format = "0.000"
CS_LAST = r0 + len(C) - 1

cs.freeze_panes = "E3"
cs.auto_filter.ref = f"A2:AG{CS_LAST}"
cs.conditional_formatting.add(f"AE3:AE{CS_LAST}", CellIsRule(operator="equal", formula=['"CHECK"'], fill=PatternFill("solid", fgColor="F4B084")))
cs.conditional_formatting.add(f"AE3:AE{CS_LAST}", CellIsRule(operator="equal", formula=['"OK"'], fill=PatternFill("solid", fgColor="C6EFCE")))
cs.conditional_formatting.add(f"AB3:AB{CS_LAST}", FormulaRule(formula=['AND(ISNUMBER(AB3),AB3>1)'], fill=PatternFill("solid", fgColor="F4B084")))

dv_sys = DataValidation(type="list", formula1=SYS_RANGE, allow_blank=False)
dv_type = DataValidation(type="list", formula1=CT_CODE, allow_blank=False)
dv_rw = DataValidation(type="list", formula1=RW_ID, allow_blank=False)
dv_tag = DataValidation(type="list", formula1=EQ_TAG, allow_blank=False)
dv_m = DataValidation(type="list", formula1='"M,D"', allow_blank=False)
dv_ph = DataValidation(type="list", formula1='"3,1,DC"', allow_blank=True)
for dv, rng in ((dv_sys, f"C3:C{CS_LAST+200}"), (dv_type, f"I3:I{CS_LAST+200}"), (dv_rw, f"L3:L{CS_LAST+200}"),
                (dv_tag, f"E3:E{CS_LAST+200} G3:G{CS_LAST+200}"), (dv_m, f"M3:M{CS_LAST+200}"), (dv_ph, f"T3:T{CS_LAST+200}")):
    cs.add_data_validation(dv)
    for part in rng.split():
        dv.add(part)
cs["O2"].comment = Comment("M: (|dX|+|dY|+rises to raceway elevation) x (1+slack) + 2 x termination allowance.\nD: 3D span x (1+sag).\nOverride (col N) wins if filled.", "Schedule")
cs["W2"].comment = Comment("3-ph: P/(sqrt3 x V x PFxEff). 1-ph / DC: P/(V x PFxEff). For kVA loads PF=1.", "Schedule")
cs["X2"].comment = Comment("1.25 motors (NEC 430.22) and continuous loads (NEC 210.19/215.2); 1.15 generators (NEC 445.13); 1.00 transformer secondaries / busway / OHL.", "Schedule")
cs["AC2"].comment = Comment("mV/A/m x (running I / runs) x L / 1000 / V. mV/A/m from NEC Ch.9 Table 9 (AC, 0.85 PF) or Table 8 (DC loop).", "Schedule")

# ---------------------------------------------------------------- BOQ
bq = wb.create_sheet("BOQ Summary")
bq["A1"] = "BILL OF QUANTITIES - CABLES, CONDUCTORS AND BUSWAY"
bq["A1"].font = Font(name=F, bold=True, size=12)
bh = ["Cable Type", "Description", "Category", "No. of circuits", "Schedule length (m)", "Incl. wastage (m)", "Incl. wastage (ft)", "Reel length (m)", "No. of reels", "Mass (t)"]
for j, h in enumerate(bh, start=1):
    c = bq.cell(row=3, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.alignment = CENTER; c.border = BORDER
SC = "'Cable Schedule'"
for i in range(len(T)):
    r = 4 + i
    src = 2 + i
    vals = {
        1: f"='Cable Types'!A{src}",
        2: f"='Cable Types'!B{src}",
        3: f"='Cable Types'!C{src}",
        4: f"=COUNTIF({SC}!$I$3:$I${CS_LAST},A{r})",
        5: f"=SUMIFS({SC}!$Q$3:$Q${CS_LAST},{SC}!$I$3:$I${CS_LAST},A{r})",
        6: f"=ROUNDUP(E{r}*(1+{WASTE}),0)",
        7: f"=ROUND(F{r}*{FT},0)",
        8: f'=IF(\'Cable Types\'!I{src}="","",\'Cable Types\'!I{src})',
        9: f'=IF(OR(H{r}="",F{r}=0),"",ROUNDUP(F{r}/H{r},0))',
        10: f"=F{r}*'Cable Types'!H{src}/1000",
    }
    for j, v in vals.items():
        c = bq.cell(row=r, column=j, value=v)
        c.font = GREEN if j in (1, 2, 3, 8) else BLACK
        c.border = BORDER
    for j in (4, 5, 6, 7, 8, 9):
        bq.cell(row=r, column=j).number_format = "#,##0"
    bq.cell(row=r, column=10).number_format = "#,##0.0"
tr = 4 + len(T)
bq.cell(row=tr, column=1, value="TOTAL").font = BOLD
for j, col in ((4, "D"), (10, "J")):
    c = bq.cell(row=tr, column=j, value=f"=SUM({col}4:{col}{tr-1})")
    c.font = BOLD; c.border = BORDER
    c.number_format = "#,##0" if j == 4 else "#,##0.0"
bq.cell(row=tr + 1, column=1, value="IPB lengths are per phase metre (3 per run); LV busway per metre; OHL lengths are conductor metres; triplexed MV sets count each 1/C cable.").font = Font(name=F, italic=True, size=8)

sr = tr + 4
bq.cell(row=sr - 1, column=1, value="SUMMARY BY SYSTEM").font = BOLD
sh = ["System", "No. of circuits", "Conductor length (m)", "Conductor length (ft)", "Circuits OK", "Circuits CHECK", "Max loading", "Max volt drop"]
for j, h in enumerate(sh, start=1):
    c = bq.cell(row=sr, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.alignment = CENTER; c.border = BORDER
for i in range(len(systems)):
    r = sr + 1 + i
    vals = {
        1: f"='Design Basis'!A{SYS_FIRST + i}",
        2: f"=COUNTIF({SC}!$C$3:$C${CS_LAST},A{r})",
        3: f"=SUMIFS({SC}!$Q$3:$Q${CS_LAST},{SC}!$C$3:$C${CS_LAST},A{r})",
        4: f"=ROUND(C{r}*{FT},0)",
        5: f'=COUNTIFS({SC}!$C$3:$C${CS_LAST},A{r},{SC}!$AE$3:$AE${CS_LAST},"OK")',
        6: f'=COUNTIFS({SC}!$C$3:$C${CS_LAST},A{r},{SC}!$AE$3:$AE${CS_LAST},"CHECK")',
        7: f'=IF(COUNTIFS({SC}!$C$3:$C${CS_LAST},A{r},{SC}!$AB$3:$AB${CS_LAST},">=0")=0,"",_xlfn.MAXIFS({SC}!$AB$3:$AB${CS_LAST},{SC}!$C$3:$C${CS_LAST},A{r}))',
        8: f'=IF(COUNTIFS({SC}!$C$3:$C${CS_LAST},A{r},{SC}!$AC$3:$AC${CS_LAST},">=0")=0,"",_xlfn.MAXIFS({SC}!$AC$3:$AC${CS_LAST},{SC}!$C$3:$C${CS_LAST},A{r}))',
    }
    for j, v in vals.items():
        c = bq.cell(row=r, column=j, value=v)
        c.font = GREEN if j == 1 else BLACK
        c.border = BORDER
    bq.cell(row=r, column=3).number_format = "#,##0"
    bq.cell(row=r, column=4).number_format = "#,##0"
    bq.cell(row=r, column=7).number_format = "0%"
    bq.cell(row=r, column=8).number_format = "0.0%"
er = sr + 1 + len(systems)
bq.cell(row=er, column=1, value="TOTAL").font = BOLD
for j, col in ((2, "B"), (5, "E"), (6, "F")):
    c = bq.cell(row=er, column=j, value=f"=SUM({col}{sr+1}:{col}{er-1})")
    c.font = BOLD; c.border = BORDER
for col, w in zip("ABCDEFGHIJ", (16, 70, 13, 12, 14, 14, 14, 12, 10, 10)):
    bq.column_dimensions[col].width = w
bq.freeze_panes = "A4"

# ---------------------------------------------------------------- References
rf = wb.create_sheet("References")
rf["A1"] = "PUBLIC REFERENCE DOCUMENTS"
rf["A1"].font = Font(name=F, bold=True, size=12)
rf["A2"] = ("These public documents were identified as references for typical plant arrangements. They were NOT opened or "
            "transcribed for this schedule: equipment positions come from the 3D model and ratings are representative values. Cable product pages are cited as examples of the MC-HL / CCW armor construction; sizes, ODs and masses in 'Cable Types' are typical values - confirm against the selected manufacturer's data sheets. "
            "Replace with project data before use.")
rf["A2"].font = Font(name=F, italic=True, size=9)
rf["A2"].alignment = WRAP
rf.merge_cells("A2:C2")
rf.row_dimensions[2].height = 40
refs = [
    ("CCPP + LNG + gas metering", "Shannon Technology & Energy Park power plant - list of planning drawings (incl. gas metering / regulating enclosures)", "https://www.pleanala.ie/publicaccess/EIAR-NIS/319566/Shannon%20Technology%20and%20Energy%20Park%20(STEP)%20Power%20Plant/02_Planning%20Drawings/SLNG_PP_List%20of%20Planning_Drawings.pdf"),
    ("CCPP layout", "Shannon - Combined Cycle Power Plant general arrangement", "https://www.pleanala.ie/publicaccess/EIAR-NIS/311233/Drawings/Structures/198291-1GSU-G2001.pdf"),
    ("CCPP layout", "Tees CCPP - indicative generating station sheet 1", "https://infrastructure.planninginspectorate.gov.uk/wp-content/ipc/uploads/projects/EN010082/EN010082-000370-4.5%20-%20Tees%20CCPP%20-%20Indicative%20Generating%20Station%20Sheet%201%20-%20Rev%202.pdf"),
    ("CCPP layout", "ESC Brooke County CCGT air permit application (conceptual layout, App. A)", "https://dep.wv.gov/daq/Documents/December%202016%20Applications/033-00264_APPL_R14-0036.pdf"),
    ("CCS", "Bechtel / Panda Sherman NGCC carbon capture FEED final report (OSTI)", "https://www.osti.gov/servlets/purl/1836563"),
    ("CCS", "NETL - EPRI CalCapture (Elk Hills) NGCC CCS FEED", "https://netl.doe.gov/sites/default/files/netl-file/21CMOG_CCUS_Bhown.pdf"),
    ("CCS", "NETL - Calpine Deer Park CCS FEED", "https://netl.doe.gov/sites/default/files/netl-file/23CM_PSCC28_Herman.pdf"),
    ("Gas metering", "Adams County CO - regulator station site plan submittal", "https://adcogov.org/sites/default/files/2024-05/RCU2024-00010-submittal1.pdf"),
    ("RICE", "KYMEA Energy Center (4 x Wartsila 18V50SG) - KY PSC case 2024-00290", "https://psc.ky.gov/pscecf/2024-00290/tosterloh@sturgillturner.com/10042024124833/07_Attachment_E_-_Public_Meeting_Information.pdf"),
    ("RICE", "We Energies Paris RICE generation project", "https://www.we-energies.com/company/paris-generation-project"),
    ("Switchyard / SLD", "PJM facilities study - 1,100 MW combined cycle interconnection (one-lines)", "https://www.pjm.com/pjmfiles/pub/planning/project-queues/facilities/b03_fac.pdf"),
    ("Cable product", "Southwire SPEC 45352 - 600 V XLPE XHHW-2 Armor-X (MC-HL) power cable with ground", "https://cabletechsupport.southwire.com/tile/26/spec/45352/?country=US"),
    ("Cable product", "Southwire SPEC 45227 - 600 V XLPE XHHW-2 Armor-X (MC-HL) control cable with ground", "https://www.southwire.com/wire-cable/armored-power-cable/cu-600v-xlpe-xhhw-2-armor-x-pvc-control-cable-with-ground/p/55061899"),
    ("Cable product", "Southwire SPEC 45302 - 600/1000 V Armor-X VFD cable", "https://www.southwire.com/wire-cable/armored-power-cable/cu-600-1000v-xlpe-insulation-armor-x-sup-sup-thermoplastic-lszh-tp-jacket-xhhw-2-vfd-cable-ct-rated-sunlight-resistant-for-direct-burial-silicone-free/p/67267399"),
    ("Cable product", "Southwire SPEC 45443 - Machine Flex TC-ER 1000 V flexible VFD cable, 3 symmetrical grounds", "https://cabletechsupport.southwire.com/tile/1/spec/45443/?country=US"),
    ("Cable product", "Southwire SPEC 45442 - reduced diameter flexible VFD cable, Type TC-ER", "https://www.southwire.com/wire-cable/power-control/cu-600v-xlpe-insulation-shielded-tpe-jacket-xhhw-2-reduced-diameter-flexible-variable-frequency-drive-vfd-/p/SPEC45442"),
    ("Switchyard / SLD", "SPP GEN-2008-006 facility study - 2-on-1 CCGT, 138 kV one-lines", "https://opsportal.spp.org/documents/studies/files/2008_Generation_Studies/GEN-2008-006FS.pdf"),
]
for j, h in enumerate(("Topic", "Document", "URL"), start=1):
    c = rf.cell(row=4, column=j, value=h)
    c.font = HDR; c.fill = HFILL; c.border = BORDER
for i, (t, d, u) in enumerate(refs, start=5):
    rf.cell(row=i, column=1, value=t).font = BLACK
    rf.cell(row=i, column=2, value=d).font = BLACK
    c = rf.cell(row=i, column=3, value=u)
    c.hyperlink = u
    c.font = Font(name=F, size=9, color="0563C1", underline="single")
rf.column_dimensions["A"].width = 24
rf.column_dimensions["B"].width = 80
rf.column_dimensions["C"].width = 90

for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 90
wb.save(OUT)
print("rows", len(C), "equipment", len(E), "types", len(T))
