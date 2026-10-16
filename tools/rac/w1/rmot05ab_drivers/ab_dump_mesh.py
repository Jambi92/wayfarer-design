# RM-OT-05AB: read the working mesh out of the pinned AA baseline .blend (verifying the .blend hash first) into V/F npz. Read-only.
# Usage: python3 ab_dump_mesh.py -- BASELINE.blend EXPECTED_SHA256 OUT.npz
import bpy, sys, hashlib, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; blend, exp, out = a
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('baseline hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend); o = bpy.data.objects['GO-05AA_C_working']; me = o.data
V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); me.calc_loop_triangles()
T = np.empty(len(me.loop_triangles) * 3, np.int32); me.loop_triangles.foreach_get('vertices', T)
P = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', P); assert (P == 3).all()
np.savez(out, V=V.reshape(-1, 3).astype(np.float32), F=T.reshape(-1, 3)); print(len(me.vertices), len(me.polygons), h)
