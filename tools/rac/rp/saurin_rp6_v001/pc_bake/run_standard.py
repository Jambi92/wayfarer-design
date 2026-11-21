# run_standard.py BODY [BODY ...] : STANDARD per-body offline bake of Saurin RP6 bodies on the bake PC (approved recipe, standards approval order c65e6c93).
#   Each body runs sa6_bake_full.py with BAKE_RECIPE=standard (pose-key half-width floor 0.25 of the full angle, dense audit 0.0025, aligned fit allowance,
#   local motion rule with motion feedback, <= 3 adaptive refits) as an independent worker, SHARDS (default 8) pose shards per stage, 1 numerical thread per
#   process, below-normal priority.  Layout (as the offline bake PC folder): tools\ = this tool folder, ..\SaurinRP6_ctrl\bodies = bodies.json + <body>.npz,
#   ..\SaurinRP6_ctrl\ctrl\<body>\BK_<body>.json/.npz = the empty-K (unbaked) artifact.  Output out_std\<body>\ (FULL_ / ACCEPT_<body>.json); resumable.
#   The effective recipe is written to out_std\<body>\RECIPE.json before the worker starts.  A new bake batch needs its own order (RP6 is NOT FROZEN).
import os, sys, json, time, subprocess
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); OUT = os.path.join(B, 'out_std')
BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies'); UA = os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl'); SHARDS = os.environ.get('SHARDS', '8')
NAMES = sys.argv[1:] or [l.strip() for l in open(os.path.join(B, 'body_list.txt')) if l.strip()]
env = dict(os.environ, BAKE_RECIPE='standard', RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'),
           RP6_LAYERS='SA_RP6_creator_layers_v004.json', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
for k in ('BAKE_PK_MINW', 'BAKE_DENSE', 'DENSE_STEP', 'BAKE_GATE_ALIGNED_ALLOW', 'BAKE_MOTION', 'BAKE_MOTION_RULE'): env.pop(k, None)   # the standard, never a stray override
ps = []
for nm in NAMES:
    od = os.path.join(OUT, nm); os.makedirs(od, exist_ok=True)
    rcp = subprocess.run([sys.executable, os.path.join(T, 'sa6_bake_full.py'), '--recipe'], env=env, capture_output=True, text=True).stdout
    open(os.path.join(od, 'RECIPE.json'), 'w').write(rcp); assert json.loads(rcp)['recipe'] == 'standard'
    lg = open(os.path.join(od, 'worker.log'), 'a')
    ps.append((nm, time.time(), subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(UA, nm), od, '3', SHARDS], env=env, stdout=lg,
                                                 stderr=subprocess.STDOUT, creationflags=0x00004000 if os.name == 'nt' else 0)))
for nm, ts, p in ps:
    rc = p.wait(); print(time.strftime('%H:%M'), nm, 'rc', rc, '%.1f h' % ((time.time() - ts) / 3600), flush=True)
    open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, recipe='standard', wall_s=round(time.time() - ts, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
print('DONE - tell Claude.', flush=True)
