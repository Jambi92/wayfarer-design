# RAC W3B1 section 2 supplement: are the low-m surfaced ridge folds biology or surface transport?  For each ridge strength m the canonical
# per-vertex relief is carried onto the ridge-modified skin along (a) raw normals (W2 convention, as in the sweep) and (b) normals of the
# 20-iteration Laplacian-smoothed base. Folds counted on the head (z > 165), non-sliver faces, excess over the canonical surfaced head.
import os, sys, json, numpy as np, igl
from scipy import sparse
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_ridge as RD
Z = SC.ref(); Vc = Z['Vu']; Fu = Z['Fu']
A = igl.adjacency_matrix(Fu).astype(float); deg = np.asarray(A.sum(1)).ravel(); L = sparse.diags(1 / deg) @ A
def sn(V):
    Vs = V.copy()
    for _ in range(20): Vs = 0.5 * Vs + 0.5 * (L @ Vs)
    return igl.per_vertex_normals(Vs, Fu)
hf = np.where(Vc[Fu[:, 0], 2] > 165)[0]; Fq = Fu[hf]; cr = lambda X: np.cross(X[Fq[:, 1]] - X[Fq[:, 0]], X[Fq[:, 2]] - X[Fq[:, 0]])
ar = 0.5 * np.linalg.norm(cr(Vc), axis=1); ok = ar >= 0.25 * np.median(ar)
fold = lambda S_, V: int((((cr(S_) * cr(V)).sum(1) < 0) & ok).sum())
fc_raw = fold(Vc + Z['disp'][:, None] * Z['N'].astype(float), Vc); fc_s = fold(Vc + Z['disp'][:, None] * sn(Vc), Vc); out = {}
for m in [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4]:
    P = RD.build({k: m for k in RD.FAMS}); Vu, _ = igl.upsample(P, C.F0); Nr = igl.per_vertex_normals(Vu, Fu)
    out[m] = dict(excess_raw=fold(Vu + Z['disp'][:, None] * Nr, Vu) - fc_raw, excess_smoothN=fold(Vu + Z['disp'][:, None] * sn(Vu), Vu) - fc_s)
    print(m, out[m], flush=True)
json.dump(dict(canonical_raw=fc_raw, canonical_smoothN=fc_s, rows=out), open(C.W + '/w3b1_ridge_transport.json', 'w'), indent=1)
