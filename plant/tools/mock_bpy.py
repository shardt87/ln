#!/usr/bin/env python3
"""
tools/mock_bpy.py -- run render_views.py WITHOUT Blender to check camera framing and callout projection.

It builds the plant in dry-run mode (build_plant.py), turns every registered object into a stand-in with a
world-space bounding box, installs a minimal `bpy` / `mathutils` / `bpy_extras` shim and executes render_views.py.
Instead of a Cycles render it writes a bounding-box wireframe preview PNG per view, plus a real callouts.json,
so make_sheets.py can be exercised end to end:

    python3 tools/mock_bpy.py --out out/mock --only 01,02
    python3 make_sheets.py --renders out/mock --out out/mock_sheets --placeholders

Nothing here is used by the real Blender pipeline.
"""
import math, os, sys, types, importlib.util, json

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
sys.path.insert(0, PLANT)

# ----------------------------------------------------------------------------- mathutils shim
class Vector:
    def __init__(self, v=(0, 0, 0)):
        v = list(v)
        self.x, self.y, self.z = float(v[0]), float(v[1]), float(v[2]) if len(v) > 2 else 0.0
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    def __getitem__(self, i):
        return (self.x, self.y, self.z)[i]
    def __add__(self, o): return Vector((self.x + o.x, self.y + o.y, self.z + o.z))
    def __sub__(self, o): return Vector((self.x - o.x, self.y - o.y, self.z - o.z))
    def __mul__(self, s): return Vector((self.x * s, self.y * s, self.z * s))
    __rmul__ = __mul__
    def __truediv__(self, s): return Vector((self.x / s, self.y / s, self.z / s))
    def __neg__(self): return Vector((-self.x, -self.y, -self.z))
    def dot(self, o): return self.x * o.x + self.y * o.y + self.z * o.z
    def cross(self, o): return Vector((self.y * o.z - self.z * o.y, self.z * o.x - self.x * o.z, self.x * o.y - self.y * o.x))
    @property
    def length(self): return math.sqrt(self.dot(self))
    def normalize(self):
        L = self.length or 1.0
        self.x, self.y, self.z = self.x / L, self.y / L, self.z / L
    def normalized(self):
        v = Vector(self); v.normalize(); return v
    def copy(self): return Vector(self)
    def to_track_quat(self, track, up):
        f = self.normalized()
        zaxis = -f                                  # object -Z points along self
        tmp = Vector((0, 0, 1))
        if abs(zaxis.dot(tmp)) > 0.999:
            tmp = Vector((0, 1, 0))
        xaxis = tmp.cross(zaxis).normalized()
        yaxis = zaxis.cross(xaxis)
        return Quaternion(Matrix.from_axes(xaxis, yaxis, zaxis))
    def __repr__(self): return "Vector(%.3f, %.3f, %.3f)" % (self.x, self.y, self.z)

class Quaternion:
    def __init__(self, m): self.m = m
    def __matmul__(self, v): return self.m @ v
    def to_euler(self): return Euler(self.m)

class Euler:
    def __init__(self, m): self.m = m
    def __iter__(self): return iter((0.0, 0.0, 0.0))

class Matrix:
    def __init__(self, rows=None):
        self.r = [list(r) for r in rows] if rows else [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    @staticmethod
    def Identity(n=4): return Matrix()
    @staticmethod
    def Translation(v):
        m = Matrix(); m.r[0][3], m.r[1][3], m.r[2][3] = v.x, v.y, v.z; return m
    @staticmethod
    def from_axes(x, y, z):
        m = Matrix()
        for i, a in enumerate((x, y, z)):
            m.r[0][i], m.r[1][i], m.r[2][i] = a.x, a.y, a.z
        return m
    def __matmul__(self, o):
        if isinstance(o, Vector):
            r = self.r
            return Vector((r[0][0] * o.x + r[0][1] * o.y + r[0][2] * o.z + r[0][3],
                           r[1][0] * o.x + r[1][1] * o.y + r[1][2] * o.z + r[1][3],
                           r[2][0] * o.x + r[2][1] * o.y + r[2][2] * o.z + r[2][3]))
        out = Matrix()
        for i in range(4):
            for j in range(4):
                out.r[i][j] = sum(self.r[i][k] * o.r[k][j] for k in range(4))
        return out
    def normalized(self): return self
    def inverted(self):
        # rigid transform inverse
        R = [[self.r[i][j] for j in range(3)] for i in range(3)]
        t = Vector((self.r[0][3], self.r[1][3], self.r[2][3]))
        m = Matrix()
        for i in range(3):
            for j in range(3):
                m.r[i][j] = R[j][i]
        it = Vector((-(R[0][0] * t.x + R[1][0] * t.y + R[2][0] * t.z), -(R[0][1] * t.x + R[1][1] * t.y + R[2][1] * t.z), -(R[0][2] * t.x + R[1][2] * t.y + R[2][2] * t.z)))
        m.r[0][3], m.r[1][3], m.r[2][3] = it.x, it.y, it.z
        return m
    @property
    def translation(self): return Vector((self.r[0][3], self.r[1][3], self.r[2][3]))

mathutils = types.ModuleType("mathutils")
mathutils.Vector, mathutils.Matrix, mathutils.Quaternion, mathutils.Euler = Vector, Matrix, Quaternion, Euler
sys.modules["mathutils"] = mathutils

# ----------------------------------------------------------------------------- bpy shim
class Attr(dict):
    """attribute bag: any attribute can be set / read; unknown reads return a nested bag."""
    def __getattr__(self, k):
        if k.startswith("__"):
            raise AttributeError(k)
        if k not in self:
            self[k] = Attr()
        return self[k]
    def __setattr__(self, k, v): self[k] = v
    def __call__(self, *a, **k): return Attr()

class Inputs(dict):
    def __getitem__(self, k):
        if not dict.__contains__(self, k):
            dict.__setitem__(self, k, Attr())
        return dict.__getitem__(self, k)
    def __contains__(self, k): return True

class Node(Attr):
    def __init__(self):
        super().__init__()
        self["inputs"] = Inputs(); self["outputs"] = Inputs()

class NodeTree(Attr):
    def __init__(self):
        super().__init__()
        self["nodes"] = NodeCol(); self["links"] = Attr()

class NodeCol(list):
    def new(self, t):
        n = Node(); self.append(n); return n
    def get(self, name):
        n = Node(); self.append(n); return n
    def remove(self, n):
        if n in self: list.remove(self, n)

class Material(Attr):
    def __init__(self, name):
        super().__init__(); self["name"] = name; self["node_tree"] = NodeTree()

class Points(list):
    def add(self, n):
        for _ in range(n):
            self.append(Attr(co=(0, 0, 0, 1)))

class Splines(list):
    def new(self, t):
        sp = Attr(); sp["points"] = Points(); sp["points"].add(1); self.append(sp); return sp

class DataBlock(Attr):
    def __init__(self, name, kind):
        super().__init__(); self["name"] = name; self["kind"] = kind; self["materials"] = MatList(); self["type"] = "PERSP"
        self["shift_x"] = 0.0; self["shift_y"] = 0.0; self["lens"] = 50.0; self["sensor_width"] = 36.0
        self["polygons"] = []; self["_verts"] = []; self["splines"] = Splines(); self["bevel_depth"] = 0.0
        self["node_tree"] = NodeTree()
    def from_pydata(self, verts, edges, faces):
        self["_verts"] = list(verts); self["polygons"] = [Attr(use_smooth=False) for _ in faces]
    def update(self): pass
    def bbox(self):
        pts = list(self["_verts"]) + [tuple(p.co[:3]) for sp in self["splines"] for p in sp["points"]]
        if not pts:
            return None
        r = float(self["bevel_depth"] or 0.0)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
        return [min(xs) - r, min(ys) - r, min(zs) - r, max(xs) + r, max(ys) + r, max(zs) + r]

class MatList(list):
    def append(self, m): list.append(self, m)
    def clear(self): del self[:]

class Object:
    def __init__(self, name, kind, data=None, bbox_m=None, props=None):
        self.name, self.type, self.data = name, kind, data
        self._bbox = bbox_m
        self.props = props or {}
        self.location = Vector((0, 0, 0))
        self._rot = Matrix()
        self.hide_render = False; self.hide_viewport = False
        self.parent = None; self.matrix_parent_inverse = Matrix()
        self.rotation_euler = None
    def get(self, k, d=None): return self.props.get(k, d)
    def __setitem__(self, k, v): self.props[k] = v
    def __getitem__(self, k): return self.props[k]
    def __setattr__(self, k, v):
        if k == "rotation_euler" and isinstance(v, Euler):
            object.__setattr__(self, "_rot", v.m)
        if k == "location" and not isinstance(v, Vector):
            v = Vector(v)
        object.__setattr__(self, k, v)
    @property
    def matrix_world(self):
        return Matrix.Translation(self.location) @ self._rot
    @property
    def bound_box(self):
        b = self._bbox
        if b is None:
            return [(0, 0, 0)] * 8
        return [(x, y, z) for x in (b[0], b[3]) for y in (b[1], b[4]) for z in (b[2], b[5])]

class ObjCol(list):
    def get(self, name):
        for o in self:
            if o.name == name:
                return o
        return None
    def __getitem__(self, k):
        if isinstance(k, str):
            o = self.get(k)
            if o is None:
                raise KeyError(k)
            return o
        return list.__getitem__(self, k)
    def new(self, name, data):
        kind = "EMPTY"
        if data is not None:
            kind = {"CAMERA": "CAMERA", "LIGHT": "LIGHT", "FONT": "FONT", "MESH": "MESH", "CURVE": "CURVE"}.get(data.get("kind"), "EMPTY")
        bb = data.bbox() if (data is not None and kind in ("MESH", "CURVE")) else None
        o = Object(name, kind, data, bb); self.append(o); return o
    def remove(self, o, do_unlink=True):
        if o in self: list.remove(self, o)
    def link(self, o): pass

class Factory(dict):
    def __init__(self, kind): super().__init__(); self.kind = kind
    def new(self, name, t=None):
        d = Material(name) if self.kind == "MAT" else DataBlock(name, t or self.kind); self[name] = d; return d
    def get(self, name): return dict.get(self, name)

def aabb_hit(origin, d, b, tmax):
    t0, t1 = 0.0, tmax
    for i in range(3):
        o, dd = origin[i], d[i]
        lo, hi = b[i], b[i + 3]
        if abs(dd) < 1e-12:
            if o < lo or o > hi:
                return None
            continue
        ta, tb = (lo - o) / dd, (hi - o) / dd
        if ta > tb: ta, tb = tb, ta
        t0, t1 = max(t0, ta), min(t1, tb)
        if t0 > t1:
            return None
    return t0

class Scene(Attr):
    def __init__(self):
        super().__init__()
        self["render"] = Attr(); self["cycles"] = Attr(); self["view_settings"] = Attr(); self["display_settings"] = Attr()
        self["world"] = None; self["camera"] = None; self["node_tree"] = NodeTree(); self["collection"] = Attr(objects=ObjCol())
        self["_props"] = {}
    def get(self, k, d=None): return self["_props"].get(k, d)
    def ray_cast(self, deps, origin, direction, distance=1e9):
        best, best_o = None, None
        for o in bpy.data.objects:
            if o.hide_viewport or o.type not in ("MESH", "CURVE") or o._bbox is None:
                continue
            t = aabb_hit(origin, direction, o._bbox, distance)
            if t is not None and t > 0.05 and (best is None or t < best):
                best, best_o = t, o
        if best is None:
            return (False, None, None, -1, None, None)
        return (True, origin + direction * best, None, 0, best_o, None)

class Ops:
    class render:
        @staticmethod
        def render(write_still=True):
            write_preview(bpy.context.scene)

def write_preview(scene):
    """bounding-box wireframe preview through the current camera (stand-in for a Cycles render)."""
    from PIL import Image, ImageDraw
    W, H = scene.render.resolution_x, scene.render.resolution_y
    im = Image.new("RGB", (W, H), "#D9D8D5")
    d = ImageDraw.Draw(im)
    cam = scene.camera
    from bpy_extras.object_utils import world_to_camera_view
    objs = sorted([o for o in bpy.data.objects if o.type in ("MESH", "CURVE") and not o.hide_render and o._bbox], key=lambda o: -(o._bbox[2] + o._bbox[5]))
    for o in objs:
        pts = []
        for c in o.bound_box:
            v = world_to_camera_view(scene, cam, Vector(c))
            if v.z <= 0:
                pts = None; break
            pts.append((v.x * W, (1 - v.y) * H))
        if not pts:
            continue
        col = "#8E8C86" if not o.name.startswith("SITE-") else "#C4C2BC"
        if "CABLE" in o.name or "CONDUCT" in o.name:
            col = "#2A2A2A"
        if "COPPER" in o.name or "CAP" in o.name or "CONNECTOR" in o.name:
            col = "#C8722E"
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 7), (6, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
        for a, b in edges:
            d.line([pts[a], pts[b]], fill=col, width=max(1, W // 2500))
    # credit stand-in at the bottom-left of the full frame
    d.text((W * 0.018, H * 0.965), "credit line (burned in by Blender text object)", fill="#4A4A48")
    im.save(scene.render.filepath)

bpy = types.ModuleType("bpy")
bpy.data = Attr()
bpy.data.objects = ObjCol()
bpy.data.materials = Factory("MAT")
bpy.data.lights = Factory("LIGHT")
bpy.data.cameras = Factory("CAMERA")
bpy.data.curves = Factory("FONT")
bpy.data.meshes = Factory("MESH")

class CollCol(dict):
    def new(self, name):
        c = Attr(name=name); c["objects"] = ObjCol(); c["children"] = Attr(); self[name] = c; return c
    def get(self, name): return dict.get(self, name)
    def remove(self, c): self.pop(c.get("name"), None)
    def __iter__(self): return iter(list(self.values()))
bpy.data.collections = CollCol()
bpy.data.worlds = Factory("WORLD")
bpy.context = Attr()
bpy.context.scene = Scene()
bpy.context.view_layer = Attr()
bpy.context.view_layer.update = lambda: None
bpy.context.evaluated_depsgraph_get = lambda: None
bpy.context.preferences = Attr()
bpy.context.preferences.addons = {}
class Wm:
    @staticmethod
    def save_as_mainfile(filepath=None): print("(mock) would save", filepath)
Ops.wm = Wm
bpy.ops = Ops
sys.modules["bpy"] = bpy

def world_to_camera_view(scene, obj, coord):
    co = obj.matrix_world.normalized().inverted() @ coord
    z = -co.z
    cam = obj.data
    hh = (cam.sensor_width / 2.0) / cam.lens
    hv = hh * scene.render.resolution_y / scene.render.resolution_x
    sx, sy = cam.shift_x * 2 * hh, cam.shift_y * 2 * hh
    if z <= 0:
        return Vector((0.5, 0.5, 0.0))
    x = (co.x / z - (-hh + sx)) / (2 * hh)
    y = (co.y / z - (-hv + sy)) / (2 * hv)
    return Vector((x, y, z))

bpy_extras = types.ModuleType("bpy_extras")
ou = types.ModuleType("bpy_extras.object_utils")
ou.world_to_camera_view = world_to_camera_view
bpy_extras.object_utils = ou
sys.modules["bpy_extras"] = bpy_extras
sys.modules["bpy_extras.object_utils"] = ou

# ----------------------------------------------------------------------------- populate from the dry-run build
def populate():
    saved = sys.argv
    sys.argv = ["build_plant.py", "--dry-run"]
    spec = importlib.util.spec_from_file_location("build_plant", os.path.join(PLANT, "build_plant.py"))
    bp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bp)
    bp.build_all()
    sys.argv = saved
    FT = bp.FT
    # objects were created through the shimmed bpy path; verify the registry matches
    names = {o.name for o in bpy.data.objects}
    missing = [r["name"] for r in bp.REG if r["name"] not in names]
    if missing:
        raise RuntimeError("shim lost objects: %s" % missing[:5])
    bpy.context.scene["_props"] = {"plant_true_scale": FT}
    return bp

if __name__ == "__main__":
    populate()
    # forward CLI args to render_views.py
    sys.argv = ["render_views.py", "--"] + sys.argv[1:]
    src = open(os.path.join(PLANT, "render_views.py")).read()
    g = {"__name__": "__main__", "__file__": os.path.join(PLANT, "render_views.py")}
    exec(compile(src, "render_views.py", "exec"), g)
