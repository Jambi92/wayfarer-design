# sa_layout.py : RP5 full-cage construction machinery (order ad9cb85 §4-§13) -- AUTHORED coarse layout -> production quad cage on the working source.
#   1. the authored coarse cage (corners + quads + semantic labels, sa_design.py) is placed on SA_RP5_WORK_v001 (SA-M188): every corner snapped to a
#      surface vertex; every coarse edge becomes a surface path (shortest mesh path inside a local ellipsoid; earlier paths are BLOCKED so paths never cross;
#      ring edges are pulled to their section plane); the tail-root edges are the accepted tail module's root ring (fixed, 8 module vertices per coarse edge).
#   2. each coarse quad = the surface region bounded by its 4 paths (flood fill; validated: one disk, boundary = exactly the 4 paths).
#   3. subdivision counts per coarse-edge CHORD (opposite edges of every quad share a count): ceil(longest member / target edge of its region);
#      tail-root chords fixed at 8 (module ring 128 = 16 x 8).
#   4. per quad: uniform Tutte map of its region onto the unit square (boundary by arc length; bijective) -> m x n grid sampled back on the surface
#      (triangle + barycentric); edge samples are shared between neighbouring quads -> one conforming all-quad mesh. The tail module is attached on its root ring.
#   5. relaxation: tangential umbrella smoothing + closest-point reprojection (pinned: tail module, identity landmarks); final barycentric embedding on the
#      canonical base face list -> exact realization on SA-M188 / SA-F188 (shared topology).
import sys, os, json, time, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra, connected_components
from scipy.sparse.linalg import spsolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa_geo as GEO
V, F, G, NV = GEO.V, GEO.F, GEO.G, GEO.NV
VN_ = GEO.VN
# half-edge -> face (outward CCW orientation of the source)
_he = {}
def he_face():
    if _he: return _he
    for k in range(3):
        a, b = F[:, k], F[:, (k + 1) % 3]
        for fi, (x, y) in enumerate(zip(a, b)): _he[(int(x), int(y))] = fi
    return _he
HE = None
def build_he():
    global HE
    if HE is None:
        a = np.r_[F[:, 0], F[:, 1], F[:, 2]]; b = np.r_[F[:, 1], F[:, 2], F[:, 0]]; f = np.r_[np.arange(len(F))] ; f = np.r_[f, f, f]
        HE = sp.coo_matrix((f + 1, (a, b)), shape=(NV, NV)).tocsr()
    return HE
def face_of(a, b): h = build_he(); return int(h[a, b]) - 1
# face adjacency across edges
_FA = None
def face_adj():
    global _FA
    if _FA is None:
        TT, _ = igl.triangle_triangle_adjacency(F); _FA = TT
    return _FA
def local_path(a, b, blocked, plane=None, factor=1.5, margin=2.0, fallback=True, allow=None):
    """shortest mesh path a -> b avoiding blocked vertices (except a, b), inside the ellipsoid |p-A|+|p-B| <= factor |A-B| + margin"""
    A, B = V[a], V[b]; L = np.linalg.norm(A - B)
    for fac, mar in (((factor, margin), (2.5, 5.0), (4.0, 12.0)) if fallback else ((factor, margin),)):
        idx = np.array(GEO.KD.query_ball_point(0.5 * (A + B), 0.5 * (fac * L + mar)))
        idx = idx[np.linalg.norm(V[idx] - A, axis=1) + np.linalg.norm(V[idx] - B, axis=1) <= fac * L + mar]
        ok = ~blocked[idx]
        if allow is not None: ok &= allow[idx]
        ok[idx == a] = True; ok[idx == b] = True; idx = idx[ok]
        mp = -np.ones(NV, int); mp[idx] = np.arange(len(idx)); Gs = G[idx][:, idx].tocoo()
        w = Gs.data.copy()
        if plane is not None:
            c, n = plane; dd = np.abs((V[idx] - c) @ n); w = w * (1.0 + 3.0 * 0.5 * (dd[Gs.row] + dd[Gs.col]))
        Gs = sp.coo_matrix((w, (Gs.row, Gs.col)), shape=Gs.shape).tocsr()
        if mp[a] < 0 or mp[b] < 0: continue
        dist, pred = dijkstra(Gs, indices=mp[a], return_predecessors=True)
        if np.isfinite(dist[mp[b]]):
            p = [mp[b]]
            while p[-1] != mp[a]: p.append(pred[p[-1]])
            return idx[np.array(p[::-1])]
    return None
def polyline_samples(P, k):
    """k-1 interior points at equal arc length along polyline P (shared edge samples), plus the arc parameters of all P vertices"""
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; L = s[-1]; out = []
    for i in range(1, k):
        t = i * L / k; j = min(np.searchsorted(s, t, side='right') - 1, len(P) - 2); w = (t - s[j]) / max(s[j + 1] - s[j], 1e-12); out.append((1 - w) * P[j] + w * P[j + 1])
    return np.array(out).reshape(-1, 3), s / max(L, 1e-12)
class Layout:
    def __init__(self, corners, quads, labels, edge_hint=None, fixed=None, targets=None, verbose=True, arcs=None):
        """corners (nc,3); quads (nq,4) corner ids, CCW from outside; labels: per-quad region label (density + semantics);
        edge_hint: {(a,b): dict(plane=(c,n), prio=int)}; fixed: {(a,b): (P (k+1,3) points incl. ends, count k)} -- tail-root edges"""
        self.C = np.asarray(corners, float); self.Q = np.asarray(quads, int); self.lab = list(labels); self.hint = edge_hint or {}; self.fixed = fixed or {}
        self.targets = targets or {}; self.verbose = verbose; self.arcs = arcs or {}
        self.cv = GEO.snap(self.C)                     # corner -> surface vertex
        if len(set(self.cv.tolist())) != len(self.cv):
            from collections import Counter; dup = [k for k, v in Counter(self.cv.tolist()).items() if v > 1]
            raise RuntimeError('corners snap to the same vertex: %s' % [np.nonzero(self.cv == d)[0].tolist() for d in dup])
        E = {}
        for qi, q in enumerate(self.Q):
            for k in range(4):
                a, b = int(q[k]), int(q[(k + 1) % 4]); E.setdefault((min(a, b), max(a, b)), []).append((qi, k))
        bad = {e: v for e, v in E.items() if len(v) > 2}
        if bad: raise RuntimeError('non-manifold coarse edges %s' % list(bad)[:5])
        self.E = E
        # corners: nearest surface vertex whose degree >= valence + 1 (room for an ordered corner fan); tail-root corners keep the module snap
        deg = np.diff(G.indptr); val = {}
        for e in E: val[e[0]] = val.get(e[0], 0) + 1; val[e[1]] = val.get(e[1], 0) + 1
        fixc = {c for e in self.fixed for c in e}; used = set()
        for c in range(len(self.C)):
            if c in fixc: used.add(int(self.cv[c])); continue
            _, cand = GEO.KD.query(self.C[c], 60)
            ok = [int(x) for x in cand if deg[x] >= val.get(c, 0) + 1 and int(x) not in used]
            self.cv[c] = ok[0] if ok else self.cv[c]; used.add(int(self.cv[c]))
    def log(self, *a):
        if self.verbose: print(*a, flush=True)
    def ring_order(self, v):
        """1-ring neighbours of surface vertex v in cyclic (CCW, outward) order"""
        fs = np.nonzero((F == v).any(1))[0] if not hasattr(self, '_vf') else self._vf[v]
        nxt = {}
        for f in F[fs]:
            k = int(np.nonzero(f == v)[0][0]); nxt[int(f[(k + 1) % 3])] = int(f[(k + 2) % 3])
        start = next(iter(nxt)); out = [start]
        while nxt.get(out[-1], start) != start and len(out) < 30: out.append(nxt[out[-1]])
        return out
    def reserve(self):
        """corner fans: every coarse edge leaving a corner gets its own first-step neighbour, in the same angular order as the edge directions
        (otherwise two boundary paths can leave through adjacent neighbours and seal a quad's wedge at the corner)"""
        vf = {}
        for fi, f in enumerate(F[np.isin(F, self.cv).any(1)]): pass
        mask = np.isin(F, self.cv); rows = np.nonzero(mask.any(1))[0]; self._vf = {}
        for fi in rows:
            for v in F[fi][mask[fi]]: self._vf.setdefault(int(v), []).append(fi)
        inc = {}
        for e in self.E:
            inc.setdefault(e[0], []).append(e); inc.setdefault(e[1], []).append(e)
        self.res = {}; taken = set(int(x) for x in self.cv)
        for c, es in inc.items():
            v = int(self.cv[c]); nb = self.ring_order(v); n0 = VN_[v]; t1 = V[nb[0]] - V[v]; t1 -= (t1 @ n0) * n0; t1 /= np.linalg.norm(t1); t2 = np.cross(n0, t1)
            def ang(p): q = p - V[v]; return np.arctan2(q @ t2, q @ t1)
            na = np.array([ang(V[x]) for x in nb])
            ea = []
            for e in es:
                o = e[1] if e[0] == c else e[0]
                if e in self.fixed:
                    Pf = self.fixed[e][0]; Pf = Pf if e[0] == c else Pf[::-1]; tgt = Pf[1]
                elif e in self.arcs:
                    P = self.arcs[e] if e[0] == c else self.arcs[e][::-1]; j = min(len(P) - 1, max(2, int(np.searchsorted(np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))], 0.6))))
                    tgt = P[j]
                else: tgt = 0.85 * V[v] + 0.15 * V[self.cv[o]]
                ea.append((e, None if tgt is None else ang(tgt)))
            fixed_nb = {}
            free = [e for e, a_ in ea if a_ is not None]
            if len(free) + len(fixed_nb) > len(nb): raise RuntimeError('corner %s valence %d > vertex degree %d' % (self.names[c] if hasattr(self, 'names') else c, len(es), len(nb)))
            # order-preserving assignment: free edges get distinct free neighbours such that ALL edges (fixed ones at their fixed neighbour) appear around
            # the corner in the same cyclic order as their directions
            avail = [i for i, x in enumerate(nb) if x not in fixed_nb.values() and x not in taken]
            if len(avail) < len(free): raise RuntimeError('corner %s: not enough free neighbours' % (self.names[c] if hasattr(self, 'names') else c))
            eang = dict(ea)
            for e, x in fixed_nb.items(): eang[e] = na[nb.index(x)]
            allE = sorted(eang, key=lambda e: eang[e]); fe = [e for e in allE if e not in fixed_nb]
            import itertools
            best = None
            cands = (comb[r:] + comb[:r] for comb in itertools.combinations(avail, len(fe)) for r in range(max(1, len(fe))))
            for comb in cands:
                slot = {e: nb.index(fixed_nb[e]) for e in fixed_nb}; slot.update({e: comb[k] for k, e in enumerate(fe)})
                seq = [slot[e] for e in allE]; k0 = int(np.argmin(seq)); seq = seq[k0:] + seq[:k0]
                if any(seq[i + 1] <= seq[i] for i in range(len(seq) - 1)): continue
                cost = sum(abs(np.angle(np.exp(1j * (na[slot[e]] - eang[e])))) for e in fe)
                if best is None or cost < best[0]: best = (cost, dict(slot))
            if best is None: raise RuntimeError('corner %s: no order-preserving fan' % (self.names[c] if hasattr(self, 'names') else c))
            for e in fe: self.res[(c, e)] = nb[best[1][e]]; taken.add(nb[best[1][e]])
            for e, x in fixed_nb.items(): self.res[(c, e)] = x
    def paths(self):
        blocked = np.zeros(NV, bool); blocked[self.cv] = True; self.P = {}
        self.reserve()
        for (c, e), x in self.res.items(): blocked[x] = True
        # corridors: every source vertex belongs to its nearest coarse quad (coarse quads = 2 triangles on the snapped corners); a coarse edge's path
        # may only use vertices of its (<= 2) quads, dilated 4 rings -> paths cannot wander into other parts of the body
        Cs = V[self.cv]; T = np.r_[self.Q[:, [0, 1, 2]], self.Q[:, [0, 2, 3]]]; _, ti, _ = igl.point_mesh_squared_distance(V, Cs, T); self.vq = ti % len(self.Q)
        def corridor(e):
            qs = [qi for qi, _ in self.E[e]]; m = np.isin(self.vq, qs)
            for _ in range(4): m = m | (G @ m.astype(float) > 0)
            return m
        self.corridor = corridor
        for e, (P, k) in self.fixed.items():                                       # tail-root ring: through the module ring points, from the reserved fan steps
            a, b = int(self.cv[e[0]]), int(self.cv[e[1]]); ra, rb = self.res[(e[0], e)], self.res[(e[1], e)]
            pts = P if np.linalg.norm(P[0] - V[a]) < np.linalg.norm(P[-1] - V[a]) else P[::-1]
            bl = blocked.copy(); vs = [a, ra]
            for p in list(pts[2:-2]) + [V[rb]]:
                t = GEO.snap(p) if not np.allclose(p, V[rb]) else rb
                if t == vs[-1] or (bl[t] and t != rb): continue
                bl[vs[-1]] = False; seg = local_path(vs[-1], t, bl | np.isin(np.arange(NV), vs[:-1]), factor=1.3, margin=0.8)
                if seg is None: raise RuntimeError('tail path')
                vs.extend(seg[1:].tolist())
            if vs[-1] != rb: raise RuntimeError('tail path end')
            vs = np.array(vs + [b]); self.P[e] = vs; blocked[vs] = True
        for (c, e), x in self.res.items(): blocked[x] = True
        def ends(e):
            a, b = int(self.cv[e[0]]), int(self.cv[e[1]]); return a, b, self.res[(e[0], e[1]) if False else (e[0], e)], self.res[(e[1], e)]
        def follow(P, a, b, bl):
            vs = [a]; pts = P[np.r_[np.arange(0, len(P), 3), len(P) - 1]]
            for p in pts[1:]:
                t = GEO.snap(p)
                if t == vs[-1] or (bl[t] and t != b): continue
                seg = local_path(vs[-1], t, bl, factor=1.4, margin=0.6, fallback=False, allow=self._allow)
                if seg is None: return None
                vs.extend(seg[1:].tolist())
            if vs[-1] != b:
                seg = local_path(vs[-1], b, bl, factor=1.4, margin=0.6, fallback=False, allow=self._allow)
                if seg is None: return None
                vs.extend(seg[1:].tolist())
            vs = np.array(vs); _, first = np.unique(vs, return_index=True)
            return vs if len(first) == len(vs) else None
        def route(e, use_arc):
            a, b, ra, rb = ends(e); bl = blocked.copy(); bl[ra] = False; bl[rb] = False
            if ra == rb: return None
            self._allow = corridor(e)
            if use_arc:
                P = self.arcs[e]; p = follow(P, ra, rb, bl)
            else:
                p = local_path(ra, rb, bl, plane=self.hint.get(e, {}).get('plane'), allow=self._allow)
                if p is None: p = local_path(ra, rb, bl, plane=self.hint.get(e, {}).get('plane'), fallback=True)
            if p is None: return None
            return np.r_[a, p, b]
        arc_ok = 0; arc_fail = []
        for e in sorted([e for e in self.E if e in self.arcs and e not in self.fixed], key=lambda e: len(self.arcs[e])):
            p = route(e, True)
            if p is None: arc_fail.append(e); continue
            self.P[e] = p; blocked[p[1:-1]] = True; arc_ok += 1
        self.log('ring arcs', arc_ok, 'failed (-> shortest paths)', len(arc_fail))
        JUNC = ('finger_web', 'toe_web', 'palm', 'forefoot', 'rostrum_cap', 'eye', 'finger_cap', 'thumb_cap', 'toe_cap')
        def prio(e):
            if 'prio' in self.hint.get(e, {}): return self.hint[e]['prio']
            labs = [self.lab[qi] for qi, _ in self.E[e]]; return 2 if any(l in JUNC for l in labs) else 1
        order = sorted([e for e in self.E if e not in self.fixed and e not in self.P], key=lambda e: (prio(e), np.linalg.norm(V[self.cv[e[0]]] - V[self.cv[e[1]]])))
        fails = []
        for e in order:
            p = route(e, False)
            if p is None: fails.append(e); continue
            self.P[e] = p; blocked[p[1:-1]] = True
        if fails:
            self.fails = fails; nm = getattr(self, 'names', None)
            raise RuntimeError('path failures (%d) %s' % (len(fails), [(nm[a], nm[b]) if nm else (a, b) for a, b in fails[:40]]))
        self.log('paths', len(self.P))
    def regions(self):
        """flood fill of faces with all path edges as cuts; per quad: region id of the face left of its first path edge"""
        cut = set()
        for e, p in self.P.items():
            for x, y in zip(p[:-1], p[1:]): cut.add((min(x, y), max(x, y)))
        TT = face_adj(); nF = len(F)
        # face graph without cut edges
        rows = []; cols = []
        for k in range(3):
            a, b = F[:, k], F[:, (k + 1) % 3]; nb = TT[:, k]
            keep = np.array([(min(x, y), max(x, y)) not in cut for x, y in zip(a, b)]) & (nb >= 0)
            rows.append(np.nonzero(keep)[0]); cols.append(nb[keep])
        rows = np.concatenate(rows); cols = np.concatenate(cols)
        Gf = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(nF, nF)); nc, flab = connected_components(Gf, directed=False)
        self.flab = flab; self.qreg = []
        for qi, q in enumerate(self.Q):
            a, b = int(q[0]), int(q[1]); e = (min(a, b), max(a, b)); p = self.P[e]
            if a > b: p = p[::-1]
            fi = face_of(int(p[0]), int(p[1]))
            self.qreg.append(flab[fi] if fi >= 0 else -1)
        from collections import Counter
        cnt = Counter(self.qreg); dup = [r for r, c in cnt.items() if c > 1]
        if dup or -1 in cnt:
            bad = [qi for qi, r in enumerate(self.qreg) if r in dup or r < 0]; raise RuntimeError('quads sharing a region / no region: %s' % bad[:20])
        self.log('regions ok; uncovered faces', int((~np.isin(flab, self.qreg)).sum()))
    def chords(self):
        """union-find over opposite quad edges -> chord classes; count = ceil(max path length / target) (fixed edges impose their count)"""
        keys = list(self.E); kid = {e: i for i, e in enumerate(keys)}; par = list(range(len(keys)))
        def find(i):
            while par[i] != i: par[i] = par[par[i]]; i = par[i]
            return i
        for q in self.Q:
            for k in (0, 1):
                e1 = (min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])); e2 = (min(q[k + 2], q[(k + 3) % 4]), max(q[k + 2], q[(k + 3) % 4]))
                par[find(kid[e1])] = find(kid[e2])
        cls = {}
        for e in keys: cls.setdefault(find(kid[e]), []).append(e)
        tgt = {}
        for qi, q in enumerate(self.Q):
            t = self.targets.get(self.lab[qi], 0.9)
            for k in range(4):
                e = (min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])); tgt[e] = min(tgt.get(e, 9e9), t)
        self.count = {}
        for c, es in cls.items():
            fx = [self.fixed[e][1] for e in es if e in self.fixed]
            if fx:
                if len(set(fx)) > 1: raise RuntimeError('conflicting fixed counts in a chord %s' % es)
                k = fx[0]
            else:
                k = max(1, int(np.ceil(max(self.plen(e) / tgt[e] for e in es))))
                if any(self.hint.get(e, {}).get('even') for e in es) and k % 2: k += 1
                kmin = max([self.hint.get(e, {}).get('min', 1) for e in es]); k = max(k, kmin)
            for e in es: self.count[e] = k
        self.chord_classes = cls
        self.log('chords', len(cls))
    def plen(self, e):
        p = V[self.P[e]]; return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())
    def build(self):
        """sample edges and quad interiors -> fine vertices (as (tri, bc)) + quads"""
        verts = []                                     # list of 3D points (embedded later)
        cid = {}
        for i, v in enumerate(self.cv): cid[i] = len(verts); verts.append(V[v])
        for e, (P, k) in self.fixed.items(): verts[cid[e[0]]] = P[0] if True else None
        # fixed edges carry exact module ring points (corner ends too)
        esamp = {}
        for e in self.E:
            k = self.count[e]
            if e in self.fixed:
                P, kk = self.fixed[e]; pts = P[1:-1]; verts[cid[e[0]]] = P[0]; verts[cid[e[1]]] = P[-1]
            else:
                pts, _ = polyline_samples(V[self.P[e]], k)
            ids = list(range(len(verts), len(verts) + len(pts))); verts.extend(list(pts)); esamp[e] = ids
        def edge_ids(a, b):
            e = (min(a, b), max(a, b)); ids = [cid[e[0]]] + esamp[e] + [cid[e[1]]]; return ids if a == e[0] else ids[::-1]
        quads = []; qlab = []; qsrc = []; self.grid = {}
        for qi, q in enumerate(self.Q):
            c0, c1, c2, c3 = [int(x) for x in q]; m = self.count[(min(c0, c1), max(c0, c1))]; n = self.count[(min(c1, c2), max(c1, c2))]
            if self.count[(min(c3, c2), max(c3, c2))] != m or self.count[(min(c0, c3), max(c0, c3))] != n: raise RuntimeError('count mismatch quad %d' % qi)
            bot = edge_ids(c0, c1); right = edge_ids(c1, c2); top = edge_ids(c3, c2); left = edge_ids(c0, c3)
            grid = -np.ones((m + 1, n + 1), int); grid[:, 0] = bot; grid[:, n] = top; grid[0, :] = left; grid[m, :] = right
            if m > 1 and n > 1:
                pts = self.param_sample(qi, m, n)
                for i in range(1, m):
                    for j in range(1, n): grid[i, j] = len(verts); verts.append(pts[(i, j)])
            for i in range(m):
                for j in range(n): quads.append([grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]]); qlab.append(self.lab[qi]); qsrc.append(qi)
            self.grid[qi] = grid
        self.fV = np.array(verts, float); self.fQ = np.array(quads, int); self.fQlab = qlab; self.fQsrc = np.array(qsrc)
        self.log('fine mesh', len(self.fV), 'V', len(self.fQ), 'Q')
    def param_sample(self, qi, m, n):
        """Tutte map of the quad's region to the unit square; return {(i,j): 3D point} for interior grid nodes"""
        q = [int(x) for x in self.Q[qi]]; reg = self.qreg[qi]; Fr = F[self.flab == reg]
        # boundary loop of the region in order c0 -> c1 -> c2 -> c3 using the 4 paths
        loop = []; uv = []
        corners_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for k in range(4):
            a, b = q[k], q[(k + 1) % 4]; e = (min(a, b), max(a, b)); p = self.P[e] if a == e[0] else self.P[e][::-1]
            _, s = polyline_samples(V[p], 2); s = s if a == e[0] else s
            # arc params along the directed path
            P_ = V[p]; ss = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P_, axis=0), axis=1))]; ss /= max(ss[-1], 1e-12)
            A, B = np.array(corners_uv[k], float), np.array(corners_uv[(k + 1) % 4], float)
            for i in range(len(p) - 1): loop.append(int(p[i])); uv.append(A + ss[i] * (B - A))
        loop = np.array(loop); uv = np.array(uv)
        if len(set(loop.tolist())) != len(loop): raise RuntimeError('quad %d boundary not simple' % qi)
        sub = np.unique(Fr); mp = -np.ones(NV, int); mp[sub] = np.arange(len(sub)); Fl = mp[Fr]
        if not np.isin(loop, sub).all(): raise RuntimeError('quad %d boundary vertices outside region' % qi)
        nv = len(sub); Ad = sp.coo_matrix((np.ones(6 * len(Fl)), (np.r_[Fl[:, 0], Fl[:, 1], Fl[:, 2], Fl[:, 1], Fl[:, 2], Fl[:, 0]], np.r_[Fl[:, 1], Fl[:, 2], Fl[:, 0], Fl[:, 0], Fl[:, 1], Fl[:, 2]])), shape=(nv, nv)).tocsr()
        Ad.data[:] = 1.0; deg = np.asarray(Ad.sum(1)).ravel(); Lu = sp.diags(deg) - Ad
        bi = mp[loop]; isb = np.zeros(nv, bool); isb[bi] = True; ii = np.nonzero(~isb)[0]
        X = np.zeros((nv, 2)); X[bi] = uv
        if len(ii):
            Lii = Lu[ii][:, ii].tocsc(); rhs = -Lu[ii][:, bi] @ uv
            from scipy.sparse.linalg import factorized
            sol = factorized(Lii); X[ii] = np.c_[sol(rhs[:, 0]), sol(rhs[:, 1])]
        # locate grid nodes
        import matplotlib.tri as mtri
        tri = mtri.Triangulation(X[:, 0], X[:, 1], Fl); finder = tri.get_trifinder()
        out = {}
        for i in range(1, m):
            for j in range(1, n):
                u, v = i / m, j / n; t = finder(u, v)
                if t < 0:
                    cc = X[Fl].mean(1); t = int(np.argmin(np.linalg.norm(cc - [u, v], axis=1)))
                a, b, c = X[Fl[t]]; T = np.c_[b - a, c - a]; l = np.linalg.solve(T, np.array([u, v]) - a); bc = np.r_[1 - l.sum(), l]
                bc = np.clip(bc, 0, 1); bc /= bc.sum(); out[(i, j)] = bc @ V[sub[Fl[t]]]
        return out
