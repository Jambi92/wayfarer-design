# RAC W1t: Durrim trunk continuity readings (central, minimum composition, frames, composition bodies, accepted short races, references,
# human-child proxy). Report only.
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers')
import gn6
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; T, F = S + '/w1t', S + '/w1f'
EV = '/home/claude/wayfarer-design/reviews/rac-w1t-du-evidence'
B = {"DU central (DU-NAT as built)": F + '/final/DU-NAT_rest.npz', "DU minimum composition": F + '/final_lean/DU-NAT-LEAN_rest.npz',
     "DU Narrow (breadth only)": T + '/frame_NARROWB/final/DU-NAT_rest.npz', "DU Broad (breadth only, pelvis x1.08)": T + '/frame_BROADB/final/DU-NAT_rest.npz',
     "DU Broad (breadth only, pelvis x1.12)": T + '/frame_BROADB_P112/final/DU-NAT_rest.npz',
     "DU low (0.25 / 0.25)": T + '/comp/DU-LOW_rest.npz', "DU low muscle (0 / 0.5)": T + '/comp/DU-LOWMUS_rest.npz', "DU high muscle (1 / 0.5)": T + '/comp/DU-HIMUS_rest.npz',
     "DU higher fat (0.5 / 1)": T + '/comp/DU-HIFAT_rest.npz', "DU high muscle + fat (1 / 1)": T + '/comp/DU-HIBOTH_rest.npz',
     "DU 152 cm (native route)": T + '/bnd/DU152-NAT_rest.npz', "MF 152 cm (native route)": T + '/bnd/MF152-NAT_rest.npz', "SG 152 cm (native route)": T + '/bnd/SG152-NAT_rest.npz',
     "DU 122 cm (native route)": T + '/bnd/DU122-NAT_rest.npz', "PK 122 cm (native route)": T + '/bnd/PK122-NAT_rest.npz', "CG 107 cm (native route)": T + '/bnd/CG107-NAT_rest.npz',
     "PK central (accepted)": F + '/final/PK-NAT_rest.npz', "PK Broad (accepted frame)": S + '/w1q/frame_BROADB_P112/final/PK-NAT_rest.npz',
     "CG central (accepted CGJ7)": S + '/w1r/probe/CGJ7_rest.npz', "CG Broad high muscle": T + '/cgb/CGBHM_rest.npz',
     "MF-M-R": F + '/final/MF-M-R_rest.npz', "SK": F + '/final/SK_rest.npz', "Human child proxy (137 cm, age ~9 y)": T + '/child/CHILD9_rest.npz'}
out = {"continuity": {}}
for k, p in B.items():
    if not os.path.exists(p): print('missing', k, p); continue
    out["continuity"][k] = {**gn6.cont(p), "waist_rise": gn6.waist_rise(p)}; print('%-44s' % k, {a: round(b, 4) for a, b in out["continuity"][k].items()}, flush=True)
json.dump(out, open(EV + '/composition.json', 'w'), indent=1, default=float)
