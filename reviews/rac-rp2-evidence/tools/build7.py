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
xmin = S0[T0][:, :, 0].min(1); xmax = S0[T0][:, :, 0].max(1); C0x = S0[T0][:, :, 0].mean(1)
_ext = np.load(R + 'vis_sstar.npz')['tri']; allvis = np.where(vis)[0]; vis = vis & _ext
isA = armS_T = None
armT_any = np.array([(labS[t] >= 3).any() for t in T0]); trT_any = np.array([(labS[t] < 3).any() for t in T0])
groups = {}
groups[0] = np.where(vis & trT_any)[0]
groups[1] = np.where(vis & trT_any & (xmin >= -0.01))[0]
groups[2] = np.where(vis & trT_any & (xmax <= 0.01))[0]
groups[3] = np.where(vis & armT_any & (C0x > 0))[0]
groups[4] = np.where(vis & armT_any & (C0x < 0))[0]
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
    def apply(idx, faces, dl, strict=False):
        d, fi, cp = igl.point_mesh_squared_distance(P[idx], S0, T0[faces]); fi = faces[fi]
        sd = ((P[idx] - cp) * TN[fi]).sum(1)                              # signed distance to the envelope
        tgt = np.clip(sd, -dl, dl)
        nv = VN[idx]; cosn = (nv * TN[fi]).sum(1)
        mv = (sd - tgt) / np.maximum(cosn, 0.5); dist = np.sqrt(d)
        mv = np.clip(mv, -dist - 0.01, dist + 0.01)
        cl = cp + TN[fi] * tgt[:, None]                                      # fallback: closest point + clamped offset
        if strict: step = cp - P[idx]; ln = np.linalg.norm(step, axis=1)[:, None]; cl = P[idx] + step * np.minimum(1.0, 0.03 / (ln + 1e-12))
        o[idx] = np.where((cosn > 0.5)[:, None], P[idx] - nv * mv[:, None], cl)   # move along the vertex normal when well aligned
    apply(np.where(~cz)[0], allvis, delta[~cz])
    for l in range(5):
        idx = np.where(pd & (labP == l) & ~pin)[0]
        if len(idx): apply(idx, groups[l], np.zeros(len(idx)), strict=True)
    return o
def symm(P):
    m = mir >= 0; Pm = P.copy(); Pm[m] = 0.5 * (P[m] + P[mir[m]] * np.array([-1, 1, 1])); self_ = m & (mir == np.arange(n)); Pm[self_, 0] = 0.0; return Pm
newB = ~oldmask & ~((np.abs(VB[:, 0]) < 8) & (VB[:, 2] > 100) & (VB[:, 2] < 122)); pd = np.asarray(S[:, newB].sum(1)).ravel() > 0
_np = np.where(~pd & ~cz)[0]; _d, _fi, _cp = igl.point_mesh_squared_distance(P[_np], S0, T0); _ok = _d < 0.3 ** 2
P[_np[_ok]] = _cp[_ok]                                                        # bilinear sub-vertices snapped onto the S* triangles
pin[:nb] &= ~newB                                                             # patch base vertices are free (projected each iteration)
def _poly_dense(c, k=20):
    c = np.asarray(c, float); out = [c[0]]
    for a_, b_ in zip(c[:-1], c[1:]):
        for t in np.linspace(0, 1, k + 1)[1:]: out.append(a_ + t * (b_ - a_))
    return np.array(out)
_crs = {}
cA = np.load(R + 'crease_axL_dense.npy'); cA = cA[np.argsort(cA[:, 1])]
for _ in range(4): cA[1:-1] = 0.5 * cA[1:-1] + 0.25 * (cA[:-2] + cA[2:])
_crs['axL'] = cA; _crs['axR'] = cA * np.array([-1, 1, 1]); _crs['crotch'] = np.asarray(b['crease_crotch'], float)
for _k in list(_crs):
    sv = b['seam_' + _k]
    if len(sv) == 0: _crs.pop(_k); continue
    a0, a1 = VB[sv[0]], VB[sv[-1]]; c = _crs[_k]
    if np.linalg.norm(c[0] - a0) > np.linalg.norm(c[-1] - a0): c = c[::-1]
    _crs[_k] = np.vstack([a0, c, a1])
seamv = {}
Sc = S.tocsc()
for key in ('crotch', 'axL', 'axR'):
    sb = np.zeros(nb, bool); sb[b['seam_' + key]] = True
    nzr = S.indptr; ok = np.zeros(n, bool)
    rows_any = np.asarray(S[:, sb].sum(1)).ravel() > 0.999
    seamv[key] = np.where(rows_any & ~pin)[0]
from scipy.spatial import cKDTree as _KD
def seam_project(P):
    for key, idx in seamv.items():
        if key not in _crs: continue
        if len(idx):
            c = _crs[key]; A_ = c[:-1]; B_ = c[1:]; AB = B_ - A_; L2 = (AB ** 2).sum(1) + 1e-12
            X = P[idx][:, None, :] - A_[None]; t = np.clip((X * AB[None]).sum(2) / L2[None], 0, 1)
            Cp = A_[None] + t[:, :, None] * AB[None]; dd = ((P[idx][:, None, :] - Cp) ** 2).sum(2); k = dd.argmin(1)
            P[idx] = Cp[np.arange(len(idx)), k]
        if key == 'crotch': P[idx, 0] = 0.0
    return P
P0 = P.copy(); NORMAL_ONLY = float(__import__('os').environ.get('NORMAL_ONLY', '1'))
for it in range(IT):
    for f in (0.5, -0.53):
        L = (A @ P) / deg[:, None] - P; P[pd & ~pin] += f * 0.8 * L[pd & ~pin]; VN_ = vnormals(P); L = (L * VN_).sum(1)[:, None] * VN_ * NORMAL_ONLY + L * (1 - NORMAL_ONLY); P = P + f * ramp[:, None] * L
    P = seam_project(symm(constrain(P))); keep = cz & ~pd; P[keep] = P0[keep]; P[pin] = P0[pin]
for it2 in range(30):
    for l in range(5):
        idx = np.where(pd & (labP == l) & ~pin)[0]
        if not len(idx): continue
        d, fi, cp = igl.point_mesh_squared_distance(P[idx], S0, T0[groups[l]]); far = np.sqrt(d) > 0.06
        step = cp[far] - P[idx[far]]; ln = np.linalg.norm(step, axis=1)[:, None]; P[idx[far]] += step * np.minimum(1.0, 0.03 / (ln + 1e-12))
    P = seam_project(symm(P)); P[pin] = P0[pin]
np.savez(out, V=P, Q=Q, mir=mir, labP=labP, cz=cz, **{'zone_' + k: v for k, v in pz.items()})
sp.save_npz(out.replace('.npz', '_SS.npz'), SS); sp.save_npz(out.replace('.npz', '_S.npz'), S)
print('saved', out, n, len(Q))
