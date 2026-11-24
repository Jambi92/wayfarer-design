# sa6_pleat_audit.py measure KIND NAME CORR|pkg OUT.npz   |   compare BASELINE.npz NEW.npz OUT.json
#   Hidden-pleat audit (rig v002, order 07a3f24c §4 "check other unaffected systems for regressions").  The quad-flip gate (relcos < 0) cannot see a pleat:
#   two neighbouring quads rotated to opposite sides of the rest-rotated normal, both just short of flipping (found on base v003: ankle_dorsi20 relcos 0.15,
#   posed dihedral 179 deg where v001 has 8 deg; toes, tail root, pelvis, thumb likewise).
#   measure: per quad edge, |posed dihedral - rest dihedral| (deg) for the 34 anatomical poses and all special gates at 0.25 / 0.5 / 0.75 / 1.0
#     (PLEAT_FRACS; the pass-8 audit used 0.5 and 1.0 and missed a pleat at 0.75, found by the pass-9 fit).
#     KIND base  : NAME = M | F, CORR = correctives json (or 'pkg' = the packaged base of the active rig version)
#     KIND state : NAME = creator state, CORR = CF_state json (or 'pkg' = the packaged state set of the active rig version / layer package)
#     KIND body  : NAME = creator body, CORR = bodies dir (sa6_blend bodies.json): the packaged blend (knots included) of the active package
#     Run once per rig version (RP6_RIG unset = archived rig v001 = the accepted baseline).
#   compare: PLEAT = edge change > 90 deg.  Per pose / fraction: pleats on edges dominated by the corrected systems (clavicle / upperarm / forearm,
#     reported for visual review) and on every other edge (must not exceed the baseline count: a new pleat outside the corrected systems is a regression).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ARM = ('clavicle_', 'upperarm_', 'forearm_')
LIM = 90.0
FRS = tuple(float(x) for x in os.environ.get('PLEAT_FRACS', '0.25,0.5,0.75,1.0').split(','))   # pass 9: all four fit fractions (pass 8 audit: 0.5, 1.0)
if sys.argv[1] == 'measure':
    import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_layer_harness as H, sa6_gates as GT
    kind, nm, corr, OUT = sys.argv[2:6]
    if kind == 'base':
        R = SP.Rig(nm, C.w_path(nm, H.PKG)); K = H.load_base(R, nm) if corr == 'pkg' else CC.Correctives.load(R, corr)
    elif kind == 'body':      # NAME = creator body (e.g. a knot body c1-MUFAHI@0.25), CORR = bodies dir: the packaged blend of the active package (base + layers + knots)
        import json as _j, sa6_blend as BL
        b = _j.load(open(os.path.join(corr, 'bodies.json')))['bodies'][nm]; R, _ = BL.rig_of(nm, b, corr)
        K = H.Blend(H.load_base(R, b['cfg']), [(ws, H.load_state(R, s_)[0]) for s_, ws in b['w'].items()])
    else:
        import sa6_pd2_fit as PF
        R, cfg = PF.state_rig(nm); K = H.load_state(R, nm)[0] if corr == 'pkg' else CC.Correctives.load(R, corr)
    Q = R.Q; E = {}
    for qi, q in enumerate(Q):
        for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)): E.setdefault((min(q[a], q[b]), max(q[a], q[b])), []).append(qi)
    pr = np.array([v for v in E.values() if len(v) == 2]); ev = np.array([k for k, v in E.items() if len(v) == 2])
    def dih(P):
        n = np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        return np.degrees(np.arccos(np.clip((n[pr[:, 0]] * n[pr[:, 1]]).sum(1), -1, 1)))
    d0 = dih(R.V); PS = dict(R.suite('anat')); PS.update({'gate:' + k: v for k, v in GT.gate_poses(R).items()})
    names, X = [], []
    for pn, spec in PS.items():
        for fr in FRS:
            T = R.pose(R.scaled(spec, fr)); P = R.skin(T, R.V + K.delta(T)); names.append('%s@%.2f' % (pn, fr)); X.append(np.abs(dih(P) - d0).astype(np.float16))
    dom = R.W[ev].mean(1).argmax(1)
    np.savez_compressed(OUT, names=np.array(names), X=np.stack(X), arm=np.array([R.DB[i].startswith(ARM) for i in dom]), ev=ev, rigv=C.RIGV, kind=kind, name=nm, corr=corr)
    print(kind, nm, C.RIGV, 'measured', len(names), flush=True)
else:
    A, B, OUT = np.load(sys.argv[2]), np.load(sys.argv[3]), sys.argv[4]
    assert (A['ev'] == B['ev']).all(), 'topology differs'
    ia = {n: i for i, n in enumerate(A['names'])}; arm = B['arm']; rows = {}; bad = {}
    for i, n in enumerate(B['names']):
        if n not in ia: continue
        xa, xb = A['X'][ia[n]].astype(float), B['X'][i].astype(float)
        r = dict(other_baseline=int(((xa > LIM) & ~arm).sum()), other_new=int(((xb > LIM) & ~arm).sum()), arm_baseline=int(((xa > LIM) & arm).sum()), arm_new=int(((xb > LIM) & arm).sum()))
        if any(r.values()): rows[n] = r
        if r['other_new'] > r['other_baseline']: bad[n] = r
    res = dict(status='RP6 RIG PILOT / NOT FROZEN', tool='sa6_pleat_audit.py', pleat_deg=LIM, baseline=dict(rig=str(A['rigv']), kind=str(A['kind']), name=str(A['name']), corr=str(A['corr'])),
               new=dict(rig=str(B['rigv']), kind=str(B['kind']), name=str(B['name']), corr=str(B['corr'])), poses_measured=len(B['names']),
               regressions_outside_corrected_systems=bad, clean=not bad, poses_with_pleats=rows)
    json.dump(res, open(OUT, 'w'), indent=1); print(B['name'], 'clean' if not bad else 'REGRESSION %d poses' % len(bad), {k: v for k, v in list(bad.items())[:6]}, flush=True)
