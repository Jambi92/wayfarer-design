"""Assemble a candidate cage = v004 cage with the old hand(s) removed distal of the wrist loop + designed hand sub-cages.
Mirrors the UI construction: delete hand faces beyond W0, extrude W0 edge loop -> P1 -> P2 -> P3, fill P3 with 4 quads,
extrude each cap quad into a digit tube (ring by ring), extrude the thumb from the palmar radial quad between P1 and P2.
Usage: python3 buildcage.py OUT.npz [R] [L]   (hands with design_S.json + wrist_S.json present get rebuilt)"""
import numpy as np, sys, json
out = sys.argv[1]; hands = sys.argv[2:]
z = np.load('/home/claude/stc/rp1/ck/v004a.npz'); Vc = (z['Vc'] * [1, -1, 1]).tolist(); Fc = [list(f[f >= 0]) for f in z['Fc']]
def edges_of(f): return [tuple(sorted((f[i], f[(i + 1) % len(f)]))) for i in range(len(f))]
meta = {}
for s in hands:
    W = json.load(open('/home/claude/stc/rp1e/wrist_%s.json' % s))   # {'d':[5 ids radial->ulnar], 'p':[5 ids radial->ulnar], 'hand_face_seed': id}
    D = json.load(open('/home/claude/stc/rp1e/design_%s.json' % s))
    ring_ids = W['d'] + W['p'][::-1]                       # d0..d4, p4..p0
    ring_edges = set(tuple(sorted((ring_ids[i], ring_ids[(i + 1) % 10]))) for i in range(10))
    # flood fill hand faces from seed without crossing ring edges
    e2f = {}
    for fi, f in enumerate(Fc):
        for e in edges_of(f): e2f.setdefault(e, []).append(fi)
    seen = {W['hand_face_seed']}; st = [W['hand_face_seed']]
    while st:
        fi = st.pop()
        for e in edges_of(Fc[fi]):
            if e in ring_edges: continue
            for g in e2f[e]:
                if g not in seen: seen.add(g); st.append(g)
    keep = [f for i, f in enumerate(Fc) if i not in seen]
    print(s, 'removed hand faces', len(seen))
    Fc = keep
    def addv(p): Vc.append(list(p)); return len(Vc) - 1
    def ring10(name): r = D['rings'][name]; return [addv(p) for p in r['d']] + [addv(p) for p in r['p'][::-1]]
    prev = ring_ids; R = {}
    RN = D.get('ring_names', ['P1', 'P2', 'P3'])
    for nm in RN:
        cur = ring10(nm); R[nm] = cur
        for i in range(10): Fc.append([prev[i], prev[(i + 1) % 10], cur[(i + 1) % 10], cur[i]])
        prev = cur
    def d_(nm, k): return R[nm][k]
    def p_(nm, k): return R[nm][9 - k]
    LAST = RN[-1]
    caps = {r: [d_(LAST, k), d_(LAST, k + 1), p_(LAST, k + 1), p_(LAST, k)] for k, r in enumerate(['index', 'middle', 'ring', 'pinky'])}
    # thumb base quad (palmar, radial end, between P1 and P2)
    ta, tb = D.get('thumb_between', ['P1', 'P2']); tq = [p_(ta, 0), p_(ta, 1), p_(tb, 1), p_(tb, 0)]
    def tube(base, rings, crotch=None):
        rings = np.array(rings)
        if crotch is not None:
            B0 = np.array([Vc[i] for i in base]); cB = B0.mean(0)
            cr = cB + crotch['offset'] + crotch['scale'] * (B0 - cB)
            # insert as first ring, corners in base order (so correspondence is identity)
            rings_c = [cr]
        # best cyclic correspondence base corner -> ring corner (min twist)
        B = np.array([Vc[i] for i in base]); best = None
        for sh in range(4):
            for rev in (False, True):
                o = [(sh + j) % 4 for j in range(4)]
                if rev: o = o[::-1]
                c = np.linalg.norm(B - rings[0][o], axis=1).sum()
                if best is None or c < best[0]: best = (c, o)
        o = best[1]; prevr = base; ids = []
        if crotch is not None:
            cur = [addv(p) for p in cr]
            for j in range(4): Fc.append([prevr[j], prevr[(j + 1) % 4], cur[(j + 1) % 4], cur[j]])
            prevr = cur; ids.append(cur)
            # recompute correspondence against the crotch ring
            B = cr; best = None
            for sh in range(4):
                for rev in (False, True):
                    oo = [(sh + j) % 4 for j in range(4)]
                    if rev: oo = oo[::-1]
                    c = np.linalg.norm(B - rings[0][oo], axis=1).sum()
                    if best is None or c < best[0]: best = (c, oo)
            o = best[1]
        for r in rings:
            cur = [addv(r[o[j]]) for j in range(4)]
            for j in range(4): Fc.append([prevr[j], prevr[(j + 1) % 4], cur[(j + 1) % 4], cur[j]])
            prevr = cur; ids.append(cur)
        Fc.append(prevr[::-1] if False else prevr)   # tip cap (orientation fixed later)
        return ids, o
    meta[s] = dict(W0=ring_ids, P=R, caps=caps, thumb_base=tq, tubes={})
    tqs = set(tq); Fc = [f for f in Fc if set(f) != tqs]   # the extruded thumb base face is replaced by the tube
    for role, base in list(caps.items()) + [('thumb', tq)]:
        cro = D.get('crotch', {}).get(role)
        if cro: cro = dict(offset=np.array(cro['offset']), scale=cro['scale'])
        ids, o = tube(base, D['tubes'][role], cro); meta[s]['tubes'][role] = dict(rings=ids, corr=o)
# fix orientation consistently (BFS winding)
import collections
Fa = [list(map(int, f)) for f in Fc]
e2f = collections.defaultdict(list)
for i, f in enumerate(Fa):
    for j in range(len(f)): e2f[tuple(sorted((f[j], f[(j + 1) % len(f)])))].append(i)
seen = [False] * len(Fa); seen[0] = True; q = collections.deque([0])
while q:
    i = q.popleft(); f = Fa[i]
    for j in range(len(f)):
        a, b = f[j], f[(j + 1) % len(f)]
        for g in e2f[tuple(sorted((a, b)))]:
            if g == i or seen[g]: continue
            h = Fa[g]; k = [t for t in range(len(h)) if h[t] == a and h[(t + 1) % len(h)] == b]
            if k: Fa[g] = h[::-1]
            seen[g] = True; q.append(g)
Vn = np.array(Vc); used = np.unique(np.concatenate([np.array(f) for f in Fa]))
mp = -np.ones(len(Vn), int); mp[used] = np.arange(len(used))
Fo = np.full((len(Fa), 4), -1)
for i, f in enumerate(Fa): Fo[i, :len(f)] = mp[f]
# outward: signed volume
T = np.array([[f[0], f[i], f[i + 1]] for f in Fo for i in range(1, (f >= 0).sum() - 1)])
Vu = Vn[used]; vol = np.einsum('ij,ij->i', Vu[T[:, 0]], np.cross(Vu[T[:, 1]], Vu[T[:, 2]])).sum()
if vol < 0: Fo = np.array([np.r_[f[f >= 0][::-1], -np.ones(4 - (f >= 0).sum(), int)] for f in Fo])
remap = {int(k): int(mp[k]) for k in used}
def rm(x):
    if isinstance(x, list): return [rm(y) for y in x]
    if isinstance(x, dict): return {k: rm(v) for k, v in x.items()}
    return remap.get(int(x), -1) if isinstance(x, (int, np.integer)) else x
json.dump({s: rm({k: v for k, v in m.items()}) for s, m in meta.items()}, open(out.replace('.npz', '_meta.json'), 'w'))
np.savez_compressed(out, V=Vu, F=Fo)
print('cage', len(Vu), 'faces', len(Fo), 'signed vol', vol)
