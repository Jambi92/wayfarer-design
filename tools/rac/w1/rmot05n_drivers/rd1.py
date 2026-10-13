# RAC RM-OT-05N: GO-RD1-REF surgical sculpt on the recovered Rodin source (F1 -> GO-RD0-SOURCE).
# Every edit is a named, region-limited operation on the source's own surface field (occupancy -> signed distance, cm).
# Zones that are reconstructed (not the source surface) are listed in RECON and reported in the gate.
import sys, json; sys.path.insert(0, D := '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd')
from field import *
from scipy import ndimage as ndi
from skimage.morphology import convex_hull_image
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05l_drivers'); from l_clay import smin, ellipsoid, cone
P = json.load(open(sys.argv[1])); OUT = sys.argv[2]
d = np.load(D + '/O0.npz'); O = d['O'].copy(); lo = d['lo']; h = float(d['h']); xs, ys, zs = coords(O.shape, lo, h)
X2, Y2 = np.meshgrid(xs, ys, indexing='ij'); log = []
def kz(z): return int(round((z - lo[2]) / h))
def open2(s, r):
    e = ndi.distance_transform_edt(s) * h > r; return (ndi.distance_transform_edt(~e) * h <= r) & s
def sd2(s): return (ndi.distance_transform_edt(~s) - ndi.distance_transform_edt(s)) * h
# ---- 1. clothing / hair-lock removal on the source sections (2D, per slice); arms split off in the pelvis/trunk slab ----
OA = np.zeros_like(O); sa, sb = P['arm_slab']
for k, z in enumerate(zs):
    s = O[:, :, k]
    if sa <= z <= sb:
        L, n = ndi.label(s); core = np.zeros_like(s)
        for i in range(1, n + 1):
            m = L == i
            if np.abs(X2[m]).min() < 25: core |= m
        OA[:, :, k] = s & ~core; s = core
    if 55 <= z < P['crotch']:                            # legs: loincloth panels and the central hanging mass
        c = s & ((np.abs(X2) >= P['slit']) | (z > P['slit_top'])); c = ndi.binary_fill_holes(open2(c, P['open_knee'] if z < P['knee_top'] else P['open_leg']))
        L2, n2 = ndi.label(c); a = ndi.sum(c, L2, range(1, n2 + 1)) * h * h; c = np.isin(L2, 1 + np.where(a > 150)[0])
        L3, n3 = ndi.label(c); new = np.zeros_like(c); hb = P['hull_leg']
        for i in range(1, n3 + 1):                       # muscle-definition reduction: pull each thigh section toward its hull
            m = L3 == i
            if X2[m].min() < 0 < X2[m].max(): new |= m; continue     # joined across the midline: left to the pelvis opening
            H = convex_hull_image(m); new |= ((1 - hb) * sd2(m) + hb * sd2(H)) < 0
        s = new
    elif sb < z <= P['neck_cut'] or (P['belt'][1] <= z <= sb):   # necklace, chest braids, back braid, mane locks
        c = ndi.binary_fill_holes(open2(s, P['open_chest']))
        if z > P['mane_z0']: c &= ~((Y2 < P['mane_y'] + (z - P['mane_z0']) * P['mane_slope']) & (np.abs(X2) < P['mane_x']))   # mane mass behind the nape (restored with the head in the organism)
        L2, n2 = ndi.label(c); a = ndi.sum(c, L2, range(1, n2 + 1)) * h * h; s = np.isin(L2, 1 + np.where(a > 60)[0])
    O[:, :, k] = s
log.append('section cleanup: loincloth panels + central mass z55-%g; necklace/braids/back braid/mane locks z%g-%g' % (P['crotch'], P['belt'][1], P['neck_cut']))
SA = sdf(OA, h)
# ---- 2. pelvis + belt zone: the loincloth skirt, tassel ring, pouches and panels are fused over the hips. They are thinner than
#      the body's own masses, so a large-radius 3D opening of the trunk core removes them and leaves the source's hip / buttock /
#      abdomen bulk; the belt rings (not thin) are then relaxed along z.
ka, kb = kz(P['pelvis'][0]), kz(P['pelvis'][1])
C = O.copy(); C[:, :, :kz(P['pelvis'][0] - 20)] = False; C[:, :, kz(P['pelvis'][1] + 20):] = False   # margin so the cut ends do not erode the zone
r = P['pelvis_open']; E = ndi.distance_transform_edt(C) * h > r; Cop = (ndi.distance_transform_edt(~E) * h <= r)
for k in range(ka, kb + 1): Cop[:, :, k] = ndi.binary_fill_holes(Cop[:, :, k])
w = np.clip(np.minimum(zs - P['pelvis'][0], P['pelvis'][1] - zs) / P['pelvis_feather'], 0, 1)   # feather into the source
SO = sdf(O, h); SC = sdf(Cop, h)
S = SO * (1 - w)[None, None, :] + SC * w[None, None, :]
for (z0, z1, sig) in P['zrelax']:
    Sz = ndi.gaussian_filter1d(S, sig / h, axis=2); t = np.clip(np.minimum(zs - z0, z1 - zs) / (2.5 * sig), 0, 1); t = (t * t * (3 - 2 * t))[None, None, :]
    S = S * (1 - t) + Sz * t
log.append('pelvis zone z%g-%g: 3D opening r=%g cm (removes skirt/tassels/pouches/panels), z-relaxation %s (belt rings)' % (P['pelvis'][0], P['pelvis'][1], r, P['zrelax']))
for (name, (x0, x1, y0, y1, z0, z1), r) in P['local_open']:      # pendants / remnants: local 3D opening, feathered
    box = lambda X_, lo_, hi_: np.clip(np.minimum(X_ - lo_, hi_ - X_) / 3.0, 0, 1)
    wv = box(np.abs(X2), x0, x1)[:, :, None] * box(Y2, y0, y1)[:, :, None] * box(zs, z0, z1)[None, None, :]
    OO = S < 0; E_ = ndi.distance_transform_edt(OO) * h > r; Sop = sdf(ndi.distance_transform_edt(~E_) * h <= r, h)
    S = S * (1 - wv) + np.maximum(S, Sop) * wv; log.append('local opening %s r=%g' % (name, r))
# ---- 3. transition volume (lower thorax into the reconstructed trunk) ----
Z3 = zs[None, None, :]; X3 = X2[:, :, None]; Y3 = Y2[:, :, None]
def bump(z, z0, z1, zp):
    return np.clip(np.where(z < zp, (z - z0) / (zp - z0), (z1 - z) / (z1 - zp)), 0, 1)
ang = np.arctan2(Y3, np.abs(X3) + 1e-6)
for (z0, zp, z1, lat, ant, post) in P['trunk']:
    w = bump(Z3, z0, z1, zp); w = w * w * (3 - 2 * w)
    dirw = np.where(ang > 0, lat + (ant - lat) * np.sin(ang) ** 2, lat + (post - lat) * np.sin(ang) ** 2)
    S -= w * dirw * (np.abs(X3) < 30)
log.append('transition volume %s' % P['trunk'])
if P.get('arm_clear'):                                  # RD2: trunk yields where the hanging arm lies against it (no arm-trunk web)
    S = np.maximum(S, P['arm_clear'] - SA); log.append('trunk cleared %.1f cm from the arm' % P['arm_clear'])
S = np.minimum(S, SA)
# ---- 3b. arm bands and bracers: relax the arm field along the (near-vertical) limb axis; hands excluded ----
za, zb2, sig = P['arm_relax']; ka2, kb2 = kz(za), kz(zb2)
Sz = ndi.gaussian_filter1d(S[:, :, ka2 - 20:kb2 + 21], sig / h, axis=2)[:, :, 20:-20]
t = np.clip(np.minimum(zs[ka2:kb2 + 1] - za, zb2 - zs[ka2:kb2 + 1]) / 4.0, 0, 1)[None, None, :]
am = np.clip((np.abs(X2) - P['arm_x']) / 3.0, 0, 1)[:, :, None]
S[:, :, ka2:kb2 + 1] = S[:, :, ka2:kb2 + 1] * (1 - t * am) + Sz * t * am
log.append('arm bands / bracers relaxed along the limb axis z%g-%g (|X|>%g)' % (za, zb2, P['arm_x']))
# ---- 3c. muscle-definition reduction: blend toward a broad-smoothed field (named regions) ----
S_pre = S.copy(); Sb = ndi.gaussian_filter(S, P['msmooth_sigma'] / h)
for name, (z0, z1, x0, x1, amt) in P['msmooth'].items():
    wz = np.clip(np.minimum(zs - z0, z1 - zs) / 5.0, 0, 1)[None, None, :]
    wx = np.clip(np.minimum(np.abs(X2) - x0, x1 - np.abs(X2)) / 3.0, 0, 1)[:, :, None]
    S = S * (1 - amt * wz * wx) + Sb * amt * wz * wx; log.append('muscle smoothing %s %.2f' % (name, amt))
x0, x1, z0, z1, gm = P['gap_guard']            # keep the arm-trunk gap open (smoothing must not web the arm to the trunk)
gbox = ((np.abs(X2) > x0) & (np.abs(X2) < x1))[:, :, None] & ((zs > z0) & (zs < z1))[None, None, :]
S = np.where(gbox & (S_pre > gm), np.maximum(S, S_pre - gm), S); del S_pre
log.append('arm-trunk gap guard')
# ---- 4. muscle reduction: deflate named masses ----
for name, c, r, amt in P['deflate']:
    for sx in (1, -1):
        cc = np.array(c, float) * [sx, 1, 1]; q = np.sqrt(((X3 - cc[0]) / r[0]) ** 2 + ((Y3 - cc[1]) / r[1]) ** 2 + ((Z3 - cc[2]) / r[2]) ** 2)
        w = np.clip(1 - q, 0, 1); S += amt * w * w * (3 - 2 * w)
    log.append('deflate %s %.1f cm' % (name, amt))
# ---- 5. shank wraps and foot strap removed; foot proportion corrected (source plantigrade five-toed foot kept) ----
F = P['foot']
z0, z1, sig = F['wrap_relax']; k0, k1 = kz(z0), kz(z1)
Sz = ndi.gaussian_filter1d(S[:, :, max(k0 - 20, 0):k1 + 21], sig / h, axis=2)
off = k0 - max(k0 - 20, 0); Sz = Sz[:, :, off:off + (k1 - k0 + 1)]
t = np.clip(np.minimum(zs[k0:k1 + 1] - z0, z1 - zs[k0:k1 + 1]) / 4.0, 0, 1)[None, None, :]
S[:, :, k0:k1 + 1] = S[:, :, k0:k1 + 1] * (1 - t) + Sz * t
log.append('shank wraps relaxed along the shank z%g-%g' % (z0, z1))
kk = kz(F['strap_z'][1]); Sb3 = ndi.gaussian_filter(S[:, :, :kk + 10], F['strap_sigma'] / h)[:, :, :kk + 1]
up = np.clip((zs[:kk + 1] - F['strap_z'][0]) / 3.0, 0, 1)[None, None, :]       # keep the plantar surface crisp
S[:, :, :kk + 1] = S[:, :, :kk + 1] * (1 - up) + Sb3 * up; log.append('foot strap smoothed z%g-%g' % tuple(F['strap_z']))
# foot length: resample the foot field about the ankle axis (forefoot and heel scaled separately in Y, breadth in X)
from scipy.ndimage import map_coordinates
kf = kz(F['warp_top']); ax_, ay_ = F['ankle_c']
Xg, Yg, Zg = np.meshgrid(xs, ys, zs[:kf + 1], indexing='ij')
wz = np.clip((F['warp_top'] - Zg) / (F['warp_top'] - F['warp_full']), 0, 1); wz = wz * wz * (3 - 2 * wz)
sf = 1 + (F['fore_s'] - 1) * wz; sh_ = 1 + (F['heel_s'] - 1) * wz; sx = 1 + (F['breadth_s'] - 1) * wz
yy = Yg - ay_; Ysrc = ay_ + np.where(yy > 0, yy / sf, yy / sh_)
xa = np.abs(Xg) - ax_; Xsrc = np.sign(Xg) * (ax_ + xa / sx)
idx = [(Xsrc - lo[0]) / h, (Ysrc - lo[1]) / h, (Zg - lo[2]) / h]
S[:, :, :kf + 1] = map_coordinates(S, idx, order=1, mode='nearest').reshape(Xg.shape)
log.append('foot length/breadth corrected: forefoot x%.2f, heel x%.2f, breadth x%.2f about ankle axis (%g, %g)' % (F['fore_s'], F['heel_s'], F['breadth_s'], ax_, ay_))
for (name, (x0, x1, y0, y1, z0, z1), r) in P['local_close']:     # cavities / folds: local 3D closing, feathered
    box = lambda X_, lo_, hi_: np.clip(np.minimum(X_ - lo_, hi_ - X_) / 3.0, 0, 1)
    wv = box(np.abs(X2), x0, x1)[:, :, None] * box(Y2, y0, y1)[:, :, None] * box(zs, z0, z1)[None, None, :]
    D_ = ndi.distance_transform_edt(~(S < 0)) * h <= r; Scl = sdf(~(ndi.distance_transform_edt(~(~D_)) * h <= r), h)
    S = S * (1 - wv) + np.minimum(S, Scl) * wv; log.append('local closing %s r=%g' % (name, r))
# ---- 6. surface relaxation: soften muscle relief, remove voxel steps ----
S = ndi.gaussian_filter(S, P['blur'] / h)
np.savez_compressed(OUT + '.npz', S=S.astype(np.float32), lo=lo, h=h)
m = mesh(S, lo, h, OUT + '_raw.obj'); print(m.bounds.round(1), m.is_watertight, len(m.faces))
json.dump(dict(params=P, log=log), open(OUT + '_log.json', 'w'), indent=1)
