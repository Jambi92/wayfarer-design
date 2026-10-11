# RAC RM-UF-05: batch-diversity metrics on normalized DIR vectors (DIAGNOSTIC; no frequency model).
import numpy as np
from scipy.spatial.distance import pdist, squareform
def d1(U): return squareform(pdist(U) / np.sqrt(U.shape[1]))                      # flat normalized RMS
def d2(U, sl):
    S = sorted(set(sl)); acc = np.zeros((len(U), len(U)))
    for s in S:
        m = sl == s; acc += squareform(pdist(U[:, m]) ** 2 / m.sum())                 # within-slot mean-square distance
    return np.sqrt(acc / len(S))                                                       # equal slot weight
def d2med(U, sl):
    S = sorted(set(sl)); st = np.stack([squareform(pdist(U[:, sl == s]) / np.sqrt((sl == s).sum())) for s in S]); return np.median(st, 0)
def nn(D):
    D = D.copy(); np.fill_diagonal(D, np.inf); return D.min(1)
def eff_rank(U):
    w = np.clip(np.linalg.eigvalsh(np.cov(U.T)), 0, None); p = w / w.sum(); p = p[p > 0]; return float(np.exp(-(p * np.log(p)).sum()))
def slot_cov(U, sl):
    return {int(s): float(U[:, sl == s].std(0).mean() / (1 / np.sqrt(12))) for s in sorted(set(sl))}  # 1.0 = uniform spread over the span
def bundle(U, sl):
    """most common multi-slot tercile tuple (slot score = mean of its normalized axes); share vs the independence expectation"""
    S = sorted(set(sl)); T = np.stack([np.digitize(U[:, sl == s].mean(1), [1 / 3, 2 / 3]) for s in S], 1)
    keys, cnt = np.unique(T, axis=0, return_counts=True); i = cnt.argmax(); share = cnt[i] / len(U)
    exp = np.prod([np.mean(T[:, j] == keys[i][j]) for j in range(len(S))])
    return dict(tuple={int(S[j]): ['low', 'mid', 'high'][keys[i][j]] for j in range(len(S))}, share=float(share), independent_expectation=float(exp), lift=float(share / max(exp, 1e-9)))
def summary(U, sl, clone_tau=(0.015, 0.02, 0.05, 0.08)):
    out = {}
    for nm, D in (('D1', d1(U)), ('D2', d2(U, sl)), ('D2med', d2med(U, sl))):
        n = nn(D); out[nm] = dict(nn_median=float(np.median(n)), nn_p5=float(np.percentile(n, 5)), nn_p95=float(np.percentile(n, 95)),
                                  frac_nn_below={str(t): float((n < t).mean()) for t in clone_tau}, pair_median=float(np.median(D[np.triu_indices(len(U), 1)])))
    sc = slot_cov(U, sl); out['slot_coverage'] = sc; out['most_converged_slot'] = min(sc, key=sc.get); out['eff_rank'] = eff_rank(U); out['eff_rank_frac'] = eff_rank(U) / U.shape[1]
    out['bundle'] = bundle(U, sl); return out
