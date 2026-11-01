# sa_vault.py IN.npz OUT.npz SPEC.json : AUTHORED local pocket patches on the full cage (order 236dddc §3 axillary vault, §8 perineal support).
#   SPEC = list of {"name", "centre": [x, f, u] (pocket region), "rings": k (patch = k-ring of quads around the cage quad nearest the pocket apex),
#   "times": n (support rings), "apex": true}. The pocket apex = the source vertex of maximum cage distance within 3 cm of "centre". The patch (a disk of
#   fine quads spanning the pocket mouth) is inset n times (one closed support ring per inset, following the patch boundary -> the pocket rim); the patch
#   rings and the patch floor are placed into the source pocket by depth bands along the pocket axis (mouth -> apex): ring 1 at 1/3, ring 2 at 2/3 of the
#   pocket depth, the patch floor (incl. the explicit VAULT APEX CORNER region) on the pocket floor; then sa_qopt slides them (source-driven). Topology outside the patch is unchanged; c1 / c2 share the new face list; tail module untouched.
import sys, os, json, numpy as np, igl, collections, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT, SPEC = sys.argv[1:4]; z = dict(np.load(IN)); Q = z['Q'].copy(); V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nb = int(z['n_body'])
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; d = np.sqrt(igl.point_mesh_squared_distance(G.V, V, T)[0])
ql = list(z['qlab'].astype(str)); qc = list(z['qcoarse']); pinned = list(z['pinned']); V = list(V); Q = [list(q) for q in Q]; log = []
for P in json.load(open(SPEC)):
    c = np.asarray(P['centre'], float); near = np.nonzero(np.linalg.norm(G.V - c, axis=1) < 3.0)[0]; apex = near[np.argmax(d[near])] if not P.get('seed_at_centre') else near[np.argmin(np.linalg.norm(G.V[near] - c, axis=1))]; A = G.V[apex]
    Va = np.array(V); Qa = np.array(Q); qcen = Va[Qa].mean(1); qcen[(Qa >= nb).any(1)] = 1e9; q0 = int(np.argmin(np.linalg.norm(qcen - A, axis=1)))
    VQ = collections.defaultdict(list)
    for i, q in enumerate(Q):
        for v in q: VQ[v].append(i)
    patch = {q0}
    for _ in range(int(P.get('rings', 2))): patch |= {j for i in list(patch) for v in Q[i] for j in VQ[v] if all(w < nb for w in Q[j])}
    patch = sorted(patch); assert all(v < nb for i in patch for v in Q[i]), 'patch touches the tail module'
    twins_all = []; bd0 = None
    for t in range(int(P.get('times', 2))):
        ec = collections.Counter(tuple(sorted((Q[i][k], Q[i][(k + 1) % 4]))) for i in patch for k in range(4))
        bd = [(Q[i][k], Q[i][(k + 1) % 4]) for i in patch for k in range(4) if ec[tuple(sorted((Q[i][k], Q[i][(k + 1) % 4])))] == 1]
        if bd0 is None: bd0 = list(bd)
        oc = collections.Counter(a for a, b in bd); ic = collections.Counter(b for a, b in bd); assert max(oc.values()) == 1 and max(ic.values()) == 1, ('not a disk', P['name'])
        cen = np.mean([V[v] for i in patch for v in Q[i]], 0); twin = {}
        for b in oc:
            inc = [i for i in patch if b in Q[i]]; cc = np.mean([np.mean([V[v] for v in Q[i]], 0) for i in inc], 0); twin[b] = len(V); V.append(V[b] + 0.4 * (cc - V[b]))
        twins_all.append(twin)
        for i in patch: Q[i] = [twin.get(v, v) for v in Q[i]]
        for a, b in bd:
            Q.append([a, b, twin[b], twin[a]]); ql.append(P.get('label', 'shoulder')); qc.append(qc[patch[0]])
    if P.get('deepen', True):
        # depth-band placement: the source pocket (vertices uncovered by the mouth-spanning cage, d > 0.8 mm, within 3 cm of the apex) gets a depth
        # coordinate s along the pocket axis D (mouth centre -> apex); support ring k sits at depth fraction k/(n+1)... ring 1 = 1/3, ring 2 = 2/3,
        # patch interior = the pocket floor; each vertex takes the pocket point of its band nearest to its own (shrunk) lateral offset.
        Pp = near[d[near] > 0.08]; ring_lv = {}
        outer = sorted({a for a, b in bd0}); mc = np.mean([V[v] for v in outer], 0); D = A - mc; D /= np.linalg.norm(D)
        sP = (G.V[Pp] - mc) @ D; smax = sP.max(); oP = (G.V[Pp] - mc) - sP[:, None] * D
        lv = {}; used_pts = []; MINSEP = float(os.environ.get('MINSEP', 0.05))
        for k, tw in enumerate(twins_all, 1):
            for v in tw.values(): lv[v] = k / (len(twins_all) + 1.0)
        for v in {v for i in patch for v in Q[i]}:
            if v not in lv and v not in outer: lv[v] = 1.0
        for v, lam in lv.items():
            band = np.abs(sP - lam * smax) < 0.18 * smax
            if not band.any(): continue
            o = (V[v] - mc) - ((V[v] - mc) @ D) * D; tgt = o * (1 - 0.35 * lam)
            cand_ = Pp[band]; dd_ = np.linalg.norm(oP[band] - tgt, axis=1)
            if used_pts:                                                     # distinct targets (no two patch vertices on one source point -> no collapsed edge)
                du_ = np.min(np.linalg.norm(G.V[cand_][:, None] - np.array(used_pts)[None], axis=2), 1); dd_ = np.where(du_ < MINSEP, np.inf, dd_)
            if not np.isfinite(dd_).any(): continue
            j = int(np.argmin(dd_)); V[v] = G.V[cand_[j]].copy(); used_pts.append(V[v])
    if P.get('apex', False):
        iv = sorted({v for i in patch for v in Q[i]}); j = min(iv, key=lambda v: np.linalg.norm(V[v] - A)); V[j] = A.copy(); pinned.append(j)
    log.append((P['name'], int(apex), np.round(A, 2).tolist(), round(float(d[apex] * 10), 2), len(patch)))
# body vertices must stay first (tail module indices >= n_body): renumber so new vertices sit before the module block
V = np.array(V); Q = np.array(Q); nold = len(z['V']) if 'V' in z else len(z['bc']); nnew = len(V) - nold
perm = np.r_[np.arange(nb), np.arange(nold, len(V)), np.arange(nb, nold)]; inv = np.empty_like(perm); inv[perm] = np.arange(len(perm))
V = V[perm]; Q = inv[Q]; pinned = inv[np.array(pinned)]; tail_ring = inv[z['tail_ring']]
ec = collections.Counter(tuple(sorted((q[k], q[(k + 1) % 4]))) for q in Q for k in range(4)); assert max(ec.values()) == 2 and min(ec.values()) == 2, 'not closed'
dirE = collections.Counter((q[k], q[(k + 1) % 4]) for q in Q for k in range(4)); assert max(dirE.values()) == 1, 'orientation'
fi, bc, dist = G.embed(V)
out = dict(z); out.update(V=V, Q=Q, tri=fi, bc=bc, qlab=np.array(ql), qcoarse=np.array(qc), n_body=nb + nnew, tail_ring=tail_ring, pinned=pinned)
np.savez_compressed(OUT, **out); print('patches', log); print('cage', len(V), 'V', len(Q), 'Q; closed, oriented; chi', len(V) - len(ec) + len(Q))
