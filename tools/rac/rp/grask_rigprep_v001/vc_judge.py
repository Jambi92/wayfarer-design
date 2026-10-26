# vc_judge.py WORKDIR BASEDIR HELPERDIR : Track E tables + the §10 acceptance checks (order 69f2660). W0 / C2 / C2rx from BASEDIR (r4), H2 from HELPERDIR (r5),
# VC1-VC3 from WORKDIR. closed-mesh volume vs W0 LBS of the same pose; 'corrective-caused loss' = -(V_candidate - V_W0) (positive = volume lost).
import sys, os, json, numpy as np
W, BD, HD = sys.argv[1:4]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); Q = np.asarray(Z['Q'])
def cvol(V):
    T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', V[T_[:, 0]], np.cross(V[T_[:, 1]], V[T_[:, 2]])).sum() / 6)
ANG = (45, 60, 75, 90, 110, 120, 130)
def load(d, s, t):
    R = json.load(open('%s/diag/diag_results_c_%s_%s.json' % (d, s, t)))['results']; out = {}
    for a in ANG:
        p = 'D2_%s_flex%d' % (s, a); r = R[p]; i = r['intersections']
        out[a] = dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 2), orient=r['flips']['total'], inv=r['inversions']['total'], folds=r['folds']['new'],
                      folds_out=r['folds']['outside'], loop=round(r['loop_spacing_min_ratio'], 3), p95=round(r['strain']['zone_p95_pct'], 1), smax=round(r['strain']['zone_max_pct'], 1),
                      zone=round(r['volume']['zone_pct'], 2), T1=r['rest_return_T1_mm'], fails=sorted(c[0] for c in crit(p, r) if not c[1]),
                      vol=cvol(np.load('%s/diag/posed/%s_c_%s_%s.npz' % (d, p, s, t))['V'].astype(float)))
    return out
SETS = {'l': [('W0', BD, 'W0'), ('C2', BD, 'C2'), ('H2', HD, 'H2'), ('VC1', W, 'VC1'), ('VC2', W, 'VC2'), ('VC3', W, 'VC3')],
        'r': [('W0', BD, 'W0'), ('C2rx', BD, 'C2rx'), ('H2', HD, 'H2'), ('VC1', W, 'VC1r'), ('VC2', W, 'VC2r'), ('VC3', W, 'VC3r')]}
OUT = {}; MD = ['cells: non-contact / crease (depth mm) / orientation / local inv / folds outside / loop / p95 (max) strain % / zone proxy % / dV vs W0 cm3 [failing retained criteria]']
for s, sets in SETS.items():
    D = {n: load(d, s, t) for n, d, t in sets}; OUT[s] = D
    MD += ['', '### %s side' % ('left' if s == 'l' else 'right'), '', '| angle | ' + ' | '.join(n for n, _, _ in sets) + ' |', '|---|' + '---|' * len(sets)]
    for a in ANG:
        cells = []
        for n, _, _ in sets:
            k = D[n][a]; cells.append('%d / %d (%.1f) / %d / %d / %d / %.2f / %.0f (%.0f) / %.1f / %+.0f [%d]' % (k['nc'], k['crease'], k['depth'], k['orient'], k['inv'], k['folds_out'], k['loop'], k['p95'], k['smax'], k['zone'], k['vol'] - D['W0'][a]['vol'], len(k['fails'])))
        MD.append('| %d | %s |' % (a, ' | '.join(cells)))
CHK = {}
for s in ('l', 'r'):
    D = OUT[s]; ref = 'C2' if s == 'l' else 'C2rx'; W0 = D['W0']; R = D[ref]; H2 = D['H2']; dv = lambda X, a: X[a]['vol'] - W0[a]['vol']
    for h in ('VC1', 'VC2', 'VC3'):
        H = D[h]; loss_ref = -dv(R, 130); loss_h = -dv(H, 130); red = (loss_ref - loss_h) / loss_ref if loss_ref > 0 else None
        zgap = lambda X: abs(X[130]['zone'] - W0[130]['zone'])
        c = {'I1 nc = 0 at 130': H[130]['nc'] == 0,
             'I2 no new local inversions vs %s (90-130)' % ref: all(H[a]['inv'] <= R[a]['inv'] for a in (90, 110, 120, 130)),
             'I3 no folds outside the crease/contact zone (90-130)': all(H[a]['folds_out'] == 0 for a in (90, 110, 120, 130)),
             'I4 rest return ~ 0 (T-1 < 1e-6 mm)': all(abs(H[a]['T1']) < 1e-6 for a in ANG),
             'C1 130 crease depth <= %s + 0.5 mm' % ref: H[130]['depth'] <= R[130]['depth'] + 0.5,
             'C1p preferred 130 crease <= 3.5 mm': H[130]['depth'] <= 3.5,
             'O1 orientation 130 not materially worse than %s (<= +10 %% / +5)' % ref: H[130]['orient'] <= max(R[130]['orient'] * 1.1, R[130]['orient'] + 5),
             'O1p preferred orientation 130 <= %d' % (100 if s == 'l' else 90): H[130]['orient'] <= (100 if s == 'l' else 90),
             'O2 orientation 120 within the 130 preferred limit (<= %d; reported vs %s too)' % (100 if s == 'l' else 90, ref): H[120]['orient'] <= (100 if s == 'l' else 90),
             'L1 loop >= 0.50 at 130': H[130]['loop'] >= 0.5,
             'L2 loop not sacrificed at 120/130 (>= %s)' % ref: all(H[a]['loop'] >= min(R[a]['loop'], 0.5) for a in (120, 130)),
             'V1 >= 50 %% reduction of corrective-caused 130 loss vs %s' % ref: red is not None and red >= 0.5,
             'V1p preferred <= 120 cm3 absolute loss at 130': loss_h <= 120,
             'Z1 130 zone proxy closer to W0 than %s' % ref: zgap(H) < zgap(R),
             'S1 p95 strain <= %s + 5 pp at 120 and 130' % ref: all(H[a]['p95'] <= R[a]['p95'] + 5 for a in (120, 130)),
             'S2 130 max strain below the H2 failed-130 spike (%.0f %%)' % H2[130]['smax']: H[130]['smax'] < H2[130]['smax'],
             'R1 90 / 110 identical to %s (no activation below 120)' % ref: all(H[a] == R[a] for a in (45, 60, 75, 90)) and H[110]['vol'] == R[110]['vol']}
        hard = [k for k in c if not k.split()[0].endswith('p')]
        CHK['%s_%s' % (h, s)] = dict(checks=c, hard_pass=all(c[k] for k in hard), volume_loss_130_ref_cm3=round(loss_ref, 1), volume_loss_130_cm3=round(loss_h, 1),
                                    loss_reduction_130=None if red is None else round(red, 3), crease_130_mm=H[130]['depth'], orient_130=H[130]['orient'], loop_130=H[130]['loop'],
                                    p95_130=H[130]['p95'], max_130=H[130]['smax'], zone_130=H[130]['zone'])
json.dump(dict(tables=OUT, checks=CHK), open(W + '/diag/trackE_judgement.json', 'w'), indent=1, default=float)
open(W + '/diag/trackE_tables.md', 'w').write('\n'.join(MD) + '\n'); print('\n'.join(MD))
for k, v in CHK.items(): print(k, 'HARD PASS' if v['hard_pass'] else 'fail', 'loss130 ref %.0f -> %.0f (reduction %s)' % (v['volume_loss_130_ref_cm3'], v['volume_loss_130_cm3'], v['loss_reduction_130']), [n for n, ok in v['checks'].items() if not ok])
