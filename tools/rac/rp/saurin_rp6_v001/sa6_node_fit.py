# sa6_node_fit.py NODE BODYDIR LAYERDIR OUTDIR : creator-weight node keys of a state corrective layer (corrective-layer validation order 3e76b509, layer v003).
#   Finding (blend coverage, SA_RP6_blend_eval v001): the proposed linear blend  (1 - w) B(T) + w S(T)  is exact at the endpoints but leaves rig-owned folds /
#   volume misses on intermediate creator bodies (c1 -> MUHI / FAHI / MUFAHI at w = 0.25 .. 0.75): the corrective a body needs is not linear in the creator
#   weight (the same reason pose keys exist in pose space).  Layer v003 therefore gives a state layer optional CREATOR KEYS: corrective sets K_n fitted at
#   creator-weight nodes w_n of the base -> state path, entering through a hat in the state's own creator weight that is 0 at w = 0 and at w = 1:
#
#     S_i(T, w_i) = S_i(T) + sum_n h_n(w_i) K_{i,n}(T)          production = (1 - sum w_i) B(T) + sum_i w_i S_i(T, w_i)
#
#   (h_n = piecewise-linear hat over the knots 0, w_1 .. w_k, 1; zero at both ends -> endpoint identities and the zero-influence identity are unchanged; K are
#   pose-driven sets like every corrective -> exactly 0 at neutral).
#   Fit of one node: the node body = base -> state convex blend at w_n (sa6_blend precomputed body, same geometry method); production at the node =
#   blend + w_n K (h = 1 there); every increment dd the standard solver (sa6_fit.solve_one, unchanged gates / locality / composition mask = sa6_pd2_fit rules)
#   asks for is stored in K as dd / w_n.  B and S_i are not changed.  Angle fractions 1.0 / 0.75 / 0.5 / 0.25, 4 rounds, pose keys from round 1, resumable.
#   NODE = <STATE>@<w> (the body 'c1-<STATE>@<w>' or 'c2-<STATE>@<w>' must exist in BODYDIR).  Output OUTDIR/CK_<STATE>@<w>.json/.npz.
import sys, os, json, time, copy, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF, sa6_layer_harness as H, sa6_blend as BL
os.environ.setdefault('PK_HAT_EXACT', '1')    # rig v002 fits: fraction keys as an exact hat partition (sa6_correctives.rehat); no effect on v001 (PK_HAT_STEP 0)
ROUNDS = int(os.environ.get('ROUNDS', 4)); FRACS = (1.0, 0.75, 0.5, 0.25)
class NodeProxy:
    """the corrective set the solver sees on the node body: production = (1 - w) B + w (S + E + K); increments are written to K scaled by 1 / w.
    E = the creator keys already packaged for this state, interpolated at w (COMPOSITE knot, layer v005: a knot added between existing knots starts from
    what the interpolation already gives there, so neighbouring knots stay consistent and the interpolation between them stays continuous); E = 0 for a
    first-generation knot."""
    def __init__(self, B, S, K, w, E=None): self.B, self.S, self.K, self.w, self.E = B, S, K, w, E; self.r = K.r; self.F = K.F; self.PK = K.PK
    def delta(self, T):
        d = self.S.delta(T) + self.K.delta(T)
        if self.E is not None: d = d + self.E(T)
        return (1 - self.w) * self.B.delta(T) + self.w * d
    def driver(self, T, f): return self.K.driver(T, f)
    def resolve(self, bone, axis, tol_deg=30.0): return self.K.resolve(bone, axis, tol_deg)
    def add(self, key, bone, axis, pivot, x, idx, dd): self.K.add(key, bone, axis, pivot, x, idx, dd / self.w)
    def add_pose_key(self, name, drivers, idx, dd): self.K.add_pose_key(name, drivers, idx, dd / self.w)
def defects(R, P, Sv, spec, F, w0):
    """open defects of the node production at one pose, as the solver counts them: folds (composition-masked) + penetrating vertices + tear edges + volume miss"""
    T = R.pose(spec); Pc = R.skin(T, R.V + P.delta(T)); vol = any(e[0] in FT.VOL_BONES or e[0].rsplit('_', 1)[0] in FT.VOL_BONES for e in spec)
    return int((R.relcos(Pc, T) < 0).sum()) + int(FT.penetration(R, Pc, F, w0).sum()) + int(Sv.tear_edges(Pc)[0].sum()) + int(vol and abs(Sv.body_volume(Pc) - Sv.V0) > FT.VOL_TRIG)
def fade(R, P, Sv, spec, F, w0, rig):
    """local fade fallback (see sa6_node_fade.py): the production corrective is faded out around the remaining folds (falloff over k quad rings,
    k = 1 .. 16) -- starting from the current production d, or from the creator blend without this node's key d0 (when the node key itself has made the
    pose worse); the first candidate with no fold, no new contact / tear and |dV| <= VOL_ACCEPT is kept and stored in K as a sample of the driving family"""
    T = R.pose(spec); d = P.delta(T); d0 = (1 - P.w) * P.B.delta(T) + P.w * P.S.delta(T); Pc = R.skin(T, R.V + d)
    p0, t0 = int(FT.penetration(R, Pc, F, w0).sum()), int(Sv.tear_edges(Pc)[0].sum())
    tear_only = not (R.relcos(Pc, T) < 0).any()        # rig v002 pass 9b: a pleat / tear the knot itself made (no fold) is faded the same way
    if tear_only and (not t0 or os.environ.get('PLEAT_GATE') != '1'): return False
    for base in (d, d0):
        Pb = R.skin(T, R.V + base); seed = np.zeros(R.nv, bool); seed[R.Q[np.nonzero((R.relcos(Pb, T) < 0) | (R.relcos(Pc, T) < 0))[0]].ravel()] = True
        if tear_only: seed |= Sv.tear_verts(Pc)
        for k in (1, 2, 3, 4, 6, 8, 12, 16):
            rings = [seed]
            for _ in range(k): rings.append(Sv.dilate(rings[-1], 1))
            f = np.zeros(R.nv)
            for j, m in enumerate(rings): f[m & (f == 0)] = 1.0 - j / (k + 1.0)
            f[rig] = 0.0; dn = base * (1 - f[:, None]); Pn = R.skin(T, R.V + dn)
            if (R.relcos(Pn, T) < 0).any() or FT.penetration(R, Pn, F, w0).sum() > p0 or Sv.tear_edges(Pn)[0].sum() > (t0 - 1 if tear_only else t0) or abs(Sv.body_volume(Pn) - Sv.V0) > FT.VOL_ACCEPT: continue
            I = np.nonzero(np.abs(dn - d).sum(1) > 1e-9)[0]; bone, pv, ax = FT.entries(R, spec, T)[0]; key, axf = P.resolve(bone, ax); x = P.driver(T, dict(bone=bone, axis=axf))
            if abs(x) < 0.5: return False
            P.add(key, bone, axf, pv, x, I, (dn - d)[I]); return k
    # last resort (per-body bake, crease-edge quads): bounded local search on the remaining folds' vertices + 1 ring (deterministic seed, |change| <= 1 cm,
    # target relcos >= 0.05 on the neighbourhood); accepted only with no fold, no new contact / tear, |dV| <= VOL_ACCEPT; stored like the fade
    Pc = R.skin(T, R.V + d); f0 = np.nonzero(R.relcos(Pc, T) < 0)[0]
    if len(f0) > 6 or tear_only: return False
    seed = np.zeros(R.nv, bool); seed[R.Q[f0].ravel()] = True; m = Sv.dilate(seed, 1) & ~rig; vs = np.nonzero(m)[0]
    loc = np.nonzero(np.isin(R.Q, np.nonzero(Sv.dilate(m, 1))[0]).any(1))[0]
    def obj(dl): Pq = R.skin(T, R.V + dl); rc = R.relcos(Pq, T); return np.minimum(rc[loc] - 0.05, 0).sum(), int((rc < 0).sum())
    ok = False
    for seed, sig in ((0, 0.15), (1, 0.15), (2, 0.08), (3, 0.3), (4, 0.08)):      # several deterministic restarts (results must not hinge on one random path)
        rng = np.random.default_rng(seed); best = d.copy(); bo = obj(best)
        for _ in range(3000):
            cand = best.copy(); j = rng.choice(vs, size=min(3, len(vs)), replace=False); cand[j] += rng.normal(0, sig, (len(j), 3))
            if np.abs(cand - d).max() > 1.0: continue
            o = obj(cand)
            if o[0] > bo[0]: best, bo = cand, o
            if bo[1] == 0 and bo[0] >= -1e-9: break
        Pn = R.skin(T, R.V + best)
        if not (bo[1] or FT.penetration(R, Pn, F, w0).sum() > p0 or Sv.tear_edges(Pn)[0].sum() > t0 or abs(Sv.body_volume(Pn) - Sv.V0) > FT.VOL_ACCEPT): ok = True; break
    if not ok: return False
    I = np.nonzero(np.abs(best - d).sum(1) > 1e-9)[0]; bone, pv, ax = FT.entries(R, spec, T)[0]; key, axf = P.resolve(bone, ax); x = P.driver(T, dict(bone=bone, axis=axf))
    if abs(x) < 0.5: return False
    P.add(key, bone, axf, pv, x, I, (best - d)[I]); return 'local'
if __name__ == '__main__':
    node, BD, LD, OD = sys.argv[1:5]; st, ws = node.rsplit('@', 1); w = float(ws); os.makedirs(OD + '/ckpt', exist_ok=True)
    bm = json.load(open(os.path.join(BD, 'bodies.json')))['bodies']; bn = [k for k in ('c1-' + node, 'c2-' + node) if k in bm][0]; b = bm[bn]
    assert b['w'] == {st: w}, (bn, b['w'])
    t0 = time.time(); R, z = BL.rig_of(bn, b, BD); R.rest_inverted = z['rest_inverted']; PF.mask_composition(R, z['comp'])
    B = H.load_base(R, b['cfg']); S = CC.Correctives.load(R, os.path.join(LD, 'CF_state_%s.json' % st)); ck = OD + '/ckpt/CK_%s.json' % node
    K = CC.Correctives.load(R, ck) if os.path.exists(ck) else CC.Correctives(R); E = None; comp = []
    if os.environ.get('COMPOSITE_FROM'):          # composite knot: the existing knots of this state in that layer package, at their hat weights at w
        os.environ['RP6_LAYERS'] = os.environ['COMPOSITE_FROM']; H.LAYERS = os.environ['COMPOSITE_FROM']; SL, _ = H.load_state(R, st)
        hs = H.hats([k[0] for k in SL.keys], w); comp = [dict(node_weight=n, coef=h) for (n, _), h in zip(SL.keys, hs) if h]
        assert all(abs(c['node_weight'] - w) > 1e-9 for c in comp), 'knot already exists'
        refs = [(h, Kn) for (n, Kn), h in zip(SL.keys, hs) if h]; E = lambda T: sum(h * Kn.delta(T) for h, Kn in refs)
        print(node, 'composite knot from', os.environ['COMPOSITE_FROM'], comp, flush=True)
    P = NodeProxy(B, S, K, w, E)
    Sv = CC.Solver(R); Sv.V0 = Sv.body_volume(R.V); Sv.protect = Sv.protect | BL.rigid_ids(b['cfg'])   # + the base configuration's rigid ids (rigid gate set)
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
    if os.environ.get('PD2_GATES') == '1': PS.update(PF.gate_set(R))   # rig v002 pass 7: special gates in the knot fit too (sa6_pd2_fit.gate_set)
    order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log, r0, i0, tot0 = [], 0, 0, 0
    if os.path.exists(ck):
        m = json.load(open(ck)); log, r0, i0, tot0 = m['fit_log'], m['ck_round'], m['ck_next'], m['ck_tot']; print(node, 'resume round', r0, 'item', i0, flush=True)
    items = [(pn, fr) for pn in order for fr in FRACS]; tot = 0
    PA = None; pa = os.environ.get('PLEAT_ALLOW', '') and os.path.join(os.environ['PLEAT_ALLOW'], 'pleat_allow_%s.npz' % bn)   # pass 9b: the v001 knot body's pleats
    if pa and os.path.exists(pa):
        PA = dict(np.load(pa)); Sv.pleat_edges(R.V); PA_n = len(Sv._pq); PA_i = {str(n_): i_ for i_, n_ in enumerate(PA['names'])}
        assert (PA['ev'] == Sv._pev).all(), 'pleat allowance edge order differs'; print(node, 'pleat allowance', pa, len(PA_i), 'poses', flush=True)
    for rnd in range(r0, ROUNDS):
        tot = tot0 if rnd == r0 else 0
        for ii, (pn, fr) in enumerate(items):
            if rnd == r0 and ii < i0: continue
            spec = [(bb, p, a, dg * fr) for bb, p, a, dg in PS[pn]]; t = time.time(); PF.start_pose(R, P, spec, F, w0, Sv)
            if PA is not None:
                pa_k = '%s@%.2f' % (pn, fr); Sv._pallow = np.unpackbits(PA['P'][PA_i[pa_k]])[:PA_n].astype(bool) if pa_k in PA_i else None
            n0 = defects(R, P, Sv, spec, F, w0); snap = copy.deepcopy((K.F, K.PK)) if n0 else None
            a, c, _ = FT.solve_one(R, P, Sv, spec, F, w0, log, pose_key=('%s@%.2f' % (pn, fr)) if rnd >= 1 else None); tot += a
            if n0:      # GUARD (layer v003): a solve that leaves this pose worse than it found it is reverted; remaining folds -> local fade fallback
                n1 = defects(R, P, Sv, spec, F, w0)
                if n1 > n0: K.F.clear(); K.F.update(snap[0]); K.PK.clear(); K.PK.update(snap[1]); log.append(dict(round=rnd, pose=pn, frac=fr, reverted=[n0, n1])); n1 = n0
                if n1:
                    k_ = fade(R, P, Sv, spec, F, w0, Sv.protect); c = defects(R, P, Sv, spec, F, w0) if k_ else n1
                    log.append(dict(round=rnd, pose=pn, frac=fr, fade_ring=k_, after=c)) if k_ else None
            if a or c: print('%s round %d %-24s x%.2f before %4d after %4d  %.1fs' % (node, rnd, pn, fr, a, c, time.time() - t), flush=True)
            log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=c))
            K.save(ck, dict(node=node, fit_log=log, ck_round=rnd, ck_next=ii + 1, ck_tot=tot)) if (a or c or ii % 16 == 15) else None
        print(node, 'round', rnd, 'total entering', tot, flush=True)
        if tot == 0: break
    K.save(OD + '/CK_%s.json' % node, dict(status='RP6 RIG PILOT / NOT FROZEN', node=node, state=st, node_weight=w, body=bn, base_config=b['cfg'], state_layer='CF_state_%s.json' % st,
                                          semantics='creator key: S(T, w) = S(T) + h(w) K(T); stored at state scale (production contribution at the node = w * K)',
                                          composite=comp, fit_log=log, converged=bool(tot == 0), empty=bool(not K.F and not K.PK)))
    print(node, 'DONE converged', tot == 0, 'families', len(K.F), 'pose keys', len(K.PK), '%.0fs' % (time.time() - t0), flush=True)
