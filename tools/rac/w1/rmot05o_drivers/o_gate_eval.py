# RM-OT-05O revised neutralized structural gate: mechanical evaluation of the PRE-REGISTERED rules
# (reviews/rac-rmot05o-evidence/blind/PREREGISTRATION.md). Usage: python3 o_gate_eval.py KEY.json S1 S2 S3 [-- KEY2 S1 S2 S3]
import sys, json
STRUCT = {'axial_section_shape', 'joint_integration', 'segment_relations', 'load_path'}
def run(key, scs):
    c = key['codes']; ref, low = c['GO-S-ref'], c['GO-S-low']; gr = [c['GR-E3-ref'], c['GR-E3-low']]
    mf = [v for k, v in c.items() if k.startswith('MF-')]; skb = c['SK-brd']; ctrl = [v for k, v in c.items() if k.startswith(('MF-', 'SK-'))]
    def grp(s, code): return next((g for g in s.get('groups', []) if code in g['codes']), None)
    n1 = n2 = n3 = n4 = 0; c5 = {'ref': 0, 'low': 0}; detail = []
    for s in scs:
        g = grp(s, ref); same = g is not None and low in g['codes']
        if same and g.get('stable') and not any(x in g['codes'] for x in ctrl + gr): n1 += 1
        if not (g and any(x in g['codes'] for x in mf)) and not (grp(s, low) and any(x in grp(s, low)['codes'] for x in mf)) and s['bodies'][ref]['class'] != 'A' and s['bodies'][low]['class'] != 'A': n2 += 1
        if not ((g and skb in g['codes']) or (grp(s, low) and skb in grp(s, low)['codes'])): n3 += 1
        if g is not None and all(grp(s, x) is not g for x in gr): n4 += 1
        row = {}
        for tag, code in (('ref', ref), ('low', low)):
            b = s['bodies'][code]; nf = b.get('non_structural_factors', {})
            ok = b.get('primary_driver') in STRUCT and all(nf.get(k) in ('none', 'minor') for k in ('posture_pose', 'fat', 'muscularity', 'boxiness')) and not b.get('posture_read')
            c5[tag] += ok
            row[tag] = dict(primary_driver=b.get('primary_driver'), posture_read=b.get('posture_read'), **{k: nf.get(k) for k in ('posture_pose', 'limb_bulk', 'fat', 'muscularity', 'boxiness')}, c5_ok=ok)
        row['group_label'] = g['label'] if g else None; detail.append(row)
    res = dict(C1_stable_same_type=n1 >= 2, C2_no_Marchfolk_collapse=n2 >= 2, C3_no_SkarnBroad_collapse=n3 >= 2, C4_distinct_from_Grask=n4 >= 2,
               C5_structural_reasons=(c5['ref'] >= 2 and c5['low'] >= 2), counts=dict(C1=n1, C2=n2, C3=n3, C4=n4, C5_ref=c5['ref'], C5_low=c5['low']), per_scorer=detail)
    res['run_pass_C1_C5'] = all(res[k] for k in ('C1_stable_same_type', 'C2_no_Marchfolk_collapse', 'C3_no_SkarnBroad_collapse', 'C4_distinct_from_Grask', 'C5_structural_reasons'))
    return res
args = sys.argv[1:]; runs = []
while args:
    k = args[0]; s = args[1:4]; args = args[5:] if len(args) > 4 and args[4] == '--' else args[4:]
    runs.append(dict(key=k.split('/')[-1], **run(json.load(open(k)), [json.load(open(x)) for x in s])))
out = dict(runs=runs, gate_pass=len(runs) >= 2 and all(r['run_pass_C1_C5'] for r in runs), C6='assessed only in the full-organism confirmation, which runs only if C1-C5 pass in both runs')
print(json.dumps(out, indent=1))
