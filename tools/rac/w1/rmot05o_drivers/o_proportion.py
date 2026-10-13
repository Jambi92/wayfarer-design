# RAC RM-OT-05O §5: one documented femur / shank SHAFT lengthening on the stance variant (see proportion/PROPOSAL_RD3c.md).
# Legs are vertical after o_stance.py, so the shafts are stretched along Z inside two bands; joints keep their shape.
# Leg vertices = pelvis-and-legs mesh component below the crotch band (forearms / hands are separate components);
# every non-leg vertex and every leg vertex above the thigh band translates up by the full delta.
# Usage: python3 o_proportion.py --in IN.obj --stance STANCE_record.json --d_femur 4.8 --d_shank 4.4 --crotch_z 99.97 --out OUT.obj
import argparse, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--stance'); ap.add_argument('--out')
ap.add_argument('--d_femur', type=float); ap.add_argument('--d_shank', type=float); ap.add_argument('--crotch_z', type=float); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float).copy(); F = np.asarray(m.faces); R = json.load(open(a.stance))
knee = np.array(R['landmarks_after']['knee']); ankle = np.array(R['landmarks_after']['ankle']); hip = np.array(R['landmarks_after']['hip'])
s0, s1 = ankle[2] + 9, knee[2] - 9; t0, t1 = knee[2] + 9, a.crotch_z - 8
sub = V[:, 2] < t1 + 1; fm = sub[F].all(1); E = np.vstack([F[fm][:, [0, 1]], F[fm][:, [1, 2]], F[fm][:, [2, 0]]])
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(len(V), len(V))); nc, lab = connected_components(A, directed=False)
legs = (lab == np.bincount(lab[V[:, 2] < 3]).argmax()) & sub
def f(z):
    fs = a.d_shank * np.clip((z - s0) / (s1 - s0), 0, 1); ft = a.d_femur * np.clip((z - t0) / (t1 - t0), 0, 1); return fs + ft
dz = np.where(legs, f(V[:, 2]), a.d_femur + a.d_shank); V[:, 2] += dz
trimesh.Trimesh(V, F, process=False).export(a.out)
kn = knee + [0, 0, a.d_shank]; hp = hip + [0, 0, a.d_shank + a.d_femur]
rec = dict(input=a.inp, output=a.out, bands=dict(shank=[round(s0, 2), round(s1, 2)], thigh=[round(t0, 2), round(t1, 2)]), d_femur=a.d_femur, d_shank=a.d_shank,
           landmarks_after=dict(hip=hp.round(2).tolist(), knee=kn.round(2).tolist(), ankle=ankle.round(2).tolist()),
           thigh_length=[round(float(np.linalg.norm(knee - hip)), 2), round(float(np.linalg.norm(kn - hp)), 2)],
           shank_length=[round(float(np.linalg.norm(ankle - knee)), 2), round(float(np.linalg.norm(ankle - kn)), 2)],
           stature_maxz=round(float(V[:, 2].max()), 2), leg_vertices=int(legs.sum()))
json.dump(rec, open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
