# run_v2_pass8.py [WORKERS] : rig v002 pass 8 (order 07a3f24c §4; regression found by the v002 tail review + sa6_pleat_audit.py).
#   Base correctives v004 = sa6_base_merge.py (corrected shoulder from v003 + every other system unfaired from pass 4).  The pass-5..7 state layers and knots
#   were faired everywhere like base v003; pass 8 refits them on base v004:
#   Stage 1: sa6_pd2_fit.py per state, INIT_LAYER = data8/init_layer8 (sa6_base_merge.py per state: clavicle / upperarm from pass 7, everything else from
#            pass 4), PD2_GATES=1 (the 56 special gates), FAIR_SCOPE=arm (fairing only on poses that drive the corrected shoulder / elbow), FRACS
#            1.0,0.75,0.5,0.25, COMP_MASK 1, SEGBULGE 1, ROUNDS 8 -> out/layers8.
#   Stage 2: sa6_node_fit.py per knot on out/layers8 -> out/nodes8 (base from repo8 = packaged base v004).
#   tools8\ = the committed tools of this pass; repo8\ = repo7\ + base v004 package; data8\ = W_{M,F} + CF_{M,F} (base v004); cage arrays from data\.
#   One process each, single-threaded, below-normal priority, resumable.  Logs out/logs/p8_*.log, out/jobs_p8.json.  PASS8_DONE.txt when complete.
import os, sys, time, json, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out'); D = os.path.join(B, 'data'); D8 = os.path.join(B, 'data8'); T = os.path.join(B, 'tools8')
LI = os.path.join(D8, 'init_layer8'); LO = os.path.join(OUT, 'layers8'); NO = os.path.join(OUT, 'nodes8')
for d in (LO, NO, os.path.join(OUT, 'logs')): os.makedirs(d, exist_ok=True)
STATES = ['MUFAHI', 'MUHI', 'FAHI', 'M208-B', 'BRD', 'B-T80', 'F-N', 'M168', 'MIN', 'LT90', 'T80', 'T55', 'DSP-LOW', 'DSP-HIGH', 'ORB-8', 'ORB+3', 'RDG0.90', 'RDG1.30', 'NAR']
NODES = ['MUFAHI@0.25', 'MUFAHI@0.50', 'MUFAHI@0.75', 'FAHI@0.25', 'FAHI@0.50', 'FAHI@0.75', 'MUHI@0.25', 'MUHI@0.50', 'MUHI@0.75', 'M208-B@0.25', 'M208-B@0.50',
         'M208-B@0.75', 'T80@0.25', 'T80@0.50', 'T80@0.75', 'F-N@0.25', 'F-N@0.50', 'BRD@0.50', 'LT90@0.50', 'NAR@0.50']
nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2) - 2)
env0 = dict(os.environ, RP6_RIG='v002', RP6_REPO=os.path.join(B, 'repo8'), RP6_BASE_CORR='SA_RP6_correctives_v004.json', SA_W=D, RP6_WD=D8, OMP_NUM_THREADS='1',
            OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PD2_GATES='1', FAIR_SCOPE='arm', PYTHONIOENCODING='utf-8')
JR = os.path.join(OUT, 'jobs_p8.json'); rec = json.load(open(JR)) if os.path.exists(JR) else {}
flags = 0x00004000 if os.name == 'nt' else 0; fails = {}
def stage(jobs):
    run = {}
    while jobs or run:
        while jobs and len(run) < nw:
            n, cmd, env = jobs.pop(0); lg = open(os.path.join(OUT, 'logs', 'p8_' + n + '.log'), 'a')
            run[n] = (subprocess.Popen(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg, time.time())
            rec.setdefault(n, []).append(dict(start=time.strftime('%Y-%m-%d %H:%M:%S'))); json.dump(rec, open(JR, 'w'), indent=1); print(time.strftime('%H:%M'), 'started', n, flush=True)
        time.sleep(20)
        for n in list(run):
            p, lg, ts = run[n]
            if p.poll() is not None:
                lg.close(); del run[n]; rec[n][-1].update(end=time.strftime('%Y-%m-%d %H:%M:%S'), exit=p.returncode, wall_h=round((time.time() - ts) / 3600, 3)); json.dump(rec, open(JR, 'w'), indent=1)
                if p.returncode: fails[n] = p.returncode
                print(time.strftime('%H:%M'), 'finished' if not p.returncode else 'FAILED', n, '- %d left' % (len(jobs) + len(run)), flush=True)
print('Saurin RP6 rig v002 pass 8 (layers + knots on base v004), %d at a time. Leave this window open; safe to close and re-run later.' % nw, flush=True)
stage([(s, [sys.executable, os.path.join(T, 'sa6_pd2_fit.py'), s, LO], dict(env0, INIT_LAYER=LI, FRACS='1.0,0.75,0.5,0.25', COMP_MASK='1', SEGBULGE='1', ROUNDS='8'))
       for s in STATES if not os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s))])
if all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES):
    stage([('node_' + n, [sys.executable, os.path.join(T, 'sa6_node_fit.py'), n, os.path.join(B, 'bodies'), LO, NO], env0) for n in NODES if not os.path.exists(os.path.join(NO, 'CK_%s.json' % n))])
ok = all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES) and all(os.path.exists(os.path.join(NO, 'CK_%s.json' % n)) for n in NODES)
if ok: open(os.path.join(OUT, 'PASS8_DONE.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
print('ALL DONE - tell Claude.' if ok and not fails else 'Failures: %s - tell Claude.' % fails, flush=True)
