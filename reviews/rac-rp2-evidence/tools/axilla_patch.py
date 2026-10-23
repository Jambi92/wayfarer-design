import sys, numpy as np, igl
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from patch import build_patch, apply, mirror_map; from hidden import hidden_quads
R_ = '/tmp/claude-0/rp2/'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 13; RING = sys.argv[2] if len(sys.argv) > 2 else '2'
b = np.load(R_ + 'sstar_p.npz'); V = b['V']; Q = b['Q']; m = b['mir']; arm = np.load(R_ + 'arm_p.npy') > 0.5
s0 = np.load(R_ + 'sstar.npz'); S0 = s0['V']; Q0 = s0['Q']; T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]
hq, sgn, ht = hidden_quads(S0, Q0); vis = ~ht
W = dict(np.load(R_ + 'weights_body.npz'))
armS = sum(W[k] for k in ('upperarm_l', 'lowerarm_l', 'hand_l', 'fingers_l', 'upperarm_r', 'lowerarm_r', 'hand_r', 'fingers_r')) > 0.5
C0 = S0[T0].mean(1)
RL = np.load(R_ + 'axR_%s.npy' % RING)
cr = np.load(R_ + 'crease_ax.npy'); cr = cr[np.argsort(cr[:, 1])]
# light smoothing of the crease polyline
for _ in range(int(__import__("os").environ.get("CSM","3"))): cr[1:-1] = 0.5 * cr[1:-1] + 0.25 * (cr[:-2] + cr[2:])
patches = []
fk = {frozenset(q): i for i, q in enumerate(Q.tolist())}
for side in (1, -1):
    if side == 1: R = RL; crease = cr
    else:
        R = np.zeros(len(Q), bool)
        for i in np.where(RL)[0]: R[fk[frozenset(m[Q[i]].tolist())]] = True
        crease = cr * np.array([-1, 1, 1])
    near = (np.sign(C0[:, 0]) == side) & (np.abs(C0[:, 0]) > 8) & (C0[:, 2] > 150) & (C0[:, 2] < 185)
    envA = T0[vis & near & armS[T0].any(1)]; envB = T0[vis & near & (~armS[T0]).any(1)]
    patches.append(build_patch(V, Q, R, arm, crease, N, envA, envB, S0))
V2, Q2, o2n, seams = apply(V, Q, patches)
m2 = mirror_map(V2, 1e-3)
old = np.where(o2n >= 0)[0]                                      # carry the input mirror map for surviving vertices (keeps freed ones free)
mo = m[old]; okm = mo >= 0
m2[o2n[old]] = np.where(okm, o2n[np.where(okm, mo, 0)], -1)
E_ = np.vstack([Q2[:, [i, (i + 1) % 4]] for i in range(4)]); u, c = np.unique(E_, axis=0, return_counts=True)
key = np.unique(np.sort(E_, 1), axis=0, return_counts=True)[1]
print('verts', len(V2), 'quads', len(Q2), 'directed dup', (c > 1).sum(), 'edge counts', np.unique(key), 'euler', len(V2) - len(key) + len(Q2), 'mirror defined', (m2 >= 0).mean())
sc = o2n[b['seam_crotch']]
np.savez(R_ + 'sstar_pp.npz', V=V2, Q=Q2, mir=m2, seam_crotch=sc, seam_axL=seams[0], seam_axR=seams[1], crease_crotch=b['crease_crotch'], crease_axL=cr, crease_axR=cr * np.array([-1, 1, 1]))
