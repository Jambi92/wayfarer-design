# Rodin sheet renders: whole sheet + per-component orthographic views (bare clay, Workbench)
import sys, os, math, numpy as np
sys.path.insert(0, "/tmp/claude-0/rb")
import bpy
from mathutils import Vector
OUT = "/tmp/claude-0/rodin/ren"; os.makedirs(OUT, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
z = np.load("/tmp/claude-0/rodin/mesh.npz"); v = z["v"]; f = z["f"]; lab = np.load("/tmp/claude-0/rodin/lab.npy")
MODE = os.environ.get("RMODE", "sheet")
def make(vsub, fsub, name):
    vb = np.stack([vsub[:, 0], -vsub[:, 2], vsub[:, 1]], 1).astype(np.float32)
    me = bpy.data.meshes.new(name); me.vertices.add(len(vb)); me.vertices.foreach_set("co", vb.ravel())
    me.loops.add(fsub.size); me.loops.foreach_set("vertex_index", fsub.ravel().astype(np.int32))
    me.polygons.add(len(fsub)); me.polygons.foreach_set("loop_start", (np.arange(len(fsub)) * 3).astype(np.int32))
    me.polygons.foreach_set("loop_total", np.full(len(fsub), 3, np.int32)); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob
sc = bpy.context.scene; sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading; sh.light = "STUDIO"; sh.color_type = "SINGLE"; sh.single_color = (0.66, 0.66, 0.68)
sh.show_cavity = True; sh.cavity_type = "BOTH"; sc.render.film_transparent = True
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
if sc.world is None: sc.world = bpy.data.worlds.new("W")
cd = bpy.data.cameras.new("C"); cd.type = "ORTHO"; cam = bpy.data.objects.new("C", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_end = 50
def shoot(ob_list, yaw, path, res=1400, pad=1.08):
    piv = bpy.data.objects.new("P", None); sc.collection.objects.link(piv)
    for o in ob_list: o.parent = piv
    cen = sum((sum((Vector(c) for c in o.bound_box), Vector()) / 8 for o in ob_list), Vector()) / len(ob_list)
    piv.location = (0, 0, 0)
    for o in ob_list: o.location = -cen
    piv.rotation_euler = (0, 0, math.radians(yaw)); bpy.context.view_layer.update()
    pts = [piv.matrix_world @ (o.matrix_local @ Vector(c)) for o in ob_list for c in o.bound_box]
    xs = [p.x for p in pts]; zs = [p.z for p in pts]
    w = max(xs) - min(xs); h = max(zs) - min(zs); s = max(w, h) * pad
    sc.render.resolution_x = res; sc.render.resolution_y = res; cd.ortho_scale = s
    cam.location = ((max(xs) + min(xs)) / 2, -20, (max(zs) + min(zs)) / 2); cam.rotation_euler = (math.radians(90), 0, 0)
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
    for o in ob_list: o.parent = None; o.location = (0, 0, 0)
    bpy.data.objects.remove(piv, do_unlink=True)
if MODE == "sheet":
    ob = make(v, f, "all")
    for yaw, nm in ((0, "front"), (180, "back"), (90, "right"), (270, "left")):
        sc.render.resolution_x, sc.render.resolution_y = 3000, 1800
        cd.ortho_scale = 2.05 if yaw in (0, 180) else 0.9
        cam.location = (0, -20, 0.57); cam.rotation_euler = (math.radians(90), 0, 0)
        ob.rotation_euler = (0, 0, math.radians(yaw)); bpy.context.view_layer.update()
        sc.render.filepath = "%s/sheet_%s.png" % (OUT, nm); bpy.ops.render.render(write_still=True)
if MODE == "comps":
    ids = [int(x) for x in os.environ["RCOMPS"].split(",")]
    for i in ids:
        m = lab[f[:, 0]] == i; fs = f[m]; used = np.unique(fs); remap = -np.ones(len(v), np.int64); remap[used] = np.arange(len(used))
        ob = make(v[used], remap[fs], "c%d" % i)
        for yaw in [int(y) for y in os.environ.get("RYAWS", "0,90,180,45,135").split(",")]:
            shoot([ob], yaw, "%s/c%02d_y%03d.png" % (OUT, i, yaw), res=int(os.environ.get("RRES", "900")))
        bpy.data.objects.remove(ob, do_unlink=True)
print("RR_DONE")
