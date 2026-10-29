# run_va_ri.sh : order chatgpt-rac-rp3-vael-ear-root-integration-order -- Vael VA-E2 root / concha integration alternatives on both accepted Vael
# configurations (VAL4-R1-VD2-VF2, VALF178-R1-VD2-VF2), same VA-E2 outer geometry (ear_branch_lib.CAND['VA-E2-RI*']):
#   RI1  reduced stand-off (rigid; concha clearance -0.30 cm)                         -- Fenn v002 cuff canon (read-only)
#   RI2  RI1 + skin-hugging cuff (geo cuff_skin_*)                                     -- Fenn v002 cuff canon (read-only)
#   RI3  RI2 on the local Vael cuff derivative (six cuff rings 52 56 60 64 66 68)       -- VAEL_EAR_CUFF_CANON_v001 (read-only)
# each with the deformation-aware guard, audit / measure / review blends; the twelve VA-E2 readiness probes on the selected alternative ($VA_RI_SEL,
# default RI3) on configuration 1. Engineering setting as the prototype order: EAR_UNT_MODE=contacts.
# env: VA_RI_WORK (default /tmp/claude-0/rt/va/ri_final), VA_CF, VA_RI_LIST, VA_RI_SEL, SKIP_MAIN / SKIP_PROBES.
B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; R=/home/claude/wayfarer-design/reviews/rac-rp3-evidence
WB=${VA_RI_WORK:-/tmp/claude-0/rt/va/ri_final}; CF=${VA_CF:-/tmp/claude-0/rt/vf/prod}; H1=VAL4-R1-VD2-VF2; H2=VALF178-R1-VD2-VF2; SEL=${VA_RI_SEL:-RI3}
export EAR_CF=$CF EAR_TOPO=v002 EAR_UNT_MODE=${EAR_UNT_MODE:-contacts}
canon(){ case $1 in RI3) echo $R/vael_rp3_ear_root_integration/topology/VAEL_EAR_CUFF_CANON_v001.json;; *) echo $R/fenn_ear_v002/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json;; esac; }
one(){ ri=$1; h=$2; c=VA-E2-$ri; W=$WB/$ri; sx=M; case $h in VALF*) sx=F;; esac; cd $W
  EAR_CAND=$c bash $T/run_ear_v002_head.sh $h $W > build/${h}_${c}_guard.log 2>&1
  $B $T/ear_audit.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz audit/${h}_${c}_audit.json > audit/${h}_$c.log 2>&1
  python3 $T/ear_measure.py build/${h}_${c}_branch.npz meas/${h}_${c}_measure.json > meas/${h}_$c.log 2>&1
  $B $T/ear_blend.py -- build/${h}_${c}_branch.npz $CF/fam/${h}_fam.npz $CF/lm/${h}_fam_landmarks.json VA_${sx}_REF_RP3_earE2_${ri}_v001 blend > blend/${h}_$c.log 2>&1; echo "EAR $ri $h"; }
for ri in ${VA_RI_LIST:-RI1 RI2 RI3}; do mkdir -p $WB/$ri/{build,audit,meas,deform,probe,blend}; [ -f $WB/$ri/canon_branch_topology.json ] || cp $(canon $ri) $WB/$ri/canon_branch_topology.json; done
[ "${SKIP_MAIN:-0}" = 1 ] || for ri in ${VA_RI_LIST:-RI1 RI2 RI3}; do one $ri $H1 & one $ri $H2 & wait; done
[ "${SKIP_PROBES:-0}" = 1 ] && { echo VARI_DONE; exit 0; }
W=$WB/$SEL; cd $W; c=VA-E2-$SEL
run(){ mkdir -p probe/$1; $B $T/ear_build.py $H1 $c probe/$1 --canon canon_branch_topology.json --probe $2 > probe/$1/build.log 2>&1
       $B $T/ear_audit.py -- probe/$1/${H1}_${c}_branch.npz $CF/fam/${H1}_fam.npz probe/$1/audit.json > probe/$1/audit.log 2>&1; python3 $T/ear_measure.py probe/$1/${H1}_${c}_branch.npz probe/$1/measure.json > /dev/null 2>&1; }
run proj_m10 proj=25 & run proj_p10 proj=45 & run tilt_m8 tilt=32 & wait
run tilt_p8 tilt=48 & run sweep_m06 sweep=1.1 & run sweep_p06 sweep=2.3 & wait
run len_m10 L=7.65 & run len_p10 L=9.35 & run tip_blunt taper_ex=0.85 & wait
run tip_sharp taper_ex=1.65 & run wb_m8 wb=1.886 & run wb_p8 wb=2.214 & wait
echo VARI_DONE
