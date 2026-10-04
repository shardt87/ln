"""Southwire PGS -- view / configuration controls.

This file is embedded in the master .blend as the text block 'sw_controls.py'
(registered on load when 'Auto Run Python Scripts' is allowed, or run it once
from the Text Editor).  It adds a sidebar tab  View3D > N-panel > 'Southwire PGS'
with one button per configuration / company view, plus explode / assemble.

The same functions are imported by render_views.py for batch rendering.
View definitions live in the scene custom property  scene["sw_views"]  (JSON).
"""
import json
import bpy

ALWAYS = {"Cameras", "Lighting", "Annotations"}


def _views(scene=None):
    scene = scene or bpy.context.scene
    return json.loads(scene.get("sw_views", "{}"))


def _parents():
    par = {}
    for c in bpy.data.collections:
        for ch in c.children:
            par[ch.name] = c.name
    return par


def apply_view(name, scene=None, explode=None):
    scene = scene or bpy.context.scene
    v = _views(scene)[name]
    par = _parents()
    vis = set(v["collections"]) | set(v.get("annotations", [])) | {v.get("rig", "")}
    # ancestors of visible collections are visible
    for n in list(vis):
        p = par.get(n)
        while p:
            vis.add(p)
            p = par.get(p)
    # descendants of a listed collection are visible (except annotation/lighting leaves)
    def walk(c):
        for ch in c.children:
            if ch.name in vis or c.name in v["collections"]:
                if not (ch.name.startswith("LGT_") or ch.name.startswith("ANN_") or ch.name.startswith("CO_")):
                    vis.add(ch.name)
            walk(ch)
    for n in v["collections"]:
        c = bpy.data.collections.get(n)
        if c:
            walk(c)
    vis |= ALWAYS
    for c in bpy.data.collections:
        hide = c.name not in vis
        c.hide_render = hide
        c.hide_viewport = hide
    hidden = set(v.get("hide_objects", []))
    for ob in scene.objects:
        h = ob.name in hidden
        if ob.hide_render != h:
            ob.hide_render = h
        if ob.hide_viewport != h:
            ob.hide_viewport = h
    set_explode(v.get("explode", []) if explode is None else explode, scene)
    cam = scene.objects.get(v["camera"])
    if cam:
        scene.camera = cam
    scene["sw_active_view"] = name
    return v


def set_explode(names, scene=None):
    """Move objects listed in `names` by their 'explode_offset'; all other
    explodable objects return to their assembled ('home') position."""
    scene = scene or bpy.context.scene
    names = set(names)
    for ob in scene.objects:
        if "explode_offset" not in ob:
            continue
        if "home_loc" not in ob:
            ob["home_loc"] = list(ob.location)
        home = ob["home_loc"]
        off = ob["explode_offset"] if ob.name in names else (0, 0, 0)
        ob.location = (home[0] + off[0], home[1] + off[1], home[2] + off[2])


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
class SWPGS_OT_apply_view(bpy.types.Operator):
    bl_idname = "swpgs.apply_view"
    bl_label = "Apply view"
    view: bpy.props.StringProperty()

    def execute(self, context):
        apply_view(self.view, context.scene)
        return {"FINISHED"}


class SWPGS_OT_explode(bpy.types.Operator):
    bl_idname = "swpgs.explode"
    bl_label = "Explode all"
    on: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        names = [o.name for o in context.scene.objects if "explode_offset" in o] if self.on else []
        set_explode(names, context.scene)
        return {"FINISHED"}


class SWPGS_PT_panel(bpy.types.Panel):
    bl_label = "Southwire PGS views"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Southwire PGS"

    def draw(self, context):
        lay = self.layout
        lay.label(text="Active: " + str(context.scene.get("sw_active_view", "-")))
        views = _views(context.scene)
        groups = {}
        for k, v in views.items():
            groups.setdefault(v.get("group", "Views"), []).append(k)
        for g, keys in groups.items():
            box = lay.box()
            box.label(text=g)
            for k in keys:
                box.operator("swpgs.apply_view", text=views[k].get("title", k)).view = k
        row = lay.row()
        row.operator("swpgs.explode", text="Explode all").on = True
        row.operator("swpgs.explode", text="Assemble all").on = False


CLASSES = (SWPGS_OT_apply_view, SWPGS_OT_explode, SWPGS_PT_panel)


def register():
    for c in CLASSES:
        try:
            bpy.utils.register_class(c)
        except ValueError:
            pass


def unregister():
    for c in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
