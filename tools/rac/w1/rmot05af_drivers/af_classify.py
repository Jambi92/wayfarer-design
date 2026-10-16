# RM-OT-05AF s6 classification of every remaining coincident duplicate group in the frozen 05AE sculpt-safe baseline.
# Region: dominant rig vertex group (05AB rig, carried in the .blend) + geometry (head above 172 cm, tail / fused root from the 05AC
# protection mask, genital box, gluteal = trunk behind the pelvis centre below 117 cm).
# Interface test, per group, on the position-welded mesh: collapse the group, take the link of the merged vertex (edges opposite it
# in every incident face, neighbours also position-welded). SAFE_SCULPT_SEAM = link is ONE simple closed cycle AND the members'
# fans agree in orientation (min pairwise fan-normal dot > -0.5): one continuous surface stored twice. PROTECTED_INTERFACE = link
# splits into >1 cycle (two distinct surfaces touching at a point: lips, folds, digits, openings) or lies in a protected landmark
# zone (genital box, tail junction, face). UNKNOWN = link not a simple cycle / opposing fans.
# Sculpt zones (AC1-AC3): trunk below 172 cm (minus genital box and tail junction), upper arm, forearm, thigh, shin, plus a 5 cm
# buffer into hand / foot (wrist / ankle) so mask falloff never meets an unwelded seam; head, hands, feet, free tail excluded.
# Usage: python3 -I af_classify.py BASE_VF.npz WEIGHTS.npz PROTECT_05AE.npy OUTDIR
import sys, os, json, numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
bp, wp, pp, od = sys.argv[1:5]
B = np.load(bp); V, F = B['V'], B['F']; n = len(V)
Wz = np.load(wp); W = Wz['W']; names = [str(x) for x in Wz['names']]; P = np.load(pp)
z = (V[:, 2] - V[:, 2].min()) * 100; X = V * 100
lab = W.argmax(1); g = lambda nm: names.index(nm)
# position weld ids (for link computation)
key, pid = np.unique(np.round(V, 7), axis=0, return_inverse=True); pid = pid.ravel()
# duplicate groups
pairs = cKDTree(V).query_pairs(1e-5, output_type='ndarray')
nc, cl = connected_components(sp.coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n)), directed=False)
sz = np.bincount(cl); dupv = np.flatnonzero(sz[cl] > 1)
order = np.argsort(cl[dupv]); dv = dupv[order]; starts = np.r_[0, np.flatnonzero(np.diff(cl[dv])) + 1]; ends = np.r_[starts[1:], len(dv)]
groups = [dv[s:e] for s, e in zip(starts, ends)]
# geometry landmarks
trunk = lab == g('trunk'); hands = np.isin(lab, [g('hand_L'), g('hand_R')]); feet = np.isin(lab, [g('foot_L'), g('foot_R')])
tailP = (P >= 1) & trunk & (z < 168.3)                                    # free tail + fused root (protection mask)
mid_x = float(np.median(X[trunk & (z > 120) & (z < 160), 0])); pel = trunk & (z > 85) & (z < 117)
pel_y = float(np.median(X[pel, 1]))
crotch = float(z[trunk & (np.abs(X[:, 0] - mid_x) < 4) & (X[:, 1] < pel_y)].min())
genital = trunk & (np.abs(X[:, 0] - mid_x) < 9) & (X[:, 1] < pel_y) & (z >= crotch - 1) & (z <= crotch + 16)
tail_tree = cKDTree(X[tailP]) if tailP.any() else None
d_tail = tail_tree.query(X)[0] if tail_tree is not None else np.full(n, 1e9)
tailj = (d_tail < 3.0) & ~tailP                                            # 3 cm junction margin
# 5 cm buffer from hands / feet toward the limbs
limb = np.isin(lab, [g(k) for k in ('upperarm_L', 'upperarm_R', 'forearm_L', 'forearm_R', 'thigh_L', 'thigh_R', 'shin_L', 'shin_R')])
d_limb = cKDTree(X[limb]).query(X)[0]
buf = (hands | feet) & (d_limb < 5.0)
def region(v):
    if z[v] > 172.0 and trunk[v]: return 'head'
    if tailP[v]: return 'free_tail_root'
    if hands[v]: return 'hand_wrist_buffer' if buf[v] else 'hand'
    if feet[v]: return 'foot_ankle_buffer' if buf[v] else 'foot'
    if genital[v]: return 'genital_landmark'
    if tailj[v]: return 'tail_junction'
    if trunk[v]:
        if z[v] >= 117: return 'torso_neckbase'
        return 'gluteal' if X[v, 1] > pel_y else 'pelvis_flank'
    return names[lab[v]].split('_')[0]                                    # upperarm / forearm / thigh / shin
SCULPT = {'torso_neckbase', 'gluteal', 'pelvis_flank', 'upperarm', 'forearm', 'thigh', 'shin', 'hand_wrist_buffer', 'foot_ankle_buffer'}
PROTECTED_ZONE = {'genital_landmark', 'tail_junction', 'free_tail_root', 'head'}
# vertex -> faces
vf = sp.csr_matrix((np.ones(F.size), (F.ravel(), np.repeat(np.arange(len(F)), 3))), shape=(n, len(F)))
fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
def link_cycles(gv):
    faces = np.unique(np.concatenate([vf.indices[vf.indptr[v]:vf.indptr[v + 1]] for v in gv]))
    c = pid[gv[0]]; E = []
    for f in faces:
        t = pid[F[f]]; o = [x for x in t if x != c]
        if len(o) != 2: return None, faces
        E.append(tuple(sorted(o)))
    E = np.array(E); u, cnt = np.unique(E, axis=0, return_counts=True)
    nodes, inv = np.unique(u.ravel(), return_inverse=True); deg = np.bincount(inv)
    if (cnt != 1).any() or (deg != 2).any(): return -1, faces
    m = len(nodes); k, _ = connected_components(sp.coo_matrix((np.ones(len(u)), (inv[0::2], inv[1::2])), shape=(m, m)), directed=False)
    return int(k), faces
rows = []; cls_count = {}
for gv in groups:
    regs = sorted({region(v) for v in gv}); reg = regs[0] if len(regs) == 1 else '+'.join(regs)
    k, faces = link_cycles(gv)
    fans = []
    for v in gv:
        fv = vf.indices[vf.indptr[v]:vf.indptr[v + 1]]; a = fn[fv].sum(0); fans.append(a / max(np.linalg.norm(a), 1e-30))
    fans = np.array(fans); dmin = float(min((fans[i] @ fans[j]) for i in range(len(gv)) for j in range(i + 1, len(gv))))
    spread = float(np.linalg.norm(V[gv] - V[gv[0]], axis=1).max() * 1000)
    if any(r in PROTECTED_ZONE for r in regs): c = 'PROTECTED_INTERFACE'
    elif k == 1 and dmin > -0.5: c = 'SAFE_SCULPT_SEAM'
    elif k is not None and k > 1: c = 'PROTECTED_INTERFACE'
    else: c = 'UNKNOWN'
    in_sculpt = all(r in SCULPT for r in regs)
    rows.append(dict(members=[int(x) for x in gv], region=reg, cls=c, link_cycles=k, min_fan_dot=round(dmin, 3), spread_mm=round(spread, 6),
                     z=round(float(z[gv[0]]), 2), in_sculpt_zone=in_sculpt))
# summary by region x class
S = {}
for r in rows:
    s = S.setdefault(r['region'], {}); c = s.setdefault(r['cls'], dict(groups=0, vertices=0, zmin=1e9, zmax=-1e9, sizes={}))
    c['groups'] += 1; c['vertices'] += len(r['members']); c['zmin'] = min(c['zmin'], r['z']); c['zmax'] = max(c['zmax'], r['z'])
    c['sizes'][str(len(r['members']))] = c['sizes'].get(str(len(r['members'])), 0) + 1
R = dict(vertices=n, duplicate_groups=len(groups), duplicate_vertices=int(sum(len(x) for x in groups)),
         max_spread_mm=round(max(r['spread_mm'] for r in rows), 6) if rows else None,
         landmarks=dict(mid_x_cm=round(mid_x, 2), pelvis_centre_y_cm=round(pel_y, 2), crotch_z_cm=round(crotch, 2),
                        genital_box='|x-mid|<9 cm, front of pelvis centre, z crotch-1 .. crotch+16', tail_junction_margin_cm=3.0, wrist_ankle_buffer_cm=5.0),
         by_region=S,
         sculpt_zone=dict(safe=sum(1 for r in rows if r['in_sculpt_zone'] and r['cls'] == 'SAFE_SCULPT_SEAM'),
                          protected=sum(1 for r in rows if r['in_sculpt_zone'] and r['cls'] == 'PROTECTED_INTERFACE'),
                          unknown=sum(1 for r in rows if r['in_sculpt_zone'] and r['cls'] == 'UNKNOWN')))
os.makedirs(od, exist_ok=True)
json.dump(rows, open(os.path.join(od, 'af_groups.json'), 'w')); json.dump(R, open(os.path.join(od, 'af_classification.json'), 'w'), indent=1)
reg_v = np.array([region(v) for v in range(n)]) if False else None
print(json.dumps({k: R[k] for k in ('duplicate_groups', 'duplicate_vertices', 'max_spread_mm', 'landmarks', 'sculpt_zone')}, indent=1))
for reg, s in sorted(S.items()): print(reg, {c: (v['groups'], v['vertices'], round(v['zmin'], 1), round(v['zmax'], 1)) for c, v in s.items()})
