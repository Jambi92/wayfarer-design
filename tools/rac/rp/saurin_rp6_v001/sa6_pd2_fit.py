# sa6_pd2_fit.py STATES OUTDIR : RP6 creator-state corrective layer (closure order 58aa486c §2 PD-2 / order a407015 §8, §18).
#   The base-configuration correctives (c1 for SA-M* states, c2 for SA-F* states) are rest-space deltas fitted on the base body; on a creator state whose
#   proportions / tissue differ (narrow, broad, muscle, fat, stature, trunk length, tail) they leave a few RIG-OWNED folds at the same joints.  This tool fits
#   a per-state ADDITIVE corrective layer with the identical solver, gates and locality rules as sa6_fit (folds, penetration, tears, closed-body volume, rigid
#   landmarks protected) on the state's own rest body (frozen cage realised through the frozen barycentric embedding; skeleton re-evaluated on the state by
#   the same landmark transfer as c2).  Base weights are NOT changed (one weight set per base configuration, carried by topology).
#   Runtime interface (documented in SA_RP6_PD1_PD2_interfaces_v001.md): corrective(state, pose) = base corrective(pose) + layer_state(pose); between
#   accepted states the creator blends the layers with the creator weights (same convex weights as the creator morphs).  Output per state:
#   OUTDIR/CF_state_<STATE>.json/.npz (full corrective set = base + layer; the layer = difference to the base set).
import sys, os, json, time, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT
os.environ.setdefault('PK_HAT_EXACT', '1')    # rig v002 fits: fraction keys as an exact hat partition (sa6_correctives.rehat); no effect on v001 (PK_HAT_STEP 0)
WD = os.environ.get('RP6_WD', '/tmp/claude-0/rp6'); ROUNDS = int(os.environ.get('ROUNDS', 4)); FRACS = tuple(float(x) for x in os.environ.get('FRACS', '1.0,0.5').split(','))   # layer v002 (corrective-layer validation): FRACS=1.0,0.5,0.75,0.25
d = C.load(); z = np.load(C.FZ + '/SA_RP5_full_cage_freeze_candidate_v001.npz'); w = None if C.PORTABLE else np.load(C.W + '/work/SA_RP5_WORK_v001.npz'); Fd = None if C.PORTABLE else w['f'].astype(np.int64)
def _canon_cage():
    if C.PORTABLE: return np.load(C.W + '/cage_V/P0.npy') if os.path.exists(C.W + '/cage_V/P0.npy') else np.load(C.W + '/cage_V/V1.npy')
    VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float)
    return (z['bc'][:, :, None] * VR[Fd[z['tri']]]).sum(1)
V1C = _canon_cage()          # the frozen cage realised on the CANONICAL base (= the RP5 PD-2 neutral-cage-flip reference)
def base_cfg(nm): return 'F' if nm.startswith('F-') else 'M'
def state_rig(nm):
    cfg = base_cfg(nm)
    if C.PORTABLE: Vs = np.load(C.W + '/cage_V/S_%s.npy' % nm)
    else: VB = np.load(C.W + '/cr_%s.npy' % nm).astype(float); Vs = (z['bc'][:, :, None] * VB[Fd[z['tri']]]).sum(1)
    J, M = SK.build(Vs, 'state'); Pst = SK.rec(J, M, 'creator state ' + nm)
    R = SP.Rig(cfg, WD + '/W_%s.npz' % cfg); R.V = Vs; R.P = Pst; R.n0 = R.qn(Vs); R.cfg = 'state'; R.base_cfg = cfg
    # closure v003: quads that the creator composition INVERTS in the neutral (normal flipped vs the canonical base cage = RP5 'neutral cage flips')
    # have no valid rest orientation: their posed orientation is composition-owned in every pose (neither 'folding' nor 'straightening' them is a
    # rig result).  Recorded here; the PD-2 audit assigns them to COMPOSITION/PD-2 and the layer fit ignores them.
    nC = R.qn(V1C); R.rest_inverted = (nC * R.n0).sum(1) < 0
    return R, cfg
def gate_set(R):
    """rig v002 (order 07a3f24c, pass 7): the 56 special-gate poses (sa6_gates, incl. the combined shoulder + elbow gates) as fit poses 'gate:<pose>', exactly as
    the base fit (sa6_fit.pose_set) uses them.  Before pass 7 the state layers / knots were fitted on the 34 anatomical poses only, and their family samples beyond
    the anatomical range (gate-only angles, e.g. foot +-25, jaw -24 / -32) were carried from the rig v001 state sets: on FAHI / MUFAHI they folded the ankle /
    foot / jaw special gates (584 rig flips on the unbaked END bodies, v004: 0)."""
    import sa6_gates as GT
    return {'gate:' + k: v for k, v in GT.gate_poses(R).items()}
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
    """COMPOSITION MASK (RP6 closure v002): a fold or a self-contact that the pre-rig composition ALREADY produces in a pose (present under plain LBS
    of the pose, on quads / vertices of the composition-folded zone) is not a rig defect and cannot be repaired by a
    corrective (the neutral body itself is folded there).  The fit ignores exactly those -- set per pose by start_pose() -- so the solver neither trades
    volume / neighbouring quads chasing them nor is blocked by them; anything NEW (also inside the composition zone) still counts.  The PD-2 audit
    evaluates WITHOUT any mask."""
    R._comp = comp; R._compv = np.zeros(R.nv, bool); R._compv[R.Q[comp].ravel()] = True
    R._allow_q = np.zeros(len(R.Q), bool); R._allow_v = np.zeros(R.nv, bool)
    if not (comp.any() or R.rest_inverted.any()): return R
    orig = R.relcos; R._relcos_raw = orig; R.relcos = lambda P, T, W=None: np.where(R._allow_q, 1.0, orig(P, T, W))
    if not hasattr(FT, '_pen_raw'): FT._pen_raw = FT.penetration
    Fn = np.r_[R.Q[~comp][:, [0, 1, 2]], R.Q[~comp][:, [0, 2, 3]]].astype(np.int64)
    def pen(R_, P, F, w0):
        m = FT._pen_raw(R_, P, F, w0) & ~getattr(R_, '_allow_v', np.zeros(len(P), bool)); c = np.nonzero(m & getattr(R_, '_compv', np.zeros(len(P), bool)))[0]
        if len(c):     # contact inside the composition zone that only meets composition-folded flesh = the fold's own self-intersection (= PD-2 audit rule)
            q = P[c] - FT.PEN_TOL * igl.per_vertex_normals(P, F)[c]; m[c[igl.fast_winding_number(P, Fn, q) < 1.5]] = False
        return m
    FT.penetration = pen
    return R
def start_pose(R, Cs, spec, F, w0, S=None):
    """per-pose allowance: composition-zone folds / contacts / stretched edges that plain LBS of this pose already shows (never ones the correctives make)"""
    if not (getattr(R, '_comp', np.zeros(1, bool)).any() or R.rest_inverted.any()): return
    T = R.pose(spec); P = R.skin(T)        # the reference is plain LBS of the pose (strict rule, = PD-2 audit): defects the composition shows
    R._allow_q = (R._comp & (R._relcos_raw(P, T) < 0)) | R.rest_inverted; R._allow_v = R._compv & FT._pen_raw(R, P, F, w0)
    if S is not None:
        if not hasattr(S, '_tear_raw'):
            S._tear_raw = S.tear_edges; S._allow_e = None
            def te(P_, S=S):
                m, dl = S._tear_raw(P_)
                if S._allow_e is None: return m, dl
                if S._allow_n is not None and (m & S._comp_e).sum() <= S._allow_n: return m & ~S._comp_e, dl   # PLEAT_COMP_COUNT (below)
                return m & ~S._allow_e, dl
            S.tear_edges = te
        m0, _ = S._tear_raw(P); S._comp_e = R._compv[S._E1].all(1); S._allow_e = m0 & S._comp_e
        # rig v002 pass 9b, PLEAT_COMP_COUNT=1: inside the composition zone the allowance is a COUNT -- no more tear / pleat edges than plain LBS of the pose
        # shows there (the creator body's own folds: the heavy belly fold moves by an edge or two as it is corrected; found on knot FAHI@0.50
        # lower_axial_flex_25: LBS 10 pleated composition edges, blend 6, knot 1, and every local fade of that one moves it to a neighbouring edge)
        S._allow_n = int(S._allow_e.sum()) if os.environ.get('PLEAT_COMP_COUNT') == '1' else None
if __name__ == '__main__':
    STATES, OD = sys.argv[1].split(','), sys.argv[2]; os.makedirs(OD, exist_ok=True)
    for nm in STATES:
        t0 = time.time(); R, cfg = state_rig(nm); comp = comp_mask(nm, R) if os.environ.get('COMP_MASK', '1') == '1' else np.zeros(len(R.Q), bool); mask_composition(R, comp)
        print(nm, 'composition-masked quads', int(comp.sum()), flush=True); ini = os.environ.get('INIT_LAYER', '') and os.path.join(os.environ['INIT_LAYER'], 'CF_state_%s.json' % nm)   # refine an earlier layer
        Cs = CC.Correctives.load(R, ini if ini and os.path.exists(ini) else WD + '/CF_%s.json' % cfg); print(nm, 'start from', ini if ini and os.path.exists(ini) else 'base', flush=True); S = CC.Solver(R); S.V0 = S.body_volume(R.V)
        F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
        if C.RIGV != 'v001' and os.environ.get('PD2_GATES') == '1': PS.update(gate_set(R))   # rig v002 pass 7: the special gates enter the state fit (as in the base fit)
        if os.environ.get('PD2_ONLY'): PS = {k: v for k, v in PS.items() if k in os.environ['PD2_ONLY'].split(',')}     # diagnostics only
        order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log = []
        ck = OD + '/ckpt/CF_ckpt_%s.json' % nm; os.makedirs(OD + '/ckpt', exist_ok=True); r0, i0, tot0 = 0, 0, 0
        if os.path.exists(ck):                              # resume after a killed run (checkpoint written after every pose solve)
            m = json.load(open(ck)); Cs = CC.Correctives.load(R, ck); log = m['fit_log']; r0, i0, tot0 = m['ck_round'], m['ck_next'], m['ck_tot']
            print(nm, 'resume round', r0, 'item', i0, flush=True)
        items = [(pn, fr) for pn in order for fr in FRACS]
        PA = None; pa = os.environ.get('PLEAT_ALLOW', '') and os.path.join(os.environ['PLEAT_ALLOW'], 'pleat_allow_%s.npz' % nm)   # pass 9b: accepted-reference pleats
        if pa and os.path.exists(pa):
            PA = dict(np.load(pa)); S.pleat_edges(R.V); PA_n = len(S._pq); PA_i = {str(n_): i_ for i_, n_ in enumerate(PA['names'])}
            assert (PA['ev'] == S._pev).all(), 'pleat allowance edge order differs'; print(nm, 'pleat allowance', pa, len(PA_i), 'poses', flush=True)
        for rnd in range(r0, ROUNDS):
            tot = tot0 if rnd == r0 else 0
            for ii, (pn, fr) in enumerate(items):
                if rnd == r0 and ii < i0: continue
                if True:
                    spec = [(b, p, a, dg * fr) for b, p, a, dg in PS[pn]]; t = time.time(); start_pose(R, Cs, spec, F, w0, S)
                    if PA is not None:
                        pa_k = '%s@%.2f' % (pn, fr); S._pallow = np.unpackbits(PA['P'][PA_i[pa_k]])[:PA_n].astype(bool) if pa_k in PA_i else None
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
