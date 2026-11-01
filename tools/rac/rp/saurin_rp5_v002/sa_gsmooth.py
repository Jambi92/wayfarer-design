# sa_gsmooth.py IN.npz OUT.npz [DESIGN.pkl] : GLOBAL fold-safe quad-quality optimisation on the working source (Option B T-4 aspect / angle closure).
#   Free vertices = the named regions (+ RING quad rings), minus pins / tail module / region border. Outer loop (re-linearisation):
#     every free vertex moves in the tangent plane of its own source host face  x = x0 + t1 e1 + t2 e2 ;
#     inner L-BFGS on  E = sum_corners MIPS (|a|^2 + |b|^2) / (2 chi(s, eps))  (s = signed corner area against the quad's host-face normal, the
#                          census frame; chi = Garanzha-type regularised barrier -> untangling-safe, eps shrinks every outer step)
#                       + WA * sum_q (A / A0 + A0 / A)           (A0 = 1-ring mean area of the input: density kept, sizes graded)
#                       + WANC * sum_v |t|^2 / h^2  (fine vertices) + WANC_C * ... (authored coarse corners: semantic loops stay)
#                       + AWT * sum relu(e_i / e_j - ART)^2 (explicit aspect barrier over the 12 edge-length ratios of a quad)
#                       + ANW * sum relu(|cos corner| - cos ANGT)^2 (corner angles inside ANGT .. 180 - ANGT)
#                       + CWT * sum relu(d_plane - 0.85 thr)^2 / thr^2  (coverage: source vertices -> plane of their nearest cage triangle; thr 1.3 mm
#                         in head / hand / foot / tail zones, 2.7 mm body)
#                       + trust region |t| <= TR h ;
#     then closest-point re-projection onto the source (rejected for a vertex if it changes sheet: host normal turn > 60 deg).
#   After every outer step the host-aware fold census is evaluated; vertices of quads that newly fold are rolled back (fold-safe). Topology unchanged.
import sys, os, pickle, numpy as np, igl, scipy.sparse as sp, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; NC = len(pickle.load(open(sys.argv[3], 'rb'))['C']) if len(sys.argv) > 3 else 0
OUTER = int(os.environ.get('OUTER', 15)); WA = float(os.environ.get('WA', 0.3)); WANC = float(os.environ.get('WANC', 0.002)); WANC_C = float(os.environ.get('WANC_C', 2.0)); TR = float(os.environ.get('TR', 0.6)); AWT = float(os.environ.get('AWT', 0.0)); ART = float(os.environ.get('ART', 3.6)); ANW = float(os.environ.get('ANW', 0.0)); CWT = float(os.environ.get('CWT', 0.0)); ACS = np.cos(np.radians(float(os.environ.get('ANGT', 46))))
torch.set_default_dtype(torch.float64)
z = dict(np.load(IN, allow_pickle=True)); Q = z['Q']; ql = z['qlab'].astype(str); nv = len(z['V']); nq = len(Q)
fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); Vin = V.copy()
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); FA = igl.doublearea(G.V, G.F); ab = igl.AABB(); ab.init(G.V, G.F)
zoneS = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thrS = np.where(zoneS, float(os.environ.get('THZ', 0.13)), float(os.environ.get('THB', 0.27)))
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']); TAIL = ql == 'tail'; m_ = ~TIP & ~TAIL
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
def metrics(P):
    P4 = P[Q]; el = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); asp = el.max(1) / np.maximum(el.min(1), 1e-9)
    u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4; ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12), -1, 1)))
    return asp, ang
def nref_of(tri):
    n = (FN[tri[Q]] * FA[tri[Q]][..., None]).sum(1); return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
def cr(a_, b_): return a_[..., 0] * b_[..., 1] - a_[..., 1] * b_[..., 0]
def segx(p1, p2, p3, p4):
    d1 = cr(p4 - p3, p1 - p3); d2 = cr(p4 - p3, p2 - p3); d3 = cr(p2 - p1, p3 - p1); d4 = cr(p2 - p1, p4 - p1); return (d1 * d2 < 0) & (d3 * d4 < 0)
def census(P, tri):
    """host-aware census (sa_foldcensus.py): inverted | bow-tie | concave per quad"""
    P4 = P[Q]; nr = nref_of(tri); c0 = P4.mean(1); e1 = P4[:, 1] - P4[:, 0]; e1 -= (e1 * nr).sum(1)[:, None] * nr; e1 /= np.linalg.norm(e1, axis=1, keepdims=True) + 1e-12; e2 = np.cross(nr, e1)
    xy = np.stack([((P4 - c0[:, None]) * e1[:, None]).sum(2), ((P4 - c0[:, None]) * e2[:, None]).sum(2)], 2)
    bow = segx(xy[:, 0], xy[:, 1], xy[:, 2], xy[:, 3]) | segx(xy[:, 1], xy[:, 2], xy[:, 3], xy[:, 0])
    area = 0.5 * sum(cr(xy[:, k], xy[:, (k + 1) % 4]) for k in range(4)); sc = (np.linalg.norm(np.diff(np.r_['1', xy, xy[:, :1]], axis=1), axis=2) ** 2).mean(1)
    inv = ~bow & (area < -1e-6 * sc)
    turn = np.stack([cr(xy[:, k] - xy[:, (k - 1) % 4], xy[:, (k + 1) % 4] - xy[:, k]) / (np.linalg.norm(xy[:, k] - xy[:, (k - 1) % 4], axis=1) * np.linalg.norm(xy[:, (k + 1) % 4] - xy[:, k], axis=1) + 1e-12) for k in range(4)], 1)
    return inv | bow | (~bow & ~inv & (turn.min(1) < -0.02))
asp, ang = metrics(V)
labs = os.environ.get('LABELS', 'palm,finger,finger_web,thumb,wrist,foot,forefoot,toe,toe_web,ankle').split(',')
reg = (np.isin(ql, labs) | ((((asp > 3.6) | (ang.min(1) < 47) | (ang.max(1) > 133)) & m_) if os.environ.get('RESID') else False)) & ~TAIL
if os.environ.get('COVREG'):                                                          # + quads nearest to source vertices above their coverage threshold
    _TT = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; _cg = igl.AABB(); _cg.init(V, _TT); _d, _ti, _ = _cg.squared_distance(V, _TT, G.V)
    _far = np.sqrt(_d) > 0.8 * thrS; reg[np.r_[np.arange(nq), np.arange(nq)][_ti[_far]]] = True; reg &= ~TAIL
for _ in range(int(os.environ.get('RING', 2))): reg = ((QQ @ reg.astype(float)) > 0) & ~TAIL
regv = np.zeros(nv, bool); regv[Q[reg].ravel()] = True; border = np.zeros(nv, bool); border[Q[~reg].ravel()] = True
free = regv & ~border & ~pin
if os.environ.get('FIXC') and NC: free[:NC] = False                                  # authored coarse corners fixed (semantic loops exact)
fidx = np.nonzero(free)[0]; RQ = np.nonzero(reg)[0]; iscorner = fidx < NC
el_ = np.linalg.norm(V[Q] - np.roll(V[Q], -1, 1), axis=2); hs = np.zeros(nv); hc = np.zeros(nv); np.add.at(hs, Q.ravel(), el_.ravel()); np.add.at(hc, Q.ravel(), 1); h = hs / np.maximum(hc, 1)
nr0 = nref_of(fiv); P4 = V[Q]; s0 = (np.cross(np.roll(P4, -1, 1) - P4, np.roll(P4, 1, 1) - P4) * nr0[:, None]).sum(2); Aq = np.abs(0.5 * (s0[:, 0] + s0[:, 2]))
A0 = np.asarray((QQ @ Aq)).ravel() / np.asarray(QQ.sum(1)).ravel()
def report(tag):
    asp, ang = metrics(V); bad = census(V, fiv) & m_
    _TT = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; _cg = igl.AABB(); _cg.init(V, _TT); _d = np.sqrt(_cg.squared_distance(V, _TT, G.V)[0]) * 10
    tag = tag + ' | cover max body %.2f zone %.2f mm' % (_d[~zoneS].max(), _d[zoneS].max())
    print(tag, '| fold census bad non-tip', int(bad.sum()), '| aspect>4 non-tip', int(((asp > 4) & m_).sum()), 'max %.1f' % asp[m_].max(), '| angle out non-tip', int((((ang.min(1) < 45) | (ang.max(1) > 135)) & m_).sum()),
          '| drift corners max %.2f mm, fine p95 %.2f max %.2f mm' % ((np.linalg.norm(V[fidx[iscorner]] - Vin[fidx[iscorner]], axis=1).max() * 10) if iscorner.any() else 0, np.percentile(np.linalg.norm(V[fidx] - Vin[fidx], axis=1), 95) * 10, np.linalg.norm(V[fidx] - Vin[fidx], axis=1).max() * 10), flush=True)
print('region quads', len(RQ), 'free vertices', len(fidx), 'authored corners among them', int(iscorner.sum()), flush=True)
report('start')
Qr = torch.tensor(Q[RQ]); A0t = torch.tensor(A0[RQ]); idx = torch.tensor(fidx); wanc = torch.tensor(np.where(iscorner, WANC_C, WANC) / h[fidx] ** 2)
eps_rel = float(os.environ.get('EPS0', 0.05))
for outer in range(OUTER):
    bad0 = census(V, fiv) & m_
    nr = torch.tensor(nref_of(fiv)[RQ]); fn = FN[fiv[fidx]]; e1 = np.cross(fn, np.where(np.abs(fn[:, :1]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))); e1 /= np.linalg.norm(e1, axis=1, keepdims=True); e2 = np.cross(fn, e1)
    E1 = torch.tensor(e1); E2 = torch.tensor(e2); Vt = torch.tensor(V); T = torch.zeros((len(fidx), 2), requires_grad=True)
    eps = eps_rel * float(np.median(np.abs(s0)))
    Vcur = V.copy(); Vin_t = torch.tensor(Vin[fidx]); x0 = torch.tensor(V[fidx]); hT = torch.tensor(h[fidx])
    if CWT > 0:                                                                       # coverage: source vertices -> nearest cage triangle (region quads)
        TT_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; tq_ = np.r_[np.arange(nq), np.arange(nq)]; cgA = igl.AABB(); cgA.init(V, TT_)
        dS, tiS, _ = cgA.squared_distance(V, TT_, G.V); dS = np.sqrt(dS); selS = reg[tq_[tiS]] & (dS > 0.5 * thrS)
        Sidx = np.nonzero(selS)[0]; asg = torch.tensor(TT_[tiS[Sidx]]); Sp = torch.tensor(G.V[Sidx]); thS = torch.tensor(thrS[Sidx])
    def energy():
        X = x0 + T[:, :1] * E1 + T[:, 1:] * E2; P = Vt.clone(); P[idx] = X; P4 = P[Qr]
        a = torch.roll(P4, -1, 1) - P4; b = torch.roll(P4, 1, 1) - P4; s = (torch.cross(a, b, dim=2) * nr[:, None]).sum(2)
        chi = 0.5 * (s + torch.sqrt(s * s + eps * eps)); mips = (((a * a).sum(2) + (b * b).sum(2)) / (2 * chi)).sum()
        A = 0.5 * (chi[:, 0] + chi[:, 2]); area = WA * (A / A0t + A0t / A).sum()
        anc = (wanc * ((X - Vin_t) ** 2).sum(1)).sum(); tn = torch.linalg.norm(T, dim=1) / hT; trr = 100.0 * torch.relu(tn - TR).pow(2).sum()
        el = torch.linalg.norm(a, dim=2); ratio = el[:, :, None] / (el[:, None, :] + 1e-12); asp_t = AWT * torch.relu(ratio - ART).pow(2).sum()
        cs = (a * b).sum(2) / (torch.linalg.norm(a, dim=2) * torch.linalg.norm(b, dim=2) + 1e-12); ang_t = ANW * torch.relu(cs.abs() - ACS).pow(2).sum()
        cov = 0.0
        if CWT > 0 and len(Sidx):
            A_ = P[asg[:, 0]]; B_ = P[asg[:, 1]]; C_ = P[asg[:, 2]]; nn_ = torch.cross(B_ - A_, C_ - A_, dim=1); nn_ = nn_ / (torch.linalg.norm(nn_, dim=1, keepdim=True) + 1e-12)
            dpl = ((Sp - A_) * nn_).sum(1).abs(); cov = CWT * (torch.relu(dpl - 0.85 * thS) / thS).pow(2).sum()
        return mips + area + anc + trr + asp_t + ang_t + cov
    opt = torch.optim.LBFGS([T], lr=1, max_iter=int(os.environ.get('INNER', 60)), line_search_fn='strong_wolfe', history_size=20)
    def closure():
        opt.zero_grad(); E = energy(); E.backward(); return E
    E_before = energy().item(); opt.step(closure); E_after = energy().item()
    X = (x0 + T[:, :1] * E1 + T[:, 1:] * E2).detach().numpy()
    _, ff, cp = ab.squared_distance(G.V, G.F, X); okn = (FN[ff] * fn).sum(1) > 0.5
    Vn = V.copy(); fn_ = fiv.copy(); Vn[fidx[okn]] = cp[okn]; fn_[fidx[okn]] = ff[okn]
    # fold safety: roll back the vertices of quads that are newly bad (repeat until stable)
    asp_old, _ = metrics(V)
    for _r in range(20):
        asp_new, _ = metrics(Vn)
        b1 = (census(Vn, fn_) & m_ & ~bad0) | ((asp_new > np.maximum(asp_old, 4.0)) & m_)
        if not b1.any(): break
        rv = np.unique(Q[b1].ravel()); rv = rv[free[rv]]; Vn[rv] = V[rv]; fn_[rv] = fiv[rv]
    V = Vn; fiv = fn_
    report('outer %d E %.1f -> %.1f' % (outer, E_before, E_after)); eps_rel *= float(os.environ.get('EPSDECAY', 0.5))
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z)
V = (bc2[:, :, None] * G.V[G.F[fi2]]).sum(1); fiv = fi2; report('final (re-embedded)'); print('DONE')
