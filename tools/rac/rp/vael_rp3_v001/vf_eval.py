# vf_eval.py OUT.json CFG : Vael elf-frame order §11 / §12 / §15 / §16 -- for VD2 and VF1 / VF2 / VF3 of one configuration against Marchfolk, Sagekin,
# frozen Fenn and frozen Aelari at 178 cm:
#  * shoulder spans / stature: clavicle span (distance between the two shoulder-joint centres along the clavicle ends = upperarm heads, rest), shoulder-joint
#    breadth (arm_measure glenohumeral), bideltoid breadth;
#  * long-bone shaft envelope at mid-shaft (t = 0.5 of the bone, +/- 2.5 cm x H/173 slab, limb-weighted vertices within 12 cm of the bone axis, projected perpendicular to it; breadth = major / depth = minor principal
#    extent) for upper arm, forearm, thigh, calf, / stature and as change vs VD2;
#  * joint / base measures: elbow, wrist, knee, ankle (arm_measure ratios), palm root / wrist, heel / foot length (as vd_eval.py);
#  * torso regression: thorax max breadth, waist, crest, thorax depth (/ stature), waist / lower-rib breadth; field audit (|V - V_VD2| per region).
import sys, os, json, numpy as np
OUT, CF = sys.argv[1:3]; VF = os.environ.get('VF_DIR', '/tmp/claude-0/rt/vf'); PA = os.environ.get('VA_PA', '/tmp/claude-0/rt/va/partA')
P_ = {'c1': 'VAL4-R1-VD2', 'c2': 'VALF178-R1-VD2'}[CF]; SX = {'c1': 'M', 'c2': 'F'}[CF]
SRC = {'VD2': '/tmp/claude-0/rt/vd/cand/' + P_}; SRC.update({t: '%s/cand/%s-%s' % (VF, P_, t) for t in ('VF1', 'VF2', 'VF3')})
for k in ('MF', 'SG', 'FN', 'AE'): SRC[k] = '%s/cmp/%s%s178' % (PA, k, SX)
jl = lambda p: json.load(open(p))
REST = {k: np.load(p + '_rest.npz') for k, p in SRC.items()}; R6 = {k: np.load(p + '_r6.npz') for k, p in SRC.items()}; MEAS = {k: jl(p + '_meas.json')['combined'] for k, p in SRC.items()}
def shaft(z, b, H):
    V = z['V'].astype(float); keep = z['keep']; J = json.loads(str(z['joints'])); out = []
    for sd in ('l', 'r'):
        h, t = np.array(J[b + '_' + sd][0]), np.array(J[b + '_' + sd][1]); ax = t - h; L = np.linalg.norm(ax); ax /= L
        grp = ('upperarm', 'lowerarm') if b in ('upperarm', 'lowerarm') else ('thigh', 'calf')
        wb = sum(z['w_' + g + '_' + sd] for g in grp); q = V - h; tt = q @ ax; P0 = q - np.outer(tt, ax)
        s = keep & (wb > 0.3) & (np.abs(tt - 0.5 * L) < 2.5 * H / 173.14) & (np.linalg.norm(P0, axis=1) < 12.0 * H / 173.14)
        P = P0[s]; ev, evc = np.linalg.eigh(np.cov(P.T)); a1, a2 = evc[:, -1], evc[:, -2]
        out.append(((P @ a1).max() - (P @ a1).min(), (P @ a2).max() - (P @ a2).min()))
    o = np.mean(out, 0); return dict(breadth_share=float(o[0] / H), depth_share=float(o[1] / H), section_share=float(np.sqrt(o[0] * o[1]) / H))
def bases(z, m):
    V = z['V'].astype(float); keep = z['keep']; J = json.loads(str(z['joints'])); w = lambda k: z['w_' + k].astype(float); H = m['stature']; pr, hr = [], []
    for sd in ('l', 'r'):
        wr, mid = np.array(J['hand_' + sd][0]), np.array(J['middle_01_' + sd][0]); ax = mid - wr; L = np.linalg.norm(ax); ax /= L
        s = keep & (w('hand_' + sd) > 0.5) & (np.abs(((V - wr) @ ax) / L - 0.40) < 0.05); Q = V[s] - wr; Q -= np.outer(Q @ ax, ax); ev, evc = np.linalg.eigh(np.cov(Q.T)); wd = evc[:, -1]
        pr.append((Q @ wd).max() - (Q @ wd).min())
        an, bl = np.array(J['foot_' + sd][0]), np.array(J['ball_' + sd][0]); fa = an - bl; fa[2] = 0; Lf = np.linalg.norm(fa); fa /= Lf; mh = np.array([-fa[1], fa[0], 0])
        s = keep & ((w('foot_' + sd) + w('ball_' + sd)) > 0.5) & (((V - bl) @ fa) / Lf > 0.85) & (V[:, 2] < an[2] - 3.0 * H / 173.14); u = V[s] @ mh; hr.append(u.max() - u.min())
    MM = m['mean']; return dict(palm_root_over_wrist=float(np.mean(pr) / MM['wrist_breadth']), heel_over_foot_length=float(np.mean(hr) / MM['foot_len']))
res = dict(cfg=CF, sources=SRC, spans={}, shafts={}, bases={}, torso={}, audit={})
for k, z in REST.items():
    m = MEAS[k]; H = m['stature']; J = json.loads(str(z['joints'])); ua = np.linalg.norm(np.array(J['upperarm_l'][0]) - np.array(J['upperarm_r'][0]))
    res['spans'][k] = dict(clavicle_span_share=ua / H, shoulder_joint_share=m['shoulder_joint_breadth'] / H, bideltoid_share=m['bideltoid_breadth'] / H)
    res['shafts'][k] = {b: shaft(z, b, H) for b in ('upperarm', 'lowerarm', 'thigh', 'calf')}
    r = m['ratio']; res['bases'][k] = dict(elbow_over_humerus=r['elbow_over_humerus'], wrist_over_forearm=r['wrist_over_forearm'], knee_over_femur=r['knee_over_femur'], ankle_over_shin=r['ankle_over_shin'],
                                          palm_breadth_over_hand=r['palm_breadth_over_hand'], foot_breadth_over_length=m['mean']['foot_breadth'] / m['mean']['foot_len'], **bases(z, m),
                                          elbow_share=m['mean']['elbow_breadth'] / H, wrist_share=m['mean']['wrist_breadth'] / H, knee_share=m['mean']['knee_breadth'] / H, ankle_share=m['mean']['ankle_breadth'] / H)
    res['torso'][k] = dict(thorax_breadth_max_share=m['thorax_breadth_max'] / H, waist_share=m['waist_breadth'] / H, crest_share=m['iliac_crest_breadth'] / H, thorax_depth_share=m['thorax_depth_max'] / H,
                           pelvic_depth_share=m['pelvic_depth'] / H, arm_share=r['arm_share'], leg_share=r['leg_share'], hand_share=r['hand_share'], foot_share=r['foot_share'])
rel = lambda a, b: round(100 * (a / b - 1), 2)
for grp in ('spans', 'torso', 'bases'):
    for k in list(res[grp]):
        res[grp][k] = {q: round(v, 5) for q, v in res[grp][k].items()}
res['spans_vs_MF_pct'] = {k: {q: rel(v, res['spans']['MF'][q]) for q, v in d.items()} for k, d in res['spans'].items()}
res['shafts_vs_VD2_pct'] = {k: {b: {q: rel(v, res['shafts']['VD2'][b][q]) for q, v in d.items()} for b, d in sh.items()} for k, sh in res['shafts'].items()}
res['shafts_vs_MF_pct'] = {k: {b: {q: rel(v, res['shafts']['MF'][b][q]) for q, v in d.items()} for b, d in sh.items()} for k, sh in res['shafts'].items()}
res['bases_vs_MF_pct'] = {k: {q: rel(v, res['bases']['MF'][q]) for q, v in d.items()} for k, d in res['bases'].items()}
res['torso_vs_MF_pct'] = {k: {q: rel(v, res['torso']['MF'][q]) for q, v in d.items()} for k, d in res['torso'].items()}
for t in ('VF1', 'VF2', 'VF3'):
    dR = np.linalg.norm(REST[t]['V'].astype(float) - REST['VD2']['V'].astype(float), axis=1); d6 = np.linalg.norm(R6[t]['V'].astype(float) - R6['VD2']['V'].astype(float), axis=1)
    z = REST['VD2']; W = {k[2:]: z[k] for k in z.files if k.startswith('w_')}; reg = {}
    for nm, ks in (('clavicle / shoulder', ('clavicle_l', 'clavicle_r')), ('upper arm', ('upperarm_l', 'upperarm_r')), ('forearm', ('lowerarm_l', 'lowerarm_r')), ('thigh', ('thigh_l', 'thigh_r')),
                   ('calf', ('calf_l', 'calf_r')), ('trunk', ('spine_01', 'spine_02', 'spine_03', 'pelvis')), ('hand / foot', ('hand_l', 'hand_r', 'foot_l', 'foot_r', 'fingers_l', 'fingers_r', 'ball_l', 'ball_r')),
                   ('head / neck', ('head', 'neck_01'))):
        mk = z['keep'] & (sum(W[k] for k in ks) > 0.3)
        reg[nm] = dict(vertices=int(mk.sum()), moved=int((dR[mk] > 0.01).sum()), max_cm=round(float(dR[mk].max()), 3) if mk.any() else 0.0, rms_cm=round(float(np.sqrt((dR[mk] ** 2).mean())), 3) if mk.any() else 0.0)
    res['audit'][t] = dict(affected_vertices_rest=int((dR > 0.01).sum()), max_cm_rest=float(dR.max()), rms_cm_rest_affected=float(np.sqrt((dR[dR > 0.01] ** 2).mean())), affected_vertices_r6=int((d6 > 0.01).sum()),
                           max_cm_r6=float(d6.max()), head_max_cm=float(dR[z['w_head'] > 0.5].max()), ears_max_cm=float(dR[z['w_ears'] > 0.05].max()), per_region=reg)
json.dump(res, open(OUT, 'w'), indent=1, default=float)
for k in ('VD2', 'VF1', 'VF2', 'VF3', 'SG', 'FN', 'AE'): print(CF, k, 'spans vs MF', res['spans_vs_MF_pct'][k], '| shafts vs VD2', {b: v['section_share'] for b, v in res['shafts_vs_VD2_pct'][k].items()})
for k in ('VD2', 'VF2', 'FN', 'AE'): print(CF, k, 'bases vs MF', res['bases_vs_MF_pct'][k])
for t in ('VF1', 'VF2', 'VF3'): print(CF, t, {q: v for q, v in res['audit'][t].items() if q != 'per_region'})
