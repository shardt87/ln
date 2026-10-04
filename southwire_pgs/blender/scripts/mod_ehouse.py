"""Module 3 -- Modular electrical building (e-house / skid), two shipping sections.

Local frame: x along the building (section 1: 0..6, section 2: 6..12),
y depth (front wall y=0, back wall y=3.6), z up (skid base 0..0.45).
Removable: roof panels (one per section) and the front wall (one per section).
Exploded view: section 1 moves -1.5 m, section 2 moves +1.5 m in x and the
interconnect cable package is shown staged between them.

Scope colouring (presentation only):
  * factory-installed cables: black jackets
  * connections completed after placement onsite: amber highlight
"""
import math
from mathutils import Vector
import bpy
from swlib import (MB, M, coll, curve_obj, wire, text, tag_panel, tag_explode, instance_mesh, cyl_between, lug)
from mod_plant import ladder_x, cabinet, gland_plate

LEN, SPLIT, DEP = 12.0, 6.0, 3.6
ZF, ZW = 0.45, 4.0          # finished floor, wall top
RUNG = 3.35
TY0, TY1 = 2.70, 3.20       # tray y range
EXP = 1.5                   # exploded offset per section


class EHouse:
    def __init__(self, root_loc, bay_mesh_obj):
        self.root = bpy.data.objects.new("EH_Root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.location = root_loc
        coll("Ehouse").objects.link(self.root)
        self.bay = bay_mesh_obj
        self.c = {1: coll("Ehouse/EH_Section1"), 2: coll("Ehouse/EH_Section2")}
        self.c_pan = coll("Ehouse/EH_Panels")
        self.c_pkg = coll("Ehouse/EH_FieldPackage")
        self.c_stage = coll("Ehouse/EH_Staging")
        self.c_tr = coll("Cable_Tray/TRAY_EH")
        self.c_fac = coll("Power_Cables/PC_EH_Factory")
        self.c_fld = coll("Power_Cables/PC_EH_FieldCompleted")
        self.c_ext = coll("Power_Cables/PC_EH_External")
        self.c_cw = coll("Control_Wiring/CW_EH")
        self.c_gnd = coll("Grounding/GND_EH")
        self.c_ann = coll("Annotations/ANN_EH_Boundaries")
        self.objs = []

    def own(self, ob, sec=None):
        ob.parent = self.root
        if sec == 1:
            tag_explode(ob, (-EXP, 0, 0))
        elif sec == 2:
            tag_explode(ob, (EXP, 0, 0))
        self.objs.append(ob)
        return ob

    def world(self, p):
        return self.root.location + Vector(p)

    def build(self):
        self.structure()
        self.equipment()
        self.trays()
        self.cables()
        self.grounding()
        self.field_package()
        self.staging()
        self.boundaries()
        return self

    # ------------------------------------------------------------------
    def structure(self):
        for s, (x0, x1) in ((1, (0.0, SPLIT)), (2, (SPLIT, LEN))):
            mb = MB()
            beam, wall = M("Paint_Base"), M("Paint_Enclosure")
            # skid base: perimeter W-beams + cross members + floor plate
            for y in (0.0, DEP - 0.25):
                mb.box_mm(x0, x1, y, y + 0.25, 0.0, 0.40, beam)
            for x in (x0, x1 - 0.25):
                mb.box_mm(x, x + 0.25, 0.0, DEP, 0.0, 0.40, beam)
            mb.box_mm(x0, x1, 0.0, DEP, 0.40, ZF, M("Steel_Galv"))
            for x in (x0 + 0.2, x1 - 0.45):                       # lifting lugs
                for y in (-0.06, DEP):
                    mb.box_mm(x, x + 0.25, y, y + 0.06, 0.12, 0.34, M("Steel_Dark"))
            # back wall and outer end wall (split side left open)
            mb.box_mm(x0, x1, DEP - 0.08, DEP, ZF, ZW, wall)
            if s == 1:
                mb.box_mm(x0, x0 + 0.08, 0.0, DEP, ZF, ZW, wall)
            else:
                mb.box_mm(x1 - 0.08, x1, 0.0, DEP, ZF, ZW, wall)
                # personnel door on end wall
                mb.box_mm(x1, x1 + 0.01, 0.6, 1.6, ZF, ZF + 2.15, M("Paint_ANSI61"))
            # wall posts at the split (structural frame stays)
            xp = x1 - 0.12 if s == 1 else x0
            for y in (0.0, DEP - 0.12):
                mb.box_mm(xp, xp + 0.12, y, y + 0.12, ZF, ZW, beam)
            mb.box_mm(xp, xp + 0.12, 0.0, DEP, ZW - 0.15, ZW, beam)
            ob = mb.obj(f"EH_S{s}_Skid_Walls", self.c[s], bevel=0.004)
            self.own(ob, s)
            # removable roof and front wall
            r = MB()
            r.box_mm(x0, x1, -0.05, DEP + 0.05, ZW, ZW + 0.12, wall)
            r.box_mm(x0, x1, DEP / 2 - 0.05, DEP / 2 + 0.05, ZW + 0.12, ZW + 0.16, wall)
            ob = r.obj(f"EH_S{s}_Roof", self.c_pan, bevel=0.004)
            tag_panel(ob)
            ob["explode_offset"] = [(-EXP if s == 1 else EXP), 0, 0]
            self.own(ob)
            f = MB()
            f.box_mm(x0 + (0.08 if s == 1 else 0), x1 - (0.08 if s == 2 else 0), 0.0, 0.08, ZF, ZW, wall)
            for k in range(4):
                xx = x0 + 0.8 + k * 1.3
                f.box_mm(xx, xx + 0.6, -0.01, 0.0, ZW - 0.6, ZW - 0.35, M("Paint_Dark"))   # HVAC louvres
            ob = f.obj(f"EH_S{s}_FrontWall", self.c_pan, bevel=0.004)
            tag_panel(ob)
            ob["explode_offset"] = [(-EXP if s == 1 else EXP), 0, 0]
            self.own(ob)
            # shipping-section stencil on the base beam
            t = text(f"EH_S{s}_Stencil", f"SHIPPING SECTION {s}", 0.16, ((x0 + x1) / 2, -0.002, 0.20),
                     (math.radians(90), 0, 0), M("Marker_White"), self.c[s])
            self.own(t, s)

    # ------------------------------------------------------------------
    def equipment(self):
        # Section 1: LV switchgear lineup (re-uses the Module 1 bay mesh)
        W = 0.762
        self.swg_x = []
        y0 = DEP - 0.10 - 1.524
        for i in range(6):
            x = 0.45 + i * W
            ob = instance_mesh(self.bay, f"EH_S1_SWG_Bay{i+1}", self.c[1], loc=(x, y0, ZF))
            self.own(ob, 1)
            self.swg_x.append(x)
        self.swg_top = ZF + 2.298
        # dry-type transformer (factory-wired within section 1)
        mb = MB()
        mb.box_mm(5.20, 5.80, 2.90, 3.45, ZF, ZF + 1.40, M("Paint_ANSI61"))
        for k in range(6):
            mb.box_mm(5.25 + k * 0.09, 5.29 + k * 0.09, 2.895, 2.90, ZF + 0.25, ZF + 1.15, M("Paint_Dark"))
        gland_plate(mb, 5.30, 5.70, 2.98, 3.38, ZF + 1.40, [])
        self.own(mb.obj("EH_S1_DryTypeTransformer", self.c[1], bevel=0.003), 1)
        # Section 2: MCC / control lineup
        self.mcc_x = []
        for i in range(5):
            x0 = 6.55 + i * 0.82
            ob = cabinet(f"EH_S2_MCC_{i+1}", self.c[2], x0, x0 + 0.80, 2.85, 3.50, ZF + 2.2,
                         None, doors=4)
            ob.location = (0, 0, 0)
            # cabinet() builds z from 0 -- lift to finished floor
            for v in ob.data.vertices:
                v.co.z += ZF
            self.own(ob, 2)
            self.mcc_x.append(x0)
        self.mcc_top = ZF + 2.2 + 0.012
        # control / PLC panel and UPS in section 2
        cp = MB()
        cp.box_mm(10.75, 11.55, 2.95, 3.50, ZF, ZF + 2.1, M("Paint_ANSI61"))
        cp.box_mm(10.80, 11.50, 2.945, 2.95, ZF + 1.2, ZF + 1.6, M("Glass_Dark"))
        self.own(cp.obj("EH_S2_ControlPanel", self.c[2], bevel=0.003), 2)
        # floor cable-entry gland plates under switchgear (bottom entry)
        g = MB()
        for x in self.swg_x[:2]:
            g.box_mm(x + 0.15, x + 0.60, 0.9, 1.8, ZF - 0.01, ZF + 0.004, M("Steel_Galv"))
        self.own(g.obj("EH_S1_FloorEntries", self.c[1]), 1)

    # ------------------------------------------------------------------
    def trays(self):
        for s, (x0, x1) in ((1, (0.35, SPLIT - 0.03)), (2, (SPLIT + 0.03, LEN - 0.35))):
            mb = MB()
            ladder_x(mb, x0, x1, TY0, TY1, RUNG)
            # wall brackets to the back wall
            x = x0 + 0.4
            while x < x1:
                mb.box_mm(x - 0.02, x + 0.02, TY0 - 0.05, DEP - 0.08, RUNG - 0.06, RUNG - 0.02, M("Steel_Galv"))
                mb.box_mm(x - 0.02, x + 0.02, DEP - 0.12, DEP - 0.08, RUNG - 0.30, RUNG - 0.02, M("Steel_Galv"))
                x += 1.5
            # control-cable channel (separated) beside the ladder
            mb.box_mm(x0, x1, TY0 - 0.16, TY0 - 0.04, RUNG - 0.02, RUNG, M("Aluminium"))
            mb.box_mm(x0, x1, TY0 - 0.16, TY0 - 0.155, RUNG, RUNG + 0.05, M("Aluminium"))
            ob = mb.obj(f"TRAY_EH_S{s}", self.c_tr)
            self.own(ob, s)
        # splice plates (field interface) at the split
        sp = MB()
        for y in (TY0 - 0.01, TY1 + 0.002):
            sp.box_mm(SPLIT - 0.12, SPLIT + 0.12, y, y + 0.008, RUNG - 0.01, RUNG + 0.06, M("Steel_Galv"))
        ob = sp.obj("TRAY_EH_SplitSpliceKit", self.c_tr)
        self.own(ob)
        tag_explode(ob, (0.0, -1.75, -3.05))      # staged with the cable package when exploded

    # ------------------------------------------------------------------
    def _run(self, a, b, lane, rz=RUNG, r=0.0135):
        """Equipment top a -> up into tray lane -> along -> down into equipment top b."""
        zc = rz + r
        y = TY0 + 0.04 + lane * 0.034
        return [a + Vector((0, 0, -0.25)), a, Vector((a.x, a.y, zc - 0.25)), Vector((a.x + (0.25 if b.x > a.x else -0.25), y, zc)),
                Vector((b.x - (0.25 if b.x > a.x else -0.25), y, zc)), Vector((b.x, b.y, zc - 0.25)), b, b + Vector((0, 0, -0.25))]

    def cables(self):
        W = 0.762
        top = self.swg_top
        # factory: section 1 switchgear bay 6 -> dry-type transformer
        for k in range(4):
            a = Vector((self.swg_x[5] + 0.25 + k * 0.06, 2.95, top))
            b = Vector((5.36 + k * 0.09, 3.18, ZF + 1.41))
            ob = curve_obj(f"PC_EH_S1_Xfmr_{k+1}", [self._run(a, b, k)], 0.0135, M("Jacket_Power"), self.c_fac, fr=0.15)
            self.own(ob, 1)
        # factory: section 2 MCC -> control panel
        for k in range(3):
            a = Vector((self.mcc_x[4] + 0.2 + k * 0.1, 3.15, self.mcc_top))
            b = Vector((10.90 + k * 0.12, 3.2, ZF + 2.1))
            ob = curve_obj(f"PC_EH_S2_Ctl_{k+1}", [self._run(a, b, 4 + k)], 0.0135, M("Jacket_Power"), self.c_fac, fr=0.15)
            self.own(ob, 2)
        # field-completed: switchgear feeders (bays 3, 4) -> MCC incoming (crosses the split)
        for k in range(6):
            a = Vector((self.swg_x[2 + k // 3] + 0.25 + (k % 3) * 0.12, 2.95, top))
            b = Vector((self.mcc_x[0] + 0.15 + k * 0.10, 3.15, self.mcc_top))
            self.own(curve_obj(f"PC_EH_Field_Feeder_{k+1}", [self._run(a, b, 7 + k)], 0.0135,
                               M("Highlight_Field"), self.c_fld, fr=0.15))
        # field-completed control interconnect (in the separate channel)
        sp = []
        for k in range(4):
            a = Vector((self.swg_x[1] + 0.3 + k * 0.04, 2.62, top))
            b = Vector((11.0 + k * 0.05, 3.05, ZF + 2.1))
            y = TY0 - 0.13 + k * 0.022
            zc = RUNG + 0.008
            sp.append([a + Vector((0, 0, -0.2)), a, Vector((a.x, y, zc - 0.15)), Vector((a.x + 0.15, y, zc)),
                       Vector((10.6, y, zc)), Vector((b.x, b.y, zc - 0.25)), b, b + Vector((0, 0, -0.2))])
        self.own(curve_obj("CW_EH_Field_ControlInterconnect", sp, 0.006, M("Highlight_Field"), self.c_fld, fr=0.12))
        # external (site) incoming cables: end-wall transit -> tray -> switchgear bay 1
        mb = MB()
        tx = LEN
        mb.box_mm(tx, tx + 0.06, 1.0, 2.2, 2.55, 3.15, M("Steel_Dark"))          # multi-cable transit frame
        for k in range(8):
            mb.cyl(0.022, 0.065, (tx + 0.03, 1.12 + (k % 4) * 0.12, 2.70 + (k // 4) * 0.3), M("Rubber"), axis="X")
        self.own(mb.obj("EH_S2_CableTransit", self.c[2], bevel=0.003), 2)
        lat = MB()
        from mod_plant import ladder_y
        ladder_y(lat, 1.0, TY0 + 0.02, 11.10, 11.52, RUNG)
        for yb in (1.3, 2.2):
            lat.box_mm(11.10, LEN - 0.08, yb - 0.02, yb + 0.02, RUNG - 0.06, RUNG - 0.02, M("Steel_Galv"))
        self.own(lat.obj("TRAY_EH_S2_EntryLateral", self.c_tr), 2)
        for k in range(8):
            ye, ze = 1.12 + (k % 4) * 0.12, 2.70 + (k // 4) * 0.3
            yl = TY0 + 0.04 + k * 0.034
            zc = RUNG + 0.0135
            xl = 11.16 + k * 0.042
            a = Vector((self.swg_x[0] + 0.2 + (k % 4) * 0.1, 2.95 if k < 4 else 3.05, top))
            pts = [Vector((tx + 0.75, ye, -0.10)), Vector((tx + 0.75, ye, 0.25)), Vector((tx + 0.75, ye, ze - 0.4)),
                   Vector((tx + 0.40, ye, ze)), Vector((tx + 0.03, ye, ze)), Vector((tx - 0.15, ye, ze)),
                   Vector((xl + 0.15, ye, zc)), Vector((xl, ye + 0.15, zc)), Vector((xl, TY0 - 0.25, zc)),
                   Vector((xl - 0.06, yl, zc + 0.06)), Vector((xl - 0.5, yl, zc + 0.06)),
                   Vector((a.x + 0.25, yl, zc + 0.06)), Vector((a.x, a.y, zc - 0.20)), a, a + Vector((0, 0, -0.25))]
            self.own(curve_obj(f"PC_EH_External_In_{k+1}", [pts], 0.0135, M("Highlight_Field"), self.c_ext, fr=0.16))
        # conduit stub-ups at grade for the external cables
        cs = MB()
        for k in range(4):
            cs.cyl(0.035, 0.30, (tx + 0.75, 1.12 + k * 0.12, 0.10), M("Insulator_Gray"))
        self.own(cs.obj("EH_External_ConduitStubs", self.c_ext))

    # ------------------------------------------------------------------
    def grounding(self):
        for s, (x0, x1) in ((1, (0.0, SPLIT)), (2, (SPLIT, LEN))):
            g = MB()
            for x in (x0 + 0.5, x1 - 0.7):
                g.box_mm(x, x + 0.2, -0.008, 0.0, 0.10, 0.28, M("Copper_Tinned"))
            g.box_mm(x0 + 0.3, x1 - 0.3, DEP - 0.09, DEP - 0.084, ZF + 0.15, ZF + 0.20, M("Copper"))   # interior ground bus
            self.own(g.obj(f"GND_EH_S{s}_Pads_and_Bus", self.c_gnd), s)
        for i, x in enumerate((0.6, SPLIT - 0.6, SPLIT + 0.6, LEN - 0.6)):
            self.own(wire(f"GND_EH_GEC_{i+1}", [Vector((x, -0.01, 0.18)), Vector((x, -0.12, 0.10)),
                                                  Vector((x, -0.14, -0.05))], 0.006, M("Wire_Ground"), self.c_gnd, fr=0.05),
                     1 if x < SPLIT else 2)
        # field bonding jumper across the shipping split (ground bus continuity)
        b = [Vector((SPLIT - 0.25, DEP - 0.10, ZF + 0.175)), Vector((SPLIT - 0.1, DEP - 0.16, ZF + 0.12)),
             Vector((SPLIT + 0.1, DEP - 0.16, ZF + 0.12)), Vector((SPLIT + 0.25, DEP - 0.10, ZF + 0.175))]
        self.own(curve_obj("GND_EH_Split_BondingJumper", [b], 0.006, M("Wire_Ground"), coll("Grounding/GND_EH_FieldBond"), fr=0.08))

    # ------------------------------------------------------------------
    def field_package(self):
        """Interconnect cable package staged for the exploded view (pallet + coils)."""
        mb = MB()
        x0, y0 = SPLIT - 0.55, 0.9
        for k in range(5):
            mb.box_mm(x0, x0 + 1.1, y0 + k * 0.22, y0 + k * 0.22 + 0.09, 0.11, 0.13, M("Wood_Reel"))
        for k in range(3):
            mb.box_mm(x0 + k * 0.5, x0 + k * 0.5 + 0.09, y0, y0 + 0.97, 0.0, 0.11, M("Wood_Reel"))
        mb.box_mm(x0 + 0.1, x0 + 1.0, y0 - 0.004, y0, 0.03, 0.10, M("Marker_White"))
        self.own(mb.obj("EH_FieldPackage_Pallet", self.c_pkg, bevel=0.002))
        coils, lugs = [], MB()
        for i in range(6):
            cx, cy = x0 + 0.28 + (i % 2) * 0.54, y0 + 0.2 + (i // 2) * 0.29
            pts = []
            for k in range(40):
                a = 2 * math.pi * k / 18
                rr = 0.16 - 0.004 * (k // 18)
                pts.append(Vector((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.7, 0.15 + 0.0028 * k)))
            coils.append(pts)
            lug(lugs, pts[-1], (pts[-1] - pts[-2]), 0.012)
        self.own(curve_obj("EH_FieldPackage_FeederCoils", coils, 0.0135, M("Highlight_Field"), self.c_pkg, fr=0.0))
        self.own(lugs.obj("EH_FieldPackage_Lugs", self.c_pkg))
        self.own(text("EH_FieldPackage_Label", "INTERCONNECT CABLE PACKAGE", 0.045, (x0 + 0.55, y0 - 0.005, 0.065),
                      (math.radians(90), 0, 0), M("Label_Ink"), self.c_pkg))

    def staging(self):
        """Staged deliveries for the coordinated-supply view: reels + kit crates."""
        def reel(name, x, y, r=0.55, w=0.6, label=None):
            mb = MB()
            for s in (-1, 1):
                mb.cyl(r, 0.04, (x, y + s * w / 2, r), M("Wood_Reel"), axis="Y", segs=40)
            mb.cyl(r * 0.82, w - 0.04, (x, y, r), M("Jacket_Power"), axis="Y", segs=40)
            for k in range(8):
                a = 2 * math.pi * k / 8
                mb.box((0.06, w + 0.06, 0.06), (x + (r + 0.02) * math.cos(a), y, r + (r + 0.02) * math.sin(a)),
                       M("Wood_Reel"), rot=(0, -a, 0))
            mb.box_mm(x - 0.16, x + 0.16, y - w / 2 - 0.025, y - w / 2 - 0.02, r - 0.1, r + 0.1, M("Marker_White"))
            self.own(mb.obj(name, self.c_stage, bevel=0.0))
            if label:
                self.own(text(name + "_Label", label, 0.05, (x, y - w / 2 - 0.0255, r), (math.radians(90), 0, 0),
                              M("Label_Ink"), self.c_stage))
        reel("STG_Reel_1", 1.0, -2.2, label="REEL 1")
        reel("STG_Reel_2", 2.5, -2.2, label="REEL 2")
        reel("STG_Reel_3", 4.0, -2.4, r=0.45, w=0.5, label="REEL 3")
        for i, (x, lab) in enumerate(((7.0, "DELIVERY 1"), (8.6, "DELIVERY 2"), (10.2, "DELIVERY 3"))):
            mb = MB()
            for k in range(5):
                mb.box_mm(x, x + 1.2, -2.8 + k * 0.2, -2.8 + k * 0.2 + 0.09, 0.11, 0.13, M("Wood_Reel"))
            for k in range(3):
                mb.box_mm(x + k * 0.555, x + k * 0.555 + 0.09, -2.8, -1.89, 0.0, 0.11, M("Wood_Reel"))
            hgt = 0.55 - i * 0.1
            mb.box_mm(x + 0.05, x + 1.15, -2.75, -1.95, 0.13, 0.13 + hgt, M("Cardboard"))
            mb.box_mm(x + 0.25, x + 0.95, -2.755, -2.75, 0.13 + hgt * 0.35, 0.13 + hgt * 0.8, M("Marker_White"))
            mb.box_mm(x + 0.25, x + 0.95, -2.756, -2.755, 0.13 + hgt * 0.68, 0.13 + hgt * 0.8, M("Wire_Control"))
            self.own(mb.obj(f"STG_Delivery_{i+1}", self.c_stage, bevel=0.003))
            self.own(text(f"STG_Delivery_{i+1}_Label", lab, 0.06, (x + 0.6, -2.757, 0.13 + hgt * 0.5),
                          (math.radians(90), 0, 0), M("Label_Ink"), self.c_stage))

    def boundaries(self):
        b = MB()
        b.box_mm(SPLIT - 0.003, SPLIT + 0.003, 0.05, DEP - 0.05, ZF, ZW - 0.05, M("Boundary_Field"))
        self.own(b.obj("ANN_EH_ShippingSplit_Plane", self.c_ann))
