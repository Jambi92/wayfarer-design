# corr_field_check.py WORKDIR CORR_TAG SIDE : corrective field record (order 6c38d75 §4 / §6): support / core / taper-band vertex ids, per-key max
# rest-space delta, per-edge delta gradient |D_a - D_b| / rest length (core / band / boundary edges), exact zero outside the support, parts crossed,
# delta hashes. Writes diag/corr_field_TAG.json and corr/support_ids_TAG.npz.
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import bl_to_src
from common import PARTS
W, TG, S = sys.argv[1:4]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
C = np.load('%s/corr/corr_%s.npz' % (W, TG)); cfg = json.load(open('%s/corr/corr_%s_log.json' % (W, TG)))['config']
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}; e = bl_to_src(np.array(B['forearm_' + S]['head'])[None])[0]
d = np.linalg.norm(V0 - e, axis=1); sup = C['support']; core = sup & (d <= cfg['R_core']); band = sup & ~core
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0); L0 = np.linalg.norm(V0[E[:, 0]] - V0[E[:, 1]], axis=1)
vpart = np.empty(len(V0), object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
cross = sup[E[:, 0]] ^ sup[E[:, 1]]; incore = core[E[:, 0]] & core[E[:, 1]]; inband = (band[E[:, 0]] | band[E[:, 1]]) & ~cross
out = dict(tag=TG, side=S, config=cfg, support_vertices=int(sup.sum()), core_vertices=int(core.sum()), band_vertices=int(band.sum()),
           support_parts=sorted(set(vpart[sup])), touches_part_boundary=bool(any(vpart[w] != 'arm_' + S for v in np.nonzero(sup)[0][:0] for w in [v])),
           support_ids_sha256=hashlib.sha256(np.ascontiguousarray(np.nonzero(sup)[0].astype(np.int32)).tobytes()).hexdigest(), keys={})
# does the support reach the arm part boundary (an arm vertex in the support sharing an edge with a non-arm vertex)?
pb = [(a, b) for a, b in E if (sup[a] and vpart[b] != 'arm_' + S) or (sup[b] and vpart[a] != 'arm_' + S)]
out['support_edges_on_part_boundary'] = len(pb); out['touches_part_boundary'] = bool(pb)
for k in C.files:
    if not (k.startswith('K') and k.endswith('_' + S)): continue
    D = C[k]; mag = np.linalg.norm(D, axis=1); g = np.linalg.norm(D[E[:, 0]] - D[E[:, 1]], axis=1) / np.maximum(L0, 1e-9)
    out['keys'][k] = dict(max_rest_delta_cm=float(mag.max()), mean_rest_delta_in_core_cm=float(mag[core].mean()), max_delta_outside_support_cm=float(mag[~sup].max()),
                          max_delta_in_outer_band_1cm=float(mag[sup & (d > cfg['R_out'] - 1.0)].max()) if (sup & (d > cfg['R_out'] - 1.0)).any() else 0.0,
                          gradient_max=dict(core=float(g[incore].max()), band=float(g[inband].max()), boundary_edges=float(g[cross].max()) if cross.any() else 0.0),
                          gradient_p95=dict(core=float(np.percentile(g[incore], 95)), band=float(np.percentile(g[inband], 95))),
                          nonzero_vertices=int((mag > 1e-9).sum()), delta_sha256=hashlib.sha256(np.ascontiguousarray(D.astype(np.float32)).tobytes()).hexdigest())
np.savez_compressed('%s/corr/support_ids_%s.npz' % (W, TG), support=np.nonzero(sup)[0].astype(np.int32), core=np.nonzero(core)[0].astype(np.int32), band=np.nonzero(band)[0].astype(np.int32))
json.dump(out, open('%s/diag/corr_field_%s.json' % (W, TG), 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'config'}, indent=1))
