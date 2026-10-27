# sg_identity.py OUT.json FAM_CAND FAM_LOOPS OWN_R6 OTHER_R6:LABEL ... : order c6c7940 §14 Sagekin identity gate. Sagekin have no identity sculpt:
# the identity source is the accepted Sagekin R-6 source itself. All bodies are MPFB hm08 realizations in one frame (R-6, grounded, analysis frame),
# so two measures are reported per audit zone:
#   fit       -- family realization -> own source surface (closest point; the propagation error, T-1 / T-2);
#   signal    -- per-vertex correspondence displacement |M @ (own hm08 - other hm08)| from the family realization to where the SAME family vertex would
#                sit on the other body (Marchfolk at matched stature, the other Sagekin configuration): the race / configuration signal carried by the
#                realization; plus the closest-point surface distance to the other body (a lower bound, tangential differences invisible).
# Identity holds when fit << signal in every zone (the realization did not regress toward the other body).
import sys, json, numpy as np, trimesh, scipy.sparse as sp
OUT, fc, fl = sys.argv[1:4]; own = sys.argv[4]; others = sys.argv[5:]
F = np.load(fc); V = F['V'].astype(float); zone = np.load(fl, allow_pickle=True)['zone']; si = F['src_index']
M = sp.csr_matrix((F['M_data'], F['M_indices'], F['M_indptr']), shape=tuple(F['M_shape']))
def body(p):
    z = np.load(p); keep = z['keep']; Fx = z['F'][keep[z['F']].all(1)]; return z, trimesh.Trimesh(z['V'].astype(float), Fx, process=False)
zo, bo = body(own.split(':')[0]); own_lab = own.split(':')[1]; _, dfit, _ = trimesh.proximity.closest_point(bo, V); dfit *= 10
assert np.abs(M @ zo['V'][si].astype(float) - V).max() < 1e-4, 'family != M @ own hm08'
ZN = ['ALL'] + sorted(set(zone.tolist())); st = lambda d, m: dict(median_mm=round(float(np.median(d[m])), 3), p95_mm=round(float(np.percentile(d[m], 95)), 3), max_mm=round(float(d[m].max()), 3))
res = dict(family=fc.split('/')[-1], own_source=own_lab, zones={zn: dict(fit=st(dfit, np.ones(len(V), bool) if zn == 'ALL' else zone == zn)) for zn in ZN}, others=[])
for arg in others:
    p, lab = arg.split(':'); zx, bx = body(p); res['others'].append(lab)
    sig = np.linalg.norm(M @ (zo['V'][si].astype(float) - zx['V'][si].astype(float)), axis=1) * 10; _, dcp, _ = trimesh.proximity.closest_point(bx, V); dcp *= 10
    for zn in ZN:
        m = np.ones(len(V), bool) if zn == 'ALL' else zone == zn; res['zones'][zn]['signal_' + lab] = st(sig, m); res['zones'][zn]['surface_' + lab] = st(dcp, m)
res['verdict'] = {}
for zn, v in res['zones'].items():
    near = min(res['others'], key=lambda k: v['signal_' + k]['median_mm'])
    res['verdict'][zn] = dict(fit_p95_mm=v['fit']['p95_mm'], nearest_other=near, signal_median_mm=v['signal_' + near]['median_mm'], ratio_signal_median_over_fit_p95=round(v['signal_' + near]['median_mm'] / max(v['fit']['p95_mm'], 1e-3), 1),
                              identity_holds=v['fit']['p95_mm'] < 0.25 * v['signal_' + near]['median_mm'])
res['identity_holds_all_zones'] = all(x['identity_holds'] for x in res['verdict'].values())
json.dump(res, open(OUT, 'w'), indent=1)
for zn, v in res['verdict'].items(): print(zn, v)
print('IDENTITY HOLDS ALL ZONES', res['identity_holds_all_zones'])
