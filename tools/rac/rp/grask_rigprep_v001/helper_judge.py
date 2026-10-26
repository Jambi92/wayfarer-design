# helper_judge.py WORKDIR BASEDIR : Stage A tables and the §7 acceptance checks (order 8e5021d). W0 and C2 / C2rx from BASEDIR (r4), H1-H3 from WORKDIR.
# closed-mesh volume change vs W0 LBS of the same pose; 'corrective-caused loss' = -(V_candidate - V_W0) (positive = volume lost).
import sys, os, json, numpy as np
W, BD = sys.argv[1:3]
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
SETS = {'l': [('W0', BD, 'W0'), ('C2', BD, 'C2'), ('H1', W, 'H1'), ('H2', W, 'H2'), ('H3', W, 'H3')],
        'r': [('W0', BD, 'W0'), ('C2rx', BD, 'C2rx'), ('H1', W, 'H1'), ('H2', W, 'H2'), ('H3', W, 'H3')]}
OUT = {}; MD = ['cells: non-contact / crease (depth mm) / orientation / local inv / folds outside / loop / p95 (max) strain % / zone proxy % / dV vs W0 cm3 [failing retained criteria]']
for s, sets in SETS.items():
    D = {n: load(d, s, t) for n, d, t in sets}; OUT[s] = D
    MD += ['', '### %s side' % ('left' if s == 'l' else 'right'), '', '| angle | ' + ' | '.join(n for n, _, _ in sets) + ' |', '|---|' + '---|' * len(sets)]
    for a in ANG:
        cells = []
        for n, _, _ in sets:
            k = D[n][a]; cells.append('%d / %d (%.1f) / %d / %d / %d / %.2f / %.0f (%.0f) / %.1f / %+.0f [%d]' % (k['nc'], k['crease'], k['depth'], k['orient'], k['inv'], k['folds_out'], k['loop'], k['p95'], k['smax'], k['zone'], k['vol'] - D['W0'][a]['vol'], len(k['fails'])))
        MD.append('| %d | %s |' % (a, ' | '.join(cells)))
# §7 checks per candidate and side (reference = C2 / C2rx)
CHK = {}
for s in ('l', 'r'):
    D = OUT[s]; ref = 'C2' if s == 'l' else 'C2rx'
    for h in ('H1', 'H2', 'H3'):
        H = D[h]; R = D[ref]; W0 = D['W0']; dv = lambda X, a: X[a]['vol'] - W0[a]['vol']
        loss_ref = -dv(R, 130); loss_h = -dv(H, 130); red = (loss_ref - loss_h) / loss_ref if loss_ref > 0 else None
        c = {'1 rest / 45 deg identical (numerically) and T-1 ~ 0': H[45]['nc'] == W0[45]['nc'] and H[45]['orient'] == W0[45]['orient'] and abs(H[45]['T1']) < 1e-6,
             '2 nc = 0 at 90 and 130, no new at intermediate': H[90]['nc'] == 0 and H[130]['nc'] == 0 and all(H[a]['nc'] <= R[a]['nc'] for a in ANG),
             '3 loop >= 0.50 at 90-120 (130 target)': all(H[a]['loop'] >= 0.5 for a in (90, 110, 120)), '3b loop >= 0.50 at 130': H[130]['loop'] >= 0.5,
             '4 crease 90 <= 2 mm; 110-130 no worse than %s' % ref: H[90]['depth'] <= 2.0 and all(H[a]['depth'] <= R[a]['depth'] + 1e-9 for a in (110, 120, 130)),
             '5 no new local inversions vs %s; orientation not materially worse (<= +10 %%)' % ref: all(H[a]['inv'] <= R[a]['inv'] for a in ANG) and all(H[a]['orient'] <= max(R[a]['orient'] * 1.1, R[a]['orient'] + 5) for a in ANG),
             '6 >= 50 %% reduction of the corrective-caused closed-volume loss at 130 vs %s' % ref: red is not None and red >= 0.5,
             '7 p95 strain <= %s + 5 pp at every angle' % ref: all(H[a]['p95'] <= R[a]['p95'] + 5 for a in ANG),
             'no folds outside the crease': all(H[a]['folds_out'] == 0 for a in ANG)}
        CHK['%s_%s' % (h, s)] = dict(checks=c, all_pass=all(c.values()), volume_loss_130_ref_cm3=round(loss_ref, 1), volume_loss_130_cm3=round(loss_h, 1), loss_reduction_130=None if red is None else round(red, 3))
json.dump(dict(tables=OUT, checks=CHK), open(W + '/diag/stageA_judgement.json', 'w'), indent=1, default=float)
open(W + '/diag/stageA_tables.md', 'w').write('\n'.join(MD) + '\n'); print('\n'.join(MD))
for k, v in CHK.items(): print(k, 'ALL PASS' if v['all_pass'] else 'fail', 'loss130 ref %.0f -> %.0f (reduction %s)' % (v['volume_loss_130_ref_cm3'], v['volume_loss_130_cm3'], v['loss_reduction_130']), [n for n, ok in v['checks'].items() if not ok])
