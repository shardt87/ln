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
    "hrsg": ("clad", "#a2a8ab", .5, .4), "hrsg_b": ("clad", "#9aa1a4", .5, .4), "filter": ("clad", "#b8bec1", .5, .25),
    "windwall": ("clad", "#adb4b8", .5, .3), "tower": ("clad", "#b3bab7", .6, 0),
    "ccs": ("clad", "#d2d6d6", .55, .1), "acc": ("clad", "#c4c9cb", .5, .2),
    "partition": ("paint", "#e4e4df", .7, 0),
    "steel": ("galv", "#8e959a", .38, .85), "stair": ("galv", "#8a9196", .4, .8),
    "grating": ("galv", "#9aa1a5", .45, .8), "pipe": ("galv", "#a2a8ab", .35, .85),
    "copper": ("galv", "#9ea5a9", .35, .85), "fence": ("fence", "#8e959a", .4, .8), "barrier": ("fence", "#e2701f", .5, 0), "safety": ("paint", "#2f9a4a", .5, 0),
    "soil": ("gravel", "#7a6347", 1, 0), "timber": ("paint", "#9a7448", .8, 0), "ductcase": ("concrete", "#b4b0a6", .9, 0),
    "pvc_grey": ("paint", "#8f969a", .5, 0), "pvc_orange": ("paint", "#d0752a", .5, 0),
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
    "water": ("water", "#2c464e", .04, 0), "conditional": ("paint", "#aab2b6", .5, .1),   # real finish, not the drawing tint
    "bess": ("paint", "#e3e5e3", .45, 0), "cabinet": ("paint", "#b9c1c6", .4, .1),
    "swgr": ("paint", "#a3adb3", .4, .1), "panel": ("paint", "#c9cfd2", .4, .1),
    "battery": ("paint", "#4c6b58", .5, 0), "equip": ("paint", "#b0b8bc", .5, .1),
    # coastal variant (sheet 15): terminal, marine structures and vessels
    "tankwall": ("concrete", "#c9c5bb", .8, 0), "tankroof": ("paint", "#d9d8d2", .55, 0),
    "lngpipe": ("paint", "#e7e6e0", .5, 0), "seawater": ("paint", "#4d7d93", .45, .05),
    "pile": ("paint", "#4d4f4f", .6, .2), "rope": ("paint", "#d8cfa9", .8, 0),
    "hull": ("paint", "#23282d", .4, .15), "antifoul": ("paint", "#8a2d25", .5, 0),
    "deck": ("paint", "#6b4a3a", .6, 0), "super": ("paint", "#ecebe5", .4, 0),
    "glass": ("paint", "#1f2d36", .08, .2), "mosscover": ("paint", "#d7cfbd", .5, 0),
    "turf": ("paint", "#6d7c45", .95, 0),
    "tug": ("paint", "#b03a26", .45, 0), "sea": ("sea", "#27434c", .05, 0),
    "sand": ("gravel", "#c2b28f", .95, 0), "rock": ("concrete", "#6f6c66", .9, 0),
    "window": ("window", "#2c3a44", .06, .55),
    # fuel systems: gas lines in safety yellow, backup fuel oil in brown
    "fuelgas": ("paint", "#c9a12e", .4, 0), "fueloil": ("paint", "#6d4a30", .45, 0),
    "feedwater": ("galv", "#b7bdc0", .35, .8),      # insulated, aluminium-jacketed
    "cable": ("paint", "#1d2124", .55, 0), "ipb": ("galv", "#a9b0b4", .35, .8),
    "firewater": ("paint", "#a52a22", .45, 0), "waterline": ("paint", "#3a7480", .45, 0), "sign": ("paint", "#efefea", .35, 0), "label": ("paint", "#efefea", .4, 0),
    "hivis": ("paint", "#bfd424", .55, 0), "hivis_o": ("paint", "#e06a22", .55, 0), "hardhat": ("paint", "#f1f1ec", .3, 0),
    "workwear": ("paint", "#26324a", .7, 0), "skin": ("paint", "#b88c6c", .6, 0), "truck": ("paint", "#e4e6e7", .25, .1),
    "cable_mv": ("paint", "#141719", .78, 0), "cable_armor": ("paint", "#6a2720", .7, 0), "cable_tc": ("paint", "#151819", .78, 0),
    "cable_mc": ("galv", "#6d7377", .45, .6), "cable_inst": ("paint", "#26467a", .5, 0),
    "cable_tcx": ("paint", "#cfa818", .45, 0), "cable_fa": ("paint", "#a52e25", .5, 0),
    "cable_fo": ("paint", "#d36f22", .45, 0),
    "sw_red": ("paint", "#c41f27", .4, 0), "xlpe": ("paint", "#e4e0cf", .3, 0), "alu": ("galv", "#b3b8bc", .3, .85),
    "steel_dark": ("paint", "#3a4045", .45, .3), "tent": ("paint", "#eeeeea", .8, 0), "white_truck": ("paint", "#e9ebea", .3, 0),
}
_mats = {}
# materials kept clean: glass, lamps, people, signs, labels, cables and the like
WEATHER_SKIP = {"tent", "sw_red", "xlpe", "alu", "white_truck", "lamp", "sign", "label", "hivis", "hivis_o", "hardhat", "workwear", "skin", "glass",
                "window", "insulator", "rail", "cable_mv", "cable_armor", "cable_tc", "cable_mc", "cable_inst", "cable_tcx",
                "cable_fa", "cable_fo", "cable", "truck", "sea", "water"}


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
    base_out = mix.outputs[2]
    if kind in ("paint", "clad", "galv", "concrete", "fins", "louvre") and key not in WEATHER_SKIP:
        # weathering: grime near grade (splash zone, first ~2 m), vertical rain streaks, and light
        # rust bloom on bare / galvanised steel; all a few percent, varied by world position
        sep = _node(nt, "ShaderNodeSeparateXYZ", (-1200, 650))
        L.new(geo.outputs["Position"], sep.inputs[0])
        gnd = _node(nt, "ShaderNodeMapRange", (-1000, 650))
        gnd.inputs["From Min"].default_value = 0.0
        gnd.inputs["From Max"].default_value = 2.2
        gnd.inputs["To Min"].default_value = 0.55
        gnd.inputs["To Max"].default_value = 0.0
        L.new(sep.outputs["Z"], gnd.inputs["Value"])
        vm = _node(nt, "ShaderNodeVectorMath", (-1000, 820))
        vm.operation = "MULTIPLY"
        vm.inputs[1].default_value = (5.0, 5.0, .18)
        L.new(geo.outputs["Position"], vm.inputs[0])
        st = _node(nt, "ShaderNodeTexNoise", (-800, 820), Scale=1.0, Detail=4.0)
        L.new(vm.outputs[0], st.inputs["Vector"])
        sm = _node(nt, "ShaderNodeMapRange", (-600, 820))
        sm.inputs["From Min"].default_value = .55
        sm.inputs["From Max"].default_value = .75
        sm.inputs["To Min"].default_value = 0.0
        sm.inputs["To Max"].default_value = .32
        L.new(st.outputs["Fac"], sm.inputs["Value"])
        mx = _node(nt, "ShaderNodeMath", (-400, 700))
        mx.operation = "MAXIMUM"
        L.new(gnd.outputs["Result"], mx.inputs[0])
        L.new(sm.outputs["Result"], mx.inputs[1])
        grime = _node(nt, "ShaderNodeMix", (-250, 500))
        grime.data_type = "RGBA"
        grime.blend_type = "MULTIPLY"
        L.new(mx.outputs[0], grime.inputs["Factor"])
        L.new(base_out, grime.inputs[6])
        grime.inputs[7].default_value = (.42, .38, .33, 1)
        base_out = grime.outputs[2]
        if kind == "galv" or key in ("steel", "stair", "grating"):
            rn = _node(nt, "ShaderNodeTexNoise", (-800, 1000), Scale=1.6, Detail=8.0)
            L.new(geo.outputs["Position"], rn.inputs["Vector"])
            rm = _node(nt, "ShaderNodeMapRange", (-600, 1000))
            rm.inputs["From Min"].default_value = .64
            rm.inputs["From Max"].default_value = .78
            rm.inputs["To Min"].default_value = 0.0
            rm.inputs["To Max"].default_value = .45
            L.new(rn.outputs["Fac"], rm.inputs["Value"])
            rust = _node(nt, "ShaderNodeMix", (-100, 650))
            rust.data_type = "RGBA"
            rust.blend_type = "MIX"
            L.new(rm.outputs["Result"], rust.inputs["Factor"])
            L.new(base_out, rust.inputs[6])
            rust.inputs[7].default_value = (.23, .1, .04, 1)
            base_out = rust.outputs[2]
    L.new(base_out, b.inputs["Base Color"])
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
    elif kind == "sea":
        # open water: two wave scales in the bump, darker and bluer with depth of view
        b.inputs["IOR"].default_value = 1.333
        b.inputs["Coat Weight"].default_value = .3
        w1 = _node(nt, "ShaderNodeTexNoise", (-800, -300), Scale=.9, Detail=6, Roughness=.55)
        w2 = _node(nt, "ShaderNodeTexWave", (-800, -500), Scale=.35, Distortion=6, Detail=4)
        w2.bands_direction = "DIAGONAL"
        L.new(geo.outputs["Position"], w1.inputs["Vector"])
        L.new(geo.outputs["Position"], w2.inputs["Vector"])
        add = _node(nt, "ShaderNodeMath", (-550, -400))
        L.new(w1.outputs["Fac"], add.inputs[0])
        L.new(w2.outputs["Fac"], add.inputs[1])
        bump = _node(nt, "ShaderNodeBump", (-350, -300), Strength=.22, Distance=.12)
        L.new(add.outputs[0], bump.inputs["Height"])
        normal_src = bump
    elif kind == "window":
        # tinted glazing: dark, glossy, with a clear coat so it picks up the sky
        b.inputs["Coat Weight"].default_value = 1
        b.inputs["Coat Roughness"].default_value = .02
        b.inputs["Specular IOR Level"].default_value = .8
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
def landscape(scene, coll, coastal=None):
    """Grass surround, tree clusters outside the fence and the public road.
    coastal: the variant metadata of a sheet 15 overlay; the land then ends at the
    shoreline with a sand strip and a rock revetment, and the sea runs north."""
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
    north = 1920 + S if not coastal else coastal["shoreline_y"] - 30
    # grass all round, with a hole for the compound (its ground carries the stormwater pond)
    v = [(-S, -S), (2420 + S, -S), (2420 + S, north), (-S, north), (0, 0), (2420, 0), (2420, 1920), (0, 1920)]
    mesh_obj("pro surround", [(x * FT, y * FT, z) for (x, y) in v],
             [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], grass)
    if coastal:
        # the coast runs east-west north of the plant; the sea is to the north
        sh, sea = coastal["shoreline_y"], coastal["sea_level"]
        x0, x1 = -S * FT, (2420 + S) * FT
        mesh_obj("pro beach", [(x0, north * FT, z), (x1, north * FT, z), (x1, sh * FT, -.9 * FT), (x0, sh * FT, -.9 * FT)],
                 [(0, 1, 2, 3)], material("sand"))
        mesh_obj("pro revetment", [(x0, sh * FT, -.9 * FT), (x1, sh * FT, -.9 * FT), (x1, (sh + 45) * FT, (sea - 7) * FT),
                                   (x0, (sh + 45) * FT, (sea - 7) * FT)], [(0, 1, 2, 3)], material("rock"))
        far = 90000
        so = mesh_obj("pro sea", [(-far * FT, (sh + 5) * FT, sea * FT), (far * FT, (sh + 5) * FT, sea * FT),
                                  (far * FT, far * FT, sea * FT), (-far * FT, far * FT, sea * FT)], [(0, 1, 2, 3)],
                      material("sea"))
        so["shore_y"] = sh
        # the sea floor below the water keeps the shallows from reading as a void
        mesh_obj("pro seabed", [(-far * FT, (sh + 45) * FT, (sea - 7) * FT), (far * FT, (sh + 45) * FT, (sea - 7) * FT),
                                (far * FT, far * FT, (sea - 60) * FT), (-far * FT, far * FT, (sea - 60) * FT)],
                 [(0, 1, 2, 3)], material("sand"))
    # public road to the main gate (west), and a county road running north-south
    asphalt = material("road")
    mesh_obj("pro gate road", [(-900 * FT, 270 * FT, -.3 * FT), (0, 270 * FT, -.3 * FT), (0, 300 * FT, -.3 * FT),
                               (-900 * FT, 300 * FT, -.3 * FT)], [(0, 1, 2, 3)], asphalt)
    mesh_obj("pro county road", [(-930 * FT, -S * FT, -.3 * FT), (-890 * FT, -S * FT, -.3 * FT),
                                 (-890 * FT, north * FT, -.3 * FT), (-930 * FT, north * FT, -.3 * FT)],
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
            if 2420 < x < 3440 and -60 < y < 1440:         # BTM data-centre campus (design option)
                continue
            if coastal:
                tx0, tx1, ty0, ty1 = coastal.get("terminal") or (1150, 1450, 1900, 2700)
                if (y > coastal["shoreline_y"] - 90 or (tx0 - 60 < x < tx1 + 60 and ty0 - 60 < y)
                        or (1300 < x < 1650 and 1880 < y < 2700) or (2400 < x < 2500 and y < 2000)
                        or (1750 < x < 2500 and 1920 < y < 2000)):
                    continue                                # sea, beach, terminal plot, links and rights of way
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


def set_sun(scene, elevation, azimuth):
    """Re-aim the sky and the sun lamp (per-camera override)."""
    sky = next(n for n in scene.world.node_tree.nodes if n.type == "TEX_SKY")
    sky.sun_elevation = math.radians(elevation)
    sky.sun_rotation = math.radians(90 - azimuth)
    ob = bpy.data.objects["pro sun"]
    el, az = math.radians(elevation), math.radians(azimuth)
    towards_sun = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    ob.rotation_euler = towards_sun.to_track_quat("Z", "Y").to_euler()


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
         show="all"),
    dict(k="P2", n="Transformer bays and filter houses from the access road", eye=(470, 238, 36),
         target=(1000, 372, 40), lens=30, show="all", dof=(320, 8.0)),
    dict(k="P3", n="HRSGs and stacks from the north-west", eye=(420, 1110, 130), target=(790, 690, 95), lens=34,
         show="all"),
    dict(k="P4", n="Air-cooled condenser and turbine hall", eye=(1760, 1140, 250), target=(1160, 560, 60), lens=32,
         show="all"),
    dict(k="P5", n="Full site with optional systems", eye=(-720, -980, 1650), target=(1260, 1020, 0), lens=30,
         show="all"),
    dict(k="P6", n="Carbon capture island (optional)", eye=(200, 1720, 420), target=(900, 1180, 120), lens=34,
         show="all"),
    # complete-plant angles (not on the board)
    dict(k="P7", n="Complete plant from the north-east", eye=(3100, 2700, 900), target=(1150, 900, 40), lens=32,
         show="all"),
    dict(k="P8", n="Complete plant from the south-east", eye=(3000, -700, 700), target=(1150, 950, 40), lens=32,
         show="all"),
    dict(k="P9", n="Complete plant from overhead", eye=(1210, 180, 4300), target=(1210, 900, 0), lens=34,
         show="all"),
    dict(k="P11", n="Modular power yard: RICE engine hall and simple-cycle units", eye=(1420, 330, 560),
         target=(2060, 940, 20), lens=30, show="all"),
    dict(k="P10", n="Complete plant from the south gate road", eye=(1200, -640, 240), target=(1200, 900, 70),
         lens=26, show="all"),
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

# Coastal variant (sheet SK-3X1-15). Morning sun from the south-east so the sea-side
# views are front lit. A: onshore import terminal and jetty; B: FSRU ~21,000 ft offshore.
COASTAL_A = [
    dict(k="C1", n="Onshore LNG import terminal beside the plant", eye=(4750, -1150, 1050),
         target=(2700, 950, 40), lens=30, show="coastal"),
    dict(k="C2", n="LNG carrier at the berth, unloading arms connected", eye=(5190, 640, 58), target=(5470, 1010, 48), lens=28,
         show="coastal"),
    dict(k="C3", n="LNG tank, regasification and send-out", eye=(2350, 120, 190), target=(3150, 950, 70),
         lens=30, show="coastal"),
    dict(k="C4", n="Plant, terminal and jetty from overhead", eye=(1250, 300, 7000), target=(1250, 2450, 0),
         lens=30, show="coastal", site=True),
    dict(k="C5", n="Jetty trestle from the tank roof", eye=(3190, 1150, 190), target=(5400, 960, 40), lens=32,
         show="coastal"),
    dict(k="C6", n="HP send-out pumps and the LNG tank with its deluge rings", eye=(2800, 352, 15),
         target=(2965, 560, 22), lens=24, show="coastal"),
    dict(k="C7", n="Berth: unloading arms with emergency-release couplers, crew, the carrier alongside",
         eye=(5346, 815, 40), target=(5420, 985, 46), lens=24, show="coastal"),
    dict(k="C8", n="Everything: plant, LNG satellite and marine terminal, BTM data centre", eye=(4300, -900, 2300),
         target=(1700, 1750, 20), lens=28, show="everything", site=True),
    # cover shots (deck cover panel, ~1.07:1): the story from the sea to the data centre
    dict(k="K1", n="LNG by sea, the 3x1 plant, the BTM data centre", eye=(-820, -620, 1450),
         target=(1600, 1950, 40), lens=30, show="everything", site=True, res=(2400, 2240)),
    dict(k="K2", n="LNG by sea, the 3x1 plant, the BTM data centre", eye=(3950, -650, 1100),
         target=(1400, 2050, 50), lens=30, show="everything", site=True, res=(2400, 2240)),
    dict(k="K3", n="LNG by sea, the 3x1 plant, the BTM data centre", eye=(1500, -1700, 950),
         target=(1550, 1850, 80), lens=28, show="everything", site=True, res=(2400, 2240)),
]
COASTAL_B = [
    dict(k="F1", n="FSRU and LNG carrier, ship-to-ship transfer", eye=(25300, -300, 300), target=(24300, 950, 40),
         lens=32, show="coastal"),
    dict(k="F2", n="Landfall valve station and plant from the sea", eye=(4900, 2900, 700), target=(2300, 900, 20),
         lens=30, show="coastal"),
    dict(k="F3", n="FSRU 6.4 km offshore, the plant on the horizon", eye=(27800, 1500, 150), target=(1400, 950, 70),
         lens=70, show="coastal"),
]


# Epic set: golden hour (sun 11 deg, from the west-south-west), low and dramatic viewpoints,
# wide lenses near the ground and long lenses for compression.
# the data centre's three supply paths, as numbered callouts on the captioned plates (x, y, z ft, number, text, colour)
BTM_CALLOUTS = [
    (3050, 506, 16, "1", "BACKUP · 36 GENSETS (130 MW) + 40 MW BATTERY", "#3d5a73"),
    (2685, 470, 12, "1", "ISLANDED BTM POWER · BTM BATTERY 40 MW / 80 MWh", "#3d5a73"),
    (2590, 880, 18, "1", "ISLANDED 34.5 kV BUS · SWITCHGEAR, TRANSFER SCHEME", "#3d5a73"),
    (2547, 790, 22, "2", "FROM THE MODULAR YARD · 3 × 90 MVA STEP-UPS (N+1)", "#4f8a5b"),
    (1955, 890, 16, "2", "MODULAR YARD 13.8 kV COLLECTOR · SUPPLIES THE CAMPUS", "#4f8a5b"),
    (2652, 788, 36, "3", "GRID TIE 230 kV · NORMALLY OPEN", "#b0573f"),
]
EPIC = [
    dict(k="E1", n="The three HRSG stacks from beside the absorbers", eye=(700, 1100, 150), target=(790, 780, 110), lens=24,
         show="all"),
    dict(k="E2", n="Long lens from the west road: stacks and absorbers stacked up", eye=(-1500, 880, 120),
         target=(800, 1000, 130), lens=135, show="all"),
    dict(k="E3", n="Low pass over the air-cooled condenser", eye=(1500, 300, 165), target=(1100, 800, 90),
         lens=20, show="all"),
    dict(k="E4", n="Along the 230 kV switchyard at eye level", eye=(560, 150, 7), target=(1600, 175, 40),
         lens=35, show="all"),
    dict(k="E5", n="Beneath the carbon-capture absorbers", eye=(880, 1115, 6), target=(790, 1220, 210), lens=16,
         show="all"),
    dict(k="E6", n="Drone dive over the power block", eye=(820, 330, 560), target=(800, 660, 0), lens=20,
         show="all"),
    dict(k="E7", n="Into the sun: the plant in silhouette across the fields", eye=(1926, 3519, 110),
         target=(900, 700, 330), lens=40, show="all"),
    dict(k="E8", n="RICE engine hall stacks at golden hour", eye=(1545, 905, 10), target=(1700, 1045, 30),
         lens=24, show="all"),
    dict(k="E9", n="Water tanks and their spiral stairs", eye=(690, 1662, 12), target=(525, 1590, 30), lens=24,
         show="all"),
    dict(k="E10", n="EV charging carport and the admin building", eye=(150, 98, 6), target=(215, 330, 12),
         lens=28, show="all"),
    dict(k="E11", n="Plant gas yard: metering, regulation, heater and filter-separators", eye=(1800, 1428, 34),
         target=(1688, 1522, 2), lens=26, show="all"),
    dict(k="E12", n="Pipeline M&R station: pig receiver, filter-separator and line heaters", eye=(1572, 1792, 24),
         target=(1640, 1858, 3), lens=24, show="all"),
    dict(k="E13", n="Fuel systems from above: M&R station, gas yard and the ULSD backup area", eye=(1260, 1300, 260),
         target=(1620, 1640, 0), lens=30, show="all"),
    dict(k="E14", n="RICE engine hall: exhaust trains, SCRs and 90 ft stacks", eye=(1840, 955, 26),
         target=(1700, 1035, 24), lens=24, show="all"),
    dict(k="E15", n="Simple-cycle units: filter house, enclosure, SCR and 80 ft stack", eye=(2085, 1120, 30),
         target=(2010, 1205, 16), lens=24, show="all"),
    dict(k="E16", n="Portable power pad: trailer turbines and containerized gensets", eye=(1925, 615, 30),
         target=(2085, 470, 6), lens=24, show="all"),
    dict(k="E17", n="Fuel cells, microturbines and the simple-cycle units", eye=(1872, 1345, 24),
         target=(2030, 1262, 5), lens=24, show="all"),
    dict(k="E18", n="Process pipes: fuel gas, fuel oil and feedwater crossing the east spine road", eye=(1395, 795, 48),
         target=(1500, 900, 6), lens=26, show="all"),
    dict(k="E19", n="GSUs facing the switchyard: HV bushings, arresters and take-off gantries", eye=(705, 255, 34),
         target=(640, 340, 22), lens=24, show="all"),
    dict(k="E20", n="The complete 230 kV switchyard: six breaker-and-a-half diameters", eye=(2140, 15, 95),
         target=(1450, 160, 10), lens=28, show="all"),
    # turbine-hall cutaways: walls and roofs hidden for these renders
    dict(k="E21", n="Turbine hall cutaway: the three H-class GTs and generators on the EL 20 deck", eye=(552, 470, 72),
         target=(720, 497, 25), lens=24, show="all", hide=("Common turbine hall",), hide_layers=("HALL_ROOF",)),
    dict(k="E22", n="GT1 close-up: compressor, combustor cans, fuel manifold, lube-oil and cable drops", eye=(604, 466, 46),
         target=(634, 506, 28), lens=24, show="all", hide=("Common turbine hall",), hide_layers=("HALL_ROOF",)),
    dict(k="E23", n="Cable trays along the hall north wall and their drops to the GT skids", eye=(574, 528, 52),
         target=(800, 546, 29), lens=22, show="all", hide=("Common turbine hall",), hide_layers=("HALL_ROOF",)),
    dict(k="E24", n="Isolated-phase bus: generator terminals, GCB, UAT tap and GSU", eye=(694, 326, 42),
         target=(636, 384, 21), lens=24, show="all", hide=("Common turbine hall",), hide_layers=("HALL_ROOF",)),
    dict(k="E25", n="South gallery: excitation cubicles, excitation transformer, IPB cubicles, GCB and cable drops",
         eye=(596, 388, 52), target=(646, 396, 4), lens=20, show="all", hide=("Common turbine hall",),
         hide_layers=("HALL_ROOF",)),
    dict(k="E51", n="Steam turbine: combined reheat valves, LP admission, turning gear, EHC unit and gland-steam condenser",
         eye=(1112, 414, 52), target=(1058, 492, 26), lens=24, show="all", hide=("Common turbine hall",),
         hide_layers=("HALL_ROOF",)),
    dict(k="E52", n="GT1 generator end: seal-oil / H2 gas-control skid, compressor bleed lines and blow-off valves",
         eye=(590, 462, 40), target=(616, 432, 23), lens=24, show="all", hide=("Common turbine hall",),
         hide_layers=("HALL_ROOF",)),
    dict(k="E53", n="South gallery: GT1 static starter (LCI) lineup and isolation transformer, deck stair",
         eye=(744, 402, 15), target=(708, 387, 4), lens=22, show="all", hide=("Common turbine hall",),
         hide_layers=("HALL_ROOF",)),
    dict(k="E54", n="Modular-yard cable pull: open manhole MH-A, davit and reel trailer",
         eye=(1684, 927, 26), target=(1718, 955, 1), lens=26, show="all"),
    dict(k="E55", n="Open trench over the 13.8 kV collector bank: trench box, excavator, crew",
         eye=(1780, 936, 24), target=(1808, 961, -3), lens=24, show="all"),
    dict(k="E56", n="CCS absorber A: bed manways, intercooler skid, tray riser, platform lights",
         eye=(712, 1150, 150), target=(655, 1215, 110), lens=28, show="all"),
    dict(k="E57", n="CCS T-1 / T-2: 230 kV cable terminations, jumpers to the bushings, firewall; tray riser at the VFD building",
         eye=(1300, 1085, 55), target=(1250, 1020, 20), lens=26, show="all"),
    dict(k="E60", n="230 kV XLPE cable termination: cleated risers, sealing ends, surge arresters, bonding link box",
         eye=(1740, 201, 10), target=(1757, 177, 13), lens=22, show="all", sun=(32, 330)),
    dict(k="E62", n="BESS PCS / MV skid: 34.5 kV elbow terminations to the collector circuit",
         eye=(1618.5, 483.5, 5.4), target=(1610, 490, 3.3), lens=26, show="all", sun=(24, 95)),
    dict(k="E64", n="Modular yard: the SIMpull Truck brings the feeder reels to the 13.8 kV cable pull",
         eye=(1702, 906, 7.5), target=(1752, 944, 5), lens=24, show="all", sun=(26, 215)),
    dict(k="E65", n="BESS yard: crew pulling 1,500 V DC conductor into the precast trench, containers either side",
         eye=(1764, 542.5, 9.5), target=(1718, 535, -0.5), lens=26, show="all", sun=(34, 150)),
    dict(k="E66", n="Turbine hall, GT1 outage: new 13.8 kV feeder pulled from the laydown bay up into the EL 48 MV tray",
         eye=(517, 484, 12.5), target=(549, 537, 23), lens=22, show="all", hide=("Common turbine hall",),
         hide_layers=("HALL_ROOF",), sun=(40, 200)),
    dict(k="E67", n="Turbine hall tray stack: ARMOR-X and MV-105, the legend on every jacket",
         eye=(603, 542.2, 50.6), target=(632, 544.2, 47.2), lens=30, show="all",
         hide_layers=("HALL_ROOF",), sun=(62, 175), dof=(7, 2.8)),
    dict(k="E58", n="Cable reel yard: SIMpull Truck unloading SIMpull Reels on payoffs, reel rows",
         eye=(214, 702, 15), target=(160, 752, 6), lens=28, show="base"),
    dict(k="E26", n="HRSG 1 west wall: buckstays, SCR doors, ammonia injection grid, downcomers, blowdown tank",
         eye=(452, 905, 92), target=(628, 690, 52), lens=28, show="all"),
    dict(k="E27", n="HRSG roofs: drums, risers, safety valves and silencers, steam leads", eye=(560, 618, 122),
         target=(645, 705, 92), lens=24, show="all"),
    dict(k="E28", n="HRSG 1 stack: breeching joint, CEMS probes and sample line, caged ladder, CEMS shelter",
         eye=(712, 900, 128), target=(632, 792, 70), lens=30, show="base"),
    dict(k="E29", n="HRSG 3 cutaway: tube harps, headers and the SCR / CO catalyst in gas-flow order",
         eye=(872, 560, 96), target=(950, 684, 34), lens=24, show="all", hide=("HRSG 3 + SCR",),
         sun=(42, 200)),
    dict(k="E30", n="Access road by the turbine hall: crews, pickups, mobile crane, hydrants and GSU deluge",
         eye=(520, 268, 9), target=(760, 330, 18), lens=28, show="all"),
    dict(k="E31", n="Switchyard bay D2: breakers with mechanisms, disconnect blades, trench to the relay house",
         eye=(862, 102, 30), target=(905, 160, 14), lens=24, show="all"),
    dict(k="E32", n="Station electrical: R2 e-houses with stairs and cable entries, unit transformers, manholes",
         eye=(512, 596, 20), target=(568, 642, 7), lens=24, show="all"),
    dict(k="E33", n="Emergency diesel generators beside the turbine-hall gallery", eye=(498, 312, 18),
         target=(450, 346, 9), lens=24, show="all"),
    dict(k="E34", n="ACC south-east corner: street risers, wind wall, stair tower, fan bells under the deck", eye=(1506, 322, 58),
         target=(1388, 470, 92), lens=24, show="all"),
    dict(k="E35", n="Tank farm: raw, fire / service and demineralised water tanks, headers, fire pump house",
         eye=(668, 1668, 46), target=(560, 1578, 14), lens=24, show="all"),
    dict(k="E36", n="Ammonia storage and the auxiliary boiler: bund, scrubber, safety shower, burner and FD fan",
         eye=(866, 1418, 34), target=(915, 1478, 16), lens=24, show="all"),
    dict(k="E37", n="Main gate and gatehouse: barrier arms, card readers, CCTV, entrance sign, control / admin building",
         eye=(352, 246, 34), target=(240, 322, 6), lens=24, show="all"),
    dict(k="E38", n="Warehouse and workshop yard: dumpsters, stock racks, gas-cylinder cage, delivery flatbed",
         eye=(96, 690, 40), target=(190, 585, 6), lens=24, show="all"),
    dict(k="E39", n="Carbon capture train A: flue duct into the DCC, booster fan, overhead duct to the absorber, amine rack",
         eye=(515, 1290, 105), target=(655, 1075, 30), lens=24, show="all"),
    dict(k="E40", n="Regenerators: strippers with overhead lines, reboilers, reflux drums, CO2 header to compression",
         eye=(1335, 1075, 85), target=(1140, 1195, 55), lens=24, show="all", sun=(28, 140)),
    dict(k="E41", n="BESS aisle: containers with rack doors and vents, PCS / MV skids, DC trenches, collector feeders",
         eye=(1548, 596, 28), target=(1672, 538, 4), lens=24, show="all"),
    dict(k="E42", n="BESS collector e-house, main power transformer and EMS, with the container rows behind",
         eye=(1700, 318, 42), target=(1800, 420, 8), lens=24, show="all"),
    dict(k="E43", n="GT inlet chilling: chiller building, CW pumps and e-house, the chiller cooling tower behind",
         eye=(345, 1015, 58), target=(175, 1195, 16), lens=24, show="all"),
    dict(k="E44", n="Inlet-chilling tower: fans, louvres, stair, CHW pumps and the TES tank",
         eye=(22, 1372, 72), target=(185, 1235, 18), lens=24, show="all"),
    dict(k="E45", n="LNG satellite: unloading arms, ambient vaporizers, vacuum-jacketed tanks in the impoundment",
         eye=(1862, 1655, 58), target=(2075, 1790, 6), lens=24, show="all"),
    dict(k="E46", n="Green hydrogen: electrolyzer building, dryer, compressors, tube banks, T-H2",
         eye=(1985, 1612, 72), target=(2215, 1500, 4), lens=24, show="all"),
    dict(k="E47", n="BTM data centre: two data halls with rooftop dry coolers, BESS, gensets, modular yard beside",
         eye=(2380, 140, 340), target=(2900, 900, 20), lens=24, show="dc", callouts=[c for c in BTM_CALLOUTS if "34.5 kV BUS" not in c[4]]),
    dict(k="E48", n="BTM substation: 13.8/34.5 kV step-ups, 230 kV tie (normally open), switchgear, BTM BESS",
         eye=(2470, 700, 60), target=(2610, 830, 12), lens=24, show="dc", callouts=BTM_CALLOUTS),
    dict(k="E49", n="Stormwater detention pond: grass banks, permanent pool, forebay berm, ramp, pump station",
         eye=(345, 1395, 95), target=(160, 1560, -6), lens=24, show="all"),
    dict(k="E50", n="Wastewater treatment: equalization basin, neutralization, clarifier, sludge tank, press building",
         eye=(800, 1405, 78), target=(680, 1490, 4), lens=24, show="all"),
]


def hero_set(coastal=None, name=""):
    """Cameras, sun (elevation, azimuth) and sheet reference for the scene being rendered."""
    if name == "epic":
        return dict(heroes=EPIC, sun=(11, 250), sheet="SK-3X1")
    if not coastal:
        return dict(heroes=HEROES, sun=(24, 258), sheet="SK-3X1")
    heroes = COASTAL_A if coastal["variant"] == "A" else COASTAL_B
    t = coastal.get("transform")
    if t:                                   # cameras are framed on sheet 15; rotate them onto the site
        f = lambda p: (t["c"] - p[1], p[0] - t["d"], p[2])
        heroes = [h if h.get("site") else dict(h, eye=f(h["eye"]), target=f(h["target"])) for h in heroes]
    return dict(heroes=heroes, sun=(28, 140), sheet="SK-3X1-15")
