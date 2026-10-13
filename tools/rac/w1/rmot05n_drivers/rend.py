# rend.py OBJ OUT.png [yaw list] : ortho grey renders centred on the mesh bbox (Z up); yaw 0 = camera on -Y looking +Y
import sys, math, bpy, numpy as np
from mathutils import Vector
from PIL import Image
obj, out = sys.argv[1], sys.argv[2]; yaws = [float(a) for a in sys.argv[3].split(',')] if len(sys.argv) > 3 else [0, 45, 90, 135, 180, 270]
V = np.array([[float(t) for t in l.split()[1:4]] for l in open(obj) if l.startswith('v ')])
F = [[int(t.split('/')[0]) - 1 for t in l.split()[1:]] for l in open(obj) if l.startswith('f ')]
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('b'); me.from_pydata(V.tolist(), [], F); me.update()
ob = bpy.data.objects.new('b', me); bpy.context.scene.collection.objects.link(ob)
for p in me.polygons: p.use_smooth = True
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.66, 0.66, 0.68); sh.show_cavity = True; sh.cavity_type = 'BOTH'
lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; H = max(hi[2] - lo[2], 1e-3)
sc.render.resolution_x = 600; sc.render.resolution_y = 900; sc.world = bpy.data.worlds.new('w')
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.clip_start = 1; cam.clip_end = 5000; cam.ortho_scale = H * 1.08
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co; ims = []
for yaw in yaws:
    a = math.radians(yaw); d = 1000
    p = Vector((c[0] + d * math.sin(a), c[1] - d * math.cos(a), c[2]))
    co.location = p; co.rotation_euler = (Vector(c) - p).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out + '_%d.png' % yaw; bpy.ops.render.render(write_still=True); ims.append(Image.open(sc.render.filepath).convert('RGB'))
W = sum(i.size[0] for i in ims); s = Image.new('RGB', (W, ims[0].size[1])); x = 0
for i in ims: s.paste(i, (x, 0)); x += i.size[0]
s = s.resize((W // 2, ims[0].size[1] // 2)); s.save(out); print(out)
