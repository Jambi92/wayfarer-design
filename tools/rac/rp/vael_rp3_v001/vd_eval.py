# vd_eval.py OUT.json CFG : Vael custom body-deformation order §8 / §11 / §12 -- for R1 and VD1 / VD2 / VD3 of one configuration (cand dir $VD_DIR/cand):
#  * field audit: per-region affected vertex counts, max and RMS displacement (field parts on the R1 rest mesh) and the realised |V - V_R1| on rest and R-6;
#  * the six order-§8 systems against humans: one structural descriptor each (Vael vs MF, with the Sagekin-Marchfolk difference as ordinary human-family
#    variation) and the region RMS vs Marchfolk on the field's own region mask (vs the SG-MF RMS on the same mask), plus Fenn / Aelari for the firewall;
#  * guard rails: trunk breadths (thorax max, waist, crest), bideltoid, thorax depth, palm / foot, joint breadths (no stocky / broad / big-joint drift).
# Descriptors (rest geometry, cm, / stature where a share): trunk side-wall half-breadth profile on trunk-weighted, arm-free vertices at three joint-defined
# levels (lower ribs = spine_03 head, waist = midway spine_01 -> spine_02, crest band = 0.30 of hip -> spine_01); palm-root breadth at 40 % of the
# wrist -> middle_01 span over the wrist breadth; heel breadth (transverse extent behind the ankle line, below the malleoli) over foot length.
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import vael_body_field as VF
OUT, CF = sys.argv[1:3]; VD = os.environ.get('VD_DIR', '/tmp/claude-0/rt/vd'); PA = os.environ.get('VA_PA', '/tmp/claude-0/rt/va/partA')
P_ = {'c1': 'VAL4-R1', 'c2': 'VALF178-R1'}[CF]; SX = {'c1': 'M', 'c2': 'F'}[CF]
SRC = {'R1': '/tmp/claude-0/rt/va2/vc2/r1/' + P_}; SRC.update({t: '%s/cand/%s-%s' % (VD, P_, t) for t in ('VD1', 'VD2', 'VD3')})
for k in ('MF', 'SG', 'FN', 'AE'): SRC[k] = '%s/cmp/%s%s178' % (PA, k, SX)
jl = lambda p: json.load(open(p))
def ld(p, s): z = np.load(p + '_%s.npz' % s); return z
REST = {k: ld(p, 'rest') for k, p in SRC.items()}; R6 = {k: ld(p, 'r6') for k, p in SRC.items()}; MEAS = {k: jl(p + '_meas.json')['combined'] for k, p in SRC.items()}
def desc(z, m):
    V = z['V'].astype(float); keep = z['keep']; J = json.loads(str(z['joints'])); w = lambda k: z['w_' + k].astype(float); H = m['stature']
    wa = sum(w(k) for k in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'fingers_l', 'fingers_r'))
    wl = sum(w(k) for k in ('thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r'))
    wt = w('spine_01') + w('spine_02') + w('spine_03') + w('pelvis'); tm = keep & (wt > 0.3) & (wa < 0.1) & (wl < 0.5)
    hz = lambda b: J[b][0][2]; hip = 0.5 * (hz('thigh_l') + hz('thigh_r'))
    def hb(u):
        s = tm & (np.abs(V[:, 2] - u) < 0.75); return float(V[s, 0].max() - V[s, 0].min()) if s.sum() > 4 else float('nan')
    rib, waist, crest = hb(hz('spine_03')), hb(0.5 * (hz('spine_01') + hz('spine_02'))), hb(hip + 0.3 * (hz('spine_01') - hip))
    d = dict(rib_breadth_share=rib / H, waist_breadth_share=waist / H, crest_band_breadth_share=crest / H, waist_over_rib=waist / rib, thorax_depth_over_rib_breadth=m['thorax_depth_max'] / rib)
    pr, hr = [], []
    for sd in ('l', 'r'):
        wr, mid, ix, pk = [np.array(J[b + sd][0]) for b in ('hand_', 'middle_01_', 'index_01_', 'pinky_01_')]
        ax = mid - wr; L = np.linalg.norm(ax); ax /= L; hv = keep & (w('hand_' + sd) > 0.5); t = ((V - wr) @ ax) / L
        s = hv & (np.abs(t - 0.40) < 0.05); Q = V[s] - wr; Q -= np.outer(Q @ ax, ax); ev, evc = np.linalg.eigh(np.cov(Q.T)); wd = evc[:, -1]
        pr.append(float((Q @ wd).max() - (Q @ wd).min()))
        an, bl = np.array(J['foot_' + sd][0]), np.array(J['ball_' + sd][0]); fa = an - bl; fa[2] = 0; Lf = np.linalg.norm(fa); fa /= Lf; mh = np.array([-fa[1], fa[0], 0])
        fv = keep & ((w('foot_' + sd) + w('ball_' + sd)) > 0.5); tf = ((V - bl) @ fa) / Lf
        s = fv & (tf > 0.85) & (V[:, 2] < an[2] - 3.0 * H / 173.14); u = V[s] @ mh; hr.append(float(u.max() - u.min()))
    MM = m['mean']
    d.update(palm_root_over_wrist=np.mean(pr) / MM['wrist_breadth'], palm_root_share=np.mean(pr) / H, heel_breadth_over_foot_length=np.mean(hr) / MM['foot_len'],
             palm_breadth_over_hand=m['ratio']['palm_breadth_over_hand'], foot_breadth_over_length=MM['foot_breadth'] / MM['foot_len'])
    return d
D = {k: desc(REST[k], MEAS[k]) for k in SRC}
# field parts on the R1 rest mesh (region masks + intended displacement)
zr = REST['R1']; W, J, keep, F = VF.npz_inputs(zr); spec = jl(VD + '/VD_definitions.json')['definition']
_, parts, info = VF.field(zr['V'], W, J, keep, F, spec, 1.0, return_parts=True)
masks = {k: (np.linalg.norm(v, axis=1) > 0.2 * np.linalg.norm(v, axis=1).max()) & keep for k, v in parts.items()}
audit = dict(field_info=info, regions={})
for t, mg in jl(VD + '/VD_definitions.json')['candidates'].items():
    dR = np.linalg.norm(REST[t]['V'].astype(float) - REST['R1']['V'].astype(float), axis=1); d6 = np.linalg.norm(R6[t]['V'].astype(float) - R6['R1']['V'].astype(float), axis=1)
    audit[t] = dict(magnitude=mg, affected_vertices_rest=int((dR > 0.01).sum()), max_cm_rest=float(dR.max()), rms_cm_rest_affected=float(np.sqrt((dR[dR > 0.01] ** 2).mean())),
                    affected_vertices_r6=int((d6 > 0.01).sum()), max_cm_r6=float(d6.max()), head_max_cm=float(dR[zr['w_head'] > 0.5].max()), ears_max_cm=float(dR[zr['w_ears'] > 0.05].max()),
                    per_region={k: dict(vertices=int(masks[k].sum()), max_cm=float(dR[masks[k]].max()), rms_cm=float(np.sqrt((dR[masks[k]] ** 2).mean()))) for k in masks})
SYS = [('1 thoracic side-wall / ribcage', 'rib', 'thorax_depth_over_rib_breadth', +1), ('2 torso-to-pelvis continuity', 'flank', 'waist_over_rib', +1),
       ('3 shoulder / clavicle integration', 'clav', None, 0), ('4 pelvis / hip silhouette', 'asis', 'crest_band_breadth_share', 0),
       ('5 wrist / hand base', 'palm', 'palm_root_over_wrist', +1), ('6 ankle / foot base', 'heel', 'heel_breadth_over_foot_length', +1)]
rms = lambda a, b, mk: float(np.sqrt((np.linalg.norm(R6[a]['V'][mk].astype(float) - R6[b]['V'][mk].astype(float), axis=1) ** 2).mean()) * 10)
sysres = {}
for name, reg, key, sg in SYS:
    mk = masks[reg]; base = rms('SG', 'MF', mk); row = dict(region=reg, region_vertices=int(mk.sum()), SG_vs_MF_rms_mm=round(base, 2), descriptor=key, direction=sg, items={})
    for t in ('R1', 'VD1', 'VD2', 'VD3', 'FN', 'AE'):
        x = dict(vs_MF_rms_mm=round(rms(t, 'MF', mk), 2)); x['rms_ratio_over_human'] = round(x['vs_MF_rms_mm'] / max(base, 1e-6), 2)
        if key:
            x['value'] = round(D[t][key], 5); x['vs_MF_pct'] = round(100 * (D[t][key] / D['MF'][key] - 1), 2)
        row['items'][t] = x
    if key: row['MF'] = round(D['MF'][key], 5); row['SG'] = round(D['SG'][key], 5); row['human_var_pct'] = round(abs(100 * (D['SG'][key] / D['MF'][key] - 1)), 2)
    sysres[name] = row
guard = {k: {t: round(v, 5) for t, v in ((t, (MEAS[t][k] if k in MEAS[t] else MEAS[t]['ratio'][k]) / (MEAS[t]['stature'] if k in MEAS[t] else 1)) for t in SRC)} for k in
         ('thorax_breadth_max', 'waist_breadth', 'iliac_crest_breadth', 'bitrochanteric_breadth', 'bideltoid_breadth', 'thorax_depth_max', 'pelvic_depth', 'shoulder_joint_breadth')}
limbs = {k: {t: round(MEAS[t]['ratio'][k], 5) for t in SRC} for k in ('elbow_over_humerus', 'wrist_over_forearm', 'knee_over_femur', 'ankle_over_shin', 'palm_breadth_over_hand', 'hand_share', 'foot_share', 'arm_share', 'leg_share')}
limbs['foot_breadth_over_length'] = {t: round(D[t]['foot_breadth_over_length'], 5) for t in SRC}
res = dict(cfg=CF, sources=SRC, field_definition_sha256=VF.spec_hash(spec), audit=audit, systems=sysres, descriptors={t: {k: round(v, 5) for k, v in D[t].items()} for t in SRC},
           guard_rails_over_stature=guard, limb_gracility=limbs)
json.dump(res, open(OUT, 'w'), indent=1)
for name, row in sysres.items():
    print(CF, '%-34s' % name, 'SG-MF %.2f mm' % row['SG_vs_MF_rms_mm'], ' '.join('%s %.2f%s' % (t, x['vs_MF_rms_mm'], (' (%+.1f%%)' % x['vs_MF_pct']) if 'vs_MF_pct' in x else '') for t, x in row['items'].items()), '| human var %s' % row.get('human_var_pct'))
for t in ('VD1', 'VD2', 'VD3'): print(CF, t, {k: v for k, v in audit[t].items() if k != 'per_region'})
