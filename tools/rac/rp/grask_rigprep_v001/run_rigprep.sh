#!/bin/bash
# run_rigprep.sh WORKDIR : reproduce the Grask RP2 rig-prep readiness proposal v001 (read-only on every parent)
#   inputs : freshly staged PC parents under /mnt/user-data/uploads/RaceBodies/production/Grask/RP2/
#            /tmp/claude-0/src3d/v5/v005.npz (v005 analysis copy; npzcheck.py proves it equals the blend)
#            /tmp/claude-0/rt/frz/v003_frz.npz (v003 freeze read-back, source frame; npzcheck.py proves it equals the blend)
#            /tmp/claude-0/src3d/v5/tools (frozen v005 hand / foot construction model)
set -e; W=${1:-/tmp/claude-0/rt/rpr}; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; D=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2
mkdir -p $W; cd $W
$T/hash_parents.sh $W/hashes_before.txt
$BP $T/npzcheck.py -- $D/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend /tmp/claude-0/src3d/v5/v005.npz 0 0 2>/dev/null | grep NPZCHECK > npzcheck.txt
$BP $T/npzcheck.py -- $D/GR_U_REF_RP2_retopo_v003.blend /tmp/claude-0/rt/frz/v003_frz.npz -0.11179767867288516 5.722717396009755 2>/dev/null | grep NPZCHECK >> npzcheck.txt
python3 $T/rigprep_fit.py /tmp/claude-0/src3d/v5/v005.npz fit_v005.json
python3 $T/rigprep_fit.py /tmp/claude-0/rt/frz/v003_frz.npz fit_v003.json
python3 $T/compose.py fit_v005.json fit_v003.json out
python3 $T/tables.py out/GR_U_REF_RP2_rigprep_landmarks_v001.json out
python3 $T/crops.py
$T/render_all.sh $W
python3 $T/overlay.py out/GR_U_REF_RP2_rigprep_landmarks_v001.json r sheets
$T/hash_parents.sh $W/hashes_after.txt
diff hashes_before.txt hashes_after.txt && echo PARENTS_UNCHANGED
