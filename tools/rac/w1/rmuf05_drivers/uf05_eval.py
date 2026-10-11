# RAC RM-UF-05: evaluate every diagnostic batch; profile study of D1 vs D2 stability across UFCA slot-count profiles.
import os, sys, json, numpy as np
from scipy.stats import qmc
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import uf05_spaces as SP, uf05_metrics as UM, uf05_batches as UB
S = UB.S; man = json.load(open(S + '/manifest.json')); res = {}
def space_of(pop): return UB.POP[pop][0]
for key, m in man.items():
    pop, cond, sd = key.split('_'); z = np.load(m['file']); U = z['U']; names = list(z['names']); sl = SP.slots(space_of(pop), names)
    r = UM.summary(U, sl)
    if pop in UB.CLICHE:
        inb = np.ones(len(U), bool)
        for k, (a, b) in UB.CLICHE[pop].items(): inb &= (U[:, names.index(k)] >= a - 1e-9) & (U[:, names.index(k)] <= b + 1e-9)
        exp = np.prod([b - a for a, b in UB.CLICHE[pop].values()]); r['canon_bundle'] = dict(share=float(inb.mean()), uniform_expectation=float(exp), lift=float(inb.mean() / exp))
        cc = [names.index(k) for k in UB.CLICHE[pop]]; C = np.corrcoef(U[:, cc].T); r['canon_bundle']['mean_abs_corr'] = float(np.abs(C[np.triu_indices(len(cc), 1)]).mean())
    if pop == 'SK':   # W3C overlap sides present in the batch (normalized MF-reference crossing)
        mf = UB.POP['MF'][2]; r['overlap_presence'] = {k: float((U[:, names.index(k)] < mf[k] + 1e-9).mean()) for k in ('brow', 'jaw_w', 'cheek')}
    res[key] = r
json.dump(res, open(S + '/eval.json', 'w'), indent=1)
# aggregate per pop / cond
agg = {}
for key, r in res.items():
    pop, cond, sd = key.split('_'); a = agg.setdefault(pop, {}).setdefault(cond, [])
    a.append([r['D1']['nn_median'], r['D2']['nn_median'], r['D2']['nn_p5'], r['D2']['frac_nn_below']['0.05'], r['eff_rank_frac'], min(r['slot_coverage'].values()), r['bundle']['lift'], r.get('canon_bundle', {}).get('lift', np.nan)])
print('pop cond | D1 nnmed | D2 nnmed | D2 p5 | frac<0.05 | effrank | minslotcov | tuple lift | canon lift  (mean over 4 seeds; range)')
for pop in agg:
    for cond, v in agg[pop].items():
        v = np.array(v); print(pop, cond.ljust(8), ' '.join('%.3f[%.3f-%.3f]' % (v[:, j].mean(), v[:, j].min(), v[:, j].max()) for j in range(8)))
# profile study: slot-count profiles from the UFCA / race-spec inventory (slots 2,3,4a,5,6,7,8,9); unit-span diagnostic sampling
PROF = {'MF': [4, 2, 2, 2, 1, 1, 2, 8], 'SK': [7, 6, 5, 3, 8, 1, 6, 8], 'SG': [6, 5, 5, 4, 11, 8, 6, 8], 'FN': [1, 9, 2, 3, 10, 6, 5, 10], 'AE': [3, 8, 2, 3, 8, 6, 5, 10],
        'VA': [4, 8, 2, 2, 8, 6, 1, 10], 'HV': [4, 2, 2, 5, 8, 5, 9, 15], 'DU': [7, 8, 1, 4, 9, 6, 7, 8], 'GR': [4, 4, 1, 4, 8, 4, 7, 5], 'GO': [5, 4, 1, 6, 8, 4, 7, 6],
        'PK': [6, 5, 2, 6, 8, 6, 7, 9], 'CG': [4, 3, 2, 5, 4, 3, 5, 13], 'SA': [1, 4, 2, 0, 0, 0, 1, 0]}
prof = {}
for pop, cnt in PROF.items():
    sl = np.concatenate([[i] * c for i, c in enumerate(cnt)]); d = len(sl); row = {'d': int(d), 'slots': int(sum(1 for c in cnt if c))}
    for cond in ('broad', 'central', 'converge'):
        vals = []
        for sd in UB.SEEDS:
            rng = np.random.default_rng(sd)
            if cond == 'broad': U = qmc.Sobol(d, scramble=True, seed=sd).random(256)
            elif cond == 'central': U = np.clip(0.5 + rng.uniform(-0.10, 0.10, (256, d)), 0, 1)
            else: P = rng.random((3, d)); U = np.clip(P[rng.integers(0, 3, 256)] + rng.normal(0, 0.01, (256, d)), 0, 1)
            vals.append([np.median(UM.nn(UM.d1(U))), np.median(UM.nn(UM.d2(U, sl))), np.median(UM.nn(UM.d2med(U, sl)))])
        row[cond] = np.mean(vals, 0).tolist()
    prof[pop] = row
print('\nprofile study (median NN; broad / central / converge) D1 | D2 | D2med')
for pop, r in prof.items(): print(pop, 'd=%d slots=%d' % (r['d'], r['slots']), ' | '.join('%.3f/%.3f/%.3f' % (r['broad'][j], r['central'][j], r['converge'][j]) for j in range(3)))
B = np.array([prof[p]['broad'] for p in prof if p != 'SA']); C = np.array([prof[p]['central'] for p in prof if p != 'SA'])
print('CV of broad median NN across human-family profiles: D1 %.3f D2 %.3f D2med %.3f' % tuple(B.std(0) / B.mean(0)))
print('CV of central median NN: D1 %.3f D2 %.3f D2med %.3f' % tuple(C.std(0) / C.mean(0)))
json.dump(prof, open(S + '/profile.json', 'w'), indent=1)
# threshold options evaluated on every batch (N = 256)
def opt(r, o):
    a = r['D2']['frac_nn_below']['0.015'] <= 0.05
    if o == 'A': return a
    b = a and r['D2']['nn_p5'] >= 0.010 and min(r['slot_coverage'].values()) >= 0.05 and r['bundle']['lift'] <= 4.0 and (('canon_bundle' not in r) or r['canon_bundle']['share'] <= max(3 * r['canon_bundle']['uniform_expectation'], 0.02))
    if o == 'B': return b
    return b and r['D2']['nn_median'] >= 0.09 and min(r['slot_coverage'].values()) >= 0.5
tab = {}
for key, r in res.items():
    pop, cond, sd = key.split('_'); t = tab.setdefault((pop, cond), {o: 0 for o in 'ABC'})
    for o in 'ABC': t[o] += opt(r, o)
print('\noption pass counts (of 4 seeds): pop cond A B C')
for (pop, cond), t in tab.items(): print(pop, cond.ljust(12), t['A'], t['B'], t['C'])
json.dump({'%s_%s' % k: v for k, v in tab.items()}, open(S + '/options.json', 'w'), indent=1)
