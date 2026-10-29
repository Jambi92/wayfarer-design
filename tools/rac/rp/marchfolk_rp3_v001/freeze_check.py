# freeze_check.py BLEND CAND.npz LANDMARKS.json OUT.json : read-back verification of an accepted production .blend (order 85b7c1c §6).
# Opens the file in Blender WITHOUT saving it, recomputes sha256 / geometry hash (float32 co + int32 loop vertex_index) / face topology hash
# (int32 loop vertex_index), counts and integrity (components, boundary / non-manifold edges and vertices, degenerate faces, quads %, outward normals),
# checks the UV layer, and proves the blend geometry equals the candidate map output (CAND V, analysis cm -> production m frame).
import sys, os, json, hashlib, numpy as np
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BL, CZ, LMJ, OUT = a[:4]
sha = hashlib.sha256(open(BL, 'rb').read()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=BL)
obs = [o for o in bpy.data.objects if o.type == 'MESH']; ob = obs[0]; me = ob.data
nV = len(me.vertices); nF = len(me.polygons)
co = np.empty(nV * 3, np.float32); me.vertices.foreach_get('co', co); li = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', li)
ls = np.empty(nF, np.int32); me.polygons.foreach_get('loop_total', ls)
gh = hashlib.sha256(co.tobytes() + li.tobytes()).hexdigest(); fh = hashlib.sha256(li.tobytes()).hexdigest()
V = co.reshape(-1, 3).astype(float); Q = li.reshape(-1, 4) if (ls == 4).all() else None
R = dict(file=os.path.basename(BL), sha256=sha, geometry_hash=gh, face_topology_hash=fh, verts=nV, faces=nF, quads_pct=float(100 * (ls == 4).mean()), mesh_objects=len(obs),
         uv_layers=[u.name for u in me.uv_layers], properties={k: str(ob[k]) for k in ob.keys() if k.startswith('RAC')})
E = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); uE, cnt = np.unique(E, axis=0, return_counts=True)
R['boundary_edges'] = int((cnt == 1).sum()); R['nonmanifold_edges'] = int((cnt > 2).sum())
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
A = sp.csr_matrix((np.ones(2 * len(uE)), (np.r_[uE[:, 0], uE[:, 1]], np.r_[uE[:, 1], uE[:, 0]])), shape=(nV, nV)); R['components'] = int(connected_components(A, directed=False)[0])
# non-manifold vertices: face fan of each vertex must be edge-connected
from collections import defaultdict
vf = defaultdict(list)
for fi, q in enumerate(Q):
    for v in q: vf[int(v)].append(fi)
nmv = 0
for v, fl in vf.items():
    if len(fl) < 2: nmv += 1; continue
    es = {fi: {tuple(sorted((int(Q[fi][k]), int(Q[fi][(k + 1) % 4])))) for k in range(4) if v in (Q[fi][k], Q[fi][(k + 1) % 4])} for fi in fl}
    seen = {fl[0]}; st = [fl[0]]
    while st:
        f_ = st.pop()
        for g in fl:
            if g not in seen and es[f_] & es[g]: seen.add(g); st.append(g)
    nmv += len(seen) != len(fl)
R['nonmanifold_vertices'] = int(nmv) + int(nV - len(vf))
fn = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]) * 0.5; R['degenerate_faces'] = int((np.linalg.norm(fn, axis=1) < 1e-10).sum())
TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; vol = float(np.einsum('ij,ij->i', V[TRI[:, 0]], np.cross(V[TRI[:, 1]], V[TRI[:, 2]])).sum() / 6); R['signed_volume_m3'] = vol; R['normals_outward'] = bool(vol > 0)
# equality with the candidate map output
cz = np.load(CZ); LM = json.load(open(LMJ)); Vc = cz['V'].astype(float) + np.array(LM['frame']['origin_translation_cm']); Vb = np.c_[Vc[:, 0], -Vc[:, 1], Vc[:, 2]] / 100.0
R['max_abs_diff_vs_candidate_m'] = float(np.abs(Vb - V).max()); R['faces_equal_candidate'] = bool(np.array_equal(Q, cz['Q'].astype(np.int32)))
if os.environ.get('RB_DUMP'): np.savez(os.environ['RB_DUMP'], V_m=V, Q=Q)          # optional: read-back geometry (production frame, m) for recomputation
json.dump(R, open(OUT, 'w'), indent=1); print('FREEZECHECK', json.dumps({k: v for k, v in R.items() if k != 'properties'}))
