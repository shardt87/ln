"""Module 2 -- Enclosed generator set (simplified engine, accurate electrical
interfaces).  Local frame: x from radiator end (0) to alternator/exit end (L),
y across (front/camera side = -y), z up.  Parented to 'GEN_Root'.

Interfaces modelled:
  * alternator terminal box (LV variant and MV variant, selectable)
  * output power cables  terminal box -> end-wall gland plate (external exit)
  * local control cabinet with engine harness, AVR/sensing and remote-control cables
  * battery / starter auxiliary wiring
  * removable enclosure panels with exploded offsets
"""
import math
from mathutils import Vector
import bpy
from swlib import (MB, M, coll, curve_obj, wire, bezier_cable, text, tag_panel,
                   tag_explode, cyl_between, lug)

L, HW = 5.4, 1.0          # enclosure length, half width
ZT, ZR = 0.40, 2.60       # top of fuel-tank base, roof
AX_Z = 1.15               # crank / alternator axis height


class Generator:
    def __init__(self, root_loc, name="GEN", scale_len=1.0):
        self.name = name
        self.root = bpy.data.objects.new(name + "_Root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.location = root_loc
        coll("Generator").objects.link(self.root)
        self.objs = []
        self.c_pkg = coll("Generator/GEN_Package")
        self.c_pan = coll("Generator/GEN_Enclosure_Panels")
        self.c_tblv = coll("Generator/GEN_TermBox_LV")
        self.c_tbmv = coll("Generator/GEN_TermBox_MV")
        self.c_ctl = coll("Generator/GEN_ControlCabinet")
        self.c_cw = coll("Control_Wiring/CW_Gen_Harness")
        self.c_pclv = coll("Power_Cables/PC_Gen_LV_Out")
        self.c_pcmv = coll("Power_Cables/PC_Gen_MV_Out")
        self.c_aux = coll("Power_Cables/PC_Gen_Aux")
        self.c_gnd = coll("Grounding/GND_Gen")

    def own(self, ob):
        ob.parent = self.root
        self.objs.append(ob)
        return ob

    def world(self, p):
        return self.root.location + Vector(p)

    def build(self):
        self.base_and_frame()
        self.enclosure_panels()
        self.engine()
        self.alternator()
        self.termbox_lv()
        self.termbox_mv()
        self.control_cabinet()
        self.aux_wiring()
        self.grounding()
        self.riser_tray()
        return self

    # ------------------------------------------------------------------
    def base_and_frame(self):
        mb = MB()
        base, frame = M("Paint_Base"), M("Paint_Enclosure")
        mb.box_mm(0, L, -HW, HW, 0.0, ZT, base)                       # sub-base fuel tank
        for y in (-0.62, 0.50):
            mb.box_mm(0.2, L - 0.2, y, y + 0.12, ZT, ZT + 0.14, M("Steel_Dark"))   # skid rails
        t = 0.06
        for (x, y) in [(0, -HW), (L - t, -HW), (0, HW - t), (L - t, HW - t), (1.8, -HW), (3.6, -HW),
                       (1.8, HW - t), (3.6, HW - t)]:
            mb.box_mm(x, x + t, y, y + t, ZT, ZR, frame)              # posts
        for y in (-HW, HW - t):
            mb.box_mm(0, L, y, y + t, ZR - t, ZR, frame)              # top rails
            mb.box_mm(0, L, y, y + t, ZT, ZT + t, frame)
        for x in (0, L - t):
            mb.box_mm(x, x + t, -HW, HW, ZR - t, ZR, frame)
        # radiator-end wall with discharge louvre
        mb.box_mm(-0.02, 0.0, -HW, HW, ZT, ZR, frame)
        for k in range(14):
            z = 0.75 + k * 0.1
            mb.box_mm(-0.06, -0.02, -0.75, 0.75, z, z + 0.05, M("Paint_Dark"), )
        # alternator-end wall with external cable gland plate (the external interface)
        mb.box_mm(L, L + 0.02, -HW, HW, ZT, ZR, frame)
        mb.box_mm(L + 0.02, L + 0.03, 0.05, 0.85, 0.80, 1.30, M("Steel_Galv"))
        self.own(mb.obj("GEN_Base_and_Frame", self.c_pkg, bevel=0.004))
        # roof-mounted exhaust silencer (context)
        ex = MB()
        ex.cyl(0.22, 1.6, (1.6, 0.25, ZR + 0.32), M("Steel_Dark"), axis="X")
        ex.cyl(0.09, 0.5, (2.4, 0.25, ZR + 0.15), M("Steel_Dark"))
        ex.box_mm(1.0, 2.2, 0.05, 0.45, ZR, ZR + 0.08, M("Steel_Dark"))
        self.own(ex.obj("GEN_Exhaust_Silencer", self.c_pkg))

    def enclosure_panels(self):
        """Removable side and roof panels (sound-attenuated enclosure)."""
        enc = M("Paint_Enclosure")
        spans = [(0.0, 1.8), (1.8, 3.6), (3.6, L)]
        for side, ys in (("F", -HW - 0.03), ("R", HW)):
            for i, (x0, x1) in enumerate(spans):
                mb = MB()
                mb.box_mm(x0 + 0.005, x1 - 0.005, ys, ys + 0.03, ZT + 0.01, ZR - 0.01, enc)
                yo = ys - 0.004 if side == "F" else ys + 0.034
                mb.box_mm(x1 - 0.22, x1 - 0.18, min(yo, ys) - 0.015 if side == "F" else ys + 0.03,
                          ys if side == "F" else ys + 0.045, 1.35, 1.55, M("Plastic_Black"))      # latch handle
                for k in range(3):                                          # intake louvres
                    z = 1.9 + k * 0.12
                    mb.box_mm(x0 + 0.25, x1 - 0.25, ys - 0.012 if side == "F" else ys + 0.03,
                              ys if side == "F" else ys + 0.042, z, z + 0.05, M("Paint_Dark"))
                ob = mb.obj(f"GEN_Panel_{side}{i+1}", self.c_pan, bevel=0.004)
                tag_panel(ob, explode=(0, -1.6 if side == "F" else 1.6, 0))
                self.own(ob)
        for i, (x0, x1) in enumerate([(0, 2.7), (2.7, L)]):
            mb = MB()
            mb.box_mm(x0, x1, -HW - 0.03, HW + 0.03, ZR, ZR + 0.04, enc)
            ob = mb.obj(f"GEN_Roof_{i+1}", self.c_pan, bevel=0.004)
            tag_panel(ob, explode=(0, 0, 1.4))
            self.own(ob)

    # ------------------------------------------------------------------
    def engine(self):
        mb = MB()
        eng, blk = M("Paint_Engine"), M("Steel_Dark")
        # radiator + fan guard
        mb.box_mm(0.15, 0.45, -0.85, 0.85, 0.60, 2.25, M("Radiator_Black"))
        mb.box_mm(0.12, 0.48, -0.88, 0.88, 0.57, 0.62, eng)
        mb.box_mm(0.12, 0.48, -0.88, 0.88, 2.22, 2.27, eng)
        mb.cyl(0.62, 0.12, (0.56, 0, 1.40), M("Steel_Dark"), axis="X", segs=32)
        mb.torus(0.62, 0.012, (0.62, 0, 1.40), M("Steel_Galv"), axis="X", segs=40)
        # block, oil pan, V-heads, intake, turbos
        mb.box_mm(0.75, 3.0, -0.42, 0.42, 0.78, 1.50, eng)
        mb.box_mm(0.95, 2.80, -0.32, 0.32, 0.56, 0.78, eng)
        for s in (-1, 1):
            mb.box((2.05, 0.30, 0.20), (1.90, s * 0.36, 1.63), eng, rot=(s * math.radians(-28), 0, 0))
            mb.box((1.95, 0.24, 0.06), (1.90, s * 0.43, 1.76), M("Paint_Dark"), rot=(s * math.radians(-28), 0, 0))
            mb.cyl(0.13, 0.20, (3.05, s * 0.48, 1.78), blk, axis="Y")          # turbo
        mb.box_mm(0.9, 2.9, -0.12, 0.12, 1.55, 1.78, M("Aluminium"))          # intake plenum
        mb.cyl(0.08, 0.95, (3.05, 0.0, 2.15), blk)                             # exhaust riser to silencer
        mb.cyl(0.62, 0.25, (3.12, 0, AX_Z), eng, axis="X", segs=36, r2=0.55)    # flywheel housing
        # engine mounts
        for x in (0.95, 2.65):
            for s in (-1, 1):
                mb.box_mm(x - 0.08, x + 0.08, s * 0.56 - 0.07, s * 0.56 + 0.07, ZT + 0.14, 0.82, blk)
        # engine ECM + starter (wiring interface points)
        mb.box_mm(1.55, 1.95, -0.47, -0.42, 1.05, 1.35, M("Plastic_Device"))
        mb.cyl(0.08, 0.30, (2.92, -0.42, 0.86), blk, axis="X")
        self.ecm = Vector((1.75, -0.48, 1.06))
        self.starter = Vector((2.78, -0.50, 0.86))
        self.own(mb.obj("GEN_Engine_Radiator", self.c_pkg, bevel=0.01))

    def alternator(self):
        mb = MB()
        alt = M("Paint_Engine")
        mb.cyl(0.60, 1.30, (3.90, 0, AX_Z), alt, axis="X", segs=48)
        for k in range(10):
            mb.torus(0.605, 0.008, (3.35 + k * 0.12, 0, AX_Z), M("Paint_Dark"), axis="X", segs=48, rsegs=6)
        mb.cyl(0.50, 0.15, (4.62, 0, AX_Z), alt, axis="X", segs=40)
        mb.cyl(0.30, 0.06, (4.72, 0, AX_Z), M("Paint_Dark"), axis="X", segs=32)
        for x in (3.40, 4.40):
            for s in (-1, 1):
                mb.box_mm(x - 0.1, x + 0.1, s * 0.56 - 0.08, s * 0.56 + 0.08, ZT + 0.14, AX_Z - 0.40, M("Steel_Dark"))
        self.own(mb.obj("GEN_Alternator", self.c_pkg, bevel=0.0))

    # ------------------------------------------------------------------
    TRAY_Z = 3.25          # overhead tray level (external interface continues here)
    RISER_X = L + 0.26     # vertical riser tray on the alternator-end wall

    def _cable_exit_route(self, start, k, n, y_exit, z_gl):
        """Gland -> layered run along the skid -> end-wall gland plate -> riser tray
        -> overhead tray start.  Each cable has its own z layer and y lane."""
        y_k = -0.86 + k * 0.032
        z_k = 0.64 + k * 0.034
        return [start, Vector((start.x, start.y, z_k + 0.10)), Vector((start.x, y_k, z_k)),
                Vector((4.92, y_k, z_k)), Vector((5.12, y_exit, z_k + 0.05)),
                Vector((L - 0.12, y_exit, z_gl)), Vector((L + 0.03, y_exit, z_gl)),
                Vector((self.RISER_X, y_exit, z_gl + 0.12)), Vector((self.RISER_X, y_exit, self.TRAY_Z - 0.25)),
                Vector((self.RISER_X + 0.25, y_exit, self.TRAY_Z - 0.065)), Vector((L + 0.9, y_exit, self.TRAY_Z - 0.065))]

    def riser_tray(self):
        """External cable interface: gland plate + ladder riser on the end wall."""
        c = coll("Cable_Tray/TRAY_Gen_Riser")
        mb = MB()
        al = M("Aluminium")
        y0, y1 = -0.02, 0.40
        xr = self.RISER_X
        ce = (xr + 0.12, self.TRAY_Z - 0.19)          # elbow centre (x, z)
        for y in (y0, y1):
            mb.box_mm(xr - 0.07, xr + 0.03, y - 0.008, y, 0.75, ce[1], al)                    # side rails (vertical)
            mb.box_mm(ce[0], L + 1.6, y - 0.008, y, self.TRAY_Z - 0.10, self.TRAY_Z, al)    # horizontal start
            # curved side plate of the 90-degree vertical elbow (annular sector)
            ro, ri, n = 0.19, 0.09, 12
            arc_o = [(ce[0] - ro * math.cos(math.pi / 2 * k / n), ce[1] + ro * math.sin(math.pi / 2 * k / n)) for k in range(n + 1)]
            arc_i = [(ce[0] - ri * math.cos(math.pi / 2 * k / n), ce[1] + ri * math.sin(math.pi / 2 * k / n)) for k in range(n, -1, -1)]
            mb.poly_prism(arc_o + arc_i, y - 0.008, y, al, plane="XZ")
        for z in [0.85 + 0.25 * k for k in range(10) if 0.85 + 0.25 * k < ce[1] - 0.05]:
            mb.box_mm(xr - 0.045, xr - 0.015, y0, y1, z, z + 0.02, al)                       # rungs
        for x in [xr + 0.25 + 0.25 * k for k in range(5)]:
            mb.box_mm(x, x + 0.03, y0, y1, self.TRAY_Z - 0.10, self.TRAY_Z - 0.08, al)
        for k in (3, 6, 9):                                                                   # elbow rungs
            ang = math.pi / 2 * k / 12
            mb.box((0.03, y1 - y0, 0.02), (ce[0] - 0.165 * math.cos(ang), (y0 + y1) / 2, ce[1] + 0.165 * math.sin(ang)),
                   al, rot=(0, ang, 0))
        # wall brackets
        for z in (1.4, 2.4):
            mb.box_mm(L + 0.02, xr - 0.07, y0, y1, z, z + 0.03, M("Steel_Dark"))
        self.own(mb.obj("TRAY_Gen_Riser", c, bevel=0.0))

    def termbox_lv(self):
        """LV terminal box on the front (-y) side; cover removable."""
        c = self.c_tblv
        x0, x1, y0, y1, z0, z1 = 3.55, 4.35, -0.95, -0.58, 0.88, 1.66
        mb = MB()
        mb.shell(x0, x1, y0, y1, z0, z1, 0.004, M("Paint_Engine"), open=("-y",))
        mb.box_mm(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.02, z0, z0 + 0.006, M("Steel_Galv"))   # gland plate
        # landing bus (T1 T2 T3 N) on insulators
        self.lv_lugs = []
        for i, xb in enumerate((3.68, 3.86, 4.04, 4.22)):
            mb.box_mm(xb - 0.025, xb + 0.025, -0.70, -0.694, 1.12, 1.52, M("Copper"))
            mb.box_mm(xb - 0.02, xb + 0.02, -0.694, -0.62, 1.40, 1.46, M("Insulator_Gray"))
            mb.box_mm(xb - 0.02, xb + 0.02, -0.694, -0.62, 1.16, 1.22, M("Insulator_Gray"))
            for j, dz in enumerate((1.30, 1.18)):
                # two lugs per terminal, barrel pointing down
                lx = xb + (-0.012 if j == 0 else 0.012)
                lug(mb, Vector((lx, -0.712, dz - 0.09)), Vector((0, 0, 1)), 0.012,
                    tongue=(0.022, 0.006, 0.05))
                self.lv_lugs.append(Vector((lx, -0.712, dz - 0.09)))
            # stator lead from alternator frame to bus top
            mb.cyl(0.03, 0.02, (xb, -0.585, 1.56), M("Rubber"), axis="Y")
        self.own(mb.obj("GEN_TermBox_LV", c, bevel=0.002))
        leads = []
        for i, xb in enumerate((3.68, 3.86, 4.04, 4.22)):
            leads.append([Vector((xb, -0.58, 1.56)), Vector((xb, -0.64, 1.58)), Vector((xb, -0.69, 1.53)),
                          Vector((xb, -0.705, 1.50))])
        self.own(curve_obj("GEN_StatorLeads_LV", leads, 0.011, M("Insulator_Gray"), c, fr=0.04))
        cov = MB()
        cov.box_mm(x0 - 0.01, x1 + 0.01, y0 - 0.006, y0, z0 - 0.01, z1 + 0.01, M("Paint_Engine"))
        ob = cov.obj("GEN_TermBox_LV_Cover", self.c_pan, bevel=0.002)
        tag_panel(ob, explode=(0, -0.9, 0))
        self.own(ob)
        # output cables: 2 per phase + 2 neutral -> external exit
        tlab = ["T1", "T2", "T3", "N"]
        self.lv_exit = []
        g = MB()
        for k, lp in enumerate(self.lv_lugs):
            gl = Vector((lp.x, -0.80 + (k % 2) * 0.05, z0))
            y_exit, z_gl = 0.08 + k * 0.035, 0.92 + (k % 2) * 0.16
            pts = [lp + Vector((0, 0, -0.02)), lp + Vector((0, 0, -0.10)), gl + Vector((0, 0, 0.06))]
            pts += self._cable_exit_route(gl, k, 8, y_exit, z_gl)
            ob = curve_obj(f"PC_Gen_LV_{tlab[k//2]}_{k%2+1}", [pts], 0.0135, M("Jacket_Power"), self.c_pclv, fr=0.12, seg=6)
            self.own(ob)
            self.lv_exit.append(pts[-1])
            g.cyl(0.02, 0.02, (gl.x, gl.y, z0 - 0.002), M("Plastic_Black"), segs=6, smooth=False)
            g.cyl(0.021, 0.03, (L + 0.03, y_exit, z_gl), M("Plastic_Black"), axis="X", segs=6, smooth=False)
        self.own(g.obj("PC_Gen_LV_Glands", self.c_pclv))

    def termbox_mv(self):
        """MV terminal box variant (larger, three stress-cone terminations, no N)."""
        c = self.c_tbmv
        x0, x1, y0, y1, z0, z1 = 3.45, 4.45, -1.00, -0.58, 0.80, 1.85
        mb = MB()
        mb.shell(x0, x1, y0, y1, z0, z1, 0.004, M("Paint_Engine"), open=("-y",))
        mb.box_mm(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.02, z0, z0 + 0.006, M("Steel_Galv"))
        self.mv_term = []
        for i, xb in enumerate((3.66, 3.95, 4.24)):
            # standoff insulator with terminal pad
            mb.cyl(0.035, 0.18, (xb, -0.68, 1.62), M("Insulator"), segs=20)
            for k in range(5):
                mb.cyl(0.05, 0.012, (xb, -0.68, 1.55 + k * 0.035), M("Insulator"), segs=20)
            mb.box_mm(xb - 0.03, xb + 0.03, -0.70, -0.66, 1.71, 1.74, M("Copper"))
            # cable termination: lug + stress cone + skirts
            mb.cyl(0.016, 0.07, (xb, -0.75, 1.67), M("Copper_Tinned"))
            mb.box_mm(xb - 0.015, xb + 0.015, -0.755, -0.745, 1.70, 1.74, M("Copper_Tinned"))
            mb.cyl(0.028, 0.32, (xb, -0.75, 1.47), M("Insulator_Gray"), segs=20)
            for k in range(3):
                mb.cyl(0.055, 0.012, (xb, -0.75, 1.52 - k * 0.06), M("Insulator_Gray"), segs=24)
            self.mv_term.append(Vector((xb, -0.75, 1.31)))
            mb.cyl(0.03, 0.03, (xb, -0.585, 1.62), M("Rubber"), axis="Y")
        self.own(mb.obj("GEN_TermBox_MV", c, bevel=0.002))
        cov = MB()
        cov.box_mm(x0 - 0.01, x1 + 0.01, y0 - 0.006, y0, z0 - 0.01, z1 + 0.01, M("Paint_Engine"))
        ob = cov.obj("GEN_TermBox_MV_Cover", self.c_pan, bevel=0.002)
        tag_panel(ob, explode=(0, -0.9, 0))
        self.own(ob)
        for k, tp in enumerate(self.mv_term):
            gl = Vector((tp.x, -0.80, z0))
            y_exit, z_gl = 0.08 + k * 0.12, 1.0
            pts = [tp, tp + Vector((0, 0, -0.15)), gl + Vector((0, 0, 0.08))]
            pts += self._cable_exit_route(gl, k * 3, 3, y_exit, z_gl)
            ob = curve_obj(f"PC_Gen_MV_{'ABC'[k]}", [pts], 0.019, M("Jacket_Power"), self.c_pcmv, fr=0.2, seg=6)
            self.own(ob)
            # shield drain / ground lead from termination to box ground
            gpt = Vector((tp.x, -0.75, 1.28))
            ob = wire(f"GND_Gen_MV_Shield_{'ABC'[k]}", [gpt, gpt + Vector((0.05, -0.02, -0.05)),
                                                         Vector((tp.x + 0.08, -0.62, 0.95)), Vector((tp.x + 0.08, -0.62, 0.86))],
                      0.003, M("Braid"), coll("Grounding/GND_Gen_MV"), fr=0.03)
            self.own(ob)
        self.mv_exit = [Vector((L + 0.9, 0.08 + k * 0.12, self.TRAY_Z - 0.065)) for k in range(3)]
        g = MB()
        g.box_mm(3.6, 4.4, -0.64, -0.60, 0.84, 0.88, M("Copper"))
        for k in range(3):
            p = Vector((L + 0.03, 0.08 + k * 0.12, 1.0))
            g.cyl(0.028, 0.03, tuple(p), M("Plastic_Black"), axis="X", segs=6, smooth=False)
        self.own(g.obj("PC_Gen_MV_Glands_GroundBar", self.c_pcmv))

    # ------------------------------------------------------------------
    def control_cabinet(self):
        c = self.c_ctl
        x0, x1, y0, y1, z0, z1 = 4.78, 5.30, -0.93, -0.63, 1.00, 1.85
        mb = MB()
        mb.shell(x0, x1, y0, y1, z0, z1, 0.003, M("Paint_ANSI61"), open=("-y",))
        mb.box_mm(x0 + 0.02, x1 - 0.02, y1 - 0.01, y1 - 0.006, z0 + 0.03, z1 - 0.03, M("Backplate_White"))
        mb.box_mm(x0 + 0.04, x1 - 0.04, y1 - 0.08, y1 - 0.01, z0 + 0.48, z0 + 0.72, M("Plastic_Device"))   # controller
        mb.box_mm(x0 + 0.06, x1 - 0.06, y1 - 0.082, y1 - 0.079, z0 + 0.52, z0 + 0.68, M("Glass_Dark"))
        mb.box_mm(x0 + 0.04, x1 - 0.04, y1 - 0.05, y1 - 0.01, z0 + 0.12, z0 + 0.17, M("Plastic_TB"))      # terminal strip
        mb.box_mm(x0 + 0.03, x0 + 0.07, y1 - 0.06, y1 - 0.01, z0 + 0.20, z0 + 0.45, M("Plastic_Duct"))
        mb.box_mm(x1 - 0.07, x1 - 0.03, y1 - 0.06, y1 - 0.01, z0 + 0.20, z0 + 0.45, M("Plastic_Duct"))
        for k in range(4):
            mb.box_mm(x0 + 0.10 + k * 0.08, x0 + 0.16 + k * 0.08, y1 - 0.07, y1 - 0.01, z0 + 0.28, z0 + 0.40, M("Plastic_DeviceLt"))
        # wall brackets to the alternator-end wall (keeps the floor clear for cables)
        for z in (z0 + 0.05, z1 - 0.10):
            mb.box_mm(x1, L, y0 + 0.04, y1 - 0.04, z, z + 0.04, M("Steel_Dark"))
        self.own(mb.obj("GEN_LocalControlCabinet", c, bevel=0.002))
        door = MB()
        door.box_mm(-0.52, 0, -0.02, 0.0, 0, 0.85, M("Paint_ANSI61"))
        door.box_mm(-0.44, -0.08, -0.024, -0.02, 0.48, 0.70, M("Glass_Dark"))
        ob = door.obj("GEN_LocalControlCabinet_Door", self.c_pan, bevel=0.002)
        ob.location = (x1, y0, z0)
        ob.rotation_euler = (0, 0, math.radians(100))
        tag_panel(ob)
        self.own(ob)
        self.ctl_tb = [Vector((x0 + 0.06 + k * 0.03, y1 - 0.05, z0 + 0.12)) for k in range(14)]
        self.ctl_box = (x0, x1, y0, y1, z0, z1)
        # internal wiring: controller -> terminal strip (presentation blue)
        sp = []
        for k in range(14):
            a = Vector((x0 + 0.06 + k * 0.03, y1 - 0.05, z0 + 0.17))
            b = Vector((x0 + 0.10 + (k % 7) * 0.05, y1 - 0.06, z0 + 0.48))
            sp.append([a, a + Vector((0, 0, 0.04)), Vector((a.x, a.y - 0.005 * (k % 3), z0 + 0.25)), b + Vector((0, 0, -0.03)), b])
        self.own(curve_obj("CW_GenCtl_Internal", sp, 0.0015, M("Wire_Control"), self.c_cw, fr=0.02))

    def aux_wiring(self):
        x0, x1, y0, y1, z0, z1 = self.ctl_box
        # engine harness: ECM -> along skid rail -> control cabinet bottom
        bottom = Vector((x0 + 0.12, -0.80, z0))
        h = [self.ecm, self.ecm + Vector((0, -0.05, -0.08)), Vector((1.8, -0.72, 0.60)),
             Vector((3.2, -0.72, 0.60)), Vector((4.6, -0.72, 0.60)), Vector((bottom.x, bottom.y, 0.75)),
             bottom + Vector((0, 0, 0.02))]
        bundle = []
        for k in range(6):
            a = 2 * math.pi * k / 6
            off = Vector((0, math.cos(a), math.sin(a))) * 0.007
            bundle.append([p + off for p in h])
        self.own(curve_obj("CW_Gen_EngineHarness", bundle, 0.0028, M("Wire_Control"), self.c_cw, fr=0.08))
        self.own(curve_obj("CW_Gen_EngineHarness_Conduit", [h[1:-1]], 0.012, M("Plastic_Black"), self.c_cw, fr=0.08))
        # AVR / voltage-sensing cable: terminal box -> control cabinet
        s = Vector((4.30, -0.80, 0.88))
        pts = [s, s + Vector((0, 0, -0.06)), Vector((4.5, -0.85, 0.72)), Vector((x0 + 0.2, -0.85, 0.75)),
               Vector((x0 + 0.2, -0.80, z0 - 0.02)), Vector((x0 + 0.2, -0.80, z0 + 0.02))]
        self.own(wire("CW_Gen_AVR_Sensing", pts, 0.006, M("Jacket_Control"), self.c_cw, fr=0.06))
        # remote start / communication cable: cabinet top -> across above power cables
        # -> end-wall gland -> conduit up the end wall (separate from power cables)
        s = Vector((x1 - 0.08, -0.78, z1))
        yc = 0.72
        pts = [s, s + Vector((0, 0, 0.12)), Vector((L - 0.12, -0.60, z1 + 0.15)), Vector((L - 0.12, yc, z1 + 0.15)),
               Vector((L + 0.10, yc, z1 + 0.15)), Vector((L + 0.10, yc, self.TRAY_Z - 0.05)),
               Vector((L + 0.40, yc, self.TRAY_Z - 0.05)), Vector((L + 0.9, yc, self.TRAY_Z - 0.05))]
        self.own(wire("CW_Gen_RemoteControl_Cable", pts, 0.006, M("Jacket_Control"), self.c_cw, fr=0.08))
        self.ctl_exit = pts[-1]
        g = MB()
        g.cyl(0.012, 0.03, (L + 0.03, yc, z1 + 0.15), M("Plastic_Black"), axis="X", segs=6, smooth=False)
        g.box_mm(L + 0.02, L + 0.03, yc - 0.07, yc + 0.07, z1 + 0.08, z1 + 0.22, M("Steel_Galv"))
        g.cyl(0.016, self.TRAY_Z - z1 - 0.25, (L + 0.10, yc, (z1 + 0.2 + self.TRAY_Z - 0.05) / 2), M("Steel_Galv"))
        g.cyl(0.016, 0.5, (L + 0.65, yc, self.TRAY_Z - 0.05), M("Steel_Galv"), axis="X")
        self.own(g.obj("CW_Gen_Control_Gland_Conduit", self.c_cw))
        # battery + starter cables
        b = MB()
        for k in range(2):
            b.box_mm(0.62 + k * 0.2, 0.80 + k * 0.2, -0.92, -0.70, ZT + 0.02, ZT + 0.26, M("Plastic_Black"))
            b.cyl(0.012, 0.02, (0.66 + k * 0.2, -0.80, ZT + 0.27), M("Pilot_Red"))
            b.cyl(0.012, 0.02, (0.76 + k * 0.2, -0.80, ZT + 0.27), M("Plastic_Device"))
        self.own(b.obj("GEN_Batteries", self.c_pkg))
        pos = [Vector((0.86, -0.80, ZT + 0.28)), Vector((0.86, -0.80, ZT + 0.36)), Vector((1.4, -0.66, 0.66)),
               Vector((2.5, -0.58, 0.70)), self.starter + Vector((-0.05, 0, 0.04)), self.starter]
        self.own(bezier_cable("PC_Gen_Starter_Positive", pos, 0.009, M("Jacket_Power"), self.c_aux))
        neg = [Vector((0.66, -0.80, ZT + 0.28)), Vector((0.66, -0.80, ZT + 0.33)), Vector((0.7, -0.66, ZT + 0.16))]
        self.own(bezier_cable("PC_Gen_Battery_Negative", neg, 0.009, M("Jacket_Power"), self.c_aux))

    def grounding(self):
        g = MB()
        g.box_mm(L - 0.4, L - 0.1, -HW - 0.035, -HW - 0.03, 0.18, 0.26, M("Copper_Tinned"))   # ground pad
        self.own(g.obj("GND_Gen_GroundPad", self.c_gnd))
        pts = [Vector((L - 0.25, -HW - 0.05, 0.20)), Vector((L - 0.25, -HW - 0.12, 0.12)),
               Vector((L - 0.25, -HW - 0.16, 0.0)), Vector((L - 0.25, -HW - 0.16, -0.05))]
        self.own(bezier_cable("GND_Gen_GEC", pts, 0.006, M("Wire_Ground"), self.c_gnd))

    # ------------------------------------------------------------------
    def kits_beside(self):
        """Separate power-lead kit and control-wire kit staged beside the set
        (used for the generator-production application)."""
        c = coll("Generator/GEN_Kits")
        n0 = len(self.objs)
        mb = MB()
        # pallet
        def pallet(x0, y0, w, d):
            for k in range(5):
                mb.box_mm(x0, x0 + w, y0 + k * (d - 0.09) / 4, y0 + k * (d - 0.09) / 4 + 0.09, 0.11, 0.13, M("Wood_Reel"))
            for k in range(3):
                mb.box_mm(x0 + k * (w - 0.09) / 2, x0 + k * (w - 0.09) / 2 + 0.09, y0, y0 + d, 0.0, 0.11, M("Wood_Reel"))
        pallet(1.0, -3.1, 1.2, 1.0)
        pallet(2.5, -3.0, 0.8, 0.6)
        # power-lead kit: pre-cut leads with lugs coiled on the pallet
        coils = []
        lugs = MB()
        for i in range(4):
            cx, cy = 1.32 + (i % 2) * 0.56, -2.85 + (i // 2) * 0.5
            for t in range(2):
                r = 0.20 - t * 0.035
                pts = []
                for k in range(26):
                    a = 2 * math.pi * k / 24
                    pts.append(Vector((cx + r * math.cos(a), cy + r * math.sin(a), 0.15 + 0.03 * t + 0.0012 * k)))
                coils.append(pts)
                e = pts[-1]
                lug(lugs, e, Vector((-math.sin(2 * math.pi * 25 / 24), math.cos(2 * math.pi * 25 / 24), 0)), 0.012)
                lugs.cyl(0.0145, 0.05, tuple(e + Vector((0, 0, 0.0))), M("Marker_White"), segs=12)
        self.own(curve_obj("KIT_Gen_PowerLeads", coils, 0.0135, M("Jacket_Power"), c, fr=0.0))
        self.own(lugs.obj("KIT_Gen_PowerLead_Lugs_Markers", c))
        # control-wire kit tote on the second pallet
        mb.box_mm(2.56, 3.24, -2.94, -2.46, 0.13, 0.139, M("Tote"))
        for (a, b, cc, d) in [(2.56, 3.24, -2.94, -2.934), (2.56, 3.24, -2.466, -2.46), (2.56, 2.566, -2.94, -2.46), (3.234, 3.24, -2.94, -2.46)]:
            mb.box_mm(a, b, cc, d, 0.13, 0.26, M("Tote"))
        mb.box_mm(2.89, 2.896, -2.94, -2.46, 0.13, 0.25, M("Tote"))
        mb.box_mm(2.62, 3.18, -2.946, -2.94, 0.17, 0.23, M("Marker_White"))
        mb.box_mm(1.25, 1.95, -3.106, -3.10, 0.03, 0.10, M("Marker_White"))
        self.own(mb.obj("KIT_Gen_Pallets_Tote", c, bevel=0.002))
        sp = []
        for b in range(2):
            for i in range(10):
                x = 2.62 + b * 0.33 + i * 0.022
                z = 0.15 + (i % 3) * 0.004
                sp.append([Vector((x, -2.91, 0.24)), Vector((x, -2.88, z)), Vector((x + 0.01, -2.52, z)),
                           Vector((x + 0.02, -2.50, z + 0.02)), Vector((x + 0.03, -2.55, z + 0.03)), Vector((x + 0.03, -2.86, 0.25))])
        self.own(curve_obj("KIT_Gen_ControlWires", sp, 0.0017, M("Wire_Control"), c, fr=0.02))
        self.own(text("KIT_Gen_PowerLeadKit_Label", "POWER LEAD KIT", 0.04, (1.6, -3.11, 0.065),
                      (math.radians(90), 0, 0), M("Label_Ink"), c))
        self.own(text("KIT_Gen_ControlKit_Label", "CONTROL WIRE KIT", 0.03, (2.9, -2.947, 0.20),
                      (math.radians(90), 0, 0), M("Label_Ink"), c))
        for ob in self.objs[n0:]:
            ob.parent = self.root
