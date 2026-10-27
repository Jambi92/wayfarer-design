# run_earbranch.sh : order bdcd6a6 -- reproduce the Fenn ear-branch prototypes (needs the CF2 family realizations from run_cfeval.sh in
# /tmp/claude-0/rt/fn/cf/fam and the CF2 native rigs in /tmp/claude-0/rt/fn/cf/src).
B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; EV=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_branch_v001
W=${EAR_WORK:-/tmp/claude-0/rt/fn/ear/final}; CF=/tmp/claude-0/rt/fn/cf; mkdir -p $W/{build,audit,meas,deform,probe,blend,sheets}; cd $W
# canonical topology: written once on configuration 1 E2, then read-only for every realization (identical topology)
[ -f canon_branch_topology.json ] || cp $EV/topology/FENN_EAR_BRANCH_CUFF_CANON_v001.json canon_branch_topology.json
for h in FNL4-CF2 FNF181-CF2; do sx=M; [ $h = FNF181-CF2 ] && sx=F; for c in E1 E2 E3; do (
  $B $T/ear_build.py $h $c build --canon canon_branch_topology.json > build/${h}_$c.log 2>&1
  $B $T/ear_audit.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz audit/${h}_${c}_audit.json > audit/${h}_$c.log 2>&1
  python3 $T/ear_measure.py build/${h}_${c}_branch.npz meas/${h}_${c}_measure.json > meas/${h}_$c.log 2>&1
  $B $T/ear_deform.py -- $CF/src/${h}_native.npz build/${h}_${c}_branch.npz deform/${h}_${c}_deform.json deform/${h}_${c} $CF/fam/${h}_fam.npz > deform/${h}_$c.log 2>&1
  $B $T/ear_blend.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz $CF/lm/${h}_fam_landmarks.json FN_${sx}_REF_RP3_cf2_ear${c}_proto_v001 blend > blend/${h}_$c.log 2>&1 ) & done; done; wait
# geometry-only shape readiness probes (configuration 1, E2 base)
run(){ mkdir -p probe/$1; $B $T/ear_build.py FNL4-CF2 E2 probe/$1 --canon canon_branch_topology.json --probe $2 > probe/$1/build.log 2>&1
       $B $T/ear_audit.py -- probe/$1/FNL4-CF2_E2_branch.npz $CF/fam/FNL4-CF2_fam.npz probe/$1/audit.json > probe/$1/audit.log 2>&1; python3 $T/ear_measure.py probe/$1/FNL4-CF2_E2_branch.npz probe/$1/measure.json > /dev/null 2>&1; }
run proj_m10 proj=40 & run proj_p10 proj=60 & run tilt_m8 tilt=24 & run tilt_p8 tilt=40 & run sweep_m06 sweep=1.0 & wait
run sweep_p06 sweep=2.2 & run len_m10 L=7.74 & run len_p10 L=9.46 & run tip_blunt taper_ex=0.7 & run tip_sharp taper_ex=1.5 & wait
python3 $T/ear_sheets.py . sheets; python3 $T/ear_sections.py . sheets; python3 $T/ear_export.py . $EV
echo EARBRANCH_DONE
