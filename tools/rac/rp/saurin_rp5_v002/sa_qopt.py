# sa_qopt.py IN.npz OUT.npz : production quality + coverage optimisation of the full cage (order 236dddc §3-§9 "local edge sliding / quad-centroid shape
# improvement"). Topology unchanged (same face list for c1 / c2); every vertex stays ON the working source (AABB projection); tail module / pins fixed.
#   Per outer iteration: every source vertex is assigned to its nearest cage quad; per quad a SHAPE excess (aspect > A_T, min angle < 47, max angle > 133;
#   explicit tip exceptions = claw / thumb / toe caps) and a COVERAGE excess (source vertices of that quad farther than the zone threshold: 1.35 mm in the
#   identity zones, 2.7 mm elsewhere). Vertices touching an excess quad are optimised on independent sets: 30 candidate positions per vertex (tangential
#   ring, centroid rule, steps towards the worst uncovered source vertex), each projected onto the source and scored by the max excess of its incident
#   quads (coverage re-measured against the moved quads = conservative upper bound); the best strictly improving candidate is taken.
import sys, os, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; IT = int(os.environ.get('IT', 30)); A_T = float(os.environ.get('A_T', 3.7)); WC = float(os.environ.get('WC', 2.0))
TZN = float(os.environ.get('TZONE', 1.35)) / 10; TBD = float(os.environ.get('TBODY', 2.7)) / 10; CH = int(os.environ.get('CHUNK', 60)); MP = int(os.environ.get('MP', 160))
z = dict(np.load(IN)); Q = z['Q']; nb = int(z['n_body']); V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nq = len(Q)
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
ql = z['qlab'].astype(str); TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; tq = np.r_[np.arange(nq), np.arange(nq)]
lab = G.LAB; zone = np.isin(lab, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, TZN, TBD)
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); MQ = int(np.diff(VQ.indptr).max())
src = igl.AABB(); src.init(G.V, G.F); FNs = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0]))
def ptri(P, A, B, C):
    """vectorised squared distance point -> triangle (Ericson), broadcasting"""
    ab = B - A; ac = C - A; ap = P - A
    d1 = (ab * ap).sum(-1); d2 = (ac * ap).sum(-1); bp = P - B; d3 = (ab * bp).sum(-1); d4 = (ac * bp).sum(-1); cp = P - C; d5 = (ab * cp).sum(-1); d6 = (ac * cp).sum(-1)
    va = d3 * d6 - d5 * d4; vb = d5 * d2 - d1 * d6; vc = d1 * d4 - d3 * d2
    den = np.where(np.abs(va + vb + vc) < 1e-30, 1e-30, va + vb + vc); v = vb / den; w = vc / den; X = A + ab * v[..., None] + ac * w[..., None]
    t = np.clip(d1 / np.where(np.abs(d1 - d3) < 1e-30, 1e-30, d1 - d3), 0, 1); X = np.where(((vc <= 0) & (d1 >= 0) & (d3 <= 0))[..., None], A + t[..., None] * ab, X)
    t = np.clip(d2 / np.where(np.abs(d2 - d6) < 1e-30, 1e-30, d2 - d6), 0, 1); X = np.where(((vb <= 0) & (d2 >= 0) & (d6 <= 0))[..., None], A + t[..., None] * ac, X)
    t = np.clip((d4 - d3) / np.where(np.abs((d4 - d3) + (d5 - d6)) < 1e-30, 1e-30, (d4 - d3) + (d5 - d6)), 0, 1); X = np.where(((va <= 0) & (d4 - d3 >= 0) & (d5 - d6 >= 0))[..., None], B + t[..., None] * (C - B), X)
    X = np.where(((d1 <= 0) & (d2 <= 0))[..., None], A, X); X = np.where(((d3 >= 0) & (d4 <= d3))[..., None], B, X); X = np.where(((d6 >= 0) & (d5 <= d6))[..., None], C, X)
    return ((P - X) ** 2).sum(-1)
def shape_ex(P4):
    """P4 (..., 4, 3) quad corners -> shape excess, aspect, min / max angle"""
    sd = np.linalg.norm(np.roll(P4, -1, -2) - P4, axis=-1); asp = sd.max(-1) / np.maximum(sd.min(-1), 1e-9)
    u1 = np.roll(P4, 1, -2) - P4; u2 = np.roll(P4, -1, -2) - P4
    ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(-1) / (np.linalg.norm(u1, axis=-1) * np.linalg.norm(u2, axis=-1) + 1e-12), -1, 1)))
    ex = np.maximum(0, asp - A_T) + np.maximum(0, 47 - ang.min(-1)) / 10 + np.maximum(0, ang.max(-1) - 133) / 10
    return ex, asp, ang.min(-1), ang.max(-1)
def report(tag, d, asp, amin, amax):
    print(tag, 'T1 max body %.2f zone %.2f mm | over thr %d | aspect>4 non-tip %d (all %d) | angle out %d | min edge %.3f mm' % (
        d[~zone].max() * 10, d[zone].max() * 10, int((d > thr).sum()), int(((asp > 4) & ~TIP).sum()), int((asp > 4).sum()), int(((amin < 45) | (amax > 135)).sum()),
        np.linalg.norm(np.roll(V[Q], -1, 1) - V[Q], axis=2).min() * 10), flush=True)
rng = np.random.default_rng(0)
for it in range(IT):
    cg = igl.AABB(); cg.init(V, T); d2, ti, _ = cg.squared_distance(V, T, G.V); d = np.sqrt(d2); sq = tq[ti]
    qex, asp, amin, amax = shape_ex(V[Q]); qex[TIP] = 0
    cov = np.zeros(nq); np.maximum.at(cov, sq, np.maximum(0, d - thr) / thr); qs = qex + WC * cov
    report('it %d' % it, d, asp, amin, amax)
    vs = np.asarray(VQ @ sp.diags(qs) .max(1).todense()).ravel() if False else np.zeros(nv)
    np.maximum.at(vs, Q.ravel(), np.repeat(qs, 4)); act = np.nonzero((vs > 1e-6) & ~pin)[0]
    if not len(act): break
    # samples per quad (sorted by excess so the worst are kept when capping)
    order = np.lexsort((-d / thr, sq)); sq_s = sq[order]; qstart = np.searchsorted(sq_s, np.arange(nq + 1))
    act = act[np.argsort(-vs[act])]; done = np.zeros(nv, bool); nacc = 0; Vprev = V.copy()
    while True:
        used = np.zeros(nq, bool); batch = []
        for v in act:
            if done[v]: continue
            qv = VQ.indices[VQ.indptr[v]:VQ.indptr[v + 1]]
            if used[qv].any(): continue
            used[qv] = True; batch.append(v); done[v] = True
        if not batch: break
        batch = np.array(batch)
        for c0 in range(0, len(batch), CH):
            bv = batch[c0:c0 + CH]; n = len(bv)
            QI = np.full((n, MQ), -1); SI = np.full((n, MP), -1)
            for i, v in enumerate(bv):
                qv = VQ.indices[VQ.indptr[v]:VQ.indptr[v + 1]]; QI[i, :len(qv)] = qv
                ss = np.concatenate([order[qstart[q]:qstart[q + 1]][:MP // 3] for q in qv]); ss = ss[np.argsort(-d[ss] / thr[ss])][:MP]; SI[i, :len(ss)] = ss
            qm = QI >= 0; sm = SI >= 0; QIc = np.where(qm, QI, 0); SIc = np.where(sm, SI, 0)
            P0 = V[bv]; N = np.nan_to_num(igl.per_vertex_normals(V, T)[bv]) if c0 == -1 else None
            # tangent frame from incident quad normals
            Qc = V[Q[QIc]]; nrm = np.cross(Qc[:, :, 2] - Qc[:, :, 0], Qc[:, :, 3] - Qc[:, :, 1]); nrm = (nrm * qm[..., None]).sum(1); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
            t1 = np.cross(nrm, [0.37, 0.59, 0.71]); t1 /= np.linalg.norm(t1, axis=1, keepdims=True) + 1e-12; t2 = np.cross(nrm, t1)
            el = np.linalg.norm(np.roll(Qc, -1, 2) - Qc, axis=3); el = (el.mean(2) * qm).sum(1) / qm.sum(1)
            cands = [P0]
            for s in (0.06, 0.16, 0.32):
                for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                    cands.append(P0 + s * el[:, None] * (np.cos(a) * t1 + np.sin(a) * t2))
            cen = (Qc.mean(2) * qm[..., None]).sum(1) / qm.sum(1)[:, None]; cands.append(P0 + 0.5 * (cen - P0))
            for j in (0, 1, 2):                                                   # towards the worst uncovered source vertices: full 3-D (into pockets / creases) and tangential
                w = G.V[SIc[:, j]]; dw = w - P0; dt = dw - (dw * nrm).sum(1)[:, None] * nrm
                for f in (0.35, 0.7, 1.0): cands.append(P0 + f * dw)
                cands.append(P0 + 0.5 * dt)
            C_ = np.stack(cands, 1); K = C_.shape[1]
            _, fq_, cp = src.squared_distance(G.V, G.F, C_.reshape(-1, 3)); nr_ = np.repeat(nrm, K, 0)
            wrong = (FNs[fq_] * nr_).sum(1) < 0.2                                           # wrong sheet (neighbouring digit / opposite wall): re-query from 1 mm inside
            if wrong.any(): _, _, cp2 = src.squared_distance(G.V, G.F, C_.reshape(-1, 3)[wrong] - 0.1 * nr_[wrong]); cp[wrong] = cp2
            cp = cp.reshape(n, K, 3)
            okj = np.linalg.norm(cp - C_, axis=2) < 0.5 * el[:, None]; cp[~okj] = P0[:, None].repeat(K, 1)[~okj]
            # incident quad corners with the vertex replaced by each candidate
            QV = Q[QIc]; isv = QV == bv[:, None, None]                        # (n, MQ, 4)
            P4 = np.where(isv[:, None, :, :, None], cp[:, :, None, None, :], V[QV][:, None])   # (n, K, MQ, 4, 3)
            ex, _, _, _ = shape_ex(P4); ex = np.where(TIP[QIc][:, None, :], 0, ex)
            # coverage of each local sample against the 2 triangles of every incident quad
            A_ = P4[:, :, :, [0, 0]]; B_ = P4[:, :, :, [1, 2]]; C3 = P4[:, :, :, [2, 3]]       # (n, K, MQ, 2, 3)
            A_ = A_.reshape(n, K, 1, 2 * MQ, 3); B_ = B_.reshape(n, K, 1, 2 * MQ, 3); C3 = C3.reshape(n, K, 1, 2 * MQ, 3)
            Ps = G.V[SIc][:, None, :, None, :]                                    # (n, 1, MP, 1, 3)
            dd = ptri(Ps, A_, B_, C3); tm = np.repeat(qm, 2, 1)[:, None, None, :]; dd = np.where(tm, dd, 1e9).min(3)   # (n, K, MP)
            ce = np.where(sm[:, None, :], np.maximum(0, np.sqrt(dd) - thr[SIc][:, None, :]) / thr[SIc][:, None, :], 0).max(2)   # (n, K)
            exm = np.where(qm[:, None, :], ex, 0); sc = exm.max(2) + 0.25 * exm.sum(2) + WC * ce                 # (n, K)
            best = sc.argmin(1); imp = sc[np.arange(n), best] < sc[:, 0] - 1e-4
            V[bv[imp]] = cp[np.arange(n), best][imp]; nacc += int(imp.sum())
    # rollback guard: any source vertex that ends above its threshold AND worse than before -> revert the vertices of its nearest quad (repeat)
    for _g in range(4):
        cg2 = igl.AABB(); cg2.init(V, T); dn2, ti2, _ = cg2.squared_distance(V, T, G.V); dn = np.sqrt(dn2)
        viol = np.nonzero((dn > thr) & (dn > d + 1e-5))[0]
        if not len(viol): break
        rv = np.unique(Q[tq[ti2[viol]]].ravel()); rv = rv[np.linalg.norm(V[rv] - Vprev[rv], axis=1) > 0]
        if not len(rv): break
        V[rv] = Vprev[rv]
    print('   active', len(act), 'moved', nacc, 'rollback passes', _g, flush=True)
    if it % 4 == 3:                                                           # checkpoint (the cloud workspace can restart)
        fi2, bc2, _ = G.embed(V); zz = dict(z); zz['V'] = V; zz['tri'] = fi2; zz['bc'] = bc2; np.savez_compressed(OUT, **zz); print('   checkpoint', it, flush=True)
    if nacc == 0: break
cg = igl.AABB(); cg.init(V, T); d = np.sqrt(cg.squared_distance(V, T, G.V)[0]); qex, asp, amin, amax = shape_ex(V[Q]); report('final', d, asp, amin, amax)
fi2, bc2, dist = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2
np.savez_compressed(OUT, **z); print('saved', OUT, 'off-surface max %.4f mm' % (dist.max() * 10))
