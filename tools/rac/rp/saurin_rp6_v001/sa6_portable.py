# sa6_portable.py OUTDIR [CKPTDIR] : portable bundle for running the RP6 creator-state corrective layer fits (sa6_pd2_fit.py) on another machine.
#   No dense arrays leave the session: the cage-level rest bodies are realised HERE from the verified clean workspace (cr_<STATE>.npy through the frozen
#   barycentric embedding, exactly as sa6_pd2_fit.state_rig does) and shipped as data/cage_V/{V1,V2,S_<STATE>}.npy (, float64, cage vertex order).
#   Bundle = tools (sa6_*.py), the read-only frozen RP5 files the loaders need (hash-listed), RP6 joint placements, production weights + correctives,
#   resumable checkpoints, a driver (run_fits.py) and a Windows launcher (RUN_FITS.bat).  bundle_manifest.json lists every file with SHA-256.
import sys, os, json, glob, shutil, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C
OUT = sys.argv[1]; CK = sys.argv[2] if len(sys.argv) > 2 else None; WD = os.environ.get('RP6_WD', '/tmp/claude-0/rp6'); TD = os.path.dirname(os.path.abspath(__file__))
assert not C.PORTABLE and C.have_workspace(), 'build from the verified clean workspace'
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + '/tools'); os.makedirs(OUT + '/data'); os.makedirs(OUT + '/out/ckpt')
for f in glob.glob(TD + '/sa6_*.py'): shutil.copy(f, OUT + '/tools/')
REPO_FILES = ['reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/' + f for f in (
    'SA_RP5_full_cage_freeze_candidate_v001.npz', 'SA_RP5_freeze_candidate_v001_semantic_map.json', 'SA_RP5_freeze_candidate_v001_landmarks_SA-M188.json',
    'SA_RP5_freeze_candidate_v001_face_semantic.npy')] + [
    'reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/SA_coarse_cage_design_optionb_final.pkl', 'reviews/rac-rp5-evidence/saurin/tail_module/SA_tail_module.npz',
    'reviews/rac-rp6-evidence/saurin/rig_pilot/SA_RP6_joint_placement_M_v001.json', 'reviews/rac-rp6-evidence/saurin/rig_pilot/SA_RP6_joint_placement_F_v001.json']
for f in REPO_FILES:
    os.makedirs(os.path.dirname(OUT + '/repo/' + f), exist_ok=True); shutil.copy(C.R + '/' + f, OUT + '/repo/' + f)
for f in ('W_M.npz', 'W_F.npz', 'CF_M.json', 'CF_M.npz', 'CF_F.json', 'CF_F.npz'): shutil.copy(WD + '/' + f, OUT + '/data/' + f)
d = C.load(); z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Fd = w['f'].astype(np.int64)
cv = dict(V1=d['V1'], V2=d['V2']); states = []
for p in sorted(glob.glob(C.W + '/cr_*.npy')):
    nm = os.path.basename(p)[3:-4]; VB = np.load(p).astype(float); cv['S_' + nm] = (z['bc'][:, :, None] * VB[Fd[z['tri']]]).sum(1); states.append(nm)
os.makedirs(OUT + '/data/cage_V')
for k, v in cv.items(): np.save(OUT + '/data/cage_V/%s.npy' % k, v)
if CK:
    for f in glob.glob(CK + '/CF_ckpt_*'): shutil.copy(f, OUT + '/out/ckpt/')
    for f in glob.glob(os.path.dirname(CK.rstrip('/')) + '/CF_state_*'): shutil.copy(f, OUT + '/out/')   # states already finished
shutil.copy(TD + '/portable/run_fits.py', OUT + '/run_fits.py'); shutil.copy(TD + '/portable/RUN_FITS.bat', OUT + '/RUN_FITS.bat')
man = dict(status='RP6 RIG PILOT / NOT FROZEN', purpose='creator-state corrective layer fits (sa6_pd2_fit.py) off-session', states=states,
           source_workspace_hashes={os.path.basename(p): C.sha(p) for p in sorted(glob.glob(C.W + '/cr_*.npy'))}, files={})
for root, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(root, f); man['files'][os.path.relpath(p, OUT).replace(os.sep, '/')] = dict(sha256=C.sha(p), bytes=os.path.getsize(p))
json.dump(man, open(OUT + '/bundle_manifest.json', 'w'), indent=1); print(len(man['files']), 'files', sum(v['bytes'] for v in man['files'].values()) / 1e6, 'MB')
