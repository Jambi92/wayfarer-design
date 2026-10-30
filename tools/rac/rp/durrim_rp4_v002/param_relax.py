# param_relax.py : joint multi-body relaxation of branch vertices in SHARED parent-surface parameters.
# Each free vertex v is a bilinear point (parent face f_v, s_v, u_v) of the frozen v005 quads -- the same (f, s, u) for every body, so every
# realization gets the same S rows (deterministic branch map) and every vertex lies on that body's own v005 surface (surface preserved).
# Objective = sum over bodies of vectorised quad-shape terms of the affected quads (angle hinge outside [lo, hi], cos^2, aspect above amax)
# + user penalty terms (e.g. ring windows, pole offsets). Faces are re-assigned between rounds when (s, u) reaches a face edge (hop to the
# neighbouring parent face through that edge, re-projected on the reference body).
import numpy as np
from scipy.optimize import minimize
import surface_relax as SR
def bilw(s, u): return np.stack([(1 - s) * (1 - u), s * (1 - u), s * u, (1 - s) * u], -1)
class Bodies:
    def __init__(s, Vs, Q0): s.Vs = [np.asarray(V, float) for V in Vs]; s.Q0 = np.asarray(Q0)
    def pos(s, b, F, S, U): return (bilw(S, U)[..., None] * s.Vs[b][s.Q0[F]]).sum(-2)
def shape_terms(P, lo=47.0, hi=133.0, amax=3.8, wh=0.2):
    """P: (nq, 4, 3) quad corners -> per-quad energy (vectorised)"""
    a = np.roll(P, 1, 1) - P; b = np.roll(P, -1, 1) - P
    c = (a * b).sum(-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1) + 1e-12); ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
    L = np.linalg.norm(P - np.roll(P, -1, 1), axis=-1); asp = L.max(1) / np.maximum(L.min(1), 1e-9)
    return (0.02 * c * c + wh * np.clip(lo - ang, 0, None) ** 2 / 45 + wh * np.clip(ang - hi, 0, None) ** 2 / 45).sum(1) + 2.0 * np.clip(asp - amax, 0, None) ** 2
def relax(B, Q, base, free, init, penalty=None, rounds=4, weights=None, lo=47.0, hi=133.0, amax=3.8, maxiter=400, verbose=False, pin=None):
    """B: Bodies; Q: new quads (full); base: per-body positions of all vertices (list of arrays, used for non-free vertices);
    free: vertex ids; init: {v: (f, s, u)}. Returns {v: (f, s, u)}."""
    free = list(free); fi = {v: i for i, v in enumerate(free)}; Q = np.asarray(Q); fs = set(free)
    aff = np.array([i for i, q in enumerate(Q) if any(int(x) in fs for x in q)]); Qa = Q[aff]
    par = {v: tuple(init[v]) for v in free}; nb = len(B.Vs); w = weights or [1.0] * nb
    def qn(P): n = np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 1]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
    NREF = []
    for b in range(nb):
        F0 = np.array([par[v][0] for v in free]); P = base[b][Qa].copy(); mk = np.array([[int(x) in fs for x in q] for q in Qa]); ix = np.array([[fi.get(int(x), -1) for x in q] for q in Qa])
        Pv = B.pos(b, F0, np.array([par[v][1] for v in free]), np.array([par[v][2] for v in free])); P[mk] = Pv[ix[mk]]; NREF.append(qn(P))
    FOV = {}; FOV_SET = [set(int(x) for x in q) for q in B.Q0]
    for g, q in enumerate(B.Q0):
        for x in q: FOV.setdefault(int(x), []).append(g)
    for rd in range(rounds):
        F = np.array([par[v][0] for v in free]); x0 = np.array([[par[v][1], par[v][2]] for v in free]).ravel()
        mask = np.array([[int(x) in fs for x in q] for q in Qa]); idx = np.array([[fi.get(int(x), -1) for x in q] for q in Qa])
        def E(x):
            S, U = x[0::2], x[1::2]; e = 0.0; Ps = []
            for b in range(nb):
                Pv = B.pos(b, F, S, U); P = base[b][Qa].copy(); P[mask] = Pv[idx[mask]]; Ps.append(P); e += w[b] * shape_terms(P, lo, hi, amax).sum() + 20 * (np.clip(0.5 - (qn(P) * NREF[b]).sum(1), 0, None) ** 2).sum()
            if penalty: e += penalty(free, F, S, U, B)
            return e
        bnds = [(0, 1)] * len(x0)
        for v, pv in (pin or {}).items():                                              # seam vertices: one coordinate fixed (slide along the seam edge only) or fully fixed
            if v not in fi: continue
            if pv == 'fix':
                for ci in (0, 1): bnds[2 * fi[v] + ci] = (x0[2 * fi[v] + ci], x0[2 * fi[v] + ci])
            elif pv[0] == 'box':                                                       # ('box', fixed coord, value, free-coord lo, hi): slide along an edge inside a range
                _, ci, val, lo_, hi_ = pv; bnds[2 * fi[v] + ci] = (val, val); x0[2 * fi[v] + ci] = val; bnds[2 * fi[v] + 1 - ci] = (lo_, hi_)
                x0[2 * fi[v] + 1 - ci] = min(max(x0[2 * fi[v] + 1 - ci], lo_), hi_)
            else: ci, val = pv; bnds[2 * fi[v] + ci] = (val, val); x0[2 * fi[v] + ci] = val
        r = minimize(E, x0, method='L-BFGS-B', bounds=bnds, options=dict(maxiter=maxiter, maxfun=maxiter * 60))
        S, U = r.x[0::2], r.x[1::2]; hop = 0
        Pcur = base[0].copy(); Pcur[free] = B.pos(0, F, S, U)
        for i, v in enumerate(free):
            f, s, u = int(F[i]), float(S[i]), float(U[i])
            if (min(s, u) < 1e-4 or max(s, u) > 1 - 1e-4) and v not in (pin or {}):    # on a face edge / corner: cross into the neighbouring parent face
                p = B.pos(0, np.array([f]), np.array([s]), np.array([u]))[0]; w4 = bilw(np.array(s), np.array(u)); sup = [int(B.Q0[f][k]) for k in range(4) if w4[k] > 1e-6]
                cands = [g for g in FOV[sup[0]] if g != f and all(x in FOV_SET[g] for x in sup)]
                nbr = [int(x) for q in Qa for k, x in enumerate(q) if int(q[(k + 1) % 4]) == v or int(q[(k - 1) % 4]) == v]
                tgt = np.mean([Pcur[x] for x in nbr], 0) if nbr else p; best = (1e9, f, s, u)
                for g in cands:
                    d, a, b2 = SR.closest_on_quad(B.Vs[0][B.Q0[g]], p)
                    if d < 1e-5:
                        sc = np.linalg.norm(B.Vs[0][B.Q0[g]].mean(0) - tgt)
                        if sc < best[0]: best = (sc, g, a, b2)
                if best[1] != f: hop += 1
                par[v] = (int(best[1]), float(best[2]), float(best[3]))
            else: par[v] = (f, s, u)
        if verbose: print('round', rd, 'E %.4f' % r.fun, 'hops', hop, flush=True)
        if hop == 0 and rd > 0: break
    return par
