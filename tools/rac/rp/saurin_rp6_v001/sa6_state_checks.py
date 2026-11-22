# sa6_state_checks.py LAYERDIR OUT.json STATES : rig v002 pass-7 checks of the creator-state layers (order 07a3f24c §4), per state on its own rest body:
#   rigid   : max corrective displacement on the BASE configuration's protected set (sa6_correctives.base_protect; gate tolerance 0.05 cm), all 34 anatomical
#             poses and all 56 special gates at 0.5 / 0.75 / 1.0;
#   gates   : special gates at 0.25 / 0.5 / 0.75 / 1.0 -- folded quads outside the state's composition zone (sa6_pd2_fit.comp_mask), not inverted at rest,
#             and not already folded by plain LBS of the pose (the pd2 ownership screen) = rig-owned gate flips.  Expect 0 (the pass-7 fit includes the gates).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_pd2_fit as PF, sa6_correctives as CC, sa6_gates as G
LD, OUT, ST = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
res = json.load(open(OUT)) if os.path.exists(OUT) else dict(status='RP6 RIG PILOT / NOT FROZEN', layers=LD, states={})
for nm in ST:
    R, cfg = PF.state_rig(nm); K = CC.Correctives.load(R, '%s/CF_state_%s.json' % (LD, nm)); prot = CC.base_protect(cfg); cm = PF.comp_mask(nm, R)
    A = R.suite('anat'); GP = G.gate_poses(R); rig = (0.0, None); gflips = {}
    for kind, PS, FR in (('anat', A, (1.0, 0.75, 0.5)), ('gate', GP, (1.0, 0.75, 0.5, 0.25))):
        for pn, spec in PS.items():
            for fr in FR:
                T = R.pose(R.scaled(spec, fr)); P0 = R.skin(T); P = R.skin(T, R.V + K.delta(T))
                m = float(np.linalg.norm((P - P0)[prot], axis=1).max())
                if m > rig[0]: rig = (m, '%s:%s@%.2f' % (kind, pn, fr))
                if kind == 'gate':
                    f = (R.relcos(P, T) < 0) & ~cm & ~R.rest_inverted & ~(R.relcos(P0, T) < 0)
                    if f.any(): gflips['%s@%.2f' % (pn, fr)] = int(f.sum())
    res['states'][nm] = dict(rigid_max_cm=round(rig[0], 5), rigid_worst=rig[1], rigid_ok=rig[0] <= 0.05, gate_rig_flips=gflips, gates_clean=not gflips)
    json.dump(res, open(OUT, 'w'), indent=1); print(nm, 'rigid %.4f' % rig[0], rig[1], 'gate flips', sum(gflips.values()), gflips, flush=True)
