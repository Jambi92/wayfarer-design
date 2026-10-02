# Saurin post-Rodin Phase A: axial blockout.
# One continuous axial sweep: cervical -> thoracic shell -> lower axial trunk -> pelvis/sacral platform -> caudal base ->
# proximal tail. The section frame rotates with the axis, so the ventral body wall becomes the tail's ventral surface and the
# dorsum becomes the tail's dorsum by construction (no attachment seam). Head = accepted TS6.1 cranium (reused). Simplified
# femora only. No arms, hands, feet, muscles, scales, claws or ridges (Phase B/C).
# Frame: centimetres. X lateral, F forward, U up, ground U = 0.
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.spatial import cKDTree
import wf_saurin_body8 as B8
from wf_saurin_body8 import smin, smax, tent, sstep, band, ellipsoid, round_cone, BIG

AT = np.array([0.0, 3.0, 179.3]); B8.AT = AT

# --- axis control points: (F, U) of the section centre, and section (lateral half-width ventral side, lateral half-width
#     dorsal side, ventral extent, dorsal extent, ventrolateral chamfer, dorsolateral chamfer)
AXIS = [
    # F      U      wV     wD     dV     dD    cv    cb
    (2.4, 183.0,  4.4,   4.4,   4.6,   4.0, 1.30, 1.30),   # inside the skull base
    (2.6, 175.0,  5.6,   6.0,   4.8,   6.0, 1.20, 1.22),   # cervical: dorsal mass larger than the throat
    (2.0, 167.0,  7.0,   7.8,   5.4,   7.8, 1.18, 1.20),
    (2.0, 160.0,  9.6,  10.4,   7.2,  10.0, 1.16, 1.18),   # cervicothoracic expansion
    (3.2, 152.0, 12.8,  13.6,  11.4,  13.2, 1.15, 1.17),   # thoracic inlet
    (4.4, 143.0, 14.2,  15.0,  17.6,  16.0, 1.13, 1.17),   # deep thoracic shell (keeled ventral wall)
    (4.4, 134.0, 14.8,  15.2,  18.0,  16.0, 1.13, 1.17),
    (3.6, 125.0, 14.6,  14.8,  15.6,  15.2, 1.15, 1.18),   # costal region
    (2.0, 116.0, 13.6,  13.8,  12.0,  13.6, 1.20, 1.20),   # lower axial trunk: depth redistributes dorsally
    (0.0, 107.0, 13.6,  14.2,  10.6,  13.8, 1.22, 1.20),
    (-4.0, 100.0, 15.6, 15.4,  10.0,  14.4, 1.24, 1.20),   # pelvic platform: wide (femoral sockets) + deep dorsally
    (-12.5, 96.8, 15.2, 15.0,   9.0,  13.0, 1.24, 1.21),   # sacral bend (wide radius: no dorsal crease)
    (-24.0, 96.6, 14.0, 13.6,   8.8,  11.4, 1.24, 1.21),   # caudal base: nearly pelvis-wide, flanks continue the pelvis;
    (-36.0, 95.4, 11.6, 11.2,   7.6,   9.6, 1.26, 1.24),   #   ventral surface kept above the crotch line (front silhouette)
    (-48.0, 93.6,  9.2,  8.8,   6.2,   7.6, 1.28, 1.26),
    (-60.0, 91.4,  7.4,  7.0,   5.2,   5.8, 1.30, 1.28),   # end of the proximal tail (Phase A stops here)
]
TAIL_TOTAL_TARGET = 0.68 * 188.0          # full tail planned for Phase B (centreline, caudal base -> tip)

def _build_path(n=900):
    pts = np.array([[0.0, a[0], a[1]] for a in AXIS])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); s = np.concatenate([[0], np.cumsum(seg)])
    cs = CubicSpline(s, pts, bc_type="natural")
    ss = np.linspace(0, s[-1], n); P = cs(ss); D = cs(ss, 1); D /= np.linalg.norm(D, axis=1, keepdims=True)
    # re-arc-length
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    par = np.array([a[2:] for a in AXIS])
    sec = np.stack([PchipInterpolator(s, par[:, j])(ss) for j in range(par.shape[1])], 1)
    X = np.array([1.0, 0, 0]); N = np.cross(D, X); N /= np.linalg.norm(N, axis=1, keepdims=True)   # dorsal direction
    return P, D, N, sec, L, s
PATH, TANG, DORS, SEC, ARC, CTRL_S = _build_path()
_TREE = cKDTree(PATH)

def plane_q2(x, f, wV, wD, dV, dD, cv, cb, k=11.0):
    """Planar section with separate ventral/dorsal half-widths and extents (f > 0 = ventral)."""
    tb = np.clip(0.5 + f / (0.9 * (dV + dD)), 0, 1); tb = tb * tb * (3 - 2 * tb); w = wD + (wV - wD) * tb; ax = np.abs(x) / w
    fv = f / dV; fd = -f / dD
    t = np.stack([ax, fv, fd, (ax + fv) / cv, (ax + fd) / cb]); m = t.max(0)
    return m + np.log(np.exp(k * (t - m)).sum(0)) / k - np.log(1.6) / k

def axial(P):
    X, F, U = P; Q = np.stack([X, F, U], -1)
    dist, idx = _TREE.query(Q, distance_upper_bound=26.0)
    ok = np.isfinite(dist); out = np.full(X.shape, BIG)
    if not ok.any(): return out
    i = idx[ok]; r = Q[ok] - PATH[i]
    along = (r * TANG[i]).sum(1); x = r[:, 0]; f = -(r * DORS[i]).sum(1)          # f > 0 ventral
    wV, wD, dV, dD, cv, cb = SEC[i].T
    q = plane_q2(x, f, wV, wD, dV, dD, cv, cb)
    sz = np.minimum(np.minimum(wV, wD), np.minimum(dV, dD))
    last = i == len(PATH) - 1; first = i == 0
    e = np.where(last & (along > 0), along / (0.9 * sz), np.where(first & (along < 0), -along / (0.9 * sz), 0.0))
    out[ok] = np.where(q > 0, np.sqrt(q * q + e * e) - 1, q - 1 + e) * sz
    return out

HIP = np.array([9.6, -0.6, 90.0])
KNEE = np.array([10.0, 2.6, 48.0])
def femora(P):
    X, F, U = P; Pa = (np.abs(X), F, U)
    d = round_cone(Pa, HIP + np.array([0.6, 0, 3.0]), KNEE, 7.8, 4.8)                  # simplified femoral segment
    d = smin(d, ellipsoid(Pa, HIP + np.array([2.2, -1.0, 2.0]), (5.6, 8.0, 8.0)), 3.0)  # acetabular / trochanteric root
    d = smin(d, round_cone(Pa, KNEE, np.array([10.0, 0.0, 30.0]), 4.6, 3.6), 1.0)      # stub of the crus (orientation only)
    return d

def head(P):
    return B8.head(P)

PARTS = [
    ("axial", axial, (-30, 30, -90, 30, 70, 190), None, False),
    ("femora", femora, (0, 20, -12, 12, 26, 104), 6.0, True),
    ("head", head, (-9, 9, -12, 22, 165, 190), 2.8, False),
]
PAD = 2.5

def sdf(X, F, U):
    d = np.full(X.shape, BIG, dtype=np.float64)
    for name, fn, bb, k, sym in PARTS:
        xs = np.abs(X) if sym else X
        m = (xs > bb[0] - PAD) & (xs < bb[1] + PAD) & (F > bb[2] - PAD) & (F < bb[3] + PAD) & (U > bb[4] - PAD) & (U < bb[5] + PAD)
        if not m.any(): continue
        v = fn((X[m], F[m], U[m]))
        d[m] = v if k is None else smin(d[m], v, k)
    return d
B8.sdf = sdf
B8.BOX = (-28.0, 28.0, -72.0, 26.0, 24.0, 191.0)

if __name__ == "__main__":
    import sys, time
    t = time.time(); step = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/rb/out/saurin_phaseA.npz"
    v, f = B8.mesh(step, log=lambda *a: print(*a, round(time.time() - t, 1), flush=True))
    np.savez_compressed(out, v=v, f=f)
    print("DONE", len(v), len(f), round(time.time() - t, 1))
