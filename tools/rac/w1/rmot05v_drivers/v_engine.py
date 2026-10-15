# RM-OT-05V: local implicit region rebuild engine (additive; nothing upstream is modified).
#
# One neutralization step replaces the surface inside a bounded REGION of the current checkpoint mesh:
#   1. g(p) < 0 defines the region (analytic: capsules / boxes / half-spaces, see Region below). Faces with any vertex g <= 0 are removed;
#      every other face and vertex is copied BIT-EXACT (float32 positions, S3 identity rac_s3_vid1).
#   2. Inside the region a new surface is extracted from a blended implicit field
#          phi = w(g) * phi_src + (1 - w(g)) * phi_inf          (w = 1 at the region boundary, 0 deeper than t)
#      phi_src = signed distance to the current mesh; phi_inf = INFERRED field (smoothed + offset source, optional primitives:
#      mirrored counterpart, toe capsules, ...). The new surface therefore meets the kept skin continuously at the boundary.
#   3. Surface nets on the grid -> quads -> triangles; patch = faces with every vertex g < -h; bridged to the kept boundary loops;
#      seam band faired; triangle quality improved (edge flips + projected tangential relaxation + sliver collapse) on NEW faces only.
# Everything new is labelled INFERRED (face label 1, vertex vid 0).
import json, numpy as np, igl, scipy.ndimage as ndi
from scipy.spatial import cKDTree

f32 = np.float32

# ---------------------------------------------------------------------------------------------------------- region / primitive SDFs
def sd_capsule(P, a, b, r):
    a = np.asarray(a, float); b = np.asarray(b, float); ab = b - a; t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1) - r

def sd_cone_capsule(P, a, b, ra, rb):   # round cone (linear radius), approximate SDF (adequate for smooth unions)
    a = np.asarray(a, float); b = np.asarray(b, float); ab = b - a; t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1) - (ra + t * (rb - ra))

def sd_box(P, lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); c = (lo + hi) / 2; e = (hi - lo) / 2; q = np.abs(P - c) - e
    return np.linalg.norm(np.maximum(q, 0), axis=1) + np.minimum(q.max(1), 0)

def sd_ellipsoid(P, c, radii):   # approximate (Quilez) ellipsoid SDF
    q = (P - np.asarray(c, float)) / np.asarray(radii, float); k0 = np.linalg.norm(q, axis=1); k1 = np.linalg.norm(q / np.asarray(radii, float), axis=1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)

def smin(a, b, k):   # polynomial smooth minimum (union)
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1); return b * (1 - h) + a * h - k * h * (1 - h)

def smax(a, b, k): return -smin(-a, -b, k)

def eval_region(spec, P):
    """spec: {'op': 'union'|'inter'|'sub', 'items': [...]} or primitive dict. Returns g (negative inside)."""
    t = spec['type']
    if t == 'capsule': return sd_capsule(P, spec['a'], spec['b'], spec['r'])
    if t == 'cone': return sd_cone_capsule(P, spec['a'], spec['b'], spec['ra'], spec['rb'])
    if t == 'box': return sd_box(P, spec['lo'], spec['hi'])
    if t == 'ellipsoid': return sd_ellipsoid(P, spec['c'], spec['radii'])
    if t == 'pointset':   # distance to a frozen point set (e.g. detected garment / braid vertices) minus a margin
        global _PS_CACHE
        try: _PS_CACHE
        except NameError: _PS_CACHE = {}
        key = spec['file']
        if key not in _PS_CACHE:
            Q = np.load(spec['file']); _PS_CACHE[key] = cKDTree(Q)
        return _PS_CACHE[key].query(P, workers=-1)[0] - spec['r']
    if t == 'voronoi':   # inside where the nearest frozen point belongs to set A (to rebuild) rather than set B (everything kept);
        # the boundary runs mid-way through air gaps and transversally across the surface at the A/B split
        global _VO_CACHE
        try: _VO_CACHE
        except NameError: _VO_CACHE = {}
        for k in ('a', 'b'):
            if spec[k] not in _VO_CACHE: _VO_CACHE[spec[k]] = cKDTree(np.load(spec[k]))
        return _VO_CACHE[spec['a']].query(P, workers=-1)[0] - _VO_CACHE[spec['b']].query(P, workers=-1)[0] + spec.get('bias', 0.0)
    if t == 'gridfile':   # frozen sampled region field (built by v_region_grid.py), trilinear; +far outside its box
        global _GF_CACHE
        try: _GF_CACHE
        except NameError: _GF_CACHE = {}
        if spec['file'] not in _GF_CACHE:
            d = np.load(spec['file']); _GF_CACHE[spec['file']] = (d['A'].astype(np.float64), d['lo'].astype(np.float64), float(d['h']))
        A, lo, hh = _GF_CACHE[spec['file']]; c = (P - lo) / hh
        out = ndi.map_coordinates(A, c.T, order=1, mode='nearest')
        ob = (c < 0).any(1) | (c > (np.array(A.shape) - 1)).any(1); out[ob] = np.maximum(out[ob], 5.0)
        return out
    if t == 'ellcyl_y':   # elliptic cylinder along y: centre (x, z), semi-axes (a, b); approximate SDF (2-D Quilez ellipse)
        q = np.stack([(P[:, 0] - spec['c'][0]) / spec['a'], (P[:, 2] - spec['c'][1]) / spec['b']], 1)
        k0 = np.linalg.norm(q, axis=1); k1 = np.linalg.norm(q / np.array([spec['a'], spec['b']]), axis=1)
        return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)
    if t == 'xprofile2':  # side-specific lateral limit: x - xc <= Lp(z) and xc - x <= Ln(z)
        dx = P[:, 0] - spec['xc']
        return np.maximum(dx - np.interp(P[:, 2], spec['z'], spec['Lp']), -dx - np.interp(P[:, 2], spec['z'], spec['Ln']))
    if t == 'xprofile':   # |x - xc| <= L(z) (piecewise linear in z): lateral limit that passes between trunk and hanging arms
        return np.abs(P[:, 0] - spec['xc']) - np.interp(P[:, 2], spec['z'], spec['L'])
    if t == 'halfspace':   # n . p <= d  is inside
        n = np.asarray(spec['n'], float); n = n / np.linalg.norm(n); return P @ n - spec['d']
    if t in ('union', 'inter', 'sub'):
        gs = [eval_region(s, P) for s in spec['items']]; k = spec.get('k', 0.0)
        if t == 'union':
            g = gs[0]
            for x in gs[1:]: g = smin(g, x, k)
            return g
        if t == 'inter':
            g = gs[0]
            for x in gs[1:]: g = smax(g, x, k)
            return g
        g = gs[0]
        for x in gs[1:]: g = smax(g, -x, k)
        return g
    raise ValueError(t)

# ---------------------------------------------------------------------------------------------------------- grid fields
class Grid:
    def __init__(self, lo, hi, h):
        self.h = float(h); self.lo = np.asarray(lo, float); self.n = np.ceil((np.asarray(hi, float) - self.lo) / h).astype(int) + 1
    def points(self):
        ax = [self.lo[i] + self.h * np.arange(self.n[i]) for i in range(3)]
        X, Y, Z = np.meshgrid(*ax, indexing='ij'); return np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    def sample(self, A, P, order=1):   # trilinear
        c = (P - self.lo) / self.h; return ndi.map_coordinates(A, c.T, order=order, mode='nearest')
    def grad(self, A, P):
        g = np.stack(np.gradient(A, self.h), 0); return np.stack([self.sample(g[i], P) for i in range(3)], 1)

def sdf_on_grid(V, F, grid, chunk=600000):
    P = grid.points(); out = np.empty(len(P))
    for s in range(0, len(P), chunk):
        out[s:s + chunk] = igl.signed_distance(P[s:s + chunk], np.asarray(V, float), np.asarray(F, np.int64),
                                               igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)[0]
    return out.reshape(grid.n)

def blur_offset(phi, grid, sigma_cm, offset_cm):
    """INFERRED under-surface: gaussian-smoothed source field moved inward by offset (positive offset shrinks)."""
    return ndi.gaussian_filter(phi, sigma_cm / grid.h, mode='nearest') + offset_cm

def blend(phi_src, phi_inf, g, t):
    w = np.clip(1.0 + g / t, 0, 1); w = w * w * (3 - 2 * w)   # smoothstep: 1 at g >= 0, 0 at g <= -t
    return w * phi_src + (1 - w) * phi_inf

# ---------------------------------------------------------------------------------------------------------- surface nets
def surface_nets(phi, grid):
    s = phi < 0; nx, ny, nz = phi.shape
    # cell corners
    c = np.stack([phi[i:nx - 1 + i, j:ny - 1 + j, k:nz - 1 + k] for i in (0, 1) for j in (0, 1) for k in (0, 1)], -1)
    inside = (c < 0); cross = inside.any(-1) & ~inside.all(-1)
    cid = -np.ones(cross.shape, np.int64); idx = np.argwhere(cross); cid[cross] = np.arange(len(idx))
    # vertex = mean of edge crossings within the cell
    corners = np.array([(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)])
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if np.abs(corners[a] - corners[b]).sum() == 1]
    cc = c[cross]; acc = np.zeros((len(idx), 3)); cnt = np.zeros(len(idx))
    for a, b in edges:
        va, vb = cc[:, a], cc[:, b]; m = (va < 0) != (vb < 0); t = va[m] / (va[m] - vb[m])
        acc[m] += corners[a] + t[:, None] * (corners[b] - corners[a]); cnt[m] += 1
    Vn = grid.lo + grid.h * (idx + acc / cnt[:, None])
    quads = []
    for ax in range(3):   # grid edges along ax with a sign change -> quad of the 4 cells around it
        sl0 = [slice(None)] * 3; sl1 = [slice(None)] * 3; sl0[ax] = slice(0, -1); sl1[ax] = slice(1, None)
        e = s[tuple(sl0)] != s[tuple(sl1)]
        o = [a for a in range(3) if a != ax]
        # edge (i,j,k)->(i+1..) ; surrounding cells: offsets in the two other axes of (0/-1)
        E = np.argwhere(e); E = E[(E[:, o[0]] > 0) & (E[:, o[0]] < phi.shape[o[0]] - 1) & (E[:, o[1]] > 0) & (E[:, o[1]] < phi.shape[o[1]] - 1)]
        def cell(d0, d1):
            q = E.copy(); q[:, o[0]] -= d0; q[:, o[1]] -= d1; return cid[q[:, 0], q[:, 1], q[:, 2]]
        q = np.stack([cell(1, 1), cell(0, 1), cell(0, 0), cell(1, 0)], 1)
        neg_first = s[E[:, 0], E[:, 1], E[:, 2]]   # inside at the lower end -> outward normal points +ax
        q[~neg_first] = q[~neg_first][:, ::-1]
        if ax == 1: q = q[:, ::-1]   # right-handedness of the (o0, o1) pair for the y axis is (z, x) not (x, z)
        quads.append(q)
    Q = np.concatenate(quads); Q = Q[(Q >= 0).all(1)]
    # split quads along the shorter diagonal
    d02 = np.linalg.norm(Vn[Q[:, 0]] - Vn[Q[:, 2]], axis=1); d13 = np.linalg.norm(Vn[Q[:, 1]] - Vn[Q[:, 3]], axis=1); u = d02 <= d13
    T = np.concatenate([Q[u][:, [0, 1, 2]], Q[u][:, [0, 2, 3]], Q[~u][:, [0, 1, 3]], Q[~u][:, [1, 2, 3]]])
    return Vn, T

# ---------------------------------------------------------------------------------------------------------- mesh helpers
def edges_of(F): return np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])

def boundary_loops(F):
    """directed boundary edges (as they appear in faces) chained into loops (lists of vertex ids)."""
    E = edges_of(F); key = np.sort(E, 1); u, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    B = E[cnt[inv.ravel()] == 1]; nxt = {}
    for a, b in B: nxt.setdefault(int(a), []).append(int(b))
    loops = []; used = set()
    for a0 in list(nxt):
        if a0 in used: continue
        lp = [a0]; used.add(a0); a = a0
        while True:
            cand = [b for b in nxt.get(a, []) if b not in used or b == a0]
            if not cand: break
            b = cand[0]
            if b == a0: break
            lp.append(b); used.add(b); a = b
        loops.append(lp)
    return loops

def components(F, nv):
    import scipy.sparse as sp, scipy.sparse.csgraph as cg
    E = edges_of(F); A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(nv, nv))
    n, lab = cg.connected_components(A, directed=False); return lab

def tri_angles(V, F):
    A = V[F]; out = []
    for i in range(3):
        u = A[:, (i + 1) % 3] - A[:, i]; v = A[:, (i + 2) % 3] - A[:, i]
        c = (u * v).sum(1) / np.maximum(np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1), 1e-30); out.append(np.degrees(np.arccos(np.clip(c, -1, 1))))
    return np.stack(out, 1)

def face_normals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); l = np.linalg.norm(n, axis=1); return n / np.maximum(l, 1e-30)[:, None], l / 2

def vertex_neighbors(F, nv):
    E = edges_of(F); E = np.concatenate([E, E[:, ::-1]]); E = np.unique(E, axis=0)
    starts = np.searchsorted(E[:, 0], np.arange(nv + 1)); return E[:, 1], starts

# ---------------------------------------------------------------------------------------------------------- bridging two loops
def bridge(Vall, A, B):
    """A: kept loop, directed as in kept faces; B: patch loop, directed as in patch faces. With both surfaces consistently
    oriented, the two loops run in OPPOSITE spatial directions, so B is traversed reversed. Start points are aligned by the
    closest pair; triangles are emitted by merging the two loops' arc-length fractions (well distributed strip).
    Bridge triangles contain a_{i+1}->a_i (opposite to the kept face) and b_k->b_{k+1} of the reversed patch order."""
    A = list(A); Bs = list(B)[::-1]
    PA = Vall[A]; k0 = int(np.argmin(np.linalg.norm(Vall[Bs] - PA[0], axis=1))); Bs = Bs[k0:] + Bs[:k0]
    def frac(L):
        P = Vall[L + L[:1]]; d = np.linalg.norm(np.diff(P, axis=0), axis=1); c = np.concatenate([[0], np.cumsum(d)]); return c / c[-1]
    fa = frac(A); fb = frac(Bs); n = len(A); m = len(Bs); i = k = 0; T = []
    while i < n or k < m:
        if i >= n: adv_a = False
        elif k >= m: adv_a = True
        else: adv_a = fa[i + 1] <= fb[k + 1]
        a0 = A[i % n]; b0 = Bs[k % m]
        if adv_a:
            T.append((A[(i + 1) % n], a0, b0)); i += 1
        else:
            T.append((b0, Bs[(k + 1) % m], a0)); k += 1
    return np.array(T, np.int64), True

# ---------------------------------------------------------------------------------------------------------- quality improvement (new faces only)
def improve(V, F, movable, project, fixed_faces_mask, iters=6, min_target=20.0, movable_all=None):
    """V float64, F faces; movable: bool per vertex (new vertices only); project(P)->P on the target surface;
    fixed_faces_mask: faces that may NOT be flipped (kept faces). Returns V, F."""
    F = F.copy(); V = V.copy()
    for it in range(iters):
        F = flip_pass(V, F, fixed_faces_mask, movable_all)
        V = relax(V, F, movable, project, n=3)
    return V, F

def relax(V, F, movable, project, n=3, lam=0.5):
    import scipy.sparse as sp
    E = edges_of(F); E = np.unique(np.sort(np.concatenate([E, E[:, ::-1]]), 1), axis=0); E = np.concatenate([E, E[:, ::-1]])
    A = sp.csr_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(len(V), len(V))); deg = np.asarray(A.sum(1)).ravel()
    mv = np.where(movable & (deg > 0))[0]
    for _ in range(n):
        avg = (A @ V)[mv] / deg[mv, None]
        V[mv] = project(V[mv] + lam * (avg - V[mv]))
    return V

def _minang(V, T):
    A = V[T[:, 0]]; B = V[T[:, 1]]; C = V[T[:, 2]]
    def ang(p, q, r):
        u = q - p; v = r - p; c = (u * v).sum(1) / np.maximum(np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1), 1e-30)
        return np.degrees(np.arccos(np.clip(c, -1, 1)))
    return np.minimum(np.minimum(ang(A, B, C), ang(B, C, A)), ang(C, A, B))

def flip_pass(V, F, fixed, movable=None, rounds=3):
    """Vectorized edge flips that raise the min angle of the two adjacent (non-fixed) triangles; normals kept within 30 deg;
    never creates an existing edge, and (if movable given) never a face made only of non-movable vertices."""
    F = F.copy(); nv = len(V)
    for _ in range(rounds):
        m = len(F); E = edges_of(F); pos = np.repeat(np.arange(3), m); fid = np.tile(np.arange(m), 3)
        key = np.minimum(E[:, 0], E[:, 1]).astype(np.int64) * nv + np.maximum(E[:, 0], E[:, 1])
        o = np.argsort(key, kind='stable'); ks = key[o]; same = np.where(ks[1:] == ks[:-1])[0]
        # only edges with exactly two faces
        ok = np.ones(len(same), bool); ok &= ~((same + 2 < len(ks)) & (np.r_[ks[2:], -1][same] == ks[same]))
        ok &= ~((same >= 1) & (np.r_[-1, ks[:-1]][same] == ks[same]))
        same = same[ok]; e0 = o[same]; e1 = o[same + 1]; f0 = fid[e0]; f1 = fid[e1]
        sel = ~fixed[f0] & ~fixed[f1]; e0, e1, f0, f1 = e0[sel], e1[sel], f0[sel], f1[sel]
        a = E[e0, 0]; b = E[e0, 1]; c = F[f0, (pos[e0] + 2) % 3]; d = F[f1, (pos[e1] + 2) % 3]
        good = (E[e1, 0] == b) & (E[e1, 1] == a) & (c != d)
        a, b, c, d, f0, f1 = a[good], b[good], c[good], d[good], f0[good], f1[good]
        old0 = np.stack([a, b, c], 1); old1 = np.stack([b, a, d], 1); new0 = np.stack([c, a, d], 1); new1 = np.stack([d, b, c], 1)
        oldm = np.minimum(_minang(V, old0), _minang(V, old1)); newm = np.minimum(_minang(V, new0), _minang(V, new1))
        imp = newm - oldm; cand = imp > 1e-6
        ex = np.unique(key); kcd = np.minimum(c, d).astype(np.int64) * nv + np.maximum(c, d); cand &= ~np.isin(kcd, ex)
        n0, _ = face_normals(V, old0); n1, _ = face_normals(V, old1); nm = n0 + n1; nm /= np.maximum(np.linalg.norm(nm, axis=1), 1e-12)[:, None]
        m0, ar0 = face_normals(V, new0); m1, ar1 = face_normals(V, new1)
        cand &= ((m0 * nm).sum(1) > 0.94) & ((m1 * nm).sum(1) > 0.94) & (ar0 > 1e-12) & (ar1 > 1e-12)
        if movable is not None: cand &= movable[new0].any(1) & movable[new1].any(1)
        # never create an edge much longer than the pair's existing edges (prevents shortcut triangles across curvature)
        lcd = np.linalg.norm(V[c] - V[d], axis=1); lab_ = np.linalg.norm(V[a] - V[b], axis=1); cand &= lcd <= 1.25 * np.maximum(lab_, 1e-9) + 1e-9
        idx = np.where(cand)[0]
        if not len(idx): break
        idx = idx[np.argsort(-imp[idx])]; used = np.zeros(m, bool); usedk = set(); take = []
        for i in idx:
            if used[f0[i]] or used[f1[i]] or kcd[i] in usedk: continue
            used[f0[i]] = used[f1[i]] = True; usedk.add(kcd[i]); take.append(i)
        take = np.array(take); F[f0[take]] = new0[take]; F[f1[take]] = new1[take]
    return F

def collapse_edge_ok(F, a, b, vf):
    """link condition for collapsing edge a-b (b removed): common neighbours of a and b must be exactly the two opposite vertices."""
    fa = vf[a]; fb = vf[b]
    na = set(F[list(fa)].ravel()) - {a}; nb = set(F[list(fb)].ravel()) - {b}
    shared = [f for f in fa if b in F[f]]
    opp = set(F[shared].ravel()) - {a, b}
    return (na & nb) == opp and len(shared) == 2

def fix_slivers(V, F, movable, fixed, floor=12.0, iters=12, collapse=True, log=None, project=None):
    pj = project if project is not None else (lambda p: p)
    """Raise the minimum angle of non-fixed faces to >= floor: local relaxation of movable vertices of bad faces + flips,
    then (if still bad) collapse the shortest edge whose removed endpoint is movable (link condition checked)."""
    F = F.copy(); V = V.copy(); fixed = fixed.copy()
    for it in range(iters):
        ang = tri_angles(V, F).min(1); bad = (ang < floor) & ~fixed
        if not bad.any(): break
        vs = np.unique(F[bad]); mv = np.zeros(len(V), bool); mv[vs] = True; mv &= movable
        V = relax(V, F, mv, pj, n=2, lam=0.6)
        F = flip_pass(V, F, fixed, movable)
    for rnd in range(3):
        V, F, fixed, movable, ns = split_caps(V, F, fixed, movable, floor)
        if not ns: break
        for it in range(4):
            ang = tri_angles(V, F).min(1); bad = (ang < floor) & ~fixed
            vs = np.unique(F[bad]); mv = np.zeros(len(V), bool); mv[vs] = True; mv &= movable
            V = relax(V, F, mv, pj, n=2, lam=0.6); F = flip_pass(V, F, fixed, movable)
        if log is not None: log.setdefault('cap_splits', []).append(int(ns))
    if collapse:
        for rnd in range(6):
            ang = tri_angles(V, F).min(1); bad = np.where((ang < floor) & ~fixed)[0]
            if not len(bad): break
            fl = F.ravel(); o = np.argsort(fl, kind='stable'); st = np.searchsorted(fl[o], np.arange(len(V) + 1))
            class VF(dict):
                def __missing__(self, v):
                    r = list(o[st[v]:st[v + 1]] // 3); self[v] = r; return r
            vf = VF()
            dead = np.zeros(len(F), bool); touched = set(); ncol = 0
            for fi in bad:
                if dead[fi]: continue
                f = F[fi]; L = [np.linalg.norm(V[f[i]] - V[f[(i + 1) % 3]]) for i in range(3)]
                for i in np.argsort(L):
                    a, b = int(f[i]), int(f[(i + 1) % 3])
                    if not movable[b]: a, b = b, a
                    if not movable[b] or a in touched or b in touched: continue
                    fa = [x for x in vf[a] if not dead[x]]; fb = [x for x in vf[b] if not dead[x]]
                    if any(fixed[x] for x in fb if b in F[x] and a not in F[x]) and not movable[b]: continue
                    vfl = {a: fa, b: fb}
                    if not collapse_edge_ok(F, a, b, vfl): continue
                    newpos = V[a] if not movable[a] else (V[a] + V[b]) / 2
                    # reject if any surviving face around b or a flips
                    surv = [x for x in set(fa + fb) if not (a in F[x] and b in F[x])]
                    Ft = F[surv].copy(); Ft[Ft == b] = a; Vt = V.copy(); Vt[a] = newpos
                    n0, _ = face_normals(V, F[surv]); n1, ar = face_normals(Vt, Ft)
                    if (ar < 1e-10).any() or ((n0 * n1).sum(1) < 0.5).any(): continue
                    V[a] = newpos
                    for x in fb:
                        if a in F[x] and b in F[x]: dead[x] = True
                        else: F[x][F[x] == b] = a; vf[a].append(x)
                    touched.update([a, b]); ncol += 1; break
            F = F[~dead]; fixed = fixed[~dead]
            F = flip_pass(V, F, fixed, movable)
            if log is not None: log.setdefault('collapses', []).append(ncol)
    return V, F, fixed, movable

def nm_count(F):
    E = np.sort(edges_of(F), 1); u, c = np.unique(E, axis=0, return_counts=True)
    D = edges_of(F); ud, cd = np.unique(D, axis=0, return_counts=True)
    return dict(nonmanifold_edges=int((c > 2).sum()), boundary_edges=int((c == 1).sum()), dup_directed=int((cd > 1).sum()))

def repair_patch(Vn, T, interior_mask, log=None, max_rounds=5):
    """Remove faces on non-manifold / inconsistently oriented edges of the extracted patch and fan-fill the small interior
    holes this leaves (centroid vertex). interior_mask: per-vertex bool, True if far from the region boundary."""
    Vn = Vn.copy(); T = T.copy(); nfix = 0
    for r in range(max_rounds):
        E = edges_of(T); key = np.sort(E, 1); u, inv, c = np.unique(key, axis=0, return_inverse=True, return_counts=True)
        ud, invd, cd = np.unique(E, axis=0, return_inverse=True, return_counts=True)
        bad_e = (c[inv.ravel()] > 2) | (cd[invd.ravel()] > 1)
        if not bad_e.any(): break
        badf = np.unique(np.tile(np.arange(len(T)), 3)[bad_e])
        # grow one ring to get clean hole boundaries
        bv = np.unique(T[badf]); badf = np.where(np.isin(T, bv).any(1))[0]
        T = np.delete(T, badf, axis=0); nfix += len(badf)
        loops = boundary_loops(T); add_v = []; add_t = []
        for lp in loops:
            if len(lp) > 40 or not interior_mask[lp].all(): continue
            cidx = len(Vn) + len(add_v); add_v.append(Vn[lp].mean(0))
            for i in range(len(lp)):
                a, b = lp[i], lp[(i + 1) % len(lp)]
                add_t.append((b, a, cidx))   # loop is directed as in the faces; fill on the opposite side
        if add_v:
            Vn = np.concatenate([Vn, np.array(add_v)]); interior_mask = np.concatenate([interior_mask, np.ones(len(add_v), bool)]); T = np.concatenate([T, np.array(add_t)])
    if log is not None: log['patch_repair_faces_removed'] = int(nfix)
    return Vn, T

def split_caps(V, F, fixed, movable, floor=12.0, maxang=100.0):
    """Split the longest edge of bad obtuse (cap) non-fixed faces at its midpoint (both adjacent faces must be non-fixed)."""
    ang = tri_angles(V, F); bad = np.where((ang.min(1) < floor) & (ang.max(1) > maxang) & ~fixed)[0]
    if not len(bad): return V, F, fixed, movable, 0
    E = edges_of(F); fid = np.tile(np.arange(len(F)), 3); key = {}
    for k, (a, b) in enumerate(E): key.setdefault((min(a, b), max(a, b)), []).append(fid[k])
    V = list(V); F = F.tolist(); fixed = list(fixed); movable = list(movable); used = set(); n = 0
    for f in bad:
        if f in used: continue
        t = F[f]; i = int(np.argmax(ang[f])); a, b = t[(i + 1) % 3], t[(i + 2) % 3]   # edge opposite the obtuse vertex
        fs = key.get((min(a, b), max(a, b)), [])
        if len(fs) != 2 or any(fixed[x] or x in used for x in fs): continue
        m = len(V); V.append((np.asarray(V[a]) + np.asarray(V[b])) / 2); movable.append(True)
        for x in fs:
            tt = F[x]; j = tt.index(a); 
            if tt[(j + 1) % 3] == b: c = tt[(j + 2) % 3]; F[x] = [a, m, c]; F.append([m, b, c])
            else: c = tt[(j + 1) % 3]; F[x] = [b, m, c]; F.append([m, a, c])
            fixed.append(False); used.add(x)
        n += 1
    return np.array(V), np.array(F, np.int64), np.array(fixed), np.array(movable), n

def mirror_spec(spec, x0):
    """Mirror an analytic region spec across the plane x = x0 (capsules, cones, boxes, ellipsoids, half-spaces, unions...)."""
    import copy
    s = copy.deepcopy(spec); t = s['type']; mx = lambda p: [2 * x0 - p[0], p[1], p[2]]
    if t in ('capsule',): s['a'] = mx(s['a']); s['b'] = mx(s['b'])
    elif t == 'cone': s['a'] = mx(s['a']); s['b'] = mx(s['b'])
    elif t == 'box': lo, hi = s['lo'], s['hi']; s['lo'] = [2 * x0 - hi[0], lo[1], lo[2]]; s['hi'] = [2 * x0 - lo[0], hi[1], hi[2]]
    elif t == 'ellipsoid': s['c'] = mx(s['c'])
    elif t == 'halfspace':
        n = np.asarray(s['n'], float); n = n / np.linalg.norm(n); s['n'] = [float(-n[0]), float(n[1]), float(n[2])]; s['d'] = float(s['d'] - 2 * x0 * n[0])
    elif t == 'xprofile': s['xc'] = 2 * x0 - s['xc']
    elif t == 'ellcyl_y': s['c'] = [2 * x0 - s['c'][0], s['c'][1]]
    elif t in ('union', 'inter', 'sub'): s['items'] = [mirror_spec(x, x0) for x in s['items']]
    else: raise ValueError('cannot mirror ' + t)
    return s

def _ear_clip(P2):
    """Triangulate a simple polygon (n x 2, any orientation) by ear clipping; returns index triples (CCW in 2-D)."""
    n = len(P2); idx = list(range(n))
    area = 0.5 * np.sum(P2[:, 0] * np.roll(P2[:, 1], -1) - np.roll(P2[:, 0], -1) * P2[:, 1])
    if area < 0: idx = idx[::-1]
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def inside(p, a, b, c):
        return cross(a, b, p) >= -1e-12 and cross(b, c, p) >= -1e-12 and cross(c, a, p) >= -1e-12
    T = []; guard = 0
    while len(idx) > 3 and guard < 20 * n:
        guard += 1; m = len(idx); best = None
        for k in range(m):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % m]; a, b, c = P2[i0], P2[i1], P2[i2]
            if cross(a, b, c) <= 1e-12: continue
            if any(inside(P2[j], a, b, c) for j in idx if j not in (i0, i1, i2)): continue
            # prefer the ear with the largest minimum angle
            q = np.array([a, b, c]); e = [q[1] - q[0], q[2] - q[1], q[0] - q[2]]
            ang = min(np.degrees(np.arccos(np.clip(np.dot(-e[(t + 2) % 3], e[t]) / (np.linalg.norm(e[t]) * np.linalg.norm(e[(t + 2) % 3]) + 1e-30), -1, 1))) for t in range(3))
            if best is None or ang > best[0]: best = (ang, k)
        if best is None: return None
        k = best[1]; m = len(idx); T.append((idx[k - 1], idx[k], idx[(k + 1) % m])); idx.pop(k)
    if len(idx) == 3: T.append(tuple(idx))
    return T

def cap_fill(Vall, loop, target=None):
    """Fill a boundary loop (directed as in the adjacent faces) with a refined, relaxed triangulated disk.
    Returns (new_vertices, faces using global indices with new ones appended after len(Vall)), or None if it fails."""
    L = np.array(loop)
    if len(L) < 3: return None
    P = Vall[L]; c = P.mean(0); U, S_, Wt = np.linalg.svd(P - c); ax = Wt[:2]
    P2 = (P - c) @ ax.T
    tri = _ear_clip(P2)
    if not tri: return None
    T = np.array([[L[a], L[b], L[c_]] for a, b, c_ in tri], np.int64)
    # orientation: the fill must contain each boundary edge reversed relative to the loop direction (a_i -> a_{i+1} in faces)
    e0 = (L[0], L[1])
    has_fwd = any((t[k], t[(k + 1) % 3]) == e0 for t in T for k in range(3))
    if has_fwd: T = T[:, ::-1]
    if target is None: target = float(np.mean(np.linalg.norm(np.diff(np.vstack([P, P[:1]]), axis=0), axis=1)))
    NV = []; base = len(Vall); V = np.vstack([Vall, np.zeros((0, 3))])
    Vloc = Vall.copy(); newv = []
    # refinement: split edges longer than 1.4 target (interior edges only) a few rounds, flipping between rounds
    for rnd in range(8):
        E = edges_of(T); key = np.sort(E, 1); u, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
        lens = np.linalg.norm(Vloc[u[:, 0]] - Vloc[u[:, 1]], axis=1)
        long_ = np.where((cnt == 2) & (lens > 1.4 * target))[0]
        if not len(long_): break
        Tl = T.tolist(); fmap = {}
        for fi, t in enumerate(Tl):
            for k in range(3): fmap.setdefault(tuple(sorted((t[k], t[(k + 1) % 3]))), []).append(fi)
        used = set()
        for ei in long_[np.argsort(-lens[long_])]:
            a, b = u[ei]; fs = fmap.get((min(a, b), max(a, b)), [])
            if len(fs) != 2 or any(f in used for f in fs): continue
            m = len(Vloc); Vloc = np.vstack([Vloc, (Vloc[a] + Vloc[b]) / 2]); newv.append(m)
            for f in fs:
                t = Tl[f]; j = t.index(a)
                if t[(j + 1) % 3] == b: cc = t[(j + 2) % 3]; Tl[f] = [a, m, cc]; Tl.append([m, b, cc])
                else: cc = t[(j + 1) % 3]; Tl[f] = [b, m, cc]; Tl.append([m, a, cc])
                used.add(f)
        T = np.array(Tl, np.int64)
        mov = np.zeros(len(Vloc), bool); mov[newv] = True
        T = flip_pass(Vloc, T, np.zeros(len(T), bool), mov)
        Vloc = relax(Vloc, T, mov, lambda p: p, n=3, lam=0.6)
    mov = np.zeros(len(Vloc), bool); mov[newv] = True
    for _ in range(4):
        T = flip_pass(Vloc, T, np.zeros(len(T), bool), mov); Vloc = relax(Vloc, T, mov, lambda p: p, n=4, lam=0.6)
    return Vloc[len(Vall):], T
