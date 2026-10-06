"""Orthographic evidence sheet for an ARM candidate (order §8): front, side, 3/4, head front, head side.
Common scale for every candidate: body views 3.4 px/cm on a 240 cm frame with 10 cm ticks; head views 14 px/cm with 1 cm ticks.
Usage: python3 evidence.py cand_r6.npz out.jpg "title" """
import sys, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))

def sphere(c, r, n=16):
    th = np.linspace(0, np.pi, n); ph = np.linspace(0, 2 * np.pi, 2 * n, endpoint=False)
    V = [c + r * np.array([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)]) for t in th for p in ph]
    F = []
    m = 2 * n
    for i in range(n - 1):
        for j in range(m):
            a = i * m + j; b = i * m + (j + 1) % m; c_ = (i + 1) * m + j; d = (i + 1) * m + (j + 1) % m
            F += [(a, c_, b), (b, c_, d)]
    return np.array(V), np.array(F)

def render(V, F, hx, hy, depth, ppcm, origin, size, tick, shade_col=(205, 205, 200), light=(-0.35, -0.45, 0.82), amb=0.25, fcol=None):
    """Orthographic z-buffer. fcol: optional (nF,3) per-face colour (default shade_col). hx, hy, depth: (N,) view coords in cm. origin=(x0,y0) cm at image bottom-left."""
    W, H = size; px = (hx - origin[0]) * ppcm; py = H - (hy - origin[1]) * ppcm
    T = F; P = np.stack([px[T], py[T], depth[T]], 2)
    e1 = np.stack([px[T[:, 1]] - px[T[:, 0]], py[T[:, 1]] - py[T[:, 0]], depth[T[:, 1]] - depth[T[:, 0]]], 1)
    e2 = np.stack([px[T[:, 2]] - px[T[:, 0]], py[T[:, 2]] - py[T[:, 0]], depth[T[:, 2]] - depth[T[:, 0]]], 1)
    n = np.cross(e1 / ppcm, e2 / ppcm); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    L = np.array(light, float); L /= np.linalg.norm(L)
    c = amb + (1 - amb) * np.clip(np.abs(n @ L), 0, 1) ** 1.5
    img = np.full((H, W, 3), 250.0); zb = np.full((H, W), -1e18)
    xmin = np.floor(P[:, :, 0].min(1)).astype(int); xmax = np.ceil(P[:, :, 0].max(1)).astype(int)
    ymin = np.floor(P[:, :, 1].min(1)).astype(int); ymax = np.ceil(P[:, :, 1].max(1)).astype(int)
    col = np.array(shade_col, float)
    for t in range(len(T)):
        x0, x1, y0, y1 = max(xmin[t], 0), min(xmax[t] + 1, W), max(ymin[t], 0), min(ymax[t] + 1, H)
        if x0 >= x1 or y0 >= y1: continue
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = P[t]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        w1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / den; w2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / den; w3 = 1 - w1 - w2
        m = (w1 >= -1e-3) & (w2 >= -1e-3) & (w3 >= -1e-3)
        if not m.any(): continue
        z = w1 * az + w2 * bz + w3 * cz
        yy, xx = np.nonzero(m); zz = z[m]; Y = yy + y0; X = xx + x0
        ok = zz > zb[Y, X]; zb[Y[ok], X[ok]] = zz[ok]; img[Y[ok], X[ok]] = (col if fcol is None else fcol[t]) * c[t]
    im = Image.fromarray(img.astype(np.uint8)); d = ImageDraw.Draw(im)
    # ground line and ticks
    gy = H - (0 - origin[1]) * ppcm
    if 0 <= gy < H: d.line([(0, gy), (W, gy)], fill=(120, 120, 120))
    k0 = int(np.ceil(origin[1] / tick)); k1 = int((origin[1] + H / ppcm) / tick)
    for k in range(k0, k1 + 1):
        y = H - (k * tick - origin[1]) * ppcm; big = (k % 5 == 0)
        d.line([(0, y), (10 if big else 5, y)], fill=(200, 40, 40));
        if big: d.text((12, y - 6), "%g" % (k * tick), fill=(200, 40, 40))
    return im

def make(npz, out, title):
    D = np.load(npz, allow_pickle=True); V = D["V"].astype(float); F = D["F"]
    keep = D["keep"]
    Vs, Fs = [V], [F]; off = len(V)
    for s in ("eye_l", "eye_r"):
        sv, sf = sphere(D[s], float(D["eye_diam"]) / 2); Vs.append(sv); Fs.append(sf + off); off += len(sv)
    V2 = np.vstack(Vs); F2 = np.vstack(Fs)
    used = np.unique(F2)
    x, f, u = V2[:, 0], V2[:, 1], V2[:, 2]
    BH = 240.0; ppcm = 3.4; Hpx = int(BH * ppcm) + 10
    views = []
    views.append(("front", render(x, F2, x, u, f, ppcm, (-60, -2), (int(120 * ppcm), Hpx), 10)))
    views.append(("left side", render(f, F2, -f * 0 + f, u, x, ppcm, (-45, -2), (int(90 * ppcm), Hpx), 10)))
    a = np.radians(45); hx = x * np.cos(a) + f * np.sin(a); dp = f * np.cos(a) - x * np.sin(a)
    views.append(("3/4 front-left", render(hx, F2, hx, u, dp, ppcm, (-60, -2), (int(120 * ppcm), Hpx), 10)))
    # head views
    hw = D["w_head"]; hv = np.where(keep & (hw > 0.5))[0]
    top = V[keep, 2].max(); hspan = top - V[keep & (hw > 0.5), 2].min()
    win = max(16.0, min(34.0, 1.25 * hspan)); hz0 = top - win + 2
    hpp = 476.0 / win; HH = 476
    hwid = max(win * 0.38, float(np.abs(V[keep & (hw > 0.5) & (V[:, 2] > hz0), 0]).max()) + 1.5)
    views.append(("head front", render(x, F2, x, u, f, hpp, (-hwid, hz0), (int(2 * hwid * hpp), HH), 1)))
    ef = float(D["eye_l"][1])
    views.append(("head side", render(f, F2, f, u, x, hpp, (ef - 0.65 * win, hz0), (int(0.88 * win * hpp), HH), 1)))
    Wt = sum(v[1].width for v in views) + 10 * len(views); Ht = max(v[1].height for v in views) + 60
    S = Image.new("RGB", (Wt, Ht), "white"); d = ImageDraw.Draw(S); xo = 0
    d.text((8, 6), title, fill=(0, 0, 0))
    for lab, im in views:
        S.paste(im, (xo, 50)); d.text((xo + 6, 34), lab + ("  (10 cm ticks)" if "head" not in lab else "  (1 cm ticks)"), fill=(0, 0, 0)); xo += im.width + 10
    S.save(out, quality=88)

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
