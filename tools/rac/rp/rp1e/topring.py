"""Generate UI actions to type a ring's vertices in a Top-ortho, ring-only view.
Usage: python3 topring.py INIT.json TARGET.json ax bx ay by s OUT.json"""
import sys, json, numpy as np
I = np.array(json.load(open(sys.argv[1]))); T = np.array(json.load(open(sys.argv[2])))
ax, bx, s, by = float(sys.argv[3]), 0, 0, 0
ax, ay, s = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]); out = sys.argv[6]
scr = lambda p: np.array([ax + s * p[0], ay - s * p[1]])
def nk(v):
    t = '%.4f' % v; m = {'-': 'minus', '.': 'period'}; return [{'action': 'key', 'text': m.get(c, c)} for c in t]
cur = [scr(p) for p in I]; acts = []; placed = []
for i in range(len(I)):
    c = cur[i]; others = [cur[j] for j in range(len(I)) if j != i]
    dmin = min(np.linalg.norm(c - o) for o in others)
    if dmin < 12: print('WARN', i, dmin)
    acts.append({'action': 'left_click', 'coordinate': [int(round(c[0])), int(round(c[1]))]})
    acts.append({'action': 'double_click', 'coordinate': [1110, 92]}); acts.append({'action': 'wait', 'duration': 0.5})
    for k, v in enumerate(T[i]):
        acts.append({'action': 'key', 'text': 'ctrl+a'}); acts += nk(v); acts.append({'action': 'key', 'text': 'Tab' if k < 2 else 'Return'})
    cur[i] = scr(T[i])
json.dump(acts, open(out, 'w')); print(len(acts))
