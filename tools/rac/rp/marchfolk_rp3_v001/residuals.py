# residuals.py CORE.npz OUT.json : v003 residual-station analysis (order 103c832 §8 "identify exact station; show why fixing it would damage
# anatomy / topology"). For every station that still fails firm or strict in either configuration: per-side band geometry (ray-exit endpoints a / b,
# their distance and AXIAL separation vs the nominal band 2W, path length, axial edges counted, crossings per cm of axial span), nearest pole in loops,
# closed rings encircling the joint with the station radius and with an anatomical radius (thumb MCP cross-section reaches ~2.8 cm), and the extra
# edge density the band count would need on the short-span side.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
B = load(); z = np.load(sys.argv[1]); M3 = sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Q = z['Q']; nV = M3.shape[0]
loops = closed_loops(Q, nV); OUT = {}
for C in 'MF':
    V = M3 @ B[C]['Vh']; meta = B[C]['meta']; R = full_s7(V, Q, meta, loops); au = Auditor(V, Q); S = {s[0]: s for s in stations(meta)}; JR = {j[0]: j for j in ring_stations(meta)}
    for k, r in R.items():
        if r['firm'] and r['strict']: continue
        _, c, d, Wd, Rr, need, Rp = S[k]; d = unit(np.asarray(d)); c = np.asarray(c)
        pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); sides = []
        for side, nm in ((pp, '+p'), (-pp, '-p'), (qq, '+q'), (-qq, '-q')):
            a = au.surf(c - d * Wd, side, Rr); b = au.surf(c + d * Wd, side, Rr); dist = float(np.linalg.norm(V[a] - V[b])); ax = float((V[b] - V[a]) @ d)
            ent = dict(side=nm, endpoint_dist_cm=round(dist, 3), axial_separation_cm=round(ax, 3), nominal_band_cm=2 * Wd, merged=bool(dist < 0.7 * 2 * Wd))
            if not ent['merged']:
                _, pred = dijkstra(au.G, indices=a, return_predecessors=True, limit=4 * Wd + 3 * Rr)
                if pred[b] >= 0:
                    path = [b]
                    while path[-1] != a: path.append(int(pred[path[-1]]))
                    P = V[path]; e = np.diff(P, axis=0); cnt = int((np.abs(e @ d) > 0.5 * np.linalg.norm(e, axis=1)).sum())
                    ent.update(path_len_cm=round(float(np.linalg.norm(e, axis=1).sum()), 3), axial_edges=cnt, crossings_per_cm=round(cnt / max(abs(ax), 1e-3), 2),
                               edge_len_needed_on_span_cm=round(abs(ax) / need, 3) if need else None)
            sides.append(ent)
        rn = ring_name(k); ring_std = len(encircling(V, loops, *JR[rn][1:5])) if rn in JR else None
        ring_anat = len(encircling(V, loops, JR[rn][1], JR[rn][2], 3.0, JR[rn][4])) if rn in JR else None
        OUT.setdefault(C, {})[k] = dict(firm=r['firm'], strict=r['strict'], loops_s7=r['loops_s7'], band_loops=r['loops'], loops_by_side=r['loops_by_side'], required=need, crease_poles=r['crease'],
                                        poles_within_2_loops=r['within2'], nearest_pole_loops=r['nearest_pole_loops'], local_edge_cm=round(r['h'], 3), sides=sides,
                                        closed_rings_station_radius=ring_std, closed_rings_radius_3cm=ring_anat)
json.dump(OUT, open(sys.argv[2], 'w'), indent=1)
for C, v in OUT.items():
    for k, e in v.items(): print(C, k, 'firm' if e['firm'] else 'FIRM-FAIL', e['loops_by_side'], 'rings', e['closed_rings_station_radius'], '->', e['closed_rings_radius_3cm'], [(s['side'], s['axial_separation_cm'], s.get('axial_edges')) for s in e['sides']])
