# axilla_fix.py: base-level arm/trunk contact resolution on the patched target (arm is the mover; trunk organization untouched)
import sys, numpy as np, igl, json, subprocess
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
R_ = '/tmp/claude-0/rp2/'
b = np.load(R_ + 'sstar_p.npz'); V = b['V'].copy(); Q = b['Q']; mir = b['mir']; o2n = b['o2n']
Wb = dict(np.load(R_ + 'weights_body.npz')); n = len(V)
n2o = -np.ones(n, int); n2o[o2n[o2n >= 0]] = np.where(o2n >= 0)[0]
arm = np.zeros(n)
for k in ('upperarm_l', 'lowerarm_l', 'hand_l', 'fingers_l', 'upperarm_r', 'lowerarm_r', 'hand_r', 'fingers_r'):
    arm[n2o >= 0] += Wb[k][n2o[n2o >= 0]]
isarm = arm > 0.5
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
armT = isarm[T].all(1); trunkT = (~isarm[T]).all(1)
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum(); sgn = 1.0 if vol > 0 else -1.0
GAP = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
import scipy.sparse as sp
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
region = isarm & (np.abs(V[:, 0]) > 10) & (V[:, 2] > 140) & (V[:, 2] < 172.5)
TT = T[trunkT & (np.abs(V[T][:, :, 0]).mean(1) > 8) & (V[T][:, :, 2].mean(1) > 135) & (V[T][:, :, 2].mean(1) < 190)]
nn = np.cross(V[TT[:, 1]] - V[TT[:, 0]], V[TT[:, 2]] - V[TT[:, 0]]); TN = sgn * nn / np.linalg.norm(nn, axis=1)[:, None]
moved = np.zeros(n, bool)
for it in range(60):
    idx = np.where(region)[0]
    w = np.abs(igl.winding_number(V[TT[:, :]].reshape(-1, 3), np.arange(len(TT) * 3).reshape(-1, 3), V[idx]))  # inside the local trunk sheet?
    d, fi, cp = igl.point_mesh_squared_distance(V[idx], V, TT)
    sd = ((V[idx] - cp) * TN[fi]).sum(1)
    bad = sd < GAP                                   # arm vertex not at least GAP outside the trunk surface it faces
    bad &= np.sqrt(d) < 3.0
    if not bad.any(): break
    V[idx[bad]] = cp[bad] + TN[fi[bad]] * GAP; moved[idx[bad]] = True
    # relax moved arm vertices' 2-ring neighbours (arm only) toward their neighbours, keeps the flattened patch smooth
    ring = moved.copy()
    for _ in range(2): ring = ring | ((A @ ring.astype(float)) > 0)
    ring &= isarm
    L = (A @ V) / deg[:, None] - V; V[ring & ~moved] += 0.3 * L[ring & ~moved]
    # keep symmetric
    m = mir >= 0; V[m] = 0.5 * (V[m] + V[mir[m]] * np.array([-1, 1, 1]))
    print('iter', it, 'pushed', int(bad.sum()), flush=True)
print('moved arm verts', moved.sum())
np.savez(R_ + 'sstar_pa.npz', V=V, Q=Q, mir=mir, o2n=o2n, isarm=isarm, moved=moved)
