# RAC RM-OT-05L: digital-clay toolkit for the blank-slate Gorrund reference sculpt (GO-RS*).
# This file holds NO anatomy. It provides sculpting primitives (signed-distance clay forms and smooth blending, like the
# primitive / ZSphere blockout of a sculpting package), a voxel "remesh" (marching cubes on the clay field) and a mesh writer.
# Every anatomical form is placed by hand in the per-revision sculpt record (l_rs1.py, ...), one stroke per line; there are no
# parameters, no sweeps and no donor body. Units cm, Z up, +Y anterior, +X = body left, ground z = 0.
import numpy as np

def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1); return b * (1 - h) + a * h - k * h * (1 - h)
def smax(a, b, k):
    return -smin(-a, -b, k)

def ellipsoid(P, c, r):
    q = (P - np.asarray(c, float)) / np.asarray(r, float); k0 = np.linalg.norm(q, axis=-1)
    k1 = np.linalg.norm(q / np.asarray(r, float), axis=-1); return k0 * (k0 - 1) / np.maximum(k1, 1e-9)
def cone(P, a, b, ra, rb, scale=(1, 1, 1)):
    """round cone (tapered capsule) from a (radius ra) to b (radius rb); scale = section squash (e.g. (0.8,1,1) flattens in x)"""
    s = np.asarray(scale, float); a = np.asarray(a, float); b = np.asarray(b, float)
    ab = b - a; L2 = ab @ ab; t = np.clip(((P - a) @ ab) / L2, 0, 1); q = (P - (a + t[..., None] * ab)) / s
    return np.linalg.norm(q, axis=-1) * s.min() - (ra + (rb - ra) * t)
def plane_below(P, z0):
    return z0 - P[..., 2]          # >0 below z0: used with smax to cut a flat sole

class Clay:
    """an ordered list of strokes: ('add'|'carve', primitive-callable, blend k). Evaluated in order on any point set."""
    def __init__(self): self.strokes = []
    def add(self, f, k=0.0, label=''): self.strokes.append(('add', f, k, label)); return self
    def carve(self, f, k=0.0, label=''): self.strokes.append(('carve', f, k, label)); return self
    def cut(self, f, k=0.0, label=''): self.strokes.append(('cut', f, k, label)); return self    # intersect (keep inside f)
    def sdf(self, P):
        d = np.full(P.shape[:-1], 1e9)
        for op, f, k, _ in self.strokes:
            v = f(P)
            d = smin(d, v, k) if op == 'add' else (smax(d, -v, k) if op == 'carve' else smax(d, v, k))
        return d

def remesh(clay, lo, hi, h=0.5, mirror_x=True):
    """voxel remesh of the clay field: marching cubes at voxel size h (cm). With mirror_x the left half is sculpted and mirrored."""
    from skimage import measure
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    xs = np.arange(lo[0], hi[0] + h, h); ys = np.arange(lo[1], hi[1] + h, h); zs = np.arange(lo[2], hi[2] + h, h)
    G = np.empty((len(xs), len(ys), len(zs)), np.float32)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    for k, z in enumerate(zs):
        P = np.stack([np.abs(X) if mirror_x else X, Y, np.full_like(X, z)], -1); G[:, :, k] = clay.sdf(P)
    v, f, n, _ = measure.marching_cubes(G, 0.0, spacing=(h, h, h))
    v += lo; return v, f.copy()                 # outward winding (marching_cubes on an SDF negative inside)

def write_obj(fn, V, F, header=''):
    with open(fn, 'w') as o:
        for line in header.splitlines(): o.write('# ' + line + '\n')
        for v in V: o.write('v %.4f %.4f %.4f\n' % tuple(v))
        for t in F: o.write('f %d %d %d\n' % tuple(np.asarray(t) + 1))

def section_sweep(P, rows, n=2.3):
    """sculptor's section templates: a vertical sweep through hand-drawn horizontal sections.
    rows = [(z, cy, half_breadth, front_depth, back_depth, exponent)], z ascending. Each section is a radiused superellipse
    (exponent 2 = ellipse; >2 = more planar sides) with separate anterior / posterior depth. Between rows the section is
    interpolated; above the top / below the bottom row the form is closed by rounding."""
    R = np.asarray(rows, float); z = P[..., 2]; zc = np.clip(z, R[0, 0], R[-1, 0])
    from scipy.interpolate import PchipInterpolator
    g = lambda j: PchipInterpolator(R[:, 0], R[:, j])(zc)     # smooth (C1) between the drawn sections
    cy, a, bf, bb, ex = g(1), g(2), g(3), g(4), g(5)
    x = np.abs(P[..., 0]); y = P[..., 1] - cy; b = np.where(y > 0, bf, bb)
    u = (x / a) ** ex + (np.abs(y) / b) ** ex; rho = u ** (1.0 / ex)
    d2 = (rho - 1.0) * np.minimum(a, b)                   # approximate in-plane distance
    dz = np.maximum(R[0, 0] - z, z - R[-1, 0])            # outside the swept height range
    return np.where(dz > 0, np.sqrt(np.maximum(d2, 0) ** 2 + dz ** 2) * (d2 > 0) + np.where(d2 <= 0, np.maximum(d2, dz), 0), d2)
