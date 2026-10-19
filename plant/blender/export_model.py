#!/usr/bin/env python3
"""Export the presentation model as GLB (glTF 2.0), USDZ (iPhone/iPad Quick Look)
and a .blend with every camera (P1-P11 plates, E1-E8 epic set).

Build the pro scene first, then export:

    python plant/blender/SW-3X1_Rev14_blender_build.py --style pro --no-render \
        --out /tmp/cams --blend plant/model/SW-3X1_plant.blend
    python plant/blender/export_model.py plant/model

Coastal variant A (onshore LNG terminal, jetty and carrier), with a trimmed sea plane:

    python plant/blender/SW-3X1_Rev14_blender_build.py --style pro --no-render --out /tmp/cams \
        --overlay plant/coastal/sw3x1_coastal_A.json --blend plant/model/SW-3X1_coastal_A.blend
    python plant/blender/export_model.py plant/model SW-3X1_coastal_A

Plant plus the BTM data centre (design option, an add-on to the plant; the plant and coastal exports leave it out):

    python plant/blender/export_model.py plant/model SW-3X1_plant_datacenter SW-3X1_plant

Everything (plant, LNG satellite and marine terminal, BTM data centre):

    python plant/blender/export_model.py plant/model SW-3X1_everything_datacenter SW-3X1_coastal_A

GLB and USDZ hold the plant and site (no trees or surrounding ground), Y-up,
with each material's base colour, roughness and metalness, and the printed decals / screens as images.
Before exporting, export_slim.py drops geometry nobody can see (hidden rod caps, buried faces) and merges the
decal quads, and tools/glb_images.py recompresses the GLB's images, so each file stays under GitHub's 100 MiB
limit (Oct 18: GLB 140-147 MB -> about 96-101 MB). The saved .blend is not trimmed.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_slim  # noqa: E402
import pro_look  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import glb_images  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
out = os.path.abspath(argv[0])
name = argv[1] if len(argv) > 1 else "SW-3X1_plant"
src = argv[2] if len(argv) > 2 else name
with_dc = "datacenter" in name               # the BTM data centre is an add-on: only its own export carries it
blend = os.path.join(out, name + ".blend")
bpy.ops.wm.open_mainfile(filepath=os.path.join(out, src + ".blend"))
scene = bpy.context.scene
have = {o.name for o in bpy.data.objects if o.type == "CAMERA"}
for h in pro_look.EPIC:
    if f"cam {h['k']}" not in have:
        pro_look.hero_camera(scene, h)
for lc in bpy.context.view_layer.layer_collection.children:
    lc.exclude = lc.name.startswith("OPT_DC") and not with_dc
bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
if os.path.exists(blend + "1"):
    os.remove(blend + "1")

land = bpy.data.collections.get("LANDSCAPE")
skip = {o.name for o in land.all_objects} if land else set()
extra = []
sea = bpy.data.objects.get("pro sea")
if sea is not None:
    # the render sea runs for miles; export a plane trimmed to the terminal, berth and approach (sea to the north)
    FT = 0.3048
    z, y0 = sea.data.vertices[0].co.z, min(v.co.y for v in sea.data.vertices)
    me = bpy.data.meshes.new("sea (export)")
    me.from_pydata([(-2000 * FT, y0, z), (5000 * FT, y0, z), (5000 * FT, 6700 * FT, z), (-2000 * FT, 6700 * FT, z)],
                   [], [(0, 1, 2, 3)])
    me.materials.append(sea.data.materials[0])
    ob = bpy.data.objects.new("sea (export)", me)
    scene.collection.objects.link(ob)
    extra.append(ob)


def chosen(o):
    dc = any(c.name.startswith("OPT_DC") for c in o.users_collection)
    return o.type == "MESH" and (o.name not in skip or o in extra) and (with_dc or not dc)


print(export_slim.slim(bpy, [o for o in bpy.data.objects if chosen(o)]))
for o in bpy.data.objects:
    o.select_set(chosen(o))
bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format="GLB",
                          use_selection=True, export_apply=True, export_yup=True, export_materials="EXPORT",
                          export_extras=True)
glb_images.main(os.path.join(out, name + ".glb"), os.path.join(out, name + ".glb"))
for im in bpy.data.images:                   # USDZ packs the decal images as files: palette PNGs, same names
    if im.packed_file:
        data = bytes(im.packed_file.data)
        new = glb_images.slim(data, "image/png", jpeg=False)[0]
        if len(new) < len(data):
            im.pack(data=new, data_len=len(new))
bpy.ops.wm.usd_export(filepath=os.path.join(out, name + ".usdz"), selected_objects_only=True,
                      export_materials=True, generate_preview_surface=True, export_textures=True,
                      overwrite_textures=True)
print("exported", sorted(os.listdir(out)))
