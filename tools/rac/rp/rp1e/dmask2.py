# dmask2.py NAME "seed_xyz"(blender cm) R PROD.npz OUTDIR [depth_mm=0.2]
# Explicit topological D mask (ruling dc9d48f s3.1, order 647fa4e s6): seeded source-face flood fill bounded by explicit throat loops.
# The hidden handle interior is sealed from the exterior by a zero/sub-mm source neck; the production envelope bridges that neck.
# Throat loops = the source edge loops where the source surface passes through the production envelope at the neck
# (faces enclosed by the production envelope, winding number > 0.5, deeper than depth_mm, vs. the rest).
# Flood: from the seed face across face adjacency inside the enclosed set; the boundary edges of the flooded set are the frozen throat loops.
import sys, os, json, numpy as np, igl
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
name = sys.argv[1]; seed = np.array(eval(sys.argv[2]), float); R = float(sys.argv[3]); P = sys.argv[4]; out = sys.argv[5]
depth = (float(sys.argv[6]) if len(sys.argv) > 6 else 0.2) / 10
os.makedirs(out, exist_ok=True)
w = np.load('/home/claude/stc/rp1/weld.npz'); S = w['V'].astype(float); SF = w['F'].astype(np.int64)
z = np.load(P); V = z['V'].astype(float).copy(); V[:, 1] *= -1; F = z['F'].astype(np.int64)[:, ::-1].copy()   # analysis -> blender (mirror flips winding)
vol = np.einsum("ij,ij->i", V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6; print("envelope signed volume", round(vol, 1))
if vol < 0: F = F[:, ::-1].copy()
C = S[SF].mean(1); near = np.where(np.linalg.norm(C - seed, axis=1) < R)[0]
fsel = np.linalg.norm(V[F].mean(1) - seed, axis=1) < R + 3
wn = igl.fast_winding_number(V, F, C[near]) if hasattr(igl, 'fast_winding_number') else igl.winding_number(V, F, C[near])
dd, _, _ = igl.point_mesh_squared_distance(C[near], V, F[fsel]); dd = np.sqrt(dd)
inside = np.zeros(len(SF), bool); inside[near[(wn > 0.5) & (dd > depth)]] = True
nf = len(SF); E = np.vstack([SF[:, [0, 1]], SF[:, [1, 2]], SF[:, [2, 0]]]); E.sort(1); fid = np.tile(np.arange(nf), 3)
o = np.lexsort((E[:, 1], E[:, 0])); Es = E[o]; fs = fid[o]; same = (Es[1:] == Es[:-1]).all(1); a = fs[:-1][same]; b = fs[1:][same]; ek = Es[:-1][same]
m = inside[a] & inside[b]; idx = np.where(inside)[0]; loc = -np.ones(nf, int); loc[idx] = np.arange(len(idx))
A = sp.coo_matrix((np.ones(m.sum()), (loc[a[m]], loc[b[m]])), shape=(len(idx), len(idx))); n, lab = connected_components(A, directed=False)
sf = idx[np.argmin(np.linalg.norm(C[idx] - seed, axis=1))]; mask = idx[lab == lab[loc[sf]]]
inm = np.zeros(nf, bool); inm[mask] = True
bnd = ek[inm[a] ^ inm[b]]   # throat edges
# chain throat edges into loops
adj = {}
for u, v in bnd: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
seen = set(); loops = []
for s0 in adj:
    if s0 in seen: continue
    L = [s0]; seen.add(s0); cur = s0; prev = None
    while True:
        nx = [x for x in adj[cur] if x != prev and x not in seen]
        if not nx: break
        prev, cur = cur, nx[0]; L.append(cur); seen.add(cur)
    loops.append([int(x) for x in L])
area = 0.5 * np.linalg.norm(np.cross(S[SF[:, 1]] - S[SF[:, 0]], S[SF[:, 2]] - S[SF[:, 0]]), axis=1)
vids = np.unique(SF[mask])
info = dict(name=name, method='seeded source-face flood fill bounded by explicit throat loops (production-envelope neck crossing)', seed_blender_cm=seed.tolist(),
            seed_face=int(sf), search_radius_cm=R, depth_mm=depth * 10, envelope_mesh=os.path.basename(P), mask_faces=int(len(mask)), mask_vertices=int(len(vids)),
            mask_area_cm2=round(float(area[mask].sum()), 4), source_area_cm2=round(float(area.sum()), 2), area_share_pct=round(float(area[mask].sum() / area.sum() * 100), 5),
            throat_loops=len(loops), throat_loop_lengths=[len(l) for l in loops], throat_loop_vertex_ids=loops,
            other_enclosed_components=int(n - 1), mask_bbox=[S[vids].min(0).round(2).tolist(), S[vids].max(0).round(2).tolist()])
np.save(os.path.join(out, name + '_source_faces.npy'), mask); np.save(os.path.join(out, name + '_source_vertices.npy'), vids)
json.dump(info, open(os.path.join(out, name + '_info.json'), 'w'), indent=1)
print({k: v for k, v in info.items() if k != 'throat_loop_vertex_ids'})
