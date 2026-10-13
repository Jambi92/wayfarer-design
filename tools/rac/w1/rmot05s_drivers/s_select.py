# RM-OT-05S interface selection on the B2 baseline (dry run: nothing is edited).
# Every baseline face near the interface gets chart coordinates (theta, l - lA(theta)) by projecting its centroid onto the
# nearest design column (s_design.py). The interface region I (per side) = faces with theta inside the zone and the
# normalized position t = (l - lA) / (lB - lA) in [0, 1], as one connected disk (enclosed islands absorbed).
# Source faces in I are classified by profile position: arm skin (below the band ledge), garment band (ledge .. lip
# peak / band top), fold edge or fused/ambiguous (posterior: beyond the lip peak; anterior: the slope above s_led + 4).
# Usage: python3 s_select.py --b2 B2.obj --q05 <05Q evidence> --design DIR --out DIR
import argparse, hashlib, json, os, sys, numpy as np, trimesh
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import s_lib, s_design
ap = argparse.ArgumentParser(); ap.add_argument('--b2'); ap.add_argument('--q05'); ap.add_argument('--design'); ap.add_argument('--src'); ap.add_argument('--out'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
fr = s_lib.Frame(os.path.join(a.q05, 'plan/patch_selection.json')); m = trimesh.load(a.b2, process=False); V = np.asarray(m.vertices); F = np.asarray(m.faces)
P05 = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz'))['P']; nP = len(P05); src = trimesh.load(a.src, process=False); Vs = np.asarray(src.vertices); Fs = np.asarray(src.faces)
C = V[F].mean(1); tC, sC, rC = fr.tsr(C); rec = dict(baseline_sha256=hashlib.sha256(open(a.b2, 'rb').read()).hexdigest(), sides={})
lab = np.zeros(len(F), np.int8); sets = {}
for name in ('posterior', 'anterior'):
    D = dict(np.load(os.path.join(a.design, 'design_%s.npz' % name))); th = D['theta']; z = s_design.ZONES[name]
    lo, hi = th.min(), th.max(); cand = np.where((tC >= lo) & (tC <= hi) & (rC < 24) & (np.abs(sC) < 20))[0]
    tt = np.full(len(F), np.nan); ll = np.full(len(F), np.nan)
    cols = {}
    for f in cand:
        k = int(np.clip(np.round((tC[f] - lo) / 0.25), 0, len(th) - 1))
        if k not in cols: cols[k] = s_lib.profile(fr, V, F, th[k], (8.0, D['s_led'][k] - 4.0))[0]
        P = cols[k]; L = s_lib.arclen(P); rad, _ = fr.dirs(th[k]); q = np.array([(C[f] - fr.O) @ rad, (C[f] - fr.O) @ fr.d])
        l, dist = s_lib.project(P, L, q)
        if dist < 0.6: ll[f] = l - D['lA'][k]; tt[f] = (l - D['lA'][k]) / (D['lB'][k] - D['lA'][k])
    inI = ~np.isnan(tt) & (tt >= 0) & (tt <= 1)
    adj = m.face_adjacency; ok = inI[adj[:, 0]] & inI[adj[:, 1]]
    nc, cl = connected_components(sp.coo_matrix((np.ones(ok.sum()), (adj[ok, 0], adj[ok, 1])), shape=(len(F), len(F))), directed=False)
    big = np.bincount(cl[inI]).argmax(); I = inI & (cl == big)
    okC = ~I[adj[:, 0]] & ~I[adj[:, 1]]; ncC, clC = connected_components(sp.coo_matrix((np.ones(okC.sum()), (adj[okC, 0], adj[okC, 1])), shape=(len(F), len(F))), directed=False)
    sizes = np.bincount(clC, weights=(~I).astype(float), minlength=ncC); main = sizes.argmax(); tv = np.zeros(len(V), bool); tv[np.unique(F[I])] = True
    absorb = ~I & (clC != main) & tv[F].any(1) & (sizes[clC] < 300); I |= absorb
    idx = np.where(I)[0]; sub = F[idx]; he = {}
    for f in sub:
        for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
    bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); loops = []; seen = set()
    for x0, _ in bnd:
        if x0 in seen: continue
        Lp = [x0]; seen.add(x0)
        while nxt[Lp[-1]] != x0: Lp.append(nxt[Lp[-1]]); seen.add(Lp[-1])
        loops.append(Lp)
    nv = len(np.unique(sub)); ne = len(np.unique(np.sort(np.r_[sub[:, [0, 1]], sub[:, [1, 2]], sub[:, [2, 0]]], 1), axis=0))
    # classification of source faces in I
    srcf = idx[idx < nP]; newf = idx[idx >= nP]
    kk = np.clip(np.round((tC[srcf] - lo) / 0.25).astype(int), 0, len(th) - 1); sled = D['s_led'][kk]
    cls = np.where(sC[srcf] < sled - 0.3, 'arm_skin', 'garment_band')
    if name == 'posterior':
        # beyond the lip peak along the column = fold edge / trunk side (t above the arclength of the max-s point after the ledge)
        tpk = []
        for j, f in enumerate(srcf):
            P = cols.get(kk[j]);
            if P is None: P = s_lib.profile(fr, V, F, th[kk[j]], (8.0, D['s_led'][kk[j]] - 4.0))[0]; cols[kk[j]] = P
            L = s_lib.arclen(P); iL = np.argmax(P[:, 1] >= D['s_led'][kk[j]])
            # first local max of s after the ledge
            sm = -1e9; ip = iL
            for i in range(iL, len(P)):
                if P[i, 1] > sm: sm = P[i, 1]; ip = i
                if sm - P[i, 1] > 0.3: break
            tpk.append(L[ip] - D['lA'][kk[j]])
        cls = np.where((cls == 'garment_band') & (ll[srcf] > np.array(tpk) + 0.2), 'fold_edge_or_trunk', cls)
    else:
        cls = np.where((cls == 'garment_band') & (sC[srcf] > sled + 4.0), 'fused_fold_ambiguous', cls)
    counts = {c: int((cls == c).sum()) for c in np.unique(cls)}
    lab[idx] = 6 if name == 'posterior' else 7
    sets[name] = dict(I_b2=idx, src_in_I=P05[srcf], src_class=cls)
    rec['sides'][name] = dict(zone=z, faces=int(len(idx)), b2_new_faces=int(len(newf)), source_faces=int(len(srcf)), source_area_cm2=round(float(trimesh.triangles.area(V[F[srcf]]).sum()), 2),
                              source_classes=counts, absorbed=int(absorb.sum()), boundary_loops=len(loops), loop_lengths=[len(l) for l in loops], euler=int(nv - ne + len(sub)),
                              bounds_cm=np.round(np.r_[V[sub].reshape(-1, 3).min(0), V[sub].reshape(-1, 3).max(0)], 2).tolist(),
                              src_faces_sha256=hashlib.sha256(np.sort(P05[srcf]).astype(np.int64).tobytes()).hexdigest())
    np.save(os.path.join(a.out, 'chart_%s_t.npy' % name), tt); np.save(os.path.join(a.out, 'chart_%s_l.npy' % name), ll)
allsrc = np.r_[sets['posterior']['src_in_I'], sets['anterior']['src_in_I']]
keep_pos = np.where(~np.isin(P05, allsrc))[0]; P05S = P05[keep_pos]
rec['protected_05S'] = dict(faces=int(len(P05S)), face_index_sha256=hashlib.sha256(P05S.astype(np.int64).tobytes()).hexdigest(),
                            coord_sha256=hashlib.sha256(np.ascontiguousarray(Vs[Fs[P05S]]).astype(np.float64).tobytes()).hexdigest(),
                            newly_inside_from_05Q_P=int(len(allsrc)), note='05Q P (140,081; coord sha 28d2b7ae...) minus the source faces inside I; original order kept')
np.savez(os.path.join(a.out, 'interface_sets.npz'), I_post_b2=sets['posterior']['I_b2'], I_ant_b2=sets['anterior']['I_b2'], src_post=sets['posterior']['src_in_I'], src_ant=sets['anterior']['src_in_I'],
         class_post=sets['posterior']['src_class'], class_ant=sets['anterior']['src_class'], P05S_src_ordered=P05S, P05_positions_kept=keep_pos)
np.save(os.path.join(a.out, 'interface_face_labels_b2.npy'), lab)
json.dump(rec, open(os.path.join(a.out, 'interface_selection.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
