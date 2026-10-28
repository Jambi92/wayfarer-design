# run_aeeval.sh : order fd71f15 Part B -- Aelari body-family candidates (AEL1 configuration 1, AELF190 configuration 2) on frozen MPFB Family Base v005,
# Standard v1 pipeline (as run_fneval.sh / run_cfeval.sh): regen from the committed record (geometry identity), native hm08 export, propagate (no topology
# change), audit, landmarks, face rings, anatomy, validator D1 + D3 + D4 + D5 + D6, contact classification, 18-pose deformation (native + family).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001
BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5; RA=/home/claude/wayfarer-design/reviews/reference-assets
W=${AE_WORK:-/tmp/claude-0/rt/ae}; cd $W; mkdir -p src fam audit anat lm val def contact
one(){ id=$1; R=$RA/r6/${id}_r6.npz; base=$2
  $BP $T/regen.py $RA/builds/${id}_build.json $R src > src/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py src/${id}_native.npz audit/${id}_native_loops.npz lm/${id}_fam_landmarks.json audit/${id}_native_face.json >> audit/${id}_native.log 2>&1
  python3 $T/anatomy.py $R fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D4_D5.json --scale-ref 173.143 --d5 > val/${id}.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz >> val/${id}.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          /tmp/claude-0/rt/v5/cand/${base}_v005.npz /tmp/claude-0/rt/v5/audit/${base}_v005_loops.npz > contact/${id}.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz fam/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1
  echo "AEEVAL $id done"; }
one ${AE_C1:-AEL1} MF-M-R & one ${AE_C2:-AELF190} MF-F-R & wait   # order 0f6aba8: AE_C1=AEL1-R1 AE_C2=AELF190-R1, AE_WORK=/tmp/claude-0/rt/ae/r1
echo AEEVAL_DONE
