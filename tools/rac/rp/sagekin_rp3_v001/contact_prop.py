# contact_prop.py OUT.json ID FAM_CAND FAM_LOOPS NATIVE NATIVE_LOOPS BASE_CAND BASE_LOOPS : order c6c7940 §17 -- contact gate for a propagation
# (no topology change). Every rest self-intersection pair of the family realization (audit.py, mathutils BVH) is classified:
#   source       -- within 1.0 cm (pair centroid) of a self-intersection pair of the accepted native hm08 source (inherited from the source);
#   family       -- the same face pair, or a pair within 0.5 cm centroid on faces sharing a vertex with it, exists in the frozen family base fit of the
#                   same configuration class (Marchfolk v005), i.e. a known family-base behaviour at that place;
#   new          -- neither: a new contact defect attributable to propagation (stop condition if in hand / foot / toe / web / groin).
import sys, json, numpy as np
from scipy.spatial import cKDTree
OUT, ID, fc, fl, nc, nl, bc, bl = sys.argv[1:9]
F = np.load(fc); Lf = np.load(fl, allow_pickle=True); N = np.load(nc); Ln = np.load(nl, allow_pickle=True); B = np.load(bc); Lb = np.load(bl, allow_pickle=True)
def cen(V, Q, S): return 0.5 * (V[Q[S[:, 0]]].mean(1) + V[Q[S[:, 1]]].mean(1)) if len(S) else np.zeros((0, 3))
Sf, Sn, Sb = Lf['SI'], Ln['SI'], Lb['SI']; Cf = cen(F['V'], F['Q'], Sf); Cn = cen(N['V'], N['Q'], Sn); Cb = cen(F['V'], F['Q'], Sb)   # family-base pairs placed on THIS realization's geometry
zf = Lf['zone']; Qf = np.asarray(F['Q'])
pairs_b = {tuple(sorted(map(int, p))) for p in Sb}
tn = cKDTree(Cn) if len(Cn) else None; tb = cKDTree(Cb) if len(Cb) else None
cls = []
for i, p in enumerate(Sf):
    c = Cf[i]; k = tuple(sorted(map(int, p)))
    if tn is not None and tn.query(c)[0] <= 1.0: cls.append('source')
    elif k in pairs_b or (tb is not None and tb.query(c)[0] <= 0.5): cls.append('family')
    else: cls.append('new')
cls = np.array(cls); zone = lambda i: str(zf[Qf[int(Sf[i][0]), 0]])
out = dict(id=ID, family_pairs=int(len(Sf)), native_pairs=int(len(Sn)), family_base_same_class_pairs=int(len(Sb)), face_count_ratio=round(len(Qf) / len(N['Q']), 3),
           classes={c: int((cls == c).sum()) for c in ('source', 'family', 'new')}, by_zone={}, new_pairs=[])
for i in range(len(Sf)):
    z = zone(i); out['by_zone'].setdefault(z, {}).setdefault(cls[i], 0); out['by_zone'][z][cls[i]] += 1
    if cls[i] == 'new': out['new_pairs'].append(dict(faces=[int(x) for x in Sf[i]], zone=z, centroid_cm=[round(float(x), 2) for x in Cf[i]]))
crit = [p for p in out['new_pairs'] if p['zone'] in ('hand', 'foot')]
out['new_hand_foot_groin_defects'] = len(crit); out['pass'] = len(crit) == 0
json.dump(out, open(OUT, 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'new_pairs'}))
