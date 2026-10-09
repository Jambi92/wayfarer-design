# RAC W2I4 final asset finish (order §4-§9) on the accepted W2I3 L1 + F2 rebuild. COPIES ONLY (frozen SA-M / SA-F, tool chain, canon unchanged).
# Accepted proportions are NOT changed; the finish only acts on surface quality:
#  (1) DISPLACEMENT FAIRING: the rebuild displacement field (rebuild - frozen, same state) is smoothed by uniform-Laplacian iterations inside the
#      transition zones (thigh band ends, neck, shoulder cap / trapezial slope, axilla, elbow) so no edge carries a morph-band strain spike.
#      Vertices outside the zones, the axial station vertices, the caudal system (tail-labelled) and the feet are held fixed.
#  (2) THIGH RELIEF RE-MODEL: the thigh surface is split into a smooth form (Gaussian, RELIEF_R = 1.5 cm) + fine relief (iterated RELIEF_ITERS
#      times so the re-measured relief equals the target). Muscle-scale forms keep the accepted
#      longer thigh (longer muscles); the fine relief, which the rebuild had stretched x1.5 vertically, is re-sampled (from the frozen surface point vertically offset from the vertex's own frozen position) at its NATIVE vertical
#      scale from the frozen thigh, anchored at the knee transition and at the hip crease and cross-faded (amplitude-normalized) through the
#      mid-thigh, so tendon lines, separations and condylar / crease detail keep their accepted size. Inserting 9.2 cm of length means the
#      frozen mid-thigh band (~70-79 cm) is read from both anchors: inside the cross-fade it appears twice at reduced amplitude (no hard repeat).
#      Applied on the anterior / lateral thigh only: the medial / posterior thigh and the upper inner thigh (adductor origin / crotch wall)
#      keep the faired W2I3 form (the transfer produced artifacts there; W2I4 evidence); fold guards (the reference state and the guard-state
#      family) attenuate the delta smoothly wherever a face would flip.
# The finish is computed once on the male centre at 188 (the reference frame) and carried to every state / stature as a fixed per-vertex
# delta added after the accepted L1 + F2 rebuild fields (W2I3 sa_rebuild.build_r), before the accepted regional stature route.
import sys, os, json, numpy as np
from scipy import sparse
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i3_drivers'))
import sa_rebuild as RB
B = RB.B; C = RB.C; L = RB.L; V0 = RB.V0; F0 = RB.F0; vary = RB.vary; ss = vary.ss; H0 = B.H0
OUTD = C.S + '/w2i4'
def adjacency():
    E = np.vstack([F0[:, [0, 1]], F0[:, [1, 2]], F0[:, [2, 0]]]); n = len(V0)
    A = sparse.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr(); A = ((A + A.T) > 0).astype(np.float64)
    deg = np.asarray(A.sum(1)).ravel(); return A, deg
def zones():
    u0 = V0[:, 2]; ax = np.abs(V0[:, 0])
    thigh_ends = (L.leg > 0.3) & (((u0 > 59) & (u0 < 70)) | ((u0 > 78) & (u0 < 92)))
    neck = (u0 > 148) & (u0 < 174) & (L.head < 0.5)
    shoulder = (u0 > 138) & (u0 < 160) & (ax > 10)
    axilla = (u0 > 125) & (u0 < 150) & (L.arm > 0.15) & (L.arm < 0.95)
    J = SJ_base(); elbow = np.zeros(len(V0), bool)
    for nm in ('L', 'R'): elbow |= (np.linalg.norm(V0 - J['E' + nm], axis=1) < 9.0) & (L.arm > 0.3)
    z = thigh_ends | neck | shoulder | axilla | elbow
    hold = (L.tail > 0.05) | (u0 < 12) | (L.head > 0.6)
    for i in B.ST.values(): hold[i] = True
    hold |= meas_hold()
    return z & ~hold, dict(thigh_ends=thigh_ends, neck=neck, shoulder=shoulder, axilla=axilla, elbow=elbow)
def meas_hold(margin=3.0):
    """vertices that can carry an accepted torso measurement (metrics.measure: shoulder_b / thorax_w / pelvis_w = lateral extent of torso > 0.6
    vertices in base-frame bands; thorax_d = mid-line depth at u 132): the lateral-extreme torso vertices of each band (within `margin` cm of
    the band's maximum |x|) and the thorax-depth section are held, so the finish cannot move a body measurement"""
    u0 = V0[:, 2]; ax = np.abs(V0[:, 0]); tor = L.torso > 0.6; h = np.zeros(len(V0), bool)
    for a, b in ((140, 156), (118, 140), (86, 100)):
        m = tor & (u0 >= a - 1) & (u0 <= b + 1); h |= m & (ax >= ax[m].max() - margin)
    h |= tor & (np.abs(u0 - 132) < 3) & (ax < 5)
    return h
def SJ_base():
    import sa_joints as SJ; return SJ.base_joints()
def fair(Pr, P0, mask, iters=40, lam=0.5):
    A, deg = adjacency(); d = Pr - P0; dm = d.copy(); w = mask.astype(np.float64)
    for _ in range(iters):
        avg = (A @ dm) / deg[:, None]; dm = dm + lam * w[:, None] * (avg - dm)
    return P0 + dm
RELIEF_R = float(os.environ.get('RELIEF_R', 1.5)); RELIEF_ITERS = int(os.environ.get('RELIEF_ITERS', 3))   # relief / form split radius (cm)
def gsmooth(P, idx, radius=2.5):
    tree = cKDTree(P); out = np.empty((len(idx), 3))
    for k0 in range(0, len(idx), 2000):
        sl = idx[k0:k0 + 2000]; nb = tree.query_ball_point(P[sl], r=2 * radius)
        for j, (i, l) in enumerate(zip(sl, nb)):
            l = np.asarray(l); w = np.exp(-0.5 * (np.linalg.norm(P[l] - P[i], axis=1) / radius) ** 2); out[k0 + j] = (w[:, None] * P[l]).sum(0) / w.sum()
    return out
def normals(P):
    import igl; return igl.per_vertex_normals(P, F0)
THIGH_LO, THIGH_HI = 63.0, 86.0                  # frozen base-frame thigh band (knee fields .. hip crease), as W2I3 THIGH core
def thigh_remodel(Pf, info_leg, radius=None):
    """replace the stretched FINE relief of the rebuilt thigh with native-scale relief sampled from the frozen thigh (two anchors, cross-faded)"""
    radius = RELIEF_R if radius is None else radius
    u0 = V0[:, 2]; th = (L.leg > 0.3) & (u0 > 54) & (u0 < 96) & (L.tail < 0.05); idx = np.where(th)[0]
    P0 = V0.astype(float); N0 = normals(P0); Nf = normals(Pf)
    S0 = gsmooth(P0, idx, radius); r0 = np.einsum('ij,ij->i', P0[idx] - S0, N0[idx])
    Sf = gsmooth(Pf, idx, radius); rf = np.einsum('ij,ij->i', Pf[idx] - Sf, Nf[idx])
    G = RB.TARGET['G']; top_r = THIGH_HI + G                                   # rebuilt hip-crease level in the reference frame
    ur = Pf[idx, 2]; t = np.clip((ur - THIGH_LO) / (top_r - THIGH_LO), 0, 1)
    src_bot = THIGH_LO + (ur - THIGH_LO); src_top = THIGH_HI - (top_r - ur)      # native vertical scale from each anchor
    wt = ss((t - 0.35) / 0.30); out = np.zeros(len(idx))
    tree = cKDTree(P0[idx])
    def q(us):                                                               # frozen surface point vertically offset from the vertex's own frozen position
        Q = P0[idx].copy(); Q[:, 2] = us; dd, j = tree.query(Q, k=8); w = 1 / (dd + 0.1) ** 2
        return (r0[j] * w).sum(1) / w.sum(1)
    rb = q(src_bot); rt = q(src_top)
    out = ((1 - wt) * rb + wt * rt) / np.sqrt((1 - wt) ** 2 + wt ** 2)
    edge = ss((ur - (THIGH_LO - 3)) / 4.0) * ss(((top_r + 2) - ur) / 4.0) * ss((L.leg[idx] - 0.5) / 0.3)   # inside the stretched span only
    for sd in (1, -1):                                                       # upper inner thigh (adductor origin / crotch wall) keeps the faired W2I3 form:
        ms = L.side[idx] == sd; A0 = P0[idx][ms]; cx = np.polyfit(A0[:, 2], np.abs(A0[:, 0]), 2)   # its surface faces the other leg / pouch and has no
        dxm = np.polyval(cx, A0[:, 2]) - np.abs(A0[:, 0])                                          # native counterpart at the offset heights
        edge[ms] *= 1 - ss((dxm - 2.0) / 3.0) * ss((A0[:, 2] - 70.0) / 4.0)
        cf_ = np.polyfit(A0[:, 2], A0[:, 1], 2); ox = np.abs(A0[:, 0]) - np.polyval(cx, A0[:, 2]); of = A0[:, 1] - np.polyval(cf_, A0[:, 2])
        al = (ox + of) / np.sqrt(2) / (np.hypot(ox, of) + 1e-9)               # cos of the angle to the anterolateral direction about the thigh axis
        edge[ms] *= ss((al + 0.15) / 0.5)                                       # re-model on the anterior / lateral thigh only (quadriceps / ITB face);
                                                                                # the medial and posterior thigh keep the faired W2I3 form (transfer artifacts there)
    corr = np.zeros(len(V0)); corr[idx] = (out - rf) * edge
    for _ in range(RELIEF_ITERS):                                                # the Gaussian split leaks the stretched 1.5-3 cm band back into the
        Pk = Pf + corr[:, None] * Nf; Sk = gsmooth(Pk, idx, radius)              # measured relief: iterate so the re-measured relief equals the native one
        rk = np.einsum('ij,ij->i', Pk[idx] - Sk, normals(Pk)[idx]); corr[idx] += (out - rk) * edge
    A, deg = adjacency(); nr = lambda Q: np.cross(Q[F0[:, 1]] - Q[F0[:, 0]], Q[F0[:, 2]] - Q[F0[:, 0]]); n_ref = nr(Pf); n_0 = nr(V0.astype(float)); att_rounds = 0
    for att_rounds in range(30):                                                 # fold guard: attenuate the relief correction locally where a face would flip
        P = Pf + corr[:, None] * normals(Pf); nP = nr(P); bad = (np.einsum('ij,ij->i', n_ref, nP) < 0) | (np.einsum('ij,ij->i', n_0, nP) < 0)
        if not bad.any(): break
        vb = np.zeros(len(V0)); vb[np.unique(F0[bad])] = 1; vb = np.minimum(1, vb + A @ vb); vb = np.minimum(1, vb + A @ vb)
        a = 1 - 0.5 * vb
        for _ in range(6): a = np.minimum(a, 0.5 * a + 0.5 * (A @ a) / deg)           # smooth, non-increasing attenuation (no pits)
        corr *= a
    return P, dict(n_vertices=int(len(idx)), relief_radius_cm=radius, relief_rms_frozen=float(np.sqrt((r0 ** 2).mean())), relief_rms_rebuild=float(np.sqrt((rf ** 2).mean())), relief_rms_finished=float(np.sqrt((out ** 2).mean())), fold_guard_rounds=att_rounds, fold_guard_attenuated_vertices=int((np.abs(corr[idx]) < np.abs((out - rf) * edge) - 1e-12).sum()))
def fold_guard_states(Dl, max_rounds=12):
    """the finish delta is carried to every state / stature; attenuate it locally (smooth x0.5 field, 2-ring) wherever ANY body of the W2I body
    list (62 bodies: sexes, frames, compositions, statures, lower-trunk and tail cases) would get a face flipped against the W2I3 rebuild of the
    same body, or (core states) a new face flipped against the frozen body that the W2I3 rebuild did not already have"""
    global _DF
    import sa_w2i2_build as WB
    core = ('SA-M168', 'SA-F168', 'SA-M188', 'SA-F188', 'SA-M208', 'SA-F208', 'SA-M188-N', 'SA-M188-B', 'SA-F188-N', 'SA-F188-B', 'SA-M208-B')
    states = [(bid, p, h) for bid, p, h, note in WB.ALL]
    A, deg = adjacency(); nr = lambda Q: np.cross(Q[F0[:, 1]] - Q[F0[:, 0]], Q[F0[:, 2]] - Q[F0[:, 0]]).astype(np.float32); refs = {}
    for bid, p, h in states:
        b = nr(RB.build_r(p, RB.TARGET, h)[0])
        if bid in core:
            a = nr(RB.build_r(p, {}, h)[0]); refs[bid] = (b, a, np.einsum('ij,ij->i', a, b) < 0)
        else: refs[bid] = (b, None, None)
    log = []
    for rnd in range(max_rounds):
        _DF = Dl; vb = np.zeros(len(V0)); tot = 0; per = {}
        for bid, p, h in states:
            nP = nr(build_f(p, h)[0]); b, a, pre = refs[bid]; bad = np.einsum('ij,ij->i', b, nP) < 0
            if a is not None: bad |= (np.einsum('ij,ij->i', a, nP) < 0) & ~pre
            n = int(bad.sum()); tot += n; vb[np.unique(F0[bad])] = 1
            if n: per[bid] = n
        log.append(dict(total=tot, bodies=per)); print('fold guard round', rnd, tot, flush=True)
        if tot == 0: break
        vb = np.minimum(1, vb + A @ vb); vb = np.minimum(1, vb + A @ vb); a_ = 1 - 0.5 * vb
        for _ in range(6): a_ = np.minimum(a_, 0.5 * a_ + 0.5 * (A @ a_) / deg)
        Dl = Dl * a_[:, None]
    _DF = None
    return Dl, dict(states=len(states), core_states=list(core), rounds=log)
def finish_delta():
    """per-vertex finish delta in the 188 male-centre reference frame (cached)"""
    fn = OUTD + '/finish_delta.npz'
    if os.path.exists(fn): z = np.load(fn); return z['D'], json.loads(str(z['info']))
    os.makedirs(OUTD, exist_ok=True)
    Pr, q, k, info = RB.build_r({}, RB.TARGET); P0 = RB.build_r({}, {})[0]
    mask, zz = zones(); Pf = fair(Pr, P0, mask)
    Pt, tinfo = thigh_remodel(Pf, info['leg'])
    Dl = Pt - Pr; Dl, guard = fold_guard_states(Dl); inf = dict(state_fold_guard=guard, zones={k_: int(v.sum()) for k_, v in zz.items()}, faired_vertices=int(mask.sum()), thigh=tinfo, max_delta_cm=float(np.abs(Dl).max()))
    np.savez_compressed(fn, D=Dl.astype(np.float64), info=json.dumps(inf)); return Dl, inf
_DF = None
def build_f(p, h=None):
    """final asset: accepted W2I3 build_r(L1 + F2) + finish delta, then the accepted regional stature route"""
    global _DF
    if _DF is None: _DF = finish_delta()[0]
    P, q = C.build(dict(p)); info = {}
    import sa_joints as SJ
    J, _ = SJ.transport(P, RB.JW); P, info['fa'] = RB.fa_rebuild(P, J, RB.TARGET['fa_delta'])
    P, q, info['leg'] = RB.leg_rebuild(P, q, RB.TARGET['G'], RB.TARGET['FT'])
    P = P + _DF
    h = H0 if h is None else h; P2, q2, k = B.at_stature(P, q, h)
    return P2, q2, k, info
