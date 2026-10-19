"""Per-digit centreline + cross-section frames from the segmented source hand (segH_S.npz).
For each digit region: geodesic distance from its base boundary (vertices adjacent to palm), iso-bands -> ring centroids
(centreline), ring points -> half extents along the width/dorsal axes of a parallel-transported frame.
Output digits_S.json: per digit {role, pts:[...], t, ew, et, a, b, s(arc length)} in Blender cm."""
import numpy as np, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
s = sys.argv[1]; roles = json.loads(sys.argv[2]); dors = np.array(json.loads(sys.argv[3]), float)   # palm dorsal direction
z = np.load('/home/claude/stc/rp1e/segH_%s.npz' % s); used = z['used']; lab = z['lab']
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
mp = -np.ones(len(V), np.int64); mp[used] = np.arange(len(used)); X = V[used]
Fh = F[(mp[F] >= 0).all(1)]; Fl = mp[Fh]
E = np.unique(np.sort(np.concatenate([Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]]), 1), axis=0)
out = {}
for k, role in roles.items():
    k = int(k); m = lab == k
    e = E[m[E[:, 0]] & m[E[:, 1]]]
    pm = lab == 9
    base = np.unique(np.concatenate([E[m[E[:, 0]] & pm[E[:, 1]], 0], E[m[E[:, 1]] & pm[E[:, 0]], 1]]))
    wt = np.linalg.norm(X[e[:, 0]] - X[e[:, 1]], axis=1)
    G = coo_matrix((wt, (e[:, 0], e[:, 1])), shape=(len(X), len(X))).tocsr()
    D = dijkstra(G, directed=False, indices=base, min_only=True)
    idx = np.where(m & np.isfinite(D))[0]; Dm = D[idx]; L = Dm.max()
    step = 0.6; rings = []
    for b0 in np.arange(0, L, step):
        q = idx[(Dm >= b0) & (Dm < b0 + step)]
        if len(q) < 12: continue
        rings.append((b0 + step / 2, X[q]))
    C = np.array([r[1].mean(0) for r in rings])
    # smooth centreline
    Cs = C.copy()
    for _ in range(3): Cs[1:-1] = 0.25 * Cs[:-2] + 0.5 * Cs[1:-1] + 0.25 * Cs[2:]
    T = np.gradient(Cs, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    et = dors - (dors @ T[0]) * T[0]; et /= np.linalg.norm(et)
    ETs, EWs, A, B = [], [], [], []
    for i, (dd, P) in enumerate(rings):
        if i: et = et - (et @ T[i]) * T[i]; et /= np.linalg.norm(et)
        ew = np.cross(T[i], et); ew /= np.linalg.norm(ew)
        Q = P - Cs[i]
        A.append(float(np.percentile(np.abs(Q @ ew), 90))); B.append(float(np.percentile(np.abs(Q @ et), 90)))
        ETs.append(et.copy()); EWs.append(ew)
    tip = X[idx[Dm.argmax()]]
    sarc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Cs, axis=0), axis=1))]
    out[role] = dict(label=k, n=len(rings), c=Cs.round(3).tolist(), t=T.round(4).tolist(), et=np.array(ETs).round(4).tolist(),
                     ew=np.array(EWs).round(4).tolist(), a=np.round(A, 3).tolist(), b=np.round(B, 3).tolist(), s=sarc.round(3).tolist(),
                     tip=tip.round(3).tolist(), geo_len=round(float(L), 2))
    print(role, 'rings', len(rings), 'len %.1f' % L, 'a', np.round(A, 1).tolist(), 'b', np.round(B, 1).tolist())
json.dump(out, open('/home/claude/stc/rp1e/digits_%s.json' % s, 'w'), indent=0)
