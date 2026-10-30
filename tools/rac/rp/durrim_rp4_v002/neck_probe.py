# neck_probe.py : the v005 submandibular 5-pole pair (5299 / 11904) in the validator neck-station frame (c = mid(neck_01, head), axis +z,
# crease band |z - zc| <= 0.5 h, h = median edge length with first vertex within R = 11 s of c). Library + CLI (local layout around the pole).
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import topo
POLES = (5299, 11904)
def frame(V, Q, meta):
    H = {k: np.array(v) for k, v in meta['heads'].items()}; s = (V[:, 2].max() - V[:, 2].min()) / 173.143; c = 0.5 * (H['neck_01'] + H['head'])
    uE, val = topo(np.asarray(Q), len(V)); wE = np.linalg.norm(V[uE[:, 0]] - V[uE[:, 1]], axis=1); near = np.linalg.norm(V[uE[:, 0]] - c, axis=1) < 11 * s
    return dict(c=c, s=s, h=float(np.median(wE[near])), Rp=11 * s, val=val, uE=uE)
def adjacency(Q, nV):
    nb = [set() for _ in range(nV)]
    for q in Q:
        for k in range(4): a, b = int(q[k]), int(q[(k + 1) % 4]); nb[a].add(b); nb[b].add(a)
    return nb
def crease_poles(V, Q, meta):
    F = frame(V, Q, meta); P = np.nonzero(F['val'] != 4)[0]; d = V[P] - F['c']; pb = d[:, 2]; pr = np.linalg.norm(d[:, :2], axis=1)
    m = pr <= F['Rp']; return F, {int(p): round(float(b / F['h']), 3) for p, b, mm in zip(P, pb, m) if mm and abs(b) <= 3 * F['h']}
if __name__ == '__main__':
    z = np.load(sys.argv[1]); V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta'])); F = frame(V, Q, meta); nb = adjacency(Q, len(V))
    p = POLES[0]; print('h %.4f  zc %.3f  pole %d at %s  t/h %+.2f  valence %d' % (F['h'], F['c'][2], p, np.round(V[p], 2), (V[p, 2] - F['c'][2]) / F['h'], F['val'][p]))
    ring = {p: 0}; frontier = [p]
    for k in range(1, 4):
        nxt = []
        for v in frontier:
            for w in nb[v]:
                if w not in ring: ring[w] = k; nxt.append(w)
        frontier = nxt
    for v, k in sorted(ring.items(), key=lambda kv: (kv[1], -V[kv[0], 2])):
        if k <= 2: print('  ring %d  v %5d  val %d  t/h %+.2f  xyz %s' % (k, v, F['val'][v], (V[v, 2] - F['c'][2]) / F['h'], np.round(V[v], 2)))
    _, cp = crease_poles(V, Q, meta); print('poles within 3h of the band (t/h):', cp)
