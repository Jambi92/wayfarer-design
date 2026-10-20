# fit3.py IN.npz OUT.npz "x,y,z"(blender) R NIT : bounded chord-error fit — vertices are moved so that the vertex, edge-midpoint and
# face-centroid samples of the production quads lie on the frozen source (least-squares, Jacobi iterations); weight -> 0 at the rim.
import sys, numpy as np, igl
a = sys.argv[1:]; z = np.load(a[0]); V = z['V'].astype(float).copy(); Q = z['Q'].astype(np.int64)
c = np.array([float(x) for x in a[2].split(',')]) * np.array([1, -1, 1]); R = float(a[3]); NIT = int(a[4])
w = np.load('/home/claude/stc/rp1/weld_a.npz'); S = w['V'].astype(float); SF = w['F'].astype(np.int64)
SF = SF[np.linalg.norm(S[SF].mean(1) - c, axis=1) < R + 1.0]
d0 = np.linalg.norm(V - c, axis=1); reg = np.where(d0 < R)[0]; wt = np.clip((R - d0) / (0.3 * R), 0, 1)
Fz = z['F'].astype(np.int64); qs = Fz[(np.linalg.norm(V[Fz].mean(1) - c, axis=1) < R + 0.2)]
E = np.unique(np.sort(np.vstack([qs[:, [i, (i + 1) % 3]] for i in range(3)]), 1), axis=0)
def err():
    P = np.vstack([V[reg], V[qs].mean(1), V[E].mean(1)]); d, _, _ = igl.point_mesh_squared_distance(P, S, SF); d = np.sqrt(d) * 10; return d.max(), np.percentile(d, 95)
import os
LAP=float(os.environ.get('LAP',0))
Qq=Q[(np.linalg.norm(V[Q].mean(1)-c,axis=1)<R+0.2)]
nbs={}
for q in Qq:
    for i in range(4): nbs.setdefault(q[i],set()).update((q[i-1],q[(i+1)%4]))
rl=[v for v in reg if v in nbs]; rn=[list(nbs[v]) for v in rl]
print('start max %.2f p95 %.2f' % err())
for it in range(NIT):
    acc = np.zeros_like(V); cnt = np.zeros(len(V))
    _, _, cp = igl.point_mesh_squared_distance(V[reg], S, SF); acc[reg] += cp - V[reg]; cnt[reg] += 1
    fc = V[qs].mean(1); _, _, cf = igl.point_mesh_squared_distance(fc, S, SF); rf = cf - fc
    for k in range(3): np.add.at(acc, qs[:, k], rf); np.add.at(cnt, qs[:, k], 1)
    em = V[E].mean(1); _, _, ce = igl.point_mesh_squared_distance(em, S, SF); re = ce - em
    for k in range(2): np.add.at(acc, E[:, k], re); np.add.at(cnt, E[:, k], 1)
    m = cnt > 0; V[m] += 0.6 * wt[m, None] * acc[m] / cnt[m, None]
    if LAP>0:
        L=np.array([V[n].mean(0) for n in rn])-V[rl]; V[rl]+=LAP*wt[rl,None]*L
print('final max %.2f p95 %.2f' % err())
np.savez_compressed(a[1], V=V, F=z['F'], Q=z['Q'])
