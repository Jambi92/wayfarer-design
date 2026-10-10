# RAC W3B RM-UB-08 section 17 / 18: scale fields carried by the accepted body extremes. For every body (w3b_bodies) and named field:
#   STRETCH = sqrt(field-core area on the body / canonical area / (h / 188)^2): how much the carried scale units grow / shrink relative to the
#             stature-scaled reference (frames, composition, §263 and tail warps stretch the fields locally);
#   BEND RADIUS on the body's base (normalized by h / 188) -> functional span of the canonical unit;
#   FLIPS of the surfaced field (canonical relief carried along the body's normals; and the candidate boundary relief carried);
#   EDGE STRAIN of the field (stature-normalized edge-length ratio p0.5 / p99.5).
# The candidate envelope must survive these; where an extreme reduces the reachable value, a relationship-aware clamp is reported.
# Usage: python3 w3b_extremes.py   (writes scratch w3b/extremes.json)
import os, sys, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_bodies as BD
CAN = json.load(open(C.W + '/scale_canon_metrics.json'))
def run(boundary=None):
    Z = SC.ref(); Fu = Z['Fu']; masks = RG.masks(); cores = {k: SC.weight(m) >= 0.9 for k, m in masks.items()}
    Vc = Z['Vu']; Nc = Z['N'].astype(np.float64); Sc = Vc + Z['disp'][:, None] * Nc
    def farea(V, F): return 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)
    A0 = farea(Vc, Fu); E = np.vstack([Fu[:, [0, 1]], Fu[:, [1, 2]], Fu[:, [2, 0]]]); L0e = np.linalg.norm(Vc[E[:, 0]] - Vc[E[:, 1]], axis=1)
    out = json.load(open(C.W + '/extremes.json')) if os.path.exists(C.W + '/extremes.json') else {}
    base0 = None
    for bid, p, h in BD.bodies():
        if bid in out: continue
        P = BD.build(bid); Vu, _ = igl.upsample(P, C.F0); Nu = igl.per_vertex_normals(Vu, Fu); k = h / 188.0
        _, _, k1, k2, _ = igl.principal_curvature(P, C.F0, radius=3); K = np.maximum(np.abs(k1), np.abs(k2))
        Sb = Vu + Z['disp'][:, None] * Nu; A = farea(Vu, Fu); Le = np.linalg.norm(Vu[E[:, 0]] - Vu[E[:, 1]], axis=1) / k / np.maximum(L0e, 1e-12)
        res = {}
        for name, core in cores.items():
            fm = core[Fu].all(1)
            if not fm.any(): continue
            stretch = float(np.sqrt(A[fm].sum() / A0[fm].sum() / k ** 2))
            idx = np.where(core)[0]; idx = idx[idx < len(C.V0)]                  # base vertices of the core (upsample keeps them first)
            bend = float(np.percentile(1 / np.maximum(K[idx], 1e-6), 10) / k) if len(idx) > 20 else None
            cr = lambda P_: np.cross(P_[Fu[fm, 1]] - P_[Fu[fm, 0]], P_[Fu[fm, 2]] - P_[Fu[fm, 0]])
            fa = (cr(Sb) * cr(Vu)).sum(1) < 0; fc = (cr(Sc) * cr(Vc)).sum(1) < 0          # folds vs each body's own unsurfaced base
            flips = int((fa & ~fc & (A0[fm] >= 0.25 * np.median(A0[fm]))).sum())         # NEW folds (canonical surface's own folds and slivers excluded)
            em = core[E[:, 0]] & core[E[:, 1]]; st = np.percentile(Le[em], [0.5, 99.5]).round(3).tolist()
            span = float(np.degrees(CAN[name]['size_cm'] * stretch / bend)) if bend else None
            res[name] = dict(stretch=stretch, bend_radius_norm_cm=bend, span_deg=span, flips_canonical_relief=flips, edge_strain=st)
        out[bid] = res; json.dump(out, open(C.W + '/extremes.json', 'w'), indent=1); print(bid, 'done', flush=True)
    return out
if __name__ == '__main__' and len(sys.argv) == 1: run()
# ---- relationship-aware relief clamp on the extremes: for every (body, field) whose CARRIED canonical relief already shows excess folds
# (> max(2, 10 % of the canonical body's own count)) or whose field is in the scale envelope's relief range, sweep the field's relief
# multiplier on that body and report the largest multiplier that keeps the excess folds within tolerance.
def clamp(rs=(0.5, 0.75, 1.0)):                      # + the field's envelope maximum
    Z = SC.ref(); Fu = Z['Fu']; masks = RG.masks(); X = json.load(open(C.W + '/extremes.json'))
    env = json.load(open(C.W + '/scale/envelope.json')); out = json.load(open(C.W + '/extremes_clamp.json')) if os.path.exists(C.W + '/extremes_clamp.json') else {}
    Vc = Z['Vu']; Nc = Z['N'].astype(np.float64)
    W_ = {k: SC.weight(m) for k, m in masks.items()}
    for bid, p, h in BD.bodies():
        if bid == 'SA-M188' or bid in out: continue
        P = BD.build(bid); Vu, _ = igl.upsample(P, C.F0); Nu = igl.per_vertex_normals(Vu, Fu); res = {}
        for k, core in ((k, W_[k] >= 0.9) for k in masks):
            e = env.get(k, {}).get('relief') or {}; rmax = e.get('max_valid') or 1.0
            fm = np.where(core[Fu].all(1))[0]; A0 = 0.5 * np.linalg.norm(np.cross(Vc[Fu[fm, 1]] - Vc[Fu[fm, 0]], Vc[Fu[fm, 2]] - Vc[Fu[fm, 0]]), axis=1); fm = fm[A0 >= 0.25 * np.median(A0)]
            cr = lambda Q: np.cross(Q[Fu[fm, 1]] - Q[Fu[fm, 0]], Q[Fu[fm, 2]] - Q[Fu[fm, 0]])
            nbase = cr(Vu); fc = int(((cr(Vc + Z['disp'][:, None] * Nc) * cr(Vc)).sum(1) < 0).sum()); tol = max(2, 0.10 * fc)
            rows = []
            for r in sorted(set(list(rs) + [rmax])):
                if r > rmax + 1e-9: continue
                rel = Z['disp'] if r == 1.0 else SC.variant(W_[k], 1.0, r, reseed=False)[0]
                fa = int(((cr(Vu + rel[:, None] * Nu) * nbase).sum(1) < 0).sum()); rows.append((r, fa - fc))
            ok = [r for r, ex in rows if ex <= tol]
            res[k] = dict(canonical_folds=fc, tol=tol, excess_by_r=rows, envelope_rmax=rmax, reachable_rmax=max(ok) if ok else None,
                          clamped=(max(ok) if ok else 0.0) < rmax - 1e-9)
        out[bid] = res; json.dump(out, open(C.W + '/extremes_clamp.json', 'w'), indent=1); print('clamp', bid, {k: v['reachable_rmax'] for k, v in res.items() if v['clamped']}, flush=True)
    return out
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'clamp': clamp()
