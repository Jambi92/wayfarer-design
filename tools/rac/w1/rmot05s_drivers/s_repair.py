# RM-OT-05S: the ONE declared direct interface study (reviews/rac-rmot05s-evidence/plan/PLAN.md, plan commit 35479a0).
#   baseline B2 (+ C1 flip) -> per side: delete I, chart (theta*9cm, l - lA), constrained quality triangulation (Triangle,
#   no boundary Steiner points), new vertices placed EXACTLY on the designed target profile P(theta, u) of s_design.py
#   (bilinear in theta-columns / u-samples), 3-D Lawson flips (topological winding, never re-creating an existing edge).
#   No Laplacian / bi-Laplacian solve, no relaxation, no smoothing.  Checkpoints are written after every stage.
# Usage: python3 s_repair.py --b2 B2.obj --q05 <05Q ev> --plan <05S plan dir> --out DIR --tag S1
import argparse, hashlib, json, os, sys, numpy as np, trimesh, triangle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import s_lib, s_design
ap = argparse.ArgumentParser(); ap.add_argument('--b2'); ap.add_argument('--q05'); ap.add_argument('--plan'); ap.add_argument('--out'); ap.add_argument('--tag', default='S1')
ap.add_argument('--h', type=float, default=0.7); ap.add_argument('--R0', type=float, default=9.0); ap.add_argument('--chart', default='baseline'); ap.add_argument('--extend', type=int, default=0); ap.add_argument('--flip_cap', type=int, default=60); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
fr = s_lib.Frame(os.path.join(a.q05, 'plan/patch_selection.json'))
b2 = trimesh.load(a.b2, process=False); V = np.asarray(b2.vertices, float); F = np.asarray(b2.faces, np.int64).copy(); Fbase = F.copy()
P05 = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz'))['P']; nP = len(P05)
vmapB2 = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_vertex_map.npy')); labB2 = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_face_labels.npy'))
S = np.load(os.path.join(a.plan, 'interface_sets.npz')); rec = dict(tag=a.tag, extend=a.extend, chart=a.chart, flip_cap=a.flip_cap, baseline_sha256=hashlib.sha256(open(a.b2, 'rb').read()).hexdigest(), params=dict(h=a.h, R0=a.R0, triangle='pq30Y'))
def save(name, VV, FF, lab=None):
    p = os.path.join(a.out, name)
    with open(p, 'w') as fh:
        np.savetxt(fh, VV, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, FF + 1, fmt='f %d %d %d')
    if lab is not None: np.save(p.replace('.obj', '_face_labels.npy'), lab)
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def minang(T):
    L = np.linalg.norm(T[:, [1, 2, 0]] - T[:, [2, 0, 1]], axis=2)
    cs = [(L[:, (i + 1) % 3]**2 + L[:, (i + 2) % 3]**2 - L[:, i]**2) / (2 * L[:, (i + 1) % 3] * L[:, (i + 2) % 3] + 1e-30) for i in range(3)]
    return np.degrees(np.arccos(np.clip(np.max(np.array(cs), 0), -1, 1)))
# ---- C1 (documented seam correction, as in 05R)
fa, fb = 140820, 140812; sh = np.intersect1d(F[fa], F[fb]); k0 = [i for i in range(3) if F[fa][i] not in sh][0]
x_, y_ = F[fa][(k0 + 1) % 3], F[fa][(k0 + 2) % 3]; pa = F[fa][k0]; pb = np.setdiff1d(F[fb], sh)[0]
before = minang(V[F[[fa, fb]]]).round(3).tolist(); F[fa] = [pa, x_, pb]; F[fb] = [pa, pb, y_]
rec['C1'] = dict(faces=[fa, fb], min_angle_before=before, min_angle_after=minang(V[F[[fa, fb]]]).round(3).tolist())
Iall = np.r_[S['I_post_b2'], S['I_ant_b2']]; assert not np.isin([fa, fb], Iall).any()
inI = np.zeros(len(F), bool); inI[Iall] = True; keepF = np.where(~inI)[0]
Vall = V.copy(); sides = {}
for name, key in (('posterior', 'I_post_b2'), ('anterior', 'I_ant_b2')):
    D = dict(np.load(os.path.join(a.plan, 'design_%s.npz' % name))); th = D['theta']; lo = th.min(); NU = D['P'].shape[1]
    I = S[key]; sub = F[I]; he = {}
    for f in sub:
        for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
    bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); loop = [bnd[0][0]]
    while nxt[loop[-1]] != loop[0]: loop.append(nxt[loop[-1]])
    loop = np.array(loop); nb = len(loop); assert nb == len(bnd)
    if a.chart == 'baseline':
        cc = {}; ch, dist = s_lib.chart_points(fr, V, Fbase, V[loop], D, cc)
    else:   # correction pass (S2): normalized baseline position t (robust ordering) re-scaled by the TARGET profile length,
            # so chart distances follow the designed surface instead of the crinkled B2 junction surface
        cc = {}; ch, dist = s_lib.chart_points(fr, V, Fbase, V[loop], D, cc)
        LP = np.array([s_lib.arclen(D['P'][k])[-1] for k in range(len(th))])
        for i in range(nb):
            k = int(np.clip(np.round((ch[i, 0] - lo) / 0.25), 0, len(th) - 1)); ch[i, 1] = ch[i, 1] / (D['lB'][k] - D['lA'][k]) * LP[k]
    X2 = np.c_[np.radians(ch[:, 0]) * a.R0, ch[:, 1]]
    cr = s_lib.simple_polygon_crossings(X2); clamped = []
    if cr:   # layout-only clamp of boundary vertices beyond the zone-end columns
        for i in range(nb):
            if ch[i, 0] < lo or ch[i, 0] > th.max(): X2[i, 0] = np.radians(np.clip(ch[i, 0], lo, th.max())) * a.R0; clamped.append(int(loop[i]))
        cr = s_lib.simple_polygon_crossings(X2)
    if cr:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        XX = np.r_[X2, X2[:1]]; plt.figure(figsize=(8, 8)); plt.plot(XX[:, 0], XX[:, 1], 'k.-'); [plt.text(X2[i, 0], X2[i, 1], str(i), fontsize=6) for i in range(nb)]; plt.savefig(os.path.join(a.out, 'chart_fail_%s_%s.png' % (a.tag, name)), dpi=90)
        json.dump(dict(side=name, crossings=cr, chart=X2.tolist(), proj_dist=dist.tolist()), open(os.path.join(a.out, 'chart_fail_%s_%s.json' % (a.tag, name)), 'w'))
    assert cr == 0, 'chart still self-intersecting'
    tri = triangle.triangulate(dict(vertices=X2, segments=np.c_[np.arange(nb), (np.arange(nb) + 1) % nb]), 'pq30Ya%g' % (a.h * a.h * np.sqrt(3) / 4))
    P2 = tri['vertices']; T2 = tri['triangles'].astype(np.int64); assert (np.abs(P2[:nb] - X2) < 1e-9).all()
    hs = set((t_[i], t_[(i + 1) % 3]) for t_ in T2 for i in range(3))
    if np.mean([((i, (i + 1) % nb) in hs) for i in range(nb)]) < 0.5: T2 = T2[:, ::-1]
    nin = len(P2) - nb; thn = np.degrees(P2[nb:, 0] / a.R0); ln = P2[nb:, 1]
    # exact placement on the designed target: bilinear in (column, u)
    kf = np.clip((thn - lo) / 0.25, 0, len(th) - 1.000001); k0_ = np.floor(kf).astype(int); fk = kf - k0_
    Xn = np.zeros((nin, 3)); basecols = {}
    for j in range(nin):
        pts = []
        for kk, wk in ((k0_[j], 1 - fk[j]), (k0_[j] + 1, fk[j])):
            den = (D['lB'][kk] - D['lA'][kk]) if a.chart == 'baseline' else LP[kk]
            ur = ln[j] / den
            if a.extend and (ur < 0 or ur > 1):   # correction pass (S3): beyond A / B the target IS the baseline surface (continue along its column)
                if kk not in basecols: basecols[kk] = s_lib.profile(fr, V, Fbase, th[kk], (8.0, D['s_led'][kk] - 4.0))[0]
                Pb = basecols[kk]; Lb = s_lib.arclen(Pb); lq = D['lA'][kk] + ur * den if ur < 0 else D['lB'][kk] + (ur - 1) * den
                rs = s_lib.at_len(Pb, Lb, lq)[0]; pts.append((wk, fr.to3(th[kk], rs[1], rs[0])[0])); continue
            u = np.clip(ur, 0, 1) * (NU - 1); u0 = int(min(np.floor(u), NU - 2)); fu = u - u0
            rs = (1 - fu) * D['P'][kk][u0] + fu * D['P'][kk][u0 + 1]; pts.append((wk, fr.to3(th[kk], rs[1], rs[0])[0]))
        Xn[j] = pts[0][0] * pts[0][1] + pts[1][0] * pts[1][1]
    gid = np.r_[loop, len(Vall) + np.arange(nin)]; Vall = np.vstack([Vall, Xn]); Tn = gid[T2]
    wv = s_design.wfun(np.r_[ch[:, 0], thn], s_design.ZONES[name])
    sides[name] = dict(I=I, loop=loop, Tn=Tn, newv=gid[nb:], nb=nb, nin=nin, clamped=clamped, chart_crossings=cr, w_at_tri=np.r_[wv][T2].mean(1), proj_max=float(dist.max()))
allF0 = np.vstack([F[keepF]] + [sides[k]['Tn'] for k in sides])
rec['checkpoint_preflip_sha256'] = save('GO-05S-%s_ckpt1_preflip.obj' % a.tag, Vall, allF0)
# ---- 3-D Lawson flips among new faces (topological winding; never re-create an existing edge)
outE = set(map(tuple, np.sort(np.r_[F[keepF][:, [0, 1]], F[keepF][:, [1, 2]], F[keepF][:, [2, 0]]], 1).tolist())); flips = {}
for name in sides:
    T = sides[name]['Tn'].copy(); n = 0
    for _ in range(a.flip_cap):
        emap = {}
        for fi, f in enumerate(T):
            for i in range(3): emap.setdefault(tuple(sorted((f[i], f[(i + 1) % 3]))), []).append(fi)
        eset = set(emap); done = False
        for e, fl in emap.items():
            if len(fl) != 2: continue
            f0, f1 = T[fl[0]], T[fl[1]]; p0 = [v for v in f0 if v not in e][0]; p1 = [v for v in f1 if v not in e][0]; ne_ = tuple(sorted((p0, p1)))
            if ne_ in eset or ne_ in outE: continue
            k0 = list(f0).index(p0); x_, y_ = f0[(k0 + 1) % 3], f0[(k0 + 2) % 3]; t0 = np.array([p0, x_, p1]); t1 = np.array([p0, p1, y_])
            n0 = np.cross(Vall[t0[1]] - Vall[t0[0]], Vall[t0[2]] - Vall[t0[0]]); n1 = np.cross(Vall[t1[1]] - Vall[t1[0]], Vall[t1[2]] - Vall[t1[0]])
            if np.linalg.norm(n0) < 1e-9 or np.linalg.norm(n1) < 1e-9: continue
            if np.degrees(np.arccos(np.clip(n0 @ n1 / np.linalg.norm(n0) / np.linalg.norm(n1), -1, 1))) > 40: continue
            if minang(Vall[np.array([t0, t1])]).min() >= minang(Vall[np.array([f0, f1])]).min() + 0.5:
                T[fl[0]], T[fl[1]] = t0, t1; n += 1; done = True; break
        if not done: break
    sides[name]['Tn'] = T; flips[name] = n
rec['lawson_flips'] = flips
# ---- assemble final
nPkeep = int((keepF < nP).sum()); allF = np.vstack([F[keepF]] + [sides[k]['Tn'] for k in sides])
used = np.unique(allF); cmap = -np.ones(len(Vall), np.int64); cmap[used] = np.arange(len(used)); Vo = Vall[used]; Fo = cmap[allF]
src_map = np.full(len(used), -1, np.int64); b2_map = np.full(len(used), -1, np.int64); isb2 = used < len(V); b2_map[isb2] = used[isb2]
fs = isb2 & (used < len(vmapB2)); src_map[fs] = vmapB2[used[fs]]
lab = np.zeros(len(Fo), np.int8); lab[:len(keepF)] = labB2[keepF]; off = len(keepF)
for k in sides:
    T = sides[k]['Tn']; wT = sides[k]['w_at_tri']; lab[off:off + len(T)] = np.where(wT >= 0.99, 5, 4); off += len(T)
rec['output_sha256'] = save('GO-05S-%s.obj' % a.tag, Vo, Fo, lab)
np.savez(os.path.join(a.out, 'GO-05S-%s_maps.npz' % a.tag), src_vertex=src_map, b2_vertex=b2_map, b2_face_of_output=np.r_[keepF, -np.ones(len(Fo) - len(keepF), np.int64)])
rec.update(protected_faces_first=nPkeep, faces=dict(total=int(len(Fo)), b2_retained_new=int(len(keepF) - nPkeep), interface_new=int(len(Fo) - len(keepF)), label5_skin=int((lab == 5).sum()), label4_transition=int((lab == 4).sum())),
           sides={k: dict(I_faces=int(len(v['I'])), boundary_vertices=v['nb'], new_vertices=v['nin'], new_faces=int(len(v['Tn'])), chart_crossings=v['chart_crossings'], layout_clamped=v['clamped'], max_chart_projection_cm=round(v['proj_max'], 3)) for k, v in sides.items()},
           layout='faces: P05S (05Q order) | retained B2 new faces (B2 order, C1) | interface faces (posterior, anterior); labels 0 source, 2/3 B2 inferred, 5 05S inferred skin, 4 05S transition/termination (inferred)')
json.dump(rec, open(os.path.join(a.out, 'GO-05S-%s_record.json' % a.tag), 'w'), indent=1); print(json.dumps(rec, indent=1))
