# ear_layout3.py : order 0d9c70b -- Fenn ear-branch sheet TOPOLOGY v002 (layout v3).
#
# v001 (layout2) used a 12 x 12 upper-extension kite F2 (corners Y, c1f, tip, P_up) whose rows swept ~90 deg from the cut Y -> P_up to the
# anterior helix edge, so both line families converged into the tip and crossed obliquely along the posterior rim (the T-4 band).
# v002 keeps the bridge block, the junction ring J, the attachment notch U and the rim strip architecture, and re-partitions the free ear:
#   F1' crescent  one 28 x kb block from the lobe front (Dp) to a new cut c1f -> P_up, between the whole notch U (c0f -> c1f, n_a edges)
#                 and the posterior rim P_lo -> P_up (n_a edges). The old corner Y becomes a regular U vertex.
#   leaf          the upper extension above the cut c1f -> P_up: rows run ACROSS the ear from the anterior helix edge (Ant[k]) to the
#                 posterior rim (Pup[k]); columns run along the ear towards the tip. The column count drops kb -> 2 through 3 -> 1
#                 reduction templates (two interior valence-3 / two valence-5 vertices each, staggered, never in consecutive bands) placed where
#                 the row width calls for it; the last 2-column row closes in one diamond quad at the tip.
# The back sheet repeats F1' + leaf (same (s, t) parameters), the rim strip wraps the new outline path (Dp, P_lo -> P_up, P_up -> tip, tip -> c1f).
import numpy as np
from scipy.spatial import cKDTree
import ear_branch_lib as E

TOPO3 = dict(n_a=28, kb=12, j_f=3, K_r=4, R=None)       # R (leaf rows) is derived once from the canonical E2 metric and stored

def _dense_xy(ip, st):
    return ip.flat(st[:, 0], st[:, 1])

def _hermite_xy(P0, T0, P1, T1, n=2000):
    u = np.linspace(0, 1, n)[:, None]; h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
    return h00 * P0 + h10 * T0 + h01 * P1 + h11 * T1

def _unit(v): return v / (np.linalg.norm(v) + 1e-12)

def _resample_xy(X, n, grade=None):
    c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; c /= c[-1]; u = np.linspace(0, 1, n + 1)
    if grade is not None:
        r = grade ** (1.0 / max(n - 1, 1)); e = r ** np.arange(n); u = np.r_[0, np.cumsum(e)] / e.sum()
    return np.c_[np.interp(u, c, X[:, 0]), np.interp(u, c, X[:, 1])]

def column_schedule(lengths, spacing, n0, hmin_ratio=1.0, gap=2):
    """even, non-increasing column counts per row: n0 at row 0, -2 steps when row length / count < hmin_ratio x row spacing,
    reductions at least `gap` rows apart, final row 2"""
    R = len(lengths) - 1; n = [n0]; last = -gap
    for k in range(1, R + 1):
        cur = n[-1]; want = max(2, int(2 * np.floor(lengths[k] / (hmin_ratio * spacing[k]) / 2)))
        rows_left = R - k; need = (cur - 2) // 2                      # reductions still needed to reach 2 by row R
        must = need > 0 and need * gap > rows_left - 0                # forced to keep pace
        if cur > 2 and k - last >= gap and (want < cur or must): cur -= 2; last = k
        n.append(cur)
    return n

def layout3(p=E.CAND['E2'], topo=TOPO3, h_red=0.75, gap=2, cap=1.0, cut_t0=0.55, cut_t1=0.45, stagger=1, R=None, fix_cut=True, a_bow=None, a_ex=None, a_hook=0.0, a_hook_w=0.12, step_min=1.0, h_red_last=None, cap_d=None):
    na, kb, jf, Kr = [topo[k] for k in ('n_a', 'kb', 'j_f', 'K_r')]; ip = E.InPlane(p)
    side = lambda st: ip.flat(st[:, 0], st[:, 1])
    def arc_split(st_dense, L0):
        X = side(st_dense); c = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]; return int(np.searchsorted(c, L0))
    # ---- unchanged v001 boundary pieces (bridge, attachment, junction, lobe front)
    # attachment line A: forward bow (v001: A_BOW, A_EX); v002 option: a posterior hook at both ends (a_hook, width a_hook_w in lambda) so the
    # bridge corners at c0 / c1 open less than v001's near-reflex corner
    a_bow = E.A_BOW if a_bow is None else a_bow; a_ex = E.A_EX if a_ex is None else a_ex
    lamA = np.linspace(0, 1, 4000); hook = lambda l_: (l_ / a_hook_w) * np.exp(1 - l_ / a_hook_w)
    Ad = np.c_[E.S0 + (E.S1 - E.S0) * lamA, -1 - a_bow * np.sin(np.pi * lamA) ** a_ex + a_hook * (hook(lamA) + hook(1 - lamA))]
    XA = ip.flat(Ad[:, 0], Ad[:, 1]); cA = np.r_[0, np.cumsum(np.linalg.norm(np.diff(XA, axis=0), axis=1))]; cA /= cA[-1]
    wA = 1 + E.A_END * np.abs(2 * (np.arange(na) + 0.5) / na - 1) ** 3; uA = np.r_[0, np.cumsum(wA)] / wA.sum()
    A = np.c_[np.interp(uA, cA, Ad[:, 0]), np.interp(uA, cA, Ad[:, 1])]; A[0] = (E.S0, -1.0); A[-1] = (E.S1, -1.0)
    Bd = E._curve_st([(E.S1, -1, 1.0, -1)]); k = arc_split(Bd, E.DATT); Batt = E._resample(Bd[:k + 1], ip, jf)
    Dd = E._curve_st([(E.S0, -1, 0.0, -1)]); k2 = arc_split(Dd, E.DATT_D); Datt = E._resample(Dd[:k2 + 1], ip, jf)
    c0f, c1f = Datt[-1], Batt[-1]
    Dp = E._resample(np.r_[Dd[k2:], E._curve_st([(0.0, 1, E.S3, 1)])], ip, kb)               # c0f -> lobe -> P_lo
    lam = np.linspace(0, 1, 4000); Ust = np.c_[c0f[0] + (c1f[0] - c0f[0]) * lam, -1 + (E.U_T + 1) * np.sin(np.pi * lam) ** E.U_EX]
    U = E._resample(Ust, ip, na); U[0] = c0f; U[-1] = c1f
    # ---- new pieces
    Plow = E._resample(E._curve_st([(E.S3, 1, E.S_UP, 1)]), ip, na)                          # P_lo -> P_up (n_a edges, matches U)
    antd = np.r_[Bd[k:], [[1.0, 0.0]]]; pupd = np.r_[E._curve_st([(E.S_UP, 1, 1.0, 1)]), [[1.0, 0.0]]]
    # leaf rows by marching (square cells): both sides at the same arc-length fraction lam; step = current cell width / mean side length;
    # columns drop by 2 when the cell width falls below h_red x the cut cell width (reductions >= gap rows apart); stop when a square cap fits
    def arcp(st_):
        X_ = side(st_); c_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(X_, axis=0), axis=1))]; return X_, c_
    XA_, cA_ = arcp(antd); XP_, cP_ = arcp(pupd); LA, LP = cA_[-1], cP_[-1]; Lm = 0.5 * (LA + LP)
    at = lambda X_, c_, lam: np.c_[np.interp(lam * c_[-1], c_, X_[:, 0]), np.interp(lam * c_[-1], c_, X_[:, 1])][0]
    w = lambda lam: np.linalg.norm(at(XA_, cA_, lam) - at(XP_, cP_, lam))
    lam = [0.0]; ncol = [kb]; h0 = w(0.0) / kb; last = 0
    while True:
        lk = lam[-1]; nk = ncol[-1]; wk = w(lk)
        if nk == 2 and ((1 - lk) * Lm <= cap * wk if cap_d is None else (1 - lk) * Lm <= cap_d): break     # R2: cap over a fixed final length
        fstep = step_min + (1 - step_min) * min(1.0, wk / (h0 * kb))                 # R2: rows tighten towards the tip (cells start wide; robust to sharper tips)
        ln = lk + fstep * (wk / nk) / Lm; ln = min(ln, 0.995); wn = w(ln); nn = nk
        hr_ = h_red_last if (h_red_last is not None and nk == 4) else h_red                 # R2: the last reduction (4 -> 2) happens at a wider row
        if nk > 2 and len(lam) - last >= gap and wn / nk < hr_ * h0: nn = nk - 2; last = len(lam)
        lam.append(ln); ncol.append(nn)
        if len(lam) > 80: raise RuntimeError('leaf march did not close')
    R = len(lam) - 1; lam_all = np.r_[lam, 1.0]
    st_at = lambda st_, c_, l_: np.c_[np.interp(l_ * c_[-1], c_, st_[:, 0]), np.interp(l_ * c_[-1], c_, st_[:, 1])]
    Ant = st_at(antd, cA_, lam_all); Pup = st_at(pupd, cP_, lam_all); Ant[0] = c1f; Ant[-1] = (1.0, 0.0); Pup[0] = (E.S_UP, 1.0); Pup[-1] = (1.0, 0.0)
    # cut c1f -> P_up: leaves c1f along the bisector of (back along U, forward along Ant), meets the posterior rim at a right angle
    XU = side(Ust); XAnt = side(antd); XPu = side(pupd); P0 = side(c1f[None])[0]; P1 = side(np.array([[E.S_UP, 1.0]]))[0]
    dU = _unit(XU[-40] - XU[-1]); dA = _unit(XAnt[40] - XAnt[0]); bis = _unit(dU + dA)
    tr = _unit(XPu[40] - XPu[0]); nout = np.array([tr[1], -tr[0]]); nout = nout if nout @ (P1 - P0) > 0 else -nout
    ch = np.linalg.norm(P1 - P0); Xc = _hermite_xy(P0, cut_t0 * 2 * ch * bis, P1, cut_t1 * 2 * ch * nout)
    sd = np.linspace(0, 1, 801); td = np.linspace(-1.6, 1, 521); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1]))
    Xcut = _resample_xy(Xc, kb); Cst, _ = E._invert(Xcut, ip, tree, G); Cst[0] = c1f; Cst[-1] = (E.S_UP, 1.0)
    # ---- F1' crescent grid (TFI + Winslow): A = U (c0f -> c1f), C = Plow (P_lo -> P_up), D = Dp (c0f -> P_lo), B = cut (c1f -> P_up)
    blocks = dict(bridge=(A, U, Datt, Batt, ('front',)), F1=(U, Plow, Dp, Cst, ('front', 'back')))
    grids = {}; err = 0.0
    for nm, (a_, c_, d_, b_, sh) in blocks.items():
        X = E._winslow(E._tfi(side(a_), side(c_), side(d_), side(b_))); st = np.zeros(X.shape[:2] + (2,))
        inner = X[1:-1, 1:-1].reshape(-1, 2)
        if len(inner):
            s_, e_ = E._invert(inner, ip, tree, G); st[1:-1, 1:-1] = s_.reshape(X.shape[0] - 2, X.shape[1] - 2, 2); err = max(err, float(e_.max()))
        st[:, 0] = a_; st[:, -1] = c_; st[0, :] = d_; st[-1, :] = b_; grids[nm] = (st, sh)
    # ---- leaf rows (in-plane): row 0 = cut (kb edges); row k from Ant[k] to Pup[k]
    XAk = side(Ant); XPk = side(Pup); Xcut0 = side(Cst)
    assert ncol[-1] == 2, ncol
    rows = []
    chord0 = np.linspace(0, 1, kb + 1)[:, None] * (Xcut0[-1] - Xcut0[0]) + Xcut0[0]; dev0 = Xcut0 - chord0   # cut deviation from its chord
    for kk in range(R + 1):
        n = ncol[kk]; xi = np.linspace(0, 1, n + 1)[:, None]; base = XAk[kk] + xi * (XPk[kk] - XAk[kk])
        fade = (1 - kk / (R + 1)) ** 2; d = np.c_[np.interp(xi[:, 0], np.linspace(0, 1, kb + 1), dev0[:, 0]), np.interp(xi[:, 0], np.linspace(0, 1, kb + 1), dev0[:, 1])]
        rows.append(Xcut0.copy() if kk == 0 else base + fade * d)
    # ---- assemble vertex ids: (s, t) for every in-plane point by inversion (outline points keep their parameters)
    idx = {}; sts = []; part = []
    def vid(sheet, s_t):
        key = (sheet, round(float(s_t[0]), 9), round(float(s_t[1]), 9))
        if key not in idx: idx[key] = len(sts); sts.append(np.array(s_t, float)); part.append(sheet)
        return idx[key]
    def vnew(sheet, tag, s_t):
        key = (sheet, tag)
        if key not in idx: idx[key] = len(sts); sts.append(np.array(s_t, float)); part.append(sheet)
        return idx[key]
    F = []; FB = []
    for nm, (st, sh) in grids.items():
        for sheet in sh:
            ni, nj = st.shape[0] - 1, st.shape[1] - 1; ids = [[vid(sheet, st[i, j]) for j in range(nj + 1)] for i in range(ni + 1)]
            for i in range(ni):
                for j in range(nj): F.append([ids[i][j], ids[i + 1][j], ids[i + 1][j + 1], ids[i][j + 1]]); FB.append(nm + '_' + sheet)
    rows_st = []
    for kk in range(R + 1):
        Xr = rows[kk]
        if kk == 0: rst = Cst.copy()
        else:
            rst = np.zeros((len(Xr), 2)); rst[0] = Ant[kk]; rst[-1] = Pup[kk]
            if len(Xr) > 2: rst[1:-1], _ = E._invert(Xr[1:-1], ip, tree, G)
        rows_st.append(rst)
    tip = np.array([1.0, 0.0]); red_log = []
    for sheet in ('front', 'back'):
        rid = [[vid(sheet, q) if (kk == 0 or j in (0, len(rows_st[kk]) - 1)) else vnew(sheet, ('row', kk, j), rows_st[kk][j]) for j, q in enumerate(rows_st[kk])]
               for kk in range(R + 1)]
        ridx = 0
        for kk in range(R):
            b = rid[kk]; t = rid[kk + 1]; nb_, nt_ = len(b) - 1, len(t) - 1
            if nt_ == nb_:
                for j in range(nb_): F.append([b[j], b[j + 1], t[j + 1], t[j]]); FB.append('leaf_' + sheet)
            else:
                assert nt_ == nb_ - 2
                c = (nb_ - 4) // 2 + (stagger * (1 if ridx % 2 else -1) if nb_ >= 8 else 0); c = int(np.clip(c, 0, nb_ - 3)); ridx += 1
                for j in range(c): F.append([b[j], b[j + 1], t[j + 1], t[j]]); FB.append('leaf_' + sheet)
                # 3 -> 1 template over b[c..c+3] / t[c], t[c+1]; m1, m2 halfway up above b[c+1], b[c+2]
                Xb = rows[kk]; Xt = rows[kk + 1]
                m_xy = [0.5 * (Xb[c + 1] + 0.5 * (Xt[c] + Xt[c + 1])), 0.5 * (Xb[c + 2] + 0.5 * (Xt[c] + Xt[c + 1]))]
                m_st, _ = E._invert(np.array(m_xy), ip, tree, G)
                m1 = vnew(sheet, ('m', kk, 1), m_st[0]); m2 = vnew(sheet, ('m', kk, 2), m_st[1])
                F += [[b[c], b[c + 1], m1, t[c]], [b[c + 1], b[c + 2], m2, m1], [b[c + 2], b[c + 3], t[c + 1], m2], [m1, m2, t[c + 1], t[c]]]; FB += ['leaf_tr_' + sheet] * 4
                for j in range(c + 3, nb_): F.append([b[j], b[j + 1], t[j - 1], t[j - 2]]); FB.append('leaf_' + sheet)
                if sheet == 'front': red_log.append(dict(band=kk, from_cols=nb_, to_cols=nt_, at_col=c))
        last = rid[R]; assert len(last) == 3
        F.append([last[0], last[1], last[2], vid(sheet, tip)]); FB.append('leaf_cap_' + sheet)
    # ---- rim strip along the new outline path: c0f -> lobe -> P_lo -> P_up -> tip -> c1f
    path = np.r_[Dp, Plow[1:], Pup[1:], Ant[::-1][1:]]
    fr = [vid('front', q) for q in path]; bk = [vid('back', q) for q in path]; rim = []
    for q in range(len(path)):
        row = [fr[q]]
        for r in range(1, Kr): idx[('rim', r, q)] = len(sts); sts.append(path[q].copy()); part.append('rim'); row.append(len(sts) - 1)
        row.append(bk[q]); rim.append(row)
    nDp, nPl = len(Dp) - 1, len(Plow) - 1
    for q in range(len(path) - 1):
        for r in range(Kr): F.append([rim[q][r], rim[q + 1][r], rim[q + 1][r + 1], rim[q][r + 1]]); FB.append('rim_up' if q >= nDp + nPl else 'rim')
    J = [vid('front', q) for q in A] + [vid('front', q) for q in Batt[1:]] + rim[-1][1:] + [vid('back', q) for q in U[::-1][1:]]
    J += rim[0][1:][::-1][1:] + [vid('front', q) for q in Datt[::-1][:-1]]
    Jseg = ['A'] * (na + 1) + ['Batt'] * jf + ['rimB'] * (Kr - 1) + ['U'] * (na + 1) + ['rimD'] * (Kr - 1) + ['Datt'] * jf
    assert len(J) == 2 * (na + jf + Kr) and len(set(J)) == len(J), (len(J), len(set(J)))
    F = np.array(F); sts = np.array(sts); part = np.array(part)
    nb = {}
    for f in F:
        for a_ in range(4): nb.setdefault(f[a_], set()).update({f[(a_ + 1) % 4], f[(a_ - 1) % 4]})
    Js = set(J); Jdir = []
    for v in J:
        ws = [w for w in nb[v] if w not in Js]
        if not ws:
            f = [f for f in F if v in f][0]; ws = [int(f[(list(f).index(v) + 2) % 4])]
        Jdir.append([v, ws[0]])
    Jnb = {int(v): [int(w) for w in nb[v] if w not in Js] for v in J}
    inward = {}; pathset = set(fr)
    for q, v in enumerate(fr):
        ws = [w for w in nb[v] if part[w] == 'front' and w not in pathset]; inward[q] = ws[0] if ws else (fr[q + 1] if q + 1 < len(fr) else fr[q - 1])
    cut_front = [vid('front', q) for q in Cst]
    corners = dict(c0=vid('front', A[0]), c1=vid('front', A[-1]), c0f=vid('front', c0f), c1f=vid('front', c1f), Y=vid('front', U[16]), P_lo=vid('front', Plow[0]),
                   P_up=vid('front', Plow[-1]), tip=vid('front', tip), tip_b=vid('back', tip))
    return dict(st=sts, part=part, F=F, J=np.array(J), Jseg=Jseg, Jdir=np.array(Jdir), Jnb=Jnb, rim=rim, rim_inward=inward, idx=idx,
                info=dict(corners=corners, inv_err_max=err, path_edges=len(path) - 1, leaf_columns=ncol, reductions=red_log, cut_front=cut_front, fix_cut=fix_cut,
                          params=dict(R=R, h_red=h_red, gap=gap, cap=cap, step_min=step_min, h_red_last=h_red_last, cap_d=cap_d, a_bow=a_bow, a_ex=a_ex, a_hook=a_hook, a_hook_w=a_hook_w, cut_t0=cut_t0, cut_t1=cut_t1, stagger=stagger, lam=[float(x) for x in lam])),
                topo=dict(topo, R=R, ka=R + 1), face_block_list=FB)

# ------------------------------------------------------------------ generic 2-D sheet optimisation (any quad topology)
def optimise_sheet3(Lo, p=E.CAND['E2'], it=600, ang_w=0.5, slide_w=0.5, win=0.6, verbose=False):
    """angle-based (Zhou-Shimada) + Laplacian smoothing of the FRONT sheet in the in-plane metric. Outline vertices slide along the outline
    (blend of neighbour-midpoint spacing and the orthogonal foot of their inward neighbours, weight slide_w on the foot); block corners,
    the junction ring J and the notch U are fixed. Back-sheet and rim copies take the front parameters. Updates Lo['st'] in place."""
    ip = E.InPlane(p); st = Lo['st']; part = Lo['part']; F = Lo['F']; fr = np.nonzero(part == 'front')[0]
    Ff = F[(part[F] == 'front').all(1)]; X = ip.flat(st[:, 0], st[:, 1]).copy(); nb = E._cyc_neighbors(Ff, len(st))
    so = np.linspace(0, 1, 4000); OL = np.r_[[[1.0, 0.0]], np.c_[so[::-1], -np.ones_like(so)], np.c_[so[1:], np.ones_like(so[1:])], [[1.0, 0.0]]]; OX = ip.flat(OL[:, 0], OL[:, 1])
    on_out = np.array([abs(abs(st[v, 1]) - 1) < 1e-9 or abs(st[v, 0] - 1) < 1e-9 or st[v, 0] < 1e-9 for v in range(len(st))]) & (part == 'front')
    cs = Lo['info']['corners']; fixed = np.zeros(len(st), bool)
    for k in ('c0', 'c1', 'c0f', 'c1f', 'P_lo', 'P_up', 'tip'): fixed[cs[k]] = True
    ukeys = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) for v, sg in zip(Lo['J'], Lo['Jseg']) if sg == 'U'}
    for v in Lo['J']: fixed[v] = True
    for v in fr:
        if (round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) in ukeys: fixed[v] = True
    if Lo['info'].get('fix_cut'): fixed[Lo['info']['cut_front']] = True              # the cut c1f -> P_up is a fixed feature line (like U)
    free_in = np.array([v for v in fr if not on_out[v] and not fixed[v]]); slide = np.array([v for v in fr if on_out[v] and not fixed[v]])
    otree = cKDTree(OX); OC = np.r_[0, np.cumsum(np.linalg.norm(np.diff(OX, axis=0), axis=1))]
    tau = {v: OC[otree.query(X[v])[1]] for v in np.nonzero(on_out)[0]}; tau[cs['tip']] = 0.0
    def stats():
        a = E._quad_angles2(X, Ff); return int(((a < 45) | (a > 135)).any(1).sum()), float(a.min()), float(a.max())
    s0 = stats()
    for k in range(it):
        Xn = X.copy()
        for v in free_in:
            ns = nb[v]; d = X[ns] - X[v]; order = np.argsort(np.arctan2(d[:, 1], d[:, 0])); ns = ns[order]; m = len(ns); cand = []
            for j in range(m):
                pj = X[ns[j]]; a1 = X[ns[(j - 1) % m]] - pj; a2 = X[ns[(j + 1) % m]] - pj; vv = X[v] - pj; L = np.linalg.norm(vv)
                bis = a1 / (np.linalg.norm(a1) + 1e-12) + a2 / (np.linalg.norm(a2) + 1e-12)
                if np.linalg.norm(bis) < 1e-9: cand.append(X[v]); continue
                bis /= np.linalg.norm(bis)
                if bis @ vv < 0: bis = -bis
                cand.append(pj + L * bis)
            Xn[v] = ang_w * np.mean(cand, 0) + (1 - ang_w) * X[ns].mean(0)
        tn = {}
        for v in slide:
            bnd = [w for w in nb[v] if on_out[w]]; ns = [w for w in nb[v] if not on_out[w]]
            tb = []
            for w in bnd:
                tw = tau[w]
                if w == cs['tip']: tw = 0.0 if tau[v] < 0.5 * OC[-1] else OC[-1]
                tb.append(tw)
            tm = 0.5 * (tb[0] + tb[1]) if len(tb) == 2 else tau[v]
            if ns:                                               # orthogonal foot, searched only along the local outline (same side of the ear)
                w0 = np.searchsorted(OC, tau[v] - win); w1 = np.searchsorted(OC, tau[v] + win)
                i = w0 + int(np.argmin(np.linalg.norm(OX[w0:w1] - X[ns].mean(0), axis=1))); tf = OC[i]
            else: tf = tm
            tn[v] = (1 - slide_w) * tm + slide_w * tf
        for v in slide:
            tau[v] = tn[v]; Xn[v] = np.array([np.interp(tau[v], OC, OX[:, 0]), np.interp(tau[v], OC, OX[:, 1])])
        X = Xn
        if verbose and k % 100 == 0: print(k, stats())
    s1 = stats()
    sd = np.linspace(0, 1, 801); td = np.linspace(-1.6, 1, 521); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1])); new = st.copy()
    if len(free_in): new[free_in], e = E._invert(X[free_in], ip, tree, G)
    for v in slide: i = int(np.argmin(np.abs(OC - tau[v]))); new[v] = OL[i]
    # back-sheet and rim copies follow their front vertex (same old parameters, or the same template tag)
    fkey = {}
    for key, v in Lo['idx'].items():
        if key[0] == 'front': fkey[key[1:]] = v
    for key, v in Lo['idx'].items():
        if key[0] == 'back' and key[1:] in fkey: new[v] = new[fkey[key[1:]]]
    for row in Lo['rim']:
        for r in row[1:-1]: new[r] = new[row[0]]
    Lo['st'] = new; Lo['info']['opt'] = dict(before=s0, after=s1, iterations=it, ang_w=ang_w, slide_w=slide_w); Lo['dbgX'] = X
    return Lo

# ------------------------------------------------------------------ quality pass: corner-angle energy, L-BFGS over free vertices (2-D or 3-D-tangent free)
def _angle_energy(X, Fo, lo, hi, nbr_i, nbr_j, mu):
    """X (n,2); Fo oriented CCW quads. E = sum relu(theta-hi)^2 + relu(lo-theta)^2 (degrees) + mu * sum |x - mean(nb)|^2; returns E, grad"""
    P = X[Fo]; E_ = 0.0; G = np.zeros_like(X)
    for k in range(4):
        pk = P[:, k]; w = P[:, (k + 1) % 4] - pk; u = P[:, (k - 1) % 4] - pk
        a = w[:, 0] * u[:, 1] - w[:, 1] * u[:, 0]; b = (w * u).sum(1); th = np.arctan2(a, b); th = np.where(th < 0, th + 2 * np.pi, th); thd = np.degrees(th)
        e_hi = np.maximum(thd - hi, 0); e_lo = np.maximum(lo - thd, 0); E_ += (e_hi ** 2 + e_lo ** 2).sum()
        dE = (2 * e_hi - 2 * e_lo) * (180 / np.pi)                                # dE / dtheta (rad)
        den = a * a + b * b + 1e-18; dth_da = b / den; dth_db = -a / den
        gw = (dth_da[:, None] * np.c_[u[:, 1], -u[:, 0]] + dth_db[:, None] * u) * dE[:, None]
        gu = (dth_da[:, None] * np.c_[-w[:, 1], w[:, 0]] + dth_db[:, None] * w) * dE[:, None]
        np.add.at(G, Fo[:, (k + 1) % 4], gw); np.add.at(G, Fo[:, (k - 1) % 4], gu); np.add.at(G, Fo[:, k], -gw - gu)
    if mu > 0:                                                                   # exact: E = mu |L X|^2, grad = 2 mu L^T L X (L = I - D^-1 A)
        Lm = nbr_i; D = Lm @ X; E_ += mu * (D ** 2).sum(); G += 2 * mu * (Lm.T @ D)
    if nbr_j is not None:                                                        # edge-length barrier: no edge below rho x its starting length
        ea, eb, l0, kap, rho, ks = nbr_j; d = X[ea] - X[eb]; l = np.linalg.norm(d, axis=1) + 1e-12; v = np.maximum(rho * l0 - l, 0) / l0
        r_ = l / l0 - 1                                                           # + ks * (l / l0 - 1)^2 : keep the local sizing
        E_ += kap * (v ** 2).sum() + ks * (r_ ** 2).sum(); gl = ((-2 * kap * v + 2 * ks * r_) / l0)[:, None] * d / l[:, None]
        np.add.at(G, ea, gl); np.add.at(G, eb, -gl)
    return E_, G

def quality_pass(X, F, free, lo=55.0, hi=125.0, mu=0.02, iters=400, ks=200.0):
    from scipy.optimize import minimize
    Fo = F.copy(); P = X[Fo]; ar = 0.5 * ((P[:, 0, 0] * P[:, 1, 1] - P[:, 1, 0] * P[:, 0, 1]) + (P[:, 1, 0] * P[:, 2, 1] - P[:, 2, 0] * P[:, 1, 1])
                                          + (P[:, 2, 0] * P[:, 3, 1] - P[:, 3, 0] * P[:, 2, 1]) + (P[:, 3, 0] * P[:, 0, 1] - P[:, 0, 0] * P[:, 3, 1]))
    Fo[ar < 0] = Fo[ar < 0][:, ::-1]
    import scipy.sparse as sp
    e = np.r_[Fo[:, [0, 1]], Fo[:, [1, 2]], Fo[:, [2, 3]], Fo[:, [3, 0]]]; e = np.unique(np.sort(e, 1), axis=0); n = len(X)
    A_ = sp.coo_matrix((np.ones(2 * len(e)), (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(n, n)).tocsr(); dg = np.asarray(A_.sum(1)).ravel()
    used = dg > 0; ni = (sp.diags(used.astype(float)) - sp.diags(np.where(used, 1 / np.maximum(dg, 1), 0)) @ A_).tocsr()
    nj = (e[:, 0], e[:, 1], np.linalg.norm(X[e[:, 0]] - X[e[:, 1]], axis=1) + 1e-9, 2.0e4, 0.5, ks)
    fi = np.nonzero(free)[0]; X0 = X.copy()
    def fun(z):
        Xc = X0.copy(); Xc[fi] = z.reshape(-1, 2); E_, G = _angle_energy(Xc, Fo, lo, hi, ni, nj, mu); return E_, G[fi].ravel()
    r = minimize(fun, X0[fi].ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=iters))
    Xn = X0.copy(); Xn[fi] = r.x.reshape(-1, 2); return Xn, dict(E0=float(fun(X0[fi].ravel())[0]), E1=float(r.fun), nit=int(r.nit))

def quality_sheet(Lo, p=E.CAND['E2'], lo=55.0, hi=125.0, mu=0.02, iters=400, ks=200.0, rings=2, flag=(50.0, 130.0)):
    """after optimise_sheet3: corner-angle energy pass on the front sheet in-plane (outline, J, U, corners fixed); back / rim copies follow"""
    ip = E.InPlane(p); st = Lo['st']; part = Lo['part']; F = Lo['F']; fr = part == 'front'; Ff = F[fr[F].all(1)]
    X = ip.flat(st[:, 0], st[:, 1]).copy(); on_out = np.array([abs(abs(st[v, 1]) - 1) < 1e-9 or abs(st[v, 0] - 1) < 1e-9 or st[v, 0] < 1e-9 for v in range(len(st))])
    fixed = on_out.copy(); cs = Lo['info']['corners']
    for k in cs.values(): fixed[k] = True
    ukeys = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) for v, sg in zip(Lo['J'], Lo['Jseg']) if sg == 'U'}
    for v in Lo['J']: fixed[v] = True
    for v in np.nonzero(fr)[0]:
        if (round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) in ukeys: fixed[v] = True
    if Lo['info'].get('fix_cut'): fixed[Lo['info']['cut_front']] = True
    used = np.zeros(len(st), bool); used[Ff.ravel()] = True
    a0 = E._quad_angles2(X, Ff); badf = ((a0 < flag[0]) | (a0 > flag[1])).any(1); loc = np.zeros(len(st), bool); loc[Ff[badf].ravel()] = True
    nbv = [set() for _ in range(len(st))]
    for q in Ff:
        for k in range(4): nbv[q[k]].update(q.tolist())
    for _ in range(rings):
        loc2 = loc.copy()
        for v in np.nonzero(loc)[0]: loc2[list(nbv[v])] = True
        loc = loc2
    free = used & fr & ~fixed & loc                                                # local: within `rings` vertex rings of a flagged face
    Xn, info = quality_pass(X, Ff, free, lo, hi, mu, iters, ks); a1 = E._quad_angles2(Xn, Ff)
    sd = np.linspace(0, 1, 801); td = np.linspace(-1.6, 1, 521); SS, TT = np.meshgrid(sd, td, indexing='ij'); G = np.c_[SS.ravel(), TT.ravel()]
    tree = cKDTree(ip.flat(G[:, 0], G[:, 1])); new = st.copy(); fi = np.nonzero(free)[0]
    new[fi], err = E._invert(Xn[fi], ip, tree, G)
    fkey = {key[1:]: v for key, v in Lo['idx'].items() if key[0] == 'front'}
    for key, v in Lo['idx'].items():
        if key[0] == 'back' and key[1:] in fkey: new[v] = new[fkey[key[1:]]]
    Lo['st'] = new; Lo['dbgX'] = Xn
    Lo['info']['quality'] = dict(info, lo=lo, hi=hi, mu=mu, ks=ks, rings=rings, free_vertices=int(free.sum()), before=int(((a0 < 45) | (a0 > 135)).any(1).sum()), after=int(((a1 < 45) | (a1 > 135)).any(1).sum()),
                                 min_angle=float(a1.min()), inv_err_max=float(err.max()))
    return Lo
