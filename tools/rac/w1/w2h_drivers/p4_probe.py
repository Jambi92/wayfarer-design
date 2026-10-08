# RAC W2H DU-P4 diagnostic probe (NOT applied): the W1t Durrim 152 cm pelvis-depth probes (pelvis bone Z x1.04 / x1.06 on the DU-NAT construction,
# w1t/bnd/DU152P4 / DU152P6) re-measured on the W2 skeletal grid and exact-plane joints, to show what a Durrim-specific pelvic AP write would do.
import subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
def g(n):
    with open(S + '/w2h/logs/grid_%s.log' % n, 'w') as f: rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', S + '/w1t/bnd/%s-NAT_build.json' % n, S + '/w2h/g/%s-NAT' % n], cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
    print('GRID', n, rc, flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g, ("DU152P4", "DU152P6")))
