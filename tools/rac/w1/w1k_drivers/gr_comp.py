# RAC W1k: Grask composition / frame continuity readings and the same-composition low check.
# (1) gn6.cont + waist_rise (W1i/W1j trunk-profile readings) for every Grask body and the MF / SK references;
# (2) Grask low composition (0.25 / 0.25) skin pelvic / girdle rows against MF-M-R and SK at the SAME composition
#     (w1e_checks with the low-composition measurements in the GR, MF-M-R and SK slots). Writes composition.json.
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, w1e_checks as WC
S = gn6.S if hasattr(gn6, 'S') else '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
K, F, G = S + '/w1k', S + '/w1f', S + '/w1g'; EV = os.environ.get('EVDIR', '/home/claude/wayfarer-design/reviews/rac-w1k-gr-evidence')
if os.environ.get('W1L'):   # W1l: corrected candidate (lumbar narrowing removed; pelvis X 0.925; proximal femur 1.20) and its variants
    L = S + '/w1l'
    B0 = {"GR W1l candidate": L + '/probe/GRL925_1200_rest.npz', "GR W1l skeleton (minimum composition)": L + '/probe/GRL925_1200-LEAN_rest.npz',
          "GR W1l Narrow": L + '/frames_w1l/GR-BODY-04_rest.npz', "GR W1l Broad": L + '/frames_w1l/GR-BODY-05_rest.npz',
          "GR W1l low composition (0.25 / 0.25)": L + '/comp_w1l/GR-LOW_rest.npz', "GR W1h as built (before)": G + '/final/GR_rest.npz'}

B = {"GR central (W1h as built)": G + '/final/GR_rest.npz', "GR skeleton (minimum composition)": G + '/final/GR-LEAN_rest.npz',
     "GR-BODY-04 Narrow": K + '/frames_asbuilt/GR-BODY-04_rest.npz', "GR-BODY-05 Broad": K + '/frames_asbuilt/GR-BODY-05_rest.npz',
     "GR-BODY-06 low muscle (0 / 0.5)": K + '/comp_asbuilt/GR-BODY-06_rest.npz', "GR-BODY-07 high muscle (1 / 0.5)": K + '/comp_asbuilt/GR-BODY-07_rest.npz',
     "GR-BODY-08 higher fat (0.5 / 1)": K + '/comp_asbuilt/GR-BODY-08_rest.npz', "GR-BODY-09 high muscle + fat (1 / 1)": K + '/comp_asbuilt/GR-BODY-09_rest.npz',
     "GR low composition (0.25 / 0.25)": K + '/comp_asbuilt/GR-LOW_rest.npz', "GR documented construction (spine_01 removed)": K + '/s01/GRS01_rest.npz',
     "MF-M-R reference": F + '/final/MF-M-R_rest.npz', "SK reference": F + '/final/SK_rest.npz',
     "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz'}
if os.environ.get('W1L'):
    B = {**B0, **{k: v for k, v in B.items() if k.startswith(("MF", "SK"))}, "MF-M-R skeleton": F + '/final_lean/MF-M-R-LEAN_rest.npz', "SK skeleton": F + '/final_lean/SK-LEAN_rest.npz', "SG skeleton": F + '/final_lean/SG-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print(k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
tmp = K + '/cand_lowpair'
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("GR", (S + '/w1l/comp_w1l/GR-LOW_meas.json') if os.environ.get('W1L') else K + '/comp_asbuilt/GR-LOW_meas.json'), ("MF-M-R", F + '/low/MF-M-R-LOW_meas.json'), ("SK", F + '/low/SK-LOW_meas.json')):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
out["low_same_composition_skin"] = [r for r in WC.run(tmp) if r.get('cand') == 'GR']
for r in out["low_same_composition_skin"]: print(r['check'], round(r['va'], 4), r['op'], round(r['vb'], 4), r['result'])
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
