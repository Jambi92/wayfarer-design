"""Two-view greedy planner: Top view first (clearance >= minsep), then Front view for the rest.
Top: sx = a + s*x, sy = bt - s*y ; Front: sx = a + s*x, sy = bf - s*z (cm)."""
import numpy as np, json, sys
sys.path.insert(0, '.')
from uigen import keys
def acts_for(p, t, field=(1110, 92)):
    a = [{'action': 'left_click', 'coordinate': [int(round(p[0])), int(round(p[1]))], 'action_summary': 'Selects vertex'},
         {'action': 'double_click', 'coordinate': list(field), 'action_summary': 'Edits vertex X'}, {'action': 'wait', 'duration': 0.3}]
    for k in range(3): a += [{'action': 'key', 'text': 'ctrl+a'}] + keys(t[k] / 100) + [{'action': 'key', 'text': 'Tab' if k < 2 else 'Return'}]
    return a
def plan2(cur, tgt, a, s, bt, bf, minsep=14):
    cur = np.array(cur, float).copy(); tgt = np.array(tgt, float)
    views = {'top': lambda P: np.c_[a + s * P[:, 0], bt - s * P[:, 1]], 'front': lambda P: np.c_[a + s * P[:, 0], bf - s * P[:, 2]]}
    out = {'top': [], 'front': [], 'left': []}; todo = list(range(len(cur)))
    for vname in ['top', 'front']:
        f = views[vname]
        while True:
            S = f(cur); best = None
            for i in todo:
                d = np.linalg.norm(S - S[i], axis=1); d[i] = 1e9
                if best is None or d.min() > best[1]: best = (i, d.min())
            if best is None or best[1] < minsep: break
            i, c = best; out[vname].append(dict(i=i, clr=float(c), acts=acts_for(S[i], tgt[i]))); cur[i] = tgt[i]; todo.remove(i)
    out['left'] = todo
    # for leftovers report best clearance in either view
    for i in todo:
        r = []
        for vname, f in views.items():
            S = f(cur); d = np.linalg.norm(S - S[i], axis=1); d[i] = 1e9; r.append((vname, round(float(d.min()), 1), S[i].round(1).tolist()))
        print('LEFT', i, r, (cur[i] / 100).round(4).tolist(), (tgt[i] / 100).round(4).tolist())
    return out
if __name__ == '__main__':
    k = int(sys.argv[1]); p = json.load(open('feet_plan.json'))
    cur = np.vstack([np.array(p[s]['rings'][k - 1]) for s in 'LR']); cur[:, 2] -= 3
    tgt = np.vstack([np.array(p[s]['rings'][k]) for s in 'LR'])
    s = 10.6; a = 598.25; bt = -91.85; bf = 374.5 + s * 5
    out = plan2(cur, tgt, a, s, bt, bf, float(sys.argv[2]) if len(sys.argv) > 2 else 14)
    json.dump(out, open('ui2_ring%d.json' % k, 'w'))
    print('top', len(out['top']), 'front', len(out['front']), 'left', out['left'])
