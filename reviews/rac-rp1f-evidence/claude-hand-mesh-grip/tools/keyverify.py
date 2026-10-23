# keyverify.py (bpy python) -- RIG SIDE TASK.json OUT.json RESULT.json
# Turn the per-frame soft-tissue correctives of one solved test into a small set of corrective KEY shapes (rest space)
# whose linear blend between keys reproduces a valid mesh at EVERY solved frame. Each frame is re-checked with the
# interpolated corrective: new self-intersections vs rest (skin <= resid, claw <= claw tol) and fixture penetration.
# Frames that fail become keys; repeat until all frames pass. Writes keys (sparse rest-space offsets) + report.
import sys, json, numpy as np
src = open('/tmp/claude-0/hand/tools/gripsolve2.py').read(); src = src[:src.index("PH = T['phases']")]
a = sys.argv[sys.argv.index('--') + 1:]; rig, side, task, outj, resj = a[:5]
sys.argv = ['x', '--', rig, side, task, '/tmp/_kv.json']
exec(src)
D = json.load(open(outj)); FR = D['frames']; Z = np.load(outj.replace('.json', '_corr.npz'))
nF = len(FR); nV = len(H.P0)

def dq_rot(angles):
    S = H.skin_mats(angles)
    from fastpose import rot2quat
    q0 = np.array([rot2quat(S[b][:3, :3]) for b in range(H.nb)]); ref = q0[0]; sg = np.sign(q0 @ ref); sg[sg == 0] = 1; q0 = q0 * sg[:, None]
    B0 = H.W @ q0; B0 /= np.linalg.norm(B0, axis=1, keepdims=True)
    w, x, y, z = B0.T
    R = np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1),
                  np.stack([2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1),
                  np.stack([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1)], 1)
    return R
# rest-space offsets per frame (dense float32 only where needed)
OFF = []
for i in range(nF):
    idx = Z['i%d' % i]; d = Z['d%d' % i].astype(float)
    if len(idx) == 0: OFF.append((idx, d)); continue
    R = dq_rot(FR[i]['angles'])[idx]; OFF.append((idx, np.einsum('nji,nj->ni', R, d)))
def dense(k):
    o = np.zeros((nV, 3)); idx, d = OFF[k]; o[idx] = d; return o
def interp(i, keys):
    ks = sorted(keys); j = np.searchsorted(ks, i)
    if ks[min(j, len(ks) - 1)] == i: return dense(i)
    k0 = ks[j - 1]; k1 = ks[j]; t = (i - k0) / (k1 - k0); return (1 - t) * dense(k0) + t * dense(k1)
def frame_ok(i, O):
    ang = FR[i]['angles']; P = H.pose(ang)
    if np.abs(O).max() > 0: P = P + np.einsum('nij,nj->ni', dq_rot(ang), O)
    pr = selfx(P); new = np.array(sorted(set(map(tuple, pr.tolist())) - rest), int).reshape(-1, 2)
    dep = depths(P, new); isc = (kerq[new[:, 0]] | kerq[new[:, 1]]) if len(new) else np.zeros(0, bool)
    tol = SKIN_TOL   # verification: skin-skin residual contact <= 1.0 mm (stated soft-tissue tolerance), claws <= 0.5 mm
    bad = int((np.where(isc, dep > CLAW_TOL, dep > tol)).sum()) if len(new) else 0
    res = dict(skin_mm=float(dep[~isc].max() * 1000) if (~isc).any() else 0.0, claw_mm=float(dep[isc].max() * 1000) if isc.any() else 0.0, bad=bad)
    if T.get('fixture'):
        sd = fixture_sd(P, T['fixture']); res['fixture_pen_mm'] = float(max(0.0, -sd.min()) * 1000);
        if (sd < -FIX_TOL).any(): res['bad'] += 1
    return res['bad'] == 0, res, P
from scipy.optimize import nnls
nz = [i for i in range(nF) if len(OFF[i][0])]
keys = set([max(nz, key=lambda i: np.abs(OFF[i][1]).max())]) if nz else set()
W = {}
def fit(i, ks):
    if not ks or not len(OFF[i][0]): return {}
    sup = np.unique(np.concatenate([OFF[k][0] for k in ks] + [OFF[i][0]]))
    pos = {v: j for j, v in enumerate(sup)}
    def col(k):
        c = np.zeros((len(sup), 3)); idx, d = OFF[k]; c[[pos[v] for v in idx]] = d; return c.ravel()
    A = np.stack([col(k) for k in ks], 1); bvec = col(i)
    w, _ = nnls(A, bvec); return {k: float(x) for k, x in zip(ks, w)}
def blend(wd):
    o = np.zeros((nV, 3))
    for k, x in wd.items():
        idx, d = OFF[k]; o[idx] += x * d
    return o
rep = {}
for rnd in range(40):
    ks = sorted(keys); fails = []
    for i in range(nF):
        if i in keys: W[i] = {i: 1.0}; continue
        W[i] = fit(i, ks); ok, r, _ = frame_ok(i, blend(W[i])); rep[i] = r
        if not ok: fails.append(i)
    print('round', rnd, 'basis', len(ks), 'failing frames', len(fails), flush=True)
    if not fails: break
    nadd = max(1, min(6, len(fails) // 8))
    chunks = np.array_split(np.array(fails), nadd)
    for ch in chunks:
        keys.add(int(max(ch, key=lambda i: rep[i]['skin_mm'] + rep[i]['claw_mm'] + rep[i].get('fixture_pen_mm', 0))))
for k in sorted(keys):
    ok, r, _ = frame_ok(k, dense(k)); rep[k] = r; W[k] = {k: 1.0}
allok = all(r['bad'] == 0 for r in rep.values())
ks = sorted(keys)
np.savez_compressed(resj.replace('.json', '_keys.npz'), keys=np.array(ks), **{'i%d' % k: OFF[k][0] for k in ks}, **{'o%d' % k: OFF[k][1].astype(np.float32) for k in ks})
json.dump(dict(frames=nF, keys=ks, weights={str(i): {str(k): v for k, v in W[i].items()} for i in range(nF)}, all_frames_pass=bool(allok), worst=dict(skin_mm=max(r['skin_mm'] for r in rep.values()), claw_mm=max(r['claw_mm'] for r in rep.values()),
          fixture_pen_mm=max(r.get('fixture_pen_mm', 0) for r in rep.values())), per_frame={str(k): v for k, v in rep.items()}), open(resj, 'w'), indent=1)
print('ALL FRAMES PASS' if allok else 'FAIL', len(ks), 'keys')
