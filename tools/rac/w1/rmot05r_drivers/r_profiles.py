# RM-OT-05R half-plane sections through the 05Q arm axis at given theta, overlaying several meshes (identical frame).
# Usage: python3 r_profiles.py --out OUT.png --frame patch_selection.json --meshes "label=mesh.obj:colour" ... --thetas -110 -104 ...
import argparse, json, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('--out'); ap.add_argument('--frame'); ap.add_argument('--meshes', nargs='+'); ap.add_argument('--thetas', nargs='+', type=float)
ap.add_argument("--title", default=""); ap.add_argument("--xlim", type=float, nargs=2, default=[4, 14]); ap.add_argument("--ylim", type=float, nargs=2, default=[-6, 10]); a = ap.parse_args()
J = json.load(open(a.frame)); O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
def segs(V, F, th):
    nrm = -np.sin(np.radians(th)) * e1 + np.cos(np.radians(th)) * e2; dv = np.cos(np.radians(th)) * e1 + np.sin(np.radians(th)) * e2
    sd = (V - O) @ nrm; T = F[(np.abs(V[F] - O).max((1, 2)) < 22)]; sv = sd[T]; cr = (sv.min(1) < 0) & (sv.max(1) > 0); out = []
    for f in T[cr]:
        p = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (sd[f[i]] < 0) != (sd[f[j]] < 0): t = sd[f[i]] / (sd[f[i]] - sd[f[j]]); p.append(V[f[i]] + t * (V[f[j]] - V[f[i]]))
        c = np.array(p) - O; out.append(np.c_[c @ dv, c @ d])
    return [o for o in out if (o[:, 0] > 0).all() and (o[:, 0] < 22).all() and (np.abs(o[:, 1]) < 16).all()]
ms = []
for spec in a.meshes:
    lab_, rest = spec.split('=', 1); path, col = rest.rsplit(':', 1); m = trimesh.load(path, process=False); ms.append((lab_, np.asarray(m.vertices), np.asarray(m.faces), col))
n = len(a.thetas); cols = min(n, 6); rows = (n + cols - 1) // cols
fig, ax = plt.subplots(rows, cols, figsize=(3.3 * cols, 4.6 * rows), squeeze=False)
for k, th in enumerate(a.thetas):
    A = ax[k // cols][k % cols]
    for j, (lab_, V, F, col) in enumerate(ms):
        for i, sg in enumerate(segs(V, F, th)): A.plot(sg[:, 0], sg[:, 1], color=col, lw=max(1.0, 2.8 - 0.6 * j), label=lab_ if i == 0 else None)
    A.set_title('theta %g' % th, fontsize=9); A.set_aspect('equal'); A.grid(alpha=.3); A.set_xlim(a.xlim[0], a.xlim[1]); A.set_ylim(a.ylim[0], a.ylim[1]); A.legend(fontsize=6, loc='lower right'); A.set_xlabel('r cm'); A.set_ylabel('s cm')
for k in range(n, rows * cols): ax[k // cols][k % cols].axis('off')
fig.suptitle(a.title, fontsize=10); plt.tight_layout(); plt.savefig(a.out, dpi=75)
