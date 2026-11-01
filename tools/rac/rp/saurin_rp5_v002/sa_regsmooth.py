# sa_regsmooth.py IN.npz OUT.npz : regional shape-improving relaxation (quad-centroid rule, tangential, reprojected onto the working source; order 236dddc
#   §9 "quad-centroid shape improvement / ring redistribution") on the named regions only (+ 2 vertex rings of feathering); tips / pins / tail fixed.
#   Followed by sa_qopt (coverage + quality) to restore the gates.
import sys, os, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; LABS = os.environ.get('LABS', 'palm,finger_web,finger,thumb,toe_web,forefoot,toe,orbit').split(','); IT = int(os.environ.get('IT', 40)); W = float(os.environ.get('W', 0.5))
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nb = int(z['n_body']); ql = z['qlab'].astype(str)
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
m = np.zeros(nv, bool); m[Q[np.isin(ql, LABS)].ravel()] = True
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
w = m.astype(float)
for _ in range(2): w = np.maximum(w, 0.5 * ((A @ w) > 0) * w.max() * 0 + 0.5 * (((A @ (w > 0).astype(float)) > 0) & (w == 0)))
w[pin] = 0; T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; tr = igl.AABB(); tr.init(G.V, G.F); cq = np.bincount(Q.ravel(), minlength=nv)
for it in range(IT):
    qc = V[Q].mean(1); acc = np.zeros_like(V); np.add.at(acc, Q.ravel(), np.repeat(qc, 4, 0)); L = acc / np.maximum(cq, 1)[:, None] - V
    N = np.nan_to_num(igl.per_vertex_normals(V, T)); L -= (L * N).sum(1)[:, None] * N
    Vt = V + W * w[:, None] * L; idx = np.nonzero(w > 0)[0]; _, _, cp = tr.squared_distance(G.V, G.F, Vt[idx])
    ok = np.linalg.norm(cp - V[idx], axis=1) < 0.3; V[idx[ok]] = cp[ok]
sd = np.linalg.norm(np.roll(V[Q], -1, 1) - V[Q], axis=2); asp = sd.max(1) / sd.min(1); TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
print('aspect>4 non-tip', int(((asp > 4) & ~TIP).sum()), 'in regions', int(((asp > 4) & np.isin(ql, LABS)).sum()))
fi, bc, _ = G.embed(V); z['V'] = V; z['tri'] = fi; z['bc'] = bc; np.savez_compressed(OUT, **z)
