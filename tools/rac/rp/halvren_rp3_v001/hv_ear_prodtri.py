# hv_ear_prodtri.py SNAP.npz HEAD LABEL OUTDIR [REBUILD.npz|-] [POSEPREFIX|-]   (bpy python, /home/claude/stc/bin/python3)
# Halvren ear family final production triangulation / shading gate (order chatgpt-rac-rp3-halvren-ear-final-production-triangulation-gate-order.md).
# Validation only: the approved vertex positions and quad connectivity of SNAP are never modified.
#   §4  production triangulation rule TRI-HV1 (below) on every quad; flagged quads (folded = the two diagonal splits disagree in orientation, the
#       folded-quad audit metric; or strongly warped = fold across the chosen diagonal > 20 deg) on the ear branch: chosen vs alternate diagonal, triangle
#       normals, surface deviation between the two splits, min angle / aspect, vertex-normal imprint, defect flags; order-invariance; rebuild identity
#   §5  smooth (angle-weighted) vertex normals on the baked triangles (Blender corner normals, no sharp edges = one smoothing group), MikkTSpace tangents
#       (Blender calc_tangents) on a deterministic projected audit UV (the production UV unwrap is not part of this gate)
#   §6  the 8 head / neck poses (posed positions from ear_deform.py on SNAP) evaluated on the baked triangles
#   §7  LOD 50 / 25 % (Decimate collapse of the baked triangulated mesh, as the closure prodcheck) -- manifoldness, zero area, self-intersection,
#       drift (source <-> LOD, ear / root / flagged regions)
#   §8  FBX export (baked triangles, normals, tangent space) -> reimport: positions, triangles, normals, tangents; quad export + importer
#       triangulation emulation (FIXED 0-2 / BEAUTY / SHORT_EDGE) vs the baked rule; left / right sheet mirroring of the diagonal choice; root seam
# TRI-HV1 (deterministic, geometry-only, evaluated ONCE on the approved rest pose and BAKED into the asset; never re-evaluated per pose / at import):
#   for quad (a, b, c, d): split A = (a,b,c)+(a,c,d) [diagonal a-c], split B = (a,b,d)+(b,c,d) [diagonal b-d];
#   1. the split with the smaller fold angle between its two triangle normals, if the folds differ by > 0.5 deg;
#   2. else the split with the larger minimum triangle angle, if they differ by > 0.5 deg;
#   3. else the shorter diagonal (> 1e-9 cm); 4. else the diagonal holding the smallest vertex index.  Triangles keep the quad winding.
import sys, os, json, hashlib, tempfile, numpy as np
import bpy, bmesh, addon_utils
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.environ.setdefault('EAR_TOPO', 'v002')
import hv_ear_domains as D
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
SNAP, HEAD, LAB, OUT = a[:4]; RB = a[4] if len(a) > 4 and a[4] != '-' else None; PP = a[5] if len(a) > 5 and a[5] != '-' else None
os.makedirs(OUT, exist_ok=True)
z = np.load(SNAP); V = z['V'].astype(float); Q = np.asarray(z['Q']).astype(np.int64); part = z['part']; side = z['side']; rec = json.load(open(SNAP.replace('.npz', '.json')))
nV, nQ = len(V), len(Q); R = dict(label=LAB, head=HEAD, snapshot=SNAP, snapshot_V_float32_sha256=hashlib.sha256(z['V'].astype(np.float32).tobytes()).hexdigest())
deg = lambda c: np.degrees(np.arccos(np.clip(c, -1, 1)))

# ---------------- triangle helpers
def tnorm(X, T):
    n = np.cross(X[T[:, 1]] - X[T[:, 0]], X[T[:, 2]] - X[T[:, 0]]); L = np.linalg.norm(n, axis=1); return n / np.maximum(L, 1e-30)[:, None], 0.5 * L
def tang(X, T):
    out = []
    for k in range(3):
        u = X[T[:, (k + 1) % 3]] - X[T[:, k]]; w = X[T[:, (k + 2) % 3]] - X[T[:, k]]
        out.append(deg((u * w).sum(1) / (np.linalg.norm(u, axis=1) * np.linalg.norm(w, axis=1) + 1e-30)))
    return np.stack(out, 1)
def tasp(X, T):
    L = np.stack([np.linalg.norm(X[T[:, (k + 1) % 3]] - X[T[:, k]], axis=1) for k in range(3)], 1); return L.max(1) / np.maximum(L.min(1), 1e-30)
SPL = {0: ([0, 1, 2], [0, 2, 3]), 1: ([0, 1, 3], [1, 2, 3])}
def split_metrics(X, Qs):
    m = {}
    for s, (i1, i2) in SPL.items():
        T1, T2 = Qs[:, i1], Qs[:, i2]; n1, a1 = tnorm(X, T1); n2, a2 = tnorm(X, T2); ang = np.minimum(tang(X, T1).min(1), tang(X, T2).min(1))
        m[s] = dict(n1=n1, n2=n2, fold=deg((n1 * n2).sum(1)), minang=ang, asp=np.maximum(tasp(X, T1), tasp(X, T2)), area_min=np.minimum(a1, a2),
                    dlen=np.linalg.norm(X[Qs[:, 2 if s == 0 else 3]] - X[Qs[:, 0 if s == 0 else 1]], axis=1))
    return m
def rule(X, Qs):
    m = split_metrics(X, Qs); fA, fB = m[0]['fold'], m[1]['fold']; aA, aB = m[0]['minang'], m[1]['minang']; dA, dB = m[0]['dlen'], m[1]['dlen']
    tie = np.where(np.minimum(Qs[:, 0], Qs[:, 2]) < np.minimum(Qs[:, 1], Qs[:, 3]), 0, 1)
    c = np.where(fA < fB - 0.5, 0, np.where(fB < fA - 0.5, 1, np.where(aA > aB + 0.5, 0, np.where(aB > aA + 0.5, 1, np.where(dA < dB - 1e-9, 0, np.where(dB < dA - 1e-9, 1, tie))))))
    return c, m
def tris(Qs, c):
    T = np.empty((2 * len(Qs), 3), np.int64); A = c == 0
    T[0::2][A], T[1::2][A] = Qs[A][:, [0, 1, 2]], Qs[A][:, [0, 2, 3]]; T[0::2][~A], T[1::2][~A] = Qs[~A][:, [0, 1, 3]], Qs[~A][:, [1, 2, 3]]; return T
def diag(Qs, c): return np.where((c == 0)[:, None], np.sort(Qs[:, [0, 2]], 1), np.sort(Qs[:, [1, 3]], 1))
def vnormals_sum(X, T):
    n, _ = tnorm(X, T); ang = np.radians(tang(X, T)); S = np.zeros((len(X), 3))
    for k in range(3): np.add.at(S, T[:, k], n * ang[:, k:k + 1])
    return S
unit = lambda v: v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-30)

# ---------------- §4 production triangulation
c, M = rule(V, Q); tq = np.repeat(np.arange(nQ), 2); br = (part[Q] != 'v005').any(1)
# step 5 -- intersection validation of the bake (authoring time): triangles of the ear neighbourhood (14 cm, as ear_deform) are checked for crossings
# touching the branch at rest and in the 8 head / neck poses; a quad whose baked triangles take part in a crossing that the other diagonal does not
# have is flipped (greedy, quads in index order, accepted only if the total crossing count over all states drops); repeated until stable
near14 = np.zeros(nV, bool)
for s_ in ('l', 'r'): near14 |= np.linalg.norm(V - V[side == s_].mean(0), axis=1) < 14
STATES = [('rest', V)]
if PP:
    for pn in json.load(open(PP + '_deform.json'))['poses']: STATES.append((pn, np.load('%s_%s.npy' % (PP, pn)).astype(float)))
nearT = np.nonzero(np.repeat(near14[Q].all(1), 2))[0]; brT2 = np.repeat(br, 2)
def crossings_all(cc, states=None):
    TT = tris(Q, cc)[nearT]; out = {}
    for nm, X in (states or STATES):
        b_ = BVHTree.FromPolygons(X.tolist(), TT.tolist(), all_triangles=True, epsilon=0.0); st = set()
        for i, j in b_.overlap(b_):
            gi, gj = nearT[i], nearT[j]
            if (brT2[gi] or brT2[gj]) and not (set(TT[i]) & set(TT[j])): st.add((min(gi, gj), max(gi, gj)))
        out[nm] = st
    return out
def total(cr): return sum(len(v) for v in cr.values())
def step5(c, states=None):
    cr = crossings_all(c, states); flipped = []; it5 = 0; c = c.copy()
    for it5 in range(6):
        badq = sorted({int(tq[t]) for st in cr.values() for pr in st for t in pr if br[tq[t]]})
        if not badq: break
        changed = False
        for f in badq:
            c2 = c.copy(); c2[f] = 1 - c2[f]; cr2 = crossings_all(c2, states)
            if total(cr2) < total(cr): c, cr, changed = c2, cr2, True; flipped.append(int(f))
        if not changed: break
    return c, cr, flipped, it5 + 1
c0 = c.copy(); crA = crossings_all(np.zeros(nQ, np.int64)); cr0 = crossings_all(c0); c, cr, flipped, nit = step5(c0)
R['intersection_validation'] = dict(states=[k for k, _ in STATES], fixed_split_ac_crossings={k: len(v) for k, v in crA.items() if v}, rule_steps1_4_crossings={k: len(v) for k, v in cr0.items() if v},
                                    flipped_quads=flipped, final_crossings={k: len(v) for k, v in cr.items() if v}, iterations=nit,
                                    note='crossings = triangle pairs touching the branch that intersect and share no vertex (stricter than the quad audit, which ignores triangles of vertex-adjacent quads)')
T = tris(Q, c); DG = diag(Q, c); alt = 1 - c
folded = ((M[0]['n1'] * M[0]['n2']).sum(1) < 0) | ((M[1]['n1'] * M[1]['n2']).sum(1) < 0)
chosen = lambda key: np.where(c == 0, M[0][key], M[1][key]); other = lambda key: np.where(c == 0, M[1][key], M[0][key])
fold_c, fold_a = chosen('fold'), other('fold'); warped = fold_c > 20.0
flag = br & (folded | warped); FL = np.nonzero(flag)[0]
# order invariance: cyclic shifts and reversed winding give the same diagonal set
inv = {}
for nm, Qx in (('shift1', np.roll(Q, 1, 1)), ('shift2', np.roll(Q, 2, 1)), ('shift3', np.roll(Q, 3, 1)), ('reversed', Q[:, ::-1])):
    cx, _ = rule(V, Qx); inv[nm] = int((diag(Qx, cx) != diag(Q, c0)).any(1).sum())
R['order_invariance_mismatched_quads'] = dict(inv, note='steps 1-4 (geometry-only) under cyclic shifts / reversed winding of every quad; step 5 visits quads in the frozen index order')
# regions
v2b = z['v005_to_branch']; loopv = set()
for s_ in ('l', 'r'): loopv |= set(v2b[np.array(rec['sides'][s_]['root_loop_v005'])].tolist())
loopm = np.isin(Q, list(loopv)).any(1); hn = np.full(nV, np.nan); fr = {}
for s_ in ('l', 'r'):
    rd = D.frame(HEAD, s_); O, u = rd['O'], rd['u']; sv = np.nonzero((side == s_) & np.isin(part, ['front', 'back', 'rim']))[0]; h = (V[sv] - O) @ u
    hn[sv] = (h - h.min()) / (h.max() - h.min()); fr[s_] = rd
def region(f):
    p = set(part[Q[f]].tolist())
    if loopm[f] and p & {'cuff', 'transition'}: return 'root_junction'
    if 'cuff' in p: return 'cuff'
    if 'transition' in p: return 'transition'
    if p <= {'front', 'back', 'rim'}:
        m_ = np.nanmean(hn[Q[f]]); return 'lobe_junction' if m_ < 0.22 else ('upper_helix_tip' if m_ > 0.80 else 'auricle_sheet')
    if p & {'front', 'back', 'rim'}: return 'sheet_cuff_seam'
    return 'head_ring'
REG = np.array([region(f) if br[f] else '' for f in range(nQ)], dtype=object)
fside = np.array([(set(side[Q[f]].tolist()) - {''} or {'-'}).pop() for f in range(nQ)])
R['intersection_validation']['flipped_regions'] = [str(REG[f]) for f in flipped]
# shading: angle-weighted vertex normals on the baked triangles; local diagonal swap for the alternate
S0 = vnormals_sum(V, T); VN = unit(S0); nT, aT = tnorm(V, T)
def tri_break(n, Tt, VNx): return max(float(deg(n[i] @ VNx[Tt[i, k]])) for i in range(len(Tt)) for k in range(3))
def seg_dist(p0, p1, q0, q1):
    d1, d2, r = p1 - p0, q1 - q0, p0 - q0; a_, e_, f_ = d1 @ d1, d2 @ d2, d2 @ r; c_, b_ = d1 @ r, d1 @ d2; den = a_ * e_ - b_ * b_
    s = np.clip((b_ * f_ - c_ * e_) / den, 0, 1) if den > 1e-18 else 0.0; t = np.clip((b_ * s + f_) / e_, 0, 1); s = np.clip((b_ * t - c_) / a_, 0, 1)
    return float(np.linalg.norm((p0 + d1 * s) - (q0 + d2 * t)))
rows = []; vis_flags = {k: 0 for k in ('normal_flip', 'sliver', 'ridge_or_dent', 'shading_discontinuity', 'imprint')}
for f in FL:
    q = Q[f]; Tc = T[2 * f:2 * f + 2]; Ta = tris(q[None], np.array([alt[f]])); nc_, _ = tnorm(V, Tc); na_, _ = tnorm(V, Ta)
    Sa = S0.copy(); ang_c = np.radians(tang(V, Tc)); ang_a = np.radians(tang(V, Ta))
    for k in range(3): np.add.at(Sa, Tc[:, k], -nc_ * ang_c[:, k:k + 1]); np.add.at(Sa, Ta[:, k], na_ * ang_a[:, k:k + 1])
    VNa = unit(Sa); imprint = float(deg((VN[q] * VNa[q]).sum(1)).max())
    dev = seg_dist(V[q[0]], V[q[2]], V[q[1]], V[q[3]]); el = float(np.mean([np.linalg.norm(V[q[k]] - V[q[(k + 1) % 4]]) for k in range(4)]))
    brk_c, brk_a = tri_break(nc_, Tc, VN), tri_break(na_, Ta, VNa); flip_c = bool(min((nc_[i] @ unit(VN[Tc[i]].sum(0))) for i in range(2)) < 0)
    mc, ma = float(chosen('minang')[f]), float(other('minang')[f])
    fl = dict(normal_flip=flip_c, sliver=mc < 5.0, ridge_or_dent=bool(fold_c[f] > 60.0 and dev / el > 0.15), shading_discontinuity=brk_c > 45.0, imprint=imprint > 20.0)
    for k, v in fl.items(): vis_flags[k] += int(v)
    rows.append(dict(quad=int(f), side=str(fside[f]), region=str(REG[f]), folded=bool(folded[f]), chosen_diagonal=[int(x) for x in DG[f]],
                     alternate_diagonal=[int(x) for x in diag(q[None], np.array([alt[f]]))[0]], fold_chosen_deg=round(float(fold_c[f]), 2), fold_alternate_deg=round(float(fold_a[f]), 2),
                     surface_deviation_cm=round(dev, 4), deviation_over_edge=round(dev / el, 3), min_angle_chosen=round(mc, 2), min_angle_alternate=round(ma, 2),
                     aspect_chosen=round(float(chosen('asp')[f]), 2), aspect_alternate=round(float(other('asp')[f]), 2), normal_break_chosen_deg=round(brk_c, 2),
                     normal_break_alternate_deg=round(brk_a, 2), vertex_normal_imprint_deg=round(imprint, 2), flags=[k for k, v in fl.items() if v]))
R['triangulation'] = dict(rule='TRI-HV1', quads=nQ, triangles=int(len(T)), branch_quads=int(br.sum()), branch_split_A_ac=int((c[br] == 0).sum()), branch_split_B_bd=int((c[br] == 1).sum()),
                          decided_by=dict(fold=int((np.abs(M[0]['fold'] - M[1]['fold']) > 0.5)[br].sum()), other=int((np.abs(M[0]['fold'] - M[1]['fold']) <= 0.5)[br].sum())),
                          branch_tri_min_angle=round(float(tang(V, T[np.repeat(br, 2)]).min()), 2), branch_tri_max_aspect=round(float(tasp(V, T[np.repeat(br, 2)]).max()), 2),
                          triangles_sha256=hashlib.sha256(T.tobytes()).hexdigest())
R['flagged'] = dict(count=len(FL), folded=int((flag & folded).sum()), warped_only=int((flag & ~folded).sum()),
                    by_region={k: int(v) for k, v in zip(*np.unique(REG[FL].astype(str), return_counts=True))} if len(FL) else {},
                    fold_chosen_max=round(float(fold_c[FL].max()), 2) if len(FL) else 0, fold_alternate_of_folded_min=round(float(fold_a[flag & folded].min()), 2) if (flag & folded).any() else None,
                    deviation_max_cm=max([r['surface_deviation_cm'] for r in rows] or [0]), min_angle_chosen_min=min([r['min_angle_chosen'] for r in rows] or [90]),
                    normal_break_chosen_max=max([r['normal_break_chosen_deg'] for r in rows] or [0]), imprint_max=max([r['vertex_normal_imprint_deg'] for r in rows] or [0]),
                    defect_flags=vis_flags, quads=rows)
# rebuild identity
if RB:
    zb = np.load(RB); Vb = zb['V'].astype(float); Qb = np.asarray(zb['Q']).astype(np.int64); cb, _ = rule(Vb, Qb); cb, _, _, _ = step5(cb, [('rest', Vb)] + STATES[1:]); Tb = tris(Qb, cb)
    R['rebuild'] = dict(path=RB, max_abs_dV_cm=float(np.abs(Vb - V).max()), quads_identical=bool(np.array_equal(Qb, Q)), triangles_identical=bool(np.array_equal(Tb, T)))

# ---------------- Blender mesh: baked triangles, smooth, audit UV, corner normals, MikkTSpace tangents
addon_utils.enable('io_scene_fbx', default_set=True)
def audit_uv(X):
    U = np.zeros((len(X), 2)); Hc = np.array([0.0, X[part == 'v005'][:, 1].mean(), X[:, 2].max() - 12.0]); d = X - Hc
    U[:, 0] = np.arctan2(d[:, 0], -d[:, 1]) / (2 * np.pi) * 3.0; U[:, 1] = d[:, 2] / 30.0                        # head: cylindrical
    for s_, rd in fr.items():
        k = side == s_; U[k, 0] = 0.6 + 0.4 * (s_ == 'r') + ((X[k] - rd['O']) @ rd['b']) / 25.0; U[k, 1] = 0.5 + ((X[k] - rd['O']) @ rd['u']) / 25.0   # ear: root-frame plane
    return U
SMART = True
def mkmesh(X, TT, name='m'):
    bpy.ops.wm.read_factory_settings(use_empty=True); me = bpy.data.meshes.new(name); me.from_pydata((X / 100).tolist(), [], TT.tolist()); me.update()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); uv = me.uv_layers.new(name='UV'); lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
    uv.data.foreach_set('uv', audit_uv(X)[lv].astype(np.float32).ravel()); me.update(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    if SMART:                                                       # production-like UV islands: Smart UV Project (66 deg), deterministic
        bpy.context.view_layer.objects.active = ob; ob.select_set(True); bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=np.radians(66.0), island_margin=0.0); bpy.ops.object.mode_set(mode='OBJECT')
    return ob
def corner_data(me):
    lv = np.empty(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv); global UVL; UVL = np.empty(len(me.loops) * 2, np.float32); me.uv_layers['UV'].data.foreach_get('uv', UVL); UVL = UVL.reshape(-1, 2); cn = np.empty(len(me.loops) * 3, np.float32); me.corner_normals.foreach_get('vector', cn)
    me.calc_tangents(uvmap='UV'); tg = np.empty(len(me.loops) * 3, np.float32); me.loops.foreach_get('tangent', tg); sg = np.empty(len(me.loops), np.float32); me.loops.foreach_get('bitangent_sign', sg)
    return lv, cn.reshape(-1, 3), tg.reshape(-1, 3), sg
ob = mkmesh(V, T); lv, CN, TG, SG = corner_data(ob.data)
brv = np.zeros(nV, bool); brv[Q[br].ravel()] = True; bl = brv[lv]; flv = np.zeros(nV, bool); flv[Q[FL].ravel()] = True; fl_l = flv[lv]
cn_vs_np = float(deg((CN.astype(float) * VN[lv]).sum(1))[bl].max())
tl = np.linalg.norm(TG, axis=1)
# tangent sign consistency: loops of one vertex sharing the sign; tangent spread between the loops of one vertex
spread = np.zeros(nV); signmix = np.zeros(nV, bool)
order_ = np.argsort(lv, kind='stable'); lvs = lv[order_]; cuts = np.r_[0, np.nonzero(np.diff(lvs))[0] + 1, len(lvs)]
for i in range(len(cuts) - 1):
    idx = order_[cuts[i]:cuts[i + 1]]; v = lvs[cuts[i]]
    if not brv[v]: continue
    uk = np.round(UVL[idx] * 1e5).astype(np.int64); grp = {}
    for j, kk in zip(idx, map(tuple, uk)): grp.setdefault(kk, []).append(j)
    for g in grp.values():
        if len(g) < 2: continue
        t0 = TG[g]; spread[v] = max(spread[v], float(deg((unit(t0) @ unit(t0.mean(0))).min()))); signmix[v] |= len(set(np.sign(SG[g]).tolist())) > 1
R['normals_tangents'] = dict(normals='smooth angle-weighted vertex normals on the baked triangles (Blender corner normals; no sharp edges / one smoothing group)',
                             blender_vs_numpy_vertex_normal_max_deg_branch=round(cn_vs_np, 4), tangents='MikkTSpace (Blender calc_tangents) on a production-like Smart UV Project unwrap (66 deg islands; the final production UV is outside this gate); spread / sign measured among the loops of a vertex that share one UV (seams excluded)',
                             degenerate_or_nan_tangents_branch=int(((tl < 0.5) | ~np.isfinite(tl))[bl].sum()), tangent_spread_per_vertex_max_deg_branch=round(float(spread[brv].max()), 2),
                             tangent_spread_per_vertex_max_deg_flagged=round(float(spread[flv].max()), 2) if flv.any() else 0.0,
                             bitangent_sign_mixed_vertices_branch=int(signmix[brv].sum()), bitangent_sign_mixed_vertices_flagged=int(signmix[flv].sum()))
# quad-normal vs baked-triangle normal (diagonal imprint over the whole branch) and what importer re-triangulations would do
Squad = np.zeros((nV, 3)); nq = unit(np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]))
qa = np.stack([deg((unit(V[Q[:, (k + 1) % 4]] - V[Q[:, k]]) * unit(V[Q[:, (k - 1) % 4]] - V[Q[:, k]])).sum(1)) for k in range(4)], 1)
for k in range(4): np.add.at(Squad, Q[:, k], nq * np.radians(qa[:, k:k + 1]))
R['normals_tangents']['quad_vs_baked_triangle_vertex_normal_max_deg_branch'] = round(float(deg((unit(Squad) * VN).sum(1))[brv].max()), 2)
def bm_tri(method):
    bm = bmesh.new(); [bm.verts.new(p) for p in (V / 100)]; bm.verts.ensure_lookup_table(); [bm.faces.new([bm.verts[i] for i in q]) for q in Q]; bm.faces.ensure_lookup_table()
    r_ = bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=method, ngon_method='BEAUTY'); dd = np.zeros((nQ, 2), np.int64)
    fm = r_['face_map']; byq = {}
    for tf, of in fm.items(): byq.setdefault(of.index, []).append(tf)
    for qi in range(nQ):
        ts = byq.get(qi, []); vs = [set(v.index for v in t.verts) for t in ts]
        if len(vs) == 2: dd[qi] = sorted(vs[0] & vs[1])
        else: dd[qi] = DG[qi]
    bm.free(); return dd
imp = {}
for meth in ('FIXED', 'BEAUTY', 'SHORT_EDGE'):
    dd = bm_tri(meth); diff = (dd != DG).any(1); dv = [seg_dist(V[Q[f][0]], V[Q[f][2]], V[Q[f][1]], V[Q[f][3]]) for f in np.nonzero(diff & flag)[0]]
    imp[meth] = dict(branch_quads_differing=int((diff & br).sum()), flagged_quads_differing=int((diff & flag).sum()), flagged_max_surface_change_cm=round(max(dv or [0]), 4),
                     flagged_differing_into_folded_split=int(((diff & flag) & (other('fold') > 90)).sum()))
R['importer_retriangulation_if_exported_as_quads'] = imp

# ---------------- §8 FBX export / reload (baked triangles) + mirroring + root seam
fbx = os.path.join(tempfile.mkdtemp(), LAB + '.fbx')
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, mesh_smooth_type='OFF', use_tspace=True, use_triangles=True, add_leaf_bones=False, bake_anim=False)
bpy.ops.wm.read_factory_settings(use_empty=True); addon_utils.enable('io_scene_fbx', default_set=True); bpy.ops.import_scene.fbx(filepath=fbx)
ob2 = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]; me2 = ob2.data; Mw = np.array(ob2.matrix_world)
P2 = np.array([v.co[:] for v in me2.vertices]); P2 = (np.c_[P2, np.ones(len(P2))] @ Mw.T)[:, :3] * 100; F2 = np.array([list(p.vertices) for p in me2.polygons])
lv2, CN2, TG2, SG2 = corner_data(me2); Rm = Mw[:3, :3] / np.linalg.norm(Mw[:3, 0]); CN2w = unit(CN2.astype(float) @ Rm.T); TG2w = unit(TG2.astype(float) @ Rm.T)
same_loops = bool(np.array_equal(lv2, lv))
R['export_fbx'] = dict(file_bytes=os.path.getsize(fbx), vertices_equal=len(P2) == nV, max_abs_dV_cm=float(np.abs(P2 - V).max()) if len(P2) == nV else None,
                       triangles_identical=bool(F2.shape == T.shape and np.array_equal(F2, T)), loop_order_identical=same_loops,
                       normal_max_deg_branch=round(float(deg((CN2w * CN.astype(float)).sum(1))[bl].max()), 4) if same_loops else None,
                       tangent_recomputed_max_deg_branch=round(float(deg((TG2w * unit(TG.astype(float))).sum(1))[bl].max()), 4) if same_loops else None,
                       bitangent_sign_identical=bool(np.array_equal(SG2, SG)) if same_loops else None)
# root seam: boundary / non-manifold edges inside the ear neighbourhood of the reloaded mesh
from collections import Counter
ec = Counter(tuple(sorted((int(t[k]), int(t[(k + 1) % 3])))) for t in F2 for k in range(3)); bnd = [e for e, n in ec.items() if n != 2]
nearv = np.zeros(nV, bool)
for s_ in ('l', 'r'): nearv |= np.linalg.norm(V - V[side == s_].mean(0), axis=1) < 8
R['export_fbx']['ear_region_boundary_or_nonmanifold_edges'] = int(sum(1 for e in bnd if nearv[e[0]] or nearv[e[1]]))
# mirroring of the diagonal choice on the auricle sheet (one layout order per side; the cuff transitions are canonical per side)
E_ = D.E; ns = len(E_.canonical_layout()['st']); l0 = int(np.nonzero(side == 'l')[0][0]); r0 = int(np.nonzero(side == 'r')[0][0])
inL = ((Q >= l0) & (Q < l0 + ns)).all(1); inR = ((Q >= r0) & (Q < r0 + ns)).all(1); key = {tuple(sorted(q.tolist())): i for i, q in enumerate(Q) if inR[i]}
mis = tot = misfl = 0
for i in np.nonzero(inL)[0]:
    j = key.get(tuple(sorted((Q[i] - l0 + r0).tolist())))
    if j is None: continue
    tot += 1; d_ = set((DG[i] - l0 + r0).tolist()) != set(DG[j].tolist()); mis += d_; misfl += d_ and (flag[i] or flag[j])
R['mirroring'] = dict(sheet_quad_pairs=tot, diagonal_choice_mismatched=int(mis), mismatched_among_flagged=int(misfl), cuff='per-side canonical transitions (Fenn / Vael cuff canon): not a mirror pair')

# ---------------- §6 poses on the baked triangles
POSE = {}
if PP:
    dj = json.load(open(PP + '_deform.json')); near_t = np.nonzero(nearv[T].all(1))[0]; TT = T[near_t]; tbr = np.repeat(br, 2)[near_t]
    def selfx(X):
        b_ = BVHTree.FromPolygons(X.tolist(), TT.tolist(), all_triangles=True, epsilon=0.0); bad = set()
        for i, j in b_.overlap(b_):
            if (tbr[i] or tbr[j]) and not (set(TT[i]) & set(TT[j])): bad.add((min(i, j), max(i, j)))
        return bad
    SX0 = selfx(V); R['rest_contacts_touching_branch_on_baked_triangles'] = len(SX0); nb = [set() for _ in range(nV)]
    for t in T[np.repeat(br, 2)]:
        for k in range(3): nb[t[k]].update(t.tolist())
    brT = np.nonzero(np.repeat(br, 2))[0]; band = np.nonzero(np.repeat(loopm & br, 2))[0]; flT = np.r_[2 * FL, 2 * FL + 1]
    n0, _ = tnorm(V, T); vn0 = VN
    def kabsch(A, B):
        A0, B0 = A - A.mean(0), B - B.mean(0); U_, _, Wt = np.linalg.svd(A0.T @ B0); dd_ = np.sign(np.linalg.det(Wt.T @ U_.T)); return Wt.T @ np.diag([1, 1, dd_]) @ U_.T
    for pn in dj['poses']:
        X = np.load('%s_%s.npy' % (PP, pn)).astype(float); n1, _ = tnorm(X, T); S1 = unit(vnormals_sum(X, T)); inv_t = []; rotdev = np.zeros(len(T)); vflip = 0
        for t in brT:
            ring = sorted(set().union(*[nb[v] for v in T[t]])); Rk = kabsch(V[ring], X[ring]); r_ = deg((Rk @ n0[t]) @ n1[t]); rotdev[t] = r_
            if r_ > 90: inv_t.append(int(t))
        for v in np.nonzero(brv)[0]:
            ring = sorted(nb[v]) if nb[v] else [v]
            if len(ring) >= 3 and (kabsch(V[ring], X[ring]) @ vn0[v]) @ S1[v] < 0: vflip += 1
        cp, mp = rule(X, Q); fold_p = np.where(c == 0, mp[0]['fold'], mp[1]['fold']); fp_any = ((mp[0]['n1'] * mp[0]['n2']).sum(1) < 0) | ((mp[1]['n1'] * mp[1]['n2']).sum(1) < 0)
        new = selfx(X) - SX0
        def cdesc(i):
            t = int(near_t[i]); f = int(tq[t]); return dict(tri=t, quad=f, region=str(REG[f]) or 'head', parts='/'.join(sorted(set(part[Q[f]].tolist()))), side=str(fside[f]))
        POSE[pn] = dict(new_contacts=len(new), new_contact_pairs=[[cdesc(i), cdesc(j)] for i, j in sorted(new)[:10]], triangle_inversions=len(inv_t), vertex_normal_flips=int(vflip), root_band_triangle_inversions=int(np.isin(inv_t, band).sum()),
                        folded_across_baked_diagonal_rest=int((fold_c > 90)[br].sum()), folded_across_baked_diagonal_pose=int((fold_p > 90)[br].sum()),
                        folded_quads_audit_metric_rest=int(folded[br].sum()), folded_quads_audit_metric_pose=int(fp_any[br].sum()),
                        flagged_max_fold_change_deg=round(float(np.abs(fold_p - fold_c)[FL].max()), 3) if len(FL) else 0.0,
                        flagged_max_local_normal_change_deg=round(float(rotdev[flT].max()), 3) if len(FL) else 0.0, branch_max_local_normal_change_deg=round(float(rotdev[brT].max()), 3),
                        rule_reevaluated_at_pose_would_change_diagonal_branch=int((cp != c)[br].sum()), baked_diagonal_changes=0)
        print(pn, POSE[pn], flush=True)
    R['poses'] = POSE
    worst = sorted(POSE, key=lambda k: (POSE[k]['triangle_inversions'], POSE[k]['flagged_max_local_normal_change_deg']), reverse=True)[:2]; R['worst_two_poses'] = worst

# ---------------- §7 LOD 50 / 25 % on the baked triangulated mesh
srcT = np.nonzero(nearv[T].any(1))[0]; bvh_src = BVHTree.FromPolygons((V / 100).tolist(), T[srcT].tolist(), all_triangles=True, epsilon=0.0)
BOX = [(V[brv & (side == s_)].min(0) - 0.2, V[brv & (side == s_)].max(0) + 0.2) for s_ in ('l', 'r')]
def inbox(P_): return np.any([((P_ >= l_) & (P_ <= h_)).all(-1) for l_, h_ in BOX], 0)
LODS = {}
rootv = np.unique(Q[loopm & br].ravel()); flc = (V[Q[FL]].mean(1) / 100) if len(FL) else np.zeros((0, 3)); nfl = unit(VN[Q[FL]].sum(1)) if len(FL) else np.zeros((0, 3))
# LOD-HV1 (production LOD constraint, source untouched): Decimate collapse with a vertex-group weight 0 on the cuff + transition band and its one-ring
# (root junction protected; the auricle sheet and the head decimate normally). 'unconstrained' = the closure prodcheck setting, kept for comparison.
prot = np.isin(part, ['cuff', 'transition']); _m = prot[Q].any(1); _nb = np.zeros(nV, bool); _nb[Q[_m].ravel()] = True; prot |= _nb
SMART = False
for mode, ratio in (('protected', 0.5), ('protected', 0.25), ('unconstrained', 0.5), ('unconstrained', 0.25)):
    ob = mkmesh(V, T); md = ob.modifiers.new('dec', 'DECIMATE'); md.ratio = ratio
    if mode == 'protected':
        vg = ob.vertex_groups.new(name='lod'); vg.add(np.nonzero(~prot)[0].tolist(), 1.0, 'REPLACE'); vg.add(np.nonzero(prot)[0].tolist(), 0.0, 'REPLACE'); md.vertex_group = 'lod'; md.vertex_group_factor = 1.0
    dg = bpy.context.evaluated_depsgraph_get(); m2 = ob.evaluated_get(dg).to_mesh()
    P = np.array([v.co[:] for v in m2.vertices]) * 100; F = np.array([list(p.vertices) for p in m2.polygons], dtype=object)
    Ft = np.array([f for f in F if len(f) == 3], np.int64); inb = inbox(P)
    ec = Counter(tuple(sorted((int(f[k]), int(f[(k + 1) % len(f)])))) for f in F for k in range(len(f))); nm = sum(1 for e, n in ec.items() if n != 2 and (inb[e[0]] or inb[e[1]]))
    nf, af = tnorm(P, Ft); za = int(((af < 1e-8) & inb[Ft].any(1)).sum())
    reg = np.nonzero(inb[Ft].any(1))[0]; b2 = BVHTree.FromPolygons((P / 100).tolist(), Ft[reg].tolist(), all_triangles=True, epsilon=0.0)
    sx = sum(1 for i, j in b2.overlap(b2) if not (set(Ft[reg][i]) & set(Ft[reg][j])))
    d_lod_to_src = np.array([(bvh_src.find_nearest(p / 100)[3] or 0) * 100 for p in P[inb]])
    def to_lod(pts): return np.array([b2.find_nearest(p)[3] * 100 for p in pts])
    d_src_to_lod = to_lod(V[brv] / 100); d_root = to_lod(V[rootv] / 100)
    if len(FL):
        hits = [b2.find_nearest(p) for p in flc]; d_fl = np.array([h_[3] * 100 for h_ in hits]); ndev = np.array([deg(np.dot(unit(np.array(h_[1])), nfl[i])) for i, h_ in enumerate(hits)])
    else: d_fl = ndev = np.zeros(1)
    LODS.setdefault(mode, {})[str(ratio)] = dict(faces=len(F), ear_region_nonmanifold_edges=int(nm), ear_region_zero_area_triangles=za, ear_region_self_intersection_pairs=int(sx),
                            ear_max_drift_source_to_lod_cm=round(float(d_src_to_lod.max()), 4), ear_p99_drift_source_to_lod_cm=round(float(np.percentile(d_src_to_lod, 99)), 4),
                            ear_max_drift_lod_to_source_cm=round(float(d_lod_to_src.max()), 4), root_region_max_drift_cm=round(float(d_root.max()), 4),
                            flagged_max_drift_cm=round(float(d_fl.max()), 4), flagged_normal_deviation_max_deg=round(float(ndev.max()), 2), flagged_normal_deviation_p95_deg=round(float(np.percentile(ndev, 95)), 2),
                            flagged_regions_lod_normal_over_60deg=int((ndev > 60).sum()))
    np.savez_compressed('%s/%s_lod%02d%s.npz' % (OUT, LAB, int(ratio * 100), '' if mode == 'protected' else 'U'), V=P.astype(np.float32), Q=Ft)
    m2 = None
R['lod'] = dict(LODS, rule='LOD-HV1: Decimate collapse, vertex-group weight 0 on cuff + transition + one ring (protected root junction)', protected_vertices=int(prot.sum()))
# baseline: source self-intersections on the baked triangles in the same ear boxes
bS = BVHTree.FromPolygons((V / 100).tolist(), T[srcT].tolist(), all_triangles=True, epsilon=0.0)
R['lod']['source_ear_region_self_intersection_pairs'] = sum(1 for i, j in bS.overlap(bS) if not (set(T[srcT][i]) & set(T[srcT][j])) and inbox(V[T[srcT][i]]).any())
np.savez_compressed('%s/%s_tri.npz' % (OUT, LAB), V=V.astype(np.float32), Q=T, tq=tq, choice=c, flagged=FL, region=REG.astype(str), folded=folded, warped=warped,
                    alt_T=np.concatenate([tris(Q[f][None], np.array([alt[f]])) for f in FL]) if len(FL) else np.zeros((0, 3), np.int64))
json.dump(R, open('%s/%s_prodtri.json' % (OUT, LAB), 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('PRODTRI_DONE', LAB, json.dumps({k: R[k] for k in ('order_invariance_mismatched_quads', 'triangulation')})[:600], json.dumps(R['flagged']['defect_flags']), flush=True)
