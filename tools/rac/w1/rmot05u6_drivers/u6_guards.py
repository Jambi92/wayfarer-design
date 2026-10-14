# RM-OT-05U6: corrected LOCAL guards for the bounded posterior upper-notch repair (read-only measurement of a return).
# Additive: the 05U3 guards (u3_guards.py) are unchanged and still reported as historical diagnostics.
#   R1 target roughness   : max angle between each vertex's incident face normals and their mean <= 36.3 deg on the FROZEN target
#                           (cap + ~1 cm strip, u6_sets_v1.json); existing in-target offenders are NOT grandfathered
#   R1 exception identity : S3 70735 / 70592 / 70408 bit-exact (float32) to the frozen 05U baseline
#   locus                 : every approved editable vertex outside the target bit-exact to the baseline (no brush spill)
#   R2 local cap quality  : on the 35 cap faces - no degenerate face (area < 1e-6 cm^2 or a zero edge), no inverted face (normal
#                           opposite to the baseline face normal), min angle >= 10 deg on every face, no NEW cap edge outside the V4
#                           band 0.25-2.5 cm (baseline out-of-band edges may remain only if unchanged; none exist in v1)
#   historical diagnostics: 365-wide roughness; the retired 05U5 per-face-relative sliver rule
# Usage: python3 u6_guards.py --s3 GO-05S-S3.obj --ret RETURN.npz --sets u6_sets_v1.json --out JSON
import argparse, hashlib, json, os, numpy as np, trimesh
from collections import defaultdict
SETS_SHA = '34646b31c0f6bc2a0bb8260cacc567f60d5bc8a2b030e3df7eac3d480d6640bf'
BASE = 'reviews/rac-rmot05u-evidence/checks/return/return.npz'; PRS = 'reviews/rac-rmot05u2-proposal/proposal_sets.npz'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--ret', '--sets', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
res = dict(tool='RM-OT-05U6 local guards', errors=[])
if not os.path.exists(a.sets) or fH(a.sets) != SETS_SHA:
    res['errors'].append('frozen u6 sets missing or hash mismatch (pinned %s)' % SETS_SHA); json.dump(res, open(a.out, 'w'), indent=1); raise SystemExit(4)
SE = json.load(open(a.sets)); T = np.array(SE['target_vertices']); X = np.array(SE['baseline_exception_vertices']); A = np.array(SE['cap_faces'])
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
def load(p):
    R = np.load(p); i = R['s3_vid1'] - 1; V = Vs.copy(); mv = ~np.all(R['V'] == Vs[i].astype(np.float32), 1); V[i[mv]] = R['V'][mv]
    W = np.zeros((len(Vs), 3), np.float32); W[i] = R['V']; return V, W          # V: float64 geometry as reintegrated; W: raw float32 return
Vb, Wb = load(BASE); Vr, Wr = load(a.ret)
E = np.load(PRS)['proposed_editable']
finite = bool(np.isfinite(Wr[E]).all())
vf = defaultdict(list)
for k, f in enumerate(F):
    for v in f: vf[int(v)].append(k)
def rough(V, vs):
    fn = trimesh.Trimesh(V, F, process=False).face_normals; o = {}
    for v in vs:
        n = fn[vf[int(v)]]; c = n.mean(0); c /= np.linalg.norm(c); o[int(v)] = float(np.degrees(np.arccos(np.clip(n @ c, -1, 1))).max())
    return o
def tri(V, fs):
    P = V[F[fs]]; L = np.linalg.norm(P[:, [1, 2, 0]] - P[:, [2, 0, 1]], axis=2)
    with np.errstate(all='ignore'):
        cs = np.stack([(L[:, (i + 1) % 3]**2 + L[:, (i + 2) % 3]**2 - L[:, i]**2) / (2 * L[:, (i + 1) % 3] * L[:, (i + 2) % 3]) for i in range(3)], 1)
        ang = np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
    cr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); return ang, 0.5 * np.linalg.norm(cr, axis=1), cr, L
# R1
rt = rough(Vr, T) if finite else {}; over = sorted(((round(g, 2), v) for v, g in rt.items() if g > SE['roughness_limit_deg']), reverse=True)
res['R1_target_roughness'] = dict(limit_deg=SE['roughness_limit_deg'], target_vertices=len(T), max_now=round(max(rt.values()), 2) if rt else None,
    max_baseline=round(max(rough(Vb, T).values()), 2), over_limit=[dict(s3_vertex=v, roughness=g) for g, v in over], pass_=finite and len(over) == 0)
xm = [int(v) for v in X if not np.array_equal(Wr[v], Wb[v])]
res['R1_baseline_exception_identity'] = dict(vertices=[int(v) for v in X], moved=xm, roughness_now={int(k): round(g, 2) for k, g in rough(Vr, X).items()} if finite else None, pass_=len(xm) == 0)
outside = np.setdiff1d(E, T); om = [int(v) for v in outside if not np.array_equal(Wr[v], Wb[v])]
tm = [int(v) for v in T if not np.array_equal(Wr[v], Wb[v])]
res['locus_outside_target_unchanged'] = dict(editable_outside_target=len(outside), moved=om[:50], moved_count=len(om), pass_=len(om) == 0)
res['changed_target_vertices'] = tm
# R2
ang_b, ar_b, cr_b, _ = tri(Vb, A); ang, ar, cr, L = tri(Vr, A)
cf = [int(f) for f, ok in zip(A, np.any(np.abs(Vr[F[A]] - Vb[F[A]]) > 0, axis=(1, 2))) if ok]
degenerate = [int(A[k]) for k in range(len(A)) if not np.isfinite(ar[k]) or ar[k] < 1e-6 or not np.all(L[k] > 0)]
inverted = [int(A[k]) for k in range(len(A)) if np.isfinite(ar[k]) and (cr[k] @ cr_b[k]) <= 0]
low = [dict(s3_face=int(A[k]), min_angle=round(float(ang[k]), 2), baseline=round(float(ang_b[k]), 2)) for k in range(len(A)) if not (ang[k] >= SE['min_angle_deg'])]
ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[A] for x, y in ((0, 1), (1, 2), (2, 0))}); lo, hi = SE['edge_band_cm']
bo = {tuple(e) for e in SE['baseline_out_of_band_cap_edges']}; bad_e = []
for e in ed:
    l = float(np.linalg.norm(Vr[e[0]] - Vr[e[1]]))
    if not (lo <= l <= hi):
        unchanged = np.array_equal(Wr[e[0]], Wb[e[0]]) and np.array_equal(Wr[e[1]], Wb[e[1]])
        if not (e in bo and unchanged): bad_e.append(dict(edge=list(e), length_cm=round(l, 4), baseline_out_of_band=e in bo))
res['R2_local_cap_quality'] = dict(cap_faces=len(A), min_angle_limit_deg=SE['min_angle_deg'], min_angle_now=round(float(np.nanmin(ang)), 2), min_angle_baseline=round(float(ang_b.min()), 2),
    face_130139=dict(baseline=round(float(ang_b[list(A).index(130139)]), 2), now=round(float(ang[list(A).index(130139)]), 2)),
    degenerate=degenerate, inverted=inverted, below_min_angle=low, edges_checked=len(ed), edge_band_cm=[lo, hi], new_out_of_band_edges=bad_e,
    baseline_out_of_band_edges_reported=sorted(bo), changed_cap_faces=cf, pass_=finite and not degenerate and not inverted and not low and not bad_e)
# historical diagnostics (never decisive in U6)
r365 = rough(Vr, E) if finite else {}
res['historical_diagnostics'] = dict(
    roughness_365_wide=dict(limit_deg=36.3, max_now=round(max(r365.values()), 2) if r365 else None, over_limit=sorted([int(v) for v, g in r365.items() if g > 36.3]), note='diagnostic only (R1)'),
    retired_05U5_per_face_relative_sliver=dict(faces_worse_than_own_baseline=[dict(s3_face=int(A[k]), baseline=round(float(ang_b[k]), 2), now=round(float(ang[k]), 2)) for k in range(len(A)) if ang[k] < ang_b[k] - 0.01],
                                               note='retired for U6 (R2); reported only'))
res['finite'] = finite
res['pass_all_local'] = all(res[k]['pass_'] for k in ('R1_target_roughness', 'R1_baseline_exception_identity', 'locus_outside_target_unchanged', 'R2_local_cap_quality'))
json.dump(res, open(a.out, 'w'), indent=1)
print(json.dumps({k: (v['pass_'] if isinstance(v, dict) and 'pass_' in v else None) for k, v in res.items() if isinstance(v, dict) and 'pass_' in v}))
