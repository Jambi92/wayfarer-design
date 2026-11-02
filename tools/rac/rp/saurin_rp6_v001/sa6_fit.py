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
        if v != A[k] if not isinstance(v, list) else any(e[3] != f[3] for e, f in zip(v, A[k])):
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
    if not len(fl) and not pen.any() and abs(dV) <= VOL_TRIG: return 0, 0, 0
    Pc0 = Pc
    pen0 = int(pen.sum())
    ent = entries(R, spec, T); best = None
    if not len(fl) and not pen.any(): best = ((0, 0.0), Pc, np.zeros(0, int), 0)
    # solver cascade (first variant that ends fold- and penetration-free wins; else the one with the fewest folds + penetrations)
    # LOCAL first (the folds / contacts + a few rings; everything else stays exactly LBS -> no anatomy drift), widening only when needed
    hinge = len(ent) == 1 and R.par[ent[0][0]] is not None
    # (ring, contact plane, unfold rounds, pin rigid): local + rigid parts pinned first; rigid vertices are released only when the pinned variants fail
    casc = [(3, False, 40, True), (6, False, 40, True), (12, False, 40, True), (6, True, 40, True), (12, True, 80, True),
            (6, False, 40, False), (12, False, 80, False), (12, True, 80, False), (24, False, 80, False), (24, True, 80, False)]
    if pen0 and hinge: casc = sorted(casc, key=lambda c_: (not c_[3], not c_[1]))      # contact poses: hinge contact plane first (within each pin level)
    for ring, plane, rounds, pin in (casc if best is None else []):
        if plane and not (len(ent) == 1 and R.par[ent[0][0]]): continue
        S.pin = pin; Ps, I, M = S.solve(T, Pc, fl, iters=1, ring=ring, spread_tol=1e-4, local=True, seed=pen); ncont = 0
        if plane and penetration(R, Ps, F, w0).any(): Ps, ncont = S.contact_plane(T, Ps, ent[0][0], ent[0][1])
        Ps, f2 = S.unfold(T, Ps, R.relcos, rounds=rounds, pin_rigid=pin)
        for _ in range(4 if (pen0 or plane) else 0):     # general contact (any remaining interpenetration), then re-relax
            pen = penetration(R, Ps, F, w0)
            if not pen.any(): break
            Ps, n_ = S.contact_general(Ps, pen); ncont += n_; Ps, f2 = S.unfold(T, Ps, R.relcos, rounds=rounds, pin_rigid=pin)
        npen = int(penetration(R, Ps, F, w0).sum()) if (pen0 or plane or not len(f2)) else 0; score = (len(f2) + npen, float(np.abs(Ps - Pc).sum()))
        if best is None or score < best[0]: best = (score, Ps, f2, ncont)
        if score[0] == 0: break
    _, Ps, f2, ncont = best
    if vol_pose and not len(f2):                         # volume-preservation corrective LAST (blend zones only): the largest step fraction that keeps the
        dVs = S.body_volume(Ps) - S.V0                   # result fold- and penetration-free (line search 1, 3/4, 1/2, 1/4)
        if abs(dVs) > VOL_TOL:
            Pv, _ = S.volume_fix(T, Ps, S.V0, tol=VOL_TOL / 4)
            for sc in (1.0, 0.75, 0.5, 0.25):
                Pt = Ps + sc * (Pv - Ps)
                if not (R.relcos(Pt, T) < 0).any() and not penetration(R, Pt, F, w0).any(): Ps = Pt; break
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
        if sc: C.add_pose_key(pose_key, [(b, a, x) for _, b, a, x in sc], I, dd); return len(fl) + pen0, len(f2), ncont
    for j, (b, pv, ax) in enumerate(ent):
        m = own == j
        if not m.any(): continue
        key, axf = C.resolve(b, ax); x = C.driver(T, dict(bone=b, axis=axf))
        if abs(x) < 0.5: continue
        C.add(key, b, axf, pv, x, I[m], dd[m])
    return len(fl) + pen0, len(f2), ncont                 # folds + interpenetrating vertices entering the solve
if __name__ == '__main__':
    cfg, out = sys.argv[1:3]; wf = sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/rp6/W_%s.npz' % cfg
    R = SP.Rig(cfg, wf); C = CC.Correctives.load(R, os.environ['INIT']) if os.environ.get('INIT') else CC.Correctives(R); S = CC.Solver(R); S.V0 = S.body_volume(R.V); PS = pose_set(R)
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = wn_out(R.V, F)
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
