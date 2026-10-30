# thumb_rings.py FAM.npz [side] : v005 thumb-MCP ring structure, exactly in the validator's frame (ring station thumb_ip1 = thumb_02 head / thumb_02 axis,
# anatomical radius 3.0 s, window 0.8 s; crease station thumb_mcp = thumb_02 head, axis thumb_03 head - thumb_01 head, R 2.0 s).
# Returns ordered closed rings (consistent orientation) with t (cm), r_max, segment lengths, and the stature-scaled limits. Library + CLI.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import closed_loops, encircling
REF = 173.143
def frame(z, side):
    meta = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}; T = {k: np.array(v) for k, v in meta['tails'].items()}
    V = z['V'].astype(float); s = (V[:, 2].max() - V[:, 2].min()) / REF
    c = H['thumb_02_' + side]; d = T['thumb_02_' + side] - H['thumb_02_' + side]; d /= np.linalg.norm(d)
    dc = H['thumb_03_' + side] - H['thumb_01_' + side]; dc /= np.linalg.norm(dc)
    return dict(V=V, s=s, c=c, d=d, dc=dc, rlim=3.0 * s, win=0.8 * s, Rp=2.0 * s)
def rings(z, side, loops=None, search=1.6):
    F = frame(z, side); V = F['V']; Q = np.asarray(z['Q']); loops = closed_loops(Q, len(V)) if loops is None else loops
    ids = encircling(V, loops, F['c'], F['d'], F['rlim'] * search, F['win'] * 3.5)
    out = []
    for li in ids:
        L = loops[li]; P = V[L] - F['c']; t = P @ F['d']; rad = P - np.outer(t, F['d']); out.append((float(t.mean()), L, float(np.linalg.norm(rad, axis=1).max())))
    out.sort(key=lambda x: x[0]); return F, out
def orient(F, L, ref=None):
    """rotate / reverse ring L so it runs counter-clockwise about d and starts at the vertex closest in angle to ref (or index-min)"""
    V = F['V']; d = F['d']; u = np.cross(d, [0, 0, 1.0]); u /= np.linalg.norm(u); w = np.cross(d, u)
    P = V[L] - F['c']; th = np.arctan2(P @ w, P @ u); dth = (np.diff(np.r_[th, th[0]]) + np.pi) % (2 * np.pi) - np.pi
    L = np.asarray(L)
    if dth.sum() < 0: L = L[::-1]; th = th[::-1]
    k0 = int(np.argmin(np.abs((th - (ref if ref is not None else 0) + np.pi) % (2 * np.pi) - np.pi)))
    return np.roll(L, -k0)
if __name__ == '__main__':
    z = np.load(sys.argv[1]); side = sys.argv[2] if len(sys.argv) > 2 else 'l'
    F, R = rings(z, side); V = F['V']
    print('s %.4f rlim %.3f win %.3f Rp %.3f' % (F['s'], F['rlim'], F['win'], F['Rp']))
    for t, L, rm in R:
        seg = np.linalg.norm(V[L] - V[np.roll(L, -1)], axis=1)
        print('t %+.3f  n %2d  rmax %.2f  %s  seg %.2f..%.2f  [%s]' % (t, len(L), rm, 'R' if rm <= F['rlim'] else '-', seg.min(), seg.max(), ' '.join('%.2f' % x for x in seg)))
