# run_mufahi_dense.py : END_MUFAHI pass-2 repair (offline bake order 8e3b7b4d).  Pass 2 stopped at it3 with 2 sweep samples failing (trunk_twist_30 0.59166 /
#   0.59167, fit ping-pong) and a 0.0025-grid audit found 10 failing fractions of trunk_twist_30 between the 0.025 sweep samples (0.585-0.5925, 0.64-0.6475).
#   Repair = the same pass-2 recipe (pose-key floor 0.125, aligned allowance, motion gate), continued from pass-2 it0-it3 (copied, not recomputed) with
#   the dense failures as seed refit samples, up to 6 refits, and the dense audit stage (BAKE_DENSE=1) once an iteration is otherwise clean.  8 shards.
#   Output out_v2d\END_MUFAHI.  Resumable.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); nm = 'END_MUFAHI'; BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_PK_MINW='0.125', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1',
           BAKE_DENSE='1', BAKE_SEED_EXTRA=os.path.join(B, 'seed_mufahi_dense.json'))
src = os.path.join(B, 'out_v2', nm); od = os.path.join(B, 'out_v2d', nm)
if not os.path.exists(od): shutil.copytree(src, od, ignore=shutil.ignore_patterns('ckpt'))
print('END_MUFAHI dense repair. Safe to close and re-run (resumes).', flush=True); t0 = time.time()
rc = subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm), od, '6', '8'], env=env, creationflags=0x00004000)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, phase='pass2_repair_dense', stage='worker', host='PC', wall_s=round(time.time() - t0, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_v2d', 'DONE.txt' if rc == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' rc %d\n' % rc)
print('DONE - tell Claude.' if rc == 0 else 'Stopped rc %d - tell Claude.' % rc, flush=True)
