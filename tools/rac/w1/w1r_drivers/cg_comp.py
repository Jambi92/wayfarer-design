# RAC W1r: Cogling continuity readings, composition bodies, and separation (% difference of CG from normalized MF, accepted PK / FN / GR,
# unaccepted DU, the diagnostic Narrow DU, and the 91 cm generator human-child proxy). Report only. CG = the W1r candidate CGJ7.
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R, Q, F, G = S + '/w1r', S + '/w1q', S + '/w1f', S + '/w1g'
EV = '/home/claude/wayfarer-design/reviews/rac-w1r-cg-evidence'
B = {"CG central (W1r candidate CGJ7)": R + '/probe/CGJ7_rest.npz', "CG as built (CG-NAT)": F + '/final/CG-NAT_rest.npz', "CG minimum composition (CGJ7)": R + '/cgj7/lean/CG-NAT-LEAN_rest.npz',
     "CG Narrow (breadth only)": R + '/frame7_NARROWB/final/CG-NAT_rest.npz', "CG Broad (breadth only, pelvis x1.12)": R + '/frame7_BROADB_P112/final/CG-NAT_rest.npz',
     "CG low (0.25 / 0.25)": R + '/comp/CG-LOW_rest.npz', "CG low muscle (0 / 0.5)": R + '/comp/CG-LOWMUS_rest.npz', "CG high muscle (1 / 0.5)": R + '/comp/CG-HIMUS_rest.npz',
     "CG higher fat (0.5 / 1)": R + '/comp/CG-HIFAT_rest.npz', "CG high muscle + fat (1 / 1)": R + '/comp/CG-HIBOTH_rest.npz',
     "PK central (accepted PK-NAT)": F + '/final/PK-NAT_rest.npz', "PK Narrow (breadth only)": Q + '/frame_NARROWB/final/PK-NAT_rest.npz',
     "DU (DU-NAT, unaccepted)": F + '/final/DU-NAT_rest.npz', "DU Narrow (diagnostic)": Q + '/du_NARROWB/final/DU-NAT_rest.npz',
     "Human child proxy (91 cm, generator age ~3 y)": R + '/child/CHILD3_rest.npz', "MF-M-R": F + '/final/MF-M-R_rest.npz',
     "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "MF-M-R minimum composition": F + '/final_lean/MF-M-R-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    if not os.path.exists(p): print('missing', k, p); continue
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-46s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
L = lambda p: json.load(open(p))["combined"]
M = {"CG (W1r CGJ7)": L(R + '/probe/CGJ7_meas.json'), "CG as built": L(G + '/cand/CG-NAT_meas.json'), "MF-M-R": L(G + '/cand/MF-M-R_meas.json'), "PK (accepted)": L(G + '/cand/PK-NAT_meas.json'),
     "FN (accepted FNL4)": L(S + '/w1p/cand/FNL4_meas.json'), "GR (accepted W1l)": L(S + '/w1l/probe/GRL925_1200_meas.json'), "DU (unaccepted)": L(G + '/cand/DU-NAT_meas.json'),
     "DU Narrow (diagnostic)": L(Q + '/du_NARROWB/final/DU-NAT_meas.json'), "Child proxy 91 cm (diagnostic)": L(R + '/child/CHILD3_meas.json')}
K = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "hand_over_arm", "femur_over_leg", "shin_over_leg", "hand_share",
     "finger_over_palm", "foot_share", "thorax_depth_share", "thorax_breadth_share", "pelvic_vertical_over_thoracic_vertical", "pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth",
     "waist_interval_over_torso"]
v = lambda b, k: M[b]["cranio"]["FVB"] if k == "FVB" else M[b]["ratio"][k]
sep = {"stature": {b: M[b]["stature"] for b in M}, "values": {b: {k: v(b, k) for k in K + ["FVB"]} for b in M},
       "pct_CG_vs": {b: {k: 100 * (v("CG (W1r CGJ7)", k) / v(b, k) - 1) for k in K + ["FVB"]} for b in M if not b.startswith("CG (")}}
json.dump(sep, open(EV + '/separation.json', 'w'), indent=1)
print('%-30s' % 'CG % vs' + ''.join('%11s' % b[:10] for b in sep["pct_CG_vs"]))
for k in K + ["FVB"]: print('%-30s' % k + ''.join('%+10.1f%%' % sep["pct_CG_vs"][b][k] for b in sep["pct_CG_vs"]))
