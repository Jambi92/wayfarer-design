# build.py OUT.npz [iters] [d_t2_mm] [d_t1_mm] : Grask RP2 production branch from the adjudicated target S*
import sys, json, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from subdiv import subdivide_levels; from zones import base_zones; from hidden import hidden_quads
R = '/tmp/claude-0/rp2/'
out = sys.argv[1]; IT = int(sys.argv[2]) if len(sys.argv) > 2 else 30
D2 = float(sys.argv[3]) / 10 if len(sys.argv) > 3 else 0.04; D1 = float(sys.argv[4]) / 10 if len(sys.argv) > 4 else 0.10
z = np.load(R + 'sstar.npz'); S0 = z['V']; Q0 = z['Q']; mir0 = np.load(R + 'mir_body.npy'); W2 = np.load(R + 'w2_body.npz')['V']
W = dict(np.load(R + 'weights_body.npz')); J = json.loads(str(np.load(R + 'GR5DE3_r6.npz')['joints']))
Q, n, S, mir = subdivide_levels(Q0, len(S0), 2, mir0); S = S.tocsr()
P = S @ S0; Pw2 = S @ W2
ok = mir >= 0; res = np.zeros(n); res[ok] = np.abs(P[ok] - P[mir[ok]] * np.array([-1, 1, 1])).max(1); mir[res > 1e-3] = -1
# envelope: visible S* triangles
T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]; hq, sgn, ht = hidden_quads(S0, Q0)
# zones (production level via interpolation of base indicator fields)
bz = base_zones(S0, W, J); pz = {k: (S @ v.astype(float)) > 0.5 for k, v in bz.items()}
hid_v = np.zeros(len(S0)); hid_v[np.unique(T0[ht])] = 1
A0 = igl.adjacency_matrix(T0).astype(float)
cz0 = hid_v.copy()
for _ in range(6): cz0 = np.maximum(cz0, (A0 @ cz0 > 0).astype(float))          # contact zone: 6 rings around hidden faces
cz = (S @ cz0) > 0.5
armw = sum(W[k] for k in ('upperarm_l', 'lowerarm_l', 'hand_l', 'fingers_l')), sum(W[k] for k in ('upperarm_r', 'lowerarm_r', 'hand_r', 'fingers_r'))
def labels(aL, aR, x):
    lab = np.where(x > 0.05, 1, np.where(x < -0.05, 2, 0)); lab = np.where(aL > 0.5, 3, lab); lab = np.where(aR > 0.5, 4, lab); return lab
labB = labels(armw[0], armw[1], W2[:, 0]); labP = labels(S @ armw[0], S @ armw[1], Pw2[:, 0])
labT = np.array([np.bincount(labB[t], minlength=5).argmax() for t in T0])
allow = {0: [0, 1, 2], 1: [0, 1], 2: [0, 2], 3: [3], 4: [4]}
vis = ~ht
groups = {}
for l in range(5):
    groups[l] = np.where(vis & np.isin(labT, allow[l]))[0]
allvis = np.where(vis)[0]
# Laplacian (uniform, quad edges)
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
delta = np.where(pz['T2'], D2, D1); delta[cz] = 0.0
def tri_normals(V, T): nn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); return sgn * nn / np.linalg.norm(nn, axis=1)[:, None]
TN = tri_normals(S0, T0)
def constrain(P):
    out = P.copy()
    # non-contact vertices: any visible face; contact-zone vertices: label-restricted visible faces
    idx = np.where(~cz)[0]; d, fi, cp = igl.point_mesh_squared_distance(P[idx], S0, T0[allvis]); fi = allvis[fi]
    sd = ((P[idx] - cp) * TN[fi]).sum(1); out[idx] = cp + TN[fi] * np.clip(sd, -delta[idx], delta[idx])[:, None]
    for l in range(5):
        idx = np.where(cz & (labP == l))[0]
        if not len(idx): continue
        g = groups[l]; d, fi, cp = igl.point_mesh_squared_distance(P[idx], S0, T0[g]); out[idx] = cp + TN[g[fi]] * 0.003   # 0.03 mm outward
    return out
def symm(P):
    m = mir >= 0; Pm = P.copy(); Pm[m] = 0.5 * (P[m] + P[mir[m]] * np.array([-1, 1, 1])); self_ = m & (mir == np.arange(n)); Pm[self_, 0] = 0.0; return Pm
for it in range(IT):
    for f in (0.5, -0.53):
        L = (A @ P) / deg[:, None] - P; P = P + f * L
    P = symm(constrain(P))
    if it % 10 == 0: print('iter', it, flush=True)
np.savez(out, V=P, Q=Q, mir=mir, labP=labP, cz=cz, T2=pz['T2'], **{'zone_' + k: v for k, v in pz.items()})
sp.save_npz(out.replace('.npz', '_S.npz'), S)
print('saved', out, n, len(Q))
