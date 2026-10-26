# helper_rig.py CONFIG.json OUTDIR : diagnostic elbow helper-volume rig (order 8e5021d §5). One helper bone per side, elbow_helper_{s}:
#   * child of forearm_{s}, rest matrix = forearm_{s} rest matrix (head = the elbow pivot) -> with zero activation it moves EXACTLY with the forearm,
#     so moving forearm weight onto it changes nothing below the activation threshold (no rest change, no pivot move, no length change);
#   * pose (diag_lib HELPER=...): counter-rotation back toward the elbow bisector by counter_fraction * beta(theta) * theta about the forearm flexion
#     axis, plus an optional small local translation beta * translate (cm, along the rest inner-crease direction 'inner' or the flexion axis 'axis');
#     beta = smoothstep(act_start, act_full, theta) (0 at <= act_start);
#   * optional flexion-driven local SCALE 1 + beta * scale_gain_local (X = the forearm flexion axis = medial-lateral): widens the helper-weighted
#     contact mass sideways so tissue displaced by contact is not simply removed (volume-preservation bulge, both sides at once);
#   * weights: the helper takes a share g(v) of the W0 forearm weight only, g = C2 bump of rest distance to the pivot (1 inside R_core, 0 at R_out)
#     x smooth inner/side mask on the angle around the elbow axis (the olecranon side keeps the forearm), with an exact-zero guard at the arm part seams.
#     Every other weight is untouched; row sums are unchanged.
# Writes OUTDIR/rig_h.json, OUTDIR/weights_H.npz, OUTDIR/helper_pose.json (diag_lib HELPER config), OUTDIR/helper_log.json.
import sys, os, json, hashlib, copy, numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import bl_to_src
from common import PARTS
CF, O = sys.argv[1:3]; CFG = json.load(open(CF)); os.makedirs(O, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; rig = json.load(open(RD + '/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
z = np.load(RD + '/rig/weights_v001c.npz'); W0 = z['W']; names = [str(n) for n in z['names']]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
vpart = np.empty(nV, object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); EL = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
G = sp.csr_matrix((np.r_[EL, EL], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
Wn = W0.astype(np.float64); newcols = []; LOG = dict(config=CFG, sides={}); HP = dict(sides={})
rig2 = copy.deepcopy(rig)
for s, hc in CFG['sides'].items():
    hd = lambda k: bl_to_src(np.array(B[k]['head'])[None])[0]; tl = lambda k: bl_to_src(np.array(B[k]['tail'])[None])[0]
    e = hd('forearm_' + s); ua = e - hd('upperarm_' + s); ua /= np.linalg.norm(ua); fa = tl('forearm_' + s) - e; fa /= np.linalg.norm(fa)
    ax = (ua + fa) / np.linalg.norm(ua + fa); ant = np.array([0, 1.0, 0]); ant -= (ant @ ax) * ax; ant /= np.linalg.norm(ant)
    d = np.linalg.norm(V0 - e, axis=1); arm = vpart == 'arm_' + s
    q = V0 - e; sa = q @ ax; rad = q - np.outer(sa, ax); cth = (rad @ ant) / np.maximum(np.linalg.norm(rad, axis=1), 1e-9)
    g = c2((hc['R_out'] - d) / (hc['R_out'] - hc['R_core'])) * c2((cth - hc['inner_cos_zero']) / (hc['inner_cos_full'] - hc['inner_cos_zero']))
    if hc.get('R_inner_full', 0) > 0:                                  # optional crease-core exclusion (H3): no helper share near the pivot
        g *= c2((d - hc['R_inner_zero']) / (hc['R_inner_full'] - hc['R_inner_zero']))
    g[~arm] = 0.0
    sup = g > 0; bnd = np.unique(np.r_[E[sup[E[:, 0]] & ~sup[E[:, 1]], 0], E[sup[E[:, 1]] & ~sup[E[:, 0]], 1]])
    seam = np.unique(np.r_[E[arm[E[:, 0]] & ~arm[E[:, 1]], 0], E[arm[E[:, 1]] & ~arm[E[:, 0]], 1]])            # arm part seams
    if len(seam):
        dist = dijkstra(G, directed=False, indices=seam, limit=hc.get('seam_guard_cm', 1.5) + 0.5, min_only=True)
        g *= c2(np.where(np.isfinite(dist), dist, 1e9) / hc.get('seam_guard_cm', 1.5))
    g *= hc.get('max_share', 1.0)
    jf = names.index('forearm_' + s); share = Wn[:, jf] * g; Wn[:, jf] -= share; newcols.append(('elbow_helper_' + s, share))
    # rig json: helper bone = forearm rest matrix, parent forearm
    fb = copy.deepcopy(B['forearm_' + s]); fb['name'] = 'elbow_helper_' + s; fb['parent'] = 'forearm_' + s; fb['deform'] = True
    rig2['bones'].append(fb); rig2['deform_order'].append(fb['name'])
    # pose config: translation in the bone-local frame (Blender pose location) from a rest-frame source direction
    Rl = np.array(B['forearm_' + s]['matrix_local'])[:3, :3]
    dsrc = {'inner': ant, 'axis': np.cross(ax, ant), 'none': np.zeros(3)}[hc.get('translate_dir', 'none')]
    dbl = np.array([dsrc[0], -dsrc[1], dsrc[2]]) * hc.get('translate_cm', 0.0) / 100.0
    HP['sides'][s] = dict(counter_fraction=hc['counter_fraction'], act_start=hc['act_start'], act_full=hc['act_full'], translate_local_m=(Rl.T @ dbl).tolist(),
                          scale_gain_local=hc.get('scale_gain_local', [0.0, 0.0, 0.0]))
    LOG['sides'][s] = dict(influence_vertices=int((share > 0).sum()), max_share=float(share.max()), share_sum=float(share.sum()), parts=sorted(set(vpart[share > 0])),
                           max_rest_dist_cm=float(d[share > 0].max()) if (share > 0).any() else 0.0, translate_local_m=HP['sides'][s]['translate_local_m'],
                           influence_ids_sha256=hashlib.sha256(np.nonzero(share > 0)[0].astype(np.int32).tobytes()).hexdigest())
Wn = np.c_[Wn, np.column_stack([c for _, c in newcols])]; names2 = names + [n for n, _ in newcols]
W32 = Wn.astype(np.float32)
LOG['row_sum_max_change'] = float(np.abs(W32.astype(np.float64).sum(1) - W0.astype(np.float64).sum(1)).max())
other = [i for i, n in enumerate(names) if not n.startswith('forearm_')]
LOG['non_forearm_columns_bit_identical'] = bool((W32[:, other].view(np.uint32) == W0[:, other].view(np.uint32)).all())
untouched = np.ones(nV, bool)
for _, c in newcols: untouched &= c == 0
LOG['rows_untouched_bit_identical'] = bool((W32[untouched][:, :len(names)].view(np.uint32) == W0[untouched].view(np.uint32)).all()) and bool((W32[untouched][:, len(names):] == 0).all())
LOG['weights_sha256'] = hashlib.sha256(np.ascontiguousarray(W32).tobytes()).hexdigest()
np.savez_compressed(O + '/weights_H.npz', W=W32, names=np.array(names2)); json.dump(rig2, open(O + '/rig_h.json', 'w'), indent=1)
json.dump(HP, open(O + '/helper_pose.json', 'w'), indent=1); json.dump(LOG, open(O + '/helper_log.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in LOG.items() if k != 'config'}, indent=1))
