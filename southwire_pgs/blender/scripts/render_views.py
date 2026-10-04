"""Batch-render saved views from the master .blend.

    python3 render_views.py [--preview] [--samples N] [VIEW ...]
    blender -b ../Southwire_PGS_Master.blend -P render_views.py -- [--preview] [VIEW ...]

Writes, per view:
    renders/clean/<VIEW>.png          (RGB, light studio background, no annotations)
    renders/clean/<VIEW>_alpha.png    (RGBA, transparent background, for re-layout)
    renders/clean/<VIEW>.json         (projected callout anchors in pixels)
--preview writes small, fast renders to renders/preview/ instead.
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402
import sw_controls  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BLEND = os.path.join(ROOT, "blender", "Southwire_PGS_Master.blend")
BG = (246, 247, 248)


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    preview = "--preview" in a
    samples = None
    if "--samples" in a:
        samples = int(a[a.index("--samples") + 1])
    names = [x for x in a if not x.startswith("--") and not x.isdigit()]
    return preview, samples, names


def composite(src, dst):
    from PIL import Image
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, BG + (255,))
    bg.alpha_composite(im)
    bg.convert("RGB").save(dst, dpi=(320, 320))


def main():
    preview, samples, names = args()
    if not bpy.data.filepath:
        bpy.ops.wm.open_mainfile(filepath=BLEND)
    scene = bpy.context.scene
    views = json.loads(scene["sw_views"])
    names = names or list(views.keys())
    outdir = os.path.join(ROOT, "renders", "preview" if preview else "clean")
    os.makedirs(outdir, exist_ok=True)
    if preview:
        scene.render.resolution_percentage = 30
        scene.cycles.samples = samples or 16
    else:
        scene.render.resolution_percentage = 100
        scene.cycles.samples = samples or 128
    for name in names:
        v = sw_controls.apply_view(name, scene)
        bpy.context.view_layer.update()
        cam = scene.camera
        rx = int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
        ry = int(scene.render.resolution_y * scene.render.resolution_percentage / 100)
        co = []
        for c in v.get("callouts", []):
            p = world_to_camera_view(scene, cam, Vector(c["anchor"]))
            co.append({"n": c["n"], "anchor_px": [p.x * rx, (1 - p.y) * ry], "label_norm": c["label"],
                       "in_frame": bool(0 <= p.x <= 1 and 0 <= p.y <= 1 and p.z > 0)})
        alpha = os.path.join(outdir, f"{name}_alpha.png")
        scene.render.filepath = alpha
        bpy.ops.render.render(write_still=True)
        composite(alpha, os.path.join(outdir, f"{name}.png"))
        with open(os.path.join(outdir, f"{name}.json"), "w") as f:
            json.dump({"view": name, "title": v["title"], "size": [rx, ry], "callouts": co}, f, indent=1)
        print("RENDERED", name, flush=True)


if __name__ == "__main__":
    main()
