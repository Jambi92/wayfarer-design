# elbow_ripple.py OUT.json SIDE ANGLE NAME=POSED.npz ... : high-frequency content of a candidate's posed displacement from W0 LBS (order 69f2660 §10 visual
# criterion made measurable). delta = X_cand - X_W0 (first entry must be W0); delta_s = 10 iterations of 0.5 self + 0.5 one-ring mean; ripple = |delta - delta_s|
# on the arm part within 18 cm (rest) of the elbow pivot. Reported: p95 / p99 / max ripple (mm) and the share of the displacement energy that is ripple.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import bl_to_src
O, S, A = sys.argv[1:4]; items = [a.split('=', 1) for a in sys.argv[4:]]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); deg = np.bincount(E.ravel(), minlength=nV).astype(float)
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
e = bl_to_src(np.array(B['forearm_' + S]['head'])[None])[0]; d = np.linalg.norm(V0 - e, axis=1)
arm = np.zeros(nV, bool); arm[Q[FP == PARTS.index('arm_' + S)].ravel()] = True; m = arm & (d < 18)
Xw = np.load(items[0][1])['V'].astype(float); out = json.load(open(O)) if os.path.exists(O) else {}
for nm, pth in items:
    D = np.load(pth)['V'].astype(float) - Xw; Ds = D.copy()
    for _ in range(10):
        M = np.zeros_like(Ds); np.add.at(M, E[:, 0], Ds[E[:, 1]]); np.add.at(M, E[:, 1], Ds[E[:, 0]]); Ds = 0.5 * Ds + 0.5 * M / deg[:, None]
    r = np.linalg.norm(D - Ds, axis=1)[m] * 10; en = (np.linalg.norm(D, axis=1)[m] ** 2).sum()
    out['%s_%s_%s' % (nm, S, A)] = dict(ripple_p95_mm=round(float(np.percentile(r, 95)), 3), ripple_p99_mm=round(float(np.percentile(r, 99)), 3), ripple_max_mm=round(float(r.max()), 3),
                                        ripple_energy_share=round(float((r ** 2).sum() / 100 / en), 4) if en > 0 else 0.0, max_disp_cm=round(float(np.linalg.norm(D, axis=1)[m].max()), 3))
    print(nm, S, A, out['%s_%s_%s' % (nm, S, A)])
json.dump(out, open(O, 'w'), indent=1)
