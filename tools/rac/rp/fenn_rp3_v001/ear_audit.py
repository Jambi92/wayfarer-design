# ear_audit.py BRANCH.npz FAM.npz OUT.json  (bpy python; mathutils BVH)
# Order bdcd6a6 §9 / §12 / §14 audits of one Fenn ear-branch realization against its CF2 family realization (v005 topology):
#   integrity  : quads, components, boundary / non-manifold edges and vertices, degenerate faces, winding consistency, outward orientation,
#                self-intersections (all; and pairs touching the branch), coincident vertices
#   T-4        : branch quad interior angles (45-135 deg), aspect (longest / shortest side) > 4 / > 6 / > 10, poles (valence != 4) by part
#   density    : branch mean edge / stature (contract ears zone <= 0.25 %), face counts vs the v005 ear zone
#   root       : outside-branch vertices identical to the CF2 family realization; root-loop valence; dihedral across the root loop;
#                deviation of the cuff (new skull skin inside the root) from the hidden-ear CF2 skull (v005 ear zone harmonically collapsed)
#   clearance  : ear sheet (front / back / rim) to the head outside the branch; minimum and the nearest region
import sys, json, numpy as np
import bpy  # noqa: F401
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); fz = np.load(a[1]); OUT = a[2]
V = z['V'].astype(float); Q = np.asarray(z['Q']); part = z['part']; side = z['side']; v2b = z['v005_to_branch']; V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q'])
nV = len(V); stature = V[:, 2].max() - V[:, 2].min(); R = dict(verts=int(nV), faces=int(len(Q)), stature_cm=float(stature))
br_v = part != 'v005'; br_f = br_v[Q].any(1)
# ---------------- integrity
E = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); Eu, cnt = np.unique(E, axis=0, return_counts=True)
R['boundary_edges'] = int((cnt == 1).sum()); R['nonmanifold_edges'] = int((cnt > 2).sum())
import scipy.sparse as sp
A = sp.coo_matrix((np.ones(len(Eu)), (Eu[:, 0], Eu[:, 1])), shape=(nV, nV)); ncomp, lab = sp.csgraph.connected_components(A, directed=False); R['components'] = int(ncomp)
# non-manifold vertices: the faces around a vertex must form one fan
vf = [[] for _ in range(nV)]
for fi, q in enumerate(Q):
    for v in q: vf[v].append(fi)
nmv = 0
for v in np.nonzero(br_v | np.isin(np.arange(nV), Q[br_f].ravel()))[0]:
    fs = vf[v]; adj = {f: set() for f in fs}
    for f in fs:
        q = list(Q[f]); k = q.index(v); nb = {q[(k + 1) % 4], q[(k - 1) % 4]}
        for g in fs:
            if g != f:
                qg = list(Q[g]); kg = qg.index(v)
                if nb & {qg[(kg + 1) % 4], qg[(kg - 1) % 4]}: adj[f].add(g)
    seen = {fs[0]}; st = [fs[0]]
    while st:
        f = st.pop()
        for g in adj[f]:
            if g not in seen: seen.add(g); st.append(g)
    nmv += len(seen) != len(fs)
R['nonmanifold_vertices_branch_region'] = int(nmv)
de = {}
for fi, q in enumerate(Q):
    for k in range(4): de[(q[k], q[(k + 1) % 4])] = de.get((q[k], q[(k + 1) % 4]), 0) + 1
R['winding_consistent'] = bool(max(de.values()) == 1)
def area(X, q): return 0.5 * np.linalg.norm(np.cross(X[q[:, 2]] - X[q[:, 0]], X[q[:, 3]] - X[q[:, 1]]), axis=1)
ar = area(V, Q); R['degenerate_faces'] = int((ar < 1e-6).sum()); R['degenerate_faces_branch'] = int((ar[br_f] < 1e-6).sum())
tri = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; vol = np.einsum('ij,ij->i', V[tri[:, 0]], np.cross(V[tri[:, 1]], V[tri[:, 2]])).sum() / 6
R['signed_volume_cm3'] = float(vol); R['normals_outward'] = bool(vol < 0)          # analysis frame left-handed (audit.py convention)
d0, _ = cKDTree(V).query(V, k=2); R['coincident_vertex_pairs'] = int((d0[:, 1] < 1e-5).sum() // 2)
# self-intersection
qid = np.r_[np.arange(len(Q)), np.arange(len(Q))]
def selfx(X):
    bvh = BVHTree.FromPolygons(X.tolist(), tri.tolist(), all_triangles=True, epsilon=0.0); bad = set()
    for i, j in bvh.overlap(bvh):
        fi, fj = qid[i], qid[j]
        if fi != fj and not (set(Q[fi]) & set(Q[fj])): bad.add((min(fi, fj), max(fi, fj)))
    return bad
SX = selfx(V); sxb = [p for p in SX if br_f[p[0]] or br_f[p[1]]]
R['self_intersection_pairs_total'] = len(SX); R['self_intersection_pairs_touching_branch'] = len(sxb)
# v005 baseline self-intersections on the CF2 family realization (for reference)
tri0 = np.r_[Q0[:, [0, 1, 2]], Q0[:, [0, 2, 3]]]; qid0 = np.r_[np.arange(len(Q0)), np.arange(len(Q0))]
bvh0 = BVHTree.FromPolygons(V0.tolist(), tri0.tolist(), all_triangles=True, epsilon=0.0); s0 = set()
for i, j in bvh0.overlap(bvh0):
    fi, fj = qid0[i], qid0[j]
    if fi != fj and not (set(Q0[fi]) & set(Q0[fj])): s0.add((min(fi, fj), max(fi, fj)))
R['self_intersection_pairs_cf2_family_v005'] = len(s0)
# ---------------- T-4 / aspect / poles on branch faces
def quad_metrics(X, q):
    P = X[q]; ang = []; L = np.linalg.norm(P - np.roll(P, -1, 1), axis=2)
    for k in range(4):
        u = P[:, (k - 1) % 4] - P[:, k]; w = P[:, (k + 1) % 4] - P[:, k]
        c = np.einsum('ij,ij->i', u, w) / (np.linalg.norm(u, axis=1) * np.linalg.norm(w, axis=1) + 1e-12); ang.append(np.degrees(np.arccos(np.clip(c, -1, 1))))
    return np.stack(ang, 1), L.max(1) / np.maximum(L.min(1), 1e-9), L
ang, asp, Ls = quad_metrics(V, Q[br_f]); bad_ang = ((ang < 45) | (ang > 135)).any(1)
def _fp(q):
    pq = set(part[q])
    for k in ('cuff', 'rim', 'back', 'front', 'transition'):
        if k in pq: return k
    return 'cuff'
fpart = np.array([_fp(q) for q in Q[br_f]])
def by(mask): return {pp: int(((fpart == pp) & mask).sum()) for pp in ('front', 'back', 'rim', 'cuff', 'transition')}
R['T4'] = dict(branch_faces=int(br_f.sum()), angle_violations=int(bad_ang.sum()), angle_violations_by_part=by(bad_ang),
               aspect_gt4=int((asp > 4).sum()), aspect_gt6=int((asp > 6).sum()), aspect_gt10=int((asp > 10).sum()), aspect_max=float(asp.max()),
               aspect_p95=float(np.percentile(asp, 95)), aspect_gt6_by_part=by(asp > 6), min_angle=float(ang.min()), max_angle=float(ang.max()),
               angle_p01_p99=[float(np.percentile(ang, 1)), float(np.percentile(ang, 99))], union_violations=int((bad_ang | (asp > 4)).sum()))
val = np.zeros(nV, int); np.add.at(val, Eu.ravel(), 1)
pv = np.nonzero(br_v & (val != 4))[0]; R['poles_branch'] = {pp: {str(k): int(((part[pv] == pp) & (val[pv] == k)).sum()) for k in sorted(set(val[pv]))} for pp in ('front', 'back', 'rim', 'cuff')}
R['poles_branch_total'] = int(len(pv))
R['_per_face'] = None
# ---------------- density
eb = Eu[br_v[Eu].any(1)]; el = np.linalg.norm(V[eb[:, 0]] - V[eb[:, 1]], axis=1)
R['density'] = dict(branch_mean_edge_cm=float(el.mean()), branch_mean_edge_pct_stature=float(100 * el.mean() / stature), limit_pct=0.25,
                    pass_mean=bool(100 * el.mean() / stature <= 0.25), p95_pct=float(100 * np.percentile(el, 95) / stature), max_edge_cm=float(el.max()),
                    branch_faces_per_side=int(br_f.sum() // 2), v005_ear_zone_faces_per_side=1206, ratio=float(br_f.sum() / 2 / 1206))
# ---------------- root continuity / unchanged outside
keep = np.nonzero(v2b >= 0)[0]; tr = part[v2b[keep]] == 'transition'; kk = keep[~tr]
R['outside_branch_max_abs_delta_cm'] = float(np.abs(V[v2b[kk]] - V0[kk]).max()); R['outside_branch_byte_identical'] = bool(np.array_equal(V[v2b[kk]], V0[kk]))
dtr = np.linalg.norm(V[v2b[keep[tr]]] - V0[keep[tr]], axis=1) if tr.any() else np.zeros(1)
R['transition_ring'] = dict(vertices=int(tr.sum()), displacement_mean_cm=float(dtr.mean()), displacement_p95_cm=float(np.percentile(dtr, 95)), displacement_max_cm=float(dtr.max()))
rec = json.load(open(a[0].replace('.npz', '.json'))); roots = {s: v2b[np.array(rec['sides'][s]['root_loop_v005'])] for s in ('l', 'r')}
R['root_valence'] = {s: {str(k): int((val[roots[s]] == k).sum()) for k in sorted(set(val[roots[s]]))} for s in roots}
def fnorm(X, q): n = np.cross(X[q[:, 2]] - X[q[:, 0]], X[q[:, 3]] - X[q[:, 1]]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
NF = fnorm(V, Q); eface = {}
for fi, q in enumerate(Q):
    for k in range(4): eface.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi)
dih = {}
for s, L in roots.items():
    ds = []
    for k in range(len(L)):
        e = (min(L[k], L[(k + 1) % len(L)]), max(L[k], L[(k + 1) % len(L)])); f1, f2 = eface[e]
        ds.append(float(np.degrees(np.arccos(np.clip(NF[f1] @ NF[f2], -1, 1)))))
    dih[s] = dict(max_deg=max(ds), mean_deg=float(np.mean(ds)))
# v005 reference: the same root edges on the CF2 family mesh
NF0 = fnorm(V0, Q0); ef0 = {}
for fi, q in enumerate(Q0):
    for k in range(4): ef0.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi)
for s in ('l', 'r'):
    L0 = np.array(rec['sides'][s]['root_loop_v005']); ds = []
    for k in range(len(L0)):
        f1, f2 = ef0[(min(L0[k], L0[(k + 1) % len(L0)]), max(L0[k], L0[(k + 1) % len(L0)]))]; ds.append(float(np.degrees(np.arccos(np.clip(NF0[f1] @ NF0[f2], -1, 1)))))
    dih[s]['v005_max_deg'] = max(ds); dih[s]['v005_mean_deg'] = float(np.mean(ds))
R['root_dihedral'] = dih
# hidden-ear skull: collapse the v005 ear-zone interior of the CF2 family mesh harmonically onto its root loop
we_zone = np.zeros(len(V0), bool); we_zone[z['removed_v005']] = True
Ei = np.unique(np.sort(np.concatenate([Q0[:, [0, 1]], Q0[:, [1, 2]], Q0[:, [2, 3]], Q0[:, [3, 0]]]), 1), axis=0)
A0 = sp.coo_matrix((np.ones(2 * len(Ei)), (np.r_[Ei[:, 0], Ei[:, 1]], np.r_[Ei[:, 1], Ei[:, 0]])), shape=(len(V0), len(V0))).tocsr(); deg = np.asarray(A0.sum(1)).ravel()
X = V0.copy()
for _ in range(600): X[we_zone] = (A0 @ X)[we_zone] / deg[we_zone, None]
hid_f = Q0[we_zone[Q0].any(1)]
# dense samples of the hidden-ear skull patch
g = np.linspace(0, 1, 6); S = []
for q in hid_f:
    P = X[q]
    for uu in g:
        for vv in g: S.append((1 - uu) * (1 - vv) * P[0] + uu * (1 - vv) * P[1] + uu * vv * P[2] + (1 - uu) * vv * P[3])
S = np.array(S); tS = cKDTree(S)
cuff = np.nonzero(np.isin(part, ['cuff', 'transition']))[0]; dc, _ = tS.query(V[cuff])
ring_of = np.zeros(nV, int) - 1
R['root_deviation'] = dict(note='distance of the new skull skin inside the root (cuff vertices) from the hidden-ear CF2 skull (v005 ear zone harmonically collapsed); root loop itself is unchanged (0)',
                           cuff_mean_cm=float(dc.mean()), cuff_p95_cm=float(np.percentile(dc, 95)), cuff_max_cm=float(dc.max()))
np.save(OUT.replace('.json', '_cuffdev.npy'), np.c_[cuff, dc])
# ---------------- clearance of the free ear to the head outside the branch
ear = np.nonzero(np.isin(part, ['front', 'back', 'rim']))[0]; head = np.nonzero((part == 'v005') & (V[:, 2] > V[:, 2].max() - 30))[0]
tH = cKDTree(V[head]); dh, ih = tH.query(V[ear])
R['ear_to_head_clearance'] = dict(min_cm=float(dh.min()), p01_cm=float(np.percentile(dh, 1)), n_below_0p2cm=int((dh < 0.2).sum()))
R['self_intersection_pairs_list_branch'] = [list(map(int, p)) for p in sorted(sxb)]
json.dump(R, open(OUT, 'w'), indent=1)
np.savez_compressed(OUT.replace('.json', '_perface.npz'), faces=np.nonzero(br_f)[0], ang_bad=bad_ang, asp=asp, minang=ang.min(1), maxang=ang.max(1))
print(json.dumps({k: v for k, v in R.items() if k not in ('self_intersection_pairs_list_branch',)}, indent=0)[:3000])
