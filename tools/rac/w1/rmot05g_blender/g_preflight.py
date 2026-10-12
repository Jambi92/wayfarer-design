# RAC RM-OT-05G — standalone PREFLIGHT for a delivered Gorrund sculpt OBJ (Python 3 + numpy only; no Blender, no repository scratch data).
# Run it on the sculptor's machine before submitting, and again on receipt. It mirrors the 05F ingest checks with the SAME thresholds,
# using only the frozen handoff package. It is a preflight: the authoritative decision is f_ingest / f_reentry in the repository.
#   P1 topology     13 380 'v' records; 'f' records identical (order, indices, winding) to the template's
#   P2 identity     no ambiguous correspondence: not a permutation of the template, not a reordered copy (count checks are not enough)
#   P3 stature/ground within 0.05 cm of the template                                 (I3)
#   P4 no-touch     every NO_TOUCH_* vertex within 0.5 cm                               (I4)
#   P5 anchor fit   similarity fit on the no-touch anchors: |scale-1| <= 0.002, rotation <= 0.2 deg, shift <= 0.3 cm   (I2)
#   P6 true floor   0 vertices (outside head / neck / hands) more than 0.2 cm inside template/GO_true_floor_r6.obj   (I5)
#   P7 posture      hand / foot / head anchor-set centroids within 0.3 cm                (I6)
#   info            per-family displacement statistics; raw volume ratio
# Usage: python3 g_preflight.py GO_sculpt_S1_r6.obj [--package <handoff dir>]      exit 0 = all PASS
import sys, os, json, math, hashlib
import numpy as np
def read(p):
    V, F, vl, fl = [], [], [], []
    for ln in open(p):
        if ln.startswith('v '): x = ln.split(); V.append([float(x[1]), float(x[2]), float(x[3])])
        elif ln.startswith('f '): F.append([int(t.split('/')[0]) - 1 for t in ln.split()[1:]]); fl.append(' '.join(t.split('/')[0] for t in ln.split()[1:]))
    return np.array(V, float), F, fl
def normals_out(V, F):
    F = np.asarray(F); n = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3): np.add.at(n, F[:, k], fn)
    n /= np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
    vol = np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6.0
    return (n if vol > 0 else -n), vol
def preflight(obj, root):
    T, TF, Tfl = read(os.path.join(root, 'template', 'GO_ref_route_r6.obj')); Fl = read(os.path.join(root, 'template', 'GO_true_floor_r6.obj'))[0]
    R = {k: np.array(v) for k, v in json.load(open(os.path.join(root, 'data', 'regions.json')))['regions'].items()}
    S, SF, Sfl = read(obj); rep = {'file': os.path.basename(obj), 'sha256': hashlib.sha256(open(obj, 'rb').read()).hexdigest(), 'checks': {}}; C = rep['checks']
    C['P1_topology'] = {'n_vertices': len(S), 'expected': len(T), 'faces_identical': Sfl == Tfl, 'pass': len(S) == len(T) and Sfl == Tfl}
    if not C['P1_topology']['pass']: rep['pass'] = False; return rep
    d = np.linalg.norm(S - T, axis=1)
    # identity: a reordered copy shows up as large displacements of most vertices while the point SET is (nearly) the template's
    perm = bool(np.median(d) > 1.0)
    C['P2_identity'] = {'median_displacement_cm': float(np.median(d)), 'pass': not perm,
                        'note': 'a median vertex displacement above 1 cm means the vertex order no longer matches the template (fail closed)'}
    C['P3_stature_ground'] = {'stature_cm': float(S[:, 2].max()), 'template_cm': float(T[:, 2].max()), 'min_z_cm': float(S[:, 2].min()),
                              'pass': bool(abs(S[:, 2].max() - T[:, 2].max()) <= 0.05 and abs(S[:, 2].min()) <= 0.05)}
    nt = {k: float(d[ix].max()) for k, ix in R.items() if k.startswith('NO_TOUCH')}
    C['P4_no_touch'] = {'max_change_cm': nt, 'limit_cm': 0.5, 'pass': max(nt.values()) <= 0.5}
    an = np.unique(np.concatenate([ix for k, ix in R.items() if k.startswith('NO_TOUCH')])); A, B = T[an], S[an]
    ca, cb = A.mean(0), B.mean(0); U, s, Vt = np.linalg.svd((B - cb).T @ (A - ca)); dd = np.sign(np.linalg.det(U @ Vt)); D = np.diag([1, 1, dd]); Rm = U @ D @ Vt
    sc = (s * np.diag(D)).sum() / ((A - ca) ** 2).sum(); ang = math.degrees(math.acos(np.clip((np.trace(Rm) - 1) / 2, -1, 1)))
    C['P5_anchor_fit'] = {'scale': float(sc), 'rotation_deg': float(ang), 'shift_cm': float(np.linalg.norm(cb - ca)), 'pass': bool(abs(sc - 1) <= 0.002 and ang <= 0.2 and np.linalg.norm(cb - ca) <= 0.3)}
    n, _ = normals_out(Fl, TF); sd = np.einsum('ij,ij->i', S - Fl, n)
    ext = np.zeros(len(S), bool); ext[R['NO_TOUCH_head_neck']] = True; ext[R['NO_TOUCH_hands_digits']] = True
    C['P6_true_floor'] = {'n_inside_0p2cm': int((sd[~ext] < -0.2).sum()), 'min_signed_cm': float(sd[~ext].min()), 'pass': bool((sd[~ext] < -0.2).sum() == 0)}
    cen = {k: float(np.linalg.norm(S[ix].mean(0) - T[ix].mean(0))) for k, ix in R.items() if k.startswith('NO_TOUCH')}
    C['P7_posture_anchors'] = {'centroid_shift_cm': cen, 'limit_cm': 0.3, 'pass': max(cen.values()) <= 0.3}
    rep['families'] = {k: {'n': int(len(ix)), 'p50_cm': round(float(np.percentile(d[ix], 50)), 2), 'p90_cm': round(float(np.percentile(d[ix], 90)), 2), 'max_cm': round(float(d[ix].max()), 2)}
                       for k, ix in R.items() if not k.startswith('NO_TOUCH')}
    rep['raw_volume_ratio'] = float(abs(normals_out(S, TF)[1]) / abs(normals_out(T, TF)[1]))
    rep['n_moved_vertices_over_0p01cm'] = int((d > 0.01).sum())
    rep['pass'] = all(c['pass'] for c in C.values())
    return rep
if __name__ == '__main__':
    a = sys.argv[1:]
    if '--package' in a: root = a[a.index('--package') + 1]
    else:
        root = os.path.dirname(os.path.abspath(__file__))
        while root != os.path.dirname(root) and not os.path.exists(os.path.join(root, 'template', 'GO_ref_route_r6.obj')): root = os.path.dirname(root)
    r = preflight(a[0], root); print(json.dumps(r, indent=1)); print('PREFLIGHT', 'PASS' if r['pass'] else 'FAIL'); sys.exit(0 if r['pass'] else 1)
