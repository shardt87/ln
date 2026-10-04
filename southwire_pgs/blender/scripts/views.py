"""Saved views: camera, visible collections, hidden/exploded objects and the
3-D anchor points for the three numbered callouts of each page.

Each view = one coherent configuration.  Collections not listed are hidden.
Callout 'label' = normalized image position (x from left, y from top) of the
numbered marker; the leader runs from the marker to the projected anchor.
"""
from mathutils import Vector

# ---------------------------------------------------------------------------
# collection groups
# ---------------------------------------------------------------------------
SWG = ["SWG_LV_Lineup", "SWG_LV_Panels", "SWG_LV_Bus", "SWG_LV_ControlDevices", "CW_Cabinet_S3",
       "CW_Door_Harness", "CW_Field_Cores", "PC_SWG_Incoming", "GND_SWG"]
KIT = ["CW_WireKit"]
GEN = ["GEN_Package", "GEN_Enclosure_Panels", "GEN_ControlCabinet", "CW_Gen_Harness", "PC_Gen_Aux",
       "GND_Gen", "TRAY_Gen_Riser"]
GEN_LV = GEN + ["GEN_TermBox_LV", "PC_Gen_LV_Out"]
GEN_MV = GEN + ["GEN_TermBox_MV", "PC_Gen_MV_Out", "GND_Gen_MV"]
CFG_A = GEN_LV + ["SWG_CfgA_Equipment", "ATS_Unit", "TRAY_CfgA", "PC_CfgA_GeneratorSource", "PC_CfgA_NormalSource",
                  "PC_CfgA_Load", "CW_CfgA_ATS", "GND_CfgA"]
CFG_B = GEN_LV + ["XFMR_Unit", "XFMR_Panels", "SWG_MV_Lineup", "TRAY_CfgB", "PC_CfgB_LV", "PC_CfgB_MV",
                  "CW_CfgB_XfmrAux", "GND_XFMR", "GND_MV"]
CFG_C = GEN_MV + ["SWG_MV_Lineup", "TRAY_CfgC", "PC_CfgC_MV", "CW_CfgC_Gen", "GND_MV"]
EH_ASM = ["EH_Section1", "EH_Section2", "EH_Panels", "TRAY_EH", "PC_EH_Factory", "PC_EH_FieldCompleted",
          "PC_EH_External", "CW_EH", "GND_EH", "GND_EH_FieldBond"]
EH_EXP = ["EH_Section1", "EH_Section2", "EH_Panels", "TRAY_EH", "PC_EH_Factory", "CW_EH", "GND_EH", "EH_FieldPackage"]
CFG_D = ["TMP_Generator", "TMP_DockingStation", "TMP_LoadBank", "TMP_CableStorage", "TMP_Panels",
         "PC_TMP_GenLeads", "PC_TMP_LoadBankLeads", "PC_TMP_DockInternal", "CW_TMP", "GND_TMP"]
ASM = ["ASM_Exploded", "ASM_Bench", "ANN_ASM"]

GEN_OPEN = ["GEN_Panel_F1", "GEN_Panel_F2", "GEN_Panel_F3", "GEN_Roof_1", "GEN_Roof_2",
            "GEN_TermBox_LV_Cover", "GEN_TermBox_MV_Cover", "GEN_LocalControlCabinet_Door"]
EH_OPEN = ["EH_S1_Roof", "EH_S2_Roof", "EH_S1_FrontWall", "EH_S2_FrontWall"]


def define_views(m):
    L, G, P, E, T, B = m["L"], m["G"], m["P"], m["E"], m["T"], m["B"]
    lw, kw, gw, ew, tw, bw = L.world, L.kit_world, G.world, E.world, T.world, B.world
    from mod_switchgear import P as bp, X3
    X3w = X3
    eh_s1 = [o.name for o in E.objs if o.get("explode_offset") is not None]
    v = {}

    def add(key, title, group, cam, tgt, lens, cols, hide=(), explode=(), rig="LGT_SWG", callouts=(), show=()):
        v[key] = {"title": title, "group": group, "camera": "CAM_" + key, "cam_loc": list(cam),
                  "cam_target": list(tgt), "lens": lens, "collections": list(cols), "hide_objects": list(hide),
                  "show_objects": list(show), "explode": list(explode), "rig": rig,
                  "callouts": [{"n": i + 1, "anchor": list(a), "label": list(lab)} for i, (a, lab) in enumerate(callouts)]}

    # ------------------------------------------------------------- switchgear
    add("IEM_ControlKit", "IEM - switchgear wire kit (main)", "Company pages",
        lw((4.05, -3.55, 2.35)), lw((2.55, -0.55, 0.98)), 32, SWG + KIT,
        hide=["SWG_S3_SidePanel_R"], rig="LGT_SWG",
        callouts=[(kw((3.45, -1.40, 0.863)), (0.86, 0.80)),
                  (kw((3.07, -1.02, 0.93)), (0.88, 0.50)),
                  (kw((3.52, -1.06, 0.866)), (0.93, 0.66))])
    add("EPD_ControlCabinet", "Electronic Power Design - control cabinet + kit", "Company pages",
        lw((3.55, -3.85, 1.9)), lw((2.5, -0.35, 1.1)), 33, SWG + KIT,
        hide=["SWG_S3_SidePanel_R"], rig="LGT_SWG",
        callouts=[(kw((3.52, -1.06, 0.866)), (0.90, 0.62)),
                  (lw(bp(0.30, 0.77, 0.05)), (0.18, 0.55)),
                  (kw((3.07, -1.02, 0.93)), (0.86, 0.40))])
    add("PATRIOT_Terminations", "Patriot - terminal and duct detail", "Company pages",
        lw((2.62, -0.70, 1.22)), lw((1.92, 0.44, 0.84)), 45, [c for c in SWG if c != "CW_Door_Harness"] + KIT,
        hide=["SWG_S3_SidePanel_R", "SWG_S3_ControlDoor"], rig="LGT_SWG",
        callouts=[(lw(bp(0.40, 0.77 + 0.0275 + 0.016, 0.018)), (0.85, 0.20)),
                  (lw(bp(0.33, 0.35 + 0.0275, 0.03)), (0.86, 0.80)),
                  (lw(bp(0.22, 0.56, 0.06)), (0.12, 0.42))])
    add("MAVERICK_Lineup", "Maverick - lineup, cable entry, control wiring", "Company pages",
        lw((5.0, -2.6, 2.15)), lw((1.55, 0.45, 1.0)), 32, [c for c in SWG if c != "CW_Door_Harness"],
        hide=["SWG_S3_SidePanel_R", "SWG_S3_ControlDoor", "GND_DoorBondStrap"], rig="LGT_SWG",
        callouts=[(lw((X3w + 0.28, 0.926, 0.64)), (0.88, 0.72)),
                  (lw(bp(0.45, 1.0, 0.05)), (0.20, 0.30)),
                  (lw((X3w + 0.62, 1.40, 0.24)), (0.86, 0.90))])
    # ------------------------------------------------------------- generator
    add("CAT_GenInterface", "Caterpillar - generator electrical interfaces", "Company pages",
        gw((8.0, -4.1, 2.75)), gw((4.55, -0.35, 1.35)), 30, GEN_LV, hide=GEN_OPEN, rig="LGT_PLANT",
        callouts=[(gw((3.86, -0.72, 1.18)), (0.10, 0.70)),
                  (gw((5.04, -0.70, 1.40)), (0.30, 0.22)),
                  (gw((5.66, 0.25, 2.2)), (0.90, 0.25))])
    add("TAYLOR_GenKits", "Taylor - generator with power-lead and control kits", "Company pages",
        gw((5.0, -7.9, 3.4)), gw((2.9, -1.2, 0.85)), 32, GEN_LV + ["GEN_Kits"], hide=GEN_OPEN, rig="LGT_PLANT",
        callouts=[(gw((1.6, -2.85, 0.22)), (0.10, 0.62)),
                  (gw((2.9, -2.7, 0.24)), (0.88, 0.62)),
                  (gw((1.6, -3.105, 0.07)), (0.40, 0.93))])
    # ------------------------------------------------------------- plant configs
    plant_cam, plant_tgt = (6.2, -9.8, 6.6), (0.7, 0.6, 1.3)
    add("CFG_A", "Configuration A - LV generator > ATS > load", "Configurations", plant_cam, plant_tgt, 32,
        CFG_A, hide=GEN_OPEN + ["ATS_Door"], rig="LGT_PLANT")
    add("CFG_B", "Configuration B - LV generator > step-up transformer > MV switchgear", "Configurations",
        plant_cam, plant_tgt, 32, CFG_B, hide=GEN_OPEN + ["XFMR_LV_Chamber_Cover", "XFMR_HV_Chamber_Cover"], rig="LGT_PLANT")
    add("CFG_C", "Configuration C - MV generator > MV switchgear", "Configurations", plant_cam, plant_tgt, 32,
        CFG_C, hide=GEN_OPEN, rig="LGT_PLANT")
    ax = P.ats_x
    add("ASCO_TransferInterface", "Schneider Electric / ASCO - transfer interfaces", "Company pages",
        (ax + 2.9, -4.5, 3.2), (ax + 0.45, 0.35, 1.6), 32, CFG_A, hide=GEN_OPEN + ["ATS_Door"], rig="LGT_PLANT",
        callouts=[((ax + 0.52, 0.39, 1.86), (0.12, 0.30)),
                  ((ax + 0.36, 0.39, 0.70), (0.12, 0.78)),
                  ((ax + 0.90, 0.57, 1.30), (0.88, 0.55))])
    add("RESA_TestBoundaries", "RESA Power - factory / field test boundaries", "Company pages",
        (7.3, -6.6, 5.0), (2.9, 0.8, 1.5), 32, CFG_B + ["ANN_CfgB_Boundaries"],
        hide=GEN_OPEN + ["XFMR_LV_Chamber_Cover", "XFMR_HV_Chamber_Cover"], rig="LGT_PLANT",
        callouts=[((5.6, 0.0, 1.7), (0.90, 0.72)),
                  ((3.25, 0.62, 2.38), (0.55, 0.12)),
                  ((P.hv_term[1].x, P.hv_term[1].y, 1.30), (0.30, 0.86))])
    # ------------------------------------------------------------- e-house
    add("POWELL_EhouseExploded", "Powell - e-house exploded with interconnect package", "Company pages",
        ew((10.8, -9.6, 7.6)), ew((6.0, 1.4, 1.3)), 28, EH_EXP, hide=EH_OPEN, explode=eh_s1, rig="LGT_EH",
        callouts=[(ew((5.45 - 1.5, 2.95, 3.0)), (0.12, 0.22)),
                  (ew((6.0, 1.35, 0.26)), (0.42, 0.90)),
                  (ew((6.0 + 1.5 + 0.06, 2.95, 3.37)), (0.66, 0.16))])
    add("SIEMENS_SkidBoundaries", "Siemens - skid factory / field boundaries", "Company pages",
        ew((12.5, -8.2, 6.8)), ew((6.3, 1.9, 1.6)), 30, EH_ASM + ["ANN_EH_Boundaries"], hide=EH_OPEN, rig="LGT_EH",
        callouts=[(ew((5.45, 2.95, 3.0)), (0.12, 0.20)),
                  (ew((6.0, 0.8, 2.6)), (0.45, 0.10)),
                  (ew((12.03, 1.3, 2.85)), (0.92, 0.42))])
    add("NVENT_EnclosureRouting", "nVent - roof removed, tray, entries, connections", "Company pages",
        ew((7.5, -7.5, 12.5)), ew((6.3, 1.9, 1.2)), 30, EH_ASM, hide=["EH_S1_Roof", "EH_S2_Roof"], rig="LGT_EH",
        callouts=[(ew((3.0, 2.95, 3.38)), (0.12, 0.18)),
                  (ew((12.03, 1.3, 2.85)), (0.92, 0.35)),
                  (ew((6.85, 3.15, 2.7)), (0.55, 0.12))])
    add("WESCO_StagedSupply", "Wesco - modules with staged reels and kits", "Company pages",
        ew((7.2, -13.4, 7.2)), ew((6.0, -0.5, 1.0)), 30, EH_EXP + ["EH_Staging"], hide=EH_OPEN, explode=eh_s1,
        rig="LGT_EH",
        callouts=[(ew((1.0, 2.2, 2.4)), (0.12, 0.12)),
                  (ew((2.5, -2.2, 1.05)), (0.10, 0.88)),
                  (ew((8.6 + 0.6, -2.75, 0.55)), (0.62, 0.90))])
    # ------------------------------------------------------------- temporary power
    add("CFG_D", "Configuration D - temporary generator > docking station > load bank", "Configurations",
        tw((12.0, -10.5, 5.2)), tw((6.4, -0.3, 0.6)), 28, CFG_D, hide=["TMP_DockingStation_Door"], rig="LGT_TMP")
    add("INPOWER_Docking", "InPower - docking station and lead sets", "Company pages",
        tw((10.4, -4.9, 2.5)), tw((7.25, -0.55, 0.8)), 32, CFG_D, hide=["TMP_DockingStation_Door"], rig="LGT_TMP",
        callouts=[(tw((6.3, -1.39, 0.03)), (0.10, 0.82)),
                  (tw((7.95, 0.13, 0.95)), (0.88, 0.30)),
                  (tw((7.33, -0.23, 0.88)), (0.20, 0.30))])
    add("MOSEBACH_LoadBankTest", "Mosebach - generator to load bank test leads", "Company pages",
        tw((11.4, -9.2, 4.7)), tw((6.4, -0.3, 0.6)), 29, CFG_D, hide=["TMP_DockingStation_Door"], rig="LGT_TMP",
        callouts=[(tw((9.0, -0.99, 0.03)), (0.55, 0.84)),
                  (tw((11.6, -0.66, 1.35)), (0.90, 0.30)),
                  (tw((5.5, 1.3, 0.85)), (0.30, 0.20))])
    # ------------------------------------------------------------- workbench
    add("WINAR_AssemblyBench", "Winar - exploded cable assembly", "Company pages",
        bw((0.84, -1.45, 1.88)), bw((0.84, 0.02, 0.93)), 31, ASM, rig="LGT_ASM",
        callouts=[(B.world(B.anchor[2]), (0.30, 0.86)),
                  (B.world(B.anchor[4]), (0.62, 0.86)),
                  (B.world(B.anchor[8]), (0.90, 0.22))])
    # ------------------------------------------------------------- module overviews
    add("MOD_Generator_Exploded", "Module 2 - generator, panels exploded", "Modules",
        gw((9.0, -8.5, 5.5)), gw((2.8, 0.0, 1.3)), 30, GEN_LV, explode=GEN_OPEN, rig="LGT_PLANT")
    add("MOD_Transformer", "Module 4 - transformer interface", "Modules",
        (5.6, -5.2, 3.5), (1.8, 0.55, 1.3), 30, ["XFMR_Unit", "XFMR_Panels", "GND_XFMR"],
        hide=["XFMR_LV_Chamber_Cover", "XFMR_HV_Chamber_Cover"], rig="LGT_PLANT")
    add("MOD_Ehouse_Exploded", "Module 3 - e-house exploded", "Modules",
        ew((11.5, -11.5, 9.0)), ew((6.0, 1.2, 1.3)), 28, EH_EXP, hide=EH_OPEN, explode=eh_s1, rig="LGT_EH")
    add("MOD_Switchgear_Overview", "Module 1 - lineup, kit beside", "Modules",
        lw((5.5, -5.2, 2.9)), lw((1.6, -0.3, 1.1)), 35, SWG + KIT, hide=["SWG_S3_SidePanel_R"], rig="LGT_SWG")
    return v
