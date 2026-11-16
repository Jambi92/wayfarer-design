# run_bake.py : Saurin RP6 per-body bake feasibility benchmark (order a13cae71) - portable PC runner.
#   ONE body at a time, one solver process, numerical threads = 1, BELOW_NORMAL priority.  Per body: fit (sa6_bake.py fit) -> reopen + evaluate from disk
#   (sa6_bake.py eval).  Resumable: finished stages are skipped; an interrupted fit resumes from out/ckpt.  Stop at any time by closing the window
#   (or creating out/STOP.txt: the runner stops after the current stage).  Timings -> out/timings.jsonl, hardware -> out/hardware.json, logs -> out/logs.
import os, sys, time, json, subprocess, platform, ctypes
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, os.environ.get('BAKE_OUT', 'out')); os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True)
def ram_gb():
    class MS(ctypes.Structure): _fields_ = [('l', ctypes.c_ulong), ('m', ctypes.c_ulong), ('t', ctypes.c_ulonglong), ('a', ctypes.c_ulonglong)] + [('x%d' % i, ctypes.c_ulonglong) for i in range(5)]
    s = MS(); s.l = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)); return round(s.t / 2 ** 30, 1), round(s.a / 2 ** 30, 1)
hw = dict(node=platform.node(), cpu=platform.processor(), logical_cpus=os.cpu_count(), ram_total_avail_gb=ram_gb(), os=platform.platform(), python=sys.version.split()[0],
          workers=1, bake_fracs=os.environ.get('BAKE_FRACS', '1.0,0.75,0.5,0.25'), threads=dict(OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1), priority='BELOW_NORMAL_PRIORITY_CLASS', started=time.strftime('%Y-%m-%d %H:%M:%S'))
json.dump(hw, open(os.path.join(OUT, 'hardware.json'), 'w'), indent=1)
env = dict(os.environ, RP6_REPO=os.path.join(B, 'repo'), SA_W=os.path.join(B, '..', 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json', BAKE_FRACS=os.environ.get('BAKE_FRACS', '1.0,0.75,0.5,0.25'),
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
names = [l.strip() for l in open(os.path.join(B, os.environ.get('BAKE_LIST', 'body_list.txt'))) if l.strip()]
rd = os.path.join(B, os.environ.get('BAKE_REDO', 'redo.txt'))       # bodies to refit FROM SCRATCH with the current tools (earlier artifacts moved to out/superseded/<stamp>/, kept as evidence)
if os.path.exists(rd):
    import shutil; stamp = time.strftime('%Y%m%d_%H%M%S'); done_rd = os.path.join(OUT, 'redo_done.txt'); prev = set(open(done_rd).read().split()) if os.path.exists(done_rd) else set()
    for nm in [l.strip() for l in open(rd) if l.strip() and l.strip() not in prev]:
        sd = os.path.join(OUT, 'superseded', stamp); os.makedirs(sd, exist_ok=True)
        for f in ('BK_%s.json' % nm, 'BK_%s.npz' % nm, 'EV_%s.json' % nm, os.path.join('ckpt', 'BK_%s.json' % nm), os.path.join('ckpt', 'BK_%s.npz' % nm),
                  os.path.join('retried', 'BK_%s.json' % nm), os.path.join('retried', 'BK_%s.npz' % nm), os.path.join('retried', 'EV_%s.json' % nm)):
            if os.path.exists(os.path.join(OUT, f)): shutil.move(os.path.join(OUT, f), os.path.join(sd, os.path.basename(f)))
        open(done_rd, 'a').write(nm + '\n'); print('redo from scratch:', nm, flush=True)
print('Saurin RP6 bake benchmark: %d bodies, one at a time, low priority. Safe to close this window and re-run later (it resumes).' % len(names), flush=True)
for nm in names:
    art = os.path.join(OUT, 'BK_%s.json' % nm)
    if os.path.exists(art) and not json.load(open(art)).get('converged', True) and not os.path.exists(os.path.join(OUT, 'retried', 'BK_%s.json' % nm)):
        print(time.strftime('%H:%M'), 'retry (unconverged)', nm, flush=True); t = time.time()     # one retry: continue the fit for more rounds, then re-evaluate
        with open(os.path.join(OUT, 'logs', '%s_fit.log' % nm), 'a') as lg:
            rc = subprocess.call([sys.executable, os.path.join(B, 'tools', 'sa6_bake.py'), 'fit', nm, os.path.join(B, 'bodies'), OUT], env=dict(env, RETRY='1'), stdout=lg,
                                 stderr=subprocess.STDOUT, creationflags=0x00004000)
        open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, stage='fit_retry', wall_s=round(time.time() - t, 1), ok=rc == 0 and os.path.exists(art), rc=rc,
                                                                            end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
        ev = os.path.join(OUT, 'EV_%s.json' % nm)
        if os.path.exists(ev): os.makedirs(os.path.join(OUT, 'retried'), exist_ok=True); os.replace(ev, os.path.join(OUT, 'retried', 'EV_%s.json' % nm))
    for stage, done in (('fit', 'BK_%s.json' % nm), ('eval', 'EV_%s.json' % nm)) + ((('sweep', os.path.join('sweeps', 'SW_%s.json' % nm)),) if os.environ.get('BAKE_SWEEP') == '1' else ()):
        if os.path.exists(os.path.join(OUT, done)): continue
        if os.path.exists(os.path.join(OUT, 'STOP.txt')): print('STOP.txt found - stopping.', flush=True); sys.exit(0)
        print(time.strftime('%H:%M'), stage, nm, flush=True); t = time.time()
        with open(os.path.join(OUT, 'logs', '%s_%s.log' % (nm, stage)), 'a') as lg:
            cmd = ([sys.executable, os.path.join(B, 'tools', 'sa6_bake_sweep.py'), nm, os.path.join(B, 'bodies'), OUT, os.path.join(OUT, 'sweeps')] if stage == 'sweep' else
                   [sys.executable, os.path.join(B, 'tools', 'sa6_bake.py'), stage, nm, os.path.join(B, 'bodies'), OUT])
            rc = subprocess.call(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT,
                                 creationflags=0x00004000)
        dt = time.time() - t; ok = rc == 0 and os.path.exists(os.path.join(OUT, done))
        open(os.path.join(OUT, 'timings.jsonl'), 'a').write(json.dumps(dict(body=nm, stage=stage, wall_s=round(dt, 1), ok=ok, rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n')
        print(time.strftime('%H:%M'), stage, nm, 'ok' if ok else 'FAILED rc=%s (see out/logs)' % rc, '%.1f min' % (dt / 60), flush=True)
        if not ok: break
if all(os.path.exists(os.path.join(OUT, 'EV_%s.json' % n)) for n in names):
    open(os.path.join(OUT, 'ALLDONE.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n'); print('ALL DONE - tell Claude.', flush=True)
else: print('Stopped with bodies left - tell Claude.', flush=True)
