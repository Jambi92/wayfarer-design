# sa_verify_package.py CONSOLIDATION_DIR : independent final internal audit of the Saurin RP5 freeze-candidate package (order cd87d9c §11), from the files on
#   disk / repository state only (fresh process; approved state read from git object 2ee75ae, not from any working copy):
#   geometry identity, topology, c1 / c2, quality / ownership results identical to the approved evidence, package integrity (manifest / sidecar / record hashes,
#   fresh Blender read-back in new bpy processes), freeze safety (nothing marked frozen, approved evidence + pilot files unchanged, immutables re-hashed).
import sys, os, json, hashlib, subprocess, tempfile, io, csv, numpy as np
D = os.path.abspath(sys.argv[1]); R = '/home/claude/wayfarer-design'; AC = '2ee75ae1845a223f3c8b8b9a5abfa10608f06b27'; T = R + '/tools/rac/rp/saurin_rp5_v002'
OFr = 'reviews/rac-rp5-evidence/saurin/full_cage/optionb_final'; N = 'SA_RP5_freeze_candidate_v001'; BPY = '/home/claude/stc/bin/python3'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def git_bytes(path): return subprocess.run(['git', '-C', R, 'show', '%s:%s' % (AC, path)], capture_output=True).stdout
res = {}; ok = True
def check(n, c, **k):
    global ok
    res[n] = dict(ok=bool(c), **k); ok &= bool(c); print(('PASS ' if c else 'FAIL ') + n, json.dumps(k, default=str)[:240], flush=True)
man = json.load(open(D + '/%s_MANIFEST.json' % N)); side = json.load(open(D + '/%s_sidecar.json' % N)); rec = json.load(open(D + '/%s_freeze_candidate_record.json' % N))
check('manifest hashes == files on disk', all(sha(D + '/' + f['file']) == f['sha256'] and os.path.getsize(D + '/' + f['file']) == f['bytes'] for f in man['files']), files=len(man['files']))
check('sidecar hashes == files on disk', all(sha(D + '/' + side['files'][k]) == side['sha256'][k] for k in side['files']))
check('record hashes == files on disk', rec['cage_sha256'] == sha(D + '/SA_RP5_full_cage_freeze_candidate_v001.npz') and rec['male_candidate_sha256'] == sha(D + '/SA_M_REF_RP5_freeze_candidate_v001.blend')
      and rec['female_candidate_sha256'] == sha(D + '/SA_F_REF_RP5_freeze_candidate_v001.blend') and rec['barycentric_map_sha256'] == sha(D + '/%s_barycentric_map.npz' % N)
      and rec['semantic_map_sha256'] == sha(D + '/%s_semantic_map.json' % N))
# geometry identity vs the approved commit
A = np.load(io.BytesIO(git_bytes(OFr + '/SA_RP5_full_cage_optionb_final.npz'))); C = np.load(D + '/SA_RP5_full_cage_freeze_candidate_v001.npz')
check('approved npz from git object has the approved sha', hashlib.sha256(git_bytes(OFr + '/SA_RP5_full_cage_optionb_final.npz')).hexdigest() == rec['approved_cage_sha256'])
check('candidate arrays bit-identical to approved', all(np.array_equal(A[k], C[k]) and A[k].dtype == C[k].dtype for k in A.files) and set(C.files) == set(A.files) | {'provenance'}, arrays=A.files)
topo = hashlib.sha256(np.ascontiguousarray(C['Q'].astype(np.int64)).tobytes()).hexdigest()
check('topology hash', topo == rec['topology_sha256'] == '255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49', topology=topo)
check('counts', len(C['V']) == 190948 and len(C['Q']) == 190946)
bm = np.load(D + '/%s_barycentric_map.npz' % N); check('barycentric map == embedding', np.array_equal(bm['base_face'], C['tri']) and np.array_equal(bm['barycentric'], C['bc']))
fsA = np.load(io.BytesIO(git_bytes(OFr + '/SA_semantic_map_final.json.face_semantic.npy')), allow_pickle=True); fsC = np.load(D + '/%s_face_semantic.npy' % N, allow_pickle=True)
check('semantic face labels identical to approved', np.array_equal(fsA, fsC))
semA = json.loads(git_bytes(OFr + '/SA_semantic_map_final.json')); semC = json.load(open(D + '/%s_semantic_map.json' % N))
check('semantic map identical to approved (loops, face hash, topology hash)', semA['loops'] == semC['loops'] and semA['face_semantic_sha256'] == semC['face_semantic_sha256'] and semA['topology_sha256'] == semC['topology_sha256'])
# quality / ownership identical to the approved evidence (validation rerun on the candidate in the clean workspace)
V = D + '/validation'
for a, b_ in (('SA_full_cage_optionb_T1-T7.json', 'SA_T1-T7.json'), ('SA_fold_census_final.json', 'SA_fold_census.json'), ('SA_deformation_4step_final.json', 'SA_deformation_4step.json'),
              ('SA_PD2_ownership_final.json', 'SA_PD2_ownership.json'), ('SA_identity_metrics_final.json', 'SA_identity_metrics.json'), ('SA_T4_angle_residuals.json', 'SA_T4_angle_residuals.json')):
    x = json.loads(git_bytes(OFr + '/' + a)); y = json.load(open(V + '/' + b_))
    for z_ in (x, y): z_.pop('cage', None); z_.pop('tag', None)          # run metadata (input path, run tag) only
    check('validation %s == approved %s' % (b_, a), json.dumps(x, sort_keys=True) == json.dumps(y, sort_keys=True))
check('angle register csv identical to approved', git_bytes(OFr + '/SA_T4_angle_residuals.csv') == open(D + '/%s_T4_angle_residuals_ACCEPTED.csv' % N, 'rb').read() == open(V + '/SA_T4_angle_residuals.csv', 'rb').read())
TT = json.load(open(V + '/SA_T1-T7.json')); FC = json.load(open(V + '/SA_fold_census.json')); DF = json.load(open(V + '/SA_deformation_4step.json'))['poses']; PD = json.load(open(V + '/SA_PD2_ownership.json'))
check('T-1 .. T-7 pass c1 / c2', all(TT[c]['T1_pass'] and all(TT[c]['T2_pass'].values()) and TT[c]['T3_pass'] and TT[c]['T6_pass'] and TT[c]['T7_pass']
                                     and all(v.get('mean_within') for v in TT[c]['T5_density_pct_of_stature'].values()) for c in ('SA-M188', 'SA-F188')))
check('host-aware census 0 / 0 / 0 / 0', FC['inverted_non_tip'] == FC['bowtie_non_tip'] == FC['concave_non_tip'] == FC['concave_deformation_critical'] == 0)
q4 = C['Q']; ql = C['qlab'].astype(str); ex = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
for cfg, key in (('c1', 'v_M'), ('c2', 'v_F')):
    w = np.load(os.environ.get('SA_W', '/tmp/claude-0/rp5clean') + '/work/SA_RP5_WORK_v001.npz'); Fw = w['f'].astype(np.int64); Vx = (C['bc'][:, :, None] * w[key].astype(float)[Fw[C['tri']]]).sum(1)
    el = np.linalg.norm(Vx[q4] - np.roll(Vx[q4], -1, 1), axis=2); asp = el.max(1) / el.min(1)
    check('%s aspect > 4 outside tip / tail exemptions = 0, no collapsed edge' % cfg, int(((asp > 4) & ~ex).sum()) == 0 and el.min() > 1e-3, min_edge_mm=float(el.min() * 10), max_aspect=float(asp[~ex].max()))
check('deformation: 0 topology poses / 0 topology-only flips', sum('TOPOLOGY' in v['classification'] for v in DF.values()) == 0 and sum(v['step4_topology_only_flips'] for v in DF.values()) == 0, poses=len(DF))
check('PD-2: 0 cage-owned flips', sum(v['cage_flips_cage_owned'] for v in PD.values()) == 0, states=len(PD))
# fresh Blender read-back (new bpy processes)
for k in ('M', 'F'):
    out = tempfile.mktemp(suffix='.json')
    subprocess.run([BPY, T + '/sa_freeze_candidate_readback.py', D + '/SA_%s_REF_RP5_freeze_candidate_v001.blend' % k, D + '/SA_RP5_full_cage_freeze_candidate_v001.npz', D + '/%s_face_semantic.npy' % N, 'v_' + k, out],
                   capture_output=True, env=dict(os.environ, SA_W=os.environ.get('SA_W', '/tmp/claude-0/rp5clean')))
    r = json.load(open(out)); r0 = json.load(open(D + '/readback_%s.json' % k))
    check('fresh Blender read-back %s' % k, r['readback_verdict'] == 'PASS' and r['topology_sha256'] == topo and r['sha256'] == sha(D + '/SA_%s_REF_RP5_freeze_candidate_v001.blend' % k)
          and json.dumps(r, sort_keys=True) == json.dumps(r0, sort_keys=True), objects=[o['name'] for o in r['objects']], max_err_cm=r['max_vertex_readback_error_cm'], scale=r['transform']['scale'])
# freeze safety
names = os.listdir(D) + os.listdir(V)
check('no file named frozen', not any('frozen' in n.lower() for n in names))
txt = ''.join(open(D + '/' + f, errors='ignore').read() for f in [x['file'] for x in man['files']] + ['%s_MANIFEST.json' % N] if f.endswith('.json'))          # package JSON files (the verification report itself excluded)
check('every status string is FREEZE CANDIDATE / NOT FROZEN (no FROZEN claim)', 'FREEZE CANDIDATE / NOT FROZEN' in txt and txt.replace('NOT FROZEN', '').upper().count('FROZEN') == 0)
diff = subprocess.run(['git', '-C', R, 'diff', '--stat', AC, '--', OFr], capture_output=True, text=True).stdout.strip()
check('approved optionb_final evidence (incl. pilot files) unchanged since 2ee75ae', diff == '', diff=diff)
imm = subprocess.run(['python3', T + '/sa_immutables.py', R + '/reviews/rac-rp5-evidence/saurin/full_cage/revision/immutable_hashes_revision.txt', tempfile.mktemp()], capture_output=True, text=True).stdout
check('canonical / accepted immutables re-hashed: 229 / 229 unchanged', '229 / 229 unchanged' in imm, out=imm.strip().splitlines()[-1] if imm.strip() else '')
check('accepted tail module file', sha(R + '/reviews/rac-rp5-evidence/saurin/tail_module/SA_tail_module.npz') == rec['accepted_tail_module_sha256'])
res['verdict'] = 'PASS' if ok else 'FAIL'; json.dump(res, open(D + '/package_verification.json', 'w'), indent=1); print('PACKAGE VERIFICATION', res['verdict'])
