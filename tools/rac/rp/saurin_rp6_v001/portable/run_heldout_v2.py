# run_heldout_v2.py [WORKERS] : held-out recheck of the earlier bake benchmark on the rig v002 pass-7 package (order 07a3f24c §4: "recheck affected held-out
#   intermediate and mixed-body cases").  The 18 benchmark bodies (bake feasibility v001: intermediate c1-/c2- blends, BK-X2a/b/c, BK-X3), each baked with
#   sa6_bake_full.py from its empty-K control (= packaged blend v005): unbaked suite, fit, then per iteration EV (34 x 4) + GT (56 special gates x 4) +
#   SW (full-suite sweep) + GS (gate transitions), <= 3 adaptive refits - the benchmark's stages (fit / eval / full-suite sweep / special gates) with the
#   standard fit settings (pose-key floor, aligned allowance).  Not run here: the motion and dense stages (BAKE_MOTION=0, BAKE_DENSE=0) - a held-out body
#   is feasibility evidence, not an accepted artifact (an artifact submitted as passing runs run_standard_v2.py).
#   repo7\ / tools7\ (pass-7 package), bodies_ho\, ctrl_ho\<body>\BK_<body>.json; one process per body (1 shard), single-threaded, below-normal priority,
#   resumable.  Output out_ho_<package hash>\<body>\ ; timings out_ho_*\timings.jsonl.
import os, sys, json, time, subprocess, hashlib, platform, glob
B = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(B, 'tools7'); R = os.path.join(B, 'repo7')
_PK = os.path.join(R, 'reviews', 'rac-rp6-evidence', 'saurin', 'rig_pilot', 'rig_v002')
_h = hashlib.sha256(b''.join(open(os.path.join(_PK, f), 'rb').read() for f in ('SA_RP6_correctives_v003.json', 'SA_RP6_creator_layers_v005.json'))).hexdigest()[:8]
OUT = os.path.join(B, 'out_ho_' + _h); os.makedirs(OUT, exist_ok=True); BD = os.path.join(B, 'bodies_ho'); UA = os.path.join(B, 'ctrl_ho')
NAMES = ['c1-MUHI@0.625', 'c1-MUFAHI@0.625', 'c1-FAHI@0.9375', 'c1-MUFAHI@0.875', 'c1-T80@0.375', 'c1-M208-B@0.75', 'c2-F-N@0.25', 'c2-F-N@0.40', 'c1-M208-B@0.25',
         'BK-X2a', 'BK-X2b', 'BK-X2c', 'BK-X3', 'c1-MUHI@0.375', 'c1-FAHI@0.375', 'c1-FAHI@0.625', 'c1-MUFAHI@0.375', 'c1-MUFAHI@0.0625']
nw = int(sys.argv[1]) if len(sys.argv) > 1 else 8
if len(sys.argv) > 2 and sys.argv[2] == 'rev': NAMES = NAMES[::-1]   # a second runner works from the other end; RUNNING.lock keeps two runners off one body
env = dict(os.environ, BAKE_RECIPE='standard', BAKE_MOTION='0', BAKE_DENSE='0', RP6_RIG='v002', RP6_REPO=R, SA_W=os.path.join(B, 'data'), RP6_WD=os.path.join(B, 'data'),
           RP6_LAYERS='SA_RP6_creator_layers_v005.json', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
json.dump(dict(runner=('rev' if len(sys.argv) > 2 else 'fwd'), status='RP6 RIG PILOT / NOT FROZEN', order='07a3f24c', rig='v002', node=platform.node(), logical_cpus=os.cpu_count(), workers=nw, bodies=NAMES,
               started=time.strftime('%Y-%m-%d %H:%M:%S'), stages='unbaked + fit + EV/GT/SW/GS per iteration, MAXIT 3, 1 shard; motion / dense off',
               tool_sha256={os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(T, 'sa6_*.py')))},
               package_sha256={os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(_PK, '*'))) if os.path.isfile(p)}), open(os.path.join(OUT, 'run_meta_%s.json' % ('rev' if len(sys.argv) > 2 else 'fwd')), 'w'), indent=1)
todo = [n for n in NAMES if not os.path.exists(os.path.join(OUT, n, 'FULL_DONE.txt'))]; run = {}
def locked(n):
    lk = os.path.join(OUT, n, 'RUNNING.lock')
    if os.path.exists(lk): return True
    os.makedirs(os.path.join(OUT, n), exist_ok=True); open(lk, 'w').write('%d %s\n' % (os.getpid(), time.strftime('%Y-%m-%d %H:%M:%S'))); return False
print('Saurin RP6 v002 held-out recheck: %d bodies, %d at a time. Safe to close and re-run (resumes).' % (len(todo), nw), flush=True)
while todo or run:
    while todo and len(run) < nw:
        n = todo.pop(0)
        if locked(n): continue
        od = os.path.join(OUT, n); os.makedirs(od, exist_ok=True); lg = open(os.path.join(od, 'worker.log'), 'a')
        run[n] = (subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_full.py'), n, BD, os.path.join(UA, n), od, '3', '1'], env=env, stdout=lg, stderr=subprocess.STDOUT,
                                   creationflags=0x00004000 if os.name == 'nt' else 0), lg, time.time()); print(time.strftime('%H:%M'), 'start', n, flush=True)
    time.sleep(30)
    for n in list(run):
        p, lg, ts = run[n]
        if p.poll() is None: continue
        lg.close(); del run[n]
        try: os.remove(os.path.join(OUT, n, 'RUNNING.lock'))
        except OSError: pass
        if p.returncode == 0: open(os.path.join(OUT, n, 'FULL_DONE.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=n, rc=p.returncode, wall_s=round(time.time() - ts, 1), end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
        print(time.strftime('%H:%M'), n, 'rc', p.returncode, '%.1f h' % ((time.time() - ts) / 3600), '- %d left' % (len(todo) + len(run)), flush=True)
print('ALL DONE - tell Claude.', flush=True)
