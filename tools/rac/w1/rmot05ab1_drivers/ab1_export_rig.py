# RM-OT-05AB1: read the cp2 rig scene (hash-checked) and export what is needed to reproduce its Armature-modifier deformation
# exactly: rest vertex positions, triangles, per-group vertex weights and per-bone deform matrices (pose @ rest^-1, armature space).
# Read-only on the .blend.   Usage: python3 ab1_export_rig.py -- RIG_cp2.blend SHA256 OUT.npz
import bpy, sys, hashlib, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; blend, exp, out = a
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('rig hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend)
o = bpy.data.objects['GO-05AA_C_working']; ao = bpy.data.objects['GO-05AB_temp_rig']; me = o.data
assert o.matrix_world.is_identity if hasattr(o.matrix_world, 'is_identity') else True
n = len(me.vertices); V = np.empty(n * 3); me.vertices.foreach_get('co', V); me.calc_loop_triangles()
T = np.empty(len(me.loop_triangles) * 3, np.int32); me.loop_triangles.foreach_get('vertices', T)
names = [g.name for g in o.vertex_groups]; W = np.zeros((n, len(names)), np.float32)
for v in me.vertices:
    for ge in v.groups: W[v.index, ge.group] = ge.weight
M = np.stack([np.array(ao.pose.bones[nm].matrix @ ao.data.bones[nm].matrix_local.inverted()) for nm in names])
dg = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(dg); m2 = ev.to_mesh(); X = np.empty(n * 3); m2.vertices.foreach_get('co', X); ev.to_mesh_clear()
np.savez(out, V=V.reshape(-1, 3), F=T.reshape(-1, 3), W=W, names=np.array(names), M=M, X_cp2=X.reshape(-1, 3),
         obj_world=np.array(o.matrix_world), arm_world=np.array(ao.matrix_world), rig_sha256=h)
print(n, len(names), names, np.array(o.matrix_world).round(4).tolist(), np.array(ao.matrix_world).round(4).tolist())
