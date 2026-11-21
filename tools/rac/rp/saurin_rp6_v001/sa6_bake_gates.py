# sa6_bake_gates.py NAME BODYDIR ARTDIR [OUTDIR] (env GATES_ONLY, GATES_FRACS, GATES_TRANSITIONS=1, GATES_SHARD=i/n, GATES_CKPT) : RP6 special gates (sa6_gates.gate_poses: tail / hand / foot-toe / jaw-head, 50 poses) on a per-body bake
#   (per-body bake feasibility order a13cae71 §2 "rerun the applicable special gates").
#   The artifact ARTDIR/BK_<NAME>.json is reopened from disk.  Every gate pose at 25 / 50 / 75 / 100 % is gated with the SAME ownership rules and thresholds as
#   sa6_blend.evaluate (closure rules: rig-owned folds / contact / tears, |dV| <= 100 cm3 with jaw poses exempt, protected rigid set <= 0.05 cm) on the
#   'bake' column (= packaged blend v004 + K); 'lbs' is the ownership reference and 'prod' (packaged blend alone) is evaluated only where K is non-zero
#   on that pose (elsewhere bake == prod exactly; max |K| is recorded per pose).  At 100 % the special-gate metrics of the rig-pilot audit are recorded
#   for lbs and bake: tail ring-area ratio (min) and turning kink ratio (max), palm and foot volume ratio, sole down-facing fraction, head rigid error.
#   -> OUTDIR/GT_<NAME>.json  (OUTDIR defaults to ARTDIR)
import sys, os, json, time, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_common as C, sa6_correctives as CC, sa6_fit as FT, sa6_layer_harness as H, sa6_blend as BL, sa6_gates as GT
from scipy.spatial import cKDTree
from sa6_bake import peak_mb
FRACS = tuple(float(x) for x in os.environ.get('GATES_FRACS', '1.0,0.75,0.5,0.25').split(','))   # GATES_FRACS: dense between-sample check of a gate pose
def run(nm, BD, AD):
    t0 = time.time(); b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; art = os.path.join(AD, 'BK_%s.json' % nm)
    R, z = BL.rig_of(nm, b, BD); S = CC.Solver(R); S.V0 = S.body_volume(R.V); Q = R.Q
    Ft = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, Ft)
    Bc = H.load_base(R, b['cfg']); Pc = H.Blend(Bc, [(ws, H.load_state(R, s)[0]) for s, ws in b['w'].items()]); Kb = CC.Correctives.load(R, art)
    pts = z['pts']; kd = cKDTree(pts) if len(pts) else None; inv = z['rest_inverted']; compq = z['comp']; compv = np.zeros(R.nv, bool); compv[Q[compq].ravel()] = True
    Fn = np.r_[Q[~compq][:, [0, 1, 2]], Q[~compq][:, [0, 2, 3]]].astype(np.int64)
    def near(X): return (kd.query(X)[0] <= 1.0) if (kd is not None and len(X)) else np.zeros(len(X), bool)
    prot = BL.rigid_ids(b['cfg']); d = C.load(); rings = d['tail_rings']
    def ring_area(P, rg):
        X = P[rg] - P[rg].mean(0); n = np.linalg.svd(X)[2][-1]; return 0.5 * abs((np.cross(X, np.roll(X, -1, 0)) @ n).sum())
    A0 = np.array([ring_area(R.V, rg) for rg in rings])
    def turning(P):
        cen = np.array([P[rg].mean(0) for rg in rings]); dv = np.diff(cen, axis=0); dv /= np.linalg.norm(dv, axis=1, keepdims=True)
        return np.degrees(np.arccos(np.clip((dv[1:] * dv[:-1]).sum(1), -1, 1)))
    def kink(th):
        win = np.array([th[max(0, k - 5):k + 6].mean() for k in range(len(th))]); m = th > 0.2
        return float((th / np.maximum(win, 0.05))[m].max()) if m.any() else 1.0
    def sidev(t): c = R.V[Q].mean(1)[:, 0]; return c > 0 if t == 'l' else c < 0
    def vol(P, m, piv): a1, b1, c1, d1 = (P[Q[m, k]] - piv for k in range(4)); return (np.einsum('ij,ij->i', a1, np.cross(b1, c1)) + np.einsum('ij,ij->i', a1, np.cross(c1, d1))).sum() / 6
    def metrics(pn, T, P):
        g = {}
        if pn.startswith('tail'):
            g['tail_ring_area_ratio_min'] = round(float((np.array([ring_area(P, rg) for rg in rings[:-3]]) / A0[:-3]).min()), 4); g['tail_kink_ratio_max'] = round(kink(turning(P)), 3)
        for s_, t in (('xpos', 'l'), ('xneg', 'r')):
            if not pn.endswith(s_): continue
            if pn.startswith('hand'):
                hp = R.H('hand_' + t); m = np.isin(R.ql, ['palm']) & sidev(t); g['palm_volume_ratio'] = round(float(vol(P, m, T['hand_' + t][0] @ hp + T['hand_' + t][1]) / vol(R.V, m, hp)), 4)
            if any(x in pn for x in ('toe', 'ankle', 'foot')):
                ap = R.H('foot_' + t); m = np.isin(R.ql, ['foot', 'forefoot']) & sidev(t); g['foot_volume_ratio'] = round(float(vol(P, m, T['foot_' + t][0] @ ap + T['foot_' + t][1]) / vol(R.V, m, ap)), 4)
                sole = m & (R.V[Q].mean(1)[:, 2] < R.V[Q[m]].mean((0, 1))[2]); nz = np.cross(P[Q[sole, 2]] - P[Q[sole, 0]], P[Q[sole, 3]] - P[Q[sole, 1]])
                g['sole_down_facing_fraction'] = round(float((nz[:, 2] < 0).mean()), 4)
        if 'jaw' in pn or 'head' in pn:
            Rr, tr = T['head']; uj = R.W[:, R.bi['head']] > 0.999; g['upper_head_rigid_max_err_cm'] = round(float(np.linalg.norm(P[uj] - (R.V[uj] @ Rr.T + tr), axis=1).max()), 6)
        return g
    T0 = R.pose([]); neutral = float(np.abs(Pc.delta(T0) + Kb.delta(T0)).max())
    GP = GT.gate_poses(R); res = dict(name=nm, status='RP6 RIG PILOT / NOT FROZEN', artifact=os.path.abspath(art), artifact_sha256=C.sha(art), gate_set='sa6_gates.gate_poses (50 poses)',
                                      fractions=list(FRACS), neutral_bake_max_displacement_cm=neutral, poses={})
    only = os.environ.get('GATES_ONLY'); only = only.split(',') if only else None
    ck = os.environ.get('GATES_CKPT')   # per-pose checkpoint: a run cut off part-way resumes at the next pose (same artifact hash + fractions required)
    if ck and os.path.exists(ck):
        old = json.load(open(ck))
        if old.get('artifact_sha256') == res['artifact_sha256'] and old.get('fractions') == res['fractions']: res['poses'] = old['poses']; res['resumed_poses'] = len(old['poses'])
    SH = os.environ.get('GATES_SHARD'); si, sn = (int(x) for x in SH.split('/')) if SH else (0, 1)   # 'i/n': this process gates poses[i::n] (sa6_bake_gates_merge.py joins)
    TR = os.environ.get('GATES_TRANSITIONS') == '1'; res['transitions'] = TR   # + samples 0.25 deg either side of every K / packaged-blend family sample and K pose-key centre / tent edge
    FAM = list(Kb.F.values()) + [f for st in [Pc.B] + [s_ for _, s_ in Pc.S] for f in getattr(st, 'F', {}).values()]
    sel = [pn for pn in GP if not (only and pn not in only)]; res['shard'] = SH; res['shard_poses'] = sel[si::sn]; res['all_poses'] = sel
    for pn in sel[si::sn]:
        spec = GP[pn]
        if pn in res['poses']: continue
        vflag = not any('jaw' in e[0] for e in spec); res['poses'][pn] = {}; fset = set(FRACS)
        if TR:
            T1 = R.pose(spec)
            for f in FAM:                    # transitions as pose fractions; R.fracs_at inverts the coupled (v002) driver exactly
                if f['bone'] not in R.bones_of(spec): continue
                fset.update(round(x, 5) for x in R.fracs_at(spec, lambda T_: Kb.driver(T_, f), [s_ + e for s_ in f['samples'] for e in (-0.25, 0.25)], key=(f['bone'], tuple(f['axis']))))
            for k, pk in Kb.PK.items():
                if k.rsplit('@', 1)[0] not in (pn, 'gate:' + pn): continue
                dd = dict(bone=pk['drivers'][0][0], axis=pk['drivers'][0][1]); s_ = pk['drivers'][0][2]; w = (pk.get('width') or [abs(s_)])[0]
                fset.update(round(x, 5) for x in R.fracs_at(spec, lambda T_: Kb.driver(T_, dd), [c + e for c in (s_ - w, s_, s_ + w) for e in (-0.25, 0.25)], key=(dd['bone'], tuple(dd['axis']))))
        for fr in sorted((f for f in fset if 0 < f <= 1), reverse=True):
            T = R.pose([(bb, p, a, dg * fr) for bb, p, a, dg in spec]); dP = Pc.delta(T); dK = Kb.delta(T); km = float(np.abs(dK).max())
            cols = [('lbs', None), ('bake', dP + dK)] + ([('prod', dP)] if km > 0 else []); o = {}
            for tag, dl in cols:
                P = R.skin(T) if dl is None else R.skin(T, R.V + dl)
                f = np.nonzero(R.relcos(P, T) < 0)[0]; pen = np.nonzero(FT.penetration(R, P, Ft, w0))[0]; te = S.tear_edges(P)[0]
                o[tag] = dict(P=P, f=f, pen=pen, tears=S._E1[te], dV=(S.body_volume(P) - S.V0) if vflag else 0.0, dl=dl)
            lb = o['lbs']; row = dict(k_max_cm=round(km, 6))
            for tag in o:
                c = o[tag]
                cf = (near(R.V[Q[c['f']]].mean(1)) & np.isin(c['f'], lb['f'])) | inv[c['f']] if len(c['f']) else np.zeros(0, bool)
                cp = near(R.V[c['pen']]) & np.isin(c['pen'], lb['pen'])
                if (~cp).any() and compq.any():
                    rp = c['pen'][~cp]; q = c['P'][rp] - FT.PEN_TOL * igl.per_vertex_normals(c['P'], Ft)[rp]
                    own = compv[rp] & (igl.fast_winding_number(c['P'], Fn, q) < 1.5); cp[np.nonzero(~cp)[0][own]] = True
                ct = near(R.V[c['tears']].mean(1)) if len(c['tears']) else np.zeros(0, bool)
                if len(c['tears']): lt = {tuple(e) for e in np.sort(lb['tears'], 1)}; ct &= np.array([tuple(e) in lt for e in np.sort(c['tears'], 1)])
                row[tag] = dict(flips=int(len(c['f'])), composition=int(cf.sum()), rig_flips=int((~cf).sum()), new_pen=int(len(c['pen'])), rig_pen=int((~cp).sum()),
                                tears=int(len(c['tears'])), rig_tears=int((~ct).sum()), dV_cm3=round(float(c['dV']), 2), volume_ok=bool(abs(c['dV']) <= 100),
                                regions=sorted({str(R.ql[q_]) for q_ in c['f'][~cf]})[:6] if len(c['f']) else [])
            rig = float(np.linalg.norm(o['bake']['dl'][prot], axis=1).max()) if prot.any() else 0.0; row['bake']['rigid_max_cm'] = round(rig, 5)
            if abs(fr - 1.0) < 1e-9: row['metrics'] = dict(lbs=metrics(pn, T, o['lbs']['P']), bake=metrics(pn, T, o['bake']['P']))
            res['poses'][pn][('%.2f' % fr) if round(fr, 2) == fr else ('%.4f' % fr) if round(fr, 4) == fr else ('%.5f' % fr)] = row
        if ck: json.dump(res, open(ck + '.tmp', 'w')); os.replace(ck + '.tmp', ck)
    tot = dict(rig_flips=0, rig_pen=0, rig_tears=0, vol_fail=0, comp=0, lbs_rig=0, rigid_max_cm=0.0, poses_with_K=0, k_max_cm=0.0)
    for pn, rows in res['poses'].items():   # totals from the saved rows, so a resumed run totals exactly like an uninterrupted one
        for row in rows.values():
            pr = row['bake']; tot['rig_flips'] += pr['rig_flips']; tot['rig_pen'] += pr['rig_pen']; tot['rig_tears'] += pr['rig_tears']; tot['vol_fail'] += int(not pr['volume_ok'])
            tot['comp'] += pr['composition']; tot['lbs_rig'] += row['lbs']['rig_flips']; tot['rigid_max_cm'] = max(tot['rigid_max_cm'], pr['rigid_max_cm'])
        kp = max(r['k_max_cm'] for r in rows.values()); tot['poses_with_K'] += int(kp > 0); tot['k_max_cm'] = max(tot['k_max_cm'], kp)
    res['totals'] = tot; res['clean'] = not (tot['rig_flips'] or tot['rig_pen'] or tot['rig_tears'] or tot['vol_fail'] or tot['rigid_max_cm'] > 0.05 or neutral > 0)
    res['seconds'] = round(time.time() - t0, 1); res['peak_mb'] = round(peak_mb(), 1); return res
if __name__ == '__main__':
    nm, BD, AD = sys.argv[1:4]; OD = sys.argv[4] if len(sys.argv) > 4 else AD; os.makedirs(OD, exist_ok=True)
    SH = os.environ.get('GATES_SHARD'); tag = '.s%sof%s' % tuple(SH.split('/')) if SH else ''
    r = run(nm, BD, AD); json.dump(r, open(os.path.join(OD, 'GT_%s%s.json' % (nm, tag)), 'w'), indent=1); t = r['totals']
    ck = os.environ.get('GATES_CKPT')
    if ck and os.path.exists(ck): os.remove(ck)
    print('%-26s gates clean %s | rig flips %d pen %d tears %d volfail %d rigid %.4f | comp %d | K active on %d poses (max %.4f cm) | %.0fs %.0f MB' % (
        nm, r['clean'], t['rig_flips'], t['rig_pen'], t['rig_tears'], t['vol_fail'], t['rigid_max_cm'], t['comp'], t['poses_with_K'], t['k_max_cm'], r['seconds'], r['peak_mb']), flush=True)
