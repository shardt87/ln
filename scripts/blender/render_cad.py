# render_cad.py — headless Blender technical/CAD-style renders for glTF/GLB models.
#
# Companion to render_glb.py (beauty renders). This script produces engineering
# drawing looks instead: orthographic projections with Freestyle edge extraction,
# in three styles:
#
#   shaded     — original materials under flat, even lighting with black feature
#                edges drawn on top (CAD viewport / "shaded with edges" look)
#   hiddenline — white shadeless model, black silhouette/crease/border lines on a
#                white sheet (classic hidden-line-removed technical drawing)
#   blueprint  — deep blueprint-blue sheet with white linework
#
# View presets follow drafting convention: iso (true isometric), plan (top),
# front/back/left/right elevations, or any custom azimuth/elevation.
#
# NOTE: Freestyle's occlusion solver can need many GB of RAM on dense models
# viewed edge-on (elevations sight through every stacked object). If a render
# is OOM-killed, use --no-lines for that view, or the shaded style without
# lines — the flat orthographic projection still reads as a CAD elevation.
#
# Usage:
#   python scripts/blender/render_cad.py --input model.glb --output out/cad.png \
#       --style hiddenline --view iso
#   python scripts/blender/render_cad.py --input model.glb --output out/cad.png \
#       --style shaded --view plan,front,right,iso        # one file per view

import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

VIEW_PRESETS = {
    # name: (azimuth, elevation) in degrees
    "iso": (45.0, 35.264),       # true isometric
    "dimetric": (45.0, 20.0),
    "plan": (0.0, 89.9),         # top view (89.9 keeps the up-vector stable)
    "front": (0.0, 0.0),
    "back": (180.0, 0.0),
    "right": (90.0, 0.0),
    "left": (270.0, 0.0),
}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    p = argparse.ArgumentParser(description="Headless Blender CAD-style renders")
    p.add_argument("--input", required=True, help="path to .glb/.gltf/.obj/.stl/.fbx/.ply")
    p.add_argument("--output", default="cad.png", help="output image path (PNG)")
    p.add_argument("--style", choices=["shaded", "hiddenline", "blueprint"], default="hiddenline")
    p.add_argument("--view", default="iso",
                   help="comma-separated view presets (%s) or az:el pairs like 30:25"
                        % ",".join(VIEW_PRESETS))
    p.add_argument("--width", type=int, default=2400)
    p.add_argument("--height", type=int, default=1700)
    p.add_argument("--samples", type=int, default=32)
    p.add_argument("--perspective", action="store_true",
                   help="perspective camera instead of orthographic")
    p.add_argument("--fov", type=float, default=35.0, help="FOV for --perspective")
    p.add_argument("--margin", type=float, default=1.05, help="framing margin (>1 zooms out)")
    p.add_argument("--line-width", type=float, default=1.4, help="Freestyle line thickness (px)")
    p.add_argument("--no-lines", action="store_true", help="disable Freestyle edge extraction")
    p.add_argument("--crease-angle", type=float, default=134.0,
                   help="crease edge threshold in degrees")
    return p.parse_args(argv)


def import_model(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=path)
    elif ext == ".stl":
        bpy.ops.wm.stl_import(filepath=path)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == ".ply":
        bpy.ops.wm.ply_import(filepath=path)
    else:
        raise ValueError(f"unsupported model format: {ext}")
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def scene_bounds(objects):
    lo = Vector((1e18, 1e18, 1e18))
    hi = Vector((-1e18, -1e18, -1e18))
    for obj in objects:
        for corner in obj.bound_box:
            w = obj.matrix_world @ Vector(corner)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    return lo, hi


def flat_material(name, color, emission=True):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    if emission:
        # Shadeless: the surface emits its own color, so the drawing has no
        # shading gradients at all — pure hidden-line style.
        sh = nodes.new("ShaderNodeEmission")
        sh.inputs["Color"].default_value = (*color, 1.0)
        sh.inputs["Strength"].default_value = 1.0
        links.new(sh.outputs["Emission"], out.inputs["Surface"])
    else:
        sh = nodes.new("ShaderNodeBsdfDiffuse")
        sh.inputs["Color"].default_value = (*color, 1.0)
        links.new(sh.outputs["BSDF"], out.inputs["Surface"])
    return mat


def flat_world(color, strength=1.0):
    world = bpy.data.worlds.new("SheetWorld")
    bpy.context.scene.world = world
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    bg = nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (*color, 1.0)
    bg.inputs["Strength"].default_value = strength
    out = nodes.new("ShaderNodeOutputWorld")
    links.new(bg.outputs["Background"], out.inputs["Surface"])


def override_materials(meshes, mat):
    for obj in meshes:
        obj.data.materials.clear()
        obj.data.materials.append(mat)


def apply_style(style, meshes):
    """Returns the Freestyle line color for the style."""
    if style == "hiddenline":
        flat_world((1.0, 1.0, 1.0))
        override_materials(meshes, flat_material("HiddenLineWhite", (1.0, 1.0, 1.0)))
        return (0.0, 0.0, 0.0)
    if style == "blueprint":
        blue = (0.012, 0.077, 0.23)  # classic blueprint ground
        flat_world(blue)
        override_materials(meshes, flat_material("BlueprintFill", (0.02, 0.11, 0.31)))
        return (0.92, 0.96, 1.0)
    # shaded: keep the model's own materials, light them evenly from all sides
    # so the result reads like a CAD viewport rather than a photo.
    flat_world((1.0, 1.0, 1.0), strength=0.9)
    sun_data = bpy.data.lights.new("KeySun", type="SUN")
    sun_data.energy = 1.6
    sun_data.angle = 0.0  # crisp CAD-style shadows... none: keep shadows off
    sun_data.use_shadow = False
    sun = bpy.data.objects.new("KeySun", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0.0, math.radians(235))
    return (0.05, 0.05, 0.05)


def setup_freestyle(line_color, line_width, crease_angle_deg):
    scene = bpy.context.scene
    scene.render.use_freestyle = True
    scene.render.line_thickness_mode = "ABSOLUTE"
    scene.render.line_thickness = line_width
    view_layer = bpy.context.view_layer
    view_layer.use_freestyle = True
    fs = view_layer.freestyle_settings
    fs.crease_angle = math.radians(crease_angle_deg)
    for ls in list(fs.linesets):
        fs.linesets.remove(ls)
    lineset = fs.linesets.new("CADLines")
    lineset.select_silhouette = True
    lineset.select_border = True
    lineset.select_crease = True
    lineset.select_edge_mark = False
    lineset.select_material_boundary = True
    style = lineset.linestyle
    style.color = line_color
    style.thickness = line_width
    style.caps = "ROUND"


def build_camera(center, radius, azimuth_deg, elevation_deg, args, fit_coords):
    for obj in list(bpy.data.objects):
        if obj.name.startswith("CADCam"):
            bpy.data.objects.remove(obj, do_unlink=True)
    cam_data = bpy.data.cameras.new("CADCam")
    if args.perspective:
        cam_data.type = "PERSP"
        cam_data.angle = math.radians(args.fov)
        cam_data.sensor_fit = "HORIZONTAL"
    else:
        cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("CADCam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    direction = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
    cam.location = center + direction * radius * 3.0
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()

    bpy.context.view_layer.update()
    loc, scale = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), fit_coords)
    if args.perspective:
        cam.location = center + (loc - center) * args.margin
    else:
        cam.location = loc
        cam_data.ortho_scale = scale * args.margin
    cam_data.clip_start = max(radius / 1000.0, 0.001)
    cam_data.clip_end = radius * 100.0
    return cam


def configure_render(args):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = args.samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.max_bounces = 3 if args.style == "shaded" else 0
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    # Technical drawings want exact colors — no filmic/AgX tone curves.
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"


def parse_views(spec):
    views = []
    for token in spec.split(","):
        token = token.strip()
        if token in VIEW_PRESETS:
            views.append((token, *VIEW_PRESETS[token]))
        elif ":" in token:
            az, el = token.split(":")
            views.append((f"az{az}el{el}", float(az), float(el)))
        else:
            raise ValueError(f"unknown view '{token}' (presets: {', '.join(VIEW_PRESETS)})")
    return views


def main():
    args = parse_args()
    bpy.ops.wm.read_factory_settings(use_empty=True)

    meshes = import_model(os.path.abspath(args.input))
    if not meshes:
        raise RuntimeError("no mesh objects were imported")
    lo, hi = scene_bounds(meshes)
    center = (lo + hi) / 2.0
    radius = max((hi - lo).length / 2.0, 1e-6)
    print(f"imported {len(meshes)} meshes, span {(hi - lo).length:.1f}")

    line_color = apply_style(args.style, meshes)
    configure_render(args)
    if not args.no_lines:
        setup_freestyle(line_color, args.line_width, args.crease_angle)

    fit_coords = [f for o in meshes for c in o.bound_box for f in (o.matrix_world @ Vector(c))]

    views = parse_views(args.view)
    base, ext = os.path.splitext(args.output)
    for name, az, el in views:
        build_camera(center, radius, az, el, args, fit_coords)
        suffix = f"_{name}" if len(views) > 1 else ""
        path = os.path.abspath(f"{base}{suffix}{ext}")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        bpy.context.scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
