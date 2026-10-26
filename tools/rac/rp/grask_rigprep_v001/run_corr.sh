#!/bin/bash
# run_corr.sh WORKDIR TAG [SIDE] : evaluate a pose-space corrective (corr/corr_TAG.npz) with the unchanged retained metrics (diag_run.py, CORR=...),
# rig v001 + v002 landmarks + W0, elbow set + intermediate driver angles (order 6c38d75 §7/§8). LBS only here; DQS via dqs_corr.py.
set -e; W=$1; TG=$2; S=${3:-l}; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p diag
RD=/tmp/claude-0/rt/rd; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json
if [ "$S" = l ]; then K=D2_l_base_abd45,D2_l_flex45,D2_l_flex60,D2_l_flex75,D2_l_flex90,D2_l_flex110,D2_l_flex120,D2_l_flex130; else K=D2_r_base_abd45,D2_r_flex45,D2_r_flex60,D2_r_flex75,D2_r_flex90,D2_r_flex110,D2_r_flex120,D2_r_flex130; fi
CORR=$( [ "$TG" = W0 ] && echo "" || echo corr/corr_$TG.npz ) ELBOW_SET=1 ELBOW_SET_R=1 ELBOW_ARC=1 ONLY_EXACT=1 ONLY=$K TAG=_c_${S}_$TG \
  $BP $T/diag_run.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json $RD/rig/weights_v001c.npz $LM diag 2>&1 | grep -E "^D|Error" | tee diag/summary_c_${S}_$TG.txt
