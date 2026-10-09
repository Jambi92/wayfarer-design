# RAC W2I2 candidate bodies: the W2I body list (sa_build.BODIES + the 173 / 178 / 181 / 190 matched statures) rebuilt with one candidate
# (sa_cand.build_c) and measured with the unchanged W2I measurement (sa_build.measure), plus J-2 limb readings (sa_joints.readings on the
# candidate joints, hip = pelvic station) and the vertical ledger. Output keys / format match sa_bodies.json so the accepted W2I evaluators
# (sa_compare.py, sa_eval.py) run on it unchanged. SET = core | full.  Usage: python3 sa_w2i2_build.py CAND SET OUT.json
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_cand as SC, sa_build as B, sa_joints as SJ
CANDS = {"AS": {}, "L1": {"G": 9.2}, "L2": {"G": 10.3}, "L3": {"G": 11.6}, "F1": {"fa_delta": 2.2}, "F2": {"fa_delta": 4.2}, "F3": {"fa_delta": 5.0}}
for k in list(CANDS):
    if k.startswith("L"): CANDS[k]["FT"] = 0.4
def combo(c): return {**CANDS[c.split('+')[0]], **CANDS[c.split('+')[1]]} if '+' in c else CANDS[c]
EXTRA = [("SA-%s%d" % (sx, h), p, float(h), "matched-height comparison stature") for h in (173, 178, 181, 190) for sx, p in (("M", {}), ("F", B.CEN))]
ALL = [b for b in B.BODIES] + EXTRA
CORE = {"SA-M%d" % h for h in (168, 173, 178, 181, 188, 190, 203, 208)} | {"SA-F%d" % h for h in (168, 173, 178, 181, 188, 190, 203, 208)} | \
       {"SA-M168-LT90", "SA-F168-LT90", "SA-M203-LT90", "SA-F203-LT90", "SA-M208-B", "SA-M208-B-MUHI", "SA-M208-B-MUFAHI", "SA-M188-N", "SA-M188-B"}
def ledger(M, J):
    H = M['height']; a = 0.5 * (J['AL'][2] + J['AR'][2]); kn = 0.5 * (J['KL'][2] + J['KR'][2]); hb = 0.5 * (J['HBL'][2] + J['HBR'][2]); chin = H - M['head_depth']
    seg = {"ground_ankle": a, "ankle_knee": kn - a, "knee_hip_station": M['u_hip'] - kn, "lower_axial_trunk": M['u_costal'] - M['u_hip'], "thoracic": M['u_inlet'] - M['u_costal'],
           "neck": chin - M['u_inlet'], "head_height": M['head_depth']}
    return dict(cm=seg, share={k: v / H for k, v in seg.items()}, B1_axis_hip_share=hb / H, sum_check=sum(seg.values()) - H)
if __name__ == '__main__':
    cname, sset, outp = sys.argv[1:4]; cand = combo(cname); out = {}
    for bid, p, h, note in ALL:
        if sset == 'core' and bid not in CORE: continue
        P, q, k, info = SC.build_c(p, cand, h); M = B.measure(P, q, k); J, U = SC.joints_c(P); r = SJ.readings(P, J, M['height'])
        M['note'] = note; M['params'] = {a: b for a, b in p.items()}; M['cand'] = cname; M['cand_info'] = info
        M['limb'] = dict(mean=r['mean'], ratio=r['ratio'], shoulder_joint_breadth=r['shoulder_joint_breadth'], transport_control_max_cm=max(U.values()),
                         joints={kk: v.tolist() for kk, v in J.items()})
        M['ledger'] = ledger(M, J); out[bid] = M
        print(cname, bid, round(M['height'], 2), 'hip %.4f' % r['ratio']['leg_share'], 'LT %.2f' % M['lower_trunk_costal_hip'], 'TV/H %.4f' % M['thoracic_vertical_over_H'],
              'fa/arm %.4f' % r['ratio']['forearm_over_arm'], 'd/w %.3f' % M['thorax_d_over_w'], flush=True)
    json.dump(out, open(outp, 'w'), indent=1, default=float)
