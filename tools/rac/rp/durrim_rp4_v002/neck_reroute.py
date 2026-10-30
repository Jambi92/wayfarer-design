# neck_reroute.py : v002 jaw-neck pole reroute (order 8080f9f §5) -- minimal local re-quad of the faces around the v005 submandibular 5-pole pair
# (5299 / 11904) by quad edge rotations: no vertex is added or moved (surface = v005 vertices), only the diagonal of a few adjacent quad pairs changes.
# One rotation of edge (u, v) shared by quads [u, v, a, b] and [v, u, c, d] (hexagon u-c? ...) replaces them by two quads over the same hexagon with the
# other "long diagonal": valence(u), valence(v) -1; two hexagon vertices +1. Sequences are searched in the pole's 3-ring and scored on every body by the
# validator neck-station crease band (pole t / h), worst body first. Mirror side via the v005 L/R vertex map.
import sys, json, itertools, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002')
from neck_probe import frame, adjacency
def quads_of(Q):
    E = {}
    for fi, q in enumerate(Q):
        for k in range(4):
            a, b = int(q[k]), int(q[(k + 1) % 4]); E.setdefault((min(a, b), max(a, b)), []).append(fi)
    return E
def rotate(Q, fa, fb, u, v, direction):
    """rotate edge (u,v) shared by faces fa, fb. Hexagon = union boundary. direction +1/-1 picks the new diagonal. Returns new (qa, qb) or None."""
    A = [int(x) for x in Q[fa]]; Bq = [int(x) for x in Q[fb]]
    if u not in A or v not in A or u not in Bq or v not in Bq: return None
    i = A.index(u)
    if A[(i + 1) % 4] != v: A, Bq = Bq, A; i = A.index(u)                            # A is the face with directed edge u -> v
    if A[(i + 1) % 4] != v: return None
    A = A[i:] + A[:i]; j = Bq.index(v)                                                # A = [u, v, a2, a3]
    if Bq[(j + 1) % 4] != u: return None
    Bq = Bq[j:] + Bq[:j]                                                              # B = [v, u, b2, b3]
    H = [u, Bq[2], Bq[3], v, A[2], A[3]]                                               # union hexagon, consistent orientation; diagonal H0-H3 now
    if len(set(H)) != 6: return None
    if direction > 0: return [H[1], H[2], H[3], H[4]], [H[4], H[5], H[0], H[1]]       # new diagonal H1-H4
    return [H[2], H[3], H[4], H[5]], [H[5], H[0], H[1], H[2]]                         # new diagonal H2-H5
def apply_ops(Q, ops):
    Q = np.asarray(Q).copy()
    for (u, v, dr) in ops:
        E = quads_of(Q); fs = E.get((min(u, v), max(u, v)), [])
        if len(fs) != 2: return None
        r = rotate(Q, fs[0], fs[1], u, v, dr)
        if r is None: return None
        Q[fs[0]], Q[fs[1]] = r
    return Q
def valences(Q, nV):
    nb = adjacency(Q, nV); return np.array([len(x) for x in nb])
def mirror_map(V, ids, tol=1e-3):
    from scipy.spatial import cKDTree
    kd = cKDTree(V); P = V[ids].copy(); P[:, 0] *= -1; d, j = kd.query(P); assert (d < tol).all(), 'no mirror'; return {int(a): int(b) for a, b in zip(ids, j)}
# ------------------------------------------------------------------ search
INNER, TOPK = 3, 150
BODIES = {'DU122C-NAT': 0.5, 'DU137C-NAT': 1.5, 'DU152C-NAT': 1.5, 'DUF137C-NAT': 0.5, 'MF152-NAT': 0.5}   # required |t/h| for every pole (137 / 152: band + 1 h)
def local_faces(Q, nb, p, rings=4):
    seen = {p}; fr = [p]
    for _ in range(rings):
        nx = []
        for v in fr:
            for w in nb[v]:
                if w not in seen: seen.add(w); nx.append(w)
        fr = nx
    return [fi for fi, q in enumerate(Q) if all(int(x) in seen for x in q)], seen
def search(fams, p=5299, depth=3, out=None):
    Z = {k: np.load(f) for k, f in fams.items()}; z0 = next(iter(Z.values())); Q0 = np.asarray(z0['Q']); nV = len(z0['V']); nb = adjacency(Q0, nV)
    FR = {k: frame(z['V'].astype(float), Q0, json.loads(str(z['meta']))) for k, z in Z.items()}
    TH = {k: (z['V'][:, 2].astype(float) - FR[k]['c'][2]) / FR[k]['h'] for k, z in Z.items()}
    fl, region = local_faces(Q0, nb, p, 4); _, inner = local_faces(Q0, nb, p, INNER); Ql = Q0[fl]; val0 = np.array([len(nb[i]) for i in range(nV)])
    edges = sorted({(min(int(q[k]), int(q[(k + 1) % 4])), max(int(q[k]), int(q[(k + 1) % 4]))) for q in Ql for k in range(4)
                    if int(q[k]) in inner and int(q[(k + 1) % 4]) in inner})
    ops = [(a, b, d) for a, b in edges for d in (1, -1)]; res = []
    def evaluate(seq):
        Qn = apply_ops(Ql, seq)
        if Qn is None: return None
        vl = {}
        for q in Qn:
            for k in range(4): a, b = int(q[k]), int(q[(k + 1) % 4]); vl.setdefault(a, set()).add(b); vl.setdefault(b, set()).add(a)
        vals = {v: len(s) - len([w for w in nb[v] if w not in region]) * 0 for v, s in vl.items()}
        # valence = local neighbours + neighbours outside the region (unchanged)
        vals = {v: len(vl[v] | {w for w in nb[v] if w not in region}) for v in vl}
        poles = [v for v in inner if vals.get(v, val0[v]) != 4]
        if any(vals.get(v, 4) < 3 or vals.get(v, 4) > 5 for v in inner): return None
        sc = min(min(abs(TH[k][v]) for v in poles) - req for k, req in BODIES.items() if k in TH) if poles else 9
        return sc, poles, Qn
    from itertools import product
    best = []
    def run(seqs):
        for s in seqs:
            r = evaluate(s)
            if r is not None: best.append((r[0], len(r[1]), s, r[1]))
    run([()] + [(o,) for o in ops])
    for d in range(2, depth + 1):
        top = sorted([x for x in best if len(x[2]) == d - 1], key=lambda x: (-x[0], x[1]))[:TOPK] if d > 2 else [x for x in best if len(x[2]) == 1]
        run([s[2] + (o,) for s in top for o in ops if o not in s[2]])
    best.sort(key=lambda x: (-x[0], x[1], len(x[2])))
    for b in best[:15]: print('score %+.2f  poles %d  ops %s  pole t/h: %s' % (b[0], b[1], b[2], {k: [round(float(TH[k][v]), 2) for v in b[3]] for k in TH}))
    return best, fl
if __name__ == '__main__' and sys.argv[1] == 'search':
    W = sys.argv[2]; fams = {k: '%s/fam/%s_fam.npz' % (W, k) for k in BODIES}; search(fams, depth=int(sys.argv[3]) if len(sys.argv) > 3 else 2)
# ------------------------------------------------------------------ v002 definition / application
NECK_OPS_L = [(5299, 24347, -1), (15131, 44928, -1), (5300, 24347, -1), (24337, 44926, -1)]   # found by state BFS (depth 4), left side
def new_diag(Q, u, v, d):
    E = quads_of(Q); fs = E[(min(u, v), max(u, v))]; qa, qb = rotate(Q, fs[0], fs[1], u, v, d); return tuple(sorted(set(qa) & set(qb)))
def define_ops(Q0, V0, ops_l=NECK_OPS_L):
    """explicit both-side op list: each op = (u, v, new diagonal a-b); right side by the L/R mirror map (x -> -x on the v005 realization)"""
    Q = np.asarray(Q0).copy(); out = {'l': [], 'r': []}; ids = sorted({x for o in ops_l for x in o[:2]} | set(np.asarray(Q0)[[f for f in range(len(Q0)) if 0]].ravel().tolist()))
    for (u, v, d) in ops_l:
        nd = new_diag(Q, u, v, d); out['l'].append([u, v, list(nd)]); Q = apply_ops(Q, [(u, v, d)])
    allv = sorted({x for o in out['l'] for x in (o[0], o[1], *o[2])}); mm = mirror_map(np.asarray(V0, float), allv)
    for u, v, nd in out['l']: out['r'].append([mm[u], mm[v], sorted([mm[nd[0]], mm[nd[1]]])])
    return out
def apply_def(Q0, ops):
    """apply explicit (u, v, new-diagonal) ops on both sides; face slots are kept (the two faces of each rotation are rewritten in place)"""
    Q = np.asarray(Q0).copy(); touched = []
    for side in ('l', 'r'):
        for u, v, nd in ops[side]:
            E = quads_of(Q); fs = E[(min(u, v), max(u, v))]; done = False
            for d in (1, -1):
                r = rotate(Q, fs[0], fs[1], u, v, d)
                if r is not None and tuple(sorted(set(r[0]) & set(r[1]))) == tuple(sorted(nd)): Q[fs[0]], Q[fs[1]] = r; touched += list(fs); done = True; break
            assert done, 'neck op not realisable: %s' % ((u, v, nd),)
    return Q, sorted(set(touched))
