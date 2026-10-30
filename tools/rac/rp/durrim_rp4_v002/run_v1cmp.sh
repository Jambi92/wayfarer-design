# run_v1cmp.sh ID... : the rejected v001 prototype realizations (du_branch.py apply of the committed v001 definition) through audit / landmarks / face rings /
# validator / density, for the order §11 three-way density comparison (v005 | v001 | v002). Outputs $W/v2/v1/.
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; D1=$R/tools/rac/rp/durrim_rp4_v001; BP=/home/claude/stc/bin/python3; RA=$R/reviews/reference-assets
PA=$R/reviews/rac-rp4-evidence/durrim/partA; W=/tmp/claude-0/rt/du; O=$W/v2/v1; mkdir -p $O; cd $W
for id in "$@"; do R6=$RA/r6/${id}_r6.npz; [ $id = DUF137C-NAT ] && R6=$PA/DUF137C-NAT_r6.npz
  C=v2/cb1/${id}_cb.npz
  $BP $T/audit.py $C $R6 $O/${id}_cb1_audit.json $O/${id}_cb1_loops.npz > $O/${id}.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R6 $C $O/${id}_cb1_landmarks.json >> $O/${id}.log 2>&1
  python3 $T/face_rings.py $C $O/${id}_cb1_loops.npz $O/${id}_cb1_landmarks.json $O/${id}_cb1_face.json >> $O/${id}.log 2>&1
  python3 $T/validator_v2.py $C $O/${id}_cb1_validator.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz >> $O/${id}.log 2>&1
  python3 $D1/du_density.py $C $O/${id}_cb1_loops.npz $O/${id}_cb1_landmarks.json $O/${id}_cb1_face.json $O/${id}_cb1_validator.json $O/${id}_cb1_density.json >> $O/${id}.log 2>&1
  echo "V1 $id"; done
