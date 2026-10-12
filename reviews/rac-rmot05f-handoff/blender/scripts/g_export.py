# RAC RM-OT-05G — Gorrund hand-sculpt CONTROLLED EXPORTER (run inside Blender on a scene made by g_setup.py).
#
#   GUI:  Scripting > Open g_export.py > set SCULPT_ID (and SCULPTOR) below > Run Script   -> writes GO_sculpt_<ID>_r6.obj next to the .blend
#   CLI:  blender --background <working.blend> --python g_export.py -- --id S1 --sculptor "Name" [--package <handoff dir>] [--outdir <dir>]
#
# Exports ONLY the base-level vertex positions of GO_SCULPT_BASE in template order, followed by the template's own face records (verbatim,
# same order and winding). It never uses Blender's OBJ exporter, never infers correspondence (no nearest-neighbour matching), and never
# repairs or reorders anything: on any doubt it REFUSES (fail closed) and writes nothing.
# Hard checks (any failure = no file):
#   X1 object      GO_SCULPT_BASE exists, is a mesh, no parent / constraints; location, rotation (all modes), scale and their deltas are identity
#                  AND the evaluated world matrix == identity (|m - I| <= 1e-9): no net rotation / scale / move
#   X2 counts      13 380 vertices, template face count
#   X3 identity    rac_src_index exists and is exactly 0..13379 in order (stored original index: catches any sort / reorder / rebuild)
#   X4 faces       every polygon's vertex loop equals the template face record (same start vertex, same winding)
#   X5 state       no shape keys, no Multires modifier (project / apply to the base first), not in Edit / Sculpt mode with unsaved buffer
#   X6 values      all coordinates finite
#   X7 template    the package template's SHA-256 equals the one stored at setup
#   X8 stature / ground   within 0.05 cm of the template                      (ingest I3 threshold)
#   X9 no-touch    every NO_TOUCH vertex within 0.5 cm of its template position  (ingest I4 threshold)
# Advisory preflight (reported, authoritative versions run in f_ingest on delivery): anchor similarity fit (I2), raw true-floor test (I5),
# anchor centroids (I6), per-family displacement statistics.
# Unmoved vertices are written with their template text verbatim (bit-exact round trip); moved vertices as %.5f cm.
import bpy, os, sys, json, hashlib, math, datetime
SCULPT_ID = 'S1'             # two characters; first genuine delivery S1, then S2, ...
SCULPTOR = ''                # name / studio of the person who sculpted (provenance)
PACKAGE_ROOT = None
NV = 13380

def args():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    d = {}
    for i, k in enumerate(a):
        if k.startswith('--'): d[k[2:]] = a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith('--') else True
    return d

def package_root(d):
    if d.get('package'): return os.path.abspath(d['package'])
    if PACKAGE_ROOT: return PACKAGE_ROOT
    cands = []
    try: cands.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except NameError: pass
    if bpy.data.filepath: cands += [os.path.dirname(bpy.data.filepath), os.path.dirname(os.path.dirname(bpy.data.filepath))]
    for t in bpy.data.texts:
        if t.filepath: cands.append(os.path.dirname(os.path.dirname(bpy.path.abspath(t.filepath))))
    for c in cands:
        for r in (c, os.path.join(c, '..')):
            if os.path.exists(os.path.join(r, 'template', 'GO_ref_route_r6.obj')): return os.path.abspath(r)
    raise RuntimeError('package root not found: set PACKAGE_ROOT')

def sha256b(b): return hashlib.sha256(b).hexdigest()

def read_template(p):
    vlines, flines, faces = [], [], []
    for ln in open(p):
        if ln.startswith('v '): vlines.append(ln.rstrip('\n'))
        elif ln.startswith('f '): flines.append(ln.rstrip('\n')); faces.append(tuple(int(t.split('/')[0]) - 1 for t in ln.split()[1:]))
    return vlines, flines, faces

def fit_similarity(A, B):
    """scale, rotation (deg), centroid shift of the best similarity map A -> B (numpy if present)"""
    import numpy as np
    A = np.asarray(A, float); B = np.asarray(B, float); ca, cb = A.mean(0), B.mean(0); A0, B0 = A - ca, B - cb
    U, s, Vt = np.linalg.svd(B0.T @ A0); dd = np.sign(np.linalg.det(U @ Vt)); D = np.diag([1, 1, dd]); R = U @ D @ Vt
    sc = (s * np.diag(D)).sum() / (A0 ** 2).sum(); ang = math.degrees(math.acos(max(-1.0, min(1.0, (np.trace(R) - 1) / 2))))
    return float(sc), float(ang), float(np.linalg.norm(cb - ca))

def check_and_export(root, sid, sculptor, outdir=None, write=True):
    rep = {'checks': {}, 'advisory': {}, 'blender': bpy.app.version_string, 'id': sid, 'sculptor': sculptor}; C = rep['checks']
    def fail(k, msg): C[k] = {'pass': False, 'detail': msg}; rep['pass'] = False; return rep
    if not (isinstance(sid, str) and len(sid) == 2 and sid.isalnum()): return fail('X0_id', 'SCULPT_ID must be two letters / digits, got %r' % (sid,))
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        try: bpy.ops.object.mode_set(mode='OBJECT')                    # flushes Edit / Sculpt buffers into the mesh before reading it
        except Exception as ex: return fail('X5_state', 'could not leave %s mode: %s' % (bpy.context.object.mode, ex))
    ob = bpy.data.objects.get('GO_SCULPT_BASE')
    if ob is None or ob.type != 'MESH': return fail('X1_object', 'GO_SCULPT_BASE mesh object not found')
    bpy.context.view_layer.update()                                   # matrix_world must reflect the current transform properties
    M = ob.matrix_world; dev = max(abs(M[i][j] - (1.0 if i == j else 0.0)) for i in range(4) for j in range(4))
    # the transform PROPERTIES are checked too (not only the cached matrix): location / rotation / scale and their deltas must be identity
    props = {'location': tuple(ob.location), 'rotation_euler': tuple(ob.rotation_euler), 'rotation_quaternion': tuple(ob.rotation_quaternion),
             'rotation_axis_angle': tuple(ob.rotation_axis_angle), 'scale': tuple(ob.scale), 'delta_location': tuple(ob.delta_location),
             'delta_rotation_euler': tuple(ob.delta_rotation_euler), 'delta_rotation_quaternion': tuple(ob.delta_rotation_quaternion), 'delta_scale': tuple(ob.delta_scale)}
    ident = {'location': (0, 0, 0), 'rotation_euler': (0, 0, 0), 'rotation_quaternion': (1, 0, 0, 0), 'rotation_axis_angle': (0, 0, 1, 0), 'scale': (1, 1, 1),
             'delta_location': (0, 0, 0), 'delta_rotation_euler': (0, 0, 0), 'delta_rotation_quaternion': (1, 0, 0, 0), 'delta_scale': (1, 1, 1)}
    pdev = max(abs(x - y) for k in props for x, y in zip(props[k], ident[k]))
    C['X1_object'] = {'pass': ob.parent is None and dev <= 1e-9 and pdev <= 1e-9, 'matrix_world_max_deviation_from_identity': dev,
                      'transform_property_max_deviation': pdev, 'parent': ob.parent.name if ob.parent else None, 'constraints': [c.type for c in ob.constraints]}
    if ob.constraints: C['X1_object']['pass'] = False
    if not C['X1_object']['pass']: rep['pass'] = False; return rep
    me = ob.data; tpl = os.path.join(root, 'template', 'GO_ref_route_r6.obj'); tb = open(tpl, 'rb').read()
    C['X7_template'] = {'pass': sha256b(tb) == me.get('rac_template_sha256'), 'template_sha256': sha256b(tb), 'stored_sha256': me.get('rac_template_sha256')}
    if not C['X7_template']['pass']: rep['pass'] = False; return rep
    vlines, flines, faces = read_template(tpl)
    C['X2_counts'] = {'pass': len(me.vertices) == NV and len(me.polygons) == len(faces), 'vertices': len(me.vertices), 'faces': len(me.polygons)}
    if not C['X2_counts']['pass']: rep['pass'] = False; return rep
    at = me.attributes.get('rac_src_index')
    if at is None or at.domain != 'POINT' or at.data_type != 'INT': return fail('X3_identity', 'rac_src_index attribute missing or wrong type: correspondence is ambiguous')
    idx = [0] * NV; at.data.foreach_get('value', idx)
    C['X3_identity'] = {'pass': idx == list(range(NV)), 'first_mismatch': next((i for i, v in enumerate(idx) if v != i), None)}
    if not C['X3_identity']['pass']: rep['pass'] = False; return rep
    bad = next((p.index for p in me.polygons if tuple(p.vertices) != faces[p.index]), None)
    C['X4_faces'] = {'pass': bad is None, 'first_mismatching_face': bad}
    if bad is not None: rep['pass'] = False; return rep
    mods = [m.type for m in ob.modifiers]
    C['X5_state'] = {'pass': me.shape_keys is None and 'MULTIRES' not in mods, 'shape_keys': me.shape_keys is not None, 'modifiers': mods,
                     'note': 'non-multires modifiers are ignored (base data is exported, never the evaluated mesh)'}
    if not C['X5_state']['pass']: rep['pass'] = False; return rep
    co = [0.0] * (3 * NV); me.vertices.foreach_get('co', co); src = [0.0] * (3 * NV); me.attributes['rac_src_co'].data.foreach_get('vector', src)
    C['X6_values'] = {'pass': all(math.isfinite(x) for x in co)}
    if not C['X6_values']['pass']: rep['pass'] = False; return rep
    P = [tuple(co[3 * i:3 * i + 3]) for i in range(NV)]; S = [tuple(src[3 * i:3 * i + 3]) for i in range(NV)]
    st, st0 = max(p[2] for p in P), max(s[2] for s in S); g = min(p[2] for p in P)
    C['X8_stature_ground'] = {'pass': abs(st - st0) <= 0.05 and abs(g) <= 0.05, 'stature_cm': st, 'template_cm': st0, 'min_z_cm': g}
    regions = json.load(open(os.path.join(root, 'data', 'regions.json')))['regions']
    dn = [math.dist(P[i], S[i]) for i in range(NV)]
    nt = {k: max(dn[i] for i in ix) for k, ix in regions.items() if k.startswith('NO_TOUCH')}
    C['X9_no_touch'] = {'pass': max(nt.values()) <= 0.5, 'max_change_cm': nt, 'limit_cm': 0.5}
    try:
        anc = sorted(set(i for k, ix in regions.items() if k.startswith('NO_TOUCH') for i in ix))
        sc_, ang, tr = fit_similarity([S[i] for i in anc], [P[i] for i in anc])
        rep['advisory']['I2_anchor_fit'] = {'scale': sc_, 'rotation_deg': ang, 'centroid_shift_cm': tr, 'ok': abs(sc_ - 1) <= 0.002 and ang <= 0.2 and tr <= 0.3}
    except Exception as ex: rep['advisory']['I2_anchor_fit'] = {'error': str(ex)}
    rep['advisory']['family_displacement_cm'] = {k: {'n': len(ix), 'max': round(max(dn[i] for i in ix), 3), 'mean': round(sum(dn[i] for i in ix) / len(ix), 3)}
                                                for k, ix in regions.items() if not k.startswith('NO_TOUCH')}
    rep['n_moved_vertices'] = sum(1 for i in range(NV) if P[i] != S[i])
    rep['pass'] = all(c['pass'] for c in C.values())
    if not rep['pass'] or not write: return rep
    outdir = outdir or (os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd())
    fn = os.path.join(outdir, 'GO_sculpt_%s_r6.obj' % sid)
    lines = ['# RM-OT-05G Gorrund hand-sculpt delivery %s. Base: template/GO_ref_route_r6.obj (sha256 %s).' % (sid, sha256b(tb)),
             '# Exported by g_export.py (template-order positions + template face records verbatim). Blender %s. Sculptor: %s. %s' % (bpy.app.version_string, sculptor or 'UNSPECIFIED', datetime.datetime.now().isoformat(timespec='seconds')),
             '# Units cm, Z up, ground z = 0, +Y anterior, +X body left, R-6 neutral stance. 13380 vertices, template faces.', 'o gorrund_body']
    for i in range(NV):
        lines.append(vlines[i] if P[i] == S[i] else 'v %.5f %.5f %.5f' % P[i])
    lines += flines
    data = ('\n'.join(lines) + '\n').encode()
    open(fn, 'wb').write(data)
    rep['output'] = fn; rep['output_sha256'] = sha256b(data); rep['template_sha256'] = sha256b(tb)
    rep['blend_file'] = bpy.data.filepath or None
    json.dump(rep, open(fn[:-4] + '_export_report.json', 'w'), indent=1)
    return rep

if __name__ == '__main__':
    d = args(); r = check_and_export(package_root(d), d.get('id', SCULPT_ID), d.get('sculptor', SCULPTOR), d.get('outdir'))
    print('RAC_EXPORT', 'PASS' if r['pass'] else 'REFUSED', json.dumps(r, default=str)[:3000])
    if not r['pass'] and bpy.app.background: sys.exit(1)
