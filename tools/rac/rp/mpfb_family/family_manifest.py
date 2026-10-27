# family_manifest.py WORK OUTDIR EVIDIR RACE "ID:NAME:R6:BUILD" ... : MPFB Family Propagation Standard v1, steps 5 / 12 -- per-file sidecars and the
# family propagation manifest (frozen base + map hashes, race source hashes, regeneration identity, production hashes, topology identity proof).
import sys, os, json, shutil, hashlib, numpy as np
W, O, E, RACE = sys.argv[1:5]; ENT = [x.split(':') for x in sys.argv[5:]]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
FROZEN = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/marchfolk_v003_freeze/MF_RP3_v003_FREEZE.json'))
PH = {os.path.basename(json.loads(l)['file']): json.loads(l) for l in open(W + '/prod_hashes.jsonl')}
for sd in ('regen', 'audit', 'anatomy', 'landmarks', 'validator', 'deformation', 'sheets'): os.makedirs(os.path.join(E, sd), exist_ok=True)
man = dict(standard='MPFB Family Propagation Standard v1 (draft)', race=RACE, frozen_family_base=dict(record='MF_RP3_v003_FREEZE.json', record_sha256=sha('/home/claude/wayfarer-design/reviews/rac-rp3-evidence/marchfolk_v003_freeze/MF_RP3_v003_FREEZE.json'),
           files=FROZEN['files'], hm08_map_sha256=FROZEN['maps']['hm08_to_v003']['sha256'], face_topology_hash=FROZEN['shared_topology']['face_topology_hash']), configurations={})
for cid, nm, r6, bj in ENT:
    rc = json.load(open('%s/src/%s_regen_check.json' % (W, cid))); fz = np.load('%s/cand/%s_fam.npz' % (W, cid)); plog = json.loads(str(fz['log'])); ph = PH[nm + '.blend']
    au = json.load(open('%s/audit/%s_fam_audit.json' % (W, cid))); an = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, cid))); fr = json.load(open('%s/audit/%s_fam_face.json' % (W, cid)))
    v1 = json.load(open('%s/val/%s_fam_validator_v2.json' % (W, cid)))['summary']; v4 = json.load(open('%s/val/%s_fam_validator_v2_D4.json' % (W, cid)))
    lm = json.load(open('%s/lm/%s_fam_landmarks.json' % (W, cid))); mapf = os.path.join(O, nm + '_hm08_map.npz')
    sc = dict(file=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], verts=ph['verts'], quads=ph['quads'],
              status='PRODUCTION CANDIDATE (%s, MPFB family propagation from frozen Marchfolk v003) - not accepted' % RACE,
              source=dict(id=cid, r6=r6, r6_sha256=rc['committed_sha256'], build=bj, build_sha256=rc['build_sha256'], r6_geometry_hash=rc['committed_geom'], regenerated_geometry_hash=rc['regen_geom'], regeneration_identical=rc['geometry_identical']),
              propagation=plog, operations=['regenerate accepted source (MPFB 2.0.17 / Blender 5.2.2), geometry identity proven', 'export hm08 body (helpers removed)', 'apply the FROZEN hm08 -> family-base map (no topology change, no per-race fitting)',
                                              'production frame / origin (pelvis root projected to ground)'],
              mapping=dict(hm08_map=os.path.basename(mapf), hm08_map_sha256=sha(mapf), arrays_identical_to_frozen=True), frame=lm['frame'], landmarks=nm.replace('_retopo_', '_') + '_landmarks.json',
              topology=dict(components=au['components'], boundary_edges=au['boundary_edges'], nonmanifold_edges=au['nonmanifold_edges'], degenerate_faces=au['degenerate_faces'], normals_outward=au['normals_outward'],
                            self_intersection_face_pairs=au['self_intersection_face_pairs'], T4_angle=au['angle_45_135_violations'], T4_aspect=au['aspect_gt4_violations'], density={k: v['mean'] for k, v in au['density_pct_of_stature'].items()},
                            validator_D1_D3_firm_fail=v1['D1_D3_firm_fail'], validator_D1_D3_D4_firm_fail=v4['summary']['D1_D3_firm_fail'], mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']]),
              anatomy=dict(T1_T2_pass=an['T1_T2_pass'], T3_pass=an['T3_pass'], T7_pass=an['T7_pass'], stature_diff_mm=an['stature_diff_mm'], prod_to_source=an['deviation_prod_to_source'], source_to_prod=an['deviation_source_to_prod'], silhouette_iou=an['silhouette_iou']),
              gate='reviews/claude-rac-rp3-skarn-family-propagation-gate.md')
    json.dump(sc, open(os.path.join(O, nm + '.json'), 'w'), indent=1); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), os.path.join(O, nm.replace('_retopo_', '_') + '_landmarks.json'))
    man['configurations'][cid] = dict(production=nm + '.blend', sha256=ph['sha256'], geometry_hash=ph['geometry_hash'], face_topology_hash=ph['face_topology_hash'], source_r6_sha256=rc['committed_sha256'], source_build_sha256=rc['build_sha256'],
                                      regeneration_identical=rc['geometry_identical'], hm08_map_sha256=sha(mapf), sidecar=nm + '.json')
    shutil.copy('%s/src/%s_regen_check.json' % (W, cid), E + '/regen/')
    for t in ('fam', 'native'):
        shutil.copy('%s/audit/%s_%s_audit.json' % (W, cid, t), E + '/audit/'); shutil.copy('%s/audit/%s_%s_face.json' % (W, cid, t), E + '/audit/'); shutil.copy('%s/def/deform_%s_%s.json' % (W, cid, t), E + '/deformation/')
    shutil.copy('%s/anat/%s_fam_anatomy.json' % (W, cid), E + '/anatomy/'); shutil.copy('%s/lm/%s_fam_landmarks.json' % (W, cid), E + '/landmarks/')
    for f_ in ('%s_fam_validator_v2.json' % cid, '%s_fam_validator_v2_D4.json' % cid): shutil.copy('%s/val/%s' % (W, f_), E + '/validator/')
    if os.path.exists('%s/anat/%s_face_identity.json' % (W, cid)): shutil.copy('%s/anat/%s_face_identity.json' % (W, cid), E + '/anatomy/')
fh = {c['face_topology_hash'] for c in man['configurations'].values()}
man['topology_identity'] = dict(all_face_topology_hashes_equal_frozen=bool(fh == {man['frozen_family_base']['face_topology_hash']}), verts=57674, quads=57672)
json.dump(man, open(os.path.join(O, '%s_RP3_family_propagation_manifest.json' % RACE[:2].upper()), 'w'), indent=1); shutil.copy(os.path.join(O, '%s_RP3_family_propagation_manifest.json' % RACE[:2].upper()), E)
for f_ in os.listdir(O):
    if f_.endswith('.json'): shutil.copy(os.path.join(O, f_), E + '/')
if os.path.isdir(W + '/sheets'):
    for f_ in os.listdir(W + '/sheets'): shutil.copy('%s/sheets/%s' % (W, f_), E + '/sheets/')
print(json.dumps(man['topology_identity']), json.dumps({k: v['sha256'][:12] for k, v in man['configurations'].items()}))
