#!/bin/bash
# run_diagstage.sh WORKDIR : reproduce the AD-R1..R12 adjudicated landmarks v002, the diagnostic rig and D1-D10 (order bf7d664)
set -e; W=${1:-/tmp/claude-0/rt/rd}; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; D=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2
mkdir -p $W/rig $W/diag; cd $W
$T/hash_parents.sh hashes_before.txt
python3 $T/adjudicate.py /tmp/claude-0/rt/rpr/out/GR_U_REF_RP2_rigprep_landmarks_v001.json /tmp/claude-0/rt/rpr/fit_v005.json out
python3 $T/package.py out/adjudicated_raw_v002.json out v002
cp $D/GR_U_REF_RP2_retopo_v003.blend v003_workcopy.blend          # work copy; the staged parent itself is never opened for writing
$BP $T/rig_build.py -- v003_workcopy.blend out/GR_U_REF_RP2_rigprep_landmarks_v002.json rig/GR_U_REF_RP2_rigdiag_v001.blend rig/rig_v001.json rig/weights_v001.npz
$BP $T/rig_clean.py -- rig/GR_U_REF_RP2_rigdiag_v001.blend rig/weights_v001c.npz rig/weight_cleanup_log.json
$BP $T/rig_check.py -- rig/GR_U_REF_RP2_rigdiag_v001.blend rig/rig_v001.json rig/weights_v001c.npz out/GR_U_REF_RP2_rigprep_landmarks_v002.json rig/rig_check.json
$T/run_diag.sh $W                                                  # LBS suite, DQS comparison, placement comparisons (alt/*.json pivots)
python3 $T/judge.py $W; python3 $T/evidence.py $W; python3 $T/cmp_sheet.py $W
python3 $T/overlay2.py out/GR_U_REF_RP2_rigprep_landmarks_v002.json /tmp/claude-0/rt/rpr/out/GR_U_REF_RP2_rigprep_landmarks_v001.json lsheets
$T/hash_parents.sh hashes_after.txt; diff hashes_before.txt hashes_after.txt && echo PARENTS_UNCHANGED
