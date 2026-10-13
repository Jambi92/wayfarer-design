# RM-OT-05S plan visuals: interface chart polygons (boundary topology + source classes) and label arrays for renders of
# source / B2 / R3 with the interface marked. Usage: python3 s_planviz.py --src F1 --b2 B2 --r3 R3 --q05 Q --plan DIR
import argparse, json, os, sys, numpy as np, trimesh
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import s_lib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--b2'); ap.add_argument('--r3'); ap.add_argument('--q05'); ap.add_argument('--plan'); a = ap.parse_args()
fr = s_lib.Frame(os.path.join(a.q05, 'plan/patch_selection.json')); b2 = trimesh.load(a.b2, process=False); V = np.asarray(b2.vertices); F = np.asarray(b2.faces)
S = np.load(os.path.join(a.plan, 'interface_sets.npz'), allow_pickle=True); P05 = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz'))['P']; nP = len(P05)
rep = {}
for name, key, ck in (('posterior', 'I_post_b2', 'class_post'), ('anterior', 'I_ant_b2', 'class_ant')):
    D = dict(np.load(os.path.join(a.plan, 'design_%s.npz' % name))); I = S[key]; sub = F[I]; he = {}
    for f in sub:
        for i in range(3): he[(f[i], f[(i + 1) % 3])] = True
    bnd = [(x, y) for (x, y) in he if (y, x) not in he]; nxt = dict(bnd); loop = [bnd[0][0]]
    while nxt[loop[-1]] != loop[0]: loop.append(nxt[loop[-1]])
    cc = {}; ch, dist = s_lib.chart_points(fr, V, F, V[loop], D, cc); R0 = 9.0; X2 = np.c_[np.radians(ch[:, 0]) * R0, ch[:, 1]]
    cr = s_lib.simple_polygon_crossings(X2); rep[name] = dict(loop_vertices=len(loop), chart_crossings=cr, max_projection_cm=round(float(dist.max()), 3))
    fig, ax = plt.subplots(figsize=(9, 6)); cls = S[ck]; srcI = I[I < nP]; col = dict(arm_skin='orange', garment_band='red', fold_edge_or_trunk='purple', fused_fold_ambiguous='purple')
    fc, _ = s_lib.chart_points(fr, V, F, V[F[I]].mean(1), D, cc)
    for j, f in enumerate(I):
        c = 'tab:blue' if f >= nP else col[cls[list(srcI).index(f)]]
        ax.plot(np.radians(fc[j, 0]) * R0, fc[j, 1], 's', color=c, ms=4, alpha=.6)
    XX = np.r_[X2, X2[:1]]; ax.plot(XX[:, 0], XX[:, 1], 'k.-', lw=.8, ms=3)
    ax.set_title('%s interface chart (theta*9cm, arclength from A): blue B2 fill, orange arm skin, red garment band, purple fold edge/fused;\nboundary loop %d vertices, chart crossings %d' % (name, len(loop), cr), fontsize=8)
    ax.grid(alpha=.3); ax.set_aspect('equal'); plt.tight_layout(); plt.savefig(os.path.join(a.plan, 'I_%s_chart_topology.png' % name), dpi=85); plt.close()
# label arrays: B2 (6/7 interface), source (interface source faces + 05Q-removed faces in the zones), R3 (nearest B2 face)
labB2 = np.load(os.path.join(a.plan, 'interface_face_labels_b2.npy'))
src = trimesh.load(a.src, process=False); Vs = np.asarray(src.vertices); Fs = np.asarray(src.faces); labS = np.zeros(len(Fs), np.int8)
labS[S['src_post']] = 6; labS[S['src_ant']] = 7
Z = np.load(os.path.join(a.q05, 'plan/patch_face_sets.npz')); Rq = np.union1d(Z['G'], Z['S']); tq, _, _ = fr.tsr(Vs[Fs[Rq]].mean(1))
labS[Rq[(tq < -80) | (tq > 74)]] = np.where(tq[(tq < -80) | (tq > 74)] < 0, 6, 7)
np.save(os.path.join(a.plan, 'interface_face_labels_source.npy'), labS)
r3 = trimesh.load(a.r3, process=False); cb = V[F].mean(1); _, nn = cKDTree(cb).query(np.asarray(r3.vertices)[np.asarray(r3.faces)].mean(1))
np.save(os.path.join(a.plan, 'interface_face_labels_r3.npy'), labB2[nn])
json.dump(rep, open(os.path.join(a.plan, 'interface_chart_check.json'), 'w'), indent=1); print(rep)
