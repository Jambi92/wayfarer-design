# python3 fit2.py IN.npz OUT.npz "cx,cy,cz"(blender cm) R NIT [EXCL1.npy,EXCL2.npy] [tol_mm]
# Final-resolution bounded two-way fit (order 913d0e4 s10 / ruling dc9d48f s10 direct final-resolution local fallback).
# Region = production vertices within R of the centre (weight falls to 0 over the outer 25% -> exact weld to the untouched mesh).
# Each iteration: (a) every region vertex is pulled toward its closest point on the frozen source (excluding explicit masks),
# (b) every source sample in the region farther than tol from the production surface pulls its nearest production vertex,
# (c) tangential Laplacian relaxation redistributes vertices.  Vertex positions only; topology unchanged.
import sys, numpy as np, igl
from scipy.spatial import cKDTree
a = sys.argv[1:]; inp, out = a[0], a[1]; c = np.array([float(x) for x in a[2].split(',')]) * np.array([1, -1, 1]); R = float(a[3]); NIT = int(a[4])
excl = [np.load(f) for f in a[5].split(',')] if len(a) > 5 and a[5] not in ('', '-') else []
tol = (float(a[6]) if len(a) > 6 else 0.5) / 10.0
AL = float(__import__('os').environ.get('AL', 0.5)); BE = float(__import__('os').environ.get('BE', 0.6)); GA = float(__import__('os').environ.get('GA', 0.5))
z = np.load(inp); V = z['V'].astype(float).copy(); Q = z['Q'].astype(np.int64); F = z['F']
w = np.load('/home/claude/stc/rp1/weld_a.npz'); S = w['V'].astype(float); SF = w['F'].astype(np.int64)
keep = np.ones(len(SF), bool)
for e in excl: keep[e] = False
SC = S[SF].mean(1); sreg = keep & (np.linalg.norm(SC - c, axis=1) < R * 1.15); SFr = SF[sreg]
sm = keep & (np.linalg.norm(SC - c, axis=1) < R * 0.9); samp = np.vstack([SC[sm], S[np.unique(SF[sm])]])
d0 = np.linalg.norm(V - c, axis=1); reg = np.where(d0 < R)[0]; wt = np.clip((R - d0[reg]) / (0.25 * R), 0, 1)
QC = np.linalg.norm(V[Q].mean(1) - c, axis=1); Qr = Q[QC < R + 0.3]
loc = -np.ones(len(V), np.int64); loc[reg] = np.arange(len(reg))
nb = [set() for _ in reg]
for q in Qr:
    for i in range(4):
        u = loc[q[i]]
        if u >= 0: nb[u].update((q[i - 1], q[(i + 1) % 4]))
nb = [np.array(sorted(s)) for s in nb]
Tr = np.vstack([Qr[:, [0, 1, 2]], Qr[:, [0, 2, 3]]])
def vnorm(P):
    fn = np.cross(P[Tr[:, 1]] - P[Tr[:, 0]], P[Tr[:, 2]] - P[Tr[:, 0]]); vn = np.zeros_like(P)
    for k in range(3): np.add.at(vn, Tr[:, k], fn)
    return vn / (np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12)
def report(tag):
    ds, _, _ = igl.point_mesh_squared_distance(samp, V, Tr); ds = np.sqrt(ds) * 10
    dp, _, _ = igl.point_mesh_squared_distance(V[reg], S, SFr); dp = np.sqrt(dp) * 10
    print('%s src->prod max %.2f p95 %.2f n>1.5 %d | prod->src max %.2f' % (tag, ds.max(), np.percentile(ds, 95), (ds > 1.5).sum(), dp.max()), flush=True)
report('start')
for it in range(NIT):
    P = V[reg]
    _, _, cp = igl.point_mesh_squared_distance(P, S, SFr)
    ds, _, _ = igl.point_mesh_squared_distance(samp, V, Tr); un = np.sqrt(ds) > tol
    pull = np.zeros_like(P); cnt = np.zeros(len(P))
    if un.any():
        _, j = cKDTree(P).query(samp[un]); np.add.at(pull, j, samp[un] - P[j]); np.add.at(cnt, j, 1)
    pull[cnt > 0] /= cnt[cnt > 0, None]
    D = AL * (cp - P) + BE * pull
    vn = vnorm(V)[reg]; L = np.array([V[n].mean(0) for n in nb]) - P; Lt = L - (L * vn).sum(1, keepdims=True) * vn
    D = D + GA * Lt * (cnt == 0)[:, None] + 0.2 * GA * L * (cnt > 0)[:, None]
    V[reg] = P + wt[:, None] * D
    if it % 10 == 9: report('it%d' % (it + 1))
# final settle: projection + light tangential relax
for it in range(5):
    P = V[reg]; _, _, cp = igl.point_mesh_squared_distance(P, S, SFr)
    vn = vnorm(V)[reg]; L = np.array([V[n].mean(0) for n in nb]) - P; Lt = L - (L * vn).sum(1, keepdims=True) * vn
    V[reg] = P + wt[:, None] * (0.8 * (cp - P) + 0.3 * Lt)
report('final')
mv = np.linalg.norm(V[reg] - z['V'][reg], axis=1) * 10; print('moved verts', int((mv > 1e-4).sum()), 'max move mm %.2f' % mv.max())
np.savez_compressed(out, V=V, F=F, Q=z['Q'])
