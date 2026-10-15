# RM-OT-05V: INFERRED field construction for v_rebuild.py.
# field spec (all optional):
#   {"blur_cm": s, "offset_cm": d,                      -> base = gaussian(phi_src, s) + d   (smoothed source moved inward by d)
#    "offset_regions": [{"region": R, "extra_cm": e, "t": w}],  -> spatially varying extra inward offset inside R (smooth edge w)
#    "base": "source" | "none",                          -> "none": start from +inf (pure primitives)
#    "primitives": [{"op": "union"|"sub"|"inter", "k": k, "sdf": REGION_SPEC} |
#                   {"op": ..., "k": k, "mesh": {"select": REGION_SPEC, "mirror_x": x0}}],
#    "ground_z": z0}                                     -> nothing below the sole plane
import numpy as np, igl
from v_engine import eval_region, smin, smax, blur_offset

def opened_sdf(phi, G, r):
    """SDF of the morphological opening (ball radius r) of {phi < 0}: erosion = {phi < -r}; opened distance = dist(eroded) - r."""
    import scipy.ndimage as ndi
    E = phi < -r
    if not E.any(): return np.full(phi.shape, 1e3)
    return ndi.distance_transform_edt(~E, sampling=G.h) - r

def mesh_sdf(S, sel, mirror_x, G, P, log):
    V = S['V'].astype(np.float64); F = S['F']; g = eval_region(sel, V); fsel = (g[F] < 0).all(1); Fs = F[fsel]
    u = np.unique(Fs); mp = -np.ones(len(V), np.int64); mp[u] = np.arange(len(u)); Vs = V[u].copy(); Fs = mp[Fs]
    if mirror_x is not None:
        Vs[:, 0] = 2 * mirror_x - Vs[:, 0]; Fs = Fs[:, ::-1]
    log.setdefault('mesh_primitives', []).append(dict(faces=int(len(Fs)), mirror_x=mirror_x))
    return igl.signed_distance(P, Vs, Fs.astype(np.int64), igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)[0].reshape(G.n)

def build(spec, phi_src, G, P, S, log):
    if spec.get('base', 'source') == 'none':
        phi = np.full(G.n, 1e3)
    else:
        import scipy.ndimage as ndi
        src = phi_src
        if spec.get('open_cm', 0) > 0:   # morphological opening of the source solid: removes features thinner than 2r (braids, sheets, relief)
            src = opened_sdf(phi_src, G, spec['open_cm'])
            if 'open_region' in spec:   # opening only inside a sub-region (smoothly), source elsewhere
                g = eval_region(spec['open_region'], P).reshape(G.n); w = np.clip(-g / spec.get('open_t', 2.0), 0, 1); w = w * w * (3 - 2 * w)
                src = (1 - w) * phi_src + w * src
        b0 = spec.get('blur_cm', 0.0); phi = ndi.gaussian_filter(src, b0 / G.h, mode='nearest') if b0 > 0 else src.copy()
        for o in spec.get('blur_regions', []):   # locally stronger / weaker smoothing
            g = eval_region(o['region'], P).reshape(G.n); w = np.clip(-g / o.get('t', 3.0), 0, 1); w = w * w * (3 - 2 * w)
            phi = (1 - w) * phi + w * ndi.gaussian_filter(src, o['blur_cm'] / G.h, mode='nearest')
        phi = phi + spec.get('offset_cm', 0.0)
        for o in spec.get('offset_regions', []):
            g = eval_region(o['region'], P).reshape(G.n); w = np.clip(-g / o.get('t', 2.0), 0, 1); w = w * w * (3 - 2 * w)
            phi = phi + w * o['extra_cm']
    for pr in spec.get('primitives', []):
        if pr.get('op') == 'inter_env':
            pass
        elif 'field' in pr:   # a complete sub-field (same spec language), e.g. shrunk source restricted below the neck
            d = build(pr['field'], phi_src, G, P, S, log)
        elif 'source' in pr:   # (opened / blurred) source solid intersected with a sub-region
            import scipy.ndimage as ndi
            so = pr['source']; src = opened_sdf(phi_src, G, so['open_cm']) if so.get('open_cm', 0) > 0 else phi_src
            if so.get('blur_cm', 0) > 0: src = ndi.gaussian_filter(src, so['blur_cm'] / G.h, mode='nearest')
            d = smax(src, eval_region(so['within'], P).reshape(G.n), so.get('k', 1.0))
        elif 'sdf' in pr: d = eval_region(pr['sdf'], P).reshape(G.n)
        elif 'file' in pr['mesh']:   # external placed mesh (e.g. the source tail), optionally smoothed
            import trimesh, scipy.ndimage as ndi
            tm = trimesh.load(pr['mesh']['file'], process=False)
            d = igl.signed_distance(P, np.asarray(tm.vertices, float), np.asarray(tm.faces, np.int64), igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)[0].reshape(G.n)
            if pr['mesh'].get('blur_cm', 0) > 0: d = ndi.gaussian_filter(d, pr['mesh']['blur_cm'] / G.h, mode='nearest')
            log.setdefault('mesh_primitives', []).append(dict(file=pr['mesh']['file'], faces=int(len(tm.faces))))
        else: d = mesh_sdf(S, pr['mesh']['select'], pr['mesh'].get('mirror_x'), G, P, log)
        k = pr.get('k', 0.0); op = pr.get('op', 'union')
        if op == 'inter_env':   # intersect with an envelope = smooth union of its parts (each part a primitive spec)
            env = None
            for part in pr['parts']:
                dp = build(dict(base='none', primitives=[dict(part, op='union', k=0.0)]), phi_src, G, P, S, log) if 'base' not in part else build(part, phi_src, G, P, S, log)
                env = dp if env is None else smin(env, dp, pr.get('k_parts', 4.0))
            phi = smax(phi, env, k); continue
        phi = smin(phi, d, k) if op == 'union' else (smax(phi, -d, k) if op == 'sub' else smax(phi, d, k))
    if 'ground_z' in spec:
        phi = np.maximum(phi, spec['ground_z'] - P[:, 2].reshape(G.n))
    return phi
