# crotch_slot.py DELTA_CM OUT.npz : vertex-only crotch resolution on S* (MPFB topology unchanged). The inner-thigh sheets crossed the
# mid-plane; every side vertex inside the crotch box is kept on its own side (|x| >= delta), the hidden pocket becomes a narrow open
# slot between the apposed inner thighs, roofed by the perineal strip. Positions stay on their own sheet except for the x clip.
import sys, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
R = '/tmp/claude-0/rp2/'
dl = float(sys.argv[1]); out = sys.argv[2]
s = np.load(R + 'sstar.npz'); V = s['V'].copy(); Q = s['Q']; W2 = np.load(R + 'w2_body.npz')['V']; m = np.load(R + 'mir_body.npy')
n = len(V); box = (np.abs(V[:, 0]) < 8) & (V[:, 2] > 100) & (V[:, 2] < 122) & (V[:, 1] > -10) & (V[:, 1] < 18)
W = dict(np.load(R + 'weights_body.npz')); dlr = W['thigh_l'] - W['thigh_r']
side = np.where(dlr > 0.03, 1, np.where(dlr < -0.03, -1, 0))                 # sheet = owning thigh (W2 x-sign is not reliable here)
# smooth taper of the clip so the walls blend into the visible inner thigh: target x' = side * max(side*x, ramp)
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
sel = box & (side != 0)
moved = sel & (side * V[:, 0] < dl)
V[moved, 0] = side[moved] * dl
# midline (bridge) vertices inside the box: x = 0 (already symmetric)
mid = box & (side == 0); V[mid, 0] = 0.0
# relax moved walls in their own plane (f, u) a little so faces are not folded, keeping x fixed
P = V.copy()
for it in range(30):
    L = (A @ P) / deg[:, None] - P; P[moved, 1:] += 0.3 * L[moved, 1:]
ok = m >= 0; P[ok] = 0.5 * (P[ok] + P[m[ok]] * np.array([-1, 1, 1])); s_ = ok & (m == np.arange(n)); P[s_, 0] = 0
np.savez(out, V=P, Q=Q, mir=m, moved=moved); print('moved', int(moved.sum()), 'mid', int(mid.sum()))
