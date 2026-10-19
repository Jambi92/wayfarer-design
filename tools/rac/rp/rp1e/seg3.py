"""digit segmentation of the source hand: voxel volume (eroded), geodesic distance D from the wrist, markers:
palm = D < palm_max (minus thumb chain), thumb = the component that separates first (band tb), fingers = the components at band fb;
watershed on -D (distal first) so each digit floods back toward the palm marker."""
import numpy as np, sys
from scipy import ndimage as ndi
from skimage.segmentation import watershed
s = sys.argv[1]; tb = float(sys.argv[2]); fb = float(sys.argv[3]); pmax = float(sys.argv[4])
g = np.load('/home/claude/stc/rp1e/geo_%s.npz' % s); idx = g['idx']; D = g['D']; lo = g['lo']; h = float(g['h']); shape = tuple(g['shape'])
ok = np.isfinite(D); idx = idx[ok]; D = D[ok]
Dv = np.full(shape, np.nan, np.float32); Dv[tuple(idx.T)] = D; mask = np.isfinite(Dv); Dz = np.where(mask, Dv, 0)
st = np.ones((3, 3, 3))
def comps(a, b):
    l2, k = ndi.label(mask & (Dz >= a) & (Dz < b), structure=st); sz = np.bincount(l2.ravel()); sz[0] = 0
    return l2, [c for c in np.argsort(-sz) if sz[c] > 300]
# thumb: grow the second component at band tb forward through bands while it stays a single separate component
lt, ct = comps(tb, tb + 0.3); thumb = lt == ct[1]
markers = np.zeros(shape, np.int32)
lf, cf = comps(fb, fb + 0.3)
print('finger band comps', len(cf), [int((lf == c).sum()) for c in cf])
# identify which finger-band comp is the thumb continuation: flood thumb seed within D in [tb, fb+0.3] restricted region
reg = mask & (Dz >= tb) & (Dz < fb + 0.3)
lr, _ = ndi.label(reg, structure=st)
thumb_lab = np.unique(lr[thumb]); thumb_lab = thumb_lab[thumb_lab > 0]
k = 3
for c in cf:
    m = lf == c
    if np.isin(lr[m], thumb_lab).mean() > 0.5 and len(thumb_lab) and np.isin(lr[m], thumb_lab).all():
        markers[m] = 2
    else:
        markers[m] = k; k += 1
markers[thumb] = 2
markers[mask & (Dz < pmax) & (markers == 0)] = 1
# keep thumb branch out of palm marker: voxels in the thumb's own separated region below pmax
lab = watershed(-Dz, markers, mask=mask)
print({int(q): round(float((lab == q).sum() * h ** 3), 1) for q in np.unique(lab) if q})
np.savez_compressed('/home/claude/stc/rp1e/lab_%s.npz' % s, lab=lab.astype(np.int8), lo=lo, h=h)
