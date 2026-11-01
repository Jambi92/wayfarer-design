# sa_reparam.py DESIGN.pkl IN.npz OUT.npz : SOURCE-PARAMETERISED re-sampling of folded coarse quads (order 236dddc §6-§9: webs, palm / forefoot 2:1 rows,
#   orbit fans). Each authored coarse quad carries an 8 x 8 fine grid. For a folded coarse quad, the working-source region it covers (source faces whose
#   nearest cage quad belongs to it, largest component, must be a disk) is mapped onto the unit square by a uniform-weight (Tutte) harmonic map whose border
#   follows the quad's four fine side chains (arc-length parameter); every interior fine vertex is then placed at its own grid parameter in that map and
#   lifted back onto the source -> the grid wraps webs / creases without folding. Side chains are re-spaced by arc length along themselves. Topology unchanged.
import sys, os, pickle, collections, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
DS, IN, OUT = sys.argv[1:4]; MINF = int(os.environ.get('MINF', 2))
d = pickle.load(open(DS, 'rb')); Cc = np.array(d['C']); Qc = np.array(d['Q']); ncq = len(Qc); qlc = np.array(d['qlab'])
Vf, Qf, src = Cc.copy(), Qc.copy(), np.arange(ncq)
for _ in range(3): Vf, Qf, src = CC.cc(Vf, Qf, src)
z = dict(np.load(IN)); Q = z['Q']; fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); nqf = len(Qf); nv = len(V); nb = int(z['n_body'])
intact = np.all(Q[:nqf] == Qf, axis=1); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; tq = np.r_[np.arange(len(Q)), np.arange(len(Q))]
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.13, 0.27)
def foldv(Vc): N = np.nan_to_num(igl.per_vertex_normals(Vc, T)); return (FN[fiv] * N).sum(1) < 0.2
fv = foldv(V) & ~pin; fq = np.zeros(ncq, int); 
for i in np.nonzero(fv[Q[:nqf]].any(1))[0]: fq[src[i]] += 1
okq = np.array([intact[src == q].all() for q in range(ncq)])
SEL = [q for q in np.argsort(-fq) if fq[q] >= MINF and okq[q] and qlc[q] not in ('tail',)]
print('folded vertices', int(fv.sum()), 'coarse quads to re-sample', len(SEL), flush=True)
cg = igl.AABB(); cg.init(V, T); _, ti_s, _ = cg.squared_distance(V, T, G.V); hostq = np.where(tq[ti_s] < nqf, src[np.minimum(tq[ti_s], nqf - 1)], -1)
d0 = np.sqrt(cg.squared_distance(V, T, G.V)[0])
def sides_of(q):
    fq_ = np.nonzero(src == q)[0]; ec = collections.Counter((min(a, b), max(a, b)) for f in fq_ for a, b in zip(Qf[f], np.roll(Qf[f], -1)))
    adj = collections.defaultdict(list)
    for (a, b), c in ec.items():
        if c == 1: adj[a].append(b); adj[b].append(a)
    cs = list(Qc[q]); loop = [cs[0], adj[cs[0]][0]]
    while loop[-1] != cs[0]: loop.append([w for w in adj[loop[-1]] if w != loop[-2]][0])
    loop = loop[:-1]
    if loop[8] != cs[1]: loop = [loop[0]] + loop[1:][::-1]
    if [loop[8 * k] for k in range(4)] != cs: return None, None
    sides = [loop[8 * k: 8 * k + 9] if k < 3 else loop[24:] + [loop[0]] for k in range(4)]
    vs = np.unique(Qf[fq_]); E2 = {(min(a, b), max(a, b)) for f in fq_ for a, b in zip(Qf[f], np.roll(Qf[f], -1))}; nbr = collections.defaultdict(list)
    for a, b in E2: nbr[a].append(b); nbr[b].append(a)
    uvg = {}
    for k, s_ in enumerate(sides):
        for j, v in enumerate(s_): t = j / 8.0; uvg[v] = [(t, 0), (1, t), (1 - t, 1), (0, 1 - t)][k]
    inner = [v for v in vs if v not in uvg]; li = {v: i for i, v in enumerate(inner)}; M = sp.lil_matrix((len(inner), len(inner))); B = np.zeros((len(inner), 2))
    for v in inner:
        M[li[v], li[v]] = len(nbr[v])
        for w in nbr[v]:
            if w in li: M[li[v], li[w]] -= 1
            else: B[li[v]] += uvg[w]
    X = np.atleast_2d(spl.spsolve(M.tocsc(), B))
    for v, x in zip(inner, X): uvg[v] = tuple(x)
    return sides, (inner, uvg)
acc = 0; WHY = collections.Counter()
for q in SEL:
    sides, g_ = sides_of(q)
    if sides is None: WHY['side order'] += 1; continue
    inner, uvg = g_; inner = [v for v in inner if not pin[v]]
    # source region: source faces all of whose vertices are hosted by this coarse quad (+ 1 face ring), largest component, disk
    m = hostq == q; Fm = np.nonzero(m[G.F].sum(1) >= 2)[0]
    if len(Fm) < 20: WHY['tiny region'] += 1; continue
    Fs = G.F[Fm]; sv, Finv = np.unique(Fs, return_inverse=True); Fl = Finv.reshape(-1, 3)
    FA = sp.coo_matrix((np.ones(3 * len(Fl)), (np.repeat(np.arange(len(Fl)), 3), Fl.ravel())), shape=(len(Fl), len(sv))).tocsr(); ncc, cl = connected_components(FA @ FA.T, directed=False)
    big = np.argmax(np.bincount(cl)); Fm = Fm[cl == big]; Fs = G.F[Fm]; sv, Finv = np.unique(Fs, return_inverse=True); Fl = Finv.reshape(-1, 3)
    chi = len(sv) - len(np.unique(np.sort(np.r_[Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]], 1), axis=0)) + len(Fl)
    if chi != 1: WHY['region not a disk (chi %d)' % chi] += 1; continue
    bl = igl.boundary_loop(Fl)
    # border -> square: nearest point on the 4 side chains (arc-length parameter along the chain)
    pts = []; par = []
    for k, s_ in enumerate(sides):
        P_ = V[s_]; L_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P_, axis=0), axis=1))]
        for j in range(8):
            for t in np.linspace(0, 1, 6, endpoint=False):
                pts.append(P_[j] + t * (P_[j + 1] - P_[j])); s01 = (L_[j] + t * (L_[j + 1] - L_[j])) / L_[-1]; par.append([(s01, 0), (1, s01), (1 - s01, 1), (0, 1 - s01)][k])
    pts = np.array(pts); par = np.array(par); bp = par[cKDTree(pts).query(G.V[sv[bl]])[1]]
    # enforce monotone boundary order (sort the boundary by its square perimeter coordinate)
    per = np.where(bp[:, 1] == 0, bp[:, 0], np.where(bp[:, 0] == 1, 1 + bp[:, 1], np.where(bp[:, 1] == 1, 3 - bp[:, 0], 4 - bp[:, 1])))
    if np.sum(np.diff(np.r_[per, per[0]]) < -2) + np.sum(np.diff(np.r_[per, per[0]]) > 2) > 2: WHY['non-monotone border'] += 1; continue
    Lu = -igl.adjacency_matrix(Fl).astype(float); Lu = Lu - sp.diags(np.asarray(Lu.sum(1)).ravel()); isb = np.zeros(len(sv), bool); isb[bl] = True
    ii = np.nonzero(~isb)[0]; UV = np.zeros((len(sv), 2)); UV[bl] = bp
    if len(ii): UV[ii] = np.stack([spl.spsolve((-Lu)[ii][:, ii].tocsc(), -((-Lu)[ii][:, bl] @ bp[:, k])) for k in range(2)], 1)
    # place the interior fine vertices at their grid parameters
    cen2 = UV[Fl].mean(1); kd2 = cKDTree(cen2); newf = []; newb = []; ok = True
    for v in inner:
        x = np.array(uvg[v]); found = False
        for f in kd2.query(x, k=min(60, len(Fl)))[1]:
            a, b_, c_ = UV[Fl[f]]; Mt = np.array([b_ - a, c_ - a]).T
            if abs(np.linalg.det(Mt)) < 1e-14: continue
            l = np.linalg.solve(Mt, x - a); w = np.r_[1 - l.sum(), l]
            if w.min() > -1e-6: newf.append(Fm[f]); newb.append(np.clip(w, 0, 1) / np.clip(w, 0, 1).sum()); found = True; break
        if not found: ok = False; break
    if not ok: WHY['grid point outside map'] += 1; continue
    P = V.copy(); P[inner] = (np.array(newb)[:, :, None] * G.V[G.F[np.array(newf)]]).sum(1); f0 = fiv.copy(); b0 = bcv.copy(); fiv[inner] = newf; bcv[inner] = newb
    rv = np.unique(Qf[src == q]); n0 = int(foldv(V)[rv].sum()); n1 = int(foldv(P)[rv].sum())
    svv = np.nonzero(m)[0]; Tl = np.r_[Qf[src == q][:, [0, 1, 2]], Qf[src == q][:, [0, 2, 3]]]
    db = np.sqrt(igl.point_mesh_squared_distance(G.V[svv], V, Tl)[0]); da = np.sqrt(igl.point_mesh_squared_distance(G.V[svv], P, Tl)[0])
    if n1 < n0 and not np.any((da > thr[svv]) & (da > db + 1e-5)): V = P; acc += 1
    else: fiv = f0; bcv = b0; WHY['no fold gain' if n1 >= n0 else 'coverage'] += 1
print(dict(WHY)); print('coarse quads re-sampled', acc, 'folded vertices now', int((foldv(V) & ~pin).sum()))
z['V'] = V; z['tri'] = fiv; z['bc'] = bcv; np.savez_compressed(OUT, **z)
