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
def penetration(R, P, F, w0):
    n = igl.per_vertex_normals(P, F); w = igl.fast_winding_number(P, F, P - 1e-3 * n); return (w > 1.5) & (w0 < 1.5)
def solve_one(R, C, S, spec, F, w0, log):
    T = R.pose(spec); d = C.delta(T); Pc = R.skin(T, R.V + d); fl = np.nonzero(R.relcos(Pc, T) < 0)[0]
    pen = penetration(R, Pc, F, w0)
    if not len(fl) and not pen.any(): return 0, 0, 0
    Ps, I, M = S.solve(T, Pc, fl, iters=1, ring=12, spread_tol=1e-4)
    ent = entries(R, spec, T); ncont = 0
    if len(ent) == 1 and R.par[ent[0][0]] and penetration(R, Ps, F, w0).any():
        Ps, ncont = S.contact_plane(T, Ps, ent[0][0], ent[0][1])
    Ps, f2 = S.unfold(T, Ps, R.relcos)
    for _ in range(6):                                   # general contact (any remaining interpenetration), then re-relax
        pen = penetration(R, Ps, F, w0)
        if not pen.any(): break
        Ps, n_ = S.contact_general(Ps, pen); ncont += n_; Ps, f2 = S.unfold(T, Ps, R.relcos)
    dmask = np.linalg.norm(Ps - Pc, axis=1) > 1e-7; I = np.nonzero(dmask)[0]
    Wb = R.W; Rb = np.stack([T[b][0] for b in R.DB]); M = np.einsum('vb,bij->vij', Wb[I], Rb)
    dd = np.linalg.solve(M, (Ps[I] - Pc[I])[:, :, None])[:, :, 0]
    # assign to the nearest driving pivot (rest space)
    piv = np.stack([e[1] for e in ent]); own = np.linalg.norm(R.V[I][:, None] - piv[None], axis=2).argmin(1)
    for j, (b, pv, ax) in enumerate(ent):
        m = own == j
        if not m.any(): continue
        f = dict(bone=b, axis=ax); x = C.driver(T, f)
        if abs(x) < 0.5: continue
        C.add(CC.fam_key(b, ax), b, ax, pv, x, I[m], dd[m])
    return len(fl), len(f2), ncont
if __name__ == '__main__':
    cfg, out = sys.argv[1:3]; wf = sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/rp6/W_%s.npz' % cfg
    R = SP.Rig(cfg, wf); C = CC.Correctives.load(R, os.environ['INIT']) if os.environ.get('INIT') else CC.Correctives(R); S = CC.Solver(R); PS = pose_set(R)
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); n0 = igl.per_vertex_normals(R.V, F); w0 = igl.fast_winding_number(R.V, F, R.V - 1e-3 * n0)
    order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k])))
    log = []
    for rnd in range(int(os.environ.get('ROUNDS', 3))):
        tot = 0
        for pn in order:
            for fr in (0.25, 0.5, 0.75, 1.0):
                spec = [(b, p, a, d * fr) for b, p, a, d in PS[pn]]; t = time.time(); a, b, c = solve_one(R, C, S, spec, F, w0, log); tot += a
                if a or b: print('round %d %-30s x%.2f flips before %4d after-solve %4d contact %4d  %.1fs' % (rnd, pn, fr, a, b, c, time.time() - t), flush=True)
                log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=b, contact_projected=c))
        print('round', rnd, 'total flips entering', tot, flush=True)
        if tot == 0: break
    C.save(out, dict(status='RP6 RIG PILOT / NOT FROZEN', config=cfg, weights=os.path.basename(wf), method=open(CC.__file__).read().split('import')[0], fit_log=log))
