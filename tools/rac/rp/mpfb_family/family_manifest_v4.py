# family_manifest_v4.py WORK OUTDIR EVIDIR : MPFB Family Base v004 (successor of frozen v003, order a18371c) -- per-file sidecars, the family-base
# manifest MPFB_FAMILY_BASE_v004.json (CANDIDATE until the author freezes it), provenance exports (heel rows, rings, pole slides) and the evidence tree.
import sys, os, json, shutil, hashlib, numpy as np
W, O, E = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
FZ = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/marchfolk_v003_freeze/MF_RP3_v003_FREEZE.json'; FROZEN = json.load(open(FZ))
ENT = [('MF-M-R', 'MF_M_REF_RP3_retopo_v004', 'Marchfolk', 'reviews/reference-assets/r6/MF-M-R_r6.npz'), ('MF-F-R', 'MF_F_REF_RP3_retopo_v004', 'Marchfolk', 'reviews/reference-assets/r6/MF-F-R_r6.npz'),
       ('SK208-C1R', 'SK_M_REF_RP3_retopo_v002', 'Skarn', 'reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz'), ('SKF208', 'SK_F_REF_RP3_retopo_v002', 'Skarn', 'reviews/reference-assets/r6/SKF208_r6.npz')]
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
core = np.load(W + '/v4core.npz'); log = json.loads(str(core['log'])); proof = json.load(open(W + '/maps/MPFB_FAMILY_v004_transfer_proof.json'))
mt = json.load(open(W + '/sheets/MPFB_FAMILY_v004_margin_table.json')); summ = json.load(open(W + '/gate_summary.json')); t4 = json.load(open(W + '/T4_union.json'))
for sd in ('maps', 'audit', 'anatomy', 'landmarks', 'validator', 'contact', 'deformation', 'readback', 'sheets', 'provenance'): os.makedirs(os.path.join(E, sd), exist_ok=True)
GATE = 'reviews/claude-rac-rp3-mpfb-family-base-v004-margin-hardening-gate.md'
hm08_map = os.path.join(O, ENT[0][1] + '_hm08_map.npz'); hm08_sha = sha(hm08_map); assert all(sha(os.path.join(O, nm + '_hm08_map.npz')) == hm08_sha for _, nm, _, _ in ENT), 'maps differ'
shutil.copy(hm08_map, os.path.join(E, 'maps', 'MPFB_FAMILY_BASE_v004_hm08_map.npz')); shutil.copy(W + '/maps/MPFB_FAMILY_v003_to_v004_map.npz', E + '/maps/'); shutil.copy(W + '/maps/MPFB_FAMILY_v004_transfer_proof.json', E + '/maps/')
shutil.copy(W + '/v4core.npz', E + '/maps/MPFB_FAMILY_BASE_v004_core.npz')
json.dump(dict(rule=log['row_class_legend']['2'], rows=log['heel']), open(E + '/provenance/MPFB_FAMILY_v004_heel_rows.json', 'w'), indent=1)
json.dump(dict(rings=log['rings'], ring_vertex_parents='MPFB_FAMILY_BASE_v004_core.npz: ring_parents (v003 edge (a, b) of every new vertex, in order), ring_name'), open(E + '/provenance/MPFB_FAMILY_v004_rings.json', 'w'), indent=1)
json.dump(dict(relocation=log['relocation']), open(E + '/provenance/MPFB_FAMILY_v004_toe3_pole_slides.json', 'w'), indent=1)
man = dict(family_base='MPFB Family Base v004 (margin-hardened successor of frozen Marchfolk v003)', status='CANDIDATE - NOT FROZEN (gate returned NEEDS AUTHOR DECISION; see %s)' % GATE,
           order='reviews/chatgpt-rac-rp3-mpfb-family-base-v004-margin-hardening-order.md (a18371c)', supersedes_if_frozen='v003 = historical accepted MPFB Family Base v1 (stays frozen, immutable)',
           parent=dict(record=os.path.basename(FZ), record_sha256=sha(FZ), files=FROZEN['files'], hm08_map_sha256=FROZEN['maps']['hm08_to_v003']['sha256'], face_topology_hash=FROZEN['shared_topology']['face_topology_hash'], verts=57674, quads=57672),
           topology=dict(verts=log['verts'], quads=log['quads'], face_topology_hash=PH[ENT[0][1] + '.blend']['face_topology_hash'], identical_in_all_configurations=bool(len({PH[nm + '.blend']['face_topology_hash'] for _, nm, _, _ in ENT}) == 1)),
           maps=dict(hm08_to_v004=dict(file='MPFB_FAMILY_BASE_v004_hm08_map.npz', sha256=hm08_sha, identical_for_every_race=True, max_row_support=proof['hm08_map']['max_row_support'], row_sum=[proof['hm08_map']['row_sum_min'], proof['hm08_map']['row_sum_max']]),
                     v003_to_v004=dict(file='MPFB_FAMILY_v003_to_v004_map.npz', sha256=sha(W + '/maps/MPFB_FAMILY_v003_to_v004_map.npz'), exact_rows=proof['v003_to_v004']['exact_rows'], residual_mm_by_row_class=proof['v003_to_v004']['max_residual_mm_by_row_class']),
                     core=dict(file='MPFB_FAMILY_BASE_v004_core.npz', sha256=sha(W + '/v4core.npz')), row_classes=dict(legend=log['row_class_legend'], counts=log['counts'])),
           operations=dict(A_heel=dict(vertices=[r['vertex'] for r in log['heel']], rule='posterior-heel linear quad-centre rows with v003 deviation > 1.0 mm on any accepted configuration -> on-surface barycentric row of the same hm08 quad'),
                           B_hip=[r for r in log['rings'] if r['name'].startswith('hip')], C_toes=[dict(name=r['name'], strip_quads=r['strip_quads'], verts_added=r['verts_added']) for r in log['rings'] if r['name'].startswith('toe')],
                           C_toe3_pole_slides=log['relocation']),
           validator=dict(authoritative='D1 + D3 + D4 (val2lib.py / validator_v2.py --scale-ref 173.143)', firm_pass={c: mt['summary'][c]['v004_firm'] for c in mt['summary']},
                          fails={c: mt['summary'][c]['v004_fail'] for c in mt['summary']}, margin0={c: mt['summary'][c]['v004_margin0'] for c in mt['summary']},
                          proposed_D5_firm_pass={c: mt['summary'][c]['D5_firm'] for c in mt['summary']}),
           T4_union=t4, configurations={})
for cid, nm, race, r6 in ENT:
    ph = PH[nm + '.blend']; an = json.load(open('%s/anat/%s_v004_anatomy.json' % (W, cid))); au = json.load(open('%s/audit/%s_v004_audit.json' % (W, cid))); lm = json.load(open('%s/lm/%s_v004_landmarks.json' % (W, cid)))
    v4 = json.load(open('%s/val/%s_v004_validator_v2_D4.json' % (W, cid)))['summary']; rb = json.load(open('%s/freeze/%s_readback.json' % (W, nm)))
    sc = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race=race, configuration=cid,
              status='MPFB FAMILY BASE v004 SUCCESSOR CANDIDATE (%s) - NOT FROZEN' % race, source=dict(id=cid, r6=r6, r6_sha256=sha('/home/claude/wayfarer-design/' + r6)),
              mapping=dict(hm08_map=nm + '_hm08_map.npz', hm08_map_sha256=sha(os.path.join(O, nm + '_hm08_map.npz')), family_map='MPFB_FAMILY_BASE_v004_hm08_map.npz (identical)'),
              frame=lm['frame'], landmarks=nm.replace('_retopo_', '_') + '_landmarks.json', readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
              topology=dict(components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], degenerate_faces=au['degenerate_faces'], self_intersection_face_pairs=au['self_intersection_face_pairs'],
                            T4_angle=au['angle_45_135_violations'], T4_aspect=au['aspect_gt4_violations'], density={k: v['mean'] for k, v in au['density_pct_of_stature'].items()},
                            validator_D1_D3_D4_firm_fail=v4['D1_D3_firm_fail'], validator_D1_D3_D4_margin0=v4['margin_zero']),
              anatomy=dict(T1_T2_pass=an['T1_T2_pass'], T3_pass=an['T3_pass'], T7_pass=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], feet_T2_max_mm=an['deviation_prod_to_source']['feet']['max_mm'], silhouette_iou=an['silhouette_iou']), gate=GATE)
    json.dump(sc, open(os.path.join(O, nm + '.json'), 'w'), indent=1); shutil.copy('%s/lm/%s_v004_landmarks.json' % (W, cid), os.path.join(O, nm.replace('_retopo_', '_') + '_landmarks.json'))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], sidecar=nm + '.json')
    for f_ in ('%s_v004_audit.json' % cid, '%s_v004_face.json' % cid): shutil.copy('%s/audit/%s' % (W, f_), E + '/audit/')
    shutil.copy('%s/audit/%s_v004_contact.json' % (W, cid), E + '/contact/'); shutil.copy('%s/anat/%s_v004_anatomy.json' % (W, cid), E + '/anatomy/'); shutil.copy('%s/lm/%s_v004_landmarks.json' % (W, cid), E + '/landmarks/')
    for f_ in ('%s_v004_validator_v2.json' % cid, '%s_v004_validator_v2_D4.json' % cid, '%s_v004_validator_v2_D4_D5proposed.json' % cid): shutil.copy('%s/val/%s' % (W, f_), E + '/validator/')
    shutil.copy('%s/def/deform_%s_v004.json' % (W, cid), E + '/deformation/'); shutil.copy('%s/freeze/%s_readback.json' % (W, nm), E + '/readback/')
for f_ in ('SK208-C1R_v004_face_identity.json', 'SK208-C1R_v003fit_face_identity.json'): shutil.copy('%s/anat/%s' % (W, f_), E + '/anatomy/')
for f_ in ('MPFB_v004_deformation_comparison.json', 'MPFB_v004_flip_parentage.json'): shutil.copy('%s/def/%s' % (W, f_), E + '/deformation/')
for f_ in ('gate_summary.json', 'T4_union.json'): shutil.copy('%s/%s' % (W, f_), E + '/')
json.dump(man, open(os.path.join(O, 'MPFB_FAMILY_BASE_v004.json'), 'w'), indent=1); shutil.copy(os.path.join(O, 'MPFB_FAMILY_BASE_v004.json'), E)
for f_ in os.listdir(O):
    if f_.endswith('.json'): shutil.copy(os.path.join(O, f_), E + '/')
for f_ in os.listdir(W + '/sheets'): shutil.copy('%s/sheets/%s' % (W, f_), E + '/sheets/')
with open(E + '/production_files_sha256.txt', 'w') as fh:
    for f_ in sorted(os.listdir(O)): fh.write('%s  %s\n' % (sha(os.path.join(O, f_)), f_))
print(json.dumps(dict(topology=man['topology'], maps={k: v.get('sha256', '')[:12] if isinstance(v, dict) else '' for k, v in man['maps'].items()}, configs={k: v['sha256'][:12] for k, v in man['configurations'].items()}), indent=1))
