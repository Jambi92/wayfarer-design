# family_manifest_v5.py WORK OUTDIR EVIDIR : MPFB Family Base v005 (final toe-2 web correction, order 33a2dfe) -- sidecars, MPFB_FAMILY_BASE_v005.json
# (CANDIDATE until the author freezes it), provenance exports and the evidence tree.
import sys, os, json, shutil, hashlib, glob, numpy as np
W, O, E = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
FZ = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/marchfolk_v003_freeze/MF_RP3_v003_FREEZE.json'; FROZEN = json.load(open(FZ))
V4M = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/mpfb_family_base_v004/MPFB_FAMILY_BASE_v004.json'
ENT = [('MF-M-R', 'MF_M_REF_RP3_retopo_v005', 'Marchfolk', 'reviews/reference-assets/r6/MF-M-R_r6.npz'), ('MF-F-R', 'MF_F_REF_RP3_retopo_v005', 'Marchfolk', 'reviews/reference-assets/r6/MF-F-R_r6.npz'),
       ('SK208-C1R', 'SK_M_REF_RP3_retopo_v003', 'Skarn', 'reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz'), ('SKF208', 'SK_F_REF_RP3_retopo_v003', 'Skarn', 'reviews/reference-assets/r6/SKF208_r6.npz')]
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
core = np.load(W + '/v5core.npz'); log = json.loads(str(core['log'])); proof = json.load(open(W + '/maps/MPFB_FAMILY_v005_transfer_proof.json'))
mt = json.load(open(W + '/audit/MPFB_FAMILY_v005_margin_table.json')); t4 = json.load(open(W + '/audit/T4_union_v003_tw0_v004_v005.json')); la = json.load(open(W + '/audit/MPFB_v005_toe2_local_audit.json'))
fp = json.load(open(W + '/def/MPFB_v005_flip_parentage.json'))
for sd in ('maps', 'audit', 'anatomy', 'landmarks', 'validator', 'contact', 'deformation', 'readback', 'sheets', 'provenance'): os.makedirs(os.path.join(E, sd), exist_ok=True)
GATE = 'reviews/claude-rac-rp3-mpfb-family-base-final-toe2-web-gate.md'
hm = os.path.join(O, ENT[0][1] + '_hm08_map.npz'); hm_sha = sha(hm); assert all(sha(os.path.join(O, nm + '_hm08_map.npz')) == hm_sha for _, nm, _, _ in ENT)
shutil.copy(hm, E + '/maps/MPFB_FAMILY_BASE_v005_hm08_map.npz'); shutil.copy(W + '/v5core.npz', E + '/maps/MPFB_FAMILY_BASE_v005_core.npz')
for f_ in ('MPFB_FAMILY_v003_to_v005_map.npz', 'MPFB_FAMILY_v004_to_v005_map.npz', 'MPFB_FAMILY_v005_transfer_proof.json'): shutil.copy(W + '/maps/' + f_, E + '/maps/'); shutil.copy(W + '/maps/' + f_, O)
json.dump(dict(racetrack=log['sides'], turns=log['turns'], vertex_provenance=json.loads(str(core['racetrack_provenance'])), retained=log['retained']), open(E + '/provenance/MPFB_FAMILY_v005_toe2_racetrack.json', 'w'), indent=1)
for f_ in glob.glob(W + '/work/rs_toe2_tw0_d5.json'): shutil.copy(f_, E + '/provenance/ring_search_toe2_on_retained_base_D5.json')
man = dict(family_base='MPFB Family Base v005 (final margin-hardened successor: v004 heel / hip / toe-3 retained, toe-2 closed ring replaced by a dorsal racetrack)',
           status='CANDIDATE - NOT FROZEN (gate: FAMILY BASE PASS WITH DOCUMENTED TOE2 EXCEPTION - AUTHOR DECISION; %s)' % GATE, order='reviews/chatgpt-rac-rp3-mpfb-family-base-final-toe2-web-order.md (33a2dfe)',
           history=dict(v003='historical accepted MPFB Family Base v1 (frozen, immutable)', v004='margin-hardening provenance (candidate, unchanged)', v005='final successor candidate'),
           parents=dict(v003_freeze_record=dict(file=os.path.basename(FZ), sha256=sha(FZ), face_topology_hash=FROZEN['shared_topology']['face_topology_hash']), v004_manifest=dict(file=os.path.basename(V4M), sha256=sha(V4M))),
           topology=dict(verts=log['verts'], quads=log['quads'], face_topology_hash=PH[ENT[0][1] + '.blend']['face_topology_hash'], identical_in_all_configurations=len({PH[nm + '.blend']['face_topology_hash'] for _, nm, _, _ in ENT}) == 1),
           maps=dict(hm08_to_v005=dict(file='MPFB_FAMILY_BASE_v005_hm08_map.npz', sha256=hm_sha, identical_for_every_race=True), v003_to_v005=dict(file='MPFB_FAMILY_v003_to_v005_map.npz', sha256=sha(W + '/maps/MPFB_FAMILY_v003_to_v005_map.npz')),
                     v004_to_v005=dict(file='MPFB_FAMILY_v004_to_v005_map.npz', sha256=sha(W + '/maps/MPFB_FAMILY_v004_to_v005_map.npz')), core=dict(file='MPFB_FAMILY_BASE_v005_core.npz', sha256=sha(W + '/v5core.npz')),
                     row_classes=dict(legend=log['row_class_legend'], counts=log['counts'])),
           validator=dict(authoritative='D1 + D3 + D4 + D5 (validator_v2.py --scale-ref 173.143 --d5)', firm_pass={c: mt['summary'][c]['firm'] for c in mt['summary']}, margin0={c: mt['summary'][c]['margin0'] for c in mt['summary']}),
           toe2=dict(architecture='dorsal racetrack around frozen-v003 loop 497 (strips 497|1262 and 497|1119), sector >= %g deg from plantar, 8 corner turns' % log['sector_deg'], local_audit={c: la[c]['v005_racetrack_patch'] for c in la},
                     toe_ext30_new_flips=fp['fold_test']), T4_union=t4, configurations={})
for cid, nm, race, r6 in ENT:
    ph = PH[nm + '.blend']; an = json.load(open('%s/anat/%s_v005_anatomy.json' % (W, cid))); au = json.load(open('%s/audit/%s_v005_audit.json' % (W, cid))); lm = json.load(open('%s/lm/%s_v005_landmarks.json' % (W, cid)))
    v5 = json.load(open('%s/val/%s_v005_validator_v2_D4_D5.json' % (W, cid)))['summary']; rb = json.load(open('%s/freeze/%s_readback.json' % (W, nm)))
    sc = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'], race=race, configuration=cid,
              status='MPFB FAMILY BASE v005 FINAL SUCCESSOR CANDIDATE (%s) - NOT FROZEN' % race, source=dict(id=cid, r6=r6, r6_sha256=sha('/home/claude/wayfarer-design/' + r6)),
              mapping=dict(hm08_map=nm + '_hm08_map.npz', hm08_map_sha256=sha(os.path.join(O, nm + '_hm08_map.npz')), family_map='MPFB_FAMILY_BASE_v005_hm08_map.npz (identical)'), frame=lm['frame'],
              landmarks=nm.replace('_retopo_', '_') + '_landmarks.json', readback=dict(max_abs_diff_vs_candidate_m=rb['max_abs_diff_vs_candidate_m'], faces_equal_candidate=rb['faces_equal_candidate'], normals_outward=rb['normals_outward']),
              topology=dict(components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], degenerate_faces=au['degenerate_faces'], self_intersection_face_pairs=au['self_intersection_face_pairs'],
                            T4_angle=au['angle_45_135_violations'], T4_aspect=au['aspect_gt4_violations'], density={k: v['mean'] for k, v in au['density_pct_of_stature'].items()}, validator_D1_D3_D4_D5_firm_fail=v5['D1_D3_firm_fail'], margin0=v5['margin_zero']),
              anatomy=dict(T1_T2_pass=an['T1_T2_pass'], T3_pass=an['T3_pass'], T7_pass=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], feet_T2_max_mm=an['deviation_prod_to_source']['feet']['max_mm'], silhouette_iou=an['silhouette_iou']), gate=GATE)
    json.dump(sc, open(os.path.join(O, nm + '.json'), 'w'), indent=1); shutil.copy('%s/lm/%s_v005_landmarks.json' % (W, cid), os.path.join(O, nm.replace('_retopo_', '_') + '_landmarks.json'))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], sidecar=nm + '.json')
    for f_ in ('%s_v005_audit.json' % cid, '%s_v005_face.json' % cid): shutil.copy('%s/audit/%s' % (W, f_), E + '/audit/')
    shutil.copy('%s/audit/%s_v005_contact_vs_v004.json' % (W, cid), E + '/contact/'); shutil.copy('%s/anat/%s_v005_anatomy.json' % (W, cid), E + '/anatomy/'); shutil.copy('%s/lm/%s_v005_landmarks.json' % (W, cid), E + '/landmarks/')
    for f_ in ('_v005_validator_v2.json', '_v005_validator_v2_D4.json', '_v005_validator_v2_D4_D5.json'): shutil.copy('%s/val/%s%s' % (W, cid, f_), E + '/validator/')
    shutil.copy('%s/def/deform_%s_v005.json' % (W, cid), E + '/deformation/'); shutil.copy('%s/freeze/%s_readback.json' % (W, nm), E + '/readback/')
shutil.copy(W + '/anat/SK208-C1R_v005_face_identity.json', E + '/anatomy/')
for f_ in ('MPFB_v005_deformation_comparison.json', 'MPFB_v005_flip_parentage.json', 'MPFB_v004_ring_vs_tw0_flip_fold.json'): shutil.copy('%s/def/%s' % (W, f_), E + '/deformation/')
for f_ in glob.glob(W + '/work/toeflip_*.json'): shutil.copy(f_, E + '/deformation/')
for f_ in ('MPFB_v005_toe2_local_audit.json', 'T4_union_v003_tw0_v004_v005.json', 'MPFB_FAMILY_v005_margin_table.json', 'MPFB_FAMILY_v005_margin_table.csv', 'retention_and_toe2_summary.json'): shutil.copy('%s/audit/%s' % (W, f_), E + '/audit/')
json.dump(man, open(os.path.join(O, 'MPFB_FAMILY_BASE_v005.json'), 'w'), indent=1)
for f_ in os.listdir(O):
    if f_.endswith('.json'): shutil.copy(os.path.join(O, f_), E + '/')
for f_ in os.listdir(W + '/sheets'): shutil.copy('%s/sheets/%s' % (W, f_), E + '/sheets/')
with open(E + '/production_files_sha256.txt', 'w') as fh:
    for f_ in sorted(os.listdir(O)): fh.write('%s  %s\n' % (sha(os.path.join(O, f_)), f_))
print(json.dumps(dict(topology=man['topology'], maps={k: v.get('sha256', '')[:12] for k, v in man['maps'].items() if isinstance(v, dict) and 'sha256' in v}, configs={k: v['sha256'][:12] for k, v in man['configurations'].items()}), indent=1))
