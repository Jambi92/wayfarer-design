# diag_run.py (bpy module, for mathutils BVH) -- python3(bpy) diag_run.py -- RIGDIAG.blend RIG.json WEIGHTS.npz LANDMARKS.json OUTDIR
# Executes D1..D10 on the diagnostic rig (numpy LBS == Blender armature, verified by rig_check.py) and measures every pose.
# Nothing is saved to any .blend; posed meshes are written as derived npz for rendering only.
import bpy, sys, os, json, numpy as np
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import Rig, build_poses, src_to_bl, bl_to_src
from common import PARTS
a = sys.argv[sys.argv.index('--') + 1:]; BL, RJ, WN, LMF, O = a[:5]; os.makedirs(O + '/posed', exist_ok=True)
PIV = json.load(open(os.environ['PIVOTS'])) if os.environ.get('PIVOTS') else None          # placement-comparison runs
ONLY = os.environ.get('ONLY', '').split(',') if os.environ.get('ONLY') else None
bpy.ops.wm.open_mainfile(filepath=BL); body = [o for o in bpy.data.objects if o.type == 'MESH'][0]
LOOPS = {}
for vg in body.vertex_groups:
    if vg.name.startswith('LOOP_'): LOOPS[vg.name[5:]] = []
gidx = {vg.index: vg.name[5:] for vg in body.vertex_groups if vg.name.startswith('LOOP_')}
for v in body.data.vertices:
    for g in v.groups:
        if g.group in gidx: LOOPS[gidx[g.group]].append(v.index)
LOOPS = {k: np.array(v) for k, v in LOOPS.items()}
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get('co', co); Vb0 = co.reshape(-1, 3)
assert np.abs(bl_to_src(Vb0) - V0).max() < 1e-4, 'mesh order mismatch'
rig = Rig(RJ, WN); P = build_poses(rig); LM = json.load(open(LMF))['joints']
PN = [PARTS[i] for i in FP]; PG = np.array([('axial' if p == 'axial' else 'ear' if p.startswith('ear') else 'arm' if p.startswith('arm') else 'hand' if p.startswith('hand')
                                             else 'leg' if p.startswith('leg') else 'foot' if p.startswith('foot') else 'digit') for p in PN])
SIDE = np.array([p[-1] if p[-2:] in ('_l', '_r') else 'c' for p in PN])
E = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); Es = np.sort(E, 1); ue, inv = np.unique(Es, axis=0, return_inverse=True)
EF = np.tile(np.arange(len(Q)), 4); o = np.argsort(inv, kind='stable'); EFs = EF[o].reshape(-1, 2)           # 2 faces per edge (closed manifold)
def fnorm(V):
    n = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]); return n / np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
def volume(V):
    T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; a_, b_, c_ = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]; return float(np.einsum('ij,ij->i', a_, np.cross(b_, c_)).sum() / 6)
def cone_vol(V, faces, c):
    T = np.r_[Q[faces][:, [0, 1, 2]], Q[faces][:, [0, 2, 3]]]; a_, b_, c_ = V[T[:, 0]] - c, V[T[:, 1]] - c, V[T[:, 2]] - c; return float(np.einsum('ij,ij->i', a_, np.cross(b_, c_)).sum() / 6)
N0 = fnorm(V0); FOLD0 = int(((N0[EFs[:, 0]] * N0[EFs[:, 1]]).sum(1) < -0.5).sum()); VOL0 = volume(V0); C0 = V0[Q].mean(1)
L0 = np.linalg.norm(V0[ue[:, 0]] - V0[ue[:, 1]], axis=1)
J = lambda k: np.array(LM[k]['position_source_frame_cm'])
TEST = {   # tested pivot joints (landmark ids), crease radius cm, declared contact part-group pairs, loops prefixes
 'D1': (['glenohumeral_{s}'], 14, [('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['shoulder_fan_{s}', 'shoulder_port_{s}']),
 'D2': (['elbow_{s}'], 9, [('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['elbow_{s}']),
 'D3': (['wrist_{s}'], 7, [('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['wrist_{s}', 'wrist_palm_{s}']),
 'D4': (['index_mcp_{s}', 'middle_mcp_{s}', 'ring_mcp_{s}', 'pinky_mcp_{s}', 'index_pip_{s}', 'middle_pip_{s}', 'ring_pip_{s}', 'pinky_pip_{s}', 'index_dip_{s}', 'middle_dip_{s}', 'ring_dip_{s}', 'pinky_dip_{s}'], 2.6,
        [('digit', 'digit'), ('digit', 'hand'), ('hand', 'leg'), ('digit', 'leg'), ('arm', 'axial')], ['index_{s}_', 'middle_{s}_', 'ring_{s}_', 'pinky_{s}_', 'mcp_palm_{s}']),
 'D5': (['thumb_cmc_{s}', 'thumb_mcp_{s}', 'thumb_ip_{s}', 'index_mcp_{s}', 'index_pip_{s}', 'index_dip_{s}'], 3.5, [('digit', 'digit'), ('digit', 'hand'), ('hand', 'leg'), ('digit', 'leg'), ('arm', 'axial')], ['thumb_{s}_']),
 'D6': (['hip_{s}'], 16, [('leg', 'axial'), ('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg'), ('leg', 'leg')], ['hip_groin_{s}']),
 'D7': (['knee_{s}'], 11, [('leg', 'leg'), ('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['knee_{s}']),
 'D8': (['ankle_{s}', 'hallux_mtp_{s}', 'toe2_mtp_{s}', 'toe3_mtp_{s}', 'toe4_mtp_{s}', 'toe5_mtp_{s}'], 8, [('digit', 'digit'), ('digit', 'foot'), ('foot', 'leg'), ('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['ankle_{s}', 'forefoot_{s}']),
 'D9': (['spine_01', 'spine_02', 'spine_03', 'thoracic_01', 'thoracic_02', 'thoracic_03'], 14, [('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg'), ('leg', 'axial')], []),
 'D10': (['neck_base', 'head_pivot'], 11, [('arm', 'axial'), ('hand', 'leg'), ('digit', 'leg')], ['neck_']),
}
NAIL = {}
FIT5 = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json'))
for f in ('index', 'middle', 'ring', 'pinky', 'thumb'):
    jd = '%s_dip_l' % f if f != 'thumb' else 'thumb_ip_l'; d, t = J(jd), J('%s_tip_l' % f); dor = np.array(FIT5['cx_' + jd]['dorsal'])
    u = (t - d) / np.linalg.norm(t - d); q = V0 - d; al = q @ u; rad = q - np.outer(al, u); rn = np.linalg.norm(rad, axis=1)
    cand = (al > 0.35 * np.linalg.norm(t - d)) & (al < np.linalg.norm(t - d) + 0.5) & (rn < 1.6)
    rmed = np.median(rn[cand]) if cand.any() else 1.0
    NAIL[f] = np.nonzero(cand & ((rad @ dor) > 0.6 * rmed))[0]           # dorsal cap of the distal phalanx (nail plate + fold)
def kabsch_res(A, B):
    a0, b0 = A.mean(0), B.mean(0); H = (A - a0).T @ (B - b0); U, S, Vt = np.linalg.svd(H); D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); Rm = Vt.T @ D @ U.T
    return float(np.linalg.norm((A - a0) @ Rm.T + b0 - B, axis=1).max())
def measure(name, pose):
    tid = name.split('_')[0]; s = name.split('_')[1] if name.split('_')[1] in ('l', 'r') else 'l'
    joints, Rz, contacts, lpre = TEST[tid]; joints = [j.format(s=s) for j in joints]
    piv = None
    if PIV and name in PIV.get('poses', [name]): piv = {b: np.array(p) for b, p in PIV['pivots'].items()}
    Vb, Lin, M = rig.skin(Vb0, pose, piv); V = bl_to_src(Vb)
    if os.environ.get('VSRC'):                                                    # externally evaluated deformation (Blender preserve-volume / DQS)
        V = np.load('%s/%s.npz' % (os.environ['VSRC'], name))['V'].astype(float)
    jr = np.array([J(j) for j in joints])
    # posed joint centres: rest centre carried by the bone whose head it is (approx: nearest bone head)
    heads = {n: bl_to_src(rig.head(n)[None])[0] for n in rig.order}
    posed_c = []
    for c in jr:
        n = min(heads, key=lambda k: np.linalg.norm(heads[k] - c)); posed_c.append(bl_to_src(M[n][:3, 3][None])[0] + (c - heads[n]))
    posed_c = np.array(posed_c)
    # ---------- intersections
    t = BVHTree.FromPolygons(V.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0); pr = np.array(t.overlap(t), int).reshape(-1, 2)
    pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): A_ = Q[pr[:, 0]]; B_ = Q[pr[:, 1]]; pr = pr[~(A_[:, :, None] == B_[:, None, :]).any((1, 2))]
    C = V[Q].mean(1); cls = []
    for f0, f1 in pr:
        g0, g1 = PG[f0], PG[f1]; pair = tuple(sorted((g0, g1)))
        dz_ = min(np.linalg.norm(posed_c - C[f0], axis=1).min(), np.linalg.norm(posed_c - C[f1], axis=1).min())
        deep_leg = tid == 'D7' and PN[f0] == PN[f1] == 'leg_' + s and abs(C[f0][2] - C[f1][2]) < 40 and max(abs(d) for _, d in pose.get('shin_' + s, [('X', 0)])) >= 120
        if (any(tuple(sorted(c)) == pair for c in contacts) and PN[f0] != PN[f1]) or deep_leg: cls.append('contact')   # declared contact (different parts; calf-thigh in deep knee flexion)
        elif dz_ <= Rz: cls.append('crease')
        else: cls.append('non-contact')
    cls = np.array(cls)
    bd = {}
    for (f0, f1), c in zip(pr, cls): kk = '%s:%s-%s' % (c, *sorted((PN[f0], PN[f1]))); bd[kk] = bd.get(kk, 0) + 1
    def pen(prs):
        if not len(prs): return 0.0
        n = fnorm(V); best = 0.0
        for f0, f1 in prs[:4000]:
            for fa, fb in ((f0, f1), (f1, f0)):
                d = (V[Q[fa]] - V[Q[fb]].mean(0)) @ n[fb]; best = max(best, float(-d.min()))
        return best * 10                                                       # mm
    out = dict(pose=name, intersections=dict(total=int(len(pr)), contact=int((cls == 'contact').sum()), crease=int((cls == 'crease').sum()), non_contact=int((cls == 'non-contact').sum()),
                                             crease_depth_mm=pen(pr[cls == 'crease']), contact_depth_mm=pen(pr[cls == 'contact']),
                                             by_pair=bd, non_contact_where=[dict(parts=[PN[a_], PN[b_]], at=np.round(C[a_], 1).tolist()) for a_, b_ in pr[cls == 'non-contact'][:12]]))
    # ---------- folds / flips
    N = fnorm(V); dot = (N[EFs[:, 0]] * N[EFs[:, 1]]).sum(1); fold = dot < -0.5; fe = EFs[fold, 0]
    inz = lambda f: np.linalg.norm(posed_c[None] - C[f][:, None], axis=2).min(1) <= Rz
    out['folds'] = dict(new=int(fold.sum() - FOLD0), in_crease=int(inz(fe).sum()) if len(fe) else 0, outside=int((~inz(fe)).sum()) if len(fe) else 0)
    Lf = Lin[Q].mean(1); Fl = np.diag([1.0, -1.0, 1.0]); ne = np.einsum('ij,fjk,kl,fl->fi', Fl, Lf, Fl, N0); ne /= np.maximum(np.linalg.norm(ne, axis=1), 1e-12)[:, None]
    flip = (N * ne).sum(1) < 0; out['flips'] = dict(total=int(flip.sum()), in_crease=int(inz(np.nonzero(flip)[0]).sum()) if flip.any() else 0)
    # ---------- volume, strain, zone
    ZG = {'D1': ('arm', 'axial'), 'D2': ('arm',), 'D3': ('arm', 'hand'), 'D4': ('hand', 'digit'), 'D5': ('hand', 'digit'), 'D6': ('leg', 'axial'), 'D7': ('leg',),
          'D8': ('leg', 'foot', 'digit'), 'D9': ('axial',), 'D10': ('axial',)}[tid]
    zf = (np.linalg.norm(C0[:, None] - jr[None], axis=2).min(1) <= Rz) & np.isin(PG, ZG) & np.isin(SIDE, [s, 'c'])   # zone = the tested segment's own tissue
    zone_v0 = sum(cone_vol(V0, np.nonzero(zf & (np.argmin(np.linalg.norm(C0[:, None] - jr[None], axis=2), 1) == i))[0], jr[i]) for i in range(len(jr)))
    zone_v1 = sum(cone_vol(V, np.nonzero(zf & (np.argmin(np.linalg.norm(C0[:, None] - jr[None], axis=2), 1) == i))[0], posed_c[i]) for i in range(len(jr)))
    Lp = np.linalg.norm(V[ue[:, 0]] - V[ue[:, 1]], axis=1); st = np.abs(Lp / L0 - 1); VZ = np.zeros(len(V0), bool); VZ[Q[zf].ravel()] = True; ze = VZ[ue[:, 0]] & VZ[ue[:, 1]]
    out['volume'] = dict(total_pct=100 * (volume(V) / VOL0 - 1), zone_pct=100 * (zone_v1 / zone_v0 - 1) if abs(zone_v0) > 1e-9 else None)
    out['strain'] = dict(zone_p95_pct=float(np.percentile(st[ze], 95) * 100) if ze.any() else 0.0, zone_max_pct=float(st[ze].max() * 100) if ze.any() else 0.0, global_max_pct=float(st.max() * 100))
    # ---------- loop spacing (consecutive loops of the zone; fixed nearest-vertex pairs from the rest pose)
    ls = {}
    for pre in lpre:
        pre = pre.format(s=s); ks = sorted([k for k in LOOPS if k.startswith(pre)], key=lambda k: (k.rsplit('_', 1)[0], float(k.rsplit('_', 1)[1]) if k.rsplit('_', 1)[1].replace('.', '').isdigit() else 0))
        for k1, k2 in zip(ks[:-1], ks[1:]):
            if k1.rsplit('_', 1)[0] != k2.rsplit('_', 1)[0]: continue
            a1, a2 = LOOPS[k1], LOOPS[k2]
            if not len(a1) or not len(a2): continue
            dd = np.linalg.norm(V0[a1][:, None] - V0[a2][None], axis=2); j2 = a2[dd.argmin(1)]; r0 = dd.min(1); r1 = np.linalg.norm(V[a1] - V[j2], axis=1)
            ok = r0 > 1e-4
            if ok.any(): ls['%s|%s' % (k1, k2)] = float((r1[ok] / r0[ok]).min())
    out['loop_spacing_min_ratio'] = min(ls.values()) if ls else None; out['loop_spacing_worst'] = min(ls, key=ls.get) if ls else None
    if tid in ('D4', 'D5'):
        out['nail_rigidity_mm'] = {f: kabsch_res(V0[ix], V[ix]) * 10 for f, ix in NAIL.items() if len(ix) >= 4 and (tid == 'D5') == (f == 'thumb')}
    if tid == 'D5':
        tip = lambda k, VV: VV[np.argmin(np.linalg.norm(V0 - J(k), axis=1))]
        tgt = 'index_tip_l' if 'pinch' in name else 'pinky_mcp_l'
        out['thumb_tip_to_target'] = dict(target=tgt, posed_cm=float(np.linalg.norm(tip('thumb_tip_l', V) - (tip(tgt, V) if tgt.endswith('tip_l') else bl_to_src(M['pinky_p1_l'][:3, 3][None])[0]))),
                                          rest_cm=float(np.linalg.norm(tip('thumb_tip_l', V0) - (tip(tgt, V0) if tgt.endswith('tip_l') else J(tgt)))), search=P.get('_D5_search'))
    # rest return (numpy LBS with the zero pose; Blender check in rig_check.py)
    Vr, _, _ = rig.skin(Vb0, {}); out['rest_return_T1_mm'] = float(np.linalg.norm(bl_to_src(Vr) - V0, axis=1).max() * 10)
    np.savez_compressed('%s/posed/%s%s.npz' % (O, name, os.environ.get('TAG', '')), V=V.astype(np.float32), Q=Q)
    return out
R = {}
for nm, pose in P.items():
    if nm.startswith('_'): continue
    if ONLY and not (nm in ONLY if os.environ.get('ONLY_EXACT') else any(nm.startswith(x) for x in ONLY)): continue
    R[nm] = measure(nm, pose); r = R[nm]
    print('%-18s int %4d (nc %d, crease %d / %.1fmm, contact %d) folds+%d out %d flips %d vol %+.2f%% zone %s strain p95 %.1f%% loop %s' % (nm, r['intersections']['total'], r['intersections']['non_contact'], r['intersections']['crease'], r['intersections']['crease_depth_mm'],
          r['intersections']['contact'], r['folds']['new'], r['folds']['outside'], r['flips']['total'], r['volume']['total_pct'], None if r['volume']['zone_pct'] is None else '%+.1f%%' % r['volume']['zone_pct'], r['strain']['zone_p95_pct'],
          None if r['loop_spacing_min_ratio'] is None else '%.2f' % r['loop_spacing_min_ratio']), flush=True)
json.dump(dict(poses={k: {b: [[ax, float(d)] for ax, d in rr] for b, rr in P[k].items()} for k in R}, results=R,
               nail_vertices={f: len(ix) for f, ix in NAIL.items()}, rest_folds=FOLD0), open(O + '/diag_results%s.json' % os.environ.get('TAG', ''), 'w'), indent=1, default=float)
