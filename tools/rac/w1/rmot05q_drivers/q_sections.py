# RM-OT-05Q plane sections for garment separability (raw mesh/plane segments, no repair).
# Each plane: "label:ox,oy,oz:nx,ny,nz:R" -> segments within R cm of the origin, chained into loops (welded vertices),
# loop count, closed/open, area and nesting depth (a loop lying inside another loop = a second surface under the first).
# Usage: python3 q_sections.py --mesh M.obj --out OUT(.png/.json) --planes P1 P2 ... [--labels face_labels.npy]
import argparse, json, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.path import Path
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--out'); ap.add_argument('--planes', nargs='+'); ap.add_argument('--labels')
ap.add_argument('--cols', type=int, default=4); a = ap.parse_args()
m = trimesh.load(a.mesh, process=False); V = np.asarray(m.vertices); F = np.asarray(m.faces)
lab = np.load(a.labels) if a.labels else None
COL = ['0.2', 'tab:red', 'tab:blue', 'orange', 'tab:green', 'tab:purple']
def basis(n):
    n = n / np.linalg.norm(n); t = np.array([0, 0, 1.0]) if abs(n[2]) < 0.9 else np.array([1.0, 0, 0])
    u = np.cross(t, n); u /= np.linalg.norm(u); return u, np.cross(n, u)
def area(p): return 0.5 * abs(np.dot(p[:, 0], np.roll(p[:, 1], 1)) - np.dot(p[:, 1], np.roll(p[:, 0], 1)))
res = []; n_ = len(a.planes); cols = min(a.cols, n_); rows = (n_ + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.4 * rows), squeeze=False)
for k, spec in enumerate(a.planes):
    name, o, n, R = spec.split(':'); o = np.array([float(t) for t in o.split(',')]); n = np.array([float(t) for t in n.split(',')]); R = float(R)
    n = n / np.linalg.norm(n); u, v = basis(n)
    near = (np.linalg.norm(V[F].mean(1) - o, axis=1) < R * 1.5); fi = np.where(near)[0]
    sd = (V - o) @ n; s = sd[F[fi]]; cross = (s.min(1) < 0) & (s.max(1) > 0); fi = fi[cross]
    segs = []; keys = []
    for f in fi:                                   # each crossing triangle -> one segment between two edge crossings
        pts = []; ks = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a_, b_ = F[f, i], F[f, j]
            if (sd[a_] < 0) != (sd[b_] < 0):
                t = sd[a_] / (sd[a_] - sd[b_]); p = V[a_] + t * (V[b_] - V[a_]); pts.append(p); ks.append((min(a_, b_), max(a_, b_)))
        if len(pts) == 2 and np.linalg.norm(pts[0] - o) < R: segs.append((pts[0], pts[1], f)); keys.append(ks)
    # chain segments by shared edge keys into loops
    adj = {}
    for si, ks in enumerate(keys):
        for kk in ks: adj.setdefault(kk, []).append(si)
    seen = np.zeros(len(segs), bool); loops = []
    for s0 in range(len(segs)):
        if seen[s0]: continue
        comp = [s0]; seen[s0] = True; st = [s0]
        while st:
            x = st.pop()
            for kk in keys[x]:
                for y in adj[kk]:
                    if not seen[y]: seen[y] = True; comp.append(y); st.append(y)
        ends = [kk for x in comp for kk in keys[x] if len(adj[kk]) == 1]
        P = np.array([[(segs[x][0] - o) @ u, (segs[x][0] - o) @ v] for x in comp])
        # order points by walking
        order = [comp[0]]; used = {comp[0]}; cur = comp[0]; last = keys[cur][1]
        while True:
            nxt = [y for y in adj[last] if y not in used]
            if not nxt: break
            cur = nxt[0]; used.add(cur); order.append(cur); last = keys[cur][1] if keys[cur][0] == last else keys[cur][0]
        Pw = np.array([[(segs[x][0] - o) @ u, (segs[x][0] - o) @ v] for x in order])
        loops.append(dict(n=len(comp), closed=len(ends) == 0, pts=Pw, faces=[segs[x][2] for x in comp]))
    for i, L in enumerate(loops):
        L['depth'] = int(sum(Path(M['pts']).contains_point(L['pts'][0]) for j, M in enumerate(loops) if j != i and M['closed'] and len(M['pts']) > 3))
        L['area'] = float(area(L['pts'])) if L['closed'] else None
    ax = axs[k // cols][k % cols]
    for p0, p1, f in segs:
        q0 = [(p0 - o) @ u, (p0 - o) @ v]; q1 = [(p1 - o) @ u, (p1 - o) @ v]
        ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color=COL[lab[f]] if lab is not None else '0.15', lw=1.1)
    for L in loops:
        if L['depth'] > 0: c = L['pts'].mean(0); ax.text(c[0], c[1], 'd%d' % L['depth'], color='m', fontsize=8)
    ax.set_aspect('equal'); ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.grid(alpha=.3); ax.set_title('%s  n=%s' % (name, np.round(n, 2).tolist()), fontsize=8)
    ax.text(-R * .95, -R * .93, 'u=%s v=%s' % (np.round(u, 2).tolist(), np.round(v, 2).tolist()), fontsize=6)
    res.append(dict(plane=name, origin=o.tolist(), normal=n.tolist(), R=R, loops=[dict(segments=L['n'], closed=L['closed'], depth=L['depth'], area_cm2=None if L['area'] is None else round(L['area'], 2)) for L in loops]))
for k in range(n_, rows * cols): axs[k // cols][k % cols].axis('off')
plt.tight_layout(); plt.savefig(a.out + '.png', dpi=110); json.dump(res, open(a.out + '.json', 'w'), indent=1)
for r in res: print(r['plane'], [(l['segments'], l['closed'], l['depth'], l['area_cm2']) for l in r['loops'] if l['segments'] > 3])
