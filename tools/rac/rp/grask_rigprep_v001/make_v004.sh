#!/bin/bash
# make_v004.sh WORKDIR : derived diagnostic GR_U_REF_RP2_rigdiag_v004.blend (order 6c38d75 §4): frozen v003 copy -> rig (v002 landmarks, skeleton
# identical to rig v001) + W0 weights (bit-identical) + the selected elbow pose-space corrective as driven shape keys (left C2, right C2rx).
# The Basis (rest) geometry stays the frozen v003 geometry; nothing is written to any frozen parent.
set -e; W=$1; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p rig4
RD=/tmp/claude-0/rt/rd; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json; SRC=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_retopo_v003.blend
cp $SRC rig4/_src.blend
WEIGHTS_NPZ=$RD/rig/weights_v001c.npz RIG_VERSION=v004 $BP $T/rig_build.py -- rig4/_src.blend $LM rig4/_base_v004.blend rig4/rig_v004.json rig4/weights_v004_readback.npz > rig4/build.log 2>&1
rm -f rig4/_src.blend
K=D2_l_base_abd45,D2_l_flex45,D2_l_flex60,D2_l_flex75,D2_l_flex90,D2_l_flex110,D2_l_flex120,D2_l_flex130,D2_r_flex45,D2_r_flex90,D2_r_flex110,D2_r_flex130,D1_l_abd90,D3_l_flex60,D4_l_fist
$BP $T/corr_blend.py -- rig4/_base_v004.blend rig4/rig_v004.json corr/corr_SEL.npz rig4/GR_U_REF_RP2_rigdiag_v004.blend rig4/check lbs $K > rig4/corr_blend.log 2>&1
rm -f rig4/_base_v004.blend
$BP $T/rig_tag.py -- rig4/GR_U_REF_RP2_rigdiag_v004.blend rig4/props_v004.json > rig4/tag.log 2>&1
$BP $T/geomhash.py -- rig4/GR_U_REF_RP2_rigdiag_v004.blend 2>/dev/null | grep -E "FILESHA|GEOMHASH|OBJ" > rig4/readback_v004.txt
echo MAKE_V004_DONE
