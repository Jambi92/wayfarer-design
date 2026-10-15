# RM-OT-05Z §7: mechanical single-body intake gate for any new Gorrund source GLB. READ-ONLY.
# Checks, in order:
#   1. exact SHA-256 and size;
#   2. connected components after welding seam duplicates (exact-position weld);
#   3. duplicate bodies: more than one component whose height is >= 50 % of the tallest (front/side/back library) -> FAIL;
#   4. small extra pieces (< 50 % of the tallest) are LISTED for review, never silently dropped;
#   5. hidden merged view shells: closed shells nested inside another (a component whose bbox lies inside a larger one's bbox)
#      and open boundary / non-manifold edges are reported (an open or non-manifold mesh is a FLAG for the anatomy review).
# A PASS here only permits the whole-source anatomy review; it accepts nothing.
# Usage: python3 z_single_body_gate.py SOURCE.glb OUT.json   (exit 0 PASS, 3 FAIL)
import sys, json, struct, hashlib, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
p, out = sys.argv[1:3]; b = open(p, 'rb').read()
R = dict(file=p.split('/')[-1], bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
assert b[:4] == b'glTF', 'not a GLB'
cl = struct.unpack('<I', b[12:16])[0]; J = json.loads(b[20:20 + cl]); o = 20 + cl; bl = struct.unpack('<I', b[o:o + 4])[0]; B = b[o + 8:o + 8 + bl]
def acc(i, dt, nc):
    a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.frombuffer(B, dt, a['count'] * nc, off).reshape(a['count'], nc)
Ps, Fs, base = [], [], 0
for mi, m in enumerate(J['meshes']):
    for pr in m['primitives']:
        P = acc(pr['attributes']['POSITION'], np.float32, 3); it = J['accessors'][pr['indices']]['componentType']
        I = acc(pr['indices'], {5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[it], 1).reshape(-1, 3).astype(np.int64)
        Ps.append(P); Fs.append(I + base); base += len(P)
R['meshes'] = len(J['meshes']); R['nodes'] = len(J['nodes']); R['node_transforms'] = [any(k in n for k in ('matrix', 'translation', 'rotation', 'scale')) for n in J['nodes']]
P = np.concatenate(Ps); I = np.concatenate(Fs); U, inv = np.unique(P, axis=0, return_inverse=True); F = inv.ravel()[I]; n = len(U)
E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1); ue, cnt = np.unique(E, axis=0, return_counts=True)
nc, lab = connected_components(sp.coo_matrix((np.ones(len(ue)), (ue[:, 0], ue[:, 1])), shape=(n, n)), directed=False)
fl = lab[F[:, 0]]; comps = []
for k in np.argsort(-np.bincount(fl, minlength=nc)):
    m = fl == k
    if not m.any(): continue
    vv = U[np.unique(F[m])]; comps.append(dict(faces=int(m.sum()), bbox_min=vv.min(0).round(4).tolist(), bbox_max=vv.max(0).round(4).tolist(), height=float(vv[:, 1].max() - vv[:, 1].min())))
Hmax = max(c['height'] for c in comps); big = [c for c in comps if c['height'] >= 0.5 * Hmax]; small = [c for c in comps if c['height'] < 0.5 * Hmax]
def inside(a, c): return all(a['bbox_min'][i] >= c['bbox_min'][i] for i in range(3)) and all(a['bbox_max'][i] <= c['bbox_max'][i] for i in range(3))
nested = [i for i, a in enumerate(comps) for j, c in enumerate(comps) if i != j and c['faces'] > a['faces'] and inside(a, c)]
R.update(exported_vertices=int(len(P)), welded_positions=int(n), triangles=int(len(F)), components=len(comps), body_sized_components=len(big),
         small_pieces=[dict(faces=c['faces'], height=round(c['height'], 4)) for c in small][:50], nested_components=nested,
         boundary_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()), components_detail=comps[:12])
fail = []
if len(big) != 1: fail.append('%d body-sized components (duplicate / multi-view figures)' % len(big))
R['verdict'] = 'PASS (single body: whole-source anatomy review may begin)' if not fail else 'FAIL: ' + '; '.join(fail)
R['flags_for_review'] = [x for x in (('%d small extra pieces' % len(small)) if small else None, ('nested components %s' % nested) if nested else None,
                                      ('open surface: %d boundary edges' % R['boundary_edges']) if R['boundary_edges'] else None,
                                      ('%d non-manifold edges' % R['nonmanifold_edges']) if R['nonmanifold_edges'] else None) if x]
json.dump(R, open(out, 'w'), indent=1); print(R['sha256'][:16], R['verdict'], R['flags_for_review']); sys.exit(0 if not fail else 3)
