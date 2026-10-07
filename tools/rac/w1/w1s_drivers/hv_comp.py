# RAC W1s: Halvren trunk continuity readings (central, minimum composition, breadth-only frames, composition bodies, panel bodies, sources)
# and the same-composition low check (HV low 0.25 / 0.25 vs MF-M-R-LOW and SK-LOW: not collapsing into a source at matched composition).
# Report only.
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers')
import gn6
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; R, F = S + '/w1s', S + '/w1f'
EV = '/home/claude/wayfarer-design/reviews/rac-w1s-hv-evidence'
B = {"HV central (as built)": F + '/final/HV_rest.npz', "HV minimum composition": R + '/hv/lean/HV-LEAN_rest.npz',
     "HV Narrow (breadth only)": R + '/frame_NARROWB/final/HV_rest.npz', "HV Broad (breadth only, pelvis x1.12)": R + '/frame_BROADB_P112/final/HV_rest.npz',
     "HV low (0.25 / 0.25)": R + '/comp/HV-LOW_rest.npz', "HV low muscle (0 / 0.5)": R + '/comp/HV-LOWMUS_rest.npz', "HV high muscle (1 / 0.5)": R + '/comp/HV-HIMUS_rest.npz',
     "HV higher fat (0.5 / 1)": R + '/comp/HV-HIFAT_rest.npz', "HV high muscle + fat (1 / 1)": R + '/comp/HV-HIBOTH_rest.npz',
     "Panel: human-leaning mixed (HVH3)": R + '/panel/HVH3_rest.npz', "Panel: elf-leaning mixed (HVE3)": R + '/panel/HVE3_rest.npz',
     "MF-M-R": F + '/final/MF-M-R_rest.npz', "SK": F + '/final/SK_rest.npz', "SG": F + '/final/SG_rest.npz', "FN (FNL4)": S + '/w1p/cand/FNL4_rest.npz',
     "AE (AEL1)": S + '/w1m/legs/AEL1_rest.npz', "VA (VAL4)": S + '/w1n/cand/VAL4_rest.npz', "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    if not os.path.exists(p): print('missing', k, p); continue
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-40s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
L = lambda p: json.load(open(p))["combined"]["ratio"]
K = ["torso_share", "neck_share", "thorax_breadth_share", "thorax_depth_share", "thorax_d_over_b", "waist_interval_over_torso", "shoulder_breadth_share", "arm_share", "leg_share",
     "upperarm_over_arm", "forearm_over_arm", "femur_over_leg", "shin_over_leg", "pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth", "pelvic_vertical_over_thoracic_vertical",
     "bitroch_over_crest", "hand_share", "finger_over_palm", "palm_breadth_over_hand", "foot_share"]
hv = L(R + '/comp/HV-LOW_meas.json'); low = {}
for nm, p in (("MF-M-R-LOW", F + '/low/MF-M-R-LOW_meas.json'), ("SK-LOW", F + '/low/SK-LOW_meas.json')):
    s = L(p); pct = {k: 100 * (hv[k] / s[k] - 1) for k in K}
    low[nm] = {"pct_HVLOW_vs": pct, "within_1pct": sum(abs(v) < 1 for v in pct.values()), "n": len(K)}
    print('HV-LOW vs %s: within 1 %% on %d of %d body readings' % (nm, low[nm]["within_1pct"], len(K)))
out["low_same_composition"] = low
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
