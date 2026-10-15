# RM-OT-05V: mechanical evaluation of the PRE-REGISTERED REF-only rules (reviews/rac-rmot05v-evidence/blind/PREREGISTRATION.md);
# o_gate_eval.py (05O) is unchanged. Usage: python3 v_gate_eval.py KEY.json S1.json S2.json S3.json [-- KEY2 S1 S2 S3] > OUT.json
import sys, json
STRUCT = {'axial_section_shape', 'joint_integration', 'segment_relations', 'load_path'}
def run(key, scs):
    c = key['codes']; ref = c['GO-S-ref']; gr = [c['GR-E3-ref'], c['GR-E3-low']]; mf = [v for k, v in c.items() if k.startswith('MF-')]; skb = c['SK-brd']
    def grp(s, code): return next((g for g in s.get('groups', []) if code in g['codes']), None)
    n2 = n3 = n4 = n5 = 0; detail = []
    for s in scs:
        g = grp(s, ref); b = s['bodies'][ref]; nf = b.get('non_structural_factors', {})
        if not (g and any(x in g['codes'] for x in mf)) and b['class'] != 'A': n2 += 1
        if not (g and skb in g['codes']): n3 += 1
        if g is None or all(x not in g['codes'] for x in gr): n4 += 1
        ok5 = b.get('primary_driver') in STRUCT and all(nf.get(k) in ('none', 'minor') for k in ('posture_pose', 'fat', 'muscularity', 'boxiness')) and not b.get('posture_read')
        n5 += ok5
        detail.append(dict(cls=b['class'], confidence=b.get('confidence'), basis=b.get('basis'), primary_driver=b.get('primary_driver'), posture_read=b.get('posture_read'),
                           **{k: nf.get(k) for k in ('posture_pose', 'limb_bulk', 'fat', 'muscularity', 'boxiness')}, c5_ok=ok5,
                           group_label=g['label'] if g else None, group_codes=g['codes'] if g else None, drivers=b.get('drivers')))
    res = dict(C2_no_Marchfolk_collapse=n2 >= 2, C3_no_SkarnBroad_collapse=n3 >= 2, C4_distinct_from_Grask=n4 >= 2, C5_REF_structural_reasons=n5 >= 2,
               C1='NOT EVALUABLE (no LOW)', C5_LOW='NOT EVALUABLE (no LOW)', counts=dict(C2=n2, C3=n3, C4=n4, C5_REF=n5), per_scorer=detail)
    res['REF_criteria_pass'] = all(res[k] for k in ('C2_no_Marchfolk_collapse', 'C3_no_SkarnBroad_collapse', 'C4_distinct_from_Grask', 'C5_REF_structural_reasons'))
    return res
args = sys.argv[1:]; runs = []
while args:
    k = args[0]; s = args[1:4]; args = args[5:] if len(args) > 4 and args[4] == '--' else args[4:]
    runs.append(dict(key=k.split('/')[-1], **run(json.load(open(k)), [json.load(open(x)) for x in s])))
print(json.dumps(dict(runs=runs, REF_criteria_pass_both_runs=all(r['REF_criteria_pass'] for r in runs),
                      gate_verdict='CANNOT PASS AS PRE-REGISTERED (C1 / C5-LOW not evaluable)' if all(r['REF_criteria_pass'] for r in runs) else 'FAIL'), indent=1))
