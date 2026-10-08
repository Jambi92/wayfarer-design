# RAC W2F closure: R2 cutoff sensitivity (diagnostic only; the ruled cutoff ~0.40 is not changed). Native-route builds of the first macro-route
# body above the cutoff in each family (FN173 macro 0.444, AE178 0.428, VA173 0.516), with skeletal grids, to test whether the surviving
# continuity reversals at the native -> macro step are the generator's short-stature behaviour fading above 0.40.
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import el_build as B
from concurrent.futures import ThreadPoolExecutor
J = []
for r, h in (("FN", 173), ("AE", 178), ("VA", 173)):
    c = dict(B.cfg(B.BASE[r])); c.update(stature=float(h), id="%s%dN" % (r, h), base_height_macro=json.load(open(B.BASE[r]))["height_macro"])
    J.append((B.native, (c, B.W + '/rt', '%s%dN' % (r, h))))
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
def g(n):
    with open(B.W + '/logs/sgrid_%s.log' % n, 'w') as f: rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', B.W + '/rt/%s-NAT_build.json' % n, B.W + '/g/%s-NAT' % n], cwd=B.T, stdout=f, stderr=subprocess.STDOUT).returncode
    print('GRID', n, rc, flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g, ("FN173N", "AE178N", "VA173N")))
print('SENS_DONE')
