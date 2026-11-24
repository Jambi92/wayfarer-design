# run_v2_pass9b.py [WORKERS] : rig v002 pass 9b (order 07a3f24c §4).  The pass-9 pleat gate disagreed with the pleat audit it was built for:
#   (1) it exempted every head / rostrum_cap edge as "mouth": the audit (sa6_pleat_audit.py, against rig v001 at 0.25 / 0.5 / 0.75 / 1.0) found new pleats
#       under the jaw (jaw / neck_02 blend, plain LBS 1-8 deg, layer 94-143 deg) at gate:jaw_open_32 on LT90 -> the exemption is now the slit proper
#       (Solver._slit: head / rostrum_cap edges that plain LBS pleats in a jaw pose, 83 edges);
#   (2) it demanded zero pleats where the accepted rig v001 state has them (knuckle creases in fist / hand_opposition: 2-4 edges of v001's 3-18) and on the
#       corrected systems (a deep skin fold at the upperarm / spine_02 seam at shoulder_abd90 on F-N: plain LBS 67-75 deg with 21 flips, layer ~100 deg,
#       which smoothing only deepens) -> F-N, DSP-LOW, LT90 ended unconverged after 8 rounds of the same 4 edges.  The gate scope is now the audit's
#       regression scope: edges outside clavicle / upperarm / forearm, less the edges the rig v001 state pleats at that pose (PLEAT_ALLOW = data9b\allow,
#       built from the v001 audit measurements); the arm pleats stay in the audit for visual review.
#   tools9b\ = the committed tools.  Stage 1: all 19 states, pass-9 recipe (PLEAT_GATE=1, PD2_GATES=1, FRACS 1.0,0.75,0.5,0.25, COMP_MASK, SEGBULGE,
#   FAIR_SCOPE=arm), ROUNDS 12, starting from the most advanced pass-9 result: data9b\init (LT90: the cloud jaw repair) > out\layers9 (finished) >
#   out\layers9\ckpt (stopped pass-9 fit) > out\layers8 -> out\layers9b.  Stage 2: the 20 knots on out\layers9b -> out\nodes9b (the pass-9 knot stage is not
#   used: tools9\sa6_node_fit.py exits at once).  One process each, single-threaded, below-normal priority, resumable.  Logs out\logs\p9b_*.log,
#   out\jobs_p9b.json (init source per state in out\init9b.json).  PASS9B_DONE.txt when complete.
import os, sys, time, json, shutil, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out'); D = os.path.join(B, 'data'); D8 = os.path.join(B, 'data8'); D9 = os.path.join(B, 'data9b')
T = os.path.join(B, 'tools9b'); L8 = os.path.join(OUT, 'layers8'); L9 = os.path.join(OUT, 'layers9'); LO = os.path.join(OUT, 'layers9b'); NO = os.path.join(OUT, 'nodes9b')
LI = os.path.join(D9, 'init_auto')
for d in (LO, NO, LI, os.path.join(OUT, 'logs')): os.makedirs(d, exist_ok=True)
STATES = ['MUFAHI', 'MUHI', 'FAHI', 'M208-B', 'BRD', 'B-T80', 'F-N', 'M168', 'MIN', 'LT90', 'T80', 'T55', 'DSP-LOW', 'DSP-HIGH', 'ORB-8', 'ORB+3', 'RDG0.90', 'RDG1.30', 'NAR']
NODES = ['MUFAHI@0.25', 'MUFAHI@0.50', 'MUFAHI@0.75', 'FAHI@0.25', 'FAHI@0.50', 'FAHI@0.75', 'MUHI@0.25', 'MUHI@0.50', 'MUHI@0.75', 'M208-B@0.25', 'M208-B@0.50',
         'M208-B@0.75', 'T80@0.25', 'T80@0.50', 'T80@0.75', 'F-N@0.25', 'F-N@0.50', 'BRD@0.50', 'LT90@0.50', 'NAR@0.50']
nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2) - 2)
env0 = dict(os.environ, RP6_RIG='v002', RP6_REPO=os.path.join(B, 'repo8'), RP6_BASE_CORR='SA_RP6_correctives_v004.json', SA_W=D, RP6_WD=D8, OMP_NUM_THREADS='1',
            OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PD2_GATES='1', FAIR_SCOPE='arm', PLEAT_GATE='1', PLEAT_ALLOW=os.path.join(D9, 'allow'), PYTHONIOENCODING='utf-8')
IR = os.path.join(OUT, 'init9b.json'); src = json.load(open(IR)) if os.path.exists(IR) else {}
for s in STATES:                                      # freeze each state's starting layer once (resumes keep the first choice)
    if s in src: continue
    for d_, nm_ in ((os.path.join(D9, 'init'), 'CF_state_%s'), (L9, 'CF_state_%s'), (os.path.join(L9, 'ckpt'), 'CF_ckpt_%s'), (L8, 'CF_state_%s')):
        if os.path.exists(os.path.join(d_, nm_ % s + '.json')):
            for ext in ('.json', '.npz'): shutil.copy2(os.path.join(d_, nm_ % s + ext), os.path.join(LI, 'CF_state_%s' % s + ext))
            src[s] = os.path.join(d_, nm_ % s + '.json'); break
json.dump(src, open(IR, 'w'), indent=1)
JR = os.path.join(OUT, 'jobs_p9b.json'); rec = json.load(open(JR)) if os.path.exists(JR) else {}
flags = 0x00004000 if os.name == 'nt' else 0; fails = {}
def stage(jobs):
    run = {}
    while jobs or run:
        while jobs and len(run) < nw:
            n, cmd, env = jobs.pop(0); lg = open(os.path.join(OUT, 'logs', 'p9b_' + n + '.log'), 'a')
            run[n] = (subprocess.Popen(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg, time.time())
            rec.setdefault(n, []).append(dict(start=time.strftime('%Y-%m-%d %H:%M:%S'))); json.dump(rec, open(JR, 'w'), indent=1); print(time.strftime('%H:%M'), 'started', n, flush=True)
        time.sleep(20)
        for n in list(run):
            p, lg, ts = run[n]
            if p.poll() is not None:
                lg.close(); del run[n]; rec[n][-1].update(end=time.strftime('%Y-%m-%d %H:%M:%S'), exit=p.returncode, wall_h=round((time.time() - ts) / 3600, 3)); json.dump(rec, open(JR, 'w'), indent=1)
                if p.returncode: fails[n] = p.returncode
                print(time.strftime('%H:%M'), 'finished' if not p.returncode else 'FAILED', n, '- %d left' % (len(jobs) + len(run)), flush=True)
print('Saurin RP6 rig v002 pass 9b (19 layers + 20 knots, pleat gate = audit scope), %d at a time. Leave this window open; safe to close and re-run later.' % nw, flush=True)
stage([(s, [sys.executable, os.path.join(T, 'sa6_pd2_fit.py'), s, LO], dict(env0, INIT_LAYER=LI, FRACS='1.0,0.75,0.5,0.25', COMP_MASK='1', SEGBULGE='1', ROUNDS='12'))
       for s in STATES if not os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s))])
if all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES):
    stage([('node_' + n, [sys.executable, os.path.join(T, 'sa6_node_fit.py'), n, os.path.join(B, 'bodies'), LO, NO], env0) for n in NODES if not os.path.exists(os.path.join(NO, 'CK_%s.json' % n))])
ok = all(os.path.exists(os.path.join(LO, 'CF_state_%s.json' % s)) for s in STATES) and all(os.path.exists(os.path.join(NO, 'CK_%s.json' % n)) for n in NODES)
if ok: open(os.path.join(OUT, 'PASS9B_DONE.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
print('ALL DONE - tell Claude.' if ok and not fails else 'Failures: %s - tell Claude.' % fails, flush=True)
