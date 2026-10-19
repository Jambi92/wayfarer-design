"""RAC RP1 T-6 re-measure with a tessellation-independent section centroid: the plane/mesh section is built as segments (one per
crossed triangle) and the centroid is the LENGTH-weighted mean of the segment midpoints (the edge-point mean in rp1_landmarks.py
depends on vertex density, so two meshes with different tessellation disagree even when the surface agrees).
Both the source and the candidate are re-sectioned with the same planes/radius from the source landmark file.
Usage: python3 rp1_landmarks_len.py SOURCE.npz CANDIDATE.npz SOURCE_LANDMARKS.json OUT.json"""
import sys, json, numpy as np
def load(p):
    z = np.load(p); return z['V'].astype(float), z['F'].astype(np.int64)
def sec(V, F, p, n, R):
    d = (V - p) @ n; s = np.sign(d[F]); m = (s.min(1) < 0) & (s.max(1) > 0); T = F[m]; D = d[T]; P = V[T]; pts = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        c = D[:, a] * D[:, b] < 0; t = np.where(c, D[:, a] / np.where(c, D[:, a] - D[:, b], 1), np.nan)
        pts.append(P[:, a] + (P[:, b] - P[:, a]) * t[:, None])
    pts = np.stack(pts, 1); ok = ~np.isnan(pts[..., 0]); k = ok.sum(1) == 2; pts = pts[k]; ok = ok[k]
    seg = np.array([q[o][:2] for q, o in zip(pts, ok)]) if len(pts) else np.zeros((0, 2, 3))
    if not len(seg): return None
    mid = seg.mean(1); L = np.linalg.norm(seg[:, 1] - seg[:, 0], axis=1); sel = np.linalg.norm(mid - p, axis=1) < R
    if sel.sum() < 8: return None
    return (mid[sel] * L[sel, None]).sum(0) / L[sel].sum()
S, SF = load(sys.argv[1]); C, CF = load(sys.argv[2]); LM = json.load(open(sys.argv[3])); R = {}
items = [(k, v) for k, v in LM.items() if isinstance(v, dict) and 'plane_point' in v]
items += [('tail_%02d' % st['station'], st) for st in LM.get('tail_chain', {}).get('stations', [])]
for k, v in items:
    p, n, r = np.array(v['plane_point']), np.array(v['plane_normal']), v['radius_cm']
    a = sec(S, SF, p, n, r); b = sec(C, CF, p, n, r)
    R[k] = None if a is None or b is None else round(float(np.linalg.norm(a - b) * 10), 3)
json.dump(R, open(sys.argv[4], 'w'), indent=1); print(json.dumps(R))
