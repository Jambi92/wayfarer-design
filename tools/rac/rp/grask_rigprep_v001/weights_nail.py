# weights_nail.py RIG.json W0.npz LANDMARKS.json OUTDIR TAG : WN = W0 + nail binding ONLY (order b303b9e §3).
# Selection = the documented distal-cap set (identical to weights_dev.py step 4 / diag_run.py nail-rigidity set), both hands:
#   DIP (thumb IP) -> tip axis u, L3 = |tip - DIP|; candidate = 0.35 L3 < along < L3 + 0.5 cm and radial < 1.6 cm;
#   nail = candidate with dorsal offset (radial . fitted dorsal) > 0.6 x median candidate radius.
# Selected vertices: weight 1.0 on the distal digit bone ({f}_p3_{s}; thumb_p2_{s}), all other bones 0 (that row is already normalised).
# Every non-selected vertex row is copied from W0 unchanged and verified bit-identical (float32 bytes).
# Writes weights_TAG.npz, weights_TAG_log.json (per digit: vertex ids, bone, per-vertex before/after rows of the changed bones),
#        weights_TAG_selection.npz (per-vertex along/radial/dorsal/part diagnostics for the inspection sheets).
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
RJ, W0F, LMF, O, TAG = sys.argv[1:6]; MODE = sys.argv[6] if len(sys.argv) > 6 else 'cap'   # cap = documented set; plate = groove-bounded subset
GROOVE = 0.08                                                        # plate mode: concavity (umbrella Laplacian . outward normal / mean edge) threshold
os.makedirs(O, exist_ok=True)
z = np.load(W0F); W0 = z['W']; assert W0.dtype == np.float32; names = [str(n) for n in z['names']]; col = {n: i for i, n in enumerate(names)}
W = W0.copy()
M = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = M['V'].astype(float); Q = np.asarray(M['Q']); FP = M['FP']
vpart = np.empty(len(V), object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
LM = json.load(open(LMF))['joints']; Jc = lambda k: np.array(LM[k]['position_source_frame_cm'])
FIT5 = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json'))
LOG = dict(tag=TAG, mode=MODE, parent='W0 (weights_v001c.npz: bone heat + midline cleanup)', landmarks=os.path.basename(LMF), digits={},
           selection='distal-phalanx dorsal cap: 0.35 L3 < along < L3 + 0.5 cm on the DIP(thumb IP)->tip axis, radial < 1.6 cm, dorsal offset > 0.6 x median candidate radius; both hands')
SEL = np.zeros(len(V), bool); DIAG = {}
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
deg = np.bincount(E.ravel(), minlength=len(V)); Sx = np.zeros_like(V); np.add.at(Sx, E[:, 0], V[E[:, 1]]); np.add.at(Sx, E[:, 1], V[E[:, 0]]); LAP = Sx / np.maximum(deg, 1)[:, None] - V
fnr = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]]); VN = np.zeros_like(V)
for kk in range(4): np.add.at(VN, Q[:, kk], fnr)
VN /= np.maximum(np.linalg.norm(VN, axis=1), 1e-12)[:, None]; el = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1); ML = np.zeros(len(V)); np.add.at(ML, E[:, 0], el); np.add.at(ML, E[:, 1], el)
CONC = (LAP * VN).sum(1) / (ML / np.maximum(deg, 1))                 # > 0 concave (groove), < 0 convex
if MODE == 'plate':
    LOG['selection'] += ('; PLATE CORRECTION: of that documented set keep only the connected nail-plate region grown (edge adjacency) from the most dorsal vertex at 0.6 L3, '
                         'not crossing groove vertices (concavity > %.2f): removes the proximal/lateral nail-fold skin beyond the groove and the groove ring itself '
                         '(those keep their W0 rows); never adds a vertex outside the documented set' % GROOVE)
for s in 'lr':
    for f in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        jd = '%s_dip_%s' % (f, s) if f != 'thumb' else 'thumb_ip_' + s; d, tp = Jc(jd), Jc('%s_tip_%s' % (f, s)); dor = np.array(FIT5['cx_' + jd]['dorsal'])
        L3 = np.linalg.norm(tp - d); u = (tp - d) / L3; q = V - d; al = q @ u; rad = q - np.outer(al, u); rn = np.linalg.norm(rad, axis=1)
        cand = (al > 0.35 * L3) & (al < L3 + 0.5) & (rn < 1.6); rmed = float(np.median(rn[cand]))
        ix = np.nonzero(cand & ((rad @ dor) > 0.6 * rmed))[0]; doc = ix.copy()
        if MODE == 'plate':
            ok = np.zeros(len(V), bool); ok[ix] = True; ok &= CONC < GROOVE; sc = (q @ dor) - 10 * np.abs(al / L3 - 0.6); R = np.zeros(len(V), bool); R[ix[np.argmax(sc[ix])]] = True
            Ee = E[ok[E[:, 0]] & ok[E[:, 1]]]
            while True:
                nw = R.copy(); nw[Ee[R[Ee[:, 0]], 1]] = True; nw[Ee[R[Ee[:, 1]], 0]] = True
                if (nw == R).all(): break
                R = nw
            ix = np.nonzero(R)[0]; assert np.isin(ix, doc).all()
        bn = '%s_p3_%s' % (f, s) if f != 'thumb' else 'thumb_p2_' + s; b3 = col[bn]
        before = W0[ix]; nzb = sorted(set(np.nonzero(before.max(0) > 0)[0].tolist()) | {b3})
        W[ix] = 0; W[ix, b3] = 1.0; SEL[ix] = True
        parts = {p: int((vpart[ix] == p).sum()) for p in sorted(set(vpart[ix]))}
        key = '%s_%s' % (f, s)
        LOG['digits'][key] = dict(bone=bn, count=int(len(ix)), L3_cm=float(L3), median_candidate_radius_cm=rmed, parts_of_selected=parts,
                                  vertex_ids=ix.tolist(), documented_set_count=int(len(doc)), removed_from_documented_set=np.setdiff1d(doc, ix).tolist(), groove_ring_ids=doc[CONC[doc] >= GROOVE].tolist() if MODE == 'plate' else [], bones_touched=[names[j] for j in nzb],
                                  W0_share_on_distal_bone=dict(min=float(before[:, b3].min()), mean=float(before[:, b3].mean()), max=float(before[:, b3].max())),
                                  max_abs_delta=float(np.abs(W[ix] - before).max()),
                                  per_vertex=[dict(v=int(v), before={names[j]: round(float(before[k, j]), 6) for j in nzb if before[k, j] > 0},
                                                   after={bn: 1.0}) for k, v in enumerate(ix)])
        DIAG[key] = dict(ix=ix, doc=doc, conc=CONC[doc], along=al[ix] / L3, radial=rn[ix], dorsal=(rad[ix] @ dor) / rmed)
# verification: bit identity outside the selection, normalisation / non-negativity inside
rowsame = (W.view(np.uint32) == W0.view(np.uint32)).all(1)
LOG['bit_identity'] = dict(non_selected_vertices=int((~SEL).sum()), non_selected_rows_bit_identical=int(rowsame[~SEL].sum()),
                           all_non_selected_bit_identical=bool(rowsame[~SEL].all()), selected_rows_changed=int((~rowsame[SEL]).sum()),
                           selected_rows_already_equal=int(rowsame[SEL].sum()))
assert rowsame[~SEL].all()
LOG['selected_row_sum_minmax'] = [float(W[SEL].sum(1).min()), float(W[SEL].sum(1).max())]; LOG['negative_weights'] = int((W < 0).sum())
LOG['selected_total'] = int(SEL.sum()); LOG['changed_vertices'] = int((~rowsame).sum())
LOG['weights_sha256'] = hashlib.sha256(np.ascontiguousarray(W).tobytes()).hexdigest()
LOG['baseline_sha256'] = hashlib.sha256(np.ascontiguousarray(W0).tobytes()).hexdigest()
np.savez_compressed(os.path.join(O, 'weights_%s.npz' % TAG), W=W, names=np.array(names))
np.save(os.path.join(O, 'weights_%s_changed_vertex_ids.npy' % TAG), np.nonzero(~rowsame)[0].astype(np.int32))
np.savez(os.path.join(O, 'weights_%s_selection.npz' % TAG), **{k + '_' + a: v[a] for k, v in DIAG.items() for a in v})
json.dump(LOG, open(os.path.join(O, 'weights_%s_log.json' % TAG), 'w'), indent=1)
print(TAG, 'selected', SEL.sum(), 'changed', (~rowsame).sum(), 'bit-identical outside', rowsame[~SEL].all(), 'sha', LOG['weights_sha256'][:12])
for k, d in LOG['digits'].items(): print(k, d['count'], d['parts_of_selected'], 'W0 distal share mean %.2f min %.2f' % (d['W0_share_on_distal_bone']['mean'], d['W0_share_on_distal_bone']['min']))
