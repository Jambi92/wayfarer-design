# core3lib.py : RP3 v003 family-core library (order 103c832).
#   * shared base: native hm08 (both configurations), v002 topology + map M2, the configuration-average hm08 surface A = (M + F) / 2;
#   * station band audit (identical maths to audit.py `band()` / `J()`; the accepted RP2 program method) for fast iteration;
#   * surface-constrained vertex placement: a v003 vertex that is moved is stored as a barycentric point on ONE hm08 source triangle
#     (quad split 0-1-2 / 0-2-3, the R-6 triangulation), so its map row is 3 hm08 weights -- identical for both configurations, and the vertex lies
#     exactly on each configuration's own accepted source surface;
#   * UV-chart restriction (a moved vertex never leaves the UV chart it started in, so per-corner UVs stay continuous).
import json, numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import dijkstra, connected_components
W = '/tmp/claude-0/rt/m3'
def unit(v): return v / np.linalg.norm(v)
def load():
    B = {}
    for C in ('M', 'F'):
        n = np.load('%s/src/MF-%s-R_native.npz' % (W, C)); B[C] = dict(Vh=n['V'].astype(float), meta=json.loads(str(n['meta'])))
        if C == 'M': B['Qh'] = np.asarray(n['Q']); B['UVh'] = n['UV'].astype(float); B['src_index'] = n['src_index']
    v = np.load('%s/cand/MF-M-R_v002.npz' % W)
    B['Q2'] = np.asarray(v['Q']); B['UV2'] = v['UV'].astype(float)
    B['M2'] = sp.csr_matrix((v['M_data'], v['M_indices'], v['M_indptr']), shape=tuple(v['M_shape']))
    B['A'] = 0.5 * (B['M']['Vh'] + B['F']['Vh'])
    return B
# ------------------------------------------------------------------ hm08 triangles / UV charts
def hm08_tris(Qh):
    T = np.r_[Qh[:, [0, 1, 2]], Qh[:, [0, 2, 3]]]; tq = np.r_[np.arange(len(Qh)), np.arange(len(Qh))]; tk = np.r_[np.zeros(len(Qh), int), np.ones(len(Qh), int)]
    return T, tq, tk
def uv_charts(Qh, UVh):
    """hm08 quads connected across an edge whose two corner UVs match on both faces = same chart"""
    d = {}; r = []; c = []
    for f, q in enumerate(Qh):
        for k in range(4):
            a, b = q[k], q[(k + 1) % 4]; key = (min(a, b), max(a, b)); uva = tuple(np.round(UVh[f, k], 5)); uvb = tuple(np.round(UVh[f, (k + 1) % 4], 5))
            ent = (f, {a: uva, b: uvb})
            if key in d:
                g, m = d[key]
                if all(m[x] == ent[1][x] for x in key): r.append(f); c.append(g)
            else: d[key] = ent
    G = sp.coo_matrix((np.ones(len(r)), (r, c)), shape=(len(Qh), len(Qh)))
    return connected_components(G, directed=False)[1]
def closest_on_tris(p, A, B, C):
    """vectorised closest point on triangles (Ericson); returns point and barycentrics (u, v, w) for A, B, C"""
    ab = B - A; ac = C - A; ap = p - A; d1 = (ab * ap).sum(1); d2 = (ac * ap).sum(1)
    bp = p - B; d3 = (ab * bp).sum(1); d4 = (ac * bp).sum(1); cp = p - C; d5 = (ab * cp).sum(1); d6 = (ac * cp).sum(1)
    n = len(A); bc = np.zeros((n, 3)); done = np.zeros(n, bool)
    m = (d1 <= 0) & (d2 <= 0); bc[m] = [1, 0, 0]; done |= m
    m = ~done & (d3 >= 0) & (d4 <= d3); bc[m] = [0, 1, 0]; done |= m
    vc = d1 * d4 - d3 * d2; m = ~done & (vc <= 0) & (d1 >= 0) & (d3 <= 0); v = d1[m] / (d1[m] - d3[m]); bc[m] = np.c_[1 - v, v, 0 * v]; done |= m
    m = ~done & (d6 >= 0) & (d5 <= d6); bc[m] = [0, 0, 1]; done |= m
    vb = d5 * d2 - d1 * d6; m = ~done & (vb <= 0) & (d2 >= 0) & (d6 <= 0); w = d2[m] / (d2[m] - d6[m]); bc[m] = np.c_[1 - w, 0 * w, w]; done |= m
    va = d3 * d6 - d5 * d4; m = ~done & (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); w = (d4[m] - d3[m]) / ((d4[m] - d3[m]) + (d5[m] - d6[m])); bc[m] = np.c_[0 * w, 1 - w, w]; done |= m
    m = ~done; den = 1.0 / (va[m] + vb[m] + vc[m]); v = vb[m] * den; w = vc[m] * den; bc[m] = np.c_[1 - v - w, v, w]
    P = bc[:, :1] * A + bc[:, 1:2] * B + bc[:, 2:] * C; return P, bc
class Surface:
    """the configuration-average hm08 surface A, triangulated as the R-6 source; projection restricted to a UV chart"""
    def __init__(s, A, Qh, chart):
        s.A = A; s.T, s.tq, s.tk = hm08_tris(Qh); s.chart_t = chart[s.tq]; s.cen = A[s.T].mean(1); s.kd = cKDTree(s.cen)
    def local_tris(s, Qh, nh):
        """hm08 vertex -> triangles of the quads within 2 quad-rings (topological neighbourhood; prevents projection onto a touching neighbour digit)"""
        vq = [[] for _ in range(nh)]
        for f, q in enumerate(Qh):
            for v in q: vq[v].append(f)
        s.vq = vq; s.Qh = Qh
        # precomputed 3-quad-ring triangle neighbourhood of every hm08 vertex (sparse quad-vertex incidence powers)
        nq = len(Qh); I = sp.csr_matrix((np.ones(4 * nq), (np.repeat(np.arange(nq), 4), Qh.ravel())), shape=(nq, nh))
        Vv = (I.T @ I).tocsr(); Vv.data[:] = 1; R = Vv
        for _ in range(2): R = (R @ Vv).tocsr(); R.data[:] = 1
        F = (R @ I.T).tocsr()                                            # hm08 vertex -> quads within 3 rings
        s.nbq = [F.indices[F.indptr[v]:F.indptr[v + 1]] for v in range(nh)]
    def tris_near(s, verts, rings=3):
        fs = np.unique(np.concatenate([s.nbq[v] for v in verts])); nq = len(s.Qh); return np.r_[fs, fs + nq]
    def project_local(s, P, charts, supports):
        out = np.zeros_like(P); tri = np.zeros(len(P), int); bcs = np.zeros((len(P), 3))
        for i in range(len(P)):
            cand = s.tris_near(supports[i], 3); c2 = cand[s.chart_t[cand] == charts[i]]
            if len(c2): cand = c2
            T = s.T[cand]; q, bc = closest_on_tris(np.repeat(P[i:i + 1], len(cand), 0), s.A[T[:, 0]], s.A[T[:, 1]], s.A[T[:, 2]])
            j = np.argmin(np.linalg.norm(q - P[i], axis=1)); out[i] = q[j]; tri[i] = cand[j]; bcs[i] = bc[j]
        return out, tri, bcs
    def project(s, P, charts, k=24):
        _, idx = s.kd.query(P, k=k); out = np.zeros_like(P); tri = np.zeros(len(P), int); bcs = np.zeros((len(P), 3))
        for i in range(len(P)):
            cand = idx[i][s.chart_t[idx[i]] == charts[i]]
            if not len(cand): cand = idx[i]
            T = s.T[cand]; q, bc = closest_on_tris(np.repeat(P[i:i + 1], len(cand), 0), s.A[T[:, 0]], s.A[T[:, 1]], s.A[T[:, 2]])
            j = np.argmin(np.linalg.norm(q - P[i], axis=1)); out[i] = q[j]; tri[i] = cand[j]; bcs[i] = bc[j]
        return out, tri, bcs
# ------------------------------------------------------------------ station band audit (same maths as audit.py)
def topo(Q, nV):
    E = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); uE = np.unique(E, axis=0)
    val = np.bincount(uE.ravel(), minlength=nV); return uE, val
def stations(meta):
    H = {k: np.array(v) for k, v in meta['heads'].items()}; T_ = {k: np.array(v) for k, v in meta['tails'].items()}; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}
    S = [('neck', 0.5 * (H['neck_01'] + H['head']), np.array([0, 0, 1.0]), 2.0, 11, 4, None)]
    for s in ('l', 'r'):
        S += [('shoulder_' + s, H['upperarm_' + s], H['lowerarm_' + s] - H['upperarm_' + s], 3.0, 9, 5, None), ('elbow_' + s, H['lowerarm_' + s], H['hand_' + s] - H['lowerarm_' + s], 1.5, 7, 4, None),
              ('wrist_' + s, H['hand_' + s], H['middle_01_' + s] - H['hand_' + s], 1.0, 5, 3, None)]
        for fg in ('index', 'middle', 'ring', 'pinky'):
            b1, b2, b3 = ['%s_%02d_%s' % (fg, k, s) for k in (1, 2, 3)]
            S += [('%s_mcp_%s' % (fg, s), H[b1], H[b2] - H[b1], 0.8, 1.6, 3, None), ('%s_ip1_%s' % (fg, s), H[b2], H[b3] - H[b1], 0.5, 1.3, 2, None), ('%s_ip2_%s' % (fg, s), H[b3], T_[b3] - H[b2], 0.5, 1.3, 2, None)]
        S += [('thumb_mcp_' + s, H['thumb_02_' + s], H['thumb_03_' + s] - H['thumb_01_' + s], 0.8, 2.0, 3, None), ('thumb_ip_' + s, H['thumb_03_' + s], T_['thumb_03_' + s] - H['thumb_02_' + s], 0.5, 1.6, 2, None)]
        S += [('hip_' + s, H['thigh_' + s], H['calf_' + s] - H['thigh_' + s], 3.0, 12, 5, None), ('knee_' + s, H['calf_' + s], H['foot_' + s] - H['calf_' + s], 1.5, 9, 4, None),
              ('ankle_' + s, H['foot_' + s], H['foot_' + s] - H['calf_' + s], 1.5, 7, 3, None)]
        for t in range(1, 6):
            for j in (1, 2, 3):
                k0, k1, k2 = '%s-toe-%d-%d' % (s, t, j - 1), '%s-toe-%d-%d' % (s, t, j), '%s-toe-%d-%d' % (s, t, j + 1)
                if k1 in JC and k2 in JC:
                    a_ = JC[k2] - (JC[k0] if k0 in JC else JC[k1]); rr = 0.5 * np.linalg.norm(JC[k2] - JC[k1]) + 0.6
                    S.append(('toe%d_j%d_%s' % (t, j, s), JC[k1], a_, 0.4, rr * 1.3, 2, 1.15 * rr))
    return S
class Auditor:
    def __init__(s, V, Q):
        s.V = V; s.Q = Q; nV = len(V); s.uE, s.val = topo(Q, nV); s.poles = np.nonzero(s.val != 4)[0]
        wE = np.linalg.norm(V[s.uE[:, 0]] - V[s.uE[:, 1]], axis=1); s.wE = wE
        s.G = sp.coo_matrix((np.r_[wE, wE], (np.r_[s.uE[:, 0], s.uE[:, 1]], np.r_[s.uE[:, 1], s.uE[:, 0]])), shape=(nV, nV)).tocsr()
        fn = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]) * 0.5; VN = np.zeros_like(V)
        for k in range(4): np.add.at(VN, Q[:, k], fn)
        s.VN = VN / np.maximum(np.linalg.norm(VN, axis=1), 1e-12)[:, None]; s.kd = cKDTree(V); s.e0 = V[s.uE[:, 0]]
    def surf(s, p, dirn, Rr):
        V = s.V; cand = s.kd.query_ball_point(p + dirn * Rr * 0.5, Rr * 0.9)
        if not cand: return int(s.kd.query(p)[1])
        cand = np.array(cand); t = (V[cand] - p) @ dirn; off = np.linalg.norm((V[cand] - p) - np.outer(t, dirn), axis=1)
        ok = (s.VN[cand] @ dirn > 0.3); sc = np.where(ok, off, 1e9); return int(cand[np.argmin(sc)])
    def band(s, c, d, Wd, Rr, Rp=None):
        V = s.V; d = unit(d); pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); res = []; merged = 0; paths = []
        for side in (pp, -pp, qq, -qq):
            a_ = s.surf(c - d * Wd, side, Rr); b_ = s.surf(c + d * Wd, side, Rr)
            if np.linalg.norm(V[a_] - V[b_]) < 0.7 * 2 * Wd: merged += 1; continue
            _, pred = dijkstra(s.G, indices=a_, return_predecessors=True, limit=4 * Wd + 3 * Rr)
            if pred[b_] < 0: continue
            path = [b_]
            while path[-1] != a_: path.append(int(pred[path[-1]]))
            P = V[path]; e = np.diff(P, axis=0); res.append(int((np.abs(e @ d) > 0.5 * np.linalg.norm(e, axis=1)).sum())); paths.append(path)
        near = np.nonzero(np.linalg.norm(s.e0 - c, axis=1) < Rr)[0]; h = float(np.median(s.wE[near])) if len(near) else 0.3
        Rp = Rr if Rp is None else Rp; PV = V[s.poles]; pb = (PV - c) @ d; pr = np.linalg.norm((PV - c) - np.outer(pb, d), axis=1)
        sel = (np.abs(pb) <= 2 * h) & (pr <= Rp); cre = (np.abs(pb) <= 0.5 * h) & (pr <= Rp)
        return dict(loops=int(min(res)) if res else 0, loops_by_side=res, merged=merged, within2=int(sel.sum()), crease=int(cre.sum()), h=h, d=d,
                    pole_ids=s.poles[sel].tolist(), pole_t=(pb[sel] / h).tolist(), paths=paths,
                    nearest_pole_loops=float(np.min(np.abs(pb[pr <= Rp]) / h)) if (pr <= Rp).any() else None)
    def run(s, S):
        out = {}
        for nm, c, d, Wd, Rr, need, Rp in S:
            r = s.band(np.asarray(c, float), np.asarray(d, float), Wd, Rr, Rp); r['required'] = need; r['c'] = np.asarray(c, float)
            r['firm'] = bool(r['loops'] >= need and r['crease'] == 0); r['strict'] = bool(r['loops'] >= need and r['within2'] == 0); out[nm] = r
        return out
# ------------------------------------------------------------------ quad quality
def quality(V, Q):
    ang = []
    for k in range(4):
        p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sides = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sides.max(1) / np.maximum(sides.min(1), 1e-9)
    return ang, asp, (ang.min(1) < 45) | (ang.max(1) > 135), asp > 4
# ------------------------------------------------------------------ closed edge loops (topology only) + encircling rings (audit.py secondary measure)
def closed_loops(Q, nV):
    from collections import defaultdict
    uE, val = topo(Q, nV); nbr = [[] for _ in range(nV)]
    for e in uE: nbr[e[0]].append(e[1]); nbr[e[1]].append(e[0])
    fe = defaultdict(set)
    for fi, q in enumerate(Q):
        for k in range(4): fe[(min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))].add(fi)
    def nxt(prev, v):
        if val[v] != 4: return None
        fp = fe[(min(prev, v), max(prev, v))]
        for u in nbr[v]:
            if u == prev: continue
            if not (fe[(min(u, v), max(u, v))] & fp): return u
        return None
    seen_e = set(); loops = []
    for e in map(tuple, uE):
        if e in seen_e: continue
        path = [e[0], e[1]]; seen_e.add(e); closed = False
        while True:
            u = nxt(path[-2], path[-1])
            if u is None: break
            ek = (min(path[-1], u), max(path[-1], u))
            if u == path[0]: closed = True; seen_e.add(ek); break
            if ek in seen_e: break
            seen_e.add(ek); path.append(u)
        if closed: loops.append(np.array(path))
        else:
            b = [e[1], e[0]]
            while True:
                u = nxt(b[-2], b[-1])
                if u is None: break
                ek = (min(b[-1], u), max(b[-1], u))
                if ek in seen_e: break
                seen_e.add(ek); b.append(u)
    return loops
def ring_stations(meta):
    H = {k: np.array(v) for k, v in meta['heads'].items()}; T_ = {k: np.array(v) for k, v in meta['tails'].items()}; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}; JR = []
    for s in ('l', 'r'):
        JR += [('shoulder_' + s, H['upperarm_' + s], T_['upperarm_' + s] - H['upperarm_' + s], 12.0, 6.0), ('elbow_' + s, H['lowerarm_' + s], T_['lowerarm_' + s] - H['upperarm_' + s], 7.0, 4.0),
               ('wrist_' + s, H['hand_' + s], T_['hand_' + s] - H['lowerarm_' + s], 5.0, 2.5), ('hip_' + s, H['thigh_' + s], T_['thigh_' + s] - H['thigh_' + s], 16.0, 8.0),
               ('knee_' + s, H['calf_' + s], T_['calf_' + s] - H['thigh_' + s], 9.0, 5.0), ('ankle_' + s, H['foot_' + s], T_['calf_' + s] - H['calf_' + s], 7.0, 3.5)]
        for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
            for k, lab in enumerate(('knuckle', 'ip1', 'ip2')):
                b = '%s_%02d_%s' % (fg, k + 1, s); JR.append(('%s_%s_%s' % (fg, lab, s), H[b], T_[b] - H[b], 1.6, 0.8 if k else 1.0))
        for t in range(1, 6):
            for j in (1, 2, 3):
                k1, k2 = '%s-toe-%d-%d' % (s, t, j), '%s-toe-%d-%d' % (s, t, j + 1)
                if k1 in JC and k2 in JC: JR.append(('toe%d_j%d_%s' % (t, j, s), JC[k1], JC[k2] - JC[k1], 1.6, 0.6))
    JR += [('neck', 0.5 * (H['neck_01'] + H['head']), H['head'] - H['neck_01'], 9.0, 0.5 * np.linalg.norm(H['head'] - H['neck_01']) + 1.0)]
    return JR
def encircling(V, loops, c, d, rmax, win):
    d = d / np.linalg.norm(d); out = []
    u = np.cross(d, [0, 0, 1.0]) if abs(d[2]) < 0.9 else np.cross(d, [1.0, 0, 0]); u /= np.linalg.norm(u); vv = np.cross(d, u)
    for li, L in enumerate(loops):
        P = V[L] - c; t = P @ d; rad = P - np.outer(t, d); rr = np.linalg.norm(rad, axis=1)
        if rr.max() > rmax or abs(t.mean()) > win or rr.min() < 1e-6: continue
        th = np.arctan2(rad @ vv, rad @ u); dth = np.diff(np.r_[th, th[0]]); dth = (dth + np.pi) % (2 * np.pi) - np.pi
        if abs(abs(dth.sum()) - 2 * np.pi) < 0.5: out.append(li)
    return out
def ring_name(nm):
    if '_mcp_' in nm: return nm.replace('thumb_mcp_', 'thumb_ip1_') if nm.startswith('thumb') else nm.replace('_mcp_', '_knuckle_')
    if nm.startswith('thumb_ip_'): return nm.replace('thumb_ip_', 'thumb_ip2_')
    return nm
def full_s7(V, Q, meta, loops, S=None, JR=None):
    """joint_s7 verdicts exactly as audit.py: loops = max(closed encircling rings, band loops); firm = loops >= need and no crease pole"""
    S = S or stations(meta); JR = JR or ring_stations(meta); au = Auditor(V, Q).run(S)
    rc = {}
    for nm, c, d, rmax, win in JR:
        # cheap prefilter on loop centroids
        rc[nm] = len(encircling(V, loops, c, d, rmax, win))
    for k, r in au.items():
        r['closed_rings'] = rc.get(ring_name(k), 0); r['loops_s7'] = max(r['closed_rings'], r['loops'])
        r['firm'] = bool(r['loops_s7'] >= r['required'] and r['crease'] == 0); r['strict'] = bool(r['loops_s7'] >= r['required'] and r['within2'] == 0)
    return au
# ------------------------------------------------------------------ v003 state: map rows, parents, charts, pins
def v002_parents(B):
    """hm08 parent quad of every v002 face (max overlap of the face's map support with the quad's vertices) and the UV chart of every v002 vertex"""
    M2 = B['M2']; Qh = B['Qh']; Q2 = B['Q2']; nV = M2.shape[0]
    vq = {}
    for f, q in enumerate(Qh):
        for v in q: vq.setdefault(int(v), []).append(f)
    par = np.zeros(len(Q2), int)
    for f, q in enumerate(Q2):
        cols = set()
        for v in q: cols.update(M2.indices[M2.indptr[v]:M2.indptr[v + 1]].tolist())
        cnt = {}
        for c in cols:
            for g in vq[c]: cnt[g] = cnt.get(g, 0) + 1
        par[f] = max(cnt, key=cnt.get)
    return par
def vertex_charts(Q2, par, chart, UV2, nV):
    vc = -np.ones(nV, int); seam = np.zeros(nV, bool); vuv = {}
    for f, q in enumerate(Q2):
        c = chart[par[f]]
        for k, v in enumerate(q):
            if vc[v] >= 0 and vc[v] != c: seam[v] = True
            vc[v] = c; u = tuple(np.round(UV2[f, k], 5))
            if v in vuv and vuv[v] != u: seam[v] = True
            vuv[v] = u
    return vc, seam
def adjacency(Q, nV):
    uE, _ = topo(Q, nV); return sp.coo_matrix((np.ones(2 * len(uE)), (np.r_[uE[:, 0], uE[:, 1]], np.r_[uE[:, 1], uE[:, 0]])), shape=(nV, nV)).tocsr()
def vnormals(V, Q):
    fn = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]); VN = np.zeros_like(V)
    for k in range(4): np.add.at(VN, Q[:, k], fn)
    return VN / np.maximum(np.linalg.norm(VN, axis=1), 1e-12)[:, None]
def build_map(M2, moved, surf):
    """M3 = M2 with the rows of moved vertices replaced by their barycentric hm08 rows. moved: {v: (tri, bary)}"""
    M = M2.tolil(copy=True)
    for v, (t, bc) in moved.items():
        row = {}
        for j, w in zip(surf.T[t], bc):
            if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
        M.rows[v] = sorted(row); M.data[v] = [row[j] for j in sorted(row)]
    return M.tocsr()
# ------------------------------------------------------------------ topology: closed-strip ring insertion (linear, quad-only), mirror map
def strip_faces(Q, A, B):
    sa, sb = set(A), set(B); m = np.array([sum(v in sa for v in q) == 2 and sum(v in sb for v in q) == 2 for q in Q.tolist()]); return np.nonzero(m)[0]
def insert_ring(Q, UV, M, A, B):
    """split every quad of the closed strip between adjacent closed loops A and B through the midpoints of its A-B edges; new rows = edge midpoints"""
    sa = set(A); fs = strip_faces(Q, A, B)
    if len(fs) != len(A): return None
    nV = M.shape[0]; mid = {}; ext = []; Qn = []; UVn = []; fset = set(fs.tolist())
    for qi, q in enumerate(Q.tolist()):
        if qi not in fset: Qn.append(q); UVn.append(UV[qi]); continue
        conn = [k for k in range(4) if (q[k] in sa) != (q[(k + 1) % 4] in sa)]; k1, k2 = conn; pts = []
        for k in (k1, k2):
            key = (min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))
            if key not in mid: mid[key] = nV + len(ext); ext.append(key)
            pts.append(mid[key])
        uv = UV[qi]; m1 = (uv[k1] + uv[(k1 + 1) % 4]) / 2; m2 = (uv[k2] + uv[(k2 + 1) % 4]) / 2
        Qn.append([q[k1], pts[0], pts[1], q[(k2 + 1) % 4]]); UVn.append([uv[k1], m1, m2, uv[(k2 + 1) % 4]])
        Qn.append([pts[0], q[(k1 + 1) % 4], q[k2], pts[1]]); UVn.append([m1, uv[(k1 + 1) % 4], uv[k2], m2])
    r_ = []; c_ = []; v_ = []
    for i, (p, q) in enumerate(ext): r_ += [i, i]; c_ += [p, q]; v_ += [0.5, 0.5]
    Mx = sp.csr_matrix((v_, (r_, c_)), shape=(len(ext), nV)) @ M
    return np.array(Qn, np.int64), np.array(UVn), sp.vstack([M, Mx]).tocsr(), ext
def mirror_map(X, tol=0.05):
    P = X * [-1, 1, 1]; d, i = cKDTree(X).query(P); i[d > tol] = -1; return i
