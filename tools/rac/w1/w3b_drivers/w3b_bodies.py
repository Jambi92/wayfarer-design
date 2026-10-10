# RAC W3B RM-UB-08 section 17: representative accepted body extremes, built with the canonical W2 route (w2i4_drivers/sa_finish.build_f =
# accepted creator / §263 warp -> F2 forearm + L1 thigh rebuild -> W2I4 finish delta -> regional stature route). Copies only.
# The scale relief is CARRIED per vertex along each body's own normals (W2I4 convention for every non-reference state / stature).
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import w3b_common as C
W = C.W + '/bodies'; os.makedirs(W, exist_ok=True)
def bodies():
    sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i_drivers')); import sa_build as B
    tail = B.tail; Mx = B.Mx; NAR, BRD, CEN = B.NAR, B.BRD, B.CEN
    return [("SA-M188", {}, B.H0), ("SA-F188", CEN, B.H0), ("SA-M168", {}, 168.0), ("SA-M208", {}, 208.0), ("SA-M188-N", NAR, B.H0), ("SA-M188-B", BRD, B.H0),
            ("SA-M188-MUHI", {'muscle': 1.0}, B.H0), ("SA-M188-FAHI", {'fat': 1.0}, B.H0), ("SA-M188-N-FAHI", Mx(NAR, {'fat': 1.0}), B.H0),
            ("SA-M188-T80", tail(80, 1.22), B.H0)]
def build(bid):
    f = W + '/%s.npy' % bid
    if os.path.exists(f): return np.load(f).astype(np.float64)
    import sa_finish as FN
    for b, p, h in bodies():
        if b == bid:
            P, q, k, info = FN.build_f(dict(p), None if h == FN.H0 else h); np.save(f, P.astype(np.float32)); return P.astype(np.float64)
if __name__ == '__main__':
    for b, p, h in bodies():
        P = build(b); print(b, P.shape, round(float(np.ptp(P[:, 2])), 2), 'max |P - canonical| %.2f' % float(np.abs(P - C.V0).max()) if b == 'SA-M188' else '', flush=True)
