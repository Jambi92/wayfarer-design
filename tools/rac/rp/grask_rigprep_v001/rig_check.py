# rig_check.py (bpy module) -- python3(bpy) rig_check.py -- RIGDIAG.blend RIG.json WEIGHTS.npz LANDMARKS.json OUT.json
# Verifies the diagnostic rig inside Blender: (1) Blender armature deformation == numpy LBS used for the measurements, on several
# D-poses; (2) rest-return: pose -> clear pose -> evaluated mesh equals the frozen v003 positions (T-1); (3) bone lengths equal the
# landmark segment lengths (T-6). Opens the derived diagnostic file only; nothing is saved.
import bpy, sys, os, json, numpy as np, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import Rig, build_poses
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); rig = Rig(a[1], a[2]); L = json.load(open(a[3]))['joints']
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]; arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
def evaluated():
    dg = bpy.context.evaluated_depsgraph_get(); ob = body.evaluated_get(dg); me = ob.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); ob.to_mesh_clear(); return co.reshape(-1, 3)
rest_co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get('co', rest_co); rest_co = rest_co.reshape(-1, 3)
def apply(pose):
    for pb in arm.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    for n, rots in pose.items():
        M = np.eye(3)
        for ax, d in rots: M = M @ __import__('diag_lib').rotm(ax, d)
        arm.pose.bones[n].rotation_quaternion = mathutils.Matrix(M.tolist()).to_quaternion()
    bpy.context.view_layer.update()
P = build_poses(rig); out = dict(equivalence={}, rest_return={})
for nm in ('D1_l_abd90', 'D2_l_flex130', 'D4_l_fist', 'D6_r_flex90', 'D9_twist_p30', 'D10_rot_p45'):
    apply(P[nm]); vb = evaluated(); vn, _, _ = rig.skin(rest_co, P[nm])
    out['equivalence'][nm] = dict(max_diff_mm=float(np.abs(vb - vn).max() * 1000), max_motion_mm=float(np.linalg.norm(vn - rest_co, axis=1).max() * 1000))
    apply({}); vr = evaluated(); out['rest_return'][nm] = dict(max_dev_mm=float(np.linalg.norm(vr - rest_co, axis=1).max() * 1000))
seg = []
for b in arm.data.bones:
    if not b.use_deform: continue
    h = np.array(b.head_local); t = np.array(b.tail_local)
    # find the landmark pair the bone was built from (head / tail coincide with landmark positions)
    hk = min(L, key=lambda k: np.linalg.norm(np.array(L[k]['position_blender_m']) - h)); tk = min(L, key=lambda k: np.linalg.norm(np.array(L[k]['position_blender_m']) - t))
    d_lm = np.linalg.norm(np.array(L[hk]['position_blender_m']) - np.array(L[tk]['position_blender_m'])) * 100; seg.append(dict(bone=b.name, head=hk, tail=tk, bone_cm=b.length * 100, landmark_cm=d_lm, diff_mm=abs(b.length * 100 - d_lm) * 10))
out['bone_lengths'] = seg; out['bone_length_max_diff_mm'] = max(s['diff_mm'] for s in seg)
out['armature_modifier'] = [dict(name=m.name, preserve_volume=m.use_deform_preserve_volume, use_vertex_groups=m.use_vertex_groups) for m in body.modifiers if m.type == 'ARMATURE']
json.dump(out, open(a[4], 'w'), indent=1)
print('EQUIV max mm', max(v['max_diff_mm'] for v in out['equivalence'].values()), 'REST max mm', max(v['max_dev_mm'] for v in out['rest_return'].values()), 'BONE max mm', out['bone_length_max_diff_mm'])
