# sa_inset.py DESIGN.pkl OUT.pkl SPEC.json : AUTHORED local support rings on the coarse cage (order 236dddc §3-§9).
#   SPEC = list of {"name": .., "quads": [coarse quad ids], "times": n}. Each patch (a disk of coarse quads) is inset n times: every patch boundary corner b
#   gets an inner twin b' (35 % towards the patch quads' centroids), the patch quads move onto the twins and one ring of quads (a, b, b', a') is added on every
#   patch boundary edge -> a closed support ring that follows the pocket / pit / crease; everything outside the patch keeps its topology and corners.
#   The tail-root hole (16 fixed edges) is never touched; quad orientation is preserved (ring quad a->b->b'->a' matches both neighbours).
import sys, json, pickle, numpy as np, collections
src, out, spec = sys.argv[1:4]; d = pickle.load(open(src, 'rb')); C = [np.asarray(c, float) for c in d['C']]; Q = [list(q) for q in d['Q']]; nm = list(d['name']); ql = list(d['qlab'])
def edges_count(QQ):
    c = collections.Counter()
    for q in QQ:
        for k in range(4): c[tuple(sorted((q[k], q[(k + 1) % 4])))] += 1
    return c
log = []
SP = json.load(open(spec)); cen0 = np.array([np.mean([C[v] for v in q], 0) for q in Q]); from scipy.spatial import cKDTree; kq = cKDTree(cen0)
qkey = {frozenset(nm[v] for v in q): i for i, q in enumerate(Q)}
def mirror(qs):
    out = []
    for q in qs:                                                   # side-tagged corners (limbs): mirror by name xneg <-> xpos; otherwise by geometry
        names = [nm[v] for v in Q[q]]
        if any('xneg' in n or 'xpos' in n for n in names):
            sw = frozenset(n.replace('xneg', '#').replace('xpos', 'xneg').replace('#', 'xpos') for n in names)
            if sw in qkey: out.append(qkey[sw]); continue
        out.append(int(kq.query(cen0[q] * [-1, 1, 1])[1]))
    return out
SP2 = []
for P in SP:                                                       # bilateral symmetry: every patch also gets its mirror twin (mirror quad by centroid x -> -x)
    SP2.append(P); mq = mirror(P['quads'])
    if P.get('sym', True) and sorted(mq) != sorted(P['quads']): SP2.append(dict(P, name=P['name'] + '_m', quads=mq))
for P in SP2:
    for t in range(int(P.get('times', 1))):
        pq = list(P['quads']); ec_all = edges_count(Q)
        bd = []                                                    # directed patch-boundary edges (orientation of the patch quad)
        ec = collections.Counter()
        for qi in pq:
            q = Q[qi]
            for k in range(4): ec[tuple(sorted((q[k], q[(k + 1) % 4])))] += 1
        for qi in pq:
            q = Q[qi]
            for k in range(4):
                a, b = q[k], q[(k + 1) % 4]
                if ec[tuple(sorted((a, b)))] == 1:
                    assert ec_all[tuple(sorted((a, b)))] == 2, ('patch touches the mesh boundary', P['name'])
                    bd.append((a, b))
        outd = collections.Counter(a for a, b in bd); ind = collections.Counter(b for a, b in bd)
        assert all(v == 1 for v in outd.values()) and all(v == 1 for v in ind.values()), ('patch is not a disk', P['name'])
        twin = {}
        for b in outd:
            inc = [qi for qi in pq if b in Q[qi]]; cen = np.mean([np.mean([C[v] for v in Q[qi]], 0) for qi in inc], 0)
            twin[b] = len(C); C.append(C[b] + 0.35 * (cen - C[b])); nm.append('%s_i%d_%s' % (P['name'], t, nm[b]))
        lab = {}
        for qi in pq:
            for a, b in [(Q[qi][k], Q[qi][(k + 1) % 4]) for k in range(4)]:
                if (a, b) in set(bd): lab[(a, b)] = ql[qi]
        for qi in pq: Q[qi] = [twin.get(v, v) for v in Q[qi]]
        for a, b in bd: Q.append([a, b, twin[b], twin[a]]); ql.append(lab[(a, b)])
        log.append((P['name'], t, len(bd)))
# validate: closed 2-manifold except the tail hole, consistent orientation
ec = edges_count(Q); dirE = collections.Counter((q[k], q[(k + 1) % 4]) for q in Q for k in range(4))
assert max(ec.values()) == 2 and sum(1 for v in ec.values() if v == 1) == 16 and max(dirE.values()) == 1
d['C'] = np.array(C); d['Q'] = np.array(Q); d['name'] = nm; d['qlab'] = ql
pickle.dump(d, open(out, 'wb')); print('inset patches', log); print('coarse', len(C), 'corners', len(Q), 'quads; chi', len(C) - len(ec) + len(Q))
