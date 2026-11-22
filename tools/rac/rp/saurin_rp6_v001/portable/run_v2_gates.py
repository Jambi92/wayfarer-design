# run_v2_gates.py [WORKERS] : rig v002 pass 7 (order 07a3f24c §4): the 19 creator-state layers and the 20 creator-weight knots refitted WITH the 56 special
#   gates (PD2_GATES=1, sa6_pd2_fit.gate_set; before: anatomical poses only -> FAHI / MUFAHI folded the ankle / foot / jaw gates, unbaked END bodies 584 rig flips).
#   Stage 1: sa6_pd2_fit.py per state, INIT_LAYER = data/init_layer7 (pass-6 layers with the gate-only samples reset to base v003, sa6_gate_reset.py),
#            FRACS 1.0,0.75,0.5,0.25, COMP_MASK 1, SEGBULGE 1, ROUNDS 8 -> out/layers7.   Stage 2: sa6_node_fit.py per knot on out/layers7 -> out/nodes7.
#   One process each, single-threaded, below-normal priority, resumable (finished jobs skipped, killed fits resume from checkpoints).  Logs out/logs/p7_*.log,
#   out/jobs_p7.json (start / end / exit / wall h).  PASS7_DONE.txt when both stages are complete.
import os, sys, time, json, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out'); D = os.path.join(B, 'data'); T = os.path.join(B, 'tools7')   # pass-7 tool copy; the running standard bakes keep tools\ untouched
LI = os.path.join(D, 'init_layer7'); LO = os.path.join(OUT, 'layers7'); NO = os.path.join(OUT, 'nodes7')
for d in (LO, NO, os.path.join(OUT, 'logs')): os.makedirs(d, exist_ok=True)
STATES = ['MUFAHI', 'MUHI', 'FAHI', 'M208-B', 'BRD', 'B-T80', 'F-N', 'M168', 'MIN', 'LT90', 'T80', 'T55', 'DSP-LOW', 'DSP-HIGH', 'ORB-8', 'ORB+3', 'RDG0.90', 'RDG1.30', 'NAR']
NODES = ['MUFAHI@0.25', 'MUFAHI@0.50', 'MUFAHI@0.75', 'FAHI@0.25', 'FAHI@0.50', 'FAHI@0.75', 'MUHI@0.25', 'MUHI@0.50', 'MUHI@0.75', 'M208-B@0.25', 'M208-B@0.50',
         'M208-B@0.75', 'T80@0.25', 'T80@0.50', 'T80@0.75', 'F-N@0.25', 'F-N@0.50', 'BRD@0.50', 'LT90@0.50', 'NAR@0.50']
nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2) - 4)
env0 = dict(os.environ, RP6_RIG='v002', RP6_REPO=os.path.join(B, 'repo'), SA_W=D, RP6_WD=D, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PD2_GATES='1')
JR = os.path.join(OUT, 'jobs_p7.json'); rec = json.load(open(JR)) if os.path.exists(JR) else {}
flags = 0x00004000 if os.name == 'nt' else 0; fails = {}
def stage(jobs):
    run = {}
    while jobs or run:
        while jobs and len(run) < nw:
            n, cmd, env = jobs.pop(0); lg = open(os.path.join(OUT, 'logs', 'p7_' + n + '.log'), 'a')
            run[n] = (subprocess.Popen(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg, time.time())
            rec.setdefault(n, []).append(dict(start=time.strftime('%Y-%m-%d %H:%M:%S'))); json.dump(rec, open(JR, 'w'), indent=1); print(time.strftime('%H:%M'), 'started', n, flush=True)
        time.sleep(20)
        for n in list(run):
            p, lg, ts = run[n]
            if p.poll() is not None:
                lg.close(); del run[n]; rec[n][-1].update(end=time.strftime('%Y-%m-%d %H:%M:%S'), exit=p.returncode, wall_h=round((time.time() - ts) / 3600, 3)); json.dump(rec, open(JR, 'w'), indent=1)
                if p.returncode: fails[n] = p.returncode
                print(time.strftime('%H:%M'), 'finished' if not p.returncode else 'FAILED', n, '- %d left' % (len(jobs) + len(run)), flush=True)
print('Saurin RP6 rig v002 pass 7 (gates in the state / knot fits), %d at a time. Leave this window open; safe to close and re-run later.' % nw, flush=True)
stage([(s, [sys.executable, os.path.join(T, 'sa6_pd2_fit.py'), s, LO], dict(env0, INIT_LAYER=LI, FRACS='1.0,0.75,0.5,0.25', COMP_MASK='1', SEGBULGE='1', ROUNDS='8'))
       for s in STATES if not os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s))])
if all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES):
    stage([('node_' + n, [sys.executable, os.path.join(T, 'sa6_node_fit.py'), n, os.path.join(B, 'bodies'), LO, NO], env0) for n in NODES if not os.path.exists(os.path.join(NO, 'CK_%s.json' % n))])
ok = all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES) and all(os.path.exists(os.path.join(NO, 'CK_%s.json' % n)) for n in NODES)
if ok: open(os.path.join(OUT, 'PASS7_DONE.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
print('ALL DONE - tell Claude.' if ok and not fails else 'Failures: %s - tell Claude.' % fails, flush=True)
