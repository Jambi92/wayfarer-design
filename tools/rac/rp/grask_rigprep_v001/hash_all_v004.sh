#!/bin/bash
# hash_all_v004.sh OUT.txt : frozen parents (hash_parents.sh) + diagnostic rigs v001-v003 (PC re-staged copies) + every weight record
# W0/W1/W2/WN/WNcap/E1/E2 (file SHA-256 and array SHA-256 of the float32 W bytes)          (order 6c38d75 §3)
T=$(cd "$(dirname "$0")" && pwd); O=$1; bash $T/hash_parents.sh "$O"
D=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2/DIAG
for f in GR_U_REF_RP2_rigdiag_v001.blend GR_U_REF_RP2_rigdiag_v002.blend GR_U_REF_RP2_rigdiag_v003.blend ${EXTRA_DIAG:-}; do echo "$(sha256sum $D/$f | cut -c1-64)  DIAG/$f" >> "$O"; done
EV=/home/claude/wayfarer-design/reviews/rac-rp2-evidence
for f in /tmp/claude-0/rt/rd/rig/weights_v001c.npz $EV/grask_rig_diagnostic_v002/weights/weights_W1.npz $EV/grask_rig_diagnostic_v002/weights/weights_W2.npz \
         $EV/grask_rig_diagnostic_v003/weights/weights_WN.npz $EV/grask_rig_diagnostic_v003/weights/weights_WNcap.npz \
         $EV/grask_rig_diagnostic_v003/weights/weights_E1.npz $EV/grask_rig_diagnostic_v003/weights/weights_E2.npz; do
  a=$(python3 -c "import numpy as np,hashlib;print(hashlib.sha256(np.ascontiguousarray(np.load('$f')['W'].astype(np.float32)).tobytes()).hexdigest())")
  echo "$(sha256sum $f | cut -c1-64)  array:$a  $(basename $f)" >> "$O"
done
