#!/usr/bin/env python3
"""Run render_views.py with the pip 'bpy' module (no Blender GUI/binary needed):
    python3 tools/run_bpy.py out/plant.blend -- --only 01 --scale 0.25 --samples 32 --device cpu"""
import sys, os, bpy
here = os.path.dirname(os.path.abspath(__file__)); plant = os.path.dirname(here)
blend = sys.argv[1]
extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
bpy.ops.wm.open_mainfile(filepath=os.path.abspath(blend))
sys.argv = ["render_views.py", "--"] + extra
g = {"__name__": "__main__", "__file__": os.path.join(plant, "render_views.py")}
exec(compile(open(os.path.join(plant, "render_views.py")).read(), "render_views.py", "exec"), g)
