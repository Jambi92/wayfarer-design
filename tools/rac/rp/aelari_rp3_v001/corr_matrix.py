# corr_matrix.py WORK OUT.json [ID:path_meas ...] : order 0f6aba8 §4 response matrix -- each probe / candidate against the AEL1 base and the matched-stature
# frozen-Fenn / Marchfolk comparators (190 cm). Reports the targeted measures (thoracic vertical share, shin / leg) and every guarded share.
import sys, json, numpy as np
W, OUT = sys.argv[1:3]; extra = sys.argv[3:]
meas = lambda p: json.load(open(p))['combined']
M = {'AEL1': meas(W + '/partA/ref/AEL1_meas.json'), 'AELF190': meas(W + '/partA/build/AELF190_meas.json')}
for n in ('FNM190', 'FNF190', 'MFM190', 'MFF190', 'SGM190', 'SGF190'): M[n] = meas('%s/partA/cmp/%s_meas.json' % (W, n))
for a in extra: n, p = a.split(':'); M[n] = meas(p)
def R(n, k):
    m = M[n]; r = m['ratio']
    if k == 'stature': return m['stature']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'central_vertical_share': return R(n, 'cranial_vertical_share') + r['neck_share'] + r['torso_share']
    if k == 'extremity_share': return r['arm_share'] + r['hand_share'] + r['leg_share'] + r['foot_share']
    if k == 'knee_height_share': return (m['mean']['hip_height'] - m['mean']['thigh']) / m['stature']
    raise KeyError(k)
KEYS = ['stature', 'thoracic_vertical_share', 'torso_share', 'waist_interval_over_torso', 'neck_share', 'cranial_vertical_share', 'central_vertical_share', 'extremity_share',
        'leg_share', 'shin_over_leg', 'femur_over_leg', 'thigh_share', 'shin_share', 'arm_share', 'forearm_over_upperarm', 'hand_share', 'foot_share', 'thorax_depth_share', 'thorax_breadth_share',
        'shoulder_breadth_share', 'pelvic_vertical_share', 'crest_share', 'bitroch_over_crest', 'pelvic_vertical_over_crest']
res = {}
for n in M:
    base = 'AELF190' if n.startswith('AELF') else 'AEL1'; fn = 'FNF190' if (n.startswith('AELF') or n.endswith('F190')) else 'FNM190'; mf = 'MFF190' if fn == 'FNF190' else 'MFM190'
    row = {k: round(R(n, k), 5) for k in KEYS}
    row['d_vs_base_pct'] = {k: round(100 * (R(n, k) / R(base, k) - 1), 2) for k in KEYS}
    row['thoracic_vs_FN_pct'] = round(100 * (R(n, 'thoracic_vertical_share') / R(fn, 'thoracic_vertical_share') - 1), 2)
    row['shin_over_leg_gap_to_MF'] = round(R(n, 'shin_over_leg') - R(mf, 'shin_over_leg'), 5); row['FN_shin_over_leg_gap_to_MF'] = round(R(fn, 'shin_over_leg') - R(mf, 'shin_over_leg'), 5)
    row['leg_more_even_than_FN'] = bool(abs(row['shin_over_leg_gap_to_MF']) < abs(row['FN_shin_over_leg_gap_to_MF']))
    res[n] = row
json.dump(res, open(OUT, 'w'), indent=1)
show = ['stature', 'thoracic_vertical_share', 'torso_share', 'waist_interval_over_torso', 'leg_share', 'shin_over_leg', 'arm_share', 'neck_share', 'pelvic_vertical_over_crest']
for n, r in res.items():
    print('%-12s' % n, ' '.join('%s %+.2f' % (k[:10], r['d_vs_base_pct'][k]) for k in show), '| thorVsFN %+.2f | shinGapMF %.4f (FN %.4f) even %s' % (r['thoracic_vs_FN_pct'], r['shin_over_leg_gap_to_MF'], r['FN_shin_over_leg_gap_to_MF'], r['leg_more_even_than_FN']))
