# RAC RM-OT-05F tally self-test: synthetic scorer outputs (no real bodies) that must PASS / FAIL f_tally exactly as specified.
import json, os, subprocess, sys, tempfile
D = os.path.dirname(os.path.abspath(__file__))
keys = ['MF-ref', 'MF-nar', 'MF-brd', 'MF-low', 'SK-ref', 'SK-nar', 'SK-brd', 'SK-low', 'GR-E3-ref', 'GR-E3-low', 'GO-S-ref', 'GO-S-low']
key = {'codes': {k: 'Z%02d' % (i + 1) for i, k in enumerate(keys)}}; c = key['codes']
def scorer(go_class='C', basis='organization', group_ctrl=False, merge_grask=False, cues=True, ctrlC=False):
    b = {}
    for k, v in c.items():
        if k.startswith('GO'): b[v] = {'class': go_class, 'basis': basis, 'axial_cues': ['slab'] if cues else [], 'limb_cues': ['knee plate'] if cues else [], 'posture_read': False}
        elif k.startswith('GR'): b[v] = {'class': 'C', 'basis': 'organization', 'axial_cues': ['hump'], 'limb_cues': ['calf'], 'posture_read': True}
        else: b[v] = {'class': 'C' if (ctrlC and k == 'SK-brd') else 'A', 'basis': 'n/a', 'axial_cues': [], 'limb_cues': [], 'posture_read': False}
    go = [c['GO-S-ref'], c['GO-S-low']] + ([c['SK-brd']] if group_ctrl else []) + ([c['GR-E3-ref'], c['GR-E3-low']] if merge_grask else [])
    groups = [{'label': 'go', 'codes': go, 'stable': True}]
    if not merge_grask: groups.append({'label': 'gr', 'codes': [c['GR-E3-ref'], c['GR-E3-low']], 'stable': True})
    return {'bodies': b, 'groups': groups, 'nonhuman_groups_distinguishable': not merge_grask}
cases = {'pass': [dict()] * 3, 'fail_bulk': [dict(basis='bulk')] * 2 + [dict()], 'fail_lowB': [dict(go_class='B')] * 2 + [dict()],
         'fail_control_group': [dict(group_ctrl=True)] * 2 + [dict()], 'fail_merge_grask': [dict(merge_grask=True)] * 2 + [dict()],
         'fail_no_cues': [dict(cues=False)] * 2 + [dict()], 'fail_control_C': [dict(ctrlC=True)] * 2 + [dict()]}
t = tempfile.mkdtemp(); kp = t + '/key.json'; json.dump(key, open(kp, 'w')); res = {}
for nm, sc in cases.items():
    ps = []
    for i, s in enumerate(sc): p = '%s/%s_%d.json' % (t, nm, i); json.dump(scorer(**s), open(p, 'w')); ps.append(p)
    args = [kp] + ps + ['--', kp] + [ps[0], ps[1], ps[2]]
    if nm == 'fail_lowB':   # only the low state is B: rebuild with ref C, low B
        for i in range(2):
            d = json.load(open(ps[i])); d['bodies'][c['GO-S-ref']]['class'] = 'C'; json.dump(d, open(ps[i], 'w'))
    out = json.loads(subprocess.run(['python3', D + '/f_tally.py'] + args, capture_output=True, text=True).stdout)
    res[nm] = out['gate_pass']
one = json.loads(subprocess.run(['python3', D + '/f_tally.py', kp] + ['%s/pass_%d.json' % (t, i) for i in range(3)], capture_output=True, text=True).stdout)['gate_pass']
res['single_run_only'] = one
expect = {'pass': True, 'single_run_only': False, **{k: False for k in cases if k.startswith('fail')}}
print(json.dumps(res), 'SELFTEST', 'OK' if res == expect else 'MISMATCH')
sys.exit(0 if res == expect else 1)
