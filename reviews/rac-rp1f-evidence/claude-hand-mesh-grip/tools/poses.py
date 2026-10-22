# poses.py (bpy python) -- RIGDIR OUTDIR : drive the diagnostic hand rigs through the movement / grip schedule and check the
# actual evaluated (posed) geometry: self-intersections (claw vs skin, digit vs digit, local folds), fixture contact vs
# penetration, quad compression at joints, bone lengths and return-to-rest.
import sys, json, numpy as np, bpy, mathutils, os, pickle, math
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; rd = a[0]; out = a[1]; os.makedirs(out, exist_ok=True)
only = a[2].split(',') if len(a) > 2 else None
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend'))
RD = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20', 'A_Lthumb'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24', 'A_Rthumb']}
sc = bpy.context.scene

def evaluated(ob):
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); m = e.to_mesh()
    P = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get('co', P); e.to_mesh_clear(); return P.reshape(-1, 3)

def set_pose(ao, angles):
    """angles: {bone: (flex_deg, abd_deg, twist_deg)} about local X (flexion), Z (abduction), Y (twist)"""
    for pb in ao.pose.bones: pb.rotation_mode = 'XYZ'; pb.rotation_euler = (0, 0, 0)
    for b, (fx, ab, tw) in angles.items():
        if b in ao.pose.bones: ao.pose.bones[b].rotation_euler = (math.radians(fx), math.radians(tw), math.radians(ab))
    bpy.context.view_layer.update()

def selfx(P, Q, faces=None):
    Qs = Q if faces is None else Q[faces]
    t = BVHTree.FromPolygons(P.tolist(), Qs.tolist(), all_triangles=False, epsilon=0.0)
    pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr):
        A = Qs[pr[:, 0]]; B = Qs[pr[:, 1]]; share = (A[:, :, None] == B[:, None, :]).any((1, 2)); pr = pr[~share]
    if faces is not None and len(pr): pr = faces[pr]
    return pr

import igl
def pair_depths(P, Q, pairs, vq_ring):
    """penetration depth (m) per intersecting pair cluster: vertices of one side below the other side's local surface
    (pseudo-normal signed distance to the partner quads + one quad ring), both directions; returns array per pair"""
    if len(pairs) == 0: return np.zeros(0)
    d = np.zeros(len(pairs))
    C = P[Q[pairs[:, 0]]].mean(1)
    from scipy.spatial import cKDTree
    import scipy.sparse as sp_; from scipy.sparse.csgraph import connected_components as cc_
    e = np.array(list(cKDTree(C).query_pairs(0.004)), int).reshape(-1, 2); n = len(C)
    g = sp_.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)); _, lab = cc_(g, directed=False)
    for c in np.unique(lab):
        m = lab == c; A = np.unique(pairs[m, 0]); B = np.unique(pairs[m, 1]); best = 0.0
        for X_, Y_ in ((A, B), (B, A)):
            Yr = np.unique(np.concatenate([vq_ring[q] for q in Y_])); Yr = np.setdiff1d(Yr, X_)
            if len(Yr) == 0: continue
            T = np.vstack([Q[Yr][:, [0, 1, 2]], Q[Yr][:, [0, 2, 3]]])[:, ::-1]
            vs = np.unique(Q[X_])
            sd, _, _, _ = igl.signed_distance(P[vs], P, T, sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
            sd = sd[np.abs(sd) < 0.005]
            if len(sd) and sd.min() < 0: best = max(best, -sd.min())
        d[m] = best
    return d

def fixture_signed(P, fx):
    if fx is None: return None
    c = np.array(fx['c']); ax = np.array(fx['ax']); ax /= np.linalg.norm(ax); r = fx['r']; hl = fx['hl']
    d = P - c; t = d @ ax; radial = np.linalg.norm(d - t[:, None] * ax, axis=1)
    # signed distance to a capped cylinder (negative inside)
    dr = radial - r; dt = np.abs(t) - hl
    out_ = np.sqrt(np.maximum(dr, 0) ** 2 + np.maximum(dt, 0) ** 2); ins = np.minimum(np.maximum(dr, dt), 0)
    return out_ + ins

results = json.load(open(os.path.join(out, 'pose_results.json'))) if os.path.exists(os.path.join(out, 'pose_results.json')) else {}
SCHED = json.load(open(os.path.join(rd, 'schedule.json')))
for side in 'LR':
    ob = bpy.data.objects['GO_hand_%s_DIAG' % side]; ao = bpy.data.objects['GO_hand_%s_RIG' % side]
    me = ob.data; Q = np.zeros(len(me.polygons) * 4, int); me.polygons.foreach_get('vertices', Q); Q = Q.reshape(-1, 4)
    set_pose(ao, {}); P0 = evaluated(ob); ker = RD[side]['ker']; own = RD[side]['own']
    rest_pairs = selfx(P0, Q)
    L0 = {b.name: (b.tail_local - b.head_local).length for b in ao.data.bones}
    area0 = np.linalg.norm(np.cross(P0[Q[:, 1]] - P0[Q[:, 0]], P0[Q[:, 3]] - P0[Q[:, 0]]), axis=1)
    kerq = ker[Q].all(1); fown = np.array([np.bincount(own[q] + 1, minlength=6).argmax() - 1 for q in Q])
    def digit_of(b):
        for i_, k_ in enumerate(digs[side]):
            if b.startswith(k_ + '_'): return i_
        return -1
    def pairs_new(P):
        pr = selfx(P, Q); new = set(map(tuple, pr.tolist())) - rest_set; return np.array(sorted(new), int).reshape(-1, 2)
    rest_set = set(map(tuple, rest_pairs.tolist()))
    vq = [[] for _ in range(len(P0))]
    for qi, q in enumerate(Q):
        for v in q: vq[v].append(qi)
    vq_ring = [np.unique(np.concatenate([vq[v] for v in Q[qi]])) for qi in range(len(Q))] if False else None
    def ring_of(qi): return np.unique(np.concatenate([vq[v] for v in Q[qi]]))
    class _R:
        def __getitem__(self, qi): return ring_of(qi)
    vq_ring = _R()
    SKIN_TOL = SCHED.get('_tolerance', {}).get('skin_contact_mm', 1.0) / 1000.0
    CLAW_TOL = SCHED.get('_tolerance', {}).get('claw_contact_mm', 0.5) / 1000.0
    def violations(P, new):
        if len(new) == 0: return new, np.zeros(0)
        dep = pair_depths(P, Q, new, vq_ring)
        isclaw = kerq[new[:, 0]] | kerq[new[:, 1]]
        bad = np.where(isclaw, dep > CLAW_TOL, dep > SKIN_TOL)
        return new[bad], dep
    vown_q = fown
    for pname, spec in SCHED[side].items():
        if only and pname not in only: continue
        if spec.get('solve'):
            # clearance solver: per-digit flexion scale; digits involved in any new intersection (skin, claw, other
            # digits, palm, fixture penetration) are backed off by 8 % until the posed mesh is clean; digits of a fixture
            # pose advance until contact (|d| <= 0.5 mm) without penetration.
            fx = spec.get('fixture'); sc_ = {i_: 1.0 for i_ in range(5)}; log = []
            base = spec['angles']
            for it in range(60):
                ang = {b: tuple(sc_[digit_of(b)] * x for x in v) for b, v in base.items()}
                set_pose(ao, ang); P = evaluated(ob); new0 = pairs_new(P); new, _dep = violations(P, new0)
                inv = set(); prio = spec.get('yield', [])   # digits listed in 'yield' give way first (e.g. the thumb wraps last)
                for a_, b_ in new:
                    oa, ob2 = int(vown_q[a_]), int(vown_q[b_])
                    ya = digs[side][oa] in prio if oa >= 0 else False; yb = digs[side][ob2] in prio if ob2 >= 0 else False
                    if ya and not yb: inv.add(oa)
                    elif yb and not ya: inv.add(ob2)
                    else: inv.add(oa); inv.add(ob2)
                if fx:
                    sd = fixture_signed(P * 100, fx)
                    for i_ in range(5):
                        if (sd[own == i_] < -0.02).any(): inv.add(i_)
                inv.discard(-1)
                log.append(dict(it=it, pairs=int(len(new0)), violating=int(len(new)), scales={digs[side][i_]: round(sc_[i_], 3) for i_ in sc_}))
                if it == 0 or it % 10 == 0:
                    from collections import Counter
                    cnt = Counter(tuple(sorted((int(vown_q[a_]), int(vown_q[b_])))) for a_, b_ in new)
                    print('   it', it, 'violating by owner pair', dict(cnt), flush=True)
                if not new.size and not inv: break
                if not inv:  # only palm-palm pairs: back everything off
                    inv = set(range(5))
                for i_ in inv: sc_[i_] *= 0.92
            spec = dict(spec); spec['angles'] = {b: [sc_[digit_of(b)] * x for x in v] for b, v in base.items()}; spec['solver_log'] = log
            print(side, pname, 'solver', log[-1])
        steps = spec.get('steps', [1.0])
        rec = []
        for f in steps:
            ang = {b: tuple(f * x for x in v) for b, v in spec['angles'].items()}
            set_pose(ao, ang); P = evaluated(ob)
            new = pairs_new(P); viol, dep = violations(P, new)
            claw_pairs = int((kerq[new[:, 0]] | kerq[new[:, 1]]).sum()) if len(new) else 0
            cross_digit = int(((fown[new[:, 0]] != fown[new[:, 1]])).sum()) if len(new) else 0
            area = np.linalg.norm(np.cross(P[Q[:, 1]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 0]]), axis=1); okq = area0 > 0.05 * np.median(area0); ratio = (area / np.maximum(area0, 1e-12))[okq]
            fx = spec.get('fixture'); sd = fixture_signed(P * 100, fx) if fx else None
            isc = (kerq[new[:, 0]] | kerq[new[:, 1]]) if len(new) else np.zeros(0, bool)
            r = dict(step=f, new_selfx_pairs=int(len(new)), claw_pairs=claw_pairs, cross_digit_pairs=cross_digit,
                     violating_pairs=int(len(viol)), max_skin_contact_depth_mm=float(dep[~isc].max() * 1000) if (~isc).any() else 0.0,
                     max_claw_contact_depth_mm=float(dep[isc].max() * 1000) if isc.any() else 0.0,
                     area_ratio_p001=float(np.percentile(ratio, 0.1)), area_ratio_min=float(ratio.min()), area_ratio_max=float(ratio.max()))
            if sd is not None:
                r['fixture_min_signed_mm'] = float(sd.min() * 10); r['fixture_penetrating_vertices_gt0p5mm'] = int((sd < -0.05).sum())
                r['fixture_contact_vertices_le0p5mm'] = int((np.abs(sd) <= 0.05).sum())
                r['fixture_claw_penetrating'] = int(((sd < -0.05) & ker).sum())
            rec.append(r)
            if f == steps[-1]:
                Lp = {pb.name: (pb.tail - pb.head).length for pb in ao.pose.bones}
                r['posed_bone_length_change_max_mm'] = float(max(abs(Lp[k_] - L0[k_]) for k_ in L0) * 1000)
                np.save(os.path.join(out, '%s_%s_posed.npy' % (side, pname)), P.astype(np.float32))
                if len(new): np.save(os.path.join(out, '%s_%s_pairs.npy' % (side, pname)), new)
                if len(viol): np.save(os.path.join(out, '%s_%s_viol.npy' % (side, pname)), viol)
        # return to rest
        set_pose(ao, {}); Pr = evaluated(ob)
        L1 = {b.name: (b.tail_local - b.head_local).length for b in ao.data.bones}
        results['%s_%s' % (side, pname)] = dict(angles=spec['angles'], solver=spec.get('solver_log', [])[-1:] if spec.get('solve') else None, steps=rec, return_to_rest_max_mm=float(np.abs(Pr - P0).max() * 1000),
                                               bone_length_change_max_mm=float(max(abs(L1[k] - L0[k]) for k in L0) * 1000))
        print(side, pname, json.dumps(rec[-1]), 'rest dev mm %.6f' % results['%s_%s' % (side, pname)]['return_to_rest_max_mm'])
    results['%s_rest_selfx_pairs' % side] = int(len(rest_pairs))
json.dump(results, open(os.path.join(out, 'pose_results.json'), 'w'), indent=1)
