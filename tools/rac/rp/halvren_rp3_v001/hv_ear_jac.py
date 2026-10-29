# hv_ear_jac.py JACDIR OUT.json [TARGET.json] : Halvren HE2 closure order §4 -- authored -> realized control sensitivity (finite-difference Jacobian of the
# measured ear domains with respect to each realization control, rest-state builds of hv_ear_try.py around HE2 on c1), the COUPLING read (which
# controls move which domains, normalised by the source pooled SD), and optionally a regularised least-squares solve for control steps that move the
# realized HE2 to a realized-space mosaic target (TARGET.json: {domain: target t vs the Marchfolk -> elf-mean line}; weights optional).
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
JD, OUT = sys.argv[1:3]; TG = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None; jl = lambda p: json.load(open(p))
SRC = jl(os.environ.get('HV_DOMSRC', '/tmp/claude-0/rt/hv/ear/src_dom.json'))['items']; DOM = D.DOM
X = {s: np.array([SRC[s][q] for q in DOM]) for s in ('MF', 'FN', 'AE', 'VA')}; sd = np.maximum(np.array(list(X.values())).std(0), [D.FLOOR[q] for q in DOM])
em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0); line = em - X['MF']
T = {os.path.basename(os.path.dirname(p)): jl(p) for p in glob.glob(JD + '/*/try.json')}; b = T.pop('base'); b0 = np.array([b['domains'][q] for q in DOM])
STEP = {}; J = {}; tech = {}
for k, r in T.items():
    kv = r['probe'].split('='); STEP[k] = (kv[0], float(kv[1])); J[k] = (np.array([r['domains'][q] for q in DOM]) - b0) / sd; tech[k] = r['tech']
res = dict(order='chatgpt-rac-rp3-halvren-he2-realization-ear-architecture-closure-order §4', base=dict(domains=b['domains'], t=b['t_vs_elf_mean'], firewall=b['firewall'], tech=b['tech']),
           controls={k: dict(control=STEP[k][0], value=STEP[k][1], response_sd={q: round(float(v), 3) for q, v in zip(DOM, J[k])}, technical=tech[k],
                             main=[q for q, v in sorted(zip(DOM, J[k]), key=lambda x: -abs(x[1]))[:3]]) for k in J})
print('%-7s' % 'ctrl', ' '.join('%7s' % q[:7] for q in DOM))
for k in J: print('%-7s' % k, ' '.join('%+7.2f' % v for v in J[k]), 'clean' if tech[k]['clean'] else 'FAIL %.1f' % tech[k]['min_angle'])
if TG:
    w = np.array([TG.get('weights', {}).get(q, 1.0) for q in DOM]); tt = np.array([TG['t'].get(q, np.nan) for q in DOM]); use = ~np.isnan(tt)
    tgt = (X['MF'] + tt * line); dz = np.where(use, (tgt - b0) / sd, 0) * w
    ks = [k for k in J if k in TG.get('controls', J.keys())]; A = np.array([J[k] for k in ks]).T * w[:, None]; lam = TG.get('lambda', 0.3)
    s = np.linalg.solve(A.T @ A + lam * np.eye(len(ks)), A.T @ dz)     # in units of the probe step
    pred = b0 + sd * (np.array([J[k] for k in ks]).T @ s)
    res['solve'] = dict(target=dict(zip(DOM, np.where(use, tgt, np.nan).round(4).tolist())), steps={k: round(float(v), 3) for k, v in zip(ks, s)},
                        predicted=dict(zip(DOM, pred.round(4).tolist())), predicted_t=dict(zip(DOM, ((pred - X['MF']) / np.where(np.abs(line) > 1e-9, line, 1)).round(2).tolist())))
    print('steps', res['solve']['steps']); print('pred t', res['solve']['predicted_t'])
json.dump(res, open(OUT, 'w'), indent=1)
