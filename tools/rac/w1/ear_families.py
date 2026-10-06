"""RAC W1d: purpose-built ear-family REFERENCE geometry (procedural, numpy). Not a pointiness continuum: each family is its own
architecture (outline function, taper law, rim/fold/bowl system), never an interpolation of the human ear.

Ear-local frame before attachment: the auricle lies in the y-z plane (y = backward, z = up), lateral = +x (away from the skull);
the attachment (root) runs along the anterior edge. After construction the ear is rotated by its projection angle (about the
root line) and its orientation (tilt backward about x, sweep), then the four RA §11 ear landmarks are read.

EVERY numeric parameter here is BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED. Canon gives the architectures and directions only
(see reviews/claude-rac-w1d-ear-family-packet.md for the canon-to-parameter map).
Usage: python3 ear_families.py outdir"""
import sys, os, json, numpy as np

def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

# ---- family parameter sets (cm / degrees) ------------------------------------------------------------------------------
# L: length root-bottom (lobe) to top/tip; wb: max half-width; taper: (law, start, exponent); top: rounded top for non-taper
# families; lobe: lower lobe fraction; bowl: concha/bowl depth; rim: (height, width); ah: antihelix ridge height; folds: (count,
# amplitude) of the folded-cartilage system; proj: projection angle of the posterior edge from the skull (deg); tilt: backward
# tilt of the long axis from vertical (deg); sweep: rearward curvature of the long axis (cm at the top); thick: cartilage+skin
FAM = {
 "MF-human": dict(L=6.4, wb=1.75, taper=None, top=0.55, lobe=0.18, bowl=0.75, rim=(0.28, 0.32), ah=0.22, folds=(0, 0.0), proj=22, tilt=12, sweep=0.4, thick=0.32, tragus=True),
 "FN-elven": dict(L=8.6, wb=1.80, taper=("continuous", 0.30, 1.05), top=None, lobe=0.15, bowl=0.65, rim=(0.24, 0.26), ah=0.18, folds=(0, 0.0), proj=42, tilt=32, sweep=1.6, thick=0.28, tragus=True),
 "AE-elven": dict(L=9.4, wb=1.70, taper=("continuous", 0.25, 0.95), top=None, lobe=0.14, bowl=0.62, rim=(0.23, 0.25), ah=0.17, folds=(0, 0.0), proj=24, tilt=30, sweep=1.7, thick=0.27, tragus=True),
 "VA-elven": dict(L=8.4, wb=2.05, taper=("continuous", 0.40, 1.25), top=None, lobe=0.16, bowl=0.68, rim=(0.26, 0.28), ah=0.19, folds=(0, 0.0), proj=26, tilt=40, sweep=1.7, thick=0.30, tragus=True),
 "HV-mixed":  dict(L=7.6, wb=1.80, taper=("continuous", 0.48, 1.30), top=None, lobe=0.18, bowl=0.72, rim=(0.27, 0.30), ah=0.21, folds=(0, 0.0), proj=26, tilt=20, sweep=0.9, thick=0.30, tragus=True),
 "GR-folded": dict(L=10.5, wb=2.10, taper=("late", 0.72, 1.6), top=None, lobe=0.17, bowl=0.75, rim=(0.32, 0.34), ah=0.24, folds=(3, 0.16), proj=26, tilt=28, sweep=1.3, thick=0.36, tragus=True),
 "GO-bowl":   dict(L=7.4, wb=2.55, taper=None, top=0.50, lobe=0.16, bowl=1.35, rim=(0.40, 0.62), ah=0.34, folds=(1, 0.10), proj=0, tilt=10, sweep=0.3, thick=0.34, tragus=True),
}

def width(s, p):
    """Half-width profile along the long axis (s = 0 lobe bottom ... 1 top/tip)."""
    lobe = np.sqrt(np.clip(s / p["lobe"], 0, 1)) * 0.82 + 0.18 * smooth(s / p["lobe"])
    w = p["wb"] * np.minimum(1.0, lobe)
    if p["taper"] is None:                      # rounded termination (human, Gorrund)
        a = p["top"]; t = np.clip((s - a) / (1 - a), 0, 1); w = w * np.sqrt(np.clip(1 - t ** 2, 0, 1))
    else:
        law, st, ex = p["taper"]
        t = np.clip((s - st) / (1 - st), 0, 1)
        if law == "continuous":                 # taper distributed smoothly from the base region to the tip (C1 at its start)
            f = np.where(s < st, 1.0, np.cos(t * np.pi / 2) ** ex)
        else:                                   # late terminal taper after a sustained upper-ear body
            f = np.where(s < st, 1.0, np.cos(t * np.pi / 2) ** ex)
        w = w * f + 0.02
    return w

def build(p, ns=90, nt=41):
    s = np.linspace(0, 1, ns); t = np.linspace(-1, 1, nt)
    S, T = np.meshgrid(s, t, indexing="ij")
    L = p["L"]; w = width(S, p)
    # long axis in the ear plane: up with rearward sweep
    ay = p["sweep"] * S ** 2; az = L * S
    # across-width: anterior edge (t=-1, root side, toward the face) .. posterior/helix edge (t=+1)
    wf = 0.38 * w                                  # anterior (root-side) half-width: the root edge stays close to the axis
    y = ay + np.where(T < 0, T * wf, T * w); z = az
    # out-of-plane relief (x, lateral): bowl, helix rim, antihelix, tragus, folds
    r = np.abs(T)
    bowl_c = (S > p["lobe"] * 0.9) & (S < 0.85)
    bowl = -p["bowl"] * np.exp(-((T + 0.15) / 0.42) ** 2) * np.exp(-((S - 0.36) / 0.20) ** 2)
    rh, rw = p["rim"]
    edge = 1 - r
    ew = rw / np.maximum(w, 0.05)
    helix = rh * (np.exp(-(edge / ew) ** 2) - 0.55 * np.exp(-((edge - 2.2 * ew) / ew) ** 2)) * smooth((S - p["lobe"]) / 0.12) * smooth((T + 0.2) / 0.3 + (S - 0.6) / 0.1)
    ah_path = 0.45 - 0.25 * smooth((S - 0.3) / 0.6)            # antihelix runs inside the rim, curving toward the root
    ah = p["ah"] * np.exp(-((T - ah_path) / 0.16) ** 2) * smooth((S - 0.25) / 0.15) * (1 - smooth((S - 0.9) / 0.1))
    trag = 0.0
    if p.get("tragus"):
        trag = 0.22 * np.exp(-((T + 0.85) / 0.12) ** 2) * np.exp(-((S - 0.30) / 0.07) ** 2)
    nf, fa = p["folds"]; folds = 0.0
    if nf:
        folds = fa * np.sin(np.pi * nf * (T + 1) / 2 + 0.6) ** 2 * smooth((S - 0.2) / 0.2) * (1 - smooth((S - 0.95) / 0.05))
    lobe_th = 0.18 * (1 - smooth(S / p["lobe"]))            # fleshy lobe thicker
    x = bowl + helix + ah + trag + folds
    th = p["thick"] + lobe_th
    front = np.stack([x, y, z], -1); back = np.stack([x - th, y, z], -1)
    # mesh: front + back surfaces, stitched at the boundary
    idx = lambda i, j, side: side * ns * nt + i * nt + j
    V = np.concatenate([front.reshape(-1, 3), back.reshape(-1, 3)])
    F = []
    for i in range(ns - 1):
        for j in range(nt - 1):
            a, b, c, d = idx(i, j, 0), idx(i + 1, j, 0), idx(i + 1, j + 1, 0), idx(i, j + 1, 0)
            F += [(a, b, c), (a, c, d)]
            a, b, c, d = idx(i, j, 1), idx(i + 1, j, 1), idx(i + 1, j + 1, 1), idx(i, j + 1, 1)
            F += [(a, c, b), (a, d, c)]
    ring = [(i, 0) for i in range(ns)] + [(ns - 1, j) for j in range(nt)] + [(i, nt - 1) for i in range(ns - 1, -1, -1)] + [(0, j) for j in range(nt - 1, -1, -1)]
    for (i0, j0), (i1, j1) in zip(ring, ring[1:]):
        a, b = idx(i0, j0, 0), idx(i1, j1, 0); c, d = idx(i1, j1, 1), idx(i0, j0, 1)
        F += [(a, d, c), (a, c, b)]
    V = np.array(V); F = np.array(F)
    # attachment: root line = anterior edge (t=-1) over the root zone s in [0.15, 0.6]; rotate the auricle outward about it
    root = front[:, 0][(s > 0.15) & (s < 0.6)].mean(0)
    pr = np.radians(p["proj"]); R = np.array([[np.cos(pr), np.sin(pr), 0], [-np.sin(pr), np.cos(pr), 0], [0, 0, 1]])
    Vr = (V - root) @ R.T
    # x' grows with y (posterior edge lifts laterally)  -> rotation in x-y plane by +proj
    tl = np.radians(p["tilt"]); Rt = np.array([[1, 0, 0], [0, np.cos(tl), np.sin(tl)], [0, -np.sin(tl), np.cos(tl)]])
    Vr = Vr @ Rt.T            # tilt the long axis backward
    Vr[:, 0] -= Vr[:, 0].min() if Vr[:, 0].min() < 0 else 0.0     # sit on the skull plane x = 0
    return Vr, F, root

def landmarks(V, p):
    top = V[np.argmax(V[:, 2])]; bot = V[np.argmin(V[:, 2])]
    rootc = np.array([0.0, 0.0, 0.0])
    tip = V[np.argmax(np.linalg.norm(V - rootc, axis=1))]
    return {"superaurale_u": float(top[2]), "subaurale_u": float(bot[2]), "auricle_height_cm": float(top[2] - bot[2]),
            "tip": tip.tolist(), "tip_distance_from_root_cm": float(np.linalg.norm(tip - rootc)),
            "auricle_projection_cm": float(V[:, 0].max()), "max_breadth_y_cm": float(V[:, 1].max() - V[:, 1].min())}

def depth_image(hx, hy, dep, F, ppcm, origin, size):
    W, H = size; px = (hx - origin[0]) * ppcm; py = H - (hy - origin[1]) * ppcm
    D = np.full((H, W), np.nan)
    for t in F:
        a, b, c = t
        xs = np.array([px[a], px[b], px[c]]); ys = np.array([py[a], py[b], py[c]]); ds = np.array([dep[a], dep[b], dep[c]])
        x0, x1 = int(max(np.floor(xs.min()), 0)), int(min(np.ceil(xs.max()) + 1, W)); y0, y1 = int(max(np.floor(ys.min()), 0)), int(min(np.ceil(ys.max()) + 1, H))
        if x0 >= x1 or y0 >= y1: continue
        den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(den) < 1e-9: continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        w1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den; w2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den; w3 = 1 - w1 - w2
        m = (w1 >= -1e-3) & (w2 >= -1e-3) & (w3 >= -1e-3)
        if not m.any(): continue
        dd = w1 * ds[0] + w2 * ds[1] + w3 * ds[2]
        sub = D[y0:y1, x0:x1]; cur = np.where(np.isnan(sub), -1e9, sub); sub[m] = np.maximum(cur[m], dd[m]); D[y0:y1, x0:x1] = sub
    return D

def hillshade(D, ppcm, az=315, alt=35, tick_origin=None, tick=1.0):
    from PIL import Image, ImageDraw
    Z = np.where(np.isnan(D), np.nanmin(D) - 0.5 if np.isfinite(np.nanmin(D)) else 0, D)
    gy, gx = np.gradient(Z * ppcm)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    a, al = np.radians(az), np.radians(alt)
    hs = np.sin(al) * np.cos(slope) + np.cos(al) * np.sin(slope) * np.cos(a - aspect)
    img = np.where(np.isnan(D), 250, np.clip(60 + 190 * hs, 0, 255))
    im = Image.fromarray(img.astype(np.uint8)).convert("RGB")
    if tick_origin is not None:
        d = ImageDraw.Draw(im); H = im.height
        for k in range(int(np.ceil(tick_origin)), int(tick_origin + H / ppcm) + 1):
            y = H - (k - tick_origin) * ppcm; d.line([(0, y), (6 if k % 5 else 12, y)], fill=(200, 40, 40))
    return im

def render_views(V, F, size=360, span=13.0):
    x, y, z = V[:, 0], V[:, 1], V[:, 2]
    zc = (z.max() + z.min()) / 2 - span / 2; ppcm = size / span
    lat = hillshade(depth_image(-y, z, x, F, ppcm, (-(span / 2) - 1.5, zc), (size, size)), ppcm, tick_origin=zc)        # lateral, from +x
    post = hillshade(depth_image(x, z, y, F, ppcm, (-2.0, zc), (int(size * 0.6), size)), ppcm, tick_origin=zc)          # posterior
    top = hillshade(depth_image(-y, x, z, F, ppcm, (-(span / 2) - 1.5, -2.0), (size, int(size * 0.5))), ppcm, tick_origin=-2.0)  # from above
    return lat, post, top

def main(out):
    from PIL import Image, ImageDraw
    os.makedirs(out, exist_ok=True); res = {}; tiles = []
    for name, p in FAM.items():
        V, F, root = build(p)
        lm = landmarks(V, p); res[name] = {"params": p, "landmarks": lm}
        with open(os.path.join(out, name + ".obj"), "w") as o:
            o.write("".join("v %.4f %.4f %.4f\n" % tuple(v) for v in V)); o.write("".join("f %d %d %d\n" % tuple(f + 1) for f in F))
        lat, post, top = render_views(V, F)  # noqa
        tile = Image.new("RGB", (lat.width + post.width + 10, lat.height + top.height + 40), "white")
        tile.paste(lat, (0, 30)); tile.paste(post, (lat.width + 10, 30)); tile.paste(top, (0, 30 + lat.height + 5))
        ImageDraw.Draw(tile).text((5, 5), "%s  L %.1f cm  proj %.2f cm  (lateral | posterior | from above; 1 cm ticks)" % (name, p["L"], lm["auricle_projection_cm"]), fill=(0, 0, 0))
        tiles.append(tile)
    W = max(t.width for t in tiles); cols = 2; rows = (len(tiles) + 1) // cols
    sheet = Image.new("RGB", (W * cols, rows * tiles[0].height), "white")
    for k, t in enumerate(tiles): sheet.paste(t, ((k % cols) * W, (k // cols) * tiles[0].height))
    sheet.save(os.path.join(out, "ear_families_sheet.jpg"), quality=88)
    json.dump(res, open(os.path.join(out, "ear_families.json"), "w"), indent=1)
    for k, v in res.items(): print(k, {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v["landmarks"].items() if a != "tip"})

if __name__ == "__main__":
    main(sys.argv[1])
