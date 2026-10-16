# RM-OT-05AI s4 prep gate: 05AF (before) vs 05AI local-quality baseline (after). Vertex order is shared (no vertices added/removed);
# faces differ only inside the repair neighbourhoods (edge rotations). Checks: vertex movement outside / inside neighbourhoods,
# nearest-surface deviation of the repaired patch (dense samples on new faces -> old local surface, and back), Blender validity
# (duplicate faces / edges, loose geometry), position-welded components / boundary / non-manifold, self-intersections, folds in the
# neighbourhoods, degenerates, protected regions, stature / bbox.
# Usage: python3 -I ai_prep_gates.py BEFORE_VF.npz AFTER_VF.npz HOOD.npy PROTECTED.npz OUT.json
import sys, json, numpy as np, scipy.sparse as sp, pymeshlab
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
bp, ap, hp, pp, out = sys.argv[1:6]
B = np.load(bp); A = np.load(ap); VB, FB = B['V'], B['F']; VA, FA = A['V'], A['F']; hood = np.load(hp); P = np.load(pp)
R = dict(vertices=dict(before=len(VB), after=len(VA)), faces=dict(before=len(FB), after=len(FA)))
d = np.linalg.norm(VA - VB, axis=1) * 1000; inh = np.zeros(len(VB), bool); inh[hood] = True
R['max_move_outside_neighbourhoods_mm'] = float(d[~inh].max()); R['max_move_inside_neighbourhoods_mm'] = round(float(d[inh].max()), 4)
R['protected_max_disp_mm'] = {k: float(d[P[k]].max()) for k in P.files}
sB = {tuple(sorted(f)) for f in FB}; sA = {tuple(sorted(f)) for f in FA}
R['duplicate_faces_after'] = int(len(FA) - len(sA)); R['faces_changed'] = int(len(sA - sB))
chg = np.array(sorted(sA - sB)); R['changed_faces_all_inside_neighbourhoods'] = bool(inh[chg].all()) if len(chg) else True
def tri_samples(V, F, k=6):
    w = np.array([(i, j, k - i - j) for i in range(k + 1) for j in range(k + 1 - i)], float) / k
    return np.einsum('sk,fkd->fsd', w, V[F]).reshape(-1, 3)
def pt_tri_dist(p, a, b, c):  # vectorised closest distance from points p (n,3) to triangles (n,3 each)
    ab, ac, ap_ = b - a, c - a, p - a; d1 = (ab * ap_).sum(1); d2 = (ac * ap_).sum(1)
    n = np.cross(ab, ac); nn = (n * n).sum(1); t = (np.cross(ab, ap_) * n).sum(1); u = (np.cross(ap_, ac) * n).sum(1)
    inside = (u >= 0) & (t >= 0) & (u + t <= nn)
    dist_plane = np.abs((ap_ * n).sum(1)) / np.sqrt(nn)
    def seg(p, x, y):
        v = y - x; tt = np.clip(((p - x) * v).sum(1) / np.maximum((v * v).sum(1), 1e-30), 0, 1); return np.linalg.norm(p - (x + tt[:, None] * v), axis=1)
    de = np.minimum(np.minimum(seg(p, a, b), seg(p, b, c)), seg(p, c, a))
    return np.where(inside, dist_plane, de)
def surf_dev(Vs, Fs, Vt, Ft):
    S = tri_samples(Vs, Fs); C = Vt[Ft].mean(1); idx = cKDTree(C).query(S, k=min(12, len(Ft)))[1]
    best = np.full(len(S), np.inf)
    for j in range(idx.shape[1]):
        f = Ft[idx[:, j]]; best = np.minimum(best, pt_tri_dist(S, Vt[f[:, 0]], Vt[f[:, 1]], Vt[f[:, 2]]))
    return float(best.max() * 1000)
locB = FB[inh[FB].all(1)]; locA = FA[inh[FA].all(1)]
R['patch_surface_deviation_mm'] = dict(new_to_old=round(surf_dev(VA, locA, VB, locB), 4), old_to_new=round(surf_dev(VB, locB, VA, locA), 4))
def topo(V, F):
    k, iv = np.unique(np.round(V, 7), axis=0, return_inverse=True); Fw = iv.ravel()[F]; m = len(k)
    E = np.sort(np.concatenate([Fw[:, [0, 1]], Fw[:, [1, 2]], Fw[:, [2, 0]]]), 1); E = E[E[:, 0] != E[:, 1]]; u, c = np.unique(E, axis=0, return_counts=True)
    nc, lab = connected_components(sp.coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(m, m)), directed=False)
    ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k, Fw)); ms.compute_selection_by_self_intersections_per_face()
    return dict(components=int(len(np.unique(lab[np.unique(Fw)]))), boundary_edges=int((c == 1).sum()), nonmanifold_edges=int((c > 2).sum()),
                self_intersecting_faces=int(ms.current_mesh().face_selection_array().sum()))
R['topology_before'] = topo(VB, FB); R['topology_after'] = topo(VA, FA)
def nrm(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); l = np.linalg.norm(n, axis=1); return n / np.maximum(l, 1e-30)[:, None], l
nA, aA = nrm(VA, FA); R['degenerate_faces_after'] = int((aA < 1e-14).sum())
# orientation: each local new face vs mean normal of old local faces nearby
lA = np.flatnonzero(inh[FA].all(1)); nB, _ = nrm(VB, locB); cB = VB[locB].mean(1); cA = VA[FA[lA]].mean(1)
nn = cKDTree(cB).query(cA, k=6)[1]; ref = nB[nn].mean(1); R['patch_faces_inverted_vs_old_surface'] = int(((nA[lA] * ref).sum(1) < 0).sum())
# folds inside the patch: max angle between adjacent patch faces
def folds(V, F):
    n, _ = nrm(V, F); E = np.concatenate([np.sort(F[:, [0, 1]], 1), np.sort(F[:, [1, 2]], 1), np.sort(F[:, [2, 0]], 1)]); fid = np.tile(np.arange(len(F)), 3)
    o = np.lexsort(E.T[::-1]); E, fid = E[o], fid[o]; same = (E[1:] == E[:-1]).all(1); a, b = fid[:-1][same], fid[1:][same]
    ang = np.degrees(np.arccos(np.clip((n[a] * n[b]).sum(1), -1, 1))); return float(ang.max()), int((ang > 60).sum())
R['patch_max_fold_deg'] = dict(before=round(folds(VB, locB)[0], 1), after=round(folds(VA, locA)[0], 1)); R['patch_folds_over_60deg'] = dict(before=folds(VB, locB)[1], after=folds(VA, locA)[1])
def qual(V, F):
    T = V[F]; e = np.stack([np.linalg.norm(T[:, i] - T[:, (i + 1) % 3], axis=1) for i in range(3)], 1); a = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1) / 2
    return 4 * np.sqrt(3) * a / (e ** 2).sum(1)
R['patch_min_quality'] = dict(before=round(float(qual(VB, locB).min()), 4), after=round(float(qual(VA, locA).min()), 4))
R['height_cm'] = dict(before=round(float(np.ptp(VB[:, 2])) * 100, 5), after=round(float(np.ptp(VA[:, 2])) * 100, 5))
R['bbox_extent_cm'] = dict(before=np.round(np.ptp(VB, 0) * 100, 5).tolist(), after=np.round(np.ptp(VA, 0) * 100, 5).tolist())
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1))
