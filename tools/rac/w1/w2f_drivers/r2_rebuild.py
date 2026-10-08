# RAC W2F closure, R2 (author ruling, reviews/chatgpt-rac-w2f-elf-family-closure-order.md §2): native short-adult route wherever the re-solved
# height macro falls below ~0.40. The four affected elf bodies (FN163, VA163, AE168, AE173) are the native builds FN163N / VA163N / AE168N / AE173N
# (built by leg_probe.py 'route' from each population's accepted base macro, targets and bone scales unchanged); this script rebuilds what depended
# on them: the Aelari 173 composition states and the Aelari 168 frames, plus skeletal grids. Matched Marchfolk 163 uses the native MF163N (W2E rt).
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import el_build as B
from concurrent.futures import ThreadPoolExecutor
RT = B.W + '/rt'
J = []
for nm, m, w in (("LOWMUS", 0, 0.5), ("HIMUS", 1, 0.5), ("HIFAT", 0.5, 1), ("HIBOTH", 1, 1), ("LOW", 0.25, 0.25), ("MIN", 0, 0)):
    J.append((B.variant, (RT + '/AE173N-NAT_build.json', {"muscle": m, "weight": w}, B.W + '/comp', 'AE173N-' + nm)))
for tag, fr in (("N", B.NARROWB), ("B", B.BROADB)):
    src = RT + '/AE168N-NAT_build.json'; J.append((B.variant, (src, B.frame(src, fr), B.W + '/fr', 'AE%s168N' % tag)))
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
G = [(RT + '/%s-NAT_build.json' % n, B.W + '/g/%s-NAT' % n) for n in ("FN163N", "VA163N", "AE168N", "AE173N")] + \
    [(B.W + '/fr/AE%s168N_build.json' % t, B.W + '/g/AE%s168N' % t) for t in "NB"] + [(B.S + '/w2e/rt/MF163N-NAT_build.json', B.W + '/g/MF163N-NAT')]
def g(x):
    p, o = x
    with open(B.W + '/logs/r2grid_%s.log' % os.path.basename(o), 'w') as f: rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', p, o], cwd=B.T, stdout=f, stderr=subprocess.STDOUT).returncode
    print('GRID', os.path.basename(o), rc, flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g, G))
print('R2_DONE')
