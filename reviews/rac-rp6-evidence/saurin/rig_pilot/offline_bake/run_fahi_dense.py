# run_fahi_dense.py : END_FAHI repair 2 (offline bake order 8e3b7b4d).  The w25 repair (out_v2w, pose-key floor 1/4) cleared every sampled gate and the local
#   motion gate, but the 0.0025-grid dense audit found 14 fractions between the 0.025 sweep samples where the packaged blend's defect leaks through
#   (hip_flex70_xpos 0.905-0.9175 fold, shoulder_abd45_xneg 0.98-0.985 and shoulder_abd90_xneg 0.49-0.58 contact; none added by the bake).
#   Repair = continue the w25 run (it0-it2 copied, not recomputed) with those fractions as seed refit samples and the dense audit stage (BAKE_DENSE=1),
#   same recipe (floor 0.25, aligned allowance, local motion gate), up to 6 refits, 8 shards.  Output out_v2wd\END_FAHI.  Resumable.
#   it2's motion record is replaced by its local-rule re-run (out_mo\v2L, the rule now in the driver) and its dense audit (out_dense\v2w) is placed as it2's DS stage,
#   so the driver refits from it2 instead of stopping on the first rule's 0.0015 cm verdict.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); nm = 'END_FAHI'; BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_PK_MINW='0.25', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1',
           BAKE_DENSE='1', BAKE_SEED_EXTRA=os.path.join(B, 'seed_fahi_dense.json'))
src = os.path.join(B, 'out_v2w', nm); od = os.path.join(B, 'out_v2wd', nm)
if not os.path.exists(od):
    shutil.copytree(src, od, ignore=shutil.ignore_patterns('ckpt', 'MO_*.s*of*.json'))
    shutil.copy(os.path.join(B, 'out_mo', 'v2L', nm, 'MO_%s.json' % nm), os.path.join(od, 'it2'))
    shutil.copy(os.path.join(B, 'out_dense', 'v2w', nm, 'DS_%s.json' % nm), os.path.join(od, 'it2'))
print('END_FAHI repair 2 (dense). Safe to close and re-run (resumes).', flush=True); t0 = time.time()
rc = subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm), od, '6', '8'], env=env, creationflags=0x00004000)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, phase='pass2_repair_dense', stage='worker', host='PC', wall_s=round(time.time() - t0, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_v2wd', 'DONE.txt' if rc == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' rc %d\n' % rc)
print('DONE - tell Claude.' if rc == 0 else 'Stopped rc %d - tell Claude.' % rc, flush=True)
