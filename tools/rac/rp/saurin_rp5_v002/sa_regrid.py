# sa_regrid.py DESIGN.pkl IN.npz OUT.npz : authored RE-GRID of crumpled coarse quads (order 236dddc §6-§9: web / forefoot / palm 2:1 / orbit-fan fold removal).
#   Every coarse quad of the authored design carries an 8 x 8 fine grid (3 Catmull-Clark levels). Coarse quads whose fine grid is folded (>= MINF fine quads
#   inverted against the source normal) are re-gridded: each side chain is re-sampled uniformly along the chord between its two coarse corners and every
#   interior vertex is placed by a Coons patch over the four side curves at its Tutte (uniform-harmonic) grid parameter; all re-placed vertices are projected
#   onto the working source SHEET-CONSISTENTLY (only source faces whose normal agrees with the patch normal, within 2.5 cm -> never onto the neighbouring
#   digit / web wall). Edge-neighbour coarse quads get their interior re-gridded against their (partly moved) sides. Topology unchanged.
import sys, os, pickle, collections, numpy as np, igl, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G, sa_ccage as CC
from scipy.spatial import cKDTree
DS, IN, OUT = sys.argv[1:4]; MINF = int(os.environ.get('MINF', 3))
d = pickle.load(open(DS, 'rb')); Cc = np.array(d['C']); Qc = np.array(d['Q']); ncq = len(Qc)
Vf, Qf, src = Cc.copy(), Qc.copy(), np.arange(ncq)
for _ in range(3): Vf, Qf, src = CC.cc(Vf, Qf, src)
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nqf = len(Qf); nv = len(V)
intact = np.all(Q[:nqf] == Qf, axis=1)                                               # fine quads still exactly as built (not touched by a later patch)
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); kdF = cKDTree(G.V[G.F].mean(1))
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
P4 = V[Q[:nqf]]; n = np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]); _, fi, _ = igl.point_mesh_squared_distance(P4.mean(1), G.V, G.F); inv = (n * FN[fi]).sum(1) < 0
cnt = np.bincount(src[inv], minlength=ncq); okq = np.array([intact[src == q].all() for q in range(ncq)])
ql = np.array(d['qlab']); SEL = np.nonzero((cnt >= MINF) & okq & ~np.isin(ql, ['tail']))[0]
EC = collections.defaultdict(list)
for q in range(ncq):
    for k in range(4): EC[(min(Qc[q][k], Qc[q][(k + 1) % 4]), max(Qc[q][k], Qc[q][(k + 1) % 4]))].append(q)
NB = sorted({j for q in SEL for k in range(4) for j in EC[(min(Qc[q][k], Qc[q][(k + 1) % 4]), max(Qc[q][k], Qc[q][(k + 1) % 4]))] if j not in SEL and okq[j] and ql[j] != 'tail'})
print('re-grid coarse quads', len(SEL), 'interior-only neighbours', len(NB), flush=True)
def sheet_project(P, nrm):
    out = P.copy()
    for i, (x, nn) in enumerate(zip(P, nrm)):
        cand = np.array(kdF.query_ball_point(x, 2.5), int)
        cand = cand[FN[cand] @ nn > 0.3] if len(cand) else cand
        if not len(cand): _, _, cp = igl.point_mesh_squared_distance(x[None], G.V, G.F)
        else: _, _, cp = igl.point_mesh_squared_distance(x[None], G.V, G.F[cand])
        out[i] = cp[0]
    return out
def grid(q):
    fq = np.nonzero(src == q)[0]; vs = np.unique(Qf[fq]); ec = collections.Counter((min(a, b), max(a, b)) for f in fq for a, b in zip(Qf[f], np.roll(Qf[f], -1)))
    bE = [e for e, c in ec.items() if c == 1]; adj = collections.defaultdict(list)
    for a, b in bE: adj[a].append(b); adj[b].append(a)
    corners = list(Qc[q]); loop = [corners[0]]; prev = None
    while True:
        nx = [w for w in adj[loop[-1]] if w != prev]; w = nx[0] if prev is not None else ([w for w in adj[loop[-1]] if w in (adj[loop[-1]])][0])
        if prev is None:   # choose the direction towards corner 1
            path_ok = None
        prev = loop[-1]; loop.append(w)
        if w == corners[0]: break
    loop = loop[:-1]
    if loop[8] != corners[1]: loop = [loop[0]] + loop[1:][::-1]
    assert [loop[8 * k] for k in range(4)] == corners, 'corner order'
    sides = [loop[8 * k: 8 * k + 9] if k < 3 else loop[24:] + [loop[0]] for k in range(4)]
    # Tutte parameters
    uv = {}; 
    for k, sdv in enumerate(sides):
        for j, v in enumerate(sdv):
            t = j / 8.0; uv[v] = [(t, 0), (1, t), (1 - t, 1), (0, 1 - t)][k]
    inner = [v for v in vs if v not in uv]; li = {v: i for i, v in enumerate(inner)}
    A = sp.lil_matrix((len(inner), len(inner))); B = np.zeros((len(inner), 2))
    E2 = {(min(a, b), max(a, b)) for f in fq for a, b in zip(Qf[f], np.roll(Qf[f], -1))}; nb_ = collections.defaultdict(list)
    for a, b in E2: nb_[a].append(b); nb_[b].append(a)
    for v in inner:
        i = li[v]; A[i, i] = len(nb_[v])
        for w in nb_[v]:
            if w in li: A[i, li[w]] -= 1
            else: B[i] += uv[w]
    X = spl.spsolve(A.tocsc(), B) if len(inner) else np.zeros((0, 2))
    for v, x in zip(inner, np.atleast_2d(X)): uv[v] = tuple(x)
    return sides, inner, uv
moved = np.zeros(nv, bool)
def coons(sides, uv, inner, Vcur):
    C = [Vcur[s_] for s_ in sides]; P0, P1, P2, P3 = Vcur[sides[0][0]], Vcur[sides[1][0]], Vcur[sides[2][0]], Vcur[sides[3][0]]
    def curve(k, t): x = t * 8; i = min(int(x), 7); f = x - i; return (1 - f) * C[k][i] + f * C[k][i + 1]
    out = []
    for v in inner:
        u, w = uv[v]
        p = (1 - w) * curve(0, u) + w * curve(2, 1 - u) + (1 - u) * curve(3, 1 - w) + u * curve(1, w) - ((1 - u) * (1 - w) * P0 + u * (1 - w) * P1 + u * w * P2 + (1 - u) * w * P3)
        out.append(p)
    return np.array(out)
def qnormal(q):
    cs = Qc[q]; _, f_, _ = igl.point_mesh_squared_distance(V[cs], G.V, G.F); nn = FN[f_].sum(0); return nn / np.linalg.norm(nn)
for q in SEL:                                                                         # sides re-sampled along the chord, then projected
    sides, inner, uv = grid(q); nn = qnormal(q)
    for sdv in sides:
        a, b = V[sdv[0]], V[sdv[-1]]; mid = [v for v in sdv[1:-1] if not pin[v]]
        P = np.array([a + (j / 8.0) * (b - a) for j, v in enumerate(sdv) if v in mid]); V[mid] = sheet_project(P, np.tile(nn, (len(mid), 1))); moved[mid] = True
for q in list(SEL) + NB:
    sides, inner, uv = grid(q); inner = [v for v in inner if not pin[v]]
    if not inner: continue
    nn = qnormal(q); P = coons(sides, uv, inner, V); V[inner] = sheet_project(P, np.tile(nn, (len(inner), 1))); moved[inner] = True
P4 = V[Q[:nqf]]; n = np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]); _, fi, _ = igl.point_mesh_squared_distance(P4.mean(1), G.V, G.F); inv2 = (n * FN[fi]).sum(1) < 0
print('inverted fine quads', int(inv.sum()), '->', int(inv2.sum()), '; vertices re-placed', int(moved.sum()))
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z)
