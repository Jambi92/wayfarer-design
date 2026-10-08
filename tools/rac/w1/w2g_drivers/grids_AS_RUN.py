# RAC W2G: CIB grids (w2a_drivers/mfm_grid.py) for every Halvren skeleton body (statures, frames, expressions)
import subprocess, os, glob
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2g'
B = [W + '/st/%s_build.json' % n for n in ("HV152N-NAT", "HV163N-NAT", "HV173M", "HV181M", "HV190M", "HV203M", "HV213M")] + sorted(glob.glob(W + '/fr/*_build.json')) + sorted(glob.glob(W + '/ex/*_build.json'))
def g(p):
    n = os.path.basename(p)[:-11]
    if os.path.exists(W + '/g/%s/skp/t1.0/MF-M-R_meas.json' % n): return
    with open(W + '/logs/grid_%s.log' % n, 'w') as f: rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', p, W + '/g/' + n], cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
    print('GRID', n, rc, flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g, B))
print('GRIDS_DONE', flush=True)
