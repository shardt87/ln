"""
CCGT cable showcase generator for Blender (tested on Blender 5.0).

Builds stepped / stripped-back cable models for every cable application in a
combined-cycle gas turbine plant, with materials, labels, lights, a camera and
a "strip" animation (each cable starts flush and its layers slide out).

Usage:
    Blender > Scripting tab > Open this file > Run Script
    or: blender --background --python ccgt_cable_showcase.py

Edit the SETTINGS block below. Cable geometry lives in CABLES; dimensions are
approximate catalogue values in millimetres (radii, not diameters).
"""

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- SETTINGS --
BUILD = "all"            # "all" or a list of keys, e.g. ["hv_export"] for a hero shot
SCALE_MODE = "normalized"  # "normalized": every cable same display diameter; "true": real size
DISPLAY_DIAMETER = 1.0   # Blender units, used when SCALE_MODE == "normalized"
TRUE_SCALE = 0.01        # Blender units per mm, used when SCALE_MODE == "true"
BASE_LENGTH = 2.0        # length of the outer sheath (Blender units)
STEP = 0.32              # how much further each inner layer sticks out
COLUMNS = 2              # grid layout when building several cables
ROW_SPACING = 1.8
LABEL_SIZE = 0.2
ANIMATE = True
ANIM_START, ANIM_LENGTH, ANIM_STAGGER = 1, 48, 6
CLEAR_SCENE = True

# --------------------------------------------------------------- MATERIALS --
# name: (base colour RGB, metallic, roughness)
MATERIALS = {
    "copper":      ((0.95, 0.45, 0.25), 1.0, 0.28),
    "tinned_cu":   ((0.80, 0.80, 0.82), 1.0, 0.35),
    "aluminium":   ((0.85, 0.86, 0.88), 1.0, 0.30),
    "steel":       ((0.62, 0.63, 0.66), 1.0, 0.38),
    "lead":        ((0.42, 0.43, 0.47), 1.0, 0.55),
    "semicon":     ((0.02, 0.02, 0.02), 0.0, 0.65),
    "xlpe":        ((0.88, 0.87, 0.80), 0.0, 0.35),
    "epr":         ((0.70, 0.30, 0.15), 0.0, 0.50),
    "mica":        ((0.75, 0.60, 0.30), 0.3, 0.45),
    "swell_tape":  ((0.85, 0.85, 0.85), 0.0, 0.80),
    "bedding":     ((0.30, 0.30, 0.30), 0.0, 0.70),
    "frp":         ((0.85, 0.78, 0.40), 0.0, 0.40),
    "glass":       ((0.80, 0.90, 1.00), 0.0, 0.10),
    "silicone":    ((0.85, 0.85, 0.85), 0.0, 0.45),
    "sheath_black": ((0.025, 0.025, 0.025), 0.0, 0.45),
    "sheath_red":  ((0.55, 0.03, 0.03), 0.0, 0.45),
    "sheath_orange": ((0.85, 0.30, 0.02), 0.0, 0.45),
    "sheath_blue": ((0.10, 0.35, 0.75), 0.0, 0.45),
    "sheath_green": ((0.05, 0.35, 0.12), 0.0, 0.45),
    "ins_brown":   ((0.25, 0.12, 0.05), 0.0, 0.40),
    "ins_black":   ((0.03, 0.03, 0.03), 0.0, 0.40),
    "ins_grey":    ((0.45, 0.45, 0.45), 0.0, 0.40),
    "ins_blue":    ((0.05, 0.20, 0.70), 0.0, 0.40),
    "ins_white":   ((0.85, 0.85, 0.85), 0.0, 0.40),
    "ins_red":     ((0.70, 0.05, 0.05), 0.0, 0.40),
    "ins_green":   ((0.05, 0.50, 0.15), 0.0, 0.40),
    "ins_yellow":  ((0.85, 0.70, 0.05), 0.0, 0.40),
    "ins_gy":      ((0.30, 0.60, 0.10), 0.0, 0.40),  # green/yellow earth
    "ins_orange":  ((0.90, 0.40, 0.05), 0.0, 0.40),
    "ins_violet":  ((0.40, 0.10, 0.60), 0.0, 0.40),
    "label":       ((0.90, 0.90, 0.90), 0.0, 0.50),
    "backdrop":    ((0.05, 0.055, 0.06), 0.0, 0.80),
}


# ------------------------------------------------------------ LAYER HELPERS --
def conductor(r, rings=3, mat="copper"):
    """Stranded conductor. rings=0 gives a solid conductor."""
    return {"type": "conductor", "r": r, "rings": rings, "mat": mat}


def tube(r, mat):
    """Concentric extruded / taped layer with outer radius r."""
    return {"type": "tube", "r": r, "mat": mat}


def wires(ring_r, wire_r, mat, fill=1.0):
    """Ring of round wires (armour, copper wire screen). fill<1 spaces them out."""
    return {"type": "wires", "r": ring_r, "wr": wire_r, "mat": mat, "fill": fill}


def cores(*rings):
    """Group of sub-cables. Each ring: ring(n, pitch, core_layers, colors, phase_deg)."""
    return {"type": "cores", "rings": rings}


def ring(n, pitch, core_layers, colors=None, phase=0.0):
    return {"n": n, "pitch": pitch, "core": core_layers, "colors": colors, "phase": phase}


def outer_radius(layers):
    layer = layers[-1]
    if layer["type"] == "wires":
        return layer["r"] + layer["wr"]
    if layer["type"] == "cores":
        return max(rg["pitch"] + outer_radius(rg["core"]) for rg in layer["rings"])
    return layer["r"]


# ------------------------------------------------------------------ CABLES --
# Each entry: title, application text (plant zone), layers from inside out.
CABLES = {
    "hv_export": {
        "title": "HV export cable  220-400 kV",
        "app": "GSU transformer to switchyard / grid",
        "layers": [
            conductor(30, rings=5),
            tube(32, "semicon"),           # conductor screen
            tube(59, "xlpe"),              # main insulation
            tube(61, "semicon"),           # insulation screen
            tube(62.5, "swell_tape"),      # water-blocking tape
            wires(63.4, 0.9, "copper", fill=0.55),  # copper wire screen
            tube(66.5, "lead"),            # metallic sheath
            tube(72, "sheath_black"),      # HDPE oversheath
        ],
    },
    "mv_3core": {
        "title": "MV power cable  6.6-33 kV, 3-core armoured",
        "app": "Aux transformer, MV switchgear, BFP / CW pump motors",
        "layers": [
            cores(ring(3, 22.3, [
                conductor(9.3, rings=3),
                tube(10.0, "semicon"),
                tube(18.0, "xlpe"),
                tube(19.0, "semicon"),
                tube(19.3, "copper"),      # copper tape screen
            ], phase=90)),
            tube(42.5, "bedding"),
            wires(44.5, 2.0, "steel"),     # SWA
            tube(50, "sheath_red"),
        ],
    },
    "lv_power": {
        "title": "LV power cable  0.6/1 kV, 4-core SWA",
        "app": "MCCs, LV motors, lighting & small power",
        "layers": [
            cores(ring(4, 9.9, [conductor(5.8, rings=2), tube(7.0, "xlpe")],
                       colors=["ins_brown", "ins_black", "ins_grey", "ins_blue"], phase=45)),
            tube(17.5, "bedding"),
            wires(18.8, 1.25, "steel"),
            tube(22, "sheath_black"),
        ],
    },
    "vfd": {
        "title": "VFD motor cable  symmetrical, screened",
        "app": "Variable-speed pumps, ACC & HRSG fans",
        "layers": [
            cores(
                ring(3, 6.35, [conductor(4.4, rings=2), tube(5.5, "xlpe")],
                     colors=["ins_brown", "ins_black", "ins_grey"], phase=90),
                ring(3, 8.5, [conductor(1.7, rings=1), tube(2.0, "ins_gy")], phase=150),
            ),
            tube(11.0, "bedding"),
            tube(11.5, "tinned_cu"),       # overall copper braid / tape screen
            tube(13.0, "sheath_black"),
        ],
    },
    "control": {
        "title": "Control cable  12-core, screened",
        "app": "Switchgear interlocks, valve actuators, MCC control",
        "layers": [
            cores(
                ring(3, 1.6, [conductor(0.7, rings=1), tube(1.35, "ins_black")]),
                ring(9, 4.3, [conductor(0.7, rings=1), tube(1.35, "ins_black")], phase=20),
            ),
            tube(6.2, "bedding"),
            tube(6.5, "tinned_cu"),
            tube(8.0, "sheath_black"),
        ],
    },
    "instrumentation": {
        "title": "Instrumentation cable  4-pair, IS + OS",
        "app": "4-20 mA transmitters, DCS I/O, analysers",
        "layers": [
            cores(ring(4, 3.05, [
                cores(ring(2, 0.95, [conductor(0.45, rings=1), tube(0.9, "ins_white")],
                           colors=["ins_white", "ins_black"])),
                tube(2.1, "aluminium"),     # individual foil screen
            ], phase=45)),
            tube(5.3, "aluminium"),          # overall foil screen
            tube(6.6, "sheath_blue"),        # intrinsically safe = light blue
        ],
    },
    "thermocouple": {
        "title": "High-temp thermocouple extension",
        "app": "Gas turbine exhaust, HRSG & steam temperatures",
        "layers": [
            cores(ring(2, 1.25, [conductor(0.6, rings=0, mat="tinned_cu"), tube(1.2, "silicone")],
                       colors=["ins_green", "ins_white"])),
            tube(2.9, "glass"),              # glass-fibre wrap
            tube(3.3, "steel"),              # stainless braid
            tube(4.0, "sheath_green"),
        ],
    },
    "fire_resistant": {
        "title": "Fire-resistant cable  LSZH, mica taped",
        "app": "Fuel-gas ESD, fire & gas detection, emergency lighting",
        "layers": [
            cores(ring(3, 2.7, [conductor(1.4, rings=1), tube(1.65, "mica"), tube(2.3, "xlpe")],
                       colors=None, phase=90)),
            tube(5.2, "bedding"),
            tube(6.4, "sheath_red"),
        ],
    },
    "fibre": {
        "title": "Fibre-optic cable  armoured loose-tube",
        "app": "DCS network, protection signalling, CCTV",
        "layers": [
            cores(
                ring(1, 0.0, [tube(1.2, "frp")]),
                ring(6, 2.45, [
                    cores(ring(4, 0.45, [tube(0.18, "glass")])),
                    tube(1.2, "ins_blue"),
                ], colors=["ins_blue", "ins_orange", "ins_green", "ins_brown", "ins_grey", "ins_white"]),
            ),
            tube(3.9, "swell_tape"),
            tube(4.2, "steel"),              # corrugated steel tape
            tube(5.5, "sheath_black"),
        ],
    },
    "dc": {
        "title": "DC / excitation cable  flexible single-core",
        "app": "Battery & UPS, generator excitation, DC lube-oil pumps",
        "layers": [
            conductor(6.0, rings=6, mat="tinned_cu"),
            tube(7.6, "epr"),
            tube(9.0, "sheath_black"),
        ],
    },
    "earthing": {
        "title": "Earthing conductor  bare stranded copper",
        "app": "Earth grid, equipment bonding, lightning protection",
        "layers": [
            conductor(6.0, rings=2),
        ],
    },
}


# ---------------------------------------------------------------- BUILDERS --
def get_material(name):
    mat = bpy.data.materials.get("cable_" + name)
    if mat:
        return mat
    color, metallic, rough = MATERIALS[name]
    mat = bpy.data.materials.new("cable_" + name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if name == "glass":
        bsdf.inputs["Transmission Weight"].default_value = 0.8
    mat.diffuse_color = (*color, 1.0)  # viewport solid-mode colour
    return mat


def add_cylinder(bm, radius, length, cy, cz, segments):
    """Cylinder along +X from x=0 to x=length, centred on (cy, cz)."""
    mat = Matrix.Translation((length / 2, cy, cz)) @ Matrix.Rotation(math.pi / 2, 4, "Y")
    geom = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                                 radius1=radius, radius2=radius, depth=length, matrix=mat)
    for v in geom["verts"]:
        for f in v.link_faces:
            is_cap = abs(f.normal.x) > 0.9
            f.smooth = not is_cap


def make_object(name, bm, material, parent, collection):
    bm.normal_update()
    for e in bm.edges:  # keep the cap rims crisp
        if len(e.link_faces) == 2 and e.link_faces[0].smooth != e.link_faces[1].smooth:
            e.smooth = False
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(get_material(material))
    obj.parent = parent
    collection.objects.link(obj)
    return obj


def segments_for(radius_bu):
    return max(12, min(96, int(radius_bu * 220)))


def build_layers(layers, length, s, cy, cz, parent, coll, prefix, color=None, out=None):
    """Build layers (inside -> out). Inner layers get longer by STEP each.
    `color` overrides the material of the outermost non-metal layer (core colours).
    Returns list of (object, full_length) for animation."""
    out = [] if out is None else out
    n = len(layers)
    for i, layer in enumerate(layers):
        L = length + (n - 1 - i) * STEP
        name = f"{prefix}_{i}_{layer['type']}"
        if layer["type"] == "cores":
            for ri, rg in enumerate(layer["rings"]):
                for k in range(rg["n"]):
                    a = math.radians(rg["phase"]) + 2 * math.pi * k / rg["n"]
                    py = cy + rg["pitch"] * s * math.cos(a)
                    pz = cz + rg["pitch"] * s * math.sin(a)
                    col = rg["colors"][k % len(rg["colors"])] if rg["colors"] else None
                    build_layers(rg["core"], L, s, py, pz, parent, coll,
                                 f"{prefix}_r{ri}c{k}", color=col, out=out)
            continue

        bm = bmesh.new()
        mat = layer["mat"]
        if layer["type"] == "tube":
            r = layer["r"] * s
            add_cylinder(bm, r, L, cy, cz, segments_for(r))
            if color and i == n - 1:
                mat = color
        elif layer["type"] == "conductor":
            R = layer["r"] * s
            k = layer["rings"]
            if k == 0:
                add_cylinder(bm, R, L, cy, cz, segments_for(R))
            else:
                sr = R / (2 * k + 1)
                add_cylinder(bm, sr, L, cy, cz, 12)
                for j in range(1, k + 1):
                    for m in range(6 * j):
                        a = 2 * math.pi * m / (6 * j) + j * 0.3
                        add_cylinder(bm, sr * 0.98, L, cy + 2 * j * sr * math.cos(a),
                                     cz + 2 * j * sr * math.sin(a), 12)
        elif layer["type"] == "wires":
            rr, wr = layer["r"] * s, layer["wr"] * s
            count = max(6, int(layer["fill"] * 2 * math.pi * rr / (2 * wr * 1.04)))
            for m in range(count):
                a = 2 * math.pi * m / count
                add_cylinder(bm, wr, L, cy + rr * math.cos(a), cz + rr * math.sin(a), 10)
        obj = make_object(name, bm, mat, parent, coll)
        out.append((obj, L))
    return out


def add_label(text, location, parent, coll):
    curve = bpy.data.curves.new("label", "FONT")
    curve.body = text
    curve.size = LABEL_SIZE
    curve.align_x = "RIGHT"
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new("label", curve)
    obj.location = location
    obj.rotation_euler = (math.pi / 2, 0, 0)  # stand up, facing -Y (camera)
    obj.data.materials.append(get_material("label"))
    obj.parent = parent
    coll.objects.link(obj)
    return obj


def build_cable(key, origin, coll):
    spec = CABLES[key]
    r_out = outer_radius(spec["layers"])
    s = DISPLAY_DIAMETER / (2 * r_out) if SCALE_MODE == "normalized" else TRUE_SCALE
    root = bpy.data.objects.new(f"CABLE_{key}", None)
    root.empty_display_type = "ARROWS"
    root.empty_display_size = 0.3
    root.location = origin
    coll.objects.link(root)
    parts = build_layers(spec["layers"], BASE_LENGTH, s, 0.0, 0.0, root, coll, key)
    add_label(f"{spec['title']}\n{spec['app']}", (-0.35, 0, 0), root, coll)
    total = max(L for _, L in parts)
    return root, parts, total


def animate_strip(parts, start):
    """Layers start flush with the oversheath, then slide out to the stepped state."""
    for obj, L in parts:
        obj.scale.x = BASE_LENGTH / L
        obj.keyframe_insert("scale", index=0, frame=start)
        obj.scale.x = 1.0
        obj.keyframe_insert("scale", index=0, frame=start + ANIM_LENGTH)


def setup_scene(bounds, single):
    scene = bpy.context.scene
    (xmin, xmax), (zmin, zmax) = bounds
    cx, cz = (xmin + xmax) / 2, (zmin + zmax) / 2
    width, height = xmax - xmin, zmax - zmin

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.01, 0.012, 0.015, 1)

    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, 3.0, cz), rotation=(math.pi / 2, 0, 0))
    backdrop = bpy.context.object
    backdrop.name = "backdrop"
    backdrop.scale = (width * 3 + 20, height * 3 + 20, 1)
    backdrop.data.materials.append(get_material("backdrop"))

    def area(name, loc, energy, size, color=(1, 1, 1)):
        data = bpy.data.lights.new(name, "AREA")
        data.energy, data.size, data.color = energy, size, color
        obj = bpy.data.objects.new(name, data)
        obj.location = loc
        bpy.context.collection.objects.link(obj)
        direction = Vector((cx, 0, cz)) - Vector(loc)
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    scale = max(width, height)
    area("key", (cx + scale * 0.6, -scale * 0.9, cz + scale * 0.7), 45 * scale ** 2, scale)
    area("fill", (cx - scale * 0.8, -scale * 0.6, cz - scale * 0.2), 10 * scale ** 2, scale, (0.8, 0.9, 1))
    area("rim", (cx, 2.5, cz + scale * 0.8), 30 * scale ** 2, scale * 0.5)

    cam_data = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    if single:  # hero 3/4 view onto the stripped end
        cam_data.lens = 60
        target = Vector((xmax - 1.0, 0, 0))
        cam.location = target + Vector((2.6, -4.2, 1.6))
    else:       # catalogue wall, orthographic front view
        cam_data.type = "ORTHO"
        cam_data.ortho_scale = max(width * 1.12, height * 1.12 * 16 / 9)
        target = Vector((cx, 0, cz))
        cam.location = (cx, -20, cz)
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()

    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.frame_start = ANIM_START
    scene.frame_end = ANIM_START + ANIM_LENGTH + ANIM_STAGGER * 12 + 24


def main():
    if CLEAR_SCENE:
        bpy.ops.wm.read_factory_settings(use_empty=True)
    keys = list(CABLES) if BUILD == "all" else list(BUILD)
    coll = bpy.data.collections.new("CCGT_cables")
    bpy.context.scene.collection.children.link(coll)

    label_room = 0.0 if len(keys) == 1 else 5.2
    max_len = max(BASE_LENGTH + 2.5, 0)
    col_width = label_room + max_len + 1.2 + 1.5
    xs, zs = [], []
    for idx, key in enumerate(keys):
        col, row = idx % COLUMNS, idx // COLUMNS
        origin = (col * col_width, 0.0, -row * ROW_SPACING)
        root, parts, total = build_cable(key, origin, coll)
        if ANIMATE:
            animate_strip(parts, ANIM_START + idx * ANIM_STAGGER)
        xs += [origin[0] - label_room, origin[0] + total]
        zs += [origin[2] - 0.6, origin[2] + 0.6]

    setup_scene(((min(xs), max(xs)), (min(zs), max(zs))), single=len(keys) == 1)
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)


main()
