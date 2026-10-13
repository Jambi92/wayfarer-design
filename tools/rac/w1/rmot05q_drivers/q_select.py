# RM-OT-05Q patch selection: +X upper-arm armband, lateral exposed arc only (the medial arc runs into the fused
# arm/trunk axillary contact and is NOT touched). Arm-local cylindrical frame: axis d (fitted to the band's lower-ledge
# plane), origin O (arm cross-section centroid just below the band); theta 0 = lateral (+X), +90 = anterior (+Y).
#   ledge curves:  s_lo(theta) = band lower ledge (faces facing down the axis), s_hi(theta) = upper ledge (facing up);
#   G (garment)  = faces connected to a seed on the band face, theta in [ta, tb], s in [s_lo - dg, s_hi + dg], r < rmax;
#   S (seam band)= faces in the same sector with s in [s_lo - ds, s_hi + ds] minus G (skin that is re-triangulated);
#   P (protected)= every other face of F1: coordinates and indices must be bit-identical after the repair.
# Usage: python3 q_select.py --mesh F1_welded.obj --out DIR
import argparse, json, hashlib, numpy as np, trimesh
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--out')
ap.add_argument('--ta', type=float, default=-97.0); ap.add_argument('--tb', type=float, default=88.0)
ap.add_argument('--dg', type=float, default=0.45); ap.add_argument('--ds', type=float, default=1.8); ap.add_argument('--rmax', type=float, default=13.0); a = ap.parse_args()
m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices); F = np.asarray(m.faces)
d = np.array([-0.294, -0.054, 0.954]); d /= np.linalg.norm(d); O = np.array([30.5, -1.3, 160.4])
e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
c = V[F].mean(1) - O; s = c @ d; x1 = c @ e1; x2 = c @ e2; r = np.hypot(x1, x2); th = np.degrees(np.arctan2(x2, x1))
N = m.face_normals; na = N @ d; A = m.area_faces
bins = np.arange(a.ta - 10, a.tb + 10.01, 5.0); bc = 0.5 * (bins[1:] + bins[:-1])
def ledge(mask):
    out = np.full(len(bc), np.nan)
    for i in range(len(bc)):
        k = mask & (th >= bins[i]) & (th < bins[i + 1])
        if A[k].sum() > 0.05:
            o = np.argsort(s[k]); cw = np.cumsum(A[k][o]); out[i] = s[k][o][np.searchsorted(cw, cw[-1] / 2)]
    ok = ~np.isnan(out); out = np.interp(bc, bc[ok], out[ok]); return np.convolve(np.r_[out[0], out, out[-1]], [1 / 3] * 3, 'valid')
s_lo = ledge((na < -0.55) & (s > -1) & (s < 3) & (r < a.rmax)); s_hi = ledge((na > 0.55) & (s > 3.5) & (s < 8) & (r < a.rmax))
lo = np.interp(th, bc, s_lo); hi = np.interp(th, bc, s_hi); sect = (th >= a.ta) & (th <= a.tb) & (r < a.rmax)
win = sect & (s >= lo - a.dg) & (s <= hi + a.dg)
adj = m.face_adjacency; ok = win[adj[:, 0]] & win[adj[:, 1]]
nc, lab = connected_components(sp.coo_matrix((np.ones(ok.sum()), (adj[ok, 0], adj[ok, 1])), shape=(len(F), len(F))), directed=False)
cand = np.where(win & (np.abs(th - 60) < 4) & (np.abs(s - 0.5 * (lo + hi)) < 0.6))[0]; seed = cand[np.argmax(r[cand])]
G = np.where(lab == lab[seed])[0]
winS = sect & (s >= lo - a.ds) & (s <= hi + a.ds); okS = winS[adj[:, 0]] & winS[adj[:, 1]]
ncS, labS = connected_components(sp.coo_matrix((np.ones(okS.sum()), (adj[okS, 0], adj[okS, 1])), shape=(len(F), len(F))), directed=False)
Rg = np.where(labS == labS[seed])[0]; S = np.setdiff1d(Rg, G)
# fill pin-holes: protected islands fully enclosed by the removed region are absorbed into S (so the hole is a disk)
rem = np.zeros(len(F), bool); rem[Rg] = True
okP = ~rem[adj[:, 0]] & ~rem[adj[:, 1]]
ncP, labP = connected_components(sp.coo_matrix((np.ones(okP.sum()), (adj[okP, 0], adj[okP, 1])), shape=(len(F), len(F))), directed=False)
big = np.bincount(labP[~rem]).argmax()
touch = np.zeros(len(F), bool); touch[np.unique(F[rem])] = True
near_lab = np.unique(labP[~rem & touch[F].any(1)])   # protected components sharing a vertex with the removed region
absorb = np.where(~rem & (labP != big) & np.isin(labP, near_lab))[0]; G = np.union1d(G, absorb); rem[absorb] = True   # enclosed islands lie on the band surface at the sector ends -> garment
P = np.where(~rem)[0]
sub = trimesh.Trimesh(V, F[rem], process=False); be = sub.edges_sorted; u, cnt = np.unique(be, axis=0, return_counts=True); bnd = u[cnt == 1]
# boundary loop count
g = {}
for x, y in bnd: g.setdefault(x, []).append(y); g.setdefault(y, []).append(x)
seen = set(); loops = 0
for v0 in g:
    if v0 in seen: continue
    loops += 1; st = [v0]
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); st += g[x]
nv = len(np.unique(F[rem])); ne = len(np.unique(sub.edges_sorted, axis=0)); chi = nv - ne + int(rem.sum())
lab_all = np.zeros(len(F), np.int8); lab_all[G] = 1; lab_all[S] = 3
np.save(a.out + '/patch_face_labels.npy', lab_all)
np.savez(a.out + '/patch_face_sets.npz', G=G, S=S, P=P, absorbed=absorb)
H = lambda x: hashlib.sha256(np.ascontiguousarray(x).astype(np.int64).tobytes()).hexdigest()
bb = lambda idx: np.round(np.r_[V[F[idx]].reshape(-1, 3).min(0), V[F[idx]].reshape(-1, 3).max(0)], 2).tolist()
ncR = connected_components(sp.coo_matrix((np.ones((rem[adj[:,0]]&rem[adj[:,1]]).sum()), (adj[rem[adj[:,0]]&rem[adj[:,1]],0], adj[rem[adj[:,0]]&rem[adj[:,1]],1])), shape=(len(F), len(F))), directed=False)
rcomp = len(np.unique(ncR[1][rem]))
rec = dict(mesh=a.mesh, mesh_sha256=hashlib.sha256(open(a.mesh, 'rb').read()).hexdigest(), frame=dict(origin=O.tolist(), axis=d.round(5).tolist(), e1_lateral=e1.round(5).tolist(), e2=e2.round(5).tolist()),
           sector_theta_deg=[a.ta, a.tb], dg=a.dg, ds=a.ds, rmax=a.rmax, seed_face=int(seed),
           ledge_theta=bc.round(1).tolist(), s_lo=s_lo.round(3).tolist(), s_hi=s_hi.round(3).tolist(),
           G=dict(absorbed_enclosed_island_faces=int(len(absorb)), faces=int(len(G)), area_cm2=round(float(A[G].sum()), 2), bounds=bb(G), sha256=H(G)),
           S=dict(faces=int(len(S)), area_cm2=round(float(A[S].sum()), 2), bounds=bb(S), sha256=H(S), ),
           P=dict(faces=int(len(P)), sha256=H(P)), removed_region=dict(faces=int(rem.sum()), boundary_edges=int(len(bnd)), boundary_loops=loops, euler=chi, components=rcomp))
json.dump(rec, open(a.out + '/patch_selection.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k not in ('ledge_theta', 's_lo', 's_hi')}, indent=1))
