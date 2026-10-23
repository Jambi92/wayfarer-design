# rview.py (bpy) -- IN.npz OUTPREFIX views [color.npy] [vmax] [center x,f,u] [halfsize cm] [px]
# orthographic workbench renders, analysis frame (x left, f forward, u up, cm) -> blender (x, -f, u)/100
import bpy, sys, numpy as np, math, mathutils
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V'].astype(float); F = z['Q'] if 'Q' in z.files else z['F']
if 'keep' in z.files and 'Q' not in z.files:
    k = z['keep']; used = np.zeros(len(V), bool); used[F.ravel()] = True
pre = a[1]; views = a[2].split(','); col = np.load(a[3]) if len(a) > 3 and a[3] != '-' else None
vmax = float(a[4]) if len(a) > 4 else 1.0
ctr = np.array([float(x) for x in a[5].split(',')]) if len(a) > 5 else None
hs = float(a[6]) if len(a) > 6 else None; px = int(a[7]) if len(a) > 7 else 900
bpy.ops.wm.read_factory_settings(use_empty=True)
P = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100
me = bpy.data.meshes.new('m'); me.from_pydata(P.tolist(), [], F.tolist()); me.update()
ob = bpy.data.objects.new('m', me); bpy.context.scene.collection.objects.link(ob)
for p in me.polygons: p.use_smooth = True
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading; sh.light = 'STUDIO'; sh.show_specular_highlight = False
if col is not None:
    import matplotlib.cm as cm
    c = cm.turbo(np.clip(col / vmax, 0, 1)); attr = me.color_attributes.new('c', 'FLOAT_COLOR', 'POINT'); attr.data.foreach_set('color', c.astype(np.float32).ravel())
    sh.color_type = 'VERTEX'
else:
    sh.color_type = 'SINGLE'; sh.single_color = (0.75, 0.72, 0.68)
sc.render.film_transparent = False; sc.world = bpy.data.worlds.new('w'); sc.world.color = (1, 1, 1)
bb0 = P.min(0); bb1 = P.max(0); c0 = (bb0 + bb1) / 2 if ctr is None else np.array([ctr[0], -ctr[1], ctr[2]]) / 100
half = (bb1[2] - bb0[2]) / 2 * 1.05 if hs is None else hs / 100
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.ortho_scale = 2 * half
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
sc.render.resolution_x = px; sc.render.resolution_y = px
dirs = {'front': (0, -1, 0), 'back': (0, 1, 0), 'left': (1, 0, 0), 'right': (-1, 0, 0), 'q3': (0.7, -0.7, 0), 'q3r': (-0.7, -0.7, 0), 'top': (0, 0, 1), 'below': (0, 0, -1)}
for v in views:
    d = mathutils.Vector(dirs[v]).normalized(); co.location = mathutils.Vector(c0) + d * 5
    up = (0, 1, 0) if v in ('top', 'below') else (0, 0, 1)
    co.rotation_euler = (-d).to_track_quat('-Z', 'Y' if v in ('top','below') else 'Y').to_euler()
    if v not in ('top','below'):
        co.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = '%s_%s.png' % (pre, v); bpy.ops.render.render(write_still=True)
