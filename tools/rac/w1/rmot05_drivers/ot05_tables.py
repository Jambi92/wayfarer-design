# RAC RM-OT-05: roster register + min / reference / max measurement table on existing accepted measurements (no new metric invented).
import os, sys, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; RV = '/home/claude/wayfarer-design/reviews'
E = RV + '/rac-rmot05-evidence'; os.makedirs(E, exist_ok=True)
REG = [  # race, min, max, reference, sex rule, conditional reach, controlling source, demo (min body, ref body, max body), status
 ('Marchfolk', 147, 203, '173 (MF-M-R 173.14; MF-F-R 172.99)', 'no sex-specific restriction; both configurations built at both bounds', 'none', 'MARCHFOLK L62-64, L23, L249; W2A', ('w2a/st/MFM147-NAT', 'w1f/final/MF-M-R', 'w2a/st/MFM203'), 'SUPPORTED'),
 ('Skarn', 183, 229, '208 (SK 208.01; central face C1R)', 'ordinary human configurations; bounds identical, both demonstrated (configuration 2 at 229 = macro 1.0 + native extension)', 'none', 'SKARN L11-13; W2B / W2B1; W2C1 knee reversion', ('w2b/st/SKM183', 'w1f/final/SK', 'w2b/st/SKM229'), 'SUPPORTED'),
 ('Sagekin', 152, 208, '178 (SG 177.99)', 'both human configurations allowed; configuration-2 boundaries NOT DEMONSTRATED', 'none', 'SAGEKIN L70-72; W2E', ('w2e/st/SG152-NAT', 'w1f/final/SG', 'w2e/st/SG208'), 'CONSTRAINED'),
 ('Fenn', 157, 211, '181 (FNL4 181.16)', 'one configuration (AD-R21)', 'none', 'FENN L22-24; W2F', ('w2f/st/FN157-NAT', 'w1p/cand/FNL4', 'w2f/st/FN211'), 'SUPPORTED'),
 ('Aelari', 168, 221, '190 (AEL1 190.01)', 'one configuration', 'none', 'AELARI L25-27; W2F (168 native route, R2)', ('w2f/rt/AE168N-NAT', 'w1m/legs/AEL1', 'w2f/st/AE221'), 'SUPPORTED'),
 ('Vael', 157, 203, '178 (VAL4 178.00)', 'one configuration', 'none', 'VAEL L15-17; W2F', ('w2f/st/VA157-NAT', 'w1n/cand/VAL4', 'w2f/st/VA203'), 'SUPPORTED'),
 ('Halvren', '152 central (outer reach > 147, H-5)', '213 central (outer reach < 229, H-5)', '178 (HVC1 177.73, diagnostic anchor)', 'follows sources (AD-R22); no sex shift', 'ancestry-conditional outer reach: 147.2 (MF-supported, bound-limited), 228.8 (SK-supported), 221.0 (AE-supported, source ceiling); H-1...H-6; AD-W3A-1...4', 'HALVREN L86-88, L481, L493-509; UCCA L296; W2G; W3A1 FINAL ACCEPT', ('w2g/st/HV152N-NAT', 'w1s/probe/HVC1', 'w2g/st/HV213M'), 'NOT FULLY DEMONSTRATABLE'),
 ('Durrim', 122, 152, '137 (DU137C 137.00; D1 pelvis rebuild)', 'one configuration, no shift (AD-R18/19)', 'none', 'DURRIM L15-17, L19; W2H / W2H1', ('w2h1/st/DU122C-NAT', 'w2h1/st/DU137C-NAT', 'w2h1/st/DU152C-NAT'), 'SUPPORTED'),
 ('Grask', 198, 239, '218 (GR218R 217.99)', 'one configuration', 'none', 'GRASK L15-17; W2C', ('w2c/b/GR198/GR198', 'w2c/b/GR218R/GR218R', 'w2c/b/GR239/GR239'), 'SUPPORTED'),
 ('Gorrund', 208, 251, '229 in R-2 / GORRUND L29; accepted ARM GOREF 230.9 (W1i / W1j / W2D)', 'one configuration', '251 = current world-validation upper stature, "never a permanent maximum" (GORRUND L31)', 'GORRUND L27-31; W2D', ('w2d/b/GO208/GO208', 'w2d/b/GOREF/GOREF', 'w2d/b/GO251/GO251'), 'SUPPORTED'),
 ('Pipkin', 91, 122, '107 (PK-NAT 107.00)', 'one configuration', 'none', 'PIPKIN L25-27, L119; W2H', ('w2h/st/PK91-NAT', 'w1f/final/PK-NAT', 'w2h/st/PK122-NAT'), 'SUPPORTED'),
 ('Cogling', 76, 107, '91 (CGJ7 90.99)', 'one configuration (sex via AC-U2, no stature shift)', 'none', 'COGLING L50-56 (provisional), L63, L1589; W2H', ('w2h/st/CG76-NAT', 'w1r/probe/CGJ7', 'w2h/st/CG107-NAT'), 'CONSTRAINED'),
 ('Saurin', 168, 208, '188 (W2 reference 187.88; tail excluded)', 'no sex shift, no sex-specific bound (s263); SA-F built at the same statures', 'none (tail length coupled per s256, not stature)', 'SAURIN L64-68, L3587-3593, s263; W2I D1 regional route; W2I6', ('SA-M168', 'SA-M188', 'SA-M208'), 'SUPPORTED')]
KEYS = ['HH_share', 'torso_share', 'leg_share', 'arm_share', 'shoulder_breadth_share', 'thorax_d_over_b']
SAF = json.load(open(RV + '/rac-w2i4-sa-evidence/bodies_F.json'))
def meas(p):
    if p.startswith('SA-'):
        m = SAF[p]; return dict(stature=m['height'], head_len_over_H=m['head_len_ratio'], lower_trunk_over_H=m['lower_trunk_over_H'], shoulder_b_over_H=m['shoulder_b_over_H'],
                                thorax_d_over_w=m['thorax_d_over_w'], tail_len_pct=m['tail_len_pct'], foot_len_over_H=m['foot_len_over_H'])
    m = json.load(open('%s/%s_meas.json' % (S, p))); r = m['r6']['ratio']; return dict(stature=m['stature_r6'], **{k: r[k] for k in KEYS})
out = {'register': [], 'measurements': {}}
for row in REG:
    race = row[0]; out['register'].append(dict(race=race, hard_min=row[1], hard_max=row[2], reference=row[3], sex_rule=row[4], conditional_reach=row[5], source=row[6], status=row[8], frequency='OPEN'))
    out['measurements'][race] = {tag: dict(body=p, **meas(p)) for tag, p in zip(('min', 'ref', 'max'), row[7])}
for tag, p in (('reach_lo_147.2_MF', 'w3a/lo/HL147p2C-NAT'), ('reach_hi_228.8_SK', 'w3a1/up/HU228p8Sc'), ('reach_hi_221.0_AE', 'w3a1/up/HU221Ac')):
    try: out['measurements']['Halvren'][tag] = dict(body=p, **meas(p))
    except Exception as e: out['measurements']['Halvren'][tag] = dict(body=p, error=str(e))
# allometry / identity checks on existing measurements: head share must fall with stature inside each race (non-uniform route); Pipkin head share
# > Marchfolk at matched short stature is canon-directional (PIPKIN L292) and Cogling head height clamped 11-13 cm (L1589)
chk = {}
for race, mm in out['measurements'].items():
    k = 'HH_share' if race != 'Saurin' else 'head_len_over_H'
    v = [mm[t].get(k) for t in ('min', 'ref', 'max')]
    chk[race] = dict(head_share_min_ref_max=v, decreasing_with_stature=bool(v[0] > v[1] > v[2]), uniform_scale_would_be_constant=True)
out['allometry_check'] = chk
json.dump(out, open(E + '/register.json', 'w'), indent=1)
for race, mm in out['measurements'].items():
    print(race.ljust(10), ' | '.join('%s %.1f HH %.4f' % (t, mm[t]['stature'], mm[t].get('HH_share', mm[t].get('head_len_over_H', 0))) for t in ('min', 'ref', 'max')), chk[race]['decreasing_with_stature'])
