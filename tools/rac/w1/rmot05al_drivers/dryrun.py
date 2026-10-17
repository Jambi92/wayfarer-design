# RM-OT-05AL diagnostic (never saved/promoted): numerical replica of Blender's Mesh Filter "Surface Smooth"
# (sculpt_smooth surface_smooth_laplacian_step + surface_smooth_displace_step) applied with fade = f*(1-mask).
# usage as module: run(V, F, mask, f, steps=1, alpha=0.5, beta=0.5) -> V'
import numpy as np, scipy.sparse as sp
def adjacency(F, n):
    E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(float); deg = np.asarray(A.sum(1)).ravel(); return sp.diags(1 / np.maximum(deg, 1)) @ A
def run(V, F, mask, f, steps=1, alpha=0.5, beta=0.5, Avg=None):
    Avg = adjacency(F, len(V)) if Avg is None else Avg
    fade = (f * (1 - mask))[:, None]; orig = V.copy(); co = V.copy()
    for _ in range(steps):
        lap = Avg @ co
        disp = lap - (alpha * orig + (1 - alpha) * co)
        co = co + (lap - co) * fade
        bavg = Avg @ disp
        co = co - (beta * disp + (1 - beta) * bavg) * fade
    return co
def flips(V0, V1, F):
    n = lambda V: np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); return np.flatnonzero((n(V0) * n(V1)).sum(1) < 0)
