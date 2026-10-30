# uv_check.py : UV continuity audit -- every interior edge whose two faces disagree on a shared vertex UV is a seam edge; compare v005 vs branch
import numpy as np
def seam_edges(Q, UV):
    E = {}
    for f, q in enumerate(Q):
        for k in range(4):
            a, b = int(q[k]), int(q[(k + 1) % 4]); E.setdefault((min(a, b), max(a, b)), []).append((f, k))
    out = set()
    for e, L in E.items():
        if len(L) != 2: continue
        (f, k), (g, j) = L; ua = {int(Q[f][k]): UV[f][k], int(Q[f][(k + 1) % 4]): UV[f][(k + 1) % 4]}; ub = {int(Q[g][j]): UV[g][j], int(Q[g][(j + 1) % 4]): UV[g][(j + 1) % 4]}
        if any(np.abs(ua[v] - ub[v]).max() > 1e-5 for v in ua): out.add(e)
    return out
def uv_flips(Q, UV, faces):
    """faces whose UV polygon winding disagrees with the majority (folded UV)"""
    A = []
    for f in faces:
        u = UV[f]; A.append(0.5 * sum(u[k][0] * u[(k + 1) % 4][1] - u[(k + 1) % 4][0] * u[k][1] for k in range(4)))
    A = np.array(A); sgn = np.sign(np.median(A)); return int((np.sign(A) != sgn).sum()), float(np.abs(A).min())
