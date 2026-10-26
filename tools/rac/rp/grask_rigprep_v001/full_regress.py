# full_regress.py OUT.json REF_DIR REF_TAG CAND_DIR CAND_TAG [CAND_TAG ...] : 43-pose suite regression (order 69f2660 §21). For every pose: max |X_cand - X_ref|
# (cm) and whether the posed arrays are bit-identical, plus the retained criteria that pass for the reference but fail for the candidate (new failures) and
# those fixed. REF = the unchanged W0 suite.
import sys, os, json, numpy as np
O, RDIR, RT = sys.argv[1:4]; CD = sys.argv[4]; TAGS = sys.argv[5:]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
R0 = json.load(open('%s/diag/diag_results_full_%s.json' % (RDIR, RT)))['results']; OUT = {}
for t in TAGS:
    R1 = json.load(open('%s/diag/diag_results_full_%s.json' % (CD, t)))['results']; rows = {}
    for p in sorted(R0):
        a = np.load('%s/diag/posed/%s_full_%s.npz' % (RDIR, p, RT))['V']; b = np.load('%s/diag/posed/%s_full_%s.npz' % (CD, p, t))['V']
        f0 = {c[0] for c in crit(p, R0[p]) if not c[1]}; f1 = {c[0] for c in crit(p, R1[p]) if not c[1]}
        rows[p] = dict(bit_identical=bool(a.shape == b.shape and (a.view(np.uint32) == b.view(np.uint32)).all()), max_dev_cm=round(float(np.abs(a.astype(float) - b.astype(float)).max()), 5),
                       new_failures=sorted(f1 - f0), fixed=sorted(f0 - f1))
    OUT[t] = rows
    ch = [p for p, r in rows.items() if not r['bit_identical']]
    print(t, 'changed poses:', len(ch), ch); print(t, 'new failures:', {p: r['new_failures'] for p, r in rows.items() if r['new_failures']}); print(t, 'fixed:', {p: r['fixed'] for p, r in rows.items() if r['fixed']})
json.dump(OUT, open(O, 'w'), indent=1)
