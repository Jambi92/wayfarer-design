# hv_pelvis_pkg.py OUT.json : Halvren body / face source order §16 / §17 -- (a) pelvis deltas of every body candidate vs the current HVC1 / HVF178 and vs
# Marchfolk (skin, 178 cm), (b) the HP-A / HP-B / HP-C author-decision package (diagnostic builds of build_hp.sh): skeletal-proxy pelvic relations
# (t = 0 / 0.5 / 1.0) vs Marchfolk, Sagekin, frozen Fenn, frozen Aelari, frozen Vael, plus hip-joint height and waist continuity. REPORT ONLY.
import sys, json, numpy as np
OUT = sys.argv[1]; PA = '/tmp/claude-0/rt/hv/partA'; HB = '/tmp/claude-0/rt/hv/hb/cand'; HP = '/tmp/claude-0/rt/hv/hp'
CMP = {'c1': dict(MF='MFM178', SG='SGM178', FN='FNM178', AE='AEM178', VA='VAM178', HV0='HVC1'), 'c2': dict(MF='MFF178', SG='SGF178', FN='FNF178', AE='AEF178', VA='VAF178', HV0='HVF178')}
PRE = {'c1': 'HVC1', 'c2': 'HVF178'}; pct = lambda a, b: 100 * (a / b - 1)
SKIN = ['bitroch_over_crest', 'pelvic_depth_share', 'pelvic_vertical_share', 'crest_share', 'pelvic_vertical_over_crest', 'waist_interval_over_torso', 'leg_share', 'hip_joint_breadth_share']
mz = lambda p: json.load(open(p + '_meas.json'))['combined']['ratio']
res = dict(note='REPORT ONLY: Halvren pelvic inheritance is OPEN; HP-A / HP-B / HP-C are diagnostic directions, none canonical', candidates={}, hp={})
for c, C in CMP.items():
    ref = {s: mz('%s/%s/%s' % (PA, 'cmp' if s != 'HV0' else ('ref' if c == 'c1' else 'build'), n)) for s, n in C.items()}
    for t in ('HB1', 'HB2', 'HB3', 'HB1HF1', 'HB2HF2', 'HB3HF3', 'HB2HF1', 'HB2HF3'):
        m = mz('%s/%s-%s' % (HB, PRE[c], t))
        res['candidates']['%s %s' % (t, c)] = {k: dict(value=round(m[k], 5), vs_current_HV_pct=round(pct(m[k], ref['HV0'][k]), 2), vs_MF_pct=round(pct(m[k], ref['MF'][k]), 2)) for k in SKIN}
    SK = {s: json.load(open('%s/skp/%s_skp.json' % (PA, n))) for s, n in C.items() if s != 'HV0'}
    for hp, tag in (('HP-A', 'HB2HF2'), ('HP-B', 'HB2HF2-HPB'), ('HP-C', 'HB2HF2-HPC')):
        x = json.load(open('%s/skp/%s-%s_skp.json' % (HP, PRE[c], tag))); rows = {}
        for k in ('leg_share', 'bitroch_over_crest', 'pelvic_vertical_share', 'pelvic_vertical_over_crest', 'pelvic_depth_share', 'crest_share', 'waist_interval_over_torso', 'hip_joint_scale_share'):
            by = {}
            for tt in x['by_t']:
                g = lambda j: (j['leg_share'] if k == 'leg_share' else (j['by_t'][tt]['extra']['prox_femur'] / j['stature_r6'] if k == 'hip_joint_scale_share' else j['by_t'][tt]['ratio'][k]))
                v = g(x); by[tt] = dict(value=round(v, 5), **{'vs_%s_pct' % s: round(pct(v, g(SK[s])), 2) for s in SK})
            rows[k] = by
        sk = mz('%s/cand/%s-%s' % (HP, PRE[c], tag))
        res['hp']['%s %s' % (hp, c)] = dict(tag=tag, skeletal_proxy=rows, skin={k: round(sk[k], 5) for k in SKIN})
json.dump(res, open(OUT, 'w'), indent=1)
for k, v in res['hp'].items(): print(k, {q: (r['0.5']['value'], r['0.5']['vs_MF_pct'], r['0.5']['vs_FN_pct'], r['0.5']['vs_AE_pct'], r['0.5']['vs_VA_pct']) for q, r in v['skeletal_proxy'].items()})
for k, v in res['candidates'].items(): print(k, {q: (r['vs_current_HV_pct'], r['vs_MF_pct']) for q, r in v.items()})
