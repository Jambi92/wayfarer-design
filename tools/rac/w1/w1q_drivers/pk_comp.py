# RAC W1q: Pipkin continuity readings, same-composition low check (PK low vs MF-M-R-LOW / SK-LOW), and separation (% difference of PK
# from normalized MF, accepted SG / FN, unaccepted DU and CG, the diagnostic Narrow DU, and the generator human-child proxy). Report only.
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, w1e_checks as WC
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; Q, F, G = S + '/w1q', S + '/w1f', S + '/w1g'
EV = '/home/claude/wayfarer-design/reviews/rac-w1q-pk-evidence'
B = {"PK central (PK-NAT, as built)": F + '/final/PK-NAT_rest.npz', "PK minimum composition": F + '/final_lean/PK-NAT-LEAN_rest.npz', "PK Narrow (breadth only)": Q + '/frame_NARROWB/final/PK-NAT_rest.npz',
     "PK Broad (breadth only, pelvis x1.12)": Q + '/frame_BROADB_P112/final/PK-NAT_rest.npz', "PK low (0.25 / 0.25)": Q + '/comp/PK-LOW_rest.npz',
     "DU (DU-NAT, unaccepted)": F + '/final/DU-NAT_rest.npz', "DU Narrow (diagnostic)": Q + '/du_NARROWB/final/DU-NAT_rest.npz', "CG (CG-NAT, unaccepted)": F + '/final/CG-NAT_rest.npz',
     "Human child proxy (107 cm, generator age ~6 y)": Q + '/child/CHILD6_rest.npz', "MF-M-R": F + '/final/MF-M-R_rest.npz',
     "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz', "MF-M-R minimum composition": F + '/final_lean/MF-M-R-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    if not os.path.exists(p): print('missing', k, p); continue
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-46s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
tmp = Q + '/cand_lowpair'
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("PK", Q + '/comp/PK-LOW_meas.json'), ("PK-NAT", Q + '/comp/PK-LOW_meas.json'), ("MF-M-R", F + '/low/MF-M-R-LOW_meas.json'), ("SK", F + '/low/SK-LOW_meas.json')): shutil.copy(src, tmp + '/%s_meas.json' % slot)
out["low_same_composition_skin"] = [r for r in WC.run(tmp) if r.get('cand') == 'PK' and r.get('b') in ('MF', 'MF-M-R', 'SK')]
for r in out["low_same_composition_skin"]: print(r['check'], round(r['va'], 4), r['op'], round(r['vb'], 4), r['result'])
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
L = lambda p: json.load(open(p))["combined"]
M = {"PK (PK-NAT)": L(G + '/cand/PK-NAT_meas.json'), "MF-M-R": L(G + '/cand/MF-M-R_meas.json'), "SG": L(G + '/cand/SG_meas.json'), "FN (accepted FNL4)": L(S + '/w1p/cand/FNL4_meas.json'),
     "DU (unaccepted)": L(G + '/cand/DU-NAT_meas.json'), "DU Narrow (diagnostic)": L(Q + '/du_NARROWB/final/DU-NAT_meas.json'), "CG (unaccepted)": L(G + '/cand/CG-NAT_meas.json'),
     "Child proxy (diagnostic)": L(Q + '/child/CHILD6_meas.json')}
K = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "hand_share", "foot_share", "thorax_depth_share", "thorax_breadth_share", "pelvic_vertical_share",
     "pelvic_vertical_over_thoracic_vertical", "pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth", "waist_interval_over_torso", "elbow_over_humerus", "wrist_over_forearm", "knee_over_femur", "ankle_over_shin"]
v = lambda b, k: M[b]["cranio"]["FVB"] if k == "FVB" else M[b]["ratio"][k]
sep = {"stature": {b: M[b]["stature"] for b in M}, "values": {b: {k: v(b, k) for k in K + ["FVB"]} for b in M},
       "pct_PK_vs": {b: {k: 100 * (v("PK (PK-NAT)", k) / v(b, k) - 1) for k in K + ["FVB"]} for b in M if not b.startswith("PK")}}
json.dump(sep, open(EV + '/separation.json', 'w'), indent=1)
print('%-30s' % 'PK % vs' + ''.join('%11s' % b[:10] for b in sep["pct_PK_vs"]))
for k in K + ["FVB"]: print('%-30s' % k + ''.join('%+10.1f%%' % sep["pct_PK_vs"][b][k] for b in sep["pct_PK_vs"]))
