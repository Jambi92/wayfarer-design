# iso_judge.py WORKDIR : full-suite before/after (W0 baseline vs W2 candidate, same v002 pivots), regressions highlighted; alt-pivot and
# LBS/DQS matrices; failure classification with confidence (order 8918cea §7). Retained thresholds unchanged.
import sys, os, json
W = sys.argv[1]; src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read()
ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
ld = lambda t: json.load(open('%s/diag/diag_results_%s.json' % (W, t)))['results']
A, B = ld('full_W0'), ld('full_W2')
def key(r):
    i = r['intersections']; return dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 1), contact=i['contact'], folds_out=r['folds']['outside'], folds=r['folds']['new'],
                                        orient=r['flips']['total'], inv=r['inversions']['total'], zone=None if r['volume']['zone_pct'] is None else round(r['volume']['zone_pct'], 1),
                                        p95=round(r['strain']['zone_p95_pct'], 1), loop=None if r['loop_spacing_min_ratio'] is None else round(r['loop_spacing_min_ratio'], 2),
                                        nail=None if not r.get('nail_rigidity_mm') else round(max(r['nail_rigidity_mm'].values()), 2))
ROWS = []; reg = []; imp = []
for n in A:
    ca, cb = crit(n, A[n]), crit(n, B[n]); pa, pb = all(x[1] for x in ca), all(x[1] for x in cb)
    fa = {x[0] for x in ca if not x[1]}; fb = {x[0] for x in cb if not x[1]}
    newf = sorted(fb - fa); fixed = sorted(fa - fb)
    ROWS.append(dict(pose=n, W0_pass=pa, W2_pass=pb, W0=key(A[n]), W2=key(B[n]), new_failures=newf, fixed=fixed))
    if newf or (pa and not pb): reg.append(n)
    if fixed: imp.append(n)
L = ['| pose | W0 | W2 | W0 nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop / nail | W2 same | newly failing criteria (REGRESSION) | criteria fixed |', '|---|---|---|---|---|---|---|']
fmt = lambda k: '%d / %d(%.1f) / %d / %d / %d / %s / %.0f / %s / %s' % (k['nc'], k['crease'], k['depth'], k['folds_out'], k['orient'], k['inv'], k['zone'], k['p95'], k['loop'], k['nail'])
for r in ROWS:
    L.append('| %s | %s | %s | %s | %s | %s | %s |' % (r['pose'], 'PASS' if r['W0_pass'] else 'fail', 'PASS' if r['W2_pass'] else 'fail', fmt(r['W0']), fmt(r['W2']),
             ('**' + '; '.join(r['new_failures']) + '**') if r['new_failures'] else '—', '; '.join(r['fixed']) or '—'))
summ = dict(W0_pass=sum(r['W0_pass'] for r in ROWS), W2_pass=sum(r['W2_pass'] for r in ROWS), total=len(ROWS), regressions=reg, improvements=imp)
# alternate pivots (identical W2 array) vs v002 pivots
ALT = []
for fn in sorted(os.listdir(W + '/diag')):
    if fn.startswith('diag_results_alt_') and fn.endswith('_W2.json'):
        nm = fn[len('diag_results_alt_'):-len('_W2.json')]; R = json.load(open(W + '/diag/' + fn))['results']
        for p, r in R.items():
            ALT.append(dict(alternative=nm, pose=p, alt=key(r), v002=key(B[p]), alt_pass=all(x[1] for x in crit(p, r)), v002_pass=all(x[1] for x in crit(p, B[p])),
                            endpoints_alt=r['world_endpoints_cm'], endpoints_v002=B[p]['world_endpoints_cm']))
LA = ['| alternative pivot (W2 weights) | pose | alt nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop | v002 pivot same | pass alt / v002 | world endpoints alt vs v002 (cm) |', '|---|---|---|---|---|---|']
for a in ALT:
    ep = '; '.join('%s %s vs %s' % (b, [round(x, 1) for x in a['endpoints_alt'][b]], [round(x, 1) for x in a['endpoints_v002'][b]]) for b in a['endpoints_alt'])
    LA.append('| %s | %s | %s | %s | %s / %s | %s |' % (a['alternative'], a['pose'], fmt(a['alt'])[:-7], fmt(a['v002'])[:-7], 'P' if a['alt_pass'] else 'f', 'P' if a['v002_pass'] else 'f', ep))
# LBS vs DQS on rig v002 (identical pivots, weights, poses)
LD = []
if os.path.exists(W + '/diag/diag_results_v2_lbs.json') and os.path.exists(W + '/diag/diag_results_v2_dqs.json'):
    l, d = ld('v2_lbs'), ld('v2_dqs')
    LD = ['| pose (rig v002, W2) | LBS nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop | DQS same | pass LBS / DQS |', '|---|---|---|---|']
    for p in d: LD.append('| %s | %s | %s | %s / %s |' % (p, fmt(key(l[p]))[:-7], fmt(key(d[p]))[:-7], 'P' if all(x[1] for x in crit(p, l[p])) else 'f', 'P' if all(x[1] for x in crit(p, d[p])) else 'f'))
json.dump(dict(summary=summ, rows=ROWS, alt=ALT), open(W + '/diag/iso_judgement.json', 'w'), indent=1)
open(W + '/diag/iso_fullsuite_table.md', 'w').write('\n'.join(L) + '\n'); open(W + '/diag/iso_alt_table.md', 'w').write('\n'.join(LA) + '\n'); open(W + '/diag/iso_dqs_table.md', 'w').write('\n'.join(LD) + '\n')
print(summ)
