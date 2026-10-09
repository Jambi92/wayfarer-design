# RAC W2I4 §7: recover the accepted final-surface scale seeds from the frozen final surface (the final-brow build carried seeds15.npy, which
# is not in the repo or on the PC). The accepted generator (gate1 g7surfc.py) raises each Voronoi cell as a plateau dome and sinks the cell
# borders into grooves (disp = h (groove (dome + tilt) - 0.35)). Seeds are therefore recovered as CELL CENTROIDS: the scaly mesh is cut at
# the grooves (normal displacement below THR x the local relief height H), the connected plateau components are the cells, and each seed is
# the vertex nearest the component centroid. Validation: regenerate the frozen surface with g7surfc + the recovered seeds and compare with
# the frozen delta (run separately). Usage: python3 sa_seeds.py OUT_SEEDS.npy [THR]
import sys, numpy as np, igl
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
THR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
up = np.load(S + '/w2i/rodin/c12/g15up.npz'); V = up['V'].astype(float); F = up['F'].astype(np.int64)
d = np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_surface_delta.npz')['d'].astype(float)
reg = np.load(S + '/w2i/rodin/c12/g15reg.npz'); FAM = reg['FAM']; H = reg['H'].astype(float)
N = igl.per_vertex_normals(V, F); s = (d * N).sum(1); n = len(V); scaly = (FAM != 6) & (FAM != 7)
up_ = scaly & (s > THR * H)
E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E = E[up_[E[:, 0]] & up_[E[:, 1]]]
A = sparse.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr()
nc, lab = connected_components(A, directed=False)
lab = np.where(up_, lab, -1); idx = np.where(up_)[0]; L = lab[idx]
cnt = np.bincount(L, minlength=nc); good = cnt >= 6
cen = np.zeros((nc, 3))
for k in range(3): cen[:, k] = np.bincount(L, weights=V[idx, k], minlength=nc)
cen = cen[good] / cnt[good][:, None]
tree = cKDTree(V[idx]); seeds = idx[tree.query(cen)[1]]
seeds = np.unique(seeds); np.save(sys.argv[1], seeds)
print('plateau components', int(good.sum()), 'of', nc, '; seeds', len(seeds), '; median size', int(np.median(cnt[good])))
