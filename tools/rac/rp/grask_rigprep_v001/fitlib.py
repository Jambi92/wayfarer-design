# fitlib.py : section / axis / sphere fitting helpers for the Grask rig-prep landmark proposal (analysis frame, cm).
# Everything here is read-only geometry measurement on a trimesh; nothing writes or edits a mesh.
import numpy as np, trimesh

T_PROD = np.array([-0.11179767867288516, 5.722717396009755, 0.0])   # production = source + T_PROD (analysis cm)

def load(npz):
    M = np.load(npz); return trimesh.Trimesh(M['V'].astype(float), np.asarray(M['Q'], np.int64), process=False)

def basis(n):
    n = n / np.linalg.norm(n)
    a = np.cross(n, [0, 1.0, 0]) if abs(n[1]) < 0.9 else np.cross(n, [1.0, 0, 0])
    a /= np.linalg.norm(a); b = np.cross(n, a); return n, a, b

def poly_props(e, o, a, b):
    q = e - o; x = q @ a; y = q @ b
    cr = x[:-1] * y[1:] - x[1:] * y[:-1]; A = 0.5 * cr.sum()
    if abs(A) < 1e-9: return None
    cx = ((x[:-1] + x[1:]) * cr).sum() / (6 * A); cy = ((y[:-1] + y[1:]) * cr).sum() / (6 * A)
    return abs(A), o + cx * a + cy * b

def section(m, o, n, pick, rmax=25.0, keep=None):
    """closed section loop of mesh m on plane (o, n) whose area centroid is nearest `pick` (within rmax).
    keep(points)->bool can reject loops (e.g. wrong side). returns dict(area, c, pts) or None"""
    n, a, b = basis(np.asarray(n, float))
    s = m.section(plane_origin=o, plane_normal=n)
    if s is None: return None
    best = None
    for e in s.discrete:
        if len(e) < 6: continue
        if np.linalg.norm(e[0] - e[-1]) > 1e-6: continue          # closed loops only
        pr = poly_props(e, np.asarray(o, float), a, b)
        if pr is None: continue
        A, c = pr; d = np.linalg.norm(c - pick)
        if d > rmax or (keep is not None and not keep(e)): continue
        if best is None or d < best[0]: best = (d, dict(area=A, c=c, pts=e))
    return None if best is None else best[1]

def line_fit(P):
    c = P.mean(0); u, s, vt = np.linalg.svd(P - c); d = vt[0]
    r = np.linalg.norm((P - c) - np.outer((P - c) @ d, d), axis=1)
    return c, d / np.linalg.norm(d), float(np.sqrt((r ** 2).mean()))

def axis_from_sections(m, A, B, ts, rmax=12.0, iters=2):
    """limb axis: centroids of sections perpendicular to A->B at A+t(B-A); refit perpendicular to the fitted line"""
    d = (B - A) / np.linalg.norm(B - A); L = np.linalg.norm(B - A); c0 = A
    for _ in range(iters):
        C = []
        for t in ts:
            o = c0 + d * (t * L) if _ else A + (B - A) * t
            s = section(m, o, d, o, rmax)
            if s is not None: C.append(s['c'])
        C = np.array(C); c, dd, rms = line_fit(C)
        if dd @ d < 0: dd = -dd
        # re-anchor: c0 = projection of A on the fitted line
        c0 = c + ((A - c) @ dd) * dd; d = dd
    return c0, d, C, rms

def sphere_fit(P):
    A = np.c_[2 * P, np.ones(len(P))]; bb = (P ** 2).sum(1)
    x, *_ = np.linalg.lstsq(A, bb, rcond=None); c = x[:3]; r = np.sqrt(x[3] + c @ c)
    res = np.linalg.norm(P - c, axis=1) - r; return c, float(r), float(np.sqrt((res ** 2).mean()))

def closest_between_lines(p1, d1, p2, d2):
    w = p1 - p2; a = d1 @ d1; b = d1 @ d2; c = d2 @ d2; d = d1 @ w; e = d2 @ w; den = a * c - b * b
    if den < 1e-9: return None, None, 0.0
    s = (b * e - c * d) / den; t = (a * e - b * d) / den; q1 = p1 + s * d1; q2 = p2 + t * d2
    ang = np.degrees(np.arccos(np.clip(abs(b) / np.sqrt(a * c), -1, 1)))
    return 0.5 * (q1 + q2), float(np.linalg.norm(q1 - q2)), float(ang)

def to_prod(p): return np.asarray(p, float) + T_PROD
def to_blender_pt(p_prod): p = np.asarray(p_prod, float); return np.array([p[0], -p[1], p[2]]) / 100.0
def to_blender_vec(v): v = np.asarray(v, float); return np.array([v[0], -v[1], v[2]])

def frame_rh_blender(long_an, flex_an):
    """orthonormal right-handed frame in the BLENDER frame from analysis-frame directions.
    Y = longitudinal (parent->child), X = flexion axis (orthogonalised), Z = X x Y. returns 3x3 (columns X,Y,Z) blender"""
    y = to_blender_vec(long_an); y /= np.linalg.norm(y)
    x = to_blender_vec(flex_an); x = x - (x @ y) * y; x /= np.linalg.norm(x)
    z = np.cross(x, y); return np.stack([x, y, z], 1)

def rot(axis, ang):
    axis = axis / np.linalg.norm(axis); K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
