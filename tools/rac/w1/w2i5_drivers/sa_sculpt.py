# RAC W2I5 localized medial / posterior thigh relief finish (order §2-§4) on the accepted W2I4 candidate. COPIES ONLY until the §12
# conditions pass. Only the fine (1.5 cm high-pass) surface relief of the medial / posterior thigh changes, plus the narrow blend into the
# accepted W2I4 anterior / lateral sector; every measurement-bearing vertex is held and the 62-body fold guard runs against W2I4.
#
# Why W2I4 failed there and what changes: W2I4 sampled the native relief from the frozen surface point vertically offset in 3-D from each
# vertex's own frozen position; on faces that turn toward the other leg / pouch that point is off-surface and its nearest surface vertex is on
# a different meridian (pits, tears). W2I5 instead WALKS ON THE FROZEN SURFACE: from each vertex's own frozen position it steps along the
# local vertical tangent of the frozen thigh surface (re-projected onto the tangent plane of the nearest same-side vertex each step) until the
# source height is reached, so the source stays on the vertex's own meridian on every face orientation. Native vertical scale comes from the
# same two anchors as W2I4 (knee transition 63 cm, hip crease 86 cm + 9.2), cross-faded through mid-thigh (amplitude-normalized).
# The copied relief is band-passed (0.45-1.5 cm Gaussian): sharp sub-0.45 cm content - including the inherited Rodin tear / speckle patch on
# the frozen medial thigh - is neither copied nor kept, so the sculpted sector is re-formed at muscle / tendon scale only.
# The W2I5 delta is computed once on the male centre at 188 (reference frame) and carried, like the W2I4 delta, before the stature route.
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers')); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers'))
import sa_finish as FN
RB = FN.RB; B = FN.B; C = FN.C; L = FN.L; V0 = FN.V0; F0 = FN.F0; ss = FN.ss; H0 = B.H0
OUTD = C.S + '/w2i5'
LO, HI, G = FN.THIGH_LO, FN.THIGH_HI, RB.TARGET['G']; TOP = HI + G
RELIEF_R = 1.5; FINE_R = 0.45
ITERS = int(os.environ.get('ITERS', 0))   # 0 = the evaluated W2I5 candidate; >0 tested (diverges, spikes; see report); XF_C = float(os.environ.get('XF_C', 0.5)); XF_W = float(os.environ.get('XF_W', 0.30))   # cross-fade centre / width in thigh fraction
def sectors(idx):
    """W2I4 anterolateral weight (exactly as applied in W2I4), the medial offset and the crotch-wall mask, per thigh vertex"""
    P0 = V0.astype(float); al = np.zeros(len(idx)); dxm = np.zeros(len(idx))
    for sd in (1, -1):
        ms = L.side[idx] == sd; A0 = P0[idx][ms]
        cx = np.polyfit(A0[:, 2], np.abs(A0[:, 0]), 2); cf = np.polyfit(A0[:, 2], A0[:, 1], 2)
        ox = np.abs(A0[:, 0]) - np.polyval(cx, A0[:, 2]); of = A0[:, 1] - np.polyval(cf, A0[:, 2])
        al[ms] = (ox + of) / np.sqrt(2) / (np.hypot(ox, of) + 1e-9); dxm[ms] = -ox
    return al, dxm
def walk(P0, N0, side, start, target_u, step=0.3, iters=80):
    """surface walk on the frozen thigh from `start` (vertex indices) to heights target_u along the local vertical tangent"""
    out = np.zeros((len(start), 3)); ok = np.zeros(len(start), bool)
    for sd in (1, -1):
        pool = np.where((L.side == sd) & (L.leg > 0.15) & (P0[:, 2] > 40) & (P0[:, 2] < 104) & (L.tail < 0.05))[0]; tr = cKDTree(P0[pool])
        ms = np.where(side == sd)[0]; p = P0[start[ms]].copy(); tu = target_u[ms]
        for _ in range(iters):
            j = pool[tr.query(p)[1]]; n = N0[j]
            t = np.array([0, 0, 1.0]) - n * n[:, 2:3]; tz = np.maximum(t[:, 2], 0.25); t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-12
            rem = tu - p[:, 2]
            if np.abs(rem).max() < 0.02: break
            dz = np.clip(rem, -step, step); d = np.clip(dz / np.maximum(t[:, 2], 0.25), -2 * step, 2 * step)
            p = p + t * d[:, None]; j = pool[tr.query(p)[1]]; p = p - (np.einsum('ij,ij->i', p - P0[j], N0[j]))[:, None] * N0[j]
        out[ms] = p; ok[ms] = (np.abs(tu - p[:, 2]) < 0.3) & (L.leg[pool[tr.query(p)[1]]] > 0.3)
    return out, ok
def sculpt_delta(P4):
    P0 = V0.astype(float); u0 = P0[:, 2]
    idx = np.where((L.leg > 0.3) & (u0 > 54) & (u0 < 96) & (L.tail < 0.05))[0]
    N0 = FN.normals(P0); N4 = FN.normals(P4)
    S0 = FN.gsmooth(P0, idx, RELIEF_R); s0 = FN.gsmooth(P0, idx, FINE_R)
    r0 = np.zeros(len(P0)); r0[idx] = np.einsum('ij,ij->i', s0 - S0, N0[idx])   # BAND-PASS native relief (FINE_R..RELIEF_R): muscle / tendon
                                                                                 # scale only; the sharp sub-0.5 cm content of the frozen thigh
                                                                                 # (Rodin tear / speckle defects on the medial thigh) is not copied
    S4 = FN.gsmooth(P4, idx, RELIEF_R); s4 = FN.gsmooth(P4, idx, FINE_R)
    r4 = np.einsum('ij,ij->i', P4[idx] - S4, N4[idx]); r4bp = np.einsum('ij,ij->i', s4 - S4, N4[idx]); r4f = np.einsum('ij,ij->i', P4[idx] - s4, N4[idx])
    ur = P4[idx, 2]; t = np.clip((ur - LO) / (TOP - LO), 0, 1); wt = ss((t - XF_C + XF_W / 2) / XF_W)   # anchor cross-fade (see XF_*)
    side = L.side[idx]; qb, okb = walk(P0, N0, side, idx, ur); qt, okt = walk(P0, N0, side, idx, ur - G)
    tr = cKDTree(P0[idx])
    def samp(Q):
        dd, j = tr.query(Q, k=4); w = 1 / (dd + 0.03) ** 2; return (r0[idx][j] * w).sum(1) / w.sum(1)
    rb = samp(qb); rt = samp(qt)
    # source-defect mask: the frozen medial thigh carries a few inherited Rodin tear / speckle patches whose roughness (local mean |sub-FINE_R
    # relief|) is far above the thigh's own; band-passed samples landing in them are faded out instead of re-copied
    rf0 = np.abs(np.einsum('ij,ij->i', P0[idx] - s0, N0[idx])); nb = tr.query_ball_point(P0[idx], r=1.0)
    rough = np.array([rf0[l].mean() for l in nb]); thr = np.percentile(rough, 95); thr_hi = np.percentile(rough, 99)
    def sdef(Q):
        dd, j = tr.query(Q, k=4); w = 1 / (dd + 0.03) ** 2; rr = (rough[j] * w).sum(1) / w.sum(1); return 1 - ss((rr - thr) / (thr_hi - thr))
    wb0 = (1 - wt) * okb; wt0 = wt * okt; wb = wb0 * sdef(qb); wtt = wt0 * sdef(qt)
    A_, deg_ = FN.adjacency()
    for _ in range(25):                                                      # smooth the anchor weights (walk failures / defect fades)
        for wv in (wb, wtt, wb0, wt0):
            z = np.zeros(len(P0)); z[idx] = wv; z = 0.5 * z + 0.5 * (A_ @ z) / deg_; wv[:] = z[idx]
    nrm = np.sqrt(wb0 ** 2 + wt0 ** 2)                                       # amplitude normalization by the UN-faded weights: a defect fade
    out = np.where(nrm > 1e-6, (wb * rb + wtt * rt) / np.maximum(nrm, 1e-6), 0.0)   # lowers the copied relief instead of being renormalized away
    al, dxm = sectors(idx)
    m5 = (1 - ss((al - 0.35) / 0.25))                                           # W2I5 sector: medial / posterior + the whole W2I4 sector
                                                                                # transition (W2I4 w4 < 1 up to al 0.35), fading out by al 0.6
    m5 *= ss((ur - (LO - 3)) / 4.0) * ss(((TOP + 2) - ur) / 4.0) * ss((L.leg[idx] - 0.5) / 0.3)
    m5 *= 1 - ss((dxm - 3.0) / 2.0) * ss((u0[idx] - 84.0) / 3.0)               # true crotch / pouch wall untouched
    m5 *= (okb | okt)
    hold = FN.meas_hold() | (L.tail > 0.05)
    for i in B.ST.values(): hold[i] = True
    # direct re-form (no iteration): in the sculpt sector the sharp sub-FINE_R content is removed (smoothing; erases the inherited tear /
    # speckle marks) and the FINE_R..RELIEF_R band is replaced by the native band-pass relief walked from the frozen thigh
    # soft weights: every mask is diffused over the mesh so no weight steps (rectangular edges) and no single held vertex (dimples / dots)
    # can print into the surface; held vertices keep exactly zero displacement, their neighbourhood tapers to it over ~1 cm
    A, deg = FN.adjacency()
    def diffuse(f, n):
        for _ in range(n): f = 0.5 * f + 0.5 * (A @ f) / deg
        return f
    full = lambda v: (lambda z: (z.__setitem__(idx, v), z)[1])(np.zeros(len(P0)))
    m5s = diffuse(full(m5), 25)[idx]
    hw = diffuse(hold.astype(float), 12); fac = np.clip(1 - 4 * hw, 0, 1); fac[hold] = 0
    # defect repair inside the blend: where the sculpt reaches the W2I4 sector (0 < m5 < 1) any inherited Rodin tear / speckle patch of the
    # current surface (local sub-FINE_R roughness above the thigh's 97th percentile) is smoothed out, so the blend cannot half-erase a tear
    tr4 = cKDTree(P4[idx]); nb4 = tr4.query_ball_point(P4[idx], r=0.8); af = np.abs(r4f); rough4 = np.array([af[l].mean() for l in nb4])
    thr4 = np.percentile(rough4, 97); dm_all = np.clip(2 * diffuse(full(ss((rough4 - thr4) / thr4)), 10)[idx], 0, 1); dm = dm_all * ss(m5s / 0.2)
    # inside the sculpt sector a torn patch of the current surface gets no copied relief either (smooth muscle surface there)
    corr = np.zeros(len(P0)); corr[idx] = (m5s * ((out * (1 - dm_all) - r4bp) - r4f) + (1 - m5s) * dm * (-r4f - 0.7 * r4bp)) * fac[idx]
    # iterate (as W2I4) so the RE-MEASURED 1.5 cm relief of the sculpted sector equals the native target (the Gaussian split otherwise leaks
    # the stretched 1.5-3 cm band of the W2I3 form back into the measured relief)
    tgt = out * (1 - dm_all)
    for _ in range(ITERS):
        Pk = P4 + corr[:, None] * N4; Sk = FN.gsmooth(Pk, idx, RELIEF_R); rk = np.einsum('ij,ij->i', Pk[idx] - Sk, FN.normals(Pk)[idx])
        corr[idx] += m5s * (tgt - rk) * fac[idx]
    target = (1 - m5) * r4 + m5 * out
    DBG.update(idx=idx, m5s=m5s, fac=fac[idx], out=out, r4bp=r4bp, r4f=r4f, dm_all=dm_all, wb=wb, wtt=wtt, rb=rb, rt=rt, al=al)
    info = dict(n_vertices=int(len(idx)), sculpt_vertices=int((m5 > 1e-3).sum()), walk_ok_bottom=float(okb.mean()), walk_ok_top=float(okt.mean()),
                relief_rms_frozen=float(np.sqrt((r0[idx] ** 2).mean())), relief_rms_W2I4=float(np.sqrt((r4 ** 2).mean())), relief_rms_target=float(np.sqrt((target ** 2).mean())))
    return corr[:, None] * N4, info
DBG = {}
_D5 = None
def build_s(p, h=None):
    """W2I5 final: W2I4 build_f route with the W2I5 sculpt delta added before the accepted regional stature route"""
    global _D5
    if _D5 is None: _D5 = final_delta()[0]
    if FN._DF is None: FN._DF = FN.finish_delta()[0]
    P, q = C.build(dict(p)); info = {}
    import sa_joints as SJ
    J, _ = SJ.transport(P, RB.JW); P, info['fa'] = RB.fa_rebuild(P, J, RB.TARGET['fa_delta'])
    P, q, info['leg'] = RB.leg_rebuild(P, q, RB.TARGET['G'], RB.TARGET['FT'])
    P = P + FN._DF + _D5
    h = H0 if h is None else h; P2, q2, k = B.at_stature(P, q, h)
    return P2, q2, k, info
def smooth_face_normals(P, A, deg, iters=10):
    """per-face normals of the locally smoothed surface (vertex normals averaged over ~iters rings)"""
    N = FN.normals(P)
    for _ in range(iters): N = 0.5 * N + 0.5 * (A @ N) / deg[:, None]
    return (N[F0[:, 0]] + N[F0[:, 1]] + N[F0[:, 2]]).astype(np.float32)
def fold_guard(D5, max_rounds=12):
    """attenuate the W2I5 delta locally (smooth x0.5 field) wherever, in any of the 62 bodies, a face would be
       (a) flipped against its W2I4 build WITHOUT turning toward the locally smoothed W2I4 surface (a genuinely new flip), or
       (b) a new fold - pointing against the locally smoothed W2I4 surface where W2I4 was not folded.
       Faces of inherited Rodin tears / W2I4 transfer marks that the sculpt turns back toward the smoothed surface (and that end up unfolded)
       are REPAIRS: counted and reported separately, never as new flips."""
    global _D5
    import sa_w2i2_build as WB
    A, deg = FN.adjacency(); nr = lambda Q: np.cross(Q[F0[:, 1]] - Q[F0[:, 0]], Q[F0[:, 2]] - Q[F0[:, 0]]).astype(np.float32)
    refs = {}
    for bid, p, h, note in WB.ALL:
        P4 = FN.build_f(p, h)[0]; n4 = nr(P4); ns = smooth_face_normals(P4, A, deg); refs[bid] = (n4, ns, np.einsum('ij,ij->i', n4, ns) < 0)
    log = []
    for rnd in range(max_rounds):
        _D5 = D5; vb = np.zeros(len(V0)); tot = 0; per = {}; rep = 0
        for bid, p, h, note in WB.ALL:
            n4, ns, fold4 = refs[bid]; nP = nr(build_s(p, h)[0])
            flip4 = np.einsum('ij,ij->i', n4, nP) < 0; foldP = np.einsum('ij,ij->i', ns, nP) < 0
            cos = lambda a, b: np.einsum('ij,ij->i', a, b) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + 1e-20)
            repair = flip4 & ~foldP & (cos(nP, ns) > cos(n4, ns))          # the face turns TOWARD the smoothed surface: a torn / folded W2I4
            bad = (flip4 & ~repair) | (foldP & ~fold4); rep += int(repair.sum())   # face being repaired, not a new flip
            n = int(bad.sum()); tot += n; vb[np.unique(F0[bad])] = 1
            if n: per[bid] = n
        log.append(dict(total=tot, bodies=per, repaired_W2I4_folds=rep)); print('W2I5 fold guard round', rnd, tot, 'repaired W2I4 folds', rep, flush=True)
        if tot == 0: break
        vb = np.minimum(1, vb + A @ vb); vb = np.minimum(1, vb + A @ vb); a = 1 - 0.5 * vb
        for _ in range(6): a = np.minimum(a, 0.5 * a + 0.5 * (A @ a) / deg)
        D5 = D5 * a[:, None]
    _D5 = None
    return D5, log
def final_delta():
    fn = OUTD + '/sculpt_delta.npz'
    if os.path.exists(fn): z = np.load(fn); return z['D'], json.loads(str(z['info']))
    os.makedirs(OUTD, exist_ok=True)
    FN._DF = FN.finish_delta()[0]; P4 = FN.build_f({})[0]
    D5, info = sculpt_delta(P4)
    if os.environ.get('NO_GUARD') != '1': D5, info['fold_guard'] = fold_guard(D5)
    info['max_delta_cm'] = float(np.linalg.norm(D5, axis=1).max())
    np.savez_compressed(fn, D=D5.astype(np.float64), info=json.dumps(info)); return D5, info
