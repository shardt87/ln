"""Procedurally generate a coal-fired power plant in Blender.

The scene is built from a single surface-of-revolution helper plus boxes, so
everything is created with direct mesh data (no edit-mode operators). That
keeps it reproducible in headless/background runs.

Usage with a Blender install:

    blender -b -P blender/power_plant.py -- --obj power_plant.obj

Usage with the ``bpy`` pip module (``pip install bpy``):

    python3 blender/power_plant.py --obj power_plant.obj

The exported OBJ feeds straight into this repo's line renderer via
``ln.LoadOBJ`` -- see examples/suzanne.go for the pattern.
"""

import argparse
import math
import sys

import bpy
from mathutils import Vector

TAU = math.pi * 2.0

# Scales every segment/ring count. Lower it for line-art exports (see --detail).
DETAIL = 1.0
STEAM = True


def seg(count, minimum=6):
    """Segment count scaled by the global detail level."""
    return max(minimum, int(round(count * DETAIL)))


# ---------------------------------------------------------------------------
# scene plumbing
# ---------------------------------------------------------------------------


def reset_scene():
    """Delete every object plus the data blocks they leave behind."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in (bpy.data.meshes, bpy.data.materials,
                       bpy.data.cameras, bpy.data.lights):
        for block in list(collection):
            if block.users == 0:
                collection.remove(block)


def make_material(name, color, roughness=0.8, metallic=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    if mat.node_tree is None:
        mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        # 'BLENDED' in 4.2+, 'BLEND' before that; the property is gone in some
        # newer builds, where alpha blending is the default anyway.
        for value in ("BLENDED", "BLEND"):
            try:
                mat.blend_method = value
                break
            except (AttributeError, TypeError):
                continue
    return mat


def new_object(name, verts, faces, material=None, smooth=False):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    if smooth:
        mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if material is not None:
        obj.data.materials.append(material)
    bpy.context.scene.collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------


def box(name, size, center, material=None):
    """Axis-aligned box given its full size and its center."""
    sx, sy, sz = (s / 2.0 for s in size)
    cx, cy, cz = center
    verts = [(cx + x * sx, cy + y * sy, cz + z * sz)
             for x, y, z in ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                             (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_object(name, verts, faces, material)


def revolve(name, profile, segments=48, center=(0.0, 0.0), material=None,
            cap_bottom=True, cap_top=True, smooth=True):
    """Build a surface of revolution from a bottom-to-top ``(z, radius)`` profile.

    A radius of 0 collapses that ring to a single point, so the same helper
    covers cylinders, cones, domes and hyperboloids.
    """
    cx, cy = center
    verts = []
    rings = []
    for z, radius in profile:
        if radius <= 0.0:
            rings.append([len(verts)])
            verts.append((cx, cy, z))
            continue
        ring = []
        for k in range(segments):
            angle = TAU * k / segments
            ring.append(len(verts))
            verts.append((cx + radius * math.cos(angle),
                          cy + radius * math.sin(angle), z))
        rings.append(ring)

    faces = []
    for lower, upper in zip(rings, rings[1:]):
        for k in range(segments):
            n = (k + 1) % segments
            if len(lower) == 1:
                faces.append((lower[0], upper[n], upper[k]))
            elif len(upper) == 1:
                faces.append((lower[k], lower[n], upper[0]))
            else:
                faces.append((lower[k], lower[n], upper[n], upper[k]))
    if cap_bottom and len(rings[0]) > 1:
        faces.append(tuple(reversed(rings[0])))
    if cap_top and len(rings[-1]) > 1:
        faces.append(tuple(rings[-1]))
    return new_object(name, verts, faces, material, smooth=smooth)


def cylinder(name, center, base, height, radius, material=None, segments=32):
    return revolve(name, [(base, radius), (base + height, radius)],
                   segments=segments, center=center, material=material)


def sphere(name, center, radius, material=None, segments=24, rings=12):
    profile = [(center[2] + radius * math.cos(math.pi * i / rings),
                radius * math.sin(math.pi * i / rings))
               for i in range(rings, -1, -1)]
    return revolve(name, profile, segments=segments, center=center[:2],
                   material=material, cap_bottom=False, cap_top=False)


def hyperboloid_profile(height, base_radius, throat_radius, throat_height,
                        rings=24):
    """Classic natural-draft cooling tower silhouette.

    ``r(z) = throat * sqrt(1 + ((z - z_throat) / c)^2)``, with ``c`` solved so
    the curve passes through ``base_radius`` at z = 0.
    """
    ratio = base_radius / throat_radius
    c = throat_height / math.sqrt(max(ratio * ratio - 1.0, 1e-6))
    profile = []
    for i in range(rings + 1):
        z = height * i / rings
        t = (z - throat_height) / c
        profile.append((z, throat_radius * math.sqrt(1.0 + t * t)))
    return profile


def radius_at(profile, z):
    """Linear interpolation of a ``(z, radius)`` profile."""
    for (z0, r0), (z1, r1) in zip(profile, profile[1:]):
        if z0 <= z <= z1:
            t = 0.0 if z1 == z0 else (z - z0) / (z1 - z0)
            return r0 + (r1 - r0) * t
    return profile[-1][1] if z > profile[-1][0] else profile[0][1]


def pipe(name, start, end, radius, material=None, segments=None):
    """Cylinder spanning two points."""
    dx, dy, dz = (end[i] - start[i] for i in range(3))
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        raise ValueError("degenerate pipe: %r -> %r" % (start, end))
    obj = revolve(name, [(-length / 2.0, radius), (length / 2.0, radius)],
                  segments=seg(16, 6) if segments is None else segments,
                  material=material)
    obj.location = ((start[0] + end[0]) / 2.0,
                    (start[1] + end[1]) / 2.0,
                    (start[2] + end[2]) / 2.0)
    # A +Z cylinder is tilted by the polar angle about Y, then swung round to
    # the azimuth about Z -- the XYZ euler order applies X, then Y, then Z.
    obj.rotation_euler = (0.0, math.acos(max(-1.0, min(1.0, dz / length))),
                          math.atan2(dy, dx))
    return obj


# ---------------------------------------------------------------------------
# the plant
# ---------------------------------------------------------------------------


def build_cooling_tower(name, center, height=34.0, base_radius=11.0,
                        throat_radius=6.4, lift=4.0, materials=None):
    """Natural-draft tower: hyperboloid shell standing on diagonal A-legs."""
    throat_height = height * 0.72
    profile = hyperboloid_profile(height, base_radius, throat_radius,
                                  throat_height, rings=seg(24, 6))
    shell_profile = [(z, r) for z, r in profile if z > lift]
    shell_profile.insert(0, (lift, radius_at(profile, lift)))
    shell = revolve(name, shell_profile, segments=seg(64, 12), center=center,
                    material=materials["concrete"], cap_bottom=False,
                    cap_top=False)
    top_radius = shell_profile[-1][1]
    revolve("%s_Rim" % name,
            [(height, top_radius), (height + 0.6, top_radius * 1.03)],
            segments=seg(64, 12), center=center, material=materials["metal"],
            cap_bottom=False, cap_top=False)

    # Air intake: pairs of splayed legs carrying the shell above the ground.
    leg_count = seg(20, 8)
    foot_radius = shell_profile[0][1] * 1.12
    spread = TAU / leg_count * 0.45
    for i in range(leg_count):
        angle = TAU * i / leg_count
        top = (center[0] + shell_profile[0][1] * math.cos(angle),
               center[1] + shell_profile[0][1] * math.sin(angle), lift)
        for j, offset in enumerate((-spread, spread)):
            foot = (center[0] + foot_radius * math.cos(angle + offset),
                    center[1] + foot_radius * math.sin(angle + offset), 0.0)
            pipe("%s_Leg_%02d_%d" % (name, i, j), foot, top, 0.4,
                 materials["concrete"], segments=seg(8, 4))

    # Steam plume: overlapping puffs drifting downwind off the rim.
    for i in range(7 if STEAM else 0):
        t = i / 6.0
        puff_radius = top_radius * (0.45 + 0.55 * t)
        sphere("%s_Steam_%d" % (name, i),
               (center[0] + 9.0 * t * t, center[1] - 5.0 * t * t,
                height + 2.0 + 16.0 * t),
               puff_radius, materials["steam"], segments=seg(20, 8),
               rings=seg(10, 5))

    return shell


def build_chimney(name, center, height, base_radius, top_radius, materials):
    revolve(name, [(0.0, base_radius * 1.35), (2.0, base_radius * 1.1),
                   (height, top_radius)],
            segments=seg(32, 8), center=center,
            material=materials["concrete"], cap_bottom=True, cap_top=False)
    revolve("%s_Crown" % name,
            [(height, top_radius * 1.15), (height + 1.0, top_radius * 1.15)],
            segments=seg(32, 8), center=center, material=materials["metal"],
            cap_bottom=False, cap_top=False)
    # Aviation warning bands, sized to the taper so they sit flush.
    for i, frac in enumerate((0.55, 0.75, 0.95)):
        z = 2.0 + (height - 2.0) * frac
        radius = base_radius * 1.1 + (top_radius - base_radius * 1.1) * \
            (z - 2.0) / (height - 2.0)
        revolve("%s_Band_%d" % (name, i),
                [(z - 1.1, radius * 1.02), (z + 1.1, radius * 1.02)],
                segments=seg(32, 8), center=center,
                material=materials["red"], cap_bottom=False, cap_top=False)


def build_turbine_hall(materials, size=(38.0, 18.0, 14.0), center=(0.0, 0.0)):
    width, depth, height = size
    cx, cy = center
    box("Turbine_Hall", (width, depth, height), (cx, cy, height / 2.0),
        materials["concrete"])
    # Gabled roof: a triangular prism with its ridge running along X.
    hw, hd = width / 2.0, depth / 2.0
    ridge = height + 3.0
    verts = [(cx - hw, cy - hd, height), (cx + hw, cy - hd, height),
             (cx + hw, cy + hd, height), (cx - hw, cy + hd, height),
             (cx - hw, cy, ridge), (cx + hw, cy, ridge)]
    faces = [(0, 3, 2, 1), (0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5)]
    new_object("Turbine_Hall_Roof", verts, faces, materials["metal"])

    # Window bands on both long walls, standing just proud of the wall.
    columns = 9
    for row, z in enumerate((height * 0.35, height * 0.68)):
        for col in range(columns):
            x = cx + (col - (columns - 1) / 2.0) * (width / columns)
            for sign in (-1, 1):
                y = cy + sign * (depth / 2.0 + 0.05)
                box("Window_%d_%d_%s" % (row, col, "S" if sign < 0 else "N"),
                    (width / columns * 0.6, 0.2, height * 0.18), (x, y, z),
                    materials["glass"])


def build_scene():
    materials = {
        "concrete": make_material("Concrete", (0.62, 0.61, 0.58), 0.9),
        "metal": make_material("Metal", (0.32, 0.33, 0.36), 0.35, metallic=0.8),
        "red": make_material("Warning_Red", (0.62, 0.13, 0.09), 0.6),
        "glass": make_material("Glass", (0.10, 0.28, 0.45), 0.1, alpha=0.45),
        "ground": make_material("Ground", (0.21, 0.24, 0.16), 0.95),
        "steam": make_material("Steam", (0.92, 0.93, 0.95), 1.0, alpha=0.12),
    }

    box("Ground", (400.0, 400.0, 0.4), (0.0, 0.0, -0.2), materials["ground"])
    build_turbine_hall(materials)
    box("Boiler_House", (16.0, 16.0, 26.0), (-27.0, 14.0, 13.0),
        materials["concrete"])
    box("Switchyard_Shed", (10.0, 8.0, 6.0), (26.0, 16.0, 3.0),
        materials["concrete"])

    towers = [(-30.0, -34.0), (2.0, -40.0)]
    for i, center in enumerate(towers):
        build_cooling_tower("Cooling_Tower_%d" % (i + 1), center,
                            materials=materials)

    chimneys = [((-27.0, 14.0), 62.0, 3.0, 2.0), ((-9.0, 22.0), 48.0, 2.4, 1.7)]
    for i, (center, height, base_radius, top_radius) in enumerate(chimneys):
        build_chimney("Chimney_%d" % (i + 1), center, height, base_radius,
                      top_radius, materials)

    # Storage tanks.
    for i, (x, y, radius, height) in enumerate(((30.0, -6.0, 5.0, 9.0),
                                                (30.0, 6.0, 5.0, 9.0))):
        revolve("Tank_%d" % (i + 1),
                [(0.0, radius), (height, radius),
                 (height + radius * 0.35, radius * 0.75),
                 (height + radius * 0.5, 0.0)],
                segments=seg(32, 8), center=(x, y),
                material=materials["metal"], cap_bottom=True, cap_top=False)

    # Steam and feedwater runs between the buildings and the towers.
    pipe("Pipe_Boiler_Hall", (-27.0, 14.0, 20.0), (-14.0, 6.0, 12.0), 0.9,
         materials["metal"])
    pipe("Pipe_Hall_Tower_1", (-16.0, -9.0, 6.0), (-30.0, -26.0, 6.0), 1.1,
         materials["metal"])
    pipe("Pipe_Hall_Tower_2", (2.0, -9.0, 6.0), (2.0, -31.0, 6.0), 1.1,
         materials["metal"])
    pipe("Pipe_Tanks", (25.0, 0.0, 5.0), (19.0, 0.0, 5.0), 0.7,
         materials["metal"])
    supports = ((-20.0, -14.0), (-26.0, -21.0), (2.0, -16.0), (2.0, -24.0))
    for i, (x, y) in enumerate(supports):
        cylinder("Pipe_Support_%d" % i, (x, y), 0.0, 5.0, 0.45,
                 materials["concrete"], segments=seg(8, 4))


def scene_bounds(skip=("Ground", "Steam")):
    """World-space bounding box of every mesh object, minus a name blacklist."""
    bpy.context.view_layer.update()
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    for obj in bpy.data.objects:
        if obj.type != "MESH" or any(word in obj.name for word in skip):
            continue
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            for axis in range(3):
                lo[axis] = min(lo[axis], world[axis])
                hi[axis] = max(hi[axis], world[axis])
    return Vector(lo), Vector(hi)


def add_camera_and_lights(azimuth=-58.0, elevation=19.0, margin=0.98):
    """Frame the whole plant, so changing the layout does not need a new camera."""
    lo, hi = scene_bounds()
    target = (lo + hi) / 2.0
    radius = (hi - lo).length / 2.0

    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 50.0
    cam_data.clip_end = 2000.0
    camera = bpy.data.objects.new("Camera", cam_data)

    render = bpy.context.scene.render
    aspect = render.resolution_x / float(render.resolution_y)
    hfov = 2.0 * math.atan(0.5 * cam_data.sensor_width / cam_data.lens)
    vfov = 2.0 * math.atan(math.tan(hfov / 2.0) / aspect)
    distance = radius / math.tan(min(hfov, vfov) / 2.0) * margin
    az, el = math.radians(azimuth), math.radians(elevation)
    offset = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az),
                     math.sin(el))) * distance
    camera.location = target + offset
    camera.rotation_euler = (-offset).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.collection.objects.link(camera)
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("Sun", type="SUN")
    sun_data.energy = 4.0
    sun_data.angle = math.radians(2.0)
    sun = bpy.data.objects.new("Sun", sun_data)
    sun.rotation_euler = (math.radians(52.0), 0.0, math.radians(35.0))
    bpy.context.scene.collection.objects.link(sun)

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    if world.node_tree is None:
        world.use_nodes = True
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = (0.55, 0.68, 0.85, 1.0)
    background.inputs["Strength"].default_value = 1.0


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def parse_args():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    elif sys.argv and sys.argv[0].endswith(".py"):
        argv = sys.argv[1:]
    else:
        argv = []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--obj", help="write the scene to this .obj file")
    parser.add_argument("--blend", help="save the scene to this .blend file")
    parser.add_argument("--render", help="render a still to this image file")
    parser.add_argument("--detail", type=float, default=1.0,
                        help="scale every segment count; try 0.3 for line art")
    parser.add_argument("--no-steam", dest="steam", action="store_false",
                        help="omit the steam plumes")
    parser.add_argument("--samples", type=int, default=48,
                        help="render samples (default: 48)")
    parser.add_argument("--resolution", type=int, nargs=2, default=(1280, 720),
                        metavar=("W", "H"))
    return parser.parse_args(argv)


def export_obj(path):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.select_set(True)
    bpy.ops.wm.obj_export(filepath=path, export_selected_objects=True,
                          export_materials=False, export_normals=False,
                          export_uv=False, apply_modifiers=True,
                          forward_axis="Y", up_axis="Z")


def render_still(path, samples):
    scene = bpy.context.scene
    scene.render.filepath = path
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    bpy.ops.render.render(write_still=True)


def main():
    global DETAIL, STEAM
    args = parse_args()
    DETAIL, STEAM = args.detail, args.steam
    reset_scene()
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = args.resolution
    build_scene()
    add_camera_and_lights()
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    tris = sum(len(o.data.polygons) for o in meshes)
    print("power plant: %d objects, %d faces" % (len(meshes), tris))
    if args.obj:
        export_obj(args.obj)
        print("wrote %s" % args.obj)
    if args.blend:
        bpy.ops.wm.save_as_mainfile(filepath=args.blend)
        print("wrote %s" % args.blend)
    if args.render:
        render_still(args.render, args.samples)
        print("wrote %s" % args.render)


if __name__ == "__main__":
    main()
