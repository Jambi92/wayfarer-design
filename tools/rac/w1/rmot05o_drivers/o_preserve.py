# RAC RM-OT-05O §2: preservation audit REF -> LOW measured on the delivered meshes, kept distinct from the edit design.
#  (a) EDIT DESIGN (not a measurement): the LOW recipe's tissue ellipsoids and protected regions (LOW params JSON);
#      reports the largest design offset that reaches each protected region.
#  (b) MEASURED: signed distance of every LOW vertex to the REF surface (igl), summarised inside each protected region
#      and each tissue region (median / 95th percentile / max |d|, cm; negative = LOW inside REF).
#  (c) MEASURED surface landmarks (proxies, not skeletal): stature (max z), crotch height (lowest z of the trunk bridge
#      at X=0), fingertip height (lowest z of the hand), acromion height (max z of the shoulder at |X| 26-34 cm),
#      knee section breadth at 58 cm, ankle breadth at 20 cm, wrist breadth at 114 cm (from o_sections).
# Usage: python3 o_preserve.py --ref REF.obj --low LOW.obj --params LOW_params.json --out OUT.json
import argparse, json, numpy as np, igl, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--ref'); ap.add_argument('--low'); ap.add_argument('--params'); ap.add_argument('--out'); a = ap.parse_args()
def ld(f):
    m = trimesh.load(f, process=False); return np.ascontiguousarray(m.vertices, float), np.ascontiguousarray(m.faces, np.int64)
VR, FR = ld(a.ref); VL, FL = ld(a.low); P = json.load(open(a.params))
d = igl.signed_distance(VL, VR, FR)[0]
def inside(V, c, r, mirror=True):
    m = np.zeros(len(V), bool)
    for sx in ((1, -1) if mirror else (1,)):
        q = ((V[:, 0] - c[0] * sx) / r[0]) ** 2 + ((V[:, 1] - c[1]) / r[1]) ** 2 + ((V[:, 2] - c[2]) / r[2]) ** 2; m |= q <= 1
    return m
def summ(m):
    if not m.any(): return None
    x = np.abs(d[m]); return dict(n=int(m.sum()), median=round(float(np.median(x)), 3), p95=round(float(np.percentile(x, 95)), 3), max=round(float(x.max()), 3), mean_signed=round(float(d[m].mean()), 3))
def design_reach(c, r):
    # largest tissue offset the LOW recipe applies at any point of this protected ellipsoid's surface sample
    u = np.random.default_rng(0).normal(size=(4000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    pts = np.array(c) + u * np.array(r) * np.random.default_rng(1).uniform(0, 1, (4000, 1)) ** (1 / 3); best = 0.0
    for name, tc, tr, amt, mir in P['tissue']:
        for sx in ((1, -1) if mir else (1,)):
            q = np.sqrt(((pts[:, 0] - tc[0] * sx) / tr[0]) ** 2 + ((pts[:, 1] - tc[1]) / tr[1]) ** 2 + ((pts[:, 2] - tc[2]) / tr[2]) ** 2)
            w = np.clip(1 - q, 0, 1); best = max(best, float((amt * w * w * (3 - 2 * w)).max()))
    return round(best, 3)
R = dict(method='signed distance of LOW vertices to the REF surface (cm); regions are the LOW recipe ellipsoids', protected={}, tissue={})
for name, c, r in P['protect']:
    R['protected'][name] = dict(measured=summ(inside(VL, c, r)), design_max_offset_reaching_region=design_reach(c, r))
for name, c, r, amt, mir in P['tissue']:
    R['tissue'][name] = dict(design_amount=amt, measured=summ(inside(VL, c, r, mir)))
def lm(V):
    out = dict(stature=round(float(V[:, 2].max()), 2))
    b = V[(np.abs(V[:, 0]) < 1.0) & (V[:, 2] > 80) & (V[:, 2] < 125)]
    # crotch: lowest midline surface point that has body above it (perineum)
    out['crotch_height'] = round(float(b[:, 2].min()), 2) if len(b) else None
    h = V[(np.abs(V[:, 0]) > 34) & (V[:, 2] > 80) & (V[:, 2] < 125)]; out['fingertip_height'] = round(float(h[:, 2].min()), 2) if len(h) else None
    s = V[(np.abs(V[:, 0]) > 26) & (np.abs(V[:, 0]) < 34) & (V[:, 2] > 170) & (V[:, 2] < 200)]; out['acromion_height_proxy'] = round(float(s[:, 2].max()), 2) if len(s) else None
    return out
R['landmarks'] = dict(REF=lm(VR), LOW=lm(VL))
R['landmarks']['delta'] = {k: (None if R['landmarks']['REF'][k] is None else round(R['landmarks']['LOW'][k] - R['landmarks']['REF'][k], 2)) for k in R['landmarks']['REF']}
json.dump(R, open(a.out, 'w'), indent=1)
print('PROTECTED (measured |d| median/p95/max cm; design offset reaching region)')
for k, v in R['protected'].items(): print('  %-28s %s  design %.2f' % (k, v['measured'] and (v['measured']['median'], v['measured']['p95'], v['measured']['max']), v['design_max_offset_reaching_region']))
print('TISSUE'); [print('  %-34s design %.2f measured %s' % (k, v['design_amount'], v['measured'] and (v['measured']['median'], v['measured']['p95'], v['measured']['max'], v['measured']['mean_signed']))) for k, v in R['tissue'].items()]
print('LANDMARKS', json.dumps(R['landmarks']))
