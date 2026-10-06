# RAC W1h driver AS RUN (scratch paths = this session's working directories; kept for provenance).
"""Gorrund W1h re-solve (AD-W1H-2, -3, -6, -12): one skeleton recipe evaluated at the reference (229 cm) AND the maximum-stature body
(GOR-BODY-03, ~251 cm) with the CIB bony stations in the loop.
Parameters: pelvis X/Y/Z, femur robusticity, clavicle length, upper-thorax length, ka amplitude, kp at r 0.18/0.31/0.44/0.6,
kb at r 0/0.18/0.31/0.44/0.6/0.8 (all other nodes W1f). Sculpt displacement is confined off the free thigh (confine_legs).
Constraints (slack >= 0):
  reference: every GO skeletal row (margins > / < 1.3 %, >= / <= 0.3 %, ~ 0.007); shares vs GR; chest-lead floors; buttock-lead
             <= 0.023; stature 229 +/- 2; arm clearance >= 0.25 cm in the closed (testable) band; SKIN thoracic breadth / stature
             > SK (1.3 %; AD-W1H-6); SKIN crest flank flare <= 0 (crest on or inside the straight waist-to-hip line, i.e. no convex flank flare; the accepted references read -0.004 ... -0.012; AD-W1H-2).
  GOR-BODY-03: GO ALPC-0...4 rows (same margins), EXCEPT the lower-thorax depth row, which is traced to the generator minimum
             corner at the maximum height macro and is reported separately under CIB and CIB-8 (AD-W1H-3).
Objective after feasibility: least extreme (sum of squared deviations from the generator value; amplitudes toward 0)."""
import sys, os, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn3, gn4, profile_bump as PB, arm_clearance as AC, alpc_invariance as AI
from scipy.optimize import minimize
W1F = gn4.W1F
NAMES = ["pelvisX", "pelvisY", "pelvisZ", "thigh", "clavY", "s03Y", "Aka", "kp18", "kp31", "kp44", "kp60", "kb0", "kb18", "kb31", "kb44", "kb60", "kb80"]
LO = [0.95, 0.97, 1.0, 1.0, 0.85, 1.0, 0.0, 0.9, 0.9, 0.9, 0.85, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
# W1h bounds kept near the W1f / W1g magnitudes (an earlier unbounded W1h run drifted into a waistless, slab-folded trunk)
HI = [1.25, 1.10, 1.35, 1.25, 1.05, 1.25, 1.1, 1.7, 1.7, 1.7, 1.4, 1.3, 1.45, 1.4, 1.3, 1.2, 1.15]
G = gn3.G; F = gn3.F
SK_TB = json.load(open(gn3.SKP.replace('/skp', '/cand') + '/SK_meas.json'))['combined']['ratio']['thorax_breadth_share']
FLARE_MAX = 0.0; CLR = 0.25   # flare: crest on or inside the straight waist-to-hip line (references MF / SK / SG / DU: -0.004 ... -0.012)
LEAD_LEAN, LEAD_ENV = 0.0028, 0.0031
STRESS = {"03": (G + '/h/GO0M251_build.json', G + '/h/GO0M251', 'GO0M251')} if os.environ.get("GN5_STRESS", "1") in ("1", "2") else {}
if os.environ.get("GN5_STRESS") == "2": STRESS["02"] = (F + '/base_w1c/GO208_build.json', F + '/go/GO2080', 'GO2080')   # W1h: minimum stature in the solve

def unpack(x, frame=None):
    x = [float(v) for v in x]
    B = {"pelvis": [x[0], x[1], x[2]], "LR:thigh": [x[3], 1.0, x[3]], "LR:clavicle": [1.0, x[4], 1.0], "spine_03": [1.0, x[5], 1.0]}
    ka = [1 + x[6] * (v - 1) for v in W1F["ka"]]; kp = list(W1F["kp"]); kp[1:5] = x[7:11]
    kb = list(W1F["kb"]); kb[0:6] = x[11:17]
    sc = {"r": W1F["r"], "ka": ka, "kp": kp, "kb": kb, "confine_legs": True}
    if frame:
        for k, v in frame.get("bone_scales", {}).items(): B[k] = [a * b for a, b in zip(B.get(k, [1, 1, 1]), v)]
        if "kb_nodes" in frame: sc["kb"] = [a * b for a, b in zip(sc["kb"], [1.0] + list(frame["kb_nodes"]) + [1.0])]
        for key in ("ka", "kp"):
            if key in frame:
                sc[key] = [a * frame[key] if (0 < i < len(sc[key]) - 1 and sc["r"][i] >= frame.get("kd_from", 0)) else a for i, a in enumerate(sc[key])]
    B = {k: [round(v, 4) for v in vv] for k, vv in B.items()}; sc = {k: ([round(v, 4) for v in vv] if isinstance(vv, list) else vv) for k, vv in sc.items()}
    return B, sc

def rowslack(rows, m, lab, pre, keep=None):
    for y in rows:
        if not (y['cand'] == 'GO' or y.get('b') == 'GO') or y['result'] in ('REPORT', 'NOT RUN'): continue
        if 'SENSITIVITY' in y['check']: continue
        if keep and not keep(y): continue
        for t, v in y['by_t'].items():
            a, b = v['va'], v['vb']
            if a is None or b is None: continue
            op = y['op']
            if 'ALPC-0' in y['check']: m.append(0.0 if a >= 1 else -0.05); lab.append(pre + 'ALPC-0|' + t); continue
            if op == '>': s = (a - b * 1.013) / abs(b)
            elif op == '<': s = (b * 0.987 - a) / abs(b)
            elif op == '>=': s = (a - b * 1.003) / abs(b)
            elif op == '<=': s = (b * 0.997 - a) / abs(b)
            elif op == '~': s = (0.007 - abs(a - b)) / abs(b)
            else: continue
            m.append(s); lab.append('%s%s|%s' % (pre, y['check'][:60], t))

GRr = None
def slacks(x, name, with_stress=True):
    global GRr
    if GRr is None: GRr = {t: json.load(open(gn3.SKP + '/t%s/GR_meas.json' % t))['combined']['ratio'] for t in ('0.0', '0.5', '1.0')}
    B, sc = unpack(x); wd = G + '/solve5'
    r, C = gn3.build("GO", name, B, sc, wd=wd); rows = gn3.checks("GO", name, wd=wd)
    m, lab = [], []; rowslack(rows, m, lab, '')
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
    c = AC.signed_clearance(wd + '/%s_r6.npz' % name); m.append((c - CLR) / 1.0); lab.append('arm clearance %.3f' % c)
    # W1h correction (audit of H8): the skin thoracic breadth must be read exactly as the directional check reads it (arm_measure
    # vertex slabs on the rest body, = thorax_breadth_share); H1-H8 used the plane-section CIB reference reading, which reads ~0.7 % wider.
    from arm_measure import load as _load
    import bony_envelope as BE
    tb = BE.fast_stations(_load(wd + '/%s_rest.npz' % name), section=False)['S2'][0] / H; m.append((tb - SK_TB * 1.013) / SK_TB); lab.append('skin TB/H > SK %.4f' % tb)
    fl = PB.flank_flare(wd + '/%s_r6.npz' % name)['flank_flare']; m.append((FLARE_MAX - fl) / 0.01); lab.append('skin flank flare %.4f' % fl)
    k4 = C.get('station_levels_from_reference', {}).get('S4', 4)     # a real waist: the reference waist minimum may not sit on an end level
    m.append(0.0 if 0 < k4 < 8 else -0.2); lab.append('waist level index %s (must be inside 1..7)' % k4)
    for S_ in ('S2', 'S3', 'S4'):   # no collapsed / folded skeleton slab: every grid body >= 60 % of the reference skin at each station
        mn = min(v['stations'][S_][1] for v in C['per_body'].values()) / C['ref_skin'][S_][1]
        m.append((mn - 0.6) / 0.1); lab.append('slab sanity %s depth %.2f' % (S_, mn))
    if with_stress and STRESS:
        for k, (base, donor, did) in STRESS.items():
            nm = name + '-' + k; gn3.build("GO", nm, B, sc, wd=wd, base=base, donor=donor, did=did); rr = gn3.checks("GO", nm, wd=wd)
            rowslack(rr, m, lab, k + ':', keep=lambda y: AI.keep_row(y['check']) and 'lower-thorax depth' not in y['check'])
    return np.array(m), lab, H, C

def log(f, *a): print(*a, file=f, flush=True)

if __name__ == '__main__':
    x = np.array(json.loads(sys.argv[1]), float); iters = int(sys.argv[2]); tag = sys.argv[3]; reg = float(sys.argv[4])
    free = json.loads(sys.argv[5]) if len(sys.argv) > 5 else list(range(len(x)))
    f = open(G + '/gn5_%s.log' % tag, 'a')
    def sneg(mm): return -mm[mm < 0].sum()
    for it in range(iters):
        m0, lab, H, C = slacks(x, tag + 'c')
        log(f, 'iter', it, json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))), 'H %.2f neg %d sumneg %.4f' % (H, int((m0 < 0).sum()), sneg(m0)))
        for k in np.where(m0 < 0)[0]: log(f, '   neg', lab[k], round(m0[k], 4))
        json.dump({"x": x.tolist(), "names": NAMES, "sumneg": sneg(m0)}, open(G + '/gn5_%s_cur.json' % tag, 'w'))
        h = 0.03
        def col(i):
            xp = x.copy(); xp[i] += h; mp, _, _, _ = slacks(xp, '%sd%d' % (tag, i)); return i, (mp - m0) / h
        J = np.zeros((len(m0), len(x)))
        with ThreadPoolExecutor(2) as ex:
            for i, c in ex.map(col, free): J[:, i] = c
        dev = lambda xn: np.where(np.arange(len(xn)) == 6, xn * 0.1, xn - 1)
        obj = lambda d: (np.minimum(0, m0 + J @ d) ** 2).sum() * 1e4 + 0.02 * (d ** 2).sum() + reg * (dev(x + d) ** 2).sum()
        mask = np.zeros(len(x)); mask[free] = 1
        bnds = [(max(-0.12, LO[i] - x[i]), min(0.12, HI[i] - x[i])) if mask[i] else (0, 0) for i in range(len(x))]
        d = minimize(obj, np.zeros(len(x)), method='L-BFGS-B', bounds=bnds).x
        best = None
        for a in (1.0, 0.5, 0.25):
            xn = x + a * d; mn, _, Hn, _ = slacks(xn, tag + 'c')
            log(f, '   step a=%.2f sumneg %.4f neg %d' % (a, sneg(mn), int((mn < 0).sum())))
            score = sneg(mn) + (reg * (dev(xn) ** 2).sum() if sneg(mn) < 1e-4 else 0)
            if best is None or score < best[0]: best = (score, xn, sneg(mn))
        cur = sneg(m0) + (reg * (dev(x) ** 2).sum() if sneg(m0) < 1e-4 else 0)
        if best[0] < cur - 1e-6: x = best[1]
        else: log(f, 'no improvement'); break
    json.dump({"x": x.tolist(), "names": NAMES}, open(G + '/gn5_%s_best.json' % tag, 'w'), indent=1)
    log(f, 'DONE', json.dumps(dict(zip(NAMES, np.round(x, 4).tolist()))))
