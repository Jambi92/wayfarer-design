# deform_cmp_v5.py WORK OUT.json : order 33a2dfe §13 (native / v003 fit / v004 / v005); was deform_cmp_v4 (order a18371c §15) -- limited deformation sanity, native hm08 | frozen-v003 family fit | successor v004 on all four
# configurations (same LBS rig / weights through each map). A successor-caused topology-class failure would show as a v004 count above the v003 fit
# in the pose zones touched by the margin changes (hip flex, toe flex / ext, ankle) -- every other pose shares the v003 geometry outside the patches.
import sys, json
W, OUT = sys.argv[1:3]; R = '/tmp/claude-0/rt'
def ld(*ps):
    out = {}
    for p in ps:
        try: out.update(json.load(open(p))['poses'])
        except FileNotFoundError: pass
    return out
SRC = {'MF-M-R': ((R + '/m3/def/deform_MF-M-R_native.json', R + '/m3/v4/deform_MF-M-R_native_toe.json'), (R + '/m3/def/deform_MF-M-R_v003.json', R + '/m3/v4/deform_MF-M-R_v003_sanity.json')),
       'MF-F-R': ((R + '/m3/def/deform_MF-F-R_native.json', R + '/m3/v4/deform_MF-F-R_native_toe.json'), (R + '/m3/def/deform_MF-F-R_v003.json', R + '/m3/v4/deform_MF-F-R_v003_sanity.json')),
       'SK208-C1R': ((R + '/sk/def/deform_SK208-C1R_native.json',), (R + '/sk/def/deform_SK208-C1R_fam.json',)), 'SKF208': ((R + '/sk/def/deform_SKF208_native.json',), (R + '/sk/def/deform_SKF208_fam.json',))}
KEYS = ('flipped_faces', 'new_selfx_pairs', 'new_folds', 'zone_volume_pct')
res = {}; flags = []
for cid, (nat, v3) in SRC.items():
    n = ld(*nat); a = ld(*v3); a4 = json.load(open('/tmp/claude-0/rt/v4/def/deform_%s_v004.json' % cid))['poses']; b = json.load(open('%s/def/deform_%s_v005.json' % (W, cid)))['poses']; res[cid] = {}
    for p in b:
        row = {k: dict(native=n.get(p, {}).get(k), v003=a.get(p, {}).get(k), v004=a4.get(p, {}).get(k), v005=b[p][k]) for k in KEYS}; res[cid][p] = row
        if p in a4:
            for k in ('flipped_faces', 'new_selfx_pairs', 'new_folds'):
                if b[p][k] > a4[p][k]: flags.append((cid, p, k, a4[p][k], b[p][k]))
json.dump(dict(poses=res, v005_above_v004=flags), open(OUT, 'w'), indent=1)
print('v005 count above v004:', flags)
for cid in res:
    print(cid, {p: (r['flipped_faces']['v004'], r['flipped_faces']['v005'], r['new_selfx_pairs']['v004'], r['new_selfx_pairs']['v005']) for p, r in res[cid].items() if p.startswith(('hip', 'toe', 'ankle', 'knee'))})
