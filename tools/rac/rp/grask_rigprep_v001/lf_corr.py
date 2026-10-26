# lf_corr.py CONFIG.json OUTDIR : order bd11ab0 — one small LEFT-flex90 pose-space corrective on top of SW3 (anterior axillary fold only).
# Baseline SW3 = SW1 weights + S1 mechanics + 0.5 LBS/DQS blend (unchanged). The corrective is a rest-space shape key D (exact rest shape preserved:
# D is applied only when the driver is non-zero) found in posed space at D1_l_flex90:
#   support: rest vertices within R_out of the fold centre (GH_l + centre_offset_cm), left of x_min, arm_l / axial; weight beta = C2 taper (1 inside R_core,
#            0 at R_out) x exact-zero guard (beta forced 0 within guard_cm of the support boundary);
#   solve:   U (posed displacement) accumulated from a self-contact push -- for every support vertex v, nearby posed vertices u (< search_cm) that are far
#            apart at rest (> rest_sep_cm) and face it (n_u . n_v < face_cos) push v out to gap_cm along n_u -- then Laplacian-smoothed (Dirichlet 0
#            outside support) and multiplied by beta, iterated;  X* = X_SW3 + U;
#   LF2 option fair_cos: fold / inversion fairing inside the support each iteration.
#   key:     D = Lin^-1 (U) with Lin = the SW3 blended linear part, refined by re-evaluating the blend (fixed point, 3 passes).
# Driver: humeral forward elevation of the LEFT arm, theta_f = asin(forward component of the world humerus direction); activation
#   a = smoothstep(act0, act1, theta_f) -> exactly 0 for theta_f <= act0 (abd*, ext30, girdle flex 64 deg, right arm poses, every non-D1 pose).
# Writes OUTDIR/lf_key.npz (D, beta, config), OUTDIR/lf_log.json and OUTDIR/vsrc/<pose>.npz for the requested poses (SW3 posed copied bit-for-bit when a = 0).
import sys, os, json, hashlib, shutil, numpy as np
from scipy.spatial import cKDTree
import scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import Rig, build_poses, bl_to_src
from dqs_blend import blend_pose
CF, O = sys.argv[1:3]; CFG = json.load(open(CF)); os.makedirs(O + '/vsrc', exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', CFG['weights']); P = build_poses(rig)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
vpart = np.empty(nV, object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
A = sp.csr_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
LM = json.load(open(RD + '/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']; gh = np.array(LM['glenohumeral_l']['position_source_frame_cm'])
bmask = np.load(CFG['blend_mask'])
def driver(pose):
    M, _ = rig.pose_mats(pose); h = M['upperarm_l'][:3, 3]; L_ = np.linalg.norm(np.array(rig.B['upperarm_l']['tail']) - np.array(rig.B['upperarm_l']['head']))
    t = (M['upperarm_l'] @ np.r_[0, L_, 0, 1])[:3]; d = (t - h) / np.linalg.norm(t - h); fwd = -d[1]          # Blender -y = source forward
    th = float(np.degrees(np.arcsin(np.clip(fwd, -1, 1)))); a0, a1 = CFG['act0'], CFG['act1']; u = min(max((th - a0) / (a1 - a0), 0.0), 1.0); return th, u * u * (3 - 2 * u)
# support
cen = gh + np.array(CFG['centre_offset_cm']); dr_ = np.linalg.norm(V0 - cen, axis=1)
beta = c2((CFG['R_out'] - dr_) / (CFG['R_out'] - CFG['R_core'])) * np.isin(vpart, ['arm_l', 'axial']) * (V0[:, 0] > CFG['x_min'])
inside = beta > 0
for _ in range(CFG.get('guard_rings', 3)):                              # exact-zero guard: rings adjacent to the outside are forced to 0
    out_ = ~inside; nb_out = np.asarray(A[:, np.nonzero(out_)[0]].sum(1)).ravel() > 0; inside = inside & ~nb_out
beta = np.where(inside, beta, 0.0); sv = np.nonzero(beta > 0)[0]
pk = 'D1_l_flex90'; X0, Lin = blend_pose(rig, V0, P[pk], bmask)
Xsw = np.load(CFG['sw3_posed'])['V'].astype(float); LOG = dict(config=CFG, support_vertices=int(len(sv)), base_vs_sw3_file_max_cm=float(np.abs(X0 - Xsw).max()))
def normals(X):
    fv = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); n = np.zeros((nV, 3))
    for k in range(4): np.add.at(n, Q[:, k], fv)
    return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
As = A[sv]; dg = np.asarray(As.sum(1)).ravel(); U = np.zeros((nV, 3)); hist = []
for it in range(CFG['iters']):
    X = X0 + U; n = normals(X); tr = cKDTree(X[sv]); push = np.zeros((nV, 3)); cnt = np.zeros(nV)
    pairs = tr.query_pairs(CFG['search_cm'], output_type='ndarray')
    if len(pairs):
        a_, b_ = sv[pairs[:, 0]], sv[pairs[:, 1]]
        ok = (np.linalg.norm(V0[a_] - V0[b_], axis=1) > CFG['rest_sep_cm']) & ((n[a_] * n[b_]).sum(1) < CFG['face_cos'])
        a_, b_ = a_[ok], b_[ok]
        for v, u in ((a_, b_), (b_, a_)):
            d = ((X[v] - X[u]) * n[u]).sum(1); m = d < CFG['gap_cm']
            np.add.at(push, v[m], 0.5 * (CFG['gap_cm'] - d[m])[:, None] * n[u[m]]); np.add.at(cnt, v[m], 1)
    nz = cnt > 0; push[nz] /= cnt[nz, None]; hist.append(dict(it=it, pushed=int(nz.sum()), max_push_cm=round(float(np.linalg.norm(push, axis=1).max()), 4)))
    U = U + CFG.get('push_gain', 1.0) * push
    if CFG.get('fair_cos'):                                                # LF2: fold / inversion fairing -- vertices whose normal disagrees with their one-ring
        nm_ = (A @ n) / np.maximum(np.asarray(A.sum(1)).ravel(), 1)[:, None]  # mean normal are pulled (with their one-ring) toward the one-ring mean position
        bad = np.zeros(nV, bool); bad[sv] = (n[sv] * nm_[sv]).sum(1) < CFG['fair_cos']
        for _ in range(CFG.get('fair_rings', 1)): bad = bad | (np.asarray(A[:, np.nonzero(bad)[0]].sum(1)).ravel() > 0)
        bad &= beta > 0; Xm = (A @ X) / np.maximum(np.asarray(A.sum(1)).ravel(), 1)[:, None]
        U[bad] += CFG.get('fair_gain', 0.5) * (Xm[bad] - X[bad]); hist[-1]['faired'] = int(bad.sum())
    for _ in range(CFG['smooth_iters']): U[sv] = 0.5 * U[sv] + 0.5 * (As @ U) / dg[:, None]
    U[beta == 0] = 0.0
U *= beta[:, None]                                                         # final C2 taper (exact 0 at the guarded boundary)
Xt = X0 + U
# rest-space key through the SW3 blended linear part (fixed point)
FL = np.array([1.0, -1.0, 1.0]); D = np.zeros((nV, 3))
for _ in range(3):
    Xd, Lc = blend_pose(rig, V0 + D, P[pk], bmask); r = (Xt - Xd) * FL / 100.0
    D[sv] += np.einsum('vij,vj->vi', np.linalg.inv(Lc[sv]), r[sv]) * 100.0 * FL
Xf, _ = blend_pose(rig, V0 + D, P[pk], bmask)
LOG.update(key_fit_err_cm=float(np.abs(Xf - Xt).max()), max_posed_delta_cm=round(float(np.linalg.norm(U, axis=1).max()), 4), max_rest_key_cm=round(float(np.linalg.norm(D, axis=1).max()), 4),
           changed_vertices=int((np.linalg.norm(D, axis=1) > 0).sum()), key_outside_support_zero=bool((D[beta == 0] == 0).all()), support_ids_sha256=hashlib.sha256(sv.astype(np.int32).tobytes()).hexdigest(),
           boundary_max_delta_cm=float(np.linalg.norm(U[np.nonzero(np.asarray(A[:, sv].sum(1)).ravel() > 0)[0]][beta[np.nonzero(np.asarray(A[:, sv].sum(1)).ravel() > 0)[0]] < 0.05], axis=1).max()) if len(sv) else 0.0,
           hist=hist[-5:])
np.savez_compressed(O + '/lf_key.npz', D=D.astype(np.float32), beta=beta.astype(np.float32), act0=CFG['act0'], act1=CFG['act1'])
acts = {}
for pn in CFG['poses']:
    th, a = driver(P[pn]); acts[pn] = dict(theta_forward_deg=round(th, 2), activation=round(a, 6))
    src_ = CFG['sw3_posed_dir'] + '/%s.npz' % pn
    if a == 0.0: shutil.copy(src_, O + '/vsrc/%s.npz' % pn)
    else:
        Xp, _ = blend_pose(rig, V0 + a * D, P[pn], bmask); np.savez_compressed(O + '/vsrc/%s.npz' % pn, V=Xp.astype(np.float32))
LOG['activation'] = acts; json.dump(LOG, open(O + '/lf_log.json', 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in LOG.items() if k not in ('config', 'hist', 'activation')})); print({k: v['activation'] for k, v in acts.items() if v['activation'] > 0})
