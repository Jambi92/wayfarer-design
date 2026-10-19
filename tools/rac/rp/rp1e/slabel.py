"""label digits from the surface Reeb bands: seeds = the components of the band where the hand shows 5 digit components;
propagate to children (distal) and to parents while the parent leads only to this digit (proximal, down to the web)."""
import numpy as np, sys, json
s = sys.argv[1]; seedband = int(sys.argv[2])
z = np.load('/home/claude/stc/rp1e/sreeb_%s.npz' % s); used = z['used']; comp = z['comp']; bands = z['bands']; sizes = z['sizes']
par = {int(k): v for k, v in json.load(open('/home/claude/stc/rp1e/sreeb_%s_par.json' % s))['par'].items()}
child = {}
for c, ps in par.items():
    for p in ps: child.setdefault(p, set()).add(c)
seeds = [c for c in range(len(bands)) if bands[c] == seedband and sizes[c] > 30]
lab = {}
for k, sd in enumerate(seeds):
    st = [sd]
    while st:
        c = st.pop()
        if c in lab: continue
        lab[c] = k
        st += list(child.get(c, []))
    c = sd
    while c in par and len(par[c]) == 1:
        p = next(iter(par[c]))
        if len(child.get(p, ())) != 1 or p in lab: break
        lab[p] = k; c = p
vl = np.array([lab.get(int(c), -1) if c >= 0 else -1 for c in comp])
print('seeds', len(seeds), {k: int((vl == k).sum()) for k in range(-1, len(seeds))})
np.save('/home/claude/stc/rp1e/vlab_%s.npy' % s, np.c_[used, vl])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'][used]
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cm = ['r', 'g', 'b', 'm', 'c', 'orange', 'y']
col = np.array(['0.75' if q < 0 else cm[q] for q in vl])
fig, ax = plt.subplots(2, 3, figsize=(27, 20))
for a, (i_, j, k, sg) in zip(ax.ravel(), [(0, 2, 1, -1), (0, 2, 1, 1), (1, 2, 0, 1), (1, 2, 0, -1), (0, 1, 2, 1), (0, 1, 2, -1)]):
    o = np.argsort(sg * V[:, k]); a.scatter(V[o, i_], V[o, j], c=col[o], s=2); a.set_aspect('equal')
plt.savefig('/home/claude/stc/rp1e/slab_%s.png' % s, dpi=45, bbox_inches='tight')
