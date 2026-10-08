"""Femoral S7 station (subtrochanteric section, 20 % down the hip->knee axis), shared by arm_measure.measure and bony_envelope.fast_stations.
Author ruling 2026-10-07 (reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md): S7 is read on an EXACT PLANE SECTION of
the thigh faces (all three vertices thigh weight > 0.5), the W1h trunk-station rule extended to S7, because a +/-0.8 cm vertex slab misses
whole vertex rings where the mesh is stretched. METHOD = "vertex_slab" reproduces the pre-normalization reading (records before 2026-10-07)."""
import numpy as np
METHOD = "section"

def s7(V, keep, F, joints_head, w_thigh, method=None):
    """V: vertices; keep: body mask; F: faces; joints_head(name) -> joint head xyz; w_thigh(side) -> per-vertex thigh weight.
    Returns (breadth, depth) averaged over both thighs, in the perpendicular frame used since W1d (components 0 and 1)."""
    method = method or METHOD; th = []
    for sd in ("l", "r"):
        hp, kn = np.asarray(joints_head("thigh_" + sd), float), np.asarray(joints_head("calf_" + sd), float)
        L = np.linalg.norm(kn - hp); ax = (kn - hp) / L; on = keep & (w_thigh(sd) > 0.5)
        if method == "section":
            TF = F[on[F].all(1)]; t = (V - hp) @ ax - 0.2 * L; pts = []
            for i, j in ((0, 1), (1, 2), (2, 0)):
                a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]])
                pts.append(V[a[m]] + (V[b[m]] - V[a[m]]) * u[:, None])
            P = np.vstack(pts) - hp
        else:
            tv = np.where(on)[0]; P = V[tv] - hp; tt = P @ ax; P = P[np.abs(tt - 0.2 * L) < 0.8]
        Q = P - np.outer(P @ ax, ax)
        th.append((float(Q[:, 0].max() - Q[:, 0].min()), float(Q[:, 1].max() - Q[:, 1].min())))
    return tuple(np.mean(th, axis=0))
