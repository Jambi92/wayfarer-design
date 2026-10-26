# lm_v003.py ADJ_RAW_v002.json V001.json OUTDIR : the one authorised landmark revision (order 8918cea §3). Knees: AD-R2 cap read as the
# TOTAL displacement from the exact v001 consensus coordinate (<= 5 mm), placed as close as possible to the horizontal section centroid
# at the consensus level. Writes adjudicated_raw_v003.json (then package.py ... v003) and the displacement-compliance audit.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fitlib import T_PROD
RAW = json.load(open(sys.argv[1])); V1 = json.load(open(sys.argv[2]))['joints']; OUT = sys.argv[3]
R = RAW['R']; A = np.asarray; P1 = lambda k: A(V1[k]['position_source_frame_cm'], float)
CAP = 0.5; AUD = []
for s in 'lr':
    k = 'knee_' + s; c0 = P1(k); sec = A(R[k]['p'], float)           # v002 knee = unrestricted horizontal section centroid at the level
    d = sec - c0; L = float(np.linalg.norm(d)); p = c0 + d * min(1.0, CAP / L) if L > 0 else c0.copy()
    R[k]['v002_unrestricted_comparison'] = dict(p_source=sec.tolist(), p_production=(sec + T_PROD).tolist(), status='comparison only — not approved (exceeded the AD-R2 5 mm total-displacement cap)')
    R[k]['p'] = p.tolist(); R[k]['provenance_class'] = 'manual-author-rig (bounded experimental candidate, pending review)'
    R[k]['construction_rule'] = ('v001 consensus %s moved toward the horizontal leg-section centroid at the consensus level, total displacement capped at 5.0 mm (AD-R2 as clarified by order 8918cea)'
                                 % np.round(c0 + T_PROD, 3).tolist())
    R[k]['limitation'] = 'section-centre requirement only partly met: %.2f cm residual to the section centroid (the two requirements conflict); internal centre accuracy not established' % float(np.linalg.norm(sec - p))
    R[k]['adjustment_cm'] = float(np.linalg.norm(p - c0)); R[k]['adjustment_reason'] = 'bounded toward the section centroid (unrestricted distance %.2f cm)' % L
RAW['LOG'].append('v003 (order 8918cea): knees re-placed with the AD-R2 5 mm cap applied to the full displacement from the v001 consensus')
json.dump(RAW, open(os.path.join(OUT, 'adjudicated_raw_v003.json'), 'w'), indent=1)
# ---------------- displacement-compliance audit (all placements that the rulings bound, plus the unbounded rule-based ones for disclosure)
def row(k, ref, cap, note):
    p = A(R[k]['p'], float); d = p - ref; n = float(np.linalg.norm(d))
    AUD.append(dict(id=k, reference=note, reference_production_cm=(ref + T_PROD).round(3).tolist(), chosen_production_cm=(p + T_PROD).round(3).tolist(),
                    displacement_cm=d.round(4).tolist(), norm_cm=round(n, 4), cap_cm=cap, compliant=None if cap is None else bool(n <= cap + 1e-6),
                    residual_to_section_centre_cm=None if not k.startswith('knee') else round(float(np.linalg.norm(A(R[k]['v002_unrestricted_comparison']['p_source']) - p)), 4)))
for s in 'lr':
    row('hip_' + s, P1('hip_' + s), CAP, 'v001 consensus (AD-R1, cap 5 mm)')
    row('knee_' + s, P1('knee_' + s), CAP, 'v001 consensus (AD-R2, cap 5 mm total)')
    row('elbow_' + s, P1('elbow_' + s), CAP, 'v001 cubital target (AD-R4, cap 5 mm)')
    row('ankle_' + s, P1('ankle_' + s), None, 'v001 consensus level (AD-R2: section-centreline placement, no cap stated) — disclosed')
row('pelvis', P1('pelvis_root'), CAP, 'v001 pelvis proposal (AD-R7, cap 5 mm)')
for s in 'lr':
    AUD.append(dict(id='glenohumeral_' + s, reference='rule-based (AD-R3; no displacement cap)', chosen_production_cm=(A(R['glenohumeral_' + s]['p']) + T_PROD).round(3).tolist(), cap_cm=None, compliant=None))
    AUD.append(dict(id='sternoclavicular_' + s, reference='rule-based (AD-R5; exactly 3.0 cm posterior)', chosen_production_cm=(A(R['sternoclavicular_' + s]['p']) + T_PROD).round(3).tolist(), cap_cm=None, compliant=None))
json.dump(AUD, open(os.path.join(OUT, 'displacement_compliance_v003.json'), 'w'), indent=1)
L = ['| id | reference | reference (prod cm) | chosen (prod cm) | displacement (cm) | norm cm | cap cm | compliant | residual to section centre cm |', '|---|---|---|---|---|---|---|---|---|']
for a in AUD:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (a['id'], a['reference'], a.get('reference_production_cm', '—'), a['chosen_production_cm'], a.get('displacement_cm', '—'), a.get('norm_cm', '—'),
             '—' if a['cap_cm'] is None else a['cap_cm'], '—' if a['compliant'] is None else ('yes' if a['compliant'] else '**NO**'), a.get('residual_to_section_centre_cm') if a.get('residual_to_section_centre_cm') is not None else '—'))
open(os.path.join(OUT, 'displacement_compliance_v003.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
