"""Minimal orthographic flat-shaded renderer for ARM inspection sheets (numpy z-buffer; triangles or point splats)."""
import numpy as np
from PIL import Image, ImageDraw
def _shade(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    return n
def view(V, F, axes, W=420, H=900, bounds=None, light=(0.3, -0.6, 0.75), grid=10.0):
    """axes: (horizontal axis index, sign, depth axis index, depth sign); vertical = z (index 2)."""
    a, sa, d, sd = axes
    X = V[:, a] * sa; Y = V[:, 2]; Z = V[:, d] * sd
    if bounds is None: bounds = (X.min(), X.max(), Y.min(), Y.max())
    x0, x1, y0, y1 = bounds; s = min((W - 20) / (x1 - x0), (H - 20) / (y1 - y0))
    px = (X - x0) * s + 10; py = H - 10 - (Y - y0) * s
    n = _shade(V, F); l = np.array(light); l = l / np.linalg.norm(l)
    # light in view space
    nv = np.stack([n[:, a] * sa, n[:, d] * sd, n[:, 2]], 1)
    c = np.clip(np.abs(nv @ np.array([0.25, -0.55, 0.8]) / np.linalg.norm([0.25, -0.55, 0.8])), 0, 1) * 0.75 + 0.2
    img = np.full((H, W), 255.0); zb = np.full((H, W), -1e18)
    T = F
    P = np.stack([px[T], py[T], Z[T]], 2)  # (n,3 verts,3)
    xmin = np.floor(P[:, :, 0].min(1)).astype(int); xmax = np.ceil(P[:, :, 0].max(1)).astype(int)
    ymin = np.floor(P[:, :, 1].min(1)).astype(int); ymax = np.ceil(P[:, :, 1].max(1)).astype(int)
    small = (xmax - xmin <= 2) & (ymax - ymin <= 2)
    # point-splat small triangles (dense meshes)
    idx = np.where(small)[0]
    if len(idx):
        cx = np.clip(np.round(P[idx, :, 0].mean(1)).astype(int), 0, W - 1); cy = np.clip(np.round(P[idx, :, 1].mean(1)).astype(int), 0, H - 1)
        cz = P[idx, :, 2].mean(1); o = np.argsort(cz)
        for dx in (0, 1):
            for dy in (0, 1):
                xx = np.clip(cx[o] + dx, 0, W - 1); yy = np.clip(cy[o] + dy, 0, H - 1)
                zb_old = zb[yy, xx]; ok = cz[o] > zb_old
                img[yy[ok], xx[ok]] = 255 * c[idx][o][ok]; zb[yy[ok], xx[ok]] = cz[o][ok]
    for t in np.where(~small)[0]:
        (ax_, ay_, az_), (bx, by, bz), (cx_, cy_, cz_) = P[t]
        xs = np.arange(max(xmin[t], 0), min(xmax[t] + 1, W)); ys = np.arange(max(ymin[t], 0), min(ymax[t] + 1, H))
        if len(xs) == 0 or len(ys) == 0: continue
        gx, gy = np.meshgrid(xs + 0.5, ys + 0.5)
        den = (by - cy_) * (ax_ - cx_) + (cx_ - bx) * (ay_ - cy_)
        if abs(den) < 1e-12: continue
        w1 = ((by - cy_) * (gx - cx_) + (cx_ - bx) * (gy - cy_)) / den; w2 = ((cy_ - ay_) * (gx - cx_) + (ax_ - cx_) * (gy - cy_)) / den; w3 = 1 - w1 - w2
        m = (w1 >= -1e-6) & (w2 >= -1e-6) & (w3 >= -1e-6)
        if not m.any(): continue
        z = w1 * az_ + w2 * bz + w3 * cz_
        yy, xx = np.nonzero(m); zz = z[m]; Y_ = ys[yy]; X_ = xs[xx]
        ok = zz > zb[Y_, X_]; zb[Y_[ok], X_[ok]] = zz[ok]; img[Y_[ok], X_[ok]] = 255 * c[t]
    im = Image.fromarray(img.astype(np.uint8)).convert('RGB'); dr = ImageDraw.Draw(im)
    for g in np.arange(np.ceil(y0 / grid) * grid, y1 + 1e-6, grid):
        yy = H - 10 - (g - y0) * s; dr.line([(0, yy), (6, yy)], fill=(200, 60, 60))
    return im
def sheet(ims, labels, out, title=''):
    W = sum(i.width for i in ims); H = max(i.height for i in ims) + 50
    S = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(S); x = 0
    d.text((8, 4), title, fill=(0, 0, 0))
    for i, l in zip(ims, labels): S.paste(i, (x, 40)); d.text((x + 8, 24), l, fill=(0, 0, 0)); x += i.width
    S.save(out, quality=90)
