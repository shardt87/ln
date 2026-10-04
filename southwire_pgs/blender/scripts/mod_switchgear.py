"""Module 1 -- LV switchgear lineup with one detailed, open auxiliary/control
section (S3) and a removable prepared control-wire kit displayed beside it.

Local frame of the lineup: x along the lineup (left->right seen from front),
y = depth (front face y=0, rear y=D), z up, floor z=0.
All objects are parented to the root empty 'SWG_LV_Root'.
"""
import math
import random
from mathutils import Vector, Matrix
from swlib import (MB, M, coll, curve_obj, wire, bezier_cable, text, empty,
                   tag_panel, tag_explode, fillet)
import bpy

W, D, H, ZB = 0.762, 1.524, 2.286, 0.08       # section width/depth/height, base channel
NSEC = 3
X3 = 2 * W                                     # detailed section S3 starts here
BP_Y = 0.46                                    # backplate front face (y)
BP_X0, BP_Z0 = X3 + 0.035, 0.20                # backplate origin (u=0, v=0)
BP_W, BP_H = W - 0.07, 1.98
BARRIER_Y = 0.52


def P(u, v, w):
    """Backplate coordinates -> lineup local coordinates."""
    return Vector((BP_X0 + u, BP_Y - w, BP_Z0 + v))


class Lineup:
    def __init__(self, root_loc, name="SWG_LV", kit_offset=(0.22, -0.28, 0.0)):
        self.kit_offset = kit_offset
        self.name = name
        self.root = bpy.data.objects.new(name + "_Root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.location = root_loc
        coll("Switchgear").objects.link(self.root)
        self.c_sw = coll("Switchgear/SWG_LV_Lineup")
        self.c_panels = coll("Switchgear/SWG_LV_Panels")
        self.c_bus = coll("Switchgear/SWG_LV_Bus")
        self.c_dev = coll("Switchgear/SWG_LV_ControlDevices")
        self.c_cw = coll("Control_Wiring/CW_Cabinet_S3")
        self.c_cwdoor = coll("Control_Wiring/CW_Door_Harness")
        self.c_field = coll("Control_Wiring/CW_Field_Cores")
        self.c_pc = coll("Power_Cables/PC_SWG_Incoming")
        self.c_gnd = coll("Grounding/GND_SWG")
        self.c_kit = coll("Control_Wiring/CW_WireKit")
        self.c_ann = coll("Annotations/ANN_SWG")
        self.objs = []

    def own(self, ob):
        ob.parent = self.root
        self.objs.append(ob)
        return ob

    # ------------------------------------------------------------------
    def build(self):
        self.simple_bays()
        self.s3_frame()
        self.s3_door()
        self.backplate_and_ducts()
        self.devices()
        self.internal_wiring()
        self.field_cables()
        self.bus_and_power()
        self.grounding()
        self.kit()
        return self

    # ------------------------------------------------------------------
    def simple_bays(self):
        for i in range(NSEC - 1):
            x0 = i * W
            mb = MB()
            paint, dark = M("Paint_ANSI61"), M("Paint_Dark")
            mb.box_mm(x0 + 0.004, x0 + W - 0.004, 0.006, D, ZB, H, paint)          # body
            mb.box_mm(x0 + 0.010, x0 + W - 0.010, 0.010, D - 0.01, 0.0, ZB, M("Paint_Base"))
            mb.box_mm(x0 + 0.000, x0 + W, -0.004, D + 0.004, H, H + 0.012, paint)  # roof cap
            # 4 breaker cubicle doors
            zz = [ZB + 0.01, ZB + 0.545, ZB + 1.08, ZB + 1.615, H - 0.14]
            for k in range(4):
                z0, z1 = zz[k] + 0.003, zz[k + 1] - 0.003
                mb.box_mm(x0 + 0.010, x0 + W - 0.010, -0.002, 0.006, z0, z1, paint)
                zc = (z0 + z1) / 2
                mb.box_mm(x0 + 0.20, x0 + 0.56, -0.006, -0.001, zc - 0.10, zc + 0.12, dark)   # breaker escutcheon
                mb.box_mm(x0 + 0.24, x0 + 0.52, -0.009, -0.005, zc - 0.05, zc + 0.08, M("Glass_Dark"))
                mb.box_mm(x0 + W - 0.07, x0 + W - 0.05, -0.03, -0.002, zc - 0.06, zc + 0.06, M("Plastic_Black"))  # handle
                mb.box_mm(x0 + 0.30, x0 + 0.46, -0.004, -0.001, z1 - 0.06, z1 - 0.03, M("Marker_White"))      # nameplate
            # top vent louvres
            for k in range(6):
                z = H - 0.12 + k * 0.016
                mb.box_mm(x0 + 0.12, x0 + W - 0.12, -0.003, 0.004, z, z + 0.006, dark)
            ob = mb.obj(f"SWG_S{i+1}_Bay", self.c_sw, bevel=0.002)
            self.own(ob)
            mbn = MB()
            mbn.box_mm(x0 + 0.26, x0 + 0.50, -0.003, 0.0, H - 0.20, H - 0.15, M("Marker_White"))
            self.own(mbn.obj(f"SWG_S{i+1}_Nameplate", self.c_sw))

    # ------------------------------------------------------------------
    def s3_frame(self):
        x0, x1 = X3, X3 + W
        paint, galv = M("Paint_ANSI61"), M("Paint_Dark")
        mb = MB()
        t = 0.04
        # corner posts and intermediate post at barrier
        for (x, y) in [(x0, 0), (x1 - t, 0), (x0, D - t), (x1 - t, D - t), (x1 - t, BARRIER_Y - 0.02)]:
            mb.box_mm(x, x + t, y, y + t, ZB, H, paint)
        # top & bottom rails
        for z in (ZB, H - t):
            mb.box_mm(x0, x1, 0, t, z, z + t, paint)
            mb.box_mm(x0, x1, D - t, D, z, z + t, paint)
            mb.box_mm(x1 - t, x1, 0, D, z, z + t, paint)
        mb.box_mm(x0 + 0.01, x1 - 0.01, 0.01, D - 0.01, 0.0, ZB, M("Paint_Base"))   # base channel
        mb.box_mm(x0, x1, -0.004, D + 0.004, H, H + 0.012, paint)                   # roof cap
        mb.box_mm(x0, x1, 0, D, H - 0.003, H, paint)                                # roof plate
        mb.box_mm(x0, x1, D - 0.003, D, ZB, H, paint)                               # rear panel (closed)
        # barrier between front control compartment and rear bus/cable compartment
        mb.box_mm(x0 + 0.004, x1 - 0.004, BARRIER_Y, BARRIER_Y + 0.003, ZB + 0.06, H - 0.003, paint)
        # compartment floor / gland plate (front)
        mb.box_mm(x0 + 0.004, x1 - 0.004, 0.0, BARRIER_Y, ZB + 0.035, ZB + 0.04, paint)
        # bus pass-through barrier on the S2/S3 partition (insulating plate with slots)
        mb.box_mm(x0 - 0.001, x0 + 0.006, 0.80, 0.95, 1.52, 2.20, M("Insulator_Gray"))
        # rear floor plate with cable-entry opening
        mb.box_mm(x0 + 0.004, x1 - 0.004, BARRIER_Y + 0.003, 0.98, ZB + 0.035, ZB + 0.04, paint)
        mb.box_mm(x0 + 0.004, x1 - 0.004, 1.36, D - 0.003, ZB + 0.035, ZB + 0.04, paint)
        ob = mb.obj("SWG_S3_Frame", self.c_sw, bevel=0.0015)
        self.own(ob)
        # removable right side panel (cutaway)
        mb = MB()
        mb.box_mm(x1, x1 + 0.003, 0, D, ZB, H, paint)
        sp = mb.obj("SWG_S3_SidePanel_R", self.c_panels, bevel=0.001)
        tag_panel(sp, explode=(0.9, 0.0, 0.0))
        self.own(sp)
        # rear panel of compartment separate & removable as well
        # (kept in frame for the IEM view; side panel removal provides cutaway)
        # gland plate (front floor) with three control cable glands
        mb = MB()
        mb.box_mm(x0 + 0.12, x1 - 0.12, 0.30, 0.44, ZB + 0.040, ZB + 0.046, M("Steel_Galv"))
        self.gland_pts = []
        for k in range(4):
            gx = x0 + 0.16 + k * 0.13
            gy = 0.375
            mb.cyl(0.016, 0.022, (gx, gy, ZB + 0.057), M("Plastic_Black"), segs=6, smooth=False)  # hex nut
            mb.cyl(0.013, 0.03, (gx, gy, ZB + 0.08), M("Plastic_Black"), segs=20)                  # dome
            self.gland_pts.append(Vector((gx, gy, ZB + 0.095)))
        self.own(mb.obj("SWG_S3_GlandPlate_Control", self.c_sw))

    # ------------------------------------------------------------------
    def s3_door(self):
        """Control compartment door, hinged left, swung open ~105 deg.
        Built in closed-door coordinates then rotated about the hinge."""
        x0 = X3
        dw, dh, dt = W - 0.006, H - ZB - 0.02, 0.025
        paint = M("Paint_ANSI61")
        mb = MB()
        # door pan: outer skin + return flanges (inner side is +y)
        mb.box_mm(0.003, dw, -0.003, 0.0, 0, dh, paint)
        mb.box_mm(0.003, 0.018, 0.0, dt, 0, dh, paint)
        mb.box_mm(dw - 0.015, dw, 0.0, dt, 0, dh, paint)
        mb.box_mm(0.003, dw, 0.0, dt, 0, 0.015, paint)
        mb.box_mm(0.003, dw, 0.0, dt, dh - 0.015, dh, paint)
        # door-mounted devices (bodies on inner side)
        dev, lt = M("Plastic_Device"), M("Plastic_DeviceLt")
        mb.box_mm(0.16, 0.42, 0.0, 0.17, 1.55, 1.79, dev)          # protection relay / controller case
        mb.box_mm(0.48, 0.68, 0.0, 0.07, 1.58, 1.76, lt)           # operator HMI
        for k in range(4):                                          # pilot lights
            mb.cyl(0.013, 0.06, (0.20 + k * 0.08, 0.03, 1.32), dev, axis="Y")
        for k in range(3):                                          # selector switches + contact blocks
            mb.box_mm(0.21 + k * 0.10, 0.25 + k * 0.10, 0.0, 0.075, 1.12, 1.16, lt)
        mb.box_mm(0.05, 0.11, 0.0, 0.05, 0.25, 1.70, M("Plastic_Duct"))   # door wire duct
        # outer face hardware
        mb.box_mm(dw - 0.07, dw - 0.05, -0.035, -0.003, 1.00, 1.14, M("Plastic_Black"))   # handle
        mb.box_mm(0.17, 0.41, -0.006, -0.003, 1.56, 1.78, M("Plastic_Black"))             # relay bezel
        mb.box_mm(0.49, 0.67, -0.006, -0.003, 1.59, 1.75, M("Glass_Dark"))                # HMI screen
        cols = ["Pilot_Green", "Pilot_Red", "Pilot_Amber", "Pilot_Green"]
        for k in range(4):
            mb.cyl(0.015, 0.008, (0.20 + k * 0.08, -0.007, 1.32), M(cols[k]), axis="Y")
        for k in range(3):
            mb.cyl(0.02, 0.01, (0.23 + k * 0.10, -0.008, 1.14), M("Plastic_Black"), axis="Y")
        mb.box_mm(0.28, 0.48, -0.004, -0.001, dh - 0.09, dh - 0.05, M("Marker_White"))
        door = mb.obj("SWG_S3_ControlDoor", self.c_panels, bevel=0.0012)
        door.location = (x0 + 0.003, -0.002, ZB + 0.01)
        door.rotation_euler = (0, 0, math.radians(-105))
        tag_panel(door, explode=None)
        door["open_angle_deg"] = -105.0
        self.own(door)
        self.door = door
        # Door harness: bundle from backplate left duct -> hinge loop -> door duct
        Mdoor = Matrix.Translation(door.location) @ Matrix.Rotation(math.radians(-105), 4, "Z")
        def dp(x, y, z):
            return Mdoor @ Vector((x, y, z))
        start = P(0.03, 1.55, 0.07)
        pts = [start, P(0.03, 1.55, 0.20), Vector((x0 + 0.06, 0.08, ZB + 1.47)),
               Vector((x0 + 0.015, -0.02, ZB + 1.40)), dp(0.04, 0.06, 1.33), dp(0.08, 0.05, 1.30),
               dp(0.08, 0.03, 1.20)]
        bundle = []
        for k in range(8):
            a = 2 * math.pi * k / 8
            off = Vector((math.cos(a), math.sin(a), 0)) * 0.0045
            bundle.append([p + off for p in pts])
        ob = curve_obj("CW_DoorHarness_Bundle", bundle, 0.0016, M("Wire_Control"), self.c_cwdoor, fr=0.05, seg=6)
        self.own(ob)
        # spiral-wrap sleeve over hinge loop (presentation: dark sleeve segments)
        sl = [pts[1], pts[2], pts[3], pts[4]]
        ob = curve_obj("CW_DoorHarness_SpiralWrap", [sl], 0.0072, M("Plastic_Black"), self.c_cwdoor, fr=0.05, seg=6)
        self.own(ob)
        # fan-out from door duct to devices, dressed along the door skin
        fan = []
        targets = [(0.16, 1.60, 0.03), (0.16, 1.70, 0.03), (0.48, 1.62, 0.03),
                   (0.20, 1.32, 0.03), (0.28, 1.32, 0.03), (0.36, 1.32, 0.03),
                   (0.21, 1.14, 0.03), (0.31, 1.14, 0.03)]
        for k, (tx, tz, ty) in enumerate(targets):
            zz = 1.26 + 0.012 * k if tz > 1.2 else 1.05 - 0.01 * k
            s = dp(0.08, 0.03, 1.20)
            fan.append([s, dp(0.08, 0.03 + 0.003 * k, zz), dp(tx - 0.02, 0.03 + 0.003 * k, zz),
                        dp(tx - 0.02, 0.035, tz), dp(tx, 0.035, tz)])
        ob = curve_obj("CW_Door_FanOut", fan, 0.0015, M("Wire_Control"), self.c_cwdoor, fr=0.012)
        self.own(ob)
        # door bonding strap
        b0 = Vector((x0 + 0.03, 0.02, ZB + 0.3))
        b1 = dp(0.03, 0.02, 0.28)
        ob = curve_obj("GND_DoorBondStrap", [[b0, (b0 + b1) / 2 + Vector((0, 0, -0.04)), b1]], 0.004,
                       M("Braid"), self.c_gnd, fr=0.03)
        self.own(ob)

    # ------------------------------------------------------------------
    def backplate_and_ducts(self):
        mb = MB()
        mb.box_mm(BP_X0, BP_X0 + BP_W, BP_Y, BP_Y + 0.003, BP_Z0, BP_Z0 + BP_H, M("Backplate_White"))
        self.own(mb.obj("SWG_S3_Backplate", self.c_sw))
        # ducts
        self.hduct_v = {"H1": 1.86, "H2": 1.40, "H3": 0.98, "H4": 0.56, "H5": 0.14}
        self.vduct_u = {"L": 0.03, "R": BP_W - 0.03}
        self.dw, self.dd = 0.06, 0.08          # duct width / depth
        self.pitch = 0.011
        duct = MB()
        pm = M("Plastic_Duct")
        u0, u1 = 0.06, BP_W - 0.06
        for k, vc in self.hduct_v.items():
            a = P(u0, vc - 0.03, 0)
            duct.box_mm(a.x, P(u1, 0, 0).x, BP_Y - 0.002, BP_Y, P(0, vc - 0.03, 0).z, P(0, vc + 0.03, 0).z, pm)
            for side in (-1, 1):
                vz0 = vc + side * 0.03 - (0.002 if side > 0 else 0)
                z0, z1 = P(0, vz0, 0).z, P(0, vz0 + 0.002, 0).z
                duct.box_mm(a.x, P(u1, 0, 0).x, BP_Y - 0.015, BP_Y, z0, z1, pm)
                u = u0 + 0.002
                while u + 0.0065 <= u1:
                    duct.box_mm(P(u, 0, 0).x, P(u + 0.0065, 0, 0).x, BP_Y - self.dd, BP_Y - 0.015, z0, z1, pm)
                    u += self.pitch
        v0, v1 = 0.11, 1.89
        for k, uc in self.vduct_u.items():
            duct.box_mm(P(uc - 0.03, 0, 0).x, P(uc + 0.03, 0, 0).x, BP_Y - 0.002, BP_Y, P(0, v0, 0).z, P(0, v1, 0).z, pm)
            for side in (-1, 1):
                ux0 = uc + side * 0.03 - (0.002 if side > 0 else 0)
                x0, x1 = P(ux0, 0, 0).x, P(ux0 + 0.002, 0, 0).x
                duct.box_mm(x0, x1, BP_Y - 0.015, BP_Y, P(0, v0, 0).z, P(0, v1, 0).z, pm)
                v = v0 + 0.002
                while v + 0.0065 <= v1:
                    duct.box_mm(x0, x1, BP_Y - self.dd, BP_Y - 0.015, P(0, v, 0).z, P(0, v + 0.0065, 0).z, pm)
                    v += self.pitch
        self.own(duct.obj("SWG_S3_WireDuct", self.c_dev))
        # DIN rails
        rail = MB()
        for vc in (1.63, 1.19, 0.77, 0.35):
            a, b = P(0.065, vc - 0.0175, 0), P(BP_W - 0.065, vc + 0.0175, 0.0075)
            rail.box_mm(a.x, b.x, b.y, a.y, a.z, b.z, M("Steel_Galv"))
        self.own(rail.obj("SWG_S3_DINRails", self.c_dev))

    # ------------------------------------------------------------------
    def devices(self):
        """Control devices; records terminal points used by the router."""
        self.terms = []          # (name, Vector point, side +1 top/-1 bottom, row duct key)
        dev, lt, blk = M("Plastic_Device"), M("Plastic_DeviceLt"), M("Plastic_Black")
        mb = MB()

        def box(u0, u1, v0, v1, w0, w1, mat):
            a, b = P(u0, v0, w0), P(u1, v1, w1)
            mb.box_mm(a.x, b.x, b.y, a.y, a.z, b.z, mat)

        def term(name, u, v, w, side, duct):
            self.terms.append((name, P(u, v, w), side, duct, u))
            # screw head
            p = P(u, v + 0.004 * side * -1, w)
            mb.cyl(0.0022, 0.002, (p.x, p.y - 0.001, p.z), M("Steel_Galv"), axis="Y", segs=10)

        # Row A ---------------------------------------------------------------
        box(0.08, 0.20, 1.56, 1.72, 0.0, 0.03, M("Steel_Dark"))          # CPT base
        box(0.09, 0.19, 1.575, 1.705, 0.03, 0.12, M("Steel_Dark"))       # core
        box(0.105, 0.175, 1.565, 1.715, 0.045, 0.135, M("Brass"))        # coil
        box(0.085, 0.195, 1.705, 1.725, 0.02, 0.10, blk)                 # terminal strip
        for k in range(4):
            term(f"CPT_X{k+1}", 0.10 + k * 0.03, 1.725, 0.08, +1, "H1")
        for k in range(4):                                               # fuse holders
            u = 0.22 + k * 0.018
            box(u, u + 0.0175, 1.585, 1.675, 0.0, 0.07, lt)
            box(u + 0.003, u + 0.0145, 1.60, 1.66, 0.07, 0.074, blk)
            term(f"FU{k+1}_1", u + 0.009, 1.675, 0.05, +1, "H1")
            term(f"FU{k+1}_2", u + 0.009, 1.585, 0.05, -1, "H2")
        for k in range(4):                                               # MCBs
            u = 0.30 + k * 0.018
            box(u, u + 0.0175, 1.585, 1.675, 0.0, 0.065, lt)
            box(u + 0.004, u + 0.0135, 1.625, 1.64, 0.065, 0.075, M("Pilot_Red") if k == 0 else blk)
            term(f"CB{k+1}_1", u + 0.009, 1.675, 0.045, +1, "H1")
            term(f"CB{k+1}_2", u + 0.009, 1.585, 0.045, -1, "H2")
        box(0.39, 0.46, 1.565, 1.695, 0.0, 0.075, dev)                   # PLC CPU
        box(0.40, 0.45, 1.62, 1.68, 0.075, 0.077, M("Glass_Dark"))
        for m in range(3):                                               # IO modules
            u = 0.462 + m * 0.04
            box(u, u + 0.038, 1.565, 1.695, 0.0, 0.075, dev)
            box(u + 0.004, u + 0.034, 1.575, 1.685, 0.075, 0.08, lt)     # front connector
            for k in range(4):
                term(f"IO{m+1}_T{k+1}", u + 0.008 + k * 0.0075, 1.695, 0.06, +1, "H1")
                term(f"IO{m+1}_B{k+1}", u + 0.008 + k * 0.0075, 1.565, 0.06, -1, "H2")
        # Row B ---------------------------------------------------------------
        for r in range(10):                                              # relays + sockets
            u = 0.08 + r * 0.0275
            box(u, u + 0.027, 1.14, 1.24, 0.0, 0.025, dev)
            box(u + 0.002, u + 0.025, 1.152, 1.228, 0.025, 0.085, lt)
            box(u + 0.002, u + 0.025, 1.152, 1.228, 0.085, 0.088, blk)
            for k in range(2):
                term(f"K{r+1}_A{k+1}", u + 0.007 + k * 0.013, 1.24, 0.02, +1, "H2")
                term(f"K{r+1}_C{k+1}", u + 0.007 + k * 0.013, 1.14, 0.02, -1, "H3")
        for r in range(2):                                               # timer relays
            u = 0.37 + r * 0.0225
            box(u, u + 0.0222, 1.14, 1.24, 0.0, 0.07, lt)
            box(u + 0.004, u + 0.018, 1.20, 1.215, 0.07, 0.076, blk)
            term(f"KT{r+1}_A1", u + 0.011, 1.24, 0.05, +1, "H2")
            term(f"KT{r+1}_15", u + 0.011, 1.14, 0.05, -1, "H3")
        box(0.44, 0.53, 1.12, 1.255, 0.0, 0.11, lt)                      # 24 VDC supply
        for k in range(5):
            box(0.45 + k * 0.016, 0.458 + k * 0.016, 1.20, 1.24, 0.11, 0.112, dev)
        for k in range(2):
            term(f"PS_L{k+1}", 0.46 + k * 0.02, 1.255, 0.08, +1, "H2")
            term(f"PS_V{k+1}", 0.46 + k * 0.02, 1.12, 0.08, -1, "H3")
        self.own(mb.obj("SWG_S3_ControlDevices", self.c_dev, bevel=0.0006))
        # Terminal blocks (rows C and D) ---------------------------------------
        self.tb = {"C": [], "D": []}
        tbm = MB()
        gry, gy = M("Plastic_TB"), M("Plastic_TB_GY")

        def tb_row(key, vc, u0, n, n_gnd=0):
            u = u0
            tbm_box = lambda a, b, mat: tbm.box_mm(a.x, b.x, b.y, a.y, a.z, b.z, mat)
            tbm_box(P(u - 0.006, vc - 0.03, 0.0075), P(u - 0.001, vc + 0.03, 0.05), M("Plastic_Device"))  # end stop
            for i in range(n):
                mat = gy if i >= n - n_gnd else gry
                tbm_box(P(u, vc - 0.0275, 0.0075), P(u + 0.0058, vc + 0.0275, 0.036), mat)
                tbm_box(P(u, vc - 0.010, 0.036), P(u + 0.0058, vc + 0.010, 0.048), mat)
                tbm_box(P(u + 0.0004, vc - 0.008, 0.048), P(u + 0.0054, vc + 0.008, 0.0495), M("Marker_White"))
                for s in (-1, 1):
                    c = P(u + 0.0029, vc + s * 0.019, 0.0362)
                    tbm.cyl(0.0018, 0.0012, (c.x, c.y, c.z), M("Steel_Galv"), axis="Y", segs=8)
                self.tb[key].append(u + 0.0029)
                u += 0.0062
            tbm_box(P(u, vc - 0.0275, 0.0075), P(u + 0.0015, vc + 0.0275, 0.036), gry)  # end plate
            tbm_box(P(u + 0.002, vc - 0.03, 0.0075), P(u + 0.007, vc + 0.03, 0.05), M("Plastic_Device"))
            return u + 0.012
        nxt = tb_row("C", 0.77, 0.085, 46)
        tb_row("C", 0.77, nxt + 0.006, 30, n_gnd=4)
        nxt = tb_row("D", 0.35, 0.085, 46)
        tb_row("D", 0.35, nxt + 0.006, 30, n_gnd=4)
        self.own(tbm.obj("SWG_S3_TerminalBlocks", self.c_dev))
        # group marker carriers (identification labels)
        lab = MB()
        for vc in (0.77, 0.35):
            a, b = P(0.075, vc + 0.034, 0.03), P(0.14, vc + 0.046, 0.032)
            lab.box_mm(a.x, b.x, b.y, a.y, a.z, b.z, M("Marker_White"))
        for (u, v) in [(0.10, 1.75), (0.40, 1.715), (0.12, 1.26), (0.45, 1.27)]:
            a, b = P(u, v, 0.0), P(u + 0.05, v + 0.012, 0.002)
            lab.box_mm(a.x, b.x, b.y, a.y, a.z, b.z, M("Marker_White"))
        self.own(lab.obj("SWG_S3_IdentLabels", self.c_dev))

    # ------------------------------------------------------------------
    def _gap(self, u, used):
        """Nearest free finger gap centre (duct slot) for a crossing at u."""
        g0 = 0.06 + 0.002 + 0.0065 + 0.00225
        k = round((u - g0) / self.pitch)
        best = None
        for dk in (0, 1, -1, 2, -2, 3, -3):
            kk = k + dk
            n = used.get(kk, 0)
            if n < 3:
                best = kk
                break
        if best is None:
            best = k
        used[best] = used.get(best, 0) + 1
        return g0 + best * self.pitch, used[best] - 1

    def _vgap(self, v, used):
        g0 = 0.11 + 0.002 + 0.0065 + 0.00225
        k = round((v - g0) / self.pitch)
        for dk in (0, 1, -1, 2, -2, 3, -3):
            kk = k + dk
            if used.get(kk, 0) < 3:
                break
        used[kk] = used.get(kk, 0) + 1
        return g0 + kk * self.pitch, used[kk] - 1

    def internal_wiring(self):
        """Point-to-point routing: terminal -> duct slot -> duct lane -> vertical duct
        -> target duct -> slot -> terminal block. One curve object per conductor."""
        random.seed(7)
        lanes = {}
        gaps = {}

        def lane(duct):
            n = lanes.get(duct, 0)
            lanes[duct] = n + 1
            across = -0.021 + (n % 8) * 0.006
            depth = 0.010 + ((n // 8) % 10) * 0.0058
            return across, depth

        def hduct_edge(duct, side):
            return self.hduct_v[duct] + side * 0.03

        tbC_top = [(u, "C") for u in self.tb["C"]]
        tbD_top = [(u, "D") for u in self.tb["D"]]
        srcs = [t for t in self.terms]
        # pair sources with TB-C (top) left-to-right, overflow to TB-D (top)
        dests = tbC_top[:]
        random.shuffle(dests)
        conns = []
        for i, s in enumerate(srcs):
            d = dests[i] if i < len(dests) else tbD_top[(i - len(dests)) * 2 + 1]
            conns.append((s, d))
        # TB-C bottom -> TB-D top cross-connections (every other used block)
        for i in range(0, len(self.tb["C"]), 2):
            conns.append((("TBC_B%d" % i, None, -1, "H4", self.tb["C"][i]), (self.tb["D"][min(i, len(self.tb["D"]) - 1)], "D")))
        self.n_internal = len(conns)
        r = 0.0017
        mat = M("Wire_Control")
        for idx, (s, d) in enumerate(conns):
            name, pt, side, duct, us = s
            ud, row = d
            vrow = 0.77 if row == "C" else 0.35
            dduct = "H3" if row == "C" else "H4"
            pts = []
            if pt is None:   # TB-C bottom terminal
                pt = P(us, 0.77 - 0.0275, 0.018)
                side = -1
            pts.append(pt + Vector((0, 0.004, 0)))              # inside terminal
            pts.append(pt + Vector((0, 0, side * 0.012)))
            gu, n = self._gap(us, gaps.setdefault((duct, side), {}))
            a, dep = lane(duct)
            edge = hduct_edge(duct, -side)                         # wall nearest the device
            pts.append(P(gu, edge - (-side) * 0.012, dep + 0.02))
            pts.append(P(gu, edge + (-side) * 0.006, dep + 0.01))
            vlane = self.hduct_v[duct] + a * 0.8
            pts.append(P(gu + (0.01 if gu < 0.3 else -0.01), vlane, dep))
            if duct != dduct:
                # choose the vertical duct on the nearer side
                vk = "L" if (us + ud) / 2 < BP_W / 2 else "R"
                uc = self.vduct_u[vk]
                a2, dep2 = lane("V" + vk)
                pts.append(P(uc + a2 * 0.8, vlane, dep))
                vlane2 = self.hduct_v[dduct] + a * 0.8
                pts.append(P(uc + a2 * 0.8, vlane2, dep2))
                pts.append(P(ud + (0.01 if ud < uc else -0.01), vlane2, dep2))
                dep_end = dep2
                vl = vlane2
            else:
                vl = vlane
                dep_end = dep
            gu2, n2 = self._gap(ud, gaps.setdefault((dduct, -1), {}))
            edge2 = hduct_edge(dduct, -1)
            pts.append(P(gu2, edge2 + 0.006, dep_end + 0.01))
            pts.append(P(gu2, edge2 - 0.010, 0.03))
            tpt = P(ud, vrow + 0.0275, 0.018)
            pts.append(tpt + Vector((0, 0, 0.010)))
            pts.append(tpt + Vector((0, 0, -0.004)))
            # dedupe consecutive identical points
            clean = [pts[0]]
            for p in pts[1:]:
                if (p - clean[-1]).length > 1e-4:
                    clean.append(p)
            ob = wire(f"CW_S3_W{idx+101:03d}", clean, r, mat, self.c_cw, fr=0.008, seg=3)
            ob["from"] = name
            ob["to"] = f"TB-{row}:{self.tb[row].index(ud)+1}"
            self.own(ob)
        # wire markers at device ends (white sleeves) as one mesh
        mk = MB()
        for (name, pt, side, duct, us) in self.terms:
            c = pt + Vector((0, 0, side * 0.016))
            mk.cyl(0.0024, 0.009, (c.x, c.y, c.z), M("Marker_White"), segs=10)
        for row, vrow in (("C", 0.77), ("D", 0.35)):
            for u in self.tb[row]:
                c = P(u, vrow + 0.0275, 0.018) + Vector((0, 0, 0.016))
                mk.cyl(0.0024, 0.009, (c.x, c.y, c.z), M("Marker_White"), segs=10)
        self.own(mk.obj("CW_S3_WireMarkers", self.c_cw))

    # ------------------------------------------------------------------
    def field_cables(self):
        """Site-installed multi-conductor control cables entering through the
        gland plate, cores landing on the TB-D bottom (field side)."""
        jm, cm = M("Jacket_Control"), M("Wire_Field")
        n_per = 10
        tbD = self.tb["D"]
        for c, g in enumerate(self.gland_pts):
            strip = Vector((g.x, BP_Y - 0.05, BP_Z0 + 0.02))
            ob = wire(f"FLD_ControlCable_{c+1}", [g + Vector((0, 0, -0.06)), g + Vector((0, 0, 0.03)),
                                                  Vector((g.x, (g.y + strip.y) / 2, g.z + 0.06)), strip],
                      0.0085, jm, self.c_field, fr=0.04)
            self.own(ob)
            cores = []
            for k in range(n_per):
                ti = c * (len(tbD) // 4) + k * 2 + 1
                ti = min(ti, len(tbD) - 1)
                ud = tbD[ti]
                a = 2 * math.pi * k / n_per
                s = strip + Vector((math.cos(a) * 0.004, math.sin(a) * 0.004, 0.0))
                gu, _ = self._gap(ud, {})
                pts = [s, s + Vector((0, 0, 0.02)),
                       P(gu, 0.14 - 0.02, 0.03 + (k % 5) * 0.008),
                       P(gu, 0.14 + 0.03 + 0.008, 0.035),
                       P(ud, 0.35 - 0.0275 - 0.012, 0.018),
                       P(ud, 0.35 - 0.0275 + 0.004, 0.018)]
                cores.append(pts)
            ob = curve_obj(f"FLD_Cores_{c+1}", cores, 0.0013, cm, self.c_field, fr=0.012)
            self.own(ob)
        # cable entering below gland plate (stub into floor conduit opening)
        mb = MB()
        for g in self.gland_pts:
            mb.cyl(0.010, 0.008, (g.x, g.y, ZB + 0.03), M("Rubber"))
        self.own(mb.obj("FLD_GlandSeals", self.c_field))

    # ------------------------------------------------------------------
    def bus_and_power(self):
        cu = M("Copper")
        mb = MB()
        x_from, x_to = 0.06, NSEC * W - 0.02
        phases = [("A", 2.08), ("B", 1.93), ("C", 1.78), ("N", 1.63)]
        y_bus = 0.85
        for ph, zc in phases:
            for lam in (0.0, 0.0128):
                mb.box_mm(x_from, x_to, y_bus + lam, y_bus + lam + 0.0064, zc - 0.05, zc + 0.05, cu)
        # bus supports (insulating)
        for xs in (X3 + 0.08, X3 + W - 0.10):
            mb_s = (xs, xs + 0.03)
            mb.box_mm(mb_s[0], mb_s[1], y_bus - 0.02, y_bus + 0.04, 1.55, 2.16, M("Insulator_Gray"))
            mb.box_mm(mb_s[0], mb_s[1], y_bus + 0.04, D - 0.04, 2.13, 2.16, M("Paint_Dark"))   # bracket to frame
        # splice plates at S2/S3 joint
        for ph, zc in phases:
            mb.box_mm(X3 - 0.06, X3 + 0.06, y_bus + 0.0192, y_bus + 0.0256, zc - 0.045, zc + 0.045, cu)
            for bx in (-0.035, 0.035):
                for bz in (-0.025, 0.025):
                    mb.cyl(0.006, 0.05, (X3 + bx, y_bus + 0.01, zc + bz), M("Steel_Galv"), axis="Y", segs=6, smooth=False)
        # vertical risers (main-lug landing) behind the main bus
        y_r = 0.90
        self.lug_pts = []
        for i, (ph, zc) in enumerate(phases):
            xr = X3 + 0.13 + i * 0.15
            mb.box_mm(xr - 0.0375, xr + 0.0375, y_r, y_r + 0.0064, 0.62, zc + 0.05, cu)
            mb.box_mm(xr - 0.0375, xr + 0.0375, y_bus + 0.0192, y_r, zc - 0.05, zc + 0.05, cu)   # spacer to own phase
            for bz in (-0.025, 0.025):
                mb.cyl(0.006, 0.08, (xr, y_r - 0.02, zc + bz), M("Steel_Galv"), axis="Y", segs=6, smooth=False)
            # lug pad: two compression lugs per phase (two parallel cables)
            for j, dx in enumerate((-0.018, 0.018)):
                lx = xr + dx
                mb.box_mm(lx - 0.012, lx + 0.012, y_r + 0.0064, y_r + 0.0124, 0.66, 0.78, M("Copper_Tinned"))   # lug tongue
                mb.cyl(0.0135, 0.07, (lx, y_r + 0.026, 0.645), M("Copper_Tinned"), segs=20)               # barrel
                for bz in (0.70, 0.75):
                    mb.cyl(0.0055, 0.04, (lx, y_r + 0.005, bz), M("Steel_Galv"), axis="Y", segs=6, smooth=False)
                self.lug_pts.append((ph, Vector((lx, y_r + 0.026, 0.61))))
            # riser insulating support
            mb.box_mm(xr - 0.045, xr + 0.045, y_r + 0.007, y_r + 0.035, 1.05, 1.09, M("Insulator_Gray"))
        mb.box_mm(X3 + 0.04, X3 + W - 0.04, y_r + 0.035, y_r + 0.06, 1.05, 1.09, M("Paint_Dark"))
        ob = mb.obj("SWG_LV_MainBus_and_Risers", self.c_bus)
        self.own(ob)
        # incoming power cables from floor conduits up to the lugs
        conduit = MB()
        for i, (ph, lp) in enumerate(self.lug_pts):
            base = Vector((lp.x, 1.16, 0.0))
            pts = [Vector((base.x, base.y, -0.05)), Vector((base.x, base.y, 0.12)),
                   Vector((base.x, base.y, 0.22)), Vector((lp.x, (base.y + lp.y) / 2, 0.36)),
                   Vector((lp.x, lp.y, 0.50)), Vector((lp.x, lp.y, 0.615))]
            ob = bezier_cable(f"PC_SWG_Incoming_{ph}{i%2+1}", pts, 0.0135, M("Jacket_Power"), self.c_pc)
            self.own(ob)
            conduit.cyl(0.024, 0.11, (base.x, base.y, 0.055), M("Insulator_Gray"))
            conduit.torus(0.0215, 0.004, (base.x, base.y, 0.11), M("Insulator_Gray"), segs=20, rsegs=6)
            # phase identification tape near lug (field identification)
            conduit.cyl(0.0142, 0.03, (lp.x, lp.y, 0.55), M("Marker_White"))
        self.own(conduit.obj("PC_SWG_ConduitStubs", self.c_pc))

    # ------------------------------------------------------------------
    def grounding(self):
        cu, g = M("Copper"), M("Wire_Ground")
        mb = MB()
        y = 1.42
        mb.box_mm(0.06, NSEC * W - 0.02, y, y + 0.0064, 0.16, 0.21, cu)        # ground bus
        for xs in (0.30, 1.05, X3 + 0.10, X3 + 0.62):
            mb.box_mm(xs - 0.015, xs + 0.015, y + 0.0064, D - 0.003, 0.165, 0.205, M("Insulator_Gray"))
        lx = X3 + 0.62
        mb.box_mm(lx - 0.012, lx + 0.012, y - 0.006, y, 0.16, 0.24, M("Copper_Tinned"))
        mb.cyl(0.011, 0.05, (lx, y - 0.016, 0.255), M("Copper_Tinned"))
        self.own(mb.obj("GND_SWG_GroundBus", self.c_gnd))
        pts = [Vector((lx, y - 0.016, 0.28)), Vector((lx, y - 0.016, 0.33)), Vector((lx, 1.30, 0.32)),
               Vector((lx, 1.25, 0.15)), Vector((lx, 1.25, -0.05))]
        ob = bezier_cable("GND_SWG_GEC", pts, 0.008, g, self.c_gnd)
        self.own(ob)
        c = MB()
        c.cyl(0.018, 0.10, (lx, 1.25, 0.05), M("Insulator_Gray"))
        self.own(c.obj("GND_SWG_Conduit", self.c_gnd))
        # backplate bonding jumper + TB ground terminal lead to the frame stud
        stud = Vector((X3 + 0.02, BP_Y + 0.01, BP_Z0 + 0.06))
        bp = P(0.02, 0.06, 0.0)
        ob = curve_obj("GND_BackplateBond", [[bp + Vector((0, -0.002, 0)), bp + Vector((-0.004, -0.01, 0.0)),
                                               stud + Vector((0.004, -0.02, 0)), stud + Vector((0, -0.001, 0))]],
                       0.0035, M("Braid"), self.c_gnd, fr=0.01)
        self.own(ob)
        uu = self.tb["D"][-1]
        ob = wire("GND_TB_Ground_Lead", [P(uu, 0.35 - 0.0275 + 0.004, 0.018), P(uu, 0.35 - 0.05, 0.018),
                                         P(uu, 0.21, 0.06), P(0.02, 0.10, 0.06), P(0.0, 0.06, 0.02)],
                   0.0018, g, self.c_gnd, fr=0.02)
        self.own(ob)

    # ------------------------------------------------------------------
    def kit(self):
        """Removable prepared control-wire kit on a shop cart beside S3."""
        ck = self.c_kit
        n_before = len(self.objs)
        cx0, cx1, cy0, cy1, ztop = 2.70, 3.66, -1.52, -0.88, 0.86
        self.kit_bounds = (cx0, cx1, cy0, cy1, ztop)
        cart = MB()
        steel = M("Paint_Dark")
        cart.box_mm(cx0, cx1, cy0, cy1, ztop - 0.03, ztop - 0.004, M("Paint_ANSI61"))
        cart.box_mm(cx0 + 0.01, cx1 - 0.01, cy0 + 0.01, cy1 - 0.01, ztop - 0.004, ztop, M("Paint_Base"))   # ESD mat
        cart.box_mm(cx0, cx1, cy0, cy1, 0.24, 0.27, M("Paint_ANSI61"))
        for (x, y) in [(cx0, cy0), (cx1 - 0.03, cy0), (cx0, cy1 - 0.03), (cx1 - 0.03, cy1 - 0.03)]:
            cart.box_mm(x, x + 0.03, y, y + 0.03, 0.10, ztop - 0.03, steel)
            cart.cyl(0.045, 0.035, (x + 0.015, y + 0.015, 0.045), M("Rubber"), axis="X")
            cart.box_mm(x - 0.005, x + 0.035, y - 0.005, y + 0.035, 0.085, 0.10, steel)
        ym = (cy0 + cy1) / 2
        for dy in (-0.2, 0.2):
            cart.box_mm(cx1, cx1 + 0.07, ym + dy - 0.012, ym + dy + 0.012, ztop - 0.03, ztop - 0.01, steel)
            cart.cyl(0.012, 0.06, (cx1 + 0.07, ym + dy, ztop + 0.005), steel)
        cart.cyl(0.013, 0.44, (cx1 + 0.07, ym, ztop + 0.04), steel, axis="Y")
        self.own(cart.obj("KIT_ShopCart", ck, bevel=0.003))
        # compartment tray (kit packaging)
        tx0, tx1, ty0, ty1 = 2.78, 3.36, -1.21, -0.93
        tz0, tz1 = ztop, ztop + 0.07
        self.tray_box = (tx0, tx1, ty0, ty1, tz0, tz1)
        tr = MB()
        tm = M("Tote")
        tr.box_mm(tx0, tx1, ty0, ty1, tz0, tz0 + 0.006, tm)
        tr.box_mm(tx0, tx1, ty0, ty0 + 0.006, tz0, tz1, tm)
        tr.box_mm(tx0, tx1, ty1 - 0.006, ty1, tz0, tz1, tm)
        tr.box_mm(tx0, tx0 + 0.006, ty0, ty1, tz0, tz1, tm)
        tr.box_mm(tx1 - 0.006, tx1, ty0, ty1, tz0, tz1, tm)
        cw = (tx1 - tx0) / 3
        for k in (1, 2):
            x = tx0 + k * cw
            tr.box_mm(x - 0.003, x + 0.003, ty0, ty1, tz0, tz1 - 0.008, tm)
        for k in range(3):
            xc = tx0 + (k + 0.5) * cw
            tr.box_mm(xc - 0.055, xc + 0.055, ty0 - 0.002, ty0, tz0 + 0.016, tz0 + 0.056, M("Marker_White"))
        # kit label card held in a slot on the back wall
        lx0, lx1 = tx0 + 0.04, tx1 - 0.04
        tr.box_mm(lx0, lx1, ty1 + 0.001, ty1 + 0.005, tz1 - 0.03, tz1 + 0.085, M("Paper"))
        tr.box_mm(lx0, lx1, ty1 + 0.0005, ty1 + 0.001, tz1 + 0.058, tz1 + 0.085, M("Wire_Control"))
        tr.box_mm(lx0 - 0.01, lx1 + 0.01, ty1 - 0.002, ty1 + 0.008, tz1 - 0.03, tz1 - 0.022, tm)
        tray = self.own(tr.obj("KIT_Tray", ck, bevel=0.0015))
        for k in range(3):
            xc = tx0 + (k + 0.5) * cw
            self.own(text(f"KIT_Tray_StepLabel_{k+1}", f"STEP {k+1}", 0.022,
                          (xc, ty0 - 0.0025, tz0 + 0.036), (math.radians(90), 0, 0), M("Label_Ink"), ck))
        lxc = (lx0 + lx1) / 2
        self.own(text("KIT_Label_Title", "CONTROL WIRE KIT", 0.019, (lxc, ty1 + 0.0002, tz1 + 0.0715),
                      (math.radians(90), 0, 0), M("Marker_White"), ck))
        self.own(text("KIT_Label_Line1", "SECTION 3  |  STEPS 1-3", 0.015, (lxc, ty1 + 0.0005, tz1 + 0.038),
                      (math.radians(90), 0, 0), M("Label_Ink"), ck))
        self.own(text("KIT_Label_Line2", "REF. WIRING SCHEDULE", 0.012, (lxc, ty1 + 0.0005, tz1 + 0.012),
                      (math.radians(90), 0, 0), M("Label_Ink"), ck))
        # bundles: folded (hairpin) groups of prepared conductors per step
        mk = MB()

        def prepared_end(e, d, mk):
            d = d.normalized()
            rot = tuple(Vector((0, 0, 1)).rotation_difference(d).to_euler())
            mk.cyl(0.0025, 0.013, tuple(e - d * 0.010), M("Marker_White"), rot=rot, segs=10)
            mk.cyl(0.0021, 0.006, tuple(e + d * 0.003), M("Ferrule_Collar"), rot=rot, segs=10)
            mk.cyl(0.0012, 0.009, tuple(e + d * 0.010), M("Copper_Tinned"), rot=rot, segs=8)

        for k in range(3):
            xc = tx0 + (k + 0.5) * cw
            for b in range(2):
                splines = []
                nw = 12 - 2 * k + b
                bx = xc - 0.042 + b * 0.084
                for i in range(nw):
                    ox = (i - nw / 2) * 0.0036
                    z = tz0 + 0.009 + (i % 3) * 0.0034
                    ye = ty0 + 0.028 + (i % 4) * 0.007
                    end_a = Vector((bx + ox - 0.012, ye - 0.012, tz0 + 0.050 + (i % 3) * 0.004))
                    end_b = Vector((bx + ox + 0.012, ye - 0.010, tz0 + 0.052 + (i % 2) * 0.004))
                    pts = [end_a,
                           Vector((bx + ox - 0.012, ye + 0.02, z + 0.004)),
                           Vector((bx + ox - 0.010, ty1 - 0.05, z)),
                           Vector((bx + ox * 0.5, ty1 - 0.018, z + 0.002)),
                           Vector((bx + ox + 0.010, ty1 - 0.05, z + 0.004)),
                           Vector((bx + ox + 0.012, ye + 0.02, z + 0.006)),
                           end_b]
                    splines.append(pts)
                    prepared_end(end_a, end_a - pts[1], mk)
                    prepared_end(end_b, end_b - pts[-2], mk)
                ob = curve_obj(f"KIT_Step{k+1}_Bundle{b+1}", splines, 0.0017, M("Wire_Control"), ck, fr=0.02, seg=5)
                ob["kit_step"] = k + 1
                self.own(ob)
                mk.torus(0.012, 0.0016, (bx, ty1 - 0.09, tz0 + 0.013), M("Plastic_Black"), axis="Y", segs=20, rsegs=6)
                mk.box_mm(bx - 0.014, bx + 0.014, ty1 - 0.115, ty1 - 0.095, tz0 + 0.022, tz0 + 0.0235, M("Marker_Yellow"))
        # exploded individual prepared conductors laid out at the cart front
        self.loose = []
        for i in range(4):
            y = cy0 + 0.07 + i * 0.05
            x0, x1 = 2.80, 3.52 - 0.04 * i
            z = ztop + 0.0018
            pts = [Vector((x0, y, z)), Vector((x1, y, z))]
            ob = wire(f"KIT_Exploded_Conductor_{i+1}", pts, 0.0019, M("Wire_Control"), ck)
            self.own(ob)
            for e, sgn in ((pts[0], -1), (pts[1], 1)):
                c = e + Vector((-sgn * 0.03, 0, 0))
                mk.cyl(0.0029, 0.026, tuple(c), M("Marker_White"), axis="X", segs=12)
                mk.cyl(0.0023, 0.010, tuple(e + Vector((sgn * 0.005, 0, 0))), M("Ferrule_Collar"), axis="X", segs=12)
                mk.cyl(0.0013, 0.012, tuple(e + Vector((sgn * 0.016, 0, 0))), M("Copper_Tinned"), axis="X", segs=10)
            self.loose.append(pts)
        self.own(mk.obj("KIT_Ends_Ferrules_Markers", ck))
        for i, pts in enumerate(self.loose):
            for j, e in enumerate(pts):
                sgn = -1 if j == 0 else 1
                c = e + Vector((-sgn * 0.03, 0, 0.0030))
                self.own(text(f"KIT_Marker_Text_{i+1}_{'AB'[j]}", f"{201+i}", 0.0048, tuple(c), (0, 0, 0),
                              M("Label_Ink"), ck))
        # clipboard: simplified wiring-schedule reference + inspection record
        cb = MB()
        bx0, bx1, by0, by1 = 3.41, 3.63, -1.24, -0.92
        self.clip_box = (bx0, bx1, by0, by1)
        cb.box_mm(bx0, bx1, by0, by1, ztop, ztop + 0.004, M("Paint_ANSI61"))
        cb.box_mm(bx0 + 0.01, bx1 - 0.01, by0 + 0.01, by1 - 0.03, ztop + 0.004, ztop + 0.0048, M("Paper"))
        cb.box_mm((bx0 + bx1) / 2 - 0.04, (bx0 + bx1) / 2 + 0.04, by1 - 0.035, by1 - 0.01, ztop + 0.004, ztop + 0.012, M("Steel_Galv"))
        for r in range(11):
            y = by1 - 0.075 - r * 0.018
            cb.box_mm(bx0 + 0.02, bx1 - 0.02, y, y + 0.0012, ztop + 0.0048, ztop + 0.0050, M("Label_Ink"))
        for cxx in (0.05, 0.10, 0.15):
            cb.box_mm(bx0 + cxx, bx0 + cxx + 0.0012, by0 + 0.03, by1 - 0.075, ztop + 0.0048, ztop + 0.0050, M("Label_Ink"))
        for r in range(4):     # blank check boxes (inspection / test record, no results)
            y = by0 + 0.03 + r * 0.018
            cb.box_mm(bx1 - 0.035, bx1 - 0.025, y, y + 0.01, ztop + 0.0048, ztop + 0.0052, M("Wire_Control"))
        self.own(cb.obj("KIT_WiringSchedule_Ref", ck))
        self.own(text("KIT_Schedule_Header", "WIRING SCHEDULE", 0.0125, ((bx0 + bx1) / 2, by1 - 0.055, ztop + 0.0052),
                      (0, 0, 0), M("Label_Ink"), ck))
        # re-parent every kit object under a movable kit root (removable / explodable)
        kr = bpy.data.objects.new("KIT_Root", None)
        kr.empty_display_type = "CUBE"
        kr.empty_display_size = 0.1
        ck.objects.link(kr)
        kr.parent = self.root
        kr.location = self.kit_offset
        tag_explode(kr, (0.6, -0.4, 0.0))
        for ob in self.objs[n_before:]:
            ob.parent = kr
        self.kit_root = kr

    def kit_world(self, p):
        return self.root.location + Vector(self.kit_offset) + Vector(p)

    def world(self, p):
        return self.root.location + Vector(p)
