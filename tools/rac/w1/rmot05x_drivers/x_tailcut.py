# RM-OT-05X R1: DISPOSABLE diagnostic body-only copy for a figure whose tail hangs close to the buttocks (y-plane rules cannot
# separate it). Tail root is found by tracking the free tail's horizontal section loop upward from a seed height until it merges with
# the trunk; faces within R_ROOT of that root and faces above the neck minimum are deleted, and only the largest connected piece is
# kept. Faces are deleted only (no vertex moves); excluded from all topology claims about the intact source.
# Usage: python3 x_tailcut.py FIG.npz OUT.npz SEED_FRAC [R_ROOT_CM=4] [NECK_Z_CM]
import sys, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
fi, fo, seed = sys.argv[1], sys.argv[2], float(sys.argv[3]); RR = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
d = np.load(fi); P = d['V'].astype(np.float64); F = d['F']; V = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) * 100; H = V[:, 2].max()
m = trimesh.Trimesh(V, F, process=False)
def loops(z):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    return [] if s is None else [(np.linalg.norm(np.diff(e, axis=0), axis=1).sum(), e.mean(0)[:2]) for e in s.discrete]
# neck minimum
if len(sys.argv) > 5: NECK = float(sys.argv[5])
else:
    zs = np.arange(0.80 * H, 0.89 * H, 0.5); NECK = float(zs[np.argmin([max(l for l, _ in loops(z)) for z in zs])])
# seed: the most posterior small loop at seed height (the hanging tail)
L0 = [(l, c) for l, c in loops(seed * H) if l < 30]; l0, c = max(L0, key=lambda t: t[1][1]); z = seed * H; track = [(round(z, 1), np.round(c, 1).tolist())]
while z < 0.8 * H:
    z += 0.5; L = [(l, cc) for l, cc in loops(z) if l < 30 and np.linalg.norm(cc - c) < 3.0]
    if not L: break
    l, c = min(L, key=lambda t: np.linalg.norm(t[1] - c)); track.append((round(z, 1), np.round(c, 1).tolist()))
root = np.array([c[0], c[1], z]); cen = V[F].mean(1)
drop_root = np.linalg.norm(cen - root, axis=1) < RR; drop_head = cen[:, 2] > NECK; keep = ~(drop_root | drop_head)
Fk = F[keep]; n = len(V); E = np.concatenate([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]])
nc, lab = connected_components(sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)), directed=False)
fl = lab[Fk[:, 0]]; sizes = np.bincount(fl); big = np.argmax(sizes); pieces = sorted([int(s) for s in sizes if s], reverse=True)
Fk = Fk[fl == big]; u = np.unique(Fk); mp = -np.ones(n, np.int64); mp[u] = np.arange(len(u))
np.savez(fo, V=P[u].astype(np.float32), F=mp[Fk].astype(np.int32))
print(json.dumps(dict(diagnostic_only=True, neck_cut_z_cm=round(NECK, 1), tail_root_cm=np.round(root, 1).tolist(), root_radius_cm=RR,
                      tail_track_first_last=[track[0], track[-1]], track_steps=len(track), pieces_after_cut_faces=pieces[:6],
                      faces_in=int(len(F)), faces_out=int(len(Fk)))))
