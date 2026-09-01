# render_glb.py — headless Blender beauty-render for glTF/GLB (and OBJ/STL/FBX/PLY) models.
#
# Techniques adapted from well-known open-source Blender CLI rendering scripts:
#   - yuki-koyama/blender-cli-rendering  (scene/light/camera building blocks, denoising setup)
#   - njanakiev/blender-scripting        (procedural sun/sky worlds, headless batch rendering)
#   - Blender glTF-Blender-IO examples   (robust glTF import handling)
#
# The model gets: an auto-framed camera (fit to the scene bounding box), a physically
# based Nishita sky + sun rig, optional fill/rim area lights, Cycles path tracing with
# adaptive sampling + OpenImageDenoise, and AgX tone mapping.
#
# Usage (regular Blender):
#   blender -b -P scripts/blender/render_glb.py -- --input model.glb --output out/render.png
#
# Usage (pip-installed bpy module):
#   python scripts/blender/render_glb.py --input model.glb --output out/render.png
#
# Multi-view and turntable:
#   ... --views 45,135,225 --elevation 28          # one still per azimuth
#   ... --turntable 120                            # 120-frame orbit animation (PNG sequence)

import argparse
import math
import os
import sys

import bpy
from mathutils import Vector


def parse_args():
    # When run via `blender -P script -- ...` only args after `--` are ours.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    p = argparse.ArgumentParser(description="Headless Blender render for glTF/GLB models")
    p.add_argument("--input", required=True, help="path to .glb/.gltf/.obj/.stl/.fbx/.ply")
    p.add_argument("--output", default="render.png", help="output image path (PNG)")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--samples", type=int, default=128, help="Cycles max samples")
    p.add_argument("--engine", choices=["cycles", "eevee"], default="cycles")
    p.add_argument("--views", default="45", help="comma-separated camera azimuths in degrees")
    p.add_argument("--elevation", type=float, default=30.0, help="camera elevation in degrees")
    p.add_argument("--fov", type=float, default=35.0, help="horizontal field of view in degrees")
    p.add_argument("--margin", type=float, default=1.06, help="framing margin (>1 zooms out)")
    p.add_argument("--sun-elevation", type=float, default=42.0)
    p.add_argument("--sun-azimuth", type=float, default=160.0)
    p.add_argument("--sun-strength", type=float, default=3.0)
    p.add_argument("--sky-strength", type=float, default=1.0, help="sky dome brightness")
    p.add_argument("--exposure", type=float, default=0.4, help="film exposure (stops-ish)")
    p.add_argument("--transparent", action="store_true", help="transparent background")
    p.add_argument("--no-fill", action="store_true", help="disable fill/rim area lights")
    p.add_argument("--turntable", type=int, default=0, help="render N-frame orbit instead of stills")
    p.add_argument("--threads", type=int, default=0, help="0 = auto-detect")
    return p.parse_args(argv)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


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


def build_camera(center, radius, azimuth_deg, elevation_deg, fov_deg, margin, fit_points):
    cam_data = bpy.data.cameras.new("RenderCam")
    cam_data.angle = math.radians(fov_deg)
    cam_data.sensor_fit = "HORIZONTAL"
    cam = bpy.data.objects.new("RenderCam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    direction = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
    # Rough placement first; camera_fit_coords then computes the exact distance
    # so the whole bounding box is in frame regardless of aspect ratio.
    cam.location = center + direction * radius * 3.0
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()

    bpy.context.view_layer.update()
    coords = [f for p in fit_points for v in p for f in v]
    loc, _scale = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
    cam.location = center + (loc - center) * margin

    cam_data.clip_start = max(radius / 1000.0, 0.001)
    cam_data.clip_end = radius * 100.0
    return cam


def build_sky_and_sun(sun_elevation, sun_azimuth, sun_strength, sky_strength):
    world = bpy.data.worlds.new("SkyWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    sky = nodes.new("ShaderNodeTexSky")
    sky.sun_elevation = math.radians(sun_elevation)
    sky.sun_rotation = math.radians(sun_azimuth)
    sky.sun_intensity = 1.0
    sky.altitude = 100.0
    bg = nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = sky_strength
    out = nodes.new("ShaderNodeOutputWorld")
    links.new(sky.outputs["Color"], bg.inputs["Color"])
    links.new(bg.outputs["Background"], out.inputs["Surface"])

    sun_data = bpy.data.lights.new("Sun", type="SUN")
    sun_data.energy = sun_strength
    sun_data.angle = math.radians(1.5)  # slightly soft shadow edges
    sun = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun)
    az, el = math.radians(sun_azimuth), math.radians(sun_elevation)
    sun.rotation_euler = (math.pi / 2.0 - el, 0.0, az + math.pi)
    return sun


def build_fill_lights(center, radius):
    # Classic key/fill/rim studio setup scaled to the model size; the sun acts as
    # the key, so we add a soft fill opposite it and a rim from behind-above.
    specs = [
        ("Fill", (-1.2, 1.0, 0.9), 0.15, 2.0),
        ("Rim", (0.9, 1.3, 1.4), 0.25, 1.4),
    ]
    for name, rel, power_scale, size_scale in specs:
        data = bpy.data.lights.new(name, type="AREA")
        data.shape = "DISK"
        data.size = radius * size_scale
        # Area light wattage must grow with the square of distance to stay balanced.
        data.energy = power_scale * 20.0 * radius * radius
        light = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(light)
        light.location = center + Vector(rel) * radius * 2.0
        look = center - light.location
        light.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()


def configure_render(args):
    scene = bpy.context.scene
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA" if args.transparent else "RGB"
    scene.render.film_transparent = args.transparent

    if args.engine == "cycles":
        scene.render.engine = "CYCLES"
        scene.cycles.device = "CPU"
        scene.cycles.samples = args.samples
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.adaptive_threshold = 0.02
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
        scene.cycles.max_bounces = 6
        scene.cycles.caustics_reflective = False
        scene.cycles.caustics_refractive = False
    else:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
        scene.eevee.taa_render_samples = max(args.samples, 32)

    if args.threads > 0:
        scene.render.threads_mode = "FIXED"
        scene.render.threads = args.threads

    # AgX handles the high dynamic range of a sun-lit scene far more gracefully
    # than the legacy Filmic/Standard transforms.
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = args.exposure


def render_still(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    bpy.context.scene.render.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
    print(f"wrote {path}")


def main():
    args = parse_args()
    reset_scene()

    meshes = import_model(os.path.abspath(args.input))
    if not meshes:
        raise RuntimeError("no mesh objects were imported")
    lo, hi = scene_bounds(meshes)
    center = (lo + hi) / 2.0
    radius = max((hi - lo).length / 2.0, 1e-6)
    print(f"imported {len(meshes)} meshes, bounds {tuple(round(v, 2) for v in lo)}"
          f" .. {tuple(round(v, 2) for v in hi)}")

    build_sky_and_sun(args.sun_elevation, args.sun_azimuth, args.sun_strength, args.sky_strength)
    if not args.no_fill:
        build_fill_lights(center, radius)
    configure_render(args)

    fit_points = [[o.matrix_world @ Vector(c) for c in o.bound_box] for o in meshes]

    base, ext = os.path.splitext(args.output)
    if args.turntable > 0:
        for frame in range(args.turntable):
            azimuth = 360.0 * frame / args.turntable
            for obj in list(bpy.data.objects):
                if obj.name == "RenderCam":
                    bpy.data.objects.remove(obj, do_unlink=True)
            build_camera(center, radius, azimuth, args.elevation, args.fov, args.margin, fit_points)
            render_still(f"{base}_{frame:04d}{ext}")
        return

    views = [float(v) for v in args.views.split(",")]
    for azimuth in views:
        for obj in list(bpy.data.objects):
            if obj.name == "RenderCam":
                bpy.data.objects.remove(obj, do_unlink=True)
        build_camera(center, radius, azimuth, args.elevation, args.fov, args.margin, fit_points)
        suffix = f"_az{int(round(azimuth)):03d}" if len(views) > 1 else ""
        render_still(f"{base}{suffix}{ext}")


if __name__ == "__main__":
    main()
