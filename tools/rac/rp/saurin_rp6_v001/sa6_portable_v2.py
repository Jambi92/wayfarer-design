# sa6_portable_v2.py OUTDIR : portable bundle for the rig v002 corrective rebuild on another machine (order 07a3f24c §4).  Same layout as sa6_portable.py
#   (tools/, repo/ = the read-only frozen RP5 files the loaders need + the RP6 joint placements, data/ = cage-level arrays realised here from the verified clean
#   workspace), plus: repo/.../rig_v002/ (v002 skeleton, joint placements, weights), data/W_{M,F}.npz = v002 weights, data/INIT_{M,F} (sa6_v2_init.py),
#   data/init_layer/ (19 state starting sets), data/cage_V/C_<STATE>.npy composition masks for every state (sa6_pd2_fit.comp_mask), P0.npy (canonical cage),
#   and the driver run_v2.py (base fits M + F, then the 19 state layers; resumable).  bundle_manifest.json lists every file with SHA-256.
import sys, os, json, glob, shutil, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_common as C, sa6_pd2_fit as PF
OUT = sys.argv[1]; WD = os.environ['RP6_WD']; TD = os.path.dirname(os.path.abspath(__file__))
assert not C.PORTABLE and C.have_workspace()
if os.path.exists(OUT): shutil.rmtree(OUT)
for d in ('tools', 'data/cage_V', 'data/init_layer', 'out'): os.makedirs(OUT + '/' + d)
for f in glob.glob(TD + '/sa6_*.py'): shutil.copy(f, OUT + '/tools/')
RF = ['reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/' + f for f in (
    'SA_RP5_full_cage_freeze_candidate_v001.npz', 'SA_RP5_freeze_candidate_v001_semantic_map.json', 'SA_RP5_freeze_candidate_v001_landmarks_SA-M188.json',
    'SA_RP5_freeze_candidate_v001_face_semantic.npy')] + [
    'reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_coarse_cage_design_optionb_final.pkl', 'reviews/rac-rp5-evidence/saurin/tail_module/SA_tail_module.npz',
    'reviews/rac-rp6-evidence/saurin/rig_pilot/SA_RP6_joint_placement_M_v001.json', 'reviews/rac-rp6-evidence/saurin/rig_pilot/SA_RP6_joint_placement_F_v001.json']
RF += [os.path.relpath(p, C.R) for p in sorted(glob.glob(C.RIGDIR + '/*')) if os.path.isfile(p)]
for f in RF:
    os.makedirs(os.path.dirname(OUT + '/repo/' + f), exist_ok=True); shutil.copy(C.R + '/' + f, OUT + '/repo/' + f)
for f in ('W_M.npz', 'W_F.npz', 'INIT_M.json', 'INIT_M.npz', 'INIT_F.json', 'INIT_F.npz', 'INIT_record.json'): shutil.copy(WD + '/' + f, OUT + '/data/' + f)
for f in glob.glob(WD + '/init_layer/*'): shutil.copy(f, OUT + '/data/init_layer/')
d = C.load(); np.save(OUT + '/data/cage_V/V1.npy', d['V1']); np.save(OUT + '/data/cage_V/V2.npy', d['V2']); np.save(OUT + '/data/cage_V/P0.npy', PF.V1C)
z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Fd = w['f'].astype(np.int64); states = []
for p in sorted(glob.glob(C.W + '/cr_*.npy')):
    nm = os.path.basename(p)[3:-4]; VB = np.load(p).astype(float); np.save(OUT + '/data/cage_V/S_%s.npy' % nm, (z['bc'][:, :, None] * VB[Fd[z['tri']]]).sum(1))
    R, _ = PF.state_rig(nm); np.save(OUT + '/data/cage_V/C_%s.npy' % nm, PF.comp_mask(nm, R)); states.append(nm); print(nm, flush=True)
shutil.copy(TD + '/portable/run_v2.py', OUT + '/run_v2.py'); shutil.copy(TD + '/portable/START_V2.bat', OUT + '/START_V2.bat')
man = dict(status='RP6 RIG PILOT / NOT FROZEN', purpose='rig v002 base + creator-state corrective rebuild off-session (order 07a3f24c)', rig_version=C.RIGV, states=states,
           source_workspace_hashes={os.path.basename(p): C.sha(p) for p in sorted(glob.glob(C.W + '/cr_*.npy'))}, files={})
for root, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(root, f); man['files'][os.path.relpath(p, OUT).replace(os.sep, '/')] = dict(sha256=C.sha(p), bytes=os.path.getsize(p))
json.dump(man, open(OUT + '/bundle_manifest.json', 'w'), indent=1); print(len(man['files']), 'files', sum(v['bytes'] for v in man['files'].values()) / 1e6, 'MB')
