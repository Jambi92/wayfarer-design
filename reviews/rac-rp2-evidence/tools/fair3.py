# fair3.py IN.npz OUT.npz lam d2_mm d1_mm [iters] : screened fairing with an adaptive data term (IRLS): minimise
#   sum_i w_i |p_i - p0_i|^2 + lam |L p|^2 ; vertices whose distance to the target S* exceeds 70 % of their zone band get a
#   larger w_i next round, so the faired surface stays smooth AND inside the band (no hard clamp creases). Fixed set as fair2.
import sys, numpy as np, igl, scipy.sparse as sp, json
from scipy.sparse.linalg import factorized
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from scipy.spatial import cKDTree
R = '/tmp/claude-0/rp2/'
z = dict(np.load(sys.argv[1])); P0 = z['V'].copy(); Q = z['Q']; n = len(P0); mir = z['mir']
lam = float(sys.argv[3]); D2 = float(sys.argv[4]) / 10; D1 = float(sys.argv[5]) / 10; IT = int(sys.argv[6]) if len(sys.argv) > 6 else 6
s0 = np.load(R + 'sstar.npz'); S0 = s0['V']; Q0 = s0['Q']; T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]
clr = np.load(R + 'clr.npy'); cz = z['cz']; T2 = z['zone_T2']
import os
if os.environ.get('FIXCZ', '1') == '1': fixed = cz | (clr < 0.4)
else:
    Sx = sp.load_npz(sys.argv[1].replace('.npz', '_S.npz')).tocsr(); bb = np.load(R + 'sstar_ppu.npz')['V']
    newB = (cKDTree(S0).query(bb)[0] > 1e-6) & ~((np.abs(bb[:, 0]) < 8) & (bb[:, 2] > 100) & (bb[:, 2] < 122)); pdx = np.asarray(Sx[:, newB].sum(1)).ravel() > 0
    fixed = pdx | (clr < 0.4)
ev = np.load(R + 'vis_sstar.npz')['tri']; fixed |= cKDTree(S0[T0[~ev]].mean(1)).query(P0)[0] < 1.5
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
L = (sp.diags(1 / deg) @ A - sp.identity(n)).tocsr(); LL = (L.T @ L).tocsr()
band = np.where(T2, D2, D1)
import os
if 'zone_girdle_shoulder' in z: band = np.where(z['zone_girdle_shoulder'], float(os.environ.get('GIRDLE_MM', '1.0')) / 10, band)
w = np.ones(n); w[fixed] = 1e8
for it in range(IT):
    M = (sp.diags(w) + lam * LL).tocsc(); solve = factorized(M)
    Pn = np.stack([solve(w * P0[:, k]) for k in range(3)], 1)
    m = mir >= 0; Pn[m] = 0.5 * (Pn[m] + Pn[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); Pn[s_, 0] = 0
    d = np.sqrt(igl.point_mesh_squared_distance(Pn, S0, T0)[0])
    r = d / band; over = r > 0.7
    w[over & ~fixed] *= (1 + (r[over & ~fixed] / 0.7) ** 4)
    print('iter', it, 'max r %.2f' % r[~fixed].max(), 'over', int(over.sum()), 'dev p95 mm %.3f' % (np.percentile(d, 95) * 10), flush=True)
z['V'] = Pn; np.savez(sys.argv[2], **z)
