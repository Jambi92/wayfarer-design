# RAC W2I5 final-asset bodies: the W2I body list built with sa_sculpt.build_s (W2I3 L1 + F2 rebuild + W2I4 finish delta + W2I5 thigh sculpt delta), measured
# with the unchanged W2I measurement + J-2 limb readings (hip = pelvic station) + ledger; output format = sa_bodies.json so the accepted W2I
# evaluators (sa_compare.py, sa_eval.py) and the W2I2 limb evaluator (sa_w2i2_eval.py) run unchanged.
# Usage: python3 sa_w2i5_build.py full|core OUT.json
import sys, os, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN; _BUILD4 = FN.build_f; FN.build_f = SC5.build_s   # W2I5: final route = W2I4 route + W2I5 sculpt delta
RB = FN.RB; B = FN.B
import sa_joints as SJ, sa_cand as SC
sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers')); import sa_w2i2_build as WB
if __name__ == '__main__':
    sset, outp = sys.argv[1:3]; out = {}
    for bid, p, h, note in WB.ALL:
        if sset == 'core' and bid not in WB.CORE: continue
        P, q, k, info = FN.build_f(p, h); M = B.measure(P, q, k); J, U = SC.joints_c(P); r = SJ.readings(P, J, M['height'])
        M['note'] = note; M['params'] = {a: b for a, b in p.items()}; M['cand'] = 'W2I5-final'; M['cand_info'] = info
        M['limb'] = dict(mean=r['mean'], ratio=r['ratio'], shoulder_joint_breadth=r['shoulder_joint_breadth'], transport_control_max_cm=max(U.values()), joints={kk: v.tolist() for kk, v in J.items()})
        M['ledger'] = WB.ledger(M, J); out[bid] = M
        print(bid, round(M['height'], 2), 'hip %.4f' % r['ratio']['leg_share'], 'fa/arm %.4f' % r['ratio']['forearm_over_arm'], 'd/w %.3f' % M['thorax_d_over_w'], flush=True)
    json.dump(out, open(outp, 'w'), indent=1, default=float)
