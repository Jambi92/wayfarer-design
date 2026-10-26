# pair_judge.py WORKDIR A B [OUTNAME] : full-suite comparison of two result sets diag_results_full_{A,B}.json (same v002 pivots, same metric
# code, retained thresholds from judge.py crit). Per pose: pass/fail, every metric, newly failing criteria (regressions) and fixed criteria,
# plus every changed numeric criterion value. Also nail Kabsch residuals on (i) the original documented cap mask (diag_run, unchanged) and
# (ii) the WN plate subset, recomputed from the posed meshes.
import sys, os, json, numpy as np
W, A, B = sys.argv[1:4]; ON = sys.argv[4] if len(sys.argv) > 4 else '%s_vs_%s' % (A, B)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
ld = lambda t: json.load(open('%s/diag/diag_results_full_%s.json' % (W, t)))['results']
RA, RB = ld(A), ld(B)
def key(r):
    i = r['intersections']; return dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 2), contact=i['contact'], folds_out=r['folds']['outside'], folds=r['folds']['new'],
                                        orient=r['flips']['total'], inv=r['inversions']['total'], zone=None if r['volume']['zone_pct'] is None else round(r['volume']['zone_pct'], 2),
                                        p95=round(r['strain']['zone_p95_pct'], 1), loop=None if r['loop_spacing_min_ratio'] is None else round(r['loop_spacing_min_ratio'], 3),
                                        nail=None if not r.get('nail_rigidity_mm') else round(max(r['nail_rigidity_mm'].values()), 3))
fmt = lambda k: '%d / %d(%.1f) / %d / %d / %d / %s / %.0f / %s / %s' % (k['nc'], k['crease'], k['depth'], k['folds_out'], k['orient'], k['inv'], k['zone'], k['p95'], k['loop'], k['nail'])
ROWS = []; reg = []; imp = []; changed = []
for n in RA:
    ca, cb = crit(n, RA[n]), crit(n, RB[n]); pa, pb = all(x[1] for x in ca), all(x[1] for x in cb)
    fa = {x[0] for x in ca if not x[1]}; fb = {x[0] for x in cb if not x[1]}
    ka, kb = key(RA[n]), key(RB[n]); dif = {m: (ka[m], kb[m]) for m in ka if ka[m] != kb[m]}
    ROWS.append(dict(pose=n, A_pass=pa, B_pass=pb, A=ka, B=kb, new_failures=sorted(fb - fa), fixed=sorted(fa - fb), changed_metrics=dif))
    if (fb - fa) or (pa and not pb): reg.append(n)
    if fa - fb: imp.append(n)
    if dif: changed.append(n)
# nail residuals on the plate subset (posed meshes)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float)
PL = json.load(open(W + '/w/weights_WN_log.json'))['digits']
def kabsch(P, X):
    P0, X0 = P - P.mean(0), X - X.mean(0); U, S, Vt = np.linalg.svd(P0.T @ X0); d = np.sign(np.linalg.det(Vt.T @ U.T)); D = np.diag([1, 1, d]); R = Vt.T @ D @ U.T
    return float(np.sqrt(((P0 @ R.T - X0) ** 2).sum(1).mean()))
NAILP = {}
for p in RA:
    if not RA[p].get('nail_rigidity_mm'): continue
    NAILP[p] = {}
    for t in (A, B):
        Vp = np.load('%s/diag/posed/%s_full_%s.npz' % (W, p, t))['V'].astype(float)
        NAILP[p][t] = {fg: round(kabsch(V0[PL[fg + '_l']['vertex_ids']], Vp[PL[fg + '_l']['vertex_ids']]) * 10, 4) for fg in RA[p]['nail_rigidity_mm']}
        NAILP[p][t + '_capmask'] = {fg: round(v, 4) for fg, v in ({'A': RA, 'B': RB}['A' if t == A else 'B'][p]['nail_rigidity_mm']).items()}
L = ['| pose | %s | %s | %s nc / crease(mm) / folds-out / orient / inv / zone %% / p95 / loop / nail | %s same | newly failing (REGRESSION) | fixed | changed metrics |' % (A, B, A, B), '|---|---|---|---|---|---|---|---|']
for r in ROWS:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (r['pose'], 'PASS' if r['A_pass'] else 'fail', 'PASS' if r['B_pass'] else 'fail', fmt(r['A']), fmt(r['B']),
             ('**' + '; '.join(r['new_failures']) + '**') if r['new_failures'] else '—', '; '.join(r['fixed']) or '—', ', '.join('%s %s->%s' % (m, a, b) for m, (a, b) in r['changed_metrics'].items()) or 'identical'))
summ = {A + '_pass': sum(r['A_pass'] for r in ROWS), B + '_pass': sum(r['B_pass'] for r in ROWS), 'total': len(ROWS), 'regressions': reg, 'improvements': imp, 'poses_with_any_metric_change': changed}
json.dump(dict(summary=summ, rows=ROWS, nail_residual_mm=NAILP), open('%s/diag/judge_%s.json' % (W, ON), 'w'), indent=1)
open('%s/diag/judge_%s_table.md' % (W, ON), 'w').write('\n'.join(L) + '\n'); print(json.dumps(summ)); print(json.dumps(NAILP, indent=0))
