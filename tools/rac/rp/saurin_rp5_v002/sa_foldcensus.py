# sa_foldcensus.py CAGE.npz DESIGN.pkl OUT.json : folded / concave quad census (RP5 targeted revision internal audit; not part of the T-4 definition
#   used so far): per quad (a) INVERTED = quad normal (diagonal cross) opposite to the working-source normal under its centroid, (b) CONCAVE = min signed
#   corner sine w.r.t. the quad normal < 0.05 (dart / bow-tie), (c) cage-vertex sheet disagreement (vertex normal vs source face normal < 0.2); by region
#   and by authored coarse structure (single-row web, 2:1 row, orbit fan, vault patch ...). Tip caps and the accepted tail module reported separately.
import sys, os, json, pickle, collections, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OUT = sys.argv[1:4]; z = np.load(CG); Q = z['Q']; V = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); ql = z['qlab'].astype(str); qc = z['qcoarse']
d = pickle.load(open(DS, 'rb')); nm = d['name']; DQ = np.array(d['Q'])
FN = igl.per_face_normals(G.V, G.F, np.array([0, 0, 1.0])); P4 = V[Q]
# reference normal = the working-source normal at the quad's OWN corners (their barycentric host faces), never the nearest face to an off-surface centroid
# (in a narrow web slot the centroid can be nearest to the opposite wall)
nref = FN[z['tri'][Q]].sum(1); nref /= np.linalg.norm(nref, axis=1, keepdims=True) + 1e-12
tri_n = [np.cross(P4[:, b] - P4[:, a], P4[:, c] - P4[:, a]) for a, b, c in ((0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3))]
inv = np.stack([(t * nref).sum(1) < 0 for t in tri_n], 1).sum(1) >= 3                # inverted: at least 3 of the 4 corner triangles face against the surface
u1 = np.roll(P4, 1, 1) - P4; u2 = np.roll(P4, -1, 1) - P4
sgall = (np.cross(u2, u1) * nref[:, None]).sum(2) / (np.linalg.norm(u1, axis=2) * np.linalg.norm(u2, axis=2) + 1e-12); nneg = (sgall < 0.05).sum(1)
nneg = np.where(inv, 0, nneg)                                                         # (an inverted quad is counted once, as inverted)
bow = nneg >= 2; conc = nneg == 1                                                   # bow-tie (self-crossing: >= 2 reflex / degenerate corners) vs dart (1)
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
