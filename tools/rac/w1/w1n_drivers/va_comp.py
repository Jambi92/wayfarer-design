# RAC W1n: Vael continuity readings, same-composition low check (VA low vs MF-M-R-LOW / SK-LOW), and separation (% difference of
# VAL4 from MF, SG, accepted AE (AEL1), FN, SK, accepted GR). Writes composition.json and separation.json. Diagnostic / report only.
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, w1e_checks as WC
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; N, F, G = S + '/w1n', S + '/w1f', S + '/w1g'
EV = '/home/claude/wayfarer-design/reviews/rac-w1n-va-evidence'
B = {"VA VAL4 candidate": N + '/cand/VAL4_rest.npz', "VA as built (W1g)": G + '/final/VA_rest.npz', "VA VAL4 minimum composition": N + '/val4/lean/VA-LEAN_rest.npz',
     "VA Narrow (breadth only)": N + '/frame_NARROWB/final/VA_rest.npz', "VA Broad (breadth only)": N + '/frame_BROADB/final/VA_rest.npz',
     "VA low (0.25 / 0.25)": N + '/comp/VA-LOW_rest.npz', "AE AEL1 (accepted)": S + '/w1m/legs/AEL1_rest.npz', "FN (W1g)": G + '/final/FN_rest.npz',
     "MF-M-R": F + '/final/MF-M-R_rest.npz', "SG": F + '/final/SG_rest.npz', "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz',
     "MF-M-R minimum composition": F + '/final_lean/MF-M-R-LEAN_rest.npz', "SG minimum composition": F + '/final_lean/SG-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items(): out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-28s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
tmp = N + '/cand_lowpair'
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("VA", N + '/comp/VA-LOW_meas.json'), ("MF-M-R", F + '/low/MF-M-R-LOW_meas.json'), ("SK", F + '/low/SK-LOW_meas.json')): shutil.copy(src, tmp + '/%s_meas.json' % slot)
out["low_same_composition_skin"] = [r for r in WC.run(tmp) if r.get('cand') == 'VA' and r.get('b') in ('MF', 'MF-M-R', 'SK')]
for r in out["low_same_composition_skin"]: print(r['check'], round(r['va'], 4), r['op'], round(r['vb'], 4), r['result'])
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
L = lambda p: json.load(open(p))["combined"]
M = {"VA (VAL4)": L(N + '/cand/VAL4_meas.json'), "MF-M-R": L(G + '/cand/MF-M-R_meas.json'), "SG": L(G + '/cand/SG_meas.json'), "AE (accepted AEL1)": L(S + '/w1m/legs/AEL1_meas.json'),
     "FN": L(G + '/cand/FN_meas.json'), "SK": L(G + '/cand/SK_meas.json'), "GR (accepted W1l)": L(S + '/w1l/probe/GRL925_1200_meas.json')}
K = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "hand_share", "foot_share", "thorax_depth_share", "thorax_breadth_share",
     "elbow_over_humerus", "wrist_over_forearm", "knee_over_femur", "ankle_over_shin", "palm_breadth_over_hand", "waist_interval_over_torso"]
v = lambda b, k: M[b]["cranio"]["FVB"] if k == "FVB" else M[b]["ratio"][k]
sep = {"stature": {b: M[b]["stature"] for b in M}, "pct_VA_vs": {b: {k: 100 * (v("VA (VAL4)", k) / v(b, k) - 1) for k in K + ["FVB"]} for b in M if not b.startswith("VA")}}
json.dump(sep, open(EV + '/separation.json', 'w'), indent=1)
print('%-26s' % 'VA % vs' + ''.join('%11s' % b[:10] for b in sep["pct_VA_vs"]))
for k in K + ["FVB"]: print('%-26s' % k + ''.join('%+10.1f%%' % sep["pct_VA_vs"][b][k] for b in sep["pct_VA_vs"]))
