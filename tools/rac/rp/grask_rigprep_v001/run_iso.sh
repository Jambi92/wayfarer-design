#!/bin/bash
# run_iso.sh WORKDIR STAGE : failure-isolation runs (order 8918cea). STAGE = select | full | alt
set -e; W=${1:-/tmp/claude-0/rt/r2}; ST=$2; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p diag
RD=/tmp/claude-0/rt/rd; RIG="$RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json"; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json
HARD=D1_l_abd90,D1_l_flex90,D1_r_abd90,D1_r_flex90,D2_l_flex90,D2_l_flex130,D3_l_flex60,D3_l_ext60,D4_l_fist,D5_l_oppose_pinch,D5_l_oppose_pinky,D6_l_flex45,D6_l_flex90,D6_r_flex90,D7_l_flex90,D7_l_flex140
if [ "$ST" = select ]; then
  for c in W0:$RD/rig/weights_v001c.npz W1:w/weights_W1.npz W2:w/weights_W2.npz; do t=${c%%:*}; f=${c#*:}
    ONLY_EXACT=1 ONLY=$HARD TAG=_sel_$t $BP $T/diag_run.py -- $RIG $f $LM diag 2>&1 | grep -E "^D" > diag/summary_sel_$t.txt; done
fi
if [ "$ST" = full ]; then
  for c in W0:$RD/rig/weights_v001c.npz $3; do t=${c%%:*}; f=${c#*:}
    TAG=_full_$t $BP $T/diag_run.py -- $RIG $f $LM diag 2>&1 | grep -E "^D" > diag/summary_full_$t.txt; done
fi
echo ISO_${ST}_DONE
if [ "$ST" = alt ]; then                                             # alternate pivots with the identical selected weight array ($3 = TAG:npz)
  c=$3; t=${c%%:*}; f=${c#*:}; : > diag/summary_alt_$t.txt
  for a in alt/*.json; do n=$(basename $a .json); o=$(python3 -c "import json;print(','.join(json.load(open('$a'))['poses']))")
    PIVOTS=$a TAG=_alt_${n}_$t ONLY_EXACT=1 ONLY=$o $BP $T/diag_run.py -- $RIG $f $LM diag 2>&1 | grep -E "^D" | sed "s/^/$n /" >> diag/summary_alt_$t.txt; done
  echo ISO_alt_DONE
fi
if [ "$ST" = dqs ]; then                                             # rig v002 (v003 landmarks + W2): LBS vs DQS, identical pivots / weights / poses
  R2="rig/GR_U_REF_RP2_rigdiag_v002.blend rig/rig_v002.json w/weights_W2.npz"; L3=out/GR_U_REF_RP2_rigprep_landmarks_v003.json
  K=$HARD,D6_l_abd30,D6_r_abd30
  ONLY_EXACT=1 ONLY=$K TAG=_v2_lbs $BP $T/diag_run.py -- $R2 $L3 diag 2>&1 | grep -E "^D" > diag/summary_v2_lbs.txt
  $BP $T/dqs_eval.py -- $R2 diag/dqs_v2 $K > /dev/null 2>&1
  VSRC=diag/dqs_v2 ONLY_EXACT=1 ONLY=$K TAG=_v2_dqs $BP $T/diag_run.py -- $R2 $L3 diag 2>&1 | grep -E "^D" > diag/summary_v2_dqs.txt
  echo ISO_dqs_DONE
fi
