set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/sg
declare -A R6=( [SG]=/home/claude/wayfarer-design/reviews/reference-assets/r6/SG_r6.npz [SGF178]=/home/claude/wayfarer-design/reviews/reference-assets/r6/SGF178_r6.npz )
for id in SG SGF178; do
  r=${R6[$id]}; c=cand/${id}_fam.npz
  $BP $T/audit.py src/${id}_native.npz $r audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py $c $r audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $r $c lm/${id}_fam_landmarks.json >> audit/${id}_fam.log
  python3 $T/face_rings.py $c audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log
  python3 $T/face_rings.py src/${id}_native.npz audit/${id}_native_loops.npz lm/${id}_fam_landmarks.json audit/${id}_native_face.json >> audit/${id}_native.log
  python3 $T/anatomy.py $r $c anat/${id}_fam_anatomy.json >> audit/${id}_fam.log
  python3 $T/validator_v2.py $c val/${id}_fam_validator_v2.json > val/${id}.log
  python3 $T/validator_v2.py $c val/${id}_fam_validator_v2_D4.json --scale-ref 173.143 >> val/${id}.log
  python3 $T/validator_v2.py $c val/${id}_fam_validator_v2_D4_D5.json --scale-ref 173.143 --d5 >> val/${id}.log
  echo "EVAL $id done"
done
for id in SG SGF178; do
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz cand/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1
  echo "DEF $id done"
done
echo SGEVALDONE
