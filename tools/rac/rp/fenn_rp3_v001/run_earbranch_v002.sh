# run_earbranch_v002.sh : order 0d9c70b -- Fenn ear-branch TOPOLOGY v002 (selected E2) on both CF2 configurations + the ten shape probes.
# Needs the CF2 family realizations / native rigs from run_cfeval.sh in /tmp/claude-0/rt/fn/cf. v002 is the library default (EAR_TOPO=v002).
B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; EV=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002
W=${EAR_WORK:-/tmp/claude-0/rt/fn/ear/v002}; CF=/tmp/claude-0/rt/fn/cf; mkdir -p $W/{build,audit,meas,deform,probe,blend,sheets}; cd $W
export EAR_TOPO=v002
# canonical cuff topology: written once on configuration 1 E2, then read-only for every realization (identical topology)
[ -f canon_branch_topology.json ] || cp $EV/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json canon_branch_topology.json 2>/dev/null || \
  $B $T/ear_build.py FNL4-CF2 E2 build --canon canon_branch_topology.json --write-canon > build/canon.log 2>&1
for h in FNL4-CF2 FNF181-CF2; do sx=M; [ $h = FNF181-CF2 ] && sx=F; c=E2; (
  bash $T/run_ear_v002_head.sh $h $W > build/${h}_guard.log 2>&1          # build + 8-pose deformation check with the deformation-aware guard
  $B $T/ear_audit.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz audit/${h}_${c}_audit.json > audit/${h}_$c.log 2>&1
  python3 $T/ear_measure.py build/${h}_${c}_branch.npz meas/${h}_${c}_measure.json > meas/${h}_$c.log 2>&1
  $B $T/ear_blend.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz $CF/lm/${h}_fam_landmarks.json FN_${sx}_REF_RP3_cf2_earE2_v002 blend > blend/${h}_$c.log 2>&1 ) & done; wait
run(){ mkdir -p probe/$1; $B $T/ear_build.py FNL4-CF2 E2 probe/$1 --canon canon_branch_topology.json --probe $2 > probe/$1/build.log 2>&1
       $B $T/ear_audit.py -- probe/$1/FNL4-CF2_E2_branch.npz $CF/fam/FNL4-CF2_fam.npz probe/$1/audit.json > probe/$1/audit.log 2>&1; python3 $T/ear_measure.py probe/$1/FNL4-CF2_E2_branch.npz probe/$1/measure.json > /dev/null 2>&1; }
run proj_m10 proj=40 & run proj_p10 proj=60 & run tilt_m8 tilt=24 & run tilt_p8 tilt=40 & run sweep_m06 sweep=1.0 & wait
run sweep_p06 sweep=2.2 & run len_m10 L=7.74 & run len_p10 L=9.46 & run tip_blunt taper_ex=0.7 & run tip_sharp taper_ex=1.5 & wait
echo EARV002_DONE
