# gate_topo.py MESH.npz OUT.json : topology, orientation, face quality (T-4), poles
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
z = np.load(sys.argv[1]); V = z['V']; Q = z['Q']; n = len(V)
E = np.vstack([Q[:, [i, (i + 1) % 4]] for i in range(4)]); key = np.sort(E, 1)
u, cnt = np.unique(key, axis=0, return_counts=True)
dirdup = (np.unique(E, axis=0, return_counts=True)[1] > 1).sum()
A = sp.coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(n, n)); ncomp, _ = connected_components(A, directed=False)
used = np.zeros(n, bool); used[Q.ravel()] = True
chi = n - len(u) + len(Q)
# non-manifold vertices: the faces around a vertex must form a single fan (edge-connected)
vf = {}
for fi, q in enumerate(Q):
    for v in q: vf.setdefault(v, []).append(fi)
nmv = 0
for v, fs in vf.items():
    if len(fs) < 2: continue
    es = {}
    for f in fs:
        q = list(Q[f]); i = q.index(v); a, b = q[(i + 1) % 4], q[(i - 1) % 4]
        es.setdefault(a, []).append(f); es.setdefault(b, []).append(f)
    adj = {f: set() for f in fs}
    for e, ff in es.items():
        for f1 in ff:
            for f2 in ff:
                if f1 != f2: adj[f1].add(f2)
    seen = {fs[0]}; st = [fs[0]]
    while st:
        f = st.pop()
        for g in adj[f]:
            if g not in seen: seen.add(g); st.append(g)
    if len(seen) != len(fs): nmv += 1
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
vol = np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum() / 6
area = 0.5 * (np.linalg.norm(np.cross(V[Q[:, 1]] - V[Q[:, 0]], V[Q[:, 2]] - V[Q[:, 0]]), axis=1) + np.linalg.norm(np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 0]]), axis=1))
L = np.linalg.norm(V[u[:, 0]] - V[u[:, 1]], axis=1)
def ang(a, b, c):
    x = a - b; y = c - b; return np.degrees(np.arccos(np.clip((x * y).sum(1) / (np.linalg.norm(x, axis=1) * np.linalg.norm(y, axis=1) + 1e-30), -1, 1)))
angs = np.stack([ang(V[Q[:, (i - 1) % 4]], V[Q[:, i]], V[Q[:, (i + 1) % 4]]) for i in range(4)], 1)
el = np.stack([np.linalg.norm(V[Q[:, (i + 1) % 4]] - V[Q[:, i]], axis=1) for i in range(4)], 1)
aspect = el.max(1) / np.maximum(el.min(1), 1e-30)
val = np.bincount(u.ravel(), minlength=n)
coinc = len(cKDTree(V).query_pairs(1e-6))
r = dict(vertices=int(n), faces=int(len(Q)), quads_pct=100.0, triangles=0, ngons=0, components=int(ncomp), boundary_edges=int((cnt == 1).sum()),
         nonmanifold_edges=int((cnt > 2).sum()), nonmanifold_vertices=int(nmv), directed_edge_duplicates=int(dirdup), unused_vertices=int((~used).sum()),
         coincident_vertex_pairs=int(coinc), euler=int(chi), genus=float((2 - chi) / 2), degenerate_faces_area_lt_1em6cm2=int((area < 1e-6).sum()),
         min_face_area_cm2=float(area.min()), signed_volume_L=float(vol / 1000), min_edge_mm=float(L.min() * 10), median_edge_mm=float(np.median(L) * 10),
         T4_angles_45_135_pct=float(((angs >= 45) & (angs <= 135)).all(1).mean() * 100), T4_aspect_le4_pct=float((aspect <= 4).mean() * 100),
         poles_valence3=int((val == 3).sum()), poles_valence5plus=int((val >= 5).sum()))
json.dump(r, open(sys.argv[2], 'w'), indent=1); print(json.dumps(r, indent=1))
