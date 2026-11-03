# run_fits.py [WORKERS] : runs the RP6 creator-state corrective layer fits from this portable bundle (see bundle_manifest.json).
#   One process per state, single-threaded numpy, below-normal priority so the PC stays usable.  Resumable: finished states are skipped and a killed state
#   resumes from out/ckpt.  Results: out/CF_state_<STATE>.json/.npz, logs in out/logs, out/ALLDONE.txt when every state has finished.
import os, sys, time, json, subprocess, ctypes
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, 'out'); os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True)
ORDER = ['MUFAHI', 'MUHI', 'FAHI', 'M208-B', 'BRD', 'B-T80', 'F-N', 'M168', 'MIN', 'LT90', 'T80', 'T55', 'DSP-LOW', 'DSP-HIGH', 'ORB-8', 'ORB+3', 'RDG0.90', 'RDG1.30', 'NAR']
man = json.load(open(os.path.join(B, 'bundle_manifest.json'))); ORDER = [s for s in ORDER if s in man['states']]
def ram_gb():
    try:
        class MS(ctypes.Structure): _fields_ = [('l', ctypes.c_ulong), ('m', ctypes.c_ulong), ('t', ctypes.c_ulonglong), ('a', ctypes.c_ulonglong)] + [('x%d' % i, ctypes.c_ulonglong) for i in range(5)]
        s = MS(); s.l = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)); return s.a / 2 ** 30
    except Exception: return 8.0
ncpu = os.cpu_count() or 2
nw = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, min(ncpu - 1, int(ram_gb() // 2.5), len(ORDER)))
env = dict(os.environ, RP6_REPO=os.path.join(B, 'repo'), SA_W=os.path.join(B, 'data'), RP6_WD=os.path.join(B, 'data'), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
todo = [s for s in ORDER if not os.path.exists(os.path.join(OUT, 'CF_state_%s.json' % s))]
print('Saurin RP6 creator-state fits: %d to do, %d at a time (%d CPUs, %.1f GB free RAM). Leave this window open; it is safe to close and re-run later.' % (len(todo), nw, ncpu, ram_gb()), flush=True)
flags = 0x00004000 if os.name == 'nt' else 0          # BELOW_NORMAL_PRIORITY_CLASS
run = {}; fails = {}; t0 = time.time()
while todo or run:
    while todo and len(run) < nw:
        s = todo.pop(0); lg = open(os.path.join(OUT, 'logs', s + '.log'), 'a')
        run[s] = (subprocess.Popen([sys.executable, os.path.join(B, 'tools', 'sa6_pd2_fit.py'), s, OUT], env=env, stdout=lg, stderr=subprocess.STDOUT, creationflags=flags), lg)
        print(time.strftime('%H:%M'), 'started', s, flush=True)
    time.sleep(20)
    for s in list(run):
        p, lg = run[s]
        if p.poll() is not None:
            lg.close(); del run[s]; ok = p.returncode == 0 and os.path.exists(os.path.join(OUT, 'CF_state_%s.json' % s))
            if not ok: fails[s] = p.returncode
            print(time.strftime('%H:%M'), 'finished' if ok else 'FAILED (see out/logs/%s.log)' % s, s, '- %d left' % (len(todo) + len(run)), flush=True)
done = [s for s in ORDER if os.path.exists(os.path.join(OUT, 'CF_state_%s.json' % s))]
if not fails and len(done) == len(ORDER):
    open(os.path.join(OUT, 'ALLDONE.txt'), 'w').write('all %d states finished in %.1f h\n' % (len(done), (time.time() - t0) / 3600))
print('ALL DONE - tell Claude.' if not fails else 'Some states failed: %s - tell Claude.' % fails, flush=True)
