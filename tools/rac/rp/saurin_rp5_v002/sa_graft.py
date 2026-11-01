# sa_graft.py BODY_CAGE.npz OPTB_CAGE.npz OPTB_DESIGN.pkl OUT.npz : Option B assembly. The gated revision cage (t2: body, head, vault / nostril patches,
#   hip-root loops, accepted tail module - T-1 / T-2 / T-3 / T-5 / T-6 / T-7 PASS) keeps everything outside the hands and feet; its hand / foot region is
#   replaced by the Option B local-density hand / foot region (incl. the fine 2:1 wrist / ankle transition rings). The two regions share the authored
#   wrist (Fa6) and ankle (S10) rings: same coarse ring, same fine vertex count (64 / 80); the Option B border ring vertices are identified with the
#   body cage's ring vertices (cyclic order + phase / direction by least distance; body positions kept). Result: one closed, consistently oriented quad
#   manifold, tail module untouched, body vertex block first (indices < n_body), tail module after.
import sys, os, pickle, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
BC, OC, DS, OUT = sys.argv[1:5]
HF = ['palm', 'finger', 'finger_web', 'finger_cap', 'thumb', 'thumb_cap', 'wrist', 'foot', 'forefoot', 'toe', 'toe_web', 'toe_cap', 'ankle']
b = np.load(BC); o = np.load(OC); d = pickle.load(open(DS, 'rb')); nm = d['name']; DQ = np.array(d['Q'])
Vb = (b['bc'][:, :, None] * G.V[G.F[b['tri']]]).sum(1); Vo = (o['bc'][:, :, None] * G.V[G.F[o['tri']]]).sum(1)
Qb, Qo = b['Q'], o['Q']; qlb, qlo = b['qlab'].astype(str), o['qlab'].astype(str); qco = o['qcoarse']
hb = np.isin(qlb, HF)
# the Option B region also holds the fine 2:1 transition band (one coarse row proximal of the body cage's wrist / ankle ring): grow the body cage's
# region by that band (DIL fine rows, edge adjacency) so both borders are the same authored ring (Fa6 / S10)
import scipy.sparse as sp
_e = np.sort(np.stack([Qb, np.roll(Qb, -1, 1)], 2).reshape(-1, 2), 1); _eu, _inv = np.unique(_e, axis=0, return_inverse=True); _inv = _inv.reshape(-1, 4)
EQ = sp.coo_matrix((np.ones(_inv.size), (_inv.ravel(), np.repeat(np.arange(len(Qb)), 4))), shape=(len(_eu), len(Qb))).tocsr(); QQe = (EQ.T @ EQ).tocsr()
HANDL = ['palm', 'finger', 'finger_web', 'finger_cap', 'thumb', 'thumb_cap', 'wrist']; hh = np.isin(qlb, HANDL); hf = hb & ~hh
for _ in range(int(os.environ.get('DIL_WRIST', 1))): hh = hh | (((QQe @ hh.astype(float)) > 0) & (qlb != 'tail'))     # nearest body-cage ring to the Option B
for _ in range(int(os.environ.get('DIL_ANKLE', 9))): hf = hf | (((QQe @ hf.astype(float)) > 0) & (qlb != 'tail'))     # Fa6 / S10 ring (measured offsets)
hb = hh | hf
trans = np.array([q >= 0 and q < len(DQ) and any(('_an2_x' in nm[i] or '_wr2_x' in nm[i]) for i in DQ[q]) for q in qco])
ho = np.isin(qlo, HF) | trans
def loops(Q, m, V):
    e = np.sort(np.stack([Q[m], np.roll(Q[m], -1, 1)], 2).reshape(-1, 2), 1); eu, c = np.unique(e, axis=0, return_counts=True); be = eu[c == 1]
    adj = collections.defaultdict(list)
    for a, b_ in be: adj[a].append(b_); adj[b_].append(a)
    assert max(len(v) for v in adj.values()) == 2
    seen = set(); L = []
    for s in adj:
        if s in seen: continue
        lp = [s]; seen.add(s); prev = None; cur = s
        while True:
            nx = [x for x in adj[cur] if x != prev and x not in seen]
            if not nx: break
            prev, cur = cur, nx[0]; lp.append(cur); seen.add(cur)
        L.append(np.array(lp))
    return L
Lb = loops(Qb, hb, Vb); Lo = loops(Qo, ho, Vo)
print('body-cage hand/foot border loops', [len(l) for l in Lb], '| Option B border loops', [len(l) for l in Lo])
ident = {}                                                        # Option B vertex -> body-cage vertex
for lo in Lo:
    c = Vo[lo].mean(0); lb = min(Lb, key=lambda l: np.linalg.norm(Vb[l].mean(0) - c)); assert len(lb) == len(lo), (len(lb), len(lo))
    best = None
    for sgn in (1, -1):
        lo_ = lo if sgn == 1 else lo[::-1]
        for sh in range(len(lo)):
            dd = np.linalg.norm(Vo[np.roll(lo_, sh)] - Vb[lb], axis=1).mean()
            if best is None or dd < best[0]: best = (dd, np.roll(lo_, sh))
    print('  ring', len(lo), 'mean offset %.3f mm' % (best[0] * 10))
    for x, y in zip(best[1], lb): ident[int(x)] = int(y)
# assemble: body-cage body vertices (minus its hand / foot interior) + Option B hand / foot vertices (minus the border) ; tail module after
nbb = int(b['n_body']); keepb_q = ~hb; vb_used = np.unique(Qb[keepb_q]); body_b = vb_used[vb_used < nbb]; tail_b = vb_used[vb_used >= nbb]
assert len(tail_b) == len(Vb) - nbb
vo_used = np.unique(Qo[ho]); new_o = np.array([v for v in vo_used if v not in ident])
nbo = int(o['n_body']); assert (new_o < nbo).all()
newidx_b = -np.ones(len(Vb), int); newidx_b[body_b] = np.arange(len(body_b)); nB = len(body_b)
newidx_o = -np.ones(len(Vo), int); newidx_o[new_o] = nB + np.arange(len(new_o)); nbody = nB + len(new_o)
newidx_b[tail_b] = nbody + np.arange(len(tail_b))
for x, y in ident.items(): newidx_o[x] = newidx_b[y]
Qn = np.vstack([newidx_b[Qb[keepb_q]], newidx_o[Qo[ho]]]); assert (Qn >= 0).all()
V = np.vstack([Vb[body_b], Vo[new_o], Vb[tail_b]])
qlab = np.r_[qlb[keepb_q], qlo[ho]]; qcoarse = np.r_[b['qcoarse'][keepb_q], -2 - np.maximum(qco[ho], 0)]   # Option B quads: -2 - (design_b coarse id)
src = np.r_[np.zeros(keepb_q.sum(), int), np.ones(ho.sum(), int)]
e = np.sort(np.stack([Qn, np.roll(Qn, -1, 1)], 2).reshape(-1, 2), 1); _, c = np.unique(e, axis=0, return_counts=True); assert c.min() == 2 and c.max() == 2, ('not closed', c.min(), c.max())
de = np.stack([Qn, np.roll(Qn, -1, 1)], 2).reshape(-1, 2); assert len(np.unique(de, axis=0)) == len(de), 'orientation'
pin_b = [newidx_b[p] for p in b['pinned'] if newidx_b[p] >= 0]; pin_o = [newidx_o[p] for p in o['pinned'] if newidx_o[p] >= 0 and ho[np.nonzero((Qo == p).any(1))[0]].any()]
pinned = np.unique(np.r_[pin_b, pin_o]).astype(int); tail_ring = newidx_b[b['tail_ring']]
fi, bc, dist = G.embed(V)
chi = len(V) - len(np.unique(e, axis=0)) + len(Qn)
np.savez_compressed(OUT, V=V, Q=Qn, tri=fi, bc=bc, qlab=qlab, qcoarse=qcoarse, n_body=nbody, tail_ring=tail_ring, pinned=pinned, part=src)
print('assembled', len(V), 'V', len(Qn), 'Q; closed, oriented, chi', chi, '| body-cage quads', int(keepb_q.sum()), 'Option B quads', int(ho.sum()), '| pins', len(pinned))
# merged design (optional 5th / 6th args: BODY_DESIGN.pkl OUT_DESIGN.pkl): name list indexed by the assembled cage's vertex index (authored corners keep
# their names; Option B corners override on the hands / feet), coarse quads of both designs mapped to the assembled indices (qcoarse: body-cage design
# quad q -> q, Option B quad q -> nQ_body + q), head / loops from the body design + the Option B knuckle / toe loops.
if len(sys.argv) > 6:
    dT = pickle.load(open(sys.argv[5], 'rb')); nmT = list(dT['name']); nmB = list(d['name'])
    names = [''] * len(V)
    for j, n in enumerate(nmB):
        if j < len(newidx_o) and newidx_o[j] >= 0 and newidx_o[j] < nbody: names[newidx_o[j]] = n
    for i, n in enumerate(nmT):
        if i < len(newidx_b) and newidx_b[i] >= 0 and newidx_b[i] < nbody and (names[newidx_b[i]] == '' or not np.isin(qlab, HF).any()): names[newidx_b[i]] = names[newidx_b[i]] or n
    seen = {}
    for i, n in enumerate(names):
        if n and n in seen: names[i] = n + '__dup'
        seen[n] = i
    QT = np.array(dT['Q']); QB = np.array(d['Q'])
    def mapq(Qd, mp): r = np.where(Qd < len(mp), mp[np.minimum(Qd, len(mp) - 1)], -1); return np.where(r < 0, 0, r)
    DQm = np.vstack([mapq(QT, newidx_b), mapq(QB, newidx_o)]); dql = list(dT['qlab']) + list(d['qlab'])
    loops = dict(dT['loops'])
    for k, v in d['loops'].items():
        if k.startswith('knuckle') or k.startswith('toe_ring'): loops[k] = v
    md = dict(C=V[:max(i for i, n in enumerate(names) if n) + 1], Q=DQm, name=names, qlab=dql, head=dT['head'], loops=loops, pins=dT.get('pins', {}), hint=None, fixed=None, arcs=None,
              note='merged design of the assembled cage: body = %s, hands / feet = Option B design' % os.path.basename(sys.argv[5]))
    pickle.dump(md, open(sys.argv[6], 'wb'))
    qcn = np.r_[b['qcoarse'][keepb_q], len(QT) + qco[ho]]; qcn = np.where(np.r_[b['qcoarse'][keepb_q], qco[ho]] < 0, -1, qcn)
    zz = dict(np.load(OUT)); zz['qcoarse'] = qcn; np.savez_compressed(OUT, **zz); print('merged design', sys.argv[6], 'named corners', sum(1 for n in names if n))
