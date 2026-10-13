# RM-OT-05R junction repair (the ONE planned operation of reviews/rac-rmot05r-evidence/plan/PLAN.md).
#   input : B2 baseline (05Q), its vertex map, the junction sets (plan), the 05Q frame / ledges
#   C1    : flip the shared edge of B2 faces 140820 / 140812 (documented seam correction, no vertex moves)
#   per J : delete J; Tutte layout of the J submesh with the boundary on an area-matched ellipse; constrained quality
#           triangulation (Triangle q30, no boundary Steiner points); 3-D positions of new interior vertices by a uniform
#           bi-Laplacian solve (boundary + outside 1-ring fixed; garment-side boundary rows omitted -> natural termination);
#           3-D Lawson flips (min-angle gain, dihedral <= 40 deg) + re-solve, two rounds. Reconstruction is INFERRED.
# Usage: python3 r_repair.py --b2 GO-05Q-B2.obj --q05 <05Q evidence> --plan <05R plan dir> --out DIR --tag R1
import argparse, json, hashlib, os, numpy as np, trimesh, triangle
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
ap = argparse.ArgumentParser(); ap.add_argument('--b2'); ap.add_argument('--q05'); ap.add_argument('--plan'); ap.add_argument('--out'); ap.add_argument('--tag', default='R1')
ap.add_argument('--h', type=float, default=0.8); ap.add_argument('--flip_rounds', type=int, default=2); ap.add_argument('--orient', default='tutte'); ap.add_argument('--flip_winding', default='normal'); ap.add_argument('--flip_guard', default='local'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
b2 = trimesh.load(a.b2, process=False); V = np.asarray(b2.vertices, float); F = np.asarray(b2.faces, np.int64).copy()
Q = json.load(open(os.path.join(a.q05, 'plan/patch_selection.json'))); P05 = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz'))['P']; nP = len(P05)
vmapB2 = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_vertex_map.npy')); labB2 = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_face_labels.npy'))
JS = np.load(os.path.join(a.plan, 'junction_sets.npz')); JR = json.load(open(os.path.join(a.plan, 'junction_selection.json')))
O = np.array(Q['frame']['origin']); d = np.array(Q['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
lt, slo, shi = np.array(Q['ledge_theta']), np.array(Q['s_lo']), np.array(Q['s_hi']); ta, tb = Q['sector_theta_deg']
def tsr(X):
    c = X - O; return np.degrees(np.arctan2(c @ e2, c @ e1)), c @ d, np.hypot(c @ e1, c @ e2)
def minang(T):
    L = np.linalg.norm(T[:, [1, 2, 0]] - T[:, [2, 0, 1]], axis=2)
    cs = [(L[:, (i + 1) % 3]**2 + L[:, (i + 2) % 3]**2 - L[:, i]**2) / (2 * L[:, (i + 1) % 3] * L[:, (i + 2) % 3] + 1e-30) for i in range(3)]
    return np.degrees(np.arccos(np.clip(np.max(np.array(cs), 0), -1, 1)))   # smallest angle = largest cosine
rec = dict(tag=a.tag, flip_winding=a.flip_winding, orient=a.orient, flip_guard=a.flip_guard, baseline=a.b2, baseline_sha256=hashlib.sha256(open(a.b2, 'rb').read()).hexdigest(), params=dict(h=a.h, flip_rounds=a.flip_rounds, triangle='pq30Y'))
# ---- C1 seam correction
fa, fb = 140820, 140812; assert not np.isin([fa, fb], np.r_[JS['J_post_b2'], JS['J_ant_b2']]).any(); sh = np.intersect1d(F[fa], F[fb]); pa = np.setdiff1d(F[fa], sh)[0]; pb = np.setdiff1d(F[fb], sh)[0]
def oriented(tri, ref):                                              # orient tri like the face ref (shared normal sign)
    n0 = np.cross(V[ref[1]] - V[ref[0]], V[ref[2]] - V[ref[0]]); n1 = np.cross(V[tri[1]] - V[tri[0]], V[tri[2]] - V[tri[0]]); return tri if n0 @ n1 > 0 else tri[::-1]
before = minang(V[F[[fa, fb]]]).round(3).tolist()
F[fa] = oriented(np.array([pa, pb, sh[0]]), F[fa]); F[fb] = oriented(np.array([pa, pb, sh[1]]), F[fb])
rec['C1'] = dict(faces=[fa, fb], min_angle_before=before, min_angle_after=minang(V[F[[fa, fb]]]).round(3).tolist())
# ---- garment-remnant faces outside J (source faces beyond the sector edges inside the band window): their vertices mark garment-side boundary
Jall = np.r_[JS['J_post_b2'], JS['J_ant_b2']]; inJ = np.zeros(len(F), bool); inJ[Jall] = True
ct, cs_, cr = tsr(V[F].mean(1)); beyond = (ct < ta) | (ct > tb)
garm_out = ~inJ & (np.arange(len(F)) < nP) & beyond & (cs_ >= np.interp(ct, lt, slo) - 0.45) & (cs_ <= np.interp(ct, lt, shi) + 0.6) & (cr < 13) & (np.abs(ct) > 80)
garm_v = np.zeros(len(V), bool); garm_v[F[garm_out].ravel()] = True
Vn = [V.copy()]; nv0 = len(V); newfaces = []; newvert_count = 0; per = {}
Vall = V.copy()
for name, key in (('posterior', 'J_post_b2'), ('anterior', 'J_ant_b2')):
    J = JS[key]; sub = F[J]
    he = {}
    for f in sub:
        for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
    bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); loop = [bnd[0][0]]
    while nxt[loop[-1]] != loop[0]: loop.append(nxt[loop[-1]])
    loop = np.array(loop); nb = len(loop); assert nb == len(bnd), 'J must have one boundary loop'
    jv = np.unique(sub); interior_old = np.setdiff1d(jv, loop)
    # Tutte layout of the J submesh (only to orient + size the ellipse placement; the new triangulation uses the boundary only)
    Xj = Vall[jv]; tt, ss, _ = tsr(Xj); K = np.pi / 180 * 8.0; ext_t = np.ptp(tt) * K; ext_s = np.ptp(ss); asp = max(ext_t, 1e-3) / max(ext_s, 1e-3)
    area3 = trimesh.triangles.area(Vall[sub]).sum(); bb = np.sqrt(area3 / (np.pi * asp)); aa = asp * bb
    L3 = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Vall[np.r_[loop, loop[:1]]], axis=0), axis=1))]; ph = 2 * np.pi * L3[:-1] / L3[-1]
    X2 = np.c_[aa * np.cos(ph), bb * np.sin(ph)]                      # CCW along the loop order
    # orientation check with a Tutte embedding of the old J faces
    idx = {v: i for i, v in enumerate(jv)}; n_ = len(jv); Lr, Lc, Lv = [], [], []
    for f in sub:
        for i in range(3):
            for j in range(3):
                if i != j: Lr.append(idx[f[i]]); Lc.append(idx[f[j]]); Lv.append(1.0)
    A = sp.csr_matrix((Lv, (Lr, Lc)), shape=(n_, n_)); A.data[:] = 1.0; deg = np.asarray(A.sum(1)).ravel()
    Lm = sp.diags(deg) - A; isb = np.zeros(n_, bool); bidx = np.array([idx[v] for v in loop]); isb[bidx] = True
    U = np.zeros((n_, 2)); U[bidx] = X2; ii = np.where(~isb)[0]
    if len(ii): U[ii] = np.column_stack([spsolve(Lm[ii][:, ii].tocsc(), -(Lm[ii][:, bidx] @ X2[:, k])) for k in range(2)])
    sgn = np.sign(np.median([np.cross(U[idx[f[1]]] - U[idx[f[0]]], U[idx[f[2]]] - U[idx[f[0]]]) for f in sub]))
    tri = triangle.triangulate(dict(vertices=X2, segments=np.c_[np.arange(nb), (np.arange(nb) + 1) % nb]), 'pq30Ya%g' % (a.h * a.h * np.sqrt(3) / 4))
    P2 = tri['vertices']; T2 = tri['triangles'].astype(np.int64); assert (np.abs(P2[:nb] - X2) < 1e-9).all()
    if a.orient == 'tutte':
        if sgn < 0: T2 = T2[:, ::-1]
    else:   # bounded correction (R2): new faces must carry each boundary half-edge loop[i] -> loop[i+1] like the removed J faces did
        hs = set()
        for t_ in T2:
            for i in range(3): hs.add((t_[i], t_[(i + 1) % 3]))
        agree = np.mean([((i, (i + 1) % nb) in hs) for i in range(nb)])
        if agree < 0.5: T2 = T2[:, ::-1]
    nin = len(P2) - nb; gid = np.r_[loop, len(Vall) + np.arange(nin)]
    Vall = np.vstack([Vall, np.zeros((nin, 3))]); Tn = gid[T2]
    # initial interior positions: barycentric of the layout through the old J surface is not needed (linear solve)
    per[name] = dict(J=J, loop=loop, Tn=Tn, newv=gid[nb:], interior_old=interior_old, layout_area=float(np.pi * aa * bb), j_area3=float(area3), nb=nb, nin=nin, orient_flip=bool(sgn < 0))
# ---- assemble connectivity: all B2 faces except J, plus new faces
keepF = np.where(~inJ)[0]
def build_and_solve(per, Vall):
    allF = np.vstack([F[keepF]] + [per[k]['Tn'] for k in per]); nV = len(Vall)
    A = sp.coo_matrix((np.ones(allF.size * 2), (np.r_[allF.ravel(), allF[:, [1, 2, 0]].ravel()], np.r_[allF[:, [1, 2, 0]].ravel(), allF.ravel()])), shape=(nV, nV)).tocsr()
    A.data[:] = 1.0; deg = np.asarray(A.sum(1)).ravel(); deg[deg == 0] = 1
    Lu = sp.eye(nV) - sp.diags(1 / deg) @ A                       # uniform Laplacian
    unk = np.concatenate([per[k]['newv'] for k in per]); rows = list(unk)
    for k in per:
        rows += [v for v in per[k]['loop'] if not garm_v[v]]       # skin / fill-side boundary rows (C1 to the outside)
    rows = np.array(rows); M = Lu[rows]; Mu = M[:, unk]; known = np.setdiff1d(np.arange(nV), unk)
    rhs = -(M[:, known] @ Vall[known])
    N = (Mu.T @ Mu).tocsc(); X = np.column_stack([spsolve(N, Mu.T @ rhs[:, c]) for c in range(3)]); Vall = Vall.copy(); Vall[unk] = X
    return Vall, allF
Vall, allF = build_and_solve(per, Vall)
# ---- 3-D Lawson flips among new faces of each J, then re-solve
flips = {}
outsideF = F[keepF]; global_edges = set(map(tuple, np.sort(np.r_[outsideF[:, [0, 1]], outsideF[:, [1, 2]], outsideF[:, [2, 0]]], 1).tolist()))
for rnd in range(a.flip_rounds):
    nflip = 0
    for k in per:
        T = per[k]['Tn']; changed = True; guard = 0
        while changed and guard < 50:
            changed = False; guard += 1
            emap = {}
            for fi, f in enumerate(T):
                for i in range(3):
                    e = tuple(sorted((f[i], f[(i + 1) % 3]))); emap.setdefault(e, []).append(fi)
            eset = set(emap)
            for e, fl in emap.items():
                if len(fl) != 2: continue
                f0, f1 = T[fl[0]], T[fl[1]]; p0 = np.setdiff1d(f0, e)[0]; p1 = np.setdiff1d(f1, e)[0]
                if tuple(sorted((p0, p1))) in eset: continue
                if a.flip_guard == 'global' and tuple(sorted((p0, p1))) in global_edges: continue
                t0 = np.array([p0, p1, e[0]]); t1 = np.array([p0, p1, e[1]])
                n_ref = np.cross(Vall[f0[1]] - Vall[f0[0]], Vall[f0[2]] - Vall[f0[0]])
                def ori(t):
                    n1 = np.cross(Vall[t[1]] - Vall[t[0]], Vall[t[2]] - Vall[t[0]]); return t if n1 @ n_ref > 0 else t[::-1]
                if a.flip_winding == 'normal':
                    t0, t1 = ori(t0), ori(t1)
                else:   # topological winding: f0 = (x, y, p0) with edge x->y, f1 has y->x; flipped faces (p0, x, p1) and (p0, p1, y)
                    k0 = [i for i in range(3) if f0[i] not in e][0]; x_, y_ = f0[(k0 + 1) % 3], f0[(k0 + 2) % 3]
                    t0 = np.array([p0, x_, p1]); t1 = np.array([p0, p1, y_])
                n0 = np.cross(Vall[t0[1]] - Vall[t0[0]], Vall[t0[2]] - Vall[t0[0]]); n1 = np.cross(Vall[t1[1]] - Vall[t1[0]], Vall[t1[2]] - Vall[t1[0]])
                if np.linalg.norm(n0) < 1e-9 or np.linalg.norm(n1) < 1e-9: continue
                dih = np.degrees(np.arccos(np.clip(n0 @ n1 / np.linalg.norm(n0) / np.linalg.norm(n1), -1, 1)))
                if dih > 40: continue
                if minang(Vall[np.array([t0, t1])]).min() > minang(Vall[np.array([f0, f1])]).min() + 0.5:
                    T[fl[0]], T[fl[1]] = t0, t1; changed = True; nflip += 1; break
        per[k]['Tn'] = T
    flips[rnd] = nflip; Vall, allF = build_and_solve(per, Vall)
rec['lawson_flips_per_round'] = flips
# ---- output: drop deleted vertices, compact
nPkeep = int((keepF < nP).sum()); assert (keepF[:nPkeep] < nP).all()
used = np.unique(allF); cmap = -np.ones(len(Vall), np.int64); cmap[used] = np.arange(len(used)); Vo = Vall[used]; Fo = cmap[allF]
src_map = np.full(len(used), -1, np.int64); b2_map = np.full(len(used), -1, np.int64)
isb2 = used < nv0; b2_map[isb2] = used[isb2]; fromsrc = isb2 & (used < len(vmapB2)); src_map[fromsrc] = vmapB2[used[fromsrc]]
lab = np.zeros(len(Fo), np.int8); lab[:len(keepF)] = labB2[keepF]; lab[len(keepF):] = 5
out = os.path.join(a.out, 'GO-05R-%s.obj' % a.tag)
with open(out, 'w') as fh:
    fh.write('# RM-OT-05R %s: B2 with both band-end junctions rebuilt; labels 2/3 = 05Q INFERRED, 5 = 05R junction INFERRED\n' % a.tag)
    np.savetxt(fh, Vo, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fo + 1, fmt='f %d %d %d')
np.save(os.path.join(a.out, 'GO-05R-%s_face_labels.npy' % a.tag), lab)
np.savez(os.path.join(a.out, 'GO-05R-%s_maps.npz' % a.tag), src_vertex=src_map, b2_vertex=b2_map, b2_face_of_output=np.r_[keepF, -np.ones(len(Fo) - len(keepF), np.int64)])
rec.update(output=out, output_sha256=hashlib.sha256(open(out, 'rb').read()).hexdigest(), protected_faces_first=nPkeep, faces=dict(total=int(len(Fo)), b2_retained_new=int(len(keepF) - nPkeep), junction_new=int(len(Fo) - len(keepF))),
           junctions={k: dict(J_faces=int(len(v['J'])), boundary_vertices=v['nb'], new_vertices=v['nin'], new_faces=int(len(v['Tn'])), deleted_old_interior_vertices=int(len(v['interior_old'])),
                              garment_side_boundary_vertices=int(garm_v[v['loop']].sum()), j_area3_cm2=round(v['j_area3'], 2), tutte_orientation_flipped=v['orient_flip']) for k, v in per.items()},
           layout='faces: P05R (05Q order) | retained B2 new faces (B2 order, C1 applied) | junction faces; maps.npz: src_vertex (F1_working index or -1), b2_vertex (B2 index or -1)')
json.dump(rec, open(os.path.join(a.out, 'GO-05R-%s_record.json' % a.tag), 'w'), indent=1); print(json.dumps(rec, indent=1))
