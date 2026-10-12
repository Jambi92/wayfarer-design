# sxdiag.py SID : locations of piercing edges in GO5F<SID> vs the route baseline
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05f_drivers')
from f_common import *
def sx(V, F, keep, cell=3.0):
    Fk = F[keep[F].all(1)]; E = np.unique(np.sort(np.r_[Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]], 1), axis=0)
    lo = V.min(0); key = lambda P: np.floor((P - lo) / cell).astype(np.int64)
    tmin = key(V[Fk].min(1)); tmax = key(V[Fk].max(1)); grid = {}
    for i, (a, b) in enumerate(zip(tmin, tmax)):
        for x in range(a[0], b[0] + 1):
            for y in range(a[1], b[1] + 1):
                for z in range(a[2], b[2] + 1): grid.setdefault((x, y, z), []).append(i)
    emid = key(0.5 * (V[E[:, 0]] + V[E[:, 1]])); pairs = []
    for ei, c in enumerate(map(tuple, emid)):
        for fi in grid.get(c, ()): pairs.append((ei, fi))
    P = np.array(pairs); e = E[P[:, 0]]; f = Fk[P[:, 1]]
    adj = (e[:, :1] == f).any(1) | (e[:, 1:] == f).any(1); P, e, f = P[~adj], e[~adj], f[~adj]
    o = V[e[:, 0]]; dvec = V[e[:, 1]] - o; v0, v1, v2 = V[f[:, 0]], V[f[:, 1]], V[f[:, 2]]
    e1 = v1 - v0; e2 = v2 - v0; h = np.cross(dvec, e2); a = np.einsum('ij,ij->i', e1, h); ok = np.abs(a) > 1e-9
    inv = np.where(ok, 1 / np.where(ok, a, 1), 0); s = o - v0; u = inv * np.einsum('ij,ij->i', s, h); q = np.cross(s, e1)
    v = inv * np.einsum('ij,ij->i', dvec, q); t = inv * np.einsum('ij,ij->i', e2, q)
    hit = ok & (u > 1e-6) & (v > 1e-6) & (u + v < 1 - 1e-6) & (t > 1e-6) & (t < 1 - 1e-6)
    return E[np.unique(P[hit, 0])], {tuple(x) for x in E[np.unique(P[hit, 0])]}, P[hit], f[hit]
n = 'GO5F' + sys.argv[1]
B = np.load(CG.path(n) + '_r6.npz', allow_pickle=True); V = B['V'].astype(float); F = B['F']; keep = B['keep'].astype(bool)
Vr = CG.route_baseline(B); V0, B0, L0, J0, f0, z0 = route_state(SKELETON_BODY); R = regions(B, V0, J0)
lab = np.array(['-'] * len(V), dtype=object)
for k, m in R.items(): lab[m] = k[:10]
Eb, sb, _, fb = sx(V, F, keep); Er, sr, _, _ = sx(Vr, F, keep)
new = [e for e in Eb if tuple(e) not in sr]
print('built', len(Eb), 'route', len(Er), 'new', len(new), 'gone', len(sr - sb))
from collections import Counter
c = Counter()
for a, b in new:
    m = (V[a] + V[b]) / 2; c[(lab[a], lab[b], 'L' if m[0] > 0 else 'R', int(m[2] // 10 * 10))] += 1
for k, v in sorted(c.items(), key=lambda x: -x[1]): print(v, k)
if len(sys.argv) > 2:
    Vs = read_obj(sys.argv[2])[0]; Vf = V0.copy(); Vf[:NBODY] = Vs
    Es, ss, _, _ = sx(Vf, F, keep); E0, s0, _, _ = sx(V0, F, keep)
    print('RAW delivered', len(Es), 'template', len(E0), 'new raw', len(ss - s0))
