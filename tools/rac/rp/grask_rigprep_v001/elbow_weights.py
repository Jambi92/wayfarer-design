# elbow_weights.py RIG.json PARENT.npz OUTDIR TAG MODE : LEFT-ELBOW-ONLY diagnostic weight candidate (order b303b9e §4).
# Support region: arm_l vertices within R_OUT of the left elbow pivot (connected elbow / upper-arm / forearm sleeve).
#   alpha = 1 inside R_CORE, smoothstep taper 1 -> 0 across the boundary band R_CORE..R_OUT, 0 outside (no hard cutoff).
# Target rows Wt: only the upperarm_l / forearm_l pair is re-split; the pair's total share P = W[upperarm] + W[forearm] of every vertex is
#   kept, every other bone's weight is untouched (so row sums and non-negativity are preserved exactly):
#   forearm = P * smoothstep(0.5 + 0.5 * s / h(theta)),  upperarm = P - forearm,   s = signed distance along the elbow bisector axis.
#   MODE uniform : h = 4.5 cm all round (regularises the bone-heat split, whose inner/outer spread is 0.17..0.53 at one axial slab).
#   MODE crease  : h = 6.0 cm on the flexor (anterior, inner-crease) side, 3.0 cm on the extensor (olecranon) side, cosine-interpolated
#                  around the axis (spreads inner-crease compression over more loops, keeps the outer contour on the forearm).
# Final W = W_parent + alpha * (Wt - W_parent); every vertex outside the support is copied bit-identical from the parent.
# Writes weights_TAG.npz, weights_TAG_log.json (region, band, per-bone deltas, boundary-continuity checks), weights_TAG_maps.npz.
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import bl_to_src
from common import PARTS
RJ, PF, O, TAG, MODE = sys.argv[1:6]; os.makedirs(O, exist_ok=True)
R_CORE, R_OUT = 9.0, 13.0
rig = json.load(open(RJ)); B = {b['name']: b for b in rig['bones']}
hd = lambda k: bl_to_src(np.array(B[k]['head'])[None])[0]; tl = lambda k: bl_to_src(np.array(B[k]['tail'])[None])[0]
z = np.load(PF); W0 = z['W']; assert W0.dtype == np.float32; names = [str(n) for n in z['names']]; iu, ifo = names.index('upperarm_l'), names.index('forearm_l')
M = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = M['V'].astype(float); Q = np.asarray(M['Q']); FP = M['FP']
vpart = np.empty(len(V), object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
e = hd('forearm_l'); ua = e - hd('upperarm_l'); ua /= np.linalg.norm(ua); fa = tl('forearm_l') - e; fa /= np.linalg.norm(fa); ax = ua + fa; ax /= np.linalg.norm(ax)
ant = np.array([0, 1.0, 0]); ant -= (ant @ ax) * ax; ant /= np.linalg.norm(ant)                   # flexor side = forward (+f) normal to the axis
ss = lambda x: (lambda c: c * c * (3 - 2 * c))(np.clip(x, 0, 1))
d = np.linalg.norm(V - e, axis=1); sup = (vpart == 'arm_l') & (d < R_OUT)
import collections
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
def components(mask):
    adj = collections.defaultdict(list)
    for a, b in E[mask[E[:, 0]] & mask[E[:, 1]]]: adj[a].append(b); adj[b].append(a)
    seen = set(); out = []
    for v in np.nonzero(mask)[0]:
        if v in seen: continue
        c = [v]; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y); c.append(y)
        out.append(c)
    return out
cs = components(sup); dropped = [c for c in cs if len(c) < max(map(len, cs))]
for c in dropped: sup[c] = False                                     # keep the single connected elbow sleeve (drop stray arm_l islands)
vi = np.nonzero(sup)[0]
alpha = np.zeros(len(V)); alpha[vi] = 1 - ss((d[vi] - R_CORE) / (R_OUT - R_CORE))
q = V[vi] - e; s = q @ ax; rad = q - np.outer(s, ax); rn = np.maximum(np.linalg.norm(rad, axis=1), 1e-9); cth = (rad @ ant) / rn   # +1 inner crease, -1 olecranon
if MODE == 'uniform': h = np.full(len(vi), 4.5)
elif MODE == 'crease': h = 4.5 + 1.5 * cth
else: raise SystemExit('MODE')
Wd = W0[vi].astype(np.float64); P = Wd[:, iu] + Wd[:, ifo]; wf = P * ss(0.5 + 0.5 * s / h); Wt = Wd.copy(); Wt[:, ifo] = wf; Wt[:, iu] = P - wf
Wn = Wd + alpha[vi, None] * (Wt - Wd)
W = W0.copy(); W[vi] = Wn.astype(np.float32)
# exact row-sum: put float32 rounding residue of the pair on the larger pair member (only inside the support)
r = W0[vi].astype(np.float64).sum(1) - W[vi].astype(np.float64).sum(1); big = np.where(W[vi, iu] >= W[vi, ifo], iu, ifo); W[vi, big] = (W[vi, big].astype(np.float64) + r).astype(np.float32)
same = (W.view(np.uint32) == W0.view(np.uint32)).all(1)
assert same[~sup].all() and (W >= 0).all()
D = W.astype(np.float64) - W0.astype(np.float64)
de = np.abs(D[E[:, 0]] - D[E[:, 1]]).max(1)                                                         # per-edge change in delta (max over bones)
band = lambda a, b: ((d[E[:, 0]] >= a) & (d[E[:, 0]] < b)) | ((d[E[:, 1]] >= a) & (d[E[:, 1]] < b))
inS = sup[E[:, 0]] | sup[E[:, 1]]; cross = sup[E[:, 0]] ^ sup[E[:, 1]]
LOG = dict(tag=TAG, mode=MODE, parent=os.path.basename(PF), parent_sha256=hashlib.sha256(np.ascontiguousarray(W0).tobytes()).hexdigest(),
           method=open(__file__).read().split('import sys')[0], elbow_pivot_src_cm=e.tolist(), bisector_axis=ax.tolist(), flexor_direction=ant.tolist(),
           support=dict(part='arm_l', core_radius_cm=R_CORE, outer_radius_cm=R_OUT, vertices=int(sup.sum()), core_vertices=int((sup & (d <= R_CORE)).sum()),
                        band_vertices=int((sup & (d > R_CORE)).sum()), connected_components=None),
           half_width_cm=dict(min=float(h.min()), max=float(h.max())), changed_vertices=int((~same).sum()),
           max_abs_delta=dict(upperarm_l=float(np.abs(D[:, iu]).max()), forearm_l=float(np.abs(D[:, ifo]).max()), other_bones=float(np.abs(np.delete(D, [iu, ifo], 1)).max())),
           row_sum_max_abs_change=float(np.abs(W.astype(np.float64).sum(1) - W0.astype(np.float64).sum(1)).max()), negative=int((W < 0).sum()),
           non_support_rows_bit_identical=bool(same[~sup].all()),
           boundary=dict(max_edge_delta_change_core=float(de[inS & band(0, R_CORE)].max()), max_edge_delta_change_band=float(de[inS & band(R_CORE, R_OUT)].max()),
                         max_edge_delta_change_on_support_boundary_edges=float(de[cross].max()) if cross.any() else 0.0, support_boundary_edges=int(cross.sum()),
                         max_abs_delta_in_outer_1cm_of_band=float(np.abs(D[sup & (d > R_OUT - 1)]).max()), max_edge_delta_change_anywhere=float(de.max())),
           weights_sha256=hashlib.sha256(np.ascontiguousarray(W).tobytes()).hexdigest())
comp = len(components(sup)); LOG['support']['dropped_islands'] = [dict(vertices=len(c), ids=[int(x) for x in c]) for c in dropped]
LOG['support']['connected_components'] = comp
np.savez_compressed(os.path.join(O, 'weights_%s.npz' % TAG), W=W, names=np.array(names))
np.savez_compressed(os.path.join(O, 'weights_%s_maps.npz' % TAG), alpha=alpha.astype(np.float32), dU=D[:, iu].astype(np.float32), dF=D[:, ifo].astype(np.float32),
                    support=sup, edge_delta_change=de.astype(np.float32), edges=E.astype(np.int32))
json.dump(LOG, open(os.path.join(O, 'weights_%s_log.json' % TAG), 'w'), indent=1)
print(TAG, MODE, 'support', sup.sum(), 'components', comp, 'changed', (~same).sum(), 'max|d| U %.3f F %.3f' % (LOG['max_abs_delta']['upperarm_l'], LOG['max_abs_delta']['forearm_l']), json.dumps(LOG['boundary']))
