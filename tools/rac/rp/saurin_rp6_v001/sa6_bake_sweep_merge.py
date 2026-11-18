# sa6_bake_sweep_merge.py NAME OUTDIR N : join the N shards SW_<NAME>.s<i>of<N>.json written by sa6_bake_sweep.py (env SWEEP_SHARD=i/N) into SW_<NAME>.json.
#   Poses are independent, so the merged file holds exactly the per-pose rows an unsharded sweep writes, in the same pose order, with the same 'clean' rule.
#   Refuses to merge unless every shard is present, all shards list the same pose set and artifact, and every pose appears exactly once.
import sys, os, json
nm, OD, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
sh = [json.load(open(os.path.join(OD, 'SW_%s.s%dof%d.json' % (nm, i, n)))) for i in range(n)]
allp = sh[0]['all_poses']
assert all(s['all_poses'] == allp and s['artifact'] == sh[0]['artifact'] for s in sh), 'shards disagree on pose set / artifact'
rows = {}
for s in sh:
    for pn, v in s['poses'].items(): assert pn not in rows, 'pose in two shards: ' + pn; rows[pn] = v
assert set(rows) == set(allp), 'missing poses: %s' % sorted(set(allp) - set(rows))
out = {k: v for k, v in sh[0].items() if k not in ('poses', 'shard', 'shard_poses', 'all_poses')}
out['poses'] = {pn: rows[pn] for pn in allp}; out['sharded'] = '%d shards (SWEEP_SHARD), merged by sa6_bake_sweep_merge.py' % n
out['clean'] = all(not v['gate_failures'] and v['rigid_max_cm'] <= 0.05 for v in out['poses'].values())
json.dump(out, open(os.path.join(OD, 'SW_%s.json' % nm), 'w'), indent=1)
for i in range(n): os.remove(os.path.join(OD, 'SW_%s.s%dof%d.json' % (nm, i, n)))
print(nm, 'SWEEP clean', out['clean'], 'poses', len(allp), '(merged %d shards)' % n, flush=True)
