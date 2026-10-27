T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5
cd /tmp/claude-0/rt/fn/cf; mkdir -p src fam audit anat lm val
one(){ id=$1; d=cand/$id; r=$d/${id}_r6.npz
  $BP $T/regen.py $d/${id}_build.json $r src > src/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $r audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $r fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $r fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}.log 2>&1
  echo "CFEVAL $id $?"; }
one FNL4-CF1 & one FNL4-CF2 & wait
one FNL4-CF3 & one FNF181-CF1 & wait
one FNF181-CF2 & one FNF181-CF3 & wait
echo CFEVALDONE
