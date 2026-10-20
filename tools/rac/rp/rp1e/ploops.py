# planar section loops of the frozen source (blender cm frame, weld.npz) for an arbitrary plane
import numpy as np
_W = None
def src():
    global _W
    if _W is None:
        w = np.load('/home/claude/stc/rp1/weld.npz'); _W = (w['V'].astype(float), w['F'].astype(np.int64))
    return _W
def plane_loops(p0, n, box_c=None, box_r=None, V=None, F=None):
    """returns list of (pts[k,3], faces[k], edges[k,2]) closed/open chains of the plane section; optionally limited to a ball."""
    if V is None: V, F = src()
    n = np.asarray(n, float); n /= np.linalg.norm(n); d = (V - p0) @ n
    if box_c is not None:
        fm = np.linalg.norm(V[F].mean(1) - box_c, axis=1) < box_r
    else: fm = np.ones(len(F), bool)
    s = np.sign(d[F]); s[s == 0] = 1; cut = fm & (s.min(1) < 0) & (s.max(1) > 0); fi = np.where(cut)[0]
    seg = {}  # edge key -> list of faces
    fe = []
    for f in fi:
        t = F[f]; es = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a, b = t[i], t[j]
            if s[f, i] != s[f, j]: es.append((min(a, b), max(a, b)))
        if len(es) == 2:
            fe.append((f, es[0], es[1]))
            for e in es: seg.setdefault(e, []).append(len(fe) - 1)
    used = np.zeros(len(fe), bool); loops = []
    def pt(e):
        a, b = e; al = d[a] / (d[a] - d[b]); return V[a] + (V[b] - V[a]) * al
    for k in range(len(fe)):
        if used[k]: continue
        used[k] = True; chain_f = [fe[k][0]]; chain_e = [fe[k][1], fe[k][2]]
        for direction in (0, 1):
            while True:
                e = chain_e[-1] if direction == 0 else chain_e[0]
                nxt = [m for m in seg.get(e, []) if not used[m]]
                if not nxt: break
                m = nxt[0]; used[m] = True; f, e1, e2 = fe[m]; ne = e2 if e1 == e else e1
                if direction == 0: chain_f.append(f); chain_e.append(ne)
                else: chain_f.insert(0, f); chain_e.insert(0, ne)
        closed = chain_e[0] == chain_e[-1]
        loops.append(dict(pts=np.array([pt(e) for e in chain_e]), faces=np.array(chain_f), edges=np.array(chain_e), closed=closed))
    return loops
