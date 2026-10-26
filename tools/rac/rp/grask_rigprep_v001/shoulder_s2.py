# shoulder_s2.py CONFIG.json OUTDIR : Track S (order 69f2660 §14) S2 bounded diagnostic shoulder / axillary weighting comparison (on top of S1 mechanics).
# W0 weights are diffused (k_iters of 0.5 * self + 0.5 * one-ring mean, all bone columns together -> rows stay normalised) and blended back with a
# bounded region mask g(v) = C2 bump of the rest distance to the GH centre (1 inside R_core, 0 at R_out) restricted to the shoulder girdle parts
# (arm_s and axial); optional front_only multiplies a smooth anterior mask (the D1 flex90 failure sits in front of GH). Every vertex with g = 0 keeps its
# W0 row bit-identical. No new bones, no pivot, landmark or rest change. Not production weight sculpting.
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
CF, O = sys.argv[1:3]; CFG = json.load(open(CF)); os.makedirs(O, exist_ok=True)
RD = '/tmp/claude-0/rt/rd'; z = np.load(RD + '/rig/weights_v001c.npz'); W0 = z['W']; names = [str(n) for n in z['names']]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']; nV = len(V0)
vpart = np.empty(nV, object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
deg = np.bincount(E.ravel(), minlength=nV).astype(float)
LM = json.load(open(RD + '/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
c2 = lambda t: (lambda u: u * u * u * (u * (6 * u - 15) + 10))(np.clip(t, 0, 1))
Wd = W0.astype(np.float64); g = np.zeros(nV); LOG = dict(config=CFG, sides={})
for s in CFG['sides']:
    gh = np.array(LM['glenohumeral_' + s]['position_source_frame_cm']); d = np.linalg.norm(V0 - gh, axis=1)
    gs = c2((CFG['R_out'] - d) / (CFG['R_out'] - CFG['R_core'])) * np.isin(vpart, ['arm_' + s, 'axial'])
    if CFG.get('front_only'): gs *= c2(((V0 - gh)[:, 1] - CFG.get('front_f0_cm', -2.0)) / CFG.get('front_ramp_cm', 4.0))
    g = np.maximum(g, gs); LOG['sides'][s] = dict(region_vertices=int((gs > 0).sum()), max_rest_dist_cm=float(d[gs > 0].max()) if (gs > 0).any() else 0.0)
act = np.nonzero(g > 0)[0]
# diffusion of the normalised (effective) weights on the region graph only: region vertices are updated, every vertex outside keeps its W0 row
# (Dirichlet boundary -> continuity at the region edge); sparse one-ring averaging, k_iters iterations (smoothing length ~ sqrt(k/2) edge lengths)
import scipy.sparse as sp
rs0 = Wd.sum(1); Wnorm = Wd / np.maximum(rs0, 1e-12)[:, None]
A = sp.csr_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nV, nV))
Ar = A[act]; dgr = np.asarray(Ar.sum(1)).ravel(); nz = np.nonzero(np.abs(Wnorm[np.unique(Ar.indices)]).sum(0) > 0)[0]
Ws = Wnorm.copy(); Y = Wnorm[:, nz].copy()
for _ in range(CFG['k_iters']):
    Y[act] = 0.5 * Y[act] + 0.5 * (Ar @ Y) / dgr[:, None]
Ws[:, nz] = Y
Ws *= rs0[:, None]                                                     # back to each row's own W0 sum
if CFG.get('bones'):                                                   # optional: diffuse only these columns (rows renormalised to the W0 sum of the set)
    cols = [names.index(b) for b in CFG['bones']]; oth = [i for i in range(len(names)) if i not in cols]
    Ws[:, oth] = Wd[:, oth]; ss0 = Wd[:, cols].sum(1); ss1 = Ws[:, cols].sum(1); Ws[:, cols] *= (ss0 / np.maximum(ss1, 1e-12))[:, None]
Wn = Wd.copy(); Wn[act] = (1 - g[act, None]) * Wd[act] + g[act, None] * Ws[act]
W32 = Wn.astype(np.float32); W32[g == 0] = W0[g == 0]
LOG['region_vertices'] = int(len(act)); LOG['bones_changed'] = [names[i] for i in np.nonzero(np.abs(W32 - W0).max(0) > 1e-6)[0]]
LOG['row_sum_max_change'] = float(np.abs(W32.astype(np.float64).sum(1) - W0.astype(np.float64).sum(1)).max())
LOG['rows_outside_region_bit_identical'] = bool((W32[g == 0].view(np.uint32) == W0[g == 0].view(np.uint32)).all())
LOG['max_weight_change'] = float(np.abs(W32 - W0).max()); LOG['weights_sha256'] = hashlib.sha256(np.ascontiguousarray(W32).tobytes()).hexdigest()
LOG['region_ids_sha256'] = hashlib.sha256(act.astype(np.int32).tobytes()).hexdigest()
np.savez_compressed(O + '/weights_S2.npz', W=W32, names=np.array(names)); np.save(O + '/region_g.npy', g.astype(np.float32))
json.dump(LOG, open(O + '/weights_S2_log.json', 'w'), indent=1); print(json.dumps({k: v for k, v in LOG.items() if k != 'config'}, indent=1))
