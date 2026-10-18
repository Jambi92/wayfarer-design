import bpy, sys, numpy as np
p, out = sys.argv[-2], sys.argv[-1]; bpy.ops.wm.open_mainfile(filepath=p)
o = [o for o in bpy.data.objects if o.type == 'MESH'][0]; me = o.data
V = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
me.calc_loop_triangles(); T = np.zeros(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T)
M = np.array(o.matrix_world); V = V @ M[:3, :3].T + M[:3, 3]
np.savez(out, v=(V * 100).astype(np.float32), f=T.reshape(-1, 3).astype(np.int32))
print('B2N', len(V), len(T) // 3)
