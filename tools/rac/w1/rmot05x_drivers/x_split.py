# RM-OT-05X R1: split a multi-figure source GLB into its connected figures for REVIEW ONLY. Each figure is written as a
# diagnostic copy with a RIGID display transform (translation to the origin in X/Y, rotation about the vertical axis so the face
# points to -Y in the review frame); vertex-to-vertex distances are unchanged and nothing is smoothed, deleted or moved relative
# to the figure itself. Facing is estimated from the head-vs-upper-trunk horizontal offset (muzzle forward) and snapped to 90 deg.
# Output npz uses glTF axes (V metres) so x_render.py / x_bodyonly.py work unchanged. Never writes the source.
# Usage: python3 x_split.py SOURCE.glb OUTDIR  -> OUTDIR/fig<k>.npz + figures.json
import sys, os, json, struct, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
src, od = sys.argv[1:3]; os.makedirs(od, exist_ok=True); b = open(src, 'rb').read()
cl = struct.unpack('<I', b[12:16])[0]; J = json.loads(b[20:20 + cl]); o = 20 + cl; bl = struct.unpack('<I', b[o:o + 4])[0]; B = b[o + 8:o + 8 + bl]
def acc(i, dt, nc):
    a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.frombuffer(B, dt, a['count'] * nc, off).reshape(a['count'], nc)
pr = J['meshes'][0]['primitives'][0]; P = acc(pr['attributes']['POSITION'], np.float32, 3); I = acc(pr['indices'], np.uint32, 1).reshape(-1, 3)
U, inv = np.unique(P, axis=0, return_inverse=True); F = inv.ravel()[I]; n = len(U)
E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
nc, lab = connected_components(sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)), directed=False)
fl = lab[F[:, 0]]; out = []
for k in np.argsort(-np.bincount(fl)):
    Fk = F[fl == k]; u = np.unique(Fk); mp = -np.ones(n, np.int64); mp[u] = np.arange(len(u)); V = U[u].astype(np.float64); Fk = mp[Fk]
    R = np.stack([V[:, 0], -V[:, 2], V[:, 1]], 1)                       # review frame (m): X right, Y back, Z up
    H = R[:, 2].max() - R[:, 2].min(); z0 = R[:, 2].min()
    head = R[R[:, 2] > z0 + 0.90 * H]; trunk = R[(R[:, 2] > z0 + 0.60 * H) & (R[:, 2] < z0 + 0.72 * H)]
    hd = head[:, :2].mean(0) - np.median(trunk[:, :2], 0); ang = np.degrees(np.arctan2(hd[1], hd[0]))   # direction the head leans/points
    face = int(np.round(ang / 90.0) * 90) % 360                         # 0:+X 90:+Y 180:-X 270:-Y
    rot = (270 - face) % 360                                            # rotate so the face points to -Y
    t = np.radians(rot); c, s = np.cos(t), np.sin(t)
    ctr = np.array([np.median(trunk[:, 0]), np.median(trunk[:, 1])])
    X = R[:, 0] - ctr[0]; Y = R[:, 1] - ctr[1]; R2 = np.stack([c * X - s * Y, s * X + c * Y, R[:, 2] - z0], 1)
    G = np.stack([R2[:, 0], R2[:, 2], -R2[:, 1]], 1)                    # back to glTF axes
    i = len(out); np.savez(os.path.join(od, 'fig%d.npz' % i), V=G.astype(np.float32), F=Fk.astype(np.int32))
    Ed = np.sort(np.concatenate([Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]]), axis=1); ue = np.unique(Ed, axis=0); chi = len(u) - len(ue) + len(Fk)
    out.append(dict(figure=i, faces=int(len(Fk)), vertices=int(len(u)), euler=int(chi), genus=int((2 - chi) // 2),
                    source_bounds_review_cm=[(R.min(0) * 100).round(1).tolist(), (R.max(0) * 100).round(1).tolist()], raw_height_cm=round(H * 100, 1),
                    head_offset_dir_deg=round(float(ang), 1), facing_in_source=['+X', '+Y (back)', '-X', '-Y (front)'][face // 90], display_yaw_deg=rot,
                    display_translation_cm=(-ctr * 100).round(1).tolist()))
json.dump(dict(source=os.path.basename(src), note='diagnostic display copies: rigid transform only', figures=out), open(os.path.join(od, 'figures.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
