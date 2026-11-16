# run_adapt.py : pass 2 of the Saurin RP6 bake benchmark - adaptive angle sampling (sa6_bake_adapt.py) on every body, starting from its pass-1 artifact in out/.
#   One body at a time, single-threaded, BELOW_NORMAL priority, resumable (a body with out_adapt/adapt_<NAME>.json 'final' is skipped).
import os, sys, json, time, subprocess
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out_adapt'); os.makedirs(OUT, exist_ok=True)
env = dict(os.environ, RP6_REPO=os.path.join(B, 'repo'), SA_W=os.path.join(B, '..', 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
names = [l.strip() for l in open(os.path.join(B, 'adapt_list.txt')) if l.strip()]
print('Saurin RP6 bake pass 2 (adaptive angle sampling): %d bodies, one at a time, low priority. Safe to close and re-run (resumes).' % len(names), flush=True)
for nm in names:
    f = os.path.join(OUT, nm, 'adapt_%s.json' % nm)
    if os.path.exists(f) and 'final' in json.load(open(f)): continue
    print(time.strftime('%H:%M'), 'adapt', nm, flush=True); t = time.time()
    rc = subprocess.call([sys.executable, os.path.join(B, 'tools', 'sa6_bake_adapt.py'), nm, os.path.join(B, 'bodies'), os.path.join(B, 'out'), os.path.join(OUT, nm), '3'], env=env,
                         creationflags=0x00004000)
    open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, stage='adapt', wall_s=round(time.time() - t, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
    r = json.load(open(f)) if os.path.exists(f) else {}
    print(time.strftime('%H:%M'), nm, 'rc', rc, r.get('final'), '%.1f min' % ((time.time() - t) / 60), flush=True)
print('ALL DONE - tell Claude.', flush=True)
