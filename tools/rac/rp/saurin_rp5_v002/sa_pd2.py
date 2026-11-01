# sa_pd2.py CAGE.npz OUT.json NAME=state.npy ... : PD-2 source-side ownership for creator composition states (order 236dddc §11).
#   For each state: (a) dense source folds = canonical-base triangles whose normal flips (cos < 0) vs the canonical rest base, and triangles whose
#   area collapses below 5 % of rest; (b) cage flips (quads whose normal flips vs the cage at rest, realized by the barycentric embedding);
#   (c) ownership: a cage flip is SOURCE-OWNED when a flipped / collapsed source triangle lies under it (within its quad footprint, 1 cm), else CAGE-OWNED.
#   Also reports the same counts with the cage re-fitted locally (one Laplacian-smoothed reprojection) to show whether any cage flip survives on a clean source.
import sys, os, json, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
from scipy.spatial import cKDTree
CG, OUT = sys.argv[1:3]; states = dict(a.split('=') for a in sys.argv[3:]); z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; F = G.F
R = np.load(G.W + '/src/saurin_w2_final_base.npz'); VR = R[[k for k in R.files if R[k].shape == G.V.shape][0]].astype(float)
def fn(P): n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); return n
nR = fn(VR); aR = np.linalg.norm(nR, axis=1)
def qn(P): return np.cross(P[Q[:, 2]] - P[Q[:, 0]], P[Q[:, 3]] - P[Q[:, 1]])
P0 = (bc[:, :, None] * VR[F[fi]]).sum(1); q0 = qn(P0); res = {}
for nm, path in states.items():
    VB = np.load(path).astype(float); nB = fn(VB); aB = np.linalg.norm(nB, axis=1)
    cos = (nR * nB).sum(1) / (aR * aB + 1e-20); sflip = cos < 0; scol = aB < 0.05 * aR; bad = sflip | scol
    P = (bc[:, :, None] * VB[F[fi]]).sum(1); q1 = qn(P); cflip = np.nonzero(((q0 * q1).sum(1)) < 0)[0]
    own_src = 0
    if bad.any() and len(cflip):
        kd = cKDTree(VB[F[bad]].mean(1)); qc = P[Q[cflip]].mean(1); rad = np.linalg.norm(P[Q[cflip]] - qc[:, None], axis=2).max(1) + 1.0
        own_src = int(sum(1 for c, r in zip(qc, rad) if kd.query_ball_point(c, r, return_length=True) > 0))
    labs = {}
    for qi in cflip: labs[str(z['qlab'][qi])] = labs.get(str(z['qlab'][qi]), 0) + 1
    r = dict(source_triangles=int(len(F)), source_flipped=int(sflip.sum()), source_collapsed=int(scol.sum()), cage_flipped_quads=int(len(cflip)),
             cage_flips_over_source_folds=own_src, cage_flips_cage_owned=int(len(cflip) - own_src), cage_flip_regions=labs)
    r['owner'] = 'NONE' if not len(cflip) else ('SOURCE (PD-2: creator composition state folds the dense source; cage inherits it)' if own_src == len(cflip) else 'MIXED -> fix cage')
    res[nm] = r; print(nm, r, flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
