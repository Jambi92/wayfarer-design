"""Toe segmentation by foot-axis sweep: region {u > t} of the foot surface for t decreasing from the tips;
each connected component containing exactly one toe-tip seed is assigned to that toe (first assignment wins).
Toe index: 0 = hallux (most medial) ... 4. Output fseg_S.npz (used, lab with 9 = forefoot/rest).
Usage: python3 footseg.py S step"""
import numpy as np, sys, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
s = sys.argv[1]; step = float(sys.argv[2])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'].astype(float); F = w['F'].astype(np.int64)
LM = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))
L = LM['toe_tips_' + s]; ax = np.array(L['foot_axis']) * [1, -1, 0]; ax /= np.linalg.norm(ax)
tips = np.array(L['points']) * [1, -1, 1]
A = LM['ankle_' + s]; pp = np.array(A['plane_point']) * [1, -1, 1]; nn = np.array(A['plane_normal']) * [1, -1, 1]
foot = (w['w_foot_' + s] > 0.5) | ((w['w_shin_' + s] > 0.5) & (((V - pp) @ nn) > -1.5))
Fh = F[foot[F].all(1)]; used = np.unique(Fh); mp = -np.ones(len(V), np.int64); mp[used] = np.arange(len(used))
X = V[used]; Fl = mp[Fh]; n = len(X)
C0 = np.array(A['centroid']) * [1, -1, 1]; C0 = C0 - float(sys.argv[4]) * ax; C0[2] = 2.0
u = np.linalg.norm((X - C0)[:, :2], axis=1)
E = np.unique(np.sort(np.concatenate([Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]]), 1), axis=0)
med = -np.sign(X[:, 0].mean()) * np.array([1.0, 0, 0])
lab = -np.ones(n, int); seeds = []
for t in np.arange(u.max(), u.max() - 25, -step):
    m = u > t; idx = np.where(m)[0]
    if len(idx) < 2: continue
    e = E[m[E[:, 0]] & m[E[:, 1]]]; li = -np.ones(n, np.int64); li[idx] = np.arange(len(idx))
    nc, cl = connected_components(coo_matrix((np.ones(len(e)), (li[e[:, 0]], li[e[:, 1]])), shape=(len(idx), len(idx))), directed=False)
    full = -np.ones(n, int); full[idx] = cl
    sz = np.bincount(cl)
    for c in range(nc):
        vv = idx[cl == c]
        ts = [k for k, sv in enumerate(seeds) if full[sv] == c]
        if not ts and sz[c] > int(sys.argv[3]) and len(seeds) < 5: seeds.append(int(vv[np.argmax(u[vv])])); ts = [len(seeds) - 1]
        if len(ts) == 1: vv = vv[lab[vv] < 0]; lab[vv] = ts[0]
    if len(seeds) == 5 and len(set(full[seeds])) == 1: print('all toes merged at t=%.1f' % t); break
order = sorted(range(len(seeds)), key=lambda k: -(X[seeds[k]] @ med)); rm = {k: i for i, k in enumerate(order)}
lab = np.array([rm[q] if q >= 0 else -1 for q in lab])
lab[lab < 0] = 9
# drop the heel protrusion (centroid behind the ankle along the foot axis) and renumber medial->lateral
for k in range(5):
    if (lab == k).any() and (X[lab == k].mean(0) - C0) @ ax < 0: lab[lab == k] = 9
ks = [k for k in range(5) if (lab == k).any()]; ks.sort(key=lambda k: -(X[lab == k].mean(0) @ med))
lab = np.array([ks.index(q) if q in ks else 9 for q in lab])
print(s, {int(k): int((lab == k).sum()) for k in np.unique(lab)})
for k in range(4): P = X[lab == k]; print('  toe', k, P.mean(0).round(1), 'u range %.1f..%.1f' % (u[lab == k].min(), u[lab == k].max()))
np.savez_compressed('fseg_%s.npz' % s, used=used, lab=lab, ax=ax)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cm = {0: 'r', 1: 'g', 2: 'b', 3: 'm', 4: 'c', 9: '0.8'}; col = np.array([cm[q] for q in lab])
sel = u > u.max() - 20
fig, axs = plt.subplots(1, 3, figsize=(30, 10))
for a, (i_, j, k, sg) in zip(axs, [(0, 1, 2, 1), (0, 2, 1, 1), (0, 1, 2, -1)]):
    Y = X[sel]; c = col[sel]; o = np.argsort(sg * Y[:, k]); a.scatter(Y[o, i_], Y[o, j], c=c[o], s=1); a.set_aspect('equal')
plt.savefig('fseg_%s.png' % s, dpi=45, bbox_inches='tight')
