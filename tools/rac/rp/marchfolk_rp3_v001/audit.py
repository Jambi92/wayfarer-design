# audit.py NATIVE.npz R6.npz OUT.json [OUT_loops.npz] : RP3 (order d18ff2a §8 / §9) production audit of a quad body (native hm08 or a candidate)
# in the R-6 stance against RAC_PRODUCTION_MESH_CONTRACT §6 / §7 / §8 / §11.
#   integrity : components, boundary / non-manifold edges and vertices, coincident duplicates, degenerate faces, winding consistency + outward
#               orientation (signed volume; analysis frame is left-handed, so outward = negative), self-intersections (BVH, non-adjacent triangle pairs),
#               face types, poles (valence != 4) and their zones, quad interior angles (T-4 45-135 deg) and aspect (T-4 <= 4:1; longest / shortest side).
#   loops     : every quad edge loop (walk through valence-4 vertices taking the opposite edge); closed loops kept. For each joint: closed loops that
#               ENCIRCLE the joint axis (winding of the loop around the axis line = +-1), lie within the limb (max distance from axis <= r_max) and
#               whose axial centre is within +-window of the joint centre; count, axial positions, spacing. Face: rings encircling the forward axis
#               through each eye and through the mouth.
#   density   : mean edge length / stature per zone (contract §8) -- face, ears, hands+digits, feet+toes, trunk / pelvis / gluteal, limbs, neck.
#   lod       : share of vertices on closed loops per zone, pole count per zone, loops tagged silhouette-critical (head profile, girdle, digits).
import sys, json, numpy as np
from collections import defaultdict
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
z = np.load(a[0]); r6 = np.load(a[1]); OUT = a[2]
V = z['V'].astype(float); Q = np.asarray(z['Q']); si = z['src_index']; nV = len(V); meta = json.loads(str(z['meta']))
H = {k: np.array(v) for k, v in meta['heads'].items()}; T_ = {k: np.array(v) for k, v in meta['tails'].items()}; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}
stature = V[:, 2].max() - V[:, 2].min(); R = {}
# ---------- zones (dominant source weight channels of the R-6 asset)
w = {k[2:]: r6[k][si] for k in r6.files if k.startswith('w_')}
if 'M_data' in z.files:                                            # subdivided candidate: zone weights carried through the linear map
    import scipy.sparse as _sp
    Mz = _sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); w = {k: Mz @ v for k, v in w.items()}
def dom(keys): return np.sum([w[k] for k in keys if k in w], 0)
zone = np.full(nV, 'other', object)
groups = {'head': ['head'], 'ears': ['ears'], 'neck': ['neck_01'], 'trunk': ['pelvis', 'spine_01', 'spine_02', 'spine_03', 'clavicle_l', 'clavicle_r'],
          'arm': ['upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r'], 'hand': ['hand_l', 'hand_r', 'fingers_l', 'fingers_r'], 'leg': ['thigh_l', 'thigh_r', 'calf_l', 'calf_r'],
          'foot': ['foot_l', 'foot_r', 'ball_l', 'ball_r']}
S = np.stack([dom(v) for v in groups.values()], 1); zone = np.array(list(groups))[S.argmax(1)]
ear_c = V[w['ears'] > 0.5].mean(0) if (w['ears'] > 0.5).any() else None
face = (zone == 'head') & (V[:, 1] > (ear_c[1] if ear_c is not None else H['head'][1]))
zone_f = zone.copy(); zone_f[face] = 'face'
# ---------- integrity
E_all = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); Es = np.sort(E_all, 1)
uE, inv, cnt = np.unique(Es, axis=0, return_inverse=True, return_counts=True)
R['verts'] = nV; R['faces'] = int(len(Q)); R['edges'] = int(len(uE)); R['quads_pct'] = 100.0; R['tris'] = 0; R['ngons'] = 0
R['boundary_edges'] = int((cnt == 1).sum()); R['nonmanifold_edges'] = int((cnt > 2).sum())
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
A = sp.csr_matrix((np.ones(2 * len(uE)), (np.r_[uE[:, 0], uE[:, 1]], np.r_[uE[:, 1], uE[:, 0]])), shape=(nV, nV))
R['components'] = int(connected_components(A, directed=False)[0]); R['euler'] = int(nV - len(uE) + len(Q)); R['genus'] = (2 - R['euler']) / 2
# non-manifold vertices: incident faces must form one edge-connected fan
vf = defaultdict(list)
for fi, q in enumerate(Q):
    for v in q: vf[v].append(fi)
nmv = 0
for v, fl in vf.items():
    if len(fl) < 2: nmv += 1; continue
    es = {fi: set(map(tuple, np.sort(np.array([[q[k], q[(k + 1) % 4]] for k in range(4) if v in (q[k], q[(k + 1) % 4])]), 1).tolist())) for fi, q in ((f, Q[f]) for f in fl)}
    seen = {fl[0]}; stack = [fl[0]]
    while stack:
        f = stack.pop()
        for g in fl:
            if g not in seen and es[f] & es[g]: seen.add(g); stack.append(g)
    nmv += len(seen) != len(fl)
R['nonmanifold_vertices'] = int(nmv)
from scipy.spatial import cKDTree
pairs = cKDTree(V).query_pairs(1e-4); R['coincident_vertex_pairs'] = len(pairs)
fn = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]) * 0.5; area = np.linalg.norm(fn, axis=1); R['degenerate_faces'] = int((area < 1e-6).sum())
# winding consistency: directed edges should appear once each direction
D = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); dkey = D[:, 0] * nV + D[:, 1]
R['winding_consistent'] = bool(len(np.unique(dkey)) == len(dkey))
TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; vol = float(np.einsum('ij,ij->i', V[TRI[:, 0]], np.cross(V[TRI[:, 1]], V[TRI[:, 2]])).sum() / 6)
R['signed_volume_cm3'] = round(vol, 1); R['normals_outward'] = bool(vol < 0)   # left-handed analysis frame: outward winding gives negative signed volume
R['stature_cm'] = round(float(stature), 4)
# self-intersections (mathutils BVH, triangles of non-adjacent quads)
try:
    import bpy  # noqa: F401  (bpy python provides mathutils)
    from mathutils.bvhtree import BVHTree
    bvh = BVHTree.FromPolygons(V.tolist(), TRI.tolist(), all_triangles=True, epsilon=0.0)
    ov = bvh.overlap(bvh); qid = np.r_[np.arange(len(Q)), np.arange(len(Q))]; bad = set()
    for i, j in ov:
        fi, fj = qid[i], qid[j]
        if fi == fj or set(Q[fi]) & set(Q[fj]): continue
        bad.add((min(fi, fj), max(fi, fj)))
    R['self_intersection_face_pairs'] = len(bad); R['self_intersection_zones'] = dict(zip(*np.unique(zone_f[Q[[p[0] for p in bad]][:, 0]], return_counts=True))) if bad else {}
    R['self_intersection_zones'] = {k: int(v) for k, v in R['self_intersection_zones'].items()}; SI = np.array(sorted(bad), int).reshape(-1, 2)
except Exception as e:
    R['self_intersection_face_pairs'] = 'n/a (%s)' % e; SI = np.zeros((0, 2), int)
# valence / poles
val = np.bincount(uE.ravel(), minlength=nV); poles = np.nonzero(val != 4)[0]
R['poles'] = {'valence_3': int((val == 3).sum()), 'valence_5plus': int((val >= 5).sum()), 'by_zone': {k: int(v) for k, v in zip(*np.unique(zone_f[poles], return_counts=True))}}
# angles / aspect
ang = []; asp = []
for k in range(4):
    p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]
    u1 = p0 - p1; u2 = p2 - p1; ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
ang = np.stack(ang, 1); sides = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sides.max(1) / np.maximum(sides.min(1), 1e-9)
fz = zone_f[Q[:, 0]]; badang = (ang.min(1) < 45) | (ang.max(1) > 135); badasp = asp > 4
R['angle_45_135_violations'] = int(badang.sum()); R['angle_violations_by_zone'] = {k: int(v) for k, v in zip(*np.unique(fz[badang], return_counts=True))}
R['aspect_gt4_violations'] = int(badasp.sum()); R['aspect_violations_by_zone'] = {k: int(v) for k, v in zip(*np.unique(fz[badasp], return_counts=True))}
R['angle_p01_p99'] = [round(float(np.percentile(ang, 1)), 1), round(float(np.percentile(ang, 99)), 1)]; R['aspect_p99'] = round(float(np.percentile(asp, 99)), 2)
# ---------- density
el = np.linalg.norm(V[uE[:, 0]] - V[uE[:, 1]], axis=1); ez = zone_f[uE[:, 0]]; same = zone_f[uE[:, 0]] == zone_f[uE[:, 1]]
LIM = {'face': 0.25, 'ears': 0.25, 'hand': 0.3, 'foot': 0.3, 'trunk': 0.6, 'arm': 0.6, 'leg': 0.6, 'neck': 0.6, 'head': 0.6}
R['density_pct_of_stature'] = {k: dict(mean=round(float(el[same & (ez == k)].mean() / stature * 100), 3), median=round(float(np.median(el[same & (ez == k)]) / stature * 100), 3),
                                       p90=round(float(np.percentile(el[same & (ez == k)], 90) / stature * 100), 3), p95=round(float(np.percentile(el[same & (ez == k)], 95) / stature * 100), 3), limit=LIM.get(k), pass_mean=bool(el[same & (ez == k)].mean() / stature * 100 <= LIM.get(k, 9)))
                               for k in LIM if (same & (ez == k)).any()}
R['density_overall_median_pct'] = round(float(np.median(el) / stature * 100), 3)
# ---------- edge loops
nbr = [[] for _ in range(nV)]
for e in uE: nbr[e[0]].append(e[1]); nbr[e[1]].append(e[0])
fe = defaultdict(set)
for fi, q in enumerate(Q):
    for k in range(4): fe[(min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))].add(fi)
def nxt(prev, v):
    if val[v] != 4: return None
    fp = fe[(min(prev, v), max(prev, v))]
    for u in nbr[v]:
        if u == prev: continue
        if not (fe[(min(u, v), max(u, v))] & fp): return u
    return None
seen_e = set(); loops = []
for e in map(tuple, uE):
    if e in seen_e: continue
    path = [e[0], e[1]]; seen_e.add(e); closed = False
    while True:
        u = nxt(path[-2], path[-1])
        if u is None: break
        ek = (min(path[-1], u), max(path[-1], u))
        if u == path[0]: closed = True; seen_e.add(ek); break
        if ek in seen_e: break
        seen_e.add(ek); path.append(u)
    if closed: loops.append(np.array(path))
    else:  # extend backwards for open chains (bookkeeping only)
        b = [e[1], e[0]]
        while True:
            u = nxt(b[-2], b[-1])
            if u is None: break
            ek = (min(b[-1], u), max(b[-1], u))
            if ek in seen_e: break
            seen_e.add(ek); b.append(u)
R['closed_loops'] = len(loops); onloop = np.zeros(nV, bool)
for L in loops: onloop[L] = True
R['lod_vertices_on_closed_loops_pct_by_zone'] = {k: round(float(onloop[zone_f == k].mean() * 100), 1) for k in np.unique(zone_f)}
def encircling(c, d, rmax, win):
    d = d / np.linalg.norm(d); out = []
    for li, L in enumerate(loops):
        P = V[L] - c; t = P @ d; rad = P - np.outer(t, d); rr = np.linalg.norm(rad, axis=1)
        if rr.max() > rmax or abs(t.mean()) > win or rr.min() < 1e-6: continue
        u = np.cross(d, [0, 0, 1.0]) if abs(d[2]) < 0.9 else np.cross(d, [1.0, 0, 0]); u /= np.linalg.norm(u); vv = np.cross(d, u)
        th = np.arctan2(rad @ vv, rad @ u); dth = np.diff(np.r_[th, th[0]]); dth = (dth + np.pi) % (2 * np.pi) - np.pi
        if abs(abs(dth.sum()) - 2 * np.pi) < 0.5: out.append((li, float(t.mean()), float(rr.mean())))
    return sorted(out, key=lambda x: x[1])
JR = []   # (name, centre, axis, rmax, window, min_loops)
for s in ('l', 'r'):
    JR += [('shoulder_' + s, H['upperarm_' + s], T_['upperarm_' + s] - H['upperarm_' + s], 12.0, 6.0, 5), ('elbow_' + s, H['lowerarm_' + s], T_['lowerarm_' + s] - H['upperarm_' + s], 7.0, 4.0, 4),
           ('wrist_' + s, H['hand_' + s], T_['hand_' + s] - H['lowerarm_' + s], 5.0, 2.5, 3), ('hip_' + s, H['thigh_' + s], T_['thigh_' + s] - H['thigh_' + s], 16.0, 8.0, 5),
           ('knee_' + s, H['calf_' + s], T_['calf_' + s] - H['thigh_' + s], 9.0, 5.0, 4), ('ankle_' + s, H['foot_' + s], T_['calf_' + s] - H['calf_' + s], 7.0, 3.5, 3)]
    for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        for k, (lab, mn) in enumerate((('knuckle', 3), ('ip1', 2), ('ip2', 2))):
            b = '%s_%02d_%s' % (fg, k + 1, s); JR.append(('%s_%s_%s' % (fg, lab, s), H[b], T_[b] - H[b], 1.6, 0.8 if k else 1.0, mn))
    for t in range(1, 6):
        for j in (1, 2, 3):
            k1, k2 = '%s-toe-%d-%d' % (s, t, j), '%s-toe-%d-%d' % (s, t, j + 1)
            if k1 in JC and k2 in JC: JR.append(('toe%d_j%d_%s' % (t, j, s), JC[k1], JC[k2] - JC[k1], 1.6, 0.6, 2))
JR += [('neck', 0.5 * (H['neck_01'] + H['head']), H['head'] - H['neck_01'], 9.0, 0.5 * np.linalg.norm(H['head'] - H['neck_01']) + 1.0, 4)]
LJ = {}
for nm, c, d, rmax, win, mn in JR:
    lo = encircling(c, d, rmax, win); LJ[nm] = dict(count=len(lo), min=mn, pass_=len(lo) >= mn, axial_cm=[round(x[1], 2) for x in lo], mean_radius_cm=[round(x[2], 2) for x in lo], loop_ids=[x[0] for x in lo])
R['closed_rings_secondary'] = {k: {kk: vv for kk, vv in v.items() if kk != 'loop_ids'} for k, v in LJ.items()}
# PRIMARY loop measure = the accepted program method (tools/rac/rp/grask_retopo_v001/loopaudit.py, used for Grask RP2 v003): number of edge loops
# crossed by a surface path across the joint band [c - W d, c + W d] on four sides (min over sides), plus poles within 2 local loops of the joint plane.
from scipy.sparse.csgraph import dijkstra
wE = np.linalg.norm(V[uE[:, 0]] - V[uE[:, 1]], axis=1); Gw = sp.coo_matrix((np.r_[wE, wE], (np.r_[uE[:, 0], uE[:, 1]], np.r_[uE[:, 1], uE[:, 0]])), shape=(nV, nV)).tocsr()
VN = np.zeros_like(V)
for k in range(4): np.add.at(VN, Q[:, k], fn)
VN /= np.maximum(np.linalg.norm(VN, axis=1), 1e-12)[:, None]; kd = cKDTree(V); PV = V[poles]
unit = lambda v: v / np.linalg.norm(v)
def surf(p, dirn, Rr):
    cand = kd.query_ball_point(p + dirn * Rr * 0.5, Rr * 0.9)
    if not cand: return int(kd.query(p)[1])
    cand = np.array(cand); t = (V[cand] - p) @ dirn; off = np.linalg.norm((V[cand] - p) - np.outer(t, dirn), axis=1)
    ok = (VN[cand] @ dirn > 0.3); sc = np.where(ok, off, 1e9); return int(cand[np.argmin(sc)])
def band(c, d, W, Rr, Rp=None):
    d = unit(d); pp = unit(np.cross(d, [0, 1.0, 0] if abs(d[1]) < 0.9 else [1.0, 0, 0])); qq = unit(np.cross(d, pp)); res = []; merged = 0
    for side in (pp, -pp, qq, -qq):
        a_ = surf(c - d * W, side, Rr); b_ = surf(c + d * W, side, Rr)
        if np.linalg.norm(V[a_] - V[b_]) < 0.7 * 2 * W: merged += 1; continue
        _, pred = dijkstra(Gw, indices=a_, return_predecessors=True, limit=4 * W + 3 * Rr)
        if pred[b_] < 0: continue
        path = [b_]
        while path[-1] != a_: path.append(int(pred[path[-1]]))
        P = V[path]; e = np.diff(P, axis=0); res.append(int((np.abs(e @ d) > 0.5 * np.linalg.norm(e, axis=1)).sum()))
    near = np.nonzero(np.linalg.norm(V[uE[:, 0]] - c, axis=1) < Rr)[0]; h = float(np.median(wE[near])) if len(near) else 0.3
    Rp = Rr if Rp is None else Rp; pb = (PV - c) @ d; pr = np.linalg.norm((PV - c) - np.outer(pb, d), axis=1)
    sel = (np.abs(pb) <= 2 * h) & (pr <= Rp)
    return dict(loops=int(min(res)) if res else 0, loops_by_side=res, web_merged_sides=merged, poles_within_2_loops=int(sel.sum()), poles_on_crease_line=int(((np.abs(pb) <= 0.5 * h) & (pr <= Rp)).sum()),
                pole_offsets_in_loops=sorted(round(float(x), 2) for x in np.abs(pb[sel]) / h), local_edge_mm=round(10 * h, 2))
BJ = {}
def J(nm, c, d, W, Rr, need, Rp=None):
    r_ = band(np.asarray(c, float), np.asarray(d, float), W, Rr, Rp); r_['required'] = need; r_['pass'] = bool(r_['loops'] >= need and r_['poles_within_2_loops'] == 0); BJ[nm] = r_
J('neck', 0.5 * (H['neck_01'] + H['head']), np.array([0, 0, 1.0]), 2.0, 11, 4)
for s in ('l', 'r'):
    J('shoulder_' + s, H['upperarm_' + s], H['lowerarm_' + s] - H['upperarm_' + s], 3.0, 9, 5); J('elbow_' + s, H['lowerarm_' + s], H['hand_' + s] - H['lowerarm_' + s], 1.5, 7, 4)
    J('wrist_' + s, H['hand_' + s], H['middle_01_' + s] - H['hand_' + s], 1.0, 5, 3)
    for fg in ('index', 'middle', 'ring', 'pinky'):
        b1, b2, b3 = ['%s_%02d_%s' % (fg, k, s) for k in (1, 2, 3)]
        J('%s_mcp_%s' % (fg, s), H[b1], H[b2] - H[b1], 0.8, 1.6, 3); J('%s_ip1_%s' % (fg, s), H[b2], H[b3] - H[b1], 0.5, 1.3, 2); J('%s_ip2_%s' % (fg, s), H[b3], T_[b3] - H[b2], 0.5, 1.3, 2)
    J('thumb_mcp_' + s, H['thumb_02_' + s], H['thumb_03_' + s] - H['thumb_01_' + s], 0.8, 2.0, 3); J('thumb_ip_' + s, H['thumb_03_' + s], T_['thumb_03_' + s] - H['thumb_02_' + s], 0.5, 1.6, 2)
    J('hip_' + s, H['thigh_' + s], H['calf_' + s] - H['thigh_' + s], 3.0, 12, 5); J('knee_' + s, H['calf_' + s], H['foot_' + s] - H['calf_' + s], 1.5, 9, 4)
    J('ankle_' + s, H['foot_' + s], H['foot_' + s] - H['calf_' + s], 1.5, 7, 3)
    for t in range(1, 6):
        for j in (1, 2, 3):
            k0, k1, k2 = '%s-toe-%d-%d' % (s, t, j - 1), '%s-toe-%d-%d' % (s, t, j), '%s-toe-%d-%d' % (s, t, j + 1)
            if k1 in JC and k2 in JC:
                a_ = JC[k2] - (JC[k0] if k0 in JC else JC[k1]); rr = 0.5 * np.linalg.norm(JC[k2] - JC[k1]) + 0.6
                J('toe%d_j%d_%s' % (t, j, s), JC[k1], a_, 0.4, rr * 1.3, 2, Rp=1.15 * rr)
R['joint_bands'] = BJ; R['joint_bands_failing'] = sorted(k for k, v in BJ.items() if not v['pass'])
LJ_ = {k: v for k, v in LJ.items()}
def ringcount(nm):
    k = nm
    if '_mcp_' in nm: k = nm.replace('thumb_mcp_', 'thumb_ip1_') if nm.startswith('thumb') else nm.replace('_mcp_', '_knuckle_')
    elif nm.startswith('thumb_ip_'): k = nm.replace('thumb_ip_', 'thumb_ip2_')
    return LJ_[k]['count'] if k in LJ_ else 0
J7 = {}
for k, v in BJ.items():
    rc = ringcount(k); lp = max(rc, v['loops']); J7[k] = dict(required=v['required'], closed_rings=rc, band_loops=v['loops'], loops=lp, poles_on_crease_line=v['poles_on_crease_line'],
                                                    poles_within_2_loops=v['poles_within_2_loops'], pass_firm=bool(lp >= v['required'] and v['poles_on_crease_line'] == 0),
                                                    pass_strict=bool(lp >= v['required'] and v['poles_within_2_loops'] == 0))
R['joint_s7'] = J7; R['s7_failing_firm'] = sorted(k for k, v in J7.items() if not v['pass_firm']); R['s7_failing_strict'] = sorted(k for k, v in J7.items() if not v['pass_strict'])
R['joint_loops'] = {k: {kk: vv for kk, vv in v.items() if kk != 'loop_ids'} for k, v in LJ.items()}
R['joint_loops_failing'] = sorted(k for k, v in LJ.items() if not v['pass_'])
# face rings: eyes (forward axis through the helper-eye centre) and mouth
fwd = np.array([0, 1.0, 0]); EH = meta['eye_helpers']; FR = {}
for s in ('l', 'r'):
    c = np.array(EH['helper-%s-eye' % s]); lo = encircling(c, fwd, 3.2, 3.0); FR['orbit_' + s] = dict(count=len(lo), mean_radius_cm=[round(x[2], 2) for x in lo])
mc = JC.get('mouth', None)
if mc is not None:
    lo = encircling(np.array(mc), fwd, 4.5, 3.0); FR['mouth'] = dict(count=len(lo), mean_radius_cm=[round(x[2], 2) for x in lo], centre=np.round(mc, 2).tolist())
R['face_rings'] = FR
# landmarks used
R['stature_note'] = 'body vertices only, crown to ground'
json.dump(R, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
if len(a) > 3:
    np.savez_compressed(a[3], zone=zone_f.astype('U8'), poles=poles, SI=SI, badang=badang, badasp=badasp, loops=np.array([L for L in loops], dtype=object), joint_loop_ids=json.dumps({k: v['loop_ids'] for k, v in LJ.items()}), onloop=onloop)
print(json.dumps({k: R[k] for k in ('components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'coincident_vertex_pairs', 'degenerate_faces', 'winding_consistent', 'normals_outward', 'self_intersection_face_pairs', 'poles', 'angle_45_135_violations', 'aspect_gt4_violations', 'closed_loops', 's7_failing_firm', 's7_failing_strict', 'face_rings')}, default=str))
print(json.dumps(R['density_pct_of_stature']))
