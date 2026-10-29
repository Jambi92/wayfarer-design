# ear_build.py HEAD CAND OUTDIR [--canon canon.json] [--write-canon] [--probe key=val,...]
# Order bdcd6a6: realise the shared Fenn ear branch on one accepted CF2 head (HEAD = FNL4-CF2 | FNF181-CF2) for one candidate (E1 / E2 / E3).
# Order 0d9c70b: topology v002 by default (ear_branch_lib.TOPO_VERSION); v002 adds the cuff quality chain (pre-smoothing, protected untangling with
# capped lowering, 3-D quality pass with root-crease / contact / clearance / deformation guards, aspect repair). EAR_TOPO=v001 reproduces v001.
# Every vertex outside the two branch zones keeps its v005 index order and its exact CF2 family-realization position; the 2 x 1,181 v005
# ear-zone interior vertices and 2 x 1,206 ear-zone faces are replaced by the branch patch (same patch topology for every head / candidate).
# Writes OUTDIR/<HEAD>_<CAND>_branch.npz (V, Q, M weight/zone proxy map, src_index, meta, branch map) and a JSON record.
import sys, os, json, pickle, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
from scipy.spatial import cKDTree
a = sys.argv[1:]; HEAD, CAND, OUT = a[:3]; os.makedirs(OUT, exist_ok=True)
CANON = a[a.index('--canon') + 1] if '--canon' in a else None; WRITE = '--write-canon' in a
PROBE = dict(kv.split('=') for kv in a[a.index('--probe') + 1].split(',')) if '--probe' in a else {}
RT = os.environ.get('EAR_CF', '/tmp/claude-0/rt/fn/cf')                            # CF2 source / family workspace (final consolidation: clean rebuild folder)
fz = np.load('%s/fam/%s_fam.npz' % (RT, HEAD)); Q0 = np.asarray(fz['Q']); V0 = fz['V'].astype(float); si = fz['src_index']
M0 = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape']))
r6p = '/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % HEAD; z6 = np.load(r6p); we = M0 @ z6['w_ears'][si].astype(float)
p = dict(E.CAND[CAND]); geo = dict(E.GEO); geo.update(p.pop('geo', {}))   # candidate-level geometry overrides (Vael: concha clearance); none for Fenn / Aelari
Q3_KW = dict(lo=55.0, hi=125.0, ks=50.0, kn=4000.0, kt=20000.0, rho=0.5, iters=int(os.environ.get('EAR_Q3_IT', '600')), amax=6.0, ka=float(os.environ.get('EAR_Q3_KA', '1000')), kd=float(os.environ.get('EAR_Q3_KD', '0')), kr=float(os.environ.get('EAR_Q3_KR', '500')), th_cap=float(os.environ.get('EAR_Q3_THCAP', '64')))
Q3_WARM = os.environ.get('EAR_Q3_WARM', '0') == '1'
for k, v in PROBE.items():                          # geometry-only readiness probes (same topology)
    if k in geo: geo[k] = float(v)
    elif k == 'taper_ex': p['taper'] = tuple(p['taper'][:2]) + (float(v),) + tuple(p['taper'][3:])   # (Halvren 4-tuple law keeps its shoulder)
    elif k == 'taper_sh': p['taper'] = tuple(p['taper'][:3]) + (float(v),)
    elif k == 'taper_st': p['taper'] = (p['taper'][0], float(v)) + tuple(p['taper'][2:])                 # Halvren order: taper start
    elif k in ('place_db', 'place_du', 'phi0', 'tauA', 'd_r', 'lift_lobe', 'lift_top', 'sulcus_h', 'sulcus_r', 'root_lower', 'root_lower_cap', 'root_lower_cap_inf',
               'root_lower_smooth', 'root_lower_ring', 'root_lower_fall', 'root_lower_fall_own', 'fair_rings'): geo[k] = float(v)       # Halvren geometry controls (inert unless set)
    else: p[k] = float(v)
# Halvren HR2 ROOT-RING LOWERING (root visual integration order; geo 'root_lower' >= 0, inert otherwise -- every frozen ear is unchanged): the v005 ear-zone
# root loop is the base of the MPFB human auricle and stands up to 0.55 cm (posterior) / 1.1 cm (inferior, the old human lobe base) above the surrounding head,
# so the auricle and its skin-hugging cuff sat on a raised plateau whose rim (the root loop) read as a second, pedestal-shaped contour with a lower tab beside
# the lobe. The head surface is extrapolated over the ear zone from the skin 3+ rings outside the loop (thin-plate, <= 5 cm, smoothing root_lower_smooth --
# a stiff fit, 1e-3, overshoots into a false bump below the ear); every root-loop vertex is lowered along the root normal toward it + root_lower cm, capped at
# root_lower_cap x head scale (root_lower_cap_inf on the inferior third of the loop = the lobe base), loop-smoothed. Outside the loop either the transition ring
# follows by root_lower_ring, or (root_lower_fall > 0) every head-skin vertex within root_lower_fall x head scale cm follows by (nearest loop drop) x
# (1 - smooth(d / fall)), never below the head fit (root_lower_fall_own). The ear frame stays the unlowered one; the auricle is then seated on the lowered head
# (skull field re-fitted), i.e. it sits on the head instead of on the pedestal. Topology unchanged.
RLW = float(geo.get('root_lower', -1.0)); rl_rec = {}; rl_frame = {}   # root frame kept from the UNLOWERED loop (ear orientation unchanged)
if RLW >= 0:
    from scipy.interpolate import RBFInterpolator
    adj_ = {}
    for q in Q0:
        for k in range(4): adj_.setdefault(int(q[k]), set()).update((int(q[(k + 1) % 4]), int(q[(k - 1) % 4])))
    for side_, sg_ in (('l', 1), ('r', -1)):
        rd0 = E.root_data(V0, Q0, we, sg_); rl_frame[side_] = {k_: rd0[k_].copy() for k_ in ('O', 'n', 'b', 'u')}; zone0 = set(np.unique(Q0[rd0['faces']]).tolist()); L0 = rd0['loop']
        r1 = {w for v in L0 for w in adj_[int(v)] if w not in zone0}; r2 = {w for v in r1 for w in adj_[v] if w not in zone0 and w not in r1}
        d0 = V0 - rd0['O']; cand = np.nonzero((np.linalg.norm(d0, axis=1) < 5.0) & (sg_ * V0[:, 0] > 0) & ((d0 @ rd0['n']) > -2.5))[0]
        out = np.array([v for v in cand if v not in zone0 and v not in r1 and v not in r2])
        bu0 = lambda X: np.c_[(X - rd0['O']) @ rd0['b'], (X - rd0['O']) @ rd0['u']]
        head_ = RBFInterpolator(bu0(V0[out]), (V0[out] - rd0['O']) @ rd0['n'], kernel='thin_plate_spline', smoothing=float(geo.get('root_lower_smooth', 1e-3)))
        cap_ = float(geo.get('root_lower_cap', 9.0)) * E.head_scale(r6p)[1]; Lg = np.asarray(L0); hL = (V0[Lg] - rd0['O']) @ rd0['n'] - head_(bu0(V0[Lg]))
        uL_ = bu0(V0[Lg])[:, 1]; s_ = (uL_.mean() - uL_) / max(uL_.mean() - uL_.min(), 1e-6); w_inf = E.smooth(np.clip((s_ - 0.3) / 0.5, 0, 1))   # inferior third of the loop
        cap_ = cap_ + (float(geo.get('root_lower_cap_inf', geo.get('root_lower_cap', 9.0))) * E.head_scale(r6p)[1] - cap_) * w_inf                 # (lobe base) may drop further
        dL = np.minimum(np.maximum(hL - RLW, 0), cap_)
        dL = 0.5 * dL + 0.25 * (np.roll(dL, 1) + np.roll(dL, -1))                       # loop-smoothed drop (no step along the loop)
        R1 = np.array(sorted(r1)); iL = cKDTree(V0[Lg]).query(V0[R1])[1]; dR = float(geo.get('root_lower_ring', 0.5)) * dL[iL]   # transition ring follows partly
        RF = float(geo.get('root_lower_fall', 0.0))       # smooth radial fall-off instead of the ring fraction
        if RF > 0:
            Rr = np.array([v for v in np.nonzero(np.linalg.norm(V0 - rd0['O'], axis=1) < 6.0)[0] if v not in zone0 and sg_ * V0[v, 0] > 0])   # without a step
            dd_, ii_ = cKDTree(V0[Lg]).query(V0[Rr]); wf_ = 1 - E.smooth(np.clip(dd_ / (RF * E.head_scale(r6p)[1]), 0, 1)); R1, dR = Rr, dL[ii_] * wf_
            if geo.get('root_lower_fall_own', 0) > 0:   # never sink a skin vertex below the head fit: drop <= its own excess height (no trough beside the loop)
                dR = np.minimum(dR, np.maximum((V0[Rr] - rd0['O']) @ rd0['n'] - head_(bu0(V0[Rr])) - RLW, 0))
        for grp, drop, h_ in ((Lg, dL, hL), (R1, dR, (V0[R1] - rd0['O']) @ rd0['n'] - head_(bu0(V0[R1])))):
            if not len(drop) or not drop.max() > 0: continue
            V0[grp] -= drop[:, None] * rd0['n']
            rl_rec.setdefault(side_, []).append(dict(n=int(len(grp)), height_before_mean_cm=float(h_.mean()), height_before_max_cm=float(h_.max()), max_drop_cm=float(drop.max())))
HH, sc = E.head_scale(r6p)
Lo = E.canonical_layout()                            # canonical layout (deterministic; E2 metric)
canon = json.load(open(CANON)) if CANON and os.path.exists(CANON) else {}
removed = []; patches = {}; recs = {}
for side, sg in (('l', 1), ('r', -1)):
    rd = E.root_data(V0, Q0, we, sg); rd['V_loop'] = V0[rd['loop']]
    if side in rl_frame: rd.update(rl_frame[side])
    skull, sk_v = E.skull_field(V0, Q0, rd, sg)
    rd['skull'] = skull
    R = E.realize(Lo, rd, skull, p, sc, canon=canon.get(side), geo=geo)
    canon[side] = R['rec']['canon']
    P, F, base = E.patch_mesh(Lo, R, rd['loop'])
    patches[side] = (P, F, rd, R); removed += rd['interior'].tolist(); recs[side] = R['rec']
    recs[side]['root_loop_v005'] = rd['loop'].tolist(); recs[side]['frame'] = dict(O=rd['O'].tolist(), n=rd['n'].tolist(), b=rd['b'].tolist(), u=rd['u'].tolist())
if WRITE and CANON: json.dump(canon, open(CANON, 'w'), indent=1)
# ---- assemble
rem = np.zeros(len(V0), bool); rem[removed] = True
efaces = np.zeros(len(Q0), bool)
for side in patches: efaces[patches[side][2]['faces']] = True
keep = np.nonzero(~rem)[0]; v2b = -np.ones(len(V0), int); v2b[keep] = np.arange(len(keep))
side_off = {}; Vb = [V0[keep]]; Qb = [v2b[Q0[~efaces]]]; nxt = len(keep); new_rows = []; part = ['v005'] * len(keep); side_of = [''] * len(keep)
for side in ('l', 'r'):
    P, F, rd, R = patches[side]; off = nxt; L = rd['loop']; side_off[side] = off
    Fg = np.where(F < 0, v2b[L[np.clip(-1 - F, 0, None)]], F + off); Vb.append(P); Qb.append(Fg); nxt += len(P)
    part += [str(x) for x in Lo['part']] + ['cuff'] * (len(P) - len(Lo['part'])); side_of += [side] * len(P)
Vb = np.concatenate(Vb); Qb = np.concatenate(Qb); assert (Qb >= 0).all()
# ---- orientation: v005 faces fixed; propagate to branch faces through shared edges
nk = int((~efaces).sum()); fixed = np.zeros(len(Qb), bool); fixed[:nk] = True
ed = {}
for fi, q in enumerate(Qb):
    for k in range(4): ed.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi)
from collections import deque
done = fixed.copy(); seed = sorted({f for fs in ed.values() if len(fs) == 2 and fixed[fs[0]] != fixed[fs[1]] for f in fs if fixed[f]}); dq = deque(seed)
def dirs(q): return {(q[k], q[(k + 1) % 4]) for k in range(4)}
while dq:
    f = dq.popleft(); df = dirs(Qb[f])
    for k in range(4):
        e = (min(Qb[f][k], Qb[f][(k + 1) % 4]), max(Qb[f][k], Qb[f][(k + 1) % 4]))
        for g in ed[e]:
            if done[g]: continue
            if dirs(Qb[g]) & df: Qb[g] = Qb[g][::-1]
            done[g] = True; dq.append(g)
assert done.all(), (~done).sum()
# ---- fairing (order §5 / §12): biharmonic (uniform umbrella) solve for the new skull skin inside the root (cuff) and the ONE bounded v005
# transition ring outside the root (v005 vertices sharing a face with the root loop). Root loop, the rest of v005 and the ear sheet are fixed.
FAIR = os.environ.get('EAR_FAIR', '1') == '1'; part_a = np.array(part, dtype='<U12'); trans = set()
# Halvren HR2 POSTAURICULAR SULCUS (root visual integration order; geo 'sulcus_h' >= 0, inert otherwise -- every frozen ear is unchanged): the junction ring
# behind / above / below the auricle (J on the back sheet and rim) stood 0.4-0.9 cm above the hidden-ear skull, so the cuff band climbing to it formed a raised
# second contour (posterior flange) and, at the lobe, a raised tab beside the free lobe (lower fork). The back / rim sheet near that junction is lowered along
# the root normal toward the skull: drop = (h_J - sulcus_h) x (1 - smooth(d / sulcus_r)), d = distance to the nearest non-front junction vertex; the front
# sheet, the anterior (front) attachment and the whole free auricle away from the root are untouched, so the auricle roots into the head in one fold.
SUL = float(geo.get('sulcus_h', -1.0)); sul_rec = {}
if SUL >= 0:
    for side in ('l', 'r'):
        P_, F_, rd_, R_ = patches[side]; off_ = side_off[side]; O_, b_, u_, n_ = rd_['O'], rd_['b'], rd_['u'], rd_['n']
        hgt_ = lambda X: (X - O_) @ n_ - rd_['skull'](np.c_[(X - O_) @ b_, (X - O_) @ u_])
        Jv_ = off_ + np.asarray(Lo['J']); Jb_ = Jv_[part_a[Jv_] != 'front']; sheet_ = off_ + np.nonzero(np.isin(Lo['part'][:len(Lo['st'])], ['back', 'rim']))[0]
        hJ_ = hgt_(Vb[Jb_]); d_, i_ = cKDTree(Vb[Jb_]).query(Vb[sheet_]); w_s = 1 - E.smooth(d_ / (float(geo.get('sulcus_r', 0.9)) * sc))
        drop_ = w_s * np.maximum(hJ_[i_] - SUL, 0); Vb[sheet_] -= drop_[:, None] * n_
        sul_rec[side] = dict(junction_back_height_before_cm=dict(mean=float(hJ_.mean()), max=float(hJ_.max())), moved_vertices=int((drop_ > 1e-4).sum()), max_drop_cm=float(drop_.max()))
for side in ('l', 'r'):
    rd_ = patches[side][2]; zone_ = set(np.unique(Q0[rd_['faces']]).tolist())
    for fi in np.nonzero(np.isin(Q0, rd_['loop']).any(1) & ~efaces)[0]:
        for v in Q0[fi]:
            if int(v) not in zone_: trans.add(int(v2b[v]))
trans = np.array(sorted(trans)); fair_rec = dict(transition_ring_vertices=int(len(trans)))
# Vael root integration (RI2 / RI3; geo 'cuff_skin_r', inert without it -- Fenn / Aelari): skin-hugging cuff. A target is built for every cuff vertex:
# its planar annulus position (cuff_build3, root-plane coordinates) at the skin height (hidden-ear skull field + the root-loop residual), rising to the
# junction ring J only within a smooth fillet of max(CSR x head scale, cuff_skin_slope x junction height) cm. The cuff + transition ring are then
# faired with the same biharmonic operator plus a data term pulling the cuff to that target (weight cuff_skin_w), so the root keeps biharmonic
# continuity with the skin while the raised cuff perimeter disappears. The pull fades to 0 at the root loop (cuff_skin_root x head scale cm).
CSR = float(geo.get('cuff_skin_r', 0.0))
TGT = None
if CSR > 0 and FAIR:
    fair_rec['cuff_skin'] = {}; TGT = Vb.copy(); TW = np.zeros(len(Vb))
    for side in ('l', 'r'):
        P_, F_, rd_, R_ = patches[side]; off_ = side_off[side]; O_, b_, u_, n_ = rd_['O'], rd_['b'], rd_['u'], rd_['n']
        bu_ = lambda X: np.c_[(X - O_) @ b_, (X - O_) @ u_]
        Lv = v2b[rd_['loop']]; buL = bu_(Vb[Lv]); rL = (Vb[Lv] - O_) @ n_ - rd_['skull'](buL); tL_ = cKDTree(buL)
        def skin(B_):                                           # skull field corrected by the inverse-distance root-loop residual
            dl_, il_ = tL_.query(B_, k=4); wl_ = 1 / np.maximum(dl_, 1e-3) ** 2; return rd_['skull'](B_) + (rL[il_] * wl_).sum(1) / wl_.sum(1)
        Jv = off_ + np.asarray(Lo['J']); cv = np.nonzero((part_a == 'cuff') & (np.array(side_of) == side))[0]
        buJ = bu_(Vb[Jv]); hJ = (Vb[Jv] - O_) @ n_ - skin(buJ); buC = bu_(Vb[cv])
        dC = np.abs(E._inside_dist(buJ, buC))                   # unsigned: the projected J ring need not be a simple polygon
        dj_, ij_ = cKDTree(buJ).query(buC, k=3); wj_ = 1 / np.maximum(dj_, 1e-3); hn = (hJ[ij_] * wj_).sum(1) / wj_.sum(1)
        Rf = np.maximum(CSR * sc, float(geo.get('cuff_skin_slope', 1.4)) * np.maximum(hn, 0))   # fillet widens where J stands high (slope cap)
        w_ = 1 - E.smooth(dC / Rf); hC = skin(buC) + np.maximum(hn, 0) * w_
        TGT[cv] = O_ + buC[:, :1] * b_ + buC[:, 1:] * u_ + hC[:, None] * n_
        dLr = tL_.query(buC)[0]; TW[cv] = E.smooth(dLr / (float(geo.get('cuff_skin_root', 0.45)) * sc))   # no pull at the root loop (biharmonic continuity there)
        nfJ = part_a[Jv] != 'front'; drim = cKDTree(buJ[nfJ]).query(buC)[0]                 # anterior (front-sheet) attachment only: the pull fades out
        TW[cv] *= E.smooth(drim / (float(geo.get('cuff_skin_corner', 0.6)) * sc)) * (part_a[Jv] == 'front')[cKDTree(buJ).query(buC)[1]]             # towards the rim / back junction (attachment corners c0 / c1 and
                                                                                               # the narrow postauricular band stay biharmonic)
        fair_rec['cuff_skin'][side] = dict(fillet_cm=CSR * sc, junction_height_mean_cm=float(hJ.mean()), junction_height_max_cm=float(hJ.max()), cuff_vertices=int(len(cv)), pulled_vertices=int((TW[cv] > 0.5).sum()))
# Halvren HR2 WIDE ROOT FAIRING (root visual integration order; geo 'fair_rings' > 0, inert otherwise): with the root loop FIXED the faired cuff met the head
# at a 40-55 deg crease along the loop (posterior / inferior), which drew the loop as a second contour behind and below the auricle (and a cliff where the loop
# stood above the head behind it). The root loop itself and fair_rings further v005 skin rings outside the transition ring join the biharmonic unknowns, so
# the auricle base blends into the head over a wide band (loop crease ~5 deg). The rest of v005 and the ear sheet stay fixed boundary.
FR = int(float(geo.get('fair_rings', 0))); fr_extra = np.zeros(0, int)
if FR > 0 and FAIR:
    ex_ = set()
    for side in ('l', 'r'):
        rd_ = patches[side][2]; zone_ = set(np.unique(Q0[rd_['faces']]).tolist()); adj0 = {}
        for q in Q0:
            for k in range(4): adj0.setdefault(int(q[k]), set()).update((int(q[(k + 1) % 4]), int(q[(k - 1) % 4])))
        cur = {int(v) for v in rd_['loop']}; seen = set(cur); ex_ |= cur
        for r_ in range(FR + 1):                                          # ring 1 (= transition ring) .. ring FR + 1
            cur = {w for v in cur for w in adj0[v] if w not in zone_ and w not in seen}; seen |= cur
            if r_ >= 1: ex_ |= cur
    fr_extra = np.array(sorted(int(v2b[v]) for v in ex_ if v2b[v] >= 0)); fr_extra = np.setdiff1d(fr_extra, trans); fair_rec['wide_rings'] = dict(rings=FR, extra_vertices=int(len(fr_extra)))
if FAIR:
    unk = np.r_[np.nonzero(part_a == 'cuff')[0], trans, fr_extra]
    Eg = np.unique(np.sort(np.concatenate([Qb[:, [0, 1]], Qb[:, [1, 2]], Qb[:, [2, 3]], Qb[:, [3, 0]]]), 1), axis=0); nV_ = len(Vb)
    Ag = sp.coo_matrix((np.ones(2 * len(Eg)), (np.r_[Eg[:, 0], Eg[:, 1]], np.r_[Eg[:, 1], Eg[:, 0]])), shape=(nV_, nV_)).tocsr()
    dg = np.asarray(Ag.sum(1)).ravel(); Lg = sp.identity(nV_) - sp.diags(1 / dg) @ Ag; B2 = (Lg.T @ Lg).tocsr()
    isU = np.zeros(nV_, bool); isU[unk] = True; kn = np.nonzero(~isU)[0]
    from scipy.sparse.linalg import spsolve
    rhs = -(B2[unk][:, kn] @ Vb[kn]); X0_ = Vb[trans].copy()
    if TGT is None: Vb[unk] = np.stack([spsolve(B2[unk][:, unk].tocsc(), rhs[:, k]) for k in range(3)], 1)
    else:
        lam = float(geo.get('cuff_skin_w', 0.2)); dw = (part_a[unk] == 'cuff').astype(float) * lam * TW[unk]; Au = (B2[unk][:, unk] + sp.diags(dw)).tocsc()
        Vb[unk] = np.stack([spsolve(Au, rhs[:, k] + dw * TGT[unk, k]) for k in range(3)], 1); fair_rec['cuff_skin']['data_weight'] = lam
    dt = np.linalg.norm(Vb[trans] - X0_, axis=1)
    fair_rec.update(transition_ring_displacement_cm=dict(mean=float(dt.mean()), p95=float(np.percentile(dt, 95)), max=float(dt.max())), unknowns=int(len(unk)))
part_a[trans] = 'transition'; part = list(part_a)
# ---- cuff quad relaxation on the faired surface: tangential angle-based + Laplacian smoothing, re-projected onto the faired cuff
if os.environ.get('EAR_RELAX', '1') == '1':
    cuffv = np.nonzero(np.isin(part_a, ['cuff', 'transition']))[0]; cf_ = np.nonzero(np.isin(part_a, ['cuff', 'transition'])[Qb].any(1))[0]
    g_ = np.linspace(0, 1, 9); Sm = []
    for q in Qb[cf_]:
        P_ = Vb[q]; Sm.append(((1 - g_[:, None, None]) * (1 - g_[None, :, None]) * P_[0] + g_[:, None, None] * (1 - g_[None, :, None]) * P_[1]
                               + g_[:, None, None] * g_[None, :, None] * P_[2] + (1 - g_[:, None, None]) * g_[None, :, None] * P_[3]).reshape(-1, 3))
    Sm = np.concatenate(Sm); tS_ = cKDTree(Sm)
    nb_ = [set() for _ in range(len(Vb))]
    for q in Qb[cf_]:
        for k in range(4): nb_[q[k]].update({int(q[(k + 1) % 4]), int(q[(k - 1) % 4])})
    for it_ in range(int(os.environ.get('EAR_RELAX_IT', '25'))):
        Vn = Vb.copy()
        for v in cuffv:
            ns_ = np.array(sorted(nb_[v])); P_ = Vb[ns_]; c_ = P_.mean(0); nrm = np.linalg.svd(P_ - c_)[2][2]
            d_ = P_ - Vb[v]; d_ -= np.outer(d_ @ nrm, nrm); e1 = d_[0] / (np.linalg.norm(d_[0]) + 1e-12); e2 = np.cross(nrm, e1)
            o_ = np.argsort(np.arctan2(d_ @ e2, d_ @ e1)); P_ = P_[o_]; m_ = len(P_); cand = []
            for j in range(m_):
                pj = P_[j]; a1 = P_[(j - 1) % m_] - pj; a2 = P_[(j + 1) % m_] - pj; vv = Vb[v] - pj; Lv = np.linalg.norm(vv)
                bis = a1 / (np.linalg.norm(a1) + 1e-12) + a2 / (np.linalg.norm(a2) + 1e-12)
                if np.linalg.norm(bis) < 1e-9: cand.append(Vb[v]); continue
                bis /= np.linalg.norm(bis); bis = bis if bis @ vv >= 0 else -bis; cand.append(pj + Lv * bis)
            Vn[v] = 0.5 * Vb[v] + 0.5 * (0.5 * np.mean(cand, 0) + 0.5 * c_)
        _, ii = tS_.query(Vn[cuffv]); Vn[cuffv] = Sm[ii]; Vb = Vn
# ---- local untangling (bpy BVH): cuff / transition vertices of self-intersecting branch faces (+2 rings) are relaxed towards their
# neighbours and lowered towards the skull side until no pair touching the branch remains (bounded rounds; logged)
try:
    import bpy  # noqa: F401
    from mathutils.bvhtree import BVHTree
    HAVE_BVH = True
except Exception:
    HAVE_BVH = False
movable = np.isin(part_a, ['cuff', 'transition']); brv = part_a != 'v005'
for side in ('l', 'r'):                                         # the rim-end cross sections of the junction ring may also relax
    P_, F_, rd_, R_ = patches[side]; off_ = side_off[side]
    for row in (Lo['rim'][0], Lo['rim'][-1]):
        for v in row[1:-1]: movable[off_ + v] = True
    if E.TOPO_VERSION == 'v001':                                 # v001 only: attachment corners c0 / c1 and their junction neighbours relax too
        Jl = list(Lo['J'])
        for k_ in ('c0', 'c1'):
            i_ = Jl.index(Lo['info']['corners'][k_])
            for d_ in (-1, 0, 1): movable[off_ + Jl[(i_ + d_) % len(Jl)]] = True
near = np.zeros(len(Vb), bool)
for side in ('l', 'r'):
    c_ = Vb[np.array(side_of) == side].mean(0); near |= np.linalg.norm(Vb - c_, axis=1) < 9
cuff_f = np.nonzero(np.isin(part_a, ['cuff', 'transition'])[Qb].any(1))[0]; Fsel = np.nonzero(near[Qb].all(1))[0]; tri = np.r_[Qb[Fsel][:, [0, 1, 2]], Qb[Fsel][:, [0, 2, 3]]]; qid = np.r_[Fsel, Fsel]
nbrs = [[] for _ in range(len(Vb))]
for q in Qb:
    for k in range(4): nbrs[q[k]] += [q[(k + 1) % 4], q[(k - 1) % 4]]
nbrs = [np.unique(x) for x in nbrs]; nrm_side = {side: patches[side][2]['n'] for side in ('l', 'r')}
def selfx(Vc):
    bvh = BVHTree.FromPolygons(Vc.tolist(), tri.tolist(), all_triangles=True, epsilon=0.0); bad = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = qid[i], qid[j]
        if fi != fj and not (set(Qb[fi]) & set(Qb[fj])) and (brv[Qb[fi]].any() or brv[Qb[fj]].any()): bad.add((min(fi, fj), max(fi, fj)))
    return bad
LOWER_CAP = float(os.environ.get('EAR_LOWER_CAP', '0.2')); lowered = np.zeros(len(Vb))
def untangle(Vc, unt, asp_lim=7.0, rounds=80):
    v2 = E.TOPO_VERSION != 'v001'; hist = []
    for rnd in range(rounds):
        bad = selfx(Vc)
        cfq = Qb[cuff_f]; Lq = np.linalg.norm(Vc[cfq] - Vc[np.roll(cfq, -1, 1)], axis=2); hi = cuff_f[Lq.max(1) / np.maximum(Lq.min(1), 1e-9) > asp_lim]
        unt['pairs'].append(len(bad)); unt.setdefault('aspect_gt7', []).append(int(len(hi)))
        if not bad and not len(hi): break
        if v2 and not bad:                                        # v002: aspect-only rounds stop once the count no longer improves (10 rounds)
            hist.append(len(hi))
            if len(hist) > 10 and min(hist[-10:]) >= min(hist[:-10]): break
        vs = set(); vc = set()
        for a_, b_ in bad: vc.update(Qb[a_].tolist()); vc.update(Qb[b_].tolist())
        vs |= vc
        for f_ in hi: vs.update(Qb[f_].tolist())
        for _ in range(3 if rnd < 20 else 5):
            vs.update(int(w) for v in list(vs) for w in nbrs[v]); vc.update(int(w) for v in list(vc) for w in nbrs[v])
        vs = np.array([v for v in vs if movable[v]])
        Vn = Vc.copy()
        for v in vs: Vn[v] = 0.85 * Vc[v] + 0.15 * Vc[nbrs[v]].mean(0)
        Vc = Vn
        for v in vs:                                              # lower slightly towards the head (along the side's root normal); v002: cumulative
            step = 0.02 if part_a[v] == 'cuff' else 0.005             # lowering per vertex capped (LOWER_CAP cm; contacts are never capped)
            if v2 and v not in vc:
                if lowered[v] + step > LOWER_CAP: continue
            sd = side_of[v] if v < len(side_of) and side_of[v] else ('l' if Vc[v, 0] > 0 else 'r'); Vc[v] -= step * nrm_side[sd]; lowered[v] += step
        unt['rounds'] += 1
    return Vc
unt = dict(rounds=0, pairs=[]); q3_rec = []
if E.TOPO_VERSION != 'v001':                                    # v002 root guard: cuff rings 1-2 (next to the root loop) never move in the untangling,
    rl0 = np.zeros(len(Vb), bool)                                 # whose lowering step otherwise creases the root (order 0d9c70b §13)
    for side in ('l', 'r'): rl0[v2b[patches[side][2]['loop']]] = True
    near_root = np.zeros(len(Vb), bool); cur = rl0.copy()
    for _ in range(2):
        nxt_ = np.zeros(len(Vb), bool); nxt_[Qb[cur[Qb].any(1)].ravel()] = True; near_root |= nxt_ & np.isin(part_a, ['cuff']); cur = nxt_
    movable &= ~near_root & (part_a != 'transition')
unt = dict(rounds=0, pairs=[])
if HAVE_BVH and os.environ.get('EAR_UNTANGLE', '1') == '1':
    if E.TOPO_VERSION == 'v001': Vb = untangle(Vb, unt)
    else:
        # v002: tangential pre-smoothing of the cuff away from the root (rings >= 3), re-projected onto the faired skin (fine sampling), then the
        # untangling only for real contacts (no aspect criterion; no transition / root-ring moves)
        PS = int(geo.get('presmooth', os.environ.get('EAR_PRESMOOTH', '40')))   # candidate geo 'presmooth' (Vael skin cuff: 0 -- the planar annulus is already regular)
        ps_mask = (movable | (near_root if os.environ.get('EAR_PS_RINGS', 'all') == 'all' else False)) & (part_a == 'cuff')
        ps_v = np.nonzero(ps_mask)[0]                              # tangential only (re-projected on the faired skin): rings 1-2 may slide too
        if PS:
            cf2 = np.nonzero(np.isin(part_a, ['cuff', 'transition'])[Qb].any(1))[0]; g2 = np.linspace(0, 1, 17); S2 = []
            for q in Qb[cf2]:
                P_ = Vb[q]; S2.append(((1 - g2[:, None, None]) * (1 - g2[None, :, None]) * P_[0] + g2[:, None, None] * (1 - g2[None, :, None]) * P_[1]
                                       + g2[:, None, None] * g2[None, :, None] * P_[2] + (1 - g2[:, None, None]) * g2[None, :, None] * P_[3]).reshape(-1, 3))
            S2 = np.concatenate(S2); tS2 = cKDTree(S2)
            for _ in range(PS):
                Vn = Vb.copy()
                for v in ps_v: Vn[v] = 0.85 * Vb[v] + 0.15 * Vb[nbrs[v]].mean(0)
                _, ii = tS2.query(Vn[ps_v]); Vn[ps_v] = S2[ii]; Vb = Vn
            unt['presmooth_rounds'] = PS
        unt['initial_contacts'] = len(selfx(Vb)); unt['mode'] = os.environ.get('EAR_UNT_MODE', 'full')
        if unt['mode'] == 'full': Vb = untangle(Vb, unt)          # v001 criterion (contacts + cuff aspect > 7), protected rings / transition
        elif unt['initial_contacts']: Vb = untangle(Vb, unt, asp_lim=1e9)
# ---- v002 (order 0d9c70b target B): 3-D corner-angle quality pass on the cuff + transition ring (tangential, on the faired skin; root loop,
# junction ring J, ear sheet and the rest of v005 fixed; ear_quality3d.py), alternated with the untangling until no branch contact remains
if os.environ.get('EAR_Q3', '1' if E.TOPO_VERSION != 'v001' else '0') == '1':
    import ear_quality3d as Q3
    free_ = np.isin(part_a, ['cuff', 'transition']); trans_ = (part_a == 'transition').astype(float)
    # root guard: the first cuff ring (sharing a face with the root loop) keeps its faired position so the root-loop crease stays at the
    # faired / v005 level (EAR_Q3_RING1 = 'fixed' | 'stiff' | 'free')
    rl_ = np.zeros(len(Vb), bool)
    for side in ('l', 'r'): rl_[v2b[patches[side][2]['loop']]] = True
    ring1_ = np.isin(part_a, ['cuff']) & np.isin(np.arange(len(Vb)), Qb[rl_[Qb].any(1)].ravel()) & ~rl_
    R1MODE = os.environ.get('EAR_Q3_RING1', 'free')
    if R1MODE == 'fixed': free_ = free_ & ~ring1_
    elif R1MODE == 'stiff': trans_ = np.maximum(trans_, ring1_.astype(float))
    # contact guard (active set): the untangled state V_ut has no branch contact. Each cycle re-runs the quality pass from V_ut; for every
    # contact found, the free vertices of each face get a side constraint against the other face's plane (side taken at V_ut); contacts that
    # persist after 4 cycles are frozen locally (contact faces + 1 ring at V_ut). No contact-free result -> keep V_ut (logged).
    V_ut = Vb.copy(); frozen = np.zeros(len(Vb), bool); pairs_ = {}; done_ = False
    FRZ = os.environ.get('EAR_Q3_FREEZE')                         # deformation-aware guard (run_ear_v002_head.sh): faces that contacted / flipped in a
    if FRZ and os.path.exists(FRZ):                               # posed check keep their free vertices (+1 ring) at the untangled state
        ff_ = np.array(json.load(open(FRZ)), int); vs0 = set(Qb[ff_].ravel().tolist())
        for _ in range(int(os.environ.get('EAR_Q3_FREEZE_RINGS', '1'))): vs0.update(int(w) for v in list(vs0) for w in nbrs[v])
        frozen[list(vs0)] = True
        fair_rec['deform_guard_faces'] = int(len(ff_)); fair_rec['deform_guard_vertices'] = int((frozen & free_).sum())
    root_pairs_ = []                                              # root-loop edges: (outer v005 face, inner root-band face, +1) for the crease term
    if os.environ.get('EAR_Q3_ROOTCAP', '1') == '1':
        edf = {}
        for fi_, q in enumerate(Qb):
            for k in range(4): edf.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi_)
        for side in ('l', 'r'):
            L_ = v2b[patches[side][2]['loop']]
            for k in range(len(L_)):
                f2_ = edf[(min(L_[k], L_[(k + 1) % len(L_)]), max(L_[k], L_[(k + 1) % len(L_)]))]
                if len(f2_) == 2: root_pairs_.append((f2_[0], f2_[1], 1.0))
    def side_pair(v, f):
        P = V_ut[Qb[f]]; n = np.cross(P[2] - P[0], P[3] - P[1]); n /= np.linalg.norm(n) + 1e-12; d = (V_ut[v] - P.mean(0)) @ n
        return (int(v), int(f), float(np.sign(d) or 1.0), float(min(0.5 * abs(d), 0.03)))
    # clearance guard: every free cuff vertex over a nearby non-adjacent face keeps >= PROX_KEEP of its untangled clearance to that face's plane
    PROX_KEEP = float(os.environ.get('EAR_PROX_KEEP', '0.7'))
    if PROX_KEEP > 0:
        region_ = np.zeros(len(Vb), bool)
        for side in ('l', 'r'): region_ |= np.linalg.norm(Vb - Vb[np.array(side_of) == side].mean(0), axis=1) < 8
        for pr in Q3.contact_pairs(V_ut, Qb, free_, region_, r=0.6, dmax=0.45, tol=0.15, keep=PROX_KEEP): pairs_[(pr[0], pr[1])] = pr
        q3_prox = len(pairs_)
    if os.environ.get('EAR_DUMP'): np.savez(os.environ['EAR_DUMP'], V=V_ut, Q=Qb, free=free_, trans=trans_, root_pairs=np.array(root_pairs_))
    for cyc in range(10):
        Vq, rq = Q3.quality3d(V_ut, Qb, free_ & ~frozen, trans_, pairs=list(pairs_.values()), warm=(Vq if cyc and Q3_WARM else None), root_pairs=root_pairs_, **Q3_KW); bad_ = selfx(Vq) if HAVE_BVH else set()
        rq = dict(rq, cycle=cyc, contacts=len(bad_), side_pairs=len(pairs_), proximity_pairs=q3_prox if PROX_KEEP > 0 else 0, frozen=int((frozen & free_).sum())); q3_rec.append(rq if not cyc else {k: v for k, v in rq.items() if k != 'params'})
        if not bad_: Vb = Vq; done_ = True; break
        for a_, b_ in bad_:
            for fa, fb in ((a_, b_), (b_, a_)):
                for v in Qb[fa]:
                    if free_[v]: pairs_[(int(v), int(fb))] = side_pair(v, fb)
            if cyc >= 3:
                vs = set(Qb[a_].tolist()) | set(Qb[b_].tolist())
                if cyc >= 6: vs.update(int(w) for v in list(vs) for w in nbrs[v])       # widen only if contacts still persist
                frozen[list(vs)] = True
    if not done_: Vb = V_ut
fair_rec['quality3d'] = q3_rec
# ---- v002 aspect repair (hard gate: no branch quad aspect > 10): branch faces above 9.5 get tangential smoothing of their free cuff vertices
# (+1 ring; projected on the local tangent plane), accepted only if no branch contact appears
if E.TOPO_VERSION != 'v001' and HAVE_BVH:
    rep = dict(rounds=0, faces_before=0, faces_after=0)
    brf = np.nonzero((part_a[Qb] != 'v005').any(1))[0]
    def hi_asp(Vc):
        L_ = np.linalg.norm(Vc[Qb[brf]] - Vc[np.roll(Qb[brf], -1, 1)], axis=2); return brf[L_.max(1) / np.maximum(L_.min(1), 1e-9) > 9.5]
    hf = hi_asp(Vb); rep['faces_before'] = int(len(hf))
    for rr_ in range(30):
        if not len(hf): break
        vs = set(Qb[hf].ravel().tolist()); vs.update(int(w) for v in list(vs) for w in nbrs[v]); vs = np.array([v for v in vs if part_a[v] == 'cuff'])
        if not len(vs): break
        ok_ = False
        for stp in (0.5, 0.25, 0.125, 0.0625):                    # adaptive step: halve until the smoothing step makes no branch contact
            Vn = Vb.copy()
            for v in vs:
                m_ = Vb[nbrs[v]].mean(0); P_ = Vb[nbrs[v]]; c_ = P_.mean(0); nrm = np.linalg.svd(P_ - c_)[2][2]; d_ = stp * (m_ - Vb[v]); Vn[v] = Vb[v] + d_ - (d_ @ nrm) * nrm
            if not selfx(Vn): ok_ = True; break
        if not ok_:                                                # R3 fallback (only when the ring step makes contact): the faces' own cuff vertices,
            def amax_(Vc):                                         # then one vertex at a time, steps to 1/32; kept only if the worst aspect drops
                L_ = np.linalg.norm(Vc[Qb[hf]] - Vc[np.roll(Qb[hf], -1, 1)], axis=2); return (L_.max(1) / np.maximum(L_.min(1), 1e-9)).max()
            a0_ = amax_(Vb); fv = [v for v in sorted(set(Qb[hf].ravel().tolist())) if part_a[v] == 'cuff']
            for grp in [fv] + [[v] for v in fv]:
                for stp in (0.5, 0.25, 0.125, 0.0625, 0.03125):
                    Vn = Vb.copy()
                    for v in grp:
                        m_ = Vb[nbrs[v]].mean(0); P_ = Vb[nbrs[v]]; c_ = P_.mean(0); nrm = np.linalg.svd(P_ - c_)[2][2]; d_ = stp * (m_ - Vb[v]); Vn[v] = Vb[v] + d_ - (d_ @ nrm) * nrm
                    if amax_(Vn) < a0_ - 1e-6 and not selfx(Vn): ok_ = True; break
                if ok_: break
            rep['fallback_rounds'] = rep.get('fallback_rounds', 0) + int(ok_)
        if not ok_: break
        Vb = Vn; rep['rounds'] += 1; hf = hi_asp(Vb)
    rep['faces_after'] = int(len(hf)); fair_rec['aspect_repair'] = rep
fair_rec['untangle'] = unt
# ---- weight / zone proxy map: v005 rows for kept vertices; branch vertices take the row of the nearest removed v005 ear vertex (same side)
rows = [M0[keep]]
for side in ('l', 'r'):
    P, F, rd, R = patches[side]; old = rd['interior']; t = cKDTree(V0[old]); _, i = t.query(P); rows.append(M0[old[i]])
Mb = sp.vstack(rows).tocsr()
# smooth the weight proxy over the branch graph (root loop / transition rows fixed) so neighbouring branch vertices carry near-identical skinning
brm = np.array([pp not in ('v005', 'transition') for pp in part]); Eg2 = np.unique(np.sort(np.concatenate([Qb[:, [0, 1]], Qb[:, [1, 2]], Qb[:, [2, 3]], Qb[:, [3, 0]]]), 1), axis=0)
Ag2 = sp.coo_matrix((np.ones(2 * len(Eg2)), (np.r_[Eg2[:, 0], Eg2[:, 1]], np.r_[Eg2[:, 1], Eg2[:, 0]])), shape=(len(Vb), len(Vb))).tocsr()
Sg = sp.diags(1 / np.asarray(Ag2.sum(1)).ravel()) @ Ag2; Pb = sp.diags(brm.astype(float)); Pk = sp.diags((~brm).astype(float))
for _ in range(int(os.environ.get('EAR_WSMOOTH', '12'))):
    Mb = (Pk @ Mb + Pb @ (0.5 * Mb + 0.5 * (Sg @ Mb))).tocsr(); Mb.data[np.abs(Mb.data) < 1e-6] = 0; Mb.eliminate_zeros()
meta = json.loads(str(fz['meta']))
bmap = dict(v005_to_branch=v2b.astype(np.int32), removed_v005=np.nonzero(rem)[0].astype(np.int32), removed_faces_v005=np.nonzero(efaces)[0].astype(np.int32))
np.savez_compressed('%s/%s_%s_branch.npz' % (OUT, HEAD, CAND), V=Vb.astype(np.float64), Q=Qb.astype(np.int32), M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr,
                    M_shape=np.array(Mb.shape), src_index=si, hm08_Q=fz['hm08_Q'], meta=fz['meta'], part=np.array(part), side=np.array(side_of), **bmap)
rec = dict(head=HEAD, cand=CAND, params=p, geo=geo, HH_cm=HH, head_scale=sc, verts=int(len(Vb)), faces=int(len(Qb)), v005_verts=int(len(V0)), v005_faces=int(len(Q0)),
           kept_v005_verts=int(len(keep)), removed_v005_verts=int(rem.sum()), removed_v005_faces=int(efaces.sum()), patch_verts=int(len(patches['l'][0])), patch_faces=int(len(patches['l'][1])),
           sides=recs, probe=PROBE, fairing=dict(fair_rec, **({'sulcus': sul_rec} if sul_rec else {}), **({'root_lower': rl_rec} if rl_rec else {})))
json.dump(rec, open('%s/%s_%s_branch.json' % (OUT, HEAD, CAND), 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in rec.items() if k != 'sides'}, default=float)); print({s: {k: v for k, v in recs[s].items() if k not in ('root_loop_v005', 'frame')} for s in recs})
