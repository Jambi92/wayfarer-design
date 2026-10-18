# RAC Stage C: build the Grask E3 stature series from the FROZEN GR.E3 spec (reviews/rac-rmot05d-evidence/candidates.json) on the exact
# 05D route (rmot05d_drivers/d_build.py: 05B arch cfg_final + race_base.organize, true skeletal floor). Same call as d_build for the
# reference body, only the stature target differs (W2C stature series 198 / 208 / 229 / 239; height macro re-solved by the generator,
# never a uniform scale). Usage: python3 stc_build.py CFG05B.json SPECS.json H...
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/w2c_drivers', W1 + '/w1g_drivers'): sys.path.insert(0, p)
A = json.load(open(sys.argv[1])); SP = json.load(open(sys.argv[2]))
import gr_body as GB
for H in sys.argv[3:]:
    GB.build('GR5DE3_%s' % H, float(H), None, None, arch=A['GR'], racebase=SP['GR']['E3'])
