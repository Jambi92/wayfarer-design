# hv_ear_family_freeze_record.py OUTDIR : Halvren RP3 ear family final author acceptance / freeze closure (record only, no rebuild of approved geometry)
#   read-back: the approved realizations (production-gate snapshot + the fam6 build files) re-hash to the recorded vertex / connectivity hashes;
#   the baked TRI-HV1 triangles are re-derived from the recorded per-quad diagonal choice and re-hash to the production-gate triangle hashes;
#   immutable references re-hashed; definitions, rules, creator bounds, tool hashes -> HALVREN_EAR_FAMILY_RP3_FREEZE.json
import sys, os, json, hashlib, shutil, subprocess, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
REPO = '/home/claude/wayfarer-design'; sys.path.insert(0, REPO + '/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
OUT = sys.argv[1]; os.makedirs(OUT + '/baked', exist_ok=True)
PG = REPO + '/reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate'; FC = REPO + '/reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure'
SNAP = '/tmp/claude-0/rt/hv/ear/prodsnap'; FAM = '/tmp/claude-0/rt/hv/ear/fam6/build'; HD = {'c1': 'HVC1-HB2HF2-HPB', 'c2': 'HVF178-HB2HF2-HPB'}
sha = lambda b: hashlib.sha256(b).hexdigest(); fsha = lambda p: sha(open(p, 'rb').read())
jl = lambda p: json.load(open(p)); pre = jl(PG + '/pre_audit_hashes.json')['meshes']; summ = jl(PG + '/HV_ear_production_gate_summary.json')
conv = lambda o: o.tolist() if isinstance(o, np.ndarray) else (float(o) if isinstance(o, np.floating) else str(o))
head = subprocess.run(['git', '-C', REPO, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
R = dict(record='HALVREN RP3 EAR FAMILY — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN', date='2026-10-30',
         authority='reviews/chatgpt-rac-rp3-halvren-ear-family-final-author-acceptance-freeze-closure-order.md (author ruling: FINAL PRODUCTION FREEZE APPROVED; reviewed Claude commit 2fa0c6e184e0e050e79bb1aeead3309ee341a6e2)',
         freeze_method='freeze-by-record: the production-gate state (2fa0c6e) is the freeze source; no geometry / topology rebuild; read-back of the approved realizations and re-derivation of the baked TRI-HV1 triangles from the recorded diagonal choices reproduce the recorded hashes exactly',
         source_commit=dict(reviewed='2fa0c6e184e0e050e79bb1aeead3309ee341a6e2', order_commit=head))
# ---------------- members + read-back
mem = {}; qh = set()
for k, ver in (('HE1', 'HVEAR4'), ('HE2', 'HVEAR3'), ('HE3', 'HVEAR4')):
    for c, h in HD.items():
        key = '%s_%s' % (h, k); p0 = pre[key]; rb = {}
        for src, path in (('production_gate_snapshot', '%s/%s_branch.npz' % (SNAP, key)), ('approved_build', '%s/%s_branch.npz' % (FAM, key))):
            z = np.load(path); rb[src] = dict(npz_sha256=fsha(path), V_float32_sha256=sha(z['V'].astype(np.float32).tobytes()), Q_sha256=sha(np.ascontiguousarray(z['Q']).astype(np.int64).tobytes()))
            rb[src]['matches_record'] = all(rb[src][q] == p0[q] for q in ('npz_sha256', 'V_float32_sha256', 'Q_sha256'))
        z = np.load('%s/%s_branch.npz' % (SNAP, key)); Q = np.asarray(z['Q']).astype(np.int64); bk = np.load('%s/baked/%s_%s_TRI-HV1.npz' % (PG, k, c)); ch = bk['diagonal_choice'].astype(np.int64)
        T = np.empty((2 * len(Q), 3), np.int64); A = ch == 0; T[0::2][A], T[1::2][A] = Q[A][:, [0, 1, 2]], Q[A][:, [0, 2, 3]]; T[0::2][~A], T[1::2][~A] = Q[~A][:, [0, 1, 3]], Q[~A][:, [1, 2, 3]]
        tsh = sha(T.tobytes()); rec_t = str(bk['triangles_sha256']); qh.add(p0['Q_sha256'])
        shutil.copy('%s/baked/%s_%s_TRI-HV1.npz' % (PG, k, c), '%s/baked/%s_%s_TRI-HV1.npz' % (OUT, k, c))
        S = summ['%s_%s' % (k, c)]
        mem['%s %s' % (k, c)] = dict(definition='%s %s' % (k, ver), head=h, n_vertices=p0['n_vertices'], n_quads=p0['n_quads'], npz_sha256=p0['npz_sha256'], V_float32_sha256=p0['V_float32_sha256'],
                                     Q_sha256=p0['Q_sha256'], read_back=rb, tri_hv1_triangles_sha256=rec_t, tri_hv1_rederived_sha256=tsh, tri_hv1_rederived_matches=tsh == rec_t,
                                     tri_hv1_step5_flips=S['step5_flips'], baked_choice_file='baked/%s_%s_TRI-HV1.npz' % (k, c),
                                     production_gate=dict(crossings_final=S['crossings_final_total'], pose_contacts=S['poses_contacts'], pose_triangle_inversions=S['poses_triangle_inversions'],
                                                          pose_root_inversions=S['poses_root_inversions'], lod_hv1={r: S['lod']['protected'][r] for r in ('0.5', '0.25')}, fbx_triangles_identical=S['fbx_triangles_identical']))
R['members'] = mem
R['quad_connectivity'] = dict(Q_sha256=sorted(qh), shared_by_all_six=len(qh) == 1, topology='VAEL_EAR_BRANCH_TOPOLOGY_v002 sheet + RI3 cuff canon on the MPFB family base v005 (HB2 + HF2 + HP-B head)')
he2f = jl(FC + '/HALVREN_HE2_HR2_FREEZE.json'); s_ = json.dumps(he2f)
R['he2_hr2_prior_freeze'] = dict(record='reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/HALVREN_HE2_HR2_FREEZE.json', record_sha256=fsha(FC + '/HALVREN_HE2_HR2_FREEZE.json'),
                                 c1_V_hash_in_record=mem['HE2 c1']['V_float32_sha256'] in s_, c2_V_hash_in_record=mem['HE2 c2']['V_float32_sha256'] in s_, unchanged=True)
# ---------------- definitions
cd = lambda k: json.loads(json.dumps(E.CAND[k], default=conv))
R['definitions'] = dict(HR2=dict(identity='HV_ROOT2 (Halvren HR2 root architecture, frozen with HE2 at ee0e98c)', HV_ROOT2=json.loads(json.dumps(E.HV_ROOT2, default=conv)), HV_SKIN=json.loads(json.dumps(E.HV_SKIN, default=conv)),
                                    HE3_variant='sulcus_h -1.0 (sulcus off), lift_top 0.55'),
                        HE1_HVEAR4=cd('HE1'), HE2_HVEAR3=cd('HE2'), HE3_HVEAR4=cd('HE3'),
                        realization_path='hv_ear.sh WORK RI3 <HE> <HEAD> with HV_REPAIR=1 -> hv_run_head.sh (ear_build.py + hv_cuff_repair.py stages 1-5 + ear_deform.py deformation guard); stages 4 / 5 only on sheet_fold_fix ears (HE1 / HE3); HE2 unflagged',
                        source_files=dict(ear_branch_lib='tools/rac/rp/fenn_rp3_v001/ear_branch_lib.py', definitions_json='reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/HV_ear_definitions_HVEAR4.json'))
# ---------------- production contract
R['production_contract'] = dict(
    TRI_HV1=dict(status='REQUIRED', rule='per quad (a,b,c,d): split A = (a,b,c)+(a,c,d), split B = (a,b,d)+(b,c,d); 1. smaller fold between the two triangle normals if the folds differ by > 0.5 deg; 2. else larger minimum triangle angle if > 0.5 deg apart; 3. else shorter diagonal (> 1e-9 cm); 4. else the diagonal holding the smallest vertex index; 5. intersection validation over rest + the 8 head / neck poses (ear neighbourhood 14 cm, triangle pairs touching the branch, no shared vertex): greedy flips in frozen quad order, kept only if the total crossing count drops, until stable. Triangles keep the quad winding.',
                 requirements=['use the baked triangle choices recorded per member (baked/*_TRI-HV1.npz; triangle hashes above)', 'never export quads / never let an importer choose diagonals',
                               'preserve the step-5 crossing-resolution diagonals', 'production exports carry the baked triangles downstream'],
                 tool='tools/rac/rp/halvren_rp3_v001/hv_ear_prodtri.py'),
    normals_tangents=dict(status='REQUIRED', normals='smooth angle-weighted vertex normals on the baked triangles (one smoothing group, no split normals), exported with the mesh and imported (not recomputed by the importer)',
                          tangents='MikkTSpace-compatible (Blender calc_tangents / Unreal MikkTSpace), computed on the production UV', importer='no re-triangulation'),
    LOD_HV1=dict(status='REQUIRED', rule='Decimate collapse of the baked triangles with vertex-group weights: 0 on the cuff + transition band and its one-ring (root junction protected), 0.35 on the lobe zone (auricle sheet below 30 % of the ear height), 1 elsewhere',
                 acceptance=['root-region drift 0', '50 % and 25 % LODs: 0 self-intersections, 0 non-manifold edges, 0 zero-area triangles in the ear region'], forbidden='unconstrained decimation'),
    evidence='reviews/claude-rac-rp3-halvren-ear-production-gate-report.md; reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate/')
# ---------------- creator bounds
fam = jl(FC + '/HV_ear_family_closure_record.json')['family']
R['character_creator'] = dict(
    architecture='one Halvren ear model (one topology, one HR2 root, one realization path); HE1 / HE2 / HE3 are presets; controls are domains (length, base width, taper start / extension / shoulder, rim roll height / width, projection, tilt / sweep, concha, lobe gate, upper-attachment lift), not a scalar human <-> elf interpolation; no literal elf-percentage slider',
    bounds=dict(HE1_minimum=dict(L=E.CAND['HE1']['L'], measured_length_vs_Marchfolk_pct=fam['HE1_length_vs_MF_pct']['HE1'], note='approved HVEAR4 floor, approximately Marchfolk +10-13 %; HE1 SIZE FLOOR ACCEPTED AS CANONICAL FAMILY BOUND'),
                HE2_central=dict(L=E.CAND['HE2']['L'], measured_length_vs_Marchfolk_pct=fam['HE1_length_vs_MF_pct']['HE2']),
                HE3_maximum=dict(L=E.CAND['HE3']['L'], measured_length_vs_Marchfolk_pct=fam['HE1_length_vs_MF_pct']['HE3'], note='approved HVEAR4 elf-forward extreme'),
                composite_elfward=fam['composite_elfward'], range_expansion='not authorized'),
    realization_couplings=['fuller upper helices use lift_top ~0.55 on narrow heads (c2)', 'HE3-type long ears keep the HR2 sulcus off', 'ears below L 6.3 rely on repair stage 3', 'non-frozen generated ears run repair stages 4 / 5 (sheet_fold_fix)'],
    validation='measured-domain arithmetic firewall (one-alpha R2 < 0.80 vs MF <-> Fenn / Aelari / Vael) for creator-generated ears')
# ---------------- immutable references
imm = []; base = REPO + '/'
for line in open(FC + '/immutable_hashes.txt').read().splitlines()[1:]:
    h0, rest = line.split('  ', 1); path = rest.rsplit('  ', 1)[0]
    if path.startswith('HE2+HR2'): continue
    p = path if path.startswith('/') else base + path; h1 = fsha(p); imm.append(dict(path=path, sha256=h1, unchanged=h1 == h0))
frz = []
for lab, k in (('Fenn E2', 'E2'), ('Aelari AE-E2', 'AE-E2'), ('Vael VA-E2-RI3', 'VA-E2-RI3')):
    a = np.load('%s/ref/%s_%s_branch.npz' % (SNAP, HD['c1'], k)); b = np.load('/tmp/claude-0/rt/hv/ear/%s/build/%s_%s_branch.npz' % ('ref/RI3' if k == 'VA-E2-RI3' else 'ref/FN', HD['c1'], k))
    frz.append(dict(ear=lab, V_float32_sha256=sha(b['V'].astype(np.float32).tobytes()), identical_to_production_gate_baseline=bool(np.array_equal(a['V'], b['V']) and np.array_equal(a['Q'], b['Q']))))
fr = jl(FC + '/HV_ear_family_closure_record.json')['frozen_ear_rebuild']
R['immutable_references'] = dict(files=imm, all_files_unchanged=all(x['unchanged'] for x in imm), frozen_elf_ears_on_the_common_head=frz, frozen_elf_ears_rebuild_closure=fr,
                                 he2_hr2=dict(c1=mem['HE2 c1']['read_back'], c2=mem['HE2 c2']['read_back']),
                                 covers=['Marchfolk ear reference (MPFB family base v005 blend / hm08 map / freeze record)', 'Fenn / Aelari / Vael freeze records, topology and cuff canon', 'HB2 + HF2 + HP-B heads (reference-assets r6)', 'HE2 + HR2 prior freeze state'])
# ---------------- tools
tools = ['tools/rac/rp/fenn_rp3_v001/ear_branch_lib.py', 'tools/rac/rp/fenn_rp3_v001/ear_build.py', 'tools/rac/rp/fenn_rp3_v001/ear_deform.py', 'tools/rac/rp/fenn_rp3_v001/ear_audit.py',
         'tools/rac/rp/halvren_rp3_v001/hv_ear.sh', 'tools/rac/rp/halvren_rp3_v001/hv_run_head.sh', 'tools/rac/rp/halvren_rp3_v001/hv_cuff_repair.py', 'tools/rac/rp/halvren_rp3_v001/hv_ear_domains.py',
         'tools/rac/rp/halvren_rp3_v001/hv_ear_prodtri.py', 'tools/rac/rp/halvren_rp3_v001/hv_ear_prodtri_collect.py', 'tools/rac/rp/halvren_rp3_v001/hv_ear_family_freeze_record.py']
R['tools'] = {t: fsha(base + t) for t in tools}
R['evidence'] = dict(production_gate='reviews/claude-rac-rp3-halvren-ear-production-gate-report.md', production_gate_evidence='reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate/',
                     family_closure='reviews/claude-rac-rp3-halvren-ear-family-closure-report.md', family_closure_evidence='reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/',
                     he2_hr2='reviews/claude-rac-rp3-halvren-he2-root-visual-integration-report.md')
R['accepted_residuals'] = ['residual folded / warped quads (HE 12-30 folded per mesh) = the frozen Fenn / Aelari / Vael class; deterministic, intersection-free, deformation / LOD / export clean under TRI-HV1 + LOD-HV1',
                           'shared polish items (also on the frozen HE2): cuff band crumple / back-sheet Z-kink, stamped interior relief, HR2 lobe-base crease (not reopened)',
                           'watch items: soft head-skin facets behind the root at 25 % LOD (normal LOD loss); HE1 c2 small pre-tragal nub (approved relief)']
R['carry_forward'] = [dict(id='HALVREN-CF-EAR-TRI-LOD-1', stage='UE5 / rig integration', item='use baked TRI-HV1 triangles; import normals / tangents (no re-triangulation); use LOD-HV1; one engine-side UE5 smoke test at first integration: exact imported triangle count / topology, no importer re-triangulation, normals / tangents intact, root seam intact, source / LOD silhouettes match the approved evidence',
                           blocking=False, register='specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md'),
                      dict(id='(Halvren canon)', stage='production rigging', item='bind the ear branch rigidly to the head at final skinning (as VAEL-CF-EARROOT-1)', blocking=False)]
R['frozen_status'] = dict(HE1_HVEAR4='human-forward production bound', HE2_HVEAR3='central production ear', HE3_HVEAR4='elf-forward production bound', HR2='frozen root architecture',
                          TRI_HV1='mandatory production triangulation', LOD_HV1='mandatory production LOD rule')
R['gates'] = dict(members_read_back=all(m['read_back'][s]['matches_record'] for m in mem.values() for s in m['read_back']), tri_hv1_rederived=all(m['tri_hv1_rederived_matches'] for m in mem.values()),
                  he2_hr2_prior_freeze=R['he2_hr2_prior_freeze']['c1_V_hash_in_record'] and R['he2_hr2_prior_freeze']['c2_V_hash_in_record'],
                  immutable_files=R['immutable_references']['all_files_unchanged'], frozen_elf_ears=all(x['identical_to_production_gate_baseline'] for x in frz) and all(v['max_abs_dV_cm'] == 0 and v['faces_identical'] for v in fr.values()))
R['all_gates_pass'] = all(R['gates'].values())
R['not_done'] = ['no HE1 / HE2 / HE3 geometry change', 'HR2 not reopened', 'firewall / HE1 size floor / folded-quad polish not revisited', 'no other race or Halvren work started']
json.dump(R, open(OUT + '/HALVREN_EAR_FAMILY_RP3_FREEZE.json', 'w'), indent=1, default=conv)
print('FREEZE_RECORD', R['gates'], R['all_gates_pass'], {k: (v['V_float32_sha256'][:12], v['tri_hv1_triangles_sha256'][:12]) for k, v in mem.items()})
