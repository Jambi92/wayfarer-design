# elbow_judge.py WORKDIR : left-elbow isolation tables (order b303b9e §4): W0 / E1 / E2 x LBS / DQS on the elbow set and the sentinels,
# retained criteria (judge.py crit), every metric, return-to-rest T-1, and sentinel regressions vs W0 under the same skinning method.
import sys, os, json
W = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
R = {(c, m): json.load(open('%s/diag/diag_results_el_%s_%s.json' % (W, m, c)))['results'] for c in ('W0', 'E1', 'E2') for m in ('lbs', 'dqs')}
ELB = ['D2_l_base_abd45', 'D2_l_flex45', 'D2_l_flex90', 'D2_l_flex130']; SEN = ['D1_l_abd90', 'D1_l_flex90', 'D3_l_flex60', 'D3_l_ext60', 'D4_l_fist', 'D5_l_oppose_pinch']
def key(r):
    i = r['intersections']; return dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 2), folds_out=r['folds']['outside'], orient=r['flips']['total'], inv=r['inversions']['total'],
                                        zone=None if r['volume']['zone_pct'] is None else round(r['volume']['zone_pct'], 1), p95=round(r['strain']['zone_p95_pct'], 1),
                                        loop=None if r['loop_spacing_min_ratio'] is None else round(r['loop_spacing_min_ratio'], 3), worst=r.get('loop_spacing_worst'), T1=round(r.get('rest_return_T1_mm') or 0, 4))
fmt = lambda k: '%d / %d(%.1f) / %d / %d / %d / %s / %.0f / %s / %s' % (k['nc'], k['crease'], k['depth'], k['folds_out'], k['orient'], k['inv'], k['zone'], k['p95'], k['loop'], k['T1'])
OUT = dict(rows=[], sentinel_regressions={}, fails={})
L = ['| pose | method | W0 nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop / T-1 mm | E1 same | E2 same | failing criteria W0 / E1 / E2 |', '|---|---|---|---|---|---|']
for p in ELB + SEN:
    for m in ('lbs', 'dqs'):
        ks = {c: key(R[(c, m)][p]) for c in ('W0', 'E1', 'E2')}; fl = {c: [x[0] for x in crit(p, R[(c, m)][p]) if not x[1]] for c in ('W0', 'E1', 'E2')}
        OUT['rows'].append(dict(pose=p, method=m, metrics=ks, failing=fl))
        L.append('| %s | %s | %s | %s | %s | %d / %d / %d |' % (p, m.upper(), fmt(ks['W0']), fmt(ks['E1']), fmt(ks['E2']), len(fl['W0']), len(fl['E1']), len(fl['E2'])))
        for c in ('E1', 'E2'):
            new = sorted(set(fl[c]) - set(fl['W0']))
            if new: OUT['sentinel_regressions' if p in SEN else 'fails'].setdefault('%s %s %s' % (c, m, p), new)
json.dump(OUT, open(W + '/diag/elbow_judgement.json', 'w'), indent=1); open(W + '/diag/elbow_table.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L)); print('new failing criteria vs W0 (elbow set):', OUT['fails']); print('sentinel regressions:', OUT['sentinel_regressions'])
