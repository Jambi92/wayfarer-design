# RM-OT-05AD s7 retry gates: frozen 05AD sculpt-safe baseline vs UI-sculpted GO-05AD_AC1 (Blender-native vertex order, read
# from the .blend files with bpy). Topology identity, opened seams (coincident groups in the 05AD baseline that separate),
# components / boundary / non-manifold (position-welded), flips, degenerates, self-intersections, displacement by region
# (protected = 05AC protection mask carried through the 05AD weld map), stature / bbox.
# Usage: python ad_ac1_gates.py BASE_VF.npz AC1.blend PROTECT.npy OLD_TO_NEW.npy OUTDIR
import sys, os, json, hashlib, numpy as np
import bpy
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
bp, ab, pp, mp, od = sys.argv[1:6]
B = np.load(bp); VB, FB = B['V'], B['F']
bpy.ops.wm.open_mainfile(filepath=ab)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data
VA = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', VA); W = np.array(o.matrix_world); VA = VA.reshape(-1, 3) @ W[:3, :3].T + W[:3, 3]
me.calc_loop_triangles(); FA = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', FA); FA = FA.reshape(-1, 3)
np.savez(os.path.join(od, 'ac1_VF.npz'), V=VA, F=FA)
R = dict(ac1_blend=os.path.basename(ab), ac1_blend_sha256=hashlib.sha256(open(ab, 'rb').read()).hexdigest(),
         vertices=dict(base=len(VB), ac1=len(VA)), triangles=dict(base=len(FB), ac1=len(FA)))
R['topology_identical'] = bool(len(VB) == len(VA) and np.array_equal(FB, FA))
n = len(VB); d = np.linalg.norm(VA - VB, axis=1) * 1000  # mm
# opened seams: coincident groups in the base
pairs = cKDTree(VB).query_pairs(1e-5, output_type='ndarray')
if len(pairs):
    sep = np.linalg.norm(VA[pairs[:, 0]] - VA[pairs[:, 1]], axis=1) * 1000
    R['coincident_pairs_in_base'] = int(len(pairs)); R['pairs_opened_gt_0_01mm'] = int((sep > 0.01).sum()); R['max_pair_gap_mm'] = round(float(sep.max()), 4)
z = (VB[:, 2] - VB[:, 2].min()) * 100
P0 = np.load(pp); o2n = np.load(mp); P = np.zeros(n); np.maximum.at(P, o2n, P0)
mv = d > 1e-3
R['moved_vertices'] = int(mv.sum()); R['max_displacement_mm'] = round(float(d.max()), 3); R['p99_moved_mm'] = round(float(np.percentile(d[mv], 99)), 3) if mv.any() else 0
R['moved_z_from_floor_cm'] = [round(float(z[mv].min()), 1), round(float(z[mv].max()), 1)] if mv.any() else None
R['moved_outside_117_170cm'] = int((mv & ((z < 117) | (z > 170))).sum())
R['protected_vertices_moved'] = int((mv & (P >= 1)).sum()); R['protected_core_max_mm'] = round(float(d[P >= 1].max()), 4)
R['height_cm'] = dict(base=round(float(np.ptp(VB[:, 2])) * 100, 4), ac1=round(float(np.ptp(VA[:, 2])) * 100, 4))
R['bbox_extent_cm'] = dict(base=np.round(np.ptp(VB, 0) * 100, 3).tolist(), ac1=np.round(np.ptp(VA, 0) * 100, 3).tolist())
def nrm(V, F):
    x = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); l = np.linalg.norm(x, axis=1); return x / np.maximum(l, 1e-30)[:, None], l
nB, aB = nrm(VB, FB); nA, aA = nrm(VA, FB); dot = (nB * nA).sum(1)
R['flipped_faces'] = int((dot < 0).sum()); R['rotated_over_60deg'] = int((dot < 0.5).sum())
R['degenerate_faces'] = dict(base=int((aB < 1e-14).sum()), ac1=int((aA < 1e-14).sum()))
def welded(V, F):
    k, iv = np.unique(np.round(V, 7), axis=0, return_inverse=True); return k, iv.ravel()[F]
def topo(k, F):
    m = len(k); E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1); E = E[E[:, 0] != E[:, 1]]
    u, c = np.unique(E, axis=0, return_counts=True)
    nc, lab = connected_components(coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(m, m)), directed=False)
    return dict(components=int(len(np.unique(lab[np.unique(F)]))), boundary_edges=int((c == 1).sum()), nonmanifold_edges=int((c > 2).sum()))
kB, WB = welded(VB, FB); kA, WA = welded(VA, FB)
R['position_welded_base'] = topo(kB, WB); R['position_welded_ac1'] = topo(kA, WA)
np.save(os.path.join(od, 'ac1_disp_mm.npy'), d.astype(np.float32))
json.dump(R, open(os.path.join(od, 'ac1_gates_partial.json'), 'w'), indent=1); print(json.dumps(R, indent=1))
