"""Digit segmentation of a source hand surface.
1) distal digit labels from the surface Reeb tree (vlab_S.npy);
2) bottom-up horizontal slab tracking: a slab component that inherits exactly one digit (from its own labelled vertices or from
   the overlapping component of the slab below) takes that digit; components inheriting several digits are merge zones (webs /
   palm / contact) and are split by geodesic Voronoi from the labelled vertices only if they lie below the palm line;
3) everything else = palm (label 9).
Output: segH_S.npz (used vertex ids, label per used vertex; digits named by role)."""
import numpy as np, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
s = sys.argv[1]; zpalm = float(sys.argv[2]); step = 0.3
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
L = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))['wrist_' + s]
pp = np.array(L['plane_point']) * [1, -1, 1]; nn = np.array(L['plane_normal']) * [1, -1, 1]
hand = (w['w_hand_' + s] > 0.5) | ((w['w_forearm_' + s] > 0.5) & (((V - pp) @ nn) > -1.5))
Fh = F[hand[F].all(1)]; used = np.unique(Fh); mp = -np.ones(len(V), np.int64); mp[used] = np.arange(len(used))
X = V[used]; Fl = mp[Fh]; n = len(X)
E = np.unique(np.sort(np.concatenate([Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]]), 1), axis=0)
vl = np.load('/home/claude/stc/rp1e/vlab_%s.npy' % s); lab = -np.ones(n, int)
li = mp[vl[:, 0]]; lab[li[li >= 0]] = vl[li >= 0, 1]
z = X[:, 2]; zs = np.arange(z.min(), zpalm + 2.0, step)
prev = None
for z0 in zs:
    m = (z >= z0 - step) & (z < z0 + step); idx = np.where(m)[0]
    if not len(idx): prev = None; continue
    e = E[m[E[:, 0]] & m[E[:, 1]]]; loc = -np.ones(n, int); loc[idx] = np.arange(len(idx))
    nc, cl = connected_components(coo_matrix((np.ones(len(e)), (loc[e[:, 0]], loc[e[:, 1]])), shape=(len(idx), len(idx))), directed=False)
    for c in range(nc):
        vv = idx[cl == c]; ls = set(lab[vv][lab[vv] >= 0].tolist())
        ext = np.ptp(X[vv, :2], axis=0).max()
        if len(ls) == 1 and z0 < zpalm and ext < float(sys.argv[4]):
            k = ls.pop(); lab[vv[lab[vv] < 0]] = k
# merge zones below the palm line: geodesic voronoi from labelled vertices
un = (lab < 0) & (z < zpalm - float(sys.argv[3]))
wt = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1)
G = coo_matrix((wt, (E[:, 0], E[:, 1])), shape=(n, n)).tocsr()
srcs = np.where(lab >= 0)[0]
D, _, src_of = dijkstra(G, directed=False, indices=srcs, min_only=True, return_predecessors=True)
lab[un] = lab[src_of[un]]
lab[lab < 0] = 9
np.savez_compressed('/home/claude/stc/rp1e/segH_%s.npz' % s, used=used, lab=lab)
print({int(k): int((lab == k).sum()) for k in np.unique(lab)})
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cm = {0: 'r', 1: 'g', 2: 'b', 3: 'm', 4: 'c', 9: '0.75'}
col = np.array([cm[q] for q in lab])
fig, ax = plt.subplots(2, 3, figsize=(27, 20))
for a, (i_, j, k, sg) in zip(ax.ravel(), [(0, 2, 1, -1), (0, 2, 1, 1), (1, 2, 0, 1), (1, 2, 0, -1), (0, 1, 2, 1), (0, 1, 2, -1)]):
    o = np.argsort(sg * X[:, k]); a.scatter(X[o, i_], X[o, j], c=col[o], s=2); a.set_aspect('equal')
plt.savefig('/home/claude/stc/rp1e/segH_%s.png' % s, dpi=45, bbox_inches='tight')
