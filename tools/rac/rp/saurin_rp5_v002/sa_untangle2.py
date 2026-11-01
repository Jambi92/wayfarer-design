# sa_untangle2.py IN.npz OUT.npz : PARAMETER-SPACE untangling of folded cage regions (order 236dddc §9 hard stops: no folded / pathological quads).
#   A cage vertex is folded where its normal disagrees with the working source under it (dot < 0.2) -> the cage is locally inverted on the surface.
#   Each folded cluster (+RING quad rings) is a cage patch; the source surface under it (host faces grown GROW face rings, largest disk component) is
#   flattened by a harmonic map onto the unit disk (fold-free); the cage patch interior is re-embedded in that plane by a uniform Tutte solve with the
#   patch border fixed (fold-free for a disk) and mapped back onto the source through the flattening. Accepted per patch only if folded vertices drop and
#   no source vertex nearby ends above its zone threshold worse than before. Topology unchanged; shape is then restored by sa_gopt.
import sys, os, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
IN, OUT = sys.argv[1:3]; RING = int(os.environ.get('RING', 3)); GROW = int(os.environ.get('GROW', 4))
z = dict(np.load(IN)); Q = z['Q']; fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); nv = len(V); nq = len(Q); nb = int(z['n_body'])
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.13, 0.27); kdS = cKDTree(G.V)
TT = igl.triangle_triangle_adjacency(G.F)[0]
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
def folded(Vc):
    N = np.nan_to_num(igl.per_vertex_normals(Vc, T)); return (FN[fiv] * N).sum(1) < 0.2
fv = folded(V) & ~pin; fq = np.zeros(nq, bool); fq[np.unique(np.nonzero(fv[Q].any(1))[0])] = True
bi = np.nonzero(fq)[0]; nc, lab = connected_components(QQ[bi][:, bi], directed=False); print('folded vertices', int(fv.sum()), 'clusters', nc, flush=True)
acc = 0; WHY = collections.Counter()
for c in range(nc):
    reg = np.zeros(nq, bool); reg[bi[lab == c]] = True
    for _ in range(RING): reg = (QQ @ reg.astype(float)) > 0
    reg &= ~(Q >= nb).any(1); rq = np.nonzero(reg)[0]; rv = np.unique(Q[rq])
    out = np.zeros(nv, bool); out[Q[~reg].ravel()] = True; inner = rv[~out[rv] & ~pin[rv]]; border = rv[out[rv] | pin[rv]]
    if len(inner) < 1: continue
    # source disk under the patch: border-vertex host faces grown g face rings (g = 1..6), the connected component holding every border host, must be a disk
    disk = None
    for g in range(1, 7):
        sf = set(fiv[border].tolist()) | set(fiv[rv].tolist()); front = list(sf)
        for _ in range(g):
            nx = set(TT[front].ravel().tolist()) - sf - {-1}; sf |= nx; front = list(nx)
        sf = np.array(sorted(sf)); Fs = G.F[sf]; sv, Finv = np.unique(Fs, return_inverse=True); Fl = Finv.reshape(-1, 3)
        FA = sp.coo_matrix((np.ones(3 * len(Fl)), (np.repeat(np.arange(len(Fl)), 3), Fl.ravel())), shape=(len(Fl), len(sv))).tocsr()
        ncc, cl = connected_components(FA @ FA.T, directed=False)
        fpos = {f: i for i, f in enumerate(sf)}; bc_ = cl[[fpos[f] for f in fiv[border]]]
        if len(set(bc_.tolist())) != 1: continue
        keep = cl == bc_[0]; sf = sf[keep]; Fs = G.F[sf]; sv, Finv = np.unique(Fs, return_inverse=True); Fl = Finv.reshape(-1, 3)
        chi = len(sv) - len(np.unique(np.sort(np.r_[Fl[:, [0, 1]], Fl[:, [1, 2]], Fl[:, [2, 0]]], 1), axis=0)) + len(Fl)
        if chi == 1: disk = g; break
    if disk is None: WHY['no disk under the patch border'] += 1; continue
    try:
        bl = igl.boundary_loop(Fl); buv = igl.map_vertices_to_circle(G.V[sv], bl); UV = igl.harmonic(G.V[sv], Fl, bl, buv, 1)
    except Exception: WHY['flattening failed'] += 1; continue
    # cage patch vertices -> uv via their host faces (must be inside the disk)
    loc = -np.ones(G.NV if hasattr(G, 'NV') else len(G.V), int); loc[sv] = np.arange(len(sv)); fmap = -np.ones(len(G.F), int); fmap[sf] = np.arange(len(sf))
    if (fmap[fiv[border]] < 0).any(): WHY['host outside'] += 1; continue
    uv = {}
    for v in border: f = fmap[fiv[v]]; uv[v] = (bcv[v][:, None] * UV[Fl[f]]).sum(0)
    li = {v: i for i, v in enumerate(inner)}; M = sp.lil_matrix((len(inner), len(inner))); B = np.zeros((len(inner), 2))
    for v in inner:
        i = li[v]; nbr = A.indices[A.indptr[v]:A.indptr[v + 1]]; M[i, i] = len(nbr)
        for w in nbr:
            if w in li: M[i, li[w]] -= 1
            elif w in uv: B[i] += uv[w]
            else: M[i, i] -= 1                                            # (neighbour outside the patch region: should not happen for inner vertices)
    try: X = spl.spsolve(M.tocsc(), B)
    except Exception: continue
    X = np.atleast_2d(X)
    # map back: locate each uv in the flattened source triangles
    cen2 = UV[Fl].mean(1); kd2 = cKDTree(cen2); newf = []; newb = []; ok = True
    for x in X:
        cand = kd2.query(x, k=min(40, len(Fl)))[1]; found = False
        for f in np.atleast_1d(cand):
            a, b_, c_ = UV[Fl[f]]; Mt = np.array([b_ - a, c_ - a]).T
            if abs(np.linalg.det(Mt)) < 1e-14: continue
            l = np.linalg.solve(Mt, x - a); w = np.r_[1 - l.sum(), l]
            if w.min() > -1e-6: newf.append(sf[f]); newb.append(np.clip(w, 0, 1) / np.clip(w, 0, 1).sum()); found = True; break
        if not found: ok = False; break
    if not ok: WHY['uv outside disk'] += 1; continue
    newf = np.array(newf); newb = np.array(newb); P = V.copy(); P[inner] = (newb[:, :, None] * G.V[G.F[newf]]).sum(1)
    f0 = fiv.copy(); b0 = bcv.copy(); fiv[inner] = newf; bcv[inner] = newb
    fv1 = folded(P); n0 = int((folded(V)[rv]).sum()); n1 = int(fv1[rv].sum())
    cen = P[rv].mean(0); rad = np.linalg.norm(P[rv] - cen, axis=1).max() + 0.3; svv = np.array(kdS.query_ball_point(cen, rad), int); Tl = np.r_[Q[rq][:, [0, 1, 2]], Q[rq][:, [0, 2, 3]]]
    cov_ok = True
    if len(svv):
        db = np.sqrt(igl.point_mesh_squared_distance(G.V[svv], V, Tl)[0]); da = np.sqrt(igl.point_mesh_squared_distance(G.V[svv], P, Tl)[0]); cov_ok = not np.any((da > thr[svv]) & (da > db + 1e-5))
    if n1 < n0 and (cov_ok or os.environ.get('NOCOV')): V = P; acc += 1
    else: fiv = f0; bcv = b0; WHY['no fold gain' if n1 >= n0 else 'coverage'] += 1
print(dict(WHY)); print('patches accepted', acc, 'folded vertices now', int((folded(V) & ~pin).sum()))
z['V'] = V; z['tri'] = fiv; z['bc'] = bcv; np.savez_compressed(OUT, **z)
