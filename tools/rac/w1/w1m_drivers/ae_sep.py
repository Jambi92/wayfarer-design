# RAC W1m: what separates Aelari (AEL1 candidate) from each population at the measurement layer: % difference of AE from each body
# on the elongation shares, thorax, joints, hand/foot, face verticality and head height share. Report only (no new pass rows).
import json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; G = S + '/w1g'
L = lambda p: json.load(open(p))["combined"]
B = {"AE (AEL1)": L(S + '/w1m/legs/AEL1_meas.json'), "MF-M-R": L(G + '/cand/MF-M-R_meas.json'), "SG": L(G + '/cand/SG_meas.json'), "FN": L(G + '/cand/FN_meas.json'),
     "VA": L(G + '/cand/VA_meas.json'), "SK": L(G + '/cand/SK_meas.json'), "GR (accepted W1l)": L(S + '/w1l/probe/GRL925_1200_meas.json')}
R = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "hand_share", "foot_share", "thorax_depth_share", "thorax_breadth_share",
     "elbow_over_humerus", "wrist_over_forearm", "knee_over_femur", "palm_breadth_over_hand"]
val = lambda b, k: B[b]["cranio"]["FVB"] if k == "FVB" else B[b]["ratio"][k]
out = {"stature": {b: B[b]["stature"] for b in B}, "values": {b: {k: val(b, k) for k in R + ["FVB"]} for b in B}, "pct_AE_vs": {}}
for b in B:
    if b.startswith("AE"): continue
    out["pct_AE_vs"][b] = {k: 100 * (val("AE (AEL1)", k) / val(b, k) - 1) for k in R + ["FVB"]}
json.dump(out, open('/home/claude/wayfarer-design/reviews/rac-w1m-ae-evidence/separation.json', 'w'), indent=1)
print('%-22s' % 'AE % vs' + ''.join('%11s' % b[:10] for b in out["pct_AE_vs"]))
for k in R + ["FVB"]: print('%-22s' % k + ''.join('%+10.1f%%' % out["pct_AE_vs"][b][k] for b in out["pct_AE_vs"]))
