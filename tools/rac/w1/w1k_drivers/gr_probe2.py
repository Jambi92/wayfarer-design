# RAC W1l probe: documented construction (spine_01 lumbar narrowing removed), pelvis X and proximal-femur robusticity
# (LR:thigh X/Z cross-section scale; length Y unchanged) varied. Skeletal CIB rows GR-P2b / P5 / P6 / G1 + stature. Diagnostic.
# Usage: python3 gr_probe2.py PELVIS_X THIGH_XZ
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers')
import gn3
px, tx = float(sys.argv[1]), float(sys.argv[2]); nm = 'GRL%03d_%03d' % (round(px * 1000), round(tx * 1000)); wd = gn3.S + '/w1l/probe'
r, C = gn3.build('GR', nm, {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [px, 1.0, 1.0], "LR:thigh": [tx, 1.0, tx]}, wd=wd)
rows = [x for x in gn3.checks('GR', nm, wd=wd) if x.get('cand') == 'GR' or x.get('b') == 'GR']
out = {"pelvis_x": px, "thigh_xz": tx, "stature": r['r6']['stature'], "rows": {x['check']: [x.get('va'), x.get('vb'), x.get('result')] for x in rows}}
json.dump(out, open(wd + '/%s_rows.json' % nm, 'w'), indent=1, default=float)
print(px, tx, {k[:30]: v[2] for k, v in out["rows"].items() if v[2] != 'PASS'} or 'ALL PASS',
      {k[:14]: round(v[0], 4) for k, v in out["rows"].items() if any(s in k for s in ('P2b', 'P6'))}, flush=True)
