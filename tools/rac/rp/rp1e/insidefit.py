"""Design aid: move selected cage vertices to sit a fixed depth inside their OWN colour-target surface
(closest point on own target minus delta * outward normal). Writes a new cage npz + a move list (old -> new) for UI authoring.
Usage: python3 insidefit.py cage.npz cage_col.npy TPREFIX boxes.json delta OUT.npz"""
import numpy as np, sys, json, igl
cg, colp, tp, bxp, delta, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), sys.argv[6]
z = np.load(cg); V = z['V'].astype(float).copy(); F = z['F']; col = np.load(colp)
boxes = json.load(open(bxp))
sel = np.zeros(len(V), bool)
for b in boxes:
    lo, hi = np.array(b[0]), np.array(b[1]); sel |= ((V > lo) & (V < hi)).all(1)
moves = []
for c in np.unique(col[sel]):
    t = np.load('%s_c%d.npz' % (tp, c)); TV = t['V'].astype(float); TF = t['F'].astype(np.int64)
    idx = np.where(sel & (col == c))[0]
    S, I, C = igl.point_mesh_squared_distance(V[idx], TV, TF)
    T3 = TV[TF[I]]; N = np.cross(T3[:, 1] - T3[:, 0], T3[:, 2] - T3[:, 0]); S = np.sqrt(S)
    for k, i in enumerate(idx):
        n = N[k] / np.linalg.norm(N[k]); new = C[k] - delta * n
        moves.append(dict(v=int(i), old=V[i].round(3).tolist(), new=new.round(3).tolist(), sd=round(float(S[k]), 2)))
        V[i] = new
np.savez_compressed(out, V=V, F=F)
json.dump(moves, open(out.replace('.npz', '_moves.json'), 'w'), indent=0)
print('moved', len(moves), 'mean shift %.2f' % np.mean([np.linalg.norm(np.array(m['new']) - np.array(m['old'])) for m in moves]))
