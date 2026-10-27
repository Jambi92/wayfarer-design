# contact_v4.py V003_CAND V003_LOOPS V004_CAND V004_LOOPS CORE_V4 OUT.json : order a18371c §10 -- contact / self-intersection gate of the family
# successor against the frozen-v003 fit of the same configuration. Self-intersection pairs come from audit.py (mathutils BVH, triangles of
# non-adjacent quads). Faces whose 4 vertices are unchanged v003 rows are geometrically identical in both meshes, so a pair can only be NEW if one of its
# faces touches a changed / new vertex (row_class != 0). Such pairs are matched to v003 pairs in the same place (centroid within 0.3 cm); unmatched
# ones are new family-base contact defects, classified by region (hand, foot: toe / web / sole / heel, groin / perineum, other).
import sys, json, numpy as np
from scipy.spatial import cKDTree
a = sys.argv[1:]; c3 = np.load(a[0]); l3 = np.load(a[1], allow_pickle=True); c4 = np.load(a[2]); l4 = np.load(a[3], allow_pickle=True); core = np.load(a[4]); OUT = a[5]
V3, Q3, V4, Q4 = c3['V'], c3['Q'], c4['V'], c4['Q']; rc = core['row_class']; S3, S4 = l3['SI'], l4['SI']; z3, z4 = l3['zone'], l4['zone']
ch = rc != 0
def cen(V, Q, S): return 0.5 * (V[Q[S[:, 0]]].mean(1) + V[Q[S[:, 1]]].mean(1)) if len(S) else np.zeros((0, 3))
C3, C4 = cen(V3, Q3, S3), cen(V4, Q4, S4)
touch = ch[Q4[S4[:, 0]]].any(1) | ch[Q4[S4[:, 1]]].any(1) if len(S4) else np.zeros(0, bool)
meta = json.loads(str(c4['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}; crotch_z = 0.5 * (H['thigh_l'][2] + H['thigh_r'][2])
def region(p, zn):
    if zn == 'hand': return 'hand'
    if zn == 'foot':
        side = 'l' if p[0] > 0 else 'r'; ball = H['ball_' + side]; foot = H['foot_' + side]
        if p[2] < 1.0: return 'foot_sole'
        if p[1] > ball[1] - 1.0: return 'foot_toe_web'
        if p[1] < foot[1]: return 'foot_heel'
        return 'foot_other'
    if zn in ('trunk', 'leg') and abs(p[0]) < 12 and crotch_z - 10 < p[2] < crotch_z + 6: return 'groin_perineum'
    return 'other'
kd = cKDTree(C3) if len(C3) else None; new = []
for i in np.nonzero(touch)[0]:
    if kd is None or kd.query(C4[i])[0] > 0.3: new.append(int(i))
def by_region(C, S, z):
    out = {}
    for p, s in zip(C, S): r = region(p, z[s[0]]); out[r] = out.get(r, 0) + 1
    return out
res = dict(v003_pairs=int(len(S3)), v004_pairs=int(len(S4)), v003_by_region=by_region(C3, S3, z3), v004_by_region=by_region(C4, S4, z4),
           v004_pairs_touching_changed_vertices=int(touch.sum()), new_pairs_unmatched_in_v003=len(new), new_by_region=by_region(C4[new], S4[new], z4) if new else {},
           new_pair_centroids_cm=np.round(C4[new], 2).tolist()[:40])
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps({k: v for k, v in res.items() if k != 'new_pair_centroids_cm'}))
