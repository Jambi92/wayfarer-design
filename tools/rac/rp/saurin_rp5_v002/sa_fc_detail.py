# sa_fc_detail.py CAGE.npz OUT.json : layered scale-detail prototype on the full cage (order ad9cb85 §19 / f0a2b96 §18). Layer 2 = the canonical scale
# relief (the saved W2I6 seed realization: saurin_w2_final_surface_delta.npz on the igl.upsample of the canonical base; seeds sha a1d07b8d...) transported
# onto a cage-derived surface: cage -> 2 Catmull-Clark levels -> closest point on the working base (triangle + barycentric) -> the delta interpolated
# piecewise-linearly on that triangle's 4 upsampled children -> displaced detail surface. Compared with the canonical surfaced organism.
# The cage itself carries no scale geometry (approved layered strategy); PD-1 (transport across creator states) stays a separate dependency.
import sys, os, json, hashlib, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
CG, OUT = sys.argv[1:3]; W = '/tmp/claude-0/rt/sa'
b = np.load(W + '/src/saurin_w2_final_base.npz'); V0 = b['v'].astype(float); F0 = b['f'].astype(np.int64)
dz = np.load(W + '/src/saurin_w2_final_surface_delta.npz')['d'].astype(float)
Vu, Fu = igl.upsample(V0, F0); S = Vu + dz                                                       # canonical surfaced (rebuild_w2_final route)
seed_sha = hashlib.sha256(open(W + '/src/saurin_w2_seeds.npy', 'rb').read()).hexdigest()
det = hashlib.sha256(np.ascontiguousarray(S.astype(np.float32)).tobytes()).hexdigest()
z = np.load(CG); Q = z['Q']; Vc = (z['bc'][:, :, None] * V0[F0[z['tri']]]).sum(1)                 # cage on the canonical base (thigh patch excluded below)
Vs, Qs, _ = CC.cc(Vc, Q, np.arange(len(Q))); Vs, Qs, _ = CC.cc(Vs, Qs, np.arange(len(Qs)))
_, ti, cp = igl.point_mesh_squared_distance(Vs, V0, F0)
ch = Fu.reshape(-1, 4, 3) if len(Fu) == 4 * len(F0) else None
P = np.zeros_like(cp)
kids = Fu.reshape(len(F0), 4, 3); out = np.zeros(len(cp))
for j in range(4):
    pass
# closest point inside each base triangle's 4 children (upsample children are consecutive faces)
best = np.full(len(cp), 1e9); disp = np.zeros_like(cp)
for j in range(4):
    T = kids[ti, j]; a, b_, c = Vu[T[:, 0]], Vu[T[:, 1]], Vu[T[:, 2]]
    v0 = b_ - a; v1 = c - a; v2 = cp - a; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
    l1 = (d11 * d20 - d01 * d21) / den; l2 = (d00 * d21 - d01 * d20) / den; l0 = 1 - l1 - l2; inside = (l0 > -1e-6) & (l1 > -1e-6) & (l2 > -1e-6)
    err = np.where(inside, 0, -np.minimum(np.minimum(l0, l1), l2)); upd = err < best; best[upd] = err[upd]
    bc = np.clip(np.c_[l0, l1, l2], 0, 1); bc /= bc.sum(1, keepdims=True); disp[upd] = (bc[:, :, None] * dz[T])[upd].sum(1)
Dsurf = cp + disp
lab = G.LAB; d2, fi2, _ = igl.point_mesh_squared_distance(S[::4], Dsurf, np.r_[Qs[:, [0, 1, 2]], Qs[:, [0, 2, 3]]]); dd = np.sqrt(d2) * 10
reg = lab[np.minimum(np.arange(len(Vu))[::4], len(V0) - 1)] if False else None
# region of upsampled vertex = label of the nearest base vertex
from scipy.spatial import cKDTree
rl = lab[cKDTree(V0).query(Vu[::4])[1]]
res = dict(seeds_sha256=seed_sha, canonical_surfaced_float32_sha256=det, canonical_surfaced_verts=int(len(S)), detail_surface_verts=int(len(Dsurf)),
           deviation_canonical_to_detail_mm=dict(median=round(float(np.median(dd)), 4), p95=round(float(np.percentile(dd, 95)), 4), p99=round(float(np.percentile(dd, 99)), 4), max=round(float(dd.max()), 4)),
           by_region_p95_mm={str(r): round(float(np.percentile(dd[rl == r], 95)), 4) for r in np.unique(rl)},
           relief_amplitude_transported_mm=dict(mean=round(float(np.linalg.norm(disp, axis=1).mean() * 10), 4), max=round(float(np.linalg.norm(disp, axis=1).max() * 10), 4)),
           relief_amplitude_canonical_mm=dict(mean=round(float(np.linalg.norm(dz, axis=1).mean() * 10), 4), max=round(float(np.linalg.norm(dz, axis=1).max() * 10), 4)),
           representation=dict(geometry='cage = structural / macro anatomy, silhouette, field boundaries (no scale geometry)',
                               displacement_or_normal='scale relief (<= 1.7 mm) = displacement / normal layer regenerated from the seed realization; field boundaries continuous by construction (the delta is interpolated, never re-seeded on the cage)'),
           joints_note='joint regions carry the canonical relief unchanged (transport is per-point); PD-1 governs re-realization on deformed / creator states')
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(res)[:900])
