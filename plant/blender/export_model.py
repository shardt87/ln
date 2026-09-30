#!/usr/bin/env python3
"""Export the presentation model as GLB (glTF 2.0), USDZ (iPhone/iPad Quick Look)
and a .blend with every camera (P1-P11 plates, E1-E8 epic set).

Build the pro scene first, then export:

    python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --no-render \
        --out /tmp/cams --blend plant/model/SK-3X1_plant.blend
    python plant/blender/export_model.py plant/model

Coastal variant A (onshore LNG terminal, jetty and carrier), with a trimmed sea plane:

    python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --no-render --out /tmp/cams \
        --overlay plant/coastal/sk3x1_coastal_A.json --blend plant/model/SK-3X1_coastal_A.blend
    python plant/blender/export_model.py plant/model SK-3X1_coastal_A

GLB and USDZ hold the plant and site (no trees or surrounding ground), Y-up,
with each material's base colour, roughness and metalness.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pro_look  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
out = os.path.abspath(argv[0])
name = argv[1] if len(argv) > 1 else "SK-3X1_plant"
blend = os.path.join(out, name + ".blend")
bpy.ops.wm.open_mainfile(filepath=blend)
scene = bpy.context.scene
have = {o.name for o in bpy.data.objects if o.type == "CAMERA"}
for h in pro_look.EPIC:
    if f"cam {h['k']}" not in have:
        pro_look.hero_camera(scene, h)
for lc in bpy.context.view_layer.layer_collection.children:
    lc.exclude = False
bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
if os.path.exists(blend + "1"):
    os.remove(blend + "1")

land = bpy.data.collections.get("LANDSCAPE")
skip = {o.name for o in land.all_objects} if land else set()
extra = []
sea = bpy.data.objects.get("pro sea")
if sea is not None:
    # the render sea runs for miles; export a plane trimmed to the terminal, berth and approach
    FT = 0.3048
    xs = [v.co.x for v in sea.data.vertices]
    z, x0 = sea.data.vertices[0].co.z, min(xs)
    me = bpy.data.meshes.new("sea (export)")
    me.from_pydata([(x0, -2500 * FT, z), (7200 * FT, -2500 * FT, z), (7200 * FT, 4400 * FT, z), (x0, 4400 * FT, z)],
                   [], [(0, 1, 2, 3)])
    me.materials.append(sea.data.materials[0])
    ob = bpy.data.objects.new("sea (export)", me)
    scene.collection.objects.link(ob)
    extra.append(ob)
for o in bpy.data.objects:
    o.select_set(o.type == "MESH" and (o.name not in skip or o in extra))
bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format="GLB",
                          use_selection=True, export_apply=True, export_yup=True, export_materials="EXPORT")
bpy.ops.wm.usd_export(filepath=os.path.join(out, name + ".usdz"), selected_objects_only=True,
                      export_materials=True, generate_preview_surface=True, export_textures=False)
print("exported", sorted(os.listdir(out)))
