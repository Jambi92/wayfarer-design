# RAC W1i: trunk-profile continuity readings (gn6.cont) of the equal-height Broad Skarn comparator bodies, skeleton (minimum
# composition) and skin, for the ALPC-7 vs pelvis-cap discussion. Usage: python3 skb_continuity.py out.json name=rest.npz ...
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); import gn6
out = {a.split('=', 1)[0]: gn6.cont(a.split('=', 1)[1]) for a in sys.argv[2:]}
json.dump(out, open(sys.argv[1], 'w'), indent=1); [print(k, {a: round(b, 4) for a, b in v.items()}) for k, v in out.items()]
