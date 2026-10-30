# thumb_opt.py DEF.json FAM1.npz [FAM2 ...] OUT.json : choose the v002 thumb-patch placement constants (one global set, shared by every body) that
# minimise T-4 violations (angle 45-135, aspect <= 4) of the branch quads over all given realizations, worst body first.
import sys, json, time, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import thumb_patch as TP
from core3lib import quality
from scipy.optimize import differential_evolution, minimize
DEF, FAMS, OUT = sys.argv[1], sys.argv[2:-1], sys.argv[-1]
br = json.load(open(DEF)); Z = [dict(np.load(f)) for f in FAMS]
KEYS = ['uz_e', 'uz_o', 'uz_m', 'ms', 'ua', 'a', 'b', 'uc_e', 'uc_o', 'uc_m']
BND = [(0.0, 0.7), (-0.3, 0.7), (-0.5, 0.6), (0.4, 0.6), (0.0, 0.35), (0.22, 0.42), (0.58, 0.72), (-0.3, 0.2), (-0.3, 0.3), (-0.2, 0.5)]
def score(x, dphase, detail=False):
    p = dict(zip(KEYS, x)); p['dphase'] = dphase; p['zr'] = 0.18; p['cr'] = 0.18; tot = 0.0; worst = 0; out = []
    if p['b'] - p['a'] < 0.2 or p['ua'] > 0.9: return 1e6
    for z in Z:
        try: r = TP.realize(z, br, p)
        except AssertionError: return 1e6
        f = np.r_[r['removed'], np.arange(len(z['Q']), len(r['Q']))]; ang, asp, ba, bs = quality(r['V'], r['Q'][f])
        n = int((ba | bs).sum()); pen = (np.clip(45 - ang, 0, None) ** 2).sum() + (np.clip(ang - 135, 0, None) ** 2).sum() + 50 * (np.clip(asp - 4, 0, None) ** 2).sum()
        tot += n + 1e-3 * pen; worst = max(worst, n); out.append(dict(viol=n, angle=int(ba.sum()), aspect=int(bs.sum()), asp_max=round(float(asp.max()), 3), ang=[round(float(ang.min()), 1), round(float(ang.max()), 1)]))
    return (tot + 2 * worst) if not detail else out
best = None; t0 = time.time()
for dph in (0, 1):
    res = differential_evolution(score, BND, args=(dph,), maxiter=40, popsize=10, seed=7, tol=1e-6, polish=False, updating='deferred', workers=1)
    res2 = minimize(score, res.x, args=(dph,), method='Nelder-Mead', options=dict(maxiter=400, xatol=1e-4, fatol=1e-3))
    x = res2.x if res2.fun < res.fun else res.x; f = min(res.fun, res2.fun)
    print('dphase', dph, 'f %.3f' % f, dict(zip(KEYS, np.round(x, 4))), score(x, dph, True), '%.0fs' % (time.time() - t0), flush=True)
    if best is None or f < best[0]: best = (f, x, dph)
p = dict(zip(KEYS, [round(float(v), 4) for v in best[1]])); p.update(dphase=best[2], zr=0.18, cr=0.18)
json.dump(dict(params=p, score=best[0], detail=score(np.array([p[k] for k in KEYS]), best[2], True), bodies=FAMS), open(OUT, 'w'), indent=1); print('BEST', p)
