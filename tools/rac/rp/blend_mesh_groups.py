"""Read-only: export the single mesh of a .blend to npz (V cm, F triangles, per-vertex-group weights). Usage: python3 blend_mesh_groups.py IN.blend OUT.npz"""
import bpy, sys, numpy as np
p, out = sys.argv[-2], sys.argv[-1]; bpy.ops.wm.open_mainfile(filepath=p)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data; n = len(me.vertices)
V = np.zeros(n * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3) * 100
me.calc_loop_triangles(); T = np.zeros(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T)
W = {g.name: np.zeros(n, np.float32) for g in o.vertex_groups}; names = [g.name for g in o.vertex_groups]
for v in me.vertices:
    for ge in v.groups: W[names[ge.group]][v.index] = ge.weight
np.savez_compressed(out, V=V.astype(np.float32), F=T.reshape(-1, 3).astype(np.int32), **{'w_' + k: v for k, v in W.items()})
print('MG', n, len(T) // 3, names)
