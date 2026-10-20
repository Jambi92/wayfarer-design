"""RAC RP1-D gate measurements on the production mesh (analysis frame cm) against the welded source.
Topology (components, boundary, non-manifold, Euler/genus, face types, orientation, degenerates), T-3 stature/bbox, T-4 quad angle /
aspect, T-5 density by zone (mean edge / stature), T-1/T-2 two-way deviation by zone (+ per-vertex arrays), T-7 silhouette IoU
(orthographic rasterisation, 1 px = 1 mm, identical frame), Gorrund nail projection per nail (AW4 plate masks).
Usage: python3 rp1_gate.py PROD.npz weld_a.npz zones.npz AW4_VF.npz plates.npy footframes.json OUTDIR"""
import sys, json, os, numpy as np, igl
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
P, W, Z, AW, PLp, FFp, out = sys.argv[1:8]; os.makedirs(out, exist_ok=True)
p = np.load(P); V = p['V'].astype(float); F = p['F'].astype(np.int64); Q = p['Q'].astype(np.int64)
w = np.load(W); S = w['V'].astype(float); SF = w['F'].astype(np.int64)
zz = np.load(Z); zone = zz['zone']; names = list(zz['names'])
R = {}
# ---------- topology ----------
polys = [q[q >= 0] for q in Q]; nside = np.array([len(q) for q in polys])
E = np.concatenate([np.c_[q, np.roll(q, -1)] for q in polys]); Eu, cnt = np.unique(np.sort(E, 1), axis=0, return_counts=True)
de, dcnt = np.unique(E, axis=0, return_counts=True)
G = coo_matrix((np.ones(len(Eu)), (Eu[:, 0], Eu[:, 1])), shape=(len(V), len(V)))
ncomp = connected_components(G, directed=False)[0]
chi = len(V) - len(Eu) + len(polys)
vol = float(np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6.0)
area = 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)
used = np.zeros(len(V), bool); used[F.ravel()] = True
R['topology'] = dict(vertices=int(len(V)), faces=int(len(polys)), quads=int((nside == 4).sum()), tris=int((nside == 3).sum()), ngons=int((nside > 4).sum()),
                     quad_share_pct=round(float((nside == 4).mean() * 100), 3), components=int(ncomp), boundary_edges=int((cnt == 1).sum()),
                     nonmanifold_edges=int((cnt > 2).sum()), euler_characteristic=int(chi), genus=(2 - chi) / 2 if ncomp == 1 else None,
                     directed_edge_duplicates=int((dcnt > 1).sum()), signed_volume_cm3=round(vol, 1), orientation='outward' if vol > 0 and (dcnt > 1).sum() == 0 else 'CHECK',
                     degenerate_faces=int((area < 1e-8).sum()), loose_vertices=int((~used).sum()))
# ---------- T-3 ----------
R['T3'] = dict(source_bbox_min=S.min(0).round(3).tolist(), source_bbox_max=S.max(0).round(3).tolist(), prod_bbox_min=V.min(0).round(3).tolist(), prod_bbox_max=V.max(0).round(3).tolist(),
               stature_source_cm=round(float(S[:, 2].max() - S[:, 2].min()), 4), stature_prod_cm=round(float(V[:, 2].max() - V[:, 2].min()), 4))
R['T3']['stature_delta_mm'] = round((R['T3']['stature_prod_cm'] - R['T3']['stature_source_cm']) * 10, 3)
R['T3']['bbox_delta_mm'] = dict(min=((V.min(0) - S.min(0)) * 10).round(3).tolist(), max=((V.max(0) - S.max(0)) * 10).round(3).tolist())
# ---------- deviation ----------
Smp = np.vstack([V[F].mean(1), (V[F[:, 0]] + V[F[:, 1]]) / 2])
dps, Ips, _ = igl.point_mesh_squared_distance(Smp, S, SF); dps = np.sqrt(dps) * 10; zps = zone[SF[Ips, 0]]
dsp, _, _ = igl.point_mesh_squared_distance(S, V, F); dsp = np.sqrt(dsp) * 10
dv, Iv, _ = igl.point_mesh_squared_distance(V, S, SF); dv = np.sqrt(dv) * 10; zv = zone[SF[Iv, 0]]
np.savez_compressed(os.path.join(out, 'deviation_arrays.npz'), src_to_prod_mm=dsp.astype(np.float32), prod_vert_to_src_mm=dv.astype(np.float32), prod_vert_zone=zv.astype(np.int8))
R['deviation'] = {}
for i, nm in enumerate(names):
    a = dps[zps == i]; b = dsp[zone == i]
    lim = (0.5, 1.5, 3.0) if nm == 'general' else (0.3, 0.8, 1.5)
    st = lambda x: [round(float(v), 3) for v in (np.median(x), np.percentile(x, 95), x.max())]
    pa, pb = st(a), st(b); ok = all(q[0] <= lim[0] and q[1] <= lim[1] and q[2] <= lim[2] for q in (pa, pb))
    R['deviation'][nm] = dict(limit_med_p95_max_mm=list(lim), prod_to_src_mm=pa, src_to_prod_mm=pb, src_over_max_pct=round(float((b > lim[2]).mean() * 100), 3),
                              prod_over_max_pct=round(float((a > lim[2]).mean() * 100), 3), within=bool(ok))
# ---------- T-4 / T-5 ----------
QQ = Q[nside == 4]; A = V[QQ]; ang = []
for k in range(4):
    u = A[:, (k + 1) % 4] - A[:, k]; v = A[:, (k - 1) % 4] - A[:, k]
    ang.append(np.degrees(np.arccos(np.clip(np.einsum('ij,ij->i', u, v) / (np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1) + 1e-12), -1, 1))))
ang = np.stack(ang, 1); el = np.stack([np.linalg.norm(A[:, (k + 1) % 4] - A[:, k], axis=1) for k in range(4)], 1); asp = el.max(1) / np.maximum(el.min(1), 1e-9)
R['T4'] = dict(quads_all_angles_45_135_pct=round(float(((ang >= 45) & (ang <= 135)).all(1).mean() * 100), 3), quads_aspect_le4_pct=round(float((asp <= 4).mean() * 100), 3),
               angle_p1_p99=[round(float(np.percentile(ang, 1)), 1), round(float(np.percentile(ang, 99)), 1)], aspect_p99=round(float(np.percentile(asp, 99)), 2))
H = R['T3']['stature_source_cm']; Eul = np.linalg.norm(V[Eu[:, 0]] - V[Eu[:, 1]], axis=1); ze = zv[Eu[:, 0]]
R['T5_density_mean_edge_pct_of_stature'] = {nm: round(float(Eul[ze == i].mean() / H * 100), 4) for i, nm in enumerate(names) if (ze == i).any()}
# ---------- T-7 silhouette IoU ----------
def raster(X, T, ax_h, ax_v, flip, box):
    x0, x1, y0, y1 = box; Wd = int(round((x1 - x0) * 10)) + 2; Ht = int(round((y1 - y0) * 10)) + 2
    im = Image.new('1', (Wd, Ht), 0); d = ImageDraw.Draw(im)
    h = (X[:, ax_h] * (-1 if flip else 1) - x0) * 10; v = (y1 - X[:, ax_v]) * 10
    for t in T: d.polygon([(h[t[0]], v[t[0]]), (h[t[1]], v[t[1]]), (h[t[2]], v[t[2]])], fill=1)
    return np.array(im)
R['T7_iou'] = {}
allP = np.vstack([V, S])
for nm, (ah, av, fl) in {'front': (0, 2, False), 'profile': (1, 2, False), 'rear': (0, 2, True)}.items():
    hh = allP[:, ah] * (-1 if fl else 1); box = (hh.min() - 1, hh.max() + 1, allP[:, 2].min() - 1, allP[:, 2].max() + 1)
    a = raster(V, F, ah, av, fl, box); b = raster(S, SF, ah, av, fl, box)
    R['T7_iou'][nm] = round(float((a & b).sum() / (a | b).sum()), 5)
    Image.fromarray((np.dstack([a & ~b, a & b, ~a & b]) * 255).astype(np.uint8)).save(os.path.join(out, 'iou_%s.png' % nm))
# ---------- nails ----------
if AW=="none":
    json.dump(R, open(os.path.join(out, "rp1_gate.json"), "w"), indent=1); sys.exit()
X = np.load(AW)['V'].astype(float); PL = np.load(PLp, allow_pickle=True).item(); FFj = json.load(open(FFp))
Vb = np.c_[V[:, 0], -V[:, 1], V[:, 2]] / 100.0           # production in Blender metres (AW4 frame)
from scipy.spatial import cKDTree
R['nails'] = {}
for n, pl in PL.items():
    a = np.array(FFj[n[0]]['a']); nail = pl['w'] > 0.3; Np = X[nail]
    tr = cKDTree(Np); dd, _ = tr.query(Vb, distance_upper_bound=0.002); reg = np.isfinite(dd)
    sp = float((Np @ a).max()); pp = float((Vb[reg] @ a).max()) if reg.any() else float('nan')
    R['nails'][n] = dict(source_tip_along_axis_m=round(sp, 5), production_tip_along_axis_m=round(pp, 5), projection_delta_mm=round((pp - sp) * 1000, 3),
                         production_points_in_plate_region=int(reg.sum()))
json.dump(R, open(os.path.join(out, 'rp1_gate.json'), 'w'), indent=1)
print(json.dumps(R, indent=1))
