# vc3_fair.py CONFIG.json IN_CORR.npz OUT_CORR.npz SIDE : Track E2 (order 28dd8d3 §6) contact-interface fairing of the VC3 130-degree key.
# Diagnostic only; the frozen rest mesh is never touched. Only the K130_{side} rest-space key changes; every other key (and therefore every angle <= 120
# degrees) is copied bit-identically.
#  1. X = posed VC3 at 130 (LBS of V0 + K130), X0 = posed W0 LBS at 130; corrective displacement field  Delta = X - X0.
#  2. interface seam I = arm vertices whose nearest vertex on the OTHER segment (upper arm vs forearm side of the posed bisector plane) is closer than
#     seam_cm; interface support = rest-geodesic distance to I <= band_cm, weight beta = C2 ramp (1 inside band_full_cm, 0 at band_cm) -- declared mask.
#  3. Taubin (lambda / mu) smoothing of Delta restricted to the support (outside it Delta is held: Dirichlet), blended by beta: Delta' = Delta + beta(Delta_s - Delta).
#     Smoothing the corrective FIELD (not positions) removes the high-frequency rumpling it carries while leaving the LBS base shape and the gross
#     contact displacement in place.
#  4. optional volume lock: the overlap-free closed-volume change caused by the fairing is given back as a smooth normal offset over the support
#     minus the seam (lock_volume), so the VC3 physical-volume gain is not spent.
#  4b. optional hold (F2): vertices within hold_cm of the other side keep their VC3 position (Dirichlet), ramped over hold_ramp_cm.
#  5. optional contact guard (F2): vertices that cross the posed bisector plane / come within gap_cm of the other side after fairing are pulled back along
#     the plane normal (contact_guard).
#  6. K130' = K130 + Lin^-1 (Delta' - Delta)  (exact inverse of the per-vertex LBS linear part, source <-> Blender axis flip handled).
# Writes OUT_CORR.npz and OUT_CORR_log.json (support mask ids + statistics).
import sys, os, json, hashlib, numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import Rig, build_poses, src_to_bl, bl_to_src
os.environ.setdefault('ELBOW_SET', '1'); os.environ.setdefault('ELBOW_SET_R', '1'); os.environ.setdefault('ELBOW_ARC', '1')
CF, IN, OUT, S = sys.argv[1:5]; CFG = json.load(open(CF))
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', RD + '/rig/weights_v001c.npz'); P = build_poses(rig)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
EL = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1); G = sp.csr_matrix((np.r_[EL, EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
C = np.load(IN); K = C['K130_' + S].astype(np.float64); pose = P['D2_%s_flex130' % S]
FLIP = np.array([1.0, -1.0, 1.0])
def posed(D):
    Vb, L, M = rig.skin(src_to_bl(V0 + D), pose); return bl_to_src(Vb), L, M
X, L, M = posed(K); X0, _, _ = posed(np.zeros_like(V0))
arm = np.zeros(nV, bool); arm[Q[FP == PARTS.index('arm_' + S)].ravel()] = True
# posed bisector plane (same construction as corr_solve)
g = lambda b: bl_to_src(M[b][:3, 3][None])[0]
pe, psh, pw = g('forearm_' + S), g('upperarm_' + S), g('hand_' + S); ra = (psh - pe) / np.linalg.norm(psh - pe); rb = (pw - pe) / np.linalg.norm(pw - pe)
PN = (ra - rb) / np.linalg.norm(ra - rb); side = (X - pe) @ PN > 0                       # True = upper-arm side
ia = np.nonzero(arm)[0]; up = ia[side[ia]]; lo = ia[~side[ia]]
du, _ = cKDTree(X[lo]).query(X[up]); dl, _ = cKDTree(X[up]).query(X[lo])
dn = np.full(nV, np.inf); dn[up] = du; dn[lo] = dl
seam = np.nonzero(arm & (dn < CFG['seam_cm']))[0]
gd = dijkstra(G, directed=False, indices=seam, limit=CFG['band_cm'] + 0.5, min_only=True); gd = np.where(np.isfinite(gd), gd, 1e9)
beta = c2((CFG['band_cm'] - gd) / (CFG['band_cm'] - CFG['band_full_cm'])); beta[~arm] = 0.0
if CFG.get('hold_cm', 0) > 0:                                          # F2: the tight contact itself is held (Dirichlet) so the seam / crease is not re-opened
    beta *= c2((dn - CFG['hold_cm']) / CFG.get('hold_ramp_cm', 0.5)); beta[~np.isfinite(dn)] = np.where(arm, beta, 0)[~np.isfinite(dn)]
sup = np.nonzero(beta > 0)[0]
# Taubin smoothing of the displacement field on the support (Dirichlet outside)
Dl = X - X0; Ds = Dl.copy()
A = sp.csr_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV)); As = A[sup]; dg = np.asarray(As.sum(1)).ravel()
for _ in range(CFG['iters']):
    for f_ in (CFG.get('lam', 0.5), CFG.get('mu', -0.53)):
        Ds[sup] = Ds[sup] + f_ * ((As @ Ds) / dg[:, None] - Ds[sup])
Dn = Dl + beta[:, None] * (Ds - Dl)
TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
def cvol(Y): return float(np.einsum('ij,ij->i', Y[TRI[:, 0]], np.cross(Y[TRI[:, 1]], Y[TRI[:, 2]])).sum() / 6)
def vnorm(Y):
    fv = np.cross(Y[Q[:, 2]] - Y[Q[:, 0]], Y[Q[:, 3]] - Y[Q[:, 1]]); n = np.zeros((nV, 3))
    for k in range(4): np.add.at(n, Q[:, k], fv)
    return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
LOG = dict(config=CFG, side=S, seam_vertices=int(len(seam)), support_vertices=int(len(sup)), support_ids_sha256=hashlib.sha256(sup.astype(np.int32).tobytes()).hexdigest())
v_vc3 = cvol(X); Xn = X0 + Dn; LOG['closed_volume_change_by_fairing_cm3'] = round(cvol(Xn) - v_vc3, 2)
if CFG.get('lock_volume'):
    w = beta * c2((gd - CFG.get('lock_excl_cm', 1.0)) / 1.0); n_ = vnorm(Xn)
    fv = np.cross(Xn[Q[:, 2]] - Xn[Q[:, 0]], Xn[Q[:, 3]] - Xn[Q[:, 1]]) * 0.5; av = np.zeros((nV, 3))
    for k in range(4): np.add.at(av, Q[:, k], fv / 4)
    gain = (w * np.linalg.norm(av, axis=1)).sum(); lam = (v_vc3 - cvol(Xn)) / max(gain, 1e-9)
    Dn = Dn + (lam * w)[:, None] * n_; Xn = X0 + Dn; LOG['volume_lock_offset_cm'] = round(float(lam), 4)
if CFG.get('contact_guard'):
    gap = CFG.get('gap_cm', 0.05); sd = (Xn - pe) @ PN; up_ = arm & side; lo_ = arm & ~side
    fix = (up_ & (sd < gap)) | (lo_ & (sd > -gap)); fix &= beta > 0
    Xn[fix] += np.outer(np.where(side[fix], gap - sd[fix], -gap - sd[fix]), PN); Dn = Xn - X0; LOG['contact_guard_moved'] = int(fix.sum())
# back to the rest-space key: D' = D + Lin^-1 (Delta' - Delta) in Blender linear frame
dXb = (Dn - Dl) * FLIP / 100.0; Li = np.linalg.inv(L[sup]); dDb = np.einsum('vij,vj->vi', Li, dXb[sup])
Kn = K.copy(); Kn[sup] += dDb * 100.0 * FLIP
Xc, _, _ = posed(Kn); LOG['roundtrip_err_cm'] = float(np.abs(Xc - (X0 + Dn)).max())
LOG['max_change_cm'] = round(float(np.linalg.norm(Xc - X, axis=1).max()), 4); LOG['closed_volume_change_total_cm3'] = round(cvol(Xc) - v_vc3, 2)
LOG['outside_support_bit_identical'] = bool((Kn[beta == 0] == K[beta == 0]).all())
out = {k: C[k] for k in C.files}; out['K130_' + S] = Kn.astype(C['K130_' + S].dtype); out['fair_support_' + S] = beta.astype(np.float32)
np.savez_compressed(OUT, **out); json.dump(LOG, open(OUT[:-4] + '_log.json', 'w'), indent=1); print(json.dumps({k: v for k, v in LOG.items() if k != 'config'}))
