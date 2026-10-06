# RAC W1h: adds the directional-check thoracic-breadth reading (arm_measure vertex slabs on the rest body = thorax_breadth_share)
# to a sensitivity.json produced before sensitivity.py recorded it, from the rest bodies it saved in w1g/sens.  Usage: sens_tb.py sensitivity.json
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn5, bony_envelope as BE
from arm_measure import load
p = sys.argv[1]; d = json.load(open(p)); wd = gn5.G + '/sens'
def tb(name, H): return BE.fast_stations(load(wd + '/%s_rest.npz' % name), section=False)['S2'][0] / H / gn5.SK_TB - 1
d["base"]["skin_TB_vs_SK_measure_layer"] = tb('S0', d["base"]["stature"])
for i, n in enumerate(gn5.NAMES):
    for sg in (-1, 1):
        k = "%s %+d" % (n, sg); d["perturb"][k]["skin_TB_vs_SK_measure_layer"] = tb('S%d%s' % (i, 'm' if sg < 0 else 'p'), d["perturb"][k]["stature"])
json.dump(d, open(p, 'w'), indent=1); print('base', d["base"]["skin_TB_vs_SK_measure_layer"])
