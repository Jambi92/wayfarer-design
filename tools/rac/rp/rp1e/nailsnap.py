# nailsnap.py IN.npz OUT.npz : local nail free-edge support (order 647fa4e s7).  For each of the 8 nails the production vertex
# nearest to the frozen source nail tip (AW4 plate vertex of max projection on the recorded foot axis) is placed on that tip and its
# 1-ring is relaxed onto the source surface; nothing else moves (no global toe/foot length change).
import sys, json, numpy as np, igl
E = '/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/nail_tooling/'
inp, out = sys.argv[1:3]
z = np.load(inp); V = z['V'].astype(float).copy(); Q = z['Q'].astype(np.int64)
X = np.load('/home/claude/stc/rp1/AW4_VF.npz')['V'].astype(float); M = np.load(E + 'nailmasks.npy', allow_pickle=True).item(); A = json.load(open(E + 'footaxes_fit.json'))
w = np.load('/home/claude/stc/rp1/weld_a.npz'); S = w['V'].astype(float); SF = w['F'].astype(np.int64)
fl = np.array([1, -1, 1]); rec = {}
for n in sorted(M):
    a = np.array(A[n[0]]['a']); P = X[M[n]]; T = P[np.argmax(P @ a)] * 100 * fl            # analysis frame cm
    d = np.linalg.norm(V - T, axis=1); v = int(np.argmin(d))
    qs = np.where((Q == v).any(1))[0]; ring = np.setdiff1d(np.unique(Q[qs]), [v])
    old = V[v].copy(); V[v] = T
    sf = np.linalg.norm(S[SF].mean(1) - T, axis=1) < 1.0
    _, _, cp = igl.point_mesh_squared_distance(0.7 * V[ring] + 0.3 * T, S, SF[sf]); V[ring] = cp
    rec[n] = dict(vertex=v, moved_mm=round(float(np.linalg.norm(old - T) * 10), 3), ring=ring.tolist())
np.savez_compressed(out, V=V, F=z['F'], Q=z['Q']); json.dump(rec, open(out.replace('.npz', '_nails.json'), 'w'), indent=1)
print({k: v['moved_mm'] for k, v in rec.items()})
