# quick_eval.py : fast branch-iteration checks on a realized mesh (V, Q) -- integrity (manifold / winding / boundary), quality of the branch quads
# (T-4 angle 45-135 and aspect <= 4 exactly as core3lib.quality), and the authoritative val2lib validator on chosen stations.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import quality
import val2lib
def integrity(Q, nV):
    from collections import Counter
    he = Counter();
    for q in Q:
        for k in range(4): he[(int(q[k]), int(q[(k + 1) % 4]))] += 1
    bad_dup = sum(1 for k, c in he.items() if c > 1); und = Counter()
    for (a, b), c in he.items(): und[(min(a, b), max(a, b))] += c
    boundary = sum(1 for k, c in und.items() if c == 1); nonman = sum(1 for k, c in und.items() if c > 2)
    opp = sum(1 for (a, b) in he if (b, a) not in he)
    used = np.zeros(nV, bool); used[np.asarray(Q).ravel()] = True; degen = int(sum(len(set(map(int, q))) < 4 for q in Q))
    return dict(boundary_edges=boundary, nonmanifold_edges=nonman, winding_conflicts=bad_dup, unpaired_halfedges=opp, unused_verts=int((~used).sum()), degenerate=degen)
def branch_quality(V, Q, fids):
    ang, asp, bad_ang, bad_asp = quality(V, np.asarray(Q)[fids])
    return dict(n=len(fids), aspect_gt4=int(bad_asp.sum()), angle_viol=int(bad_ang.sum()), aspect_max=round(float(asp.max()), 3), aspect_p95=round(float(np.percentile(asp, 95)), 3),
                angle_min=round(float(ang.min()), 1), angle_max=round(float(ang.max()), 1), worst=[int(fids[i]) for i in np.argsort(-asp)[:5]])
def validate(V, Q, meta, names=None, d6=None):
    r = val2lib.evaluate(V, Q, meta, ref_stature=173.143, names=names, d5=True, d6=d6)
    return {k: dict(firm=v['firm_D1_D3'], status=v['status_D1_D3'], loops=v['loops_v2'], margin=v['margin'], crease=v['crease_poles'], within2=len(v['within2_poles']), h=v['local_loop_cm'])
            for k, v in r['stations'].items()}, r['summary']
