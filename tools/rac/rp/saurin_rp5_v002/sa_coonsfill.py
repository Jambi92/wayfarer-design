# sa_coonsfill.py DESIGN_P.pkl DESIGN_B.pkl IN.npz OUT.npz : fallback for the hand / foot blocks sa_handmap could not map (handmap_block_ok == 0):
#   the block's 17 x 17 fine grid is rebuilt as a Coons patch over its four current border chains (re-spaced by arc length) at its Tutte grid parameters,
#   then every vertex is projected onto the working source sheet-consistently (closest point; if the hit face disagrees with the patch normal, re-queried
#   from 1 mm inside). Kept per block only if the block's host-aware inverted / bow-tie count drops. Topology unchanged.
import sys, os, pickle, collections, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
DP, DB, IN, OUT = sys.argv[1:5]; dp = pickle.load(open(DP, 'rb')); db = pickle.load(open(DB, 'rb')); nmB = list(db['name']); ixB = {n: i for i, n in enumerate(nmB)}
Cb = np.array(db['C']); Qb = np.array(db['Q']); Vf, Qf, src = Cb.copy(), Qb.copy(), np.arange(len(Qb))
for _ in range(3): Vf, Qf, src = CC.cc(Vf, Qf, src)
z = dict(np.load(IN)); Q = z['Q']; fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); nv = len(V); ok_ = z['handmap_block_ok']
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); ab = igl.AABB(); ab.init(G.V, G.F)
qlP = list(dp['qlab']); nmP = list(dp['name']); QP = np.array(dp['Q'])
def bad_count(fq, Vc, tri):
    P4 = Vc[Qf[fq]]; nr = FN[tri[Qf[fq]]].sum(1); return int((np.einsum('ij,ij->i', np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]), nr) < 0).sum())
acc = 0; tried = 0
for qp in range(len(QP)):
    if 'subf_%d' % qp not in ixB: continue
    sq = [i for i, q in enumerate(Qb) if ixB['subf_%d' % qp] in q]; fq = np.nonzero(np.isin(src, sq))[0]
    if not len(fq) or ok_[fq[0]] != 0: continue
    tried += 1; cf = [ixB[nmP[i]] for i in QP[qp]]
    ec = collections.Counter((min(x, y), max(x, y)) for f in fq for x, y in zip(Qf[f], np.roll(Qf[f], -1))); adj = collections.defaultdict(list)
    for (x, y), c in ec.items():
        if c == 1: adj[x].append(y); adj[y].append(x)
    loop = [cf[0], adj[cf[0]][0]]
    while loop[-1] != cf[0]: loop.append([y for y in adj[loop[-1]] if y != loop[-2]][0])
    loop = loop[:-1]
    if len(loop) != 64: continue
    if loop[16] != cf[1]: loop = [loop[0]] + loop[1:][::-1]
    if [loop[16 * k] for k in range(4)] != cf: continue
    sides = [loop[16 * k:16 * k + 17] if k < 3 else loop[48:] + [loop[0]] for k in range(4)]
    vs = np.unique(Qf[fq]); uvg = {}
    for k, s_ in enumerate(sides):
        for j, v_ in enumerate(s_): t = j / 16.0; uvg[v_] = [(t, 0), (1, t), (1 - t, 1), (0, 1 - t)][k]
    inner = [v_ for v_ in vs if v_ not in uvg]; li = {v_: i for i, v_ in enumerate(inner)}; nb_ = collections.defaultdict(set)
    for f in fq:
        for x, y in zip(Qf[f], np.roll(Qf[f], -1)): nb_[x].add(y); nb_[y].add(x)
    M = sp.lil_matrix((len(inner), len(inner))); Bv = np.zeros((len(inner), 2))
    for v_ in inner:
        M[li[v_], li[v_]] = len(nb_[v_])
        for y in nb_[v_]:
            if y in li: M[li[v_], li[y]] -= 1
            else: Bv[li[v_]] += uvg[y]
    X = np.atleast_2d(spl.spsolve(M.tocsc(), Bv))
    for v_, x in zip(inner, X): uvg[v_] = tuple(x)
    curves = []
    for s_ in sides:
        P_ = V[s_]; L_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P_, axis=0), axis=1))]; L_ /= max(L_[-1], 1e-12); curves.append((L_, P_))
    def cv(k, t): L_, P_ = curves[k]; return np.array([np.interp(t, L_, P_[:, d]) for d in range(3)])
    C0, C1, C2, C3 = V[cf[0]], V[cf[1]], V[cf[2]], V[cf[3]]; nn = FN[fiv[cf]].sum(0); nn /= np.linalg.norm(nn)
    Pn = V.copy()
    for v_ in vs:
        if pin[v_] or v_ in cf: continue
        u, w = uvg[v_]
        Pn[v_] = (1 - w) * cv(0, u) + w * cv(2, 1 - u) + (1 - u) * cv(3, 1 - w) + u * cv(1, w) - ((1 - u) * (1 - w) * C0 + u * (1 - w) * C1 + u * w * C2 + (1 - u) * w * C3)
    mv = np.array([v_ for v_ in vs if not pin[v_] and v_ not in cf])
    _, ff, cp = ab.squared_distance(G.V, G.F, Pn[mv]); wr = FN[ff] @ nn < 0.2
    if wr.any(): _, ff2, cp2 = ab.squared_distance(G.V, G.F, Pn[mv][wr] - 0.1 * nn); cp[wr] = cp2; ff[wr] = ff2
    Pn[mv] = cp; fi2, bc2, _ = G.embed(Pn[mv]); tri2 = fiv.copy(); tri2[mv] = fi2
    if bad_count(fq, Pn, tri2) < bad_count(fq, V, fiv): V = Pn; fiv[mv] = fi2; bcv[mv] = bc2; acc += 1
print('failed blocks tried', tried, 'improved by Coons fill', acc)
z['V'] = V; z['tri'] = fiv; z['bc'] = bcv; np.savez_compressed(OUT, **z)
