# RAC W2H: CIB grids (run twice: the second pass adds MF152-NAT) (w2a_drivers/mfm_grid.py) for every short-race skeleton body (references, stature families, frames, distal extremes)
import subprocess, os, glob
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2h'
B = [S + '/w1f/final/DU-NAT_build.json', S + '/w1f/final/PK-NAT_build.json', S + '/w1r/probe/CGJ7_build.json'] + \
    [W + '/st/%s-NAT_build.json' % n for n in ("DU122", "DU152", "PK91", "PK122", "CG76", "CG107")] + sorted(glob.glob(W + '/fr/*_build.json')) + \
    [W + '/nm/COG12-NAT_build.json', W + '/nm/COG13-NAT_build.json', S + '/w1t/bnd/MF152-NAT_build.json']   # MF152 re-gridded on the W2 method (DU-P4 like-for-like)
def g(p):
    n = os.path.basename(p)[:-11]
    if os.path.exists(W + '/g/%s/skp/t1.0/MF-M-R_meas.json' % n): return
    with open(W + '/logs/grid_%s.log' % n, 'w') as f: rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', p, W + '/g/' + n], cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
    print('GRID', n, rc, flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g, B))
print('GRIDS_DONE', flush=True)
