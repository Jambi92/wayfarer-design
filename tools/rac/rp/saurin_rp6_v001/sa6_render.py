# sa6_render.py W_M.npz W_F.npz CF_M.json CF_F.json OUTDIR : RP6 visual evidence package (order a407015 §24), matched c1 / c2.
#   Software renderer (matplotlib polygons, painter's order, Lambert shading; flipped quads red, interpenetrating vertices' quads orange, weights / corrective
#   magnitudes as heat maps).  Every image is generated from the same evaluator used by the audit (sa6_pose + sa6_correctives) - no separate pose code.
import sys, os, json, numpy as np, igl, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_fit as FT
WM, WF, CM, CFF, OD = sys.argv[1:6]; os.makedirs(OD, exist_ok=True)
RIG = {}; COR = {}
for cfg, wf, cf in (('M', WM, CM), ('F', WF, CFF)): RIG[cfg] = SP.Rig(cfg, wf); COR[cfg] = CC.Correctives.load(RIG[cfg], cf)
F3 = None
def view_basis(v):
    v = np.asarray(v, float); v /= np.linalg.norm(v); up = np.array([0, 0, 1.0]) if abs(v[2]) < 0.95 else np.array([0, 1.0, 0]); x = np.cross(up, v); x /= np.linalg.norm(x); y = np.cross(v, x); return x, y, v
def draw(ax, R, P, view, centre=None, rad=None, qcol=None, title='', flips=None, pen=None, bones=None, T=None, cmap=None, vals=None, vmax=None):
    Q = R.Q; x, y, v = view_basis(view); qc = P[Q].mean(1)
    m = np.ones(len(Q), bool) if centre is None else np.linalg.norm(qc - centre, axis=1) < rad
    n = np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    front = (n @ v) > -0.05 if centre is None else np.ones(len(Q), bool)
    m &= front; idx = np.nonzero(m)[0]; dep = qc[idx] @ v; idx = idx[np.argsort(dep)]
    pts = np.stack([P[Q[idx]] @ x, P[Q[idx]] @ y], -1); sh = 0.35 + 0.65 * np.abs(n[idx] @ (0.6 * v + 0.4 * y) / np.linalg.norm(0.6 * v + 0.4 * y))
    if vals is not None:
        cm = plt.get_cmap(cmap or 'viridis'); c = cm(np.clip(vals[idx] / (vmax or max(vals.max(), 1e-9)), 0, 1)); c[:, :3] *= sh[:, None] * 0.5 + 0.5
    else:
        c = np.c_[np.repeat(sh[:, None], 3, 1) * [0.82, 0.8, 0.76], np.ones(len(idx))]
    if pen is not None: pq = pen[Q[idx]].any(1); c[pq] = [1.0, 0.6, 0.1, 1]
    if flips is not None: fq = np.isin(idx, flips); c[fq] = [0.9, 0.05, 0.05, 1]
    pc = PolyCollection(pts, facecolors=c, edgecolors=(0, 0, 0, 0.12 if centre is not None else 0.0), linewidths=0.15); ax.add_collection(pc)
    if bones is not None:
        segs = [];
        for b in bones:
            h, t = R.H(b), R.Tl(b)
            if T is not None: h, t = T[b][0] @ h + T[b][1], T[b][0] @ t + T[b][1]
            segs.append([[h @ x, h @ y], [t @ x, t @ y]])
        ax.add_collection(LineCollection(segs, colors='tab:blue', linewidths=1.2)); hs = np.array([s_[0] for s_ in segs]); ax.scatter(hs[:, 0], hs[:, 1], s=4, c='navy', zorder=5)
    ax.autoscale(); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=8)
def posed(cfg, spec, corr=True):
    R = RIG[cfg]; T = R.pose(spec); d = COR[cfg].delta(T) if corr else 0 * R.V; P = R.skin(T, R.V + d); fl = np.nonzero(R.relcos(P, T) < 0)[0]
    Ft = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64)
    return R, T, P, fl, FT.penetration(R, P, Ft, FT.wn_out(R.V, Ft)), d
def fig_pairs(name, items, ncol=None):
    """items: list of (cfg, pose_spec_name_or_None, view, centre_fn, rad, kwargs) -> one row per item pair"""
    n = len(items); ncol = ncol or min(n, 4); nrow = (n + ncol - 1) // ncol
    f, axs = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 4.2 * nrow)); axs = np.atleast_1d(axs).ravel()
    for a, it in zip(axs, items): it(a)
    for a in axs[n:]: a.axis('off')
    plt.tight_layout(); f.savefig(os.path.join(OD, name), dpi=110); plt.close(f); print('wrote', name, flush=True)
PS = {c: FT.pose_set(RIG[c]) for c in 'MF'}
for c in 'MF': PS[c]['jaw_open_20_rp5lit'] = RIG[c].suite('rp5')['jaw_open_20']
def item(cfg, pn, view, centre=None, rad=None, corr=True, label='', heat=None, bones=None, frac=1.0):
    def f(ax):
        spec = [] if pn is None else [(b, p, a, d * frac) for b, p, a, d in PS[cfg][pn]]; R, T, P, fl, pen, dl = posed(cfg, spec, corr)
        ctr = None if centre is None else (T[centre][0] @ R.H(centre) + T[centre][1] if isinstance(centre, str) else np.asarray(centre))
        kw = {}
        if heat == 'corr': kw = dict(vals=np.linalg.norm(dl, axis=1)[R.Q].mean(1), cmap='magma', vmax=max(0.05, np.linalg.norm(dl, axis=1).max()))
        elif heat: kw = dict(vals=R.W[:, R.bi[heat]][R.Q].mean(1), cmap='viridis', vmax=1.0)
        draw(ax, R, P, view, ctr, rad, title='%s %s %s%s | flips %d pen %d' % ('c1 SA-M188' if cfg == 'M' else 'c2 SA-F188', pn or 'reference', label, '' if corr else ' (LBS only)', len(fl), pen.sum()),
             flips=fl, pen=pen, bones=bones, T=T, **kw)
    return f
FR, PR, TQ, BK = (0, 1, 0), (1, 0, 0), (0.7, 0.7, 0.2), (0, -1, 0)
both = lambda fn: [fn('M'), fn('F')]
deform = [b for b in RIG['M'].DB]
fig_pairs('01_reference_stance.png', sum([[item(c, None, FR), item(c, None, PR)] for c in 'MF'], []))
# rig-prep
for c in 'MF':
    rp = json.load(open(C.EV6 + '/SA_RP6_rig_prep_%s_v001.json' % c)); PS[c]['rig_prep'] = [(b, RIG[c].H(b), v['axis_world'], v['rotation_deg']) for b, v in rp['rig_prep_stance'].items()]
fig_pairs('02_rig_prep_stance.png', sum([[item(c, 'rig_prep', FR), item(c, 'rig_prep', PR)] for c in 'MF'], []))
fig_pairs('03_skeleton_overlay.png', sum([[item(c, None, v, bones=deform) for v in (FR, PR, TQ)] for c in 'MF'], []), ncol=3)
fig_pairs('04_shoulder_45_90.png', sum([[item(c, 'shoulder_abd45_xpos', FR, 'upperarm_l', 22), item(c, 'shoulder_abd90_xpos', FR, 'upperarm_l', 22), item(c, 'shoulder_abd90_xpos', BK, 'upperarm_l', 22, label='back')] for c in 'MF'], []), ncol=3)
fig_pairs('05_elbow_90_130.png', sum([[item(c, 'elbow_90_xpos', PR, 'forearm_l', 14), item(c, 'elbow_130_xpos', PR, 'forearm_l', 14), item(c, 'elbow_130_xpos', (-1, 0.3, 0), 'forearm_l', 14, label='medial')] for c in 'MF'], []), ncol=3)
for nm, pn in (('06_fist.png', 'fist_xpos'), ('07_grasp.png', 'grasp_xpos'), ('08_thumb_opposition.png', 'thumb_opposition_xpos')):
    fig_pairs(nm, sum([[item(c, pn, (0.3, 0.2, -1), 'hand_l', 13, label='palm'), item(c, pn, (0.3, 0.2, 1), 'hand_l', 13, label='dorsal'), item(c, pn, PR, 'hand_l', 13, label='side')] for c in 'MF'], []), ncol=3)
fig_pairs('09_hip_flexion.png', sum([[item(c, 'hip_flex70_xpos', PR, 'thigh_l', 26), item(c, 'hip_flex70_xpos', (0.3, 1, -0.2), 'thigh_l', 26, label='groin')] for c in 'MF'], []), ncol=2)
fig_pairs('10_knee.png', sum([[item(c, 'knee_90_xpos', PR, 'shin_l', 20), item(c, 'knee_90_xpos', BK, 'shin_l', 20, label='back'), item(c, 'knee_90_xpos', PR, 'shin_l', 20, corr=False)] for c in 'MF'], []), ncol=3)
fig_pairs('11_ankle_toes.png', sum([[item(c, 'ankle_dorsi20_xpos', PR, 'foot_l', 16), item(c, 'toe_flex30_xpos', PR, 'foot_l', 16), item(c, 'toe_ext30_xpos', PR, 'foot_l', 16), item(c, 'gate:foot_pushoff_xpos', PR, 'foot_l', 16)] for c in 'MF'], []), ncol=4)
fig_pairs('12_trunk_flex_twist.png', sum([[item(c, 'lower_axial_flex_25', PR), item(c, 'trunk_twist_30', FR)] for c in 'MF'], []), ncol=2)
fig_pairs('13_tail.png', sum([[item(c, 'tail_root_lateral_30', (0, 0, 1)), item(c, 'tail_root_vertical_25', PR), item(c, 'tail_twist_30', BK, 'tail_01', 30), item(c, 'gate:tail_lat_135', (0, 0, 1)), item(c, 'gate:tail_S_curve', (0, 0, 1)), item(c, 'gate:tail_combined', TQ)] for c in 'MF'], []), ncol=6)
fig_pairs('14_jaw_open.png', sum([[item(c, 'gate:jaw_open_8', PR, 'jaw', 14), item(c, 'jaw_open_20', PR, 'jaw', 14), item(c, 'gate:jaw_open_32', PR, 'jaw', 14), item(c, 'gate:jaw32_head_pitch_up', TQ, 'jaw', 16)] for c in 'MF'], []), ncol=4)
# worst residual before / after: chosen from the audit (largest LBS flip count among required-suite poses)
au = {c: json.load(open(os.path.join(C.EV6, 'SA_RP6_deformation_audit_v001.json')))['configurations'][c]['poses'] for c in ('c1', 'c2')} if os.path.exists(os.path.join(C.EV6, 'SA_RP6_deformation_audit_v001.json')) else None
worst = max([k for k in PS['M'] if not k.startswith('gate:') and k != 'jaw_open_20_rp5lit'], key=lambda k: au['c1'][k]['step3_lbs_flips'] if au else 0) if au else 'fist_xpos'
ctr = {'fist': 'hand_l', 'grasp': 'hand_l', 'knee': 'shin_l', 'elbow': 'forearm_l', 'hip': 'thigh_l', 'tail': 'tail_01', 'jaw': 'jaw', 'toe': 'foot_l', 'ankle': 'foot_l', 'shoulder': 'upperarm_l'}
cb = next((v for k, v in ctr.items() if worst.startswith(k)), None); cb = cb.replace('_l', '_r') if (cb and worst.endswith('xneg')) else cb
fig_pairs('15_worst_residual_before_corrective.png', [item(c, worst, (0.3, 0.2, -1) if 'fist' in worst or 'grasp' in worst else PR, cb, 14, corr=False) for c in 'MF'], ncol=2)
fig_pairs('16_worst_residual_after_corrective.png', [item(c, worst, (0.3, 0.2, -1) if 'fist' in worst or 'grasp' in worst else PR, cb, 14) for c in 'MF'], ncol=2)
fig_pairs('17_weight_heatmaps.png', sum([[item(c, None, FR, 'upperarm_l', 18, heat='upperarm_l', label='upperarm_l (axilla)'), item(c, None, (0.3, 0.2, -1), 'hand_l', 12, heat='thumb_01_l', label='thumb_01_l'),
                                          item(c, None, (0.3, 0.2, -1), 'hand_l', 12, heat='finger_2_01_l', label='finger_2_01_l (web)'), item(c, None, PR, 'thigh_l', 22, heat='thigh_l', label='thigh_l (groin)'),
                                          item(c, None, (0, 0, 1), 'tail_01', 20, heat='tail_01', label='tail_01 (root)'), item(c, None, PR, 'jaw', 12, heat='jaw', label='jaw (mouth)')] for c in 'MF'], []), ncol=6)
fig_pairs('18_corrective_heatmaps.png', sum([[item(c, 'knee_90_xpos', PR, 'shin_l', 20, heat='corr'), item(c, 'fist_xpos', (0.3, 0.2, -1), 'hand_l', 13, heat='corr'), item(c, 'shoulder_abd90_xpos', FR, 'upperarm_l', 22, heat='corr'),
                                              item(c, 'tail_root_lateral_30', (0, 0, 1), 'tail_01', 25, heat='corr')] for c in 'MF'], []), ncol=4)
# 19 c1 / c2 comparison: overlay of the two neutral silhouettes + joint offsets
def c1c2(ax):
    x, y, v = view_basis(FR)
    for c, col in (('M', 'tab:blue'), ('F', 'tab:red')):
        R = RIG[c]; ax.scatter(R.V[::7] @ x, R.V[::7] @ y, s=0.05, c=col, alpha=0.4); hs = np.array([R.H(b) for b in R.DB]); ax.scatter(hs @ x, hs @ y, s=5, c=col, marker='x')
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title('c1 (blue) / c2 (red) neutral + joints (front)', fontsize=8)
def c1c2p(ax):
    x, y, v = view_basis(PR)
    for c, col in (('M', 'tab:blue'), ('F', 'tab:red')):
        R = RIG[c]; ax.scatter(R.V[::7] @ x, R.V[::7] @ y, s=0.05, c=col, alpha=0.4); hs = np.array([R.H(b) for b in R.DB]); ax.scatter(hs @ x, hs @ y, s=5, c=col, marker='x')
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title('c1 (blue) / c2 (red) neutral + joints (profile)', fontsize=8)
fig_pairs('19_c1_c2_comparison.png', [c1c2, c1c2p, item('M', 'fist_xpos', (0.3, 0.2, -1), 'hand_l', 13), item('F', 'fist_xpos', (0.3, 0.2, -1), 'hand_l', 13)], ncol=4)
# 20 neutral overlay: RP6 Blender read-back vs frozen RP5 (displacement heat, expected 0 up to float32)
def neutral(cfg):
    def f(ax):
        R = RIG[cfg]
        fp = os.path.join(os.environ.get('RB_DIR', '/tmp/claude-0/rp6'), 'neutral_disp_%s.npy' % cfg); disp = np.load(fp)   # written by sa6_blend_readback.py
        draw(ax, R, R.V, FR, vals=disp[R.Q].mean(1), cmap='magma', vmax=1e-4, title='%s neutral: RP6 .blend read-back vs frozen RP5, |d| max %.2e cm (scale 1e-4 cm)' % (cfg, disp.max()))
    return f
fig_pairs('20_neutral_overlay.png', [neutral('M'), neutral('F')], ncol=2)
# ownership evidence for non-rig residual classes: contact (knee / elbow 130) and the RP5-literal jaw closure
fig_pairs('21_contact_ownership.png', sum([[item(c, 'knee_90_xpos', PR, 'shin_l', 14, corr=False, label='LBS: interpenetration (orange)'), item(c, 'knee_90_xpos', PR, 'shin_l', 14, label='contact corrective'),
                                             item(c, 'elbow_130_xpos', PR, 'forearm_l', 12, corr=False), item(c, 'elbow_130_xpos', PR, 'forearm_l', 12), item(c, 'jaw_open_20_rp5lit', PR, 'jaw', 12, corr=False, label='RP5-literal +20 = closure')] for c in 'MF'], []), ncol=5)
