# sa_geo.py : RP5 full-cage geometry helpers -- the SA_RP5_WORK_v001 SA-M188 working surface (cm, x right(subject left = +x), f forward, u up), plane-section
# loops, ray / loop intersections, mesh-graph shortest paths with blocking, closest-point embedding (triangle + barycentric).
import os, json, numpy as np, igl, scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import dijkstra
W = os.environ.get('SA_W', '/tmp/claude-0/rt/sa')
_z = np.load(W + '/work/SA_RP5_WORK_v001.npz'); V = _z['v_M'].astype(float); VF2 = _z['v_F'].astype(float); F = _z['f'].astype(np.int64)
NV = len(V); KD = cKDTree(V)
E = igl.edges(F); EL = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
G = sp.coo_matrix((np.r_[EL, EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(NV, NV)).tocsr()
LM = {k: np.array(v['p_cm']) for k, v in json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks'].items()}
LAB = np.load(W + '/lm/SA-M188_regions.npz')['label']
VN = igl.per_vertex_normals(V, F)
def section_loops(c, n, rad=None, vmask=None, field=None):
    """closed loops of the plane (point c, normal n) with the surface -- or of the level set field == 0 when field (per vertex) is given;
    each loop = dict(P (k,3) points, ab (k,2) crossing edges, w edge params). rad: only faces within rad of c (speed)."""
    if field is None: n = np.asarray(n, float); n = n / np.linalg.norm(n); s = (V - c) @ n
    else: s = field
    Fm = F if rad is None else F[np.linalg.norm(V[F[:, 0]] - c, axis=1) < rad]
    sg = s[Fm] > 0; cross = ~(sg.all(1) | (~sg).all(1)); Fc = Fm[cross]
    if vmask is not None: Fc = Fc[vmask[Fc].all(1)]
    segs = {}
    def ekey(a, b): return (a, b) if a < b else (b, a)
    adj = {}
    for t in Fc:
        ks = [ekey(t[a], t[b]) for a, b in ((0, 1), (1, 2), (2, 0)) if (s[t[a]] > 0) != (s[t[b]] > 0)]
        if len(ks) != 2: continue
        adj.setdefault(ks[0], []).append(ks[1]); adj.setdefault(ks[1], []).append(ks[0])
    loops = []; seen = set()
    for k0 in adj:
        if k0 in seen: continue
        loop = [k0]; seen.add(k0); prev = None; cur = k0
        while True:
            nx = [k for k in adj[cur] if k != prev and k not in seen]
            if not nx: break
            prev, cur = cur, nx[0]; seen.add(cur); loop.append(cur)
        if len(loop) < 6: continue
        ab = np.array(loop); wa = s[ab[:, 0]] / (s[ab[:, 0]] - s[ab[:, 1]]); P = V[ab[:, 0]] + wa[:, None] * (V[ab[:, 1]] - V[ab[:, 0]])
        closed = ekey(*ab[-1]) in [ekey(*x) for x in [tuple(y) for y in adj[ekey(*ab[0])]]] or len(adj[ekey(*ab[0])]) == 2
        loops.append(dict(P=P, ab=ab, w=wa, closed=bool(closed)))
    return loops
def frame(n, up=(0, 0, 1.0)):
    n = np.asarray(n, float); n = n / np.linalg.norm(n); a = np.asarray(up, float); e1 = a - (a @ n) * n
    if np.linalg.norm(e1) < 1e-6: e1 = np.array([1.0, 0, 0]) - n[0] * n
    e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1); return e1, e2
def loop_around(c, n, rad=None, pick='contains'):
    """the section loop enclosing c (2D point-in-polygon in the plane); among several the smallest enclosing one"""
    L = section_loops(c, n, rad); e1, e2 = frame(n); best = None
    for lp in L:
        xy = np.c_[(lp['P'] - c) @ e1, (lp['P'] - c) @ e2]
        from matplotlib.path import Path
        if Path(xy).contains_point((0, 0)):
            A = 0.5 * abs(np.dot(xy[:, 0], np.roll(xy[:, 1], -1)) - np.dot(xy[:, 1], np.roll(xy[:, 0], -1)))
            if best is None or A < best[0]: best = (A, lp)
    return None if best is None else best[1]
def ray_loop(c, n, lp, dirs):
    """first intersection of rays from c (in-plane unit directions dirs) with the loop polyline (2D), returns (k,3) points"""
    e1, e2 = frame(n); P = lp['P']; xy = np.c_[(P - c) @ e1, (P - c) @ e2]; A = xy; B = np.roll(xy, -1, 0); out = []
    for d in dirs:
        d2 = np.array([d @ e1, d @ e2]); d2 /= np.linalg.norm(d2)
        # solve c + t d = A + s (B - A)
        AB = B - A; den = d2[0] * AB[:, 1] - d2[1] * AB[:, 0]; ok = np.abs(den) > 1e-12
        t = np.where(ok, (A[:, 0] * AB[:, 1] - A[:, 1] * AB[:, 0]) / np.where(ok, den, 1), np.inf); s_ = np.where(ok, (A[:, 0] * d2[1] - A[:, 1] * d2[0]) / np.where(ok, den, 1), -1)
        hit = ok & (t > 0) & (s_ >= 0) & (s_ <= 1)
        if not hit.any(): out.append(None); continue
        i = np.argmin(np.where(hit, t, np.inf)); q = A[i] + s_[i] * AB[i]; out.append(c + q[0] * e1 + q[1] * e2)
    return out
def ring(c, n, angles, up=(0, 0, 1.0), rad=None, lp=None):
    """ring points at in-plane angles (deg, measured from the in-plane 'up' projection e1 towards e2)"""
    e1, e2 = frame(n, up); lp = lp or loop_around(c, n, rad)
    if lp is None: raise RuntimeError('no loop around %s' % (c,))
    dirs = [np.cos(np.radians(a)) * e1 + np.sin(np.radians(a)) * e2 for a in angles]; return ray_loop(c, n, lp, dirs), lp
def snap(P): return KD.query(np.asarray(P))[1]
def embed(P):
    d2, fi, cp = igl.point_mesh_squared_distance(np.asarray(P, float), V, F); a0, b0, c0 = V[F[fi, 0]], V[F[fi, 1]], V[F[fi, 2]]
    v0 = b0 - a0; v1 = c0 - a0; v2 = cp - a0; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1); den = d00 * d11 - d01 * d01
    bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den; return fi, np.c_[1 - bb - cc, bb, cc], np.sqrt(d2)
def iso_loops(field, level, vmask):
    """level-set loops of a per-vertex field restricted to faces whose vertices are all in vmask"""
    f = np.full(NV, np.nan); f[vmask] = field[vmask] - level; f[~vmask] = 1e9
    return section_loops(None, None, vmask=vmask, field=f)
def harmonic(region, zero, one):
    """cotan-harmonic field on the region sub-mesh with phi = 0 on zero, 1 on one (vertex masks)"""
    from scipy.sparse.linalg import factorized
    keep = region[F].all(1); Fs = F[keep]; sub = np.unique(Fs); mp = -np.ones(NV, int); mp[sub] = np.arange(len(sub)); Fl = mp[Fs]
    L = -igl.cotmatrix(V[sub], Fl).tocsr(); b = np.zeros(len(sub)); fix = np.zeros(len(sub), bool)
    z = zero[sub]; o = one[sub]; fix[z | o] = True; b[o] = 1.0
    fr = np.nonzero(~fix)[0]; fx = np.nonzero(fix)[0]; x = b.copy()
    x[fr] = factorized(L[fr][:, fr].tocsc())(-L[fr][:, fx] @ b[fx]); out = np.full(NV, np.nan); out[sub] = x; return out
def geodesic_from(seed_mask, region):
    sub = np.nonzero(region)[0]; mp = -np.ones(NV, int); mp[sub] = np.arange(len(sub)); Gs = G[sub][:, sub]
    d = dijkstra(Gs, indices=mp[np.nonzero(seed_mask & region)[0]], min_only=True); out = np.full(NV, np.inf); out[sub] = d; return out
def loop_len(P): return float(np.linalg.norm(np.diff(np.vstack([P, P[:1]]), axis=0), axis=1).sum())
def arc_points(P, start_idx, fracs, direction=1):
    """points at arc fractions along the closed polyline P starting at index start_idx in the given direction"""
    P = np.roll(P, -start_idx, 0)
    if direction < 0: P = np.vstack([P[:1], P[1:][::-1]])
    Q = np.vstack([P, P[:1]]); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; L = s[-1]; out = []
    for t in fracs:
        t = (t % 1.0) * L; j = min(np.searchsorted(s, t, side='right') - 1, len(P) - 1); w = (t - s[j]) / max(s[j + 1] - s[j], 1e-12); out.append((1 - w) * Q[j] + w * Q[j + 1])
    return np.array(out)
