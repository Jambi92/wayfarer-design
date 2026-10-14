# RM-OT-05U4: FIXED-REFERENCE crease-depth measurement for the opt-in U2 path (replaces the moving-plane u3_crease use).
#
#   build   : derive the reference ONCE from the pinned, unchanged 05U RETURN and write a versioned reference artifact.
#   measure : intersect a RETURN with the FROZEN planes, walk the in-region run from the FROZEN entry edge, require it to
#             leave through the FROZEN exit edge, and measure depth against the FROZEN chord / inward normal.
#
# Reference (per section, keyed by section id "A" / "B"):
#   frame O, d (05Q arm frame, float64); plane P = {x : (x - O).d = s0}, s0 = (Vbaseline[anchor] - O).d computed once;
#   anchor = named S3 vertex (61581 / 61580; zero-based S3 index) used ONLY at build time to pick the section component;
#   entry / exit = the two region/non-region edges (S3 vertex-index pairs; all four vertices are frozen-ring vertices) where the
#   baseline in-region run starts / ends; chord endpoints A_, B_ (float64), unit chord u, inward unit normal n (toward
#   O + s0 d); baseline depth (full precision) and threshold = 0.75 * depth (full precision).
# Measurement rules (return):
#   * the reference file must hash to the value pinned below, and its baseline / S3 / proposal hashes must match;
#   * the intersection on the frozen entry and exit edges must reproduce the frozen chord endpoints within TOL_INTERSECT_CM
#     (1e-9 cm; a numerical tolerance for plane/edge interpolation only - vertex protection itself stays bit-exact);
#   * side rule (deterministic, identical to the 05U3 measurement): a vertex is on the negative side iff (x - O).d - s0 < 0,
#     otherwise (including exactly 0, e.g. the anchor vertex at build time) on the non-negative side; an edge crosses iff its
#     two vertices are on different sides;
#   * the run is walked face by face from the entry edge through region faces; a face with != 2 crossing edges, a non-region exit other than the frozen exit edge, a walk longer than MAX_STEPS, or any
#     non-finite value => explicit FAILED measurement (never a substitute section, moving chord or relaxed threshold);
#   * depth = max over run points of (p - A_) . n; PASS iff depth >= threshold.
import argparse, hashlib, json, math, os, sys, numpy as np, trimesh
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, '..', 'rmot05s_drivers')); import s_lib
VERSION = 'RM-OT-05U4-crease-ref-v1'; TOL_INTERSECT_CM = 1e-9; MAX_STEPS = 200
REF_SHA_PINNED = 'c1efefde5b50316b1ff4b2edaeae3fe702dc94b9722f52ba8da7f6d490772d51'   # crease_reference_v1.json (RM-OT-05U4); measure refuses any other reference
PINS = dict(s3_sha='1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c', baseline_sha='0989caf45cba8ddf0f44bdfba962671430c613bb752ac543d99d9b4b16420265',
            added_faces='483ab7feac190c76679eadc3ce677cd8e538349e2dc4842c6db0dfd441797692')
SECTIONS = (('A', 61581), ('B', 61580))
fH = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
H = lambda x: hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
def load_geo(Vs, ret):
    R = np.load(ret); i = R['s3_vid1'].astype(np.int64) - 1; V = Vs.copy(); Vr = R['V']
    if len(i) != len(Vs) or len(np.unique(i)) != len(Vs): raise ValueError('return is not a one-to-one S3 cover')
    mv = ~np.all(Vr == Vs[i].astype(np.float32), 1); V[i[mv]] = Vr[mv].astype(np.float64); return V
def region_of(Fs, prop):
    lab = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_face_labels.npy'); reg = (lab == 4) | (lab == 5)
    A = np.load(os.path.join(prop, 'proposal_sets.npz'))['added_faces']
    if H(A) != PINS['added_faces']: raise ValueError('added-face list hash mismatch')
    reg[A] = True; return reg
def edge_faces(Fs):
    e2f = {}
    for k, f in enumerate(Fs):
        for i in range(3): e2f.setdefault(tuple(sorted((int(f[i]), int(f[(i + 1) % 3])))), []).append(k)
    return e2f
def cross_pt(V, sd, e):
    a_, b_ = e; t = sd[a_] / (sd[a_] - sd[b_]); return V[a_] + t * (V[b_] - V[a_])
def walk(V, Fs, reg, e2f, sd, entry, exit_=None):
    """Walk from the entry edge through region faces along the plane. Returns (points, faces, exit_edge) or raises."""
    if not (np.isfinite(sd[list(entry)]).all()) or (sd[entry[0]] < 0) == (sd[entry[1]] < 0):
        raise ValueError('frozen entry edge does not cross the frozen plane')
    fs = [f for f in e2f[entry] if reg[f]]
    if len(fs) != 1: raise ValueError('entry edge is not a region boundary edge')
    pts = [cross_pt(V, sd, entry)]; faces = []; e = entry; f = fs[0]
    for _ in range(MAX_STEPS):
        tri = Fs[f]; s3 = sd[tri]
        if not np.isfinite(s3).all(): raise ValueError('non-finite geometry in walked face %d' % f)
        cr = [tuple(sorted((int(tri[i]), int(tri[(i + 1) % 3])))) for i in range(3) if (s3[i] < 0) != (s3[(i + 1) % 3] < 0)]
        if len(cr) != 2 or e not in cr: raise ValueError('face %d does not continue the section (crossing edges %s)' % (f, cr))
        e = cr[0] if cr[1] == e else cr[1]; faces.append(int(f)); pts.append(cross_pt(V, sd, e))
        nb = [g for g in e2f[e] if g != f]
        if len(nb) != 1: raise ValueError('non-manifold or boundary edge %s in walk' % (e,))
        if not reg[nb[0]]: return np.array(pts), faces, e
        f = nb[0]
    raise ValueError('walk exceeded %d steps' % MAX_STEPS)
def build(a):
    fr = s_lib.Frame('reviews/rac-rmot05q-evidence/plan/patch_selection.json')
    if fH(a.s3) != PINS['s3_sha'] or fH(a.baseline) != PINS['baseline_sha']: raise SystemExit('pinned S3 / baseline hash mismatch')
    s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); V = load_geo(Vs, a.baseline)
    reg = region_of(Fs, a.proposal); e2f = edge_faces(Fs); O = np.asarray(fr.O, float); d = np.asarray(fr.d, float)
    ref = dict(version=VERSION, index_convention='zero-based S3 vertex / face indices (rac_s3_vid1 = index + 1)',
               hashes=dict(s3_obj=PINS['s3_sha'], baseline_return_npz=PINS['baseline_sha'], proposal_sets_npz=fH(os.path.join(a.proposal, 'proposal_sets.npz')),
                           proposal_region_json=fH(os.path.join(a.proposal, 'proposal_region.json')), added_faces_list=PINS['added_faces']),
               frame=dict(O=O.tolist(), d=d.tolist()), tol_intersect_cm=TOL_INTERSECT_CM, sections={})
    for sid, anc in SECTIONS:
        s0 = float((V[anc] - O) @ d); sd = (V - O) @ d - s0
        # baseline component pick (build time only): among region boundary edges crossing the plane, take the pair whose walk
        # passes nearest the anchor
        cands = [e for e, fl in e2f.items() if len(fl) == 2 and reg[fl[0]] != reg[fl[1]] and (sd[e[0]] < 0) != (sd[e[1]] < 0)]
        runs = []
        for e in cands:
            try: P, faces, ex = walk(V, Fs, reg, e2f, sd, e); runs.append((float(np.linalg.norm(P - V[anc], axis=1).min()), e, ex, P, faces))
            except ValueError: pass
        runs.sort(key=lambda r: r[0]); _, ent, ex, P, faces = runs[0]
        both = [r for r in runs if {r[1], r[2]} == {ent, ex}]
        if len(both) != 2: raise SystemExit('section %s: entry/exit pair not unique' % sid)
        A_, B_ = P[0], P[-1]; u = (B_ - A_) / np.linalg.norm(B_ - A_); n = np.cross(d, u); n /= np.linalg.norm(n)
        if (O + s0 * d - A_) @ n < 0: n = -n
        dep = (P - A_) @ n; k = int(np.argmax(dep))
        ref['sections'][sid] = dict(anchor_s3_vertex=anc, s0_cm=s0, plane_normal=d.tolist(), entry_edge=list(ent), exit_edge=list(ex),
                                    entry_edge_frozen=True, chord_A=A_.tolist(), chord_B=B_.tolist(), chord_u=u.tolist(), inward_n=n.tolist(),
                                    baseline_run_faces=faces, baseline_depth_cm=float(dep[k]), baseline_deepest_point=P[k].tolist(), threshold_cm=0.75 * float(dep[k]),
                                    display=dict(s0=round(s0, 4), depth=round(float(dep[k]), 4), threshold=round(0.75 * float(dep[k]), 4)))
    ring = np.load(os.path.join(a.proposal, 'proposal_sets.npz'))['proposed_frozen_ring']
    for sid, s in ref['sections'].items():
        if not all(v in set(ring.tolist()) for v in s['entry_edge'] + s['exit_edge']): raise SystemExit('section %s endpoints not on frozen ring' % sid)
    body = json.dumps(ref, sort_keys=True, indent=1); open(a.out, 'w').write(body); print(json.dumps({k: v['display'] for k, v in ref['sections'].items()}), 'sha', fH(a.out))
def measure(a):
    res = dict(version=VERSION, reference=a.ref, status='FAILED_MEASUREMENT', sections={}, errors=[])
    try:
        if not os.path.exists(a.ref): raise ValueError('reference artifact missing')
        pinned = a.ref_sha or REF_SHA_PINNED
        if pinned is None or fH(a.ref) != pinned: raise ValueError('reference artifact hash mismatch (got %s)' % fH(a.ref))
        ref = json.load(open(a.ref))
        if ref.get('version') != VERSION: raise ValueError('reference version mismatch')
        if fH(a.s3) != ref['hashes']['s3_obj']: raise ValueError('S3 hash mismatch')
        if fH(os.path.join(a.proposal, 'proposal_sets.npz')) != ref['hashes']['proposal_sets_npz']: raise ValueError('proposal_sets hash mismatch')
        s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); V = load_geo(Vs, a.ret)
        reg = region_of(Fs, a.proposal); e2f = edge_faces(Fs); O = np.array(ref['frame']['O']); d = np.array(ref['frame']['d'])
        if set(ref['sections']) != {sid for sid, _ in SECTIONS}: raise ValueError('reference does not contain exactly sections A and B')
        for sid, _ in SECTIONS:
            s = ref['sections'][sid]; out = dict(section_id=sid, anchor_s3_vertex=s['anchor_s3_vertex'], s0_cm=s['s0_cm'], threshold_cm=s['threshold_cm'],
                                                 baseline_depth_cm=s['baseline_depth_cm'], fingerprint=hashlib.sha256(json.dumps(s, sort_keys=True).encode()).hexdigest())
            try:
                sd = (V - O) @ d - s['s0_cm']; P, faces, ex = walk(V, Fs, reg, e2f, sd, tuple(s['entry_edge']))
                if list(ex) != s['exit_edge']: raise ValueError('run exits through %s, frozen exit is %s' % (list(ex), s['exit_edge']))
                A_, B_ = np.array(s['chord_A']), np.array(s['chord_B']); n = np.array(s['inward_n'])
                ea, eb = float(np.abs(P[0] - A_).max()), float(np.abs(P[-1] - B_).max())
                if not (ea <= TOL_INTERSECT_CM and eb <= TOL_INTERSECT_CM): raise ValueError('chord endpoints moved (%.3g, %.3g cm)' % (ea, eb))
                dep = (P - A_) @ n
                if not np.isfinite(dep).all(): raise ValueError('non-finite depth')
                k = int(np.argmax(dep)); depth = float(dep[k])
                out.update(status='PASS' if depth >= s['threshold_cm'] else 'FAIL', depth_cm=depth, deepest_point=P[k].tolist(), run_faces=len(faces),
                           endpoint_deviation_cm=[ea, eb], display=dict(depth=round(depth, 4), threshold=round(s['threshold_cm'], 4)))
            except ValueError as e:
                out.update(status='FAILED_MEASUREMENT', error=str(e))
            res['sections'][sid] = out
        st = [res['sections'][sid]['status'] for sid, _ in SECTIONS]
        res['status'] = 'PASS' if all(x == 'PASS' for x in st) else ('FAILED_MEASUREMENT' if 'FAILED_MEASUREMENT' in st else 'FAIL')
    except (ValueError, KeyError, OSError) as e:
        res['errors'].append(str(e))
    json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps({'status': res['status'], **{k: (v['status'], v.get('display')) for k, v in res['sections'].items()}, 'errors': res['errors']}))
    return 0 if res['status'] == 'PASS' else 4
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['build', 'measure']); [ap.add_argument(k) for k in ('--s3', '--baseline', '--proposal', '--ret', '--ref', '--ref_sha', '--out')]
    a = ap.parse_args(); sys.exit(build(a) if a.mode == 'build' else measure(a))
