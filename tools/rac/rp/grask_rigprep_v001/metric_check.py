# metric_check.py (bpy module, mathutils BVH) -- python3(bpy) metric_check.py -- RIG.json WEIGHTS.npz LANDMARKS.json OUT.json
# Metric validation (order 8918cea §6):
#  (1) rigid-transform sanity: the whole body rotated 30 deg about the root (a rigid motion through the rig) must give 0 intersections,
#      0 orientation failures, 0 local inversions, 0 new folds, 0 strain and 0.000 % change of every zone cone-volume proxy;
#  (2) reference-point sensitivity of the open-patch cone-volume proxy (moving the reference 1 cm changes the number although the
#      surface is unchanged) — documents that it is a proxy, not tissue volume;
#  (3) closed-volume identity: the total closed-mesh volume (divergence theorem) is reference-independent.
import bpy, sys, os, json, numpy as np
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import Rig, src_to_bl, bl_to_src
from common import PARTS
a = sys.argv[sys.argv.index('--') + 1:]; rig = Rig(a[0], a[1]); LM = json.load(open(a[2]))['joints']
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; PN = [PARTS[i] for i in FP]
def fnorm(V):
    n = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
def cone(V, faces, c):
    T = np.r_[Q[faces][:, [0, 1, 2]], Q[faces][:, [0, 2, 3]]]; x, y, w = V[T[:, 0]] - c, V[T[:, 1]] - c, V[T[:, 2]] - c; return float(np.einsum('ij,ij->i', x, np.cross(y, w)).sum() / 6)
def vol(V): return cone(V, np.arange(len(Q)), np.zeros(3))
C0 = V0[Q].mean(1); J = lambda k: np.array(LM[k]['position_source_frame_cm'])
ZONES = {'D1 shoulder': ('glenohumeral_l', 14, ('arm_l', 'axial')), 'D2 elbow': ('elbow_l', 9, ('arm_l',)), 'D6 hip': ('hip_l', 16, ('leg_l', 'axial')), 'D7 knee': ('knee_l', 11, ('leg_l',))}
Vb0 = src_to_bl(V0); Vb, Lin, M = rig.skin(Vb0, {'root': [('Z', 30.0)]}); V = bl_to_src(Vb)
_, S = rig.pose_mats({'root': [('Z', 30.0)]}); Sr = S['root']; Fl = np.diag([1.0, -1.0, 1.0])
def carry(p):                                                       # rigid image of a rest point (the root skinning matrix)
    pb = src_to_bl(p[None])[0]; return bl_to_src((Sr[:3, :3] @ pb + Sr[:3, 3])[None])[0]
out = dict(rigid={})
t = BVHTree.FromPolygons(V.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0); pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
if len(pr): A_ = Q[pr[:, 0]]; B_ = Q[pr[:, 1]]; pr = pr[~(A_[:, :, None] == B_[:, None, :]).any((1, 2))]
N0, N = fnorm(V0), fnorm(V); ne = np.einsum('ij,fjk,kl,fl->fi', Fl, Lin[Q].mean(1), Fl, N0)
E = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); Es = np.sort(E, 1); ue, inv = np.unique(Es, axis=0, return_inverse=True)
o = np.argsort(inv, kind='stable'); EFs = np.tile(np.arange(len(Q)), 4)[o].reshape(-1, 2)
def ninv(N):
    NS = np.zeros_like(N); np.add.at(NS, EFs[:, 0], N[EFs[:, 1]]); np.add.at(NS, EFs[:, 1], N[EFs[:, 0]]); return (N * NS).sum(1) < 0
L0 = np.linalg.norm(V0[ue[:, 0]] - V0[ue[:, 1]], axis=1); L1 = np.linalg.norm(V[ue[:, 0]] - V[ue[:, 1]], axis=1)
out['rigid'] = dict(pose='root rotated 30 deg about Z (whole body, rigid)', max_vertex_motion_cm=float(np.linalg.norm(V - V0, axis=1).max()), intersections=int(len(pr)),
                    orientation_failures=int(((N * ne).sum(1) < 0).sum()), local_inversions=int((ninv(N) & ~ninv(N0)).sum()),
                    new_folds=int(((N[EFs[:, 0]] * N[EFs[:, 1]]).sum(1) < -0.5).sum() - ((N0[EFs[:, 0]] * N0[EFs[:, 1]]).sum(1) < -0.5).sum()),
                    max_edge_strain_pct=float(np.abs(L1 / L0 - 1).max() * 100), total_volume_change_pct=100 * (vol(V) / vol(V0) - 1), zones={})
for zn, (jk, Rz, parts) in ZONES.items():
    c = J(jk); f = np.nonzero((np.linalg.norm(C0 - c, axis=1) <= Rz) & np.isin(PN, parts))[0]
    v0 = cone(V0, f, c); v1 = cone(V, f, carry(c))
    sens = {d: 100 * (cone(V0, f, c + np.array(e) * 1.0) / v0 - 1) for d, e in (('+x 1 cm', (1, 0, 0)), ('+f 1 cm', (0, 1, 0)), ('+u 1 cm', (0, 0, 1)))}
    out['rigid']['zones'][zn] = dict(faces=int(len(f)), cone_volume_rest_cm3=v0, rigid_change_pct=100 * (v1 / v0 - 1), reference_shift_sensitivity_pct=sens)
out['estimator'] = ('zone volume = signed open-patch CONE-VOLUME PROXY: sum over the zone faces (split into triangles) of the tetrahedron from the posed joint centre '
                    'to each triangle (divergence form without a cap). The patch boundary is not closed, so the number depends on the reference point (see '
                    'reference_shift_sensitivity_pct) and is not anatomical tissue volume; under rigid motion with the reference carried along it is exactly invariant.')
out['total_volume_estimator'] = 'closed-mesh divergence-theorem volume of the whole body (reference independent).'
json.dump(out, open(a[3], 'w'), indent=1); print(json.dumps(out['rigid'], indent=0)[:1500])
