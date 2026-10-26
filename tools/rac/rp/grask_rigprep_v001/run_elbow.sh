#!/bin/bash
# run_elbow.sh WORKDIR : left-elbow isolation runs (order b303b9e §4). Rig v001 skeleton + v002 landmarks/pivots, identical arrays under LBS and DQS.
# Elbow set: reference (D2_l_base_abd45), flexion 45 / 90 / 130 from the abd45 shoulder setup; return-to-rest = rest_return_T1_mm of each pose.
# Sentinels: shoulder D1_l_abd90 / D1_l_flex90, wrist D3_l_flex60 / D3_l_ext60, fingers D4_l_fist / D5_l_oppose_pinch.
set -e; W=$1; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p diag rig
RD=/tmp/claude-0/rt/rd; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json; SRC=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_retopo_v003.blend
K=D2_l_base_abd45,D2_l_flex45,D2_l_flex90,D2_l_flex130,D1_l_abd90,D1_l_flex90,D3_l_flex60,D3_l_ext60,D4_l_fist,D5_l_oppose_pinch
for c in W0:$RD/rig/weights_v001c.npz E1:w/weights_E1.npz E2:w/weights_E2.npz; do t=${c%%:*}; f=${c#*:}
  if [ ! -f rig/el_$t.blend ]; then cp $SRC /tmp/claude-0/rt/r3/rig/_src.blend
    WEIGHTS_NPZ=$f RIG_VERSION=eltest_$t $BP $T/rig_build.py -- rig/_src.blend $LM rig/el_$t.blend rig/el_$t.json rig/el_${t}_readback.npz > rig/el_$t.log 2>&1; rm -f rig/_src.blend; fi
  ELBOW_SET=1 ONLY_EXACT=1 ONLY=$K TAG=_el_lbs_$t $BP $T/diag_run.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json $f $LM diag 2>&1 | grep -E "^D" > diag/summary_el_lbs_$t.txt
  ELBOW_SET=1 $BP $T/dqs_eval.py -- rig/el_$t.blend $RD/rig/rig_v001.json $f diag/dqs_$t $K > /dev/null 2>&1
  VSRC=diag/dqs_$t ELBOW_SET=1 ONLY_EXACT=1 ONLY=$K TAG=_el_dqs_$t $BP $T/diag_run.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json $f $LM diag 2>&1 | grep -E "^D" > diag/summary_el_dqs_$t.txt
  echo done $t
done
echo ELBOW_DONE
