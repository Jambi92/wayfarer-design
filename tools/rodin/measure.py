# Rodin Saurin sheet: per-body normalized measurements from surface samples + horizontal sections.
import numpy as np, json, sys
from scipy import ndimage
z = np.load("/tmp/claude-0/rodin/mesh.npz"); V = z["v"]; Fa = z["f"]; lab = np.load("/tmp/claude-0/rodin/lab.npy")
rng = np.random.default_rng(1)

def sample(cid, n=600000):
    fs = Fa[lab[Fa[:, 0]] == cid]; a, b, c = V[fs[:, 0]], V[fs[:, 1]], V[fs[:, 2]]
    ar = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1); p = ar / ar.sum()
    k = rng.choice(len(fs), n, p=p); r1, r2 = rng.random(n), rng.random(n); s = np.sqrt(r1)
    P = a[k] * (1 - s)[:, None] + b[k] * (s * (1 - r2))[:, None] + c[k] * (s * r2)[:, None]
    return np.stack([P[:, 0], P[:, 2], P[:, 1]], 1)   # -> (x, f(=objZ), u(=objY))

def blobs(pts2, cell):
    lo = pts2.min(0) - 2 * cell; ij = np.floor((pts2 - lo) / cell).astype(int); sh = ij.max(0) + 3
    g = np.zeros(sh, bool); g[ij[:, 0], ij[:, 1]] = True
    g = ndimage.binary_closing(g, iterations=2); g = ndimage.binary_fill_holes(g)
    L, n = ndimage.label(g); out = []
    for i in range(1, n + 1):
        m = L == i; ii, jj = np.nonzero(m)
        out.append(dict(x0=lo[0] + ii.min() * cell, x1=lo[0] + (ii.max() + 1) * cell, f0=lo[1] + jj.min() * cell,
                        f1=lo[1] + (jj.max() + 1) * cell, cx=lo[0] + (ii.mean() + .5) * cell, cf=lo[1] + (jj.mean() + .5) * cell,
                        area=m.sum() * cell * cell))
    return out

def analyse(cid, name, facing_override=None):
    P = sample(cid); u0 = P[:, 2].min(); H = P[:, 2].max() - u0; P[:, 2] -= u0
    # facing: best bilateral-symmetry plane of the upper body (0.5-1.0H), sign from the snout
    from scipy.spatial import cKDTree
    up = P[P[:, 2] > 0.5 * H]; up = up[rng.choice(len(up), min(40000, len(up)), replace=False)]
    tree = cKDTree(up); best = None
    for th in np.radians(np.arange(0, 180, 1.0)):
        n = np.array([np.cos(th), np.sin(th)])                       # lateral axis candidate (x,f)
        for off in np.linspace(-0.06 * H, 0.06 * H, 13):
            dd = up[:, :2] @ n - (up[:, :2].mean(0) @ n + off)
            R = up.copy(); R[:, :2] = up[:, :2] - 2 * dd[:, None] * n[None, :]
            sc = tree.query(R[::8], k=1)[0].mean()
            if best is None or sc < best[0]: best = (sc, th, off)
    th = best[1]; lat = np.array([np.cos(th), np.sin(th)]); fwd = np.array([-lat[1], lat[0]])
    nk = P[(P[:, 2] > 0.80 * H) & (P[:, 2] < 0.86 * H)]; hd = P[P[:, 2] > 0.90 * H]
    hv = hd[:, :2].mean(0) - nk[:, :2].mean(0)
    if hv @ fwd < 0: fwd = -fwd
    ang = np.arctan2(fwd[0], fwd[1]) if facing_override is None else np.radians(facing_override)
    snout_ratio = float(best[0] / H)                                  # symmetry residual (lower = more symmetric)
    c = up[:, :2].mean(0) + lat * best[2]
    ca, sa = np.cos(-ang), np.sin(-ang)
    x = P[:, 0] - c[0]; f = P[:, 1] - c[1]
    P[:, 0], P[:, 1] = x * ca + f * sa, -x * sa + f * ca          # rotate so snout points to +F
    cell = 0.006 * H; dz = 0.004 * H
    rows = []
    for k in range(int(0.995 * H / dz)):
        u = (k + 0.5) * dz; m = np.abs(P[:, 2] - u) < dz / 2
        if m.sum() < 30: rows.append(None); continue
        rows.append((u, blobs(P[m][:, :2], cell)))
    return P, H, rows, float(np.degrees(ang)), snout_ratio

def central(bl, fref=None):
    # blob nearest the body axis (x = 0)
    return min(bl, key=lambda b: abs(b["cx"]) + (0 if fref is None else 0.3 * abs(b["cf"] - fref)))

def landmarks(P, H, rows):
    U = np.array([r[0] if r else np.nan for r in rows])
    # per-slice main (axial) blob
    main = []
    for r in rows:
        if r is None: main.append(None); continue
        main.append(central(r[1]))
    wid = np.array([m["x1"] - m["x0"] if m else np.nan for m in main]) / H
    dep = np.array([m["f1"] - m["f0"] if m else np.nan for m in main]) / H
    nbl = np.array([len(r[1]) if r else 0 for r in rows])
    out = {}
    # crotch: scanning down from 0.6H, first slice where the central blob is much narrower than the hips and two
    # blobs straddle x=0 (legs)
    crotch = None
    for k in range(len(rows) - 1, -1, -1):
        if rows[k] is None or U[k] > 0.62 * H or U[k] < 0.3 * H: continue
        legs = [b for b in rows[k][1] if abs(b["cx"]) < 0.13 * H and (b["f1"] - b["f0"]) > 0.03 * H]
        left = [b for b in legs if b["x1"] < 0.003 * H]; right = [b for b in legs if b["x0"] > -0.003 * H]
        if left and right:
            crotch = U[k]; break
    out["crotch"] = crotch
    # axilla: scanning down from 0.85H, first slice where lateral (arm) blobs separate from the torso on both sides
    ax = None
    for k in range(len(rows) - 1, -1, -1):
        if rows[k] is None or U[k] > 0.84 * H or U[k] < 0.55 * H: continue
        m = main[k]; arms = [b for b in rows[k][1] if b is not m and abs(b["cx"]) > 0.06 * H]
        if any(b["cx"] > 0 for b in arms) and any(b["cx"] < 0 for b in arms):
            ax = U[k]; break
    out["axilla"] = ax
    # neck: minimum central-blob width between axilla and 0.93H; head base = where depth starts to grow (snout)
    sel = [k for k in range(len(rows)) if rows[k] and ax and ax + 0.02 * H < U[k] < 0.95 * H]
    kn = min(sel, key=lambda k: wid[k]) if sel else None
    out["neck_min_u"] = U[kn] if kn is not None else None
    out["neck_min_width"] = wid[kn] if kn is not None else None
    # jaw (lowest point of the forward-projecting snout): head points with f > neck front + 0.05H
    nf = main[kn]["f1"] if kn is not None else 0
    sn = P[(P[:, 1] > nf + 0.04 * H) & (P[:, 2] > 0.8 * H)]
    out["jaw_u"] = float(sn[:, 2].min()) if len(sn) else None
    # shoulder breadth: max lateral extent of everything 0.00-0.04H above the axilla
    if ax:
        b = P[(P[:, 2] > ax) & (P[:, 2] < ax + 0.04 * H)]
        out["shoulder_breadth"] = float(b[:, 0].max() - b[:, 0].min()) / H
    # thorax (axilla .. waist): waist = min central width between crotch+0.05H and axilla-0.08H
    if ax and crotch and ax - crotch > 0.15 * H:
        selw = [k for k in range(len(rows)) if rows[k] and crotch + 0.05 * H < U[k] < ax - 0.08 * H]
        kw = min(selw, key=lambda k: wid[k]); out["waist_u"] = U[kw]; out["waist_width"] = wid[kw]; out["waist_depth"] = dep[kw]
        selt = [k for k in range(len(rows)) if rows[k] and U[kw] < U[k] < ax]
        kt = max(selt, key=lambda k: wid[k]); out["thorax_width"] = wid[kt]; out["thorax_u"] = U[kt]
        out["thorax_depth"] = float(np.nanmax([dep[k] for k in selt]))
        selp = [k for k in range(len(rows)) if rows[k] and crotch < U[k] < U[kw]]
        kp = max(selp, key=lambda k: wid[k]); out["pelvis_width"] = wid[kp]; out["pelvis_u"] = U[kp]
        out["pelvis_depth"] = float(np.nanmax([dep[k] for k in selp]))
        # sagittal centres
        out["thorax_cf"] = main[kt]["cf"] / H; out["pelvis_cf"] = main[kp]["cf"] / H
        ka = int(np.nanargmin(np.abs(U - (ax - 0.01 * H)))); out["chest_width_below_axilla"] = wid[ka]; out["chest_depth_below_axilla"] = dep[ka]
        selu = [k for k in range(len(rows)) if rows[k] and ax < U[k] < ax + 0.12 * H]
        out["upper_thorax_depth"] = float(np.nanmax([dep[k] for k in selu]))
    # hip-joint spacing: leg blob centroids 0.04H below crotch
    if crotch:
        k = int(np.nanargmin(np.abs(U - (crotch - 0.04 * H))))
        legs = sorted([b for b in rows[k][1] if abs(b["cx"]) < 0.14 * H and b["area"] > 0.0004 * H * H], key=lambda b: -b["area"])[:2]
        if len(legs) == 2:
            out["hip_spacing"] = abs(legs[0]["cx"] - legs[1]["cx"]) / H; out["hip_cf"] = np.mean([b["cf"] for b in legs]) / H
    # knee / ankle: leg width profile (one leg, x>0 side) -> knee = min width 0.22-0.36H, ankle = min width 0.03-0.12H
    leg = []
    for k in range(len(rows)):
        if rows[k] is None or crotch is None or U[k] > crotch - 0.02 * H: leg.append(np.nan); continue
        lb = [b for b in rows[k][1] if b["cx"] > 0 and b["cx"] < 0.14 * H]
        leg.append(max(lb, key=lambda b: b["area"])["x1"] - max(lb, key=lambda b: b["area"])["x0"] if lb else np.nan)
    leg = np.array(leg) / H
    def argmin_in(a, lo, hi):
        ks = [k for k in range(len(U)) if lo * H < U[k] < hi * H and not np.isnan(a[k])]
        return U[min(ks, key=lambda k: a[k])] if ks else None
    out["knee_u"] = argmin_in(leg, 0.22, 0.34); out["ankle_u"] = argmin_in(leg, 0.025, 0.10)
    # foot length: ground slab (u < 0.035H), x>0 foot
    g = P[(P[:, 2] < 0.035 * H) & (P[:, 0] > 0)]
    if len(g): out["foot_length"] = float(g[:, 1].max() - g[:, 1].min()) / H; out["foot_width"] = float(g[:, 0].max() - g[:, 0].min()) / H
    out["ankle_cf"] = float(np.median(P[(P[:, 2] < 0.08 * H) & (P[:, 2] > 0.05 * H)][:, 1])) / H
    hd = P[P[:, 2] > (out["jaw_u"] or 0.9 * H)]
    out["head_cf"] = float(hd[:, 1].mean()) / H
    # arm (x>0): lowest point = fingertip; wrist = min lateral-blob width between fingertip+0.05H and axilla
    arm = P[(P[:, 0] > 0.10 * H) & (P[:, 2] < (ax or 0.8 * H)) & (P[:, 2] > 0.22 * H)]
    if len(arm):
        out["fingertip_u"] = float(arm[:, 2].min())
    return out, wid, dep, U

def tail_metrics(P, H, rows, lm):
    """Tail: points behind the pelvis back plane; base section at the plane, length from geodesic-free centreline."""
    if not lm.get("crotch"): return {}
    pel = [r for r in rows if r and lm["crotch"] < r[0] < (lm.get("waist_u") or lm["crotch"] + 0.1 * H)]
    back = np.median([central(r[1])["f0"] for r in pel])
    T = P[(P[:, 1] < back - 0.02 * H) & (P[:, 2] > 0.05 * H) & (P[:, 2] < lm.get("waist_u", 0.6 * H))]
    if len(T) < 2000: return {"tail": "absent"}
    # base section: points in a thin slab of F just behind the back plane
    sl = P[np.abs(P[:, 1] - (back - 0.03 * H)) < 0.004 * H]
    sl = sl[(sl[:, 2] > lm["crotch"] - 0.08 * H) & (sl[:, 2] < lm.get("waist_u", 0.6 * H))]
    bl = blobs(sl[:, [0, 2]], 0.006 * H) if len(sl) > 30 else []
    base = max(bl, key=lambda b: b["area"]) if bl else None
    # centreline: cluster tail points along their distance from the root, average per bin
    root = np.array([0.0, back, base["cf"] if base else lm["crotch"]])
    Tall = P[(P[:, 1] < back - 0.005 * H)]
    dist = np.linalg.norm(Tall - root, axis=1)
    bins = np.linspace(0, dist.max(), 60); cl = []
    for a, b in zip(bins[:-1], bins[1:]):
        m = (dist >= a) & (dist < b)
        if m.sum() > 20: cl.append(Tall[m].mean(0))
    cl = np.array(cl); L = float(np.linalg.norm(np.diff(cl, axis=0), axis=1).sum()) / H
    tip = Tall[np.argmax(dist)]
    return {"tail": "present", "tail_base_width": (base["x1"] - base["x0"]) / H if base else None,
            "tail_base_height": (base["f1"] - base["f0"]) / H if base else None,
            "tail_base_area": base["area"] / H / H if base else None, "tail_root_u": base["cf"] / H if base else None,
            "tail_length_centreline": L, "tail_tip_u": float(tip[2]) / H, "tail_tip_lateral": float(tip[0]) / H,
            "pelvis_back_cf": back / H}

if __name__ == "__main__":
    bodies = {"c12_front_panel": (12, None), "c11_profile_panel": (11, None), "c10_front34_panel": (10, None), "c07_rear34_panel": (7, None)}
    res = {}
    for nm, (cid, fo) in bodies.items():
        P, H, rows, ang, sr = analyse(cid, nm, fo)
        lm, wid, dep, U = landmarks(P, H, rows)
        tm = tail_metrics(P, H, rows, lm)
        lm = {k: (float(v) / H if k.endswith("_u") and v is not None and k not in () else (float(v) if isinstance(v, (int, float, np.floating)) else v)) for k, v in lm.items()}
        for k in ("crotch", "axilla"):
            if lm.get(k) is not None: lm[k] = lm[k] / H
        print(nm, 'crotch', lm.get('crotch'), 'axilla', lm.get('axilla'))
        res[nm] = dict(height_units=float(H), facing_deg_from_feet=ang, snout_dir_deg=sr, **lm, **tm)
        np.savez("/tmp/claude-0/rodin/prof_%s.npz" % nm, wid=wid, dep=dep, U=np.array(U) / H, P=P[::20] / H)
        print(nm, json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[nm].items()}))
    json.dump(res, open("/tmp/claude-0/rodin/measure.json", "w"), indent=1, default=float)
