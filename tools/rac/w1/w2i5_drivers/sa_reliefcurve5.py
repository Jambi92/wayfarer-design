# RAC W2I5 §4 diagnostic detail: vertical autocorrelation curve (lags 0.5-9 cm) of the 1.5 cm high-pass relief on the medial / posterior
# mid-thigh (sa_thighrelief5 sector), frozen vs W2I4 vs W2I5 - shows WHY the sa_thighrelief metric (first lag below 0.5) reads > 9 cm for W2I5.
# Usage: python3 sa_reliefcurve5.py OUT.json
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_sculpt as SC
FN = SC.FN; L = FN.L; V0 = FN.V0.astype(float); u0 = V0[:, 2]
idx = np.where((L.leg > 0.6) & (u0 > 66) & (u0 < 84) & (L.tail < 0.05))[0]; al, _ = SC.sectors(idx); mp = idx[al < -0.35]
FN._DF = FN.finish_delta()[0]; P4 = FN.build_f({})[0]; P5 = SC.build_s({})[0]; out = {}
for nm, P in (('frozen', V0), ('W2I4', P4), ('W2I5', P5)):
    N = FN.normals(P); S15 = FN.gsmooth(P, idx, 1.5); r = np.zeros(len(P)); r[idx] = np.einsum('ij,ij->i', P[idx] - S15, N[idx])
    tr = cKDTree(P); smp = np.random.default_rng(3).choice(mp, 5000, replace=False); n = N[smp]; zt = np.array([0, 0, 1.]) - n * n[:, 2:3]; zt /= np.linalg.norm(zt, axis=1, keepdims=True)
    out[nm] = {}
    for dl in (0.5, 1, 2, 3, 4, 6, 9):
        j = tr.query(P[smp] + dl * zt)[1]; out[nm][str(dl)] = float(np.corrcoef(r[smp], r[j])[0, 1])
    print(nm, {k: round(v, 2) for k, v in out[nm].items()}, flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
