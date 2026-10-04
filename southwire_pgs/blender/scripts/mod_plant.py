"""Plant zone: equipment and routing for Configurations A, B and C.

  A  LV generator -> automatic transfer switch (ATS) -> load distribution board
     (normal source from a utility service section; open-transition ATS)
  B  LV generator -> step-up unit transformer (Module 4) -> MV switchgear
  C  MV generator -> MV switchgear

World = local here (plant root at origin).  Generator root sits at x = -6.6,
so its end-wall riser tray hands cables over at x = -0.3, z = 3.185.
Only one configuration is shown per render (see sw_controls.apply_view).
"""
import math
from mathutils import Vector
import bpy
from swlib import (MB, M, coll, curve_obj, wire, text, empty, tag_panel, cyl_between, lug)

TZ = 3.25            # tray top level
RUNG = 3.17          # rung top (LV cables r 0.0135 sit at z 3.185)


def ladder_x(mb, x0, x1, y0, y1, rung_top, mat=None, pitch=0.25):
    mat = mat or M("Aluminium")
    for y in (y0, y1):
        mb.box_mm(x0, x1, y - 0.008, y, rung_top - 0.02, rung_top + 0.08, mat)
    x = x0 + 0.05
    while x < x1 - 0.02:
        mb.box_mm(x, x + 0.03, y0, y1 - 0.008, rung_top - 0.02, rung_top, mat)
        x += pitch


def ladder_y(mb, y0, y1, x0, x1, rung_top, mat=None, pitch=0.25):
    mat = mat or M("Aluminium")
    for x in (x0, x1):
        mb.box_mm(x - 0.008, x, y0, y1, rung_top - 0.02, rung_top + 0.08, mat)
    y = y0 + 0.05
    while y < y1 - 0.02:
        mb.box_mm(x0, x1 - 0.008, y, y + 0.03, rung_top - 0.02, rung_top, mat)
        y += pitch


def hanger(mb, x, y0, y1, rung_top, top=None):
    """Floor-standing H-frame tray support (strut posts + cross-arm)."""
    st = M("Steel_Galv")
    for y in (y0 - 0.06, y1 + 0.06):
        mb.box_mm(x - 0.02, x + 0.02, y - 0.02, y + 0.02, 0.0, rung_top - 0.02, st)
        mb.box_mm(x - 0.08, x + 0.08, y - 0.08, y + 0.08, 0.0, 0.01, st)
    mb.box_mm(x - 0.02, x + 0.02, y0 - 0.08, y1 + 0.08, rung_top - 0.06, rung_top - 0.02, st)


def cabinet(name, collection, x0, x1, y0, y1, h, plate_text=None, doors=2):
    """Simplified closed equipment section (context)."""
    mb = MB()
    p = M("Paint_ANSI61")
    mb.box_mm(x0 + 0.004, x1 - 0.004, y0 + 0.006, y1, 0.08, h, p)
    mb.box_mm(x0 + 0.01, x1 - 0.01, y0 + 0.01, y1 - 0.01, 0.0, 0.08, M("Paint_Base"))
    mb.box_mm(x0, x1, y0 - 0.004, y1 + 0.004, h, h + 0.012, p)
    zs = [0.09 + i * (h - 0.25) / doors for i in range(doors + 1)]
    for i in range(doors):
        mb.box_mm(x0 + 0.01, x1 - 0.01, y0 - 0.002, y0 + 0.006, zs[i] + 0.003, zs[i + 1] - 0.003, p)
        zc = (zs[i] + zs[i + 1]) / 2
        mb.box_mm(x1 - 0.07, x1 - 0.05, y0 - 0.03, y0 - 0.002, zc - 0.06, zc + 0.06, M("Plastic_Black"))
        w = x1 - x0
        mb.box_mm(x0 + w * 0.25, x0 + w * 0.70, y0 - 0.006, y0 - 0.001, zc - 0.12, zc + 0.10, M("Paint_Dark"))
        mb.box_mm(x0 + w * 0.30, x0 + w * 0.65, y0 - 0.009, y0 - 0.005, zc - 0.06, zc + 0.05, M("Glass_Dark"))
    mb.box_mm((x0 + x1) / 2 - 0.12, (x0 + x1) / 2 + 0.12, y0 - 0.004, y0, h - 0.17, h - 0.11, M("Marker_White"))
    for k in range(5):
        z = h - 0.10 + k * 0.014
        mb.box_mm(x0 + 0.12, x1 - 0.12, y0 - 0.003, y0 + 0.004, z, z + 0.006, M("Paint_Dark"))
    ob = mb.obj(name, collection, bevel=0.002)
    if plate_text:
        text(name + "_Plate", plate_text, 0.032, ((x0 + x1) / 2, y0 - 0.0045, h - 0.14),
             (math.radians(90), 0, 0), M("Label_Ink"), collection)
    return ob


def gland_plate(mb, x0, x1, y0, y1, z, holes):
    mb.box_mm(x0, x1, y0, y1, z, z + 0.006, M("Steel_Galv"))
    for (x, y, r) in holes:
        mb.cyl(r + 0.008, 0.02, (x, y, z + 0.016), M("Plastic_Black"), segs=6, smooth=False)


class Plant:
    def __init__(self, gen):
        self.gen = gen
        self.gx = gen.root.location.x
        self.L = 5.4
        # hand-over points from the generator module (world)
        self.lv_in = [gen.world(p) for p in gen.lv_exit]
        self.mv_in = [gen.world(p) for p in gen.mv_exit]
        self.ctl_in = gen.world(gen.ctl_exit)

    def build(self):
        self.cfg_a()
        self.cfg_b()
        self.cfg_c()
        return self

    # ==================================================================
    # Configuration A
    # ==================================================================
    def cfg_a(self):
        c_eq = coll("Switchgear/SWG_CfgA_Equipment")
        c_ats = coll("Switchgear/ATS_Unit")
        c_tr = coll("Cable_Tray/TRAY_CfgA")
        c_g = coll("Power_Cables/PC_CfgA_GeneratorSource")
        c_n = coll("Power_Cables/PC_CfgA_NormalSource")
        c_l = coll("Power_Cables/PC_CfgA_Load")
        c_cw = coll("Control_Wiring/CW_CfgA_ATS")
        c_gnd = coll("Grounding/GND_CfgA")
        D = 0.9
        AX = 1.6                                  # ATS x origin (1.0 wide)
        self.ats_x = AX
        cabinet("SWG_CfgA_LoadDistribution", c_eq, 0.2, 1.2, 0.0, D, 2.3, "LOAD DISTRIBUTION")
        cabinet("SWG_CfgA_UtilityService", c_eq, 3.0, 3.8, 0.0, D, 2.3, "UTILITY SERVICE")
        # ---------------- ATS enclosure (door removed) ----------------
        mb = MB()
        p = M("Paint_ANSI61")
        H = 2.3
        mb.shell(AX, AX + 1.2, 0.0, D, 0.08, H, 0.003, p, open=("-y", "+z"))
        mb.box_mm(AX + 0.01, AX + 1.19, 0.01, D - 0.01, 0.0, 0.08, M("Paint_Base"))
        mb.box_mm(AX, AX + 1.2, 0.0, D, H, H + 0.006, p)          # roof (gland plates added below)
        mb.box_mm(AX + 0.02, AX + 1.18, D - 0.02, D - 0.017, 0.12, H - 0.04, M("Backplate_White"))
        # transfer switch (two-position, mechanically interlocked)
        sx0, sx1 = AX + 0.28, AX + 0.76
        mb.box_mm(sx0, sx1, 0.44, 0.75, 0.95, 1.65, M("Plastic_Device"))
        mb.box_mm(sx0 + 0.02, sx1 - 0.02, 0.43, 0.44, 1.02, 1.26, M("Paint_Dark"))   # normal contacts
        mb.box_mm(sx0 + 0.02, sx1 - 0.02, 0.43, 0.44, 1.34, 1.58, M("Paint_Dark"))   # emergency contacts
        mb.box_mm(sx0 + 0.14, sx1 - 0.14, 0.36, 0.44, 1.22, 1.38, M("Paint_ANSI61")) # operator / interlock
        mb.box_mm(sx0 - 0.02, sx1 + 0.02, 0.70, 0.86, 0.95, 1.65, M("Steel_Dark"))   # mounting frame
        self.ats_lugs = {"N": [], "E": [], "L": [], "NB": []}
        xs = [AX + 0.36, AX + 0.52, AX + 0.68]
        for pi, xp in enumerate(xs):
            mb.box_mm(xp - 0.035, xp + 0.035, 0.40, 0.44, 1.65, 1.74, M("Copper_Tinned"))   # N pad (top)
            mb.box_mm(xp - 0.035, xp + 0.035, 0.40, 0.44, 0.86, 0.95, M("Copper_Tinned"))   # E pad (bottom)
            for dx in (-0.022, 0.022):
                lug(mb, Vector((xp + dx, 0.39, 1.84)), Vector((0, 0, -1)), 0.0125, tongue=(0.02, 0.006, 0.04))
                self.ats_lugs["N"].append(Vector((xp + dx, 0.39, 1.84)))
                lug(mb, Vector((xp + dx, 0.39, 0.77)), Vector((0, 0, 1)), 0.0125, tongue=(0.02, 0.006, 0.04))
                self.ats_lugs["E"].append(Vector((xp + dx, 0.39, 0.77)))
        for pi, zp in enumerate((1.12, 1.30, 1.48)):                      # load terminals (right side)
            mb.box_mm(sx1, sx1 + 0.04, 0.48, 0.66, zp - 0.03, zp + 0.03, M("Copper_Tinned"))
            for dy in (0.52, 0.62):
                lug(mb, Vector((sx1 + 0.13, dy, zp)), Vector((-1, 0, 0)), 0.0125, tongue=(0.02, 0.006, 0.04))
                self.ats_lugs["L"].append(Vector((sx1 + 0.13, dy, zp)))
        # solid neutral bar (bottom)
        mb.box_mm(AX + 0.26, AX + 0.92, 0.48, 0.52, 0.28, 0.33, M("Copper_Tinned"))
        mb.box_mm(AX + 0.26, AX + 0.30, 0.52, D - 0.02, 0.27, 0.34, M("Insulator_Gray"))
        mb.box_mm(AX + 0.88, AX + 0.92, 0.52, D - 0.02, 0.27, 0.34, M("Insulator_Gray"))
        # neutral lugs placed in the gaps between the E-phase risers (no crossings)
        for xn in (0.44, 0.60, 0.32, 0.76, 0.82, 0.87):
            lug(mb, Vector((AX + xn, 0.50, 0.42)), Vector((0, 0, -1)), 0.0125, tongue=(0.02, 0.006, 0.04))
            self.ats_lugs["NB"].append(Vector((AX + xn, 0.50, 0.42)))
        # ATS controller + control terminal strip
        mb.box_mm(AX + 0.05, AX + 0.27, D - 0.10, D - 0.02, 1.80, 2.10, M("Plastic_Device"))
        mb.box_mm(AX + 0.08, AX + 0.24, D - 0.102, D - 0.098, 1.92, 2.04, M("Glass_Dark"))
        mb.box_mm(AX + 0.30, AX + 0.62, D - 0.06, D - 0.02, 2.08, 2.13, M("Plastic_TB"))
        # gland plates on the roof: E (left), N (centre), L (right), control knockout
        gland_plate(mb, AX + 0.03, AX + 0.20, 0.05, 0.36, H + 0.006, [])
        gland_plate(mb, AX + 0.30, AX + 0.72, 0.38, 0.62, H + 0.006, [])
        gland_plate(mb, AX + 1.00, AX + 1.17, 0.62, 0.86, H + 0.006, [])
        self.own_ats = mb.obj("ATS_Enclosure_and_Switch", c_ats, bevel=0.0015)
        door = MB()
        door.box_mm(AX, AX + 1.2, -0.025, 0.0, 0.09, H, p)
        dob = door.obj("ATS_Door", c_ats, bevel=0.002)
        tag_panel(dob, explode=(0, -1.2, 0))
        for lab, pos in (("NORMAL", (AX + 0.52, 0.395, 1.95)), ("GENERATOR", (AX + 0.52, 0.395, 0.66)),
                         ("LOAD", (sx1 + 0.10, 0.44, 1.62)), ("NEUTRAL", (AX + 0.56, 0.395, 0.22))):
            mbp = MB()
            mbp.box_mm(pos[0] - 0.075, pos[0] + 0.075, pos[1] - 0.002, pos[1], pos[2] - 0.022, pos[2] + 0.022, M("Marker_White"))
            mbp.obj("ATS_Label_" + lab, c_ats)
            text("ATS_LabelText_" + lab, lab, 0.026 if len(lab) < 8 else 0.021, (pos[0], pos[1] - 0.0025, pos[2]),
                 (math.radians(90), 0, 0), M("Label_Ink"), c_ats)
        # ---------------- trays ----------------
        tr = MB()
        # generator-source tray (z 3.25) from generator riser to over ATS left
        ladder_x(tr, -0.30, AX + 0.10, -0.02, 0.40, RUNG)
        for x in (-0.05, 1.4):
            hanger(tr, x, -0.02, 0.40, RUNG)
        # normal-source tray (z 2.95) utility -> ATS
        n_r = 2.88
        ladder_x(tr, AX + 0.30, 3.70, 0.40, 0.64, n_r)
        hanger(tr, 2.9, 0.40, 0.64, n_r)
        # load tray (z 2.65) ATS -> load distribution
        l_r = 2.58
        ladder_x(tr, 0.45, AX + 1.17, 0.64, 0.88, l_r)
        hanger(tr, 1.43, 0.64, 0.88, l_r)
        # control conduit gen -> ATS (separate raceway)
        cy = 0.47
        tr.cyl(0.016, AX + 0.12 + 0.3, ((AX + 0.12 - 0.3) / 2, cy, 3.20), M("Steel_Galv"), axis="X")
        cyl_between(tr, (-0.3, 0.72, 3.20), (-0.1, cy, 3.20), 0.016, M("Steel_Galv"))
        tr.cyl(0.016, 3.20 - H - 0.02, (AX + 0.12, cy, (3.20 + H) / 2), M("Steel_Galv"))
        tr.obj("TRAY_CfgA_All", c_tr)
        # ---------------- generator-source cables ----------------
        names = ["A1", "A2", "B1", "B2", "C1", "C2", "N1", "N2"]
        for k, sp in enumerate(self.lv_in):
            y = sp.y
            xw = AX + (0.07 if k % 2 == 0 else 0.13)
            zb = 0.50 + k * 0.03
            pts = [sp, Vector((AX - 0.25, y, sp.z)), Vector((xw, y, sp.z - 0.10)), Vector((xw, y, 2.0)),
                   Vector((xw, y, zb))]
            if k < 6:
                tgt = self.ats_lugs["E"][k]
                pts += [Vector((tgt.x, y, zb)), Vector((tgt.x, tgt.y, zb + 0.06)), tgt + Vector((0, 0, -0.06)),
                        tgt + Vector((0, 0, 0.005))]
            else:
                tgt = self.ats_lugs["NB"][k - 6]
                zz = 0.62 + (k - 6) * 0.03
                pts[-1] = Vector((xw, y, zz))
                pts += [Vector((tgt.x, y, zz)), Vector((tgt.x, tgt.y, zz - 0.06)), tgt + Vector((0, 0, 0.06)),
                        tgt + Vector((0, 0, -0.005))]
            curve_obj(f"PC_CfgA_Gen_{names[k]}", [pts], 0.0135, M("Jacket_Power"), c_g, fr=0.14, seg=6)
        # ---------------- normal-source cables (utility -> ATS N) ----------------
        for k in range(8):
            yl = 0.43 + (k % 6) * 0.034 if k < 6 else 0.43 + (k - 6) * 0.034 + 0.03
            ys = 0.43 + k * 0.025
            x_u = 3.25 + (k % 4) * 0.08
            zl = n_r + 0.0135
            pts = [Vector((x_u, ys, 2.0)), Vector((x_u, ys, H + 0.02)), Vector((x_u, ys, zl - 0.25)),
                   Vector((x_u - 0.25, yl if k < 6 else 0.60, zl)), Vector((AX + 0.85, yl if k < 6 else 0.60, zl))]
            if k < 6:
                tgt = self.ats_lugs["N"][k]
                pts += [Vector((tgt.x + 0.08, yl, zl)), Vector((tgt.x, 0.45, zl - 0.25)),
                        Vector((tgt.x, 0.45, H)), Vector((tgt.x, tgt.y, 2.00)), tgt + Vector((0, 0, 0.06)),
                        tgt + Vector((0, 0, -0.005))]
            else:
                tgt = self.ats_lugs["NB"][2 + (k - 6)]
                xw = AX + 0.24 - (k - 6) * 0.03
                pts[-1] = Vector((AX + 0.60, 0.60, zl))
                pts += [Vector((xw + 0.15, 0.60, zl)), Vector((xw, 0.56, zl - 0.25)), Vector((xw, 0.56, H)),
                        Vector((xw, 0.56, 0.55 - (k - 6) * 0.03)), Vector((tgt.x, 0.56, 0.55 - (k - 6) * 0.03)),
                        Vector((tgt.x, tgt.y, 0.50 - (k - 6) * 0.03)), tgt + Vector((0, 0, 0.05)), tgt + Vector((0, 0, -0.005))]
            curve_obj(f"PC_CfgA_Normal_{names[k]}", [pts], 0.0135, M("Jacket_Power"), c_n, fr=0.14, seg=6)
        # ---------------- load cables (ATS L -> load distribution) ----------------
        for k in range(8):
            yl = 0.67 + k * 0.026
            zl = l_r + 0.0135
            xd = 0.55 + (k % 4) * 0.08
            xw = AX + 1.06 + (k % 2) * 0.06
            if k < 6:
                tgt = self.ats_lugs["L"][k]
                pts = [tgt + Vector((-0.005, 0, 0)), tgt + Vector((0.05, 0, 0)), Vector((xw, tgt.y, tgt.z)),
                       Vector((xw, yl, tgt.z + 0.10)), Vector((xw, yl, H)), Vector((xw, yl, zl - 0.18))]
            else:
                tgt = self.ats_lugs["NB"][4 + (k - 6)]
                zz = 0.48 + (k - 6) * 0.03
                pts = [tgt + Vector((0, 0, -0.005)), tgt + Vector((0, 0, 0.05)), Vector((tgt.x, tgt.y, zz)),
                       Vector((tgt.x, yl, zz)), Vector((xw, yl, zz + 0.02)), Vector((xw, yl, H)), Vector((xw, yl, zl - 0.18))]
            pts += [Vector((xw - 0.18, yl, zl)), Vector((xd + 0.2, yl, zl)), Vector((xd, yl, zl - 0.2)),
                    Vector((xd, yl, H - 0.10))]
            curve_obj(f"PC_CfgA_Load_{names[k]}", [pts], 0.0135, M("Jacket_Power"), c_l, fr=0.14, seg=6)
        # ---------------- ATS control wiring ----------------
        sp = []
        tbx = [AX + 0.32 + i * 0.03 for i in range(10)]
        for i, x in enumerate(tbx[:5]):     # TB -> controller
            a = Vector((x, D - 0.06, 2.08))
            b = Vector((AX + 0.20 - i * 0.02, D - 0.10, 2.0))
            sp.append([a, a + Vector((0, -0.01, -0.05)), Vector((b.x + 0.04, D - 0.07, 1.98)), b])
        for i, x in enumerate(tbx[5:]):     # TB -> operator / position switches
            a = Vector((x, D - 0.06, 2.08))
            sp.append([a, a + Vector((0, -0.01, -0.05)), Vector((x, D - 0.08, 1.80)),
                       Vector((AX + 0.46 + i * 0.02, 0.60, 1.72)), Vector((AX + 0.46 + i * 0.02, 0.62, 1.66))])
        curve_obj("CW_CfgA_ATS_Internal", sp, 0.0016, M("Wire_Control"), c_cw, fr=0.03)
        # engine-start / communication cable gen -> ATS control terminal strip
        pts = [self.ctl_in, Vector((-0.10, cy, 3.20)), Vector((AX + 0.12, cy, 3.20)), Vector((AX + 0.12, cy, H - 0.02)),
               Vector((AX + 0.12, D - 0.06, 2.20)), Vector((AX + 0.40, D - 0.06, 2.16)), Vector((AX + 0.40, D - 0.06, 2.12))]
        wire("CW_CfgA_EngineStart_Cable", pts, 0.006, M("Jacket_Control"), c_cw, fr=0.1)
        # ---------------- grounding ----------------
        g = MB()
        for x0 in (0.2, AX, 3.0):
            g.box_mm(x0 + 0.3, x0 + 0.5, -0.006, 0.0, 0.10, 0.16, M("Copper_Tinned"))
        g.obj("GND_CfgA_Pads", c_gnd)
        for i, x0 in enumerate((0.2, AX, 3.0)):
            wire(f"GND_CfgA_GEC_{i+1}", [Vector((x0 + 0.4, -0.01, 0.13)), Vector((x0 + 0.4, -0.06, 0.08)),
                                         Vector((x0 + 0.4, -0.08, -0.05))], 0.006, M("Wire_Ground"), c_gnd, fr=0.04)

    # ==================================================================
    # Configuration B (transformer = Module 4) and MV switchgear
    # ==================================================================
    def mv_switchgear(self):
        c = coll("Switchgear/SWG_MV_Lineup")
        X0, W, Dm, H = 4.2, 0.9, 2.3, 2.45
        self.mvx = X0
        for i in range(3):
            x0 = X0 + i * W
            cabinet(f"SWG_MV_S{i+1}", c, x0, x0 + W, 0.0, Dm, H, f"MV SECTION {i+1}", doors=2)
        mb = MB()
        gland_plate(mb, X0 + 0.15, X0 + 0.75, 1.70, 2.20, H + 0.012, [])
        gland_plate(mb, X0 + W + 0.25, X0 + W + 0.65, 1.80, 2.20, H + 0.012, [])
        mb.box_mm(X0 + 0.3, X0 + 0.6, -0.006, 0.0, 0.10, 0.16, M("Copper_Tinned"))
        mb.obj("SWG_MV_RoofGlands_GroundPad", c)
        wire("GND_MV_GEC", [Vector((X0 + 0.45, -0.01, 0.13)), Vector((X0 + 0.45, -0.06, 0.08)),
                            Vector((X0 + 0.45, -0.08, -0.05))], 0.006, M("Wire_Ground"), coll("Grounding/GND_MV"), fr=0.04)
        self.mv_drop = [Vector((X0 + 0.30 + k * 0.15, 1.95, H)) for k in range(3)]
        self.mv_ctl_drop = Vector((X0 + W + 0.45, 2.0, H))

    def transformer(self):
        """Module 4 -- simplified unit substation transformer: tank + radiators,
        LV and HV air-terminal chambers with top cable entry, aux/control box."""
        c = coll("Transformer/XFMR_Unit")
        cp = coll("Transformer/XFMR_Panels")
        mb = MB()
        t = M("Paint_Transformer")
        TX0, TX1, TY0, TY1 = 0.85, 2.55, 0.15, 1.15
        self.xf = (TX0, TX1, TY0, TY1)
        mb.box_mm(TX0, TX1, TY0, TY1, 0.12, 2.05, t)                           # tank
        mb.box_mm(TX0 - 0.03, TX1 + 0.03, TY0 - 0.03, TY1 + 0.03, 2.05, 2.10, t)   # cover
        mb.box_mm(TX0 + 0.05, TX1 - 0.05, TY0 + 0.05, TY1 - 0.05, 0.0, 0.12, M("Paint_Base"))
        for side, y in ((-1, TY0), (1, TY1)):                                   # radiator banks
            for k in range(9):
                x = TX0 + 0.15 + k * 0.16
                yy0 = y - 0.40 if side < 0 else y
                yy1 = y if side < 0 else y + 0.40
                mb.box_mm(x, x + 0.03, yy0, yy1, 0.35, 1.85, t)
            yy0 = y - 0.06 if side < 0 else y
            yy1 = y if side < 0 else y + 0.06
            mb.box_mm(TX0 + 0.12, TX1 - 0.12, yy0, yy1, 1.80, 1.88, t)
            mb.box_mm(TX0 + 0.12, TX1 - 0.12, yy0, yy1, 0.32, 0.40, t)
        # lifting lugs, nameplate area, conservator-free sealed tank
        for (x, y) in ((TX0, TY0), (TX1, TY0), (TX0, TY1), (TX1, TY1)):
            mb.box_mm(x - 0.03, x + 0.03, y - 0.03, y + 0.03, 2.10, 2.20, M("Steel_Dark"))
        mb.box_mm(1.5, 1.9, TY0 - 0.41, TY0 - 0.405, 1.45, 1.70, M("Marker_White"))
        # auxiliary / control enclosure (gauges, alarm contacts)
        mb.box_mm(1.25, 1.55, TY0 - 0.50, TY0 - 0.42, 1.25, 1.65, M("Paint_ANSI61"))
        mb.box_mm(1.25, 1.55, TY0 - 0.42, TY0 - 0.40, 1.35, 1.40, M("Steel_Dark"))
        for k in range(2):
            mb.cyl(0.05, 0.03, (1.33 + k * 0.14, TY0 - 0.515, 1.55), M("Paint_Dark"), axis="Y", segs=24)
            mb.cyl(0.04, 0.005, (1.33 + k * 0.14, TY0 - 0.532, 1.55), M("Marker_White"), axis="Y", segs=24)
        self.aux_box_top = Vector((1.40, TY0 - 0.46, 1.65))
        # LV air-terminal chamber (left) -- open front for view
        LX0, LX1 = 0.20, TX0
        mb.shell(LX0, LX1, 0.05, 1.25, 0.10, 2.35, 0.003, t, open=("-y",))
        gland_plate(mb, LX0 + 0.06, LX1 - 0.06, 0.08, 0.40, 2.356, [])
        self.lv_spades = []
        for i, yb in enumerate((0.30, 0.52, 0.74, 0.96)):        # X1 X2 X3 X0 bushings
            mb.cyl(0.05, 0.22, (TX0 - 0.11, yb, 1.55), M("Insulator"), axis="X", segs=20)
            for k in range(3):
                mb.cyl(0.07, 0.015, (TX0 - 0.06 - k * 0.05, yb, 1.55), M("Insulator"), axis="X", segs=24)
            mb.box_mm(TX0 - 0.36, TX0 - 0.20, yb - 0.04, yb + 0.04, 1.53, 1.56, M("Copper_Tinned"))   # spade
            for dx in (-0.31, -0.25):
                lug(mb, Vector((TX0 + dx, yb, 1.68)), Vector((0, 0, -1)), 0.0125, tongue=(0.02, 0.006, 0.06))
                self.lv_spades.append(Vector((TX0 + dx, yb, 1.68)))
        # HV air-terminal chamber (right)
        HX0, HX1 = TX1, TX1 + 1.0
        mb.shell(HX0, HX1, 0.05, 1.25, 0.10, 2.35, 0.003, t, open=("-y",))
        gland_plate(mb, HX1 - 0.25, HX1 - 0.05, 0.10, 1.10, 2.356, [])
        self.hv_term = []
        for i, yb in enumerate((0.30, 0.62, 0.94)):              # H1 H2 H3 bushings + terminations
            mb.cyl(0.045, 0.32, (TX1 + 0.16, yb, 1.70), M("Insulator"), axis="X", segs=20)
            for k in range(5):
                mb.cyl(0.075, 0.012, (TX1 + 0.04 + k * 0.055, yb, 1.70), M("Insulator"), axis="X", segs=24)
            mb.box_mm(TX1 + 0.30, TX1 + 0.42, yb - 0.02, yb + 0.02, 1.60, 1.74, M("Copper"))
            xt = TX1 + 0.40
            mb.cyl(0.016, 0.08, (xt, yb, 1.56), M("Copper_Tinned"))                  # lug barrel
            mb.cyl(0.028, 0.36, (xt, yb, 1.34), M("Insulator_Gray"), segs=20)         # termination body
            for k in range(3):
                mb.cyl(0.06, 0.012, (xt, yb, 1.46 - k * 0.07), M("Insulator_Gray"), segs=24)
            self.hv_term.append(Vector((xt, yb, 1.16)))
        mb.obj("XFMR_Tank_Chambers_Aux", c, bevel=0.003)
        # removable chamber front covers
        for nm, x0, x1 in (("LV", LX0, LX1), ("HV", HX0, HX1)):
            cv = MB()
            cv.box_mm(x0, x1, 0.02, 0.05, 0.10, 2.35, t)
            ob = cv.obj(f"XFMR_{nm}_Chamber_Cover", cp, bevel=0.002)
            tag_panel(ob, explode=(0, -1.0, 0))
        g = MB()
        g.box_mm(TX1 - 0.3, TX1 - 0.1, TY0 - 0.006, TY0, 0.15, 0.22, M("Copper_Tinned"))
        g.obj("GND_XFMR_TankPad", coll("Grounding/GND_XFMR"))
        wire("GND_XFMR_GEC", [Vector((TX1 - 0.2, TY0 - 0.01, 0.18)), Vector((TX1 - 0.2, TY0 - 0.06, 0.10)),
                              Vector((TX1 - 0.2, TY0 - 0.08, -0.05))], 0.006, M("Wire_Ground"), coll("Grounding/GND_XFMR"), fr=0.04)
        self.hv_roof = HX1 - 0.15

    def cfg_b(self):
        self.mv_switchgear()
        self.transformer()
        c_tr = coll("Cable_Tray/TRAY_CfgB")
        c_lv = coll("Power_Cables/PC_CfgB_LV")
        c_mv = coll("Power_Cables/PC_CfgB_MV")
        c_cw = coll("Control_Wiring/CW_CfgB_XfmrAux")
        tr = MB()
        ladder_x(tr, -0.30, 0.45, -0.02, 0.40, RUNG)
        hanger(tr, -0.05, -0.02, 0.40, RUNG)
        # MV tray: HV chamber -> over to switchgear rear (plan elbow)
        mv_r = 3.15
        hx = self.hv_roof
        ladder_x(tr, hx - 0.15, 3.95, 0.05, 1.10, mv_r)
        ladder_y(tr, 1.10, 2.20, 3.55, 3.95, mv_r)
        ladder_x(tr, 3.95, self.mvx + 0.85, 1.75, 2.20, mv_r)
        hanger(tr, 3.75, 0.05, 1.10, mv_r)
        hanger(tr, 4.10, 1.75, 2.20, mv_r)
        # aux control conduit transformer -> MV switchgear
        a = self.aux_box_top
        pts_c = [a, Vector((a.x, a.y, 2.85)), Vector((3.45, a.y, 2.85)), Vector((3.45, 2.0, 2.85)),
                 Vector((self.mv_ctl_drop.x, 2.0, 2.85)), self.mv_ctl_drop]
        for i in range(len(pts_c) - 1):
            cyl_between(tr, pts_c[i], pts_c[i + 1], 0.016, M("Steel_Galv"), segs=12)
        tr.obj("TRAY_CfgB_All", c_tr)
        wire("CW_CfgB_XfmrAlarm_Cable", [p + Vector((0, 0, 0)) for p in pts_c] + [self.mv_ctl_drop + Vector((0, 0, -0.3))],
             0.006, M("Jacket_Control"), c_cw, fr=0.08)
        # LV: generator -> LV chamber spades
        for k, sp in enumerate(self.lv_in):
            tgt = self.lv_spades[k]
            xd = 0.28 + (k % 2) * 0.08
            pts = [sp, Vector((xd + 0.2, sp.y, sp.z)), Vector((xd, sp.y, sp.z - 0.2)), Vector((xd, sp.y, 2.36)),
                   Vector((xd, sp.y, 2.20)), Vector((tgt.x, tgt.y, 1.95)), tgt + Vector((0, 0, 0.06)),
                   tgt + Vector((0, 0, -0.005))]
            curve_obj(f"PC_CfgB_LV_{k+1}", [pts], 0.0135, M("Jacket_Power"), c_lv, fr=0.14, seg=6)
        # MV: HV chamber terminations -> tray -> MV switchgear incoming section
        for k, tp in enumerate(self.hv_term):
            yl = tp.y
            xd = hx - 0.05 + k * 0.0
            zc = mv_r + 0.019
            xt = 3.62 + k * 0.12
            yt = 1.85 + k * 0.10
            pts = [tp + Vector((0, 0, 0.005)), tp + Vector((0, 0, -0.10)), Vector((tp.x, yl, 0.62)),
                   Vector((xd, yl, 0.62)), Vector((xd, yl, 2.36)), Vector((xd, yl, zc - 0.3)),
                   Vector((xt, yl, zc)), Vector((xt, yt, zc)), Vector((self.mv_drop[k].x + 0.25, yt, zc)),
                   Vector((self.mv_drop[k].x, yt, zc - 0.3)), Vector((self.mv_drop[k].x, yt, self.mv_drop[k].z + 0.02)),
                   Vector((self.mv_drop[k].x, yt, self.mv_drop[k].z - 0.3))]
            curve_obj(f"PC_CfgB_MV_{'ABC'[k]}", [pts], 0.019, M("Jacket_Power"), c_mv, fr=0.28, seg=8)
        # boundary markers (presentation): equipment-supplied | site-installed
        ann = coll("Annotations/ANN_CfgB_Boundaries")
        b = MB()
        for (x0, x1, y0, y1, z) in ((0.24, 0.81, 0.06, 1.24, 2.37), (self.xf[1] + 0.02, self.xf[1] + 0.98, 0.06, 1.24, 2.37),
                                    (self.mvx + 0.05, self.mvx + 0.85, 1.65, 2.25, 2.475)):
            b.box_mm(x0, x1, y0, y1, z, z + 0.004, M("Boundary_Field"))
        b.obj("ANN_CfgB_SiteInstalledBoundary", ann)

    # ==================================================================
    def cfg_c(self):
        c_tr = coll("Cable_Tray/TRAY_CfgC")
        c_mv = coll("Power_Cables/PC_CfgC_MV")
        c_cw = coll("Control_Wiring/CW_CfgC_Gen")
        tr = MB()
        mv_r = 3.155
        ladder_x(tr, -0.30, 3.95, -0.02, 0.40, mv_r)
        ladder_y(tr, 0.40, 2.20, 3.55, 3.95, mv_r)
        ladder_x(tr, 3.95, self.mvx + 0.85, 1.75, 2.20, mv_r)
        for x in (0.6, 2.0, 3.3):
            hanger(tr, x, -0.02, 0.40, mv_r)
        hanger(tr, 4.10, 1.75, 2.20, mv_r)
        # control conduit gen -> MV switchgear
        cpts = [self.ctl_in, Vector((3.45, self.ctl_in.y, self.ctl_in.z)), Vector((3.45, 2.0, self.ctl_in.z)),
                Vector((self.mv_ctl_drop.x, 2.0, self.ctl_in.z)), self.mv_ctl_drop]
        for i in range(len(cpts) - 1):
            cyl_between(tr, cpts[i], cpts[i + 1], 0.016, M("Steel_Galv"), segs=12)
        tr.obj("TRAY_CfgC_All", c_tr)
        wire("CW_CfgC_GenControl_Cable", cpts + [self.mv_ctl_drop + Vector((0, 0, -0.3))], 0.006,
             M("Jacket_Control"), c_cw, fr=0.08)
        for k, sp in enumerate(self.mv_in):
            zc = sp.z
            xt = 3.62 + k * 0.12
            yt = 1.85 + k * 0.10
            d = self.mv_drop[k]
            pts = [sp, Vector((xt, sp.y, zc)), Vector((xt, yt, zc)), Vector((d.x + 0.25, yt, zc)),
                   Vector((d.x, yt, zc - 0.3)), Vector((d.x, yt, d.z + 0.02)), Vector((d.x, yt, d.z - 0.3))]
            curve_obj(f"PC_CfgC_MV_{'ABC'[k]}", [pts], 0.019, M("Jacket_Power"), c_mv, fr=0.28, seg=8)
