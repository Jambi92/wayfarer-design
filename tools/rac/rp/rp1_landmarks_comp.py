"""RAC RP1E T-6 with the anatomical-component filter (v014 ruling §7.1).
Same plane / radius / length-weighted centroid as rp1_landmarks_len.py, but the section segments are first grouped into connected
section curves (segments whose end points coincide within TOL, union-find), and only the curve(s) belonging to the cluster nearest
the landmark's own source region are kept:  the kept cluster is the connected curve with the smallest distance to the landmark
plane_point (the source joint/pelvis landmark).  The identical rule is applied to source and candidate.
Usage: python3 rp1_landmarks_comp.py SOURCE.npz CANDIDATE.npz SOURCE_LANDMARKS.json OUT.json [keys,comma]"""
import sys, json, numpy as np
from scipy.spatial import cKDTree
def load(p):
    z = np.load(p); return z['V'].astype(float), z['F'].astype(np.int64)
def segs(V, F, p, n):
    d = (V - p) @ n; s = np.sign(d[F]); m = (s.min(1) < 0) & (s.max(1) > 0); T = F[m]; D = d[T]; P = V[T]; pts = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        c = D[:, a] * D[:, b] < 0; t = np.where(c, D[:, a] / np.where(c, D[:, a] - D[:, b], 1), np.nan)
        pts.append(P[:, a] + (P[:, b] - P[:, a]) * t[:, None])
    pts = np.stack(pts, 1); ok = ~np.isnan(pts[..., 0]); k = ok.sum(1) == 2; pts = pts[k]; ok = ok[k]
    return np.array([q[o][:2] for q, o in zip(pts, ok)]) if len(pts) else np.zeros((0, 2, 3))
def curves(seg, tol=1e-4):
    E = seg.reshape(-1, 3); tr = cKDTree(E); par = np.arange(len(E))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i in range(len(seg)): par[f(2 * i)] = f(2 * i + 1)
    for a, b in tr.query_pairs(tol): par[f(a)] = f(b)
    r = np.array([f(2 * i) for i in range(len(seg))]); return r
def cent(seg, p, R, comp):
    if not len(seg): return None, None
    mid = seg.mean(1); L = np.linalg.norm(seg[:, 1] - seg[:, 0], axis=1); sel = np.linalg.norm(mid - p, axis=1) < R
    seg, mid, L = seg[sel], mid[sel], L[sel]
    if len(L) < 8: return None, None
    if comp:
        lab = curves(seg); best = None
        for c in np.unique(lab):
            dmin = np.linalg.norm(mid[lab == c] - p, axis=1).min()
            if best is None or dmin < best[0]: best = (dmin, c)
        k = lab == best[1]; mid, L = mid[k], L[k]
    if len(L) < 8: return None, None
    return (mid * L[:, None]).sum(0) / L.sum(), float(L.sum())
if __name__ == '__main__':
    S, SF = load(sys.argv[1]); C, CF = load(sys.argv[2]); LM = json.load(open(sys.argv[3]))
    keys = sys.argv[5].split(',') if len(sys.argv) > 5 else None
    items = [(k, v) for k, v in LM.items() if isinstance(v, dict) and 'plane_point' in v]
    items += [('tail_%02d' % st['station'], st) for st in LM.get('tail_chain', {}).get('stations', [])]
    R = {}
    for k, v in items:
        if keys and k not in keys: continue
        p, n, r = np.array(v['plane_point']), np.array(v['plane_normal']), v['radius_cm']
        a, la = cent(segs(S, SF, p, n), p, r, True); b, lb = cent(segs(C, CF, p, n), p, r, True)
        R[k] = None if a is None or b is None else dict(drift_mm=round(float(np.linalg.norm(a - b) * 10), 3), src_len_cm=round(la, 2), cand_len_cm=round(lb, 2))
    json.dump(R, open(sys.argv[4], 'w'), indent=1); print(json.dumps({k: (v['drift_mm'] if v else None) for k, v in R.items()}))
