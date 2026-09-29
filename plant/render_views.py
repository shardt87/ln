#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_views.py  --  cameras, lighting, look, render loop and callout projection (Blender 4.x, Cycles)

Run after build_plant.py has written out/plant.blend:
    blender -b out/plant.blend -P render_views.py -- --views views.json --out out/renders
Options:
    --only 01,04,12      render a subset of view ids
    --scale 0.25         quick test at a quarter of the resolution (callouts.json stays consistent)
    --samples 64         override sample count
    --device gpu|cpu     Cycles device (default: try GPU, fall back to CPU)
    --no-render          only place cameras and write callouts.json (fast check of framing)

Writes:
    out/renders/<id>.png          5000 x 3550 renders (credit line burned into the pixels via a camera-parented text)
    out/renders/callouts.json     2-D frame position of EVERY anchor empty, projected through each view's camera,
                                  plus in-frame / occlusion flags and the camera used
"""
import bpy, json, math, os, sys
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

def arg(name, default=None):
    if name in ARGV:
        i = ARGV.index(name)
        return ARGV[i + 1] if i + 1 < len(ARGV) else True
    return default

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
VIEWS_PATH = arg("--views", os.path.join(HERE, "views.json"))
OUT_DIR = arg("--out", os.path.join(HERE, "out", "renders"))
ONLY = arg("--only")
SCALE = float(arg("--scale", 1.0))
SAMPLES = arg("--samples")
DEVICE = arg("--device", "auto")
NO_RENDER = "--no-render" in ARGV
os.makedirs(OUT_DIR, exist_ok=True)

with open(VIEWS_PATH) as f:
    VIEWS = json.load(f)
RENDER = VIEWS["render"]
SHEET = VIEWS["sheet"]
scene = bpy.context.scene
FT = float(scene.get("plant_true_scale", 0.3048))

# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
def hex_to_lin(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)

def starts_any(name, prefixes):
    return any(name.startswith(p) for p in prefixes)

def emission_material(name, hexcol):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*hex_to_lin(hexcol), 1.0)
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return m

def xray_material():
    m = bpy.data.materials.get("MAT-XRAY-VIEW")
    if m:
        return m
    m = bpy.data.materials.new("MAT-XRAY-VIEW")
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*hex_to_lin(RENDER.get("xray_color", "#C9C6BF")), 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Alpha"].default_value = float(RENDER.get("xray_alpha", 0.3))
    m.blend_method = "BLEND"
    return m

# -----------------------------------------------------------------------------
# scene / look setup (done once)
# -----------------------------------------------------------------------------
def setup_scene():
    scene.render.engine = "CYCLES"
    cy = scene.cycles
    cy.samples = int(SAMPLES) if SAMPLES else int(RENDER.get("samples", 384))
    cy.use_denoising = bool(RENDER.get("denoise", True))
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    cy.use_adaptive_sampling = True
    cy.max_bounces = 6
    cy.diffuse_bounces = 3
    cy.glossy_bounces = 2
    cy.transparent_max_bounces = 12
    cy.film_exposure = float(RENDER.get("exposure", 1.0))
    # device
    if DEVICE != "cpu":
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for dt in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = dt
                    prefs.get_devices()
                    if any(d.type != "CPU" for d in prefs.devices):
                        for d in prefs.devices:
                            d.use = True
                        cy.device = "GPU"
                        print("Cycles device:", dt)
                        break
                except Exception:
                    continue
        except Exception:
            cy.device = "CPU"
    else:
        cy.device = "CPU"
    # resolution
    W, H = RENDER["px"]
    scene.render.resolution_x = int(round(W * SCALE))
    scene.render.resolution_y = int(round(H * SCALE))
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 50
    # colour management: Standard so the backdrop hex lands on the page exactly
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    # world: flat neutral grey, no sky
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (*hex_to_lin(RENDER["backdrop"]), 1.0)
    bg.inputs["Strength"].default_value = float(RENDER.get("world_strength", 1.0))
    world.light_settings.distance = float(RENDER.get("ao_distance_ft", 20)) * FT
    # soft sun (large angular size = soft shadows), coming from the camera's left-front
    for ob in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(ob, do_unlink=True)
    sun_data = bpy.data.lights.new("SUN", "SUN")
    sun_data.energy = float(RENDER.get("sun_energy", 2.0))
    sun_data.angle = math.radians(float(RENDER.get("sun_angle_deg", 25)))
    sun_data.color = (1.0, 0.99, 0.97)
    sun = bpy.data.objects.new("LIGHT-SUN", sun_data)
    scene.collection.objects.link(sun)
    el = math.radians(float(RENDER.get("sun_elevation_deg", 55)))
    az = math.radians(float(RENDER.get("sun_azimuth_deg", 200)))   # measured eastward from south, like the cameras
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))   # from target toward sun
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sun.location = (0, 0, 300)
    # passes for the compositor
    vl = bpy.context.view_layer
    vl.use_pass_ambient_occlusion = True
    vl.use_pass_mist = True
    setup_compositor()

def setup_compositor():
    scene.use_nodes = True
    nt = scene.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers")
    ao = nt.nodes.new("CompositorNodeMixRGB")
    ao.blend_type = "MULTIPLY"
    ao.inputs["Fac"].default_value = float(RENDER.get("ao_strength", 0.45))
    mist = nt.nodes.new("CompositorNodeMixRGB")
    mist.blend_type = "MIX"
    mist.inputs[2].default_value = (*hex_to_lin(RENDER["backdrop"]), 1.0)
    comp = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"], ao.inputs[1])
    nt.links.new(rl.outputs["AO"], ao.inputs[2])
    nt.links.new(ao.outputs["Image"], mist.inputs[1])
    nt.links.new(rl.outputs["Mist"], mist.inputs["Fac"])
    nt.links.new(mist.outputs["Image"], comp.inputs["Image"])

# -----------------------------------------------------------------------------
# visibility / x-ray per view
# -----------------------------------------------------------------------------
_orig_mats = {}

def apply_visibility(view):
    hidden = list(view.get("hidden", []))
    show_below = bool(view.get("show_below_grade", False))
    xray = list(view.get("xray", []))
    for ob in bpy.data.objects:
        if ob.type in ("CAMERA", "LIGHT") or ob.name.startswith(("CREDIT-", "CAM-")):
            continue
        hide = starts_any(ob.name, hidden)
        if ob.get("below_grade", False) and not show_below:
            hide = True
        if ob.name.startswith("ANCHOR-"):
            hide = True                       # empties never render anyway; keep them out of ray casts
        ob.hide_render = hide
        ob.hide_viewport = hide
        # x-ray material swap
        if ob.type in ("MESH", "CURVE") and ob.data and starts_any(ob.name, xray):
            if ob.name not in _orig_mats:
                _orig_mats[ob.name] = [m for m in ob.data.materials]
            xm = xray_material()
            for i in range(len(ob.data.materials)):
                ob.data.materials[i] = xm
    bpy.context.view_layer.update()

def restore_materials():
    for name, mats in _orig_mats.items():
        ob = bpy.data.objects.get(name)
        if ob and ob.data:
            for i, m in enumerate(mats):
                if i < len(ob.data.materials):
                    ob.data.materials[i] = m
    _orig_mats.clear()

# -----------------------------------------------------------------------------
# camera framing
# -----------------------------------------------------------------------------
def visible_bbox(prefixes, box_ft=None):
    if box_ft:
        b = [v * FT for v in box_ft]
        return Vector((b[0], b[1], b[2])), Vector((b[3], b[4], b[5]))
    lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9))
    for ob in bpy.data.objects:
        if ob.hide_render or ob.type not in ("MESH", "CURVE") or not starts_any(ob.name, prefixes):
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
            hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
    if lo.x > hi.x:
        raise RuntimeError("frame prefixes matched nothing: %s" % prefixes)
    return lo, hi

def place_camera(view):
    cam_spec = view["camera"]
    name = "CAM-" + view["id"]
    cam = bpy.data.objects.get(name)
    if cam is None:
        cd = bpy.data.cameras.new(name)
        cam = bpy.data.objects.new(name, cd)
        scene.collection.objects.link(cam)
    cd = cam.data
    cd.type = "PERSP"
    cd.lens = float(cam_spec["lens"])
    cd.sensor_width = 36.0
    cd.sensor_fit = "HORIZONTAL"
    cd.clip_start = 0.5
    cd.clip_end = 20000.0
    W, H = scene.render.resolution_x, scene.render.resolution_y
    hh = 18.0 / cd.lens                     # tan(hfov/2)
    hv = hh * H / W                          # tan(vfov/2)
    ct = float(cam_spec.get("crop_top", 0.0))
    cd.shift_x = 0.0
    cd.shift_y = (hv * ct) / (2.0 * hh)      # visible (un-cropped) region centred on the target
    az = math.radians(float(cam_spec["az"]))
    el = math.radians(float(cam_spec["el"]))
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))   # target -> camera
    # target: explicit anchor, explicit point (ft) or the centre of the framed bbox
    lo, hi = visible_bbox(view.get("frame", ["SITE-GROUND"]), view.get("frame_box_ft"))
    if "target_ft" in cam_spec:
        t = Vector([v * FT for v in cam_spec["target_ft"]])
    elif "target_anchor" in cam_spec:
        t = bpy.data.objects[cam_spec["target_anchor"]].matrix_world.translation.copy()
    else:
        t = (lo + hi) / 2.0
        t.z = lo.z + (hi.z - lo.z) * float(cam_spec.get("target_height_frac", 0.35))
    rot = (-d).to_track_quat("-Z", "Y")
    f = -d                                      # camera forward (toward target)
    right = rot @ Vector((1, 0, 0))
    up = rot @ Vector((0, 1, 0))
    corners = [Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
    need = 0.0
    for c in corners:
        rel = c - t
        depth = rel.dot(f)
        need = max(need, abs(rel.dot(right)) / hh - depth, abs(rel.dot(up)) / (hv * (1.0 - ct)) - depth)
    dist = need * float(cam_spec.get("pad", 1.08))
    if "distance_ft" in cam_spec:
        dist = float(cam_spec["distance_ft"]) * FT
    cam.location = t + d * dist
    cam.rotation_euler = rot.to_euler()
    scene.camera = cam
    # mist: fade the far ground into the page colour
    scene.world.mist_settings.start = dist * float(RENDER.get("mist_start_factor", 1.1))
    scene.world.mist_settings.depth = dist * float(RENDER.get("mist_depth_factor", 2.5))
    scene.world.mist_settings.falloff = "LINEAR"
    scene.world.mist_settings.intensity = 0.0
    # credit line burned into the pixels: text parented to the camera, bottom-left of the FULL frame
    place_credit(cam, hh, hv, ct)
    return cam, dist, t

def place_credit(cam, hh, hv, ct):
    name = "CREDIT-" + cam.name
    tx = bpy.data.objects.get(name)
    if tx is None:
        cu = bpy.data.curves.new(name, "FONT")
        tx = bpy.data.objects.new(name, cu)
        scene.collection.objects.link(tx)
    cu = tx.data
    cu.body = SHEET["credit"]
    cu.align_x = "LEFT"
    cu.align_y = "BOTTOM"
    cu.resolution_u = 8
    cu.materials.clear()
    cu.materials.append(emission_material("MAT-CREDIT", SHEET.get("credit_color", "#4A4A48")))
    D = 6.0                                     # metres in front of the lens
    frame_w = 2.0 * hh * D
    frame_h = 2.0 * hv * D
    bottom = (-hv + 2.0 * hh * cam.data.shift_y) * D
    cu.size = frame_h * float(SHEET.get("credit_height_frac", 0.011))
    tx.parent = cam
    tx.matrix_parent_inverse = Matrix.Identity(4)
    tx.location = (-hh * D + frame_w * 0.018, bottom + frame_h * 0.022, -D)
    tx.rotation_euler = (0, 0, 0)
    tx.hide_render = False
    tx.hide_viewport = False
    for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
        if hasattr(tx, attr):
            setattr(tx, attr, False)
    # only this view's credit is visible
    for ob in bpy.data.objects:
        if ob.name.startswith("CREDIT-") and ob is not tx:
            ob.hide_render = True
            ob.hide_viewport = True

# -----------------------------------------------------------------------------
# callout projection
# -----------------------------------------------------------------------------
def project_anchors(cam, view):
    W, H = scene.render.resolution_x, scene.render.resolution_y
    deps = bpy.context.evaluated_depsgraph_get()
    origin = cam.matrix_world.translation
    out = {}
    xray = list(view.get("xray", []))
    for ob in bpy.data.objects:
        if not ob.name.startswith("ANCHOR-"):
            continue
        p = ob.matrix_world.translation
        v = world_to_camera_view(scene, cam, p)
        in_frame = (0.0 <= v.x <= 1.0) and (0.0 <= v.y <= 1.0) and v.z > 0
        visible = None
        hit_name = None
        if in_frame:
            direction = (p - origin)
            dist = direction.length
            direction.normalize()
            ok, loc, nrm, idx, hit_ob, mat = scene.ray_cast(deps, origin, direction, distance=dist + 5.0)
            if ok:
                hit_name = hit_ob.name
                hit_d = (loc - origin).length
                # a hit close to the anchor (its own equipment) counts as visible; x-rayed objects never occlude
                visible = (hit_d >= dist - 1.5) or starts_any(hit_ob.name, xray)
            else:
                visible = True
        out[ob.name] = dict(
            u=round(v.x, 5), v=round(1.0 - v.y, 5),          # v measured from the TOP of the image
            px=round(v.x * W, 1), py=round((1.0 - v.y) * H, 1),
            depth_m=round(v.z, 2), in_frame=in_frame, visible=visible, hit=hit_name,
            label=str(ob.get("label", "")), zone=int(ob.get("zone", 0)))
    return out

# -----------------------------------------------------------------------------
# main loop
# -----------------------------------------------------------------------------
def main():
    setup_scene()
    callouts = dict(render_px=[scene.render.resolution_x, scene.render.resolution_y], scale=SCALE, views={})
    only = set(ONLY.split(",")) if ONLY else None
    for view in VIEWS["views"]:
        if view.get("kind", "camera") != "camera":
            continue
        if only and view["id"] not in only:
            continue
        print("=== view", view["id"], view["title"])
        apply_visibility(view)
        cam, dist, t = place_camera(view)
        bpy.context.view_layer.update()
        anchors = project_anchors(cam, view)
        callouts["views"][view["id"]] = dict(
            camera=dict(name=cam.name, az=view["camera"]["az"], el=view["camera"]["el"], lens=view["camera"]["lens"],
                        crop_top=view["camera"].get("crop_top", 0.0), shift_y=cam.data.shift_y,
                        location_m=[round(c, 3) for c in cam.location], target_m=[round(c, 3) for c in t],
                        distance_m=round(dist, 2)),
            anchors=anchors)
        missing = [c["anchor"] for c in view.get("callouts", []) if c["anchor"] not in anchors]
        offframe = [c["anchor"] for c in view.get("callouts", []) if c["anchor"] in anchors and not anchors[c["anchor"]]["in_frame"]]
        occluded = [c["anchor"] for c in view.get("callouts", []) if c["anchor"] in anchors and anchors[c["anchor"]]["visible"] is False]
        if missing:
            print("  ! missing anchors:", missing)
        if offframe:
            print("  ! callouts outside frame:", offframe)
        if occluded:
            print("  - callouts occluded (still placed, check leader):", occluded)
        if not NO_RENDER:
            scene.render.filepath = os.path.join(OUT_DIR, view["id"] + ".png")
            bpy.ops.render.render(write_still=True)
            print("  wrote", scene.render.filepath)
        restore_materials()
        # write after every view so a long run can be resumed / inspected
        with open(os.path.join(OUT_DIR, "callouts.json"), "w") as f:
            json.dump(callouts, f, indent=1)
    print("done:", os.path.join(OUT_DIR, "callouts.json"))

main()
