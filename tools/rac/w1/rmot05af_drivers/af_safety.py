# RM-OT-05AF s8-s9: (a) merges per region (protected interfaces must have 0 merges); (b) remaining coincident duplicates inside the
# AC1-AC3 sculpt zones on 05AF; (c) non-authoring dry test (in memory only, never saved): apply a sculpt-like random Laplacian
# displacement to every sculpt-zone vertex of 05AF and, as a control, of 05AE; count coincident pairs that separate and
# position-welded boundary edges that appear. Usage: python3 -I af_safety.py AF_DIR
import sys, os, json, numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree
od = sys.argv[1]
rows = json.load(open(os.path.join(od, 'af_groups.json')))
B = np.load(os.path.join(od, 'base_VF.npz')); VB, FB = B['V'], B['F']; A = np.load(os.path.join(od, 'after_VF.npz')); VA, FA = A['V'], A['F']
o2n = np.load(os.path.join(od, 'old_to_new_05AE_to_05AF.npy'))
R = {}
# (a) merges per region / class
merged = {}
for r in rows:
    if r['in_sculpt_zone'] and r['cls'] == 'SAFE_SCULPT_SEAM': merged[r['region']] = merged.get(r['region'], 0) + 1
R['groups_merged_by_region'] = merged
R['groups_merged_in_protected_interfaces'] = sum(1 for r in rows if r['cls'] != 'SAFE_SCULPT_SEAM' and len(set(o2n[r['members']])) < len(r['members']))
R['groups_merged_outside_sculpt_zone'] = sum(1 for r in rows if not r['in_sculpt_zone'] and len(set(o2n[r['members']])) < len(r['members']))
# sculpt-zone vertex mask on 05AE, carried to 05AF
nB = len(VB); zoneB = np.zeros(nB, bool)
# rebuild zone membership: vertices labelled by af_classify regions are only stored per group, so recompute zone from weights
W = np.load(os.path.join(od, 'weights_05AE.npz')); names = [str(x) for x in W['names']]; lab = W['W'].argmax(1)
P = np.load(os.path.join(od, 'protect_05AE.npy')); z = (VB[:, 2] - VB[:, 2].min()) * 100
trunk = lab == names.index('trunk'); limbs = np.isin(lab, [names.index(k) for k in names if k.split('_')[0] in ('upperarm', 'forearm', 'thigh', 'shin')])
prot_groups = [r for r in rows if r['cls'] != 'SAFE_SCULPT_SEAM']
excl = np.zeros(nB, bool)
for r in prot_groups: excl[r['members']] = True
zoneB = ((trunk & (z <= 172.0) & ~(P >= 1)) | limbs) & ~excl
zoneA = np.zeros(len(VA), bool); zoneA[o2n[zoneB]] = True
# (b) remaining coincident duplicates touching the sculpt zone in 05AF
pa = cKDTree(VA).query_pairs(1e-5, output_type='ndarray')
inz = zoneA[pa[:, 0]] | zoneA[pa[:, 1]]
R['coincident_pairs_05AF_total'] = int(len(pa)); R['coincident_pairs_touching_sculpt_zone'] = int(inz.sum())
R['sculpt_zone_vertices_05AF'] = int(zoneA.sum())
listed = [dict(region=r['region'], z=r['z'], members_05AF=[int(x) for x in o2n[r['members']]], note=r.get('note', '')) for r in rows
          if r['cls'] != 'SAFE_SCULPT_SEAM' and r['region'] in ('gluteal', 'pelvis_flank', 'torso_neckbase', 'thigh', 'shin', 'upperarm', 'forearm')]
R['protected_groups_inside_sculpt_regions'] = listed
# (c) dry test
def dry(V, F, zone, seed=0):
    n = len(V); rng = np.random.default_rng(seed)
    E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); Adj = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n)).tocsr(); Adj = ((Adj + Adj.T) > 0).astype(float)
    deg = np.asarray(Adj.sum(1)).ravel(); lap = (Adj @ V) / np.maximum(deg, 1)[:, None] - V                     # per-vertex topological Laplacian
    D = np.zeros_like(V); D[zone] = 0.5 * lap[zone] + rng.normal(0, 2e-4, (int(zone.sum()), 3))               # smooth + 0.2 mm jitter
    V2 = V + D
    p = cKDTree(V).query_pairs(1e-5, output_type='ndarray'); sep = np.linalg.norm(V2[p[:, 0]] - V2[p[:, 1]], axis=1)
    k, iv = np.unique(np.round(V2, 7), axis=0, return_inverse=True); Fw = iv.ravel()[F]
    Ew = np.sort(np.concatenate([Fw[:, [0, 1]], Fw[:, [1, 2]], Fw[:, [2, 0]]]), 1); Ew = Ew[Ew[:, 0] != Ew[:, 1]]; u, c = np.unique(Ew, axis=0, return_counts=True)
    return dict(pairs_separated_gt_0_01mm=int((sep > 1e-5).sum()), position_welded_boundary_edges=int((c == 1).sum()))
R['dry_test_05AF'] = dry(VA, FA, zoneA)
R['dry_test_control_05AE'] = dry(VB, FB, zoneB)
json.dump(R, open(os.path.join(od, 'af_safety.json'), 'w'), indent=1); print(json.dumps({k: v for k, v in R.items() if k != 'protected_groups_inside_sculpt_regions'}, indent=1)); print('listed', listed)
