# RM-OT-05R junction selection on the B2 baseline (dry run: no geometry is changed here).
# For each band end a region J is selected in the 05Q arm-local frame (theta 0 lateral, +90 anterior; s along the arm):
#   fill side   : B2 new faces (labels 2/3) with theta between the sector edge and t_in (the end of B2's ramp zone);
#   extension   : protected source faces with theta between t_out and the sector edge, s >= s_lo - 1.8 and s <= top(theta)
#                 (posterior: 0.25 cm below the fold-edge overhang; anterior: a fixed cap above the lip), r < rmax;
#   the connected component of these faces touching the sector edge, with enclosed islands absorbed (disk).
# Reports counts, boundary topology, layout simplicity in (theta*8cm, s), and the extension relative to 05Q R (879 faces).
# Usage: python3 r_select.py --src F1_working.obj --b2 GO-05Q-B2.obj --q05 <05Q evidence dir> --out DIR
import argparse, json, hashlib, os, numpy as np, trimesh
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--b2'); ap.add_argument('--q05'); ap.add_argument('--out'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
J = json.load(open(os.path.join(a.q05, 'plan/patch_selection.json'))); Z = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz')); P05 = Z['P']; nP = len(P05)
src = trimesh.load(a.src, process=False); b2 = trimesh.load(a.b2, process=False); V = np.asarray(b2.vertices); F = np.asarray(b2.faces)
lab = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_face_labels.npy')); vmap = np.load(os.path.join(a.q05, 'repair/GO-05Q-B2_vertex_map.npy'))
O = np.array(J['frame']['origin']); d = np.array(J['frame']['axis']); d /= np.linalg.norm(d); e1 = np.cross([0, 1, 0], d); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1); K = np.pi / 180 * 8.0
def tsr(X):
    c = X - O; return np.degrees(np.arctan2(c @ e2, c @ e1)), c @ d, np.hypot(c @ e1, c @ e2)
t, s, r = tsr(b2.triangles_center); na = b2.face_normals @ d; lt, slo, shi = np.array(J['ledge_theta']), np.array(J['s_lo']), np.array(J['s_hi'])
ta, tb = J['sector_theta_deg']; isnew = np.arange(len(F)) >= nP
lo = np.interp(t, lt, slo) - 1.8
# posterior fold-edge line: lowest s of strongly down-facing faces above the band (per 2 deg bin), smoothed
bins = np.arange(-120, -90, 2.0); edge = []
for b in bins:
    k = ~isnew & (t >= b) & (t < b + 2) & (na < -0.55) & (s > 3) & (s < 8) & (r < 12)
    edge.append(np.percentile(s[k], 10) if k.sum() >= 2 else np.nan)
edge = np.array(edge); ok = ~np.isnan(edge); edge = np.interp(bins + 1, (bins + 1)[ok], edge[ok])
ENDS = dict(posterior=dict(t_out=-110.0, t_edge=ta, t_in=-82.0, top=lambda tt: np.interp(tt, bins + 1, edge) - 0.25, rmax=11.0),
            anterior=dict(t_out=102.0, t_edge=tb, t_in=74.0, top=lambda tt: np.full_like(tt, 4.5), rmax=13.0))
adj = b2.face_adjacency; rec = dict(baseline=a.b2, baseline_sha256=hashlib.sha256(open(a.b2, 'rb').read()).hexdigest(), frame=J['frame'], ends={})
labJ = np.zeros(len(F), np.int8); sets = {}
for name, E in ENDS.items():
    t0, t1 = sorted((E['t_out'], E['t_in'])); inT = (t >= t0) & (t <= t1)
    side_ext = (t - E['t_edge']) * np.sign(E['t_out'] - E['t_edge']) > 0                      # beyond the 05Q sector edge
    fill = inT & isnew                                                                       # all B2 faces in the theta window (incl. those beyond the edge)
    ext = inT & ~isnew & side_ext & (s >= lo) & (s <= E['top'](t)) & (r < E['rmax'])
    # protected faces inside the sector but near the edge that were left between fill and extension (B2 boundary skin) are included only when enclosed
    cand = fill | ext
    okE = cand[adj[:, 0]] & cand[adj[:, 1]]
    nc, cl = connected_components(sp.coo_matrix((np.ones(okE.sum()), (adj[okE, 0], adj[okE, 1])), shape=(len(F), len(F))), directed=False)
    big = np.bincount(cl[cand]).argmax(); Jm = cand & (cl == big)
    # absorb enclosed islands (faces not in J whose component in the complement is small and touches J)
    okC = ~Jm[adj[:, 0]] & ~Jm[adj[:, 1]]
    ncC, clC = connected_components(sp.coo_matrix((np.ones(okC.sum()), (adj[okC, 0], adj[okC, 1])), shape=(len(F), len(F))), directed=False)
    sizes = np.bincount(clC, weights=(~Jm).astype(float), minlength=ncC); main = sizes.argmax(); touch = np.zeros(len(V), bool); touch[np.unique(F[Jm])] = True
    absorb = ~Jm & (clC != main) & touch[F].any(1) & (sizes[clC] < 200); Jm |= absorb
    # boundary edges shorter than the V4 lower bound (0.25 cm) would force a V4 failure on the new face that uses them:
    # absorb the single outside face across each such edge (recorded), at most 3 rounds
    short_added = []
    eF = b2.face_adjacency_edges
    for _ in range(3):
        bo = Jm[adj[:, 0]] != Jm[adj[:, 1]]; ln = np.linalg.norm(V[eF[:, 0]] - V[eF[:, 1]], axis=1); kk = np.where(bo & (ln < 0.25))[0]
        if not len(kk): break
        out_f = np.where(Jm[adj[kk, 0]], adj[kk, 1], adj[kk, 0]); Jm[out_f] = True; short_added += out_f.tolist()
    idx = np.where(Jm)[0]; sub = F[idx]
    he = {}
    for f in sub:
        for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
    bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd)
    loops = []; seen = set()
    for x0, _ in bnd:
        if x0 in seen: continue
        L = [x0]; seen.add(x0)
        while nxt[L[-1]] != x0: L.append(nxt[L[-1]]); seen.add(L[-1])
        loops.append(L)
    nv = len(np.unique(sub)); ne = len(np.unique(np.sort(np.r_[sub[:, [0, 1]], sub[:, [1, 2]], sub[:, [2, 0]]], 1), axis=0)); chi = nv - ne + len(sub)
    L = max(loops, key=len); bt, bs_, br = tsr(V[L]); X2 = np.c_[bt * K, bs_]
    def crossings(P_):
        m_ = len(P_); out = 0
        for i in range(m_):
            for j in range(i + 2, m_):
                if i == 0 and j == m_ - 1: continue
                p1, p2, p3, p4 = P_[i], P_[(i + 1) % m_], P_[j], P_[(j + 1) % m_]
                d1 = np.cross(p2 - p1, p3 - p1); d2 = np.cross(p2 - p1, p4 - p1); d3 = np.cross(p4 - p3, p1 - p3); d4 = np.cross(p4 - p3, p2 - p3)
                out += int(d1 * d2 < 0 and d3 * d4 < 0)
        return out
    srcfaces = idx[idx < nP]; newfaces = idx[idx >= nP]
    hi_ = np.interp(t[srcfaces], lt, shi) + 0.45 if name == 'posterior' else E['top'](t[srcfaces])
    garm = (s[srcfaces] >= np.interp(t[srcfaces], lt, slo) - 0.45) & (s[srcfaces] <= hi_)
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig_, ax_ = plt.subplots(figsize=(6, 7)); X_ = np.r_[X2, X2[:1]]; ax_.plot(X_[:, 0], X_[:, 1], 'k.-', lw=0.8, ms=3)
    for fi in idx:
        tt_, ss_, _ = tsr(V[F[fi]]); ax_.fill(tt_ * K, ss_, color=('tab:blue' if fi >= nP else ('tab:red' if garm[list(srcfaces).index(fi)] else 'orange')), alpha=0.35, lw=0)
    ax_.set_title('%s J layout (theta*8cm, s): blue B2 fill, red garment remnant, orange skin seam;\nloop crossings %d (layout only)' % (name, crossings(X2)), fontsize=8)
    ax_.set_aspect('equal'); ax_.grid(alpha=.3); fig_.tight_layout(); fig_.savefig(os.path.join(a.out, 'J_%s_layout_topology.png' % name), dpi=90); plt.close(fig_)
    ext_src_idx = P05[srcfaces]                                                                   # F1_working face indices now inside the extension
    labJ[idx] = 6 if name == 'posterior' else 7; sets[name] = dict(J_b2=idx, ext_src=ext_src_idx, b2_new=newfaces)
    rec['ends'][name] = dict(theta_out=E['t_out'], theta_sector_edge=E['t_edge'], theta_in=E['t_in'], rmax=E['rmax'], faces=int(len(idx)), b2_new_faces=int(len(newfaces)),
                             extension_source_faces=int(len(srcfaces)), extension_garment_faces=int(garm.sum()), extension_skin_seam_faces=int((~garm).sum()), extension_source_area_cm2=round(float(src.area_faces[ext_src_idx].sum()), 2), absorbed=int(absorb.sum()), added_for_short_boundary_edges=[int(x) for x in short_added],
                             boundary_loops=len(loops), loop_lengths=[len(l) for l in loops], boundary_edge_cm=np.round([np.linalg.norm(V[L] - V[np.roll(L, -1)], axis=1).min(), np.linalg.norm(V[L] - V[np.roll(L, -1)], axis=1).max()], 3).tolist(), euler=int(chi), layout_crossings=crossings(X2),
                             extension_bounds_cm=np.round(np.r_[V[F[srcfaces]].reshape(-1, 3).min(0), V[F[srcfaces]].reshape(-1, 3).max(0)], 2).tolist() if len(srcfaces) else None,
                             ext_src_faces_sha256=hashlib.sha256(np.sort(ext_src_idx).astype(np.int64).tobytes()).hexdigest())
allext = np.sort(np.r_[sets['posterior']['ext_src'], sets['anterior']['ext_src']]); Pnew = np.setdiff1d(P05, allext)
Fs = np.asarray(src.faces); Vs = np.asarray(src.vertices)
order = np.setdiff1d(np.arange(nP), np.r_[np.where(np.isin(P05, allext))[0]])                       # P05 positions kept, original order
Pnew_ordered = P05[order]
rec['extension_total_source_faces'] = int(len(allext)); rec['removed_region_05Q_faces'] = 879
rec['protected_05R'] = dict(faces=int(len(Pnew_ordered)), face_index_sha256=hashlib.sha256(Pnew_ordered.astype(np.int64).tobytes()).hexdigest(),
                            coord_sha256=hashlib.sha256(np.ascontiguousarray(Vs[Fs[Pnew_ordered]]).astype(np.float64).tobytes()).hexdigest(),
                            note='05Q protected set P (140,081 faces, coord sha 28d2b7ae...) minus the extension faces listed in junction_sets.npz (ext_*_src); original order kept')
rec['fold_edge_line'] = dict(theta=(bins + 1).tolist(), s=np.round(edge, 3).tolist())
np.savez(os.path.join(a.out, 'junction_sets.npz'), J_post_b2=sets['posterior']['J_b2'], J_ant_b2=sets['anterior']['J_b2'], ext_post_src=sets['posterior']['ext_src'], ext_ant_src=sets['anterior']['ext_src'],
         P05R_src_ordered=Pnew_ordered, P05_positions_kept=order)
np.save(os.path.join(a.out, 'junction_face_labels_b2.npy'), labJ)
json.dump(rec, open(os.path.join(a.out, 'junction_selection.json'), 'w'), indent=1); print(json.dumps({k: v for k, v in rec.items() if k not in ('frame', 'fold_edge_line')}, indent=1))
