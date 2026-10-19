"""Usage: python3 ring2.py PREV.json TGT.json 'obs list' OUT.json  (prev ring scaled 0.6 about its xy median)"""
import sys, json, numpy as np
P = np.array(json.load(open(sys.argv[1])))[:, :2]; T = np.array(json.load(open(sys.argv[2]))); S = np.array(json.loads(sys.argv[3]), float)
m = P.mean(0); I = m + 0.6 * (P - m)
sx = np.linalg.lstsq(np.c_[I[:, 0], np.ones(10)], S[:, 0], rcond=None)[0]; sy = np.linalg.lstsq(np.c_[-I[:, 1], np.ones(10)], S[:, 1], rcond=None)[0]
print('fit', sx, sy); scr = lambda p: np.array([sx[0] * p[0] + sx[1], sy[0] * -p[1] + sy[1]])
print('resid', np.abs(np.array([scr(p) for p in I]) - S).max())
def nk(v): return [{'action': 'key', 'text': {'-': 'minus', '.': 'period'}.get(c, c)} for c in '%.4f' % v]
cur = [s.copy() for s in S]; acts = []
for i in range(10):
    d = min(np.linalg.norm(cur[i] - cur[j]) for j in range(10) if j != i)
    if d < 15: print('WARN', i, d)
    acts.append({'action': 'left_click', 'coordinate': [int(cur[i][0]), int(cur[i][1])]})
    acts += [{'action': 'double_click', 'coordinate': [1110, 92]}, {'action': 'wait', 'duration': 0.5}]
    for k, v in enumerate(T[i]): acts += [{'action': 'key', 'text': 'ctrl+a'}] + nk(v) + [{'action': 'key', 'text': 'Tab' if k < 2 else 'Return'}]
    cur[i] = scr(T[i])
acts += [{'action': 'mouse_move', 'coordinate': [700, 450]}, {'action': 'key', 'text': 'a'}, {'action': 'wait', 'duration': 0.5}, {'action': 'zoom', 'region': [1040, 56, 1180, 135]}]
json.dump(acts, open(sys.argv[4], 'w')); print(len(acts))
