import numpy as np, sys
from scipy import ndimage as ndi
s = sys.argv[1]; step = float(sys.argv[2]); ndig = int(sys.argv[3])
g = np.load('/home/claude/stc/rp1e/geo_%s.npz' % s); idx = g['idx']; D = g['D']; lo = g['lo']; h = float(g['h']); shape = tuple(g['shape'])
ok = np.isfinite(D); idx = idx[ok]; D = D[ok]
bidx = np.floor(D / step).astype(int); nb = bidx.max() + 1; st = np.ones((3, 3, 3))
band = np.full(shape, -1, np.int32); band[tuple(idx.T)] = bidx
comp_of = np.zeros(shape, np.int32); info = [None]; nid = 0
for b in range(nb):
    l2, k = ndi.label(band == b, structure=st); sz = np.bincount(l2.ravel())
    remap = np.zeros(k + 1, np.int32)
    for c in range(1, k + 1):
        if sz[c] >= 150: nid += 1; remap[c] = nid; info.append(dict(band=b, n=int(sz[c])))
    m = l2 > 0; comp_of[m] = remap[l2[m]]
par = {}
I = idx; cI = comp_of[tuple(I.T)]; bI = band[tuple(I.T)]
for d in [(a, b_, c) for a in (-1, 0, 1) for b_ in (-1, 0, 1) for c in (-1, 0, 1) if (a, b_, c) != (0, 0, 0)]:
    q = I + d; v = (q >= 0).all(1) & (q < np.array(shape)).all(1); q = q[v]; cq = comp_of[tuple(q.T)]; bq = band[tuple(q.T)]
    m = (bq == bI[v] - 1) & (cq > 0) & (cI[v] > 0)
    pairs = np.unique(np.c_[cI[v][m], cq[m]], axis=0)
    for a, b_ in pairs.tolist(): par.setdefault(a, set()).add(b_)
child = {}
for c, ps in par.items():
    for p in ps: child.setdefault(p, set()).add(c)
leaves = [i for i in range(1, nid + 1) if i not in child]
digits = []
for lf in leaves:
    chain = [lf]; c = lf
    while c in par and len(par[c]) == 1 and len(child.get(next(iter(par[c])), ())) == 1: c = next(iter(par[c])); chain.append(c)
    digits.append((sum(info[q]['n'] for q in chain), chain))
digits.sort(reverse=True)
for k, (vol, chain) in enumerate(digits[:9]):
    print(k, 'vol cm3 %.1f' % (vol * h ** 3), 'D %.1f-%.1f' % (info[chain[-1]]['band'] * step, (info[chain[0]]['band'] + 1) * step),
          'base parents', [(p, len(child[p])) for p in par.get(chain[-1], [])])
lab = np.zeros(shape, np.int8)
for k, (vol, chain) in enumerate(digits[:ndig]):
    lab[np.isin(comp_of, chain)] = k + 2
lab[(band >= 0) & (lab == 0)] = 1
np.savez_compressed('/home/claude/stc/rp1e/lab_%s.npz' % s, lab=lab, lo=lo, h=h)
