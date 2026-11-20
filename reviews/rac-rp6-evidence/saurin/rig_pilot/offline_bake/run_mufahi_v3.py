# run_mufahi_v3.py : END_MUFAHI repair 2 (offline bake order 8e3b7b4d).  The dense repair (out_v2d) cleared every sample, sweep and dense gate (it4 dense:
#   trunk_twist_30 clean; it5 refit cleared hip_flex70_xpos 0.2125), but the LOCAL motion gate fails on shoulder_abd90_xneg: the full-abduction pose key
#   PK008 (2.77 cm, width 11.25 deg = 1/8 of 90 deg) moves the trunk 0.73 cm in one frame (78.75-81.75 deg; bake 0.5033 cm vs allowance 0.50).
#   Repair = the END_FAHI repair recipe from v004: pose-key floor 1/4 of the full angle (BAKE_PK_MINW=0.25), aligned allowance, motion gate, plus the dense
#   audit stage (BAKE_DENSE=1) and every dense failure found so far as seed refit samples.  Up to 6 refits, 8 shards.  Output out_v3\END_MUFAHI.  Resumable.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); nm = 'END_MUFAHI'; BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_PK_MINW='0.25', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1',
           BAKE_DENSE='1', BAKE_SEED_EXTRA=os.path.join(B, 'seed_mufahi_v3.json'))
od = os.path.join(B, 'out_v3', nm); os.makedirs(od, exist_ok=True)
if not os.path.exists(os.path.join(od, 'unbaked')): shutil.copytree(os.path.join(B, 'out', nm, 'unbaked'), os.path.join(od, 'unbaked'), ignore=shutil.ignore_patterns('ckpt'))
print('END_MUFAHI repair 2 (pose-key floor 1/4 + dense audit). Safe to close and re-run (resumes).', flush=True); t0 = time.time()
rc = subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm), od, '6', '8'], env=env, creationflags=0x00004000)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, phase='pass2_repair_v3', stage='worker', host='PC', wall_s=round(time.time() - t0, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_v3', 'DONE.txt' if rc == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' rc %d\n' % rc)
print('DONE - tell Claude.' if rc == 0 else 'Stopped rc %d - tell Claude.' % rc, flush=True)
