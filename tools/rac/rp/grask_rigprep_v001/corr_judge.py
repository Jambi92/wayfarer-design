# corr_judge.py WORKDIR : candidate tables for the elbow corrective (order 6c38d75 §8/§9/§10/§11/§17): W0 vs C1 / C2 / C3 (left LBS), W0 vs C2 (left
# DQS, identical keys / activation), W0 vs C2r (18 cm) / C2rx (21 cm) (right LBS). Retained criteria (judge.crit), metrics, new / fixed criteria,
# closed-volume change caused by the corrective, and the §17 selection checks.
import sys, os, json, numpy as np
W = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); Q = np.asarray(Z['Q'])
def cvol(V):
    T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', V[T_[:, 0]], np.cross(V[T_[:, 1]], V[T_[:, 2]])).sum() / 6)
ld = lambda t: json.load(open('%s/diag/diag_results_c_%s.json' % (W, t)))['results']
def key(r):
    i = r['intersections']; return dict(nc=i['non_contact'], crease=i['crease'], depth=round(i['crease_depth_mm'], 2), orient=r['flips']['total'], inv=r['inversions']['total'],
                                        folds=r['folds']['new'], folds_out=r['folds']['outside'], loop=round(r['loop_spacing_min_ratio'], 3), p95=round(r['strain']['zone_p95_pct'], 1),
                                        smax=round(r['strain']['zone_max_pct'], 1), zone=round(r['volume']['zone_pct'], 2), T1=round(r['rest_return_T1_mm'], 4))
fmt = lambda k: '%d / %d (%.1f) / %d / %d / +%d (%d) / %.2f / %.0f (%.0f) / %.1f' % (k['nc'], k['crease'], k['depth'], k['orient'], k['inv'], k['folds'], k['folds_out'], k['loop'], k['p95'], k['smax'], k['zone'])
OUT = {}; MD = []
for title, base, cands, side in (('left LBS', 'l_W0', ['l_C1', 'l_C2', 'l_C3'], 'l'), ('left DQS (C2 keys)', 'dqs_W0', ['dqs_C2'], 'l'), ('right LBS', 'r_W0', ['r_C2r', 'r_C2rx'], 'r')):
    A = ld(base); MD += ['', '### %s' % title, '', '| pose | %s | %s |' % (base, ' | '.join(cands)), '|---|---|' + '---|' * len(cands)]
    for p in sorted(A, key=lambda k: int(k.split('flex')[1]) if 'flex' in k else 0):
        cells = [fmt(key(A[p])) + ' [%d fail]' % sum(1 for x in crit(p, A[p]) if not x[1])]
        va = cvol(np.load('%s/diag/posed/%s_c_%s.npz' % (W, p, base))['V'].astype(float))
        for c in cands:
            R = ld(c)[p]; fa = {x[0] for x in crit(p, A[p]) if not x[1]}; fb = {x[0] for x in crit(p, R) if not x[1]}
            vb = cvol(np.load('%s/diag/posed/%s_c_%s.npz' % (W, p, c))['V'].astype(float))
            OUT.setdefault(c, {})[p] = dict(metrics=key(R), base=key(A[p]), newly_failing=sorted(fb - fa), fixed=sorted(fa - fb), closed_volume_change_vs_base_cm3=round(vb - va, 1),
                                            activation=R.get('corrective', {}).get('activation'))
            cells.append(fmt(key(R)) + ' [%d fail]%s%s; dV %+.0f cm3' % (len(fb), (' **new: ' + '; '.join(sorted(fb - fa)) + '**') if fb - fa else '', (' fixed: ' + '; '.join(sorted(fa - fb))) if fa - fb else '', vb - va))
        MD.append('| %s | %s |' % (p, ' | '.join(cells)))
MD.insert(0, 'cells: non-contact / crease (depth mm) / orientation disagreement / local fold-inversion indicator / folds new (outside crease) / loop min / p95 strain (max) % / cone-volume proxy % [failing retained criteria]; dV = closed-mesh volume change caused by the corrective vs the baseline of the same skinning method')
# §17 selection checks for C2 (left LBS)
c2 = OUT['l_C2']; B0 = ld('l_W0')
chk = {'no newly failing retained criterion at any tested angle': all(not v['newly_failing'] for v in c2.values()),
       '45 deg identical (activation 0)': c2['D2_l_flex45']['metrics'] == key(B0['D2_l_flex45']),
       '90 deg integrity improves (nc, crease depth, orientation, local inv, loop)': c2['D2_l_flex90']['metrics']['depth'] <= key(B0['D2_l_flex90'])['depth'] and c2['D2_l_flex90']['metrics']['orient'] < key(B0['D2_l_flex90'])['orient'] and c2['D2_l_flex90']['metrics']['loop'] > key(B0['D2_l_flex90'])['loop'],
       '130 deg improves (nc, crease depth, orientation, loop)': all(c2['D2_l_flex130']['metrics'][m] < key(B0['D2_l_flex130'])[m] for m in ('nc', 'depth', 'orient')) and c2['D2_l_flex130']['metrics']['loop'] > key(B0['D2_l_flex130'])['loop'],
       'no new local fold/inversion indicator faces (any tested angle)': all(v['metrics']['inv'] <= v['base']['inv'] for v in c2.values()),
       'no folds outside the crease': all(v['metrics']['folds_out'] == 0 for v in c2.values()),
       'rest-return exact (T-1)': all(v['metrics']['T1'] == 0 for v in c2.values())}
OUT['selection_checks_C2'] = chk
json.dump(OUT, open(W + '/diag/corr_judgement.json', 'w'), indent=1, default=str); open(W + '/diag/corr_tables.md', 'w').write('\n'.join(MD) + '\n')
print('\n'.join(MD)); print(json.dumps(chk, indent=1))
