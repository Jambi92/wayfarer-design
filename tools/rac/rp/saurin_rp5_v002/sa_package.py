# sa_package.py CONSOLIDATION_DIR : Saurin RP5 freeze-candidate package (order cd87d9c §6, §8, §10): copies the verified semantic map and the accepted residual
#   register under candidate names, writes the sidecar, the freeze-candidate record and the package manifest (sha256 of every package file).
#   Status everywhere: FREEZE CANDIDATE / NOT FROZEN. Inputs must already exist: consolidation_rebuild.json, validation/, readback_M.json, readback_F.json.
import sys, os, json, shutil, hashlib, subprocess, datetime, numpy as np
D = sys.argv[1]; R = '/home/claude/wayfarer-design'; EV = R + '/reviews/rac-rp5-evidence/saurin'; OF = EV + '/full_cage/optionb_final'; V = D + '/validation'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
N = 'SA_RP5_freeze_candidate_v001'
shutil.copy2(V + '/SA_semantic_map.json', D + '/%s_semantic_map.json' % N); shutil.copy2(V + '/SA_semantic_map.json.face_semantic.npy', D + '/%s_face_semantic.npy' % N)
shutil.copy2(OF + '/SA_T4_angle_residuals.csv', D + '/%s_T4_angle_residuals_ACCEPTED.csv' % N); shutil.copy2(OF + '/SA_T4_angle_residuals.json', D + '/%s_T4_angle_residuals_ACCEPTED.json' % N)
shutil.copy2(EV + '/landmarks/SA-M188_landmarks.json', D + '/%s_landmarks_SA-M188.json' % N)
rb = json.load(open(D + '/consolidation_rebuild.json')); rM = json.load(open(D + '/readback_M.json')); rF = json.load(open(D + '/readback_F.json'))
sem = json.load(open(D + '/%s_semantic_map.json' % N)); T = json.load(open(V + '/SA_T1-T7.json')); FC = json.load(open(V + '/SA_fold_census.json'))
DF = json.load(open(V + '/SA_deformation_4step.json'))['poses']; PD = json.load(open(V + '/SA_PD2_ownership.json')); AR = json.load(open(OF + '/SA_T4_angle_residuals.json'))['summary']
imm = open(V + '/immutable_hashes.txt').read().splitlines(); n_unch = sum(1 for l in imm if l.endswith('UNCHANGED'))
head = subprocess.run(['git', '-C', R, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
files = {'cage': 'SA_RP5_full_cage_freeze_candidate_v001.npz', 'male_blend': 'SA_M_REF_RP5_freeze_candidate_v001.blend', 'female_blend': 'SA_F_REF_RP5_freeze_candidate_v001.blend',
         'barycentric_map': N + '_barycentric_map.npz', 'semantic_map': N + '_semantic_map.json', 'face_semantic': N + '_face_semantic.npy',
         'angle_residual_register_csv': N + '_T4_angle_residuals_ACCEPTED.csv', 'angle_residual_register_json': N + '_T4_angle_residuals_ACCEPTED.json', 'landmarks': N + '_landmarks_SA-M188.json'}
H = {k: sha(D + '/' + f) for k, f in files.items()}
gates = dict(
    T1={c: dict(max_mm=T[c]['T1_body']['max_mm'], p95_mm=T[c]['T1_body']['p95_mm'], median_mm=T[c]['T1_body']['median_mm'], passed=T[c]['T1_pass']) for c in ('SA-M188', 'SA-F188')},
    T2={c: dict(max_mm={k: v['max_mm'] for k, v in T[c]['T2'].items()}, passed=all(T[c]['T2_pass'].values())) for c in ('SA-M188', 'SA-F188')},
    T3={c: T[c]['T3_pass'] for c in ('SA-M188', 'SA-F188')}, T4_quality={c: T[c]['T4'] for c in ('SA-M188', 'SA-F188')},
    T5={c: all(v.get('mean_within') for v in T[c]['T5_density_pct_of_stature'].values()) for c in ('SA-M188', 'SA-F188')},
    T6={c: dict(max_mm=T[c]['T6_max_mm'], passed=T[c]['T6_pass'], accepted_residual='approx 1.03 / 1.02 mm, PASS under the established tool rule, below the 1.5 mm ceiling') for c in ('SA-M188', 'SA-F188')},
    T7={c: T[c]['T7_pass'] for c in ('SA-M188', 'SA-F188')},
    fold_census=dict(inverted_non_tip=FC['inverted_non_tip'], bowtie_non_tip=FC['bowtie_non_tip'], concave_non_tip=FC['concave_non_tip'], concave_deformation_critical=FC['concave_deformation_critical']),
    aspect_gt4_outside_tip_tail_exemptions=0,
    deformation=dict(poses=len(DF), topology_classified=sum('TOPOLOGY' in v['classification'] for v in DF.values()), topology_only_flips=sum(v['step4_topology_only_flips'] for v in DF.values())),
    PD2=dict(states=len(PD), cage_owned_flips=sum(v['cage_flips_cage_owned'] for v in PD.values())),
    accepted_angle_residuals={c: dict(quads=AR[c]['angle_residual_quads'], pct=AR[c]['pct'], severity=AR[c]['by_severity']) for c in AR})
side = dict(asset='Saurin RP5 full authored cage', status='FREEZE CANDIDATE / NOT FROZEN', version='freeze_candidate_v001', files=files, sha256=H,
            verts=rM['verts'], quads=rM['quads'], topology_sha256=rb['candidate']['topology_sha256'], shared_topology_c1_c2=True,
            semantic_labels=json.loads(rM['properties']['semantic_table']), semantic_face_sha256=sem['face_semantic_sha256'],
            units='cm in the npz and in the Blender mesh data; Blender object scale 0.01 (metres), identity location / rotation',
            source='canonical W2I6 base face list + SA_RP5_WORK_v001 (canonical + committed thigh art-pass delta); geometry = barycentric embedding (barycentric map file)',
            tail_module='accepted module, sha256 559565cc28a89db67c559c6db899cee51af0e349614fcb466255a6b35156baab, unchanged',
            readback=dict(male=rM['readback_verdict'], female=rF['readback_verdict'], max_vertex_error_cm=max(rM['max_vertex_readback_error_cm'], rF['max_vertex_readback_error_cm'])),
            provenance=dict(approved_commit='2ee75ae1845a223f3c8b8b9a5abfa10608f06b27', approved_cage='reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_RP5_full_cage_optionb_final.npz',
                            approved_cage_sha256=rb['approved']['sha256']))
json.dump(side, open(D + '/%s_sidecar.json' % N, 'w'), indent=1)
record = dict(record='Saurin RP5 freeze-candidate record', race='Saurin', stage='RP5', architecture='Option B local hand / foot density', status='FREEZE CANDIDATE / NOT FROZEN',
              source_approval_commit='2ee75ae1845a223f3c8b8b9a5abfa10608f06b27', approval_gate='reviews/claude-rac-rp5-saurin-full-authored-cage-gate.md',
              consolidation_order='reviews/chatgpt-rac-rp5-saurin-final-consolidation-freeze-readiness-order.md (cd87d9c)',
              generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), generated_at_repo_commit=head,
              cage_sha256=H['cage'], approved_cage_sha256=rb['approved']['sha256'], topology_sha256=rb['candidate']['topology_sha256'], male_candidate_sha256=H['male_blend'],
              female_candidate_sha256=H['female_blend'], semantic_map_sha256=H['semantic_map'], semantic_face_sha256=sem['face_semantic_sha256'], barycentric_map_sha256=H['barycentric_map'],
              accepted_tail_module_sha256='559565cc28a89db67c559c6db899cee51af0e349614fcb466255a6b35156baab',
              canonical_immutables='%d / %d unchanged' % (n_unch, len([l for l in imm if l.strip()])), clean_rebuild=rb['verdict'],
              accepted_residuals=dict(T4_angle_register=files['angle_residual_register_csv'], T6='max 1.03 mm (c1) / 1.02 mm (c2), PASS under the established tool rule'),
              gates=gates, production_copy='PRODUCTION COPY DEFERRED — NO UNAMBIGUOUS APPROVED DESTINATION')
json.dump(record, open(D + '/%s_freeze_candidate_record.json' % N, 'w'), indent=1)
pkg = list(files.values()) + [N + '_sidecar.json', N + '_freeze_candidate_record.json']
man = dict(package='Saurin RP5 freeze candidate v001 (FREEZE CANDIDATE / NOT FROZEN)', directory='reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/',
           files=[dict(file=f, bytes=os.path.getsize(D + '/' + f), sha256=sha(D + '/' + f)) for f in pkg],
           supporting_evidence=['consolidation_rebuild.json', 'readback_M.json', 'readback_F.json', 'validation/', 'package_verification.json'])
json.dump(man, open(D + '/%s_MANIFEST.json' % N, 'w'), indent=1); print(json.dumps(man, indent=1))
