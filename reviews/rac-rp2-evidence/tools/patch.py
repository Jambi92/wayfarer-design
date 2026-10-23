# patch.py: generic "seam patch" for a hidden contact lens. A region R (quads) is removed; its boundary loop splits at two apexes
# into arc A and arc B (loop order); each side gets an M x N Coons grid between its arc and a shared seam that follows the visible
# crease; interior nodes are relaxed and kept on that side's visible envelope faces.
import numpy as np, igl
from crotch_region import loops
def grid(arc, seam, M, N):
    """arc: (2M+N+1,3) loop-ordered from seam[0] to seam[N]; seam (N+1,3) from arc[0] to arc[-1]"""
    d0 = arc[0:M + 1]; c1 = arc[M:M + N + 1]; d1 = arc[M + N:][::-1]
    G = np.zeros((M + 1, N + 1, 3))
    for i in range(M + 1):
        for j in range(N + 1):
            s, t = i / M, j / N
            G[i, j] = (1 - s) * seam[j] + s * c1[j] + (1 - t) * d0[i] + t * d1[i] - (
                (1 - s) * (1 - t) * seam[0] + s * (1 - t) * c1[0] + (1 - s) * t * seam[N] + s * t * c1[N])
    G[0, :] = seam; G[M, :] = c1; G[:, 0] = d0; G[:, N] = d1
    return G
def relax(G, Venv, Tenv, iters=40, clampx=None):
    M, N = G.shape[0] - 1, G.shape[1] - 1
    for it in range(iters):
        Gn = G.copy(); Gn[1:M, 1:N] = 0.25 * (G[:-2, 1:N] + G[2:, 1:N] + G[1:M, :-2] + G[1:M, 2:])
        G = 0.5 * G + 0.5 * Gn
        P = G[1:M, 1:N].reshape(-1, 3); d, fi, cp = igl.point_mesh_squared_distance(P, Venv, Tenv)
        if clampx is not None: cp = clampx(cp)
        G[1:M, 1:N] = cp.reshape(M - 1, N - 1, 3)
    return G
def resample(poly, N):
    cl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(poly, axis=0), axis=1))]; tt = np.linspace(0, cl[-1], N + 1)
    return np.stack([np.interp(tt, cl, poly[:, k]) for k in range(3)], 1)
class Patch:
    def __init__(self, R, arcA, arcB, GA, GB):
        self.R, self.arcA, self.arcB, self.GA, self.GB = R, arcA, arcB, GA, GB
def build_patch(V, Q, R, sideA, seam_poly, N, envA, envB, Venv, iters=40, clampA=None, clampB=None):
    L = np.array(loops(Q, R)[0]); n = len(L); a = sideA[L]
    ch = [i for i in range(n) if a[i] != a[i - 1]]; assert len(ch) == 2, ch
    # apexes: the side-B vertex at each transition
    p = [i if not a[i] else (i - 1) % n for i in ch]
    # arc A: from one apex through the side-A run to the other apex (loop order)
    def run(s, e): return [L[(s + k) % n] for k in range((e - s) % n + 1)]
    r1 = run(p[0], p[1]); r2 = run(p[1], p[0])
    arcA, arcB = (r1, r2) if sideA[r1[1:-1]].mean() > sideA[r2[1:-1]].mean() else (r2, r1)
    KA, KB = len(arcA) - 1, len(arcB) - 1; MA, MB = (KA - N) // 2, (KB - N) // 2
    assert (KA - N) % 2 == 0 and (KB - N) % 2 == 0 and MA >= 1 and MB >= 1, (KA, KB, N)
    seam = resample(np.vstack([V[arcA[0]], seam_poly, V[arcA[-1]]]) if np.linalg.norm(seam_poly[0] - V[arcA[0]]) < np.linalg.norm(seam_poly[-1] - V[arcA[0]])
                    else np.vstack([V[arcA[0]], seam_poly[::-1], V[arcA[-1]]]), N)
    GA = relax(grid(V[arcA], seam, MA, N), Venv, envA, iters, clampA)
    GB = relax(grid(V[arcB], seam[::-1], MB, N), Venv, envB, iters, clampB)
    return Patch(R, np.array(arcA), np.array(arcB), GA, GB)
def apply(V, Q, patches):
    """remove every patch region, add the grids. returns V2, Q2, o2n"""
    seams = []
    Rall = np.zeros(len(Q), bool)
    for P in patches: Rall |= P.R
    used = np.zeros(len(V), bool); used[Q[~Rall].ravel()] = True
    o2n = -np.ones(len(V), int); o2n[used] = np.arange(used.sum()); Vl = [V[used]]; nv = used.sum(); Ql = [o2n[Q[~Rall]]]
    for P in patches:
        idx = {}
        for tag, G, arc in (('A', P.GA, P.arcA), ('B', P.GB, P.arcB)):
            M, N = G.shape[0] - 1, G.shape[1] - 1; I = -np.ones((M + 1, N + 1), int)
            for i in range(M + 1): I[i, 0] = o2n[arc[i]]; I[i, N] = o2n[arc[2 * M + N - i]]
            for j in range(N + 1): I[M, j] = o2n[arc[M + j]]
            idx[tag] = I
        NA = P.GA.shape[1] - 1
        for j in range(1, NA):                                   # shared seam: A[0,j] == B[0,N-j]
            idx['A'][0, j] = nv; idx['B'][0, NA - j] = nv; Vl.append(P.GA[0, j][None]); nv += 1
        for tag, G in (('A', P.GA), ('B', P.GB)):
            I = idx[tag]; M, N = G.shape[0] - 1, G.shape[1] - 1
            for i in range(1, M):
                for j in range(1, N): I[i, j] = nv; Vl.append(G[i, j][None]); nv += 1
            q = [[I[i, j], I[i + 1, j], I[i + 1, j + 1], I[i, j + 1]] for i in range(M) for j in range(N)]
            Ql.append(np.array(q))
        assert all((v >= 0).all() for v in idx.values()); seams.append(idx['A'][0, :].copy())
    return np.vstack(Vl), np.vstack(Ql), o2n, seams
def mirror_map(V, tol=1e-4):
    from scipy.spatial import cKDTree
    d, j = cKDTree(V).query(V * np.array([-1, 1, 1])); m = np.where(d < tol, j, -1); return m
