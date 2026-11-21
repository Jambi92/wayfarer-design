# sa6_muscle_validate.py OUT.json [BODIES] : rig v002 elbow muscle layer validation (order 07a3f24c §2, SAURIN-RP6-DEF-ELBOW-MUSCLE-1).
#   Bodies: base M (c1), base F (c2) and the heavy-body regression control states (default FAHI, MUFAHI, MUHI); the muscle families are rebuilt on
#   each rest body exactly as sa6_v2_init / sa6_muscle add do.  Per body, per arm, at elbow flexion 0 (neutral), 15, 30, 45, 60, 75, 90, 110, 130 deg and
#   145 deg (beyond the range: held), measured in rest space (the layer is a rest-space delta):
#     driver value / activation s, max |delta|, biceps rise (max outward radial displacement on the anterior side), triceps flattening (max inward on the
#     posterior side), the axial position of the biceps peak (t, 0 = GH, 1 = elbow: moves proximally = shortening), the closed-body volume change of the
#     layer alone at that pose (posed LBS + muscle vs posed LBS), and the locality checks: displacement on vertices outside the arm's region (must be 0),
#     on the cap zone t < 0.10 and the crease zone t > 0.93 (W = 0 there), on the other arm, and at the RP5 rigid landmarks.
#   Combined with the corrected shoulder: the same elbow angles under shoulder_abd90 and shoulder_flex60 / 90 (girdle coupled): the muscle driver and delta
#   must equal the elbow-only values (the driver is the forearm twist RELATIVE to the upper arm).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_muscle as MU
OUT = sys.argv[1]; BODIES = (sys.argv[2] if len(sys.argv) > 2 else 'M,F,FAHI,MUFAHI,MUHI').split(',')
ANG = [0, 15, 30, 45, 60, 75, 90, 110, 130, 145]
def body(nm):
    if nm in ('M', 'F'): return MU.state_rig(nm, None)
    return MU.state_rig(None, nm)
def run(nm):
    R = body(nm); fams = MU.families(R); Cr = CC.Correctives(R)
    for f in fams: Cr.F[CC.fam_key(f['bone'], f['axis'], 'muscle')] = f
    S = CC.Solver(R); d = C.load(); LMI = sorted({int(np.argmin(np.linalg.norm(R.V - p, axis=1))) for p in R.LM.values()}) if hasattr(R, 'LM') else []
    out = dict(body=nm, arms={})
    for f, t in zip(fams, 'lr'):
        side = 'xpos' if t == 'l' else 'xneg'; fr = MU.arm_frame(R, t); idx = MU.region(R, t, fr); tt, rh, c, rloc, W = MU.profiles(R, t, fr, idx)
        inreg = np.zeros(R.nv, bool); inreg[idx] = True; cap = idx[tt < 0.10]; crease = idx[tt > 0.93]
        other = MU.region(R, 'r' if t == 'l' else 'l', MU.arm_frame(R, 'r' if t == 'l' else 'l'))
        spec130 = R.suite('anat')['elbow_130_' + side]; rows = []
        for a in ANG:
            spec = SP.Rig.scaled(R, spec130, a / 130.0) if a else []; T = R.pose(spec); D = Cr.delta(T); x = Cr.driver(T, dict(bone=f['bone'], axis=f['axis'])) if a else 0.0
            rad = (D[idx] * rh).sum(1); P0 = R.skin(T); dv = S.body_volume(R.skin(T, R.V + D)) - S.body_volume(P0)
            pk = np.argmax(np.where(c > 0, rad, -np.inf))
            rows.append(dict(elbow_deg=a, driver=round(float(x), 4), activation=round(float(MU.smooth(x / fr['x130'])) if a else 0.0, 4),
                             max_delta_cm=round(float(np.linalg.norm(D, axis=1).max()), 4), biceps_rise_cm=round(float(max(0, rad[c > 0].max())), 4),
                             triceps_flatten_cm=round(float(max(0, -rad[c < 0].min())), 4), biceps_peak_t=round(float(tt[pk]), 3) if rad[pk] > 1e-6 else None,
                             dV_layer_cm3=round(float(dv), 3), outside_region_max_cm=float(np.linalg.norm(D[~inreg], axis=1).max()),
                             cap_zone_max_cm=float(np.linalg.norm(D[cap], axis=1).max()) if len(cap) else 0.0, crease_zone_max_cm=float(np.linalg.norm(D[crease], axis=1).max()) if len(crease) else 0.0,
                             other_arm_max_cm=float(np.linalg.norm(D[other], axis=1).max()), landmark_max_cm=float(np.linalg.norm(D[LMI], axis=1).max()) if LMI else None))
        comb = []
        for sh in ('shoulder_abd90_' + side, 'shoulder_flex60_' + side, 'shoulder_flex90_' + side):
            ssp = R.suite('anat').get(sh)
            if ssp is None:
                if sh.startswith('shoulder_flex90'):
                    b60 = R.suite('anat')['shoulder_flex60_' + side]; ssp = SP.Rig.scaled(R, b60, 1.5)
                else: continue
            for a in (45, 90, 130):
                T = R.pose(list(ssp) + SP.Rig.scaled(R, spec130, a / 130.0)); D = Cr.delta(T); T0 = R.pose(SP.Rig.scaled(R, spec130, a / 130.0)); D0 = Cr.delta(T0)
                comb.append(dict(shoulder=sh, elbow_deg=a, driver=round(float(Cr.driver(T, dict(bone=f['bone'], axis=f['axis']))), 4),
                                 driver_elbow_only=round(float(Cr.driver(T0, dict(bone=f['bone'], axis=f['axis']))), 4), max_diff_vs_elbow_only_cm=float(np.abs(D - D0).max())))
        bins = np.clip((tt * 20).astype(int), 0, 19); vol = float(sum(np.pi * np.median(np.linalg.norm((R.V[idx] - fr['H'])[bins == k] - np.outer((R.V[idx] - fr['H'])[bins == k] @ fr['u'], fr['u']), axis=1)) ** 2 * fr['L'] / 20 for k in range(20) if (bins == k).any()))
        out['arms'][t] = dict(params=f['layer_params'], upper_arm_volume_est_cm3=round(vol, 1), max_dV_pct_of_upper_arm=round(100 * max(abs(x['dV_layer_cm3']) for x in rows) / vol, 3), region_vertices=int(len(idx)), cap_zone_vertices=int(len(cap)), crease_zone_vertices=int(len(crease)), angles=rows, combined=comb)
    return out
res = dict(status='RP6 RIG PILOT / NOT FROZEN', rig_version=C.RIGV, order='07a3f24c §2', bodies=[run(b) for b in BODIES])
chk = []
for b in res['bodies']:
    for t, a in b['arms'].items():
        r = a['angles']; mono = all(r[i + 1]['biceps_rise_cm'] >= r[i]['biceps_rise_cm'] - 1e-9 for i in range(len(r) - 1))
        chk.append(dict(body=b['body'], arm=t, neutral_zero=r[0]['max_delta_cm'] == 0.0, local=max(x['outside_region_max_cm'] + x['other_arm_max_cm'] + x['cap_zone_max_cm'] + x['crease_zone_max_cm'] for x in r) < 1e-9,
                        landmarks_fixed=all((x['landmark_max_cm'] or 0) < 1e-9 for x in r), bounded=max(x['max_delta_cm'] for x in r) <= a['params']['max_delta_cm'] + 1e-6,
                        monotone_rise=mono, held_beyond_130=abs(r[-1]['max_delta_cm'] - r[-2]['max_delta_cm']) < 1e-6,
                        combined_independent=max(x['max_diff_vs_elbow_only_cm'] for x in a['combined']) < 1e-6 if a['combined'] else None,
                        volume_cm3_at_130=r[-2]['dV_layer_cm3'], max_dV_pct_of_upper_arm=a['max_dV_pct_of_upper_arm'], volume_within_1pct=a['max_dV_pct_of_upper_arm'] < 1.0))
res['checks'] = chk; res['pass'] = all(all(v for k, v in c.items() if isinstance(v, bool)) for c in chk)
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(chk, indent=1)); print('PASS' if res['pass'] else 'FAIL')
