"""UI actions for palm rings P1..P4 of hand S (fixed Top ortho view; x = ax*X+bx, y = ay*(-Y)+by), starting from W0 ids in the UI file.
Usage: python3 palm_ui.py S ax bx ay by uiV.npz 'w0ids' OUT.json"""
import sys, json, numpy as np
S = sys.argv[1]; ax, bx, ay, by = map(float, sys.argv[2:6]); U = np.load(sys.argv[6])['V'] / 100; w0 = json.loads(sys.argv[7]); out = sys.argv[8]
D = json.load(open('design_%s.json' % S))
scr = lambda p: np.array([ax * p[0] + bx, ay * -p[1] + by])
def nk(v):
    t = ('%.4f' % v).replace('0.', '.', 1) if abs(v) < 1 else '%.4f' % v
    return [{'action': 'key', 'text': {'-': 'minus', '.': 'period'}.get(c, c)} for c in t]
cur = [U[i].copy() for i in w0]; acts = []
for nm in D['ring_names']:
    tgt = np.array(D['rings'][nm]['d'] + D['rings'][nm]['p'][::-1]) / 100
    acts += [{'action': 'key', 'text': 'e'}, {'action': 'key', 'text': 'Escape'}, {'action': 'key', 'text': 'shift+h'}, {'action': 'wait', 'duration': 0.3}]
    todo = list(range(10))
    while todo:
        sc = {j: min(np.linalg.norm(scr(cur[j]) - scr(cur[i])) for i in range(10) if i != j) for j in todo}
        j = max(todo, key=lambda t: sc[t]); todo.remove(j)
        if sc[j] < 12: print('WARN', nm, j, round(sc[j], 1))
        p = scr(cur[j])
        if not (45 < p[1] < 715 and 45 < p[0] < 1030): print('OFFSCREEN', nm, p)
        acts += [{'action': 'left_click', 'coordinate': [int(round(p[0])), int(round(p[1]))]}, {'action': 'double_click', 'coordinate': [1110, 92]}, {'action': 'wait', 'duration': 0.5}]
        for kk, v in enumerate(tgt[j]): acts += ([{'action': 'key', 'text': 'ctrl+a'}] if kk == 0 else []) + nk(v) + [{'action': 'key', 'text': 'Tab' if kk < 2 else 'Return'}]
        cur[j] = tgt[j].copy()
    acts += [{'action': 'mouse_move', 'coordinate': [700, 450]}, {'action': 'key', 'text': 'a'}, {'action': 'wait', 'duration': 0.3}]
    print(nm, 'median', tgt.mean(0).round(5))
json.dump(acts, open(out, 'w')); print(len(acts))
