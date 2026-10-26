# judge.py WORKDIR : pass/fail per D-pose against the AD-R12 retained criteria + failure-cause classification; placement comparison table
import sys, json, os, collections
W = sys.argv[1]; R = json.load(open(W + '/diag/diag_results.json'))['results']
DQ = json.load(open(W + '/diag/diag_results_dqs.json'))['results']
ALT = {}
for fn in os.listdir(W + '/diag'):
    if fn.startswith('diag_results_alt_'): ALT[fn[len('diag_results_alt_'):-5]] = json.load(open(W + '/diag/' + fn))['results']
VOLTOL = {'D2': 3.0}
def crit(name, r):
    t = name.split('_')[0]; out = []
    i = r['intersections']
    out.append(('0 non-contact intersections', i['non_contact'] == 0, '%d' % i['non_contact']))
    out.append(('no new flipped faces', r['flips']['total'] == 0, '%d (%d in crease)' % (r['flips']['total'], r['flips']['in_crease'])))
    out.append(('no new folds outside crease/contact zones', r['folds']['outside'] == 0, '+%d (outside %d)' % (r['folds']['new'], r['folds']['outside'])))
    zv = r['volume']['zone_pct']
    if t == 'D5' or zv is None: out.append(('zone volume (n/a: reference centre <2.2 cm under the thenar surface)', True, 'n/a'))
    else: out.append(('zone volume within ±%.0f%%' % VOLTOL.get(t, 5.0), abs(zv) <= VOLTOL.get(t, 5.0), '%+.1f%%' % zv))
    if r['loop_spacing_min_ratio'] is not None: out.append(('joint-loop spacing >= 50% of rest', r['loop_spacing_min_ratio'] >= 0.5, '%.2f' % r['loop_spacing_min_ratio']))
    if i['crease']: out.append(('crease contact depth <= 2 mm', i['crease_depth_mm'] <= 2.0, '%.1f mm' % i['crease_depth_mm']))
    if r.get('nail_plate_v2_mm'):                                       # runs from order 6c38d75 on: Nail Plate Rigidity v2 gates; cap v1 is report-only
        m = max(r['nail_plate_v2_mm'].values()); out.append(('Nail Plate Rigidity v2 <= 0.3 mm', m <= 0.3, '%.3f mm' % m))
    elif 'nail_rigidity_mm' in r and r['nail_rigidity_mm']: m = max(r['nail_rigidity_mm'].values()); out.append(('nail rigidity <= 0.3 mm', m <= 0.3, '%.2f mm' % m))   # historical runs
    out.append(('rest-return T-1 (<= 3.0 mm body)', r['rest_return_T1_mm'] <= 3.0, '%.4f mm' % r['rest_return_T1_mm']))
    return out
def cause(name, r, c):
    t = name.split('_')[0]; fails = [x[0] for x in c if not x[1]]; cs = []
    if not fails: return []
    nc = r['intersections']['by_pair']
    if any(k.startswith('non-contact') for k in nc):
        kinds = [k for k in nc if k.startswith('non-contact')]
        if t == 'D2': cs.append('source-contact anatomy: forearm mass against the upper-arm mass in deep (130 deg) flexion — undeclared in v001, analogous to the declared calf–thigh contact')
        elif t == 'D1': cs.append('diagnostic rig configuration: pure GH flexion without girdle participation pinches the pectoral / anterior-axillary tissue (the girdle-assisted variant has 0 non-contact intersections)')
        elif t == 'D4': cs.append('crease-adjacent self contact just outside the 2.6 cm crease radius (pad region) — diagnostic weights')
        elif t == 'D5': cs.append('palm / thenar or index self-fold contact just outside the 3.5 cm crease radius during opposition — diagnostic weights (thenar crease)')
        elif t == 'D9': cs.append('diagnostic weights: axillary arm–arm contact dragged by the trunk rotation')
        else: cs.append('unclassified non-contact intersections: ' + ', '.join(kinds))
    if any(f.startswith(('no new flipped', 'crease contact', 'joint-loop', 'zone volume')) for f in fails):
        d = DQ.get(name)
        if d and d['volume']['zone_pct'] is not None and r['volume']['zone_pct'] is not None and abs(d['volume']['zone_pct']) < abs(r['volume']['zone_pct']) - 5:
            cs.append('diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from %+.1f%% to %+.1f%%; flips / contact remain where tissue must meet)' % (r['volume']['zone_pct'], d['volume']['zone_pct']))
        else: cs.append('diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone)')
    if any(f.startswith('no new folds outside') for f in fails): cs.append('diagnostic weights: fold outside the crease radius adjacent to the crease (see sheet)')
    if any(f.startswith('nail') for f in fails): cs.append('diagnostic weights: the distal phalanx / nail cap is shared between the middle and distal phalanx bones (heat weights), so the nail bends with the DIP; production weights would bind the nail rigidly to the distal bone')
    return cs
T = collections.OrderedDict(); ALLP = 0
for n, r in R.items():
    c = crit(n, r); ok = all(x[1] for x in c); T[n] = dict(pass_=ok, criteria=[dict(criterion=a, ok=b, value=v) for a, b, v in c], causes=cause(n, r, c), dqs=DQ.get(n) is not None)
    ALLP += ok
# placement comparison (same diagnostic weights; only the pivot moved)
PC = []
for alt, rr in sorted(ALT.items()):
    for n, r in rr.items():
        if 'girdle' in n: continue
        b = R[n]; f = lambda x: dict(int=x['intersections']['total'], nc=x['intersections']['non_contact'], depth=round(x['intersections']['crease_depth_mm'], 1), flips=x['flips']['total'],
                                     folds_out=x['folds']['outside'], zone=None if x['volume']['zone_pct'] is None else round(x['volume']['zone_pct'], 1), p95=round(x['strain']['zone_p95_pct'], 1), loop=x['loop_spacing_min_ratio'])
        PC.append(dict(alternative=alt, pose=n, alt=f(r), v002=f(b)))
json.dump(dict(per_pose=T, passed=ALLP, total=len(T), placement_comparison=PC), open(W + '/diag/judgement.json', 'w'), indent=1)
L = ['| pose | result | failed criteria | likely cause |', '|---|---|---|---|']
for n, t in T.items():
    fl = '; '.join('%s (%s)' % (c['criterion'], c['value']) for c in t['criteria'] if not c['ok'])
    L.append('| %s | %s | %s | %s |' % (n, 'PASS' if t['pass_'] else '**FAIL**', fl or '—', ' / '.join(t['causes']) or '—'))
open(W + '/diag/judgement_table.md', 'w').write('\n'.join(L) + '\n')
L = ['| alternative pivot | pose | int (nc) | crease depth mm | flips | folds outside | zone vol % | strain p95 % | loop | v002 int (nc) / depth / flips / folds out / zone / p95 / loop |', '|---|---|---|---|---|---|---|---|---|---|']
for p in PC:
    a, b = p['alt'], p['v002']
    L.append('| %s | %s | %d (%d) | %.1f | %d | %d | %s | %.0f | %.2f | %d (%d) / %.1f / %d / %d / %s / %.0f / %.2f |' % (p['alternative'], p['pose'], a['int'], a['nc'], a['depth'], a['flips'], a['folds_out'], a['zone'], a['p95'], a['loop'] or 0,
             b['int'], b['nc'], b['depth'], b['flips'], b['folds_out'], b['zone'], b['p95'], b['loop'] or 0))
open(W + '/diag/placement_table.md', 'w').write('\n'.join(L) + '\n')
print('passed', ALLP, '/', len(T))
