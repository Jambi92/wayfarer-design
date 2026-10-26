# ring_search.py : candidate closed-ring insertions for v002 loop-count shortfall stations (order 103c832 §4: minimal thenar / hypothenar / root loops)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
B = load(); Q = B['Q2']; M = B['M2']; UV = B['UV2']; nV = M.shape[0]; loops = closed_loops(Q, nV)
targets = sys.argv[1].split(',')
St = {C: {s[0]: s for s in stations(B[C]['meta'])} for C in 'MF'}
def score(Qx, Mx, nm):
    out = {}
    for C in 'MF':
        V = Mx @ B[C]['Vh']; nm_, c, d, Wd, Rr, need, Rp = St[C][nm]; r = Auditor(V, Qx).band(np.asarray(c), np.asarray(d), Wd, Rr, Rp); out[C] = (r['loops'], r['loops_by_side'])
    return out
for nm in targets:
    print('==', nm, 'v002', score(Q, M, nm))
    cands = []
    for C in 'M':
        V = M @ B[C]['Vh']; _, c, d, Wd, Rr, need, Rp = St[C][nm]; d = unit(np.asarray(d))
        for li, L in enumerate(loops):
            P = V[L] - c; t = P @ d; rad = np.linalg.norm(P - np.outer(t, d), axis=1); inb = (np.abs(t) <= 1.5 * Wd) & (rad <= Rr)
            if inb.sum() >= 2: cands.append(li)
    # adjacent pairs forming a clean strip
    cs = set(cands); seen = set(); res = []
    vl = {}
    for li in cands:
        for v in loops[li]: vl.setdefault(int(v), []).append(li)
    for li in cands:
        A = loops[li]; sa = set(A.tolist())
        nb = set()
        for q in Q[np.nonzero(np.isin(Q, A).sum(1) == 2)[0]].tolist():
            for v in q:
                if v not in sa:
                    for lj in vl.get(v, []):
                        if lj != li: nb.add(lj)
        for lj in nb:
            key = (min(li, lj), max(li, lj))
            if key in seen or len(loops[lj]) != len(A): continue
            seen.add(key); out = insert_ring(Q, UV, M, A.tolist(), loops[lj].tolist())
            if out is None: continue
            Qx, UVx, Mx, ext = out; sc = score(Qx, Mx, nm); res.append((min(sc['M'][0], sc['F'][0]), key, len(A), sc))
    res.sort(key=lambda x: -x[0])
    for r in res[:8]: print('   ', r)
