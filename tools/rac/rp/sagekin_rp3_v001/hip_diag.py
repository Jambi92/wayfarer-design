# hip_diag.py OUT.json CAND:LABEL ... : order c6c7940 diagnostic -- why does the hip band count differ between family realizations that share one topology?
# Re-runs the validator v2 band construction (D4 scale) for hip_l / hip_r on each candidate and reports, per band side: the surface endpoints, the
# Dijkstra side path, every path edge's angle to the station axis, the counted (|e.d| > 0.5|e|) edges, the closed family loops the path crosses
# (topological, identical ids across realizations), the band length 2W and the axial span of each crossed loop on that side.
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import *
from val2lib import REF_STATURE_CM
from scipy.sparse.csgraph import dijkstra
OUT = sys.argv[1]; res = {}
Lref = None
for arg in sys.argv[2:]:
    p, lab = arg.split(':'); cz = np.load(p); V = cz['V'].astype(float); Q = np.asarray(cz['Q']); meta = json.loads(str(cz['meta']))
    loops = closed_loops(Q, len(V)) if Lref is None else Lref; Lref = loops; au = Auditor(V, Q)
    vl = {}
    for i, L in enumerate(loops):
        for v in L: vl.setdefault(int(v), []).append(i)
    st = float(V[:, 2].max() - V[:, 2].min()); s = st / REF_STATURE_CM; S = {x[0]: x for x in stations(meta)}; out = {}
    for nm in ('hip_l', 'hip_r'):
        _, c, d, Wd, Rr, need, Rp = S[nm]; Wd *= s; Rr *= s; c = np.asarray(c, float); d = unit(np.asarray(d, float))
        pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); sides = {}
        for side, sn in ((pp, '+p'), (-pp, '-p'), (qq, '+q'), (-qq, '-q')):
            a = au.surf(c - d * Wd, side, Rr); b = au.surf(c + d * Wd, side, Rr)
            _, pred = dijkstra(au.G, indices=a, return_predecessors=True, limit=4 * Wd + 3 * Rr)
            if pred[b] < 0: sides[sn] = 'no_path'; continue
            path = [b]
            while path[-1] != a: path.append(int(pred[path[-1]]))
            e = np.diff(V[path], axis=0); ang = np.degrees(np.arccos(np.clip(np.abs(e @ d) / np.linalg.norm(e, axis=1), 0, 1)))
            cnt = int((ang < 60).sum())
            # topological loop crossings: an edge crosses from loop-set A to loop-set B when its end vertices share no closed loop
            cross = [k for k in range(len(path) - 1) if not (set(vl.get(path[k], [])) & set(vl.get(path[k + 1], [])))]
            ax = (V[path] - c) @ d
            sides[sn] = dict(endpoints=[int(a), int(b)], endpoint_axial_cm=[round(float((V[a] - c) @ d), 3), round(float((V[b] - c) @ d), 3)], path_len=len(path), counted=cnt,
                             edge_angles_deg=[round(float(x), 1) for x in ang], topological_crossings=len(cross), crossing_angles_deg=[round(float(ang[k]), 1) for k in cross],
                             uncounted_crossings=[round(float(ang[k]), 1) for k in cross if ang[k] >= 60], path_axial_span_cm=round(float(ax.max() - ax.min()), 3),
                             mean_crossing_edge_len_cm=round(float(np.linalg.norm(e[cross], axis=1).mean()), 3) if cross else None, path=[int(x) for x in path])
        out[nm] = dict(W_cm=round(Wd, 3), band_len_cm=round(2 * Wd, 3), R_cm=round(Rr, 3), required=need, station_scale=round(s, 5), sides=sides)
    res[lab] = dict(file=os.path.basename(p), stature=round(st, 3), stations=out)
    print(lab, {nm: {sn: (v['counted'], v['topological_crossings'], v['uncounted_crossings'], v['path_axial_span_cm']) if isinstance(v, dict) else v for sn, v in o['sides'].items()} for nm, o in out.items()}, flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
