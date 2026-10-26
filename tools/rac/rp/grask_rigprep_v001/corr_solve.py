# corr_solve.py OUTDIR TAG SIDE CONFIG.json : pose-space elbow corrective (order 6c38d75 §5-§9). Diagnostic only; never edits the rest mesh.
# For each keyed flexion angle (CONFIG anchors[1:]) the target posed shape of the elbow support region is solved in posed space and converted to a
# REST-SPACE delta (exact inverse of the per-vertex LBS linear part), i.e. a pose-driven shape key applied before the armature:
#   LBS(V0 + D_k) = LBS(V0) + Lin_v D_k  ->  D_k = Lin_v^-1 (X*_k - LBS(V0)).
# Target X*_k (projective-dynamics style, sparse least squares re-solved each outer iteration):
#   * detail term   : uniform Laplacian of X equals the LBS posed Laplacian (smooth harmonic correction field), optionally blended (CONFIG.rest_detail,
#                     scaled by tau) with the REST Laplacian rotated by the per-vertex skinning rotation (polar part of Lin), which un-crumples LBS;
#   * anchor term   : (1 - tau) * w_anchor * |X - LBS|  (tau = 1 in the core, C2 smootherstep taper to 0 at the support boundary; outside = fixed);
#   * collision term: support vertices found behind a non-local posed face (rest separation > CONFIG.local_cm) within depth CONFIG.depth_cm are
#                     projected to that face plane + gap (both sides of a contact are processed, each moves its own vertices);
#   * loop floor    : tagged elbow loop pairs (the retained metric's nearest-vertex pairs) kept >= CONFIG.loop_floor x rest distance;
#   * edge floor    : every support edge kept >= CONFIG.edge_floor x rest length (prevents collapsed quads).
# Final delta is multiplied by a C2 guard that is 1 inside R_out - guard_cm and exactly 0 at R_out (exact zero at the boundary).
import sys, os, json, hashlib, collections, numpy as np
import bpy  # noqa: F401  (bpy python: provides mathutils BVHTree)
from mathutils.bvhtree import BVHTree
import scipy.sparse as sp, scipy.sparse.linalg as spl
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import Rig, build_poses, src_to_bl, bl_to_src
from common import PARTS
a_ = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]; O, TAG, S, CFGF = a_[:4]; CFG = json.load(open(CFGF)); os.makedirs(O, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', RD + '/rig/weights_v001c.npz')
os.environ['ELBOW_SET'] = '1'; os.environ['ELBOW_SET_R'] = '1'; os.environ['ELBOW_ARC'] = '1'; P = build_poses(rig)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
LOOPS = json.load(open('/tmp/claude-0/rt/r4/loops.json'))
e = bl_to_src(np.array(rig.B['forearm_' + S]['head'])[None])[0]
d = np.linalg.norm(V0 - e, axis=1)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
nb = [[] for _ in range(nV)]
_Es = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); _ue, _inv = np.unique(_Es, axis=0, return_inverse=True)
EFP = np.tile(np.arange(len(Q)), 4)[np.argsort(_inv.ravel(), kind='stable')].reshape(-1, 2)          # the 2 faces of every edge
def _fn(X_):
    n_ = np.cross(X_[Q[:, 2]] - X_[Q[:, 0]], X_[Q[:, 3]] - X_[Q[:, 1]]); return n_ / np.maximum(np.linalg.norm(n_, axis=1), 1e-12)[:, None]
_N0 = _fn(V0); _NS0 = np.zeros_like(_N0); np.add.at(_NS0, EFP[:, 0], _N0[EFP[:, 1]]); np.add.at(_NS0, EFP[:, 1], _N0[EFP[:, 0]]); INV0 = (_N0 * _NS0).sum(1) < 0
for a, b in E: nb[a].append(b); nb[b].append(a)
# ---- support: one connected component of arm_S vertices within R_out of the pivot
R_core, R_out, guard = CFG['R_core'], CFG['R_out'], CFG.get('guard_cm', 1.0)
vpart = np.empty(nV, object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
sup = (vpart == 'arm_' + S) & (d < R_out)
adj = collections.defaultdict(list)
for a, b in E[sup[E[:, 0]] & sup[E[:, 1]]]: adj[a].append(b); adj[b].append(a)
seen = set(); comps = []
for v in np.nonzero(sup)[0]:
    if v in seen: continue
    c = [v]; st = [v]; seen.add(v)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y); c.append(y)
    comps.append(c)
big = max(comps, key=len); dropped = [c for c in comps if c is not big]
for c in dropped: sup[c] = False
sv = np.nonzero(sup)[0]; idx = -np.ones(nV, int); idx[sv] = np.arange(len(sv)); n = len(sv)
def c2(t): t = np.clip(t, 0, 1); return t * t * t * (t * (6 * t - 15) + 10)          # smootherstep (C2)
tau = 1 - c2((d - R_core) / (R_out - R_core)); tau[~sup] = 0.0
gd = 1 - c2((d - (R_out - guard)) / guard); gd[~sup] = 0.0                         # final exact-zero guard
# the support can also end at a PART boundary (arm vs torso / hand) inside R_out: guard by the surface (edge-graph) distance to ANY support boundary
from scipy.sparse.csgraph import dijkstra
_EL = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1); _G = sp.csr_matrix((np.r_[_EL, _EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
_bnd = np.unique(np.r_[E[sup[E[:, 0]] & ~sup[E[:, 1]], 0], E[sup[E[:, 1]] & ~sup[E[:, 0]], 1]])
_dist = np.full(nV, np.inf)
if len(_bnd): _dist = dijkstra(_G, directed=False, indices=_bnd, limit=CFG.get('boundary_guard_cm', 1.5) + 0.5, min_only=True)
gb = c2(np.where(np.isfinite(_dist), _dist, 1e9) / CFG.get('boundary_guard_cm', 1.5)); gd = gd * gb; gd[~sup] = 0.0; tau = tau * gb
ua_ = e - bl_to_src(np.array(rig.B['upperarm_' + S]['head'])[None])[0]; ua_ /= np.linalg.norm(ua_)
fa_ = bl_to_src(np.array(rig.B['forearm_' + S]['tail'])[None])[0] - e; fa_ /= np.linalg.norm(fa_); AX = (ua_ + fa_) / np.linalg.norm(ua_ + fa_)
ANT = np.array([0, 1.0, 0]); ANT -= (ANT @ AX) * AX; ANT /= np.linalg.norm(ANT)          # flexor (inner) side
FSIDE = rig.W[:, rig.names.index('forearm_' + S)] > 0.5                                  # forearm-side flesh (W0 forearm share > 0.5)
# ---- rest Laplacian
deg = np.array([len(x) for x in nb]); NB0 = np.array([x[0] for x in nb]); Mn = np.zeros((nV, 3))
for a, b in E: Mn[a] += V0[b]; Mn[b] += V0[a]
delta0 = V0 - Mn / deg[:, None]
# Laplacian rows (support vertices): x_i - mean(x_nb) = R_i delta0_i ; neighbours outside the support are constants
rows, cols, vals = [], [], []
for k, v in enumerate(sv):
    rows.append(k); cols.append(k); vals.append(1.0)
    for w in nb[v]:
        if sup[w]: rows.append(k); cols.append(idx[w]); vals.append(-1.0 / deg[v])
Lmat = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
ext = np.array([[w for w in nb[v] if not sup[w]] for v in sv], dtype=object)
tagged = {}
for k in range(17, 23):
    nm = 'LOOP_elbow_%s_%d' % (S, k)
    if nm in LOOPS: tagged[k] = np.array(LOOPS[nm])
LP = []                                                                             # retained loop-metric pairs (rest nearest-vertex pairing)
ks = sorted(tagged)
for k1, k2 in zip(ks[:-1], ks[1:]):
    a1, a2 = tagged[k1], tagged[k2]; dd = np.linalg.norm(V0[a1][:, None] - V0[a2][None], axis=2); j = a2[dd.argmin(1)]
    for a_, b_, r0 in zip(a1, j, dd.min(1)): LP.append((a_, b_, r0))
LP = [p for p in LP if sup[p[0]] and sup[p[1]]]
SE = E[sup[E[:, 0]] & sup[E[:, 1]]]; SE0 = np.linalg.norm(V0[SE[:, 0]] - V0[SE[:, 1]], axis=1)
def polar(M):
    U, _, Vt = np.linalg.svd(M); R = U @ Vt
    if np.linalg.det(R) < 0: U[:, -1] *= -1; R = U @ Vt
    return R
Fl = np.diag([1.0, -1.0, 1.0])
CF = np.nonzero(sup[Q].any(1))[0]                                                  # faces touching the support (collision partners)
C0f = V0[Q[CF]].mean(1)
def fnorm(X, F):
    nr = np.cross(X[Q[F, 2]] - X[Q[F, 0]], X[Q[F, 3]] - X[Q[F, 1]]); return nr / np.maximum(np.linalg.norm(nr, axis=1), 1e-12)[:, None]
LOG = dict(tag=TAG, side=S, config=CFG, method=open(__file__).read().split('import sys')[0], support=dict(vertices=int(n), core=int((sup & (d <= R_core)).sum()),
           band=int((sup & (d > R_core)).sum()), dropped_islands=[len(c) for c in dropped], parts=sorted(set(vpart[sv]))), keys={})
OUT = dict(anchors=np.array(CFG['anchors'], float))
for ang in CFG['anchors'][1:]:
    pname = 'D2_%s_flex%d' % (S, ang)
    # key pose = ELBOW FLEXION ONLY (the abd45 shoulder setup of the test poses is removed), so the key carries no shoulder-pose correction;
    # the rest-space delta is then valid for any shoulder pose (it is applied before skinning)
    KP = {b: r for b, r in P[pname].items() if b.startswith('forearm_')} if CFG.get('key_pose', 'elbow_only') == 'elbow_only' else P[pname]
    Vb, Lin, M = rig.skin(src_to_bl(V0), KP); X0 = bl_to_src(Vb)                    # LBS posed (source frame)
    Ls = np.einsum('ij,njk,kl->nil', Fl, Lin, Fl)                                    # per-vertex linear part in the source frame (cm units cancel)
    Rv = np.array([polar(Ls[v]) for v in sv]); rot_delta = np.einsum('nij,nj->ni', Rv, delta0[sv])
    MnX = np.zeros((nV, 3)); np.add.at(MnX, E[:, 0], X0[E[:, 1]]); np.add.at(MnX, E[:, 1], X0[E[:, 0]]); lbs_delta = (X0 - MnX / deg[:, None])[sv]
    lam = CFG.get('rest_detail', 0.0) * tau[sv][:, None]                           # 0 = smooth (harmonic) displacement of the LBS shape; >0 blends in rotated rest detail
    tgt_delta = (1 - lam) * lbs_delta + lam * rot_delta
    # constant part from outside neighbours
    bL = tgt_delta.copy()
    for k, v in enumerate(sv):
        if ext[k]: bL[k] += X0[ext[k]].sum(0) / deg[v]
    # stable orientation for contact tests: the SKINNED-REFERENCE normals (rest normals carried by the per-vertex LBS linear part), not the
    # current posed normals, which are themselves flipped inside the LBS crease
    N0f = fnorm(V0, CF); NFREF = np.einsum('nij,nj->ni', Ls[Q[CF]].mean(1), N0f); NFREF /= np.linalg.norm(NFREF, axis=1)[:, None]
    VN0 = np.zeros((nV, 3))
    for kk in range(4): np.add.at(VN0, Q[CF, kk], N0f)
    VNREF = np.einsum('nij,nj->ni', Ls, VN0); VNREF /= np.maximum(np.linalg.norm(VNREF, axis=1), 1e-12)[:, None]
    # ---- delta-mush base (CONFIG.dm_iters > 0): smooth the LBS shape inside the support and re-apply the rest detail in local frames
    Xb = X0.copy()
    if CFG.get('dm_iters', 0) > 0:
        def smooth(Y, k):
            Y = Y.copy()
            for _ in range(k):
                Mn_ = np.zeros_like(Y); np.add.at(Mn_, E[:, 0], Y[E[:, 1]]); np.add.at(Mn_, E[:, 1], Y[E[:, 0]]); Ym = Mn_ / deg[:, None]
                Y[sv] = Y[sv] + 0.5 * (Ym[sv] - Y[sv])
            return Y
        def frames(Y):
            Nv = np.zeros_like(Y); fn_ = np.cross(Y[Q[:, 2]] - Y[Q[:, 0]], Y[Q[:, 3]] - Y[Q[:, 1]])
            for kk in range(4): np.add.at(Nv, Q[:, kk], fn_)
            Nv /= np.maximum(np.linalg.norm(Nv, axis=1), 1e-12)[:, None]
            t = Y[NB0] - Y; t -= (t * Nv).sum(1)[:, None] * Nv; t /= np.maximum(np.linalg.norm(t, axis=1), 1e-12)[:, None]; b = np.cross(Nv, t); return t, b, Nv
        S0 = smooth(V0, CFG['dm_iters']); t0, b0, n0 = frames(S0); dl = V0 - S0; loc = np.c_[(dl * t0).sum(1), (dl * b0).sum(1), (dl * n0).sum(1)]
        Sx = smooth(X0, CFG['dm_iters']); t1, b1, n1 = frames(Sx); Xdm = Sx + loc[:, :1] * t1 + loc[:, 1:2] * b1 + loc[:, 2:] * n1
        Xb[sv] = X0[sv] + tau[sv][:, None] * (Xdm[sv] - X0[sv])
    MnB = np.zeros((nV, 3)); np.add.at(MnB, E[:, 0], Xb[E[:, 1]]); np.add.at(MnB, E[:, 1], Xb[E[:, 0]]); bL = (Xb - MnB / deg[:, None])[sv].copy()
    for k, v in enumerate(sv):
        if ext[k]: bL[k] += X0[ext[k]].sum(0) / deg[v]
    # bisector plane of the posed joint angle (through the posed pivot): rays to the shoulder and to the wrist from the elbow
    Mp, _ = rig.pose_mats(KP); pe = bl_to_src(Mp['forearm_' + S][:3, 3][None])[0]; psh = bl_to_src(Mp['upperarm_' + S][:3, 3][None])[0]
    pw = bl_to_src(Mp['hand_' + S][:3, 3][None])[0]; ra = (psh - pe) / np.linalg.norm(psh - pe); rb = (pw - pe) / np.linalg.norm(pw - pe)
    PN_ = (ra - rb) / np.linalg.norm(ra - rb); PC = pe                                # + side = upper-arm side
    q_ = V0[sv] - e; s_ax = q_ @ AX; rad_ = q_ - np.outer(s_ax, AX); cth_ = (rad_ @ ANT) / np.maximum(np.linalg.norm(rad_, axis=1), 1e-9)
    PLM = (d[sv] >= CFG.get('plane_min_rest_cm', 6.0)) & (cth_ > CFG.get('plane_inner_cos', 0.2)); PHOLD = np.full((n, 3), np.nan); FAIRV = set()
    X = Xb.copy(); wA = (1 - tau[sv]) * CFG['w_anchor'] + CFG.get('w_core_anchor', 1e-3); hist = []; HOLD = np.full((n, 3), np.nan)
    for it in range(CFG['iters']):
        R_ = [Lmat]; B_ = [bL]; W_ = [np.ones(n)]
        # anchors
        R_.append(sp.identity(n, format='csr')); B_.append(Xb[sv]); W_.append(wA)
        # collisions (non-local posed faces)
        Nf = NFREF; Cf = X[Q[CF]].mean(1)
        bvh = BVHTree.FromPolygons(X.tolist(), Q[CF].tolist(), all_triangles=False, epsilon=0.0); pr = np.array(bvh.overlap(bvh), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
        if len(pr):
            A_ = Q[CF[pr[:, 0]]]; B_q = Q[CF[pr[:, 1]]]; pr = pr[~(A_[:, :, None] == B_q[:, None, :]).any((1, 2))]
            sep_ = np.linalg.norm(C0f[pr[:, 0]] - C0f[pr[:, 1]], axis=1); pr = pr[(sep_ >= CFG['local_cm']) & (sep_ < CFG.get('contact_max_sep_cm', 1e9))]
        best = np.full(nV, np.inf); push = np.zeros((nV, 3))
        NP = fnorm(X, CF); PFAC = np.zeros(len(pr), bool)
        if len(pr):                                                                       # only surfaces that face each other (posed OR skinned-reference normals)
            pf = (NP[pr[:, 0]] * NP[pr[:, 1]]).sum(1) < -CFG.get('facing', 0.2); rf = (Nf[pr[:, 0]] * Nf[pr[:, 1]]).sum(1) < -CFG.get('facing', 0.2)
            keepp = pf | rf; PFAC = pf[keepp]; pr = pr[keepp]
        for (fa, fb), pfac in zip(pr if len(pr) else [], PFAC):
            NN = NP if pfac else Nf                                                     # posed normals when they already face each other
            for x_, y_ in ((fa, fb), (fb, fa)):
                vs = Q[CF[x_]]; s_ = (X[vs] - Cf[y_]) @ NN[y_]
                for v, sv_ in zip(vs, s_):
                    if sup[v] and sv_ < CFG['gap_cm'] and sv_ < best[v]: best[v] = sv_; dv_ = NN[y_] - NN[x_]; push[v] = dv_ / max(np.linalg.norm(dv_), 1e-9)   # out of the other surface, back into its own
        hitv = np.nonzero(np.isfinite(best) & sup)[0]; hit = np.zeros(n, bool); hit[idx[hitv]] = True
        col_t = np.full((n, 3), np.nan)
        if len(hitv):
            amt = np.minimum(CFG.get('push_share', 0.5) * (CFG['gap_cm'] - best[hitv]), CFG.get('max_push_cm', 0.2)); col_t[idx[hitv]] = X[hitv] + amt[:, None] * push[hitv]
        ncol = int(len(pr)); maxpen = float(max(0.0, -best[hitv].min())) if len(hitv) else 0.0
        if CFG.get('contact_mode') == 'sdf':                                         # side-vs-side signed distance (upper-arm flesh vs forearm flesh)
            Nv = np.zeros((nV, 3)); fnp = np.cross(X[Q[CF, 2]] - X[Q[CF, 0]], X[Q[CF, 3]] - X[Q[CF, 1]])
            for kk in range(4): np.add.at(Nv, Q[CF, kk], fnp)
            for _ in range(2):
                Mn_ = np.zeros_like(Nv); np.add.at(Mn_, E[:, 0], Nv[E[:, 1]]); np.add.at(Mn_, E[:, 1], Nv[E[:, 0]]); Nv = Nv + Mn_
            Nv /= np.maximum(np.linalg.norm(Nv, axis=1), 1e-12)[:, None]
            col_t = np.full((n, 3), np.nan); best = np.full(n, np.inf)
            combos = [(True, False), (False, True)] + ([(True, True), (False, False)] if CFG.get('same_side') else [])
            for A_side, B_side in combos:
                ia = np.nonzero(FSIDE[sv] == A_side)[0]; ib = np.nonzero(FSIDE[sv] == B_side)[0]; tb = cKDTree(X[sv[ib]])
                lc = CFG['local_cm'] if A_side != B_side else CFG.get('same_side_local_cm', 2.0)
                dq_, jq_ = tb.query(X[sv[ia]], k=4, distance_upper_bound=CFG['depth_cm'] + 0.5)
                for c_ in range(4):
                    okk = np.isfinite(dq_[:, c_]); a_i = ia[okk]; b_i = ib[jq_[okk, c_]]
                    rs = np.linalg.norm(V0[sv[a_i]] - V0[sv[b_i]], axis=1) >= lc
                    a_i, b_i = a_i[rs], b_i[rs]; nb_ = Nv[sv[b_i]]; rel = X[sv[a_i]] - X[sv[b_i]]; sd_ = (rel * nb_).sum(1)
                    tang = np.linalg.norm(rel - sd_[:, None] * nb_, axis=1)
                    fac_ = (Nv[sv[a_i]] * nb_).sum(1) < -CFG.get('facing', 0.2)
                    inside = (sd_ < CFG['gap_cm']) & (sd_ > -CFG['depth_cm']) & (tang < CFG.get('tang_cm', 0.4)) & fac_
                    for a1, s1, n1 in zip(a_i[inside], sd_[inside], nb_[inside]):
                        if s1 < best[a1]: best[a1] = s1; col_t[a1] = X[sv[a1]] + min(CFG.get('push_share', 0.5) * (CFG['gap_cm'] - s1), CFG.get('max_push_cm', 0.2)) * n1
            hit = np.isfinite(best); maxpen = float(max(0.0, -best[hit].min())) if hit.any() else 0.0
        # persistence (ratchet): a vertex once pushed keeps a target at its current position, so resolved contacts do not snap back
        hold = np.isfinite(HOLD[:, 0]) & ~np.isfinite(col_t[:, 0]); col_t[hold] = X[sv][hold]
        HOLD = np.where(np.isfinite(col_t[:, :1]), 1.0, np.nan) * np.ones((1, 3))
        m = np.isfinite(col_t[:, 0])
        if m.any():
            ii = np.nonzero(m)[0]; R_.append(sp.csr_matrix((np.ones(len(ii)), (np.arange(len(ii)), ii)), shape=(len(ii), n))); B_.append(col_t[ii]); W_.append(np.full(len(ii), CFG['w_collision']))
        # plane contact (CONFIG.plane_contact): forearm-side vs upper-arm-side flesh beyond plane_min_rest_cm from the pivot, inner side only, is kept
        # on its own side of the posed bisector plane of the joint angle (+-gap); violators get a persistent target on the plane
        npl = 0
        if CFG.get('plane_contact') and ang in CFG.get('plane_keys', CFG['anchors'][1:]):
            sd_ = (X[sv] - PC) @ PN_; viol = PLM & (((FSIDE[sv]) & (sd_ > -CFG['gap_cm'])) | ((~FSIDE[sv]) & (sd_ < CFG['gap_cm'])))
            tgtp = X[sv] - ((sd_ + np.where(FSIDE[sv], CFG['gap_cm'], -CFG['gap_cm']))[:, None] * PN_[None])
            held = np.isfinite(PHOLD[:, 0]) & ~viol; PHOLD[held] = X[sv][held]; PHOLD[viol] = tgtp[viol]; keep = np.isfinite(PHOLD[:, 0])
            if keep.any():
                ii = np.nonzero(keep)[0]; R_.append(sp.csr_matrix((np.ones(len(ii)), (np.arange(len(ii)), ii)), shape=(len(ii), n))); B_.append(PHOLD[ii]); W_.append(np.full(len(ii), CFG.get('w_plane', CFG['w_collision'])))
            npl = int(viol.sum())
        # local-inversion fairing (CONFIG.fair): vertices of faces whose normal opposes the sum of their edge-neighbour normals (the diagnostic's
        # local fold/inversion indicator) get a persistent soft target at the mean of their neighbours
        nfair = 0
        if CFG.get('fair'):
            Nall = fnorm(X, np.arange(len(Q))); NS_ = np.zeros_like(Nall); np.add.at(NS_, EFP[:, 0], Nall[EFP[:, 1]]); np.add.at(NS_, EFP[:, 1], Nall[EFP[:, 0]])
            invf = np.nonzero(((Nall * NS_).sum(1) < 0) & ~INV0 & sup[Q].all(1))[0]
            if len(invf):
                vv_ = np.unique(Q[invf].ravel()); FAIRV.update(int(v) for v in vv_ if sup[v])
            nfair = int(len(invf))
            if FAIRV:
                fv = np.array(sorted(FAIRV)); Mn_ = np.zeros((nV, 3)); np.add.at(Mn_, E[:, 0], X[E[:, 1]]); np.add.at(Mn_, E[:, 1], X[E[:, 0]]); tgt_ = (Mn_ / deg[:, None])[fv]
                ii = idx[fv]; R_.append(sp.csr_matrix((np.ones(len(ii)), (np.arange(len(ii)), ii)), shape=(len(ii), n))); B_.append(tgt_); W_.append(np.full(len(ii), CFG.get('w_fair', 10.0)))
        # loop floor
        nl = 0
        if CFG.get('loop_floor', 0) > 0 and LP:
            rr, cc, vv, bb = [], [], [], []
            for a_, b_, r0 in LP:
                dv = X[a_] - X[b_]; L_ = np.linalg.norm(dv)
                if L_ < CFG['loop_floor'] * r0:
                    t_ = dv / max(L_, 1e-9) * CFG['loop_floor'] * r0; r = len(bb); rr += [r, r]; cc += [idx[a_], idx[b_]]; vv += [1.0, -1.0]; bb.append(t_); nl += 1
            if bb: R_.append(sp.csr_matrix((vv, (rr, cc)), shape=(len(bb), n))); B_.append(np.array(bb)); W_.append(np.full(len(bb), CFG['w_loop']))
        # edge floor
        ne_ = 0
        if CFG.get('edge_floor', 0) > 0:
            dv = X[SE[:, 0]] - X[SE[:, 1]]; L_ = np.linalg.norm(dv, axis=1); low = L_ < CFG['edge_floor'] * SE0
            if low.any():
                k_ = np.nonzero(low)[0]; t_ = dv[k_] / np.maximum(L_[k_], 1e-9)[:, None] * (CFG['edge_floor'] * SE0[k_])[:, None]
                r = np.arange(len(k_)); R_.append(sp.csr_matrix((np.r_[np.ones(len(k_)), -np.ones(len(k_))], (np.r_[r, r], np.r_[idx[SE[k_, 0]], idx[SE[k_, 1]]])), shape=(len(k_), n)))
                B_.append(t_); W_.append(np.full(len(k_), CFG['w_edge'])); ne_ = int(len(k_))
        A = sp.vstack(R_).tocsr(); Bm = np.vstack(B_); Wt = np.concatenate(W_)
        AtW = A.T.multiply(Wt[None, :]).tocsr(); Xs = spl.factorized((AtW @ A).tocsc())
        rhs = AtW @ Bm; Xn = np.c_[Xs(rhs[:, 0]), Xs(rhs[:, 1]), Xs(rhs[:, 2])]
        X = X.copy(); X[sv] = Xn; hist.append(dict(it=it, intersecting_pairs=int(ncol), pushed_vertices=int(hit.sum()), col_rest_dist_pct=[round(float(x), 1) for x in np.percentile(d[sv][hit], [5, 50, 95])] if hit.any() else [], max_pen_cm=round(float(maxpen), 4), loop_floor_active=nl, edge_floor_active=ne_, plane_violations=npl, local_inversions=nfair))
    # volume restoration (CONFIG.volume_restore = fraction of the corrective-induced closed-volume loss to give back): a smooth outward bump on the
    # medial / lateral sides of the elbow (not the inner contact patch, not the olecranon contour), scaled by the linearised closed-volume change
    if CFG.get('volume_restore', 0) > 0:
        def cvol(Y):
            T_ = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; return float(np.einsum('ij,ij->i', Y[T_[:, 0]], np.cross(Y[T_[:, 1]], Y[T_[:, 2]])).sum() / 6)
        loss = cvol(X0) - cvol(X)
        q_ = V0[sv] - e; s_ax = q_ @ AX; rad_ = q_ - np.outer(s_ax, AX); cth_v = (rad_ @ ANT) / np.maximum(np.linalg.norm(rad_, axis=1), 1e-9)
        lo_, hi_ = CFG.get('bulge_rest_cm', [3.0, 11.0]); dd_ = d[sv]
        bump = c2((dd_ - lo_) / 1.5) * (1 - c2((dd_ - (hi_ - 2.0)) / 2.0)) * c2((CFG.get('bulge_cos_max', 0.55) - cth_v) / 0.3) * c2((cth_v + CFG.get('bulge_cos_min', 0.45)) / 0.3)
        held_ = np.isfinite(PHOLD[:, 0]) if CFG.get('plane_contact') and ang in CFG.get('plane_keys', []) else np.zeros(n, bool); bump[held_] = 0
        fv_ = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]) * 0.5; av = np.zeros((nV, 3))
        for kk in range(4): np.add.at(av, Q[:, kk], fv_ / 4)
        nvv = av[sv] / np.maximum(np.linalg.norm(av[sv], axis=1), 1e-12)[:, None]; gain = (bump * (nvv * av[sv]).sum(1)).sum()
        alpha_ = CFG['volume_restore'] * loss / max(gain, 1e-9) if loss > 0 else 0.0
        X = X.copy(); X[sv] += (alpha_ * bump)[:, None] * nvv
        hist.append(dict(it='volume', loss_cm3=round(loss, 2), bump_vertices=int((bump > 1e-3).sum()), max_bump_cm=round(float(alpha_ * bump.max()), 3), after_loss_cm3=round(cvol(X0) - cvol(X), 2)))
    # final local repair (CONFIG.repair_passes): faces still flagged by the local fold/inversion indicator get their vertices and 1-ring relaxed
    rep = []
    for _ in range(CFG.get('repair_passes', 0)):
        Nall = fnorm(X, np.arange(len(Q))); NS_ = np.zeros_like(Nall); np.add.at(NS_, EFP[:, 0], Nall[EFP[:, 1]]); np.add.at(NS_, EFP[:, 1], Nall[EFP[:, 0]])
        invf = np.nonzero(((Nall * NS_).sum(1) < 0) & ~INV0 & sup[Q].all(1))[0]; rep.append(int(len(invf)))
        if not len(invf): break
        vv_ = set(np.unique(Q[invf].ravel()).tolist()); vv_ |= {w for v in list(vv_) for w in nb[v]}; vv_ = np.array([v for v in vv_ if sup[v] and gd[v] > 0])
        Mn_ = np.zeros((nV, 3)); np.add.at(Mn_, E[:, 0], X[E[:, 1]]); np.add.at(Mn_, E[:, 1], X[E[:, 0]]); X[vv_] = 0.5 * X[vv_] + 0.5 * (Mn_ / deg[:, None])[vv_]
    if rep: hist.append(dict(it='repair', local_inversions_per_pass=rep))
    Dp = (X - X0) * gd[:, None]; Dp[~sup] = 0.0                                      # posed-space correction with exact-zero guard
    Dr = np.zeros_like(V0); Dr[sv] = np.linalg.solve(Ls[sv], Dp[sv][:, :, None])[:, :, 0]    # rest-space shape-key delta
    OUT['K%d_%s' % (ang, S)] = Dr; OUT['X%d_%s' % (ang, S)] = X.astype(np.float32); OUT['L%d_%s' % (ang, S)] = X0.astype(np.float32)
    LOG['keys'][str(ang)] = dict(pose=pname, key_pose_bones=sorted(KP), iterations=hist, max_posed_delta_cm=float(np.linalg.norm(Dp, axis=1).max()),
                                 max_rest_delta_cm=float(np.linalg.norm(Dr, axis=1).max()), rest_delta_sha256=hashlib.sha256(np.ascontiguousarray(Dr.astype(np.float32)).tobytes()).hexdigest(),
                                 nonzero_vertices=int((np.linalg.norm(Dr, axis=1) > 1e-9).sum()))
    print(TAG, pname, [(h.get('intersecting_pairs'), h.get('pushed_vertices'), h.get('max_pen_cm'), h.get('plane_violations'), h.get('local_inversions_per_pass')) for h in hist][-3:], 'max posed delta %.3f cm' % LOG['keys'][str(ang)]['max_posed_delta_cm'], flush=True)
OUT['support'] = sup; OUT['tau'] = tau.astype(np.float32); OUT['guard'] = gd.astype(np.float32)
np.savez_compressed(os.path.join(O, 'corr_%s.npz' % TAG), **OUT)
LOG['support_ids_sha256'] = hashlib.sha256(np.ascontiguousarray(sv.astype(np.int32)).tobytes()).hexdigest()
json.dump(LOG, open(os.path.join(O, 'corr_%s_log.json' % TAG), 'w'), indent=1, default=float)
