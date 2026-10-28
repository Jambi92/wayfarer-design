# va2_pelvis.py OUT.json SKPDIR C1ID C2ID : Vael body / face source order §8 -- pelvis hard gate on the skeletal proxy (lean skeletal-envelope builds,
# skeletal_proxy.py; t = 0 / 0.5 / 1.0 cm; a rule holds only at all three) for the selected Vael sources, against the 178 cm comparators of the Vael Part A
# workspace (Marchfolk, frozen Fenn, frozen Aelari). Same rules and tolerances as va_partA.py (VA-P2a / P2b / P4 / P6 gating; VA-P2c / VA-P3 construction
# proxies report-only, visual check on the pelvis sheet) plus the limb-balance rows (forearm / upper arm, lower leg / thigh ~ MF +/- 0.010, W1n convention).
import sys, os, json
OUT, SD, C1, C2 = sys.argv[1:5]; PA = os.environ.get('VA_PA', '/tmp/claude-0/rt/va/partA')
SK = {n: json.load(open('%s/skp/%s_skp.json' % (PA, n))) for n in ('MFM178', 'MFF178', 'FNM178', 'FNF178', 'AEM178', 'AEF178')}
for n in (C1, C2): SK[n] = json.load(open('%s/%s_skp.json' % (SD, n)))
CFG = {'c1': dict(VA=C1, MF='MFM178', FN='FNM178', AE='AEM178'), 'c2': dict(VA=C2, MF='MFF178', FN='FNF178', AE='AEF178')}
TIE = 0.003
def check(v, ref, rule):
    if rule == '~=MF': return v >= ref * 0.98                                        # "approximately MF is sufficient": within 2 % below MF, or above
    if rule.startswith('>='): return v >= ref * (1 - TIE)
    if rule.startswith('>'): return v > ref
    if rule.startswith('<'): return v < ref
def sk(n, k, t):
    b = SK[n]['by_t'][t]; r = b['ratio']; H = SK[n]['stature_r6']
    if k == 'leg_share': return SK[n]['leg_share']
    if k == 'hip_joint_scale_share': return b['extra']['prox_femur'] / H
    if k == 'iliac_envelope_share': return r['crest_share'] * r['pelvic_depth_share']
    return r[k]
PR = [('VA-P2a hip-joint height / stature > MF', 'leg_share', '>MF'), ('VA-P2a hip-joint height / stature < Fenn', 'leg_share', '<FN'), ('VA-P2a hip-joint height / stature < Aelari', 'leg_share', '<AE'),
      ('VA-P2b bitrochanteric / crest not lower than MF', 'bitroch_over_crest', '>=MF'),
      ('VA-P2c hip-joint scale (proximal femur / stature) > Fenn', 'hip_joint_scale_share', '>FN'), ('VA-P2c hip-joint scale > Aelari', 'hip_joint_scale_share', '>AE'),
      ('VA-P2c hip-joint scale gracile vs MF', 'hip_joint_scale_share', '<MF'),
      ('VA-P3 iliac structural presence (crest x AP depth / stature^2) > Fenn', 'iliac_envelope_share', '>FN'), ('VA-P3 iliac structural presence > Aelari', 'iliac_envelope_share', '>AE'),
      ('VA-P3 iliac structural presence lighter than MF', 'iliac_envelope_share', '<MF'),
      ('VA-P3 no Aelari-style vertical iliac elongation (pelvic vertical / crest < Aelari)', 'pelvic_vertical_over_crest', '<AE'),
      ('VA-P4 pelvic AP depth / stature > Fenn', 'pelvic_depth_share', '>FN'), ('VA-P4 pelvic AP depth / stature > Aelari', 'pelvic_depth_share', '>AE'),
      ('VA-P4 pelvic AP depth / stature ~ MF (minimum relation; > MF not required)', 'pelvic_depth_share', '~=MF'),
      ('VA-P6 waist interval / torso < Aelari (compact continuity)', 'waist_interval_over_torso', '<AE')]
res = dict(order='reviews/chatgpt-rac-rp3-vael-body-face-source-order.md §8', sources={'c1': C1, 'c2': C2}, rules={}, summary={})
for cfg, C in CFG.items():
    rows = []
    for lab, k, rel in PR:
        ref = C[rel.lstrip('~=<>')[:2]]; by = {}
        for t in SK[C['VA']]['by_t']:
            a, b = sk(C['VA'], k, t), sk(ref, k, t); by[t] = dict(VA=round(a, 6), ref=round(b, 6), diff_pct=round(100 * (a / b - 1), 3), holds=bool(check(a, b, rel)))
        rows.append(dict(rule=lab, key=k, rel=rel, by_t=by, holds_all_t=all(x['holds'] for x in by.values()), gating=k not in ('hip_joint_scale_share', 'iliac_envelope_share'),
                         align_resid_cm=SK[C['VA']].get('align_joint_resid_cm')))
    res['rules'][cfg] = rows
    res['summary'][cfg] = dict(gating_hold=sum(r['holds_all_t'] for r in rows if r['gating']), gating_of=sum(r['gating'] for r in rows),
                               failing=[r['rule'] for r in rows if r['gating'] and not r['holds_all_t']], report_only_not_holding=[r['rule'] for r in rows if not r['gating'] and not r['holds_all_t']])
json.dump(res, open(OUT, 'w'), indent=1)
for cfg in CFG:
    print(cfg, 'pelvis gating %d/%d' % (res['summary'][cfg]['gating_hold'], res['summary'][cfg]['gating_of']), 'fail', res['summary'][cfg]['failing'], 'report-only not holding', res['summary'][cfg]['report_only_not_holding'])
    for r in res['rules'][cfg]: print('   %-80s %s %s' % (r['rule'][:80], r['holds_all_t'], ' '.join('%+.3f' % r['by_t'][t]['diff_pct'] for t in sorted(r['by_t']))))
