"""Export-only trims that keep the GLB / USDZ under GitHub's 100 MiB file limit without visible change.

Called by export_model.py after the .blend is saved, so the saved scene and the renders are untouched:

- rod end caps nobody sees: every cap of a thin rod (cable, conduit, rail, handrail: radius under 3 in; a cable
  run is a chain of rods whose caps sit inside the next segment or in a gland), and the two caps of a straight
  joint between equal rods (face to face). rod_geo builds each cap as a separate flat ring, half of a rod's
  vertices.
- buried faces: faces entirely below grade with the site ground straight above every corner (duct banks,
  foundations, buried pipe); stub-ups, open trenches and anything not under the ground surface stay.
- decals: the 1,800 printed panels are one quad each; quads that share an item and an image become one object
  (2,500 -> ~1,000 meshes, far fewer draw calls in PowerPoint).
"""
import collections

import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

FT = 0.3048
THIN = 3 / 12 * FT          # rods thinner than this (radius) lose both caps


def _delete_faces(me, faces):
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in faces], context="FACES")   # loose verts go with them
    bm.to_mesh(me)
    bm.free()
    me.update()


def _caps(me):
    """Rod end caps: lone flat n-gons (their verts belong to no other face) whose rim coincides with the verts of
    smooth faces (the rod's side). Returns (face, centre, normal, radius) per cap."""
    nv, npg = len(me.vertices), len(me.polygons)
    if not npg:
        return []
    co = np.empty(nv * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    lv = np.empty(len(me.loops), dtype=np.int64)
    me.loops.foreach_get("vertex_index", lv)
    ls, lt = np.empty(npg, dtype=np.int64), np.empty(npg, dtype=np.int64)
    me.polygons.foreach_get("loop_start", ls)
    me.polygons.foreach_get("loop_total", lt)
    sm = np.empty(npg, dtype=bool)
    me.polygons.foreach_get("use_smooth", sm)
    fn = np.empty(npg * 3)
    me.polygons.foreach_get("normal", fn)
    fn = fn.reshape(-1, 3)
    fid = np.repeat(np.arange(npg), lt)
    lone = np.ones(npg, bool)
    np.logical_and.at(lone, fid, np.bincount(lv, minlength=nv)[lv] == 1)
    cand = lone & ~sm & (lt >= 4)
    if not cand.any() or not sm.any():
        return []
    key = lambda p: np.round(p / 1e-5).astype(np.int64)
    side = set(map(tuple, key(co[np.unique(lv[sm[fid]])])))
    cl = np.where(cand[fid])[0]
    on_side = np.fromiter((tuple(k) in side for k in key(co[lv[cl]])), bool, len(cl))
    np.logical_and.at(cand, fid[cl], on_side)
    out = []
    for f in np.where(cand)[0]:
        p = co[lv[ls[f]:ls[f] + lt[f]]]
        c = p.mean(0)
        out.append((int(f), c, fn[f], float(np.linalg.norm(p - c, axis=1).max())))
    return out


def strip_hidden_caps(me):
    caps = _caps(me)
    drop, at = set(), collections.defaultdict(list)
    for i, (f, c, n, r) in enumerate(caps):
        if r < THIN:
            drop.add(i)
        else:
            at[tuple(np.round(c / 1e-4).astype(int))].append(i)
    for g in at.values():                      # straight joint: equal caps face to face
        for a in g:
            for b in g:
                if a < b and abs(caps[a][3] - caps[b][3]) < 1e-4 and abs(np.dot(caps[a][2], caps[b][2])) > .999:
                    drop.update((a, b))
    if drop:
        _delete_faces(me, [caps[i][0] for i in drop])
    return len(drop)


def ground_tree(objs):
    vs, fs = [], []
    for o in objs:
        b = len(vs)
        vs += [o.matrix_world @ v.co for v in o.data.vertices]
        fs += [[b + i for i in p.vertices] for p in o.data.polygons]
    return BVHTree.FromPolygons(vs, fs) if fs else None


def strip_buried(ob, tree, zmax=-0.1 * FT, reach=30 * FT):
    me, mw = ob.data, ob.matrix_world
    co = [mw @ v.co for v in me.vertices]
    up, hit = Vector((0, 0, 1)), {}

    def covered(i):
        if i not in hit:
            hit[i] = tree.ray_cast(co[i], up, reach)[0] is not None
        return hit[i]

    faces = [p.index for p in me.polygons
             if all(co[i].z < zmax for i in p.vertices) and all(covered(i) for i in p.vertices)]
    if faces:
        _delete_faces(me, faces)
    return len(faces)


def join_decals(bpy, objs):
    groups = collections.defaultdict(list)
    for o in objs:
        if o.name.startswith("decal ") and o.data.materials:
            groups[(o.get("item"), o.data.materials[0].name)].append(o)
    n = 0
    for obs in groups.values():
        if len(obs) < 2:
            continue
        with bpy.context.temp_override(active_object=obs[0], selected_editable_objects=obs):
            bpy.ops.object.join()
        n += len(obs) - 1
    return n


def slim(bpy, objs):
    """objs: the mesh objects going into the export. Returns a one-line report."""
    site = bpy.data.collections.get("SITE")
    tree = ground_tree([o for o in site.all_objects if o.type == "MESH"]) if site else None
    nb = nc = 0
    done = set()
    for o in objs:
        if o.name.startswith("decal ") or o.data.name in done or o.data.users > 1:
            continue
        done.add(o.data.name)
        if tree and not any(c.name in ("SITE", "LANDSCAPE") for c in o.users_collection):
            nb += strip_buried(o, tree)
        nc += strip_hidden_caps(o.data)
    nd = join_decals(bpy, objs)
    return f"slim: {nc} hidden rod caps, {nb} buried faces removed, {nd} decal quads merged"
