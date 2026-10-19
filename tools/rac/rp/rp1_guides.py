"""RAC RP1-A: reference guide table for the manual cage (read-only measurement of the source).
For each limb / trunk / neck segment: axis end points (from the source landmark sections) and the mean section half-widths at
evenly spaced stations, in Blender metres (x = subject left, y = -forward, z up). The artist uses these as reference; they are
not topology. Usage: python3 rp1_guides.py weld_a.npz landmarks_source.json OUT.json"""
import sys, json, numpy as np
z = np.load(sys.argv[1]); V = z['V'].astype(float); F = z['F'].astype(np.int64); L = json.load(open(sys.argv[2]))
E = np.unique(np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1), axis=0)
def sec(p, n, R):
    loc = np.linalg.norm(V - p, axis=1) < R * 1.2; e = E[loc[E[:, 0]] | loc[E[:, 1]]]; d = (V - p) @ n
    e = e[d[e[:, 0]] * d[e[:, 1]] < 0]; t = d[e[:, 0]] / (d[e[:, 0]] - d[e[:, 1]]); X = V[e[:, 0]] + (V[e[:, 1]] - V[e[:, 0]]) * t[:, None]
    X = X[np.linalg.norm(X - p, axis=1) < R]
    if len(X) < 8: return None
    c = X.mean(0); r = np.linalg.norm(X - c, axis=1); return c, float(np.median(r)), float(r.max()), len(X)
c = lambda k: np.array(L[k]['centroid'])
segs = {}
for s in ('L', 'R'):
    segs['thigh_' + s] = (c('hip_' + s), c('knee_' + s), 18); segs['shin_' + s] = (c('knee_' + s), c('ankle_' + s), 12)
    segs['upperarm_' + s] = (c('shoulder_' + s), c('elbow_' + s), 12); segs['forearm_' + s] = (c('elbow_' + s), c('wrist_' + s), 9)
segs['trunk'] = (c('pelvis_root'), c('neck_min'), 40)
out = {'frame': 'Blender metres: x = subject left, y = -forward, z = up', 'segments': {}}
B = lambda p: [round(p[0] / 100, 4), round(-p[1] / 100, 4), round(p[2] / 100, 4)]
for k, (a, b, R) in segs.items():
    ax = (b - a) / np.linalg.norm(b - a); st = []
    for t in np.linspace(0, 1, 9):
        p = a + (b - a) * t; r = sec(p, ax, R)
        if r: st.append({'t': round(float(t), 3), 'centre_m': B(r[0]), 'median_radius_cm': round(r[1], 2), 'max_radius_cm': round(r[2], 2)})
    out['segments'][k] = {'start_m': B(a), 'end_m': B(b), 'length_cm': round(float(np.linalg.norm(b - a)), 2),
                          'axis_blender': [round(ax[0], 4), round(-ax[1], 4), round(ax[2], 4)], 'stations': st}
out['tail_chain_m'] = [B(np.array(s['centroid'])) for s in L['tail_chain']['stations']]
json.dump(out, open(sys.argv[3], 'w'), indent=1)
for k, v in out['segments'].items(): print(k, v['start_m'], v['end_m'], v['length_cm'], [s['median_radius_cm'] for s in v['stations']])
print('tail', out['tail_chain_m'])
