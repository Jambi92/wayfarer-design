"""Label toes from footreeb bands: seeds = components (>30 verts) of band `seedband`; each grows to all distal connected
bands (children) and proximally while its parent leads only to it. Output ftlab_S.npy [used vertex id, toe label or -1].
Toes are renamed by position across the foot (0 = hallux/medial ... 4 = little toe). Usage: python3 footlabel.py S seedband"""
import numpy as np, sys, json
s = sys.argv[1]; sb = int(sys.argv[2])
z = np.load('freeb_%s.npz' % s); used = z['used']; comp = z['comp']; bands = z['bands']; sizes = z['sizes']; E = z['E']
ca, cb = comp[E[:, 0]], comp[E[:, 1]]; ok = (ca >= 0) & (cb >= 0); ca, cb = ca[ok], cb[ok]
par = {}; child = {}
for x, y in set(zip(ca.tolist(), cb.tolist())):
    if bands[y] == bands[x] - 1: par.setdefault(x, set()).add(y); child.setdefault(y, set()).add(x)
    if bands[x] == bands[y] - 1: par.setdefault(y, set()).add(x); child.setdefault(x, set()).add(y)
seeds = [c for c in range(len(bands)) if bands[c] == sb and sizes[c] > 30]
lab = {}
for k, sd in enumerate(seeds):
    st = [sd]
    while st:
        c = st.pop()
        if c in lab: continue
        lab[c] = k; st += list(child.get(c, []))
    c = sd
    while c in par and len(par[c]) == 1:
        p = next(iter(par[c]))
        if len(child.get(p, ())) != 1 or p in lab: break
        lab[p] = k; c = p
vl = np.array([lab.get(int(c), -1) if c >= 0 else -1 for c in comp])
w = np.load('/home/claude/stc/rp1/weld.npz'); V = w['V'][used]
L = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))['toe_tips_' + s]
ax = np.array(L['foot_axis']) * [1, -1, 0]; ax /= np.linalg.norm(ax); lat = np.cross([0, 0, 1.0], ax)   # lat points to subject right? 
cen = {k: V[vl == k].mean(0) for k in range(len(seeds))}
# medial direction: toward body midline (x -> 0)
med = -np.sign(V[:, 0].mean()) * np.array([1.0, 0, 0])
order = sorted(cen, key=lambda k: -(cen[k] @ med))      # most medial first = hallux
remap = {k: i for i, k in enumerate(order)}
vl2 = np.array([remap[q] if q >= 0 else -1 for q in vl])
print(s, 'seeds', len(seeds), {i: int((vl2 == i).sum()) for i in range(-1, len(seeds))})
for i in range(len(seeds)):
    P = V[vl2 == i]; print('  toe', i, 'centroid', P.mean(0).round(1), 'n', len(P))
np.save('ftlab_%s.npy' % s, np.c_[used, vl2])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cm = ['r', 'g', 'b', 'm', 'c', 'orange']
col = np.array(['0.75' if q < 0 else cm[q] for q in vl2])
fig, axs = plt.subplots(1, 3, figsize=(30, 10))
for a, (i_, j, k, sg) in zip(axs, [(0, 1, 2, 1), (0, 2, 1, 1), (0, 1, 2, -1)]):
    o = np.argsort(sg * V[:, k]); a.scatter(V[o, i_], V[o, j], c=col[o], s=1); a.set_aspect('equal')
plt.savefig('ftlab_%s.png' % s, dpi=40, bbox_inches='tight')
