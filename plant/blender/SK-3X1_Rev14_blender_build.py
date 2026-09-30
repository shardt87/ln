"""SK-3X1 Rev 14 Blender build: scene, cameras and renders.

The script named on sheet SK-3X1-11. It builds the plant from
plant/sk3x1_model.json into collections named as on that sheet, sets up the
orthographic 1920 x 1080 cameras fitted to each view with a 3% margin, and
renders them in the sheet-11 style (white world, neutral grey equipment,
copper only on cables / trays / bus, dark Freestyle outlines).

Runs in Blender or as the `bpy` Python module:

    blender -b -P plant/blender/SK-3X1_Rev14_blender_build.py -- --views A,B
    python  plant/blender/SK-3X1_Rev14_blender_build.py --views A,B

Options (after `--` in Blender):
    --views A,B,...   views to render (default: all but ALL)
    --style drawing   sheet-11 look (default) | photo (sky, no outlines)
    --samples 64      Cycles samples (denoised)
    --scale 100       resolution percentage of 1920 x 1080
    --out DIR         output directory (default plant/renders/blender)
    --blend FILE      also save the .blend
    --no-render       build the scene only

Each render writes <view>.png plus <view>.labels.json (tag anchors in
pixel coordinates, visible from the camera) for annotate.py, which burns
labels and the credit block into the image.

Conceptual illustration. Not engineered. Not for construction.
"""
import argparse
import json
import math
import os
import sys
import time

import bpy
import bmesh  # after bpy: the bpy module build registers bmesh on import
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
ap = argparse.ArgumentParser()
ap.add_argument("--views", default="")
ap.add_argument("--style", default="drawing", choices=["drawing", "photo", "pro"])
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--scale", type=int, default=100)
ap.add_argument("--out", default=os.path.join(PLANT, "renders", "blender"))
ap.add_argument("--blend", default="")
ap.add_argument("--no-render", action="store_true")
ap.add_argument("--set", default="", help="camera set for --style pro: '' (plates P1-P11) or 'epic' (E1-E8)")
ap.add_argument("--overlay", default="", help="coastal variant overlay (plant/coastal/sk3x1_coastal_A.json or _B)")
args = ap.parse_args(argv)

model = json.load(open(os.path.join(PLANT, "sk3x1_model.json")))
coastal = None
if args.overlay:
    ov = json.load(open(args.overlay))
    model["layers"].update(ov["layers"])
    model["items"] += ov["items"]
    model["parts"] += ov["parts"]
    coastal = ov["coastal"]
sys.path.insert(0, HERE)
import pro_look  # noqa: E402  (professional presentation look, --style pro)
palette = json.load(open(os.path.join(PLANT, "palette.json")))
items = {it["id"]: it for it in model["items"]}

# ---------------------------------------------------------------------------
# Scene reset
# ---------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "IMPERIAL"
scene.unit_settings.length_unit = "FEET"
FT = 0.3048  # Blender units are metres; the model is in feet


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
ROUGH = {"steel": .45, "stair": .5, "grating": .55, "machine": .4, "xfmr": .45, "radiator": .45,
         "duct": .5, "stack": .5, "tank": .35, "crane": .4, "conductor": .3, "copper": .35,
         "copper_dark": .35, "insulator": .25, "water": .08, "door": .4}
METAL = {"copper": .85, "copper_dark": .85, "conductor": .7, "steel": .3, "crane": .2}
mats = {}
PHOTO_KEEP = {"copper", "copper_dark", "amber", "crane", "red", "water", "conditional", "insulator", "door"}


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def material(key):
    if args.style == "pro":
        return pro_look.material(key)
    if key in mats:
        return mats[key]
    hx = palette.get(key, palette["equip"])["hex"].lstrip("#")
    rgb = [srgb_to_lin(int(hx[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    if args.style == "photo" and key not in PHOTO_KEEP:
        rgb = [c * .55 for c in rgb]      # drawing palette is light; real albedos are darker
    m = bpy.data.materials.new(key)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = ROUGH.get(key, .7)
    # drawing style: matte paint everywhere (metal reflections of a white world go black)
    b.inputs["Metallic"].default_value = METAL.get(key, 0) if args.style == "photo" else 0
    if key == "hall" and args.style == "photo":
        b.inputs["Base Color"].default_value = (*[srgb_to_lin(v) for v in (.80, .84, .87)], 1)
    m.diffuse_color = (*rgb, 1)
    mats[key] = m
    return m


# ---------------------------------------------------------------------------
# Geometry (model coordinates are X east, Y north, Z up, feet)
# ---------------------------------------------------------------------------
def box_geo(lo, hi):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    v = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    f = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    return v, f, [False] * 6


def rod_geo(a, b, r1, r2, n):
    ax = Vector(b) - Vector(a)
    L = ax.length or 1
    ax.normalize()
    ref = Vector((1, 0, 0)) if abs(ax.x) < .9 else Vector((0, 1, 0))
    u = ax.cross(ref).normalized()
    w = ax.cross(u)
    ring = lambda c, r: [tuple(Vector(c) + r * (math.cos(2 * math.pi * k / n) * u + math.sin(2 * math.pi * k / n) * w))
                         for k in range(n)]
    s0, s1 = ring(a, r1), ring(b, r2)
    v = s0 + s1 + ring(a, r1) + ring(b, r2)          # separate cap rings keep caps flat
    f = [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    f += [tuple(2 * n + k for k in reversed(range(n))), tuple(3 * n + k for k in range(n))]
    return v, f, [True] * n + [False, False]


def prism_geo(lo, hi, ridge):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    if ridge == "x":
        ym = (y0 + y1) / 2
        v = [(x0, y0, z0), (x0, y1, z0), (x0, ym, z1), (x1, y0, z0), (x1, y1, z0), (x1, ym, z1)]
    else:
        xm = (x0 + x1) / 2
        v = [(x0, y0, z0), (x1, y0, z0), (xm, y0, z1), (x0, y1, z0), (x1, y1, z0), (xm, y1, z1)]
    f = [(0, 2, 1), (3, 4, 5), (0, 3, 5, 2), (1, 2, 5, 4), (0, 1, 4, 3)]
    return v, f, [False] * 5


def hex_geo(q):
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return [tuple(p) for p in q], f, [False] * 6


def part_geo(p):
    k = p["kind"]
    if k == "box":
        return box_geo(p["min"], p["max"])
    if k == "rod":
        rr = max(p["r"], p["r2"])
        return rod_geo(p["a"], p["b"], p["r"], p["r2"], p.get("seg", 36 if rr > 10 else 16))
    if k == "prism":
        return prism_geo(p["min"], p["max"], p.get("ridge", "y"))
    return hex_geo(p["v"])


collections = {}


def coll(name):
    if name not in collections:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        collections[name] = c
    return collections[name]


def make_object(name, layer, geos):
    """geos: list of (verts, faces, smooth flags, material key)."""
    verts, faces, smooth, mat_idx, keys = [], [], [], [], []
    for (v, f, sm, key) in geos:
        if key not in keys:
            keys.append(key)
        base = len(verts)
        verts += [(x * FT, y * FT, z * FT) for (x, y, z) in v]
        faces += [tuple(base + i for i in face) for face in f]
        smooth += sm
        mat_idx += [keys.index(key)] * len(f)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if me.validate(clean_customdata=False) and os.environ.get("SK_DEBUG"):
        print("validated (fixed):", name)
    for k in keys:
        me.materials.append(material(k))
    me.polygons.foreach_set("material_index", mat_idx)
    me.polygons.foreach_set("use_smooth", smooth)
    # consistent outward normals (lofts can be wound either way)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll(layer).objects.link(ob)
    return ob


t0 = time.time()
buckets = {}
for p in model["parts"]:
    buckets.setdefault((p["item"], p["layer"]), []).append(p)
item_objs = {}
for (iid, layer), ps in buckets.items():
    it = items[iid]
    geos = [(*part_geo(p), p["color"]) for p in ps]
    ob = make_object(f"{it['tag'] or it['name'][:40]} [{iid}]", layer, geos)
    ob["item"] = iid
    item_objs.setdefault(iid, []).append(ob)
# Routes. The drawing runs many circuits along one tray path, so collinear
# segments overlap; coincident faces render black in Cycles. Merge them into
# one run per (layer, type, line) and lift N-S runs slightly above E-W runs.
runs, risers = {}, {}
for r in model["routes"]:
    z = .3 if r["z"] < 0 else r["z"]
    key0 = (r["layer"], r["type"], r["color"], z, r["w"], .35 if r["z"] < 0 else r["h"])
    for (ax, ay), (bx, by) in zip(r["points"], r["points"][1:]):
        if ay == by and ax != bx:
            runs.setdefault(key0 + ("x", ay), []).append((min(ax, bx), max(ax, bx)))
        elif ax == bx and ay != by:
            runs.setdefault(key0 + ("y", ax), []).append((min(ay, by), max(ay, by)))
    if r["z"] > 6 and r["type"] not in ("ipb", "hv_overhead", "hmod"):
        for (x, y) in (r["points"][0], r["points"][-1]):
            risers[(r["layer"], r["color"], round(x, 1), round(y, 1))] = (r["w"], z)
route_geos = {}
for (layer, rtype, color, z, w, h, axis, c), ivs in runs.items():
    ivs.sort()
    merged = [list(ivs[0])]
    for a, b in ivs[1:]:
        if a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    hw, dz = w / 2, (0.03 if axis == "y" else 0)
    for a, b in merged:
        lo, hi = ((a - hw, c - hw), (b + hw, c + hw)) if axis == "x" else ((c - hw, a - hw), (c + hw, b + hw))
        route_geos.setdefault((layer, rtype), []).append(
            (*box_geo((lo[0], lo[1], z - h / 2 + dz), (hi[0], hi[1], z + h / 2 + dz)), color))
for (layer, color, x, y), (w, z) in risers.items():
    hw = w / 2 * 0.98
    route_geos.setdefault((layer, "riser"), []).append((*box_geo((x - hw, y - hw, 0), (x + hw, y + hw, z - .5)), color))
for (layer, rtype), geos in route_geos.items():
    make_object(f"routes {layer} {rtype}", layer, geos)

# ground beyond the compound
if args.style == "pro":
    n_trees = pro_look.landscape(scene, coll("LANDSCAPE"), coastal)
    print(f"landscape: {n_trees} trees")
else:
    me = bpy.data.meshes.new("surround")
    S = 6000
    me.from_pydata([(-S * FT, -S * FT, -.6 * FT), ((2420 + S) * FT, -S * FT, -.6 * FT),
                    ((2420 + S) * FT, (1920 + S) * FT, -.6 * FT), (-S * FT, (1920 + S) * FT, -.6 * FT)], [], [(0, 1, 2, 3)])
    surround = bpy.data.objects.new("surround", me)
    coll("SITE").objects.link(surround)
    gm = bpy.data.materials.new("surround")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = \
        (.93, .93, .92, 1) if args.style == "drawing" else (.20, .26, .14, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = .95
    me.materials.append(gm)
print(f"scene built: {len(bpy.data.objects)} objects in {len(collections)} collections, {time.time()-t0:.1f}s")

# ---------------------------------------------------------------------------
# World, light, render settings
# ---------------------------------------------------------------------------
HERO_SET = pro_look.hero_set(coastal, args.set)
if args.style == "pro":
    pro_look.world_and_sun(scene, *HERO_SET["sun"])
else:
    world = bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    wn = world.node_tree.nodes
    bg = wn["Background"]
    if args.style == "drawing":
        # camera sees white; lighting comes from a softer grey world
        lp = wn.new("ShaderNodeLightPath")
        mix = wn.new("ShaderNodeMixShader")
        white = wn.new("ShaderNodeBackground")
        white.inputs["Color"].default_value = (1, 1, 1, 1)
        white.inputs["Strength"].default_value = 1.0
        world.node_tree.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
        world.node_tree.links.new(bg.outputs["Background"], mix.inputs[1])
        world.node_tree.links.new(white.outputs["Background"], mix.inputs[2])
        world.node_tree.links.new(mix.outputs["Shader"], wn["World Output"].inputs["Surface"])
        bg.inputs["Color"].default_value = (1, 1, 1, 1)
        bg.inputs["Strength"].default_value = .55
    else:
        sky = wn.new("ShaderNodeTexSky")
        sky.sky_type = "NISHITA"
        sky.sun_elevation = math.radians(38)
        sky.sun_rotation = math.radians(215)
        world.node_tree.links.new(sky.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = .1

    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 2.6 if args.style == "drawing" else 3.0
    sun.angle = math.radians(2.5)
    sun_ob = bpy.data.objects.new("sun", sun)
    sun_ob.rotation_euler = (math.radians(50), 0, math.radians(215))
    scene.collection.objects.link(sun_ob)

scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 4
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.resolution_percentage = args.scale
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = -0.4 if args.style == "photo" else 0
scene.render.image_settings.file_format = "PNG"
if args.style == "pro":
    pro_look.render_settings(scene, args.samples)
    pro_look.compositor(scene)
if args.style == "drawing":
    scene.render.use_freestyle = True
    scene.render.line_thickness_mode = "ABSOLUTE"
    scene.render.line_thickness = 1.0
    vl = scene.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(140)
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("outlines")
    ls.select_by_visibility = True
    ls.select_silhouette = ls.select_border = ls.select_crease = True
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("sk3x1 outline")
    ls.linestyle.color = (0, 0, 0)
    ls.linestyle.alpha = 1
    # below ~1 px Freestyle strokes disappear; 1.6 px at full size
    ls.linestyle.thickness = max(1.2, 1.8 * args.scale / 100)

# ---------------------------------------------------------------------------
# Cameras (SK-3X1-11: orthographic, 1920 x 1080, sensor fit horizontal, 3% margin)
# ---------------------------------------------------------------------------
def fit_points(v):
    fit, pts = v["fit"], []
    boxes = []
    if "box" in fit:
        b = fit["box"]
        boxes.append((b[0], b[1], b[2], b[3], b[4], b[5]))
    if "layers" in fit and "box" not in fit:
        cx0, cx1, cy0, cy1 = fit.get("clip", (-1e9, 1e9, -1e9, 1e9))
        for it in model["items"]:
            f = it["fp"]
            if it["layer"] in fit["layers"] and it["z"][1] > .7 and cx0 <= f[0] and f[1] <= cx1 \
                    and cy0 <= f[2] and f[3] <= cy1:
                boxes.append((f[0], f[1], f[2], f[3], it["z"][0], it["z"][1]))
    for (x0, x1, y0, y1, z0, z1) in boxes:
        pts += [Vector((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    return pts


def make_camera(v, margin=.03):
    t, c = Vector(v["t"]), Vector(v["c"])
    d = (t - c).normalized()
    right = d.cross(Vector((0, 0, 1))).normalized()
    up = right.cross(d)
    pts = fit_points(v)
    us = [(p - t).dot(right) for p in pts]
    vs = [(p - t).dot(up) for p in pts]
    uc, vc = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
    uw, vh = max(us) - min(us), max(vs) - min(vs)
    aspect = 1920 / 1080
    # 3% margin on the tighter axis
    scale = max(uw, vh * aspect) / (1 - 2 * margin)
    target = t + right * uc + up * vc
    cam = bpy.data.cameras.new(f"cam {v['k']}")
    cam.type = "ORTHO"
    cam.sensor_fit = "HORIZONTAL"
    cam.ortho_scale = scale * FT
    cam.clip_start, cam.clip_end = 100 * FT, 12000 * FT
    ob = bpy.data.objects.new(f"cam {v['k']}", cam)
    ob.location = (target - d * 4000) * FT
    ob.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()
    scene.collection.objects.link(ob)
    mu = (scale - uw) / 2 / scale
    mv = (scale / aspect - vh) / 2 / (scale / aspect)
    return ob, dict(ortho_ft=round(scale, 1), margin_lr=round(mu * 100, 1), margin_tb=round(mv * 100, 1))


def set_visibility(show):
    """Exclude hidden collections from the view layer, so they neither
    render nor block the label visibility rays."""
    show = set(show) | {"SITE", "LANDSCAPE"}
    for lc in bpy.context.view_layer.layer_collection.children:
        lc.exclude = lc.name not in show


LABEL = {"GT1", "GT2", "GT3", "ST", "HRSG-1", "HRSG-2", "HRSG-3", "STK-1", "ACC", "R1", "R2A", "R2B", "R2C", "R3",
         "R4", "RH", "CR", "GSU-1", "GSU-2", "GSU-3", "GSU-ST", "FH-1", "FH-2", "FH-3", "R-WT", "EDG-1", "EDG-2",
         "ABS-A", "ABS-B", "ABS-C", "STR-B", "DCC-A", "CCS T-1", "BF-A", "AUXC", "CP-A/B/C", "VAC-A/B", "CCW-A/B",
         "CRANE", "BESS", "BESS MPT", "RICE", "SC-1", "SC-2", "H2-EL", "T-H2", "T-MOD-1", "MOD-EH", "MOB-1",
         "LNG-T4", "Line-1", "Line-2", "SWGR-13.8-1", "SWGR-13.8-2", "SWGR-13.8-3", "SWGR-4.16-A", "LC-480-A",
         "LCI-1", "LCI-2", "LCI-3", "MCC-GT1", "VFD-L1", "VFD-L4", "CCS-CT", "D1-CB2", "D2-CB2", "D3-CB2",
         "GCB-1", "SPOOL-1", "GTG-1", "STG", "INL-1", "BFP-1", "CONT-1", "PAD-EH", "H2-ST", "ST exhaust"}


def labels_for(v, cam_ob, show):
    show = set(show)
    deps = bpy.context.evaluated_depsgraph_get()
    out = []
    seen = set()
    for it in model["items"]:
        if it["tag"] not in LABEL or it["layer"] not in show or it["tag"] in seen:
            continue
        f = it["fp"]
        top = Vector(((f[0] + f[1]) / 2, (f[2] + f[3]) / 2, it["z"][1])) * FT
        p = world_to_camera_view(scene, cam_ob, top)
        if not (0.02 < p.x < 0.98 and 0.04 < p.y < 0.98):
            continue
        # visible if the ray from the anchor back toward the camera is clear
        d = (cam_ob.matrix_world.to_quaternion() @ Vector((0, 0, 1))).normalized()
        hit, loc, *_ = scene.ray_cast(deps, top + d * 0.3, d, distance=20000)
        if hit:
            continue
        seen.add(it["tag"])
        out.append(dict(tag=it["tag"], name=it["name"], x=round(p.x * 1920 * args.scale / 100, 1),
                        y=round((1 - p.y) * 1080 * args.scale / 100, 1), optional=it["layer"].startswith("OPT_")))
    return out


os.makedirs(args.out, exist_ok=True)
manifest = []
if args.style == "pro":
    heroes = HERO_SET["heroes"]
    keys = [k for k in args.views.split(",") if k] or [h["k"] for h in heroes]
    ALL = [l for l in model["layers"] if l not in ("R1_INTERIOR", "R4_INTERIOR")]
    COAST = [l for l, v in model["layers"].items() if v.get("group", "").startswith("Coastal")]
    BASE = [l for l in ALL if not l.startswith(("OPT_", "HV_CORRIDOR", "SWYD_FUTURE")) and l not in COAST]
    ALL = [l for l in ALL if l not in COAST]
    for h in heroes:
        if h["k"] not in keys:
            continue
        cam_ob = pro_look.hero_camera(scene, h)
        scene.camera = cam_ob
        # coastal: the whole plant with its optional systems, except the trucked LNG satellite (sheet 14),
        # which the marine terminal replaces
        show = {"base": BASE, "all": ALL,
                "coastal": [l for l in ALL if not l.startswith("OPT_LNG")] + COAST}[h["show"]]
        set_visibility(show)
        info = dict(k=h["k"], name=h["n"], show=show, style="pro", samples=args.samples, lens=h["lens"],
                    ortho_ft=0, margin_lr=0, margin_tb=0, sun=list(HERO_SET["sun"]), sheet=HERO_SET["sheet"])
        base = os.path.join(args.out, f"{h['k']}_pro")
        json.dump(dict(view=info, labels=[]), open(base + ".labels.json", "w"), indent=1)
        if not args.no_render:
            t1 = time.time()
            scene.render.filepath = base + ".png"
            bpy.ops.render.render(write_still=True)
            info["seconds"] = round(time.time() - t1, 1)
            print(f"rendered {h['k']:<3} {h['n']:<40} {h['lens']} mm  {info['seconds']}s")
        manifest.append(info)
else:
    keys = [k for k in args.views.split(",") if k] or [v["k"] for v in model["views"] if v["k"] != "ALL"]
for v in (model["views"] if args.style != "pro" else []):
    if v["k"] not in keys:
        continue
    cam_ob, info = make_camera(v)
    scene.camera = cam_ob
    set_visibility(v["show"])
    info.update(k=v["k"], name=v["n"], show=v["show"], style=args.style, samples=args.samples)
    lab = labels_for(v, cam_ob, v["show"])
    base = os.path.join(args.out, f"{v['k']}_{args.style}")
    json.dump(dict(view=info, labels=lab), open(base + ".labels.json", "w"), indent=1)
    if not args.no_render:
        t1 = time.time()
        scene.render.filepath = base + ".png"
        bpy.ops.render.render(write_still=True)
        info["seconds"] = round(time.time() - t1, 1)
        print(f"rendered {v['k']:<3} {v['n']:<26} ortho {info['ortho_ft']} ft  "
              f"margins L/R {info['margin_lr']}% T/B {info['margin_tb']}%  {info['seconds']}s")
    manifest.append(info)
json.dump(manifest, open(os.path.join(args.out, f"manifest_{args.style}_{'-'.join(keys)}.json"), "w"), indent=1)
set_visibility([c for c in collections])
if args.blend:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend))
    print("saved", args.blend)
