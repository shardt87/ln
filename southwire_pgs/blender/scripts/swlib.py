"""Shared helpers for the Southwire PGS master scene.

Units: metres (real-world scale).  Z is up.  Every module builds into its own
named collection so assemblies stay independently selectable / removable /
exportable.  Geometry that repeats (terminal blocks, bays, reels ...) is built
once and re-used through linked mesh data or collection instances.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix, Euler

# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------
_COLL = {}


def coll(path):
    """Return (creating if needed) a collection addressed as 'Top/Sub/Leaf'."""
    parent = bpy.context.scene.collection
    key = ""
    for part in path.split("/"):
        key = part if not key else key + "/" + part
        if key not in _COLL:
            c = bpy.data.collections.get(part) or bpy.data.collections.new(part)
            if c.name not in parent.children:
                parent.children.link(c)
            _COLL[key] = c
        parent = _COLL[key]
    return parent


def link(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------------------
# Materials  (one shared library; every module re-uses these)
# ---------------------------------------------------------------------------
_MATS = {}

PALETTE = {
    # name: (base colour sRGB hex, metallic, roughness, extra)
    "Paint_ANSI61":      ("#B3B8BC", 0.0, 0.42, {}),
    "Paint_Dark":        ("#5E656B", 0.0, 0.45, {}),
    "Paint_Enclosure":   ("#B8BDC1", 0.0, 0.40, {}),
    "Paint_Base":        ("#5F676E", 0.0, 0.55, {}),
    "Bench_Mat":         ("#69737A", 0.0, 0.70, {}),
    "Paint_Engine":      ("#6F767C", 0.1, 0.45, {}),
    "Paint_Transformer": ("#A9B0B5", 0.0, 0.42, {}),
    "Backplate_White":   ("#ECECEA", 0.0, 0.50, {}),
    "Steel_Galv":        ("#A7ABAE", 1.0, 0.42, {}),
    "Steel_Dark":        ("#3E4347", 0.8, 0.45, {}),
    "Copper":            ("#C27A4A", 1.0, 0.28, {}),
    "Copper_Tinned":     ("#C9CBC9", 1.0, 0.30, {}),
    "Brass":             ("#B59A5A", 1.0, 0.32, {}),
    "Aluminium":         ("#C8CCCF", 1.0, 0.35, {}),
    "Plastic_Duct":      ("#C9CDD0", 0.0, 0.62, {}),
    "Plastic_TB":        ("#B3B7B9", 0.0, 0.55, {}),
    "Plastic_TB_GY":     ("#5F9E48", 0.0, 0.55, {}),
    "Plastic_Device":    ("#2C3034", 0.0, 0.50, {}),
    "Plastic_DeviceLt":  ("#D9DBDB", 0.0, 0.50, {}),
    "Plastic_Black":     ("#18191B", 0.0, 0.45, {}),
    "Rubber":            ("#1E1F21", 0.0, 0.80, {}),
    "Insulator":         ("#7B3F2C", 0.0, 0.35, {}),   # brown glazed porcelain / polymer
    "Insulator_Gray":    ("#8E9599", 0.0, 0.40, {}),
    "Glass_Dark":        ("#22282D", 0.0, 0.15, {}),
    # conductors -- presentation colours (see legend; NOT conductor ID)
    "Wire_Control":      ("#2E66B0", 0.0, 0.48, {}),  # presentation blue = kit control wiring
    "Wire_Field":        ("#8A9096", 0.0, 0.50, {}),  # site-installed field cores
    "Wire_Ground":       ("#3E8E41", 0.0, 0.50, {}),  # equipment grounding conductor (green)
    "Jacket_Power":      ("#1C1D1F", 0.0, 0.62, {}),
    "Jacket_Control":    ("#55595D", 0.0, 0.60, {}),
    "Jacket_Portable":   ("#26272A", 0.0, 0.70, {}),
    "Highlight_Field":   ("#D88A1E", 0.0, 0.50, {}),  # presentation amber = site-installed scope
    "Insulation_XLPE":   ("#2B2C2E", 0.0, 0.40, {}),
    "Semicon":           ("#111111", 0.0, 0.70, {}),
    "Marker_White":      ("#F3F3F1", 0.0, 0.55, {}),
    "Marker_Yellow":     ("#E8C547", 0.0, 0.55, {}),
    "Ferrule_Collar":    ("#9AA0A6", 0.0, 0.50, {}),
    "Heatshrink_Black":  ("#202123", 0.0, 0.55, {}),
    "Braid":             ("#B9BBBC", 1.0, 0.55, {}),
    "Cardboard":         ("#B7976A", 0.0, 0.85, {}),
    "Tote":              ("#5B6670", 0.0, 0.55, {}),
    "Paper":             ("#F7F7F4", 0.0, 0.80, {}),
    "Label_Ink":         ("#202326", 0.0, 0.60, {}),
    "Wood_Reel":         ("#A8835A", 0.0, 0.75, {}),
    "Concrete":          ("#D2D3D1", 0.0, 0.85, {}),
    "Radiator_Black":    ("#2A2D30", 0.3, 0.55, {}),
    "Cam_Black":         ("#1B1B1B", 0.0, 0.45, {}),
    "Cam_Red":           ("#A8312B", 0.0, 0.45, {}),
    "Cam_Blue":          ("#2B4E99", 0.0, 0.45, {}),
    "Cam_White":         ("#E4E4E0", 0.0, 0.45, {}),
    "Cam_Green":         ("#2F7D3A", 0.0, 0.45, {}),
    "Pilot_Green":       ("#3C9A4C", 0.0, 0.25, {}),
    "Pilot_Red":         ("#B23A33", 0.0, 0.25, {}),
    "Pilot_Amber":       ("#D49A2A", 0.0, 0.25, {}),
    "Boundary_Factory":  ("#2E66B0", 0.0, 0.50, {"alpha": 0.16}),
    "Boundary_Field":    ("#D88A1E", 0.0, 0.50, {"alpha": 0.12}),
    "Floor_Pad":         ("#E3E4E2", 0.0, 0.90, {}),
}


def _srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_rgba(h):
    h = h.lstrip("#")
    return tuple(_srgb_to_lin(int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4)) + (1.0,)


def M(name):
    if name in _MATS:
        return _MATS[name]
    col, met, rough, extra = PALETTE[name]
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = hex_rgba(col)
    bsdf.inputs["Metallic"].default_value = met
    bsdf.inputs["Roughness"].default_value = rough
    if "alpha" in extra:
        bsdf.inputs["Alpha"].default_value = extra["alpha"]
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    m.diffuse_color = hex_rgba(col)  # viewport solid colour
    _MATS[name] = m
    return m


# ---------------------------------------------------------------------------
# Mesh builder: many primitives -> one object (multi-material)
# ---------------------------------------------------------------------------
class MB:
    def __init__(self):
        self.bm = bmesh.new()
        self.mats = []
        self.smooth_from = []

    def _mi(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def _tag(self, verts, mat, smooth=False):
        mi = self._mi(mat)
        faces = {f for v in verts for f in v.link_faces}
        for f in faces:
            f.material_index = mi
            f.smooth = smooth

    def box(self, size, center, mat, rot=None):
        """Axis-aligned (or rotated) box. size = full (x, y, z)."""
        R = Euler(rot).to_matrix().to_4x4() if rot else Matrix()
        m = Matrix.Translation(Vector(center)) @ R @ Matrix.Diagonal((*size, 1.0))
        r = bmesh.ops.create_cube(self.bm, size=1.0, matrix=m)
        self._tag(r["verts"], mat)
        return self

    def box_mm(self, xmin, xmax, ymin, ymax, zmin, zmax, mat):
        return self.box((xmax - xmin, ymax - ymin, zmax - zmin),
                        ((xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2), mat)

    def shell(self, x0, x1, y0, y1, z0, z1, t, mat, open=("-y",)):
        """Hollow box (sheet-metal enclosure) with the listed faces left open."""
        faces = {"-x": (x0, x0 + t, y0, y1, z0, z1), "+x": (x1 - t, x1, y0, y1, z0, z1),
                 "-y": (x0, x1, y0, y0 + t, z0, z1), "+y": (x0, x1, y1 - t, y1, z0, z1),
                 "-z": (x0, x1, y0, y1, z0, z0 + t), "+z": (x0, x1, y0, y1, z1 - t, z1)}
        for k, b in faces.items():
            if k not in open:
                self.box_mm(*b, mat)
        return self

    def cyl(self, r, length, center, mat, axis="Z", segs=20, r2=None, smooth=True, rot=None):
        if rot is not None:
            R = Euler(rot).to_matrix().to_4x4()
        else:
            R = {"Z": Matrix(), "X": Matrix.Rotation(math.pi / 2, 4, "Y"),
                 "Y": Matrix.Rotation(math.pi / 2, 4, "X")}[axis]
        m = Matrix.Translation(Vector(center)) @ R
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segs,
                                    radius1=r, radius2=(r if r2 is None else r2), depth=length, matrix=m)
        self._tag(res["verts"], mat, smooth)
        return self

    def sphere(self, r, center, mat, segs=16):
        res = bmesh.ops.create_uvsphere(self.bm, u_segments=segs, v_segments=max(6, segs // 2), radius=r,
                                        matrix=Matrix.Translation(Vector(center)))
        self._tag(res["verts"], mat, True)
        return self

    def torus(self, R, r, center, mat, axis="Z", segs=32, rsegs=10, arc=2 * math.pi):
        """Ring / partial ring built from a swept circle."""
        rings = []
        steps = segs if arc >= 2 * math.pi - 1e-6 else segs + 1
        for i in range(steps):
            a = arc * i / segs
            c = Vector((R * math.cos(a), R * math.sin(a), 0))
            radial = Vector((math.cos(a), math.sin(a), 0))
            ring = []
            for j in range(rsegs):
                b = 2 * math.pi * j / rsegs
                p = c + radial * (r * math.cos(b)) + Vector((0, 0, r * math.sin(b)))
                ring.append(p)
            rings.append(ring)
        R4 = {"Z": Matrix(), "X": Matrix.Rotation(math.pi / 2, 4, "Y"),
              "Y": Matrix.Rotation(math.pi / 2, 4, "X")}[axis]
        T = Matrix.Translation(Vector(center)) @ R4
        vs = [[self.bm.verts.new(T @ p) for p in ring] for ring in rings]
        for i in range(len(vs) - (0 if arc >= 2 * math.pi - 1e-6 else 1)):
            a, b = vs[i], vs[(i + 1) % len(vs)]
            for j in range(rsegs):
                self.bm.faces.new((a[j], a[(j + 1) % rsegs], b[(j + 1) % rsegs], b[j]))
        self._tag([v for ring in vs for v in ring], mat, True)
        return self

    def poly_prism(self, pts2d, z0, z1, mat, plane="XY", offset=(0, 0, 0)):
        """Extrude a 2-D polygon (list of (a,b)) between z0..z1 along plane normal."""
        def P(a, b, c):
            if plane == "XY":
                v = (a, b, c)
            elif plane == "XZ":
                v = (a, c, b)
            else:  # YZ
                v = (c, a, b)
            return Vector(v) + Vector(offset)
        bot = [self.bm.verts.new(P(a, b, z0)) for a, b in pts2d]
        top = [self.bm.verts.new(P(a, b, z1)) for a, b in pts2d]
        self.bm.faces.new(bot[::-1])
        self.bm.faces.new(top)
        k = len(pts2d)
        for i in range(k):
            self.bm.faces.new((bot[i], bot[(i + 1) % k], top[(i + 1) % k], top[i]))
        self._tag(bot + top, mat)
        return self

    def obj(self, name, collection, bevel=0.0, loc=(0, 0, 0), sharp_angle=35):
        me = bpy.data.meshes.new(name)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        self.bm.to_mesh(me)
        self.bm.free()
        for m in self.mats:
            me.materials.append(m)
        try:
            me.set_sharp_from_angle(angle=math.radians(sharp_angle))
        except Exception:
            pass
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        collection.objects.link(ob)
        if bevel > 0:
            bv = ob.modifiers.new("Bevel", "BEVEL")
            bv.width = bevel
            bv.segments = 2
            bv.limit_method = "ANGLE"
            bv.angle_limit = math.radians(40)
            bv.harden_normals = False
        return ob


def instance_mesh(src, name, collection, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    """Linked duplicate (shares mesh data -> re-used geometry)."""
    ob = bpy.data.objects.new(name, src.data)
    ob.location = loc
    ob.rotation_euler = rot
    ob.scale = scale
    for m in src.modifiers:
        if m.type == "BEVEL":
            bv = ob.modifiers.new(m.name, "BEVEL")
            bv.width, bv.segments, bv.limit_method, bv.angle_limit = m.width, m.segments, m.limit_method, m.angle_limit
    collection.objects.link(ob)
    return ob


def instance_coll(src_coll, name, collection, loc=(0, 0, 0), rot=(0, 0, 0)):
    """Collection instance (re-uses a whole multi-object assembly)."""
    e = bpy.data.objects.new(name, None)
    e.instance_type = "COLLECTION"
    e.instance_collection = src_coll
    e.location = loc
    e.rotation_euler = rot
    e.empty_display_size = 0.3
    collection.objects.link(e)
    return e


# ---------------------------------------------------------------------------
# Wires / cables as editable curves
# ---------------------------------------------------------------------------

def fillet(pts, r, seg=4):
    """Round polyline corners with radius r (keeps curve editable as POLY points)."""
    pts = [Vector(p) for p in pts]
    if len(pts) < 3 or r <= 0:
        return pts
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        d1 = (a - b)
        d2 = (c - b)
        l1, l2 = d1.length, d2.length
        if l1 < 1e-6 or l2 < 1e-6:
            continue
        d1n, d2n = d1 / l1, d2 / l2
        cosang = max(-1, min(1, d1n.dot(d2n)))
        if cosang < -0.999:  # straight
            out.append(b)
            continue
        rr = min(r, l1 * 0.45, l2 * 0.45)
        p1 = b + d1n * rr
        p2 = b + d2n * rr
        for k in range(seg + 1):
            t = k / seg
            # quadratic bezier through corner
            q = (1 - t) ** 2 * p1 + 2 * (1 - t) * t * b + t ** 2 * p2
            out.append(q)
    out.append(pts[-1])
    return out


def curve_obj(name, splines, radius, mat, collection, res=6, fill_caps=True, fr=None, seg=4):
    """splines: list of point lists.  One curve object, one spline per conductor."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = max(1, res // 2)
    cu.use_fill_caps = fill_caps
    cu.twist_mode = "MINIMUM"
    for pts in splines:
        pp = fillet(pts, fr if fr is not None else radius * 4, seg) if len(pts) > 2 else [Vector(p) for p in pts]
        sp = cu.splines.new("POLY")
        sp.points.add(len(pp) - 1)
        for i, p in enumerate(pp):
            sp.points[i].co = (p.x, p.y, p.z, 1.0)
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu)
    collection.objects.link(ob)
    return ob


def wire(name, pts, radius, mat, collection, fr=None, seg=4):
    return curve_obj(name, [pts], radius, mat, collection, fr=fr, seg=seg)


def bezier_cable(name, pts, radius, mat, collection, res=12):
    """Smooth auto-handle Bezier cable (for heavy power / portable cables)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    cu.resolution_u = res
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        bp = sp.bezier_points[i]
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu)
    collection.objects.link(ob)
    return ob


# ---------------------------------------------------------------------------
# Text, empties, cameras
# ---------------------------------------------------------------------------

def text(name, body, size, loc, rot, mat, collection, extrude=0.0004, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.extrude = extrude
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    ob.rotation_euler = rot
    collection.objects.link(ob)
    return ob


def empty(name, loc, collection, size=0.05, kind="SPHERE"):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = kind
    e.empty_display_size = size
    e.location = loc
    collection.objects.link(e)
    return e


def camera(name, loc, target, lens=50, collection=None, sensor=36.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = sensor
    ob = bpy.data.objects.new(name, cd)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    ob["target"] = list(target)
    (collection or bpy.context.scene.collection).objects.link(ob)
    return ob


def cyl_between(mb, a, b, r, mat, segs=16):
    """Cylinder from point a to point b."""
    a, b = Vector(a), Vector(b)
    d = b - a
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler()
    mb.cyl(r, d.length, tuple((a + b) / 2), mat, rot=tuple(rot), segs=segs)


def lug(mb, end, direction, r_barrel, mat=None, tongue=(0.024, 0.006, 0.05)):
    """Compression lug: barrel over cable end + flat tongue continuing along direction."""
    mat = mat or M("Copper_Tinned")
    d = Vector(direction).normalized()
    e = Vector(end)
    cyl_between(mb, e - d * 0.01, e + d * 0.055, r_barrel, mat, segs=16)
    rot = Vector((0, 0, 1)).rotation_difference(d).to_euler()
    c = e + d * (0.055 + tongue[2] / 2)
    mb.box(tongue, tuple(c), mat, rot=tuple(rot))


def tag_panel(ob, explode=None):
    """Mark an object as a removable enclosure panel; optional exploded offset."""
    ob["removable_panel"] = True
    if explode is not None:
        ob["explode_offset"] = list(explode)
    return ob


def tag_explode(ob, offset):
    ob["explode_offset"] = list(offset)
    return ob


def V(*a):
    return Vector(a)
