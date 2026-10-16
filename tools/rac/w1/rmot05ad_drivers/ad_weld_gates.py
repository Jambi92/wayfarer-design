# RM-OT-05AD s4 weld-safety gates: 05AB1 baseline (before_VF.npz) vs welded 05AD derivative (after_VF.npz), Blender world metres.
# Checks: surface identity (every old vertex lands on a new vertex; triangle-by-triangle position identity; two-sided Hausdorff
# by vertex), stature / bbox, components / boundary / non-manifold edges (true Blender topology AND position-welded), flips,
# degenerates, self-intersections (pymeshlab, before and after), weld confined to the band, protected regions untouched.
# Usage: python3 -I ad_weld_gates.py BEFORE_VF.npz AFTER_VF.npz OLD_TO_NEW.npy PROTECT.npy OUT.json
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
bp, ap, mp, pp, out = sys.argv[1:6]
B = np.load(bp); A = np.load(ap); VB, FB = B['V'], B['F']; VA, FA = A['V'], A['F']; o2n = np.load(mp); P = np.load(pp)
R = dict(vertices=dict(before=len(VB), after=len(VA)), triangles=dict(before=len(FB), after=len(FA)))
def topo(V, F):
    n = len(V); E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1); E = E[E[:, 0] != E[:, 1]]
    u, c = np.unique(E, axis=0, return_counts=True)
    nc, lab = connected_components(sp.coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(n, n)), directed=False)
    used = np.unique(F); real = len(np.unique(lab[used]))
    bnd = u[c == 1]
    return dict(components=int(real), boundary_edges=int((c == 1).sum()), nonmanifold_edges=int((c > 2).sum())), bnd
def welded(V, F):
    k, iv = np.unique(np.round(V, 7), axis=0, return_inverse=True); return k, iv.ravel()[F]
R['topology_blender_before'], bndB = topo(VB, FB); R['topology_blender_after'], bndA = topo(VA, FA)
kB, WB = welded(VB, FB); kA, WA = welded(VA, FA)
R['topology_position_welded_before'], _ = topo(kB, WB); R['topology_position_welded_after'], _ = topo(kA, WA)
zB = (VB[:, 2] - VB[:, 2].min()) * 100
# Blender-topology boundary (unwelded seam) edges remaining inside the AC1 band, before vs after
zA = (VA[:, 2] - VA[:, 2].min()) * 100
inb = lambda V, z, e: (z[e[:, 0]] >= 117) & (z[e[:, 0]] <= 168.3) & (z[e[:, 1]] >= 117) & (z[e[:, 1]] <= 168.3)
R['seam_edges_in_117_168cm_band'] = dict(before=int(inb(VB, zB, bndB).sum()), after=int(inb(VA, zA, bndA).sum()))
# surface identity
d_o2n = np.linalg.norm(VA[o2n] - VB, axis=1); dA, _ = cKDTree(VB).query(VA)
R['hausdorff_vertex_mm'] = dict(old_to_new=float(d_o2n.max() * 1000), new_to_old=float(dA.max() * 1000))
same_tri = np.array_equal(np.sort(o2n[FB], 1)[np.lexsort(np.sort(o2n[FB], 1).T[::-1])], np.sort(FA, 1)[np.lexsort(np.sort(FA, 1).T[::-1])])
R['triangles_identical_after_vertex_remap'] = bool(same_tri)
R['triangle_corner_max_shift_mm'] = float(np.linalg.norm(VA[o2n[FB]] - VB[FB], axis=2).max() * 1000)
R['height_cm'] = dict(before=round(float(np.ptp(VB[:, 2])) * 100, 5), after=round(float(np.ptp(VA[:, 2])) * 100, 5))
R['bbox_extent_cm'] = dict(before=np.round(np.ptp(VB, 0) * 100, 5).tolist(), after=np.round(np.ptp(VA, 0) * 100, 5).tolist())
def nrm(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); l = np.linalg.norm(n, axis=1); return n / np.maximum(l, 1e-30)[:, None], l
nB, aB = nrm(VB, FB); nA, aA = nrm(VA, o2n[FB])
R['flipped_faces'] = int(((nB * nA).sum(1) < 0).sum()); R['degenerate_faces'] = dict(before=int((aB < 1e-14).sum()), after=int((aA < 1e-14).sum()))
# where did merges happen
merged = np.bincount(o2n, minlength=len(VA)) > 1; mz = zA[merged]
R['merged_vertices_z_from_floor_cm'] = [round(float(mz.min()), 2), round(float(mz.max()), 2)] if merged.any() else None
R['protected_vertices_merged'] = int(((P >= 1) & merged[o2n]).sum())
R['protected_vertices_moved'] = int(((P >= 1) & (d_o2n > 0)).sum())
try:
    import pymeshlab
    def si(k, W):
        ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k, W)); ms.compute_selection_by_self_intersections_per_face()
        return int(ms.current_mesh().face_selection_array().sum())
    R['self_intersecting_faces'] = dict(before=si(kB, WB), after=si(kA, WA))
except Exception as e:
    R['self_intersecting_faces'] = dict(error=repr(e))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1))
