# sa_audit_renders.py CAGE.npz DESIGN.pkl OUTDIR : visual verification of the fold census (order 50ef121 §3).
#   1. classifies every quad with BOTH methods:
#        OLD  = nearest source face to the quad centroid for inversion + one diagonal-derived quad normal for concavity / bow-tie (pre-50ef121 census);
#        NEW  = host-aware census of sa_foldcensus.py (corner host faces -> tangent plane; true segment-crossing bow-tie; signed turns);
#      -> census_method_comparison.json : per structure, counts per class for both methods and the class-change matrix (old false positives listed).
#   2. renders close-ups of every audited structure (finger webs, toe webs, palm / forefoot 2:1 rows, thumb base, orbit fans, wrist / ankle 2:1 rings),
#      one per side, from OUTSIDE (along the mean source normal) and from INSIDE (opposite direction; back faces drawn), with overlays:
#      quad fill = NEW class (grey ok, red inverted, magenta bow-tie, orange concave), hatched outline = OLD flag, quad IDs on flagged / changed quads
#      and on a deterministic sample (every 37th quad), source host triangles (corner hosts) of the sampled quads in blue, orientation arrows (0 -> 1 edge).
#   3. a deterministic sample of class-changed quads per structure is rendered individually (zoomed) -> sample_<structure>_<n>.png.
import sys, os, json, pickle, collections, numpy as np, igl, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OD = sys.argv[1:4]; os.makedirs(OD, exist_ok=True)
z = np.load(CG); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); ql = z['qlab'].astype(str); qc = z['qcoarse']; tri = z['tri']
d = pickle.load(open(DS, 'rb')); nm = d['name']; DQ = np.array(d['Q'])
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); FA = igl.doublearea(G.V, G.F); P4 = V[Q]; nq = len(Q)
def cr(a_, b_): return a_[..., 0] * b_[..., 1] - a_[..., 1] * b_[..., 0]
def segx(p1, p2, p3, p4):
    d1 = cr(p4 - p3, p1 - p3); d2 = cr(p4 - p3, p2 - p3); d3 = cr(p2 - p1, p3 - p1); d4 = cr(p2 - p1, p4 - p1); return (d1 * d2 < 0) & (d3 * d4 < 0)
# NEW (host-aware)
nref = (FN[tri[Q]] * FA[tri[Q]][..., None]).sum(1); nref /= np.linalg.norm(nref, axis=1, keepdims=True) + 1e-12
c0 = P4.mean(1); e1 = P4[:, 1] - P4[:, 0]; e1 -= (e1 * nref).sum(1)[:, None] * nref; e1 /= np.linalg.norm(e1, axis=1, keepdims=True) + 1e-12; e2 = np.cross(nref, e1)
xy = np.stack([((P4 - c0[:, None]) * e1[:, None]).sum(2), ((P4 - c0[:, None]) * e2[:, None]).sum(2)], 2)
bow = segx(xy[:, 0], xy[:, 1], xy[:, 2], xy[:, 3]) | segx(xy[:, 1], xy[:, 2], xy[:, 3], xy[:, 0])
area = 0.5 * sum(cr(xy[:, k], xy[:, (k + 1) % 4]) for k in range(4)); sc = (np.linalg.norm(np.diff(np.r_['1', xy, xy[:, :1]], axis=1), axis=2) ** 2).mean(1)
inv = ~bow & (area < -1e-6 * sc)
turn = np.stack([cr(xy[:, k] - xy[:, (k - 1) % 4], xy[:, (k + 1) % 4] - xy[:, k]) / (np.linalg.norm(xy[:, k] - xy[:, (k - 1) % 4], axis=1) * np.linalg.norm(xy[:, (k + 1) % 4] - xy[:, k], axis=1) + 1e-12) for k in range(4)], 1)
conc = ~bow & ~inv & (turn.min(1) < -0.02)
NEW = np.where(inv, 'inverted', np.where(bow, 'bow-tie', np.where(conc, 'concave', 'ok')))
# OLD (nearest face to centroid + diagonal normal)
_, fi_c, _ = igl.point_mesh_squared_distance(c0, G.V, G.F); nd = np.cross(P4[:, 2] - P4[:, 0], P4[:, 3] - P4[:, 1]); nd /= np.linalg.norm(nd, axis=1, keepdims=True) + 1e-12
oinv = (nd * FN[fi_c]).sum(1) < 0
u1 = P4 - np.roll(P4, 1, 1); u2 = np.roll(P4, -1, 1) - P4; osin = (np.cross(u1, u2) * nd[:, None]).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12)
oconc = ~oinv & (osin.min(1) < 0.05)
OLD = np.where(oinv, 'inverted', np.where(oconc, 'concave/bow-tie', 'ok'))
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']); TAIL = ql == 'tail'; m = ~TIP & ~TAIL
def struct(q):
    q = int(q)
    if q < 0 or q >= len(DQ): return 'revision patch'
    names = [nm[i] for i in DQ[q]]; l = str(d['qlab'][q])
    for t, lab in (('_wr2_x', 'wrist 2:1 ring'), ('_an2_x', 'ankle 2:1 ring'), ('_pt_x', 'palm 2:1 row'), ('_ft_x', 'forefoot 2:1 row')):
        if any(t in x for x in names): return lab
    if l == 'finger_web': return 'finger web'
    if l == 'toe_web': return 'toe web'
    if l == 'orbit': return 'orbit fan'
    if l == 'thumb' and any(('H0b' in x or 'Wr_' in x or 'H0_' in x) for x in names): return 'thumb base'
    return l
ST = np.array([struct(q) for q in qc])
AUD = ['finger web', 'toe web', 'palm 2:1 row', 'forefoot 2:1 row', 'thumb base', 'orbit fan', 'wrist 2:1 ring', 'ankle 2:1 ring']
cmp = {}
for s in AUD + ['all non-tip']:
    mm = m & ((ST == s) if s != 'all non-tip' else True)
    ch = collections.Counter(zip(OLD[mm], NEW[mm]))
    cmp[s] = dict(quads=int(mm.sum()), new=dict(collections.Counter(NEW[mm])), old=dict(collections.Counter(OLD[mm])),
                  changed={'%s -> %s' % k: int(v) for k, v in ch.items() if k[0] != k[1] and not (k[0] == 'concave/bow-tie' and k[1] in ('concave', 'bow-tie'))},
                  old_false_positives=int(((OLD[mm] != 'ok') & (NEW[mm] == 'ok')).sum()), old_false_negatives=int(((OLD[mm] == 'ok') & (NEW[mm] != 'ok')).sum()))
json.dump(dict(cage=os.path.basename(CG), method=dict(new='host-aware: reference normal = area-weighted normals of the 4 corners\' barycentric host faces; corners projected to that tangent plane; '
               'bow-tie = opposite edges cross (segment test); inverted = simple polygon with signed area < -1e-6 * mean edge^2; concave = simple positive polygon with a signed turn < -0.02 (corner > ~181 deg)',
               old='inverted = diagonal-cross quad normal opposite to the normal of the source face nearest to the quad centroid; concave/bow-tie = min signed corner sine about that normal < 0.05'),
               tolerances=dict(area_rel=1e-6, turn=-0.02), structures=cmp), open(OD + '/census_method_comparison.json', 'w'), indent=1)
COL = {'ok': '#d9d9d9', 'inverted': '#e31a1c', 'bow-tie': '#c51b8a', 'concave': '#fd8d3c'}
def render(sel, centre, nrm, r, title, out, ids_all=False):
    nrm = nrm / np.linalg.norm(nrm); up = np.array([0, 0, 1.0]) if abs(nrm[2]) < 0.9 else np.array([0, 1.0, 0]); a1 = np.cross(up, nrm); a1 /= np.linalg.norm(a1); a2 = np.cross(nrm, a1)
    fig, axs = plt.subplots(1, 2, figsize=(16, 8.4))
    for ax, sgn, lab in ((axs[0], 1.0, 'outside (view along -n)'), (axs[1], -1.0, 'inside (view along +n, back faces)')):
        vdir = -sgn * nrm; b1 = a1 * sgn
        P = V[Q[sel]]; dep = ((P.mean(1) - centre) @ vdir); o = np.argsort(dep)[::-1]; s_ = sel[o]; P = P[o]
        XY = np.stack([(P - centre) @ b1, (P - centre) @ a2], 2)
        ax.add_collection(PolyCollection(XY, facecolors=[COL[NEW[q]] for q in s_], edgecolors='#444444', linewidths=0.25, alpha=0.95))
        oldf = np.array([OLD[q] != 'ok' for q in s_])
        if oldf.any(): ax.add_collection(PolyCollection(XY[oldf], facecolors='none', edgecolors='#1f78b4', linewidths=1.0, hatch='////'))
        # sample + flagged ids, host triangles, orientation arrows
        smp = [i for i, q in enumerate(s_) if q % 37 == 0 or NEW[q] != 'ok' or OLD[q] != 'ok' or ids_all]
        for i in smp[:400]:
            q = s_[i]; cxy = XY[i].mean(0); ax.text(cxy[0], cxy[1], str(q), fontsize=4.5, ha='center', va='center', color='k')
            a_, b_ = XY[i, 0], XY[i, 1]; ax.annotate('', xy=a_ + 0.6 * (b_ - a_), xytext=a_, arrowprops=dict(arrowstyle='->', lw=0.5, color='#006d2c'))
            for k in range(4):
                t = G.V[G.F[tri[Q[q, k]]]]; txy = np.stack([(t - centre) @ b1, (t - centre) @ a2], 1)
                ax.add_collection(LineCollection([txy[[0, 1]], txy[[1, 2]], txy[[2, 0]]], colors='#3182bd', linewidths=0.35))
        ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_aspect('equal'); ax.set_title(lab, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    cnt = {str(k): int(v) for k, v in collections.Counter(NEW[sel]).items()}; oc = {str(k): int(v) for k, v in collections.Counter(OLD[sel]).items()}
    fig.suptitle('%s   |   NEW (fill): %s   |   OLD flag (blue hatch): %s   |   ids: flagged + every 37th, blue = corner host triangles, green arrow = edge 0->1' % (title, cnt, oc), fontsize=8)
    plt.tight_layout(); plt.savefig(out, dpi=110); plt.close(fig)
TN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0]))
index = []
for s in AUD:
    qs = np.nonzero((ST == s) & m)[0]
    if not len(qs): continue
    # split into clusters (sides / digits) by the coarse structure connectivity
    cen = V[Q[qs]].mean(1); from scipy.cluster.hierarchy import fcluster, linkage
    labs = fcluster(linkage(cen, 'single'), t=1.2, criterion='distance') if len(qs) > 1 else np.array([1])
    for ci in np.unique(labs):
        cq = qs[labs == ci]; centre = V[Q[cq]].mean((0, 1)); nr = (nref[cq]).sum(0); r = max(0.6, np.linalg.norm(V[Q[cq]].reshape(-1, 3) - centre, axis=1).max() * 1.15)
        allq = np.nonzero(np.linalg.norm(c0 - centre, axis=1) < r)[0]
        fn = '%s_%02d.png' % (s.replace(' ', '_').replace(':', ''), ci); render(allq, centre, nr, r, '%s cluster %d (%d structure quads) centre %s' % (s, ci, len(cq), np.round(centre, 1).tolist()), OD + '/' + fn)
        index.append(dict(structure=s, cluster=int(ci), file=fn, quads=int(len(cq)), new={str(k): int(v) for k, v in collections.Counter(NEW[cq]).items()}, old={str(k): int(v) for k, v in collections.Counter(OLD[cq]).items()}))
    # deterministic sample of class-changed quads (zoomed)
    chg = qs[(OLD[qs] != 'ok') != (NEW[qs] != 'ok')]
    for j, q in enumerate(chg[:: max(1, len(chg) // 6)][:6]):
        centre = c0[q]; r = 3.0 * np.linalg.norm(P4[q] - centre, axis=1).max(); allq = np.nonzero(np.linalg.norm(c0 - centre, axis=1) < r)[0]
        fn = 'sample_%s_%d.png' % (s.replace(' ', '_').replace(':', ''), j); render(allq, centre, nref[q], r, '%s sample quad %d: OLD %s -> NEW %s' % (s, q, OLD[q], NEW[q]), OD + '/' + fn, ids_all=True)
        index.append(dict(structure=s, sample_quad=int(q), old=str(OLD[q]), new=str(NEW[q]), file=fn))
json.dump(index, open(OD + '/render_index.json', 'w'), indent=1); print(json.dumps(cmp['all non-tip'], indent=1)); print('renders', len(index))
