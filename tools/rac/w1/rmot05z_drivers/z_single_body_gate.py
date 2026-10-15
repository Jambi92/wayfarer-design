# RM-OT-05Z / 05Z1: mechanical single-body intake gate for any new Gorrund source GLB. READ-ONLY (the GLB is never written).
#
# 05Z1 hardening: the test is based on the ACTIVE SCENE GRAPH, not on unique mesh definitions.
#   1. the active scene (glTF "scene", default 0) is resolved and its node hierarchy traversed recursively;
#   2. node transforms are composed from "matrix" (column-major) or TRS (translation, rotation quaternion xyzw, scale);
#   3. each referenced mesh primitive is instantiated once per node instance;
#   4. POSITION data is transformed to world coordinates before component and body-size analysis;
#   5. several primitives per mesh / several meshes per body are supported (geometry is welded by exact WORLD position);
#   6. mesh definitions not referenced by the active scene are ignored for the body count (and reported);
#   7. counts reported: scene nodes, mesh instances, primitive instances, connected components, body-sized components;
#   8. FAIL when more than one body-sized component exists, including several nodes instancing the same mesh. Coincident
#      duplicate instances (same mesh, same world bounds - they would weld into one component) are detected and FAIL too;
#   9. small disconnected pieces (< 50 % of the tallest component's height) are LISTED, never silently dropped.
# Anything the gate cannot read reliably returns REVIEW (fail-safe, exit 4), never PASS: non-GLB container, external or
# data-URI buffers, sparse accessors, non-triangle primitive modes, non-float32 / normalized POSITION, malformed or
# out-of-range indices, index count not divisible by 3, missing scene, node cycles, non-finite transforms or positions.
# Flags for the later anatomy review (do not change the verdict): nested components, open boundary / non-manifold edges.
# A PASS only permits the whole-source anatomy review; it accepts nothing.
#
# Usage: python3 z_single_body_gate.py SOURCE.glb OUT.json      exit 0 PASS, 3 FAIL, 4 REVIEW
import sys, json, struct, hashlib, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

class Review(Exception): pass

CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def parse_glb(b):
    if len(b) < 20 or b[:4] != b'glTF': raise Review('not a binary glTF (GLB) container')
    ver, total = struct.unpack('<II', b[4:12])
    if ver != 2: raise Review('glTF version %d is not supported' % ver)
    if total != len(b): raise Review('declared length %d != file length %d' % (total, len(b)))
    o = 12; J = None; BIN = None
    while o + 8 <= len(b):
        ln, typ = struct.unpack('<I4s', b[o:o + 8]); body = b[o + 8:o + 8 + ln]
        if len(body) != ln: raise Review('truncated chunk')
        if typ == b'JSON' and J is None: J = json.loads(body.rstrip(b' \x00').decode('utf-8'))
        elif typ == b'BIN\x00' and BIN is None: BIN = body
        o += 8 + ln
    if J is None: raise Review('no JSON chunk')
    return J, BIN

def read_accessor(J, BIN, i, want_float_vec3=False):
    try: a = J['accessors'][i]
    except (IndexError, KeyError, TypeError): raise Review('accessor %r missing' % i)
    if 'sparse' in a: raise Review('sparse accessor %d not supported' % i)
    if 'bufferView' not in a: raise Review('accessor %d has no bufferView' % i)
    ct = a.get('componentType'); nc = NC.get(a.get('type')); cnt = a.get('count', 0)
    if ct not in CT or nc is None: raise Review('accessor %d has unsupported type' % i)
    if want_float_vec3 and (ct != 5126 or nc != 3 or a.get('normalized', False)): raise Review('POSITION accessor %d is not float32 VEC3' % i)
    v = J['bufferViews'][a['bufferView']]; buf = J['buffers'][v['buffer']]
    if 'uri' in buf or v['buffer'] != 0 or BIN is None: raise Review('external / data-URI buffer not supported')
    dt = np.dtype(CT[ct]); es = dt.itemsize * nc; stride = v.get('byteStride') or es
    start = v.get('byteOffset', 0) + a.get('byteOffset', 0); need = start + (cnt - 1) * stride + es if cnt else start
    if cnt and (need > v.get('byteOffset', 0) + v['byteLength'] or need > len(BIN)): raise Review('accessor %d reads past its buffer view' % i)
    if cnt == 0: return np.zeros((0, nc), dt)
    if stride == es: arr = np.frombuffer(BIN, dt, cnt * nc, start).reshape(cnt, nc)
    else: arr = np.ndarray(shape=(cnt, nc), dtype=dt, buffer=BIN, offset=start, strides=(stride, dt.itemsize)).copy()
    return arr

def quat_mat(q):
    x, y, z, w = q; n = np.sqrt(x * x + y * y + z * z + w * w)
    if not np.isfinite(n) or n == 0: raise Review('invalid rotation quaternion')
    x, y, z, w = x / n, y / n, z / n, w / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])

def local_matrix(n):
    if 'matrix' in n:
        M = np.array(n['matrix'], float)
        if M.shape != (16,): raise Review('node matrix is not 16 values')
        M = M.reshape(4, 4).T                                  # glTF matrices are column-major
    else:
        M = np.eye(4); t = np.array(n.get('translation', [0, 0, 0]), float); s = np.array(n.get('scale', [1, 1, 1]), float)
        R = quat_mat(n.get('rotation', [0, 0, 0, 1])); M[:3, :3] = R * s[None, :]; M[:3, 3] = t
    if not np.all(np.isfinite(M)): raise Review('non-finite node transform')
    return M

def instances(J):
    scenes = J.get('scenes') or []
    si = J.get('scene', 0)
    if not scenes or not (0 <= si < len(scenes)): raise Review('no active scene')
    out = []; visited = 0
    def walk(ni, parent, path):
        nonlocal visited
        if ni in path: raise Review('node cycle at node %d' % ni)
        try: n = J['nodes'][ni]
        except (IndexError, KeyError): raise Review('node %r missing' % ni)
        visited += 1; W = parent @ local_matrix(n)
        if 'mesh' in n: out.append(dict(node=ni, mesh=n['mesh'], world=W))
        for c in n.get('children', []): walk(c, W, path | {ni})
    for r in scenes[si].get('nodes', []): walk(r, np.eye(4), frozenset())
    return si, visited, out

def run(path):
    b = open(path, 'rb').read()
    R = dict(file=path.split('/')[-1], bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
    try:
        J, BIN = parse_glb(b)
        si, visited, inst = instances(J)
        if not inst: raise Review('active scene references no mesh')
        Ps, Fs, tag, base = [], [], [], 0; prim_inst = 0
        used = sorted({i['mesh'] for i in inst}); nmesh = len(J.get('meshes', []))
        for k, it in enumerate(inst):
            try: mesh = J['meshes'][it['mesh']]
            except (IndexError, KeyError): raise Review('mesh %r missing' % it['mesh'])
            for pr in mesh['primitives']:
                if pr.get('mode', 4) != 4: raise Review('primitive mode %d (not TRIANGLES) not supported' % pr.get('mode'))
                if 'POSITION' not in pr.get('attributes', {}): raise Review('primitive without POSITION')
                P = read_accessor(J, BIN, pr['attributes']['POSITION'], want_float_vec3=True).astype(np.float64)
                if 'indices' in pr:
                    I = read_accessor(J, BIN, pr['indices'])
                    if I.dtype.kind != 'u': raise Review('indices are not unsigned integers')
                    I = I.ravel().astype(np.int64)
                else: I = np.arange(len(P), dtype=np.int64)
                if len(I) % 3: raise Review('index count not divisible by 3')
                if len(I) and (I.min() < 0 or I.max() >= len(P)): raise Review('index out of range')
                Wp = P @ it['world'][:3, :3].T + it['world'][:3, 3]
                if not np.all(np.isfinite(Wp)): raise Review('non-finite world positions')
                Ps.append(Wp); Fs.append(I.reshape(-1, 3) + base); tag.append(np.full(len(I) // 3, k)); base += len(P); prim_inst += 1
        P = np.concatenate(Ps); F = np.concatenate(Fs); T = np.concatenate(tag)
        U, inv = np.unique(P, axis=0, return_inverse=True); F = inv.ravel()[F]; n = len(U)
        E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1); ue, cnt = np.unique(E, axis=0, return_counts=True)
        nc, lab = connected_components(sp.coo_matrix((np.ones(len(ue)), (ue[:, 0], ue[:, 1])), shape=(n, n)), directed=False)
        fl = lab[F[:, 0]]; comps = []
        for c in np.argsort(-np.bincount(fl, minlength=nc)):
            m = fl == c
            if not m.any(): continue
            vv = U[np.unique(F[m])]
            comps.append(dict(faces=int(m.sum()), instances=sorted({int(x) for x in np.unique(T[m])}), bbox_min=vv.min(0).round(5).tolist(),
                              bbox_max=vv.max(0).round(5).tolist(), height=float(vv[:, 1].max() - vv[:, 1].min())))
        Hmax = max(c['height'] for c in comps); big = [c for c in comps if c['height'] >= 0.5 * Hmax]; small = [c for c in comps if c['height'] < 0.5 * Hmax]
        # coincident duplicate instances: same mesh, identical world bounds -> would weld into one component
        ib = {}
        for k, it in enumerate(inst):
            m = T == k
            if m.any():
                vv = U[np.unique(F[m])]; ib.setdefault(it['mesh'], []).append((k, tuple(np.round(np.r_[vv.min(0), vv.max(0)], 5))))
        dup = [[a[0], c[0]] for v in ib.values() for i, a in enumerate(v) for c in v[i + 1:] if a[1] == c[1]]
        def inside(a, c): return all(a['bbox_min'][i] >= c['bbox_min'][i] for i in range(3)) and all(a['bbox_max'][i] <= c['bbox_max'][i] for i in range(3))
        nested = [i for i, a in enumerate(comps) for j, c in enumerate(comps) if i != j and c['faces'] > a['faces'] and inside(a, c)]
        R.update(active_scene=si, scene_nodes_traversed=visited, mesh_definitions=nmesh, meshes_referenced_by_scene=used,
                 unused_mesh_definitions=[i for i in range(nmesh) if i not in used], mesh_instances=len(inst), primitive_instances=prim_inst,
                 instance_nodes=[it['node'] for it in inst], world_positions=int(len(P)), welded_world_positions=int(n), triangles=int(len(F)),
                 components=len(comps), body_sized_components=len(big), coincident_duplicate_instances=dup,
                 small_pieces=[dict(faces=c['faces'], height=round(c['height'], 5), bbox_min=c['bbox_min'], bbox_max=c['bbox_max']) for c in small][:50],
                 nested_components=nested, boundary_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
                 world_bounds=dict(min=U.min(0).round(5).tolist(), max=U.max(0).round(5).tolist()), components_detail=comps[:12])
        fail = []
        if len(big) != 1: fail.append('%d body-sized components (duplicate / multi-view / instanced figures)' % len(big))
        if dup: fail.append('coincident duplicate mesh instances %s' % dup)
        R['result'] = 'PASS' if not fail else 'FAIL'
        R['verdict'] = 'PASS (single body: whole-source anatomy review may begin)' if not fail else 'FAIL: ' + '; '.join(fail)
        R['flags_for_review'] = [x for x in (('%d small extra pieces listed' % len(small)) if small else None, ('nested components %s' % nested) if nested else None,
                                              ('open surface: %d boundary edges' % R['boundary_edges']) if R['boundary_edges'] else None,
                                              ('%d non-manifold edges' % R['nonmanifold_edges']) if R['nonmanifold_edges'] else None) if x]
    except Review as e:
        R['result'] = 'REVIEW'; R['verdict'] = 'REVIEW (fail-safe; the gate could not be evaluated reliably): %s' % e; R['flags_for_review'] = []
    return R

if __name__ == '__main__':
    R = run(sys.argv[1]); json.dump(R, open(sys.argv[2], 'w'), indent=1)
    print(R['sha256'][:16], R['verdict'], R['flags_for_review']); sys.exit({'PASS': 0, 'FAIL': 3, 'REVIEW': 4}[R['result']])
