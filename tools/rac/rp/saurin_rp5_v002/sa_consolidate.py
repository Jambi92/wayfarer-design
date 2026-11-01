# sa_consolidate.py APPROVED_CAGE.npz CLEAN_WS OUTDIR : Saurin RP5 final consolidation (order cd87d9c §1-§6). NO geometry development.
#   1. CLEAN WORKSPACE: CLEAN_WS is created empty and filled only with hash-verified inputs:
#        canonical W2I6 base + SA-F188 realization (sha recorded in the W2I6 closure / derivation records), SA_RP5_WORK_v001 REBUILT from the canonical
#        arrays + the committed thigh delta (array hashes must equal the recorded working_array_sha256), landmarks / regions / accepted tail module
#        copied from the repository (sha recorded), creator-state realizations (validation inputs only; hashes recorded).
#   2. CLEAN REBUILD of the approved cage: the approved authored cage is defined by its face list Q + barycentric embedding (base triangle, barycentrics)
#        on the canonical face list + the accepted tail module block. Geometry is re-derived from the rebuilt working source for c1 (SA-M188) and
#        c2 (SA-F188); the tail block is re-derived from the accepted module. Compared with every array of the approved npz (exact equality required for
#        topology / embedding / labels; geometry difference quantified).
#   3. FREEZE-CANDIDATE npz = the approved arrays (bit-identical) + provenance fields; written to OUTDIR, re-read from disk and re-compared.
import sys, os, json, hashlib, shutil, subprocess, numpy as np
AP, WS, OUT = sys.argv[1:4]; REPO = '/home/claude/wayfarer-design'; STAGE = '/tmp/claude-0/rt/sa'
EV = REPO + '/reviews/rac-rp5-evidence/saurin'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def ash(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
rec = dict(order='reviews/chatgpt-rac-rp5-saurin-final-consolidation-freeze-readiness-order.md (cd87d9c)', approved_commit='2ee75ae1845a223f3c8b8b9a5abfa10608f06b27',
           repo_commit=subprocess.run(['git', '-C', REPO, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(), tool=os.path.abspath(__file__), checks={})
ok = True
def check(name, cond, **info):
    global ok
    rec['checks'][name] = dict(ok=bool(cond), **info); ok &= bool(cond); print(('PASS ' if cond else 'FAIL ') + name, json.dumps(info)[:300], flush=True)
# ---- 1. clean workspace
if os.path.exists(WS): shutil.rmtree(WS)
for d in ('src', 'work', 'lm', 'tail'): os.makedirs(WS + '/' + d)
der = json.load(open(EV + '/full_cage/thigh/SA_RP5_WORK_v001_derivation.json'))
for f, h in der['canonical_inputs'].items():
    shutil.copy2(STAGE + '/src/' + f, WS + '/src/' + f); check('canonical input ' + f, sha(WS + '/src/' + f) == h, sha256=sha(WS + '/src/' + f), recorded=h)
for f in ('saurin_w2_final_surface_delta.npz', 'saurin_w2_seeds.npy'):                         # detail-layer inputs (canonical W2I6 closure files)
    if os.path.exists(STAGE + '/src/' + f): shutil.copy2(STAGE + '/src/' + f, WS + '/src/' + f)
b = np.load(WS + '/src/saurin_w2_final_base.npz'); fr = np.load(WS + '/src/saurin_w2_SA-F188_realization.npz')
check('canonical arrays', ash(b['v']) == der['canonical_array_sha256']['v_M'] and ash(fr['v']) == der['canonical_array_sha256']['v_F'] and ash(b['f']) == der['canonical_array_sha256']['f'])
dl = np.load(EV + '/full_cage/thigh/SA_RP5_WORK_v001_delta.npz'); vM = b['v'].copy(); vF = fr['v'].copy(); vM[dl['idx']] = dl['v_M']; vF[dl['idx']] = dl['v_F']
np.savez_compressed(WS + '/work/SA_RP5_WORK_v001.npz', v_M=vM, v_F=vF, f=b['f'])
wa = {k: ash(a) for k, a in (('v_M', vM), ('v_F', vF), ('f', b['f']))}
check('working source rebuilt (canonical + committed thigh delta)', wa == der['working_array_sha256'], arrays=wa, staged_file_sha=sha(STAGE + '/work/SA_RP5_WORK_v001.npz'))
for f in ('SA-M188_landmarks.json', 'SA-M188_regions.npz'): shutil.copy2(EV + '/landmarks/' + f, WS + '/lm/' + f)
for f in ('SA_tail_module.npz', 'SA_tail_module.json'): shutil.copy2(EV + '/tail_module/' + f, WS + '/tail/' + f)
check('accepted tail module file', sha(WS + '/tail/SA_tail_module.npz').startswith('559565cc'), sha256=sha(WS + '/tail/SA_tail_module.npz'))
crs = {}
for f in sorted(os.listdir(STAGE)):
    if f.startswith('cr_') and f.endswith('.npy'): shutil.copy2(STAGE + '/' + f, WS + '/' + f); crs[f] = sha(WS + '/' + f)
rec['clean_workspace'] = dict(path=WS, files={os.path.relpath(os.path.join(r, f), WS): sha(os.path.join(r, f)) for r, _, fs in os.walk(WS) for f in fs}, creator_states=crs)
# ---- 2. clean rebuild from the approved authored embedding
z = np.load(AP); A = {k: z[k] for k in z.files}; rec['approved'] = dict(file=AP, sha256=sha(AP), arrays=sorted(A))
Q = A['Q']; tri = A['tri']; bc = A['bc']; nb = int(A['n_body']); F = b['f'].astype(np.int64)
TM = np.load(WS + '/tail/SA_tail_module.npz'); mapv = np.r_[A['tail_ring'], nb + np.arange(len(TM['V']) - 128)]
V1 = (bc[:, :, None] * vM.astype(float)[F[tri]]).sum(1); V2 = (bc[:, :, None] * vF.astype(float)[F[tri]]).sum(1)
dV = np.abs(V1 - A['V']).max(); dT = np.abs(V1[mapv] - TM['V']).max(); dT2 = np.abs(A['V'][mapv] - TM['V']).max()
check('c1 geometry rebuilt == approved V', dV < 1e-9, max_abs_diff_cm=float(dV))
check('tail module block == accepted module (approved and rebuilt)', dT < 1e-9 and dT2 < 1e-9, rebuilt_cm=float(dT), approved_cm=float(dT2))
qs = set(map(tuple, np.sort(mapv[TM['Q']], 1))); tq = set(map(tuple, np.sort(Q[A['qlab'].astype(str) == 'tail'], 1)))
check('tail module faces', qs == tq, module_quads=len(TM['Q']))
# manifold / orientation / counts
e = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); eu, c = np.unique(e, axis=0, return_counts=True)
de = np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2); chi = len(A['V']) - len(eu) + len(Q)
check('counts', len(A['V']) == 190948 and len(Q) == 190946, verts=int(len(A['V'])), quads=int(len(Q)))
check('closed 2-manifold, consistently oriented, chi 2, 100 % quads', c.min() == 2 and c.max() == 2 and len(np.unique(de, axis=0)) == len(de) and chi == 2 and Q.shape[1] == 4, chi=int(chi))
check('all vertices used, no degenerate quad', len(np.unique(Q)) == len(A['V']) and (np.array([len(set(q)) for q in Q]) == 4).all())
topo = ash(Q.astype(np.int64)); check('topology hash', topo == '255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49', topology_sha256=topo)
check('c1 / c2 share face list and vertex order (one Q, one embedding)', V2.shape == V1.shape, c1_c2_max_vertex_offset_cm=float(np.linalg.norm(V2 - V1, axis=1).max()))
# ---- 3. freeze-candidate npz: approved arrays bit-identical + provenance
os.makedirs(OUT, exist_ok=True); cand = OUT + '/SA_RP5_full_cage_freeze_candidate_v001.npz'
prov = dict(status='FREEZE CANDIDATE / NOT FROZEN', approved_commit=rec['approved_commit'], approved_file='reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_RP5_full_cage_optionb_final.npz',
            approved_sha256=rec['approved']['sha256'], topology_sha256=topo, architecture='Option B local hand / foot density', race='Saurin', stage='RP5')
np.savez_compressed(cand, **A, provenance=np.array(json.dumps(prov)))
z2 = np.load(cand); same = all(np.array_equal(z2[k], A[k]) and z2[k].dtype == A[k].dtype for k in A)
check('candidate npz re-read == approved arrays (bit-identical, all %d arrays)' % len(A), same, candidate_sha256=sha(cand))
V1c = (z2['bc'][:, :, None] * vM.astype(float)[F[z2['tri']]]).sum(1); V2c = (z2['bc'][:, :, None] * vF.astype(float)[F[z2['tri']]]).sum(1)
check('candidate c1 / c2 geometry == rebuild', np.array_equal(V1c, V1) and np.array_equal(V2c, V2))
np.savez_compressed(OUT + '/SA_RP5_freeze_candidate_v001_barycentric_map.npz', base_face=z2['tri'], barycentric=z2['bc'], n_body=z2['n_body'], tail_ring=z2['tail_ring'],
                    face_list_note=np.array('canonical W2I6 base face list (saurin_w2_final_base.npz f, sha256 %s)' % der['canonical_array_sha256']['f']))
bm = np.load(OUT + '/SA_RP5_freeze_candidate_v001_barycentric_map.npz'); check('barycentric map == candidate embedding', np.array_equal(bm['base_face'], A['tri']) and np.array_equal(bm['barycentric'], A['bc']))
rec['candidate'] = dict(npz=os.path.basename(cand), sha256=sha(cand), barycentric_map=sha(OUT + '/SA_RP5_freeze_candidate_v001_barycentric_map.npz'), topology_sha256=topo,
                        c1_geometry_sha256=ash(V1), c2_geometry_sha256=ash(V2))
rec['verdict'] = 'PASS' if ok else 'FAIL'
json.dump(rec, open(OUT + '/consolidation_rebuild.json', 'w'), indent=1); print('REBUILD', rec['verdict'])
