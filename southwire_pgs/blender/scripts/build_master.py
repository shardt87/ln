"""Build the Southwire PGS master scene and save it as a .blend file.

Usage (either):
    blender -b -P build_master.py                 # Blender 4.2+ / 5.x
    python3 build_master.py                       # with the 'bpy' module installed
Output: ../Southwire_PGS_Master.blend  (next to this scripts/ folder)
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bpy  # noqa: E402
import scene_setup as ss  # noqa: E402
from swlib import coll, camera, empty  # noqa: E402
import mod_switchgear, mod_generator, mod_plant, mod_ehouse, mod_temp, mod_bench  # noqa: E402
from views import define_views  # noqa: E402

ZONES = {"SWG": (0.0, 40.0, 0.0), "PLANT": (0.0, 0.0, 0.0), "EH": (40.0, 0.0, 0.0),
         "TMP": (0.0, -40.0, 0.0), "ASM": (40.0, 40.0, 0.0)}
TOP = ["Generator", "Switchgear", "Control_Wiring", "Power_Cables", "Grounding", "Ehouse", "Cable_Tray",
       "Transformer", "Temporary_Power", "Assembly_Kit", "Annotations", "Cameras", "Lighting"]


def main(out_path=None):
    ss.reset()
    for n in TOP:                       # fixed, documented top-level order
        coll(n)
    ss.world()
    ss.render_settings(samples=128)
    ss.floor()
    L = mod_switchgear.Lineup(ZONES["SWG"]).build()
    G = mod_generator.Generator((-6.6, 0.0, 0.0)).build()
    G.kits_beside()
    P = mod_plant.Plant(G).build()
    E = mod_ehouse.EHouse(ZONES["EH"], bpy.data.objects["SWG_S1_Bay"]).build()
    T = mod_temp.TempPower(ZONES["TMP"]).build()
    B = mod_bench.Bench(ZONES["ASM"]).build()
    # lighting rigs per zone (only the rig of the active view renders)
    ss.light_rig("LGT_SWG", (2.3, 40.0, 1.0), radius=7, energy=1.0, collection="Lighting/LGT_SWG")
    ss.light_rig("LGT_PLANT", (1.0, 0.5, 1.5), radius=12, energy=2.2, collection="Lighting/LGT_PLANT")
    ss.light_rig("LGT_EH", (46.0, 1.5, 1.5), radius=14, energy=2.6, collection="Lighting/LGT_EH")
    ss.light_rig("LGT_TMP", (6.0, -40.0, 1.0), radius=14, energy=2.6, collection="Lighting/LGT_TMP")
    ss.light_rig("LGT_ASM", (40.9, 40.0, 1.0), radius=5, energy=0.5, collection="Lighting/LGT_ASM")
    views = define_views(dict(L=L, G=G, P=P, E=E, T=T, B=B))
    # cameras + callout anchor empties
    for key, v in views.items():
        camera(v["camera"], tuple(v["cam_loc"]), tuple(v["cam_target"]), lens=v["lens"],
               collection=coll("Cameras"))
        if v["callouts"]:
            c = coll(f"Annotations/CO_{key}")
            for co in v["callouts"]:
                e = empty(f"CO_{key}_{co['n']}", tuple(co["anchor"]), c, size=0.04)
                co["empty"] = e.name
    scene = bpy.context.scene
    scene["sw_views"] = json.dumps(views)
    # embed the control script (sidebar panel) and register it on load
    t = bpy.data.texts.new("sw_controls.py")
    t.from_string(open(os.path.join(HERE, "sw_controls.py")).read())
    t.use_module = True
    readme = os.path.join(HERE, "..", "..", "README.md")
    if os.path.exists(readme):
        bpy.data.texts.new("README.md").from_string(open(readme).read())
    import sw_controls
    sw_controls.apply_view("IEM_ControlKit", scene)
    out = out_path or os.path.join(HERE, "..", "Southwire_PGS_Master.blend")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out), compress=True)
    print("saved", os.path.abspath(out), "views:", len(views))
    return views


if __name__ == "__main__":
    main()
