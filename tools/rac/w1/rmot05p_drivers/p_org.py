# RM-OT-05P organism REVIEW presentation (not an acceptance asset): the provisional leonine mane-over-nape and the short
# curled tail study are taken UNCHANGED from the 05N organism (GO-RD2-ORG-REF minus GO-RD2-REF), carried by the trunk frame
# shift of the RD3b/RD4 lineage (+dz), and placed on the new body. The parts are written as a separate closed surface that
# overlaps the body by about 1 cm at the attachment (presentation only, no boolean fusion). Head and neck are the body's own.
# Usage: python3 p_org.py --org ORG_RD2.obj --ref RD2_REF.obj --body BODY.obj --dz 3.55 --out OUT.obj
import argparse, json, numpy as np, trimesh, igl
from scipy import ndimage as ndi
from skimage import measure
ap = argparse.ArgumentParser(); ap.add_argument('--org'); ap.add_argument('--ref'); ap.add_argument('--body'); ap.add_argument('--dz', type=float); ap.add_argument('--out'); ap.add_argument('--h', type=float, default=0.4); a = ap.parse_args()
ld = lambda f: (lambda m: (np.ascontiguousarray(m.vertices, float), np.ascontiguousarray(m.faces, np.int64)))(trimesh.load(f, process=False))
Vo, Fo = ld(a.org); Vr, Fr = ld(a.ref); h = a.h
lo = np.array([-45, -50, 60.0]); hi = np.array([45, 10, 215.0])           # posterior / nape region where the tail and mane lie
xs, ys, zs = (np.arange(lo[i], hi[i], h) for i in range(3)); G = np.stack(np.meshgrid(xs, ys, zs, indexing='ij'), -1).reshape(-1, 3)
Oo = (igl.fast_winding_number(Vo, Fo, G) > 0.5).reshape(len(xs), len(ys), len(zs)); Or = (igl.fast_winding_number(Vr, Fr, G) > 0.5).reshape(Oo.shape)
extra = Oo & ~ndi.binary_dilation(Or, iterations=1); L, n = ndi.label(extra); sz = ndi.sum(extra, L, range(1, n + 1))
keep = np.isin(L, 1 + np.where(sz * h ** 3 > 30)[0])                      # tail + mane pieces (drop slivers)
part = keep | (ndi.binary_dilation(keep, iterations=int(2.5 / h)) & Or)  # grow ~1 cm into the old body so the attachment overlaps
S = ndi.gaussian_filter((ndi.distance_transform_edt(~part) - ndi.distance_transform_edt(part)) * h, 0.5 / h)
v, f, _, _ = measure.marching_cubes(S, 0.0, spacing=(h, h, h)); v += lo; v[:, 2] += a.dz
P = trimesh.Trimesh(v, f[:, ::-1], process=True)
if P.volume < 0: P.invert()
B = trimesh.load(a.body, process=False); out = trimesh.util.concatenate([B, P]); out.export(a.out)
json.dump(dict(org=a.org, ref=a.ref, body=a.body, dz=a.dz, part_volume_L=round(P.volume / 1000, 2), part_components=int(len(P.split(only_watertight=False))), note='presentation overlay; tail and mane unchanged from 05N, provisional'), open(a.out.replace('.obj', '_record.json'), 'w'), indent=1)
print(a.out, round(P.volume / 1000, 2))
