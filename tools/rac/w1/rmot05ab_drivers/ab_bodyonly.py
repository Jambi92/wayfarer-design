# RM-OT-05AB: DISPOSABLE body-only diagnostic copies for meshes that share the donor's topology (donor C and its rig derivatives).
# The tail / head face mask is computed ONCE on the donor with the x_tailtrack.py tube-tracking method (logic copied here; the 05X
# tool is unchanged) and the identical face set is then removed from every derivative, so before/after body-only views hide exactly
# the same anatomy. Vertices are exact-position welded (UV seams) before connectivity. Faces deleted only; nothing is repaired.
# Usage: python3 ab_bodyonly.py DONOR_GLTF.npz SEED_Z_FRAC SEED_MIN_Y_CM NECK_Z_CM OUT_MASK.json  IN1.npz:OUT1.npz [IN2.npz:OUT2.npz ...]
#   npz: V in glTF metres (Y up, front +Z), F triangles. NECK_Z_CM: donor neck-minimum height (168.3 for C).
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
dn, sf, smy, neck, mout = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]; pairs = [p.split(':') for p in sys.argv[6:]]
STEP, PMAX = 1.0, 40.0
d = np.load(dn); P = d['V'].astype(np.float64); F0 = d['F'].astype(np.int64)
key, inv = np.unique(np.round(P, 6), axis=0, return_inverse=True); inv = inv.ravel(); F = inv[F0]
V = np.stack([key[:, 0], -key[:, 2], key[:, 1]], 1) * 100; H = V[:, 2].max(); m = trimesh.Trimesh(V, F, process=False)
def loops(o, nrm):
    s = m.section(plane_origin=o, plane_normal=nrm)
    return [] if s is None else [(np.linalg.norm(np.diff(e, axis=0), axis=1).sum(), e.mean(0), np.linalg.norm(e - e.mean(0), axis=1).max()) for e in s.discrete]
L = [t for t in loops([0, 0, sf * H], [0, 0, 1]) if t[0] < PMAX and t[1][1] > smy]; assert L, 'no seed loop'; per0, c0, r0 = max(L, key=lambda t: t[1][1])
def track(c, dirv, per_ref):
    pts = []
    for _ in range(400):
        nxt = c + dirv * STEP; L = [t for t in loops(nxt, dirv) if np.linalg.norm(t[1] - nxt) < 2.5 * STEP + 1.0]
        if not L: break
        per, cc, rr = min(L, key=lambda t: np.linalg.norm(t[1] - nxt))
        if per > 1.6 * per_ref: break
        nd = cc - c; nd /= np.linalg.norm(nd); dirv = 0.6 * dirv + 0.4 * nd; dirv /= np.linalg.norm(dirv); c = cc; pts.append((c.copy(), rr)); per_ref = 0.8 * per_ref + 0.2 * per
    return pts
up = track(c0, np.array([0, 0, 1.0]), per0); dnn = track(c0, np.array([0, 0, -1.0]), per0)
cl = np.array([p for p, _ in dnn[::-1]] + [c0] + [p for p, _ in up]); rad = np.array([r for _, r in dnn[::-1]] + [r0] + [r for _, r in up])
seg, srad = [], []
for a, b, ra, rb in zip(cl[:-1], cl[1:], rad[:-1], rad[1:]):
    for t in np.linspace(0, 1, 6, endpoint=False): seg.append(a + t * (b - a)); srad.append(ra + t * (rb - ra))
seg.append(cl[-1]); srad.append(rad[-1]); seg = np.array(seg); srad = np.array(srad)
cen = V[F].mean(1); dd, ii = cKDTree(seg).query(cen); tail = dd < 1.35 * srad[ii]
keep = ~(tail | (cen[:, 2] > neck)); Fk = F[keep]; n = len(V)
E = np.concatenate([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]])
nc, lab = connected_components(sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)), directed=False)
fl = lab[Fk[:, 0]]; sizes = np.bincount(fl); big = np.argmax(sizes); kf = np.where(keep)[0][fl == big]
json.dump(dict(diagnostic_only=True, neck_cut_z_cm_donor=neck, tail_faces_hidden=int(tail.sum()), faces_kept=int(len(kf)),
               pieces_after_cut=sorted([int(s) for s in sizes if s], reverse=True)[:6], tail_merge_with_body=np.round(cl[-1], 1).tolist()), open(mout, 'w'), indent=1)
for i, o in pairs:
    q = np.load(i); assert np.array_equal(q['F'], d['F']), 'topology differs from donor'
    Q = q['V'].astype(np.float64); Ff = F0[kf]; u = np.unique(Ff); mp = -np.ones(len(Q), np.int64); mp[u] = np.arange(len(u))
    np.savez(o, V=Q[u].astype(np.float32), F=mp[Ff].astype(np.int32))
print(open(mout).read())
