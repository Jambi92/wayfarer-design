# dqs_eval.py (bpy module) -- python3(bpy) dqs_eval.py -- RIGDIAG.blend RIG.json WEIGHTS.npz OUTDIR POSE1,POSE2,...
# Comparison skinning only: the same diagnostic weights evaluated by Blender's armature modifier with Preserve Volume (dual-quaternion)
# on; separates linear-blend (weights / skinning method) collapse from topology. Nothing is saved to the .blend.
import bpy, sys, os, json, numpy as np, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import Rig, build_poses, rotm, bl_to_src
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); rig = Rig(a[1], a[2]); P = build_poses(rig); os.makedirs(a[3], exist_ok=True)
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]; arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
for m in body.modifiers:
    if m.type == 'ARMATURE': m.use_deform_preserve_volume = True
for nm in a[4].split(','):
    for pb in arm.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
    for n, rots in P[nm].items():
        M = np.eye(3)
        for ax, d in rots: M = M @ rotm(ax, d)
        arm.pose.bones[n].rotation_quaternion = mathutils.Matrix(M.tolist()).to_quaternion()
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); ob = body.evaluated_get(dg); me = ob.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); ob.to_mesh_clear()
    np.savez_compressed('%s/%s.npz' % (a[3], nm), V=bl_to_src(co.reshape(-1, 3)).astype(np.float32)); print('DQS', nm, flush=True)
