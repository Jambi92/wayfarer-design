# Crotch-height relation, same surface method for every body: lowest midline (|X| < 1 cm) surface point between 30 % and 60 %
# of the measured height. Usage: python3 o_crotch.py --crown CROWN_Z MESH_OR_R6NPZ ...   (crown: cranial vault top for the
# Gorrund GO-RD meshes whose max z includes ears / mane tufts; otherwise max z is used)
import sys, argparse, numpy as np, trimesh, json
ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--crown', type=float, nargs='*', default=None); a = ap.parse_args()
out = []
for i, f in enumerate(a.files):
    if f.endswith('.npz'):
        d = np.load(f); V = d['V'][d['keep'].astype(bool)]
    else: V = trimesh.load(f, process=False).vertices
    z0 = V[:, 2].min(); st = (a.crown[i] if a.crown and a.crown[i] > 0 else V[:, 2].max()) - z0
    b = V[np.abs(V[:, 0]) < 1.0]; b = b[(b[:, 2] - z0 > 0.3 * st) & (b[:, 2] - z0 < 0.6 * st)]
    c = b[:, 2].min() - z0; out.append(dict(file=f, stature=round(float(st), 2), crotch=round(float(c), 2), ratio=round(float(c / st), 4))); print(out[-1])
