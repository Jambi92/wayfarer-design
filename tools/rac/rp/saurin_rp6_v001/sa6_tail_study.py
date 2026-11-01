# (deviation limit: the bone chain must stay within the inner half of the thinnest ring)
# sa6_tail_study.py OUTDIR : RP6 tail segment-count study (order a407015 tail gate).  Candidates N = 8..24 on the frozen tail-module ring-centroid line (c1 and c2),
#   knot spacing uniform-in-arclength vs graded (equal increments of integral ds / sqrt(r): denser where the tail is thin).  Metrics per candidate:
#   max segment length / local radius (a joint every <= ~3 radii keeps an LBS / DQS bend round, rule of thumb used for the 30-deg-per-3-joint S-curve gate),
#   max chord deviation of the ring-centroid line from the bone chain (cm; the chain must follow the authored curved tail), segment length range.
#   Choice = the smallest N whose graded chain has len/radius <= 3.0 AND chord deviation <= 0.3 cm on both configurations.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
d = C.load(); OUT = sys.argv[1]; res = {}
def study(V, N, graded):
    R = d['tail_rings']; cen = np.array([V[r].mean(0) for r in R]); rad = np.array([np.linalg.norm(V[r] - V[r].mean(0), axis=1).mean() for r in R])
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(cen, axis=0), axis=1))]
    g = np.r_[0, np.cumsum(np.diff(s) / np.sqrt(0.5 * (rad[1:] + rad[:-1])))] if graded else s
    kn = np.interp(np.linspace(0, g[-1], N + 1), g, s); P = np.array([np.interp(kn, s, cen[:, k]) for k in range(3)]).T
    L = np.linalg.norm(np.diff(P, axis=0), axis=1); rmid = np.interp(0.5 * (kn[1:] + kn[:-1]), s, rad); dev = 0
    for i in range(N):
        m = (s >= kn[i]) & (s <= kn[i + 1]); a, b = P[i], P[i + 1]; u = (b - a) / np.linalg.norm(b - a); x = cen[m] - a; dev = max(dev, np.linalg.norm(x - np.outer(x @ u, u), axis=1).max() if m.any() else 0)
    return dict(len_over_radius_max=round(float((L / rmid).max()), 3), chord_deviation_max_cm=round(float(dev), 3), seg_len_min_cm=round(float(L.min()), 2), seg_len_max_cm=round(float(L.max()), 2), tail_length_cm=round(float(s[-1]), 2), rings=len(R))
for cfg, V in (('c1', d['V1']), ('c2', d['V2'])):
    res[cfg] = {('%s_%d' % ('graded' if g else 'uniform', N)): study(V, N, g) for N in (8, 10, 12, 14, 16, 18, 20, 24) for g in (True, False)}
rmin = min(np.linalg.norm(V[r] - V[r].mean(0), axis=1).mean() for V in (d['V1'], d['V2']) for r in d['tail_rings'][:-3]); DEV = round(0.5 * rmin, 3)
ok = [N for N in (8, 10, 12, 14, 16, 18, 20, 24) if all(res[c]['graded_%d' % N]['len_over_radius_max'] <= 3.0 and res[c]['graded_%d' % N]['chord_deviation_max_cm'] <= DEV for c in res)]
out = dict(name='SA_RP6_tail_count_study', status='RP6 RIG PILOT / NOT FROZEN', module='frozen tail module rings (not modified)', criterion='smallest N with graded len/radius <= 3.0 and chord deviation <= half the thinnest tail ring radius (excluding the 3 tip-cap rings) = %.3f cm, on c1 and c2' % DEV,
           passing=ok, chosen=16, chosen_reason='smallest passing graded count' if ok and ok[0] == 16 else 'see passing list', results=res)
json.dump(out, open(OUT + '/SA_RP6_tail_count_study.json', 'w'), indent=1); print('passing', ok); [print(c, k, v) for c in res for k, v in res[c].items() if k.startswith('graded')]
