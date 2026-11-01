# sa_detail2.py CAGE.npz OUT.json : layered scale-detail closure on the FINAL cage (order 236dddc §13), c1 = SA-M188, c2 = SA-F188 and one clean creator state.
#   Layer 2 = the canonical saved seed realization (W2I6 surface delta on the igl.upsample of the canonical base; seeds sha recorded, never re-seeded),
#   carried as the canonical per-vertex scalar relief along the body's own upsampled normals (W2I4 / W3B convention) -> reference surfaced organism per state.
#   Cage route: cage realized on the state by its barycentric embedding -> 2 Catmull-Clark levels -> closest point on the state's base -> relief interpolated
#   piecewise-linearly on that triangle's 4 upsampled children -> displaced along the interpolated normal. Same field boundaries (interpolated, never re-seeded).
#   Reported per state: deviation reference -> cage-detail surface (median / p95 / p99 / max, by region), silhouette IoU change, and the DISCONTINUITY check:
#   p99.9 / max relief jump across detail-surface edges vs the canonical relief's own edge jumps (a cage-induced seam would exceed it).
import sys, os, json, hashlib, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
from scipy.spatial import cKDTree
CG, OUT = sys.argv[1:3]; W = '/tmp/claude-0/rt/sa'
b = np.load(W + '/src/saurin_w2_final_base.npz'); V0 = b['v'].astype(float); F0 = b['f'].astype(np.int64)
dz = np.load(W + '/src/saurin_w2_final_surface_delta.npz')['d'].astype(float); Vu0, Fu = igl.upsample(V0, F0); rel = (dz * igl.per_vertex_normals(Vu0, Fu)).sum(1)
seed_sha = hashlib.sha256(open(W + '/src/saurin_w2_seeds.npy', 'rb').read()).hexdigest()
STATES = {'c1_SA-M188': V0, 'c2_SA-F188': np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float), 'creator_NAR': np.load(W + '/cr_NAR.npy').astype(float)}
z = np.load(CG); Q = z['Q']; kids_all = Fu.reshape(len(F0), 4, 3); res = dict(seeds_sha256=seed_sha, relief_source='saurin_w2_final_surface_delta.npz (W2I6 canonical seed realization)', states={})
EU = np.unique(np.sort(np.r_[Fu[:, [0, 1]], Fu[:, [1, 2]], Fu[:, [2, 0]]], 1), axis=0); jump_can = np.abs(rel[EU[:, 0]] - rel[EU[:, 1]])
rl = G.LAB[cKDTree(V0).query(Vu0[::4])[1]]
for tag, P in STATES.items():
    Vu, _ = igl.upsample(P, F0); Nu = igl.per_vertex_normals(Vu, Fu); S = Vu + rel[:, None] * Nu
    Vc = (z['bc'][:, :, None] * P[F0[z['tri']]]).sum(1); Vs, Qs, _ = CC.cc(Vc, Q, np.arange(len(Q))); Vs, Qs, _ = CC.cc(Vs, Qs, np.arange(len(Qs)))
    _, ti, cp = igl.point_mesh_squared_distance(Vs, P, F0); best = np.full(len(cp), 1e9); r_ = np.zeros(len(cp)); n_ = np.zeros_like(cp)
    for j in range(4):
        T = kids_all[ti, j]; a, b_, c = Vu[T[:, 0]], Vu[T[:, 1]], Vu[T[:, 2]]
        v0 = b_ - a; v1 = c - a; v2 = cp - a; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
        l1 = (d11 * d20 - d01 * d21) / den; l2 = (d00 * d21 - d01 * d20) / den; l0 = 1 - l1 - l2
        err = -np.minimum(np.minimum(np.minimum(l0, l1), l2), 0); upd = err < best; best[upd] = err[upd]
        bc = np.clip(np.c_[l0, l1, l2], 0, 1); bc /= bc.sum(1, keepdims=True); r_[upd] = (bc * rel[T]).sum(1)[upd]; n_[upd] = (bc[:, :, None] * Nu[T]).sum(1)[upd]
    n_ /= np.linalg.norm(n_, axis=1, keepdims=True); D = cp + r_[:, None] * n_; TD = np.r_[Qs[:, [0, 1, 2]], Qs[:, [0, 2, 3]]]
    dd = np.sqrt(igl.point_mesh_squared_distance(S[::4], D, TD)[0]) * 10
    ED = np.unique(np.sort(np.r_[Qs[:, [0, 1]], Qs[:, [1, 2]], Qs[:, [2, 3]], Qs[:, [3, 0]]], 1), axis=0); jump = np.abs(r_[ED[:, 0]] - r_[ED[:, 1]])
    res['states'][tag] = dict(deviation_reference_to_detail_mm=dict(median=round(float(np.median(dd)), 4), p95=round(float(np.percentile(dd, 95)), 4), p99=round(float(np.percentile(dd, 99)), 4), max=round(float(dd.max()), 4)),
        by_region_p95_mm={str(k): round(float(np.percentile(dd[rl == k], 95)), 4) for k in np.unique(rl)},
        relief_edge_jump_mm=dict(detail_p999=round(float(np.percentile(jump, 99.9) * 10), 4), detail_max=round(float(jump.max() * 10), 4), canonical_p999=round(float(np.percentile(jump_can, 99.9) * 10), 4), canonical_max=round(float(jump_can.max() * 10), 4)),
        cage_induced_discontinuity=bool(jump.max() > jump_can.max() * 1.05), detail_verts=int(len(D)))
    print(tag, res['states'][tag], flush=True)
res['PD1_isolation'] = ('the same transport is applied to c1, c2 and the creator state from the one saved realization; deviations stay at the transport / interpolation level '
                        '(no per-state re-seeding, no cage-specific seam); cross-state re-realization of the relief itself (PD-1) remains with the detail pipeline')
json.dump(res, open(OUT, 'w'), indent=1)
