# run_full.py : Saurin RP6 offline bake validation (order 8e3b7b4d) on Tyler's PC.  Every roster body runs sa6_bake_full.py (unbaked reference suite, fit,
#   EV 34x4 + GT 50x4 + full sweep + dense sweep of refit special gates, adaptive refit <= 3, integrity, RP5-literal diagnostics, before / after) as an
#   independent worker; gates and sweeps run in SHARDS pose shards.  1 numerical thread per process, BELOW_NORMAL priority.  Resumable: re-run to continue.
import os, sys, json, time, subprocess, platform
B = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(B); T = os.path.join(B, 'tools'); OUT = os.path.join(B, 'out'); os.makedirs(OUT, exist_ok=True)
BD = os.path.join(RB, 'SaurinRP6_ctrl', 'bodies'); UA = os.path.join(RB, 'SaurinRP6_ctrl', 'ctrl')
NAMES = ['BASE_c1', 'BASE_c2', 'END_FAHI', 'END_MUFAHI']; SHARDS = int(os.environ.get('SHARDS', '4'))
env = dict(os.environ, RP6_REPO=os.path.join(RB, 'SaurinRP6_bake', 'repo'), SA_W=os.path.join(RB, 'SaurinRP6_fits', 'data'), RP6_LAYERS='SA_RP6_creator_layers_v004.json',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
# frozen RP5 files the earlier PC bundle did not carry (additive copies into the PC repo snapshot; hashes verified per body by sa6_bake_integrity.py)
import shutil; FZ = os.path.join(env['RP6_REPO'], 'reviews', 'rac-rp5-evidence', 'saurin', 'full_cage', 'final_consolidation')
for f in os.listdir(os.path.join(B, 'fz')):
    if not os.path.exists(os.path.join(FZ, f)): shutil.copy(os.path.join(B, 'fz', f), FZ)
try:
    import ctypes
    class MS(ctypes.Structure): _fields_ = [('l', ctypes.c_ulong), ('m', ctypes.c_ulong), ('t', ctypes.c_ulonglong), ('a', ctypes.c_ulonglong), ('tp', ctypes.c_ulonglong), ('ap', ctypes.c_ulonglong), ('tv', ctypes.c_ulonglong), ('av', ctypes.c_ulonglong), ('x', ctypes.c_ulonglong)]
    m = MS(); m.l = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); ram = round(m.t / 2 ** 30, 1)
except Exception: ram = None
hw = dict(node=platform.node(), cpu=platform.processor(), logical_cpus=os.cpu_count(), ram_gb=ram, os=platform.platform(), python=sys.version.split()[0], workers=len(NAMES),
          shards_per_worker=SHARDS, threads_per_process=1, priority='BELOW_NORMAL_PRIORITY_CLASS', started=time.strftime('%Y-%m-%d %H:%M:%S'))
hl = os.path.join(B, 'hardware.jsonl'); open(hl, 'a').write(json.dumps(hw) + '\n')
print('Saurin RP6 offline bake: %d bodies in parallel, %d shards each. Safe to close and re-run (resumes).' % (len(NAMES), SHARDS), flush=True)
ps = []; t0 = time.time()
for nm in NAMES:
    r = os.path.join(OUT, nm, 'FULL_%s.json' % nm)
    if os.path.exists(r) and json.load(open(r)).get('done'): print('done already:', nm, flush=True); continue
    lg = open(os.path.join(OUT, 'worker_%s.log' % nm), 'a')
    ps.append((nm, time.time(), subprocess.Popen([sys.executable, os.path.join(T, 'sa6_bake_full.py'), nm, BD, os.path.join(UA, nm), os.path.join(OUT, nm), '3', str(SHARDS)], env=env,
                                                 stdout=lg, stderr=subprocess.STDOUT, creationflags=0x00004000)))
tl = open(os.path.join(B, 'timings.jsonl'), 'a')
for nm, ts, p in ps:
    rc = p.wait(); tl.write(json.dumps(dict(body=nm, stage='worker', host='PC', wall_s=round(time.time() - ts, 1), rc=rc, end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n'); tl.flush()
    print(time.strftime('%H:%M'), nm, 'worker rc', rc, '%.1f min' % ((time.time() - ts) / 60), flush=True)
tl.write(json.dumps(dict(stage='run', host='PC', wall_s=round(time.time() - t0, 1), end=time.strftime('%Y-%m-%d %H:%M:%S'))) + '\n'); tl.close()
ok = all(os.path.exists(os.path.join(OUT, n, 'FULL_%s.json' % n)) and json.load(open(os.path.join(OUT, n, 'FULL_%s.json' % n))).get('done') for n in NAMES)
open(os.path.join(B, 'ALLDONE.txt' if ok else 'STOPPED.txt'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n'); print('ALL DONE - tell Claude.' if ok else 'Stopped with work left - tell Claude.', flush=True)
