# run_v2.py [WORKERS] : rig v002 corrective rebuild from this portable bundle (order 07a3f24c §4; bundle by sa6_portable_v2.py).
#   Jobs: base c1 / c2 (sa6_fit.py, INIT = data/INIT_<c>, ROUNDS 6) and the 19 creator-state layers (sa6_pd2_fit.py, INIT_LAYER = data/init_layer,
#   FRACS 1.0,0.75,0.5,0.25, COMP_MASK 1, SEGBULGE 1, ROUNDS 8) -- independent, run in parallel, one process each, single-threaded numpy, below-normal
#   priority.  Resumable: finished jobs are skipped; a killed state resumes from its checkpoint, a killed base fit restarts from its last partial save.
#   Results: out/CF_<c>.json/.npz, out/layers/CF_state_<STATE>.json/.npz, logs in out/logs, out/jobs.json (start / end / exit / wall time), ALLDONE.txt.
import os, sys, time, json, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out'); LO = os.path.join(OUT, 'layers'); os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True); os.makedirs(LO, exist_ok=True)
man = json.load(open(os.path.join(B, 'bundle_manifest.json')))
ORDER = ['MUFAHI', 'MUHI', 'FAHI', 'M208-B', 'BRD', 'B-T80', 'F-N', 'M168', 'MIN', 'LT90', 'T80', 'T55', 'DSP-LOW', 'DSP-HIGH', 'ORB-8', 'ORB+3', 'RDG0.90', 'RDG1.30', 'NAR']
ncpu = os.cpu_count() or 2; nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, ncpu - 2)
D = os.path.join(B, 'data'); T = os.path.join(B, 'tools')
env0 = dict(os.environ, RP6_RIG='v002', RP6_REPO=os.path.join(B, 'repo'), SA_W=D, RP6_WD=D, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
# passes: data/INIT<n>_<c>.json (base) and data/init_layer<n>/ (states) -> out/CF<n>_<c>.json, out/layers<n>/ ; the highest n present runs.
#   pass 1 = INIT / init_layer (sa6_v2_init.py); pass 3 = hat fraction keys + duplicate keys merged + girdle elevation-only + solver no-worse guard (07a3f24c)
PASS = max([n for n in range(2, 10) if os.path.exists(os.path.join(D, 'INIT%d_M.json' % n))] or [1])
BN = ('CF%d_%%s.json' % PASS) if PASS > 1 else 'CF_%s.json'
LP = max([n for n in range(2, 10) if os.path.isdir(os.path.join(D, 'init_layer%d' % n))] or [1])
LI = os.path.join(D, 'init_layer%d' % LP if LP > 1 else 'init_layer'); LO = os.path.join(OUT, 'layers%d' % LP if LP > 1 else 'layers'); os.makedirs(LO, exist_ok=True)
def done_base(c):
    p = os.path.join(OUT, BN % c); return os.path.exists(p) and 'partial' not in json.load(open(p))['status']
jobs = []
for c in 'MF':
    if done_base(c): continue
    part = os.path.join(OUT, BN % c); ini = part if os.path.exists(part) else os.path.join(D, ('INIT%d_%%s.json' % PASS if PASS > 1 else 'INIT_%s.json') % c)
    jobs.append(('base_' + c, [sys.executable, os.path.join(T, 'sa6_fit.py'), c, part, os.path.join(D, 'W_%s.npz' % c)], dict(env0, INIT=ini, ROUNDS='6')))
for s in ORDER:
    if s in man['states'] and not os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)):
        jobs.append((s, [sys.executable, os.path.join(T, 'sa6_pd2_fit.py'), s, LO], dict(env0, INIT_LAYER=LI, FRACS='1.0,0.75,0.5,0.25', COMP_MASK='1', SEGBULGE='1', ROUNDS='8')))
JR = os.path.join(OUT, 'jobs%s.json' % ('_p%d' % max(PASS, LP) if max(PASS, LP) > 1 else '')); rec = json.load(open(JR)) if os.path.exists(JR) else {}
print('Saurin RP6 rig v002 rebuild: %d jobs, %d at a time (%d CPUs). Leave this window open; safe to close and re-run later.' % (len(jobs), nw, ncpu), flush=True)
flags = 0x00004000 if os.name == 'nt' else 0; run = {}; fails = {}; t0 = time.time()
while jobs or run:
    while jobs and len(run) < nw:
        n, cmd, env = jobs.pop(0); lg = open(os.path.join(OUT, 'logs', ('p%d_' % max(PASS, LP) if max(PASS, LP) > 1 else '') + n + '.log'), 'a')
        run[n] = (subprocess.Popen(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg, time.time())
        rec.setdefault(n, []).append(dict(start=time.strftime('%Y-%m-%d %H:%M:%S'))); json.dump(rec, open(JR, 'w'), indent=1); print(time.strftime('%H:%M'), 'started', n, flush=True)
    time.sleep(20)
    for n in list(run):
        p, lg, ts = run[n]
        if p.poll() is not None:
            lg.close(); del run[n]; rec[n][-1].update(end=time.strftime('%Y-%m-%d %H:%M:%S'), exit=p.returncode, wall_h=round((time.time() - ts) / 3600, 3)); json.dump(rec, open(JR, 'w'), indent=1)
            if p.returncode: fails[n] = p.returncode
            print(time.strftime('%H:%M'), 'finished' if not p.returncode else 'FAILED (see out/logs/%s.log)' % n, n, '- %d left' % (len(jobs) + len(run)), flush=True)
ok = all(done_base(c) for c in 'MF') and all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in ORDER if s in man['states'])
if ok: open(os.path.join(OUT, 'ALLDONE.txt'), 'w').write('all jobs finished; this session %.2f h\n' % ((time.time() - t0) / 3600))
print('ALL DONE - tell Claude.' if ok and not fails else 'Some jobs failed: %s - tell Claude.' % fails, flush=True)
