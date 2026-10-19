"""RAC RP1-A diagnostic: density needed for the accepted deviation tolerances (T-1 / T-2), from source curvature.
Chord model: a production quad of edge h whose vertices lie on the source surface deviates by about kappa*h^2/8 where the
surface curvature is kappa. Required h = sqrt(8 e / kappa). Read-only analysis of the welded working copy (cm).
Usage: python3 rp1_density.py weld_a.npz zones.npz OUT.json"""
import sys, json, numpy as np, igl
z = np.load(sys.argv[1]); V = z['V'].astype(np.float64); F = z['F'].astype(np.int64)
Z = np.load(sys.argv[2]); zone = Z['zone']; names = list(Z['names'])
pd1, pd2, k1, k2, _ = igl.principal_curvature(V, F, radius=3)
kap = np.maximum(np.abs(k1), np.abs(k2))                           # 1/cm
A = igl.doublearea(V, F) / 2; va = np.zeros(len(V)); np.add.at(va, F.ravel(), np.repeat(A / 3, 3))
TOL = {'general': (0.15, 0.30), 'identity': (0.08, 0.15)}       # cm: (p95, max)
out = {}
for zi, nm in enumerate(names):
    m = zone == zi
    if not m.any(): continue
    kind = 'general' if nm == 'general' else 'identity'
    e95, emax = TOL[kind]
    k95, k999 = np.percentile(kap[m], 95), np.percentile(kap[m], 99.9)
    h95 = np.sqrt(8 * e95 / k95); hmax = np.sqrt(8 * emax / k999); h = min(h95, hmax)
    area = va[m].sum()
    out[nm] = {'tolerance': kind, 'area_cm2': round(float(area), 1), 'kappa_p50_p95_p999_per_cm': [round(float(x), 4) for x in np.percentile(kap[m], [50, 95, 99.9])],
               'h_for_p95_cm': round(float(h95), 3), 'h_for_max_cm': round(float(hmax), 3), 'h_required_cm': round(float(h), 3), 'quads_estimate': int(area / h ** 2)}
out['total_quads_estimate'] = sum(v['quads_estimate'] for v in out.values())
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(json.dumps(out, indent=1))
