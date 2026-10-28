# run_ear_v002_head.sh HEAD WORK (env EAR_CAND, default E2; EAR_CF) : order 0d9c70b -- one v002 E2 realization with the deformation-aware guard: build -> 8-pose deformation check
# -> faces with a new posed contact / flip / root inversion, or a degenerate (twisted) rest face, are held at the untangled state (+1 ring; +2 rings
# from the third iteration) -> rebuild (at most 6 guard iterations; logged).
H=$1; W=$2; C=${EAR_CAND:-E2}; B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; CF=${EAR_CF:-/tmp/claude-0/rt/fn/cf}; cd $W; export EAR_TOPO=v002
FZ=$W/build/${H}_${C}_deform_guard.json; rm -f $FZ; echo '[]' > $FZ
for it in 0 1 2 3 4 5; do
  RINGS=1; [ $it -ge 2 ] && RINGS=2
  EAR_Q3_FREEZE_RINGS=$RINGS EAR_Q3_FREEZE=$FZ $B $T/ear_build.py $H $C build --canon canon_branch_topology.json > build/${H}_${C}.log 2>&1
  $B $T/ear_deform.py -- $CF/src/${H}_native.npz build/${H}_${C}_branch.npz deform/${H}_${C}_deform.json deform/${H}_${C} $CF/fam/${H}_fam.npz > deform/${H}_${C}.log 2>&1
  n=$(python3 - $FZ deform/${H}_${C}_deform.json $it build/${H}_${C}_branch.npz <<'PY'
import json, sys, numpy as np
fz, dj, it = sys.argv[1], sys.argv[2], int(sys.argv[3]); F = set(json.load(open(fz))); d = json.load(open(dj)); new = set()
z = np.load(sys.argv[4]); V = z['V']; Q = z['Q']; br = (z['part'][Q] != 'v005').any(1); P = V[Q]
ar = 0.5 * np.linalg.norm(np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 1]), axis=1); new.update(int(f) for f in np.nonzero(br & (ar < 1e-6))[0])
for v in d['poses'].values():
    for pr in v['new_pairs']: new.update(pr[:2])
    new.update(v['flipped_faces']); new.update(v['root_inverted_faces'])
log = fz.replace('.json', '_log.json'); L = json.load(open(log)) if it else []
L.append(dict(iteration=it, guarded_faces_before=len(F), new_problem_faces=len(new - F))); json.dump(L, open(log, 'w'), indent=1)
json.dump(sorted(F | new), open(fz, 'w')); print(len(new - F))
PY
)
  [ "$n" = "0" ] && break
done
echo GUARD_DONE $H $it
