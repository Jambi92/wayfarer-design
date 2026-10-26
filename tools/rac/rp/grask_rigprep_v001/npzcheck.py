# npzcheck.py (bpy module, read-only) -- python3(bpy) npzcheck.py -- BLEND NPZ T_X T_F : confirm the analysis npz used for fitting is the
# blend's geometry. Analysis = (x, -y, z)*100 - (T_X, T_F, 0); T = 0 for the source, the production translation for v003.
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0])
m = [o for o in bpy.data.objects if o.type == 'MESH'][0].data
co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get('co', co); co = co.reshape(-1, 3).astype(float)
V = np.c_[co[:, 0], -co[:, 1], co[:, 2]] * 100 - np.array([float(a[2]), float(a[3]), 0.0])
P = np.load(a[1])['V']
print('NPZCHECK', a[1], 'nV', len(P), len(V), 'max_abs_diff_cm', float(np.abs(P - V).max()) if len(P) == len(V) else 'size-mismatch')
