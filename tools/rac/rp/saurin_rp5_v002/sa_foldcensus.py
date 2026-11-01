# sa_foldcensus.py CAGE.npz DESIGN.pkl OUT.json : folded / concave quad census (RP5 targeted revision internal audit; not part of the T-4 definition
#   used so far): per quad (a) INVERTED = quad normal (diagonal cross) opposite to the working-source normal under its centroid, (b) CONCAVE = min signed
#   corner sine w.r.t. the quad normal < 0.05 (dart / bow-tie), (c) cage-vertex sheet disagreement (vertex normal vs source face normal < 0.2); by region
#   and by authored coarse structure (single-row web, 2:1 row, orbit fan, vault patch ...). Tip caps and the accepted tail module reported separately.
import sys, os, json, pickle, collections, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OUT = sys.argv[1:4]; z = np.load(CG); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); ql = z['qlab'].astype(str); qc = z['qcoarse']
d = pickle.load(open(DS, 'rb')); nm = d['name']; DQ = np.array(d['Q'])
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); P4 = V[Q]
# HOST-AWARE census (order 50ef121 §1-§2). Reference frame of a quad = its OWN source correspondence: the area-weighted normals of the barycentric host
# faces of its 4 corners (never the nearest face to an off-surface centroid -> no classification against the opposite wall of a web slot). Corners are
# projected into that tangent plane (e1, e2 from the first edge). There:
#   BOW-TIE  = opposite edges cross (true segment-intersection test, tol 1e-9 relative);
#   INVERTED = simple polygon whose signed area is negative w.r.t. the host normal (orientation reversed against its own source patch);
#   CONCAVE  = simple, positively oriented polygon with a reflex corner (signed turn < -0.02, i.e. a corner beyond ~181 deg).
FA = igl.doublearea(G.V, G.F); nref = (FN[z['tri'][Q]] * FA[z['tri'][Q]][..., None]).sum(1); nref /= np.linalg.norm(nref, axis=1, keepdims=True) + 1e-12
c0 = P4.mean(1); e1 = P4[:, 1] - P4[:, 0]; e1 -= (e1 * nref).sum(1)[:, None] * nref; e1 /= np.linalg.norm(e1, axis=1, keepdims=True) + 1e-12; e2 = np.cross(nref, e1)
xy = np.stack([((P4 - c0[:, None]) * e1[:, None]).sum(2), ((P4 - c0[:, None]) * e2[:, None]).sum(2)], 2)
def cr(a_, b_): return a_[..., 0] * b_[..., 1] - a_[..., 1] * b_[..., 0]
def segx(p1, p2, p3, p4):
    d1 = cr(p4 - p3, p1 - p3); d2 = cr(p4 - p3, p2 - p3); d3 = cr(p2 - p1, p3 - p1); d4 = cr(p2 - p1, p4 - p1); return (d1 * d2 < 0) & (d3 * d4 < 0)
bowx = segx(xy[:, 0], xy[:, 1], xy[:, 2], xy[:, 3]) | segx(xy[:, 1], xy[:, 2], xy[:, 3], xy[:, 0])
area = 0.5 * sum(cr(xy[:, k], xy[:, (k + 1) % 4]) for k in range(4)); scale = (np.linalg.norm(np.diff(np.r_['1', xy, xy[:, :1]], axis=1), axis=2) ** 2).mean(1)
inv = ~bowx & (area < -1e-6 * scale)
turn = np.stack([cr(xy[:, k] - xy[:, (k - 1) % 4], xy[:, (k + 1) % 4] - xy[:, k]) / (np.linalg.norm(xy[:, k] - xy[:, (k - 1) % 4], axis=1) * np.linalg.norm(xy[:, (k + 1) % 4] - xy[:, k], axis=1) + 1e-12) for k in range(4)], 1)
bow = bowx; conc = ~bowx & ~inv & (turn.min(1) < -0.02)
T = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; NV_ = np.nan_to_num(igl.per_vertex_normals(V, T)); vdis = (FN[z['tri']] * NV_).sum(1) < 0.2
TIP = np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']); TAIL = ql == 'tail'
def struct(q):
    if q < 0 or q >= len(DQ): return 'revision patch (vault / nostril / loop)'
    names = [nm[i] for i in DQ[q]]; l = str(d['qlab'][q])
    if any('_wr2_x' in x for x in names): return 'wrist 2:1 transition'
    if any('_an2_x' in x for x in names): return 'ankle 2:1 transition'
    if any('_pt_x' in x for x in names): return 'palm 2:1 row'
    if any('_ft_x' in x for x in names): return 'forefoot 2:1 row'
    if l in ('finger_web', 'toe_web'): return 'single-row web (' + l + ')'
    if l == 'orbit': return 'orbit fan'
    return l
m = ~TIP & ~TAIL
CRIT = np.isin(ql, ['shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle', 'neck', 'finger', 'thumb', 'toe', 'finger_web', 'toe_web', 'palm', 'forefoot', 'foot'])
res = dict(quads=int(len(Q)), inverted_vs_source=int(inv.sum()), inverted_non_tip=int((inv & m).sum()), bowtie_non_tip=int((bow & m).sum()),
           concave_non_tip=int((conc & m).sum()), concave_deformation_critical=int((conc & m & CRIT).sum()),
           concave_or_bowtie_non_tip=int(((conc | bow) & m).sum()),
           vertex_sheet_disagreement=int(vdis.sum()), tip_caps=dict(inverted=int((inv & TIP).sum()), concave=int((conc & TIP).sum()), bowtie=int((bow & TIP).sum())),
           accepted_tail_module=dict(inverted=int((inv & TAIL).sum()), concave=int((conc & TAIL).sum()), bowtie=int((bow & TAIL).sum())),
           by_region_concave={k: int(v) for k, v in collections.Counter(ql[conc & m]).most_common()}, by_region_bowtie={k: int(v) for k, v in collections.Counter(ql[bow & m]).most_common()}, by_region_inverted={k: int(v) for k, v in collections.Counter(ql[inv & m]).most_common()},
           by_structure_concave={k: int(v) for k, v in collections.Counter(struct(int(q)) for q in qc[conc & m]).most_common()},
           by_structure_inverted={k: int(v) for k, v in collections.Counter(struct(int(q)) for q in qc[inv & m]).most_common()})
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(res, indent=1)[:1500])
