# sa6_pd2_fit.py STATES OUTDIR : RP6 creator-state corrective layer (closure order 58aa486c §2 PD-2 / order a407015 §8, §18).
#   The base-configuration correctives (c1 for SA-M* states, c2 for SA-F* states) are rest-space deltas fitted on the base body; on a creator state whose
#   proportions / tissue differ (narrow, broad, muscle, fat, stature, trunk length, tail) they leave a few RIG-OWNED folds at the same joints.  This tool fits
#   a per-state ADDITIVE corrective layer with the identical solver, gates and locality rules as sa6_fit (folds, penetration, tears, closed-body volume, rigid
#   landmarks protected) on the state's own rest body (frozen cage realised through the frozen barycentric embedding; skeleton re-evaluated on the state by
#   the same landmark transfer as c2).  Base weights are NOT changed (one weight set per base configuration, carried by topology).
#   Runtime interface (documented in SA_RP6_PD1_PD2_interfaces_v001.md): corrective(state, pose) = base corrective(pose) + layer_state(pose); between
#   accepted states the creator blends the layers with the creator weights (same convex weights as the creator morphs).  Output per state:
#   OUTDIR/CF_state_<STATE>.json/.npz (full corrective set = base + layer; the layer = difference to the base set).
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT
WD = os.environ.get('RP6_WD', '/tmp/claude-0/rp6'); ROUNDS = int(os.environ.get('ROUNDS', 4)); FRACS = (1.0, 0.5)
d = C.load(); z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = None if C.PORTABLE else np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Fd = None if C.PORTABLE else w['f'].astype(np.int64)
def base_cfg(nm): return 'F' if nm.startswith('F-') else 'M'
def state_rig(nm):
    cfg = base_cfg(nm)
    if C.PORTABLE: Vs = np.load(C.W + '/cage_V/S_%s.npy' % nm)
    else: VB = np.load(C.W + '/cr_%s.npy' % nm).astype(float); Vs = (z['bc'][:, :, None] * VB[Fd[z['tri']]]).sum(1)
    J, M = SK.build(Vs, 'state'); Pst = SK.rec(J, M, 'creator state ' + nm)
    R = SP.Rig(cfg, WD + '/W_%s.npz' % cfg); R.V = Vs; R.P = Pst; R.n0 = R.qn(Vs); R.cfg = 'state'
    return R, cfg
def comp_mask(nm, R):
    """quads owned by the PRE-RIG composition (same rule as the sa6_pd2 ownership screen): rest quad centroid within 1 cm of a dense-source fold
    (canonical-base triangle whose normal flips or whose area collapses below 5 %) or of a neutral cage flip of the state."""
    cp = C.W + '/cage_V/C_%s.npy' % nm
    if C.PORTABLE: return np.load(cp) if os.path.exists(cp) else np.zeros(len(R.Q), bool)
    from scipy.spatial import cKDTree
    VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float)
    VB = np.load(C.W + '/cr_%s.npy' % nm).astype(float)
    def fn(P): return np.cross(P[Fd[:, 1]] - P[Fd[:, 0]], P[Fd[:, 2]] - P[Fd[:, 0]])
    nR, nB = fn(VR), fn(VB); aR, aB = np.linalg.norm(nR, axis=1), np.linalg.norm(nB, axis=1); bad = ((nR * nB).sum(1) / (aR * aB + 1e-20) < 0) | (aB < 0.05 * aR)
    P0 = (z['bc'][:, :, None] * VR[Fd[z['tri']]]).sum(1); Q = d['Q']
    q0 = np.cross(P0[Q[:, 2]] - P0[Q[:, 0]], P0[Q[:, 3]] - P0[Q[:, 1]]); q1 = np.cross(R.V[Q[:, 2]] - R.V[Q[:, 0]], R.V[Q[:, 3]] - R.V[Q[:, 1]]); nfl = (q0 * q1).sum(1) < 0
    pts = np.r_[VB[Fd[bad]].mean(1) if bad.any() else np.zeros((0, 3)), R.V[Q[nfl]].mean(1) if nfl.any() else np.zeros((0, 3))]
    return cKDTree(pts).query(R.V[R.Q].mean(1))[0] <= 1.0 if len(pts) else np.zeros(len(R.Q), bool)
def mask_composition(R, comp):
    """COMPOSITION MASK (RP6 closure v002): quads folded by the pre-rig composition are not rig defects and cannot be repaired by a corrective (the
    neutral body itself is folded there); the fit ignores their orientation so the solver does not trade volume / neighbouring quads chasing them.
    The PD-2 audit evaluates WITHOUT this mask (they are reported as COMPOSITION/PD-2 there, every other fold stays rig-owned)."""
    if not comp.any(): return R
    orig = R.relcos; R.relcos = lambda P, T, W=None: np.where(comp, 1.0, orig(P, T, W)); return R
if __name__ == '__main__':
    STATES, OD = sys.argv[1].split(','), sys.argv[2]; os.makedirs(OD, exist_ok=True)
    for nm in STATES:
        t0 = time.time(); R, cfg = state_rig(nm); comp = comp_mask(nm, R) if os.environ.get('COMP_MASK', '1') == '1' else np.zeros(len(R.Q), bool); mask_composition(R, comp)
        print(nm, 'composition-masked quads', int(comp.sum()), flush=True); Cs = CC.Correctives.load(R, WD + '/CF_%s.json' % cfg); S = CC.Solver(R); S.V0 = S.body_volume(R.V)
        F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
        order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log = []
        ck = OD + '/ckpt/CF_ckpt_%s.json' % nm; os.makedirs(OD + '/ckpt', exist_ok=True); r0, i0, tot0 = 0, 0, 0
        if os.path.exists(ck):                              # resume after a killed run (checkpoint written after every pose solve)
            m = json.load(open(ck)); Cs = CC.Correctives.load(R, ck); log = m['fit_log']; r0, i0, tot0 = m['ck_round'], m['ck_next'], m['ck_tot']
            print(nm, 'resume round', r0, 'item', i0, flush=True)
        items = [(pn, fr) for pn in order for fr in FRACS]
        for rnd in range(r0, ROUNDS):
            tot = tot0 if rnd == r0 else 0
            for ii, (pn, fr) in enumerate(items):
                if rnd == r0 and ii < i0: continue
                if True:
                    spec = [(b, p, a, dg * fr) for b, p, a, dg in PS[pn]]; t = time.time()
                    a, b, c = FT.solve_one(R, Cs, S, spec, F, w0, log, pose_key=('%s@%.2f' % (pn, fr)) if rnd >= 1 else None); tot += a
                    if a or b: print('%s round %d %-24s x%.2f before %4d after %4d  %.1fs' % (nm, rnd, pn, fr, a, b, time.time() - t), flush=True)
                    log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=b))
                    if a or b: Cs.save(ck, dict(state=nm, fit_log=log, ck_round=rnd, ck_next=ii + 1, ck_tot=tot))
                    else: json.dump(dict(json.load(open(ck)), fit_log=log, ck_round=rnd, ck_next=ii + 1, ck_tot=tot), open(ck, 'w')) if os.path.exists(ck) else None
            print(nm, 'round', rnd, 'total entering', tot, flush=True)
            if tot == 0: break
        Cs.save(OD + '/CF_state_%s.json' % nm, dict(status='RP6 RIG PILOT / NOT FROZEN', state=nm, base_config=cfg, composition_masked_quads=int(comp.sum()), base_correctives='CF_%s.json' % cfg,
                                                     weights='W_%s.npz' % cfg, fit_log=log, converged=bool(tot == 0)))
        print(nm, 'DONE converged', tot == 0, '%.0fs' % (time.time() - t0), flush=True)
