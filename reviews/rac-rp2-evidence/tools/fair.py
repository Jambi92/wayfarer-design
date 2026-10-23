# fair.py IN.npz OUT.npz [d2_mm] [d1_mm] : interpolating fairing of the production candidate.
# Base (MPFB / patch) vertices, contact-zone, patch and low-clearance vertices stay fixed; every other sub-vertex is placed by
# biharmonic interpolation (removes the inherited facet creases of the 13.4k base), then the deviation from the target S* is clamped
# to +-d (T-2 zones d2, elsewhere d1). Symmetric.
import sys, numpy as np, igl, scipy.sparse as sp, json
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from hidden import hidden_quads
R = '/tmp/claude-0/rp2/'
z = dict(np.load(sys.argv[1])); P = z['V'].copy(); Q = z['Q']; n = len(P); mir = z['mir']
D2 = float(sys.argv[3]) / 10 if len(sys.argv) > 3 else 0.12; D1 = float(sys.argv[4]) / 10 if len(sys.argv) > 4 else 0.25
S = sp.load_npz(sys.argv[1].replace('.npz', '_S.npz').replace('cand', 'cand')).tocsr() if False else None
b = np.load(R + 'sstar_ppu.npz'); nb = len(b['V'])
s0 = np.load(R + 'sstar.npz'); S0 = s0['V']; Q0 = s0['Q']; T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]
clr = np.load(R + 'clr.npy'); cz = z['cz']; T2 = z['zone_T2']
fixed = np.zeros(n, bool); fixed[:nb] = True; fixed |= cz; fixed |= clr < 0.4
ev = np.load(R + 'vis_sstar.npz')['tri']; from scipy.spatial import cKDTree
fixed |= cKDTree(S0[T0[~ev]].mean(1)).query(P)[0] < 1.5
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
bidx = np.where(fixed)[0]
Pn = igl.harmonic(P, T, bidx, P[bidx], 2)
# clamp to the envelope band
hq, sgn, ht = hidden_quads(S0, Q0)
nn = np.cross(S0[T0[:, 1]] - S0[T0[:, 0]], S0[T0[:, 2]] - S0[T0[:, 0]]); TN = sgn * nn / np.linalg.norm(nn, axis=1)[:, None]
free = np.where(~fixed)[0]; d, fi, cp = igl.point_mesh_squared_distance(Pn[free], S0, T0)
sd = ((Pn[free] - cp) * TN[fi]).sum(1); dl = np.where(T2[free], D2, D1)
Pn[free] = Pn[free] - TN[fi] * (sd - np.clip(sd, -dl, dl))[:, None]
m = mir >= 0; Pn[m] = 0.5 * (Pn[m] + Pn[mir[m]] * np.array([-1, 1, 1])); s_ = m & (mir == np.arange(n)); Pn[s_, 0] = 0
z['V'] = Pn; np.savez(sys.argv[2], **z)
print(json.dumps(dict(fixed=int(fixed.sum()), free=int(len(free)), moved_mm_p95=float(np.percentile(np.linalg.norm(Pn - P, axis=1), 95) * 10), clamped=int((np.abs(sd) > dl).sum()))))
