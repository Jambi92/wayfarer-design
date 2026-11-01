# sa_qsmooth.py IN.npz OUT.npz : fold-safe quad-quality smoothing ON the working source (Option B hand / foot quality closure, T-4 aspect / angle).
#   Optimisation-based smoothing, vertex by vertex in independent sets (graph colouring: no two vertices of one quad move together):
#     energy of a quad = sum over its 4 corners of MIPS (|a|^2 + |b|^2) / (2 s)   (s = signed corner area against the quad's host-face normal, the
#     same reference frame as sa_foldcensus.py; minimum = square corner; infinite at s -> 0, so a corner can never fold / dart / bow-tie)
#     + WA * (A / A0 + A0 / A)   (A0 = mean area of the 1-ring quads: smooth size gradation, density kept)
#     + WANC * |x - x0|^2 / h^2  (anchor to the input position: semantic loops do not drift; h = local edge length).
#   Candidate = gradient step in the vertex's tangent plane, re-projected onto the source (closest point; rejected if it lands on another sheet:
#   host normal turn > 60 deg, or drift from the input above MAXD cm). A move is kept only if every incident corner stays positive and the local energy drops. Topology unchanged.
import sys, os, numpy as np, igl, scipy.sparse as sp, torch, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; SWEEPS = int(os.environ.get('SWEEPS', 30)); WA = float(os.environ.get('WA', 0.3)); WANC = float(os.environ.get('WANC', 0.05)); MAXD = float(os.environ.get('MAXD', 0.15)); MODE = os.environ.get('MODE', 'mips'); UW = float(os.environ.get('UW', 0.5)); ASPT = float(os.environ.get('ASPT', 3.5))
z = dict(np.load(IN, allow_pickle=True)); Q = z['Q']; ql = z['qlab'].astype(str); nv = len(z['V']); nq = len(Q)
fiv = z['tri'].copy(); bcv = z['bc'].copy(); V = (bcv[:, :, None] * G.V[G.F[fiv]]).sum(1); V0 = V.copy()
pin = np.zeros(nv, bool); pin[int(z['n_body']):] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); FA = igl.doublearea(G.V, G.F); ab = igl.AABB(); ab.init(G.V, G.F)
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']); TAIL = ql == 'tail'
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
def metrics(P):
    P4 = P[Q]; el = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); asp = el.max(1) / np.maximum(el.min(1), 1e-9)
    u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4; ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12), -1, 1)))
    return asp, ang
def nref_of(tri):
    n = (FN[tri[Q]] * FA[tri[Q]][..., None]).sum(1); return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
def corner_s(P, nr):
    P4 = P[Q]; a = np.roll(P4, -1, 1) - P4; b = np.roll(P4, 1, 1) - P4; return (np.cross(a, b) * nr[:, None]).sum(2), a, b
# region: named labels + every quad with a quality residual, dilated
asp, ang = metrics(V); m_ = ~TIP & ~TAIL
labs = os.environ.get('LABELS', 'palm,finger,finger_web,thumb,wrist,foot,forefoot,toe,toe_web,ankle').split(',')
reg = (np.isin(ql, labs) | (((asp > 3.6) | (ang.min(1) < 47) | (ang.max(1) > 133)) & (not os.environ.get('ONLYLAB')))) & m_
for _ in range(int(os.environ.get('RING', 2))): reg = ((QQ @ reg.astype(float)) > 0) & ~TAIL
regv = np.zeros(nv, bool); regv[Q[reg].ravel()] = True; border = np.zeros(nv, bool); border[Q[~reg].ravel()] = True
free = regv & ~border & ~pin; fidx = np.nonzero(free)[0]
# colouring of free vertices on the 'share a quad' graph
VV = (VQ @ VQ.T).tocsr(); col = -np.ones(nv, int)
for v in fidx:
    used = set(col[VV.indices[VV.indptr[v]:VV.indptr[v + 1]]].tolist()); c = 0
    while c in used: c += 1
    col[v] = c
ncol = col.max() + 1
print('region quads', int(reg.sum()), 'free vertices', len(fidx), 'colours', ncol, flush=True)
QL = [VQ.indices[VQ.indptr[v]:VQ.indptr[v + 1]] for v in range(nv)]
def quad_energy(P, nr, qs, A0):
    P4 = P[Q[qs]]; a = np.roll(P4, -1, 1) - P4; b = np.roll(P4, 1, 1) - P4; s = (np.cross(a, b) * nr[qs][:, None]).sum(2)
    bad = (s <= 1e-12).any(1); s = np.maximum(s, 1e-12)
    e = (((a * a).sum(2) + (b * b).sum(2)) / (2 * s)).sum(1); A = 0.5 * (s[:, 0] + s[:, 2]); e = e + WA * (A / A0[qs] + A0[qs] / A); e[bad] = np.inf
    return e
def report(tag):
    asp, ang = metrics(V); s, _, _ = corner_s(V, nref_of(fiv)); fold = (s <= 0).any(1) & m_
    print(tag, 'aspect>4 non-tip', int(((asp > 4) & m_).sum()), 'angle out non-tip', int((((ang.min(1) < 45) | (ang.max(1) > 135)) & m_).sum()),
          'non-positive corner quads', int(fold.sum()), 'max drift mm %.2f' % (np.linalg.norm(V - V0, axis=1).max() * 10), flush=True)
report('start')
h = np.zeros(nv); el_ = np.linalg.norm(V[Q] - np.roll(V[Q], -1, 1), axis=2); np.maximum.at(h, Q.ravel(), 0); hs = np.zeros(nv); hc = np.zeros(nv)
np.add.at(hs, Q.ravel(), el_.ravel()); np.add.at(hc, Q.ravel(), 1); h = hs / np.maximum(hc, 1)
Qt = torch.tensor(Q); step = np.full(nv, 0.15)
for sw in range(SWEEPS):
    nr = nref_of(fiv); s0, _, _ = corner_s(V, nr); Aq = np.maximum(0.5 * (s0[:, 0] + s0[:, 2]), 1e-12)
    A0 = np.asarray((QQ @ Aq) / np.asarray(QQ.sum(1)).ravel()).ravel()
    # gradient of the total energy (exact local gradients)
    Pt = torch.tensor(V, requires_grad=True); P4 = Pt[Qt]; a = torch.roll(P4, -1, 1) - P4; b = torch.roll(P4, 1, 1) - P4
    s = (torch.cross(a, b, dim=2) * torch.tensor(nr)[:, None]).sum(2); s = torch.clamp(s, min=1e-10)
    Et = (((a * a).sum(2) + (b * b).sum(2)) / (2 * s)).sum(1); A = 0.5 * (s[:, 0] + s[:, 2]); A0t = torch.tensor(A0)
    Et = Et + WA * (A / A0t + A0t / A); Et = (Et * torch.tensor(reg.astype(float))).sum() + WANC * (((Pt - torch.tensor(V0)) ** 2).sum(1) / torch.tensor(h ** 2 + 1e-12)).sum()
    Et.backward(); g = Pt.grad.numpy(); Nv = np.nan_to_num(igl.per_vertex_normals(V, np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]))
    g -= (g * Nv).sum(1)[:, None] * Nv; gn = np.linalg.norm(g, axis=1) + 1e-30
    moved = 0
    for c in range(ncol):
        vs = fidx[col[fidx] == c]
        if not len(vs): continue
        qs_l = [QL[v] for v in vs]; allq = np.concatenate(qs_l); own = np.repeat(np.arange(len(vs)), [len(x) for x in qs_l])
        e_old = np.bincount(own, weights=quad_energy(V, nr, allq, A0), minlength=len(vs)) + WANC * np.linalg.norm(V[vs] - V0[vs], axis=1) ** 2 / h[vs] ** 2
        todo = np.ones(len(vs), bool)
        if MODE == 'umbrella':
            P4o = V[Q[allq]]; elo = np.linalg.norm(np.roll(P4o, -1, 1) - P4o, axis=2); ao = elo.max(1) / np.maximum(elo.min(1), 1e-12); mx_old = np.zeros(len(vs)); np.maximum.at(mx_old, own, ao)
        for t_ in (1.0, 0.4, 0.1):
            if not todo.any(): break
            vt = vs[todo]
            if MODE == 'umbrella':
                Cn = np.array([V[Q[QL[v]]].mean(1).mean(0) for v in vt]) - V[vt]; Cn -= (Cn * Nv[vt]).sum(1)[:, None] * Nv[vt]; cand = V[vt] + UW * t_ * Cn
            else: cand = V[vt] - (step[vt] * t_ * h[vt] / gn[vt])[:, None] * g[vt]
            _, ff, cp = ab.squared_distance(G.V, G.F, cand); okn = ((FN[ff] * FN[fiv[vt]]).sum(1) > 0.5) & (np.linalg.norm(cp - V0[vt], axis=1) < MAXD)
            Vb = V[vt].copy(); V[vt] = np.where(okn[:, None], cp, Vb)
            sel = np.nonzero(todo)[0]; qs_t = [QL[v] for v in vt]; allt = np.concatenate(qs_t); ownt = np.repeat(np.arange(len(vt)), [len(x) for x in qs_t])
            fsave = fiv[vt].copy(); fiv[vt] = np.where(okn, ff, fiv[vt]); nr_t = nr.copy(); nr_loc = nref_of(fiv)
            e_new = np.bincount(ownt, weights=quad_energy(V, nr_loc, allt, A0), minlength=len(vt)) + WANC * np.linalg.norm(V[vt] - V0[vt], axis=1) ** 2 / h[vt] ** 2
            if MODE == 'umbrella':
                P4n = V[Q[allt]]; eln = np.linalg.norm(np.roll(P4n, -1, 1) - P4n, axis=2); an = eln.max(1) / np.maximum(eln.min(1), 1e-12)
                mx_new = np.zeros(len(vt)); np.maximum.at(mx_new, ownt, an)
                acc = okn & np.isfinite(e_new) & (mx_new <= np.maximum(mx_old[sel], ASPT))
            else: acc = okn & (e_new < e_old[sel] - 1e-9)
            V[vt[~acc]] = Vb[~acc]; fiv[vt[~acc]] = fsave[~acc]; todo[sel[acc]] = False; moved += int(acc.sum())
        step[vs[~todo]] = np.minimum(step[vs[~todo]] * 1.3, 0.5); step[vs[todo]] *= 0.6
    if sw % 5 == 0 or sw == SWEEPS - 1: report('sweep %d moved %d' % (sw, moved))
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z); V = (bc2[:, :, None] * G.V[G.F[fi2]]).sum(1); fiv = fi2; report('final (re-embedded)')
print('DONE')
