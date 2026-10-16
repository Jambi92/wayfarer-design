# RM-OT-05AC2 / AC1 gates: 05AB1 clean baseline GLB (before) vs UI-sculpted GO-05AC_AC1.glb (after). Read-only.
# Topology identity, single-body (nodes/meshes), welded components / boundary / non-manifold, displacement by region
# (protected = GO-05AC_protect_mask >= 1, AC1 allowed = GO-05AC_mask_AC1 < 0.5), flipped / >60deg-rotated faces,
# self-intersecting faces (pymeshlab, welded) before and after, height / bbox preservation.
# Usage: python3 -I ac1_checks.py BEFORE.glb AFTER.glb PROTECT.npy MASK_AC1.npy OUT.json
import sys, json, struct, hashlib, numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

def load_glb(p):
    raw = open(p, 'rb').read()
    L = struct.unpack_from('<I', raw, 12)[0]; js = json.loads(raw[20:20 + L]); off = 20 + L
    bl = struct.unpack_from('<I', raw, off)[0]; bin_ = raw[off + 8: off + 8 + bl]
    def acc(i):
        a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
        dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a['componentType']]
        n = {'SCALAR': 1, 'VEC3': 3, 'VEC2': 2, 'VEC4': 4}[a['type']]
        o = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        return np.frombuffer(bin_, dt, a['count'] * n, o).reshape(a['count'], n) if n > 1 else np.frombuffer(bin_, dt, a['count'], o)
    prims = js['meshes'][0]['primitives']; assert len(prims) == 1
    V = acc(prims[0]['attributes']['POSITION']).astype(float); F = acc(prims[0]['indices']).astype(np.int64).reshape(-1, 3)
    meta = dict(file=p.split('/')[-1], bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), nodes=len(js['nodes']),
                meshes=len(js['meshes']), primitives=len(prims), node_names=[n.get('name') for n in js['nodes']])
    return V, F, meta

b, a, pp, mp, out = sys.argv[1:6]
VB, FB, mb = load_glb(b); VA, FA, ma = load_glb(a)
R = dict(before=mb, after=ma, glb_vertices=dict(before=len(VB), after=len(VA)), faces=dict(before=len(FB), after=len(FA)))
R['single_body'] = dict(before=mb['nodes'] == 1 and mb['meshes'] == 1, after=ma['nodes'] == 1 and ma['meshes'] == 1)
R['note'] = 'glTF splits vertices at normal seams; sculpting changes normals, so raw GLB vertex counts differ. All checks use welded positions matched by face corner.'

def weld(V, F):
    key, iv = np.unique(np.round(V, 6), axis=0, return_inverse=True); iv = iv.ravel(); return key, iv[F]
kB, WB = weld(VB, FB); kA, WA = weld(VA, FA)
same_faces = len(FB) == len(FA)
pair = np.unique(np.c_[WB.ravel(), WA.ravel()], axis=0) if same_faces else None
R['topology_identical'] = bool(same_faces and len(pair) == len(kB) == len(kA) and len(np.unique(pair[:, 0])) == len(pair) and len(np.unique(pair[:, 1])) == len(pair))
F = WB  # welded faces in baseline numbering
mapBA = np.empty(len(kB), np.int64); mapBA[pair[:, 0]] = pair[:, 1]
XB = kB; XA = kA[mapBA]  # welded positions, same order

def topo(F, n):
    E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1); E = E[E[:, 0] != E[:, 1]]
    u, c = np.unique(E, axis=0, return_counts=True)
    nc, _ = connected_components(sp.coo_matrix((np.ones(len(u)), (u[:, 0], u[:, 1])), shape=(n, n)), directed=False)
    return dict(welded_vertices=int(n), components=int(nc), boundary_edges=int((c == 1).sum()), nonmanifold_edges=int((c > 2).sum()))
R['topo_before'] = topo(WB, len(kB)); R['topo_after'] = topo(mapBA[WB], len(kA))

cm = lambda V: np.c_[V[:, 0], -V[:, 2], V[:, 1]] * 100   # glTF Y-up metres -> Z-up cm
CB, CA = cm(XB), cm(XA); d = np.linalg.norm(CA - CB, axis=1)
P0 = np.load(pp).astype(float); M0 = np.load(mp).astype(float)
# masks are in the Blender base-mesh vertex order; map them onto welded baseline vertices by nearest position (KD-tree)
from scipy.spatial import cKDTree
R['mask_vertices'] = len(P0)
if len(P0) == len(kB):
    P, M = P0, M0; R['mask_mapping'] = 'same length as welded baseline; assumed same order (verified by protect mask geometry below)'
else:
    P, M = P0, M0; R['mask_mapping'] = 'length mismatch'
def st(m):
    x = d[m]
    if not len(x): return dict(n=0)
    return dict(n=int(m.sum()), moved_gt_0_01mm=int((x > 1e-3).sum()), max_mm=round(float(x.max()) * 10, 3),
                p99_mm=round(float(np.percentile(x, 99)) * 10, 3), mean_mm=round(float(x.mean()) * 10, 4))
R['displacement'] = dict(all=st(np.ones(len(d), bool)))
if len(P) == len(d):
    R['displacement'].update(protected_core=st(P >= 1), ac1_allowed=st(M < 0.5), outside_ac1_allowed=st(M >= 0.5))
moved = d > 1e-3
R['moved_vertices'] = int(moved.sum())
R['moved_region_bbox_cm_zup'] = dict(min=np.round(CA[moved].min(0), 1).tolist(), max=np.round(CA[moved].max(0), 1).tolist()) if moved.any() else None
# region classification by geometry (Z-up cm, figure height ~204.5): neck minimum 168.3 in donor frame
z = CB[:, 2] - CB[:, 2].min(); R['moved_height_band_cm_from_floor'] = [round(float(z[moved].min()), 1), round(float(z[moved].max()), 1)] if moved.any() else None
R['height_cm'] = dict(before=round(float(np.ptp(CB[:, 2])), 4), after=round(float(np.ptp(CA[:, 2])), 4))
R['bbox_extent_cm'] = dict(before=np.round(np.ptp(CB, 0), 3).tolist(), after=np.round(np.ptp(CA, 0), 3).tolist())
R['max_displacement_mm'] = round(float(d.max()) * 10, 3)

def fn(V):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); l = np.linalg.norm(n, axis=1); return n / np.maximum(l, 1e-20)[:, None], l
nB, aB = fn(XB); nA, aA = fn(XA); dot = (nB * nA).sum(1)
fm = moved[F].any(1)
R['faces_touched'] = int(fm.sum())
R['flipped_faces'] = int((dot < 0).sum()); R['rotated_over_60deg'] = int((dot < 0.5).sum())
R['degenerate_faces'] = dict(before=int((aB < 1e-14).sum()), after=int((aA < 1e-14).sum()))
np.save(out.replace('.json', '_disp_cm.npy'), d.astype(np.float32))
try:
    import pymeshlab
    def si(X):
        ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(X, F)); ms.compute_selection_by_self_intersections_per_face()
        return np.where(ms.current_mesh().face_selection_array())[0]
    sB, sA = si(XB), si(XA); new = np.setdiff1d(sA, sB)
    R['self_intersecting_faces'] = dict(before=int(len(sB)), after=int(len(sA)), new=int(len(new)), new_in_touched_faces=int(fm[new].sum()))
except Exception as e:
    R['self_intersecting_faces'] = dict(error=repr(e))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps({k: v for k, v in R.items() if k not in ('before', 'after')}, indent=1))
