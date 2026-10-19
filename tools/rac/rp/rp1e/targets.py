"""Build colour-ownership projection targets from per-vertex source colours.
target(c) = faces whose vertices are all in ext(c); ext(c) = core(c) + margin: vertices v not in c with geodesic distance
d_geo(v, core c) < M (surface edge graph) and Euclidean distance d_euc(v, core c) > ratio * d_geo (excludes vertices that are
close in space but far along the surface = across a contact gap).
Usage: python3 targets.py COLOURS.npy OUTPREFIX M ratio"""
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
col = np.load(sys.argv[1]); nom = np.load(sys.argv[5]) if len(sys.argv) > 5 else None; pre = sys.argv[2]; M = float(sys.argv[3]); ratio = float(sys.argv[4])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
E = np.unique(np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1), axis=0)
wt = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
G = coo_matrix((wt, (E[:, 0], E[:, 1])), shape=(len(V), len(V))).tocsr()
for c in np.unique(col):
    core = np.where(col == c)[0]
    # boundary of the core (core vertices with a non-core neighbour) as Dijkstra sources, limited radius
    nb = np.zeros(len(V), bool); a, b = E[:, 0], E[:, 1]
    bd = np.unique(np.concatenate([a[(col[a] == c) & (col[b] != c)], b[(col[b] == c) & (col[a] != c)]]))
    if len(bd):
        D = dijkstra(G, directed=False, indices=bd, min_only=True, limit=M)
        cand = np.where(np.isfinite(D) & (col != c))[0]
        de, _ = cKDTree(V[core]).query(V[cand])
        ok = de > ratio * D[cand]
        if nom is not None: ok &= ~nom[cand]
        ext = np.zeros(len(V), bool); ext[core] = True; ext[cand[ok]] = True
    else:
        ext = col == c
    Fc = F[ext[F].all(1)]
    used = np.unique(Fc); mp = -np.ones(len(V), int); mp[used] = np.arange(len(used))
    np.savez_compressed('%s_c%d.npz' % (pre, c), V=V[used], F=mp[Fc])
    print('colour', c, 'core', len(core), 'margin added', int(ext.sum() - len(core)), 'faces', len(Fc))
