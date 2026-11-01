# sa_untangle.py IN.npz OUT.npz : untangling of folded / concave quads (dart or bow-tie corners) -- order 236dddc §9 hard stop "no pathological shapes".
#   Tangled clusters (signed corner sine < 0.05 w.r.t. the quad normal, tip caps excepted) + RING quad rings form a patch; its interior is re-placed by a
#   uniform harmonic (Tutte-like) solve with the patch border fixed (fold-free on a disk), then projected onto the working source with a SHEET-CONSISTENT
#   closest point (only source faces whose normal agrees with the harmonic surface normal, dot > 0.3, within 2.5 cm -> no snapping onto the neighbouring
#   digit / the opposite palm or pocket wall). Accepted per patch only if folded quads drop, no quad exceeds aspect 4 that did not before, and no source
#   vertex near the patch ends above its zone threshold worse than before. Topology unchanged.
import sys, os, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
IN, OUT = sys.argv[1:3]; RING = int(os.environ.get('RING', 3))
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nq = len(Q); nb = int(z['n_body']); ql = z['qlab'].astype(str)
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True; TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.13, 0.27)
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); FC = G.V[G.F].mean(1); kdF = cKDTree(FC); kdS = cKDTree(G.V)
def sgn(P, qs):
    P4 = P[Q[qs]]; n = np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12; u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4
    return ((np.cross(u2, u1) * n[:, None]).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12)).min(1)
def aspq(P, qs): P4 = P[Q[qs]]; sd = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); return sd.max(1) / np.maximum(sd.min(1), 1e-9)
allq = np.arange(nq); s0 = sgn(V, allq); bad = (s0 < 0.05) & ~TIP
bi = np.nonzero(bad)[0]; nc, lab = connected_components(QQ[bi][:, bi], directed=False); print('folded quads', len(bi), 'clusters', nc, flush=True)
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; acc = 0; fixed_total = 0
for c in range(nc):
    core = bi[lab == c]; reg = np.zeros(nq, bool); reg[core] = True
    for _ in range(RING): reg = (QQ @ reg.astype(float)) > 0
    reg &= ~(Q >= nb).any(1); rq = np.nonzero(reg)[0]
    rv = np.unique(Q[rq]); outside = np.zeros(nv, bool); outside[Q[~reg].ravel()] = True
    inner = rv[~outside[rv] & ~pin[rv]]
    if len(inner) < 1: continue
    # harmonic interior, border fixed
    loc = -np.ones(nv, int); loc[inner] = np.arange(len(inner)); Ai = A[inner]; deg = np.asarray(Ai.sum(1)).ravel()
    L = sp.diags(deg) - Ai[:, inner]; Bm = Ai.tolil(); Bm[:, inner] = 0; rhs = Bm.tocsr() @ V
    try: X = np.stack([spl.spsolve(L.tocsc(), rhs[:, k]) for k in range(3)], 1)
    except Exception: continue
    P = V.copy(); P[inner] = X
    Nh = np.nan_to_num(igl.per_vertex_normals(P, T))[inner]
    # sheet-consistent projection
    newp = X.copy()
    for i, (x, nrm) in enumerate(zip(X, Nh)):
        cand = np.array(kdF.query_ball_point(x, 2.5), int)
        if not len(cand): continue
        cand = cand[FN[cand] @ nrm > 0.3]
        if not len(cand): continue
        _, _, cp = igl.point_mesh_squared_distance(x[None], G.V, G.F[cand]); newp[i] = cp[0]
    P[inner] = newp
    s1 = sgn(P, rq); a0 = aspq(V, rq); a1 = aspq(P, rq)
    n0 = int(((s0[rq] < 0.05) & ~TIP[rq]).sum()); n1 = int(((s1 < 0.05) & ~TIP[rq]).sum())
    if os.environ.get('DBG') and c < 25: print(c, 'core', len(core), 'inner', len(inner), 'folded', n0, '->', n1, 'new asp>4', int(np.sum((a1 > 4) & (a0 <= 4) & ~TIP[rq])), flush=True)
    if n1 >= n0 or (not os.environ.get('ALLOWASP') and np.any((a1 > 4) & (a0 <= 4) & ~TIP[rq])): continue
    cen = P[rv].mean(0); rad = np.linalg.norm(P[rv] - cen, axis=1).max() + 0.3; sv = np.array(kdS.query_ball_point(cen, rad), int)
    Tl = np.r_[Q[rq][:, [0, 1, 2]], Q[rq][:, [0, 2, 3]]]
    if len(sv):
        db = np.sqrt(igl.point_mesh_squared_distance(G.V[sv], V, Tl)[0]); da = np.sqrt(igl.point_mesh_squared_distance(G.V[sv], P, Tl)[0])
        if np.any((da > thr[sv]) & (da > db + 1e-5)):
            if os.environ.get('DBG'): print(c, 'coverage reject', float(da.max() * 10), flush=True)
            continue
    V = P; s0[rq] = s1; acc += 1; fixed_total += n0 - n1
print('patches accepted', acc, 'folded quads removed', fixed_total, '-> remaining', int(((sgn(V, allq) < 0.05) & ~TIP).sum()))
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z)
