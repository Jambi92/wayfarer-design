# RAC RM-OT-05O §2: corrected REF/LOW section audit measured on the DELIVERED meshes (not the working fields).
#
# Axes: RAC body frame, cm, Z up (ground z = 0), +Y anterior, X lateral (body is bilaterally symmetric about X = 0).
# Method per station z:
#   1. exact inside test on a 0.25 cm XY grid (fast generalized winding number of the closed mesh, threshold 0.5);
#   2. connected components; trunk = component spanning X = 0. Where a hanging arm touches the trunk (no separate arm
#      component on each side), the slice is split by a marker watershed on its distance map: trunk marker at the
#      midline, arm markers at the arm centroids of the nearest slice where both arms are separate. The split follows
#      the contact neck. The method used is REPORTED per station ("method");
#   3. breadth = X extent, depth = Y extent, area, centroid; legs = component with centroid X > 5 below the crotch;
#      arm = component with centroid |X| > trunk half-breadth.
# No fixed X mask is used (the 05N audit's |X| < 29 cm mask clipped REF trunk breadth to 57.5 cm - see report).
# Usage: python3 o_sections.py --ref REF.obj --low LOW.obj --out OUTDIR [--tag NAME]
import argparse, json, os, numpy as np, igl, trimesh
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

STATIONS = [('thorax_axilla', 170, 'trunk'), ('thorax', 162, 'trunk'), ('lower_thorax', 155, 'trunk'), ('lower_trunk', 146, 'trunk'), ('waist', 138, 'trunk'), ('upper_pelvis', 125, 'trunk'),
            ('pelvis', 115, 'trunk'), ('thigh', 85, 'leg'), ('knee', 58, 'leg'), ('calf', 42, 'leg'), ('ankle', 20, 'leg'),
            ('upper_arm', 150, 'arm'), ('elbow', 140, 'arm'), ('forearm', 128, 'arm'), ('wrist', 114, 'arm')]
H = 0.25

def load(fn):
    m = trimesh.load(fn, process=False); return np.ascontiguousarray(m.vertices, float), np.ascontiguousarray(m.faces, np.int64)

def slice_occ(V, F, z, lo, hi):
    xs = np.arange(lo[0], hi[0], H); ys = np.arange(lo[1], hi[1], H); X, Y = np.meshgrid(xs, ys, indexing='ij')
    P = np.c_[X.ravel(), Y.ravel(), np.full(X.size, z)]
    return igl.fast_winding_number(V, F, P).reshape(X.shape) > 0.5, xs, ys

def opened(s, r):
    if r <= 0: return s
    e = ndi.distance_transform_edt(s) * H > r; return (ndi.distance_transform_edt(~e) * H <= r) & s

def parts(s, xs, ys):
    L, n = ndi.label(s); out = []
    for i in range(1, n + 1):
        w = np.where(L == i); x = xs[w[0]]; y = ys[w[1]]
        out.append(dict(mask=(L == i), x0=x.min(), x1=x.max() + H, y0=y.min(), y1=y.max() + H, cx=x.mean(), cy=y.mean(), area=len(x) * H * H))
    return out

def arm_centroids_near(V, F, z, lo, hi):
    """centroids of the two hanging arms at the nearest slice (searching below, then above) where both are separate"""
    for dz in list(np.arange(0, -30, -1.0)) + list(np.arange(1, 15, 1.0)):
        zz = z + dz; s, xs, ys = slice_occ(V, F, zz, lo, hi); ps = [p for p in parts(s, xs, ys) if p['area'] > 4]
        mid = [p for p in ps if p['x0'] < 0 < p['x1']]
        L = [p for p in ps if p['cx'] < -15 and p['x1'] < 0]; R_ = [p for p in ps if p['cx'] > 15 and p['x0'] > 0]
        if mid and L and R_:
            l = max(L, key=lambda p: p['area']); r = max(R_, key=lambda p: p['area'])
            return [(l['cx'], l['cy']), (r['cx'], r['cy'])], float(zz)
    return None, None

def measure(V, F, z, kind, lo, hi):
    from skimage.segmentation import watershed
    s, xs, ys = slice_occ(V, F, z, lo, hi); method = 'component'
    ps = [p for p in parts(s, xs, ys) if p['area'] > 4]; res = None
    if kind == 'leg':
        c = [p for p in ps if p['cx'] > 5]; res = max(c, key=lambda p: p['area']) if c else None
    else:
        mid = [p for p in ps if p['x0'] < 0 < p['x1']]; arms = [p for p in ps if not (p['x0'] < 0 < p['x1']) and abs(p['cx']) > 15]
        separate = bool(mid) and any(p['cx'] > 0 for p in arms) and any(p['cx'] < 0 for p in arms)
        if separate:
            res = max(mid, key=lambda p: p['area']) if kind == 'trunk' else max([p for p in arms if p['cx'] > 0], key=lambda p: p['area'])
        else:   # arm touching the trunk: marker watershed on the in-slice distance map (trunk marker at the midline,
                # arm markers at the arm centroids of the nearest slice where the arms are separate); boundary = the contact neck
            cents, zsep = arm_centroids_near(V, F, z, lo, hi)
            if cents is not None and mid:
                t = max(mid, key=lambda p: p['area']); mk = np.zeros(s.shape, int)
                def put(x, y, lab):
                    i = int(round((x - xs[0]) / H)); j = int(round((y - ys[0]) / H))
                    mk[max(i - 2, 0):i + 3, max(j - 2, 0):j + 3] = lab
                put(0.0, t['cy'], 1); put(*cents[0], 2); put(*cents[1], 3)
                lab = watershed(-ndi.distance_transform_edt(s), mk, mask=s); method = 'watershed_arm_markers_z%g' % zsep
                m = lab == (1 if kind == 'trunk' else 3)
                q = parts(m, xs, ys); res = max(q, key=lambda p: p['area']) if q else None
    if res is None: return None, s, xs, ys
    d = {k: round(float(res[k]), 2) for k in ('x0', 'x1', 'y0', 'y1', 'cx', 'cy', 'area')}
    d.update(breadth=round(float(res['x1'] - res['x0']), 2), depth=round(float(res['y1'] - res['y0']), 2), method=method, z=z)
    if kind == 'trunk':   # arm-independent: AP depth of the midline strip |X| <= 2 cm (anterior wall to posterior wall)
        col = s[np.abs(xs) <= 2.0].any(0); yy = ys[col]; d['midline_ap_depth'] = round(float(yy.max() - yy.min() + H), 2)
        d['arm_contact'] = method != 'component'
    d['_mask'] = res['mask']; return d, s, xs, ys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--ref', required=True); ap.add_argument('--low', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--tag', default='REF_LOW')
    ap.add_argument('--station_z', default=None, help='JSON {station: z} overriding the station heights (same anatomy in a moved frame)')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    zmap = json.load(open(a.station_z)) if a.station_z else {}
    M = {'REF': load(a.ref), 'LOW': load(a.low)}
    lo = np.minimum(M['REF'][0].min(0), M['LOW'][0].min(0)) - 2; hi = np.maximum(M['REF'][0].max(0), M['LOW'][0].max(0)) + 2
    R = {'axes': 'cm; Z up, ground z=0; +Y anterior; X lateral (+X body left); grid 0.25 cm; exact winding-number inside test',
         'inputs': {'REF': a.ref, 'LOW': a.low}, 'stations': {}}
    tiles = []
    for name, z, kind in STATIONS:
        z = zmap.get(name, z); row = {}; masks = {}
        for tag in ('REF', 'LOW'):
            d, s, xs, ys = measure(*M[tag], z, kind, lo, hi); masks[tag] = (d['_mask'] if d else None, s)
            if d: d.pop('_mask')
            row[tag] = d
        if row['REF'] and row['LOW']:
            for k in ('breadth', 'depth', 'area', 'midline_ap_depth'):
                if k not in row['REF']: continue
                row['d_' + k] = round(row['LOW'][k] - row['REF'][k], 2); row['pct_' + k] = round(100 * (row['LOW'][k] - row['REF'][k]) / row['REF'][k], 1)
        R['stations'][name] = dict(kind=kind, **row)
        # overlay tile: grey = full slice (REF), outline red = REF measured region, blue = LOW measured region
        sR = masks['REF'][1]; img = np.full(sR.shape + (3,), 255, np.uint8); img[sR] = (215, 215, 215); img[masks['LOW'][1] & ~sR] = (190, 205, 235)
        for tag, col in (('REF', (200, 30, 30)), ('LOW', (30, 60, 200))):
            mk = masks[tag][0]
            if mk is not None: img[mk & ~ndi.binary_erosion(mk, iterations=2)] = col
        im = Image.fromarray(img.transpose(1, 0, 2)[::-1]); dr = ImageDraw.Draw(im)
        for g in range(-60, 61, 10):
            px = (g - lo[0]) / H; py = im.height - (g - lo[1]) / H
            dr.line([(px, 0), (px, im.height)], fill=(235, 235, 235) if g else (160, 160, 160)); dr.line([(0, py), (im.width, py)], fill=(235, 235, 235) if g else (160, 160, 160))
        dr.text((4, 4), '%s z=%g (%s) %s' % (name, z, kind, (row['REF'] or {}).get('method', '')), fill=(0, 0, 0))
        if row['REF'] and row['LOW']:
            dr.text((4, 18), 'REF b%.1f d%.1f  LOW b%.1f d%.1f' % (row['REF']['breadth'], row['REF']['depth'], row['LOW']['breadth'], row['LOW']['depth']), fill=(0, 0, 0))
        tiles.append(im)
    w, h = tiles[0].size; c = 4; S = Image.new('RGB', (w * c, h * ((len(tiles) + c - 1) // c)), 'white')
    for i, t in enumerate(tiles): S.paste(t, ((i % c) * w, (i // c) * h))
    S.save(os.path.join(a.out, '%s_section_overlays.png' % a.tag))
    R['volume_L'] = {t: round(trimesh.Trimesh(*M[t], process=False).volume / 1000, 1) for t in M}
    json.dump(R, open(os.path.join(a.out, '%s_sections.json' % a.tag), 'w'), indent=1)
    print('station        kind   REF b/d/area            LOW b/d/area            d_breadth  d_depth  d_area(%)   method REF/LOW')
    for n, r in R['stations'].items():
        if r.get('REF') and r.get('LOW'):
            md = ('  midAP %.1f/%.1f' % (r['REF']['midline_ap_depth'], r['LOW']['midline_ap_depth'])) if 'midline_ap_depth' in r['REF'] else ''
            print(md.join(['', '']) if False else '', end='')
            print('%-14s %-5s %5.1f/%5.1f/%6.0f  %5.1f/%5.1f/%6.0f  %+6.1f   %+6.1f  %+7.0f (%+5.1f%%)  %s/%s' % (n, r['kind'], r['REF']['breadth'], r['REF']['depth'], r['REF']['area'], r['LOW']['breadth'], r['LOW']['depth'], r['LOW']['area'], r['d_breadth'], r['d_depth'], r['d_area'], r['pct_area'], r['REF']['method'], r['LOW']['method']) + md)
        else: print(n, 'missing', r)
    print('volume', R['volume_L'])

if __name__ == '__main__': main()
