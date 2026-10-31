# sa_ccage.py DESIGN.pkl OUT.npz : RP5 Saurin production cage from the AUTHORED coarse cage (sa_design.py) -- route without surface path routing:
#   1. coarse corners snapped onto SA_RP5_WORK_v001 (SA-M188);  2. three Catmull-Clark levels (topology = the authored coarse cage x 64; every authored ring /
#   column becomes a fine edge loop; the 16-edge tail-root hole becomes exactly the 128-vertex root ring of the accepted tail module);
#   3. projection onto the working surface RESTRICTED (when the free closest point leaves the neighbourhood) to the source region of the vertex's own coarse quad and its neighbours (nearest-coarse-quad partition)
#      -> no jumps between fingers / toes / lips;  4. relaxation: 60 x (tangential umbrella step 0.45 + coverage pull of uncovered source samples + reprojection); pinned: tail ring (module),
#      claw / toe / thumb tips, rostrum tip, eye floors;  5. the accepted tail module (unchanged) attached on its root ring; barycentric embedding on the
#      canonical base face list -> exact SA-M188 / SA-F188 realization (one topology).
import sys, os, pickle, json, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa_geo as GEO
V, F = GEO.V, GEO.F
def cc(Vc, Q, qsrc, bnd_pin=None):
    """one Catmull-Clark step on a quad mesh with boundary; returns V, Q, qsrc (coarse quad id per face)"""
    nv = len(Vc); nq = len(Q)
    E = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); Eu, inv = np.unique(E, axis=0, return_inverse=True); inv = inv.reshape(nq, 4)
    ne = len(Eu); efc = np.bincount(inv.ravel(), minlength=ne); fp = Vc[Q].mean(1)
    esum = np.zeros((ne, 3)); np.add.at(esum, inv.ravel(), np.repeat(fp, 4, 0))
    ep = np.where((efc == 2)[:, None], (Vc[Eu[:, 0]] + Vc[Eu[:, 1]] + esum) / 4.0, 0.5 * (Vc[Eu[:, 0]] + Vc[Eu[:, 1]]))
    bE = Eu[efc == 1]; isb = np.zeros(nv, bool); isb[bE.ravel()] = True
    # interior vertex rule
    val = np.zeros(nv); np.add.at(val, Eu.ravel(), 1); Fs = np.zeros((nv, 3)); fc = np.zeros(nv); np.add.at(Fs, Q.ravel(), np.repeat(fp, 4, 0)); np.add.at(fc, Q.ravel(), 1)
    Rs = np.zeros((nv, 3)); mid = 0.5 * (Vc[Eu[:, 0]] + Vc[Eu[:, 1]]); np.add.at(Rs, Eu[:, 0], mid); np.add.at(Rs, Eu[:, 1], mid)
    n = val; Vn = (Fs / np.maximum(fc, 1)[:, None] + 2 * Rs / np.maximum(n, 1)[:, None] + (n - 3)[:, None] * Vc) / np.maximum(n, 1)[:, None]
    nbsum = np.zeros((nv, 3)); np.add.at(nbsum, bE[:, 0], Vc[bE[:, 1]]); np.add.at(nbsum, bE[:, 1], Vc[bE[:, 0]])
    Vn[isb] = (6 * Vc[isb] + nbsum[isb]) / 8.0
    Vout = np.vstack([Vn, ep, fp]); eo = nv; fo = nv + ne; Qn = []; src = []
    for k in range(4):
        Qn.append(np.c_[Q[:, k], eo + inv[:, k], fo + np.arange(nq), eo + inv[:, (k - 1) % 4]]); src.append(qsrc)
    return Vout, np.vstack(Qn), np.concatenate(src)
if __name__ == '__main__':
    d = pickle.load(open(sys.argv[1], 'rb')); C = np.array(d['C']); Q = np.array(d['Q']); nm = d['name']; ix = {x: i for i, x in enumerate(nm)}
    fi, bc, _ = GEO.embed(C); C0 = (bc[:, :, None] * V[F[fi]]).sum(1)
    # nearest-coarse-quad partition of the source (coarse quads = 2 triangles on the snapped corners)
    T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; _, ti, _ = igl.point_mesh_squared_distance(V, C0, T); vq = ti % len(Q); fq = vq[F[:, 0]]
    # coarse quad adjacency (shared edge or corner)
    nq = len(Q); A = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(len(C), nq)).tocsr(); QQ = (A.T @ A).tocsr()
    Vf, Qf, src = C0.copy(), Q.copy(), np.arange(nq)
    for _ in range(3): Vf, Qf, src = cc(Vf, Qf, src)
    nvf = len(Vf); print('CC x3:', nvf, 'V', len(Qf), 'Q', flush=True)
    # vertex -> coarse quads
    VQ = sp.coo_matrix((np.ones(4 * len(Qf)), (Qf.ravel(), np.repeat(src, 4))), shape=(nvf, nq)).tocsr()
    home = np.asarray(VQ.argmax(1)).ravel()
    # tail-root ring: boundary loop of the fine mesh <-> module ring 0 (128), aligned on corner P0_8 = module index 0
    bl = np.asarray(igl.boundary_loop(Qf[:, [0, 1, 2]] if False else np.r_[Qf[:, [0, 1, 2]], Qf[:, [0, 2, 3]]]))
    TM = np.load(GEO.W + '/tail/SA_tail_module.npz'); TR0 = TM['V'][:128]
    assert len(bl) == 128, len(bl)
    k0 = int(np.nonzero(bl == ix['P0_8'])[0][0]); bl = np.roll(bl, -k0)
    if np.linalg.norm(Vf[bl[1]] - TR0[1]) > np.linalg.norm(Vf[bl[1]] - TR0[127]): bl = np.r_[bl[:1], bl[1:][::-1]]
    Vf[bl] = TR0
    pin = np.zeros(nvf, bool); pin[bl] = True; target = {}
    for k, p in d['pins'].items():
        j = int(np.argmin(np.linalg.norm(Vf - p, axis=1))); target[j] = np.asarray(p); pin[j] = True
    # restricted projection
    groups = {}
    for v in range(nvf): groups.setdefault(home[v], []).append(v)
    sub_cache = {}
    nbq = {q: set(QQ[q].indices.tolist()) for q in range(nq)}
    def project(P):
        """closest point on the full surface; vertices whose hit lies outside the source region of their own coarse quad's neighbourhood are re-projected
        onto that region only (no jumps across finger / toe / lip gaps)"""
        _, fi_, cp = igl.point_mesh_squared_distance(P, V, F); out = cp
        bad = np.nonzero([fq[fi_[v]] not in nbq[home[v]] for v in range(len(P))])[0]
        for q in np.unique(home[bad]):
            vs = bad[home[bad] == q]
            if q not in sub_cache: sub_cache[q] = np.nonzero(np.isin(fq, list(nbq[q])))[0]
            _, _, c2 = igl.point_mesh_squared_distance(P[vs], V, F[sub_cache[q]]); out[vs] = c2
        return out
    Vf[~pin] = project(Vf)[~pin]
    for j, p in target.items(): Vf[j] = p
    Eq = np.unique(np.sort(np.r_[Qf[:, [0, 1]], Qf[:, [1, 2]], Qf[:, [2, 3]], Qf[:, [3, 0]]], 1), axis=0)
    Ad = sp.coo_matrix((np.ones(2 * len(Eq)), (np.r_[Eq[:, 0], Eq[:, 1]], np.r_[Eq[:, 1], Eq[:, 0]])), shape=(nvf, nvf)).tocsr(); deg = np.asarray(Ad.sum(1)).ravel()
    TT = np.r_[Qf[:, [0, 1, 2]], Qf[:, [0, 2, 3]]]
    TMV = TM['V']; _mm = np.r_[bl, nvf + np.arange(len(TMV) - 128)]; _mq = _mm[TM['Q']]; TMT = np.r_[_mq[:, [0, 1, 2]], _mq[:, [0, 2, 3]]]; rng = np.random.default_rng(0); samp = rng.choice(len(V), 250000, replace=False)
    for it in range(int(os.environ.get('RELAX', 60))):
        # data term (coverage): source samples farther than 0.6 mm from the cage pull the vertices of their closest cage triangle towards them
        VA = np.vstack([Vf, TMV[128:]]); TA = np.r_[TT, TMT]                           # body + the (fixed) tail module: tail samples are covered by the module
        d2, ti_, cp_ = igl.point_mesh_squared_distance(V[samp], VA, TA); far = (np.sqrt(d2) > 0.06) & (ti_ < len(TT))
        acc = np.zeros_like(Vf); cnt = np.zeros(nvf)
        if far.any():
            tv = TT[ti_[far]]; dv = V[samp[far]] - cp_[far]
            for k in range(3): np.add.at(acc, tv[:, k], dv); np.add.at(cnt, tv[:, k], 1)
        D_ = np.where(cnt[:, None] > 0, acc / np.maximum(cnt, 1)[:, None], 0)
        N = np.nan_to_num(igl.per_vertex_normals(Vf, TT)); L = (Ad @ Vf) / deg[:, None] - Vf; L -= (L * N).sum(1)[:, None] * N
        wl = np.where(cnt > 0, 0.12, 0.45)[:, None]                               # pulled vertices smooth less (lets the cage enter crevices)
        Vt = Vf + wl * L + 0.8 * D_; Vt = np.where(np.isfinite(Vt), Vt, Vf); Vt = project(Vt); ok = ~pin & np.isfinite(Vt).all(1); Vf[ok] = Vt[ok]
        if it % 10 == 0: print('relax', it, 'far samples', int(far.sum()), 'max %.1f mm' % (np.sqrt(d2[ti_ < len(TT)].max()) * 10), flush=True)
    # attach the accepted tail module (unchanged): module vertex i of ring 0 -> fine boundary vertex bl[i]
    mV, mQ = TM['V'], TM['Q']; mmap = np.r_[bl, nvf + np.arange(len(mV) - 128)]
    Vall = np.vstack([Vf, mV[128:]]); Qall = np.vstack([Qf, mmap[mQ]]); qlab = np.r_[np.array(d['qlab'])[src], np.array(['tail'] * len(mQ))]
    qcoarse = np.r_[src, -1 - np.zeros(len(mQ), int)]
    fi, bc, dist = GEO.embed(Vall)
    print('final', len(Vall), 'V', len(Qall), 'Q; max off-surface %.3f mm' % (dist.max() * 10), flush=True)
    np.savez_compressed(sys.argv[2], V=Vall, Q=Qall, tri=fi, bc=bc, qlab=qlab, qcoarse=qcoarse, n_body=nvf, tail_ring=bl, pinned=np.nonzero(pin)[0])
