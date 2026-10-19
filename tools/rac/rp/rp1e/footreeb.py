"""Toe segmentation of a source foot: geodesic distance (surface edge graph) from the ankle section over the foot submesh,
then per-band connected components; seeds at a band showing 5 toe components grown distally and proximally (until merge).
Usage: python3 footreeb.py S step [seedband]"""
import numpy as np, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
s = sys.argv[1]; step = float(sys.argv[2])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
L = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))['ankle_' + s]
pp = np.array(L['plane_point']) * [1, -1, 1]; nn = np.array(L['plane_normal']) * [1, -1, 1]
dpl = (V - pp) @ nn          # >0 below ankle plane (normal points down)
foot = (w['w_foot_' + s] > 0.5) | ((w['w_shin_' + s] > 0.5) & (dpl > -1.5))
Fh = F[foot[F].all(1)]; used = np.unique(Fh); mp = -np.ones(len(V), np.int64); mp[used] = np.arange(len(used))
X = V[used]; Fl = mp[Fh]; dh = dpl[used]; n = len(X)
E = np.unique(np.sort(np.concatenate([Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]]), 1), axis=0)
wt = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=1)
G = coo_matrix((wt, (E[:, 0], E[:, 1])), shape=(n, n)).tocsr()
src = np.where(dh < dh.min() + 0.5)[0]
D = dijkstra(G, directed=False, indices=src, min_only=True)
b = np.floor(D / step).astype(int); nb = b.max() + 1
comp = -np.ones(n, np.int64); info = []
for k in range(nb):
    m = b == k; idx = np.where(m)[0]
    if not len(idx): continue
    e = E[m[E[:, 0]] & m[E[:, 1]]]; li = -np.ones(n, np.int64); li[idx] = np.arange(len(idx))
    n2, l2 = connected_components(coo_matrix((np.ones(len(e)), (li[e[:, 0]], li[e[:, 1]])), shape=(len(idx), len(idx))), directed=False)
    for c in range(n2):
        sel = idx[l2 == c]; comp[sel] = len(info); info.append(dict(band=k, n=len(sel)))
bands = np.array([i['band'] for i in info]); sizes = np.array([i['n'] for i in info])
for k in range(0, nb):
    cs = np.where((bands == k) & (sizes > 30))[0]
    if len(cs) > 1: print('%5.1f' % (k * step), len(cs), sorted(sizes[cs].tolist(), reverse=True)[:7])
np.savez_compressed('freeb_%s.npz' % s, used=used, D=D, comp=comp, bands=bands, sizes=sizes, E=E)
