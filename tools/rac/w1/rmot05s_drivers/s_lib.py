# RM-OT-05S shared geometry: the 05Q arm-local frame, half-plane profile columns of a mesh, and the (theta, arclength)
# chart used to address the band-to-axilla interface explicitly (vertex / face selection by profile position).
import json, numpy as np

class Frame:
    def __init__(self, sel_json):
        J = json.load(open(sel_json)); self.J = J
        self.O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); self.d = d / np.linalg.norm(d)
        e1 = np.cross([0, 1, 0], self.d); self.e1 = e1 / np.linalg.norm(e1); self.e2 = np.cross(self.d, self.e1)
        self.lt, self.slo, self.shi = np.array(J['ledge_theta']), np.array(J['s_lo']), np.array(J['s_hi']); self.ta, self.tb = J['sector_theta_deg']
    def tsr(self, X):
        c = np.atleast_2d(X) - self.O; return np.degrees(np.arctan2(c @ self.e2, c @ self.e1)), c @ self.d, np.hypot(c @ self.e1, c @ self.e2)
    def dirs(self, th):
        t = np.radians(th); return np.cos(t) * self.e1 + np.sin(t) * self.e2, -np.sin(t) * self.e1 + np.cos(t) * self.e2   # radial, plane normal
    def to3(self, th, s, r):
        rad, _ = self.dirs(th); return self.O + np.outer(np.atleast_1d(s), self.d) + np.outer(np.atleast_1d(r), rad)

def profile(fr, V, F, th, ref_rs, box=26.0):
    """Half-plane (r > 0) section of mesh (V, F) at angle th, as ONE ordered polyline in (r, s): the connected chain
    containing the segment nearest ref_rs = (r, s). Returns (P (n,2) ordered from low s end on the ref side upward,
    face index per segment (n-1,)) or (None, None)."""
    rad, nrm = fr.dirs(th); sd = (V - fr.O) @ nrm
    near = np.abs(V[F] - fr.O).max((1, 2)) < box; T = np.where(near)[0]; sv = sd[F[T]]
    cr = T[(sv.min(1) < 0) & (sv.max(1) > 0)]
    if not len(cr): return None, None
    segs = []; keys = []; fids = []
    for f in cr:
        pts = []; ks = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a, b = F[f, i], F[f, j]
            if (sd[a] < 0) != (sd[b] < 0):
                t = sd[a] / (sd[a] - sd[b]); p = V[a] + t * (V[b] - V[a]); c = p - fr.O; pts.append((c @ rad, c @ fr.d)); ks.append((min(a, b), max(a, b)))
        if len(pts) == 2 and pts[0][0] > 0 and pts[1][0] > 0: segs.append(pts); keys.append(ks); fids.append(f)
    if not segs: return None, None
    adj = {}
    for i, ks in enumerate(keys):
        for k in ks: adj.setdefault(k, []).append(i)
    mid = np.array([[(p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2] for p in segs]); s0 = int(np.argmin(np.linalg.norm(mid - np.array(ref_rs), axis=1)))
    # walk both directions from s0
    def walk(start, via):
        out = []; cur = start; k = via
        while True:
            nx = [j for j in adj[k] if j != cur]
            if not nx: break
            cur = nx[0]
            if cur in seen: break
            seen.add(cur); out.append(cur); k = keys[cur][1] if keys[cur][0] == k else keys[cur][0]
        return out
    seen = {s0}; fwd = walk(s0, keys[s0][1]); bwd = walk(s0, keys[s0][0])
    order = bwd[::-1] + [s0] + fwd
    # point list: start at the end of the first segment that is not shared with the second, then walk
    i = order[0]
    if len(order) > 1:
        sh = [k for k in keys[i] if k in keys[order[1]]][0]; cur_k = keys[i][0] if keys[i][1] == sh else keys[i][1]
    else:
        cur_k = keys[i][0]
    pts = []
    for i in order:
        a_k, b_k = keys[i]; pa, pb = segs[i]
        if a_k == cur_k: pts.append(pa); cur_k = b_k; last = pb
        else: pts.append(pb); cur_k = a_k; last = pa
    pts.append(last)
    P = np.array(pts, float); fid = np.array([fids[i] for i in order])
    if P[0, 1] > P[-1, 1]: P = P[::-1]; fid = fid[::-1]
    return P, fid

def arclen(P):
    return np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]

def at_len(P, L, l):
    return np.c_[np.interp(l, L, P[:, 0]), np.interp(l, L, P[:, 1])]

def project(P, L, q):
    """closest point of polyline P to q (r, s): returns (arclength, distance)"""
    A = P[:-1]; B = P[1:]; AB = B - A; t = np.clip(((q - A) * AB).sum(1) / np.maximum((AB * AB).sum(1), 1e-12), 0, 1)
    C = A + t[:, None] * AB; dd = np.linalg.norm(C - q, axis=1); i = int(np.argmin(dd)); return L[i] + t[i] * np.linalg.norm(AB[i]), dd[i]

def chart_points(fr, V, F, X, D, colcache, step=0.25):
    """chart coordinates (theta, l - lA) for 3-D points X lying on the mesh (V, F), using design columns D (s_design)"""
    th = D['theta']; lo = th.min(); t_, s_, r_ = fr.tsr(X); out = np.zeros((len(X), 2)); dist = np.zeros(len(X))
    for i in range(len(X)):
        k = int(np.clip(np.round((t_[i] - lo) / step), 0, len(th) - 1))
        if k not in colcache: colcache[k] = profile(fr, V, F, th[k], (8.0, D['s_led'][k] - 4.0))[0]
        P = colcache[k]; L = arclen(P); rad, _ = fr.dirs(th[k]); q = np.array([(X[i] - fr.O) @ rad, (X[i] - fr.O) @ fr.d])
        l, dd = project(P, L, q); out[i] = (t_[i], l - D['lA'][k]); dist[i] = dd
    return out, dist

def simple_polygon_crossings(P):
    m = len(P); n = 0
    for i in range(m):
        p1, p2 = P[i], P[(i + 1) % m]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1: continue
            p3, p4 = P[j], P[(j + 1) % m]
            d1 = np.cross(p2 - p1, p3 - p1); d2 = np.cross(p2 - p1, p4 - p1); d3 = np.cross(p4 - p3, p1 - p3); d4 = np.cross(p4 - p3, p2 - p3)
            n += int(d1 * d2 < 0 and d3 * d4 < 0)
    return n
