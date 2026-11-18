# run_ctrl.py : Saurin RP6 per-body bake order a13cae71 - control sweeps (base controls BASE_c1/BASE_c2 + accepted endpoints END_FAHI/END_MUFAHI, empty K so
#   baked == packaged blend v004) on the PC.  Full-suite sweep (SWEEP_SET=all, SWEEP_STEP_OTHER=0.125), same gates as every bake body.
#   Each body is split into SHARDS pose shards run in parallel (poses are independent; sa6_bake_sweep_merge.py joins them into SW_<NAME>.json, identical rows).
#   Numerical threads = 1 per process, BELOW_NORMAL priority (the PC stays responsive; no throughput cost when idle).  Resumable: per-pose checkpoints.
import os, sys, json, time, subprocess, platform
B = os.path.dirname(os.path.abspath(__file__)); BD = os.path.join(B, 'bodies'); T = os.path.join(B, 'tools')
NAMES = ['END_FAHI', 'END_MUFAHI', 'BASE_c1', 'BASE_c2']; SHARDS = int(os.environ.get('SHARDS', '4'))
env = dict(os.environ, RP6_REPO=os.path.join(B, '..', 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(B, '..', 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8', SWEEP_SET='all', SWEEP_STEP_OTHER='0.125')
os.makedirs(os.path.join(B, 'logs'), exist_ok=True)
json.dump(dict(node=platform.node(), cpu=platform.processor(), logical_cpus=os.cpu_count(), python=sys.version.split()[0], processes=len(NAMES) * SHARDS, shards_per_body=SHARDS,
               threads_per_process=1, priority='BELOW_NORMAL_PRIORITY_CLASS', started=time.strftime('%Y-%m-%d %H:%M:%S')), open(os.path.join(B, 'hardware.json'), 'w'), indent=1)
print('Saurin RP6 control sweeps: %d bodies x %d shards = %d processes. Safe to close and re-run (resumes).' % (len(NAMES), SHARDS, len(NAMES) * SHARDS), flush=True)
procs = []; t0 = time.time()
for nm in NAMES:
    D = os.path.join(B, 'ctrl', nm)
    if os.path.exists(os.path.join(D, 'SW_%s.json' % nm)): print('done already:', nm, flush=True); continue
    for i in range(SHARDS):
        if os.path.exists(os.path.join(D, 'SW_%s.s%dof%d.json' % (nm, i, SHARDS))): continue
        lg = open(os.path.join(B, 'logs', '%s_s%d.log' % (nm, i)), 'a')
        procs.append((nm, i, time.time(), subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_sweep.py'), nm, BD, D, D], env=dict(env, SWEEP_SHARD='%d/%d' % (i, SHARDS)),
                                                           stdout=lg, stderr=subprocess.STDOUT, creationflags=0x00004000)))
tl = open(os.path.join(B, 'timings.jsonl'), 'a')
for nm, i, ts, p in procs:
    rc = p.wait(); tl.write(json.dumps(dict(body=nm, stage='control_sweep_shard', shard='%d/%d' % (i, SHARDS), host='PC', wall_s=round(time.time() - ts, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n'); tl.flush()
    print(time.strftime('%H:%M'), nm, 'shard', i, 'rc', rc, '%.1f min' % ((time.time() - ts) / 60), flush=True)
for nm in NAMES:
    D = os.path.join(B, 'ctrl', nm)
    if not os.path.exists(os.path.join(D, 'SW_%s.json' % nm)): subprocess.call([sys.executable, os.path.join(T, 'sa6_bake_sweep_merge.py'), nm, D, str(SHARDS)], env=env)
tl.write(json.dumps(dict(stage='control_sweeps_all', host='PC', wall_s=round(time.time() - t0, 1), end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n'); tl.close()
ok = all(os.path.exists(os.path.join(B, 'ctrl', n, 'SW_%s.json' % n)) for n in NAMES)
open(os.path.join(B, 'ALLDONE.txt' if ok else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n'); print('ALL DONE - tell Claude.' if ok else 'Stopped with work left - tell Claude.', flush=True)
