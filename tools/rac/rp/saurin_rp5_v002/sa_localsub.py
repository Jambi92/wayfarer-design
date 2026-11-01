# sa_localsub.py DESIGN.pkl CAGE_OF_DESIGN.npz OUT.pkl : OPTION B local structural density (order fe3b98a). One extra subdivision level ONLY in the
#   hands (palm, thumb, fingers, finger webs, caps) and feet (ankle / heel rings, foot, forefoot, toes, toe webs, caps): every coarse quad there is split
#   1 -> 4 (edge midpoints + face point), which after the 3 Catmull-Clark levels of sa_ccage gives those regions one more level than the body.
#   Controlled all-quad 2:1 transitions replace the wrist band (Fa6 8 -> Wr 16) and the distal shin band (S10 10 -> S11 20); nothing else changes
#   (head, torso, pelvis, tail, upper arms, thighs untouched). New corner positions are taken from the built cage of the same design (the level-1
#   Catmull-Clark edge / face points of a coarse quad are fine vertices that already lie on the working source -> no projection across web gaps).
import sys, os, pickle, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
DS, CG, OUT = sys.argv[1:4]; d = pickle.load(open(DS, 'rb')); z = np.load(CG)
C = [np.asarray(c, float) for c in d['C']]; Q = [list(q) for q in d['Q']]; nm = list(d['name']); ql = list(d['qlab']); ix = {n: i for i, n in enumerate(nm)}
Vfine = (z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1); nv0 = len(C); Qa = np.array(Q)
Eu = np.unique(np.sort(np.stack([Qa, np.roll(Qa, -1, 1)], 2).reshape(-1, 2), 1), axis=0); eid = {tuple(e): i for i, e in enumerate(Eu)}; ne0 = len(Eu)
assert len(Vfine) >= nv0 + ne0 + len(Q)
def epos(a, b): return Vfine[nv0 + eid[(min(a, b), max(a, b))]]
def fpos(q): return Vfine[nv0 + ne0 + q]
HAND = {'palm', 'finger', 'finger_web', 'finger_cap', 'thumb', 'thumb_cap'}; FOOT = {'ankle', 'foot', 'forefoot', 'toe', 'toe_web', 'toe_cap'}
R = [i for i, l in enumerate(ql) if l in HAND | FOOT]; Rs = set(R)
mid = {}
def m(a, b):
    k = (min(a, b), max(a, b))
    if k not in mid: mid[k] = len(C); C.append(epos(a, b).copy()); nm.append('sub_%s__%s' % (nm[k[0]], nm[k[1]]))
    return mid[k]
newQ = []; newL = []
for qi in R:
    a, b, c, dd = Q[qi]; mab, mbc, mcd, mda = m(a, b), m(b, c), m(c, dd), m(dd, a); f = len(C); C.append(fpos(qi).copy()); nm.append('subf_%d' % qi)
    for qq in ([a, mab, f, mda], [mab, b, mbc, f], [f, mbc, c, mcd], [mda, f, mcd, dd]): newQ.append(qq); newL.append(ql[qi])
# 2:1 transitions: band between COARSE ring Rc (N corners) and FINE ring Rf (the region boundary ring, now 2N with its midpoints)
drop = set(R); tr = []
def transition(rc_pre, rf_pre, lab, tag):
    rc = [ix['%s_%d' % (rc_pre, k)] for k in range(100) if '%s_%d' % (rc_pre, k) in ix]; rf = [ix['%s_%d' % (rf_pre, k)] for k in range(100) if '%s_%d' % (rf_pre, k) in ix]
    N = len(rc); assert len(rf) == N and N % 2 == 0
    band = [i for i, q in enumerate(Q) if set(q) <= set(rc) | set(rf) and len(set(q) & set(rc)) == 2]; assert len(band) == N, (rc_pre, len(band))
    for i in band: drop.add(i)
    fine = []
    for k in range(N): fine += [rf[k], mid[(min(rf[k], rf[(k + 1) % N]), max(rf[k], rf[(k + 1) % N]))]]
    for p in range(N // 2):
        f_ = [fine[(4 * p + j) % (2 * N)] for j in range(5)]; cc = [rc[(2 * p + j) % N] for j in range(3)]
        x = len(C); C.append(epos(rc[(2 * p + 1) % N], rf[(2 * p + 1) % N]).copy()); nm.append('%s_x%d' % (tag, p))
        for qq in ([f_[0], f_[1], x, cc[0]], [f_[1], f_[2], f_[3], x], [f_[3], f_[4], cc[2], x], [x, cc[2], cc[1], cc[0]]): newQ.append(qq); newL.append(lab); tr.append(len(newQ) - 1)
for s in ('xpos', 'xneg'):
    transition('Fa6_' + s, 'Wr_' + s, 'wrist', '%s_wr2' % s); transition('S10_' + s, 'S11_' + s, 'shin', '%s_an2' % s)
Qn = [q for i, q in enumerate(Q) if i not in drop]; Ln = [l for i, l in enumerate(ql) if i not in drop]; Qn += newQ; Ln += newL
# consistent orientation (BFS from the untouched body quads)
EQ = collections.defaultdict(list)
for i, q in enumerate(Qn):
    for k in range(4): EQ[(min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4]))].append(i)
seen = np.zeros(len(Qn), bool); seen[:len(Qn) - len(newQ)] = True; st = list(range(len(Qn) - len(newQ))); flips = 0
while st:
    a = st.pop(); da = {(Qn[a][k], Qn[a][(k + 1) % 4]) for k in range(4)}
    for k in range(4):
        e = (min(Qn[a][k], Qn[a][(k + 1) % 4]), max(Qn[a][k], Qn[a][(k + 1) % 4]))
        for b in EQ[e]:
            if seen[b]: continue
            if {(Qn[b][j], Qn[b][(j + 1) % 4]) for j in range(4)} & da: Qn[b] = Qn[b][::-1]; flips += 1
            seen[b] = True; st.append(b)
ec = collections.Counter((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])) for q in Qn for k in range(4))
dirE = collections.Counter((q[k], q[(k + 1) % 4]) for q in Qn for k in range(4))
assert max(ec.values()) == 2 and sum(1 for v in ec.values() if v == 1) == 16 and max(dirE.values()) == 1, 'manifold / orientation'
d2 = dict(d); d2['C'] = np.array(C); d2['Q'] = np.array(Qn); d2['name'] = nm; d2['qlab'] = Ln
pickle.dump(d2, open(OUT, 'wb')); print('Option B local subdivision: region coarse quads', len(R), '-> x4;', 'coarse', len(C), 'corners', len(Qn), 'quads; chi', len(C) - len(ec) + len(Qn), '; flips', flips)
