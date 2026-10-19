"""Zone re-layout aid (design only): place selected cage vertices
 - junction vertices on the source segment-label boundary curve (nearest boundary point),
 - other vertices at `inset` cm inside their own colour-core surface,
then alternate Laplacian relaxation (movable, non-junction) and re-placement. Outputs new cage + move list.
Usage: python3 zonefit.py cage.npz cage_col.npy TCORE junction.json movable.npy boundary.npy inset iters OUT.npz"""
import numpy as np, sys, json, igl
from scipy.spatial import cKDTree
cg, colp, tp, jp, mp_, bp, inset, iters, out = sys.argv[1:10]; inset = float(inset); iters = int(iters)
z = np.load(cg); V = z['V'].astype(float).copy(); V0 = V.copy(); F = z['F']; col = np.load(colp)
J = np.array(json.load(open(jp)), int); mov = np.load(mp_); B = np.load(bp)
adj = {}
for f in F:
    f = f[f >= 0]
    for j in range(len(f)): p_, q_ = int(f[j]), int(f[(j + 1) % len(f)]); adj.setdefault(p_, set()).add(q_); adj.setdefault(q_, set()).add(p_)
T = {}
for c in np.unique(col[mov]):
    t = np.load('%s_c%d.npz' % (tp, c)); T[int(c)] = (t['V'].astype(float), t['F'].astype(np.int64))
BT = cKDTree(B)
free = np.where(mov)[0]; free = np.array([i for i in free if i not in set(J.tolist())], int)
def place():
    _, k = BT.query(V[J]); V[J] = B[k]
    for c, (TV, TF) in T.items():
        idx = free[col[free] == c]
        if not len(idx): continue
        S, I, C = igl.point_mesh_squared_distance(V[idx], TV, TF)
        T3 = TV[TF[I]]; N = np.cross(T3[:, 1] - T3[:, 0], T3[:, 2] - T3[:, 0]); N /= np.linalg.norm(N, axis=1)[:, None]
        V[idx] = C - inset * N
for it in range(iters):
    place()
    Vn = V.copy()
    for i in free: Vn[i] = 0.5 * V[i] + 0.5 * V[list(adj[i])].mean(0)
    V[:] = Vn
place()
np.savez_compressed(out, V=V, F=F)
mv = [dict(v=int(i), old=V0[i].round(3).tolist(), new=V[i].round(3).tolist()) for i in np.where(mov)[0]]
json.dump(mv, open(out.replace('.npz', '_moves.json'), 'w'), indent=0)
print('moved', len(mv), 'mean shift %.2f max %.2f' % (np.mean([np.linalg.norm(np.array(m['new']) - np.array(m['old'])) for m in mv]), max(np.linalg.norm(np.array(m['new']) - np.array(m['old'])) for m in mv)))
