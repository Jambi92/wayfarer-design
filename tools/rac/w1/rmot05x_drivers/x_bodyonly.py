# RM-OT-05X (order §2): DISPOSABLE DIAGNOSTIC copy for body-only identity views. Not a repair, not a production edit, and excluded
# from every topology claim about the intact source. It deletes faces only (no vertex moves): head above the neck root and the tail
# beyond its root, then keeps the largest connected piece. The output is checked by w_tile_check.py after rendering.
# Cut rules (raw source units, Blender-like cm axes X right, Y back (front = -Y), Z up; declared, builder-chosen):
#   head: face centroid Z > NECK_Z (neck root = minimum neck section, measured 162 cm raw; cut at 160);
#   tail: face centroid Y > TAIL_Y and Z < TAIL_ZMAX (behind the buttock plane, below the lumbar region).
# Usage: python3 x_bodyonly.py welded.npz OUT.npz [NECK_Z=160] [TAIL_Y=-21] [TAIL_ZMAX=112]
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
d = np.load(sys.argv[1]); P = d['V'].astype(np.float64); F = d['F']
NECK_Z, TAIL_Y, TAIL_ZMAX = [float(x) for x in (sys.argv[3:6] + ['160', '-21', '112'][len(sys.argv[3:6]):])]
V = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) * 100; c = V[F].mean(1)
drop_head = c[:, 2] > NECK_Z; drop_tail = (c[:, 1] > TAIL_Y) & (c[:, 2] < TAIL_ZMAX); keep = ~(drop_head | drop_tail)
Fk = F[keep]; n = len(V)
E = np.concatenate([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]])
nc, lab = connected_components(sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)), directed=False)
fl = lab[Fk[:, 0]]; sizes = np.bincount(fl); big = np.argmax(sizes); dropped_pieces = [int(s) for s in sorted(sizes[sizes > 0], reverse=True)[1:]]
Fk = Fk[fl == big]; u = np.unique(Fk); mp = -np.ones(n, np.int64); mp[u] = np.arange(len(u))
np.savez(sys.argv[2], V=P[u].astype(np.float32), F=mp[Fk].astype(np.int32))
print(json.dumps(dict(diagnostic_only=True, neck_cut_z_cm=NECK_Z, tail_rule=dict(y_gt=TAIL_Y, z_lt=TAIL_ZMAX), faces_in=int(len(F)),
                      head_faces_hidden=int(drop_head.sum()), tail_faces_hidden=int((drop_tail & ~drop_head).sum()),
                      other_pieces_dropped_faces=dropped_pieces, faces_out=int(len(Fk)))))
