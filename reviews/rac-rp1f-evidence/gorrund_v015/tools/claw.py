# claw.py IN.npz OUT.npz NAILS.json : RP1F local feline claw/sheath treatment on the production mesh (blender cm in json; mesh in analysis frame)
# per nail: frame (n dorsal, e1 distal, e2 lateral) from C (plate centre) and T (free-edge apex);
#  1. lateral in-surface slide of the plate margins toward the midline (narrower keratin base), reprojected onto the original surface
#  2. dorsal keel ridge along the midline growing toward the tip (stronger dorsal taper)
#  3. sheath lip: small raised band around the claw root
#  4. tip: free-edge apex pulled distally with mild downward curl (modest pointed tip)
import sys, json, numpy as np, igl
inp, out, nj = sys.argv[1:4]
z = np.load(inp); V0 = z['V'].astype(float); Q = z['Q'].astype(np.int64); F = z['F'].astype(np.int64)
fl = np.array([1, -1, 1]); V = V0 * fl  # work in blender frame
Fb = F
nails = json.load(open(nj)); rep = {}
fn = np.cross(V[Fb[:, 1]] - V[Fb[:, 0]], V[Fb[:, 2]] - V[Fb[:, 0]]); vn = np.zeros_like(V)
for k in range(3): np.add.at(vn, Fb[:, k], fn)
vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-15
def smooth01(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
Vn = V.copy()
for nm, P in nails.items():
    C = np.array(P['C']); T = np.array(P['T']); W = P['W']
    near = np.where(np.linalg.norm(V - C, axis=1) < 0.25)[0]; n = vn[near].mean(0); n /= np.linalg.norm(n)
    if 'n' in P: n = np.array(P['n']) / np.linalg.norm(P['n'])
    d = T - C; e1 = d - (d @ n) * n; L = np.linalg.norm(e1); e1 /= L; e2 = np.cross(n, e1)
    Rr = max(1.8 * W, L + 0.6) + 0.3
    reg = np.where((np.linalg.norm(V - C, axis=1) < Rr) & ((vn @ n) > P.get('ncut', 0.0)))[0]
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    lm = -np.ones(len(V), int); lm[reg] = np.arange(len(reg)); qq = Q[(lm[Q] >= 0).all(1)]
    ee = np.vstack([qq[:, [i, (i + 1) % 4]] for i in range(4)]); A = sp.coo_matrix((np.ones(len(ee)), (lm[ee[:, 0]], lm[ee[:, 1]])), shape=(len(reg), len(reg)))
    _, lab = connected_components(A, directed=False); reg = reg[lab == lab[np.argmin(np.linalg.norm(V[reg] - C, axis=1))]]
    X = V[reg] - C; s = X @ e1; u = X @ e2
    sr = -P.get('root', L)                       # plate root (proximal) coordinate
    chi = smooth01((s - (sr - 0.35)) / 0.35) * smooth01((L + 0.25 - s) / 0.25)
    # 1 lateral slide
    au = np.abs(u); psi = np.where(au <= W, u / W, np.sign(u) * np.clip(1 - (au - W) / (0.6 * W), 0, 1))
    rootw = 0.6 + 0.4 * smooth01((L - s) / max(L - sr, 1e-6))          # stronger narrowing toward the base
    dl = -P['delta'] * psi * chi * rootw
    Y = V[reg] + dl[:, None] * e2
    fs = np.linalg.norm(V[Fb].mean(1) - C, axis=1) < Rr + 0.5
    _, _, cp = igl.point_mesh_squared_distance(Y, V, Fb[fs])
    nv = vn[reg]
    # 2 keel
    ramp = smooth01((s - sr) / max(L - sr, 1e-6))
    keel = P['keel'] * np.exp(-(u / (P.get('kw', 0.4) * W * (1 - P['delta'] / W))) ** 2) * ramp * chi
    # 3 sheath lip (root band + faint side bands)
    lip = P['lip'] * np.exp(-((s - sr) / 0.07) ** 2) * smooth01((1.15 * W - au) / (0.3 * W))
    # 4 tip
    g = np.exp(-(np.linalg.norm(V[reg] - T, axis=1) / P['rt']) ** 2) * np.clip((nv @ n) + 0.3, 0, 1)
    th = np.radians(P.get('curl_deg', 30))
    tipd = P['tip'] * g[:, None] * (np.cos(th) * e1 - np.sin(th) * n)[None, :]
    Vn[reg] = cp + (keel + lip)[:, None] * nv + tipd
    mv = np.linalg.norm(Vn[reg] - V[reg], axis=1)
    rep[nm] = dict(C=C.round(3).tolist(), T=T.round(3).tolist(), n=n.round(3).tolist(), e1=e1.round(3).tolist(), plate_halfwidth_cm=W, C_to_T_cm=round(float(L), 3),
                   region_vertices=int(len(reg)), moved_vertices=int((mv > 1e-5).sum()), max_move_mm=round(float(mv.max() * 10), 3), params=P)
    print(nm, 'region', len(reg), 'moved', int((mv > 1e-5).sum()), 'max mm %.2f' % (mv.max() * 10))
np.savez_compressed(out, V=Vn * fl, F=F, Q=Q); json.dump(rep, open(out.replace('.npz', '_claws.json'), 'w'), indent=1)
