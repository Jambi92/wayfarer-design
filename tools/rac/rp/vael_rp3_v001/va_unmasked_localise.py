# va_unmasked_localise.py WORK OUT.json : Vael final §8 unmasked transparency run -- localise the unmasked anatomy.py exceedances (rule of the Aelari
# freeze, AELARI_unmasked_anatomy_localisation.json): surface deviation both directions restricted to points farther than 1.5 cm from every ear-branch
# vertex (and, for source points, outside w_ears > 0.05); must sit within the T-1 body limits.
import sys, json, numpy as np, trimesh
from scipy.spatial import cKDTree
W, OUT = sys.argv[1:3]; RA = '/home/claude/wayfarer-design/reviews/reference-assets'; T1 = dict(median_mm=0.5, p95_mm=1.5, max_mm=3.0); R = {}
st = lambda d: dict(max_mm=round(float(d.max() * 10), 4), p95_mm=round(float(np.percentile(d, 95) * 10), 4), median_mm=round(float(np.median(d) * 10), 4))
for h in ('VAL4-R1-VD2-VF2', 'VALF178-R1-VD2-VF2'):
    r6 = np.load('%s/r6/%s_r6.npz' % (RA, h)); cz = np.load('%s/ear/RI3/build/%s_VA-E2-RI3_branch.npz' % (W, h)); SV = r6['V'].astype(float); keep = r6['keep']; Vp = cz['V'].astype(float); Q = cz['Q']
    src = trimesh.Trimesh(SV, r6['F'], process=False); prod = trimesh.Trimesh(Vp, np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]], process=False); bs = SV[keep]
    _, d1, _ = trimesh.proximity.closest_point(src, Vp); _, d2, _ = trimesh.proximity.closest_point(prod, bs)
    ear = cKDTree(Vp[cz['part'] != 'v005']); o1 = ear.query(Vp)[0] > 1.5; o2 = (ear.query(bs)[0] > 1.5) & (r6['w_ears'][keep] <= 0.05)
    a, b = st(d1[o1]), st(d2[o2])
    R[h] = dict(rule='unmasked anatomy.py exceedances localised: points farther than 1.5 cm from every ear-branch vertex (and, for source points, outside w_ears > 0.05)',
                prod_to_source_outside_ear_region=a, source_to_prod_outside_ear_region=b, prod_to_source_overall_max_mm=round(float(d1.max() * 10), 3), T1_body_limits=T1,
                within_T1_body_limits_outside_ear=all(a[k] <= T1[k] and b[k] <= T1[k] for k in T1))
    print(h, a, b, R[h]['within_T1_body_limits_outside_ear'])
json.dump(R, open(OUT, 'w'), indent=1)
