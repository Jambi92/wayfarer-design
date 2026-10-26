#!/bin/bash
# run_v004.sh WORKDIR : reproducible run of order 6c38d75 (elbow pose-space corrective). Candidates cand/C1-C3 (left), right counterpart cand/C2r_ext21
# (same class, support extended for the right contact extent), LBS arc both sides, DQS (Blender shape keys + drivers, preserve volume), knee check,
# full 43-pose suite W0 vs W0+selected corrective, judges and field checks.
set -e; W=$1; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; cd $W; mkdir -p corr diag
RD=/tmp/claude-0/rt/rd; LM=$RD/out/GR_U_REF_RP2_rigprep_landmarks_v002.json; RIG="$RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json $RD/rig/weights_v001c.npz"
KL=D2_l_base_abd45,D2_l_flex45,D2_l_flex60,D2_l_flex75,D2_l_flex90,D2_l_flex110,D2_l_flex120,D2_l_flex130
for c in C1 C2 C3; do $BP $T/corr_solve.py -- corr $c l cand/$c.json > corr/solve_$c.txt 2>&1; done
$BP $T/corr_solve.py -- corr C2r r cand/C2.json > corr/solve_C2r.txt 2>&1
$BP $T/corr_solve.py -- corr C2rx r cand/C2r_ext21.json > corr/solve_C2rx.txt 2>&1
for c in W0 C1 C2 C3; do bash $T/run_corr.sh . $c l > /dev/null; done
for c in W0 C2r C2rx; do bash $T/run_corr.sh . $c r > /dev/null; done
# DQS: W0 (no corrective) and C2 (identical keys as Blender shape keys + drivers)
ELBOW_SET=1 ELBOW_ARC=1 $BP $T/dqs_eval.py -- $RIG dqs_W0 $KL > /dev/null 2>&1
$BP $T/corr_blend.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json corr/corr_C2.npz - blend_lbs lbs $KL > corr/blend_lbs.txt 2>&1
$BP $T/corr_blend.py -- $RD/rig/GR_U_REF_RP2_rigdiag_v001.blend $RD/rig/rig_v001.json corr/corr_C2.npz - blend_dqs dqs $KL > corr/blend_dqs.txt 2>&1
for t in W0:dqs_W0 C2:blend_dqs; do n=${t%%:*}; d=${t#*:}
  VSRC=$d ELBOW_SET=1 ELBOW_ARC=1 ONLY_EXACT=1 ONLY=$KL TAG=_c_dqs_$n $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" > diag/summary_c_dqs_$n.txt; done
# merged selected corrective (left C2 + right C2rx) and the full 43-pose suite
python3 -c "
import numpy as np
L=np.load('corr/corr_C2.npz'); R=np.load('corr/corr_C2rx.npz'); assert list(L['anchors'])==list(R['anchors'])
o={'anchors':L['anchors']}; o.update({k:L[k] for k in L.files if k.startswith('K')}); o.update({k:R[k] for k in R.files if k.startswith('K')})
o.update(support_l=L['support'], support_r=R['support'], guard_l=L['guard'], guard_r=R['guard']); np.savez_compressed('corr/corr_SEL.npz', **o)"
TAG=_full_W0 $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" > diag/summary_full_W0.txt
CORR=corr/corr_SEL.npz TAG=_full_SEL $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D" > diag/summary_full_SEL.txt
python3 $T/full_judge_v004.py . > diag/full_judge_stdout.txt
python3 $T/corr_field_check.py . C2 l > /dev/null; python3 $T/corr_field_check.py . C2rx r > /dev/null
# knee: bounded v003 vs unrestricted v002 (W0, corrective inactive: no elbow flexion in D7)
ONLY_EXACT=1 ONLY=D7_l_flex90,D7_l_flex140 TAG=_knee_v002 $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D7" > diag/summary_knee_v002.txt
PIVOTS=knee_v003_l.json ONLY_EXACT=1 ONLY=D7_l_flex90,D7_l_flex140 TAG=_knee_v003_l $BP $T/diag_run.py -- $RIG $LM diag 2>&1 | grep -E "^D7" > diag/summary_knee_v003.txt
echo V004_DONE
