# sa6_fit.py CFG OUT.json : fit the RP6 corrective families for one configuration (c1 = M, c2 = F) over the gated pose set:
#   the 34-pose RP5 suite with anatomical sagittal signs ('anat') + the RP5-literal sagittal variants ('_rp5lit', the exact RP5 signs) except the literal
#   jaw closure (jaw_open_20_rp5lit = +20 deg closes the closed mouth into the upper rostrum: CONTACT/SETUP intrusion, not a deformation pose).
#   + the special-gate poses (sa6_gates, prefixed 'gate:').  Each pose is solved at 0.25 / 0.5 / 0.75 / 1.0 of its angles (Gauss-Seidel rounds over the whole set, residual-only updates), then sa6_eval verifies 0.25/0.5/0.75/1.0.
import sys, os, json, time, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_pose as SP, sa6_correctives as CC
def pose_set(R, gates=True):
    import sa6_gates as GT
    A = R.suite('anat'); L = R.suite('rp5'); P = dict(A)
    for k, v in L.items():
        if any(e[3] != f[3] or np.abs(np.asarray(e[1], float) - np.asarray(f[1], float)).max() > 1e-9 for e, f in zip(v, A[k])):
            if k != 'jaw_open_20': P[k + '_rp5lit'] = v
    if gates: P.update({'gate:' + k: v for k, v in GT.gate_poses(R).items()})
    return P
def entries(R, spec, T):
    """unique driving (bone, axis) per pose: per bone the entry with the largest |angle|; driver value measured from T"""
    best = {}
    for b, piv, ax, deg in spec:
        if b not in best or abs(deg) > abs(best[b][2]): best[b] = (piv, ax, deg)
    out = []
    for b, (piv, ax, deg) in best.items():
        f = dict(bone=b, axis=np.asarray(ax, float) / np.linalg.norm(ax)); x = CC.Correctives(R).driver(T, f) if False else None
        out.append((b, np.asarray(piv, float), np.asarray(ax, float) / np.linalg.norm(ax)))
    return out
VOL_TOL = 20.0     # cm3: target of the volume-preservation corrective (|dV| <= VOL_TOL / 4 after the fix)
VOL_ACCEPT = 60.0  # cm3: the volume path's result is accepted when the closed-body |dV| <= VOL_ACCEPT (audit gate = 100 cm3 per pose)
NONREAL = ('tail_root_lateral_30_rp5lit', 'tail_root_vertical_25_rp5lit', 'tail_twist_30_rp5lit')
LOC_RING = int(os.environ.get('LOC_RING', 8))
CONTACT_RING = int(os.environ.get('CONTACT_RING', 10))
VOL_TRIG = 60.0    # cm3: |dV| above which the volume corrective is (re)solved (hysteresis: fold / contact fixes may lose a little volume afterwards)
VOL_BONES = {'clavicle', 'upperarm', 'forearm', 'hand', 'thigh', 'shin', 'foot', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'neck_01', 'neck_02'} | {'tail_%02d' % k for k in range(1, 17)}
#   tissue-volume joints only: the jaw opens a cavity (the closed mesh volume legitimately changes), digits are below the volume tolerance
PEN_TOL = 0.02     # cm: a vertex interpenetrates when the point PEN_TOL INSIDE its own surface also lies inside another part of the body (generalised winding
                   # number > 1.5) -> penetration depth >= 0.2 mm; shallower overlaps count as touching contact.  Vertices already in that state at rest excluded.
def wn_out(P, F): return igl.fast_winding_number(P, F, P - PEN_TOL * igl.per_vertex_normals(P, F))
def penetration(R, P, F, w0): return (wn_out(P, F) > 1.5) & (w0 < 1.5)
def solve_one(R, C, S, spec, F, w0, log, pose_key=None):
    T = R.pose(spec); d = C.delta(T); Pc = R.skin(T, R.V + d); fl = np.nonzero(R.relcos(Pc, T) < 0)[0]
    vol_pose = any(e[0] in VOL_BONES or e[0].rsplit('_', 1)[0] in VOL_BONES for e in spec)
    pen = penetration(R, Pc, F, w0); dV = (S.body_volume(Pc) - S.V0) if vol_pose else 0.0
    ntear = int(S.tear_edges(Pc)[0].sum()) + int(abs(dV) > VOL_TRIG)       # a volume miss also counts as an open defect (convergence = a fully clean round)
    if not len(fl) and not pen.any() and abs(dV) <= VOL_TRIG and not ntear: return 0, 0, 0
    Pc0 = Pc
    pen0 = int(pen.sum())
    ent = entries(R, spec, T)
    # LOCALITY (RP6 v002): this pose's corrective may move only (a) the blend zone of its driving joints (vertices weighted both inside and outside the
    # driving bone's subtree) dilated LOC_RING quad rings, (a2) the flesh of the two segments the joint connects (dominant bone = the driving bone or
    # its parent), and (b) contact sites (vertices interpenetrating at the incoming state or the DQS start)
    # dilated 4 rings.  Everything else is pinned for this solve (added to the protected set) -> no anatomy drift far from the joint.
    bz = np.zeros(R.nv, bool)
    for b_, _, _ in ent:
        ws_ = R.W[:, [R.bi[x] for x in R.sub(b_) if x in R.bi]].sum(1); bz |= (ws_ > 1e-3) & (ws_ < 1 - 1e-3)
    dom = np.array(R.DB)[R.W.argmax(1)]; seg = np.zeros(R.nv, bool)
    for b_, _, _ in ent:
        seg |= np.isin(dom, [b_] + ([R.par[b_]] if R.par[b_] in R.bi else []))                   # flesh of the two segments the joint connects
        if b_.startswith('thigh'): seg |= dom == 'tail_01'          # caudofemoral coupling: hip motion deforms the tail-root segment (tail_01 only)
    allowed = S.dilate(bz, LOC_RING) | seg | S.dilate(pen | penetration(R, R.dqs(T, R.V + d), F, w0) | S.tear_verts(Pc), CONTACT_RING)   # contact and tear sites (local defects)
    base_protect = S.protect; S.protect = base_protect | ~allowed
    try:
        return _solve_rest(R, C, S, spec, F, w0, T, d, Pc, Pc, fl, pen, dV, vol_pose, ntear, ent, pose_key)
    finally:
        S.protect = base_protect
def _solve_rest(R, C, S, spec, F, w0, T, d, Pc, Pc0, fl, pen, dV, vol_pose, ntear, ent, pose_key):
    pen0 = int(pen.sum())
    hinge = len(ent) == 1 and R.par[ent[0][0]] is not None
    # (ring, contact plane, unfold rounds, pin rigid): local + rigid parts pinned first; rigid vertices are released only when the pinned variants fail
    CASC = [(3, False, 40, True), (6, False, 40, True), (12, False, 40, True), (6, True, 40, True), (12, True, 80, True),
            (6, False, 40, False), (12, False, 80, False), (12, True, 80, False), (24, False, 80, False), (24, True, 80, False)]
    def cascade(P0):
        """LOCAL fold / contact cascade from the start shape P0: first variant that ends fold- and penetration-free wins, else the fewest folds + pen."""
        f0 = np.nonzero(R.relcos(P0, T) < 0)[0]; p0 = penetration(R, P0, F, w0)
        if not len(f0) and not p0.any() and not S.tear_edges(P0)[0].any(): return ((0, 0.0), P0, np.zeros(0, int), 0)
        casc = sorted(CASC, key=lambda c_: (not c_[3], not c_[1])) if (p0.any() and hinge) else CASC   # contact poses: hinge contact plane first
        best = None
        for ring, plane, rounds, pin in casc:
            if plane and not hinge: continue
            S.pin = pin; Ps, I, M = S.solve(T, P0, f0, iters=1, ring=ring, spread_tol=1e-4, local=True, seed=p0); ncont = 0
            if plane and penetration(R, Ps, F, w0).any(): Ps, ncont = S.contact_plane(T, Ps, ent[0][0], ent[0][1])
            Ps, f2 = S.unfold(T, Ps, R.relcos, rounds=rounds, pin_rigid=pin)
            for _ in range(4 if (p0.any() or plane) else 0):     # general contact (any remaining interpenetration), then re-relax
                pq = penetration(R, Ps, F, w0)
                if not pq.any(): break
                Ps, n_ = S.contact_general(Ps, pq); ncont += n_; Ps, f2 = S.unfold(T, Ps, R.relcos, rounds=rounds, pin_rigid=pin)
            for _ in range(3):                                # tension tears (weight seams / contact projection): seeded local ARAP, then re-check contact
                if not S.tear_edges(Ps)[0].any(): break
                Ps = S.tear_fix(T, Ps, R.relcos, ring=ring if ring >= 12 else 12)
                pq = penetration(R, Ps, F, w0)
                if pq.any(): Ps, n_ = S.contact_general(Ps, pq); ncont += n_; Ps, _ = S.unfold(T, Ps, R.relcos, rounds=rounds, pin_rigid=pin)
            f2 = np.nonzero(R.relcos(Ps, T) < 0)[0]
            npen = int(penetration(R, Ps, F, w0).sum()); nt = int(S.tear_edges(Ps)[0].sum()); score = (len(f2) + npen + nt, float(np.abs(Ps - P0).sum()))
            if best is None or score < best[0]: best = (score, Ps, f2, ncont)
            if score[0] == 0: break
        return best
    def polish(Ps):
        """volume polish on a clean result: up to 3 cycles of broad self-masking bulge -> (small tear fix if the bulge tore an edge) -> unfold;
        a cycle is kept only when it stays fold- / penetration-free with no more tear edges; else the line-searched concentrated volume_fix."""
        def bad(P_):
            m = np.zeros(R.nv, bool); m[R.Q[R.relcos(P_, T) < 0].ravel()] = True; return m | penetration(R, P_, F, w0) | S.tear_verts(P_)
        def clean(P_, ref): return not (R.relcos(P_, T) < 0).any() and not penetration(R, P_, F, w0).any() and S.tear_edges(P_)[0].sum() <= S.tear_edges(ref)[0].sum()
        fails = 0
        for k in range(14):
            if abs(S.body_volume(Ps) - S.V0) <= VOL_TOL: return Ps
            ct, sm = ((0.85, 150), (0.7, 300), (0.55, 500), (0.45, 500), (0.35, 800), (0.25, 800))[min(fails, 5)]      # escalate: allow the bulge closer to the crease, broader field
            # PARTIAL BROAD BULGE (RP6 v003): the unmasked broad bulge scaled back along its own direction -- a clean partial restore that reaches the
            # acceptance band beats a fully restored but spiky self-masked field (masking concentrates the field near the crease)
            hit = None; pmask = np.zeros(R.nv, bool)
            for kk in range(8):                    # self-masked partial bulge: mask the vertices the full trial made bad, then scale back to the largest clean step
                Pb = S.bulge(T, Ps, S.V0, smooth=sm, crease_thr=ct, exclude=pmask)
                for s_ in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4):
                    Pt = Ps + s_ * (Pb - Ps)
                    if clean(Pt, Ps) and abs(S.body_volume(Pt) - S.V0) < abs(S.body_volume(Ps) - S.V0) - 2.0: hit = Pt; break
                if hit is not None: break
                pmask |= S.dilate(bad(Pb) & ~bad(Ps), 1)
            if hit is not None:
                if os.environ.get('PDEBUG'): print('   polish partial bulge s=%.1f dV %.0f -> %.0f' % (s_, S.body_volume(Ps) - S.V0, S.body_volume(hit) - S.V0), flush=True)
                Ps = hit; continue
            Pv, nb = S.bulge_safe(T, Ps, S.V0, bad, smooth=sm, crease_thr=ct)
            if S.tear_edges(Pv)[0].sum() > S.tear_edges(Ps)[0].sum(): Pv = S.tear_fix(T, Pv, R.relcos, ring=6, iters=2)
            if nb or (R.relcos(Pv, T) < 0).any(): Pv, _ = S.unfold(T, Pv, R.relcos)
            if os.environ.get('PDEBUG'): print('   polish cycle: nb', nb, 'flips', int((R.relcos(Pv, T) < 0).sum()), 'pen', int(penetration(R, Pv, F, w0).sum()), 'tears', int(S.tear_edges(Pv)[0].sum()), 'vs', int(S.tear_edges(Ps)[0].sum()), 'dV %.0f -> %.0f' % (S.body_volume(Ps) - S.V0, S.body_volume(Pv) - S.V0), flush=True)
            if clean(Pv, Ps) and abs(S.body_volume(Pv) - S.V0) < abs(S.body_volume(Ps) - S.V0) - 2.0: Ps = Pv
            else:
                fails += 1
                if fails > 5: break
        if abs(S.body_volume(Ps) - S.V0) <= VOL_TOL: return Ps
        Pv, _ = S.volume_fix(T, Ps, S.V0, tol=VOL_TOL / 4)
        for sc in (1.0, 0.75, 0.5, 0.25):
            Pt = Ps + sc * (Pv - Ps)
            if clean(Pt, Ps): return Pt
        return Ps
    def finish(c_):
        sc_, Ps, f2, ncont = c_
        if vol_pose and sc_[0] == 0: Ps = polish(Ps)
        return ((sc_[0], max(0.0, abs(S.body_volume(Ps) - S.V0) - VOL_ACCEPT) if vol_pose else 0.0, sc_[1]), Ps, f2, ncont)
    out = [finish(cascade(Pc))]
    if vol_pose and out[0][0][:2] != (0, 0.0) and abs(dV) > VOL_TRIG / 3 and os.environ.get('VOLPATH', '1') == '1':
        # RP6 v002 VOLUME START (only when the LBS start misses the clean + volume target): DQS of (rest + current correctives) + broad
        # crease-avoiding bulge -> the same local cascade from there
        out.append(finish(cascade(S.bulge(T, R.dqs(T, R.V + d), S.V0))))
    _, Ps, f2, ncont = min(out, key=lambda o: o[0])
    Ps = Ps.copy(); Ps[S.protect] = Pc0[S.protect]          # hard guard: protected vertices carry no corrective
    Pc = Pc0                                             # the stored corrective = everything relative to the incoming state
    dmask = np.linalg.norm(Ps - Pc, axis=1) > 1e-7; I = np.nonzero(dmask)[0]
    Wb = R.W; Rb = np.stack([T[b][0] for b in R.DB]); M = np.einsum('vb,bij->vij', Wb[I], Rb)
    dd = np.linalg.solve(M, (Ps[I] - Pc[I])[:, :, None])[:, :, 0]
    # assign each corrected vertex to a driving joint: the most distal driving bone whose subtree carries weight (> 0.05) at the vertex (the joint whose motion
    # deforms it); vertices weighted by no driving subtree -> the nearest driving pivot (rest space)
    piv = np.stack([e[1] for e in ent]); own = np.linalg.norm(R.V[I][:, None] - piv[None], axis=2).argmin(1)
    depth = lambda b: 0 if R.par[b] is None else 1 + depth(R.par[b])
    for j in sorted(range(len(ent)), key=lambda j: depth(ent[j][0])):          # proximal first, distal overwrites
        sw = R.W[I][:, [R.bi[b] for b in R.sub(ent[j][0]) if b in R.bi]].sum(1); own[sw > 0.05] = j
    if pose_key:                                         # Gauss-Seidel conflict: residual -> a pose key driven by the joints that deform these vertices (<= 3)
        sc = []
        for j, (b, pv, ax) in enumerate(ent):
            key, axf = C.resolve(b, ax); x = C.driver(T, dict(bone=b, axis=axf))
            if abs(x) < 0.5: continue
            sw = R.W[I][:, [R.bi[bb] for bb in R.sub(b) if bb in R.bi]].sum(1); sc.append(((sw * np.linalg.norm(dd, axis=1)).sum(), b, axf, x))
        sc = sorted(sc, key=lambda t: -t[0])[:3]
        if sc: C.add_pose_key(pose_key, [(b, a, x) for _, b, a, x in sc], I, dd); return len(fl) + pen0 + ntear, len(f2), ncont
    for j, (b, pv, ax) in enumerate(ent):
        m = own == j
        if not m.any(): continue
        key, axf = C.resolve(b, ax); x = C.driver(T, dict(bone=b, axis=axf))
        if abs(x) < 0.5: continue
        C.add(key, b, axf, pv, x, I[m], dd[m])
    return len(fl) + pen0 + ntear, len(f2), ncont         # folds + interpenetrating vertices + tear edges entering the solve
if __name__ == '__main__':
    cfg, out = sys.argv[1:3]; wf = sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/rp6/W_%s.npz' % cfg
    R = SP.Rig(cfg, wf); C = CC.Correctives.load(R, os.environ['INIT']) if os.environ.get('INIT') else CC.Correctives(R); S = CC.Solver(R); S.V0 = S.body_volume(R.V); PS = pose_set(R)
    for f in C.F.values():                                 # protected vertices never carry a corrective (also strips older fits)
        f['D'] = [(i_[~S.protect[i_]], d_[~S.protect[i_]]) for i_, d_ in f['D']]
    for pk in C.PK.values(): k_ = ~S.protect[pk['idx']]; pk['idx'] = pk['idx'][k_]; pk['d'] = pk['d'][k_]
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = wn_out(R.V, F)
    # literal-RP5 tail-root poses pivot 9-10 cm off the tail_01 joint: not producible by bone rotation (same driver angle as the realisable pose,
    # different shape -> no corrective can serve both).  Fitted set = realisable poses only; the literal ones stay in sa6_eval as diagnostics.
    PS = {k: v for k, v in PS.items() if k not in NONREAL}
    if os.environ.get('POSE_SUBSTR'): PS = {k: v for k, v in PS.items() if any(x in k for x in os.environ['POSE_SUBSTR'].split(','))}
    order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k])))
    log = []
    for rnd in range(int(os.environ.get('ROUNDS', 3))):
        tot = 0
        for ip, pn in enumerate(order):
            if ip and ip % 8 == 0: C.save(out, dict(status='RP6 RIG PILOT / NOT FROZEN (partial: round %d pose %d)' % (rnd, ip), config=cfg, weights=os.path.basename(wf), fit_log=log))
            for fr in (1.0, 0.5, 0.75, 0.25):           # full and half first; quarter fractions only get their own sample if interpolation leaves a fold
                spec = [(b, p, a, d * fr) for b, p, a, d in PS[pn]]; t = time.time()
                pk = ('%s@%.2f' % (pn, fr)) if (rnd >= int(os.environ.get('PK_ROUND', 2)) or '%s@%.2f' % (pn, fr) in C.PK) else None   # stubborn after the first rounds
                a, b, c = solve_one(R, C, S, spec, F, w0, log, pose_key=pk); tot += a
                if a or b: print('round %d %-30s x%.2f flips+pen before %4d after-solve %4d contact %4d  %.1fs' % (rnd, pn, fr, a, b, c, time.time() - t), flush=True)
                log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=b, contact_projected=c))
        print('round', rnd, 'total flips entering', tot, flush=True)
        C.save(out, dict(status='RP6 RIG PILOT / NOT FROZEN (partial: after round %d)' % rnd, config=cfg, weights=os.path.basename(wf), fit_log=log))
        if tot == 0: break
    C.save(out, dict(status='RP6 RIG PILOT / NOT FROZEN', config=cfg, weights=os.path.basename(wf), method=open(CC.__file__).read().split('import')[0], fit_log=log))
