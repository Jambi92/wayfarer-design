"""Generate per-vertex UI typing for digit tubes in a fixed Top-ortho view (no reframing).
Usage: python3 tubes_ui.py S role ax bx ay by OUTPREFIX  (screen x = ax*X+bx, y = ay*(-Y)+by)"""
import sys, json, numpy as np
S, role = sys.argv[1], sys.argv[2]; ax, bx, ay, by = map(float, sys.argv[3:7]); pre = sys.argv[7]
D = json.load(open('design_%s.json' % S))
P4 = np.array(D['rings']['P4']['d'] + D['rings']['P4']['p'][::-1]) / 100  # d0..d4,p4..p0
def d_(k): return P4[k]
def p_(k): return P4[9 - k]
k = ['index', 'middle', 'ring', 'pinky'].index(role) if role != 'thumb' else None
if role == 'thumb':
    R = {nm: np.array(D['rings'][nm]['d'] + D['rings'][nm]['p'][::-1]) / 100 for nm in D['ring_names']}
    ta, tb = D['thumb_between']; base = np.array([R[ta][9], R[ta][8], R[tb][8], R[tb][9]])
else:
    base = np.array([d_(k), d_(k + 1), p_(k + 1), p_(k)])
rings = np.array(D['tubes'][role]) / 100
best = None
for sh in range(4):
    for rev in (False, True):
        o = [(sh + j) % 4 for j in range(4)]
        if rev: o = o[::-1]
        c = np.linalg.norm(base - rings[0][o], axis=1).sum()
        if best is None or c < best[0]: best = (c, o)
o = best[1]
scr = lambda p: np.array([ax * p[0] + bx, ay * -p[1] + by])
def nk(v):
    t = ('%.4f' % v).replace('0.', '.', 1) if abs(v) < 1 else '%.4f' % v
    return [{'action': 'key', 'text': {'-': 'minus', '.': 'period'}.get(c, c)} for c in t]
cur = [base[j].copy() for j in range(4)]; acts = []; warn = 0
print('base centre screen', scr(base.mean(0)).round(0), 'corr', o)
for ri, r in enumerate(rings):
    acts += [{'action': 'key', 'text': 'e'}, {'action': 'key', 'text': 'Escape'}, {'action': 'key', 'text': 'shift+h'}, {'action': 'wait', 'duration': 0.3}]
    tgt = [r[o[j]] for j in range(4)]
    todo = list(range(4)); order = []
    while todo:   # pick a vertex whose click spot is clear of all other visible verts
        sc = {j: min(np.linalg.norm(scr(cur[j]) - scr(cur[i])) for i in range(4) if i != j) for j in todo}
        j = max(todo, key=lambda t: sc[t]); order.append(j); todo.remove(j)
        if sc[j] < 12: print('WARN ring', ri, 'v', j, 'clear', round(sc[j], 1)); warn += 1
        p = scr(cur[j])
        if not (45 < p[1] < 715 and 45 < p[0] < 1030): print('OFFSCREEN ring', ri, p); warn += 1
        acts.append({'action': 'left_click', 'coordinate': [int(round(p[0])), int(round(p[1]))]})
        acts += [{'action': 'double_click', 'coordinate': [1110, 92]}, {'action': 'wait', 'duration': 0.5}]
        for kk, v in enumerate(tgt[j]): acts += ([{'action': 'key', 'text': 'ctrl+a'}] if kk == 0 else []) + nk(v) + [{'action': 'key', 'text': 'Tab' if kk < 2 else 'Return'}]
        cur[j] = tgt[j].copy()
    # reselect the ring (4 verts) : select all visible
    acts += [{'action': 'mouse_move', 'coordinate': [700, 450]}, {'action': 'key', 'text': 'a'}, {'action': 'wait', 'duration': 0.3}]
json.dump(acts, open(pre + '.json', 'w'))
json.dump([c.tolist() for c in cur], open(pre + '_tip.json', 'w'))
print(role, 'rings', len(rings), 'actions', len(acts), 'warn', warn)
