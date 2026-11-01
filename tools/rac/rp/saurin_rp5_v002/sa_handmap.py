# sa_handmap.py DESIGN_P.pkl DESIGN_B.pkl CAGE_B.npz OUT.npz : Option B hand / foot PARAMETERISED placement (order fe3b98a: webs, palm / forefoot
#   creases, thumb). Every authored hand / foot coarse quad of the pre-split design (a 2 x 2 block after sa_localsub -> a regular 17 x 17 fine grid) is
#   laid onto the working source WITHOUT closest-point projection (which collapses grid rows into the narrow web slots / creases):
#   1. its four sides = geodesic (Dijkstra) paths on the source between its authored corners (one path per coarse edge, shared by both neighbours);
#   2. the block's source region = flood fill from its centre bounded by those vertex paths (a vertex path separates the triangulated surface);
#   3. Tutte map of the region onto the unit square (paths -> sides by arc length) -> fold-free; 4. the fine grid placed at its own (i/16, j/16)
#   parameters and lifted back through the map (barycentric on source faces). Side chains are re-spaced uniformly along the paths.
#   Blocks whose region is not a clean disk are left unchanged (reported). Topology unchanged.
import sys, os, pickle, collections, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
DP, DB, CG, OUT = sys.argv[1:5]
dp = pickle.load(open(DP, 'rb')); db = pickle.load(open(DB, 'rb')); nmB = list(db['name']); ixB = {n: i for i, n in enumerate(nmB)}
Cb = np.array(db['C']); Qb = np.array(db['Q']); Vf, Qf, src = Cb.copy(), Qb.copy(), np.arange(len(Qb))
for _ in range(3): Vf, Qf, src = CC.cc(Vf, Qf, src)
z = dict(np.load(CG)); Q = z['Q']; nqf = len(Qf); assert np.array_equal(Q[:nqf], Qf); fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); nv = len(V)
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
HAND = {'palm', 'finger', 'finger_web', 'finger_cap', 'thumb', 'thumb_cap'}; FOOT = {'ankle', 'foot', 'forefoot', 'toe', 'toe_web', 'toe_cap'}
SKIP = set(os.environ.get('SKIP_LABELS', '').split(','))
qlP = list(dp['qlab']); nmP = list(dp['name']); QP = np.array(dp['Q'])
blocks = [q for q, l in enumerate(qlP) if l in HAND | FOOT and l not in SKIP]
# source graph with edge lengths
E = np.unique(np.sort(np.r_[G.F[:, [0, 1]], G.F[:, [1, 2]], G.F[:, [2, 0]]], 1), axis=0); w = np.linalg.norm(G.V[E[:, 0]] - G.V[E[:, 1]], axis=1)
GW = sp.coo_matrix((np.r_[w, w], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(len(G.V), len(G.V))).tocsr(); kdS = cKDTree(G.V)
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); vf = {}                     # source vertex -> one incident face
for f_, tri in enumerate(G.F):
    for v_ in tri: vf.setdefault(int(v_), f_)
def snapv(p): return int(kdS.query(p)[1])
paths = {}
def geopath(a, b):
    """geodesic vertex path between fine corners a, b (fine cage indices) on the source, inside a corridor ball"""
    key = (min(a, b), max(a, b))
    if key in paths: return None if paths[key] is None else (paths[key] if key[0] == a else paths[key][::-1])
    sa, sb = snapv(V[a]), snapv(V[b]); c = 0.5 * (G.V[sa] + G.V[sb]); r = 0.75 * np.linalg.norm(G.V[sa] - G.V[sb]) + 1.0
    sub = np.array(kdS.query_ball_point(c, r), int); loc = -np.ones(len(G.V), int); loc[sub] = np.arange(len(sub))
    GS = GW[sub][:, sub]; dist, pred = dijkstra(GS, indices=loc[sa], return_predecessors=True)
    if not np.isfinite(dist[loc[sb]]): paths[key] = None; return None
    p = [loc[sb]]
    while p[-1] != loc[sa]: p.append(pred[p[-1]])
    p = sub[np.array(p[::-1])]; paths[key] = p if key[0] == a else p[::-1]; return p
def geopath_avoid(a, b, avoid):
    sa, sb = snapv(V[a]), snapv(V[b]); c = 0.5 * (G.V[sa] + G.V[sb]); r = 0.75 * np.linalg.norm(G.V[sa] - G.V[sb]) + 1.0
    sub = np.array([x for x in kdS.query_ball_point(c, r) if x not in avoid], int); loc = -np.ones(len(G.V), int); loc[sub] = np.arange(len(sub))
    if loc[sa] < 0 or loc[sb] < 0: return None
    dist, pred = dijkstra(GW[sub][:, sub], indices=loc[sa], return_predecessors=True)
    if not np.isfinite(dist[loc[sb]]): return None
    p = [loc[sb]]
    while p[-1] != loc[sa]: p.append(pred[p[-1]])
    return sub[np.array(p[::-1])]
used_edges = set()
def chain_fine(qs, ca, cb):
    """the fine cage vertex chain between fine corners ca -> cb along the block border (16 hops)"""
    fq = np.nonzero(np.isin(src, qs))[0]; ec = collections.Counter((min(x, y), max(x, y)) for f in fq for x, y in zip(Qf[f], np.roll(Qf[f], -1)))
    adj = collections.defaultdict(list)
    for (x, y), c in ec.items():
        if c == 1: adj[x].append(y); adj[y].append(x)
    return adj, fq
def arcparam(P):
    L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; return L / max(L[-1], 1e-12)
acc = 0; WHY = collections.Counter(); moved = np.zeros(nv, bool)
for qp in blocks:
    cnames = [nmP[i] for i in QP[qp]]; cf = [ixB[n] for n in cnames]                     # corner fine indices (coarse index = fine index)
    subs = sorted({src[i] for i in range(nqf) if False})                                   # (filled below)
    # the 4 b-design sub-quads of this block contain the face point 'subf_<qp>'
    sq = [i for i, q in enumerate(Qb) if ixB.get('subf_%d' % qp, -1) in q]
    if len(sq) != 4: WHY['no 2x2 block'] += 1; continue
    adj, fq = chain_fine(sq, None, None)
    # border loop from corner 0, oriented so that the next corner is cf[1] after 16 hops
    loop = [cf[0], adj[cf[0]][0]]
    while loop[-1] != cf[0]:
        nx = [y for y in adj[loop[-1]] if y != loop[-2]]
        if not nx: break
        loop.append(nx[0])
    loop = loop[:-1]
    if len(loop) != 64: WHY['border not 64'] += 1; continue
    if loop[16] != cf[1]: loop = [loop[0]] + loop[1:][::-1]
    if [loop[16 * k] for k in range(4)] != cf: WHY['corner order'] += 1; continue
    sides = [loop[16 * k:16 * k + 17] if k < 3 else loop[48:] + [loop[0]] for k in range(4)]
    gp = [geopath(cf[k], cf[(k + 1) % 4]) for k in range(4)]
    if any(p is None for p in gp): WHY['no geodesic'] += 1; continue
    bar = np.concatenate(gp); bset = set(bar.tolist())
    if len(bset) != len(bar) - 4:
        # re-route the block's not-yet-shared sides so they avoid the vertices of its other sides (cached shared sides are kept)
        fixed_k = [k for k in range(4) if (min(cf[k], cf[(k + 1) % 4]), max(cf[k], cf[(k + 1) % 4])) in used_edges]
        for k in [k for k in range(4) if k not in fixed_k]:
            others = set(np.concatenate([gp[j] for j in range(4) if j != k]).tolist()) - {snapv(V[cf[k]]), snapv(V[cf[(k + 1) % 4]])}
            pk = geopath_avoid(cf[k], cf[(k + 1) % 4], others)
            if pk is not None: gp[k] = pk
        bar = np.concatenate(gp); bset = set(bar.tolist())
        if len(bset) != len(bar) - 4: WHY['paths cross'] += 1; continue
        for k in range(4): paths[(min(cf[k], cf[(k + 1) % 4]), max(cf[k], cf[(k + 1) % 4]))] = gp[k] if cf[k] < cf[(k + 1) % 4] else gp[k][::-1]
    # seed: source vertex nearest the block centre fine vertex (face point), not on the barrier; flood bounded by the paths
    # seed: middle of the geodesic between the midpoints of two opposite sides, avoiding the barrier (robust when the old grid is crumpled)
    m0 = gp[0][len(gp[0]) // 2]; m2 = gp[2][len(gp[2]) // 2]
    sub_ = np.array([x for x in kdS.query_ball_point(0.5 * (G.V[m0] + G.V[m2]), 0.75 * np.linalg.norm(G.V[m0] - G.V[m2]) + 1.0) if x not in bset or x in (m0, m2)], int)
    loc_ = -np.ones(len(G.V), int); loc_[sub_] = np.arange(len(sub_)); seed = None
    if loc_[m0] >= 0 and loc_[m2] >= 0:
        dist_, pred_ = dijkstra(GW[sub_][:, sub_], indices=loc_[m0], return_predecessors=True)
        if np.isfinite(dist_[loc_[m2]]):
            pp = [loc_[m2]]
            while pp[-1] != loc_[m0]: pp.append(pred_[pp[-1]])
            pp = sub_[np.array(pp[::-1])]; inner_ = [x for x in pp if x not in bset]
            if inner_: seed = int(inner_[len(inner_) // 2])
    if seed is None:
        cen_f = ixB['subf_%d' % qp]; seed = snapv(V[cen_f])
    if seed in bset: WHY['seed on barrier'] += 1; continue
    lim = 4.0 * max(np.linalg.norm(V[cf[0]] - V[cf[2]]), np.linalg.norm(V[cf[1]] - V[cf[3]])) + 1.0
    cand = np.array(kdS.query_ball_point(G.V[seed], lim), int); inball = np.zeros(len(G.V), bool); inball[cand] = True
    region = {seed}; front = [seed]; leak = False
    while front:
        nxt = []
        for u in front:
            for x in G.G.indices[G.G.indptr[u]:G.G.indptr[u + 1]]:
                if x in region or x in bset: continue
                if not inball[x]: leak = True; break
                region.add(x); nxt.append(x)
            if leak: break
        if leak: break
        front = nxt
    if leak: WHY['flood leaks (paths do not enclose)'] += 1; continue
    rv = np.array(sorted(region | bset)); loc = -np.ones(len(G.V), int); loc[rv] = np.arange(len(rv))
    Fm = np.nonzero((loc[G.F] >= 0).all(1))[0]; Fl = loc[G.F[Fm]]
    chi = len(rv) - len(np.unique(np.sort(np.r_[Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]], 1), axis=0)) + len(Fl)
    if chi != 1: WHY['region chi %d' % chi] += 1; continue
    uvb = {}
    for k, p in enumerate(gp):
        t = arcparam(G.V[p])
        for v_, s_ in zip(p, t): uvb[int(v_)] = [(s_, 0), (1, s_), (1 - s_, 1), (0, 1 - s_)][k]
    isb = np.array([v_ in uvb for v_ in rv]); ii = np.nonzero(~isb)[0]; bi_ = np.nonzero(isb)[0]
    A = igl.adjacency_matrix(Fl).astype(float); deg = np.asarray(A.sum(1)).ravel(); Lm = (sp.diags(deg) - A).tocsr()
    UV = np.zeros((len(rv), 2)); UV[bi_] = np.array([uvb[int(rv[i])] for i in bi_])
    try: UV[ii] = np.stack([spl.spsolve(Lm[ii][:, ii].tocsc(), -(Lm[ii][:, bi_] @ UV[bi_, k])) for k in range(2)], 1)
    except Exception: WHY['solve'] += 1; continue
    # fine grid parameters: regular 17 x 17 via a Tutte solve on the fine block (border sides at j/16)
    vsB = np.unique(Qf[fq]); uvg = {}
    for k, s_ in enumerate(sides):
        for j, v_ in enumerate(s_): t = j / 16.0; uvg[v_] = [(t, 0), (1, t), (1 - t, 1), (0, 1 - t)][k]
    inner = [v_ for v_ in vsB if v_ not in uvg]; li = {v_: i for i, v_ in enumerate(inner)}
    EB = {(min(x, y), max(x, y)) for f in fq for x, y in zip(Qf[f], np.roll(Qf[f], -1))}; nb_ = collections.defaultdict(list)
    for x, y in EB: nb_[x].append(y); nb_[y].append(x)
    M = sp.lil_matrix((len(inner), len(inner))); Bv = np.zeros((len(inner), 2))
    for v_ in inner:
        M[li[v_], li[v_]] = len(nb_[v_])
        for y in nb_[v_]:
            if y in li: M[li[v_], li[y]] -= 1
            else: Bv[li[v_]] += uvg[y]
    X = np.atleast_2d(spl.spsolve(M.tocsc(), Bv))
    for v_, x in zip(inner, X): uvg[v_] = tuple(x)
    # lift every block vertex (border chains re-spaced along the geodesic paths) through the map
    cen2 = UV[Fl].mean(1); kd2 = cKDTree(cen2); ok = True; newf = {}; newb = {}
    for v_ in vsB:
        if pin[v_]: continue
        x = np.array(uvg[v_]); found = False
        for f in kd2.query(x, k=min(80, len(Fl)))[1]:
            a_, b_, c_ = UV[Fl[f]]; Mt = np.array([b_ - a_, c_ - a_]).T
            if abs(np.linalg.det(Mt)) < 1e-16: continue
            l = np.linalg.solve(Mt, x - a_); wv = np.r_[1 - l.sum(), l]
            if wv.min() > -1e-6: newf[v_] = Fm[f]; newb[v_] = np.clip(wv, 0, 1) / np.clip(wv, 0, 1).sum(); found = True; break
        if not found: ok = False; break
    if not ok: WHY['grid point outside map'] += 1; continue
    for v_ in newf: fiv[v_] = newf[v_]; bcv[v_] = newb[v_]; moved[v_] = True
    for k in range(4): used_edges.add((min(cf[k], cf[(k + 1) % 4]), max(cf[k], cf[(k + 1) % 4])))
    acc += 1
V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1)
# seam relaxation: unmapped vertices (2:1 transitions, unmapped blocks) within SEAM rings of the mapped region -> tangential umbrella + sheet-consistent
# re-projection, mapped vertices fixed
T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; Ec = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
Ac = sp.coo_matrix((np.ones(2 * len(Ec)), (np.r_[Ec[:, 0], Ec[:, 1]], np.r_[Ec[:, 1], Ec[:, 0]])), shape=(nv, nv)).tocsr(); degc = np.asarray(Ac.sum(1)).ravel()
zoneB = moved.copy()
for _ in range(int(os.environ.get('SEAM', 4))): zoneB |= (Ac @ zoneB.astype(float)) > 0
fr = np.nonzero(zoneB & ~moved & ~pin)[0]; ab = igl.AABB(); ab.init(G.V, G.F)
for it in range(40):
    N_ = np.nan_to_num(igl.per_vertex_normals(V, T_)); L_ = (Ac @ V) / degc[:, None] - V; L_ -= (L_ * N_).sum(1)[:, None] * N_
    P_ = V[fr] + 0.4 * L_[fr]; _, ff_, cp_ = ab.squared_distance(G.V, G.F, P_); wr_ = (FN[ff_] * N_[fr]).sum(1) < 0.2
    if wr_.any(): _, _, cp2 = ab.squared_distance(G.V, G.F, P_[wr_] - 0.1 * N_[fr][wr_]); cp_[wr_] = cp2
    V[fr] = cp_
fi2, bc2, _ = G.embed(V[fr]); fiv[fr] = fi2; bcv[fr] = bc2
print('seam vertices relaxed', len(fr))
print('blocks', len(blocks), 'parameterised', acc, dict(WHY), 'vertices placed', int(moved.sum()))
z['V'] = V; z['tri'] = fiv; z['bc'] = bcv; np.savez_compressed(OUT, **z)
