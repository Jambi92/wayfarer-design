# fair2.py IN.npz OUT.npz lam d2_mm d1_mm : screened (implicit) fairing (I + lam L^T L) P = P0 of every vertex outside the
# fixed set (contact zones, patches, low clearance, interior surfaces), then the deviation from the target S* is clamped to the
# zone band (T-2 zones d2, elsewhere d1); symmetric.
import sys, numpy as np, igl, scipy.sparse as sp, json
from scipy.sparse.linalg import spsolve
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from hidden import hidden_quads
from scipy.spatial import cKDTree
R = '/tmp/claude-0/rp2/'
z = dict(np.load(sys.argv[1])); P0 = z['V'].copy(); Q = z['Q']; n = len(P0); mir = z['mir']
lam = float(sys.argv[3]); D2 = float(sys.argv[4]) / 10; D1 = float(sys.argv[5]) / 10
s0 = np.load(R + 'sstar.npz'); S0 = s0['V']; Q0 = s0['Q']; T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]
clr = np.load(R + 'clr.npy'); cz = z['cz']; T2 = z['zone_T2']
fixed = cz | (clr < 0.4)
ev = np.load(R + 'vis_sstar.npz')['tri']; fixed |= cKDTree(S0[T0[~ev]].mean(1)).query(P0)[0] < 1.5
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
L = sp.diags(1 / deg) @ A - sp.identity(n)
M = (sp.identity(n) + lam * (L.T @ L)).tocsr()
# Dirichlet rows for fixed vertices
fx = np.where(fixed)[0]; Mf = M.tolil(); 
D = sp.diags(fixed.astype(float)); M2 = (sp.diags((~fixed).astype(float)) @ M + D).tocsr()
B = P0.copy()
Pn = np.stack([spsolve(M2, B[:, k]) for k in range(3)], 1)
hq, sgn, ht = hidden_quads(S0, Q0)
nn = np.cross(S0[T0[:, 1]] - S0[T0[:, 0]], S0[T0[:, 2]] - S0[T0[:, 0]]); TN = sgn * nn / np.linalg.norm(nn, axis=1)[:, None]
free = np.where(~fixed)[0]; d, fi, cp = igl.point_mesh_squared_distance(Pn[free], S0, T0)
sd = ((Pn[free] - cp) * TN[fi]).sum(1); dl = np.where(T2[free], D2, D1)
Pn[free] = Pn[free] - TN[fi] * (sd - np.clip(sd, -dl, dl))[:, None]
m = mir >= 0; Pn[m] = 0.5 * (Pn[m] + Pn[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); Pn[s_, 0] = 0
z['V'] = Pn; np.savez(sys.argv[2], **z)
print(json.dumps(dict(fixed=int(fixed.sum()), moved_mm_p95=float(np.percentile(np.linalg.norm(Pn - P0, axis=1), 95) * 10), clamped=int((np.abs(sd) > dl).sum()))))
