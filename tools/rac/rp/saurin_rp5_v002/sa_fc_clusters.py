# sa_fc_clusters.py CAGE.npz OUT.json : T-1 (> 3 mm) / T-2 (> 1.5 mm in identity zones) error clusters and T-4 quality clusters (order f0a2b96 §4 / §10)
import sys, json, numpy as np, igl, collections
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002'); import sa_geo as G
from scipy.sparse.csgraph import connected_components
import scipy.sparse as sp
z = np.load(sys.argv[1]); Q = z['Q']; Vc = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
d = np.sqrt(igl.point_mesh_squared_distance(G.V, Vc, T)[0]) * 10; lab = G.LAB
zone = np.full(G.NV, '', object); zone[lab == 'head'] = 'head'; zone[np.isin(lab, ['hand_xneg', 'hand_xpos'])] = 'hands'; zone[np.isin(lab, ['foot_xneg', 'foot_xpos'])] = 'feet'
zone[(lab == 'tail') & (np.linalg.norm(G.V - G.LM['tail_root_centre'], axis=1) < 18)] = 'tail_root'; zone[(lab == 'tail') & (zone == '')] = 'tail_stations'
def anat(p, l):
    x, f, u = p
    if 145 < u < 156 and 13 < abs(x) < 21: return 'axilla vault'
    if 156 <= u < 165 and abs(x) > 15: return 'shoulder-neck slope'
    if l == 'head': return 'snout / rostrum (lip crease, nostril)' if f > 6 else 'head'
    if 'hand' in l or ('arm' in l and u < 100): return 'hand / thumb base'
    if 'foot' in l: return 'foot / toe'
    if 92 < u < 103 and abs(x) < 8 and f > -12: return 'ventral pelvis / perineum'
    if l == 'tail' or (88 < u < 125 and f < -10): return 'body quads at the tail-module root'
    return l
def clusters(mask, vals):
    idx = np.nonzero(mask)[0]
    if not len(idx): return []
    nc, cl = connected_components(G.G[idx][:, idx], directed=False); out = []
    for k in range(nc):
        m = idx[cl == k]; c = G.V[m].mean(0)
        out.append(dict(anatomy=anat(c, str(lab[m[0]])), centre_cm=np.round(c, 1).tolist(), count=int(len(m)), max_mm=round(float(vals[m].max()), 3), p95_mm=round(float(np.percentile(vals[m], 95)), 3)))
    return sorted(out, key=lambda r: -r['max_mm'])
t1 = clusters(d > 3.0, d); t2 = clusters((zone != '') & (d > 1.5), d)
CAUSE = {'axilla vault': ('TOPOLOGY + PROJECTION', 'the vault pocket rises ~6-10 cm above the hole bottom row inside a fused section; the cage spans the pocket mouth. Fix: hole bottom row authored INTO the vault (vault-apex corner + its own support ring) with a local sliding pass; the cc5 trial (row moved to the apex by sections) regressed -> needs an authored vault patch, not row heights'),
         'shoulder-neck slope': ('PROJECTION / RELAX', 'trapezius-deltoid concavity between T0 and T1 rows; bounded fix: one support row at u ~160 on cols 2-6 / 10-14'),
         'snout / rostrum (lip crease, nostril)': ('PROJECTION', 'lip-crease / nostril pits narrower than the 2 mm head edge; fix: crease-snapped row on the mouth slit, nostril pit rings'),
         'hand / thumb base': ('TOPOLOGY (local)', 'thumb hole / palm 2:1 row corners; fix: thumb-base support ring + 2:1 row re-phase'),
         'foot / toe': ('PROJECTION', 'web saddles / toe-pad creases; fix: web quad corner sliding'),
         'ventral pelvis / perineum': ('TOPOLOGY (local)', 'large crotch quads (P4_0 - crotch - P4_8); fix: extra perineal row'),
         'body quads at the tail-module root': ('PROJECTION', 'body ring P0-P4 quads just cranial of the module root ring (module fixed); fix: P-row redistribution + sliding')}
for r in t1 + t2:
    c = CAUSE.get(r['anatomy'], ('PROJECTION', 'local projection miss')); r['cause'] = c[0]; r['proposed_bounded_correction'] = c[1]
# T-4
ang = []
for k in range(4):
    p0, p1, p2 = Vc[Q[:, (k - 1) % 4]], Vc[Q[:, k]], Vc[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
    ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / (np.linalg.norm(u1, axis=1) * np.linalg.norm(u2, axis=1) + 1e-12), -1, 1))))
ang = np.stack(ang, 1); sd = np.stack([np.linalg.norm(Vc[Q[:, (k + 1) % 4]] - Vc[Q[:, k]], axis=1) for k in range(4)], 1); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9)
ql = z['qlab'].astype(str); TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
CRIT = {'shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'neck', 'finger', 'thumb', 'toe'}
t4 = {}
for L in np.unique(ql):
    m = ql == L; bad_a = m & (asp > 4); bad_g = m & ((ang.min(1) < 45) | (ang.max(1) > 135))
    if bad_a.any() or bad_g.any():
        t4[L] = dict(quads=int(m.sum()), aspect_gt4=int(bad_a.sum()), max_aspect=round(float(asp[m].max()), 2), angle_outliers=int(bad_g.sum()), min_angle=round(float(ang[m].min()), 1),
                     max_angle=round(float(ang[m].max()), 1), deformation_critical=L in CRIT, tip_exemption_zone=bool(L in ('finger_cap', 'thumb_cap', 'toe_cap', 'tail')))
res = dict(T1_over_3mm_clusters=t1, T2_over_1p5mm_clusters=t2, T4_by_region=t4,
           T4_totals=dict(aspect_gt4=int((asp > 4).sum()), aspect_gt4_outside_tip_zones=int(((asp > 4) & ~TIP).sum()), angle_outliers=int(((ang.min(1) < 45) | (ang.max(1) > 135)).sum()),
                          near_zero_edges_lt_0p05mm=int((sd < 0.005).sum()), max_aspect=round(float(asp.max()), 2)))
json.dump(res, open(sys.argv[2], 'w'), indent=1)
print('T1 clusters', len(t1), [(r['anatomy'], r['max_mm']) for r in t1[:8]]); print('T2 clusters', len(t2), collections.Counter(r['anatomy'] for r in t2)); print(res['T4_totals'])
print({k: (v['aspect_gt4'], v['angle_outliers']) for k, v in t4.items() if v['aspect_gt4'] > 10})
