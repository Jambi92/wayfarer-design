# RM-OT-05U3: stop-condition guards (b) and (e) for the opt-in U2 path (read-only measurement of a return).
#  (b) roughness: max angle between each vertex's incident face normals and their mean (deg); limit = source p95 36.3 deg
#      (05U2 baseline, 1,438 source vertices); evaluated on the 365 proposed editable vertices.
#  (e) sliver guard: for each of the 35 added faces, min angle must be >= its baseline (05U RETURN) min angle - 0.01 deg and
#      >= 5 deg (the existing FAIL rule); baseline min angles are recomputed from the frozen 05U baseline.
# Usage: python3 u3_guards.py --s3 GO-05S-S3.obj --ret RETURN.npz --baseline 05U_return.npz --proposal DIR --out JSON
import argparse, json, os, numpy as np, trimesh
from collections import defaultdict
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--ret', '--baseline', '--proposal', '--out')]; a = ap.parse_args()
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
def geo(p):
    R = np.load(p); i = R['s3_vid1'] - 1; V = Vs.copy(); mv = ~np.all(R['V'] == Vs[i].astype(np.float32), 1); V[i[mv]] = R['V'][mv]; return V
PS = np.load(os.path.join(a.proposal, 'proposal_sets.npz')); E = PS['proposed_editable']; A = PS['added_faces']; P95 = json.load(open(os.path.join(a.proposal, 'proposal_region.json')))['source_skin_baseline_roughness']['p95']
vf = defaultdict(list)
for k, f in enumerate(F):
    for v in f: vf[int(v)].append(k)
def rough(V, vs):
    fn = trimesh.Trimesh(V, F, process=False).face_normals; out = {}
    for v in vs:
        n = fn[vf[int(v)]]; c = n.mean(0); c /= np.linalg.norm(c); out[int(v)] = float(np.degrees(np.arccos(np.clip(n @ c, -1, 1))).max())
    return out
def minang(V, fs):
    T = V[F[fs]]; L = np.linalg.norm(T[:, [1, 2, 0]] - T[:, [2, 0, 1]], axis=2)
    cs = np.stack([(L[:, (i + 1) % 3]**2 + L[:, (i + 2) % 3]**2 - L[:, i]**2) / (2 * L[:, (i + 1) % 3] * L[:, (i + 2) % 3]) for i in range(3)], 1)
    return np.degrees(np.arccos(np.clip(cs, -1, 1))).min(1)
Vb = geo(a.baseline); Vr = geo(a.ret)
rb = rough(Vb, E); rr = rough(Vr, E); mb = minang(Vb, A); mr = minang(Vr, A)
over = sorted(((round(x, 1), v) for v, x in rr.items() if x > P95), reverse=True)
worse = [dict(s3_face=int(A[k]), baseline=round(float(mb[k]), 2), now=round(float(mr[k]), 2)) for k in range(len(A)) if mr[k] < mb[k] - 0.01 or mr[k] < 5]
res = dict(b_roughness=dict(limit_deg=P95, vertices=len(E), max_now=round(max(rr.values()), 1), max_baseline=round(max(rb.values()), 1), over_limit_now=len(over), over_limit_examples=[dict(s3_vertex=v, roughness=g) for g, v in over[:10]], pass_=len(over) == 0),
           e_sliver_guard=dict(faces=len(A), min_angle_baseline=round(float(mb.min()), 2), min_angle_now=round(float(mr.min()), 2), worse_or_below_5=worse, pass_=len(worse) == 0))
json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps({k: {x: y for x, y in v.items() if x != 'over_limit_examples'} for k, v in res.items()}))
