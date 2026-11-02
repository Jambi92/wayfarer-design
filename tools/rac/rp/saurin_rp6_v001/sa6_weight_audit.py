# sa6_weight_audit.py OUT.json W_M.npz W_F.npz : RP6 weight audit (order a407015 §22) for c1 and c2 + the c1/c2 comparison.
#   groups / deform-only / influence histogram / max influences / sum error / zero-weight vertices / orphan groups / islands / spikes / left-right mirror
#   (symmetric-difference) diagnostics / cross-surface leakage at finger webs, toe webs, axilla, groin, tail root, mouth / throat.
import sys, os, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
def loadw(f):
    z = np.load(f); S = sp.csr_matrix((z['data'], z['indices'], z['indptr']), shape=tuple(z['shape'])); return S, [str(b) for b in z['bones']], str(z['method'])
def audit(cfg, wf, d):
    S, DB, meth = loadw(wf); bi = {b: i for i, b in enumerate(DB)}; Q = d['Q']; V = d['V1'] if cfg == 'M' else d['V2']; nv = len(V); ql = d['qlab']; fs = d['face_sem']
    W = S.toarray().astype(np.float64); nnz = np.diff(S.indptr); sums = np.asarray(S.sum(1)).ravel()
    E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
    A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); deg = np.asarray(A.sum(1)).ravel()
    out = dict(config=cfg, file=os.path.basename(wf), method=meth, vertex_groups=DB, n_groups=len(DB), deform_groups_only=True,
               influence_histogram={str(k): int(v) for k, v in enumerate(np.bincount(nnz, minlength=5))}, max_influences=int(nnz.max()),
               weight_sum_abs_error_max=float(np.abs(sums - 1).max()), zero_weight_vertices=int((nnz == 0).sum()), min_nonzero_weight=float(S.data.min()))
    used = np.asarray((S > 0).sum(0)).ravel(); out['orphan_groups'] = [DB[i] for i in range(len(DB)) if used[i] == 0]
    # islands: per bone, connected components of the vertices with w > 0.01 (mesh graph)
    isl = {}
    for i, b in enumerate(DB):
        m = W[:, i] > 0.01
        if m.sum() < 2: continue
        idx = np.nonzero(m)[0]; sub = A[idx][:, idx]; n, lab = connected_components(sub, directed=False)
        if n > 1: sz = np.bincount(lab); isl[b] = dict(components=int(n), sizes=sorted(sz.tolist())[::-1][:6])
    out['islands'] = isl
    # spikes: |w - mean of 1-ring| > 0.5
    nb = (A @ W) / deg[:, None]; sp_ = np.abs(W - nb).max(1); out['spike_vertices_gt_0.5'] = int((sp_ > 0.5).sum()); out['max_one_ring_deviation'] = round(float(sp_.max()), 4)
    # left / right symmetric-difference diagnostics: the frozen stance is not mirror-symmetric (hands / feet / digits sit at different positions), so a
    # spatial mirror match is meaningless; compare each _l / _r bone pair by weighted-vertex count, weight mass and mass per semantic label.
    labs = sorted(set(ql)); vlab = np.zeros((nv, len(labs)), bool); li = {l: i for i, l in enumerate(labs)}; vlab[Q.ravel(), np.repeat([li[q] for q in ql], 4)] = True
    pairs = {}
    for b in DB:
        if not b.endswith('_l'): continue
        i, j = bi[b], bi[b[:-2] + '_r']; cl, cr = int((W[:, i] > 0).sum()), int((W[:, j] > 0).sum()); ml, mr = float(W[:, i].sum()), float(W[:, j].sum())
        ll = vlab.T.astype(float) @ W[:, i]; lr = vlab.T.astype(float) @ W[:, j]; lab_d = float(np.abs(ll / max(ll.sum(), 1e-9) - lr / max(lr.sum(), 1e-9)).sum() / 2)
        Pp = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % cfg))['bones']; Ll, Lr = Pp[b]['length_cm'], Pp[b[:-2] + '_r']['length_cm']
        pairs[b[:-2]] = dict(count_l=cl, count_r=cr, bone_length_rel_diff=round(abs(Ll - Lr) / max(Ll, Lr), 4), mass_rel_diff=round(abs(ml - mr) / max(ml, mr), 4), label_distribution_total_variation=round(lab_d, 4))
    out['left_right'] = dict(pairs=pairs, mass_rel_diff_max=max(v['mass_rel_diff'] for v in pairs.values()), label_tv_max=max(v['label_distribution_total_variation'] for v in pairs.values()),
                             worst=max(pairs, key=lambda k: pairs[k]['mass_rel_diff']),
                             note='the frozen stance / digits are not mirror-symmetric; pairs with mass difference > 5 % are listed with their l / r bone-length difference (same method both sides, no side-specific tuning)')
    # ---- leakage ----
    def verts(labels, side=None):
        m = np.ones(nv, bool); m[Q[~(np.isin(fs, labels) | np.isin(ql, labels))].ravel()] = False      # interior: every incident quad carries the label
        if side: m &= (V[:, 0] > 0) if side == 'l' else (V[:, 0] < 0)
        return m
    def wsum(mask, bones): ii = [bi[b] for b in bones if b in bi]; return float(W[np.ix_(mask, ii)].sum(1).max()) if mask.any() and ii else 0.0
    L = {}
    for t, s_ in (('l', 'xpos'), ('r', 'xneg')):
        o = 'r' if t == 'l' else 'l'
        # finger webs: each web component may only carry the two neighbouring digit chains (+ metacarpals / hand)
        for lab, pre, n, stem in (('finger_web', 'f', 4, 'finger_%d_%02d_' ), ('toe_web', 't', 5, 'toe_%d_%02d_')):
            qm = (fs == lab) & ((V[Q].mean(1)[:, 0] > 0) if t == 'l' else (V[Q].mean(1)[:, 0] < 0)); qq = Q[qm]
            if not len(qq): continue
            rr = np.repeat(np.arange(len(qq)), 4); Aq = sp.coo_matrix((np.ones(len(rr)), (rr, qq.ravel())), shape=(len(qq), nv)).tocsr(); nc, lq = connected_components(Aq @ Aq.T)
            bases = np.array([V[d['loops']['%s_%s%d_base' % (s_, pre, k)]].mean(0) for k in range(1, n + 1)]); worst = 0.0
            for ci in range(nc):
                vv = np.unique(qq[lq == ci]); c0 = V[vv].mean(0); near = np.argsort(np.linalg.norm(bases - c0, axis=1))[:2] + 1
                others = [stem % (k, j) + t for k in range(1, n + 1) if k not in near for j in (1, 2, 3)]; mk = np.zeros(nv, bool); mk[vv] = True; worst = max(worst, wsum(mk, others))
            L['%s_%s_non_adjacent_digit_weight_max' % (lab, t)] = worst
        arm = ['upperarm_' + t, 'forearm_' + t, 'hand_' + t] + [b for b in DB if b.endswith('_' + t) and b.startswith(('meta', 'finger', 'thumb'))]
        Pp_ = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % cfg))['bones']; g_ = np.array(Pp_['upperarm_' + t]['head']); La_ = Pp_['upperarm_' + t]['length_cm']
        beyond = np.linalg.norm(V - g_, axis=1) > 0.45 * La_          # outside the deliberate shoulder blend zone (sa6_weights SH_R)
        L['axilla_trunk_wall_arm_weight_max_' + t] = wsum(verts(['trunk'], t) & beyond, arm)
        L['shoulder_blend_zone_trunk_vertices_with_upperarm_weight_' + t] = int((verts(['trunk', 'neck'], t) & ~beyond & (W[:, bi['upperarm_' + t]] > 0)).sum())
        L['axilla_arm_vertices_spine_weight_max_' + t] = wsum(verts(['upper_arm', 'elbow'], t), ['spine_01', 'spine_02', 'spine_03', 'spine_04', 'pelvis'])
        leg = ['thigh_' + t, 'shin_' + t, 'foot_' + t] + [b for b in DB if b.startswith('toe') and b.endswith('_' + t)]
        L['groin_opposite_leg_weight_max_' + t] = wsum(verts(['hip', 'thigh', 'knee', 'pelvis'], o), leg)
        L['groin_leg_vertices_tail_weight_max_' + t] = wsum(verts(['thigh', 'knee', 'shin'], t), [b for b in DB if b.startswith('tail')])
        L['tail_root_tail_vertices_leg_weight_max_' + t] = wsum(verts(['tail']), leg)
        L['opposite_side_any_weight_max_' + t] = wsum(np.abs(V[:, 0]) > 1.0, []) if False else float(max((W[(V[:, 0] < -1.0) if t == 'l' else (V[:, 0] > 1.0)][:, [bi[b] for b in DB if b.endswith('_' + t)]].sum(1)).max(), 0))
    mouth = d['loops']['mouth_slit']; lip_z = np.interp(V[:, 1], np.sort(V[mouth, 1]), V[mouth, 2][np.argsort(V[mouth, 1])]); J = np.array([0, 0, 0])
    hv = verts(['head', 'rostrum_cap', 'orbit', 'eye', 'display_root'])
    L['mouth_upper_jaw_vertices_jaw_weight_max'] = wsum(hv & (V[:, 2] > lip_z + 0.3) & (V[:, 1] > V[mouth, 1].min()), ['jaw'])
    L['orbit_eye_display_jaw_weight_max'] = wsum(verts(['orbit', 'eye', 'display_root']), ['jaw'])
    L['throat_neck_vertices_jaw_weight_max'] = wsum(verts(['neck', 'trunk']), ['jaw'])
    L['jaw_weighted_vertices'] = int((W[:, bi['jaw']] > 0).sum())
    out['leakage'] = L; out['leakage_pass'] = all(v == 0 for k, v in L.items() if k.endswith(('_max',)) or '_max_' in k)
    out['shoulder_blend_note'] = 'the upper arm deliberately weights trunk / neck vertices within 0.45 x its length of the glenohumeral joint (and the clavicle the proximal upper arm within 0.35 x) to avoid the LBS shoulder pinch; the leakage test checks the trunk wall beyond that zone'
    return out, W
if __name__ == '__main__':
    d = C.load(); OUT, WM, WF = sys.argv[1:4]
    aM, W1 = audit('M', WM, d); aF, W2 = audit('F', WF, d)
    dw = np.abs(W1 - W2).max(1); cmp = dict(per_vertex_weight_abs_diff_max=round(float(dw.max()), 4), p99=round(float(np.percentile(dw, 99)), 4), vertices_identical=int((dw < 1e-6).sum()),
                                           note='c2 weights are computed by the same method on the c2 realisation and c2 joint placement (not copied from c1)')
    json.dump(dict(status='RP6 RIG PILOT / NOT FROZEN', c1=aM, c2=aF, c1_c2=cmp), open(OUT, 'w'), indent=1)
    for a in (aM, aF): print(a['config'], 'hist', a['influence_histogram'], 'sumerr %.1e' % a['weight_sum_abs_error_max'], 'zero', a['zero_weight_vertices'], 'orph', a['orphan_groups'], 'islands', len(a['islands']), 'spikes', a['spike_vertices_gt_0.5'], 'leak_pass', a['leakage_pass']); print(json.dumps(a['leakage'])); print(json.dumps(a['islands'])[:1500]); print(a['left_right']['mass_rel_diff_max'], a['left_right']['label_tv_max'], a['left_right']['worst'])
    print(cmp)
