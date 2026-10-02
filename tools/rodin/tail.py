import numpy as np, json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
z = np.load("mesh.npz"); V = z["v"]; Fa = z["f"]; lab = np.load("lab.npy")
out = {}
for cid, nm in ((11, "c11_profile_panel"), (7, "c07_rear34_panel"), (13, "c13_rear_panel_janus")):
    fs = Fa[lab[Fa[:, 0]] == cid]; used = np.unique(fs); rm = -np.ones(len(V), int); rm[used] = np.arange(len(used))
    v = V[used]; f = rm[fs]; H = v[:, 1].max() - v[:, 1].min(); y0 = v[:, 1].min()
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]); w = np.linalg.norm(v[e[:, 0]] - v[e[:, 1]], axis=1)
    G = coo_matrix((w, (e[:, 0], e[:, 1])), shape=(len(v), len(v))).tocsr(); G = G.maximum(G.T)
    # body axis: centroid of 0.55-0.75H band; tail tip = farthest point (horizontal) from it below 0.45H
    band = v[(v[:, 1] - y0 > 0.55 * H) & (v[:, 1] - y0 < 0.75 * H)]; ax = band[:, [0, 2]].mean(0)
    low = np.where(v[:, 1] - y0 < 0.45 * H)[0]
    hd = np.linalg.norm(v[low][:, [0, 2]] - ax, axis=1); tip = low[np.argmax(hd)]
    # root: point on the posterior pelvis at ~0.47H nearest the tip direction
    tipdir = (v[tip, [0, 2]] - ax); tipdir /= np.linalg.norm(tipdir)
    pel = np.where((np.abs(v[:, 1] - y0 - 0.47 * H) < 0.01 * H) & (np.linalg.norm(v[:, [0, 2]] - ax, axis=1) < 0.15 * H))[0]
    proj = (v[pel][:, [0, 2]] - ax) @ tipdir
    root = pel[np.argmax(proj)]
    dist, pred = dijkstra(G, indices=tip, return_predecessors=True)
    path = [root]; 
    while path[-1] != tip and pred[path[-1]] >= 0: path.append(pred[path[-1]])
    P = v[path]; L = float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum()) / H
    # cross-section near the root: points within 0.03H of the root along the path, perpendicular extent
    near = v[np.linalg.norm(v - v[root], axis=1) < 0.10 * H]
    out[nm] = dict(surface_path_length=round(L, 3), tip_height=round(float(v[tip, 1] - y0) / H, 3),
                   tip_horizontal_from_axis=round(float(hd.max()) / H, 3), root_to_tip_straight=round(float(np.linalg.norm(v[tip]-v[root]))/H,3), root_height=round(float(v[root, 1] - y0) / H, 3))
    print(nm, out[nm])
json.dump(out, open("tail.json", "w"), indent=1)
