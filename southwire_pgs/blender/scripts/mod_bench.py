"""Module 6 -- Cable-assembly workbench: isolated exploded view of one
representative single-conductor power-lead assembly.

Sequence (left -> right along the exploded axis):
  1 cable   2 prepared end   3 identification sleeve   4 compression lug
  5 accessory (support cleat)   6 finished assembly   7 packaging
  8 generic inspection / test-record card (blank fields, no results)
"""
import math
from mathutils import Vector
import bpy
from swlib import MB, M, coll, curve_obj, wire, bezier_cable, text, cyl_between, lug

ZT = 0.90              # bench top
AXZ = 1.00             # exploded axis height
R = 0.0125             # cable radius (representative)


class Bench:
    def __init__(self, root_loc):
        self.root = bpy.data.objects.new("ASM_Root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.location = root_loc
        coll("Assembly_Kit").objects.link(self.root)
        self.c = coll("Assembly_Kit/ASM_Exploded")
        self.c_b = coll("Assembly_Kit/ASM_Bench")
        self.c_ann = coll("Annotations/ANN_ASM")
        self.objs = []
        self.anchor = {}

    def own(self, ob):
        ob.parent = self.root
        self.objs.append(ob)
        return ob

    def world(self, p):
        return self.root.location + Vector(p)

    def build(self):
        self.bench()
        self.exploded()
        self.finished_and_packaging()
        return self

    def bench(self):
        mb = MB()
        mb.box_mm(-0.1, 1.9, -0.45, 0.45, ZT - 0.04, ZT - 0.002, M("Paint_ANSI61"))
        mb.box_mm(-0.08, 1.88, -0.43, 0.43, ZT - 0.0025, ZT + 0.0, M("Bench_Mat"))
        for (x, y) in ((-0.05, -0.40), (1.8, -0.40), (-0.05, 0.36), (1.8, 0.36)):
            mb.box_mm(x, x + 0.05, y, y + 0.05, 0.0, ZT - 0.04, M("Paint_Dark"))
        mb.box_mm(-0.05, 1.85, 0.36, 0.41, 0.15, 0.20, M("Paint_Dark"))
        self.own(mb.obj("ASM_Workbench", self.c_b, bevel=0.003))

    def exploded(self):
        y = -0.18
        mb = MB()
        # 1 cable segment with print line (unreadable) along jacket
        c1 = [Vector((0.02, y, AXZ)), Vector((0.30, y, AXZ))]
        self.own(wire("ASM_1_Cable", c1, R, M("Jacket_Power"), self.c))
        mb.box_mm(0.05, 0.28, y - 0.002, y + 0.002, AXZ + R - 0.0004, AXZ + R + 0.0003, M("Marker_White"))
        self.anchor[1] = Vector((0.16, y, AXZ + R))
        # 2 prepared end: insulation cut square, stranded conductor exposed
        self.own(wire("ASM_2_PreparedEnd_Insulation", [Vector((0.40, y, AXZ)), Vector((0.62, y, AXZ))], R,
                      M("Jacket_Power"), self.c))
        strands = MB()
        for k in range(19):
            if k == 0:
                off = Vector((0, 0, 0))
            elif k < 7:
                a = 2 * math.pi * k / 6
                off = Vector((0, math.cos(a), math.sin(a))) * 0.0034
            else:
                a = 2 * math.pi * (k - 7) / 12
                off = Vector((0, math.cos(a), math.sin(a))) * 0.0068
            strands.cyl(0.0018, 0.045, (0.6425, y + off.y, AXZ + off.z), M("Copper"), axis="X", segs=8)
        self.own(strands.obj("ASM_2_PreparedEnd_Strands", self.c))
        self.anchor[2] = Vector((0.645, y, AXZ + 0.008))
        # 3 identification sleeve (heat-shrink marker, blank legend area)
        mb.cyl(R + 0.004, 0.06, (0.76, y, AXZ), M("Marker_White"), axis="X", segs=24)
        mb.cyl(R + 0.0045, 0.012, (0.74, y, AXZ), M("Wire_Control"), axis="X", segs=24)
        self.anchor[3] = Vector((0.76, y, AXZ + R + 0.004))
        # 4 compression lug (two-hole), aligned on the axis
        lug(mb, Vector((0.86, y, AXZ)), Vector((1, 0, 0)), 0.0145, tongue=(0.006, 0.04, 0.07))
        for dx in (0.935, 0.965):
            mb.cyl(0.0055, 0.008, (dx + 0.02, y, AXZ), M("Paint_Dark"), axis="Z", segs=12)
        self.anchor[4] = Vector((0.90, y, AXZ + 0.016))
        # 5 accessory: two-piece support cleat
        cx = 1.12
        mb.box_mm(cx - 0.035, cx + 0.035, y - 0.03, y + 0.03, AXZ - 0.045, AXZ - 0.016, M("Plastic_Black"))
        mb.box_mm(cx - 0.035, cx + 0.035, y - 0.03, y + 0.03, AXZ + 0.030, AXZ + 0.058, M("Plastic_Black"))
        for s in (-1, 1):
            mb.cyl(0.004, 0.13, (cx, y + s * 0.022, AXZ + 0.005), M("Steel_Galv"), segs=8)
        self.anchor[5] = Vector((cx, y, AXZ + 0.058))
        self.own(mb.obj("ASM_3to5_Sleeve_Lug_Cleat", self.c))
        # exploded centre line (annotation)
        ax = MB()
        x = 0.02
        while x < 1.22:
            ax.cyl(0.0012, 0.025, (x + 0.0125, y, AXZ), M("Label_Ink"), axis="X", segs=6)
            x += 0.045
        self.own(ax.obj("ANN_ASM_ExplodedAxis", self.c_ann))
        # step numbers (small plates) under each part
        for k, xx in enumerate((0.16, 0.52, 0.76, 0.92, 1.12)):
            t = text(f"ANN_ASM_Step_{k+1}", str(k + 1), 0.05, (xx, -0.36, ZT + 0.0025), (0, 0, 0),
                     M("Label_Ink"), self.c_ann)
            self.own(t)
            d = MB()
            d.cyl(0.04, 0.002, (xx, -0.36, ZT + 0.0005), M("Marker_White"), segs=32)
            self.own(d.obj(f"ANN_ASM_StepDisc_{k+1}", self.c_ann))

    def finished_and_packaging(self):
        y = -0.12
        # 6 finished assembly: coiled lead, lug + sleeve at both ends
        pts = []
        cx, cy = 0.42, 0.20
        for k in range(46):
            a = 2 * math.pi * k / 22
            rr = 0.17 - 0.012 * (k // 22)
            pts.append(Vector((cx + rr * math.cos(a), cy + rr * math.sin(a), ZT + R + 0.002 + 0.0009 * k)))
        start = [Vector((cx - 0.30, cy - 0.06, ZT + R)), Vector((cx - 0.22, cy - 0.02, ZT + R)), pts[0]]
        endp = [pts[-1], pts[-1] + Vector((0.10, 0.02, 0.004)), Vector((cx + 0.30, cy + 0.10, ZT + R + 0.01))]
        full = start + pts[1:-1] + endp
        self.own(curve_obj("ASM_6_FinishedAssembly", [full], R, M("Jacket_Power"), self.c, fr=0.0))
        mb = MB()
        for e, d in ((full[0], full[0] - full[1]), (full[-1], full[-1] - full[-2])):
            lug(mb, e, d, 0.0145, tongue=(0.04, 0.006, 0.07))
            dn = d.normalized()
            cyl_between(mb, e - dn * 0.085, e - dn * 0.025, R + 0.004, M("Marker_White"), segs=20)
        self.own(mb.obj("ASM_6_FinishedAssembly_Ends", self.c))
        self.anchor[6] = Vector((cx, cy - 0.17, ZT + 0.03))
        # 7 packaging: carton with label + bagged assembly identification
        pk = MB()
        bx0, bx1, by0, by1 = 0.86, 1.30, 0.04, 0.40
        pk.box_mm(bx0, bx1, by0, by1, ZT, ZT + 0.22, M("Cardboard"))
        pk.box_mm(bx0, bx1, by0 - 0.004, by1 + 0.004, ZT + 0.22, ZT + 0.225, M("Cardboard"))
        pk.box_mm(bx0 + 0.1, bx1 - 0.1, by0 - 0.004, by0, ZT + 0.06, ZT + 0.17, M("Marker_White"))
        pk.box_mm(bx0 + 0.1, bx1 - 0.1, by0 - 0.005, by0 - 0.004, ZT + 0.145, ZT + 0.17, M("Wire_Control"))
        for k in range(3):
            pk.box_mm(bx0 + 0.13, bx1 - 0.18 + 0.03 * k, by0 - 0.005, by0 - 0.004, ZT + 0.08 + k * 0.02, ZT + 0.086 + k * 0.02, M("Label_Ink"))
        self.own(pk.obj("ASM_7_Packaging_Carton", self.c, bevel=0.003))
        self.anchor[7] = Vector(((bx0 + bx1) / 2, by0, ZT + 0.20))
        # 8 inspection / test-record card (generic, blank fields)
        cd = MB()
        kx0, kx1, ky0, ky1 = 1.40, 1.72, 0.06, 0.30
        cd.box_mm(kx0, kx1, ky0, ky1, ZT, ZT + 0.0015, M("Paper"))
        cd.box_mm(kx0, kx1, ky1 - 0.035, ky1, ZT + 0.0015, ZT + 0.0018, M("Wire_Control"))
        for r in range(6):
            yy = ky1 - 0.06 - r * 0.025
            cd.box_mm(kx0 + 0.02, kx0 + 0.10, yy, yy + 0.0015, ZT + 0.0016, ZT + 0.0019, M("Label_Ink"))
            cd.box_mm(kx0 + 0.12, kx1 - 0.06, yy, yy + 0.0008, ZT + 0.0016, ZT + 0.0019, M("Paint_Dark"))
            cd.box_mm(kx1 - 0.045, kx1 - 0.025, yy, yy + 0.016, ZT + 0.0016, ZT + 0.0019, M("Paint_Dark"))
            cd.box_mm(kx1 - 0.043, kx1 - 0.027, yy + 0.002, yy + 0.014, ZT + 0.0019, ZT + 0.0021, M("Paper"))
        self.own(cd.obj("ASM_8_InspectionRecordCard", self.c))
        self.own(text("ASM_8_Card_Title", "INSPECTION / TEST RECORD", 0.0125, ((kx0 + kx1) / 2, ky1 - 0.0175, ZT + 0.0021),
                      (0, 0, 0), M("Marker_White"), self.c))
        self.anchor[8] = Vector(((kx0 + kx1) / 2, (ky0 + ky1) / 2, ZT))
