#!/bin/bash
# run_diag.sh WORKDIR : D1-D10 on the diagnostic rig (LBS), Blender preserve-volume (DQS) comparison, joint-placement comparisons
set -e; W=${1:-/tmp/claude-0/rt/rd}; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W
RIG="rig/GR_U_REF_RP2_rigdiag_v001.blend rig/rig_v001.json rig/weights_v001c.npz"; LM=out/GR_U_REF_RP2_rigprep_landmarks_v002.json
$BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" > diag/summary_lbs.txt
KEY=D1_l_abd90,D1_l_flex90,D1_r_abd90,D1_r_flex90,D2_l_flex90,D2_l_flex130,D4_l_fist,D6_l_flex90,D6_r_flex90,D7_l_flex90,D7_l_flex140
$BP $T/dqs_eval.py -- $RIG diag/dqs $KEY > /dev/null 2>&1
VSRC=diag/dqs TAG=_dqs ONLY_EXACT=1 ONLY=$KEY $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" > diag/summary_dqs.txt
for f in alt/*.json; do n=$(basename $f .json); o=$(python3 -c "import json;print(','.join(json.load(open('$f'))['poses']))")
  PIVOTS=$f TAG=_alt_$n ONLY_EXACT=1 ONLY=$o $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" | sed "s/^/$n /" >> diag/summary_alt.txt; done
echo DIAG_DONE
