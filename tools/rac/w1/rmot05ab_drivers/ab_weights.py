# RM-OT-05AB: temporary-rig vertex groups for donor C (scripted ASSIGNMENT only, per order 05AB s4: no per-vertex shapes).
# Each vertex is labelled by multi-source GEODESIC (surface edge-graph) distance to seed loops placed symmetrically either side of
# each estimated joint (so label boundaries fall at the joints), then blended across each boundary with a geodesic softmax
# (T = 1.5 cm, two strongest groups) so joints deform through a smooth transition band. Tail and neck/head are seeded into the
# rigid trunk group. Weights are computed on exact-position-welded vertices and copied to their UV-seam duplicates (no cracks).
# Usage: python3 ab_weights.py MESH_V_F.npz JOINTS.json OUT.npz OFFSET_X_CM OFFSET_Y_CM
#   MESH_V_F.npz: V (Blender metres, as imported), F (triangles); JOINTS.json from ab_joints.py (fig0 review frame);
#   OFFSET: fig0 -> Blender-source translation in cm (source = fig0 + offset).
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
mp, jp, out, ox, oy = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
# optional 6th arg PELVIC_RING_OFFSET_CM (checkpoint 2): also seed the trunk with the pelvic-ring loop at crotch + offset, so the groin
# and gluteal fold stay with the rigid pelvis and the thigh group starts at the crotch plane
ring = float(sys.argv[6]) if len(sys.argv) > 6 else None
d = np.load(mp); V = d['V'].astype(np.float64) * 100; F = d['F'].astype(np.int64)
J = json.load(open(jp)); off = np.array([ox, oy, 0.0]); H = J['H']
j = {k: np.array(v) + off for k, v in J.items() if isinstance(v, list) and len(v) == 3}
mid = np.array([J['midline_x'] + ox, J['midline_y'] + oy])
key, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True); inv = inv.ravel(); W = key; Fw = inv[F]
E = np.concatenate([Fw[:, [0, 1]], Fw[:, [1, 2]], Fw[:, [2, 0]]]); E = np.unique(np.sort(E, 1), axis=0); E = E[E[:, 0] != E[:, 1]]
L = np.linalg.norm(W[E[:, 0]] - W[E[:, 1]], axis=1); n = len(W)
G = sp.coo_matrix((np.r_[L, L], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
mesh = trimesh.Trimesh(W, Fw, process=False); kd = cKDTree(W)
def seed(z, xy, maxd=12.0):
    s = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1]); best = None
    for e in s.discrete:
        c = e[:, :2].mean(0); dd = np.linalg.norm(c - xy)
        if best is None or dd < best[0]: best = (dd, e)
    assert best is not None and best[0] < maxd, ('no seed loop', z, xy, None if best is None else best[0])
    return np.unique(kd.query(best[1])[1])
S = {}
S['trunk'] = np.concatenate([seed(f * H, mid, 15) for f in (0.55, 0.60, 0.64, 0.89)] +
                            [seed(z, np.array(xy) + off[:2], 8) for z, xy in ((0.40 * H, (-4.5, 37.7)), (0.30 * H, (-2.85, 63.1)), (0.34 * H, (-7.9, 103.7)))])
if ring is not None: S['trunk'] = np.concatenate([S['trunk'], seed(J['crotch_z'] + ring, mid, 15)])
for s in 'LR':
    e, w, k, a = j['elbow_' + s], j['wrist_' + s], j['knee_' + s], j['ankle_' + s]
    S['upperarm_' + s] = seed(e[2] + 4, e[:2], 8)
    S['forearm_' + s] = np.concatenate([seed(e[2] - 4, e[:2], 8), seed(w[2] + 4, w[:2], 8)])
    S['hand_' + s] = seed(w[2] - 4, w[:2], 8)
    hp = j['hip_' + s]; th = k + (0.40 * H - k[2]) / (hp[2] - k[2]) * (hp - k)
    S['thigh_' + s] = np.concatenate([seed(k[2] + 5, k[:2], 8), seed(0.40 * H, th[:2], 8)])
    S['shin_' + s] = np.concatenate([seed(k[2] - 5, k[:2], 8), seed(a[2] + 5, a[:2], 8)])
    S['foot_' + s] = seed(3.0, a[:2] + np.array([0, -8.0]), 10)
names = list(S); D = np.stack([dijkstra(G, indices=S[nm], min_only=True) for nm in names], 1)   # n x groups, cm
lab = np.argmin(D, 1); T = 1.5
srt = np.sort(D, 1); idx = np.argsort(D, 1)[:, :2]
w2 = np.exp(-(srt[:, :2] - srt[:, :1]) / T); w2 /= w2.sum(1, keepdims=True)
Wt = np.zeros((n, len(names)), np.float32); Wt[np.arange(n), idx[:, 0]] = w2[:, 0]; Wt[np.arange(n), idx[:, 1]] += w2[:, 1]
np.savez(out, names=np.array(names), weights_welded=Wt, welded_index=inv.astype(np.int32), label_welded=lab.astype(np.int16),
         seeds=np.array([len(S[k]) for k in names]))
print(json.dumps({nm: dict(seed_vertices=int(len(S[nm])), welded_vertices_labelled=int((lab == i).sum())) for i, nm in enumerate(names)}, indent=1))
