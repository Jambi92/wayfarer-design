# RM-OT-05X R1: DISPOSABLE diagnostic body-only copy, tail separated by TUBE TRACKING (the tail lies against the buttocks, so plane
# rules fail). From a seed loop on the free hanging tail, planes normal to the running tail axis are stepped in both directions;
# the tail centreline is followed while the section loop stays tube-like. Faces within (loop radius x 1.35) of the tracked
# centreline, plus faces above the neck minimum, are deleted; only the largest piece is kept. Where tracking stops (the tail merges
# with the body surface) is REPORTED as the tail contact/root zone. Faces deleted only; never a repair; source untouched.
# Usage: python3 x_tailtrack.py FIG.npz OUT.npz SEED_Z_FRAC SEED_MIN_Y_CM [STEP_CM=1.0] [SEED_MAX_PERIMETER_CM=30]
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
fi, fo, sf, smy = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); STEP = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0; PMAX = float(sys.argv[6]) if len(sys.argv) > 6 else 30.0
d = np.load(fi); P = d['V'].astype(np.float64); F = d['F']; V = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) * 100; H = V[:, 2].max()
m = trimesh.Trimesh(V, F, process=False)
def loops(o, nrm):
    s = m.section(plane_origin=o, plane_normal=nrm)
    if s is None: return []
    out = []
    for e in s.discrete:
        c = e.mean(0); out.append((np.linalg.norm(np.diff(e, axis=0), axis=1).sum(), c, np.linalg.norm(e - c, axis=1).max()))
    return out
z0 = sf * H; L = [t for t in loops([0, 0, z0], [0, 0, 1]) if t[0] < PMAX and t[1][1] > smy]
assert L, 'no seed loop'; per0, c0, r0 = max(L, key=lambda t: t[1][1])
def track(c, dirv, per_ref):
    pts = []; misses = 0
    for _ in range(400):
        nxt = c + dirv * STEP; L = [t for t in loops(nxt, dirv) if np.linalg.norm(t[1] - nxt) < 2.5 * STEP + 1.0]
        if not L: break
        per, cc, rr = min(L, key=lambda t: np.linalg.norm(t[1] - nxt))
        if per > 1.6 * per_ref: break                      # merged into the body
        nd = cc - c; nd /= np.linalg.norm(nd); dirv = 0.6 * dirv + 0.4 * nd; dirv /= np.linalg.norm(dirv); c = cc
        pts.append((c.copy(), rr)); per_ref = 0.8 * per_ref + 0.2 * per
    return pts, c
up, cu = track(c0, np.array([0, 0, 1.0]), per0); dn, cd = track(c0, np.array([0, 0, -1.0]), per0)
cl = [p for p, _ in dn[::-1]] + [c0] + [p for p, _ in up]; rad = [r for _, r in dn[::-1]] + [r0] + [r for _, r in up]
cl = np.array(cl); rad = np.array(rad); cen = V[F].mean(1)
# densify the centreline and delete faces inside the swept tube
seg = []; srad = []
for a, b, ra, rb in zip(cl[:-1], cl[1:], rad[:-1], rad[1:]):
    for t in np.linspace(0, 1, 6, endpoint=False): seg.append(a + t * (b - a)); srad.append(ra + t * (rb - ra))
seg.append(cl[-1]); srad.append(rad[-1]); seg = np.array(seg); srad = np.array(srad)
dd, ii = cKDTree(seg).query(cen); tail = dd < 1.35 * srad[ii]
zs = np.arange(0.80 * H, 0.89 * H, 0.5)
NECK = float(zs[np.argmin([max(l for l, _, _ in loops([0, 0, z], [0, 0, 1])) for z in zs])])
keep = ~(tail | (cen[:, 2] > NECK)); Fk = F[keep]; n = len(V); E = np.concatenate([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]])
nc, lab = connected_components(sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)), directed=False)
fl = lab[Fk[:, 0]]; sizes = np.bincount(fl); big = np.argmax(sizes); pieces = sorted([int(s) for s in sizes if s], reverse=True)
Fk = Fk[fl == big]; u = np.unique(Fk); mp = -np.ones(n, np.int64); mp[u] = np.arange(len(u))
np.savez(fo, V=P[u].astype(np.float32), F=mp[Fk].astype(np.int32))
print(json.dumps(dict(diagnostic_only=True, neck_cut_z_cm=round(NECK, 1), seed=np.round(c0, 1).tolist(), tracked_points=len(cl),
                      tail_end_a=np.round(cl[0], 1).tolist(), tail_end_b_merge_with_body=np.round(cl[-1], 1).tolist(),
                      tail_faces_hidden=int(tail.sum()), pieces_after_cut_faces=pieces[:6], faces_in=int(len(F)), faces_out=int(len(Fk)))))
