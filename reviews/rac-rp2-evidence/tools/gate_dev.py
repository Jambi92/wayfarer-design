# gate_dev.py PROD.npz REF.npz OUT.json : T-1 / T-2 surface deviation, both directions, production vs reference envelope
# reference = S* (adjudicated) or E3 (raw). Reference sample set = vertices + triangle centroids of VISIBLE reference triangles
# (hidden = inside the reference volume, i.e. the source's own interpenetration lens; excluded and counted).
import sys, json, numpy as np, igl
sys.path.insert(0, '/tmp/claude-0/rp2/tools'); sys.path.insert(0, '/tmp/claude-0/rp2')
from hidden import hidden_quads; from zones import base_zones
pz_ = np.load(sys.argv[1]); P = pz_['V']; Q = pz_['Q']; TP = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
r = np.load(sys.argv[2]); S = r['V']; QS = r['Q']; TS = np.r_[QS[:, [0, 1, 2]], QS[:, [0, 2, 3]]]
W = dict(np.load('/tmp/claude-0/rp2/weights_body.npz')); J = json.loads(str(np.load('/tmp/claude-0/rp2/GR5DE3_r6.npz')['joints']))
hq, sgn, ht = hidden_quads(S, QS)
EX = np.load(sys.argv[4]) if len(sys.argv) > 4 else np.zeros(len(QS), bool)   # resolution-zone reference quads (replaced by patches)
ht = ht | np.r_[EX, EX]
zS = base_zones(S, W, J)
# production zones carried in the candidate file
zP = {k[5:]: pz_[k] for k in pz_.files if k.startswith('zone_')}
# prod -> ref (vertices and face centroids of production)
PP = np.vstack([P, P[Q].mean(1)]); zPP = {k: np.r_[v, v[Q].all(1)] for k, v in zP.items()}
_d, _fi, _ = igl.point_mesh_squared_distance(PP, S, TS); d1 = np.sqrt(_d) * 10
EXT = np.r_[EX, EX]; inzone = EXT[_fi]                                  # nearest reference surface is a replaced (resolution-zone) quad
dz1 = d1[inzone]; d1 = d1[~inzone]; zPP = {k: v[~inzone] for k, v in zPP.items()}
# ref -> prod: visible vertices and visible triangle centroids
visv = np.ones(len(S), bool); visv[np.unique(TS[ht])] = False
SP = np.vstack([S[visv], S[TS[~ht]].mean(1)]); zSP = {k: np.r_[v[visv], v[TS[~ht]].all(1)] for k, v in zS.items()}
d2 = np.sqrt(igl.point_mesh_squared_distance(SP, P, TP)[0]) * 10
def st(d): return dict(median=float(np.median(d)), p95=float(np.percentile(d, 95)), max=float(d.max()), n=int(len(d)))
out = dict(reference=sys.argv[2], hidden_reference_triangles=int(ht.sum()), body=dict(prod_to_ref=st(d1), ref_to_prod=st(d2)))
zone_report = dict(prod_points_in_resolution_zones=int(inzone.sum()), prod_to_ref=st(dz1) if len(dz1) else None)
for k in zS:
    if k == 'T2': continue
    out[k] = dict(prod_to_ref=st(d1[zPP[k]]), ref_to_prod=st(d2[zSP[k]]))
T1 = out['body']; ok1 = all(T1[d]['median'] <= 0.5 and T1[d]['p95'] <= 1.5 and T1[d]['max'] <= 3.0 for d in T1)
ok2 = all(out[k][d]['median'] <= 0.3 and out[k][d]['p95'] <= 0.8 and out[k][d]['max'] <= 1.5 for k in out if k not in ('reference', 'hidden_reference_triangles', 'body') for d in out[k])
out['T1_pass'] = bool(ok1); out['T2_pass'] = bool(ok2); out['resolution_zone_report'] = zone_report
json.dump(out, open(sys.argv[3], 'w'), indent=1)
for k, v in out.items():
    if isinstance(v, dict) and 'prod_to_ref' in v and isinstance(v.get('ref_to_prod'), dict): print('%-16s' % k, ' | '.join('%s med %.3f p95 %.3f max %.3f' % (d, v[d]['median'], v[d]['p95'], v[d]['max']) for d in v))
print('T1', ok1, 'T2', ok2)
print('resolution zones:', zone_report)
