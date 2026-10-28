# run_ae_ear.sh : order fd71f15 Part C -- Aelari ear-branch prototype on the Fenn ear topology v002 ENGINEERING template (reuse test): AE-E1 / AE-E2 /
# AE-E3 (W1e AE-elven geometry, wholly Aelari parameters) on both Aelari configurations (AEL1, AELF190), the Fenn v002 cuff canon read-only (same
# connectivity), the deformation-aware guard, audit / measure / review blends, and the ten AE-E2 shape probes on configuration 1.
# env: AE_EAR_WORK (default /tmp/claude-0/rt/ae/ear), EAR_LAYOUT_METRIC (sheet-position metric; connectivity from the Fenn v002 layout).
# order 0f6aba8 (AE-E2 regression on the corrected heads): AE_H1 / AE_H2 (heads), AE_CF (body workspace), AE_EAR_CANDS, AE_EAR_VER, SKIP_PROBES=1.
B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; EV2=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002
W=${AE_EAR_WORK:-/tmp/claude-0/rt/ae/ear}; CF=${AE_CF:-/tmp/claude-0/rt/ae}; H1=${AE_H1:-AEL1}; H2=${AE_H2:-AELF190}; EV_=${AE_EAR_VER:-v001}; export EAR_CF=$CF EAR_TOPO=v002; mkdir -p $W/{build,audit,meas,deform,probe,blend}; cd $W
[ -f canon_branch_topology.json ] || cp $EV2/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json canon_branch_topology.json
one(){ h=$1; c=$2; sx=M; case $h in AELF*) sx=F;; esac
  EAR_CAND=$c bash $T/run_ear_v002_head.sh $h $W > build/${h}_${c}_guard.log 2>&1
  $B $T/ear_audit.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz audit/${h}_${c}_audit.json > audit/${h}_$c.log 2>&1
  python3 $T/ear_measure.py build/${h}_${c}_branch.npz meas/${h}_${c}_measure.json > meas/${h}_$c.log 2>&1
  $B $T/ear_blend.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz $CF/lm/${h}_fam_landmarks.json AE_${sx}_REF_RP3_ear${c#AE-}_proto_$EV_ blend > blend/${h}_$c.log 2>&1; echo "EAR $h $c"; }
[ "${SKIP_MAIN:-0}" = 1 ] || for c in ${AE_EAR_CANDS:-AE-E2 AE-E1 AE-E3}; do one $H1 $c & one $H2 $c & wait; done
[ "${SKIP_PROBES:-0}" = 1 ] && { echo AEEAR_DONE; exit 0; }
run(){ mkdir -p probe/$1; $B $T/ear_build.py AEL1 AE-E2 probe/$1 --canon canon_branch_topology.json --probe $2 > probe/$1/build.log 2>&1
       $B $T/ear_audit.py -- probe/$1/AEL1_AE-E2_branch.npz $CF/fam/AEL1_fam.npz probe/$1/audit.json > probe/$1/audit.log 2>&1; python3 $T/ear_measure.py probe/$1/AEL1_AE-E2_branch.npz probe/$1/measure.json > /dev/null 2>&1; }
run proj_m10 proj=14 & run proj_p10 proj=34 & run tilt_m8 tilt=22 & wait
run tilt_p8 tilt=38 & run sweep_m06 sweep=1.1 & run sweep_p06 sweep=2.3 & wait
run len_m10 L=8.46 & run len_p10 L=10.34 & wait
run tip_blunt taper_ex=0.65 & run tip_sharp taper_ex=1.4 & wait
echo AEEAR_DONE
