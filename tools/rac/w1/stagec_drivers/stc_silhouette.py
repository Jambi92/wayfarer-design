# RAC Stage C distinctness diagnostics (REPORT ONLY, no thresholds): silhouette overlap of two bodies rendered at the SAME
# stature on the same orthographic scale (stc_render.py *_Fs / *_Ps alpha masks), horizontally centred.
#   iou       = raw silhouette IoU (front, profile)
#   centring: median column of the 40-70 % stature band (trunk), so tails / arms do not shift the body
#   iou_xfit  = IoU after the best uniform horizontal stretch of B (0.80..1.25): how much of the difference is breadth only
# Usage: python3 stc_silhouette.py OUT.json A=prefix B=prefix ...pairs as A:B
import sys, json, numpy as np
from PIL import Image
out = sys.argv[1]; P = dict(a.split('=', 1) for a in sys.argv[2:] if '=' in a and ':' not in a); pairs = [a.split(':') for a in sys.argv[2:] if ':' in a]
def mask(p, v):
    a = np.array(Image.open('%s_%s.png' % (p, v)).split()[3]) > 0
    rows = np.where(a.any(1))[0]; top, bot = rows[0], rows[-1]; h = bot - top
    band = a[int(bot - 0.70 * h):int(bot - 0.40 * h)]          # trunk band (40-70 % of stature): centre without arms / tail bias
    c = float(np.median(np.nonzero(band)[1]))
    return a, c
def shift(a, c, W=600):
    o = np.zeros((a.shape[0], W), bool); x0 = int(round(W / 2 - c)); src = a
    xs = np.arange(a.shape[1]) + x0; ok = (xs >= 0) & (xs < W); o[:, xs[ok]] = src[:, ok]; return o
def stretch(a, c, k, W=600):
    ys, xs = np.nonzero(a); o = np.zeros((a.shape[0], W), bool)
    for kk in (0.0, 0.5):
        nx = np.round((xs + kk - c) * k + W / 2).astype(int); ok = (nx >= 0) & (nx < W); o[ys[ok], nx[ok]] = True
    return o
iou = lambda a, b: float((a & b).sum() / max((a | b).sum(), 1))
R = {}
for A, B in pairs:
    r = {}
    for v in ('Fs', 'Ps'):
        a, ca = mask(P[A], v); b, cb = mask(P[B], v); sa = shift(a, ca)
        best = max((iou(sa, stretch(b, cb, k)), k) for k in np.linspace(0.8, 1.25, 46))
        r[v] = {"iou": round(iou(sa, shift(b, cb)), 4), "iou_xfit": round(best[0], 4), "xfit_k": round(float(best[1]), 3)}
    R['%s vs %s' % (A, B)] = r
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1))
