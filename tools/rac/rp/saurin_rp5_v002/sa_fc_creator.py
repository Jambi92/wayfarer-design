# sa_fc_creator.py CAGE.npz OUT.json STATE=path.npy ... : creator-support topology diagnostics (order f0a2b96 §17). Each accepted creator state is a body on the
# shared canonical base face list built with the accepted W2 route (tools/rac/w1/w2i4_drivers/sa_finish.build_f; W3B body set); the cage is realized on it by
# its barycentric embedding (no re-fit). Per state: fit to that body (cage -> body distance stats), quad quality (angles / aspect vs rest), flipped quads
# relative to rest, edge strain p95 / max -> PASS (fit p95 <= 1.5 mm, no flips, aspect>4 not increased > 10 %), CONSTRAIN (fit max > 3 mm or strain > 25 %), FAIL (flips).
import sys, os, json, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, OUT = sys.argv[1:3]; states = dict(a.split('=') for a in sys.argv[3:]); z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; F = G.F
def quality(P):
    ang = []
    for k in range(4):
        p0, p1, p2 = P[Q[:, (k - 1) % 4]], P[Q[:, k]], P[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / (np.linalg.norm(u1, axis=1) * np.linalg.norm(u2, axis=1) + 1e-12), -1, 1))))
    ang = np.stack(ang, 1); sd = np.stack([np.linalg.norm(P[Q[:, (k + 1) % 4]] - P[Q[:, k]], axis=1) for k in range(4)], 1)
    return ((ang.min(1) < 45) | (ang.max(1) > 135)), sd.max(1) / np.maximum(sd.min(1), 1e-9), np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]])
P0 = (bc[:, :, None] * G.V[F[fi]]).sum(1); a0, s0, n0 = quality(P0); E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
l0 = np.linalg.norm(P0[E[:, 0]] - P0[E[:, 1]], axis=1); res = {}; T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
for nm, path in states.items():
    VB = np.load(path).astype(float); P = (bc[:, :, None] * VB[F[fi]]).sum(1); a1, s1, n1 = quality(P)
    rng = np.random.default_rng(0); smp = rng.choice(len(VB), 200000, replace=False); d = np.sqrt(igl.point_mesh_squared_distance(VB[smp], P, T)[0]) * 10
    cosn = (n0 * n1).sum(1) / (np.linalg.norm(n0, axis=1) * np.linalg.norm(n1, axis=1) + 1e-12); flips = int((cosn < 0).sum())
    l1 = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1); st = np.abs(l1 / np.maximum(l0, 1e-9) - 1)
    worst = np.argsort(-st)[:200]; wl = sorted({str(z['qlab'][qi]) for qi in np.nonzero(np.isin(Q, E[worst]).any(1))[0][:400]})[:6]
    r = dict(fit_mm=dict(median=round(float(np.median(d)), 3), p95=round(float(np.percentile(d, 95)), 3), max=round(float(d.max()), 3)), flipped_quads=flips,
             angle_outliers=int(a1.sum()), angle_outliers_rest=int(a0.sum()), aspect_gt4=int((s1 > 4).sum()), aspect_gt4_rest=int((s0 > 4).sum()),
             edge_strain_p95_pct=round(float(np.percentile(st, 95) * 100), 2), edge_strain_max_pct=round(float(st.max() * 100), 2), thinnest_margin_regions=wl,
             stature_cm=round(float(np.ptp(VB[:, 2])), 2))
    r['verdict'] = 'FAIL' if flips else ('CONSTRAIN' if (r['fit_mm']['max'] > 3 or r['edge_strain_max_pct'] > 25) else ('PASS' if r['fit_mm']['p95'] <= 1.5 and r['aspect_gt4'] <= 1.1 * r['aspect_gt4_rest'] + 5 else 'CONSTRAIN'))
    res[nm] = r; print(nm, r, flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
