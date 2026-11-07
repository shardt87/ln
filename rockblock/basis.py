"""ER-RB Rev 00 basis register: every number that drives geometry or the takeoff, with its status and the source to
check. KNOWN = the Oct 26 call or the public record; WA = working assumption (stated, changed on feedback);
TV = to verify (named source to check). Nothing from any bid under NDA."""

DOC = "ER-RB Rev 00"
CREDIT = "Stephan Hardt - Power Generation Solutions"
STAMP = "Conceptual illustration · not engineered · not for construction"

K, WA, TV = "KNOWN", "WORKING ASSUMPTION", "TO VERIFY"

# key: (value, unit, status, statement, source / where to check)
B = {
    # ---- hierarchy -------------------------------------------------------------------------------------------
    "unit_kw":        (500, "kW", K, "Standard unit (ERT500): 500 kW standby rating", "Oct 26 call; ERT500 release (PR Newswire)"),
    "unit_kw_prime":  (450, "kW", K, "ERT500 prime / long-term rating (used in public permit filings)",
                       "ERT500 release; PUCT Docket 59076 (813 x 450 kW = 366 MW)"),
    "block_sqft":     (448, "sq ft", K, "RockBlock 2.5 MW footprint (units)", "erock.com/rock-block"),
    "blocks_4_or_5":  ("4 or 5", "units", K, "Units per RockBlock in a public campus filing", "PUCT Docket 59076"),
    "installed_mw":   ("1,059 (Mar 31) / 1,104 (Jun 30, 2026)", "MW", K, "Installed base", "ERock S-1/A; 10-Q Q2 2026"),
    "fleet":          ("2,000+ units, ~400 sites", "", K, "Deployed fleet", "ERock S-1/A"),
    "assembly":       ("Titan (Houston); Hyperion ~1.2 GW/yr by end 2026", "", K, "In-house assembly",
                       "ERock S-1/A"),
    "units_per_block": (5, "units", K, "Units paralleled per RockBlock (2.5 MW)", "Oct 26 call"),
    "rb_range":       ("1.5-3.5 MW in 0.5 MW steps", "", K, "RockBlock product range (3-7 units)", "ERock S-1/A"),
    "blocks_per_group": (8, "blocks", WA, "Blocks on one 35 kV loop to one switchgear breaker (~20 MW)",
                         "Cliff / ER engineering"),
    "groups_per_lineup": (4, "groups", K, "Generator-group breakers per switchgear lineup (about four)", "Oct 26 call"),
    "lineup_mw":      (75, "MW", K, "Feed from a lineup to the data center (about 75 MW)", "Oct 26 call"),
    # ---- voltages / conductors -------------------------------------------------------------------------------
    "gen_v":          (480, "V", K, "Generator output, 3-phase, to the GCB", "Oct 26 call; confirm with ER product sheet"),
    "dist_kv":        (34.5, "kV", TV, "Distribution / collection voltage (34.5 kV vs 13.8 kV)", "Cliff / ER engineering"),
    "xfmr_kva":       (3000, "kVA", WA, "One pad-mount step-up per block, 480 V : 34.5 kV (2.5-3 MVA)",
                       "ER product sheet / El Paso air permit"),
    "loop_cond":      ("3 x 1/C 750 kcmil Al, 35 kV, 133 %, concentric neutral", "", WA,
                       "35 kV collector loop conductor (call: mostly 750 / 500 kcmil Al)", "Cliff / ER engineering"),
    "l1_runs":        (2, "parallel sets", TV, "480 V generator leads: parallel sets per generator", "Cliff / ER engineering"),
    "l1_cond":        ("4 x 1/C 500 kcmil (3 phase + EGC), 600 V", "", TV, "480 V lead size and construction",
                       "Cliff / ER engineering"),
    "l2_runs":        (8, "parallel sets", TV, "GCB to transformer LV: parallel sets (or bus duct)", "Cliff / ER engineering"),
    "l2_cond":        ("4 x 1/C 600 kcmil (3 phase + N), 600 V", "", TV, "Block feed construction, cable vs bus",
                       "Cliff / ER engineering"),
    "feeder_sets":    (3, "parallel sets", TV, "~75 MW feeder: parallel 35 kV sets per lineup", "Cliff / ER engineering"),
    "feeder_scope":   ("customer or ER", "", TV, "Whether the ~75 MW feeders are in ER scope", "Cliff (one line)"),
    "ground":         ("4/0 bare Cu ring per block, #2/0 taps, rods at corners", "", WA, "Grounding scheme",
                       "ER engineering"),
    "control":        ("12/C #14 control + Cat6A per unit to the GCB; 12-strand SM fibre ring per group to the SWG / SCADA",
                       "", WA, "Control / comms architecture", "ER engineering"),
    # ---- geometry (dimensions) -------------------------------------------------------------------------------
    "genset_lwh":     ((10.0, 8.0, 9.0), "ft", TV, "ERT500 enclosure: 10 x 8 ft footprint KNOWN; 9 ft height TO VERIFY",
                       "ERT500 spec sheet (erock.com/ert500-spec-sheet)"),
    "stack_el":       (25.0, "ft", WA, "Stack top EL (TCEQ gas-EGU standard permit minimum 25 ft)", "TCEQ standard permit; site permit"),
    "gcb_lwh":        ((10.0, 4.0, 7.5), "ft", TV, "GCB (480 V panelboard, 5 breakers) L x W x H (placeholder)",
                       "ER product sheet"),
    "xfmr_lwh":       ((9.0, 9.0, 7.0), "ft", TV, "3 MVA pad-mount L x W x H (placeholder)", "ER / transformer data sheet"),
    "swg_lwh":        ((64.0, 16.0, 14.0), "ft", TV, "35 kV switchgear e-house L x W x H (placeholder)", "ER / switchgear data sheet"),
    "unit_pitch":     (8.6, "ft", WA, "Unit pitch in a block (5 x 8 ft units in a string, ~448 sq ft)", "ER layout"),
    "block_pitch":    (80.0, "ft", WA, "Block pitch along the row (block + fire separation)", "ER layout / NFPA 37"),
    "road_w":         (30.0, "ft", WA, "Access road between the two rows of a group", "ER layout"),
    "group_gap":      (32.0, "ft", WA, "Perimeter road between groups", "ER layout"),
    # ---- install allowances (takeoff) ------------------------------------------------------------------------
    "depth_lv":       (3.0, "ft", WA, "480 V trench depth to the cable", "NEC 300.5 / ER spec"),
    "depth_mv":       (4.0, "ft", WA, "35 kV duct / trench depth", "NEC 300.50 / ER spec"),
    "term_lv":        (3.0, "ft/end", WA, "Termination allowance per end, 600 V", "ER spec"),
    "term_mv":        (6.0, "ft/end", WA, "Termination allowance per end, 35 kV", "ER spec"),
    "slack":          (0.03, "of routed", WA, "Snaking / slack", "ER spec"),
    "spare":          (0.05, "", WA, "Spare (cut-length waste)", "ER spec"),
}


def v(k):
    return B[k][0]


def status(k):
    return B[k][2]


# ASSUMED-basis lengths (the alternative to MEASURED; never summed with it), per run, ft
ASSUMED_LEN = {"L1": 100.0, "L2": 20.0, "L3": 90.0, "L4": 300.0, "L5": 1500.0, "L6": 260.0, "L7": 100.0}

LAYERS = [
    # key, name, colour, status, dash
    ("L1", "480 V generator leads", "#2ab3a6", K, False),
    ("L2", "480 V block feed (GCB to transformer)", "#1f8a80", TV, False),
    ("L3", "35 kV collector loop (the quoted scope)", "#e3a21a", K, False),
    ("L4", "35 kV lineup ties", "#e3a21a", K, True),
    ("L5", "~75 MW feeders to the data center", "#d8402f", TV, False),
    ("L6", "Grounding", "#4caf50", WA, False),
    ("L7", "Control / comms", "#9aa3a8", WA, True),
]

# fixed equipment key (sheet bubbles and viewer legend)
KEY = [
    (1, "Genset unit, 500 kW (G-nnn-k)"), (2, "GCB, generator collector box, 480 V (GCB-nnn)"),
    (3, "Step-up transformer, 480 V : 34.5 kV (XFMR-nnn)"), (4, "35 kV loop corridor"),
    (5, "35 kV switchgear lineup e-house (SWG-x)"), (6, "Data center, customer (ghosted)"),
    (7, "Ownership line: ER scope / customer scope, TO VERIFY"), (8, "Operations / maintenance building"),
    (9, "Warehouse"), (10, "Water retention"), (11, "Gas metering skid"), (12, "Gas lateral (context)"),
    (13, "Access road"), (14, "Fence"),
]
