# RAC W1g driver AS RUN (scratch paths = this session's working directories; kept for provenance).
"""Gorrund AD-G14 re-solve WITH the CIB bony envelope in the loop (AD-W1G-1, AD-W1G-3).
Parameters (x): pelvis X/Y/Z, femur (thigh X=Z robusticity), clavicle length, upper-thorax length, ka amplitude (multiplying the W1f
anterior depth profile deviations), kp (posterior depth) at nodes r = 0.18 ... 0.6 and kb at nodes r = 0 ... 0.44 (other nodes W1f).
Feasibility = every GO skeletal row passes with margin (> / < : 1.3 %, >= / <= : 0.3 %, ~ : within 0.007), torso share > GR,
leg < GR, arm < GR (1.3 %), chest-lead not below the W1f GO skeleton / envelope values (0.0029 / 0.0031), buttock-lead <= 0.023, stature 229 +/- 2.
Least-extreme: among feasible steps the objective adds sum((x - 1)^2) (amplitudes toward 0 deviation), so values are pulled to
the smallest deviation from the generator that keeps every accepted relation."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn3, profile_bump as PB
from scipy.optimize import minimize
W1F = {"r": [0.0, 0.18, 0.31, 0.44, 0.6, 0.8, 1.0, 1.15], "ka": [1.0, 1.0, 1.0, 1.06, 1.16, 1.08, 1.02, 1.0],
       "kp": [1.0, 1.25, 1.5, 1.65, 1.35, 1.0, 0.97, 1.0], "kb": [1.0, 1.16, 1.19, 1.16, 1.11, 1.06, 1.03, 1.0]}
NAMES = ["pelvisX", "pelvisY", "pelvisZ", "thigh", "clavY", "s03Y", "Aka", "kp18", "kp31", "kp44", "kp60", "kb0", "kb18", "kb31", "kb44"]
X0 = [1.10, 1.045, 1.28, 1.20, 0.90, 1.186, 1.0, 1.25, 1.5, 1.65, 1.35, 1.0, 1.16, 1.19, 1.16]
LO = [1.0, 0.97, 1.0, 1.0, 0.85, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.95, 0.95, 0.95, 0.95]
# W1g least extreme: femur and ka amplitude capped at W1f; no posterior-depth node above the W1f maximum factor (1.65)
HI = [1.3, 1.1, 1.4, 1.2, 1.05, 1.25, 1.0, 1.65, 1.65, 1.65, 1.35, 1.35, 1.4, 1.35, 1.3]   # posterior-depth nodes capped at the W1f maximum factor 1.65

def unpack(x, frame=None):
    x = [float(v) for v in x]
    B = {"pelvis": [x[0], x[1], x[2]], "LR:thigh": [x[3], 1.0, x[3]], "LR:clavicle": [1.0, x[4], 1.0], "spine_03": [1.0, x[5], 1.0]}
    ka = [1 + x[6] * (v - 1) for v in W1F["ka"]]; kp = list(W1F["kp"]); kp[1], kp[2], kp[3], kp[4] = x[7], x[8], x[9], x[10]
    kb = list(W1F["kb"]); kb[0], kb[1], kb[2], kb[3] = x[11], x[12], x[13], x[14]; kb[4], kb[5] = KB_UPPER
    sc = {"r": W1F["r"], "ka": ka, "kp": kp, "kb": kb}
    if frame:
        for k, v in frame.get("bone_scales", {}).items(): B[k] = [a * b for a, b in zip(B.get(k, [1, 1, 1]), v)]
        if "kb_nodes" in frame: sc["kb"] = [a * b for a, b in zip(sc["kb"], [1.0] + list(frame["kb_nodes"]) + [1.0])]
        for key in ("ka", "kp"):
            if key in frame:
                sc[key] = [a * frame[key] if (0 < i < len(sc[key]) - 1 and sc["r"][i] >= frame.get("kd_from", 0)) else a for i, a in enumerate(sc[key])]
    B = {k: [round(v, 4) for v in vv] for k, vv in B.items()}; sc = {k: [round(v, 4) for v in vv] for k, vv in sc.items()}
    return B, sc

GRr = None
# AD-W1G-4 (adopted after the shrink pass): upper-thorax breadth nodes r = 0.6 / 0.8 lowered from the W1f 1.11 / 1.06 to 1.05 / 1.02
# (less extreme) so the hanging arm clears the trunk at the reference AND the 208 / 215 cm bodies (probe5: clearance 0.71 / 0.29 /
# 0.42 cm); 1.03 / 1.00 would break thoracic breadth / stature > SK. Set KB_UPPER = [1.11, 1.06] to reproduce the solver runs.
KB_UPPER = [1.05, 1.02]
LEAD_LEAN, LEAD_ENV = 0.0028, 0.0031   # chest-lead floors: W1f GO envelope value (0.00315) and W1f skeleton value (0.00291) less 0.0001
CLR = 0.25      # cm: required signed arm-to-trunk-section clearance (builder threshold above mesh noise; disclosed)
def slacks(x, name, lead=0.003):
    global GRr
    if GRr is None: GRr = {t: json.load(open(gn3.SKP + '/t%s/GR_meas.json' % t))['combined']['ratio'] for t in ('0.0', '0.5', '1.0')}
    B, sc = unpack(x); r, C = gn3.build("GO", name, B, sc); rows = gn3.checks("GO", name); wd = gn3.G + '/solve_GO'
    m, lab = [], []
    for y in rows:
        if not (y['cand'] == 'GO' or y.get('b') == 'GO') or y['result'] in ('REPORT', 'NOT RUN'): continue
        for t, v in y['by_t'].items():
            a, b = v['va'], v['vb']
            if a is None or b is None: continue
            op = y['op']; sign = 1 if y['cand'] == 'GO' else -1
            if 'ALPC-0' in y['check']: m.append(0.0 if a >= 1 else -0.05); lab.append('ALPC-0|' + t); continue
            if op == '>': s = (a - b * 1.013) / abs(b)
            elif op == '<': s = (b * 0.987 - a) / abs(b)
            elif op == '>=': s = (a - b * 1.003) / abs(b)
            elif op == '<=': s = (b * 0.997 - a) / abs(b)
            elif op == '~': s = (0.007 - abs(a - b)) / abs(b)
            else: continue
            m.append(s); lab.append('%s|%s' % (y['check'][:60], t))
    sk = json.load(open(wd + '/skp_%s/%s_skp.json' % (name, name)))
    for t in ('0.0', '0.5', '1.0'):
        R = sk['by_t'][t]['ratio']
        m.append((R['torso_share'] - GRr[t]['torso_share'] * 1.013) / GRr[t]['torso_share']); lab.append('torso>GR|' + t)
        m.append((GRr[t]['leg_share'] * 0.987 - R['leg_share']) / GRr[t]['leg_share']); lab.append('leg<GR|' + t)
        m.append((GRr[t]['arm_share'] * 0.987 - R['arm_share']) / GRr[t]['arm_share']); lab.append('arm<GR|' + t)
    for nm, lv in ((name + '-LEAN', LEAD_LEAN), (name, LEAD_ENV)):
        b = PB.chest_lead(wd + '/%s_r6.npz' % nm); m.append((b - lv) / 0.01); lab.append('chest-lead ' + nm)
    b = PB.buttock_lead(wd + '/%s_r6.npz' % name); m.append((0.023 - b) / 0.01); lab.append('buttock-lead')
    H = r['r6']['stature']; m.append((2.0 - abs(H - 229.0)) / 100); lab.append('stature')
    import arm_clearance as AC      # AD-W1G-4: clean neutral-pose (R-6) arm-to-trunk clearance on the reference envelope
    c = AC.signed_clearance(wd + '/%s_r6.npz' % name); m.append((c - CLR) / 1.0); lab.append('arm clearance %.3f' % c)
    return np.array(m), lab, H, C

def log(f, *a):
    print(*a, file=f, flush=True)

if __name__ == '__main__':
    x = np.array(json.loads(sys.argv[1]), float); iters = int(sys.argv[2]); tag = sys.argv[3]; reg = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
    free = json.loads(sys.argv[5]) if len(sys.argv) > 5 else list(range(len(x)))
    f = open(gn3.G + '/gn4_%s.log' % tag, 'a')
    for it in range(iters):
        m0, lab, H, C = slacks(x, tag + 'c')
        log(f, 'iter', it, json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))), 'H %.2f' % H, 'neg', int((m0 < 0).sum()), 'sumneg %.4f' % (-m0[m0 < 0].sum()),
            'S5 %.2f S2 %.2f' % (C['bony']['S5'][0], C['bony']['S2'][0]))
        for k in np.where(m0 < 0)[0]: log(f, '   neg', lab[k], round(m0[k], 4))
        json.dump({"x": x.tolist(), "neg": int((m0 < 0).sum()), "H": H}, open(gn3.G + '/gn4_%s_cur.json' % tag, 'w'))
        h = 0.03; J = np.zeros((len(m0), len(x)))
        for i in free:
            xp = x.copy(); xp[i] += h; mp, _, _, _ = slacks(xp, tag + 'd'); J[:, i] = (mp - m0) / h
        lo, hi = np.array(LO), np.array(HI); dev = np.where(np.arange(len(x)) >= 6, np.where(np.arange(len(x)) < 8, x, x - 1), x - 1)
        def obj(d):
            xn = x + d; dv = np.where(np.arange(len(x)) == 6, xn * 0.1, xn - 1)
            return (np.minimum(0, m0 + J @ d) ** 2).sum() * 1e4 + 0.02 * (d ** 2).sum() + reg * (dv ** 2).sum()
        mask = np.zeros(len(x)); mask[free] = 1
        bnds = [(max(-0.15, lo[i] - x[i]), min(0.15, hi[i] - x[i])) if mask[i] else (0, 0) for i in range(len(x))]
        d = minimize(obj, np.zeros(len(x)), method='L-BFGS-B', bounds=bnds).x
        best = None
        for a in (1.0, 0.5, 0.25):
            xn = x + a * d; mn, _, Hn, _ = slacks(xn, tag + 'c'); sc_ = -mn[mn < 0].sum()
            log(f, '   step a=%.2f sumneg %.4f neg %d H %.2f' % (a, sc_, int((mn < 0).sum()), Hn))
            if best is None or sc_ < best[0]: best = (sc_, xn)
        if best[0] <= -m0[m0 < 0].sum() + 1e-5: x = best[1]
        else: log(f, 'no improvement'); break
    json.dump({"x": x.tolist(), "names": NAMES}, open(gn3.G + '/gn4_%s_best.json' % tag, 'w'), indent=1)
    log(f, 'DONE', json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))))
