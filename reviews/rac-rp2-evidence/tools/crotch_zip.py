# crotch_zip.py OUT.npz : resolve the crotch lens of S* by mid-plane clipping + mirror zip (MPFB topology kept):
#  side vertices that crossed x = 0 are clipped onto the mid-plane, quads that then lie entirely on the mid-plane (the hidden
#  perineal strip and the hidden thigh overlap) are removed, mirror vertex pairs on the mid-plane are merged (zip), and the seam
#  is snapped down onto the true crease (lower envelope of the x = 0 section).
import sys, numpy as np, json
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from xsec import sec
R = '/tmp/claude-0/rp2/'
s = np.load(R + 'sstar.npz'); V = s['V'].copy(); Q = s['Q']; m = np.load(R + 'mir_body.npy'); W2 = np.load(R + 'w2_body.npz')['V']
box = (np.abs(V[:, 0]) < 8) & (V[:, 2] > 104) & (V[:, 2] < 121) & (V[:, 1] > -8) & (V[:, 1] < 16)
side = np.where(W2[:, 0] > 0.05, 1, np.where(W2[:, 0] < -0.05, -1, 0))
clip = box & ((side == 1) & (V[:, 0] < 0.0) | (side == -1) & (V[:, 0] > 0.0) | (side == 0))
V[clip, 0] = 0.0
onp = box & (np.abs(V[:, 0]) < 1e-9)
slit = onp[Q].all(1)
print('clipped', int(clip.sum()), 'mid-plane verts', int(onp.sum()), 'slit quads', int(slit.sum()))
Qk = Q[~slit]
# zip: merge mirror pairs lying on the mid-plane
rep = np.arange(len(V))
for v in np.where(onp)[0]:
    w = m[v]
    if w != v and onp[w]: rep[max(v, w)] = min(v, w)
Qz = rep[Qk]
# drop degenerate / duplicate faces
deg = np.array([len(set(q)) < 4 for q in Qz.tolist()]); Qz = Qz[~deg]
key = [tuple(sorted(q)) for q in Qz.tolist()]
from collections import Counter
c = Counter(key); dup = np.array([c[k] > 1 for k in key]); Qz = Qz[~dup]
used = np.zeros(len(V), bool); used[Qz.ravel()] = True; o2n = -np.ones(len(V), int); o2n[used] = np.arange(used.sum())
Vn = V[used]; Qn = o2n[Qz]
E = np.vstack([Qn[:, [i, (i + 1) % 4]] for i in range(4)]); u, cnt = np.unique(np.sort(E, 1), axis=0, return_counts=True)
dirdup = (np.unique(E, axis=0, return_counts=True)[1] > 1).sum()
print('degenerate removed', int(deg.sum()), 'duplicates removed', int(dup.sum()), 'edge use', dict(zip(*np.unique(cnt, return_counts=True))), 'directed dup', int(dirdup),
      'euler', len(Vn) - len(u) + len(Qn))
seam = o2n[np.where(onp & used & (rep == np.arange(len(V))))[0]]
seam = seam[seam >= 0]
np.savez(sys.argv[1], V=Vn, Q=Qn, o2n=o2n, seam=seam)
