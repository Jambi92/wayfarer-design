import numpy as np, json
import measure as M
rng = np.random.default_rng(2)
res = {}
for nm, path in (("TS8", "/tmp/claude-0/rb/out/saurin_ts8_body_035.npz"), ("TS9", "/tmp/claude-0/rb/out/saurin_ts9_body_035.npz")):
    z = np.load(path); v = z["v"].astype(float); f = z["f"]
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]; ar = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    n = 600000; k = rng.choice(len(f), n, p=ar / ar.sum()); r1, r2 = rng.random(n), rng.random(n); s = np.sqrt(r1)
    P = a[k] * (1 - s)[:, None] + b[k] * (s * (1 - r2))[:, None] + c[k] * (s * r2)[:, None]   # (X, F, U) cm
    M.sample = lambda cid, n=0, P=P: P.copy()
    Pp, H, rows, ang, sr = M.analyse(0, nm, facing_override=0.0)
    lm, wid, dep, U = M.landmarks(Pp, H, rows); tm = M.tail_metrics(Pp, H, rows, lm)
    lm = {kk: (float(vv) / H if kk.endswith("_u") and vv is not None else (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)) for kk, vv in lm.items()}
    for kk in ("crotch", "axilla"):
        if lm.get(kk) is not None: lm[kk] = lm[kk] / H
    res[nm] = dict(height_cm=float(H), **lm, **tm)
    print(nm, json.dumps({kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in res[nm].items()}))
json.dump(res, open("measure_ts.json", "w"), indent=1, default=float)
