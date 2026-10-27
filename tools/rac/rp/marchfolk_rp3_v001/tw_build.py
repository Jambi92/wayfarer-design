# tw_build.py BASE_CORE.npz OUT.npz [--mid 497 --x 1262 --d 1119 --sector 110 --fair N] : MPFB Family Base v005 toe-2 web-architecture correction
# (order 33a2dfe). BASE_CORE = the retained v004 architecture WITHOUT the rejected toe-2 closed ring (heel + hip + toe-3 + toe-3 pole slides, built by
# v004_build.py with RINGS_SPEC="hip_support:195:790,toe3_root:508:1264" --relocate-toe3).
# The toe-2 root support is a DORSAL RACETRACK instead of a closed ring: a short transverse support loop that crosses the toe-2 root only over the
# wide dorsal sector of the frozen-v003 root strip (loop MID | loop X, the strip the dorsal band path crosses) and returns through the adjacent distal
# strip (MID | D), closing with one corner-turn at each end of each strip (3-quad turn: one valence-3 interior vertex + one valence-5 corner). It never
# enters the thin plantar / web sectors where the rejected ring made aspect 12-13 half-quads. Sector: the MID-loop edges whose angle about the toe-2
# axis (family reference body, toe2_j1 station frame) is >= SECTOR degrees from the plantar direction, plus one turn quad at each end. Mirrored.
# New vertices: rung / loop-edge midpoints (2 parents) and turn centres (4 parents, the original quad), then re-expressed as on-surface barycentric
# rows (UV-chart guarded); --fair N: N tangential relaxation iterations of the racetrack patch (new vertices + turn corners + their 1-ring, seams fixed).
import sys, os, json, time, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v004_lib import *
arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
BASE, OUT = sys.argv[1:3]; MID, XL, DL, SECTOR, FAIR = arg('--mid', 497), arg('--x', 1262), arg('--d', 1119), arg('--sector', 110.0), arg('--fair', 0)
LAMBDA = arg('--lam', 0.3); FAIR_HOPS = arg('--hops', 1); DFRAC = arg('--dfrac', 0.5)   # D-strip rung split point (weight on the MID-loop end)
B = load_base(); bz = np.load(BASE); Q = np.asarray(bz['Q']).astype(np.int64); UV = bz['UV'].astype(float); M = csr(bz); nV0 = M.shape[0]
A = B['A']; Qh = B['Qh']; surf = Surface(A, Qh, B['chart']); surf.local_tris(Qh, len(A))
loops = closed_loops(Q, nV0); L3 = closed_loops(B['Q3'], B['M3'].shape[0]); idx = {frozenset(l.tolist()): i for i, l in enumerate(loops)}
lid = lambda v3: loops[idx[frozenset(L3[v3].tolist())]]
X0 = M @ A; mir = mirror_map(X0, 0.3)
from collections import defaultdict
def edge_faces(Qx):
    ef = defaultdict(list)
    for f, q in enumerate(Qx.tolist()):
        for k in range(4): ef[frozenset((q[k], q[(k + 1) % 4]))].append(f)
    return ef
nbr = defaultdict(set)
for q in Q.tolist():
    for k in range(4): nbr[q[k]].add(q[(k + 1) % 4]); nbr[q[(k + 1) % 4]].add(q[k])
meta = B['C']['MF-M-R']['meta']; JCa = {k: 0.5 * (np.array(B['C']['MF-M-R']['meta']['joint_cubes'][k]) + np.array(B['C']['MF-F-R']['meta']['joint_cubes'][k])) for k in meta['joint_cubes']}
LOG = dict(base=os.path.basename(BASE), base_sha256=sha(BASE), mid=MID, x=XL, d=DL, sector_deg=SECTOR, fair=FAIR, sides=[])
newrows = []; newuv = {}; prov = []; faces_new = []; faces_del = set(); nextv = [nV0]; turn_info = []
def newv(rowdict, parents, kind):
    v = nextv[0]; nextv[0] += 1; newrows.append(rowdict); prov.append(dict(vertex=v, kind=kind, parents=[int(p) for p in parents])); return v
def row_of(v): return dict(zip(M.indices[M.indptr[v]:M.indptr[v + 1]].tolist(), M.data[M.indptr[v]:M.indptr[v + 1]].tolist()))
def avg_rows(vs):
    out = {}
    for v in vs:
        for j, w in row_of(v).items(): out[j] = out.get(j, 0.0) + w / len(vs)
    return out
ef = edge_faces(Q)
for side in ('l', 'r'):
    Bm = lid(MID).tolist(); Xs = set(lid(XL).tolist()); Ds = set(lid(DL).tolist())
    if side == 'r': Bm = [int(mir[v]) for v in Bm]; Xs = {int(mir[v]) for v in Xs}; Ds = {int(mir[v]) for v in Ds}
    n = len(Bm); s_ = side; ax = unit(JCa['%s-toe-2-2' % s_] - JCa['%s-toe-2-1' % s_]); c = JCa['%s-toe-2-1' % s_]
    pp = unit(np.cross(ax, [0, 1.0, 0] if abs(ax[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(ax, pp))
    ang = np.array([np.degrees(np.arctan2((0.5 * (X0[Bm[k]] + X0[Bm[(k + 1) % n]]) - c) @ qq, (0.5 * (X0[Bm[k]] + X0[Bm[(k + 1) % n]]) - c) @ pp)) for k in range(n)])
    inS = np.abs(ang) >= SECTOR
    # contiguous dorsal block (cyclic) of sector edges; turn quads = one edge beyond each end
    ks = [k for k in range(n) if inS[k]]; assert ks, 'empty sector'
    start = [k for k in ks if not inS[(k - 1) % n]]; assert len(start) == 1, ('sector not contiguous', side, start)
    e0 = (start[0] - 1) % n; span = []
    k = start[0]
    while inS[k]: span.append(k); k = (k + 1) % n
    e1 = k; E = [e0] + span + [e1]
    partner = lambda v, S: [u for u in nbr[v] if u in S]
    def face_of(edge_k, S):
        a, b = Bm[edge_k], Bm[(edge_k + 1) % n]
        for f in ef[frozenset((a, b))]:
            if set(Q[f].tolist()) - {a, b} <= S: return f
        raise RuntimeError('no strip face')
    # split rungs at Bm vertices between consecutive edges of E
    mids = {}
    for strip, S in (('X', Xs), ('D', Ds)):
        for k in E[1:]:
            v = Bm[k]; u = partner(v, S); assert len(u) == 1, (side, strip, v, u); u = u[0]
            fr = DFRAC if strip == 'D' else 0.5; rw_ = {}
            for j, w in row_of(v).items(): rw_[j] = rw_.get(j, 0.0) + fr * w
            for j, w in row_of(u).items(): rw_[j] = rw_.get(j, 0.0) + (1 - fr) * w
            mids[(strip, v)] = newv(rw_, [v, u], 'rung_point_%s_%.2f' % (strip, fr)); mids[('edge', frozenset((v, u)))] = mids[(strip, v)]
    # loop-edge midpoints at the two turn edges (shared by the X and D turn quads)
    for k in (e0, e1):
        a, b = Bm[k], Bm[(k + 1) % n]; mids[('edge', frozenset((a, b)))] = newv(avg_rows([a, b]), [a, b], 'loop_edge_midpoint')
    for strip, S in (('X', Xs), ('D', Ds)):
        for k in E:
            f = face_of(k, S); q = Q[f].tolist(); faces_del.add(f); uvq = UV[f]
            b, buv = [], []
            for i in range(4):
                b.append(q[i]); buv.append(uvq[i]); e = frozenset((q[i], q[(i + 1) % 4]))
                if ('edge', e) in mids: b.append(mids[('edge', e)]); buv.append(0.5 * (uvq[i] + uvq[(i + 1) % 4]))
            assert len(b) == 6, (side, strip, k, len(b))
            mi = [i for i in range(6) if b[i] >= nV0]
            if k not in (e0, e1):                                    # full split: midpoints on opposite edges
                i, j = mi; assert (j - i) % 6 == 3
                faces_new.append(([b[(i + t) % 6] for t in range(4)], [buv[(i + t) % 6] for t in range(4)]))
                faces_new.append(([b[(j + t) % 6] for t in range(4)], [buv[(j + t) % 6] for t in range(4)]))
            else:                                                    # corner turn: midpoints on adjacent edges -> 3 quads around an interior vertex
                i = mi[0] if (mi[1] - mi[0]) % 6 == 2 else mi[1]; assert (b[(i + 2) % 6] in mi and b[(i + 2) % 6] >= nV0) or True
                if (mi[1] - mi[0]) % 6 == 2: i = mi[0]
                elif (mi[0] - mi[1]) % 6 == 2: i = mi[1]
                else: raise RuntimeError('turn midpoints not adjacent')
                x = newv(avg_rows(q), q, 'turn_centre_%s' % strip); xuv = uvq.mean(0)
                for a0 in (i, i + 2, i + 4):
                    faces_new.append(([b[(a0 + t) % 6] for t in range(3)] + [x], [buv[(a0 + t) % 6] for t in range(3)] + [xuv]))
                turn_info.append(dict(side=side, strip=strip, edge_k=int(k), centre=x, val5_corner=int(b[(i + 4) % 6]), shared_corner=int(b[(i + 1) % 6])))
    LOG['sides'].append(dict(side=side, mid_loop=Bm, sector_edges=[int(k) for k in span], turn_edges=[int(e0), int(e1)], edge_angles_deg=np.round(ang, 1).tolist()))
# ---- assemble topology / map / UV
keep = np.array([f not in faces_del for f in range(len(Q))]); Qn = np.r_[Q[keep], np.array([f[0] for f in faces_new], np.int64)]; UVn = np.r_[UV[keep], np.array([f[1] for f in faces_new])]
nV = nextv[0]; r_, c_, w_ = [], [], []
for i, rw in enumerate(newrows):
    for j, w in rw.items(): r_.append(i); c_.append(j); w_.append(w)
Mn = sp.vstack([M, sp.csr_matrix((w_, (r_, c_)), shape=(nV - nV0, M.shape[1]))]).tocsr()
# ---- project new vertices to the family reference surface (barycentric rows), UV-chart guarded
CU = corner_uvs(Qn, UVn, nV); Xl = Mn @ A; Ml = Mn.tolil(); uvset = {}; proj = np.zeros(nV, bool)
def bary_row(t, bc):
    row = {}
    for j, w in zip(surf.T[t], bc):
        if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
    return row
def project_vertex(v, P, Mx):
    if len(CU[v]) != 1: return None
    uv0 = np.array(next(iter(CU[v]))); sup = Mx.indices[Mx.indptr[v]:Mx.indptr[v + 1]]; cand = surf.tris_near(sup, 3); T = surf.T[cand]
    q, bc = closest_on_tris(np.repeat(P[None], len(cand), 0), A[T[:, 0]], A[T[:, 1]], A[T[:, 2]])
    corners = np.where(surf.tk[cand][:, None] == 0, [[0, 1, 2]], [[0, 2, 3]]); UVt = np.array([B['UVh'][surf.tq[c0]][k0] for c0, k0 in zip(cand, corners)])
    uvp = (UVt * bc[:, :, None]).sum(1); dd = np.where(np.linalg.norm(uvp - uv0, axis=1) < 4e-3, np.linalg.norm(q - P, axis=1), 1e9); j = int(np.argmin(dd))
    if dd[j] >= 1e9: return None
    return bary_row(int(cand[j]), bc[j]), uvp[j], q[j]
for v in range(nV0, nV):
    r = project_vertex(v, Xl[v], Mn)
    if r is None: continue
    rw, uvp, _ = r; Ml.rows[v] = sorted(rw); Ml.data[v] = [rw[j] for j in sorted(rw)]; uvset[v] = uvp; proj[v] = True
Mn = Ml.tocsr()
# ---- --opt: per-turn angle optimisation (order 33a2dfe §6 "local relocation of pole transitions within the same anatomy envelope"). For each corner
# turn the turn centre, its valence-5 corner and the two loop midpoints it joins are slid ON the family reference surface (2 tangent parameters each,
# displacement capped at 0.35 x local edge length) to minimise, summed over ALL FOUR configurations, the squared angle excess outside 50-130 deg of every
# incident quad plus aspect excess over 3. Each trial position is re-expressed as a barycentric row, so every configuration stays on its own source.
opt_set = set(); OPT = '--opt' in sys.argv or '--opt-wide' in sys.argv; OPT_WIDE = '--opt-wide' in sys.argv; OPT_CAP = arg('--opt-cap', 0.35); OPT_LO = arg('--opt-lo', 50.0)
if OPT:
    from scipy.optimize import minimize
    VH = [B['C'][c_]['Vh'] for c_ in CFG]; vf = defaultdict(list)
    for f, qd in enumerate(Qn.tolist()):
        for v in qd: vf[v].append(f)
    CU = corner_uvs(Qn, UVn, nV)
    def rowpos(rw, Vh): return sum(w * Vh[j] for j, w in rw.items())
    for t in [t_ for _ in range(arg('--opt-passes', 1)) for t_ in turn_info]:
        x = t['centre']; ids = [x, t['val5_corner']] + [u for u in set(Qn[vf[x]].ravel().tolist()) if u >= nV0 and u != x and len(CU[u]) == 1]
        if OPT_WIDE: ids += sorted(set(Qn[vf[x]].ravel().tolist()) | set(Qn[vf[t['val5_corner']]].ravel().tolist()))   # TW3: whole turn + valence-5 corner 1-ring
        ids = [v for v in dict.fromkeys(ids) if len(CU[v]) == 1]
        if '--opt-newonly' in sys.argv: ids = [v for v in ids if v >= nV0]
        fs = sorted({f for v in ids for f in vf[v]}); Xa = Mn @ A; N = vnormals(Xa, Qn)
        frames = []
        for v in ids:
            n_ = N[v]; e1 = unit(np.cross(n_, [1.0, 0, 0] if abs(n_[0]) < 0.9 else [0, 1.0, 0])); e2 = np.cross(n_, e1)
            el = np.mean([np.linalg.norm(Xa[v] - Xa[u]) for u in set(Qn[vf[v]].ravel().tolist()) if u != v]); frames.append((Xa[v].copy(), e1, e2, el))
        base_rows = {v: dict(zip(Mn.indices[Mn.indptr[v]:Mn.indptr[v + 1]].tolist(), Mn.data[Mn.indptr[v]:Mn.indptr[v + 1]].tolist())) for v in ids}
        fixedV = [Mn @ Vh for Vh in VH]
        def trial(p):
            rws = {}
            for i, v in enumerate(ids):
                X0_, e1, e2, el = frames[i]; d_ = p[2 * i] * e1 + p[2 * i + 1] * e2
                r = project_vertex(v, X0_ + el * d_, Mn); rws[v] = r[0] if r is not None else base_rows[v]
            return rws
        def cost(p):
            if np.abs(p).max() > OPT_CAP: return 1e6 + np.abs(p).max()
            rws = trial(p); tot = 0.0
            for k_, Vh in enumerate(VH):
                Vc = fixedV[k_]
                for v, rw in rws.items(): Vc[v] = rowpos(rw, Vh)
                ang_, asp_, _, _ = quality(Vc, Qn[fs]); tot += (np.clip(OPT_LO - ang_, 0, None) ** 2).sum() + (np.clip(ang_ - (180 - OPT_LO), 0, None) ** 2).sum() + 20 * (np.clip(45.5 - ang_, 0, None) ** 2).sum() + 20 * (np.clip(ang_ - 134.5, 0, None) ** 2).sum() + 50 * (np.clip(asp_ - 3, 0, None) ** 2).sum()
            for k_, Vh in enumerate(VH): fixedV[k_][ids] = (Mn[ids] @ Vh)
            return tot
        c0 = cost(np.zeros(2 * len(ids))); res_ = minimize(cost, np.zeros(2 * len(ids)), method='Powell', options=dict(maxiter=3000, xtol=1e-3, ftol=1e-4))
        rws = trial(res_.x); Ml = Mn.tolil()
        for v, rw in rws.items(): Ml.rows[v] = sorted(rw); Ml.data[v] = [rw[j] for j in sorted(rw)]; opt_set.add(int(v))
        Mn = Ml.tocsr(); t['opt'] = dict(vertices=[int(v) for v in ids], cost_before=round(float(c0), 1), cost_after=round(float(res_.fun), 1), max_shift_x_edge=round(float(np.abs(res_.x).max()), 3))
        print('  turn', t['side'], t['strip'], t['edge_k'], 'cost %.0f -> %.0f' % (c0, res_.fun), flush=True)
    for v in opt_set:
        if len(CU[v]) == 1:
            cols = Mn.indices[Mn.indptr[v]:Mn.indptr[v + 1]]
            for f_ in surf.vq[int(cols[0])]:
                for tri_c in ([0, 1, 2], [0, 2, 3]):
                    if set(int(c0_) for c0_ in cols) <= set(Qh[f_][tri_c].tolist()):
                        w_ = dict(zip(cols.tolist(), Mn.data[Mn.indptr[v]:Mn.indptr[v + 1]].tolist())); uvset[int(v)] = sum(w_.get(int(Qh[f_][k_]), 0.0) * B['UVh'][f_][k_] for k_ in tri_c); break
                else: continue
                break
# ---- --csmooth N: quad-centroid smoothing of the turn vertices (centre, valence-5 corner, the two joined midpoints): each moves to the mean of the
# centroids of its incident quads (equalises the corner angles around the valence-3 / valence-5 pair), tangentially, re-expressed on the reference surface.
CS = arg('--csmooth', 0)
if CS:
    vf2 = defaultdict(list)
    for f, qd in enumerate(Qn.tolist()):
        for v in qd: vf2[v].append(f)
    CU = corner_uvs(Qn, UVn, nV); tv = []
    for t in turn_info:
        x = t['centre']; tv += [x, t['val5_corner']] + [u for u in set(Qn[vf2[x]].ravel().tolist()) if u >= nV0 and u != x]
    tv = np.array(sorted({v for v in tv if len(CU[v]) == 1}), int)
    for _ in range(CS):
        Xa = Mn @ A; N = vnormals(Xa, Qn); Ml = Mn.tolil()
        for v in tv:
            tgt = np.mean([Xa[Qn[f]].mean(0) for f in vf2[v]], 0); dX = 0.5 * (tgt - Xa[v]); dX -= (dX @ N[v]) * N[v]
            r = project_vertex(int(v), Xa[v] + dX, Mn)
            if r is None: continue
            rw, uvp, _ = r; Ml.rows[v] = sorted(rw); Ml.data[v] = [rw[j] for j in sorted(rw)]; uvset[int(v)] = uvp; opt_set.add(int(v))
        Mn = Ml.tocsr()
# ---- optional conservative fairing of the racetrack patch
fair_set = set()
if FAIR:
    Adj = adjacency(Qn, nV); deg = np.asarray(Adj.sum(1)).ravel(); seed = set(range(nV0, nV)) | {t['val5_corner'] for t in turn_info}
    reg = set(seed)
    for _ in range(FAIR_HOPS):
        for v in list(reg): reg.update(Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]].tolist())
    CU = corner_uvs(Qn, UVn, nV); reg = np.array(sorted(v for v in reg if len(CU[v]) == 1), int); fair_set = set(reg.tolist())
    for _ in range(FAIR):
        Xa = Mn @ A; N = vnormals(Xa, Qn); Lp = (Adj[reg] @ Xa) / deg[reg, None]; dX = LAMBDA * (Lp - Xa[reg]); dX -= (dX * N[reg]).sum(1, keepdims=True) * N[reg]
        Ml = Mn.tolil()
        for i, v in enumerate(reg):
            r = project_vertex(int(v), Xa[v] + dX[i], Mn)
            if r is None: continue
            rw, uvp, _ = r; Ml.rows[v] = sorted(rw); Ml.data[v] = [rw[j] for j in sorted(rw)]; uvset[int(v)] = uvp
        Mn = Ml.tocsr()
for f, qd in enumerate(Qn):
    for k, v in enumerate(qd):
        if int(v) in uvset: UVn[f, k] = uvset[int(v)]
# ---- provenance / row classes (extends v004 classes: 5 = racetrack vertex barycentric, 6 = racetrack vertex linear (seam), 7 = retained vertex re-expressed by racetrack fairing)
rc = np.r_[bz['row_class'], np.zeros(nV - nV0, np.int8)]
for v in range(nV0, nV): rc[v] = 5 if proj[v] else 6
for v in fair_set | opt_set:
    if v < nV0 and rc[v] == 0: rc[v] = 7
legend = dict(json.loads(str(bz['log']))['row_class_legend']); legend.update({'5': 'toe-2 racetrack vertex, on-surface barycentric row', '6': 'toe-2 racetrack vertex, linear row (seam)', '7': 'retained vertex re-expressed barycentric by toe-2 racetrack turn optimisation / fairing'})
blog = json.loads(str(bz['log'])); LOG.update(dict(turns=turn_info, verts_added=int(nV - nV0), quads=int(len(Qn)), verts=int(nV), counts={k: int((rc == int(k)).sum()) for k in legend}, row_class_legend=legend,
                                                   retained=dict(heel=blog['heel'], rings=blog['rings'], relocation=blog['relocation'])))
assert len(set(map(tuple, np.sort(Qn, 1).tolist()))) == len(Qn)
np.savez_compressed(OUT, Q=Qn, UV=UVn, M_data=Mn.data, M_indices=Mn.indices, M_indptr=Mn.indptr, M_shape=np.array(Mn.shape), row_class=rc, ring_parents=bz['ring_parents'], ring_name=bz['ring_name'],
                    n_v003=int(bz['n_v003']), n_base=nV0, racetrack_provenance=json.dumps(prov), log=json.dumps(LOG))
print('saved', OUT, 'verts', nV, 'quads', len(Qn), 'added', nV - nV0, 'projected', int(proj[nV0:].sum()), 'turns', len(turn_info), 'faired', len(fair_set), 'optimised', len(opt_set))
