# sa_thumbfix.py DESIGN_FIXED.pkl IN.npz OUT.npz : re-place the thumb tubes after the sa_design thumb-correspondence fix (the coarse face list is unchanged,
#   only the sense of the thumb ring corners r1/r2 1<->3 was corrected, so every fine index is unchanged). The fine thumb vertices (quads whose coarse
#   home is a thumb / thumb-cap quad, hole ring kept fixed) are re-initialised from the corrected coarse cage (3 Catmull-Clark levels), projected onto
#   the working source restricted to the hand of that side, and relaxed (tangential umbrella + reprojection); sa_qopt / sa_gopt then finish the region.
import sys, os, pickle, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
DS, IN, OUT = sys.argv[1:4]; d = pickle.load(open(DS, 'rb')); C = np.array(d['C']); Qc = np.array(d['Q'])
fi, bc, _ = G.embed(C); C0 = (bc[:, :, None] * G.V[G.F[fi]]).sum(1)
Vf, Qf, src = C0.copy(), Qc.copy(), np.arange(len(Qc))
for _ in range(3): Vf, Qf, src = CC.cc(Vf, Qf, src)
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nvf = len(Vf)
ql = np.array(d['qlab']); thq = np.isin(ql[src], ['thumb', 'thumb_cap'])
tv = np.zeros(nvf, bool); tv[Qf[thq].ravel()] = True; ov = np.zeros(nvf, bool); ov[Qf[~thq].ravel()] = True; mov = np.nonzero(tv & ~ov)[0]
pin = np.zeros(nv, bool); pin[z['pinned']] = True; mov = mov[~pin[mov]]
print('thumb vertices re-placed', len(mov), flush=True)
for s, sg in (('xpos', 1), ('xneg', -1)):
    ms = mov[np.sign(Vf[mov, 0]) == sg]; fm = np.isin(G.LAB[G.F[:, 0]], ['hand_' + s]); FF = G.F[fm]
    _, _, cp = igl.point_mesh_squared_distance(Vf[ms], G.V, FF); V[ms] = cp
    T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
    A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); deg = np.asarray(A.sum(1)).ravel()
    for it in range(30):
        N = np.nan_to_num(igl.per_vertex_normals(V, T)); L = (A @ V) / deg[:, None] - V; L -= (L * N).sum(1)[:, None] * N
        P = V[ms] + 0.4 * L[ms]; _, _, cp = igl.point_mesh_squared_distance(P, G.V, FF); V[ms] = cp
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z)
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); ql2 = z['qlab'].astype(str); m = np.isin(ql2, ['thumb', 'thumb_cap']); P4 = V[Q[m]]
n = np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]); _, f_, _ = igl.point_mesh_squared_distance(P4.mean(1), G.V, G.F); print('thumb quads inverted vs source', int(((n * FN[f_]).sum(1) < 0).sum()), '/', int(m.sum()))
