"""Module 5 -- Temporary power and testing (Configuration D).

Temporary (trailer) generator -> portable single-conductor cable set ->
generator docking station (generator-input port) ; docking station load-bank
port -> second portable cable set -> load bank (configurable test load).
The facility feed from the docking station leaves through conduits below the
pad and is shown only as an interface (no permanent loads are connected to
the test arrangement).

Local frame: x along the arrangement, front (camera) side = -y.
Cam-lock connector body colours follow common single-pole connector practice
(phase / neutral / ground) and are equipment colours, not presentation colours.
"""
import math
from mathutils import Vector
import bpy
from swlib import MB, M, coll, curve_obj, bezier_cable, text, tag_panel, cyl_between, lug

CAM_COLS = ["Cam_Black", "Cam_Red", "Cam_Blue", "Cam_White", "Cam_Green"]
CAM_TAG = ["A", "B", "C", "N", "G"]
R_CAB = 0.016


def receptacle(mb, p, normal=(0, -1, 0), col="Cam_Black"):
    n = Vector(normal)
    cyl_between(mb, p - n * 0.05, p, 0.034, M(col), segs=20)
    cyl_between(mb, p, p + n * 0.006, 0.026, M("Steel_Dark"), segs=16)


def plug(mb, p, d, col):
    """Plug body mated to a receptacle face at p, cable leaves along d."""
    d = Vector(d).normalized()
    cyl_between(mb, p, p + d * 0.11, 0.032, M(col), segs=20)
    cyl_between(mb, p + d * 0.11, p + d * 0.17, 0.026, M("Rubber"), segs=16)
    return p + d * 0.165


class TempPower:
    def __init__(self, root_loc):
        self.root = bpy.data.objects.new("TMP_Root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.location = root_loc
        coll("Temporary_Power").objects.link(self.root)
        self.c_gen = coll("Temporary_Power/TMP_Generator")
        self.c_dock = coll("Temporary_Power/TMP_DockingStation")
        self.c_lb = coll("Temporary_Power/TMP_LoadBank")
        self.c_store = coll("Temporary_Power/TMP_CableStorage")
        self.c_pan = coll("Temporary_Power/TMP_Panels")
        self.c_genset = coll("Power_Cables/PC_TMP_GenLeads")
        self.c_lbset = coll("Power_Cables/PC_TMP_LoadBankLeads")
        self.c_int = coll("Power_Cables/PC_TMP_DockInternal")
        self.c_cw = coll("Control_Wiring/CW_TMP")
        self.c_gnd = coll("Grounding/GND_TMP")
        self.c_ann = coll("Annotations/ANN_TMP_Boundaries")
        self.objs = []

    def own(self, ob):
        ob.parent = self.root
        self.objs.append(ob)
        return ob

    def world(self, p):
        return self.root.location + Vector(p)

    def build(self):
        self.generator()
        self.dock()
        self.loadbank()
        self.leads()
        self.storage()
        return self

    # ------------------------------------------------------------------
    def generator(self):
        mb = MB()
        enc, base = M("Paint_Enclosure"), M("Paint_Base")
        x0, x1, y0, y1 = 0.0, 4.2, -0.8, 0.8
        zb = 0.62
        # trailer chassis, tandem axle, tongue, jacks
        mb.box_mm(x0 + 0.1, x1 - 0.1, -0.55, -0.45, zb - 0.18, zb, M("Steel_Dark"))
        mb.box_mm(x0 + 0.1, x1 - 0.1, 0.45, 0.55, zb - 0.18, zb, M("Steel_Dark"))
        for xa in (1.75, 2.55):
            for s in (-1, 1):
                mb.cyl(0.38, 0.22, (xa, s * 0.92, 0.38), M("Rubber"), axis="Y", segs=32)
                mb.cyl(0.20, 0.23, (xa, s * 0.92, 0.38), M("Steel_Galv"), axis="Y", segs=24)
                mb.box_mm(xa - 0.45, xa + 0.45, s * 0.92 - 0.14, s * 0.92 + 0.14, 0.80, 0.83, base)   # fender
        cyl_between(mb, (0.1, -0.5, zb - 0.1), (-1.0, 0, 0.45), 0.04, M("Steel_Dark"))
        cyl_between(mb, (0.1, 0.5, zb - 0.1), (-1.0, 0, 0.45), 0.04, M("Steel_Dark"))
        mb.cyl(0.05, 0.06, (-1.05, 0, 0.45), M("Steel_Dark"))
        mb.cyl(0.03, 0.45, (-0.6, 0, 0.22), M("Steel_Galv"))
        # enclosure
        mb.box_mm(x0, x1, y0, y1, zb, zb + 1.95, enc)
        mb.box_mm(x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, zb + 1.95, zb + 2.0, enc)
        for k in range(3):                                         # access door seams
            xx = 0.3 + k * 1.2
            mb.box_mm(xx, xx + 1.1, y0 - 0.006, y0, zb + 0.15, zb + 1.8, M("Paint_ANSI61"))
            mb.box_mm(xx + 0.95, xx + 1.0, y0 - 0.03, y0 - 0.006, zb + 0.9, zb + 1.05, M("Plastic_Black"))
        for k in range(10):
            mb.box_mm(-0.02, 0.0, y0 + 0.2, y1 - 0.2, zb + 0.4 + k * 0.12, zb + 0.46 + k * 0.12, M("Paint_Dark"))
        mb.cyl(0.08, 0.35, (1.0, 0.3, zb + 2.15), M("Steel_Dark"))
        # output connection panel recess (front, alternator end)
        px0, px1, pz0, pz1 = 3.70, 4.15, zb + 0.18, zb + 1.10
        mb.box_mm(px0, px1, y0 - 0.004, y0 + 0.002, pz0, pz1, M("Paint_Dark"))
        self.gen_recep = []
        for i in range(5):
            p = Vector((px0 + 0.07 + i * 0.077, y0 - 0.006, pz0 + 0.30))
            receptacle(mb, p, col=CAM_COLS[i])
            self.gen_recep.append(p)
        mb.box_mm(px0 + 0.05, px1 - 0.05, y0 - 0.008, y0 - 0.004, pz0 + 0.55, pz0 + 0.80, M("Steel_Galv"))  # lug box cover
        mb.box_mm(px0 + 0.03, px1 - 0.03, y0 - 0.008, y0 - 0.004, pz0 + 0.05, pz0 + 0.12, M("Marker_White"))
        # ground stud + ground rod
        mb.box_mm(4.05, 4.15, y0 - 0.02, y0, zb - 0.12, zb - 0.02, M("Copper_Tinned"))
        self.own(mb.obj("TMP_TrailerGenerator", self.c_gen, bevel=0.004))
        g = [Vector((4.10, y0 - 0.03, zb - 0.07)), Vector((4.10, y0 - 0.15, 0.30)), Vector((4.25, -1.05, 0.02)),
             Vector((4.45, -1.05, 0.02))]
        self.own(bezier_cable("GND_TMP_GenToRod", g, 0.005, M("Wire_Ground"), self.c_gnd))
        rod = MB()
        rod.cyl(0.008, 0.12, (4.5, -1.05, 0.06), M("Copper"))
        rod.cyl(0.02, 0.025, (4.5, -1.05, 0.04), M("Brass"))
        self.own(rod.obj("GND_TMP_GroundRod", self.c_gnd))

    # ------------------------------------------------------------------
    def dock(self):
        mb = MB()
        X0, X1, Y0, Y1, H = 7.0, 8.3, -0.30, 0.25, 2.0
        self.dock_box = (X0, X1, Y0, Y1, H)
        mb.box_mm(X0 - 0.3, X1 + 0.3, Y0 - 0.5, Y1 + 0.3, 0.0, 0.12, M("Concrete"))           # pad
        mb.shell(X0, X1, Y0, Y1, 0.12, H, 0.003, M("Paint_ANSI61"), open=("-y",))
        mb.box_mm(X0 - 0.02, X1 + 0.02, Y0 - 0.06, Y1 + 0.02, H, H + 0.02, M("Paint_ANSI61"))   # rain hood
        mb.box_mm(X0 + 0.02, X1 - 0.02, Y1 - 0.02, Y1 - 0.017, 0.16, H - 0.04, M("Backplate_White"))
        # recessed receptacle panel (generator input upper, load-bank port lower)
        mb.box_mm(X0 + 0.04, X0 + 0.62, Y0 + 0.08, Y0 + 0.085, 0.30, 1.50, M("Paint_Dark"))
        self.dock_gen_in, self.dock_lb_out = [], []
        for i in range(5):
            p = Vector((X0 + 0.10 + i * 0.11, Y0 + 0.075, 1.20))
            receptacle(mb, p, col=CAM_COLS[i])
            self.dock_gen_in.append(p)
            q = Vector((X0 + 0.10 + i * 0.11, Y0 + 0.075, 0.55))
            receptacle(mb, q, col=CAM_COLS[i])
            self.dock_lb_out.append(q)
        for z, lab in ((1.38, "GENERATOR INPUT"), (0.73, "LOAD BANK")):
            mb.box_mm(X0 + 0.09, X0 + 0.57, Y0 + 0.076, Y0 + 0.08, z - 0.03, z + 0.03, M("Marker_White"))
        # internal bus + disconnect + facility lugs
        for i in range(4):
            xb = X0 + 0.78 + i * 0.11
            mb.box_mm(xb - 0.02, xb + 0.02, Y1 - 0.10, Y1 - 0.094, 0.40, 1.30, M("Copper"))
            mb.box_mm(xb - 0.03, xb + 0.03, Y1 - 0.094, Y1 - 0.02, 0.45, 0.50, M("Insulator_Gray"))
            mb.box_mm(xb - 0.03, xb + 0.03, Y1 - 0.094, Y1 - 0.02, 1.20, 1.25, M("Insulator_Gray"))
        mb.box_mm(X0 + 0.74, X1 - 0.05, Y1 - 0.20, Y1 - 0.10, 1.40, 1.75, M("Plastic_Device"))   # facility disconnect
        mb.box_mm(X0 + 0.95, X0 + 1.05, Y1 - 0.24, Y1 - 0.20, 1.50, 1.65, M("Pilot_Red"))
        mb.box_mm(X0 + 0.04, X0 + 0.62, Y1 - 0.06, Y1 - 0.02, 1.62, 1.90, M("Plastic_Device"))  # phase-rotation / metering
        self.own(mb.obj("TMP_DockingStation", self.c_dock, bevel=0.002))
        door = MB()
        door.box_mm(X0, X1, Y0 - 0.025, Y0, 0.13, H - 0.01, M("Paint_ANSI61"))
        dob = door.obj("TMP_DockingStation_Door", self.c_pan, bevel=0.002)
        tag_panel(dob, explode=(0, -1.0, 0))
        self.own(dob)
        for z, lab in ((1.38, "GENERATOR INPUT"), (0.73, "LOAD BANK")):
            self.own(text(f"TMP_Dock_Label_{lab.split()[0]}", lab, 0.032, (X0 + 0.33, Y0 + 0.0755, z),
                          (math.radians(90), 0, 0), M("Label_Ink"), self.c_dock))
        # internal prepared connections: receptacle backs -> bus (power assemblies)
        sp_g, sp_l = [], []
        lugs = MB()
        for i in range(4):
            xb = X0 + 0.78 + i * 0.11
            a = self.dock_gen_in[i] + Vector((0, 0.06, 0))
            b = Vector((xb, Y1 - 0.12, 1.05 - i * 0.04))
            sp_g.append([a, a + Vector((0, 0.05, 0)), Vector((a.x, Y1 - 0.14, a.z - 0.06)), Vector((xb - 0.06, Y1 - 0.14, b.z)), b])
            lug(lugs, b, Vector((1, 0, 0)) * 0 + Vector((0.0, 1.0, 0.0)), 0.011, tongue=(0.02, 0.005, 0.02))
            a2 = self.dock_lb_out[i] + Vector((0, 0.06, 0))
            b2 = Vector((xb, Y1 - 0.12, 0.70 - i * 0.04))
            sp_l.append([a2, a2 + Vector((0, 0.05, 0)), Vector((a2.x, Y1 - 0.14, a2.z + 0.04)), Vector((xb - 0.06, Y1 - 0.14, b2.z)), b2])
            lug(lugs, b2, Vector((0.0, 1.0, 0.0)), 0.011, tongue=(0.02, 0.005, 0.02))
        self.own(curve_obj("PC_TMP_Dock_GenInput_Internal", sp_g, 0.011, M("Jacket_Power"), self.c_int, fr=0.05))
        self.own(curve_obj("PC_TMP_Dock_LoadBank_Internal", sp_l, 0.011, M("Jacket_Power"), self.c_int, fr=0.05))
        # ground receptacles -> ground bar
        gb = Vector((X0 + 0.70, Y1 - 0.05, 0.25))
        lugs.box_mm(X0 + 0.05, X1 - 0.05, Y1 - 0.06, Y1 - 0.04, 0.22, 0.27, M("Copper_Tinned"))
        self.own(lugs.obj("PC_TMP_Dock_Internal_Lugs_GroundBar", self.c_int))
        gnd = []
        for p in (self.dock_gen_in[4], self.dock_lb_out[4]):
            a = p + Vector((0, 0.06, 0))
            gnd.append([a, a + Vector((0, 0.04, 0)), Vector((a.x + 0.05, Y1 - 0.08, 0.40)), Vector((a.x + 0.05, Y1 - 0.06, 0.28))])
        self.own(curve_obj("GND_TMP_Dock_Internal", gnd, 0.007, M("Wire_Ground"), self.c_gnd, fr=0.05))
        # facility feed (permanent wiring interface): disconnect -> conduits below the pad
        fac = []
        cond = MB()
        for i in range(4):
            xb = X0 + 0.80 + i * 0.10
            a = Vector((xb, Y1 - 0.15, 1.40))
            fac.append([a, Vector((xb, Y1 - 0.16, 1.30)), Vector((xb + 0.02, Y1 - 0.22, 1.0)),
                        Vector((xb + 0.02, Y1 - 0.22, 0.20)), Vector((xb + 0.02, Y1 - 0.22, -0.10))])
            cond.cyl(0.026, 0.06, (xb + 0.02, Y1 - 0.22, 0.15), M("Insulator_Gray"))
        self.own(curve_obj("PC_TMP_Dock_FacilityFeed", fac, 0.011, M("Jacket_Power"), self.c_int, fr=0.12))
        self.own(cond.obj("PC_TMP_Dock_FacilityConduits", self.c_int))

    # ------------------------------------------------------------------
    def loadbank(self):
        mb = MB()
        X0, X1, Y0, Y1, zb = 10.2, 12.8, -0.65, 0.65, 0.20
        mb.box_mm(X0, X1, Y0, Y1, 0.0, zb, M("Paint_Base"))                     # skid
        mb.box_mm(X0 + 0.02, X1 - 0.02, Y0 + 0.02, Y1 - 0.02, zb, 1.95, M("Paint_Enclosure"))
        # discharge grille (top), intake louvres (sides)
        for k in range(14):
            x = X0 + 0.9 + k * 0.11
            mb.box_mm(x, x + 0.05, Y0 + 0.12, Y1 - 0.12, 1.95, 1.99, M("Paint_Dark"))
        for k in range(8):
            z = 0.6 + k * 0.13
            mb.box_mm(X0 + 1.0, X1 - 0.2, Y0, Y0 + 0.02, z, z + 0.06, M("Paint_Dark"))
        # connection panel (front, left end) with cam-lock receptacles and lug cover
        mb.box_mm(X0 + 0.10, X0 + 0.80, Y0 - 0.006, Y0 + 0.02, 0.35, 1.30, M("Paint_ANSI61"))
        self.lb_recep = []
        for i in range(5):
            p = Vector((X0 + 0.18 + i * 0.13, Y0 - 0.008, 0.60))
            receptacle(mb, p, col=CAM_COLS[i])
            self.lb_recep.append(p)
        mb.box_mm(X0 + 0.15, X0 + 0.75, Y0 - 0.01, Y0 - 0.006, 0.82, 1.20, M("Steel_Galv"))
        # control panel (configurable load steps) -- simplified, no readable values
        mb.box_mm(X0 + 0.95, X0 + 1.55, Y0 - 0.01, Y0 + 0.02, 1.05, 1.55, M("Paint_ANSI61"))
        for r in range(2):
            for k in range(5):
                mb.cyl(0.018, 0.02, (X0 + 1.03 + k * 0.11, Y0 - 0.015, 1.20 + r * 0.16), M("Plastic_Black"), axis="Y")
        mb.box_mm(X0 + 1.03, X0 + 1.47, Y0 - 0.014, Y0 - 0.01, 1.43, 1.50, M("Glass_Dark"))
        self.own(mb.obj("TMP_LoadBank", self.c_lb, bevel=0.004))

    # ------------------------------------------------------------------
    def _lead(self, a, b, lane_y, i, name, coll_):
        """Portable single-conductor lead: plug at a (receptacle face, out -y),
        lies on grade along lane_y, rises to plug at b."""
        mb = MB()
        ca = plug(mb, a, (0, -1, 0), CAM_COLS[i])
        cb = plug(mb, b, (0, -1, 0), CAM_COLS[i])
        r = R_CAB
        pts = [ca, ca + Vector((0, -0.12, -0.02)), Vector((ca.x, lane_y + 0.30, r + 0.02)),
               Vector((ca.x + 0.35, lane_y, r)), Vector((cb.x - 0.35, lane_y, r)),
               Vector((cb.x, lane_y + 0.30, r + 0.02)), cb + Vector((0, -0.12, -0.02)), cb]
        self.own(curve_obj(name, [pts], r, M("Jacket_Portable"), coll_, fr=0.25, seg=8))
        # identification sleeves near both ends (colour = connector colour)
        for c, d in ((ca, -1), (cb, -1)):
            mb.cyl(r + 0.003, 0.05, tuple(c + Vector((0, -0.05, 0))), M(CAM_COLS[i]), axis="Y")
        self.own(mb.obj(name + "_Plugs", coll_))

    def leads(self):
        for i in range(5):
            self._lead(self.gen_recep[i], self.dock_gen_in[i] + Vector((0, -0.006, 0)), -1.25 - i * 0.07, i,
                       f"PC_TMP_GenLead_{CAM_TAG[i]}", self.c_genset)
            self._lead(self.dock_lb_out[i] + Vector((0, -0.006, 0)), self.lb_recep[i], -0.85 - (4 - i) * 0.07, i,
                       f"PC_TMP_LoadBankLead_{CAM_TAG[i]}", self.c_lbset)

    # ------------------------------------------------------------------
    def storage(self):
        """Cable storage / transport cart with coiled spare lead sets."""
        mb = MB()
        x0, x1, y0, y1 = 4.8, 6.2, 1.3, 2.1
        mb.box_mm(x0, x1, y0, y1, 0.12, 0.16, M("Paint_Dark"))
        for (x, y) in ((x0, y0), (x1 - 0.04, y0), (x0, y1 - 0.04), (x1 - 0.04, y1 - 0.04)):
            mb.box_mm(x, x + 0.04, y, y + 0.04, 0.16, 1.3, M("Paint_Dark"))
            mb.cyl(0.06, 0.04, (x + 0.02, y + 0.02, 0.06), M("Rubber"), axis="X")
        mb.box_mm(x0, x1, y1 - 0.04, y1, 1.26, 1.30, M("Paint_Dark"))
        mb.box_mm(x0, x1, y0, y0 + 0.04, 1.26, 1.30, M("Paint_Dark"))
        mb.box_mm(x0 + 0.2, x1 - 0.2, y0 - 0.004, y0, 0.25, 0.40, M("Marker_White"))
        self.own(mb.obj("TMP_CableCart", self.c_store, bevel=0.003))
        coils = []
        plugs = MB()
        for i in range(5):
            cx = x0 + 0.17 + i * 0.265
            for t in range(3):
                pts = []
                for k in range(19):
                    a = 2 * math.pi * k / 18
                    pts.append(Vector((cx + 0.11 * math.cos(a) * 0.35, (y0 + y1) / 2 + 0.28 * math.cos(a) * 0.2 + (t - 1) * 0.05,
                                       0.75 + 0.42 * math.sin(a))))
                coils.append(pts)
            plugs.cyl(0.032, 0.11, (cx, y0 + 0.02, 0.36), M(CAM_COLS[i]), axis="Z")
        self.own(curve_obj("TMP_StoredLeadSets", coils, R_CAB, M("Jacket_Portable"), self.c_store, fr=0.0))
        self.own(plugs.obj("TMP_StoredLeadSets_Plugs", self.c_store))
        # hanging bar
        bar = MB()
        bar.cyl(0.02, x1 - x0, ((x0 + x1) / 2, (y0 + y1) / 2, 1.18), M("Steel_Galv"), axis="X")
        self.own(bar.obj("TMP_CableCart_Bar", self.c_store))
        self.own(text("TMP_CableCart_Label", "LEAD SET STORAGE", 0.05, ((x0 + x1) / 2, y0 - 0.005, 0.325),
                      (math.radians(90), 0, 0), M("Label_Ink"), self.c_store))

