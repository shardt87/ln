#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_plant.py  --  procedural 3x1 combined-cycle gas power plant for Blender 4.x

Run inside Blender (background):
    blender -b -P build_plant.py -- --out out/plant.blend
Run without Blender (dry run: builds all geometry in memory, prints the
preflight report, writes out/preflight.json, creates no .blend):
    python3 build_plant.py --dry-run

Everything is generated from the single PARAMS block below.  All dimensions
are FEET; TRUE_SCALE converts once to Blender metres at object creation.
Every object is named  <PACKAGE>-<PART>  so packages can be hidden by prefix
(GT-1-, HRSG-2-, ACC-, ELEC-EHOUSE-, ...).  Anchor empties are named
ANCHOR-<PACKAGE>-<KEY> and carry a "label" custom property used by the sheets.

No add-ons, no booleans, no modifiers: plain meshes, curves, empties.
"""
import math, json, os, sys, random

# =============================================================================
# PARAMS  --  the only block you should need to edit
# =============================================================================
TRUE_SCALE = 0.3048            # one conversion: feet -> Blender metres

PARAMS = {
    "seed": 31,
    # ---- site -------------------------------------------------------------
    "site_ft": (2000, 1400),            # x east, y north (plan: 1800 x 1400; widened for zone column E)
    "outside_strip_ft": 250,            # fuel-supply context strip east of the fence
    "fence_inset_ft": 30, "fence_h_ft": 8,
    "road_w_ft": 24, "perimeter_road_inset_ft": 60,
    "spine_road_y_ft": 312,             # centreline of the E-W spine road
    "ns_roads_x_ft": (512, 1162, 1407, 1707),
    "pad_t_ft": 1.5, "joint_pitch_ft": 20,
    "backdrop_extent_ft": 12000,
    # ---- counts -----------------------------------------------------------
    "counts": {"GT": 3, "HRSG": 3, "ST": 1, "GSU": 4, "BESS": 8, "PCS_TX": 8,
               "standby": 2, "black_start": 1, "fuel_cell": 4, "reels": 6,
               "chiller": 3, "tower": 4},
    # ---- power block ------------------------------------------------------
    "unit_pitch_ft": 130, "hrsg_gap_ft": 35, "service_gap_ft": 25,
    "hall_ft": (600, 164.04, 114.83),   # L (E-W) x W (N-S) x eave height  [Keadby ES Table 4.1 W/H]
    "hall_origin_ft": (540, 640),       # SW corner of hall
    "hall_crane_rail_ft": 65,
    "gt_axes_x_ft": (640, 770, 900),    # GT train axes (N-S), pitch 130
    "st_axis_x_ft": 1050,
    "gt_train_ft": (110, 35, 28),       # train envelope L x W x H
    "st_train_ft": (140, 45, 35),
    "inlet_ft": (60, 40, 25), "inlet_base_ft": 25, "inlet_offset_x_ft": -55,
    "hrsg_ft": (91.86, 164.04, 183.73), # transverse x gas-path length x height [Keadby envelope]
    "stack_d_h_ft": (26.25, 278.87),    # [Keadby]
    # ---- ACC --------------------------------------------------------------
    "acc_ft": (262.47, 262.47, 118.11), "acc_cells": (8, 8),
    "acc_fan_deck_ft": 82, "acc_fan_d_ft": 28, "acc_origin_ft": (1428, 1040),
    # ---- electrical -------------------------------------------------------
    "switchyard_ft": (360, 240), "switchyard_origin_ft": (90, 1060),
    "gen_tie_h_ft": 70, "gen_tie_gantry_y_ft": 505, "gen_tie_route_x_ft": 470,
    "gsu_ft": (49.21, 32.81, 32.81), "gsu_y_ft": 540,      # [Spalding transformer limit 15x10x10 m]
    "ipb_d_ft": 2.5, "ipb_z_ft": 18, "ipb_spacing_ft": 5,
    "ehouse_ft": (120, 32, 14), "ehouse_floor_ft": 8, "ehouse_origin_ft": (300, 420),
    "mcc_ft": (80, 40, 16), "mcc_origin_ft": (1190, 780),
    "admin_ft": (100, 60, 24), "admin_origin_ft": (110, 600),
    "bess_ft": (40, 8, 9.5), "pcs_tx_ft": (24, 10, 10), "bess_origin_ft": (110, 900),
    # ---- balance of plant -------------------------------------------------
    "laydown_ft": (180, 110), "laydown_origin_ft": (110, 740),
    "reel_d_w_ft": (8, 6), "prefab_spine_l_ft": 40,
    "modular_yard_ft": (180, 120), "modular_origin_ft": (1200, 520),
    "genset_ft": (40, 12, 14), "fuel_cell_ft": (20, 8, 10),
    "chiller_ft": (30, 10, 12), "tower_cell_ft": (24, 24, 30), "chill_origin_ft": (1440, 860),
    "water_treatment_ft": (80, 50, 20), "pond_ft": (140, 90, 8),
    "water_tank_n_d_h_ft": (2, 40, 30), "water_origin_ft": (1440, 470),
    "dcc_d_h_ft": (35, 90), "absorber_ft": (52.49, 141.08, 324.80),
    "regenerator_d_h_ft": (49.21, 173.88), "ccs_outlet_z_ft": 344.49, "ccs_origin_ft": (1730, 960),
    "flue_duct_d_ft": 14, "flue_duct_z_ft": 50,
    "gas_meter_ft": (40, 25, 16), "process_tank_n_d_h_ft": (2, 22, 28), "gasmet_origin_ft": (1740, 560),
    "lng_d_h_ft": (18, 50), "h2_module_ft": (40, 8, 9.5), "pipeline_d_ft": 2.0, "pipeline_y_ft": 580,
    # ---- cable corridor ---------------------------------------------------
    "corridor_w_ft": 24, "corridor_y_ft": 340, "corridor_x_ft": (300, 1900),
    "tray_power_control_z_ft": (4, 6), "duct_z_ft": -4, "earth_z_pitch_ft": (-1.5, 25),
    "mv_laterals_x_ft": (410, 1180, 1430, 1735),
    "voltages_kV": {"generator": 18, "MV": 13.8, "LV": 0.48, "HV": 230},
    # ---- look -------------------------------------------------------------
    "colors": {"ENCL": "#E6E4DF", "STEEL": "#9A9C9E", "STEEL_DK": "#6E7072", "CONC": "#C9C6BF",
               "JOINT": "#A8A59E", "ASPH": "#5A5A58", "CRACK": "#3C3C3A", "CABLE": "#141414",
               "COPPER": "#C8722E", "BACKDROP": "#D9D8D5", "GRAVEL": "#BDBBB4", "WATER": "#8E9A9C",
               "GLASS": "#9FA6A8", "INSUL": "#D2D0CB", "PORCELAIN": "#B9BDBE", "TEXT": "#4A4A48"},
}
# =============================================================================

P = PARAMS
FT = TRUE_SCALE
random.seed(P["seed"])

try:
    import bpy
    HAVE_BPY = True
except ImportError:      # dry run outside Blender
    bpy = None
    HAVE_BPY = False

DRY_RUN = (not HAVE_BPY) or ("--dry-run" in sys.argv)
ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
OUT_BLEND = "out/plant.blend"
if "--out" in ARGV:
    OUT_BLEND = ARGV[ARGV.index("--out") + 1]

# -----------------------------------------------------------------------------
# materials
# -----------------------------------------------------------------------------
def hex_to_lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)

C = P["colors"]
# key: (hex, roughness, metallic, special)
MATERIALS = {
    "ENCL":     (C["ENCL"], 0.85, 0.0, None),
    "STEEL":    (C["STEEL"], 0.65, 0.25, None),
    "STEEL_DK": (C["STEEL_DK"], 0.6, 0.3, None),
    "CONC":     (C["CONC"], 0.95, 0.0, "scored"),
    "GRAVEL":   (C["GRAVEL"], 1.0, 0.0, None),
    "ASPH":     (C["ASPH"], 0.95, 0.0, None),
    "CRACK":    (C["CRACK"], 1.0, 0.0, None),
    "CABLE":    (C["CABLE"], 0.55, 0.0, None),
    "COPPER":   (C["COPPER"], 0.35, 0.9, None),
    "BACKDROP": (C["BACKDROP"], 1.0, 0.0, None),
    "WATER":    (C["WATER"], 0.15, 0.0, None),
    "GLASS":    (C["GLASS"], 0.2, 0.0, None),
    "INSUL":    (C["INSUL"], 0.8, 0.0, None),
    "PORCELAIN": (C["PORCELAIN"], 0.35, 0.0, None),
    "XRAY":     (C["CONC"], 0.9, 0.0, "xray"),
    "DUCT":     ("#8A8882", 0.9, 0.0, None),
}
_MAT_CACHE = {}

# (noise scale per metre, bump strength, colour variation, per-object tint variation)
_DETAIL = {
    "GRAVEL": (55.0, 0.55, 0.10, 0.00), "ASPH": (170.0, 0.45, 0.10, 0.00), "CONC": (9.0, 0.10, 0.045, 0.02),
    "ENCL": (14.0, 0.0, 0.020, 0.035), "STEEL": (60.0, 0.06, 0.05, 0.05), "STEEL_DK": (60.0, 0.06, 0.05, 0.05),
    "INSUL": (18.0, 0.0, 0.03, 0.03), "DUCT": (20.0, 0.05, 0.04, 0.03), "PORCELAIN": (30.0, 0.0, 0.02, 0.03),
}

def _surface_detail(m, bsdf, key, rgb, special):
    """large-scale mottling + fine bump + a small per-object tint, so flat surfaces read as real materials.
    The colour stays inside the specified palette (variations are a few percent)."""
    if key not in _DETAIL:
        return
    scale, bump_s, var, tint = _DETAIL[key]
    nt = m.node_tree
    N = nt.nodes
    tc = N.new("ShaderNodeTexCoord")
    mp = N.new("ShaderNodeMapping")
    nz = N.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 8.0
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    # where does the current colour come from? (the scored-concrete brick node, if present)
    src = None
    for l in nt.links:
        if l.to_socket == bsdf.inputs["Base Color"]:
            src = l.from_socket
    def ramp(fac_socket, lo, hi):
        cr = N.new("ShaderNodeValToRGB")
        cr.color_ramp.elements[0].color = (lo, lo, lo, 1.0)
        cr.color_ramp.elements[1].color = (hi, hi, hi, 1.0)
        nt.links.new(fac_socket, cr.inputs["Fac"])
        return cr.outputs["Color"]
    cur = src
    if var > 0:
        mix = N.new("ShaderNodeMixRGB")
        mix.blend_type = "MULTIPLY"
        mix.inputs["Fac"].default_value = 1.0
        if cur is None:
            mix.inputs["Color1"].default_value = (*rgb, 1.0)
        else:
            nt.links.new(cur, mix.inputs["Color1"])
        nt.links.new(ramp(nz.outputs["Fac"], 1.0 - var, 1.0 + var * 0.4), mix.inputs["Color2"])
        cur = mix.outputs["Color"]
    if tint > 0:
        oi = N.new("ShaderNodeObjectInfo")
        mix2 = N.new("ShaderNodeMixRGB")
        mix2.blend_type = "MULTIPLY"
        mix2.inputs["Fac"].default_value = 1.0
        if cur is None:
            mix2.inputs["Color1"].default_value = (*rgb, 1.0)
        else:
            nt.links.new(cur, mix2.inputs["Color1"])
        nt.links.new(ramp(oi.outputs["Random"], 1.0 - tint, 1.0), mix2.inputs["Color2"])
        cur = mix2.outputs["Color"]
    if cur is not None:
        nt.links.new(cur, bsdf.inputs["Base Color"])
    if bump_s > 0:
        bp = N.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump_s
        bp.inputs["Distance"].default_value = 0.02
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])

def get_mat(key):
    if not HAVE_BPY:
        return key
    if key in _MAT_CACHE:
        return _MAT_CACHE[key]
    hexcol, rough, metal, special = MATERIALS[key]
    m = bpy.data.materials.new("MAT-" + key)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    rgb = hex_to_lin(hexcol)
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    for k in ("Specular IOR Level", "Specular"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.2
            break
    if special == "scored":
        # expansion-joint grid: brick texture used as a plain grid in world metres
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        br = nt.nodes.new("ShaderNodeTexBrick")
        pitch = P["joint_pitch_ft"] * FT
        mp.inputs["Scale"].default_value = (1.0 / pitch, 1.0 / pitch, 1.0 / pitch)
        br.offset = 0.0
        br.squash = 1.0
        br.inputs["Scale"].default_value = 1.0
        br.inputs["Mortar Size"].default_value = 0.006
        br.inputs["Mortar Smooth"].default_value = 0.5
        br.inputs["Color1"].default_value = (*rgb, 1.0)
        br.inputs["Color2"].default_value = (*rgb, 1.0)
        br.inputs["Mortar"].default_value = (*hex_to_lin(C["JOINT"]), 1.0)
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], br.inputs["Vector"])
        nt.links.new(br.outputs["Color"], bsdf.inputs["Base Color"])
    if special == "xray":
        m.blend_method = "BLEND"
        bsdf.inputs["Alpha"].default_value = 0.35
    else:
        _surface_detail(m, bsdf, key, rgb, special)
    m["plant_material"] = key
    _MAT_CACHE[key] = m
    return m

# -----------------------------------------------------------------------------
# registry + object factories (work with or without bpy)
# -----------------------------------------------------------------------------
REG = []            # every created object: dict(name, pkg, kind, bbox, below_grade, coll)
NAMES = set()

def _pkg_of(name):
    parts = name.split("-")
    if parts[0] in ("GT", "HRSG", "GSU", "UAT", "INLET") and len(parts) > 1 and parts[1].isdigit():
        return parts[0] + "-" + parts[1]
    if parts[0] == "ELEC" and len(parts) > 1:
        return parts[0] + "-" + parts[1]
    if parts[0] == "ANCHOR":
        return "ANCHOR"
    return parts[0]

def _collection_for(name):
    p = _pkg_of(name)
    return p.split("-")[0] if p.startswith(("GT-", "HRSG-", "GSU-", "UAT-", "INLET-")) else p

def _register(name, kind, bbox, below, coll=None):
    if name in NAMES:
        raise ValueError("duplicate object name: " + name)
    NAMES.add(name)
    REG.append(dict(name=name, pkg=_pkg_of(name), kind=kind, bbox=bbox, below_grade=bool(below),
                    coll=coll or _collection_for(name)))

def _bpy_link(obj, collname):
    col = bpy.data.collections.get(collname)
    if col is None:
        col = bpy.data.collections.new(collname)
        bpy.context.scene.collection.children.link(col)
    col.objects.link(obj)

def _bbox(verts):
    xs = [v[0] for v in verts]; ys = [v[1] for v in verts]; zs = [v[2] for v in verts]
    return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))

def _rotz(x, y, cx, cy, ang):
    if not ang:
        return (x, y)
    c, s = math.cos(ang), math.sin(ang)
    dx, dy = x - cx, y - cy
    return (cx + c * dx - s * dy, cy + s * dx + c * dy)


class MeshAcc:
    """Accumulates boxes / cylinders / prisms in FEET and builds ONE mesh object."""
    def __init__(self, name, mat, below=False, coll=None, cutaway=False):
        self.name, self.mat, self.below, self.coll, self.cutaway = name, mat, below, coll, cutaway
        self.verts, self.faces, self.smooth = [], [], []

    # --- primitives ---------------------------------------------------------
    def _add(self, verts, faces, smooth_flags=None):
        base = len(self.verts)
        self.verts.extend(verts)
        for i, f in enumerate(faces):
            self.faces.append(tuple(base + j for j in f))
            self.smooth.append(bool(smooth_flags[i]) if smooth_flags else False)

    def hexa(self, pts):
        """8 points: bottom quad (ccw seen from above) then top quad in same order."""
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        self._add(list(pts), f)
        return self

    def box(self, x0, y0, z0, x1, y1, z1):
        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0
        if z0 > z1: z0, z1 = z1, z0
        return self.hexa([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                          (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)])

    def boxc(self, cx, cy, z0, L, W, H, rot=0.0):
        hx, hy = L / 2.0, W / 2.0
        c = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
        b = [(_rotz(cx + dx, cy + dy, cx, cy, rot) + (z0,)) for dx, dy in c]
        t = [(x, y, z0 + H) for x, y, _ in b]
        return self.hexa(b + t)

    def cyl_between(self, p0, p1, r, n=16, caps=True, r2=None):
        ax = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        L = math.sqrt(sum(a * a for a in ax))
        if L < 1e-9:
            return self
        ax = tuple(a / L for a in ax)
        ref = (0, 0, 1) if abs(ax[2]) < 0.9 else (1, 0, 0)
        u = (ax[1] * ref[2] - ax[2] * ref[1], ax[2] * ref[0] - ax[0] * ref[2], ax[0] * ref[1] - ax[1] * ref[0])
        ul = math.sqrt(sum(a * a for a in u)); u = tuple(a / ul for a in u)
        v = (ax[1] * u[2] - ax[2] * u[1], ax[2] * u[0] - ax[0] * u[2], ax[0] * u[1] - ax[1] * u[0])
        r2 = r if r2 is None else r2
        verts = []
        for (p, rr) in ((p0, r), (p1, r2)):
            for i in range(n):
                a = 2 * math.pi * i / n
                verts.append((p[0] + rr * (math.cos(a) * u[0] + math.sin(a) * v[0]),
                              p[1] + rr * (math.cos(a) * u[1] + math.sin(a) * v[1]),
                              p[2] + rr * (math.cos(a) * u[2] + math.sin(a) * v[2])))
        faces, sm = [], []
        for i in range(n):
            j = (i + 1) % n
            faces.append((i, j, n + j, n + i)); sm.append(True)
        if caps:
            faces.append(tuple(reversed(range(n)))); sm.append(False)
            faces.append(tuple(range(n, 2 * n))); sm.append(False)
        self._add(verts, faces, sm)
        return self

    def cyl(self, cx, cy, z0, r, h, n=16, caps=True, r2=None):
        return self.cyl_between((cx, cy, z0), (cx, cy, z0 + h), r, n, caps, r2)

    def seg(self, p0, p1, r, n=8):
        return self.cyl_between(p0, p1, r, n, True)

    def sphere(self, cx, cy, cz, r, n=12):
        verts, faces = [], []
        rings = n // 2
        for i in range(1, rings):
            th = math.pi * i / rings
            for j in range(n):
                ph = 2 * math.pi * j / n
                verts.append((cx + r * math.sin(th) * math.cos(ph), cy + r * math.sin(th) * math.sin(ph), cz + r * math.cos(th)))
        top = len(verts); verts.append((cx, cy, cz + r))
        bot = len(verts); verts.append((cx, cy, cz - r))
        for i in range(rings - 2):
            for j in range(n):
                a, b = i * n + j, i * n + (j + 1) % n
                faces.append((a, b, b + n, a + n))
        for j in range(n):
            faces.append((top, (j + 1) % n, j))
            faces.append((bot, (rings - 2) * n + j, (rings - 2) * n + (j + 1) % n))
        self._add(verts, faces, [True] * len(faces))
        return self

    def plate(self, pts, z, flip=False):
        """flat n-gon (list of (x,y)) at height z."""
        f = list(range(len(pts)))
        if flip:
            f.reverse()
        self._add([(x, y, z) for x, y in pts], [tuple(f)])
        return self

    # --- composite helpers --------------------------------------------------
    def stair(self, x, y, z0, z1, run_dir=(1, 0), width=3.0, riser=0.6):
        n = max(1, int((z1 - z0) / riser))
        tread = 0.9
        for i in range(n):
            px, py = x + run_dir[0] * i * tread, y + run_dir[1] * i * tread
            L = tread if run_dir[0] else width
            W = width if run_dir[0] else tread
            self.box(px, py, z0 + i * riser, px + L, py + W, z0 + i * riser + 0.15)
        return self

    def lattice(self, cx, cy, z0, h, w_base, w_top, r=0.45, panels=None):
        """4-leg lattice tower (legs + rings + X braces) as segments."""
        panels = panels or max(2, int(h / 18))
        for k in range(4):
            sx, sy = ((-1, -1), (1, -1), (1, 1), (-1, 1))[k]
            self.seg((cx + sx * w_base / 2, cy + sy * w_base / 2, z0), (cx + sx * w_top / 2, cy + sy * w_top / 2, z0 + h), r, 6)
        for i in range(panels + 1):
            t = i / panels
            w = w_base + (w_top - w_base) * t
            z = z0 + h * t
            cs = [(cx - w / 2, cy - w / 2, z), (cx + w / 2, cy - w / 2, z), (cx + w / 2, cy + w / 2, z), (cx - w / 2, cy + w / 2, z)]
            for k in range(4):
                self.seg(cs[k], cs[(k + 1) % 4], r * 0.6, 5)
            if i < panels:
                t2 = (i + 1) / panels
                w2 = w_base + (w_top - w_base) * t2
                z2 = z0 + h * t2
                cs2 = [(cx - w2 / 2, cy - w2 / 2, z2), (cx + w2 / 2, cy - w2 / 2, z2), (cx + w2 / 2, cy + w2 / 2, z2), (cx - w2 / 2, cy + w2 / 2, z2)]
                for k in range(4):
                    self.seg(cs[k], cs2[(k + 1) % 4], r * 0.5, 5)
        return self

    def tray(self, pts, z, width=3.0, rail_h=0.5, post_pitch=10.0, posts=True, post_z0=0.0):
        """cable tray (bottom plate + 2 side rails) along polyline pts at height z."""
        for (a, b) in zip(pts[:-1], pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            if L < 1e-6:
                continue
            ux, uy = dx / L, dy / L
            nx, ny = -uy, ux
            hw = width / 2
            corners = [(a[0] + nx * hw, a[1] + ny * hw), (a[0] - nx * hw, a[1] - ny * hw),
                       (b[0] - nx * hw, b[1] - ny * hw), (b[0] + nx * hw, b[1] + ny * hw)]
            # ladder tray: rungs every 1 ft between the side rails (cables are visible through it)
            kk = 0.0
            while kk <= L:
                cx_, cy_ = a[0] + ux * kk, a[1] + uy * kk
                c0 = (cx_ + nx * hw, cy_ + ny * hw)
                c1 = (cx_ - nx * hw, cy_ - ny * hw)
                q = [(c0[0] - ux * 0.07, c0[1] - uy * 0.07), (c1[0] - ux * 0.07, c1[1] - uy * 0.07),
                     (c1[0] + ux * 0.07, c1[1] + uy * 0.07), (c0[0] + ux * 0.07, c0[1] + uy * 0.07)]
                self.hexa([(x, y, z) for x, y in q] + [(x, y, z + 0.1) for x, y in q])
                kk += 1.0
            kk = 10.0                      # splice plates on the rails every 10 ft
            while kk < L:
                for s in (1, -1):
                    px_, py_ = a[0] + ux * kk + s * nx * hw, a[1] + uy * kk + s * ny * hw
                    self.box(px_ - 0.5 * abs(ux) - 0.12, py_ - 0.5 * abs(uy) - 0.12, z + 0.05,
                             px_ + 0.5 * abs(ux) + 0.12, py_ + 0.5 * abs(uy) + 0.12, z + rail_h + 0.04)
                kk += 10.0
            for s in (1, -1):
                c2 = [(a[0] + s * nx * hw, a[1] + s * ny * hw), (a[0] + s * nx * (hw - 0.15), a[1] + s * ny * (hw - 0.15)),
                      (b[0] + s * nx * (hw - 0.15), b[1] + s * ny * (hw - 0.15)), (b[0] + s * nx * hw, b[1] + s * ny * hw)]
                self.hexa([(x, y, z) for x, y in c2] + [(x, y, z + rail_h) for x, y in c2])
            if posts:
                k = 0.0
                while k <= L + 1e-6:
                    px, py = a[0] + ux * k, a[1] + uy * k
                    if on_road(px, py):
                        k += post_pitch
                        continue
                    self.box(px - 0.3, py - 0.3, post_z0, px + 0.3, py + 0.3, z)
                    self.box(px - 0.2 - abs(nx) * hw, py - 0.2 - abs(ny) * hw, z - 0.35,
                             px + 0.2 + abs(nx) * hw, py + 0.2 + abs(ny) * hw, z)
                    k += post_pitch
        return self

    def pipe_supports(self, pts, z, pitch=20.0, w=1.0):
        for (a, b) in zip(pts[:-1], pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 1e-6:
                continue
            k = 0.0
            while k <= L + 1e-6:
                t = k / L
                px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                if not on_road(px, py):
                    self.box(px - w / 2, py - w / 2, 0, px + w / 2, py + w / 2, z)
                k += pitch
        return self

    # --- build ----------------------------------------------------------------
    def build(self, props=None):
        if not self.verts:
            return None
        bb = _bbox(self.verts)
        _register(self.name, "mesh", bb, self.below, self.coll)
        if not HAVE_BPY:
            return None
        me = bpy.data.meshes.new(self.name)
        me.from_pydata([(x * FT, y * FT, z * FT) for x, y, z in self.verts], [], self.faces)
        me.update()
        for i, pl in enumerate(me.polygons):
            pl.use_smooth = self.smooth[i]
        me.materials.append(get_mat(self.mat))
        ob = bpy.data.objects.new(self.name, me)
        ob["package"] = _pkg_of(self.name)
        ob["below_grade"] = bool(self.below)
        ob["cutaway_part"] = bool(self.cutaway)
        for k, v in (props or {}).items():
            ob[k] = v
        _bpy_link(ob, "BELOWGRADE" if self.below else (self.coll or _collection_for(self.name)))
        return ob


class CurveAcc:
    """Many polylines (feet) -> ONE curve object with a round bevel (cables, pipes, bus)."""
    def __init__(self, name, mat, radius, below=False, coll=None, caps=True):
        self.name, self.mat, self.radius, self.below, self.coll, self.caps = name, mat, radius, below, coll, caps
        self.splines = []

    def add(self, pts):
        if len(pts) >= 2:
            self.splines.append([tuple(p) for p in pts])
        return self

    def add_catenary(self, a, b, sag, n=12):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t
            z = a[2] + (b[2] - a[2]) * t - sag * 4 * t * (1 - t)
            pts.append((x, y, z))
        return self.add(pts)

    def build(self, props=None):
        if not self.splines:
            return None
        allp = [p for s in self.splines for p in s]
        bb = _bbox(allp)
        r = self.radius
        bb = (bb[0] - r, bb[1] - r, bb[2] - r, bb[3] + r, bb[4] + r, bb[5] + r)
        _register(self.name, "curve", bb, self.below, self.coll)
        if not HAVE_BPY:
            return None
        cu = bpy.data.curves.new(self.name, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = self.radius * FT
        cu.bevel_resolution = 3
        cu.fill_mode = "FULL"
        cu.use_fill_caps = self.caps
        for s in self.splines:
            sp = cu.splines.new("POLY")
            sp.points.add(len(s) - 1)
            for i, p in enumerate(s):
                sp.points[i].co = (p[0] * FT, p[1] * FT, p[2] * FT, 1.0)
            sp.use_smooth = True
        cu.materials.append(get_mat(self.mat))
        ob = bpy.data.objects.new(self.name, cu)
        ob["package"] = _pkg_of(self.name)
        ob["below_grade"] = bool(self.below)
        ob["cutaway_part"] = False
        for k, v in (props or {}).items():
            ob[k] = v
        _bpy_link(ob, "BELOWGRADE" if self.below else (self.coll or _collection_for(self.name)))
        return ob


ANCHORS = []

def anchor(key, x, y, z, label, zone=None):
    """Named empty used for callouts.  key -> ANCHOR-<key>."""
    name = "ANCHOR-" + key
    _register(name, "anchor", (x, y, z, x, y, z), False, "ANCHORS")
    ANCHORS.append(dict(name=name, label=label, zone=zone, pos=(x, y, z)))
    if not HAVE_BPY:
        return None
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_type = "PLAIN_AXES"
    ob.empty_display_size = 2.0
    ob.location = (x * FT, y * FT, z * FT)
    ob["label"] = label
    ob["zone"] = zone if zone is not None else 0
    ob["package"] = "ANCHOR"
    _bpy_link(ob, "ANCHORS")
    return ob


def cable_end_caps(name, ends, r=0.25, L=0.8):
    """copper end caps / connectors at cable ends: ends = list of (point, direction)."""
    m = MeshAcc(name, "COPPER")
    for (p, d) in ends:
        dl = math.sqrt(sum(a * a for a in d)) or 1.0
        d = tuple(a / dl for a in d)
        m.cyl_between(p, (p[0] + d[0] * L, p[1] + d[1] * L, p[2] + d[2] * L), r, 10)
    return m.build()


def wall_with_openings(m, x0, x1, y0, y1, z0, z1, openings, axis="x"):
    """Solid wall as boxes leaving rectangular holes.  openings: list of (a0,a1,z0,z1) along the wall axis.
    For axis 'x' the wall runs E-W (y0..y1 is thickness); for 'y' it runs N-S (x0..x1 thickness)."""
    lo, hi = (x0, x1) if axis == "x" else (y0, y1)
    ops = sorted(openings)
    cur = lo
    def put(a0, a1, b0, b1):
        if a1 - a0 < 1e-6 or b1 - b0 < 1e-6:
            return
        if axis == "x":
            m.box(a0, y0, b0, a1, y1, b1)
        else:
            m.box(x0, a0, b0, x1, a1, b1)
    for (a0, a1, oz0, oz1) in ops:
        put(cur, a0, z0, z1)
        put(a0, a1, z0, oz0)
        put(a0, a1, oz1, z1)
        cur = a1
    put(cur, hi, z0, z1)
    return m

# =============================================================================
# LAYOUT  (all ft, derived from PARAMS)
# =============================================================================
SW, SH = P["site_ft"]
HX0, HY0 = P["hall_origin_ft"]
HL, HW, HH = P["hall_ft"]
HX1, HY1 = HX0 + HL, HY0 + HW
GT_X = P["gt_axes_x_ft"]
ST_X = P["st_axis_x_ft"]
HRSG_W, HRSG_L, HRSG_H = P["hrsg_ft"]
HRSG_Y0 = HY1 + P["hrsg_gap_ft"]
HRSG_Y1 = HRSG_Y0 + HRSG_L
STACK_D, STACK_H = P["stack_d_h_ft"]
STACK_Y = HRSG_Y1 + STACK_D / 2 + 4
GSU_L, GSU_W, GSU_H = P["gsu_ft"]
GSU_Y0 = P["gsu_y_ft"]
GSU_X = list(GT_X) + [ST_X]
GANTRY_Y = P["gen_tie_gantry_y_ft"]
ROUTE_X = P["gen_tie_route_x_ft"]
SY_X0, SY_Y0 = P["switchyard_origin_ft"]
SY_L, SY_W = P["switchyard_ft"]
ACC_X0, ACC_Y0 = P["acc_origin_ft"]
ACC_L, ACC_W, ACC_H = P["acc_ft"]
CORR_Y = P["corridor_y_ft"]
CORR_W = P["corridor_w_ft"]
CORR_X0, CORR_X1 = P["corridor_x_ft"]
ROAD_W = P["road_w_ft"]
SPINE_Y = P["spine_road_y_ft"]
FENCE_IN = P["fence_inset_ft"]
PR_IN = P["perimeter_road_inset_ft"]
PAD_T = P["pad_t_ft"]

ZONES = {
    1: ("Switchyard and GSU transformers", (SY_X0, SY_Y0, SY_X0 + SY_L, SY_Y0 + SY_W)),
    2: ("BESS yard", (P["bess_origin_ft"][0], P["bess_origin_ft"][1], P["bess_origin_ft"][0] + 250, P["bess_origin_ft"][1] + 100)),
    3: ("Reel staging, laydown and prefab spine", (P["laydown_origin_ft"][0], P["laydown_origin_ft"][1], P["laydown_origin_ft"][0] + P["laydown_ft"][0], P["laydown_origin_ft"][1] + P["laydown_ft"][1])),
    4: ("Admin building and control room", (P["admin_origin_ft"][0], P["admin_origin_ft"][1], P["admin_origin_ft"][0] + P["admin_ft"][0], P["admin_origin_ft"][1] + P["admin_ft"][1])),
    5: ("Elevated modular e-house", (P["ehouse_origin_ft"][0], P["ehouse_origin_ft"][1], P["ehouse_origin_ft"][0] + P["ehouse_ft"][0], P["ehouse_origin_ft"][1] + P["ehouse_ft"][1])),
    6: ("HRSGs and stacks", (GT_X[0] - HRSG_W / 2, HRSG_Y0, GT_X[-1] + HRSG_W / 2, STACK_Y + STACK_D / 2)),
    7: ("Turbine hall (3 GT + 1 ST)", (HX0, HY0, HX1, HY1)),
    8: ("GT air-inlet filter houses", (GT_X[0] + P["inlet_offset_x_ft"] - 30, GSU_Y0 - 5, GT_X[-1] + 30, HY0)),
    9: ("MCC / VFD / UPS building", (P["mcc_origin_ft"][0], P["mcc_origin_ft"][1], P["mcc_origin_ft"][0] + P["mcc_ft"][0], P["mcc_origin_ft"][1] + P["mcc_ft"][1])),
    10: ("Modular power yard", (P["modular_origin_ft"][0], P["modular_origin_ft"][1], P["modular_origin_ft"][0] + P["modular_yard_ft"][0], P["modular_origin_ft"][1] + P["modular_yard_ft"][1])),
    11: ("Air-cooled condenser", (ACC_X0, ACC_Y0, ACC_X0 + ACC_L, ACC_Y0 + ACC_W)),
    12: ("Chillers and auxiliary cooling towers", (P["chill_origin_ft"][0], P["chill_origin_ft"][1], P["chill_origin_ft"][0] + 240, P["chill_origin_ft"][1] + 130)),
    13: ("Water treatment, tanks and pond", (P["water_origin_ft"][0], P["water_origin_ft"][1], P["water_origin_ft"][0] + 240, P["water_origin_ft"][1] + 290)),
    14: ("Carbon capture block", (P["ccs_origin_ft"][0], P["ccs_origin_ft"][1], P["ccs_origin_ft"][0] + 170, P["ccs_origin_ft"][1] + 330)),
    15: ("Gas metering house and process tanks", (P["gasmet_origin_ft"][0], P["gasmet_origin_ft"][1], P["gasmet_origin_ft"][0] + 150, P["gasmet_origin_ft"][1] + 110)),
    16: ("Site cable corridor and MV distribution", (CORR_X0, CORR_Y, CORR_X1, CORR_Y + CORR_W)),
}

GZ = 0.2          # top of concrete pads / equipment base elevation (ft); gravel is at 0, roads at 0.1
ROADS = []        # (x0, y0, x1, y1) of every road strip, filled by road(); used to keep posts off the asphalt

def on_road(x, y, margin=2.0):
    for (x0, y0, x1, y1) in ROADS:
        if x0 - margin <= x <= x1 + margin and y0 - margin <= y <= y1 + margin:
            return True
    return False

# =============================================================================
# SITE: backdrop, ground, pads, roads, fence, earth grid
# =============================================================================
def pad(name, x0, y0, x1, y1, mat="CONC", top=GZ, t=PAD_T):
    MeshAcc(name, mat).box(x0, y0, top - t, x1, y1, top).build()

def road(name, x0, y0, x1, y1):
    ROADS.append((x0, y0, x1, y1))
    MeshAcc(name, "ASPH").box(x0, y0, -0.5, x1, y1, 0.1).build()
    # centre crack: thin wavy strip along the long axis
    m = MeshAcc(name.replace("ROAD", "ROADCRACK"), "CRACK")
    along_x = (x1 - x0) >= (y1 - y0)
    L = (x1 - x0) if along_x else (y1 - y0)
    n = max(2, int(L / 12))
    pts = []
    for i in range(n + 1):
        t = i / n
        w = 0.6 * math.sin(t * 37.0 + (x0 + y0) * 0.01) + 0.3 * math.sin(t * 91.0)
        if along_x:
            pts.append((x0 + L * t, (y0 + y1) / 2 + w))
        else:
            pts.append(((x0 + x1) / 2 + w, y0 + L * t))
    for a, b in zip(pts[:-1], pts[1:]):
        if along_x:
            m.hexa([(a[0], a[1] - 0.15, 0.1), (b[0], b[1] - 0.15, 0.1), (b[0], b[1] + 0.15, 0.1), (a[0], a[1] + 0.15, 0.1),
                    (a[0], a[1] - 0.15, 0.13), (b[0], b[1] - 0.15, 0.13), (b[0], b[1] + 0.15, 0.13), (a[0], a[1] + 0.15, 0.13)])
        else:
            m.hexa([(a[0] - 0.15, a[1], 0.1), (a[0] + 0.15, a[1], 0.1), (b[0] + 0.15, b[1], 0.1), (b[0] - 0.15, b[1], 0.1),
                    (a[0] - 0.15, a[1], 0.13), (a[0] + 0.15, a[1], 0.13), (b[0] + 0.15, b[1], 0.13), (b[0] - 0.15, b[1], 0.13)])
    m.build()

def fence_run(m, pts, h=None, gap=None):
    h = h or P["fence_h_ft"]
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L / 20))
        for i in range(n + 1):
            t = i / n
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if gap and gap[0] <= x <= gap[1] and abs(y - gap[2]) < 1:
                continue
            m.cyl(x, y, 0, 0.25, h, 6)
        for z in (2.5, 5.0, h - 0.3):
            if gap and abs(a[1] - gap[2]) < 1 and abs(b[1] - gap[2]) < 1:
                # split rail around gate
                m.seg((a[0], a[1], z), (gap[0], a[1], z), 0.12, 5)
                m.seg((gap[1], a[1], z), (b[0], b[1], z), 0.12, 5)
            else:
                m.seg((a[0], a[1], z), (b[0], b[1], z), 0.12, 5)

def build_site():
    E = P["backdrop_extent_ft"]
    MeshAcc("SITE-BACKDROP", "BACKDROP").box(-E, -E, -0.6, SW + E, SH + E, -0.3).build()
    MeshAcc("SITE-GROUND", "GRAVEL").box(0, 0, -0.3, SW, SH, 0.0).build()
    # context strip east of the fence
    MeshAcc("FUELGAS-GROUND", "GRAVEL").box(SW, 420, -0.3, SW + P["outside_strip_ft"], 760, 0.0).build()
    # roads
    ri, rw = PR_IN, ROAD_W / 2
    road("SITE-ROAD-PERIM-S", ri - rw, ri - rw, SW - ri + rw, ri + rw)
    road("SITE-ROAD-PERIM-N", ri - rw, SH - ri - rw, SW - ri + rw, SH - ri + rw)
    road("SITE-ROAD-PERIM-W", ri - rw, ri + rw, ri + rw, SH - ri - rw)
    road("SITE-ROAD-PERIM-E", SW - ri - rw, ri + rw, SW - ri + rw, SH - ri - rw)
    road("SITE-ROAD-SPINE", ri + rw, SPINE_Y - rw, SW - ri - rw, SPINE_Y + rw)
    for i, x in enumerate(P["ns_roads_x_ft"]):
        road("SITE-ROAD-NS-%dS" % (i + 1), x - rw, ri + rw, x + rw, SPINE_Y - rw)
        road("SITE-ROAD-NS-%dN" % (i + 1), x - rw, SPINE_Y + rw, x + rw, SH - ri - rw)
    road("SITE-ROAD-GATE", 188, FENCE_IN, 212, ri - rw)
    # concrete pads per zone (ground tiles)
    for z, (label, r) in ZONES.items():
        if z in (7, 6, 8):          # power block: one common pad
            continue
        if z in (1, 16):            # zone 1 is padded by SWYD-PAD; zone 16 by the corridor pad
            continue
        if z == 13:                 # pad starts north of the pond so the basin is not covered
            wx, wy = P["water_origin_ft"]
            pad("SITE-PAD-Z13", r[0] - 10, wy + P["pond_ft"][1] + 12, r[2] + 10, r[3] + 10)
            continue
        pad("SITE-PAD-Z%02d" % z, r[0] - 10, r[1] - 10, r[2] + 10, r[3] + 10, "GRAVEL" if z in (1, 3, 10) else "CONC")
    pad("SITE-PAD-POWERBLOCK", HX0 - 20, GSU_Y0 - 50, HX1 + 30, STACK_Y + STACK_D / 2 + 20)
    pad("SITE-PAD-CORRIDOR", CORR_X0, CORR_Y - 2, CORR_X1, CORR_Y + CORR_W + 2)
    # fence with gate (south, x 180..220)
    m = MeshAcc("SITE-FENCE", "STEEL_DK")
    f = FENCE_IN
    fence_run(m, [(f, f), (SW - f, f)], gap=(180, 220, f))
    fence_run(m, [(SW - f, f), (SW - f, SH - f), (f, SH - f), (f, f)])
    m.build()
    MeshAcc("SITE-GATEHOUSE", "ENCL").box(224, f - 6, GZ, 236, f + 6, GZ + 10).build()
    pad("SITE-PAD-GATE", 170, f - 8, 240, f + 12)
    # grounding grid (below grade)
    z0, pitch = P["earth_z_pitch_ft"]
    g = CurveAcc("SITE-EARTHGRID", "CABLE", 0.06, below=True)
    x = 50
    while x <= SW - 50:
        g.add([(x, 50, z0), (x, SH - 50, z0)]); x += pitch
    y = 50
    while y <= SH - 50:
        g.add([(50, y, z0), (SW - 50, y, z0)]); y += pitch
    g.build()
    anchor("SITE-EARTHGRID", 1250, 380, z0, "Grounding grid (below grade)", 16)

# =============================================================================
# TURBINE HALL + GT TRAINS + ST TRAIN + STEAM HEADERS
# =============================================================================
WT = 2.0   # wall thickness
CRANE_Z = P["hall_crane_rail_ft"]

def gt_train_geometry(i):
    """y-stations of GT train i (north = exhaust end)."""
    ax = GT_X[i]
    y_wall = HY1 - WT
    y_diff0 = y_wall - 15
    y_enc0 = y_diff0 - 48
    y_gen1 = y_enc0 - 6
    y_gen0 = y_gen1 - 42
    y_exc0 = y_gen0 - 6
    return dict(ax=ax, y_wall=y_wall, y_diff0=y_diff0, y_enc0=y_enc0, y_gen0=y_gen0, y_gen1=y_gen1, y_exc0=y_exc0)

def build_hall():
    x0, y0, x1, y1 = HX0, HY0, HX1, HY1
    MeshAcc("HALL-FLOOR", "CONC").box(x0, y0, GZ - 1.0, x1, y1, GZ + 0.3).build()
    # steel columns along both long walls + end walls
    cols = MeshAcc("HALL-COLUMNS", "STEEL")
    for x in range(int(x0), int(x1) + 1, 30):
        for y in (y0 + 1, y1 - 3):
            cols.box(x - 1, y, GZ, x + 1, y + 2, HH)
    for y in range(int(y0) + 30, int(y1), 30):
        for x in (x0 + 1, x1 - 3):
            cols.box(x, y - 1, GZ, x + 2, y + 1, HH)
    cols.build()
    # roof trusses (N-S) at each column line
    tr = MeshAcc("HALL-TRUSSES", "STEEL")
    for x in range(int(x0), int(x1) + 1, 30):
        tr.box(x - 0.75, y0 + 1, HH - 6, x + 0.75, y1 - 1, HH - 5.5)
        tr.box(x - 0.75, y0 + 1, HH - 0.5, x + 0.75, y1 - 1, HH)
        for k in range(10):
            ya = y0 + 1 + (y1 - y0 - 2) * k / 10
            yb = y0 + 1 + (y1 - y0 - 2) * (k + 1) / 10
            tr.seg((x, ya, HH - 5.75), (x, yb, HH - 0.25), 0.3, 5)
    tr.build()
    # crane rails + bridge crane
    cr = MeshAcc("HALL-CRANE-RAILS", "STEEL_DK")
    for y in (y0 + 4, y1 - 4):
        cr.box(x0 + 2, y - 1.5, CRANE_Z - 3, x1 - 2, y + 1.5, CRANE_Z)
    cr.build()
    bc = MeshAcc("HALL-CRANE", "STEEL")
    cx = HX0 + 250
    for dx in (-4, 4):
        bc.box(cx + dx - 1.5, y0 + 4, CRANE_Z, cx + dx + 1.5, y1 - 4, CRANE_Z + 6)
    bc.box(cx - 8, y0 + 60, CRANE_Z + 6, cx + 8, y0 + 72, CRANE_Z + 10)
    bc.build()
    anchor("HALL-CRANE", cx, y0 + 66, CRANE_Z + 11, "Turbine hall bridge crane", 7)
    # walls: N (exhaust + steam openings), S (inlet duct, IPB, gas openings) separate cutaway part, E (ST exhaust), W
    wn = MeshAcc("HALL-WALL-N", "ENCL")
    ops = [(ax - 11, ax + 11, GZ + 4, GZ + 26) for ax in GT_X] + [(ST_X - 6, ST_X + 6, 44, 56)]
    wall_with_openings(wn, x0, x1, y1 - WT, y1, GZ, HH, ops, axis="x")
    wn.build()
    ws = MeshAcc("HALL-WALL-S", "ENCL", cutaway=True)
    ops = []
    for ax in GT_X:
        ix = ax + P["inlet_offset_x_ft"]
        ops.append((ix - 7.5, ix + 7.5, 49, 63))                # inlet duct
    for ax in GSU_X:
        ops.append((ax - 8, ax + 8, P["ipb_z_ft"] - 4, P["ipb_z_ft"] + 4))   # isophase bus
    ops.append((x1 - 12, x1 - 6, 10, 14))                      # fuel gas header
    wall_with_openings(ws, x0, x1, y0, y0 + WT, GZ, HH, ops, axis="x")
    ws.build()
    we = MeshAcc("HALL-WALL-E", "ENCL")
    wall_with_openings(we, x1 - WT, x1, y0, y1, GZ, HH, [(722, 738, 22, 38)], axis="y")
    we.build()
    MeshAcc("HALL-WALL-W", "ENCL").box(x0, y0, GZ, x0 + WT, y1, HH).build()
    # roof: shallow gable, separate part
    rf = MeshAcc("HALL-ROOF", "ENCL", cutaway=True)
    ym = (y0 + y1) / 2
    ridge = HH + 8
    rf.hexa([(x0 - 1, y0 - 1, HH), (x1 + 1, y0 - 1, HH), (x1 + 1, ym, ridge - 1), (x0 - 1, ym, ridge - 1),
             (x0 - 1, y0 - 1, HH + 1), (x1 + 1, y0 - 1, HH + 1), (x1 + 1, ym, ridge), (x0 - 1, ym, ridge)])
    rf.hexa([(x0 - 1, ym, ridge - 1), (x1 + 1, ym, ridge - 1), (x1 + 1, y1 + 1, HH), (x0 - 1, y1 + 1, HH),
             (x0 - 1, ym, ridge), (x1 + 1, ym, ridge), (x1 + 1, y1 + 1, HH + 1), (x0 - 1, y1 + 1, HH + 1)])
    for x in range(int(x0) + 40, int(x1) - 20, 80):     # roof vents
        rf.box(x, ym - 6, ridge, x + 20, ym + 6, ridge + 4)
    rf.build()
    # interior cable trays along the south wall (power lower, controls upper)
    tp = MeshAcc("HALL-TRAY-POWER", "STEEL")
    tp.tray([(x0 + 6, y0 + 8), (x1 - 6, y0 + 8)], 30, width=3, posts=False)
    tp.build()
    tc = MeshAcc("HALL-TRAY-CONTROL", "STEEL")
    tc.tray([(x0 + 6, y0 + 8), (x1 - 6, y0 + 8)], 33, width=2, posts=False)
    tc.build()
    hb = MeshAcc("HALL-TRAY-BRACKETS", "STEEL_DK")
    for x in range(int(x0) + 6, int(x1) - 5, 10):
        hb.box(x - 0.3, y0 + WT, 29, x + 0.3, y0 + 10, 29.6)
        hb.box(x - 0.3, y0 + WT, 32, x + 0.3, y0 + 9, 32.6)
    hb.build()
    cab = CurveAcc("HALL-CABLES-POWER", "CABLE", 0.12)
    for k in range(6):
        cab.add([(x0 + 6, y0 + 7 + k * 0.4, 30.3), (x1 - 6, y0 + 7 + k * 0.4, 30.3)])
    cab.build()
    cab = CurveAcc("HALL-CABLES-CONTROL", "CABLE", 0.05)
    for k in range(8):
        cab.add([(x0 + 6, y0 + 7.3 + k * 0.2, 33.25), (x1 - 6, y0 + 7.3 + k * 0.2, 33.25)])
    cab.build()
    anchor("HALL-TRAY", x0 + 300, y0 + 8, 34, "Hall cable tray (power below, controls above)", 7)
    # fuel-gas header inside the hall along the south wall, drops to each GT
    fg = CurveAcc("GAS-HEADER-HALL", "STEEL", 0.5)
    fg.add([(x1 - 9, y0 - 2, 12), (x1 - 9, y0 + 5, 12), (x1 - 9, y0 + 5, 20), (GT_X[0], y0 + 5, 20)])
    for ax in GT_X:
        g = gt_train_geometry(GT_X.index(ax))
        fg.add([(ax + 6, y0 + 5, 20), (ax + 6, g["y_enc0"] + 10, 20), (ax + 6, g["y_enc0"] + 10, GZ + 6 + 9)])
    fg.build()
    anchor("ZONE-07", HX0 + 300, (y0 + y1) / 2, HH + 9, ZONES[7][0], 7)


def build_gt(i):
    g = gt_train_geometry(i)
    ax = g["ax"]
    n = i + 1
    pre = "GT-%d-" % n
    # pedestal
    MeshAcc(pre + "PEDESTAL", "CONC").box(ax - 11, g["y_exc0"] - 4, GZ, ax + 11, g["y_diff0"], GZ + 6).build()
    # enclosure (packaged GT) with roof vents
    e = MeshAcc(pre + "ENCLOSURE", "ENCL")
    e.box(ax - 9, g["y_enc0"], GZ + 6, ax + 9, g["y_enc0"] + 48, GZ + 24)
    for k in range(3):
        e.cyl(ax - 4 + k * 4, g["y_enc0"] + 12 + k * 12, GZ + 24, 1.5, 2.0, 12)
    e.build()
    # inlet plenum / silencer on the compressor end (south end of enclosure)
    MeshAcc(pre + "INLET-PLENUM", "ENCL").box(ax - 9, g["y_enc0"], GZ + 24, ax + 9, g["y_enc0"] + 16, GZ + 36).build()
    # inlet duct inside hall: from south wall opening (x = ax+offset, z 49..63) north then east then down into plenum
    ix = ax + P["inlet_offset_x_ft"]
    d = MeshAcc(pre + "INLET-DUCT", "ENCL")
    d.box(ix - 7, HY0 + WT, 49, ix + 7, g["y_enc0"] + 2, 63)
    d.box(ix - 7, g["y_enc0"] + 2, 49, ax + 7, g["y_enc0"] + 16, 63)
    d.box(ax - 7, g["y_enc0"] + 2, GZ + 36, ax + 7, g["y_enc0"] + 16, 49)
    d.build()
    # exhaust diffuser to the north wall opening
    x = MeshAcc(pre + "EXHAUST-DIFFUSER", "STEEL")
    x.hexa([(ax - 7, g["y_diff0"], GZ + 8), (ax + 7, g["y_diff0"], GZ + 8), (ax + 11, g["y_wall"] + WT + 1, GZ + 4), (ax - 11, g["y_wall"] + WT + 1, GZ + 4),
            (ax - 7, g["y_diff0"], GZ + 22), (ax + 7, g["y_diff0"], GZ + 22), (ax + 11, g["y_wall"] + WT + 1, GZ + 26), (ax - 11, g["y_wall"] + WT + 1, GZ + 26)])
    x.build()
    # generator (cylinder body on a frame), exciter, coupling, terminal box
    gen = MeshAcc(pre + "GENERATOR", "ENCL")
    gen.cyl_between((ax, g["y_gen0"], GZ + 14), (ax, g["y_gen1"], GZ + 14), 7.5, 24)
    gen.box(ax - 8, g["y_gen0"] + 2, GZ + 6, ax + 8, g["y_gen1"] - 2, GZ + 14)
    gen.box(ax - 6, g["y_gen0"] + 6, GZ + 21, ax + 6, g["y_gen1"] - 6, GZ + 25)   # cooler top
    gen.build()
    MeshAcc(pre + "COUPLING", "STEEL_DK").cyl_between((ax, g["y_gen1"], GZ + 14), (ax, g["y_enc0"], GZ + 14), 2.5, 12).build()
    MeshAcc(pre + "EXCITER", "ENCL").box(ax - 4, g["y_exc0"], GZ + 6, ax + 4, g["y_gen0"], GZ + 20).build()
    tb = MeshAcc(pre + "TERMINAL-BOX", "ENCL")
    tb.box(ax - 9, g["y_gen0"] + 4, GZ + 6, ax + 9, g["y_gen0"] + 14, GZ + 12)     # line-side terminal enclosure under generator
    tb.box(ax + 9, g["y_gen0"] + 10, GZ + 6, ax + 14, g["y_gen0"] + 16, GZ + 13)   # neutral grounding cubicle
    tb.build()
    # generator leads: flexible links from terminal box down/out to the IPB adaptor
    leads = CurveAcc(pre + "GEN-LEADS", "CABLE", 0.18)
    ends = []
    for k, dx in enumerate((-5, 0, 5)):
        p0 = (ax + dx, g["y_gen0"] + 4, GZ + 9)
        p1 = (ax + dx, g["y_gen0"] - 2, P["ipb_z_ft"])
        leads.add([p0, (ax + dx, g["y_gen0"] + 1, GZ + 9), (ax + dx, g["y_gen0"] - 1, (GZ + 9 + P["ipb_z_ft"]) / 2), p1])
        ends.append((p0, (0, 1, 0)))
        ends.append((p1, (0, -1, 0)))
    leads.build()
    cable_end_caps(pre + "LEAD-CONNECTORS", ends, r=0.28, L=0.9)
    # isophase bus: 3 tubes from generator terminal box south through the wall to the GSU LV bushings
    zb = P["ipb_z_ft"]
    ipb = CurveAcc(pre + "IPB", "STEEL", P["ipb_d_ft"] / 2)
    y_end = GSU_Y0 + GSU_W - 4
    for dx in (-5, 0, 5):
        ipb.add([(ax + dx, g["y_gen0"] - 2, zb), (ax + dx, y_end, zb), (ax + dx, y_end, GZ + GSU_H + 1)])
    # tap to unit auxiliary transformer
    ipb.add([(ax + 5, 615, zb), (ax + 32, 615, zb), (ax + 32, 615, GZ + 8)])
    ipb.add([(ax + 0, 617, zb), (ax + 32, 617, zb - 0.01), (ax + 32, 617, GZ + 8)])
    ipb.add([(ax - 5, 619, zb), (ax + 32, 619, zb), (ax + 32, 619, GZ + 8)])
    ipb.build()
    sup = MeshAcc(pre + "IPB-SUPPORTS", "STEEL_DK")
    y = g["y_gen0"] - 8
    while y > y_end + 4:
        sup.box(ax - 7, y - 0.5, GZ, ax + 7, y + 0.5, zb - 1.5)
        sup.box(ax - 7, y - 1.5, zb - 1.5, ax + 7, y + 1.5, zb - 1.2)
        y -= 20
    sup.build()
    # unit auxiliary transformer (from IPB tap)
    uat = MeshAcc("UAT-%d-TANK" % n, "ENCL")
    uat.box(ax + 24, 605, GZ, ax + 40, 621, GZ + 10)
    for k in range(3):
        uat.cyl(ax + 28 + k * 4, 617, GZ + 10, 0.5, 4, 8)
    uat.build()
    # local GT control module beside the enclosure
    MeshAcc(pre + "CONTROL-MODULE", "ENCL").box(ax - 22, g["y_enc0"] + 8, GZ + 0.3, ax - 14, g["y_enc0"] + 28, GZ + 9.3).build()
    ctl = CurveAcc(pre + "CONTROL-CABLES", "CABLE", 0.05)
    for k in range(4):
        ctl.add([(ax - 18 + k * 0.4, g["y_enc0"] + 28, GZ + 9.3), (ax - 18 + k * 0.4, HY0 + 8, 33.3)])
    ctl.build()
    # anchors
    anchor(pre + "TURBINE", ax, g["y_enc0"] + 30, GZ + 25, "Gas turbine package (enclosed)", 7)
    anchor(pre + "GENERATOR", ax, (g["y_gen0"] + g["y_gen1"]) / 2, GZ + 26, "GT generator", 7)
    anchor(pre + "LEADS", ax + 6, g["y_gen0"] + 1, GZ + 10, "Generator leads and terminal box", 7)
    anchor(pre + "IPB", ax + 6, 660, zb + 2, "Isophase bus duct (generator to GSU)", 7)
    anchor(pre + "INLET-PLENUM", ax, g["y_enc0"] + 8, GZ + 37, "Inlet plenum and silencer", 7)
    anchor(pre + "EXHAUST", ax, g["y_diff0"] + 8, GZ + 27, "Exhaust diffuser to HRSG", 7)
    anchor(pre + "CONTROL-MODULE", ax - 18, g["y_enc0"] + 18, GZ + 10.3, "GT local control module", 7)
    anchor("UAT-%d" % n, ax + 32, 613, GZ + 15, "Unit auxiliary transformer (IPB tap)", 7)
    anchor(pre + "EXCITER", ax, g["y_exc0"] + 3, GZ + 21, "Exciter", 7)


def build_st():
    ax = ST_X
    y0, y1 = 660, 800
    deck = 30
    # tabletop pedestal
    ped = MeshAcc("ST-PEDESTAL", "CONC")
    for x in (ax - 19, ax + 13):
        for y in (y0 + 4, y0 + 40, y0 + 76, y0 + 112, y1 - 10):
            ped.box(x, y, GZ, x + 6, y + 6, deck - 6)
    ped.box(ax - 22.5, y0, deck - 6, ax + 22.5, y1, deck)
    ped.build()
    MeshAcc("ST-HP-CASING", "ENCL").cyl_between((ax, y1 - 25, deck + 6), (ax, y1, deck + 6), 6, 24).build()
    MeshAcc("ST-IP-CASING", "ENCL").cyl_between((ax, y1 - 50, deck + 7), (ax, y1 - 25, deck + 7), 7, 24).build()
    MeshAcc("ST-LP-CASING", "ENCL").box(ax - 15, y1 - 90, deck, ax + 15, y1 - 50, deck + 18).build()
    gen = MeshAcc("ST-GENERATOR", "ENCL")
    gen.cyl_between((ax, y0 + 5, deck + 8), (ax, y1 - 90, deck + 8), 7.5, 24)
    gen.box(ax - 8, y0 + 7, deck, ax + 8, y1 - 92, deck + 8)
    gen.build()
    MeshAcc("ST-EXCITER", "ENCL").box(ax - 4, y0, deck, ax + 4, y0 + 5, deck + 14).build()
    sh = MeshAcc("ST-SHAFT-COVERS", "STEEL_DK")
    sh.cyl_between((ax, y1 - 50, deck + 7), (ax, y1 - 90, deck + 7), 2.5, 12)
    sh.build()
    # LP exhaust duct: from LP casing east side out through the east wall (continues as ACC-STEAM-DUCT)
    ex = CurveAcc("ST-EXHAUST-DUCT", "STEEL", 6)
    ex.add([(ax + 15, 730, 22), (ax + 40, 730, 22), (ax + 60, 730, 30), (HX1 + 1, 730, 30)])
    ex.build()
    MeshAcc("ST-EXHAUST-SUPPORTS", "STEEL_DK").box(ax + 34, 727, GZ, ax + 36, 733, 16).box(ax + 64, 727, GZ, ax + 66, 733, 24).build()
    # ST GSU isophase bus
    zb = P["ipb_z_ft"]
    ipb = CurveAcc("ST-IPB", "STEEL", P["ipb_d_ft"] / 2)
    y_end = GSU_Y0 + GSU_W - 4
    for dx in (-5, 0, 5):
        ipb.add([(ax + dx, y0 + 4, deck + 2), (ax + dx, y0 - 6, deck + 2), (ax + dx, y0 - 6, zb), (ax + dx, y_end, zb), (ax + dx, y_end, GZ + GSU_H + 1)])
    ipb.build()
    sup = MeshAcc("ST-IPB-SUPPORTS", "STEEL_DK")
    y = y0 - 14
    while y > y_end + 4:
        sup.box(ax - 7, y - 0.5, GZ, ax + 7, y + 0.5, zb - 1.5)
        sup.box(ax - 7, y - 1.5, zb - 1.5, ax + 7, y + 1.5, zb - 1.2)
        y -= 20
    sup.build()
    leads = CurveAcc("ST-GEN-LEADS", "CABLE", 0.18)
    ends = []
    for dx in (-5, 0, 5):
        p0 = (ax + dx, y0 + 8, deck + 1)
        p1 = (ax + dx, y0 + 4, deck + 2)
        leads.add([p0, (ax + dx, y0 + 6, deck + 0.5), p1])
        ends.append((p0, (0, 1, 0))); ends.append((p1, (0, -1, 0)))
    leads.build()
    cable_end_caps("ST-LEAD-CONNECTORS", ends, r=0.28, L=0.9)
    anchor("ST-TURBINE", ax, y1 - 40, deck + 19, "Steam turbine (HP / IP / LP)", 7)
    anchor("ST-GENERATOR", ax, y0 + 45, deck + 17, "Steam turbine generator", 7)
    anchor("ST-PEDESTAL", ax - 22, y0 + 60, deck + 1, "ST tabletop pedestal", 7)
    anchor("ST-EXHAUST-DUCT", ax + 50, 730, 37, "LP exhaust duct to ACC", 7)
    anchor("ST-IPB", ax + 6, 640, zb + 2, "ST isophase bus to GSU", 7)


def build_steam_headers():
    """HP and hot-reheat headers collect from the three HRSGs and enter the hall at the ST bay."""
    hp = CurveAcc("STEAM-HP-HEADER", "INSUL", 1.5)
    rh = CurveAcc("STEAM-RH-HEADER", "INSUL", 1.75)
    yh = HY1 + 12
    for ax in GT_X:
        hp.add([(ax - 20, HRSG_Y0 + 60, 160), (ax - 20, HRSG_Y0 - 2, 160), (ax - 20, HRSG_Y0 - 2, 50), (ax - 20, yh, 50)])
        rh.add([(ax - 30, HRSG_Y0 + 60, 150), (ax - 30, HRSG_Y0 - 2, 150), (ax - 30, HRSG_Y0 - 2, 44), (ax - 30, yh + 6, 44)])
    hp.add([(GT_X[0] - 20, yh, 50), (ST_X, yh, 50), (ST_X, HY1 - WT - 1, 50), (ST_X, 790, 50), (ST_X, 790, 42)])
    rh.add([(GT_X[0] - 30, yh + 6, 44), (ST_X + 4, yh + 6, 44), (ST_X + 4, HY1 - WT - 1, 44), (ST_X + 4, 770, 44), (ST_X + 4, 770, 40)])
    hp.build(); rh.build()
    sup = MeshAcc("STEAM-HEADER-SUPPORTS", "STEEL_DK")
    for x in range(int(GT_X[0]) - 35, int(ST_X) + 1, 65):      # half the unit pitch: clears the exhaust ducts
        sup.box(x - 1, yh - 1, GZ, x + 1, yh + 1, 42)
        sup.box(x - 1, yh - 3, 42, x + 1, yh + 9, 43)
    sup.build()
    anchor("STEAM-HEADERS", (GT_X[1] + ST_X) / 2, yh + 3, 53, "HP and reheat steam headers (3 HRSGs to 1 ST)", 6)

# =============================================================================
# HRSG + STACK, INLET FILTER HOUSES
# =============================================================================
def build_hrsg(i):
    ax = GT_X[i]
    n = i + 1
    pre = "HRSG-%d-" % n
    hw = HRSG_W / 2
    y0, y1 = HRSG_Y0, HRSG_Y1
    cas_h = 150.0
    # exhaust duct from hall north wall to HRSG inlet
    MeshAcc(pre + "EXHAUST-DUCT", "STEEL").box(ax - 11, HY1 - 1, GZ + 4, ax + 11, y0 + 1, GZ + 26).build()
    # inlet transition (wedge) 22x22 -> 92 x 150 over 30 ft
    t = MeshAcc(pre + "INLET-TRANSITION", "STEEL")
    t.hexa([(ax - 11, y0, GZ + 4), (ax + 11, y0, GZ + 4), (ax + hw, y0 + 30, GZ + 8), (ax - hw, y0 + 30, GZ + 8),
            (ax - 11, y0, GZ + 26), (ax + 11, y0, GZ + 26), (ax + hw, y0 + 30, cas_h), (ax - hw, y0 + 30, cas_h)])
    t.build()
    # main casing on support steel
    c = MeshAcc(pre + "CASING", "ENCL")
    c.box(ax - hw, y0 + 30, GZ + 8, ax + hw, y1 - 24, cas_h)
    c.build()
    # external structural columns + girts
    st = MeshAcc(pre + "STEEL", "STEEL")
    for y in range(int(y0) + 30, int(y1) - 23, 20):
        for x in (ax - hw - 1.5, ax + hw + 1.5):
            st.box(x - 1, y - 1, GZ, x + 1, y + 1, HRSG_H)
    for z in (40, 80, 120, 160, HRSG_H - 1):
        for x in (ax - hw - 1.5, ax + hw + 1.5):
            st.box(x - 1, y0 + 30, z - 1, x + 1, y1 - 24, z)
    # roof deck frame at envelope height
    st.build()
    # steam drums on top (HP, IP, LP) + downcomers
    d = MeshAcc(pre + "DRUMS", "INSUL")
    for k, (dy, r) in enumerate(((y0 + 50, 4.5), (y0 + 85, 3.5), (y0 + 115, 3.0))):
        d.cyl_between((ax - 30, dy, cas_h + 9), (ax + 30, dy, cas_h + 9), r, 20)
        d.box(ax - 20, dy - 2, cas_h, ax - 16, dy + 2, cas_h + 9)
        d.box(ax + 16, dy - 2, cas_h, ax + 20, dy + 2, cas_h + 9)
    d.build()
    dc = CurveAcc(pre + "DOWNCOMERS", "INSUL", 1.0)
    for dy in (y0 + 50, y0 + 85, y0 + 115):
        dc.add([(ax + 30, dy, cas_h + 9), (ax + hw + 4, dy, cas_h + 9), (ax + hw + 4, dy, GZ + 20)])
    dc.build()
    # outlet transition to the stack
    o = MeshAcc(pre + "OUTLET-TRANSITION", "STEEL")
    r = STACK_D / 2
    o.hexa([(ax - hw, y1 - 24, GZ + 8), (ax + hw, y1 - 24, GZ + 8), (ax + r, y1, GZ + 8), (ax - r, y1, GZ + 8),
            (ax - hw, y1 - 24, cas_h), (ax + hw, y1 - 24, cas_h), (ax + r, y1, 60), (ax - r, y1, 60)])
    o.build()
    # stack
    s = MeshAcc(pre + "STACK", "ENCL")
    s.cyl(ax, STACK_Y, GZ, r, STACK_H, 40)
    s.build()
    pl = MeshAcc(pre + "STACK-PLATFORMS", "STEEL")
    for z in (60, 140, 220, STACK_H - 8):
        pl.cyl(ax, STACK_Y, z, r + 3.5, 0.4, 40)
        for k in range(24):
            a = 2 * math.pi * k / 24
            pl.cyl(ax + (r + 3.3) * math.cos(a), STACK_Y + (r + 3.3) * math.sin(a), z, 0.12, 3.5, 5)
    pl.cyl_between((ax + r + 1.2, STACK_Y, GZ), (ax + r + 1.2, STACK_Y, STACK_H - 8), 1.2, 10, caps=False)   # ladder cage
    pl.build()
    # CEMS / damper tap toward CCS collector
    MeshAcc(pre + "CCS-TAP", "STEEL").box(ax - 8, STACK_Y + r - 2, P["flue_duct_z_ft"] - 8, ax + 8, STACK_Y + r + 8, P["flue_duct_z_ft"] + 8).build()
    # stair tower (lattice) on the east side of the casing
    MeshAcc(pre + "STAIR-TOWER", "STEEL").lattice(ax + hw + 10, y0 + 60, GZ, HRSG_H, 10, 10, r=0.4, panels=10).build()
    # anchors
    anchor(pre + "CASING", ax, (y0 + y1) / 2, cas_h + 1, "HRSG casing (triple-pressure, reheat)", 6)
    anchor(pre + "STACK", ax, STACK_Y, STACK_H + 2, "HRSG exhaust stack", 6)
    anchor(pre + "DRUMS", ax, y0 + 50, cas_h + 14.5, "Steam drums", 6)
    anchor(pre + "INLET-TRANSITION", ax, y0 + 15, cas_h / 2 + 30, "Inlet transition duct from GT exhaust", 6)
    anchor(pre + "OUTLET", ax, y1 - 12, 62, "Outlet transition to stack", 6)
    anchor(pre + "STAIR-TOWER", ax + hw + 10, y0 + 60, HRSG_H + 2, "Access stair tower", 6)
    anchor(pre + "CCS-TAP", ax, STACK_Y + r + 9, P["flue_duct_z_ft"] + 9, "Flue-gas take-off and damper to CCS", 6)
    if i == 1:
        anchor("ZONE-06", ax, STACK_Y, STACK_H + 6, ZONES[6][0], 6)


def build_inlet(i):
    ax = GT_X[i]
    n = i + 1
    pre = "INLET-%d-" % n
    L, W, H = P["inlet_ft"]
    base = P["inlet_base_ft"]
    cx = ax + P["inlet_offset_x_ft"]
    cy = 590
    x0, x1 = cx - L / 2, cx + L / 2
    y0, y1 = cy - W / 2, cy + W / 2
    h = MeshAcc(pre + "FILTER-HOUSE", "ENCL")
    h.box(x0, y0, base, x1, y1, base + H)
    h.build()
    hoods = MeshAcc(pre + "WEATHER-HOODS", "STEEL")
    for k in range(6):
        hx = x0 + 4 + k * 9
        hoods.box(hx, y0 - 3, base + 2, hx + 7, y0, base + H - 3)      # south face
        hoods.box(hx, y1, base + 2, hx + 7, y1 + 3, base + H - 3)      # north face
    hoods.build()
    s = MeshAcc(pre + "SUPPORT-STEEL", "STEEL")
    for x in (x0 + 2, (x0 + x1) / 2, x1 - 2):
        for y in (y0 + 2, y1 - 2):
            s.box(x - 1, y - 1, GZ, x + 1, y + 1, base)
    for x in (x0 + 2, x1 - 2):
        s.seg((x, y0 + 2, GZ), (x, y1 - 2, base), 0.4, 6)
        s.seg((x, y1 - 2, GZ), (x, y0 + 2, base), 0.4, 6)
    s.box(x0, y0, base - 2, x1, y1, base)                      # support deck
    s.build()
    MeshAcc(pre + "STAIR-TOWER", "STEEL").lattice(x0 - 6, cy, GZ, base + 2, 8, 8, r=0.35, panels=3).build()
    # duct: plenum on the north face -> silencer -> 14x14 duct to the hall wall at z 49..63
    d = MeshAcc(pre + "INLET-DUCT", "ENCL")
    d.hexa([(cx - 20, y1, base + 2), (cx + 20, y1, base + 2), (cx + 7, y1 + 10, 49), (cx - 7, y1 + 10, 49),
            (cx - 20, y1, base + H - 2), (cx + 20, y1, base + H - 2), (cx + 7, y1 + 10, 63), (cx - 7, y1 + 10, 63)])
    d.box(cx - 8, y1 + 10, 48, cx + 8, y1 + 22, 64)            # silencer section
    d.box(cx - 7, y1 + 22, 49, cx + 7, HY0 + 1, 63)            # duct to wall
    d.build()
    ds = MeshAcc(pre + "DUCT-SUPPORTS", "STEEL_DK")
    ds.box(cx - 9, y1 + 16, GZ, cx - 7, y1 + 18, 48).box(cx + 7, y1 + 16, GZ, cx + 9, y1 + 18, 48)
    ds.box(cx - 9, HY0 - 8, GZ, cx - 7, HY0 - 6, 49).box(cx + 7, HY0 - 8, GZ, cx + 9, HY0 - 6, 49)
    ds.build()
    anchor(pre + "FILTER-HOUSE", cx, cy, base + H + 1, "Elevated inlet air filter house", 8)
    anchor(pre + "WEATHER-HOODS", cx, y0 - 3, base + H - 4, "Weather hoods / filter stages", 8)
    anchor(pre + "INLET-DUCT", cx, y1 + 26, 64, "Inlet duct and silencer into the hall", 8)
    anchor(pre + "SUPPORT-STEEL", x1 - 2, y0 + 2, base / 2, "Support steel and bracing", 8)
    if i == 1:
        anchor("ZONE-08", cx, cy, base + H + 6, ZONES[8][0], 8)

# =============================================================================
# GSU TRANSFORMERS, GEN-TIE (OVERHEAD + UNDERGROUND OPTION), SWITCHYARD
# =============================================================================
def build_gsu(i):
    ax = GSU_X[i]
    n = i + 1
    pre = "GSU-%d-" % n
    y0, y1 = GSU_Y0, GSU_Y0 + GSU_W
    hx = GSU_L / 2
    tank = MeshAcc(pre + "TANK", "ENCL")
    tank.box(ax - hx + 8, y0 + 2, GZ + 1, ax + hx - 8, y1 - 2, GZ + GSU_H - 6)
    tank.cyl_between((ax - hx + 8, (y0 + y1) / 2, GZ + GSU_H - 2), (ax + hx - 8, (y0 + y1) / 2, GZ + GSU_H - 2), 3.0, 16)   # conservator
    tank.box(ax - hx + 6, y0, GZ, ax + hx - 6, y1, GZ + 1)    # base frame
    tank.build()
    rad = MeshAcc(pre + "RADIATORS", "STEEL")
    for side in (-1, 1):
        for k in range(8):
            y = y0 + 4 + k * 3.2
            x = ax + side * (hx - 8)
            rad.box(min(x, x + side * 7), y, GZ + 4, max(x, x + side * 7), y + 1.2, GZ + GSU_H - 10)
        rad.cyl(ax + side * (hx - 4), y0 + 8, GZ + GSU_H - 9, 2.5, 1.5, 12)     # cooler fans
        rad.cyl(ax + side * (hx - 4), y1 - 8, GZ + GSU_H - 9, 2.5, 1.5, 12)
    rad.build()
    b = MeshAcc(pre + "BUSHINGS", "PORCELAIN")
    for dx in (-5, 0, 5):     # LV (north side, toward hall) - IPB lands here
        b.cyl(ax + dx, y1 - 4, GZ + GSU_H - 6, 0.8, 7, 10)
    for dx in (-8, 0, 8):     # HV 230 kV on top
        b.cyl(ax + dx, y0 + 8, GZ + GSU_H - 6, 1.2, 10, 10)
        b.cyl(ax + dx, y0 + 8, GZ + GSU_H - 6, 1.9, 0.6, 10)
    b.build()
    fw = MeshAcc(pre + "FIREWALLS", "CONC")
    for x in (ax - hx - 6, ax + hx + 5):
        fw.box(x, y0 - 6, GZ, x + 1.5, y1 + 6, GZ + 38)
    fw.build()
    curb = MeshAcc(pre + "OIL-CONTAINMENT", "CONC")
    for (x0, y0c, x1, y1c) in ((ax - hx - 4, y0 - 5, ax + hx + 4, y0 - 4), (ax - hx - 4, y1 + 4, ax + hx + 4, y1 + 5),
                               (ax - hx - 4, y0 - 5, ax - hx - 3, y1 + 5), (ax + hx + 3, y0 - 5, ax + hx + 4, y1 + 5)):
        curb.box(x0, y0c, GZ, x1, y1c, GZ + 1.5)
    curb.build()
    # HV jumpers from bushings up to the gen-tie gantry beam (droppers)
    j = CurveAcc(pre + "HV-JUMPERS", "CABLE", 0.12)
    for k, dx in enumerate((-8, 0, 8)):
        j.add_catenary((ax + dx, y0 + 8, GZ + GSU_H + 4), (ax + dx, GANTRY_Y + 2, P["gen_tie_h_ft"] - 6), 3.0, 8)
    j.build()
    # surge arresters + earth risers with copper connectors
    sa = MeshAcc(pre + "ARRESTERS", "PORCELAIN")
    for dx in (-8, 0, 8):
        sa.cyl(ax + dx, y0 - 3, GZ, 0.5, 12, 8)
    sa.build()
    gr = CurveAcc(pre + "GROUND-RISERS", "CABLE", 0.08)
    ends = []
    for x in (ax - hx + 6, ax + hx - 6):
        gr.add([(x, y0 - 0.5, P["earth_z_pitch_ft"][0]), (x, y0 - 0.5, GZ + 1)])
        ends.append(((x, y0 - 0.5, GZ + 1), (0, 0, 1)))
    gr.build()
    cable_end_caps(pre + "GROUND-CONNECTORS", ends, r=0.15, L=0.4)
    lbl = "ST generator step-up transformer" if i == 3 else "GT-%d generator step-up transformer (18/230 kV)" % n
    anchor(pre + "TANK", ax, (y0 + y1) / 2, GZ + GSU_H + 2, lbl, 1)
    anchor(pre + "HV-BUSHINGS", ax, y0 + 8, GZ + GSU_H + 5, "230 kV HV bushings", 1)
    anchor(pre + "LV-BUSHINGS", ax, y1 - 4, GZ + GSU_H + 2, "LV bushings (IPB termination)", 1)
    anchor(pre + "FIREWALL", ax + hx + 6, (y0 + y1) / 2, GZ + 39, "Transformer fire wall", 1)
    anchor(pre + "ARRESTER", ax, y0 - 3, GZ + 13, "Surge arresters", 1)


def build_gentie():
    H = P["gen_tie_h_ft"]
    gy = GANTRY_Y
    # take-off gantry along the GSU row
    g = MeshAcc("GENTIE-GANTRY", "STEEL")
    for x in (600, 725, 850, 975, 1100):
        g.lattice(x, gy, GZ, H, 8, 4, r=0.35, panels=4)
    g.box(600, gy - 2, H - 4, 1100, gy + 2, H)
    g.box(600, gy - 2, H - 22, 1100, gy + 2, H - 18)     # lower strain-bus beam
    g.build()
    ins = MeshAcc("GENTIE-INSULATORS", "PORCELAIN")
    for x in range(610, 1100, 30):
        ins.cyl(x, gy, H - 8, 0.45, 4, 8)
    ins.build()
    # strain buses on the gantry (two circuits: A = GT-1+GT-2, B = GT-3+ST), phase spacing 12 ft along y
    bus = CurveAcc("GENTIE-STRAIN-BUS", "CABLE", 0.12)
    for k, dy in enumerate((-4, 0, 4)):
        bus.add([(602, gy + dy, H - 8), (860, gy + dy, H - 8)])
        bus.add([(860, gy + dy, H - 24), (1098, gy + dy, H - 24)])
    bus.build()
    # towers along the route: T1 near the gantry, then north along ROUTE_X
    towers = [(ROUTE_X, 500), (ROUTE_X, 700), (ROUTE_X, 900), (ROUTE_X, 1020)]
    t = MeshAcc("GENTIE-TOWERS", "STEEL")
    arms = []
    for (x, y) in towers:
        t.lattice(x, y, GZ, 92, 22, 6, r=0.5, panels=6)
        for z in (62, 76):
            t.box(x - 14, y - 1, z - 1, x + 14, y + 1, z)      # cross-arms (double circuit, 2 levels)
        for dx in (-13, 13):
            for z in (62, 76):
                t.cyl(x + dx, y, z - 5, 0.4, 5, 8)
        arms.append((x, y))
    t.build()
    # conductors: 6 phases (2 circuits x 3) + shield wire, catenaries between attachment points
    cond = CurveAcc("GENTIE-CONDUCTORS", "CABLE", 0.09)
    chain = [(602, gy, H - 8)] + [(x, y, 0) for (x, y) in towers]
    for ci, dx in enumerate((-13, 13)):
        for pi, z in enumerate((62, 76, 62)):
            zc = z if pi != 2 else 76 - 7
            prev = (602 if ci == 0 else 860, gy + (pi - 1) * 4, H - 8 if ci == 0 else H - 24)
            for (x, y) in towers:
                p = (x + dx, y, (62, 76, 69)[pi] - 5)
                sag = 6 + 0.02 * math.hypot(p[0] - prev[0], p[1] - prev[1])
                cond.add_catenary(prev, p, sag, 10)
                prev = p
            # into the switchyard dead-end
            de = (405 + pi * 12 + ci * 6, 1090, 56)
            cond.add_catenary(prev, de, 6, 10)
    shield = CurveAcc("GENTIE-SHIELD-WIRE", "CABLE", 0.05)
    prev = (602, gy, H)
    for (x, y) in towers:
        shield.add_catenary(prev, (x, y, 92), 4, 8); prev = (x, y, 92)
    shield.add_catenary(prev, (425, 1090, 62), 3, 8)
    cond.build(); shield.build()
    # underground HV getaway option: sealing-end structures at both ends, duct bank, manholes, cables (below grade)
    for (name, x, y, ang) in (("A", 585, 528, 0), ("B", 430, 1050, 0)):
        se = MeshAcc("GENTIE-UG-TERMINATION-" + name, "STEEL")
        se.box(x - 6, y - 2, GZ, x + 6, y + 2, GZ + 12)
        for k in (-4, 0, 4):
            se.box(x + k - 0.6, y - 0.6, GZ, x + k + 0.6, y + 0.6, GZ + 12)
        se.build()
        pc = MeshAcc("GENTIE-UG-SEALING-ENDS-" + name, "PORCELAIN")
        for k in (-4, 0, 4):
            pc.cyl(x + k, y, GZ + 12, 0.9, 9, 10)
        pc.build()
        MeshAcc("GENTIE-UG-LINKBOX-" + name, "ENCL").box(x + 8, y - 1.5, GZ, x + 11, y + 1.5, GZ + 3).build()
    route = [(585, 528), (442, 528), (442, 1050), (430, 1050)]
    db = MeshAcc("GENTIE-UG-DUCTBANK", "DUCT", below=True)
    for a, b in zip(route[:-1], route[1:]):
        x0, x1 = min(a[0], b[0]) - 3, max(a[0], b[0]) + 3
        y0, y1 = min(a[1], b[1]) - 3, max(a[1], b[1]) + 3
        db.box(x0, y0, -9, x1, y1, -5)
    db.build()
    cab = CurveAcc("GENTIE-UG-CABLES", "CABLE", 0.3, below=True)
    for k in (-1.5, 0, 1.5):
        pts = [(585 + k, 528, GZ + 12)] + [(x + (k if a_i > 0 else 0), y + (k if a_i == 0 else 0), -7) for a_i, (x, y) in enumerate(route)] + [(430, 1050 + k, GZ + 12)]
        cab.add(pts)
    cab.build()
    mh = MeshAcc("GENTIE-UG-MANHOLES", "CONC", below=True)
    cov = MeshAcc("GENTIE-UG-MANHOLE-COVERS", "STEEL_DK")
    for y in (640, 840, 1040):
        mh.box(442 - 4, y - 4, -10, 442 + 4, y + 4, GZ)
        cov.cyl(442, y, GZ, 1.6, 0.2, 16)
    mh.build(); cov.build()
    anchor("GENTIE-GANTRY", 850, gy, H + 2, "Gen-tie take-off gantry and strain buses", 1)
    anchor("GENTIE-TOWER", ROUTE_X, 700, 94, "230 kV double-circuit gen-tie towers", 1)
    anchor("GENTIE-CONDUCTORS", ROUTE_X + 13, 800, 62, "Overhead gen-tie conductors", 1)
    anchor("GENTIE-UG-TERMINATION", 585, 528, GZ + 22, "Underground option: cable sealing ends (plant end)", 1)
    anchor("GENTIE-UG-TERMINATION-B", 430, 1050, GZ + 22, "Underground option: sealing ends (switchyard end)", 1)
    anchor("GENTIE-UG-DUCTBANK", 442, 780, -5, "Underground option: 230 kV XLPE duct bank (below grade)", 1)
    anchor("GENTIE-UG-MANHOLE", 442, 840, GZ + 0.5, "Underground option: splice manhole", 1)
    anchor("GENTIE-UG-LINKBOX", 594, 528, GZ + 3.5, "Sheath link box", 1)


def build_switchyard():
    x0, y0 = SY_X0, SY_Y0
    x1, y1 = x0 + SY_L, y0 + SY_W
    pad("SWYD-PAD", x0, y0, x1, y1, "GRAVEL", top=GZ, t=1.0)
    f = MeshAcc("SWYD-FENCE", "STEEL_DK")
    fence_run(f, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], h=8)
    f.build()
    # line dead-end gantry (from gen-tie) and grid exit gantry (north)
    g = MeshAcc("SWYD-DEADEND", "STEEL")
    for x in (395, 450):
        g.lattice(x, 1090, GZ, 60, 6, 3, r=0.3, panels=3)
    g.box(395, 1088, 56, 450, 1092, 60)
    for x in (200, 300):
        g.lattice(x, y1 - 10, GZ, 60, 6, 3, r=0.3, panels=3)
    g.box(200, y1 - 12, 56, 300, y1 - 8, 60)
    g.build()
    # two main buses (E-W) on post insulators
    bus = CurveAcc("SWYD-BUS", "STEEL", 0.35)
    posts = MeshAcc("SWYD-BUS-SUPPORTS", "STEEL")
    ins = MeshAcc("SWYD-INSULATORS", "PORCELAIN")
    for yb in (1130, 1230):
        for dy in (-15, 0, 15):
            bus.add([(x0 + 20, yb + dy, 40), (x1 - 20, yb + dy, 40)])
        for x in range(int(x0) + 30, int(x1) - 20, 60):
            posts.box(x - 1, yb - 17, GZ, x + 1, yb + 17, 30)
            posts.box(x - 1, yb - 1, GZ, x + 1, yb + 1, 30)
            for dy in (-15, 0, 15):
                ins.cyl(x, yb + dy, 30, 0.6, 10, 8)
    # bays between the buses: 3 bays (line, GSU circuits A/B... generic) each 60 ft
    brk = MeshAcc("SWYD-BREAKERS", "ENCL")
    dis = MeshAcc("SWYD-DISCONNECTS", "STEEL")
    ct = MeshAcc("SWYD-CT-CVT", "PORCELAIN")
    jump = CurveAcc("SWYD-JUMPERS", "CABLE", 0.1)
    for bx in (170, 250, 330, 410):
        if bx > x1 - 20:
            continue
        for dy in (-15, 0, 15):
            # breaker: dead-tank cylinder on stand
            brk.cyl_between((bx - 4, 1180 + dy, GZ + 8), (bx + 4, 1180 + dy, GZ + 8), 2.0, 14)
            brk.box(bx - 3, 1180 + dy - 1, GZ, bx + 3, 1180 + dy + 1, GZ + 8)
            ins.cyl(bx - 2.5, 1180 + dy, GZ + 10, 0.6, 8, 8)
            ins.cyl(bx + 2.5, 1180 + dy, GZ + 10, 0.6, 8, 8)
            # disconnects either side
            for yd in (1152, 1208):
                dis.box(bx - 4, yd + dy - 0.5, GZ, bx + 4, yd + dy + 0.5, GZ + 14)
                for xd in (-3, 0, 3):
                    ins.cyl(bx + xd, yd + dy, GZ + 14, 0.5, 6, 8)
                dis.box(bx - 3, yd + dy - 0.2, GZ + 20, bx + 3, yd + dy + 0.2, GZ + 20.4)
            # CTs
            ct.cyl(bx, 1196 + dy, GZ, 0.9, 16, 10)
            # jumpers from bus to disconnect to breaker to bus
            jump.add_catenary((bx, 1130 + dy, 40), (bx, 1152 + dy, GZ + 20.5), 1.5, 6)
            jump.add_catenary((bx, 1152 + dy, GZ + 20.5), (bx - 2.5, 1180 + dy, GZ + 18), 1.0, 6)
            jump.add_catenary((bx + 2.5, 1180 + dy, GZ + 18), (bx, 1196 + dy, GZ + 16), 0.6, 6)
            jump.add_catenary((bx, 1196 + dy, GZ + 16), (bx, 1208 + dy, GZ + 20.5), 0.8, 6)
            jump.add_catenary((bx, 1208 + dy, GZ + 20.5), (bx, 1230 + dy, 40), 1.5, 6)
    # CVTs on the line entries
    for x in (405, 417, 429, 441):
        ct.cyl(x, 1105, GZ, 0.8, 18, 10)
    for x in (230, 250, 270):
        ct.cyl(x, y1 - 30, GZ, 0.8, 18, 10)
        jump.add_catenary((x, 1230, 40), (x, y1 - 10, 56), 2.0, 6)
    bus.build(); posts.build(); ins.build(); brk.build(); dis.build(); ct.build(); jump.build()
    # lightning masts, control house, station-service transformer
    lm = MeshAcc("SWYD-LIGHTNING-MASTS", "STEEL")
    for (x, y) in ((x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x0 + 10, y1 - 10), (x1 - 10, y1 - 10)):
        lm.cyl(x, y, GZ, 0.8, 95, 8, r2=0.3)
    lm.build()
    MeshAcc("SWYD-CONTROL-HOUSE", "ENCL").box(x0 + 20, y1 - 45, GZ, x0 + 50, y1 - 25, GZ + 12).build()
    ss = MeshAcc("SWYD-STATION-SERVICE-TX", "ENCL")
    ss.box(x0 + 60, y0 + 15, GZ, x0 + 75, y0 + 25, GZ + 10)
    for k in range(3):
        ss.cyl(x0 + 63 + k * 4.5, y0 + 20, GZ + 10, 0.4, 3, 8)
    ss.build()
    # grid line leaving north: one lattice tower outside the fence
    MeshAcc("SWYD-GRID-TOWER", "STEEL").lattice(250, SH + 70, 0, 110, 26, 6, r=0.5, panels=7).build()
    ex = CurveAcc("SWYD-GRID-LINE", "CABLE", 0.09)
    for k, x in enumerate((230, 250, 270)):
        ex.add_catenary((x, y1 - 10, 56), (x - 20 + k * 20, SH + 70, 90), 8, 10)
        ex.add_catenary((x - 20 + k * 20, SH + 70, 90), (x - 40 + k * 40, SH + 600, 90), 14, 10)
    ex.build()
    anchor("SWYD-BUS", (x0 + x1) / 2, 1130, 42, "230 kV main buses", 1)
    anchor("SWYD-BREAKER", 250, 1180, GZ + 12, "230 kV circuit breakers", 1)
    anchor("SWYD-DISCONNECT", 250, 1152, GZ + 21, "Disconnect switches", 1)
    anchor("SWYD-DEADEND", 422, 1090, 62, "Gen-tie dead-end structure", 1)
    anchor("SWYD-GRID-EXIT", 250, y1 - 10, 62, "Grid line exit gantry (230 kV)", 1)
    anchor("SWYD-CONTROL-HOUSE", x0 + 35, y1 - 35, GZ + 13, "Switchyard control house", 1)
    anchor("SWYD-STATION-SERVICE", x0 + 67, y0 + 20, GZ + 14, "Station service transformer", 1)
    anchor("SWYD-CT", 250, 1196, GZ + 17, "Current transformers / CVTs", 1)
    anchor("ZONE-01", (x0 + x1) / 2, (y0 + y1) / 2, 44, ZONES[1][0], 1)

# =============================================================================
# ELECTRICAL BUILDINGS: E-HOUSE (elevated modular), MCC/VFD/UPS, ADMIN
# =============================================================================
def cabinet_row(m, x0, y0, z0, n, w, d, h, along="x", door_side=None, detail=True):
    """row of n cabinets: body, proud door panel with handle and vent slots, top hood and plinth."""
    for k in range(n):
        if along == "x":
            bx0, bx1, by0, by1 = x0 + k * w, x0 + (k + 1) * w - 0.1, y0, y0 + d
        else:
            bx0, bx1, by0, by1 = x0, x0 + d, y0 + k * w, y0 + (k + 1) * w - 0.1
        m.box(bx0, by0, z0 + 0.3, bx1, by1, z0 + (h - 0.25 if detail else h))
        if not detail:
            continue
        m.box(bx0 - 0.03, by0 - 0.03, z0, bx1 + 0.03, by1 + 0.03, z0 + 0.3)              # plinth
        m.box(bx0 - 0.05, by0 - 0.05, z0 + h - 0.25, bx1 + 0.05, by1 + 0.05, z0 + h)     # top hood
        # door panel on the operating face(s): -y for x-rows, -x for y-rows (and the opposite face for double-sided rows)
        if along == "x":
            e = 0.06
            for (fy, sg) in ((by0, -1), ) if door_side != "both" else ((by0, -1), (by1, 1)):
                yy0, yy1 = (fy - e, fy) if sg < 0 else (fy, fy + e)
                m.box(bx0 + 0.12, yy0, z0 + 0.55, bx1 - 0.12, yy1, z0 + h - 0.45)
                m.box(bx1 - 0.35, yy0 - sg * 0.04 if sg < 0 else yy0, z0 + h * 0.5 - 0.5, bx1 - 0.28, yy1 + (0.06 if sg > 0 else 0.0) if sg > 0 else yy1 + 0.0, z0 + h * 0.5 + 0.5)
                for v in range(4):                                                        # vent slots (raised bars)
                    zz = z0 + h - 1.3 - v * 0.22
                    m.box(bx0 + 0.3, yy0 - (0.03 if sg < 0 else 0.0), zz, bx1 - 0.3, yy1 + (0.03 if sg > 0 else 0.0), zz + 0.08)
        else:
            e = 0.06
            xx0, xx1 = bx0 - e, bx0
            m.box(xx0, by0 + 0.12, z0 + 0.55, xx1, by1 - 0.12, z0 + h - 0.45)
            m.box(xx0 - 0.04, by1 - 0.35, z0 + h * 0.5 - 0.5, xx1, by1 - 0.28, z0 + h * 0.5 + 0.5)
            for v in range(4):
                zz = z0 + h - 1.3 - v * 0.22
                m.box(xx0 - 0.03, by0 + 0.3, zz, xx1, by1 - 0.3, zz + 0.08)

def build_ehouse():
    pre = "ELEC-EHOUSE-"
    x0, y0 = P["ehouse_origin_ft"]
    L, W, H = P["ehouse_ft"]
    fl = P["ehouse_floor_ft"]
    x1, y1 = x0 + L, y0 + W
    zf = GZ + fl
    st = MeshAcc(pre + "SUPPORT-STEEL", "STEEL")
    for x in range(int(x0) + 2, int(x1), 24):
        for y in (y0 + 2, y1 - 4):
            st.box(x - 1, y, GZ, x + 1, y + 2, zf - 1)
        st.seg((x, y0 + 3, GZ), (x, y1 - 3, zf - 1), 0.3, 6)
    for y in (y0 + 2, y1 - 4):
        st.box(x0, y, zf - 1.5, x1, y + 2, zf - 0.4)
    for x in range(int(x0), int(x1) + 1, 12):
        st.box(x - 0.4, y0, zf - 1.2, x + 0.4, y1, zf - 0.4)
    st.build()
    MeshAcc(pre + "FLOOR", "STEEL_DK").box(x0, y0, zf - 0.4, x1, y1, zf).build()
    # cable vault below the floor: under-floor tray with risers into cabinets
    ut = MeshAcc(pre + "UNDERFLOOR-TRAY", "STEEL")
    ut.tray([(x0 + 4, y0 + 10), (x1 - 4, y0 + 10)], GZ + 4, width=3, posts=True)
    ut.tray([(x0 + 4, y1 - 8), (x1 - 4, y1 - 8)], GZ + 4, width=3, posts=True)
    ut.build()
    # walls (S wall + roof are cutaway parts)
    wl = MeshAcc(pre + "WALLS", "ENCL")
    wl.box(x0, y1 - 0.6, zf, x1, y1, zf + H)
    wl.box(x0, y0, zf, x0 + 0.6, y1, zf + H)
    wl.box(x1 - 0.6, y0, zf, x1, y1, zf + H)
    wl.build()
    ws = MeshAcc(pre + "WALL-S", "ENCL", cutaway=True)
    wall_with_openings(ws, x0, x1, y0, y0 + 0.6, zf, zf + H, [(x0 + 4, x0 + 8, zf, zf + 8)], axis="x")   # door
    ws.build()
    MeshAcc(pre + "ROOF", "ENCL", cutaway=True).box(x0 - 0.5, y0 - 0.5, zf + H, x1 + 0.5, y1 + 0.5, zf + H + 0.6).build()
    hv = MeshAcc(pre + "ROOF-HVAC", "STEEL")
    for x in (x0 + 20, x0 + 70):
        hv.box(x, y1 - 10, zf + H + 0.6, x + 8, y1 - 2, zf + H + 4)
    hv.build()
    # interior lineups
    mv = MeshAcc(pre + "MV-SWITCHGEAR", "ENCL")
    cabinet_row(mv, x0 + 6, y1 - 6, zf, 8, 3.0, 5.0, 7.5)
    mv.build()
    lv = MeshAcc(pre + "LV-SWITCHGEAR", "ENCL")
    cabinet_row(lv, x0 + 40, y1 - 5, zf, 12, 2.5, 4.0, 7.5)
    lv.build()
    rp = MeshAcc(pre + "RELAY-PANELS", "ENCL")
    cabinet_row(rp, x0 + 6, y0 + 1, zf, 10, 2.5, 2.0, 7.5)
    rp.build()
    ups = MeshAcc(pre + "UPS-BATTERY", "ENCL")
    ups.box(x0 + 80, y0 + 1, zf, x0 + 86, y0 + 4, zf + 6.5)
    ups.box(x0 + 88, y0 + 1, zf, x0 + 104, y0 + 3.5, zf + 5.5)    # battery rack
    for k in range(6):
        for r in range(3):
            ups.box(x0 + 88.5 + k * 2.6, y0 + 1.2, zf + 0.5 + r * 1.7, x0 + 90.8 + k * 2.6, y0 + 3.3, zf + 1.9 + r * 1.7)
    ups.build()
    MeshAcc(pre + "DC-PANEL", "ENCL").box(x0 + 106, y0 + 1, zf, x0 + 110, y0 + 2.5, zf + 7).build()
    MeshAcc(pre + "STATION-TX", "ENCL").box(x0 + 72, y1 - 8, zf, x0 + 80, y1 - 2, zf + 7).build()
    # overhead control tray + cables inside
    ot = MeshAcc(pre + "OVERHEAD-TRAY", "STEEL")
    ot.tray([(x0 + 4, (y0 + y1) / 2), (x1 - 4, (y0 + y1) / 2)], zf + 11, width=2, posts=False)
    ot.build()
    cc = CurveAcc(pre + "CONTROL-CABLES", "CABLE", 0.04)
    for k in range(8):
        cc.add([(x0 + 4, (y0 + y1) / 2 - 0.8 + k * 0.2, zf + 11.3), (x1 - 4, (y0 + y1) / 2 - 0.8 + k * 0.2, zf + 11.3)])
    for k in range(8):
        xx = x0 + 7.5 + k * 3.0
        cc.add([(xx, (y0 + y1) / 2, zf + 11.3), (xx, y1 - 6.5, zf + 11.3), (xx, y1 - 6.5, zf + 7.5)])
    cc.build()
    # power risers from the under-floor trays up into MV / LV cubicles, copper terminations
    ri = CurveAcc(pre + "POWER-RISERS", "CABLE", 0.12)
    ends = []
    for k in range(8):
        xx = x0 + 7.5 + k * 3.0
        p = (xx, y1 - 3.5, zf + 1.0)
        ri.add([(xx, y1 - 8, GZ + 4.3), (xx, y1 - 8, zf - 2), (xx, y1 - 3.5, zf - 2), p])
        ends.append((p, (0, 0, 1)))
    for k in range(12):
        xx = x0 + 41.2 + k * 2.5
        p = (xx, y1 - 3, zf + 1.0)
        ri.add([(xx, y1 - 8, GZ + 4.3), (xx, y1 - 8, zf - 2), (xx, y1 - 3, zf - 2), p])
        ends.append((p, (0, 0, 1)))
    ri.build()
    cable_end_caps(pre + "TERMINATIONS", ends, r=0.16, L=0.6)
    # stairs and landing at the west end
    sl = MeshAcc(pre + "STAIR", "STEEL")
    sl.stair(x0 - 14, y0 + 2, GZ, zf, run_dir=(1, 0), width=4)
    sl.box(x0 - 2, y0 + 1, zf - 0.3, x0, y0 + 7, zf)
    sl.box(x0 - 14, y0 + 6.2, GZ, x0, y0 + 6.4, zf + 3.5)
    sl.build()
    # aux transformer at grade + feeder
    MeshAcc(pre + "AUX-TX", "ENCL").box(x0 + 40, y0 - 14, GZ, x0 + 50, y0 - 6, GZ + 8).build()
    fd = CurveAcc(pre + "AUX-FEEDER", "CABLE", 0.14)
    for k in range(3):
        fd.add([(x0 + 44 + k, y0 - 6, GZ + 8), (x0 + 44 + k, y0 - 2, GZ + 4.3), (x0 + 44 + k, y0 + 10, GZ + 4.3)])
    fd.build()
    anchor(pre + "MV-SWITCHGEAR", x0 + 18, y1 - 3.5, zf + 8.5, "MV switchgear lineup (13.8 kV)", 5)
    anchor(pre + "LV-SWITCHGEAR", x0 + 55, y1 - 3, zf + 8.5, "LV switchgear (480 V)", 5)
    anchor(pre + "RELAY-PANELS", x0 + 18, y0 + 2, zf + 8.5, "Protection and relay panels", 5)
    anchor(pre + "UPS", x0 + 83, y0 + 2.5, zf + 7.5, "UPS and battery rack", 5)
    anchor(pre + "OVERHEAD-TRAY", x0 + 60, (y0 + y1) / 2, zf + 12.5, "Overhead control tray", 5)
    anchor(pre + "RISERS", x0 + 18, y1 - 8, zf - 2, "Power cable risers from cable vault", 5)
    anchor(pre + "UNDERFLOOR-TRAY", x0 + 60, y1 - 8, GZ + 5, "Under-floor cable tray (vault)", 5)
    anchor(pre + "SUPPORT-STEEL", x0 + 26, y0 + 2, GZ + 4, "Elevated support steel", 5)
    anchor(pre + "HVAC", x0 + 24, y1 - 6, zf + H + 5, "Roof HVAC units", 5)
    anchor(pre + "STAIR", x0 - 7, y0 + 4, zf + 1, "Access stair and landing", 5)
    anchor(pre + "AUX-TX", x0 + 45, y0 - 10, GZ + 9, "Auxiliary transformer", 5)
    anchor(pre + "DC-PANEL", x0 + 108, y0 + 2, zf + 8, "DC distribution", 5)
    anchor("ZONE-05", (x0 + x1) / 2, (y0 + y1) / 2, zf + H + 6, ZONES[5][0], 5)


def build_mcc():
    pre = "ELEC-MCC-"
    x0, y0 = P["mcc_origin_ft"]
    L, W, H = P["mcc_ft"]
    x1, y1 = x0 + L, y0 + W
    MeshAcc(pre + "SLAB", "CONC").box(x0, y0, GZ - 0.5, x1, y1, GZ + 0.5).build()
    z0 = GZ + 0.5
    wl = MeshAcc(pre + "WALLS", "ENCL")
    wl.box(x0, y1 - 0.8, z0, x1, y1, z0 + H)
    wl.box(x0, y0, z0, x0 + 0.8, y1, z0 + H)
    wl.box(x1 - 0.8, y0, z0, x1, y1, z0 + H)
    for xp in (x0 + 30, x0 + 55):     # partitions: MCC | VFD | UPS-DC
        wall_with_openings(wl, xp - 0.4, xp + 0.4, y0, y1, z0, z0 + H, [(y0 + 4, y0 + 8, z0, z0 + 8)], axis="y")
    wl.build()
    ws = MeshAcc(pre + "WALL-S", "ENCL", cutaway=True)
    wall_with_openings(ws, x0, x1, y0, y0 + 0.8, z0, z0 + H, [(x0 + 4, x0 + 10, z0, z0 + 8), (x0 + 60, x0 + 66, z0, z0 + 8)], axis="x")
    ws.build()
    MeshAcc(pre + "ROOF", "ENCL", cutaway=True).box(x0 - 0.5, y0 - 0.5, z0 + H, x1 + 0.5, y1 + 0.5, z0 + H + 0.6).build()
    hv = MeshAcc(pre + "ROOF-HVAC", "STEEL")
    hv.box(x0 + 10, y1 - 12, z0 + H + 0.6, x0 + 18, y1 - 4, z0 + H + 4)
    hv.box(x0 + 40, y1 - 12, z0 + H + 0.6, x0 + 48, y1 - 4, z0 + H + 4)
    hv.build()
    mcc = MeshAcc(pre + "MCC-LINEUP", "ENCL")
    cabinet_row(mcc, x0 + 3, y1 - 3, z0, 12, 2.0, 1.7, 7.5)
    mcc.build()
    vfd = MeshAcc(pre + "VFD-CABINETS", "ENCL")
    cabinet_row(vfd, x0 + 33, y1 - 5, z0, 5, 4.0, 3.5, 8.0)
    vfd.box(x0 + 33, y0 + 3, z0, x0 + 45, y0 + 8, z0 + 6)   # line reactor / filter
    vfd.build()
    ups = MeshAcc(pre + "UPS-BATTERY", "ENCL")
    ups.box(x0 + 58, y1 - 5, z0, x0 + 64, y1 - 2, z0 + 6.5)
    ups.box(x0 + 66, y1 - 5, z0, x0 + 76, y1 - 2.5, z0 + 5.5)
    for k in range(4):
        for r in range(3):
            ups.box(x0 + 66.5 + k * 2.4, y1 - 4.8, z0 + 0.5 + r * 1.7, x0 + 68.6 + k * 2.4, y1 - 2.8, z0 + 1.9 + r * 1.7)
    ups.build()
    MeshAcc(pre + "DC-PANEL", "ENCL").box(x0 + 60, y0 + 3, z0, x0 + 64, y0 + 4.5, z0 + 7).build()
    ot = MeshAcc(pre + "OVERHEAD-TRAY", "STEEL")
    ot.tray([(x0 + 3, y0 + 12), (x1 - 3, y0 + 12)], z0 + 12, width=2.5, posts=False)
    ot.build()
    cb = CurveAcc(pre + "CABLES", "CABLE", 0.08)
    ends = []
    for k in range(10):
        cb.add([(x0 + 3, y0 + 11.2 + k * 0.18, z0 + 12.3), (x1 - 3, y0 + 11.2 + k * 0.18, z0 + 12.3)])
    for k in range(12):
        xx = x0 + 4 + k * 2.0
        p = (xx, y1 - 2.5, z0 + 7.6)
        cb.add([(xx, y0 + 12, z0 + 12.3), (xx, y1 - 4, z0 + 12.3), (xx, y1 - 4, z0 + 9), p])
        ends.append((p, (0, 0, -1)))
    for k in range(5):
        xx = x0 + 35 + k * 4.0
        p = (xx, y1 - 4.5, z0 + 8.1)
        cb.add([(xx, y0 + 12, z0 + 12.3), (xx, y1 - 6, z0 + 12.3), (xx, y1 - 6, z0 + 9.5), p])
        ends.append((p, (0, 0, -1)))
    cb.build()
    cable_end_caps(pre + "TERMINATIONS", ends, r=0.12, L=0.5)
    # cable entry pit at the west wall from the corridor lateral (below grade)
    MeshAcc(pre + "CABLE-PIT", "CONC", below=True).box(x0 - 8, y0 + 10, -6, x0 + 2, y0 + 16, GZ).build()
    MeshAcc(pre + "PIT-COVER", "STEEL_DK").box(x0 - 8, y0 + 10, GZ, x0 - 1, y0 + 16, GZ + 0.3).build()
    anchor(pre + "MCC-LINEUP", x0 + 15, y1 - 2, z0 + 8.5, "Motor control centre lineup", 9)
    anchor(pre + "VFD", x0 + 43, y1 - 3.5, z0 + 9, "Variable-frequency drives", 9)
    anchor(pre + "UPS", x0 + 61, y1 - 3.5, z0 + 7.5, "UPS and battery rack", 9)
    anchor(pre + "DC-PANEL", x0 + 62, y0 + 4, z0 + 8, "DC distribution panel", 9)
    anchor(pre + "OVERHEAD-TRAY", x0 + 40, y0 + 12, z0 + 13.5, "Overhead cable tray", 9)
    anchor(pre + "TERMINATIONS", x0 + 10, y1 - 2.5, z0 + 8, "Cable terminations (copper)", 9)
    anchor(pre + "CABLE-PIT", x0 - 4, y0 + 13, GZ + 1, "Cable entry pit from corridor lateral", 9)
    anchor(pre + "HVAC", x0 + 14, y1 - 8, z0 + H + 5, "Roof HVAC", 9)
    anchor(pre + "PARTITION", x0 + 30, y0 + 20, z0 + H + 1, "Fire-rated room partitions", 9)
    anchor("ZONE-09", (x0 + x1) / 2, (y0 + y1) / 2, z0 + H + 6, ZONES[9][0], 9)


def build_admin():
    pre = "ADMIN-"
    x0, y0 = P["admin_origin_ft"]
    L, W, H = P["admin_ft"]
    x1, y1 = x0 + L, y0 + W
    b = MeshAcc(pre + "BUILDING", "ENCL")
    b.box(x0, y0, GZ, x1, y1, GZ + H)
    b.build()
    g = MeshAcc(pre + "GLAZING", "GLASS")
    for z in (GZ + 4, GZ + 16):
        g.box(x0 + 4, y0 - 0.3, z, x1 - 4, y0 + 0.1, z + 6)
        g.box(x0 + 4, y1 - 0.1, z, x1 - 4, y1 + 0.3, z + 6)
    g.build()
    MeshAcc(pre + "CONTROL-ROOM", "ENCL").box(x1 - 44, y0 + 8, GZ + H, x1 - 8, y1 - 8, GZ + H + 3).build()   # raised roof block over control room
    MeshAcc(pre + "CANOPY", "STEEL").box(x0 + 40, y0 - 12, GZ + 9, x0 + 60, y0, GZ + 10).box(x0 + 41, y0 - 11, GZ, x0 + 42, y0 - 10, GZ + 9).box(x0 + 58, y0 - 11, GZ, x0 + 59, y0 - 10, GZ + 9).build()
    pad(pre + "PARKING", x0, y0 - 40, x1 + 40, y0 - 14, "ASPH", top=0.1, t=0.6)
    MeshAcc(pre + "CABLE-ENTRY", "CONC", below=True).box(x1 - 20, y0 - 30, -5, x1 - 16, y0, -2).build()
    anchor(pre + "CONTROL-ROOM", x1 - 26, (y0 + y1) / 2, GZ + H + 4, "Central control room", 4)
    anchor(pre + "BUILDING", x0 + 30, (y0 + y1) / 2, GZ + H + 1, "Admin building (two storeys)", 4)
    anchor("ZONE-04", (x0 + x1) / 2, (y0 + y1) / 2, GZ + H + 8, ZONES[4][0], 4)

# =============================================================================
# BESS, LAYDOWN / REELS, MODULAR POWER YARD
# =============================================================================
def build_bess():
    pre = "BESS-"
    x0, y0 = P["bess_origin_ft"]
    cL, cW, cH = P["bess_ft"]
    pL, pW, pH = P["pcs_tx_ft"]
    cont = MeshAcc(pre + "CONTAINERS", "ENCL")
    hvac = MeshAcc(pre + "HVAC", "STEEL")
    pcs = MeshAcc(pre + "PCS-SKIDS", "ENCL")
    dc = CurveAcc(pre + "DC-CABLES", "CABLE", 0.1)
    ac = CurveAcc(pre + "AC-CABLES", "CABLE", 0.12)
    ends = []
    k = 0
    for row in range(2):
        for col in range(4):
            cx0 = x0 + 10 + col * 50
            cy0 = y0 + 10 + row * 50
            cont.box(cx0, cy0, GZ + 0.5, cx0 + cL, cy0 + cW, GZ + 0.5 + cH)
            cont.box(cx0 + 1, cy0 - 0.3, GZ, cx0 + cL - 1, cy0 + cW + 0.3, GZ + 0.5)
            hvac.box(cx0 + 4, cy0 + cW, GZ + 2, cx0 + 9, cy0 + cW + 2, GZ + 7)
            hvac.box(cx0 + cL - 9, cy0 + cW, GZ + 2, cx0 + cL - 4, cy0 + cW + 2, GZ + 7)
            py0 = cy0 + cW + 6
            pcs.box(cx0 + 8, py0, GZ, cx0 + 8 + pL, py0 + pW, GZ + 0.8)
            pcs.box(cx0 + 9, py0 + 1, GZ + 0.8, cx0 + 19, py0 + pW - 1, GZ + pH)          # PCS inverter cabinet
            pcs.box(cx0 + 21, py0 + 1.5, GZ + 0.8, cx0 + 31, py0 + pW - 1.5, GZ + pH - 2)   # MV transformer
            for kk in range(3):
                pcs.cyl(cx0 + 23 + kk * 3, py0 + pW / 2, GZ + pH - 2, 0.35, 2.5, 8)
            for kk in range(4):
                p0 = (cx0 + 12 + kk * 1.2, cy0 + cW, GZ + 3)
                p1 = (cx0 + 12 + kk * 1.2, py0 + 1, GZ + 3)
                dc.add([p0, (p0[0], p0[1] + 1.5, GZ + 1.2), (p1[0], p1[1] - 1.5, GZ + 1.2), p1])
                ends.append((p0, (0, 1, 0))); ends.append((p1, (0, -1, 0)))
            for kk in range(3):
                p1 = (cx0 + 23 + kk * 3, py0 + pW, GZ + 2)
                ac.add([p1, (p1[0], py0 + pW + 4, GZ + 1.5), (p1[0], y0 + 10 + row * 50 + cW + 6 + pW + 6, GZ + 3.3)])
                ends.append((p1, (0, 1, 0)))
            k += 1
    cont.build(); hvac.build(); pcs.build(); dc.build(); ac.build()
    cable_end_caps(pre + "CONNECTORS", ends, r=0.14, L=0.5)
    # collector trays to the MV switchgear container, then feeder to the e-house
    tr = MeshAcc(pre + "COLLECTOR-TRAY", "STEEL")
    for row in range(2):
        yt = y0 + 10 + row * 50 + cW + 6 + pW + 6
        tr.tray([(x0 + 15, yt), (x0 + 230, yt)], GZ + 3, width=2.5)
    tr.tray([(x0 + 230, y0 + 34), (x0 + 230, y0 + 84)], GZ + 3, width=2.5)
    tr.build()
    MeshAcc(pre + "MV-SWITCHGEAR", "ENCL").box(x0 + 226, y0 + 88, GZ, x0 + 246, y0 + 96, GZ + 9).build()
    fd = MeshAcc(pre + "FEEDER-TRAY", "STEEL")
    fd.tray([(x0 + 236, y0 + 88), (x0 + 236, P["ehouse_origin_ft"][1] + P["ehouse_ft"][1] + 8)], GZ + 3, width=2.5)
    fd.build()
    fc = CurveAcc(pre + "FEEDER-CABLES", "CABLE", 0.13)
    for kk in range(3):
        xx = x0 + 235.5 + kk * 0.5
        fc.add([(xx, y0 + 88, GZ + 3.3), (xx, P["ehouse_origin_ft"][1] + P["ehouse_ft"][1] + 8, GZ + 3.3),
                (xx, P["ehouse_origin_ft"][1] + P["ehouse_ft"][1] - 8, GZ + 4.3)])
    fc.build()
    anchor(pre + "CONTAINER", x0 + 30, y0 + 14, GZ + cH + 2, "Battery enclosure (ISO container)", 2)
    anchor(pre + "PCS", x0 + 24, y0 + 10 + cW + 6 + 5, GZ + pH + 1.5, "PCS inverter and MV transformer skid", 2)
    anchor(pre + "DC-CABLES", x0 + 32, y0 + 10 + cW + 3, GZ + 3, "DC cables, container to PCS", 2)
    anchor(pre + "COLLECTOR-TRAY", x0 + 120, y0 + 10 + cW + 6 + pW + 6, GZ + 4.5, "MV collector tray", 2)
    anchor(pre + "MV-SWITCHGEAR", x0 + 236, y0 + 92, GZ + 10, "BESS MV switchgear", 2)
    anchor(pre + "FEEDER", x0 + 236, y0 - 12, GZ + 4.5, "MV feeder to e-house", 2)
    anchor(pre + "HVAC", x0 + 16.5, y0 + 10 + cW + 1, GZ + 8, "Container HVAC", 2)
    anchor("ZONE-02", x0 + 110, y0 + 50, GZ + 16, ZONES[2][0], 2)


def build_laydown():
    pre = "LAYDOWN-"
    x0, y0 = P["laydown_origin_ft"]
    L, W = P["laydown_ft"]
    rd, rw = P["reel_d_w_ft"]
    reels = MeshAcc(pre + "REELS", "STEEL_DK")
    stands = MeshAcc(pre + "PAYOUT-STANDS", "STEEL")
    for k in range(P["counts"]["reels"]):
        cx, cy = x0 + 20 + k * 22, y0 + 24
        r = rd / 2 + (1.0 if k % 2 else 0.0)
        z = r + 1.5
        for dx in (-rw / 2, rw / 2 - 0.4):
            reels.cyl_between((cx + dx, cy, z), (cx + dx + 0.4, cy, z), r, 24)
        reels.cyl_between((cx - rw / 2, cy, z), (cx + rw / 2, cy, z), r * 0.45, 16)
        # A-frame stand + axle
        for sx in (-rw / 2 - 1.5, rw / 2 + 1.5):
            stands.seg((cx + sx, cy - 3, GZ), (cx + sx, cy, z), 0.3, 6)
            stands.seg((cx + sx, cy + 3, GZ), (cx + sx, cy, z), 0.3, 6)
            stands.box(cx + sx - 0.4, cy - 3.5, GZ, cx + sx + 0.4, cy + 3.5, GZ + 0.4)
        stands.cyl_between((cx - rw / 2 - 2, cy, z), (cx + rw / 2 + 2, cy, z), 0.35, 8)
    reels.build(); stands.build()
    # prefab electrical spine: 40 ft two-tier tray on trestles, cable being pulled from reel 3
    sx0, sy = x0 + 40, y0 + 70
    sp = MeshAcc(pre + "PREFAB-SPINE", "STEEL")
    sp.tray([(sx0, sy), (sx0 + P["prefab_spine_l_ft"], sy)], GZ + 4, width=3)
    sp.tray([(sx0, sy), (sx0 + P["prefab_spine_l_ft"], sy)], GZ + 6, width=2, posts=False)
    for x in range(int(sx0), int(sx0 + P["prefab_spine_l_ft"]) + 1, 10):
        sp.box(x - 0.3, sy - 1.2, GZ + 4.5, x + 0.3, sy + 1.2, GZ + 6)
    sp.build()
    cl = MeshAcc(pre + "CLEATS", "STEEL_DK")
    for x in range(int(sx0) + 2, int(sx0 + P["prefab_spine_l_ft"]), 3):
        cl.box(x - 0.25, sy - 1.2, GZ + 4.12, x + 0.25, sy + 1.2, GZ + 4.6)
    cl.build()
    pc = CurveAcc(pre + "PULLED-CABLES", "CABLE", 0.12)
    ends = []
    reel_cx, reel_cy, reel_z = x0 + 20 + 2 * 22, y0 + 24, rd / 2 + 1.5
    for k in range(4):
        pts = [(reel_cx - 1.5 + k, reel_cy, reel_z + rd / 2), (reel_cx - 1.5 + k, reel_cy + 8, reel_z + 1),
               (reel_cx - 1.5 + k, sy - 6, GZ + 3.5), (reel_cx - 1.5 + k, sy - 1.0 + k * 0.6, GZ + 4.3),
               (sx0 + 4 + k * 8, sy - 1.0 + k * 0.6, GZ + 4.3)]
        pc.add(pts)
        ends.append((pts[-1], (1, 0, 0)))
    for k in range(6):
        pts = [(sx0, sy - 0.7 + k * 0.28, GZ + 6.3), (sx0 + P["prefab_spine_l_ft"], sy - 0.7 + k * 0.28, GZ + 6.3)]
        pc.add(pts)
        ends.append((pts[-1], (1, 0, 0)))
    pc.build()
    cable_end_caps(pre + "CABLE-END-CAPS", ends, r=0.18, L=0.6)
    # bonding jumpers at tray joints (copper)
    bj = MeshAcc(pre + "BONDING-JUMPERS", "COPPER")
    for x in (sx0 + 10, sx0 + 20, sx0 + 30):
        bj.cyl_between((x - 0.6, sy + 1.5, GZ + 4.3), (x + 0.6, sy + 1.5, GZ + 4.3), 0.08, 6)
        bj.cyl_between((x - 0.6, sy + 1.0, GZ + 6.3), (x + 0.6, sy + 1.0, GZ + 6.3), 0.08, 6)
    bj.build()
    # crates, container office, spare drums flat
    cr = MeshAcc(pre + "CRATES", "STEEL_DK")
    for k in range(6):
        cr.box(x0 + 110 + (k % 3) * 10, y0 + 60 + (k // 3) * 6, GZ, x0 + 118 + (k % 3) * 10, y0 + 64 + (k // 3) * 6, GZ + 4)
    cr.box(x0 + 120, y0 + 66, GZ + 4, x0 + 128, y0 + 70, GZ + 8)
    cr.build()
    MeshAcc(pre + "SITE-OFFICE", "ENCL").box(x0 + 140, y0 + 20, GZ, x0 + 160, y0 + 28, GZ + 8.5).build()
    sd = MeshAcc(pre + "SPARE-DRUMS", "STEEL_DK")
    for k in range(3):
        sd.cyl(x0 + 150 + k * 9, y0 + 90, GZ, 4, 3, 20)
    sd.build()
    anchor(pre + "REEL", x0 + 64, y0 + 24, rd + 3, "Cable reels on payout stands", 3)
    anchor(pre + "PAYOUT-STAND", x0 + 20, y0 + 21, GZ + 3, "Payout stand (A-frame, axle, brake)", 3)
    anchor(pre + "PREFAB-SPINE", sx0 + 20, sy, GZ + 7.5, "Prefab two-tier tray spine (power below, controls above)", 3)
    anchor(pre + "CLEATS", sx0 + 8, sy - 1.2, GZ + 5, "Cable cleats", 3)
    anchor(pre + "BONDING", sx0 + 20, sy + 1.5, GZ + 5, "Tray bonding jumpers (copper)", 3)
    anchor(pre + "CABLE-ENDS", sx0 + 36, sy, GZ + 5, "Cable end caps (copper)", 3)
    anchor(pre + "PULLED-CABLES", reel_cx, sy - 6, GZ + 4, "Cables paid out from reel", 3)
    anchor(pre + "CRATES", x0 + 124, y0 + 68, GZ + 9, "Crated equipment", 3)
    anchor(pre + "SITE-OFFICE", x0 + 150, y0 + 24, GZ + 10, "Site office", 3)
    anchor("ZONE-03", x0 + 90, y0 + 55, GZ + 14, ZONES[3][0], 3)


def build_modular():
    pre = "MODPWR-"
    x0, y0 = P["modular_origin_ft"]
    gL, gW, gH = P["genset_ft"]
    fL, fW, fH = P["fuel_cell_ft"]
    gs = MeshAcc(pre + "GENSETS", "ENCL")
    ex = MeshAcc(pre + "GENSET-EXHAUSTS", "STEEL_DK")
    names = ("STANDBY-1", "STANDBY-2", "BLACK-START")
    for k in range(3):
        gx, gy = x0 + 10, y0 + 10 + k * 22
        gs.box(gx, gy, GZ + 0.5, gx + gL, gy + gW, GZ + 0.5 + gH)
        gs.box(gx + 1, gy - 0.3, GZ, gx + gL - 1, gy + gW + 0.3, GZ + 0.5)
        gs.box(gx + gL, gy + 1, GZ + 2, gx + gL + 2, gy + gW - 1, GZ + gH - 1)   # radiator grille
        ex.cyl_between((gx + 8, gy + gW / 2, GZ + gH + 0.5), (gx + 22, gy + gW / 2, GZ + gH + 0.5), 1.4, 12)
        ex.cyl(gx + 20, gy + gW / 2, GZ + gH + 1.5, 0.6, 6, 8)
        anchor(pre + names[k], gx + gL / 2, gy + gW / 2, GZ + gH + 4, ("Standby genset" if k < 2 else "Black-start genset") + " (containerised)", 10)
    gs.build(); ex.build()
    fc = MeshAcc(pre + "FUEL-CELLS", "ENCL")
    inv = MeshAcc(pre + "INVERTERS", "ENCL")
    for k in range(4):
        fx, fy = x0 + 80 + k * 26, y0 + 12
        fc.box(fx, fy, GZ, fx + fL, fy + fW, GZ + fH)
        fc.cyl(fx + 5, fy + fW / 2, GZ + fH, 1.2, 3, 10)
        fc.cyl(fx + 12, fy + fW / 2, GZ + fH, 1.2, 3, 10)
        inv.box(fx + 4, fy + fW + 4, GZ, fx + 12, fy + fW + 8, GZ + 6)
    fc.build(); inv.build()
    MeshAcc(pre + "PARALLELING-SWGR", "ENCL").box(x0 + 100, y0 + 70, GZ, x0 + 120, y0 + 78, GZ + 9).build()
    MeshAcc(pre + "FUEL-GAS-SKID", "STEEL").box(x0 + 130, y0 + 70, GZ, x0 + 140, y0 + 76, GZ + 5).build()
    cb = CurveAcc(pre + "CABLES", "CABLE", 0.12)
    ends = []
    for k in range(3):
        p0 = (x0 + 10 + gL - 4, y0 + 10 + k * 22 + gW, GZ + 3)
        p1 = (x0 + 102 + k * 1.5, y0 + 70, GZ + 3)
        cb.add([p0, (p0[0], p0[1] + 2, GZ + 1), (x0 + 60, y0 + 60 + k * 0.5, GZ + 1), (p1[0], p1[1] - 2, GZ + 1), p1])
        ends.append((p0, (0, 1, 0))); ends.append((p1, (0, -1, 0)))
    for k in range(4):
        p0 = (x0 + 88 + k * 26, y0 + 12 + fW + 8, GZ + 3)
        p1 = (x0 + 110 + k * 1.5, y0 + 70, GZ + 3)
        cb.add([p0, (p0[0], p0[1] + 2, GZ + 1), (p0[0], y0 + 60, GZ + 1), (p1[0], y0 + 62, GZ + 1), (p1[0], p1[1] - 2, GZ + 1), p1])
        ends.append((p0, (0, 1, 0))); ends.append((p1, (0, -1, 0)))
    cb.build()
    cable_end_caps(pre + "CONNECTORS", ends, r=0.15, L=0.5)
    tr = MeshAcc(pre + "TRAY", "STEEL")
    tr.tray([(x0 + 60, y0 + 60), (x0 + 120, y0 + 60)], GZ + 1, width=2.5, posts=False)
    tr.build()
    anchor(pre + "FUEL-CELL", x0 + 90, y0 + 16, GZ + fH + 4, "Fuel-cell modules with inverters", 10)
    anchor(pre + "PARALLELING-SWGR", x0 + 110, y0 + 74, GZ + 10, "Paralleling switchgear", 10)
    anchor(pre + "FUEL-GAS-SKID", x0 + 135, y0 + 73, GZ + 6, "Fuel-gas conditioning skid", 10)
    anchor(pre + "CABLES", x0 + 60, y0 + 61, GZ + 2, "Genset and fuel-cell output cables", 10)
    anchor(pre + "INVERTER", x0 + 88, y0 + 12 + fW + 6, GZ + 7, "Fuel-cell inverter skid", 10)
    anchor("ZONE-10", x0 + 90, y0 + 50, GZ + 20, ZONES[10][0], 10)

# =============================================================================
# ACC, CHILLERS / TOWERS, WATER TREATMENT
# =============================================================================
def build_acc():
    pre = "ACC-"
    x0, y0 = ACC_X0, ACC_Y0
    x1, y1 = x0 + ACC_L, y0 + ACC_W
    nx, ny = P["acc_cells"]
    deck = P["acc_fan_deck_ft"]
    cw = ACC_L / nx
    fr = P["acc_fan_d_ft"] / 2
    cols = MeshAcc(pre + "COLUMNS", "STEEL")
    for i in range(nx + 1):
        for j in range(ny + 1):
            x, y = x0 + i * cw, y0 + j * cw
            cols.box(x - 1.2, y - 1.2, GZ, x + 1.2, y + 1.2, deck)
    for i in range(nx):
        for j in (0, ny):
            x, y = x0 + i * cw, y0 + j * cw
            cols.seg((x, y, GZ), (x + cw, y, deck / 2), 0.4, 6)
            cols.seg((x + cw, y, GZ), (x, y, deck / 2), 0.4, 6)
    for j in range(ny):
        for i in (0, nx):
            x, y = x0 + i * cw, y0 + j * cw
            cols.seg((x, y, GZ), (x, y + cw, deck / 2), 0.4, 6)
            cols.seg((x, y + cw, GZ), (x, y, deck / 2), 0.4, 6)
    for z in (deck / 2, deck - 6):
        for i in range(nx + 1):
            cols.box(x0 + i * cw - 0.6, y0, z, x0 + i * cw + 0.6, y1, z + 1.2)
        for j in range(ny + 1):
            cols.box(x0, y0 + j * cw - 0.6, z, x1, y0 + j * cw + 0.6, z + 1.2)
    cols.build()
    MeshAcc(pre + "FAN-DECK", "STEEL_DK").box(x0, y0, deck - 1, x1, y1, deck).build()
    fans = MeshAcc(pre + "FANS", "STEEL")
    motors = MeshAcc(pre + "FAN-MOTORS", "ENCL")
    for i in range(nx):
        for j in range(ny):
            cx, cy = x0 + (i + 0.5) * cw, y0 + (j + 0.5) * cw
            fans.cyl(cx, cy, deck, fr, 5, 28, caps=False)
            fans.cyl(cx, cy, deck + 3.0, 1.6, 2.2, 12)
            for a in (0, 45, 90, 135):
                fans.boxc(cx, cy, deck + 3.4, fr * 1.9, 1.2, 0.25, rot=math.radians(a))
            motors.box(cx - 1.5, cy - 1.5, deck + 0.4, cx + 1.5, cy + 1.5, deck + 3.0)
    fans.build(); motors.build()
    ww = MeshAcc(pre + "WINDWALL", "ENCL")
    ww.box(x0 - 1, y0 - 1, deck, x1 + 1, y0, ACC_H)
    ww.box(x0 - 1, y1, deck, x1 + 1, y1 + 1, ACC_H)
    ww.box(x0 - 1, y0, deck, x0, y1, ACC_H)
    ww.box(x1, y0, deck, x1 + 1, y1, ACC_H)
    ww.build()
    # A-frame tube bundles per column row (ridge along y)
    tb = MeshAcc(pre + "TUBE-BUNDLES", "STEEL")
    hdr = MeshAcc(pre + "STEAM-HEADERS", "INSUL")
    t = 1.5
    for i in range(nx):
        xr = x0 + (i + 0.5) * cw
        zb, zt = deck + 2, ACC_H - 4
        for s in (-1, 1):
            xb = xr + s * (cw / 2 - 2)
            xt = xr + s * 1.5
            b = [(xb, y0 + 1, zb), (xb + t, y0 + 1, zb), (xb + t, y1 - 1, zb), (xb, y1 - 1, zb)]
            tp = [(xt, y0 + 1, zt), (xt + t, y0 + 1, zt), (xt + t, y1 - 1, zt), (xt, y1 - 1, zt)]
            tb.hexa(b + tp)
        hdr.cyl_between((xr, y0 + 1, zt + 2), (xr, y1 - 1, zt + 2), 3.0, 16)
        hdr.cyl_between((xr - cw / 2 + 2, y0 + 1, zb - 1), (xr - cw / 2 + 2, y1 - 1, zb - 1), 1.2, 10)   # condensate headers
    hdr.cyl_between((x0 - 8, (y0 + y1) / 2, ACC_H - 2), (x1 + 2, (y0 + y1) / 2, ACC_H - 2), 5.5, 20)   # main steam duct along top
    for i in range(nx):
        xr = x0 + (i + 0.5) * cw
        hdr.cyl_between((xr, (y0 + y1) / 2, ACC_H - 2), (xr, (y0 + y1) / 2, ACC_H - 5.5), 2.5, 12)
    tb.build(); hdr.build()
    # main steam duct from the ST exhaust: hall east wall -> east -> north -> up the west face
    sd = CurveAcc(pre + "STEAM-DUCT", "STEEL", 6)
    ym = (y0 + y1) / 2
    sd.add([(HX1 - 1, 730, 30), (1385, 730, 30), (1385, ym, 30), (x0 - 8, ym, 30), (x0 - 8, ym, ACC_H - 2), (x0 + 2, ym, ACC_H - 2)])
    sd.build()
    ds = MeshAcc(pre + "STEAM-DUCT-SUPPORTS", "STEEL_DK")
    ds.pipe_supports([(HX1 + 20, 730), (1385, 730), (1385, ym), (x0 - 8, ym)], 24, pitch=40, w=2.5)
    ds.build()
    # condensate tank + pumps, ACC MCC and fan feeders (all on the south side of the ACC)
    ct = MeshAcc(pre + "CONDENSATE-TANK", "ENCL")
    ct.cyl(x0 + 80, y0 - 22, GZ, 10, 24, 24)
    for k in range(2):
        ct.cyl(x0 + 100 + k * 10, y0 - 14, GZ, 1.5, 6, 10)
        ct.box(x0 + 98 + k * 10, y0 - 16, GZ, x0 + 102 + k * 10, y0 - 12, GZ + 1)
    ct.build()
    cp = CurveAcc(pre + "CONDENSATE-PIPING", "INSUL", 1.0)
    cp.add([(x0 + 90, y0 - 22, GZ + 6), (x0 + 100, y0 - 22, GZ + 6), (x0 + 100, y0 - 14, GZ + 6), (x0 + 100, y0 - 14, GZ + 4)])
    cp.add([(x0 + 110, y0 - 14, GZ + 6), (x0 + 120, y0 - 14, GZ + 6), (x0 + 120, y0 + 2, GZ + 6), (x0 + 120, y0 + 2, deck + 1)])
    cp.build()
    MeshAcc(pre + "MCC", "ENCL").box(x0 + 20, y0 - 32, GZ, x0 + 48, y0 - 24, GZ + 9).build()
    ft = MeshAcc(pre + "FEEDER-TRAYS", "STEEL")
    ft.tray([(x0 + 34, y0 - 24), (x0 + 34, y0 - 4)], GZ + 6, width=2.5, posts=True)
    ft.box(x0 + 32.8, y0 - 4, GZ + 6, x0 + 35.2, y0 - 1, deck + 1)      # vertical riser tray on the south face
    ft.tray([(x0 + 34, y0 - 1), (x0 + 34, y0 + 2), (x0 + 2, y0 + 2)], deck + 1, width=2.5, posts=False)
    for j in range(ny):
        yt = y0 + (j + 0.5) * cw - fr - 2
        ft.tray([(x0 + 2, yt), (x1 - 2, yt)], deck + 1, width=2.0, posts=False)
    ft.tray([(x0 + 2, y0 + 2), (x0 + 2, y1 - 2)], deck + 1, width=2.5, posts=False)
    ft.build()
    fd = CurveAcc(pre + "FAN-FEEDERS", "CABLE", 0.09)
    ends = []
    for j in range(ny):
        yt = y0 + (j + 0.5) * cw - fr - 2
        for k in range(3):
            fd.add([(x0 + 2, yt - 0.6 + k * 0.5, deck + 1.3), (x1 - 2, yt - 0.6 + k * 0.5, deck + 1.3)])
        for i in range(nx):
            cx, cy = x0 + (i + 0.5) * cw, y0 + (j + 0.5) * cw
            p = (cx + 1.5, cy - 1.0, deck + 2.5)
            fd.add([(cx + 1.5, yt, deck + 1.3), (cx + 1.5, cy - fr + 2, deck + 0.4), (cx + 1.5, cy - 1.5, deck + 0.4), p])
            ends.append((p, (0, 1, 0)))
    for k in range(6):
        xx = x0 + 34 - 0.6 + k * 0.25
        fd.add([(xx, y0 - 24, GZ + 6.3), (xx, y0 - 3, GZ + 6.3), (xx, y0 - 3, deck + 1.3), (xx, y0 + 2, deck + 1.3), (x0 + 2, y0 + 2, deck + 1.3)])
    fd.build()
    cable_end_caps(pre + "FEEDER-CONNECTORS", ends, r=0.11, L=0.4)
    anchor(pre + "FAN", x0 + 0.5 * cw, y0 + 0.5 * cw, deck + 6, "ACC fan cell (8 x 8 array)", 11)
    anchor(pre + "FAN-MOTOR", x0 + 1.5 * cw, y0 + 0.5 * cw, deck + 3.5, "Fan gearbox / motor", 11)
    anchor(pre + "DECK-TRAY", x0 + 3 * cw, y0 + 0.5 * cw - fr - 2, deck + 2.5, "Fan-deck feeder trays", 11)
    anchor(pre + "FEEDERS", x0 + 2.5 * cw + 1.5, y0 + 0.5 * cw - 1, deck + 3.2, "Fan motor feeders (copper terminations)", 11)
    anchor(pre + "RISER", x0 + 34, y0 - 2.5, deck / 2, "Riser tray up the south face", 11)
    anchor(pre + "MCC", x0 + 34, y0 - 28, GZ + 10, "ACC motor control centre", 11)
    anchor(pre + "STEAM-DUCT", 1400, ym, 37, "Main steam duct from ST exhaust", 11)
    anchor(pre + "STEAM-HEADER", x0 + 4 * cw, ym, ACC_H + 4, "Steam distribution header / ridge manifolds", 11)
    anchor(pre + "TUBE-BUNDLES", x0 + 2.5 * cw, y0 + 4, ACC_H - 10, "A-frame finned tube bundles", 11)
    anchor(pre + "WINDWALL", x0 + ACC_L / 2, y0 - 1, ACC_H + 1, "Wind wall", 11)
    anchor(pre + "COLUMNS", x0, y0, deck / 2, "Support structure and bracing", 11)
    anchor(pre + "CONDENSATE-TANK", x0 + 80, y0 - 22, GZ + 26, "Condensate tank and pumps", 11)
    anchor("ZONE-11", x0 + ACC_L / 2, y0 + ACC_W / 2, ACC_H + 8, ZONES[11][0], 11)


def build_chillers():
    pre = "CHILL-"
    x0, y0 = P["chill_origin_ft"]
    cL, cW, cH = P["chiller_ft"]
    tL, tW, tH = P["tower_cell_ft"]
    ch = MeshAcc(pre + "CHILLERS", "ENCL")
    for k in range(P["counts"]["chiller"]):
        cx = x0 + 10 + k * 40
        ch.box(cx, y0 + 20, GZ, cx + cL, y0 + 20 + cW, GZ + 3)
        ch.cyl_between((cx + 2, y0 + 20 + cW / 2, GZ + 6), (cx + cL - 2, y0 + 20 + cW / 2, GZ + 6), 3.0, 16)
        ch.cyl_between((cx + 2, y0 + 20 + cW / 2, GZ + 9.5), (cx + cL - 2, y0 + 20 + cW / 2, GZ + 9.5), 2.4, 16)
        ch.box(cx + 10, y0 + 20 + 1, GZ + 3, cx + 16, y0 + 20 + cW - 1, GZ + 8)
    ch.build()
    tw = MeshAcc(pre + "TOWER-CELLS", "ENCL")
    tf = MeshAcc(pre + "TOWER-FANS", "STEEL")
    tw.box(x0 + 10, y0 + 80, GZ, x0 + 10 + P["counts"]["tower"] * tL, y0 + 80 + tW, GZ + 1.5)   # basin curb
    for k in range(P["counts"]["tower"]):
        tx = x0 + 10 + k * tL
        tw.box(tx + 0.5, y0 + 80.5, GZ + 1.5, tx + tL - 0.5, y0 + 80 + tW - 0.5, GZ + tH)
        tw.box(tx + 1, y0 + 79.5, GZ + 3, tx + tL - 1, y0 + 80.5, GZ + tH - 6)
        tf.cyl(tx + tL / 2, y0 + 80 + tW / 2, GZ + tH, 8, 5, 24, caps=False, r2=9)
        tf.cyl(tx + tL / 2, y0 + 80 + tW / 2, GZ + tH + 1, 1.2, 2, 10)
    tw.build(); tf.build()
    pm = MeshAcc(pre + "PUMPS", "STEEL_DK")
    for k in range(3):
        pm.cyl(x0 + 20 + k * 8, y0 + 60, GZ, 1.3, 4, 10)
        pm.box(x0 + 18 + k * 8, y0 + 58, GZ, x0 + 22 + k * 8, y0 + 62, GZ + 0.8)
    pm.build()
    pp = CurveAcc(pre + "PIPING", "INSUL", 0.9)
    for k in range(3):
        pp.add([(x0 + 20 + k * 8, y0 + 60, GZ + 4), (x0 + 20 + k * 8, y0 + 70, GZ + 4), (x0 + 20 + k * 8, y0 + 80, GZ + 4)])
        pp.add([(x0 + 25 + k * 40, y0 + 30, GZ + 4), (x0 + 25 + k * 40, y0 + 55, GZ + 4), (x0 + 20 + k * 8, y0 + 55, GZ + 4)])
    pp.add([(x0 + 10, y0 + 40, GZ + 4), (x0 + 10 + 3 * 40, y0 + 40, GZ + 4)])
    pp.build()
    anchor(pre + "CHILLER", x0 + 25, y0 + 25, GZ + 13, "Water-cooled chiller package", 12)
    anchor(pre + "TOWER-CELL", x0 + 22, y0 + 92, GZ + tH + 7, "Auxiliary cooling tower cells", 12)
    anchor(pre + "PUMPS", x0 + 28, y0 + 60, GZ + 5, "Circulating pumps", 12)
    anchor(pre + "PIPING", x0 + 70, y0 + 40, GZ + 5.5, "Chilled / cooling-water piping", 12)
    anchor("ZONE-12", x0 + 60, y0 + 60, GZ + tH + 12, ZONES[12][0], 12)


def build_water():
    pre = "WATER-"
    x0, y0 = P["water_origin_ft"]
    bL, bW, bH = P["water_treatment_ft"]
    pL, pW, pD = P["pond_ft"]
    n, td, th = P["water_tank_n_d_h_ft"]
    # pond: berm ring + water surface (visible; the excavation is a depression, not below-grade equipment)
    bm = MeshAcc(pre + "POND-BERM", "GRAVEL")
    bm.box(x0 - 6, y0 - 6, 0.0, x0 + pL + 6, y0, GZ + 3.0)
    bm.box(x0 - 6, y0 + pW, 0.0, x0 + pL + 6, y0 + pW + 6, GZ + 3.0)
    bm.box(x0 - 6, y0, 0.0, x0, y0 + pW, GZ + 3.0)
    bm.box(x0 + pL, y0, 0.0, x0 + pL + 6, y0 + pW, GZ + 3.0)
    bm.build()
    MeshAcc(pre + "POND-LINER", "STEEL_DK").box(x0, y0, 0.0, x0 + pL, y0 + pW, 0.25).build()
    MeshAcc(pre + "POND-WATER", "WATER").box(x0 + 0.3, y0 + 0.3, 0.25, x0 + pL - 0.3, y0 + pW - 0.3, 1.9).build()
    # building + tanks
    by = y0 + pW + 40
    MeshAcc(pre + "BUILDING", "ENCL").box(x0, by, GZ, x0 + bL, by + bW, GZ + bH).build()
    tk = MeshAcc(pre + "TANKS", "ENCL")
    for k in range(n):
        cx = x0 + bL + 40 + k * 60
        tk.cyl(cx, by + bW / 2, GZ, td / 2, th, 32)
        tk.cyl(cx, by + bW / 2, GZ + th, td / 2, 3, 32, r2=1.0)
        tk.cyl(cx, by + bW / 2, GZ - 1, td / 2 + 1, 1, 32)
    tk.build()
    pm = MeshAcc(pre + "PUMPS", "STEEL_DK")
    for k in range(3):
        pm.cyl(x0 + bL + 10, by + 10 + k * 8, GZ, 1.2, 4, 10)
    pm.build()
    pp = CurveAcc(pre + "PIPING", "INSUL", 0.8)
    for k in range(n):
        cx = x0 + bL + 40 + k * 60
        pp.add([(cx - td / 2, by + bW / 2, GZ + 3), (x0 + bL + 10, by + bW / 2, GZ + 3), (x0 + bL + 10, by + 14, GZ + 3)])
    pp.add([(x0 + bL, by + 10, GZ + 3), (x0 + bL + 10, by + 10, GZ + 3)])
    pp.add([(x0 + 40, by, GZ + 3), (x0 + 40, y0 + pW + 6, GZ + 3), (x0 + 40, y0 + pW - 2, GZ + 3), (x0 + 40, y0 + pW - 2, GZ + 1.2)])
    pp.build()
    anchor(pre + "BUILDING", x0 + bL / 2, by + bW / 2, GZ + bH + 1, "Water treatment building", 13)
    anchor(pre + "TANK", x0 + bL + 40, by + bW / 2, GZ + th + 4, "Raw / demineralised water tanks", 13)
    anchor(pre + "POND", x0 + pL / 2, y0 + pW / 2, GZ + 1, "Lined wastewater pond", 13)
    anchor(pre + "PUMPS", x0 + bL + 10, by + 18, GZ + 5, "Transfer pumps", 13)
    anchor("ZONE-13", x0 + 120, y0 + 150, GZ + th + 10, ZONES[13][0], 13)

# =============================================================================
# CCS BLOCK, GAS METERING, OUTSIDE-FENCE FUEL CONTEXT
# =============================================================================
def build_ccs():
    pre = "CCS-"
    x0, y0 = P["ccs_origin_ft"]
    dd, dh = P["dcc_d_h_ft"]
    aL, aW, aH = P["absorber_ft"]
    rd, rh = P["regenerator_d_h_ft"]
    dcc = (x0 + 28, y0 + 300)
    ab = (x0 + 10, y0 + 120)          # absorber SW corner
    rg = (x0 + 130, y0 + 190)
    # direct-contact cooler
    m = MeshAcc(pre + "DCC", "ENCL")
    m.cyl(dcc[0], dcc[1], GZ + 4, dd / 2, dh, 32)
    m.cyl(dcc[0], dcc[1], GZ, dd / 2 + 2, 4, 32)
    m.cyl(dcc[0], dcc[1], GZ + 4 + dh, dd / 2, 6, 32, r2=4.0)
    m.build()
    # absorber (rectangular, Keadby envelope) with outlet stub at ccs_outlet_z
    a = MeshAcc(pre + "ABSORBER", "ENCL")
    a.box(ab[0], ab[1], GZ, ab[0] + aL, ab[1] + aW, aH)
    a.box(ab[0] + aL / 2 - 10, ab[1] + aW / 2 - 10, aH, ab[0] + aL / 2 + 10, ab[1] + aW / 2 + 10, P["ccs_outlet_z_ft"])
    a.build()
    s = MeshAcc(pre + "ABSORBER-STEEL", "STEEL")
    for y in range(int(ab[1]), int(ab[1] + aW) + 1, 20):
        for x in (ab[0] - 1.5, ab[0] + aL + 1.5):
            s.box(x - 1, y - 1, GZ, x + 1, y + 1, aH)
    for z in range(40, int(aH), 40):
        for x in (ab[0] - 1.5, ab[0] + aL + 1.5):
            s.box(x - 1, ab[1], z - 1, x + 1, ab[1] + aW, z)
    s.lattice(ab[0] + aL + 12, ab[1] + aW / 2, GZ, aH, 10, 10, r=0.4, panels=14)
    s.build()
    # regenerator (stripper) + reboiler
    r = MeshAcc(pre + "REGENERATOR", "ENCL")
    r.cyl(rg[0], rg[1], GZ + 4, rd / 2, rh, 32)
    r.cyl(rg[0], rg[1], GZ, rd / 2 + 2, 4, 32)
    r.cyl(rg[0], rg[1], GZ + 4 + rh, rd / 2, 6, 32, r2=3.0)
    r.cyl_between((rg[0] + rd / 2 + 4, rg[1] - 20, GZ + 8), (rg[0] + rd / 2 + 4, rg[1] + 20, GZ + 8), 5, 20)   # reboiler
    r.build()
    MeshAcc(pre + "REGEN-STEEL", "STEEL").lattice(rg[0] - rd / 2 - 8, rg[1], GZ, rh, 8, 8, r=0.35, panels=8).build()
    # compressor building, amine tank, heat exchanger skid
    MeshAcc(pre + "COMPRESSOR-BUILDING", "ENCL").box(x0, y0, GZ, x0 + 80, y0 + 40, GZ + 24).build()
    MeshAcc(pre + "AMINE-TANK", "ENCL").cyl(x0 + 140, y0 + 40, GZ, 15, 30, 32).build()
    hx = MeshAcc(pre + "HX-SKID", "STEEL")
    hx.box(x0 + 90, y0 + 90, GZ, x0 + 110, y0 + 100, GZ + 1)
    for k in range(3):
        hx.cyl_between((x0 + 92, y0 + 92 + k * 3, GZ + 3), (x0 + 108, y0 + 92 + k * 3, GZ + 3), 1.2, 12)
    hx.build()
    # process piping: rich / lean amine, CO2 to compressor, flue gas DCC -> absorber
    pp = CurveAcc(pre + "PIPING", "INSUL", 1.2)
    pp.add([(ab[0] + aL, ab[1] + 20, GZ + 10), (x0 + 100, ab[1] + 20, GZ + 10), (x0 + 100, y0 + 100, GZ + 10), (x0 + 100, y0 + 100, GZ + 3)])
    pp.add([(x0 + 100, y0 + 90, GZ + 3), (x0 + 100, y0 + 80, GZ + 10), (rg[0], y0 + 80, GZ + 10), (rg[0], rg[1] - rd / 2, GZ + 10)])
    pp.add([(rg[0] - rd / 2, rg[1], rh - 20), (ab[0] + aL / 2, rg[1], rh - 20), (ab[0] + aL / 2, ab[1] + aW, aH - 30)])
    pp.add([(rg[0], rg[1], GZ + 4 + rh + 6), (rg[0], rg[1], rh + 20), (rg[0], y0 + 60, rh + 20), (x0 + 40, y0 + 60, rh + 20), (x0 + 40, y0 + 60, GZ + 24)])
    pp.add([(x0 + 140, y0 + 40, GZ + 30), (x0 + 140, y0 + 70, GZ + 12), (x0 + 110, y0 + 95, GZ + 12), (x0 + 100, y0 + 95, GZ + 4)])
    pp.build()
    fd = CurveAcc(pre + "DCC-TO-ABSORBER-DUCT", "STEEL", 5)
    fd.add([(dcc[0], dcc[1] - dd / 2, GZ + 30), (dcc[0], ab[1] + aW + 6, GZ + 30), (dcc[0], ab[1] + aW + 6, 40), (ab[0] + aL / 2, ab[1] + aW + 6, 40), (ab[0] + aL / 2, ab[1] + aW - 4, 40)])
    fd.build()
    # CO2 export pipeline leaving the compressor building west/south (to pipeline outside the view)
    co2 = CurveAcc(pre + "CO2-EXPORT", "STEEL", 0.8)
    co2.add([(x0 + 80, y0 + 10, GZ + 3), (x0 + 165, y0 + 10, GZ + 3), (x0 + 165, y0 - 70, GZ + 3), (x0 + 165, y0 - 80, -3)])
    co2.build()
    # flue-gas collector duct from the three stacks, over the north road to the DCC
    z = P["flue_duct_z_ft"]
    rr = P["flue_duct_d_ft"] / 2
    yc = STACK_Y + STACK_D / 2 + 12
    yn = SH - PR_IN - ROAD_W / 2 - 12       # just south of the north perimeter road
    route = [(GT_X[0], yc), (GT_X[-1] + 20, yc), (GT_X[-1] + 20, yn), (dcc[0], yn), (dcc[0], dcc[1] + dd / 2 + 8)]
    du = CurveAcc(pre + "FLUE-DUCT", "STEEL", rr)
    du.add([(x, y, z) for x, y in route] + [(dcc[0], dcc[1] + dd / 2 + 8, GZ + 40), (dcc[0], dcc[1] + dd / 2 - 2, GZ + 40)])
    for ax in GT_X:
        du.add([(ax, STACK_Y + STACK_D / 2 + 6, z), (ax, yc, z)])
    du.build()
    sp = MeshAcc(pre + "FLUE-DUCT-SUPPORTS", "STEEL_DK")
    sp.pipe_supports(route, z - rr - 0.5, pitch=40, w=3.0)
    sp.build()
    MeshAcc(pre + "BOOSTER-FAN", "ENCL").box(GT_X[-1] + 8, yc + 30, GZ, GT_X[-1] + 32, yc + 60, GZ + 20).build()
    anchor(pre + "DCC", dcc[0], dcc[1], GZ + dh + 12, "Direct-contact cooler (flue-gas quench)", 14)
    anchor(pre + "ABSORBER", ab[0] + aL / 2, ab[1] + aW / 2, P["ccs_outlet_z_ft"] + 2, "CO2 absorber (amine) with treated-gas outlet", 14)
    anchor(pre + "REGENERATOR", rg[0], rg[1], rh + 12, "Regenerator (stripper) and reboiler", 14)
    anchor(pre + "COMPRESSOR", x0 + 40, y0 + 20, GZ + 26, "CO2 compression and dehydration building", 14)
    anchor(pre + "AMINE-TANK", x0 + 140, y0 + 40, GZ + 32, "Solvent storage tank", 14)
    anchor(pre + "HX", x0 + 100, y0 + 95, GZ + 6, "Lean / rich solvent heat exchanger", 14)
    anchor(pre + "FLUE-DUCT", GT_X[-1] + 20, (yc + yn) / 2, z + rr + 1, "Flue-gas collector duct from stacks", 14)
    anchor(pre + "BOOSTER-FAN", GT_X[-1] + 20, yc + 45, GZ + 22, "Flue-gas booster fan", 14)
    anchor(pre + "PIPING", x0 + 100, y0 + 80, GZ + 12, "Rich / lean solvent piping", 14)
    anchor(pre + "CO2-EXPORT", x0 + 165, y0 - 30, GZ + 5, "CO2 export pipeline (to storage, off view)", 14)
    anchor("ZONE-14", ab[0] + aL / 2, ab[1] + aW / 2, P["ccs_outlet_z_ft"] + 12, ZONES[14][0], 14)


def build_gasmet():
    pre = "GASMET-"
    x0, y0 = P["gasmet_origin_ft"]
    hL, hW, hH = P["gas_meter_ft"]
    n, td, th = P["process_tank_n_d_h_ft"]
    yp = P["pipeline_y_ft"]
    pr = P["pipeline_d_ft"] / 2
    MeshAcc(pre + "HOUSE", "ENCL").box(x0, y0 + 40, GZ, x0 + hL, y0 + 40 + hW, GZ + hH).build()
    tk = MeshAcc(pre + "PROCESS-TANKS", "ENCL")
    for k in range(n):
        cx = x0 + 75 + k * 35
        tk.cyl(cx, y0 + 80, GZ, td / 2, th, 28)
        tk.cyl(cx, y0 + 80, GZ + th, td / 2, 2, 28, r2=0.8)
    tk.build()
    # incoming pipeline: from fence, over the perimeter road on a pipe bridge, ESD, pig receiver, filters, meter runs, PRS, heater
    pl = CurveAcc(pre + "PIPELINE", "STEEL", pr)
    xr = SW - PR_IN
    pl.add([(SW - FENCE_IN + 2, yp, GZ + 3), (xr + 20, yp, GZ + 3), (xr + 16, yp, GZ + 18), (xr - 16, yp, GZ + 18), (xr - 20, yp, GZ + 3), (x0 + 160, yp, GZ + 3)])
    pl.add([(x0 + 160, yp, GZ + 3), (x0 + 100, yp, GZ + 3)])
    pl.build()
    br = MeshAcc(pre + "PIPE-BRIDGE", "STEEL")
    for x in (xr - 18, xr + 18):
        br.box(x - 1, yp - 1, GZ, x + 1, yp + 1, GZ + 17)
    br.pipe_supports([(x0 + 100, yp), (xr - 20, yp)], GZ + 2.5, pitch=20, w=1.5)
    br.pipe_supports([(xr + 20, yp), (SW - FENCE_IN + 2, yp)], GZ + 2.5, pitch=20, w=1.5)
    br.build()
    esd = MeshAcc(pre + "ESD-VALVE", "STEEL_DK")
    esd.box(x0 + 150, yp - 2, GZ + 1, x0 + 156, yp + 2, GZ + 5)
    esd.cyl(x0 + 153, yp, GZ + 5, 1.2, 4, 10)
    esd.build()
    pig = MeshAcc(pre + "PIG-RECEIVER", "STEEL")
    pig.cyl_between((x0 + 120, yp - 12, GZ + 3), (x0 + 140, yp - 12, GZ + 3), 1.6, 14)
    pig.cyl_between((x0 + 140, yp - 12, GZ + 3), (x0 + 142, yp - 12, GZ + 3), 2.0, 14)
    pig.box(x0 + 124, yp - 13, GZ, x0 + 126, yp - 11, GZ + 2).box(x0 + 136, yp - 13, GZ, x0 + 138, yp - 11, GZ + 2)
    pig.build()
    CurveAcc(pre + "PIG-BRANCH", "STEEL", pr * 0.8).add([(x0 + 130, yp, GZ + 3), (x0 + 130, yp - 12, GZ + 3)]).build()
    flt = MeshAcc(pre + "FILTER-SEPARATORS", "STEEL")
    for k in range(2):
        flt.cyl(x0 + 110, yp + 8 + k * 10, GZ, 2.5, 12, 16)
        flt.cyl(x0 + 110, yp + 8 + k * 10, GZ + 12, 2.5, 2, 16, r2=0.5)
    flt.build()
    mr = CurveAcc(pre + "METER-RUNS", "STEEL", 0.8)
    for k in range(3):
        mr.add([(x0 + 100, yp - 8 + k * 8, GZ + 3), (x0 + 50, yp - 8 + k * 8, GZ + 3)])
    mr.add([(x0 + 100, yp - 8, GZ + 3), (x0 + 100, yp + 8, GZ + 3)])
    mr.add([(x0 + 50, yp - 8, GZ + 3), (x0 + 50, yp + 8, GZ + 3)])
    mr.build()
    of = MeshAcc(pre + "ORIFICE-FLANGES", "STEEL_DK")
    for k in range(3):
        of.cyl_between((x0 + 74, yp - 8 + k * 8, GZ + 3), (x0 + 76, yp - 8 + k * 8, GZ + 3), 1.4, 12)
    of.build()
    MeshAcc(pre + "PRESSURE-REDUCTION", "STEEL").box(x0 + 30, yp - 12, GZ, x0 + 46, yp - 4, GZ + 6).build()
    ht = MeshAcc(pre + "FUEL-GAS-HEATER", "ENCL")
    ht.box(x0 + 8, yp - 12, GZ, x0 + 24, yp - 4, GZ + 8)
    ht.cyl(x0 + 20, yp - 8, GZ + 8, 0.8, 10, 10)
    ht.build()
    # fuel-gas header to the hall: along y 395 west, then north to the hall SE corner (pipe bridges over the N-S roads)
    hd = CurveAcc("GAS-HEADER-SITE", "STEEL", 0.9)
    xs = 392
    pts = [(x0 + 50, yp, GZ + 3), (x0 + 8, yp, GZ + 3), (x0 - 10, yp, GZ + 3), (x0 - 10, xs, GZ + 3)]
    x = x0 - 10
    for rx in sorted(P["ns_roads_x_ft"], reverse=True):
        if rx < x and rx > HX1 - 20:
            pts += [(rx + 18, xs, GZ + 3), (rx + 14, xs, GZ + 18), (rx - 14, xs, GZ + 18), (rx - 18, xs, GZ + 3)]
    pts += [(HX1 - 9, xs, GZ + 3), (HX1 - 9, HY0 - 12, GZ + 3), (HX1 - 9, HY0 - 8, 12), (HX1 - 9, HY0 + 1, 12)]
    hd.add(pts)
    hd.build()
    hs = MeshAcc("GAS-HEADER-SUPPORTS", "STEEL_DK")
    hs.pipe_supports([(x0 - 10, yp), (x0 - 10, xs)], GZ + 2.4, pitch=20, w=1.2)
    hs.pipe_supports([(x0 - 10, xs), (HX1 - 9, xs)], GZ + 2.4, pitch=20, w=1.2)
    hs.pipe_supports([(HX1 - 9, xs), (HX1 - 9, HY0 - 12)], GZ + 2.4, pitch=20, w=1.2)
    for rx in P["ns_roads_x_ft"]:
        if HX1 - 20 < rx < x0 - 10:
            hs.box(rx - 17, xs - 1, GZ, rx - 15, xs + 1, GZ + 17).box(rx + 15, xs - 1, GZ, rx + 17, xs + 1, GZ + 17)
    hs.build()
    anchor(pre + "HOUSE", x0 + hL / 2, y0 + 40 + hW / 2, GZ + hH + 1, "Gas metering / analyser house", 15)
    anchor(pre + "TANKS", x0 + 75, y0 + 80, GZ + th + 4, "Process-water tanks (non-fuel)", 15)
    anchor(pre + "PIPELINE", xr + 30, yp, GZ + 6, "Incoming transmission pipeline (fence crossing)", 15)
    anchor(pre + "ESD", x0 + 153, yp, GZ + 10, "Emergency shutdown valve", 15)
    anchor(pre + "PIG-RECEIVER", x0 + 130, yp - 12, GZ + 6, "Pig receiver", 15)
    anchor(pre + "FILTERS", x0 + 110, yp + 13, GZ + 15, "Filter / separators", 15)
    anchor(pre + "METER-RUNS", x0 + 75, yp, GZ + 6, "Custody-transfer meter runs", 15)
    anchor(pre + "PRESSURE-REDUCTION", x0 + 38, yp - 8, GZ + 7, "Pressure-reduction skid", 15)
    anchor(pre + "HEATER", x0 + 16, yp - 8, GZ + 10, "Fuel-gas performance heater", 15)
    anchor("GAS-HEADER", x0 - 10, 480, GZ + 6, "Fuel-gas header to the turbine hall", 15)
    anchor("ZONE-15", x0 + 60, y0 + 50, GZ + th + 10, ZONES[15][0], 15)


def build_fuelgas():
    pre = "FUELGAS-"
    x0 = SW
    W = P["outside_strip_ft"]
    yp = P["pipeline_y_ft"]
    pr = P["pipeline_d_ft"] / 2
    ld, lh = P["lng_d_h_ft"]
    hL, hW, hH = P["h2_module_ft"]
    # pipeline continuing east out of the context strip
    pl = CurveAcc(pre + "PIPELINE", "STEEL", pr)
    pl.add([(x0 + W + 60, yp, -4), (x0 + W + 40, yp, -4), (x0 + W + 30, yp, GZ + 3), (SW - FENCE_IN + 2, yp, GZ + 3)])
    pl.build()
    sp = MeshAcc(pre + "PIPE-SUPPORTS", "STEEL_DK")
    sp.pipe_supports([(x0 + W + 30, yp), (SW - FENCE_IN + 2, yp)], GZ + 2.4, pitch=20, w=1.5)
    sp.build()
    bv = MeshAcc(pre + "BLOCK-VALVE", "STEEL_DK")
    for k in range(2):
        bv.box(x0 + 90 + k * 12, yp - 2, GZ + 1, x0 + 96 + k * 12, yp + 2, GZ + 5)
        bv.cyl(x0 + 93 + k * 12, yp, GZ + 5, 1.2, 4, 10)
    bv.build()
    MeshAcc(pre + "VALVE-FENCE", "STEEL_DK").box(x0 + 84, yp - 10, GZ, x0 + 114, yp - 9.7, GZ + 6).box(x0 + 84, yp + 9.7, GZ, x0 + 114, yp + 10, GZ + 6).build()
    MeshAcc(pre + "MARKER-POST", "ENCL").box(x0 + W + 28, yp + 4, GZ, x0 + W + 29, yp + 5, GZ + 5).build()
    # LNG supply: horizontal vessel on saddles, vaporiser, tie-in to the header
    lng = MeshAcc(pre + "LNG-VESSEL", "ENCL")
    lc = (x0 + 140, 700)
    lng.cyl_between((lc[0] - lh / 2, lc[1], GZ + ld / 2 + 3), (lc[0] + lh / 2, lc[1], GZ + ld / 2 + 3), ld / 2, 28)
    lng.sphere(lc[0] - lh / 2, lc[1], GZ + ld / 2 + 3, ld / 2, 16)
    lng.sphere(lc[0] + lh / 2, lc[1], GZ + ld / 2 + 3, ld / 2, 16)
    for dx in (-lh / 3, lh / 3):
        lng.box(lc[0] + dx - 2, lc[1] - ld / 2 - 1, GZ, lc[0] + dx + 2, lc[1] + ld / 2 + 1, GZ + 5)
    lng.build()
    vap = MeshAcc(pre + "VAPORISER", "STEEL")
    vap.box(x0 + 90, 680, GZ, x0 + 110, 690, GZ + 1)
    for k in range(6):
        vap.box(x0 + 92 + k * 3, 681, GZ + 1, x0 + 93.5 + k * 3, 689, GZ + 12)
    vap.build()
    tie = CurveAcc(pre + "LNG-TIE-IN", "STEEL", 0.6)
    tie.add([(lc[0] - lh / 2 - 2, lc[1], GZ + 6), (x0 + 112, 685, GZ + 6), (x0 + 88, 685, GZ + 6), (x0 + 50, 685, GZ + 3), (x0 + 50, yp, GZ + 3), (x0 + 20, yp, GZ + 3)])
    tie.build()
    # hydrogen supply: tube module + compressor + tie-in
    h2 = MeshAcc(pre + "H2-MODULE", "STEEL")
    hc = (x0 + 130, 470)
    h2.box(hc[0], hc[1], GZ, hc[0] + hL, hc[1] + hW, GZ + 1)
    for k in range(4):
        for rrow in range(2):
            h2.cyl_between((hc[0] + 1, hc[1] + 1.5 + k * 1.7, GZ + 2 + rrow * 3.4), (hc[0] + hL - 1, hc[1] + 1.5 + k * 1.7, GZ + 2 + rrow * 3.4), 0.8, 12)
    for x in (hc[0] + 0.5, hc[0] + hL - 0.5):
        h2.box(x - 0.5, hc[1], GZ, x + 0.5, hc[1] + hW, GZ + hH)
    h2.box(hc[0], hc[1], GZ + hH - 0.3, hc[0] + hL, hc[1] + hW, GZ + hH)
    h2.build()
    MeshAcc(pre + "H2-COMPRESSOR", "ENCL").box(x0 + 90, 470, GZ, x0 + 102, 478, GZ + 8).build()
    h2t = CurveAcc(pre + "H2-TIE-IN", "STEEL", 0.4)
    h2t.add([(hc[0], hc[1] + 4, GZ + 3), (x0 + 102, 474, GZ + 3), (x0 + 90, 474, GZ + 3), (x0 + 40, 474, GZ + 3), (x0 + 40, yp - 4, GZ + 3), (x0 + 20, yp - 4, GZ + 3), (x0 + 20, yp, GZ + 3)])
    h2t.build()
    MeshAcc(pre + "BLENDING-SKID", "STEEL").box(x0 + 14, yp - 14, GZ, x0 + 26, yp - 6, GZ + 6).build()
    f = MeshAcc(pre + "FENCE", "STEEL_DK")
    fence_run(f, [(x0 + 80, 660), (x0 + 200, 660), (x0 + 200, 740), (x0 + 80, 740), (x0 + 80, 660)], h=8)
    fence_run(f, [(x0 + 80, 455), (x0 + 200, 455), (x0 + 200, 500), (x0 + 80, 500), (x0 + 80, 455)], h=8)
    f.build()
    anchor(pre + "PIPELINE", x0 + 60, yp, GZ + 6, "Transmission pipeline supply (primary)", 15)
    anchor(pre + "BLOCK-VALVE", x0 + 99, yp, GZ + 10, "Pipeline block-valve station", 15)
    anchor(pre + "LNG-VESSEL", lc[0], lc[1], GZ + ld + 5, "LNG storage vessel (alternative supply)", 15)
    anchor(pre + "VAPORISER", x0 + 100, 685, GZ + 13, "Ambient-air LNG vaporiser", 15)
    anchor(pre + "H2-MODULE", hc[0] + hL / 2, hc[1] + hW / 2, GZ + hH + 2, "Hydrogen tube storage module (alternative / blend)", 15)
    anchor(pre + "H2-COMPRESSOR", x0 + 96, 474, GZ + 9, "Hydrogen compressor", 15)
    anchor(pre + "BLENDING-SKID", x0 + 20, yp - 10, GZ + 7, "Supply tie-in / blending skid", 15)

# =============================================================================
# SITE CABLE CORRIDOR + MV DISTRIBUTION
# =============================================================================
def build_corridor():
    pre = "CORR-"
    y0 = CORR_Y
    x0, x1 = CORR_X0, CORR_X1
    zp, zc = P["tray_power_control_z_ft"]
    yt = y0 + 18
    # tray segments between the N-S road crossings; at each crossing the cables dive into the duct bank
    cuts = sorted(rx for rx in P["ns_roads_x_ft"] if x0 < rx < x1)
    segs, cur = [], x0
    for rx in cuts:
        segs.append((cur, rx - 16)); cur = rx + 16
    segs.append((cur, x1))
    tp = MeshAcc(pre + "TRAY-POWER", "STEEL")
    tc = MeshAcc(pre + "TRAY-CONTROL", "STEEL")
    for (a, b) in segs:
        tp.tray([(a, yt), (b, yt)], zp, width=3.0, posts=True)
        tc.tray([(a, yt), (b, yt)], zc, width=2.0, posts=False)
    tp.build(); tc.build()
    pits = MeshAcc(pre + "ROAD-CROSSING-PITS", "CONC", below=True)
    pitc = MeshAcc(pre + "ROAD-CROSSING-COVERS", "STEEL_DK")
    for rx in cuts:
        for xx in (rx - 19, rx + 19):
            pits.box(xx - 3, yt - 3, -6, xx + 3, yt + 3, GZ)
            pitc.box(xx - 3, yt - 3, GZ, xx + 3, yt + 3, GZ + 0.3)
    pits.build(); pitc.build()
    def run_with_dips(yy, zz):
        pts = [(x0, yy, zz)]
        for rx in cuts:
            pts += [(rx - 16, yy, zz), (rx - 19, yy, -3.5), (rx + 19, yy, -3.5), (rx + 16, yy, zz)]
        pts.append((x1, yy, zz))
        return pts
    cp = CurveAcc(pre + "CABLES-POWER", "CABLE", 0.12)
    for k in range(6):
        cp.add(run_with_dips(yt - 1.2 + k * 0.28, zp + 0.3))
    for k in range(6):
        cp.add(run_with_dips(yt + 0.5 + k * 0.15, zp + 0.25))
    cp.build()
    cc = CurveAcc(pre + "CABLES-CONTROL", "CABLE", 0.045)
    for k in range(8):
        cc.add(run_with_dips(yt - 0.7 + k * 0.2, zc + 0.25))
    cc.build()
    # duct bank below grade with conduits, manholes every 200 ft (covers visible)
    zd = P["duct_z_ft"]
    yd = y0 + 8
    MeshAcc(pre + "DUCTBANK", "DUCT", below=True).box(x0, yd - 3, zd - 2, x1, yd + 3, zd + 1).build()
    cd = CurveAcc(pre + "CONDUITS", "STEEL_DK", 0.25, below=True)
    for r in range(2):
        for k in range(4):
            cd.add([(x0, yd - 2.2 + k * 1.4, zd - 1.2 + r * 1.4), (x1, yd - 2.2 + k * 1.4, zd - 1.2 + r * 1.4)])
    cd.build()
    dc = CurveAcc(pre + "DUCTBANK-CABLES", "CABLE", 0.12, below=True)
    for k in range(4):
        dc.add([(x0, yd - 2.2 + k * 1.4, zd - 1.2), (x1, yd - 2.2 + k * 1.4, zd - 1.2)])
    dc.build()
    mh = MeshAcc(pre + "MANHOLES", "CONC", below=True)
    cov = MeshAcc(pre + "MANHOLE-COVERS", "STEEL_DK")
    for x in range(int(x0) + 100, int(x1), 200):
        mh.box(x - 4, yd - 4, zd - 4, x + 4, yd + 4, GZ)
        cov.cyl(x, yd, GZ, 1.6, 0.2, 16)
    mh.build(); cov.build()
    # MV distribution: ring-main switchgear kiosks + pad-mount transformers at each lateral, laterals north
    ks = MeshAcc(pre + "MV-SWITCHGEAR", "ENCL")
    px = MeshAcc(pre + "PADMOUNT-TX", "ENCL")
    lat = MeshAcc(pre + "LATERAL-TRAYS", "STEEL")
    lc = CurveAcc(pre + "LATERAL-CABLES", "CABLE", 0.12)
    gr = CurveAcc(pre + "GROUND-RISERS", "CABLE", 0.08)
    ends = []
    dest = {410: (P["ehouse_origin_ft"][1] - 2, "e-house"), 1180: (P["mcc_origin_ft"][1] - 8, "MCC building"),
            1430: (P["chill_origin_ft"][1] - 4, "chillers / ACC MCC"), 1735: (P["ccs_origin_ft"][1] - 4, "CCS block")}
    for lx in P["mv_laterals_x_ft"]:
        ky = y0 + CORR_W + 6
        ks.box(lx - 4, ky, GZ, lx + 4, ky + 4, GZ + 8)
        px.box(lx + 8, ky, GZ, lx + 14, ky + 6, GZ + 6)
        for k in range(3):
            px.cyl(lx + 9.5 + k * 1.5, ky + 3, GZ + 6, 0.3, 1.5, 8)
        yend = dest[lx][0]
        lat.tray([(lx, yt), (lx, ky)], zp, width=2.5, posts=False)
        lat.tray([(lx, ky + 4), (lx, yend)], zp, width=2.5, posts=True)
        for k in range(3):
            p0 = (lx - 0.5 + k * 0.5, ky, GZ + 4)
            lc.add([(lx - 0.5 + k * 0.5, yt, zp + 0.3), p0])
            ends.append((p0, (0, -1, 0)))
            p1 = (lx - 0.5 + k * 0.5, yend, zp + 0.3)
            lc.add([(lx - 0.5 + k * 0.5, ky + 4, GZ + 4), (lx - 0.5 + k * 0.5, ky + 6, zp + 0.3), p1])
            ends.append((p1, (0, 1, 0)))
        g0 = (lx + 5, ky - 1, GZ + 1.5)
        gr.add([(lx + 5, ky - 1, P["earth_z_pitch_ft"][0]), g0])
        ends.append((g0, (0, 0, 1)))
        anchor(pre + "MV-SWGR-%d" % lx, lx, ky + 2, GZ + 9, "MV ring-main switchgear (%s)" % dest[lx][1], 16)
    ks.build(); px.build(); lat.build(); lc.build(); gr.build()
    cable_end_caps(pre + "CABLE-ENDS", ends, r=0.16, L=0.5)
    # e-house to corridor lateral is covered by lx=410 (ends at the e-house south wall)
    anchor(pre + "TRAY-POWER", 1300, yt, zp + 1.5, "Power tray (lower tier: MV / LV feeders)", 16)
    anchor(pre + "TRAY-CONTROL", 1250, yt, zc + 1.5, "Control tray (upper tier: I&C, fibre)", 16)
    anchor(pre + "DUCTBANK", 1300, yd, zd + 1.5, "Concrete duct bank (below grade)", 16)
    anchor(pre + "CONDUITS", 1250, yd, zd - 1, "Conduits with feeder cables (below grade)", 16)
    anchor(pre + "MANHOLE", 1300, yd, GZ + 0.5, "Pull-pit / manhole cover", 16)
    anchor(pre + "ROAD-CROSSING", 1407 - 19, yt, GZ + 1, "Road crossing: cables dive into the duct bank", 16)
    anchor(pre + "PADMOUNT", 1180 + 11, y0 + CORR_W + 9, GZ + 7, "Pad-mount MV/LV transformer", 16)
    anchor(pre + "LATERAL", 1180, y0 + 90, zp + 1.5, "Lateral tray to building", 16)
    anchor(pre + "GROUND-RISER", 1185, y0 + CORR_W + 5, GZ + 2, "Grounding riser to earth grid (copper connector)", 16)
    anchor(pre + "CABLE-ENDS", 1181, y0 + CORR_W + 6, GZ + 4.5, "Cable end caps (copper)", 16)
    anchor("ZONE-16", 1000, yt, zc + 6, ZONES[16][0], 16)


# =============================================================================
# DETAIL PASS  --  cladding, doors, louvres, rails, ladders, skids, hardware
# =============================================================================
def _m_rail(self, pts, z, h=3.5, pitch=5.0, r=0.07, skip=None, toe=True):
    """handrail (posts + top rail + mid rail + toe board) along a polyline of (x, y) at deck height z."""
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-6:
            continue
        n = max(1, int(round(L / pitch)))
        for i in range(n + 1):
            t = i / n
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if skip and skip(px, py):
                continue
            self.seg((px, py, z), (px, py, z + h), r, 4)
        for hh in (h, h * 0.5):
            self.seg((a[0], a[1], z + hh), (b[0], b[1], z + hh), r, 4)
        if toe:
            self.seg((a[0], a[1], z + 0.2), (b[0], b[1], z + 0.2), r * 1.6, 4)
    return self

def _m_ladder(self, x, y, z0, z1, face=(0, -1), cage=True, w=1.6):
    """vertical fixed ladder; `face` is the horizontal direction the climber faces away from... (points away from the wall)."""
    fx, fy = face
    px, py = -fy, fx
    for s in (-1, 1):
        self.seg((x + px * s * w / 2, y + py * s * w / 2, z0), (x + px * s * w / 2, y + py * s * w / 2, z1), 0.07, 4)
    k = 1.0
    while z0 + k < z1:
        self.seg((x - px * w / 2, y - py * w / 2, z0 + k), (x + px * w / 2, y + py * w / 2, z0 + k), 0.05, 4)
        k += 1.0
    if cage and z1 - z0 > 8:
        zc = z0 + 7.0
        cx, cy = x + fx * 1.1, y + fy * 1.1
        base = math.atan2(fy, fx)
        while zc < z1:
            pts = []
            for j in range(9):
                a = base - math.radians(100) + math.radians(200) * j / 8
                pts.append((cx + 1.7 * math.cos(a) - fx * 0.0, cy + 1.7 * math.sin(a), zc))
            for p0, p1 in zip(pts[:-1], pts[1:]):
                self.seg(p0, p1, 0.04, 4)
            zc += 2.5
        for j in (0, 4, 8):
            a = base - math.radians(100) + math.radians(200) * j / 8
            self.seg((cx + 1.7 * math.cos(a), cy + 1.7 * math.sin(a), z0 + 7.0), (cx + 1.7 * math.cos(a), cy + 1.7 * math.sin(a), z1), 0.04, 4)
    return self

def _m_ribs_x(self, y_face, sign, x0, x1, z0, z1, pitch=6.0, w=0.5, d=0.4, avoid=()):
    """vertical cladding ribs on a wall running along x (outer face at y_face, outside is `sign` * y)."""
    x = x0 + pitch / 2
    while x < x1:
        if not any(a - 1.0 < x + w / 2 < b + 1.0 for a, b in avoid):
            ya, yb = (y_face, y_face + d) if sign > 0 else (y_face - d, y_face)
            self.box(x, ya, z0, x + w, yb, z1)
        x += pitch
    return self

def _m_ribs_y(self, x_face, sign, y0, y1, z0, z1, pitch=6.0, w=0.5, d=0.4, avoid=()):
    y = y0 + pitch / 2
    while y < y1:
        if not any(a - 1.0 < y + w / 2 < b + 1.0 for a, b in avoid):
            xa, xb = (x_face, x_face + d) if sign > 0 else (x_face - d, x_face)
            self.box(xa, y, z0, xb, y + w, z1)
        y += pitch
    return self

def _m_louvre_x(self, x0, x1, y_face, sign, z0, z1, slat=0.5, d=0.5):
    """louvre panel on a wall along x: frame + tilted slats."""
    ya, yb = (y_face, y_face + d) if sign > 0 else (y_face - d, y_face)
    self.box(x0, ya, z0, x0 + 0.25, yb, z1).box(x1 - 0.25, ya, z0, x1, yb, z1)
    self.box(x0, ya, z0, x1, yb, z0 + 0.25).box(x0, ya, z1 - 0.25, x1, yb, z1)
    z = z0 + 0.4
    sd = sign * d
    while z < z1 - 0.4:
        self.hexa([(x0 + 0.2, y_face, z), (x1 - 0.2, y_face, z), (x1 - 0.2, y_face + sd, z - 0.22), (x0 + 0.2, y_face + sd, z - 0.22),
                   (x0 + 0.2, y_face, z + 0.09), (x1 - 0.2, y_face, z + 0.09), (x1 - 0.2, y_face + sd, z - 0.13), (x0 + 0.2, y_face + sd, z - 0.13)])
        z += slat
    return self

def _m_louvre_y(self, y0, y1, x_face, sign, z0, z1, slat=0.5, d=0.5):
    xa, xb = (x_face, x_face + d) if sign > 0 else (x_face - d, x_face)
    self.box(xa, y0, z0, xb, y0 + 0.25, z1).box(xa, y1 - 0.25, z0, xb, y1, z1)
    self.box(xa, y0, z0, xb, y1, z0 + 0.25).box(xa, y0, z1 - 0.25, xb, y1, z1)
    z = z0 + 0.4
    sd = sign * d
    while z < z1 - 0.4:
        self.hexa([(x_face, y0 + 0.2, z), (x_face, y1 - 0.2, z), (x_face + sd, y1 - 0.2, z - 0.22), (x_face + sd, y0 + 0.2, z - 0.22),
                   (x_face, y0 + 0.2, z + 0.09), (x_face, y1 - 0.2, z + 0.09), (x_face + sd, y1 - 0.2, z - 0.13), (x_face + sd, y0 + 0.2, z - 0.13)])
        z += slat
    return self

def _m_door_x(self, cx, y_face, sign, z0, w=3.4, h=7.0):
    """personnel door on a wall along x: frame, leaf, kick plate, handle, small vision panel."""
    ya, yb = (y_face, y_face + 0.35) if sign > 0 else (y_face - 0.35, y_face)
    self.box(cx - w / 2 - 0.3, ya, z0, cx - w / 2, yb, z0 + h + 0.3).box(cx + w / 2, ya, z0, cx + w / 2 + 0.3, yb, z0 + h + 0.3)
    self.box(cx - w / 2 - 0.3, ya, z0 + h, cx + w / 2 + 0.3, yb, z0 + h + 0.3)
    la, lb = (y_face, y_face + 0.2) if sign > 0 else (y_face - 0.2, y_face)
    self.box(cx - w / 2, la, z0, cx + w / 2, lb, z0 + h)
    ha, hb = (y_face + 0.2, y_face + 0.5) if sign > 0 else (y_face - 0.5, y_face - 0.2)
    self.box(cx - w / 2 + 0.15, ha, z0, cx + w / 2 - 0.15, hb, z0 + 0.9)                      # kick plate
    self.box(cx + w / 2 - 0.8, ha, z0 + 3.2, cx + w / 2 - 0.3, hb, z0 + 3.5)                  # handle
    self.box(cx - w / 2 + 0.6, ha, z0 + 4.6, cx + w / 2 - 0.6, hb, z0 + 6.0)                  # vision / signage panel
    return self

def _m_door_y(self, cy, x_face, sign, z0, w=3.4, h=7.0):
    xa, xb = (x_face, x_face + 0.35) if sign > 0 else (x_face - 0.35, x_face)
    self.box(xa, cy - w / 2 - 0.3, z0, xb, cy - w / 2, z0 + h + 0.3).box(xa, cy + w / 2, z0, xb, cy + w / 2 + 0.3, z0 + h + 0.3)
    self.box(xa, cy - w / 2 - 0.3, z0 + h, xb, cy + w / 2 + 0.3, z0 + h + 0.3)
    la, lb = (x_face, x_face + 0.2) if sign > 0 else (x_face - 0.2, x_face)
    self.box(la, cy - w / 2, z0, lb, cy + w / 2, z0 + h)
    ha, hb = (x_face + 0.2, x_face + 0.5) if sign > 0 else (x_face - 0.5, x_face - 0.2)
    self.box(ha, cy - w / 2 + 0.15, z0, hb, cy + w / 2 - 0.15, z0 + 0.9)
    self.box(ha, cy + w / 2 - 0.8, z0 + 3.2, hb, cy + w / 2 - 0.3, z0 + 3.5)
    self.box(ha, cy - w / 2 + 0.6, z0 + 4.6, hb, cy + w / 2 - 0.6, z0 + 6.0)
    return self

def _m_rollup_x(self, cx, y_face, sign, z0, w=12.0, h=14.0):
    """roller shutter door: guides, slats, hood, bottom bar."""
    def yy(a, b):
        return (y_face + a, y_face + b) if sign > 0 else (y_face - b, y_face - a)
    ya, yb = yy(0.0, 0.5)
    self.box(cx - w / 2 - 0.5, ya, z0, cx - w / 2, yb, z0 + h + 1.0).box(cx + w / 2, ya, z0, cx + w / 2 + 0.5, yb, z0 + h + 1.0)
    ya, yb = yy(0.0, 0.25)
    z = z0
    while z < z0 + h - 0.2:
        self.box(cx - w / 2, ya, z, cx + w / 2, yb, z + 0.42)
        z += 0.5
    ya, yb = yy(0.0, 0.9)
    self.box(cx - w / 2 - 0.5, ya, z0 + h, cx + w / 2 + 0.5, yb, z0 + h + 1.4)                  # hood
    ya, yb = yy(0.25, 0.5)
    self.box(cx - w / 2, ya, z0, cx + w / 2, yb, z0 + 0.4)                                      # bottom bar
    return self

def _m_rollup_y(self, cy, x_face, sign, z0, w=12.0, h=14.0):
    def xx(a, b):
        return (x_face + a, x_face + b) if sign > 0 else (x_face - b, x_face - a)
    xa, xb = xx(0.0, 0.5)
    self.box(xa, cy - w / 2 - 0.5, z0, xb, cy - w / 2, z0 + h + 1.0).box(xa, cy + w / 2, z0, xb, cy + w / 2 + 0.5, z0 + h + 1.0)
    xa, xb = xx(0.0, 0.25)
    z = z0
    while z < z0 + h - 0.2:
        self.box(xa, cy - w / 2, z, xb, cy + w / 2, z + 0.42)
        z += 0.5
    xa, xb = xx(0.0, 0.9)
    self.box(xa, cy - w / 2 - 0.5, z0 + h, xb, cy + w / 2 + 0.5, z0 + h + 1.4)
    return self

def _m_stiff_ring(self, cx, cy, z, r, h=0.45, out=0.3, n=28):
    self.cyl(cx, cy, z, r + out, h, n)
    return self

MeshAcc.rail = _m_rail
MeshAcc.ladder = _m_ladder
MeshAcc.ribs_x = _m_ribs_x
MeshAcc.ribs_y = _m_ribs_y
MeshAcc.louvre_x = _m_louvre_x
MeshAcc.louvre_y = _m_louvre_y
MeshAcc.door_x = _m_door_x
MeshAcc.door_y = _m_door_y
MeshAcc.rollup_x = _m_rollup_x
MeshAcc.rollup_y = _m_rollup_y
MeshAcc.stiff_ring = _m_stiff_ring


def apron(name, x0, y0, x1, y1, mat="CONC"):
    """small concrete landing / apron slab (top at pad level)."""
    MeshAcc(name, mat).box(x0, y0, 0.0, x1, y1, GZ + 0.05).build()


def blocked(x, y, margin=2.5, zmax=25.0):
    """True if (x, y) lies inside the plan bbox of any built solid (used to keep site furniture clear of equipment)."""
    for r in REG:
        if r["kind"] == "anchor" or r["below_grade"]:
            continue
        n = r["name"]
        if n.startswith(("SITE-BACKDROP", "SITE-GROUND", "SITE-PAD", "SITE-ROAD", "SITE-EARTHGRID", "FUELGAS-GROUND", "SWYD-PAD",
                         "SWYD-GRID", "GENTIE-CONDUCTORS", "GENTIE-SHIELD", "GENTIE-UG", "WATER-POND")):
            continue
        b = r["bbox"]
        if b[2] > zmax:
            continue
        if b[0] - margin <= x <= b[3] + margin and b[1] - margin <= y <= b[4] + margin and b[5] > 0.6:
            # long thin objects (fences, trays, pipes) only block at their own footprint; bbox test is conservative
            return True
    return False


# ---- turbine hall ------------------------------------------------------------------------
def detail_hall():
    x0, y0, x1, y1 = HX0, HY0, HX1, HY1
    ipb_x = [(ax - 8, ax + 8) for ax in GSU_X]
    inlet_x = [(ax + P["inlet_offset_x_ft"] - 7.5, ax + P["inlet_offset_x_ft"] + 7.5) for ax in GT_X]
    gas_x = [(x1 - 12, x1 - 6)]
    exh_x = [(ax - 11, ax + 11) for ax in GT_X] + [(ST_X - 6, ST_X + 6)]
    HH_ = HH
    # cladding ribs on every wall (south ones belong to the removable south-wall part)
    MeshAcc("HALL-WALL-S-RIBS", "ENCL", cutaway=True).ribs_x(y0, -1, x0, x1, GZ, HH_ - 0.5, 6.0, 0.5, 0.4, ipb_x + inlet_x + gas_x + [(555, 565), (685, 695), (795, 805), (968, 982)]).build()
    MeshAcc("HALL-WALL-N-RIBS", "ENCL").ribs_x(y1, 1, x0, x1, GZ, HH_ - 0.5, 6.0, 0.5, 0.4, exh_x).build()
    MeshAcc("HALL-WALL-W-RIBS", "ENCL").ribs_y(x0, -1, y0, y1, GZ, HH_ - 0.5, 6.0, 0.5, 0.4, [(674, 686), (714, 726), (754, 766)]).build()
    MeshAcc("HALL-WALL-E-RIBS", "ENCL").ribs_y(x1, 1, y0, y1, GZ, HH_ - 0.5, 6.0, 0.5, 0.4, [(715, 745), (674, 686), (774, 786)]).build()
    # base course and eaves band
    for nm, pts in (("S", (x0, y0 - 0.5, x1, y0)), ("N", (x0, y1, x1, y1 + 0.5))):
        MeshAcc("HALL-WALL-%s-PLINTH" % nm, "CONC", cutaway=(nm == "S")).box(pts[0], pts[1], GZ, pts[2], pts[3], GZ + 3.0).box(pts[0], pts[1] - (0.1 if nm == "S" else 0), HH_ - 2.0, pts[2], pts[3] + (0.1 if nm == "N" else 0), HH_).build()
    # doors
    dS = MeshAcc("HALL-WALL-S-DOORS", "STEEL", cutaway=True)
    for cx in (560, 690, 800):
        dS.door_x(cx, y0, -1, GZ)
    dS.rollup_x(975, y0, -1, GZ, 14.0, 16.0)
    dS.build()
    dW = MeshAcc("HALL-WALL-W-DOORS", "STEEL")
    dW.door_y(680, x0, -1, GZ).door_y(760, x0, -1, GZ).rollup_y(720, x0, -1, GZ, 12.0, 15.0)
    dW.build()
    dE = MeshAcc("HALL-WALL-E-DOORS", "STEEL")
    dE.door_y(680, x1, 1, GZ).door_y(780, x1, 1, GZ)
    dE.build()
    for (nx_, ny_, sx, sy) in ((560, y0 - 5, 6, 4), (690, y0 - 5, 6, 4), (800, y0 - 5, 6, 4), (975, y0 - 9, 18, 8)):
        apron("HALL-APRON-S-%d" % nx_, nx_ - sx / 2, ny_ - sy / 2, nx_ + sx / 2, ny_ + sy / 2)
    # louvres high on the long walls
    lS = MeshAcc("HALL-WALL-S-LOUVRES", "STEEL", cutaway=True)
    lN = MeshAcc("HALL-WALL-N-LOUVRES", "STEEL")
    for k in range(9):
        xs = x0 + 30 + k * 60
        lS.louvre_x(xs, xs + 24, y0, -1, HH_ - 22, HH_ - 8)
        lN.louvre_x(xs, xs + 24, y1, 1, HH_ - 22, HH_ - 8)
    lS.build(); lN.build()
    # standing-seam roof ribs, eaves gutters and downpipes
    ym = (y0 + y1) / 2.0
    ridge = HH_ + 8
    rr = MeshAcc("HALL-ROOF-RIBS", "ENCL", cutaway=True)
    x = x0 + 3
    while x < x1:
        rr.hexa([(x, y0 - 1, HH_ + 1), (x + 0.4, y0 - 1, HH_ + 1), (x + 0.4, ym, ridge), (x, ym, ridge),
                 (x, y0 - 1, HH_ + 1.35), (x + 0.4, y0 - 1, HH_ + 1.35), (x + 0.4, ym, ridge + 0.35), (x, ym, ridge + 0.35)])
        rr.hexa([(x, ym, ridge), (x + 0.4, ym, ridge), (x + 0.4, y1 + 1, HH_ + 1), (x, y1 + 1, HH_ + 1),
                 (x, ym, ridge + 0.35), (x + 0.4, ym, ridge + 0.35), (x + 0.4, y1 + 1, HH_ + 1.35), (x, y1 + 1, HH_ + 1.35)])
        x += 5.0
    rr.build()
    gu = MeshAcc("HALL-ROOF-GUTTER", "STEEL", cutaway=True)
    gu.box(x0 - 1, y0 - 2.4, HH_ - 0.6, x1 + 1, y0 - 1, HH_ + 0.4).box(x0 - 1, y1 + 1, HH_ - 0.6, x1 + 1, y1 + 2.4, HH_ + 0.4)
    gu.build()
    dpS = MeshAcc("HALL-WALL-S-DOWNPIPES", "STEEL", cutaway=True)
    dpN = MeshAcc("HALL-WALL-N-DOWNPIPES", "STEEL")
    for x in range(int(x0) + 30, int(x1), 60):
        dpS.cyl(x + 0.5, y0 - 1.6, GZ, 0.32, HH_ - 0.5, 8)
        dpN.cyl(x + 0.5, y1 + 1.6, GZ, 0.32, HH_ - 0.5, 8)
    dpS.build(); dpN.build()
    # roof-top hatches and a ridge walkway rail
    hb = MeshAcc("HALL-ROOF-HATCHES", "STEEL", cutaway=True)
    for x in range(int(x0) + 60, int(x1) - 40, 120):
        hb.box(x, ym - 12, ridge + 0.3, x + 6, ym - 8, ridge + 2.0)
        hb.rail([(x - 3, ym - 15), (x + 9, ym - 15), (x + 9, ym - 5), (x - 3, ym - 5), (x - 3, ym - 15)], ridge + 0.3, 3.0, 4.0)
    hb.build()
    # interior: cable-tray drops and lighting fixtures along the trusses
    li = MeshAcc("HALL-LIGHTS", "STEEL_DK")
    for x in range(int(x0) + 15, int(x1), 30):
        for y in (y0 + 40, (y0 + y1) / 2, y1 - 40):
            li.seg((x, y, HH_ - 6.0), (x, y, HH_ - 12.0), 0.05, 4)
            li.cyl(x, y, HH_ - 13.5, 1.3, 1.5, 12, r2=2.0)
    li.build()

# ---- gas turbine trains and steam turbine -------------------------------------------------
def detail_gt(i):
    g = gt_train_geometry(i)
    ax, ye0, yg0, yg1, yd0 = g["ax"], g["y_enc0"], g["y_gen0"], g["y_gen1"], g["y_diff0"]
    n = i + 1
    pre = "GT-%d-" % n
    zb = GZ + 6.0
    # enclosure cladding: vertical ribs on both sides, roof ribs, louvre panels, service door
    r = MeshAcc(pre + "ENCLOSURE-RIBS", "ENCL")
    for side in (-1, 1):
        xf = ax + side * 9
        y = ye0 + 1.5
        while y < ye0 + 47:
            xa, xb = (xf, xf + 0.3) if side > 0 else (xf - 0.3, xf)
            r.box(xa, y, zb + 0.3, xb, y + 0.3, GZ + 24)
            y += 3.0
    y = ye0 + 1.0
    while y < ye0 + 47:
        r.box(ax - 9, y, GZ + 24, ax + 9, y + 0.3, GZ + 24.3)
        y += 3.0
    r.build()
    lv = MeshAcc(pre + "ENCLOSURE-LOUVRES", "STEEL")
    lv.louvre_y(ye0 + 26, ye0 + 44, ax + 9, 1, GZ + 12, GZ + 21)
    lv.louvre_y(ye0 + 26, ye0 + 44, ax - 9, -1, GZ + 12, GZ + 21)
    lv.door_y(ye0 + 8, ax + 9, 1, zb + 0.3, 3.2, 6.6)
    lv.build()
    # walkway along the east side of the train with handrail, stair to grade and posts
    wz = GZ + 8.0
    wy0, wy1 = yg0 - 6.0, ye0 + 47.0
    wk = MeshAcc(pre + "WALKWAY", "STEEL")
    wk.box(ax + 17, wy0, wz - 0.25, ax + 9.3, wy1, wz)
    for y in range(int(wy0), int(wy1), 10):
        wk.box(ax + 17.2, y, GZ, ax + 16.8, y + 0.4, wz - 0.25)
        wk.box(ax + 17.2, y, wz - 0.9, ax + 9.3, y + 0.35, wz - 0.25)
    wk.rail([(ax + 17, wy0), (ax + 17, wy1), (ax + 9.3, wy1)], wz, 3.5, 5.0)
    wk.rail([(ax + 9.3, wy0), (ax + 17, wy0)], wz, 3.5, 5.0, toe=False)
    wk.stair(ax + 13.5, wy0 - 12.0, GZ, wz, run_dir=(0, 1), width=3.0)
    wk.rail([(ax + 17, wy0 - 12.0), (ax + 17, wy0)], GZ, 3.5, 5.0, toe=False)
    wk.build()
    # lube-oil skid, fuel-gas valve skid, fire-protection cylinders, seal-oil skid
    sk = MeshAcc(pre + "SKID-LUBE-OIL", "ENCL")
    sk.box(ax + 33, yg0 + 6, GZ, ax + 21, yg0 + 34, GZ + 0.6)
    sk.box(ax + 32.5, yg0 + 6.5, GZ + 0.6, ax + 21.5, yg0 + 22, GZ + 6.5)               # tank
    for k in range(3):
        sk.cyl(ax + 30 + k * 3.2, yg0 + 27, GZ + 0.6, 0.9, 3.2, 12)                        # pumps
        sk.box(ax + 31.2 + k * 3.2, yg0 + 30, GZ + 0.6, ax + 28.8 + k * 3.2, yg0 + 33, GZ + 3.2)   # motors
    sk.cyl_between((ax + 32, yg0 + 24, GZ + 5.0), (ax + 22, yg0 + 24, GZ + 5.0), 1.1, 14)  # cooler
    sk.build()
    fv = MeshAcc(pre + "SKID-FUEL-GAS", "STEEL")
    fv.box(ax + 33, ye0 + 6, GZ, ax + 22, ye0 + 26, GZ + 0.6)
    for k in range(4):
        fv.box(ax + 31.5 + k * 2.4, ye0 + 9, GZ + 0.6, ax + 30.3 + k * 2.4, ye0 + 23, GZ + 3.4)      # valve trains
        fv.cyl(ax + 30.9 + k * 2.4, ye0 + 16, GZ + 3.4, 0.55, 0.9, 10)                                # actuators
        fv.cyl(ax + 30.9 + k * 2.4, ye0 + 16, GZ + 4.3, 0.85, 0.12, 12)                               # handwheels
    fv.cyl_between((ax + 32.5, ye0 + 8, GZ + 4.2), (ax + 22.5, ye0 + 8, GZ + 4.2), 0.7, 10)
    fv.build()
    fp = MeshAcc(pre + "SKID-FIRE-PROTECTION", "STEEL_DK")
    fp.box(ax + 33, ye0 + 30, GZ, ax + 21, ye0 + 42, GZ + 0.5)
    for k in range(6):
        for row in range(2):
            fp.cyl(ax + 31.8 + k * 1.9, ye0 + 33 + row * 4, GZ + 0.5, 0.65, 4.2, 12)
            fp.cyl(ax + 31.8 + k * 1.9, ye0 + 33 + row * 4, GZ + 4.7, 0.3, 0.5, 8)
    fp.box(ax + 32.5, ye0 + 31, GZ + 3.6, ax + 21.5, ye0 + 31.3, GZ + 3.8).box(ax + 32.5, ye0 + 38, GZ + 3.6, ax + 21.5, ye0 + 38.3, GZ + 3.8)
    fp.build()
    so = MeshAcc(pre + "SKID-SEAL-OIL", "ENCL")
    so.box(ax - 11, yg0 + 18, GZ, ax - 19, yg0 + 38, GZ + 0.5)
    so.box(ax - 11.5, yg0 + 18.5, GZ + 0.5, ax - 18.5, yg0 + 30, GZ + 5.5)
    for k in range(2):
        so.cyl(ax - 14 + k * 3, yg0 + 34, GZ + 0.5, 0.8, 3.0, 10)
    so.build()
    # interconnecting piping from the skids to the enclosure and generator
    pp = CurveAcc(pre + "SKID-PIPING", "STEEL", 0.32)
    for k in range(3):
        pp.add([(ax + 21.5, yg0 + 12 + k * 3, GZ + 3.0), (ax + 19, yg0 + 12 + k * 3, GZ + 3.0), (ax + 19, yg0 + 12 + k * 3, GZ + 6.9), (ax + 9.2, yg0 + 12 + k * 3, GZ + 6.9)])
    for k in range(2):
        pp.add([(ax + 22.5, ye0 + 12 + k * 4, GZ + 4.2), (ax + 19.5, ye0 + 12 + k * 4, GZ + 4.2), (ax + 19.5, ye0 + 12 + k * 4, GZ + 6.9), (ax + 9.2, ye0 + 12 + k * 4, GZ + 6.9)])
    for k in range(2):
        pp.add([(ax - 11, yg0 + 24 + k * 3, GZ + 3.5), (ax - 8, yg0 + 24 + k * 3, GZ + 3.5), (ax - 7.5, yg0 + 24 + k * 3, GZ + 8.5)])
    pp.build()
    fl = MeshAcc(pre + "SKID-PIPE-FLANGES", "STEEL_DK")
    for k in range(3):
        for dx in (-20.5, -12.0):
            fl.cyl_between((ax + dx, yg0 + 12 + k * 3, GZ + 6.9), (ax + dx + 0.18, yg0 + 12 + k * 3, GZ + 6.9), 0.6, 12)
    fl.build()
    # generator: bearing bands, cooler fins, end bell, foot plates
    ge = MeshAcc(pre + "GENERATOR-DETAIL", "STEEL")
    for yy in (yg0 + 3, yg0 + 12, yg0 + 21, yg0 + 30, yg0 + 39):
        if yy < yg1 - 1:
            ge.cyl_between((ax, yy, GZ + 14), (ax, yy + 0.5, GZ + 14), 7.8, 24)
    for k in range(9):
        ge.box(ax - 6 + k * 1.5, yg0 + 7, GZ + 25, ax - 5.75 + k * 1.5, yg1 - 7, GZ + 27.2)
    ge.box(ax - 6.2, yg0 + 2, GZ + 6, ax + 6.2, yg0 + 4, GZ + 6.4)
    ge.box(ax - 9, yg0 + 1, GZ + 0.6, ax - 6, yg0 + 3, GZ + 6).box(ax + 6, yg0 + 1, GZ + 0.6, ax + 9, yg0 + 3, GZ + 6)
    ge.build()
    # exhaust expansion joints (bellows) on the diffuser
    ej = MeshAcc(pre + "EXPJOINT", "STEEL_DK")
    for yy in (yd0 - 1.2, yd0 + 6.0):
        ej.box(ax - 7.6, yy, GZ + 7.6, ax + 7.6, yy + 0.8, GZ + 8.3).box(ax - 7.6, yy, GZ + 21.8, ax + 7.6, yy + 0.8, GZ + 22.5)
        ej.box(ax - 7.6, yy, GZ + 8.3, ax - 6.8, yy + 0.8, GZ + 21.8).box(ax + 6.8, yy, GZ + 8.3, ax + 7.6, yy + 0.8, GZ + 21.8)
    ej.build()
    # cable drops: power tray branch to the control module and skids
    tr = MeshAcc(pre + "TRAY-BRANCH", "STEEL")
    tr.tray([(ax - 22.5, ye0 + 18), (ax - 26, ye0 + 18), (ax - 26, HY0 + 8)], GZ + 10.0, width=1.5, posts=False)
    tr.build()
    anchor(pre + "WALKWAY", ax + 13, (wy0 + wy1) / 2, wz + 3.8, "Access walkway and stair", 7)
    anchor(pre + "SKID-LUBE-OIL", ax + 27, yg0 + 20, GZ + 7.5, "Lube-oil skid", 7)
    anchor(pre + "SKID-FUEL-GAS", ax + 28, ye0 + 16, GZ + 6.0, "Fuel-gas valve skid", 7)


def detail_st():
    ax = ST_X
    y0, y1 = 660, 800
    deck = 30
    # tabletop guard rail, stair from grade, lube-oil console, stop valves and gland steam
    dk = MeshAcc("ST-DECK-DETAIL", "STEEL")
    dk.rail([(ax - 22.5, y0), (ax - 22.5, y1), (ax + 22.5, y1), (ax + 22.5, y0), (ax - 22.5, y0)], deck, 3.5, 5.0,
            skip=lambda x, y: (abs(x - (ax - 22.5)) < 0.1 and 735 < y < 740))
    dk.box(ax - 26.5, 733, deck - 0.25, ax - 22.5, 741, deck)
    dk.stair(ax - 27.0, 690, GZ, deck, run_dir=(0, 1), width=3.0)
    dk.rail([(ax - 27.2, 690), (ax - 27.2, 735)], GZ, 3.5, 5.0, toe=False)
    dk.build()
    lc = MeshAcc("ST-LUBE-CONSOLE", "ENCL")
    lc.box(ax + 24, 676, GZ, ax + 36, 700, GZ + 0.5)
    lc.box(ax + 24.5, 676.5, GZ + 0.5, ax + 35.5, 690, GZ + 7.5)
    for k in range(3):
        lc.cyl(ax + 27 + k * 3.2, 695, GZ + 0.5, 0.9, 3.4, 12)
    lc.cyl_between((ax + 25, 686, GZ + 6.5), (ax + 35, 686, GZ + 6.5), 1.2, 14)
    lc.build()
    vv = MeshAcc("ST-STOP-VALVES", "STEEL_DK")
    vv.box(ax - 2.5, 786, deck + 11, ax + 2.5, 792, deck + 15)
    vv.cyl(ax, 789, deck + 15, 0.8, 1.2, 10)
    vv.box(ax - 2.5, 768, deck + 11, ax + 2.5, 774, deck + 15)
    vv.cyl(ax, 771, deck + 15, 0.8, 1.2, 10)
    vv.build()
    gs = MeshAcc("ST-GLAND-STEAM", "ENCL")
    gs.cyl_between((ax + 8, 700, GZ + 4), (ax + 8, 720, GZ + 4), 2.2, 16)
    gs.box(ax + 6, 702, GZ, ax + 10, 704, GZ + 4).box(ax + 6, 716, GZ, ax + 10, 718, GZ + 4)
    gs.build()
    # rings on the LP exhaust duct, expansion joint and supports
    ex = MeshAcc("ST-EXHAUST-FLANGES", "STEEL_DK")
    for xx in (ax + 22, ax + 36, ax + 52):
        ex.box(xx, 723.2, 21.2, xx + 0.5, 736.8, 22.8)
    ex.build()
    anchor("ST-DECK", ax, y0 + 20, deck + 3.5, "ST tabletop with guard rail and stair", 7)
    anchor("ST-LUBE-CONSOLE", ax + 30, 685, GZ + 8.5, "ST lube-oil console", 7)

def switchback(m, tx, ty, z0, z1, lane_w=2.2, run=9.0, riser=0.6):
    """four-flight switchback stair inside a tower footprint centred on (tx, ty)."""
    lanes = 4
    rise = (z1 - z0) / lanes
    n = max(1, int(round(rise / riser)))
    tread = run / n
    x_start = tx - lane_w * lanes / 2.0
    for k in range(lanes):
        xl = x_start + k * lane_w
        up = (k % 2 == 0)
        zb = z0 + k * rise
        for j in range(n):
            yy = (ty - run / 2 + j * tread) if up else (ty + run / 2 - (j + 1) * tread)
            m.box(xl + 0.1, yy, zb + j * (rise / n), xl + lane_w - 0.1, yy + tread, zb + j * (rise / n) + 0.14)
        # landing at the end of each flight
        ly = ty + run / 2 if up else ty - run / 2 - 1.0
        m.box(xl - 0.05, ly, zb + rise - 0.2, xl + lane_w * 2 + 0.05 if k < lanes - 1 else xl + lane_w, ly + 1.0, zb + rise)


# ---- HRSG, stack, inlet houses, GSUs -----------------------------------------------------------
def detail_hrsg(i):
    ax = GT_X[i]
    n = i + 1
    pre = "HRSG-%d-" % n
    hw = HRSG_W / 2.0
    y0, y1 = HRSG_Y0, HRSG_Y1
    yc0, yc1 = y0 + 30, y1 - 24
    cas_h = 150.0
    top = HRSG_H
    r = STACK_D / 2.0
    # insulation-panel stiffeners: horizontal bands + vertical ribs on both sides and the rear face
    st = MeshAcc(pre + "CASING-STIFFENERS", "STEEL")
    for side in (-1, 1):
        xf = ax + side * hw
        xa, xb = (xf, xf + 0.6) if side > 0 else (xf - 0.6, xf)
        z = 20.0
        while z < cas_h:
            st.box(xa, yc0, z, xb, yc1, z + 0.7)
            z += 10.0
        y = yc0 + 5.5
        while y < yc1:
            st.box(xa, y, GZ + 8, xb, y + 0.7, cas_h)
            y += 11.0
    z = 20.0
    while z < cas_h:
        st.box(ax - hw, yc1, z, ax + hw, yc1 + 0.6, z + 0.7)
        z += 10.0
    x = ax - hw + 6
    while x < ax + hw:
        st.box(x, yc1, GZ + 8, x + 0.7, yc1 + 0.6, cas_h)
        x += 11.5
    st.build()
    # expansion joints at the inlet and outlet of the casing
    ej = MeshAcc(pre + "EXPJOINT", "STEEL_DK")
    for yy in (yc0 - 1.0, yc1 - 0.2):
        ej.box(ax - hw - 0.8, yy, GZ + 7.5, ax + hw + 0.8, yy + 1.2, GZ + 8.6).box(ax - hw - 0.8, yy, cas_h - 0.4, ax + hw + 0.8, yy + 1.2, cas_h + 0.8)
        ej.box(ax - hw - 0.8, yy, GZ + 8.6, ax - hw + 0.4, yy + 1.2, cas_h).box(ax + hw - 0.4, yy, GZ + 8.6, ax + hw + 0.8, yy + 1.2, cas_h)
    ej.build()
    # access platforms on both sides at six levels, with rails, brackets and caged ladders
    levels = [25.0, 50.0, 75.0, 100.0, 125.0, 150.0]
    pf = MeshAcc(pre + "PLATFORMS", "STEEL")
    tower_y = (y0 + 60 - 7, y0 + 60 + 7)
    for side in (1, -1):
        xin = ax + side * (hw + 2.5)
        xout = ax + side * (hw + 7.5)
        lo, hi = min(xin, xout), max(xin, xout)
        for z in levels:
            pf.box(lo, yc0 + 6, z - 0.25, hi, yc1 - 6, z)
            pf.rail([(xout, yc0 + 6), (xout, yc1 - 6)], z, 3.5, 5.0,
                    skip=(lambda px, py: side > 0 and tower_y[0] < py < tower_y[1]))
            pf.rail([(xout, yc0 + 6), (xin, yc0 + 6)], z, 3.5, 5.0, toe=False)
            pf.rail([(xout, yc1 - 6), (xin, yc1 - 6)], z, 3.5, 5.0, toe=False)
            yb = yc0 + 6.0
            while yb <= yc1 - 6:
                pf.seg((ax + side * (hw + 1.9), yb, z - 4.0), (xout, yb, z - 0.3), 0.14, 4)
                yb += 11.0
        prev = GZ
        for k, z in enumerate(levels):
            yl = yc0 + 24 if (k % 2 == 0) else yc1 - 24
            pf.ladder(xout - side * 0.4, yl, prev, z, face=(-side, 0), cage=True)
            prev = z
    pf.build()
    # access tower: landings at each level plus switchback stairs
    tx, ty = ax + hw + 10, y0 + 60
    tl = MeshAcc(pre + "STAIR-LANDINGS", "STEEL")
    for z in levels:
        tl.box(tx - 5.6, ty - 5.6, z - 0.25, tx + 5.6, ty + 5.6, z)
        tl.rail([(tx + 5.6, ty - 5.6), (tx + 5.6, ty + 5.6), (tx - 5.6, ty + 5.6)], z, 3.5, 5.0, toe=False)
    prev = GZ
    for z in levels:
        switchback(tl, tx, ty, prev, z)
        prev = z
    tl.build()
    # roof: open steel frame + perimeter grating and rail, so the drums are visible from above
    rf = MeshAcc(pre + "ROOF-FRAME", "STEEL")
    xL, xR = ax - hw - 2.5, ax + hw + 2.5
    rf.box(xL, yc0, top - 1.5, xL + 0.8, yc1, top).box(xR - 0.8, yc0, top - 1.5, xR, yc1, top)
    rf.box(xL, yc0, top - 1.5, xR, yc0 + 0.8, top).box(xL, yc1 - 0.8, top - 1.5, xR, yc1, top)
    y = yc0 + 10
    while y < yc1:
        rf.box(xL, y, top - 1.2, xR, y + 0.6, top - 0.2)
        y += 10.0
    for xx in (ax - 22, ax + 22):
        rf.box(xx - 0.4, yc0, top - 1.2, xx + 0.4, yc1, top - 0.2)
    rf.box(xL, yc0, top - 0.25, xL + 3.5, yc1, top).box(xR - 3.5, yc0, top - 0.25, xR, yc1, top)       # grating walkways
    rf.box(xL, yc0, top - 0.25, xR, yc0 + 3.5, top).box(xL, yc1 - 3.5, top - 0.25, xR, yc1, top)
    rf.rail([(xL, yc0), (xL, yc1), (xR, yc1), (xR, yc0), (xL, yc0)], top, 3.5, 5.0)
    rf.build()
    # drum nozzles, safety valves and silencers
    sv = MeshAcc(pre + "DRUM-VALVES", "STEEL")
    sil = MeshAcc(pre + "DRUM-SILENCERS", "INSUL")
    for dy, rr in ((y0 + 50, 4.5), (y0 + 85, 3.5), (y0 + 115, 3.0)):
        zt = cas_h + 9 + rr
        for dx in (-14, -6, 6, 14):
            sv.cyl(ax + dx, dy, zt - 0.3, 0.5, 4.3, 8)
            sv.cyl(ax + dx, dy, zt + 4.0, 0.9, 0.35, 10)
            sv.cyl(ax + dx, dy, zt + 4.35, 0.7, 4.0, 10)
        sil.cyl(ax + 10, dy, zt, 0.6, 6.0, 8)
        sil.cyl(ax + 10, dy, zt + 6.0, 1.5, 5.0, 12)
        sil.cyl(ax + 10, dy, zt + 11.0, 1.0, 1.0, 12, r2=0.3)
        for xx in (-26.5, 26.5):
            sv.box(ax + xx - 0.6, dy - 1.2, zt - 1.5, ax + xx + 0.6, dy + 1.2, zt + 1.5)
    sv.build(); sil.build()
    # rear vertical piping rack (feed / blowdown / vents) with supports and flanges
    pr = CurveAcc(pre + "PIPING-RACK", "INSUL", 0.7)
    fl = MeshAcc(pre + "PIPING-FLANGES", "STEEL_DK")
    for k in range(6):
        px = ax - 25 + k * 10
        pr.add([(px, yc1 + 2.5, GZ + 3), (px, yc1 + 2.5, cas_h - 8)])
        zf = 20.0
        while zf < cas_h - 8:
            fl.cyl(px, yc1 + 2.5, zf, 1.05, 0.3, 12)
            zf += 20.0
    pr.add([(ax - 25, yc1 + 2.5, GZ + 3), (ax - 25, yc1 + 12, GZ + 3), (ax + 25, yc1 + 12, GZ + 3), (ax + 25, yc1 + 2.5, GZ + 3)])
    pr.build(); fl.build()
    sup = MeshAcc(pre + "PIPING-SUPPORTS", "STEEL_DK")
    for zf in (30.0, 70.0, 110.0):
        sup.box(ax - 27, yc1 + 1.8, zf, ax + 27, yc1 + 3.2, zf + 0.5)
    sup.build()
    # stack: stiffener rings, base flange, cap, lightning rod, aviation lights, caged ladder
    sd = MeshAcc(pre + "STACK-DETAIL", "STEEL")
    zz = 20.0
    while zz < STACK_H - 12:
        sd.stiff_ring(ax, STACK_Y, zz, r, 0.5, 0.35, 40)
        zz += 25.0
    sd.cyl(ax, STACK_Y, GZ, r + 1.2, 1.1, 40)
    sd.cyl(ax, STACK_Y, GZ + STACK_H - 0.6, r + 0.7, 1.2, 40)
    sd.cyl(ax, STACK_Y, GZ + STACK_H, 0.12, 12, 6)
    for a_ in range(4):
        aa = a_ * math.pi / 2
        sd.cyl(ax + (r + 0.4) * math.cos(aa), STACK_Y + (r + 0.4) * math.sin(aa), GZ + STACK_H - 12, 0.4, 0.7, 8)
        sd.cyl(ax + (r + 0.4) * math.cos(aa), STACK_Y + (r + 0.4) * math.sin(aa), GZ + STACK_H / 2, 0.4, 0.7, 8)
    sd.ladder(ax, STACK_Y - r - 0.3, GZ, STACK_H - 8, face=(0, -1), cage=True)
    for pz in (60.0, 140.0, 220.0):
        sd.box(ax - 1.2, STACK_Y - r - 4.5, pz - 0.25, ax + 1.2, STACK_Y - r - 0.2, pz)      # ladder landing
    sd.build()


def detail_inlet(i):
    ax = GT_X[i]
    n = i + 1
    pre = "INLET-%d-" % n
    L, W, H = P["inlet_ft"]
    base = P["inlet_base_ft"]
    cx = ax + P["inlet_offset_x_ft"]
    cy = 590.0
    x0, x1 = cx - L / 2, cx + L / 2
    y0, y1 = cy - W / 2, cy + W / 2
    # louvred weather hoods, roof rail and ladder, support-deck rail
    lv = MeshAcc(pre + "HOOD-LOUVRES", "STEEL")
    for k in range(6):
        hx = x0 + 4 + k * 9
        lv.louvre_x(hx + 0.6, hx + 6.4, y0 - 3, -1, base + 3, base + H - 4, 0.6, 0.4)
        lv.louvre_x(hx + 0.6, hx + 6.4, y1 + 3, 1, base + 3, base + H - 4, 0.6, 0.4)
    lv.build()
    rl = MeshAcc(pre + "ROOF-RAIL", "STEEL")
    rl.rail([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], base + H, 3.5, 5.0)
    rl.rail([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], base - 2 + 0.0, 3.5, 5.0, toe=True)
    rl.ladder(x1 + 0.3, cy, GZ, base + H, face=(1, 0), cage=True)
    rl.build()
    ri = MeshAcc(pre + "ROOF-DETAIL", "ENCL")
    x = x0 + 2
    while x < x1:
        ri.box(x, y0, base + H, x + 0.4, y1, base + H + 0.35)
        x += 4.0
    ri.box(x0 + 8, y0 + 8, base + H + 0.3, x0 + 14, y0 + 14, base + H + 2.5)      # roof hatch
    ri.build()


def detail_gsu(i):
    ax = GSU_X[i]
    n = i + 1
    pre = "GSU-%d-" % n
    y0 = GSU_Y0
    y1 = y0 + GSU_W
    hx = GSU_L / 2
    sk = MeshAcc(pre + "BUSHING-SHEDS", "PORCELAIN")
    for dx in (-8, 0, 8):                                   # 230 kV bushings: skirts every foot
        for k in range(9):
            sk.cyl(ax + dx, y0 + 8, GZ + GSU_H - 6 + 1.2 + k * 1.0, 1.75, 0.18, 12)
    for dx in (-5, 0, 5):
        for k in range(5):
            sk.cyl(ax + dx, y1 - 4, GZ + GSU_H - 6 + 0.8 + k * 1.05, 1.1, 0.15, 10)
    sk.build()
    tx = MeshAcc(pre + "TANK-DETAIL", "STEEL")
    for z in (GZ + 6, GZ + 12, GZ + 18):                    # tank stiffener bands
        tx.box(ax - hx + 8 - 0.3, y0 + 2 - 0.3, z, ax + hx - 8 + 0.3, y1 - 2 + 0.3, z + 0.5)
    tx.ladder(ax - hx + 7.6, y0 + 6, GZ + 1, GZ + GSU_H - 6, face=(-1, 0), cage=False)
    tx.cyl(ax + hx - 9.5, y0 + 6, GZ + GSU_H - 6.0, 0.9, 1.4, 10)                  # pressure relief device
    for k in range(3):
        tx.box(ax - 8 + k * 8 - 0.6, y0 + 6, GZ + GSU_H - 6.4, ax - 8 + k * 8 + 0.6, y0 + 10, GZ + GSU_H - 6.0)
    tx.box(ax + 4, y0 + 1.4, GZ + 5, ax + 8, y0 + 2, GZ + 9)                        # marshalling box
    tx.build()
    # radiator fans: shrouds
    fs = MeshAcc(pre + "COOLER-FANS", "STEEL_DK")
    for side in (-1, 1):
        for yy in (y0 + 8, y1 - 8):
            cx_ = ax + side * (hx - 4)
            fs.cyl(cx_, yy, GZ + GSU_H - 9, 2.6, 0.35, 16)
            for k in range(4):
                fs.boxc(cx_, yy, GZ + GSU_H - 8.6, 4.6, 0.5, 0.12, rot=math.radians(k * 45))
    fs.build()

def stair_rails(m, x, y, z0, z1, run_dir=(1, 0), width=3.0, riser=0.6, tread=0.9):
    """sloped handrails (with posts) on both sides of a straight stair built by MeshAcc.stair()."""
    n = max(1, int((z1 - z0) / riser))
    dx, dy = run_dir
    px, py = (0.0, 1.0) if dx else (1.0, 0.0)
    for s in (0.0, width):
        a = (x + px * s, y + py * s, z0 + 3.2)
        b = (x + px * s + dx * n * tread, y + py * s + dy * n * tread, z0 + n * riser + 3.2)
        m.seg(a, b, 0.07, 4)
        a2 = (a[0], a[1], a[2] - 1.5); b2 = (b[0], b[1], b[2] - 1.5)
        m.seg(a2, b2, 0.05, 4)
        for k in range(0, n + 1, 3):
            t = k / float(n)
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)
            m.seg((p[0], p[1], p[2] - 3.2), p, 0.06, 4)


def clad_building(pre, x0, y0, x1, y1, zb, ztop, s_cut=False, roof_top=None, doors=None, louvres=None, avoid=None,
                  roof_ribs=True, parapet=True, plinth=True, downpipes=True, rib_pitch=5.0):
    """cladding ribs, doors, louvres, roof ribs, eaves trim and downpipes for a rectangular building.
    Sides: S = -y face, N = +y face, W = -x face, E = +x face.  With s_cut the south wall and roof are separate,
    removable parts (named <pre>WALL-S-* and <pre>ROOF-*)."""
    doors = doors or {}
    louvres = louvres or {}
    avoid = avoid or {}
    rt = roof_top if roof_top is not None else ztop
    # ribs
    def av(side, extra=()):
        out = list(avoid.get(side, [])) + list(extra)
        for d in doors.get(side, []):
            w = d[2] if d[1] == "r" else 3.4
            out.append((d[0] - w / 2 - 0.6, d[0] + w / 2 + 0.6))
        for l in louvres.get(side, []):
            out.append((l[0], l[1]))
        return out
    top = ztop - (0.8 if parapet else 0.0)
    MeshAcc(pre + "WALL-S-RIBS" if s_cut else pre + "WALLS-RIBS-S", "ENCL", cutaway=s_cut).ribs_x(y0, -1, x0, x1, zb + (0.7 if plinth else 0), top, rib_pitch, 0.45, 0.35, av("S")).build()
    walls = MeshAcc(pre + "WALLS-RIBS", "ENCL")
    walls.ribs_x(y1, 1, x0, x1, zb + (0.7 if plinth else 0), top, rib_pitch, 0.45, 0.35, av("N"))
    walls.ribs_y(x0, -1, y0, y1, zb + (0.7 if plinth else 0), top, rib_pitch, 0.45, 0.35, av("W"))
    walls.ribs_y(x1, 1, y0, y1, zb + (0.7 if plinth else 0), top, rib_pitch, 0.45, 0.35, av("E"))
    walls.build()
    if plinth:
        MeshAcc(pre + "WALL-S-PLINTH" if s_cut else pre + "PLINTH-S", "CONC", cutaway=s_cut).box(x0 - 0.3, y0 - 0.3, zb, x1 + 0.3, y0, zb + 0.7).build()
        pl = MeshAcc(pre + "PLINTH", "CONC")
        pl.box(x0 - 0.3, y1, zb, x1 + 0.3, y1 + 0.3, zb + 0.7).box(x0 - 0.3, y0 - 0.3, zb, x0, y1 + 0.3, zb + 0.7).box(x1, y0 - 0.3, zb, x1 + 0.3, y1 + 0.3, zb + 0.7)
        pl.build()
    # doors and louvres per side
    for side in ("S", "N", "W", "E"):
        ds = doors.get(side, [])
        ls = louvres.get(side, [])
        if not ds and not ls:
            continue
        nm = (pre + "WALL-S-DOORS") if (side == "S" and s_cut) else (pre + "DOORS-" + side)
        acc = MeshAcc(nm, "STEEL", cutaway=(side == "S" and s_cut))
        for d in ds:
            pos, kind = d[0], d[1]
            if side == "S":
                (acc.door_x(pos, y0, -1, zb) if kind == "p" else acc.rollup_x(pos, y0, -1, zb, d[2], d[3]))
            elif side == "N":
                (acc.door_x(pos, y1, 1, zb) if kind == "p" else acc.rollup_x(pos, y1, 1, zb, d[2], d[3]))
            elif side == "W":
                (acc.door_y(pos, x0, -1, zb) if kind == "p" else acc.rollup_y(pos, x0, -1, zb, d[2], d[3]))
            else:
                (acc.door_y(pos, x1, 1, zb) if kind == "p" else acc.rollup_y(pos, x1, 1, zb, d[2], d[3]))
        for l in ls:
            a, b, zl, zh = l
            if side == "S":
                acc.louvre_x(a, b, y0, -1, zl, zh)
            elif side == "N":
                acc.louvre_x(a, b, y1, 1, zl, zh)
            elif side == "W":
                acc.louvre_y(a, b, x0, -1, zl, zh)
            else:
                acc.louvre_y(a, b, x1, 1, zl, zh)
        acc.build()
        # landing apron in front of each door
        for d in ds:
            pos, kind = d[0], d[1]
            w = 4.5 if kind == "p" else (d[2] + 3)
            dpt = 3.5 if kind == "p" else 6.0
            if side == "S":
                apron(pre + "APRON-S-%d" % int(pos), pos - w / 2, y0 - dpt - 0.3, pos + w / 2, y0 - 0.3)
            elif side == "N":
                apron(pre + "APRON-N-%d" % int(pos), pos - w / 2, y1 + 0.3, pos + w / 2, y1 + dpt + 0.3)
            elif side == "W":
                apron(pre + "APRON-W-%d" % int(pos), x0 - dpt - 0.3, pos - w / 2, x0 - 0.3, pos + w / 2)
            else:
                apron(pre + "APRON-E-%d" % int(pos), x1 + 0.3, pos - w / 2, x1 + dpt + 0.3, pos + w / 2)
    # roof ribs, eaves trim / parapet, downpipes
    nm_r = pre + "ROOF-RIBS" if s_cut else pre + "ROOF-DETAIL"
    rr = MeshAcc(nm_r, "ENCL", cutaway=s_cut)
    if roof_ribs:
        x = x0 + 2.0
        while x < x1 - 1:
            rr.box(x, y0 + 0.4, rt, x + 0.4, y1 - 0.4, rt + 0.3)
            x += 4.0
    if parapet:
        rr.box(x0 - 0.3, y0 - 0.3, rt, x1 + 0.3, y0 + 0.3, rt + 0.9).box(x0 - 0.3, y1 - 0.3, rt, x1 + 0.3, y1 + 0.3, rt + 0.9)
        rr.box(x0 - 0.3, y0 + 0.3, rt, x0 + 0.3, y1 - 0.3, rt + 0.9).box(x1 - 0.3, y0 + 0.3, rt, x1 + 0.3, y1 - 0.3, rt + 0.9)
    rr.build()
    if downpipes:
        dp = MeshAcc(pre + "DOWNPIPES", "STEEL")
        for (px, py) in ((x0 - 0.5, y1 + 0.5), (x1 + 0.5, y1 + 0.5), (x1 + 0.5, y0 - 0.5), (x0 - 0.5, y0 - 0.5)):
            dp.cyl(px, py, zb, 0.28, ztop - zb - 0.5, 8)
        dp.build()


def tank_detail(pre, cx, cy, z0, r, h, roof_h=3.0, spiral=True):
    """ring stiffeners, wind girder, roof rail and vent, manway, nozzles, spiral stair and ring-wall foundation."""
    t = MeshAcc(pre + "TANK-DETAIL", "STEEL")
    zz = z0 + 8.0
    while zz < z0 + h - 3:
        t.stiff_ring(cx, cy, zz, r, 0.35, 0.22, 36)
        zz += 9.0
    t.cyl(cx, cy, z0 + h - 1.2, r + 1.2, 0.35, 36)                           # wind girder
    for a in range(0, 360, 20):
        aa = math.radians(a)
        t.seg((cx + (r + 1.2) * math.cos(aa), cy + (r + 1.2) * math.sin(aa), z0 + h - 1.2), (cx + r * math.cos(aa), cy + r * math.sin(aa), z0 + h - 3.0), 0.08, 4)
    # roof rail, vent, manway, nozzles
    pts = [(cx + (r - 0.6) * math.cos(math.radians(a)), cy + (r - 0.6) * math.sin(math.radians(a))) for a in range(0, 361, 15)]
    t.rail(pts, z0 + h, 3.5, 6.0, toe=False)
    t.cyl(cx, cy, z0 + h + roof_h - 0.3, 0.6, 2.2, 10)
    t.cyl(cx, cy, z0 + h + roof_h + 1.9, 1.1, 0.3, 12)
    t.cyl(cx + r * 0.45, cy - r * 0.15, z0 + h + roof_h * 0.55, 1.4, 1.5, 12)          # roof manway
    ang = math.radians(210)
    t.cyl_between((cx + r * math.cos(ang), cy + r * math.sin(ang), z0 + 3.0), (cx + (r + 2.2) * math.cos(ang), cy + (r + 2.2) * math.sin(ang), z0 + 3.0), 1.3, 12)   # shell manway
    for k, a in enumerate((20, 55, 300)):
        aa = math.radians(a)
        t.cyl_between((cx + r * math.cos(aa), cy + r * math.sin(aa), z0 + 2.0 + k * 0.4), (cx + (r + 3.0) * math.cos(aa), cy + (r + 3.0) * math.sin(aa), z0 + 2.0 + k * 0.4), 0.55, 10)
        t.cyl_between((cx + (r + 2.8) * math.cos(aa), cy + (r + 2.8) * math.sin(aa), z0 + 2.0 + k * 0.4), (cx + (r + 3.05) * math.cos(aa), cy + (r + 3.05) * math.sin(aa), z0 + 2.0 + k * 0.4), 0.85, 12)
    t.cyl(cx, cy, z0 - 0.2, r + 1.4, 0.6, 36)                                        # ring-wall foundation lip
    t.build()
    if spiral:
        sp = MeshAcc(pre + "TANK-STAIR", "STEEL")
        rs = r + 0.4
        n = max(12, int((h - 1.0) / 0.62))
        turn = 1.15
        for k in range(n):
            a0 = math.radians(300) + 2 * math.pi * turn * k / n
            zc = z0 + 0.5 + k * ((h - 0.5) / n)
            sp.boxc(cx + (rs + 1.5) * math.cos(a0), cy + (rs + 1.5) * math.sin(a0), zc, 3.0, 2 * math.pi * (rs + 1.5) * turn / n + 0.05, 0.16, rot=a0)
        prevp = None
        for k in range(n + 1):
            a0 = math.radians(300) + 2 * math.pi * turn * k / n
            zc = z0 + 0.5 + k * ((h - 0.5) / n) + 3.4
            p = (cx + (rs + 3.0) * math.cos(a0), cy + (rs + 3.0) * math.sin(a0), zc)
            if prevp:
                sp.seg(prevp, p, 0.07, 4)
                sp.seg((prevp[0], prevp[1], prevp[2] - 1.6), (p[0], p[1], p[2] - 1.6), 0.05, 4)
            if k % 3 == 0:
                sp.seg((p[0], p[1], p[2] - 3.4), p, 0.06, 4)
            prevp = p
        sp.build()


def column_detail(pre, cx, cy, z0, r, h, platforms=None):
    """process column: stiffener rings, platforms with rails, caged ladder, riser pipes, top vent."""
    c = MeshAcc(pre + "COLUMN-DETAIL", "STEEL")
    zz = z0 + 6.0
    while zz < z0 + h - 4:
        c.stiff_ring(cx, cy, zz, r, 0.4, 0.3, 32)
        zz += 14.0
    levels = platforms or [z0 + h * f for f in (0.25, 0.5, 0.75, 0.97)]
    prev = z0
    for k, zl in enumerate(levels):
        pts = [(cx + (r + 4.5) * math.cos(math.radians(a)), cy + (r + 4.5) * math.sin(math.radians(a))) for a in range(-70, 71, 14)]
        for a in range(-70, 70, 14):
            a0, a1 = math.radians(a), math.radians(a + 14)
            c.boxc(cx + (r + 2.2) * math.cos((a0 + a1) / 2), cy + (r + 2.2) * math.sin((a0 + a1) / 2), zl - 0.25, 4.6, 2 * (r + 2.2) * math.sin(math.radians(7)) + 0.2, 0.25, rot=(a0 + a1) / 2)
        c.rail(pts, zl, 3.5, 5.0)
        lx, ly = cx + (r + 0.3) * math.cos(math.radians(-15)), cy + (r + 0.3) * math.sin(math.radians(-15))
        c.ladder(lx, ly, prev, zl, face=(math.cos(math.radians(-15)), math.sin(math.radians(-15))), cage=True)
        prev = zl
    for k, a in enumerate((100, 128)):
        aa = math.radians(a)
        c.seg((cx + (r + 0.9) * math.cos(aa), cy + (r + 0.9) * math.sin(aa), z0 + 4), (cx + (r + 0.9) * math.cos(aa), cy + (r + 0.9) * math.sin(aa), z0 + h - 6), 0.55, 8)
        zc = z0 + 10
        while zc < z0 + h - 6:
            c.seg((cx + (r + 0.3) * math.cos(aa), cy + (r + 0.3) * math.sin(aa), zc), (cx + (r + 0.9) * math.cos(aa), cy + (r + 0.9) * math.sin(aa), zc), 0.12, 4)
            zc += 12
    c.cyl(cx, cy, z0 + h + 5, 0.9, 9, 10)
    c.build()


def detail_buildings():
    # ---- e-house ---------------------------------------------------------------------------------------
    x0, y0 = P["ehouse_origin_ft"]
    L, W, H = P["ehouse_ft"]
    zf = GZ + P["ehouse_floor_ft"]
    x1, y1 = x0 + L, y0 + W
    clad_building("ELEC-EHOUSE-", x0, y0, x1, y1, zf, zf + H, s_cut=True, roof_top=zf + H + 0.6,
                  doors={"S": [(x0 + 6, "p")], "E": [((y0 + y1) / 2, "p")]}, avoid={"S": [(x0 + 3, x0 + 9)]},
                  louvres={"N": [(x0 + 100, x0 + 112, zf + 6, zf + 12)]}, plinth=False)
    st = MeshAcc("ELEC-EHOUSE-STAIR-RAILS", "STEEL")
    stair_rails(st, x0 - 14, y0 + 2, GZ, zf, (1, 0), 4.0)
    st.build()
    rh = MeshAcc("ELEC-EHOUSE-ROOF-HVAC-DETAIL", "STEEL_DK", cutaway=True)
    for x in (x0 + 20, x0 + 70):
        rh.cyl(x + 4, y1 - 6, zf + H + 4.6, 2.6, 0.25, 20)
        for k in range(6):
            rh.boxc(x + 4, y1 - 6, zf + H + 4.85, 4.8, 0.35, 0.1, rot=math.radians(k * 30))
        rh.louvre_x(x + 0.6, x + 7.4, y1 - 10, -1, zf + H + 1.3, zf + H + 3.8, 0.5, 0.25)
        rh.seg((x + 8, y1 - 6, zf + H + 2), (x + 20, y1 - 6, zf + H + 2), 0.12, 6)
    rh.build()
    # ---- MCC / VFD / UPS building ----------------------------------------------------------------------
    x0, y0 = P["mcc_origin_ft"]
    L, W, H = P["mcc_ft"]
    z0 = GZ + 0.5
    x1, y1 = x0 + L, y0 + W
    clad_building("ELEC-MCC-", x0, y0, x1, y1, z0, z0 + H, s_cut=True, roof_top=z0 + H + 0.6,
                  doors={"S": [(x0 + 7, "p"), (x0 + 63, "p")], "E": [((y0 + y1) / 2, "p")], "N": [(x0 + 20, "p")]},
                  avoid={"S": [(x0 + 3, x0 + 11), (x0 + 59, x0 + 67)]}, louvres={"N": [(x0 + 45, x0 + 57, z0 + 5, z0 + 11)]})
    rh = MeshAcc("ELEC-MCC-ROOF-HVAC-DETAIL", "STEEL_DK", cutaway=True)
    for x in (x0 + 10, x0 + 40):
        rh.cyl(x + 4, y1 - 8, z0 + H + 4.6, 2.6, 0.25, 20)
        for k in range(6):
            rh.boxc(x + 4, y1 - 8, z0 + H + 4.85, 4.8, 0.35, 0.1, rot=math.radians(k * 30))
        rh.louvre_x(x + 0.6, x + 7.4, y1 - 12, -1, z0 + H + 1.3, z0 + H + 3.8, 0.5, 0.25)
    rh.build()
    # ---- admin building: mullions, sun fins, parapet, entrance steps and ramp ---------------------------
    x0, y0 = P["admin_origin_ft"]
    L, W, H = P["admin_ft"]
    x1, y1 = x0 + L, y0 + W
    mu = MeshAcc("ADMIN-MULLIONS", "STEEL")
    for zl in (GZ + 4, GZ + 16):
        for sy, sg in ((y0, -1), (y1, 1)):
            xx = x0 + 4
            while xx <= x1 - 4 + 0.01:
                ya, yb = (sy - 0.6, sy + 0.1) if sg < 0 else (sy - 0.1, sy + 0.6)
                mu.box(xx - 0.12, ya, zl - 0.2, xx + 0.12, yb, zl + 6.2)
                xx += 4.0
            for zz in (zl - 0.2, zl + 3.0, zl + 6.0):
                ya, yb = (sy - 0.6, sy + 0.1) if sg < 0 else (sy - 0.1, sy + 0.6)
                mu.box(x0 + 4, ya, zz, x1 - 4, yb, zz + 0.2)
    mu.build()
    fn = MeshAcc("ADMIN-SUN-FINS", "ENCL")
    for zl in (GZ + 4, GZ + 16):
        xx = x0 + 6
        while xx < x1 - 6:
            fn.box(xx, y0 - 1.8, zl, xx + 0.25, y0 - 0.1, zl + 6.0)
            xx += 8.0
        fn.box(x0 + 4, y0 - 1.8, zl + 6.0, x1 - 4, y0 - 0.1, zl + 6.25)
    fn.build()
    pr = MeshAcc("ADMIN-PARAPET", "ENCL")
    pr.box(x0 - 0.4, y0 - 0.4, GZ + H, x1 + 0.4, y0 + 0.4, GZ + H + 1.2).box(x0 - 0.4, y1 - 0.4, GZ + H, x1 + 0.4, y1 + 0.4, GZ + H + 1.2)
    pr.box(x0 - 0.4, y0 + 0.4, GZ + H, x0 + 0.4, y1 - 0.4, GZ + H + 1.2).box(x1 - 0.4, y0 + 0.4, GZ + H, x1 + 0.4, y1 - 0.4, GZ + H + 1.2)
    for k in range(3):
        pr.box(x0 + 8 + k * 14, y1 - 14, GZ + H, x0 + 16 + k * 14, y1 - 6, GZ + H + 3.5)
        pr.cyl(x0 + 12 + k * 14, y1 - 10, GZ + H + 3.5, 2.2, 0.2, 18)
    pr.build()
    en = MeshAcc("ADMIN-ENTRANCE", "STEEL")
    en.door_x(x0 + 50, y0, -1, GZ, 6.0, 8.0)
    for k in range(4):
        en.box(x0 + 46, y0 - 1.5 - k * 0.6, GZ, x0 + 54, y0 - 0.9 - k * 0.6 + 0.6, GZ + 0.5 - k * 0.12)
    en.rail([(x0 + 44, y0 - 4), (x0 + 44, y0 - 0.5)], GZ, 3.0, 4.0, toe=False)
    en.rail([(x0 + 56, y0 - 4), (x0 + 56, y0 - 0.5)], GZ, 3.0, 4.0, toe=False)
    en.build()
    ba = MeshAcc("ADMIN-BOLLARDS", "STEEL_DK")
    for k in range(7):
        ba.cyl(x0 + 30 + k * 6, y0 - 16, GZ, 0.4, 3.0, 8)
    ba.build()
    # ---- water treatment building + tanks -------------------------------------------------------------------
    wx, wy = P["water_origin_ft"]
    bL, bW, bH = P["water_treatment_ft"]
    pL, pW, pD = P["pond_ft"]
    by = wy + pW + 40
    clad_building("WATER-BLDG-", wx, by, wx + bL, by + bW, GZ, GZ + bH,
                  doors={"S": [(wx + 12, "p"), (wx + 50, "r", 12.0, 14.0)], "E": [(by + 25, "p")]}, avoid={"S": [(wx + 44, wx + 56)]},
                  louvres={"N": [(wx + 20, wx + 32, GZ + 10, GZ + 16), (wx + 46, wx + 58, GZ + 10, GZ + 16)]})
    n, td, th = P["water_tank_n_d_h_ft"]
    for k in range(n):
        tank_detail("WATER-T%d-" % (k + 1), wx + bL + 40 + k * 60, by + bW / 2, GZ, td / 2, th)
    # ---- gas metering house + process tanks --------------------------------------------------------------------
    gx, gy = P["gasmet_origin_ft"]
    hL, hW, hH = P["gas_meter_ft"]
    clad_building("GASMET-HOUSE-", gx, gy + 40, gx + hL, gy + 40 + hW, GZ, GZ + hH,
                  doors={"S": [(gx + 10, "p")], "E": [(gy + 40 + hW / 2, "p")]}, avoid={"S": [(gx + 6, gx + 14)]},
                  louvres={"N": [(gx + 22, gx + 34, GZ + 7, GZ + 13)], "W": [(gy + 48, gy + 56, GZ + 7, GZ + 13)]})
    n2, td2, th2 = P["process_tank_n_d_h_ft"]
    for k in range(n2):
        tank_detail("GASMET-T%d-" % (k + 1), gx + 75 + k * 35, gy + 80, GZ, td2 / 2, th2, roof_h=2.0)
    # ---- CCS compressor building, amine tank ---------------------------------------------------------------------------
    cx0, cy0 = P["ccs_origin_ft"]
    clad_building("CCS-COMP-", cx0, cy0, cx0 + 80, cy0 + 40, GZ, GZ + 24,
                  doors={"S": [(cx0 + 12, "p"), (cx0 + 50, "r", 14.0, 16.0)], "E": [(cy0 + 20, "p")]}, avoid={"S": [(cx0 + 43, cx0 + 57)]},
                  louvres={"N": [(cx0 + 15, cx0 + 27, GZ + 14, GZ + 21), (cx0 + 40, cx0 + 52, GZ + 14, GZ + 21), (cx0 + 60, cx0 + 72, GZ + 14, GZ + 21)]})
    tank_detail("CCS-AMINE-", cx0 + 140, cy0 + 40, GZ, 15, 30, roof_h=2.5)
    # ---- ACC condensate tank (south side) -------------------------------------------------------------------------------------
    tank_detail("ACC-CT-", ACC_X0 + 80, ACC_Y0 - 22, GZ, 10, 24, roof_h=2.0)
    # ---- gate house, site office, switchyard control house -------------------------------------------------------------
    clad_building("SITE-GATEHOUSE-", 224, FENCE_IN - 6, 236, FENCE_IN + 6, GZ, GZ + 10, doors={"N": [(230, "p")]}, roof_ribs=False, plinth=False, downpipes=False)
    lx, ly = P["laydown_origin_ft"]
    clad_building("LAYDOWN-OFFICE-", lx + 140, ly + 20, lx + 160, ly + 28, GZ, GZ + 8.5, doors={"S": [(lx + 146, "p")]}, roof_ribs=False, plinth=False)
    sx, sy = SY_X0, SY_Y0
    clad_building("SWYD-CH-", sx + 20, sy + SY_W - 45, sx + 50, sy + SY_W - 25, GZ, GZ + 12, doors={"S": [(sx + 28, "p")], "E": [(sy + SY_W - 35, "p")]},
                  louvres={"N": [(sx + 34, sx + 44, GZ + 5, GZ + 10)]})
    # ---- absorber / regenerator / DCC columns --------------------------------------------------------------------------------
    ox, oy = P["ccs_origin_ft"]
    dd, dh = P["dcc_d_h_ft"]
    rd, rh_ = P["regenerator_d_h_ft"]
    column_detail("CCS-DCC-", ox + 28, oy + 300, GZ + 4, dd / 2, dh)
    column_detail("CCS-REGEN-", ox + 130, oy + 190, GZ + 4, rd / 2, rh_)
    aL, aW, aH = P["absorber_ft"]
    abx, aby = ox + 10, oy + 120
    ap = MeshAcc("CCS-ABSORBER-PLATFORMS", "STEEL")
    zz = 40.0
    prev = GZ
    while zz < aH:
        ap.box(abx + aL + 1.5, aby + 8, GZ + zz - 0.25, abx + aL + 7.5, aby + aW - 8, GZ + zz)
        ap.rail([(abx + aL + 7.5, aby + 8), (abx + aL + 7.5, aby + aW - 8), (abx + aL + 1.5, aby + aW - 8)], GZ + zz, 3.5, 5.0)
        ap.rail([(abx + aL + 1.5, aby + 8), (abx + aL + 7.5, aby + 8)], GZ + zz, 3.5, 5.0, toe=False)
        ap.ladder(abx + aL + 7.1, aby + 12 + (int(zz / 40) % 2) * 20, GZ + prev if prev > 0 else GZ, GZ + zz, face=(-1, 0), cage=True)
        prev = zz
        zz += 40.0
    yy = aby + 10
    while yy < aby + aW:
        for zg in range(40, int(aH), 40):
            ap.box(abx - 0.3, yy, GZ + zg - 0.35, abx + aL + 0.3, yy + 0.6, GZ + zg)
        yy += 14
    ap.build()
    ab_top = MeshAcc("CCS-ABSORBER-TOP", "STEEL")
    ztop = P["ccs_outlet_z_ft"]
    ab_top.box(abx + aL / 2 - 12, aby + aW / 2 - 12, GZ + aH - 0.25, abx + aL / 2 + 12, aby + aW / 2 + 12, GZ + aH)
    ab_top.rail([(abx + aL / 2 - 12, aby + aW / 2 - 12), (abx + aL / 2 + 12, aby + aW / 2 - 12), (abx + aL / 2 + 12, aby + aW / 2 + 12), (abx + aL / 2 - 12, aby + aW / 2 + 12), (abx + aL / 2 - 12, aby + aW / 2 - 12)], GZ + aH, 3.5, 6.0)
    ab_top.box(abx + aL / 2 - 10.5, aby + aW / 2 - 10.5, GZ + ztop, abx + aL / 2 + 10.5, aby + aW / 2 + 10.5, GZ + ztop + 0.8)
    ab_top.build()

# ---- switchyard ---------------------------------------------------------------------------------------
def detail_switchyard():
    x0, y0 = SY_X0, SY_Y0
    x1, y1 = x0 + SY_L, y0 + SY_W
    pl = MeshAcc("SWYD-PLINTHS", "CONC")
    lg = MeshAcc("SWYD-GROUND-LUGS", "COPPER")
    for bx in (170, 250, 330, 410):
        for dy in (-15, 0, 15):
            pl.box(bx - 4.5, 1180 + dy - 2.0, GZ, bx + 4.5, 1180 + dy + 2.0, GZ + 0.6)
            for yd in (1152, 1208):
                pl.box(bx - 4.5, yd + dy - 1.0, GZ, bx + 4.5, yd + dy + 1.0, GZ + 0.5)
            pl.box(bx - 1.5, 1196 + dy - 1.5, GZ, bx + 1.5, 1196 + dy + 1.5, GZ + 0.5)
            for sx in (-1, 1):
                lg.box(bx + sx * 3.4 - 0.25, 1180 + dy - 2.0, GZ + 0.6, bx + sx * 3.4 + 0.25, 1180 + dy - 1.6, GZ + 1.6)
    for x in (230, 250, 270):
        pl.box(x - 1.5, y1 - 30 - 1.5, GZ, x + 1.5, y1 - 30 + 1.5, GZ + 0.5)
    pl.build(); lg.build()
    # insulator strings at the dead-ends (line entry and grid exit)
    ins = MeshAcc("SWYD-INSULATOR-STRINGS", "PORCELAIN")
    for (xs, ys, zt) in [(405 + pi * 12 + ci * 6, 1090, 56) for pi in range(3) for ci in range(2)] + [(x, y1 - 10, 56) for x in (230, 250, 270)]:
        for k in range(16):
            ins.cyl(xs, ys, zt - 0.5 - (k + 1) * 0.36, 0.65, 0.14, 12)
        ins.seg((xs, ys, zt), (xs, ys, zt - 0.6), 0.09, 4)
    ins.build()
    # bus spacers / clamps
    cl = MeshAcc("SWYD-BUS-CLAMPS", "STEEL_DK")
    for yb in (1130, 1230):
        for x in range(int(x0) + 30, int(x1) - 20, 60):
            for dy in (-15, 0, 15):
                cl.box(x - 0.6, yb + dy - 0.6, 39.6, x + 0.6, yb + dy + 0.6, 40.8)
            cl.box(x - 0.2, yb - 15, 40.0, x + 0.2, yb + 15, 40.3)
    cl.build()
    # cable trench with cover plates + marshalling kiosks + lighting masts
    tr = MeshAcc("SWYD-TRENCH", "CONC")
    tr.box(x0 + 20, 1262, GZ, x1 - 20 - 0, 1264.5, GZ + 0.5)
    tr.box(x0 + 20, 1262, GZ, x0 + 22, 1300, GZ + 0.5)
    tr.build()
    cv = MeshAcc("SWYD-TRENCH-COVERS", "STEEL")
    x = x0 + 22
    while x < x1 - 22:
        cv.box(x, 1262.2, GZ + 0.5, x + 3.6, 1264.3, GZ + 0.62)
        x += 4.0
    cv.build()
    mk = MeshAcc("SWYD-MARSHALLING-KIOSKS", "ENCL")
    for bx in (170, 250, 330, 410):
        mk.box(bx - 1.5, 1266, GZ, bx + 1.5, 1268.5, GZ + 5.5)
        mk.box(bx - 1.6, 1265.9, GZ + 5.5, bx + 1.6, 1268.6, GZ + 5.8)
        mk.box(bx - 1.2, 1265.95, GZ + 0.4, bx + 1.2, 1266.0, GZ + 5.0)
    mk.build()
    mt = MeshAcc("SWYD-LIGHTS", "STEEL_DK")
    for (x, y) in ((x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x0 + 10, y1 - 10), (x1 - 10, y1 - 10)):
        for zz in (70.0, 84.0):
            mt.box(x - 1.2, y - 0.5, zz, x + 1.2, y + 0.5, zz + 0.9)
    mt.build()


# ---- BESS, modular yard, laydown ---------------------------------------------------------------------------
def detail_bess():
    x0, y0 = P["bess_origin_ft"]
    cL, cW, cH = P["bess_ft"]
    pL, pW, pH = P["pcs_tx_ft"]
    co = MeshAcc("BESS-CONTAINER-DETAIL", "ENCL")
    dr = MeshAcc("BESS-DOORS", "STEEL")
    hv = MeshAcc("BESS-HVAC-DETAIL", "STEEL_DK")
    ps = MeshAcc("BESS-PCS-DETAIL", "STEEL")
    fin = MeshAcc("BESS-TX-FINS", "STEEL_DK")
    cur = MeshAcc("BESS-SKID-CURBS", "CONC")
    for row in range(2):
        for col in range(4):
            cx0 = x0 + 10 + col * 50
            cy0 = y0 + 10 + row * 50
            zb = GZ + 0.5
            # corrugation on both long faces
            co.ribs_x(cy0, -1, cx0 + 0.5, cx0 + cL - 0.5, zb + 0.5, zb + cH - 0.4, 1.4, 0.5, 0.12)
            co.ribs_x(cy0 + cW, 1, cx0 + 0.5, cx0 + cL - 0.5, zb + 0.5, zb + cH - 0.4, 1.4, 0.5, 0.12, avoid=[(cx0 + 3, cx0 + 10), (cx0 + cL - 10, cx0 + cL - 3)])
            # roof ribs and vents
            xr = cx0 + 1.0
            while xr < cx0 + cL - 1:
                co.box(xr, cy0 + 0.3, zb + cH, xr + 0.25, cy0 + cW - 0.3, zb + cH + 0.12)
                xr += 3.0
            co.box(cx0 + 12, cy0 + 2, zb + cH, cx0 + 16, cy0 + 6, zb + cH + 0.9).box(cx0 + 24, cy0 + 2, zb + cH, cx0 + 28, cy0 + 6, zb + cH + 0.9)
            # corner castings
            for xx in (cx0 - 0.3, cx0 + cL - 0.3):
                for yy in (cy0 - 0.3, cy0 + cW - 0.3):
                    for zz in (zb - 0.3, zb + cH - 0.3):
                        co.box(xx, yy, zz, xx + 0.6, yy + 0.6, zz + 0.6)
            # end doors with locking bars, hinges and handles
            for xf, sg in ((cx0, -1), (cx0 + cL, 1)):
                for half in range(2):
                    ya = cy0 + 0.3 + half * 3.85
                    xa, xb = (xf - 0.16, xf) if sg < 0 else (xf, xf + 0.16)
                    dr.box(xa, ya, zb + 0.9, xb, ya + 3.7, zb + cH - 0.5)
                    for lr in (0.9, 2.4):
                        xc = xf + sg * 0.22
                        dr.cyl_between((xc, ya + lr, zb + 1.0), (xc, ya + lr, zb + cH - 0.6), 0.05, 5)
                    dr.box(min(xf, xf + sg * 0.3), ya + (3.0 if half == 0 else 0.4), zb + 4.0, max(xf, xf + sg * 0.3), ya + (3.3 if half == 0 else 0.7), zb + 5.0)
            # HVAC fan grilles on the service face
            for hx in (cx0 + 6.5, cx0 + cL - 6.5):
                yy = cy0 + cW + 2.0
                hv.cyl_between((hx, yy, GZ + 4.5), (hx, yy + 0.18, GZ + 4.5), 1.6, 18)
                hv.cyl_between((hx, yy + 0.18, GZ + 4.5), (hx, yy + 0.3, GZ + 4.5), 0.3, 8)
                for a in (0, 60, 120):
                    hv.boxc(hx, yy + 0.24, GZ + 4.5, 3.0, 0.08, 0.12, rot=math.radians(a))
            # PCS skid: louvres, doors, fins, curb
            py0 = cy0 + cW + 6
            ps.louvre_x(cx0 + 10.5, cx0 + 17.5, py0 + pW - 1, 1, GZ + 2.0, GZ + 8.0, 0.5, 0.3)
            ps.door_x(cx0 + 12, py0 + 1, -1, GZ + 0.8, 3.4, 7.0)
            for sx, sgx in ((cx0 + 21, -1), (cx0 + 31, 1)):
                yy = py0 + 2.0
                while yy < py0 + pW - 2.0:
                    fin.box(min(sx, sx + sgx * 0.8), yy, GZ + 1.6, max(sx, sx + sgx * 0.8), yy + 0.13, GZ + pH - 2.4)
                    yy += 0.55
            cur.box(cx0 + 7.6, py0 - 0.4, GZ + 0.8, cx0 + 8 + pL + 0.4, py0, GZ + 1.3).box(cx0 + 7.6, py0 + pW, GZ + 0.8, cx0 + 8 + pL + 0.4, py0 + pW + 0.4, GZ + 1.3)
            cur.box(cx0 + 7.6, py0, GZ + 0.8, cx0 + 8, py0 + pW, GZ + 1.3).box(cx0 + 8 + pL, py0, GZ + 0.8, cx0 + 8 + pL + 0.4, py0 + pW, GZ + 1.3)
    co.build(); dr.build(); hv.build(); ps.build(); fin.build(); cur.build()
    # switchgear container detail
    clad_building("BESS-SWGR-", x0 + 226, y0 + 88, x0 + 246, y0 + 96, GZ, GZ + 9, doors={"S": [(x0 + 233, "p"), (x0 + 240, "p")]}, avoid={"S": [(x0 + 230, x0 + 244)]}, roof_ribs=False, plinth=False, parapet=False, downpipes=False)


def detail_modular():
    x0, y0 = P["modular_origin_ft"]
    gL, gW, gH = P["genset_ft"]
    fL, fW, fH = P["fuel_cell_ft"]
    co = MeshAcc("MODPWR-CONTAINER-DETAIL", "ENCL")
    dr = MeshAcc("MODPWR-DOORS", "STEEL")
    lv = MeshAcc("MODPWR-LOUVRES", "STEEL_DK")
    ex = MeshAcc("MODPWR-EXHAUST-DETAIL", "STEEL_DK")
    for k in range(3):
        gx, gy = x0 + 10, y0 + 10 + k * 22
        zb = GZ + 0.5
        co.ribs_x(gy, -1, gx + 0.5, gx + gL - 0.5, zb + 0.6, zb + gH - 0.4, 1.6, 0.5, 0.12, avoid=[(gx + 4, gx + 9)])
        co.ribs_x(gy + gW, 1, gx + 0.5, gx + gL - 0.5, zb + 0.6, zb + gH - 0.4, 1.6, 0.5, 0.12, avoid=[(gx + 12, gx + 30)])
        dr.door_x(gx + 6.5, gy, -1, zb, 3.2, 6.6)
        lv.louvre_x(gx + 12, gx + 30, gy + gW, 1, zb + 3.0, zb + gH - 3.0, 0.5, 0.25)
        lv.louvre_y(gy + 1, gy + gW - 1, gx + gL + 2, 1, zb + 2.0, zb + gH - 2.0, 0.5, 0.35)
        for xx in (gx - 0.3, gx + gL - 0.3):
            for yy in (gy - 0.3, gy + gW - 0.3):
                for zz in (zb - 0.3, zb + gH - 0.3):
                    co.box(xx, yy, zz, xx + 0.6, yy + 0.6, zz + 0.6)
        ex.stiff_ring(gx + 20, gy + gW / 2, GZ + gH + 1.5, 0.6, 0.3, 0.12, 12)
        ex.cyl(gx + 20, gy + gW / 2, GZ + gH + 7.5, 1.0, 1.4, 10, r2=0.6)
        ex.cyl(gx + 20, gy + gW / 2, GZ + gH + 6.6, 0.8, 0.25, 10)
        for xx in (gx + 8, gx + 14):
            ex.cyl(xx, gy + gW / 2, GZ + gH + 0.9, 0.9, 0.3, 10)
    co.build(); dr.build(); lv.build(); ex.build()
    fc = MeshAcc("MODPWR-FUELCELL-DETAIL", "ENCL")
    fd = MeshAcc("MODPWR-FUELCELL-FINS", "STEEL_DK")
    for k in range(4):
        fx, fy = x0 + 80 + k * 26, y0 + 12
        fc.ribs_x(fy, -1, fx + 0.5, fx + fL - 0.5, GZ + 0.6, GZ + fH - 0.3, 1.5, 0.5, 0.1)
        xx = fx + 8
        while xx < fx + fL - 1:
            fd.box(xx, fy + 1, GZ + fH, xx + 0.12, fy + fW - 1, GZ + fH + 1.8)
            xx += 0.6
    fc.build(); fd.build()
    clad_building("MODPWR-SWGR-", x0 + 100, y0 + 70, x0 + 120, y0 + 78, GZ, GZ + 9, doors={"S": [(x0 + 106, "p"), (x0 + 114, "p")]}, avoid={"S": [(x0 + 103, x0 + 117)]}, roof_ribs=False, plinth=False, parapet=False, downpipes=False)


def detail_laydown():
    x0, y0 = P["laydown_origin_ft"]
    rd, rw = P["reel_d_w_ft"]
    wc = MeshAcc("LAYDOWN-REEL-WINDINGS", "CABLE")
    sp = MeshAcc("LAYDOWN-REEL-SPOKES", "STEEL_DK")
    for k in range(P["counts"]["reels"]):
        cx, cy = x0 + 20 + k * 22, y0 + 24
        r = rd / 2 + (1.0 if k % 2 else 0.0)
        z = r + 1.5
        wc.cyl_between((cx - rw / 2 + 0.5, cy, z), (cx + rw / 2 - 0.1, cy, z), r * 0.82, 28)
        for a in range(0, 360, 30):
            aa = math.radians(a)
            for xf in (cx - rw / 2 - 0.25, cx + rw / 2 + 0.05):
                sp.seg((xf, cy + r * 0.5 * math.cos(aa), z + r * 0.5 * math.sin(aa)), (xf, cy + r * 0.95 * math.cos(aa), z + r * 0.95 * math.sin(aa)), 0.1, 4)
        sp.cyl_between((cx - rw / 2 - 0.45, cy, z), (cx + rw / 2 + 0.45, cy, z), 0.7, 12)          # hub / arbor
    wc.build(); sp.build()
    # sheave rollers under the pulled cables, on stands
    cx3 = x0 + 20 + 2 * 22
    ro = MeshAcc("LAYDOWN-ROLLERS", "STEEL")
    y = y0 + 24 + 12
    sy = y0 + 70
    while y < sy - 8:
        for xo in (-1.5, -0.5, 0.5, 1.5):
            pass
        ro.cyl_between((cx3 - 3.0, y, GZ + 1.1), (cx3 + 3.0, y, GZ + 1.1), 0.4, 10)
        ro.box(cx3 - 3.3, y - 0.4, GZ, cx3 - 2.9, y + 0.4, GZ + 1.1).box(cx3 + 2.9, y - 0.4, GZ, cx3 + 3.3, y + 0.4, GZ + 1.1)
        y += 4.0
    ro.build()
    # canopy frame over the prefab spine (open frame + hanging lights + monorail)
    sx0, sy = x0 + 40, y0 + 70
    cp = MeshAcc("LAYDOWN-CANOPY", "STEEL")
    L = P["prefab_spine_l_ft"] + 12
    xs0 = sx0 - 6
    for xx in (xs0, xs0 + L / 2, xs0 + L):
        for yy in (sy - 6, sy + 6):
            cp.box(xx - 0.4, yy - 0.4, GZ, xx + 0.4, yy + 0.4, GZ + 14)
        cp.box(xx - 0.3, sy - 6.4, GZ + 13.4, xx + 0.3, sy + 6.4, GZ + 14.0)
    for yy in (sy - 6, sy, sy + 6):
        cp.box(xs0 - 0.3, yy - 0.2, GZ + 14.0, xs0 + L + 0.3, yy + 0.2, GZ + 14.5)
    xx = xs0
    while xx <= xs0 + L:
        cp.box(xx - 0.15, sy - 6.4, GZ + 14.0, xx + 0.15, sy + 6.4, GZ + 14.3)
        xx += 4.0
    for xx in (xs0, xs0 + L):
        cp.seg((xx, sy - 6, GZ), (xx, sy + 6, GZ + 13.4), 0.12, 4)
        cp.seg((xx, sy + 6, GZ), (xx, sy - 6, GZ + 13.4), 0.12, 4)
    cp.box(xs0 + 3, sy - 0.4, GZ + 12.0, xs0 + L - 3, sy + 0.4, GZ + 12.5)               # monorail with hoist
    cp.box(xs0 + L / 2 - 1.5, sy - 1.0, GZ + 10.5, xs0 + L / 2 + 1.5, sy + 1.0, GZ + 12.0)
    for xx in range(int(xs0) + 5, int(xs0 + L), 10):
        cp.seg((xx, sy - 3, GZ + 14.0), (xx, sy - 3, GZ + 12.5), 0.05, 4)
        cp.cyl(xx, sy - 3, GZ + 11.9, 0.9, 0.6, 12, r2=1.3)
    cp.build()
    # workbench with cable cutter, barrier panels, pallets, telehandler
    wb = MeshAcc("LAYDOWN-WORKBENCH", "STEEL")
    wb.box(sx0 + 46, sy - 3, GZ + 2.8, sx0 + 54, sy + 3, GZ + 3.2)
    for xx in (sx0 + 46.4, sx0 + 53.6):
        for yy in (sy - 2.6, sy + 2.6):
            wb.box(xx - 0.2, yy - 0.2, GZ, xx + 0.2, yy + 0.2, GZ + 2.8)
    wb.box(sx0 + 48, sy - 1.5, GZ + 3.2, sx0 + 51, sy + 1.5, GZ + 4.2)
    wb.build()
    bar = MeshAcc("LAYDOWN-BARRIERS", "STEEL_DK")
    bpts = [(x0 + 4, y0 + 8), (x0 + 4, y0 + 46), (x0 + 140, y0 + 46), (x0 + 140, y0 + 8)]
    bar.rail(bpts, GZ, 3.5, 6.0, toe=False)
    bar.build()
    pa = MeshAcc("LAYDOWN-PALLETS", "ENCL")
    for k in range(4):
        px, py = x0 + 100 + k * 9, y0 + 88
        pa.box(px, py, GZ, px + 6, py + 5, GZ + 0.5)
        pa.box(px + 0.3, py + 0.3, GZ + 0.5, px + 5.7, py + 4.7, GZ + 3.5)
    pa.build()
    th = MeshAcc("LAYDOWN-TELEHANDLER", "STEEL")
    tx, ty = x0 + 150, y0 + 55
    th.box(tx, ty, GZ + 1.5, tx + 14, ty + 6, GZ + 4.5)
    th.box(tx + 9, ty + 0.5, GZ + 4.5, tx + 13, ty + 5.5, GZ + 8.0)
    th.seg((tx + 2, ty + 3, GZ + 4.0), (tx - 12, ty + 3, GZ + 11), 0.6, 6)
    th.box(tx - 14, ty + 1.2, GZ + 10.5, tx - 11.5, ty + 4.8, GZ + 11.2)
    for wx, wy in ((tx + 2.5, ty - 0.3), (tx + 11, ty - 0.3), (tx + 2.5, ty + 6.3), (tx + 11, ty + 6.3)):
        th.cyl_between((wx, wy - 0.3, GZ + 1.6), (wx, wy + 0.3, GZ + 1.6), 1.6, 14)
    th.build()
    anchor("LAYDOWN-CANOPY", sx0 + 20, sy, GZ + 15, "Canopy frame with monorail hoist", 3)
    anchor("LAYDOWN-ROLLERS", cx3, y0 + 55, GZ + 2.5, "Sheave rollers under the cable pull", 3)

# ---- ACC, cooling, gas, corridor, site furniture ----------------------------------------------------------
def detail_acc():
    x0, y0 = ACC_X0, ACC_Y0
    x1, y1 = x0 + ACC_L, y0 + ACC_W
    nx, ny = P["acc_cells"]
    deck = P["acc_fan_deck_ft"]
    cw = ACC_L / nx
    fr = P["acc_fan_d_ft"] / 2
    ym = (y0 + y1) / 2
    # column base plates with anchor bolts
    bp = MeshAcc("ACC-BASE-PLATES", "STEEL_DK")
    for i in range(nx + 1):
        for j in range(ny + 1):
            x, y = x0 + i * cw, y0 + j * cw
            bp.box(x - 1.7, y - 1.7, GZ, x + 1.7, y + 1.7, GZ + 0.5)
            for sx in (-1.2, 1.2):
                for sy in (-1.2, 1.2):
                    bp.cyl(x + sx, y + sy, GZ + 0.5, 0.14, 0.5, 6)
    bp.build()
    # fan-deck perimeter rail, walkway grating between rows, access ladder
    dk = MeshAcc("ACC-DECK-RAIL", "STEEL")
    dk.rail([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], deck, 3.5, 5.0)
    for j in range(ny + 1):
        yy = y0 + j * cw
        dk.box(x0, yy - 1.0, deck, x1, yy + 1.0, deck + 0.2)
    dk.ladder(x0 + 3, y0 - 0.3, GZ, deck, face=(0, -1), cage=True)
    dk.ladder(x1 - 3, y1 + 0.3, GZ, deck, face=(0, 1), cage=True)
    dk.build()
    # per-fan detail: gearbox, hub, shroud lip, motor cooling fins
    gb = MeshAcc("ACC-FAN-DETAIL", "STEEL_DK")
    for i in range(nx):
        for j in range(ny):
            cx, cy = x0 + (i + 0.5) * cw, y0 + (j + 0.5) * cw
            gb.cyl(cx, cy, deck + 0.4, 1.1, 1.8, 12)
            gb.cyl(cx, cy, deck + 5.0, fr + 0.45, 0.3, 28)
            for k in range(6):
                gb.box(cx + 1.6, cy - 1.0 + k * 0.4, deck + 0.8, cx + 1.75, cy - 0.85 + k * 0.4, deck + 2.6)
    gb.build()
    # steam duct expansion bellows and supports
    bl = MeshAcc("ACC-STEAM-DUCT-BELLOWS", "STEEL_DK")
    xx = HX1 + 25
    while xx < 1375:
        bl.cyl_between((xx, 730, 30), (xx + 0.5, 730, 30), 6.6, 24)
        xx += 45
    bl.build()
    clad_building("ACC-MCC-", x0 + 20, y0 - 32, x0 + 48, y0 - 24, GZ, GZ + 9, doors={"N": [(x0 + 30, "p"), (x0 + 38, "p")]}, avoid={"N": [(x0 + 26, x0 + 42)]}, roof_ribs=False, plinth=False, parapet=False, downpipes=False)


def detail_cooling():
    x0, y0 = P["chill_origin_ft"]
    cL, cW, cH = P["chiller_ft"]
    tL, tW, tH = P["tower_cell_ft"]
    ch = MeshAcc("CHILL-CHILLER-DETAIL", "STEEL")
    for k in range(P["counts"]["chiller"]):
        cx = x0 + 10 + k * 40
        yc = y0 + 20 + cW / 2
        for xe in (cx + 2, cx + cL - 2):
            ch.cyl_between((xe, yc, GZ + 6), (xe + 0.4, yc, GZ + 6), 3.5, 20)
            ch.cyl_between((xe, yc, GZ + 9.5), (xe + 0.4, yc, GZ + 9.5), 2.9, 18)
        ch.cyl_between((cx + 8, yc, GZ + 6), (cx + 8.3, yc, GZ + 6), 3.3, 20)
        ch.cyl(cx + 22, yc, GZ + 12.0, 1.7, 2.0, 16)                       # compressor motor
        ch.box(cx + 11, yc - 4.6, GZ + 3, cx + 15, yc - 4.5, GZ + 7.4)      # control panel door
        for zz in (GZ + 4.0, GZ + 8.0):
            ch.cyl_between((cx + 15, yc - 3, zz), (cx + 15, yc - 6.5, zz), 0.4, 8)
        ch.cyl(cx + 26, yc - 4.5, GZ + 3.0, 0.5, 2.2, 8)
        ch.cyl(cx + 26, yc - 4.5, GZ + 5.2, 0.9, 0.12, 12)                # valve handwheel
    ch.build()
    tl = MeshAcc("CHILL-TOWER-LOUVRES", "STEEL_DK")
    fanb = MeshAcc("CHILL-TOWER-FAN-BLADES", "STEEL")
    for k in range(P["counts"]["tower"]):
        tx = x0 + 10 + k * tL
        tl.louvre_x(tx + 2, tx + tL - 2, y0 + 80, -1, GZ + 4, GZ + 22, 0.5, 0.45)
        tl.louvre_x(tx + 2, tx + tL - 2, y0 + 80 + tW, 1, GZ + 4, GZ + 22, 0.5, 0.45)
        for a in range(0, 180, 30):
            fanb.boxc(tx + tL / 2, y0 + 80 + tW / 2, GZ + tH + 0.8, 14.0, 1.6, 0.14, rot=math.radians(a))
        fanb.cyl(tx + tL / 2, y0 + 80 + tW / 2, GZ + tH + 0.6, 1.0, 1.0, 10)
    tl.louvre_y(y0 + 82, y0 + 80 + tW - 2, x0 + 10, -1, GZ + 4, GZ + 22, 0.5, 0.45)
    tl.louvre_y(y0 + 82, y0 + 80 + tW - 2, x0 + 10 + P["counts"]["tower"] * tL, 1, GZ + 4, GZ + 22, 0.5, 0.45)
    tl.build(); fanb.build()
    tr = MeshAcc("CHILL-TOWER-DECK-RAIL", "STEEL")
    xe = x0 + 10 + P["counts"]["tower"] * tL
    tr.rail([(x0 + 10, y0 + 80), (xe, y0 + 80), (xe, y0 + 80 + tW), (x0 + 10, y0 + 80 + tW), (x0 + 10, y0 + 80)], GZ + tH, 3.5, 6.0)
    tr.ladder(xe + 0.3, y0 + 80 + tW / 2, GZ, GZ + tH, face=(1, 0), cage=True)
    tr.build()


def detail_gas():
    x0, y0 = P["gasmet_origin_ft"]
    yp = P["pipeline_y_ft"]
    pr = P["pipeline_d_ft"] / 2
    fl = MeshAcc("GASMET-FLANGES", "STEEL_DK")
    vv = MeshAcc("GASMET-VALVES", "STEEL_DK")
    ins = MeshAcc("GASMET-INSTRUMENTS", "ENCL")
    # flange rings along the ground run of the main pipeline
    xx = x0 + 100
    while xx < SW - PR_IN - 22:
        fl.cyl_between((xx, yp, GZ + 3), (xx + 0.28, yp, GZ + 3), pr * 1.75, 14)
        xx += 24
    xx = SW - FENCE_IN + 4
    # meter runs: valves with stems and hand wheels, orifice flanges, transmitters
    for k in range(3):
        yr = yp - 8 + k * 8
        for xv in (x0 + 90, x0 + 58):
            vv.box(xv - 1.4, yr - 1.1, GZ + 1.9, xv + 1.4, yr + 1.1, GZ + 4.1)
            vv.cyl(xv, yr, GZ + 4.1, 0.16, 2.2, 6)
            vv.cyl(xv, yr, GZ + 6.3, 0.9, 0.12, 14)
        for xf in (x0 + 66, x0 + 84):
            fl.cyl_between((xf, yr, GZ + 3), (xf + 0.22, yr, GZ + 3), 1.4, 12)
        ins.box(x0 + 74.5, yr - 0.6, GZ + 3.7, x0 + 75.5, yr + 0.6, GZ + 5.8)                    # DP transmitter
        ins.cyl(x0 + 75, yr, GZ + 5.8, 0.55, 0.6, 10)
        vv.cyl_between((x0 + 75, yr, GZ + 3.7), (x0 + 75, yr, GZ + 4.2), 0.08, 4)
        ins.box(x0 + 73.6, yr - 0.3, GZ, x0 + 76.4, yr + 0.3, GZ + 0.3)
    # pressure gauges + isolation valves on the header, sample points
    for xg in (x0 + 100, x0 + 50, x0 + 30):
        ins.cyl(xg, yp + 5.5, GZ + 4.5, 0.5, 0.25, 12)
        vv.cyl(xg, yp + 5.5, GZ + 3.0, 0.12, 1.5, 6)
    # ESD valve actuator flange + hand wheel; pig receiver door and pig signaller
    vv.cyl(x0 + 153, yp, GZ + 9.0, 0.5, 1.2, 10)
    vv.cyl_between((x0 + 142, yp - 12, GZ + 3), (x0 + 142.6, yp - 12, GZ + 3), 2.4, 16)
    vv.box(x0 + 141.8, yp - 9.9, GZ + 2.4, x0 + 142.4, yp - 9.5, GZ + 3.6)
    ins.cyl(x0 + 132, yp - 12, GZ + 4.5, 0.4, 0.8, 8)
    fl.build(); vv.build(); ins.build()
    # bollards around the pig receiver and the outside supply skids
    bo = MeshAcc("GASMET-BOLLARDS", "STEEL_DK")
    for k in range(6):
        bo.cyl(x0 + 118 + k * 5, yp - 17, GZ, 0.4, 3.0, 8)
    bo.build()
    # LNG vessel: saddle plates, top platform, relief stack; H2 module: manifold, gauges
    xl = SW
    lc = (xl + 140, 700)
    ld, lh = P["lng_d_h_ft"]
    lg = MeshAcc("FUELGAS-LNG-DETAIL", "STEEL")
    zc = GZ + ld / 2 + 3
    for dx in (-lh / 3, lh / 3):
        lg.box(lc[0] + dx - 2.4, lc[1] - ld / 2 - 0.8, GZ, lc[0] + dx + 2.4, lc[1] + ld / 2 + 0.8, GZ + 0.7)
    lg.box(lc[0] - 8, lc[1] - 3, zc + ld / 2 - 0.2, lc[0] + 8, lc[1] + 3, zc + ld / 2 + 0.1)
    lg.rail([(lc[0] - 8, lc[1] - 3), (lc[0] + 8, lc[1] - 3), (lc[0] + 8, lc[1] + 3), (lc[0] - 8, lc[1] + 3), (lc[0] - 8, lc[1] - 3)], zc + ld / 2 + 0.1, 3.5, 5.0)
    lg.ladder(lc[0] + lh / 3 + 3.2, lc[1] - ld / 2 - 1.2, GZ, zc + ld / 2, face=(0, -1), cage=True)
    lg.cyl(lc[0] + 4, lc[1], zc + ld / 2 + 0.1, 0.5, 6.0, 8)
    lg.cyl(lc[0] + 4, lc[1], zc + ld / 2 + 6.1, 0.9, 0.4, 10)
    lg.build()
    hc = (xl + 130, 470)
    hL, hW, hH = P["h2_module_ft"]
    hg = MeshAcc("FUELGAS-H2-DETAIL", "STEEL")
    for k in range(4):
        for rr in range(2):
            hg.cyl_between((hc[0] + hL - 1, hc[1] + 1.5 + k * 1.7, GZ + 2 + rr * 3.4), (hc[0] + hL + 0.6, hc[1] + 1.5 + k * 1.7, GZ + 2 + rr * 3.4), 0.35, 8)
    hg.cyl_between((hc[0] + hL + 0.6, hc[1] + 1.0, GZ + 2), (hc[0] + hL + 0.6, hc[1] + hW - 1.0, GZ + 5.4), 0.45, 8)
    hg.cyl(hc[0] + hL + 0.6, hc[1] + hW / 2, GZ + 3.6, 0.5, 0.25, 10)
    hg.rail([(hc[0] - 0.5, hc[1] - 0.5), (hc[0] + hL + 1.2, hc[1] - 0.5)], GZ, 3.0, 8.0, toe=False)
    hg.build()


def detail_corridor():
    y0 = CORR_Y
    yt = y0 + 18
    yd = y0 + 8
    zp, zc = P["tray_power_control_z_ft"]
    x0, x1 = CORR_X0, CORR_X1
    mk = MeshAcc("CORR-MARKER-POSTS", "CONC")
    lb = MeshAcc("CORR-CABLE-LABELS", "ENCL")
    ct = MeshAcc("CORR-CABLE-TIES", "CABLE")
    bj = MeshAcc("CORR-BONDING-JUMPERS", "COPPER")
    jb = MeshAcc("CORR-JUNCTION-BOXES", "ENCL")
    x = x0 + 30
    while x < x1:
        if not on_road(x, yd, 3.0):
            mk.box(x - 0.3, yd - 0.3, GZ, x + 0.3, yd + 0.3, GZ + 2.6)
            mk.box(x - 0.5, yd - 0.5, GZ, x + 0.5, yd + 0.5, GZ + 0.4)
        x += 60
    x = x0 + 25
    while x < x1 - 10:
        if not on_road(x, yt, 3.0):
            lb.box(x, yt - 1.62, zp + 0.05, x + 0.5, yt - 1.5, zp + 0.4)
            lb.box(x, yt - 1.12, zc + 0.05, x + 0.5, yt - 1.0, zc + 0.4)
            for kk in range(3):
                ct.box(x + 3 + kk * 1.6, yt - 1.4, zp + 0.3, x + 3.15 + kk * 1.6, yt + 1.5, zp + 0.42)
            ct.box(x + 3, yt - 0.9, zc + 0.25, x + 3.15, yt + 0.9, zc + 0.35)
            if int(x) % 10 == 5:
                bj.cyl_between((x + 5, yt - 1.5, zp + 0.5), (x + 5, yt + 1.5, zp + 0.5), 0.07, 5)
        x += 20
    x = x0 + 40
    while x < x1:
        if not on_road(x, yt, 3.0):
            jb.box(x - 0.8, yt + 2.2, GZ, x + 0.8, yt + 2.9, GZ + 3.0)
            jb.box(x - 0.9, yt + 2.1, GZ + 3.0, x + 0.9, yt + 3.0, GZ + 3.2)
        x += 120
    mk.build(); lb.build(); ct.build(); bj.build(); jb.build()
    # MV kiosks: doors, hoods, plinths; pad-mount transformer: cooling fins, dead-front door, bushing covers
    kd = MeshAcc("CORR-KIOSK-DETAIL", "ENCL")
    tf = MeshAcc("CORR-PADMOUNT-DETAIL", "STEEL_DK")
    for lx in P["mv_laterals_x_ft"]:
        ky = y0 + CORR_W + 6
        kd.box(lx - 4.1, ky - 0.1, GZ, lx + 4.1, ky + 4.1, GZ + 0.5)
        kd.box(lx - 4.15, ky - 0.15, GZ + 8, lx + 4.15, ky + 4.15, GZ + 8.3)
        for d in (-2, 2):
            kd.box(lx + d - 1.5, ky - 0.08, GZ + 0.8, lx + d + 1.5, ky, GZ + 7.2)
            kd.box(lx + d + 1.1, ky - 0.18, GZ + 3.5, lx + d + 1.3, ky, GZ + 4.5)
        yy = ky + 0.7
        while yy < ky + 5.5:
            tf.box(lx + 14, yy, GZ + 0.8, lx + 14.6, yy + 0.15, GZ + 5.2)
            yy += 0.6
        tf.box(lx + 8, ky - 0.1, GZ + 0.6, lx + 14, ky, GZ + 5.4)
        tf.box(lx + 7.9, ky + 6.0, GZ + 6, lx + 14.1, ky + 6.1, GZ + 6.5)
    kd.build(); tf.build()
    # local earth-grid patch under the kiosks (the whole-site grid is hidden on the corridor sheet)
    zg = P["earth_z_pitch_ft"][0]
    eg = CurveAcc("CORR-EARTH-PATCH", "CABLE", 0.09, below=True)
    gx = 1100.0
    while gx <= 1450.0:
        eg.add([(gx, y0 - 30, zg), (gx, y0 + 90, zg)])
        gx += 25.0
    gy = y0 - 30.0
    while gy <= y0 + 90:
        eg.add([(1100, gy, zg), (1450, gy, zg)])
        gy += 25.0
    eg.build()
    anchor("CORR-EARTH-PATCH", 1215, y0 + 30, zg, "Earth grid (copper riser bonds to it)", 16)


def detail_site():
    poles = MeshAcc("SITE-LIGHT-POLES", "STEEL")
    heads = MeshAcc("SITE-LIGHT-HEADS", "STEEL_DK")
    hyd = MeshAcc("SITE-HYDRANTS", "STEEL")
    cb = MeshAcc("SITE-CATCH-BASINS", "STEEL_DK")
    def pole(x, y, arm):
        if blocked(x, y, 3.0, 40.0) or on_road(x, y, 0.5):
            return
        poles.box(x - 0.8, y - 0.8, GZ - 0.2, x + 0.8, y + 0.8, GZ + 0.8)
        poles.cyl(x, y, GZ + 0.8, 0.5, 32, 10, r2=0.28)
        ax_, ay_ = arm
        poles.seg((x, y, GZ + 31.5), (x + ax_ * 6.0, y + ay_ * 6.0, GZ + 33.0), 0.16, 6)
        heads.box(x + ax_ * 6.0 - 1.4, y + ay_ * 6.0 - 0.7, GZ + 32.5, x + ax_ * 6.0 + 1.4, y + ay_ * 6.0 + 0.7, GZ + 33.3)
    rw = ROAD_W / 2
    y = 120.0
    while y < SH - 100:
        for xr in P["ns_roads_x_ft"]:
            pole(xr + rw + 2.5, y, (-1, 0))
            pole(xr - rw - 2.5, y + 55, (1, 0))
        y += 110.0
    x = 100.0
    while x < SW - 100:
        pole(x, SPINE_Y + rw + 2.5, (0, -1))
        pole(x + 55, SPINE_Y - rw - 2.5, (0, 1))
        x += 110.0
    for k in range(int((SW - 200) / 140)):
        pole(150 + k * 140, PR_IN + rw + 3.0, (0, -1))
        pole(150 + k * 140, SH - PR_IN - rw - 3.0, (0, 1))
    for k in range(int((SH - 200) / 140)):
        pole(PR_IN + rw + 3.0, 150 + k * 140, (-1, 0))
        pole(SW - PR_IN - rw - 3.0, 150 + k * 140, (1, 0))
    # hydrants and catch basins along the N-S roads, bollards at the gate
    for xr in P["ns_roads_x_ft"]:
        yy = 200.0
        while yy < SH - 150:
            hx_, hy_ = xr - rw - 1.8, yy
            if not blocked(hx_, hy_, 2.0, 10.0) and not on_road(hx_, hy_, 0.3):
                hyd.cyl(hx_, hy_, GZ, 0.5, 2.8, 10)
                hyd.cyl(hx_, hy_, GZ + 2.8, 0.7, 0.3, 10)
                hyd.cyl_between((hx_ - 0.9, hy_, GZ + 2.0), (hx_ + 0.9, hy_, GZ + 2.0), 0.3, 8)
            cb.box(xr + rw - 1.6, yy + 40, 0.12, xr + rw - 0.1, yy + 41.5, 0.22)
            yy += 300.0
    poles.build(); heads.build(); hyd.build(); cb.build()
    # fence outriggers (barbed-wire arms) every 20 ft along the straight runs, and the sliding gate
    fo = MeshAcc("SITE-FENCE-OUTRIGGERS", "STEEL_DK")
    f = FENCE_IN
    h = P["fence_h_ft"]
    runs = [((f, f), (180, f)), ((220, f), (SW - f, f)), ((SW - f, f), (SW - f, SH - f)), ((SW - f, SH - f), (f, SH - f)), ((f, SH - f), (f, f))]
    for (a, b) in runs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(L / 20)
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        ox, oy = uy, -ux                   # push the arms toward the outside of the site
        if a[1] == f and b[1] == f:
            ox, oy = 0.0, -1.0
        elif a[0] == SW - f and b[0] == SW - f:
            ox, oy = 1.0, 0.0
        elif a[1] == SH - f and b[1] == SH - f:
            ox, oy = 0.0, 1.0
        else:
            ox, oy = -1.0, 0.0
        for i in range(n + 1):
            px, py = a[0] + ux * i * 20, a[1] + uy * i * 20
            fo.seg((px, py, h), (px + ox * 1.6, py + oy * 1.6, h + 1.6), 0.06, 4)
        for dz in (0.0, 0.8):
            fo.seg((a[0] + ox * 1.6, a[1] + oy * 1.6, h + 1.6 - dz * 0.0), (b[0] + ox * 1.6, b[1] + oy * 1.6, h + 1.6), 0.03, 3)
    fo.build()
    gt = MeshAcc("SITE-GATE", "STEEL")
    gt.box(178.5, f - 0.5, 0, 180.5, f + 0.5, h + 1.0).box(219.5, f - 0.5, 0, 221.5, f + 0.5, h + 1.0)
    gt.box(180.5, f - 0.25, 0.8, 200, f + 0.25, 1.1).box(180.5, f - 0.25, h - 0.6, 200, f + 0.25, h - 0.3)
    for k in range(10):
        gt.box(181 + k * 2, f - 0.2, 1.1, 181.25 + k * 2, f + 0.2, h - 0.6)
    gt.seg((180.5, f, 1.1), (200, f, h - 0.6), 0.1, 4)
    gt.build()
    br = MeshAcc("SITE-GATE-BARRIER", "STEEL_DK")
    br.box(214.0, 44.6, GZ, 215.0, 45.6, GZ + 4.0)
    br.box(214.0, 44.6, GZ + 3.0, 226.0, 45.6, GZ + 3.5)
    br.build()



def detail_interiors():
    # ---- e-house: control / relay panel rows, floor plates, overhead-tray gantries, wall boards ---------------
    x0, y0 = P["ehouse_origin_ft"]
    L, W, H = P["ehouse_ft"]
    zf = GZ + P["ehouse_floor_ft"]
    x1, y1 = x0 + L, y0 + W
    ym = (y0 + y1) / 2.0
    cp = MeshAcc("ELEC-EHOUSE-CONTROL-PANELS", "ENCL")
    cabinet_row(cp, x0 + 8, ym - 2.6, zf, 22, 2.6, 2.4, 7.5, "x", "both")
    cp.build()
    dc = MeshAcc("ELEC-EHOUSE-DC-CHARGERS", "ENCL")
    cabinet_row(dc, x0 + 68, ym - 2.6, zf, 4, 3.0, 2.6, 7.5, "x", "both")
    dc.build()
    fp = MeshAcc("ELEC-EHOUSE-FLOOR-PLATES", "STEEL")
    for (xa, xb, ya, yb) in ((x0 + 6, x0 + 66, ym - 6.0, ym - 3.0), (x0 + 6, x0 + 66, ym + 3.0, ym + 6.0), (x0 + 6, x0 + 62, y1 - 12, y1 - 9),
                            (x0 + 38, x0 + 68, y1 - 12, y1 - 8), (x0 + 6, x0 + 30, y0 + 4, y0 + 7)):
        fp.box(xa, ya, zf, xb, yb, zf + 0.12)
        xx = xa + 3
        while xx < xb:
            fp.box(xx, ya, zf + 0.12, xx + 0.08, yb, zf + 0.2)
            xx += 3.0
    fp.build()
    tg = MeshAcc("ELEC-EHOUSE-TRAY-GANTRIES", "STEEL")
    for xx in range(int(x0) + 10, int(x1) - 8, 22):
        for yy in (ym - 3.2, ym + 3.2):
            tg.box(xx - 0.2, yy - 0.2, zf, xx + 0.2, yy + 0.2, zf + 11.0)
        tg.box(xx - 0.25, ym - 3.4, zf + 10.4, xx + 0.25, ym + 3.4, zf + 10.9)
    tg.build()
    wb = MeshAcc("ELEC-EHOUSE-WALL-BOARDS", "ENCL")
    for k in range(5):
        xx = x1 - 30 + k * 5.5
        wb.box(xx, y1 - 1.0, zf + 1.8, xx + 3.5, y1 - 0.6, zf + 6.4)
        wb.box(xx + 0.25, y1 - 1.04, zf + 2.2, xx + 3.25, y1 - 1.0, zf + 6.0)
    wb.box(x0 + 100, y1 - 1.2, zf + 2.0, x0 + 103, y1 - 0.6, zf + 5.5)
    wb.build()
    fs = MeshAcc("ELEC-EHOUSE-FIRE-SYSTEM", "STEEL_DK")
    for k in range(6):
        fs.cyl(x0 + 112, y1 - 3 - k * 1.0, zf, 0.4, 3.6, 8)
    fs.cyl_between((x0 + 105, y1 - 1.5, zf + 6.5), (x0 + 118, y1 - 1.5, zf + 6.5), 0.18, 6)
    fs.build()
    # ---- MCC room: motor control rows, drive lineup and UPS with floor plates -----------------------------
    x0, y0 = P["mcc_origin_ft"]
    L, W, H = P["mcc_ft"]
    z0 = GZ + 0.5
    x1, y1 = x0 + L, y0 + W
    mc = MeshAcc("ELEC-MCC-MCC-ROW-B", "ENCL")
    cabinet_row(mc, x0 + 3, y0 + 27, z0, 12, 2.0, 1.7, 7.5, "x", "both")
    mc.build()
    vf = MeshAcc("ELEC-MCC-VFD-ROW-B", "ENCL")
    cabinet_row(vf, x0 + 33, y0 + 20, z0, 5, 4.0, 3.0, 8.0, "x", "both")
    vf.build()
    fp = MeshAcc("ELEC-MCC-FLOOR-PLATES", "STEEL")
    for (xa, xb, ya, yb) in ((x0 + 3, x0 + 27, y1 - 8, y1 - 5.4), (x0 + 33, x0 + 53, y1 - 10, y1 - 6), (x0 + 3, x0 + 27, y0 + 22, y0 + 25), (x0 + 58, x0 + 76, y1 - 8, y1 - 5.5)):
        fp.box(xa, ya, z0, xb, yb, z0 + 0.12)
        xx = xa + 3
        while xx < xb:
            fp.box(xx, ya, z0 + 0.12, xx + 0.08, yb, z0 + 0.2)
            xx += 3.0
    fp.build()
    tg = MeshAcc("ELEC-MCC-TRAY-GANTRIES", "STEEL")
    for xx in range(int(x0) + 8, int(x1) - 4, 18):
        for yy in (y0 + 10.5, y0 + 13.5):
            tg.box(xx - 0.2, yy - 0.2, z0, xx + 0.2, yy + 0.2, z0 + 12.0)
        tg.box(xx - 0.25, y0 + 10.3, z0 + 11.4, xx + 0.25, y0 + 13.7, z0 + 11.9)
    tg.build()
    wb = MeshAcc("ELEC-MCC-WALL-BOARDS", "ENCL")
    for k in range(4):
        xx = x0 + 4 + k * 6
        wb.box(xx, y0 + 0.9, z0 + 1.8, xx + 3.5, y0 + 1.4, z0 + 6.4)
    wb.build()


def car(body, cab, wheels, cx, cy, rot=0.0, L=15.0, W=6.2, H=2.3, truck=False):
    """simple generic vehicle: lower body, glazed cabin, four wheels (no brand cues)."""
    body.boxc(cx, cy, GZ + 0.7, L, W, H * 0.55, rot)
    cl = L * (0.30 if not truck else 0.34)
    off = -L * (0.06 if not truck else 0.2)
    ox, oy = _rotz(cx + off, cy, cx, cy, rot)
    cab.boxc(ox, oy, GZ + 0.7 + H * 0.55, cl, W * 0.9, H * 0.5, rot)
    if truck:
        px, py = _rotz(cx - L * 0.28, cy, cx, cy, rot)
        body.boxc(px, py, GZ + 0.7 + H * 0.55, L * 0.42, W * 0.96, 0.35, rot)
    for dx in (-L * 0.32, L * 0.32):
        for dy in (-W * 0.5, W * 0.5):
            wx, wy = _rotz(cx + dx, cy + dy, cx, cy, rot)
            ax_, ay_ = _rotz(cx + dx, cy + dy + (0.25 if dy > 0 else -0.25), cx, cy, rot)
            bx_, by_ = _rotz(cx + dx, cy + dy - (0.25 if dy > 0 else -0.25), cx, cy, rot)
            wheels.cyl_between((ax_, ay_, GZ + 1.1), (bx_, by_, GZ + 1.1), 1.1, 14)


def detail_props():
    # ---- parking at the admin building, pickups at the gate and laydown --------------------------------------
    x0, y0 = P["admin_origin_ft"]
    L, W, H = P["admin_ft"]
    body = MeshAcc("SITE-VEHICLES-BODY", "ENCL")
    dark = MeshAcc("SITE-VEHICLES-BODY-DK", "STEEL")
    cab = MeshAcc("SITE-VEHICLES-CABINS", "GLASS")
    wh = MeshAcc("SITE-VEHICLES-WHEELS", "CABLE")
    ln = MeshAcc("SITE-PARKING-LINES", "CONC")
    for k in range(16):
        cx = x0 + 5 + k * 7.0
        ln.box(cx - 3.5, y0 - 37, 0.1, cx - 3.4, y0 - 20, 0.16)
        ln.box(cx - 3.5, y0 - 21.4, 0.1, cx - 3.0, y0 - 20.9, 0.3)
        if k not in (3, 7, 11):
            car(body if k % 3 else dark, cab, wh, cx, y0 - 29, math.radians(90), 15.0, 6.2, 4.6 if k % 4 == 0 else 4.0, truck=(k % 4 == 0))
    ln.box(x0 + 5 + 16 * 7.0 - 3.5, y0 - 37, 0.1, x0 + 5 + 16 * 7.0 - 3.4, y0 - 20, 0.16)
    car(dark, cab, wh, 205, 60, math.radians(90), 16.0, 6.4, 4.6, truck=True)
    lx, ly = P["laydown_origin_ft"]
    car(body, cab, wh, lx + 120, ly - 8, 0.0, 16.0, 6.4, 4.6, truck=True)
    body.build(); dark.build(); cab.build(); wh.build(); ln.build()
    # ---- laydown extras: tray rack, conduit stacks, light tower, skips, drums on flat ---------------------------------
    rk = MeshAcc("LAYDOWN-TRAY-RACK", "STEEL")
    tl = MeshAcc("LAYDOWN-TRAY-STOCK", "STEEL_DK")
    for xx in (lx + 112, lx + 120, lx + 128, lx + 136):
        for yy in (ly + 8, ly + 22):
            rk.box(xx - 0.15, yy - 0.15, GZ, xx + 0.15, yy + 0.15, GZ + 7.0)
    for zz in (GZ + 1.0, GZ + 3.2, GZ + 5.4):
        rk.box(lx + 111.8, ly + 7.8, zz, lx + 136.2, ly + 8.2, zz + 0.25).box(lx + 111.8, ly + 21.8, zz, lx + 136.2, ly + 22.2, zz + 0.25)
        for kk in range(4):
            tl.box(lx + 112.5 + kk * 6.0, ly + 8.3, zz + 0.25, lx + 117.5 + kk * 6.0, ly + 21.7, zz + 0.9)
    rk.build(); tl.build()
    cs = MeshAcc("LAYDOWN-CONDUIT-STACKS", "STEEL")
    for row in range(4):
        for col in range(5):
            cs.cyl_between((lx + 100, ly + 40 + col * 0.9 + (row % 2) * 0.45, GZ + 0.6 + row * 0.8), (lx + 124, ly + 40 + col * 0.9 + (row % 2) * 0.45, GZ + 0.6 + row * 0.8), 0.42, 8)
    for xx in (lx + 101, lx + 112, lx + 123):
        cs.box(xx, ly + 39.4, GZ, xx + 0.4, ly + 44.4, GZ + 0.35)
    cs.build()
    lt = MeshAcc("LAYDOWN-LIGHT-TOWER", "STEEL")
    lt.box(lx + 160, ly + 4, GZ + 0.5, lx + 168, ly + 8, GZ + 3.5)
    lt.cyl(lx + 164, ly + 6, GZ + 3.5, 0.3, 24, 8)
    lt.box(lx + 161.5, ly + 5.5, GZ + 27.4, lx + 166.5, ly + 6.5, GZ + 28.6)
    for wxx in (lx + 160.6, lx + 167.4):
        lt.cyl_between((wxx, ly + 4.2, GZ + 0.4), (wxx, ly + 4.6, GZ + 0.4), 0.5, 10)
    lt.build()
    sk = MeshAcc("LAYDOWN-SKIPS", "STEEL_DK")
    for k in range(2):
        sx_ = lx + 145 + k * 12
        sk.hexa([(sx_, ly + 90, GZ + 0.4), (sx_ + 9, ly + 90, GZ + 0.4), (sx_ + 9, ly + 96, GZ + 0.4), (sx_, ly + 96, GZ + 0.4),
                 (sx_ - 0.4, ly + 89.6, GZ + 4.2), (sx_ + 9.4, ly + 89.6, GZ + 4.2), (sx_ + 9.4, ly + 96.4, GZ + 4.2), (sx_ - 0.4, ly + 96.4, GZ + 4.2)])
    sk.build()


def detail_hrsg_transition(i):
    ax = GT_X[i]
    pre = "HRSG-%d-" % (i + 1)
    hw = HRSG_W / 2.0
    y0 = HRSG_Y0
    cas_h = 150.0
    tr = MeshAcc(pre + "TRANSITION-RIBS", "STEEL")
    for k in range(1, 10):
        f = k / 10.0
        y = y0 + 30 * f
        w = 11 + (hw - 11) * f
        zb = GZ + 4 + 4 * f
        zt = GZ + 26 + (cas_h - GZ - 26) * f
        for sg in (-1, 1):
            tr.box(ax + sg * w, y - 0.35, zb, ax + sg * (w + 0.5), y + 0.35, zt - 0.4)
    # front face (toward the hall): horizontal stiffeners and diagonal braces on the sloped panel
    def wf(f):
        return 11 + (hw - 11) * f
    for k in range(1, 12):
        f = k / 12.0
        y = y0 + 30 * f - 0.25
        z = GZ + 26 + (cas_h - GZ - 26) * f
        tr.box(ax - wf(f), y - 0.3, z - 0.3, ax + wf(f), y + 0.3, z + 0.3)
    for u in (-0.75, -0.4, 0.0, 0.4, 0.75):
        f0, f1 = 0.03, 0.97
        tr.seg((ax + u * wf(f0), y0 + 30 * f0 - 0.35, GZ + 26 + (cas_h - GZ - 26) * f0), (ax + u * wf(f1), y0 + 30 * f1 - 0.35, GZ + 26 + (cas_h - GZ - 26) * f1), 0.28, 4)
    tr.build()


def detail_anchors():
    ax = GT_X[1]
    hw = HRSG_W / 2.0
    y0 = HRSG_Y0
    anchor("HRSG-2-PLATFORMS", ax + hw + 5, y0 + 120, 101.0, "Access platforms with handrails and caged ladders", 6)
    anchor("HRSG-2-DRUM-SILENCERS", ax + 10, y0 + 85, 176.0, "Drum safety valves and silencers under the open roof frame", 6)
    anchor("HRSG-2-ROOF-FRAME", ax - hw - 2.5, y0 + 90, HRSG_H + 1.0, "Open roof frame with perimeter grating and rail", 6)
    cx0, cy0 = P["bess_origin_ft"][0] + 10, P["bess_origin_ft"][1] + 10
    anchor("BESS-DOOR", cx0 + 40.2, cy0 + 4, GZ + 6.2, "Container end doors with locking bars", 2)
    anchor("BESS-TX-FINS", cx0 + 31.8, cy0 + 8 + 6 + 5, GZ + 6.0, "Transformer cooling fins", 2)
    lx, ly = P["laydown_origin_ft"]
    anchor("LAYDOWN-TRAY-RACK", lx + 124, ly + 15, GZ + 8.5, "Cable-tray stock on racking", 3)
    anchor("CORR-MARKER", 1230, CORR_Y + 16, GZ + 3.2, "Duct-bank route marker post", 16)
    anchor("CCS-ABSORBER-PLATFORMS", P["ccs_origin_ft"][0] + 10 + P["absorber_ft"][0] + 6, P["ccs_origin_ft"][1] + 140, GZ + 122.0, "Absorber platforms and ladders", 14)
    anchor("WATER-T1-STAIR", P["water_origin_ft"][0] + P["water_treatment_ft"][0] + 40 + 24, P["water_origin_ft"][1] + P["pond_ft"][1] + 40 + 25, GZ + 20.0, "Tank spiral stair", 13)

def build_detail():
    """detail pass: run after every package exists so site furniture can avoid the equipment."""
    detail_hall()
    for i in range(P["counts"]["GT"]):
        detail_gt(i)
    detail_st()
    for i in range(P["counts"]["HRSG"]):
        detail_hrsg(i)
    for i in range(P["counts"]["GT"]):
        detail_inlet(i)
    for i in range(P["counts"]["GSU"]):
        detail_gsu(i)
    detail_switchyard()
    detail_buildings()
    detail_interiors()
    detail_bess()
    detail_modular()
    detail_laydown()
    detail_acc()
    detail_cooling()
    detail_gas()
    detail_corridor()
    detail_site()
    detail_props()
    for i in range(P["counts"]["HRSG"]):
        detail_hrsg_transition(i)
    detail_anchors()

# =============================================================================
# MAIN
# =============================================================================
def build_all():
    build_site()
    build_hall()
    for i in range(P["counts"]["GT"]):
        build_gt(i)
    build_st()
    build_steam_headers()
    for i in range(P["counts"]["HRSG"]):
        build_hrsg(i)
    for i in range(P["counts"]["GT"]):
        build_inlet(i)
    for i in range(P["counts"]["GSU"]):
        build_gsu(i)
    build_gentie()
    build_switchyard()
    build_ehouse()
    build_mcc()
    build_admin()
    build_bess()
    build_laydown()
    build_modular()
    build_acc()
    build_chillers()
    build_water()
    build_ccs()
    build_gasmet()
    build_fuelgas()
    build_corridor()
    build_detail()


def _overlap(a, b, tol=0.5):
    """2-D footprint overlap; accepts 4-tuples (x0,y0,x1,y1) or 6-tuple bboxes."""
    ax0, ay0, ax1, ay1 = (a[0], a[1], a[2], a[3]) if len(a) == 4 else (a[0], a[1], a[3], a[4])
    bx0, by0, bx1, by1 = (b[0], b[1], b[2], b[3]) if len(b) == 4 else (b[0], b[1], b[3], b[4])
    return not (ax1 <= bx0 + tol or bx1 <= ax0 + tol or ay1 <= by0 + tol or by1 <= ay0 + tol)


def preflight(views_path=None):
    rep = dict(objects=len(REG), anchors=len(ANCHORS), packages={}, problems=[])
    for r in REG:
        rep["packages"][r["pkg"]] = rep["packages"].get(r["pkg"], 0) + 1
    # nothing hovers: every above-grade object should touch grade (or sit on a pad / another object of its package)
    for r in REG:
        if r["kind"] != "mesh" or r["below_grade"]:
            continue
        if r["bbox"][2] < -1.5 and not r["name"].startswith(("SITE-", "WATER-POND", "ADMIN-CABLE", "SWYD-PAD")):
            rep["problems"].append("below-grade geometry not flagged: %s (zmin %.1f)" % (r["name"], r["bbox"][2]))
    # zone footprint overlaps
    zl = list(ZONES.items())
    for i in range(len(zl)):
        for j in range(i + 1, len(zl)):
            a, b = zl[i][1][1], zl[j][1][1]
            if _overlap(a, b, 0.0):
                rep["problems"].append("zone footprints overlap: %d and %d" % (zl[i][0], zl[j][0]))
    # solid-body collisions between packages (3-D bbox overlap of compact objects only;
    # linear items such as trays, pipes, ducts, cables, steel and walls are excluded)
    skip_words = ("TRAY", "PIPE", "DUCT", "SUPPORT", "HEADER", "CABLE", "FENCE", "PAD", "GROUND", "STEEL", "JUMPER",
                  "BUS", "LATERAL", "CONDUIT", "PLATFORM", "STAIR", "TOWER", "GANTRY", "COLUMNS", "TRUSS", "RAIL",
                  "CRANE", "BRACKET", "RISER", "CONNECTOR", "CAP", "WALL", "ROOF", "FLOOR", "SLAB", "PIPING", "LEADS",
                  "IPB", "FEEDER", "WIRE", "BRIDGE", "BRANCH", "TIE-IN", "PIPELINE", "RUNS", "EXHAUST", "TRANSITION",
                  "BERM", "LINER", "POND", "CURB", "CONTAINMENT", "FIREWALL", "GLAZING", "CANOPY", "PARKING", "HOODS",
                  "INSULATOR", "ARRESTER", "SEALING", "TERMINATION", "COVER", "MANHOLE", "DEADEND", "MAST", "FLANGE", "GRID",
                  "RIB", "LADDER", "RAIL", "LOUVRE", "DOOR", "LIGHT", "POLE", "BOLLARD", "DETAIL", "PLATFORM", "STIFF", "MARKER",
                  "LABEL", "TIES", "SHED", "FINS", "CURB", "APRON", "PLINTH", "SKID", "TRENCH", "STRING", "CLAMP", "HYDRANT",
                  "CATCH", "OUTRIGGER", "GATE", "BARRIER", "PALLET", "BARRIERS", "CANOPY", "ROLLERS", "WINDINGS", "SPOKES", "MULLION",
                  "PARAPET", "STAIR", "TANK-DETAIL", "COLUMN", "WALKWAY", "BRACKET", "VALVE", "SILENCER", "PILING", "GRATING",
                  "TELEHANDLER", "WORKBENCH", "FRAME", "BELLOWS", "PLATES", "LUGS", "INSTRUMENTS", "ENTRANCE", "FINS")
    solids = [r for r in REG if r["kind"] == "mesh" and not r["below_grade"] and r["pkg"] not in ("SITE", "ANCHOR")
              and not any(w in r["name"] for w in skip_words)]
    def fam(n):
        return n.split("-")[0]
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            a, b = solids[i], solids[j]
            if fam(a["pkg"]) == fam(b["pkg"]):
                continue
            ba, bb = a["bbox"], b["bbox"]
            if _overlap(ba, bb, 0.5) and ba[5] > bb[2] + 0.5 and bb[5] > ba[2] + 0.5:
                rep["problems"].append("solids collide: %s x %s" % (a["name"], b["name"]))
    # anchors referenced by views.json must exist
    if views_path and os.path.exists(views_path):
        with open(views_path) as f:
            views = json.load(f)
        names = {a["name"] for a in ANCHORS}
        for v in views.get("views", []):
            for c in v.get("callouts", []):
                if c["anchor"] not in names:
                    rep["problems"].append("view %s references missing anchor %s" % (v["id"], c["anchor"]))
    return rep


def main():
    if HAVE_BPY:
        # clean default scene
        for ob in list(bpy.data.objects):
            bpy.data.objects.remove(ob, do_unlink=True)
        for col in list(bpy.data.collections):
            bpy.data.collections.remove(col)
        scene = bpy.context.scene
        scene.unit_settings.system = "METRIC"
        scene.unit_settings.length_unit = "METERS"
    build_all()
    here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    views_path = os.path.join(here, "views.json")
    rep = preflight(views_path)
    rep["params"] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in P.items()}
    rep["anchors_list"] = [dict(name=a["name"], label=a["label"], zone=a["zone"], pos=list(a["pos"])) for a in ANCHORS]
    rep["zones"] = {str(k): dict(label=v[0], rect=list(v[1])) for k, v in ZONES.items()}
    out_dir = os.path.dirname(os.path.abspath(OUT_BLEND)) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "preflight.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("PREFLIGHT: %d objects, %d anchors, %d packages" % (rep["objects"], rep["anchors"], len(rep["packages"])))
    for pr in rep["problems"]:
        print("  ! " + pr)
    if not rep["problems"]:
        print("  no problems found")
    if HAVE_BPY:
        # store site metadata on the scene for render_views.py
        scene = bpy.context.scene
        scene["plant_true_scale"] = FT
        scene["plant_site_ft"] = list(P["site_ft"])
        scene["plant_backdrop"] = C["BACKDROP"]
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT_BLEND))
        print("saved", os.path.abspath(OUT_BLEND))
    else:
        print("dry run: no .blend written (bpy not available)")


if __name__ == "__main__":
    main()
