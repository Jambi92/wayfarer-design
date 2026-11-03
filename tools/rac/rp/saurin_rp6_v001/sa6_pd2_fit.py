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
d = C.load(); z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Fd = w['f'].astype(np.int64)
def base_cfg(nm): return 'F' if nm.startswith('F-') else 'M'
def state_rig(nm):
    cfg = base_cfg(nm); VB = np.load(C.W + '/cr_%s.npy' % nm).astype(float); Vs = (z['bc'][:, :, None] * VB[Fd[z['tri']]]).sum(1)
    J, M = SK.build(Vs, 'state'); Pst = SK.rec(J, M, 'creator state ' + nm)
    R = SP.Rig(cfg, WD + '/W_%s.npz' % cfg); R.V = Vs; R.P = Pst; R.n0 = R.qn(Vs); R.cfg = 'state'
    return R, cfg
if __name__ == '__main__':
    STATES, OD = sys.argv[1].split(','), sys.argv[2]; os.makedirs(OD, exist_ok=True)
    for nm in STATES:
        t0 = time.time(); R, cfg = state_rig(nm); Cs = CC.Correctives.load(R, WD + '/CF_%s.json' % cfg); S = CC.Solver(R); S.V0 = S.body_volume(R.V)
        F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
        order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log = []
        for rnd in range(ROUNDS):
            tot = 0
            for pn in order:
                for fr in FRACS:
                    spec = [(b, p, a, dg * fr) for b, p, a, dg in PS[pn]]; t = time.time()
                    a, b, c = FT.solve_one(R, Cs, S, spec, F, w0, log, pose_key=('%s@%.2f' % (pn, fr)) if rnd >= 1 else None); tot += a
                    if a or b: print('%s round %d %-24s x%.2f before %4d after %4d  %.1fs' % (nm, rnd, pn, fr, a, b, time.time() - t), flush=True)
                    log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=b))
            print(nm, 'round', rnd, 'total entering', tot, flush=True)
            if tot == 0: break
        Cs.save(OD + '/CF_state_%s.json' % nm, dict(status='RP6 RIG PILOT / NOT FROZEN', state=nm, base_config=cfg, base_correctives='CF_%s.json' % cfg,
                                                     weights='W_%s.npz' % cfg, fit_log=log, converged=bool(tot == 0)))
        print(nm, 'DONE converged', tot == 0, '%.0fs' % (time.time() - t0), flush=True)
