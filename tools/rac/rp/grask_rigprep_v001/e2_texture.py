# e2_texture.py OUT.json SIDE SUPPORT_CORR.npz W0.npz NAME=POSED.npz ... : contact-interface texture metrics at 130 degrees (order 28dd8d3 §10).
# Band = the declared E2 interface support (fair_support_{side} of SUPPORT_CORR, beta > 0). Per candidate:
#   * curvature proxy H_v = (one-ring mean - X_v) . n_v / (mean incident edge length)^2  (1/cm); variation = |H_v - one-ring mean of H|;
#     reported p95 |H| and mean / p95 variation on the band (rumpling = high variation);
#   * displacement field Delta = X - X_W0: edge gradient |Delta_i - Delta_j| / rest length, split ACROSS the interface (edge direction within 45 degrees
#     of the gradient of rest-geodesic distance to the seam) and ALONG it; mean and p95 per class.
import sys, os, json, numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
O, S, SC, W0 = sys.argv[1:5]; items = [a.split('=', 1) for a in sys.argv[5:]]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); nV = len(V0)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); EL = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
A = sp.csr_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV)); deg = np.asarray(A.sum(1)).ravel()
beta = np.load(SC)['fair_support_' + S]; band = beta > 0
G = sp.csr_matrix((np.r_[EL, EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
seam = np.nonzero(beta >= beta.max() - 1e-6)[0]
gd = dijkstra(G, directed=False, indices=seam[:: max(1, len(seam) // 1500)], limit=12, min_only=True); gd = np.where(np.isfinite(gd), gd, 12)
eb = band[E[:, 0]] & band[E[:, 1]]; Eb = E[eb]; ddir = np.abs(gd[Eb[:, 0]] - gd[Eb[:, 1]]) / EL[eb]; across = ddir > np.cos(np.radians(45))
mel = np.asarray((sp.csr_matrix((np.r_[EL, EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))).sum(1)).ravel() / np.maximum(deg, 1)
Xw = np.load(W0)['V'].astype(float); out = json.load(open(O)) if os.path.exists(O) else {}
for nm, pth in items:
    X = np.load(pth)['V'].astype(float)
    fv = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); n = np.zeros((nV, 3))
    for k in range(4): np.add.at(n, Q[:, k], fv)
    n /= np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
    H = (((A @ X) / np.maximum(deg, 1)[:, None] - X) * n).sum(1) / np.maximum(mel, 1e-6) ** 2
    Hv = np.abs(H - (A @ H) / np.maximum(deg, 1))
    D = X - Xw; gr = np.linalg.norm(D[Eb[:, 0]] - D[Eb[:, 1]], axis=1) / EL[eb]
    out['%s_%s' % (nm, S)] = dict(band_vertices=int(band.sum()), curv_p95=round(float(np.percentile(np.abs(H[band]), 95)), 4), curv_var_mean=round(float(Hv[band].mean()), 4),
                                  curv_var_p95=round(float(np.percentile(Hv[band], 95)), 4), grad_across_mean=round(float(gr[across].mean()), 4), grad_across_p95=round(float(np.percentile(gr[across], 95)), 4),
                                  grad_along_mean=round(float(gr[~across].mean()), 4), grad_along_p95=round(float(np.percentile(gr[~across], 95)), 4))
    print(nm, S, out['%s_%s' % (nm, S)])
json.dump(out, open(O, 'w'), indent=1)
