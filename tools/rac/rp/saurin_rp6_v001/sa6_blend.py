# sa6_blend.py : creator-blend bodies and their evaluation (corrective-layer validation order 3e76b509).
#   python3 sa6_blend.py bodies OUTDIR           -> precompute every body (needs the clean dense workspace): cage, pre-rig folds, ownership inputs
#   python3 sa6_blend.py eval BODYDIR OUTDIR [NAMES|all] [FRACS]   -> evaluate bodies (portable: needs only BODYDIR + the RP6 package + frozen files)
#
#   GEOMETRY METHOD (documented body interpolation of the proposed interface): a creator body = convex blend of the accepted DENSE creator bodies on the
#   canonical W2I6 face list,  VB = (1 - sum w_i) * VB_base + sum w_i * VB_i  (VB_base = the base configuration's dense body: c1 = SA-M188 work body,
#   c2 = SA-F188 work body), with the same weights as the corrective blend.  The frozen cage is realised on VB through the frozen barycentric embedding
#   (linear, so cage(VB) = the same blend of the state cages); joints are re-derived on the body by the RP6 landmark transfer (sa6_skeleton 'state');
#   weights = the base configuration's production weights.  Pre-rig source folds of VB (flipped vs the canonical base or area < 5 % of rest) and neutral
#   cage flips (vs the canonical-base cage) are measured on every body.
#   OWNERSHIP = the closure rules (sa6_pd2.py at c7e3151): composition only at a pre-rig fold (<= 1 cm) AND already present under plain LBS of the pose;
#   creator-inverted neutral quads always composition; a contact inside the composition zone that only meets composition-folded flesh = the fold's own
#   self-intersection.  Every other fold / new contact / tear (> 2.5x and > 0.75 cm) / |dV| > 100 cm3 (jaw poses exempt) is rig-owned.
#   Columns per pose: plain LBS | base correctives alone | base + blended layers (production).  Neutral: max corrective displacement of B, every S_i and
#   the blend at the rest pose.  Rigid: max production corrective displacement on the base configuration's protected rigid set (head unit, rigid claw
#   caps, rigid landmark vertices + 2 rings; vertex ids carried by topology) -- gate <= 0.05 cm as for c1 / c2.
import os, sys, json, time, numpy as np, igl
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT, sa6_layer_harness as H
ST = 'RP6 RIG PILOT / NOT FROZEN'; FRACS = (0.25, 0.5, 0.75, 1.0)
M_EXT = ['MUHI', 'FAHI', 'MUFAHI', 'NAR', 'BRD', 'T80', 'LT90', 'M208-B']     # base -> extreme paths on c1
TWO = [('MUHI', 'FAHI'), ('NAR', 'BRD'), ('FAHI', 'MUFAHI'), ('T55', 'T80')]    # between-state paths, two active layers
T3 = (0.25, 0.5, 0.75)
HELD = ['MUHI', 'FAHI', 'MUFAHI', 'T80', 'M208-B']                             # paths whose v003 node carries creator keys
STATES = ['B-T80', 'BRD', 'DSP-HIGH', 'DSP-LOW', 'F-N', 'FAHI', 'LT90', 'M168', 'M208-B', 'MIN', 'MUFAHI', 'MUHI', 'NAR', 'ORB+3', 'ORB-8', 'RDG0.90', 'RDG1.30', 'T55', 'T80']
def bodies():
    b = {'BASE_c1': dict(cfg='M', w={}, kind='control: base c1 (zero state influence)'), 'BASE_c2': dict(cfg='F', w={}, kind='control: base c2 (zero state influence)')}
    for s in STATES: b['END_' + s] = dict(cfg=H.state_cfg(s), w={s: 1.0}, kind='endpoint: accepted state at unit influence')
    for s in M_EXT:
        for t in T3: b['c1-%s@%.2f' % (s, t)] = dict(cfg='M', w={s: t}, kind='base -> extreme', path='c1 -> ' + s, t=t)
    for s in HELD:      # held-out weights between the creator-key knots (layer v003 nodes at 0.50): 0.375 / 0.625
        for t in (0.375, 0.625): b['c1-%s@%.3f' % (s, t)] = dict(cfg='M', w={s: t}, kind='base -> extreme, held-out weight (between creator-key knots)', path='c1 -> ' + s, t=t)
    for t in T3: b['c2-F-N@%.2f' % t] = dict(cfg='F', w={'F-N': t}, kind='base -> state (c2)', path='c2 -> F-N', t=t)
    for x, y in TWO:
        for t in T3: b['%s-%s@%.2f' % (x, y, t)] = dict(cfg='M', w={x: 1 - t, y: t}, kind='between states (two active layers)', path=x + ' -> ' + y, t=t)
    b['MIX1'] = dict(cfg='M', w={'MUHI': 0.4, 'FAHI': 0.3, 'BRD': 0.3}, kind='mixed: three active layers (broad + muscle + fat)')
    b['MIX2'] = dict(cfg='M', w={'NAR': 0.3, 'FAHI': 0.3, 'T80': 0.3}, kind='mixed: three active layers + base 0.1 (narrow + fat + long tail)')
    return b
def precompute(OUT, B=None):
    import sa6_pd2_fit as PF
    os.makedirs(OUT, exist_ok=True); d = C.load(); z = PF.z; w = PF.w; F = PF.Fd
    VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float)
    def fn(P): return np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    nR = fn(VR); aR = np.linalg.norm(nR, axis=1); P0 = (z['bc'][:, :, None] * VR[F[z['tri']]]).sum(1); Q = d['Q']
    q0 = np.cross(P0[Q[:, 2]] - P0[Q[:, 0]], P0[Q[:, 3]] - P0[Q[:, 1]])
    dense = {}
    def VBof(n):
        if n not in dense: dense[n] = (w['v_M'] if n == 'M' else w['v_F'] if n == 'F' else np.load(C.W + '/cr_%s.npy' % n)).astype(float)
        return dense[n]
    man = {}; jp = os.path.join(OUT, 'bodies.json'); old = json.load(open(jp))['bodies'] if os.path.exists(jp) else {}
    for nm, b in (B or bodies()).items():
        f = os.path.join(OUT, nm + '.npz')
        if os.path.exists(f) and os.environ.get('KEEP', '1') == '1' and nm in old:
            man[nm] = old[nm]; continue
        VB = VBof(b['cfg']) * (1.0 - sum(b['w'].values()))
        for s, ws in b['w'].items(): VB = VB + ws * VBof(s)
        nB = fn(VB); aB = np.linalg.norm(nB, axis=1); sflip = (nR * nB).sum(1) / (aR * aB + 1e-20) < 0; scol = aB < 0.05 * aR; bad = sflip | scol
        Vs = (z['bc'][:, :, None] * VB[F[z['tri']]]).sum(1); q1 = np.cross(Vs[Q[:, 2]] - Vs[Q[:, 0]], Vs[Q[:, 3]] - Vs[Q[:, 1]]); nflip = (q0 * q1).sum(1) < 0
        pts = np.r_[VB[F[bad]].mean(1) if bad.any() else np.zeros((0, 3)), Vs[Q[nflip]].mean(1) if nflip.any() else np.zeros((0, 3))]
        comp = cKDTree(pts).query(Vs[Q].mean(1))[0] <= 1.0 if len(pts) else np.zeros(len(Q), bool)
        np.savez(f, Vs=Vs, pts=pts, comp=comp, rest_inverted=nflip)
        man[nm] = dict(b, source_flipped=int(sflip.sum()), source_collapsed=int(scol.sum()), neutral_cage_flips=int(nflip.sum()), composition_quads=int(comp.sum()), sha256=C.sha(f))
        print(nm, b['cfg'], b['w'], 'src', int(sflip.sum()), int(scol.sum()), 'cage', int(nflip.sum()), 'comp', int(comp.sum()), flush=True)
    if B: man = dict(old, **man)        # adding bodies to an existing body set keeps the others
    json.dump(dict(status=ST, name='SA_RP6_blend_bodies_v001', method=open(__file__).read().split('import os')[0], bodies=man), open(os.path.join(OUT, 'bodies.json'), 'w'), indent=1)
def rig_of(nm, b, BD):
    z = np.load(os.path.join(BD, nm + '.npz')); Vs = z['Vs']; cfg = b['cfg']
    R = SP.Rig(cfg, os.path.join(H.PKG, 'SA_RP6_weights_%s_v001.npz' % cfg)); J, M = SK.build(Vs, 'state'); R.V = Vs; R.P = SK.rec(J, M, 'creator body ' + nm); R.n0 = R.qn(Vs); R.cfg = 'state'
    return R, z
_RID = {}
def rigid_ids(cfg):
    """protected rigid set of the BASE configuration (head-rigid unit, rigid claw caps, rigid landmark vertices + 2 rings), as vertex ids: carried to
    every creator body by topology (the same set the base fit protects and the c1 / c2 rigidity gate checks)"""
    if cfg not in _RID: _RID[cfg] = CC.Solver(SP.Rig(cfg, os.path.join(H.PKG, 'SA_RP6_weights_%s_v001.npz' % cfg))).protect
    return _RID[cfg]
def evaluate(nm, b, BD, fracs=FRACS, poses=None, bake=None):
    """bake: path of a per-body bake artifact (sa6_bake.py, K set): adds column 'bake' = packaged blend + K, re-opened from disk; the gates then apply to it"""
    t0 = time.time(); R, z = rig_of(nm, b, BD); S = CC.Solver(R); S.V0 = S.body_volume(R.V)
    Ft = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, Ft)
    Bc = H.load_base(R, b['cfg']); Ss = [(ws, H.load_state(R, s)[0]) for s, ws in b['w'].items()]; Pc = H.Blend(Bc, Ss)
    Kb = CC.Correctives.load(R, bake) if bake else None; G = 'bake' if bake else 'prod'; TAGS = ('lbs', 'base', 'prod') + (('bake',) if bake else ())
    pts = z['pts']; kd = cKDTree(pts) if len(pts) else None; inv = z['rest_inverted']; compq = z['comp']; compv = np.zeros(R.nv, bool); compv[R.Q[compq].ravel()] = True
    Fn = np.r_[R.Q[~compq][:, [0, 1, 2]], R.Q[~compq][:, [0, 2, 3]]].astype(np.int64)
    def near(X): return (kd.query(X)[0] <= 1.0) if (kd is not None and len(X)) else np.zeros(len(X), bool)
    T0 = R.pose([]); neutral = dict(base=float(np.abs(Bc.delta(T0)).max()), states={s: float(np.abs(c.delta(T0)).max()) for (s, _), (_, c) in zip(b['w'].items(), Ss)}, blend=float(np.abs(Pc.delta(T0)).max()))
    if bake: neutral['bake'] = float(np.abs(Pc.delta(T0) + Kb.delta(T0)).max())
    prot = rigid_ids(b['cfg']); res = dict(name=nm, status=ST, body=b, neutral_max_displacement_cm=neutral, poses={}); tot = dict(rig_flips=0, rig_pen=0, rig_tears=0, vol_fail=0, comp=0, base_rig=0, lbs_rig=0, rigid_max_cm=0.0)
    suite = R.suite('anat')
    for pn, spec in suite.items():
        if poses and pn not in poses: continue
        vol = not any('jaw' in e[0] for e in spec); res['poses'][pn] = {}
        for fr in fracs:
            T = R.pose([(bb, p, a, dg * fr) for bb, p, a, dg in spec]); o = {}
            dP = Pc.delta(T); cols = [('lbs', None), ('base', Bc.delta(T)), ('prod', dP)] + ([('bake', dP + Kb.delta(T))] if bake else [])
            for tag, dl in cols:
                P = R.skin(T) if dl is None else R.skin(T, R.V + dl)
                f = np.nonzero(R.relcos(P, T) < 0)[0]; pen = np.nonzero(FT.penetration(R, P, Ft, w0))[0]; te = S.tear_edges(P)[0]
                o[tag] = dict(P=P, f=f, pen=pen, tears=S._E1[te], dV=(S.body_volume(P) - S.V0) if vol else 0.0, dl=dl)
            lb = o['lbs']; row = {}
            for tag in TAGS:
                c = o[tag]
                cf = (near(R.V[R.Q[c['f']]].mean(1)) & np.isin(c['f'], lb['f'])) | inv[c['f']] if len(c['f']) else np.zeros(0, bool)
                cp = near(R.V[c['pen']]) & np.isin(c['pen'], lb['pen'])
                if (~cp).any() and compq.any():
                    rp = c['pen'][~cp]; q = c['P'][rp] - FT.PEN_TOL * igl.per_vertex_normals(c['P'], Ft)[rp]
                    own = compv[rp] & (igl.fast_winding_number(c['P'], Fn, q) < 1.5); cp[np.nonzero(~cp)[0][own]] = True
                ct = near(R.V[c['tears']].mean(1)) if len(c['tears']) else np.zeros(0, bool)
                if len(c['tears']): lt = {tuple(e) for e in np.sort(lb['tears'], 1)}; ct &= np.array([tuple(e) in lt for e in np.sort(c['tears'], 1)])
                row[tag] = dict(flips=int(len(c['f'])), composition=int(cf.sum()), rig_flips=int((~cf).sum()), new_pen=int(len(c['pen'])), rig_pen=int((~cp).sum()),
                                tears=int(len(c['tears'])), rig_tears=int((~ct).sum()), dV_cm3=round(float(c['dV']), 2), volume_ok=bool(abs(c['dV']) <= 100),
                                regions=sorted({str(R.ql[q_]) for q_ in c['f'][~cf]})[:6] if len(c['f']) else [])
            rig = float(np.linalg.norm(o[G]['dl'][prot], axis=1).max()) if prot.any() else 0.0; row[G]['rigid_max_cm'] = round(rig, 5)
            res['poses'][pn][('%.2f' % fr) if round(fr, 2) == fr else ('%.5f' % fr)] = row; pr = row[G]
            tot['rig_flips'] += pr['rig_flips']; tot['rig_pen'] += pr['rig_pen']; tot['rig_tears'] += pr['rig_tears']; tot['vol_fail'] += int(not pr['volume_ok']); tot['comp'] += pr['composition']
            tot['base_rig'] += row['base']['rig_flips'] + row['base']['rig_pen'] + row['base']['rig_tears'] + int(not row['base']['volume_ok']); tot['lbs_rig'] += row['lbs']['rig_flips']
            tot['rigid_max_cm'] = max(tot['rigid_max_cm'], rig)
    if bake: tot['blend_rig'] = sum(r['prod']['rig_flips'] + r['prod']['rig_pen'] + r['prod']['rig_tears'] + int(not r['prod']['volume_ok']) for v in res['poses'].values() for r in v.values())
    res['gated_column'] = G; res['totals'] = tot; res['clean'] = not (tot['rig_flips'] or tot['rig_pen'] or tot['rig_tears'] or tot['vol_fail'] or tot['rigid_max_cm'] > 0.05 or max([neutral['base'], neutral['blend'], neutral.get('bake', 0.0)] + list(neutral['states'].values())) > 0)
    res['seconds'] = round(time.time() - t0, 1); return res
if __name__ == '__main__':
    if sys.argv[1] == 'bodies': precompute(sys.argv[2])
    elif sys.argv[1] == 'eval':
        BD, OD = sys.argv[2], sys.argv[3]; os.makedirs(OD, exist_ok=True); man = json.load(open(os.path.join(BD, 'bodies.json')))['bodies']
        names = list(man) if len(sys.argv) < 5 or sys.argv[4] == 'all' else sys.argv[4].split(',')
        fr = tuple(float(x) for x in sys.argv[5].split(',')) if len(sys.argv) > 5 else FRACS
        for nm in names:
            fo = os.path.join(OD, nm + '.json')
            if os.path.exists(fo): continue
            r = evaluate(nm, man[nm], BD, fr); json.dump(r, open(fo, 'w'), indent=1)
            t = r['totals']; print('%-22s clean %s | rig flips %d pen %d tears %d volfail %d rigid %.4f | comp %d | base-only rig %d | neutral %s | %.0fs' % (
                nm, r['clean'], t['rig_flips'], t['rig_pen'], t['rig_tears'], t['vol_fail'], t['rigid_max_cm'], t['comp'], t['base_rig'], r['neutral_max_displacement_cm'], r['seconds']), flush=True)
