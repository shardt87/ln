#!/usr/bin/env python3
"""Export the presentation model as GLB (glTF 2.0), USDZ (iPhone/iPad Quick Look)
and a .blend with every camera (P1-P11 plates, E1-E8 epic set).

Build the pro scene first, then export:

    python plant/blender/SK-3X1_Rev14_blender_build.py --style pro --no-render \
        --out /tmp/cams --blend plant/model/SK-3X1_plant.blend
    python plant/blender/export_model.py plant/model

GLB and USDZ hold the plant and site (no trees or surrounding ground), Y-up,
with each material's base colour, roughness and metalness.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pro_look  # noqa: E402

out = os.path.abspath(sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else sys.argv[1])
blend = os.path.join(out, "SK-3X1_plant.blend")
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
for o in bpy.data.objects:
    o.select_set(o.type == "MESH" and o.name not in skip)
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "SK-3X1_plant.glb"), export_format="GLB",
                          use_selection=True, export_apply=True, export_yup=True, export_materials="EXPORT")
bpy.ops.wm.usd_export(filepath=os.path.join(out, "SK-3X1_plant.usdz"), selected_objects_only=True,
                      export_materials=True, generate_preview_surface=True, export_textures=False)
print("exported", sorted(os.listdir(out)))
