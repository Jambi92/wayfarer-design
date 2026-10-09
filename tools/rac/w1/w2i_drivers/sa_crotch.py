# RAC W2I1 leg watch item: Saurin surface crotch height (lowest non-tail vertex with |x| < 3 cm between 0.25 H and 0.6 H; the same rule is
# applied to the MPFB comparators in sa_limbcmp.py). Usage: python3 sa_crotch.py OUT.json
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_build as B
out = {}
for h in (168, 173, 178, 181, 188, 190, 203, 208):
    hh = B.H0 if h == 188 else float(h)
    for bid, p in (("SA-M%d" % h, {}), ("SA-F%d" % h, B.CEN)) + ((("SA-M208-B", B.BRD),) if h == 208 else ()):
        P, q = B.C.build(p); P2, q2, k = B.at_stature(P, q, hh); H = P2[:, 2].max()
        m = (np.abs(P2[:, 0]) < 3.0) & (P2[:, 2] > 0.25 * H) & (P2[:, 2] < 0.6 * H) & (B.L.tail < 0.2)
        out[bid] = float(P2[m, 2].min()); print(bid, round(out[bid], 2), round(out[bid] / H, 4), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
