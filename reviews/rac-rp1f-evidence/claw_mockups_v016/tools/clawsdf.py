# clawsdf.py IN.npz NAILS.json NAME OUTTARGET.npz : RP1F claw/sheath TARGET surface for one nail (production unchanged here)
#  body  = v014 production with the human nail-plate border relaxed away (bounded Taubin smoothing of the plate area)
#  claw  = laterally compressed, tapering keratin cone along a curved centreline that starts inside the fingertip under the sheath
#          and exits at the distal-dorsal tip with a mild downward hook
#  target= marching-cubes iso-surface of smin(body SDF, claw SDF, k) on a local grid -> the sheath fold is the smooth-union fillet
# The production patch is then remapped onto this target with remap.py (SRCMESH) — topology unchanged.
import sys, json, numpy as np, igl
from skimage.measure import marching_cubes
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
inp, nj, name, outp = sys.argv[1:5]
P = json.load(open(nj))[name]
z = np.load(inp); Q = z['Q'].astype(np.int64); F = z['F'].astype(np.int64)
fl = np.array([1, -1, 1]); V = z['V'].astype(float) * fl
def smooth01(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); vn = np.zeros_like(V)
for k in range(3): np.add.at(vn, F[:, k], fn)
vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-15
C = np.array(P['C']); T = np.array(P['T'])
near = np.where(np.linalg.norm(V - C, axis=1) < 0.25)[0]; n = vn[near].mean(0); n /= np.linalg.norm(n)
d = T - C; e1 = d - (d @ n) * n; L = np.linalg.norm(e1); e1 /= L; e2 = np.cross(n, e1)
# --- erase the nail border: Taubin smoothing over the plate area (dorsal, connected)
R0 = P.get('erase_r', 1.0)
reg = np.where((np.linalg.norm(V - C, axis=1) < max(R0, 1.35 * L + 0.15) + 0.5) & ((vn @ n) > -0.3))[0]
lm = -np.ones(len(V), int); lm[reg] = np.arange(len(reg)); qq = Q[(lm[Q] >= 0).all(1)]
ee = np.vstack([qq[:, [i, (i + 1) % 4]] for i in range(4)])
A = sp.coo_matrix((np.ones(len(ee)), (lm[ee[:, 0]], lm[ee[:, 1]])), shape=(len(reg), len(reg))).tocsr(); A.data[:] = 1
_, lab = connected_components(A, directed=False); keep = lab == lab[np.argmin(np.linalg.norm(V[reg] - C, axis=1))]
reg = reg[keep]; A = A[keep][:, keep]; deg = np.asarray(A.sum(1)).ravel()
X = V[reg] - C; s = X @ e1; u = X @ e2
rs = P.get('erase_rs', 1.35 * L + 0.15); ru = P.get('erase_ru', 0.75)
ell = np.sqrt((np.minimum(s, 0) / rs) ** 2 + (u / ru) ** 2)
we = smooth01((1 - ell) / 0.3) * smooth01((L + 0.08 - s) / 0.12)
Pm = V[reg].copy()
for it in range(P.get('erase_it', 40)):
    for lam in (0.5,):
        Lp = (A @ Pm) / np.maximum(deg, 1)[:, None] - Pm; Pm += lam * we[:, None] * Lp
Vb = V.copy(); Vb[reg] = Pm; print('erase region', len(reg), 'core', int((we>0.9).sum()), 'max erase move mm %.2f' % (np.linalg.norm(Pm - V[reg], axis=1).max() * 10))
# --- local grid
half = P.get('half', 0.9); h = P.get('h', 0.018)
c0 = T - P.get('c0back', 0.3) * e1
g = np.arange(-half, half + 1e-9, h); GX, GY, GZ = np.meshgrid(g, g, g, indexing='ij')
G = np.stack([GX.ravel(), GY.ravel(), GZ.ravel()], 1) + c0
fm = np.linalg.norm(Vb[F].mean(1) - c0, axis=1) < half * 1.8 + 0.8
Sb, _, _, _ = igl.signed_distance(G, Vb, F[fm])
if P.get('blur', 0) > 0:
    from scipy.ndimage import gaussian_filter
    Sg = gaussian_filter(Sb.reshape(GX.shape), P['blur'] / h).ravel()
    Xg = G - C; sg = Xg @ e1; ug = Xg @ e2; hg = Xg @ n
    ellg = np.sqrt((np.minimum(sg, 0) / P.get('erase_rs', 1.35 * L + 0.15)) ** 2 + (ug / P.get('erase_ru', 0.75)) ** 2)
    wg = smooth01((1 - ellg) / 0.3) * smooth01((L + 0.25 - sg) / 0.2)
    Sb = Sb * (1 - wg) + Sg * wg
# --- claw SDF: quadratic bezier centreline, elliptical section (lateral rl, dorso-ventral rn), radius tapering to the tip
Tdor = T + P.get('tip_lift', 0.0) * n
p0 = Tdor - P['root'] * e1 - P['depth'] * n            # inside the fingertip, under the sheath
p2 = Tdor + P['ext'] * e1 - P['hook'] * n              # exposed tip, hooked down
p1 = Tdor + 0.15 * P['ext'] * e1 + P['arch'] * n       # dorsal arch
ts = np.linspace(0, 1, 60); Cc = ((1 - ts) ** 2)[:, None] * p0 + (2 * (1 - ts) * ts)[:, None] * p1 + (ts ** 2)[:, None] * p2
from scipy.spatial import cKDTree
kd = cKDTree(Cc); _, j = kd.query(G); j = np.clip(j, 0, len(ts) - 1)
tan = np.gradient(Cc, axis=0); tan /= np.linalg.norm(tan, axis=1, keepdims=True)
D = G - Cc[j]; along = (D * tan[j]).sum(1); D = D - along[:, None] * tan[j]
bn = np.cross(tan, e2); bn /= np.linalg.norm(bn, axis=1, keepdims=True)
dl = D @ e2; dn = (D * bn[j]).sum(1)
tt = ts[j]; r = P['r0'] * (1 - tt) ** P.get('taper', 0.9) + P.get('rtip', 0.012)
rl = r * P.get('lat', 0.7); rn = r
q = np.sqrt((dl / rl) ** 2 + (dn / rn) ** 2); Sc = (q - 1) * np.minimum(rl, rn)
endcap = np.where(j == len(ts) - 1, np.maximum(along, 0), 0) + np.where(j == 0, np.maximum(-along, 0), 0); Sc = np.sqrt(np.maximum(Sc, 0) ** 2 + endcap ** 2) + np.minimum(Sc, 0)
k = P.get('k', 0.06)
hh = np.clip(0.5 + 0.5 * (Sc - Sb) / k, 0, 1); S = Sb * hh + Sc * (1 - hh) - k * hh * (1 - hh)
S = S.reshape(GX.shape)
vv, ff, _, _ = marching_cubes(S, 0.0, spacing=(h, h, h))
vv = vv + c0 - half
# keep the component nearest the tip (drop grid-boundary fragments)
from scipy.sparse.csgraph import connected_components as cc2
E2 = np.vstack([ff[:, [0, 1]], ff[:, [1, 2]], ff[:, [2, 0]]]); M2 = sp.coo_matrix((np.ones(len(E2)), (E2[:, 0], E2[:, 1])), shape=(len(vv), len(vv)))
_, l2 = cc2(M2, directed=False); best = l2[np.argmin(np.linalg.norm(vv - T, axis=1))]; fk = l2[ff[:, 0]] == best
ff = ff[fk]; used = np.unique(ff); rm = -np.ones(len(vv), int); rm[used] = np.arange(len(used)); vv = vv[used]; ff = rm[ff]
# marching_cubes orientation: make outward (normals agree with body normals nearby)
fnn = np.cross(vv[ff[:, 1]] - vv[ff[:, 0]], vv[ff[:, 2]] - vv[ff[:, 0]]); cen = vv[ff].mean(1)
_, I, _ = igl.point_mesh_squared_distance(cen[::50], Vb, F[fm]); ref = fn[fm][I]
if (np.einsum('ij,ij->i', fnn[::50], ref) < 0).mean() > 0.5: ff = ff[:, ::-1]
np.savez_compressed(outp, V=vv * fl, F=ff[:, ::-1].astype(np.int64))   # claw target (MC, local box), analysis frame
np.savez_compressed(outp.replace('.npz', '_erased.npz'), V=Vb * fl, F=F, Q=Q)   # production with the nail border relaxed away
json.dump(dict(name=name, C=C.round(3).tolist(), T=T.round(3).tolist(), n=n.round(3).tolist(), e1=e1.round(3).tolist(), e2=e2.round(3).tolist(),
               centreline=[p0.round(3).tolist(), p1.round(3).tolist(), p2.round(3).tolist()], params=P, target_vertices=int(len(vv))),
          open(outp.replace('.npz', '_info.json'), 'w'), indent=1)
print(name, 'target V', len(vv), 'F', len(ff))
