# compose.py FIT_V005.json FIT_V003.json OUTDIR : build the separate, versioned Grask rig-prep landmark/axis PROPOSAL
# (GR_U_REF_RP2_rigprep_landmarks_v001.json) + readable tables. Never touches the frozen landmark package.
import sys, os, json, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import T_PROD, to_prod, to_blender_pt, to_blender_vec, rot, load

F5, F3, OUT = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
os.makedirs(OUT, exist_ok=True)
FROZEN_PATH = ('/home/claude/wayfarer-design/reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/production/'
               'GR_U_REF_RP2_retopo_v003_landmarks.json')
FROZEN = json.load(open(FROZEN_PATH))['landmarks']
FZ = lambda k: np.array(FROZEN[k]['source_frame_cm'], float)
A_ = lambda v: np.array(v, float)
M5 = load('/tmp/claude-0/src3d/v5/v005.npz')
SIDES = (('l', 1), ('r', -1))

# ------------------------------------------------------------------ 1. provenance audit of the frozen package (74 records)
def prov_class(k, v):
    if k.startswith('jaw_hinge'): return 'rule-based estimate (heuristic offset from the ear root; mislabelled "construction coordinate (copied)" in the frozen package)'
    if v['method'] == 'manual': return 'copied construction coordinate'
    if v['method'] == 'surface-fit': return 'independently measured surface landmark'
    if v['method'] == 'prior-seed+surface-fit': return 'fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids)'
    return 'unclassified'
audit = []
for k, v in FROZEN.items():
    audit.append(dict(id=k, method=v['method'], frozen_evidence=v.get('evidence', ''), provenance=prov_class(k, v),
                      t6_drift_mm=v.get('drift_mm'), counts_as_independent_measurement=(v['method'] != 'manual' and not k.startswith('jaw_hinge'))))
pc = {}
for a in audit: pc[a['provenance']] = pc.get(a['provenance'], 0) + 1

# ------------------------------------------------------------------ helpers
pts_depth = {}
def depth(p):
    key = tuple(np.round(p, 5))
    if key not in pts_depth:
        cp, d, _ = M5.nearest.on_surface(np.array([p])); pts_depth[key] = (bool(M5.contains(np.array([p]))[0]), float(d[0]))
    return pts_depth[key]
def consensus(alts):
    P = np.array([a for a in alts.values()]); c = np.median(P, 0) if len(P) >= 3 else P.mean(0)
    return c, float(max(np.linalg.norm(P - c, axis=1)))
J = {}                                                                   # proposal joints (source frame)
def add(jid, side, p, cls, method, alts=None, unc=None, status=None, note=None, cross=None):
    ins, dd = depth(p)
    if unc is None and alts: unc = float(max(np.linalg.norm(A_(a) - p) for a in alts.values()))
    if status is None: status = 'usable (diagnostic)' if (unc is not None and unc <= 1.0) else 'provisional'
    J[jid] = dict(id=jid, side=side, class_=cls, p_src=A_(p), method=method, alts={k: A_(v) for k, v in (alts or {}).items()},
                  uncertainty_cm=unc, status=status, note=note, inside_v005=ins, depth_to_v005_surface_cm=dd, cross=cross)

def v3_consensus(key, letters, frozen):
    alts = {L: A_(F3[key][L]) for L in letters if L in F3[key]}; alts['C_frozen'] = frozen
    return consensus(alts)[0]

# ------------------------------------------------------------------ 2. proposals
for s, sg in SIDES:
    for jn, letters in (('hip', 'A'), ('knee', 'AB'), ('ankle', 'AB'), ('glenohumeral', 'AB'), ('elbow', 'AB')):
        key = '%s_%s' % (jn, s); r = F5[key]
        alts = {('%s: %s' % (L, r[L + '_method'])): A_(r[L]) for L in letters}; alts['C: frozen v003 package value (MPFB/E3-seeded)'] = FZ(key)
        c, unc = consensus(alts); c3 = v3_consensus(key, letters, FZ(key))
        add(key, s, c, 'fitted joint-centre estimate', 'consensus (coordinate median) of the independent surface definitions A, B and the frozen value C',
            alts, unc, note=r.get('note'), cross=float(np.linalg.norm(c3 - c)))
    # wrist: construction origin, surface-validated; forearm waist reported as a reference only
    r = F5['wrist_' + s]; W = A_(r['A'])
    sc_off = None
    add('wrist_' + s, s, W, 'copied construction coordinate (surface-validated)', 'v005 hand-construction frame origin',
        {'B (reference only, not an alternative): forearm waist %.1f cm proximal' % r['B_offset_proximal_cm']: A_(r['B'])},
        unc=None, status='usable (construction)', note='ML/AP placement validated by the forearm/hand section; longitudinal placement is construction-defined (the forearm waist lies %.1f cm proximal)' % r['B_offset_proximal_cm'], cross=0.0)
    J['wrist_' + s]['uncertainty_cm'] = None
    # SC: frozen (deep) vs anterior surface summit; depth unresolved
    r = F5['sternoclavicular_' + s]
    alts = {'A: anterior surface summit beside the jugular notch (skin point)': A_(r['surface_point']), 'C: frozen v003 package value (MPFB/E3-seeded)': FZ('sternoclavicular_' + s)}
    c, unc = consensus(alts)
    add('sternoclavicular_' + s, s, c, 'fitted joint-centre estimate', 'midpoint of the skin summit and the frozen value (joint depth unresolved)', alts, unc,
        note='frozen value is %.1f cm behind the anterior skin summit; the joint depth is not expressed by the source surface' % (r['surface_point'][1] - FZ('sternoclavicular_' + s)[1]),
        cross=float(np.linalg.norm(A_(F3['sternoclavicular_' + s]['surface_point']) - A_(r['surface_point'])) / 2))
    # carried surface markers
    for k in ('acromion_', 'scapular_inferior_proxy_', 'ear_root_', 'ear_tip_', 'mouth_corner_'):
        add(k + s, s, FZ(k + s), 'independently measured surface landmark (carried from the frozen package)', FROZEN[k + s].get('note', ''),
            status='usable (surface marker)' if k != 'scapular_inferior_proxy_' else 'provisional (surface proxy only)', unc=None, cross=FROZEN[k + s]['drift_mm'] / 10)
    add('jaw_hinge_' + s, s, FZ('jaw_hinge_' + s), 'rule-based estimate (heuristic)', FROZEN['jaw_hinge_' + s]['note'], status='provisional (no jaw anatomy)', unc=None,
        note='the source has a closed sculpted mouth and no mandible/oral cavity; the hinge is an offset rule, not a fit')
    # eyes
    r = F5['eye_' + s]
    alts = {'A: v003 eyeball-volume centre (construction)': A_(r['A']), 'B: sphere on the anterior eye surface (r=%.2f cm, rms %.2f mm)' % (r['B_r_cm'], 10 * r['B_rms_cm']): A_(r['B'])}
    add('eye_' + s, s, A_(r['A']), 'copied construction coordinate (surface-validated)', 'v003 eyeball-volume centre; validated by an independent sphere fit', alts,
        status='usable (construction)', note='eyes are sculpted surface on the single body mesh: there is no separate eyeball object', cross=float(np.linalg.norm(A_(F3['eye_' + s]['B']) - A_(r['B']))))
    # hands / feet construction chains
    for k, v in F5.items():
        if not k.startswith('cx_') or not k.endswith('_' + s): continue
        jid = k[3:]; off = v.get('section_offset_cm')
        add(jid, s, A_(v['p']), 'copied construction coordinate (surface-validated)', 'exact v005 extremity-construction joint' if not jid.split('_')[1] == 'tip' else 'v005 construction distal-phalanx end',
            unc=off, status='usable (construction)', cross=0.0,
            note=('digit-section centroid offset %.2f cm' % off if off is not None else 'inside the palm/forefoot mass; %.2f cm deep' % v['surface_dist_cm']) +
                 ('; surface tip %.2f cm beyond' % v['tip_to_surface_tip_cm'] if 'tip_to_surface_tip_cm' in v else ''))
        J[jid]['axis_long'] = A_(v['axis_long']); J[jid]['axis_flex'] = A_(v['axis_flex']); J[jid]['dorsal'] = A_(v['dorsal'])
        if 'surface_tip' in v: J[jid]['surface_tip_src'] = A_(v['surface_tip'])
# pelvis root
hipmid = 0.5 * (J['hip_l']['p_src'] + J['hip_r']['p_src'])
alts = {'A: midpoint of the proposed hip centres': hipmid, 'B: torso section centroid at the frozen pelvis-root height': A_(F5['axial_pelvis_root']['section_centroid']),
        'C: frozen v003 package value (defines the production origin)': FZ('pelvis_root')}
c, unc = consensus(alts)
add('pelvis_root', 'c', c, 'fitted joint-centre estimate', 'consensus of A, B, C', alts, unc,
    note='the production origin stays the frozen pelvis_root projection (contract §3); a different rig root would be an offset, not a re-origin',
    cross=float(np.linalg.norm(0.5 * (v3_consensus('hip_l', 'A', FZ('hip_l')) + v3_consensus('hip_r', 'A', FZ('hip_r'))) - hipmid)))
for k in ('spine_01', 'spine_02', 'spine_03', 'neck_base'):
    r = F5['axial_' + k]
    alts = {'A: torso section centroid at the station height': A_(r['section_centroid']), 'C: frozen v003 package value (MPFB/E3-seeded)': FZ(k)}
    c, unc = consensus(alts)
    add(k, 'c', c, 'fitted joint-centre estimate', 'midpoint of the section centroid and the frozen value (station heights carried from the frozen package)', alts, unc,
        note='no vertebral anatomy in the source; back skin at f=%.1f, front at f=%.1f (source frame)' % (r['back_surface_f'], r['front_surface_f']),
        cross=float(np.linalg.norm(A_(F3['axial_' + k]['section_centroid']) - A_(r['section_centroid'])) / 2))
alts = {'A: neck/head section centroid at the mean ear-root height': A_(F5['head_pivot_alt']['p']), 'C: frozen v003 package value (MPFB/E3-seeded)': FZ('head_pivot')}
c, unc = consensus(alts)
add('head_pivot', 'c', c, 'fitted joint-centre estimate', 'midpoint of A and C', alts, unc, note='atlanto-occipital pivot; internal, no skull anatomy',
    cross=float(np.linalg.norm(A_(F3['head_pivot_alt']['p']) - A_(F5['head_pivot_alt']['p'])) / 2))
for k in ('crown', 'chin'):
    add(k, 'c', FZ(k), 'independently measured surface landmark (carried from the frozen package)', FROZEN[k]['note'], status='usable (surface marker)',
        unc=None, cross=FROZEN[k]['drift_mm'] / 10)
for s, sg in SIDES:                                                    # ball (MTP) line midpoint, construction-derived
    p = 0.5 * (J['hallux_mtp_' + s]['p_src'] + J['toe5_mtp_' + s]['p_src'])
    add('ball_' + s, s, p, 'derived from copied construction coordinates', 'midpoint of the hallux and fifth MTP construction joints (MTP line)', status='usable (construction)', unc=None, cross=0.0)

# ------------------------------------------------------------------ 3. hierarchy, segment lengths, frames
PAR = {'spine_01': 'pelvis_root', 'spine_02': 'spine_01', 'spine_03': 'spine_02', 'neck_base': 'spine_03', 'head_pivot': 'neck_base', 'crown': 'head_pivot', 'chin': 'head_pivot'}
FLEX_DIR = {}   # analysis-frame direction the child moves in "flexion" (definition used for the sign; technical, not ROM canon)
for s, sg in SIDES:
    PAR.update({'hip_' + s: 'pelvis_root', 'knee_' + s: 'hip_' + s, 'ankle_' + s: 'knee_' + s, 'ball_' + s: 'ankle_' + s,
                'sternoclavicular_' + s: 'spine_03', 'glenohumeral_' + s: 'sternoclavicular_' + s, 'elbow_' + s: 'glenohumeral_' + s,
                'wrist_' + s: 'elbow_' + s, 'eye_' + s: 'head_pivot', 'jaw_hinge_' + s: 'head_pivot'})
    for f in ('index', 'middle', 'ring', 'pinky'):
        PAR.update({'%s_mcp_%s' % (f, s): 'wrist_' + s, '%s_pip_%s' % (f, s): '%s_mcp_%s' % (f, s), '%s_dip_%s' % (f, s): '%s_pip_%s' % (f, s), '%s_tip_%s' % (f, s): '%s_dip_%s' % (f, s)})
    PAR.update({'thumb_cmc_' + s: 'wrist_' + s, 'thumb_mcp_' + s: 'thumb_cmc_' + s, 'thumb_ip_' + s: 'thumb_mcp_' + s, 'thumb_tip_' + s: 'thumb_ip_' + s})
    PAR.update({'hallux_mtp_' + s: 'ankle_' + s, 'hallux_ip_' + s: 'hallux_mtp_' + s, 'hallux_tip_' + s: 'hallux_ip_' + s})
    for t in ('toe2', 'toe3', 'toe4', 'toe5'):
        PAR.update({'%s_mtp_%s' % (t, s): 'ankle_' + s, '%s_pip_%s' % (t, s): '%s_mtp_%s' % (t, s), '%s_dip_%s' % (t, s): '%s_pip_%s' % (t, s), '%s_tip_%s' % (t, s): '%s_dip_%s' % (t, s)})
CHILD = {'pelvis_root': 'spine_01', 'spine_01': 'spine_02', 'spine_02': 'spine_03', 'spine_03': 'neck_base', 'neck_base': 'head_pivot', 'head_pivot': 'crown'}
for s, sg in SIDES:
    CHILD.update({'hip_' + s: 'knee_' + s, 'knee_' + s: 'ankle_' + s, 'ankle_' + s: 'ball_' + s, 'sternoclavicular_' + s: 'glenohumeral_' + s,
                  'glenohumeral_' + s: 'elbow_' + s, 'elbow_' + s: 'wrist_' + s, 'wrist_' + s: 'middle_mcp_' + s, 'jaw_hinge_' + s: 'chin'})
    for f in ('index', 'middle', 'ring', 'pinky'):
        CHILD.update({'%s_mcp_%s' % (f, s): '%s_pip_%s' % (f, s), '%s_pip_%s' % (f, s): '%s_dip_%s' % (f, s), '%s_dip_%s' % (f, s): '%s_tip_%s' % (f, s)})
    CHILD.update({'thumb_cmc_' + s: 'thumb_mcp_' + s, 'thumb_mcp_' + s: 'thumb_ip_' + s, 'thumb_ip_' + s: 'thumb_tip_' + s,
                  'hallux_mtp_' + s: 'hallux_ip_' + s, 'hallux_ip_' + s: 'hallux_tip_' + s})
    for t in ('toe2', 'toe3', 'toe4', 'toe5'):
        CHILD.update({'%s_mtp_%s' % (t, s): '%s_pip_%s' % (t, s), '%s_pip_%s' % (t, s): '%s_dip_%s' % (t, s), '%s_dip_%s' % (t, s): '%s_tip_%s' % (t, s)})
UP, FWD, LEFT = A_([0, 0, 1.0]), A_([0, 1.0, 0]), A_([1.0, 0, 0])
def flex_def(jid):
    n = jid.rsplit('_', 1)[0] if jid[-2:] in ('_l', '_r') else jid
    if n in ('knee',): return -FWD, 'knee flexion: ankle moves posterior'
    if n in ('hip',): return FWD, 'hip flexion: knee moves anterior'
    if n in ('ankle',): return UP, 'ankle dorsiflexion: ball moves up'
    if n in ('glenohumeral',): return FWD, 'shoulder flexion: elbow moves anterior'
    if n in ('elbow',): return FWD, 'elbow flexion: wrist moves anterior'
    if n in ('pelvis_root', 'spine_01', 'spine_02', 'spine_03', 'neck_base', 'head_pivot'): return FWD, 'trunk/neck flexion: child moves anterior'
    return None, None
def frame_for(jid):
    """right-handed BLENDER-frame triad (columns X=flexion axis, Y=longitudinal to child, Z=X x Y) + the same vectors in the analysis frame"""
    j = J[jid]
    if 'axis_long' in j and jid.split('_')[1] != 'tip' and jid not in ('ball_l', 'ball_r'):
        y = j['axis_long']; x = j['axis_flex'] * (1 if j['axis_flex'] @ LEFT >= 0 else -1); fd = -j['dorsal']; fdn = 'digit flexion: child moves palmar/plantar'
    elif jid.startswith('wrist_'):
        Mh = A_(F5[jid]['hand_frame']); y = Mh[:, 0]; x = Mh[:, 1] * (1 if Mh[:, 1] @ LEFT >= 0 else -1); fd = -Mh[:, 2]; fdn = 'wrist flexion: hand moves palmar'
    elif jid in CHILD and CHILD[jid] in J:
        y = J[CHILD[jid]]['p_src'] - j['p_src']; y = y / np.linalg.norm(y)
        if jid.startswith('elbow_'):
            b = A_(F5[jid]['flex_axis_from_bend']); x = b * (1 if b @ LEFT >= 0 else -1)
        else: x = LEFT.copy()
        fd, fdn = flex_def(jid)
    else: return None
    xb = to_blender_vec(x); yb = to_blender_vec(y); yb /= np.linalg.norm(yb); xb = xb - (xb @ yb) * yb; xb /= np.linalg.norm(xb); zb = np.cross(xb, yb)
    Mb = np.stack([xb, yb, zb], 1)
    out = dict(blender_columns_XYZ=Mb.T.tolist(), blender_det=float(np.linalg.det(Mb)),
               analysis_columns_XYZ=np.stack([Mb[:, i] * A_([1, -1, 1]) for i in range(3)], 0).tolist(),
               analysis_det=float(np.linalg.det(np.stack([Mb[:, i] * A_([1, -1, 1]) for i in range(3)], 1))),
               convention='X = flexion axis (oriented toward subject-left, +X Blender, on both sides), Y = longitudinal toward the child, Z = X x Y; right-handed in Blender')
    if jid.startswith('sternoclavicular_') or jid.startswith('jaw_') or jid.startswith('eye_'):
        out['flexion'] = 'not defined in this proposal (girdle/jaw/eye axes deferred)'
    elif fd is not None:
        y2 = rot(xb, np.radians(10)) @ yb; sgn = np.sign((y2 - yb) @ to_blender_vec(fd))
        out['flexion'] = '%s rotation about local +X (right-hand rule, Blender frame) — %s' % ('positive' if sgn > 0 else 'negative', fdn)
    return out
SEG = []
for jid, j in J.items():
    p = PAR.get(jid)
    j['parent'] = p
    if p in J:
        Ls = float(np.linalg.norm(j['p_src'] - J[p]['p_src'])); j['segment_from_parent_cm'] = Ls; SEG.append((p, jid, Ls))
    j['frame'] = frame_for(jid)

# ------------------------------------------------------------------ 4. write JSON
def ser(j):
    p = j['p_src']; pp = to_prod(p)
    d = dict(id=j['id'], side=j['side'], provenance_class=j['class_'], status=j['status'],
             position_production_cm=pp.round(4).tolist(), position_blender_m=to_blender_pt(pp).round(6).tolist(), position_source_frame_cm=p.round(4).tolist(),
             method=j['method'], uncertainty_cm=None if j['uncertainty_cm'] is None else round(j['uncertainty_cm'], 3),
             alternatives_production_cm={k: to_prod(v).round(3).tolist() for k, v in j['alts'].items()},
             alternative_distance_cm={k: round(float(np.linalg.norm(v - p)), 3) for k, v in j['alts'].items()},
             inside_v005=j['inside_v005'], depth_to_v005_surface_cm=round(j['depth_to_v005_surface_cm'], 3),
             v003_crosscheck_delta_cm=None if j['cross'] is None else round(j['cross'], 3),
             parent=j.get('parent'), segment_from_parent_cm=None if 'segment_from_parent_cm' not in j else round(j['segment_from_parent_cm'], 3),
             frame=j['frame'], note=j['note'])
    if 'surface_tip_src' in j: d['surface_tip_production_cm'] = to_prod(j['surface_tip_src']).round(3).tolist()
    return d
asym = []
for jid in J:
    if jid.endswith('_l') and jid[:-2] + '_r' in J:
        a, b = J[jid]['p_src'], J[jid[:-2] + '_r']['p_src']; asym.append((jid[:-2], float(a[0] + b[0]), float(a[1] - b[1]), float(a[2] - b[2])))
doc = dict(meta=dict(
    file='GR_U_REF_RP2_rigprep_landmarks_v001.json', status='PROPOSAL — awaiting ChatGPT review; not a skeleton, not a replacement for the frozen landmarks',
    order='reviews/chatgpt-rac-rp2-grask-rigprep-readiness-and-landmark-review-order.md (c6db89c)',
    parents=dict(production='GR_U_REF_RP2_retopo_v003.blend sha256 03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0 geometry f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f',
                 source='GR_U_REF_RP2_SOURCE_3D_v005.blend sha256 7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14 geometry 2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc',
                 frozen_landmarks='GR_U_REF_RP2_retopo_v003_landmarks.json sha256 aafbe617260dfa67632f7fe9abe495fcbf5cacd39584ab31ae8a1ead6ec8ff09 (unchanged; this file does not replace it)'),
    frames=dict(production_cm='analysis axes x = subject left, f = forward, u = up; origin = frozen pelvis_root projected to the ground',
                source_frame_cm='the same axes in the frozen v005 frame; production = source + (%.5f, %.5f, 0) cm' % tuple(T_PROD[:2]),
                blender_m='(x, -f, u) / 100 applied to production_cm (Z up, faces -Y, subject left = +X)',
                handedness='the analysis frame is LEFT-handed (x × f = −u) because the Blender mapping negates one axis; frames below are right-handed in Blender and therefore have det −1 when written in analysis coordinates'),
    rule='internal centres = coordinate median of >= 2 independent surface definitions (A, B) and the frozen value (C); uncertainty = largest distance to any alternative; '
         'status usable (diagnostic) only if that is <= 1.0 cm. Construction joints are carried exactly and validated against the v005 surface. Numerical fit precision is not anatomical certainty.',
    v003_crosscheck='the same measurement code re-run on the frozen v003 production read-back (same frame); delta = movement of the proposal. It shows method stability on the production surface; it is NOT accuracy of an inferred internal centre, and is 0 by construction for copied construction joints.',
    t6_note='T-6 of the frozen package remains a surface-preservation check only.'),
    provenance_audit=dict(counts=pc, records=audit),
    joints={jid: ser(j) for jid, j in J.items()},
    segments=[dict(parent=a, child=b, length_cm=round(L, 3)) for a, b, L in SEG],
    asymmetry_l_minus_mirrored_r_cm=[dict(joint=a, x_sum=round(x, 3), df=round(f, 3), du=round(u, 3)) for a, x, f, u in asym],
    raw_measurements=dict(v005='fit_v005.json', v003='fit_v003.json'))
json.dump(doc, open(os.path.join(OUT, 'GR_U_REF_RP2_rigprep_landmarks_v001.json'), 'w'), indent=1)
print('joints', len(J), 'segments', len(SEG), 'provenance', pc)
