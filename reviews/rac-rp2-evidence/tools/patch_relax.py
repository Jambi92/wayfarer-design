# patch_relax.py IN.npz OUT.npz [iters] : relax the resolution-zone patches (patch descendants + contact ring) so they are clean
# and smooth: Taubin smoothing restricted to the zone (zone border fixed), seam vertices kept on the crease polyline, symmetric.
import sys, numpy as np, scipy.sparse as sp, igl
sys.path.insert(0, '/tmp/claude-0/rp2/tools')
R = '/tmp/claude-0/rp2/'
z = dict(np.load(sys.argv[1])); P = z['V'].copy(); Q = z['Q']; n = len(P); mir = z['mir']; IT = int(sys.argv[3]) if len(sys.argv) > 3 else 40
S = sp.load_npz(sys.argv[1].replace('.npz', '_S.npz')).tocsr()
b = np.load(R + 'sstar_ppu.npz'); VB = b['V']; nb = len(VB)
S0 = np.load(R + 'sstar.npz')['V']
from scipy.spatial import cKDTree
newB = (cKDTree(S0).query(VB)[0] > 1e-6) & ~((np.abs(VB[:, 0]) < 8) & (VB[:, 2] > 100) & (VB[:, 2] < 122))
pd = np.asarray(S[:, newB].sum(1)).ravel() > 0
zone = pd.copy()
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
RINGS = int(__import__('os').environ.get('RINGS', '4'))
for _ in range(RINGS): zone = zone | ((A @ zone.astype(float)) > 0)
free = zone.copy()
for _ in range(1): free = free & ~((A @ (~zone).astype(float)) > 0)            # one-ring border of the zone stays fixed
# seam vertices
seam = {}
for key in ('crotch', 'axL', 'axR'):
    sb = np.zeros(nb, bool); sb[b['seam_' + key]] = True; seam[key] = np.where((np.asarray(S[:, sb].sum(1)).ravel() > 0.999) & free)[0]
crs = {'crotch': np.asarray(b['crease_crotch'], float)}
cA = np.load(R + 'crease_axL_dense.npy'); cA = cA[np.argsort(cA[:, 1])]
for _ in range(4): cA[1:-1] = 0.5 * cA[1:-1] + 0.25 * (cA[:-2] + cA[2:])
crs['axL'] = cA; crs['axR'] = cA * np.array([-1, 1, 1])
for k in list(crs):
    sv = b['seam_' + k]
    if len(sv) == 0: crs.pop(k); continue
    a0, a1 = VB[sv[0]], VB[sv[-1]]; c = crs[k]
    if np.linalg.norm(c[0] - a0) > np.linalg.norm(c[-1] - a0): c = c[::-1]
    crs[k] = np.vstack([a0, c, a1])
def onpoly(X, c):
    A_ = c[:-1]; B_ = c[1:]; AB = B_ - A_; L2 = (AB ** 2).sum(1) + 1e-12
    Y = X[:, None, :] - A_[None]; t = np.clip((Y * AB[None]).sum(2) / L2[None], 0, 1); Cp = A_[None] + t[:, :, None] * AB[None]
    k = ((X[:, None, :] - Cp) ** 2).sum(2).argmin(1); return Cp[np.arange(len(X)), k]
fr = np.where(free)[0]; pdf = np.where(free & pd)[0]
for it in range(IT):
    for f in (0.5, -0.53):
        L = (A @ P) / deg[:, None] - P; P[fr] += f * L[fr]
    if it < int(__import__('os').environ.get('SHRINK', '12')):
        L = (A @ P) / deg[:, None] - P; P[pdf] += 0.3 * L[pdf]                   # a few shrinking steps on the patch itself: removes knobs
    for k, idx in seam.items():
        if k not in crs: continue
        if len(idx) and __import__('os').environ.get('SEAMFREE', '0') != '1': P[idx] = onpoly(P[idx], crs[k])
        if k == 'crotch': P[idx, 0] = 0
    m = mir >= 0; P[m] = 0.5 * (P[m] + P[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); P[s_, 0] = 0
z['V'] = P; np.savez(sys.argv[2], **z); print('zone verts', int(zone.sum()), 'free', int(free.sum()))
