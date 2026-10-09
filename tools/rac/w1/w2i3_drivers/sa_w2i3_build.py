# RAC W2I3 rebuilt-candidate bodies: the W2I body list rebuilt with sa_rebuild.build_r (clean L1 + F2 fields; optional caudal alpha), measured
# with the unchanged W2I measurement + J-2 limb readings (hip = pelvic station) + ledger; output format = sa_bodies.json so the accepted W2I
# evaluators (sa_compare.py, sa_eval.py) and the W2I2 limb evaluator (sa_w2i2_eval.py) run unchanged.
# Usage: python3 sa_w2i3_build.py CAND full|core OUT.json   (CAND: R = L1 + F2 rebuild; RC<n> adds caudal alpha)
import sys, os, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_rebuild as RB, sa_build as B, sa_joints as SJ, sa_cand as SC
sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers')); import sa_w2i2_build as WB
CANDS = {"AS": {}, "R": dict(RB.TARGET)}
if __name__ == '__main__':
    cname, sset, outp = sys.argv[1:4]; cand = CANDS[cname]; out = {}
    for bid, p, h, note in WB.ALL:
        if sset == 'core' and bid not in WB.CORE: continue
        P, q, k, info = RB.build_r(p, cand, h); M = B.measure(P, q, k); J, U = SC.joints_c(P); r = SJ.readings(P, J, M['height'])
        M['note'] = note; M['params'] = {a: b for a, b in p.items()}; M['cand'] = cname; M['cand_info'] = info
        M['limb'] = dict(mean=r['mean'], ratio=r['ratio'], shoulder_joint_breadth=r['shoulder_joint_breadth'], transport_control_max_cm=max(U.values()), joints={kk: v.tolist() for kk, v in J.items()})
        M['ledger'] = WB.ledger(M, J); out[bid] = M
        print(cname, bid, round(M['height'], 2), 'hip %.4f' % r['ratio']['leg_share'], 'fa/arm %.4f' % r['ratio']['forearm_over_arm'], 'd/w %.3f' % M['thorax_d_over_w'], flush=True)
    json.dump(out, open(outp, 'w'), indent=1, default=float)
