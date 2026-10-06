# RAC W1g driver AS RUN: least-extreme refinement. From a feasible gn4 point, move each parameter toward its generator value
# (1.0; ka amplitude toward 0) in steps of 1/3 of its deviation, largest deviation first; keep a move only if every gn4
# constraint still holds (summed residual <= TOL = 0.0006, see below). Usage: python3 shrink.py x.json passes tag
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers')
import gn4
x = np.array(json.loads(sys.argv[1]), float); passes = int(sys.argv[2]); tag = sys.argv[3]
f = open(gn4.gn3.G + '/shrink_%s.log' % tag, 'a')
TOL = 0.0006   # summed residual tolerated (the ALPC-3 shaft row passes by 0.25 % against the solver's 0.3 % margin)
feas = lambda mm: -mm[mm < 0].sum() <= TOL
m, lab, H, C = gn4.slacks(x, tag); ok = feas(m)
print('start feasible', ok, 'sumneg %.4f' % -m[m < 0].sum(), json.dumps(dict(zip(gn4.NAMES, np.round(x, 4).tolist()))), file=f, flush=True)
for k in np.where(m < 0)[0]: print('   neg', lab[k], round(m[k], 4), file=f, flush=True)
tgt = np.array([0.0 if n == "Aka" else 1.0 for n in gn4.NAMES])
for p in range(passes):
    order = np.argsort(-np.abs(x - tgt))
    for i in order:
        if abs(x[i] - tgt[i]) < 0.01: continue
        xn = x.copy(); xn[i] = tgt[i] + (x[i] - tgt[i]) * 0.67
        mn, _, Hn, _ = gn4.slacks(xn, tag + 's')
        acc = feas(mn)
        print('pass %d %s %.4f -> %.4f  %s  sumneg %.4f' % (p, gn4.NAMES[i], x[i], xn[i], 'KEEP' if acc else 'reject', -mn[mn < 0].sum()), file=f, flush=True)
        if acc: x, m = xn, mn; ok = feas(m)
json.dump({"x": x.tolist(), "names": gn4.NAMES, "feasible": bool(ok)}, open(gn4.gn3.G + '/shrink_%s_best.json' % tag, 'w'), indent=1)
print('DONE', ok, json.dumps(dict(zip(gn4.NAMES, np.round(x, 4).tolist()))), file=f, flush=True)
