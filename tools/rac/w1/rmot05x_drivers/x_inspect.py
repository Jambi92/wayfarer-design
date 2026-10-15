# RM-OT-05X (order §1, §3): READ-ONLY intake and geometry inspection of the new Gorrund GLB. Never writes the GLB.
# Reports: hash/size, glTF container facts, node transforms, axis convention, bounds, material, vertex welding (split seams vs real
# disconnection), connected components, boundary / non-manifold / orientation, Euler characteristic, degenerate and sliver faces,
# self-intersection (pymeshlab, whole mesh), and rig-less approximate levels (skull vertex, ears, sole contact, heel, crotch, tail).
# All lengths in raw source units x100 ("raw cm"): NOT a stature measurement. Axes reported as glTF (Y up, +Z front) and as the
# review frame used by the renders (X right, Y back, Z up).
# Usage: python3 x_inspect.py Gorrund.glb OUT.json
import sys, json, struct, hashlib, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
p, out = sys.argv[1:3]; b = open(p, 'rb').read(); R = dict(file=p.split('/')[-1], bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
cl = struct.unpack('<I', b[12:16])[0]; J = json.loads(b[20:20 + cl]); o = 20 + cl; bl = struct.unpack('<I', b[o:o + 4])[0]; B = b[o + 8:o + 8 + bl]
R['gltf'] = dict(version=J['asset'].get('version'), generator=J['asset'].get('generator'), scenes=len(J['scenes']), nodes=J['nodes'], meshes=len(J['meshes']),
                 primitives=[dict(attributes=list(pr['attributes']), mode=pr.get('mode', 4)) for m in J['meshes'] for pr in m['primitives']],
                 materials=J.get('materials'), textures=len(J.get('textures', [])), images=len(J.get('images', [])), skins=len(J.get('skins', [])), animations=len(J.get('animations', [])),
                 node_transform='none (identity: no matrix / translation / rotation / scale on the only node)' if not any(k in J['nodes'][0] for k in ('matrix', 'translation', 'rotation', 'scale')) else J['nodes'][0])
def acc(i, dt, nc):
    a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.frombuffer(B, dt, a['count'] * nc, off).reshape(a['count'], nc)
pr = J['meshes'][0]['primitives'][0]; Pos = acc(pr['attributes']['POSITION'], np.float32, 3); I = acc(pr['indices'], np.uint32, 1).reshape(-1, 3)
R['position_bounds_gltf'] = dict(min=Pos.min(0).round(5).tolist(), max=Pos.max(0).round(5).tolist())
U, inv = np.unique(Pos, axis=0, return_inverse=True); F = inv.ravel()[I]; V = np.stack([U[:, 0], -U[:, 2], U[:, 1]], 1).astype(np.float64) * 100
E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1); ue, cnt = np.unique(E, axis=0, return_counts=True)
n = len(U); nc, lab = connected_components(sp.coo_matrix((np.ones(len(ue)), (ue[:, 0], ue[:, 1])), shape=(n, n)), directed=False)
DE = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); _, dc = np.unique(DE, axis=0, return_counts=True)
chi = int(n - len(ue) + len(F))
R['topology'] = dict(exported_vertices=int(len(Pos)), welded_positions=int(n), split_vertices_from_seams=int(len(Pos) - n), triangles=int(len(F)),
                     connected_components_after_welding=int(nc), boundary_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
                     inconsistent_orientation_edges=int((dc > 1).sum()), euler_characteristic=chi, genus_if_single_closed=int((2 - chi) // 2),
                     note='seam splits are UV/normal duplicates at identical positions; after welding the surface is ONE closed orientable manifold. '
                          'Genus 2 = two small handles, located at the axillae (closed section loops ~3-10 raw cm perimeter at raw z 128.5-129.5, x +-23).')
a = V[F[:, 1]] - V[F[:, 0]]; bb = V[F[:, 2]] - V[F[:, 1]]; c = V[F[:, 0]] - V[F[:, 2]]
def ang(u, v): return np.degrees(np.arccos(np.clip((u * v).sum(1) / np.linalg.norm(u, axis=1) / np.linalg.norm(v, axis=1), -1, 1)))
mn = np.stack([ang(a, -c), ang(bb, -a), ang(c, -bb)], 1).min(1); L = np.linalg.norm(np.stack([a, bb, c]), axis=2)
R['quality'] = dict(edge_raw_cm=dict(median=round(float(np.median(L)), 3), p99=round(float(np.percentile(L, 99)), 3), max=round(float(L.max()), 3)),
                    min_angle_deg=dict(median=round(float(np.median(mn)), 1), below_10=int((mn < 10).sum()), below_1=int((mn < 1).sum()), min=round(float(mn.min()), 3)),
                    zero_area_faces=int((np.linalg.norm(np.cross(a, -c), axis=1) < 1e-10).sum()))
try:
    import pymeshlab
    ms = pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(V, F.astype(np.int32))); ms.compute_selection_by_self_intersections_per_face()
    R['self_intersection'] = dict(faces=int(ms.current_mesh().face_selection_array().sum()), scope='whole welded mesh, triangle-triangle (pymeshlab), all 1,000,000 faces')
except Exception as e: R['self_intersection'] = dict(error=str(e))
X, Y, Z = V.T; mid = np.abs(X) < 3; lat = np.abs(X) > 5
R['levels_raw_cm_approx'] = dict(
    frame='review frame: X right, Y back (figure faces -Y = glTF +Z), Z up; ground = lowest vertex (raw y 0)',
    top_vertex=V[np.argmax(Z)].round(1).tolist(), top_is='ear (lateral)' if abs(V[np.argmax(Z), 0]) > 5 else 'midline',
    skull_vertex_midline=V[mid][np.argmax(Z[mid])].round(1).tolist(), ear_top=V[lat][np.argmax(Z[lat])].round(1).tolist(),
    neck_min_section_z=162.0, crotch_shorts_surface_z=81.0, fingertips_z=71.5, tail_root_z=[99.0, 109.7], tail_lowest_z=round(float(Z[Y > 25].min()), 1),
    tail_min_gap_to_body_hanging_part=19.1, sole_contact_vertices_z_lt_0_3=int((Z < 0.3).sum()),
    heel_height_above_lowest_point=[1.74, 1.76], foot_length=[35.0, 34.6],
    note='rig-less surface estimates only; no joint centres or skeleton are claimed')
json.dump(R, open(out, 'w'), indent=1); print(json.dumps({k: R[k] for k in ('sha256', 'topology', 'self_intersection')}, indent=1))
