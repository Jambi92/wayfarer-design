# thumb_grid.py : align the v005 thumb rings into a (column, row) grid via strip connectivity, in the validator frames.
#   grid(z, side) -> dict(G = int array [rows, 20] of v005 vertex ids (row 0 = most proximal found ring, columns aligned so G[r,k]-G[r+1,k] is a rung edge),
#                         t (ring mean t along thumb_02 axis), F (ring frame), Fc (crease frame: c, dc, Rp, h0))
# Library for the v002 thumb patch; CLI prints per-vertex (pb, pr) in the crease frame and the long-column positions.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002')
from thumb_rings import rings, orient
def edges_of(Q):
    E = set()
    for q in Q:
        for k in range(4): a, b = int(q[k]), int(q[(k + 1) % 4]); E.add((min(a, b), max(a, b)))
    return E
def grid(z, side, nrows=None):
    F, R = rings(z, side); Q = np.asarray(z['Q']); E = edges_of(Q)
    Ls = [orient(F, L) for t, L, rm in R]; ts = [t for t, L, rm in R]
    # keep the consecutive run of rings joined by rungs, starting at the ring nearest t = 0
    k0 = int(np.argmin(np.abs(ts))); rows = [Ls[k0]]; rt = [ts[k0]]
    for j in range(k0 + 1, len(Ls)):
        prev = rows[-1]; L = Ls[j]; pos = {int(v): i for i, v in enumerate(L)}
        match = [next((pos[w] for w in pos if (min(int(v), w), max(int(v), w)) in E), None) for v in prev]
        if any(m is None for m in match): break
        sh = (match[0]) % len(L)
        if not all((match[i] - i - sh) % len(L) == 0 for i in range(len(L))): break
        rows.append(np.roll(L, -sh)); rt.append(ts[j])
        if nrows and len(rows) >= nrows: break
    # one ring proximal of the seed (Z-1) if it exists, aligned
    G = np.array(rows); return dict(G=G, t=np.array(rt), F=F)
def crease_frame(z, side):
    meta = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}; V = z['V'].astype(float)
    s = (V[:, 2].max() - V[:, 2].min()) / 173.143; c = H['thumb_02_' + side]; d = H['thumb_03_' + side] - H['thumb_01_' + side]; d /= np.linalg.norm(d)
    return dict(c=c, d=d, Rp=2.0 * s, Rr=2.0 * s, s=s)
def pb_pr(V, ids, Fc):
    P = V[ids] - Fc['c']; pb = P @ Fc['d']; pr = np.linalg.norm(P - np.outer(pb, Fc['d']), axis=1); return pb, pr
if __name__ == '__main__':
    z = np.load(sys.argv[1]); side = sys.argv[2] if len(sys.argv) > 2 else 'l'; g = grid(z, side, 8); V = z['V'].astype(float); Fc = crease_frame(z, side); G = g['G']
    print('rows', G.shape, 't', np.round(g['t'], 3), 'Rp %.3f' % Fc['Rp'])
    for r in range(len(G)):
        pb, pr = pb_pr(V, G[r], Fc); seg = np.linalg.norm(V[G[r]] - V[np.roll(G[r], -1)], axis=1)
        print('row %d  pb[%s]' % (r, ' '.join('%+.2f' % x for x in pb)))
        print('       pr[%s]' % ' '.join('%5.2f' % x for x in pr))
        print('      seg[%s]' % ' '.join('%5.2f' % x for x in seg))
        if r + 1 < len(G): rung = np.linalg.norm(V[G[r]] - V[G[r + 1]], axis=1); print('     rung[%s]' % ' '.join('%5.2f' % x for x in rung))
