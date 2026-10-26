# elbow_penetration.py WORKDIR : demonstrated penetration vs expected proximity at the left elbow (order b303b9e §5), D2_l_flex90 / 130,
# W0 / E1 / E2, LBS and DQS. For every intersecting face pair (BVH overlap, ids file) the penetration depth = how far the vertices of each face
# lie behind the other face's plane, limited to vertices whose projection falls within that face (max over both directions). Proximity =
# arm_l vertices within 2 mm of a non-adjacent arm_l face on the opposite side of the crease (forearm vs upper-arm dominant) WITHOUT intersection.
import sys, json, numpy as np
from scipy.spatial import cKDTree
W = sys.argv[1]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
sys.path.insert(0, '/tmp/claude-0/rt'); from common import PARTS
z0 = np.load('/tmp/claude-0/rt/rd/rig/weights_v001c.npz'); nm = [str(n) for n in z0['names']]; WF = z0['W'][:, nm.index('forearm_l')]
arm = FP == PARTS.index('arm_l'); fore = WF[Q].mean(1) > 0.5
def depth(V, a, b):
    best = 0.0
    for x, y in ((a, b), (b, a)):
        qy = V[Q[y]]; c = qy.mean(0); n = np.cross(qy[2] - qy[0], qy[3] - qy[1]); n /= np.linalg.norm(n)
        r = np.linalg.norm(qy - c, axis=1).max()
        for p in V[Q[x]]:
            s = (p - c) @ n
            if s < 0 and np.linalg.norm((p - c) - s * n) <= r: best = max(best, -s)
    return best
out = {}
for pose in ('D2_l_flex90', 'D2_l_flex130'):
    for m in ('lbs', 'dqs'):
        for cd in ('W0', 'E1', 'E2'):
            V = np.load('%s/diag/posed/%s_el_%s_%s.npz' % (W, pose, m, cd))['V'].astype(float); ids = np.load('%s/diag/ids/%s_el_%s_%s.npz' % (W, pose, m, cd))
            pr = ids['pairs']; pc = ids['pair_class']; R = {}
            for code, lab in ((0, 'non_contact'), (1, 'crease')):
                s = pr[pc == code]; d = np.array([depth(V, a, b) for a, b in s]) * 10 if len(s) else np.zeros(0)
                R[lab] = dict(pairs=int(len(s)), max_depth_mm=round(float(d.max()), 2) if len(d) else 0.0, p95_depth_mm=round(float(np.percentile(d, 95)), 2) if len(d) else 0.0)
            # proximity without intersection: forearm-side arm faces' vertices within 2 mm of upper-arm-side arm face centres
            inter = set(pr.ravel().tolist()) if len(pr) else set()
            fa = np.nonzero(arm & fore)[0]; ua = np.nonzero(arm & ~fore)[0]; C = V[Q].mean(1)
            t = cKDTree(C[ua]); dd, j = t.query(C[fa], distance_upper_bound=0.2)
            ok = np.isfinite(dd); near = [int(x) for x in fa[ok] if x not in inter]
            R['proximity_2mm_faces_without_intersection'] = len(near)
            out['%s %s %s' % (pose, m, cd)] = R
            print(pose, m, cd, R)
json.dump(out, open(W + '/diag/elbow_penetration.json', 'w'), indent=1)
