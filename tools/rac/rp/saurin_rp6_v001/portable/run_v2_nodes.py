# run_v2_nodes.py [WORKERS] : rig v002 creator-key knots (order 07a3f24c §4), after run_v2.py and the base package v003 (repo/.../rig_v002).
#   The 20 knots of layer package v004 (same states / node weights / bodies): sa6_node_fit.py <STATE>@<w> bodies out/layers out/nodes, ROUNDS 4 (tool default),
#   RP6_LAYERS unused (base from the v003 package, state sets from out/layers).  Parallel, one process each, resumable; out/nodes/CK_*.json, logs in out/logs.
import os, sys, time, json, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out')
NODES = ['MUFAHI@0.25', 'MUFAHI@0.50', 'MUFAHI@0.75', 'FAHI@0.25', 'FAHI@0.50', 'FAHI@0.75', 'MUHI@0.25', 'MUHI@0.50', 'MUHI@0.75', 'M208-B@0.25', 'M208-B@0.50',
         'M208-B@0.75', 'T80@0.25', 'T80@0.50', 'T80@0.75', 'F-N@0.25', 'F-N@0.50', 'BRD@0.50', 'LT90@0.50', 'NAR@0.50']
LN = max([n for n in range(2, 10) if os.path.isdir(os.path.join(OUT, 'layers%d' % n))] or [1]); LD = os.path.join(OUT, 'layers%d' % LN if LN > 1 else 'layers')   # latest state-layer pass
ND = os.path.join(OUT, 'nodes%d' % LN if LN > 1 else 'nodes'); os.makedirs(ND, exist_ok=True)   # knots of that pass (never mixed with an older pass)
nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2) - 2); D = os.path.join(B, 'data'); T = os.path.join(B, 'tools')
env = dict(os.environ, RP6_RIG='v002', RP6_REPO=os.path.join(B, 'repo'), SA_W=D, RP6_WD=D, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
jobs = [n for n in NODES if not os.path.exists(os.path.join(ND, 'CK_%s.json' % n))]
JR = os.path.join(OUT, 'jobs_nodes%s.json' % (LN if LN > 1 else '')); rec = json.load(open(JR)) if os.path.exists(JR) else {}
print('Saurin RP6 rig v002 knots: %d to do, %d at a time.' % (len(jobs), nw), flush=True)
flags = 0x00004000 if os.name == 'nt' else 0; run = {}; fails = {}
while jobs or run:
    while jobs and len(run) < nw:
        n = jobs.pop(0); lg = open(os.path.join(OUT, 'logs', 'node%s_' % (LN if LN > 1 else '') + n + '.log'), 'a')
        run[n] = (subprocess.Popen([sys.executable, os.path.join(T, 'sa6_node_fit.py'), n, os.path.join(B, 'bodies'), LD, ND], env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg, time.time())
        rec.setdefault(n, []).append(dict(start=time.strftime('%Y-%m-%d %H:%M:%S'))); json.dump(rec, open(JR, 'w'), indent=1); print(time.strftime('%H:%M'), 'started', n, flush=True)
    time.sleep(20)
    for n in list(run):
        p, lg, ts = run[n]
        if p.poll() is not None:
            lg.close(); del run[n]; rec[n][-1].update(end=time.strftime('%Y-%m-%d %H:%M:%S'), exit=p.returncode, wall_h=round((time.time() - ts) / 3600, 3)); json.dump(rec, open(JR, 'w'), indent=1)
            if p.returncode: fails[n] = p.returncode
            print(time.strftime('%H:%M'), 'finished' if not p.returncode else 'FAILED', n, flush=True)
ok = all(os.path.exists(os.path.join(ND, 'CK_%s.json' % n)) for n in NODES)
if ok: open(os.path.join(OUT, 'NODES%s_DONE.txt' % (LN if LN > 1 else '')), 'w').write('done\n')
print('ALL DONE - tell Claude.' if ok and not fails else 'Failures: %s - tell Claude.' % fails, flush=True)
