"""Professional presentation look for the SK-3X1 Blender build (--style pro).

- Materials: procedural PBR per surface type. They include ribbed metal
  cladding (wave-texture bump), board-marked concrete, galvanised steel
  with roughness break-up, gravel, asphalt, porcelain, safety-yellow
  handrails and a chain-link fence. Hard-surface materials get a Bevel
  node, so edges catch the light.
- Landscape: grass with colour variation, clusters of trees outside the
  fence, and a public road to the main gate.
- Light: late-afternoon sun (elevation 24 deg) with a Nishita sky and
  soft sun disc.
- Cameras: perspective hero shots with real lenses and subtle depth of field.
- Compositor: atmospheric haze from the mist pass, fog glow, a slight lens
  dispersion and a warm grade; finish_pro.py adds the vignette and caption.

All of it is visual dressing; the model geometry is the verified one.
"""
import math
import random

import bpy
from mathutils import Vector

FT = 0.3048


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1,)


# surface type, colour (sRGB), roughness, metallic
LOOK = {
    "ground": ("gravel", "#857f72", .95, 0), "road": ("asphalt", "#3b3d3f", .9, 0),
    "gravel": ("gravel", "#8a867c", .95, 0), "corridor": ("gravel", "#928e83", .95, 0),
    "pad": ("concrete", "#a9a69e", .85, 0), "concrete": ("concrete", "#a6a39b", .85, 0),
    "basement": ("concrete", "#8f8c86", .9, 0), "future": ("gravel", "#b3afa4", .95, 0),
    "building": ("clad", "#c2bfb7", .55, .05), "hall": ("clad", "#aeb7bd", .45, .3),
    "roof": ("clad", "#9da5ab", .5, .3), "ehouse": ("clad", "#bfc4c2", .5, .1),
    "hrsg": ("clad", "#a2a8ab", .5, .4), "filter": ("clad", "#b8bec1", .5, .25),
    "windwall": ("clad", "#adb4b8", .5, .3), "tower": ("clad", "#b3bab7", .6, 0),
    "ccs": ("clad", "#d2d6d6", .55, .1), "acc": ("clad", "#c4c9cb", .5, .2),
    "partition": ("paint", "#e4e4df", .7, 0),
    "steel": ("galv", "#8e959a", .38, .85), "stair": ("galv", "#8a9196", .4, .8),
    "grating": ("galv", "#9aa1a5", .45, .8), "pipe": ("galv", "#a2a8ab", .35, .85),
    "copper": ("galv", "#9ea5a9", .35, .85), "fence": ("fence", "#8e959a", .4, .8),
    "copper_dark": ("paint", "#6f787d", .4, .5), "duct": ("paint", "#9ba2a6", .5, .4),
    "stack": ("paint", "#858c91", .55, .35), "machine": ("paint", "#8a9499", .4, .3),
    "xfmr": ("paint", "#7d898f", .42, .1), "radiator": ("fins", "#7b878d", .42, .15),
    "bundle": ("fins", "#8b9396", .45, .5), "fan": ("paint", "#5e666b", .45, .4),
    "fanhub": ("paint", "#3e4549", .45, .4), "motor": ("paint", "#3d6c8c", .35, .05),
    "pump": ("paint", "#3f6f8e", .35, .05), "tank": ("paint", "#dcdcd6", .45, 0),
    "rail": ("paint", "#dca21f", .4, 0), "crane": ("paint", "#e0b01a", .38, 0),
    "red": ("paint", "#b3342c", .4, 0), "amber": ("paint", "#d8a63a", .45, 0),
    "door": ("paint", "#4f6f86", .4, .1), "rollup": ("clad", "#9ca3a7", .5, .3),
    "louvre": ("fins", "#7c8489", .5, .3), "lamp": ("paint", "#f2efe4", .3, 0),
    "insulator": ("ceramic", "#6a3a28", .12, 0), "conductor": ("galv", "#aeb3b6", .3, .9),
    "water": ("water", "#2c464e", .04, 0), "conditional": ("paint", "#d9bd7b", .6, 0),
    "bess": ("paint", "#e3e5e3", .45, 0), "cabinet": ("paint", "#b9c1c6", .4, .1),
    "swgr": ("paint", "#a3adb3", .4, .1), "panel": ("paint", "#c9cfd2", .4, .1),
    "battery": ("paint", "#4c6b58", .5, 0), "equip": ("paint", "#b0b8bc", .5, .1),
}
_mats = {}


def _node(nt, t, loc, **inputs):
    n = nt.nodes.new(t)
    n.location = loc
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def material(key):
    if key in _mats:
        return _mats[key]
    kind, hexc, rough, metal = LOOK.get(key, LOOK["equip"])
    m = bpy.data.materials.new(f"pro {key}")
    m.use_nodes = True
    nt = m.node_tree
    L = nt.links
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    geo = _node(nt, "ShaderNodeNewGeometry", (-1400, 0))
    # colour break-up: large-scale noise darkens / lightens the base colour a few percent
    nz = _node(nt, "ShaderNodeTexNoise", (-1100, 300), Scale=.35, Detail=3.0)
    L.new(geo.outputs["Position"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-850, 300)
    ramp.color_ramp.elements[0].color = (.9, .9, .9, 1)
    ramp.color_ramp.elements[1].color = (1.06, 1.06, 1.06, 1)
    L.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    mix = _node(nt, "ShaderNodeMix", (-550, 300))
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 1
    mix.inputs[6].default_value = lin(hexc)
    L.new(ramp.outputs["Color"], mix.inputs[7])
    L.new(mix.outputs[2], b.inputs["Base Color"])
    normal_src = None
    if kind in ("clad", "fins", "louvre"):
        # ribs: wave bands on (x + y), so every wall orientation gets vertical ribs
        sep = _node(nt, "ShaderNodeSeparateXYZ", (-1200, -300))
        L.new(geo.outputs["Position"], sep.inputs[0])
        add = _node(nt, "ShaderNodeMath", (-1000, -300))
        add.operation = "ADD"
        L.new(sep.outputs["X"], add.inputs[0])
        L.new(sep.outputs["Y"], add.inputs[1])
        comb = _node(nt, "ShaderNodeCombineXYZ", (-800, -300))
        L.new(add.outputs[0], comb.inputs["X"])
        L.new(sep.outputs["Z"], comb.inputs["Z"])
        wave = _node(nt, "ShaderNodeTexWave", (-600, -300), Scale=(3.6 if kind == "clad" else 9.0),
                     Distortion=0.0, Detail=0.0)
        wave.bands_direction = "X"
        wave.wave_profile = "SAW" if kind != "clad" else "SIN"
        L.new(comb.outputs[0], wave.inputs["Vector"])
        bump = _node(nt, "ShaderNodeBump", (-350, -300), Strength=.35 if kind == "clad" else .5, Distance=.02)
        L.new(wave.outputs["Fac"], bump.inputs["Height"])
        normal_src = bump
    elif kind in ("concrete", "gravel", "asphalt"):
        vor = _node(nt, "ShaderNodeTexNoise" if kind != "gravel" else "ShaderNodeTexVoronoi", (-800, -300))
        if kind == "gravel":
            vor.inputs["Scale"].default_value = 90
        else:
            vor.inputs["Scale"].default_value = 28 if kind == "concrete" else 120
            vor.inputs["Detail"].default_value = 8
        L.new(geo.outputs["Position"], vor.inputs["Vector"])
        bump = _node(nt, "ShaderNodeBump", (-350, -300), Strength=.25 if kind == "concrete" else .45, Distance=.01)
        L.new(vor.outputs[0] if kind != "gravel" else vor.outputs["Distance"], bump.inputs["Height"])
        normal_src = bump
        # finer speckle into roughness
        if kind == "asphalt":
            L.new(nz.outputs["Fac"], b.inputs["Roughness"])
    elif kind == "galv":
        # spangle / weathering: roughness break-up
        vr = _node(nt, "ShaderNodeTexNoise", (-800, -150), Scale=2.5, Detail=6)
        L.new(geo.outputs["Position"], vr.inputs["Vector"])
        mr = _node(nt, "ShaderNodeMapRange", (-500, -150))
        mr.inputs["To Min"].default_value = rough - .12
        mr.inputs["To Max"].default_value = rough + .12
        L.new(vr.outputs["Fac"], mr.inputs["Value"])
        L.new(mr.outputs["Result"], b.inputs["Roughness"])
    elif kind == "water":
        b.inputs["Coat Weight"].default_value = 1
        wv = _node(nt, "ShaderNodeTexNoise", (-800, -300), Scale=6, Detail=2)
        L.new(geo.outputs["Position"], wv.inputs["Vector"])
        bump = _node(nt, "ShaderNodeBump", (-350, -300), Strength=.08)
        L.new(wv.outputs["Fac"], bump.inputs["Height"])
        normal_src = bump
    elif kind == "ceramic":
        b.inputs["Coat Weight"].default_value = .6
    elif kind == "fence":
        # chain-link reads as a light haze, not a wall
        b.inputs["Alpha"].default_value = .22
        m.blend_method = "HASHED"
    if kind in ("clad", "paint", "galv", "concrete", "fins", "ceramic"):
        bev = _node(nt, "ShaderNodeBevel", (-150, -500))
        bev.samples = 6
        bev.inputs["Radius"].default_value = .025
        if normal_src is not None:
            L.new(normal_src.outputs["Normal"], bev.inputs["Normal"])
        L.new(bev.outputs["Normal"], b.inputs["Normal"])
    elif normal_src is not None:
        L.new(normal_src.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = lin(hexc)
    _mats[key] = m
    return m


# ---------------------------------------------------------------------------
def landscape(scene, coll):
    """Grass surround, tree clusters outside the fence and the public road."""
    def mesh_obj(name, verts, faces, mat):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.materials.append(mat)
        ob = bpy.data.objects.new(name, me)
        coll.objects.link(ob)
        return ob

    grass = bpy.data.materials.new("pro grass")
    grass.use_nodes = True
    nt = grass.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = .95
    geo = _node(nt, "ShaderNodeNewGeometry", (-1200, 0))
    n1 = _node(nt, "ShaderNodeTexNoise", (-900, 200), Scale=.02, Detail=4)
    n2 = _node(nt, "ShaderNodeTexNoise", (-900, -100), Scale=1.5, Detail=8)
    nt.links.new(geo.outputs["Position"], n1.inputs["Vector"])
    nt.links.new(geo.outputs["Position"], n2.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-600, 200)
    ramp.color_ramp.elements[0].color = lin("#5f6e3c")
    ramp.color_ramp.elements[1].color = lin("#8d8f55")
    nt.links.new(n1.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = _node(nt, "ShaderNodeBump", (-400, -100), Strength=.3)
    nt.links.new(n2.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])

    S = 9000
    z = -.6 * FT
    mesh_obj("pro surround", [(-S * FT, -S * FT, z), ((2420 + S) * FT, -S * FT, z), ((2420 + S) * FT, (1920 + S) * FT, z),
                              (-S * FT, (1920 + S) * FT, z)], [(0, 1, 2, 3)], grass)
    # public road to the main gate (west), and a county road running north-south
    asphalt = material("road")
    mesh_obj("pro gate road", [(-900 * FT, 270 * FT, -.3 * FT), (0, 270 * FT, -.3 * FT), (0, 300 * FT, -.3 * FT),
                               (-900 * FT, 300 * FT, -.3 * FT)], [(0, 1, 2, 3)], asphalt)
    mesh_obj("pro county road", [(-930 * FT, -S * FT, -.3 * FT), (-890 * FT, -S * FT, -.3 * FT),
                                 (-890 * FT, (1920 + S) * FT, -.3 * FT), (-930 * FT, (1920 + S) * FT, -.3 * FT)],
             [(0, 1, 2, 3)], asphalt)

    # trees: three low-poly archetypes, instanced as linked duplicates
    bark = bpy.data.materials.new("pro bark")
    bark.use_nodes = True
    bark.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = lin("#4a3b2c")
    leaves = []
    for i, hx in enumerate(("#4e6a33", "#5b7236", "#43602f")):
        lm = bpy.data.materials.new(f"pro leaves {i}")
        lm.use_nodes = True
        lb = lm.node_tree.nodes["Principled BSDF"]
        lb.inputs["Base Color"].default_value = lin(hx)
        lb.inputs["Roughness"].default_value = .8
        lb.inputs["Subsurface Weight"].default_value = .15
        leaves.append(lm)
    protos = []
    rng = random.Random(1987)
    for i in range(3):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
        crown = bpy.context.active_object
        for v in crown.data.vertices:
            v.co *= 1 + rng.uniform(-.12, .12)
        crown.scale = (14 * FT, 14 * FT, (18 + 5 * i) * FT)
        crown.location = (0, 0, (30 + 4 * i) * FT)
        crown.data.materials.append(leaves[i])
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.2 * FT, depth=24 * FT, location=(0, 0, 12 * FT))
        trunk = bpy.context.active_object
        trunk.data.materials.append(bark)
        bpy.ops.object.select_all(action="DESELECT")
        crown.select_set(True)
        trunk.select_set(True)
        bpy.context.view_layer.objects.active = crown
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.join()
        proto = bpy.context.active_object
        bpy.ops.object.shade_smooth()
        proto.name = f"pro tree {i}"
        for c in proto.users_collection:
            c.objects.unlink(proto)
        protos.append(proto)
    placed = 0
    centres = [(rng.uniform(-1600, 4000), rng.uniform(-1600, 3500)) for _ in range(70)]
    for (cx, cy) in centres:
        n = rng.randint(4, 14)
        for _ in range(n):
            x, y = cx + rng.gauss(0, 90), cy + rng.gauss(0, 90)
            if -80 < x < 2500 and -80 < y < 2000:          # keep the compound and its margin clear
                continue
            if -960 < x < -860 or (-900 < x < 0 and 250 < y < 320):
                continue                                    # roads
            ob = bpy.data.objects.new("tree", protos[rng.randrange(3)].data)
            s = rng.uniform(.7, 1.35)
            ob.scale = (s, s, s * rng.uniform(.9, 1.2))
            ob.rotation_euler = (0, 0, rng.uniform(0, 6.28))
            ob.location = (x * FT, y * FT, -.6 * FT)
            coll.objects.link(ob)
            placed += 1
    # a windbreak row along the south and west fence lines
    for x in range(-60, 2480, 38):
        ob = bpy.data.objects.new("tree", protos[x % 3].data)
        ob.location = ((x + rng.uniform(-6, 6)) * FT, (-70 + rng.uniform(-8, 8)) * FT, -.6 * FT)
        s = rng.uniform(.8, 1.1)
        ob.scale = (s, s, s)
        coll.objects.link(ob)
        placed += 1
    return placed


def world_and_sun(scene, elevation=24, azimuth=258):
    """Late-afternoon sky and sun. azimuth: compass bearing the sun shines FROM."""
    world = bpy.data.worlds.new("pro world")
    scene.world = world
    world.use_nodes = True
    wn = world.node_tree.nodes
    bg = wn["Background"]
    sky = wn.new("ShaderNodeTexSky")
    sky.sky_type = "NISHITA"
    sky.sun_disc = True
    sky.sun_size = math.radians(1.2)
    sky.sun_elevation = math.radians(elevation)
    # Nishita rotation is measured from +X counter-clockwise; convert from a compass bearing
    sky.sun_rotation = math.radians(90 - azimuth)
    sky.air_density = 1.2
    sky.dust_density = 2.5
    world.node_tree.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = .14
    world.mist_settings.start = 120
    world.mist_settings.depth = 2200
    world.mist_settings.falloff = "QUADRATIC"
    sun = bpy.data.lights.new("pro sun", "SUN")
    sun.energy = 3.1
    sun.angle = math.radians(1.2)
    sun.color = (1.0, .9, .78)
    ob = bpy.data.objects.new("pro sun", sun)
    el, az = math.radians(elevation), math.radians(azimuth)
    towards_sun = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    ob.rotation_euler = towards_sun.to_track_quat("Z", "Y").to_euler()
    scene.collection.objects.link(ob)


def render_settings(scene, samples):
    c = scene.cycles
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = .02
    c.use_denoising = True
    c.max_bounces = 8
    c.diffuse_bounces = 4
    c.glossy_bounces = 4
    c.transparent_max_bounces = 8
    c.caustics_reflective = c.caustics_refractive = False
    c.sample_clamp_indirect = 8
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = -.3
    scene.render.use_freestyle = False
    scene.view_layers[0].use_pass_mist = True


def compositor(scene):
    scene.use_nodes = True
    nt = scene.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    L = nt.links
    rl = nt.nodes.new("CompositorNodeRLayers")
    rl.location = (-900, 0)
    # atmospheric perspective: blend toward the horizon haze with the mist pass
    mul = nt.nodes.new("CompositorNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = .28
    mul.location = (-650, -200)
    L.new(rl.outputs["Mist"], mul.inputs[0])
    haze = nt.nodes.new("CompositorNodeMixRGB")
    haze.location = (-450, 0)
    haze.inputs[2].default_value = (.80, .84, .88, 1)
    L.new(mul.outputs[0], haze.inputs["Fac"])
    L.new(rl.outputs["Image"], haze.inputs[1])
    glare = nt.nodes.new("CompositorNodeGlare")
    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.threshold = .9
    glare.mix = -.85
    glare.size = 8
    glare.location = (-250, 0)
    L.new(haze.outputs[0], glare.inputs["Image"])
    lens = nt.nodes.new("CompositorNodeLensdist")
    lens.use_fit = True
    lens.inputs["Distortion"].default_value = -.004
    lens.inputs["Dispersion"].default_value = .006
    lens.location = (-50, 0)
    L.new(glare.outputs["Image"], lens.inputs["Image"])
    # vignette is applied in finishing (finish_pro.py): smooth and resolution independent
    grade = nt.nodes.new("CompositorNodeColorBalance")
    grade.correction_method = "LIFT_GAMMA_GAIN"
    grade.lift = (1.0, 1.0, 1.02)
    grade.gamma = (1.0, 1.0, 1.0)
    grade.gain = (1.03, 1.0, .97)
    grade.location = (550, 0)
    L.new(lens.outputs["Image"], grade.inputs["Image"])
    comp = nt.nodes.new("CompositorNodeComposite")
    comp.location = (800, 0)
    L.new(grade.outputs["Image"], comp.inputs["Image"])


# Hero cameras: model feet (X east, Y north, Z up)
HEROES = [
    dict(k="P1", n="Aerial three-quarter, late afternoon", eye=(-160, -560, 640), target=(860, 560, 20), lens=36,
         show="base"),
    dict(k="P2", n="Transformer bays and filter houses from the access road", eye=(470, 238, 36),
         target=(1000, 372, 40), lens=30, show="base", dof=(320, 8.0)),
    dict(k="P3", n="HRSGs and stacks from the north-west", eye=(420, 1110, 130), target=(790, 690, 95), lens=34,
         show="base"),
    dict(k="P4", n="Air-cooled condenser and turbine hall", eye=(1760, 1140, 250), target=(1160, 560, 60), lens=32,
         show="base"),
    dict(k="P5", n="Full site with optional systems", eye=(-720, -980, 1650), target=(1260, 1020, 0), lens=30,
         show="all"),
    dict(k="P6", n="Carbon capture island (optional)", eye=(200, 1720, 420), target=(900, 1180, 120), lens=34,
         show="all"),
]


def hero_camera(scene, h):
    eye, tgt = Vector(h["eye"]) * FT, Vector(h["target"]) * FT
    cam = bpy.data.cameras.new(f"cam {h['k']}")
    cam.lens = h["lens"]
    cam.sensor_width = 36
    cam.clip_start, cam.clip_end = 1, 20000
    if "dof" in h:
        cam.dof.use_dof = True
        cam.dof.focus_distance = h["dof"][0] * FT
        cam.dof.aperture_fstop = h["dof"][1]
    ob = bpy.data.objects.new(f"cam {h['k']}", cam)
    ob.location = eye
    ob.rotation_euler = (eye - tgt).to_track_quat("Z", "Y").to_euler()
    scene.collection.objects.link(ob)
    return ob
