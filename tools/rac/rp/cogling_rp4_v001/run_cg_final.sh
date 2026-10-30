# run_cg_final.sh : RP4 Cogling final production gate (order f58dbd9). Fresh realizations from the reviewed MPFB_COGLING_COMPACT_BRANCH_v001 definition
# (run_cg_v1.sh pipeline into $W/final), production candidates CG_M/F_REF_RP4_v001 (cg_make_prod.py) + Blender read-back (freeze_check.py, no save),
# the approved Cogling toe-station exception record (raw validators kept) and the raw + scale-consistent T-7 record (cg_t7_scaled.py).
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; P=$R/tools/rac/rp/cogling_rp4_v001; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/cg; RA=$R/reviews/reference-assets/r6
DEF=$R/reviews/rac-rp4-evidence/cogling/branch/MPFB_COGLING_COMPACT_BRANCH_v001.json; F=$W/final; mkdir -p $F
OUTDIR=$F bash $P/run_cg_v1.sh $DEF CGJ7 CGF91-NAT CG76H-NAT CG107-NAT
cd $F; mkdir -p prod readback t7
ST="COGLING RP4 PRODUCTION REFERENCE CANDIDATE (MPFB_COGLING_COMPACT_BRANCH_v001, 2026-10-30) - CANDIDATE / NOT FROZEN; freeze only by author acceptance record"
for x in "CGJ7 CG_M_REF_RP4_v001" "CGF91-NAT CG_F_REF_RP4_v001"; do set -- $x
  $BP $P/cg_make_prod.py -- cb/$1_cgb.npz lm/$1_cgb_landmarks.json $2 prod "$ST" > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend cb/$1_cgb.npz lm/$1_cgb_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1; echo "PROD $2"; done
python3 $P/cg_toe_exception.py $F/COGLING_toe_exception_validator_summary.json $(for i in CG76H-NAT CGJ7 CGF91-NAT CG107-NAT; do echo "$i=$F/val/${i}_cgb_validator_v2_D1-D6.json:$F/cb/${i}_cgb.npz"; done)
for i in CG76H-NAT CGJ7 CGF91-NAT CG107-NAT; do R6=$RA/${i}_r6.npz; [ $i = CGF91-NAT ] && R6=$W/nat/CGF91-NAT_r6.npz
  python3 $P/cg_t7_scaled.py $R6 cb/${i}_cgb.npz t7/${i}_t7_scaled.json $W/fam/${i}_fam.npz > t7/${i}.log; done
echo CG_FINAL_DONE
