# run_pk_final.sh : RP4 Pipkin final production gate (order 68ba8e5). Fresh realizations from the reviewed MPFB_PIPKIN_COMPACT_BRANCH_v001 definition
# (run_pk_v1.sh pipeline into $W/final), production candidates PK_M/F_REF_RP4_v001 (pk_make_prod.py) + Blender read-back (freeze_check.py, no save),
# and the approved toe-station exception record (raw validators kept).
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; P=$R/tools/rac/rp/pipkin_rp4_v001; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/pk
DEF=$R/reviews/rac-rp4-evidence/pipkin/branch/MPFB_PIPKIN_COMPACT_BRANCH_v001.json; F=$W/final; mkdir -p $F
sed "s|O=\$W/v1;|O=$F;|" $P/run_pk_v1.sh > $F/run_gates.sh
bash $F/run_gates.sh $DEF PK-NAT PKF107-NAT PK91-NAT PK122-NAT
cd $F; mkdir -p prod readback
ST="PIPKIN RP4 PRODUCTION REFERENCE CANDIDATE (MPFB_PIPKIN_COMPACT_BRANCH_v001, 2026-10-30) - CANDIDATE / NOT FROZEN; freeze only by author acceptance record"
for x in "PK-NAT PK_M_REF_RP4_v001" "PKF107-NAT PK_F_REF_RP4_v001"; do set -- $x
  $BP $P/pk_make_prod.py -- cb/$1_pkb.npz lm/$1_pkb_landmarks.json $2 prod "$ST" > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend cb/$1_pkb.npz lm/$1_pkb_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1; echo "PROD $2"; done
python3 $P/pk_toe_exception.py $F/PIPKIN_toe_exception_validator_summary.json $(for i in PK91-NAT PK-NAT PKF107-NAT PK122-NAT; do echo "$i=$F/val/${i}_pkb_validator_v2_D1-D6.json:$F/cb/${i}_pkb.npz"; done)
echo PK_FINAL_DONE
