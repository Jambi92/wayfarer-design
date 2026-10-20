"""Per-nail projection gate (rp1_gate.py nail block) with regenerated masks/axes (v014 ruling §8).
Masks: GO-05AW4_nails_final vertex groups AW3_{L,R}{D,P} (w>0.3), split into the 4 connected nail plates per foot, numbered medial->lateral.
Axes: per-foot unit axis fitted so the source tip (max X.a over each plate) reproduces the recorded rp1d source tips (8 values, residual <=0.003 mm).
Usage: python3 nailcheck.py PROD.npz(analysis frame cm: V,F) AW4_VF.npz nailmasks.npy footaxes_fit.json OUT.json"""
import sys, json, numpy as np
from scipy.spatial import cKDTree
P, AW, MK, AX, out = sys.argv[1:6]
V = np.load(P)['V'].astype(float); X = np.load(AW)['V'].astype(float); M = np.load(MK, allow_pickle=True).item(); A = json.load(open(AX))
Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0
R = {}
for n in sorted(M):
    a = np.array(A[n[0]]['a']); Np = X[M[n]]; tr = cKDTree(Np); dd, _ = tr.query(Vb, distance_upper_bound=0.002); reg = np.isfinite(dd)
    sp = float((Np @ a).max()); pp = float((Vb[reg] @ a).max()) if reg.any() else float('nan')
    R[n] = dict(source_tip_along_axis_m=round(sp, 5), production_tip_along_axis_m=round(pp, 5), projection_delta_mm=round((pp - sp) * 1000, 3), production_points_in_plate_region=int(reg.sum()), within_0p15=bool(abs(pp - sp) * 1000 <= 0.15))
json.dump(R, open(out, 'w'), indent=1); print({n: R[n]['projection_delta_mm'] for n in R})
