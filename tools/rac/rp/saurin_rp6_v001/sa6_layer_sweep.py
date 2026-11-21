# sa6_layer_sweep.py OUTDIR : driver-transition and creator-weight sweeps (corrective-layer validation order 3e76b509, "Driver transitions").
#   ANGLE SWEEPS on the most demanding cases: the pose fraction runs 0 -> 1 -> 0 in 2 % steps (forward + return), plus samples 0.25 deg either side of
#   every corrective family sample angle of the driving joints (the hat-interpolation knots) and of every pose-key driver sample.  Per sample: production
#   gates (folds / new contact / tears / |dV|, closure ownership) and the corrective displacement; continuity = the largest per-vertex change of the
#   production corrective between neighbouring samples, normalised per degree, compared with the median; the return sweep must reproduce the forward
#   sweep exactly (the rig is stateless).
#   WEIGHT SWEEPS: the creator weight of a path runs 0 -> 1 in 0.05 steps (stateless: a return sweep repeats the same bodies) at a fixed full-angle pose; the body, joints and blended correctives are
#   rebuilt at every weight (geometry method of sa6_blend.py); same gates and continuity metric (per 0.05 weight).
import os, sys, json, time, numpy as np, igl
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT, sa6_layer_harness as H, sa6_blend as BL, sa6_pd2_fit as PF
OD = sys.argv[1]; os.makedirs(OD, exist_ok=True)
ANGLE_CASES = [('END_MUFAHI', 'hip_flex70_xpos'), ('END_MUHI', 'elbow_130_xneg'), ('END_FAHI', 'trunk_twist_30'), ('END_MUFAHI', 'shoulder_flex60_xneg'),
               ('MIX1', 'shoulder_abd90_xneg'), ('c1-MUFAHI@0.50', 'hip_flex70_xpos'), ('END_M208-B', 'fist_xpos'), ('T55-T80@0.50', 'tail_root_lateral_30'),
               ('c2-F-N@0.50', 'knee_90_xpos'), ('END_DSP-HIGH', 'jaw_open_20')]
WEIGHT_CASES = [('c1 -> MUFAHI', 'M', lambda t: {'MUFAHI': t}, 'hip_flex70_xpos'), ('MUHI -> FAHI', 'M', lambda t: {'MUHI': 1 - t, 'FAHI': t}, 'elbow_130_xneg'),
                ('c1 -> MUHI', 'M', lambda t: {'MUHI': t}, 'shoulder_abd90_xneg'), ('c2 -> F-N', 'F', lambda t: {'F-N': t}, 'hip_flex70_xneg'),
                ('T55 -> T80', 'M', lambda t: {'T55': 1 - t, 'T80': t}, 'tail_root_lateral_30')]
d = C.load(); z = PF.z; w = PF.w; F = PF.Fd
VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float)
def fn(P): return np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
nR = fn(VR); aR = np.linalg.norm(nR, axis=1); P0 = (z['bc'][:, :, None] * VR[F[z['tri']]]).sum(1); Q = d['Q']; q0 = np.cross(P0[Q[:, 2]] - P0[Q[:, 0]], P0[Q[:, 3]] - P0[Q[:, 1]])
DEN = {}
def dense(n):
    if n not in DEN: DEN[n] = (w['v_M'] if n == 'M' else w['v_F'] if n == 'F' else np.load(C.W + '/cr_%s.npy' % n)).astype(float)
    return DEN[n]
def body(cfg, wts):
    VB = dense(cfg) * (1 - sum(wts.values()))
    for s, x in wts.items(): VB = VB + x * dense(s)
    nB = fn(VB); aB = np.linalg.norm(nB, axis=1); bad = ((nR * nB).sum(1) / (aR * aB + 1e-20) < 0) | (aB < 0.05 * aR)
    Vs = (z['bc'][:, :, None] * VB[F[z['tri']]]).sum(1); nfl = (q0 * np.cross(Vs[Q[:, 2]] - Vs[Q[:, 0]], Vs[Q[:, 3]] - Vs[Q[:, 1]])).sum(1) < 0
    pts = np.r_[VB[F[bad]].mean(1) if bad.any() else np.zeros((0, 3)), Vs[Q[nfl]].mean(1) if nfl.any() else np.zeros((0, 3))]
    comp = cKDTree(pts).query(Vs[Q].mean(1))[0] <= 1.0 if len(pts) else np.zeros(len(Q), bool)
    R = SP.Rig(cfg, C.w_path(cfg, H.PKG)); J, M_ = SK.build(Vs, 'state'); R.V = Vs; R.P = SK.rec(J, M_, 'sweep'); R.n0 = R.qn(Vs); R.cfg = 'state'
    B = H.load_base(R, cfg); P = H.Blend(B, [(x, H.load_state(R, s)[0]) for s, x in wts.items()])
    return R, P, B, dict(pts=pts, comp=comp, inv=nfl)
class Gate:
    def __init__(s, R, own):
        s.R = R; s.S = CC.Solver(R); s.V0 = s.S.body_volume(R.V); s.Ft = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); s.w0 = FT.wn_out(R.V, s.Ft)
        s.kd = cKDTree(own['pts']) if len(own['pts']) else None; s.inv = own['inv']; s.compq = own['comp']; s.compv = np.zeros(R.nv, bool); s.compv[R.Q[s.compq].ravel()] = True
        s.Fn = np.r_[R.Q[~s.compq][:, [0, 1, 2]], R.Q[~s.compq][:, [0, 2, 3]]].astype(np.int64)
    def near(s, X): return (s.kd.query(X)[0] <= 1.0) if (s.kd is not None and len(X)) else np.zeros(len(X), bool)
    def __call__(s, T, dl, vol=True):
        R = s.R; out = {}
        for tag, dd in (('lbs', None), ('prod', dl)):
            P = R.skin(T) if dd is None else R.skin(T, R.V + dd); f = np.nonzero(R.relcos(P, T) < 0)[0]; pen = np.nonzero(FT.penetration(R, P, s.Ft, s.w0))[0]; te = s.S.tear_edges(P)[0]
            out[tag] = (P, f, pen, s.S._E1[te], (s.S.body_volume(P) - s.V0) if vol else 0.0)
        P, f, pen, tears, dV = out['prod']; _, lf, lpen, ltears, _ = out['lbs']
        cf = ((s.near(R.V[R.Q[f]].mean(1)) & np.isin(f, lf)) | s.inv[f]) if len(f) else np.zeros(0, bool); cp = s.near(R.V[pen]) & np.isin(pen, lpen)
        if (~cp).any() and s.compq.any():
            rp = pen[~cp]; q = P[rp] - FT.PEN_TOL * igl.per_vertex_normals(P, s.Ft)[rp]; own = s.compv[rp] & (igl.fast_winding_number(P, s.Fn, q) < 1.5); cp[np.nonzero(~cp)[0][own]] = True
        ct = s.near(R.V[tears].mean(1)) if len(tears) else np.zeros(0, bool)
        if len(tears): lt = {tuple(e) for e in np.sort(ltears, 1)}; ct &= np.array([tuple(e) in lt for e in np.sort(tears, 1)])
        return dict(rig_flips=int((~cf).sum()), composition=int(cf.sum()), rig_pen=int((~cp).sum()), rig_tears=int((~ct).sum()), dV=round(float(dV), 2), vol_ok=bool(abs(dV) <= 100))
def summarise(xs, ds, rows, unit):
    steps = [float(np.linalg.norm(ds[i + 1] - ds[i], axis=1).max()) / max(abs(xs[i + 1] - xs[i]), 1e-9) for i in range(len(xs) - 1) if xs[i + 1] != xs[i]]
    med = float(np.median(steps)) if steps else 0.0; mx = max(steps) if steps else 0.0
    return dict(samples=len(xs), continuity=dict(unit=unit, max_rate_cm=round(mx, 5), median_rate_cm=round(med, 5), max_over_median=round(mx / med, 2) if med > 0 else None),
                gate_fail_samples=[r for r in rows if r['rig_flips'] or r['rig_pen'] or r['rig_tears'] or not r['vol_ok']],
                max_rig=dict(flips=max(r['rig_flips'] for r in rows), pen=max(r['rig_pen'] for r in rows), tears=max(r['rig_tears'] for r in rows), max_abs_dV=max(abs(r['dV']) for r in rows)))
res = dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_layer_sweeps_v001', method=open(__file__).read().split('import os')[0], angle={}, weight={})
bm = json.load(open(os.path.join(os.environ.get('BODYDIR', '/tmp/claude-0/rp6/blend_bodies'), 'bodies.json')))['bodies']
for bn, pn in ANGLE_CASES:
    t0 = time.time(); b = bm[bn]; R, P, B, own = body(b['cfg'], b['w']); g = Gate(R, own); spec = R.suite('anat')[pn]; mx = max(abs(e[3]) for e in spec); vol = not any('jaw' in e[0] for e in spec)
    knots = set(); bs = R.bones_of(spec)
    if C.RIGV == 'v001':          # historical: driver = |total| angle
        for f in P.B.F.values():
            if any(f['bone'] == e[0] for e in spec): knots |= {abs(sv) for sv in f['samples']}
        for _, s_ in P.S:
            for f in s_.F.values():
                if any(f['bone'] == e[0] for e in spec): knots |= {abs(sv) for sv in f['samples']}
            for k in s_.PK.values():
                for b_, _, sv in k['drivers']:
                    if any(b_ == e[0] for e in spec): knots.add(abs(sv))
        kf = {round((k + e) / mx, 6) for k in knots for e in (-0.25, 0.25) if 0 <= (k + e) / mx <= 1}
    else:                         # v002: transitions inverted through the coupled rig (R.fracs_at), both signs of every sample
        kf = set(); dv = CC.Correctives(R)
        fams = list(P.B.F.values()) + [f for _, s_ in P.S for f in s_.F.values()] + [dict(bone=b_, axis=a_, samples=[sv]) for _, s_ in P.S for k in s_.PK.values() for b_, a_, sv in k['drivers']]
        for f in fams:
            if f['bone'] in bs: kf |= {round(x, 6) for x in R.fracs_at(spec, lambda T_: dv.driver(T_, f), [sg * abs(sv) + e for sv in f['samples'] for sg in (-1, 1) for e in (-0.25, 0.25)], key=(f['bone'], tuple(f['axis']))) if 0 <= x <= 1}
    fr = sorted({round(i * 0.02, 4) for i in range(51)} | kf)
    seq = fr + fr[::-1]; ds = []; rows = []
    for x in seq:
        T = R.pose([(b_, p, a, dg * x) for b_, p, a, dg in spec]); dl = P.delta(T); ds.append(dl); rows.append(dict(frac=x, **g(T, dl, vol)))
    n = len(fr); rev_ok = all(np.array_equal(ds[i], ds[2 * n - 1 - i]) for i in range(n))
    sm = summarise([x * mx for x in fr], ds[:n], rows, 'degree'); sm.update(pose=pn, body=bn, weights=b['w'], knots_deg=sorted(knots), return_sweep_identical=rev_ok, seconds=round(time.time() - t0))
    res['angle']['%s|%s' % (bn, pn)] = sm
    print('ANGLE', bn, pn, 'samples', len(seq), 'fails', len(sm['gate_fail_samples']), 'max rig', sm['max_rig'], 'continuity', sm['continuity'], 'return identical', rev_ok, '%.0fs' % (time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(OD, 'SA_RP6_layer_sweeps_v001.json'), 'w'), indent=1)
for name, cfg, wf, pn in WEIGHT_CASES:
    t0 = time.time(); ts = [round(i * 0.05, 4) for i in range(21)]; ds = {}; rows = []
    for t in ts:
        R, P, B, own = body(cfg, {k: v for k, v in wf(t).items() if v > 0}); g = Gate(R, own); spec = R.suite('anat')[pn]; T = R.pose(spec)
        dl = P.delta(T); ds[t] = dl; rows.append(dict(weight=t, **g(T, dl, not any('jaw' in e[0] for e in spec))))
    sm = summarise(ts, [ds[t] for t in ts], rows, '1.0 creator weight'); sm.update(path=name, pose=pn, note='forward sweep only: body, joints and correctives are a pure function of the weights (stateless), so a return sweep repeats the same samples', seconds=round(time.time() - t0))
    res['weight'][name + '|' + pn] = sm
    print('WEIGHT', name, pn, 'fails', len(sm['gate_fail_samples']), 'max rig', sm['max_rig'], 'continuity', sm['continuity'], '%.0fs' % (time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(OD, 'SA_RP6_layer_sweeps_v001.json'), 'w'), indent=1)
print('SWEEPS DONE')
