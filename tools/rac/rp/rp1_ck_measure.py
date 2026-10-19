"""RAC RP1 checkpoint DIAGNOSTIC: two-way deviation by T-2 zone between the evaluated checkpoint mesh (rp1_ck_export.py) and the
welded source (weld_a.npz, analysis frame cm). prod->src samples face centroids + edge midpoints; src->prod uses every source vertex.
Usage: python3 rp1_ck_measure.py weld_a.npz zones.npz CK.npz OUT.json"""
import sys, json, numpy as np, igl
z = np.load(sys.argv[1]); V = z['V'].astype(np.float64); F = z['F'].astype(np.int64)
Z = np.load(sys.argv[2]); zone = Z['zone']; names = list(Z['names'])
c = np.load(sys.argv[3]); Ve = c['Ve']; Fe = c['Fe']
S = np.vstack([Ve[Fe].mean(1), (Ve[Fe[:, 0]] + Ve[Fe[:, 1]]) / 2])
dps, Ips, _ = igl.point_mesh_squared_distance(S, V, F); dps = np.sqrt(dps) * 10; zps = zone[F[Ips, 0]]
dsp, _, _ = igl.point_mesh_squared_distance(V, Ve, Fe); dsp = np.sqrt(dsp) * 10
tol = {'general': (0.5, 1.5, 3.0)}; t2 = (0.3, 0.8, 1.5)
out = {'eval_vertices': int(len(Ve)), 'eval_triangles': int(len(Fe)), 'cage': str(c['cage']), 'zones': {}}
for i, nm in enumerate(names):
    a = dps[zps == i]; b = dsp[zone == i]
    if len(b) == 0: continue
    lim = tol.get(nm, t2); st = lambda x: [round(float(v), 3) for v in (np.median(x), np.percentile(x, 95), x.max())] if len(x) else None
    pa, pb = st(a), st(b)
    ok = all(p is not None and p[0] <= lim[0] and p[1] <= lim[1] and p[2] <= lim[2] for p in (pa, pb))
    out['zones'][nm] = {'limit_med_p95_max_mm': list(lim), 'prod_to_src_mm': pa, 'src_to_prod_mm': pb,
                        'src_share_over_max_pct': round(float((b > lim[2]).mean() * 100), 2), 'within': ok}
json.dump(out, open(sys.argv[4], 'w'), indent=1)
np.savez_compressed(sys.argv[4].replace('.json', '_dist.npz'), dsp=dsp.astype(np.float32))
print(json.dumps(out, indent=1))
