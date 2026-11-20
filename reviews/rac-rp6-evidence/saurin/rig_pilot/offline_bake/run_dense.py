# run_dense.py : dense between-sample audit (sa6_bake_dense.py, 0.0025 grid) of the per-body bakes listed in dense_jobs.json (offline bake order 8e3b7b4d).
#   dense_jobs.json = [[name, artifact dir relative to this folder, output tag], ...].  12 pose shards per body, WORKERS processes at a time.  Resumable.
import os, sys, json, time, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies')
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
WORKERS, NSH = int(os.environ.get('DENSE_WORKERS', '6')), 12
jobs = json.load(open(os.path.join(B, 'dense_jobs.json'))); q = []
for nm, ad, tag in jobs:
    od = os.path.join(B, 'out_dense', tag, nm); os.makedirs(od, exist_ok=True)
    for i in range(NSH):
        q.append((nm, ad, od, i))
print('dense audit:', len(jobs), 'bodies,', len(q), 'shards,', WORKERS, 'workers. Safe to close and re-run (resumes).', flush=True); t0 = time.time(); run = []; rc_all = 0
while q or run:
    while q and len(run) < WORKERS:
        nm, ad, od, i = q.pop(0); e = dict(env, DENSE_SHARD='%d/%d' % (i, NSH)); lg = open(os.path.join(od, 'w%02d.log' % i), 'a')
        run.append((subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_dense.py'), nm, BD, os.path.join(B, ad), od], env=e, stdout=lg, stderr=subprocess.STDOUT, creationflags=0x00004000), nm, i))
    time.sleep(5)
    for p in [r for r in run if r[0].poll() is not None]:
        run.remove(p); rc_all |= p[0].returncode; print(time.strftime('%H:%M:%S'), p[1], 'shard', p[2], 'rc', p[0].returncode, flush=True)
for nm, ad, tag in jobs:
    od = os.path.join(B, 'out_dense', tag, nm); subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_dense.py'), '--merge', nm, od], env=env)
open(os.path.join(B, 'timings.jsonl'), 'a').write(json.dumps(dict(body=','.join(j[0] for j in jobs), phase='dense_audit', stage='pool', host='PC', workers=WORKERS, wall_s=round(time.time() - t0, 1), rc=rc_all, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
open(os.path.join(B, 'out_dense', 'DONE.txt' if rc_all == 0 else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' rc %d\n' % rc_all)
print('DONE - tell Claude.' if rc_all == 0 else 'Stopped - tell Claude.', flush=True)
