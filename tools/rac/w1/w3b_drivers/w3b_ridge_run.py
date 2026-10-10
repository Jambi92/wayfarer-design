# RAC W3B RM-UF-04 ridge-strength sweep: one hidden normalized strength m (all families) and per-family sweeps; metrics, guards, quality.
# Guards (diagnostic criteria; values reported so the author can re-threshold):
#   LOWER - LEGIBILITY THROUGH THE INTEGUMENT: each family's strength (core - flank height above the smoothed base) must stay >= 1.5x the
#           canonical scale-relief amplitude around it (p95 - p5 of the W2 relief within 1 cm of the core). Below 1.0x the plane break is
#           carried by the scale texture, not the skull (order section 11 / 13: "face requires scales ...", "scale relief creating the ridge").
#           MARGINAL 1.0-1.5x. Visual check: naked skull still reads Saurin (renders).
#   UPPER - RAZOR / FIN: the slope the ridge adds to its base plane (p95 angle vs the family-removed skull) must stay <= 45 deg (flanks
#           steeper than 45 deg read as a fin / blade edge rather than a plane change); MARGINAL 40-45.
#           SCOWL: frontal eye visibility (0 and 10 deg elevation) must not fall more than 10 % below the canonical value.
#           ARMOR / FACET / CARICATURE: visual (renders, naked skull).
#   QUALITY - 0 flipped / degenerate faces; edge strain within [0.67, 1.5] (W2I precedent).
# Usage: python3 w3b_ridge_run.py global | family NAME
import os, sys, json, numpy as np
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_ridge as RG
W = C.W + '/ridge'; os.makedirs(W, exist_ok=True)
_rel = None
def relief_amp():
    global _rel
    if _rel is None:
        p = W + '/relief_amp.json'
        if os.path.exists(p): _rel = json.load(open(p))
        else:
            import igl
            Vu, Fu = igl.upsample(C.V0, C.F0); d = C.canon_disp(); hm = Vu[:, 2] > 165; idx = np.where(hm)[0]; tr = cKDTree(Vu[idx]); _rel = {}
            for k, (core, flank) in RG.sets().items():
                nb = np.unique(np.concatenate(tr.query_ball_point(C.V0[RG.HV[core]], 1.0))); dd = d[idx[nb]]
                _rel[k] = float(np.percentile(dd, 95) - np.percentile(dd, 5))
            json.dump(_rel, open(p, 'w'), indent=1)
    return _rel
def evaluate(tag, m):
    f = W + '/%s.npy' % tag
    if os.path.exists(f): P = np.load(f).astype(float)
    else: P = RG.build(m); np.save(f, P.astype(np.float32))
    M, _ = RG.metric(P); sl = RG.flank_slope(P); q = C.quality(P, C.F0, C.V0); ra = relief_amp()
    return {"m": m, "metric": M, "flank_slope_p95_deg": sl, "legibility_ratio": {k: M[k]["strength_cm"] / ra[k] for k in M},
            "eye_vis_0": RG.eye_visibility(P, 0.0), "eye_vis_10": RG.eye_visibility(P, 10.0), "quality": q}
def run(cases):
    rp = W + '/results.json'; res = json.load(open(rp)) if os.path.exists(rp) else {}
    for tag, m in cases:
        if tag in res: continue
        res[tag] = evaluate(tag, m); json.dump(res, open(rp, 'w'), indent=1)
        r = res[tag]; print(tag, 'eye %.3f/%.3f flips %d' % (r['eye_vis_0'], r['eye_vis_10'], r['quality']['flipped']),
                            ' '.join('%s:%.3f/%.1f/%.2f' % (k[:4], r['metric'][k]['strength_cm'], r['flank_slope_p95_deg'][k], r['legibility_ratio'][k]) for k in RG.FAMS), flush=True)
if __name__ == '__main__':
    if sys.argv[1] == 'global':
        ms = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.0, 0.0, 0.25, 0.5, 0.75, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
        run([('g%.2f' % v, {k: v for k in RG.FAMS}) for v in ms])
    if sys.argv[1] == 'family':
        k = sys.argv[2]; ms = [float(x) for x in sys.argv[3].split(',')]
        run([('%s%.2f' % (k, v), {k: v}) for v in ms])
