# run_standard_v2.py [BODY ...] : STANDARD per-body offline bake of Saurin RP6 bodies on the rig v002 package (order 07a3f24c §4: BASE_c1, BASE_c2, END_FAHI,
#   END_MUFAHI).  Same recipe and worker as pc_bake/run_standard.py (sa6_bake_full.py, BAKE_RECIPE=standard: pose-key floor 0.25, dense 0.0025, aligned
#   allowance, local motion rule + motion feedback with the grid-step restart, local contact clearance 0.03, <= 3 adaptive refits), with:
#     RP6_RIG=v002, repo = this bundle's repo\ (rig_v002\: skeleton, weights, base correctives v003, creator layers v005), SA_W = this bundle's data\,
#     bodies = ..\SaurinRP6_ctrl\bodies (the same blend bodies), empty-K control artifacts = ctrl_v2\<body>\BK_<body>.json (baked == packaged blend v005).
#   One worker per body, SHARDS (default 8) pose shards per stage, 1 numerical thread per process, below-normal priority.  Output out_std_<package hash>\<body>\; resumable.
#   Pass 9 (base v004 / creator layers v006): STD_BASE / STD_LAYERS name the package (defaults v004 / v006; the pass-7 bakes used v003 / v005), STD_CTRL the
#   control dir (default ctrl_v3), and the fit runs with PLEAT_GATE=1 (sa6_correctives.Solver.pleat_edges: a > 90 deg dihedral change is a defect like a tear).
#   Pass 9b: the bake tools see no pose names, so the pleat gate's allowance is per body: PLEAT_ALLOW_UNION = STD_UNION\pleat_union_<body>.npz (default
#   data9b\union; sa6_pleat_union.py: the edges the body's rig v001 references pleat at any pose); the per-pose verdict is the pleat audit of the baked artifact.
#   STD_MAXIT (default 3, the standard): adaptive refits.  Pass 9b END_FAHI ended it3 with one local-motion miss (hip_flex70_xpos, 0.044 cm over the
#   allowance); a resumed run with STD_MAXIT=5 continues the same loop (it0-it3 are reused, the it3 failures feed it4).  A resumed run keeps the first
#   run_meta.json and writes its own run_meta_resume_<time>.json.
#   Writes out_std\<body>\RECIPE.json first, and out_std\run_meta.json (hardware, worker settings, tool hashes, start / end, peak memory via the workers' logs).
import os, sys, json, time, subprocess, hashlib, platform, glob
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B)
RDIR, TDIR = os.environ.get('STD_REPO', 'repo'), os.environ.get('STD_TOOLS', 'tools')   # pass 7: repo7 / tools7 (a second package state baked beside a running one)
T = os.path.join(B, TDIR)
_PK = os.path.join(B, RDIR, 'reviews', 'rac-rp6-evidence', 'saurin', 'rig_pilot', 'rig_v002')
SB, SL = os.environ.get('STD_BASE', 'SA_RP6_correctives_v004.json'), os.environ.get('STD_LAYERS', 'SA_RP6_creator_layers_v006.json')
_h = hashlib.sha256(b''.join(open(os.path.join(_PK, f), 'rb').read() for f in (SB, SL))).hexdigest()[:8]
OUT = os.path.join(B, 'out_std_' + _h); os.makedirs(OUT, exist_ok=True)   # one output dir per package state: a resumed run never mixes packages
BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies'); UN = os.path.join(B, os.environ.get('STD_UNION', os.path.join('data9b', 'union'))); UA = os.path.join(B, os.environ.get('STD_CTRL', 'ctrl_v3')); SHARDS = os.environ.get('SHARDS', '8')
NAMES = sys.argv[1:] or ['BASE_c1', 'BASE_c2', 'END_FAHI', 'END_MUFAHI']
env = dict(os.environ, BAKE_RECIPE='standard', RP6_RIG='v002', RP6_REPO=os.path.join(B, RDIR), SA_W=os.path.join(B, 'data'), RP6_WD=os.path.join(B, 'data'),
           RP6_LAYERS=SL, RP6_BASE_CORR=SB, PLEAT_GATE=os.environ.get('STD_PLEAT', '1'), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
for k in ('BAKE_PK_MINW', 'BAKE_DENSE', 'DENSE_STEP', 'BAKE_GATE_ALIGNED_ALLOW', 'BAKE_MOTION', 'BAKE_MOTION_RULE', 'BAKE_MOTION_REFIT', 'BAKE_MOTION_REFIT_MODE',
          'BAKE_MOTION_GRID', 'BAKE_LOCAL_MARGIN', 'PK_HAT_EXACT'): env.pop(k, None)   # the standard, never a stray override
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
meta = dict(status='RP6 RIG PILOT / NOT FROZEN', order='07a3f24c', rig='v002', base_correctives=SB, creator_layers=SL, pleat_gate=env['PLEAT_GATE'], pleat_union_dir=UN, node=platform.node(), cpu=platform.processor(), logical_cpus=os.cpu_count(), python=sys.version.split()[0],
            workers=len(NAMES), shards_per_stage=int(SHARDS), threads_per_process=1, priority='BELOW_NORMAL_PRIORITY_CLASS', bodies=NAMES, started=time.strftime('%Y-%m-%d %H:%M:%S'),
            tool_sha256={os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(T, 'sa6_*.py')))},
            repo=RDIR, tools=TDIR, package_sha256={os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(B, RDIR, 'reviews', 'rac-rp6-evidence', 'saurin', 'rig_pilot', 'rig_v002', '*'))) if os.path.isfile(p)})
MAXIT = os.environ.get('STD_MAXIT', '3'); meta['maxit'] = int(MAXIT)
MF = os.path.join(OUT, 'run_meta.json') if not os.path.exists(os.path.join(OUT, 'run_meta.json')) else os.path.join(OUT, 'run_meta_resume_%s.json' % time.strftime('%Y%m%d_%H%M'))
json.dump(meta, open(MF, 'w'), indent=1)
ps = []
for nm in NAMES:
    od = os.path.join(OUT, nm); os.makedirs(od, exist_ok=True)
    rcp = subprocess.run([sys.executable, os.path.join(T, 'sa6_bake_full.py'), '--recipe'], env=env, capture_output=True, text=True).stdout
    open(os.path.join(od, 'RECIPE.json'), 'w').write(rcp); r = json.loads(rcp); assert r['recipe'] == 'standard'
    lg = open(os.path.join(od, 'worker.log'), 'a'); print(time.strftime('%H:%M'), 'start', nm, flush=True)
    eb = dict(env); u = os.path.join(UN, 'pleat_union_%s.npz' % nm)
    if env['PLEAT_GATE'] == '1': assert os.path.exists(u), u; eb['PLEAT_ALLOW_UNION'] = u   # the body's v001 crease edges (sa6_pleat_union.py)
    ps.append((nm, time.time(), subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(UA, nm), od, MAXIT, SHARDS], env=eb, stdout=lg,
                                                 stderr=subprocess.STDOUT, creationflags=0x00004000 if os.name == 'nt' else 0)))
for nm, ts, p in ps:
    rc = p.wait(); print(time.strftime('%H:%M'), nm, 'rc', rc, '%.1f h' % ((time.time() - ts) / 3600), flush=True)
    open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, recipe='standard', rig='v002', wall_s=round(time.time() - ts, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
meta['ended'] = time.strftime('%Y-%m-%d %H:%M:%S'); json.dump(meta, open(MF, 'w'), indent=1)
open(os.path.join(OUT, 'ALLDONE.txt'), 'w').write(meta['ended'] + '\n'); print('ALL DONE - tell Claude.', flush=True)
