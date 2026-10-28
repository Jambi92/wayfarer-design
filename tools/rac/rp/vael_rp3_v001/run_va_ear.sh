# run_va_ear.sh : order chatgpt-rac-rp3-vael-ear-prototype-order -- Vael ear prototypes VA-E1 / VA-E2 / VA-E3 on the frozen Fenn ear topology v002
# ENGINEERING template (connectivity reuse only; wholly Vael parameters, ear_branch_lib.CAND['VA-E*']) on both accepted Vael configurations
# (VAL4-R1-VD2-VF2, VALF178-R1-VD2-VF2), the Fenn v002 cuff canon read-only, the deformation-aware guard, audit / measure / review blends, and the
# twelve VA-E2 geometry-only readiness probes on configuration 1 (projection, tilt, sweep, length, tip, base width).
# Engineering setting (Vael): EAR_UNT_MODE=contacts -- the v002 'full' untangle adds cuff-aspect rounds that lower cuff vertices towards the
# head; on the broader Vael base those rounds create contacts (c2 VA-E2: 3 pairs at the 80-round cap, so the quality pass falls back to the untangled
# state). Contacts-only untangling + the unchanged v002 3-D quality pass and aspect repair. Vael geometry also carries a 0.15 cm concha clearance
# (CAND VA-E* geo; Fenn / Aelari 0.05): at 0.05 the broad, backward Vael base sits on the cuff and the quality pass freezes contact faces (VA-E3 c2
# min corner 4.2 deg, cuff T-4 56); at 0.15 cuff T-4 17, min corner 19.8 deg. Topology is unchanged.
# env: VA_EAR_WORK (default /tmp/claude-0/rt/va/ear), VA_CF (VF2 family workspace), SKIP_MAIN / SKIP_PROBES.
B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; EV2=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002
W=${VA_EAR_WORK:-/tmp/claude-0/rt/va/ear}; CF=${VA_CF:-/tmp/claude-0/rt/vf/prod}; H1=VAL4-R1-VD2-VF2; H2=VALF178-R1-VD2-VF2
export EAR_CF=$CF EAR_TOPO=v002 EAR_UNT_MODE=${EAR_UNT_MODE:-contacts}; mkdir -p $W/{build,audit,meas,deform,probe,blend}; cd $W
[ -f canon_branch_topology.json ] || cp $EV2/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json canon_branch_topology.json
one(){ h=$1; c=$2; sx=M; case $h in VALF*) sx=F;; esac
  EAR_CAND=$c bash $T/run_ear_v002_head.sh $h $W > build/${h}_${c}_guard.log 2>&1
  $B $T/ear_audit.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz audit/${h}_${c}_audit.json > audit/${h}_$c.log 2>&1
  python3 $T/ear_measure.py build/${h}_${c}_branch.npz meas/${h}_${c}_measure.json > meas/${h}_$c.log 2>&1
  $B $T/ear_blend.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz $CF/lm/${h}_fam_landmarks.json VA_${sx}_REF_RP3_ear${c#VA-}_proto_v001 blend > blend/${h}_$c.log 2>&1; echo "EAR $h $c"; }
[ "${SKIP_MAIN:-0}" = 1 ] || for c in VA-E2 VA-E1 VA-E3; do one $H1 $c & one $H2 $c & wait; done
[ "${SKIP_PROBES:-0}" = 1 ] && { echo VAEAR_DONE; exit 0; }
run(){ mkdir -p probe/$1; $B $T/ear_build.py $H1 VA-E2 probe/$1 --canon canon_branch_topology.json --probe $2 > probe/$1/build.log 2>&1
       $B $T/ear_audit.py -- probe/$1/${H1}_VA-E2_branch.npz $CF/fam/${H1}_fam.npz probe/$1/audit.json > probe/$1/audit.log 2>&1; python3 $T/ear_measure.py probe/$1/${H1}_VA-E2_branch.npz probe/$1/measure.json > /dev/null 2>&1; }
run proj_m10 proj=25 & run proj_p10 proj=45 & run tilt_m8 tilt=32 & wait
run tilt_p8 tilt=48 & run sweep_m06 sweep=1.1 & run sweep_p06 sweep=2.3 & wait
run len_m10 L=7.65 & run len_p10 L=9.35 & run tip_blunt taper_ex=0.85 & wait
run tip_sharp taper_ex=1.65 & run wb_m8 wb=1.886 & run wb_p8 wb=2.214 & wait
echo VAEAR_DONE
