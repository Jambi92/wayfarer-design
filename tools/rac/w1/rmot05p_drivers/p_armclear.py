# RM-OT-05P stage C1: documented ARM POSE CLEARANCE (pose only, no tissue edit), field-based.
#  1. exact winding occupancy of the input mesh on a voxel grid (h cm);
#  2. 3-D marker watershed on the in-body distance map splits each arm from the trunk along the contact neck / axilla:
#     trunk marker = midline column z 105-185; arm markers = the arm centroid line measured on slices where the arm is
#     separate (both sides). Only the region below the shoulder band is re-posed;
#  3. each arm is rotated about the AP axis through the declared glenohumeral centre (abduction, angle deg), with the
#     rotation weight ramping from 0 at z_top to 1 at z_full (deltoid blend); segment lengths are rigid;
#  4. trunk and arm signed-distance fields are rebuilt; the arm field is resampled through the inverse rotation; the
#     cut faces left where the arm used to touch the trunk are relaxed by a local blur confined to the old contact zone;
#  5. union (smooth min, k cm) -> marching cubes -> decimation back to the input face count.
# Usage: python3 p_armclear.py --in IN.obj --out OUT.obj --shoulder 29 -1 184 --deg 5 [--h 0.4 --z_top 186 --z_full 170]
import argparse, json, sys, os, numpy as np, trimesh, igl
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage import measure
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--out'); ap.add_argument('--shoulder', type=float, nargs=3)
ap.add_argument('--deg', type=float, default=5.0); ap.add_argument('--h', type=float, default=0.4); ap.add_argument('--z_top', type=float, default=186.0)
ap.add_argument('--z_full', type=float, default=170.0); ap.add_argument('--k', type=float, default=0.8); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.ascontiguousarray(m.vertices, float); F = np.ascontiguousarray(m.faces, np.int64); h = a.h
lo = V.min(0) - 3; hi = V.max(0) + 3; lo[0] = -hi[0] - 6; hi[0] = -lo[0]       # symmetric in X with room for abduction
xs = np.arange(lo[0], hi[0], h); ys = np.arange(lo[1], hi[1], h); zs = np.arange(lo[2], hi[2], h)
X2, Y2 = np.meshgrid(xs, ys, indexing='ij'); O = np.zeros((len(xs), len(ys), len(zs)), bool)
for k in range(0, len(zs), 16):
    Z = zs[k:k + 16]; P = np.stack(np.broadcast_arrays(X2[..., None], Y2[..., None], Z[None, None, :]), -1).reshape(-1, 3)
    O[:, :, k:k + 16] = igl.fast_winding_number(V, F, P).reshape(len(xs), len(ys), len(Z)) > 0.5
kz = lambda z: int(round((z - zs[0]) / h)); kx = lambda x: int(round((x - xs[0]) / h)); ky = lambda y: int(round((y - ys[0]) / h))
def sdf(M): return ((ndi.distance_transform_edt(~M) - ndi.distance_transform_edt(M)) * h).astype(np.float32)
S = sdf(O)                                                     # full-body field (untouched outside the arm box)
# exact signed distance in a narrow band around the surface (removes voxel stair-stepping from the remesh)
band = np.abs(S) < 1.6; Pb = np.stack([xs[np.where(band)[0]], ys[np.where(band)[1]], zs[np.where(band)[2]]], -1)
S[band] = igl.signed_distance(Pb, V, F)[0].astype(np.float32); del Pb, band
b0, b1 = kz(92.0), min(kz(a.z_top + 8), len(zs))               # all re-posing work happens inside this z box
Ob = O[:, :, b0:b1]; zb = zs[b0:b1]
cents = {}
for z in np.arange(118, 158, 2.0):
    s_ = O[:, :, kz(z)]; L, n = ndi.label(s_)
    for i in range(1, n + 1):
        w_ = np.where(L == i); x = xs[w_[0]]
        if x.min() > 15 and len(x) * h * h > 40: cents.setdefault(z, []).append((x.mean(), ys[w_[1]].mean()))
ztop_c = max(cents); cx_t, cy_t = max(cents[ztop_c], key=lambda c: c[0]); sx0, sy0, sz0 = a.shoulder
for f in np.linspace(0, 1, 24):                                 # upper-arm axis: top separated centroid -> 8 cm below the shoulder centre
    cents.setdefault(round(ztop_c + f * (sz0 - 8 - ztop_c), 2), []).append((cx_t + f * (sx0 + 3 - cx_t), cy_t + f * (sy0 - cy_t)))
mk = np.zeros(Ob.shape, np.int32)
for z in np.arange(105, min(186, zb[-1]), 1.0): mk[kx(-1):kx(1) + 1, ky(-1):ky(3) + 1, kz(z) - b0] = 1
for z, cl in cents.items():
    for cx, cy in cl:
        for sgn, lab_ in ((1, 2), (-1, 3)):
            mk[kx(sgn * cx) - 1:kx(sgn * cx) + 2, ky(cy) - 1:ky(cy) + 2, kz(z) - b0] = lab_
lab = watershed(-ndi.distance_transform_edt(Ob).astype(np.float32), mk, mask=Ob); del mk
arm = (lab == 2) | (lab == 3); trunk = Ob & ~arm
# label every grid voxel by its nearest body voxel, so the arm / trunk split is a partition of space; the part fields are
# the exact body field intersected with that partition (cut faces only where the arm touched the trunk)
idx = ndi.distance_transform_edt(~Ob, return_distances=False, return_indices=True)
lab_all = lab[idx[0], idx[1], idx[2]]; del idx, lab
Ra = (lab_all == 2) | (lab_all == 3); del lab_all
Sb = S[:, :, b0:b1]; Sa = np.maximum(Sb, sdf(Ra)); St = np.maximum(Sb, sdf(~Ra)); del Ra
sx, sy, sz = a.shoulder; t = np.radians(a.deg)
Xg, Yg, Zg = np.meshgrid(xs.astype(np.float32), ys.astype(np.float32), zb.astype(np.float32), indexing='ij')
w = np.clip((a.z_top - Zg) / (a.z_top - a.z_full), 0, 1); w = w * w * (3 - 2 * w); th = t * w; del w
qx = np.abs(Xg) - sx; qz = Zg - sz
ix = qx * np.cos(th) + qz * np.sin(th); iz = -qx * np.sin(th) + qz * np.cos(th); del qx, qz, th   # inverse of the abduction
from scipy.ndimage import map_coordinates
Sa2 = map_coordinates(Sa, [(np.sign(Xg) * (ix + sx) - xs[0]) / h, (Yg - ys[0]) / h, (iz + sz - zb[0]) / h], order=1, mode='nearest').astype(np.float32)
del ix, iz, Yg, Zg, Sa
contact = ndi.binary_dilation(arm, iterations=max(1, int(round(1.5 / h)))) & ndi.binary_dilation(trunk, iterations=max(1, int(round(1.5 / h))))
czone = ndi.binary_dilation(contact, iterations=int(round(3.0 / h))) & (np.abs(Xg) > 8); del Xg
St2 = np.where(czone, np.maximum(St, ndi.gaussian_filter(St, 1.6 / h)), St); del St
kk = a.k; hh = np.clip(0.5 + 0.5 * (Sa2 - St2) / kk, 0, 1); S[:, :, b0:b1] = Sa2 * (1 - hh) + St2 * hh - kk * hh * (1 - hh)
arm_n, contact_n = int(arm.sum()), int(contact.sum()); del Sa2, St2, hh, arm, trunk, czone, contact, O
vv, ff, _, _ = measure.marching_cubes(S, 0.0, spacing=(h, h, h)); vv += [xs[0], ys[0], zs[0]]
M = trimesh.Trimesh(vv, ff[:, ::-1], process=True)
if M.volume < 0: M.invert()
parts = M.split(only_watertight=False); M = max(parts, key=lambda p: len(p.faces))
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('b'); me.from_pydata(M.vertices.tolist(), [], M.faces.tolist()); me.update(); ob = bpy.data.objects.new('b', me)
bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
d = ob.modifiers.new('d', 'DECIMATE'); d.ratio = min(1.0, len(F) / len(M.faces)); bpy.ops.object.modifier_apply(modifier='d')
r = ob.modifiers.new('r', 'LAPLACIANSMOOTH'); r.iterations = 2; r.lambda_factor = 0.4; r.use_volume_preserve = True; bpy.ops.object.modifier_apply(modifier='r')
me = ob.data; me.calc_loop_triangles(); Vo = np.array([v.co[:] for v in me.vertices]); Fo = np.array([tt.vertices[:] for tt in me.loop_triangles])
Vo[:, 2] -= Vo[:, 2].min() - V[:, 2].min()
trimesh.Trimesh(Vo, Fo, process=False).export(a.out)
hand = lambda VV: VV[(np.abs(VV[:, 0]) > 30) & (VV[:, 2] > 90) & (VV[:, 2] < 130)]
rec = dict(input=a.inp, output=a.out, shoulder_centre=a.shoulder, abduction_deg=a.deg, blend=dict(z_top=a.z_top, z_full=a.z_full), voxel_cm=h, smooth_union_k=a.k,
           arm_voxels=arm_n, contact_voxels=contact_n, faces=[int(len(F)), int(len(Fo))],
           volume_L=[round(m.volume / 1000, 2), round(trimesh.Trimesh(Vo, Fo, process=False).volume / 1000, 2)],
           hand_lowest_z=[round(float(hand(V)[:, 2].min()), 2), round(float(hand(Vo)[:, 2].min()), 2)],
           hand_max_x=[round(float(np.abs(hand(V)[:, 0]).max()), 2), round(float(np.abs(hand(Vo)[:, 0]).max()), 2)],
           note='topology changes here (voxel remesh at %.2f cm); stage-C tissue edits and the LOW are built on this mesh' % h)
json.dump(rec, open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
