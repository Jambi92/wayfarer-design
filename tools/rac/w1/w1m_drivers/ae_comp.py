# RAC W1m: Aelari trunk-continuity readings (W1i/W1j gn6.cont + waist_rise) and the same-composition low check
# (AE low 0.25/0.25 vs MF-M-R-LOW / SK-LOW in the w1e skin rows). Writes composition.json. Diagnostic.
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn6, w1e_checks as WC
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; M, F, G = S + '/w1m', S + '/w1f', S + '/w1g'
EV = '/home/claude/wayfarer-design/reviews/rac-w1m-ae-evidence'
B = {"AE AEL1 candidate": M + '/legs/AEL1_rest.npz', "AE as built (W1g)": G + '/final/AE_rest.npz', "AE AEL1 minimum composition": M + '/ael1/lean/AE-LEAN_rest.npz',
     "AE Narrow": M + '/frame_NARROW/final/AE_rest.npz', "AE Broad": M + '/frame_BROAD/final/AE_rest.npz', "AE low (0.25 / 0.25)": M + '/comp/AE-LOW_rest.npz',
     "AE high muscle + fat (1 / 1)": M + '/comp/AE-HIBOTH_rest.npz', "FN (W1g)": G + '/final/FN_rest.npz', "VA (W1g)": G + '/final/VA_rest.npz',
     "MF-M-R": F + '/final/MF-M-R_rest.npz', "SG": F + '/final/SG_rest.npz', "SK": F + '/final/SK_rest.npz',
     "MF-M-R low (0.25 / 0.25)": F + '/low/MF-M-R-LOW_rest.npz', "SK low (0.25 / 0.25)": F + '/low/SK-LOW_rest.npz',
     "MF-M-R minimum composition": F + '/final_lean/MF-M-R-LEAN_rest.npz', "SG minimum composition": F + '/final_lean/SG-LEAN_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-30s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
tmp = M + '/cand_lowpair'
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("AE", M + '/comp/AE-LOW_meas.json'), ("MF-M-R", F + '/low/MF-M-R-LOW_meas.json'), ("SK", F + '/low/SK-LOW_meas.json')): shutil.copy(src, tmp + '/%s_meas.json' % slot)
out["low_same_composition_skin"] = [r for r in WC.run(tmp) if r.get('cand') == 'AE' and r.get('b') in ('MF', 'MF-M-R', 'SK')]
for r in out["low_same_composition_skin"]: print(r['check'], round(r['va'], 4), r['op'], round(r['vb'], 4), r['result'])
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
