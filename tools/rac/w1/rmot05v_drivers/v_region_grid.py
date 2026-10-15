# RM-OT-05V: build a frozen sampled REGION field from a detected point set (garment / braid / jewellery vertices).
# g = signed distance to the morphologically CLOSED union of balls (radius r around every point; closing radius c fills the
# narrow gaps between neighbouring balls so the region boundary is smooth and simple), lightly blurred. Negative inside.
# Usage: python3 v_region_grid.py --points P.npy --r 3 --close 3 --blur 0.8 --h 0.4 --out REGION.npz
import argparse, numpy as np, scipy.ndimage as ndi
from scipy.spatial import cKDTree
ap = argparse.ArgumentParser(); ap.add_argument('--points'); [ap.add_argument(k, type=float) for k in ('--r', '--close', '--blur', '--h')]; ap.add_argument('--out'); a = ap.parse_args()
Q = np.load(a.points); m = a.r + a.close + 4.0; lo = Q.min(0) - m; hi = Q.max(0) + m; n = np.ceil((hi - lo) / a.h).astype(int) + 1
ax = [lo[i] + a.h * np.arange(n[i]) for i in range(3)]; X = np.stack(np.meshgrid(*ax, indexing='ij'), -1).reshape(-1, 3)
d = cKDTree(Q).query(X, workers=-1)[0].reshape(n); M = d < a.r
if a.close > 0:
    D = ndi.distance_transform_edt(~M, sampling=a.h) <= a.close          # dilate
    M = ndi.distance_transform_edt(D, sampling=a.h) > a.close            # erode -> closing
g = ndi.distance_transform_edt(~M, sampling=a.h) - ndi.distance_transform_edt(M, sampling=a.h)
if a.blur > 0: g = ndi.gaussian_filter(g, a.blur / a.h)
np.savez_compressed(a.out, A=g.astype(np.float32), lo=lo, h=a.h, points=len(Q), r=a.r, close=a.close, blur=a.blur)
print(dict(shape=n.tolist(), inside_voxels=int(M.sum())))
