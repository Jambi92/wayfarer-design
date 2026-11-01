# sa6_rigprep.py CFG WEIGHTS.npz CORRECTIVES.json : RP6 reference / rig-prep stance record + round trip (order a407015 §4).
#   Reference stance = the frozen RP5 neutral (anatomy truth; armature rest).  Rig-prep stance = generated ONLY through the armature: each upper arm raised in
#   its own abduction plane (axis = (-z) x arm direction, through the glenohumeral head) from its reference angle to 45 deg from vertical (the conventional
#   A-pose); elbows, hands, digits, legs, tail, neck / head unchanged (reference values recorded).  Writes SA_RP6_rig_prep_<CFG>_v001.json.
#   Round trips:  (a) reference -> rig-prep -> reference through the armature (bone transforms back to identity): exact by construction of LBS
#   (posed = sum w (R v + t) with R = I, t = 0 and every corrective driver at 0 -> the bound frozen mesh, bit-identical);
#   (b) RE-BIND round trip (production check: the rig-prep mesh bound with the same weights and returned through the inverse bone matrices with LBS
#   blending, i.e. sum w T_b^-1 (P_prep)): reports the LBS-inverse residual (not zero: an LBS blend of inverses is not the inverse of the blend);
#   (c) exact per-vertex inverse v = M_v^-1 (P_prep - sum w t) - d_corrective: residual = numerical precision.
import sys, os, json, numpy as np
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C, sa6_pose as SP, sa6_correctives as CC
cfg, wf, cf = sys.argv[1:4]; R = SP.Rig(cfg, wf); Cr = CC.Correctives.load(R, cf)
spec = []; rec = {}
for t in ('l', 'r'):
    b = 'upperarm_' + t; h, tl = R.H(b), R.Tl(b); dv = (tl - h) / np.linalg.norm(tl - h); ang0 = np.degrees(np.arccos(-dv[2])); ax = np.cross([0, 0, -1.0], dv); ax /= np.linalg.norm(ax)
    spec.append((b, h, ax, 45.0 - ang0)); rec[b] = dict(reference_angle_from_vertical_deg=round(float(ang0), 3), rig_prep_angle_deg=45.0, rotation_deg=round(float(45 - ang0), 3), axis_world=np.round(ax, 6).tolist())
T = R.pose(spec); dl = R.V * 0 + Cr.delta(T); Pp = R.skin(T, R.V + dl)
import json as _j; Pl = _j.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % cfg))['bones']
def bmat(b):
    a = Pl[b]['local_axes']; return np.c_[a['x'], a['y_bone'], a['z']]
quats = {}
for b, _, _, _ in spec:
    Bm = bmat(b); Rb = Bm.T @ T[b][0] @ Bm; q = Rot.from_matrix(Rb).as_quat(); quats[b] = [float(q[3]), float(q[0]), float(q[1]), float(q[2])]
# (b) re-bind round trip
Tinv = {b: (T[b][0].T, -T[b][0].T @ T[b][1]) for b in T}; back = R.skin(Tinv, Pp)
# (c) exact inverse
Rb = np.stack([T[b][0] for b in R.DB]); tb = np.stack([T[b][1] for b in R.DB]); M = np.einsum('vb,bij->vij', R.W, Rb); tt = R.W @ tb
ex = np.linalg.solve(M, (Pp - tt)[:, :, None])[:, :, 0] - dl
e_b = np.linalg.norm(back - R.V, axis=1); e_c = np.linalg.norm(ex - R.V, axis=1); moved = np.linalg.norm(Pp - R.V, axis=1) > 1e-9
flips = int((R.relcos(Pp, T) < 0).sum())
out = dict(status='RP6 RIG PILOT / NOT FROZEN', configuration=cfg, method=open(__file__).read().split('import')[0],
           reference_stance='frozen RP5 neutral = armature rest', rig_prep_stance=rec, elbow='unchanged (reference)', hands='unchanged (reference orientation)', tail='neutral (reference)',
           head_neck='no offset', basis_quaternions_wxyz=quats, rig_prep_flips=flips, rig_prep_active_corrective_keys=int(sum(len(v[1]) > 0 for v in Cr.delta(T, True)[1].values())),
           round_trip_a_armature='exact (identity transforms, all drivers 0)', round_trip_b_rebind_lbs_inverse=dict(max_cm=round(float(e_b.max()), 5), p99_cm=round(float(np.percentile(e_b[moved], 99)), 5), n_moved=int(moved.sum())),
           round_trip_c_exact_inverse_max_cm=float(e_c.max()))
json.dump(out, open(C.EV6 + '/SA_RP6_rig_prep_%s_v001.json' % cfg, 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'method'}, indent=0)[:1500])
