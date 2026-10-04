"""Studio environment: floor shadow catcher, soft lighting rig, render settings."""
import math
import bpy
from mathutils import Vector
from swlib import coll, M, hex_rgba

RES_X, RES_Y = 2400, 1664          # 7.5 x 5.2 in at 320 dpi (main render panel)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = "METRIC"
    s.unit_settings.scale_length = 1.0
    s.unit_settings.length_unit = "METERS"


def world():
    s = bpy.context.scene
    w = bpy.data.worlds.new("Studio_World")
    s.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hex_rgba("#F2F3F4")
    bg.inputs["Strength"].default_value = 0.55


def floor():
    c = coll("Lighting")
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0))
    f = bpy.context.active_object
    f.name = "Studio_Floor_ShadowCatcher"
    for cc in list(f.users_collection):
        cc.objects.unlink(f)
    c.objects.link(f)
    f.data.materials.append(M("Floor_Pad"))
    f.is_shadow_catcher = True
    return f


def light_rig(name, target, radius=7.0, energy=1.0, collection="Lighting"):
    """Three soft area lights aimed at `target` (a zone centre). Lights are
    parented to an empty so the rig can be moved per view."""
    c = coll(collection)
    root = bpy.data.objects.new(name + "_Rig", None)
    root.location = target
    c.objects.link(root)
    spec = [  # (azimuth deg, elevation deg, size, power W, colour temp tint)
        ("Key", -35, 48, 4.0, 1400 * energy, (1.0, 0.985, 0.965)),
        ("Fill", 70, 30, 5.0, 520 * energy, (0.965, 0.98, 1.0)),
        ("Top", 160, 78, 6.0, 700 * energy, (1.0, 1.0, 1.0)),
        ("Rim", 150, 28, 3.0, 380 * energy, (1.0, 1.0, 1.0)),
    ]
    for nm, az, el, size, pw, col in spec:
        ld = bpy.data.lights.new(f"{name}_{nm}", "AREA")
        ld.shape = "DISK"
        ld.size = size
        ld.energy = pw
        ld.color = col
        ob = bpy.data.objects.new(f"{name}_{nm}", ld)
        a, e = math.radians(az), math.radians(el)
        # azimuth measured from -Y (front) towards +X
        local = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * radius
        ob.location = local
        ob.rotation_euler = (-local).to_track_quat("-Z", "Y").to_euler()
        ob.parent = root
        c.objects.link(ob)
    return root


def render_settings(samples=128):
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = samples
    s.cycles.use_adaptive_sampling = True
    s.cycles.adaptive_threshold = 0.02
    s.cycles.use_denoising = True
    try:
        s.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    s.cycles.max_bounces = 8
    s.cycles.diffuse_bounces = 3
    s.cycles.glossy_bounces = 3
    s.cycles.transparent_max_bounces = 8
    s.render.film_transparent = True
    s.render.resolution_x = RES_X
    s.render.resolution_y = RES_Y
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = "PNG"
    s.render.image_settings.color_mode = "RGBA"
    s.render.image_settings.color_depth = "8"
    try:
        s.view_settings.view_transform = "AgX"
        s.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        s.view_settings.view_transform = "Standard"
    s.view_settings.exposure = -0.25
    s.render.use_persistent_data = True
    s.render.threads_mode = "AUTO"
