# lr.py OBJ [--json out] : source-relative left/right displacement audit. Correspondence: each template vertex with x>0.5 is paired with the
# nearest template vertex to its mirror image (-x, y, z) (pairs with mirror distance > 1.5 cm are dropped). Displacements D = S - T are compared
# as D_left vs mirror(D_right) = (-dx, dy, dz). Reports per family: n pairs, mean |D| left / right, p90 and max of |D_left - mirror(D_right)|.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05f_drivers')
from f_common import *
from scipy.spatial import cKDTree
PK = REPO + '/reviews/rac-rmot05f-handoff'
G = {k: np.array(v) for k, v in json.load(open(PK + '/data/regions.json'))['regions'].items()}
T = route_state(SKELETON_BODY)[0][:NBODY]; S = read_obj(sys.argv[1])[0]; D = S - T
Lx = np.where(T[:, 0] > 0.5)[0]; M = T[Lx] * [-1, 1, 1]; d, j = cKDTree(T).query(M); ok = d < 1.5; Li, Ri = Lx[ok], j[ok]
pair_err = d[ok]
out = {'template_pair_mirror_error_cm': {'p50': round(float(np.percentile(pair_err, 50)), 3), 'p90': round(float(np.percentile(pair_err, 90)), 3), 'max': round(float(pair_err.max()), 3)}}
for k, ix in G.items():
    if k.startswith('NO_TOUCH'): continue
    s = set(ix.tolist()); m = np.array([a in s or b in s for a, b in zip(Li, Ri)])
    if not m.any(): continue
    dl = D[Li[m]]; dr = D[Ri[m]] * [-1, 1, 1]; diff = np.linalg.norm(dl - dr, axis=1)
    out[k] = {'pairs': int(m.sum()), 'mean_disp_left': round(float(np.linalg.norm(dl, axis=1).mean()), 2), 'mean_disp_right': round(float(np.linalg.norm(dr, axis=1).mean()), 2),
              'asym_p50': round(float(np.percentile(diff, 50)), 2), 'asym_p90': round(float(np.percentile(diff, 90)), 2), 'asym_max': round(float(diff.max()), 2),
              'worst_left_vertex': int(Li[m][diff.argmax()]), 'worst_at': np.round(T[Li[m][diff.argmax()]], 1).tolist()}
print(json.dumps(out, indent=1))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
