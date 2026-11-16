# sa6_bake_adapt.py NAME BODYDIR ARTDIR OUTDIR [MAXIT] : adaptive angle sampling for a per-body bake (per-body bake feasibility order a13cae71).
#   The 25 / 50 / 75 / 100 % fit leaves single folds at angles BETWEEN those samples on heavy bodies (sweep finding; the accepted END_FAHI shows the same
#   pattern).  Loop: sweep the current artifact (sa6_bake_sweep.py: 0.025 grid + both sides of every bake transition) -> every failing (pose, fraction)
#   becomes an extra fit sample -> refit from the current artifact (sa6_bake.py fit, BAKE_INIT, BAKE_EXTRA; pose-key tents span to the neighbouring
#   samples) -> evaluate from disk -> sweep again; stop when the sweep is clean or after MAXIT (default 3) iterations.  Each iteration's artifact, eval and
#   sweep are kept in OUTDIR/it<k>/.  Timings per stage -> OUTDIR/adapt_<NAME>.json.
import sys, os, json, time, shutil, subprocess
T = os.path.dirname(os.path.abspath(__file__)); nm, BD, AD, OD = sys.argv[1:5]; MAXIT = int(sys.argv[5]) if len(sys.argv) > 5 else 3
os.makedirs(OD, exist_ok=True); rec = dict(name=nm, iterations=[]); cur = os.path.join(AD, 'BK_%s.json' % nm); extra = {}
def run(args, env=None):
    t = time.time(); r = subprocess.run([sys.executable] + args, env=dict(os.environ, **(env or {})), capture_output=True, text=True)
    open(os.path.join(OD, 'log_%s.txt' % nm), 'a').write(r.stdout + r.stderr); return r.returncode, round(time.time() - t, 1)
for it in range(MAXIT + 1):
    d = os.path.join(OD, 'it%d' % it); os.makedirs(d, exist_ok=True)
    if it == 0:
        for ext in ('.json', '.npz'): shutil.copy(cur.replace('.json', ext), os.path.join(d, os.path.basename(cur).replace('.json', ext)))
        ev = os.path.join(AD, 'EV_%s.json' % nm)
        if os.path.exists(ev): shutil.copy(ev, d)
        tf = te = 0.0
    else:
        json.dump(extra, open(os.path.join(d, 'extra.json'), 'w'), indent=1)
        rc, tf = run([os.path.join(T, 'sa6_bake.py'), 'fit', nm, BD, d], dict(BAKE_INIT=cur, BAKE_EXTRA=os.path.join(d, 'extra.json')))
        rc2, te = run([os.path.join(T, 'sa6_bake.py'), 'eval', nm, BD, d])
    rc3, ts = run([os.path.join(T, 'sa6_bake_sweep.py'), nm, BD, d, d]) if not os.path.exists(os.path.join(d, 'SW_%s.json' % nm)) else (0, 0.0); sw = json.load(open(os.path.join(d, 'SW_%s.json' % nm)))
    ev = json.load(open(os.path.join(d, 'EV_%s.json' % nm))) if os.path.exists(os.path.join(d, 'EV_%s.json' % nm)) else None
    fails = {pn: [float(g['frac']) for g in v['gate_failures']] for pn, v in sw['poses'].items() if v['gate_failures']}
    rec['iterations'].append(dict(it=it, fit_s=tf, eval_s=te, sweep_s=ts, eval_clean=ev and ev['clean'], sweep_clean=sw['clean'],
                                  sweep_failures={k: len(v) for k, v in fails.items()}, extra_samples=sum(len(v) for v in extra.values())))
    print(nm, 'it', it, 'eval clean', ev and ev['clean'], 'sweep clean', sw['clean'], 'failures', {k: len(v) for k, v in fails.items()}, flush=True)
    json.dump(rec, open(os.path.join(OD, 'adapt_%s.json' % nm), 'w'), indent=1)
    if sw['clean'] and (ev is None or ev['clean']): break
    for pn, fs in fails.items(): extra[pn] = sorted(set(extra.get(pn, [])) | set(round(f, 4) for f in fs))
    cur = os.path.join(d, 'BK_%s.json' % nm)
rec['final'] = dict(iteration=rec['iterations'][-1]['it'], sweep_clean=rec['iterations'][-1]['sweep_clean'], eval_clean=rec['iterations'][-1]['eval_clean'])
json.dump(rec, open(os.path.join(OD, 'adapt_%s.json' % nm), 'w'), indent=1); print(nm, 'ADAPT done', rec['final'], flush=True)
