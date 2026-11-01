# sa_ringsplit.py IN.npz OUT.npz : Option B local ring insertion (order 50ef121 §4: "local quad split ... within the Option B hand / foot regions").
#   For every quad with aspect > ASPT (outside tip caps) the quad strip that crosses its two LONG sides is traced. If that strip is a CLOSED ring lying
#   entirely in hand / foot labels (a digit / palm ring - local, it never runs through the body) and has at most MAXLEN quads, every quad of the ring is
#   split in two through the midpoints of its long sides (one new edge loop). New vertices = long-edge midpoints re-projected onto the working source
#   (closest point, sheet-consistent). New quads inherit label / coarse id. No T-junctions (the ring is closed), manifold quad mesh kept, tail untouched.
#   Repeated ROUNDS times (a ring is split at most once per round).
import sys, os, collections, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; ASPT = float(os.environ.get('ASPT', 4.0)); MAXLEN = int(os.environ.get('MAXLEN', 400)); ROUNDS = int(os.environ.get('ROUNDS', 2))
HF = set(os.environ.get('LABELS', 'palm,finger,finger_web,finger_cap,thumb,thumb_cap,wrist,foot,forefoot,toe,toe_web,toe_cap,ankle').split(','))
z = dict(np.load(IN, allow_pickle=True)); Q = z['Q'].copy(); ql = z['qlab'].astype(str).copy(); qc = z['qcoarse'].copy(); nb = int(z['n_body'])
V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); ab = igl.AABB(); ab.init(G.V, G.F); FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0]))
extra = {k: z[k] for k in z if k not in ('V', 'Q', 'tri', 'bc', 'qlab', 'qcoarse', 'n_body', 'tail_ring', 'pinned')}
# body vertices first, tail-module vertices after n_body: new vertices are inserted at the end of the BODY block (indices >= nb shift)
def key(a, b): return (a, b) if a < b else (b, a)
log = []
for rnd in range(ROUNDS):
    P4 = V[Q]; s = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); asp = s.max(1) / np.maximum(s.min(1), 1e-9); la = 0.5 * (s[:, 0] + s[:, 2]); lb = 0.5 * (s[:, 1] + s[:, 3])
    m = ~np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
    E = collections.defaultdict(list)
    for q, quad in enumerate(Q):
        for k in range(4): E[key(quad[k], quad[(k + 1) % 4])].append((q, k))
    def strip(q0, k0):
        out = [(q0, k0)]; q, k = q0, (k0 + 2) % 4
        for _ in range(MAXLEN):
            nbq = [x for x in E[key(Q[q, k], Q[q, (k + 1) % 4])] if x[0] != q]
            if not nbq: return out, False
            q2, k2 = nbq[0]
            if q2 == q0: return out, True
            out.append((q2, k2)); q, k = q2, (k2 + 2) % 4
        return out, False
    done = np.zeros(len(Q), bool); rings = []
    for q in np.argsort(-asp):
        if asp[q] <= ASPT: break
        if not m[q] or done[q]: continue
        k0 = 0 if la[q] > lb[q] else 1; st, cl = strip(q, k0)          # k0: the long side pair (k0, k0+2) is crossed / split
        qs = [x[0] for x in st]
        if not cl or not all(ql[x] in HF for x in qs) or done[qs].any(): continue
        Ls = np.array([0.5 * (s[x, k] + s[x, (k + 2) % 4]) for x, k in st]); Ss = np.array([0.5 * (s[x, (k + 1) % 4] + s[x, (k + 3) % 4]) for x, k in st])
        na = np.maximum(Ls / 2, Ss) / np.minimum(Ls / 2, Ss); oa = asp[qs]
        if na.max() > float(os.environ.get('NEWMAX', 3.2)) or (na > 4).sum() >= ((oa > 4) & m[qs]).sum(): continue
        rings.append(st); done[qs] = True
    if not rings: print('round', rnd, 'no local closed ring left'); break
    # split
    newv = {}; Vb = list(V[:nb]); Vt = V[nb:]; addP = []
    def mid(a, b):
        kk = key(a, b)
        if kk not in newv: newv[kk] = nb + len(addP); addP.append(0.5 * (V[a] + V[b]))
        return newv[kk]
    Qn = []; keepq = np.ones(len(Q), bool); lab_n = []; qc_n = []; sq_order = []
    for st in rings:
        for q, k in st:
            a, b, c, d = [Q[q, (k + j) % 4] for j in range(4)]        # side k = a-b (split), side k+2 = c-d (split)
            m1 = mid(a, b); m2 = mid(c, d)
            Qn += [[a, m1, m2, d], [m1, b, c, m2]]; lab_n += [ql[q]] * 2; qc_n += [qc[q]] * 2; keepq[q] = False; sq_order.append(q)
    addP = np.array(addP); _, ff, cp = ab.squared_distance(G.V, G.F, addP)
    # re-index: body vertices [0, nb), new vertices [nb, nb + k), tail vertices shifted by k
    k_ = len(addP); shift = lambda A: np.where(A >= nb, A + k_, A)
    Qold = shift(Q[keepq]); Qnew_fixed = np.array(Qn)            # ring quads are hand / foot body quads: their old ids are < nb, new ids in [nb, nb + k)
    assert (np.array([[Q[q, j] for j in range(4)] for st in rings for q, _ in st]) < nb).all()
    Q = np.vstack([Qold, Qnew_fixed]); ql = np.r_[ql[keepq], np.array(lab_n)]; qc = np.r_[qc[keepq], np.array(qc_n)]
    V = np.vstack([V[:nb], cp, V[nb:]]); z['tail_ring'] = np.where(z['tail_ring'] >= nb, z['tail_ring'] + k_, z['tail_ring']); z['pinned'] = np.where(z['pinned'] >= nb, z['pinned'] + k_, z['pinned'])
    for kx in list(extra):
        if np.ndim(extra[kx]) and len(extra[kx]) == len(keepq): extra[kx] = np.r_[extra[kx][keepq], np.repeat(extra[kx][np.array(sq_order)], 2)]
    nb += k_
    log.append(dict(round=rnd, rings=len(rings), ring_lengths=[len(r) for r in rings], new_vertices=k_, labels=collections.Counter(ql[-len(Qn):]).most_common()))
    P4 = V[Q]; s = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); asp = s.max(1) / np.maximum(s.min(1), 1e-9); m = ~np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
    print('round', rnd, 'rings split', len(rings), 'lengths', sorted(len(r) for r in rings), 'new vertices', k_, '| aspect>4 non-tip now', int(((asp > 4) & m).sum()), flush=True)
# manifold / orientation sanity
e = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); _, cnt = np.unique(e, axis=0, return_counts=True); assert cnt.max() <= 2, 'non-manifold'
de = np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2); assert len(np.unique(de, axis=0)) == len(de), 'orientation'
fi, bc, _ = G.embed(V)
out = dict(z); out.update(extra); out.update(V=V, Q=Q, tri=fi, bc=bc, qlab=ql, qcoarse=qc, n_body=nb)
np.savez_compressed(OUT, **out); print('quads', len(Q), 'vertices', len(V), 'boundary edges', int((cnt == 1).sum())); print('DONE')
