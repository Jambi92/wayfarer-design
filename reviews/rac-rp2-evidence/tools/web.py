# web.py : vertex-only resolution of a crossing-sheet lens (MPFB topology unchanged). The hidden vertices of both sheets and of the
# bridge strip that closes the pocket are moved into a narrow "web" that fills the tip of the visible V between the two sheets just
# outside the crease: the crease curve c(s) is the intersection of the sheets; the web is spanned by the air bisector a(s) and the
# cross direction e(s) (from sheet B toward sheet A); sheet-A rows sit at +e, sheet-B rows at -e, the bridge at the web bottom.
import numpy as np, igl, scipy.sparse as sp
AIRSIGN = 1.0
def onpoly(X, c):
    A_ = c[:-1]; B_ = c[1:]; AB = B_ - A_; L2 = (AB ** 2).sum(1) + 1e-12
    Y = X[:, None, :] - A_[None]; t = np.clip((Y * AB[None]).sum(2) / L2[None], 0, 1); Cp = A_[None] + t[:, :, None] * AB[None]
    k = ((X[:, None, :] - Cp) ** 2).sum(2).argmin(1); return Cp[np.arange(len(X)), k], k
def graph_rank(Q, n, src_mask, allowed):
    E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
    A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr()
    r = np.full(n, -1); r[src_mask] = 0; front = src_mask.copy(); k = 0
    while True:
        k += 1; nxt = (A @ front.astype(float) > 0) & allowed & (r < 0)
        if not nxt.any(): break
        r[nxt] = k; front = nxt
    return r
def make_web(V, Q, hidden, sideA, sideB, bridge, crease, nA_fun, nB_fun, g=0.3, eps=0.04):
    """hidden: bool (n,) vertices to move; sideA/sideB/bridge: bool labels; crease: (k,3) polyline;
       nA_fun/nB_fun(points)->outward normals of sheet A / B at those crease points"""
    n = len(V); P = V.copy()
    visA = sideA & ~hidden; visB = sideB & ~hidden
    rA = graph_rank(Q, n, visA, hidden & (sideA | bridge)); rB = graph_rank(Q, n, visB, hidden & (sideB | bridge))
    idx = np.where(hidden)[0]
    c, _ = onpoly(V[idx], crease)
    nA = nA_fun(c); nB = nB_fun(c)
    a = nA + nB; a /= np.linalg.norm(a, axis=1)[:, None] + 1e-12; a = a * AIRSIGN
    e = nB - nA; e -= (e * a).sum(1)[:, None] * a; e /= np.linalg.norm(e, axis=1)[:, None] + 1e-12   # points from A-wall side toward... (A wall at -e*?)
    KA = max(1, rA[hidden & sideA].max(initial=1)); KB = max(1, rB[hidden & sideB].max(initial=1))
    for j, v in enumerate(idx):
        if bridge[v]: t = 1.0; off = 0.0
        elif sideA[v]: t = min(1.0, rA[v] / (KA + 1)); off = -eps * (1 - t)
        else: t = min(1.0, rB[v] / (KB + 1)); off = +eps * (1 - t)
        P[v] = c[j] + a[j] * g * t + e[j] * off
    return P, rA, rB
