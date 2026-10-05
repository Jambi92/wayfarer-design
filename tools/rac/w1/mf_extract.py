"""RAC W1: extract evaluated Marchfolk candidate geometry + rig joints from the Iteration 3 .blend (read-only).
Usage: python mf_extract.py <in.blend> <out.npz>   (bpy 5.0.1). Units written in cm."""
import sys, bpy, numpy as np
src, out = sys.argv[1], sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=src)
body = bpy.data.objects["Marchfolk.body"]; rig = bpy.data.objects["Marchfolk"]
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg); me = ev.to_mesh()
M = np.array(ev.matrix_world)
V = np.array([v.co[:] for v in me.vertices]); V = (np.c_[V, np.ones(len(V))] @ M.T)[:, :3] * 100
F = []
for p in me.polygons:
    vs = list(p.vertices)
    for i in range(1, len(vs) - 1): F.append([vs[0], vs[i], vs[i + 1]])
F = np.array(F)
R = np.array(rig.matrix_world)
J = {}
for pb in rig.pose.bones:
    h = R @ np.r_[np.array(pb.head), 1]; t = R @ np.r_[np.array(pb.tail), 1]
    J[pb.name] = np.r_[h[:3], t[:3]] * 100
rest_vs_pose = max(float(np.abs(np.array(pb.matrix_basis) - np.eye(4)).max()) for pb in rig.pose.bones)
mods = [(m.name, m.type, getattr(m, 'show_viewport', None)) for m in body.modifiers]
sk = {k.name: k.value for k in body.data.shape_keys.key_blocks} if body.data.shape_keys else {}
np.savez_compressed(out, V=V, F=F, J_names=np.array(list(J)), J=np.array(list(J.values())),
                    meta=np.array([repr(dict(mods=mods, pose_delta=rest_vs_pose, shape_keys=sk, n_orig=len(body.data.vertices),
                                                 props={k: str(body[k])[:300] for k in body.keys()}))]))
print("verts", len(V), "tris", len(F), "pose_delta", rest_vs_pose, "z range cm", V[:, 2].min(), V[:, 2].max())
print("mods", mods); print("shape keys", {k: round(v, 3) for k, v in sk.items() if abs(v) > 1e-4})
