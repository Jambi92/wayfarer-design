# RM-OT-05AB s6 preservation checks: donor working mesh (before) vs macro-corrected derivative (after). Read-only.
# - topology identity (triangle index arrays equal), welded components, boundary / non-manifold edges (before and after);
# - rigid-block preservation: hands, feet, head (above the neck minimum), free tail - best-fit rigid (Kabsch) residual and extents;
# - deformation quality: per-group edge-length ratio percentiles, counts of strongly stretched/compressed edges, face-normal flips.
# Usage: python3 ab_checks.py BEFORE.npz AFTER.npz WEIGHTS.npz JOINTS.json OUT.json   (npz in Blender metres, V/F)
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
b, a, wp, jp, out = sys.argv[1:6]
B = np.load(b); A = np.load(a); VB = B['V'].astype(float) * 100; VA = A['V'].astype(float) * 100; F = B['F'].astype(np.int64)
R = dict(topology_identical=bool(np.array_equal(B['F'], A['F'])), vertices=len(VB), faces=len(F))
Wd = np.load(wp); names = [str(x) for x in Wd['names']]; inv = Wd['welded_index']; Wt = Wd['weights_welded'][inv]; lab = Wd['label_welded'][inv]
J = json.load(open(jp)); OFF = np.array([6.888, -39.481, 0.0])
def topo(V):
    key, iv = np.unique(np.round(V, 4), axis=0, return_inverse=True); iv = iv.ravel(); Fw = iv[F]; n = len(key)
    E = np.sort(np.concatenate([Fw[:, [0, 1]], Fw[:, [1, 2]], Fw[:, [2, 0]]]), 1); E = E[E[:, 0] != E[:, 1]]
    u, c = np.unique(E, axis=0, return_counts=True)
    nc, _ = connected_components(sp.coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(n, n)), directed=False)
    used = np.unique(Fw); return dict(welded_vertices=int(n), components=int(nc - (n - len(used))), boundary_edges=int((c == 1).sum()), nonmanifold_edges=int((c > 2).sum()))
R['before'] = topo(VB); R['after'] = topo(VA)
def kabsch(P, Q):
    pc, qc = P.mean(0), Q.mean(0); Hm = (P - pc).T @ (Q - qc); U, S, Vt = np.linalg.svd(Hm); d = np.sign(np.linalg.det(Vt.T @ U.T))
    Rm = Vt.T @ np.diag([1, 1, d]) @ U.T; res = np.linalg.norm((P - pc) @ Rm.T + qc - Q, axis=1)
    ang = np.degrees(np.arccos(np.clip((np.trace(Rm) - 1) / 2, -1, 1))); return res, ang, qc - pc
neck = 168.3; bodyy = J['midline_y'] + OFF[1]
blocks = {g: (lab == names.index(g)) & (Wt.max(1) > 0.99) for g in ('hand_L', 'hand_R', 'foot_L', 'foot_R')}
blocks['head (above neck minimum)'] = (VB[:, 2] > neck) & (lab == names.index('trunk')) & (Wt.max(1) > 0.99)
blocks['tail free portion'] = (VB[:, 1] > bodyy + 25) & (VB[:, 2] < 85) & (lab == names.index('trunk')) & (Wt.max(1) > 0.99)
R['rigid_blocks'] = {}
for k, m in blocks.items():
    res, ang, t = kabsch(VB[m], VA[m])
    R['rigid_blocks'][k] = dict(vertices=int(m.sum()), rms_residual_mm=round(float(np.sqrt((res ** 2).mean()) * 10), 4), max_residual_mm=round(float(res.max() * 10), 4),
                                rotation_deg=round(float(ang), 4), translation_cm=np.round(t, 2).tolist(),
                                extents_before_cm=np.round(np.ptp(VB[m], 0), 2).tolist(), extents_after_cm=np.round(np.ptp(VA[m], 0), 2).tolist())
E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); r = np.linalg.norm(VA[E[:, 0]] - VA[E[:, 1]], axis=1) / np.maximum(np.linalg.norm(VB[E[:, 0]] - VB[E[:, 1]], axis=1), 1e-9)
el = lab[E[:, 0]]; band = (Wt[E[:, 0]].max(1) < 0.9) | (Wt[E[:, 1]].max(1) < 0.9)
R['edge_length_ratio'] = {}
for i, g in enumerate(names + ['JOINT BLEND BANDS']):
    m = band if g == 'JOINT BLEND BANDS' else (el == i)
    q = np.percentile(r[m], [0.1, 1, 50, 99, 99.9]); R['edge_length_ratio'][g] = dict(edges=int(m.sum()), p0_1=round(q[0], 3), p1=round(q[1], 3), median=round(q[2], 3),
        p99=round(q[3], 3), p99_9=round(q[4], 3), min=round(float(r[m].min()), 3), max=round(float(r[m].max()), 3), over_1_6=int((r[m] > 1.6).sum()), under_0_6=int((r[m] < 0.6).sum()))
def fn(V):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
dot = (fn(VB) * fn(VA)).sum(1); R['face_normals'] = dict(flipped=int((dot < 0).sum()), rotated_over_60deg=int((dot < 0.5).sum()), rotated_over_30deg=int((dot < 0.866).sum()))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1))
