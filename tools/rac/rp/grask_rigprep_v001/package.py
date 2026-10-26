# package.py ADJ_RAW.json OUTDIR REV : versioned diagnostic landmark package GR_U_REF_RP2_rigprep_landmarks_<REV>.json + tables + validation
import sys, os, json, csv, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import T_PROD, to_blender_pt, to_blender_vec, rot
RAW = json.load(open(sys.argv[1])); OUT = sys.argv[2]; REV = sys.argv[3]; R = RAW['R']; A = np.asarray
UP, FWD, LEFT = A([0, 0, 1.0]), A([0, 1.0, 0]), A([1.0, 0, 0])
P = {k: A(v['p'], float) for k, v in R.items()}
PAR = {'pelvis': 'root', 'spine_01': 'pelvis', 'spine_02': 'spine_01', 'spine_03': 'spine_02', 'thoracic_01': 'spine_03', 'thoracic_02': 'thoracic_01',
       'thoracic_03': 'thoracic_02', 'neck_base': 'thoracic_03', 'head_pivot': 'neck_base', 'crown': 'head_pivot', 'chin': 'head_pivot'}
CHILD = {'root': 'pelvis', 'pelvis': 'spine_01', 'spine_01': 'spine_02', 'spine_02': 'spine_03', 'spine_03': 'thoracic_01', 'thoracic_01': 'thoracic_02',
         'thoracic_02': 'thoracic_03', 'thoracic_03': 'neck_base', 'neck_base': 'head_pivot', 'head_pivot': 'crown'}
for s in 'lr':
    PAR.update({'hip_' + s: 'pelvis', 'knee_' + s: 'hip_' + s, 'ankle_' + s: 'knee_' + s, 'ball_' + s: 'ankle_' + s, 'sternoclavicular_' + s: 'thoracic_03',
                'glenohumeral_' + s: 'sternoclavicular_' + s, 'elbow_' + s: 'glenohumeral_' + s, 'wrist_' + s: 'elbow_' + s, 'scapula_medial_proxy_' + s: 'sternoclavicular_' + s,
                'eye_' + s: 'head_pivot', 'acromion_' + s: 'sternoclavicular_' + s, 'scapular_inferior_proxy_' + s: 'sternoclavicular_' + s})
    CHILD.update({'hip_' + s: 'knee_' + s, 'knee_' + s: 'ankle_' + s, 'ankle_' + s: 'ball_' + s, 'sternoclavicular_' + s: 'glenohumeral_' + s,
                  'glenohumeral_' + s: 'elbow_' + s, 'elbow_' + s: 'wrist_' + s, 'wrist_' + s: 'middle_mcp_' + s, 'scapula_medial_proxy_' + s: 'acromion_' + s})
    for f in ('index', 'middle', 'ring', 'pinky'):
        PAR.update({'%s_mcp_%s' % (f, s): 'wrist_' + s, '%s_pip_%s' % (f, s): '%s_mcp_%s' % (f, s), '%s_dip_%s' % (f, s): '%s_pip_%s' % (f, s), '%s_tip_%s' % (f, s): '%s_dip_%s' % (f, s)})
    PAR.update({'thumb_cmc_' + s: 'wrist_' + s, 'thumb_mcp_' + s: 'thumb_cmc_' + s, 'thumb_ip_' + s: 'thumb_mcp_' + s, 'thumb_tip_' + s: 'thumb_ip_' + s,
                'hallux_mtp_' + s: 'ankle_' + s, 'hallux_ip_' + s: 'hallux_mtp_' + s, 'hallux_tip_' + s: 'hallux_ip_' + s})
    for t in ('toe2', 'toe3', 'toe4', 'toe5'):
        PAR.update({'%s_mtp_%s' % (t, s): 'ankle_' + s, '%s_pip_%s' % (t, s): '%s_mtp_%s' % (t, s), '%s_dip_%s' % (t, s): '%s_pip_%s' % (t, s), '%s_tip_%s' % (t, s): '%s_dip_%s' % (t, s)})
for k, p in PAR.items():
    if k in CHILD: continue
for k in list(PAR):
    if any(k.startswith(x) for x in ('index', 'middle', 'ring', 'pinky', 'thumb', 'hallux', 'toe')) and not k.split('_')[1] == 'tip':
        nxt = [c for c, pp in PAR.items() if pp == k]
        if nxt: CHILD[k] = nxt[0]
FLEX = {'hip': (FWD, 'hip flexion: knee moves anterior'), 'knee': (-FWD, 'knee flexion: ankle moves posterior'), 'ankle': (UP, 'ankle dorsiflexion: ball moves up'),
        'glenohumeral': (FWD, 'shoulder flexion: elbow moves anterior'), 'elbow': (FWD, 'elbow flexion: wrist moves anterior')}
def frame(k):
    r = R[k]; base = k[:-2] if k[-2:] in ('_l', '_r') else k
    if r.get('v001_frame') and 'blender_columns_XYZ' in r['v001_frame']:
        f = dict(r['v001_frame']); f['source'] = 'v001 construction frame (unchanged)'; return f
    if k not in CHILD or CHILD[k] not in P: return None
    y = P[CHILD[k]] - P[k]; y /= np.linalg.norm(y)
    x = A(r['flex_axis']) if 'flex_axis' in r else LEFT.copy()
    if base in FLEX: fd, fn = FLEX[base]
    elif base in ('pelvis', 'spine_01', 'spine_02', 'spine_03', 'thoracic_01', 'thoracic_02', 'thoracic_03', 'neck_base', 'head_pivot'): fd, fn = FWD, 'trunk/neck flexion: child moves anterior'
    else: fd, fn = None, None
    xb, yb = to_blender_vec(x), to_blender_vec(y); yb /= np.linalg.norm(yb); xb = xb - (xb @ yb) * yb; xb /= np.linalg.norm(xb); zb = np.cross(xb, yb)
    Mb = np.stack([xb, yb, zb], 1); an = Mb * A([1, -1, 1])[:, None]
    out = dict(blender_columns_XYZ=Mb.T.tolist(), blender_det=float(np.linalg.det(Mb)), analysis_columns_XYZ=an.T.tolist(), analysis_det=float(np.linalg.det(an)),
               convention='AD-R10 diagnostic convention: right-handed in Blender; X = flexion axis toward subject-left (+X) both sides; Y = toward child; Z = X x Y',
               source='v002 adjudicated')
    if fd is not None and base not in ('sternoclavicular', 'scapula_medial_proxy', 'root'):
        y2 = rot(xb, np.radians(10)) @ yb; sg = np.sign((y2 - yb) @ to_blender_vec(fd))
        out['flexion'] = '%s rotation about local +X (Blender, right-hand rule) — %s' % ('positive' if sg > 0 else 'negative', fn)
    else: out['flexion'] = 'not defined (girdle / root / control)'
    return out
J = {}
for k, r in R.items():
    pp = P[k] + T_PROD; par = PAR.get(k)
    J[k] = dict(id=k, side=r['side'], provenance_class=r['provenance_class'], suitability=r['suitability'],
                position_source_frame_cm=P[k].round(4).tolist(), position_production_cm=pp.round(4).tolist(), position_blender_m=to_blender_pt(pp).round(6).tolist(),
                parent=par, children=[c for c, q in PAR.items() if q == k], segment_from_parent_cm=None if par not in P else round(float(np.linalg.norm(P[k] - P[par])), 3),
                frame=frame(k), construction_rule=r['construction_rule'], uncertainty_limitation=r['limitation'],
                inside_v005=r['inside_v005'], depth_v005_cm=round(r['depth_v005_cm'], 3), inside_v003=r['inside_v003'], depth_v003_cm=round(r['depth_v003_cm'], 3),
                **{a: b for a, b in r.items() if a in ('adjustment_cm', 'adjustment_reason', 'acromion_to_gh_cm', 'acromion_vertical_drop_cm', 'surface_anchor', 'inward_direction',
                                                        'inward_cm', 'through_thickness_cm', 'clip_half_width_cm', 'frozen_label', 'gh_rule')})
# ------------------------------------------------------------------ validation against the order
V = []
def chk(name, ok, detail): V.append(dict(check=name, ok=bool(ok), detail=detail))
v1 = json.load(open('/tmp/claude-0/rt/rpr/out/GR_U_REF_RP2_rigprep_landmarks_v001.json'))['joints']; P1 = lambda k: A(v1[k]['position_source_frame_cm'])
for s in 'lr':
    chk('AD-R1 hip_%s within 5 mm of the v001 consensus' % s, np.linalg.norm(P['hip_' + s] - P1('hip_' + s)) <= 0.5001, '%.3f cm' % np.linalg.norm(P['hip_' + s] - P1('hip_' + s)))
    chk('AD-R2 knee_%s level = v001 consensus level (±5 mm)' % s, abs(P['knee_' + s][2] - P1('knee_' + s)[2]) <= 0.5, 'dz %.3f cm' % (P['knee_' + s][2] - P1('knee_' + s)[2]))
    chk('AD-R2 ankle_%s level = v001 consensus level' % s, abs(P['ankle_' + s][2] - P1('ankle_' + s)[2]) <= 0.01, 'z %.2f' % P['ankle_' + s][2])
    g = R['glenohumeral_' + s]
    chk('AD-R3 GH_%s 3.5-4.5 cm inferior to the acromion, on the extrapolated shaft line, internal' % s, 3.5 <= g['acromion_vertical_drop_cm'] <= 4.5 and g['inside_v005'] and g['gh_rule']['rule_satisfied'],
        'drop %.1f cm, 3-D %.2f cm, depth %.2f cm' % (g['acromion_vertical_drop_cm'], g['acromion_to_gh_cm'], g['depth_v005_cm']))
    chk('AD-R4 elbow_%s within 5 mm of the v001 cubital target' % s, np.linalg.norm(P['elbow_' + s] - P1('elbow_' + s)) <= 0.5001, '%.3f cm' % np.linalg.norm(P['elbow_' + s] - P1('elbow_' + s)))
    sc = R['sternoclavicular_' + s]
    chk('AD-R5 SC_%s 3.0 cm posterior of the surface anchor, inside' % s, abs(sc['inward_cm'] - 3.0) < 1e-6 and sc['inside_v005'], 'inward %.2f cm, depth %.2f' % (sc['inward_cm'], sc['depth_v005_cm']))
    chk('AD-R9 scapula_medial_proxy_%s on the posterior surface' % s, R['scapula_medial_proxy_' + s]['depth_v005_cm'] < 0.01, 'surface dist %.4f cm' % R['scapula_medial_proxy_' + s]['depth_v005_cm'])
    chk('AD-R8 eye_%s non-deforming only; jaw deferred' % s, 'NON-DEFORMING' in R['eye_' + s]['suitability'] and 'DEFERRED' in R['jaw_hinge_' + s]['suitability'], '')
    chk('AD-R11 jaw_hinge_%s provenance corrected' % s, 'placeholder' in R['jaw_hinge_' + s]['provenance_class'], R['jaw_hinge_' + s]['provenance_class'])
z3, zn = P['spine_03'][2], P['neck_base'][2]
for i, fr in enumerate((0.25, 0.5, 0.75)):
    chk('AD-R6 thoracic_%02d at %d%% of the interval' % (i + 1, fr * 100), abs(P['thoracic_%02d' % (i + 1)][2] - (z3 + fr * (zn - z3))) < 1e-6, 'z %.3f' % P['thoracic_%02d' % (i + 1)][2])
FZJ = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/production/GR_U_REF_RP2_retopo_v003_landmarks.json'))['landmarks']
chk('AD-R6 spine_01..03 identical to the frozen records', all(np.allclose(P[k], FZJ[k]['source_frame_cm']) for k in ('spine_01', 'spine_02', 'spine_03')), '')
chk('AD-R7 root at the production origin', np.allclose(P['root'] + T_PROD, 0), '')
chk('AD-R7 pelvis within 5 mm of the v001 proposal', np.linalg.norm(P['pelvis'] - P1('pelvis_root')) <= 0.5001, '%.3f cm' % np.linalg.norm(P['pelvis'] - P1('pelvis_root')))
chk('AD-R10 all frames right-handed in Blender', all(abs(j['frame']['blender_det'] - 1) < 1e-6 for j in J.values() if j['frame'] and 'blender_det' in j['frame']), '')
chk('no L/R mirroring (asymmetric x-sum of hips / GH)', abs(P['hip_l'][0] + P['hip_r'][0]) > 1e-3 and abs(P['glenohumeral_l'][0] + P['glenohumeral_r'][0]) > 1e-3,
    'hip x-sum %.3f, GH x-sum %.3f' % (P['hip_l'][0] + P['hip_r'][0], P['glenohumeral_l'][0] + P['glenohumeral_r'][0]))
rig_int = [k for k in J if J[k]['provenance_class'].startswith('manual-author-rig') and k != 'root' and not k.startswith('scapula')]
chk('every manual rig centre inside v005 and v003', all(J[k]['inside_v005'] and J[k]['inside_v003'] for k in rig_int), ', '.join(k for k in rig_int if not (J[k]['inside_v005'] and J[k]['inside_v003'])))
doc = dict(meta=dict(file='GR_U_REF_RP2_rigprep_landmarks_%s.json' % REV, status='AUTHOR-ADJUDICATED DIAGNOSTIC LANDMARK PACKAGE (diagnostic rig only; not a final skeleton; frozen package unchanged)',
                     order='reviews/chatgpt-rac-rp2-grask-rig-landmark-adjudication-and-diagnostic-rig-order.md (bf7d664)', parent_proposal='GR_U_REF_RP2_rigprep_landmarks_v001.json (2558dc0)',
                     frames='production cm = source + (%.5f, %.5f, 0); Blender m = (x, -f, u)/100; analysis frame left-handed, Blender frames right-handed' % tuple(T_PROD[:2]),
                     classes=['frozen surface marker / proxy', 'copied construction coordinate (surface-validated)', 'manual-author-rig (centre)', 'manual-author-rig-proxy', 'deferred facial placeholder', 'rig control'],
                     log=RAW['LOG']), joints=J, validation=V)
json.dump(doc, open(os.path.join(OUT, 'GR_U_REF_RP2_rigprep_landmarks_%s.json' % REV), 'w'), indent=1)
# tables
vec = lambda v, n=2: '(' + ', '.join('%.*f' % (n, x) for x in v) + ')'
L = ['# GR_U_REF_RP2_rigprep_landmarks_%s — readable tables' % REV, '', 'Author-adjudicated diagnostic landmark package. The frozen v003 landmark package is unchanged. Production cm: x = subject left, f = forward, u = up.', '',
     '## Validation against the order', '', '| check | result | detail |', '|---|---|---|'] + ['| %s | %s | %s |' % (v['check'], 'PASS' if v['ok'] else '**FAIL**', v['detail']) for v in V]
L += ['', '## Records', '', '| id | provenance | suitability | production cm | Blender m | parent | length cm | depth v005 cm | rule / limitation |', '|---|---|---|---|---|---|---|---|---|']
for k, j in J.items():
    L.append('| %s | %s | %s | %s | %s | %s | %s | %.2f | %s — %s |' % (k, j['provenance_class'], j['suitability'], vec(j['position_production_cm']), vec(j['position_blender_m'], 4), j['parent'] or '—',
             '—' if j['segment_from_parent_cm'] is None else '%.2f' % j['segment_from_parent_cm'], j['depth_v005_cm'], j['construction_rule'], j['uncertainty_limitation']))
L += ['', '## Frames (Blender, right-handed)', '', '| id | X | Y | Z | flexion |', '|---|---|---|---|---|']
for k, j in J.items():
    f = j['frame']
    if f and 'blender_columns_XYZ' in f: L.append('| %s | %s | %s | %s | %s |' % (k, vec(f['blender_columns_XYZ'][0], 3), vec(f['blender_columns_XYZ'][1], 3), vec(f['blender_columns_XYZ'][2], 3), f.get('flexion', '')))
open(os.path.join(OUT, 'GR_U_REF_RP2_rigprep_landmarks_%s_tables.md' % REV), 'w').write('\n'.join(L) + '\n')
with open(os.path.join(OUT, 'GR_U_REF_RP2_rigprep_landmarks_%s.csv' % REV), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['id', 'side', 'provenance', 'suitability', 'x_cm', 'f_cm', 'u_cm', 'X_m', 'Y_m', 'Z_m', 'src_x', 'src_f', 'src_u', 'parent', 'length_cm', 'depth_v005_cm', 'rule', 'limitation'])
    for k, j in J.items(): w.writerow([k, j['side'], j['provenance_class'], j['suitability'], *j['position_production_cm'], *j['position_blender_m'], *j['position_source_frame_cm'], j['parent'], j['segment_from_parent_cm'], j['depth_v005_cm'], j['construction_rule'], j['uncertainty_limitation']])
print('records', len(J), 'validation', sum(v['ok'] for v in V), '/', len(V)); [print('FAIL', v) for v in V if not v['ok']]
