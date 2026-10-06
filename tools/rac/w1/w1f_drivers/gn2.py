# RAC W1f driver script AS RUN (scratch paths are the session's working directories; kept for provenance of the AD-G14 construction)
"""GN solver over AD-G14 skeleton parameters: bone scales (joint-moving) + skeletal trunk sculpt profile."""
import sys, json, os, numpy as np, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import search as S, skeleton_envelope as SE, skeletal_checks as SC, profile_bump as PB
from scipy.optimize import minimize
F = S.F; T = S.T; D = F + '/go'
RN = [0.18, 0.31, 0.44, 0.6, 0.8, 1.0]
NAMES = ["pelvisX", "pelvisY", "pelvisZ", "thigh", "clavY", "s03Y"] + ["ka%.2f" % r for r in RN] + ["kp%.2f" % r for r in RN] + ["kb%.2f" % r for r in RN]
GRr = {t: json.load(open(F + '/skp/t%s/GR_meas.json' % t))['combined']['ratio'] for t in ('0.0', '0.5', '1.0')}
def unpack(x):
    B = {"pelvis": [x[0], x[1], x[2]], "LR:thigh": [x[3], 1.0, x[3]], "LR:clavicle": [1.0, x[4], 1.0], "spine_03": [1.0, x[5], 1.0]}
    B = {k: [round(float(v), 4) for v in vv] for k, vv in B.items()}
    sc = {"r": [0.0] + RN + [1.15], "ka": [1.0] + [round(float(v), 4) for v in x[6:12]] + [1.0], "kp": [1.0] + [round(float(v), 4) for v in x[12:18]] + [1.0],
          "kb": [1.0] + [round(float(v), 4) for v in x[18:24]] + [1.0]}
    return B, sc
TISSUE = {"mode": os.environ.get("TISSUE", "race")}
def build(x, name, base=F + '/base_w1c/GO_build.json', donor=D + '/GO0', frame=None, comp_donor=None, tissue=None):
    B, sc = unpack(x)
    if frame:
        for k, v in frame.get("bone_scales", {}).items():
            B[k] = [round(a * b, 4) for a, b in zip(B.get(k, [1, 1, 1]), v)]
        for key in ("ka", "kp", "kb"):
            if key + "_nodes" in frame:
                mult = [1.0] + list(frame[key + "_nodes"]) + [1.0]
                sc[key] = [round(a * b, 4) for a, b in zip(sc[key], mult)]; continue
            if key in frame:
                r0 = frame.get(key + "_from", frame.get("kd_from", 0.0) if key in ("ka", "kp") else 0.0)
                sc[key] = [round(a * frame[key], 4) if (0 < i < len(sc[key]) - 1 and sc["r"][i] >= r0) else a for i, a in enumerate(sc[key])]
    ov = {"muscle": 0.0, "weight": 0.0, "bone_scales": B}; json.dump(ov, open(D + '/%s_ov.json' % name, 'w'))
    subprocess.run(['python3', T + '/build_variant.py', base, D + '/%s_ov.json' % name, D, name + '-LEAN'], check=True, capture_output=True)
    mode = tissue or TISSUE["mode"]
    if mode == "MF":      # human reference composition distribution (MF-M-R), size-scaled by stature ratio
        Hs = 228.77 / 173.143
        dref = F + ('/low/MF-M-R-LOW' if comp_donor else '/ref/MF-M-R')
        r = SE.make(D + '/' + name + '-LEAN', dref, F + '/lean/MF-M-R-LEAN', D + '/' + name, tag=name, sculpt=sc, tissue_scale=Hs)
    else:
        dref = comp_donor or donor
        r = SE.make(D + '/' + name + '-LEAN', dref, donor + '-LEAN', D + '/' + name, tag=name, sculpt=sc)
    subprocess.run(['python3', T + '/skeletal_proxy.py', D, D, name, D + '/skp_' + name], check=True, capture_output=True)
    return B, sc, r
def checks(name):
    tmp = D + '/chk_' + name
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(F + '/skp', tmp, symlinks=True)
    for t in ('0.0', '0.5', '1.0'):
        dst = tmp + '/t%s/GO_meas.json' % t
        if os.path.lexists(dst): os.remove(dst)
        shutil.copy(D + '/skp_%s/t%s/%s_meas.json' % (name, t, name), dst)
    return SC.run(tmp)
def slacks(x, name, lead=0.0045):
    B, sc, r = build(x, name); rows = checks(name)
    mine = [y for y in rows if (y['cand'] == 'GO' or y.get('b') == 'GO') and y['result'] not in ('REPORT', 'NOT RUN')]
    m, lab = [], []
    for y in mine:
        for t, v in y['by_t'].items():
            a, b = v['va'], v['vb']
            if a is None or b is None: continue
            op = y['op']
            if 'ALPC-0' in y['check']: m.append(0.0 if a >= 1 else -0.05); lab.append('ALPC-0|' + t); continue
            if op == '>': s = (a - b * 1.013) / abs(b)
            elif op == '<': s = (b * 0.987 - a) / abs(b)
            elif op == '>=': s = (a - b * 1.003) / abs(b)
            elif op == '<=': s = (b * 0.997 - a) / abs(b)
            elif op == '~': s = (0.007 - abs(a - b)) / abs(b)
            else: continue
            m.append(s); lab.append('%s|%s' % (y['check'][:60], t))
    sk = json.load(open(D + '/skp_%s/%s_skp.json' % (name, name)))
    for t in ('0.0', '0.5', '1.0'):
        R = sk['by_t'][t]['ratio']
        m.append((R['torso_share'] - GRr[t]['torso_share'] * 1.013) / GRr[t]['torso_share']); lab.append('torso>GR|' + t)
        m.append((GRr[t]['leg_share'] * 0.987 - R['leg_share']) / GRr[t]['leg_share']); lab.append('leg<GR|' + t)
        m.append((GRr[t]['arm_share'] * 0.987 - R['arm_share']) / GRr[t]['arm_share']); lab.append('arm<GR|' + t)
    for nm in (name + '-LEAN', name):
        b = PB.chest_lead(D + '/%s_r6.npz' % nm); m.append((b - lead) / 0.01); lab.append('chest-lead ' + nm)
    b = PB.buttock_lead(D + '/%s_r6.npz' % name); m.append((0.023 - b) / 0.01); lab.append('buttock-lead ' + name)
    H = r['r6']['stature']; m.append((2.0 - abs(H - 229.0)) / 100); lab.append('stature')
    return np.array(m), lab, H
if __name__ == '__main__':
    x = np.array(json.loads(sys.argv[1]), float); iters = int(sys.argv[2]); tag = sys.argv[3]
    log = open(D + '/gn2_%s.log' % tag, 'a')
    for it in range(iters):
        m0, lab, H = slacks(x, tag + 'c')
        print('iter', it, json.dumps(unpack(x)), 'H %.2f' % H, 'neg', int((m0 < 0).sum()), 'sumneg %.4f' % (-m0[m0 < 0].sum()), file=log, flush=True)
        for k in np.where(m0 < 0)[0]: print('   neg', lab[k], round(m0[k], 4), file=log, flush=True)
        json.dump({"x": x.tolist(), "unpack": unpack(x), "H": H, "neg": int((m0 < 0).sum())}, open(D + '/gn2_%s_cur.json' % tag, 'w'))
        if (m0 >= 0).all(): break
        h = 0.03; J = np.zeros((len(m0), len(x)))
        for i in range(len(x)):
            xp = x.copy(); xp[i] += h; mp, _, _ = slacks(xp, tag + 'd'); J[:, i] = (mp - m0) / h
        LO = np.array([1.0, 0.97, 1.0, 1.0, 0.85, 1.0] + [0.95] * 12 + [0.9] * 6); HI = np.array([1.25, 1.1, 1.4, 1.3, 1.05, 1.2] + [1.5] * 12 + [1.3] * 6)
        def rough(y):
            return sum((np.diff(np.r_[1.0, y[a:a + 6], 1.0], 2) ** 2).sum() for a in (6, 12, 18))
        f = lambda d: (np.minimum(0, m0 + J @ d) ** 2).sum() * 1e4 + 0.02 * (d ** 2).sum() + 0.002 * ((x + d - 1) ** 2).sum() + 2.0 * rough(x + d)
        bnds = [(max(-0.15, LO[i] - x[i]), min(0.15, HI[i] - x[i])) for i in range(len(x))]
        d = minimize(f, np.zeros(len(x)), method='L-BFGS-B', bounds=bnds).x
        best = None
        for a in (1.0, 0.5, 0.25):
            xn = x + a * d; mn, _, Hn = slacks(xn, tag + 'c'); sc_ = -mn[mn < 0].sum()
            print('   step a=%.2f sumneg %.4f neg %d H %.2f' % (a, sc_, int((mn < 0).sum()), Hn), file=log, flush=True)
            if best is None or sc_ < best[0]: best = (sc_, xn)
        if best[0] < -m0[m0 < 0].sum() - 1e-5: x = best[1]
        else: print('no improvement', file=log, flush=True); break
    json.dump({"x": x.tolist(), "unpack": unpack(x)}, open(D + '/gn2_%s_best.json' % tag, 'w'), indent=1)
    print('DONE', json.dumps(unpack(x)), file=log, flush=True)
