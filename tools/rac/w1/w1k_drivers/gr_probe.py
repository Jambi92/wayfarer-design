# RAC W1k probe: documented construction (spine_01 removed) with pelvis X varied; skeletal GR-P2b / GR-P5 / GR-P6 only. Diagnostic.
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers')
import gn3
px = float(sys.argv[1]); nm = 'GRP%03d' % round(px * 1000); wd = gn3.S + '/w1k/probe'
gn3.build('GR', nm, {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [px, 1.0, 1.0]}, wd=wd)
rows = [r for r in gn3.checks('GR', nm, wd=wd) if r.get('cand') == 'GR']
out = {r['check']: [r.get('va'), r.get('vb'), r.get('result')] for r in rows if any(s in r['check'] for s in ('P2b', 'P5', 'P6'))}
json.dump(out, open(wd + '/%s_rows.json' % nm, 'w'), indent=1, default=float); print(px, json.dumps(out, default=float), flush=True)
