"""surface Reeb segmentation of a source hand: geodesic (edge-graph) distance from the wrist section over the hand submesh,
iso-bands -> connected components (vertex graph restricted to band) -> tree. Contact between digits does not connect surfaces,
so bands split cleanly into digits (except at welded handles)."""
import numpy as np, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
s = sys.argv[1]; step = float(sys.argv[2])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
L = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))['wrist_' + s]
pp = np.array(L['plane_point']) * [1, -1, 1]; nn = np.array(L['plane_normal']) * [1, -1, 1]
dpl = (V - pp) @ nn
hand = (w['w_hand_' + s] > 0.5) | ((w['w_forearm_' + s] > 0.5) & (dpl > -1.5))
Fh = F[hand[F].all(1)]; used = np.unique(Fh); mp = -np.ones(len(V), np.int64); mp[used] = np.arange(len(used))
Vh = V[used]; Fl = mp[Fh]; dh = dpl[used]
E = np.unique(np.sort(np.concatenate([Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]]), 1), axis=0)
wt = np.linalg.norm(Vh[E[:, 0]] - Vh[E[:, 1]], axis=1)
G = coo_matrix((wt, (E[:, 0], E[:, 1])), shape=(len(Vh), len(Vh))).tocsr()
src = np.where(dh < dh.min() + 0.5)[0]
D = dijkstra(G, directed=False, indices=src, min_only=True)
nc, cl = connected_components(G, directed=False); print('hand submesh', len(Vh), 'components', nc, 'finite', np.isfinite(D).mean())
b = np.floor(D / step).astype(int); nb = b[np.isfinite(D)].max() + 1
# band components
comp = -np.ones(len(Vh), np.int64); info = []
for k in range(nb):
    m = b == k; idx = np.where(m)[0]
    if not len(idx): continue
    e = E[m[E[:, 0]] & m[E[:, 1]]]; li = -np.ones(len(Vh), np.int64); li[idx] = np.arange(len(idx))
    g2 = coo_matrix((np.ones(len(e)), (li[e[:, 0]], li[e[:, 1]])), shape=(len(idx), len(idx)))
    n2, l2 = connected_components(g2, directed=False)
    for c in range(n2):
        sel = idx[l2 == c]
        comp[sel] = len(info); info.append(dict(band=k, n=len(sel)))
# parent links between consecutive bands
eb = E[(comp[E[:, 0]] >= 0) & (comp[E[:, 1]] >= 0)]
ca, cb = comp[eb[:, 0]], comp[eb[:, 1]]; ba = np.array([info[c]['band'] for c in ca]); bb = np.array([info[c]['band'] for c in cb])
par = {}; child = {}
for x, y, bx, by in zip(ca, cb, ba, bb):
    if by == bx - 1: par.setdefault(x, set()).add(y)
    if bx == by - 1: par.setdefault(y, set()).add(x)
for c, ps in par.items():
    for p in ps: child.setdefault(p, set()).add(c)
np.savez_compressed('/home/claude/stc/rp1e/sreeb_%s.npz' % s, used=used, D=D, comp=comp, bands=np.array([i['band'] for i in info]), sizes=np.array([i['n'] for i in info]))
# report: number of significant comps per band
for k in range(0, nb, 2):
    cs = [i for i, x in enumerate(info) if x['band'] == k and x['n'] > 30]
    print('%5.1f' % (k * step), len(cs), sorted([info[c]['n'] for c in cs], reverse=True)[:8])
json.dump({'par': {int(k): sorted(int(x) for x in v) for k, v in par.items()}}, open('/home/claude/stc/rp1e/sreeb_%s_par.json' % s, 'w'))
