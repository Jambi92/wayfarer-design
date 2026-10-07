# RAC W1p: Fenn continuity readings, same-composition low check (FN low vs MF-M-R-LOW / SK-LOW), separation (% difference of FNL4
# from MF, SG, accepted AE (AEL1), accepted VA (VAL4), SK, accepted GR) and the elf-family chain table. Diagnostic / report only.
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, w1e_checks as WC
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; P, F, G = S + '/w1p', S + '/w1f', S + '/w1g'
EV = '/home/claude/wayfarer-design/reviews/rac-w1p-fn-evidence'
B = {"FN FNL4 candidate": P + '/cand/FNL4_rest.npz', "FN as built (W1g)": G + '/final/FN_rest.npz', "FN FNL4 minimum composition": P + '/fnl4/lean/FN-LEAN_rest.npz',
     "FN Narrow (breadth only)": P + '/frame_NARROWB/final/FN_rest.npz', "FN Broad (breadth only, pelvis x1.12)": P + '/frame_BROADB_P112/final/FN_rest.npz',
     "FN low (0.25 / 0.25)": P + '/comp/FN-LOW_rest.npz', "AE AEL1 (accepted)": S + '/w1m/legs/AEL1_rest.npz', "VA VAL4 (accepted)": S + '/w1n/cand/VAL4_rest.npz',
     "MF-M-R": F + '/final/MF-M-R_rest.npz', "SG": F + '/final/SG_rest.npz', "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz',
     "MF-M-R minimum composition": F + '/final_lean/MF-M-R-LEAN_rest.npz', "SG minimum composition": F + '/final_lean/SG-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items(): out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-36s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
tmp = P + '/cand_lowpair'
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("FN", P + '/comp/FN-LOW_meas.json'), ("MF-M-R", F + '/low/MF-M-R-LOW_meas.json'), ("SK", F + '/low/SK-LOW_meas.json')): shutil.copy(src, tmp + '/%s_meas.json' % slot)
out["low_same_composition_skin"] = [r for r in WC.run(tmp) if r.get('cand') == 'FN' and r.get('b') in ('MF', 'MF-M-R', 'SK')]
for r in out["low_same_composition_skin"]: print(r['check'], round(r['va'], 4), r['op'], round(r['vb'], 4), r['result'])
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
L = lambda p: json.load(open(p))["combined"]
M = {"FN (FNL4)": L(P + '/cand/FNL4_meas.json'), "MF-M-R": L(G + '/cand/MF-M-R_meas.json'), "SG": L(G + '/cand/SG_meas.json'), "AE (accepted AEL1)": L(S + '/w1m/legs/AEL1_meas.json'),
     "VA (accepted VAL4)": L(S + '/w1n/cand/VAL4_meas.json'), "SK": L(G + '/cand/SK_meas.json'), "GR (accepted W1l)": L(S + '/w1l/probe/GRL925_1200_meas.json')}
K = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_hand", "foot_share", "thorax_depth_share", "thorax_breadth_share",
     "elbow_over_humerus", "wrist_over_forearm", "knee_over_femur", "ankle_over_shin", "palm_breadth_over_hand", "waist_interval_over_torso"]
v = lambda b, k: M[b]["cranio"]["FVB"] if k == "FVB" else M[b]["ratio"][k]
sep = {"stature": {b: M[b]["stature"] for b in M}, "values": {b: {k: v(b, k) for k in K + ["FVB"]} for b in M},
       "pct_FN_vs": {b: {k: 100 * (v("FN (FNL4)", k) / v(b, k) - 1) for k in K + ["FVB"]} for b in M if not b.startswith("FN")}}
json.dump(sep, open(EV + '/separation.json', 'w'), indent=1)
print('%-24s' % 'FN % vs' + ''.join('%11s' % b[:10] for b in sep["pct_FN_vs"]))
for k in K + ["FVB"]: print('%-24s' % k + ''.join('%+10.1f%%' % sep["pct_FN_vs"][b][k] for b in sep["pct_FN_vs"]))
