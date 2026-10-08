# RAC W2I §4 / §14: intermediate Saurin statures needed ONLY for real matched-height comparisons with the accepted W2 families
# (173 / 178 / 181 / 190 cm: Marchfolk, Sagekin, Fenn, Aelari, Vael, Halvren, Skarn 190); same regional route as sa_build.py. Usage: python3 sa_build_extra.py OUT.json
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
out = {}
for h in (173, 178, 181, 190):
    for bid, p in (("SA-M%d" % h, {}), ("SA-F%d" % h, B.CEN)):
        P, q = B.C.build(p); P2, q2, k = B.at_stature(P, q, float(h)); M = B.measure(P2, q2, k); M['note'] = 'matched-height comparison stature'; M['params'] = dict(p); out[bid] = M
        print(bid, round(M['height'], 2), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
