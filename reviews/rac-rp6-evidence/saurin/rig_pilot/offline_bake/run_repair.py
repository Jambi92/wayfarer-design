# run_repair.py : END_MUFAHI repairability check (offline bake order 8e3b7b4d) -- OUTSIDE the order's 3-refit cap, reported separately.
#   The official run (out/END_MUFAHI) stopped after 3 refits with trunk_twist_30 @0.61667 / 0.625 (1 rig-owned contact, vertex 4524) remaining: the fit's
#   composition allowance (composition zone & plain-LBS contact) is wider than the gate's ownership rule (also within 1.0 cm of a pre-rig defect point), so the
#   fit never saw that contact.  This copies the official iterations to out_repair/END_MUFAHI and runs ONE more refit (it4) with BAKE_GATE_ALIGNED_ALLOW=1
#   (fit allowance = gate ownership; gates unchanged), then the full suite (EV 34x4, GT 50x4, full sweep, gate sweep), integrity, RP5-literal, before/after.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); nm = 'END_MUFAHI'
src = os.path.join(B, 'out', nm); dst = os.path.join(B, 'out_repair', nm)
if not os.path.exists(dst): shutil.copytree(src, dst, ignore=shutil.ignore_patterns('ckpt'))
BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies'); UA = os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm)
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_GATE_ALIGNED_ALLOW='1')
print('END_MUFAHI repairability check: one refit beyond the cap with the gate-aligned fit allowance. Safe to close and re-run (resumes).', flush=True)
t0 = time.time(); lg = open(os.path.join(B, 'out_repair', 'worker_%s.log' % nm), 'a')
rc = subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, UA, dst, '4', '8'], env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=0x00004000)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, stage='repair_worker', host='PC', wall_s=round(time.time() - t0, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_repair', 'DONE.txt' if rc == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n'); print('DONE - tell Claude.' if rc == 0 else 'Stopped rc %d - tell Claude.' % rc, flush=True)
