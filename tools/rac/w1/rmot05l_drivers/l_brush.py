# RAC RM-OT-05L: sculpt-brush engine for the concept mesh (the digital equivalent of Blender's Draw / Flatten / Crease / Smooth
# brushes). A stroke is a polyline of points ON the body that the sculptor draws by hand; the brush acts on the vertices within
# its radius (smooth falloff), along the surface normal (draw / crease) or toward the local tangent plane (flatten), or relaxes
# them (smooth). Strokes on the body's left side are mirrored to the right (bilateral symmetry). No anatomy lives in this file.
import numpy as np

class Mesh:
    def __init__(self, V, F):
        self.V = np.asarray(V, float).copy(); self.F = np.asarray(F, int)
        E = np.vstack([self.F[:, [0, 1]], self.F[:, [1, 2]], self.F[:, [2, 0]]]); self.E = np.unique(np.sort(E, 1), axis=0)
        self.deg = np.bincount(self.E.ravel(), minlength=len(self.V)).astype(float)
    def normals(self):
        V, F = self.V, self.F; fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); n = np.zeros_like(V)
        for k in range(3): np.add.at(n, F[:, k], fn)
        return n / np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
    def lap(self):
        acc = np.zeros_like(self.V); np.add.at(acc, self.E[:, 0], self.V[self.E[:, 1]]); np.add.at(acc, self.E[:, 1], self.V[self.E[:, 0]])
        return acc / np.maximum(self.deg, 1)[:, None] - self.V

def _samples(pts, r):
    pts = np.asarray(pts, float); out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / (0.35 * r))))
        out += [a + (b - a) * t for t in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)

def stroke(M, kind, pts, r, s, mirror=True, side_only=None):
    """kind: 'draw' (+s cm outward along the normal at the brush centre), 'crease' (narrow inward groove, s cm),
    'flatten' (s = 0..1 pull toward the plane fitted under the brush), 'smooth' (s = 0..1 relax, iterated)."""
    sets = [np.asarray(pts, float)]
    if mirror: sets.append(np.asarray(pts, float) * [-1, 1, 1])
    for P in sets:
        S = _samples(P, r); D = np.min(np.linalg.norm(M.V[:, None, :] - S[None, :, :], axis=2), axis=1) if len(M.V) * len(S) < 4e7 else None
        if D is None:
            D = np.full(len(M.V), np.inf)
            for c in S: D = np.minimum(D, np.linalg.norm(M.V - c, axis=1))
        w = np.clip(1 - D / r, 0, 1); w = w * w * (3 - 2 * w)
        if kind == 'crease': w = np.clip(1 - D / r, 0, 1) ** 2.5
        m = w > 0
        if not m.any(): continue
        if kind in ('draw', 'crease'):
            n = M.normals(); M.V[m] += (n[m] * (s if kind == 'draw' else -s)) * w[m, None]
        elif kind == 'flatten':
            c = (M.V[m] * w[m, None]).sum(0) / w[m].sum(); X = M.V[m] - c
            nrm = np.linalg.svd(X * np.sqrt(w[m, None]), full_matrices=False)[2][-1]
            M.V[m] -= np.outer(X @ nrm, nrm) * (s * w[m])[:, None]
        elif kind == 'smooth':
            for _ in range(3):
                L = M.lap(); M.V[m] += 0.5 * s * L[m] * w[m, None]
    return M
