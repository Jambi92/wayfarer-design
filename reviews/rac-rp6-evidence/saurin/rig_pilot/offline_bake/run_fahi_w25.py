# run_fahi_w25.py : END_FAHI repair of pass 2 (offline bake order 8e3b7b4d).  Pass 2 END_FAHI cleared every sample gate (31 -> 0, integrity clean) but the
#   motion gate fails on hip_flex70_xpos: 0.6205 vs limit 0.6183 cm per frame (packaged blend's own excursion, 67.67-70 deg, vertex 41489, same frame/vertex).
#   The full-flexion key PK@1.0 was floored to 8.75 deg (1/8 of 70 deg) because adaptive samples sat next to it.  Repair = the same pass-2 recipe from v004 with the
#   pose-key floor at 1/4 of the full angle (BAKE_PK_MINW=0.25, the standard fraction spacing), 8 shards.  Output out_v2w\END_FAHI.  Resumable.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); nm = 'END_FAHI'; BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_PK_MINW='0.25', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1')
od = os.path.join(B, 'out_v2w', nm); os.makedirs(od, exist_ok=True)
if not os.path.exists(os.path.join(od, 'unbaked')): shutil.copytree(os.path.join(B, 'out', nm, 'unbaked'), os.path.join(od, 'unbaked'), ignore=shutil.ignore_patterns('ckpt'))
print('END_FAHI repair (pose-key floor 1/4). Safe to close and re-run (resumes).', flush=True); t0 = time.time()
rc = subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm), od, '3', '8'], env=env, creationflags=0x00004000)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, phase='pass2_repair_w25', stage='worker', host='PC', wall_s=round(time.time() - t0, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_v2w', 'DONE.txt' if rc == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' rc %d\n' % rc)
print('DONE - tell Claude.' if rc == 0 else 'Stopped rc %d - tell Claude.' % rc, flush=True)
