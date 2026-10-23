# build2.py OUT.npz [iters] [d_t2_mm] [d_t1_mm] : Grask RP2 production branch
#  base = adjudicated target S* (bilateral average of E3) with the symmetric crotch patch (sstar_p), subdivided twice (bilinear),
#  then Taubin-relaxed and constrained to within +-delta of the visible S* envelope (delta by zone; 0 in contact zones), symmetric.
import sys, json, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from subdiv import subdivide_levels; from zones import base_zones; from hidden import hidden_quads
R = '/tmp/claude-0/rp2/'
out = sys.argv[1]; IT = int(sys.argv[2]) if len(sys.argv) > 2 else 30
D2 = float(sys.argv[3]) / 10 if len(sys.argv) > 3 else 0.04; D1 = float(sys.argv[4]) / 10 if len(sys.argv) > 4 else 0.10
s0 = np.load(R + 'sstar.npz'); S0 = s0['V']; Q0 = s0['Q']                       # envelope reference (S*)
b = np.load(R + 'sstar_ppu.npz'); VB = b['V']; QB = b['Q']; mirB = b['mir']
from scipy.spatial import cKDTree as _K
_d, _j = _K(S0).query(VB); oldmask = _d < 1e-9
Wb = dict(np.load(R + 'weights_body.npz')); J = json.loads(str(np.load(R + 'GR5DE3_r6.npz')['joints']))
# base attributes for the patched base: old vertices copy, patch vertices from the nearest S* surface point (barycentric)
T0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]
nb = len(VB); n2o = np.where(oldmask, _j, -1)
newi = np.where(~oldmask)[0]; d, fi, cp = igl.point_mesh_squared_distance(VB[newi], S0, T0)
bc = igl.barycentric_coordinates(cp, S0[T0[fi, 0]], S0[T0[fi, 1]], S0[T0[fi, 2]])
rows = list(np.where(oldmask)[0]); cols = list(n2o[oldmask]); vals = [1.0] * oldmask.sum()
for k, i in enumerate(newi):
    for c in range(3): rows.append(i); cols.append(T0[fi[k], c]); vals.append(bc[k, c])
B2S = sp.csr_matrix((vals, (rows, cols)), shape=(nb, len(S0)))              # patched base <- S* vertex attributes
WB = {k: B2S @ v for k, v in Wb.items()}
Q, n, S, mir = subdivide_levels(QB, nb, 2, mirB); S = S.tocsr(); SS = (S @ B2S).tocsr()   # production <- S* vertices
P = S @ VB
ok = mir >= 0; res = np.zeros(n); res[ok] = np.abs(P[ok] - P[mir[ok]] * np.array([-1, 1, 1])).max(1); mir[res > 1e-3] = -1
hq, sgn, ht = hidden_quads(S0, Q0); vis = ~ht
bz = base_zones(S0, Wb, J); pz = {k: (SS @ v.astype(float)) > 0.5 for k, v in bz.items()}
# contact zones: production vertices within 4 cm of a hidden S* triangle
Hc = S0[T0[ht]].mean(1)
from scipy.spatial import cKDTree
chg = ~oldmask | (np.linalg.norm(VB - S0[np.where(oldmask, n2o, 0)], axis=1) > 1e-6)
chg |= np.isin(np.arange(nb), np.unique(QB[np.zeros(len(QB),bool)]))
dz = cKDTree(VB[chg]).query(P)[0]; cz = dz < 3.0; ramp = np.clip((dz - 3.0) / 3.0, 0, 1)
armL = sum(Wb[k] for k in ('upperarm_l', 'lowerarm_l', 'hand_l', 'fingers_l')); armR = sum(Wb[k] for k in ('upperarm_r', 'lowerarm_r', 'hand_r', 'fingers_r'))
xs = S0[:, 0]
labS = np.where(armL > 0.5, 3, np.where(armR > 0.5, 4, np.where(xs > 0.05, 1, np.where(xs < -0.05, 2, 0))))
aLP = SS @ armL; aRP = SS @ armR
labP = np.where(aLP > 0.5, 3, np.where(aRP > 0.5, 4, np.where(P[:, 0] > 0.05, 1, np.where(P[:, 0] < -0.05, 2, 0))))
labT = np.array([np.bincount(labS[t], minlength=5).argmax() for t in T0])
xmin = S0[T0][:, :, 0].min(1); xmax = S0[T0][:, :, 0].max(1)
allow = {0: [0, 1, 2], 1: [0, 1], 2: [0, 2], 3: [3], 4: [4]}
groups = {}
for l in range(5):
    g = vis & np.isin(labT, allow[l])
    if l == 1: g &= xmin >= -0.01
    if l == 2: g &= xmax <= 0.01
    groups[l] = np.where(g)[0]
allvis = np.where(vis)[0]
E = np.unique(np.sort(np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]), 1), axis=0)
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)); A = (A + A.T).tocsr(); deg = np.asarray(A.sum(1)).ravel()
clr = np.load(R + 'clr.npy'); assert len(clr) == n
rc = np.clip((clr - 0.1) / 0.3, 0, 1); ramp = ramp * rc
_ev = np.load(R + 'vis_sstar.npz')['tri']; _hc = S0[T0[~_ev]].mean(1)
_dh = cKDTree(_hc).query(P)[0]; ramp = ramp * np.clip((_dh - 0.5) / 1.0, 0, 1)           # interior (non-exterior-visible) surfaces stay linear                       # no smoothing where another surface is < 1-4 mm away
delta = np.minimum(np.where(pz['T2'], D2, D1), clr / 4) * ramp
pin = np.zeros(n, bool); pin[:nb] = True                                     # base (MPFB / patch) vertices stay exactly on the target
nn = np.cross(S0[T0[:, 1]] - S0[T0[:, 0]], S0[T0[:, 2]] - S0[T0[:, 0]]); TN = sgn * nn / np.linalg.norm(nn, axis=1)[:, None]
QT = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
def vnormals(P):
    fn = np.cross(P[QT[:, 1]] - P[QT[:, 0]], P[QT[:, 2]] - P[QT[:, 0]]); vn = np.zeros_like(P)
    for k in range(3): np.add.at(vn, QT[:, k], fn)
    return sgn * vn / (np.linalg.norm(vn, axis=1)[:, None] + 1e-30)
def constrain(P):
    o = P.copy(); VN = vnormals(P)
    def apply(idx, faces, dl):
        d, fi, cp = igl.point_mesh_squared_distance(P[idx], S0, T0[faces]); fi = faces[fi]
        sd = ((P[idx] - cp) * TN[fi]).sum(1)                              # signed distance to the envelope
        tgt = np.clip(sd, -dl, dl)
        nv = VN[idx]; cosn = (nv * TN[fi]).sum(1)
        mv = (sd - tgt) / np.maximum(cosn, 0.5); dist = np.sqrt(d)
        mv = np.clip(mv, -dist - 0.01, dist + 0.01)
        cl = cp + TN[fi] * tgt[:, None]                                      # fallback: closest point + clamped offset
        o[idx] = np.where((cosn > 0.5)[:, None], P[idx] - nv * mv[:, None], cl)   # move along the vertex normal when well aligned
    apply(np.where(~cz)[0], allvis, delta[~cz])
    return o
def symm(P):
    m = mir >= 0; Pm = P.copy(); Pm[m] = 0.5 * (P[m] + P[mir[m]] * np.array([-1, 1, 1])); self_ = m & (mir == np.arange(n)); Pm[self_, 0] = 0.0; return Pm
P0 = P.copy(); NORMAL_ONLY = float(__import__('os').environ.get('NORMAL_ONLY', '1'))
for it in range(IT):
    for f in (0.5, -0.53):
        L = (A @ P) / deg[:, None] - P; VN_ = vnormals(P); L = (L * VN_).sum(1)[:, None] * VN_ * NORMAL_ONLY + L * (1 - NORMAL_ONLY); P = P + f * ramp[:, None] * L
    P = symm(constrain(P)); P[cz] = P0[cz]; P[pin] = P0[pin]
np.savez(out, V=P, Q=Q, mir=mir, labP=labP, cz=cz, **{'zone_' + k: v for k, v in pz.items()})
sp.save_npz(out.replace('.npz', '_SS.npz'), SS); sp.save_npz(out.replace('.npz', '_S.npz'), S)
print('saved', out, n, len(Q))
