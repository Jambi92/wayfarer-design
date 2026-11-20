# run_v2.py : offline bake, second pass (offline bake order 8e3b7b4d).  The first pass (out/) passed every gate on BASE_c1 / BASE_c2 / END_FAHI, but the
#   adaptive refits created pose keys from sweep samples 0.025 / 0.25 deg apart, so their tents were 0.25-1.75 deg wide: 0.2-1.8 cm switched on inside one
#   30 fps frame (motion pops, END_FAHI / END_MUFAHI).  Pass 2, same roster, same suite, from v004 again, with:
#     BAKE_PK_MINW=0.125            pose-key tent half-width >= 1/8 of the pose's full angle (the coarse sweep spacing)
#     BAKE_GATE_ALIGNED_ALLOW=1     fit composition allowance = the gate's ownership rule (END_MUFAHI trunk_twist_30 vertex 4524, 1.40 cm from pre-rig points)
#     MO stage                      motion gate (sa6_bake_motion.py) on every iteration
#   Unbaked references are copied from out/ (same body, same artifact, same suite).  4 bodies x 4 shards in parallel.  Resumable: close and re-run any time.
import os, sys, json, time, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools')
NAMES = ['BASE_c1', 'BASE_c2', 'END_FAHI', 'END_MUFAHI']; BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', BAKE_PK_MINW='0.125', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1')
os.makedirs(os.path.join(B, 'out_v2'), exist_ok=True)
for nm in NAMES:
    u0 = os.path.join(B, 'out', nm, 'unbaked'); u1 = os.path.join(B, 'out_v2', nm, 'unbaked')
    if not os.path.exists(u1): shutil.copytree(u0, u1, ignore=shutil.ignore_patterns('ckpt'))
print('Offline bake pass 2 (4 bodies in parallel). Safe to close and re-run (resumes).', flush=True)
t0 = time.time(); ps = {}
for nm in NAMES:
    lg = open(os.path.join(B, 'out_v2', 'worker_%s.log' % nm), 'a')
    ps[nm] = (subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl', nm), os.path.join(B, 'out_v2', nm), '3', '4'],
                               env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=0x00004000), time.time())
rcs = {}
for nm, (p, ts) in ps.items():
    rcs[nm] = p.wait(); open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, phase='pass2', stage='worker', host='PC', wall_s=round(time.time() - ts, 1), rc=rcs[nm], end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(phase='pass2', stage='all', host='PC', wall_s=round(time.time() - t0, 1), end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
ok = not any(rcs.values()); open(os.path.join(B, 'out_v2', 'DONE.txt' if ok else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + json.dumps(rcs) + '\n')
print('DONE - tell Claude.' if ok else 'Stopped %s - tell Claude.' % rcs, flush=True)
