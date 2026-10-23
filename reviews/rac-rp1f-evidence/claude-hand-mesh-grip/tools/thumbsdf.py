# thumbsdf.py (python) -- IN.npz OUT.npz [params.json]
# Rebuild each thumb tip as a finger-like tip: the thumb solid is kept up to t=TD (IP joint -> claw apex axis), and
# the same side's index fingertip solid (pad + claw, index t >= TG) is grafted on, uniformly scaled to the thumb
# section (smooth union, implicit). The target surface is extracted by marching cubes, clipped at t=TCUT, and the
# thumb's own patch beyond TCUT (same quad topology) is draped onto it (authalic init, fold-guarded relaxation,
# claw apex pinned). The cut loop is restored and the correction blended over BAND. New keratin = vertices on the
# grafted claw. Vertices only.
import sys, json, pickle, numpy as np, time
sys.path.insert(0, '/tmp/claude-0/hand/tools')
import drape as DR
from drape import drape, loops_of, clip_plane
import scipy.sparse as sp, igl
from skimage.measure import marching_cubes
from scipy.sparse.csgraph import connected_components, dijkstra
a = sys.argv[1:]; inf, outf = a[:2]; prm = json.load(open(a[2])) if len(a) > 2 else {}
TCUT = prm.get('tcut', 0.12); TPL = prm.get('template', {'L': 'A_L20', 'R': 'A_R21'}); ITERS = prm.get('iters', 800)
TD = prm.get('td', {'L': 0.42, 'R': 0.42}); TG = prm.get('tg', {'L': 0.35, 'R': 0.35}); KS = prm.get('smooth_k_cm', 0.3)
RES = prm.get('res_cm', 0.04); BAND = prm.get('band_cm', 0.6); SIDES = prm.get('sides', 'LR'); SCL = prm.get('scale', {})
DR.AUTH_ITERS = prm.get('auth_iters', 50)
RG = '/tmp/claude-0/hand/rig_c3'
RD = pickle.load(open(RG + '/rig_data.pkl', 'rb')); Dn = pickle.load(open(RG + '/rig_np.pkl', 'rb')); dj = json.load(open('/tmp/claude-0/hand/digits.json'))
z = np.load(inf); Vall = z['V'].astype(np.float64); out = Vall.copy(); report = {}
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20', 'A_Lthumb'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24', 'A_Rthumb']}
Fl = np.array([1, -1, 1.0]); log = lambda *x: print(*x, flush=True)

def dframe(P, own, ker, i, key, S):
    j2 = np.array(RD[S]['joints'][key]['j2']); km = ker & (own == i)
    kv = np.where(km)[0]; ap = kv[np.argmin(np.linalg.norm(P[kv] - np.array(dj[key]['claw_tip']), axis=1))]
    ea = P[ap] - j2; L = np.linalg.norm(ea); ea /= L
    kc = P[km].mean(0) - j2; ed = kc - (kc @ ea) * ea; ed /= np.linalg.norm(ed); el = np.cross(ea, ed)
    return dict(o=j2, ea=ea, ed=ed, el=el, L=L, ap=ap, R=np.c_[ea, ed, el])

def tri_of(Q, m): QQ = Q[m]; return np.vstack([QQ[:, [0, 1, 2]], QQ[:, [0, 2, 3]]])

def section(P, f, sel, t0, w=0.03):
    Y = P[sel] - f['o']; t = Y @ f['ea'] / f['L']; m = np.abs(t - t0) < w; Z = Y[m]
    c = Z.mean(0); dd = (Z - c) @ f['ed']; ll = (Z - c) @ f['el']
    return f['o'] + c, 0.5 * (np.percentile(dd, 97) - np.percentile(dd, 3)), 0.5 * (np.percentile(ll, 97) - np.percentile(ll, 3))

def smin(a_, b_, k):
    h = np.clip(0.5 + 0.5 * (b_ - a_) / k, 0, 1); return b_ * (1 - h) + a_ * h - k * h * (1 - h)

for S in SIDES:
    t0 = time.time()
    vid = RD[S]['vid']; own = RD[S]['own']; ker = RD[S]['ker']; P = Vall[vid] * Fl; Q = Dn[S]['Q']; n = len(P)
    th = digs[S].index('A_%sthumb' % S); ix = digs[S].index(TPL[S])
    ft = dframe(P, own, ker, th, 'A_%sthumb' % S, S); fi = dframe(P, own, ker, ix, TPL[S], S)
    ct, hd_t, hl_t = section(P, ft, own == th, TD[S]); ci, hd_i, hl_i = section(P, fi, own == ix, TG[S])
    sg = SCL.get(S, 0.5 * (hd_t / hd_i + hl_t / hl_i))
    # graft transform: index point p -> ct + sg * Rt Ri^T (p - ci)
    M = ft['R'] @ fi['R'].T
    def to_thumb(p): return ct + sg * (p - ci) @ M.T
    def to_index(x): return ci + ((x - ct) / sg) @ M
    # meshes for SDF
    T_th = tri_of(Q, (own[Q] >= 0).any(1) | (own[Q] < 0).any(1))     # whole crop (closed except the forearm cut)
    T_ix = tri_of(Q, (own[Q] == ix).all(1))
    apT = to_thumb(P[fi['ap']]); tq = ((P - ft['o']) @ ft['ea']) / ft['L']
    if prm.get('reuse_target'):
        _t = np.load(prm['reuse_target'] % S); X = _t['X']; F = _t['F']; lps = loops_of(F); rloop = np.array(max(lps, key=len))
    else:
        # grid
        tq = ((P - ft['o']) @ ft['ea']) / ft['L']
        pts = np.vstack([P[(own == th) & (tq > TCUT - 0.08)], to_thumb(P[(own == ix) & ((((P - fi['o']) @ fi['ea']) / fi['L']) > TG[S] - 0.1)])])
        lo = pts.min(0) - 0.4; hi = pts.max(0) + 0.4; nn = np.ceil((hi - lo) / RES).astype(int) + 1
        gx = [lo[d] + RES * np.arange(nn[d]) for d in range(3)]
        G = np.stack(np.meshgrid(*gx, indexing='ij'), -1).reshape(-1, 3)
        log(S, 'grid', nn.tolist(), len(G), 'scale %.3f' % sg)
        # thumb SDF (only near the thumb: elsewhere +big), truncated at t<=TD
        inb = ((P > lo - 1.5) & (P < hi + 1.5)).all(1); T_th = T_th[inb[T_th].all(1)]
        s_th, _, _, _ = igl.signed_distance(G, P, T_th, sign_type=igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
        tg_ = ((G - ft['o']) @ ft['ea']) / ft['L']
        s1 = s_th
        # graft SDF in index space (only index triangles; scaled distance), truncated at index t >= TG - 0.12
        Gi = to_index(G); s_ix, _, _, _ = igl.signed_distance(Gi, P, T_ix, sign_type=igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
        ti_ = ((Gi - fi['o']) @ fi['ea']) / fi['L']
        s2 = np.maximum(s_ix * sg, (TG[S] - 0.3 - ti_) * fi['L'] * sg)
        # keep the rest of the hand from the thumb SDF only where it belongs to the thumb region: points whose nearest crop
        # vertex is not a thumb vertex are excluded (outside), so neighbouring fingers do not enter the target
        from scipy.spatial import cKDTree
        _, nv = cKDTree(P).query(G); s1 = np.where(own[nv] == th, s1, np.maximum(s1, 0.05))
        MW = prm.get('morph_w', 0.12)
        beta = np.clip((tg_ - (TD[S] - MW)) / (2 * MW), 0, 1); beta = beta * beta * (3 - 2 * beta)
        sdf = ((1 - beta) * s1 + beta * s2).reshape(nn)
        vv, ff, _, _ = marching_cubes(sdf, 0.0, spacing=(RES, RES, RES)); vv = vv + lo; ff = ff[:, ::-1]
        # orient outward: check with SDF gradient sign via a centroid test
        # keep the component nearest the grafted apex
        apT = to_thumb(P[fi['ap']])
        Ec = np.vstack([ff[:, [0, 1]], ff[:, [1, 2]], ff[:, [2, 0]]]); A = sp.coo_matrix((np.ones(len(Ec)), (Ec[:, 0], Ec[:, 1])), shape=(len(vv), len(vv)))
        _, lab = connected_components(A, directed=False); seed = int(np.argmin(np.linalg.norm(vv - apT, axis=1)))
        ff = ff[lab[ff[:, 0]] == lab[seed]]
        # clip at TCUT - 0.06 (keep distal)
        p0 = ft['o'] + (TCUT - 0.06) * ft['L'] * ft['ea']
        X, F = clip_plane(vv, ff, p0, ft['ea'])
        _, lab2 = connected_components(sp.coo_matrix((np.ones(3 * len(F)), (np.r_[F[:, 0], F[:, 1], F[:, 2]], np.r_[F[:, 1], F[:, 2], F[:, 0]])), shape=(len(X), len(X))), directed=False)
        s2i = int(np.argmin(np.linalg.norm(X - apT, axis=1))); F = F[lab2[F[:, 0]] == lab2[s2i]]
        u = np.unique(F); mp = -np.ones(len(X), int); mp[u] = np.arange(len(u)); X = X[u]; F = mp[F]
        # light Taubin smoothing of the target (voxel noise), boundary fixed
        lps = loops_of(F); log(S, 'target loops', [len(l) for l in lps]); rloop = np.array(max(lps, key=len))
        Et = np.unique(np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1), axis=0)
        At = sp.coo_matrix((np.ones(2 * len(Et)), (np.r_[Et[:, 0], Et[:, 1]], np.r_[Et[:, 1], Et[:, 0]])), shape=(len(X), len(X))).tocsr()
        dg = np.asarray(At.sum(1)).ravel(); isb = np.zeros(len(X), bool); isb[np.concatenate(lps)] = True
        for it in range(prm.get('tgt_smooth', 6)):
            for fct in (0.5, -0.53):
                Lp = At @ X / dg[:, None] - X; Lp[isb] = 0; X = X + fct * Lp
    np.savez(outf.replace('.npz', '_tgt_%s.npz' % S), X=X, F=F)
    if prm.get('target_only'): log(S, 'target saved'); continue
    # thumb patch
    qp = (own[Q] == th).all(1) & (tq[Q].min(1) > TCUT)
    QP = Q[qp]; up = np.unique(QP); mq = -np.ones(n, int); mq[up] = np.arange(len(up)); Ql = mq[QP]
    lp = loops_of(Ql); assert len(lp) == 1, [len(l) for l in lp]; bl = np.array(lp[0]); Pl = P[up].copy(); bp = Pl[bl]
    gap = np.sqrt(igl.point_mesh_squared_distance(bp, X, F)[0])
    log(S, 'patch verts', len(up), 'target verts', len(X), 'cut gap mm max %.2f med %.2f' % (gap.max() * 10, np.median(gap) * 10))
    apl = int(mq[ft['ap']]); apTt = X[np.argmin(np.linalg.norm(X - apT, axis=1))]
    X3, P2, U = drape(Pl, Ql, bl, bp, X, F, rloop, pins=[(None, apTt)], hard_pins=[], iters=ITERS, init='authalic', log=log, mix=0.2, shape=0.5)
    # restore the cut loop; blend the correction over BAND
    dB = bp - X3[bl]
    E = np.vstack([Ql[:, [0, 1]], Ql[:, [1, 2]], Ql[:, [2, 3]], Ql[:, [3, 0]]]); el_ = np.linalg.norm(X3[E[:, 0]] - X3[E[:, 1]], axis=1)
    Gq = sp.coo_matrix((el_, (E[:, 0], E[:, 1])), shape=(len(up), len(up))).tocsr()
    dgq, _, src = dijkstra(Gq, directed=False, indices=bl, min_only=True, return_predecessors=True)
    pos = {int(v): k for k, v in enumerate(bl)}; w = np.clip(1 - dgq / BAND, 0, 1); w = w * w * (3 - 2 * w)
    corr = np.array([dB[pos[int(s_)]] if s_ >= 0 else np.zeros(3) for s_ in src]); X3 = X3 + w[:, None] * corr
    # keratin: vertices on the grafted claw (near the transformed index keratin surface)
    TK = tri_of(Q, (own[Q] == ix).all(1) & ker[Q].all(1)); PK = to_thumb(P)
    dk = np.sqrt(igl.point_mesh_squared_distance(X3, PK, TK)[0]); nk_l = dk < prm.get('ker_tol_cm', 0.06)
    # keep only the keratin component containing the apex
    Ek = E[nk_l[E[:, 0]] & nk_l[E[:, 1]]]
    _, labk = connected_components(sp.coo_matrix((np.ones(len(Ek)), (Ek[:, 0], Ek[:, 1])), shape=(len(up), len(up))), directed=False)
    sa_ = int(np.argmin(np.linalg.norm(X3 - apTt, axis=1))); nk_l = nk_l & (labk == labk[sa_])
    Pn = P.copy(); Pn[up] = X3; out[vid] = Pn * Fl
    nk = np.zeros(n, bool); nk[up[nk_l]] = True; np.save(outf.replace('.npz', '_ker_%s.npy' % S), np.where(nk)[0])
    e = np.linalg.norm(X3[Ql] - X3[np.roll(Ql, 1, 1)], axis=2)
    report[S] = dict(scale=float(sg), cut_gap_mm_max=float(gap.max() * 10), patch_verts=int(len(up)), new_keratin=int(nk.sum()),
                     edge_mm_med=float(np.median(e) * 10), edge_mm_min=float(e.min() * 10), edge_mm_max=float(e.max() * 10),
                     apex_gap_cm=float(np.linalg.norm(X3 - apTt, axis=1).min()), seconds=time.time() - t0)
    log(S, json.dumps(report[S]))
np.savez(outf, V=out, **{k: z[k] for k in z.files if k != 'V'})
json.dump(report, open(outf.replace('.npz', '.json'), 'w'), indent=1); print(json.dumps(report))
