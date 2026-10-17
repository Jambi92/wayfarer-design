# RM-OT-05AN: 05AL bounded repair method driven by predict_an.py for the exact proposed Smooth Mesh Filter step (N Laplacian
# iterations, fade = 1 - saved mask; calibrated on a UI scratch: 1 mouse-move event = 1 iteration, corr 0.991).
# Flags: cumulative flips / >60 deg rotation vs the 05AL baseline (own reference for rotated triangles), adjacent >60 deg folds,
# new local inversions. Cap 0.5 mm from the CURRENT checkpoint. env: NITER, OUTNAME, BUDGET, MAXCYC
# RM-OT-05AL predictive limb-quality repair on the frozen 05AJ preflight baseline (bpy/bmesh, cloud workspace).
# Each cycle: predict (AK1-equivalent + 2x stress, predict2.py) -> 2-ring neighbourhoods around flagged faces (merged) ->
#   (a) relax: vertices of predicted-flip faces move by uniform-Laplacian half-steps (8 sweeps), capped 0.5 mm from the SOURCE position;
#   (b) near-coplanar edge rotations inside the neighbourhood union (05AI conditions: convex quad, diagonal absent, dihedral < 15 deg,
#       new triangles within the local plane, orientation preserved, worse-triangle quality improved by > 0.02).
# Protected vertices (05AF protected sets + 05AI torso / glute / pelvis_other) never move and no rotation may touch them.
# Max 3 cycles; budget 60 merged neighbourhoods (cumulative). Usage: python al_repair.py SRC.blend SHA MASK.npy OUTDIR
import sys, os, json, hashlib, numpy as np, bpy, bmesh
sys.path.insert(0, '/home/claude/an'); sys.path.insert(0, '/home/claude/al'); import predict_an as PA, predict2 as P, dryrun as DR
src, exp, mp, od = sys.argv[1:5]; os.makedirs(od, exist_ok=True); OUTNAME = os.environ.get('OUTNAME', 'GO-05AN_prep'); BUDGET = int(os.environ.get('BUDGET', '80')); NITER = int(os.environ.get('NITER', '100'))
assert hashlib.sha256(open(src, 'rb').read()).hexdigest() == exp
bpy.ops.wm.open_mainfile(filepath=src); o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data
M = np.load(mp); PZ = np.load('/home/claude/ag/protected_05AF.npz'); RZ = np.load('/home/claude/aj/regions_05AI.npz')
prot = PZ['all'] | RZ['torso'] | RZ['glute'] | RZ['pelvis_other']
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
V0 = np.array([v.co[:] for v in bm.verts]); n = len(V0)
def arrays():
    bm.faces.ensure_lookup_table(); V = np.array([v.co[:] for v in bm.verts]); F = np.array([[v.index for v in f.verts] for f in bm.faces]); return V, F
def q(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c); A = np.linalg.norm(np.cross(b - a, c - a)) / 2; s = ((b - a)**2).sum() + ((c - b)**2).sum() + ((a - c)**2).sum(); return 4 * np.sqrt(3) * A / s if s > 0 else 0
REF0 = None
def REF_KEEP(F, V):
    ref, isnew = PA.reference(F, V0); return ref
def PROPOSAL(F, Avg):
    kind = os.environ.get('PROPOSAL', 'smooth')
    if kind.startswith('inflate'):
        c = float(kind.split(':')[1])
        def f(X):
            fn = np.cross(X[F[:, 1]] - X[F[:, 0]], X[F[:, 2]] - X[F[:, 0]]); v = np.zeros_like(X)
            for i in range(3): np.add.at(v, F[:, i], fn)
            v /= np.maximum(np.linalg.norm(v, axis=1), 1e-30)[:, None]; return X + v * (c * (1 - M))[:, None]
        return f
    return lambda X: PA.laplace_iter(X, Avg, M, NITER)
import scipy.sparse as _sp
def RECLASS(r, V, F, S):
    # 05AO: a face counts as unstable only if it folds against its local surface: flips whose predicted 1-ring angle > 45 deg,
    # faces newly folded > 60 deg vs their 1-ring, and new local inversions. Surface reorientation (aligned < 30 deg) is not flagged.
    vf = _sp.csr_matrix((np.ones(F.size), (F.ravel(), np.repeat(np.arange(len(F)), 3))), shape=(len(V), len(F)))
    rv = PA.ringang(V, F, vf); rs = PA.ringang(S, F, vf)
    out = dict(flips=[f for f in r['flips'] if rs[f] > 45], near60=[int(f) for f in np.flatnonzero((rs > 60) & (rv <= 60))],
               adj=[], local_new_inversions=r['local_new_inversions'], raw_flips=len(r['flips']), raw_near60=len(r['near60']))
    return out
CAP = 5e-4; log = dict(cycles=[]); hood_all = np.zeros(n, bool); flagged_all = set(); rot_all = []; moved = {}
MAXCYC = int(os.environ.get('MAXCYC', '3'))
for cyc in range(1, MAXCYC + 2):
    V, F = arrays(); Avg = DR.adjacency(F, len(V)); ref, _ = PA.reference(F, V0) if cyc == 1 else (REF_KEEP(F, V), None); r = PA.predict(V, F, M, PROPOSAL(F, Avg), ref=ref); SS_ = r.pop('S'); r = RECLASS(r, V, F, SS_); r['stats'] = dict(median=float(np.median(np.linalg.norm(SS_ - V, axis=1)[np.linalg.norm(SS_ - V, axis=1) > 1e-5]) * 1000))
    entry = dict(cycle=cyc, prediction={k: v for k, v in r.items()}); log['cycles'].append(entry)
    print('cycle', cyc, {k: (len(v) if isinstance(v, list) else v) for k, v in r.items() if k != 'stats'}, flush=True)
    if not any(r[k] for k in ('flips','near60','local_new_inversions')): entry['result'] = 'ZERO_PREDICTED_FLIPS'; break
    if cyc == MAXCYC + 1: entry['result'] = 'CYCLE_LIMIT'; break
    flagged = sorted(set().union(*[set(r[k]) for k in ('flips','near60','adj','local_new_inversions')]))
    # neighbourhoods are defined on the current face list; record as face vertex triples (stable across rotations)
    groups, hood = P.neighbourhoods(F, flagged, n); hood &= ~prot; hood_all |= hood
    flagged_all |= set(tuple(sorted(F[f])) for f in flagged)
    allg, _ = P.neighbourhoods(F, [f for f in range(len(F)) if tuple(sorted(F[f])) in flagged_all], n)
    entry['neighbourhoods_this_cycle'] = len(groups); entry['neighbourhoods_cumulative'] = len(allg)
    if len(allg) > BUDGET: entry['result'] = 'BUDGET_EXCEEDED'; break
    # (a) relax flip-face vertices
    rel = sorted(set(int(x) for f in set().union(*[set(r[k]) for k in ('flips','near60','local_new_inversions')]) for x in F[f]) - set(np.flatnonzero(prot).tolist()))
    for it in range(8):
        newp = {}
        for vi in rel:
            v = bm.verts[vi]; nb = np.array([e.other_vert(v).co[:] for e in v.link_edges]); c = np.array(v.co[:])
            p = c + 0.5 * (nb.mean(0) - c); d = np.linalg.norm(p - V0[vi])
            if d > CAP: p = V0[vi] + (p - V0[vi]) * (CAP / d)
            newp[vi] = p
        for vi, p in newp.items(): bm.verts[vi].co = p.tolist(); moved[vi] = float(np.linalg.norm(p - V0[vi]))
    bm.normal_update()
    # (b) edge rotations inside the hood
    nrot = 0
    for sweep in range(20):
        ch = 0
        for e in list(bm.edges):
            if not e.is_valid or len(e.link_faces) != 2: continue
            f1, f2 = e.link_faces
            vs = set(v.index for f in (f1, f2) for v in f.verts)
            if not all(hood[i] for i in vs): continue
            a, b = e.verts; c = [v for v in f1.verts if v not in (a, b)][0]; d = [v for v in f2.verts if v not in (a, b)][0]
            if bm.edges.get([c, d]) is not None: continue
            if f1.normal.dot(f2.normal) < np.cos(np.radians(15)): continue
            old = min(q(a.co, b.co, c.co), q(a.co, b.co, d.co)); new = min(q(c.co, d.co, a.co), q(c.co, d.co, b.co))
            if new <= old + 0.02: continue
            nav = np.array(f1.normal) + np.array(f2.normal); nav /= np.linalg.norm(nav) + 1e-30
            A_, B_, C_, D_ = (np.array(x.co[:]) for x in (a, b, c, d)); side = lambda p, x, y: np.dot(np.cross(y - x, p - x), nav)
            if not (side(A_, C_, D_) * side(B_, C_, D_) < 0 and side(C_, A_, B_) * side(D_, A_, B_) < 0): continue
            m1 = np.cross(D_ - C_, A_ - C_); m2 = np.cross(D_ - C_, B_ - C_); m1 /= np.linalg.norm(m1) + 1e-30; m2 /= np.linalg.norm(m2) + 1e-30
            if abs(np.dot(m1, nav)) < 0.97 or abs(np.dot(m2, nav)) < 0.97: continue
            ne = bmesh.utils.edge_rotate(e, True)
            if ne is None: continue
            bm.normal_update(); nf = list(ne.link_faces)
            ok = len(nf) == 2 and all(np.dot(np.array(f.normal), nav) > 0.95 for f in nf) and nf[0].normal.dot(nf[1].normal) > np.cos(np.radians(15))
            if not ok:
                if bmesh.utils.edge_rotate(ne, False) is None: raise RuntimeError('revert failed')
                bm.normal_update(); continue
            rot_all.append(dict(cycle=cyc, edge_was=[a.index, b.index], edge_now=[c.index, d.index], q_old=round(float(old), 4), q_new=round(float(new), 4))); ch += 1; nrot += 1
        if not ch: break
    entry['relaxed_vertices'] = len(rel); entry['edge_rotations'] = nrot
V1, F1 = arrays(); dv = np.linalg.norm(V1 - V0, axis=1)
assert set(np.flatnonzero(dv > 0)) <= set(np.flatnonzero(hood_all)), 'movement outside hood'
assert dv[prot].max() == 0
bm.to_mesh(me); bm.free(); me.update()
me.calc_loop_triangles(); T = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get('vertices', T)
Vw = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', Vw)
np.savez(os.path.join(od, 'after_VF.npz'), V=Vw.reshape(-1, 3), F=T.reshape(-1, 3)); np.save(os.path.join(od, 'hood_vertices.npy'), np.flatnonzero(hood_all))
out = os.path.join(od, OUTNAME + '.blend'); bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
bpy.ops.export_scene.gltf(filepath=out.replace('.blend', '.glb'), export_format='GLB')
log.update(source_sha256=exp, hood_vertices=int(hood_all.sum()), vertices_moved={str(k): round(v * 1000, 4) for k, v in sorted(moved.items()) if v > 0},
           max_vertex_move_mm=round(float(dv.max() * 1000), 4), edge_rotations=rot_all,
           blend_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(), glb_sha256=hashlib.sha256(open(out.replace('.blend', '.glb'), 'rb').read()).hexdigest())
json.dump(log, open(os.path.join(od, 'al_repair_log.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in log.items() if k not in ('cycles', 'edge_rotations', 'vertices_moved')}, indent=1))
print([(c['cycle'], c.get('result'), c.get('neighbourhoods_cumulative'), c.get('relaxed_vertices'), c.get('edge_rotations')) for c in log['cycles']])
