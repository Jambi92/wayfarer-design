# RAC Stage C renderer: one body (npz V cm (x, f fwd, u up) + F [+ keep]) -> orthographic Workbench views at ONE common scale
# (px per cm fixed, frame 280 cm, ground at the same image row), grey shaded + flat silhouette. Optional uniform comparison scale
# (Gorrund only, ruling D2(c): temporary comparison copy, never saved as a body). Usage: python3 stc_render.py IN.npz OUTPREFIX [target_stature_cm]
import sys, numpy as np, bpy, mathutils
inp, out = sys.argv[-3], sys.argv[-2]
try: tgt = float(sys.argv[-1])
except ValueError: inp, out, tgt = sys.argv[-2], sys.argv[-1], None
d = np.load(inp, allow_pickle=True); V = d['V'].astype(np.float64); F = d['F'].astype(np.int64)
keep = d['keep'].astype(bool) if 'keep' in d.files else np.ones(len(V), bool)
if keep.sum() < len(V):                                   # drop helper geometry (MPFB helpers) from the faces
    F = F[keep[F].all(1)]
V[:, 2] -= V[keep, 2].min()
if tgt: V *= tgt / V[keep, 2].max()                       # uniform comparison copy (D2(c)); in-memory only
band = keep & (V[:, 2] > 0.45 * V[keep, 2].max()) & (V[:, 2] < 0.7 * V[keep, 2].max())
lo = np.percentile(V[band, 1], 2); hi = np.percentile(V[band, 1], 98); V[:, 0] -= np.median(V[band, 0]); V[:, 1] -= 0.5 * (lo + hi)
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('b'); me.from_pydata((V / 100.0 * np.array([1, -1, 1])).tolist(), [], F.tolist()); me.update()
o = bpy.data.objects.new('b', me); sc = bpy.context.scene; sc.collection.objects.link(o)
for p in me.polygons: p.use_smooth = True
sc.render.engine = 'BLENDER_WORKBENCH'; sc.world = bpy.data.worlds.new('w'); sc.render.film_transparent = True
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.7, 0.7, 0.7)
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co; cam.clip_end = 50
PXCM = 3.0; FR = 280.0; sc.render.resolution_x = int(160 * PXCM); sc.render.resolution_y = int(FR * PXCM)
cam.shift_y = 0.0
def shot(yaw, name, flat=False):
    y = np.radians(yaw); dvec = np.array([np.sin(y), -np.cos(y), 0.0])   # Blender: front of body faces -y
    tgt3 = np.array([0, 0, FR / 2 / 100.0 - 0.10])
    co.location = mathutils.Vector((tgt3 + dvec * 10).tolist()); co.rotation_euler = mathutils.Vector((-dvec).tolist()).to_track_quat('-Z', 'Y').to_euler()
    sh.light = 'FLAT' if flat else 'STUDIO'; sh.single_color = (0.05, 0.05, 0.05) if flat else (0.7, 0.7, 0.7)
    sc.render.filepath = '%s_%s.png' % (out, name); bpy.ops.render.render(write_still=True)
cam.ortho_scale = FR / 100.0      # vertical extent = FR cm
cam.sensor_fit = 'VERTICAL'
for yaw, n in ((0, 'F'), (35, 'Q'), (90, 'P'), (180, 'B')): shot(yaw, n)
for yaw, n in ((0, 'Fs'), (90, 'Ps')): shot(yaw, n, flat=True)
print('RENDERED', out, round(float(V[keep, 2].max()), 2))
