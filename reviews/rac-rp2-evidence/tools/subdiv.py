# subdiv.py: quad-mesh linear (bilinear) subdivision with exact parametric mapping to the base mesh and mirror-map propagation
import numpy as np
def subdivide(Q, n, mirror=None):
    """one level. Q (m,4) quads over n verts. returns Q2, n2, parent info: for each new vertex (kind, ids):
       kind 0 = old vertex v ; 1 = edge point (a,b) ; 2 = face point (quad q). mirror (n,) -> mirror2 (n2,) (-1 if undefined)"""
    m = len(Q); E = np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]); key = np.sort(E, 1)
    u, inv = np.unique(key, axis=0, return_inverse=True); ne = len(u)
    eid = inv.reshape(4, m).T                       # eid[q, i] = edge (Q[q,i], Q[q,i+1])
    fpt = n + ne + np.arange(m); ept = n + eid
    Q2 = []
    for i in range(4):
        a = Q[:, i]; e_next = ept[:, i]; e_prev = ept[:, (i - 1) % 4]
        Q2.append(np.stack([a, e_next, fpt, e_prev], 1))
    Q2 = np.stack(Q2, 1).reshape(-1, 4)
    n2 = n + ne + m
    mir2 = None
    if mirror is not None:
        mir2 = -np.ones(n2, int); mir2[:n] = mirror
        ek = {tuple(e): i for i, e in enumerate(u.tolist())}
        mu = np.sort(np.where((mirror[u] >= 0).all(1)[:, None], mirror[u], -1), 1)
        for i, e in enumerate(mu.tolist()):
            j = ek.get(tuple(e)) if e[0] >= 0 else None
            if j is not None: mir2[n + i] = n + j
        fk = {frozenset(q): i for i, q in enumerate(Q.tolist())}
        for i, q in enumerate(Q.tolist()):
            mq = [mirror[x] for x in q]
            if min(mq) >= 0:
                j = fk.get(frozenset(mq))
                if j is not None: mir2[n + ne + i] = n + ne + j
    return Q2, n2, u, mir2
def param_subdivide(Q, P, n, U):
    """P: (n,) base quad id per vertex, U: (n,2) param. returns params for the new vertex set (same order as subdivide)."""
    m = len(Q); E = np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]); key = np.sort(E, 1)
    u, inv = np.unique(key, axis=0, return_inverse=True)
    return u

import scipy.sparse as sp
def interp_matrix(Q, n, u):
    """sparse (n2 x n) linear subdivision operator for subdivide()'s vertex order"""
    m = len(Q); ne = len(u); rows = [np.arange(n)]; cols = [np.arange(n)]; vals = [np.ones(n)]
    rows += [n + np.arange(ne)] * 2; cols += [u[:, 0], u[:, 1]]; vals += [np.full(ne, .5)] * 2
    for i in range(4): rows.append(n + ne + np.arange(m)); cols.append(Q[:, i]); vals.append(np.full(m, .25))
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n + ne + m, n))
def subdivide_levels(Q, n, levels, mirror=None):
    S = sp.identity(n, format='csr'); Qc, nc, mc = Q, n, mirror
    for _ in range(levels):
        Q2, n2, u, m2 = subdivide(Qc, nc, mc); S = interp_matrix(Qc, nc, u) @ S; Qc, nc, mc = Q2, n2, m2
    return Qc, nc, S, mc
