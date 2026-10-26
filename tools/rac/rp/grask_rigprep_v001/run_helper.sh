#!/bin/bash
# run_helper.sh WORKDIR TAG SIDE HDIR [CORR.npz] : evaluate a helper-volume candidate (order 8e5021d §7): rig HDIR/rig_h.json + HDIR/weights_H.npz,
# helper poses HELPER=HDIR/helper_pose.json, optional pose-space corrective keys (CORR, solved on the helper base), v002 landmarks, LBS, elbow arc.
set -e; W=$1; TG=$2; S=$3; HD=$4; CR=${5:-}; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p diag
RD=/tmp/claude-0/rt/rd; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json
K=D2_${S}_base_abd45,D2_${S}_flex45,D2_${S}_flex60,D2_${S}_flex75,D2_${S}_flex90,D2_${S}_flex110,D2_${S}_flex120,D2_${S}_flex130
HELPER=$HD/helper_pose.json CORR=$CR ELBOW_SET=1 ELBOW_SET_R=1 ELBOW_ARC=1 ONLY_EXACT=1 ONLY=$K TAG=_c_${S}_$TG \
  $BP $T/diag_run.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $HD/rig_h.json $HD/weights_H.npz $LM diag 2>&1 | grep -E "^D|Error" | tee diag/summary_c_${S}_$TG.txt
