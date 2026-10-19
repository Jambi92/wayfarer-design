"""Assemble a candidate cage = UI cage (ui_v005.npz) with each foot below its ankle ring A replaced by the designed foot
sub-cage (fdesign_S.json). Mirrors the UI construction: delete faces below A, extrude A ring by ring (F1..V1, K),
fill K with 6 quads (cap), delete the cap quads used by toes, extrude toe tubes, close tips.
Usage: python3 buildfoot.py IN.npz OUT.npz L R"""
import numpy as np, sys, json, collections
inp, out = sys.argv[1], sys.argv[2]; sides = sys.argv[3:]
z = np.load(inp); Vc = z['V'].tolist(); Fc = [list(map(int, f[f >= 0])) for f in z['F']]
meta = {}
def edges_of(f): return [tuple(sorted((f[i], f[(i + 1) % len(f)]))) for i in range(len(f))]
for s in sides:
    D = json.load(open('fdesign_%s.json' % s)); ring = D['ankle_ring']; N = len(ring)
    rs = set(ring); re_ = set(tuple(sorted((ring[i], ring[(i + 1) % N]))) for i in range(N))
    # seed: a face touching the ring on the lower side
    VV = np.array(Vc)
    zr = VV[ring, 2].mean()
    e2f = collections.defaultdict(list)
    for fi, f in enumerate(Fc):
        for e in edges_of(f): e2f[e].append(fi)
    seed = None
    for e in re_:
        for fi in e2f[e]:
            if VV[Fc[fi], 2].mean() < zr: seed = fi
    seen = {seed}; st = [seed]
    while st:
        fi = st.pop()
        for e in edges_of(Fc[fi]):
            if e in re_: continue
            for g in e2f[e]:
                if g not in seen: seen.add(g); st.append(g)
    print(s, 'removed foot faces', len(seen))
    Fc = [f for i, f in enumerate(Fc) if i not in seen]
    def addv(p): Vc.append(list(map(float, p))); return len(Vc) - 1
    prev = ring; R = {}
    for sec in D['sections']:
        cur = [addv(p) for p in sec['pts']]; R[sec['name']] = cur
        for i in range(N): Fc.append([prev[i], prev[(i + 1) % N], cur[(i + 1) % N], cur[i]])
        prev = cur
    K = R['K']   # order d3,d4,d5,d6,p6..p0,d0,d1,d2  (or flipped: d3,d2,d1,d0,p0..p6,d6,d5,d4)
    if D['flipped']:
        dI = {3: K[0], 2: K[1], 1: K[2], 0: K[3]}; pI = {j: K[4 + j] for j in range(7)}; dI.update({6: K[11], 5: K[12], 4: K[13]})
    else:
        dI = {3: K[0], 4: K[1], 5: K[2], 6: K[3]}; pI = {6 - j: K[4 + j] for j in range(7)}; dI.update({0: K[11], 1: K[12], 2: K[13]})
    caps = [[dI[j], dI[j + 1], pI[j + 1], pI[j]] for j in range(6)]
    groups = {'t1': [0, 1], 't2': [2], 't3': [3], 't4': [4, 5]}
    for nm, cs in groups.items():
        if len(cs) == 1: base = caps[cs[0]]
        else: base = [dI[cs[0]], dI[cs[0] + 1], dI[cs[0] + 2], pI[cs[0] + 2], pI[cs[0] + 1], pI[cs[0]]]
        rings = np.array(D['tubes'][nm]); nb = len(base)
        B = np.array([Vc[i] for i in base]); best = None
        for sh in range(nb):
            for rev in (False, True):
                o = [(sh + j) % nb for j in range(nb)]
                if rev: o = o[::-1]
                c = np.linalg.norm(B - rings[0][o], axis=1).sum()
                if best is None or c < best[0]: best = (c, o)
        o = best[1]; pr = base; ids = []
        for r in rings:
            cur = [addv(r[o[j]]) for j in range(nb)]
            for j in range(nb): Fc.append([pr[j], pr[(j + 1) % nb], cur[(j + 1) % nb], cur[j]])
            pr = cur; ids.append(cur)
        if nb == 4: Fc.append(pr)
        else: Fc.append([pr[0], pr[1], pr[2], pr[3]]); Fc.append([pr[3], pr[4], pr[5], pr[0]])
        meta.setdefault(s, {}).setdefault('tubes', {})[nm] = ids
    meta[s]['rings'] = R
# orientation fix (BFS) + outward
Fa = Fc; e2f = collections.defaultdict(list)
for i, f in enumerate(Fa):
    for j in range(len(f)): e2f[tuple(sorted((f[j], f[(j + 1) % len(f)])))].append(i)
bad = [e for e, l in e2f.items() if len(l) != 2]
print('non-manifold/boundary edges', len(bad))
seen = [False] * len(Fa); seen[0] = True; qq = collections.deque([0])
while qq:
    i = qq.popleft(); f = Fa[i]
    for j in range(len(f)):
        a, b = f[j], f[(j + 1) % len(f)]
        for g in e2f[tuple(sorted((a, b)))]:
            if g == i or seen[g]: continue
            h = Fa[g]
            if any(h[t] == a and h[(t + 1) % len(h)] == b for t in range(len(h))): Fa[g] = h[::-1]
            seen[g] = True; qq.append(g)
Vn = np.array(Vc); usedv = np.unique(np.concatenate([np.array(f) for f in Fa])); mp = -np.ones(len(Vn), int); mp[usedv] = np.arange(len(usedv))
Fo = np.full((len(Fa), 4), -1)
for i, f in enumerate(Fa): Fo[i, :len(f)] = mp[f]
Vu = Vn[usedv]
T = np.array([[f[0], f[i], f[i + 1]] for f in Fo for i in range(1, (f >= 0).sum() - 1)])
vol = np.einsum('ij,ij->i', Vu[T[:, 0]], np.cross(Vu[T[:, 1]], Vu[T[:, 2]])).sum()
if vol < 0: Fo = np.array([np.r_[f[f >= 0][::-1], -np.ones(4 - (f >= 0).sum(), int)] for f in Fo])
def rm(x):
    if isinstance(x, list): return [rm(y) for y in x]
    if isinstance(x, dict): return {k: rm(v) for k, v in x.items()}
    return int(mp[x])
json.dump(rm(meta), open(out.replace('.npz', '_meta.json'), 'w'))
np.savez_compressed(out, V=Vu, F=Fo); print('cage', len(Vu), 'faces', len(Fo), 'vol', round(vol))
