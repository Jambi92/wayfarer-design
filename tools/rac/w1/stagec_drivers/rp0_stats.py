"""RAC RP0: read-only mesh statistics for a race source (npz with V/F[/keep] or v/f). No geometry is written.
Usage: python3 rp0_stats.py OUT.json NAME=path[:unit_scale_to_cm][:upaxis] ...   (upaxis z default; 'y' for glTF Y-up)"""
import sys, json, hashlib, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
def stats(path, sc=1.0, up='z'):
    z = np.load(path, allow_pickle=True)
    V = (z['V'] if 'V' in z.files else z['v']).astype(np.float64) * sc; F = (z['F'] if 'F' in z.files else z['f']).astype(np.int64)
    if up == 'y': V = V[:, [0, 2, 1]] * np.array([1, -1, 1])
    keep = z['keep'].astype(bool) if 'keep' in z.files else np.ones(len(V), bool)
    F = F[keep[F].all(1)]
    used = np.unique(F); n = len(V)
    E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1)
    key = E[:, 0] * n + E[:, 1]; u, cnt = np.unique(key, return_counts=True)
    A = coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n))
    nc, lab = connected_components(A, directed=False); comps = len(np.unique(lab[used]))
    a = V[F[:, 1]] - V[F[:, 0]]; b = V[F[:, 2]] - V[F[:, 0]]; cr = np.cross(a, b); area = 0.5 * np.linalg.norm(cr, axis=1)
    vol = np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6.0
    Vu = V[used]; lo, hi = Vu.min(0), Vu.max(0)
    T = cKDTree(Vu); dd, _ = T.query(Vu, k=2); dup = int((dd[:, 1] < 1e-5).sum())
    M = Vu * np.array([-1, 1, 1]); dm, _ = T.query(M); 
    chi = len(used) - len(u) + len(F); genus = (2 * comps - chi) / 2 if (cnt == 2).all() else None
    el = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
    return {"vertices_used": int(len(used)), "vertices_total": int(n), "triangles": int(len(F)), "edges": int(len(u)), "components": int(comps),
            "boundary_edges": int((cnt == 1).sum()), "nonmanifold_edges": int((cnt > 2).sum()), "degenerate_tris_area_lt_1e-8cm2": int((area < 1e-8).sum()),
            "coincident_vertices_lt_1e-5cm": dup, "euler_genus_if_closed": genus, "signed_volume_l": round(vol / 1000, 3),
            "normals": "outward" if vol > 0 else "inward/inconsistent", "bbox_cm": [round(x, 2) for x in (hi - lo)], "min_up_cm": round(lo[2], 3),
            "stature_cm": round(hi[2] - lo[2], 4), "x_centre_cm": round((hi[0] + lo[0]) / 2, 3),
            "mirror_rms_cm": round(float(np.sqrt((dm ** 2).mean())), 4), "mirror_p99_cm": round(float(np.percentile(dm, 99)), 4),
            "edge_len_cm_p1_med_p99": [round(float(x), 4) for x in np.percentile(el, [1, 50, 99])],
            "file_sha256": hashlib.sha256(open(path, 'rb').read()).hexdigest()}
out = {}
for a in sys.argv[2:]:
    nm, rest = a.split('=', 1); parts = rest.split(':'); p = parts[0]; sc = float(parts[1]) if len(parts) > 1 else 1.0; up = parts[2] if len(parts) > 2 else 'z'
    out[nm] = stats(p, sc, up); out[nm]['path'] = p; print(nm, json.dumps(out[nm])[:400], flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
