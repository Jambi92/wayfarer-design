# run_adapt2.py : pass 3 of the Saurin RP6 bake benchmark - full-suite between-sample sweep (SWEEP_SET=all: heavy-joint poses at 0.025 + every other pose at the
#   0.125 midpoints, both sides of every bake AND packaged-blend transition) on the pass-2 final artifact (out_adapt/<NAME>/it<final>), refitting at any failing angle.
#   One body at a time, single-threaded, BELOW_NORMAL priority, resumable (a body with out_adapt/adapt_<NAME>.json 'final' is skipped).
import os, sys, json, time, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out_adapt2'); os.makedirs(OUT, exist_ok=True)
env = dict(os.environ, RP6_REPO=os.path.join(B, 'repo'), SA_W=os.path.join(B, '..', 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', SWEEP_SET='all', SWEEP_STEP_OTHER='0.125')
names = [l.strip() for l in open(os.path.join(B, 'adapt2_list.txt')) if l.strip()]
print('Saurin RP6 bake pass 3 (full-suite sweep + adaptive refit): %d bodies, one at a time, low priority. Safe to close and re-run (resumes).' % len(names), flush=True)
for nm in names:
    f = os.path.join(OUT, nm, 'adapt_%s.json' % nm)
    if os.path.exists(f) and 'final' in json.load(open(f)): continue
    a1 = json.load(open(os.path.join(B, 'out_adapt', nm, 'adapt_%s.json' % nm))); src = os.path.join(B, 'out_adapt', nm, 'it%d' % a1['final']['iteration'])
    print(time.strftime('%H:%M'), 'adapt2', nm, 'from', src, flush=True); t = time.time()
    rc = subprocess.call([sys.executable, os.path.join(B, 'tools', 'sa6_bake_adapt.py'), nm, os.path.join(B, 'bodies'), src, os.path.join(OUT, nm), '3'], env=env,
                         creationflags=0x00004000)
    open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, stage='adapt2', wall_s=round(time.time() - t, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
    r = json.load(open(f)) if os.path.exists(f) else {}
    print(time.strftime('%H:%M'), nm, 'rc', rc, r.get('final'), '%.1f min' % ((time.time() - t) / 60), flush=True)
print('ALL DONE - tell Claude.', flush=True)
