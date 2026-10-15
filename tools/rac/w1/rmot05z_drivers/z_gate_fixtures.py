# RM-OT-05Z1: deterministic synthetic GLB fixtures and self-test for z_single_body_gate.py.
# Builds small binary GLBs from code (byte-identical on every run), runs the gate on each, and compares with the committed
# expectations in reviews/rac-rmot05z-input/gate_selftest/expected_fixtures.json. Optionally also checks the two real sources.
# A "body" is a closed box 0.4 x 1.8 x 0.3 (standing on y = 0); an "accessory" is a closed 0.05 cube.
# Usage: python3 z_gate_fixtures.py OUTDIR EXPECTED.json [--real GORRUND_05X.glb BASE1_05Y.glb]   exit 0 all as expected, 1 otherwise
import sys, os, json, struct, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z_single_body_gate as G

def box(lo, hi):
    x0, y0, z0 = lo; x1, y1, z1 = hi
    V = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], np.float32)
    F = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4], [3, 7, 6], [3, 6, 2], [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]], np.uint32)
    return V, F
BODY = box((-0.2, 0.0, -0.15), (0.2, 1.8, 0.15)); ACC = box((0.5, 0.0, 0.0), (0.55, 0.05, 0.05))

def glb(meshes, nodes, scenes, scene=0, mode=None):
    """meshes: list of lists of (V, F) primitives. Returns GLB bytes."""
    bin_ = b''; views = []; accs = []; jm = []
    def add(arr, target):
        nonlocal bin_
        while len(bin_) % 4: bin_ += b'\x00'
        off = len(bin_); data = arr.tobytes(); bin_ += data; views.append(dict(buffer=0, byteOffset=off, byteLength=len(data), target=target)); return len(views) - 1
    for prims in meshes:
        ps = []
        for V, F in prims:
            vp = add(V, 34962); accs.append(dict(bufferView=vp, componentType=5126, count=len(V), type='VEC3', min=V.min(0).tolist(), max=V.max(0).tolist()))
            pa = len(accs) - 1; vi = add(F.ravel(), 34963); accs.append(dict(bufferView=vi, componentType=5125, count=int(F.size), type='SCALAR'))
            p = dict(attributes=dict(POSITION=pa), indices=len(accs) - 1)
            if mode is not None: p['mode'] = mode
            ps.append(p)
        jm.append(dict(primitives=ps))
    while len(bin_) % 4: bin_ += b'\x00'
    J = dict(asset=dict(version='2.0', generator='RM-OT-05Z1 fixture builder'), scene=scene, scenes=scenes, nodes=nodes, meshes=jm,
             accessors=accs, bufferViews=views, buffers=[dict(byteLength=len(bin_))])
    js = json.dumps(J, separators=(',', ':'), sort_keys=True).encode()
    while len(js) % 4: js += b' '
    total = 12 + 8 + len(js) + 8 + len(bin_)
    return struct.pack('<4sII', b'glTF', 2, total) + struct.pack('<I4s', len(js), b'JSON') + js + struct.pack('<I4s', len(bin_), b'BIN\x00') + bin_

S2 = 2 ** -0.5
FIX = {
    'f1_one_mesh_one_node': glb([[BODY]], [dict(mesh=0)], [dict(nodes=[0])]),
    'f2_one_mesh_three_instanced_nodes': glb([[BODY]], [dict(mesh=0, translation=[0, 0, 0]), dict(mesh=0, translation=[1, 0, 0]), dict(mesh=0, translation=[2, 0, 0])], [dict(nodes=[0, 1, 2])]),
    'f3_body_plus_small_accessory': glb([[BODY, ACC]], [dict(mesh=0)], [dict(nodes=[0])]),
    'f4_parent_child_transform': glb([[BODY]], [dict(children=[1], translation=[10, 0, 0], scale=[2, 2, 2]), dict(mesh=0, translation=[1, 0, 0], rotation=[0, S2, 0, S2])], [dict(nodes=[0])]),
    'f5_unused_mesh_definition': glb([[BODY], [BODY]], [dict(mesh=0)], [dict(nodes=[0])]),
    'f6_matrix_node_instances': glb([[BODY]], [dict(mesh=0, matrix=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]), dict(mesh=0, matrix=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0, 0, 1])], [dict(nodes=[0, 1])]),
    'f7_coincident_duplicate_instances': glb([[BODY]], [dict(mesh=0), dict(mesh=0)], [dict(nodes=[0, 1])]),
    'f8_unsupported_strip_mode': glb([[BODY]], [dict(mesh=0)], [dict(nodes=[0])], mode=5),
    'f9_inactive_scene_with_extra_bodies': glb([[BODY]], [dict(mesh=0), dict(mesh=0, translation=[1, 0, 0]), dict(mesh=0, translation=[2, 0, 0])], [dict(nodes=[0]), dict(nodes=[0, 1, 2])], scene=0),
}

def summary(R):
    s = dict(result=R['result'])
    for k in ('mesh_definitions', 'mesh_instances', 'primitive_instances', 'body_sized_components', 'unused_mesh_definitions', 'coincident_duplicate_instances'):
        if k in R: s[k] = R[k]
    if 'small_pieces' in R: s['small_pieces'] = len(R['small_pieces'])
    if 'world_bounds' in R: s['world_bounds'] = R['world_bounds']
    return s

if __name__ == '__main__':
    od, expf = sys.argv[1:3]; os.makedirs(od, exist_ok=True); got = {}
    for name, data in FIX.items():
        p = os.path.join(od, name + '.glb'); open(p, 'wb').write(data)
        R = G.run(p); got[name] = dict(sha256=hashlib.sha256(data).hexdigest(), **summary(R))
    if '--real' in sys.argv:
        a, b = sys.argv[sys.argv.index('--real') + 1:sys.argv.index('--real') + 3]
        for name, p in (('real_05X_Gorrund', a), ('real_05Y_base_1', b)):
            R = G.run(p); got[name] = dict(sha256=R['sha256'], **{k: v for k, v in summary(R).items() if k != 'world_bounds'})
    exp = json.load(open(expf)) if os.path.exists(expf) else None
    ok = True
    if exp is None:
        json.dump(got, open(expf, 'w'), indent=1); print('expectations written (first run): review them before committing')
    else:
        for k, v in exp.items():
            g = got.get(k)
            if g is None: print('NOT RUN', k); ok = ok and k.startswith('real_') and '--real' not in sys.argv; continue
            if g != v: ok = False; print('MISMATCH', k, '\n expected', v, '\n got     ', g)
            else: print('ok', k, g['result'])
    sys.exit(0 if ok else 1)
