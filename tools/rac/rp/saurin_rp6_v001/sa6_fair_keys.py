# sa6_fair_keys.py CFG WEIGHTS.npz IN.json OUT.json [IT] : rest-space fairing of every fitted corrective key (rig v002, order 07a3f24c §1).
#   Each family key and pose key field (rest-space displacement on its vertex set) is low-pass filtered over its support dilated 2 rings (uniform Laplacian,
#   IT iterations, default 20; protected / rigid-landmark vertices held at 0; elbow-muscle layer families untouched -- they are procedural and smooth).
#   The result is the starting point of a refit pass whose solver (sa6_fit.fair after every clean solve) keeps the fields fair; the refit removes any fold /
#   tear / volume defect the filtering re-opens.  Same JSON schema as the fit output (families, pose keys, names); method and source recorded.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_pose as SP, sa6_correctives as CC
cfg, wf, IN, OUT = sys.argv[1:5]; IT = int(sys.argv[5]) if len(sys.argv) > 5 else 20
R = SP.Rig(cfg, wf); S = CC.Solver(R); deg = np.asarray(S.A1.sum(1)).ravel(); js = json.load(open(IN)); z = np.load(IN.replace('.json', '.npz')); out = {}; n = 0
def fair(idx, d):
    D = np.zeros((R.nv, 3)); D[idx] = d; sup = np.zeros(R.nv, bool); sup[idx] = np.linalg.norm(d, axis=1) > 1e-9
    m = S.dilate(sup, 2) & ~S.protect; ii = np.nonzero(m)[0]
    for _ in range(IT): D[ii] = 0.5 * D[ii] + 0.5 * ((S.A1 @ D) / deg[:, None])[ii]
    D[S.protect] = 0; k = np.nonzero(np.linalg.norm(D, axis=1) > 1e-7)[0]; return k.astype(np.int32), D[k].astype(np.float32)
for f in js['families']:
    for k in f['keys']:
        a, b = z[k['name'] + '_idx'], z[k['name'] + '_d']
        if f.get('layer'): out[k['name'] + '_idx'], out[k['name'] + '_d'] = a, b
        else: out[k['name'] + '_idx'], out[k['name'] + '_d'] = fair(a.astype(np.int64), b.astype(np.float64)); n += 1
for p in js.get('pose_keys', []):
    out[p['name'] + '_idx'], out[p['name'] + '_d'] = fair(z[p['name'] + '_idx'].astype(np.int64), z[p['name'] + '_d'].astype(np.float64)); n += 1
for k in z.files:
    if k not in out: out[k] = z[k]
js['status'] = js.get('status', 'RP6 RIG PILOT / NOT FROZEN'); js['faired'] = dict(tool='sa6_fair_keys.py', iterations=IT, keys=n, source=os.path.basename(IN))
np.savez_compressed(OUT.replace('.json', '.npz'), **out); json.dump(js, open(OUT, 'w'), indent=1); print(cfg, 'faired keys', n)
