# Saurin RP6 pass 9c diagnostics (not a bake): one motion-fed pose refit from a bake iteration with several key-grid spacings, in parallel,
# each checked on that pose with the standard motion (local rule), sweep (0.025) and dense (0.0025) stages. RP6 RIG PILOT / NOT FROZEN.
#   python exp_grid_v2.py BODY POSE INIT_DIR EXTRA_JSON UNION_NPZ OUT_DIR w1,w2:beta,...   (w = key-grid spacing, beta = BAKE_MOTION_RAMP)
# Env as run_standard_v2.py (STD_REPO / STD_TOOLS / STD_LAYERS / STD_BASE). Writes OUT_DIR\<w>\{BK,MO,SW,DS}_<BODY>.json and OUT_DIR\SUMMARY.json.
import os, sys, json, time, subprocess, shutil
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B)
nm, pose, init, extra, union, od, ws = sys.argv[1:8]; ws = ws.split(',')
T = os.path.join(B, os.environ.get('STD_TOOLS', 'tools12')); BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies'); PY = sys.executable
env = dict(os.environ, BAKE_RECIPE='standard', RP6_RIG='v002', RP6_REPO=os.path.join(B, os.environ.get('STD_REPO', 'repo9')), SA_W=os.path.join(B, 'data'), RP6_WD=os.path.join(B, 'data'),
           RP6_LAYERS=os.environ.get('STD_LAYERS', 'SA_RP6_creator_layers_v006.json'), RP6_BASE_CORR=os.environ.get('STD_BASE', 'SA_RP6_correctives_v004.json'), PLEAT_GATE='1',
           PLEAT_ALLOW_UNION=union, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8',
           BAKE_PK_MINW='0.25', BAKE_DENSE='1', DENSE_STEP='0.0025', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1', BAKE_MOTION_RULE='local',
           BAKE_MOTION_REFIT='1', BAKE_MOTION_REFIT_MODE='grid', BAKE_MOTION_GRID='step', BAKE_LOCAL_MARGIN='0.03')
LOW = 0x00004000 if os.name == 'nt' else 0
os.makedirs(od, exist_ok=True)
def run(w):
    d = os.path.join(od, w.replace(':', '_r')); os.makedirs(d, exist_ok=True); shutil.copy(extra, os.path.join(d, 'extra.json')); L = open(os.path.join(d, 'log.txt'), 'a'); t = time.time()
    e = dict(env, BAKE_ONLY_POSES=pose, BAKE_INIT=os.path.join(init, 'BK_%s.json' % nm), BAKE_EXTRA=os.path.join(d, 'extra.json'), BAKE_MOTION_GRID_POSE='%s=%s' % (pose, w.split(':')[0]), BAKE_MOTION_RAMP=(w.split(':') + ['0'])[1])   # variant 'w' or 'w:ramp beta'
    steps = [('fit', [os.path.join(T, 'sa6_bake.py'), 'fit', nm, BD, d], e, 'BK_%s.json' % nm),
             ('motion', [os.path.join(T, 'sa6_bake_motion.py'), nm, BD, d, d], dict(env, MOTION_ONLY=pose), 'MO_%s.json' % nm),
             ('sweep', [os.path.join(T, 'sa6_bake_sweep.py'), nm, BD, d, d], dict(env, SWEEP_SET='all', SWEEP_ONLY=pose), 'SW_%s.json' % nm),
             ('dense', [os.path.join(T, 'sa6_bake_dense.py'), nm, BD, d, d], dict(env, DENSE_ONLY=pose), 'DS_%s.json' % nm)]
    return d, L, t, steps
jobs = {w: run(w) for w in ws}; procs = {}
summary = dict(status='RP6 RIG PILOT / NOT FROZEN', body=nm, pose=pose, init=init, extra=json.load(open(extra)), union=union, started=time.strftime('%Y-%m-%d %H:%M:%S'), variants={})
def nxt(w):
    d, L, t, steps = jobs[w]
    while steps and os.path.exists(os.path.join(d, steps[0][3])): steps.pop(0)
    if not steps: return None
    s = steps[0]; print(time.strftime('%H:%M'), w, s[0], flush=True)
    return subprocess.Popen([PY] + s[1], env=s[2], stdout=L, stderr=subprocess.STDOUT, creationflags=LOW)
for w in ws: procs[w] = nxt(w)
while any(procs.values()):
    time.sleep(30)
    for w, p in list(procs.items()):
        if p is None or p.poll() is None: continue
        if p.returncode: print(time.strftime('%H:%M'), w, 'rc', p.returncode, flush=True); procs[w] = None; continue
        procs[w] = nxt(w)
for w in ws:
    d = jobs[w][0]; r = dict(minutes=round((time.time() - jobs[w][2]) / 60, 1))
    try:
        bk = json.load(open(os.path.join(d, 'BK_%s.json' % nm))); r['converged'] = bk.get('converged')
        mo = json.load(open(os.path.join(d, 'MO_%s.json' % nm)))['poses'][pose]; r['motion'] = dict(pass_=mo['pass'], local_excess=mo['local']['worst_excess_cm'], bake=mo['bake']['frame_excursion_cm'], k_max=mo['k_max_cm'])
        sw = json.load(open(os.path.join(d, 'SW_%s.json' % nm)))['poses'][pose]; r['sweep_failing'] = [g['frac'] for g in sw['gate_failures']]
        ds = json.load(open(os.path.join(d, 'DS_%s.json' % nm)))['poses'][pose]; r['dense_bake_failing'] = ds['bake_failing']
    except Exception as ex: r['error'] = repr(ex)
    summary['variants'][w] = r
summary['ended'] = time.strftime('%Y-%m-%d %H:%M:%S'); json.dump(summary, open(os.path.join(od, 'SUMMARY.json'), 'w'), indent=1)
print(json.dumps(summary['variants'], indent=1)); print('EXP DONE - tell Claude.', flush=True)
