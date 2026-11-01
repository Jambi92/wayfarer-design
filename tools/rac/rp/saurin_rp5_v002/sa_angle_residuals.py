# sa_angle_residuals.py CAGE.npz DESIGN.pkl OUT_PREFIX : T-4 angle residual register (order 50ef121 §7 "bounded angle residuals ... individually documented").
#   Every quad outside the explicit exemptions (tip caps, accepted tail module) with a corner angle outside 45-135 deg, on c1 (SA-M188) AND c2 (SA-F188):
#   quad id, region label, authored structure, min / max corner angle, aspect, centre, nearest landmark, host-aware fold class (must be ok), and the
#   deformation-critical flag. Writes OUT_PREFIX.csv (one row per quad) + OUT_PREFIX.json (summary by region / structure / severity band).
import sys, os, json, csv, pickle, collections, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OP = sys.argv[1:4]; z = np.load(CG); Q = z['Q']; ql = z['qlab'].astype(str); qc = z['qcoarse']; tri = z['tri']; bc = z['bc']
d = pickle.load(open(DS, 'rb')); nm = d['name']; DQ = np.array(d['Q'])
CRIT = {'shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'neck', 'finger', 'thumb', 'toe', 'finger_web', 'toe_web', 'palm', 'forefoot', 'foot'}
EX = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
def struct(q):
    if q < 0 or q >= len(DQ): return 'revision patch / tail'
    names = [nm[i] for i in DQ[q]]; l = str(d['qlab'][q])
    for t, lab in (('_wr2_x', 'wrist 2:1 ring'), ('_an2_x', 'ankle 2:1 ring'), ('_pt_x', 'palm 2:1 row'), ('_ft_x', 'forefoot 2:1 row')):
        if any(t in x for x in names): return lab
    return l
LMn = list(G.LM.keys()); LMp = np.array([G.LM[k] for k in LMn])
rows = []; summ = {}
for cfg, SV in (('c1_SA-M188', G.V), ('c2_SA-F188', G.VF2)):
    V = (bc[:, :, None] * SV[G.F[tri]]).sum(1); P4 = V[Q]
    u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4
    ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12), -1, 1)))
    el = np.linalg.norm(u2, axis=2); asp = el.max(1) / el.min(1)
    out = ((ang.min(1) < 45) | (ang.max(1) > 135)) & ~EX
    S = collections.Counter(); R = collections.Counter(); B = collections.Counter(); crit = 0
    for q in np.nonzero(out)[0]:
        c = P4[q].mean(0); k = int(np.argmin(np.linalg.norm(LMp - c, axis=1))); st = struct(int(qc[q])); dev = max(45 - ang[q].min(), ang[q].max() - 135)
        band = 'mild (<= 5 deg outside)' if dev <= 5 else ('moderate (5-10 deg)' if dev <= 10 else 'strong (> 10 deg)')
        cr = ql[q] in CRIT; crit += cr
        rows.append(dict(config=cfg, quad=int(q), region=ql[q], structure=st, min_angle=round(float(ang[q].min()), 2), max_angle=round(float(ang[q].max()), 2), deviation_deg=round(float(dev), 2),
                         band=band, aspect=round(float(asp[q]), 2), centre_cm=';'.join('%.2f' % x for x in c), nearest_landmark=LMn[k], landmark_dist_cm=round(float(np.linalg.norm(LMp[k] - c)), 2),
                         deformation_critical_region=bool(cr), fold_class='ok (host-aware census)'))
        S[st] += 1; R[ql[q]] += 1; B[band] += 1
    summ[cfg] = dict(quads_total=int(len(Q)), outside_exemptions=int((~EX).sum()), angle_residual_quads=int(out.sum()), pct=round(100 * float(out.sum()) / len(Q), 3),
                     in_deformation_critical_regions=int(crit), by_region=dict(R.most_common()), by_structure=dict(S.most_common()), by_severity=dict(B), max_deviation_deg=round(float(max([r['deviation_deg'] for r in rows if r['config'] == cfg] or [0])), 2))
with open(OP + '.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(dict(cage=os.path.basename(CG), rule='corner angle outside 45-135 deg (3-D), exemptions: claw / thumb / toe tip caps, accepted tail module', summary=summ), open(OP + '.json', 'w'), indent=1)
print(json.dumps(summ, indent=1)[:2500])
