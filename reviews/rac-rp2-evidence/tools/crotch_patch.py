# crotch_patch.py: replace the MPFB crotch region (S* hidden perineal lens + 2 rings, mirror-closed) by a symmetric quad patch
# (two 3 x 21 Coons grids meeting on the x = 0 crease seam) lying on the visible envelope of S*.
import sys, numpy as np, igl
sys.path.insert(0, '/tmp/claude-0/rp2'); sys.path.insert(0, '/tmp/claude-0/rp2/tools')
from xsec import sec; from crotch_region import loops; from hidden import hidden_quads
R_ = '/tmp/claude-0/rp2/'
def build(M=3, N=21, ring_file='crR_2.npy', relax=40):
    z = np.load(R_ + 'sstar.npz'); V = z['V']; Q = z['Q']; m = np.load(R_ + 'mir_body.npy'); W2 = np.load(R_ + 'w2_body.npz')['V']
    R = np.load(R_ + ring_file); L = np.array(loops(Q, R)[0]); n = len(L)
    ap = [i for i, v in enumerate(L) if m[v] == v]; a0, a1 = ap
    arcA = [L[(a0 + k) % n] for k in range((a1 - a0) % n + 1)]
    if V[arcA[1:-1], 0].mean() < 0: a0, a1 = a1, a0; arcA = [L[(a0 + k) % n] for k in range((a1 - a0) % n + 1)]
    arc = np.array(arcA)                       # left arc (x > 0), from apex a0 to apex a1 in loop orientation
    K = len(arc) - 1; assert K == 2 * M + N, (K, M, N)
    back_first = V[arc[0], 1] < V[arc[-1], 1]
    # envelope
    T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; hq, sgn, ht = hidden_quads(V, Q); vis = ~ht
    labT = np.sign(np.round(W2[T][:, :, 0].mean(1), 2))
    TL = T[vis & (labT >= 0) & (V[T][:, :, 0].min(1) >= -0.01)]
    # seam: lower envelope of the x = 0 section of visible faces between the two apex f's
    Cz = V[T].mean(1); S = sec(V, T[(Cz[:, 2] < 125) & (Cz[:, 2] > 100) & (np.abs(Cz[:, 0]) < 8)], 0, 0.0); pts = S.reshape(-1, 2)          # (f, u)
    f0, f1 = V[arc[0], 1], V[arc[-1], 1]
    fs = np.linspace(f0, f1, 400); us = []
    for f in fs:
        # intersect each segment with vertical line f
        a, b = S[:, 0], S[:, 1]; t = (f - a[:, 0]) / (b[:, 0] - a[:, 0] + 1e-12); ok = (t >= 0) & (t <= 1)
        u = a[ok, 1] + t[ok] * (b[ok, 1] - a[ok, 1]); us.append(u.min() if len(u) else np.nan)
    us = np.array(us); good = ~np.isnan(us)
    cur = np.c_[np.zeros(good.sum()), fs[good], us[good]]
    cur[0] = V[arc[0]]; cur[-1] = V[arc[-1]]
    cl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(cur, axis=0), axis=1))]
    tt = np.linspace(0, cl[-1], N + 1); seam = np.stack([np.interp(tt, cl, cur[:, k]) for k in range(3)], 1); seam[:, 0] = 0.0
    # boundary curves (grid i = 0 seam ... M lateral, j = 0 at arc[0] ... N at arc[-1])
    d0 = V[arc[0:M + 1]]                       # j = 0 side, i = 0..M
    c1 = V[arc[M:M + N + 1]]                   # i = M side, j = 0..N
    d1 = V[arc[M + N:][::-1]]                  # j = N side, i = 0..M
    G = np.zeros((M + 1, N + 1, 3))
    for i in range(M + 1):
        for j in range(N + 1):
            s, t = i / M, j / N
            G[i, j] = (1 - s) * seam[j] + s * c1[j] + (1 - t) * d0[i] + t * d1[i] \
                - ((1 - s) * (1 - t) * seam[0] + s * (1 - t) * c1[0] + (1 - s) * t * seam[N] + s * t * c1[N])
    G[0, :] = seam; G[M, :] = c1; G[:, 0] = d0; G[:, N] = d1
    inner = np.zeros((M + 1, N + 1), bool); inner[1:M, 1:N] = True
    for it in range(relax):
        Gn = G.copy()
        Gn[1:M, 1:N] = 0.25 * (G[:-2, 1:N] + G[2:, 1:N] + G[1:M, :-2] + G[1:M, 2:])
        G = 0.5 * G + 0.5 * Gn
        P = G[inner]; d, fi, cp = igl.point_mesh_squared_distance(P, V, TL); cp[:, 0] = np.maximum(cp[:, 0], 0.02); G[inner] = cp
    return dict(V=V, Q=Q, R=R, arc=arc, M=M, N=N, G=G, seam=seam, back_first=back_first, m=m, crease=cur)
def assemble(B):
    V, Q, R, arc, M, N, G, m = B['V'], B['Q'], B['R'], B['arc'], B['M'], B['N'], B['G'], B['m']
    keepQ = ~R; used = np.zeros(len(V), bool); used[Q[keepQ].ravel()] = True
    bnd = set(arc.tolist()) | set(m[arc].tolist())
    o2n = -np.ones(len(V), int); o2n[used] = np.arange(used.sum()); nv = used.sum()
    newV = [V[used]]; idxL = -np.ones((M + 1, N + 1), int); idxR = -np.ones((M + 1, N + 1), int)
    # boundary grid nodes reuse existing vertices
    for i in range(M + 1): idxL[i, 0] = o2n[arc[i]]; idxL[i, N] = o2n[arc[2 * M + N - i]]
    for j in range(N + 1): idxL[M, j] = o2n[arc[M + j]]
    idxL[0, 0] = o2n[arc[0]]; idxL[0, N] = o2n[arc[-1]]
    for i in range(M + 1):
        for j in (0, N): idxR[i, j] = o2n[m[arc[i if j == 0 else 2 * M + N - i]]]
    for j in range(N + 1): idxR[M, j] = o2n[m[arc[M + j]]]
    add = []
    for j in range(1, N):                     # seam (shared)
        idxL[0, j] = idxR[0, j] = nv + len(add); add.append(G[0, j])
    for i in range(1, M):
        for j in range(1, N):
            idxL[i, j] = nv + len(add); add.append(G[i, j])
            idxR[i, j] = nv + len(add); add.append(G[i, j] * np.array([-1, 1, 1]))
    Vn = np.vstack([V[used], np.array(add)]); Qn = [o2n[Q[keepQ]]]
    qa = []; qb = []
    for i in range(M):
        for j in range(N):
            qa.append([idxL[i, j], idxL[i + 1, j], idxL[i + 1, j + 1], idxL[i, j + 1]])
            qb.append([idxR[i, j], idxR[i, j + 1], idxR[i + 1, j + 1], idxR[i + 1, j]])
    Qn = np.vstack([Qn[0], np.array(qa), np.array(qb)])
    assert (Qn >= 0).all()
    # mirror map for the new vertex set
    mn = -np.ones(len(Vn), int); mn[o2n[used]] = o2n[m[used]] if True else None
    for i in range(M + 1):
        for j in range(N + 1): mn[idxL[i, j]] = idxR[i, j]; mn[idxR[i, j]] = idxL[i, j]
    return Vn, Qn, mn, o2n, used, idxL[0, :].copy()
