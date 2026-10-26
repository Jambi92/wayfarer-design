# render.py (bpy module) -- MESH.npz OUTDIR TAG VIEWSPEC [WIRE 0|1] [PX]
# Neutral-clay orthographic renders of a mesh given in the v005 analysis SOURCE frame (cm; x subject-left, f forward, u up).
# Derived inspection scene only: the mesh is rebuilt from the npz in an empty scene, nothing is saved, no armature/weights/pose.
# VIEWSPEC: name:dx,df,du:cx,cf,cu:halfsize ; several separated by ';'  (d = direction from the subject toward the camera)
# Writes OUTDIR/TAG_name.png and OUTDIR/TAG_name.json (camera centre, image-right x and image-up y in the analysis frame, half-size, px).
import bpy, sys, os, json, numpy as np, mathutils
a = sys.argv[sys.argv.index('--') + 1:]
src, O, TAG, VS = a[0], a[1], a[2], a[3]
WIRE = len(a) > 4 and a[4] == '1'; PX = int(a[5]) if len(a) > 5 else 1000
z = np.load(src); V = z['V'].astype(float); F = np.asarray(z['Q'])
bpy.ops.wm.read_factory_settings(use_empty=True)
P = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100
me = bpy.data.meshes.new('m'); me.from_pydata(P.tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new('m', me); bpy.context.scene.collection.objects.link(ob)
me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading
sh.light = 'STUDIO'; sh.show_specular_highlight = False; sh.color_type = 'MATERIAL'
m1 = bpy.data.materials.new('clay'); m1.diffuse_color = (0.80, 0.77, 0.73, 1); ob.data.materials.append(m1)
if WIRE:
    w = ob.copy(); w.data = ob.data.copy(); sc.collection.objects.link(w)
    md = w.modifiers.new('wf', 'WIREFRAME'); md.thickness = float(os.environ.get('WIRE_T', '0.0006')); md.use_replace = True; md.use_even_offset = False
    m2 = bpy.data.materials.new('wire'); m2.diffuse_color = (0.12, 0.13, 0.18, 1); w.data.materials.clear(); w.data.materials.append(m2)
sc.world = bpy.data.worlds.new('w'); sc.world.color = (1, 1, 1)
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co_ = bpy.data.objects.new('c', cam); sc.collection.objects.link(co_); sc.camera = co_
sc.render.resolution_x = sc.render.resolution_y = PX; sc.render.film_transparent = False
B = lambda v: np.array([v[0], -v[1], v[2]])
for spec in VS.split(';'):
    nm, d, c, h = spec.split(':'); d = np.array([float(v) for v in d.split(',')]); d /= np.linalg.norm(d)
    c = np.array([float(v) for v in c.split(',')]); h = float(h)
    up = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([0, 1.0, 0])
    y = up - (up @ d) * d; y /= np.linalg.norm(y)
    xb = np.cross(B(y), B(d)); M = mathutils.Matrix([list(xb), list(B(y)), list(B(d))]).transposed()
    co_.matrix_world = mathutils.Matrix.Translation(mathutils.Vector(B(c + d * 150) / 100)) @ M.to_4x4()
    cam.ortho_scale = 2 * h / 100; cam.clip_end = 10
    sc.render.filepath = '%s/%s_%s.png' % (O, TAG, nm); bpy.ops.render.render(write_still=True)
    xa = np.array([xb[0], -xb[1], xb[2]])
    json.dump(dict(c=c.tolist(), x=xa.tolist(), y=y.tolist(), d=d.tolist(), h=h, px=PX), open('%s/%s_%s.json' % (O, TAG, nm), 'w'))
