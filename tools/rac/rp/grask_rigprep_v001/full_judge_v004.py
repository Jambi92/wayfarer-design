# full_judge_v004.py WORKDIR : 43-pose full-suite regression gate (order 6c38d75 §15). W0 baseline vs W0 + selected elbow corrective (SEL), same
# evaluator, v002 pivots; Nail Plate Rigidity v2 gates (judge.crit), Nail Cap Historical v1 reported. For every pose: pass/fail, failing criteria,
# fixed / newly failing criteria, every changed metric, corrective activation, and BIT IDENTITY of the posed mesh when the activation is zero.
import sys, os, json, numpy as np
W = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
ld = lambda t: json.load(open('%s/diag/diag_results_full_%s.json' % (W, t)))['results']
A, B = ld('W0'), ld('SEL')
def hist_crit(n, r):                                                    # historical v1 gating (cap mask) for continuity with 9703fd2 / 44e1ec6
    rr = dict(r); rr.pop('nail_plate_v2_mm', None); return crit(n, rr)
def key(r):
    i = r['intersections']; return dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 2), folds_out=r['folds']['outside'], folds=r['folds']['new'], orient=r['flips']['total'],
                                        inv=r['inversions']['total'], zone=None if r['volume']['zone_pct'] is None else round(r['volume']['zone_pct'], 2), p95=round(r['strain']['zone_p95_pct'], 1),
                                        loop=None if r['loop_spacing_min_ratio'] is None else round(r['loop_spacing_min_ratio'], 3),
                                        nail_v2=None if not r.get('nail_plate_v2_mm') else round(max(r['nail_plate_v2_mm'].values()), 3),
                                        nail_cap_v1=None if not r.get('nail_cap_historical_v1_mm') else round(max(r['nail_cap_historical_v1_mm'].values()), 3), T1=round(r['rest_return_T1_mm'], 4))
rows = []; reg = []; fixed_any = []; unexpected = []
for n in A:
    ca, cb = crit(n, A[n]), crit(n, B[n]); fa = {x[0] for x in ca if not x[1]}; fb = {x[0] for x in cb if not x[1]}
    act = B[n].get('corrective', {}).get('activation', {}); active = any(any(w != 0 for w in v['weights'].values()) for v in act.values()) if act else False
    va = np.load('%s/diag/posed/%s_full_W0.npz' % (W, n))['V']; vb = np.load('%s/diag/posed/%s_full_SEL.npz' % (W, n))['V']
    bit = bool((va.view(np.uint32) == vb.view(np.uint32)).all()); ka, kb = key(A[n]), key(B[n]); dif = {m: (ka[m], kb[m]) for m in ka if ka[m] != kb[m]}
    if not active and (not bit or dif): unexpected.append(n)
    row = dict(pose=n, corrective_active=active, activation=act, bit_identical_to_W0=bit, W0_pass=not fa, SEL_pass=not fb, W0_failing=sorted(fa), SEL_failing=sorted(fb),
               newly_failing=sorted(fb - fa), fixed=sorted(fa - fb), changed_metrics=dif, W0_hist_v1_pass=all(x[1] for x in hist_crit(n, A[n])))
    rows.append(row)
    if row['newly_failing']: reg.append(n)
    if row['fixed']: fixed_any.append(n)
summ = dict(total=len(rows), W0_pass_v2=sum(r['W0_pass'] for r in rows), SEL_pass_v2=sum(r['SEL_pass'] for r in rows), W0_pass_historical_v1=sum(r['W0_hist_v1_pass'] for r in rows),
            regressions=reg, poses_with_fixed_criteria=fixed_any, corrective_active_poses=[r['pose'] for r in rows if r['corrective_active']],
            inactive_poses_bit_identical=all(r['bit_identical_to_W0'] for r in rows if not r['corrective_active']), unexpected_unrelated_changes=unexpected)
fmt = lambda k: '%d / %d(%.1f) / %d / %d / %d / %s / %.0f / %s / v2 %s, v1 %s' % (k['nc'], k['crease'], k['depth'], k['folds_out'], k['orient'], k['inv'], k['zone'], k['p95'], k['loop'], k['nail_v2'], k['nail_cap_v1'])
L = ['| pose | corrective | bit-identical | W0 | SEL | W0 nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop / nail | SEL same | newly failing | fixed |', '|---|---|---|---|---|---|---|---|---|']
for r in rows:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (r['pose'], 'active' if r['corrective_active'] else '0', 'yes' if r['bit_identical_to_W0'] else 'no', 'PASS' if r['W0_pass'] else 'fail', 'PASS' if r['SEL_pass'] else 'fail',
             fmt(key(A[r['pose']])), fmt(key(B[r['pose']])), ('**' + '; '.join(r['newly_failing']) + '**') if r['newly_failing'] else '—', '; '.join(r['fixed']) or '—'))
json.dump(dict(summary=summ, rows=rows), open(W + '/diag/full_suite_judgement_v004.json', 'w'), indent=1, default=str)
open(W + '/diag/full_suite_table_v004.md', 'w').write('\n'.join(L) + '\n'); print(json.dumps(summ, indent=1))
