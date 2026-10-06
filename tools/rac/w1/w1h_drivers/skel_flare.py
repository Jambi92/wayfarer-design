# RAC W1h: skin flank flare of the minimum-composition (skeleton) bodies, GO W1g / W1h vs the accepted references (AD-W1H-2 context).
# Usage: python3 skel_flare.py out.json name=path ...
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import profile_bump as PB
out = {a.split('=', 1)[0]: PB.flank_flare(a.split('=', 1)[1])['flank_flare'] for a in sys.argv[2:]}
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(out)
