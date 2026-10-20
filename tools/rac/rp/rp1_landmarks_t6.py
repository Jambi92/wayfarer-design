"""RAC RP1E T-6 as ruled (v014 manifold-contact ruling §8): length-weighted section centroid with EXACT clipping of every section
segment against the landmark radius circle (source and candidate identically, all landmarks and tail stations), plus the
connected-curve rule for the hip landmarks (curve nearest the landmark plane point, from rp1_landmarks_comp.py).
Usage: python3 rp1_landmarks_t6.py SOURCE.npz CANDIDATE.npz SOURCE_LANDMARKS.json OUT.json"""
import sys, json, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rp1_landmarks_comp import load, segs, curves
def clip(seg, p, r):
    out = []
    for a, b in seg:
        da, db = np.linalg.norm(a - p), np.linalg.norm(b - p)
        if da <= r and db <= r: out.append((a, b)); continue
        d = b - a; A = d @ d; B = 2 * (a - p) @ d; C = (a - p) @ (a - p) - r * r; disc = B * B - 4 * A * C
        if disc <= 0 or A == 0: continue
        t1, t2 = sorted(((-B - np.sqrt(disc)) / (2 * A), (-B + np.sqrt(disc)) / (2 * A)))
        lo, hi = max(t1, 0.0), min(t2, 1.0)
        if hi > lo: out.append((a + lo * d, a + hi * d))
    return np.array(out).reshape(-1, 2, 3)
def centroid(seg, p, r, comp):
    s = clip(seg, p, r)
    if comp and len(s):
        lab = curves(s); mid = s.mean(1); best = min(np.unique(lab), key=lambda c: np.linalg.norm(mid[lab == c] - p, axis=1).min()); s = s[lab == best]
    if len(s) < 8: return None, 0.0
    mid = s.mean(1); L = np.linalg.norm(s[:, 1] - s[:, 0], axis=1); return (mid * L[:, None]).sum(0) / L.sum(), float(L.sum())
if __name__ == '__main__':
    S, SF = load(sys.argv[1]); C, CF = load(sys.argv[2]); LM = json.load(open(sys.argv[3]))
    items = [(k, v) for k, v in LM.items() if isinstance(v, dict) and 'plane_point' in v]
    items += [('tail_%02d' % st['station'], st) for st in LM.get('tail_chain', {}).get('stations', [])]
    R = {}
    for k, v in items:
        p, n, r = np.array(v['plane_point']), np.array(v['plane_normal']), v['radius_cm']; comp = k.startswith('hip')
        a, la = centroid(segs(S, SF, p, n), p, r, comp); b, lb = centroid(segs(C, CF, p, n), p, r, comp)
        R[k] = None if a is None or b is None else dict(drift_mm=round(float(np.linalg.norm(a - b) * 10), 3), src_len_cm=round(la, 2), cand_len_cm=round(lb, 2), component_rule=comp)
    json.dump(R, open(sys.argv[4], 'w'), indent=1); print(json.dumps({k: (v['drift_mm'] if v else None) for k, v in R.items()}))
