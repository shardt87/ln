"""Cable cross-section icons: one studio render per cable family, cut back in steps and seen end-on at three-quarter,
on black, for the product cards and the product index.

Constructions are typical (layer order and proportions of each cable type), not catalog data. Every cable is built
straight along x with its cut end at x = 0; each layer stops a little further back than the one inside it.

    python blender/cable_icons.py [--only hv_xlpe,mv105] --px 1000 --samples 64 --out renders/icons
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
ap.add_argument("--only", default="")
ap.add_argument("--px", type=int, default=1000)
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--out", default=os.path.join(PLANT, "renders", "icons"))
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
os.makedirs(args.out, exist_ok=True)
IN = .0254


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92 for v in c) + (1,)


MATS = {}


def mat(key):
    spec = dict(copper=("#c97a4a", 1, .26), tape=("#b8693e", 1, .32), semicon=("#141414", 0, .55),
                xlpe=("#e9e6dc", 0, .3), epr=("#b9a99a", 0, .5), alu=("#c9cdd0", 1, .24), foil=("#d7dadc", 1, .18),
                pvc_black=("#1b1d1f", 0, .45), pvc_red=("#9a221b", 0, .42), cpe_yellow=("#d1a21c", 0, .5),
                hdpe=("#151617", 0, .35), filler=("#cfc6b2", 0, .7), binder=("#e9e6dc", 0, .5),
                ins_black=("#232527", 0, .4), ins_red=("#a3271f", 0, .4), ins_blue=("#244f8c", 0, .4),
                ins_white=("#e4e2da", 0, .4), ins_green=("#2f7a3c", 0, .4), ins_yellow=("#d6b22a", 0, .4))[key]
    if key not in MATS:
        m = bpy.data.materials.new(key)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = lin(spec[0])
        b.inputs["Metallic"].default_value = spec[1]
        b.inputs["Roughness"].default_value = spec[2]
        MATS[key] = m
    return MATS[key]


def cyl(name, x0, x1, r, m, cy=0.0, cz=0.0, n=96, r_in=0.0, corrugate=0.0):
    """Tube or rod along x centred on (cy, cz); corrugate = amplitude of annular corrugation (armor)."""
    nx = 2 if not corrugate else max(2, int((x1 - x0) / .0012))
    xs = [x0 + (x1 - x0) * i / nx for i in range(nx + 1)]
    rr = [r + (corrugate * (math.sin(2 * math.pi * x / (.25 * IN)) * .5 + .5) if corrugate else 0) for x in xs]
    V, F = [], []
    for i, x in enumerate(xs):
        for j in range(n):
            a = 2 * math.pi * j / n
            V.append((x, cy + rr[i] * math.cos(a), cz + rr[i] * math.sin(a)))
    for i in range(nx):
        for j in range(n):
            F.append((i * n + j, i * n + (j + 1) % n, (i + 1) * n + (j + 1) % n, (i + 1) * n + j))
    for end, i in ((0, 0), (1, nx)):
        b0 = len(V)
        if r_in > 0:
            for j in range(n):
                a = 2 * math.pi * j / n
                V.append((xs[i], cy + r_in * math.cos(a), cz + r_in * math.sin(a)))
            for j in range(n):
                q = (i * n + j, i * n + (j + 1) % n, b0 + (j + 1) % n, b0 + j)
                F.append(q if end else q[::-1])
        else:
            V.append((xs[i], cy, cz))
            for j in range(n):
                q = (i * n + j, i * n + (j + 1) % n, b0)
                F.append(q if end else q[::-1])
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], F)
    me.materials.append(m)
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def strands(x0, cy, cz, R, n_layers, m="copper", fine=False, x1=0.0):
    """Concentric stranded conductor of radius R: 1 + 6 + 12 + ... strands (fine: many small strands)."""
    if fine:
        rs = R / 9
        cyl("strand core", x0, x1, R * .25, mat(m), cy, cz, n=24)
        rings = [(R * f, int(2 * math.pi * R * f / (2 * rs))) for f in (.35, .55, .75, .9)]
    else:
        rs = R / (2 * n_layers - 1)
        cyl("strand", x0, x1, rs, mat(m), cy, cz, n=24)
        rings = [(2 * k * rs, 6 * k) for k in range(1, n_layers)]
    for (rr, n) in rings:
        for j in range(n):
            a = 2 * math.pi * j / n
            cyl("strand", x0, x1, rs * 1.02, mat(m), cy + rr * math.cos(a), cz + rr * math.sin(a), n=20)


def core(cy, cz, R, layers, step, x_start, strand_layers=4, fine=False, x0=-.5):
    """A conductor with its layers [(thickness, material)], each cut back one step further."""
    step *= 1.5
    strands(x_start - step * .6, cy, cz, R, strand_layers, fine=fine, x1=x_start)
    cyl("cond fill", x0, x_start - step * .6, R * .98, mat("copper"), cy, cz)
    r = R
    x = x_start
    for k, (t, m) in enumerate(layers):
        x -= step
        cyl(f"layer {m}", x0, x, r + t, mat(m), cy, cz, r_in=r * .999)
        r += t
    return r, x


def build(fam):
    """Families: radii in inches, layers inside-out. Returns overall diameter (m)."""
    for ob in list(bpy.context.scene.collection.objects):
        if ob.type == "MESH" and ob.name not in ("floor", "sweep"):
            bpy.data.objects.remove(ob)
    s = IN
    if fam == "hv_xlpe":                       # 230 kV 1/C 2500 kcmil Cu, XLPE, Cu wire shield, Al laminate, HDPE
        R = .95 * s
        r, x = core(0, 0, R, [(.05 * s, "semicon"), (.95 * s, "xlpe"), (.05 * s, "semicon")], .55 * s, 0,
                    strand_layers=6)
        x -= .5 * s
        for j in range(44):                    # copper wire screen
            a = 2 * math.pi * j / 44
            cyl("screen wire", -.5, x, .035 * s, mat("copper"), (r + .035 * s) * math.cos(a), (r + .035 * s) * math.sin(a), n=12)
        r += .07 * s
        x -= .4 * s
        cyl("Al laminate", -.5, x, r + .015 * s, mat("alu"), r_in=r)
        r += .015 * s
        x -= .35 * s
        cyl("HDPE jacket", -.5, x, r + .18 * s, mat("hdpe"), r_in=r)
        return 2 * (r + .18 * s)
    if fam == "mv105":                         # 15 kV 1/C 500 kcmil, EPR 133%, Cu tape, PVC
        r, x = core(0, 0, .405 * s, [(.015 * s, "semicon"), (.22 * s, "epr"), (.03 * s, "semicon"), (.008 * s, "tape")],
                    .42 * s, 0)
        x -= .4 * s
        cyl("jacket", -.5, x, r + .08 * s, mat("pvc_red"), r_in=r)
        return 2 * (r + .08 * s)
    if fam in ("armorx15", "armorx600"):
        if fam == "armorx15":
            Rc, lay, rr_ = .405 * s, [(.015 * s, "semicon"), (.22 * s, "epr"), (.03 * s, "semicon"), (.008 * s, "tape")], .3 * s
            cols = [None, None, None]
            jk = "pvc_red"
        else:
            Rc, rr_ = .26 * s, .3 * s
            cols = ["ins_black", "ins_red", "ins_blue"]
            jk = "pvc_black"
        rcore = Rc + (sum(t for t, _ in lay) if fam == "armorx15" else .045 * s)
        rc = 2 * rcore / math.sqrt(3)
        for k in range(3):
            a = math.pi / 2 + 2 * math.pi * k / 3
            L = lay if fam == "armorx15" else [(.045 * s, cols[k])]
            core(rc * math.cos(a), rc * math.sin(a), Rc, L, rr_, -.0 - k * .08 * s)
        rg = rc * .62
        core(rg * math.cos(-math.pi / 2), rg * math.sin(-math.pi / 2), .09 * s, [], .1, -.9 * s, strand_layers=2)
        ra = rc + rcore
        x = -(len(lay) + 1.6) * rr_ if fam == "armorx15" else -1.1 * s
        cyl("binder", -.5, x, ra + .01 * s, mat("binder"), r_in=ra * .98)
        x -= .25 * s
        cyl("armor", -.5, x, ra + .06 * s, mat("alu"), r_in=ra + .01 * s, corrugate=.05 * s)
        x -= .35 * s
        cyl("jacket", -.5, x, ra + .19 * s, mat(jk), r_in=ra + .11 * s)
        return 2 * (ra + .19 * s)
    if fam in ("tc_er", "vfd"):
        Rc = .2 * s if fam == "vfd" else .145 * s
        ins = .045 * s
        rcore = Rc + ins
        rc = 2 * rcore / math.sqrt(3)
        cols = ["ins_black", "ins_red", "ins_blue"] if fam == "tc_er" else ["ins_black", "ins_black", "ins_black"]
        for k in range(3):
            a = math.pi / 2 + 2 * math.pi * k / 3
            core(rc * math.cos(a), rc * math.sin(a), Rc, [(ins, cols[k])], .35 * s, -k * .1 * s, strand_layers=3)
        if fam == "tc_er":
            rg = rc * .78
            core(0, -rg, .1 * s, [(.03 * s, "ins_green")], .3 * s, -.6 * s, strand_layers=2)
        else:                                  # three symmetrical bare grounds in the interstices
            for k in range(3):
                a = -math.pi / 2 + 2 * math.pi * k / 3
                core(rc * .72 * math.cos(a), rc * .72 * math.sin(a), .07 * s, [], .1, -.5 * s, strand_layers=2)
        ra = rc + rcore
        x = -1.0 * s
        if fam == "vfd":
            cyl("overall Cu tape", -.5, x, ra + .01 * s, mat("tape"), r_in=ra)
            ra += .01 * s
            x -= .3 * s
        else:
            cyl("filler", -.5, x, ra, mat("filler"), r_in=ra * .4)
        cyl("jacket", -.5, x - .3 * s, ra + .08 * s, mat("pvc_black"), r_in=ra)
        return 2 * (ra + .08 * s)
    if fam == "pltc":                          # 4 pairs, overall foil + drain, PVC
        Rc, ins = .02 * s, .015 * s
        k = 0
        for p in range(4):
            a = 2 * math.pi * p / 4 + .4
            cy0, cz0 = .085 * s * math.cos(a), .085 * s * math.sin(a)
            for w, c in ((-1, "ins_black"), (1, "ins_white")):
                b = a + w * math.pi / 2
                core(cy0 + .037 * s * math.cos(b), cz0 + .037 * s * math.sin(b), Rc, [(ins, c)], .12 * s, -k * .02 * s,
                     strand_layers=2)
                k += 1
        core(0, 0, .015 * s, [], .1, -.2 * s, strand_layers=1)            # drain
        ra = .16 * s
        cyl("foil", -.5, -.45 * s, ra, mat("foil"), r_in=ra * .97)
        cyl("jacket", -.5, -.65 * s, ra + .045 * s, mat("pvc_black"), r_in=ra)
        return 2 * (ra + .045 * s)
    if fam == "pv":                            # 2 kV PV / RHW-2 1/C, XLPE
        r, x = core(0, 0, .405 * s, [(.09 * s, "ins_black")], .45 * s, 0)
        return 2 * r
    if fam == "shdgc":                         # 15 kV 3/C SHD-GC: shielded cores, 2 grounds, GC, yellow CPE
        Rc = .2 * s
        L = [(.012 * s, "semicon"), (.2 * s, "epr"), (.02 * s, "semicon"), (.01 * s, "tape")]
        rcore = Rc + sum(t for t, _ in L)
        rc = 2 * rcore / math.sqrt(3)
        for k in range(3):
            a = math.pi / 2 + 2 * math.pi * k / 3
            core(rc * math.cos(a), rc * math.sin(a), Rc, L, .2 * s, -k * .06 * s, fine=True)
        for k, a in enumerate((-math.pi / 2 + 1.05, -math.pi / 2 - 1.05)):
            core(rc * .7 * math.cos(a), rc * .7 * math.sin(a), .09 * s, [], .1, -.7 * s, fine=True)
        core(0, -rc * .62, .05 * s, [(.03 * s, "ins_yellow")], .2 * s, -.7 * s, strand_layers=2)
        ra = rc + rcore
        cyl("jacket", -.5, -1.6 * s, ra + .2 * s, mat("cpe_yellow"), r_in=ra * .98)
        return 2 * (ra + .2 * s)
    if fam == "type_w":                        # 2 kV 1/C 4/0 flexible: fine strands, EPDM, CPE
        r, x = core(0, 0, .3 * s, [(.08 * s, "ins_black"), (.1 * s, "pvc_black")], .4 * s, 0, fine=True)
        return 2 * r
    if fam == "bare_cu":                       # 4/0 19-strand bare copper
        strands(-.5, 0, 0, .26 * s, 3)
        return .52 * s
    raise ValueError(fam)


FAMS = ["hv_xlpe", "mv105", "armorx15", "armorx600", "tc_er", "vfd", "pltc", "pv", "shdgc", "type_w", "bare_cu"]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.resolution_x = scene.render.resolution_y = args.px
scene.render.film_transparent = True                 # icons composite on any page tone
world = bpy.data.worlds.new("w")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (.004, .004, .005, 1)
cam = bpy.data.cameras.new("cam")
cam.lens = 85
cam_ob = bpy.data.objects.new("cam", cam)
scene.collection.objects.link(cam_ob)
scene.camera = cam_ob
lights = []
for name, loc, size, e in (("key", (-.4, -.6, .8), 1.0, 1.0), ("rim", (.5, .5, .4), .2, .6), ("fill", (.6, -.5, -.2), .6, .2)):
    ld = bpy.data.lights.new(name, "AREA")
    ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    scene.collection.objects.link(ob)
    lights.append((ob, e))
for fam in (args.only.split(",") if args.only else FAMS):
    D = build(fam)
    # three-quarter end view, framed on the diameter
    d = D * 7.0
    eye = Vector((d * .78, -d * .48, d * .30))
    tgt = Vector((-D * .9, 0, 0))
    cam_ob.location = eye
    cam_ob.rotation_euler = (eye - tgt).to_track_quat("Z", "Y").to_euler()
    cam.dof.use_dof = True
    cam.dof.focus_distance = (eye - Vector((-D * .25, 0, 0))).length
    cam.dof.aperture_fstop = 14
    cam.clip_start = D * .3
    for ob, e in lights:
        ob.location = Vector(ob.location).normalized() * d * 1.6
        ob.rotation_euler = (Vector(ob.location) - tgt).to_track_quat("Z", "Y").to_euler()
        ob.data.energy = 55 * e * (d / .5) ** 2
    scene.render.filepath = os.path.join(args.out, f"{fam}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", fam, round(D / IN, 2), "in")
