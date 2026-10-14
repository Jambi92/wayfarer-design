# RM-OT-05U7: local safety guards on the 22 U7 faces + DIAGNOSTIC-ONLY facet report (read-only measurement of a return).
#   local quality (mandatory): no degenerate face (area < 1e-6 cm^2 or zero edge), no inverted face (normal opposite to the cp3 face
#     normal), every U7 face min angle >= 10 deg, no NEW edge outside 0.25-2.5 cm (no U7 edge is out of band at cp3)
#   facet diagnostic (reported only; NO pass threshold): dihedral angle (deg) between adjacent faces for every edge touching a U7 face,
#     max / p95 / per-seed, compared with cp3; it confirms whether the upper-crease facets are reduced and is never a gate
# Usage: python3 u7_guards.py --s3 GO-05S-S3.obj --ret RETURN.npz --cp3 cp3_return.npz --sets DIR --out JSON
import argparse, hashlib, json, os, numpy as np, trimesh
from collections import defaultdict
SETS_SHA = '67aeca8d826cf6a9566d1b2987f26aa4c6565129a1b47f2eeda542f7a50ae1b0'
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--ret', '--cp3', '--sets', '--out')]; a = ap.parse_args()
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); sp = os.path.join(a.sets, 'u7_sets_v1.json'); res = dict(tool='RM-OT-05U7 local guards', errors=[])
if not os.path.exists(sp) or fH(sp) != SETS_SHA:
    res['errors'].append('u7 sets missing or hash mismatch'); json.dump(res, open(a.out, 'w'), indent=1); raise SystemExit(4)
SE = json.load(open(sp)); U7F = np.array(SE['u7_faces']); SEEDS = SE['seeds']
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
def geo(p):
    R = np.load(p); i = R['s3_vid1'] - 1; V = Vs.copy(); W = np.zeros_like(Vs, dtype=np.float32); W[i] = R['V']; mv = ~np.all(W == Vs.astype(np.float32), 1); V[mv] = W[mv]; return V
Vc = geo(a.cp3); Vr = geo(a.ret); finite = bool(np.isfinite(Vr).all())
def tri(V, fs):
    P = V[F[fs]]; L = np.linalg.norm(P[:, [1, 2, 0]] - P[:, [2, 0, 1]], axis=2)
    with np.errstate(all='ignore'):
        cs = np.stack([(L[:, (k + 1) % 3]**2 + L[:, (k + 2) % 3]**2 - L[:, k]**2) / (2 * L[:, (k + 1) % 3] * L[:, (k + 2) % 3]) for k in range(3)], 1)
        ang = np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
    cr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); return ang, 0.5 * np.linalg.norm(cr, axis=1), cr, L
ab, _, crb, _ = tri(Vc, U7F); an, ar, cr, L = tri(Vr, U7F)
degen = [int(U7F[k]) for k in range(len(U7F)) if not np.isfinite(ar[k]) or ar[k] < 1e-6 or not np.all(L[k] > 0)]
inv = [int(U7F[k]) for k in range(len(U7F)) if np.isfinite(ar[k]) and cr[k] @ crb[k] <= 0]
low = [dict(s3_face=int(U7F[k]), min_angle=round(float(an[k]), 2), cp3=round(float(ab[k]), 2)) for k in range(len(U7F)) if not an[k] >= SE['min_angle_deg']]
lo, hi = SE['edge_band_cm']; ed = sorted({tuple(sorted((int(f[x]), int(f[y])))) for f in F[U7F] for x, y in ((0, 1), (1, 2), (2, 0))})
bad = [dict(edge=list(e), length_cm=round(float(np.linalg.norm(Vr[e[0]] - Vr[e[1]])), 4)) for e in ed if not lo <= np.linalg.norm(Vr[e[0]] - Vr[e[1]]) <= hi]
res['local_quality'] = dict(u7_faces=len(U7F), min_angle_now=round(float(np.nanmin(an)), 2), min_angle_cp3=round(float(ab.min()), 2), degenerate=degen, inverted=inv, below_10deg=low,
                            edges_checked=len(ed), out_of_band_edges=bad, pass_=finite and not degen and not inv and not low and not bad)
# facet diagnostic
def facets(V):
    m = trimesh.Trimesh(V, F, process=False); adj = m.face_adjacency; ae = m.face_adjacency_edges; fn = m.face_normals
    sel = np.isin(adj, U7F).any(1); d = np.degrees(np.arccos(np.clip((fn[adj[sel, 0]] * fn[adj[sel, 1]]).sum(1), -1, 1))); e = ae[sel]
    per = {s: round(float(d[(e == s).any(1)].max()), 2) for s in SEEDS}
    top = [dict(edge=[int(x) for x in e[k]], dihedral=round(float(d[k]), 2)) for k in np.argsort(-d)[:8]]
    return dict(edges=int(len(d)), max=round(float(d.max()), 2), p95=round(float(np.percentile(d, 95)), 2), mean=round(float(d.mean()), 2), per_seed_max=per, top_edges=top)
res['facet_diagnostic'] = dict(note='DIAGNOSTIC ONLY - no pass threshold; dihedral between adjacent faces on every edge touching a U7 face', cp3=facets(Vc), now=facets(Vr) if finite else None)
res['changed_vertices_vs_cp3'] = [int(v) for v in np.where(np.any(Vr != Vc, 1))[0]] if finite else None
res['finite'] = finite
json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps(dict(local_quality=res['local_quality']['pass_'], facet_max_cp3=res['facet_diagnostic']['cp3']['max'], facet_max_now=(res['facet_diagnostic']['now'] or {}).get('max'))))
