# cg_def_sum.py OUT.json REF_TAG:REF_DIR CAND_TAG:CAND_DIR ID... : RP4 Cogling deformation classification (order 9424c72 §18). Per body and pose, the candidate
# (e.g. the v005 realization, or the Cogling branch realization) against the reference run of the same body (native hm08 source, or the v005 realization)
# on mf_deform metrics: new self-intersecting pairs, new folds (> 120 deg), flipped faces, joint-zone strain p95 / max, zone volume.
#   identical      : every metric equal;
#   same class     : no metric class appears that the reference does not have (a count may differ: e.g. finer faces counting the same contact more times);
#   NEW CLASS      : self-intersection, fold or flip appears where the reference has none (a topology-class failure) -- EXCEPT new self-intersection pairs that
#                    are all arm <-> trunk faces (the axillary arm / torso contact of the R-6 stance under trunk twist, present on the c2 native and the
#                    Pipkin natives): classed 'same class (axillary arm-trunk contact)'. Zones from the candidate's audit loops npz (ZONES_DIR/<id>_<tag>_loops.npz).
import sys, os, json, numpy as np
OUT = sys.argv[1]; (rt, rd), (ct, cd) = [a.split(':') for a in sys.argv[2:4]]; ids = sys.argv[4:]
K = ('new_selfx_pairs', 'new_folds', 'flipped_faces')
res = {}; tagc = None
for i in ids:
    a = json.load(open('%s/deform_%s_%s.json' % (rd, i, rt)))['poses']; b = json.load(open('%s/deform_%s_%s.json' % (cd, i, ct)))['poses']; rows = {}
    for p in a:
        if p not in b: continue
        x, y = a[p], b[p]; same = all(x[k] == y[k] for k in K) and abs(x['strain_p95_pct'] - y['strain_p95_pct']) < 1e-9 and abs(x['strain_max_pct'] - y['strain_max_pct']) < 1e-9
        new = [k for k in K if y[k] > 0 and x[k] == 0]
        if new == ['new_selfx_pairs']:
            zp = os.environ.get('ZONES_DIR', '') + '/%s_%s_loops.npz' % (i, ct); pp = '%s/%s_%s_%s.npz' % (cd, p, i, ct)
            if os.path.exists(zp) and os.path.exists(pp):
                zone = np.load(zp, allow_pickle=True)['zone'].astype(str); Qc = np.asarray(np.load(os.environ['FACES_' + ct] % i)['Q']); sx = np.load(pp)['selfx']
                if len(sx) and all({zone[Qc[a][0]], zone[Qc[b][0]]} == {'arm', 'trunk'} for a, b in sx.tolist()): new = []; same = False; tagc = 'same class (axillary arm-trunk contact)'
        cls = 'identical' if same else ('NEW CLASS: ' + ', '.join(new) if new else (locals().get('tagc') or 'same class'))
        tagc = None
        rows[p] = dict(cls=cls, ref={k: x[k] for k in K + ('strain_p95_pct', 'strain_max_pct', 'zone_volume_pct')}, cand={k: y[k] for k in K + ('strain_p95_pct', 'strain_max_pct', 'zone_volume_pct')})
    n = len(rows); res[i] = dict(poses=n, identical=sum(r['cls'] == 'identical' for r in rows.values()), same_class=sum(r['cls'].startswith('same class') for r in rows.values()),
                                 new_class=[p for p, r in rows.items() if r['cls'].startswith('NEW')], rows=rows)
    print(i, '%s vs %s: %d poses, identical %d, same class %d, NEW %s' % (ct, rt, n, res[i]['identical'], res[i]['same_class'], res[i]['new_class']))
    for p, r in rows.items():
        if r['cls'] != 'identical': print('   %-20s %-22s ref %s  cand %s' % (p, r['cls'], [r['ref'][k] for k in K] + [r['ref']['strain_p95_pct']], [r['cand'][k] for k in K] + [r['cand']['strain_p95_pct']]))
json.dump(dict(reference=rt, candidate=ct, bodies=res), open(OUT, 'w'), indent=1)
