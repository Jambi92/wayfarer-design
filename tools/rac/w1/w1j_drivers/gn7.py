# RAC W1j driver (scratch paths = this session's working directories; kept for provenance).
"""Gorrund W1j robustness re-solve (order reviews/chatgpt-rac-w1i-author-decisions-w1j-robustness-order.md).

Same recipe, parameters and bodies as W1i gn6 (w1i_drivers/gn6.py), with three changes:
 1. ORDINARY thresholds instead of the W1i robustness margins (order §3, §4: trade surplus margin for an interior solution, never
    below the accepted thresholds): strict > / < by 1.1 % (1 % convention + 0.1 %), >= / <= by 0.1 %, '~' within 0.0095; skin
    thoracic breadth > SK by 1.1 %.
 2. LINEARISED +/-2 % ROBUSTNESS (order §4): every accepted relation r (all skeletal rows at every body and pair, thoracic breadth > SK)
    must keep slack_r >= max_i |dslack_r/dx_i| * h_i, where h_i is the +/-2 % step of value i (ka amplitude 0.05) - i.e. each single
    +/-2 % perturbation of the sensitivity protocol keeps the relation, to first order. The Jacobian of the current iterate is used.
 3. LOW COMPOSITION AND TRUE MINIMUM IN THE LOOP (order §5, §7): the stature series uses the true ~208 cm donor (height macro 0.685,
    w1i_drivers/true208.py) instead of the W1f 208 cm donor, with the equal-height ALPC-7 pair vs Broad Skarn 208 added; the
    low-composition grid body (muscle 0.25 / weight 0.25) of the reference AND of the 208 cm body must keep, against MF and SK at the
    SAME composition (w1f/low): waist / hip-block >= the larger reference (no pelvic shelf), waist / thorax >= the larger reference
    (no pinch), and a waist above the crest (plane-section crest / narrowest level above it >= 1.01).
Objective: least squares of the robust shortfalls + a barrier that keeps every value out of the outer 5 % of its bound range +
a small pull toward the generator value. FEMUR_HI (env GN7_FEMUR_HI) caps femur robusticity for the trade study (order §3)."""
import sys, os, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, gn3
from scipy.optimize import minimize
G, F, S = gn3.G, gn3.F, gn3.S
gn6.M_STRICT, gn6.M_GE, gn6.M_TILDE = 0.011, 0.001, 0.0095
gn6.CLR = 0.25
gn6.HEIGHTS = {"208": (G + '/h/GO0M208_build.json', G + '/h/GO0M208', 'GO0M208'), "215": gn6.HEIGHTS["215"], "222": gn6.HEIGHTS["222"], "03": gn6.HEIGHTS["03"]}
gn6.PAIRS = {"208": (208, 215, 222, 229), "215": (222, 229), "222": (229,)}
NAMES, LO, HI = gn6.NAMES, list(gn6.LO), list(gn6.HI)
FEMUR_HI = float(os.environ.get("GN7_FEMUR_HI", "1.40")); HI[NAMES.index("thigh")] = FEMUR_HI
STEP = np.array([0.05 if n == "Aka" else None for n in NAMES], dtype=object)
LOWREF = {k: gn6.cont(p) for k, p in (("MF-M-R low", F + '/low/MF-M-R-LOW_rest.npz'), ("SK low", F + '/low/SK-LOW_rest.npz'))}
LOWLIM = {"waist_over_hip_min": max(v["waist_over_hip"] for v in LOWREF.values()), "waist_over_thorax_min": max(v["waist_over_thorax"] for v in LOWREF.values())}

def robust_row(label):
    """accepted relations (counted by the +/-2 % protocol): skeletal rows (label ends in |t) and thoracic breadth > SK"""
    return label.startswith('skin TB/H > SK') or (('|0.' in label or '|1.' in label) and not label.startswith(('torso>GR', 'leg<GR', 'arm<GR')))

def slacks(x, name, wd=None):
    wd = wd or G + '/solve7'
    m, lab, H, C = gn6.slacks(x, name, wd=wd)
    m, lab = list(m), list(lab)
    for nm in (name, name + '-208'):
        gp = wd + '/grid_%s/%s-C025025_rest.npz' % (nm, nm); c = gn6.cont(gp); wr = gn6.waist_rise(gp)
        m.append((c["waist_over_hip"] - LOWLIM["waist_over_hip_min"]) / LOWLIM["waist_over_hip_min"]); lab.append('%s low-comp waist/hip %.4f >= low refs' % (nm, c["waist_over_hip"]))
        m.append((c["waist_over_thorax"] - LOWLIM["waist_over_thorax_min"]) / LOWLIM["waist_over_thorax_min"]); lab.append('%s low-comp waist/thorax %.4f >= low refs' % (nm, c["waist_over_thorax"]))
        m.append(wr - 1.01); lab.append('%s low-comp waist rise %.4f >= 1.01' % (nm, wr))
    return np.array(m), lab, H, C

def hstep(x): return np.array([0.05 if n == "Aka" else 0.02 * abs(v) for n, v in zip(NAMES, x)])

def robust(m, lab, J, x):
    R = np.max(np.abs(J) * hstep(x)[None, :], axis=1); mask = np.array([robust_row(l) for l in lab])
    return m - np.where(mask, R, 0.0), mask

def barrier(xn):
    lo, hi = np.array(LO), np.array(HI); w = (hi - lo) * 0.05 + 1e-9
    return (np.maximum(0, (lo + w) - xn) / w) ** 2 + (np.maximum(0, xn - (hi - w)) / w) ** 2

def log(f, *a): print(*a, file=f, flush=True)

if __name__ == '__main__':
    x = np.array(json.loads(sys.argv[1]), float); iters = int(sys.argv[2]); tag = sys.argv[3]
    f = open(G + '/gn7_%s.log' % tag, 'a'); log(f, 'W1j gn7 FEMUR_HI %.3f LOWLIM %s margins %s %s %s' % (FEMUR_HI, json.dumps(LOWLIM), gn6.M_STRICT, gn6.M_GE, gn6.M_TILDE))
    J0 = os.environ.get('GN7_J0')
    def sneg(v): return -v[v < 0].sum()
    for it in range(iters):
        m0, lab, H, C = slacks(x, tag + 'c')
        if it == 0 and J0: J = np.load(J0); log(f, '   Jacobian loaded', J0)
        else:
            h = 0.02
            def col(i):
                xp = x.copy(); xp[i] += h; mp, _, _, _ = slacks(xp, '%sd%d' % (tag, i)); return i, (mp - m0) / h
            J = np.zeros((len(m0), len(x)))
            with ThreadPoolExecutor(2) as ex:
                for i, c in ex.map(col, range(len(x))): J[:, i] = c
        np.save(G + '/gn7_%s_J%d.npy' % (tag, it), J); json.dump({"x": x.tolist(), "labels": lab, "m": m0.tolist()}, open(G + '/gn7_%s_pt%d.json' % (tag, it), 'w'))
        r0, mask = robust(m0, lab, J, x)
        log(f, 'iter', it, json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))), 'H %.2f ordinary-neg %d sum %.4f | robust-neg %d sum %.4f' % (H, int((m0 < 0).sum()), sneg(m0), int((r0 < 0).sum()), sneg(r0)))
        for k in np.where(r0 < 0)[0]: log(f, '   rneg', lab[k], 'slack %.4f robust %.4f' % (m0[k], r0[k]))
        def obj(d):
            xn = x + d; rn, _ = robust(m0 + J @ d, lab, J, xn)
            return (np.minimum(0, rn) ** 2).sum() * 1e4 + 0.05 * (d ** 2).sum() + 2.0 * barrier(xn).sum() + 0.001 * ((xn - 1) ** 2).sum()
        bnds = [(max(-0.08, LO[i] - x[i]), min(0.08, HI[i] - x[i])) for i in range(len(x))]
        d = minimize(obj, np.zeros(len(x)), method='L-BFGS-B', bounds=bnds).x
        log(f, '   predicted robust-neg sum %.4f' % sneg(robust(m0 + J @ d, lab, J, x + d)[0]))
        best = None
        for a in (1.0, 0.5):
            xn = x + a * d; mn, _, _, _ = slacks(xn, tag + 'c'); rn, _ = robust(mn, lab, J, xn)
            sc_ = sneg(rn) + 0.01 * barrier(xn).sum()
            log(f, '   step a=%.2f ordinary-neg %d sum %.4f robust-neg %d sum %.4f score %.5f' % (a, int((mn < 0).sum()), sneg(mn), int((rn < 0).sum()), sneg(rn), sc_))
            if best is None or sc_ < best[0]: best = (sc_, xn)
        if best[0] < sneg(r0) + 0.01 * barrier(x).sum() - 1e-6: x = best[1]
        else: log(f, 'no improvement'); break
        json.dump({"x": x.tolist(), "names": NAMES}, open(G + '/gn7_%s_cur.json' % tag, 'w'))
    json.dump({"x": x.tolist(), "names": NAMES}, open(G + '/gn7_%s_best.json' % tag, 'w'), indent=1)
    log(f, 'DONE', json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))))
