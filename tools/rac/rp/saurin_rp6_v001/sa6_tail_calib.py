# sa6_tail_calib.py OUT.json BODYDIR NAME [ARTDIR|-] [POSES|tail] : tail-kink calibration data (offline bake validation order 8e3b7b4d §3).
#   Same body in three deformations: neutral (rest), plain LBS, packaged blend v004 ('prod', the unbaked production) and, when ARTDIR is given, the baked
#   artifact ARTDIR/BK_<NAME> (packaged blend + K, reopened from disk).  For every tail special-gate pose (sa6_gates.gate_poses, 'tail*') and every angle
#   fraction on a 0.025 grid (0.025 .. 1.0) the centreline of the 181 frozen tail rings is measured exactly as the rig-pilot audit does (sa6_eval.gate_metrics):
#     turning th_k   = angle (deg) between consecutive ring-centroid segments at ring k+1 (k = 0 .. 178)
#     kink_k         = th_k / mean(th over the 11-junction window centred on k), on junctions with th_k > 0.2 deg  (raw kink ratio; audit = max over k)
#     dth_k          = |th_k - th_k(neutral)|  (deformation-introduced turning; neutral curvature is inherited)  and its own windowed ratio (delta kink)
#     area retention = ring area / neutral ring area (rings[:-3], as the audit)
#   Per (column, pose, fraction): max raw kink with its ring, absolute turning there, neutral turning there, change from neutral, the window mean ('nearby
#   turning'), the max delta-kink, max absolute turning anywhere, min area retention, and the nearest tail joint (bone boundary) to the worst ring.
#   Concentration measures in absolute degrees (v2): excess e_k = th_k - window mean (how much one junction turns beyond its neighbours); its change from
#   neutral e_k - e0_k (concentration introduced or amplified by the deformation); and the introduced excess dth_k - window mean of dth.
#   Per (column, pose) the worst frame keeps the full per-junction arrays for the evidence plots.  -> OUT.json
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_common as C, sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL, sa6_gates as GT
OUT, BD, nm = sys.argv[1:4]; AD = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None; sel = sys.argv[5] if len(sys.argv) > 5 else 'tail'
t0 = time.time(); b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()])
K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm)) if AD else None
rings = C.load()['tail_rings']; TB = sorted(b_ for b_ in R.bi if b_.startswith('tail_'))
def cen(P): return np.array([P[rg].mean(0) for rg in rings])
def turning(P):
    dv = np.diff(cen(P), axis=0); dv /= np.linalg.norm(dv, axis=1, keepdims=True); return np.degrees(np.arccos(np.clip((dv[1:] * dv[:-1]).sum(1), -1, 1)))
def win(th): return np.array([th[max(0, k - 5):k + 6].mean() for k in range(len(th))])
def area(P, rg):
    X = P[rg] - P[rg].mean(0); n = np.linalg.svd(X)[2][-1]; return 0.5 * abs((np.cross(X, np.roll(X, -1, 0)) @ n).sum())
A0 = np.array([area(R.V, rg) for rg in rings[:-3]]); th0 = turning(R.V); c0 = cen(R.V); E0 = th0 - win(th0)
JH = {tb: np.asarray(R.H(tb), float) for tb in TB}
def boundary(k):
    """worst junction k sits at ring k+1: nearest tail joint head (bone boundary) to that ring centroid in neutral"""
    p = c0[k + 1]; d = {tb: float(np.linalg.norm(p - h)) for tb, h in JH.items()}; tb = min(d, key=d.get); return dict(ring=k + 1, nearest_joint=tb, distance_cm=round(d[tb], 3))
def measure(P):
    th = turning(P); w = win(th); m = th > 0.2; kr = np.where(m, th / np.maximum(w, 0.05), 0.0); k = int(kr.argmax()) if m.any() else int(th.argmax())
    dth = np.abs(th - th0); dw = win(dth); dm = dth > 0.2; dk = np.where(dm, dth / np.maximum(dw, 0.05), 0.0)
    ar = np.array([area(P, rg) for rg in rings[:-3]]) / A0
    e = th - w; ec = e - E0; de = dth - dw; ke, kc, kd = int(e.argmax()), int(ec.argmax()), int(de.argmax())
    ext = dict(excess_turning_max_deg=round(float(e.max()), 4), excess_junction=ke, excess_change_from_neutral_max_deg=round(float(ec.max()), 4), excess_change_junction=kc,
               introduced_excess_max_deg=round(float(de.max()), 4), introduced_excess_junction=kd, introduced_excess_boundary=boundary(kd))
    return dict(**ext, kink_max=round(float(kr.max()) if m.any() else 1.0, 4), junction=k, turning_deg=round(float(th[k]), 4), neutral_turning_deg=round(float(th0[k]), 4),
                change_from_neutral_deg=round(float(th[k] - th0[k]), 4), nearby_turning_deg=round(float(w[k]), 4), delta_kink_max=round(float(dk.max()) if dm.any() else 1.0, 4),
                delta_kink_junction=int(dk.argmax()), dturning_max_deg=round(float(dth.max()), 4), turning_max_deg=round(float(th.max()), 4), turning_max_junction=int(th.argmax()),
                area_retention_min=round(float(ar.min()), 4), area_min_ring=int(ar.argmin()), boundary=boundary(k)), (th, w, dth, ar)
GP = GT.gate_poses(R); poses = [p for p in GP if p.startswith('tail')] if sel == 'tail' else sel.split(',')
FR = [round(0.025 * i, 3) for i in range(1, 41)]
res = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, artifact=(os.path.join(AD, 'BK_%s.json' % nm) if AD else None), artifact_sha256=(C.sha(os.path.join(AD, 'BK_%s.json' % nm)) if AD else None),
           body_sha256=C.sha(os.path.join(BD, nm + '.npz')), definition='sa6_eval.gate_metrics tail kink (11-junction window, th > 0.2 deg), 181 frozen rings', fractions=FR,
           neutral=dict(turning_deg=[round(float(x), 4) for x in th0], kink_max=measure(R.V)[0]['kink_max'], turning_max_deg=round(float(th0.max()), 4)),
           joints={tb: boundary_ for tb, boundary_ in ((tb, int(np.linalg.norm(c0 - JH[tb], axis=1).argmin())) for tb in TB)}, poses={})
for pn in poses:
    spec = GP[pn]; res['poses'][pn] = {}
    for col in ('lbs', 'prod') + (('bake',) if K else ()):
        rows = {}; worst = None; worst2 = None
        for fr in FR:
            T = R.pose([(bb, p, a, dg * fr) for bb, p, a, dg in spec])
            d = None if col == 'lbs' else (P0.delta(T) + (K.delta(T) if col == 'bake' else 0))
            P = R.skin(T) if d is None else R.skin(T, R.V + d); m, arr = measure(P); rows['%.3f' % fr] = m
            if worst is None or m['kink_max'] > worst[0]['kink_max']: worst = (m, arr, fr)
            if worst2 is None or m['excess_change_from_neutral_max_deg'] > worst2[0]['excess_change_from_neutral_max_deg']: worst2 = (m, arr, fr)
        res['poses'][pn][col] = dict(frames=rows, worst_frame=worst[2], worst=worst[0], worst_arrays=dict(turning_deg=[round(float(x), 3) for x in worst[1][0]], window_deg=[round(float(x), 3) for x in worst[1][1]],
                                     dturning_deg=[round(float(x), 3) for x in worst[1][2]], area_retention=[round(float(x), 4) for x in worst[1][3]]),
                                     at_100=rows['1.000'], worst_concentration_frame=worst2[2], worst_concentration=worst2[0],
                                     worst_concentration_turning_deg=[round(float(x), 3) for x in worst2[1][0]])
    print(nm, pn, {c: (v['worst']['kink_max'], v['worst_frame'], v['at_100']['kink_max']) for c, v in res['poses'][pn].items()}, flush=True)
    json.dump(res, open(OUT + '.partial', 'w'))
res['seconds'] = round(time.time() - t0, 1)
from sa6_bake import peak_mb
res['peak_mb'] = round(peak_mb(), 1); json.dump(res, open(OUT, 'w'), indent=1); os.path.exists(OUT + '.partial') and os.remove(OUT + '.partial')
print(nm, 'TAIL CALIB done', round(res['seconds']), 's', flush=True)
