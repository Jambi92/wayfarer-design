# quick_cmp.py WORKDIR SIDE BASEDIR TAG... : compact elbow-arc comparison incl. closed-volume change vs the W0 LBS baseline (order 8e5021d §7)
import sys, json, numpy as np
W, S, BD = sys.argv[1:4]; TAGS = sys.argv[4:]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); Q = np.asarray(Z['Q'])
def cvol(V):
    T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', V[T_[:, 0]], np.cross(V[T_[:, 1]], V[T_[:, 2]])).sum() / 6)
for p in ['D2_%s_flex%d' % (S, a) for a in (60, 75, 90, 110, 120, 130)]:
    v0 = cvol(np.load('%s/diag/posed/%s_c_%s_W0.npz' % (BD, p, S))['V'].astype(float))
    for t in TAGS:
        d = W if not t.startswith('@') else BD; tt = t.lstrip('@')
        r = json.load(open('%s/diag/diag_results_c_%s_%s.json' % (d, S, tt)))['results'][p]; i = r['intersections']
        v = cvol(np.load('%s/diag/posed/%s_c_%s_%s.npz' % (d, p, S, tt))['V'].astype(float))
        print('%-13s %-6s nc %3d cr %3d d %5.1f fl %3d inv %2d fo %d loop %.2f p95 %3.0f max %3.0f zone %6.1f dV %+6.0f' % (p, tt, i['non_contact'], i['crease'], i['crease_depth_mm'], r['flips']['total'], r['inversions']['total'], r['folds']['outside'], r['loop_spacing_min_ratio'], r['strain']['zone_p95_pct'], r['strain']['zone_max_pct'], r['volume']['zone_pct'], v - v0))
