"""Cable anatomy studio render: ARMOR-X MC-HL 15 kV 3/C 500 kcmil, cut back in steps.

Typical construction (customer list: 500-37 3/C CPRESS CU NL-EPR 25% T/S 1X#1 CU GW ARMOR-X MC-HL OR MV-105
15KV 133% RED PVC JACKET), modelled at true scale in metres:
- three cores: 37-strand compressed copper, semiconducting conductor shield, EPR insulation (133%), semiconducting
  insulation shield, helically applied copper tape shield; cores splay at the cut like a termination in progress;
- one #1 bare copper grounding conductor in the interstice, a polyester binder;
- continuously welded, annularly corrugated aluminium armor;
- red PVC jacket with the printed legend.
Studio: black sweep, large soft key, strip rim lights, a dark glossy floor.

    python blender/cable_anatomy.py --view hero|end|both --scale 25 --samples 64 --out renders/anatomy
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--view", default="both")
ap.add_argument("--scale", type=int, default=25)
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--out", default=os.path.join(PLANT, "renders", "anatomy"))
ap.add_argument("--anchors-only", action="store_true", help="write the layer anchor points (pixels) and stop")
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
os.makedirs(args.out, exist_ok=True)

IN = .0254
LEGEND = ("SOUTHWIRE®  ARMOR-X®  MC-HL  OR  MV-105   15 kV  133%   3/C 500 KCMIL CU  NL-EPR  25% T/S   "
          "1X#1 CU GW   CWA   RED PVC JACKET   SUNLIGHT RESISTANT   UL 2225   ")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92 for v in c) + (1,)


def mat(name, color, metal=0.0, rough=.4, coat=0.0, spec=.5, sss=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    return m


M = dict(
    copper=mat("copper", "#c97a4a", 1.0, .26),
    copper_tape=mat("copper tape", "#b8693e", 1.0, .33),
    semicon=mat("semicon", "#141414", 0.0, .55),
    epr=mat("EPR", "#b9a99a", 0.0, .5),
    binder=mat("binder", "#e9e6dc", 0.0, .5),
    alu=mat("aluminium", "#c9cdd0", 1.0, .24),
    floor=mat("floor", "#060607", 0.0, .55),
    sweep=mat("sweep", "#0e0f10", 0.0, .8),
)
# copper tape: overlapping helical tape edges as a bump pattern on object coordinates
nt = M["copper_tape"].node_tree
tc = nt.nodes.new("ShaderNodeTexCoord")
wv = nt.nodes.new("ShaderNodeTexWave")
wv.wave_type = "BANDS"
wv.bands_direction = "DIAGONAL"
wv.inputs["Scale"].default_value = 140
wv.inputs["Distortion"].default_value = 0
bp = nt.nodes.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = .12
nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
nt.links.new(wv.outputs["Fac"], bp.inputs["Height"])
nt.links.new(bp.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])


def jacket_material():
    """Red PVC with the white printed legend (image texture on the tube's UVs)."""
    from PIL import Image, ImageDraw, ImageFont
    W, H = 8192, 512
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-Bold.ttf"), 34)
    x = 40
    while x < W:
        d.text((x, 236), LEGEND, font=f, fill=(244, 240, 232, 255))
        x += d.textlength(LEGEND, font=f)
    p = os.path.join(args.out, "_legend.png")
    im.save(p)
    m = mat("PVC jacket", "#9a221b", 0.0, .42)
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(p)
    tex.extension = "REPEAT"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = lin("#9a221b")
    mix.inputs["B"].default_value = lin("#efe9de")
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    return m


M["jacket"] = jacket_material()


def tube(name, x0, x1, r_out, r_in, material, n=160, nx=None, prof=None, uv_len=None):
    """Lathe a tube along x: outer radius r_out(x) (or prof(x)), inner radius r_in, with annular end faces."""
    nx = nx or max(2, int((x1 - x0) / .0015))
    xs = [x0 + (x1 - x0) * k / nx for k in range(nx + 1)]
    ro = [prof(x) if prof else r_out for x in xs]
    verts, faces, uvs = [], [], []
    for i, x in enumerate(xs):
        for j in range(n):
            a = 2 * math.pi * j / n
            verts.append((x, ro[i] * math.cos(a), Z0 + ro[i] * math.sin(a)))
    base = len(verts)
    for i, x in enumerate((x0, x1)):
        for j in range(n):
            a = 2 * math.pi * j / n
            verts.append((x, r_in * math.cos(a), Z0 + r_in * math.sin(a)))
    for i in range(nx):
        for j in range(n):
            j2 = (j + 1) % n
            faces.append((i * n + j, i * n + j2, (i + 1) * n + j2, (i + 1) * n + j))
            if uv_len:
                u0, u1 = (xs[i] - x0) / uv_len, (xs[i + 1] - x0) / uv_len
                v0, v1 = 1 - j / n, 1 - (j + 1) / n
                uvs.append([(u0, v0), (u0, v1), (u1, v1), (u1, v0)])
    for side, i in ((0, 0), (1, nx)):                  # end annuli
        for j in range(n):
            j2 = (j + 1) % n
            a, b = i * n + j, i * n + j2
            c, d = base + side * n + j2, base + side * n + j
            faces.append((a, d, c, b) if side == 0 else (a, b, c, d))
            if uv_len:
                uvs.append([(0, 0)] * 4)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if uv_len:
        uv = me.uv_layers.new()
        k = 0
        for poly, quad in zip(me.polygons, uvs):
            for li, (u, v) in zip(poly.loop_indices, quad):
                uv.data[li].uv = (u, v)
    me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    return ob


def curve(name, pts, r, material, caps=True, res=6):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    cu.bevel_resolution = res
    cu.use_fill_caps = caps
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (q[0], q[1], q[2], 1)
    cu.materials.append(material)
    ob = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(ob)
    return ob


# ------------------------------------------------------------------ geometry (metres; cable along x, cut end at x=0)
Z0 = .075                                            # cable axis height above the floor
R_COND = .405 * IN                                   # 500 kcmil compressed
R_CSH = R_COND + .015 * IN                           # conductor shield
R_INS = R_CSH + .22 * IN                             # EPR 133% 15 kV
R_ISH = R_INS + .03 * IN                             # insulation shield
R_TAPE = R_ISH + .006 * IN                           # copper tape
RC = 2 * R_TAPE / math.sqrt(3) * 1.0                 # core centre radius (touching cores)
R_ASM = RC + R_TAPE                                  # cabled assembly
R_ARM_IN = R_ASM + .03 * IN
R_ARM = R_ARM_IN + .07 * IN                          # corrugated armor (crest)
R_JKT = R_ARM + .08 * IN
LAY = 1.10                                           # core lay length
X_END = -1.4
X_JKT, X_ARM, X_BND = -.215, -.150, -.132           # cut-back stations
SPLAY0 = -.125


def core_centre(k, x):
    a = 2 * math.pi * k / 3 + 2 * math.pi * x / LAY + .35
    s = 0.0
    if x > SPLAY0:
        t = (x - SPLAY0) / (0 - SPLAY0)
        s = .022 * t * t
    r = RC + s
    return Vector((x, r * math.cos(a), Z0 + r * math.sin(a)))


def core_path(k, x0, x1, n=None):
    n = n or max(4, int((x1 - x0) / .004))
    return [core_centre(k, x0 + (x1 - x0) * i / n) for i in range(n + 1)]


# jacket and armor (lathed, with corrugations)
tube("jacket", X_END, X_JKT, R_JKT, R_ARM + .002 * IN, M["jacket"], n=192,
     prof=lambda x: R_JKT + .012 * IN * (math.sin(2 * math.pi * x / (.25 * IN)) * .5 + .5), uv_len=16 * 2 * math.pi * R_JKT)
tube("armor", X_END + .02, X_ARM, R_ARM, R_ARM_IN, M["alu"], n=192,
     prof=lambda x: R_ARM_IN + .02 * IN + .05 * IN * (math.sin(2 * math.pi * x / (.25 * IN)) * .5 + .5))
tube("binder", X_END + .04, X_BND, R_ASM + .012 * IN, R_ASM - .002, M["binder"], n=160)
# stations along each core: tape, insulation shield, insulation, conductor shield, conductor
STAT = dict(tape=-.098, ish=-.082, ins=-.040, csh=-.032, cond=0.0)
for k in range(3):
    curve(f"core {k} tape", core_path(k, X_END + .05, STAT["tape"]), R_TAPE, M["copper_tape"])
    curve(f"core {k} ins shield", core_path(k, X_END + .05, STAT["ish"]), R_ISH, M["semicon"])
    curve(f"core {k} insulation", core_path(k, X_END + .05, STAT["ins"]), R_INS, M["epr"])
    curve(f"core {k} cond shield", core_path(k, STAT["ins"] - .01, STAT["csh"]), R_CSH, M["semicon"])
    # 37 strands: 1 + 6 + 12 + 18, alternating lay, from inside the insulation to the cut
    rs = R_COND / 7 * 1.02
    layers = [(0, 1), (2 * rs, 6), (4 * rs, 12), (6 * rs, 18)]
    xs0, xs1 = STAT["csh"] - .006, 0.0
    for li, (rl, n) in enumerate(layers):
        for j in range(n):
            pts = []
            for i in range(31):
                x = xs0 + (xs1 - xs0) * i / 30
                c = core_centre(k, x)
                a = 2 * math.pi * j / max(n, 1) + (1 if li % 2 else -1) * 2 * math.pi * x / .14
                pts.append(c + Vector((0, rl * math.cos(a), rl * math.sin(a))))
            curve(f"core {k} strand {li}.{j}", pts, rs, M["copper"], res=3)
# bare #1 ground in the interstice (7 strands), ends short of the cores
for j in range(7):
    pts = []
    for i in range(80):
        x = X_END + .05 + (-.06 - X_END - .05) * i / 79
        a = 2 * math.pi * 1.5 / 3 + 2 * math.pi * x / LAY + .35
        rg = RC * .62 + (0 if x < SPLAY0 else .012 * ((x - SPLAY0) / -SPLAY0) ** 2)
        c = Vector((x, rg * math.cos(a), Z0 + rg * math.sin(a)))
        rr = 0 if j == 0 else .0028
        b = 2 * math.pi * j / 6 + 2 * math.pi * x / .09
        pts.append(c + Vector((0, rr * math.cos(b), rr * math.sin(b))))
    curve(f"ground strand {j}", pts, .0014, M["copper"], res=3)

# ------------------------------------------------------------------ studio
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
bpy.context.object.data.materials.append(M["floor"])
# curved sweep behind
verts, faces = [], []
for i in range(41):
    t = i / 40
    a = t * math.pi / 2
    y, z = 1.2 + .6 * math.sin(a), .6 - .6 * math.cos(a)
    if i == 40:
        y, z = 1.8, .6
    verts += [(-3, y if i else 1.2, z), (3, y if i else 1.2, z)]
for i in range(40):
    faces.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
verts += [(-3, 1.8, .6), (3, 1.8, .6), (3, 1.8, 3), (-3, 1.8, 3)]
faces.append((len(verts) - 4, len(verts) - 3, len(verts) - 2, len(verts) - 1))
me = bpy.data.meshes.new("sweep")
me.from_pydata(verts, [], faces)
me.materials.append(M["sweep"])
sw = bpy.data.objects.new("sweep", me)
scene.collection.objects.link(sw)
world = bpy.data.worlds.new("w")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (.003, .003, .0035, 1)


def area(name, loc, target, size, energy, color=(1, 1, 1), shape="RECTANGLE", sy=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.shape = shape
    ld.size = size
    if sy:
        ld.size_y = sy
    ld.energy = energy
    ld.color = color
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = (Vector(loc) - Vector(target)).to_track_quat("Z", "Y").to_euler()
    scene.collection.objects.link(ob)
    return ob


area("key", (-.35, -.55, .75), (-.15, 0, Z0), 1.1, 38, (1, .97, .93), sy=.7)
area("rim right", (.45, .45, .35), (-.05, 0, Z0), .18, 22, (1, .95, .9), sy=1.4)
area("rim back", (-.6, .55, .28), (-.3, 0, Z0), .15, 16, (.9, .95, 1), sy=1.6)
area("fill", (.3, -.7, .12), (-.1, 0, Z0), .8, 5, (1, 1, 1))


def camera(name, loc, target, lens, focus, fstop):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.sensor_width = 36
    cam.clip_start = .01
    cam.dof.use_dof = True
    cam.dof.focus_distance = focus
    cam.dof.aperture_fstop = fstop
    ob = bpy.data.objects.new(name, cam)
    ob.location = loc
    ob.rotation_euler = (Vector(loc) - Vector(target)).to_track_quat("Z", "Y").to_euler()
    scene.collection.objects.link(ob)
    return ob


VIEWS = {
    # spread (17 x 11): the cable enters from the left page, the stepped end on the right page
    "hero": dict(cam=camera("hero", (.13, -.66, .215), (-.20, 0, Z0 + .045), 54, .68, 7.1), res=(5100, 3300)),
    # cover (letter portrait): the cut end face on, layers receding
    "end": dict(cam=camera("end", (.30, -.10, .15), (-.05, .01, Z0 + .048), 80, .34, 5.6), res=(2550, 3300)),
}
scene.render.engine = "CYCLES"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 10
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.film_transparent = False
# layer anchors for the brochure callouts: a point on each layer, projected to pixels for each view
from bpy_extras.object_utils import world_to_camera_view


def top(k, x, r):
    c = core_centre(k, x)
    return c + Vector((0, 0, r))


ANCH = {
    "conductor": core_centre(1, -.004) + Vector((0, 0, R_COND * .5)),
    "cond0": core_centre(0, 0.0), "cond1": core_centre(1, 0.0), "cond2": core_centre(2, 0.0),
    "cond_shield": top(1, (STAT["ins"] + STAT["csh"]) / 2, R_CSH),
    "insulation": top(1, (STAT["ish"] + STAT["ins"]) / 2, R_INS),
    "ins_shield": top(1, (STAT["tape"] + STAT["ish"]) / 2, R_ISH),
    "tape": top(1, (X_BND + STAT["tape"]) / 2 + .004, R_TAPE),
    "ground": Vector((-.075, 0, Z0)),
    "armor": Vector(((X_JKT + X_ARM) / 2, 0, Z0 + R_ARM)),
    "jacket": Vector((-.27, 0, Z0 + R_JKT)),
}
import json as _json
anchors = {}
for k, v in VIEWS.items():
    rx, ry = v["res"]
    scene.render.resolution_x, scene.render.resolution_y = rx, ry
    bpy.context.view_layer.update()
    anchors[k] = {}
    for n, p in ANCH.items():
        q = world_to_camera_view(scene, v["cam"], p)
        anchors[k][n] = [round(q.x * rx, 1), round((1 - q.y) * ry, 1)]
_json.dump(dict(res={k: v["res"] for k, v in VIEWS.items()}, anchors=anchors),
           open(os.path.join(args.out, "armorx_anchors.json"), "w"), indent=1)
if args.anchors_only:
    sys.exit(0)
for k in (["hero", "end"] if args.view == "both" else [args.view]):
    v = VIEWS[k]
    scene.camera = v["cam"]
    scene.render.resolution_x, scene.render.resolution_y = v["res"]
    scene.render.resolution_percentage = args.scale
    scene.render.filepath = os.path.join(args.out, f"armorx_{k}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", k, scene.render.filepath)
