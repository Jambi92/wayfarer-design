# sa_xparam.py CAGE.npz OUT.npz : Option B fold repair by local CROSS-PARAMETERISATION (orders fe3b98a / 50ef121, local block parameterisation /
#   local source-patch mapping).  For every connected group of genuinely folded quads (host-aware census: inverted | bow-tie | concave, outside tip caps
#   and the tail module) a disk REGION of the fine cage is formed (the group dilated by RINGS rings, enclosed holes filled). Its border vertices stay where
#   they are. The source under it is refined locally (exact midpoint subdivision, REFINE levels -> finer than the cage), the border is traced on it as a
#   closed vertex loop (shortest paths between consecutive border vertices), the side of the loop that lies on the LEFT (same orientation as the cage
#   region) is flooded, and both disks are mapped to the unit circle with the same border parameter (cage arc length):
#       source  : mean-value (Floater) weights -> convex-combination map, bijective (Tutte / Floater);
#       cage    : uniform weights on the region's quad graph (CW=uniform) or mean-value weights on the current geometry (CW=mvc).
#   Interior cage vertices are lifted through  source_map^-1 o cage_map  -> the region is re-laid fold-free on its OWN source patch (no closest-point
#   projection, no classification against the opposite wall of a web slot). A region is kept only if its local census improves. Topology unchanged.
import sys, os, collections, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
from scipy.sparse.csgraph import dijkstra, connected_components
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, OUT = sys.argv[1:3]
RINGS = int(os.environ.get('RINGS', 2)); REFINE = int(os.environ.get('REFINE', 3)); CW = os.environ.get('CW', 'uniform'); MAXQ = int(os.environ.get('MAXQ', 6000))
z = dict(np.load(CG, allow_pickle=True)); Q = z['Q']; ql = z['qlab'].astype(str); nv = len(z['V'])
fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1)
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); FA = igl.doublearea(G.V, G.F)
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']); TAIL = ql == 'tail'
def cr(a_, b_): return a_[..., 0] * b_[..., 1] - a_[..., 1] * b_[..., 0]
def segx(p1, p2, p3, p4):
    d1 = cr(p4 - p3, p1 - p3); d2 = cr(p4 - p3, p2 - p3); d3 = cr(p2 - p1, p3 - p1); d4 = cr(p2 - p1, p4 - p1); return (d1 * d2 < 0) & (d3 * d4 < 0)
def census(qs):
    """host-aware census (identical to sa_foldcensus.py) on quads qs -> bad mask (inverted | bow-tie | concave)"""
    q4 = Q[qs]; P4 = V[q4]; tr = fiv[q4]; nref = (FN[tr] * FA[tr][..., None]).sum(1); nref /= np.linalg.norm(nref, axis=1, keepdims=True) + 1e-12
    c0 = P4.mean(1); e1 = P4[:, 1] - P4[:, 0]; e1 -= (e1 * nref).sum(1)[:, None] * nref; e1 /= np.linalg.norm(e1, axis=1, keepdims=True) + 1e-12; e2 = np.cross(nref, e1)
    xy = np.stack([((P4 - c0[:, None]) * e1[:, None]).sum(2), ((P4 - c0[:, None]) * e2[:, None]).sum(2)], 2)
    bow = segx(xy[:, 0], xy[:, 1], xy[:, 2], xy[:, 3]) | segx(xy[:, 1], xy[:, 2], xy[:, 3], xy[:, 0])
    area = 0.5 * sum(cr(xy[:, k], xy[:, (k + 1) % 4]) for k in range(4)); scale = (np.linalg.norm(np.diff(np.r_['1', xy, xy[:, :1]], axis=1), axis=2) ** 2).mean(1)
    inv = ~bow & (area < -1e-6 * scale)
    turn = np.stack([cr(xy[:, k] - xy[:, (k - 1) % 4], xy[:, (k + 1) % 4] - xy[:, k]) / (np.linalg.norm(xy[:, k] - xy[:, (k - 1) % 4], axis=1) * np.linalg.norm(xy[:, (k + 1) % 4] - xy[:, k], axis=1) + 1e-12) for k in range(4)], 1)
    conc = ~bow & ~inv & (turn.min(1) < -0.02)
    el = np.linalg.norm(P4 - np.roll(P4, -1, 1), axis=2); asp = el.max(1) / np.maximum(el.min(1), 1e-9)
    return inv | bow | conc, asp
# quad adjacency (shared vertex) for dilation / components
nq = len(Q); VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
Eall = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1)
def mvc_matrix(P, T, idx_local):
    """mean-value weights (Floater 2003) on triangle mesh (P, T): W[i, j] = (tan(a_ij / 2) + tan(b_ij / 2)) / |p_i - p_j| ; returns csr (n x n)"""
    rows, cols, vals = [], [], []
    for k in range(3):
        i, j, l = T[:, k], T[:, (k + 1) % 3], T[:, (k + 2) % 3]
        u = P[j] - P[i]; w_ = P[l] - P[i]; nu = np.linalg.norm(u, axis=1) + 1e-15; nw = np.linalg.norm(w_, axis=1) + 1e-15
        ang = np.arccos(np.clip((u * w_).sum(1) / (nu * nw), -1, 1)); t = np.tan(ang / 2)
        rows += [i, i]; cols += [j, l]; vals += [t / nu, t / nw]
    n = len(P); return sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsr()
def solve_disk(W, bidx, buv, n):
    """convex-combination map: interior rows normalised, boundary fixed"""
    W = W.tolil(); W.setdiag(0); W = W.tocsr(); W.eliminate_zeros(); s = np.asarray(W.sum(1)).ravel(); isb = np.zeros(n, bool); isb[bidx] = True; ii = np.nonzero(~isb)[0]
    L = (sp.diags(s) - W).tocsr(); UV = np.zeros((n, 2)); UV[bidx] = buv
    if len(ii):
        A = L[ii][:, ii].tocsc(); B = -(L[ii][:, bidx] @ buv); lu = spl.splu(A); UV[ii] = np.stack([lu.solve(B[:, 0]), lu.solve(B[:, 1])], 1)
    return UV
def region_disk(qset):
    """quad set -> (quads, ordered border loop) as a disk, filling enclosed holes; None if impossible"""
    qset = set(qset)
    for _ in range(6):
        qs = np.array(sorted(qset)); e = np.sort(np.stack([Q[qs], np.roll(Q[qs], -1, 1)], 2).reshape(-1, 2), 1); eu, cnt = np.unique(e, axis=0, return_counts=True)
        be = eu[cnt == 1]
        if len(be) == 0: return None
        adj = collections.defaultdict(list)
        for a, b in be: adj[a].append(b); adj[b].append(a)
        if any(len(v) != 2 for v in adj.values()):                         # pinched border vertex -> grow by one ring and retry
            qset |= set(np.nonzero((QQ[qs].sum(0) > 0).A1)[0].tolist()); continue
        loops = []; seen = set()
        for s0 in adj:
            if s0 in seen: continue
            lp = [s0, adj[s0][0]]; seen.update(lp)
            while lp[-1] != s0:
                nx = [y for y in adj[lp[-1]] if y != lp[-2]][0]
                if nx == s0: break
                lp.append(nx); seen.add(nx)
            loops.append(lp)
        if len(loops) == 1:
            lp = loops[0]
            # orient: region on the left = the loop direction matches the quad orientation of the border quads
            a, b = lp[0], lp[1]
            for q in qs:
                r = list(Q[q])
                if a in r and b in r:
                    ia = r.index(a); ok_dir = r[(ia + 1) % 4] == b; break
            if not ok_dir: lp = [lp[0]] + lp[1:][::-1]
            return qs, lp
        # holes: fill every non-outer loop's enclosed complement component (if small)
        L_ = [sum(np.linalg.norm(V[l[i]] - V[l[(i + 1) % len(l)]]) for i in range(len(l))) for l in loops]; outer = int(np.argmax(L_)); grew = False
        notin = np.ones(nq, bool); notin[qs] = False; notin[TAIL] = False
        for k, l in enumerate(loops):
            if k == outer: continue
            start = set(np.nonzero((VQ[l].sum(0) > 0).A1 & notin)[0].tolist()); comp = set(start); st = list(start)
            while st and len(comp) < MAXQ:
                q = st.pop()
                for q2 in QQ[q].indices:
                    if notin[q2] and q2 not in comp: comp.add(q2); st.append(q2)
            if len(comp) < MAXQ: qset |= comp; grew = True
        if not grew: return None
    return None
def optimize_uv(UVc, lc, Ql, lp, inner, UVs, Tl, Pl):
    """quality optimisation of the cage region INSIDE the bijective source map: cage vertices move in the map's disk (border fixed); 3-D positions =
    the map's piecewise-affine lift. Energy per quad corner: MIPS (|a|^2 + |b|^2) / (2 s), s = signed corner area against the host-face normal (barrier:
    s -> 0 is infinite, so no fold / dart / bow-tie can appear), plus an area-balance term (A / A0 + A0 / A). Gradient steps with back-tracking that
    reject any step making a corner non-positive in the map or in 3-D."""
    import torch, matplotlib.tri as mtri
    tri_ = mtri.Triangulation(UVs[:, 0], UVs[:, 1], Tl); tf = tri_.get_trifinder()
    U0 = UVs[Tl[:, 0]]; D = np.stack([UVs[Tl[:, 1]] - U0, UVs[Tl[:, 2]] - U0], 2); det = np.linalg.det(D); okd = np.abs(det) > 1e-24
    Dinv = np.zeros_like(D); Dinv[okd] = np.linalg.inv(D[okd]); P0 = Pl[Tl[:, 0]]; E3 = np.stack([Pl[Tl[:, 1]] - P0, Pl[Tl[:, 2]] - P0], 2); Aff = E3 @ Dinv   # (nt, 3, 2)
    TN = np.cross(Pl[Tl[:, 1]] - P0, Pl[Tl[:, 2]] - P0); TN /= np.linalg.norm(TN, axis=1, keepdims=True) + 1e-15
    nloc = len(UVc); isin = np.zeros(nloc, bool); isin[lc[inner]] = True; ii = np.nonzero(isin)[0]
    # local index of every region vertex -> global (for fixed 3-D positions of border vertices)
    glob = np.empty(nloc, int); glob[lc[lc >= 0] if False else np.arange(nloc)] = 0
    inv_lc = {int(l): g for g, l in enumerate(lc) if l >= 0}; Pfix = np.array([V[inv_lc[i]] for i in range(nloc)])
    def locate(X):
        f = tf(X[:, 0], X[:, 1])
        if (f < 0).any():
            cen = UVs[Tl].mean(1); kdc = cKDTree(cen); f[f < 0] = kdc.query(X[f < 0])[1]
        return f
    Qt = torch.tensor(Ql)
    def energy(Xi, f, A0=None, ret_parts=False):
        Af = torch.tensor(Aff[f]); u0 = torch.tensor(U0[f]); p0 = torch.tensor(P0[f]); nn = torch.tensor(TN[f])
        P3i = p0 + (Af @ (Xi - u0)[:, :, None])[:, :, 0]
        P = torch.tensor(Pfix).clone(); P[torch.tensor(ii)] = P3i
        N = torch.tensor(np.zeros((nloc, 3))); N[torch.tensor(ii)] = nn
        P4 = P[Qt]; a = torch.roll(P4, -1, 1) - P4; b = torch.roll(P4, 1, 1) - P4
        nq_ = N[Qt].sum(1); 
        nq_ = torch.where(torch.linalg.norm(nq_, dim=1, keepdim=True) > 1e-9, nq_, torch.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1], dim=1))
        nq_ = nq_ / torch.linalg.norm(nq_, dim=1, keepdim=True)
        sgn = (torch.cross(a, b, dim=2) * nq_[:, None]).sum(2)
        return P4, a, b, sgn
    X = UVc[ii].copy(); f = locate(X)
    with torch.no_grad(): P4, a, b, sgn = energy(torch.tensor(X), f)
    A0 = torch.clamp((0.5 * (sgn[:, 0] + sgn[:, 2])).abs(), min=float(sgn.abs().median()) * 0.5)
    WA = float(os.environ.get('WAREA', 0.5)); WU = float(os.environ.get('WUV', 1e-3))
    U4idx = torch.tensor(Ql); Ufix = torch.tensor(UVc)
    def chi(s_, e_): return 0.5 * (s_ + torch.sqrt(s_ * s_ + e_ * e_))
    def E_of(Xt, f, eps, epsu):
        P4, a, b, sgn = energy(Xt, f)
        mips = ((a * a).sum(2) + (b * b).sum(2)) / (2 * chi(sgn, eps)); A = chi(0.5 * (sgn[:, 0] + sgn[:, 2]), eps)
        U = Ufix.clone(); U[torch.tensor(ii)] = Xt; U4 = U[U4idx]; au = torch.roll(U4, -1, 1) - U4; bu = torch.roll(U4, 1, 1) - U4; su = au[..., 0] * bu[..., 1] - au[..., 1] * bu[..., 0]
        mu = ((au * au).sum(2) + (bu * bu).sum(2)) / (2 * chi(su, epsu))
        return mips.sum() + WA * (A / A0 + A0 / A).sum() + WU * mu.sum(), sgn, su
    eps = 0.2 * float(sgn.abs().median()); 
    with torch.no_grad():
        U4 = UVc[Ql]; au = np.roll(U4, -1, 1) - U4; bu = np.roll(U4, 1, 1) - U4; su0 = au[..., 0] * bu[..., 1] - au[..., 1] * bu[..., 0]
    epsu = 0.2 * float(np.median(np.abs(su0))); Xt = torch.tensor(X, requires_grad=True); E0 = None
    for outer in range(int(os.environ.get('OPT', 12))):
        f = locate(Xt.detach().numpy())
        opt_ = torch.optim.LBFGS([Xt], lr=1, max_iter=40, line_search_fn='strong_wolfe', history_size=10)
        def closure():
            opt_.zero_grad(); E, _, _ = E_of(Xt, f, eps, epsu); E.backward(); return E
        try: opt_.step(closure)
        except Exception: break
        with torch.no_grad(): E, sg_, su_ = E_of(Xt, f, eps, epsu)
        E0 = E.item() if E0 is None else E0; mn = float(sg_.min()); mnu = float(su_.min())
        eps = eps * (0.5 if mn < 0 else 0.1); epsu = epsu * (0.5 if mnu < 0 else 0.1)
        eps = max(eps, 1e-9); epsu = max(epsu, 1e-12)
    if os.environ.get('VERB'): print('    opt: E', round(E0, 1), '->', round(E.item(), 1), 'min corner', mn, 'min uv', mnu)
    UVo = UVc.copy(); UVo[ii] = Xt.detach().numpy(); return UVo
def repair(qs, lp):
    """cross-parameterise one disk region; returns (new fi, new bc) for interior vertices or None"""
    vreg = np.unique(Q[qs]); inner = np.setdiff1d(vreg, lp); inner = inner[~pin[inner]]
    if len(inner) == 0: return None
    # local refined source patch
    c = V[vreg].mean(0); rad = np.linalg.norm(V[vreg] - c, axis=1).max() * 1.6 + 0.4
    fsel = np.nonzero(np.linalg.norm(G.V[G.F].mean(1) - c, axis=1) < rad)[0]
    Vs, Fs = G.V, G.F[fsel]; used = np.unique(Fs); loc = -np.ones(len(G.V), int); loc[used] = np.arange(len(used)); Ps = G.V[used]; Ts = loc[Fs]
    lev = int(max(1, min(REFINE, np.floor(np.log(float(os.environ.get('MAXT', 6e5)) / max(len(Ts), 1)) / np.log(4)))))
    if REFINE: Ps, Ts = igl.upsample(Ps, Ts, lev)
    Es = igl.edges(Ts); el = np.linalg.norm(Ps[Es[:, 0]] - Ps[Es[:, 1]], axis=1); ns = len(Ps)
    GS = sp.coo_matrix((np.r_[el, el], (np.r_[Es[:, 0], Es[:, 1]], np.r_[Es[:, 1], Es[:, 0]])), shape=(ns, ns)).tocsr(); kd = cKDTree(Ps)
    bnd_s = np.zeros(ns, bool); bl_ = igl.boundary_facets(Ts); bl_ = bl_[0] if isinstance(bl_, tuple) else bl_; bnd_s[np.unique(np.asarray(bl_))] = True
    # border loop on the refined source: shortest paths between consecutive (snapped) border vertices
    sn = kd.query(V[lp])[1]; m = len(lp); loop = []; owner = []; usedv = set()
    import heapq
    def dpath(a, b, lim):
        """local Dijkstra a -> b avoiding vertices already on the loop (keeps the traced border simple in pinched slots)"""
        dist = {a: 0.0}; prev = {}; h = [(0.0, a)]
        while h:
            d0, u = heapq.heappop(h)
            if u == b: break
            if d0 > dist.get(u, np.inf) or d0 > lim: continue
            for x, w in zip(GS.indices[GS.indptr[u]:GS.indptr[u + 1]], GS.data[GS.indptr[u]:GS.indptr[u + 1]]):
                x = int(x)
                if x in usedv and x != b: continue
                nd = d0 + w
                if nd < dist.get(x, np.inf): dist[x] = nd; prev[x] = u; heapq.heappush(h, (nd, x))
        if b not in prev and a != b: return None
        p = [b]
        while p[-1] != a: p.append(prev[p[-1]])
        return p[::-1]
    for i in range(m):
        a = int(sn[i]) if not loop else int(loop[-1]) if False else int(sn[i]); b = int(sn[(i + 1) % m])
        if loop and a != (loop[-1] if True else a):
            pass
        cur = loop[-1] if loop else a
        tgt = b if i < m - 1 else int(loop[0])
        if cur == tgt: continue
        if tgt in usedv and i < m - 1: continue                       # two border vertices on one refined vertex: skip
        dd = np.linalg.norm(Ps[cur] - Ps[tgt]); p = dpath(cur, tgt, 4 * dd + 0.05)
        if p is None: p = dpath(cur, tgt, 12 * dd + 0.2)
        if p is None: return 'path'
        if not loop: loop.append(p[0]); owner.append(i); usedv.add(p[0])
        for v in p[1:]:
            if i == m - 1 and v == loop[0]: break
            loop.append(v); owner.append(i); usedv.add(v)
    loop = np.array(loop); owner = np.array(owner)
    if len(np.unique(loop)) != len(loop): return 'loop not simple'
    if bnd_s[loop].any(): return 'loop reaches patch border'
    # flood the LEFT side: faces containing a directed loop edge (a -> b) in their own orientation
    onl = np.zeros(ns, bool); onl[loop] = True; dir_ = {(int(loop[k]), int(loop[(k + 1) % len(loop)])) for k in range(len(loop))}
    seeds = set()
    for t in Ts[np.nonzero(onl[Ts].sum(1) >= 2)[0]]:
        for k in range(3):
            if (int(t[k]), int(t[(k + 1) % 3])) in dir_ and not onl[t[(k + 2) % 3]]: seeds.add(int(t[(k + 2) % 3]))
    if not seeds: return 'no seed'
    reg = np.zeros(ns, bool); st = list(seeds); reg[st] = True
    while st:
        u = st.pop()
        for x in GS.indices[GS.indptr[u]:GS.indptr[u + 1]]:
            if not reg[x] and not onl[x]: reg[x] = True; st.append(x)
    if (reg & bnd_s).any(): return 'flood leaks'
    rv = reg | onl; Tm = Ts[rv[Ts].all(1)]
    # faces made only of loop vertices: keep those on the left (contain a directed loop edge in their own orientation)
    allon = ~reg[Tm].any(1)
    if allon.any():
        lf = np.array([any((int(t[k]), int(t[(k + 1) % 3])) in dir_ for k in range(3)) for t in Tm[allon]]); keep = ~allon; keep[np.nonzero(allon)[0][lf]] = True; Tm = Tm[keep]
    usedm = np.unique(Tm); lm = -np.ones(ns, int); lm[usedm] = np.arange(len(usedm)); Tl = lm[Tm]; Pl = Ps[usedm]
    chi = len(Pl) - len(igl.edges(Tl)) + len(Tl)
    if chi != 1: return 'source region chi %d' % chi
    # border parameter: cage arc length; source loop vertices interpolated inside their owner segment
    cl = np.r_[0, np.cumsum([np.linalg.norm(V[lp[i]] - V[lp[(i + 1) % m]]) for i in range(m)])]; Lc = cl[-1]
    th = np.zeros(len(loop))
    for i in np.unique(owner):
        ks = np.nonzero(owner == i)[0]; P_ = Ps[loop[ks]]; nxt = Ps[loop[(ks[-1] + 1) % len(loop)]]
        seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack([P_, nxt]), axis=0), axis=1))]; t = seg[:-1] / max(seg[-1], 1e-12)
        th[ks] = (cl[i] + t * (cl[i + 1] - cl[i])) / Lc
    if np.any(np.diff(th) <= 0): return 'border param not monotone'
    bs = lm[loop]
    if (bs < 0).any(): return 'loop vertex dropped'
    UVs = solve_disk(mvc_matrix(Pl, Tl, None), bs, np.c_[np.cos(2 * np.pi * th), np.sin(2 * np.pi * th)], len(Pl))
    # cage map
    lc = -np.ones(nv, int); lc[vreg] = np.arange(len(vreg)); Ql = lc[Q[qs]]
    if CW == 'mvc':
        Tq = np.r_[Ql[:, [0, 1, 2]], Ql[:, [0, 2, 3]], Ql[:, [1, 2, 3]], Ql[:, [1, 3, 0]]]; Wc = mvc_matrix(V[vreg], Tq, None)
    else:
        e = np.sort(np.stack([Ql, np.roll(Ql, -1, 1)], 2).reshape(-1, 2), 1); e = np.unique(e, axis=0)
        Wc = sp.coo_matrix((np.ones(2 * len(e)), (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(len(vreg), len(vreg))).tocsr()
    pinned_in = np.nonzero(pin[vreg] & ~np.isin(vreg, lp))[0]
    if len(pinned_in): return 'pinned vertex inside'
    UVc = solve_disk(Wc, lc[np.array(lp)], np.c_[np.cos(2 * np.pi * cl[:-1] / Lc), np.sin(2 * np.pi * cl[:-1] / Lc)], len(vreg))
    # lift interior vertices through the source map
    import matplotlib.tri as mtri
    if int(os.environ.get('OPT', 200)) > 0:
        UVc = optimize_uv(UVc, lc, Ql, np.array(lp), inner, UVs, Tl, Pl)
        if isinstance(UVc, str): return UVc
    tf = mtri.Triangulation(UVs[:, 0], UVs[:, 1], Tl).get_trifinder(); X = UVc[lc[inner]]; ff = tf(X[:, 0], X[:, 1]); out = {}
    for v, x, f in zip(inner, X, ff):
        if f < 0:
            cen = UVs[Tl].mean(1); f = int(np.argmin(np.linalg.norm(cen - x, axis=1)))
            if np.linalg.norm(cen[f] - x) > 0.02: return 'lift miss'
        a_, b_, c_ = UVs[Tl[f]]; M = np.array([b_ - a_, c_ - a_]).T; l = np.linalg.lstsq(M, x - a_, rcond=None)[0]; w = np.r_[1 - l.sum(), l].clip(0); w /= w.sum()
        out[v] = w @ Pl[Tl[f]]
    vs = np.array(list(out)); P3 = np.array([out[v] for v in vs]); f2, b2, _ = G.embed(P3)
    return vs, f2, b2
bad, asp = census(np.arange(nq)); m_ = ~TIP & ~TAIL; bad &= m_
print('start: bad (inv | bow | conc) non-tip', int(bad.sum()), flush=True)
for rnd in range(int(os.environ.get('ROUNDS', 3))):
    rings = [int(x) for x in os.environ.get('RSEQ', '').split(',')][rnd] if os.environ.get('RSEQ') else RINGS + rnd
    selq = bad | (((asp > float(os.environ.get('ASPT', 4.0))) & m_) if 'asp' in os.environ.get('SEL', 'bad') else False)
    if os.environ.get('FOCUS'):
        fc_ = np.array([float(x) for x in os.environ['FOCUS'].split(',')]); selq = selq & (np.linalg.norm(V[Q].mean(1) - fc_[:3], axis=1) < fc_[3])
    bq = np.nonzero(selq)[0]; mask = np.zeros(nq, bool); mask[bq] = True
    for _ in range(rings): mask |= (QQ @ mask.astype(float)) > 0
    mask &= ~TAIL
    sub = QQ[mask][:, mask]; ncomp, lab = connected_components(sub, directed=False); qidx = np.nonzero(mask)[0]
    WHY = collections.Counter(); kept = 0
    for ci in range(ncomp):
        qset = qidx[lab == ci]
        if len(qset) > MAXQ: WHY['region too large'] += 1; continue
        rd = region_disk(qset)
        if rd is None: WHY['not a disk'] += 1; continue
        qs, lp = rd
        if TAIL[qs].any(): WHY['touches tail'] += 1; continue
        try: res = repair(qs, lp)
        except Exception as ex:
            if os.environ.get("DEBUG"): raise
            res = "error %s" % type(ex).__name__
        if isinstance(res, str) or res is None:
            WHY[res if res else 'none'] += 1
            if os.environ.get('VERB'): print('  comp', ci, 'quads', len(qs), collections.Counter(ql[qs]).most_common(2), 'bad', int(bad[qs].sum()), '->', res, np.round(V[Q[qs]].mean((0, 1)), 1))
            continue
        vs, f2, b2 = res
        ring = np.unique(np.r_[qs, np.nonzero((QQ[qs].sum(0) > 0).A1)[0]]); ring = ring[m_[ring]]
        b0, a0 = census(ring); old = (fiv[vs].copy(), bcv[vs].copy(), V[vs].copy())
        fiv[vs] = f2; bcv[vs] = b2; V[vs] = (b2[:, :, None] * G.V[G.F[f2]]).sum(1)
        b1, a1 = census(ring)
        if 'asp' in os.environ.get('SEL', 'bad'): good_ = (b1.sum() < b0.sum()) or (b1.sum() == b0.sum() and (a1 > 4).sum() < (a0 > 4).sum())
        else: good_ = b1.sum() < b0.sum() and (a1 > 4).sum() <= (a0 > 4).sum() + max(2, b0.sum() - b1.sum())
        if good_:
            kept += 1; WHY['kept'] += 1
        else:
            if os.environ.get('VERB'): print('  comp', ci, 'quads', len(qs), collections.Counter(ql[qs]).most_common(2), 'bad', int(b0.sum()), '->', int(b1.sum()), 'asp', int((a0 > 4).sum()), int((a1 > 4).sum()), np.round(V[Q[qs]].mean((0, 1)), 1))
            fiv[vs], bcv[vs], V[vs] = old; WHY['rejected bad %d->%d asp %d->%d' % (b0.sum(), b1.sum(), (a0 > 4).sum(), (a1 > 4).sum())] += 1
    bad, asp = census(np.arange(nq)); bad &= m_
    print('round', rnd, 'rings', rings, 'components', ncomp, 'kept', kept, 'bad now', int(bad.sum()), 'aspect>4 non-tip', int(((asp > 4) & m_).sum()), dict(WHY.most_common(12)), flush=True)
    z['V'] = V; z['tri'] = fiv; z['bc'] = bcv; np.savez_compressed(OUT, **z)
print('DONE')
