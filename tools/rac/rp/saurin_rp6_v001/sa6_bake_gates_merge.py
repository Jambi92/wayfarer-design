# sa6_bake_gates_merge.py NAME OUTDIR N : join the N shards GT_<NAME>.s<i>of<N>.json (sa6_bake_gates.py, env GATES_SHARD=i/N) into GT_<NAME>.json.
#   Poses are independent, so the merged file holds exactly the per-pose rows of an unsharded run, in the same pose order; totals and the clean rule are
#   recomputed from the rows exactly as sa6_bake_gates.run does.  Refuses unless every shard is present, agrees on pose set / artifact, and each pose appears once.
import sys, os, json
nm, OD, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
sh = [json.load(open(os.path.join(OD, 'GT_%s.s%dof%d.json' % (nm, i, n)))) for i in range(n)]; allp = sh[0]['all_poses']
assert all(s['all_poses'] == allp and s['artifact_sha256'] == sh[0]['artifact_sha256'] for s in sh), 'shards disagree on pose set / artifact'
rows = {}
for s in sh:
    for pn, v in s['poses'].items(): assert pn not in rows, 'pose in two shards: ' + pn; rows[pn] = v
assert set(rows) == set(allp), 'missing poses: %s' % sorted(set(allp) - set(rows))
out = {k: v for k, v in sh[0].items() if k not in ('poses', 'shard', 'shard_poses', 'totals', 'clean', 'seconds', 'peak_mb', 'resumed_poses')}
out['poses'] = {pn: rows[pn] for pn in allp}; out['sharded'] = '%d shards (GATES_SHARD), merged by sa6_bake_gates_merge.py' % n
out['seconds_per_shard'] = [s['seconds'] for s in sh]; out['peak_mb'] = max(s['peak_mb'] for s in sh)
tot = dict(rig_flips=0, rig_pen=0, rig_tears=0, vol_fail=0, comp=0, lbs_rig=0, rigid_max_cm=0.0, poses_with_K=0, k_max_cm=0.0)
for pn, rs in out['poses'].items():
    for row in rs.values():
        pr = row['bake']; tot['rig_flips'] += pr['rig_flips']; tot['rig_pen'] += pr['rig_pen']; tot['rig_tears'] += pr['rig_tears']; tot['vol_fail'] += int(not pr['volume_ok'])
        tot['comp'] += pr['composition']; tot['lbs_rig'] += row['lbs']['rig_flips']; tot['rigid_max_cm'] = max(tot['rigid_max_cm'], pr['rigid_max_cm'])
    kp = max(r['k_max_cm'] for r in rs.values()); tot['poses_with_K'] += int(kp > 0); tot['k_max_cm'] = max(tot['k_max_cm'], kp)
neutral = out['neutral_bake_max_displacement_cm']
out['totals'] = tot; out['clean'] = not (tot['rig_flips'] or tot['rig_pen'] or tot['rig_tears'] or tot['vol_fail'] or tot['rigid_max_cm'] > 0.05 or neutral > 0)
json.dump(out, open(os.path.join(OD, 'GT_%s.json' % nm), 'w'), indent=1)
for i in range(n): os.remove(os.path.join(OD, 'GT_%s.s%dof%d.json' % (nm, i, n)))
print(nm, 'GATES clean', out['clean'], 'poses', len(allp), '(merged %d shards)' % n, tot, flush=True)
