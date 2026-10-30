# surface_relax.py : relax a small set of vertices ON the frozen v005 surface (piecewise bilinear parent quads) to restore quad shape after a local
# re-quad. Each free vertex ends as a bilinear point (parent face, s, u) of one v005 quad -> an S row with <= 4 non-zeros (surface preserved by
# construction; the mesh is a re-sampling of the same surface). Objective per affected quad: corner angle deviation from 90 deg (hinge above 45-135),
# aspect above 2.5, and edge-length evenness; optional per-vertex constraints (e.g. pole t / h >= limit) as penalties.
import numpy as np
from scipy.optimize import minimize
def bil(P, s, u): return (1 - s) * (1 - u) * P[0] + s * (1 - u) * P[1] + s * u * P[2] + (1 - s) * u * P[3]
def closest_on_quad(P, x):
    best = None
    for s0 in np.linspace(0, 1, 7):
        for u0 in np.linspace(0, 1, 7):
            d = np.linalg.norm(bil(P, s0, u0) - x)
            if best is None or d < best[0]: best = (d, s0, u0)
    s, u = best[1], best[2]
    for _ in range(25):                                                               # projected Gauss-Newton on the bilinear patch
        r = bil(P, s, u) - x; ds = (1 - u) * (P[1] - P[0]) + u * (P[2] - P[3]); du = (1 - s) * (P[3] - P[0]) + s * (P[2] - P[1])
        J = np.stack([ds, du], 1); step = np.linalg.lstsq(J, -r, rcond=None)[0]; s = float(np.clip(s + step[0], 0, 1)); u = float(np.clip(u + step[1], 0, 1))
    return np.linalg.norm(bil(P, s, u) - x), s, u
class Surface:
    def __init__(s, V0, Q0, faces):
        s.V0 = V0; s.Q0 = np.asarray(Q0); s.faces = list(faces); s.C = np.array([V0[s.Q0[f]].mean(0) for f in s.faces])
    def project(s, x):
        order = np.argsort(np.linalg.norm(s.C - x, axis=1))[:8]; best = None
        for i in order:
            f = s.faces[i]; d, a, b = closest_on_quad(s.V0[s.Q0[f]], x)
            if best is None or d < best[0]: best = (d, f, a, b)
        return best                                                                   # (dist, parent face, s, u)
ANG_LO, ANG_HI, W_HINGE = 47.0, 133.0, 0.2
def quad_terms(V, Q):
    out = []
    for q in Q:
        P = V[q]
        for k in range(4):
            a = P[(k - 1) % 4] - P[k]; b = P[(k + 1) % 4] - P[k]; c = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)
            ang = np.degrees(np.arccos(np.clip(c, -1, 1))); out.append(0.02 * c * c + W_HINGE * max(0, ANG_LO - ang) ** 2 / 45 + W_HINGE * max(0, ang - ANG_HI) ** 2 / 45)
        L = np.linalg.norm(P - np.roll(P, -1, 0), axis=1); asp = L.max() / max(L.min(), 1e-9); out.append(0.5 * max(0, asp - 2.5) ** 2)
    return np.array(out)
def relax(V0, Q, free, surf, cons=None, iters=3):
    """free: vertex ids; Q: current quads (full); returns {vid: (face, s, u)} and new positions"""
    free = list(free); fset = set(free); aff = np.array([i for i, q in enumerate(Q) if any(int(x) in fset for x in q)]); Qa = np.asarray(Q)[aff]
    V = V0.copy(); h = np.median([np.linalg.norm(V[q[k]] - V[q[(k + 1) % 4]]) for q in Qa for k in range(4)])
    x = V[free].ravel()
    for _ in range(iters):                                                            # optimise in each vertex's tangent plane, then project exactly
        P0 = x.reshape(-1, 3); T = []
        for v, p in zip(free, P0):
            fs = [q for q in Qa if int(v) in [int(t) for t in q]]; n = np.zeros(3)
            for q in fs: n += np.cross(V[q[2]] - V[q[0]], V[q[3]] - V[q[1]])
            n /= np.linalg.norm(n); t1 = np.cross(n, [0, 0, 1.0]) if abs(n[2]) < 0.9 else np.cross(n, [1.0, 0, 0]); t1 /= np.linalg.norm(t1); T.append((t1, np.cross(n, t1)))
        def pos(y):
            y = y.reshape(-1, 2); return P0 + np.array([a * t[0] + b * t[1] for (a, b), t in zip(y, T)])
        def E(y):
            Vt = V.copy(); Vt[free] = pos(y); e = quad_terms(Vt, Qa).sum() + 0.01 * (y ** 2).sum() / h ** 2
            if cons: e += sum(c(Vt) for c in cons)
            return e
        r = minimize(E, np.zeros(2 * len(free)), method='L-BFGS-B', options=dict(maxiter=3000))
        P = pos(r.x); proj = [surf.project(p) for p in P]; x = np.array([bil(V0[np.asarray(surf.Q0)[pr[1]]], pr[2], pr[3]) for pr in proj]).ravel()
        V[free] = x.reshape(-1, 3)
    res = {}
    for v, pr in zip(free, [surf.project(p) for p in x.reshape(-1, 3)]): res[int(v)] = (int(pr[1]), round(float(pr[2]), 6), round(float(pr[3]), 6))
    Vn = V.copy()
    for v, (f, a, b) in res.items(): Vn[v] = bil(V0[np.asarray(surf.Q0)[f]], a, b)
    return res, Vn
