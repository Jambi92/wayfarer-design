# v004_build.py OUT.npz [--relocate-toe3] : MPFB Family Base v004 = margin-hardening successor of FROZEN Marchfolk v003 (order a18371c §4-§8).
# One shared family topology; every operation is identical for every family race (rows of the hm08 -> family map) and mirrored left / right.
#  A  posterior-heel rows (§4): every foot vertex behind the ankle whose v003 row is a LINEAR hm08 QUAD-CENTRE row (4 x 0.25 on one hm08 quad) and
#     whose v003 production -> source deviation exceeds 1.0 mm on ANY of the four accepted configurations is re-expressed as the on-source-surface
#     barycentric point of the same hm08 quad (closest point on the quad's two R-6 triangles to the old linear point, on the family reference surface).
#     Topology unchanged. The original and the new row are recorded.
#  B  hip support ring (§5) and C  toe-2 / toe-3 root rings (§6): one closed ring split into one closed quad strip per band (frozen-v003 loop pairs,
#     chosen by v004_ringsearch.py on all four configurations), mirrored. New vertices: linear edge-midpoint rows, then re-expressed as the closest
#     on-source-surface barycentric point (UV-chart and topological-neighbourhood restricted; a seam vertex, or one whose surface UV would differ from
#     its interpolated UV, keeps the linear midpoint row).
#  P  (--relocate-toe3) toe-3 MTP crease poles: the forefoot poles that D3 assigns to toe 3 and that sit inside the D4-scaled toe3_j1 crease window on
#     any configuration are slid distally along the toe-3 axis on the family reference surface (barycentric rows, cosine falloff over 2 rings).
import sys, os, json, time, numpy as np, scipy.sparse as sp, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v004_lib import *
OUT = sys.argv[1]; t0 = time.time()
B = load_base(); Q = B['Q3'].copy(); UV = B['UV3'].copy(); M = B['M3'].copy(); nV0 = M.shape[0]; Qh = B['Qh']; A = B['A']
surf = Surface(A, Qh, B['chart']); surf.local_tris(Qh, len(A)); X = M @ A; mir = mirror_map(X, 0.3); loops0 = closed_loops(Q, nV0)
LOG = dict(base=dict(frozen_map=os.path.basename(FROZEN_MAP), frozen_map_sha256=B['frozen_map_sha'], verts=int(nV0), quads=int(len(Q))), heel=[], rings=[], relocation=[])
def quad_of(cols):
    """hm08 quad whose 4 vertices are exactly cols"""
    s = set(int(c) for c in cols); cand = set(surf.vq[int(cols[0])])
    for f in cand:
        if set(Qh[f].tolist()) == s: return int(f)
    return None
def bary_row(t, bc):
    row = {}
    for j, w in zip(surf.T[t], bc):
        if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
    return row
def set_row(Ml, v, row): Ml.rows[v] = sorted(row); Ml.data[v] = [row[j] for j in sorted(row)]
# ------------------------------------------------------------------ A: posterior-heel quad-centre rows
dev = {}
for cid in CFG:
    r6 = np.load(R6[cid]); src = trimesh.Trimesh(r6['V'].astype(float), r6['F'], process=False); _, d, _ = trimesh.proximity.closest_point(src, M @ B['C'][cid]['Vh']); dev[cid] = d
    if cid == 'MF-M-R': w = {k[2:]: r6[k][B['src_index']] for k in r6.files if k.startswith('w_')}
dmax = np.max([dev[c] for c in CFG], 0)
H = {k: np.array(v) for k, v in B['C']['MF-M-R']['meta']['heads'].items()}
heel = []
for s in ('l', 'r'):
    foot = (M @ (w['foot_' + s] + w['ball_' + s])) > 0.5; fd = H['ball_' + s] - H['foot_' + s]; fd[2] = 0; fd = unit(fd)
    behind = ((M @ B['C']['MF-M-R']['Vh']) - H['foot_' + s]) @ fd < 0
    for v in np.nonzero(foot & behind & (dmax > 0.10))[0]:
        cols = M.indices[M.indptr[v]:M.indptr[v + 1]]; ws = M.data[M.indptr[v]:M.indptr[v + 1]]
        if len(cols) == 4 and np.allclose(ws, 0.25) and quad_of(cols) is not None: heel.append(int(v))
heel = sorted(heel); assert sorted(int(mir[v]) for v in heel) == heel, 'heel set not mirror-closed'
Ml = M.tolil(copy=True)
for v in heel:
    cols = M.indices[M.indptr[v]:M.indptr[v + 1]]; f = quad_of(cols); tt = np.array([f, f + len(Qh)])
    T = surf.T[tt]; q, bc = closest_on_tris(np.repeat(X[v:v + 1], 2, 0), A[T[:, 0]], A[T[:, 1]], A[T[:, 2]]); j = int(np.argmin(np.linalg.norm(q - X[v], axis=1)))
    row = bary_row(int(tt[j]), bc[j]); old = {int(c): float(x) for c, x in zip(cols, M.data[M.indptr[v]:M.indptr[v + 1]])}; set_row(Ml, v, row)
    LOG['heel'].append(dict(vertex=v, hm08_quad=f, old_row=old, new_row=row, v003_dev_mm={c: round(float(dev[c][v] * 10), 4) for c in CFG}, moved_on_reference_cm=round(float(np.linalg.norm(q[j] - X[v])), 4)))
M = Ml.tocsr(); print('A heel rows', heel, '%.0fs' % (time.time() - t0), flush=True)
# ------------------------------------------------------------------ B / C: rings (frozen-v003 loop ids, left side; mirrored)
RINGS = [('hip_support', 195, 790), ('toe2_root', int(os.environ.get('TOE2A', 497)), int(os.environ.get('TOE2B', 1262))), ('toe3_root', 508, 1264)]
parents = []; ring_of = []
for nm, la, lb in RINGS:
    for side, (A_, B_) in (('l', (loops0[la], loops0[lb])), ('r', (mir[loops0[la]], mir[loops0[lb]]))):
        assert (A_ >= 0).all() and (B_ >= 0).all(), nm
        if side == 'r' and set(A_.tolist()) == set(loops0[la].tolist()) and set(B_.tolist()) == set(loops0[lb].tolist()):
            LOG['rings'][-1]['self_mirrored'] = True; LOG['rings'][-1]['name'] = nm + '_lr'; ring_of[-LOG['rings'][-1]['verts_added']:] = [nm + '_lr'] * LOG['rings'][-1]['verts_added']; continue   # one symmetric ring serves both sides
        out = insert_ring(Q, UV, M, A_.tolist(), B_.tolist()); assert out is not None, (nm, side)
        Q, UV, M, ext = out; parents += [tuple(int(x) for x in e) for e in ext]; ring_of += [nm + '_' + side] * len(ext)
        LOG['rings'].append(dict(name=nm + '_' + side, v003_loop_a=A_.tolist(), v003_loop_b=B_.tolist(), strip_quads=len(A_), verts_added=len(ext)))
nV = M.shape[0]; new = np.arange(nV0, nV); print('rings: verts', nV, 'quads', len(Q), '%.0fs' % (time.time() - t0), flush=True)
# project new ring vertices onto the family reference surface
CU = corner_uvs(Q, UV, nV); Xl = M @ A; Ml = M.tolil(copy=True); proj = np.zeros(nV, bool); uvset = {}
for v in new:
    if len(CU[v]) != 1: continue                                     # seam vertex: keep the linear row
    uv0 = np.array(next(iter(CU[v]))); sup = M.indices[M.indptr[v]:M.indptr[v + 1]]; cand = surf.tris_near(sup, 3); T = surf.T[cand]
    q, bc = closest_on_tris(np.repeat(Xl[v:v + 1], len(cand), 0), A[T[:, 0]], A[T[:, 1]], A[T[:, 2]])
    corners = np.where(surf.tk[cand][:, None] == 0, [[0, 1, 2]], [[0, 2, 3]]); UVt = np.array([B['UVh'][surf.tq[c_]][k_] for c_, k_ in zip(cand, corners)])   # (n,3,2) hm08 corner UVs
    uvp = (UVt * bc[:, :, None]).sum(1); ok = np.linalg.norm(uvp - uv0, axis=1) < 2e-3
    if not ok.any(): continue
    dd = np.where(ok, np.linalg.norm(q - Xl[v], axis=1), 1e9); j = int(np.argmin(dd)); set_row(Ml, v, bary_row(int(cand[j]), bc[j])); proj[v] = True; uvset[int(v)] = uvp[j]
M = Ml.tocsr()
for f, qd in enumerate(Q):
    for k, v in enumerate(qd):
        if int(v) in uvset: UV[f, k] = uvset[int(v)]
print('ring vertices projected', int(proj.sum()), 'of', len(new), 'max move cm', float(np.linalg.norm((M @ A)[new] - Xl[new], axis=1).max()), flush=True)
# ------------------------------------------------------------------ F: conservative fairing of the toe-root ring patches (+ toe-3 MTP crease poles)
# The toe-root strips taper towards the webs, so a midpoint split doubles the aspect of the narrow strip quads. Each toe patch (new ring + its two
# frozen loops + FAIR_HOPS neighbour rings, both sides, seam vertices fixed) is relaxed tangentially on the family reference surface (umbrella /
# parallelogram mix, every iterate re-expressed as barycentric rows). With --relocate-toe3 the toe-3 MTP poles that D3 assigns to toe 3 and that sit in
# the D4-scaled toe3_j1 crease window on any configuration are first slid distally along the toe-3 axis (TOE3_SHIFT_CM, cosine falloff over 2 rings).
# A variant is kept only if, on ALL FOUR configurations, the toe target stations do not lose loops / gain own-digit crease poles; among those the one
# with the fewest T-4 violations in the patch (sum over configurations) wins; the no-fairing state is always a candidate.
from val2lib import evaluate, REF_STATURE_CM
Adj = adjacency(Q, nV); deg = np.asarray(Adj.sum(1)).ravel(); lp = closed_loops(Q, nV); CU = corner_uvs(Q, UV, nV); seam = np.array([len(x) > 1 for x in CU])
def vchart(v, Mx):
    cs = {}
    for c_ in Mx.indices[Mx.indptr[v]:Mx.indptr[v + 1]]:
        for f_ in surf.vq[int(c_)]: cs[int(B['chart'][f_])] = cs.get(int(B['chart'][f_]), 0) + 1
    return max(cs, key=cs.get)
def hops_from(seed, K):
    d = {int(v): 0 for v in seed}; fr = list(d)
    for h_ in range(1, K + 1):
        nf = []
        for u in fr:
            for w_ in Adj.indices[Adj.indptr[u]:Adj.indptr[u + 1]]:
                if int(w_) not in d: d[int(w_)] = h_; nf.append(int(w_))
        fr = nf
    return d
TARGETS = ['toe2_j1_l', 'toe2_j1_r', 'toe3_j1_l', 'toe3_j1_r']
def target_state(Mx):
    out = {}
    for cid in CFG:
        e = evaluate(Mx @ B['C'][cid]['Vh'], Q, B['C'][cid]['meta'], REF_STATURE_CM, names=TARGETS, loops=lp)['stations']
        out[cid] = {k: (e[k]['loops_v2'], len(e[k]['crease_poles_own_digit']), [x.get('loops') if x['defined'] else None for x in e[k]['sides']]) for k in TARGETS}
    return out
def patch_t4(Mx, faces):
    n = 0; mx = 0.0
    for cid in CFG:
        _, asp, va, vs = quality(Mx @ B['C'][cid]['Vh'], Q[faces]); n += int((va | vs).sum()); mx = max(mx, float(asp.max()))
    return n, mx
def write_rows(Ml, ids, Pp, tri, bc):
    for i, t_, b_ in zip(ids, tri, bc): set_row(Ml, int(i), bary_row(int(t_), b_))
def fair(Mx, region, it, lam, para):
    Mx = Mx.tolil(copy=True).tocsr(); region = np.array(sorted(region), int)
    rq = np.unique(np.nonzero(np.isin(Q, region))[0]); chs = np.array([vchart(int(v), Mx) for v in region])
    for _ in range(it):
        Xa = Mx @ A; N = vnormals(Xa, Q); L = (Adj[region] @ Xa) / deg[region, None]; tgt = L
        if para > 0:
            acc = np.zeros((nV, 3)); cnt = np.zeros(nV); qq_ = Q[rq]
            for k in range(4): pr = Xa[qq_[:, (k - 1) % 4]] + Xa[qq_[:, (k + 1) % 4]] - Xa[qq_[:, (k + 2) % 4]]; np.add.at(acc, qq_[:, k], pr); np.add.at(cnt, qq_[:, k], 1)
            tgt = (1 - para) * L + para * acc[region] / np.maximum(cnt[region], 1)[:, None]
        dX = lam * (tgt - Xa[region]); dX -= (dX * N[region]).sum(1, keepdims=True) * N[region]
        P = Xa[region] + dX; sups = [Mx.indices[Mx.indptr[v]:Mx.indptr[v + 1]].tolist() for v in region]
        Pp, tri, bc = surf.project_local(P, chs, sups); Ml_ = Mx.tolil(); write_rows(Ml_, region, Pp, tri, bc); Mx = Ml_.tocsr()
    return Mx
REL = []
if '--relocate-toe3' in sys.argv:
    # minimal deterministic slide: each pole moves along the toe-3 axis AWAY from the crease plane (sign of its axial offset where it violates) by the
    # smallest step (0.02 cm grid) that puts it at |axial| >= 0.75 local loop (or outside the D4 pole radius) on EVERY configuration; falloff over 1 ring.
    poles = set(); FR = {}
    for cid in CFG:
        V_ = M @ B['C'][cid]['Vh']; sc_ = (V_[:, 2].max() - V_[:, 2].min()) / REF_STATURE_CM; au_ = Auditor(V_, Q); Sd = {x[0]: x for x in stations(B['C'][cid]['meta'])}
        e = evaluate(V_, Q, B['C'][cid]['meta'], REF_STATURE_CM, names=['toe3_j1_l', 'toe3_j1_r'], loops=lp, au=au_)['stations']
        for k, v in e.items():
            poles.update(v['crease_poles_own_digit']); _, c_, d_, Wd_, Rr_, need_, Rp_ = Sd[k]; FR[(cid, k[-1])] = (np.asarray(c_), unit(np.asarray(d_)), v['local_loop_cm'], Rp_ * sc_)
    poles = sorted(poles | {int(mir[p]) for p in poles if mir[p] >= 0})
    JCa = {k: 0.5 * (np.array(B['C']['MF-M-R']['meta']['joint_cubes'][k]) + np.array(B['C']['MF-F-R']['meta']['joint_cubes'][k])) for k in B['C']['MF-M-R']['meta']['joint_cubes']}
    X = M @ A
    def shifted(Mx, p, ax_, dist):
        hp = hops_from([p], 1); ids = np.array(sorted(v for v in hp if not seam[v]), int); P = (Mx @ A)[ids] + np.array([0.5 * (1 + np.cos(np.pi * hp[int(i)] / 2)) for i in ids])[:, None] * dist * ax_
        Pp, tri, bc = surf.project_local(P, np.array([vchart(int(i), Mx) for i in ids]), [Mx.indices[Mx.indptr[i]:Mx.indptr[i + 1]].tolist() for i in ids]); Ml_ = Mx.tolil(copy=True); write_rows(Ml_, ids, Pp, tri, bc)
        return Ml_.tocsr(), len(ids)
    def clear(Mx, p, s_):
        ok = True
        for cid in CFG:
            c_, d_, h_, Rp_ = FR[(cid, s_)]; P_ = (Mx[p] @ B['C'][cid]['Vh']).ravel(); t_ = float((P_ - c_) @ d_); r_ = float(np.linalg.norm(P_ - c_ - t_ * d_))
            ok &= bool(r_ > Rp_ or abs(t_) >= 0.75 * h_)
        return ok
    for p in poles:
        s_ = 'l' if X[p, 0] > 0 else 'r'; ax_ = unit(JCa['%s-toe-3-2' % s_] - JCa['%s-toe-3-1' % s_]); worst = None
        for cid in CFG:
            c_, d_, h_, Rp_ = FR[(cid, s_)]; P_ = (M[p] @ B['C'][cid]['Vh']).ravel(); t_ = float((P_ - c_) @ d_); r_ = float(np.linalg.norm(P_ - c_ - t_ * d_))
            if r_ <= Rp_ and (worst is None or abs(t_) / h_ < worst[0]): worst = (abs(t_) / h_, np.sign(t_) if t_ != 0 else 1.0, cid)
        if worst is None: continue
        sg = worst[1]
        for dist in np.arange(0.02, 0.42, 0.02):
            Mt, nreg = shifted(M, p, sg * ax_, dist)
            if clear(Mt, p, s_): M = Mt; REL.append(dict(pole=int(p), side=s_, direction='distal' if sg > 0 else 'proximal', shift_cm=round(float(dist), 3), region=int(nreg), worst_before=worst[2], t_over_h_before=round(worst[0], 3))); break
    LOG['relocation'] = REL; print('toe3 crease poles relocated', REL, flush=True)
if '--fair' in sys.argv:
    HOPS = int(os.environ.get('FAIR_HOPS', 1)); st0 = target_state(M); LOG['fairing'] = []
    for rname in ('toe2_root', 'toe3_root'):
        seed = set()
        for r in LOG['rings']:
            if r['name'].startswith(rname): seed.update(r['v003_loop_a'] + r['v003_loop_b'])
        seed.update(int(v) for v in np.arange(nV0, nV)[np.char.startswith(np.array(ring_of), rname)])
        reg = {v for v in hops_from(seed, HOPS) if not seam[v]}; faces = np.unique(np.nonzero(np.isin(Q, list(reg))[:, :].any(1))[0])
        best = (patch_t4(M, faces), 'none', M); print(rname, 'patch faces', len(faces), 'T4 (sum 4 cfg, max aspect)', best[0], flush=True)
        for it, lam, para in ((2, 0.3, 0.0), (4, 0.3, 0.0), (4, 0.35, 0.5), (8, 0.3, 0.5), (8, 0.35, 0.0), (12, 0.3, 0.5)):
            Mt = fair(M, reg, it, lam, para); stt = target_state(Mt)
            ok = all(stt[c][k][0] >= st0[c][k][0] and stt[c][k][1] <= st0[c][k][1] for c in CFG for k in TARGETS); sc = patch_t4(Mt, faces)
            print('   ', (it, lam, para), 'ok', ok, 'T4', sc, {c: [stt[c][k][0] for k in TARGETS] for c in CFG}, flush=True)
            if ok and (sc[0], sc[1]) < (best[0][0], best[0][1]): best = (sc, (it, lam, para), Mt)
        M = best[2]; LOG['fairing'].append(dict(patch=rname, region=len(reg), faces=int(len(faces)), chosen=str(best[1]), t4_sum4=best[0][0], max_aspect=round(best[0][1], 2)))
        print(rname, 'chosen', best[1], best[0], flush=True)
    st1 = target_state(M); LOG['fairing_targets'] = {c: {k: list(v[:2]) for k, v in st1[c].items()} for c in CFG}
# UVs of every vertex whose row is now barycentric and changed (non-seam): surface UV at the barycentric point
M3pad = sp.vstack([B['M3'], sp.csr_matrix((nV - nV0, M.shape[1]))]).tocsr(); chg = np.nonzero(abs(M - M3pad).sum(1).A.ravel() > 1e-12)[0]
uvset = {}
for v in chg:
    if seam[v]: continue
    cols = M.indices[M.indptr[v]:M.indptr[v + 1]]
    if len(cols) > 3: continue
    t_ = None
    for f_ in surf.vq[int(cols[0])]:
        for kk, tri_c in ((0, [0, 1, 2]), (1, [0, 2, 3])):
            if set(int(c_) for c_ in cols) <= set(Qh[f_][tri_c].tolist()): t_ = (f_, tri_c); break
        if t_: break
    if t_ is None: continue
    f_, tri_c = t_; w_ = dict(zip(M.indices[M.indptr[v]:M.indptr[v + 1]].tolist(), M.data[M.indptr[v]:M.indptr[v + 1]].tolist()))
    uvset[int(v)] = sum(w_.get(int(Qh[f_][k_]), 0.0) * B['UVh'][f_][k_] for k_ in tri_c)
for f, qd in enumerate(Q):
    for k, v in enumerate(qd):
        if int(v) in uvset: UV[f, k] = uvset[int(v)]
# ------------------------------------------------------------------ provenance + save
row_class = np.zeros(nV, np.int8); row_class[heel] = 2; row_class[nV0:] = np.where(proj[nV0:], 3, 1)
LOG['row_class_legend'] = {'0': 'frozen v003 row (unchanged)', '1': 'new ring vertex, linear edge-midpoint row (seam / UV-guard)', '2': 'posterior-heel row re-expressed on-surface barycentric',
                           '3': 'new ring vertex, on-surface barycentric row', '4': 'frozen v003 vertex re-expressed barycentric by toe-patch fairing / toe-3 crease-pole relocation'}
for v in chg:
    if v < nV0 and row_class[v] == 0: row_class[v] = 4
LOG['counts'] = {k: int((row_class == int(k)).sum()) for k in LOG['row_class_legend']}; LOG['verts'] = int(nV); LOG['quads'] = int(len(Q))
np.savez_compressed(OUT, Q=Q, UV=UV, M_data=M.data, M_indices=M.indices, M_indptr=M.indptr, M_shape=np.array(M.shape), row_class=row_class, ring_parents=np.array(parents, np.int64),
                    ring_name=np.array(ring_of), n_v003=nV0, log=json.dumps(LOG))
print('saved', OUT, LOG['counts'], '%.0fs' % (time.time() - t0))
