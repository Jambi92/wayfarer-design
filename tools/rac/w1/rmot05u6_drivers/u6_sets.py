# RM-OT-05U6: build the FROZEN local-repair sets ONCE from the pinned 05U baseline + 05U2 proposal (never from a return).
#   target      = the 15 approved added (cap) vertices + approved editable vertices within 1.0 cm (Euclidean, baseline) of them
#                 ("upper cap plus approximately 1 cm of the posterior strip"); roughness <= 36.3 deg is binding here (R1)
#   exceptions  = S3 70735, 70592, 70408: baseline roughness offenders outside the working locus; must stay bit-exact (R1)
#   cap_faces   = the 35 approved added faces (R2 local cap quality); edge band 0.25-2.5 cm (V4); min angle >= 10 deg
#   baseline_out_of_band_cap_edges = cap edges outside the band at the frozen baseline (may remain only if unchanged)
# Usage: python3 u6_sets.py --s3 GO-05S-S3.obj --out u6_sets_v1.json
import argparse, hashlib, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--s3'); ap.add_argument('--out'); a = ap.parse_args()
BASE = 'reviews/rac-rmot05u-evidence/checks/return/return.npz'; PRS = 'reviews/rac-rmot05u2-proposal/proposal_sets.npz'
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert fH(BASE) == '0989caf45cba8ddf0f44bdfba962671430c613bb752ac543d99d9b4b16420265'
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
R = np.load(BASE); i = R['s3_vid1'] - 1; V = Vs.copy(); mv = ~np.all(R['V'] == Vs[i].astype(np.float32), 1); V[i[mv]] = R['V'][mv]
P = np.load(PRS); E = P['proposed_editable']; A = P['added_faces']; ring = P['proposed_frozen_ring']
added = np.setdiff1d(np.unique(F[A]), ring); assert len(added) == 15 and np.isin(added, E).all()
d = np.min(np.linalg.norm(V[E][:, None] - V[added][None], axis=2), 1); target = np.sort(E[d <= 1.0])
exc = np.array([70735, 70592, 70408]); assert np.isin(exc, E).all() and not np.isin(exc, target).any()
ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[A] for x, y in ((0, 1), (1, 2), (2, 0))})
L = {e: float(np.linalg.norm(V[e[0]] - V[e[1]])) for e in ed}
out = dict(version='u6_sets_v1', target_vertices=[int(x) for x in target], target_rule='15 added cap vertices + editable within 1.0 cm (baseline, Euclidean)',
           baseline_exception_vertices=[int(x) for x in exc], cap_faces=[int(x) for x in A], cap_edges=len(ed), edge_band_cm=[0.25, 2.5], min_angle_deg=10.0, roughness_limit_deg=36.3,
           baseline_out_of_band_cap_edges=[list(e) for e, l in L.items() if l < 0.25 or l > 2.5],
           sources=dict(baseline_return_npz=fH(BASE), proposal_sets=fH(PRS), s3_obj=fH(a.s3)))
json.dump(out, open(a.out, 'w'), indent=1, sort_keys=True); print(json.dumps({k: v for k, v in out.items() if k != 'cap_faces'})); print('sha', fH(a.out))
