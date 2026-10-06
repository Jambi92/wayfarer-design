# RAC W1h probe AS RUN (thoracic breadth vs SK on the directional reading; reference body only)
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers')
import gn5
x0 = json.load(open('/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GO_params.json'))['x']
N = gn5.NAMES
V0 = {"T0": {}, "T1": {"kb60": 1.06}, "T2": {"kb60": 1.06, "kb44": 0.95}, "T3": {"kb80": 1.18}, "T4": {"kb60": 1.08, "kb80": 1.17}}
xx = dict(zip(N, x0)); KB = [n for n in N if n.startswith('kb')]; KP = [n for n in N if n.startswith('kp')]
V6 = {"T6": {**{n: xx[n] * 1.017 for n in KB}, **{n: xx[n] * 1.017 for n in KP}}, "T7": {**{n: xx[n] * 1.017 for n in KB}, **{n: xx[n] * 1.03 for n in KP}}}
T7 = {**{n: xx[n] * 1.017 for n in KB}, **{n: xx[n] * 1.03 for n in KP}}
V = {"T9": {**T7, "thigh": 1.28}, "T10": {**T7, "kb0": xx["kb0"] * 1.04}}
for tag, ch in V.items():
    x = list(x0)
    for k, v in ch.items(): x[N.index(k)] = v
    m, lab, H, C = gn5.slacks(np.array(x), 'PT' + tag, with_stress=False)
    neg = [(lab[k], round(m[k], 4)) for k in np.where(m < 0)[0]]
    import gn3; bad=[(y['result'],y['check'][:60]) for y in gn3.checks('GO','PT'+tag,wd=gn5.G+'/solve5') if (y['cand']=='GO' or y.get('b')=='GO') and y['result'] not in ('PASS','REPORT','NOT RUN')]
    print(tag, 'ORDINARY RULE not-pass:', bad, ch, 'H %.2f' % H, [l for l in lab if 'TB' in l or 'clearance' in l or 'flare' in l], 'neg', neg, flush=True)
