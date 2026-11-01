# sa_gopt.py IN.npz OUT.npz : JOINT gradient optimisation of the T-4 residual regions with T-1 / T-2 coverage (order 236dddc §9). Topology unchanged.
#   Region = every vertex within RING quad-rings of a residual quad (aspect > 3.8 or angle outside 46-134, tip caps excepted); region border, pins and the tail
#   module fixed. Energy (exact gradients, torch): shape barrier on every region quad (all 12 edge-length ratios above A_T, corner |cos| above cos 47 deg)
#   + coverage barrier: each local source vertex (zone thr 1.3 mm, body 2.7 mm) assigned to its nearest cage quad, distance to the quad's two triangles'
#   planes above 0.9 thr. Adam steps, every step re-projected onto the working source (vertices stay on the surface), assignment refreshed every 25 steps.
#   Final acceptance per connected region: the region's worst quad must improve and no source vertex may end above its threshold worse than before.
import sys, os, numpy as np, igl, scipy.sparse as sp, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.sparse.csgraph import connected_components
IN, OUT = sys.argv[1:3]; STEPS = int(os.environ.get('STEPS', 300)); RING = int(os.environ.get('RING', 4)); A_T = float(os.environ.get('A_T', 3.3)); LR = float(os.environ.get('LR', 0.004))
torch.set_num_threads(1)
z = dict(np.load(IN)); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv = len(V); nq = len(Q); nb = int(z['n_body']); ql = z['qlab'].astype(str)
pin = np.zeros(nv, bool); pin[nb:] = True; pin[z['tail_ring']] = True; pin[z['pinned']] = True
if os.environ.get('FREEZE_LABELS'): pin[np.unique(Q[np.isin(z['qlab'].astype(str), os.environ['FREEZE_LABELS'].split(','))])] = True
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap', 'tail'])
zone = np.isin(G.LAB, ['head', 'hand_xneg', 'hand_xpos', 'foot_xneg', 'foot_xpos', 'tail']); thr = np.where(zone, 0.13, 0.27)
src = igl.AABB(); src.init(G.V, G.F); FNs = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; tq = np.r_[np.arange(nq), np.arange(nq)]
VQ = sp.coo_matrix((np.ones(4 * nq), (Q.ravel(), np.repeat(np.arange(nq), 4))), shape=(nv, nq)).tocsr(); QQ = (VQ.T @ VQ).tocsr()
FNh = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0]))
def concave(P, tri=None):
    """host-aware fold flag (same test as sa_foldcensus): signed turns of the quad in the tangent plane of its corners' source host faces < 0.02"""
    tri = z['tri'] if tri is None else tri; P4 = P[Q]; n = FNh[tri[Q]].sum(1); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    u1 = P4 - np.roll(P4, 1, 1); u2 = np.roll(P4, -1, 1) - P4
    return ((np.cross(u1, u2) * n[:, None]).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12)).min(1) < 0.02
def metrics(P):
    P4 = P[Q]; sd = np.linalg.norm(np.roll(P4, -1, 1) - P4, axis=2); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9)
    u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4; ang = np.degrees(np.arccos(np.clip((u1 * u2).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12), -1, 1)))
    return asp, ang
asp, ang = metrics(V); cv0 = concave(V); bad = ((asp > 3.8) | (ang.min(1) < 46) | (ang.max(1) > 134) | cv0) & ~TIP
if os.environ.get('CRITONLY'): bad = ((ang.min(1) < 47) | (ang.max(1) > 133)) & np.isin(ql, ['shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'neck', 'finger', 'thumb', 'toe'])
reg = bad.copy()
for _ in range(RING): reg = (QQ @ reg.astype(float)) > 0
regv = np.zeros(nv, bool); regv[Q[reg].ravel()] = True; border = np.zeros(nv, bool); border[Q[~reg].ravel()] = True
free = regv & ~border & ~pin; fi_ = np.nonzero(free)[0]; RQ = np.nonzero(reg)[0]
print('residual quads', int(bad.sum()), 'region quads', len(RQ), 'free vertices', len(fi_), flush=True)
cg = igl.AABB(); cg.init(V, T); d0, ti0, _ = cg.squared_distance(V, T, G.V); d0 = np.sqrt(d0)
# local source samples: source vertices whose nearest cage quad is a region quad
smask = reg[tq[ti0]]; S = np.nonzero(smask)[0]; print('coverage samples', len(S), flush=True)
Vt = torch.tensor(V, dtype=torch.float64); X = torch.tensor(V[fi_], dtype=torch.float64, requires_grad=True); idx = torch.tensor(fi_)
RQt = torch.tensor(Q[RQ]); Sp = torch.tensor(G.V[S]); thS = torch.tensor(thr[S]); ca = np.cos(np.radians(47))
opt = torch.optim.Adam([X], lr=LR)
def full(Xv): P = Vt.clone(); P[idx] = Xv; return P
assign = None
for st in range(STEPS):
    if st % 25 == 0:
        Pn = full(X.detach()).numpy(); cgi = igl.AABB(); cgi.init(Pn, T); _, ti, _ = cgi.squared_distance(Pn, T, G.V[S]); assign = torch.tensor(T[ti])
    P = full(X); P4 = P[RQt]; e = torch.linalg.norm(torch.roll(P4, -1, 1) - P4, dim=2)
    ratio = e[:, :, None] / (e[:, None, :] + 1e-9); Es = torch.relu(ratio - A_T).pow(2).sum()
    u1 = torch.roll(P4, 1, 1) - P4; u2 = torch.roll(P4, -1, 1) - P4; cs = (u1 * u2).sum(2) / (torch.linalg.norm(u1, dim=2) * torch.linalg.norm(u2, dim=2) + 1e-12)
    Ea = torch.relu(cs.abs() - ca).pow(2).sum() * float(os.environ.get('AW', 20))
    nq_ = torch.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1], dim=1); nq_ = nq_ / (torch.linalg.norm(nq_, dim=1, keepdim=True) + 1e-12)
    sg = (torch.cross(u2, u1, dim=2) * nq_[:, None]).sum(2) / (torch.linalg.norm(u1, dim=2) * torch.linalg.norm(u2, dim=2) + 1e-12)
    Ea = Ea + torch.relu(0.35 - sg).pow(2).sum() * float(os.environ.get('VW', 200))          # convexity barrier (signed corner sine >= 0.35, i.e. corners < ~160 deg, no dart / bow-tie)
    A_ = P[assign[:, 0]]; B_ = P[assign[:, 1]]; C_ = P[assign[:, 2]]; n = torch.cross(B_ - A_, C_ - A_, dim=1); n = n / (torch.linalg.norm(n, dim=1, keepdim=True) + 1e-12)
    dpl = ((Sp - A_) * n).sum(1).abs(); Ec = (torch.relu(dpl - 0.9 * thS) / thS).pow(2).sum() * float(os.environ.get('CW', 50))
    E = Es + Ea + Ec; opt.zero_grad(); E.backward(); opt.step()
    with torch.no_grad():
        Pn_ = full(X).numpy(); Nv_ = np.nan_to_num(igl.per_vertex_normals(Pn_, T))[fi_]
        _, fq_, cp = src.squared_distance(G.V, G.F, X.numpy()); wrong = (FNs[fq_] * Nv_).sum(1) < 0.2      # wrong-sheet hits re-queried from 1 mm inside
        if wrong.any(): _, _, cp2 = src.squared_distance(G.V, G.F, X.numpy()[wrong] - 0.1 * Nv_[wrong]); cp[wrong] = cp2
        X.copy_(torch.tensor(cp))
    if st % 50 == 0 or st == STEPS - 1: print('step', st, 'E %.3f shape %.3f angle %.3f cover %.3f' % (E.item(), Es.item(), Ea.item(), Ec.item()), flush=True)
Vn = full(X.detach()).numpy()
# acceptance: take the optimised region, roll back (to the input) the vertices of every quad nearest to a source vertex that ends above its threshold
# and worse than before (repeat), then keep a region component only if its shape residual does not grow
V0 = V.copy(); V = V.copy(); V[fi_] = Vn[fi_]
asn, ann = metrics(V); nc, lab = connected_components(QQ[RQ][:, RQ], directed=False); acc = 0
for c in range(nc):
    qs = RQ[lab == c]; vs = np.unique(Q[qs]); vs = vs[free[vs]]
    cvn = concave(V)
    w0 = np.maximum(asp[qs] - 4, 0).sum() * 10 + ((ang[qs].min(1) < 45) | (ang[qs].max(1) > 135)).sum() * 0.1 + cv0[qs].sum() * 1.0
    w1 = np.maximum(asn[qs] - 4, 0).sum() * 10 + ((ann[qs].min(1) < 45) | (ann[qs].max(1) > 135)).sum() * 0.1 + cvn[qs].sum() * 1.0
    if w1 > w0: V[vs] = V0[vs]
    else: acc += 1
for _g in range(10):
    cgn = igl.AABB(); cgn.init(V, T); dn2, tin, _ = cgn.squared_distance(V, T, G.V); dn = np.sqrt(dn2)
    viol = np.nonzero((dn > thr) & (dn > d0 + 1e-5))[0]
    if not len(viol): break
    rv = np.unique(np.r_[Q[tq[tin[viol]]].ravel(), Q[tq[ti0[viol]]].ravel()]); rv = rv[np.linalg.norm(V[rv] - V0[rv], axis=1) > 0]   # current AND original nearest quads
    if not len(rv): break
    V[rv] = V0[rv]
print('rollback passes', _g)
cgf = igl.AABB(); cgf.init(V, T); df = np.sqrt(cgf.squared_distance(V, T, G.V)[0]) * 10; asf, anf = metrics(V)
print('components', nc, 'accepted', acc, '| aspect>4 non-tip', int(((asf > 4) & ~TIP).sum()), 'angle out', int(((anf.min(1) < 45) | (anf.max(1) > 135)).sum()), 'concave non-tip', int((concave(V) & ~TIP).sum()),
      '| T1 body max %.2f zone max %.2f' % (df[~zone].max(), df[zone].max()))
fi2, bc2, _ = G.embed(V); z['V'] = V; z['tri'] = fi2; z['bc'] = bc2; np.savez_compressed(OUT, **z)
