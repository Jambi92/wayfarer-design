# sa_fc_semantic.py DESIGN.pkl CAGE.npz OUT.json [PATCH_SPEC.json ...] : semantic topology map of the full cage (order ad9cb85 §13 / f0a2b96 §14). Every authored coarse ring /
# named loop is traced on the fine cage (coarse corners keep their indices through Catmull-Clark; each coarse edge = an 8-hop fine edge chain), labelled
# by anatomy; per-face labels (coarse quad label, claw caps, 2:1 rows, display root) and the accepted tail module bands. Topology-only -> identical c1 / c2.
import sys, re, json, pickle, hashlib, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
d = pickle.load(open(sys.argv[1], 'rb')); z = np.load(sys.argv[2]); Q = z['Q']; nv = len(z['V']); nm = d['name']; ix = {x: i for i, x in enumerate(nm)}
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0); A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr()
def chain(a, b):
    """fine vertex chain a -> b along the subdivided coarse edge (BFS, <= 8 hops); None if the corners are not coarse neighbours"""
    prev = {a: -1}; front = [a]
    for _ in range(int(__import__('os').environ.get('HOPS', 20))):
        nxt = []
        for u in front:
            for w in A.indices[A.indptr[u]:A.indptr[u + 1]]:
                if w not in prev: prev[w] = u; nxt.append(w)
        front = nxt
        if b in prev: break
    if b not in prev: return None
    p = [b]
    while p[-1] != a: p.append(prev[p[-1]])
    return p[::-1]
rings = {}
for n in nm:
    m = re.match(r'^(.*)_(\d+)$', n)
    if m: rings.setdefault(m.group(1), []).append((int(m.group(2)), n))
def sem(r):
    rules = [(r'^T[0-2]$', 'trunk flex ring (upper thorax / shoulder rows)'), (r'^T3$', 'shoulder / axilla row'), (r'^T[45]$', 'trunk flex ring'), (r'^P[0-3]$', 'lower axial ring (tail-root hole rows)'),
             (r'^P4$', 'hip / thigh-root ring'), (r'^A\d_', 'shoulder / upper-arm support ring'), (r'^El\d_', 'elbow ring'), (r'^Fa\d_', 'forearm ring'), (r'^Wr_', 'wrist ring'),
             (r'^(H0b|H1)_', 'palm ring'), (r'^L1_', 'hip ring'), (r'^L\d_', 'thigh ring'), (r'^Kn\d_', 'knee ring'), (r'^S11_', 'ankle ring'), (r'^S\d+_', 'shin ring'),
             (r'^Fd[0-2]_', 'ankle / heel ring'), (r'^Fd\d_', 'foot ring'), (r'_f\d_r1$', 'finger PIP ring'), (r'_f\d_r2$', 'finger DIP / claw-base ring'), (r'_th_r1$', 'thumb IP ring'),
             (r'_th_r2$', 'thumb claw-base ring'), (r'_t\d_r1$', 'toe IP ring'), (r'_t\d_r2$', 'toe claw-base ring'), (r'_orb\d$', 'orbit ring'), (r'^Hd\d+$', 'head / neck ring')]
    for pat, lab in rules:
        if re.search(pat, r): return lab
    return 'ring'
im = d['head']['im']; loops = []
for r, lst in rings.items():
    lst = [n for _, n in sorted(lst)]
    if len(lst) < 3: continue
    lab = sem(r)
    if r.startswith('Hd'):
        k = int(r[2:]); lab = 'neck ring' if k < 3 else ('jaw-hinge / mouth-corner ring' if k == im else ('mouth-support ring (rostral)' if k > im else 'head ring'))
    loops.append((r, lab, lst))
for k, lst in d['loops'].items():
    lab = {'tail': 'tail root ring (= accepted module ring 0)', 'hip_': 'hip root ring', 'shoulder': 'shoulder / axilla hole ring', 'knuckle': 'MCP (knuckle) ring incl. webs',
           'toe_ring': 'MTP ring incl. webs', 'orbit_rim': 'orbit rim ring', 'mouth': 'mouth slit (closed lip line)'}
    loops.append((k, next((v for kk, v in lab.items() if k.startswith(kk)), 'loop'), lst))
for s in ('xpos', 'xneg'):
    for i in range(1, 5): loops.append(('%s_f%d_base' % (s, i), 'finger MCP base ring', ['%s_f%d_%s' % (s, i, x) for x in ('DR', 'DU', 'PU', 'PR')]))
    for i in range(1, 6): loops.append(('%s_t%d_base' % (s, i), 'toe MTP base ring', ['%s_t%d_%s' % (s, i, x) for x in ('DM', 'DL', 'PL', 'PM')]))
out = []
for name, lab, lst in loops:
    if not all(x in ix for x in lst): continue
    cyc = name not in ('mouth_slit',); seq = lst + ([lst[0]] if cyc else []); vs = []
    segs = [chain(ix[a], ix[b]) for a, b in zip(seq[:-1], seq[1:])]
    if any(c is None for c in segs): cyc = False                                     # ring interrupted by a hole (tail root / shoulder / orbit): open chain
    for c in segs:
        if c is not None: vs += c[:-1]
    out.append(dict(name=name, semantic=lab, closed=cyc, fine_vertices=[int(v) for v in vs]))
# tail module bands (module rings after the body vertices)
tm = np.load('/tmp/claude-0/rt/sa/tail/SA_tail_module.npz'); nb = int(z['n_body']); bl = z['tail_ring']; rs, rn = tm['ring_start'], tm['ring_N']
mm = np.r_[bl, nb + np.arange(len(tm['V']) - 128)]
for i, (a, n) in enumerate(zip(rs, rn)):
    if i % 10 == 0 or i < 11: out.append(dict(name='tail_ring_%03d' % i, semantic='tail root ring' if i < 11 else 'tail chain band ring', closed=True, fine_vertices=mm[a:a + n].tolist()))
qlab = z['qlab'].astype(str).copy(); qc = z['qcoarse']
for i in np.nonzero(qc >= 0)[0][:0]: pass
crn = np.array(d['Q']); has_x = np.array([any(re.search(r'_(pt|ft|wr2|an2)_x\d', nm[c]) for c in q) for q in crn])
face_sem = np.where(np.isin(qlab, ['finger_cap', 'thumb_cap', 'toe_cap']), 'claw cap', qlab)
face_sem = np.where((qc >= 0) & has_x[np.maximum(qc, 0)], '2:1 reduction row', face_sem)
# authored local patches added in the targeted revision (sa_vault): quads touching a body vertex created after the CC build (index >= NB0)
NB0 = int(__import__('os').environ.get('NB0', 91969)); PATCH = []
for f_ in sys.argv[4:]:
    for P_ in json.load(open(f_)): PATCH.append((P_['name'], np.asarray(P_['centre'], float)))
if PATCH:
    Vv = z['V']; newq = np.nonzero(((Q >= NB0) & (Q < nb)).any(1))[0]; qcen = Vv[Q[newq]].mean(1)
    nmP = np.array([n_ for n_, _ in PATCH]); cP = np.array([c_ for _, c_ in PATCH]); near = np.argmin(np.linalg.norm(qcen[:, None] - cP[None], axis=2), 1)
    tagmap = {'axillary_vault': 'axillary vault patch (apex floor + 2 support rings)', 'nostril_pit': 'nostril pit ring', 'perineal': 'perineal / tail-underside support ring', 'tail_underside': 'perineal / tail-underside support ring'}
    face_sem = face_sem.astype(object)
    for q_, k_ in zip(newq, near): face_sem[q_] = next(v for kk, v in tagmap.items() if nmP[k_].startswith(kk))
    face_sem = face_sem.astype(str)
res = dict(order='ad9cb85 §13 / f0a2b96 §14', loops=out, face_semantic_counts={k: int(v) for k, v in zip(*np.unique(face_sem, return_counts=True))},
           face_semantic_sha256=hashlib.sha256('\n'.join(face_sem).encode()).hexdigest(), topology_sha256=hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest(),
           c1_c2='one face list / vertex order / semantic map: realized on SA-M188 and SA-F188 by the same barycentric embedding')
json.dump(res, open(sys.argv[3], 'w')); np.save(sys.argv[3] + '.face_semantic.npy', face_sem)
print('loops', len(out), res['face_semantic_counts'])
