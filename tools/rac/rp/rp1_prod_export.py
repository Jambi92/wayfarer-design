"""RAC RP1-D: export the production object from the production .blend (read-only; never saved) to npz in the analysis frame
(cm; x = subject left, f = forward = -y Blender, u = up). Writes V, quad/ngon face list (padded -1), triangles F (fan split), names.
Usage: blender-python rp1_prod_export.py -- PRODUCTION.blend OBJECT OUT.npz"""
import sys, numpy as np, bpy
a = sys.argv[sys.argv.index('--') + 1:]; path, name, out = a
bpy.ops.wm.open_mainfile(filepath=path)
o = bpy.data.objects[name]; me = o.data
assert len(o.modifiers) == 0, 'production object must have all modifiers applied'
M = np.asarray(o.matrix_world)
V = np.array([v.co[:] for v in me.vertices], np.float64); V = (M @ np.c_[V, np.ones(len(V))].T).T[:, :3]
V = np.c_[V[:, 0], -V[:, 1], V[:, 2]] * 100.0
P = [list(p.vertices) for p in me.polygons]; k = max(map(len, P))
Q = np.array([p + [-1] * (k - len(p)) for p in P], np.int64)
T = np.array([[p[0], p[i], p[i + 1]] for p in P for i in range(1, len(p) - 1)], np.int64)
np.savez_compressed(out, V=V, F=T, Q=Q, objects=np.array([ob.name for ob in bpy.data.objects]), mods=np.array([len(ob.modifiers) for ob in bpy.data.objects]))
print('PROD', name, len(V), len(P), 'tris', len(T), 'objects', [(ob.name, len(ob.modifiers), len(ob.data.vertices) if ob.type == 'MESH' else 0) for ob in bpy.data.objects])
