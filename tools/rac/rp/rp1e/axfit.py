"""Axilla re-layout on the crease (design only, cloud).
1) movable set M = axilla verts of the e30 re-layout (by position) [+ ring neighbours if GROW];
2) junction loop J = min vertex separator (networkx) between arm seeds and trunk seeds through M, vertex cost = 1 + K*d(v,B)^2,
   B = crease points (+ colour-boundary points of the source where there is no crease);
3) cage colours inside M by flood from the seeds with J removed; J keep nearest-source colour;
4) zonefit-like: J -> nearest point of B; free M -> INSET cm inside own colour target; Laplacian relax; repeat.
Usage: python3 axfit.py CAGE.npz SRC_COL.npy TPREFIX OUT.npz [K INSET ITERS GROW]"""
import numpy as np, sys, json, igl, networkx as nx
from scipy.spatial import cKDTree
cg, colp, tp, out = sys.argv[1:5]; K = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
INSET = float(sys.argv[6]) if len(sys.argv) > 6 else 0.6; ITERS = int(sys.argv[7]) if len(sys.argv) > 7 else 30; GROW = int(sys.argv[8]) if len(sys.argv) > 8 else 0
z = np.load(cg); V = z['V'].astype(float).copy(); V0 = V.copy(); F = z['F']
w = np.load('/home/claude/stc/rp1/weld.npz'); S = w['V'].astype(float); SF = w['F']; scol = np.load(colp)
_, ni = cKDTree(S).query(V); cc = scol[ni].copy()
adj = {}
for f in F:
    f = f[f >= 0]
    for j in range(len(f)): a, b = int(f[j]), int(f[(j + 1) % len(f)]); adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
mv = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/axilla_ui_moves_e30.json'))
P = np.array(list(mv.values())); d, M = cKDTree(V).query(P); print('M match max', d.max().round(3))
M = set(M.tolist())
for g in range(GROW): M |= set(j for i in list(M) for j in adj[i] if cc[j] in (1, 2))
# source colour-boundary points (1|2) and creases
E = np.unique(np.sort(np.concatenate([SF[:, [0, 1]], SF[:, [1, 2]], SF[:, [2, 0]]]), 1), axis=0)
be = E[((scol[E[:, 0]] == 1) & (scol[E[:, 1]] == 2)) | ((scol[E[:, 0]] == 2) & (scol[E[:, 1]] == 1))]
BP = (S[be[:, 0]] + S[be[:, 1]]) / 2
T = {c: (lambda t: (t['V'].astype(float), t['F'].astype(np.int64)))(np.load('%s_c%d.npz' % (tp, c))) for c in (1, 2)}
newcol = cc.copy(); J_all = []
for s, sg in (('R', -1), ('L', 1)):
    Ms = [i for i in M if V[i, 0] * sg > 0]
    Cr = np.load('crease_%s.npy' % s)[:, :3]
    side = (BP[:, 0] * sg > 10) & (BP[:, 0] * sg < 36) & (BP[:, 2] > 120) & (BP[:, 2] < 175) & (BP[:, 1] > -60) & (BP[:, 1] < 5)
    Bs = np.vstack([Cr, BP[side][cKDTree(Cr).query(BP[side])[0] > 2.0]])   # crease where it exists, else colour boundary
    BT = cKDTree(Bs)
    Mset = set(Ms)
    ring = set(j for i in Ms for j in adj[i]) - Mset            # first verts outside M = seeds
    arm = [j for j in ring if cc[j] == 2]; trunk = [j for j in ring if cc[j] == 1]
    G = nx.DiGraph()
    dB, _ = BT.query(V[Ms]); cost = {i: 1.0 + K * dB[k] ** 2 for k, i in enumerate(Ms)}
    for i in Ms: G.add_edge(('in', i), ('out', i), capacity=cost[i])
    def node_in(i): return ('in', i) if i in Mset else ('t', i)
    def node_out(i): return ('out', i) if i in Mset else ('t', i)
    for i in Ms + list(ring):
        for j in adj[i]:
            if j in Mset or j in ring:
                if i in Mset or j in Mset: G.add_edge(node_out(i), node_in(j), capacity=1e9)
    for j in arm: G.add_edge('SRC', ('t', j), capacity=1e9)
    for j in trunk: G.add_edge(('t', j), 'SNK', capacity=1e9)
    cut, (Sset, Tset) = nx.minimum_cut(G, 'SRC', 'SNK')
    J = [i for i in Ms if ('in', i) in Sset and ('out', i) in Tset]
    # colours: flood with J removed
    Jset = set(J)
    for i in Ms:
        if i in Jset: continue
        newcol[i] = 2 if ('in', i) in Sset else 1
    dJ, _ = BT.query(V[J]); print(s, 'M', len(Ms), 'seeds arm/trunk', len(arm), len(trunk), 'J', len(J), 'cut', round(cut, 1), 'J dist to B before: mean %.2f max %.2f' % (dJ.mean(), dJ.max()))
    J_all.append((J, BT, Bs, Ms))
free = np.array([i for i in M if i not in set(j for J, _, _, _ in J_all for j in J)], int)
Jall = np.array([j for J, _, _, _ in J_all for j in J], int)
def place():
    for J, BT, Bs, Ms in J_all:
        _, k = BT.query(V[J]); V[J] = Bs[k]
    for c, (TV, TF) in T.items():
        idx = free[newcol[free] == c]
        if not len(idx): continue
        S2, I, C = igl.point_mesh_squared_distance(V[idx], TV, TF)
        T3 = TV[TF[I]]; N = np.cross(T3[:, 1] - T3[:, 0], T3[:, 2] - T3[:, 0]); N /= np.linalg.norm(N, axis=1)[:, None]
        V[idx] = C - INSET * N
for it in range(ITERS):
    place(); Vn = V.copy()
    for i in free: Vn[i] = 0.5 * V[i] + 0.5 * V[list(adj[i])].mean(0)
    V[:] = Vn
place()
np.savez_compressed(out, V=V, F=F); np.save(out.replace('.npz', '_col.npy'), newcol)
json.dump(dict(J=Jall.tolist(), M=sorted(int(i) for i in M)), open(out.replace('.npz', '_ax.json'), 'w'))
sh = np.linalg.norm(V - V0, axis=1)[list(M)]; print('moved', len(M), 'mean shift %.2f max %.2f' % (sh.mean(), sh.max()))
